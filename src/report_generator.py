import os
import json
from pathlib import Path
from typing import Dict, Any, List

class RehabReportGenerator:
    @staticmethod
    def generate_json_report(analysis_results: Dict[str, Any], output_path: str) -> str:
        """Saves assessment results as a formatted JSON document."""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(analysis_results, f, indent=2)
        return output_path

    @staticmethod
    def generate_markdown_report(analysis_results: Dict[str, Any], output_path: str) -> str:
        """Saves assessment results as a structured Markdown document."""
        meta = analysis_results["metadata"]
        pred = analysis_results["prediction"]
        unc = analysis_results["uncertainty"]
        mqs = analysis_results["movement_quality"]
        rom = analysis_results["rom_analysis"]
        err = analysis_results["error_attribution"]
        rep = analysis_results["repetitions"]
        feedback = analysis_results["feedback"]

        md = f"""# Rehab AI Assessment Report
**Date:** {meta.get('timestamp', 'N/A')}
**Patient ID:** {meta.get('subject_id', 'unknown')} | **Exercise:** {meta.get('exercise_type', 'stand')} | **Source:** {meta.get('source_type', 'txt')}

---

## 1. Executive Summary

| Metric | Value | Reference / Status |
| :--- | :--- | :--- |
| **Prediction Verdict** | {pred['verdict']} | {pred['confidence']:.2%} Confidence |
| **Movement Quality Score** | {mqs['score']:.1f} / 100 | Research Movement-Quality Index |
| **Uncertainty Status** | {unc['decision_status']} | Threshold: {unc['confidence_threshold']:.2f} |
| **Repetitions Detected** | {rep['count']} | Trajectory: {rep['trajectory']} |

---

## 2. Model Inference Output
> [!NOTE]
> This section displays the model's raw classification and attention weights. These represent statistical patterns detected by the neural network.

- **Class Probabilities:**
  - Healthy (0): {pred['probabilities'][0]:.4f}
  - Compensated (1): {pred['probabilities'][1]:.4f}
- **Confidence Status:** {pred['confidence']:.4f} ({'Sufficient' if unc['uncertainty_score'] < 0.3 else 'Low Confidence / Review Recommended'})

### Spatial Joint Attention (Top 5 joints)
{chr(10).join([f"- **{joint}**: {val:.4f}" for joint, val in sorted(analysis_results['attention']['joint_attention'].items(), key=lambda x: x[1], reverse=True)[:5]])}

---

## 3. Biomechanical Measurements
> [!IMPORTANT]
> These measurements represent actual physical calculations derived from the joint trajectories, completely independent of the classification model.

### Movement Quality Score Breakdown
- **ROM Conformity:** {mqs['components']['rom']:.1f}%
- **Bilateral Symmetry:** {mqs['components']['symmetry']:.1f}%
- **Temporal Consistency:** {mqs['components']['temporal']:.1f}%
- **Biomechanical Conformity:** {mqs['components']['biomechanical']:.1f}%

### Ranked Joint Deviations (Top 5 Error Scores)
Each joint score combines ROM deviation, bilateral asymmetry, velocity deviation, and model attention weight.
{chr(10).join([f"{idx+1}. **{joint}** — Score: {score:.2f}" for idx, (joint, score) in enumerate(err['top_error_joints'][:5])])}

For these joints, detailed features are:
| Joint Name | ROM Deviation | Asymmetry | Velocity Dev | overall score |
| :--- | :---: | :---: | :---: | :---: |
{chr(10).join([f"| {joint} | {err['joint_error_details'][joint]['rom_deviation']:.2f} | {err['joint_error_details'][joint]['symmetry_deviation']:.2f} | {err['joint_error_details'][joint]['velocity_deviation']:.2f} | {err['joint_error_details'][joint]['error_score']:.2f} |" for joint, _ in err['top_error_joints'][:5]])}

---

## 4. Repetition Analysis
- **Repetitions segmented:** {rep['count']}
- **Quality progression slope:** {rep['degradation_slope']:.3f} per repetition
- **Fatigue / Degradation status:** **{rep['trajectory']}**

---

## 5. Interpretive Feedback & Recommendations
> [!TIP]
> **AI-Assisted Exercise Feedback:** The following comments are rule-based suggestions generated directly from the biomechanical deviations recorded above. This does not constitute a clinical medical diagnosis.

{chr(10).join([f"- {comment}" for comment in feedback])}

---

## 6. Limitations & Disclaimer
1. **No Clinical Validation:** The Movement Quality Score and error ranking are biomechanical indices for research and reference only.
2. **Camera Calibration:** Tracking quality depends heavily on lighting, clothing, and occlusion. High uncertainty flags should prompt a retry.
"""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(md)
        return output_path

    @staticmethod
    def generate_html_report(analysis_results: Dict[str, Any], output_path: str) -> str:
        """Saves assessment results as a clean HTML file."""
        meta = analysis_results["metadata"]
        pred = analysis_results["prediction"]
        mqs = analysis_results["movement_quality"]
        feedback = analysis_results["feedback"]

        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Rehab AI Report - Patient {meta.get('subject_id')}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; max-width: 800px; margin: 40px auto; padding: 0 20px; color: #333; }}
        h1, h2 {{ color: #1E3A8A; border-bottom: 1px solid #E5E7EB; padding-bottom: 8px; }}
        .metric-card {{ background: #F3F4F6; border-left: 4px solid #3B82F6; padding: 15px; border-radius: 4px; margin-bottom: 20px; }}
        .alert {{ background: #FEF3C7; border: 1px solid #F59E0B; padding: 12px; border-radius: 4px; font-size: 0.9em; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ padding: 10px; border: 1px solid #E5E7EB; text-align: left; }}
        th {{ background-color: #F9FAFB; }}
        .feedback {{ background: #ECFDF5; border-left: 4px solid #10B981; padding: 15px; border-radius: 4px; }}
    </style>
</head>
<body>
    <h1>🧬 Rehabilitation Assessment Report</h1>
    <p><strong>Patient ID:</strong> {meta.get('subject_id')} | <strong>Exercise:</strong> {meta.get('exercise_type')} | <strong>Source:</strong> {meta.get('source_type')}</p>
    
    <div class="metric-card">
        <h3>Verdict: {pred['verdict']} ({pred['confidence']:.2%} confidence)</h3>
        <h3>Movement Quality Score: {mqs['score']:.1f} / 100</h3>
    </div>
    
    <h2>AI-Assisted Exercise Feedback</h2>
    <div class="feedback">
        <ul>
            {"".join([f"<li>{f}</li>" for f in feedback])}
        </ul>
    </div>
    
    <div class="alert" style="margin-top: 40px;">
        <strong>Disclaimer:</strong> This is an engineering/research quality score and is NOT a clinically validated medical diagnosis.
    </div>
</body>
</html>
"""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        return output_path
