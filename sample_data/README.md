# Sample Data: Synthetic Demonstration Files

## What these files are

`mock_kinetic_features_sample.csv` and `mock_record_evidence_register.csv` are **synthetic** files of 10 rows each. They follow the column names and data types of the project's feature matrix and record evidence register.

**They contain no literature data.** Since v1.0.1, the study, year, journal and DOI columns use neutral labels ("Synthetic study A"–"H", year 2000, "none (synthetic record)"). These labels are not connected to any real publication. In v1.0.0 these columns carried names of real studies together with incorrect years and DOIs.

The register's `Classification` column keeps the schema value `1_Directly_reported_kinetic_qt` (and `Primary_Kinetic_Dataset_Inclusion` = `TRUE`) only so that the column remains a valid example of the real schema. In these files the value is **synthetic**: it says nothing about any real record or publication.

The files let users exercise the code paths (loading, feature handling, model fitting syntax). They cannot reproduce any reported result.

## Why the real data are not included

- The modelling records were taken from the dataset published with Lamsiah et al. (2026), *Artificial Intelligence Chemistry* 4, 100117 (https://doi.org/10.1016/j.aichem.2026.100117). The 20 original studies are listed in `docs/data_dictionary.md`.
- These literature-derived values are not redistributed in this package, and their reuse is governed by the source publications.
- The out-of-fold predictions, the exclusion lists and the record evidence register are also not included.

## Paths used by the scripts in the author's research repository

When the scripts are run inside the author's research repository, they look for:
- `phase2b/phase2b_bounded_closeout/PHASE2B_REMEDIATION_CARBON_FEATURE_MATRIX_CORRECTED.csv` (feature matrix)
- `phase3/versioned_phase3_protocol_freeze/dr040b_reconciliation/DR040B_DOMAIN_B_RECORD_EVIDENCE_REGISTER.csv` (evidence register)
- `phase3/model_development/domain_B_carbon/results/CARB_CR_CANDIDATE_OOF_PREDICTIONS.csv` and `CARB_PB_CANDIDATE_OOF_PREDICTIONS.csv` (out-of-fold predictions)

Outside that repository, these files are not available, and the scripts must be given explicit paths to equivalent files.
