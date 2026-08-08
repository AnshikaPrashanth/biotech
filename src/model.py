import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import GATConv
from typing import Dict, Optional, Tuple

from src.graph import get_edge_index, build_batched_edge_index

class SpatialGATBlock(nn.Module):
    def __init__(self, in_channels: int, out_channels: int, heads: int = 4, dropout: float = 0.1):
        super().__init__()
        # GATConv divides hidden dimensions into heads. So out_channels must be divisible by heads.
        self.gat = GATConv(in_channels, out_channels // heads, heads=heads, concat=True, dropout=dropout)
        self.norm = nn.BatchNorm1d(out_channels)
        self.act = nn.LeakyReLU(0.2)
        self.residual = nn.Identity() if in_channels == out_channels else nn.Linear(in_channels, out_channels)

    def forward(self, x: torch.Tensor, edge_index: torch.Tensor, return_attn: bool = True) -> Tuple[torch.Tensor, Optional[torch.Tensor]]:
        residual = self.residual(x)
        if return_attn:
            x, (_, attn) = self.gat(x, edge_index, return_attention_weights=True)
            x = self.norm(x)
            x = self.act(x)
            x = x + residual
            # Average attention weights over multiple attention heads
            edge_attention = attn.mean(dim=1)
            return x, edge_attention
        else:
            x = self.gat(x, edge_index)
            x = self.norm(x)
            x = self.act(x)
            x = x + residual
            return x, None

class TemporalConvBlock(nn.Module):
    def __init__(self, channels: int, kernel_size: int = 3, dropout: float = 0.1):
        super().__init__()
        self.conv = nn.Conv1d(channels, channels, kernel_size=kernel_size, padding=kernel_size // 2)
        self.norm = nn.BatchNorm1d(channels)
        self.act = nn.ReLU()
        self.dropout = nn.Dropout(dropout)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        batch, nodes, channels, seq_len = x.shape
        x_in = x
        # Collapse batch and node dimensions to perform 1D temporal convolution
        x = x.reshape(batch * nodes, channels, seq_len)
        x = self.conv(x)
        x = self.norm(x)
        x = self.act(x)
        x = self.dropout(x)
        x = x.reshape(batch, nodes, channels, seq_len)
        return x + x_in

class TemporalAttentionBlock(nn.Module):
    def __init__(self, channels: int, num_heads: int = 4, dropout: float = 0.1):
        super().__init__()
        self.attn = nn.MultiheadAttention(embed_dim=channels, num_heads=num_heads, dropout=dropout, batch_first=False)
        self.norm = nn.LayerNorm(channels)

    def forward(self, x: torch.Tensor, return_attn: bool = True) -> Tuple[torch.Tensor, Optional[torch.Tensor]]:
        batch, nodes, channels, seq_len = x.shape
        # Permute to (seq_len, batch * nodes, channels) for PyTorch MultiheadAttention
        query = x.permute(3, 0, 1, 2).reshape(seq_len, batch * nodes, channels)
        
        if return_attn:
            attn_out, attn_weights = self.attn(query, query, query, need_weights=True, average_attn_weights=False)
            # attn_out shape: (seq_len, batch * nodes, channels)
            # attn_weights shape: (batch * nodes, seq_len, seq_len)
            attn_out = attn_out.reshape(seq_len, batch, nodes, channels).permute(1, 2, 3, 0)
            
            # Compute frame attention: average weights over heads, then average over nodes and queries
            # attn_weights has shape (batch_size * nodes, num_heads, seq_len, seq_len)
            attn_weights = attn_weights.mean(dim=1)  # shape: (batch_size * nodes, seq_len, seq_len)
            attn_weights = attn_weights.reshape(batch, nodes, seq_len, seq_len)
            attn_weights = attn_weights.mean(dim=1)  # shape: (batch, seq_len, seq_len)
            frame_attn = attn_weights.mean(dim=1)  # shape: (batch, seq_len)
            # Apply LayerNorm along the channels dimension by transposing
            out = (attn_out + x).permute(0, 1, 3, 2)  # shape: (batch, nodes, seq_len, channels)
            out = self.norm(out)
            out = out.permute(0, 1, 3, 2)  # shape: (batch, nodes, channels, seq_len)
            return out, frame_attn
        else:
            attn_out, _ = self.attn(query, query, query, need_weights=False)
            attn_out = attn_out.reshape(seq_len, batch, nodes, channels).permute(1, 2, 3, 0)
            out = (attn_out + x).permute(0, 1, 3, 2)
            out = self.norm(out)
            out = out.permute(0, 1, 3, 2)
            return out, None

class STGAT(nn.Module):
    def __init__(
        self,
        input_dim: int = 3,
        hidden_dim: int = 64,
        num_classes: int = 2,
        heads: int = 4,
        dropout: float = 0.2,
    ):
        super().__init__()
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.num_classes = num_classes
        self.heads = heads
        
        # Spatial graph structure
        self.register_buffer('spatial_edge_index', get_edge_index())
        
        self.input_proj = nn.Linear(input_dim, hidden_dim)
        
        # Spatial Graph Attention blocks
        self.spatial1 = SpatialGATBlock(hidden_dim, hidden_dim, heads=heads, dropout=dropout)
        self.spatial2 = SpatialGATBlock(hidden_dim, hidden_dim, heads=heads, dropout=dropout)
        
        # Temporal Convolution Blocks
        self.temporal1 = TemporalConvBlock(hidden_dim, kernel_size=3, dropout=dropout)
        self.temporal2 = TemporalConvBlock(hidden_dim, kernel_size=3, dropout=dropout)
        
        # Temporal Multi-Head Attention block
        self.temporal_attention = TemporalAttentionBlock(hidden_dim, num_heads=heads, dropout=dropout)
        
        self.classifier = nn.Sequential(
            nn.LayerNorm(hidden_dim),
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim // 2, num_classes),
        )
        self.export_mode = False

    def forward(self, x: torch.Tensor) -> Dict[str, torch.Tensor]:
        """Runs full forward pass returning logits, probabilities, and spatial/temporal explainability weights."""
        if self.export_mode:
            # Route to simplified forward if export mode is manually turned on
            logits = self.forward_export(x)
            probabilities = F.softmax(logits, dim=-1)
            return {
                'logits': logits,
                'probabilities': probabilities,
                'joint_attention': torch.zeros_like(probabilities),
                'frame_attention': torch.zeros_like(probabilities),
                'edge_attention': torch.zeros_like(probabilities)
            }
            
        batch_size, seq_len, num_nodes, num_features = x.shape
        # Project features
        x_proj = self.input_proj(x)  # (batch_size, seq_len, 25, hidden_dim)
        
        # Reshape to batched PyG inputs
        flattened = x_proj.reshape(batch_size * seq_len * num_nodes, -1)
        
        # Re-build edge index for PyG batched structure
        edge_index = build_batched_edge_index(self.spatial_edge_index, batch_size * seq_len, num_nodes)
        
        # Spatial Graph Attention
        spatial_out1, edge_attn1 = self.spatial1(flattened, edge_index, return_attn=True)
        spatial_out2, edge_attn2 = self.spatial2(spatial_out1, edge_index, return_attn=True)
        
        # Reshape back to spatial-temporal structure
        spatial_out = spatial_out2.reshape(batch_size, seq_len, num_nodes, -1).permute(0, 2, 3, 1)  # (batch, nodes, channels, seq_len)
        
        # Temporal Conv Blocks
        temporal_out = self.temporal1(spatial_out)
        temporal_out = self.temporal2(temporal_out)
        
        # Temporal Attention
        temporal_out, frame_attention = self.temporal_attention(temporal_out, return_attn=True)
        
        # Global Pooling (average over sequence frames and spatial joints)
        pooled = temporal_out.mean(dim=3).mean(dim=1)  # (batch_size, hidden_dim)
        
        # Classifier
        logits = self.classifier(pooled)
        probabilities = F.softmax(logits, dim=-1)
        
        # Reshape and aggregate edge attentions
        edge_attention = edge_attn2.reshape(batch_size, seq_len, -1).mean(dim=1)  # (batch_size, num_edges_per_graph)
        joint_attention = self._aggregate_node_attention(edge_index, edge_attn2, batch_size, seq_len, num_nodes)
        
        return {
            'logits': logits,
            'probabilities': probabilities,
            'joint_attention': joint_attention,        # Shape: (batch_size, 25)
            'frame_attention': frame_attention,        # Shape: (batch_size, seq_len)
            'edge_attention': edge_attention,          # Shape: (batch_size, num_edges)
        }

    def forward_export(self, x: torch.Tensor) -> torch.Tensor:
        """Simplified forward pass for JIT script and ONNX export (no dict returns or PyG attention weights)."""
        batch_size, seq_len, num_nodes, num_features = x.shape
        x_proj = self.input_proj(x)
        flattened = x_proj.reshape(batch_size * seq_len * num_nodes, -1)
        
        edge_index = build_batched_edge_index(self.spatial_edge_index, batch_size * seq_len, num_nodes)
        
        spatial_out1, _ = self.spatial1(flattened, edge_index, return_attn=False)
        spatial_out2, _ = self.spatial2(spatial_out1, edge_index, return_attn=False)
        
        spatial_out = spatial_out2.reshape(batch_size, seq_len, num_nodes, -1).permute(0, 2, 3, 1)
        
        temporal_out = self.temporal1(spatial_out)
        temporal_out = self.temporal2(temporal_out)
        
        temporal_out, _ = self.temporal_attention(temporal_out, return_attn=False)
        
        pooled = temporal_out.mean(dim=3).mean(dim=1)
        logits = self.classifier(pooled)
        return logits

    def _aggregate_node_attention(
        self,
        edge_index: torch.Tensor,
        edge_attention: torch.Tensor,
        batch_size: int,
        seq_len: int,
        num_nodes: int
    ) -> torch.Tensor:
        dst = edge_index[1]  # Destination node indices
        
        # Accumulate edge attentions per node
        node_attention = torch.zeros((batch_size * seq_len * num_nodes,), dtype=edge_attention.dtype, device=edge_attention.device)
        node_attention = node_attention.scatter_add(0, dst, edge_attention)
        
        node_attention = node_attention.reshape(batch_size, seq_len, num_nodes)
        return node_attention.mean(dim=1)  # Average attention over time -> (batch_size, num_nodes)

def stgat_from_config(config: Optional[Dict] = None) -> STGAT:
    config = config or {}
    return STGAT(
        input_dim=config.get('input_dim', 3),
        hidden_dim=config.get('hidden_dim', 64),
        num_classes=config.get('num_classes', 2),
        heads=config.get('heads', 4),
        dropout=config.get('dropout', 0.2),
    )
