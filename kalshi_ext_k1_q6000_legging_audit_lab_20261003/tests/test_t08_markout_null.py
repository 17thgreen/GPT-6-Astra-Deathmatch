import unittest

import support  # noqa: F401
from markouts import QuoteBook, outcome_mid, portion_markouts


def _quote(at, asof, bid, ask):
    return {"at": at, "asof": asof, "ticker": "T", "bid": bid, "ask": ask, "kind": "quote"}


class T08MarkoutNull(unittest.TestCase):
    def test_staleness_bounds_and_prints_do_not_move_the_mid(self):
        book = QuoteBook()
        book.add_quote(_quote(299.999, 0.0, 0.40, 0.60))
        book.note("T", 1000.0)
        self.assertAlmostEqual(book.yes_mid("T", 299.999), 0.50)
        self.assertIsNone(book.yes_mid("T", 300.0))
        self.assertIsNone(book.yes_mid("T", -0.001))
        self.assertIsNone(book.yes_mid("T", 1000.001))
        empty = QuoteBook()
        empty.note("T", 10.0)
        self.assertIsNone(empty.yes_mid("T", 10.0))
        crossed = QuoteBook()
        crossed.add_quote(_quote(0.0, 0.0, 0.60, 0.40))
        self.assertIsNone(crossed.yes_mid("T", 10.0))
        fresh = QuoteBook()
        fresh.add_quote(_quote(10.0, 10.0, 0.40, 0.42))
        before = fresh.yes_mid("T", 10.0)
        fresh.note("T", 10.0)
        self.assertEqual(fresh.yes_mid("T", 10.0), before)
        self.assertNotEqual(before, 0.99)
        self.assertEqual(outcome_mid(before, "yes"), before)
        self.assertAlmostEqual(outcome_mid(before, "no"), 1 - before)

    def test_settlement_does_not_change_horizon_or_close(self):
        book = QuoteBook()
        book.add_quote(_quote(0.0, 0.0, 0.40, 0.60))
        book.add_quote(_quote(100.0, 100.0, 0.45, 0.55))
        portion = {
            "ticker": "T",
            "outcome": "yes",
            "t_open": 0.0,
            "p_entry": 0.40,
            "closes": [(1.0, 100.0)],
        }
        left = portion_markouts(portion, book, (60,), 0.01, 1.0)
        right = portion_markouts(portion, book, (60,), 0.01, 0.0)
        self.assertEqual(left["60"], right["60"])
        self.assertEqual(left["CLOSE"], right["CLOSE"])
        self.assertNotEqual(left["SETTLE"], right["SETTLE"])


if __name__ == "__main__":
    unittest.main()
