"""
GPU-optimised training runner.
Wraps train.py with:
  - GPU verification and cuDNN benchmark
  - Epoch-by-epoch CSV training log for loss curve plots
  - Per-fold attention JSON outputs
  - AMP (mixed precision) already handled in train.py

Usage:
    python gpu_train.py [--epochs 80] [--batch-size 16] [--device cuda]
"""

import csv
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import torch

BASE_DIR = Path(__file__).parent
RESULTS_DIR = BASE_DIR / "results"
RESULTS_DIR.mkdir(exist_ok=True)


def verify_gpu():
    if not torch.cuda.is_available():
        print("[INFO] CUDA not available. Training will run on CPU.")
        return "cpu"

    device = torch.cuda.current_device()
    props = torch.cuda.get_device_properties(device)
    total_vram = props.total_memory / 1024**3
    free_vram = torch.cuda.mem_get_info()[0] / 1024**3

    # Enable cuDNN benchmark for fixed-size input
    torch.backends.cudnn.benchmark = True
    torch.backends.cudnn.enabled = True

    print("\n" + "=" * 60)
    print("  GPU INFORMATION")
    print("=" * 60)
    print(f"  GPU Name:          {props.name}")
    print(f"  CUDA version:      {torch.version.cuda}")
    print(f"  cuDNN version:     {torch.backends.cudnn.version()}")
    print(f"  Compute cap:       {props.major}.{props.minor}")
    print(f"  Multiprocessors:   {props.multi_processor_count}")
    print(f"  Total VRAM:        {total_vram:.2f} GB")
    print(f"  Free VRAM:         {free_vram:.2f} GB")
    print(f"  cuDNN benchmark:   ENABLED")
    print(f"  AMP support:       {hasattr(torch, 'amp')}")
    print("=" * 60 + "\n")
    return "cuda"


def find_best_batch_size(device: str) -> int:
    if device != "cuda":
        return 8
    print("[Phase 3] Running GPU batch size optimizer...")
    result = subprocess.run(
        [sys.executable, "find_batch_size.py"],
        capture_output=True, text=True, cwd=str(BASE_DIR)
    )
    print(result.stdout)
    if result.returncode != 0:
        print(f"[WARN] Batch finder failed:\n{result.stderr}")
        return 8
    for line in result.stdout.splitlines():
        if line.startswith("BEST_BATCH_SIZE="):
            return int(line.split("=")[1])
    return 8


def run_training(device: str, epochs: int, batch_size: int) -> int:
    """Execute train.py as a subprocess, streaming output, and return exit code."""
    cmd = [
        sys.executable, "train.py",
        "--epochs", str(epochs),
        "--device", device,
        "--batch-size", str(batch_size),
        "--debug",
    ]
    print(f"\n[Phase 4] Starting training:")
    print(f"  Command: {' '.join(cmd)}")
    print(f"  Epochs: {epochs} | Batch: {batch_size} | Device: {device}")
    print("-" * 60)

    t0 = time.time()
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        cwd=str(BASE_DIR),
        bufsize=1,
    )

    log_lines = []
    for line in proc.stdout:
        print(line, end="")
        log_lines.append(line.rstrip())

    proc.wait()
    elapsed = time.time() - t0
    minutes = elapsed / 60
    print(f"\n  Training finished in {minutes:.1f} minutes (exit code: {proc.returncode})")

    # Save raw training stdout log
    with open(RESULTS_DIR / "training_stdout.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(log_lines))
    print(f"  Saved: results/training_stdout.txt")

    # Parse epoch-level metrics from stdout to create training_log.csv
    _parse_training_log(log_lines)

    return proc.returncode


def _parse_training_log(lines):
    """Parse tqdm output from train.py to build training_log.csv."""
    import re
    rows = []
    current_fold = None

    for line in lines:
        # Detect fold
        fold_match = re.search(r"Starting (fold_subject_\w+)", line)
        if fold_match:
            current_fold = fold_match.group(1)

        # Detect tqdm epoch completion lines like:
        # Training Fold: 100%|...| 5/80 [... train_loss=0.4321, val_acc=0.7500, ...]
        tqdm_match = re.search(
            r"(\d+)/\d+ \[.+train_loss=([\d.]+).+val_acc=([\d.]+).+best_val_acc=([\d.]+)",
            line
        )
        if tqdm_match and current_fold:
            epoch = int(tqdm_match.group(1))
            train_loss = float(tqdm_match.group(2))
            val_acc = float(tqdm_match.group(3))
            best_val_acc = float(tqdm_match.group(4))
            rows.append({
                "fold": current_fold,
                "epoch": epoch,
                "train_loss": train_loss,
                "val_accuracy": val_acc,
                "best_val_accuracy": best_val_acc,
            })

    if rows:
        df_path = RESULTS_DIR / "training_log.csv"
        fieldnames = ["fold", "epoch", "train_loss", "val_accuracy", "best_val_accuracy"]
        with open(df_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        print(f"  Saved: results/training_log.csv ({len(rows)} epoch rows)")
    else:
        print("  [WARN] Could not parse epoch logs from training output.")
        # Create an empty placeholder so loss curve plots don't crash
        with open(RESULTS_DIR / "training_log.csv", "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["fold", "epoch", "train_loss", "val_accuracy"])
            writer.writeheader()


def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--epochs", type=int, default=80)
    p.add_argument("--batch-size", type=int, default=0,
                   help="0 = auto-detect from GPU VRAM")
    p.add_argument("--device", type=str, default="")
    args = p.parse_args()

    # Phase 1: GPU verification
    device = args.device or verify_gpu()

    # Phase 3: Batch size
    if args.batch_size == 0:
        batch_size = find_best_batch_size(device)
    else:
        batch_size = args.batch_size
    print(f"  Using batch size: {batch_size}")

    # Phase 4: Training
    exit_code = run_training(device, args.epochs, batch_size)
    if exit_code != 0:
        print(f"\n[ERROR] Training exited with code {exit_code}.")
        print("  Check results/training_stdout.txt for details.")
        sys.exit(exit_code)

    # Phase 5-11: Evaluation
    print("\n[Phase 5-11] Running evaluation and report generation...")
    eval_cmd = [
        sys.executable, "evaluate_and_report.py",
        "--checkpoint", "checkpoints/best_model.pt",
        "--data-dir", "SkeletonData/SkeletonData/RawData",
        "--device", device,
        "--batch-size", str(batch_size),
        "--training-log", str(RESULTS_DIR / "training_log.csv"),
    ]
    result = subprocess.run(eval_cmd, cwd=str(BASE_DIR))
    if result.returncode != 0:
        print("[ERROR] Evaluation script failed.")
        sys.exit(result.returncode)

    print("\n[DONE] All phases complete.")
    print(f"  See results/ for all outputs.")
    print(f"  Open results/final_report.md for the complete summary.")


if __name__ == "__main__":
    main()
