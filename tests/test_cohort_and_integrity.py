"""
Test Suite: Cohort and Scientific Integrity Verification.
Asserts that canonical Category 1 populations match Cr N=120, Pb N=318, Total N=438,
and that out-of-fold prediction values are non-negative.
"""

import os
import unittest
from pathlib import Path
import pandas as pd


class TestCohortAndIntegrity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.script_dir = Path(__file__).resolve().parent
        cls.pkg_root = cls.script_dir.parent
        cls.repo_root = cls.pkg_root.parent.parent

        cls.cr_path = cls.repo_root / "phase3" / "model_development" / "domain_B_carbon" / "results" / "CARB_CR_CANDIDATE_OOF_PREDICTIONS.csv"
        cls.pb_path = cls.repo_root / "phase3" / "model_development" / "domain_B_carbon" / "results" / "CARB_PB_CANDIDATE_OOF_PREDICTIONS.csv"

    def test_cr_cohort_size_and_studies(self):
        if not self.cr_path.exists():
            self.skipTest(f"Missing {self.cr_path}")
        df = pd.read_csv(self.cr_path)
        self.assertEqual(len(df), 120, "Cr(VI) cohort must have exactly 120 records")
        studies = df['Literature_Reference'].unique()
        self.assertEqual(len(studies), 5, "Cr(VI) cohort must span exactly 5 studies")

    def test_pb_cohort_size_and_studies(self):
        if not self.pb_path.exists():
            self.skipTest(f"Missing {self.pb_path}")
        df = pd.read_csv(self.pb_path)
        self.assertEqual(len(df), 318, "Pb(II) cohort must have exactly 318 records")
        studies = df['Literature_Reference'].unique()
        self.assertEqual(len(studies), 15, "Pb(II) cohort must span exactly 15 studies")

    def test_non_negativity_cr(self):
        if not self.cr_path.exists():
            self.skipTest(f"Missing {self.cr_path}")
        df = pd.read_csv(self.cr_path)
        pred_cols = [c for c in df.columns if c.startswith('Pred_Cr')]
        for c in pred_cols:
            self.assertTrue((df[c] >= 0.0).all(), f"Found negative predictions in Cr column {c}")

    def test_non_negativity_pb(self):
        if not self.pb_path.exists():
            self.skipTest(f"Missing {self.pb_path}")
        df = pd.read_csv(self.pb_path)
        pred_cols = [c for c in df.columns if c.startswith('Pred_Pb')]
        for c in pred_cols:
            self.assertTrue((df[c] >= 0.0).all(), f"Found negative predictions in Pb column {c}")


if __name__ == '__main__':
    unittest.main()
