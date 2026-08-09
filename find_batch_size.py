"""
GPU batch size optimizer.
Tests increasing batch sizes until CUDA OOM to find the largest stable batch size.

Usage:
    python find_batch_size.py
"""
import sys
import gc
from pathlib import Path

import torch

BASE_DIR = Path(__file__).parent
sys.path.insert(0, str(BASE_DIR))

from config import TRAINING_CONFIG
from src.model import stgat_from_config


def test_batch_size(model, batch_size: int, seq_len: int, device: torch.device) -> bool:
    """Returns True if the batch size fits in VRAM without OOM."""
    try:
        model.train()
        dummy = torch.randn(batch_size, seq_len, 25, 3, device=device)
        labels = torch.randint(0, 2, (batch_size,), device=device)

        criterion = torch.nn.CrossEntropyLoss()
        optimizer = torch.optim.AdamW(model.parameters(), lr=1e-4)

        if hasattr(torch, "amp"):
            scaler = torch.amp.GradScaler(device=device.type, enabled=True)
            with torch.amp.autocast(device_type=device.type, enabled=True):
                out = model(dummy)
                loss = criterion(out["logits"], labels)
        else:
            out = model(dummy)
            loss = criterion(out["logits"], labels)
            scaler = None

        if scaler:
            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()
        else:
            loss.backward()
            optimizer.step()

        # Cleanup
        del dummy, labels, out, loss
        torch.cuda.empty_cache()
        gc.collect()
        return True

    except torch.cuda.OutOfMemoryError:
        torch.cuda.empty_cache()
        gc.collect()
        return False
    except Exception as e:
        print(f"  [ERROR] Unexpected error: {e}")
        torch.cuda.empty_cache()
        gc.collect()
        return False


def main():
    if not torch.cuda.is_available():
        print("No CUDA GPU detected. Batch size optimization only applies to GPU training.")
        print("Recommended CPU batch size: 4-8")
        return 8

    device = torch.device("cuda")
    print("\n" + "=" * 55)
    print("  GPU BATCH SIZE OPTIMIZER")
    print("=" * 55)

    props = torch.cuda.get_device_properties(0)
    total_vram = props.total_memory / 1024**3
    free_vram = torch.cuda.mem_get_info()[0] / 1024**3
    print(f"  GPU:       {props.name}")
    print(f"  VRAM:      {total_vram:.2f} GB total, {free_vram:.2f} GB free")

    seq_len = TRAINING_CONFIG["sequence_length"]
    config = {
        "hidden_dim": TRAINING_CONFIG["hidden_dim"],
        "heads": TRAINING_CONFIG["heads"],
        "dropout": TRAINING_CONFIG["dropout"],
    }

    model = stgat_from_config(config).to(device)
    model_params = sum(p.numel() for p in model.parameters())
    print(f"  Model:     {model_params:,} parameters")
    print(f"  Seq len:   {seq_len}")
    print()

    candidates = [2, 4, 8, 16, 32, 48, 64]
    best_batch = 2
    print(f"  {'Batch Size':>12}  {'Status':>10}  {'VRAM Used':>10}")
    print(f"  {'-'*12}  {'-'*10}  {'-'*10}")

    for bs in candidates:
        torch.cuda.reset_peak_memory_stats()
        success = test_batch_size(model, bs, seq_len, device)
        vram_used = torch.cuda.max_memory_allocated() / 1024**3
        status = "OK" if success else "OOM"
        print(f"  {bs:>12}  {status:>10}  {vram_used:>8.2f} GB")
        if success:
            best_batch = bs
        else:
            # One extra try at the midpoint to be precise
            mid = (bs + candidates[candidates.index(bs) - 1]) // 2 if candidates.index(bs) > 0 else bs
            if mid != bs and mid != best_batch:
                mid_ok = test_batch_size(model, mid, seq_len, device)
                vram_mid = torch.cuda.max_memory_allocated() / 1024**3
                print(f"  {mid:>12}  {'OK' if mid_ok else 'OOM':>10}  {vram_mid:>8.2f} GB")
                if mid_ok:
                    best_batch = mid
            break

    del model
    torch.cuda.empty_cache()
    gc.collect()

    print()
    print(f"  Recommended batch size: {best_batch}")
    print(f"  GPU utilization:        See 'nvidia-smi' during training")
    print("=" * 55 + "\n")
    return best_batch


if __name__ == "__main__":
    best = main()
    print(f"\nBEST_BATCH_SIZE={best}")
