import numpy as np
from typing import List, Dict, Any, Optional
from src.graph import INTELLIREHAB_JOINTS

def calculate_trunk_lean(sequence: np.ndarray) -> float:
    """Calculates the average trunk lean angle (in degrees) relative to the vertical Y-axis."""
    # Joint indices: SpineBase=0, SpineShoulder=20
    # sequence shape: (T, 25, 3)
    spine_base = sequence[:, 0]
    spine_shoulder = sequence[:, 20]
    
    trunk_vectors = spine_shoulder - spine_base  # (T, 3)
    
    # Calculate angle with vertical [0, 1, 0]
    y_components = trunk_vectors[:, 1]
    magnitudes = np.linalg.norm(trunk_vectors, axis=1)
    
    # Avoid division by zero
    valid = magnitudes > 1e-6
    if not valid.any():
        return 0.0
        
    cos_angles = np.clip(y_components[valid] / magnitudes[valid], -1.0, 1.0)
    lean_angles = np.degrees(np.arccos(cos_angles))
    
    return float(np.mean(lean_angles))

def generate_clinical_feedback(
    sequence: np.ndarray,
    error_attribution: Dict[str, Any],
    calibration_results: Optional[Dict[str, Any]] = None,
    decision_status: str = "Healthy"
) -> List[str]:
    """Generates AI-assisted exercise feedback grounded in actual biomechanical measurements."""
    feedback = []
    
    # 1. High Uncertainty check
    if decision_status == "Uncertain / Human Review":
        feedback.append("The movement could not be assessed reliably. Please repeat the movement under better lighting or camera placement.")
        return feedback
        
    # 2. Trunk Lean check
    lean_angle = calculate_trunk_lean(sequence)
    # Threshold for trunk lean: 15 degrees is standard for compensatory leaning
    if lean_angle > 15.0:
        feedback.append(f"Excessive trunk inclination of {lean_angle:.1f}° was detected. Try to maintain a more upright posture.")
        
    # 3. Left/Right Asymmetry check
    symmetry_scores = []
    for joint_name, details in error_attribution.get("joint_error_details", {}).items():
        symmetry_scores.append(details.get("symmetry_deviation", 0.0))
        
    mean_symmetry_err = np.mean(symmetry_scores) if symmetry_scores else 0.0
    if mean_symmetry_err > 0.15:
        feedback.append(f"Left/right movement asymmetry was detected (deviation: {mean_symmetry_err:.2f}). Focus on moving both sides symmetrically.")
        
    # 4. Joint-level ROM Deficits
    if calibration_results and 'joint_errors' in calibration_results:
        # Check for joints with high ROM error
        top_errors = calibration_results.get('top_errors', [])
        for angle_name, dtw_err in top_errors:
            # If error is greater than baseline tolerance, suggest correction
            tol = 15.0
            if 'baselines' in calibration_results and 'tolerance' in calibration_results:
                tol = calibration_results['tolerance'].get(angle_name, 15.0)
                
            if dtw_err > tol:
                angle_clean = angle_name.replace('_', ' ').title()
                feedback.append(f"Observed {angle_clean} ROM (deviation: {dtw_err:.1f}°) is below the personalized reference range. Attempt to elevate/extend fully.")
                
    # 5. Fallback positive feedback
    if not feedback:
        feedback.append("Excellent execution! Your range of motion and symmetry conform well to your personalized baseline.")
        
    return feedback
