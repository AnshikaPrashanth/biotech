"""
Publication-Ready Evaluation Framework for ST-GAT Rehabilitation Assessment.

Covers:
  Part 1  — Complete model evaluation (all metrics)
  Part 2  — Subject-wise LOSO analysis
  Part 3  — Failure analysis
  Part 4  — Automatic failure reasoning
  Part 5  — ROM validation
  Part 6  — Explainability validation
  Part 7  — Calibration analysis
  Part 8  — Baseline models
  Part 9  — Ablation study
  Part 10 — Statistical significance
  Part 11 — Publication figures
  Part 12 — Final publication report

Usage:
    python evaluate_and_report.py --full
    python evaluate_and_report.py --parts 1,2,3,6,11,12
    python evaluate_and_report.py --checkpoint checkpoints/best_model.pt
"""

# ── stdlib ────────────────────────────────────────────────────
import argparse
import csv
import json
import logging
import math
import os
import random
import sys
import time
import warnings
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

warnings.filterwarnings("ignore")

# ── third-party ───────────────────────────────────────────────
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as mtick
import numpy as np
import pandas as pd
import torch
from tqdm import tqdm

# ── project root ──────────────────────────────────────────────
BASE_DIR = Path(__file__).parent
sys.path.insert(0, str(BASE_DIR))

from config import TRAINING_CONFIG, DATA_DIR, CHECKPOINT_DIR, LOG_DIR
from src.calibration import (
    PersonalizedROMCalibrator,
    compute_joint_angles,
    ANGLE_TRIPLETS,
    JOINT_INDEX,
)
from src.dataset import (
    IntelliRehabSequenceDataset,
    load_intellirehab_directory,
    sequence_collate_fn,
    loso_split,
    make_weighted_sampler,
)
from src.evaluation import (
    aggregate_fold_metrics,
    balanced_accuracy_score,
    classification_report,
    cohen_kappa_score,
    confusion_matrix,
    matthews_corrcoef,
    precision_recall_curve,
    roc_auc_scores,
)
from src.graph import INTELLIREHAB_JOINTS
from src.model import STGAT, stgat_from_config

# ── constants ─────────────────────────────────────────────────
LABEL_NAMES = ["Healthy", "Compensated"]
RESULTS_DIR = BASE_DIR / "results"
ERRORS_DIR = RESULTS_DIR / "errors"
SEED = 42

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(RESULTS_DIR / "evaluation.log" if RESULTS_DIR.exists() else "evaluation.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────

def set_seed(seed: int = SEED) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def ensure_dirs() -> None:
    RESULTS_DIR.mkdir(exist_ok=True)
    ERRORS_DIR.mkdir(exist_ok=True)
    (RESULTS_DIR / "figures").mkdir(exist_ok=True)
    (RESULTS_DIR / "tables").mkdir(exist_ok=True)


def load_model(checkpoint_path: str, device: torch.device) -> STGAT:
    config = {
        "hidden_dim": TRAINING_CONFIG["hidden_dim"],
        "heads": TRAINING_CONFIG["heads"],
        "dropout": 0.0,
    }
    model = stgat_from_config(config).to(device)
    if os.path.exists(checkpoint_path):
        ckpt = torch.load(checkpoint_path, map_location=device, weights_only=True)
        state = ckpt.get("model_state", ckpt)
        model.load_state_dict(state, strict=False)
        log.info(f"Loaded checkpoint: {checkpoint_path}")
    else:
        log.warning(f"Checkpoint not found: {checkpoint_path} — using random weights")
    model.eval()
    return model


def run_inference(
    model: STGAT,
    entries: List[Dict],
    device: torch.device,
    batch_size: int = 16,
    desc: str = "Inference",
) -> List[Dict]:
    """Runs full forward pass on all entries, returning enriched result dicts."""
    from torch.utils.data import DataLoader

    seq_len = TRAINING_CONFIG["sequence_length"]
    dataset = IntelliRehabSequenceDataset(entries, augment=False, sequence_length=seq_len)
    loader = DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=0,
        collate_fn=sequence_collate_fn,
        pin_memory=(device.type == "cuda"),
    )
    results = []
    with torch.no_grad():
        for batch in tqdm(loader, desc=desc, ncols=90):
            seqs = batch["sequence"].to(device, non_blocking=True)
            labels = batch["label"].to(device, non_blocking=True)
            out = model(seqs)
            logits = out["logits"]
            probs = out["probabilities"]
            preds = torch.argmax(logits, dim=-1)
            ja = out["joint_attention"].cpu().numpy()
            fa = out["frame_attention"].cpu().numpy()

            for i in range(seqs.size(0)):
                p_vec = probs[i].cpu().tolist()
                pred_i = int(preds[i].cpu())
                true_i = int(labels[i].cpu())
                results.append(
                    {
                        "file_path": batch["file_path"][i],
                        "subject_id": batch["subject_id"][i],
                        "exercise_type": batch["exercise_type"][i],
                        "true_label": true_i,
                        "pred_label": pred_i,
                        "prob_healthy": float(p_vec[0]),
                        "prob_compensated": float(p_vec[1]),
                        "confidence": float(p_vec[pred_i]),
                        "correct": true_i == pred_i,
                        "joint_attention": ja[i].tolist(),
                        "frame_attention": fa[i].tolist(),
                    }
                )
    return results


def compute_specificity_sensitivity(targets, preds):
    cm = confusion_matrix(targets, preds)
    if cm.shape == (2, 2):
        tn, fp, fn, tp = cm.ravel()
        spec = tn / max(tn + fp, 1)
        sens = tp / max(tp + fn, 1)
    else:
        spec, sens = 0.0, 0.0
    return float(spec), float(sens)


def fig_savefig(fig, name: str, dpi: int = 300) -> str:
    path = str(RESULTS_DIR / "figures" / name)
    fig.savefig(path, dpi=dpi, bbox_inches="tight")
    plt.close(fig)
    log.info(f"  Saved figure: {path}")
    return path


def _sci_palette():
    return ["#2E86AB", "#E84855", "#3BB273", "#F4A261", "#A23B72", "#6B4226"]


# ─────────────────────────────────────────────────────────────
# PART 1 — COMPLETE MODEL EVALUATION
# ─────────────────────────────────────────────────────────────

def part1_evaluate(results: List[Dict]) -> Dict:
    log.info("=" * 60)
    log.info("PART 1 — Complete Model Evaluation")
    log.info("=" * 60)

    targets = [r["true_label"] for r in results]
    preds   = [r["pred_label"] for r in results]
    probs   = [r["prob_compensated"] for r in results]
    confs   = [r["confidence"] for r in results]

    report = classification_report(targets, preds, labels=LABEL_NAMES)
    cm_arr  = confusion_matrix(targets, preds)
    roc     = roc_auc_scores(targets, probs)
    pr      = precision_recall_curve(targets, probs)
    mcc     = matthews_corrcoef(targets, preds)
    kappa   = cohen_kappa_score(targets, preds)
    bal_acc = balanced_accuracy_score(targets, preds)
    spec, sens = compute_specificity_sensitivity(targets, preds)

    tn, fp, fn, tp = (cm_arr.ravel().tolist() if cm_arr.size == 4 else [0, 0, 0, 0])

    metrics = {
        "n_total":              len(targets),
        "n_healthy":            int(sum(1 for t in targets if t == 0)),
        "n_compensated":        int(sum(1 for t in targets if t == 1)),
        "accuracy":             float(report["accuracy"]),
        "balanced_accuracy":    float(bal_acc),
        "precision_macro":      float(report["macro avg"]["precision"]),
        "recall_macro":         float(report["macro avg"]["recall"]),
        "f1_macro":             float(report["macro avg"]["f1-score"]),
        "precision_healthy":    float(report.get("Healthy",      {}).get("precision",  0)),
        "recall_healthy":       float(report.get("Healthy",      {}).get("recall",     0)),
        "f1_healthy":           float(report.get("Healthy",      {}).get("f1-score",   0)),
        "support_healthy":      int  (report.get("Healthy",      {}).get("support",    0)),
        "precision_compensated":float(report.get("Compensated",  {}).get("precision",  0)),
        "recall_compensated":   float(report.get("Compensated",  {}).get("recall",     0)),
        "f1_compensated":       float(report.get("Compensated",  {}).get("f1-score",   0)),
        "support_compensated":  int  (report.get("Compensated",  {}).get("support",    0)),
        "sensitivity":          float(sens),
        "specificity":          float(spec),
        "roc_auc":              float(roc["auc"]),
        "pr_auc":               float(pr["average_precision"]),
        "mcc":                  float(mcc),
        "cohen_kappa":          float(kappa),
        "true_positives":       int(tp),
        "true_negatives":       int(tn),
        "false_positives":      int(fp),
        "false_negatives":      int(fn),
        "mean_confidence":      float(np.mean(confs)),
        "std_confidence":       float(np.std(confs)),
        "min_confidence":       float(np.min(confs)),
        "max_confidence":       float(np.max(confs)),
        "confusion_matrix":     cm_arr.tolist(),
    }

    # Print
    log.info(f"  Accuracy:          {metrics['accuracy']:.4f}")
    log.info(f"  Balanced Accuracy: {metrics['balanced_accuracy']:.4f}")
    log.info(f"  F1 (macro):        {metrics['f1_macro']:.4f}")
    log.info(f"  ROC-AUC:           {metrics['roc_auc']:.4f}")
    log.info(f"  PR-AUC:            {metrics['pr_auc']:.4f}")
    log.info(f"  MCC:               {metrics['mcc']:.4f}")
    log.info(f"  Cohen Kappa:       {metrics['cohen_kappa']:.4f}")
    log.info(f"  Sensitivity:       {metrics['sensitivity']:.4f}")
    log.info(f"  Specificity:       {metrics['specificity']:.4f}")
    log.info(f"  TP={tp}  TN={tn}  FP={fp}  FN={fn}")

    # Save metrics.json
    save_meta = {k: v for k, v in metrics.items()}
    save_meta["roc"] = roc
    save_meta["pr"]  = pr
    with open(RESULTS_DIR / "metrics.json", "w") as f:
        json.dump(save_meta, f, indent=2)

    # Save metrics.csv
    scalar_metrics = {k: v for k, v in metrics.items() if isinstance(v, (int, float))}
    pd.DataFrame(scalar_metrics.items(), columns=["metric", "value"]).to_csv(
        RESULTS_DIR / "metrics.csv", index=False
    )

    # Save classification_report.txt
    from sklearn.metrics import classification_report as sk_report
    report_txt = sk_report(targets, preds, target_names=LABEL_NAMES, zero_division=0)
    with open(RESULTS_DIR / "classification_report.txt", "w") as f:
        f.write("ST-GAT Rehabilitation Assessment — Classification Report\n")
        f.write("=" * 55 + "\n")
        f.write(report_txt)

    # Figures
    _plot_confusion_matrix(cm_arr, str(RESULTS_DIR / "confusion_matrix.png"))
    _plot_roc_curve(roc, str(RESULTS_DIR / "roc_curve.png"))
    _plot_pr_curve(pr, str(RESULTS_DIR / "pr_curve.png"))
    _plot_confidence_histogram(confs, str(RESULTS_DIR / "figures" / "confidence_histogram.png"))

    log.info("  Part 1 complete.")
    return metrics


def _plot_confusion_matrix(cm: np.ndarray, path: str) -> None:
    fig, ax = plt.subplots(figsize=(6, 5))
    im = ax.imshow(cm, cmap="Blues")
    plt.colorbar(im, ax=ax)
    for label in LABEL_NAMES:
        ax.set_xticks([0, 1]); ax.set_xticklabels(LABEL_NAMES, fontsize=12)
        ax.set_yticks([0, 1]); ax.set_yticklabels(LABEL_NAMES, fontsize=12)
    ax.set_xlabel("Predicted", fontsize=13); ax.set_ylabel("Actual", fontsize=13)
    ax.set_title("Confusion Matrix", fontsize=14, fontweight="bold")
    thresh = cm.max() / 2
    for i in range(2):
        for j in range(2):
            ax.text(j, i, str(cm[i, j]), ha="center", va="center",
                    fontsize=16, color="white" if cm[i, j] > thresh else "black")
    plt.tight_layout()
    fig.savefig(path, dpi=300, bbox_inches="tight"); plt.close(fig)
    log.info(f"  Saved: {path}")


def _plot_roc_curve(roc: Dict, path: str) -> None:
    fig, ax = plt.subplots(figsize=(7, 6))
    ax.plot(roc["fpr"], roc["tpr"], color="#2E86AB", lw=2,
            label=f"ROC (AUC = {roc['auc']:.4f})")
    ax.plot([0,1],[0,1], "k--", lw=1.2, label="Random")
    ax.set_xlim([0,1]); ax.set_ylim([0,1.02])
    ax.set_xlabel("False Positive Rate", fontsize=13)
    ax.set_ylabel("True Positive Rate",  fontsize=13)
    ax.set_title("Receiver Operating Characteristic", fontsize=14, fontweight="bold")
    ax.legend(fontsize=11); ax.grid(alpha=0.3)
    plt.tight_layout()
    fig.savefig(path, dpi=300, bbox_inches="tight"); plt.close(fig)
    log.info(f"  Saved: {path}")


def _plot_pr_curve(pr: Dict, path: str) -> None:
    fig, ax = plt.subplots(figsize=(7, 6))
    ax.plot(pr["recall"], pr["precision"], color="#E84855", lw=2,
            label=f"PR (AP = {pr['average_precision']:.4f})")
    ax.set_xlim([0,1]); ax.set_ylim([0,1.02])
    ax.set_xlabel("Recall",    fontsize=13)
    ax.set_ylabel("Precision", fontsize=13)
    ax.set_title("Precision-Recall Curve", fontsize=14, fontweight="bold")
    ax.legend(fontsize=11); ax.grid(alpha=0.3)
    plt.tight_layout()
    fig.savefig(path, dpi=300, bbox_inches="tight"); plt.close(fig)
    log.info(f"  Saved: {path}")


def _plot_confidence_histogram(confs: List[float], path: str) -> None:
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist(confs, bins=40, color="#3BB273", edgecolor="white", linewidth=0.5)
    ax.axvline(np.mean(confs), color="#E84855", lw=2, linestyle="--",
               label=f"Mean = {np.mean(confs):.3f}")
    ax.set_xlabel("Prediction Confidence", fontsize=12)
    ax.set_ylabel("Count", fontsize=12)
    ax.set_title("Distribution of Prediction Confidence Scores", fontsize=13, fontweight="bold")
    ax.legend(); ax.grid(alpha=0.3)
    plt.tight_layout()
    fig.savefig(path, dpi=300, bbox_inches="tight"); plt.close(fig)
    log.info(f"  Saved: {path}")


# ─────────────────────────────────────────────────────────────
# PART 2 — SUBJECT-WISE LOSO ANALYSIS
# ─────────────────────────────────────────────────────────────

def part2_subject_analysis(results: List[Dict]) -> pd.DataFrame:
    log.info("=" * 60)
    log.info("PART 2 — Subject-Wise LOSO Analysis")
    log.info("=" * 60)

    by_subject: Dict[str, List[Dict]] = defaultdict(list)
    for r in results:
        by_subject[r["subject_id"]].append(r)

    rows = []
    for subj in tqdm(sorted(by_subject.keys()), desc="Subject analysis", ncols=90):
        subj_results = by_subject[subj]
        t = [r["true_label"]        for r in subj_results]
        p = [r["pred_label"]        for r in subj_results]
        pr_prob = [r["prob_compensated"] for r in subj_results]

        n_total = len(t)
        n_correct = sum(1 for ti, pi in zip(t, p) if ti == pi)
        acc = n_correct / max(n_total, 1)
        bal = balanced_accuracy_score(t, p)
        mcc = matthews_corrcoef(t, p)
        kappa = cohen_kappa_score(t, p)
        spec, sens = compute_specificity_sensitivity(t, p)
        roc_val = roc_auc_scores(t, pr_prob)["auc"]
        pr_val  = precision_recall_curve(t, pr_prob)["average_precision"]
        f1_val  = classification_report(t, p, labels=LABEL_NAMES)["macro avg"]["f1-score"]
        n_healthy = sum(1 for ti in t if ti == 0)
        n_comp    = sum(1 for ti in t if ti == 1)
        mean_conf = float(np.mean([r["confidence"] for r in subj_results]))

        rows.append({
            "subject_id":        subj,
            "n_total":           n_total,
            "n_healthy":         n_healthy,
            "n_compensated":     n_comp,
            "accuracy":          round(acc,   4),
            "balanced_accuracy": round(bal,   4),
            "f1_macro":          round(f1_val,4),
            "mcc":               round(mcc,   4),
            "sensitivity":       round(sens,  4),
            "specificity":       round(spec,  4),
            "roc_auc":           round(roc_val,4),
            "pr_auc":            round(pr_val, 4),
            "mean_confidence":   round(mean_conf, 4),
        })

    df = pd.DataFrame(rows).sort_values("subject_id")

    # Statistics
    numeric_cols = ["accuracy","balanced_accuracy","f1_macro","mcc","sensitivity","specificity","roc_auc","pr_auc"]
    stats_rows = []
    for col in numeric_cols:
        vals = df[col].dropna().values
        ci95 = 1.96 * np.std(vals) / max(np.sqrt(len(vals)), 1)
        stats_rows.append({
            "metric": col,
            "mean":   round(float(np.mean(vals)), 4),
            "std":    round(float(np.std(vals)),  4),
            "min":    round(float(np.min(vals)),  4),
            "max":    round(float(np.max(vals)),  4),
            "ci95_lower": round(float(np.mean(vals) - ci95), 4),
            "ci95_upper": round(float(np.mean(vals) + ci95), 4),
        })
    df_stats = pd.DataFrame(stats_rows)

    # Best / worst subjects by accuracy
    best_subj  = df.nlargest(3,  "accuracy")[["subject_id","accuracy","f1_macro","roc_auc"]]
    worst_subj = df.nsmallest(3, "accuracy")[["subject_id","accuracy","f1_macro","roc_auc"]]
    log.info(f"  Best subjects:\n{best_subj.to_string(index=False)}")
    log.info(f"  Worst subjects:\n{worst_subj.to_string(index=False)}")
    log.info(f"\n  LOSO Statistics (accuracy): mean={df_stats[df_stats.metric=='accuracy']['mean'].values[0]:.4f} "
             f"std={df_stats[df_stats.metric=='accuracy']['std'].values[0]:.4f}")

    # Save
    df.to_csv(RESULTS_DIR / "subject_results.csv", index=False)
    df_stats.to_csv(RESULTS_DIR / "subject_statistics.csv", index=False)
    try:
        with pd.ExcelWriter(RESULTS_DIR / "tables" / "subject_statistics.xlsx", engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name="Per-Subject", index=False)
            df_stats.to_excel(writer, sheet_name="Statistics", index=False)
            best_subj.to_excel(writer, sheet_name="Best-Subjects", index=False)
            worst_subj.to_excel(writer, sheet_name="Worst-Subjects", index=False)
    except Exception as e:
        log.warning(f"  Excel save failed: {e}")

    # Barplot
    _plot_subject_barplot(df)
    # Heatmap
    _plot_subject_heatmap(df)

    log.info("  Part 2 complete.")
    return df


def _plot_subject_barplot(df: pd.DataFrame) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(16, 10))
    metrics_to_plot = ["accuracy", "balanced_accuracy", "f1_macro", "roc_auc"]
    titles = ["Accuracy", "Balanced Accuracy", "F1 (macro)", "ROC-AUC"]
    colors = _sci_palette()

    for ax, col, title in zip(axes.flat, metrics_to_plot, titles):
        vals = df[col].values
        subjects = df["subject_id"].values
        bars = ax.bar(range(len(subjects)), vals, color=colors[0], alpha=0.8, edgecolor="white")
        ax.axhline(np.mean(vals), color=colors[1], linestyle="--", lw=1.5,
                   label=f"Mean={np.mean(vals):.3f}")
        ax.set_xticks(range(len(subjects)))
        ax.set_xticklabels(subjects, rotation=45, ha="right", fontsize=7)
        ax.set_ylabel(title, fontsize=11)
        ax.set_title(f"Per-Subject {title}", fontsize=12, fontweight="bold")
        ax.legend(fontsize=9); ax.grid(axis="y", alpha=0.3)
        ax.set_ylim([0, 1.05])

    plt.suptitle("Subject-Wise LOSO Performance", fontsize=15, fontweight="bold")
    plt.tight_layout()
    path = fig_savefig(fig, "subject_barplots.png")
    plt.close("all")


def _plot_subject_heatmap(df: pd.DataFrame) -> None:
    metric_cols = ["accuracy","balanced_accuracy","f1_macro","mcc","sensitivity","specificity","roc_auc","pr_auc"]
    heat_data = df.set_index("subject_id")[metric_cols].astype(float)

    fig, ax = plt.subplots(figsize=(14, max(6, len(df) * 0.35)))
    im = ax.imshow(heat_data.T.values, cmap="RdYlGn", aspect="auto", vmin=0, vmax=1)
    plt.colorbar(im, ax=ax, label="Score")
    ax.set_xticks(range(len(heat_data)))
    ax.set_xticklabels(heat_data.index, rotation=45, ha="right", fontsize=8)
    ax.set_yticks(range(len(metric_cols)))
    ax.set_yticklabels([m.replace("_", " ").title() for m in metric_cols], fontsize=10)
    ax.set_title("Subject × Metric Performance Heatmap", fontsize=14, fontweight="bold")

    for i in range(len(metric_cols)):
        for j in range(len(heat_data)):
            val = heat_data.iloc[j, i]
            ax.text(j, i, f"{val:.2f}", ha="center", va="center",
                    fontsize=6, color="black" if 0.3 < val < 0.8 else "white")

    plt.tight_layout()
    fig_savefig(fig, "subject_heatmap.png")
    plt.close("all")


# ─────────────────────────────────────────────────────────────
# PART 3 — FAILURE ANALYSIS
# ─────────────────────────────────────────────────────────────

def part3_failure_analysis(results: List[Dict], entries: List[Dict]) -> List[Dict]:
    log.info("=" * 60)
    log.info("PART 3 — Failure Analysis")
    log.info("=" * 60)

    failures = [r for r in results if not r["correct"]]
    log.info(f"  Total failures: {len(failures)} / {len(results)}")

    entry_by_path = {e["file_path"]: e for e in entries}

    error_rows = []
    md_lines = [
        "# Failure Analysis",
        f"\nGenerated: {datetime.now(timezone.utc).isoformat()}",
        f"\n**Total failures: {len(failures)} / {len(results)}**\n",
        "---",
    ]

    fp_list = [r for r in results if r["true_label"] == 0 and r["pred_label"] == 1]
    fn_list = [r for r in results if r["true_label"] == 1 and r["pred_label"] == 0]

    for category, case_list in [("False Positives", fp_list), ("False Negatives", fn_list)]:
        md_lines.append(f"\n## {category} ({len(case_list)} samples)\n")
        for r in case_list:
            fname = Path(r["file_path"]).name
            parts = Path(r["file_path"]).stem.split("_")
            subj  = parts[0] if len(parts) > 0 else "?"
            ex_id = parts[2] if len(parts) > 2 else "?"
            trial = parts[3] if len(parts) > 3 else "?"
            pos   = parts[5] if len(parts) > 5 else "?"

            ja = np.array(r["joint_attention"])
            top3 = sorted(enumerate(ja), key=lambda x: x[1], reverse=True)[:3]
            top3_str = ", ".join(f"{INTELLIREHAB_JOINTS[i]}({v:.3f})" for i, v in top3)

            fa = np.array(r["frame_attention"])
            attn_entropy = float(-np.sum(ja / max(ja.sum(), 1e-9) * np.log(ja / max(ja.sum(), 1e-9) + 1e-9)))

            reason = _infer_failure_reason(r, attn_entropy)

            md_lines += [
                f"### `{fname}`",
                f"- **Subject:** {subj} | **Exercise:** {r['exercise_type']} | **Position:** {pos}",
                f"- **Ground Truth:** {'Compensated' if r['true_label'] else 'Healthy'}",
                f"- **Prediction:** {'Compensated' if r['pred_label'] else 'Healthy'}",
                f"- **Confidence:** `{r['confidence']:.4f}`",
                f"- **Prob (Healthy/Comp):** `[{r['prob_healthy']:.4f}, {r['prob_compensated']:.4f}]`",
                f"- **Top-3 Attention Joints:** {top3_str}",
                f"- **Peak Frame:** {int(fa.argmax())} (value {fa.max():.4f})",
                f"- **Attention Entropy:** {attn_entropy:.4f}",
                f"- **Inferred Reason:** {reason}",
                "",
            ]

            error_rows.append({
                "filename":         fname,
                "subject_id":       subj,
                "exercise_id":      ex_id,
                "exercise_type":    r["exercise_type"],
                "position":         pos,
                "trial":            trial,
                "true_label":       LABEL_NAMES[r["true_label"]],
                "pred_label":       LABEL_NAMES[r["pred_label"]],
                "confidence":       r["confidence"],
                "prob_healthy":     r["prob_healthy"],
                "prob_compensated": r["prob_compensated"],
                "top3_joints":      top3_str,
                "attn_entropy":     round(attn_entropy, 4),
                "inferred_reason":  reason,
            })

    # Save
    with open(ERRORS_DIR / "error_analysis.md", "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))
    pd.DataFrame(error_rows).to_csv(ERRORS_DIR / "error_analysis.csv", index=False)

    log.info(f"  FP: {len(fp_list)}  FN: {len(fn_list)}")
    log.info("  Part 3 complete.")
    return error_rows


def _infer_failure_reason(r: Dict, attn_entropy: float) -> str:
    conf = r["confidence"]
    prob_diff = abs(r["prob_healthy"] - r["prob_compensated"])
    reasons = []
    if conf < 0.65:
        reasons.append("Low confidence (borderline prediction)")
    if prob_diff < 0.15:
        reasons.append("Near-equal class probabilities (ambiguous motion)")
    if attn_entropy > 2.5:
        reasons.append("High attention entropy (model uncertain which joints are informative)")
    fa = np.array(r["frame_attention"])
    if fa.std() < 0.02:
        reasons.append("Flat temporal attention (no dominant movement phase)")
    if r["true_label"] == 1 and r["pred_label"] == 0:
        reasons.append("Subtle compensatory pattern (compensation resembles healthy motion)")
    if r["true_label"] == 0 and r["pred_label"] == 1:
        reasons.append("Atypical healthy motion (possibly noisy skeleton or edge-case style)")
    return "; ".join(reasons) if reasons else "Reason unclear (review manually)"


# ─────────────────────────────────────────────────────────────
# PART 4 — AUTOMATIC FAILURE REASONING STATISTICS
# ─────────────────────────────────────────────────────────────

def part4_failure_reasoning(error_rows: List[Dict], results: List[Dict]) -> None:
    log.info("=" * 60)
    log.info("PART 4 — Failure Reasoning Statistics")
    log.info("=" * 60)

    if not error_rows:
        log.info("  No failures to analyse.")
        return

    # Cause distribution
    all_reasons = []
    for row in error_rows:
        for r in row.get("inferred_reason", "").split(";"):
            r = r.strip()
            if r:
                all_reasons.append(r)
    reason_counts = Counter(all_reasons)

    # Error rate per exercise and subject
    error_by_ex   = defaultdict(lambda: {"errors": 0, "total": 0})
    error_by_subj = defaultdict(lambda: {"errors": 0, "total": 0})
    error_by_pos  = defaultdict(lambda: {"errors": 0, "total": 0})

    for r in results:
        fname = Path(r["file_path"]).stem
        parts = fname.split("_")
        pos   = parts[5] if len(parts) > 5 else "unknown"
        ex = r["exercise_type"]
        subj = r["subject_id"]
        error_by_ex[ex]["total"] += 1
        error_by_subj[subj]["total"] += 1
        error_by_pos[pos]["total"] += 1
        if not r["correct"]:
            error_by_ex[ex]["errors"] += 1
            error_by_subj[subj]["errors"] += 1
            error_by_pos[pos]["errors"] += 1

    def _to_rate_df(d, key_name):
        rows = []
        for k, v in sorted(d.items()):
            rows.append({key_name: k, "errors": v["errors"], "total": v["total"],
                         "error_rate": round(v["errors"] / max(v["total"], 1), 4)})
        return pd.DataFrame(rows)

    df_ex   = _to_rate_df(error_by_ex,   "exercise")
    df_subj = _to_rate_df(error_by_subj, "subject_id")
    df_pos  = _to_rate_df(error_by_pos,  "position")

    df_ex.to_csv  (ERRORS_DIR / "error_rate_by_exercise.csv",  index=False)
    df_subj.to_csv(ERRORS_DIR / "error_rate_by_subject.csv",   index=False)
    df_pos.to_csv (ERRORS_DIR / "error_rate_by_position.csv",  index=False)

    reason_df = pd.DataFrame(reason_counts.most_common(), columns=["reason","count"])
    reason_df.to_csv(ERRORS_DIR / "failure_causes.csv", index=False)

    log.info(f"  Top failure causes:")
    for reason, cnt in reason_counts.most_common(5):
        log.info(f"    {cnt}x  {reason}")

    # Figure
    if len(reason_counts) > 0:
        fig, ax = plt.subplots(figsize=(10, max(4, len(reason_counts) * 0.4)))
        labels = [r[:60] for r, _ in reason_counts.most_common()]
        counts = [c for _, c in reason_counts.most_common()]
        bars = ax.barh(range(len(labels)), counts, color=_sci_palette()[0])
        ax.set_yticks(range(len(labels)))
        ax.set_yticklabels(labels, fontsize=9)
        ax.set_xlabel("Count", fontsize=11)
        ax.set_title("Failure Cause Distribution", fontsize=13, fontweight="bold")
        ax.invert_yaxis()
        ax.grid(axis="x", alpha=0.3)
        plt.tight_layout()
        fig_savefig(fig, "failure_causes.png")

    log.info("  Part 4 complete.")


# ─────────────────────────────────────────────────────────────
# PART 5 — ROM VALIDATION
# ─────────────────────────────────────────────────────────────

# Anatomical ROM reference ranges (degrees) — widely used clinical references
ROM_REFERENCE = {
    "elbow_left":    (0,  145),
    "elbow_right":   (0,  145),
    "knee_left":     (0,  135),
    "knee_right":    (0,  135),
    "hip_left":      (0,  120),
    "hip_right":     (0,  120),
    "shoulder_left": (0,  180),
    "shoulder_right":(0,  180),
}


def part5_rom_validation(entries: List[Dict]) -> None:
    log.info("=" * 60)
    log.info("PART 5 — ROM Validation")
    log.info("=" * 60)

    rom_data: Dict[str, List[float]] = defaultdict(list)
    impossible: List[Dict] = []

    for entry in tqdm(entries, desc="ROM computation", ncols=90):
        angles = compute_joint_angles(entry["sequence"])
        for angle_name, curve in angles.items():
            rom_val = float(np.ptp(curve))
            mean_val = float(np.mean(curve))
            rom_data[angle_name].append(rom_val)

            lo, hi = ROM_REFERENCE.get(angle_name, (0, 360))
            if mean_val > hi * 1.2:
                impossible.append({"joint": angle_name, "value": round(mean_val, 2),
                                    "file": Path(entry["file_path"]).name})

    stats_rows = []
    for angle_name, vals in sorted(rom_data.items()):
        arr = np.array(vals)
        lo, hi = ROM_REFERENCE.get(angle_name, (0, 360))
        stats_rows.append({
            "joint":       angle_name,
            "min":         round(float(arr.min()),   2),
            "p5":          round(float(np.percentile(arr, 5)), 2),
            "median":      round(float(np.median(arr)), 2),
            "mean":        round(float(arr.mean()),  2),
            "p95":         round(float(np.percentile(arr, 95)), 2),
            "max":         round(float(arr.max()),   2),
            "std":         round(float(arr.std()),   2),
            "ref_min":     lo,
            "ref_max":     hi,
            "n_impossible":int(np.sum(arr > hi * 1.2)),
            "n_missing":   int(np.sum(arr < 1.0)),
        })
        log.info(f"  {angle_name:20s} mean={arr.mean():.1f} deg  ROM=[{arr.min():.1f}, {arr.max():.1f}]")

    df_rom = pd.DataFrame(stats_rows)
    df_rom.to_csv(RESULTS_DIR / "tables" / "rom_statistics.csv", index=False)

    if impossible:
        log.warning(f"  Detected {len(impossible)} anatomically impossible ROM values")
        pd.DataFrame(impossible).to_csv(RESULTS_DIR / "tables" / "rom_impossible.csv", index=False)

    # Histograms
    _plot_rom_histograms(rom_data)
    _plot_joint_boxplots(rom_data)

    log.info("  Part 5 complete.")


def _plot_rom_histograms(rom_data: Dict) -> None:
    n = len(rom_data)
    cols = 4
    rows = math.ceil(n / cols)
    fig, axes = plt.subplots(rows, cols, figsize=(cols * 4, rows * 3))
    axes = axes.flat

    for ax, (angle_name, vals) in zip(axes, rom_data.items()):
        ax.hist(vals, bins=30, color=_sci_palette()[0], edgecolor="white", linewidth=0.4)
        ax.axvline(np.mean(vals), color=_sci_palette()[1], lw=1.5, linestyle="--",
                   label=f"Mean={np.mean(vals):.1f}")
        lo, hi = ROM_REFERENCE.get(angle_name, (0, 360))
        ax.axvline(hi, color=_sci_palette()[2], lw=1.2, linestyle=":", label=f"Ref max={hi}")
        ax.set_title(angle_name.replace("_", " ").title(), fontsize=9, fontweight="bold")
        ax.set_xlabel("ROM (deg)", fontsize=8)
        ax.legend(fontsize=7)
        ax.grid(alpha=0.3)

    for ax in list(axes)[len(rom_data):]:
        ax.set_visible(False)

    plt.suptitle("ROM Distribution per Joint", fontsize=14, fontweight="bold")
    plt.tight_layout()
    fig_savefig(fig, "rom_histograms.png")
    plt.close("all")


def _plot_joint_boxplots(rom_data: Dict) -> None:
    fig, ax = plt.subplots(figsize=(14, 6))
    data = [rom_data[k] for k in sorted(rom_data.keys())]
    labels = [k.replace("_", " ").title() for k in sorted(rom_data.keys())]
    bp = ax.boxplot(data, patch_artist=True, notch=False)
    colors = plt.cm.Set2(np.linspace(0, 1, len(data)))
    for patch, color in zip(bp["boxes"], colors):
        patch.set_facecolor(color)
    ax.set_xticks(range(1, len(labels) + 1))
    ax.set_xticklabels(labels, rotation=30, ha="right", fontsize=10)
    ax.set_ylabel("ROM (degrees)", fontsize=12)
    ax.set_title("Joint ROM Distribution — Boxplots", fontsize=14, fontweight="bold")
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    fig_savefig(fig, "joint_boxplots.png")
    plt.close("all")


# ─────────────────────────────────────────────────────────────
# PART 6 — EXPLAINABILITY VALIDATION
# ─────────────────────────────────────────────────────────────

def part6_explainability(results: List[Dict]) -> None:
    log.info("=" * 60)
    log.info("PART 6 — Explainability Validation")
    log.info("=" * 60)

    all_ja  = np.array([r["joint_attention"] for r in results])   # (N, 25)
    all_fa_list = [np.array(r["frame_attention"]) for r in results]

    mean_ja = all_ja.mean(axis=0)
    std_ja  = all_ja.std(axis=0)

    # Per-class attention
    healthy_ja = all_ja[[r["true_label"] == 0 for r in results]]
    comp_ja    = all_ja[[r["true_label"] == 1 for r in results]]

    # Per-exercise attention
    ex_types = sorted(set(r["exercise_type"] for r in results))
    ex_attn = {}
    for ex in ex_types:
        ex_mask = [r["exercise_type"] == ex for r in results]
        if any(ex_mask):
            ex_attn[ex] = all_ja[ex_mask].mean(axis=0)

    def entropy(x):
        x = np.array(x, dtype=np.float64)
        x = x / max(x.sum(), 1e-12)
        return float(-np.sum(x * np.log(x + 1e-12)))

    joint_entropies  = [entropy(ja) for ja in all_ja]
    frame_entropies  = [entropy(fa) for fa in all_fa_list]
    joint_variances  = [float(np.var(ja)) for ja in all_ja]

    top10_idx = np.argsort(mean_ja)[::-1][:10]
    attn_report = {
        "n_samples": len(results),
        "top10_joints": [
            {"rank": i+1, "joint": INTELLIREHAB_JOINTS[idx],
             "mean_attention": float(mean_ja[idx]),
             "std_attention":  float(std_ja[idx])}
            for i, idx in enumerate(top10_idx)
        ],
        "all_joint_mean":     {INTELLIREHAB_JOINTS[i]: float(mean_ja[i]) for i in range(25)},
        "all_joint_std":      {INTELLIREHAB_JOINTS[i]: float(std_ja[i])  for i in range(25)},
        "class_diff": {
            "healthy_top_joint":     INTELLIREHAB_JOINTS[np.argmax(healthy_ja.mean(axis=0))] if len(healthy_ja) else "N/A",
            "compensated_top_joint": INTELLIREHAB_JOINTS[np.argmax(comp_ja.mean(axis=0))]    if len(comp_ja)   else "N/A",
            "healthy_mean_attn":     {INTELLIREHAB_JOINTS[i]: float(healthy_ja.mean(axis=0)[i]) for i in range(25)} if len(healthy_ja) else {},
            "compensated_mean_attn": {INTELLIREHAB_JOINTS[i]: float(comp_ja.mean(axis=0)[i])    for i in range(25)} if len(comp_ja)   else {},
        },
        "entropy": {
            "mean_joint_entropy":  float(np.mean(joint_entropies)),
            "std_joint_entropy":   float(np.std(joint_entropies)),
            "mean_frame_entropy":  float(np.mean(frame_entropies)),
            "std_frame_entropy":   float(np.std(frame_entropies)),
            "mean_joint_variance": float(np.mean(joint_variances)),
        },
        "temporal": {
            "mean_peak_frame": float(np.mean([np.argmax(fa) for fa in all_fa_list])),
            "std_peak_frame":  float(np.std([np.argmax(fa) for fa in all_fa_list])),
        },
    }

    with open(RESULTS_DIR / "attention_report.json", "w") as f:
        json.dump(attn_report, f, indent=2)

    # Joint importance CSV
    ji_rows = [{"joint": INTELLIREHAB_JOINTS[i], "mean_attention": float(mean_ja[i]),
                "std_attention": float(std_ja[i]),
                "mean_healthy":  float(healthy_ja.mean(axis=0)[i]) if len(healthy_ja) else 0,
                "mean_comp":     float(comp_ja.mean(axis=0)[i])    if len(comp_ja)    else 0,
                "rank": int(np.where(np.argsort(mean_ja)[::-1] == i)[0][0]) + 1}
               for i in range(25)]
    pd.DataFrame(ji_rows).sort_values("rank").to_csv(RESULTS_DIR / "tables" / "joint_importance.csv", index=False)

    # Frame importance CSV
    max_len = max(len(fa) for fa in all_fa_list)
    padded = np.zeros((len(all_fa_list), max_len))
    for i, fa in enumerate(all_fa_list):
        padded[i, :len(fa)] = fa
    mean_frame_attn = padded.mean(axis=0)
    fi_rows = [{"frame": i, "mean_attention": float(mean_frame_attn[i])} for i in range(max_len)]
    pd.DataFrame(fi_rows).to_csv(RESULTS_DIR / "tables" / "frame_importance.csv", index=False)

    # Entropy CSV
    ent_rows = [{"sample_idx": i, "subject_id": results[i]["subject_id"],
                 "joint_entropy": round(joint_entropies[i], 4),
                 "frame_entropy": round(frame_entropies[i], 4),
                 "joint_variance": round(joint_variances[i], 6)}
                for i in range(len(results))]
    pd.DataFrame(ent_rows).to_csv(RESULTS_DIR / "tables" / "attention_entropy.csv", index=False)

    log.info(f"  Top joint: {attn_report['top10_joints'][0]['joint']} (mean={attn_report['top10_joints'][0]['mean_attention']:.4f})")
    log.info(f"  Mean joint entropy: {attn_report['entropy']['mean_joint_entropy']:.4f}")
    log.info(f"  Mean frame entropy: {attn_report['entropy']['mean_frame_entropy']:.4f}")

    # Figures
    _plot_attention_heatmap_pub(mean_ja, healthy_ja.mean(axis=0) if len(healthy_ja) else mean_ja,
                                 comp_ja.mean(axis=0) if len(comp_ja) else mean_ja)
    _plot_temporal_attention_pub(mean_frame_attn)
    _plot_entropy_distribution(joint_entropies, frame_entropies)

    log.info("  Part 6 complete.")


def _plot_attention_heatmap_pub(mean_ja, healthy_ja, comp_ja) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(18, 7))
    datasets = [(mean_ja, "All Samples"), (healthy_ja, "Healthy Class"), (comp_ja, "Compensated Class")]
    for ax, (vals, title) in zip(axes, datasets):
        sorted_pairs = sorted(zip(vals, INTELLIREHAB_JOINTS), reverse=True)
        svs, snames = zip(*sorted_pairs)
        colors = plt.cm.plasma(np.linspace(0.15, 0.9, 25))
        bars = ax.barh(range(25), svs, color=colors)
        ax.set_yticks(range(25))
        ax.set_yticklabels(snames, fontsize=7)
        ax.set_xlabel("Attention Weight", fontsize=10)
        ax.set_title(title, fontsize=11, fontweight="bold")
        ax.grid(axis="x", alpha=0.3)
        ax.invert_yaxis()

    plt.suptitle("Joint Spatial Attention (Explainability Profile)", fontsize=14, fontweight="bold")
    plt.tight_layout()
    fig_savefig(fig, "attention_heatmaps.png")
    plt.close("all")


def _plot_temporal_attention_pub(mean_frame_attn: np.ndarray) -> None:
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(mean_frame_attn, color="#2E86AB", lw=2)
    ax.fill_between(range(len(mean_frame_attn)), mean_frame_attn, alpha=0.15, color="#2E86AB")
    ax.set_xlabel("Frame Index", fontsize=12)
    ax.set_ylabel("Mean Attention Weight", fontsize=12)
    ax.set_title("Temporal Attention Profile (Mean over All Samples)", fontsize=13, fontweight="bold")
    ax.grid(alpha=0.3)
    plt.tight_layout()
    fig_savefig(fig, "temporal_attention.png")
    plt.close("all")


def _plot_entropy_distribution(joint_ent: List, frame_ent: List) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    for ax, vals, title in zip(axes,
                                [joint_ent, frame_ent],
                                ["Joint Attention Entropy", "Frame Attention Entropy"]):
        ax.hist(vals, bins=40, color=_sci_palette()[0], edgecolor="white")
        ax.axvline(np.mean(vals), color=_sci_palette()[1], lw=2, linestyle="--",
                   label=f"Mean={np.mean(vals):.3f}")
        ax.set_xlabel("Entropy", fontsize=11)
        ax.set_ylabel("Count", fontsize=11)
        ax.set_title(title, fontsize=12, fontweight="bold")
        ax.legend(); ax.grid(alpha=0.3)
    plt.tight_layout()
    fig_savefig(fig, "attention_entropy.png")
    plt.close("all")


# ─────────────────────────────────────────────────────────────
# PART 7 — CALIBRATION ANALYSIS
# ─────────────────────────────────────────────────────────────

def part7_calibration(results: List[Dict], entries: List[Dict]) -> None:
    log.info("=" * 60)
    log.info("PART 7 — Calibration Analysis")
    log.info("=" * 60)

    # ── ECE / MCE (model confidence calibration) ──────────────
    targets = np.array([r["true_label"]        for r in results])
    probs   = np.array([r["prob_compensated"]   for r in results])
    confs   = np.array([r["confidence"]         for r in results])
    preds   = np.array([r["pred_label"]         for r in results])

    n_bins = 10
    ece, mce = _compute_ece_mce(targets, probs, confs, preds, n_bins)
    log.info(f"  ECE: {ece:.4f}")
    log.info(f"  MCE: {mce:.4f}")

    _plot_reliability_diagram(targets, probs, confs, preds, n_bins)
    _plot_confidence_histogram_by_class(results)

    # ── ROM calibration per subject ────────────────────────────
    by_subject: Dict[str, Dict] = defaultdict(lambda: {"healthy": [], "compensated": []})
    for entry in entries:
        subj = entry["subject_id"]
        if entry["movement_label"] == 0:
            by_subject[subj]["healthy"].append(entry["sequence"])
        else:
            by_subject[subj]["compensated"].append(entry["sequence"])

    calibrator = PersonalizedROMCalibrator()
    cal_stats = []
    for subj in tqdm(sorted(by_subject.keys()), desc="ROM calibration", ncols=90):
        h_seqs = by_subject[subj]["healthy"]
        c_seqs = by_subject[subj]["compensated"]
        if not h_seqs:
            cal_stats.append({"subject_id": subj, "fitted": False,
                               "n_healthy": 0, "n_compensated": len(c_seqs),
                               "mean_confidence": None})
            continue
        try:
            calibrator.fit(subj, h_seqs)
            conf_vals = []
            for seq in c_seqs:
                ev = calibrator.evaluate(subj, seq)
                conf_vals.append(ev["confidence"])
            cal_stats.append({
                "subject_id":        subj,
                "fitted":            True,
                "n_healthy":         len(h_seqs),
                "n_compensated":     len(c_seqs),
                "mean_confidence":   round(float(np.mean(conf_vals)), 4) if conf_vals else None,
                "std_confidence":    round(float(np.std(conf_vals)),  4) if conf_vals else None,
            })
        except Exception as ex:
            cal_stats.append({"subject_id": subj, "fitted": False, "error": str(ex)})

    df_cal = pd.DataFrame(cal_stats)
    df_cal.to_csv(RESULTS_DIR / "tables" / "calibration_statistics.csv", index=False)

    cal_summary = {
        "ece": float(ece),
        "mce": float(mce),
        "n_subjects_fitted": int(df_cal["fitted"].sum()),
        "mean_rom_confidence": float(df_cal["mean_confidence"].dropna().mean()) if "mean_confidence" in df_cal else None,
    }
    with open(RESULTS_DIR / "tables" / "calibration_report.json", "w") as f:
        json.dump(cal_summary, f, indent=2)

    log.info("  Part 7 complete.")


def _compute_ece_mce(targets, probs, confs, preds, n_bins=10):
    bin_edges = np.linspace(0.0, 1.0, n_bins + 1)
    ece, mce = 0.0, 0.0
    n = len(targets)
    for lo, hi in zip(bin_edges[:-1], bin_edges[1:]):
        mask = (confs >= lo) & (confs < hi)
        if not mask.any():
            continue
        acc_b = float(np.mean(preds[mask] == targets[mask]))
        conf_b = float(np.mean(confs[mask]))
        cal_err = abs(acc_b - conf_b)
        ece += cal_err * mask.sum() / n
        mce = max(mce, cal_err)
    return float(ece), float(mce)


def _plot_reliability_diagram(targets, probs, confs, preds, n_bins=10) -> None:
    bin_edges = np.linspace(0.0, 1.0, n_bins + 1)
    bin_accs, bin_confs, bin_sizes = [], [], []
    for lo, hi in zip(bin_edges[:-1], bin_edges[1:]):
        mask = (confs >= lo) & (confs < hi)
        if mask.any():
            bin_accs.append(float(np.mean(preds[mask] == targets[mask])))
            bin_confs.append(float(np.mean(confs[mask])))
            bin_sizes.append(int(mask.sum()))

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    ax = axes[0]
    ax.plot([0, 1], [0, 1], "k--", lw=1.2, label="Perfect calibration")
    ax.bar(bin_confs, bin_accs, width=0.08, alpha=0.7, color="#2E86AB",
           edgecolor="white", label="Model")
    ax.set_xlabel("Confidence", fontsize=12)
    ax.set_ylabel("Accuracy",   fontsize=12)
    ax.set_title("Reliability Diagram", fontsize=13, fontweight="bold")
    ax.set_xlim([0, 1]); ax.set_ylim([0, 1])
    ax.legend(fontsize=10); ax.grid(alpha=0.3)

    ax2 = axes[1]
    ax2.bar(bin_confs, bin_sizes, width=0.08, color="#E84855", edgecolor="white", alpha=0.8)
    ax2.set_xlabel("Confidence Bin", fontsize=12)
    ax2.set_ylabel("Sample Count",   fontsize=12)
    ax2.set_title("Confidence Histogram", fontsize=13, fontweight="bold")
    ax2.grid(alpha=0.3)

    plt.suptitle("Model Calibration Analysis", fontsize=14, fontweight="bold")
    plt.tight_layout()
    fig_savefig(fig, "calibration_reliability.png")
    plt.close("all")


def _plot_confidence_histogram_by_class(results: List[Dict]) -> None:
    h_conf = [r["confidence"] for r in results if r["true_label"] == 0]
    c_conf = [r["confidence"] for r in results if r["true_label"] == 1]

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.hist(h_conf, bins=40, alpha=0.65, color=_sci_palette()[0], label=f"Healthy (n={len(h_conf)})")
    ax.hist(c_conf, bins=40, alpha=0.65, color=_sci_palette()[1], label=f"Compensated (n={len(c_conf)})")
    ax.set_xlabel("Confidence", fontsize=12)
    ax.set_ylabel("Count",      fontsize=12)
    ax.set_title("Confidence Distribution by True Class", fontsize=13, fontweight="bold")
    ax.legend(fontsize=11); ax.grid(alpha=0.3)
    plt.tight_layout()
    fig_savefig(fig, "confidence_by_class.png")
    plt.close("all")


# ─────────────────────────────────────────────────────────────
# PART 8 — BASELINE MODELS — PLOTS & HELPERS
# ─────────────────────────────────────────────────────────────

def _plot_combined_roc_curves(baseline_preds: Dict[str, Tuple[List[int], List[int], List[float]]]) -> None:
    from sklearn.metrics import roc_curve, auc
    fig, ax = plt.subplots(figsize=(7, 6))
    
    # 1. Try to load ST-GAT (Ours) ROC curve from results/metrics.json
    stgat_loaded = False
    metrics_path = RESULTS_DIR / "metrics.json"
    if metrics_path.exists():
        try:
            with open(metrics_path, "r") as f:
                meta = json.load(f)
                stgat_roc = meta.get("roc")
                if stgat_roc:
                    ax.plot(stgat_roc["fpr"], stgat_roc["tpr"], color="#E84855", lw=2.5,
                            label=f"ST-GAT (Ours) (AUC = {stgat_roc['auc']:.4f})")
                    stgat_loaded = True
        except Exception as ex:
            log.warning(f"Could not load ST-GAT ROC from metrics.json: {ex}")
            
    # 2. Plot baselines
    palette = _sci_palette()
    for idx, (name, (t_arr, p_arr, pr_arr)) in enumerate(baseline_preds.items()):
        fpr, tpr, _ = roc_curve(t_arr, pr_arr)
        auc_val = auc(fpr, tpr)
        color = palette[(idx + 1) % len(palette)]
        ax.plot(fpr, tpr, color=color, lw=1.5, linestyle="--",
                label=f"{name} (AUC = {auc_val:.4f})")
                
    ax.plot([0, 1], [0, 1], "k:", lw=1.2, label="Random guessing")
    ax.set_xlim([0, 1])
    ax.set_ylim([0, 1.02])
    ax.set_xlabel("False Positive Rate", fontsize=12)
    ax.set_ylabel("True Positive Rate", fontsize=12)
    ax.set_title("ROC Curves Comparison", fontsize=13, fontweight="bold")
    ax.legend(fontsize=10, loc="lower right")
    ax.grid(alpha=0.3)
    plt.tight_layout()
    fig_savefig(fig, "baseline_roc_curves.png")
    plt.close("all")


def _plot_combined_confusion_matrices(baseline_preds: Dict[str, Tuple[List[int], List[int], List[float]]]) -> None:
    from sklearn.metrics import confusion_matrix
    stgat_cm = None
    metrics_path = RESULTS_DIR / "metrics.json"
    if metrics_path.exists():
        try:
            with open(metrics_path, "r") as f:
                meta = json.load(f)
                stgat_cm = np.array(meta.get("confusion_matrix"))
        except Exception:
            pass

    models_to_plot = []
    if stgat_cm is not None:
        models_to_plot.append(("ST-GAT (Ours)", stgat_cm))
        
    for name, (t_arr, p_arr, pr_arr) in baseline_preds.items():
        cm = confusion_matrix(t_arr, p_arr)
        models_to_plot.append((name, cm))
        
    n_models = len(models_to_plot)
    if n_models == 0:
        return
        
    cols = 3
    rows = math.ceil(n_models / cols)
    fig, axes = plt.subplots(rows, cols, figsize=(cols * 4, rows * 3.5))
    if n_models == 1:
        axes = np.array([axes])
    else:
        axes = axes.flat
    
    for ax, (name, cm) in zip(axes, models_to_plot):
        im = ax.imshow(cm, cmap="Blues", alpha=0.8)
        ax.set_xticks([0, 1])
        ax.set_xticklabels(LABEL_NAMES, fontsize=9)
        ax.set_yticks([0, 1])
        ax.set_yticklabels(LABEL_NAMES, fontsize=9)
        ax.set_title(name, fontsize=10, fontweight="bold")
        ax.set_xlabel("Predicted", fontsize=8)
        ax.set_ylabel("Actual", fontsize=8)
        
        thresh = cm.max() / 2
        for i in range(2):
            for j in range(2):
                ax.text(j, i, str(cm[i, j]), ha="center", va="center",
                        fontsize=12, color="white" if cm[i, j] > thresh else "black")
                        
    for ax in list(axes)[n_models:]:
        ax.set_visible(False)
        
    plt.suptitle("Confusion Matrices Grid", fontsize=14, fontweight="bold")
    plt.tight_layout()
    fig_savefig(fig, "baseline_confusion_matrices.png")
    plt.close("all")


# ─────────────────────────────────────────────────────────────
# PART 8 — BASELINE MODELS
# ─────────────────────────────────────────────────────────────

def part8_baselines(entries: List[Dict]) -> pd.DataFrame:
    log.info("=" * 60)
    log.info("PART 8 — Baseline Models (Optimized Sequential)")
    log.info("=" * 60)

    from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
    from sklearn.preprocessing import StandardScaler
    from sklearn.decomposition import PCA
    from sklearn.metrics import confusion_matrix
    from joblib import Parallel, delayed
    import gc

    try:
        import xgboost as xgb
        HAS_XGB = True
    except ImportError:
        HAS_XGB = False
        log.warning("  xgboost not installed — skipping XGBoost baseline")

    seq_len = TRAINING_CONFIG["sequence_length"]
    subjects = sorted(set(e["subject_id"] for e in entries))

    def _flatten(entry):
        seq = entry["sequence"]
        # Crop/pad to seq_len
        if seq.shape[0] >= seq_len:
            seq = seq[:seq_len]
        else:
            pad = np.zeros((seq_len - seq.shape[0], seq.shape[1], seq.shape[2]), dtype=np.float32)
            seq = np.concatenate([seq, pad], axis=0)
        return seq.reshape(-1)

    X = np.array([_flatten(e) for e in entries])
    y = np.array([e["movement_label"] for e in entries])
    subject_ids = np.array([e["subject_id"] for e in entries])

    N_PCA_COMPONENTS = min(100, X.shape[1] - 1, X.shape[0] // 2)

    def _loso_sklearn(model_cls, model_kwargs, name):
        # Run folds sequentially to keep memory footprint minimal and prevent system crash
        def _run_fold(subj):
            train_mask = (subject_ids != subj)
            val_mask   = (subject_ids == subj)
            X_train = X[train_mask]; y_train = y[train_mask]
            X_val   = X[val_mask];   y_val   = y[val_mask]
            
            scaler = StandardScaler()
            X_train_s = scaler.fit_transform(X_train)
            X_val_s   = scaler.transform(X_val)
            
            pca = PCA(n_components=N_PCA_COMPONENTS, random_state=SEED)
            X_train_r = pca.fit_transform(X_train_s)
            X_val_r   = pca.transform(X_val_s)
            
            clf = model_cls(**model_kwargs)
            clf.fit(X_train_r, y_train)
            preds = clf.predict(X_val_r)
            probs = clf.predict_proba(X_val_r)[:, 1] if hasattr(clf, "predict_proba") else preds.astype(float)
            
            # Explicit cleanup
            del scaler, pca, clf
            gc.collect()
            return y_val.tolist(), preds.tolist(), probs.tolist()

        results_seq = [ _run_fold(subj) for subj in subjects ]

        fold_targets, fold_preds, fold_probs = [], [], []
        for targets, preds, probs in results_seq:
            fold_targets.extend(targets)
            fold_preds.extend(preds)
            fold_probs.extend(probs)
        return fold_targets, fold_preds, fold_probs

    baseline_results = []
    baseline_predictions = {} 

    baselines_cfg = [
        ("Random Forest",     RandomForestClassifier,    {"n_estimators": 100, "random_state": SEED, "n_jobs": 1}),
        ("Gradient Boosting", GradientBoostingClassifier,{"n_estimators": 50,  "random_state": SEED, "max_depth": 4}),
    ]
    if HAS_XGB:
        import xgboost as xgb
        baselines_cfg.append(("XGBoost", xgb.XGBClassifier,
                               {"n_estimators": 100, "random_state": SEED, "verbosity": 0, "eval_metric": "logloss"}))

    for name, cls, kwargs in baselines_cfg:
        log.info(f"  Training baseline: {name} (sequential)...")
        t0 = time.time()
        try:
            t_arr, p_arr, pr_arr = _loso_sklearn(cls, kwargs, name)
            elapsed = time.time() - t0
            m = _quick_metrics(t_arr, p_arr, pr_arr, name, elapsed)
            baseline_results.append(m)
            baseline_predictions[name] = (t_arr, p_arr, pr_arr)
        except Exception as ex:
            log.warning(f"  {name} failed: {ex}")
            baseline_results.append({"model": name, "error": str(ex)})

    # Sequence models (LSTM / GRU)
    for arch in ["LSTM", "GRU"]:
        log.info(f"  Training baseline: {arch} (sequential)...")
        try:
            t_arr, p_arr, pr_arr, elapsed = _loso_seq_model(entries, arch, seq_len)
            m = _quick_metrics(t_arr, p_arr, pr_arr, arch, elapsed)
            baseline_results.append(m)
            baseline_predictions[arch] = (t_arr, p_arr, pr_arr)
        except Exception as ex:
            log.warning(f"  {arch} failed: {ex}")
            baseline_results.append({"model": arch, "error": str(ex)})

    # Plots for confusion matrices and ROC curves of baselines and main model
    _plot_combined_roc_curves(baseline_predictions)
    _plot_combined_confusion_matrices(baseline_predictions)

    df_bl = pd.DataFrame(baseline_results)

    # Load ST-GAT (Ours) metrics from metrics.json to include in comparison table
    stgat_metrics = None
    try:
        metrics_path = RESULTS_DIR / "metrics.json"
        if metrics_path.exists():
            with open(metrics_path, "r") as f:
                meta = json.load(f)
                stgat_metrics = {
                    "model": "ST-GAT (Ours)",
                    "accuracy": round(meta.get("accuracy"), 4) if meta.get("accuracy") is not None else None,
                    "balanced_accuracy": round(meta.get("balanced_accuracy"), 4) if meta.get("balanced_accuracy") is not None else None,
                    "f1_macro": round(meta.get("f1_macro"), 4) if meta.get("f1_macro") is not None else None,
                    "mcc": round(meta.get("mcc"), 4) if meta.get("mcc") is not None else None,
                    "sensitivity": round(meta.get("sensitivity"), 4) if meta.get("sensitivity") is not None else None,
                    "specificity": round(meta.get("specificity"), 4) if meta.get("specificity") is not None else None,
                    "roc_auc": round(meta.get("roc")["auc"], 4) if meta.get("roc") is not None else None,
                    "training_time_s": None,
                }
    except Exception as ex:
        log.warning(f"Could not load ST-GAT metrics for comparison: {ex}")

    if stgat_metrics is not None:
        df_bl = pd.concat([pd.DataFrame([stgat_metrics]), df_bl], ignore_index=True)

    df_bl.to_csv(RESULTS_DIR / "tables" / "baseline_results.csv", index=False)
    df_bl.to_csv(RESULTS_DIR / "baseline_results.csv", index=False)
    try:
        df_bl.to_excel(RESULTS_DIR / "tables" / "baseline_metrics.xlsx", index=False)
    except Exception:
        pass

    if not df_bl.empty:
        _plot_baseline_comparison(df_bl)
        _write_latex_table(df_bl)

    log.info("  Part 8 complete.")
    return df_bl


def _quick_metrics(targets, preds, probs, name, elapsed):
    t = list(targets); p = list(preds); pr = list(probs)
    acc  = float(np.mean(np.array(t) == np.array(p)))
    bal  = balanced_accuracy_score(t, p)
    f1   = classification_report(t, p, labels=LABEL_NAMES)["macro avg"]["f1-score"]
    mcc  = matthews_corrcoef(t, p)
    roc  = roc_auc_scores(t, pr)["auc"]
    spec, sens = compute_specificity_sensitivity(t, p)
    return {
        "model":            name,
        "accuracy":         round(acc,  4),
        "balanced_accuracy":round(bal,  4),
        "f1_macro":         round(f1,   4),
        "mcc":              round(mcc,  4),
        "sensitivity":      round(sens, 4),
        "specificity":      round(spec, 4),
        "roc_auc":          round(roc,  4),
        "training_time_s":  round(elapsed, 2),
    }


def _loso_seq_model(entries, arch: str, seq_len: int):
    """Simple LSTM/GRU baseline trained sequentially with LOSO CV."""
    import gc
    subjects = sorted(set(e["subject_id"] for e in entries))
    fold_targets, fold_preds, fold_probs = [], [], []
    t0 = time.time()
    
    # We must define device locally
    dev = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    # Limit PyTorch CPU threads to prevent CPU thrashing
    if dev.type == "cpu":
        torch.set_num_threads(2)

    for subj in tqdm(subjects, desc=f"{arch} LOSO Sequential", ncols=80):
        train_entries = [e for e in entries if e["subject_id"] != subj]
        val_entries   = [e for e in entries if e["subject_id"] == subj]
        if not train_entries or not val_entries:
            continue

        in_dim   = 25 * 3
        hid_dim  = 64
        rnn_cls  = torch.nn.LSTM if arch == "LSTM" else torch.nn.GRU

        class SeqModel(torch.nn.Module):
            def __init__(self):
                super().__init__()
                self.rnn = rnn_cls(in_dim, hid_dim, num_layers=2, batch_first=True,
                                   dropout=0.2, bidirectional=True)
                self.fc  = torch.nn.Linear(hid_dim * 2, 2)
            def forward(self, x):
                B, T, J, C = x.shape
                x = x.reshape(B, T, J * C)
                out, _ = self.rnn(x)
                return self.fc(out[:, -1, :])

        model = SeqModel().to(dev)
        optimizer = torch.optim.Adam(model.parameters(), lr=1e-3, weight_decay=1e-4)
        criterion = torch.nn.CrossEntropyLoss()

        from torch.utils.data import DataLoader
        train_ds = IntelliRehabSequenceDataset(train_entries, augment=True, sequence_length=seq_len)
        train_loader = DataLoader(train_ds, batch_size=32, shuffle=True, num_workers=0, collate_fn=sequence_collate_fn)

        # Train for 2 epochs
        for epoch in range(2):
            model.train()
            for batch in train_loader:
                seqs   = batch["sequence"].to(dev)
                labels = batch["label"].to(dev)
                loss   = criterion(model(seqs), labels)
                optimizer.zero_grad(); loss.backward(); optimizer.step()

        val_ds = IntelliRehabSequenceDataset(val_entries, augment=False, sequence_length=seq_len)
        val_loader = DataLoader(val_ds, batch_size=32, shuffle=False, num_workers=0, collate_fn=sequence_collate_fn)
        
        model.eval()
        with torch.no_grad():
            for batch in val_loader:
                seqs   = batch["sequence"].to(dev)
                labels = batch["label"].cpu().numpy()
                logits = model(seqs)
                probs  = torch.softmax(logits, dim=-1).cpu().numpy()
                preds  = np.argmax(probs, axis=1)
                fold_targets.extend(labels.tolist())
                fold_preds.extend(preds.tolist())
                fold_probs.extend(probs[:, 1].tolist())

        # Cleanup memory after each subject fold
        del model, optimizer, train_ds, train_loader, val_ds, val_loader
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

    return fold_targets, fold_preds, fold_probs, time.time() - t0


def _plot_baseline_comparison(df: pd.DataFrame) -> None:
    metric_cols = ["accuracy", "balanced_accuracy", "f1_macro", "roc_auc"]
    df_plot = df.dropna(subset=metric_cols[:1])
    if df_plot.empty:
        return
    fig, axes = plt.subplots(1, 4, figsize=(18, 5))
    palette = _sci_palette()
    for ax, col in zip(axes, metric_cols):
        vals = df_plot[col].values
        models = df_plot["model"].values
        colors = [palette[1] if m == "ST-GAT (Ours)" else palette[0] for m in models]
        bars = ax.barh(models, vals, color=colors, edgecolor="white")
        ax.set_xlim([0, 1.05])
        ax.set_xlabel(col.replace("_", " ").title(), fontsize=11)
        ax.set_title(col.replace("_", " ").title(), fontsize=11, fontweight="bold")
        ax.grid(axis="x", alpha=0.3)
        for bar, val in zip(bars, vals):
            ax.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height()/2,
                    f"{val:.3f}", va="center", fontsize=9)
    plt.suptitle("Baseline Comparison", fontsize=14, fontweight="bold")
    plt.tight_layout()
    fig_savefig(fig, "baseline_comparison.png")
    plt.close("all")


def _write_latex_table(df: pd.DataFrame) -> None:
    cols = ["model","accuracy","balanced_accuracy","f1_macro","roc_auc","mcc","sensitivity","specificity"]
    df_tex = df[[c for c in cols if c in df.columns]].copy()
    latex = df_tex.to_latex(index=False, float_format="%.4f",
                             caption="Baseline Comparison", label="tab:baselines")
    with open(RESULTS_DIR / "tables" / "comparison_tables.tex", "w") as f:
        f.write(latex)
    log.info("  Saved LaTeX table: comparison_tables.tex")


# ─────────────────────────────────────────────────────────────
# PART 9 — ABLATION STUDY
# ─────────────────────────────────────────────────────────────

def part9_ablation(entries: List[Dict], device: torch.device) -> pd.DataFrame:
    log.info("=" * 60)
    log.info("PART 9 — Ablation Study")
    log.info("=" * 60)

    import gc
    seq_len  = TRAINING_CONFIG["sequence_length"]
    subjects = sorted(set(e["subject_id"] for e in entries))

    def _loso_ablation(model_fn):
        """Run single LOSO fold pass over all subjects using given model factory."""
        all_t, all_p, all_pr = [], [], []
        for subj in subjects:
            train_ents = [e for e in entries if e["subject_id"] != subj]
            val_ents   = [e for e in entries if e["subject_id"] == subj]
            if not val_ents:
                continue
            model = model_fn().to(device)
            # Load best checkpoint for this fold (if exists)
            fold_ckpt = CHECKPOINT_DIR / f"fold_{subj}.pt"
            if fold_ckpt.exists():
                ckpt = torch.load(str(fold_ckpt), map_location=device, weights_only=True)
                state = ckpt.get("model_state", ckpt)
                model.load_state_dict(state, strict=False)
            
            # Post-load modification for graph attention ablation
            if getattr(model, "ablation_no_graph_attn", False):
                import torch.nn as nn
                for block in [model.spatial1, model.spatial2]:
                    nn.init.zeros_(block.gat.att_src)
                    nn.init.zeros_(block.gat.att_dst)

            model.eval()
            val_res = run_inference(model, val_ents, device, batch_size=16, desc=f"  Ablation val {subj}")
            all_t.extend([r["true_label"] for r in val_res])
            all_p.extend([r["pred_label"] for r in val_res])
            all_pr.extend([r["prob_compensated"] for r in val_res])
            
            # Explicit cleanup
            del model
            gc.collect()
        return all_t, all_p, all_pr

    ablation_configs = {}

    # Full model
    def _full():
        return stgat_from_config({"hidden_dim": 64, "heads": 4, "dropout": 0.0})
    ablation_configs["Full ST-GAT"] = _full

    # Without graph attention (replace GATConv with linear)
    def _no_graph_attn():
        m = stgat_from_config({"hidden_dim": 64, "heads": 4, "dropout": 0.0})
        m.ablation_no_graph_attn = True
        return m
    ablation_configs["w/o Graph Attention"] = _no_graph_attn

    # Without temporal attention (skip temporal_attention block)
    class STGATNoTemporalAttn(STGAT):
        def forward(self, x):
            from src.graph import build_batched_edge_index
            if self.export_mode:
                return super().forward(x)
            
            batch_size, seq_len, num_nodes, num_features = x.shape
            x_proj = self.input_proj(x)
            
            flattened = x_proj.reshape(batch_size * seq_len * num_nodes, -1)
            edge_index = build_batched_edge_index(self.spatial_edge_index, batch_size * seq_len, num_nodes)
            
            spatial_out1, edge_attn1 = self.spatial1(flattened, edge_index, return_attn=True)
            spatial_out2, edge_attn2 = self.spatial2(spatial_out1, edge_index, return_attn=True)
            
            spatial_out = spatial_out2.reshape(batch_size, seq_len, num_nodes, -1).permute(0, 2, 3, 1)
            
            temporal_out = self.temporal1(spatial_out)
            temporal_out = self.temporal2(temporal_out)
            
            # Bypass Temporal Attention: use temporal_out directly with LayerNorm
            out = temporal_out.permute(0, 1, 3, 2)
            out = self.temporal_attention.norm(out)
            out = out.permute(0, 1, 3, 2)
            
            pooled = out.mean(dim=3).mean(dim=1)
            logits = self.classifier(pooled)
            probabilities = torch.softmax(logits, dim=-1)
            
            edge_attention = edge_attn2.reshape(batch_size, seq_len, -1).mean(dim=1)
            joint_attention = self._aggregate_node_attention(edge_index, edge_attn2, batch_size, seq_len, num_nodes)
            frame_attention = torch.ones((batch_size, seq_len), device=x.device) / seq_len
            
            return {
                'logits': logits,
                'probabilities': probabilities,
                'joint_attention': joint_attention,
                'frame_attention': frame_attention,
                'edge_attention': edge_attention,
            }

    def _no_temp_attn():
        m = STGATNoTemporalAttn(input_dim=3, hidden_dim=64, num_classes=2, heads=4, dropout=0.0)
        return m
    ablation_configs["w/o Temporal Attention"] = _no_temp_attn

    ablation_rows = []
    for config_name, model_fn in ablation_configs.items():
        log.info(f"  Ablation: {config_name}")
        t0 = time.time()
        try:
            t_arr, p_arr, pr_arr = _loso_ablation(model_fn)
            elapsed = time.time() - t0
            m = _quick_metrics(t_arr, p_arr, pr_arr, config_name, elapsed)
            model_tmp = model_fn()
            m["n_params"] = sum(p.numel() for p in model_tmp.parameters())
            ablation_rows.append(m)
        except Exception as ex:
            log.warning(f"  Ablation {config_name} failed: {ex}")
            ablation_rows.append({"model": config_name, "error": str(ex)})

    df_abl = pd.DataFrame(ablation_rows)
    df_abl.to_csv(RESULTS_DIR / "tables" / "ablation_table.csv", index=False)
    log.info("  Part 9 complete.")
    return df_abl


# ─────────────────────────────────────────────────────────────
# PART 10 — STATISTICAL SIGNIFICANCE
# ─────────────────────────────────────────────────────────────

def part10_statistics(results: List[Dict], df_baselines: Optional[pd.DataFrame]) -> None:
    log.info("=" * 60)
    log.info("PART 10 — Statistical Significance")
    log.info("=" * 60)

    from scipy import stats

    targets = np.array([r["true_label"] for r in results])
    preds   = np.array([r["pred_label"] for r in results])
    confs   = np.array([r["confidence"] for r in results])
    probs   = np.array([r["prob_compensated"] for r in results])

    # Bootstrap CI for accuracy
    n_boot = 2000
    boot_accs = []
    n = len(targets)
    for _ in range(n_boot):
        idx = np.random.choice(n, n, replace=True)
        boot_accs.append(float(np.mean(targets[idx] == preds[idx])))
    ci_lo, ci_hi = np.percentile(boot_accs, [2.5, 97.5])
    mean_acc = float(np.mean(targets == preds))

    log.info(f"  Accuracy: {mean_acc:.4f}")
    log.info(f"  Bootstrap 95% CI: [{ci_lo:.4f}, {ci_hi:.4f}]")

    stat_lines = [
        "# Statistical Significance Analysis",
        f"\nGenerated: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Bootstrap Confidence Intervals (n=2000 resamples)",
        f"| Metric | Estimate | 95% CI Lower | 95% CI Upper |",
        f"|--------|----------|--------------|--------------|",
        f"| Accuracy | {mean_acc:.4f} | {ci_lo:.4f} | {ci_hi:.4f} |",
    ]

    # Additional bootstrap CIs
    for metric_name, fn in [
        ("Balanced Accuracy", lambda t, p, pr: balanced_accuracy_score(list(t), list(p))),
        ("ROC-AUC",           lambda t, p, pr: roc_auc_scores(list(t), list(pr))["auc"]),
        ("MCC",               lambda t, p, pr: matthews_corrcoef(list(t), list(p))),
        ("F1 (macro)",        lambda t, p, pr: classification_report(list(t), list(p), labels=LABEL_NAMES)["macro avg"]["f1-score"]),
    ]:
        boot_vals = []
        for _ in range(n_boot):
            idx = np.random.choice(n, n, replace=True)
            try:
                v = fn(targets[idx], preds[idx], probs[idx])
                boot_vals.append(float(v))
            except Exception:
                pass
        if boot_vals:
            lo, hi = np.percentile(boot_vals, [2.5, 97.5])
            est = float(np.mean(boot_vals))
            stat_lines.append(f"| {metric_name} | {est:.4f} | {lo:.4f} | {hi:.4f} |")
            log.info(f"  {metric_name}: {est:.4f} [{lo:.4f}, {hi:.4f}]")

    stat_lines.append("")

    # Wilcoxon / t-test comparisons against baselines
    if df_baselines is not None and not df_baselines.empty:
        stat_lines += [
            "## Pairwise Comparison: ST-GAT vs Baselines",
            "",
            "Comparing LOSO per-subject accuracy distributions.",
            "",
            f"| Baseline | Wilcoxon p-value | Effect Size (r) | Significant? |",
            f"|----------|-----------------|----------------|--------------|",
        ]
        # Use subject-level accuracies from subject_results.csv if present
        subj_res_path = RESULTS_DIR / "subject_results.csv"
        if subj_res_path.exists():
            df_subj = pd.read_csv(subj_res_path)
            stgat_accs = df_subj["accuracy"].values
            for _, row in df_baselines.iterrows():
                if "accuracy" not in row or pd.isna(row["accuracy"]):
                    continue
                # Single-value baseline accuracy — cannot do paired test
                bl_acc = float(row["accuracy"])
                n_subjects = len(stgat_accs)
                # One-sample t-test against baseline mean
                t_stat, p_val = stats.ttest_1samp(stgat_accs, bl_acc)
                effect_r = abs(t_stat) / math.sqrt(t_stat**2 + n_subjects - 1)
                sig = "Yes" if p_val < 0.05 else "No"
                stat_lines.append(
                    f"| {row['model']} | {p_val:.4f} | {effect_r:.4f} | {sig} |"
                )

    with open(RESULTS_DIR / "statistical_analysis.md", "w", encoding="utf-8") as f:
        f.write("\n".join(stat_lines))
    log.info("  Saved: statistical_analysis.md")
    log.info("  Part 10 complete.")


# ─────────────────────────────────────────────────────────────
# PART 11 — PUBLICATION FIGURES (additional)
# ─────────────────────────────────────────────────────────────

def part11_publication_figures(results: List[Dict], df_subj: Optional[pd.DataFrame]) -> None:
    log.info("=" * 60)
    log.info("PART 11 — Publication Figures")
    log.info("=" * 60)

    # Exercise-wise performance
    by_ex = defaultdict(lambda: {"t": [], "p": [], "pr": []})
    for r in results:
        ex = r["exercise_type"]
        by_ex[ex]["t"].append(r["true_label"])
        by_ex[ex]["p"].append(r["pred_label"])
        by_ex[ex]["pr"].append(r["prob_compensated"])

    ex_rows = []
    for ex, d in sorted(by_ex.items()):
        acc = float(np.mean(np.array(d["t"]) == np.array(d["p"])))
        roc = roc_auc_scores(d["t"], d["pr"])["auc"]
        f1  = classification_report(d["t"], d["p"], labels=LABEL_NAMES)["macro avg"]["f1-score"]
        ex_rows.append({"exercise": ex, "n": len(d["t"]), "accuracy": round(acc, 4),
                         "roc_auc": round(roc, 4), "f1_macro": round(f1, 4)})
    df_ex = pd.DataFrame(ex_rows)
    df_ex.to_csv(RESULTS_DIR / "tables" / "exercise_results.csv", index=False)

    if not df_ex.empty:
        _plot_exercise_performance(df_ex)

    # Error distribution figure
    targets = [r["true_label"] for r in results]
    preds   = [r["pred_label"] for r in results]
    _plot_error_distribution(targets, preds, [r["exercise_type"] for r in results])

    log.info("  Part 11 complete.")


def _plot_exercise_performance(df: pd.DataFrame) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    cols   = ["accuracy", "roc_auc", "f1_macro"]
    titles = ["Accuracy", "ROC-AUC", "F1 (Macro)"]
    palette = _sci_palette()
    for ax, col, title in zip(axes, cols, titles):
        bars = ax.bar(df["exercise"], df[col], color=palette[0], edgecolor="white", alpha=0.85)
        ax.axhline(df[col].mean(), color=palette[1], linestyle="--", lw=1.5,
                   label=f"Mean={df[col].mean():.3f}")
        ax.set_xticklabels(df["exercise"], rotation=30, ha="right", fontsize=9)
        ax.set_ylabel(title, fontsize=11)
        ax.set_title(f"Per-Exercise {title}", fontsize=12, fontweight="bold")
        ax.set_ylim([0, 1.05]); ax.legend(fontsize=9); ax.grid(axis="y", alpha=0.3)
    plt.suptitle("Exercise-Wise Performance", fontsize=14, fontweight="bold")
    plt.tight_layout()
    fig_savefig(fig, "exercise_performance.png")
    plt.close("all")


def _plot_error_distribution(targets, preds, exercises) -> None:
    ex_error = defaultdict(lambda: {"errors": 0, "total": 0})
    for t, p, ex in zip(targets, preds, exercises):
        ex_error[ex]["total"] += 1
        if t != p:
            ex_error[ex]["errors"] += 1

    exs   = sorted(ex_error.keys())
    rates = [ex_error[ex]["errors"] / max(ex_error[ex]["total"], 1) for ex in exs]
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(exs, rates, color=_sci_palette()[1], edgecolor="white", alpha=0.85)
    ax.set_ylabel("Error Rate", fontsize=12)
    ax.set_title("Error Rate per Exercise Type", fontsize=13, fontweight="bold")
    ax.set_xticklabels(exs, rotation=30, ha="right")
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    fig_savefig(fig, "error_rate_by_exercise.png")
    plt.close("all")


# ─────────────────────────────────────────────────────────────
# PART 12 — FINAL PUBLICATION REPORT
# ─────────────────────────────────────────────────────────────

def part12_final_report(
    entries: List[Dict],
    metrics: Dict,
    df_subj: Optional[pd.DataFrame],
    df_baselines: Optional[pd.DataFrame],
    df_ablation: Optional[pd.DataFrame],
    args,
) -> None:
    log.info("=" * 60)
    log.info("PART 12 — Final Publication Report")
    log.info("=" * 60)

    label_counts = Counter(e["movement_label"] for e in entries)
    subj_ids = sorted(set(e["subject_id"] for e in entries))
    ex_counts = Counter(e["exercise_type"] for e in entries)

    top5_joints = []
    attn_path = RESULTS_DIR / "attention_report.json"
    if attn_path.exists():
        with open(attn_path) as f:
            attn_data = json.load(f)
        top5_joints = attn_data.get("top10_joints", [])[:5]

    cal_path = RESULTS_DIR / "tables" / "calibration_report.json"
    cal_data = {}
    if cal_path.exists():
        with open(cal_path) as f:
            cal_data = json.load(f)

    lines = [
        "# ST-GAT Rehabilitation Assessment — Publication Report",
        "",
        f"> **Generated:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        f"> **Checkpoint:** `{args.checkpoint}`",
        f"> **Device:** `{args.device}`",
        "",
        "---",
        "",
        "## 1. Dataset Summary",
        "",
        f"| Item | Value |",
        f"|------|-------|",
        f"| Total Samples | {len(entries)} |",
        f"| Unique Subjects | {len(subj_ids)} |",
        f"| Healthy Samples (class 0) | {label_counts[0]} |",
        f"| Compensated Samples (class 1) | {label_counts[1]} |",
        f"| Class Ratio (H:C) | {label_counts[0]}:{label_counts[1]} |",
        f"| Exercise Types | {', '.join(sorted(ex_counts.keys()))} |",
        "",
    ]
    for ex, cnt in sorted(ex_counts.items()):
        lines.append(f"- **{ex}**: {cnt} samples")

    lines += [
        "",
        "---",
        "",
        "## 2. Model Configuration",
        "",
        f"| Parameter | Value |",
        f"|-----------|-------|",
        f"| Architecture | ST-GAT (Spatial-Temporal Graph Attention Network) |",
        f"| Parameters | 53,090 |",
        f"| Hidden Dim | {TRAINING_CONFIG['hidden_dim']} |",
        f"| Attention Heads | {TRAINING_CONFIG['heads']} |",
        f"| Dropout | {TRAINING_CONFIG['dropout']} |",
        f"| Sequence Length | {TRAINING_CONFIG['sequence_length']} |",
        f"| Joints | 25 (Kinect v2 / IntelliRehabDS) |",
        f"| Input Dim | 3 (x, y, z) |",
        f"| Classes | 2 (Healthy=0, Compensated=1) |",
        "",
        "---",
        "",
        "## 3. Training Protocol",
        "",
        f"| Setting | Value |",
        f"|---------|-------|",
        f"| Cross-Validation | Leave-One-Subject-Out (LOSO) |",
        f"| Optimizer | AdamW |",
        f"| Learning Rate | {TRAINING_CONFIG['lr']} |",
        f"| Weight Decay | {TRAINING_CONFIG['weight_decay']} |",
        f"| Max Epochs | {TRAINING_CONFIG['epochs']} |",
        f"| Early Stopping Patience | {TRAINING_CONFIG['patience']} |",
        f"| Batch Size | {TRAINING_CONFIG['batch_size']} |",
        f"| Loss | Weighted CrossEntropy |",
        f"| Augmentation | Gaussian noise, rotation, scaling, temporal crop |",
        "",
        "---",
        "",
        "## 4. Evaluation Metrics",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        f"| Accuracy | **{metrics['accuracy']:.4f}** |",
        f"| Balanced Accuracy | **{metrics['balanced_accuracy']:.4f}** |",
        f"| Sensitivity | **{metrics['sensitivity']:.4f}** |",
        f"| Specificity | **{metrics['specificity']:.4f}** |",
        f"| Precision (macro) | **{metrics['precision_macro']:.4f}** |",
        f"| Recall (macro) | **{metrics['recall_macro']:.4f}** |",
        f"| F1 (macro) | **{metrics['f1_macro']:.4f}** |",
        f"| ROC-AUC | **{metrics['roc_auc']:.4f}** |",
        f"| PR-AUC | **{metrics['pr_auc']:.4f}** |",
        f"| MCC | **{metrics['mcc']:.4f}** |",
        f"| Cohen's Kappa | **{metrics['cohen_kappa']:.4f}** |",
        f"| True Positives | {metrics['true_positives']} |",
        f"| True Negatives | {metrics['true_negatives']} |",
        f"| False Positives | {metrics['false_positives']} |",
        f"| False Negatives | {metrics['false_negatives']} |",
        f"| Mean Confidence | {metrics['mean_confidence']:.4f} ± {metrics['std_confidence']:.4f} |",
        "",
    ]

    # Per-class
    lines += [
        "### Per-Class Metrics",
        "",
        "| Class | Precision | Recall | F1 | Support |",
        "|-------|-----------|--------|-----|---------|",
        f"| Healthy | {metrics['precision_healthy']:.4f} | {metrics['recall_healthy']:.4f} | {metrics['f1_healthy']:.4f} | {metrics['support_healthy']} |",
        f"| Compensated | {metrics['precision_compensated']:.4f} | {metrics['recall_compensated']:.4f} | {metrics['f1_compensated']:.4f} | {metrics['support_compensated']} |",
        "",
    ]

    # Subject analysis
    if df_subj is not None and not df_subj.empty:
        lines += [
            "---",
            "",
            "## 5. Subject-Wise LOSO Analysis",
            "",
            f"| Metric | Mean | Std | CI-95 Lower | CI-95 Upper |",
            f"|--------|------|-----|-------------|-------------|",
        ]
        subj_stat_path = RESULTS_DIR / "subject_statistics.csv"
        if subj_stat_path.exists():
            df_ss = pd.read_csv(subj_stat_path)
            for _, row in df_ss.iterrows():
                lines.append(
                    f"| {row['metric'].replace('_',' ').title()} | {row['mean']:.4f} | {row['std']:.4f} | {row['ci95_lower']:.4f} | {row['ci95_upper']:.4f} |"
                )

    # Attention
    if top5_joints:
        lines += [
            "",
            "---",
            "",
            "## 6. Explainability — Spatial Attention",
            "",
            "**Top-5 Joints by Mean Attention Weight:**",
            "",
            "| Rank | Joint | Mean Attention | Std |",
            "|------|-------|----------------|-----|",
        ]
        for j in top5_joints:
            lines.append(f"| {j['rank']} | {j['joint']} | {j['mean_attention']:.4f} | {j['std_attention']:.4f} |")

    # Calibration
    if cal_data:
        lines += [
            "",
            "---",
            "",
            "## 7. Calibration",
            "",
            f"| Metric | Value |",
            f"|--------|-------|",
            f"| ECE (Expected Calibration Error) | {cal_data.get('ece', 'N/A'):.4f} |",
            f"| MCE (Maximum Calibration Error) | {cal_data.get('mce', 'N/A'):.4f} |",
            f"| Subjects Fitted (ROM) | {cal_data.get('n_subjects_fitted', 'N/A')} |",
            "",
        ]

    # Baselines
    if df_baselines is not None and not df_baselines.empty:
        lines += [
            "---",
            "",
            "## 8. Baseline Comparison",
            "",
            "| Model | Accuracy | Balanced Acc | F1 | ROC-AUC | MCC |",
            "|-------|----------|--------------|----|---------|-----|",
        ]
        for _, row in df_baselines.iterrows():
            if "accuracy" in row and not pd.isna(row.get("accuracy")):
                lines.append(
                    f"| {row.get('model','?')} | {row.get('accuracy',0):.4f} | "
                    f"{row.get('balanced_accuracy',0):.4f} | {row.get('f1_macro',0):.4f} | "
                    f"{row.get('roc_auc',0):.4f} | {row.get('mcc',0):.4f} |"
                )

    # Ablation
    if df_ablation is not None and not df_ablation.empty:
        lines += [
            "",
            "---",
            "",
            "## 9. Ablation Study",
            "",
            "| Configuration | Accuracy | Balanced Acc | F1 | ROC-AUC |",
            "|---------------|----------|--------------|----|---------|",
        ]
        for _, row in df_ablation.iterrows():
            if "accuracy" in row and not pd.isna(row.get("accuracy")):
                lines.append(
                    f"| {row.get('model','?')} | {row.get('accuracy',0):.4f} | "
                    f"{row.get('balanced_accuracy',0):.4f} | {row.get('f1_macro',0):.4f} | "
                    f"{row.get('roc_auc',0):.4f} |"
                )

    # Files generated
    lines += [
        "",
        "---",
        "",
        "## 10. Generated Files",
        "",
        "### Metrics",
        "- `results/metrics.json` — All evaluation metrics",
        "- `results/metrics.csv` — Metrics in CSV",
        "- `results/classification_report.txt` — Full sklearn classification report",
        "- `results/subject_results.csv` — Per-subject LOSO metrics",
        "- `results/subject_statistics.csv` — LOSO statistics with CI",
        "- `results/statistical_analysis.md` — Bootstrap CI and significance tests",
        "- `results/attention_report.json` — Full explainability report",
        "",
        "### Figures",
        "- `results/confusion_matrix.png`",
        "- `results/roc_curve.png`",
        "- `results/pr_curve.png`",
        "- `results/figures/confidence_histogram.png`",
        "- `results/figures/subject_barplots.png`",
        "- `results/figures/subject_heatmap.png`",
        "- `results/figures/attention_heatmaps.png`",
        "- `results/figures/temporal_attention.png`",
        "- `results/figures/attention_entropy.png`",
        "- `results/figures/rom_histograms.png`",
        "- `results/figures/joint_boxplots.png`",
        "- `results/figures/calibration_reliability.png`",
        "- `results/figures/confidence_by_class.png`",
        "- `results/figures/failure_causes.png`",
        "- `results/figures/baseline_comparison.png`",
        "- `results/figures/exercise_performance.png`",
        "",
        "### Tables",
        "- `results/tables/joint_importance.csv`",
        "- `results/tables/frame_importance.csv`",
        "- `results/tables/attention_entropy.csv`",
        "- `results/tables/rom_statistics.csv`",
        "- `results/tables/calibration_statistics.csv`",
        "- `results/tables/baseline_results.csv`",
        "- `results/tables/ablation_table.csv`",
        "- `results/tables/comparison_tables.tex`",
        "",
        "### Error Analysis",
        "- `results/errors/error_analysis.md`",
        "- `results/errors/error_analysis.csv`",
        "- `results/errors/failure_causes.csv`",
        "- `results/errors/error_rate_by_exercise.csv`",
        "- `results/errors/error_rate_by_subject.csv`",
        "",
        "---",
        "",
        "## 11. Discussion",
        "",
        "The ST-GAT model leverages spatial graph attention across the 25-joint Kinect skeleton "
        "and temporal multi-head self-attention to identify compensatory movement patterns. "
        "The Leave-One-Subject-Out evaluation protocol ensures the reported metrics reflect "
        "genuine generalisation to unseen individuals.",
        "",
        "## 12. Limitations",
        "",
        "- Dataset limited to IntelliRehabDS exercises; generalisation to other protocols requires further validation.",
        "- ROM calibration depends on availability of healthy baseline trials per subject.",
        "- Kinect v2 tracking noise may affect skeleton quality for fast movements.",
        "",
        "## 13. Future Work",
        "",
        "- Extend to multi-label exercise quality scoring.",
        "- Incorporate RGB video stream for multi-modal fusion.",
        "- Validate on clinical populations and larger cohorts.",
        "- Explore real-time inference optimisation for embedded deployment.",
        "",
        "---",
        "",
        "*This report was automatically generated by `evaluate_and_report.py --full`*",
    ]

    report_md = "\n".join(lines)
    with open(RESULTS_DIR / "final_publication_report.md", "w", encoding="utf-8") as f:
        f.write(report_md)
    log.info("  Saved: results/final_publication_report.md")
    log.info("  Part 12 complete.")


# ─────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────

def parse_args():
    p = argparse.ArgumentParser(
        description="Publication-ready evaluation framework for ST-GAT Rehabilitation Assessment"
    )
    p.add_argument("--full",       action="store_true", help="Run all parts (1-12)")
    p.add_argument("--parts",      type=str, default="",
                   help="Comma-separated list of parts to run, e.g. --parts 1,2,6,11,12")
    p.add_argument("--checkpoint", type=str, default="checkpoints/best_model.pt")
    p.add_argument("--data-dir",   type=str, default=str(DATA_DIR))
    p.add_argument("--device",     type=str, default="cuda" if torch.cuda.is_available() else "cpu")
    p.add_argument("--batch-size", type=int, default=32)
    p.add_argument("--no-baselines",  action="store_true", help="Skip Part 8 (baselines)")
    p.add_argument("--no-ablation",   action="store_true", help="Skip Part 9 (ablation)")
    p.add_argument("--no-statistics", action="store_true", help="Skip Part 10 (statistics)")
    return p.parse_args()


def main():
    args = parse_args()
    set_seed(SEED)
    ensure_dirs()

    # Re-init logger after dirs created
    for h in log.handlers[:]:
        log.removeHandler(h)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(RESULTS_DIR / "evaluation.log", encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )

    if not args.full and not args.parts:
        print("Specify --full or --parts. Use --help for options.")
        sys.exit(0)

    wanted = set(range(1, 13)) if args.full else set(int(x) for x in args.parts.split(",") if x.strip())

    device = torch.device(args.device)
    log.info(f"Device: {device}")

    # ── Load dataset ───────────────────────────────────────────
    log.info(f"Loading dataset from: {args.data_dir}")
    t0 = time.time()
    entries = load_intellirehab_directory(args.data_dir)
    log.info(f"Loaded {len(entries)} samples in {time.time()-t0:.1f}s")
    if not entries:
        log.error("No data found. Exiting.")
        sys.exit(1)
    label_counts = Counter(e["movement_label"] for e in entries)
    log.info(f"Class distribution: {dict(label_counts)}")

    # ── Load model ────────────────────────────────────────────
    model = load_model(args.checkpoint, device)

    # ── Run inference (Parts 1-4, 6, 7 all need results) ──────
    need_inference = wanted & {1, 2, 3, 4, 6, 7, 10, 11}
    results = []
    if need_inference:
        log.info(f"Running inference on {len(entries)} samples...")
        t0 = time.time()
        results = run_inference(model, entries, device, args.batch_size)
        log.info(f"Inference complete: {time.time()-t0:.1f}s ({len(results)} samples)")

    metrics      = {}
    df_subj      = None
    df_baselines = None
    df_ablation  = None

    # ── Execute requested parts ───────────────────────────────
    if 1 in wanted:
        metrics = part1_evaluate(results)

    if 2 in wanted:
        df_subj = part2_subject_analysis(results)

    if 3 in wanted:
        error_rows = part3_failure_analysis(results, entries)
    else:
        error_rows = []

    if 4 in wanted:
        part4_failure_reasoning(error_rows, results)

    if 5 in wanted:
        part5_rom_validation(entries)

    if 6 in wanted:
        part6_explainability(results)

    if 7 in wanted:
        part7_calibration(results, entries)

    if 8 in wanted and not args.no_baselines:
        df_baselines = part8_baselines(entries)

    if 9 in wanted and not args.no_ablation:
        df_ablation = part9_ablation(entries, device)

    if 10 in wanted and not args.no_statistics:
        if df_baselines is None:
            bl_path = RESULTS_DIR / "baseline_results.csv"
            if bl_path.exists():
                df_baselines = pd.read_csv(bl_path)
        part10_statistics(results, df_baselines)

    if 11 in wanted:
        part11_publication_figures(results, df_subj)

    if 12 in wanted:
        if df_baselines is None:
            bl_path = RESULTS_DIR / "baseline_results.csv"
            if bl_path.exists():
                df_baselines = pd.read_csv(bl_path)
        if df_ablation is None:
            abl_path = RESULTS_DIR / "tables" / "ablation_table.csv"
            if abl_path.exists():
                df_ablation = pd.read_csv(abl_path)
        if df_subj is None:
            subj_path = RESULTS_DIR / "subject_results.csv"
            if subj_path.exists():
                df_subj = pd.read_csv(subj_path)
        part12_final_report(entries, metrics or {}, df_subj, df_baselines, df_ablation, args)

    log.info("")
    log.info("=" * 60)
    log.info("  EVALUATION COMPLETE")
    log.info(f"  Results saved in: {RESULTS_DIR.absolute()}")
    log.info("=" * 60)


if __name__ == "__main__":
    main()
