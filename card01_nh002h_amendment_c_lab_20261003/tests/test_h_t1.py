"""T1 display-only tally for an empty 11-03 book. Synthetic rows only."""
from __future__ import annotations

import unittest
from decimal import Decimal

from card01_amc.book_1103 import LABELS, TALLY_LABELS, adverse_selection
from tests.test_regime_split_secondary import EXPECTED, fixture_b


class EmptyBookTallyTests(unittest.TestCase):
    def test_h_t1_empty_book_tallies_entry_book_empty(self):
        rows, signals, _book, _settled = fixture_b()
        block = adverse_selection(signals, {row["race_id"]: row for row in rows}, {})
        self.assertEqual(block["class"], "DISPLAY-ONLY")
        plus = block["plus_24h"]
        self.assertEqual(plus["n_missing_by_label"]["ENTRY_BOOK_EMPTY"], len(signals))
        self.assertIsNone(plus["sum_cents"])
        self.assertIsNone(plus["mean_cents"])
        statuses = {item["status"] for item in plus["per_signal"]}
        self.assertTrue(statuses <= set(TALLY_LABELS))
        self.assertEqual(LABELS, (
            "MARKET_NOT_OPEN_AT_T",
            "NOT_CAPTURED",
            "NOT_CAPTURED_EGRESS_CLOSED",
            "NO_TWO_SIDED_BOOK_IN_WINDOW",
        ))
        self.assertEqual(TALLY_LABELS, LABELS + ("ENTRY_BOOK_EMPTY",))

    def test_h_t1_defined_case_unchanged(self):
        rows, signals, book, _settled = fixture_b()
        block = adverse_selection(signals, {row["race_id"]: row for row in rows}, book)
        plus = [item["value"] for item in block["plus_24h"]["per_signal"]]
        settle = [item["value"] for item in block["settlement"]["per_signal"]]
        self.assertEqual([Decimal(item) for item in plus], [Decimal(item) for item in EXPECTED["T1h"]["plus_24h"]])
        self.assertEqual(Decimal(block["plus_24h"]["mean_cents"]), Decimal(EXPECTED["T1h"]["plus_24h_mean"]))
        self.assertEqual(Decimal(block["plus_24h"]["sum_cents"]), Decimal(EXPECTED["T1h"]["plus_24h_sum"]))
        self.assertEqual([Decimal(item) for item in settle], [Decimal(item) for item in EXPECTED["T1h"]["settlement"]])
        self.assertEqual(block["class"], "DISPLAY-ONLY")
