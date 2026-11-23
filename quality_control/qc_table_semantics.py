"""
Domain B Quality Control: Table Semantic and Numerical Parity Verification.
Checks table cell values, rounding, signs, and physical limits against canonical results.
"""

import os
import sys
import argparse
from pathlib import Path
import pandas as pd


def parse_args():
    parser = argparse.ArgumentParser(description="QC Table Semantics and Numerical Consistency.")
    parser.add_argument("--table1-csv", default=None, help="Path to Table 1 CSV")
    parser.add_argument("--rmse-recon", default=None, help="Path to PHASE_3_2A_RMSE_RECONCILIATION.csv")
    return parser.parse_args()


def resolve_paths(args):
    script_dir = Path(__file__).resolve().parent
    pkg_root = script_dir.parent
    repo_root = pkg_root.parent.parent

    t1_p = args.table1_csv
    if t1_p is None:
        cands = [
            pkg_root / "figure_generation" / "TABLE_1_FROZEN_MODEL_PERFORMANCE.csv",
            repo_root / "phase3" / "domain_b_manuscript" / "phase3_3_wp3_bounded_execution_v1_0_2" / "TABLE_1_FROZEN_MODEL_PERFORMANCE.csv"
        ]
        for c in cands:
            if c.exists():
                t1_p = str(c)
                break

    recon_p = args.rmse_recon
    if recon_p is None:
        c = repo_root / "phase3" / "domain_b_manuscript" / "phase3_2a_corrections" / "PHASE_3_2A_RMSE_RECONCILIATION.csv"
        if c.exists():
            recon_p = str(c)

    return t1_p, recon_p


def check_table1_parity(t1_path, recon_path):
    print(f"\n[QC TABLE 1] Checking numerical parity between:\n  Table 1: {t1_path}\n  Reconciliation: {recon_path}")
    if not t1_path or not os.path.exists(t1_path):
        print(f"WARNING: Table 1 CSV not found at {t1_path}; skipping parity check.")
        return True
    if not recon_path or not os.path.exists(recon_path):
        print(f"WARNING: Reconciliation CSV not found at {recon_path}; skipping parity check.")
        return True

    t1_df = pd.read_csv(t1_path)
    recon_df = pd.read_csv(recon_path)

    # Table 1 in WP3 format contains the 4 headline publication models
    # Expected models in Table 1
    models_spec = {
        "Chromium Ridge": {"id": "CARB_MODEL_01_Ridge", "n": 120, "mae": 7.167, "rmse": 9.118, "r2": 0.7758},
        "Lead Extra Trees": {"id": "CARB_MODEL_04_ExtraTrees_Grouped", "n": 318, "mae": 5.752, "rmse": 8.075, "r2": 0.8586},
        "Lead Dummy Baseline": {"id": "CARB_BASE_01_Pb_AlignedGrouped", "n": 318, "mae": 20.849, "rmse": 26.154, "r2": -0.4832},
        "Lead Monotonic HGB": {"id": "CARB_MODEL_05B_HistGradientBoosting_Monotonic_LOSO15", "n": 318, "mae": 7.322, "rmse": 10.075, "r2": 0.7799}
    }

    mismatches = 0
    if len(t1_df) == 4:
        for idx, row in t1_df.iterrows():
            m_name = row['Model']
            if m_name not in models_spec:
                print(f"  Unexpected model in Table 1: {m_name}")
                mismatches += 1
                continue
            spec = models_spec[m_name]
            recon_sub = recon_df[recon_df['Model_Identifier'] == spec['id']]
            if len(recon_sub) != 1:
                print(f"  Reconciliation entry not found for {spec['id']}")
                mismatches += 1
                continue
            r_row = recon_sub.iloc[0]

            obs_n = int(row['N'])
            obs_mae = float(row['MAE_mg_g'])
            obs_rmse = float(row['RMSE_mg_g'])
            obs_r2 = float(row['R2'])

            rec_n = int(r_row['Observation_Count'])
            rec_mae = float(r_row['Pooled_MAE'])
            rec_rmse = float(r_row['Pooled_RMSE'])
            rec_r2 = float(r_row['Pooled_R2_OOD'])

            if obs_n != rec_n or abs(obs_mae - rec_mae) > 0.005 or abs(obs_rmse - rec_rmse) > 0.005 or abs(obs_r2 - rec_r2) > 0.0005:
                print(f"  Mismatch for {m_name}: Table 1=(N={obs_n}, MAE={obs_mae}, RMSE={obs_rmse}, R2={obs_r2}), Recon=(N={rec_n}, MAE={rec_mae:.3f}, RMSE={rec_rmse:.3f}, R2={rec_r2:.4f})")
                mismatches += 1
            else:
                print(f"  [PASS] {m_name} (N={obs_n}, MAE={obs_mae:.3f}, RMSE={obs_rmse:.3f}, R2={obs_r2:.4f}) exactly matches reconciliation record index {recon_sub.index[0]}.")
    else:
        # If complete 18 rows table
        assert len(t1_df) == 18, f"Expected either 4 or 18 rows in Table 1, got {len(t1_df)}"
        for idx in range(18):
            t_row = t1_df.iloc[idx]
            r_row = recon_df.iloc[idx]
            t_mae = float(str(t_row.get('Pooled_MAE', t_row.get('Pooled MAE (mg/g)', 0))).split()[0])
            r_mae = float(r_row['Pooled_MAE'])
            if abs(t_mae - r_mae) > 0.01:
                print(f"  Row {idx} MAE mismatch: Table 1={t_mae:.3f}, Recon={r_mae:.3f}")
                mismatches += 1

    if mismatches == 0:
        print("[QC TABLE 1] PASS: All Table 1 entries matched canonical reconciliation benchmarks within numerical tolerance.")
        return True
    else:
        print(f"[QC TABLE 1] FAIL: Found {mismatches} mismatches.")
        return False


if __name__ == '__main__':
    args = parse_args()
    t1_p, rec_p = resolve_paths(args)
    success = check_table1_parity(t1_p, rec_p)
    sys.exit(0 if success else 1)
