import asyncio
import sys

# Fix for Python 3.13 on Windows: ProactorEventLoop causes WinError 10054
# with Streamlit/uvicorn pipe transport. Force SelectorEventLoop instead.
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import os
import json
import time
from pathlib import Path
from typing import Dict, List, Optional

import cv2
import numpy as np
import plotly.graph_objects as go
import streamlit as st
import torch
import pandas as pd

try:
    import mediapipe as mp
    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    HAS_MEDIAPIPE = True
except (ImportError, AttributeError):
    HAS_MEDIAPIPE = False
    mp_pose = None
    mp_drawing = None
    mp_drawing_styles = None

from config import CHECKPOINT_DIR, BASELINE_DIR, DB_PATH, TRAINING_CONFIG, DATA_DIR
from src.calibration import PersonalizedROMCalibrator, compute_joint_angles, smooth_angle_signal, interpolate_1d_curve
from src.database import SQLiteSessionDB
from src.dataset import (
    INTELLIREHAB_JOINTS, 
    convert_mediapipe_landmarks, 
    load_intellirehab_directory,
    extract_movement_label,
    parse_intellirehab_file
)
from src.model import STGAT, stgat_from_config
from src.utils import make_directory, load_checkpoint
from src.visualization import (
    plot_3d_skeleton, 
    plot_attention_heatmap, 
    plot_temporal_attention, 
    plot_rom_curve,
    plot_weekly_trend,
    plot_monthly_trend,
    plot_exercise_adherence_trend
)

MODEL_WEIGHTS_PATH = CHECKPOINT_DIR / 'best_model.pt'
BASELINE_FILE_PATH = BASELINE_DIR / 'rom_baselines.json'

@st.cache_resource
def load_model(weights_path: Path) -> STGAT:
    """Loads and caches the ST-GAT model weights."""
    config = {
        'hidden_dim': TRAINING_CONFIG['hidden_dim'],
        'heads': TRAINING_CONFIG['heads'],
        'dropout': 0.0
    }
    model = stgat_from_config(config)
    if weights_path.exists():
        try:
            checkpoint = torch.load(weights_path, map_location='cpu')
            state_dict = checkpoint.get('model_state', checkpoint)
            model.load_state_dict(state_dict, strict=False)
        except Exception:
            pass  # Weights load error handled at display time
    model.eval()
    return model

@st.cache_resource
def get_database(db_path: str) -> SQLiteSessionDB:
    """Creates and caches a single persistent DB connection."""
    return SQLiteSessionDB(db_path)

@st.cache_data(show_spinner=False)
def get_subjects_fast(data_dir: str) -> List[str]:
    """Instantly extracts subject IDs from filenames only — no file parsing.
    Subject ID is the leading digits before the first '_' in each filename.
    This replaces the 14-second full parse that was blocking the event loop.
    """
    import glob, re
    pattern = os.path.join(data_dir, '**', '*.txt')
    files = glob.glob(pattern, recursive=True)
    subjects: set = set()
    for f in files:
        m = re.match(r'^(\d+)_', os.path.basename(f))
        if m:
            subjects.add(m.group(1))
    return sorted(subjects)

@st.cache_data(show_spinner="Loading subject trials...")
def load_subject_entries(data_dir: str, subject_id: str) -> List[Dict]:
    """Parses only the files for a specific subject (used by calibration).
    Much faster than loading all 5185 files at startup.
    """
    import glob, re
    pattern = os.path.join(data_dir, '**', f'{subject_id}_*.txt')
    files = glob.glob(pattern, recursive=True)
    entries = []
    for fp in files:
        try:
            sequence, exercise_type, sid, movement_label = parse_intellirehab_file(fp)
            entries.append({
                'sequence': sequence,
                'exercise_type': exercise_type,
                'subject_id': sid,
                'movement_label': movement_label,
                'file_path': fp
            })
        except Exception:
            pass
    return entries

@st.cache_resource
def get_calibrator(baseline_path: Optional[str]) -> PersonalizedROMCalibrator:
    """Creates and caches the ROM calibrator."""
    return PersonalizedROMCalibrator(baseline_path=baseline_path)

def predict_sequence(model: STGAT, sequence: np.ndarray) -> Dict[str, object]:
    """Runs a 3D skeleton sequence through the model to obtain binary predictions and attention weights."""
    device = torch.device('cpu')
    tensor = torch.from_numpy(sequence[None, ...]).float().to(device)
    
    with torch.no_grad():
        outputs = model(tensor)
        
    logits = outputs['logits'][0].numpy()
    probs = outputs['probabilities'][0].numpy()
    pred_class = int(np.argmax(logits))
    confidence = float(probs[pred_class])
    
    joint_attn = outputs['joint_attention'][0].numpy()
    frame_attn = outputs['frame_attention'][0].numpy()
    
    joint_attention_map = {
        INTELLIREHAB_JOINTS[i]: float(joint_attn[i]) 
        for i in range(len(INTELLIREHAB_JOINTS))
    }
    
    return {
        'verdict': "Compensated" if pred_class == 1 else "Healthy",
        'confidence': confidence,
        'joint_attention': joint_attention_map,
        'frame_attention': frame_attn.tolist()
    }

def main() -> None:
    st.set_page_config(page_title='Adaptive ST-GAT Rehabilitation Dashboard', layout='wide', page_icon="🧬")
    st.title('🧬 Adaptive Spatial-Temporal Graph Attention Rehab Assessment')
    st.markdown("Clinical-grade end-to-end framework for personalized movement quality prediction, Range of Motion calibration, and temporal explainability.")

    make_directory(str(BASELINE_DIR))
    make_directory(str(CHECKPOINT_DIR))
    
    # DB Instance (cached - single connection across reruns)
    db = get_database(str(DB_PATH))

    # Load model (cached)
    model = load_model(MODEL_WEIGHTS_PATH)

    # Model load status
    if MODEL_WEIGHTS_PATH.exists():
        st.sidebar.success("✅ Model weights loaded")
    else:
        st.sidebar.warning("⚠️ No model weights — using random init")

    # Get subjects instantly from filenames (no file parsing, ~instant)
    if DATA_DIR.exists():
        subjects = get_subjects_fast(str(DATA_DIR))
        if not subjects:
            subjects = ["101", "102", "103", "104", "105"]
    else:
        subjects = ["101", "102", "103", "104", "105"]

    # Initialize Calibrator (cached)
    baseline_path = str(BASELINE_FILE_PATH) if BASELINE_FILE_PATH.exists() else None
    calibrator = get_calibrator(baseline_path)
        
    # Sidebar
    st.sidebar.header('🧬 Biotech Rehab System')
    
    active_mode = st.sidebar.selectbox(
        "Navigation Mode", 
        ["Movement Quality Assessment", "Patient Calibration Manager", "Clinical Progression Dashboard"]
    )
    
    selected_subject = st.sidebar.selectbox("Active Patient ID", subjects)
    selected_exercise = st.sidebar.selectbox("Exercise Type", ["Stand", "Chair", "Wheelchair"])
    
    # Toggle ROM Tolerance
    tolerance_scale = st.sidebar.slider('Personalized ROM Tolerance Scale', 0.5, 2.0, 1.0, step=0.1)
    if selected_subject in calibrator.baselines:
        calibrator.update_tolerance(selected_subject, tolerance_scale)

    # 1. MOVEMENT ASSESSMENT MODE
    if active_mode == "Movement Quality Assessment":
        st.subheader("📊 Session Assessment & Video Analysis")
        
        if not HAS_MEDIAPIPE:
            session_type = st.radio("Input Source", ["Static File Upload"], horizontal=True)
            st.warning("⚠️ MediaPipe is not installed or unavailable in this environment. Live Webcam Capture is disabled. Please upload a static trial file instead.")
        else:
            session_type = st.radio("Input Source", ["Static File Upload", "Live Webcam Capture"], horizontal=True)
        
        sequence_data = None
        exercise_detected = selected_exercise
        subj_detected = selected_subject
        
        if session_type == "Static File Upload":
            uploaded = st.file_uploader('Upload IntelliRehabDS Trial file (.txt)', type=['txt'])
            if uploaded:
                temp_path = Path(uploaded.name)
                with open(temp_path, "wb") as f:
                    f.write(uploaded.getbuffer())
                
                try:
                    sequence_data, exercise_detected, subj_detected, _ = parse_intellirehab_file(str(temp_path))
                    st.success(f"Successfully loaded file. Patient: {subj_detected} | Exercise: {exercise_detected} | Frame Count: {sequence_data.shape[0]}")
                except Exception as e:
                    st.error(f"Error parsing uploaded file: {e}")
                finally:
                    if temp_path.exists():
                        temp_path.unlink()
                    
        else: # Live Webcam Capture
            st.info("Ensure you are in a well-lit area. Press 'Start Webcam' to capture a 60-frame movement sequence.")
            run_cam = st.checkbox("Start Webcam Capture Stream")
            st_frame = st.empty()
            
            if run_cam:
                cap = cv2.VideoCapture(0)
                pose_engine = mp_pose.Pose(
                    static_image_mode=False,
                    model_complexity=1,
                    smooth_landmarks=True,
                    min_detection_confidence=0.5,
                    min_tracking_confidence=0.5
                )
                
                sequence_buf = []
                smoothed_frame = None
                pbar = st.progress(0)
                
                while cap.isOpened() and run_cam and len(sequence_buf) < 60:
                    ret, frame = cap.read()
                    if not ret:
                        break
                    
                    # Flip frame horizontally for natural view
                    frame = cv2.flip(frame, 1)
                    h, w, c = frame.shape
                    
                    # Process frame
                    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    results = pose_engine.process(rgb_frame)
                    
                    # Overlay skeleton drawing using OpenCV
                    if results.pose_landmarks:
                        mp_drawing.draw_landmarks(
                            frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                            mp_drawing_styles.get_default_pose_landmarks_style()
                        )
                        
                        # Add landmarks to buffer
                        landmarks = np.array([[lm.x, lm.y, lm.z] for lm in results.pose_world_landmarks.landmark], dtype=np.float32)
                        joint_coords = convert_mediapipe_landmarks(landmarks)
                        
                        # Apply smoothing filter
                        if smoothed_frame is None:
                            smoothed_frame = joint_coords
                        else:
                            smoothed_frame = 0.7 * smoothed_frame + 0.3 * joint_coords
                        
                        sequence_buf.append(smoothed_frame.copy())
                        
                    # Display webcam frame
                    st_frame.image(frame, channels="BGR", use_container_width=True)
                    pbar.progress(len(sequence_buf) / 60)
                    time.sleep(0.03) # Cap at ~30 FPS
                    
                cap.release()
                pose_engine.close()
                st.success("Webcam sequence capture complete!")
                
                if len(sequence_buf) == 60:
                    raw_seq = np.stack(sequence_buf, axis=0)
                    # Normalize
                    from src.dataset import normalize_pelvis_centered
                    sequence_data = normalize_pelvis_centered(raw_seq)
        
        # Analyze Sequence if available
        if sequence_data is not None:
            # Model prediction
            results = predict_sequence(model, sequence_data)
            
            # Calibration evaluation
            calibration_eval = {}
            if subj_detected in calibrator.baselines:
                calibration_eval = calibrator.evaluate(subj_detected, sequence_data)
            
            # Layout Columns
            col1, col2 = st.columns([1, 1])
            with col1:
                st.subheader("🧬 3D Skeleton Reconstruction")
                # Colors joint by GAT attention weights
                fig_sk = plot_3d_skeleton(sequence_data[0], attention=results['joint_attention'])
                st.plotly_chart(fig_sk, use_container_width=True)
                
            with col2:
                st.subheader("🩺 ST-GAT Classification Verdict")
                
                # Dynamic visual feedback card
                bg_color = "#e8f5e9" if results['verdict'] == "Healthy" else "#ffebee"
                text_color = "#2e7d32" if results['verdict'] == "Healthy" else "#c62828"
                
                st.markdown(f"""
                <div style="background-color: {bg_color}; padding: 20px; border-radius: 10px; border: 2px solid {text_color}; text-align: center;">
                    <h3 style="color: {text_color}; margin: 0;">Predicted Verdict: {results['verdict']}</h3>
                    <h4 style="color: {text_color}; margin: 10px 0 0 0;">Confidence Score: {results['confidence']:.2%}</h4>
                </div>
                """, unsafe_allow_html=True)
                
                # Calibration deviations
                if calibration_eval:
                    st.markdown("### 📏 ROM Joint Deviations")
                    st.write(f"Calibration Template Confidence: **{calibration_eval['confidence']:.2%}**")
                    st.write(f"Patient Progression Index: **{calibration_eval['progression_score']:.2%}**")
                    
                    err_df = pd.DataFrame(calibration_eval['top_error_joints'], columns=['Joint Angle', 'DTW Mean Error'])
                    st.markdown("**Top Joint Deviations (Anatomical Errors):**")
                    st.table(err_df)
                else:
                    st.warning(f"No Calibration ROM template fitted for subject {subj_detected}. Visit Calibration Manager first.")
                    
                # Save session logs to database
                if st.button("📝 Log Rehab Session to Patient History"):
                    rom_devs = calibration_eval.get('joint_errors', {}) if calibration_eval else None
                    db.log_session(
                        subject_id=subj_detected,
                        exercise_type=exercise_detected,
                        confidence=results['confidence'] if results['verdict'] == "Healthy" else 1.0 - results['confidence'],
                        verdict=results['verdict'],
                        attention_map=results['joint_attention'],
                        rom_deviation=rom_devs,
                        session_duration=float(sequence_data.shape[0] / 30.0), # seconds at 30fps
                        notes="Uploaded skeleton analysis log"
                    )
                    st.success("Session logged successfully!")
                    
            # Bottom explainability charts
            st.markdown("---")
            st.subheader("🔍 Attention Explainability Profiling")
            
            ex_col1, ex_col2 = st.columns([1, 1])
            with ex_col1:
                # Joint attention bar chart
                fig_attn = plot_attention_heatmap(list(results['joint_attention'].values()), list(results['joint_attention'].keys()))
                st.plotly_chart(fig_attn, use_container_width=True)
            with ex_col2:
                # Temporal attention line chart
                frames = list(range(len(results['frame_attention'])))
                fig_temp = plot_temporal_attention(frames, results['frame_attention'])
                st.plotly_chart(fig_temp, use_container_width=True)
                
            # ROM angles curve plotting
            st.subheader("📈 Angle Range of Motion Trajectories")
            angles = compute_joint_angles(sequence_data)
            fig_rom = plot_rom_curve(angles)
            st.plotly_chart(fig_rom, use_container_width=True)

    # 2. CALIBRATION MANAGER MODE
    elif active_mode == "Patient Calibration Manager":
        st.subheader("📐 Personalized Range of Motion Calibration Manager")
        st.markdown("Fitted ROM baselines eliminate hardcoded thresholds by capturing the subject's unique baseline from healthy trials.")
        
        # Display baseline template details if it exists
        if selected_subject in calibrator.baselines:
            st.success(f"Fitted Baseline template exists for Patient {selected_subject}!")
            baseline = calibrator.baselines[selected_subject]
            
            st.markdown("### Existing Fitted ROM Baselines (Mean Template Curve)")
            # Plot the fitted templates
            fig_base = plot_rom_curve(baseline.baseline_angles)
            st.plotly_chart(fig_base, use_container_width=True)
            
            st.markdown("### Fitted Tolerances (Standard Deviation Thresholds)")
            st.json(baseline.tolerance)
        else:
            st.warning(f"No ROM baseline fitted for Patient {selected_subject} yet.")
            
        st.markdown("---")
        st.subheader("🆕 Calibrate Patient Baseline")
        
        # Load only THIS subject's trials (lazy, on-demand — not all 5185 files)
        if DATA_DIR.exists():
            subject_entries = load_subject_entries(str(DATA_DIR), selected_subject)
            subject_healthy_trials = [
                e for e in subject_entries
                if e['movement_label'] == 0
            ]
        else:
            subject_healthy_trials = []

        st.write(f"Found **{len(subject_healthy_trials)}** healthy trials for subject **{selected_subject}** in the RawData dataset directory.")

        if len(subject_healthy_trials) < 2:
            st.warning("At least 2 healthy trials are recommended in the raw dataset directory to build a robust template.")

        if st.button("🧬 Run Calibration Optimization"):
            if not subject_healthy_trials:
                st.error("No healthy trials found to fit a template. Make sure raw data includes subject files.")
            else:
                with st.spinner("Aligning sequences using DTW and smoothing with Savitzky-Golay..."):
                    sequences_pool = [e['sequence'] for e in subject_healthy_trials]
                    calibrator.fit(selected_subject, sequences_pool)
                    calibrator.save(str(BASELINE_FILE_PATH))
                st.success(f"Fitted patient {selected_subject} baseline calibration successfully and saved to disk!")
                if hasattr(st, "rerun"):
                    st.rerun()
                else:
                    st.experimental_rerun()

    # 3. CLINICAL PROGRESSION MODE
    elif active_mode == "Clinical Progression Dashboard":
        st.subheader("📈 Patient Recovery & Compliance Dashboard")
        
        # Pull DB metrics
        latest_sessions = db.fetch_latest(10)
        weekly = db.get_weekly_trends(selected_subject)
        monthly = db.get_monthly_trends(selected_subject)
        adherence = db.get_exercise_adherence(selected_subject)
        improvement = db.get_best_improvement(selected_subject)
        
        # Metric cards
        st.markdown("### 🏆 Recovery Progress Indexes")
        mcol1, mcol2, mcol3 = st.columns(3)
        with mcol1:
            st.metric("Total Rehab Sessions Completed", len(db.fetch_latest(100)))
        with mcol2:
            if improvement.get('sessions_tracked', 0) >= 2:
                st.metric("Patient Recovery Improvement Index", f"{improvement['improvement']:.1%}", delta=f"{improvement['improvement'] * 100:.1f}%")
            else:
                st.metric("Patient Recovery Improvement Index", "Insufficient sessions", help="At least 2 sessions are needed to calculate progress.")
        with mcol3:
            st.metric("Avg Session Adherence Duration", f"{np.mean([x.get('session_duration', 0) for x in latest_sessions]):.1f} sec" if latest_sessions else "0 sec")
            
        # Graphs
        st.markdown("---")
        gcol1, gcol2 = st.columns([1, 1])
        with gcol1:
            st.subheader("Weekly Calibration Progression Trend")
            fig_week = plot_weekly_trend(weekly)
            st.plotly_chart(fig_week, use_container_width=True)
        with gcol2:
            st.subheader("Monthly Calibration Index")
            fig_month = plot_monthly_trend(monthly)
            st.plotly_chart(fig_month, use_container_width=True)
            
        st.markdown("---")
        st.subheader("🍕 Exercise Compliance & Adherence Profile")
        fig_pie = plot_exercise_adherence_trend(adherence)
        st.plotly_chart(fig_pie, use_container_width=True)
        
        st.markdown("---")
        st.subheader("📝 Latest Evaluated Sessions Logs")
        if latest_sessions:
            log_df = pd.DataFrame(latest_sessions)[['timestamp', 'subject_id', 'exercise_type', 'confidence', 'verdict', 'session_duration']]
            st.table(log_df)
        else:
            st.info("No recorded sessions found in the database. Evaluate movements to add logs.")
            
    # Note: db connection is cached and managed by Streamlit's cache_resource
    # Do NOT call db.close() here — it would break on the next rerun

if __name__ == '__main__':
    main()
