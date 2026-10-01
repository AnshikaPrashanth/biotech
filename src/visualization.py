from typing import Dict, List, Optional
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from src.graph import INTELLIREHAB_JOINTS, INTELLIREHAB_EDGES

def plot_3d_skeleton(
    joints: np.ndarray, 
    edges: Optional[List[tuple]] = None, 
    attention: Optional[Dict[str, float]] = None,
    show_labels: bool = False,
    title: str = "3D Skeleton Attention Layout"
) -> go.Figure:
    """Renders an upright 3D scatter and anatomical bone structure of the human skeleton,
    with GAT attention heat-mapping, prominent node markers, and full joint visibility.
    """
    if edges is None:
        edges = INTELLIREHAB_EDGES
        
    # IntelliRehabDS / Kinect coordinates:
    # joints[:, 0] is X (Lateral: Left to Right)
    # joints[:, 1] is Y (Vertical Height: SpineBase = 0, Feet = -0.98m, Head = +0.98m)
    # joints[:, 2] is Z (Depth: Forward / Backward distance)
    #
    # Plotly 3D Coordinate Mapping (Z is vertical UP):
    plot_x = joints[:, 0]  # Lateral (meters)
    plot_y = joints[:, 2]  # Depth (meters)
    plot_z = joints[:, 1]  # Height (meters, Feet at bottom, Head at top)
    
    fig = go.Figure()
    
    # 1. Bone segments (edges) - single combined trace for performance & clean depth sorting
    edge_x: List[Optional[float]] = []
    edge_y: List[Optional[float]] = []
    edge_z: List[Optional[float]] = []
    for start, end in edges:
        edge_x.extend([plot_x[start], plot_x[end], None])
        edge_y.extend([plot_y[start], plot_y[end], None])
        edge_z.extend([plot_z[start], plot_z[end], None])
        
    fig.add_trace(go.Scatter3d(
        x=edge_x, y=edge_y, z=edge_z,
        mode='lines',
        line=dict(color='rgba(100, 116, 139, 0.85)', width=6),
        hoverinfo='none',
        name='Skeletal Bones',
        showlegend=False
    ))
    
    # 2. Subtle ground reference circle beneath feet for depth perspective
    floor_z = float(np.min(plot_z) - 0.04)
    theta = np.linspace(0, 2 * np.pi, 48)
    ring_r = 0.45
    ring_x = ring_r * np.cos(theta)
    ring_y = ring_r * np.sin(theta)
    ring_z = np.full_like(ring_x, floor_z)
    fig.add_trace(go.Scatter3d(
        x=ring_x, y=ring_y, z=ring_z,
        mode='lines',
        line=dict(color='rgba(148, 163, 184, 0.35)', width=2, dash='dash'),
        hoverinfo='none',
        name='Floor Level',
        showlegend=False
    ))
    
    # 3. Node Colors & Sizes based on attention
    color_vals = []
    for i, joint_name in enumerate(INTELLIREHAB_JOINTS):
        val = attention.get(joint_name, attention.get(str(i), 0.0)) if attention else 0.5
        color_vals.append(float(val))
    
    color_arr = np.array(color_vals, dtype=np.float32)
    min_val = float(color_arr.min())
    max_val = float(color_arr.max())
    val_range = (max_val - min_val) if max_val > min_val else 1.0
    
    if attention is not None:
        # Scale marker sizes dynamically so high attention joints prominently stand out
        norm_vals = (color_arr - min_val) / val_range
        marker_sizes = (8 + 7 * norm_vals).tolist()
        marker_color = color_vals
        show_scale = True
    else:
        marker_sizes = [9] * 25
        marker_color = ['#0ea5e9'] * 25
        show_scale = False
        
    # Customdata for rich hover tooltip
    customdata = np.stack([
        INTELLIREHAB_JOINTS,
        [f"{i}" for i in range(25)],
        [f"{c:.4f}" for c in color_vals]
    ], axis=1)
    
    hovertemplate = (
        "<b>%{customdata[0]}</b> (Joint #%{customdata[1]})<br>"
        + ("Attention Weight: <b>%{customdata[2]}</b><br>" if attention is not None else "")
        + "Lateral X: %{x:.2f}m<br>"
        + "Height Z: %{z:.2f}m<br>"
        + "Depth Y: %{y:.2f}m<extra></extra>"
    )
    
    # Joint markers
    fig.add_trace(go.Scatter3d(
        x=plot_x, y=plot_y, z=plot_z,
        mode='markers+text' if show_labels else 'markers',
        marker=dict(
            size=marker_sizes, 
            color=marker_color, 
            colorscale='Plasma', 
            showscale=show_scale, 
            colorbar=dict(
                title=dict(text="Attention", font=dict(size=11)),
                thickness=12,
                len=0.65,
                x=0.92,
                tickfont=dict(size=10)
            ) if show_scale else None,
            line=dict(color='white', width=1.5),
            opacity=0.95
        ),
        text=INTELLIREHAB_JOINTS if show_labels else None,
        textposition='top right',
        textfont=dict(size=9, color='#1e293b'),
        customdata=customdata,
        hovertemplate=hovertemplate,
        name='Joints',
        showlegend=False
    ))
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=13, color="#334155"), x=0.03, y=0.96),
        scene=dict(
            xaxis=dict(
                title='Lateral X (m)', 
                showbackground=False, 
                gridcolor="rgba(203, 213, 225, 0.4)",
                zerolinecolor="rgba(148, 163, 184, 0.4)",
                nticks=5
            ),
            yaxis=dict(
                title='Depth Y (m)', 
                showbackground=False, 
                gridcolor="rgba(203, 213, 225, 0.4)",
                zerolinecolor="rgba(148, 163, 184, 0.4)",
                nticks=5
            ),
            zaxis=dict(
                title='Height Z (m)', 
                showbackground=False, 
                gridcolor="rgba(203, 213, 225, 0.4)",
                zerolinecolor="rgba(148, 163, 184, 0.4)",
                nticks=6
            ),
            aspectmode='data', # Crucial 1:1:1 geometric scaling!
            camera=dict(
                eye=dict(x=0.0, y=-2.4, z=0.1), # Direct frontal view at eye-level
                center=dict(x=0.0, y=0.0, z=0.0),
                up=dict(x=0, y=0, z=1)
            )
        ),
        margin=dict(l=0, r=0, t=30, b=0),
        height=500
    )
    return fig

def plot_attention_heatmap(attention: List[float], labels: List[str]) -> go.Figure:
    df = pd.DataFrame({'Joint': labels, 'Weight': attention})
    df = df.sort_values(by='Weight', ascending=False)
    fig = px.bar(
        df, x='Joint', y='Weight', 
        title='Joint Attention Weights (Explainability Profile)',
        color='Weight', color_continuous_scale='Plasma'
    )
    fig.update_layout(xaxis_tickangle=-45, template="plotly_white")
    return fig

def plot_temporal_attention(frames: List[int], values: List[float]) -> go.Figure:
    fig = px.line(
        x=frames, y=values, 
        labels={'x': 'Frame / Repetition Timestamp', 'y': 'Attention Weight'},
        title='Temporal Attention (Frame Significance over Sequence Time)'
    )
    fig.update_traces(line=dict(color="royalblue", width=2.5))
    fig.update_layout(template="plotly_white")
    return fig

def plot_confusion_matrix(matrix: np.ndarray, labels: List[str]) -> go.Figure:
    fig = go.Figure(data=go.Heatmap(
        z=matrix, x=labels, y=labels, 
        colorscale='Blues', showscale=True,
        text=matrix, texttemplate="%{text}", textfont={"size": 14}
    ))
    fig.update_layout(
        title='Confusion Matrix', 
        xaxis_title='Predicted Class', 
        yaxis_title='Actual Class',
        template="plotly_white"
    )
    return fig

def plot_rom_curve(angle_curves: Dict[str, np.ndarray]) -> go.Figure:
    """Plots Range of Motion curves across frames."""
    fig = go.Figure()
    for angle_name, curve in angle_curves.items():
        fig.add_trace(go.Scatter(y=curve, mode='lines', name=angle_name.replace('_', ' ').title()))
    fig.update_layout(
        title='Range of Motion (ROM) Joint Angular Signal', 
        xaxis_title='Frame index', 
        yaxis_title='Angle (degrees)',
        template="plotly_white"
    )
    return fig

def plot_weekly_trend(trends: List[Dict[str, object]]) -> go.Figure:
    """Plots patient weekly recovery progression trend graph."""
    if not trends:
        fig = go.Figure()
        fig.update_layout(title="No weekly data logged yet")
        return fig
    df = pd.DataFrame(trends)
    fig = px.line(
        df, x='week', y='average_confidence', 
        markers=True,
        title='Weekly Recovery Progression Score Trend',
        labels={'week': 'Week Year', 'average_confidence': 'Mean Confidence'}
    )
    fig.update_traces(line=dict(color="#10B981", width=3))
    fig.update_layout(yaxis_range=[0.0, 1.0], template="plotly_white")
    return fig

def plot_monthly_trend(trends: List[Dict[str, object]]) -> go.Figure:
    if not trends:
        fig = go.Figure()
        fig.update_layout(title="No monthly data logged yet")
        return fig
    df = pd.DataFrame(trends)
    fig = px.bar(
        df, x='month', y='average_confidence',
        title='Monthly Recovery Index',
        labels={'month': 'Month Year', 'average_confidence': 'Mean Confidence'},
        color='average_confidence', color_continuous_scale='Viridis'
    )
    fig.update_layout(yaxis_range=[0.0, 1.0], template="plotly_white")
    return fig

def plot_exercise_adherence_trend(adherence: List[Dict[str, object]]) -> go.Figure:
    if not adherence:
        fig = go.Figure()
        fig.update_layout(title="No exercises recorded")
        return fig
    df = pd.DataFrame(adherence)
    fig = px.pie(
        df, names='exercise_type', values='session_count',
        title='Exercise Adherence Profile (Completed Sessions Distribution)',
        hole=0.4
    )
    fig.update_layout(template="plotly_white")
    return fig
