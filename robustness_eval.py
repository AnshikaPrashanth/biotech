import os
import glob
import math
import numpy as np
import pandas as pd
import torch
import matplotlib.pyplot as plt
from pathlib import Path

from config import TRAINING_CONFIG, MODEL_WEIGHTS
from src.dataset import parse_intellirehab_file
from src.model import stgat_from_config
from src.evaluation import classification_report, balanced_accuracy_score, matthews_corrcoef, roc_auc_scores

def rotate_sequence_y(sequence: np.ndarray, angle_degrees: float) -> np.ndarray:
    """Rotates a skeleton sequence (T, 25, 3) around the vertical Y-axis."""
    angle_rad = np.deg2rad(angle_degrees)
    cos_a = math.cos(angle_rad)
    sin_a = math.sin(angle_rad)
    
    # Rotation matrix around Y axis
    R = np.array([
        [cos_a, 0.0, sin_a],
        [0.0, 1.0, 0.0],
        [-sin_a, 0.0, cos_a]
    ], dtype=np.float32)
    
    return np.einsum('ij,tkj->tki', R, sequence).astype(np.float32)

def evaluate_robustness(
    model,
    file_paths: list,
    angles: list = [0, 15, 30, 45],
    device: str = "cpu"
) -> pd.DataFrame:
    """Evaluates classification accuracy and other metrics for different rotation angles."""
    model.eval()
    results = []
    
    # Pre-load all sequences to avoid parsing speed bottlenecks during evaluation loops
    loaded_data = []
    for fp in file_paths:
        try:
            seq, _, _, label = parse_intellirehab_file(fp)
            # Enforce fixed sequence length (64)
            target_len = TRAINING_CONFIG.get('sequence_length', 64)
            if seq.shape[0] > target_len:
                start = (seq.shape[0] - target_len) // 2
                seq = seq[start:start + target_len]
            elif seq.shape[0] < target_len:
                padded = np.zeros((target_len, 25, 3), dtype=np.float32)
                padded[:seq.shape[0]] = seq
                padded[seq.shape[0]:] = seq[-1:]
                seq = padded
            loaded_data.append((seq, label))
        except Exception:
            pass
            
    print(f"Loaded {len(loaded_data)} test sequences for robustness analysis.")
    if not loaded_data:
        raise ValueError("No sequences loaded successfully.")
        
    for angle in angles:
        targets = []
        preds = []
        probs = []
        
        for seq, label in loaded_data:
            # Apply Y-rotation
            rot_seq = rotate_sequence_y(seq, angle)
            
            # Format to batch structure (1, T, 25, 3)
            tensor = torch.from_numpy(rot_seq[None, ...]).float().to(device)
            
            with torch.no_grad():
                out = model(tensor)
                
            logits = out['logits'][0]
            pred_probs = torch.softmax(logits, dim=-1).cpu().numpy()
            pred_class = int(np.argmax(pred_probs))
            
            targets.append(label)
            preds.append(pred_class)
            probs.append(float(pred_probs[1])) # Prob of Compensated class
            
        # Calculate metrics
        report = classification_report(targets, preds, labels=['healthy', 'compensated'])
        acc = report['accuracy']
        bal_acc = balanced_accuracy_score(targets, preds)
        f1 = report['macro avg']['f1-score']
        mcc = matthews_corrcoef(targets, preds)
        
        roc_results = roc_auc_scores(targets, probs)
        auc = roc_results['auc']
        
        results.append({
            "Angle": f"{angle}°",
            "Accuracy": acc,
            "Balanced Accuracy": bal_acc,
            "F1-Score": f1,
            "MCC": mcc,
            "ROC-AUC": auc
        })
        print(f"Angle: {angle}° | Accuracy: {acc:.4f} | Balanced Accuracy: {bal_acc:.4f} | F1: {f1:.4f} | ROC-AUC: {auc:.4f}")
        
    return pd.DataFrame(results)

def main():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Running robustness evaluation on {device}...")
    
    # Load model
    model_config = {
        'hidden_dim': TRAINING_CONFIG['hidden_dim'],
        'heads': TRAINING_CONFIG['heads'],
        'dropout': 0.0
    }
    model = stgat_from_config(model_config).to(device)
    
    if os.path.exists("checkpoints/best_model.pt"):
        checkpoint = torch.load("checkpoints/best_model.pt", map_location=device)
        state_dict = checkpoint.get('model_state', checkpoint)
        model.load_state_dict(state_dict, strict=False)
        print("Model weights loaded successfully.")
    else:
        print("WARNING: Model weights not found. Using random initialization.")
        
    # Get subset of files for evaluation (subjects 101 and 102)
    raw_dir = "SkeletonData/SkeletonData/RawData"
    file_paths = glob.glob(os.path.join(raw_dir, "101_*.txt")) + glob.glob(os.path.join(raw_dir, "102_*.txt"))
    
    if not file_paths:
        print(f"No trial files found in {raw_dir} for evaluation.")
        return
        
    # Run evaluation
    df = evaluate_robustness(model, file_paths, angles=[0, 15, 30, 45], device=device)
    
    # Save results
    out_dir = Path("results/robustness")
    out_dir.mkdir(parents=True, exist_ok=True)
    
    csv_path = out_dir / "robustness_table.csv"
    df.to_csv(csv_path, index=False)
    print(f"Robustness results table saved to: {csv_path}")
    
    # Generate Plot
    plt.figure(figsize=(8, 5))
    x_labels = df["Angle"]
    plt.plot(x_labels, df["Accuracy"], marker='o', linewidth=2.5, color='#2E86AB', label='Accuracy')
    plt.plot(x_labels, df["F1-Score"], marker='s', linewidth=2.5, color='#E84855', label='F1-Score')
    plt.plot(x_labels, df["ROC-AUC"], marker='^', linestyle='--', linewidth=2, color='#10B981', label='ROC-AUC')
    
    plt.title("Model Classification Robustness under Camera Angle Rotations", fontsize=12, fontweight='bold')
    plt.xlabel("Controlled Y-Axis Rotation Angle (Yaw)", fontsize=11)
    plt.ylabel("Performance Score", fontsize=11)
    plt.ylim([0.0, 1.05])
    plt.grid(alpha=0.3)
    plt.legend(fontsize=10, loc='lower left')
    
    plot_path = out_dir / "robustness_plot.png"
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Robustness plot saved to: {plot_path}")

if __name__ == '__main__':
    main()
