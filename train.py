import argparse
from functools import partial
import os
import json
from pathlib import Path
from typing import Any, Dict, List, Tuple, Optional
from collections import Counter

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.optim import AdamW
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter
from tqdm import tqdm

from config import CHECKPOINT_DIR, LOG_DIR, MODEL_WEIGHTS, TRAINING_CONFIG, GLOBAL_CONFIG
from src.calibration import PersonalizedROMCalibrator
from src.dataset import (
    INTELLIREHAB_JOINTS, 
    build_loso_dataloaders, 
    load_intellirehab_directory,
    IntelliRehabSequenceDataset,
    make_weighted_sampler,
    sequence_collate_fn
)
from src.evaluation import (
    aggregate_fold_metrics, 
    classification_report,
    confusion_matrix, 
    matthews_corrcoef,
    cohen_kappa_score,
    balanced_accuracy_score,
    precision_recall_curve, 
    roc_auc_scores
)
from src.model import STGAT, stgat_from_config
from src.utils import get_device, load_checkpoint, save_checkpoint, set_seed, format_timestamp, print_diagnostics

# Focal Loss Implementation for Imbalanced Rehab Movement Datasets
class FocalLoss(nn.Module):
    def __init__(self, alpha: Optional[torch.Tensor] = None, gamma: float = 2.0, reduction: str = 'mean'):
        super().__init__()
        self.alpha = alpha
        self.gamma = gamma
        self.reduction = reduction

    def forward(self, inputs: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
        ce_loss = F.cross_entropy(inputs, targets, reduction='none')
        pt = torch.exp(-ce_loss)  # Probability of correct class
        focal_weight = (1 - pt) ** self.gamma
        loss = focal_weight * ce_loss
        
        if self.alpha is not None:
            alpha_t = self.alpha[targets]
            loss = alpha_t * loss
            
        if self.reduction == 'mean':
            return loss.mean()
        elif self.reduction == 'sum':
            return loss.sum()
        return loss

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Train ST-GAT with LOSO cross validation')
    parser.add_argument('--data-dir', type=str, default=str(Path('SkeletonData/SkeletonData/RawData')), help='Path to IntelliRehabDS root folder')
    parser.add_argument('--epochs', type=int, default=TRAINING_CONFIG['epochs'])
    parser.add_argument('--batch-size', type=int, default=TRAINING_CONFIG['batch_size'])
    parser.add_argument('--lr', type=float, default=TRAINING_CONFIG['lr'])
    parser.add_argument('--weight-decay', type=float, default=TRAINING_CONFIG['weight_decay'])
    parser.add_argument('--patience', type=int, default=TRAINING_CONFIG['patience'])
    parser.add_argument('--sequence-length', type=int, default=TRAINING_CONFIG['sequence_length'])
    parser.add_argument('--resume', type=str, default='', help='Checkpoint path to resume training')
    parser.add_argument('--device', type=str, default=TRAINING_CONFIG['device'])
    parser.add_argument('--fold', type=str, default='', help='Specific subject ID to run as validation fold (e.g. 101). Empty runs all folds.')
    parser.add_argument('--debug', action='store_true', default=True, help='Print diagnostic statistics during training.')
    return parser.parse_args()

def train_one_epoch(
    model: nn.Module,
    loader: torch.utils.data.DataLoader,
    criterion: nn.Module,
    optimizer: torch.optim.Optimizer,
    scaler: Any,
    device: torch.device,
) -> Tuple[float, float]:
    model.train()
    total_loss = 0.0
    total_samples = 0
    correct = 0
    
    for batch in loader:
        sequences = batch['sequence'].to(device, non_blocking=True)
        frame_mask = batch['mask'].to(device, non_blocking=True)
        labels = batch['label'].to(device, non_blocking=True)
        optimizer.zero_grad()
        
        if hasattr(torch, 'amp'):
            autocast_ctx = torch.amp.autocast(device_type=device.type, enabled=device.type == 'cuda')
        else:
            autocast_ctx = torch.cuda.amp.autocast(enabled=device.type == 'cuda')
            
        with autocast_ctx:
            outputs = model(sequences, mask=frame_mask)
            loss = criterion(outputs['logits'], labels)
            
        scaler.scale(loss).backward()
        scaler.unscale_(optimizer)
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        scaler.step(optimizer)
        scaler.update()
        
        total_loss += loss.item() * sequences.size(0)
        total_samples += sequences.size(0)
        
        preds = torch.argmax(outputs['logits'], dim=-1)
        correct += (preds == labels).sum().item()
        
    avg_loss = total_loss / total_samples if total_samples else 0.0
    avg_acc = correct / total_samples if total_samples else 0.0
    return avg_loss, avg_acc

def evaluate(
    model: nn.Module,
    loader: torch.utils.data.DataLoader,
    device: torch.device,
) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    model.eval()
    all_targets = []
    all_preds = []
    all_probs = []
    
    # Store explainability weights for reproducible visualization
    saved_attentions = []
    
    with torch.no_grad():
        for batch in loader:
            sequences = batch['sequence'].to(device, non_blocking=True)
            frame_mask = batch['mask'].to(device, non_blocking=True)
            labels = batch['label'].to(device, non_blocking=True)
            
            outputs = model(sequences, mask=frame_mask)
            logits = outputs['logits']
            probs = torch.softmax(logits, dim=-1)[:, 1]
            preds = torch.argmax(logits, dim=-1)
            
            all_targets.extend(labels.cpu().numpy().tolist())
            all_preds.extend(preds.cpu().numpy().tolist())
            all_probs.extend(probs.cpu().numpy().tolist())
            
            # Save raw model attention mappings along with label/prediction info
            for i in range(sequences.size(0)):
                saved_attentions.append({
                    'subject_id': batch['subject_id'][i],
                    'exercise_type': batch['exercise_type'][i],
                    'file_path': batch['file_path'][i],
                    'true_label': int(labels[i].cpu().item()),
                    'pred_label': int(preds[i].cpu().item()),
                    'confidence': float(torch.softmax(logits[i], dim=0)[preds[i]].cpu().item()),
                    'joint_attention': outputs['joint_attention'][i].cpu().numpy().tolist(),
                    'frame_attention': outputs['frame_attention'][i].cpu().numpy().tolist()
                })
                
    report = classification_report(all_targets, all_preds, labels=['healthy', 'compensated'])
    cm = confusion_matrix(all_targets, all_preds)
    roc = roc_auc_scores(all_targets, all_probs)
    pr = precision_recall_curve(all_targets, all_probs)
    mcc = matthews_corrcoef(all_targets, all_preds)
    kappa = cohen_kappa_score(all_targets, all_preds)
    balanced_acc = balanced_accuracy_score(all_targets, all_preds)
    
    metrics_dict = {
        'accuracy': report['accuracy'],
        'balanced_accuracy': balanced_acc,
        'precision_macro': report['macro avg']['precision'],
        'recall_macro': report['macro avg']['recall'],
        'f1_macro': report['macro avg']['f1-score'],
        'confusion_matrix': cm.tolist(),
        'roc_auc': roc,
        'pr_curve': pr,
        'mcc': mcc,
        'cohen_kappa': kappa
    }
    return metrics_dict, saved_attentions

def run_fold(
    model: nn.Module,
    train_loader: torch.utils.data.DataLoader,
    val_loader: torch.utils.data.DataLoader,
    train_entries: List[Dict],
    fold_name: str,
    device: torch.device,
    args: argparse.Namespace,
    writer: Optional[SummaryWriter],
    training_config: Optional[Dict[str, Any]] = None,
) -> Tuple[Dict[str, Any], List[Dict[str, Any]], int]:
    config = training_config or TRAINING_CONFIG
    # Check if sampler is used (default is WeightedRandomSampler).
    # If sampler is active, we disable class weighting in the loss to prevent double-penalization bias.
    use_class_weights = True
    if hasattr(train_loader, 'sampler') and train_loader.sampler is not None:
        from torch.utils.data import WeightedRandomSampler
        if isinstance(train_loader.sampler, WeightedRandomSampler):
            use_class_weights = False
            
    if use_class_weights:
        targets = [entry['movement_label'] for entry in train_entries]
        counts = Counter(targets)
        total = len(targets)
        w0 = total / max(counts[0], 1)
        w1 = total / max(counts[1], 1)
        class_weights = torch.tensor([w0, w1], dtype=torch.float, device=device)
    else:
        class_weights = None
        
    # Configure Loss Selection
    loss_type = config.get('loss_type', 'weighted_ce')
    if loss_type == 'focal':
        criterion = FocalLoss(alpha=class_weights, gamma=config.get('focal_gamma', 2.0))
    else:
        criterion = nn.CrossEntropyLoss(weight=class_weights)
        
    optimizer = AdamW(model.parameters(), lr=args.lr, weight_decay=args.weight_decay)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=args.epochs)
    
    if hasattr(torch, 'amp') and hasattr(torch.amp, 'GradScaler'):
        scaler = torch.amp.GradScaler(device=device.type, enabled=device.type == 'cuda')
    else:
        scaler = torch.cuda.amp.GradScaler(enabled=device.type == 'cuda')
    
    best_val_error_rate = float('inf')
    best_val_acc = 0.0
    patience_counter = 0
    best_state = None
    best_metrics = None
    best_attentions = []
    best_epoch = 0
    best_train_loss = float('nan')
    
    print(f"\n--- Starting {fold_name} ---")
    pbar = tqdm(range(args.epochs), desc="Training Fold")
    for epoch in pbar:
        train_loss, train_acc = train_one_epoch(model, train_loader, criterion, optimizer, scaler, device)
        val_metrics, val_attns = evaluate(model, val_loader, device)
        val_error_rate = 1.0 - val_metrics['accuracy']
        
        # Log to TensorBoard
        if writer is not None:
            writer.add_scalar(f'{fold_name}/train_loss', train_loss, epoch)
            writer.add_scalar(f'{fold_name}/train_accuracy', train_acc, epoch)
            writer.add_scalar(f'{fold_name}/val_accuracy', val_metrics['accuracy'], epoch)
            writer.add_scalar(f'{fold_name}/val_balanced_accuracy', val_metrics['balanced_accuracy'], epoch)
            writer.add_scalar(f'{fold_name}/val_f1_macro', val_metrics['f1_macro'], epoch)
        
        scheduler.step()
        
        # Early Stopping check
        if val_error_rate + config['early_stopping_delta'] < best_val_error_rate:
            best_val_error_rate = val_error_rate
            best_val_acc = val_metrics['accuracy']
            patience_counter = 0
            best_state = {k: v.cpu().clone() for k, v in model.state_dict().items()}
            best_metrics = val_metrics
            best_attentions = val_attns
            best_epoch = epoch + 1
            best_train_loss = train_loss
        else:
            patience_counter += 1
            
        pbar.set_postfix({
            'train_loss': f"{train_loss:.4f}",
            'val_acc': f"{val_metrics['accuracy']:.4f}",
            'best_val_acc': f"{best_val_acc:.4f}",
            'patience': f"{patience_counter}/{args.patience}"
        })
        
        if patience_counter >= args.patience:
            print(f"Early stopping triggered at epoch {epoch+1}")
            break
            
    if best_state is not None:
        model.load_state_dict(best_state)
        
    return best_metrics, best_attentions, best_epoch, best_train_loss

def build_model() -> nn.Module:
    config = {
        'input_dim': TRAINING_CONFIG['input_dim'] if 'input_dim' in TRAINING_CONFIG else 3,
        'hidden_dim': TRAINING_CONFIG['hidden_dim'],
        'num_classes': 2,
        'heads': TRAINING_CONFIG['heads'],
        'dropout': TRAINING_CONFIG['dropout'],
    }
    return stgat_from_config(config)

def main() -> None:
    args = parse_args()
    set_seed(TRAINING_CONFIG['seed'])
    
    os.makedirs(CHECKPOINT_DIR, exist_ok=True)
    os.makedirs(LOG_DIR, exist_ok=True)
    
    device = torch.device(args.device if torch.cuda.is_available() else 'cpu')
    # Enable cuDNN benchmark for fixed-size inputs (no-op on CPU)
    if device.type == 'cuda':
        torch.backends.cudnn.benchmark = True
        torch.backends.cudnn.enabled = True
        props = torch.cuda.get_device_properties(device)
        print(f"GPU: {props.name} ({props.total_memory / 1024**3:.1f} GB VRAM)")
    print(f"Using execution device: {device}")
    
    print(f"Scanning data from: {args.data_dir}")
    entries = load_intellirehab_directory(args.data_dir)
    if not entries:
        print("No skeleton files found. Please ensure IntelliRehabDS is extracted inside data-dir.")
        return
        
    print(f"Loaded {len(entries)} parsed repetition sequences.")
    
    # Organize LOSO cross-validation splits
    subjects = sorted(list({entry['subject_id'] for entry in entries}))
    print(f"Identified {len(subjects)} subjects: {subjects}")
    
    # Calculate dataset-wide statistics
    all_labels = [entry['movement_label'] for entry in entries]
    all_class_counts = Counter(all_labels)
    all_exercises = [entry['exercise_type'] for entry in entries]
    all_exercise_counts = Counter(all_exercises)
    
    print_diagnostics(
        title="Dataset Overview",
        subject_ids=subjects,
        num_samples=len(entries),
        class_distribution=dict(all_class_counts),
        exercise_distribution=dict(all_exercise_counts),
        debug=args.debug
    )
    
    writer = SummaryWriter(str(LOG_DIR))
    
    fold_results: List[Dict[str, Any]] = []
    experiment_metadata = {
        'timestamp': format_timestamp(),
        'parameters': GLOBAL_CONFIG,
        'subjects': subjects,
        'folds_evaluated': [],
        'fold_metrics': {}
    }
    
    # Run folds
    for subject_id in subjects:
        if args.fold and args.fold != subject_id:
            continue  # Skip if single fold requested and doesn't match
            
        # Extract splits manually to pass entries
        subject_entries_train = [e for e in entries if e['subject_id'] != subject_id]
        subject_entries_val = [e for e in entries if e['subject_id'] == subject_id]
        
        train_dataset = IntelliRehabSequenceDataset(subject_entries_train, augment=True, sequence_length=args.sequence_length)
        val_dataset = IntelliRehabSequenceDataset(subject_entries_val, augment=False, sequence_length=args.sequence_length)
        
        sampler = make_weighted_sampler(subject_entries_train, target_key='movement_label')
        
        pin_mem = device.type == 'cuda'
        train_loader = DataLoader(
            train_dataset,
            batch_size=args.batch_size,
            sampler=sampler,
            num_workers=TRAINING_CONFIG['num_workers'],
            collate_fn=partial(sequence_collate_fn, max_length=args.sequence_length),
            pin_memory=pin_mem,
        )
        val_loader = DataLoader(
            val_dataset,
            batch_size=args.batch_size,
            shuffle=False,
            num_workers=TRAINING_CONFIG['num_workers'],
            collate_fn=partial(sequence_collate_fn, max_length=args.sequence_length),
            pin_memory=pin_mem,
        )
        
        model = build_model().to(device)
        fold_name = f'fold_subject_{subject_id}'
        
        # Calculate fold training split statistics
        train_labels = [entry['movement_label'] for entry in subject_entries_train]
        train_class_counts = Counter(train_labels)
        train_exercises = [entry['exercise_type'] for entry in subject_entries_train]
        train_exercise_counts = Counter(train_exercises)
        train_subject_ids = sorted(list({entry['subject_id'] for entry in subject_entries_train}))
        
        print_diagnostics(
            title=f"Fold {subject_id} Configuration",
            subject_ids=train_subject_ids,
            num_samples=len(subject_entries_train),
            class_distribution=dict(train_class_counts),
            exercise_distribution=dict(train_exercise_counts),
            val_subject=subject_id,
            model=model,
            device=device,
            debug=args.debug
        )
        
        # Resume if requested
        if args.resume:
            print(f"Resuming weights from checkpoint: {args.resume}")
            model.load_state_dict(torch.load(args.resume, map_location=device)['model_state'])
            
        val_metrics, val_attentions, _, _ = run_fold(
            model, 
            train_loader, 
            val_loader, 
            subject_entries_train, 
            fold_name, 
            device, 
            args, 
            writer
        )
        
        fold_results.append(val_metrics)
        
        # Save checkpoints
        checkpoint_path = CHECKPOINT_DIR / f'fold_{subject_id}.pt'
        save_checkpoint({
            'model_state': model.state_dict(),
            'subject_id': subject_id,
            'metrics': val_metrics
        }, str(checkpoint_path))
        
        # Save validation attention weights for paper visualization
        attn_save_path = LOG_DIR / f'attention_outputs_fold_{subject_id}.json'
        with open(attn_save_path, 'w') as f:
            json.dump(val_attentions, f, indent=2)
            
        print(f"Validation metrics for Fold {subject_id}:")
        print(f"  Acc: {val_metrics['accuracy']:.4f} | Balanced Acc: {val_metrics['balanced_accuracy']:.4f} | F1: {val_metrics['f1_macro']:.4f} | MCC: {val_metrics['mcc']:.4f}")
        
        experiment_metadata['folds_evaluated'].append(subject_id)
        experiment_metadata['fold_metrics'][subject_id] = {
            'accuracy': val_metrics['accuracy'],
            'balanced_accuracy': val_metrics['balanced_accuracy'],
            'precision_macro': val_metrics['precision_macro'],
            'recall_macro': val_metrics['recall_macro'],
            'f1_macro': val_metrics['f1_macro'],
            'mcc': val_metrics['mcc'],
            'cohen_kappa': val_metrics['cohen_kappa']
        }
        
    # Aggregate and log final experiments
    if fold_results:
        aggregate = aggregate_fold_metrics(fold_results)
        experiment_metadata['overall_averages'] = aggregate
        
        # Save experiment summary
        metadata_path = LOG_DIR / f'experiment_metadata_{format_timestamp()}.json'
        with open(metadata_path, 'w') as f:
            json.dump(experiment_metadata, f, indent=2)
            
        # Save global best state (last fold model as global baseline weights)
        torch.save({'model_state': model.state_dict()}, str(MODEL_WEIGHTS))
        torch.save({'model_state': model.state_dict()}, str(CHECKPOINT_DIR / 'best_model.pt'))
        
        print('\n=========================================')
        print('LOSO Cross-Validation Training Completed')
        print('=========================================')
        print('Average Aggregated Metrics:')
        for k, v in aggregate.items():
            print(f"  {k.replace('_', ' ').title()}: {v:.4f}")
            
    writer.close()

if __name__ == '__main__':
    main()
