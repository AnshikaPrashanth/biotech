# Statistical Significance Analysis

Generated: 2026-08-10T11:09:07.478043+00:00

## Bootstrap Confidence Intervals (n=2000 resamples)
| Metric | Estimate | 95% CI Lower | 95% CI Upper |
|--------|----------|--------------|--------------|
| Accuracy | 0.8548 | 0.8409 | 0.8683 |
| Balanced Accuracy | 0.8384 | 0.8203 | 0.8558 |
| ROC-AUC | 0.9318 | 0.9198 | 0.9423 |
| MCC | 0.6137 | 0.5786 | 0.6484 |
| F1 (macro) | 0.7998 | 0.7817 | 0.8174 |

## Pairwise Comparison: ST-GAT vs Baselines

Comparing LOSO per-subject accuracy distributions.

| Baseline | Wilcoxon p-value | Effect Size (r) | Significant? |
|----------|-----------------|----------------|--------------|
| ST-GAT (Ours) | 0.3513 | 0.1733 | No |
| Random Forest | 0.6288 | 0.0904 | No |
| Gradient Boosting | 0.5812 | 0.1030 | No |
| XGBoost | 0.3917 | 0.1594 | No |
| LSTM | 0.5594 | 0.1090 | No |
| GRU | 0.8758 | 0.0293 | No |