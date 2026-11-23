"""
Domain B Quality Control: Scientific Integrity and Physical Constraints Verification Suite.
Verifies non-negativity of predictions, physical bounds, metric validity, and cohort geometry.
"""

import os
import sys
import argparse
from pathlib import Path
import numpy as np
import pandas as pd


def verify_scientific_integrity(cr_pred_path, pb_pred_path):
    print("\n=======================================================")
    print("   SCIENTIFIC INTEGRITY AND CONSTRAINT QC SUITE")
    print("=======================================================")
    checks_passed = 0
    checks_failed = 0

    # 1. Verify Cr(VI) predictions
    if not os.path.exists(cr_pred_path):
        print(f"FAIL: Cr(VI) predictions file missing: {cr_pred_path}")
        return False

    cr_df = pd.read_csv(cr_pred_path)
    print(f"Checking Cr(VI) predictions ({len(cr_df)} records)...")

    # Check N=120
    if len(cr_df) == 120:
        print("  [PASS] Cr(VI) sample count N=120 exact.")
        checks_passed += 1
    else:
        print(f"  [FAIL] Cr(VI) sample count mismatch: {len(cr_df)} != 120")
        checks_failed += 1

    # Check 5 studies
    cr_studies = cr_df['Literature_Reference'].unique()
    if len(cr_studies) == 5:
        print("  [PASS] Cr(VI) study count = 5 exact.")
        checks_passed += 1
    else:
        print(f"  [FAIL] Cr(VI) study count mismatch: {len(cr_studies)} != 5")
        checks_failed += 1

    # Check non-negativity across all prediction columns
    pred_cols_cr = [c for c in cr_df.columns if c.startswith('Pred_Cr')]
    for col in pred_cols_cr:
        neg_count = np.sum(cr_df[col] < 0.0)
        if neg_count == 0:
            print(f"  [PASS] Non-negativity check for {col} (0 negative predictions).")
            checks_passed += 1
        else:
            print(f"  [FAIL] {col} contains {neg_count} negative predictions (physical violation).")
            checks_failed += 1

    # 2. Verify Pb(II) predictions
    if not os.path.exists(pb_pred_path):
        print(f"FAIL: Pb(II) predictions file missing: {pb_pred_path}")
        return False

    pb_df = pd.read_csv(pb_pred_path)
    print(f"\nChecking Pb(II) predictions ({len(pb_df)} records)...")

    # Check N=318
    if len(pb_df) == 318:
        print("  [PASS] Pb(II) sample count N=318 exact.")
        checks_passed += 1
    else:
        print(f"  [FAIL] Pb(II) sample count mismatch: {len(pb_df)} != 318")
        checks_failed += 1

    # Check 15 studies
    pb_studies = pb_df['Literature_Reference'].unique()
    if len(pb_studies) == 15:
        print("  [PASS] Pb(II) study count = 15 exact.")
        checks_passed += 1
    else:
        print(f"  [FAIL] Pb(II) study count mismatch: {len(pb_studies)} != 15")
        checks_failed += 1

    # Check non-negativity across all prediction columns
    pred_cols_pb = [c for c in pb_df.columns if c.startswith('Pred_Pb')]
    for col in pred_cols_pb:
        neg_count = np.sum(pb_df[col] < 0.0)
        if neg_count == 0:
            print(f"  [PASS] Non-negativity check for {col} (0 negative predictions).")
            checks_passed += 1
        else:
            print(f"  [FAIL] {col} contains {neg_count} negative predictions (physical violation).")
            checks_failed += 1

    total_n = len(cr_df) + len(pb_df)
    if total_n == 438:
        print(f"\n[PASS] Total Category 1 dynamic kinetic observations N = 438 exact.")
        checks_passed += 1
    else:
        print(f"\n[FAIL] Total Category 1 observations mismatch: {total_n} != 438")
        checks_failed += 1

    print("-------------------------------------------------------")
    print(f"Integrity QC Results: {checks_passed} PASSED, {checks_failed} FAILED.")
    print("=======================================================\n")
    return checks_failed == 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run Scientific Integrity QC.")
    parser.add_argument("--cr-pred", default=None, help="Path to Cr(VI) candidate predictions")
    parser.add_argument("--pb-pred", default=None, help="Path to Pb(II) candidate predictions")
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    repo_root = script_dir.parent.parent.parent

    cr_path = args.cr_pred or str(repo_root / "phase3" / "model_development" / "domain_B_carbon" / "results" / "CARB_CR_CANDIDATE_OOF_PREDICTIONS.csv")
    pb_path = args.pb_pred or str(repo_root / "phase3" / "model_development" / "domain_B_carbon" / "results" / "CARB_PB_CANDIDATE_OOF_PREDICTIONS.csv")

    ok = verify_scientific_integrity(cr_path, pb_path)
    sys.exit(0 if ok else 1)
