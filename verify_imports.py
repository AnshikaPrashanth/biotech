import sys; sys.path.insert(0, '.')
print('--- Project Module Imports ---')
from config import CHECKPOINT_DIR, LOG_DIR, BASELINE_DIR, DB_PATH, TRAINING_CONFIG, DATA_DIR, MODEL_WEIGHTS
print('config.py:        OK')
print(f"  DATA_DIR       = {DATA_DIR}")
print(f"  CHECKPOINT_DIR = {CHECKPOINT_DIR}")
print(f"  LOG_DIR        = {LOG_DIR}")
print(f"  BASELINE_DIR   = {BASELINE_DIR}")
print(f"  device         = {TRAINING_CONFIG['device']}")

from src.graph import get_edge_index, INTELLIREHAB_JOINTS
print(f"src.graph:        OK ({len(INTELLIREHAB_JOINTS)} joints)")
from src.model import STGAT, stgat_from_config
print("src.model:        OK")
from src.dataset import parse_intellirehab_file, load_intellirehab_directory
print("src.dataset:      OK")
from src.calibration import PersonalizedROMCalibrator, compute_joint_angles
print("src.calibration:  OK")
from src.database import SQLiteSessionDB
print("src.database:     OK")
from src.evaluation import aggregate_fold_metrics, classification_report
print("src.evaluation:   OK")
from src.utils import get_device, save_checkpoint, load_checkpoint, set_seed
print("src.utils:        OK")
from src.visualization import plot_3d_skeleton, plot_attention_heatmap
print("src.visualization:OK")

print()
print("--- Model Build + Forward Pass Test ---")
import torch
model = stgat_from_config({'hidden_dim': 64, 'heads': 4, 'dropout': 0.2})
model.eval()
dummy = torch.randn(2, 32, 25, 3)
with torch.no_grad():
    out = model(dummy)
print(f"logits shape:        {out['logits'].shape}")
print(f"joint_attn shape:    {out['joint_attention'].shape}")
print(f"frame_attn shape:    {out['frame_attention'].shape}")
params = sum(p.numel() for p in model.parameters())
print(f"Model parameters:    {params:,}")

print()
print("--- SQLite DB Test ---")
db = SQLiteSessionDB("test_verify.db")
db.log_session("101", "Stand", 0.92, "Healthy", {"SpineBase": 0.1}, None, 2.0, "test")
rows = db.fetch_latest(1)
print(f"SQLite log/fetch:    OK (row id={rows[0]['id']})")
db.close()
import os; os.remove("test_verify.db")

print()
print("=== ALL CHECKS PASSED ===")
