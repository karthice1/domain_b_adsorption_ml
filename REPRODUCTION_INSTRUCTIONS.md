# Domain B Adsorption ML Framework: Reproduction Instructions

This document provides step-by-step instructions for executing the research software and reproducing all computational claims, tables, figures, and sensitivity analyses reported in the manuscript:

**"Study-grouped and leave-one-study-out evaluation of machine-learning models for time-resolved Cr(VI) and Pb(II) uptake on activated carbons using pre-assay inputs."**

---

## 1. Prerequisites and Environment Setup

### System Requirements
- Operating System: macOS (arm64 / x86_64) or Linux (x86_64)
- Python Version: Python >= 3.10, < 3.14 (Validated on Python 3.13.5)
- RAM: Minimum 8 GB recommended (for parallel tree fitting)
- Disk Space: ~500 MB for repository and generated publication figures

### Conda Environment Setup (Recommended)
```bash
# 1. Clone or navigate to the software package directory
cd software_publication/domain_b_adsorption_ml

# 2. Create and activate conda environment
conda env create -f environment.yml
conda activate domain_b_adsorption_ml
```

### Standard Virtualenv Setup (Alternative)
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 2. Running Automated Unit and Verification Tests

Run the comprehensive test suite to verify environment dependencies, metric implementations, non-negativity constraints, and artifact generation pipelines:

```bash
python3 -m unittest discover tests -v
```

Expected output:
- `test_environment.py`: All standard libraries (NumPy, Pandas, Scikit-learn, Matplotlib, SciPy, Pillow) importable and version compliant.
- `test_metrics.py`: Regression metrics (MAE, RMSE, R2_OOD, MedAE) match analytical solutions.
- `test_cohort_and_integrity.py`: Verifies Cr(VI) N=120 (5 studies), Pb(II) N=318 (15 studies), Total N=438, and non-negativity ($q_t \ge 0$).
- `test_artifact_generation.py`: Verifies clean end-to-end figure and table rendering.

---

## 3. Level-by-Level Reproduction Workflows

### Level A: Full Model Training and Baseline Pipelines
Train all candidate machine-learning models (Ridge, ElasticNet, RandomForest, ExtraTrees, unconstrained HistGradientBoosting, monotonic HistGradientBoosting) and study-median baselines:

```bash
# Run candidate continuous regression models
python3 src/modelling/run_carbon_models.py

# Run in-training-study null median baselines (CARB_BASE_01)
python3 src/modelling/run_baselines.py
```
*Expected Outputs:*
- `results/CARB_CR_CANDIDATE_OOF_PREDICTIONS.csv` (120 rows)
- `results/CARB_PB_CANDIDATE_OOF_PREDICTIONS.csv` (318 rows)
- `results/CARB_BASE_01_CR_LOSO_OOF_PREDICTIONS.csv` (120 rows)
- `results/CARB_BASE_01_PB_OOF_PREDICTIONS.csv` (318 rows)
- `results/DOMAIN_B_EXPERIMENT_REGISTRY.csv`

---

### Level B: Scientific Integrity and Physical Constraint Validation
Verify that all out-of-fold predictions satisfy physical boundaries ($q_t \ge 0$) and exact cohort dimensions:

```bash
python3 quality_control/qc_scientific_integrity.py
```
*Expected Output:*
- Cr(VI) sample count = 120 (5 studies) PASS
- Pb(II) sample count = 318 (15 studies) PASS
- Zero negative predictions across all model columns PASS

---

### Level C: Published Table 1 Reproduction
Verify that out-of-fold performance metrics exactly match Table 1 of the manuscript across all 18 canonical rows:

```bash
python3 quality_control/qc_table_semantics.py
```
*Key Benchmarks Verified:*
- Cr(VI) Top Model: Ridge Regressor (MAE 7.167 mg/g, RMSE 9.118 mg/g, $R^2_{\text{OOD}} = 0.7758$ vs Null MAE 30.885 mg/g)
- Pb(II) Primary 5-Fold Grouped Top Model: Extra Trees (MAE 5.752 mg/g, RMSE 8.075 mg/g, $R^2_{\text{OOD}} = 0.8586$ vs Null MAE 20.849 mg/g)
- Pb(II) Sensitivity 15-Fold LOSO Top Model: Monotonic HGB (MAE 7.322 mg/g, RMSE 10.075 mg/g, $R^2_{\text{OOD}} = 0.7799$ vs Null MAE 22.585 mg/g)

---

### Level D: Publication Figures 1-4 Generation
Regenerate publication-ready figures in 4 formats (SVG, PDF with TrueType Type 42 fonts, TIFF 600 dpi, PNG 300 dpi) and Table 1 (CSV, Markdown, PDF):

```bash
# Full multi-format generation (Figures 1-4 and Table 1)
python3 figure_generation/generate_publication_figures_and_tables.py

# Optional: Fast PDF-only generation
python3 figure_generation/generate_publication_figures_and_tables.py --pdf-only
```
*Artifacts Generated:*
- `FIGURE_1_PARITY_PLOTS` (Observed vs Predicted $q_t$ with 1:1 identity line)
- `FIGURE_2_RESIDUAL_DISTRIBUTIONS` (Residual histograms and contact-time trends)
- `FIGURE_3_CORPUS_TOPOLOGY` (Observation frequency per published literature study)
- `FIGURE_4_FEATURE_COVERAGE_POPULATION_C` (Textural and operational feature space coverage)
- `TABLE_1_FROZEN_MODEL_PERFORMANCE` (Complete 18-row model performance metrics)

---

### Level E: Feature Extraction and Sensitivity Analyses

#### 1. Derive 12 Carbon Physical/Chemical Features
```bash
python3 src/feature_engineering/derive_carbon_features.py
```

#### 2. S2 Provenance Sensitivity (N=398 vs S0 N=438)
```bash
# Evaluate baseline population S0 (N=438)
python3 sensitivity_analysis/run_S2_sensitivity.py S0

# Evaluate provenance-restricted population S2 (N=398)
python3 sensitivity_analysis/run_S2_sensitivity.py S2
```

#### 3. S3 Source Classification Sensitivity (N=387 Candidate Dry-Run)
```bash
# Execute pre-execution dry-run check (membership and fold validation)
python3 sensitivity_analysis/run_S3_sensitivity_candidate.py S3 --dry-run
```

#### 4. Tree-Based Feature Importances
```bash
python3 src/modelling/feature_importance.py
```
