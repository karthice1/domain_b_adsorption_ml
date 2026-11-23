# Domain B Adsorption ML: Software Limitations and Boundary Conditions

This document defines the operational boundaries, physical applicability domains, and scientific limitations of the Domain B machine-learning framework.

---

## 1. Domain Applicability and Operating Envelope

The empirical models packaged herein were trained and validated on laboratory batch adsorption experiments. Operating outside the following bounds represents extreme extrapolation:

| Parameter | Minimum Valid Bound | Maximum Valid Bound | Boundary Commentary |
|---|---|---|---|
| **Solution pH** | 2.0 | 8.0 | Beyond pH > 8.0, Cr(VI) and Pb(II) undergo hydroxide precipitation ($\text{Pb(OH)}_2 \downarrow$), shifting the removal mechanism from surface adsorption to chemical precipitation. |
| **Operating Temperature** | 15.0 °C (288.15 K) | 45.0 °C (318.15 K) | Ambient and moderate industrial effluent temperatures. Superheated or refrigerated regimes are unvalidated. |
| **Initial Concentration ($C_0$)** | 10.0 mg/L | 500.0 mg/L | Dilute to high-strength laboratory synthetic solutions. Trace-level (sub-ppb) adsorption dynamics are uncharacterized. |
| **Adsorbent Dosage ($D$)** | 0.5 g/L | 10.0 g/L | Realistic operational slurry densities. |
| **Contact Time ($t$)** | 5.0 min | 1440.0 min (24 h) | Dynamic kinetic phase up to equilibrium plateau. Not calibrated for multi-day batch contact. |
| **BET Surface Area ($S_{\text{BET}}$)** | 400.0 $\text{m}^2/\text{g}$ | 1800.0 $\text{m}^2/\text{g}$ | Typical physical activation and chemical activation (KOH, $\text{H}_3\text{PO}_4$) ranges for porous carbons. |

---

## 2. Chemical and Hydrodynamic Limitations

1. **Synthetic Single-Solute Solutions:** The Category 1 dynamic kinetic dataset comprises single-metal aqueous solutions ($\text{Cr(VI)}$ alone or $\text{Pb(II)}$ alone). Competitive multi-metal adsorption, co-solute interference (e.g., competing organic natural organic matter [NOM], EDTA chelators, or high-salinity sulfate/chloride matrices) are not explicitly accounted for.
2. **Batch Agitation vs Fixed-Bed Columns:** Models predict dynamic capacity ($q_t$) under well-mixed batch slurry conditions. They do not simulate continuous-flow fixed-bed breakthrough curves, mass transfer zone (MTZ) progression, or axial dispersion.
3. **Equilibrium vs Kinetic Estimands:** This package models dynamic kinetic uptake ($q_t$) as a function of contact time ($t$). Static equilibrium isotherms ($q_e$ vs $C_e$) without time resolution are governed by companion benchmark protocols (Category 2).

---

## 3. Statistical vs Causal Interpretation

- **Feature Importances Represent Statistical Associations:** The tree-based Mean Decrease in Impurity (MDI) scores and regression coefficients reflect predictive predictive correlations present across published literature corpora. They must **not** be construed as formal causal mechanisms or mechanistic reaction orders.
- **Corpus Imbalance:** As documented in the manuscript, the Chromium(VI) literature corpus exhibits significant study imbalance (Labied et al. 2018 accounts for 60.83% of Cr records). While Leave-One-Study-Out CV penalizes models that overfit to dominant studies, predictive variance remains higher for Cr(VI) than for the more evenly balanced Pb(II) cohort (15 studies).
