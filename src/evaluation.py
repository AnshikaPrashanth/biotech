from typing import Dict, List, Optional, Tuple

import numpy as np
from sklearn import metrics

def classification_report(targets: List[int], predictions: List[int], labels: Optional[List[str]] = None) -> Dict[str, object]:
    # Ensure scikit-learn maps integer targets [0, 1] to target_names even if one class is missing
    if labels is not None and len(labels) == 2:
        report = metrics.classification_report(targets, predictions, labels=[0, 1], target_names=labels, output_dict=True, zero_division=0)
    else:
        report = metrics.classification_report(targets, predictions, target_names=labels, output_dict=True, zero_division=0)
    return report

def confusion_matrix(targets: List[int], predictions: List[int]) -> np.ndarray:
    return metrics.confusion_matrix(targets, predictions, labels=[0, 1])

def roc_auc_scores(targets: List[int], probabilities: List[float]) -> Dict[str, object]:
    unique_targets = set(targets)
    if len(unique_targets) <= 1:
        auc_val = 1.0 if (0 in unique_targets and all(p < 0.5 for p in probabilities)) or (1 in unique_targets and all(p >= 0.5 for p in probabilities)) else 0.5
        return {
            'fpr': [0.0, 1.0],
            'tpr': [0.0, 1.0],
            'thresholds': [0.0, 1.0],
            'auc': float(auc_val),
        }
    fpr, tpr, thresholds = metrics.roc_curve(targets, probabilities)
    return {
        'fpr': fpr.tolist(),
        'tpr': tpr.tolist(),
        'thresholds': thresholds.tolist(),
        'auc': float(metrics.auc(fpr, tpr)),
    }

def precision_recall_curve(targets: List[int], probabilities: List[float]) -> Dict[str, object]:
    unique_targets = set(targets)
    if len(unique_targets) <= 1:
        ap_val = 1.0 if (0 in unique_targets and all(p < 0.5 for p in probabilities)) or (1 in unique_targets and all(p >= 0.5 for p in probabilities)) else 0.5
        return {
            'precision': [1.0, 1.0],
            'recall': [1.0, 0.0],
            'thresholds': [0.0],
            'average_precision': float(ap_val),
        }
    precision, recall, thresholds = metrics.precision_recall_curve(targets, probabilities)
    return {
        'precision': precision.tolist(),
        'recall': recall.tolist(),
        'thresholds': thresholds.tolist(),
        'average_precision': float(metrics.average_precision_score(targets, probabilities)),
    }

def matthews_corrcoef(targets: List[int], predictions: List[int]) -> float:
    if len(set(targets)) <= 1 or len(set(predictions)) <= 1:
        return 0.0
    return float(metrics.matthews_corrcoef(targets, predictions))

def cohen_kappa_score(targets: List[int], predictions: List[int]) -> float:
    if len(set(targets)) <= 1:
        return 1.0 if all(t == p for t, p in zip(targets, predictions)) else 0.0
    return float(metrics.cohen_kappa_score(targets, predictions))

def balanced_accuracy_score(targets: List[int], predictions: List[int]) -> float:
    if len(set(targets)) <= 1:
        return float(np.mean(np.array(targets) == np.array(predictions)))
    return float(metrics.balanced_accuracy_score(targets, predictions))

def aggregate_fold_metrics(fold_results: List[Dict[str, object]]) -> Dict[str, float]:
    metrics_list = {
        'accuracy': [],
        'balanced_accuracy': [],
        'precision_macro': [],
        'recall_macro': [],
        'f1_macro': [],
        'mcc': [],
        'cohen_kappa': []
    }
    for fold in fold_results:
        metrics_list['accuracy'].append(float(fold['accuracy']))
        metrics_list['balanced_accuracy'].append(float(fold.get('balanced_accuracy', fold['accuracy'])))
        metrics_list['precision_macro'].append(float(fold['precision_macro']))
        metrics_list['recall_macro'].append(float(fold['recall_macro']))
        metrics_list['f1_macro'].append(float(fold['f1_macro']))
        metrics_list['mcc'].append(float(fold['mcc']))
        metrics_list['cohen_kappa'].append(float(fold.get('cohen_kappa', 0.0)))
        
    return {k: float(np.mean(v)) for k, v in metrics_list.items()}
