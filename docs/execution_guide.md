# Domain B Adsorption ML: Command-Line Execution Guide

This guide documents the command-line options and expected behaviour of the executable modules in `domain_b_adsorption_ml`.

> **Prerequisite.** Except for the unit tests, every module below needs the literature-derived feature matrix, the record evidence register or the stored out-of-fold predictions. None of these is included in this package (see README, Section 6). Running the training pipelines refits the models.

---

## 1. Candidate modelling pipeline (`src/modelling/run_carbon_models.py`)

Fits the six candidate models (Ridge, ElasticNet, random forest, extra trees, unconstrained HGB, monotonic HGB) under the three designs:
- Cr(VI) 5-fold LOSO;
- Pb(II) 5-fold study-grouped;
- Pb(II) 15-fold LOSO (HGB-U and HGB-M only).

### Syntax
```bash
python3 src/modelling/run_carbon_models.py [OPTIONS]
```

### Options
- `--features PATH`: path to `PHASE2B_REMEDIATION_CARBON_FEATURE_MATRIX_CORRECTED.csv`. If omitted, it is resolved from the repository root.
- `--register PATH`: path to `DR040B_DOMAIN_B_RECORD_EVIDENCE_REGISTER.csv`. If omitted, it is resolved from the repository root.
- `--output-dir PATH`: directory for out-of-fold prediction CSVs and the experiment registry (default: `./results`).
- `--seed INT`: random seed (default: `42`).

### Outputs
- `results/CARB_CR_CANDIDATE_OOF_PREDICTIONS.csv` ($N = 120$)
- `results/CARB_PB_CANDIDATE_OOF_PREDICTIONS.csv` ($N = 318$)
- `results/DOMAIN_B_EXPERIMENT_REGISTRY.csv`

This packaged pipeline is a refactored version of the research script. It has not been re-executed to regenerate the reported predictions.

---

## 2. Baseline pipeline (`src/modelling/run_baselines.py`)

Computes the training-median null baselines (CARB_BASE_01). In every fold, each test record is predicted with the median $q_t$ of that fold's training records.

### Syntax
```bash
python3 src/modelling/run_baselines.py [OPTIONS]
```

### Options
Same as the candidate modelling pipeline (`--features`, `--register`, `--output-dir`, `--seed`).

### Outputs
- `results/CARB_BASE_01_CR_LOSO_OOF_PREDICTIONS.csv` ($N = 120$)
- `results/CARB_BASE_01_PB_OOF_PREDICTIONS.csv` ($N = 318$)

---

## 3. Figure and table generation (`figure_generation/generate_publication_figures_and_tables.py`)

Generates Figures 1–4 and Table 1 from the stored out-of-fold predictions, the feature matrix and the reconciliation file.

Before plotting, it checks the SHA-256 hash and row count of each input. It stops with an error if an input is missing or does not match.

### Syntax
```bash
python3 figure_generation/generate_publication_figures_and_tables.py [OPTIONS]
```

### Options
- `--output-dir PATH`: output directory (default: `./figure_generation`).
- `--repo-root PATH`: research repository root that contains the stored inputs.
- `--pdf-only`: produce only the vector PDF outputs.
- `--skip-hash`: skip the SHA-256 checks (for testing with synthetic data only).

### Formats
- Figures 1–4: `.svg`, `.pdf` (Type 42 TrueType fonts), `.tiff` (600 dpi), `.png` (300 dpi).
- Table 1: `.csv`, `.md`, `.pdf`.

---

## 4. Quality-control scripts

Both scripts are read-only. When the input files are not found, they print a warning and do not perform the check. Always pass explicit paths, and confirm in the output that each check was actually run.

### 4.1 Record counts and non-negativity (`quality_control/qc_scientific_integrity.py`)
```bash
python3 quality_control/qc_scientific_integrity.py --cr-pred PATH --pb-pred PATH
```
Checks:
- Cr(VI) record count (120) and study count (5).
- Pb(II) record count (318) and study count (15).
- No negative values in any `Pred_Cr*` or `Pred_Pb*` prediction column.
- Total of 438 records.
- Exit code 0 if all checks pass, 1 otherwise.

### 4.2 Table 1 check (`quality_control/qc_table_semantics.py`)
```bash
python3 quality_control/qc_table_semantics.py --table1-csv PATH --rmse-recon PATH
```
For the 4-row Table 1, checks each row against `PHASE_3_2A_RMSE_RECONCILIATION.csv`:
- the same N;
- MAE and RMSE within 0.005 mg/g;
- R² within 0.0005.

For an 18-row table, it compares MAE only, within 0.01 mg/g.

---

## 5. Provenance sensitivity analysis S2 (`sensitivity_analysis/run_S2_sensitivity.py`)

Re-runs the evaluation on the provenance-restricted population ($N = 398$; 40 records excluded) or on S0 ($N = 438$) as a control.

### Syntax
```bash
python3 sensitivity_analysis/run_S2_sensitivity.py S0 [--features PATH] [--register PATH] [--exclusion PATH] [--output-dir PATH]
python3 sensitivity_analysis/run_S2_sensitivity.py S2 [--features PATH] [--register PATH] [--exclusion PATH] [--output-dir PATH]
```

### Outputs
- `results/S0/S0_METRICS_18_ROWS.csv` and `results/S0/S0_RUN_METADATA.json`
- `results/S2/S2_METRICS_18_ROWS.csv` and `results/S2/S2_RUN_METADATA.json`

---

## 6. Source-classification sensitivity analysis S3 (`sensitivity_analysis/run_S3_sensitivity_candidate.py`)

```bash
python3 sensitivity_analysis/run_S3_sensitivity_candidate.py S3 --dry-run
```

The `--dry-run` option checks membership and fold assignment without fitting models. A full run additionally requires the `--authorized` flag and the S3 exclusion list, which is not included in this package.
