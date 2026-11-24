# Domain B Adsorption ML: Research Workflow

This document outlines the computational workflow of the Domain B evaluation of time-resolved Cr(VI) and Pb(II) uptake on activated carbons.

---

## 1. Workflow

```mermaid
flowchart TD
    subgraph Records
        A1["Compiled dataset of Lamsiah et al. (2026)<br/>(783 Cr(VI)/Pb(II) rows)"] --> A2["Harmonisation and schema unification<br/>(PHASE2_REMEDIATION_CARBON_HARMONIZED.csv)"]
        A2 --> A3["Record-level evidence register<br/>(DR040B_DOMAIN_B_RECORD_EVIDENCE_REGISTER.csv)"]
        A3 --> A4["Category 1 selection, classified on compiled data<br/>(N = 438; 20 original studies)"]
    end

    subgraph Inputs
        A4 --> B1["Operating conditions<br/>(C0, dose, pH, T, contact time)"]
        A4 --> B2["Textural properties<br/>(BET area, pore volume, pore diameter)"]
        A4 --> B3["Arithmetic transformations<br/>(C0/dose, C0*t, BET/Vp, BET*Dp)"]
        B1 & B2 & B3 --> B4["12 pre-assay inputs"]
    end

    subgraph Validation designs
        B4 --> C1{"Analyte"}
        C1 -->|"Cr(VI) (N = 120, 5 studies)"| C2["5-fold leave-one-study-out"]
        C1 -->|"Pb(II) (N = 318, 15 studies)"| C3["5-fold study-grouped<br/>(alphabetical modulo 5, 3 studies per fold)"]
        C1 -->|"Pb(II), HGB-U and HGB-M only"| C4["15-fold leave-one-study-out"]
    end

    subgraph Fitting
        C2 & C3 & C4 --> D1["Linear models with in-fold scaling<br/>(Ridge, ElasticNet)"]
        C2 & C3 & C4 --> D2["Tree ensembles<br/>(RF, ET)"]
        C2 & C3 & C4 --> D3["HistGradientBoosting<br/>(HGB-U; HGB-M with monotonic_cst on t)"]
        C2 & C3 & C4 --> D4["Training-median null baselines"]
    end

    subgraph Evaluation
        D1 & D2 & D3 & D4 --> E1["Truncation of predictions at zero"]
        E1 --> E2["Pooled out-of-fold metrics<br/>(MAE, RMSE, R2_OOD, MedAE)"]
        E2 --> E3["Table 1, Figures 1-4, QC checks"]
        E2 --> E4["Sensitivity analyses S2 (N = 398) and S3 (N = 387)"]
    end
```

---

## 2. Methodological principles

### 2.1 Study-aware validation
Records of one experimental series share every input except contact time. Records of one study share adsorbent, laboratory and protocol. A split that placed records of the same study in both training and test sets would let the model draw on the study's own series and would give optimistic error estimates.

To avoid this:
1. **Study-grouped folds:** all records of a study are kept in the same fold.
2. **In-fold preprocessing:** the scaler for the linear models is fitted on the training records of each fold only.
3. **Training-median null:** in every fold, each test record is predicted with the median $q_t$ of that fold's training records. Models are compared with this null under the same folds.

How much random row-wise splitting would inflate performance on these data was not measured.

### 2.2 Monotonic constraint on contact time
- **What HGB-M does:** it applies `monotonic_cst=[1, 0, ..., 0]`. This guarantees only that the fitted function does not decrease when contact time increases **and all other inputs are held fixed**.
- **Why trajectories are not guaranteed:** along a real batch experiment, the input $C_0 t$ also changes with time and is unconstrained. The predicted uptake curve of an experiment is therefore **not guaranteed** to be non-decreasing.
- **Status:** whether the fitted trajectories are in fact non-decreasing was not tested.
- **Effect on accuracy:** in the primary population, the constraint produced no appreciable change in accuracy (at most 0.075 mg/g in MAE; single seed, no significance test).
