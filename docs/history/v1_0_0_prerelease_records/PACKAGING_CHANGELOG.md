> **SUPERSEDED HISTORICAL RECORD (added in v1.0.1, 2026-11-23).** This is a pre-release working record of v1.0.0, kept unchanged below this banner for provenance. It is not current documentation. Superseded content includes its "VERIFIED - 100% MATHEMATICAL & ALGORITHMIC PARITY" status (the packaged scripts are refactored and the training code was not re-executed); its SHA-256 register remains a valid record of the original and packaged files. For current information see `README.md`, `docs/` and `RELEASE_AUDIT_V1_0_1.md`. Original location: `PACKAGING_CHANGELOG.md` (repository root); original SHA-256: `6db4f6837dc269d114bc42f9f1764fcce3f65e851d106c49fe16d0252bf461e9`.

---

# PACKAGING CHANGELOG: DOMAIN B ADSORPTION ML FRAMEWORK

**Repository Source:** `/Users/karthik/research_project`
**Package Directory:** `software_publication/domain_b_adsorption_ml/`
**Audited Baseline:** Phase 3.3 WP3 Bounded Execution V1.0.2 & Phase 3.4 Baseline R3.2.1a
**Audit Timestamp:** 2026-11-23
**Portability Status:** VERIFIED — 100% MATHEMATICAL & ALGORITHMIC PARITY MAINTAINED

## 1. Summary of Portability and Cleaning Principles
During the packaging of the research codebase into the standalone publication package, strict non-negotiable scientific governance boundaries were maintained:
1. **Zero Mathematical or Methodological Alterations:** All estimator architectures, model hyperparameters, random seeds (42), cross-validation fold structures, in-fold preprocessing, and feature sets remain byte-for-byte identical to the accepted research baseline.
2. **Elimination of Machine-Specific Hardcoded Paths:** File paths previously pointing to fixed absolute directories (e.g. `/Users/karthik/research_project/...`) were replaced with dynamic relative path resolution using `pathlib.Path` and configurable CLI arguments (`--repo-root`, `--output-dir`, `--features`, etc.).
3. **Modular Subpackage Architecture:** Monolithic scripts were decoupled into clean, single-responsibility modules under `src/data_processing/`, `src/feature_engineering/`, `src/modelling/`, `src/validation/`, and `src/metrics/`.
4. **Cryptographic Traceability:** Every original research script and its packaged counterpart is tracked below with full SHA-256 cryptographic hashes.

## 2. Exhaustive File Transformation Register

### `src/modelling/run_carbon_models.py`
- **Original Research Path:** `phase3/model_development/domain_B_carbon/models/run_carbon_models.py`
- **Original SHA-256:** `0b43ec55f6b13239a2db8ebab5b81a24e4aa6f35007ac324d4cb0737d0d5a0a5`
- **Packaged SHA-256:** `94021465690b8a268481801b4194c2f8d08cd1d8471115f8727f2e40c054264b`
- **Refactoring & Portability Description:** Modularized import structure (import from src.modelling.seed, src.metrics.metrics, src.modelling.experiment_logger); replaced hardcoded absolute repository paths with argparse CLI flags and fallback path resolution; 100% preservation of model hyperparameters, random seed 42, feature lists, scaling pipeline, fold generators, and non-negativity clipping.

### `src/modelling/run_baselines.py`
- **Original Research Path:** `phase3/model_development/domain_B_carbon/baselines/run_carbon_baselines.py`
- **Original SHA-256:** `6ddc3b4ab6a468d7d6b51c8a00bdada4829ac32f08e88cc26ca3da5bf6c0f785`
- **Packaged SHA-256:** `8a2380fca4b1c2daccc0fac3acb67ae97171f7e489ab311bf84837887bfcd5d9`
- **Refactoring & Portability Description:** Modularized imports; added CLI argument parsing for feature matrix, evidence register, and output directory; 100% preservation of CARB_BASE_01 training-fold-median null baseline logic for Cr(VI) LOSO (N=120), Pb(II) 5-fold grouped (N=318), and Pb(II) 15-fold LOSO (N=318).

### `src/modelling/seed.py`
- **Original Research Path:** `phase3/model_development/common/reproducibility/seed.py`
- **Original SHA-256:** `c74f68c40133c69bcfec9c6b62d1559fbae721f637548056323deb01822c18c3`
- **Packaged SHA-256:** `d6f7317435ed610d127369f7ac62ad017d5d354e32d93701529ce18849b3fa28`
- **Refactoring & Portability Description:** Added type annotations, docstrings, and standalone packaging structure; preserved deterministic seed=42 configuration across random, numpy, and PYTHONHASHSEED.

### `src/metrics/metrics.py`
- **Original Research Path:** `phase3/model_development/common/evaluation/metrics.py`
- **Original SHA-256:** `b9235e44fafc10a0cff29465f5f13f7e1d622a7fb7f81ac670e0f3c73d0fd918`
- **Packaged SHA-256:** `8a4adedddf4a82e1fa46433877d0d7503e86e34cbdc8e392f1aa95c898735968`
- **Refactoring & Portability Description:** Extracted regression metrics module (MAE, RMSE, R2, MedAE, MaxAE); focused scope specifically on continuous dynamic kinetic uptake (qt, mg/g); preserved out-of-distribution R2 calculation.

### `src/modelling/experiment_logger.py`
- **Original Research Path:** `phase3/model_development/common/reporting/experiment_logger.py`
- **Original SHA-256:** `c8318e30f60eb45d8082a5fc64c6d577aaf7c008f507a01a3346fd856ac02a10`
- **Packaged SHA-256:** `0192d4b575d670173c996875ef57341f99479c5f5181d0951bb705b016344281`
- **Refactoring & Portability Description:** Added configurable registry destination path via CLI parameter or EXPERIMENT_REGISTRY_PATH environment variable; preserved full schema of 28 experiment tracking columns.

### `src/modelling/feature_importance.py`
- **Original Research Path:** `phase3/model_development/common/interpretation/run_milestone5_interpretation.py`
- **Original SHA-256:** `cc130eaa255518642bab9cee02b30eb6d0013651b7d8cbd28e7635e1610ac1fd`
- **Packaged SHA-256:** `fa3f38c615c11b44df600aaaaf79508d35ee94eafc31bc53fa89cab2a42f21cd`
- **Refactoring & Portability Description:** Extracted and modularized Domain B carbon-specific tree-based feature importance logic; derives ExtraTrees and RandomForest MDI scores across all 12 operational and textural features; exports structured CSV.

### `src/feature_engineering/derive_carbon_features.py`
- **Original Research Path:** `phase2b/execute_phase2b_feature_engineering.py`
- **Original SHA-256:** `ac1e02a1a464940fcd6ecb7e3d1205e302c51cadaf8047db51110460349b58f1`
- **Packaged SHA-256:** `a63c2756d54cc5e359c6eef1d23ff58703f7ba441112395c2c0f23f5d25d5a9f`
- **Refactoring & Portability Description:** Isolated Domain B carbon remediation feature transformation logic from multi-domain pipeline; derives operational, structural, loading, and mass transfer interaction terms; added flexible CLI paths.

### `figure_generation/generate_publication_figures_and_tables.py`
- **Original Research Path:** `phase3/domain_b_manuscript/phase3_3_wp3_bounded_execution_v1_0_2/generate_wp3_artifacts.py`
- **Original SHA-256:** `4e0ddf01f62f561c1c7d33c45591f75cfc1936111638ff4fad60cfd67d1f49ea`
- **Packaged SHA-256:** `f2f0eda5724c5610db6c2942f531842f205284dc2d7485f38a8c0a1bb9f6dd7b`
- **Refactoring & Portability Description:** Enhanced with argparse CLI parameters (--repo-root, --output-dir, --pdf-only, --skip-hash); maintained fail-closed cryptographic hash verification, TrueType Type 42 PDF font embedding, deterministic Figure 4 jitter seed (20261121), and multi-format raster/vector export.

### `sensitivity_analysis/run_S2_sensitivity.py`
- **Original Research Path:** `phase3/model_development/domain_B_carbon/results_sensitivity_S2/run_S2_sensitivity.py`
- **Original SHA-256:** `a3a298b13b647e197d85809ddd17c24b0e6f904c6ea50cefad3eb922d807714b`
- **Packaged SHA-256:** `a7a1d4e495dbe8996e5b35f859a2f6de3aa23d14e0ef73d1d4eb271b32f385c6`
- **Refactoring & Portability Description:** Refactored path resolution using pathlib and CLI arguments; preserved 40-record frozen exclusion list verification, exact 18 canonical model rows, paired null reductions, and delta calculations.

### `sensitivity_analysis/run_S3_sensitivity_candidate.py`
- **Original Research Path:** `phase3/domain_b_manuscript/phase3_4_s3_preexecution/run_S3_sensitivity_CANDIDATE.py`
- **Original SHA-256:** `864588401d4ae3dace960f0d6463deab5fe32f4c86c352cc3467ad2d3e569537`
- **Packaged SHA-256:** `aacebf6b353011cb0078efbf059c904a46fe62b52fba7db41526cfe74e70a40a`
- **Refactoring & Portability Description:** Packaged candidate S3 sensitivity evaluation; preserved fail-closed --dry-run vs --authorized execution gate and 51-record secondary exclusion list verification.

### `sensitivity_analysis/compare_S3.py`
- **Original Research Path:** `phase3/domain_b_manuscript/phase3_4_s3_preexecution/compare_S3_CANDIDATE.py`
- **Original SHA-256:** `7aedff35c4e5836887d290e92c8a26a9a97873cb221e7eeee341277fc66711d3`
- **Packaged SHA-256:** `c5ca72e09948dee042dea70e1d0e31f9cbbadb2d8608474026c75ccf6042df22`
- **Refactoring & Portability Description:** Modularized paths; preserved frozen D3 materiality thresholds (|dR2| >= 0.05, |dSkill| >= 5.0 pts, |dMAE| >= 10%), evaluation-set vs retraining effect decomposition, and tolerance TOL=1e-9.

### `quality_control/qc_scientific_integrity.py`
- **Original Research Path:** `phase3/domain_b_manuscript/phase3_6_r3_2_final_manuscript/qc/qc_sign_aware_r3.py`
- **Original SHA-256:** `67cebc5eeac7fbbbf30c030fc73f9d7e3552fb48e24a94772c3b71072479b0a4`
- **Packaged SHA-256:** `149147f03f2b850e73a2c505cc130e5f9c5a1cbcd77e6d2464708984177ec03a`
- **Refactoring & Portability Description:** Created standalone, portable scientific integrity test suite; verifies non-negativity of all continuous uptake predictions (qt >= 0), cohort sizes (Cr N=120, Pb N=318, Total N=438), and study distributions.

### `quality_control/qc_table_semantics.py`
- **Original Research Path:** `phase3/domain_b_manuscript/phase3_6_r3_2_final_manuscript/qc/r3_table_semantic_check.py`
- **Original SHA-256:** `6a079f6898e6831dc0c06135bd10c5015e5ad408e8a4c1634c26af70b770bfae`
- **Packaged SHA-256:** `e2249f888b2bf171170361ff7b050b7c4e2975eda6e42b6c722746fa1248a0da`
- **Refactoring & Portability Description:** Created modular table semantic parity checker; validates Table 1 cell values against authoritative Phase 3.2A reconciliation records.

