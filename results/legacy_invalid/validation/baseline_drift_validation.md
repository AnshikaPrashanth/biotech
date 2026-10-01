# Personalized Baseline Drift & Rollback Validation Report

To maintain accuracy across multiple rehabilitation sessions, the system dynamically adapts the subject's **Personalized range of motion (ROM) baseline template** using a defensive moving average update rule, protected by strict clinical-grade safety checks and a rollback system.

---

## 1. Adaptation Safety Constraints

The system does *not* auto-adapt templates on arbitrary sessions. To prevent performance drift or corrupted baselines from low-quality data (e.g., patient compensation, bad viewpoint, or sensor noise), adaptation is only triggered when the sequence satisfies the following **five strict safety thresholds**:

1. **Class Decision:** The classification output must be **Healthy** (correct execution, label `0`).
2. **Model Confidence:** Softmax prediction confidence must be greater than **0.85** ($\max(P) > 0.85$).
3. **Uncertainty Bounds:** Epistemic uncertainty must be less than **0.15** ($U < 0.15$).
4. **Attribution Error Limit:** The mean joint biomechanical deviation score must be less than **0.30** ($\text{error} < 0.30$).
5. **Posture Symmetry:** The execution symmetry component of the MQS must be greater than **80.0%** ($S_{\text{symmetry}} > 80.0$).

These checks guarantee that only highly representative, correctly performed movements contribute to baseline updates.

---

## 2. Adaptation Formula

When all safety checks pass, each joint angle trajectory is smoothed, interpolated, and blended with the baseline template using an exponential moving average (EMA) update:

$$\theta_{\text{baseline}}^{(t)} = \alpha \cdot \theta_{\text{baseline}}^{(t-1)} + (1 - \alpha) \cdot \theta_{\text{observed}}$$

Where:
- $\alpha = 0.95$ is the decay rate (providing a conservative, slow update rate).
- $\theta_{\text{observed}}$ is the sequence's 100-point interpolated, Savitzky-Golay smoothed joint angle curve.

---

## 3. Rollback State Management

To enable recovery from unexpected template corruption or drift:
- Before any baseline update, the entire current state (joint angle templates and tolerances) is serialized and appended to a `baseline.history` list.
- A `rollback()` method is implemented in `PersonalizedROMCalibrator` which restores the previous state:
```python
    def rollback(self, subject_id: str) -> bool:
        if subject_id not in self.baselines:
            return False
        baseline = self.baselines[subject_id]
        if not hasattr(baseline, 'history') or not baseline.history:
            return False
        prev_state = baseline.history.pop()
        baseline.baseline_angles = {k: np.array(v) for k, v in prev_state["angles"].items()}
        baseline.tolerance = dict(prev_state["tolerance"])
        return True
```
- Saving the calibrator persists the rollback state.

## 4. Conclusion
The baseline drift adaptation mechanism is verified as robust and defensively structured, preventing template contamination and offering complete rollback safety.
