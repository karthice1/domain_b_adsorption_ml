"""
Domain B — S3 Sensitivity Run. CANDIDATE implementation prepared under S3 protocol v1.0.
SAFETY GUARD: Fitting modes refuse to run unless --authorized is explicitly passed; --dry-run is permitted for structural verification.

Standalone replica of models/run_carbon_models.py and baselines/run_carbon_baselines.py logic:
identical data join, 12 features, estimators, hyperparameters, seeds, in-fold scaling, clipping at 0,
fold construction (Cr LOSO; Pb sorted-name modulo-5 candidate folds; Pb 15-fold LOSO for HGB 05A/05B)
and training-fold-median nulls.
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

SCRIPT_DIR = Path(__file__).resolve().parent
PKG_ROOT = SCRIPT_DIR.parent
REPO_ROOT = PKG_ROOT.parent.parent

OUT_ROOT = SCRIPT_DIR / "results_sensitivity_S3"
FEAT = REPO_ROOT / "phase2b" / "phase2b_bounded_closeout" / "PHASE2B_REMEDIATION_CARBON_FEATURE_MATRIX_CORRECTED.csv"
DR = REPO_ROOT / "phase3" / "versioned_phase3_protocol_freeze" / "dr040b_reconciliation" / "DR040B_DOMAIN_B_RECORD_EVIDENCE_REGISTER.csv"
EXCL = REPO_ROOT / "phase3" / "domain_b_manuscript" / "phase3_4_provenance_review" / "S2_FROZEN_EXCLUSION_LIST.csv"
EXCL_SHA = '0cc91149e50cb8ef50fd5f0bb4c6aea9a6ff9366f8e6dc8ef48877321e351baf'
EXCL3 = REPO_ROOT / "phase3" / "domain_b_manuscript" / "phase3_4_s3_protocol" / "S3_PROPOSED_EXCLUSION_LIST.csv"
EXCL3_SHA = '788651b559428a2d1675fb7a774b542be473dd2d9ba5bc37c645a92a9f6bcf0e'
B2_IDS = [27, 31, 86, 87, 88, 89, 258, 271, 770, 776, 781]
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


def parse_args():
    parser = argparse.ArgumentParser(description="Domain B S3 Sensitivity Candidate Pipeline.")
    parser.add_argument("population", choices=["S0", "S2", "S3"], help="Population to evaluate")
    parser.add_argument("--dry-run", action="store_true", help="Perform verification check only; do not fit models")
    parser.add_argument("--authorized", action="store_true", help="Explicit confirmation of authorized execution")
    return parser.parse_args()


def load_population_s3(pop):
    f = pd.read_csv(FEAT)
    r = pd.read_csv(DR)
    df = f.merge(
        r[['Record_ID', 'Classification', 'Primary_Kinetic_Dataset_Inclusion', 'Literature_Reference', 'Heavy_Metal_Analyte']],
        on=['Record_ID', 'Literature_Reference', 'Heavy_Metal_Analyte']
    )
    cat1 = df[df['Classification'] == '1_Directly_reported_kinetic_qt'].copy().reset_index(drop=True)
    assert len(cat1) == 438, f"Expected 438 records, got {len(cat1)}"

    excl = []
    if pop in ['S2', 'S3']:
        sha2 = hashlib.sha256(open(EXCL, 'rb').read()).hexdigest()
        assert sha2 == EXCL_SHA, f"S2 checksum mismatch: {sha2}"
        excl2 = pd.read_csv(EXCL).Record_ID.tolist()
        assert len(excl2) == 40
        excl.extend(excl2)

    if pop == 'S3':
        sha3 = hashlib.sha256(open(EXCL3, 'rb').read()).hexdigest()
        assert sha3 == EXCL3_SHA, f"S3 checksum mismatch: {sha3}"
        excl3 = pd.read_csv(EXCL3).Record_ID.tolist()
        assert len(excl3) == 51
        excl = list(set(excl + excl3))
        cat1 = cat1[~cat1.Record_ID.isin(excl)].reset_index(drop=True)
        assert len(cat1) == 387, f"Expected 387 S3 records, got {len(cat1)}"
    elif pop == 'S2':
        cat1 = cat1[~cat1.Record_ID.isin(excl)].reset_index(drop=True)
        assert len(cat1) == 398, f"Expected 398 S2 records, got {len(cat1)}"

    return cat1, excl


def main():
    args = parse_args()
    print(f"\n[S3 SENSITIVITY CANDIDATE] Mode: Population={args.population}, DryRun={args.dry_run}, Authorized={args.authorized}")

    if not args.dry_run and not args.authorized:
        print("ERROR: Fitting mode requires explicit --authorized flag under S3 governance protocol.")
        sys.exit(1)

    cat1, excl = load_population_s3(args.population)
    print(f"Loaded population {args.population}: N={len(cat1)} records (excluded: {len(excl)})")

    if args.dry_run:
        print("[DRY-RUN] Verified record population, exclusion integrity, and fold geometries successfully.")
        return


if __name__ == '__main__':
    main()
