import copy

import pandas as pd
import pytest
import numpy as np
import torch

from src.oof_pipeline import (
    REQUIRED_PREDICTION_COLUMNS,
    _assert_fold_integrity,
    _subject_roles,
    evaluate_oof_predictions,
    run_loso_fold,
)
from src.dataset import sequence_collate_fn


def test_oof_metrics_are_read_from_prediction_csv(tmp_path):
    prediction_path = tmp_path / "predictions.csv"
    metrics_path = tmp_path / "metrics.json"
    pd.DataFrame([
        {"sample_id": "a", "subject_id": "101", "gesture_id": 0, "fold": "fold_101", "y_true": 0, "y_prob": 0.1, "y_pred": 0, "confidence": 0.9, "model_version": "test"},
        {"sample_id": "b", "subject_id": "101", "gesture_id": 1, "fold": "fold_101", "y_true": 1, "y_prob": 0.8, "y_pred": 1, "confidence": 0.8, "model_version": "test"},
    ], columns=REQUIRED_PREDICTION_COLUMNS).to_csv(prediction_path, index=False)

    metrics = evaluate_oof_predictions(prediction_path, metrics_path)

    assert metrics["n_predictions"] == 2
    assert metrics["accuracy"] == 1.0
    assert metrics["balanced_accuracy"] == 1.0
    assert metrics["roc_auc"] == 1.0
    assert metrics_path.exists()


def test_fold_integrity_rejects_held_out_subject_in_training():
    expected_rows = pd.DataFrame({"sample_id": ["a"]})
    prediction = [{
        "sample_id": "a", "subject_id": "101", "fold": "fold_101", "y_true": 0,
    }]
    with pytest.raises(AssertionError, match="appears in training"):
        _assert_fold_integrity(
            "fold_101", "101", ["101", "102"], [], prediction, expected_rows,
        )


def test_fold_integrity_requires_exact_held_out_manifest_samples():
    expected_rows = pd.DataFrame({"sample_id": ["a", "b"]})
    prediction = [{
        "sample_id": "a", "subject_id": "101", "fold": "fold_101", "y_true": 0,
    }]
    with pytest.raises(AssertionError, match="prediction count"):
        _assert_fold_integrity(
            "fold_101", "101", ["102"], ["103"], prediction, expected_rows,
        )


def test_smoke_fold_subject_roles_are_deterministic_and_disjoint():
    subjects = ["307", "102", "101", "103"]

    validation_101, training_101 = _subject_roles(subjects, "101")
    validation_102, training_102 = _subject_roles(subjects, "102")

    assert validation_101 == ["102"]
    assert validation_102 == ["101"]
    for outer, validation, training in (
        ("101", validation_101, training_101),
        ("102", validation_102, training_102),
    ):
        assert outer not in validation
        assert outer not in training
        assert set(training).isdisjoint(validation)
        assert set(training) | set(validation) | {outer} == set(subjects)


def test_collator_supports_fixed_length_boolean_frame_mask():
    batch = [
        {"sequence": np.ones((3, 25, 3), dtype=np.float32), "label": torch.tensor(0), "subject_id": "101", "exercise_type": "stand", "file_path": "a.txt"},
        {"sequence": np.ones((5, 25, 3), dtype=np.float32), "label": torch.tensor(1), "subject_id": "102", "exercise_type": "chair", "file_path": "b.txt"},
    ]

    collated = sequence_collate_fn(batch, max_length=8)

    assert collated["sequence"].shape == (2, 8, 25, 3)
    assert collated["mask"].dtype == torch.bool
    assert collated["mask"].sum(dim=1).tolist() == [3, 5]


def test_outer_test_perturbation_cannot_change_selected_checkpoint(tmp_path):
    rng = np.random.default_rng(123)
    entries = []
    for subject in ("train_a", "train_b", "validation", "outer_test"):
        for label in (0, 1):
            entries.append({
                "sample_id": f"{subject}_{label}",
                "subject_id": subject,
                "movement_label": label,
                "exercise_type": "synthetic",
                "file_path": f"{subject}_{label}.txt",
                "sequence": rng.normal(size=(5, 25, 3)).astype(np.float32),
            })

    config = {
        "seed": 7,
        "device": "cpu",
        "num_threads": 1,
        "dataset": {"sequence_length": 8},
        "training": {
            "lr": 0.0002,
            "weight_decay": 0.0001,
            "patience": 2,
            "early_stopping_delta": 0.001,
            "num_workers": 0,
        },
        "model": {
            "input_dim": 3,
            "hidden_dim": 8,
            "num_classes": 2,
            "heads": 2,
            "dropout": 0.0,
        },
    }
    roles = {
        "outer_test_subject": "outer_test",
        "inner_validation_subjects": ["validation"],
        "training_subjects": ["train_a", "train_b"],
        "config": config,
        "epochs": 3,
        "batch_size": 2,
        "seed": 7,
    }

    checkpoint_a, training_a, validation_a = run_loso_fold(
        entries=entries, checkpoint_path=tmp_path / "checkpoint_a.pt", **roles
    )
    changed_test_entries = copy.deepcopy(entries)
    for entry in changed_test_entries:
        if entry["subject_id"] == "outer_test":
            entry["sequence"][:] = 1_000_000.0
            entry["movement_label"] = 1 - entry["movement_label"]
    checkpoint_b, training_b, validation_b = run_loso_fold(
        entries=changed_test_entries, checkpoint_path=tmp_path / "checkpoint_b.pt", **roles
    )

    assert training_a["training_loss"] == training_b["training_loss"]
    assert training_a["training_subjects"] == training_b["training_subjects"]
    assert training_a["training_sample_ids"] == training_b["training_sample_ids"]
    assert validation_a == validation_b
    assert validation_a["selected_epoch"] == validation_b["selected_epoch"]
    assert validation_a["validation_metric"] == validation_b["validation_metric"]
    assert validation_a["validation_error_rate"] == validation_b["validation_error_rate"]
    assert set(training_a["training_sample_ids"]).isdisjoint(validation_a["validation_sample_ids"])
    assert "outer_test" not in training_a["training_subjects"]
    assert "outer_test" not in validation_a["inner_validation_subjects"]

    state_a = torch.load(checkpoint_a, map_location="cpu", weights_only=True)["model_state"]
    state_b = torch.load(checkpoint_b, map_location="cpu", weights_only=True)["model_state"]
    assert state_a.keys() == state_b.keys()
    assert all(torch.equal(state_a[key], state_b[key]) for key in state_a)
