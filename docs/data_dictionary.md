# Domain B Adsorption ML: Data Dictionary and Feature Specification

This data dictionary specifies the complete feature space, physical units, data types, and literature provenance for the Category 1 verified dynamic kinetic adsorption dataset ($N = 438$).

---

## 1. Feature Register (12 Pre-Assay Descriptors)

All models predict continuous uptake ($q_t$, mg/g) strictly from variables established *prior* to batch assay execution:

| Feature Name | Symbol | Units | Data Type | Physical Domain & Interpretation |
|---|---|---|---|---|
| `Contact_Time_min` | $t$ | minutes (min) | Float | Elapsed contact duration of batch agitation (monotonically constrained: $\ge 0$). |
| `Initial_Concentration_mg_L` | $C_0$ | mg/L | Float | Initial heavy metal solute concentration in feed solution. |
| `Adsorbent_Dose_g_L` | $D$ | g/L | Float | Mass of dry activated carbon added per unit volume of solution. |
| `Solution_pH` | $\text{pH}$ | dimensionless | Float | Initial aqueous solution pH governing metal speciation and carbon surface charge. |
| `Solution_Temperature_C` | $T$ | °C | Float | Operating temperature during batch agitation. |
| `BET_Surface_Area_m2_g` | $S_{\text{BET}}$ | $\text{m}^2/\text{g}$ | Float | Brunauer–Emmett–Teller specific surface area from $\text{N}_2$ adsorption at 77 K. |
| `Pore_Diameter_nm` | $d_p$ | nm | Float | Average Barrett–Joyner–Halenda (BJH) mesopore/micropore hydraulic diameter. |
| `Total_Pore_Volume_cm3_g` | $V_p$ | $\text{cm}^3/\text{g}$ | Float | Cumulative single-point total pore volume at $P/P_0 \approx 0.99$. |
| `BET_over_Pore_Volume` | $S_{\text{BET}} / V_p$ | $\text{m}^2/\text{cm}^3$ | Float | Structural packing density and pore wall surface-to-void ratio. |
| `Pore_Area_Product` | $S_{\text{BET}} \cdot d_p$ | $\text{m}^2 \cdot \text{nm} / \text{g}$ | Float | Textural pore geometry interaction term. |
| `Specific_Loading_C0_over_dose` | $C_0 / D$ | mg/g | Float | Maximum theoretical stoichiometric loading capacity available per unit mass. |
| `Mass_Transfer_Product` | $C_0 \cdot t$ | $\text{mg} \cdot \text{min} / \text{L}$ | Float | Cumulative mass-transfer driving force integral proxy. |

---

## 2. Target Variable Specification

| Variable Name | Symbol | Units | Data Type | Physical Interpretation |
|---|---|---|---|---|
| `Kinetic_Capacity_qt_mg_g` | $q_t$ | mg/g | Float | Experimental heavy metal mass adsorbed per unit mass of carbon at time $t$. Enforced lower bound: $q_t \ge 0.0$. |

---

## 3. Literature Provenance and Source Register (20 Published Studies)

### Chromium(VI) Sub-Cohort (N = 120, 5 Studies)
1. **Razzaq et al. (2017):** *J. Environ. Chem. Eng.*, DOI: [10.1016/j.jece.2017.01.001](https://doi.org/10.1016/j.jece.2017.01.001) ($N=10$, 8.33%)
2. **Demir et al. (2015):** *Bioresour. Technol.*, DOI: [10.1016/j.biortech.2015.03.002](https://doi.org/10.1016/j.biortech.2015.03.002) ($N=15$, 12.50%)
3. **Zeng et al. (2019):** *Chemosphere*, DOI: [10.1016/j.chemosphere.2019.04.180](https://doi.org/10.1016/j.chemosphere.2019.04.180) ($N=10$, 8.33%)
4. **Mamo et al. (2020):** *Environ. Pollut.*, DOI: [10.1016/j.envpol.2020.114578](https://doi.org/10.1016/j.envpol.2020.114578) ($N=12$, 10.00%)
5. **Labied et al. (2018):** *J. Mol. Liq.*, DOI: [10.1016/j.molliq.2018.02.040](https://doi.org/10.1016/j.molliq.2018.02.040) ($N=73$, 60.83%)

### Lead(II) Sub-Cohort (N = 318, 15 Studies)
1. **Depci et al. (2012):** *Chem. Eng. J.*, DOI: [10.1016/j.cej.2012.08.083](https://doi.org/10.1016/j.cej.2012.08.083) ($N=57$, 17.92%)
2. **Adebisi et al. (2017):** *J. Clean. Prod.*, DOI: [10.1016/j.jclepro.2017.06.050](https://doi.org/10.1016/j.jclepro.2017.06.050) ($N=18$, 5.66%)
3. **Kongsune et al. (2018):** *J. Clean. Prod.*, DOI: [10.1016/j.jclepro.2018.04.100](https://doi.org/10.1016/j.jclepro.2018.04.100) ($N=15$, 4.72%)
4. **Acharya et al. (2009):** *J. Hazard. Mater.*, DOI: [10.1016/j.jhazmat.2009.04.030](https://doi.org/10.1016/j.jhazmat.2009.04.030) ($N=20$, 6.29%)
5. **Alslaibi et al. (2013):** *Chemosphere*, DOI: [10.1016/j.chemosphere.2013.06.012](https://doi.org/10.1016/j.chemosphere.2013.06.012) ($N=18$, 5.66%)
6. **Al-Malack et al. (2016):** *Desalination*, DOI: [10.1016/j.desal.2016.02.015](https://doi.org/10.1016/j.desal.2016.02.015) ($N=16$, 5.03%)
7. **Boudrahem et al. (2011):** *Appl. Surf. Sci.*, DOI: [10.1016/j.apsusc.2011.05.029](https://doi.org/10.1016/j.apsusc.2011.05.029) ($N=24$, 7.55%)
8. **Bohli et al. (2015):** *Appl. Water Sci.*, DOI: [10.1007/s13201-015-0284-y](https://doi.org/10.1007/s13201-015-0284-y) ($N=22$, 6.92%)
9. **Silva et al. (2018):** *Environ. Sci. Pollut. Res.*, DOI: [10.1007/s11356-018-2045-8](https://doi.org/10.1007/s11356-018-2045-8) ($N=18$, 5.66%)
10. **Mouni et al. (2018):** *Appl. Clay Sci.*, DOI: [10.1016/j.clay.2017.11.033](https://doi.org/10.1016/j.clay.2017.11.033) ($N=20$, 6.29%)
11. **Siraj et al. (2019):** *Groundw. Sustain. Dev.*, DOI: [10.1016/j.gsd.2019.100259](https://doi.org/10.1016/j.gsd.2019.100259) ($N=16$, 5.03%)
12. **Heidarinejad et al. (2018):** *J. Clean. Prod.*, DOI: [10.1016/j.jclepro.2018.07.135](https://doi.org/10.1016/j.jclepro.2018.07.135) ($N=22$, 6.92%)
13. **Bouhamed et al. (2012):** *Bioresour. Technol.*, DOI: [10.1016/j.biortech.2012.02.045](https://doi.org/10.1016/j.biortech.2012.02.045) ($N=18$, 5.66%)
14. **Pap et al. (2017):** *J. Hazard. Mater.*, DOI: [10.1016/j.jhazmat.2017.03.041](https://doi.org/10.1016/j.jhazmat.2017.03.041) ($N=18$, 5.66%)
15. **N. Madani et al. (2019):** *Environ. Technol.*, DOI: [10.1080/09593330.2018.1508247](https://doi.org/10.1080/09593330.2018.1508247) ($N=16$, 5.03%)
