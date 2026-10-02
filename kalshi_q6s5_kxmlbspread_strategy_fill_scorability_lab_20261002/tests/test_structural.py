import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import unittest
from decimal import Decimal

import support


class Structural(unittest.TestCase):
    def test_pinned_tape_counts(self):
        import orchestrator
        from scoring import score
        tape = orchestrator.load_tape()
        counts = orchestrator.structural_counts(tape)
        self.assertEqual(counts['n_books'], 15)
        self.assertEqual(counts['eligible_placements'], 15)
        self.assertEqual(counts['crossed_or_locked_n'], 0)
        self.assertEqual(counts['empty_side_n'], 0)
        self.assertEqual(counts['fresh_n'], 15)
        self.assertEqual(counts['stale_n'], 0)
        self.assertEqual(counts['requested_maker_contracts'], 30)
        self.assertEqual(counts['prints_in'], 21)
        self.assertEqual(counts['excluded_block_n'], 0)
        self.assertEqual(counts['excluded_native_conflict_n'], 0)
        self.assertEqual(counts['excluded_price_inconsistent_n'], 0)
        self.assertEqual(counts['excluded_admit1_window_n'], 0)
        self.assertEqual(
            counts['maker_filled_n'] + counts['maker_unfilled_n'],
            30,
        )
        self.assertIsInstance(counts['requested_taker_contracts'], int)
        self.assertIsNone(counts['pnl'])
        self.assertIsNone(counts['roi'])
        self.assertIsNone(counts['Q6S5A0_maker_vs_taker_roi_delta'])
        self.assertIsNone(counts['Q6S5A1_fresh_vs_stale_gap'])
        self.assertEqual(counts['A1_null_reason'], 'STALE_BIN_EMPTY')
        self.assertFalse(counts['counts_toward_keep'])
        self.assertIsNone(counts['verdict'])
        self.assertEqual(counts['labels']['family_size'], 1)
        self.assertEqual(counts['labels']['fee'], 'CACHE_NOT_R1P1')
        self.assertEqual(counts['labels']['verdict_domain'], 'ITERATE|INCONCLUSIVE')
        packed = orchestrator.run_quote_fill(tape)
        reasons = {}
        for row in packed['quote_document']['rows']:
            reasons[row['fresh_reason']] = reasons.get(row['fresh_reason'], 0) + 1
        self.assertEqual(reasons.get('initial'), 6)
        self.assertEqual(reasons.get('content_changed'), 9)
        joined = orchestrator.run_join(packed['fill_bytes'], packed['fills_sha256'])
        self.assertEqual(joined['settled_join_n'], 6)
        self.assertEqual(joined['unresolved_tickers'], [])
        ones = 0
        zeros = 0
        mapped = {}
        for ticker, value in joined['values'].items():
            number = Decimal(value)
            mapped[ticker] = number
            if number == 1:
                ones += 1
            elif number == 0:
                zeros += 1
            else:
                self.fail('domain')
        self.assertEqual(ones, 1)
        self.assertEqual(zeros, 5)
        scored = score(packed['fill_document'], mapped)
        self.assertIsNone(scored['Q6S5A1_fresh_vs_stale_gap'])
        self.assertEqual(scored['A1_null_reason'], 'STALE_BIN_EMPTY')
        self.assertFalse(scored['counts_toward_keep'])
        self.assertIsNone(scored['formula_id'])
        self.assertIsNone(scored['common_scorecard']['fill_rate'])
        self.assertIsNone(scored['verdict'])


if __name__ == '__main__':
    unittest.main()
