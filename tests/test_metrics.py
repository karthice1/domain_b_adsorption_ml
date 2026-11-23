"""
Test Suite: Regression Metrics Verification.
Tests MAE, RMSE, R2, R2_OOD, and MedAE calculations against analytical ground truth.
"""

import unittest
import numpy as np
from src.metrics.metrics import compute_regression_metrics


class TestMetrics(unittest.TestCase):
    def test_perfect_prediction(self):
        y_true = np.array([10.0, 20.0, 30.0, 40.0])
        y_pred = np.array([10.0, 20.0, 30.0, 40.0])
        m = compute_regression_metrics(y_true, y_pred)

        self.assertAlmostEqual(m['MAE'], 0.0)
        self.assertAlmostEqual(m['RMSE'], 0.0)
        self.assertAlmostEqual(m['R2'], 1.0)
        self.assertAlmostEqual(m['MedAE'], 0.0)
        self.assertAlmostEqual(m['MaxAE'], 0.0)
        self.assertEqual(m['N'], 4)

    def test_known_error(self):
        y_true = np.array([10.0, 20.0, 30.0, 40.0])
        y_pred = np.array([12.0, 18.0, 32.0, 38.0])  # absolute errors: 2, 2, 2, 2
        m = compute_regression_metrics(y_true, y_pred)

        self.assertAlmostEqual(m['MAE'], 2.0)
        self.assertAlmostEqual(m['RMSE'], 2.0)
        self.assertAlmostEqual(m['MedAE'], 2.0)
        self.assertAlmostEqual(m['MaxAE'], 2.0)

    def test_out_of_sample_r2(self):
        y_true = np.array([10.0, 20.0, 30.0])
        y_pred = np.array([15.0, 25.0, 35.0])  # errors = 5, ss_res = 75
        y_train_mean = 0.0                      # ss_tot vs 0 = 100 + 400 + 900 = 1400
        m = compute_regression_metrics(y_true, y_pred, y_train_mean=y_train_mean)

        expected_r2 = 1.0 - (75.0 / 1400.0)
        self.assertAlmostEqual(m['R2'], expected_r2)


if __name__ == '__main__':
    unittest.main()
