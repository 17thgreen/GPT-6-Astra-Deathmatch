"""Real-data tier. Skipped unless EXT2K1_REAL_DATA=1. Does not call score."""

import os
import unittest

_REAL = os.environ.get("EXT2K1_REAL_DATA") == "1"


def _receipt():
    from ext2k1.__main__ import _production_inputs
    from ext2k1.constants import PRODUCTION_PINS
    from ext2k1.pins_io import sweeps_module_sha256
    from ext2k1.report import build_receipt

    checked, builder_sha, markets, week_membership, rows = _production_inputs()
    return build_receipt(
        rows,
        markets,
        week_membership,
        PRODUCTION_PINS,
        builder_sha256=builder_sha,
        source_pins=checked,
        sweeps_module_sha256=sweeps_module_sha256(),
    )


@unittest.skipUnless(_REAL, "EXT2K1_REAL_DATA is unset; real tape stays off this run")
class R1Receipt(unittest.TestCase):
    def test_r1_counts_and_post_group(self):
        receipt, _document = _receipt()
        self.assertTrue(receipt["count_gate"]["pass"])
        counts = receipt["per_print_counts"]
        self.assertEqual(counts["NO_ge_1000"], 343)
        self.assertEqual(counts["NO_ge_5000"], 94)
        self.assertEqual(counts["YES_ge_1000"], 4500)
        self.assertEqual(counts["YES_ge_5000"], 608)
        cross = receipt["post_grouping_crosscheck"]
        self.assertEqual(cross["expected"], {"NO": 317, "YES": 4367})
        self.assertEqual(cross["NO"], 317)
        self.assertEqual(cross["YES"], 4367)
        self.assertIs(cross["gate"], False)


@unittest.skipUnless(_REAL, "EXT2K1_REAL_DATA is unset; real tape stays off this run")
class R2Structure(unittest.TestCase):
    def test_r2_structure_gate(self):
        receipt, _document = _receipt()
        self.assertTrue(receipt["structure_gate"]["pass"])
        self.assertTrue(receipt["structure_gate"]["quote_at_minus_asof_60_and_asof_mod_60_0"])
        self.assertTrue(receipt["structure_gate"]["trade_at_not_coarser_than_1s"])


@unittest.skipUnless(_REAL, "EXT2K1_REAL_DATA is unset; real tape stays off this run")
class R3Builder(unittest.TestCase):
    def test_r3_builder_sha(self):
        from ext2k1.constants import BUILDER_SHA256

        receipt, _document = _receipt()
        builder = receipt["b1_quote_builder"]
        self.assertEqual(builder["sha256"], BUILDER_SHA256)
        self.assertEqual(builder["expected_sha256"], BUILDER_SHA256)
        self.assertTrue(builder["match"])


if __name__ == "__main__":
    unittest.main()
