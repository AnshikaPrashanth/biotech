# Rehab AI Assessment Report
**Date:** N/A
**Patient ID:** 101 | **Exercise:** 4 | **Source:** txt

---

## 1. Executive Summary

| Metric | Value | Reference / Status |
| :--- | :--- | :--- |
| **Prediction Verdict** | Uncertain / Human Review | 54.21% Confidence |
| **Movement Quality Score** | 67.0 / 100 | Research Movement-Quality Index |
| **Uncertainty Status** | Uncertain / Human Review | Threshold: 0.70 |
| **Repetitions Detected** | 3 | Trajectory: Stable |

---

## 2. Model Inference Output
> [!NOTE]
> This section displays the model's raw classification and attention weights. These represent statistical patterns detected by the neural network.

- **Class Probabilities:**
  - Healthy (0): 0.4579
  - Compensated (1): 0.5421
- **Confidence Status:** 0.5421 (Low Confidence / Review Recommended)

### Spatial Joint Attention (Top 5 joints)
- **SpineShoulder**: 0.8050
- **SpineBase**: 0.7800
- **WristRight**: 0.7589
- **WristLeft**: 0.7515
- **KneeLeft**: 0.6993

---

## 3. Biomechanical Measurements
> [!IMPORTANT]
> These measurements represent actual physical calculations derived from the joint trajectories, completely independent of the classification model.

### Movement Quality Score Breakdown
- **ROM Conformity:** 80.0%
- **Bilateral Symmetry:** 33.0%
- **Temporal Consistency:** 91.3%
- **Biomechanical Conformity:** 80.0%

### Ranked Joint Deviations (Top 5 Error Scores)
Each joint score combines ROM deviation, bilateral asymmetry, velocity deviation, and model attention weight.
1. **ShoulderRight** — Score: 0.66
2. **KneeLeft** — Score: 0.59
3. **KneeRight** — Score: 0.59
4. **HipRight** — Score: 0.53
5. **ElbowLeft** — Score: 0.52

For these joints, detailed features are:
| Joint Name | ROM Deviation | Asymmetry | Velocity Dev | overall score |
| :--- | :---: | :---: | :---: | :---: |
| ShoulderRight | 0.97 | 1.00 | 0.00 | 0.66 |
| KneeLeft | 1.00 | 0.60 | 0.00 | 0.59 |
| KneeRight | 1.00 | 0.60 | 0.00 | 0.59 |
| HipRight | 0.87 | 0.50 | 0.00 | 0.53 |
| ElbowLeft | 0.50 | 1.00 | 0.00 | 0.52 |

---

## 4. Repetition Analysis
- **Repetitions segmented:** 3
- **Quality progression slope:** -0.047 per repetition
- **Fatigue / Degradation status:** **Stable**

---

## 5. Interpretive Feedback & Recommendations
> [!TIP]
> **AI-Assisted Exercise Feedback:** The following comments are rule-based suggestions generated directly from the biomechanical deviations recorded above. This does not constitute a clinical medical diagnosis.

- The movement could not be assessed reliably. Please repeat the movement under better lighting or camera placement.

---

## 6. Limitations & Disclaimer
1. **No Clinical Validation:** The Movement Quality Score and error ranking are biomechanical indices for research and reference only.
2. **Camera Calibration:** Tracking quality depends heavily on lighting, clothing, and occlusion. High uncertainty flags should prompt a retry.
