import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import unittest

import support
from tape_quotes import LookaheadRefused, build_quotes


class T3PrintsAfterQuote(unittest.TestCase):
    def test_trades_argument_refused(self):
        snaps = [support.snapshot(support.DET, support.T0)]
        gets = [support.market(support.DET, '2026-09-25T04:50:00Z')]
        ends = {support.DET: support.TAPE_END}
        with self.assertRaises(LookaheadRefused):
            build_quotes(snaps, gets, ends, trades=[])
        with self.assertRaises(LookaheadRefused):
            build_quotes(snaps, gets, ends, [])

    def test_later_book_and_get_do_not_change_placement_terms(self):
        """Placement price, size, queue, side, and freshness stay on the t0 book.

        R11/R12 may still move the cancel stamp of the resting order. A later
        inactive GET shortens only the last order. It does not reprice t0.
        """
        early = support.snapshot(support.DET, support.T0, path='a')
        later = support.snapshot(
            support.DET, support.T1, yes=('0.2000', '9.00'), no=('0.2000', '9.00'), path='b',
        )
        first = support.quote([early, later])
        later['orderbook_fp'] = {
            'yes_dollars': [['0.1100', '1.00']],
            'no_dollars': [['0.1100', '1.00']],
        }
        second = support.quote([early, later])
        self.assertEqual(first['rows'][0], second['rows'][0])
        self.assertEqual(first['rows'][0]['yes_maker']['price'], '0.4000')
        self.assertEqual(first['rows'][0]['cancel_utc'], support.T1)
        lone = support.snapshot(support.DET, support.T0, path='only')
        resting = support.quote([lone])
        shortened = support.quote(
            [lone],
            gets=[
                support.market(support.DET, '2026-09-25T04:50:00Z', status='active'),
                support.market(support.DET, '2026-09-25T05:30:00Z', status='closed'),
            ],
        )
        self.assertEqual(resting['rows'][0]['yes_maker'], shortened['rows'][0]['yes_maker'])
        self.assertEqual(resting['rows'][0]['no_maker'], shortened['rows'][0]['no_maker'])
        self.assertEqual(resting['rows'][0]['content_fresh_flag'], shortened['rows'][0]['content_fresh_flag'])
        self.assertEqual(shortened['rows'][0]['cancel_utc'], '2026-09-25T05:30:00Z')
        self.assertNotEqual(resting['rows'][0]['cancel_utc'], shortened['rows'][0]['cancel_utc'])
        two = support.quote(
            [early, later],
            gets=[
                support.market(support.DET, '2026-09-25T04:50:00Z', status='active'),
                support.market(support.DET, '2026-09-25T05:05:00Z', status='closed'),
            ],
        )
        self.assertEqual(two['rows'][0]['cancel_utc'], support.T1)
        self.assertEqual(two['rows'][0]['yes_maker']['price'], '0.4000')

    def test_same_second_print_unused_and_classifier_refuses_equal_stamps(self):
        import fill_engine
        snaps = [support.snapshot(support.DET, support.T0, yes=('0.4000', '1.00'), no=('0.4000', '1.00'))]
        quotes = support.quote(snaps)
        prints = [
            support.trade(
                support.DET, '2026-09-25T05:00:00.500000Z', 'no', '0.1000', '0.9000',
                count='5.00', trade_id='same-second',
            ),
        ]
        fills = fill_engine.run_fills(quotes, prints)
        makers = [row for row in fills['rows'] if row['leg'] == 'maker']
        self.assertTrue(makers)
        self.assertTrue(all(row['filled'] is False for row in makers))
        pr60 = fill_engine.load_pr60()
        with self.assertRaises(pr60.LookaheadRefused):
            pr60.classify_fill({
                'quote_ts': support.T0,
                'trade_ts': support.T0,
                'resting_side': 'bid',
                'resting_price': '0.4000',
                'trade_yes_price': '0.1000',
                'ticker': support.DET,
            })

    def test_print_at_cancel_stamp_fills_neither_order(self):
        import fill_engine
        early = support.snapshot(support.DET, support.T0, yes=('0.4000', '1.00'), no=('0.4000', '2.00'), path='a')
        later = support.snapshot(support.DET, support.T1, yes=('0.4000', '1.00'), no=('0.4000', '2.00'), path='b')
        quotes = support.quote([early, later])
        prints = [
            support.trade(
                support.DET, support.T1, 'no', '0.1000', '0.9000',
                count='5.00', trade_id='at-cancel',
            ),
        ]
        fills = fill_engine.run_fills(quotes, prints)
        makers = [row for row in fills['rows'] if row['leg'] == 'maker' and row['side'] == 'yes']
        self.assertEqual(len(makers), 2)
        self.assertTrue(all(row['filled'] is False for row in makers))


if __name__ == '__main__':
    unittest.main()
