# Frozen Experimental Protocol Notes
**Project Title:** Adaptive Spatial-Temporal Graph Attention Network with Personalized Calibration for Explainable Rehabilitation Movement Quality Assessment  
**Date:** September 30, 2026  
**Status:** FROZEN EXPERIMENTAL PROTOCOL (Phase 3 Execution)

---

## 1. Dataset & Filtering Specifications
- **Physical Raw Skeleton Files:** 2,589 `.txt` files extracted from `SkeletonData/SkeletonData/RawData/`.
- **Physical Subjects Count:** 30 subjects (`101–107`, `201–207`, `209`, `210–217`, `301–307`). Subject `208` is absent in IntelliRehabDS.
- **Label 3 Exclusion Handling:** 12 files with filename `CorrectLabel` = 3 (unclassified / ambiguous repetitions) are **explicitly excluded** from training, validation, testing, calibration, and metric computation. Label 3 is NOT converted into Class 0.
- **Final Valid Dataset Size:** **2,577 samples**.
- **Binary Target Terminology & Class Distribution:**
  - `0`: **Correct execution** (2,047 samples / 79.43%) — derived from `CorrectLabel` == 1.
  - `1`: **Incorrect execution** (530 samples / 20.57%) — derived from `CorrectLabel` == 2.
- **Gestures Evaluated:** Gestures 0 through 8 (standing stance, elbow flexion L/R, shoulder flexion L/R, side lunge L/R, squat, deep squat).

---

## 2. Preprocessing & Padding Protocol
- **Pelvis Centering:** Subtracts `SpineBase` (joint index 0) coordinates from all 25 joints per frame.
- **Scale Normalization:** Divides centered coordinates by the maximum joint spread within each sample sequence.
- **Missing Landmark Interpolation:** Applies linear temporal interpolation to fill zero-valued joints within each sequence instance.
- **Target Sequence Length:** Fixed sequence length of $T = 64$ frames.
- **Padding Strategy & Masking:** Sequences shorter than 64 frames are padded with zeros, and a boolean mask `valid_frame_mask` ($T \in \{True, False\}$) is passed into `STGAT`. `TemporalAttentionBlock` and temporal pooling use this mask to ensure padded frames do NOT participate in self-attention or global average pooling.
- **Resampling Strategy:** Sequences longer than 64 frames are cropped (random temporal crop during training, center crop during validation/testing).

---

## 3. Leave-One-Subject-Out (LOSO) Cross-Validation
- **Number of Folds:** 30 folds.
- **Fold Partitioning:** For each of the 30 folds, exactly 1 subject is the outer test subject. Of the remaining 29 development subjects, the first sorted subject ID is the deterministic inner-validation subject and the other 28 are used for model fitting.
- **Subject Disjointness:** Training, inner validation, and outer test subject sets are pairwise disjoint. The outer subject is evaluated only after the checkpoint is selected and frozen.
- **Internal Validation & Checkpoint Selection:** `train.run_fold()` selects the checkpoint and stops early by minimizing validation error rate ($1 - \\text{accuracy}$) on the single inner-validation subject, with the configured delta and patience. The outer subject is not used for fitting, selection, early stopping, hyperparameter selection, or threshold selection.

---

## 4. OOF Prediction Accumulation Protocol
- Every test sample $i \in \{1, \dots, 2,577\}$ is evaluated exactly once when its subject is held out.
- Predictions are logged in `results/final/OOF_PREDICTIONS.csv` with fields: `sample_id`, `file_path`, `subject_id`, `gesture_id`, `fold`, `y_true`, `y_prob`, `y_pred`, `confidence`, `model_version`, `seed`.
- All final metrics (Pooled OOF Metrics and Subject-Level Statistics) are derived strictly from `OOF_PREDICTIONS.csv`.

---

## 5. Model Architecture & Hyperparameters
- **Device & Execution:** CPU sequential execution (`DEVICE = 'cpu'`, `torch.set_num_threads(4)`).
- **Architecture:** `STGAT` (Spatial GATConv 4-heads, 1D TCN kernel size 3, Temporal MultiheadAttention 4-heads with padding mask, Global Pooling, LayerNorm MLP classifier).
- **Input Dimension:** $3$ (X, Y, Z coordinates).
- **Hidden Dimension:** $64$.
- **Attention Heads:** $4$.
- **Dropout:** $0.2$.
- **Batch Size:** $16$ (or $8$ for memory safety).
- **Optimizer:** `AdamW` (`lr = 0.0002`, `weight_decay = 0.0001`).
- **Loss Function:** `CrossEntropyLoss` (class balancing handled by `WeightedRandomSampler` on training fold entries).
- **Early Stopping:** Patience = 8 epochs based on internal validation error rate ($1 - \\text{accuracy}$); `early_stopping_delta = 0.001`.
- **Other selection parameters:** Learning rate ($0.0002$), weight decay ($0.0001$), epoch cap (50), confidence threshold (0.70), and biomechanical/MQS weights are fixed in the frozen config. The classifier OOF path does not tune confidence thresholds, calibration, or MQS using outer-test results; confidence thresholding and MQS are not used to produce its class predictions.
- **Random Seed:** `42`.

---

## 6. Discrepancy Note & Publication Positioning
- The repository protocol (2,577 valid samples, 30 physical subjects, 64-frame masked padding, pelvis normalization) is evaluated in a 30-fold OOF LOSO framework.
- Results are reported as **out-of-fold generalizability metrics** on IntelliRehabDS. Direct baseline comparisons are evaluated under the exact same 30-fold OOF protocol on the exact same 2,577 valid samples.
