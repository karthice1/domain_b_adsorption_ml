"""
Domain B Carbon Feature Engineering Pipeline.
Derives operational, structural, and interaction descriptors for dynamic kinetic adsorption
of heavy metals (Cr(VI) and Pb(II)) onto activated carbons from harmonized laboratory observations.
"""

import os
import sys
import argparse
from pathlib import Path
import numpy as np
import pandas as pd


def parse_args():
    parser = argparse.ArgumentParser(description="Derive Domain B Carbon Remediation Features.")
    parser.add_argument(
        "--input-file",
        type=str,
        default=None,
        help="Path to harmonized carbon dataset (PHASE2_REMEDIATION_CARBON_HARMONIZED.csv)"
    )
    parser.add_argument(
        "--output-file",
        type=str,
        default=None,
        help="Destination path for engineered feature matrix CSV"
    )
    return parser.parse_args()


def resolve_default_paths(args):
    script_dir = Path(__file__).resolve().parent
    pkg_root = script_dir.parents[1]
    repo_root = pkg_root.parent.parent

    input_file = args.input_file
    if input_file is None:
        candidate_paths = [
            repo_root / "phase2a" / "PHASE2_REMEDIATION_CARBON_HARMONIZED.csv",
            repo_root / "phase2b" / "versioned_dr026_corrections" / "inputs" / "PHASE2_REMEDIATION_CARBON_HARMONIZED.csv",
            pkg_root / "sample_data" / "mock_harmonized_carbon_sample.csv"
        ]
        for cp in candidate_paths:
            if cp.exists():
                input_file = str(cp)
                break

    output_file = args.output_file
    if output_file is None:
        output_file = str(pkg_root / "results" / "PHASE2B_REMEDIATION_CARBON_FEATURE_MATRIX.csv")

    return input_file, output_file


def derive_carbon_features(input_path, output_path):
    """
    Transform raw harmonized observation table into the complete 12-feature representation
    used by candidate machine-learning models.
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

    print(f"Loading harmonized observations from: {input_path}")
    carb = pd.read_csv(input_path)
    print(f"Loaded {len(carb)} rows and {len(carb.columns)} columns.")

    # Operational & Structural Transformations
    t_k = carb['Solution_Temperature_C'] + 273.15
    spec_loading = carb['Initial_Concentration_mg_L'] / carb['Adsorbent_Dose_g_L']
    mass_trans_prod = carb['Initial_Concentration_mg_L'] * carb['Contact_Time_min']
    inv_t = 1000.0 / t_k
    bet_over_vp = carb['BET_Surface_Area_m2_g'] / (carb['Total_Pore_Volume_cm3_g'] + 1e-6)
    dim_ph = carb['Solution_pH'] / 7.0
    pore_area_prod = carb['BET_Surface_Area_m2_g'] * carb['Pore_Diameter_nm']
    electroneg_ph = carb['Electronegativity_Pauling'] * carb['Solution_pH']

    # Ionic potential z / r_hyd
    # Cr(VI) (HCrO4- / CrO4 2-, effective r_hyd ~ 0.461 nm, charge ~ 2) vs Pb(II) (r_hyd ~ 0.401 nm, charge 2)
    ionic_potential = np.where(carb['Heavy_Metal_Analyte'].str.contains('Cr'), 2.0 / 0.461, 2.0 / 0.401)

    # Log10 features
    log10_c0 = np.log10(np.maximum(carb['Initial_Concentration_mg_L'], 1e-4))
    log10_dose = np.log10(np.maximum(carb['Adsorbent_Dose_g_L'], 1e-4))
    log10_time = np.log10(np.maximum(carb['Contact_Time_min'], 1e-4))
    log10_bet = np.log10(np.maximum(carb['BET_Surface_Area_m2_g'], 1.0))
    log10_pore_vol = np.log10(np.maximum(carb['Total_Pore_Volume_cm3_g'], 1e-4))

    carb_feat = pd.DataFrame({
        'Record_ID': carb['Record_ID'],
        'Original_Study_ID': carb['Original_Study_ID'],
        'Literature_Reference': carb['Literature_Reference'],
        'Publication_Year': carb['Publication_Year'],
        'Adsorbent_Name': carb['Adsorbent_Name'],
        'Adsorbent_Source_Material': carb['Adsorbent_Source_Material'],
        'Adsorbent_Code': carb['Adsorbent_Code'],
        'Heavy_Metal_Analyte': carb['Heavy_Metal_Analyte'],
        # Analyte Descriptors
        'Molar_Mass_g_mol': carb['Molar_Mass_g_mol'],
        'Hydrated_Radius_nm': carb['Hydrated_Radius_nm'],
        'Electronegativity_Pauling': carb['Electronegativity_Pauling'],
        'Van_der_Waals_Radius_nm': carb['Van_der_Waals_Radius_nm'],
        'Ionic_Potential_z_over_r': ionic_potential,
        # Operational Parameters
        'Initial_Concentration_mg_L': carb['Initial_Concentration_mg_L'],
        'Adsorbent_Dose_g_L': carb['Adsorbent_Dose_g_L'],
        'Solution_pH': carb['Solution_pH'],
        'Contact_Time_min': carb['Contact_Time_min'],
        'Solution_Temperature_C': carb['Solution_Temperature_C'],
        'Solution_Temperature_K': t_k,
        # Structural / Pore Properties
        'Activation_Temperature_C': carb['Activation_Temperature_C'],
        'BET_Surface_Area_m2_g': carb['BET_Surface_Area_m2_g'],
        'Pore_Diameter_nm': carb['Pore_Diameter_nm'],
        'Total_Pore_Volume_cm3_g': carb['Total_Pore_Volume_cm3_g'],
        'BET_over_Pore_Volume': bet_over_vp,
        'Pore_Area_Product': pore_area_prod,
        # Engineered Ratios & Interaction Terms
        'Specific_Loading_C0_over_dose': spec_loading,
        'Mass_Transfer_Product': mass_trans_prod,
        'Inverse_Temperature_1000_over_T': inv_t,
        'Dimensionless_pH_ratio': dim_ph,
        'Electronegativity_pH_product': electroneg_ph,
        # Log-transformed Features
        'log10_C0': log10_c0,
        'log10_dose': log10_dose,
        'log10_time': log10_time,
        'log10_BET': log10_bet,
        'log10_pore_vol': log10_pore_vol,
        # Contextual Flags & Target
        'Matrix_Class': carb['Matrix_Class'],
        'Thermodynamic_Regime': carb['Thermodynamic_Regime'],
        'Multi_Metal_Competition': carb['Multi_Metal_Competition'],
        'Kinetic_Capacity_qt_mg_g': carb['Kinetic_Capacity_qt_mg_g']
    })

    carb_feat.to_csv(output_path, index=False)
    print(f"Successfully derived feature matrix: {carb_feat.shape[0]} rows, {carb_feat.shape[1]} columns -> {output_path}")
    return carb_feat


if __name__ == '__main__':
    args = parse_args()
    inp, outp = resolve_default_paths(args)
    derive_carbon_features(inp, outp)
