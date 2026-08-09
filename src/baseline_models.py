import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import List, Tuple, Dict

from src.calibration import compute_joint_angles
from src.graph import get_edge_index, build_batched_edge_index, INTELLIREHAB_JOINTS


def pad_or_crop_sequence(sequence: np.ndarray, target_length: int) -> np.ndarray:
    if sequence.shape[0] == target_length:
        return sequence
    if sequence.shape[0] > target_length:
        start = (sequence.shape[0] - target_length) // 2
        return sequence[start:start + target_length]
    padded = np.zeros((target_length, sequence.shape[1], sequence.shape[2]), dtype=sequence.dtype)
    padded[:sequence.shape[0]] = sequence
    padded[sequence.shape[0]:] = sequence[-1:]
    return padded


def extract_sequence_features(sequence: np.ndarray, target_length: int = 64) -> np.ndarray:
    sequence = pad_or_crop_sequence(sequence, target_length)
    seq_len, num_nodes, dims = sequence.shape
    coords = sequence.reshape(seq_len, num_nodes * dims)

    stats = [coords.mean(axis=0), coords.std(axis=0), coords.min(axis=0), coords.max(axis=0)]
    coord_features = np.concatenate(stats, axis=0)

    angles = compute_joint_angles(sequence)
    angle_array = np.stack([angles[key] for key in sorted(angles.keys())], axis=1)
    angle_stats = [angle_array.mean(axis=0), angle_array.std(axis=0), np.percentile(angle_array, 5, axis=0), np.percentile(angle_array, 95, axis=0)]
    angle_features = np.concatenate(angle_stats, axis=0)

    temporal_grad = np.diff(coords, axis=0)
    grad_stats = [temporal_grad.mean(axis=0), temporal_grad.std(axis=0)]
    grad_features = np.concatenate(grad_stats, axis=0)

    return np.concatenate([coord_features, angle_features, grad_features], axis=0)


def build_feature_matrix(entries: List[Dict], target_length: int = 64) -> Tuple[np.ndarray, np.ndarray, List[str]]:
    features = []
    labels = []
    subject_ids = []
    for entry in entries:
        features.append(extract_sequence_features(entry['sequence'], target_length=target_length))
        labels.append(entry['movement_label'])
        subject_ids.append(entry['subject_id'])
    return np.stack(features, axis=0), np.array(labels, dtype=np.int64), subject_ids


class SequenceBaselineModel(nn.Module):
    def __init__(self, input_size: int, hidden_dim: int = 64, num_layers: int = 2, dropout: float = 0.2):
        super().__init__()
        self.input_size = input_size
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers
        self.dropout = dropout

    @staticmethod
    def _final_classification(hidden: torch.Tensor, num_classes: int = 2) -> torch.Tensor:
        return hidden


class LSTMClassifier(SequenceBaselineModel):
    def __init__(self, input_size: int = 75, hidden_dim: int = 64, num_layers: int = 2, dropout: float = 0.2):
        super().__init__(input_size, hidden_dim, num_layers, dropout)
        self.lstm = nn.LSTM(input_size, hidden_dim, num_layers=num_layers, batch_first=True, dropout=dropout, bidirectional=False)
        self.classifier = nn.Sequential(
            nn.LayerNorm(hidden_dim),
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(inplace=True),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim // 2, 2),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = x.view(x.shape[0], x.shape[1], -1)
        outputs, (hidden, _) = self.lstm(x)
        pooled = hidden[-1]
        return self.classifier(pooled)


class GRUClassifier(SequenceBaselineModel):
    def __init__(self, input_size: int = 75, hidden_dim: int = 64, num_layers: int = 2, dropout: float = 0.2):
        super().__init__(input_size, hidden_dim, num_layers, dropout)
        self.gru = nn.GRU(input_size, hidden_dim, num_layers=num_layers, batch_first=True, dropout=dropout, bidirectional=False)
        self.classifier = nn.Sequential(
            nn.LayerNorm(hidden_dim),
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(inplace=True),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim // 2, 2),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = x.view(x.shape[0], x.shape[1], -1)
        outputs, hidden = self.gru(x)
        pooled = hidden[-1]
        return self.classifier(pooled)


class STGCNBlock(nn.Module):
    def __init__(self, in_channels: int, out_channels: int, dropout: float = 0.2):
        super().__init__()
        self.conv = nn.Conv1d(in_channels, out_channels, kernel_size=3, padding=1)
        self.norm = nn.BatchNorm1d(out_channels)
        self.act = nn.ReLU(inplace=True)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.conv(x)
        x = self.norm(x)
        x = self.act(x)
        return self.dropout(x)


class STGCNClassifier(SequenceBaselineModel):
    def __init__(self, input_dim: int = 3, hidden_dim: int = 64, num_layers: int = 2, dropout: float = 0.2):
        super().__init__(input_dim, hidden_dim, num_layers, dropout)
        self.input_proj = nn.Linear(input_dim, hidden_dim)
        self.spatial_conv = nn.ModuleList([
            STGCNBlock(hidden_dim, hidden_dim, dropout=dropout) for _ in range(2)
        ])
        self.temporal_conv = nn.ModuleList([
            STGCNBlock(hidden_dim, hidden_dim, dropout=dropout) for _ in range(2)
        ])
        self.classifier = nn.Sequential(
            nn.LayerNorm(hidden_dim),
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(inplace=True),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim // 2, 2),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        batch, seq_len, num_nodes, dims = x.shape
        x = self.input_proj(x)
        x = x.permute(0, 2, 3, 1)
        for block in self.spatial_conv:
            x = block(x)
        x = x.permute(0, 2, 3, 1)
        for block in self.temporal_conv:
            x = block(x)
        pooled = x.mean(dim=3).mean(dim=1)
        return self.classifier(pooled)
