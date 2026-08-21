import numpy as np
import torch
from typing import Dict, Any, Optional

from src.dataset import (
    normalize_pelvis_centered,
    interpolate_missing_frames,
    convert_mediapipe_landmarks
)

def mediapipe_to_intellirehab(landmarks: np.ndarray) -> np.ndarray:
    """Transforms MediaPipe world landmarks coordinate convention to Kinect/IntelliRehabDS format.
    
    Coordinate mapping rationale:
    - MediaPipe: X points user-left (screen-right), Y points down, Z points forward (towards camera).
    - Kinect: X points screen-left (user-right), Y points up, Z points away (depth from camera).
    - Negating X, Y, Z rotates the coordinates by 180 degrees and inverts depth to match Kinect.
    """
    return landmarks * np.array([-1.0, -1.0, -1.0], dtype=np.float32)

def canonicalize_skeleton(sequence: np.ndarray, source_metadata: Dict[str, Any]) -> np.ndarray:
    """Processes a skeleton sequence from any source (txt, video, webcam) to (T, 25, 3) canonical representation.
    
    Parameters:
        sequence: np.ndarray of shape (T, N, 3) where N=33 for MediaPipe or N=25 for Kinect.
        source_metadata: Dict with key 'source_type' ('txt', 'video', 'webcam').
        
    Returns:
        np.ndarray: normalized, interpolated sequence of shape (T, 25, 3).
    """
    source_type = source_metadata.get("source_type", "txt").lower()
    
    if source_type in ["video", "webcam"]:
        # Input is MediaPipe (T, 33, 3)
        T, N, C = sequence.shape
        assert N == 33, f"Expected 33 MediaPipe joints for {source_type}, got {N}"
        
        # 1. Transform coordinates
        transformed_seq = np.zeros((T, 33, 3), dtype=np.float32)
        for t in range(T):
            transformed_seq[t] = mediapipe_to_intellirehab(sequence[t])
            
        # 2. Map joints 33 -> 25
        mapped_seq = np.zeros((T, 25, 3), dtype=np.float32)
        for t in range(T):
            mapped_seq[t] = convert_mediapipe_landmarks(transformed_seq[t])
            
        sequence = mapped_seq
        
    elif source_type == "txt":
        # Input is Kinect (T, 25, 3)
        T, N, C = sequence.shape
        assert N == 25, f"Expected 25 Kinect joints for txt, got {N}"
    else:
        raise ValueError(f"Unknown source_type: {source_type}")
        
    # 3. Interpolate missing frames
    sequence = interpolate_missing_frames(sequence)
    
    # 4. Normalize coordinates (pelvis-centered and scaled)
    sequence = normalize_pelvis_centered(sequence)
    
    return sequence.astype(np.float32)
