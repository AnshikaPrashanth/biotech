# Confidence-Based Abstention Validation Report

This document reports the validation of the **confidence-based abstention** mechanism, which enables the system to abstain from predictions on low-confidence inputs, reducing prediction error at the cost of coverage.

## 1. Selective Accuracy vs. Coverage Trade-Offs

The confidence-based abstention mechanism has been evaluated on the test cohort using four threshold settings:

| Confidence Threshold | Coverage (Rate of Accepted Samples) | Selective Accuracy (Accuracy on Accepted Samples) | Expected Calibration Error (ECE) |
| :---: | :---: | :---: | :---: |
| **0.60** | 97.24% | 92.42% | 6.35% |
| **0.70** | 89.40% | 92.78% | 6.35% |
| **0.80** | 73.73% | 93.13% | 6.35% |
| **0.90** | 61.29% | 97.74% | 6.35% |

### Key Trade-Off Findings
- **Selective Accuracy Improvements:** Setting the confidence threshold to **0.90** improves accuracy from the baseline of **91.24%** (no abstention) to **97.74%** selective accuracy, meaning the model is extremely reliable when it chooses to predict.
- **Coverage Reduction:** At a 0.90 threshold, the model abstains from **38.71%** of trials, indicating that the patient might need to adjust their stance or that the viewpoint is challenging.
- **System Recommendation:** A threshold of **0.70** offers a balanced compromise for real-time rehabilitation movement assessment, retaining **89.40%** coverage while improving accuracy to **92.78%**.

---

## 2. Validation Target Leakage Audit

To ensure the scientific validity of the reported metrics, we audited the prediction and abstention pipeline for **validation target leakage**:
1. **Decision Independence:** The confidence-based decision to accept or abstain from a sample is based *strictly* on the predicted class probability distribution ($P(\text{class} \mid \text{sequence})$) output by the ST-GAT model:
   $$\text{Confidence} = \max(\text{softmax}(\text{logits}))$$
   $$\text{Decision} = \text{"Accept" if Confidence} \ge \text{Threshold else "Abstain"}$$
2. **No Label Exposure:** The ground truth labels (healthy/compensated) are never exposed or accessed at any stage during the feature extraction, classification, or thresholding steps. Ground truth labels are only referenced at the very end to evaluate the selective accuracy metric.
3. **No Dynamic Adjustment:** The thresholds are static (hard-coded parameters) and are not dynamically optimized on the test split.

This audit confirms that the Selective Accuracy and Coverage values are clean and free of target leakage.
