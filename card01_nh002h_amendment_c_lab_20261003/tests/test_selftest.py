"""Full synthetic self-test reproduction. Each run is about 100 seconds.

Marked slow. Both runs are required.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import unittest

from tests.support import INPUT_SHA, LAB, OUTPUT_SHA, sha256_bytes


class SelftestReproductionTests(unittest.TestCase):
    def test_pinned_script_bytes(self):
        script = LAB / "pins" / "NH002H_AMENDMENT_B_national_miss.py"
        inp = LAB / "pins" / "SELFTEST_SYNTHETIC_input.json"
        expected = (LAB / "pins" / "SELFTEST_SYNTHETIC_output.json").read_bytes()
        proc = subprocess.run(
            [sys.executable, str(script), str(inp)],
            capture_output=True,
            check=True,
        )
        self.assertEqual(hashlib.sha256(proc.stdout).hexdigest(), OUTPUT_SHA)
        self.assertEqual(proc.stdout, expected)
        self.assertEqual(sha256_bytes(inp.read_bytes()), INPUT_SHA)

    def test_score_projection_matches_pinned_output(self):
        from card01_amc.score import ADDED_TOP_KEYS, project, score_document

        doc = json.loads((LAB / "pins" / "SELFTEST_SYNTHETIC_input.json").read_text())
        scored = score_document(doc)
        projected = json.dumps(project(scored), indent=1).encode()
        self.assertEqual(hashlib.sha256(projected).hexdigest(), OUTPUT_SHA)
        self.assertEqual(projected, (LAB / "pins" / "SELFTEST_SYNTHETIC_output.json").read_bytes())
        for key in ADDED_TOP_KEYS:
            self.assertIn(key, scored)
        self.assertNotIn("UNSTABLE_SPLIT", json.dumps(scored))
        for name in ("all_admitted", "split_KXHOUSERACE", "split_LEGACY"):
            block = scored[name]
            self.assertGreater(block["n"], 0)
            counts = block["n_boundary_resamples"]
            self.assertEqual(set(counts), {"0.0", "0.25", "0.5", "1.0"})
            for value in counts.values():
                self.assertIsInstance(value, int)
                self.assertGreaterEqual(value, 0)
                self.assertLessEqual(value, 10000)


if __name__ == "__main__":
    unittest.main()
