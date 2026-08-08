import os
import yaml
from pathlib import Path

BASE_DIR = Path(__file__).parent

config_path = BASE_DIR / 'config.yaml'
if config_path.exists():
    with open(config_path, 'r') as f:
        _config = yaml.safe_load(f)
else:
    # Default fallback parameters
    _config = {
        'paths': {
            'data_dir': 'SkeletonData/SkeletonData/RawData',
            'checkpoint_dir': 'checkpoints',
            'log_dir': 'logs',
            'baseline_dir': 'baselines',
            'db_path': 'rehab_sessions.db',
            'model_weights': 'checkpoints/st_gat_loso.pt',
            'best_model_weights': 'checkpoints/best_model.pt',
        },
        'training': {
            'seed': 42,
            'batch_size': 8,
            'epochs': 80,
            'lr': 2e-4,
            'weight_decay': 1e-4,
            'num_workers': 0,
            'patience': 8,
            'early_stopping_delta': 1e-3,
            'sequence_length': 64,
            'hidden_dim': 64,
            'heads': 4,
            'dropout': 0.2,
            'loss_type': 'weighted_ce',
            'focal_gamma': 2.0,
            'device': 'cuda',
        },
        'model': {
            'num_joints': 25,
            'input_dim': 3,
            'num_classes': 2,
            'heads': 4,
            'dropout': 0.2,
        }
    }

# API compatibility variables
DATA_DIR = BASE_DIR / _config['paths']['data_dir']
CHECKPOINT_DIR = BASE_DIR / _config['paths']['checkpoint_dir']
LOG_DIR = BASE_DIR / _config['paths']['log_dir']
BASELINE_DIR = BASE_DIR / _config['paths']['baseline_dir']
DB_PATH = BASE_DIR / _config['paths']['db_path']
MODEL_WEIGHTS = BASE_DIR / _config['paths']['model_weights']
BEST_MODEL_WEIGHTS = BASE_DIR / _config['paths']['best_model_weights']

TRAINING_CONFIG = _config['training']
MODEL_CONFIG = _config.get('model', {})
GLOBAL_CONFIG = _config
