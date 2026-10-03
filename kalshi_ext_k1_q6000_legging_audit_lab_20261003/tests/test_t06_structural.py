import unittest

import support  # noqa: F401
from constants import (
    EVENTS,
    FILL_ROWS,
    LEDGER_UCH,
    MAKER_CONTRACTS,
    MAKER_NO_CONTRACTS,
    MAKER_NO_SHARE,
    MAKER_YES_CONTRACTS,
    QUOTE_ROWS,
    SCOUT_MAKER_NO_SHARE,
    SCOUT_TAKER_YES_SHARE,
    TAKER_CONTRACTS,
    TAKER_YES_SHARE,
    TICKERS,
    TRADE_ROWS,
)
from orchestrator import measure


class T06Structural(unittest.TestCase):
    def test_scout_facts_reproduce(self):
        measurement = measure(write=True)
        facts = measurement["facts"]
        tape = measurement["tape"]
        self.assertEqual(measurement["structural_failures"], [])
        self.assertTrue(measurement["structural_ok"])
        self.assertAlmostEqual(facts["maker_no_share"], MAKER_NO_SHARE, delta=1e-6)
        self.assertLessEqual(abs(facts["maker_no_share"] - SCOUT_MAKER_NO_SHARE), 0.0005)
        self.assertAlmostEqual(facts["maker_no_share"], 0.989706, delta=5e-7)
        self.assertAlmostEqual(tape["taker_yes_contract_share"], TAKER_YES_SHARE, delta=1e-6)
        self.assertLessEqual(abs(tape["taker_yes_contract_share"] - SCOUT_TAKER_YES_SHARE), 0.0005)
        self.assertAlmostEqual(tape["taker_yes_contract_share"], 0.916882, delta=5e-7)
        self.assertEqual(facts["rows"], FILL_ROWS)
        self.assertEqual(facts["rows"], 12853)
        self.assertEqual(tape["trades"], TRADE_ROWS)
        self.assertEqual(tape["quotes"], QUOTE_ROWS)
        self.assertEqual(len(tape["tickers"]), TICKERS)
        self.assertEqual(len(measurement["weeks"]), EVENTS)
        self.assertAlmostEqual(facts["maker_no_contracts"], MAKER_NO_CONTRACTS, delta=0.01)
        self.assertAlmostEqual(facts["maker_yes_contracts"], MAKER_YES_CONTRACTS, delta=0.01)
        self.assertAlmostEqual(facts["maker_contracts"], MAKER_CONTRACTS, delta=0.01)
        self.assertAlmostEqual(facts["taker_contracts"], TAKER_CONTRACTS, delta=0.01)
        self.assertAlmostEqual(measurement["lots"]["uch_integral"], LEDGER_UCH, delta=0.01)
        self.assertEqual(measurement["lots"]["uch_integral"], LEDGER_UCH)
        self.assertEqual(measurement["joined"]["game_ids"].__len__(), 31)


if __name__ == "__main__":
    unittest.main()
