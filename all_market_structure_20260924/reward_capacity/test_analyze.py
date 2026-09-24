import unittest
from decimal import Decimal as D
from analyze import concurrent, ledger


class CapacityTests(unittest.TestCase):
    def test_full_capital_and_reserve(self):
        r = ledger(2000, 0)
        self.assertEqual((r['quote_capital'], r['fee_reserve'], r['reward'], r['net_cushion']),
                         (5000, 500, 7420, 1920))
        self.assertEqual(r['roi_quote_pct'], 38.4)

    def test_failed_quotes_lose_reward_without_double_counting_principal(self):
        self.assertEqual(ledger(2000, '.25')['net_cushion'], 65)
        self.assertEqual(ledger(2000, 1)['net_cushion'], -5500)

    def test_all_in_budget(self):
        r = ledger(1818, 0)
        self.assertEqual(r['quote_capital']+r['fee_reserve'], 4999.5)
        self.assertEqual(r['net_cushion'], 1745.28)
        self.assertGreater(D(1819)*D('2.75'), 5000)

    def test_failure_inputs_rejected(self):
        for f in ('-.1', '1.1'):
            with self.assertRaises(ValueError):
                ledger(2000, f)

    def test_no_snapshot_or_alternative_side_double_counting(self):
        a=dict(source='test', cycle=1, book_received_ns=1, ticker='T', program_id='P', side='yes',
               passes=True, principal=2.5, fee_stress_reserve=.25, base_half_uptime_reward=4,
               stressed_half_uptime_reward=3.71, conditional_cushion=.96, classification='supported_level')
        rows=[a, dict(a), dict(a, side='no'), dict(a, book_received_ns=2)]
        batches=concurrent(rows)
        self.assertEqual([r['orders'] for r in batches], [1, 1])
        self.assertEqual([r['quote_capital'] for r in batches], [2.5, 2.5])


if __name__ == '__main__':
    unittest.main()
