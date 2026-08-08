import torch
import networkx as nx
from typing import List, Tuple

# Kinect v2 / IntelliRehabDS 25 joints in order
INTELLIREHAB_JOINTS = [
    'SpineBase',       # 0
    'SpineMid',        # 1
    'Neck',            # 2
    'Head',            # 3
    'ShoulderLeft',    # 4
    'ElbowLeft',       # 5
    'WristLeft',       # 6
    'HandLeft',        # 7
    'ShoulderRight',   # 8
    'ElbowRight',      # 9
    'WristRight',      # 10
    'HandRight',       # 11
    'HipLeft',         # 12
    'KneeLeft',        # 13
    'AnkleLeft',       # 14
    'FootLeft',        # 15
    'HipRight',        # 16
    'KneeRight',       # 17
    'AnkleRight',      # 18
    'FootRight',       # 19
    'SpineShoulder',   # 20
    'HandTipLeft',     # 21
    'ThumbLeft',       # 22
    'HandTipRight',    # 23
    'ThumbRight'       # 24
]

# Cleaned up anatomical edge connections (correcting hand connectivity)
INTELLIREHAB_EDGES = [
    # Spine and head
    (0, 1),      # SpineBase -> SpineMid
    (1, 20),     # SpineMid -> SpineShoulder
    (20, 2),     # SpineShoulder -> Neck
    (2, 3),      # Neck -> Head
    
    # Left Arm
    (20, 4),     # SpineShoulder -> ShoulderLeft
    (4, 5),      # ShoulderLeft -> ElbowLeft
    (5, 6),      # ElbowLeft -> WristLeft
    (6, 7),      # WristLeft -> HandLeft
    (7, 21),     # HandLeft -> HandTipLeft
    (6, 22),     # WristLeft -> ThumbLeft
    
    # Right Arm
    (20, 8),     # SpineShoulder -> ShoulderRight
    (8, 9),      # ShoulderRight -> ElbowRight
    (9, 10),     # ElbowRight -> WristRight
    (10, 11),    # WristRight -> HandRight
    (11, 23),    # HandRight -> HandTipRight
    (10, 24),    # WristRight -> ThumbRight
    
    # Left Leg
    (0, 12),     # SpineBase -> HipLeft
    (12, 13),    # HipLeft -> KneeLeft
    (13, 14),    # KneeLeft -> AnkleLeft
    (14, 15),    # AnkleLeft -> FootLeft
    
    # Right Leg
    (0, 16),     # SpineBase -> HipRight
    (16, 17),    # HipRight -> KneeRight
    (17, 18),    # KneeRight -> AnkleRight
    (18, 19),    # AnkleRight -> FootRight
]

def get_edge_index() -> torch.Tensor:
    """Returns the bidirectionally connected spatial graph edge index for PyTorch Geometric GATConv."""
    edges = []
    for u, v in INTELLIREHAB_EDGES:
        edges.append([u, v])
        edges.append([v, u]) # Bidirectional message passing
    return torch.tensor(edges, dtype=torch.long).t().contiguous()

def build_networkx_graph() -> nx.Graph:
    """Constructs a NetworkX graph object of the human skeleton structure."""
    g = nx.Graph()
    for i, joint in enumerate(INTELLIREHAB_JOINTS):
        g.add_node(i, name=joint)
    g.add_edges_from(INTELLIREHAB_EDGES)
    return g

def build_batched_edge_index(edge_index: torch.Tensor, batch_size_seq_len: int, num_nodes: int = 25) -> torch.Tensor:
    """Repeats spatial graph edges across batch elements and frames for efficient execution."""
    device = edge_index.device
    num_edges = edge_index.size(1)
    
    # Create offset for each batch * frame
    offsets = torch.arange(batch_size_seq_len, device=device).repeat_interleave(num_edges)
    
    # Offset the edge indices
    batched_edges = edge_index.repeat(1, batch_size_seq_len) + offsets.unsqueeze(0) * num_nodes
    return batched_edges
