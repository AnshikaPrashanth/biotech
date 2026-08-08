from typing import Dict, List, Optional
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from src.graph import INTELLIREHAB_JOINTS, INTELLIREHAB_EDGES

def plot_3d_skeleton(
    joints: np.ndarray, 
    edges: Optional[List[tuple]] = None, 
    attention: Optional[Dict[str, float]] = None
) -> go.Figure:
    """Renders a 3D scatter plot of the human skeleton with optional attention-based node highlighting."""
    if edges is None:
        edges = INTELLIREHAB_EDGES
        
    x, y, z = joints[:, 0], joints[:, 1], joints[:, 2]
    fig = go.Figure()
    
    # Node Colors
    if attention is not None:
        # attention maps joint names or indices to weights
        color_vals = []
        for i, joint_name in enumerate(INTELLIREHAB_JOINTS):
            val = attention.get(joint_name, attention.get(str(i), 0.0))
            color_vals.append(val)
        marker_color = color_vals
        show_scale = True
    else:
        marker_color = 'green'
        show_scale = False
        
    # Scatter plot for joints (nodes)
    fig.add_trace(go.Scatter3d(
        x=x, y=y, z=z,
        mode='markers+text',
        marker=dict(
            size=6, 
            color=marker_color, 
            colorscale='Viridis', 
            showscale=show_scale, 
            colorbar=dict(title="Attention", x=0.85) if show_scale else None,
            line=dict(color='darkblue', width=1)
        ),
        text=INTELLIREHAB_JOINTS,
        textposition='top center',
        name='Joints'
    ))
    
    # Line segments (edges)
    for start, end in edges:
        fig.add_trace(go.Scatter3d(
            x=[x[start], x[end]],
            y=[y[start], y[end]],
            z=[z[start], z[end]],
            mode='lines',
            line=dict(color='rgba(120, 120, 120, 0.8)', width=4),
            showlegend=False
        ))
        
    fig.update_layout(
        scene=dict(
            xaxis=dict(title='X (meters)', backgroundcolor="rgb(200, 200, 230)", gridcolor="white", showbackground=True),
            yaxis=dict(title='Y (meters)', backgroundcolor="rgb(230, 200, 230)", gridcolor="white", showbackground=True),
            zaxis=dict(title='Z (meters)', backgroundcolor="rgb(230, 230, 200)", gridcolor="white", showbackground=True),
        ),
        margin=dict(l=0, r=0, t=10, b=0),
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
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
