import numpy as np
from typing import Dict, Any, List, Tuple

def confidence_based_abstention(
    probabilities: np.ndarray,
    threshold: float = 0.70
) -> Tuple[int, str, float, float]:
    """Applies confidence-based thresholding for abstention.
    
    Parameters:
        probabilities: np.ndarray of shape (2,) representing [P(Healthy), P(Compensated)]
        threshold: float, decision confidence threshold
        
    Returns:
        pred_class: int (0 or 1)
        decision: str ("Healthy", "Compensated", or "Uncertain / Human Review")
        confidence: float, probability of the predicted class
        uncertainty: float, 1.0 - confidence
    """
    pred_class = int(np.argmax(probabilities))
    confidence = float(probabilities[pred_class])
    uncertainty = 1.0 - confidence
    
    if confidence >= threshold:
        decision = "Compensated" if pred_class == 1 else "Healthy"
    else:
        decision = "Uncertain / Human Review"
        
    return pred_class, decision, confidence, uncertainty

def compute_ece_mce(
    targets: np.ndarray,
    probabilities: np.ndarray,
    n_bins: int = 10
) -> Tuple[float, float]:
    """Computes Expected Calibration Error (ECE) and Maximum Calibration Error (MCE) for class 1 probabilities."""
    preds = (probabilities[:, 1] >= 0.5).astype(int)
    confs = np.max(probabilities, axis=1)
    
    bin_edges = np.linspace(0.0, 1.0, n_bins + 1)
    ece, mce = 0.0, 0.0
    n = len(targets)
    
    for lo, hi in zip(bin_edges[:-1], bin_edges[1:]):
        mask = (confs >= lo) & (confs < hi)
        if not mask.any():
            continue
        acc_b = float(np.mean(preds[mask] == targets[mask]))
        conf_b = float(np.mean(confs[mask]))
        cal_err = abs(acc_b - conf_b)
        ece += cal_err * mask.sum() / n
        mce = max(mce, cal_err)
        
    return float(ece), float(mce)

def evaluate_uncertainty(
    targets: np.ndarray,
    probabilities: np.ndarray,
    threshold: float = 0.70
) -> Dict[str, Any]:
    """Evaluates accuracy, selective accuracy, coverage, and ECE at a given confidence threshold."""
    preds = np.argmax(probabilities, axis=1)
    confs = np.max(probabilities, axis=1)
    
    covered_mask = confs >= threshold
    coverage = float(np.mean(covered_mask))
    
    total_acc = float(np.mean(preds == targets))
    
    if covered_mask.any():
        selective_acc = float(np.mean(preds[covered_mask] == targets[covered_mask]))
    else:
        selective_acc = 1.0  # Perfect accuracy on empty set by definition
        
    ece, mce = compute_ece_mce(targets, probabilities)
    
    return {
        "accuracy": total_acc,
        "selective_accuracy": selective_acc,
        "coverage": coverage,
        "ece": ece,
        "mce": mce,
        "uncertain_sample_rate": 1.0 - coverage
    }

def compute_risk_coverage_curve(
    targets: np.ndarray,
    probabilities: np.ndarray,
    steps: int = 100
) -> Dict[str, List[float]]:
    """Generates selective error (risk) and coverage values for different threshold steps."""
    thresholds = np.linspace(0.5, 1.0, steps)
    confs = np.max(probabilities, axis=1)
    preds = np.argmax(probabilities, axis=1)
    
    risk_list = []
    coverage_list = []
    
    for thresh in thresholds:
        covered = confs >= thresh
        cov = float(np.mean(covered))
        
        if covered.any():
            err = float(np.mean(preds[covered] != targets[covered]))
        else:
            err = 0.0
            
        risk_list.append(err)
        coverage_list.append(cov)
        
    return {
        "thresholds": thresholds.tolist(),
        "risk": risk_list,
        "coverage": coverage_list
    }
