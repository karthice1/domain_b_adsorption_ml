"""
Test Suite: Artifact Generation Pipeline Verification.
Verifies that publication Figures 1-4 and Table 1 can be reproduced from frozen predictions.
"""

import os
import unittest
import tempfile
import subprocess
import sys
from pathlib import Path


class TestArtifactGeneration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.script_dir = Path(__file__).resolve().parent
        cls.pkg_root = cls.script_dir.parent
        cls.generator_script = cls.pkg_root / "figure_generation" / "generate_publication_figures_and_tables.py"

    def test_artifact_generation_pdf_only(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            cmd = [
                sys.executable,
                str(self.generator_script),
                "--output-dir", tmpdir,
                "--pdf-only"
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, f"Artifact generation failed:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}")

            # Verify generated files
            expected_files = [
                "FIGURE_1_PARITY_PLOTS.pdf",
                "FIGURE_2_RESIDUAL_DISTRIBUTIONS.pdf",
                "FIGURE_3_CORPUS_TOPOLOGY.pdf",
                "FIGURE_4_FEATURE_COVERAGE_POPULATION_C.pdf",
                "TABLE_1_FROZEN_MODEL_PERFORMANCE.pdf"
            ]
            for ef in expected_files:
                target = os.path.join(tmpdir, ef)
                self.assertTrue(os.path.exists(target), f"Missing expected artifact: {ef}")
                self.assertGreater(os.path.getsize(target), 0, f"Artifact is empty: {ef}")


if __name__ == '__main__':
    unittest.main()
