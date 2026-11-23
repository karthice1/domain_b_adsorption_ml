# Sample Data and Mock Schemas for Domain B Adsorption ML

## Data Redistribution Governance & Licensing Boundary

In accordance with scholarly software engineering standards and copyright compliance:
- Raw observation tables extracted from third-party published journal literature cannot be redistributed under open-source software licenses without explicit secondary distribution rights from original publishers and copyright holders.
- To maintain complete reproducibility while preserving intellectual property compliance, this directory provides **mock sample datasets** that strictly adhere to the exact column schemas, data types, physical units, and naming conventions of the full canonical datasets.

## Full Dataset Availability and Reconstruction

1. **Local Project Environment:**
   When running inside the author's research repository (`/Users/karthik/research_project`), the execution scripts automatically locate the frozen canonical matrices at:
   - Feature Matrix: `phase2b/phase2b_bounded_closeout/PHASE2B_REMEDIATION_CARBON_FEATURE_MATRIX_CORRECTED.csv` (783 rows, SHA-256: `6c0531d1...`)
   - Evidence Register: `phase3/versioned_phase3_protocol_freeze/dr040b_reconciliation/DR040B_DOMAIN_B_RECORD_EVIDENCE_REGISTER.csv` (783 rows, SHA-256: `1850fc46...`)
   - Out-of-Fold Predictions: `phase3/model_development/domain_B_carbon/results/CARB_CR_CANDIDATE_OOF_PREDICTIONS.csv` & `CARB_PB_CANDIDATE_OOF_PREDICTIONS.csv`

2. **Literature Reconstruction:**
   Users outside the private research repository can reconstruct the exact dataset by following the step-by-step extraction protocol detailed in [docs/data_dictionary.md](../docs/data_dictionary.md) and referencing the 20 primary peer-reviewed source literature articles cited in the manuscript.

3. **Mock Data Usage:**
   The mock datasets in this directory allow researchers to test all code pipelines, import structures, feature engineering routines, and model training syntax without requiring access to proprietary or licensed literature extracts.
