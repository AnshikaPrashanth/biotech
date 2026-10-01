import asyncio
import sys

# Fix for Python 3.13 on Windows: ProactorEventLoop causes WinError 10054
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import os
import json
import time
import tempfile
from pathlib import Path
from typing import Dict, List, Optional

import cv2
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import torch

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

from config import CHECKPOINT_DIR, BASELINE_DIR, DB_PATH, TRAINING_CONFIG, DATA_DIR, GLOBAL_CONFIG
from src.calibration import PersonalizedROMCalibrator, compute_joint_angles
from src.database import SQLiteSessionDB
from src.dataset import (
    INTELLIREHAB_JOINTS, 
    parse_intellirehab_file
)
from src.model import STGAT, stgat_from_config
from src.utils import make_directory
from src.visualization import (
    plot_3d_skeleton, 
    plot_attention_heatmap, 
    plot_temporal_attention, 
    plot_rom_curve,
    plot_weekly_trend,
    plot_monthly_trend,
    plot_exercise_adherence_trend
)
from src.skeleton_pipeline import canonicalize_skeleton
from src.video_to_skeleton import extract_skeleton_from_video, generate_video_overlay
from src.webcam_pose import WebcamPoseStreamer
from src.analysis_pipeline import analyze_sequence
from src.report_generator import RehabReportGenerator

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
            pass
    model.eval()
    return model

@st.cache_resource
def get_database(db_path: str) -> SQLiteSessionDB:
    """Creates and caches a single persistent DB connection."""
    return SQLiteSessionDB(db_path)

@st.cache_data(show_spinner=False)
def get_subjects_fast(data_dir: str) -> List[str]:
    """Instantly extracts subject IDs from filenames only."""
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
    """Parses only the files for a specific subject (used by calibration)."""
    import glob
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

def main() -> None:
    st.set_page_config(page_title='Rehab Assessment & Biofeedback System', layout='wide', page_icon="🧬")
    st.title('🧬 Explainable Rehabilitation & Movement Assessment Framework')
    st.markdown("Clinical-grade assessment dashboard featuring video translation, real-time webcam feedback, ROM calibration, and biomechanical error attribution.")

    make_directory(str(BASELINE_DIR))
    make_directory(str(CHECKPOINT_DIR))
    
    db = get_database(str(DB_PATH))
    model = load_model(MODEL_WEIGHTS_PATH)

    if MODEL_WEIGHTS_PATH.exists():
        st.sidebar.success("✅ Model weights loaded")
    else:
        st.sidebar.warning("⚠️ No model weights — using random init")

    if DATA_DIR.exists():
        subjects = get_subjects_fast(str(DATA_DIR))
        if not subjects:
            subjects = ["101", "102", "103", "104", "105"]
    else:
        subjects = ["101", "102", "103", "104", "105"]

    baseline_path = str(BASELINE_FILE_PATH) if BASELINE_FILE_PATH.exists() else None
    calibrator = get_calibrator(baseline_path)
        
    st.sidebar.header('🧬 Config & Patient Selection')
    
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
        
        # Tabs for different inputs
        tab_txt, tab_video, tab_webcam = st.tabs(["TXT / Skeleton File", "Upload Video", "Live Webcam"])
        
        sequence_data = None
        source_type = "txt"
        exercise_detected = selected_exercise
        subj_detected = selected_subject
        video_overlay_path = None
        
        # --- TAB 1: TXT FILE UPLOAD ---
        with tab_txt:
            uploaded_txt = st.file_uploader('Upload IntelliRehabDS Trial file (.txt)', type=['txt'], key='uploader_txt')
            if uploaded_txt:
                with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as temp_file:
                    temp_file.write(uploaded_txt.getbuffer())
                    temp_path = Path(temp_file.name)
                
                try:
                    sequence_data, exercise_detected, subj_detected, _ = parse_intellirehab_file(str(temp_path))
                    source_type = "txt"
                    st.success(f"Loaded trial file. Patient: {subj_detected} | Exercise: {exercise_detected} | Frames: {sequence_data.shape[0]}")
                except Exception as e:
                    st.error(f"Error parsing file: {e}")
                finally:
                    if temp_path.exists():
                        temp_path.unlink()
                        
        # --- TAB 2: UPLOAD VIDEO ---
        with tab_video:
            if not HAS_MEDIAPIPE:
                st.warning("⚠️ MediaPipe is not installed. Video processing is disabled.")
            else:
                uploaded_vid = st.file_uploader('Upload movement video (.mp4, .avi, .mov)', type=['mp4', 'avi', 'mov'], key='uploader_vid')
                if uploaded_vid:
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_file:
                        temp_file.write(uploaded_vid.getbuffer())
                        temp_path = Path(temp_file.name)
                    
                    with st.spinner("Extracting 3D skeleton joints using MediaPipe Pose..."):
                        try:
                            # Run video pose extraction
                            raw_lm, canonical_seq, meta_summary = extract_skeleton_from_video(
                                video_path=str(temp_path),
                                subject_id=selected_subject,
                                exercise_type=selected_exercise,
                                export_txt=True
                            )
                            sequence_data = canonical_seq
                            source_type = "video"
                            subj_detected = selected_subject
                            exercise_detected = selected_exercise
                            
                            # Render skeleton overlay side-by-side video
                            video_overlay_path = f"results/video/{selected_subject}_{selected_exercise}_overlay.mp4"
                            generate_video_overlay(str(temp_path), raw_lm, canonical_seq, video_overlay_path)
                            st.success(f"Video skeleton tracking complete! Detection success rate: {meta_summary['detection_success_rate']:.1%}")
                        except Exception as e:
                            st.error(f"Failed to process video: {e}")
                        finally:
                            if temp_path.exists():
                                temp_path.unlink()

                    if video_overlay_path and os.path.exists(video_overlay_path):
                        st.markdown("### Processed Video Skeleton Overlay")
                        st.video(video_overlay_path)

        # --- TAB 3: LIVE WEBCAM ---
        with tab_webcam:
            if not HAS_MEDIAPIPE:
                st.warning("⚠️ MediaPipe is not installed. Webcam capture is disabled.")
            else:
                st.info("Press 'Start Webcam' to capture a live sequence. Keep your full body in view.")
                run_cam = st.checkbox("Start Live Webcam Feed", key='webcam_check')
                st_frame = st.empty()
                st_metrics_webcam = st.empty()
                
                if run_cam:
                    cap = cv2.VideoCapture(0)
                    if not cap.isOpened():
                        st.error("Cannot access camera.")
                    else:
                        streamer = WebcamPoseStreamer(sequence_length=64, inference_interval=5)
                        try:
                            while cap.isOpened() and run_cam:
                                ret, frame = cap.read()
                                if not ret:
                                    break
                                # Mirror frame
                                frame = cv2.flip(frame, 1)
                                frame, inf_seq, status_str = streamer.process_frame(frame)
                                
                                # Render live frame in Streamlit
                                st_frame.image(frame, channels="BGR")
                                st_metrics_webcam.write(f"**Status:** {status_str} | **FPS:** {streamer.fps:.1f} | **Buffer:** {len(streamer.raw_buffer)}/64")
                                
                                if inf_seq is not None:
                                    # Cache latest sequence in session state to show results below stream
                                    st.session_state["latest_webcam_sequence"] = inf_seq
                                time.sleep(0.01)
                        finally:
                            cap.release()
                            streamer.close()
                            
                if "latest_webcam_sequence" in st.session_state:
                    if st.button("Use Captured Webcam Sequence"):
                        sequence_data = st.session_state["latest_webcam_sequence"]
                        source_type = "webcam"
                        subj_detected = selected_subject
                        exercise_detected = selected_exercise

        # --- UNIFIED REPORTING & ANALYSIS ---
        if sequence_data is not None:
            # Run the unified analysis pipeline
            metadata = {
                "subject_id": subj_detected,
                "exercise_type": exercise_detected,
                "source_type": source_type
            }
            with st.spinner("Executing unified rehabilitation assessment pipeline..."):
                report = analyze_sequence(
                    sequence=sequence_data,
                    metadata=metadata,
                    model=model,
                    calibrator=calibrator,
                    db=db,
                    device=torch.device('cpu'),
                    config_dict=GLOBAL_CONFIG
                )
            
            st.markdown("---")
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.subheader("🧬 3D Skeleton Attention Layout")
                num_frames = len(sequence_data)
                peak_frame = 0
                if 'frame_attention' in report['attention'] and report['attention']['frame_attention']:
                    peak_frame = int(np.argmax(report['attention']['frame_attention']))
                    peak_frame = min(peak_frame, num_frames - 1)
                
                if num_frames > 1:
                    sk_col_a, sk_col_b = st.columns([3, 2])
                    with sk_col_a:
                        selected_frame = st.slider(
                            "Skeleton Frame Index", 
                            0, num_frames - 1, value=peak_frame,
                            help="Scrub through movement frames. Default is set to the peak temporal attention frame."
                        )
                    with sk_col_b:
                        show_labels = st.checkbox("Show Joint Tags", value=False, help="Toggle 3D text labels on all 25 joints.")
                else:
                    selected_frame = 0
                    show_labels = st.checkbox("Show Joint Tags", value=False, help="Toggle 3D text labels on all 25 joints.")
                    
                fig_sk = plot_3d_skeleton(
                    sequence_data[selected_frame], 
                    attention=report['attention']['joint_attention'],
                    show_labels=show_labels,
                    title=f"3D Skeleton (Frame {selected_frame} of {num_frames - 1})"
                )
                st.plotly_chart(fig_sk, use_container_width=True)
                
            with col2:
                st.subheader("🩺 Session Analysis Report")
                
                # Colors for decision card
                verdict = report['prediction']['verdict']
                if verdict == "Healthy":
                    bg_color, border_color = "#e8f5e9", "#2e7d32"
                elif verdict == "Compensated":
                    bg_color, border_color = "#ffebee", "#c62828"
                else:
                    bg_color, border_color = "#fffde7", "#f57f17"  # Yellow for Uncertain
                    
                st.markdown(f"""
                <div style="background-color: {bg_color}; padding: 20px; border-radius: 10px; border: 2px solid {border_color}; text-align: center; margin-bottom: 20px;">
                    <h3 style="color: {border_color}; margin: 0;">Verdict: {verdict}</h3>
                    <h4 style="color: {border_color}; margin: 10px 0 0 0;">Confidence: {report['prediction']['confidence']:.2%}</h4>
                    <p style="color: #666; margin: 5px 0 0 0;">Uncertainty Index: {report['uncertainty']['uncertainty_score']:.3f}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Movement Quality Score
                st.markdown(f"### 🏆 Movement Quality Score: **{report['movement_quality']['score']:.1f}/100**")
                comp = report['movement_quality']['components']
                st.write(f"ROM Conformity: {comp['rom']:.1f}% | Symmetry: {comp['symmetry']:.1f}% | Smoothness: {comp['temporal']:.1f}%")
                
                # Joint Deviations
                st.markdown("### 📏 Top Biomechanical Joint Deviations")
                top_err_list = report['error_attribution']['top_error_joints'][:4]
                err_rows = []
                for joint, score in top_err_list:
                    det = report['error_attribution']['joint_error_details'][joint]
                    err_rows.append({
                        "Joint": joint,
                        "Error Score": f"{score:.2f}",
                        "ROM Dev": f"{det['rom_deviation']:.2f}",
                        "Asymmetry": f"{det['symmetry_deviation']:.2f}",
                        "Attention": f"{det['attention_contribution']:.2f}"
                    })
                st.table(pd.DataFrame(err_rows))
                
                # Clinical Feedback
                st.markdown("### 🩺 AI-Assisted Exercise Feedback")
                for f in report['feedback']:
                    st.info(f"💡 {f}")

                # Save / Export Actions
                st.markdown("### Report Export Actions")
                rep_gen = RehabReportGenerator()
                
                json_path = f"results/{subj_detected}_rehab_report.json"
                md_path = f"results/{subj_detected}_rehab_report.md"
                
                rep_gen.generate_json_report(report, json_path)
                rep_gen.generate_markdown_report(report, md_path)
                
                with open(json_path, 'r') as j_f:
                    st.download_button("Download JSON Report", j_f.read(), file_name=f"{subj_detected}_rehab_report.json")
                with open(md_path, 'r') as m_f:
                    st.download_button("Download Markdown Report", m_f.read(), file_name=f"{subj_detected}_rehab_report.md")

                # Baseline update status
                if report['baseline_adaptation']['baseline_updated']:
                    st.success("🔄 Personalized ROM baseline successfully updated based on healthy movement execution!")
                
            # Explainability Charts
            st.markdown("---")
            st.subheader("🔍 Attention Explainability Profiling")
            ex_col1, ex_col2 = st.columns([1, 1])
            with ex_col1:
                fig_attn = plot_attention_heatmap(list(report['attention']['joint_attention'].values()), list(report['attention']['joint_attention'].keys()))
                st.plotly_chart(fig_attn, use_container_width=True)
            with ex_col2:
                frames = list(range(len(report['attention']['frame_attention'])))
                fig_temp = plot_temporal_attention(frames, report['attention']['frame_attention'])
                st.plotly_chart(fig_temp, use_container_width=True)
                
            # ROM Trajectories
            st.subheader("📈 Range of Motion Trajectories")
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
            fig_base = plot_rom_curve(baseline.baseline_angles)
            st.plotly_chart(fig_base, use_container_width=True)
            
            st.markdown("### Fitted Tolerances (Standard Deviation Thresholds)")
            st.json(baseline.tolerance)
            
            # Rollback mechanism
            if hasattr(baseline, 'history') and baseline.history:
                st.markdown("### Baseline Adaptation History")
                st.write(f"Found {len(baseline.history)} adaptive baseline updates.")
                if st.button("Rollback to Previous Baseline Version"):
                    prev_ver = baseline.history.pop()
                    baseline.baseline_angles = {k: np.array(v, dtype=np.float32) for k, v in prev_ver["angles"].items()}
                    baseline.tolerance = prev_ver["tolerance"]
                    calibrator.save(str(BASELINE_FILE_PATH))
                    st.success("Reverted baseline to the previous saved version.")
                    st.rerun()
        else:
            st.warning(f"No ROM baseline fitted for Patient {selected_subject} yet.")
            
        st.markdown("---")
        st.subheader("🆕 Calibrate Patient Baseline")
        
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
                with st.spinner("Aligning sequences using DTW and smoothing..."):
                    sequences_pool = [e['sequence'] for e in subject_healthy_trials]
                    calibrator.fit(selected_subject, sequences_pool)
                    calibrator.save(str(BASELINE_FILE_PATH))
                st.success(f"Fitted patient {selected_subject} baseline calibration successfully and saved to disk!")
                st.rerun()

    # 3. CLINICAL PROGRESSION MODE
    elif active_mode == "Clinical Progression Dashboard":
        st.subheader("📈 Patient Recovery & Compliance Dashboard")
        
        latest_sessions = db.fetch_latest(10)
        weekly = db.get_weekly_trends(selected_subject)
        monthly = db.get_monthly_trends(selected_subject)
        adherence = db.get_exercise_adherence(selected_subject)
        improvement = db.get_best_improvement(selected_subject)
        
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

if __name__ == '__main__':
    main()
