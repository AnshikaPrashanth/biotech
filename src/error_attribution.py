import numpy as np
from typing import Dict, List, Tuple, Any, Optional

from src.graph import INTELLIREHAB_JOINTS
from src.calibration import ANGLE_TRIPLETS, compute_joint_angles, smooth_angle_signal, interpolate_1d_curve

# Bilateral counterpart joint mapping for symmetry calculations
BILATERAL_PAIRS = {
    'ShoulderLeft': 'ShoulderRight',
    'ElbowLeft': 'ElbowRight',
    'WristLeft': 'WristRight',
    'HandLeft': 'HandRight',
    'HipLeft': 'HipRight',
    'KneeLeft': 'KneeRight',
    'AnkleLeft': 'AnkleRight',
    'FootLeft': 'FootRight',
    'HandTipLeft': 'HandTipRight',
    'ThumbLeft': 'ThumbRight'
}

# Map from angle name to its main vertex joint
ANGLE_TO_VERTEX = {
    'elbow_left': 'ElbowLeft',
    'elbow_right': 'ElbowRight',
    'knee_left': 'KneeLeft',
    'knee_right': 'KneeRight',
    'hip_left': 'HipLeft',
    'hip_right': 'HipRight',
    'shoulder_left': 'ShoulderLeft',
    'shoulder_right': 'ShoulderRight'
}

def calculate_derivatives(sequence: np.ndarray, dt: float = 0.033) -> Tuple[np.ndarray, np.ndarray]:
    """Computes first and second derivatives of joint positions (velocity and acceleration)."""
    # sequence shape: (T, 25, 3)
    velocity = np.diff(sequence, axis=0) / dt  # Shape: (T-1, 25, 3)
    acceleration = np.diff(velocity, axis=0) / dt  # Shape: (T-2, 25, 3)
    
    # Pad to maintain length T
    pad_vel = np.zeros((sequence.shape[0], 25, 3), dtype=np.float32)
    pad_vel[1:] = velocity
    pad_vel[0] = velocity[0] if len(velocity) > 0 else 0
    
    pad_acc = np.zeros((sequence.shape[0], 25, 3), dtype=np.float32)
    pad_acc[2:] = acceleration
    pad_acc[:2] = acceleration[0] if len(acceleration) > 0 else 0
    
    return pad_vel, pad_acc

def calculate_symmetry_deviations(sequence: np.ndarray) -> Dict[str, float]:
    """Computes asymmetry deviation for each bilateral joint pair across the sequence."""
    deviations = {}
    joint_map = {name: idx for idx, name in enumerate(INTELLIREHAB_JOINTS)}
    
    for left_name, right_name in BILATERAL_PAIRS.items():
        left_idx = joint_map[left_name]
        right_idx = joint_map[right_name]
        
        # Anatomical symmetry: reflect left X coordinate and compare to right
        left_coords = sequence[:, left_idx]
        right_coords = sequence[:, right_idx]
        
        # Difference vector with X-reflection (assuming centered at SpineBase):
        diff_x = left_coords[:, 0] + right_coords[:, 0]
        diff_y = left_coords[:, 1] - right_coords[:, 1]
        diff_z = left_coords[:, 2] - right_coords[:, 2]
        
        asymmetry = np.sqrt(diff_x**2 + diff_y**2 + diff_z**2)
        mean_asymmetry = float(np.mean(asymmetry))
        
        # Normalize asymmetry deviation (0.1 meters or more represents full asymmetry)
        norm_val = min(1.0, mean_asymmetry / 0.1)
        deviations[left_name] = norm_val
        deviations[right_name] = norm_val
        
    # Central joints have 0 asymmetry deviation
    for name in INTELLIREHAB_JOINTS:
        if name not in deviations:
            deviations[name] = 0.0
            
    return deviations

class BiomechanicalErrorEngine:
    def __init__(self, config: Dict[str, Any]):
        # Load weights and configurations
        bio_cfg = config.get('biomechanical', {})
        self.weights = bio_cfg.get('weights', {
            'w_rom': 0.3,
            'w_sym': 0.2,
            'w_vel': 0.2,
            'w_acc': 0.1,
            'w_attention': 0.2
        })
        
        # Ensure weights sum to 1
        total_w = sum(self.weights.values())
        if not np.isclose(total_w, 1.0):
            self.weights = {k: v / total_w for k, v in self.weights.items()}
            
        self.mqs_weights = bio_cfg.get('quality_score', {
            'w_rom': 0.4,
            'w_sym': 0.3,
            'w_temporal': 0.1,
            'w_bio': 0.2
        })
        total_mqs_w = sum(self.mqs_weights.values())
        if not np.isclose(total_mqs_w, 1.0):
            self.mqs_weights = {k: v / total_mqs_w for k, v in self.mqs_weights.items()}

    def compute_errors(
        self,
        sequence: np.ndarray,
        attention_map: Dict[str, float],
        calibration_results: Optional[Dict[str, Any]] = None,
        baseline_template: Optional[np.ndarray] = None
    ) -> Dict[str, Any]:
        """Calculates joint-level error scores and ranks them."""
        # 1. Derivatives (Velocity and Acceleration)
        velocity, acceleration = calculate_derivatives(sequence)
        
        # Average magnitude across time
        vel_mag = np.linalg.norm(velocity, axis=2).mean(axis=0)  # (25,)
        acc_mag = np.linalg.norm(acceleration, axis=2).mean(axis=0)  # (25,)
        
        # 2. Symmetry
        symmetry_map = calculate_symmetry_deviations(sequence)
        
        # 3. Position and velocity deviations from template if available
        pos_dev_map = {name: 0.0 for name in INTELLIREHAB_JOINTS}
        vel_dev_map = {name: 0.0 for name in INTELLIREHAB_JOINTS}
        acc_dev_map = {name: 0.0 for name in INTELLIREHAB_JOINTS}
        
        if baseline_template is not None:
            # Interpolate template and sequence to same length for direct frame comparison
            t_len = baseline_template.shape[0]
            s_len = sequence.shape[0]
            
            # Simple frame-wise linear interpolation matching
            indices = np.linspace(0, s_len - 1, t_len).astype(int)
            seq_matched = sequence[indices]
            
            ref_vel, ref_acc = calculate_derivatives(baseline_template)
            seq_vel, seq_acc = calculate_derivatives(seq_matched)
            
            for j_idx, name in enumerate(INTELLIREHAB_JOINTS):
                # Position deviation
                p_dev = np.linalg.norm(seq_matched[:, j_idx] - baseline_template[:, j_idx], axis=1).mean()
                pos_dev_map[name] = min(1.0, float(p_dev) / 0.2)  # Scale against 20cm threshold
                
                # Velocity deviation
                v_dev = np.linalg.norm(seq_vel[:, j_idx] - ref_vel[:, j_idx], axis=1).mean()
                vel_dev_map[name] = min(1.0, float(v_dev) / 1.0)
                
                # Acceleration deviation
                a_dev = np.linalg.norm(seq_acc[:, j_idx] - ref_acc[:, j_idx], axis=1).mean()
                acc_dev_map[name] = min(1.0, float(a_dev) / 3.0)
                
        # 4. ROM deviations
        rom_dev_map = {name: 0.0 for name in INTELLIREHAB_JOINTS}
        if calibration_results and 'joint_errors' in calibration_results:
            # calibration_results['joint_errors'] maps angle -> DTW distance
            for angle_name, dtw_err in calibration_results['joint_errors'].items():
                vertex_joint = ANGLE_TO_VERTEX.get(angle_name)
                if vertex_joint:
                    # Normalize by baseline tolerance if available
                    tol = 15.0  # Fallback tolerance of 15 degrees
                    if 'baselines' in calibration_results and 'tolerance' in calibration_results:
                        tol = calibration_results['tolerance'].get(angle_name, 15.0)
                    rom_dev_map[vertex_joint] = min(1.0, float(dtw_err) / (tol + 1e-6))
                    
        # Max attention for normalization
        max_attn = max(attention_map.values()) if attention_map else 1.0
        
        # 5. Combine component scores into joint-level Error Scores
        joint_error_details = {}
        overall_joint_scores = {}
        
        for name in INTELLIREHAB_JOINTS:
            rom_err = rom_dev_map.get(name, 0.0)
            sym_err = symmetry_map.get(name, 0.0)
            vel_err = vel_dev_map.get(name, 0.0)
            acc_err = acc_dev_map.get(name, 0.0)
            
            # Attention component (normalized)
            attn_val = attention_map.get(name, 0.0)
            norm_attn = attn_val / (max_attn + 1e-6)
            
            # Joint error score formulation
            score = (
                self.weights['w_rom'] * rom_err +
                self.weights['w_sym'] * sym_err +
                self.weights['w_vel'] * vel_err +
                self.weights['w_acc'] * acc_err +
                self.weights['w_attention'] * norm_attn
            )
            
            overall_joint_scores[name] = float(score)
            
            # Store details for reporting
            joint_error_details[name] = {
                "rom_deviation": rom_err,
                "symmetry_deviation": sym_err,
                "velocity_deviation": vel_err,
                "acceleration_deviation": acc_err,
                "attention_contribution": attn_val,
                "error_score": float(score)
            }
            
        # Rank joints by score
        top_error_joints = sorted(overall_joint_scores.items(), key=lambda x: x[1], reverse=True)
        
        return {
            "overall_joint_scores": overall_joint_scores,
            "joint_error_details": joint_error_details,
            "top_error_joints": top_error_joints
        }
        
    def compute_movement_quality_score(
        self,
        sequence: np.ndarray,
        calibration_results: Optional[Dict[str, Any]] = None,
        baseline_template: Optional[np.ndarray] = None
    ) -> Tuple[float, Dict[str, float]]:
        """Calculates a continuous Movement Quality Score (0 to 100)."""
        # A. ROM Conformity Score
        if calibration_results and ('joint_errors' in calibration_results or 'confidence' in calibration_results):
            # Base it on mean joint confidences from calibration evaluation
            s_rom = float(calibration_results.get('rom_confidence', calibration_results.get('confidence', 0.80)))
        else:
            s_rom = 0.80  # Default fallback if no calibration is loaded
            
        # B. Symmetry Score
        sym_deviations = calculate_symmetry_deviations(sequence)
        s_sym = 1.0 - float(np.mean(list(sym_deviations.values())))
        
        # C. Temporal Consistency Score
        # Look at standard deviation of joint velocities over time (jitter/smoothness)
        vel, _ = calculate_derivatives(sequence)
        vel_std = np.linalg.norm(vel, axis=2).std(axis=0).mean()
        # High jitter (velocity standard deviation > 1.5) lowers consistency
        s_temporal = float(np.clip(1.0 - (vel_std / 1.5), 0.0, 1.0))
        
        # D. Biomechanical Quality Score
        if baseline_template is not None:
            # Mean position deviation across all joints
            t_len = baseline_template.shape[0]
            indices = np.linspace(0, sequence.shape[0] - 1, t_len).astype(int)
            seq_matched = sequence[indices]
            pos_diff = np.linalg.norm(seq_matched - baseline_template, axis=2).mean()
            s_bio = float(np.clip(1.0 - (pos_diff / 0.3), 0.0, 1.0))
        else:
            s_bio = 0.80
            
        # Weighted combination
        mqs = 100.0 * (
            self.mqs_weights['w_rom'] * s_rom +
            self.mqs_weights['w_sym'] * s_sym +
            self.mqs_weights['w_temporal'] * s_temporal +
            self.mqs_weights['w_bio'] * s_bio
        )
        
        components = {
            "rom": float(s_rom * 100),
            "symmetry": float(s_sym * 100),
            "temporal": float(s_temporal * 100),
            "biomechanical": float(s_bio * 100)
        }
        
        return float(mqs), components
