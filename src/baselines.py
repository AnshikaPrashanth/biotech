import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import GCNConv
from sklearn.ensemble import RandomForestClassifier
import numpy as np
from typing import Dict, List, Optional
from src.calibration import compute_joint_angles
from src.graph import get_edge_index, build_batched_edge_index

# 1. LSTM Baseline Model
class LSTMRehabClassifier(nn.Module):
    def __init__(self, input_dim: int = 25 * 3, hidden_dim: int = 64, num_layers: int = 2, num_classes: int = 2):
        super().__init__()
        self.lstm = nn.LSTM(
            input_size=input_dim,
            hidden_size=hidden_dim,
            num_layers=num_layers,
            batch_first=True,
            bidirectional=True
        )
        self.fc = nn.Sequential(
            nn.Linear(hidden_dim * 2, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(hidden_dim, num_classes)
        )

    def forward(self, x: torch.Tensor) -> Dict[str, torch.Tensor]:
        # x shape: (batch, seq_len, 25, 3)
        batch, seq_len, num_nodes, num_features = x.shape
        x_flat = x.reshape(batch, seq_len, num_nodes * num_features) # (batch, seq_len, 75)
        
        lstm_out, _ = self.lstm(x_flat) # (batch, seq_len, hidden_dim * 2)
        # Global max pooling over time dimension
        pooled, _ = torch.max(lstm_out, dim=1) # (batch, hidden_dim * 2)
        
        logits = self.fc(pooled)
        probs = F.softmax(logits, dim=-1)
        return {
            'logits': logits,
            'probabilities': probs,
            'joint_attention': torch.zeros((batch, num_nodes), device=x.device),
            'frame_attention': torch.zeros((batch, seq_len), device=x.device)
        }

# 2. ST-GCN Simplified Baseline Model
class STGCNBlock(nn.Module):
    def __init__(self, in_channels: int, out_channels: int):
        super().__init__()
        self.gcn = GCNConv(in_channels, out_channels)
        self.tcn = nn.Conv1d(out_channels, out_channels, kernel_size=3, padding=1)
        self.norm = nn.BatchNorm1d(out_channels)
        self.act = nn.ReLU()

    def forward(self, x: torch.Tensor, edge_index: torch.Tensor, batch_size: int, seq_len: int, num_nodes: int) -> torch.Tensor:
        # Spatial Graph Convolution
        x = self.gcn(x, edge_index)
        
        # Reshape to temporal sequence: (batch, nodes, channels, seq_len)
        x = x.reshape(batch_size, seq_len, num_nodes, -1).permute(0, 2, 3, 1) # (batch, nodes, channels, seq)
        
        # Temporal convolution
        batch, nodes, channels, seq = x.shape
        x = x.reshape(batch * nodes, channels, seq)
        x = self.tcn(x)
        x = self.norm(x)
        x = self.act(x)
        
        # Reshape back to flat nodes format: (batch * seq * nodes, channels)
        x = x.reshape(batch, nodes, channels, seq).permute(0, 3, 1, 2).reshape(batch * seq * nodes, -1)
        return x

class STGCNRehabClassifier(nn.Module):
    def __init__(self, input_dim: int = 3, hidden_dim: int = 64, num_classes: int = 2):
        super().__init__()
        self.register_buffer('edge_index', get_edge_index())
        self.input_proj = nn.Linear(input_dim, hidden_dim)
        
        self.block1 = STGCNBlock(hidden_dim, hidden_dim)
        self.block2 = STGCNBlock(hidden_dim, hidden_dim)
        
        self.fc = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(),
            nn.Linear(hidden_dim // 2, num_classes)
        )

    def forward(self, x: torch.Tensor) -> Dict[str, torch.Tensor]:
        batch_size, seq_len, num_nodes, num_features = x.shape
        x_proj = self.input_proj(x) # (batch, seq, nodes, hidden)
        
        # Flatten for PyG convolution layers
        flattened = x_proj.reshape(batch_size * seq_len * num_nodes, -1)
        batched_edges = build_batched_edge_index(self.edge_index, batch_size * seq_len, num_nodes)
        
        h1 = self.block1(flattened, batched_edges, batch_size, seq_len, num_nodes)
        h2 = self.block2(h1, batched_edges, batch_size, seq_len, num_nodes)
        
        # Reshape to (batch, seq, nodes, hidden)
        h_seq = h2.reshape(batch_size, seq_len, num_nodes, -1)
        # Average pooling over time and nodes
        pooled = h_seq.mean(dim=2).mean(dim=1) # (batch, hidden)
        
        logits = self.fc(pooled)
        probs = F.softmax(logits, dim=-1)
        return {
            'logits': logits,
            'probabilities': probs,
            'joint_attention': torch.zeros((batch_size, num_nodes), device=x.device),
            'frame_attention': torch.zeros((batch_size, seq_len), device=x.device)
        }

# 3. Biomechanical Feature Extractor for Random Forest
class BiomechanicalRFClassifier:
    def __init__(self, n_estimators: int = 100):
        self.rf = RandomForestClassifier(n_estimators=n_estimators, random_state=42, class_weight='balanced')

    def extract_features(self, sequences: List[np.ndarray]) -> np.ndarray:
        features = []
        for seq in sequences:
            # seq shape: (frames, 25, 3)
            angles = compute_joint_angles(seq)
            f_vec = []
            for name in sorted(angles.keys()):
                traj = angles[name]
                if len(traj) > 0:
                    f_vec.extend([float(traj.min()), float(traj.max()), float(traj.mean()), float(traj.std())])
                else:
                    f_vec.extend([0.0, 0.0, 0.0, 0.0])
            features.append(f_vec)
        return np.array(features, dtype=np.float32)

    def fit(self, sequences: List[np.ndarray], labels: List[int]):
        X = self.extract_features(sequences)
        y = np.array(labels, dtype=np.int64)
        self.rf.fit(X, y)

    def predict(self, sequences: List[np.ndarray]) -> np.ndarray:
        X = self.extract_features(sequences)
        return self.rf.predict(X)

    def predict_proba(self, sequences: List[np.ndarray]) -> np.ndarray:
        X = self.extract_features(sequences)
        return self.rf.predict_proba(X)
