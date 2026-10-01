import os
import sys
import tempfile
import sqlite3
import numpy as np
import pytest
import torch

sys.path.append(os.path.abspath("e:/INTERNSHIP COE"))

from src.dataset import convert_mediapipe_landmarks, normalize_pelvis_centered, interpolate_missing_frames
from src.skeleton_pipeline import canonicalize_skeleton, mediapipe_to_intellirehab
from src.video_to_skeleton import extract_skeleton_from_video, write_kinect_txt
from src.webcam_pose import WebcamPoseStreamer
from src.error_attribution import BiomechanicalErrorEngine, calculate_derivatives, calculate_symmetry_deviations
from src.uncertainty import confidence_based_abstention, evaluate_uncertainty
from src.calibration import segment_repetitions
from src.database import SQLiteSessionDB
from src.report_generator import RehabReportGenerator

def test_mediapipe_to_intellirehab_rotation():
    """Verify coordinate translation (inversion of all axes)."""
    raw_mp = np.array([1.0, 2.0, 3.0], dtype=np.float32)
    aligned = mediapipe_to_intellirehab(raw_mp)
    assert np.allclose(aligned, [-1.0, -2.0, -3.0])

def test_joint_mapping():
    """Verify mapping of 33 MediaPipe joints to 25 Kinect joints."""
    # dummy MediaPipe frame of shape (33, 3)
    dummy_mp = np.ones((33, 3), dtype=np.float32)
    dummy_mp[23] = [0.5, 0.5, 0.5] # HipLeft
    dummy_mp[24] = [1.5, 1.5, 1.5] # HipRight
    
    # SpineBase should be average of HipLeft and HipRight = [1.0, 1.0, 1.0]
    mapped = convert_mediapipe_landmarks(dummy_mp)
    assert mapped.shape == (25, 3)
    assert np.allclose(mapped[0], [1.0, 1.0, 1.0])

def test_pelvis_normalization():
    """Verify pelvis centering and scale normalization."""
    # sequence of 10 frames, shape (10, 25, 3)
    seq = np.ones((10, 25, 3), dtype=np.float32) * 5.0
    # Make SpineBase (index 0) different
    seq[:, 0] = [1.0, 2.0, 3.0]
    
    normalized = normalize_pelvis_centered(seq)
    assert normalized.shape == (10, 25, 3)
    # SpineBase (pelvis) must be centered at zero
    assert np.allclose(normalized[:, 0], 0.0)

def test_missing_landmark_interpolation():
    """Verify that missing frames (zeros) are correctly interpolated."""
    seq = np.ones((5, 25, 3), dtype=np.float32)
    # Set frame index 2 to zeros (representing missing frame)
    seq[2, :, :] = 0.0
    
    interpolated = interpolate_missing_frames(seq)
    # The zeros should be replaced by linear interpolation of frame 1 and 3 (which are both 1.0)
    assert np.allclose(interpolated[2], 1.0)

def test_webcam_pose_streamer_buffering():
    """Verify sliding buffer and inference trigger stride."""
    streamer = WebcamPoseStreamer(sequence_length=10, inference_interval=3)
    
    # Create mock frame
    mock_frame = np.zeros((100, 100, 3), dtype=np.uint8)
    
    # Feed 10 frames
    for i in range(10):
        # We don't have a person in mock_frame, so pose_engine will fail and push zeros.
        # This is expected and tests missing landmark handling.
        frame, inf_seq, status = streamer.process_frame(mock_frame)
        
    assert len(streamer.raw_buffer) == 10
    
    # 11th frame (should pop first, buffer remains size 10)
    # Frame count is 11, which is not divisible by 3 (so inf_seq is None)
    frame, inf_seq, status = streamer.process_frame(mock_frame)
    assert len(streamer.raw_buffer) == 10
    assert inf_seq is None
    
    # 12th frame (frame_count 12 is divisible by 3, should return sequence)
    frame, inf_seq, status = streamer.process_frame(mock_frame)
    assert inf_seq is not None
    assert inf_seq.shape == (10, 25, 3)
    streamer.close()

def test_video_extraction():
    """Verify video skeleton extraction pipeline runs successfully on a mock video."""
    import cv2
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_vid:
        temp_path = temp_vid.name
        
    # Write a short mock video (15 frames of blue background) using cv2
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(temp_path, fourcc, 10.0, (100, 100))
    for _ in range(15):
        frame = np.zeros((100, 100, 3), dtype=np.uint8)
        frame[:, :] = [255, 0, 0]
        out.write(frame)
    out.release()
    
    # Run extraction (should run CV2 read and fallback to zeros since no pose is in blue frames)
    # Tests handling of failures and coordinate interpolation
    try:
        raw, canonical, meta = extract_skeleton_from_video(
            video_path=temp_path,
            subject_id="test_sub",
            exercise_type="stand",
            export_txt=True,
            out_dir=tempfile.gettempdir()
        )
        assert raw.shape == (15, 33, 3)
        assert canonical.shape == (15, 25, 3)
        assert meta["detection_success_rate"] == 0.0  # mock video had no actual person
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

def test_biomechanical_error_engine():
    """Verify derivative calculations and symmetry checks."""
    # Create sequence with horizontal motion on arms
    seq = np.zeros((10, 25, 3), dtype=np.float32)
    # Left Shoulder = idx 4, Right Shoulder = idx 8
    seq[:, 4] = np.linspace(0.0, 0.3, 10)[:, None]
    
    vel, acc = calculate_derivatives(seq, dt=1.0)
    # Velocity is diff: np.diff(seq) -> constant 0.0333...
    assert np.allclose(vel[1:, 4], 0.03333333333333333)
    
    asymmetry = calculate_symmetry_deviations(seq)
    # ShoulderLeft should have asymmetry deviation
    assert asymmetry["ShoulderLeft"] > 0.0

def test_movement_quality_score():
    """Verify MQS calculation range and parameter responsiveness."""
    config = {
        "biomechanical": {
            "weights": {
                "w_rom": 0.3, "w_sym": 0.2, "w_vel": 0.2, "w_acc": 0.1, "w_attention": 0.2
            },
            "quality_score": {
                "w_rom": 0.4, "w_sym": 0.3, "w_temporal": 0.1, "w_bio": 0.2
            }
        }
    }
    engine = BiomechanicalErrorEngine(config)
    seq = np.zeros((20, 25, 3), dtype=np.float32)
    
    mqs, components = engine.compute_movement_quality_score(seq)
    assert 0.0 <= mqs <= 100.0
    assert "rom" in components
    assert "symmetry" in components

def test_uncertainty_thresholding():
    """Verify confidence-based abstention threshold triggers."""
    probs = np.array([0.55, 0.45], dtype=np.float32)
    
    # 0.55 < 0.70 threshold -> Uncertain
    pred, decision, conf, unc = confidence_based_abstention(probs, threshold=0.70)
    assert decision == "Uncertain / Human Review"
    
    # 0.55 >= 0.50 threshold -> Healthy
    pred2, decision2, conf2, unc2 = confidence_based_abstention(probs, threshold=0.50)
    assert decision2 == "Healthy"

def test_repetition_segmentation():
    """Verify repetition segmentation returns list of sequences."""
    seq = np.random.normal(size=(50, 25, 3))
    reps = segment_repetitions(seq)
    assert isinstance(reps, list)
    assert len(reps) >= 1

def test_sqlite_migration_and_logging():
    """Verify SQLite Session DB initialization, column migration, and data logging."""
    with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as temp_db:
        temp_db_path = temp_db.name
        
    try:
        db = SQLiteSessionDB(temp_db_path)
        
        # Verify columns exist
        cursor = db.connection.cursor()
        cursor.execute("PRAGMA table_info(sessions)")
        cols = [row['name'] for row in cursor.fetchall()]
        assert "movement_quality" in cols
        assert "uncertainty" in cols
        assert "top_error_joints" in cols
        
        # Log session
        sess_id = db.log_session(
            subject_id="test_patient",
            exercise_type="chair",
            confidence=0.85,
            verdict="Healthy",
            attention_map={"Head": 0.5},
            movement_quality=88.5,
            uncertainty=0.15
        )
        assert sess_id > 0
        
        latest = db.fetch_latest(1)[0]
        assert latest["subject_id"] == "test_patient"
        assert latest["movement_quality"] == 88.5
        db.close()
    finally:
        if os.path.exists(temp_db_path):
            os.remove(temp_db_path)

def test_report_generation():
    """Verify JSON, Markdown, and HTML reports are written properly."""
    dummy_results = {
        "metadata": {"subject_id": "101", "exercise_type": "stand", "source_type": "txt", "timestamp": "2026-08-16"},
        "prediction": {"verdict": "Healthy", "confidence": 0.95, "probabilities": [0.95, 0.05]},
        "uncertainty": {"uncertainty_score": 0.05, "decision_status": "Healthy", "confidence_threshold": 0.70},
        "movement_quality": {"score": 92.5, "components": {"rom": 95, "symmetry": 90, "temporal": 92, "biomechanical": 93}},
        "rom_analysis": {"tolerance_scale": 1.0, "calibrated_deviations": {}, "overall_rom_confidence": 0.95},
        "error_attribution": {
            "overall_joint_scores": {"Head": 0.1},
            "joint_error_details": {"Head": {"rom_deviation": 0.0, "symmetry_deviation": 0.0, "velocity_deviation": 0.0, "error_score": 0.0}},
            "top_error_joints": [("Head", 0.1)]
        },
        "attention": {"joint_attention": {"Head": 0.5}, "frame_attention": [0.1]},
        "repetitions": {"count": 4, "degradation_slope": 0.02, "trajectory": "Stable"},
        "feedback": ["Feedback 1"]
    }
    
    with tempfile.TemporaryDirectory() as temp_dir:
        json_p = os.path.join(temp_dir, "report.json")
        md_p = os.path.join(temp_dir, "report.md")
        html_p = os.path.join(temp_dir, "report.html")
        
        RehabReportGenerator.generate_json_report(dummy_results, json_p)
        RehabReportGenerator.generate_markdown_report(dummy_results, md_p)
        RehabReportGenerator.generate_html_report(dummy_results, html_p)
        
        assert os.path.exists(json_p)
        assert os.path.exists(md_p)
        assert os.path.exists(html_p)

def test_3d_skeleton_layout_and_visibility():
    """Verify 3D skeleton plot renders upright with true metric aspectmode and visible joints."""
    from src.visualization import plot_3d_skeleton
    from src.graph import INTELLIREHAB_JOINTS
    
    # Create an upright mock skeleton of 25 joints
    dummy_joints = np.zeros((25, 3), dtype=np.float32)
    dummy_joints[3] = [0.0, 0.95, -0.1]   # Head (Height Y = +0.95)
    dummy_joints[0] = [0.0, 0.0, 0.0]     # SpineBase (Height Y = 0.0)
    dummy_joints[15] = [-0.15, -0.95, 0.0] # FootLeft (Height Y = -0.95)
    
    fig = plot_3d_skeleton(dummy_joints, attention={"Head": 0.85, "SpineBase": 0.4})
    
    # 1. Verify 1:1:1 physical meter aspect scaling
    assert fig.layout.scene.aspectmode == "data"
    
    # 2. Verify Plotly Z axis is height (+Z is UP)
    assert fig.layout.scene.camera.up.z == 1
    
    # 3. Find bones trace and markers trace
    bones_trace = fig.data[0]
    marker_trace = fig.data[2]  # trace 0: bones, trace 1: floor level, trace 2: joints
    
    # 4. Verify all 25 joints are present
    assert len(marker_trace.x) == 25
    assert len(marker_trace.y) == 25
    assert len(marker_trace.z) == 25
    
    # 5. Verify Head is higher than SpineBase, which is higher than FootLeft in Plotly Z
    assert marker_trace.z[3] > marker_trace.z[0] > marker_trace.z[15]

def test_label_3_exclusion():
    """Verify that files with Label 3 raise ValueError and cannot enter the dataset."""
    from src.dataset import extract_movement_label
    with pytest.raises(ValueError) as excinfo:
        extract_movement_label("SkeletonData/SkeletonData/RawData/101_20160101_1_1_3_pos.txt")
    assert "Label 3" in str(excinfo.value)

def test_hand_wrist_non_duplication():
    """Verify Wrist and Hand landmarks are not duplicated and have non-zero distance."""
    dummy_mp = np.random.normal(size=(33, 3)).astype(np.float32)
    mapped = convert_mediapipe_landmarks(dummy_mp)
    wrist_left = mapped[6]
    hand_left = mapped[7]
    wrist_right = mapped[10]
    hand_right = mapped[11]
    
    assert not np.allclose(wrist_left, hand_left)
    assert not np.allclose(wrist_right, hand_right)
    assert np.linalg.norm(wrist_left - hand_left) > 1e-4
    assert np.linalg.norm(wrist_right - hand_right) > 1e-4

def test_temporal_attention_padding_mask_invariance():
    """Verify that modifying padded frames does NOT change model predictions when key_padding_mask is passed."""
    from src.model import stgat_from_config
    model = stgat_from_config({'hidden_dim': 64, 'heads': 4, 'dropout': 0.0})
    model.eval()
    
    # Sequence of 64 frames where first 30 frames are valid and last 34 are padded
    seq1 = torch.randn(1, 64, 25, 3)
    mask = torch.zeros(1, 64, dtype=torch.bool)
    mask[0, :30] = True  # valid frames
    
    # Sequence 2 has identical valid frames (0..30) but different random values in padded frames (30..64)
    seq2 = seq1.clone()
    seq2[0, 30:] = torch.randn(34, 25, 3)
    
    with torch.no_grad():
        out1 = model(seq1, mask=mask)
        out2 = model(seq2, mask=mask)
        
    assert torch.allclose(out1['logits'], out2['logits'], atol=1e-5)
    assert torch.allclose(out1['probabilities'], out2['probabilities'], atol=1e-5)


