import os
import random
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional, Tuple, List
import numpy as np
import torch
import torch.nn as nn

def set_seed(seed: int = 42) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    # Ensure deterministic execution
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

def make_directory(path: str) -> Path:
    dir_path = Path(path)
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path

def save_checkpoint(state: Dict[str, Any], path: str) -> None:
    torch.save(state, path)

def load_checkpoint(path: str, device: Optional[torch.device] = None) -> Dict[str, Any]:
    if device is None:
        device = torch.device('cpu')
    return torch.load(path, map_location=device)

def get_device() -> torch.device:
    return torch.device('cuda' if torch.cuda.is_available() else 'cpu')

def format_timestamp() -> str:
    return datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')

def print_diagnostics(
    title: str,
    subject_ids: List[str],
    num_samples: int,
    class_distribution: Dict[int, int],
    exercise_distribution: Dict[str, int],
    val_subject: Optional[str] = None,
    model: Optional[nn.Module] = None,
    optimizer: Optional[torch.optim.Optimizer] = None,
    device: Optional[torch.device] = None,
    debug: bool = True
) -> None:
    if not debug:
        return
    print("\n" + "="*40)
    print(f"DIAGNOSTICS: {title}")
    print("="*40)
    print(f"Subjects: {subject_ids}")
    if val_subject:
        print(f"Validation Subject: {val_subject}")
    print(f"Number of Samples: {num_samples}")
    print(f"Class Distribution: {class_distribution}")
    print(f"Exercise Distribution: {exercise_distribution}")
    
    if model is not None:
        param_count = sum(p.numel() for p in model.parameters() if p.requires_grad)
        print(f"Model Trainable Parameter Count: {param_count}")
        
    if device is not None and device.type == 'cuda':
        memory_allocated = torch.cuda.memory_allocated(device) / (1024 ** 2)
        print(f"GPU Memory Allocated: {memory_allocated:.2f} MB")
        
    if optimizer is not None:
        lrs = [group['lr'] for group in optimizer.param_groups]
        print(f"Current Learning Rate: {lrs}")
    print("="*40 + "\n")

def export_to_onnx(
    model: nn.Module, 
    dummy_input: torch.Tensor, 
    onnx_path: str,
    input_names: Optional[list] = None,
    output_names: Optional[list] = None
) -> None:
    """Exports a trained PyTorch model to ONNX format."""
    model.eval()
    # Temporarily set model to export mode to bypass PyG dict returns
    old_export_mode = getattr(model, 'export_mode', False)
    if hasattr(model, 'export_mode'):
        model.export_mode = True
        
    input_names = input_names or ["input_sequence"]
    output_names = output_names or ["logits"]
    
    torch.onnx.export(
        model,
        dummy_input,
        onnx_path,
        export_params=True,
        opset_version=14,
        do_constant_folding=True,
        input_names=input_names,
        output_names=output_names,
        dynamic_axes={
            "input_sequence": {0: "batch_size", 1: "sequence_length"}
        }
    )
    
    if hasattr(model, 'export_mode'):
        model.export_mode = old_export_mode
    print(f"Model exported to ONNX format at: {onnx_path}")

def export_to_torchscript(
    model: nn.Module, 
    dummy_input: torch.Tensor, 
    ts_path: str
) -> None:
    """Exports a trained PyTorch model to TorchScript (JIT traced) format."""
    model.eval()
    old_export_mode = getattr(model, 'export_mode', False)
    if hasattr(model, 'export_mode'):
        model.export_mode = True
        
    with torch.no_grad():
        traced_model = torch.jit.trace(model.forward_export, dummy_input)
        traced_model.save(ts_path)
        
    if hasattr(model, 'export_mode'):
        model.export_mode = old_export_mode
    print(f"Model traced and saved to TorchScript format at: {ts_path}")
