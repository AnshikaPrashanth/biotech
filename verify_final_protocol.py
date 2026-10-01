"""Smoke test for the repository's final LOSO protocol and manifest contract."""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parent
CONFIG_PATH = ROOT / "configs" / "FINAL_PROTOCOL.yaml"
MANIFEST_PATH = ROOT / "results" / "final" / "dataset_manifest.csv"
PROTOCOL_NOTES_PATH = ROOT / "results" / "final" / "PROTOCOL_NOTES.md"


def _fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def main() -> None:
    print("=== FINAL PROTOCOL SMOKE TEST ===")

    if not CONFIG_PATH.exists():
        _fail(f"Missing protocol config: {CONFIG_PATH}")
    if not MANIFEST_PATH.exists():
        _fail(f"Missing dataset manifest: {MANIFEST_PATH}")
    if not PROTOCOL_NOTES_PATH.exists():
        _fail(f"Missing protocol notes: {PROTOCOL_NOTES_PATH}")

    with CONFIG_PATH.open("r", encoding="utf-8") as handle:
        config = yaml.safe_load(handle) or {}

    dataset_cfg = config.get("dataset", {})
    manifest_cfg = dataset_cfg.get("manifest_path")
    if manifest_cfg is None:
        _fail("dataset.manifest_path is missing from configs/FINAL_PROTOCOL.yaml")
    if str(Path(manifest_cfg)).replace("\\", "/") != "results/final/dataset_manifest.csv":
        _fail(f"Unexpected manifest path in config: {manifest_cfg!r}")
    if not dataset_cfg.get("exclude_label_3", False):
        _fail("dataset.exclude_label_3 must be true in the final protocol")
    if not config.get("evaluation", {}).get("oof_only", False):
        _fail("evaluation.oof_only must be true in the final protocol")

    df = pd.read_csv(MANIFEST_PATH)
    required_columns = {
        "sample_id",
        "file_path",
        "subject_id",
        "gesture_id",
        "original_label",
        "binary_label",
        "frame_count",
        "valid",
        "excluded_reason",
    }
    missing_columns = sorted(required_columns - set(df.columns))
    if missing_columns:
        _fail(f"Manifest is missing required columns: {missing_columns}")

    valid_rows = df[df["valid"] == True].copy()
    if len(valid_rows) != 2577:
        _fail(f"Expected 2577 valid rows, but found {len(valid_rows)}")
    if valid_rows["original_label"].eq(3).any():
        _fail("Label 3 rows must not remain in the valid manifest")
    if valid_rows["binary_label"].isin([0, 1]).all() is False:
        _fail("Valid manifest rows must use binary labels {0, 1} only")
    if df["valid"].sum() != 2577:
        _fail(f"Manifest valid count mismatch: expected 2577, got {int(df['valid'].sum())}")
    if df["subject_id"].nunique() != 30:
        _fail(f"Expected 30 unique subjects, found {df['subject_id'].nunique()}")
    if len(df) != 2589:
        _fail(f"Expected 2589 total manifest rows including exclusions, found {len(df)}")

    notes_text = PROTOCOL_NOTES_PATH.read_text(encoding="utf-8")
    if "2,577" not in notes_text and "2577" not in notes_text:
        _fail("Protocol notes do not reference the final valid-sample count")
    if "30" not in notes_text:
        _fail("Protocol notes do not reference the LOSO subject count")

    print(f"Total rows: {len(df)}")
    print(f"Valid rows: {len(valid_rows)}")
    print(f"Excluded rows: {int((df['valid'] == False).sum())}")
    print(f"Subjects: {df['subject_id'].nunique()}")
    print("Protocol manifest and label filter are valid.")
    print("FINAL PROTOCOL CHECK: PASS")


if __name__ == "__main__":
    main()
