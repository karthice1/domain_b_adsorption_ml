"""
Evaluation Metrics Module for Domain B Heavy-Metal Carbon Adsorption ML.
Implements primary (MAE) and secondary (RMSE, R2_OOD, MedAE, MaxAE) evaluation metrics.
"""

import numpy as np
from sklearn.metrics import (
    mean_absolute_error,
    root_mean_squared_error,
    r2_score,
    median_absolute_error
)

def compute_regression_metrics(y_true, y_pred, y_train_mean=None):
    """
    Compute continuous regression metrics for kinetic uptake prediction.
    
    Parameters
    ----------
    y_true : array-like
        True kinetic uptake observations (qt, mg/g).
    y_pred : array-like
        Predicted kinetic uptake values (qt, mg/g).
    y_train_mean : float or array-like, optional
        Mean of training observations to compute out-of-distribution R2 (R2_OOD).
        If None, computes standard sample R2.
        
    Returns
    -------
    dict
        Dictionary containing MAE, RMSE, R2, MedAE, MaxAE, and N.
    """
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    
    mae = mean_absolute_error(y_true, y_pred)
    rmse = root_mean_squared_error(y_true, y_pred)
    medae = median_absolute_error(y_true, y_pred)
    max_err = float(np.max(np.abs(y_true - y_pred)))
    
    # Calculate out-of-sample R2
    # If y_train_mean is provided, calculate true out-of-distribution R2 vs training mean baseline
    # Otherwise standard sklearn r2_score
    if y_train_mean is not None and np.sum((y_true - y_train_mean) ** 2) > 1e-12:
        ss_res = np.sum((y_true - y_pred) ** 2)
        ss_tot = np.sum((y_true - y_train_mean) ** 2)
        r2 = float(1.0 - (ss_res / ss_tot))
    else:
        var_y = np.var(y_true)
        if var_y < 1e-12:
            r2 = float('nan')
        else:
            r2 = float(r2_score(y_true, y_pred))
            
    return {
        'MAE': float(mae),
        'RMSE': float(rmse),
        'R2': float(r2),
        'MedAE': float(medae),
        'MaxAE': float(max_err),
        'N': int(len(y_true))
    }
