"""
Domain B Carbon Adsorption Kinetics Candidate Models Implementation.
Trains and evaluates continuous regression models for dynamic kinetic uptake (qt, mg/g).
Strictly restricted to DR-040B Category 1 (N=438 verified dynamic kinetic observations).
Evaluated across:
- Cr(VI) (N=120): 5-Fold Leave-One-Study-Out CV (LOSO-CV)
- Pb(II) (N=318): Primary 5-Fold Study-Grouped CV (3 studies/fold)
- Pb(II) (N=318): Sensitivity 15-Fold Leave-One-Study-Out CV (LOSO-CV)
Includes candidate sensitivity comparison:
- CARB_MODEL_05A: Unconstrained HistGradientBoostingRegressor
- CARB_MODEL_05B: Monotonic-Contact-Time HistGradientBoostingRegressor (monotonic_cst=+1 on t)
"""

import os
import sys
import json
import time
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge, ElasticNet
from sklearn.ensemble import (
    RandomForestRegressor,
    ExtraTreesRegressor,
    HistGradientBoostingRegressor
)

# Portable imports within package
try:
    from src.modelling.seed import set_seed
    from src.metrics.metrics import compute_regression_metrics
    from src.modelling.experiment_logger import log_experiment
except ImportError:
    # Fallback if executed directly from inside src/modelling/
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from src.modelling.seed import set_seed
    from src.metrics.metrics import compute_regression_metrics
    from src.modelling.experiment_logger import log_experiment


def parse_args():
    parser = argparse.ArgumentParser(description="Run Domain B Heavy-Metal Carbon Adsorption ML Models.")
    parser.add_argument(
        "--features",
        type=str,
        default=None,
        help="Path to PHASE2B_REMEDIATION_CARBON_FEATURE_MATRIX_CORRECTED.csv"
    )
    parser.add_argument(
        "--register",
        type=str,
        default=None,
        help="Path to DR040B_DOMAIN_B_RECORD_EVIDENCE_REGISTER.csv"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=None,
        help="Directory to save out-of-fold prediction CSVs"
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed (default: 42)"
    )
    return parser.parse_args()


def resolve_default_paths(args):
    # Locate repository root if available
    script_dir = Path(__file__).resolve().parent
    pkg_root = script_dir.parents[1]
    repo_root = pkg_root.parent.parent  # /Users/karthik/research_project

    features_path = args.features
    if features_path is None:
        candidate_paths = [
            repo_root / "phase2b" / "phase2b_bounded_closeout" / "PHASE2B_REMEDIATION_CARBON_FEATURE_MATRIX_CORRECTED.csv",
            repo_root / "phase2b" / "versioned_dr025_corrections" / "PHASE2B_REMEDIATION_CARBON_FEATURE_MATRIX_CORRECTED.csv",
            pkg_root / "sample_data" / "mock_kinetic_features_sample.csv"
        ]
        for cp in candidate_paths:
            if cp.exists():
                features_path = str(cp)
                break

    register_path = args.register
    if register_path is None:
        candidate_paths = [
            repo_root / "phase3" / "versioned_phase3_protocol_freeze" / "dr040b_reconciliation" / "DR040B_DOMAIN_B_RECORD_EVIDENCE_REGISTER.csv",
            pkg_root / "sample_data" / "mock_record_evidence_register.csv"
        ]
        for cp in candidate_paths:
            if cp.exists():
                register_path = str(cp)
                break

    output_dir = args.output_dir
    if output_dir is None:
        output_dir = str(pkg_root / "results")

    return features_path, register_path, output_dir


def run_carbon_models(features_path=None, register_path=None, output_dir=None, seed=42):
    set_seed(seed)
    print("\n=======================================================")
    print("   RUNNING DOMAIN B CARBON CANDIDATE MODELS")
    print("=======================================================")

    if features_path is None or not os.path.exists(features_path):
        raise FileNotFoundError(f"Feature matrix not found: {features_path}")
    if register_path is None or not os.path.exists(register_path):
        raise FileNotFoundError(f"Evidence register not found: {register_path}")

    os.makedirs(output_dir, exist_ok=True)

    print(f"Loading feature matrix from: {features_path}")
    carb_feat = pd.read_csv(features_path)
    print(f"Loading record evidence register from: {register_path}")
    carb_reg = pd.read_csv(register_path)

    # Merge classification metadata
    df = carb_feat.merge(
        carb_reg[['Record_ID', 'Classification', 'Primary_Kinetic_Dataset_Inclusion', 'Literature_Reference', 'Heavy_Metal_Analyte']],
        on=['Record_ID', 'Literature_Reference', 'Heavy_Metal_Analyte']
    )

    # Filter Category 1
    cat1_df = df[df['Classification'] == '1_Directly_reported_kinetic_qt'].copy().reset_index(drop=True)
    assert len(cat1_df) == 438, f"Expected 438 Category 1 records, got {len(cat1_df)}"

    feature_cols = [
        'Contact_Time_min', 'Initial_Concentration_mg_L', 'Adsorbent_Dose_g_L',
        'Solution_pH', 'Solution_Temperature_C', 'BET_Surface_Area_m2_g',
        'Pore_Diameter_nm', 'Total_Pore_Volume_cm3_g', 'BET_over_Pore_Volume',
        'Pore_Area_Product', 'Specific_Loading_C0_over_dose', 'Mass_Transfer_Product'
    ]

    # Monotonic constraint: +1 for Contact_Time_min (index 0), 0 for all other features
    monotonic_cst = [1] + [0] * (len(feature_cols) - 1)

    # -------------------------------------------------------------
    # 1. Cr(VI) Kinetic Uptake: 5-Fold LOSO-CV (N=120)
    # -------------------------------------------------------------
    print("\n--- Training Cr(VI) Kinetic Models (5-Fold LOSO-CV, N=120) ---")
    cr_df = cat1_df[cat1_df['Heavy_Metal_Analyte'] == 'Cr(VI)'].copy().reset_index(drop=True)
    cr_studies = cr_df['Literature_Reference'].unique().tolist()
    assert len(cr_studies) == 5, f"Expected 5 Cr(VI) studies, got {len(cr_studies)}"

    cr_models = {
        'CARB_MODEL_01_Ridge': Ridge(alpha=1.0, random_state=42),
        'CARB_MODEL_02_ElasticNet': ElasticNet(alpha=0.1, l1_ratio=0.5, random_state=42),
        'CARB_MODEL_03_RandomForest': RandomForestRegressor(n_estimators=300, max_depth=8, min_samples_leaf=2, random_state=42, n_jobs=-1),
        'CARB_MODEL_04_ExtraTrees': ExtraTreesRegressor(n_estimators=300, max_depth=8, min_samples_leaf=2, random_state=42, n_jobs=-1),
        'CARB_MODEL_05A_HistGradientBoosting_Unconstrained': HistGradientBoostingRegressor(max_iter=150, max_depth=5, min_samples_leaf=3, learning_rate=0.05, random_state=42),
        'CARB_MODEL_05B_HistGradientBoosting_Monotonic': HistGradientBoostingRegressor(max_iter=150, max_depth=5, min_samples_leaf=3, learning_rate=0.05, monotonic_cst=monotonic_cst, random_state=42)
    }

    cr_oof = cr_df[['Record_ID', 'Literature_Reference', 'Contact_Time_min', 'Kinetic_Capacity_qt_mg_g']].copy()

    for m_id, model in cr_models.items():
        t0 = time.time()
        oof_col = f'Pred_Cr_{m_id}'
        cr_oof[oof_col] = np.nan
        train_counts = []

        for study in cr_studies:
            train_idx = cr_df.index[cr_df['Literature_Reference'] != study].tolist()
            test_idx = cr_df.index[cr_df['Literature_Reference'] == study].tolist()
            train_counts.append(len(train_idx))

            X_train = cr_df.loc[train_idx, feature_cols]
            y_train = cr_df.loc[train_idx, 'Kinetic_Capacity_qt_mg_g'].values
            X_test = cr_df.loc[test_idx, feature_cols]

            if 'Ridge' in m_id or 'ElasticNet' in m_id:
                pipe = Pipeline([('scaler', StandardScaler()), ('reg', model)])
            else:
                pipe = model

            pipe.fit(X_train, y_train)
            pred = pipe.predict(X_test)
            cr_oof.loc[test_idx, oof_col] = np.maximum(pred, 0.0)

        elapsed = time.time() - t0
        m = compute_regression_metrics(cr_oof['Kinetic_Capacity_qt_mg_g'], cr_oof[oof_col])
        print(f"  [{m_id}] Pooled MAE: {m['MAE']:.3f} mg/g, RMSE: {m['RMSE']:.3f}, R2_OOD: {m['R2']:.4f}, MedAE: {m['MedAE']:.3f} ({elapsed:.1f}s)")

        log_experiment({
            'Experiment_ID': f"EXP_CARB_CR_{m_id}",
            'Domain': 'Domain_B_Carbon_Kinetic',
            'Subgroup_or_Analyte': 'Cr(VI)',
            'Target_Variable': 'Kinetic_Capacity_qt_mg_g',
            'Task_Type': 'Continuous_Regression',
            'Model_Family': m_id.split('_')[2],
            'Model_Name': m_id,
            'Is_Baseline': False,
            'Validation_Scheme': '5-Fold Leave-One-Study-Out CV (LOSO-CV)',
            'Grouping_Key': 'Literature_Reference',
            'N_Train_Avg': float(np.mean(train_counts)),
            'N_Test_Total': 120,
            'Primary_Metric_Name': 'MAE',
            'Primary_Metric_Value': m['MAE'],
            'RMSE': m['RMSE'],
            'R2_OOD': m['R2'],
            'MedAE': m['MedAE'],
            'Hyperparameters': json.dumps(model.get_params()),
            'Random_Seed': 42,
            'Runtime_Seconds': round(elapsed, 2),
            'Status': 'COMPLETED',
            'Artifact_Path': os.path.join(output_dir, 'CARB_CR_CANDIDATE_OOF_PREDICTIONS.csv'),
            'Notes': f"Cr(VI) candidate kinetic model under 5-Fold LOSO-CV. Monotonic: {'Yes' if 'Monotonic' in m_id else 'No'}."
        }, registry_path=os.path.join(output_dir, 'DOMAIN_B_EXPERIMENT_REGISTRY.csv'))

    cr_pred_path = os.path.join(output_dir, 'CARB_CR_CANDIDATE_OOF_PREDICTIONS.csv')
    cr_oof.to_csv(cr_pred_path, index=False)
    print(f"Saved Cr(VI) OOF predictions to: {cr_pred_path}")

    # -------------------------------------------------------------
    # 2. Pb(II) Kinetic Uptake: Primary 5-Fold Study-Grouped CV (N=318)
    # -------------------------------------------------------------
    print("\n--- Training Pb(II) Kinetic Models (Primary 5-Fold Study-Grouped CV, N=318) ---")
    pb_df = cat1_df[cat1_df['Heavy_Metal_Analyte'] == 'Pb(II)'].copy().reset_index(drop=True)
    pb_studies = pb_df['Literature_Reference'].unique().tolist()
    assert len(pb_studies) == 15, f"Expected 15 Pb(II) studies, got {len(pb_studies)}"

    # Standard 5-fold grouping (3 studies per fold)
    sorted_studies = sorted(pb_studies)
    study_to_fold = {s: i % 5 for i, s in enumerate(sorted_studies)}
    pb_df['Study_Grouped_Fold'] = pb_df['Literature_Reference'].map(study_to_fold)

    pb_models = {
        'CARB_MODEL_01_Ridge': Ridge(alpha=1.0, random_state=42),
        'CARB_MODEL_02_ElasticNet': ElasticNet(alpha=0.1, l1_ratio=0.5, random_state=42),
        'CARB_MODEL_03_RandomForest': RandomForestRegressor(n_estimators=300, max_depth=8, min_samples_leaf=2, random_state=42, n_jobs=-1),
        'CARB_MODEL_04_ExtraTrees': ExtraTreesRegressor(n_estimators=300, max_depth=8, min_samples_leaf=2, random_state=42, n_jobs=-1),
        'CARB_MODEL_05A_HistGradientBoosting_Unconstrained': HistGradientBoostingRegressor(max_iter=150, max_depth=5, min_samples_leaf=3, learning_rate=0.05, random_state=42),
        'CARB_MODEL_05B_HistGradientBoosting_Monotonic': HistGradientBoostingRegressor(max_iter=150, max_depth=5, min_samples_leaf=3, learning_rate=0.05, monotonic_cst=monotonic_cst, random_state=42)
    }

    pb_oof = pb_df[['Record_ID', 'Literature_Reference', 'Study_Grouped_Fold', 'Contact_Time_min', 'Kinetic_Capacity_qt_mg_g']].copy()

    for m_id, model in pb_models.items():
        t0 = time.time()
        oof_col = f'Pred_Pb_Grouped_{m_id}'
        pb_oof[oof_col] = np.nan
        train_counts = []

        for f in range(5):
            train_idx = pb_df.index[pb_df['Study_Grouped_Fold'] != f].tolist()
            test_idx = pb_df.index[pb_df['Study_Grouped_Fold'] == f].tolist()
            train_counts.append(len(train_idx))

            X_train = pb_df.loc[train_idx, feature_cols]
            y_train = pb_df.loc[train_idx, 'Kinetic_Capacity_qt_mg_g'].values
            X_test = pb_df.loc[test_idx, feature_cols]

            if 'Ridge' in m_id or 'ElasticNet' in m_id:
                pipe = Pipeline([('scaler', StandardScaler()), ('reg', model)])
            else:
                pipe = model

            pipe.fit(X_train, y_train)
            pred = pipe.predict(X_test)
            pb_oof.loc[test_idx, oof_col] = np.maximum(pred, 0.0)

        elapsed = time.time() - t0
        m = compute_regression_metrics(pb_oof['Kinetic_Capacity_qt_mg_g'], pb_oof[oof_col])
        print(f"  [{m_id}] Pooled MAE: {m['MAE']:.3f} mg/g, RMSE: {m['RMSE']:.3f}, R2_OOD: {m['R2']:.4f}, MedAE: {m['MedAE']:.3f} ({elapsed:.1f}s)")

        log_experiment({
            'Experiment_ID': f"EXP_CARB_PB_GROUPED_{m_id}",
            'Domain': 'Domain_B_Carbon_Kinetic',
            'Subgroup_or_Analyte': 'Pb(II)',
            'Target_Variable': 'Kinetic_Capacity_qt_mg_g',
            'Task_Type': 'Continuous_Regression',
            'Model_Family': m_id.split('_')[2],
            'Model_Name': m_id,
            'Is_Baseline': False,
            'Validation_Scheme': '5-Fold Study-Grouped CV (3 studies/fold)',
            'Grouping_Key': 'Literature_Reference',
            'N_Train_Avg': float(np.mean(train_counts)),
            'N_Test_Total': 318,
            'Primary_Metric_Name': 'MAE',
            'Primary_Metric_Value': m['MAE'],
            'RMSE': m['RMSE'],
            'R2_OOD': m['R2'],
            'MedAE': m['MedAE'],
            'Hyperparameters': json.dumps(model.get_params()),
            'Random_Seed': 42,
            'Runtime_Seconds': round(elapsed, 2),
            'Status': 'COMPLETED',
            'Artifact_Path': os.path.join(output_dir, 'CARB_PB_CANDIDATE_OOF_PREDICTIONS.csv'),
            'Notes': f"Pb(II) primary candidate kinetic model under 5-Fold Study-Grouped CV. Monotonic: {'Yes' if 'Monotonic' in m_id else 'No'}."
        }, registry_path=os.path.join(output_dir, 'DOMAIN_B_EXPERIMENT_REGISTRY.csv'))

    # -------------------------------------------------------------
    # 3. Pb(II) Kinetic Uptake: Sensitivity 15-Fold LOSO-CV (N=318)
    # -------------------------------------------------------------
    print("\n--- Training Pb(II) Kinetic Models (Sensitivity 15-Fold LOSO-CV, N=318) ---")
    for m_id in ['CARB_MODEL_05A_HistGradientBoosting_Unconstrained', 'CARB_MODEL_05B_HistGradientBoosting_Monotonic']:
        model = pb_models[m_id]
        t0 = time.time()
        oof_col = f'Pred_Pb_LOSO15_{m_id}'
        pb_oof[oof_col] = np.nan
        train_counts = []

        for s in sorted_studies:
            train_idx = pb_df.index[pb_df['Literature_Reference'] != s].tolist()
            test_idx = pb_df.index[pb_df['Literature_Reference'] == s].tolist()
            train_counts.append(len(train_idx))

            X_train = pb_df.loc[train_idx, feature_cols]
            y_train = pb_df.loc[train_idx, 'Kinetic_Capacity_qt_mg_g'].values
            X_test = pb_df.loc[test_idx, feature_cols]

            pipe = model
            pipe.fit(X_train, y_train)
            pred = pipe.predict(X_test)
            pb_oof.loc[test_idx, oof_col] = np.maximum(pred, 0.0)

        elapsed = time.time() - t0
        m = compute_regression_metrics(pb_oof['Kinetic_Capacity_qt_mg_g'], pb_oof[oof_col])
        print(f"  [Sensitivity 15-Fold LOSO - {m_id}] Pooled MAE: {m['MAE']:.3f} mg/g, RMSE: {m['RMSE']:.3f}, R2_OOD: {m['R2']:.4f}, MedAE: {m['MedAE']:.3f} ({elapsed:.1f}s)")

        log_experiment({
            'Experiment_ID': f"EXP_CARB_PB_LOSO15_{m_id}",
            'Domain': 'Domain_B_Carbon_Kinetic',
            'Subgroup_or_Analyte': 'Pb(II)',
            'Target_Variable': 'Kinetic_Capacity_qt_mg_g',
            'Task_Type': 'Continuous_Regression',
            'Model_Family': m_id.split('_')[2],
            'Model_Name': m_id,
            'Is_Baseline': False,
            'Validation_Scheme': '15-Fold Leave-One-Study-Out CV (LOSO-CV)',
            'Grouping_Key': 'Literature_Reference',
            'N_Train_Avg': float(np.mean(train_counts)),
            'N_Test_Total': 318,
            'Primary_Metric_Name': 'MAE',
            'Primary_Metric_Value': m['MAE'],
            'RMSE': m['RMSE'],
            'R2_OOD': m['R2'],
            'MedAE': m['MedAE'],
            'Hyperparameters': json.dumps(model.get_params()),
            'Random_Seed': 42,
            'Runtime_Seconds': round(elapsed, 2),
            'Status': 'COMPLETED',
            'Artifact_Path': os.path.join(output_dir, 'CARB_PB_CANDIDATE_OOF_PREDICTIONS.csv'),
            'Notes': f"Pb(II) sensitivity candidate kinetic model under 15-Fold LOSO-CV. Monotonic: {'Yes' if 'Monotonic' in m_id else 'No'}."
        }, registry_path=os.path.join(output_dir, 'DOMAIN_B_EXPERIMENT_REGISTRY.csv'))

    pb_pred_path = os.path.join(output_dir, 'CARB_PB_CANDIDATE_OOF_PREDICTIONS.csv')
    pb_oof.to_csv(pb_pred_path, index=False)
    print(f"\nSaved Pb(II) out-of-fold predictions to: {pb_pred_path}")
    print("=======================================================\n")


if __name__ == '__main__':
    args = parse_args()
    feat_p, reg_p, out_d = resolve_default_paths(args)
    run_carbon_models(feat_p, reg_p, out_d, args.seed)
