# Domain B Adsorption ML: Command-Line Execution Guide

This manual documents the command-line interfaces (CLI), configuration options, input arguments, and expected behaviors for all executable modules in `domain_b_adsorption_ml`.

---

## 1. Candidate Modeling Pipeline (`src/modelling/run_carbon_models.py`)

Trains all candidate models (Ridge, ElasticNet, Random Forest, Extra Trees, unconstrained HGB, monotonic HGB) across Cr(VI) 5-fold LOSO-CV, Pb(II) 5-fold grouped CV, and Pb(II) 15-fold LOSO-CV.

### Syntax:
```bash
python3 src/modelling/run_carbon_models.py [OPTIONS]
```

### Options:
- `--features PATH`: Explicit path to `PHASE2B_REMEDIATION_CARBON_FEATURE_MATRIX_CORRECTED.csv`. If omitted, automatically resolves from repository root.
- `--register PATH`: Explicit path to `DR040B_DOMAIN_B_RECORD_EVIDENCE_REGISTER.csv`. If omitted, automatically resolves from repository root.
- `--output-dir PATH`: Target directory to save out-of-fold prediction CSVs and experiment logs (default: `./results`).
- `--seed INT`: Random seed for model initialization and tree splitting (default: `42`).

### Outputs Generated:
- `results/CARB_CR_CANDIDATE_OOF_PREDICTIONS.csv` ($N = 120$)
- `results/CARB_PB_CANDIDATE_OOF_PREDICTIONS.csv` ($N = 318$)
- `results/DOMAIN_B_EXPERIMENT_REGISTRY.csv`

---

## 2. Baseline Model Pipeline (`src/modelling/run_baselines.py`)

Computes in-training-fold study-median null baselines (CARB_BASE_01) to benchmark candidate model performance.

### Syntax:
```bash
python3 src/modelling/run_baselines.py [OPTIONS]
```

### Options:
- Same options as candidate modeling pipeline (`--features`, `--register`, `--output-dir`, `--seed`).

### Outputs Generated:
- `results/CARB_BASE_01_CR_LOSO_OOF_PREDICTIONS.csv` ($N = 120$)
- `results/CARB_BASE_01_PB_OOF_PREDICTIONS.csv` ($N = 318$)

---

## 3. Publication Artifact Generation (`figure_generation/generate_publication_figures_and_tables.py`)

Reproduces Figures 1-4 and Table 1 with pre-execution fail-closed cryptographic hash verification.

### Syntax:
```bash
python3 figure_generation/generate_publication_figures_and_tables.py [OPTIONS]
```

### Options:
- `--output-dir PATH`: Directory where generated figure and table files will be saved (default: `./figure_generation`).
- `--repo-root PATH`: Path to research repository root containing canonical inputs.
- `--pdf-only`: Flags the generator to produce only publication vector PDF outputs (skips SVG, TIFF, PNG for faster execution).
- `--skip-hash`: Bypasses pre-execution fail-closed SHA-256 checks (useful when testing synthetic mock data).

### Formats Exported:
- Figures 1, 2, 3, 4: `.svg` (vector), `.pdf` (vector, Type 42 TrueType embedded), `.tiff` (600 dpi), `.png` (300 dpi).
- Table 1: `.csv`, `.md`, `.pdf`.

---

## 4. Scientific Quality Control Suites

### 4.1 Physical Bounds and Non-Negativity QC
```bash
python3 quality_control/qc_scientific_integrity.py [--cr-pred PATH] [--pb-pred PATH]
```
Checks:
- Cr(VI) exact sample count ($N=120$) and study count ($K=5$).
- Pb(II) exact sample count ($N=318$) and study count ($K=15$).
- Non-negativity ($q_t \ge 0.0$) across all 18 prediction columns.
- Exit code 0 on PASS, 1 on FAIL.

### 4.2 Table 1 Semantic Parity QC
```bash
python3 quality_control/qc_table_semantics.py [--table1-csv PATH] [--rmse-recon PATH]
```
Checks:
- Validates all 18 table rows against canonical Phase 3.2A reconciliation records.
- Verifies exact decimal precision and sign consistency.
- Exit code 0 on PASS, 1 on FAIL.

---

## 5. Provenance Sensitivity S2 (`sensitivity_analysis/run_S2_sensitivity.py`)

Re-runs full evaluation pipeline under the provenance-restricted cohort ($N=398$, excluding 40 records).

### Syntax:
```bash
# Evaluate baseline population S0 (N=438)
python3 sensitivity_analysis/run_S2_sensitivity.py S0

# Evaluate provenance sensitivity population S2 (N=398)
python3 sensitivity_analysis/run_S2_sensitivity.py S2
```

### Outputs Generated:
- `results/S0/S0_METRICS_18_ROWS.csv` & `results/S0/S0_RUN_METADATA.json`
- `results/S2/S2_METRICS_18_ROWS.csv` & `results/S2/S2_RUN_METADATA.json`
