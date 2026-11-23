"""
Domain B Feature Importance and Interpretability Module.
Computes Mean Decrease in Impurity (MDI) feature importances for ensemble models
(ExtraTrees and RandomForest) trained on verified Category 1 dynamic kinetic observations (N=438).
"""

import os
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesRegressor, RandomForestRegressor


def parse_args():
    parser = argparse.ArgumentParser(description="Compute Domain B Feature Importances.")
    parser.add_argument("--features", default=None, help="Path to feature matrix CSV")
    parser.add_argument("--register", default=None, help="Path to record evidence register CSV")
    parser.add_argument("--output-csv", default=None, help="Path to save feature importances CSV")
    return parser.parse_args()


def resolve_paths(args):
    script_dir = Path(__file__).resolve().parent
    pkg_root = script_dir.parents[1]
    repo_root = pkg_root.parent.parent

    feat_p = args.features or str(repo_root / "phase2b" / "phase2b_bounded_closeout" / "PHASE2B_REMEDIATION_CARBON_FEATURE_MATRIX_CORRECTED.csv")
    reg_p = args.register or str(repo_root / "phase3" / "versioned_phase3_protocol_freeze" / "dr040b_reconciliation" / "DR040B_DOMAIN_B_RECORD_EVIDENCE_REGISTER.csv")
    out_p = args.output_csv or str(pkg_root / "results" / "DOMAIN_B_FEATURE_IMPORTANCES.csv")
    return feat_p, reg_p, out_p


def compute_feature_importances(features_path, register_path, output_csv):
    print(f"\n[FEATURE IMPORTANCE] Computing tree-based feature importances for Domain B...")
    feat_df = pd.read_csv(features_path)
    reg_df = pd.read_csv(register_path)

    df = feat_df.merge(
        reg_df[['Record_ID', 'Classification', 'Literature_Reference', 'Heavy_Metal_Analyte']],
        on=['Record_ID', 'Literature_Reference', 'Heavy_Metal_Analyte']
    )
    cat1 = df[df['Classification'] == '1_Directly_reported_kinetic_qt'].copy().reset_index(drop=True)
    assert len(cat1) == 438, f"Expected 438 Category 1 records, got {len(cat1)}"

    feature_cols = [
        'Contact_Time_min', 'Initial_Concentration_mg_L', 'Adsorbent_Dose_g_L',
        'Solution_pH', 'Solution_Temperature_C', 'BET_Surface_Area_m2_g',
        'Pore_Diameter_nm', 'Total_Pore_Volume_cm3_g', 'BET_over_Pore_Volume',
        'Pore_Area_Product', 'Specific_Loading_C0_over_dose', 'Mass_Transfer_Product'
    ]

    # Extra Trees Regressor
    et = ExtraTreesRegressor(n_estimators=300, max_depth=8, min_samples_leaf=2, random_state=42)
    et.fit(cat1[feature_cols], cat1['Kinetic_Capacity_qt_mg_g'])
    imp_et = pd.Series(et.feature_importances_, index=feature_cols)

    # Random Forest Regressor
    rf = RandomForestRegressor(n_estimators=300, max_depth=8, min_samples_leaf=2, random_state=42)
    rf.fit(cat1[feature_cols], cat1['Kinetic_Capacity_qt_mg_g'])
    imp_rf = pd.Series(rf.feature_importances_, index=feature_cols)

    records = []
    for f in feature_cols:
        records.append({
            'Feature_Name': f,
            'ExtraTrees_Importance_MDI': round(float(imp_et[f]), 5),
            'RandomForest_Importance_MDI': round(float(imp_rf[f]), 5),
            'Scientific_Description': 'Operational parameter' if 'Time' in f or 'dose' in f.lower() or 'conc' in f.lower() or 'ph' in f.lower() or 'temp' in f.lower() else 'Textural / Structural Carbon Property'
        })

    out_df = pd.DataFrame(records).sort_values(by='ExtraTrees_Importance_MDI', ascending=False)
    os.makedirs(os.path.dirname(os.path.abspath(output_csv)), exist_ok=True)
    out_df.to_csv(output_csv, index=False)
    print(f"Saved feature importances to: {output_csv}")
    print(out_df.to_string(index=False))
    return out_df


if __name__ == '__main__':
    args = parse_args()
    fp, rp, op = resolve_paths(args)
    compute_feature_importances(fp, rp, op)
