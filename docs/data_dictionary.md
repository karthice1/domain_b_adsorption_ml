# Domain B Adsorption ML: Data Dictionary and Source Register

This document specifies the 12 model inputs, the target, their units and observed ranges, and the source studies of the 438 Category 1 records.

**Category 1 records:**
- The 438 records were classified as time-resolved because each belongs to a multi-point contact-time sequence in the compiled data. The classification was made on the compiled data and was **not** confirmed against each original publication.
- All values were taken from the dataset published with Lamsiah et al. (2026) (see Section 3). None was re-extracted or corrected.
- The records themselves are **not** included in this package.

---

## 1. Input register (12 pre-assay inputs, in model column order)

None of the inputs is measured after the assay. The equilibrium or residual concentration, percentage removal and equilibrium capacity are excluded. Ranges are the observed marginal ranges of the 438 records. They are **not** an applicability domain: combinations of inputs inside every marginal range may still be far from any training record. No joint applicability analysis was performed.

| # | Column name | Symbol and definition | Unit | Range (N = 438) |
|---:|---|---|---|---|
| 0 | `Contact_Time_min` | Contact time $t$ at which $q_t$ is predicted | min | 2.5–360 |
| 1 | `Initial_Concentration_mg_L` | Initial concentration $C_0$ | mg/L | 10–207.2 |
| 2 | `Adsorbent_Dose_g_L` | Adsorbent dose $D$ | g/L | 0.5–6.0 |
| 3 | `Solution_pH` | Solution pH | — | 2.0–8.0 |
| 4 | `Solution_Temperature_C` | Solution temperature $T$ | °C | 20–40 |
| 5 | `BET_Surface_Area_m2_g` | BET surface area $S_{\mathrm{BET}}$, as reported in the compilation | m²/g | 9.81–1824 |
| 6 | `Pore_Diameter_nm` | Mean pore diameter $D_p$, as reported in the compilation | nm | 0.36–5.16 |
| 7 | `Total_Pore_Volume_cm3_g` | Total pore volume $V_p$, as reported in the compilation | cm³/g | 0.01–1.45 |
| 8 | `BET_over_Pore_Volume` | $S_{\mathrm{BET}}/(V_p+10^{-6})$; the $10^{-6}$ guards against division by zero | m²/cm³ | 775.9–3500.0 |
| 9 | `Pore_Area_Product` | $S_{\mathrm{BET}}\,D_p$ | m²·nm/g | 43.2–5805 |
| 10 | `Specific_Loading_C0_over_dose` | Specific loading $C_0/D$ | mg/g | 5–200 |
| 11 | `Mass_Transfer_Product` | Concentration–time product $C_0\,t$ | mg·min/L | 50–72,000 |

**Notes on the inputs:**
- Inputs 8–11 are arithmetic transformations of inputs 0–7. They are not separately measured quantities.
- The measurement methods behind inputs 5–7 (for example the isotherm model or pressure point used) are not recorded in the compiled data and are not assumed here.
- In the monotonic model variant HGB-M, input 0 carries a non-decreasing constraint, which holds only when all other inputs are fixed. Input 11 also changes with time and is unconstrained, so predicted uptake curves are not guaranteed to be non-decreasing (see `software_limitations.md`).

**Ranges by cohort (from the manuscript):**

| Input | Cr(VI) | Pb(II) |
|---|---|---|
| pH | 2–8 | 4–7 |
| $T$ | 20–40 °C | 20–30 °C |
| $S_{\mathrm{BET}}$ | 369.7–1345.26 m²/g | 9.81–1824 m²/g |

---

## 2. Target

| Column name | Symbol | Unit | Range (N = 438) | Notes |
|---|---|---|---|---|
| `Kinetic_Capacity_qt_mg_g` | $q_t$ | mg/g | 1.03–85.02 | Adsorbed amount at contact time $t$, as compiled |

The compiling study labels this response "adsorption capacity" and describes it as equilibrium uptake. The time-resolved interpretation rests on the Category 1 classification above.

The software truncates **predictions** at zero ($\hat q \leftarrow \max(\hat q, 0)$). Observed target values are not modified.

---

## 3. Source register

**Compilation (source of all values):** S. Lamsiah, M. Benhadj, I. Alouiz, M. Bouhadda, M.Y. Amarouch, D. Mazouzi, M. Sennoune, Prediction of heavy metal adsorption by activated carbon using machine learning, *Artificial Intelligence Chemistry* 4 (2026) 100117. https://doi.org/10.1016/j.aichem.2026.100117

**Original studies.** The 20 original studies are listed below, as cited in the manuscript.

How the details were checked:
- **DOIs:** each DOI was confirmed on Crossref (first author, year, journal) on 2026-11-23.
- **Record counts:** counted from the stored out-of-fold prediction files and equal to manuscript Table 2.1.
- **Record label:** the study identifier used in the data files.

What the source status means:
- **Partially verified:** the article was inspected in full, but not every compiled value was re-extracted from it.
- **Unresolved:** only the bibliographic identity of the source was verified. Whether its values were reported, digitised or calculated is not known.

### Chromium(VI) (N = 120, 5 studies)

| Ref. in manuscript | Study | Record label in data | Records | Verified DOI | Source status |
|---|---|---|---:|---|---|
| [5] | R. Labied, O. Benturki, A.Y.E. Hamitouche, A. Donnot, Adsorption of hexavalent chromium by activated carbon obtained from a waste lignocellulosic material (*Ziziphus jujuba* cores): Kinetic, equilibrium, and thermodynamic study, Adsorption Science & Technology 36 (2018) 1066–1099. | `Labied et al` | 73 | [10.1177/0263617417750739](https://doi.org/10.1177/0263617417750739) | Partially verified (article inspected in full) |
| [6] | Z. Razzaq, M. Hamayun, S. Murtaza, S. Kausar, A.A. Altaf, R.U. Khan, T. Javaid, Removal of As(V) and Cr(VI) with low-cost novel virgin and iron-impregnated banana peduncle-activated carbons, ACS Omega 8 (2023) 2098–2111. | `Razzaq et al` | 20 | [10.1021/acsomega.2c05957](https://doi.org/10.1021/acsomega.2c05957) | Partially verified (article inspected in full) |
| [7] | D.W. Mamo, T.G. Asere, T.H. Habtemariam, Adsorptive removal of Cr(VI) from aqueous solution using activated carbon of Enset root (*Ensete ventricosum*), Desalination and Water Treatment 321 (2025) 101053. | `Mamo et al` | 10 | [10.1016/j.dwt.2025.101053](https://doi.org/10.1016/j.dwt.2025.101053) | Unresolved (bibliographic identity only) |
| [8] | I. Demir, A. Caglar, D. Yildiz, The high-efficiency Cr(VI) adsorption using poplar wood based activated carbon, International Journal of Ecosystems and Ecology Science (IJEES) 13 (2023) 63–74. | `Demir et al` | 9 | [10.31407/ijees13.310](https://doi.org/10.31407/ijees13.310) | Unresolved (bibliographic identity only) |
| [9] | G. Zeng, C. Hong, Y. Zhang, H. You, W. Shi, M. Du, N. Ai, B. Chen, Adsorptive removal of Cr(VI) by *Sargassum horneri*-based activated carbon coated with chitosan, Water, Air, & Soil Pollution 231 (2020) 77. | `Zeng et al` | 8 | [10.1007/s11270-020-4440-2](https://doi.org/10.1007/s11270-020-4440-2) | Unresolved (bibliographic identity only) |

### Lead(II) (N = 318, 15 studies)

| Ref. in manuscript | Study | Record label in data | Records | Verified DOI | Source status |
|---|---|---|---:|---|---|
| [10] | T. Depci, A.R. Kul, Y. Önal, Competitive adsorption of lead and zinc from aqueous solution on activated carbon prepared from Van apple pulp: Study in single- and multi-solute systems, Chemical Engineering Journal 200–202 (2012) 224–236. | `Depci et al` | 57 | [10.1016/j.cej.2012.06.077](https://doi.org/10.1016/j.cej.2012.06.077) | Partially verified (article inspected in full) |
| [11] | F. Boudrahem, F. Aissani-Benissad, H. Aït-Amar, Batch sorption dynamics and equilibrium for the removal of lead ions from aqueous phase using activated carbon developed from coffee residue activated with zinc chloride, Journal of Environmental Management 90 (2009) 3031–3039. | `Boudrahem et al` | 48 | [10.1016/j.jenvman.2009.04.005](https://doi.org/10.1016/j.jenvman.2009.04.005) | Unresolved (bibliographic identity only) |
| [12] | J. Acharya, J.N. Sahu, C.R. Mohanty, B.C. Meikap, Removal of lead(II) from wastewater by activated carbon developed from Tamarind wood by zinc chloride activation, Chemical Engineering Journal 149 (2009) 249–262. | `Acharya et al` | 43 | [10.1016/j.cej.2008.10.029](https://doi.org/10.1016/j.cej.2008.10.029) | Unresolved (bibliographic identity only) |
| [13] | L. Mouni, L. Belkhiri, F. Zouggaghe, M. Tafer, Removal of Pb(II) from aqueous solution by adsorption using activated carbon developed from Apricot stone: equilibrium and kinetic, Desalination and Water Treatment 52 (2014) 6412–6419. | `Mouni et al` | 39 | [10.1080/19443994.2013.812992](https://doi.org/10.1080/19443994.2013.812992) | Partially verified (article inspected in full) |
| [14] | F. Bouhamed, Z. Elouear, J. Bouzid, B. Ouddane, Batch sorption of Pb(II) ions from aqueous solutions using activated carbon prepared from date stones: equilibrium, kinetic, and thermodynamic studies, Desalination and Water Treatment 52 (2014) 2261–2271. | `Bouhamed et al` | 32 | [10.1080/19443994.2013.806222](https://doi.org/10.1080/19443994.2013.806222) | Unresolved (bibliographic identity only) |
| [15] | T. Bohli, Comparative study of bivalent cationic metals adsorption Pb(II), Cd(II), Ni(II) and Cu(II) on olive stones chemically activated carbon, Journal of Chemical Engineering & Process Technology 4 (2013). | `Bohli et al` | 18 | [10.4172/2157-7048.1000158](https://doi.org/10.4172/2157-7048.1000158) | Unresolved (bibliographic identity only) |
| [16] | K. Siraj, J.S. Aballa, M. Danish, T. Ahmad, M.M. Khan, S. Majeed, B. Adane, The effect of microwave and muffle furnace-assisted heating on the surface characteristics of teff husk activated carbons: Thermodynamic, isotherm, and kinetics study of Pb removal, Diamond and Related Materials 143 (2024) 110912. | `Siraj et al` | 18 | [10.1016/j.diamond.2024.110912](https://doi.org/10.1016/j.diamond.2024.110912) | Unresolved (bibliographic identity only) |
| [17] | G.A. Adebisi, Z.Z. Chowdhury, P.A. Alaba, Equilibrium, kinetic, and thermodynamic studies of lead ion and zinc ion adsorption from aqueous solution onto activated carbon prepared from palm oil mill effluent, Journal of Cleaner Production 148 (2017) 958–968. | `Adebisi et al` | 14 | [10.1016/j.jclepro.2017.02.047](https://doi.org/10.1016/j.jclepro.2017.02.047) | Unresolved (bibliographic identity only) |
| [18] | S. Pap, T.Š. Knudsen, J. Radonić, S. Maletić, S.M. Igić, M.T. Sekulić, Utilization of fruit processing industry waste as green activated carbon for the treatment of heavy metals and chlorophenols contaminated water, Journal of Cleaner Production 162 (2017) 958–972. | `Pap et al` | 10 | [10.1016/j.jclepro.2017.06.083](https://doi.org/10.1016/j.jclepro.2017.06.083) | Unresolved (bibliographic identity only) |
| [19] | M.H. Al-Malack, A.A. Basaleh, Adsorption of heavy metals using activated carbon produced from municipal organic solid waste, Desalination and Water Treatment 57 (2016) 24519–24531. | `Al-Malack et al` | 9 | [10.1080/19443994.2016.1144536](https://doi.org/10.1080/19443994.2016.1144536) | Partially verified (article inspected in full) |
| [20] | N. Madani, N. Bouchenafa-Saib, O. Mohammedi, F.J. Varela-Gandía, D. Cazorla-Amorós, B. Hamada, O. Cherifi, Removal of heavy metal ions by adsorption onto activated carbon prepared from *Stipa tenacissima* leaves, Desalination and Water Treatment 64 (2017) 179–188. | `N. Madani et al` | 9 | [10.5004/dwt.2017.20254](https://doi.org/10.5004/dwt.2017.20254) | Unresolved (bibliographic identity only) |
| [21] | T.M. Alslaibi, I. Abustan, M.A. Ahmad, A.A. Foul, Kinetics and equilibrium adsorption of iron (II), lead (II), and copper (II) onto activated carbon prepared from olive stone waste, Desalination and Water Treatment 52 (2014) 7887–7897. | `Alslaibi et al` | 7 | [10.1080/19443994.2013.833875](https://doi.org/10.1080/19443994.2013.833875) | Unresolved (bibliographic identity only) |
| [22] | Z. Heidarinejad, O. Rahmanian, M. Heidari, Production of KOH-activated carbon from date press cake: effect of the activating agent on its properties and Pb(II) adsorption potential, Desalination and Water Treatment 165 (2019) 232–243. | `Heidarinejad et al` | 7 | [10.5004/dwt.2019.24501](https://doi.org/10.5004/dwt.2019.24501) | Unresolved (bibliographic identity only) |
| [23] | P. Kongsune, S. Rattanapan, R. Chanajaree, The removal of Pb²⁺ from aqueous solution using mangosteen peel activated carbon: Isotherm, kinetic, thermodynamic and binding energy calculation, Groundwater for Sustainable Development 12 (2021) 100524. | `Kongsune et al` | 4 | [10.1016/j.gsd.2020.100524](https://doi.org/10.1016/j.gsd.2020.100524) | Unresolved (bibliographic identity only) |
| [24] | M.C. Silva, L.H.S. Crespo, A.L. Cazetta, T.L. Silva, L. Spessato, V.C. Almeida, Activated carbon fibers of high surface area from corn husk: Mono and multicomponent adsorption studies of Pb²⁺ and Cu²⁺ ions from aqueous solution, Journal of Molecular Liquids 405 (2024) 124919. | `Silva et al` | 3 | [10.1016/j.molliq.2024.124919](https://doi.org/10.1016/j.molliq.2024.124919) | Unresolved (bibliographic identity only) |

**Correction note.** Version 1.0.0 of this file listed incorrect DOIs, years, journals and record counts for these studies. They are corrected here; see `RELEASE_AUDIT_V1_0_1.md`.
