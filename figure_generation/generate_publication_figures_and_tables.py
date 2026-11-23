#!/usr/bin/env python3
"""
STAGE 1 — BOUNDED WP3 ARTIFACT GENERATION SCRIPT (VERSION 1.0.2)
Project: AI-Driven ML Framework for Heavy Metal Remediation (Domain B Carbon Adsorption)
Script: generate_wp3_artifacts.py
Release: V1.0.2 (Documentation Reconciliation, PDF Font Embedding & Timezone Correction)

MANDATORY CORRECTIONS & GOVERNANCE CONTROLS:
- Strict fail-closed verification of canonical source file hashes and row counts before execution.
- Deterministic Figure 4 jitter via fixed Seed: rng = np.random.default_rng(20261121).
- Corrected Figure 3 titles removing fold-validation descriptions (Corpus frequency only).
- Table 1 dynamically reads and verifies metrics from PHASE_3_2A_RMSE_RECONCILIATION.csv.
- Zero model training, refitting, retraining, or tuning.
- Zero new predictions or synthetic trajectory points.
- Strictly no Table 2 generation.
- Zero unapproved residual error bands on Figure 1.
- No outlier deletion or artificial smoothing on Figure 2.
- Generates SVG, PDF, TIFF (600 dpi), PNG (300 dpi) for Figures 1-4.
- Generates CSV, MD, PDF for Table 1.
"""

import os
import sys
import hashlib
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from PIL import Image
from datetime import datetime
from zoneinfo import ZoneInfo

# TrueType font embedding configuration (Type 42)
mpl.rcParams["pdf.fonttype"] = 42
mpl.rcParams["ps.fonttype"] = 42
mpl.rcParams["pdf.use14corefonts"] = False

# Monkey-patch Matplotlib PDF date formatting for explicit +05'30' timezone syntax
import matplotlib.backends.backend_pdf as bpdf
def _correct_datetime_to_pdf(d):
    r = d.strftime('D:%Y%m%d%H%M%S')
    z = d.utcoffset()
    if z is not None:
        total_seconds = int(z.total_seconds())
        sign = '+' if total_seconds >= 0 else '-'
        total_seconds = abs(total_seconds)
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        r += f"{sign}{hours:02d}'{minutes:02d}'"
    else:
        r += 'Z'
    return r
bpdf._datetime_to_pdf = _correct_datetime_to_pdf

# Ensure reproducibility and professional font styling
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
plt.rcParams['axes.edgecolor'] = '#333333'
plt.rcParams['axes.linewidth'] = 0.8
plt.rcParams['xtick.color'] = '#333333'
plt.rcParams['ytick.color'] = '#333333'
plt.rcParams['text.color'] = '#111111'
plt.rcParams['figure.autolayout'] = False

def compute_sha256(filepath):
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def get_paths_and_verify_sources(custom_repo_root=None, custom_output_dir=None, skip_hash=False):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if custom_repo_root:
        repo_root = os.path.abspath(custom_repo_root)
    else:
        # Check standard locations
        c1 = os.path.abspath(os.path.join(script_dir, "../../.."))
        c2 = os.path.abspath(os.path.join(script_dir, "../../../.."))
        if os.path.exists(os.path.join(c1, "phase3")):
            repo_root = c1
        elif os.path.exists(os.path.join(c2, "phase3")):
            repo_root = c2
        else:
            repo_root = "/Users/karthik/research_project"
    
    sources = {
        "cr_oof": {
            "path": os.path.join(repo_root, "phase3/model_development/domain_B_carbon/results/CARB_CR_CANDIDATE_OOF_PREDICTIONS.csv"),
            "expected_sha256": "b292a62cd90655e8520049c8d5bd8b09f136f1335f035ac21dfbf35c38cd748e",
            "expected_rows": 120,
            "expected_size": 17634
        },
        "pb_oof": {
            "path": os.path.join(repo_root, "phase3/model_development/domain_B_carbon/results/CARB_PB_CANDIDATE_OOF_PREDICTIONS.csv"),
            "expected_sha256": "1e44109b81740e5fdceaab27ec1276d5faa56d40923de3936051992bb2013388",
            "expected_rows": 318,
            "expected_size": 58405
        },
        "feature_matrix": {
            "path": os.path.join(repo_root, "phase2b/versioned_dr025_corrections/PHASE2B_REMEDIATION_CARBON_FEATURE_MATRIX_CORRECTED.csv"),
            "expected_sha256": "6c0531d14c2d2b4f302c9fd4fdfca8523f904e43e3df323c5c793f8340ef2da6",
            "expected_rows": 783,
            "expected_size": 405552
        },
        "rmse_recon": {
            "path": os.path.join(repo_root, "phase3/domain_b_manuscript/phase3_2a_corrections/PHASE_3_2A_RMSE_RECONCILIATION.csv"),
            "expected_sha256": "01d189b6130c7b4211922539f8a46bd46a39a9a9aeb7ec369344bb9b5eb825d5",
            "expected_rows": 18,
            "expected_size": 9527
        }
    }

    print("--- PRE-EXECUTION FAIL-CLOSED SOURCE VERIFICATION ---")
    for key, info in sources.items():
        p = info["path"]
        if not os.path.exists(p):
            print(f"FATAL ERROR: Missing source file: {p}")
            sys.exit(1)
        
        st = os.stat(p)
        actual_size = st.st_size
        actual_hash = compute_sha256(p)
        df_temp = pd.read_csv(p)
        actual_rows = len(df_temp)
        
        if actual_size != info["expected_size"]:
            print(f"FATAL ERROR: Size mismatch for {key}: expected {info['expected_size']}, got {actual_size}")
            sys.exit(1)
        if not skip_hash and actual_hash.lower() != info["expected_sha256"].lower():
            print(f"FATAL ERROR: SHA-256 mismatch for {key}: expected {info['expected_sha256']}, got {actual_hash}")
            sys.exit(1)
        if actual_rows != info["expected_rows"]:
            print(f"FATAL ERROR: Row count mismatch for {key}: expected {info['expected_rows']}, got {actual_rows}")
            sys.exit(1)
            
        print(f"  Verified {key}: {actual_rows} rows, {actual_size} bytes, SHA-256 {actual_hash[:16]}... PASS")

    out_d = custom_output_dir if custom_output_dir else script_dir
    os.makedirs(out_d, exist_ok=True)
    return {
        "output_dir": out_d,
        "repo_root": repo_root,
        "cr_oof": sources["cr_oof"]["path"],
        "pb_oof": sources["pb_oof"]["path"],
        "feature_matrix": sources["feature_matrix"]["path"],
        "rmse_recon": sources["rmse_recon"]["path"]
    }

def save_multiformat(fig, base_filename, output_dir, pdf_only=False):
    pdf_path = os.path.join(output_dir, f"{base_filename}.pdf")
    now_ist = datetime.now(ZoneInfo("Asia/Kolkata"))
    pdf_meta = {
        'Creator': f'Matplotlib v{matplotlib.__version__}',
        'Producer': f'Matplotlib pdf backend v{matplotlib.__version__}',
        'CreationDate': now_ist,
        'ModDate': now_ist,
    }
    # Always save publication PDF with TrueType fonts & aware metadata
    fig.savefig(pdf_path, format="pdf", bbox_inches="tight", metadata=pdf_meta)
    
    if not pdf_only:
        svg_path = os.path.join(output_dir, f"{base_filename}.svg")
        png_path = os.path.join(output_dir, f"{base_filename}.png")
        tiff_path = os.path.join(output_dir, f"{base_filename}.tiff")
        
        # Save Vector SVG
        fig.savefig(svg_path, format="svg", bbox_inches="tight")
        # Save 300 dpi PNG preview
        fig.savefig(png_path, format="png", dpi=300, bbox_inches="tight")
        # Save 600 dpi TIFF publication format via PIL lossless compression
        temp_png = os.path.join(output_dir, f"_temp_{base_filename}_600.png")
        fig.savefig(temp_png, format="png", dpi=600, bbox_inches="tight")
        im = Image.open(temp_png)
        im.save(tiff_path, format="TIFF", compression="tiff_lzw", dpi=(600, 600))
        im.close()
        if os.path.exists(temp_png):
            os.remove(temp_png)
            
        print(f"Saved: {base_filename} (SVG, PDF, PNG-300dpi, TIFF-600dpi)")
    else:
        print(f"Saved (PDF-only): {base_filename}.pdf")

# ==============================================================================
# 1. FIGURE 1: PARITY PLOTS (3 SEPARATE PANELS)
# ==============================================================================
def generate_figure1(paths, pdf_only=False):
    cr_df = pd.read_csv(paths["cr_oof"])
    pb_df = pd.read_csv(paths["pb_oof"])
    
    fig, axes = plt.subplots(1, 3, figsize=(16, 5.2), dpi=300)
    
    # Panel 1A: Cr Ridge
    y_true_cr = cr_df['Kinetic_Capacity_qt_mg_g']
    y_pred_cr = cr_df['Pred_Cr_CARB_MODEL_01_Ridge']
    
    ax = axes[0]
    ax.scatter(y_true_cr, y_pred_cr, color='#1f77b4', edgecolors='#0e3d61', alpha=0.75, s=36, label='Cr(VI) Evaluated Observations')
    lims_a = [0, max(max(y_true_cr), max(y_pred_cr)) * 1.05]
    ax.plot(lims_a, lims_a, color='#d62728', linestyle='--', linewidth=1.5, label='Identity Line ($y = x$)')
    ax.set_xlim(lims_a)
    ax.set_ylim(lims_a)
    ax.set_xlabel('Observed Uptake, $q_t$ (mg/g)', fontsize=11, fontweight='bold')
    ax.set_ylabel('Predicted Uptake, $\\hat{q}_t$ (mg/g)', fontsize=11, fontweight='bold')
    ax.set_title('(A) Chromium(VI) — Ridge Regression\n5-Fold Leave-One-Study-Out ($N = 120$)', fontsize=12, fontweight='bold', pad=10)
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.legend(loc='upper left', frameon=True, framealpha=0.9, fontsize=9)
    ax.text(0.95, 0.08, '$R^2 = 0.7758$\nRMSE = 9.118 mg/g\nMAE = 7.167 mg/g',
            transform=ax.transAxes, fontsize=10, ha='right', va='bottom',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor='#cccccc', alpha=0.9))

    # Panel 1B: Pb Extra Trees
    y_true_pb = pb_df['Kinetic_Capacity_qt_mg_g']
    y_pred_pb_et = pb_df['Pred_Pb_Grouped_CARB_MODEL_04_ExtraTrees']
    
    ax = axes[1]
    ax.scatter(y_true_pb, y_pred_pb_et, color='#2ca02c', edgecolors='#145214', alpha=0.75, s=36, label='Pb(II) Evaluated Observations')
    lims_b = [0, max(max(y_true_pb), max(y_pred_pb_et)) * 1.05]
    ax.plot(lims_b, lims_b, color='#d62728', linestyle='--', linewidth=1.5, label='Identity Line ($y = x$)')
    ax.set_xlim(lims_b)
    ax.set_ylim(lims_b)
    ax.set_xlabel('Observed Uptake, $q_t$ (mg/g)', fontsize=11, fontweight='bold')
    ax.set_ylabel('Predicted Uptake, $\\hat{q}_t$ (mg/g)', fontsize=11, fontweight='bold')
    ax.set_title('(B) Lead(II) — Extra Trees Regressor\n5-Fold Study-Grouped ($N = 318$)', fontsize=12, fontweight='bold', pad=10)
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.legend(loc='upper left', frameon=True, framealpha=0.9, fontsize=9)
    ax.text(0.95, 0.08, '$R^2 = 0.8586$\nRMSE = 8.075 mg/g\nMAE = 5.752 mg/g',
            transform=ax.transAxes, fontsize=10, ha='right', va='bottom',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor='#cccccc', alpha=0.9))

    # Panel 1C: Pb Monotonic HistGradientBoosting
    y_pred_pb_hgb = pb_df['Pred_Pb_LOSO15_CARB_MODEL_05B_HistGradientBoosting_Monotonic']
    
    ax = axes[2]
    ax.scatter(y_true_pb, y_pred_pb_hgb, color='#ff7f0e', edgecolors='#994800', alpha=0.75, s=36, label='Pb(II) Evaluated Observations')
    lims_c = [0, max(max(y_true_pb), max(y_pred_pb_hgb)) * 1.05]
    ax.plot(lims_c, lims_c, color='#d62728', linestyle='--', linewidth=1.5, label='Identity Line ($y = x$)')
    ax.set_xlim(lims_c)
    ax.set_ylim(lims_c)
    ax.set_xlabel('Observed Uptake, $q_t$ (mg/g)', fontsize=11, fontweight='bold')
    ax.set_ylabel('Predicted Uptake, $\\hat{q}_t$ (mg/g)', fontsize=11, fontweight='bold')
    ax.set_title('(C) Lead(II) — Monotonic HistGradientBoosting\n15-Fold Leave-One-Study-Out ($N = 318$)', fontsize=12, fontweight='bold', pad=10)
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.legend(loc='upper left', frameon=True, framealpha=0.9, fontsize=9)
    ax.text(0.95, 0.08, '$R^2 = 0.7799$\nRMSE = 10.075 mg/g\nMAE = 7.322 mg/g',
            transform=ax.transAxes, fontsize=10, ha='right', va='bottom',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor='#cccccc', alpha=0.9))

    plt.tight_layout()
    save_multiformat(fig, "FIGURE_1_PARITY_PLOTS", paths["output_dir"], pdf_only=pdf_only)
    plt.close(fig)

# ==============================================================================
# 2. FIGURE 2: RESIDUAL DISTRIBUTIONS (3 SEPARATE PANELS)
# ==============================================================================
def generate_figure2(paths, pdf_only=False):
    cr_df = pd.read_csv(paths["cr_oof"])
    pb_df = pd.read_csv(paths["pb_oof"])
    
    # Residual definition: e_i = predicted_i - observed_i
    res_cr = cr_df['Pred_Cr_CARB_MODEL_01_Ridge'] - cr_df['Kinetic_Capacity_qt_mg_g']
    res_pb_et = pb_df['Pred_Pb_Grouped_CARB_MODEL_04_ExtraTrees'] - pb_df['Kinetic_Capacity_qt_mg_g']
    res_pb_hgb = pb_df['Pred_Pb_LOSO15_CARB_MODEL_05B_HistGradientBoosting_Monotonic'] - pb_df['Kinetic_Capacity_qt_mg_g']
    
    fig, axes = plt.subplots(1, 3, figsize=(16, 5.0), dpi=300)
    
    # Panel 2A: Cr Ridge
    ax = axes[0]
    n_a, bins_a, patches_a = ax.hist(res_cr, bins=16, color='#1f77b4', edgecolor='#0e3d61', alpha=0.75, rwidth=0.9)
    ax.axvline(0, color='#d62728', linestyle='--', linewidth=1.5, label='Zero Error ($e = 0$)')
    ax.set_xlabel('Residual Error, $e_i = \\hat{q}_i - q_i$ (mg/g)', fontsize=11, fontweight='bold')
    ax.set_ylabel('Observation Count', fontsize=11, fontweight='bold')
    ax.set_title('(A) Residual Distribution — Cr(VI) Ridge\n5-Fold LOSO ($N = 120$)', fontsize=12, fontweight='bold', pad=10)
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.legend(loc='upper right', frameon=True, fontsize=9)
    ax.text(0.05, 0.78, f'Mean Bias: {res_cr.mean():+.2f} mg/g\nStd Dev:   {res_cr.std():.2f} mg/g\nRange: [{res_cr.min():.1f}, {res_cr.max():.1f}]',
            transform=ax.transAxes, fontsize=9.5, family='monospace', va='top',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor='#cccccc', alpha=0.9))

    # Panel 2B: Pb Extra Trees
    ax = axes[1]
    n_b, bins_b, patches_b = ax.hist(res_pb_et, bins=20, color='#2ca02c', edgecolor='#145214', alpha=0.75, rwidth=0.9)
    ax.axvline(0, color='#d62728', linestyle='--', linewidth=1.5, label='Zero Error ($e = 0$)')
    ax.set_xlabel('Residual Error, $e_i = \\hat{q}_i - q_i$ (mg/g)', fontsize=11, fontweight='bold')
    ax.set_ylabel('Observation Count', fontsize=11, fontweight='bold')
    ax.set_title('(B) Residual Distribution — Pb(II) Extra Trees\n5-Fold Study-Grouped ($N = 318$)', fontsize=12, fontweight='bold', pad=10)
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.legend(loc='upper right', frameon=True, fontsize=9)
    ax.text(0.05, 0.78, f'Mean Bias: {res_pb_et.mean():+.2f} mg/g\nStd Dev:   {res_pb_et.std():.2f} mg/g\nRange: [{res_pb_et.min():.1f}, {res_pb_et.max():.1f}]',
            transform=ax.transAxes, fontsize=9.5, family='monospace', va='top',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor='#cccccc', alpha=0.9))

    # Panel 2C: Pb Monotonic HistGradientBoosting
    ax = axes[2]
    n_c, bins_c, patches_c = ax.hist(res_pb_hgb, bins=20, color='#ff7f0e', edgecolor='#994800', alpha=0.75, rwidth=0.9)
    ax.axvline(0, color='#d62728', linestyle='--', linewidth=1.5, label='Zero Error ($e = 0$)')
    ax.set_xlabel('Residual Error, $e_i = \\hat{q}_i - q_i$ (mg/g)', fontsize=11, fontweight='bold')
    ax.set_ylabel('Observation Count', fontsize=11, fontweight='bold')
    ax.set_title('(C) Residual Distribution — Pb(II) Monotonic HGB\n15-Fold LOSO ($N = 318$)', fontsize=12, fontweight='bold', pad=10)
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.legend(loc='upper right', frameon=True, fontsize=9)
    ax.text(0.05, 0.78, f'Mean Bias: {res_pb_hgb.mean():+.2f} mg/g\nStd Dev:   {res_pb_hgb.std():.2f} mg/g\nRange: [{res_pb_hgb.min():.1f}, {res_pb_hgb.max():.1f}]',
            transform=ax.transAxes, fontsize=9.5, family='monospace', va='top',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor='#cccccc', alpha=0.9))

    plt.tight_layout()
    save_multiformat(fig, "FIGURE_2_RESIDUAL_DISTRIBUTIONS", paths["output_dir"], pdf_only=pdf_only)
    plt.close(fig)

# ==============================================================================
# 3. FIGURE 3: LITERATURE CORPUS TOPOLOGY (CORRECTED TITLES — NO FOLD LABELS)
# ==============================================================================
def generate_figure3(paths, pdf_only=False):
    cr_df = pd.read_csv(paths["cr_oof"])
    pb_df = pd.read_csv(paths["pb_oof"])
    
    cr_counts = cr_df['Literature_Reference'].value_counts(ascending=True)
    pb_counts = pb_df['Literature_Reference'].value_counts(ascending=True)
    
    fig, axes = plt.subplots(1, 2, figsize=(15, 6.8), dpi=300)
    
    # Panel 3A: Chromium(VI) Kinetic Corpus — 5 Studies, N = 120 Observations
    ax = axes[0]
    bars_a = ax.barh(cr_counts.index, cr_counts.values, color='#1f77b4', edgecolor='#0e3d61', alpha=0.8, height=0.6)
    ax.set_xlabel('Kinetic Observations ($N$)', fontsize=11, fontweight='bold')
    ax.set_title('(A) Chromium(VI) Kinetic Corpus — 5 Studies, N = 120 Observations', fontsize=12, fontweight='bold', pad=12)
    ax.grid(True, axis='x', linestyle=':', alpha=0.6)
    ax.set_xlim(0, max(cr_counts.values) * 1.15)
    for bar in bars_a:
        w = bar.get_width()
        ax.text(w + 1.2, bar.get_y() + bar.get_height()/2, f'{int(w)} ({w/120*100:.1f}%)',
                va='center', ha='left', fontsize=9.5, fontweight='bold', color='#1f77b4')

    # Panel 3B: Lead(II) Kinetic Corpus — 15 Studies, N = 318 Observations
    ax = axes[1]
    bars_b = ax.barh(pb_counts.index, pb_counts.values, color='#2ca02c', edgecolor='#145214', alpha=0.8, height=0.65)
    ax.set_xlabel('Kinetic Observations ($N$)', fontsize=11, fontweight='bold')
    ax.set_title('(B) Lead(II) Kinetic Corpus — 15 Studies, N = 318 Observations', fontsize=12, fontweight='bold', pad=12)
    ax.grid(True, axis='x', linestyle=':', alpha=0.6)
    ax.set_xlim(0, max(pb_counts.values) * 1.15)
    for bar in bars_b:
        w = bar.get_width()
        ax.text(w + 1.0, bar.get_y() + bar.get_height()/2, f'{int(w)} ({w/318*100:.1f}%)',
                va='center', ha='left', fontsize=9, fontweight='bold', color='#145214')

    plt.tight_layout()
    save_multiformat(fig, "FIGURE_3_CORPUS_TOPOLOGY", paths["output_dir"], pdf_only=pdf_only)
    plt.close(fig)

# ==============================================================================
# 4. FIGURE 4: OPERATIONAL RANGE COVERAGE (DETERMINISTIC JITTER — SEED: 20261121)
# ==============================================================================
def generate_figure4(paths, pdf_only=False):
    cr_df = pd.read_csv(paths["cr_oof"])
    pb_df = pd.read_csv(paths["pb_oof"])
    fm_df = pd.read_csv(paths["feature_matrix"])
    
    # 1. Verify key uniqueness in source populations
    if cr_df['Record_ID'].duplicated().sum() != 0:
        print("FATAL ERROR: Duplicate Record_ID in cr_oof")
        sys.exit(1)
    if pb_df['Record_ID'].duplicated().sum() != 0:
        print("FATAL ERROR: Duplicate Record_ID in pb_oof")
        sys.exit(1)
    if fm_df['Record_ID'].duplicated().sum() != 0:
        print("FATAL ERROR: Duplicate Record_ID in feature_matrix")
        sys.exit(1)

    # 2. 1-to-1 deterministic merges on Record_ID
    cr_joined = pd.merge(cr_df[['Record_ID']], fm_df, on='Record_ID', how='inner', validate='one_to_one')
    pb_joined = pd.merge(pb_df[['Record_ID']], fm_df, on='Record_ID', how='inner', validate='one_to_one')
    
    if len(cr_joined) != 120:
        print(f"FATAL ERROR: Cr join produced {len(cr_joined)} rows, expected 120")
        sys.exit(1)
    if len(pb_joined) != 318:
        print(f"FATAL ERROR: Pb join produced {len(pb_joined)} rows, expected 318")
        sys.exit(1)

    features = [
        ("Initial_Concentration_mg_L", "Initial Concentration, $C_0$ (mg/L)"),
        ("Adsorbent_Dose_g_L", "Adsorbent Dosage, $D$ (g/L)"),
        ("Solution_pH", "Solution pH"),
        ("Solution_Temperature_C", "Solution Temperature, $T$ (°C)"),
        ("BET_Surface_Area_m2_g", "BET Surface Area, $S_{\\mathrm{BET}}$ (m$^2$/g)")
    ]
    
    # Verify numeric and finite properties
    for col_name, _ in features:
        for name, jdf in [("Cr", cr_joined), ("Pb", pb_joined)]:
            s = pd.to_numeric(jdf[col_name], errors='coerce')
            if s.isnull().sum() > 0 or np.isinf(s).sum() > 0:
                print(f"FATAL ERROR: Non-numeric or non-finite values in {col_name} for {name}")
                sys.exit(1)

    # MANDATORY REPRODUCIBILITY SEED: Defined once, used consistently
    rng = np.random.default_rng(20261121)

    fig = plt.figure(figsize=(16, 10.5), dpi=300)
    gs = gridspec.GridSpec(5, 2, figure=fig, hspace=0.38, wspace=0.28)
    
    for row_idx, (col_name, label) in enumerate(features):
        # Left column: Cr (Population C - Panel A)
        ax_cr = fig.add_subplot(gs[row_idx, 0])
        vals_cr = cr_joined[col_name]
        bp_cr = ax_cr.boxplot(vals_cr, vert=False, patch_artist=True, widths=0.55,
                              boxprops=dict(facecolor='#1f77b4', alpha=0.5, edgecolor='#0e3d61', linewidth=1.2),
                              medianprops=dict(color='#d62728', linewidth=1.8),
                              whiskerprops=dict(color='#0e3d61', linewidth=1.2),
                              capprops=dict(color='#0e3d61', linewidth=1.2),
                              flierprops=dict(marker='o', markerfacecolor='#1f77b4', markersize=4, alpha=0.6))
        
        # Deterministic jitter using rng
        jitter_cr = rng.normal(1.0, 0.04, size=len(vals_cr))
        ax_cr.scatter(vals_cr, jitter_cr, color='#0e3d61', alpha=0.45, s=16, zorder=3)
        ax_cr.set_yticks([])
        ax_cr.set_xlabel(label, fontsize=10, fontweight='bold')
        ax_cr.grid(True, axis='x', linestyle=':', alpha=0.6)
        if row_idx == 0:
            ax_cr.set_title('(A) Chromium(VI) Kinetic Cohort ($N = 120$)\nOOF-Linked Validation Population', fontsize=12, fontweight='bold', pad=10)
        
        # Right column: Pb (Population C - Panel B)
        ax_pb = fig.add_subplot(gs[row_idx, 1])
        vals_pb = pb_joined[col_name]
        bp_pb = ax_pb.boxplot(vals_pb, vert=False, patch_artist=True, widths=0.55,
                              boxprops=dict(facecolor='#2ca02c', alpha=0.5, edgecolor='#145214', linewidth=1.2),
                              medianprops=dict(color='#d62728', linewidth=1.8),
                              whiskerprops=dict(color='#145214', linewidth=1.2),
                              capprops=dict(color='#145214', linewidth=1.2),
                              flierprops=dict(marker='o', markerfacecolor='#2ca02c', markersize=4, alpha=0.6))
        
        # Deterministic jitter using rng
        jitter_pb = rng.normal(1.0, 0.04, size=len(vals_pb))
        ax_pb.scatter(vals_pb, jitter_pb, color='#145214', alpha=0.4, s=14, zorder=3)
        ax_pb.set_yticks([])
        ax_pb.set_xlabel(label, fontsize=10, fontweight='bold')
        ax_pb.grid(True, axis='x', linestyle=':', alpha=0.6)
        if row_idx == 0:
            ax_pb.set_title('(B) Lead(II) Kinetic Cohort ($N = 318$)\nOOF-Linked Validation Population', fontsize=12, fontweight='bold', pad=10)

    save_multiformat(fig, "FIGURE_4_FEATURE_COVERAGE_POPULATION_C", paths["output_dir"], pdf_only=pdf_only)
    plt.close(fig)

# ==============================================================================
# 5. TABLE 1: FROZEN BENCHMARK SUMMARY (DYNAMICALLY READ & VERIFIED FROM SOURCE)
# ==============================================================================
def generate_table1(paths, pdf_only=False):
    rmse_df = pd.read_csv(paths["rmse_recon"])
    
    # Model specification and exact identifiers
    models_spec = [
        {
            "display_name": "Chromium Ridge",
            "model_identifier": "CARB_MODEL_01_Ridge",
            "validation_regime": "5-Fold Leave-One-Study-Out (LOSO)",
            "expected_mae": "7.167",
            "expected_rmse": "9.118",
            "expected_r2": "0.7758",
            "expected_n": 120
        },
        {
            "display_name": "Lead Extra Trees",
            "model_identifier": "CARB_MODEL_04_ExtraTrees_Grouped",
            "validation_regime": "5-Fold Study-Grouped",
            "expected_mae": "5.752",
            "expected_rmse": "8.075",
            "expected_r2": "0.8586",
            "expected_n": 318
        },
        {
            "display_name": "Lead Dummy Baseline",
            "model_identifier": "CARB_BASE_01_Pb_AlignedGrouped",
            "validation_regime": "5-Fold Study-Grouped",
            "expected_mae": "20.849",
            "expected_rmse": "26.154",
            "expected_r2": "-0.4832",
            "expected_n": 318
        },
        {
            "display_name": "Lead Monotonic HGB",
            "model_identifier": "CARB_MODEL_05B_HistGradientBoosting_Monotonic_LOSO15",
            "validation_regime": "15-Fold Leave-One-Study-Out (LOSO)",
            "expected_mae": "7.322",
            "expected_rmse": "10.075",
            "expected_r2": "0.7799",
            "expected_n": 318
        }
    ]
    
    table_data = []
    print("\n--- TABLE 1 LINEAGE & METRIC VERIFICATION ---")
    for spec in models_spec:
        sub = rmse_df[rmse_df['Model_Identifier'] == spec['model_identifier']]
        if len(sub) != 1:
            print(f"FATAL ERROR: Could not find unique row for {spec['model_identifier']} in reconciliation CSV")
            sys.exit(1)
            
        r = sub.iloc[0]
        df_idx = sub.index[0]
        n_obs = int(r['Observation_Count'])
        mae_val = f"{float(r['Pooled_MAE']):.3f}"
        rmse_val = f"{float(r['Pooled_RMSE']):.3f}"
        r2_val = f"{float(r['Pooled_R2_OOD']):.4f}"
        
        print(f"Model: {spec['display_name']} ({spec['model_identifier']})")
        print(f"  Source Index: {df_idx} (1-based row {df_idx+1})")
        print(f"  Observed: N={n_obs}, MAE={mae_val}, RMSE={rmse_val}, R2={r2_val}")
        print(f"  Expected: N={spec['expected_n']}, MAE={spec['expected_mae']}, RMSE={spec['expected_rmse']}, R2={spec['expected_r2']}")
        
        if n_obs != spec['expected_n'] or mae_val != spec['expected_mae'] or rmse_val != spec['expected_rmse'] or r2_val != spec['expected_r2']:
            print(f"FATAL ERROR: Metric mismatch for {spec['display_name']}!")
            sys.exit(1)
            
        table_data.append({
            "Model": spec["display_name"],
            "N": n_obs,
            "Validation_Regime": spec["validation_regime"],
            "MAE_mg_g": mae_val,
            "RMSE_mg_g": rmse_val,
            "R2": r2_val,
            "MedAE_mg_g": "UNAVAILABLE"
        })

    # 1. Save CSV
    csv_path = os.path.join(paths["output_dir"], "TABLE_1_FROZEN_MODEL_PERFORMANCE.csv")
    df = pd.DataFrame(table_data)
    if not pdf_only:
        df.to_csv(csv_path, index=False)
    
    # 2. Save Markdown
    md_path = os.path.join(paths["output_dir"], "TABLE_1_FROZEN_MODEL_PERFORMANCE.md")
    md_content = f"""# TABLE 1 — FROZEN MODEL PERFORMANCE SUMMARY
## Domain B Activated-Carbon Heavy-Metal Dynamic Adsorption Kinetic Benchmarks

| Model | Evaluated $N$ | Validation Geometry | MAE (mg/g) | RMSE (mg/g) | $R^2$ | MedAE |
| :--- | :---: | :--- | :---: | :---: | :---: | :---: |
| **Chromium Ridge** | 120 | 5-Fold Leave-One-Study-Out (LOSO) | 7.167 | 9.118 | 0.7758 | *UNAVAILABLE* |
| **Lead Extra Trees** | 318 | 5-Fold Study-Grouped | 5.752 | 8.075 | 0.8586 | *UNAVAILABLE* |
| **Lead Dummy Baseline** | 318 | 5-Fold Study-Grouped | 20.849 | 26.154 | -0.4832 | *UNAVAILABLE* |
| **Lead Monotonic HGB** | 318 | 15-Fold Leave-One-Study-Out (LOSO) | 7.322 | 10.075 | 0.7799 | *UNAVAILABLE* |

### Methodological and Governance Notes:
1. **Source Lineage:** All numerical values are read directly from and verified against historical benchmark records in `PHASE_3_2A_RMSE_RECONCILIATION.csv` (DataFrame index 1 for Cr Ridge, index 13 for Pb Extra Trees, index 8 for Pb Dummy Baseline, and index 17 for Pb Monotonic HGB).
2. **Validation Incomparability:** Models were evaluated under distinct validation geometries (5-fold study-grouped vs. 15-fold LOSO); metrics must not be interpreted as if generated from a single homogeneous cross-validation scheme.
3. **Median Absolute Error (MedAE):** Formally omitted and designated `UNAVAILABLE` because it was not evaluated in the historical Phase 2B/3.2A reconciliation baseline.
4. **Table 2 Status:** Study-level breakdown table remains excluded under `TABLE_2_STATUS = NOT_AUTHORIZED_PENDING_METHODOLOGY_SPECIFICATION`.
"""
    if not pdf_only:
        with open(md_path, "w") as f:
            f.write(md_content)

    # 3. Save Publication PDF using ReportLab with embedded DejaVuSans and explicit timezone
    pdf_path = os.path.join(paths["output_dir"], "TABLE_1_FROZEN_MODEL_PERFORMANCE.pdf")
    try:
        from reportlab import rl_config
        from reportlab.lib.pagesizes import letter, landscape
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib import colors
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        import reportlab.pdfbase.pdfdoc as pdfdoc

        # Register DejaVuSans from local matplotlib data directory
        font_dir = '/Users/karthik/miniconda3/lib/python3.13/site-packages/matplotlib/mpl-data/fonts/ttf'
        pdfmetrics.registerFont(TTFont('DejaVuSans', os.path.join(font_dir, 'DejaVuSans.ttf')))
        pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', os.path.join(font_dir, 'DejaVuSans-Bold.ttf')))
        pdfmetrics.registerFont(TTFont('DejaVuSans-Oblique', os.path.join(font_dir, 'DejaVuSans-Oblique.ttf')))
        pdfmetrics.registerFont(TTFont('DejaVuSans-BoldOblique', os.path.join(font_dir, 'DejaVuSans-BoldOblique.ttf')))
        pdfmetrics.registerFontFamily('DejaVuSans', normal='DejaVuSans', bold='DejaVuSans-Bold', italic='DejaVuSans-Oblique', boldItalic='DejaVuSans-BoldOblique')
        rl_config.canvas_basefontname = 'DejaVuSans'

        # Patch ReportLab PDFDate.format for exact +05'30' timezone syntax
        def _patched_pdfdate_format(self, doc):
            now_ist = datetime.now(ZoneInfo('Asia/Kolkata'))
            formatted = now_ist.strftime("D:%Y%m%d%H%M%S+05'30'")
            return pdfdoc.format(pdfdoc.PDFString(formatted), doc)
        pdfdoc.PDFDate.format = _patched_pdfdate_format

        doc = SimpleDocTemplate(pdf_path, pagesize=landscape(letter),
                                rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
        elements = []
        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            'TableTitle',
            fontName='DejaVuSans-Bold',
            fontSize=16,
            leading=20,
            textColor=colors.HexColor('#111111')
        )
        subtitle_style = ParagraphStyle(
            'TableSubTitle',
            fontName='DejaVuSans',
            fontSize=10,
            leading=14,
            textColor=colors.HexColor('#444444')
        )
        note_style = ParagraphStyle(
            'TableNotes',
            fontName='DejaVuSans',
            fontSize=8.5,
            leading=12,
            textColor=colors.HexColor('#333333')
        )

        elements.append(Paragraph("<b>Table 1. Frozen Benchmark Performance Summary of Selected Adsorption Models</b>", title_style))
        elements.append(Paragraph("Domain B: Activated-Carbon Dynamic Kinetic Adsorption (Cr(VI) and Pb(II))", subtitle_style))
        elements.append(Spacer(1, 14))

        raw_table = [
            ["Model Identifier", "Sample (N)", "Validation Strategy", "MAE (mg/g)", "RMSE (mg/g)", "R²", "MedAE"]
        ]
        for row in table_data:
            raw_table.append([
                row["Model"],
                str(row["N"]),
                row["Validation_Regime"],
                row["MAE_mg_g"],
                row["RMSE_mg_g"],
                row["R2"],
                row["MedAE_mg_g"]
            ])

        t = Table(raw_table, colWidths=[140, 75, 200, 80, 80, 70, 85])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'DejaVuSans-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9.5),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('TOPPADDING', (0, 0), (-1, 0), 8),
            ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('FONTNAME', (0, 1), (-1, -1), 'DejaVuSans'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#bdc3c7')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        elements.append(t)
        elements.append(Spacer(1, 14))

        notes_text = (
            "<b>Methodological & Governance Notes:</b><br/>"
            "1. <i>Values strictly read from and verified against authoritative Phase 3.2A reconciliation records (`PHASE_3_2A_RMSE_RECONCILIATION.csv`).</i><br/>"
            "2. <i>Validation designs differ across models (LOSO vs Study-Grouped); cross-model metrics reflect distinct out-of-fold regimes.</i><br/>"
            "3. <i>Median Absolute Error (MedAE) was not computed in historical reconciliation data and is marked UNAVAILABLE.</i><br/>"
            "4. <i>Table 2 (study-level performance breakdown) is strictly excluded pending methodology specification.</i>"
        )
        elements.append(Paragraph(notes_text, note_style))
        doc.build(elements)
        if pdf_only:
            print("Saved (PDF-only): TABLE_1_FROZEN_MODEL_PERFORMANCE.pdf")
        else:
            print("Saved: TABLE_1_FROZEN_MODEL_PERFORMANCE (CSV, MD, PDF)")
    except Exception as e:
        print(f"Warning: PDF generation via ReportLab encountered: {e}")

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Domain B Bounded Publication Artifact Generator (Figures 1-4 & Table 1)")
    parser.add_argument("--repo-root", default=None, help="Repository root directory")
    parser.add_argument("--output-dir", default=None, help="Target directory for artifacts")
    parser.add_argument("--pdf-only", action="store_true", help="Generate PDF format only")
    parser.add_argument("--skip-hash", action="store_true", help="Skip fail-closed SHA-256 validation")
    args = parser.parse_args()

    paths = get_paths_and_verify_sources(args.repo_root, args.output_dir, args.skip_hash)
    mode_str = "PDF-ONLY" if args.pdf_only else "FULL"
    print(f"\n=== EXECUTING BOUNDED WP3 ARTIFACT GENERATION (V1.0.2 - {mode_str} MODE) ===")
    print(f"Output Directory: {paths['output_dir']}")
    
    generate_figure1(paths, pdf_only=args.pdf_only)
    generate_figure2(paths, pdf_only=args.pdf_only)
    generate_figure3(paths, pdf_only=args.pdf_only)
    generate_figure4(paths, pdf_only=args.pdf_only)
    generate_table1(paths, pdf_only=args.pdf_only)
    
    print(f"=== ALL BOUNDED WP3 ARTIFACTS SUCCESSFULLY GENERATED (V1.0.2 - {mode_str} MODE) ===")

if __name__ == "__main__":
    main()
