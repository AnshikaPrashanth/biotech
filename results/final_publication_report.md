# ST-GAT Rehabilitation Assessment — Publication Report

> **Generated:** 2026-08-10 11:09 UTC
> **Checkpoint:** `checkpoints/best_model.pt`
> **Device:** `cpu`

---

## 1. Dataset Summary

| Item | Value |
|------|-------|
| Total Samples | 2589 |
| Unique Subjects | 30 |
| Healthy Samples (class 0) | 2059 |
| Compensated Samples (class 1) | 530 |
| Class Ratio (H:C) | 2059:530 |
| Exercise Types | 0, 1, 2, 3, 4, 5 |

- **0**: 584 samples
- **1**: 112 samples
- **2**: 404 samples
- **3**: 511 samples
- **4**: 426 samples
- **5**: 552 samples

---

## 2. Model Configuration

| Parameter | Value |
|-----------|-------|
| Architecture | ST-GAT (Spatial-Temporal Graph Attention Network) |
| Parameters | 53,090 |
| Hidden Dim | 64 |
| Attention Heads | 4 |
| Dropout | 0.2 |
| Sequence Length | 64 |
| Joints | 25 (Kinect v2 / IntelliRehabDS) |
| Input Dim | 3 (x, y, z) |
| Classes | 2 (Healthy=0, Compensated=1) |

---

## 3. Training Protocol

| Setting | Value |
|---------|-------|
| Cross-Validation | Leave-One-Subject-Out (LOSO) |
| Optimizer | AdamW |
| Learning Rate | 0.0002 |
| Weight Decay | 0.0001 |
| Max Epochs | 80 |
| Early Stopping Patience | 8 |
| Batch Size | 64 |
| Loss | Weighted CrossEntropy |
| Augmentation | Gaussian noise, rotation, scaling, temporal crop |

---

## 4. Evaluation Metrics

| Metric | Value |
|--------|-------|
| Accuracy | **0.8548** |
| Balanced Accuracy | **0.8379** |
| Sensitivity | **0.8094** |
| Specificity | **0.8664** |
| Precision (macro) | **0.7779** |
| Recall (macro) | **0.8379** |
| F1 (macro) | **0.8000** |
| ROC-AUC | **0.9321** |
| PR-AUC | **0.8008** |
| MCC | **0.6129** |
| Cohen's Kappa | **0.6024** |
| True Positives | 429 |
| True Negatives | 1784 |
| False Positives | 275 |
| False Negatives | 101 |
| Mean Confidence | 0.8738 ± 0.1389 |

### Per-Class Metrics

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|-----|---------|
| Healthy | 0.9464 | 0.8664 | 0.9047 | 2059 |
| Compensated | 0.6094 | 0.8094 | 0.6953 | 530 |

---

## 5. Subject-Wise LOSO Analysis

| Metric | Mean | Std | CI-95 Lower | CI-95 Upper |
|--------|------|-----|-------------|-------------|
| Accuracy | 0.8220 | 0.1866 | 0.7552 | 0.8888 |
| Balanced Accuracy | 0.7723 | 0.1943 | 0.7028 | 0.8418 |
| F1 Macro | 0.5662 | 0.1268 | 0.5208 | 0.6116 |
| Mcc | 0.2011 | 0.2483 | 0.1122 | 0.2899 |
| Sensitivity | 0.4793 | 0.4261 | 0.3268 | 0.6318 |
| Specificity | 0.7701 | 0.2574 | 0.6780 | 0.8622 |
| Roc Auc | 0.7801 | 0.1920 | 0.7114 | 0.8487 |
| Pr Auc | 0.6260 | 0.2774 | 0.5267 | 0.7252 |

---

## 6. Explainability — Spatial Attention

**Top-5 Joints by Mean Attention Weight:**

| Rank | Joint | Mean Attention | Std |
|------|-------|----------------|-----|
| 1 | SpineShoulder | 0.8054 | 0.0022 |
| 2 | SpineBase | 0.7790 | 0.0092 |
| 3 | WristRight | 0.7531 | 0.0039 |
| 4 | WristLeft | 0.7525 | 0.0028 |
| 5 | KneeRight | 0.7025 | 0.0148 |

---

## 7. Calibration

| Metric | Value |
|--------|-------|
| ECE (Expected Calibration Error) | 0.0311 |
| MCE (Maximum Calibration Error) | 0.1112 |
| Subjects Fitted (ROM) | 30 |

---

## 8. Baseline Comparison

| Model | Accuracy | Balanced Acc | F1 | ROC-AUC | MCC |
|-------|----------|--------------|----|---------|-----|
| ST-GAT (Ours) | 0.8548 | 0.8379 | 0.8000 | 0.9321 | 0.6129 |
| Random Forest | 0.8389 | 0.6325 | 0.6625 | 0.8741 | 0.4131 |
| Gradient Boosting | 0.8413 | 0.6522 | 0.6841 | 0.8122 | 0.4292 |
| XGBoost | 0.8521 | 0.6828 | 0.7177 | 0.8764 | 0.4803 |
| LSTM | 0.8015 | 0.5536 | 0.5514 | 0.7079 | 0.2011 |
| GRU | 0.8165 | 0.5946 | 0.6110 | 0.6627 | 0.3026 |

---

## 9. Ablation Study

| Configuration | Accuracy | Balanced Acc | F1 | ROC-AUC |
|---------------|----------|--------------|----|---------|
| Full ST-GAT | 0.8644 | 0.7971 | 0.7940 | 0.8604 |
| w/o Graph Attention | 0.8629 | 0.7814 | 0.7860 | 0.8546 |
| w/o Temporal Attention | 0.7393 | 0.6175 | 0.6132 | 0.6116 |

---

## 10. Generated Files

### Metrics
- `results/metrics.json` — All evaluation metrics
- `results/metrics.csv` — Metrics in CSV
- `results/classification_report.txt` — Full sklearn classification report
- `results/subject_results.csv` — Per-subject LOSO metrics
- `results/subject_statistics.csv` — LOSO statistics with CI
- `results/statistical_analysis.md` — Bootstrap CI and significance tests
- `results/attention_report.json` — Full explainability report

### Figures
- `results/confusion_matrix.png`
- `results/roc_curve.png`
- `results/pr_curve.png`
- `results/figures/confidence_histogram.png`
- `results/figures/subject_barplots.png`
- `results/figures/subject_heatmap.png`
- `results/figures/attention_heatmaps.png`
- `results/figures/temporal_attention.png`
- `results/figures/attention_entropy.png`
- `results/figures/rom_histograms.png`
- `results/figures/joint_boxplots.png`
- `results/figures/calibration_reliability.png`
- `results/figures/confidence_by_class.png`
- `results/figures/failure_causes.png`
- `results/figures/baseline_comparison.png`
- `results/figures/exercise_performance.png`

### Tables
- `results/tables/joint_importance.csv`
- `results/tables/frame_importance.csv`
- `results/tables/attention_entropy.csv`
- `results/tables/rom_statistics.csv`
- `results/tables/calibration_statistics.csv`
- `results/tables/baseline_results.csv`
- `results/tables/ablation_table.csv`
- `results/tables/comparison_tables.tex`

### Error Analysis
- `results/errors/error_analysis.md`
- `results/errors/error_analysis.csv`
- `results/errors/failure_causes.csv`
- `results/errors/error_rate_by_exercise.csv`
- `results/errors/error_rate_by_subject.csv`

---

## 11. Discussion

The ST-GAT model leverages spatial graph attention across the 25-joint Kinect skeleton and temporal multi-head self-attention to identify compensatory movement patterns. The Leave-One-Subject-Out evaluation protocol ensures the reported metrics reflect genuine generalisation to unseen individuals.

## 12. Limitations

- Dataset limited to IntelliRehabDS exercises; generalisation to other protocols requires further validation.
- ROM calibration depends on availability of healthy baseline trials per subject.
- Kinect v2 tracking noise may affect skeleton quality for fast movements.

## 13. Future Work

- Extend to multi-label exercise quality scoring.
- Incorporate RGB video stream for multi-modal fusion.
- Validate on clinical populations and larger cohorts.
- Explore real-time inference optimisation for embedded deployment.

---

*This report was automatically generated by `evaluate_and_report.py --full`*