import csv
import glob
import math
import os
import random
import re
from collections import Counter
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

import cv2
import numpy as np
import torch
from torch.utils.data import DataLoader, Dataset, WeightedRandomSampler

from src.graph import INTELLIREHAB_JOINTS

# Map from joint name to its index in the 25-joint list
INTELLIREHAB_NAME_TO_INDEX = {name: idx for idx, name in enumerate(INTELLIREHAB_JOINTS)}

def extract_subject_id(file_path: str) -> str:
    """Extracts SubjectID from the filename:
    SubjectID_DateID_GestureLabel_RepetitionNumber_CorrectLabel_Position.txt
    """
    basename = os.path.basename(file_path)
    match = re.match(r'^(\d+)_', basename)
    if match:
        return match.group(1)
    return os.path.splitext(basename)[0]

def extract_movement_label(file_path: str) -> int:
    """Extracts movement quality target label from filename.
    CorrectLabel (5th component, split by '_'):
      1 = Correct execution -> Map to 0 (Correct execution)
      2 = Incorrect execution -> Map to 1 (Incorrect execution)
      3 = Unclassified / Ambiguous -> Raise ValueError (Excluded)
    """
    basename = os.path.basename(file_path)
    name_without_ext = os.path.splitext(basename)[0]
    parts = name_without_ext.split('_')
    if len(parts) >= 5:
        correct_label_str = parts[4]
        try:
            val = int(correct_label_str)
            if val == 1:
                return 0  # Correct execution
            elif val == 2:
                return 1  # Incorrect execution
            elif val == 3:
                raise ValueError(f"Label 3 (unclassified repetition) excluded for file {file_path}")
        except ValueError as ve:
            if "Label 3" in str(ve):
                raise ve
            pass
    raise ValueError(f"Invalid or missing movement label in filename: {file_path}")

def parse_intellirehab_file(file_path: str) -> Tuple[np.ndarray, str, str, int]:
    """Parse a single IntelliRehabDS skeleton file into raw 3D joint positions,
    returning the sequence, exercise type, subject_id, and binary movement label.
    """
    frames: List[np.ndarray] = []
    exercise_type = ''
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row or len(row) < 3:
                continue
            exercise_type = row[1].strip()
            joint_data = row[3:]
            frame_joints = np.zeros((len(INTELLIREHAB_JOINTS), 3), dtype=np.float32)
            for idx in range(0, len(joint_data), 7):
                if idx + 6 >= len(joint_data):
                    break
                joint_name = joint_data[idx].replace('(', '').replace(')', '').strip()
                try:
                    x = float(joint_data[idx + 2])
                    y = float(joint_data[idx + 3])
                    z = float(joint_data[idx + 4])
                except ValueError:
                    continue
                if joint_name in INTELLIREHAB_NAME_TO_INDEX:
                    joint_index = INTELLIREHAB_NAME_TO_INDEX[joint_name]
                    frame_joints[joint_index] = [x, y, z]
            frames.append(frame_joints)
    
    if not frames:
        raise ValueError(f'No skeleton frames parsed from {file_path}')
        
    subject_id = extract_subject_id(file_path)
    movement_label = extract_movement_label(file_path)
    
    sequence = np.stack(frames, axis=0)
    sequence = interpolate_missing_frames(sequence)
    sequence = normalize_pelvis_centered(sequence)
    return sequence, exercise_type, subject_id, movement_label

def load_intellirehab_directory(data_dir: str) -> List[Dict]:
    """Recursively search and parse all skeleton files under data_dir."""
    entries = []
    path = Path(data_dir)
    if not path.exists():
        print(f"Data directory {data_dir} does not exist.")
        return []
    
    if path.is_file():
        file_paths = [path]
    else:
        file_paths = list(path.glob('**/*.txt')) + list(path.glob('**/*.csv'))
        
    for fp in file_paths:
        try:
            sequence, exercise_type, subject_id, movement_label = parse_intellirehab_file(str(fp))
            entries.append({
                'sequence': sequence,
                'exercise_type': exercise_type,
                'subject_id': subject_id,
                'movement_label': movement_label,
                'file_path': str(fp)
            })
        except Exception as e:
            print(f"Skipping {fp}: error parsing: {e}")
    return entries

def normalize_pelvis_centered(sequence: np.ndarray) -> np.ndarray:
    """Center skeleton on the pelvis and normalize scale by average skeleton span."""
    # Pelvis reference is SpineBase (0)
    pelvis_idx = INTELLIREHAB_NAME_TO_INDEX.get('SpineBase', 0)
    pelvis = sequence[:, pelvis_idx:pelvis_idx+1, :] # Shape (frames, 1, 3)
    centered = sequence - pelvis
    
    # Compute standard bounding box size or joint spread to normalize size
    joint_spread = np.linalg.norm(centered, axis=2) # Shape (frames, 25)
    scale = np.maximum(np.max(joint_spread), 1e-6)
    normalized = centered / scale
    return normalized.astype(np.float32)

def interpolate_missing_frames(sequence: np.ndarray) -> np.ndarray:
    """Fill missing Kinect frames (coordinates near 0) by linear interpolation."""
    sequence = sequence.copy()
    num_frames, num_joints, _ = sequence.shape
    time_axis = np.arange(num_frames)
    for joint_idx in range(num_joints):
        for dim in range(3):
            values = sequence[:, joint_idx, dim]
            missing = np.isclose(values, 0.0, atol=1e-5)
            if missing.all():
                continue
            valid_idx = time_axis[~missing]
            valid_values = values[~missing]
            if valid_idx.size == 0:
                continue
            sequence[:, joint_idx, dim] = np.interp(time_axis, valid_idx, valid_values)
    return sequence.astype(np.float32)

# Augmentations
def gaussian_noise(sequence: np.ndarray, std: float = 0.01) -> np.ndarray:
    return sequence + np.random.normal(scale=std, size=sequence.shape).astype(np.float32)

def random_rotation(sequence: np.ndarray, max_angle_degrees: float = 15.0) -> np.ndarray:
    angle = np.deg2rad(np.random.uniform(-max_angle_degrees, max_angle_degrees))
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    # Rotation about the vertical (Y) axis
    rotation_matrix = np.array([
        [cos_a, 0.0, sin_a],
        [0.0, 1.0, 0.0],
        [-sin_a, 0.0, cos_a],
    ], dtype=np.float32)
    return np.einsum('ij,tkj->tki', rotation_matrix, sequence).astype(np.float32)

def random_scaling(sequence: np.ndarray, scale_range: Tuple[float, float] = (0.9, 1.1)) -> np.ndarray:
    scale = np.random.uniform(*scale_range)
    return (sequence * scale).astype(np.float32)

def temporal_crop(sequence: np.ndarray, target_length: int) -> np.ndarray:
    if sequence.shape[0] <= target_length:
        return sequence
    start = np.random.randint(0, sequence.shape[0] - target_length + 1)
    return sequence[start:start + target_length]

def frame_dropout(sequence: np.ndarray, dropout_prob: float = 0.1) -> np.ndarray:
    mask = np.random.rand(sequence.shape[0]) >= dropout_prob
    if not mask.any():
        mask[np.random.randint(sequence.shape[0])] = True
    return sequence[mask]

def pad_sequences(sequences: Sequence[np.ndarray], max_length: Optional[int] = None) -> Tuple[torch.Tensor, torch.Tensor]:
    lengths = [seq.shape[0] for seq in sequences]
    max_length = max_length or max(lengths)
    padded = torch.zeros((len(sequences), max_length, len(INTELLIREHAB_JOINTS), 3), dtype=torch.float32)
    mask = torch.zeros((len(sequences), max_length), dtype=torch.bool)
    for i, seq in enumerate(sequences):
        length = min(seq.shape[0], max_length)
        padded[i, :length] = torch.from_numpy(seq[:length])
        mask[i, :length] = 1
    return padded, mask

def build_label_encoder(entries: List[Dict]) -> Dict[str, int]:
    labels = sorted({entry['exercise_type'].lower() for entry in entries})
    return {label: idx for idx, label in enumerate(labels)}

def make_weighted_sampler(entries: List[Dict], target_key: str = 'movement_label') -> WeightedRandomSampler:
    """Balances targets using a WeightedRandomSampler based on target_key classes."""
    targets = [entry[target_key] for entry in entries]
    class_counts = Counter(targets)
    weights = [1.0 / max(class_counts[t], 1) for t in targets]
    return WeightedRandomSampler(weights, num_samples=len(weights), replacement=True)

def sequence_collate_fn(batch: List[Dict], max_length: Optional[int] = None) -> Dict[str, torch.Tensor]:
    sequences = [item['sequence'].numpy() if isinstance(item['sequence'], torch.Tensor) else item['sequence'] for item in batch]
    padded_sequences, mask = pad_sequences(sequences, max_length=max_length)
    labels = torch.stack([item['label'] for item in batch])
    subject_ids = [item['subject_id'] for item in batch]
    exercise_types = [item['exercise_type'] for item in batch]
    file_paths = [item['file_path'] for item in batch]
    return {
        'sequence': padded_sequences,
        'mask': mask,
        'label': labels,
        'subject_id': subject_ids,
        'exercise_type': exercise_types,
        'file_path': file_paths,
    }

class IntelliRehabSequenceDataset(Dataset):
    """PyTorch dataset wrapper for IntelliRehab skeleton sequences."""

    def __init__(
        self,
        entries: List[Dict],
        augment: bool = False,
        sequence_length: Optional[int] = None,
    ):
        self.entries = entries
        self.augment = augment
        self.sequence_length = sequence_length

    def __len__(self) -> int:
        return len(self.entries)

    def _apply_augmentation(self, sequence: np.ndarray) -> np.ndarray:
        if not self.augment:
            return sequence
        if random.random() < 0.5:
            sequence = gaussian_noise(sequence, std=0.01)
        if random.random() < 0.5:
            sequence = random_rotation(sequence, max_angle_degrees=10.0)
        if random.random() < 0.5:
            sequence = random_scaling(sequence, scale_range=(0.95, 1.05))
        if self.sequence_length is not None and sequence.shape[0] > self.sequence_length:
            sequence = temporal_crop(sequence, self.sequence_length)
        if random.random() < 0.3:
            sequence = frame_dropout(sequence, dropout_prob=0.05)
        sequence = interpolate_missing_frames(sequence)
        return sequence

    def __getitem__(self, index: int) -> Dict:
        entry = self.entries[index]
        sequence = entry['sequence']
        
        # Enforce sequence length constraint for both train and validation
        if self.sequence_length is not None and sequence.shape[0] > self.sequence_length:
            if self.augment:
                # Random crop during training
                start = np.random.randint(0, sequence.shape[0] - self.sequence_length + 1)
                sequence = sequence[start:start + self.sequence_length]
            else:
                # Center crop during validation to maintain determinism
                start = (sequence.shape[0] - self.sequence_length) // 2
                sequence = sequence[start:start + self.sequence_length]
                
        sequence = self._apply_augmentation(sequence)
        sequence = torch.from_numpy(sequence.astype(np.float32))
        
        # Binary Classification Target: 0 (Healthy) or 1 (Compensated)
        label = entry['movement_label']
        
        return {
            'sequence': sequence,
            'label': torch.tensor(label, dtype=torch.long),
            'subject_id': entry['subject_id'],
            'exercise_type': entry['exercise_type'],
            'file_path': entry['file_path'],
        }

def loso_split(entries: List[Dict]) -> List[Dict[str, List[int]]]:
    """Create Leave-One-Subject-Out splits from parsed dataset entries."""
    subjects = sorted({entry['subject_id'] for entry in entries})
    subject_to_indices = {subj: [] for subj in subjects}
    for idx, entry in enumerate(entries):
        subject_to_indices[entry['subject_id']].append(idx)
    splits = []
    for left_out in subjects:
        train_indices = [i for subj, idxs in subject_to_indices.items() if subj != left_out for i in idxs]
        val_indices = list(subject_to_indices[left_out])
        splits.append({'left_out_subject': left_out, 'train': train_indices, 'val': val_indices})
    return splits

def build_loso_dataloaders(
    entries: List[Dict],
    batch_size: int = 8,
    num_workers: int = 0,
    shuffle: bool = True,
    augment: bool = False,
    sequence_length: Optional[int] = None,
) -> List[Tuple[str, DataLoader, DataLoader]]:
    """Build a list of LOSO train/validation data loaders for each subject."""
    splits = loso_split(entries)
    dataloaders = []
    for split in splits:
        train_entries = [entries[i] for i in split['train']]
        val_entries = [entries[i] for i in split['val']]
        
        train_dataset = IntelliRehabSequenceDataset(train_entries, augment=augment, sequence_length=sequence_length)
        val_dataset = IntelliRehabSequenceDataset(val_entries, augment=False, sequence_length=None)
        
        sampler = make_weighted_sampler(train_entries, target_key='movement_label')
        
        train_loader = DataLoader(
            train_dataset,
            batch_size=batch_size,
            sampler=sampler,
            num_workers=num_workers,
            collate_fn=sequence_collate_fn,
        )
        val_loader = DataLoader(
            val_dataset,
            batch_size=batch_size,
            shuffle=False,
            num_workers=num_workers,
            collate_fn=sequence_collate_fn,
        )
        dataloaders.append((split['left_out_subject'], train_loader, val_loader))
    return dataloaders

def convert_mediapipe_landmarks(landmarks: np.ndarray) -> np.ndarray:
    """Convert MediaPipe pose landmarks (33, 3) to Kinect v2 (25, 3) skeleton coordinates."""
    if landmarks.ndim != 2 or landmarks.shape[0] != 33:
        raise ValueError('MediaPipe landmarks must be a (33, 3) array.')
    
    coords = np.zeros((25, 3), dtype=np.float32)
    
    # 0: SpineBase = (HipLeft + HipRight) / 2
    coords[0] = (landmarks[23] + landmarks[24]) / 2.0
    
    # 4: ShoulderLeft, 8: ShoulderRight
    coords[4] = landmarks[11]
    coords[8] = landmarks[12]
    
    # 20: SpineShoulder = (ShoulderLeft + ShoulderRight) / 2
    coords[20] = (landmarks[11] + landmarks[12]) / 2.0
    
    # 3: Head = Nose (0)
    coords[3] = landmarks[0]
    
    # 2: Neck = SpineShoulder + 0.3 * (Head - SpineShoulder)
    coords[2] = coords[20] + 0.3 * (coords[3] - coords[20])
    
    # 1: SpineMid = (SpineBase + SpineShoulder) / 2
    coords[1] = (coords[0] + coords[20]) / 2.0
    
    # Upper extremities
    coords[5] = landmarks[13]  # ElbowLeft
    coords[6] = landmarks[15]  # WristLeft
    coords[7] = (landmarks[15] + landmarks[19]) / 2.0  # HandLeft (midpoint between Wrist and Left Index)
    coords[21] = landmarks[19] # HandTipLeft (Left Index)
    coords[22] = landmarks[21] # ThumbLeft
    
    coords[9] = landmarks[14]  # ElbowRight
    coords[10] = landmarks[16] # WristRight
    coords[11] = (landmarks[16] + landmarks[20]) / 2.0 # HandRight (midpoint between Wrist and Right Index)
    coords[23] = landmarks[20] # HandTipRight (Right Index)
    coords[24] = landmarks[22] # ThumbRight
    
    # Lower extremities
    coords[12] = landmarks[23] # HipLeft
    coords[13] = landmarks[25] # KneeLeft
    coords[14] = landmarks[27] # AnkleLeft
    coords[15] = landmarks[31] # FootLeft (Left Foot index/heel)
    
    coords[16] = landmarks[24] # HipRight
    coords[17] = landmarks[26] # KneeRight
    coords[18] = landmarks[28] # AnkleRight
    coords[19] = landmarks[32] # FootRight (Right Foot index/heel)
    
    return coords

def build_mediapipe_pose():
    try:
        import mediapipe as mp
    except ImportError:
        raise ImportError("MediaPipe is not installed. Please install it with 'pip install mediapipe' to use live webcam pose capture.")
    mp_pose = mp.solutions.pose
    return mp_pose.Pose(
        static_image_mode=False,
        model_complexity=1,
        smooth_landmarks=True,
        enable_segmentation=False,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    )

def capture_mediapipe_sequence(
    sequence_length: int = 60,
    source: int = 0,
    smoothing_alpha: float = 0.7,
) -> np.ndarray:
    """Capture a live MediaPipe sequence from a webcam and return 25-joint 3D coordinates."""
    pose = build_mediapipe_pose()
    cap = cv2.VideoCapture(source)
    buffered_sequence: List[np.ndarray] = []
    smoothed_frame: Optional[np.ndarray] = None
    while len(buffered_sequence) < sequence_length and cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = pose.process(image)
        if result.pose_world_landmarks is None:
            continue
        landmarks = np.array([[lm.x, lm.y, lm.z] for lm in result.pose_world_landmarks.landmark], dtype=np.float32)
        joint_coords = convert_mediapipe_landmarks(landmarks)
        if smoothed_frame is None:
            smoothed_frame = joint_coords
        else:
            smoothed_frame = smoothing_alpha * smoothed_frame + (1.0 - smoothing_alpha) * joint_coords
        buffered_sequence.append(smoothed_frame.astype(np.float32))
    cap.release()
    pose.close()
    if not buffered_sequence:
        raise RuntimeError('No pose data captured from webcam.')
    sequence = np.stack(buffered_sequence, axis=0)
    return normalize_pelvis_centered(sequence)
