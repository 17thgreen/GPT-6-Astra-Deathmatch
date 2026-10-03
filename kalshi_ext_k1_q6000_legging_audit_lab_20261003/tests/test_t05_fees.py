import unittest
from decimal import Decimal

import support  # noqa: F401
from constants import PINS_REL
from fees import ceil_cent, fee_labels, headline_order_fee, model_fee, read_kxnflgame_maker_multiplier
from pins_io import verified_bytes


class T05Fees(unittest.TestCase):
    def test_headline_examples_and_per_order_sum(self):
        raw, six = model_fee(Decimal("1"), Decimal("0.50"))
        self.assertEqual(six, Decimal("0.004375"))
        self.assertEqual(ceil_cent(six), Decimal("0.01"))

        raw, six = model_fee(Decimal("247.5"), Decimal("0.37"))
        self.assertEqual(raw, Decimal("1.009614375"))
        self.assertEqual(six, Decimal("1.009615"))
        self.assertEqual(ceil_cent(six), Decimal("1.01"))

        raw, six = model_fee(Decimal("2.5"), Decimal("0.37"))
        self.assertEqual(raw, Decimal("0.010198125"))
        self.assertEqual(six, Decimal("0.010199"))
        self.assertEqual(ceil_cent(six), Decimal("0.02"))

        _raw, six = model_fee(Decimal("100"), Decimal("0.50"))
        self.assertEqual(six, Decimal("0.437500"))
        self.assertEqual(ceil_cent(six), Decimal("0.44"))

        raw, six = model_fee(Decimal("1"), Decimal("0.05"))
        self.assertEqual(raw, Decimal("0.00083125"))
        self.assertEqual(six, Decimal("0.000832"))
        self.assertEqual(ceil_cent(six), Decimal("0.01"))

        raw, six = model_fee(Decimal("250"), Decimal("0.95"))
        self.assertEqual(raw, Decimal("0.2078125"))
        self.assertEqual(six, Decimal("0.207813"))
        self.assertEqual(ceil_cent(six), Decimal("0.21"))

        order_fee, per_contract, six_sum = headline_order_fee(
            [(Decimal("247.5"), Decimal("0.37")), (Decimal("2.5"), Decimal("0.37"))]
        )
        self.assertEqual(six_sum, Decimal("1.019814"))
        self.assertEqual(order_fee, Decimal("1.02"))
        self.assertEqual(per_contract, Decimal("1.02") / Decimal("250"))
        per_fill = ceil_cent(Decimal("1.009615")) + ceil_cent(Decimal("0.010199"))
        self.assertEqual(per_fill, Decimal("1.03"))
        self.assertNotEqual(order_fee, per_fill)

    def test_multiplier_and_labels(self):
        text = verified_bytes(PINS_REL["schedule"]).decode("utf-8")
        multiplier, rows = read_kxnflgame_maker_multiplier(text)
        self.assertEqual(multiplier, Decimal(1))
        self.assertTrue(rows)
        self.assertTrue(all(maker == "1" and taker == "1" for _line, maker, taker in rows))
        labels = fee_labels()
        self.assertEqual(labels["fee_label"], "CACHE_NOT_R1P1")
        self.assertEqual(labels["headline_name"], "NON_DIRECT_CENT_HEADLINE")
        self.assertIsNone(labels["examiner_pin_account_class"])


if __name__ == "__main__":
    unittest.main()
