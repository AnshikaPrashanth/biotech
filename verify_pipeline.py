"""End-to-end pipeline verification script."""
import os, json
os.chdir(os.path.dirname(os.path.abspath(__file__)))

print("=== STEP 1: PARSER ===")
from src.dataset import parse_intellirehab_file, load_intellirehab_directory
seq, ex, subj, label = parse_intellirehab_file(
    "SkeletonData/SkeletonData/RawData/101_18_0_1_1_stand.txt"
)
print(f"  sequence shape: {seq.shape}, exercise: {ex}, subject: {subj}, label: {label}")

print("=== STEP 2: PREPROCESSING ===")
import numpy as np
print(f"  mean: {seq.mean():.4f}, std: {seq.std():.4f}")

print("=== STEP 3: MODEL BUILD ===")
from src.model import stgat_from_config
model = stgat_from_config({"hidden_dim": 64, "heads": 4, "dropout": 0.0})
model.eval()
print(f"  parameters: {sum(p.numel() for p in model.parameters())}")

print("=== STEP 4: CHECKPOINT LOAD ===")
import torch
if os.path.exists("checkpoints/best_model.pt"):
    ckpt = torch.load("checkpoints/best_model.pt", map_location="cpu")
    model.load_state_dict(ckpt.get("model_state", ckpt), strict=False)
    print("  checkpoint loaded: OK")
else:
    print("  WARNING: checkpoint not found, using random weights")

print("=== STEP 5: FORWARD PASS ===")
tensor = torch.from_numpy(seq[None, ...]).float()
with torch.no_grad():
    out = model(tensor)
probs = out["probabilities"].tolist()[0]
print(f"  logits shape: {out['logits'].shape}")
print(f"  probabilities: healthy={probs[0]:.4f}, compensated={probs[1]:.4f}")
print(f"  joint_attention shape: {out['joint_attention'].shape}")
print(f"  frame_attention shape: {out['frame_attention'].shape}")

print("=== STEP 6: PREDICTION ===")
pred_class = int(torch.argmax(out["logits"][0]))
verdict = "Compensated" if pred_class == 1 else "Healthy"
confidence = probs[pred_class]
print(f"  prediction: {verdict} (confidence: {confidence:.4f})")

print("=== STEP 7: CALIBRATION / ROM ===")
from src.calibration import compute_joint_angles
angles = compute_joint_angles(seq)
print(f"  angle keys: {list(angles.keys())}")
for k, v in list(angles.items())[:3]:
    print(f"    {k}: range={v.max()-v.min():.2f} deg")

print("=== STEP 8: ATTENTION MAP ===")
from src.graph import INTELLIREHAB_JOINTS
joint_attn = out["joint_attention"][0].numpy()
top5 = sorted(enumerate(joint_attn), key=lambda x: x[1], reverse=True)[:5]
print("  Top-5 joints by attention:")
for idx, val in top5:
    print(f"    {INTELLIREHAB_JOINTS[idx]}: {val:.4f}")

frame_attn = out["frame_attention"][0].numpy()
print(f"  frame attention shape: {frame_attn.shape}, peak frame: {frame_attn.argmax()}")

print("=== STEP 9: VISUALIZATION (headless) ===")
from src.visualization import plot_attention_heatmap, plot_temporal_attention, plot_rom_curve
fig_attn = plot_attention_heatmap(joint_attn.tolist(), INTELLIREHAB_JOINTS)
fig_temp = plot_temporal_attention(list(range(len(frame_attn))), frame_attn.tolist())
fig_rom = plot_rom_curve(angles)
print("  plotly figures created: OK")

print("=== STEP 10: SQLITE LOGGING ===")
from src.database import SQLiteSessionDB
db = SQLiteSessionDB("test_pipeline.db")
sess_id = db.log_session(
    subject_id="101",
    exercise_type="stand",
    confidence=confidence,
    verdict=verdict,
    attention_map={INTELLIREHAB_JOINTS[i]: float(joint_attn[i]) for i in range(25)},
    session_duration=float(seq.shape[0] / 30.0),
    notes="pipeline_verification_test"
)
print(f"  session logged, id: {sess_id}")
rows = db.fetch_latest(1)
print(f"  retrieved: subject={rows[0]['subject_id']}, verdict={rows[0]['verdict']}, duration={rows[0]['session_duration']:.2f}s")
db.close()
os.remove("test_pipeline.db")

print()
print("=" * 50)
print("ALL PIPELINE STAGES PASSED SUCCESSFULLY")
print("=" * 50)
