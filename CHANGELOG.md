# Changelog

All notable changes to this project are documented in this file. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [1.0.1] — 2026-11-24

This release corrects documentation and metadata only. **No Python source file was changed.** Every `.py` file is byte-identical to v1.0.0. No model, prediction, metric, figure or table was changed, and no model was refitted. Full record: `RELEASE_AUDIT_V1_0_1.md`.

### Fixed
- **Source-study register** (`docs/data_dictionary.md`). v1.0.0 listed incorrect DOIs for all 20 source studies, and incorrect years for 14 and record counts for 18 of them. These are replaced with the bibliography of the accompanying manuscript. Each DOI was confirmed on Crossref, and record counts were checked against the stored out-of-fold prediction files. The source compilation (Lamsiah et al., 2026) and each study's verification status were added.
- **Benchmark table** (`README.md`). Four rows of the v1.0.0 table did not match the canonical results:
  - Cr(VI) HGB-M;
  - Pb(II) Ridge (grouped);
  - the Pb(II) grouped null MedAE;
  - the Pb(II) LOSO null MedAE.

  The table now reproduces all 18 rows of the canonical results file. It is no longer labelled "Table 1".
- **Operating envelope** (`docs/software_limitations.md`). The v1.0.0 "valid bounds" did not match the data. They are replaced with the observed marginal ranges, which are stated not to define an applicability domain. An unsupported pH-precipitation statement was removed.
- **Monotonic constraint.** The v1.0.0 statements that it prevents non-physical desorption or guarantees thermodynamically sound curves were removed. It is now described as a per-input constraint on contact time, with no trajectory guarantee and not tested.
- **Null baseline.** It is now described correctly as the training-median null (median $q_t$ of each fold's training records).
- **Reproducibility statements:**
  - the "Reproducibility 100% Verified" and "tests 10/10 passed" badges were removed;
  - the non-public inputs, the refactored and not re-executed training code, and the absence of saved models (QC-11, the saved model-artefact inventory) are now stated;
  - `REPRODUCIBILITY_MATRIX.csv` records the execution status of each level.
- **`CITATION.cff`.** The `preferred-citation` entry describing the article as "Manuscript Submitted for Peer Review / under-review" was removed; the article has not been submitted. The concept DOI was added and v1.0.0 is marked as superseded.
- **`requirements.txt`.** The "Confirmed Historical Execution Environment" header was corrected: the versions of the original S0 run were not recorded. Version pins are unchanged.
- **`docs/execution_guide.md`.** QC behaviour is now described accurately: Table 1 is checked as 4 rows within stated tolerances, and the scripts skip with a warning when inputs are missing.
- **`docs/publication_metadata.md`.** The software-author record is separated from the article's CRediT statement, and the article status is "not submitted".
- **Synthetic sample data** (`sample_data/`). The study, year, journal and DOI columns no longer carry real study names with incorrect DOIs; they now use neutral synthetic labels. Numeric values are unchanged.
- **`CODE_TO_MANUSCRIPT_TRACEABILITY.csv`.** Mapped to the manuscript's actual section, table and figure numbers, with the packaged-file SHA-256 added.
- **Undeclared dependency.** `reportlab`, which is needed for the Table 1 PDF, is now declared as `reportlab==5.1.0` (the version of the author environment) in `requirements.txt`, `environment.yml` and `pyproject.toml`. No existing pin was changed.
- **Portability documentation.** The machine-specific paths in the unchanged code are now documented in the README (Section 6), `REPRODUCTION_INSTRUCTIONS.md` and `docs/software_limitations.md`:
  - the absolute repository-root fallback and the absolute font directory in the figure generator;
  - layout-dependent input paths in the data-dependent tests and the S3 script.

  The documentation states that the artifact-generation test fails in a clean copy without the non-public inputs and the original repository path. Measured results: 10 passed (author repository); 6 passed and 4 skipped (copy outside the layout); 5 passed, 4 skipped and 1 failed (clean copy).

### Changed
- Six v1.0.0 pre-release working reports were moved to `docs/history/v1_0_0_prerelease_records/` and marked as superseded. Their content is otherwise unchanged.
- `pyproject.toml` version is 1.0.1.
- `CITATION.cff` omits `date-released` until the release is tagged.
- `.gitignore` now excludes `.claude/`.
- `CODE_MANIFEST_SHA256.txt` was recomputed.

### Added
- `CHANGELOG.md`.
- `RELEASE_AUDIT_V1_0_1.md`.

## [1.0.0] — 2026-11-23

Initial release. Zenodo version DOI 10.5281/zenodo.24463280. Superseded by v1.0.1 because of the documentation errors listed above; the code is identical.
