# Preprocessing Consistency Audit

This document audits the preprocessing steps across the three input modalities: **IntelliRehabDS TXT**, **Video-derived skeleton**, and **Webcam skeleton**.

## 1. Preprocessing Steps Comparison

| Preprocessing Step | TXT Files | Video Upload | Webcam Feed |
| :--- | :--- | :--- | :--- |
| **Coordinate Space** | Kinect (Frontal X-right, Y-up, Z-away) | MediaPipe World Landmarks | MediaPipe World Landmarks |
| **Rotation Transformation** | None (Native Kinect) | Negate $X, Y, Z$ coordinates | Negate $X, Y, Z$ coordinates |
| **Joint Mapping** | None (Native 25 joints) | 33 to 25 joint mapper | 33 to 25 joint mapper |
| **Missing Frame Handling** | Linear interpolation (`interpolate_missing_frames`) | Linear interpolation (`interpolate_missing_frames`) | Temporal smoothing + buffer interpolation |
| **Pelvis Centering** | SpineBase (index 0) centering | SpineBase (index 0) centering | SpineBase (index 0) centering |
| **Scale Normalization** | Divided by max joint spread | Divided by max joint spread | Divided by max joint spread |
| **Sequence Length Alignment** | Dynamic batch padding (offline) / 64-cropping | Cropped/padded to exactly 64 (last-frame pad) | Cropped/padded to exactly 64 (last-frame pad) |

---

## 2. Identified Preprocessing Discrepancies

During our validation pass, we identified a critical discrepancy in **Sequence Length Alignment** between the **Offline Evaluation Pipeline** (`evaluate_and_report.py`) and the **Real-Time Deployment Pipeline** (`analyze_sequence()` / `app.py` / `evaluate_features.py`):

1. **Offline Evaluation Pipeline (Dataloader batch mode):**
   * If a sequence is longer than 64, it is center-cropped to 64.
   * If a sequence is shorter than 64, it is loaded at its native length.
   * During collation, the batch is padded with **zeros** (`torch.zeros`) to the maximum length of that specific batch (which varies and is often less than 64).
   * Since the ST-GAT pooling averages over all frames without masking, the logits are batch-dependent and affected by zero padding.

2. **Real-Time Deployment Pipeline (Single-sample mode):**
   * If a sequence is longer than 64, it is center-cropped to 64.
   * If a sequence is shorter than 64, it is padded with **last-frame repetition** (edge padding) to exactly 64.
   * The model averages over exactly 64 frames.

### Impact on Results
This difference in padding (zero-padding to batch-max vs. edge-padding to 64) is the primary driver behind the discrepancy between the overall ST-GAT cross-validation results (e.g., subjects 101/102 combined accuracy of 94.47%) and the deployment-ready robustness 0° evaluation (91.24%). 

For the research paper, the **dynamic zero-padding in batch evaluation** represents the historical baseline metric, while the **edge-padded single-sample mode** represents the true real-time performance and should be reported as the system's operational deployment metric.
