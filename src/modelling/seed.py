"""
Seed and Reproducibility Infrastructure for Domain B Adsorption ML Package.
Ensures deterministic random states across NumPy, Python random, Scikit-learn, and OS hash seed.
"""

import os
import random
import numpy as np

GLOBAL_SEED = 42

def set_seed(seed=GLOBAL_SEED):
    """
    Set global random seeds for reproducibility.
    
    Parameters
    ----------
    seed : int, default=42
        Integer seed value.
        
    Returns
    -------
    int
        The seed value configured.
    """
    random.seed(seed)
    np.random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    return seed

def get_seed():
    """Return the global random seed."""
    return GLOBAL_SEED
