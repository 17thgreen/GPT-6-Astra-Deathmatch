import unittest

import support  # noqa: F401
from constants import OPENING_PORTIONS, PAIRED_UNITS
from orchestrator import measure


class T07Uch(unittest.TestCase):
    def test_identity_inventory_and_flat_window(self):
        measurement = measure(write=True)
        lots = measurement["lots"]
        self.assertLessEqual(abs(lots["uch_fifo"] - lots["uch_integral"]), 1e-6)
        self.assertAlmostEqual(lots["opening_contracts"], PAIRED_UNITS, delta=0.01)
        self.assertAlmostEqual(lots["closing_contracts"], PAIRED_UNITS, delta=0.01)
        self.assertAlmostEqual(lots["opening_contracts"], lots["closing_contracts"], delta=1e-6)
        self.assertEqual(len(lots["portions"]), OPENING_PORTIONS)
        self.assertEqual(len(lots["portions"]), 6161)
        self.assertTrue(all(portion["kind"] == "maker" for portion in lots["portions"]))
        self.assertEqual(lots["open_at_window_end_contracts"], 0)
        self.assertTrue(all(abs(value) < 1e-8 for value in lots["inventory_terminal"].values()))


if __name__ == "__main__":
    unittest.main()
