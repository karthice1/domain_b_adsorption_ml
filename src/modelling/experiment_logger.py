"""
Experiment Logger Module for Domain B Adsorption ML Package.
Maintains the centralized, reproducible experiment registry for model tracking.
"""

import os
import pandas as pd
from datetime import datetime

DEFAULT_REGISTRY_PATH = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', '..', 'results', 'DOMAIN_B_EXPERIMENT_REGISTRY.csv'
))

REGISTRY_COLUMNS = [
    'Experiment_ID',
    'Timestamp',
    'Domain',
    'Subgroup_or_Analyte',
    'Target_Variable',
    'Task_Type',
    'Model_Family',
    'Model_Name',
    'Is_Baseline',
    'Validation_Scheme',
    'Grouping_Key',
    'N_Train_Avg',
    'N_Test_Total',
    'Primary_Metric_Name',
    'Primary_Metric_Value',
    'RMSE',
    'R2_OOD',
    'MedAE',
    'Hyperparameters',
    'Random_Seed',
    'Runtime_Seconds',
    'Status',
    'Artifact_Path',
    'Notes'
]

def init_registry(registry_path=None):
    """
    Initialize the experiment registry CSV if it does not already exist.
    """
    path = registry_path or os.environ.get('EXPERIMENT_REGISTRY_PATH', DEFAULT_REGISTRY_PATH)
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    if not os.path.exists(path):
        df = pd.DataFrame(columns=REGISTRY_COLUMNS)
        df.to_csv(path, index=False)
        print(f"[REGISTRY] Initialized experiment registry at: {path}")
    return path

def log_experiment(record_dict, registry_path=None):
    """
    Log an experiment run to the registry CSV.
    Missing fields are filled with None/NaN.
    """
    path = init_registry(registry_path)
    df_reg = pd.read_csv(path)
    
    # Ensure timestamp
    if 'Timestamp' not in record_dict or not record_dict['Timestamp']:
        record_dict['Timestamp'] = datetime.now().isoformat()
        
    # Construct complete row
    row = {col: record_dict.get(col, None) for col in REGISTRY_COLUMNS}
    df_new = pd.DataFrame([row])
    
    # Check if Experiment_ID already exists, update or append
    exp_id = record_dict.get('Experiment_ID')
    if exp_id and exp_id in df_reg['Experiment_ID'].values:
        idx = df_reg[df_reg['Experiment_ID'] == exp_id].index[0]
        for col in REGISTRY_COLUMNS:
            df_reg.at[idx, col] = row[col]
        df_reg.to_csv(path, index=False)
        print(f"[REGISTRY] Updated experiment {exp_id} in {path}")
    else:
        df_new.to_csv(path, mode='a', header=False, index=False)
        print(f"[REGISTRY] Logged experiment {exp_id} to {path}")
