"""Run a CPU LOSO OOF integrity smoke test or the explicitly requested full run."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.oof_pipeline import evaluate_oof_loso, evaluate_oof_predictions, write_validation_report

MANIFEST = ROOT / "results/final/dataset_manifest.csv"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--smoke-folds", type=int, default=2, help="Run 2 or 3 held-out subjects (default: 2)")
    parser.add_argument("--epochs", type=int, default=None, help="Training epochs per fold (smoke default: 1; full defaults to FINAL_PROTOCOL.yaml)")
    parser.add_argument("--batch-size", type=int, default=None, help="Batch size (defaults to FINAL_PROTOCOL.yaml)")
    parser.add_argument("--full", action="store_true", help="Explicitly run all 30 LOSO folds")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.full:
        selected_subjects = None
        epochs = args.epochs
        predictions_path = ROOT / "results/final/OOF_PREDICTIONS.csv"
        provenance_path = ROOT / "results/final/OOF_CHECKPOINT_PROVENANCE.csv"
        metrics_path = ROOT / "results/final/OOF_METRICS.json"
        report_path = ROOT / "results/final/OOF_PIPELINE_VALIDATION.md"
        smoke_samples_per_class = None
    else:
        if args.smoke_folds not in (2, 3):
            raise SystemExit("Smoke mode must run exactly 2 or 3 folds; use --full only for all 30 folds.")
        if args.epochs is not None and args.epochs < 1:
            raise SystemExit("--epochs must be positive")
        manifest = pd.read_csv(MANIFEST)
        valid = manifest.loc[manifest["valid"].astype(bool)]
        selected_subjects = sorted(valid["subject_id"].astype(str).unique())[:args.smoke_folds]
        epochs = args.epochs if args.epochs is not None else 1
        predictions_path = ROOT / "results/final/smoke_OOF_PREDICTIONS.csv"
        provenance_path = ROOT / "results/final/smoke_checkpoint_provenance.csv"
        metrics_path = ROOT / "results/final/smoke_OOF_METRICS.json"
        report_path = ROOT / "results/final/OOF_PIPELINE_VALIDATION.md"
        smoke_samples_per_class = 1

    result = evaluate_oof_loso(
        selected_subjects=selected_subjects,
        epochs=epochs,
        batch_size=args.batch_size,
        device="cpu",
        predictions_path=predictions_path,
        provenance_path=provenance_path,
        report_path=report_path,
        smoke_samples_per_class=smoke_samples_per_class,
    )

    first_metrics = evaluate_oof_predictions(result["predictions_path"], metrics_path)
    first_bytes = metrics_path.read_bytes()
    metrics_path.unlink()
    second_metrics = evaluate_oof_predictions(result["predictions_path"], metrics_path)
    exact_recompute = first_bytes == metrics_path.read_bytes() and first_metrics == second_metrics
    if not exact_recompute:
        raise SystemExit("STOP: OOF metrics did not reproduce exactly from the prediction CSV")
    write_validation_report(result, second_metrics, recompute_exact=exact_recompute)

    print(f"OOF predictions: {result['predictions_path']}")
    print(f"Checkpoint provenance: {result['provenance_path']}")
    print(f"Metrics (from prediction CSV only): {metrics_path}")
    print(f"Validation report: {result['report_path']}")
    print(f"Folds: {', '.join(result['selected_subjects'])}")
    for fold in result["fold_summaries"]:
        print(f"held_out_subject: {fold['held_out_subject']}")
        print(f"training_subjects: {fold['training_subjects']}")
        print(f"validation_subjects: {fold['validation_subjects']}")
        print(f"test_subject: {fold['held_out_subject']}")
        print(f"training_sample_count: {fold['training_sample_count']}")
        print(f"test_prediction_count: {fold['test_count']}")
    print(f"Prediction count: {result['prediction_count']}")
    print(f"Model parameters: {result['model_parameter_count']}")
    print("Metric delete-and-recompute: exact match")
    print("OOF SMOKE CHECK: PASS")


if __name__ == "__main__":
    main()
