# Evaluation Result Reconciliation

This document reconciles the differences in performance metrics between the **Original ST-GAT Evaluation** and the **Viewpoint Robustness Evaluation (at 0°)**.

## 1. Metric Comparison Summary

| Metric | Original ST-GAT (Overall Dataset) | Robustness Evaluation (0° Rotation) |
| :--- | :---: | :---: |
| **Accuracy** | 0.8548 | 0.9124 |
| **Balanced Accuracy** | 0.8379 | 0.9556 |
| **Macro F1-Score** | 0.8000 | 0.5968 |
| **MCC** | 0.6129 | 0.5968 |
| **ROC-AUC** | 0.9321 | 0.9330 |

---

## 2. Experimental Protocols

### A. Original ST-GAT Evaluation Protocol
- **Checkpoints:** Fold-specific checkpoints (`checkpoints/fold_*.pt`) for Leave-One-Subject-Out (LOSO) cross-validation, except for the overall summary baseline evaluation which loaded `checkpoints/best_model.pt` (the checkpoint from the last trained fold) to evaluate on the entire dataset.
- **Dataset Split:** Tested on **all 30 subjects** (subjects 101 to 307) across all trials, containing 2,518 total samples.
- **Preprocessing & Padding:** Center-cropped sequences longer than 64 frames. For sequences shorter than 64, loaded their native length and dynamically padded them with **zeros** to the maximum sequence length of each batch (batch size = 16) during data collation.
- **Inference Mode:** Batched inference (batch size = 16).

### B. Robustness Evaluation Protocol (at 0°)
- **Checkpoints:** A single model checkpoint (`checkpoints/best_model.pt`) representing the last trained fold.
- **Dataset Split:** Evaluated only on a subset of **two subjects** (subject 101 and subject 102), containing 217 total samples.
- **Preprocessing & Padding:** Cropped or padded all sequences to **exactly 64 frames** using **last-frame repetition** (edge padding).
- **Inference Mode:** Single-sample inference (batch size = 1).

---

## 3. Reasons for Divergence

1. **Dataset Size and Cohort Composition:**
   The original evaluation covers all 30 subjects, including subjects with low classification scores (e.g., subject 210 has 26.47% accuracy). The robustness evaluation evaluates only subjects 101 and 102, who are high-performing healthy-dominated subjects (subject 101 has 98.13% baseline accuracy; subject 102 has 90.91%). This demographic selection shifts the accuracy upwards from 0.8548 to 0.9124.

2. **Temporal Padding Modality:**
   In the original evaluation, sequences shorter than 64 frames are padded with zeros to the batch maximum. The ST-GAT model averages features over time without masking the padded zeros, reducing logit magnitudes. In the robustness evaluation, sequences are edge-padded to exactly 64 frames using last-frame repetition, which preserves active joint coordinates and produces more robust model predictions.

3. **Inference Batching:**
   The batch-dependent padding in the original evaluation causes sample logits to vary depending on the other samples in the same batch, whereas the robustness evaluation uses single-sample inference (batch size = 1) with deterministic padding.

---

## 4. Validity of Comparison and Paper Recommendations

### Is the comparison valid?
No, a direct comparison between the two sets of numbers is **invalid**. They represent different experiments (evaluating the entire cohort via dynamic zero-padding vs. evaluating a subset of subjects 101/102 via fixed edge-padding).

### Which numbers should be reported in the paper?
- **For Cohort-Wide Performance:** Report the original **0.8548 accuracy** from the full 30-subject LOSO evaluation to demonstrate generalization across all subjects.
- **For Viewpoint Robustness:** Report the robustness metrics (0° = 91.24%, 15° = 87.10%, 30° = 68.20%, 45° = 61.29%) clearly labeled as a **viewpoint robustness study on the subject 101/102 test subset**, showing the relative degradation as camera yaw angles increase.
- **For Deployment Mode:** Report that single-sample inference with edge-padding to 64 frames achieves 91.24% accuracy on the test subjects, compared to batch-based zero-padding.
