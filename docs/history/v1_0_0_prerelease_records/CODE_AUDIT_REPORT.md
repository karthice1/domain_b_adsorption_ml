> **SUPERSEDED HISTORICAL RECORD (added in v1.0.1, 2026-11-23).** This is a pre-release working record of v1.0.0, kept unchanged below this banner for provenance. It is not current documentation. Superseded content includes its statements on packaging parity and on the role of each script. For current information see `README.md`, `docs/` and `RELEASE_AUDIT_V1_0_1.md`. Original location: `CODE_AUDIT_REPORT.md` (repository root); original SHA-256: `062b6d1ec7367a4f60ba7fb25c4af01f222eb3784c382d2b719fab5baa1e84eb`.

---

# DOMAIN B RESEARCH CODE AUDIT AND CLASSIFICATION REPORT

**Project:** AI-Driven Machine Learning Framework for Chromium and Lead Contamination Assessment, Prediction and Remediation Intelligence Using Secondary Data
**Research Domain:** Domain B — Activated-Carbon Heavy-Metal Dynamic Adsorption Kinetics
**Manuscript Title:** *Study-grouped and leave-one-study-out evaluation of machine-learning models for time-resolved Cr(VI) and Pb(II) uptake on activated carbons using pre-assay inputs.*
**Lead Author / Supervisor:** Dr. V. Karthik (ORCID: 0009-0002-9336-8287), Department of Civil Engineering, Karpagam Academy of Higher Education, Coimbatore, Tamil Nadu, India
**Contact Email:** `karthik.vasanthakumar@kahedu.edu.in`
**Software Publication Target:** `software_publication/domain_b_adsorption_ml/`
**Audit Date:** 2026-11-23
**Audit Governance Status:** `AUDIT_COMPLETE_AND_VERIFIED`

## 1. Executive Summary and Audit Scope
This audit establishes the definitive, complete inventory of research software supporting the Domain B manuscript. Every script associated with the carbon adsorption kinetic evaluation was surveyed across `/Users/karthik/research_project`, inspected for inputs, outputs, computational dependencies, cryptographic identity (SHA-256), and categorized into five distinct classes:
- **Class A (Essential Research Scripts):** 6 scripts directly executing the research methodology, feature extraction, model fitting, sensitivity analysis, and publication artifact generation.
- **Class B (Supporting Research Scripts):** 7 scripts providing utility functions, seed control, regression metrics calculation, logging, interpretability, and scientific quality control.
- **Class C (Development / Exploratory Scripts):** 3 scripts used during initial milestone infrastructure validation or cross-domain prototyping (excluded from publication package).
- **Class D (Obsolete / Superseded Scripts):** 3 scripts representing historical or bug-fixed iterations (excluded from publication package).
- **Class E (Unverified / Out-of-Domain Scripts):** 2 scripts belonging to companion research domains (Domain A Groundwater and Domain C Mineral Soil) that must remain outside Domain B packaging.

## 2. Complete Codebase Inventory and Cryptographic Signatures

| Class | Script Name | Original Repository Path | Bytes | Lines | SHA-256 Checksum | Packaging Action |
|---|---|---|---|---|---|---|
| Class A | `run_carbon_models.py` | `phase3/model_development/domain_B_carbon/models/run_carbon_models.py` | 14,671 | 288 | `0b43ec55f6b13239a2db8ebab5b81a24e4aa6f35007ac324d4cb0737d0d5a0a5` | Included in Package (refactored for portability in src/modelling/) |
| Class A | `run_carbon_baselines.py` | `phase3/model_development/domain_B_carbon/baselines/run_carbon_baselines.py` | 11,406 | 241 | `6ddc3b4ab6a468d7d6b51c8a00bdada4829ac32f08e88cc26ca3da5bf6c0f785` | Included in Package (src/modelling/) |
| Class A | `generate_wp3_artifacts.py` | `phase3/domain_b_manuscript/phase3_3_wp3_bounded_execution_v1_0_2/generate_wp3_artifacts.py` | 34,220 | 666 | `4e0ddf01f62f561c1c7d33c45591f75cfc1936111638ff4fad60cfd67d1f49ea` | Included in Package (figure_generation/) |
| Class A | `run_S2_sensitivity.py` | `phase3/model_development/domain_B_carbon/results_sensitivity_S2/run_S2_sensitivity.py` | 10,134 | 143 | `a3a298b13b647e197d85809ddd17c24b0e6f904c6ea50cefad3eb922d807714b` | Included in Package (sensitivity_analysis/) |
| Class A | `run_S3_sensitivity_CANDIDATE.py` | `phase3/domain_b_manuscript/phase3_4_s3_preexecution/run_S3_sensitivity_CANDIDATE.py` | 13,360 | 190 | `864588401d4ae3dace960f0d6463deab5fe32f4c86c352cc3467ad2d3e569537` | Included in Package (sensitivity_analysis/) |
| Class A | `execute_phase2b_feature_engineering.py` | `phase2b/execute_phase2b_feature_engineering.py` | 38,143 | 610 | `ac1e02a1a464940fcd6ecb7e3d1205e302c51cadaf8047db51110460349b58f1` | Included in Package (src/feature_engineering/) |
| Class B | `seed.py` | `phase3/model_development/common/reproducibility/seed.py` | 512 | 21 | `c74f68c40133c69bcfec9c6b62d1559fbae721f637548056323deb01822c18c3` | Included in Package (src/modelling/) |
| Class B | `metrics.py` | `phase3/model_development/common/evaluation/metrics.py` | 2,979 | 90 | `b9235e44fafc10a0cff29465f5f13f7e1d622a7fb7f81ac670e0f3c73d0fd918` | Included in Package (src/metrics/) |
| Class B | `experiment_logger.py` | `phase3/model_development/common/reporting/experiment_logger.py` | 2,446 | 80 | `c8318e30f60eb45d8082a5fc64c6d577aaf7c008f507a01a3346fd856ac02a10` | Included in Package (src/modelling/) |
| Class B | `run_milestone5_interpretation.py` | `phase3/model_development/common/interpretation/run_milestone5_interpretation.py` | 11,343 | 198 | `cc130eaa255518642bab9cee02b30eb6d0013651b7d8cbd28e7635e1610ac1fd` | Included in Package (src/modelling/) |
| Class B | `compare_S3_CANDIDATE.py` | `phase3/domain_b_manuscript/phase3_4_s3_preexecution/compare_S3_CANDIDATE.py` | 10,354 | 156 | `7aedff35c4e5836887d290e92c8a26a9a97873cb221e7eeee341277fc66711d3` | Included in Package (sensitivity_analysis/) |
| Class B | `qc_sign_aware_r3.py` | `phase3/domain_b_manuscript/phase3_6_r3_2_final_manuscript/qc/qc_sign_aware_r3.py` | 44,619 | 507 | `67cebc5eeac7fbbbf30c030fc73f9d7e3552fb48e24a94772c3b71072479b0a4` | Included in Package (quality_control/) |
| Class B | `r3_table_semantic_check.py` | `phase3/domain_b_manuscript/phase3_6_r3_2_final_manuscript/qc/r3_table_semantic_check.py` | 7,008 | 110 | `6a079f6898e6831dc0c06135bd10c5015e5ad408e8a4c1634c26af70b770bfae` | Included in Package (quality_control/) |
| Class C | `run_milestone1_initialization.py` | `phase3/model_development/common/environment/run_milestone1_initialization.py` | 10,441 | 193 | `ed7727becca8237849a7004cc84bfef2570485c2125443d1bf6a874860d7f6db` | Excluded (Multi-domain development harness) |
| Class C | `generate_audit_tables.py` | `phase3/model_development/generate_audit_tables.py` | 26,581 | 421 | `c9b0e1cecefb887496c53327e194061257e2b82de81b96a42613133255d84ef3` | Excluded (Exploratory cross-domain audit) |
| Class C | `test_phase3_1_results_audit.py` | `phase3/model_development/test_phase3_1_results_audit.py` | 11,240 | 182 | `4ea0023cfda949c01533f490fc4037ff1dcc0e88bc54323eecaf65e3afaf3730` | Excluded (Superseded by dedicated domain tests) |
| Class D | `generate_wp3_artifacts.py` | `phase3/domain_b_manuscript/phase3_3_wp3_bounded_execution_v1/generate_wp3_artifacts.py` | 25,174 | 483 | `6280fe4a641b23f78a5812b5d718fad4775c3b5c7ebbc3bb78b71fdc45b37040` | Excluded (Superseded by V1.0.2) |
| Class D | `generate_wp3_artifacts.py` | `phase3/domain_b_manuscript/phase3_3_wp3_bounded_execution_v1_0_1/generate_wp3_artifacts.py` | 30,840 | 604 | `dd3fe60cc6e4fbc459eecc0a5ec729879c59496bdf0b9688b37ecaf9438c5fe6` | Excluded (Superseded by V1.0.2) |
| Class D | `execute_bounded_closeout_pipeline.py` | `phase2b/phase2b_bounded_closeout/execute_bounded_closeout_pipeline.py` | 90,449 | 1,758 | `6bf80442295c84c3421ba44735d5b9d6b02f615fb195dbff7bd773a96828adc4` | Excluded (Superseded) |
| Class E | `run_groundwater_models.py` | `phase3/model_development/domain_A_groundwater/models/run_groundwater_models.py` | 13,853 | 288 | `3b627c77554eb38c7f59b37edacc3107db4bab554a29760ff51f7d76eb8a9825` | Excluded (Domain A groundwater scope) |
| Class E | `run_mineral_models.py` | `phase3/model_development/domain_C_mineral_soil/models/run_mineral_models.py` | 8,311 | 171 | `eada0f832b53b272116a41f0e5118469586b9638edd23a2c42cc88bd445f3007` | Excluded (Domain C mineral soil scope) |

## 3. Detailed Architectural Assessment by Class

### Class A: Essential Research Script
#### `run_carbon_models.py`
- **Original Path:** `phase3/model_development/domain_B_carbon/models/run_carbon_models.py`
- **Packaged Destination:** `src/modelling/run_carbon_models.py`
- **File Dimensions:** 14,671 bytes | 288 lines
- **Cryptographic Hash (SHA-256):** `0b43ec55f6b13239a2db8ebab5b81a24e4aa6f35007ac324d4cb0737d0d5a0a5`
- **Role & Scientific Purpose:** Core machine-learning modeling pipeline. Implements Ridge, ElasticNet, RandomForest, ExtraTrees, and HistGradientBoosting (unconstrained and monotonic contact time) across Cr(VI) 5-fold LOSO-CV (N=120), Pb(II) 5-fold grouped CV (N=318), and Pb(II) 15-fold LOSO-CV (N=318). Generates canonical out-of-fold predictions.
- **Primary Inputs:** `PHASE2B_REMEDIATION_CARBON_FEATURE_MATRIX_CORRECTED.csv, DR040B_DOMAIN_B_RECORD_EVIDENCE_REGISTER.csv`
- **Primary Outputs:** `CARB_CR_CANDIDATE_OOF_PREDICTIONS.csv, CARB_PB_CANDIDATE_OOF_PREDICTIONS.csv, P3_1_EXPERIMENT_REGISTRY.csv`
- **External Software Dependencies:** numpy, pandas, scikit-learn
- **Packaging Decision:** Included in Package (refactored for portability in src/modelling/)

#### `run_carbon_baselines.py`
- **Original Path:** `phase3/model_development/domain_B_carbon/baselines/run_carbon_baselines.py`
- **Packaged Destination:** `src/modelling/run_baselines.py`
- **File Dimensions:** 11,406 bytes | 241 lines
- **Cryptographic Hash (SHA-256):** `6ddc3b4ab6a468d7d6b51c8a00bdada4829ac32f08e88cc26ca3da5bf6c0f785`
- **Role & Scientific Purpose:** Baseline benchmark pipeline. Evaluates CARB_BASE_01 (in-training-fold study median null baseline) across Cr(VI) 5-fold LOSO-CV (N=120), Pb(II) 5-fold grouped CV (N=318), Pb(II) 15-fold LOSO-CV (N=318), and Category 2 equilibrium baseline (N=196).
- **Primary Inputs:** `PHASE2B_REMEDIATION_CARBON_FEATURE_MATRIX_CORRECTED.csv, DR040B_DOMAIN_B_RECORD_EVIDENCE_REGISTER.csv`
- **Primary Outputs:** `CARB_BASE_01_CR_LOSO_OOF_PREDICTIONS.csv, CARB_BASE_01_PB_OOF_PREDICTIONS.csv`
- **External Software Dependencies:** numpy, pandas, scikit-learn
- **Packaging Decision:** Included in Package (src/modelling/)

#### `generate_wp3_artifacts.py`
- **Original Path:** `phase3/domain_b_manuscript/phase3_3_wp3_bounded_execution_v1_0_2/generate_wp3_artifacts.py`
- **Packaged Destination:** `figure_generation/generate_publication_figures_and_tables.py`
- **File Dimensions:** 34,220 bytes | 666 lines
- **Cryptographic Hash (SHA-256):** `4e0ddf01f62f561c1c7d33c45591f75cfc1936111638ff4fad60cfd67d1f49ea`
- **Role & Scientific Purpose:** Publication artifact generation pipeline (WP3 V1.0.2). Enforces pre-execution fail-closed cryptographic hash checks; reproduces Figures 1-4 in 4 vector/raster formats (SVG, PDF, TIFF 600dpi, PNG 300dpi) and Table 1 in CSV, Markdown, and PDF formats.
- **Primary Inputs:** `CARB_CR_CANDIDATE_OOF_PREDICTIONS.csv, CARB_PB_CANDIDATE_OOF_PREDICTIONS.csv, PHASE2B_REMEDIATION_CARBON_FEATURE_MATRIX_CORRECTED.csv, PHASE_3_2A_RMSE_RECONCILIATION.csv`
- **Primary Outputs:** `FIGURE_1_PARITY_PLOTS.*, FIGURE_2_RESIDUAL_DISTRIBUTIONS.*, FIGURE_3_CORPUS_TOPOLOGY.*, FIGURE_4_FEATURE_COVERAGE_POPULATION_C.*, TABLE_1_MODEL_PERFORMANCE_METRICS.*`
- **External Software Dependencies:** numpy, pandas, matplotlib, pillow
- **Packaging Decision:** Included in Package (figure_generation/)

#### `run_S2_sensitivity.py`
- **Original Path:** `phase3/model_development/domain_B_carbon/results_sensitivity_S2/run_S2_sensitivity.py`
- **Packaged Destination:** `sensitivity_analysis/run_S2_sensitivity.py`
- **File Dimensions:** 10,134 bytes | 143 lines
- **Cryptographic Hash (SHA-256):** `a3a298b13b647e197d85809ddd17c24b0e6f904c6ea50cefad3eb922d807714b`
- **Role & Scientific Purpose:** Provenance sensitivity pipeline (S2). Re-runs identical candidate ML models and study-median baselines excluding 40 records with provenance ambiguity (N=398 vs S0 N=438). Evaluates paired null reductions and delta MAE/RMSE.
- **Primary Inputs:** `PHASE2B_REMEDIATION_CARBON_FEATURE_MATRIX_CORRECTED.csv, DR040B_DOMAIN_B_RECORD_EVIDENCE_REGISTER.csv, S2_FROZEN_EXCLUSION_LIST.csv`
- **Primary Outputs:** `S0_vs_S2_COMPARISON_18_ROWS.csv, S0_vs_S2_PAIRED_NULL_REDUCTIONS.csv, S2_DIAGNOSTICS.csv, S0_vs_S2_SUMMARY.txt`
- **External Software Dependencies:** numpy, pandas, scikit-learn
- **Packaging Decision:** Included in Package (sensitivity_analysis/)

#### `run_S3_sensitivity_CANDIDATE.py`
- **Original Path:** `phase3/domain_b_manuscript/phase3_4_s3_preexecution/run_S3_sensitivity_CANDIDATE.py`
- **Packaged Destination:** `sensitivity_analysis/run_S3_sensitivity_candidate.py`
- **File Dimensions:** 13,360 bytes | 190 lines
- **Cryptographic Hash (SHA-256):** `864588401d4ae3dace960f0d6463deab5fe32f4c86c352cc3467ad2d3e569537`
- **Role & Scientific Purpose:** Source classification sensitivity pipeline (S3 candidate). Implements fail-closed dry-run verification and authorized execution excluding 51 secondary records (N=387 candidate).
- **Primary Inputs:** `PHASE2B_REMEDIATION_CARBON_FEATURE_MATRIX_CORRECTED.csv, DR040B_DOMAIN_B_RECORD_EVIDENCE_REGISTER.csv, S2_FROZEN_EXCLUSION_LIST.csv, S3_PROPOSED_EXCLUSION_LIST.csv`
- **Primary Outputs:** `S3 candidate evaluation diagnostics and comparison logs`
- **External Software Dependencies:** numpy, pandas, scikit-learn
- **Packaging Decision:** Included in Package (sensitivity_analysis/)

#### `execute_phase2b_feature_engineering.py`
- **Original Path:** `phase2b/execute_phase2b_feature_engineering.py`
- **Packaged Destination:** `src/feature_engineering/derive_carbon_features.py`
- **File Dimensions:** 38,143 bytes | 610 lines
- **Cryptographic Hash (SHA-256):** `ac1e02a1a464940fcd6ecb7e3d1205e302c51cadaf8047db51110460349b58f1`
- **Role & Scientific Purpose:** Physical and chemical feature extraction pipeline. Computes 12 pre-assay operational and material descriptors (BET, pore volume, pore diameter, dose, C0, pH, T, t, loading ratios, and mass transfer products) from harmonized observation tables.
- **Primary Inputs:** `PHASE2_REMEDIATION_CARBON_HARMONIZED.csv`
- **Primary Outputs:** `PHASE2B_REMEDIATION_CARBON_FEATURE_MATRIX.csv`
- **External Software Dependencies:** numpy, pandas
- **Packaging Decision:** Included in Package (src/feature_engineering/)

### Class B: Supporting Research Script
#### `seed.py`
- **Original Path:** `phase3/model_development/common/reproducibility/seed.py`
- **Packaged Destination:** `src/modelling/seed.py`
- **File Dimensions:** 512 bytes | 21 lines
- **Cryptographic Hash (SHA-256):** `c74f68c40133c69bcfec9c6b62d1559fbae721f637548056323deb01822c18c3`
- **Role & Scientific Purpose:** Deterministic seed setter. Enforces seed=42 across Python random, NumPy random, Scikit-learn random states, and PYTHONHASHSEED.
- **Primary Inputs:** `seed integer (default: 42)`
- **Primary Outputs:** `Configured global pseudo-random state`
- **External Software Dependencies:** random, numpy, os
- **Packaging Decision:** Included in Package (src/modelling/)

#### `metrics.py`
- **Original Path:** `phase3/model_development/common/evaluation/metrics.py`
- **Packaged Destination:** `src/metrics/metrics.py`
- **File Dimensions:** 2,979 bytes | 90 lines
- **Cryptographic Hash (SHA-256):** `b9235e44fafc10a0cff29465f5f13f7e1d622a7fb7f81ac670e0f3c73d0fd918`
- **Role & Scientific Purpose:** Statistical performance metric module. Implements MAE, RMSE, MedAE, MaxAE, and out-of-sample R2_OOD against out-of-distribution training baselines.
- **Primary Inputs:** `y_true, y_pred, y_train_mean (arrays)`
- **Primary Outputs:** `Dict of regression metrics`
- **External Software Dependencies:** numpy, scikit-learn
- **Packaging Decision:** Included in Package (src/metrics/)

#### `experiment_logger.py`
- **Original Path:** `phase3/model_development/common/reporting/experiment_logger.py`
- **Packaged Destination:** `src/modelling/experiment_logger.py`
- **File Dimensions:** 2,446 bytes | 80 lines
- **Cryptographic Hash (SHA-256):** `c8318e30f60eb45d8082a5fc64c6d577aaf7c008f507a01a3346fd856ac02a10`
- **Role & Scientific Purpose:** Standardized experiment logging module. Logs model parameters, validation folds, sample sizes, and performance metrics to a centralized CSV registry.
- **Primary Inputs:** `Run metadata dict`
- **Primary Outputs:** `P3_1_EXPERIMENT_REGISTRY.csv record`
- **External Software Dependencies:** pandas, os
- **Packaging Decision:** Included in Package (src/modelling/)

#### `run_milestone5_interpretation.py`
- **Original Path:** `phase3/model_development/common/interpretation/run_milestone5_interpretation.py`
- **Packaged Destination:** `src/modelling/feature_importance.py`
- **File Dimensions:** 11,343 bytes | 198 lines
- **Cryptographic Hash (SHA-256):** `cc130eaa255518642bab9cee02b30eb6d0013651b7d8cbd28e7635e1610ac1fd`
- **Role & Scientific Purpose:** Feature importance and interpretability module. Calculates Gini impurity reduction and permutation feature importances for ensemble models.
- **Primary Inputs:** `Trained models and feature matrices`
- **Primary Outputs:** `Feature importance rankings`
- **External Software Dependencies:** numpy, pandas, scikit-learn
- **Packaging Decision:** Included in Package (src/modelling/)

#### `compare_S3_CANDIDATE.py`
- **Original Path:** `phase3/domain_b_manuscript/phase3_4_s3_preexecution/compare_S3_CANDIDATE.py`
- **Packaged Destination:** `sensitivity_analysis/compare_S3.py`
- **File Dimensions:** 10,354 bytes | 156 lines
- **Cryptographic Hash (SHA-256):** `7aedff35c4e5836887d290e92c8a26a9a97873cb221e7eeee341277fc66711d3`
- **Role & Scientific Purpose:** Sensitivity comparison utility. Computes delta performance across baseline S0 (N=438), S2 (N=398), and S3 (N=387).
- **Primary Inputs:** `S0, S2, S3 result tables`
- **Primary Outputs:** `Sensitivity comparison report`
- **External Software Dependencies:** numpy, pandas
- **Packaging Decision:** Included in Package (sensitivity_analysis/)

#### `qc_sign_aware_r3.py`
- **Original Path:** `phase3/domain_b_manuscript/phase3_6_r3_2_final_manuscript/qc/qc_sign_aware_r3.py`
- **Packaged Destination:** `quality_control/qc_scientific_integrity.py`
- **File Dimensions:** 44,619 bytes | 507 lines
- **Cryptographic Hash (SHA-256):** `67cebc5eeac7fbbbf30c030fc73f9d7e3552fb48e24a94772c3b71072479b0a4`
- **Role & Scientific Purpose:** Rigorous scientific quality control suite. Verifies numerical signs, physical bounds (qt >= 0), metric parity, and table text alignments against manuscript claims.
- **Primary Inputs:** `Table 1 CSV, prediction CSVs, manuscript drafts`
- **Primary Outputs:** `QC validation logs and assertions`
- **External Software Dependencies:** numpy, pandas, re
- **Packaging Decision:** Included in Package (quality_control/)

#### `r3_table_semantic_check.py`
- **Original Path:** `phase3/domain_b_manuscript/phase3_6_r3_2_final_manuscript/qc/r3_table_semantic_check.py`
- **Packaged Destination:** `quality_control/qc_table_semantics.py`
- **File Dimensions:** 7,008 bytes | 110 lines
- **Cryptographic Hash (SHA-256):** `6a079f6898e6831dc0c06135bd10c5015e5ad408e8a4c1634c26af70b770bfae`
- **Role & Scientific Purpose:** Table semantics QC checker. Verifies table column definitions, units of measurement, fold structures, and summary numbers.
- **Primary Inputs:** `Table 1 CSV and markdown tables`
- **Primary Outputs:** `Semantic consistency verification report`
- **External Software Dependencies:** pandas
- **Packaging Decision:** Included in Package (quality_control/)

### Class C: Development / Exploratory Script
#### `run_milestone1_initialization.py`
- **Original Path:** `phase3/model_development/common/environment/run_milestone1_initialization.py`
- **Packaged Destination:** `N/A`
- **File Dimensions:** 10,441 bytes | 193 lines
- **Cryptographic Hash (SHA-256):** `ed7727becca8237849a7004cc84bfef2570485c2125443d1bf6a874860d7f6db`
- **Role & Scientific Purpose:** Multi-domain milestone initialization test harness for Phase 3.1. Validates schema across groundwater, carbon, and mineral soil.
- **Primary Inputs:** `Multi-domain feature matrices`
- **Primary Outputs:** `Milestone 1 log`
- **External Software Dependencies:** numpy, pandas
- **Packaging Decision:** Excluded (Multi-domain development harness)

#### `generate_audit_tables.py`
- **Original Path:** `phase3/model_development/generate_audit_tables.py`
- **Packaged Destination:** `N/A`
- **File Dimensions:** 26,581 bytes | 421 lines
- **Cryptographic Hash (SHA-256):** `c9b0e1cecefb887496c53327e194061257e2b82de81b96a42613133255d84ef3`
- **Role & Scientific Purpose:** Audit table generator for multi-domain comparison.
- **Primary Inputs:** `Experiment registries`
- **Primary Outputs:** `Audit CSVs`
- **External Software Dependencies:** pandas
- **Packaging Decision:** Excluded (Exploratory cross-domain audit)

#### `test_phase3_1_results_audit.py`
- **Original Path:** `phase3/model_development/test_phase3_1_results_audit.py`
- **Packaged Destination:** `N/A`
- **File Dimensions:** 11,240 bytes | 182 lines
- **Cryptographic Hash (SHA-256):** `4ea0023cfda949c01533f490fc4037ff1dcc0e88bc54323eecaf65e3afaf3730`
- **Role & Scientific Purpose:** Multi-domain results audit unit tests.
- **Primary Inputs:** `Phase 3.1 registries`
- **Primary Outputs:** `Test assertions`
- **External Software Dependencies:** pytest, pandas
- **Packaging Decision:** Excluded (Superseded by dedicated domain tests)

### Class D: Obsolete / Superseded Script
#### `generate_wp3_artifacts.py`
- **Original Path:** `phase3/domain_b_manuscript/phase3_3_wp3_bounded_execution_v1/generate_wp3_artifacts.py`
- **Packaged Destination:** `N/A`
- **File Dimensions:** 25,174 bytes | 483 lines
- **Cryptographic Hash (SHA-256):** `6280fe4a641b23f78a5812b5d718fad4775c3b5c7ebbc3bb78b71fdc45b37040`
- **Role & Scientific Purpose:** Version 1.0.0 WP3 artifact generator. Superseded by V1.0.2 due to timezone and font embedding bugs.
- **Primary Inputs:** `OOF predictions`
- **Primary Outputs:** `V1 artifacts`
- **External Software Dependencies:** matplotlib
- **Packaging Decision:** Excluded (Superseded by V1.0.2)

#### `generate_wp3_artifacts.py`
- **Original Path:** `phase3/domain_b_manuscript/phase3_3_wp3_bounded_execution_v1_0_1/generate_wp3_artifacts.py`
- **Packaged Destination:** `N/A`
- **File Dimensions:** 30,840 bytes | 604 lines
- **Cryptographic Hash (SHA-256):** `dd3fe60cc6e4fbc459eecc0a5ec729879c59496bdf0b9688b37ecaf9438c5fe6`
- **Role & Scientific Purpose:** Version 1.0.1 WP3 artifact generator. Superseded by V1.0.2 for final Figure 3 titles and PDF fonts.
- **Primary Inputs:** `OOF predictions`
- **Primary Outputs:** `V1.0.1 artifacts`
- **External Software Dependencies:** matplotlib
- **Packaging Decision:** Excluded (Superseded by V1.0.2)

#### `execute_bounded_closeout_pipeline.py`
- **Original Path:** `phase2b/phase2b_bounded_closeout/execute_bounded_closeout_pipeline.py`
- **Packaged Destination:** `N/A`
- **File Dimensions:** 90,449 bytes | 1,758 lines
- **Cryptographic Hash (SHA-256):** `6bf80442295c84c3421ba44735d5b9d6b02f615fb195dbff7bd773a96828adc4`
- **Role & Scientific Purpose:** Monolithic feature extraction pipeline for Phase 2B. Superseded by modular feature derivation.
- **Primary Inputs:** `Harmonized data`
- **Primary Outputs:** `Intermediate matrices`
- **External Software Dependencies:** pandas
- **Packaging Decision:** Excluded (Superseded)

### Class E: Unverified / Out-of-Domain Script
#### `run_groundwater_models.py`
- **Original Path:** `phase3/model_development/domain_A_groundwater/models/run_groundwater_models.py`
- **Packaged Destination:** `N/A`
- **File Dimensions:** 13,853 bytes | 288 lines
- **Cryptographic Hash (SHA-256):** `3b627c77554eb38c7f59b37edacc3107db4bab554a29760ff51f7d76eb8a9825`
- **Role & Scientific Purpose:** Domain A (Groundwater Contamination) spatial cross-validation and classification pipeline.
- **Primary Inputs:** `Groundwater feature matrices`
- **Primary Outputs:** `Groundwater model artifacts`
- **External Software Dependencies:** xgboost, lightgbm, scikit-learn
- **Packaging Decision:** Excluded (Domain A groundwater scope)

#### `run_mineral_models.py`
- **Original Path:** `phase3/model_development/domain_C_mineral_soil/models/run_mineral_models.py`
- **Packaged Destination:** `N/A`
- **File Dimensions:** 8,311 bytes | 171 lines
- **Cryptographic Hash (SHA-256):** `eada0f832b53b272116a41f0e5118469586b9638edd23a2c42cc88bd445f3007`
- **Role & Scientific Purpose:** Domain C (Mineral Soil Heavy Metal Adsorption) regression modeling pipeline.
- **Primary Inputs:** `Mineral soil feature matrices`
- **Primary Outputs:** `Mineral soil model artifacts`
- **External Software Dependencies:** scikit-learn
- **Packaging Decision:** Excluded (Domain C mineral soil scope)

