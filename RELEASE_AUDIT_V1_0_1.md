# Release Audit — Domain B Adsorption ML v1.0.1

- **Audit date:** 2026-11-23.
- **Base:** `main` at commit `4085b4f`. That commit is v1.0.0 (tag `v1.0.0` → `c8ecb5c`) plus one post-release metadata commit that changed no code.
- **Release type:** documentation and metadata correction. **No Python source file was changed.**
- **What v1.0.0 was:** published as Zenodo record 10.5281/zenodo.24463280. That record, its tag and its release are not modified by this release.

---

## 1. Why v1.0.1 was needed

An audit of v1.0.0 against the manuscript, the canonical results file and Crossref found the following defects in the documentation:

| ID | Defect in v1.0.0 | Corrected in |
|---|---|---|
| D-1 | `docs/data_dictionary.md` listed incorrect DOIs for **all 20** source studies. 18 resolved to unrelated papers and 2 did not exist. 14 years and 18 record counts were also wrong | `docs/data_dictionary.md` |
| D-2 | Four rows of the README benchmark table did not match the canonical results: Cr(VI) HGB-M (all four metrics); Pb(II) Ridge, grouped (all four metrics); the Pb(II) grouped null MedAE; and the Pb(II) LOSO null MedAE | `README.md` §5 |
| D-3 | The "operating envelope" of "valid bounds" did not match the data and implied an applicability domain. An unsupported pH-precipitation statement was included | `docs/software_limitations.md` |
| D-4 | The monotonic constraint was described as preventing "non-physical desorption artifacts in forward time trajectory forecasts" and as "guaranteeing thermodynamically sound adsorption curves" | `README.md`, `docs/research_workflow.md`, `docs/data_dictionary.md` |
| D-5 | Badges claimed "Reproducibility 100% Verified (Level A–E)" and "tests 10/10 passed", with no statement of scope | `README.md` |
| D-6 | `CITATION.cff` (v1.0.0) described the article as "Manuscript Submitted for Peer Review", status "under-review". It has not been submitted | `CITATION.cff` |
| D-7 | Reproducibility statements overstated what was done or what is included: Level A described as verified for the packaged code; "reproducing all computational claims"; "100% parity" | `REPRODUCIBILITY_MATRIX.csv`, `REPRODUCTION_INSTRUCTIONS.md`, `README.md`, history banners |
| D-8 | `requirements.txt` called Python 3.10–3.12 / scikit-learn 1.4.0+ the "Confirmed Historical Execution Environment". The versions of the original S0 run were not recorded | `requirements.txt` |
| D-9 | The null baseline was described as a "study-median" or "held-out study-median" baseline. It is the median $q_t$ of each fold's training records | `README.md`, `docs/research_workflow.md`, `docs/execution_guide.md` |
| D-10 | The synthetic sample files attached real study names to incorrect years, journals and DOIs | `sample_data/*.csv`, `sample_data/README.md` |
| D-11 | `docs/publication_metadata.md` assigned every article CRediT role to one author, which conflicts with the article's own statement | `docs/publication_metadata.md` |
| D-12 | `CODE_TO_MANUSCRIPT_TRACEABILITY.csv` mapped scripts to sections and tables that do not exist in the manuscript (for example "Section 2.3", "Table S3") | `CODE_TO_MANUSCRIPT_TRACEABILITY.csv` |
| D-13 | `docs/execution_guide.md` said the Table 1 QC "validates all 18 table rows". It checks the 4-row Table 1 within tolerances, and it skips with a warning if its inputs are absent | `docs/execution_guide.md` |
| D-14 | `docs/data_dictionary.md` stated measurement methods for the textural inputs (BJH, N₂ at 77 K, P/P₀ ≈ 0.99) that are not recorded in the compiled data. It also called derived inputs "stoichiometric loading capacity" and "mass-transfer driving force integral proxy" | `docs/data_dictionary.md` |
| D-15 | `reportlab`, used for the Table 1 PDF, was not declared in any dependency file | `requirements.txt`, `environment.yml`, `pyproject.toml` (`reportlab==5.1.0`) |
| D-16 | The machine-specific absolute paths and layout-dependent input paths in the code were not documented, and the test badge implied the suite passes anywhere | `README.md` §6, `REPRODUCTION_INSTRUCTIONS.md`, `docs/software_limitations.md` (code unchanged by decision: Option A) |

## 2. Changes

### 2.1 File-level summary (v1.0.0 → v1.0.1)

| Category | Files |
|---|---|
| Python sources (30 files) | **Unchanged**, byte-identical to v1.0.0 |
| Unchanged non-code files | `LICENSE`, `docs/licensing_guide.md`, the five figure/table PDFs |
| Modified (18) | `.gitignore`, `environment.yml` (`reportlab==5.1.0` added to the pip section only), `CITATION.cff`, `CODE_MANIFEST_SHA256.txt`, `CODE_TO_MANUSCRIPT_TRACEABILITY.csv`, `README.md`, `REPRODUCIBILITY_MATRIX.csv`, `REPRODUCTION_INSTRUCTIONS.md`, `docs/data_dictionary.md`, `docs/execution_guide.md`, `docs/publication_metadata.md`, `docs/research_workflow.md`, `docs/software_limitations.md`, `pyproject.toml` (version and `reportlab==5.1.0`), `requirements.txt` (header comments and `reportlab==5.1.0`; existing pins unchanged), `sample_data/README.md`, `sample_data/mock_kinetic_features_sample.csv` and `sample_data/mock_record_evidence_register.csv` (identity columns only) |
| Moved (6) | `CODE_AUDIT_REPORT.md`, `CODE_RELEASE_SECURITY_AND_LICENCE_AUDIT.md`, `DOMAIN_B_SOFTWARE_PUBLICATION_READINESS_REPORT.md`, `PACKAGING_CHANGELOG.md`, `LICENCE_ACTIVATION_CHANGELOG.md`, `ZENODO_METADATA_DRAFT.md`. Each moved from the root to `docs/history/v1_0_0_prerelease_records/`, with a superseded banner prepended. Content below the banner is byte-identical to v1.0.0 |
| Added | `CHANGELOG.md`, `RELEASE_AUDIT_V1_0_1.md` (this file), `docs/history/v1_0_0_prerelease_records/README.md` |

The full line-level diff is kept with the release-validation records outside the package (`RELEASE_DIFF_V1_0_0_TO_V1_0_1.patch`).

### 2.2 Sources used for corrections

| Correction | Source |
|---|---|
| Source DOIs, years, journals, authors | Reference list [5]–[24] of the accompanying manuscript (draft R3.3.3), each DOI confirmed on Crossref (first author, year, journal) on 2026-11-23. Full texts were not re-read for this release |
| Record counts | Stored out-of-fold prediction files (counts per `Literature_Reference`), equal to manuscript Table 2.1 |
| Source status | Manuscript Table 2.1 (5 partially verified; 15 unresolved) |
| Benchmark metrics | Canonical 18-row results file `S1_CANONICAL_18_ROW_RECOMPUTATION.csv` (SHA-256 `9846de1b4c130cfcb1257be237962288aac95b3cea6f0d939e79783f8016df10`), values copied, display rounding only |
| Input ranges | Manuscript Table 2.2 and Section 2.2 |
| Model settings | `src/modelling/run_carbon_models.py` (lines 156–161) and manuscript Section 3.1 |
| Limitations and constraint wording | Manuscript Sections 3.4 and 7 |

## 3. Verification results

All checks were run (and re-run after the final changes) on 2026-11-23 with Python 3.13.5 (miniconda), on the author's machine. Final logs: `validation/final/` in the release-validation records.

| # | Check | Result |
|---|---|---|
| K1 | Every `.py` file byte-identical to v1.0.0 (same set of 30 files) | **PASS** (0 differing) |
| K2 | Frozen inputs (8 files) and WP3 figure/table assets (24 files) hashed before and after all checks | **Unchanged** |
| K3 | Unit tests, author environment (`python -m unittest discover tests -v`, run in the repository working tree, whose `.py` files are identical) | **10 run, 10 passed, 0 skipped** |
| K4 | Unit tests, release copy outside the repository layout, on the author's machine | **10 run, 6 passed, 4 skipped**. The skipped tests are the 4 cohort/non-negativity tests (inputs not found). The artifact test passed only because of the absolute-path fallback; see note 1 |
| K4b | Unit tests, clean copy outside the repository, in a sandbox that denies all access to the author's research repository (simulated public clone) | **10 run, 5 passed, 4 skipped, 1 failed.** The failure is `test_artifact_generation_pdf_only`: the generator fell back to `/Users/karthik/research_project` and stopped with "Missing source file". See note 1 |
| K5a | `qc_scientific_integrity.py` on the stored OOF predictions | **19 passed, 0 failed** (counts 120/5, 318/15, total 438; no negative predictions) |
| K5b | `qc_table_semantics.py` on the 4-row Table 1 against the reconciliation file | **4/4 rows PASS** |
| K6 | Figures 1–4 and Table 1 regenerated by the packaged generator (PDF only), after its input SHA-256 checks passed (4/4 inputs) | Regenerated PDFs and archived package PDFs both **render-identical (100 and 300 dpi) and text-identical** to the manuscript (WP3 V1.0.2) assets |
| K7 | Source register | **20/20** DOIs equal the manuscript references. **20/20** record counts equal Table 2.1 and the OOF counts (total 438). Live Crossref re-check: all resolved. The compilation DOI equals manuscript reference [1] |
| K8 | README benchmark table | **18/18 rows** equal the canonical file (N, MAE, RMSE, R², MedAE) |
| K9 | Input ranges in `data_dictionary.md` | **12/12** equal manuscript Table 2.2 |
| K10 | README model settings | All present in the code and the README |
| K11 | Phrase scan of current documentation for the removed claims and the 20 incorrect v1.0.0 DOIs | **0 substantive hits.** 5 benign hits: "thermodynamic" in the titles of 4 cited source articles, and "LICENSE_PENDING.md" in a historical instruction in `docs/licensing_guide.md` |
| K12 | History files: banner present; body identical to v1.0.0; original removed from root | **6/6** |
| K13 | `CODE_MANIFEST_SHA256.txt` recomputed and every line verified | **PASS** (63 files listed, 63 verified) |
| K14 | `CITATION.cff` validated against the official CFF 1.2.0 JSON schema | **VALID**. For reference, the v1.0.0 file was **invalid** (`preferred-citation.status: "under-review"` is not an allowed value). `date-released` is omitted until tagging |
| K15 | Generator from the sandboxed clean copy, given `--repo-root` pointing to copies of the inputs | Exit 0. The 5 PDFs are render-identical (100/300 dpi) and text-identical to the manuscript assets |
| K16 | Unchanged package placed in a repository-like layout, sandboxed (Option A workaround) | Unit tests: **10 passed**. S3 dry run: success |
| K17 | Dependency files | `reportlab==5.1.0` in `requirements.txt`, `environment.yml` (pip section) and `pyproject.toml`. All three parse. Existing pins unchanged. The author environment satisfies every pin. As in v1.0.0, `pyproject.toml` carries lower bounds only; this is not changed |
| K18 | Unchanged non-code files | `LICENSE`, `docs/licensing_guide.md` and the 5 figure/table PDFs are byte-identical to v1.0.0. `environment.yml` differs only by the `reportlab` line |

**Note 1: clean-clone limitations of the unchanged code.** Each item below was demonstrated in a sandbox that denies access to the author's repository, or found by code inspection where stated.

1. **Absolute repository-root fallback.**
   - `figure_generation/generate_publication_figures_and_tables.py` line 88 falls back to `/Users/karthik/research_project` when no inputs are found near the package.
   - Without `--repo-root`, the generator therefore stops with "Missing source file", and `tests/test_artifact_generation.py` **fails**: it is not skipped, because the test passes no `--repo-root`.
   - With `--repo-root <inputs>`, the generator ran from a clean copy. Its five PDFs were render- and text-identical to the manuscript assets.
2. **Absolute font directory.**
   - Line 568 hard-codes `/Users/karthik/miniconda3/.../matplotlib/mpl-data/fonts/ttf` for the Table 1 PDF.
   - By code inspection: on a machine without that exact path, registering the font fails. The generator catches the error and prints a warning, so the Table 1 PDF is **not produced** and the artifact test would fail.
   - This could not be demonstrated here, because the path exists on the author's machine.
3. **`reportlab` not declared.**
   - The Table 1 PDF uses `reportlab` (5.1.0 in the author environment).
   - It is not listed in `requirements.txt`, `environment.yml` or `pyproject.toml`. Without it, the Table 1 PDF is likewise skipped with a warning.
4. **Layout-dependent defaults with no override.**
   - The data-dependent tests (`tests/test_cohort_and_integrity.py` line 18) and the S3 script (`sensitivity_analysis/run_S3_sensitivity_candidate.py` line 33) locate inputs two directories above the package. They have no command-line or environment override.
   - Placing the unchanged package inside a directory tree laid out like the author's repository (`<root>/<any>/domain_b_adsorption_ml`, with the inputs under `<root>`) made all 10 tests pass and the S3 dry run succeed, with access to the author's repository denied.
5. **Scripts with explicit path options:** the model and baseline pipelines, S2, the feature derivation, the importances and both QC scripts.
   - All of them accept explicit input paths (code inspection).
   - Running from a clean copy was demonstrated only for `qc_scientific_integrity.py` (19 passed, 0 failed). The training pipelines were not run, because running them would refit models.

**Decision (2026-11-23): Option A.**
- The `.py` files stay unchanged in v1.0.1, and these limitations are documented in `README.md` §6, `REPRODUCTION_INSTRUCTIONS.md` and `docs/software_limitations.md` §5.
- Items 1–4 also mean that **the complete test suite does not pass on an independent machine.**
- The minimal path patch (Option B) was prototyped. Its outputs were identical to the manuscript, but it was not applied; it is planned for a later code release.
- Item 3 (`reportlab`) is corrected in the dependency files.

## 4. What this release does not do

- It does not change any code path, hyperparameter, fold, seed, metric, prediction, figure or table.
- It does not refit any model.
- It does not add literature data, out-of-fold predictions or fitted models.
- It does not establish external, prospective or independent validation.
- It does not modify v1.0.0.

## 5. Items to complete at tagging

- Add `date-released: "YYYY-MM-DD"` to `CITATION.cff`, after `version`; it is currently omitted, which the CFF schema allows. Replace `RELEASE_DATE_TO_BE_SET_AT_TAGGING` in `CHANGELOG.md` with the same date.
- Recompute `CODE_MANIFEST_SHA256.txt`.
- After Zenodo assigns the v1.0.1 DOI, add it to `CITATION.cff`, the README §12 and `docs/publication_metadata.md` on `main`, in a post-release metadata commit. This commit is not part of the archived v1.0.1, as was done for v1.0.0.
