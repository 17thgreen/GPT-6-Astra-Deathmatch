import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import unittest
from decimal import Decimal

import support
from scoring import cache_order_fee, score
from tape_quotes import stamp_from_name


class UnpinnedRules(unittest.TestCase):
    def test_r04_filename_stamp(self):
        stamped = stamp_from_name(
            '2026-09-25__c0001__20260925T044831Z__KXMLBSPREAD-26SEP251840PITDET-DET2.json'
        )
        self.assertEqual(stamped[0], '2026-09-25T04:48:31Z')
        self.assertEqual(stamped[1], support.DET)
        self.assertIsNone(stamp_from_name('latest__KXMLBSPREAD-26SEP251840PITDET-DET2.json'))

    def test_r08_no_bid_side(self):
        quotes = support.quote([
            support.snapshot(support.DET, support.T0, yes=('0.4000', '2.00'), no=None),
        ])
        row = quotes['rows'][0]
        self.assertIsNone(row['no_maker'])
        self.assertIsNotNone(row['yes_maker'])
        self.assertEqual(quotes['counts']['empty_side_n'], 1)

    def test_r09_crossed_book(self):
        quotes = support.quote([
            support.snapshot(support.DET, support.T0, yes=('0.6000', '2.00'), no=('0.4000', '2.00')),
        ])
        row = quotes['rows'][0]
        self.assertFalse(row['eligible'])
        self.assertIsNone(row['yes_maker'])
        self.assertIsNone(row['no_maker'])
        self.assertEqual(quotes['counts']['crossed_or_locked_n'], 1)

    def test_r11_cancel_at_next_snapshot_even_if_ineligible(self):
        early = support.snapshot(support.DET, support.T0, path='a')
        crossed = support.snapshot(
            support.DET, support.T1, yes=('0.6000', '2.00'), no=('0.4000', '2.00'), path='b',
        )
        quotes = support.quote([early, crossed])
        self.assertEqual(quotes['rows'][0]['cancel_utc'], support.T1)
        self.assertEqual(quotes['rows'][0]['cancel_reason'], 'next_snapshot')
        self.assertTrue(quotes['rows'][0]['eligible'])
        self.assertFalse(quotes['rows'][1]['eligible'])

    def test_r12_tape_end_and_inactive_get(self):
        lone = support.snapshot(support.DET, support.T0)
        resting = support.quote([lone])
        self.assertEqual(resting['rows'][0]['cancel_utc'], support.TAPE_END)
        self.assertEqual(resting['rows'][0]['cancel_reason'], 'tape_end')
        shortened = support.quote(
            [lone],
            gets=[
                support.market(support.DET, '2026-09-25T04:50:00Z', status='active'),
                support.market(support.DET, '2026-09-25T05:30:00Z', status='closed'),
            ],
        )
        self.assertEqual(shortened['rows'][0]['cancel_reason'], 'status_not_active')
        self.assertEqual(shortened['rows'][0]['yes_maker']['price'], resting['rows'][0]['yes_maker']['price'])
        import orchestrator
        ends = orchestrator.load_tape()['tape_ends']
        self.assertEqual(ends['KXMLBSPREAD-26SEP251845NYMWSH-WSH2'], '2026-09-25T06:02:31Z')

    def test_r13_window(self):
        import fill_engine
        snaps = [support.snapshot(support.DET, support.T0, yes=('0.4000', '1.00'))]
        quotes = support.quote(snaps)
        inside = support.trade(
            support.DET, '2026-09-25T05:00:02Z', 'no', '0.2000', '0.8000',
            count='2.00', trade_id='in',
        )
        same = support.trade(
            support.DET, '2026-09-25T05:00:00.200000Z', 'no', '0.2000', '0.8000',
            count='2.00', trade_id='same',
        )
        filled = fill_engine.run_fills(quotes, [inside])
        skipped = fill_engine.run_fills(quotes, [same])
        yes = [row for row in filled['rows'] if row['leg'] == 'maker' and row['side'] == 'yes'][0]
        no = [row for row in skipped['rows'] if row['leg'] == 'maker' and row['side'] == 'yes'][0]
        self.assertTrue(yes['filled'])
        self.assertFalse(no['filled'])

    def test_r15_block(self):
        import fill_engine
        quotes = support.quote([
            support.snapshot(support.DET, support.T0, yes=('0.4000', '1.00')),
        ])
        prints = [support.trade(
            support.DET, '2026-09-25T05:00:02Z', 'no', '0.2000', '0.8000',
            count='5.00', trade_id='block', block=True,
        )]
        fills = fill_engine.run_fills(quotes, prints)
        self.assertEqual(fills['counts']['excluded_block_n'], 1)
        yes = [row for row in fills['rows'] if row['leg'] == 'maker' and row['side'] == 'yes'][0]
        self.assertFalse(yes['filled'])

    def test_r16_price(self):
        import fill_engine
        quotes = support.quote([
            support.snapshot(support.DET, support.T0, yes=('0.4000', '1.00')),
        ])
        bad = support.trade(
            support.DET, '2026-09-25T05:00:02Z', 'no', '0.3000', '0.3000',
            count='5.00', trade_id='bad-px',
        )
        fills = fill_engine.run_fills(quotes, [bad])
        self.assertEqual(fills['counts']['excluded_price_inconsistent_n'], 1)
        yes = [row for row in fills['rows'] if row['leg'] == 'maker' and row['side'] == 'yes'][0]
        self.assertFalse(yes['filled'])

    def test_r20_best_level_size(self):
        small = support.quote([
            support.snapshot(support.DET, support.T0, yes=('0.4000', '0.50'), no=('0.4000', '0.50')),
        ])
        self.assertIsNone(small['rows'][0]['yes_taker'])
        self.assertIsNone(small['rows'][0]['no_taker'])
        enough = support.quote([
            support.snapshot(support.DET, support.T0, yes=('0.4000', '1.00'), no=('0.4000', '1.00')),
        ])
        self.assertEqual(enough['rows'][0]['yes_taker']['price'], '0.6000')
        self.assertEqual(enough['counts']['requested_taker_contracts'], 2)

    def test_r21_queue_not_reduced_by_taker(self):
        import fill_engine
        quotes = support.quote([
            support.snapshot(support.DET, support.T0, yes=('0.4000', '5.00'), no=('0.4000', '5.00')),
        ])
        self.assertEqual(quotes['rows'][0]['yes_maker']['queue_ahead'], '5.00')
        prints = [support.trade(
            support.DET, '2026-09-25T05:00:02Z', 'no', '0.3000', '0.7000',
            count='6.00', trade_id='q',
        )]
        fills = fill_engine.run_fills(quotes, prints)
        maker = [row for row in fills['rows'] if row['leg'] == 'maker' and row['side'] == 'yes'][0]
        taker = [row for row in fills['rows'] if row['leg'] == 'taker' and row['side'] == 'yes'][0]
        self.assertEqual(maker['queue_ahead'], '5.00')
        self.assertTrue(taker['filled'])
        self.assertTrue(maker['filled'])

    def test_r23_cache_fee_label(self):
        labeled = cache_order_fee('maker', 1, '0.4000')
        self.assertEqual(labeled['label'], 'CACHE_NOT_R1P1')
        self.assertIsNone(labeled['formula_id'])
        self.assertFalse(labeled['fee_honest'])
        self.assertFalse(labeled['claim_as_live_R1P1'])

    def test_r26_identical_second_book_is_stale(self):
        first = support.snapshot(support.DET, support.T0, path='a')
        second = support.snapshot(support.DET, support.T1, path='b')
        quotes = support.quote([first, second])
        self.assertTrue(quotes['rows'][0]['content_fresh_flag'])
        self.assertEqual(quotes['rows'][0]['fresh_reason'], 'initial')
        self.assertFalse(quotes['rows'][1]['content_fresh_flag'])
        self.assertEqual(quotes['rows'][1]['fresh_reason'], 'unchanged')
        self.assertEqual(quotes['counts']['stale_n'], 1)

    def test_r27_empty_is_null_and_true_zero_stays_zero(self):
        empty = score({'rows': []}, {})
        self.assertIsNone(empty['pnl'])
        self.assertIsNone(empty['Q6S5A0_maker_vs_taker_roi_delta'])
        self.assertNotEqual(empty['pnl'], 0)
        self.assertNotEqual(empty['Q6S5A0_maker_vs_taker_roi_delta'], 0)
        rows = []
        for leg in ('maker', 'taker'):
            rows.append({
                'ticker': support.DET,
                'captured_utc': support.T0,
                'leg': leg,
                'side': 'yes',
                'role': leg,
                'filled': True,
                'fill_price': '0',
                'requested': True,
                'content_fresh_flag': True,
            })
        zero = score({'rows': rows}, {support.DET: Decimal('0')})
        self.assertEqual(zero['pnl'], Decimal('0'))
        self.assertIsNone(zero['Q6S5A0_maker_vs_taker_roi_delta'])
        self.assertEqual(zero['A0_null_reason'], 'zero_denominator')

    def test_r28_stress_uses_max_fee_and_keeps_fills(self):
        fee_now = cache_order_fee('maker', 1, '0.99')['fee']
        fee_next = cache_order_fee('maker', 1, '1.00')['fee']
        self.assertGreater(fee_now, fee_next)
        row = {
            'ticker': support.DET,
            'captured_utc': support.T0,
            'leg': 'maker',
            'side': 'yes',
            'role': 'maker',
            'filled': True,
            'fill_price': '0.99',
            'requested': True,
            'content_fresh_flag': True,
        }
        document = {'rows': [row]}
        scored = score(document, {support.DET: Decimal('1')})
        worse = Decimal('1') - Decimal('1.00') - max(fee_now, fee_next)
        doubled = Decimal('1') - Decimal('0.99') - (fee_now * 2)
        self.assertEqual(scored['one_tick_worse']['pnl'], worse)
        self.assertEqual(scored['fees_2x']['pnl'], doubled)
        self.assertTrue(document['rows'][0]['filled'])
        self.assertEqual(scored['filled_contracts_simulated'], 1)


if __name__ == '__main__':
    unittest.main()
