# Rehab AI Assessment Report
**Date:** N/A
**Patient ID:** 101 | **Exercise:** Stand | **Source:** video

---

## 1. Executive Summary

| Metric | Value | Reference / Status |
| :--- | :--- | :--- |
| **Prediction Verdict** | Compensated | 85.87% Confidence |
| **Movement Quality Score** | 56.8 / 100 | Research Movement-Quality Index |
| **Uncertainty Status** | Compensated | Threshold: 0.70 |
| **Repetitions Detected** | 9 | Trajectory: Stable |

---

## 2. Model Inference Output
> [!NOTE]
> This section displays the model's raw classification and attention weights. These represent statistical patterns detected by the neural network.

- **Class Probabilities:**
  - Healthy (0): 0.1413
  - Compensated (1): 0.8587
- **Confidence Status:** 0.8587 (Sufficient)

### Spatial Joint Attention (Top 5 joints)
- **SpineShoulder**: 0.8044
- **SpineBase**: 0.7805
- **WristLeft**: 0.7491
- **WristRight**: 0.7457
- **HipRight**: 0.6998

---

## 3. Biomechanical Measurements
> [!IMPORTANT]
> These measurements represent actual physical calculations derived from the joint trajectories, completely independent of the classification model.

### Movement Quality Score Breakdown
- **ROM Conformity:** 64.8%
- **Bilateral Symmetry:** 20.0%
- **Temporal Consistency:** 88.9%
- **Biomechanical Conformity:** 80.0%

### Ranked Joint Deviations (Top 5 Error Scores)
Each joint score combines ROM deviation, bilateral asymmetry, velocity deviation, and model attention weight.
1. **KneeRight** — Score: 0.67
2. **HipRight** — Score: 0.67
3. **ShoulderLeft** — Score: 0.63
4. **HipLeft** — Score: 0.59
5. **KneeLeft** — Score: 0.56

For these joints, detailed features are:
| Joint Name | ROM Deviation | Asymmetry | Velocity Dev | overall score |
| :--- | :---: | :---: | :---: | :---: |
| KneeRight | 1.00 | 1.00 | 0.00 | 0.67 |
| HipRight | 0.98 | 1.00 | 0.00 | 0.67 |
| ShoulderLeft | 0.87 | 1.00 | 0.00 | 0.63 |
| HipLeft | 0.72 | 1.00 | 0.00 | 0.59 |
| KneeLeft | 0.61 | 1.00 | 0.00 | 0.56 |

---

## 4. Repetition Analysis
- **Repetitions segmented:** 9
- **Quality progression slope:** -0.950 per repetition
- **Fatigue / Degradation status:** **Stable**

---

## 5. Interpretive Feedback & Recommendations
> [!TIP]
> **AI-Assisted Exercise Feedback:** The following comments are rule-based suggestions generated directly from the biomechanical deviations recorded above. This does not constitute a clinical medical diagnosis.

- Left/right movement asymmetry was detected (deviation: 0.80). Focus on moving both sides symmetrically.

---

## 6. Limitations & Disclaimer
1. **No Clinical Validation:** The Movement Quality Score and error ranking are biomechanical indices for research and reference only.
2. **Camera Calibration:** Tracking quality depends heavily on lighting, clothing, and occlusion. High uncertainty flags should prompt a retry.
