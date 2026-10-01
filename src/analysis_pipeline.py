import os
import json
from pathlib import Path
import numpy as np
import torch
from typing import Dict, Any, List, Tuple, Optional

from config import TRAINING_CONFIG, DB_PATH, GLOBAL_CONFIG
from src.model import stgat_from_config, STGAT
from src.calibration import PersonalizedROMCalibrator, segment_repetitions, compute_joint_angles, smooth_angle_signal, interpolate_1d_curve
from src.error_attribution import BiomechanicalErrorEngine
from src.uncertainty import confidence_based_abstention
from src.feedback import generate_clinical_feedback
from src.database import SQLiteSessionDB

# Helper to run model prediction and retrieve attention maps
def predict_raw_sequence(model: STGAT, sequence: np.ndarray, device: torch.device) -> Dict[str, Any]:
    """Runs a 3D skeleton sequence through ST-GAT and maps attention weights to joints."""
    model.eval()
    tensor = torch.from_numpy(sequence[None, ...]).float().to(device)
    
    with torch.no_grad():
        outputs = model(tensor)
        
    logits = outputs['logits'][0].cpu().numpy()
    probs = outputs['probabilities'][0].cpu().numpy()
    pred_class = int(np.argmax(logits))
    confidence = float(probs[pred_class])
    
    joint_attn = outputs['joint_attention'][0].cpu().numpy()
    frame_attn = outputs['frame_attention'][0].cpu().numpy()
    
    from src.graph import INTELLIREHAB_JOINTS
    joint_attention_map = {
        INTELLIREHAB_JOINTS[i]: float(joint_attn[i]) 
        for i in range(len(INTELLIREHAB_JOINTS))
    }
    
    return {
        'class_idx': pred_class,
        'probabilities': probs.tolist(),
        'confidence': confidence,
        'joint_attention': joint_attention_map,
        'frame_attention': frame_attn.tolist()
    }

def analyze_sequence(
    sequence: np.ndarray,
    metadata: Dict[str, Any],
    model: Optional[STGAT] = None,
    calibrator: Optional[PersonalizedROMCalibrator] = None,
    db: Optional[SQLiteSessionDB] = None,
    device: Optional[torch.device] = None,
    config_dict: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Unified assessment pipeline executing predictions, ROM, error attribution,
    quality scoring, uncertainty tracking, repetitions segmentation, and feedback generation.
    """
    if device is None:
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
    if config_dict is None:
        config_dict = GLOBAL_CONFIG
        
    subject_id = metadata.get("subject_id", "unknown")
    exercise_type = metadata.get("exercise_type", "stand")
    source_type = metadata.get("source_type", "txt")
    
    # 1. Load model if not provided
    if model is None:
        model_config = {
            'hidden_dim': TRAINING_CONFIG['hidden_dim'],
            'heads': TRAINING_CONFIG['heads'],
            'dropout': 0.0
        }
        model = stgat_from_config(model_config).to(device)
        model_path = Path("checkpoints/best_model.pt")
        if model_path.exists():
            checkpoint = torch.load(model_path, map_location=device)
            state_dict = checkpoint.get('model_state', checkpoint)
            model.load_state_dict(state_dict, strict=False)
            
    # 2. Load calibrator if not provided
    if calibrator is None:
        baseline_path = "baselines/rom_baselines.json"
        calibrator = PersonalizedROMCalibrator(baseline_path=baseline_path if os.path.exists(baseline_path) else None)
        
    # 3. Load DB if not provided
    if db is None:
        db = SQLiteSessionDB(str(DB_PATH))
        
    # 4. ST-GAT Model Prediction
    # Ensure sequence length matches model expectations by cropping/padding
    seq_len = sequence.shape[0]
    target_len = TRAINING_CONFIG.get('sequence_length', 64)
    if seq_len > target_len:
        # Center crop
        start = (seq_len - target_len) // 2
        model_seq = sequence[start:start + target_len]
    elif seq_len < target_len:
        # Pad with last frame
        model_seq = np.zeros((target_len, 25, 3), dtype=np.float32)
        model_seq[:seq_len] = sequence
        model_seq[seq_len:] = sequence[-1:]
    else:
        model_seq = sequence
        
    pred_results = predict_raw_sequence(model, model_seq, device)
    probs = np.array(pred_results['probabilities'])
    
    # 5. Uncertainty / Abstention
    thresh = config_dict.get('uncertainty', {}).get('confidence_threshold', 0.70)
    pred_class, decision_status, confidence, uncertainty = confidence_based_abstention(probs, threshold=thresh)
    
    # 6. ROM Baseline calibration
    calibration_eval = {}
    baseline_template = None
    if subject_id in calibrator.baselines:
        calibration_eval = calibrator.evaluate(subject_id, sequence)
        # Reconstruct baseline template sequence for error attribution reference
        # Average baseline angles over 100 points
        baseline = calibrator.baselines[subject_id]
        # We can pass baseline angles as reference curves
        
    # 7. Biomechanical Error Attribution
    err_engine = BiomechanicalErrorEngine(config_dict)
    error_attribution = err_engine.compute_errors(
        sequence=sequence,
        attention_map=pred_results['joint_attention'],
        calibration_results=calibration_eval
    )
    
    # 8. Movement Quality Score
    mqs, mqs_components = err_engine.compute_movement_quality_score(
        sequence=sequence,
        calibration_results=calibration_eval
    )
    
    # 9. Repetition-Level Analysis
    reps = segment_repetitions(sequence)
    rep_details = []
    
    for r_idx, rep_seq in enumerate(reps):
        if rep_seq.shape[0] < 5:
            continue
        # Run local prediction
        rep_pred = predict_raw_sequence(model, rep_seq, device)
        rep_probs = np.array(rep_pred['probabilities'])
        r_class, r_status, r_conf, r_unc = confidence_based_abstention(rep_probs, threshold=thresh)
        
        # Local ROM check
        r_cal = {}
        if subject_id in calibrator.baselines:
            r_cal = calibrator.evaluate(subject_id, rep_seq)
            
        r_errs = err_engine.compute_errors(rep_seq, rep_pred['joint_attention'], r_cal)
        r_mqs, r_mqs_comp = err_engine.compute_movement_quality_score(rep_seq, r_cal)
        
        rep_details.append({
            "rep_index": r_idx + 1,
            "prediction": r_status,
            "confidence": r_conf,
            "movement_quality_score": r_mqs,
            "rom_deviation": float(np.mean([x[1] for x in r_cal.get('top_error_joints', [])])) if r_cal else 0.0,
            "top_error_joints": r_errs['top_error_joints'][:3]
        })
        
    # Quality trajectory trend slope
    degradation_slope = 0.0
    trajectory = "Stable"
    if len(rep_details) >= 2:
        x_vals = np.arange(len(rep_details))
        y_vals = np.array([r["movement_quality_score"] for r in rep_details])
        degradation_slope = float(np.polyfit(x_vals, y_vals, 1)[0])
        
        if degradation_slope < -1.0:
            trajectory = "Deteriorating"
        elif degradation_slope > 1.0:
            trajectory = "Improving"
            
    # 10. Personalized Baseline Drift (Optional adaptation)
    drift_enabled = config_dict.get('calibration', {}).get('baseline_drift_enabled', True)
    alpha = config_dict.get('calibration', {}).get('baseline_drift_alpha', 0.95)
    baseline_updated = False
    
    if drift_enabled and subject_id in calibrator.baselines:
        # Strict update conditions:
        # - Healthy prediction
        # - High confidence
        # - Low uncertainty
        # - Low biomechanical error
        # - High symmetry (mqs symmetry > 80)
        overall_err = np.mean(list(error_attribution['overall_joint_scores'].values()))
        if (
            decision_status == "Healthy" and 
            confidence > 0.85 and 
            uncertainty < 0.15 and 
            overall_err < 0.30 and
            mqs_components['symmetry'] > 80.0
        ):
            # Update baseline using conservative update rule
            baseline = calibrator.baselines[subject_id]
            rep_angles = compute_joint_angles(sequence)
            
            # Store historical version before update (roll-back mechanism)
            if not hasattr(baseline, 'history'):
                baseline.history = []
            baseline.history.append({
                "timestamp": time.time(),
                "angles": {k: v.tolist() if isinstance(v, np.ndarray) else v for k, v in baseline.baseline_angles.items()},
                "tolerance": dict(baseline.tolerance)
            })

            # Smooth and interpolate observed curves
            for angle_name in baseline.baseline_angles:
                if angle_name in rep_angles:
                    smoothed = smooth_angle_signal(rep_angles[angle_name])
                    observed_curve = interpolate_1d_curve(smoothed, target_length=100)
                    
                    # update baseline template curve
                    baseline.baseline_angles[angle_name] = alpha * baseline.baseline_angles[angle_name] + (1 - alpha) * observed_curve
                    
            calibrator.save("baselines/rom_baselines.json")
            baseline_updated = True
            
    # 11. AI-Assisted Clinical Feedback
    feedback = generate_clinical_feedback(
        sequence=sequence,
        error_attribution=error_attribution,
        calibration_results=calibration_eval,
        decision_status=decision_status
    )
    
    # 12. Save logs to SQLite Database
    rom_devs = calibration_eval.get('joint_errors', {}) if calibration_eval else None
    top_errs_serialized = json.dumps(error_attribution['top_error_joints'][:5])
    rep_stats_serialized = json.dumps({
        "reps": rep_details,
        "degradation_slope": degradation_slope,
        "trajectory": trajectory
    })
    
    # Check if database has updated columns, if not run migration
    db.log_session(
        subject_id=subject_id,
        exercise_type=exercise_type,
        confidence=confidence,
        verdict=decision_status,
        attention_map=pred_results['joint_attention'],
        rom_deviation=rom_devs,
        session_duration=float(sequence.shape[0] / 30.0),
        notes=f"Analysis pipeline source: {source_type}",
        movement_quality=mqs,
        uncertainty=uncertainty,
        rom_score=calibration_eval.get('confidence', 0.0) if calibration_eval else 0.0,
        symmetry_score=mqs_components['symmetry'],
        top_error_joints=error_attribution['top_error_joints'],
        repetition_stats={
            "count": len(reps),
            "reps_detail": rep_details,
            "degradation_slope": degradation_slope,
            "trajectory": trajectory
        }
    )
    
    # Assemble comprehensive report
    return {
        "metadata": {
            "subject_id": subject_id,
            "exercise_type": exercise_type,
            "source_type": source_type,
            "frame_count": sequence.shape[0],
            "duration_seconds": float(sequence.shape[0] / 30.0)
        },
        "prediction": {
            "verdict": decision_status,
            "confidence": confidence,
            "probabilities": pred_results['probabilities'],
            "class_idx": pred_class
        },
        "uncertainty": {
            "uncertainty_score": uncertainty,
            "decision_status": decision_status,
            "confidence_threshold": thresh
        },
        "movement_quality": {
            "score": mqs,
            "components": mqs_components
        },
        "rom_analysis": {
            "tolerance_scale": calibrator.tolerance_scale,
            "calibrated_deviations": rom_devs,
            "overall_rom_confidence": calibration_eval.get('confidence', 0.0) if calibration_eval else 0.0
        },
        "error_attribution": {
            "overall_joint_scores": error_attribution['overall_joint_scores'],
            "joint_error_details": error_attribution['joint_error_details'],
            "top_error_joints": error_attribution['top_error_joints']
        },
        "attention": {
            "joint_attention": pred_results['joint_attention'],
            "frame_attention": pred_results['frame_attention']
        },
        "repetitions": {
            "count": len(reps),
            "reps_detail": rep_details,
            "degradation_slope": degradation_slope,
            "trajectory": trajectory
        },
        "baseline_adaptation": {
            "drift_enabled": drift_enabled,
            "baseline_updated": baseline_updated
        },
        "feedback": feedback
    }
