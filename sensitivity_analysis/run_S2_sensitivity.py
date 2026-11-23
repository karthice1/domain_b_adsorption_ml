"""
Domain B — S2 Provenance Sensitivity Pipeline.
Evaluates the impact of excluding 40 records with provenance ambiguity (N=398 vs S0 N=438).
Computes the exact 18 canonical model and baseline rows under identical hyperparameter and fold configurations.
"""

import os
import sys
import json
import hashlib
import platform
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
from sklearn.metrics import mean_absolute_error, median_absolute_error, r2_score

# Portable path resolution
SCRIPT_DIR = Path(__file__).resolve().parent
PKG_ROOT = SCRIPT_DIR.parent
REPO_ROOT = PKG_ROOT.parent.parent

DEFAULT_FEAT = REPO_ROOT / "phase2b" / "phase2b_bounded_closeout" / "PHASE2B_REMEDIATION_CARBON_FEATURE_MATRIX_CORRECTED.csv"
DEFAULT_DR = REPO_ROOT / "phase3" / "versioned_phase3_protocol_freeze" / "dr040b_reconciliation" / "DR040B_DOMAIN_B_RECORD_EVIDENCE_REGISTER.csv"
DEFAULT_EXCL = REPO_ROOT / "phase3" / "domain_b_manuscript" / "phase3_4_provenance_review" / "S2_FROZEN_EXCLUSION_LIST.csv"
EXCL_SHA = '0cc91149e50cb8ef50fd5f0bb4c6aea9a6ff9366f8e6dc8ef48877321e351baf'

Y = 'Kinetic_Capacity_qt_mg_g'
FEATURES = [
    'Contact_Time_min', 'Initial_Concentration_mg_L', 'Adsorbent_Dose_g_L',
    'Solution_pH', 'Solution_Temperature_C', 'BET_Surface_Area_m2_g',
    'Pore_Diameter_nm', 'Total_Pore_Volume_cm3_g', 'BET_over_Pore_Volume',
    'Pore_Area_Product', 'Specific_Loading_C0_over_dose', 'Mass_Transfer_Product'
]
MONO = [1] + [0] * (len(FEATURES) - 1)
ORIG_PB_FOLDS = {
    0: ['Depci et al', 'Adebisi et al', 'Kongsune et al'],
    1: ['Acharya et al', 'Alslaibi et al', 'Al-Malack et al'],
    2: ['Boudrahem et al', 'Bohli et al', 'Silva et al'],
    3: ['Mouni et al', 'Siraj et al', 'Heidarinejad et al'],
    4: ['Bouhamed et al', 'Pap et al', 'N. Madani et al']
}


def get_models():
    return {
        'CARB_MODEL_01_Ridge': Ridge(alpha=1.0, random_state=42),
        'CARB_MODEL_02_ElasticNet': ElasticNet(alpha=0.1, l1_ratio=0.5, random_state=42),
        'CARB_MODEL_03_RandomForest': RandomForestRegressor(n_estimators=300, max_depth=8, min_samples_leaf=2, random_state=42, n_jobs=-1),
        'CARB_MODEL_04_ExtraTrees': ExtraTreesRegressor(n_estimators=300, max_depth=8, min_samples_leaf=2, random_state=42, n_jobs=-1),
        'CARB_MODEL_05A_HistGradientBoosting_Unconstrained': HistGradientBoostingRegressor(max_iter=150, max_depth=5, min_samples_leaf=3, learning_rate=0.05, random_state=42),
        'CARB_MODEL_05B_HistGradientBoosting_Monotonic': HistGradientBoostingRegressor(max_iter=150, max_depth=5, min_samples_leaf=3, learning_rate=0.05, monotonic_cst=MONO, random_state=42)
    }


def fit_predict(m_id, model, Xtr, ytr, Xte):
    pipe = Pipeline([('scaler', StandardScaler()), ('reg', model)]) if ('Ridge' in m_id or 'ElasticNet' in m_id) else model
    pipe.fit(Xtr, ytr)
    return np.maximum(pipe.predict(Xte), 0.0)


def compute_metrics(y, p):
    y, p = np.asarray(y, float), np.asarray(p, float)
    return {
        'MAE': mean_absolute_error(y, p),
        'RMSE': float(np.sqrt(np.mean((y - p) ** 2))),
        'R2': r2_score(y, p),
        'MedAE': median_absolute_error(y, p)
    }


def fold_metrics(df, col, key):
    ms = [compute_metrics(g[Y], g[col]) for _, g in df.groupby(key)]
    return np.mean([m['MAE'] for m in ms]), np.mean([m['RMSE'] for m in ms])


def load_population(pop, feat_path, dr_path, excl_path):
    np.random.seed(42)
    f = pd.read_csv(feat_path)
    r = pd.read_csv(dr_path)
    df = f.merge(
        r[['Record_ID', 'Classification', 'Primary_Kinetic_Dataset_Inclusion', 'Literature_Reference', 'Heavy_Metal_Analyte']],
        on=['Record_ID', 'Literature_Reference', 'Heavy_Metal_Analyte']
    )
    cat1 = df[df['Classification'] == '1_Directly_reported_kinetic_qt'].copy().reset_index(drop=True)
    assert len(cat1) == 438, f"Expected 438 Category 1 records, got {len(cat1)}"

    excl = []
    if pop == 'S2':
        with open(excl_path, 'rb') as ef:
            sha = hashlib.sha256(ef.read()).hexdigest()
        assert sha == EXCL_SHA, f"Exclusion list checksum mismatch: {sha}"
        excl = pd.read_csv(excl_path).Record_ID.tolist()
        assert len(excl) == 40, f"Expected 40 excluded records, got {len(excl)}"
        cat1 = cat1[~cat1.Record_ID.isin(excl)].reset_index(drop=True)
        assert len(cat1) == 398, f"Expected 398 S2 records, got {len(cat1)}"

    return cat1, excl


def run_sensitivity(pop, feat_path=None, dr_path=None, excl_path=None, output_dir=None):
    t0 = time.time()
    feat_path = feat_path or str(DEFAULT_FEAT)
    dr_path = dr_path or str(DEFAULT_DR)
    excl_path = excl_path or str(DEFAULT_EXCL)
    output_dir = output_dir or str(SCRIPT_DIR / "results" / pop)

    cat1, excl = load_population(pop, feat_path, dr_path, excl_path)
    rows = []

    # ---------------- Cr(VI) 5-fold LOSO ----------------
    cr = cat1[cat1.Heavy_Metal_Analyte == 'Cr(VI)'].copy().reset_index(drop=True)
    cr_studies = cr.Literature_Reference.unique().tolist()
    assert len(cr_studies) == 5, f"Expected 5 Cr studies, got {len(cr_studies)}"
    cr_oof = cr[['Record_ID', 'Literature_Reference', 'Contact_Time_min', Y]].copy()
    cr_oof['Cr_Pred_Median_Baseline'] = np.nan

    for s in cr_studies:
        te = cr.Literature_Reference == s
        cr_oof.loc[te, 'Cr_Pred_Median_Baseline'] = float(np.median(cr.loc[~te, Y]))

    for m_id, model in get_models().items():
        col = f'Pred_Cr_{m_id}'
        cr_oof[col] = np.nan
        for s in cr_studies:
            te = cr.Literature_Reference == s
            cr_oof.loc[te, col] = fit_predict(m_id, model, cr.loc[~te, FEATURES], cr.loc[~te, Y].values, cr.loc[te, FEATURES])

    # ---------------- Pb(II) 5-fold study-grouped (candidate folds) ----------------
    pb = cat1[cat1.Heavy_Metal_Analyte == 'Pb(II)'].copy().reset_index(drop=True)
    pb_studies = pb.Literature_Reference.unique().tolist()
    assert len(pb_studies) == 15, f"Expected 15 Pb studies, got {len(pb_studies)}"
    sorted_studies = sorted(pb_studies)
    pb['Study_Grouped_Fold'] = pb.Literature_Reference.map({s: i % 5 for i, s in enumerate(sorted_studies)})
    pb_oof = pb[['Record_ID', 'Literature_Reference', 'Study_Grouped_Fold', 'Contact_Time_min', Y]].copy()
    pb_oof['Null_AlignedGrouped'] = np.nan
    pb_oof['Null_OrigGrouped'] = np.nan
    pb_oof['Null_LOSO15'] = np.nan

    for f_ in range(5):
        te = pb.Study_Grouped_Fold == f_
        pb_oof.loc[te, 'Null_AlignedGrouped'] = float(np.median(pb.loc[~te, Y]))
    for f_, studies in ORIG_PB_FOLDS.items():
        te = pb.Literature_Reference.isin(studies)
        pb_oof.loc[te, 'Null_OrigGrouped'] = float(np.median(pb.loc[~te, Y]))
    for s in sorted_studies:
        te = pb.Literature_Reference == s
        pb_oof.loc[te, 'Null_LOSO15'] = float(np.median(pb.loc[~te, Y]))

    pbm = get_models()
    for m_id, model in pbm.items():
        col = f'Pred_Pb_Grouped_{m_id}'
        pb_oof[col] = np.nan
        for f_ in range(5):
            te = pb.Study_Grouped_Fold == f_
            pb_oof.loc[te, col] = fit_predict(m_id, model, pb.loc[~te, FEATURES], pb.loc[~te, Y].values, pb.loc[te, FEATURES])

    # ---------------- Pb(II) 15-fold LOSO (HGB only) ----------------
    for m_id in ['CARB_MODEL_05A_HistGradientBoosting_Unconstrained', 'CARB_MODEL_05B_HistGradientBoosting_Monotonic']:
        col = f'Pred_Pb_LOSO15_{m_id}'
        pb_oof[col] = np.nan
        for s in sorted_studies:
            te = pb.Literature_Reference == s
            model = pbm[m_id]
            model.fit(pb.loc[~te, FEATURES], pb.loc[~te, Y].values)
            pb_oof.loc[te, col] = np.maximum(model.predict(pb.loc[te, FEATURES]), 0.0)

    # ---------------- 18 metric rows (canonical row order/identifiers) ----------------
    spec = [('Cr(VI)', 'CARB_BASE_01_Cr_LOSO', cr_oof, 'Cr_Pred_Median_Baseline', 'Literature_Reference')]
    spec += [('Cr(VI)', m, cr_oof, f'Pred_Cr_{m}', 'Literature_Reference') for m in get_models()]
    spec += [
        ('Pb(II)', 'CARB_BASE_01_Pb_OrigGrouped', pb_oof, 'Null_OrigGrouped', None),
        ('Pb(II)', 'CARB_BASE_01_Pb_AlignedGrouped', pb_oof, 'Null_AlignedGrouped', 'Study_Grouped_Fold'),
        ('Pb(II)', 'CARB_BASE_01_Pb_LOSO15', pb_oof, 'Null_LOSO15', 'Literature_Reference')
    ]
    spec += [('Pb(II)', f'{m}_Grouped', pb_oof, f'Pred_Pb_Grouped_{m}', 'Study_Grouped_Fold') for m in get_models()]
    spec += [
        ('Pb(II)', f'{m}_LOSO15', pb_oof, f'Pred_Pb_LOSO15_{m}', 'Literature_Reference')
        for m in ['CARB_MODEL_05A_HistGradientBoosting_Unconstrained', 'CARB_MODEL_05B_HistGradientBoosting_Monotonic']
    ]

    for an, mid, d, col, key in spec:
        m = compute_metrics(d[Y], d[col])
        if mid == 'CARB_BASE_01_Pb_OrigGrouped':
            d2 = d.assign(_f=d.Literature_Reference.map({s: k for k, v in ORIG_PB_FOLDS.items() for s in v}))
            fm = fold_metrics(d2, col, '_f')
        else:
            fm = fold_metrics(d, col, key)
        rows.append({
            'Population': pop,
            'Analyte': an,
            'Model_Identifier': mid,
            'N': len(d),
            'Prediction_Column': col,
            'Pooled_MAE': m['MAE'],
            'Pooled_RMSE': m['RMSE'],
            'Pooled_R2_OOD': m['R2'],
            'Pooled_MedAE': m['MedAE'],
            'Mean_Fold_MAE': fm[0],
            'Mean_Fold_RMSE': fm[1]
        })

    os.makedirs(output_dir, exist_ok=True)
    cr_oof.to_csv(os.path.join(output_dir, f'{pop}_CR_OOF_PREDICTIONS.csv'), index=False)
    pb_oof.to_csv(os.path.join(output_dir, f'{pop}_PB_OOF_PREDICTIONS.csv'), index=False)
    metrics_df = pd.DataFrame(rows)
    metrics_df.to_csv(os.path.join(output_dir, f'{pop}_METRICS_18_ROWS.csv'), index=False)

    meta = {
        'population': pop,
        'n_records': len(cat1),
        'n_excluded': len(excl),
        'runtime_s': round(time.time() - t0, 1),
        'python': platform.python_version(),
        'sklearn': sklearn.__version__,
        'numpy': np.__version__,
        'pandas': pd.__version__,
        'platform': platform.platform()
    }
    with open(os.path.join(output_dir, f'{pop}_RUN_METADATA.json'), 'w') as jf:
        json.dump(meta, jf, indent=2)

    print(f"\n[S2 SENSITIVITY] Completed run for population {pop} ({len(cat1)} records) in {meta['runtime_s']}s")
    print(metrics_df[['Model_Identifier', 'N', 'Pooled_MAE', 'Pooled_RMSE', 'Pooled_R2_OOD']].round(4).to_string())
    return metrics_df


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run Domain B S2 Sensitivity Analysis.")
    parser.add_argument("population", choices=["S0", "S2"], help="Population to evaluate: S0 (N=438) or S2 (N=398)")
    parser.add_argument("--features", default=None, help="Path to feature matrix CSV")
    parser.add_argument("--register", default=None, help="Path to record evidence register CSV")
    parser.add_argument("--exclusion", default=None, help="Path to S2 exclusion list CSV")
    parser.add_argument("--output-dir", default=None, help="Output directory")
    args = parser.parse_args()

    run_sensitivity(args.population, args.features, args.register, args.exclusion, args.output_dir)
