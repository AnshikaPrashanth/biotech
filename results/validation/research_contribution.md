# Research Engineering & Integration Contribution Report

This document separates the reused components of the baseline rehabilitation movement assessment system from the new engineering and validation contributions introduced in this pass.

---

## 1. Reused Core Components (Baseline)

The following components represent the foundational research codebase and have been preserved intact to maintain historical reproducibility:

1. **ST-GAT Model Architecture (`src/model.py` & `src/graph.py`):** The Spatial-Temporal Graph Attention Network architecture, including the spatial GAT layer, temporal convolution, and temporal self-attention.
2. **Pre-trained Model Checkpoints (`checkpoints/`):** The fold-specific PyTorch weights (`fold_*.pt`) generated during the cohort Leave-One-Subject-Out (LOSO) training runs.
3. **Primary Evaluation Protocol (`evaluate_and_report.py`):** The cohort-wide cross-validation evaluation routines.

---

## 2. New Engineering & Integration Contributions

The following modules, pipelines, and validation passes were designed, implemented, and verified in this pass:

### A. Core Multi-Modal Skeleton Pipeline
- **MediaPipe Pose Integration (`src/video_to_skeleton.py` & `src/webcam_pose.py`):** Direct landmark extraction from standard video files and real-time webcam feeds.
- **MediaPipe ↔ Kinect Joint Mapping (`src/dataset.py`):** An anatomical mapping algorithm converting 33 MediaPipe landmarks into the 25-joint Kinect v2 representation.
- **Coordinate Alignment Rotation Matrix (`src/skeleton_pipeline.py` & `tools/validate_coordinate_alignment.py`):** A validated transformation matrix correcting lateral, vertical, and depth orientations between the two coordinate systems.

### B. Movement Quality Index & Clinician Tools
- **Movement Quality Score (MQS) (`src/error_attribution.py`):** A normalized, 0-to-100 index synthesized from joint range of motion (ROM), bilateral symmetry, temporal smoothness, and biomechanical trajectory conformity.
- **Confidence-Based Abstention (`src/uncertainty.py`):** Threshold-controlled epistemic uncertainty filtering to improve selective prediction accuracy on noisy sequences.
- **Repetition Segmentation (`src/calibration.py`):** Temporal velocity-based movement segmentation to analyze performance degradation across repetitions.
- **Adaptive Personalized ROM Baseline (`src/analysis_pipeline.py`):** Exponential moving average (EMA) baseline template updates with strict clinical safety constraints and a history-based rollback mechanism.

### C. Scientific Verification & Validation Reports
- **Result Reconciliation Audit (`results/validation/result_reconciliation.md`):** Discovered the dynamic zero-padding batch discrepancy causing divergence between evaluation modes.
- **Biomechanical Symmetry Correction (`src/error_attribution.py`):** Refactored the symmetry formula from raw Euclidean joint distance to X-reflected coordinate distance, eliminating anatomical bias.
- **Selective Accuracy Trade-off Study (`results/validation/uncertainty_validation.md`):** Checked for validation target leakage and mapped the selective accuracy gains (up to 97.74% accuracy) across confidence thresholds.
- **Data Leakage Split Audit (`results/validation/leakage_audit.md`):** Verified 100% subject-wise disjointness across all 30 cross-validation folds.
