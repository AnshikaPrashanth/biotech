"""Subject-held-out OOF training and prediction pipeline.

This module deliberately keeps prediction generation separate from metrics:
``evaluate_oof_loso`` writes fold predictions, while
``evaluate_oof_predictions`` derives metrics from a prediction CSV only.
"""
from __future__ import annotations

import gc
import copy
import hashlib
import json
import os
import random
import time
from functools import partial
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Dict, List, Optional, Sequence

import numpy as np
import pandas as pd
import torch
import yaml
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    balanced_accuracy_score,
    confusion_matrix,
    f1_score,
    matthews_corrcoef,
    precision_score,
    recall_score,
    roc_auc_score,
)
from torch.utils.data import DataLoader

from src.dataset import (
    IntelliRehabSequenceDataset,
    load_intellirehab_directory,
    parse_intellirehab_file,
    make_weighted_sampler,
    sequence_collate_fn,
)
from src.model import stgat_from_config
from train import run_fold as train_run_fold

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL_PATH = ROOT / "configs" / "FINAL_PROTOCOL.yaml"
REQUIRED_PREDICTION_COLUMNS = [
    "sample_id", "subject_id", "gesture_id", "fold", "y_true", "y_prob",
    "y_pred", "confidence", "model_version",
]


def _read_valid_manifest(manifest_path: Path) -> pd.DataFrame:
    frame = pd.read_csv(manifest_path)
    required = {
        "sample_id", "file_path", "subject_id", "gesture_id", "original_label",
        "binary_label", "frame_count", "valid",
    }
    missing = sorted(required - set(frame.columns))
    if missing:
        raise ValueError(f"Manifest missing columns: {missing}")
    valid = frame.loc[frame["valid"].astype(bool)].copy()
    if valid["sample_id"].duplicated().any():
        raise ValueError("Manifest contains duplicate sample_id values")
    if valid["original_label"].eq(3).any() or not valid["binary_label"].isin([0, 1]).all():
        raise ValueError("Valid manifest rows contain an excluded/non-binary label")
    return valid


def _load_protocol() -> Dict[str, Any]:
    with PROTOCOL_PATH.open("r", encoding="utf-8") as handle:
        protocol = yaml.safe_load(handle) or {}
    dataset_config = protocol.get("dataset", {})
    if not dataset_config.get("exclude_label_3"):
        raise ValueError("Frozen protocol must exclude label 3")
    if not dataset_config.get("use_frame_mask"):
        raise ValueError("Frozen protocol must enable frame masks")
    if dataset_config.get("padding_strategy") != "zero_padded_with_mask":
        raise ValueError("Unsupported padding strategy in frozen protocol")
    if not protocol.get("evaluation", {}).get("oof_only"):
        raise ValueError("Frozen protocol must require OOF-only evaluation")
    if not protocol.get("loso", {}).get("enabled") or int(protocol["loso"].get("folds", 0)) != 30:
        raise ValueError("Frozen protocol must configure 30-fold LOSO")
    return protocol


def _load_manifest_entries(valid_manifest: pd.DataFrame, root: Path) -> List[Dict[str, Any]]:
    entries: List[Dict[str, Any]] = []
    for row in valid_manifest.itertuples(index=False):
        file_path = (root / str(row.file_path)).resolve()
        if not file_path.is_file():
            raise FileNotFoundError(f"Manifest sample file does not exist: {file_path}")
        sequence, exercise, subject_id, parsed_label = parse_intellirehab_file(str(file_path))
        if str(subject_id) != str(row.subject_id):
            raise ValueError(f"Subject mismatch for sample {row.sample_id}: parsed {subject_id}")
        if parsed_label != int(row.binary_label):
            raise ValueError(f"Label mismatch for sample {row.sample_id}: parsed {parsed_label}")
        if int(sequence.shape[0]) != int(row.frame_count):
            raise ValueError(f"Frame-count mismatch for sample {row.sample_id}")
        entries.append({
            "sequence": sequence,
            "exercise_type": exercise,
            "subject_id": str(subject_id),
            "movement_label": int(row.binary_label),
            "file_path": str(file_path),
            "sample_id": str(row.sample_id),
            "gesture_id": int(row.gesture_id),
        })
    return entries


def _rss_mb() -> Optional[float]:
    try:
        import psutil
        return float(psutil.Process(os.getpid()).memory_info().rss / (1024 ** 2))
    except (ImportError, OSError):
        return None


def _evaluate_loader(
    model: torch.nn.Module,
    loader: DataLoader,
    device: torch.device,
    expected_sequence_length: int,
) -> tuple[float, List[Dict[str, Any]]]:
    model.eval()
    targets: List[int] = []
    predictions: List[Dict[str, Any]] = []
    with torch.no_grad():
        for batch in loader:
            sequences = batch["sequence"].to(device)
            mask = batch["mask"].to(device)
            if mask.shape != sequences.shape[:2] or mask.dtype != torch.bool:
                raise AssertionError("valid_frame_mask shape/dtype does not match sequence tensor")
            if sequences.shape[1] != expected_sequence_length:
                raise AssertionError("Batch sequence length does not match the frozen protocol")
            output = model(sequences, mask=mask)
            logits = output["logits"]
            probs = output["probabilities"]
            pred = torch.argmax(logits, dim=-1)
            targets.extend(batch["label"].tolist())
            if output["frame_attention"].shape != mask.shape:
                raise AssertionError("Temporal attention output does not preserve the frame-mask shape")
            invalid_attention = output["frame_attention"].masked_select(~mask)
            if invalid_attention.numel() and not torch.allclose(
                invalid_attention, torch.zeros_like(invalid_attention), atol=1e-6
            ):
                raise AssertionError("Padded frames have nonzero temporal attention")
            for index, file_path in enumerate(batch["file_path"]):
                probability = float(probs[index, 1].cpu())
                predicted = int(pred[index].cpu())
                predictions.append({
                    "file_path": str(Path(file_path).resolve()),
                    "y_true": int(batch["label"][index]),
                    "y_prob": probability,
                    "y_pred": predicted,
                    "confidence": float(probs[index, predicted].cpu()),
                    "valid_frame_mask": True,
                    "temporal_attention_masked_frames_zero": True,
                })
    accuracy = float(accuracy_score(targets, [item["y_pred"] for item in predictions]))
    return accuracy, predictions


def _assert_fold_integrity(
    fold_id: str,
    held_out_subject: str,
    train_subjects: Sequence[str],
    validation_subjects: Sequence[str],
    fold_predictions: Sequence[Dict[str, Any]],
    expected_rows: pd.DataFrame,
) -> None:
    test_subjects = {str(held_out_subject)}
    if held_out_subject in train_subjects:
        raise AssertionError(f"Held-out subject {held_out_subject} appears in training")
    if held_out_subject in validation_subjects:
        raise AssertionError(f"Held-out subject {held_out_subject} appears in validation")
    if set(train_subjects) & set(validation_subjects):
        raise AssertionError("Training/validation subject intersection is not empty")
    if set(train_subjects) & test_subjects:
        raise AssertionError("Training/test subject intersection is not empty")
    if set(validation_subjects) & test_subjects:
        raise AssertionError("Validation/test subject intersection is not empty")
    if not fold_predictions:
        raise AssertionError(f"Fold {fold_id} generated no predictions")
    if any(str(item["subject_id"]) != held_out_subject for item in fold_predictions):
        raise AssertionError(f"Fold {fold_id} emitted a prediction for a non-held-out subject")
    if any(item["subject_id"] in train_subjects for item in fold_predictions):
        raise AssertionError(f"Fold {fold_id} emitted a prediction for a training subject")
    if any(item["fold"] != fold_id for item in fold_predictions):
        raise AssertionError(f"Fold {fold_id} prediction has an invalid fold identifier")
    if len(fold_predictions) != len(expected_rows):
        raise AssertionError(
            f"Fold {fold_id} prediction count {len(fold_predictions)} != expected {len(expected_rows)}"
        )
    expected_ids = set(expected_rows["sample_id"].astype(str))
    actual_ids = {str(item["sample_id"]) for item in fold_predictions}
    if actual_ids != expected_ids:
        raise AssertionError(f"Fold {fold_id} predictions do not exactly match its valid manifest samples")
    if any(int(item["y_true"]) == 3 for item in fold_predictions):
        raise AssertionError("Label-3 sample found in fold predictions")


def _subject_roles(subjects: Sequence[str], outer_test_subject: str) -> tuple[List[str], List[str]]:
    """Use the first sorted development subject for validation; train on the rest."""
    development_subjects = sorted(str(subject) for subject in subjects if str(subject) != str(outer_test_subject))
    if len(development_subjects) < 2:
        raise ValueError("At least two development subjects are required for train/validation roles")
    validation_subjects = development_subjects[:1]
    training_subjects = development_subjects[1:]
    return validation_subjects, training_subjects


def run_loso_fold(
    *,
    entries: Sequence[Dict[str, Any]],
    outer_test_subject: str,
    inner_validation_subjects: Sequence[str],
    training_subjects: Sequence[str],
    config: Dict[str, Any],
    checkpoint_path: Path,
    epochs: int,
    batch_size: int,
    seed: int,
    smoke_samples_per_class: Optional[int] = None,
) -> tuple[Path, Dict[str, Any], Dict[str, Any]]:
    """Fit one LOSO fold with role-checked train/validation data and persist provenance."""
    outer_test_subject = str(outer_test_subject)
    validation_subjects = [str(subject) for subject in inner_validation_subjects]
    training_subjects = [str(subject) for subject in training_subjects]
    if not validation_subjects or len(validation_subjects) != len(set(validation_subjects)):
        raise ValueError("Inner validation subjects must be a nonempty unique list")
    if not training_subjects or len(training_subjects) != len(set(training_subjects)):
        raise ValueError("Training subjects must be a nonempty unique list")
    if outer_test_subject in training_subjects or outer_test_subject in validation_subjects:
        raise ValueError("Outer test subject cannot be assigned to training or validation")
    if set(training_subjects) & set(validation_subjects):
        raise ValueError("Training and validation subjects must be disjoint")

    subject_ids = {str(entry["subject_id"]) for entry in entries}
    expected_subjects = set(training_subjects) | set(validation_subjects) | {outer_test_subject}
    if subject_ids != expected_subjects:
        raise ValueError("Training, validation, and outer test roles must cover the dataset subjects exactly")
    sample_ids = [str(entry["sample_id"]) for entry in entries]
    if len(sample_ids) != len(set(sample_ids)):
        raise ValueError("Fold entries contain duplicate sample IDs")

    training_entries = [entry for entry in entries if str(entry["subject_id"]) in training_subjects]
    validation_entries = [entry for entry in entries if str(entry["subject_id"]) in validation_subjects]
    outer_test_entries = [entry for entry in entries if str(entry["subject_id"]) == outer_test_subject]
    if not training_entries or not validation_entries or not outer_test_entries:
        raise ValueError("Training, validation, and outer test roles must all contain samples")

    if smoke_samples_per_class is not None:
        if smoke_samples_per_class < 1:
            raise ValueError("smoke_samples_per_class must be positive")
        selected_training_entries = []
        for subject in training_subjects:
            subject_entries = sorted(
                (entry for entry in training_entries if str(entry["subject_id"]) == subject),
                key=lambda entry: str(entry["sample_id"]),
            )
            for label in (0, 1):
                candidates = [entry for entry in subject_entries if int(entry["movement_label"]) == label]
                selected_training_entries.extend(candidates[:smoke_samples_per_class])
        training_entries = selected_training_entries
        if {str(entry["subject_id"]) for entry in training_entries} != set(training_subjects):
            raise ValueError("Smoke subset must include at least one sample from every training subject")

    training_sample_ids = [str(entry["sample_id"]) for entry in training_entries]
    validation_sample_ids = [str(entry["sample_id"]) for entry in validation_entries]
    outer_test_sample_ids = {str(entry["sample_id"]) for entry in outer_test_entries}
    if set(training_sample_ids) & set(validation_sample_ids):
        raise AssertionError("Training and validation sample IDs overlap")
    if outer_test_sample_ids & (set(training_sample_ids) | set(validation_sample_ids)):
        raise AssertionError("Outer test samples appear in training or validation")
    if {str(entry["subject_id"]) for entry in training_entries} != set(training_subjects):
        raise AssertionError("Training subjects do not match the samples supplied to training")
    if {str(entry["subject_id"]) for entry in validation_entries} != set(validation_subjects):
        raise AssertionError("Validation subjects do not match the samples supplied to validation")

    protocol = copy.deepcopy(config)
    effective_training_config = dict(protocol["training"])
    effective_training_config.setdefault("loss_type", "weighted_ce")
    model_config = protocol["model"]
    sequence_length = int(protocol["dataset"]["sequence_length"])
    device = torch.device(protocol.get("device", "cpu"))
    if device.type != "cpu":
        raise ValueError("The final OOF fold runner currently requires CPU")
    torch.set_num_threads(int(protocol.get("num_threads", 1)))
    torch.manual_seed(seed)
    np.random.seed(seed)
    random.seed(seed)

    train_dataset = IntelliRehabSequenceDataset(
        training_entries, augment=True, sequence_length=sequence_length
    )
    validation_dataset = IntelliRehabSequenceDataset(
        validation_entries, augment=False, sequence_length=sequence_length
    )
    sampler = make_weighted_sampler(training_entries, target_key="movement_label")
    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        sampler=sampler,
        num_workers=0,
        collate_fn=partial(sequence_collate_fn, max_length=sequence_length),
        pin_memory=False,
    )
    validation_loader = DataLoader(
        validation_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=0,
        collate_fn=partial(sequence_collate_fn, max_length=sequence_length),
        pin_memory=False,
    )
    model = stgat_from_config({
        "input_dim": model_config["input_dim"],
        "hidden_dim": model_config["hidden_dim"],
        "num_classes": model_config["num_classes"],
        "heads": model_config["heads"],
        "dropout": model_config["dropout"],
    }).to(device)
    fold_args = SimpleNamespace(
        epochs=int(epochs),
        lr=float(effective_training_config["lr"]),
        weight_decay=float(effective_training_config["weight_decay"]),
        patience=int(effective_training_config["patience"]),
    )
    started = time.perf_counter()
    validation_metrics, _, selected_epoch, training_loss = train_run_fold(
        model,
        train_loader,
        validation_loader,
        training_entries,
        f"outer_test_{outer_test_subject}",
        device,
        fold_args,
        writer=None,
        training_config=effective_training_config,
    )
    training_time_seconds = time.perf_counter() - started
    if validation_metrics is None:
        raise RuntimeError("No checkpoint was selected by inner validation")

    validation_accuracy = float(validation_metrics["accuracy"])
    validation_error_rate = 1.0 - validation_accuracy
    config_payload = json.dumps(protocol, sort_keys=True, separators=(",", ":"), default=str)
    protocol_hash = hashlib.sha256(config_payload.encode("utf-8")).hexdigest()
    training_metadata = {
        "outer_test_subject": outer_test_subject,
        "training_subjects": training_subjects,
        "training_sample_ids": training_sample_ids,
        "training_sample_count": len(training_sample_ids),
        "training_loss": float(training_loss),
        "training_time_seconds": training_time_seconds,
        "seed": int(seed),
        "model_parameter_count": sum(parameter.numel() for parameter in model.parameters()),
        "protocol_hash": protocol_hash,
    }
    validation_metadata = {
        "outer_test_subject": outer_test_subject,
        "inner_validation_subjects": validation_subjects,
        "validation_subjects": validation_subjects,
        "validation_sample_ids": validation_sample_ids,
        "selected_epoch": int(selected_epoch),
        "validation_metric": "accuracy",
        "validation_metric_value": validation_accuracy,
        "validation_error_rate": validation_error_rate,
    }
    checkpoint_metadata = {
        "model_state": model.state_dict(),
        **training_metadata,
        **validation_metadata,
        "held_out_subject": outer_test_subject,
        "training_sample_ids": training_sample_ids,
        "epoch": int(selected_epoch),
        "validation_error_rate_for_selection": validation_error_rate,
        "protocol_config": protocol,
    }
    checkpoint_path = Path(checkpoint_path)
    checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
    torch.save(checkpoint_metadata, checkpoint_path)
    return checkpoint_path, training_metadata, validation_metadata


def evaluate_oof_loso(
    *,
    selected_subjects: Optional[Sequence[str]] = None,
    epochs: Optional[int] = None,
    batch_size: Optional[int] = None,
    device: str = "cpu",
    manifest_path: Optional[Path] = None,
    data_root: Optional[Path] = None,
    predictions_path: Optional[Path] = None,
    provenance_path: Optional[Path] = None,
    report_path: Optional[Path] = None,
    smoke_samples_per_class: Optional[int] = None,
    seed: int = 42,
) -> Dict[str, Any]:
    """Train subject-disjoint folds, select by internal validation, and predict held-out subjects only."""
    protocol = _load_protocol()
    training_config = protocol["training"]
    model_config = protocol["model"]
    configured_manifest = ROOT / protocol["dataset"]["manifest_path"]
    manifest_path = Path(manifest_path or configured_manifest)
    if manifest_path.resolve() != configured_manifest.resolve():
        raise ValueError("OOF runner manifest must match the frozen final protocol")
    torch.set_num_threads(int(protocol.get("num_threads", 1)))
    valid_manifest = _read_valid_manifest(manifest_path)
    root = Path(data_root or ROOT).resolve()
    entries = _load_manifest_entries(valid_manifest, root)
    by_sample = {entry["sample_id"]: entry for entry in entries}
    by_path = {entry["file_path"]: entry for entry in entries}
    subjects = sorted({entry["subject_id"] for entry in entries})
    if len(subjects) != int(protocol["loso"]["folds"]):
        raise ValueError(
            f"Manifest has {len(subjects)} subjects but frozen protocol requires {protocol['loso']['folds']} LOSO folds"
        )
    fold_subjects = [str(value) for value in (selected_subjects or subjects)]
    unknown = sorted(set(fold_subjects) - set(subjects))
    if unknown:
        raise ValueError(f"Requested held-out subjects are absent from the valid manifest: {unknown}")
    if len(fold_subjects) != len(set(fold_subjects)):
        raise ValueError("Held-out subject list contains duplicates")
    if not fold_subjects:
        raise ValueError("At least one held-out subject is required")

    epoch_count = int(epochs if epochs is not None else training_config["epochs"])
    batch_size = int(batch_size if batch_size is not None else training_config["batch_size"])
    if epoch_count < 1 or batch_size < 1:
        raise ValueError("epochs and batch_size must be positive")
    device_obj = torch.device(device)
    if device_obj.type != "cpu":
        raise ValueError("This protocol runner is CPU-only; use device='cpu'")
    sequence_length = int(protocol["dataset"]["sequence_length"])
    output_predictions = Path(predictions_path or ROOT / "results/final/OOF_PREDICTIONS.csv")
    output_provenance = Path(provenance_path or ROOT / "results/final/checkpoint_provenance.csv")
    output_report = Path(report_path or ROOT / "results/final/OOF_PIPELINE_VALIDATION.md")
    checkpoint_dir = output_provenance.parent / (
        "smoke_checkpoints" if "smoke" in output_provenance.name.lower() else "oof_checkpoints"
    )
    for path in (output_predictions, output_provenance, output_report):
        path.parent.mkdir(parents=True, exist_ok=True)

    all_predictions: List[Dict[str, Any]] = []
    provenance_rows: List[Dict[str, Any]] = []
    fold_summaries: List[Dict[str, Any]] = []
    param_count: Optional[int] = None
    version = f"STGAT-h{model_config['hidden_dim']}-heads{model_config['heads']}-seq{sequence_length}-seed{seed}"

    for fold_number, held_out_subject in enumerate(fold_subjects, start=1):
        fold_id = f"fold_{held_out_subject}"
        fold_started = time.perf_counter()
        validation_subjects, train_subjects = _subject_roles(subjects, held_out_subject)
        test_rows = valid_manifest.loc[valid_manifest["subject_id"].astype(str) == held_out_subject]
        test_entries = [by_sample[str(sample_id)] for sample_id in test_rows["sample_id"]]
        if not test_entries:
            raise ValueError(f"Empty outer test set for {fold_id}")
        fold_seed = seed + fold_number - 1
        fold_config = copy.deepcopy(protocol)
        fold_config["seed"] = fold_seed
        fold_config["training"]["epochs"] = epoch_count
        fold_config["training"]["batch_size"] = batch_size
        checkpoint_path = checkpoint_dir / f"{fold_id}.pt"
        checkpoint_path, training_metadata, validation_metadata = run_loso_fold(
            entries=entries,
            outer_test_subject=held_out_subject,
            inner_validation_subjects=validation_subjects,
            training_subjects=train_subjects,
            config=fold_config,
            checkpoint_path=checkpoint_path,
            epochs=epoch_count,
            batch_size=batch_size,
            seed=fold_seed,
            smoke_samples_per_class=smoke_samples_per_class,
        )
        if param_count is None:
            param_count = int(training_metadata["model_parameter_count"])

        test_dataset = IntelliRehabSequenceDataset(
            test_entries, augment=False, sequence_length=sequence_length
        )
        model = stgat_from_config({
            "input_dim": model_config["input_dim"],
            "hidden_dim": model_config["hidden_dim"],
            "num_classes": model_config["num_classes"],
            "heads": model_config["heads"],
            "dropout": model_config["dropout"],
        }).to(device_obj)
        loaded = torch.load(checkpoint_path, map_location=device_obj, weights_only=True)
        if (
            loaded["outer_test_subject"] != held_out_subject
            or loaded["training_subjects"] != train_subjects
            or loaded["training_sample_ids"] != training_metadata["training_sample_ids"]
            or loaded["inner_validation_subjects"] != validation_subjects
            or loaded["validation_sample_ids"] != validation_metadata["validation_sample_ids"]
            or loaded["selected_epoch"] != validation_metadata["selected_epoch"]
            or loaded["protocol_hash"] != training_metadata["protocol_hash"]
        ):
            raise AssertionError(f"Checkpoint provenance does not match fold {fold_id}")
        if (
            set(loaded["training_sample_ids"]) & set(loaded["validation_sample_ids"])
            or held_out_subject in {
                str(entry["subject_id"])
                for entry in entries
                if str(entry["sample_id"]) in (
                    set(loaded["training_sample_ids"]) | set(loaded["validation_sample_ids"])
                )
            }
        ):
            raise AssertionError(f"Checkpoint samples violate role isolation for {fold_id}")
        model.load_state_dict(loaded["model_state"])

        test_loader = DataLoader(
            test_dataset, batch_size=batch_size, shuffle=False, num_workers=0,
            collate_fn=partial(sequence_collate_fn, max_length=sequence_length), pin_memory=False,
        )
        _, raw_predictions = _evaluate_loader(model, test_loader, device_obj, sequence_length)
        fold_predictions: List[Dict[str, Any]] = []
        for prediction in raw_predictions:
            entry = by_path[prediction["file_path"]]
            fold_predictions.append({
                "sample_id": entry["sample_id"],
                "subject_id": entry["subject_id"],
                "gesture_id": entry["gesture_id"],
                "fold": fold_id,
                "y_true": prediction["y_true"],
                "y_prob": prediction["y_prob"],
                "y_pred": prediction["y_pred"],
                "confidence": prediction["confidence"],
                "model_version": version,
            })
        _assert_fold_integrity(
            fold_id, held_out_subject, train_subjects, validation_subjects,
            fold_predictions, test_rows,
        )
        all_predictions.extend(fold_predictions)
        provenance_rows.append({
            "checkpoint_path": str(checkpoint_path.relative_to(ROOT)).replace("\\", "/"),
            "fold": fold_id,
            "held_out_subject": held_out_subject,
            "outer_test_subject": held_out_subject,
            "training_subjects": json.dumps(train_subjects),
            "training_sample_ids": json.dumps(training_metadata["training_sample_ids"]),
            "validation_subjects": json.dumps(validation_subjects),
            "validation_sample_ids": json.dumps(validation_metadata["validation_sample_ids"]),
            "selected_epoch": validation_metadata["selected_epoch"],
            "validation_metric": validation_metadata["validation_metric"],
            "validation_metric_value": validation_metadata["validation_metric_value"],
            "training_loss": training_metadata["training_loss"],
            "validation_error_rate": validation_metadata["validation_error_rate"],
            "seed": training_metadata["seed"],
            "protocol_hash": training_metadata["protocol_hash"],
        })
        fold_summaries.append({
            "fold": fold_id,
            "held_out_subject": held_out_subject,
            "checkpoint_path": str(checkpoint_path.relative_to(ROOT)).replace("\\", "/"),
            "training_subjects": train_subjects,
            "validation_subjects": validation_subjects,
            "test_count": len(fold_predictions),
            "training_sample_count": training_metadata["training_sample_count"],
            "training_time_seconds": training_metadata["training_time_seconds"],
            "fold_runtime_seconds": time.perf_counter() - fold_started,
            "rss_mb_before_cleanup": _rss_mb(),
            "valid_frame_mask_passed": True,
            "temporal_attention_respected_mask": all(
                item["temporal_attention_masked_frames_zero"] for item in raw_predictions
            ),
            "calibration_reference_source": "none; classifier OOF path does not call calibration or DTW",
            "calibration_sample_ids": [],
            "calibration_training_sample_ids": [],
            "calibration_test_sample_ids": [],
        })
        del loaded, model, test_loader, test_dataset, test_entries
        gc.collect()
        fold_summaries[-1]["rss_mb_after_release"] = _rss_mb()

    predictions_frame = pd.DataFrame(all_predictions, columns=REQUIRED_PREDICTION_COLUMNS)
    if predictions_frame["sample_id"].duplicated().any():
        raise AssertionError("OOF output contains duplicate sample_id values")
    valid_by_id = valid_manifest.set_index(valid_manifest["sample_id"].astype(str))
    if not predictions_frame["sample_id"].astype(str).isin(valid_by_id.index).all():
        raise AssertionError("OOF prediction references a sample missing from the valid manifest")
    if len(predictions_frame) and predictions_frame["sample_id"].astype(str).map(
        valid_by_id["valid"].astype(bool)
    ).eq(False).any():
        raise AssertionError("OOF prediction references an invalid manifest sample")
    if len(predictions_frame) and predictions_frame["fold"].isna().any():
        raise AssertionError("OOF prediction is missing a fold")
    fold_counts = predictions_frame.groupby("sample_id")["fold"].nunique()
    if not fold_counts.eq(1).all():
        raise AssertionError("Each sample must have exactly one fold assignment")
    if predictions_frame["y_true"].eq(3).any():
        raise AssertionError("Label-3 sample found in OOF predictions")

    predictions_frame.to_csv(output_predictions, index=False)
    pd.DataFrame(provenance_rows).to_csv(output_provenance, index=False)
    return {
        "predictions_path": output_predictions,
        "provenance_path": output_provenance,
        "report_path": output_report,
        "valid_manifest": valid_manifest,
        "fold_summaries": fold_summaries,
        "model_parameter_count": int(param_count or 0),
        "selected_subjects": fold_subjects,
        "prediction_count": len(predictions_frame),
        "model_version": version,
    }


def evaluate_oof_predictions(
    predictions_csv: Path | str,
    metrics_path: Optional[Path | str] = None,
) -> Dict[str, Any]:
    """Calculate final classification metrics from an OOF CSV without loading any checkpoint."""
    frame = pd.read_csv(predictions_csv)
    missing = [column for column in REQUIRED_PREDICTION_COLUMNS if column not in frame.columns]
    if missing:
        raise ValueError(f"OOF CSV missing required columns: {missing}")
    if frame.empty:
        raise ValueError("OOF CSV contains no predictions")
    if frame["sample_id"].duplicated().any():
        raise ValueError("OOF CSV contains duplicate sample_id values")
    targets = frame["y_true"].astype(int).to_numpy()
    probabilities = frame["y_prob"].astype(float).to_numpy()
    predictions = frame["y_pred"].astype(int).to_numpy()
    if not set(np.unique(targets)).issubset({0, 1}) or not set(np.unique(predictions)).issubset({0, 1}):
        raise ValueError("OOF labels and predictions must be binary")
    metrics: Dict[str, Any] = {
        "n_predictions": int(len(frame)),
        "accuracy": float(accuracy_score(targets, predictions)),
        "balanced_accuracy": float(balanced_accuracy_score(targets, predictions)),
        "precision_macro": float(precision_score(targets, predictions, labels=[0, 1], average="macro", zero_division=0)),
        "recall_macro": float(recall_score(targets, predictions, labels=[0, 1], average="macro", zero_division=0)),
        "macro_f1": float(f1_score(targets, predictions, labels=[0, 1], average="macro", zero_division=0)),
        "roc_auc": float(roc_auc_score(targets, probabilities)) if len(np.unique(targets)) == 2 else None,
        "pr_auc": float(average_precision_score(targets, probabilities)) if len(np.unique(targets)) == 2 else None,
        "mcc": float(matthews_corrcoef(targets, predictions)),
        "confusion_matrix": confusion_matrix(targets, predictions, labels=[0, 1]).tolist(),
    }
    if metrics_path is not None:
        destination = Path(metrics_path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(json.dumps(metrics, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return metrics


def write_validation_report(result: Dict[str, Any], metrics: Dict[str, Any], recompute_exact: bool) -> None:
    folds = result["fold_summaries"]
    lines = [
        "# OOF Pipeline Validation",
        "",
        "This is a pipeline-integrity smoke test, not a performance experiment.",
        "",
        "## Dataset",
        f"- Manifest: `results/final/dataset_manifest.csv`",
        f"- Valid dataset size: {len(result['valid_manifest'])} samples; predictions in this run: {result['prediction_count']}.",
        f"- Subject count: {result['valid_manifest']['subject_id'].nunique()}.",
        "- Data loaded only from valid manifest rows; label 3 is excluded.",
        "",
        "## Evaluation Path",
        "- Training source: valid manifest samples from all subjects except the outer held-out subject and one internal-validation subject; smoke mode uses the recorded deterministic subset from each training subject.",
        "- Training implementation: `train.run_fold()` and `train.train_one_epoch()`; validation/checkpoint selection uses `train.evaluate()` on the internal-validation subject only.",
        "- Inner-validation policy: choose the first subject in sorted subject-ID order after excluding the outer test subject; train on the remaining 28 development subjects. This deterministic rule uses no outer-test performance.",
        "- Validation source: all valid manifest samples for the selected internal-validation subject; checkpoint selection minimizes validation error rate (1 - accuracy), with the configured early-stopping delta applied to that same value.",
        "- Checkpoint source: best internal-validation state saved with exact training sample IDs and subject provenance, then reloaded before test inference.",
        "- Outer test source: valid manifest samples belonging only to the held-out subject.",
        f"- Prediction output: `{result['predictions_path'].relative_to(ROOT).as_posix()}`; metric aggregation: `evaluate_oof_predictions()` reads this CSV and loads no model checkpoint.",
        "",
        "## Fold Boundaries and Provenance",
    ]
    for fold in folds:
        lines.extend([
            f"### {fold['fold']}",
            f"- Held-out subject: `{fold['held_out_subject']}`",
            f"- Training subjects: `{', '.join(fold['training_subjects'])}`",
            f"- Validation subjects: `{', '.join(fold['validation_subjects'])}`",
            f"- Test subject: `{fold['held_out_subject']}`; test predictions: {fold['test_count']}.",
            f"- Training examples used: {fold['training_sample_count']} (smoke subset, represented by every training subject).",
            f"- Checkpoint: `{fold['checkpoint_path']}`; see `{result['provenance_path'].relative_to(ROOT).as_posix()}`.",
            "- Checkpoint epoch, validation accuracy, and its error-rate selection value are recorded in checkpoint metadata and provenance CSV.",
            f"- Training time: {fold['training_time_seconds']:.2f} seconds; total fold runtime: {fold['fold_runtime_seconds']:.2f} seconds.",
            f"- Approximate RSS before fold cleanup: {fold['rss_mb_before_cleanup']} MB; after releasing model/loaders: {fold['rss_mb_after_release']} MB.",
            "- Split assertions: held-out subject excluded from training and validation; training/test and validation/test intersections are empty.",
            "",
        ])
    lines.extend([
        "## OOF Integrity",
        "- Every prediction belongs to its fold's held-out subject and expected valid manifest sample set.",
        "- No training-subject predictions, duplicate sample IDs, invalid/missing manifest samples, or label-3 rows.",
        "- Every prediction has exactly one fold; per-fold prediction counts equal held-out valid manifest counts.",
        f"- Integrity assertions: PASS ({result['prediction_count']} predictions).",
        "",
        "## Calibration and DTW Provenance",
        "- The classifier OOF runner does not instantiate a calibrator or call calibration/DTW functions.",
        "- Calibration reference source: none; calibration sample IDs: none; training/test sample IDs used for calibration: none.",
        "- Separate legacy `evaluate_and_report.py` Part 7 fits ROM calibration from each subject's healthy sequences and evaluates that subject's compensated sequences. That is not an outer-subject OOF calibration protocol and is not invoked here.",
        "",
        "## EMA / Baseline Adaptation",
        "- No EMA or baseline adaptation is used by the classifier OOF prediction path.",
        "- The clinical `src/analysis_pipeline.py` has optional persisted ROM baseline drift: it updates after scoring a sequence under confidence/quality conditions, so prior sequences may influence later ROM-derived assessment. It does not update ST-GAT weights or its class prediction; it uses no ground-truth labels or future sequences. This is online downstream adaptation, outside this OOF experiment.",
        "",
        "## Baseline Split Compatibility",
        "- The legacy Part 8 baseline implementation groups by the same sorted subject IDs and uses `subject_ids != held_out_subject` for fitting and equality for that fold's held-out predictions; scaler/PCA fit only on its training rows.",
        "- Baselines were inspected but not run. Their current implementation aggregates per-fold arrays rather than writing the required OOF prediction schema; baseline OOF persistence remains follow-up work before baseline comparisons.",
        "",
        "## Padding and Masking",
        "- Train, internal validation, and held-out test loaders use 64-frame zero padding via `sequence_collate_fn` and its boolean `mask`.",
        "- The mask is passed to `STGAT.forward`, temporal attention, and masked temporal pooling; padded temporal-attention outputs were checked as zero.",
        f"- Mask verification: {'PASS' if all(fold['valid_frame_mask_passed'] and fold['temporal_attention_respected_mask'] for fold in folds) else 'FAIL'}.",
        "",
        "## Runtime and Memory",
        f"- Model parameters: {result['model_parameter_count']:,}.",
        "- CPU only; sequential folds; `num_workers=0`; model/optimizer/loaders are released and garbage-collected after each fold.",
        "- Per-fold runtime and approximate RSS are listed above.",
        "",
        "## OOF Metrics Reproduction",
        f"- Metrics calculated from the OOF CSV only; metric file deleted and recomputed identically: {'PASS' if recompute_exact else 'FAIL'}.",
        f"- Smoke metrics (not final performance): `{json.dumps(metrics, sort_keys=True)}`.",
        "",
        "## Issues and Scope",
        "- OOF training uses a deterministic smoke subset (one sample per available class per training subject); full mode uses every valid training sample.",
        "- Legacy `train.py` uses its sole held-out subject as both validation data and the basis for checkpoint selection, so it has no independent outer test set; it is not used as the OOF split constructor.",
        "- Legacy full-dataset inference in `evaluate_and_report.py` is explicitly gated as `legacy_full_dataset_evaluation`; it is not the OOF entry point.",
        "- No full 30-fold experiment was run. Smoke metrics are not paper-ready performance estimates.",
    ])
    Path(result["report_path"]).write_text("\n".join(lines) + "\n", encoding="utf-8")
