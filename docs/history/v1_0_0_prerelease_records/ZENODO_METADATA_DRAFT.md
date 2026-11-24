> **SUPERSEDED HISTORICAL RECORD (added in v1.0.1, 2026-11-23).** This is a pre-release working record of v1.0.0, kept unchanged below this banner for provenance. It is not current documentation. Superseded content includes its draft metadata (DOI "pending"; "complete, reproducible" description). The published Zenodo records are authoritative. For current information see `README.md`, `docs/` and `RELEASE_AUDIT_V1_0_1.md`. Original location: `ZENODO_METADATA_DRAFT.md` (repository root); original SHA-256: `82178920c19a9e9a519dca9ae46182f37a3d49cbb4e92b46e32007badc7a199c`.

---

# ZENODO DEPOSIT METADATA SPECIFICATION (DRAFT)

**Package Identifier:** `domain_b_adsorption_ml`  
**Target Platform:** Zenodo (CERN) Open Research Repository  
**Upload Type:** Software (`software`)  
**Publication Date:** 2026-11-23  

---

## 1. Human-Readable Deposit Summary

| Metadata Field | Value |
|---|---|
| **Title** | Research Software for Study-Grouped and Leave-One-Study-Out Machine-Learning Evaluation of Cr(VI) and Pb(II) Adsorption on Activated Carbons |
| **Creators / Authors** | Dr. V. Karthik (ORCID: `0009-0002-9336-8287`, Affiliation: Karpagam Academy of Higher Education) |
| **Description** | Open-source Python research software implementing study-grouped and leave-one-study-out (LOSO) cross-validation evaluation of machine-learning models (Ridge, ElasticNet, Random Forest, Extra Trees, and monotonic HistGradientBoosting) for predicting dynamic kinetic uptake ($q_t$, mg/g) of Cr(VI) and Pb(II) on activated carbons using pre-assay operational, structural, and chemical descriptors. |
| **Keywords** | Machine Learning; Activated Carbon; Adsorption Kinetics; Heavy Metal Remediation; Chromium(VI); Lead(II); Leave-One-Study-Out Cross-Validation; Study-Grouped Cross-Validation; Monotonic Gradient Boosting; Computational Environmental Engineering |
| **Access Right** | Open Access (`open`) |
| **License** | BSD 3-Clause License (`BSD-3-Clause`) |
| **Version** | `1.0.0` |
| **Related Identifiers** | `isSupplementTo` -> Manuscript: *Study-grouped and leave-one-study-out evaluation of machine-learning models for time-resolved Cr(VI) and Pb(II) uptake on activated carbons using pre-assay inputs.* (DOI pending publication) |
| **Communities** | `environmental-science`, `materials-science`, `computational-chemistry`, `open-research-software` |

---

## 2. Machine-Readable Zenodo JSON Deposit Schema (`.zenodo.json`)

```json
{
  "title": "Research Software for Study-Grouped and Leave-One-Study-Out Machine-Learning Evaluation of Cr(VI) and Pb(II) Adsorption on Activated Carbons",
  "upload_type": "software",
  "publication_date": "2026-11-23",
  "version": "1.0.0",
  "description": "<p>This software package contains the complete, reproducible Python code, validation schemes, and figure generation routines for the research study: <strong>Study-grouped and leave-one-study-out evaluation of machine-learning models for time-resolved Cr(VI) and Pb(II) uptake on activated carbons using pre-assay inputs</strong>.</p><p>Key capabilities include:</p><ul><li>Evaluation of six candidate regression architectures across Cr(VI) (N=120) and Pb(II) (N=318) dynamic adsorption datasets.</li><li>Strict out-of-distribution evaluation using 5-fold and 15-fold Leave-One-Study-Out cross-validation.</li><li>Monotonic contact-time constraints to guarantee physically valid kinetic uptake trajectories.</li><li>Automated generation of publication-grade figures (Figures 1-4) in multi-format vector (SVG, PDF) and high-resolution raster (TIFF 600 dpi, PNG 300 dpi) outputs.</li></ul>",
  "creators": [
    {
      "name": "Karthik, V.",
      "affiliation": "Department of Civil Engineering, Karpagam Academy of Higher Education, Coimbatore, Tamil Nadu, India",
      "orcid": "0009-0002-9336-8287"
    }
  ],
  "access_right": "open",
  "license": "bsd-3-clause",
  "keywords": [
    "Machine Learning",
    "Activated Carbon",
    "Heavy Metals",
    "Adsorption Kinetics",
    "Chromium Remediation",
    "Lead Remediation",
    "Leave-One-Study-Out",
    "Grouped Cross-Validation",
    "Environmental Engineering"
  ],
  "communities": [
    { "identifier": "environmental-engineering" },
    { "identifier": "computational-materials" },
    { "identifier": "open-science" }
  ],
  "related_identifiers": [
    {
      "relation": "isSupplementTo",
      "identifier": "10.1016/j.envres.2026.XXXXXX",
      "scheme": "doi",
      "resource_type": "publication-article"
    }
  ]
}
```
