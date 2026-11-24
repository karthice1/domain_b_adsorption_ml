# Domain B Adsorption ML: Limitations and Scope

This document states the scientific and software limitations that apply to this package and to the results it supports. The scientific limitations follow Section 7 of the accompanying manuscript; manuscript item numbers are given in brackets.

---

## 1. Observed input ranges (not an applicability domain)

The models were trained on single-metal batch adsorption records on activated carbons. The observed marginal ranges of the 438 Category 1 records are listed in [data_dictionary.md](./data_dictionary.md) (Section 1). The key ranges are:

| Input | All records (N = 438) | Cr(VI) (N = 120) | Pb(II) (N = 318) |
|---|---|---|---|
| Contact time $t$ | 2.5–360 min | — | — |
| Initial concentration $C_0$ | 10–207.2 mg/L | — | — |
| Adsorbent dose $D$ | 0.5–6.0 g/L | — | — |
| pH | 2.0–8.0 | 2–8 | 4–7 |
| Temperature $T$ | 20–40 °C | 20–40 °C | 20–30 °C |
| BET surface area $S_{\mathrm{BET}}$ | 9.81–1824 m²/g | 369.7–1345.26 m²/g | 9.81–1824 m²/g |

**These marginal ranges do not define where the models apply.** Combinations of inputs inside every marginal range may still be far from any training record. A joint applicability analysis, such as an area of applicability, was not performed [14].

In this corpus a held-out study changes adsorbent, laboratory and protocol at the same time. In the Cr(VI) LOSO design, 111 of the 120 held-out records lie outside the training range on at least one input; in the Pb(II) 15-fold LOSO design, 131 of the 318 do. The LOSO errors are therefore estimates for transfer to a further study from the same literature population. They are not separate estimates of generalisation to new adsorbents or new laboratories [14].

Predictions at contact times longer than those sampled for comparable adsorbents and conditions are extrapolations. The models predict $q_t$ at a specified contact time; they do not forecast later uptake from earlier measurements of the same experiment.

---

## 2. Data and provenance

1. **Secondary data; limited source verification [9].**
   - All values come from the compilation of Lamsiah et al. (2026).
   - Only 5 of the 20 original articles were inspected in full.
   - For the other 15 studies (240 records), whether each value was reported, digitised or calculated is unresolved.
   - Even for the inspected studies, not every compiled value was re-extracted.
2. **Classification not confirmed at source [11].** The Category 1 (time-resolved) classification is based on the structure of the compiled data.
3. **Imbalance among Cr(VI) studies [3].**
   - One study supplies 60.83 % of the Cr(VI) records (73/120), so pooled Cr(VI) metrics are weighted towards it.
   - The Cr(VI) results rest on five studies.
4. **Repeated inputs within studies [12].** The 438 records contain 398 distinct input vectors. This sets a floor on achievable error.
5. **Single-solute batch data.** The records are single-metal batch experiments. Competitive multi-metal adsorption and fixed-bed operation are not represented.

---

## 3. Models and validation

1. **Monotonicity holds only for each input separately [1].**
   - The HGB-M constraint guarantees only that the fitted function does not decrease when contact time increases **and all other inputs are held fixed**.
   - Along a real batch experiment, the input $C_0 t$ also changes and is unconstrained, so predicted uptake curves are **not guaranteed** to be non-decreasing.
   - Whether the fitted trajectories are non-decreasing was not tested.
2. **Ceiling of tree-averaging ensembles [2].** Random forest and extra trees cannot predict above the training maximum.
3. **One fold partition for Pb(II) [18].**
   - The Pb(II) study-grouped folds come from one deterministic alphabetical modulo-5 assignment.
   - Other partitions were not evaluated.
4. **Pb(II) LOSO limited to two models [17].**
   - The 15-fold Pb(II) LOSO design was run for HGB-U and HGB-M only.
   - The comparison of all six models for Pb(II) rests on the 5-fold study-grouped design.
5. **Statistical uncertainty [13].**
   - Results come from a single seed, with no confidence intervals or significance tests.
   - Small differences between models are not statistically distinguished.
6. **Truncation at zero [8].** All predictions are truncated at zero. This changed nine Cr(VI) Ridge predictions.
7. **No prospective validation [5].**
   - No new adsorption experiments were run to test the models.
   - The S2 and S3 sensitivity analyses re-evaluate the same literature records. They are not prospective or external validation.
8. **No comparison with kinetic rate laws [19].** Pseudo-first-order, pseudo-second-order or other rate laws were not refitted to the source studies.

---

## 4. Interpretation

- **Feature importances are diagnostics only [4].** The impurity-based (MDI) importances come from an in-sample, pooled fit. They reflect statistical associations in the compiled literature data and are not evidence of an adsorption mechanism.
- Explanations for the model rankings are hypotheses [7].

---

## 5. Software and reproducibility

1. **No saved model files [6].**
   - Fitted models were not serialised.
   - The project's saved model-artefact inventory (QC-11) therefore recorded the existence and deserialisation of saved model objects as **not tested**, because no saved model objects were available.
   - Reproducibility rests on deterministic training scripts and the recorded out-of-fold predictions.
2. **Refactored code, not re-executed.**
   - The packaged scripts are refactored versions of the research scripts: module structure, configurable paths and command-line options.
   - The packaged training code has not been re-executed to regenerate the reported predictions.
   - The S0/S2 reproduction controls (agreement within $5\times10^{-14}$ mg/g) were run with the original research scripts.
3. **Inputs not included.** The literature-derived records, exclusion lists, out-of-fold predictions and fitted models are not included in this package. The reported results cannot be regenerated from the package alone.
4. **Recorded software environment.** The software versions of the original S0 run were not recorded. The S2/S3 runs used Python 3.13.5, scikit-learn 1.9.1, NumPy 2.4.6 and pandas 2.3.3.
5. **Portability (machine-specific paths).**
   - The figure generator falls back to the absolute path `/Users/karthik/research_project` (line 88) and loads Table 1 PDF fonts from an absolute miniconda path (line 568).
   - The data-dependent tests (`tests/test_cohort_and_integrity.py`, line 18) and the S3 script (line 33) locate inputs two directories above the package, with no path option.
   - In a clean copy without the non-public inputs and the original repository path, the artifact-generation test **fails** and 4 tests skip (5 passed, 4 skipped, 1 failed). The complete test suite does not pass on an independent machine.
   - The code is unchanged in v1.0.1 by decision; a path patch is planned for a later code release.
6. **Meaning of checks.**
   - The SHA-256 manifest establishes file integrity only.
   - Passing tests shows only that the tested checks pass.
   - Neither is evidence of predictive validity.
