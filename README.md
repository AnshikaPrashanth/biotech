# Adaptive Spatial-Temporal Graph Attention Network with Personalized Calibration for Explainable Rehabilitation Movement Quality Assessment

This repository hosts a clinical-grade, end-to-end explainable Deep Learning and Calibration framework designed for Rehabilitation Movement Quality Assessment. The system uses a **Spatial-Temporal Graph Attention Network (ST-GAT)** to classify movement trials, combined with a **Personalized Range of Motion (ROM) Calibration Engine** to evaluate joint angular deviations without hardcoded thresholds.

---

## 🧬 Key Features
1. **No Subject Data Leakage**: Enforces Leave-One-Subject-Out (LOSO) cross-validation across all clinical evaluation folds.
2. **ST-GAT Re-Architected**: Features anatomical 25-joint spatial GAT convolutional blocks (correcting scaffold edge mapping bugs) paired with multi-head self-attention over sequence frames.
3. **Personalized ROM Calibration**: Combines Savitzky-Golay filters, linear interpolation, and Dynamic Time Warping (DTW) to align repetitions of varying lengths and compute adaptive tolerances.
4. **Multi-level Explainability**: Computes and logs frame-level temporal attention, joint attention maps (heatmap-ready), and specific ROM deviations for clinic reporting.
5. **Interactive Dashboard**: Streamlit interface containing a Live webcam analyzer (30 FPS), 3D skeleton visualizer, calibration template manager, and clinical trend charts.
6. **Model Export & Deployment**: Supports TorchScript tracing and ONNX exporting for edge devices.

---

## 🚀 Extended Features & Pipelines (Research Assessment Extension)

We have extended the system into an integrated **Real-Time + Video + Skeleton + Biomechanical + Uncertainty-Aware** rehab framework.

### 1. Multi-Modal Workflows
* **TXT Workflow:** Parses Kinect skeletal sequences from IntelliRehabDS files, applies linear interpolation to restore missing/zero values, performs pelvis centering and scale normalization, and routes the sequence to the ST-GAT and calibration engines.
* **Video Workflow:** Accepts video files (`.mp4`, `.avi`, `.mov`). OpenCV extracts frames; MediaPipe Pose extracts 33 3D world landmarks; coordinates are rotated and negated to match Kinect orientations; landmarks map to the project's 25 joints; and the sequence is normalized. Results are exported as `.npy` and `.txt` files alongside metadata.
* **Webcam Workflow:** Opens a camera feed. Runs MediaPipe Pose on frames, maps 33 world landmarks to 25 Kinect coordinates, normalizes coordinates, and holds a sliding sequence buffer of 64 frames. Model inference runs periodically at a configurable stride (default: every 5 frames) to avoid CPU bottlenecks.

### 2. MediaPipe to Kinect Coordinate Alignment
MediaPipe Pose world landmarks and Kinect IntelliRehabDS coordinate systems are aligned using a mathematically validated reflection matrix:
$$X_{\text{Kinect}} = -X_{\text{MediaPipe}}, \quad Y_{\text{Kinect}} = -Y_{\text{MediaPipe}}, \quad Z_{\text{Kinect}} = -Z_{\text{MediaPipe}}$$
This corrects for vertical inversion (MediaPipe Y points down, Kinect points up), lateral flipping (mirroring), and depth direction (MediaPipe Z points towards camera, Kinect points away), enabling MediaPipe inputs to feed directly into the trained ST-GAT model.

### 3. 33 MediaPipe → 25 Kinect Joints Mapping
A documented, anatomically sound mapping interpolates central spine joints (Neck, SpineMid, SpineShoulder, SpineBase) from MediaPipe hip/shoulder landmarks and aligns extremities to canonical indices. Missing joint details are handled using linear interpolation.

### 4. Biomechanical Error Attribution Engine
Calculates individual joint errors combining multiple physical and statistical dimensions:
1. **ROM Deviation:** DTW distance against personalized baselines.
2. **Left/Right Asymmetry:** Mean distance difference between bilateral counterpart joints (e.g. Left/Right Shoulder).
3. **Velocity / Acceleration Deviations:** Extracted using numerical differentiation and compared to baseline curves.
4. **Model Attention:** GAT spatial attention weights.

The final score is formulated as:
$$\text{JointError}_j = w_{\text{rom}} \cdot \text{ROMDeviation}_j + w_{\text{sym}} \cdot \text{SymmetryDeviation}_j + w_{\text{vel}} \cdot \text{VelocityDeviation}_j + w_{\text{acc}} \cdot \text{AccelerationDeviation}_j + w_{\text{att}} \cdot \text{AttentionContribution}_j$$
*Note: Attention is treated as an interpretability signal, not as causal proof of error.*

### 5. Movement Quality Score (MQS)
Calculates a continuous movement score from 0–100 combining ROM conformity, symmetry, smoothness, and biomechanical conformity:
$$\text{MQS} = 100 \cdot \sum_{c} w_c \cdot S_c$$
This is labeled as a **research movement-quality index** and is not a clinically validated score.

### 6. Uncertainty-Based Abstention
Instead of forcing predictions, the model utilizes calibrated confidence thresholding. If the predicted probability is below a configurable threshold (default: `0.70`), the final status is marked as `"Uncertain / Human Review"`, advising a repeat movement or manual therapist review.

### 7. Repetition Analysis
Uses angular velocities to segment trials into individual repetitions, evaluating quality trajectories, repetition-level MQS deviations, and movement quality degradation slopes over time (identifying improving, stable, or deteriorating execution).

### 8. Longitudinal Progress & SQLite DB
The database schema has been extended to log `movement_quality`, `uncertainty`, `decision_status`, `rom_score`, `symmetry_score`, `top_error_joints`, and `repetition_stats`, enabling weekly/monthly recovery dashboards.

### 9. Personalized Baseline Drift
Enables patient baselines to adapt to healthy progress over time. Baseline templates are updated using a conservative exponential rule:
$$B_{\text{new}} = \alpha \cdot B_{\text{old}} + (1-\alpha) \cdot X_{\text{healthy}}$$
Updates are restricted to high-confidence (`> 0.85`), low-error healthy movements, and can be disabled or rolled back via the dashboard.

### 10. Robustness Evaluation
Rotates coordinate arrays around the vertical Y-axis (0°, 15°, 30°, 45°) to evaluate view yaw robustness. Normalization makes the model highly resilient to moderate angle drifts.

---

## 📁 Repository Structure
```
├── src/
│   ├── dataset.py            # Data parser, 33->25 joint mapper, and sequence dataloaders
│   ├── model.py              # ST-GAT model with export-friendly forward passes
│   ├── calibration.py        # Range of Motion alignment and personalized calibrator
│   ├── database.py           # SQLite logger with dynamic schema migrations
│   ├── graph.py              # Anatomical graph construction utilities
│   ├── evaluation.py         # Standardized evaluation metrics
│   ├── visualization.py      # Plotly plots for 3D skeletons, attention maps, and trends
│   ├── utils.py              # Seeding, checkpointing, and ONNX/TorchScript exporters
│   ├── skeleton_pipeline.py  # Preprocessing, coordinate reflection, and mapping
│   ├── video_to_skeleton.py  # Video skeleton translation and side-by-side overlays
│   ├── webcam_pose.py        # Webcam capture thread and sliding buffer manager
│   ├── error_attribution.py  # Biomechanical error engine, MQS, and derivatives
│   ├── uncertainty.py        # Confidence thresholding, ECE, and risk-coverage curves
│   ├── feedback.py           # Deterministic feedback rules (AI-assisted feedback)
│   └── report_generator.py   # Reports exporter (JSON, Markdown, HTML)
├── tests/
│   └── test_features.py      # Comprehensive unit and pipeline test suite
├── app.py                    # Streamlit clinical dashboard application
├── train.py                  # LOSO cross-validation training execution script
├── inference.py              # Model inference, ROM checker, and model exporter CLI
├── robustness_eval.py        # Controlled coordinate rotations evaluation CLI
├── evaluate_features.py      # Main feature evaluation and results generator CLI
├── config.yaml               # YAML configuration (weights, MQS, uncertainty thresholds)
├── config.py                 # Config module loader
├── requirements.txt          # Project dependencies
└── README.md                 # Documentation
```

---

## 🛠️ Installation & Setup

1. **Clone the repository** and navigate to the project directory.
2. **Install the dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## 🚀 Running the System

### 1. Training (LOSO Cross-Validation)
```bash
python train.py --device cuda
```

### 2. Run Main Feature Evaluations (ECE, MQS, Ablations, Trajectories)
```bash
python evaluate_features.py
```
This generates and saves metrics tables, reliability diagrams, risk-coverage curves, error heatmaps, and repetition progress plots under the `results/` folder.

### 3. Run Camera Yaw Robustness Evaluations
```bash
python robustness_eval.py
```
This applies rotations of 0°, 15°, 30°, and 45° to evaluate yaw orientation robustness.

### 4. Run PyTest Unit Tests
```bash
python -m pytest tests/test_features.py
```

### 5. Launch the Streamlit Dashboard
```bash
streamlit run app.py
```

---

## 🧪 Loss Customization
You can switch the training loss criteria in `config.yaml` under `training.loss_type` between `"weighted_ce"` and `"focal"`.

---

## 📈 Model Export Outputs
During model export (via `inference.py` CLI arguments), the STGAT module automatically toggles `export_mode = True` and outputs `logits` of shape `[batch_size, 2]`.

---

## ⚠️ Research Disclaimer & Limitations
1. **Qualitative Verification:** Biomechanical error joint rankings represent a proxy score. If expert annotations do not exist, scores serve as relative indexes.
2. **Abstention Thresholding:** Abstention is based on prediction confidence, which is a proxy for model certainty, not a direct measurement of physical data quality.
3. **Webcam Validation:** Webcam hardware validation requires a connected device. If unavailable, use video upload or TXT upload pathways.
