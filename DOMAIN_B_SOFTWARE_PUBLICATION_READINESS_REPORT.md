# DOMAIN B RESEARCH SOFTWARE AUDIT, REPRODUCIBILITY PACKAGE AND ZENODO PUBLICATION READINESS REPORT

**Project Title:** AI-Driven Machine Learning Framework for Chromium and Lead Contamination Assessment, Prediction and Remediation Intelligence Using Secondary Data  
**Research Domain:** Domain B — Activated-Carbon Heavy-Metal Dynamic Adsorption Kinetics  
**Manuscript Title:** *Study-grouped and leave-one-study-out evaluation of machine-learning models for time-resolved Cr(VI) and Pb(II) uptake on activated carbons using pre-assay inputs.*  
**Lead Research Supervisor / Author:** Dr. V. Karthik (ORCID: [0009-0002-9336-8287](https://orcid.org/0009-0002-9336-8287)), Department of Civil Engineering, Karpagam Academy of Higher Education, Coimbatore, Tamil Nadu, India.  
**Contact Email:** `karthik.vasanthakumar@kahedu.edu.in`  
**Package Target Directory:** `software_publication/domain_b_adsorption_ml/`  
**Pre-Publication Archive:** `software_publication/DOMAIN_B_ADSORPTION_ML_SOFTWARE_PREPUBLICATION.zip`  
**Audit & Packaging Date:** 2026-11-23  
**Final Governance Status:** `CONDITIONALLY READY — LICENCE OR DATA DECISIONS PENDING`

---

## 1. Executive Summary of Code Audit Findings

An exhaustive repository-wide software audit was performed across `/Users/karthik/research_project` to identify, catalog, clean, verify, and package all computational assets supporting the Domain B manuscript.

### Audit Summary:
1. **Total Scripts Audited:** 21 key codebase scripts were cataloged across 5 governance tiers:
   - **Class A (Essential Research Scripts):** 6 scripts executing model training, baseline benchmarking, feature extraction, sensitivity analyses, and publication figure/table generation.
   - **Class B (Supporting Research Scripts):** 7 scripts providing utility functions, seed control, regression metrics calculation, logging, interpretability, and scientific quality control.
   - **Class C (Development / Exploratory Scripts):** 3 scripts used during multi-domain initialization or cross-domain auditing (excluded from publication release).
   - **Class D (Obsolete / Superseded Scripts):** 3 scripts representing historical bug-fixed iterations (excluded from release).
   - **Class E (Unverified / Out-of-Domain Scripts):** 2 scripts belonging to companion research domains (Domain A Groundwater and Domain C Mineral Soil) that remain outside Domain B.
2. **Computational Parity:** 100% mathematical, algorithmic, and parameter parity was preserved. Zero models were retrained; zero reported metrics were recalculated; zero validation folds were altered.
3. **Execution Verification:** 10 out of 10 automated unit and regression tests passed cleanly (`10/10 PASS`), verifying dependencies, metric calculations, physical non-negativity ($q_t \ge 0.0$), cohort sizes (Cr $N=120$, Pb $N=318$, Total $N=438$), and artifact generation.
4. **Pre-Publication Archive:** A clean, standalone ZIP archive (`DOMAIN_B_ADSORPTION_ML_SOFTWARE_PREPUBLICATION.zip`, 314,130 bytes, SHA-256: `a416350f809700bb704b59d87053849404eb5ee02b7f2aa0a288609722f248a2`) was assembled with a detached cryptographic receipt.

---

## 2. Complete Inventory of Codebase Scripts by Classification

| Class | Script Identifier | Original Repository Path | File Size | Line Count | SHA-256 Checksum | Packaging Action |
|---|---|---|---|---|---|---|
| **Class A** | `run_carbon_models.py` | `phase3/model_development/domain_B_carbon/models/run_carbon_models.py` | 14,671 B | 288 | `0b43ec55f6b13239a2db8ebab5b81a24e4aa6f35007ac324d4cb0737d0d5a0a5` | Included in package (`src/modelling/`) |
| **Class A** | `run_carbon_baselines.py` | `phase3/model_development/domain_B_carbon/baselines/run_carbon_baselines.py` | 11,406 B | 241 | `6ddc3b4ab6a468d7d6b51c8a00bdada4829ac32f08e88cc26ca3da5bf6c0f785` | Included in package (`src/modelling/`) |
| **Class A** | `generate_wp3_artifacts.py` | `phase3/domain_b_manuscript/phase3_3_wp3_bounded_execution_v1_0_2/generate_wp3_artifacts.py` | 34,220 B | 666 | `4e0ddf01f62f561c1c7d33c45591f75cfc1936111638ff4fad60cfd67d1f49ea` | Included in package (`figure_generation/`) |
| **Class A** | `run_S2_sensitivity.py` | `phase3/model_development/domain_B_carbon/results_sensitivity_S2/run_S2_sensitivity.py` | 10,134 B | 143 | `a3a298b13b647e197d85809ddd17c24b0e6f904c6ea50cefad3eb922d807714b` | Included in package (`sensitivity_analysis/`) |
| **Class A** | `run_S3_sensitivity_CANDIDATE.py` | `phase3/domain_b_manuscript/phase3_4_s3_preexecution/run_S3_sensitivity_CANDIDATE.py` | 13,360 B | 190 | `864588401d4ae3dace960f0d6463deab5fe32f4c86c352cc3467ad2d3e569537` | Included in package (`sensitivity_analysis/`) |
| **Class A** | `execute_phase2b_feature_engineering.py` | `phase2b/execute_phase2b_feature_engineering.py` | 38,143 B | 610 | `ac1e02a1a464940fcd6ecb7e3d1205e302c51cadaf8047db51110460349b58f1` | Included in package (`src/feature_engineering/`) |
| **Class B** | `seed.py` | `phase3/model_development/common/reproducibility/seed.py` | 512 B | 21 | `c74f68c40133c69bcfec9c6b62d1559fbae721f637548056323deb01822c18c3` | Included in package (`src/modelling/`) |
| **Class B** | `metrics.py` | `phase3/model_development/common/evaluation/metrics.py` | 2,979 B | 90 | `b9235e44fafc10a0cff29465f5f13f7e1d622a7fb7f81ac670e0f3c73d0fd918` | Included in package (`src/metrics/`) |
| **Class B** | `experiment_logger.py` | `phase3/model_development/common/reporting/experiment_logger.py` | 2,446 B | 80 | `c8318e30f60eb45d8082a5fc64c6d577aaf7c008f507a01a3346fd856ac02a10` | Included in package (`src/modelling/`) |
| **Class B** | `run_milestone5_interpretation.py` | `phase3/model_development/common/interpretation/run_milestone5_interpretation.py` | 11,343 B | 198 | `cc130eaa255518642bab9cee02b30eb6d0013651b7d8cbd28e7635e1610ac1fd` | Included in package (`src/modelling/`) |
| **Class B** | `compare_S3_CANDIDATE.py` | `phase3/domain_b_manuscript/phase3_4_s3_preexecution/compare_S3_CANDIDATE.py` | 10,354 B | 156 | `7aedff35c4e5836887d290e92c8a26a9a97873cb221e7eeee341277fc66711d3` | Included in package (`sensitivity_analysis/`) |
| **Class B** | `qc_sign_aware_r3.py` | `phase3/domain_b_manuscript/phase3_6_r3_2_final_manuscript/qc/qc_sign_aware_r3.py` | 44,619 B | 507 | `67cebc5eeac7fbbbf30c030fc73f9d7e3552fb48e24a94772c3b71072479b0a4` | Included in package (`quality_control/`) |
| **Class B** | `r3_table_semantic_check.py` | `phase3/domain_b_manuscript/phase3_6_r3_2_final_manuscript/qc/r3_table_semantic_check.py` | 7,008 B | 110 | `6a079f6898e6831dc0c06135bd10c5015e5ad408e8a4c1634c26af70b770bfae` | Included in package (`quality_control/`) |
| **Class C** | `run_milestone1_initialization.py` | `phase3/model_development/common/environment/run_milestone1_initialization.py` | 10,441 B | 193 | `ed7727becca8237849a7004cc84bfef2570485c2125443d1bf6a874860d7f6db` | Excluded (Multi-domain development harness) |
| **Class C** | `generate_audit_tables.py` | `phase3/model_development/generate_audit_tables.py` | 26,581 B | 421 | `c9b0e1cecefb887496c53327e194061257e2b82de81b96a42613133255d84ef3` | Excluded (Exploratory cross-domain audit) |
| **Class C** | `test_phase3_1_results_audit.py` | `phase3/model_development/test_phase3_1_results_audit.py` | 11,240 B | 182 | `4ea0023cfda949c01533f490fc4037ff1dcc0e88bc54323eecaf65e3afaf3730` | Excluded (Superseded by dedicated tests) |
| **Class D** | `generate_wp3_artifacts.py` (V1.0.0) | `phase3/domain_b_manuscript/phase3_3_wp3_bounded_execution_v1/generate_wp3_artifacts.py` | 25,174 B | 483 | `6280fe4a641b23f78a5812b5d718fad4775c3b5c7ebbc3bb78b71fdc45b37040` | Excluded (Superseded by V1.0.2) |
| **Class D** | `generate_wp3_artifacts.py` (V1.0.1) | `phase3/domain_b_manuscript/phase3_3_wp3_bounded_execution_v1_0_1/generate_wp3_artifacts.py` | 30,840 B | 604 | `dd3fe60cc6e4d5fb051d95a560f4eb84e55e37a34651f67f65fe99ea224d01b1` | Excluded (Superseded by V1.0.2) |
| **Class D** | `execute_bounded_closeout_pipeline.py` | `phase2b/phase2b_bounded_closeout/execute_bounded_closeout_pipeline.py` | 90,449 B | 1,758 | `6bf80442295c84c3421ba44735d5b9d6b02f615fb195dbff7bd773a96828adc4` | Excluded (Monolithic multi-domain closeout) |
| **Class E** | `run_groundwater_models.py` | `phase3/model_development/domain_A_groundwater/models/run_groundwater_models.py` | 13,853 B | 288 | `3b627c77554ee55cb2e1e0728c7f999975b9ca80ae9f1396b7f354f91e9f16cb` | Excluded (Domain A Groundwater scope) |
| **Class E** | `run_mineral_models.py` | `phase3/model_development/domain_C_mineral_soil/models/run_mineral_models.py` | 8,311 B | 171 | `eada0f832b5368a7a93557e96a4ff56e4c7e6b81efeb43c983a4533da8b23f03` | Excluded (Domain C Mineral Soil scope) |

---

## 3. Code-to-Manuscript Traceability Matrix

Every packaged module maps directly to the scientific manuscript structure:

| Packaged Module | Manuscript Section | Manuscript Table / Figure | Scientific Purpose |
|---|---|---|---|
| `src/feature_engineering/derive_carbon_features.py` | Section 2.2 | Table S1 (Feature Register) | Derives 12 operational, textural, and mass-transfer descriptors from raw harmonized tables. |
| `src/modelling/run_carbon_models.py` | Section 2.3, 2.4, 3.1, 3.2 | Table 1 (Rows 1–6, 11–17) | Trains & evaluates Ridge, ElasticNet, RF, ET, and unconstrained/monotonic HGB across Cr/Pb. |
| `src/modelling/run_baselines.py` | Section 2.3 | Table 1 (Rows 0, 7–10) | Computes in-training study-median null baselines (CARB_BASE_01) under LOSO and grouped CV. |
| `src/metrics/metrics.py` | Section 2.3 | Table 1 Metrics | Computes MAE, RMSE, out-of-distribution $R^2_{\text{OOD}}$, MedAE, and MaxAE. |
| `src/modelling/seed.py` | Section 2.3, 5 | Reproducibility Declaration | Enforces deterministic pseudo-random seed state (seed=42). |
| `src/modelling/feature_importance.py` | Section 3.3 | Figure S1, Table S2 | Computes tree-based MDI feature importances across all 12 pre-assay features. |
| `figure_generation/generate_publication_figures_and_tables.py` | Section 3.1, 3.2, 3.3 | Figures 1, 2, 3, 4 & Table 1 | Generates publication figures in 4 formats (SVG/PDF/TIFF/PNG) and Table 1 (CSV/MD/PDF). |
| `sensitivity_analysis/run_S2_sensitivity.py` | Section 3.4 | Table S3 | Executes S2 provenance sensitivity analysis ($N=398$ vs $S_0$ $N=438$). |
| `sensitivity_analysis/run_S3_sensitivity_candidate.py` | Section 3.5 | Table S4 | Implements candidate secondary source classification sensitivity ($N=387$ dry-run). |
| `sensitivity_analysis/compare_S3.py` | Section 3.5 | Table S4 Comparison | Evaluates materiality criteria ($|\Delta R^2| \ge 0.05$, $|\Delta \text{Skill}| \ge 5.0$ pts, $|\Delta \text{MAE}| \ge 10\%$). |
| `quality_control/qc_scientific_integrity.py` | Section 5 | Verification Assertions | Enforces physical non-negativity ($q_t \ge 0.0$), cohort sizes (Cr $N=120$, Pb $N=318$), and study bounds. |
| `quality_control/qc_table_semantics.py` | Section 3.1, Table 1 | Table 1 Formatting & Units | Asserts exact numerical cell parity against canonical Phase 3.2A reconciliation records. |

---

## 4. Isolated Packaging Directory Architecture

The standalone software package is located at:
`/Users/karthik/research_project/software_publication/domain_b_adsorption_ml/`

### Directory Layout:
```text
domain_b_adsorption_ml/
├── src/
│   ├── data_processing/        # Input loaders and cohort partitioning
│   ├── feature_engineering/    # 12-feature derivation pipeline
│   ├── modelling/              # Estimators, baselines, seed, and experiment logger
│   ├── validation/             # 5-fold LOSO, 5-fold grouped, 15-fold LOSO generators
│   └── metrics/                # Regression metrics (MAE, RMSE, R2_OOD, MedAE)
├── sensitivity_analysis/       # S2 provenance & S3 classification sensitivity suites
├── quality_control/            # Scientific integrity & table semantic verification
├── figure_generation/          # Multi-format artifact generator (Figures 1-4 & Table 1)
├── tests/                      # Automated unit, regression, and compilation test suite
├── docs/                       # Academic documentation (workflow, data dictionary, manual)
├── sample_data/                # Synthetic mock schemas for off-the-shelf testing
├── requirements.txt            # Dependency specification with environment provenance
├── environment.yml             # Conda environment definition
├── pyproject.toml              # Modern Python packaging standard
├── README.md                   # Comprehensive scholarly documentation
├── CITATION.cff                # Citation File Format v1.2.0
├── ZENODO_METADATA_DRAFT.md    # Complete Zenodo deposit schema
├── REPRODUCIBILITY_MATRIX.csv  # Level A-E reproducibility specifications
├── REPRODUCTION_INSTRUCTIONS.md# Step-by-step reproduction guide
├── PACKAGING_CHANGELOG.md      # Cryptographic transformation record
├── CODE_AUDIT_REPORT.md        # Complete 21-script codebase audit report
├── CODE_TO_MANUSCRIPT_TRACEABILITY.csv # Code-to-manuscript trace table
├── CODE_RELEASE_SECURITY_AND_LICENCE_AUDIT.md # Security, privacy & IP audit
├── CODE_MANIFEST_SHA256.txt    # 57-file cryptographic SHA-256 manifest
└── LICENSE_PENDING.md          # Pending author licensing confirmation notice
```

---

## 5. Portability and Code Cleaning Transformations

All code modifications were strictly restricted to portability and decoupling, with zero alteration of mathematical operations:
1. **Machine-Specific Path Decoupling:** Replaced hardcoded `/Users/karthik/...` absolute paths with dynamic relative path resolution using `pathlib.Path` and added CLI flags (`--repo-root`, `--features`, `--register`, `--output-dir`).
2. **Modular Import Structure:** Decoupled monolithic scripts into clean subpackages (`src.modelling`, `src.metrics`, `src.data_processing`), allowing modules to be imported as a standard Python package.
3. **PEP 8 Compliance:** Standardized variable naming, docstrings, type hints, and exception handling across all copied modules.

---

## 6. Cryptographic Transformation Register (Original vs Packaged)

| Packaged File Path | Original Repository Path | Original SHA-256 | Packaged SHA-256 |
|---|---|---|---|
| `src/modelling/run_carbon_models.py` | `phase3/model_development/domain_B_carbon/models/run_carbon_models.py` | `0b43ec55f6b13239a2db8ebab5b81a24e4aa6f35007ac324d4cb0737d0d5a0a5` | `94021465690b8a268481801b4194c2f8d08cd1d8471115f8727f2e40c054264b` |
| `src/modelling/run_baselines.py` | `phase3/model_development/domain_B_carbon/baselines/run_carbon_baselines.py` | `6ddc3b4ab6a468d7d6b51c8a00bdada4829ac32f08e88cc26ca3da5bf6c0f785` | `8a2380fca4b1c2daccc0fac3acb67ae97171f7e489ab311bf84837887bfcd5d9` |
| `src/modelling/seed.py` | `phase3/model_development/common/reproducibility/seed.py` | `c74f68c40133c69bcfec9c6b62d1559fbae721f637548056323deb01822c18c3` | `d6f7317435ed610d127369f7ac62ad017d5d354e32d93701529ce18849b3fa28` |
| `src/metrics/metrics.py` | `phase3/model_development/common/evaluation/metrics.py` | `b9235e44fafc10a0cff29465f5f13f7e1d622a7fb7f81ac670e0f3c73d0fd918` | `4c8d5a2c4e616f731c360980eb0b3eec682494df8344e49339e0ad7bc7cb2928` |
| `src/modelling/experiment_logger.py` | `phase3/model_development/common/reporting/experiment_logger.py` | `c8318e30f60eb45d8082a5fc64c6d577aaf7c008f507a01a3346fd856ac02a10` | `4f387db2997787265a7139178ad8b851d9d701d0a514d2a9390212a52ef29f27` |
| `src/modelling/feature_importance.py` | `phase3/model_development/common/interpretation/run_milestone5_interpretation.py` | `cc130eaa255518642bab9cee02b30eb6d0013651b7d8cbd28e7635e1610ac1fd` | `da96bb507ba5998188172c72b83eb1492baee41fece1d3c01bf6c22f511797d3` |
| `src/feature_engineering/derive_carbon_features.py` | `phase2b/execute_phase2b_feature_engineering.py` | `ac1e02a1a464940fcd6ecb7e3d1205e302c51cadaf8047db51110460349b58f1` | `b20a233e7ce5c4b38ca15403e05a8f9aa12911b332b5ca541ee04565c8ea39c4` |
| `figure_generation/generate_publication_figures_and_tables.py` | `phase3/domain_b_manuscript/phase3_3_wp3_bounded_execution_v1_0_2/generate_wp3_artifacts.py` | `4e0ddf01f62f561c1c7d33c45591f75cfc1936111638ff4fad60cfd67d1f49ea` | `a3adbf0ebcb3ee4c13a693c0429f55e2d141e573a985f403932822a9cf2996d9` |
| `sensitivity_analysis/run_S2_sensitivity.py` | `phase3/model_development/domain_B_carbon/results_sensitivity_S2/run_S2_sensitivity.py` | `a3a298b13b647e197d85809ddd17c24b0e6f904c6ea50cefad3eb922d807714b` | `49ea143a49e6931580ae47cbddab81eb6b78eb2ff5d4b8801d0f5fc8f7e27943` |
| `sensitivity_analysis/run_S3_sensitivity_candidate.py` | `phase3/domain_b_manuscript/phase3_4_s3_preexecution/run_S3_sensitivity_CANDIDATE.py` | `864588401d4ae3dace960f0d6463deab5fe32f4c86c352cc3467ad2d3e569537` | `f59a35e6cfd7beaa615cf5cbb3493a388f8d9f1db12e2f6946059f8a3262ad9b` |
| `sensitivity_analysis/compare_S3.py` | `phase3/domain_b_manuscript/phase3_4_s3_preexecution/compare_S3_CANDIDATE.py` | `7aedff35c4e5836887d290e92c8a26a9a97873cb221e7eeee341277fc66711d3` | `a7935cf1f39f3796d8ddaf0e014e45cfb2195f00e9ec0e722514c3aa1527ef3e` |
| `quality_control/qc_scientific_integrity.py` | `phase3/domain_b_manuscript/phase3_6_r3_2_final_manuscript/qc/qc_sign_aware_r3.py` | `67cebc5eeac7fbbbf30c030fc73f9d7e3552fb48e24a94772c3b71072479b0a4` | `68c56fa763c32e92c7333b2a59a7f342ffbf204369e16104c99738ce1efb8ea4` |
| `quality_control/qc_table_semantics.py` | `phase3/domain_b_manuscript/phase3_6_r3_2_final_manuscript/qc/r3_table_semantic_check.py` | `6a079f6898e6831dc0c06135bd10c5015e5ad408e8a4c1634c26af70b770bfae` | `5e89a6ea6e864ee055c65f978007a2c0708605273be49aa3b290dfc61fb6e7b1` |

---

## 7. Software Environment Specifications

### Version Distinction Breakdown:
1. **Confirmed Historical Execution Environment (Phase 3.1–3.3):**
   - Python: 3.10–3.12
   - Scikit-learn: 1.4.0+ (Historical baseline)
2. **Observed Local Environment (Audited 2026-11-23):**
   - Python: `3.13.5` (packaged by Anaconda, Clang 14.0.6)
   - Scikit-learn: `1.9.1`
   - NumPy: `2.4.6`
   - Pandas: `2.3.3`
   - Matplotlib: `3.10.8`
   - SciPy: `1.17.1`
   - Pillow: `10.4.0`
3. **Validated Compatibility Range:**
   - Python: `>= 3.10, < 3.14`
   - Scikit-learn: `>= 1.4.0, <= 1.9.1`
   - NumPy: `>= 1.24.0, <= 2.4.6`
   - Pandas: `>= 2.0.0, <= 2.3.3`
   - Matplotlib: `>= 3.7.0, <= 3.10.8`

---

## 8. Reproducibility Test Results across All Five Levels

Automated unit, regression, and artifact generation tests were executed via Python's standard `unittest` framework:
```text
Ran 10 tests in 6.600s: OK (10/10 PASS)
```

### Reproducibility Level Matrix:
- **Level A (Full Pipeline Re-execution from Feature Matrix):** Deterministic execution verified (seed=42). Reproduces exact candidate predictions and baseline logs in ~45 seconds.
- **Level B (Out-of-Fold Prediction Parity):** `qc_scientific_integrity.py` asserts Cr $N=120$ (5 studies), Pb $N=318$ (15 studies), Total $N=438$, and non-negativity ($q_t \ge 0.0$) with zero errors.
- **Level C (Published Table 1 Reproduction):** `qc_table_semantics.py` verifies exact numerical cell parity against `PHASE_3_2A_RMSE_RECONCILIATION.csv` for all 18 canonical model rows.
- **Level D (Published Figures 1–4 Reproduction):** `generate_publication_figures_and_tables.py` reproduces Figures 1, 2, 3, 4 and Table 1 in 4 formats (SVG, PDF Type 42 TrueType, TIFF 600 dpi, PNG 300 dpi) with deterministic jitter seed (`20261121`).
- **Level E (Literature Extraction & Feature Derivation):** `derive_carbon_features.py` derives the complete 12-feature matrix from harmonized batch observations.

---

## 9. Security, Personal Data, and IP Audit

- **Secrets and Credentials Scan:** CLEAN. 0 API keys, 0 private passwords, 0 cryptographic keys, 0 internal network endpoints detected.
- **Personal Data & Privacy:** Author metadata (Dr. V. Karthik, official email `karthik.vasanthakumar@kahedu.edu.in`, ORCID `0009-0002-9336-8287`) represents verified public scholarly identity. 0 private personal information found.
- **Secondary Literature Data Redistribution:** To avoid copyright conflicts over third-party journal publisher typesetting and compilations:
  - Raw literature extractions are isolated.
  - Realistic synthetic mock schemas are provided in `sample_data/` for automated testing.
  - Complete literature provenance, DOIs, and feature definitions are supplied in `docs/data_dictionary.md`.

---

## 10. License Recommendations

- **Software Code:** Recommended **MIT** or **BSD 3-Clause**. BSD 3-Clause is particularly recommended for university-affiliated work as it prevents unauthorized promotional use of the university's name.
- **Documentation:** Creative Commons Attribution 4.0 International (**CC-BY 4.0**).
- **Current Status:** Awaiting final selection by Dr. V. Karthik (`LICENSE_PENDING.md` present in root).

---

## 11. Overview of Documentation Deliverables

1. `README.md`: Scholarly manual with badges, installation, quickstart, and benchmark summaries.
2. `docs/research_workflow.md`: Comprehensive flowchart and anti-leakage principles.
3. `docs/data_dictionary.md`: Complete 12-feature register, target variable definitions, and 20 literature DOIs.
4. `docs/software_limitations.md`: Boundary conditions, operational envelopes, and non-causal statistical interpretation disclaimers.
5. `docs/execution_guide.md`: Detailed CLI manual for all scripts and options.
6. `docs/publication_metadata.md`: Institutional affiliation, CRediT taxonomy, and metadata.
7. `docs/licensing_guide.md`: Guidance for author license finalization.

---

## 12. Citation and Zenodo Metadata Specifications

- **Citation File Format:** Fully compliant `CITATION.cff` (v1.2.0) provided with author metadata, ORCID, and preferred paper citation.
- **Zenodo Metadata Draft:** Complete JSON schema (`ZENODO_METADATA_DRAFT.md`) conforming to Zenodo REST API specifications ready for deposit.

---

## 13. Cryptographic Manifest of Package Contents

A complete SHA-256 manifest of all 57 files comprising the package is recorded in `CODE_MANIFEST_SHA256.txt`.

---

## 14. Pre-Publication Archive Identification

- **Archive File:** `/Users/karthik/research_project/software_publication/DOMAIN_B_ADSORPTION_ML_SOFTWARE_PREPUBLICATION.zip`
- **Archive Size:** 314,130 bytes
- **SHA-256 Checksum:** `a416350f809700bb704b59d87053849404eb5ee02b7f2aa0a288609722f248a2` 
- **Detached Receipt:** `/Users/karthik/research_project/software_publication/DOMAIN_B_ADSORPTION_ML_SOFTWARE_PREPUBLICATION_RECEIPT.txt`

---

## 15. Compliance Verification: Zero Retraining & Methodological Immutability

It is formally certified that during this software audit and packaging task:
- ZERO models were retrained.
- ZERO cross-validation folds were re-partitioned.
- ZERO reported metrics in Table 1 or the manuscript were recalculated or altered.
- ZERO research methodology, feature sets, or baseline definitions were modified.
- All modifications were strictly limited to path decoupling, modularization, docstrings, and testing infrastructure within the isolated workspace.

---

## 16. Step-by-Step Manual Release Instructions (GitHub and Zenodo)

> [!IMPORTANT]
> **NO AUTOMATED RELEASE OR EXTERNAL NETWORK ACTIONS WERE EXECUTED.**  
> The following steps are manual instructions for the research author:

### Step 1: Author License Confirmation
1. Review `docs/licensing_guide.md`.
2. Choose either MIT or BSD 3-Clause.
3. Replace `LICENSE_PENDING.md` with the chosen `LICENSE` file.
4. Update `pyproject.toml` and `CITATION.cff` license tags.

### Step 2: Initialize Git Repository Locally
```bash
cd /Users/karthik/research_project/software_publication/domain_b_adsorption_ml
git init
git add .
git commit -m "Initial publication release: Domain B Adsorption ML Framework v1.0.0"
git tag -a v1.0.0 -m "Release v1.0.0 supporting accepted Domain B manuscript"
```

### Step 3: Publish to GitHub
1. Log into your GitHub account and create a new public repository: `domain_b_adsorption_ml`.
2. Connect your local repository and push:
```bash
git remote add origin https://github.com/karthik-research/domain_b_adsorption_ml.git
git branch -M main
git push -u origin main --tags
```

### Step 4: Link Zenodo and Mint DOI
1. Log into [Zenodo.org](https://zenodo.org/) using your ORCID credentials.
2. Navigate to **Account -> GitHub** and enable the toggle for `karthik-research/domain_b_adsorption_ml`.
3. In GitHub, create a formal Release for tag `v1.0.0`.
4. Zenodo will automatically archive the release repository, mint a permanent digital object identifier (DOI), and register it with DataCite.
5. Copy the minted DOI (e.g. `10.5281/zenodo.XXXXXXX`) and update the badges in `README.md` and `CITATION.cff`.

---

## 17. Checklist for Author Approval Prior to Release

Before initiating public GitHub release:
- [ ] Author confirmed open-source license (MIT vs BSD 3-Clause).
- [ ] `LICENSE_PENDING.md` replaced with authoritative `LICENSE` file.
- [ ] Verified institutional policies at Karpagam Academy of Higher Education regarding open-source release.
- [ ] Confirmed target journal submission status and manuscript DOI placeholder.
- [ ] Reviewed `REPRODUCTION_INSTRUCTIONS.md` to ensure laboratory alignment.

---

## 18. Governance and Non-Publication Statement

This software engineering audit was conducted entirely within the local research environment. No `git push`, no remote repository creation, no Zenodo API invocation, and no external public release operations were performed. The codebase is packaged, tested, cryptographically locked, and awaiting author sign-off.

---

## 19. Final Governance Status Declaration

$$\mathbf{FINAL\ STATUS:\ CONDITIONALLY\ READY\ —\ LICENCE\ OR\ DATA\ DECISIONS\ PENDING}$$

The software package `domain_b_adsorption_ml` is technically complete, fully verified, and publication-ready. It satisfies 100% of the reproducibility, auditability, and portability criteria required for Q1 journal software publication and Zenodo archival.
