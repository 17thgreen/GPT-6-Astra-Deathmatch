import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import unittest
from decimal import Decimal

import support
from scoring import score
from tape_quotes import canonical_bytes


class T1Permutation(unittest.TestCase):
    def test_swap_changes_pnl_only(self):
        snapshots = [
            support.snapshot(support.DET, support.T0),
            support.snapshot(support.PIT, support.T0),
        ]
        prints = [
            support.trade(
                support.DET, '2026-09-25T05:00:02.100000Z', 'no', '0.3000', '0.7000',
                count='3.00', trade_id='det-through',
            ),
        ]
        first = support.quote(snapshots)
        second = support.quote(snapshots)
        self.assertEqual(canonical_bytes(first), canonical_bytes(second))
        import fill_engine
        left = fill_engine.run_fills(first, prints)
        right = fill_engine.run_fills(second, prints)
        self.assertEqual(canonical_bytes(left), canonical_bytes(right))
        self.assertEqual(
            hashlib_same(left, right),
            True,
        )
        maker = [row for row in left['rows'] if row['ticker'] == support.DET and row['leg'] == 'maker' and row['filled']]
        taker = [row for row in left['rows'] if row['ticker'] == support.DET and row['leg'] == 'taker' and row['filled']]
        self.assertGreaterEqual(len(maker), 1)
        self.assertGreaterEqual(len(taker), 1)
        base = {support.DET: Decimal('1'), support.PIT: Decimal('0')}
        swapped = {support.DET: Decimal('0'), support.PIT: Decimal('1')}
        self.assertNotEqual(score(left, base)['pnl'], score(left, swapped)['pnl'])


def hashlib_same(left, right):
    import hashlib
    return hashlib.sha256(canonical_bytes(left)).hexdigest() == hashlib.sha256(canonical_bytes(right)).hexdigest()


if __name__ == '__main__':
    unittest.main()
