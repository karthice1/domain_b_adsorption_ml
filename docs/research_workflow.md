# Domain B Adsorption ML: Research Workflow and Methodology

This document outlines the end-to-end computational and empirical workflow governing the Domain B machine-learning evaluation for dynamic heavy-metal adsorption onto activated carbons.

---

## 1. End-to-End Workflow Architecture

```mermaid
flowchart TD
    subgraph Data Harmonization & Screening
        A1["Raw Secondary Literature<br/>(20 Published Studies)"] --> A2["Harmonization & Schema Unification<br/>(PHASE2_REMEDIATION_CARBON_HARMONIZED.csv)"]
        A2 --> A3["DR-040B Evidence Auditing<br/>(DR040B_DOMAIN_B_RECORD_EVIDENCE_REGISTER.csv)"]
        A3 --> A4["Category 1 Filtering<br/>(Verified Dynamic Kinetic Records: N=438)"]
    end

    subgraph Feature Engineering
        A4 --> B1["Pre-Assay Operational Descriptors<br/>(C0, Dose, pH, Temp, Time)"]
        A4 --> B2["Textural & Structural Descriptors<br/>(BET Area, Pore Vol, Pore Diam)"]
        A4 --> B3["Interaction Terms & Mass Transfer<br/>(C0/Dose, C0*Time, BET/Vp, Pore Area Prod)"]
        B1 & B2 & B3 --> B4["Canonical 12-Feature Representation"]
    end

    subgraph Grouped Cross-Validation
        B4 --> C1{"Analyte Cohort Partition"}
        C1 -->|"Cr(VI) (N=120, 5 Studies)"| C2["5-Fold Leave-One-Study-Out CV<br/>(LOSO-CV)"]
        C1 -->|"Pb(II) (N=318, 15 Studies)"| C3["Primary 5-Fold Study-Grouped CV<br/>(3 Studies/Fold)"]
        C1 -->|"Pb(II) Sensitivity"| C4["15-Fold Leave-One-Study-Out CV<br/>(Full LOSO-CV)"]
    end

    subgraph Model Training & In-Fold Preprocessing
        C2 & C3 & C4 --> D1["In-Fold Standard Scaling<br/>(Linear Models: Ridge, ElasticNet)"]
        C2 & C3 & C4 --> D2["Tree Ensemble Training<br/>(Random Forest, Extra Trees)"]
        C2 & C3 & C4 --> D3["Constrained Gradient Boosting<br/>(HistGradientBoosting with monotonic_cst=+1)"]
        C2 & C3 & C4 --> D4["In-Training Study-Median Null Baselines<br/>(CARB_BASE_01)"]
    end

    subgraph Out-of-Fold Evaluation & Diagnostics
        D1 & D2 & D3 & D4 --> E1["Physical Non-Negativity Clipping<br/>(qt >= 0.0 mg/g)"]
        E1 --> E2["Pooled Metrics & Fold-Wise Statistics<br/>(MAE, RMSE, R2_OOD, MedAE)"]
        E2 --> E3["Publication Artifacts & Verification<br/>(Table 1, Figures 1-4, QC Assertions)"]
    end
```

---

## 2. Key Methodological Principles

### 2.1 Anti-Leakage Guarantee
In batch adsorption studies, dynamic kinetic data points from the same experimental run or literature study share identical adsorbent preparation methods, precursor chemistry, activation temperatures, and laboratory instrumentation. Standard random k-fold cross-validation results in severe data leakage, inflating test scores artificially because samples from the same isotherm or trajectory appear in both training and test sets.

To eliminate this vulnerability:
1. **Study-Grouped CV:** All data points from any individual published study are strictly confined to either the training split or the test split—never both.
2. **In-Fold Preprocessing:** Standard scalers and transformers calculate sample statistics strictly on the in-fold training subset.
3. **Out-of-Distribution Null Benchmark:** Every candidate model is evaluated against the held-out study-median baseline (CARB_BASE_01) to verify whether the model outperforms the simple empirical median of known historical studies.

### 2.2 Physical Constraint Enforcement
Under constant batch operating conditions with non-desorbing activated carbons, cumulative metal uptake ($q_t$, mg/g) is monotonically non-decreasing over contact time:
$$\frac{\partial q_t}{\partial t} \ge 0$$

Unconstrained non-linear estimators (e.g. standard gradient boosting or deep neural networks) can produce non-physical transient dips in predicted uptake over time. We enforce monotonicity directly during tree construction using histogram-based gradient boosting (`monotonic_cst=[+1, 0, ..., 0]`), guaranteeing thermodynamically sound adsorption curves.
