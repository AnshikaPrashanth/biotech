# Rehab AI Assessment Report
**Date:** N/A
**Patient ID:** tmph4jvalhq | **Exercise:** 0.07592836 | **Source:** txt

---

## 1. Executive Summary

| Metric | Value | Reference / Status |
| :--- | :--- | :--- |
| **Prediction Verdict** | Compensated | 80.95% Confidence |
| **Movement Quality Score** | 88.0 / 100 | Research Movement-Quality Index |
| **Uncertainty Status** | Compensated | Threshold: 0.70 |
| **Repetitions Detected** | 1 | Trajectory: Stable |

---

## 2. Model Inference Output
> [!NOTE]
> This section displays the model's raw classification and attention weights. These represent statistical patterns detected by the neural network.

- **Class Probabilities:**
  - Healthy (0): 0.1905
  - Compensated (1): 0.8095
- **Confidence Status:** 0.8095 (Sufficient)

### Spatial Joint Attention (Top 5 joints)
- **SpineShoulder**: 0.8000
- **SpineBase**: 0.7500
- **WristLeft**: 0.7500
- **WristRight**: 0.7500
- **SpineMid**: 0.6667

---

## 3. Biomechanical Measurements
> [!IMPORTANT]
> These measurements represent actual physical calculations derived from the joint trajectories, completely independent of the classification model.

### Movement Quality Score Breakdown
- **ROM Conformity:** 80.0%
- **Bilateral Symmetry:** 100.0%
- **Temporal Consistency:** 100.0%
- **Biomechanical Conformity:** 80.0%

### Ranked Joint Deviations (Top 5 Error Scores)
Each joint score combines ROM deviation, bilateral asymmetry, velocity deviation, and model attention weight.
1. **SpineShoulder** — Score: 0.20
2. **SpineBase** — Score: 0.19
3. **WristLeft** — Score: 0.19
4. **WristRight** — Score: 0.19
5. **SpineMid** — Score: 0.17

For these joints, detailed features are:
| Joint Name | ROM Deviation | Asymmetry | Velocity Dev | overall score |
| :--- | :---: | :---: | :---: | :---: |
| SpineShoulder | 0.00 | 0.00 | 0.00 | 0.20 |
| SpineBase | 0.00 | 0.00 | 0.00 | 0.19 |
| WristLeft | 0.00 | 0.00 | 0.00 | 0.19 |
| WristRight | 0.00 | 0.00 | 0.00 | 0.19 |
| SpineMid | 0.00 | 0.00 | 0.00 | 0.17 |

---

## 4. Repetition Analysis
- **Repetitions segmented:** 1
- **Quality progression slope:** 0.000 per repetition
- **Fatigue / Degradation status:** **Stable**

---

## 5. Interpretive Feedback & Recommendations
> [!TIP]
> **AI-Assisted Exercise Feedback:** The following comments are rule-based suggestions generated directly from the biomechanical deviations recorded above. This does not constitute a clinical medical diagnosis.

- Excellent execution! Your range of motion and symmetry conform well to your personalized baseline.

---

## 6. Limitations & Disclaimer
1. **No Clinical Validation:** The Movement Quality Score and error ranking are biomechanical indices for research and reference only.
2. **Camera Calibration:** Tracking quality depends heavily on lighting, clothing, and occlusion. High uncertainty flags should prompt a retry.
