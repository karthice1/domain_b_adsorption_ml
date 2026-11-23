"""
Test Suite: Environment Verification.
Verifies runtime environment, Python version, and dependency versions.
"""

import sys
import unittest


class TestEnvironment(unittest.TestCase):
    def test_python_version(self):
        # Assert Python >= 3.10
        self.assertGreaterEqual(sys.version_info.major, 3)
        self.assertGreaterEqual(sys.version_info.minor, 10)

    def test_required_packages_importable(self):
        import numpy
        import pandas
        import sklearn
        import matplotlib
        import scipy
        import PIL

        self.assertIsNotNone(numpy.__version__)
        self.assertIsNotNone(pandas.__version__)
        self.assertIsNotNone(sklearn.__version__)
        self.assertIsNotNone(matplotlib.__version__)
        self.assertIsNotNone(scipy.__version__)
        self.assertIsNotNone(PIL.__version__)


if __name__ == '__main__':
    unittest.main()
