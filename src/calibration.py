import json
from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np
from fastdtw import fastdtw
from scipy.signal import find_peaks, savgol_filter

# Target joints for ROM calculations
ANGLE_TRIPLETS = {
    'elbow_left': ('ShoulderLeft', 'ElbowLeft', 'WristLeft'),
    'elbow_right': ('ShoulderRight', 'ElbowRight', 'WristRight'),
    'knee_left': ('HipLeft', 'KneeLeft', 'AnkleLeft'),
    'knee_right': ('HipRight', 'KneeRight', 'AnkleRight'),
    'hip_left': ('SpineBase', 'HipLeft', 'KneeLeft'),
    'hip_right': ('SpineBase', 'HipRight', 'KneeRight'),
    'shoulder_left': ('SpineShoulder', 'ShoulderLeft', 'ElbowLeft'),
    'shoulder_right': ('SpineShoulder', 'ShoulderRight', 'ElbowRight'),
}

JOINT_INDEX = {
    'SpineBase': 0, 'SpineMid': 1, 'Neck': 2, 'Head': 3,
    'ShoulderLeft': 4, 'ElbowLeft': 5, 'WristLeft': 6, 'HandLeft': 7,
    'ShoulderRight': 8, 'ElbowRight': 9, 'WristRight': 10, 'HandRight': 11,
    'HipLeft': 12, 'KneeLeft': 13, 'AnkleLeft': 14, 'FootLeft': 15,
    'HipRight': 16, 'KneeRight': 17, 'AnkleRight': 18, 'FootRight': 19,
    'SpineShoulder': 20, 'HandTipLeft': 21, 'ThumbLeft': 22, 'HandTipRight': 23, 'ThumbRight': 24,
}

@dataclass
class ROMBaseline:
    baseline_angles: Dict[str, np.ndarray]
    tolerance: Dict[str, float]
    subject_id: str
    progression_score: float = 1.0

def compute_angle(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> float:
    """Calculates the angle (in degrees) formed by points a, b (vertex), and c."""
    ab = a - b
    cb = c - b
    numerator = np.dot(ab, cb)
    denominator = np.linalg.norm(ab) * np.linalg.norm(cb)
    if denominator < 1e-6:
        return 0.0
    cos_value = np.clip(numerator / denominator, -1.0, 1.0)
    return float(np.degrees(np.arccos(cos_value)))

def compute_joint_angles(sequence: np.ndarray) -> Dict[str, np.ndarray]:
    """Extracts joint angle trajectories for all configured triplets across a skeleton sequence."""
    angles: Dict[str, np.ndarray] = {}
    for angle_name, joints in ANGLE_TRIPLETS.items():
        a = sequence[:, JOINT_INDEX[joints[0]], :]
        b = sequence[:, JOINT_INDEX[joints[1]], :]
        c = sequence[:, JOINT_INDEX[joints[2]], :]
        angles[angle_name] = np.array(
            [compute_angle(a[i], b[i], c[i]) for i in range(sequence.shape[0])],
            dtype=np.float32,
        )
    return angles

def smooth_angle_signal(angles: np.ndarray, window_length: int = 9, polyorder: int = 2) -> np.ndarray:
    """Smooths a 1D angle signal using a Savitzky-Golay filter."""
    if angles.shape[0] < window_length:
        # Window size must be odd and less than signal length
        w_len = angles.shape[0]
        if w_len % 2 == 0:
            w_len -= 1
        if w_len < 3:
            return angles
        return savgol_filter(angles, window_length=w_len, polyorder=1, axis=0)
    return savgol_filter(angles, window_length=window_length, polyorder=polyorder, axis=0)

def interpolate_1d_curve(curve: np.ndarray, target_length: int = 100) -> np.ndarray:
    """Linearly interpolates a 1D curve to a fixed target length (for template matching)."""
    if len(curve) <= 1:
        return np.zeros((target_length,), dtype=np.float32)
    x = np.arange(len(curve))
    x_new = np.linspace(0, len(curve) - 1, target_length)
    return np.interp(x_new, x, curve).astype(np.float32)

def segment_repetitions(sequence: np.ndarray, min_peak_height: float = 10.0, min_peak_distance: int = 15) -> List[np.ndarray]:
    """Segments a continuous skeleton sequence into individual repetitions using joint angular changes."""
    angles = compute_joint_angles(sequence)
    if not angles:
        return [sequence]
    
    # Take mean amplitude of dynamic joints to locate repetition boundaries
    segment_scores = np.vstack(list(angles.values())).mean(axis=0)
    smoothed_scores = smooth_angle_signal(segment_scores)
    
    peaks, _ = find_peaks(np.abs(smoothed_scores), height=min_peak_height, distance=min_peak_distance)
    if len(peaks) < 2:
        return [sequence]
        
    repetitions = []
    starts = np.concatenate(([0], peaks))
    ends = np.concatenate((peaks, [sequence.shape[0]]))
    for start, end in zip(starts, ends):
        if end - start >= 5:
            repetitions.append(sequence[start:end])
    return repetitions

def align_repetition_1d(reference_curve: np.ndarray, query_curve: np.ndarray) -> float:
    """Computes normalized DTW distance between two 1D angle trajectories."""
    ref = np.squeeze(reference_curve)
    qry = np.squeeze(query_curve)
    
    distance, _ = fastdtw(ref, qry)
    # Normalize by sequence lengths to make it scale/length-independent
    return float(distance / max(len(ref) + len(qry), 1))

def align_repetition(reference: np.ndarray, query: np.ndarray) -> float:
    """Anatomically aligns two 3D skeleton sequences and returns the average joint-wise DTW distance."""
    ref_angles = compute_joint_angles(reference)
    qry_angles = compute_joint_angles(query)
    total_distance = 0.0
    common_keys = set(ref_angles.keys()).intersection(qry_angles.keys())
    for key in common_keys:
        total_distance += align_repetition_1d(ref_angles[key], qry_angles[key])
    return total_distance / max(len(common_keys), 1)

class PersonalizedROMCalibrator:
    """Adaptive calibration engine. Computes joint angle ranges of motion and templates from healthy repetitions."""

    def __init__(self, tolerance_scale: float = 1.0, baseline_path: Optional[str] = None):
        self.baselines: Dict[str, ROMBaseline] = {}
        self.tolerance_scale = tolerance_scale
        if baseline_path:
            self.load(baseline_path)

    def fit(self, subject_id: str, healthy_sequences: Sequence[np.ndarray]) -> ROMBaseline:
        """Fits baseline joint angle ranges of motion from a pool of healthy sequences."""
        candidate_segments: Dict[str, List[np.ndarray]] = {}
        for sequence in healthy_sequences:
            reps = segment_repetitions(sequence)
            for rep in reps:
                rep_angles = compute_joint_angles(rep)
                for angle_name, curve in rep_angles.items():
                    # Ignore flat or static trajectories (movement range less than 1.5 degrees)
                    if np.ptp(curve) < 1.5:
                        continue
                    smoothed = smooth_angle_signal(curve)
                    # Interpolate to 100 points to resolve varying repetition lengths
                    interpolated = interpolate_1d_curve(smoothed, target_length=100)
                    candidate_segments.setdefault(angle_name, []).append(interpolated)
                    
        baseline_angles: Dict[str, np.ndarray] = {}
        tolerance: Dict[str, float] = {}
        
        for angle_name, curves in candidate_segments.items():
            if not curves:
                continue
            stacked = np.stack(curves, axis=0)  # Shape: (num_repetitions, 100)
            mean_curve = np.mean(stacked, axis=0)
            std_val = float(np.std(stacked))
            
            baseline_angles[angle_name] = mean_curve
            # Compute adaptive threshold (std deviation scale + minimal safety boundary)
            tolerance[angle_name] = float(std_val * self.tolerance_scale + np.maximum(np.mean(np.abs(mean_curve)) * 0.05, 3.0))
            
        baseline = ROMBaseline(baseline_angles=baseline_angles, tolerance=tolerance, subject_id=subject_id)
        self.baselines[subject_id] = baseline
        return baseline

    def evaluate(self, subject_id: str, sequence: np.ndarray) -> Dict[str, object]:
        """Evaluates execution quality of a test skeleton sequence against the subject's ROM baseline."""
        if subject_id not in self.baselines:
            raise ValueError(f'Baseline for subject {subject_id} is not fitted.')
            
        baseline = self.baselines[subject_id]
        joint_confidences = {}
        joint_errors = {}
        
        reps = segment_repetitions(sequence)
        if not reps:
            reps = [sequence]
            
        rep_errors: Dict[str, List[float]] = {k: [] for k in baseline.baseline_angles}
        
        for rep in reps:
            rep_angles = compute_joint_angles(rep)
            for angle_name in baseline.baseline_angles:
                if angle_name not in rep_angles:
                    continue
                ref_curve = baseline.baseline_angles[angle_name]
                smoothed = smooth_angle_signal(rep_angles[angle_name])
                interpolated = interpolate_1d_curve(smoothed, target_length=100)
                
                # Perform DTW alignment
                distance = align_repetition_1d(ref_curve, interpolated)
                rep_errors[angle_name].append(distance)
                
        # Average errors and compute calibrated confidences
        for angle_name in baseline.baseline_angles:
            if rep_errors[angle_name]:
                avg_err = float(np.mean(rep_errors[angle_name]))
                joint_errors[angle_name] = avg_err
                tol = baseline.tolerance[angle_name]
                joint_confidences[angle_name] = float(np.clip(1.0 - (avg_err / (tol + 1e-6)), 0.0, 1.0))
            else:
                joint_errors[angle_name] = 0.0
                joint_confidences[angle_name] = 1.0
                
        overall_confidence = float(np.mean(list(joint_confidences.values()))) if joint_confidences else 0.0
        baseline.progression_score = overall_confidence
        
        top_errors = sorted(joint_errors.items(), key=lambda item: item[1], reverse=True)[:5]
        
        return {
            'subject_id': subject_id,
            'confidence': overall_confidence,
            'joint_confidences': joint_confidences,
            'joint_errors': joint_errors,
            'top_error_joints': top_errors,
            'segments': reps,
            'progression_score': baseline.progression_score,
        }

    def update_tolerance(self, subject_id: str, new_scale: float) -> None:
        """Adapts tolerance values by scale factor based on progress or recovery."""
        if subject_id not in self.baselines:
            raise ValueError(f'Baseline for subject {subject_id} is not fitted.')
        baseline = self.baselines[subject_id]
        for angle_name in baseline.tolerance:
            baseline.tolerance[angle_name] = float(baseline.tolerance[angle_name] * new_scale)

    def rollback(self, subject_id: str) -> bool:
        """Rolls back the subject's baseline to the previous historical state if available."""
        if subject_id not in self.baselines:
            return False
        baseline = self.baselines[subject_id]
        if not hasattr(baseline, 'history') or not baseline.history:
            return False
        
        # Pop previous state from history list
        prev_state = baseline.history.pop()
        
        # Restore angles and tolerances
        baseline.baseline_angles = {k: np.array(v, dtype=np.float32) for k, v in prev_state["angles"].items()}
        baseline.tolerance = dict(prev_state["tolerance"])
        return True

    def save(self, file_path: str) -> None:
        payload = {
            'tolerance_scale': self.tolerance_scale,
            'baselines': {
                subject_id: {
                    'baseline_angles': {k: v.tolist() for k, v in baseline.baseline_angles.items()},
                    'tolerance': baseline.tolerance,
                    'progression_score': baseline.progression_score,
                }
                for subject_id, baseline in self.baselines.items()
            },
        }
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(payload, f, indent=2)

    def load(self, file_path: str) -> None:
        with open(file_path, 'r', encoding='utf-8') as f:
            payload = json.load(f)
        self.tolerance_scale = payload.get('tolerance_scale', 1.0)
        for subject_id, baseline_payload in payload['baselines'].items():
            baseline_angles = {k: np.array(v, dtype=np.float32) for k, v in baseline_payload['baseline_angles'].items()}
            tolerance = {k: float(v) for k, v in baseline_payload['tolerance'].items()}
            progression_score = float(baseline_payload.get('progression_score', 1.0))
            self.baselines[subject_id] = ROMBaseline(
                baseline_angles=baseline_angles,
                tolerance=tolerance,
                subject_id=subject_id,
                progression_score=progression_score,
            )
