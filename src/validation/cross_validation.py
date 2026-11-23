"""
Validation Scheme and Grouped Cross-Validation Module.
Implements study-grouped and leave-one-study-out (LOSO) cross-validation splits.
"""

import numpy as np
import pandas as pd


def generate_cr_loso_folds(cr_df):
    """
    Generate 5-Fold Leave-One-Study-Out CV folds for Cr(VI) (N=120, 5 studies).
    Yields (fold_idx, held_out_study, train_indices, test_indices).
    """
    studies = sorted(cr_df['Literature_Reference'].unique().tolist())
    for fold, study in enumerate(studies):
        train_idx = cr_df.index[cr_df['Literature_Reference'] != study].tolist()
        test_idx = cr_df.index[cr_df['Literature_Reference'] == study].tolist()
        yield fold, study, train_idx, test_idx


def generate_pb_grouped_folds(pb_df):
    """
    Generate primary 5-Fold Study-Grouped CV folds for Pb(II) (N=318, 15 studies).
    Studies are sorted alphabetically and assigned modulo 5 (3 studies per fold).
    Yields (fold_idx, held_out_studies_list, train_indices, test_indices).
    """
    sorted_studies = sorted(pb_df['Literature_Reference'].unique().tolist())
    study_to_fold = {s: i % 5 for i, s in enumerate(sorted_studies)}
    fold_col = pb_df['Literature_Reference'].map(study_to_fold)

    for fold in range(5):
        train_idx = pb_df.index[fold_col != fold].tolist()
        test_idx = pb_df.index[fold_col == fold].tolist()
        held_out_studies = [s for s, f in study_to_fold.items() if f == fold]
        yield fold, held_out_studies, train_idx, test_idx


def generate_pb_loso_folds(pb_df):
    """
    Generate sensitivity 15-Fold Leave-One-Study-Out CV folds for Pb(II) (N=318, 15 studies).
    Yields (fold_idx, held_out_study, train_indices, test_indices).
    """
    sorted_studies = sorted(pb_df['Literature_Reference'].unique().tolist())
    for fold, study in enumerate(sorted_studies):
        train_idx = pb_df.index[pb_df['Literature_Reference'] != study].tolist()
        test_idx = pb_df.index[pb_df['Literature_Reference'] == study].tolist()
        yield fold, study, train_idx, test_idx
