# Domain B Adsorption ML: Reproduction Instructions

This document describes how to run the research software that accompanies the manuscript:

**"Study-grouped and leave-one-study-out evaluation of machine-learning models for time-resolved Cr(VI) and Pb(II) uptake on activated carbons using pre-assay inputs."**

> **Before you start: what this package can and cannot reproduce**
> - The literature-derived feature matrix, the record evidence register, the S2/S3 exclusion lists, the stored out-of-fold predictions and fitted models are **not included**. Levels A–E below need these files. Without them, only the unit tests and the synthetic files in `sample_data/` can be used, which exercise the code paths but do not reproduce the reported results.
> - The packaged training code is a refactored version of the research scripts and **has not been re-executed** to regenerate the reported predictions. The reported predictions were produced by the original research scripts.
> - Level A refits all models.
> - See `REPRODUCIBILITY_MATRIX.csv` for the execution status of each level.
> - **Portability.** The code contains machine-specific paths (README, Section 6): an absolute repository-root fallback and an absolute font directory in the figure generator, and layout-dependent input paths in the data-dependent tests and the S3 script. Outside the author's repository, always pass `--repo-root` to the generator, and place the package inside a directory tree laid out like the author's repository to run the data-dependent tests or S3. **The complete test suite does not pass on an independent machine.**

---

## 1. Environment

### System
- Operating system: macOS or Linux.
- Python 3.10–3.13. The S2/S3 runs and their reproduction controls used Python 3.13.5 with scikit-learn 1.9.1, NumPy 2.4.6 and pandas 2.3.3. The versions of the original S0 run were not recorded.

### Conda (recommended)
```bash
conda env create -f environment.yml
conda activate domain_b_adsorption_ml
```

### virtualenv
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 2. Unit tests

```bash
python3 -m unittest discover tests -v
```

| Test file | What it checks | Needs non-public inputs |
|---|---|---|
| `test_environment.py` | Python version; required packages importable | No |
| `test_metrics.py` | Metric functions on known cases | No |
| `test_cohort_and_integrity.py` | Record and study counts; no negative predictions in the stored OOF files | Yes (tests skip if absent) |
| `test_artifact_generation.py` | The figure/table generator runs and writes the five PDFs | Yes (stored inputs and the original repository path). In a clean copy without them this test **fails**; it is not skipped |

Measured results (v1.0.1; code identical to v1.0.0):

| Where the tests were run | Passed | Skipped | Failed |
|---|---:|---:|---:|
| Author's repository (all non-public inputs present) | 10 | 0 | 0 |
| Copy outside the repository layout, on the author's machine | 6 | 4 | 0 |
| Clean copy, access to the author's repository blocked | 5 | 4 | 1 |

Skipped tests are not passed tests. Passing tests shows only that the tested checks pass.

---

## 3. Levels

### Level A — Model fitting and null baselines (refits models)
```bash
python3 src/modelling/run_carbon_models.py --features PATH --register PATH --output-dir results
python3 src/modelling/run_baselines.py --features PATH --register PATH --output-dir results
```
Expected outputs:
- `results/CARB_CR_CANDIDATE_OOF_PREDICTIONS.csv` (120 rows)
- `results/CARB_PB_CANDIDATE_OOF_PREDICTIONS.csv` (318 rows)
- `results/CARB_BASE_01_CR_LOSO_OOF_PREDICTIONS.csv` (120 rows)
- `results/CARB_BASE_01_PB_OOF_PREDICTIONS.csv` (318 rows)
- `results/DOMAIN_B_EXPERIMENT_REGISTRY.csv`

Agreement with the stored predictions has been shown for the original research scripts: the S0/S2 reproduction controls agreed within $5\times10^{-14}$ mg/g. It has not been shown for this packaged code.

### Level B — Integrity checks on stored predictions
```bash
python3 quality_control/qc_scientific_integrity.py --cr-pred PATH --pb-pred PATH
```
Checks record and study counts (120/5, 318/15, total 438) and that no prediction is negative.

### Level C — Table 1 check
```bash
python3 quality_control/qc_table_semantics.py --table1-csv PATH --rmse-recon PATH
```
Checks the four rows of Table 1 against the reconciliation file:
- N exact;
- MAE and RMSE within 0.005 mg/g;
- R² within 0.0005.

Headline values in the manuscript:
- Cr(VI), Ridge, 5-fold LOSO: MAE 7.167 mg/g, RMSE 9.118 mg/g, $R^2_{\mathrm{OOD}}$ 0.7758; training-median null MAE 30.885 mg/g.
- Pb(II), extra trees, 5-fold study-grouped: MAE 5.752 mg/g, RMSE 8.075 mg/g, $R^2_{\mathrm{OOD}}$ 0.8586; null MAE 20.849 mg/g.
- Pb(II), monotonic HGB, 15-fold LOSO: MAE 7.322 mg/g, RMSE 10.075 mg/g, $R^2_{\mathrm{OOD}}$ 0.7799; null MAE 22.585 mg/g.

### Level D — Figures 1–4 and Table 1
```bash
python3 figure_generation/generate_publication_figures_and_tables.py --repo-root PATH
python3 figure_generation/generate_publication_figures_and_tables.py --repo-root PATH --pdf-only
```
Outputs:
- `FIGURE_1_PARITY_PLOTS`
- `FIGURE_2_RESIDUAL_DISTRIBUTIONS`
- `FIGURE_3_CORPUS_TOPOLOGY`
- `FIGURE_4_FEATURE_COVERAGE_POPULATION_C`
- `TABLE_1_FROZEN_MODEL_PERFORMANCE`

The generator checks the SHA-256 hashes of its inputs before plotting. Outside the author's repository, `--repo-root` is required (otherwise it falls back to `/Users/karthik/research_project` and stops). The Table 1 PDF needs `reportlab` and the font directory hard-coded at line 568; where that directory does not exist, the Table 1 PDF is not written (warning only).

### Level E — Input derivation and sensitivity analyses
```bash
# Derive the 12 inputs from the harmonised table (not included)
python3 src/feature_engineering/derive_carbon_features.py

# S2 provenance sensitivity analysis (S0 control and S2, N = 398)
python3 sensitivity_analysis/run_S2_sensitivity.py S0
python3 sensitivity_analysis/run_S2_sensitivity.py S2

# S3 source-classification sensitivity analysis: structural dry run only
# (no path option: the package must sit inside a repository-like layout; see README Section 6)
python3 sensitivity_analysis/run_S3_sensitivity_candidate.py S3 --dry-run

# Impurity-based feature importances (diagnostic only)
python3 src/modelling/feature_importance.py
```
