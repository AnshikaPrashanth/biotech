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

## 📁 Repository Structure
```
├── src/
│   ├── dataset.py         # Data parser, 33->25 joint mapper, and sequence dataloaders
│   ├── model.py           # ST-GAT model with export-friendly forward passes
│   ├── calibration.py     # Range of Motion alignment and personalized calibrator
│   ├── database.py        # SQLite logger for patient sessions and progress queries
│   ├── graph.py           # Anatomical graph construction and batched edge index utilities
│   ├── evaluation.py      # Standardized metrics (MCC, Kappa, Balanced Accuracy, ROC AUC)
│   ├── visualization.py   # Plotly plots for 3D skeletons, attention maps, and trends
│   └── utils.py           # Seeding, checkpointing, and ONNX/TorchScript exporters
├── app.py                 # Streamlit clinical dashboard application
├── train.py               # LOSO cross-validation training execution script
├── inference.py           # Model inference, ROM checker, and model exporter CLI
├── config.yaml            # YAML configuration for parameters and paths
├── config.py              # Backward-compatible config module loader
├── requirements.txt       # Project dependencies
├── GoogleColabTraining.ipynb # Jupyter notebook for Colab cloud GPU training
└── README.md              # Documentation
```

---

## 🛠️ Installation & Setup

1. **Clone the repository** and navigate to the project directory.
2. **Install the dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   *Note: For Windows compatibility, `num_workers` in `config.yaml` is set to 0 to prevent multiprocessing socket errors.*

---

## 📊 Dataset Structure
The system parses files from the **IntelliRehabDS** dataset. Place your data files in the path specified by the `paths.data_dir` variable in `config.yaml` (default: `SkeletonData/SkeletonData/RawData`).

Filenames must adhere to the official IntelliRehabDS naming convention:
```
SubjectID_DateID_GestureLabel_RepetitionNumber_CorrectLabel_Position.txt
```
* `CorrectLabel` at index 4 (0-indexed split by `_`):
  * `1` = Correct Execution -> Map to target `0` (Healthy)
  * `2` = Incorrect/Compensated -> Map to target `1` (Compensated)

---

## 🚀 Running the System

### 1. Training (LOSO Cross-Validation)
Train models for all clinical subjects sequentially using Leave-One-Subject-Out Cross-Validation with GPU acceleration:
```bash
python train.py --device cuda
```
To run a fast validation fold training for a single specific left-out subject (e.g., leaving out subject `101`) to speed up CPU checks:
```bash
python train.py --fold 101 --epochs 5 --batch-size 4 --device cpu
```

### 2. Running Inference & Model Export
Run inference on a single skeleton sequence file to predict class label, confidence, top ROM joint deviations, and export models:
```bash
python inference.py --input-file SkeletonData/SkeletonData/RawData/101_18_0_1_1_stand.txt --export-onnx checkpoints/st_gat_model.onnx --export-ts checkpoints/st_gat_model.ts
```

### 3. Launching the Streamlit Clinical Dashboard
Start the production interactive Streamlit dashboard to analyze upload trials, capture real-time webcam video feeds, run calibrations, and check progression scores:
```bash
streamlit run app.py
```

---

## 🧪 Loss Customization
You can switch the training loss criteria in `config.yaml` under `training.loss_type` between:
* `"weighted_ce"`: Weighted CrossEntropy balanced dynamically using class counts of the training fold split.
* `"focal"`: Focal Loss designed for highly imbalanced dataset scenarios to focus learning on difficult boundary classification frames.

---

## 📈 Model Export Outputs
During model export (via `inference.py` CLI arguments), the STGAT module automatically toggles `export_mode = True`. This routes execution through a specialized `forward_export` method, bypassing dynamic dict unpacking which is unsupported by ONNX tracing. The exported models output `logits` of shape `[batch_size, 2]`.
