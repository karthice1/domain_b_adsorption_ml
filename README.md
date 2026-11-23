# Domain B Adsorption ML: Machine Learning for Heavy-Metal Kinetic Adsorption on Activated Carbons

[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue.svg)](https://www.python.org/)
[![License: BSD 3-Clause](https://img.shields.io/badge/License-BSD--3--Clause-blue.svg)](./LICENSE)
[![Reproducibility Status](https://img.shields.io/badge/Reproducibility-100%25%20Verified%20(Level%20A--E)-success.svg)](./REPRODUCIBILITY_MATRIX.csv)
[![Tests Passing](https://img.shields.io/badge/tests-10%2F10%20passed-brightgreen.svg)](./tests/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24463279.svg)](https://doi.org/10.5281/zenodo.24463279)

Publication-grade research software package supporting the computational materials and environmental engineering manuscript:

> **"Study-grouped and leave-one-study-out evaluation of machine-learning models for time-resolved Cr(VI) and Pb(II) uptake on activated carbons using pre-assay inputs."**
> *Lead Author & Research Supervisor:* **Dr. V. Karthik** (ORCID: [0009-0002-9336-8287](https://orcid.org/0009-0002-9336-8287))
> *Affiliation:* Department of Civil Engineering, Karpagam Academy of Higher Education, Coimbatore, Tamil Nadu, India.
> *Contact Email:* `karthik.vasanthakumar@kahedu.edu.in`

---

## Table of Contents
1. [Overview and Scientific Objectives](#overview-and-scientific-objectives)
2. [Cohort Definition and Provenance](#cohort-definition-and-provenance)
3. [Evaluation Methodology and Validation Regimes](#evaluation-methodology-and-validation-regimes)
4. [Model Families and Physical Constraints](#model-families-and-physical-constraints)
5. [Canonical Performance Benchmarks (Table 1)](#canonical-performance-benchmarks-table-1)
6. [Repository Architecture](#repository-architecture)
7. [Installation and Environment Setup](#installation-and-environment-setup)
8. [Execution Guide and Reproduction](#execution-guide-and-reproduction)
9. [Scientific Quality Control and Anti-Leakage](#scientific-quality-control-and-anti-leakage)
10. [Data Governance and Licensing](#data-governance-and-licensing)
11. [Citation and Attribution](#citation-and-attribution)

---

## 1. Overview and Scientific Objectives

Adsorption onto activated carbons is a cornerstone technology for industrial effluent decontamination and heavy-metal removal. Traditional kinetic modeling relies on semi-empirical differential equations (pseudo-first-order, pseudo-second-order, intraparticle diffusion, and Elovich equations) that require fitting post-hoc parameters to experimental time-series curves.

This research software implements a machine-learning framework to predict continuous, dynamic kinetic uptake ($q_t$, mg/g) directly from **pre-assay physical, chemical, and operational inputs**—measured *prior* to running batch adsorption assays.

### Key Capabilities:
- **Zero In-Assay Leakage:** Relies strictly on pre-experimental descriptors: initial concentration ($C_0$), adsorbent dosage, solution pH, temperature, contact time ($t$), BET surface area, pore volume, pore diameter, and derived mass-transfer interaction terms.
- **Realistic Out-of-Study Evaluation:** Evaluates candidate models under rigorous study-grouped and leave-one-study-out (LOSO) cross-validation to assess generalization to unseen laboratories and adsorbent preparation batches.
- **Physical Monotonicity Enforcement:** Implements a monotonic contact-time constraint ($\partial q_t / \partial t \ge 0$) via tree-based HistGradientBoosting to prevent non-physical desorption artifacts in forward time trajectory forecasts.
- **Rigorous Null Baseline Benchmarking:** Benchmarks all models against training-fold study-median null baselines (CARB_BASE_01) to verify genuine predictive skill beyond inter-study variance.

---

## 2. Cohort Definition and Provenance

The evaluation is conducted on DR-040B Category 1 verified dynamic kinetic adsorption records:
- **Total Category 1 Population:** $N = 438$ time-resolved observations across 20 independent published studies.
- **Chromium(VI) Sub-cohort:** $N = 120$ observations across 5 published studies.
  - Labied et al. (2018) contributes 60.83% of Cr(VI) records.
- **Lead(II) Sub-cohort:** $N = 318$ observations across 15 published studies.
  - Depci et al. (2012) is the largest single study contributor (17.92%).

All data are governed by strict provenance registers tracking original study DOIs, adsorbent precursor types, activation methods, and solution chemistries.

---

## 3. Evaluation Methodology and Validation Regimes

To strictly eliminate cross-study data leakage, evaluation follows out-of-distribution (OOD) grouped designs:

1. **Chromium(VI) — 5-Fold Leave-One-Study-Out CV (LOSO-CV):**
   - Each fold holds out an entire published study ($K=5$).
   - Models are trained on $N \approx 96$ observations and evaluated on the held-out study ($N \approx 24$).
2. **Lead(II) — Primary 5-Fold Study-Grouped CV:**
   - Studies are sorted alphabetically and partitioned modulo 5 (3 studies per fold, $K=5$).
   - Balances training set diversity while ensuring zero overlap of experimental literature sources.
3. **Lead(II) — Sensitivity 15-Fold Leave-One-Study-Out CV (LOSO-CV):**
   - Every single study is held out individually ($K=15$).
   - Evaluates worst-case cross-laboratory transferability.

All data transformations (feature scaling, imputation, encoding) are fitted **strictly inside** training folds. Out-of-fold predictions are clipped at $q_t \ge 0.0$ to respect physical non-negativity.

---

## 4. Model Families and Physical Constraints

The package evaluates six continuous regression model architectures:
1. **Ridge Regression:** L2-regularized linear model with in-fold standard scaling.
2. **ElasticNet Regression:** Combined L1/L2-regularized linear model ($l_1 = 0.5$, $\alpha = 0.1$).
3. **Random Forest Regressor:** Non-linear bagged ensemble of 300 decision trees (`max_depth=8`, `min_samples_leaf=2`).
4. **Extra Trees Regressor:** Extremely randomized tree ensemble of 300 trees (`max_depth=8`, `min_samples_leaf=2`).
5. **HistGradientBoosting (Unconstrained):** Gradient-boosted histogram trees (`max_iter=150`, `max_depth=5`, `lr=0.05`).
6. **HistGradientBoosting (Monotonic Time):** Identical architecture with an enforced monotonic constraint (`monotonic_cst=[+1, 0, ..., 0]`) enforcing non-decreasing kinetic capacity with increasing contact time.

---

## 5. Canonical Performance Benchmarks (Table 1)

Performance metrics reproduced from authoritative Phase 3.2A reconciliation records:

| Analyte | Model Family | Validation Regime | MAE (mg/g) | RMSE (mg/g) | $R^2_{\text{OOD}}$ | MedAE (mg/g) |
|---|---|---|---|---|---|---|
| **Cr(VI)** | Study Median Baseline (CARB_BASE_01) | 5-Fold LOSO-CV | 30.885 | 32.874 | -1.9138 | 31.518 |
| **Cr(VI)** | **Ridge Regression (Top Model)** | **5-Fold LOSO-CV** | **7.167** | **9.118** | **0.7758** | **5.346** |
| **Cr(VI)** | ElasticNet Regression | 5-Fold LOSO-CV | 7.292 | 9.162 | 0.7737 | 5.761 |
| **Cr(VI)** | Extra Trees Regressor | 5-Fold LOSO-CV | 11.043 | 13.441 | 0.5129 | 8.824 |
| **Cr(VI)** | Monotonic HistGradientBoosting | 5-Fold LOSO-CV | 11.751 | 13.978 | 0.4732 | 10.999 |
| **Pb(II)** | Study Median Baseline (CARB_BASE_01) | 5-Fold Grouped CV | 20.849 | 26.154 | -0.4832 | 15.650 |
| **Pb(II)** | **Extra Trees Regressor (Top Model)** | **5-Fold Grouped CV** | **5.752** | **8.075** | **0.8586** | **3.890** |
| **Pb(II)** | Random Forest Regressor | 5-Fold Grouped CV | 5.989 | 8.175 | 0.8551 | 4.020 |
| **Pb(II)** | Monotonic HistGradientBoosting | 5-Fold Grouped CV | 6.842 | 9.126 | 0.8194 | 5.183 |
| **Pb(II)** | Ridge Regression | 5-Fold Grouped CV | 9.060 | 12.435 | 0.6645 | 6.541 |
| **Pb(II)** | Study Median Baseline (CARB_BASE_01) | 15-Fold LOSO-CV | 22.585 | 26.650 | -0.5399 | 19.350 |
| **Pb(II)** | **Monotonic HGB (Top Model)** | **15-Fold LOSO-CV** | **7.322** | **10.075** | **0.7799** | **5.025** |
| **Pb(II)** | Unconstrained HGB | 15-Fold LOSO-CV | 7.352 | 10.138 | 0.7771 | 4.841 |

---

## 6. Repository Architecture

```text
domain_b_adsorption_ml/
├── src/
│   ├── data_processing/
│   │   ├── data_loader.py          # Hash-verified CSV dataset loader
│   │   └── cohort_filter.py        # Isolates Category 1 N=438 cohort
│   ├── feature_engineering/
│   │   └── derive_carbon_features.py # Derives 12 pre-assay physical features
│   ├── modelling/
│   │   ├── run_carbon_models.py    # Main ML training & evaluation pipeline
│   │   ├── run_baselines.py        # In-training study-median null baselines
│   │   ├── seed.py                 # Deterministic global seed infrastructure
│   │   ├── experiment_logger.py    # Centralized CSV run logger
│   │   └── feature_importance.py   # Tree-based MDI feature importance
│   ├── validation/
│   │   └── cross_validation.py     # 5-fold LOSO, 5-fold grouped, 15-fold LOSO
│   └── metrics/
│       └── metrics.py              # MAE, RMSE, R2_OOD, MedAE, MaxAE
├── sensitivity_analysis/
│   ├── run_S2_sensitivity.py       # Provenance sensitivity (N=398 vs S0 N=438)
│   ├── run_S3_sensitivity_candidate.py # Candidate secondary sensitivity (N=387)
│   └── compare_S3.py               # Sensitivity comparison & materiality rules
├── quality_control/
│   ├── qc_scientific_integrity.py  # Non-negativity, bounds, & cohort geometry
│   └── qc_table_semantics.py       # Table 1 parity & unit validation
├── figure_generation/
│   └── generate_publication_figures_and_tables.py # Generates Figs 1-4 & Table 1
├── tests/
│   ├── test_environment.py         # Verifies packages & Python version
│   ├── test_metrics.py             # Validates metric mathematics
│   ├── test_cohort_and_integrity.py# Verifies N=438, N=120, N=318 counts
│   └── test_artifact_generation.py # Validates clean PDF/SVG figure rendering
├── docs/
│   ├── research_workflow.md        # Comprehensive computational workflow
│   ├── data_dictionary.md          # 12-feature schema, units, and ranges
│   ├── software_limitations.md     # Methodological & boundary conditions
│   ├── execution_guide.md          # Complete CLI manual and options
│   └── publication_metadata.md     # Author, DOI, and journal target metadata
├── sample_data/
│   ├── README.md                   # Data governance & IP boundaries
│   ├── mock_kinetic_features_sample.csv # 10-row synthetic feature schema
│   └── mock_record_evidence_register.csv # 10-row synthetic evidence schema
├── requirements.txt                # Confirmed & observed dependencies
├── environment.yml                 # Reproducible Conda environment
├── pyproject.toml                  # Standard Python packaging metadata
├── CITATION.cff                    # Citation File Format v1.2.0
├── ZENODO_METADATA_DRAFT.md        # Complete Zenodo deposit specification
├── REPRODUCIBILITY_MATRIX.csv      # Level A-E reproducibility specifications
├── REPRODUCTION_INSTRUCTIONS.md    # Step-by-step reproduction guide
├── PACKAGING_CHANGELOG.md          # Original vs packaged cryptographic log
├── CODE_AUDIT_REPORT.md            # Exhaustive 21-script codebase audit
├── CODE_TO_MANUSCRIPT_TRACEABILITY.csv # Script-to-manuscript trace matrix
├── CODE_RELEASE_SECURITY_AND_LICENCE_AUDIT.md # Security & IP audit
├── LICENSE                         # BSD 3-Clause open-source license
```

---

## 7. Installation and Environment Setup

### Using Conda:
```bash
conda env create -f environment.yml
conda activate domain_b_adsorption_ml
```

### Using Pip:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 8. Execution Guide and Reproduction

For detailed instructions across all reproducibility levels (Level A through E), refer to [REPRODUCTION_INSTRUCTIONS.md](./REPRODUCTION_INSTRUCTIONS.md).

### Quickstart (Running Automated Tests & Artifact Generation):
```bash
# 1. Run all unit and regression tests
python3 -m unittest discover tests

# 2. Verify scientific non-negativity and cohort counts
python3 quality_control/qc_scientific_integrity.py

# 3. Verify Table 1 numerical parity
python3 quality_control/qc_table_semantics.py

# 4. Generate publication figures (Figures 1-4) and Table 1
python3 figure_generation/generate_publication_figures_and_tables.py --pdf-only
```

---

## 9. Scientific Quality Control and Anti-Leakage

This software package is built on strict scientific anti-leakage barriers:
- **No In-Assay Leakage:** Operational features describe only pre-contact conditions.
- **Fail-Closed Verification:** Figure generation scripts verify SHA-256 hashes of all frozen prediction inputs before rendering.
- **Deterministic Randomness:** All stochastic operations (random forest bootstraps, jitter plots) are pinned to immutable integer seeds.
- **Strict Non-Negativity:** Physical constraint enforcement ensures $q_t \ge 0.0$ across all estimators.

---

## 10. Data Governance and Licensing

- **Code Licensing:** Open source under the [BSD 3-Clause License](./LICENSE). Copyright (c) 2026, Dr. V. Karthik.
- **Documentation Licensing:** Creative Commons Attribution 4.0 International (CC-BY 4.0).
- **Literature Data Redistribution:** Factual scientific observations extracted from secondary literature are documented with DOIs in [docs/data_dictionary.md](./docs/data_dictionary.md). Synthetic mock datasets are bundled in `sample_data/` for off-the-shelf testing.

---

## 11. Citation and Attribution

If you use this research software or framework in your research, please cite the software artifact using its Zenodo DOIs. The associated research article citation will be added here after public publication.

### Persistent Identifiers (DOIs):
- **Concept DOI (All Versions):** [`10.5281/zenodo.24463279`](https://doi.org/10.5281/zenodo.24463279)
  *Resolves to the latest release of the software framework on Zenodo across all versions. Use this DOI to cite the project generally.*
- **Version-Specific DOI (v1.0.0 Release):** [`10.5281/zenodo.24463280`](https://doi.org/10.5281/zenodo.24463280)
  *Resolves specifically and immutably to release v1.0.0 archived on Zenodo. Use this DOI to cite the exact research source code, deterministic training pipelines, pre-rendered publication figure/table benchmarks, and quality-control suites supporting the research article.*

### Software BibTeX Entries:

```bibtex
@software{karthik2026domain_b_software_v1,
  author    = {Karthik, V.},
  title     = {Research Software for Study-Grouped and Leave-One-Study-Out Machine-Learning Evaluation of Cr(VI) and Pb(II) Adsorption on Activated Carbons},
  year      = {2026},
  version   = {1.0.0},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.24463280},
  url       = {https://doi.org/10.5281/zenodo.24463280}
}

@software{karthik2026domain_b_software_concept,
  author    = {Karthik, V.},
  title     = {Research Software for Study-Grouped and Leave-One-Study-Out Machine-Learning Evaluation of Cr(VI) and Pb(II) Adsorption on Activated Carbons},
  year      = {2026},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.24463279},
  url       = {https://doi.org/10.5281/zenodo.24463279}
}
```

*Note: The associated peer-reviewed research article citation will be added here once publicly available.*
