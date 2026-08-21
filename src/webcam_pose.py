import cv2
import numpy as np
import time
from typing import Dict, Any, List, Optional, Tuple

import mediapipe as mp
from src.skeleton_pipeline import canonicalize_skeleton

class WebcamPoseStreamer:
    """Manages real-time webcam frame processing, pose tracking, coordinate mapping,
    temporal buffering, and periodic ST-GAT model inference triggering.
    """
    def __init__(
        self,
        sequence_length: int = 64,
        inference_interval: int = 5,
    ):
        self.sequence_length = sequence_length
        self.inference_interval = inference_interval
        
        # Sliding buffer for MediaPipe 33-landmark world coordinates
        self.raw_buffer: List[np.ndarray] = []
        self.frame_times: List[float] = []
        self.frame_count = 0
        self.fps = 0.0
        
        # MediaPipe Solutions setup
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.pose_engine = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            smooth_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
    def process_frame(self, frame: np.ndarray) -> Tuple[np.ndarray, Optional[np.ndarray], str]:
        """Processes a single BGR video frame.
        
        Updates the frame buffer, calculates current FPS, runs MediaPipe,
        overlays pose landmarks, and returns:
          - The annotated BGR frame
          - Mapped (T, 25, 3) canonical skeleton sequence (if buffer is full and stride is met)
          - Status string
        """
        self.frame_count += 1
        t_start = time.time()
        self.frame_times.append(t_start)
        if len(self.frame_times) > 30:
            self.frame_times.pop(0)
            
        if len(self.frame_times) > 1:
            self.fps = len(self.frame_times) / (self.frame_times[-1] - self.frame_times[0])
            
        h, w, c = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose_engine.process(rgb_frame)
        
        pose_detected = False
        status_msg = "No person detected"
        
        if results.pose_landmarks and results.pose_world_landmarks:
            pose_detected = True
            status_msg = "Tracking skeleton"
            
            # Draw standard MediaPipe skeleton on frame
            self.mp_drawing.draw_landmarks(
                frame,
                results.pose_landmarks,
                self.mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=self.mp_drawing_styles.get_default_pose_landmarks_style()
            )
            
            # Extract world landmarks (33, 3)
            landmarks = np.array([[lm.x, lm.y, lm.z] for lm in results.pose_world_landmarks.landmark], dtype=np.float32)
            self.raw_buffer.append(landmarks)
        else:
            # If tracking fails, insert a frame of all zeros.
            # Our parser's interpolate_missing_frames will automatically interpolate it.
            self.raw_buffer.append(np.zeros((33, 3), dtype=np.float32))
            status_msg = "Pose detection failed (interpolating)"
            
        # Maintain sliding buffer size
        if len(self.raw_buffer) > self.sequence_length:
            self.raw_buffer.pop(0)
            
        # Determine if we should trigger inference
        # Trigger when buffer is full AND we hit the inference interval (stride)
        inference_seq = None
        if len(self.raw_buffer) == self.sequence_length:
            if self.frame_count % self.inference_interval == 0:
                raw_seq = np.stack(self.raw_buffer, axis=0) # (T, 33, 3)
                metadata = {"source_type": "webcam"}
                inference_seq = canonicalize_skeleton(raw_seq, metadata)
                status_msg = "Running inference"
            else:
                status_msg = "Buffering (Inference stride)"
        else:
            status_msg = f"Buffering ({len(self.raw_buffer)}/{self.sequence_length})"
            
        return frame, inference_seq, status_msg
        
    def close(self) -> None:
        """Closes the MediaPipe pose tracking engine."""
        self.pose_engine.close()
