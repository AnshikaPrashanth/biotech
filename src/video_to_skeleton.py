import os
import json
import time
import cv2
import numpy as np
from pathlib import Path
from typing import Dict, Any, Tuple, Optional

from src.graph import INTELLIREHAB_JOINTS
from src.skeleton_pipeline import canonicalize_skeleton

def write_kinect_txt(file_path: str, sequence: np.ndarray, exercise_type: str) -> None:
    """Writes a 25-joint skeleton sequence to the IntelliRehabDS-compatible TXT format.
    
    Format:
    frame_idx,exercise_type,timestamp,(joint_name,Tracked,x,y,z,0,0),(joint_name,Tracked,x,y,z,0,0)...
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write("Version0.1\n")  # IntelliRehabDS header
        for t in range(sequence.shape[0]):
            frame_joints = sequence[t]  # (25, 3)
            timestamp = int(t * 33.33)  # Approximate 30 FPS timestamp (33.33ms per frame)
            
            joint_strings = []
            for j_idx, joint_name in enumerate(INTELLIREHAB_JOINTS):
                x, y, z = frame_joints[j_idx]
                joint_strings.append(f"({joint_name},Tracked,{x:.6f},{y:.6f},{z:.6f},0,0)")
                
            line = f"{t},{exercise_type},{timestamp}," + ",".join(joint_strings)
            f.write(line + "\n")

def extract_skeleton_from_video(
    video_path: str,
    subject_id: str = "unknown",
    exercise_type: str = "stand",
    export_txt: bool = True,
    out_dir: str = "results/video"
) -> Tuple[np.ndarray, np.ndarray, Dict[str, Any]]:
    """Reads a video, runs MediaPipe Pose on each frame, converts landmarks, 
    and returns both the raw MediaPipe sequence and the canonicalized (T, 25, 3) sequence.
    """
    import mediapipe as mp
    mp_pose = mp.solutions.pose
    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise FileNotFoundError(f"Could not open video file: {video_path}")
        
    fps = float(cap.get(cv2.CAP_PROP_FPS))
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = float(frame_count / fps) if fps > 0 else 0.0
    
    raw_landmarks_list = []
    success_count = 0
    total_frames = 0
    
    # Initialize MediaPipe Pose
    with mp_pose.Pose(
        static_image_mode=False,
        model_complexity=1,
        smooth_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as pose:
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
                
            total_frames += 1
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(rgb_frame)
            
            if results.pose_world_landmarks:
                landmarks = np.array([[lm.x, lm.y, lm.z] for lm in results.pose_world_landmarks.landmark], dtype=np.float32)
                raw_landmarks_list.append(landmarks)
                success_count += 1
            else:
                # Failed frames get a placeholder shape of all zeros
                # These are handled and interpolated by coordinate parser
                raw_landmarks_list.append(np.zeros((33, 3), dtype=np.float32))
                
    cap.release()
    
    if not raw_landmarks_list:
        raise ValueError("No pose data could be extracted from video.")
        
    raw_landmarks_seq = np.stack(raw_landmarks_list, axis=0) # (T, 33, 3)
    
    # Preprocess sequence to canonical representation (T, 25, 3)
    metadata = {"source_type": "video"}
    canonical_seq = canonicalize_skeleton(raw_landmarks_seq, metadata)
    
    detection_success_rate = float(success_count / total_frames) if total_frames > 0 else 0.0
    
    # Store metadata
    metadata_summary = {
        "fps": fps,
        "frame_count": total_frames,
        "duration": duration,
        "subject_id": subject_id,
        "exercise_type": exercise_type,
        "source_path": str(video_path),
        "detection_success_rate": detection_success_rate,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Save outputs
    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    
    npy_path = out_path / f"{subject_id}_{exercise_type}_skeleton.npy"
    np.save(str(npy_path), canonical_seq)
    
    txt_path = None
    if export_txt:
        txt_path = out_path / f"{subject_id}_{exercise_type}_skeleton.txt"
        write_kinect_txt(str(txt_path), canonical_seq, exercise_type)
        
    metadata_path = out_path / f"{subject_id}_{exercise_type}_metadata.json"
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata_summary, f, indent=2)
        
    metadata_summary["npy_path"] = str(npy_path)
    if txt_path:
        metadata_summary["txt_path"] = str(txt_path)
        
    return raw_landmarks_seq, canonical_seq, metadata_summary

def generate_video_overlay(
    video_path: str,
    raw_landmarks_seq: np.ndarray,
    canonical_seq: np.ndarray,
    output_path: str
) -> None:
    """Generates an overlay video showing the original frames, MediaPipe pose, and the 25-joint skeleton side-by-side."""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return
        
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # We will draw a side-by-side video: Left=Original + Pose Overlay, Right=Mapped 25-joint skeleton on black canvas
    out_width = width * 2
    out_height = height
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (out_width, out_height))
    
    import mediapipe as mp
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose
    
    frame_idx = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret or frame_idx >= len(raw_landmarks_seq):
            break
            
        # Draw MediaPipe overlay on left image
        left_img = frame.copy()
        # Draw 25-joint skeleton on right image (black canvas)
        right_img = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Mapped skeleton coordinate visualization
        # The coordinates are normalized (centered at SpineBase, scaled). Let's project them to fit the canvas.
        sk_frame = canonical_seq[frame_idx]
        
        # Let's project 3D joints to 2D image coordinates (use X and Y axes, center at width/2, height/2)
        center_x = width // 2
        center_y = height // 2
        scale = min(width, height) * 0.4
        
        # Draw joints
        projected = {}
        for j_idx, name in enumerate(INTELLIREHAB_JOINTS):
            # Coordinates are inverted, let's uninvert Y and X for standard screen coords
            # Screen: X increases to the right, Y increases downwards
            # Normalized: X points screen-left (-X), Y points screen-up (+Y)
            x_norm, y_norm, _ = sk_frame[j_idx]
            px = int(center_x - x_norm * scale)
            py = int(center_y - y_norm * scale)
            projected[j_idx] = (px, py)
            cv2.circle(right_img, (px, py), 4, (0, 255, 0), -1)
            
        # Draw edges
        from src.graph import INTELLIREHAB_EDGES
        for start, end in INTELLIREHAB_EDGES:
            if start in projected and end in projected:
                cv2.line(right_img, projected[start], projected[end], (255, 255, 255), 2)
                
        # Draw frame number
        cv2.putText(left_img, f"Frame: {frame_idx}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(right_img, "25-Joint Kinect Representation", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        
        # Concatenate side-by-side
        combined = np.hstack((left_img, right_img))
        out.write(combined)
        
        frame_idx += 1
        
    cap.release()
    out.release()
