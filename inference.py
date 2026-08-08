import argparse
import json
import os
from pathlib import Path
from typing import Dict, Any

import numpy as np
import torch

from config import TRAINING_CONFIG, BASELINE_DIR
from src.dataset import parse_intellirehab_file, INTELLIREHAB_JOINTS
from src.calibration import PersonalizedROMCalibrator, compute_joint_angles
from src.model import stgat_from_config, STGAT
from src.utils import get_device, export_to_onnx, export_to_torchscript

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Run Inference and Calibration Quality Assessment')
    parser.add_argument('--model-path', type=str, default='checkpoints/best_model.pt', help='Path to checkpoint weights')
    parser.add_argument('--input-file', type=str, required=True, help='Path to skeleton .txt trial file')
    parser.add_argument('--subject-id', type=str, default='101', help='Subject ID for calibration template')
    parser.add_argument('--baseline-path', type=str, default='baselines/rom_baselines.json', help='Path to ROM baseline file')
    
    # Export formats
    parser.add_argument('--export-onnx', type=str, default='', help='Path to save exported ONNX model')
    parser.add_argument('--export-ts', type=str, default='', help='Path to save traced TorchScript model')
    
    parser.add_argument('--device', type=str, default='cpu')
    return parser.parse_args()

def run_inference(
    model: STGAT,
    sequence: np.ndarray,
    device: torch.device
) -> Dict[str, Any]:
    """Runs sequence through ST-GAT model to obtain class probabilities and explainability attention maps."""
    model.eval()
    # Unpack sequence to batch structure (1, seq_len, 25, 3)
    tensor = torch.from_numpy(sequence[None, ...]).float().to(device)
    
    with torch.no_grad():
        outputs = model(tensor)
        
    logits = outputs['logits'][0]
    probs = outputs['probabilities'][0].cpu().numpy()
    pred_class = int(torch.argmax(logits).cpu().item())
    pred_label = "Compensated" if pred_class == 1 else "Healthy"
    confidence = float(probs[pred_class])
    
    joint_attn = outputs['joint_attention'][0].cpu().numpy()
    frame_attn = outputs['frame_attention'][0].cpu().numpy()
    
    # Map attention indices to joint names
    joint_attention_map = {
        INTELLIREHAB_JOINTS[i]: float(joint_attn[i]) 
        for i in range(len(INTELLIREHAB_JOINTS))
    }
    
    return {
        'prediction': pred_label,
        'class_idx': pred_class,
        'confidence': confidence,
        'joint_attention': joint_attention_map,
        'frame_attention': frame_attn.tolist()
    }

def main() -> None:
    args = parse_args()
    device = torch.device(args.device)
    
    # Load model configuration
    config = {
        'hidden_dim': TRAINING_CONFIG['hidden_dim'],
        'heads': TRAINING_CONFIG['heads'],
        'dropout': 0.0
    }
    
    model = stgat_from_config(config).to(device)
    
    # Load checkpoint
    if os.path.exists(args.model_path):
        checkpoint = torch.load(args.model_path, map_location=device)
        state_dict = checkpoint.get('model_state', checkpoint)
        model.load_state_dict(state_dict, strict=False)
        print(f"Loaded weights from {args.model_path}")
    else:
        print(f"Warning: Weights at {args.model_path} not found. Running with randomized weights.")
        
    # Model Export Handling
    if args.export_onnx or args.export_ts:
        # Dummy sequence shape for tracing/export: (batch_size, sequence_length, joints, dimensions)
        dummy_input = torch.zeros((1, TRAINING_CONFIG['sequence_length'], 25, 3), dtype=torch.float32, device=device)
        
        if args.export_onnx:
            export_to_onnx(model, dummy_input, args.export_onnx)
        if args.export_ts:
            export_to_torchscript(model, dummy_input, args.export_ts)
            
    # Load sequence
    print(f"Parsing skeleton trial file: {args.input_file}")
    try:
        sequence, exercise_type, subject_id, movement_label = parse_intellirehab_file(args.input_file)
    except Exception as e:
        print(f"Error parsing file: {e}")
        return
        
    # Perform model inference
    results = run_inference(model, sequence, device)
    
    # Perform calibration analysis if baseline exists
    calibration_results = {}
    if os.path.exists(args.baseline_path):
        print(f"Loading patient ROM template calibration from: {args.baseline_path}")
        calibrator = PersonalizedROMCalibrator(baseline_path=args.baseline_path)
        
        # Override baseline subject_id if requested
        subj = args.subject_id if args.subject_id in calibrator.baselines else subject_id
        if subj in calibrator.baselines:
            cal_eval = calibrator.evaluate(subj, sequence)
            calibration_results = {
                'rom_deviation': cal_eval['joint_errors'],
                'rom_confidence': cal_eval['confidence'],
                'top_errors': cal_eval['top_error_joints'],
                'progression_score': cal_eval['progression_score']
            }
        else:
            print(f"Warning: Subject ID {subj} not found inside calibration baseline file.")
    else:
        print("Warning: Calibration baseline file not found. Skipping ROM deviation checks.")
        
    # Assemble comprehensive explainability report
    report = {
        'metadata': {
            'input_file': args.input_file,
            'exercise_type': exercise_type,
            'subject_id': subject_id,
            'ground_truth_label': "Compensated" if movement_label == 1 else "Healthy"
        },
        'st_gat_prediction': {
            'verdict': results['prediction'],
            'confidence': results['confidence'],
        },
        'calibration_metrics': calibration_results,
        'explainability': {
            'top_joint_attentions': sorted(results['joint_attention'].items(), key=lambda x: x[1], reverse=True)[:5]
        }
    }
    
    # Output report
    print("\n==========================================")
    print("EXPLAINABLE REHAB AI INFERENCE REPORT")
    print("==========================================")
    print(json.dumps(report, indent=2))
    
if __name__ == '__main__':
    main()
