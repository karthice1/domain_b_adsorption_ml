# Domain B Adsorption ML: Machine-Learning Evaluation of Time-Resolved Cr(VI) and Pb(II) Uptake on Activated Carbons

[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue.svg)](https://www.python.org/)
[![License: BSD 3-Clause](https://img.shields.io/badge/License-BSD--3--Clause-blue.svg)](./LICENSE)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24463279.svg)](https://doi.org/10.5281/zenodo.24463279)

Research software accompanying the manuscript:

> **"Study-grouped and leave-one-study-out evaluation of machine-learning models for time-resolved Cr(VI) and Pb(II) uptake on activated carbons using pre-assay inputs."**
> The manuscript has not yet been published. It has not been peer reviewed.
> *Software author:* **Dr. V. Karthik** (ORCID: [0009-0002-9336-8287](https://orcid.org/0009-0002-9336-8287)), Department of Civil Engineering, Karpagam Academy of Higher Education, Coimbatore, Tamil Nadu, India. Contact: `karthik.vasanthakumar@kahedu.edu.in`

**Version 1.0.1** corrects documentation and metadata errors in v1.0.0. The Python code is unchanged. See [CHANGELOG.md](./CHANGELOG.md) and [RELEASE_AUDIT_V1_0_1.md](./RELEASE_AUDIT_V1_0_1.md).

---

## Table of Contents
1. [Overview](#1-overview)
2. [Records and provenance](#2-records-and-provenance)
3. [Validation designs](#3-validation-designs)
4. [Models](#4-models)
5. [Out-of-fold benchmark metrics](#5-out-of-fold-benchmark-metrics)
6. [Reproducibility scope](#6-reproducibility-scope)
7. [Repository architecture](#7-repository-architecture)
8. [Installation](#8-installation)
9. [Execution](#9-execution)
10. [Quality control](#10-quality-control)
11. [Data governance and licensing](#11-data-governance-and-licensing)
12. [Citation](#12-citation)

---

## 1. Overview

Kinetic adsorption studies commonly fit empirical rate laws (for example pseudo-first-order and pseudo-second-order models) to each measured uptake curve. This software instead evaluates regression models that predict time-resolved uptake ($q_t$, mg/g) from 12 **pre-assay inputs**. These are quantities known before an adsorption assay begins:
- the operating conditions $C_0$, dose, pH, temperature and contact time;
- the textural properties BET surface area, mean pore diameter and total pore volume;
- four arithmetic transformations of these.

The equilibrium or residual concentration, the percentage removal and the equilibrium capacity are not used as inputs.

Main features:
- **Study-aware validation.** All records of a study stay in the same fold, so test predictions do not draw on the study's own experimental series.
- **Training-median null baseline.** In every fold, each test record is predicted with the median $q_t$ of that fold's training records. Models are compared with this null under the same folds.
- **Monotonic variant (HGB-M).** One HistGradientBoosting variant applies a non-decreasing constraint on contact time. The constraint holds only when all other inputs are fixed. Along a real batch experiment, $C_0 t$ also changes, and that input is unconstrained, so predicted uptake curves are **not guaranteed** to be non-decreasing. Whether they are was not tested. The models predict $q_t$ at a user-specified contact time. They do not forecast later uptake from earlier measurements of the same experiment.

---

## 2. Records and provenance

- **Source of the values:** the dataset published with Lamsiah et al. (2026), *Artificial Intelligence Chemistry* 4, 100117 (https://doi.org/10.1016/j.aichem.2026.100117). Its 783 Cr(VI)/Pb(II) rows were screened.
- **Category 1 records:** 438 records (120 Cr(VI) from 5 studies; 318 Pb(II) from 15 studies) were classified as time-resolved because they belong to a multi-point contact-time sequence in the compiled data.
  - This classification was made on the compiled data. It was **not** confirmed against each original publication.
  - Labied et al. (2018) supplies 73 of the 120 Cr(VI) records (60.83 %). Depci et al. (2012) is the largest Pb(II) source (57 records, 17.92 %).
- **Source verification:** only 5 of the 20 original articles were inspected in full. For the other 15 studies (240 records), only the bibliographic identity was verified; whether each value was reported, digitised or calculated is unresolved.

The 20 source studies, with verified DOIs, are listed in [docs/data_dictionary.md](./docs/data_dictionary.md).

---

## 3. Validation designs

Three designs are used. Their results must not be compared across designs.

1. **Cr(VI): 5-fold leave-one-study-out (LOSO), N = 120.** Each of the 5 studies is held out in turn. Held-out study sizes range from 8 to 73 records.
2. **Pb(II): 5-fold study-grouped, N = 318 (primary Pb(II) design).** The 15 study names are sorted alphabetically and assigned to folds by position modulo 5, giving 3 studies per fold. This is one deterministic partition; other partitions were not evaluated.
3. **Pb(II): 15-fold LOSO, N = 318.** Each study is held out in turn. This design was run for HGB-U and HGB-M only.

Feature scaling for the linear models is fitted on the training records of each fold only. Every prediction is truncated at zero, $\hat q \leftarrow \max(\hat q, 0)$.

---

## 4. Models

All models are implemented with scikit-learn and use `random_state = 42` (see `src/modelling/run_carbon_models.py`). No hyperparameter search was performed.

| Model | Settings (others at scikit-learn defaults) |
|---|---|
| Ridge | `alpha=1.0`; inputs standardised in-fold |
| ElasticNet | `alpha=0.1`, `l1_ratio=0.5`; inputs standardised in-fold |
| Random forest (RF) | 300 trees, `max_depth=8`, `min_samples_leaf=2` |
| Extra trees (ET) | 300 trees, `max_depth=8`, `min_samples_leaf=2` |
| HistGradientBoosting, unconstrained (HGB-U) | `max_iter=150`, `max_depth=5`, `min_samples_leaf=3`, `learning_rate=0.05` |
| HistGradientBoosting, monotonic (HGB-M) | as HGB-U, with `monotonic_cst=[1, 0, ..., 0]` (non-decreasing in contact time only) |

---

## 5. Out-of-fold benchmark metrics

The 18 rows below are copied from the project's canonical results file (`S1_CANONICAL_18_ROW_RECOMPUTATION.csv`, SHA-256 `9846de1b4c130cfcb1257be237962288aac95b3cea6f0d939e79783f8016df10`). That file was recomputed from the stored out-of-fold predictions. The table is not "Table 1" of the manuscript: manuscript Table 1 is a 4-row extract.

| Row | Analyte | Design | Model (identifier) | N | MAE (mg/g) | RMSE (mg/g) | $R^2_{\mathrm{OOD}}$ | MedAE (mg/g) |
|---:|---|---|---|---:|---:|---:|---:|---:|
| 0 | Cr(VI) | Cr 5-fold LOSO | Training-median null (`CARB_BASE_01_Cr_LOSO`) | 120 | 30.885 | 32.874 | -1.9138 | 31.518 |
| 1 | Cr(VI) | Cr 5-fold LOSO | Ridge (`CARB_MODEL_01_Ridge`) | 120 | 7.167 | 9.118 | 0.7758 | 5.346 |
| 2 | Cr(VI) | Cr 5-fold LOSO | ElasticNet (`CARB_MODEL_02_ElasticNet`) | 120 | 7.292 | 9.162 | 0.7737 | 5.761 |
| 3 | Cr(VI) | Cr 5-fold LOSO | RF (`CARB_MODEL_03_RandomForest`) | 120 | 12.335 | 14.598 | 0.4255 | 11.740 |
| 4 | Cr(VI) | Cr 5-fold LOSO | ET (`CARB_MODEL_04_ExtraTrees`) | 120 | 11.043 | 13.441 | 0.5129 | 8.824 |
| 5 | Cr(VI) | Cr 5-fold LOSO | HGB-U (`CARB_MODEL_05A_HistGradientBoosting_Unconstrained`) | 120 | 9.272 | 11.612 | 0.6364 | 7.533 |
| 6 | Cr(VI) | Cr 5-fold LOSO | HGB-M (`CARB_MODEL_05B_HistGradientBoosting_Monotonic`) | 120 | 9.347 | 11.692 | 0.6314 | 7.629 |
| 7 | Pb(II) | Pb 5-fold grouped | Training-median null (original grouped) (`CARB_BASE_01_Pb_OrigGrouped`) | 318 | 21.439 | 25.818 | -0.4453 | 18.945 |
| 8 | Pb(II) | Pb 5-fold grouped | Training-median null (aligned grouped) (`CARB_BASE_01_Pb_AlignedGrouped`) | 318 | 20.849 | 26.154 | -0.4832 | 18.055 |
| 9 | Pb(II) | Pb 15-fold LOSO | Training-median null (`CARB_BASE_01_Pb_LOSO15`) | 318 | 22.585 | 26.650 | -0.5399 | 19.599 |
| 10 | Pb(II) | Pb 5-fold grouped | Ridge (`CARB_MODEL_01_Ridge_Grouped`) | 318 | 9.045 | 11.517 | 0.7124 | 8.158 |
| 11 | Pb(II) | Pb 5-fold grouped | ElasticNet (`CARB_MODEL_02_ElasticNet_Grouped`) | 318 | 10.578 | 12.807 | 0.6444 | 9.382 |
| 12 | Pb(II) | Pb 5-fold grouped | RF (`CARB_MODEL_03_RandomForest_Grouped`) | 318 | 5.989 | 8.175 | 0.8551 | 4.020 |
| 13 | Pb(II) | Pb 5-fold grouped | ET (`CARB_MODEL_04_ExtraTrees_Grouped`) | 318 | 5.752 | 8.075 | 0.8586 | 3.890 |
| 14 | Pb(II) | Pb 5-fold grouped | HGB-U (`CARB_MODEL_05A_HistGradientBoosting_Unconstrained_Grouped`) | 318 | 6.904 | 9.109 | 0.8201 | 5.525 |
| 15 | Pb(II) | Pb 5-fold grouped | HGB-M (`CARB_MODEL_05B_HistGradientBoosting_Monotonic_Grouped`) | 318 | 6.842 | 9.126 | 0.8194 | 5.183 |
| 16 | Pb(II) | Pb 15-fold LOSO | HGB-U (`CARB_MODEL_05A_HistGradientBoosting_Unconstrained_LOSO15`) | 318 | 7.352 | 10.138 | 0.7771 | 4.841 |
| 17 | Pb(II) | Pb 15-fold LOSO | HGB-M (`CARB_MODEL_05B_HistGradientBoosting_Monotonic_LOSO15`) | 318 | 7.322 | 10.075 | 0.7799 | 5.025 |

**Notes:**
- $R^2_{\mathrm{OOD}} = 1 - \sum(q_i-\hat q_i)^2/\sum(q_i-\bar q)^2$, where $\bar q$ is the mean of the pooled observed values.
- Rows come from three different validation designs and are not a single ranking.
- "Aligned grouped" is the Pb(II) null computed on exactly the same five study folds as the candidate models; it is the comparison used in the manuscript.
- "Original grouped" is the Pb(II) null computed on an earlier, different 5-fold study assignment; it is not used for comparisons.
- Results come from a single seed, with no confidence intervals or significance tests.

---

## 6. Reproducibility scope

Read this section before using the package to reproduce results.

1. **Inputs are not included.** The following are **not** in this package:
   - the literature-derived feature matrix and evidence register;
   - the S2/S3 exclusion lists;
   - the out-of-fold prediction files;
   - fitted model objects.

   Without them, the training pipelines, the QC scripts and the figure/table generator cannot reproduce the reported results. The synthetic files in `sample_data/` allow the code paths to be exercised only.
2. **The packaged code is a refactored version of the research scripts.** The changes are module structure, configurable file paths and command-line options. **The packaged training code has not been re-executed to regenerate the reported predictions.** The predictions and metrics reported in the manuscript were produced by the original research scripts. With those scripts, the S0 and S2 reproduction controls reproduced the stored out-of-fold predictions to within $5\times10^{-14}$ mg/g.
3. **No saved models.** Fitted models were not serialised. The project's saved model-artefact inventory (QC-11) therefore recorded the existence and deserialisation of saved model objects as **not tested**, because no saved model objects were available.
4. **Figures and tables.** The figure/table PDFs in `figure_generation/` render identically to the figures and Table 1 of the manuscript. The release check for v1.0.1 regenerated them from the stored inputs; see `RELEASE_AUDIT_V1_0_1.md`.
5. **What the checks mean.**
   - The SHA-256 manifest establishes file integrity only.
   - Passing the automated tests shows only that the tested checks pass.
   - Deterministic re-execution would not establish prospective predictive validity.
   - No prospective or external validation was performed, and no joint applicability domain was computed.

6. **Portability: running outside the author's repository.** The Python code is unchanged from v1.0.0 and contains machine-specific paths:
   - `figure_generation/generate_publication_figures_and_tables.py`, line 88: if no inputs are found near the package, the generator falls back to the absolute path `/Users/karthik/research_project`. Pass `--repo-root PATH` to point it at the inputs.
   - Same file, line 568: the Table 1 PDF uses fonts from the absolute path `/Users/karthik/miniconda3/lib/python3.13/site-packages/matplotlib/mpl-data/fonts/ttf`. On a machine without this path, font registration fails; the generator prints a warning and does **not** write the Table 1 PDF (Figures 1–4 are not affected). This was established by code inspection; it could not be demonstrated on the author's machine, where the path exists.
   - `tests/test_cohort_and_integrity.py` (line 18) and `sensitivity_analysis/run_S3_sensitivity_candidate.py` (line 33) look for their inputs two directories above the package and have no path option. They work only if the package is placed inside a directory tree laid out like the author's repository (`<root>/<any directory>/domain_b_adsorption_ml`, with the inputs under `<root>` at their repository paths).
   - `tests/test_artifact_generation.py` calls the generator without `--repo-root`.

   **Consequence: the complete test suite does not pass on an independent machine.** In a clean copy without the non-public inputs and the original repository path, `test_artifact_generation_pdf_only` **fails** (the generator stops with "Missing source file") and the 4 data-dependent tests **skip**. Measured results for v1.0.1 (identical code to v1.0.0):

   | Where the tests were run | Passed | Skipped | Failed |
   |---|---:|---:|---:|
   | Author's repository (all non-public inputs present) | 10 | 0 | 0 |
   | Copy outside the repository layout, on the author's machine (artifact test reached the inputs only through the absolute fallback) | 6 | 4 | 0 |
   | Clean copy, with access to the author's repository blocked (simulated independent machine) | 5 | 4 | 1 |

   Skipped tests are not passed tests. Only the 5 environment and metric tests can be run with the publicly distributed package contents alone. The layout-independent alternative (a small path patch) is planned for a later code release; v1.0.1 changes no code.

See [docs/software_limitations.md](./docs/software_limitations.md) for the full list of limitations.

---

## 7. Repository architecture

```text
domain_b_adsorption_ml/
├── src/
│   ├── data_processing/
│   │   ├── data_loader.py          # CSV loader with optional SHA-256 and row-count checks
│   │   └── cohort_filter.py        # Selects the 438 Category 1 records
│   ├── feature_engineering/
│   │   └── derive_carbon_features.py # Derives the 12 pre-assay inputs
│   ├── modelling/
│   │   ├── run_carbon_models.py    # Model fitting and out-of-fold evaluation
│   │   ├── run_baselines.py        # Training-median null baselines
│   │   ├── seed.py                 # Global seed setting
│   │   ├── experiment_logger.py    # CSV run registry
│   │   └── feature_importance.py   # Impurity-based (MDI) importances; diagnostic only
│   ├── validation/
│   │   └── cross_validation.py     # Cr 5-fold LOSO, Pb 5-fold grouped, Pb 15-fold LOSO
│   └── metrics/
│       └── metrics.py              # MAE, RMSE, R2, MedAE, MaxAE
├── sensitivity_analysis/
│   ├── run_S2_sensitivity.py       # Provenance sensitivity analysis (S2, N = 398)
│   ├── run_S3_sensitivity_candidate.py # Source-classification sensitivity analysis (S3, N = 387)
│   └── compare_S3.py               # S3 comparison and materiality rules
├── quality_control/
│   ├── qc_scientific_integrity.py  # Record and study counts; non-negativity of predictions
│   └── qc_table_semantics.py       # 4-row Table 1 against the reconciliation file
├── figure_generation/
│   └── generate_publication_figures_and_tables.py # Figs 1-4 and Table 1 (needs the stored inputs)
├── tests/                          # 10 unit tests (5 need the non-public inputs; see Section 6)
├── docs/
│   ├── research_workflow.md
│   ├── data_dictionary.md          # Inputs, units, ranges, verified source register
│   ├── software_limitations.md
│   ├── execution_guide.md
│   ├── publication_metadata.md
│   ├── licensing_guide.md
│   └── history/                    # Superseded v1.0.0 pre-release records (kept for provenance)
├── sample_data/                    # Synthetic demonstration files (10 rows each)
├── requirements.txt, environment.yml, pyproject.toml
├── CITATION.cff
├── CHANGELOG.md
├── RELEASE_AUDIT_V1_0_1.md
├── REPRODUCIBILITY_MATRIX.csv
├── REPRODUCTION_INSTRUCTIONS.md
├── CODE_TO_MANUSCRIPT_TRACEABILITY.csv
├── CODE_MANIFEST_SHA256.txt
└── LICENSE
```

---

## 8. Installation

### Using Conda
```bash
conda env create -f environment.yml
conda activate domain_b_adsorption_ml
```

### Using pip
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

`reportlab` (pinned to 5.1.0) is required for the Table 1 PDF; it was not declared in v1.0.0.

The S2/S3 runs and their reproduction controls used Python 3.13.5, scikit-learn 1.9.1, NumPy 2.4.6 and pandas 2.3.3. The software versions of the original S0 run were not recorded.

---

## 9. Execution

See [REPRODUCTION_INSTRUCTIONS.md](./REPRODUCTION_INSTRUCTIONS.md) and [docs/execution_guide.md](./docs/execution_guide.md). Every pipeline except the unit tests needs the non-public inputs listed in Section 6.

```bash
# Unit tests. Without the non-public inputs: 5 pass, 4 skip, 1 fails (artifact test); see Section 6
python3 -m unittest discover tests

# Integrity QC on stored out-of-fold predictions (paths to the non-public files)
python3 quality_control/qc_scientific_integrity.py --cr-pred PATH --pb-pred PATH

# Table 1 check
python3 quality_control/qc_table_semantics.py --table1-csv PATH --rmse-recon PATH

# Figures 1-4 and Table 1 (needs the stored inputs; always pass --repo-root outside the author repository)
python3 figure_generation/generate_publication_figures_and_tables.py --pdf-only --repo-root PATH
```

---

## 10. Quality control

- **Pre-assay inputs only:** no measurement taken after the assay is used as an input.
- **Input checks:** the figure/table generator verifies SHA-256 hashes and row counts of its inputs and stops on a mismatch, unless `--skip-hash` is given.
- **Fixed seeds:** all stochastic operations use fixed integer seeds (model seed 42; Fig. 4 jitter seed 20261121).
- **Truncation at zero:** out-of-fold predictions are truncated at zero. In the evaluated predictions this changed nine Cr(VI) Ridge predictions.

---

## 11. Data governance and licensing

- **Code:** [BSD 3-Clause License](./LICENSE). Copyright (c) 2026, Dr. V. Karthik.
- **Documentation:** Creative Commons Attribution 4.0 International (CC BY 4.0).
- **Literature-derived data:**
  - These are not redistributed in this package.
  - Reuse is governed by the source publications and by the compilation of Lamsiah et al. (2026).
  - The verified source register is in [docs/data_dictionary.md](./docs/data_dictionary.md).
  - `sample_data/` contains synthetic files only.

---

## 12. Citation

Cite the version you used, by its version-specific DOI.

- **Concept DOI (all versions; resolves to the latest version):** [`10.5281/zenodo.24463279`](https://doi.org/10.5281/zenodo.24463279)
- **v1.0.1:** version-specific DOI assigned by Zenodo on release; listed in `CITATION.cff` on the main branch and on the Zenodo record.
- **v1.0.0:** [`10.5281/zenodo.24463280`](https://doi.org/10.5281/zenodo.24463280). Superseded: its documentation contains errors (source-study DOIs, four benchmark rows, the operating envelope and reproducibility statements) that are corrected in v1.0.1. The code is identical.

```bibtex
@software{karthik_domain_b_adsorption_ml,
  author    = {Karthik, V.},
  title     = {Research Software for Study-Grouped and Leave-One-Study-Out Machine-Learning Evaluation of Cr(VI) and Pb(II) Adsorption on Activated Carbons},
  year      = {2026},
  version   = {1.0.1},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.24463279},
  note      = {Concept DOI; use the version-specific DOI of the version you cite}
}
```

The citation of the associated research article will be added after it is published.
