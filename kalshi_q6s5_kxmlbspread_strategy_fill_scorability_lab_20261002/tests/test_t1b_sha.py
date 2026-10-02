import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import itertools
import unittest
from decimal import Decimal

import support
from scoring import score


class T1b(unittest.TestCase):
    def test_t1b_sha_constancy(self):
        import orchestrator
        tape = orchestrator.load_tape()
        packed = orchestrator.run_quote_fill(tape)
        joined = orchestrator.run_join(packed['fill_bytes'], packed['fills_sha256'])
        tickers = tuple(sorted(joined['values']))
        vector = tuple(joined['values'][ticker] for ticker in tickers)
        seen = 0
        for perm in itertools.permutations(vector):
            again = orchestrator.run_quote_fill(tape)
            if again['quotes_sha256'] != packed['quotes_sha256']:
                raise AssertionError('quotes')
            if again['fills_sha256'] != packed['fills_sha256']:
                raise AssertionError('fills')
            mapped = {
                ticker: Decimal(value)
                for ticker, value in zip(tickers, perm)
            }
            score(again['fill_document'], mapped)
            seen += 1
        if seen != 720:
            raise AssertionError('perms')


if __name__ == '__main__':
    unittest.main()
