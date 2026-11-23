"""
Cohort Filtering and Quality Verification Module.
Filters and partitions Domain B observations according to DR-040B protocol specifications.
"""

import pandas as pd


def get_category1_cohort(features_df, register_df):
    """
    Merge feature matrix with evidence register and isolate Category 1 kinetic cohort.
    
    Parameters
    ----------
    features_df : pd.DataFrame
        Remediation carbon feature matrix.
    register_df : pd.DataFrame
        Domain B record evidence register.
        
    Returns
    -------
    tuple of (pd.DataFrame, pd.DataFrame, pd.DataFrame)
        (cat1_df, cr_df, pb_df) containing combined (N=438), Cr(VI) (N=120), and Pb(II) (N=318).
    """
    df = features_df.merge(
        register_df[['Record_ID', 'Classification', 'Primary_Kinetic_Dataset_Inclusion', 'Literature_Reference', 'Heavy_Metal_Analyte']],
        on=['Record_ID', 'Literature_Reference', 'Heavy_Metal_Analyte']
    )

    cat1_df = df[df['Classification'] == '1_Directly_reported_kinetic_qt'].copy().reset_index(drop=True)
    if len(cat1_df) != 438:
        raise ValueError(f"Cohort validation error: Expected 438 Category 1 records, got {len(cat1_df)}")

    cr_df = cat1_df[cat1_df['Heavy_Metal_Analyte'] == 'Cr(VI)'].copy().reset_index(drop=True)
    if len(cr_df) != 120:
        raise ValueError(f"Cohort validation error: Expected 120 Cr(VI) records, got {len(cr_df)}")
    cr_studies = cr_df['Literature_Reference'].unique()
    if len(cr_studies) != 5:
        raise ValueError(f"Expected 5 distinct Cr(VI) studies, got {len(cr_studies)}")

    pb_df = cat1_df[cat1_df['Heavy_Metal_Analyte'] == 'Pb(II)'].copy().reset_index(drop=True)
    if len(pb_df) != 318:
        raise ValueError(f"Cohort validation error: Expected 318 Pb(II) records, got {len(pb_df)}")
    pb_studies = pb_df['Literature_Reference'].unique()
    if len(pb_studies) != 15:
        raise ValueError(f"Expected 15 distinct Pb(II) studies, got {len(pb_studies)}")

    return cat1_df, cr_df, pb_df
