import copy
import json
import tempfile
import unittest
from pathlib import Path
from dataclasses import replace
from normalize import normalize_quote, normalize_trade, covered_seconds, load
from transport import ListingRouter, GuardedRouter, Config


class NormalizationTests(unittest.TestCase):
    def trade(self, **changes):
        row = dict(ticker='A', created_time='2026-09-17T00:00:00Z', trade_id='t',
                   yes_price_dollars='.51', no_price_dollars='.49', count_fp='5.25', taker_side='yes')
        row.update(changes)
        return row

    def test_aggressor_and_fractional_size_preserved(self):
        row = normalize_trade(self.trade(), 'A', 0, 2e9)
        self.assertEqual((row['taker_side'], row['size']), ('yes', 5.25))

    def test_bad_trade_identity_block_precision_and_price_rejected(self):
        for change in [dict(ticker='B'), dict(is_block_trade=True), dict(count_fp='1.001'),
                       dict(no_price_dollars='.48'), dict(taker_side=''), dict(count_fp='NaN')]:
            with self.subTest(change=change), self.assertRaises(ValueError):
                normalize_trade(self.trade(**change), 'A', 0, 2e9)

    def test_trade_outside_window_rejected(self):
        with self.assertRaises(ValueError):
            normalize_trade(self.trade(), 'A', 0, 1)

    def candle(self, bid='.49', ask='.51'):
        return dict(end_period_ts=120, yes_bid=dict(close_dollars=bid), yes_ask=dict(close_dollars=ask))

    def test_quote_is_delayed_and_uses_only_close(self):
        c = self.candle()
        c['yes_bid']['high_dollars'] = '.90'
        row = normalize_quote(c, 'A', 0, 180)
        self.assertEqual((row['asof'], row['at'], row['bid']), (120, 180, .49))

    def test_null_quote_not_interpolated(self):
        self.assertIsNone(normalize_quote(self.candle(None), 'A', 0, 180))

    def test_crossed_quote_retained_to_invalidate_book(self):
        row = normalize_quote(self.candle('.6', '.4'), 'A', 0, 180)
        self.assertGreater(row['bid'], row['ask'])

    def test_coverage_expires_from_asof_and_breaks_on_invalid_quote(self):
        a = normalize_quote(self.candle(), 'A', 0, 180)
        b = dict(a, at=240, asof=180, bid=.6, ask=.4)
        self.assertEqual(covered_seconds([a], 0, 1000), 240)
        self.assertEqual(covered_seconds([a, b], 0, 1000), 60)

    def test_missing_cohort_never_shrinks(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / 'COHORT.json').write_text(json.dumps(dict(complete=False, games=[])))
            (root / 'CAPTURE.json').write_text(json.dumps(dict(complete=True, failures=[])))
            with self.assertRaisesRegex(ValueError, 'no subset'):
                load(root)


class ListingTests(unittest.TestCase):
    def setup_engines(self, listed_at):
        self.ko = 2_000_000
        self.at = self.ko - 100_000
        self.markets = {t: dict(event='G', direction=d, kickoff=self.ko,
            listed_at=listed_at, verified_mecnet=True) for t, d in [('A', 1), ('B', -1)]}
        cfg = replace(Config(), queue_early=0, queue_last12h=0, quote_source='candles', liquidation_lead_seconds=300)
        return ListingRouter(copy.deepcopy(self.markets), cfg), GuardedRouter(copy.deepcopy(self.markets), cfg)

    def test_listing_gate_blocks_even_with_valid_book(self):
        a, b = self.setup_engines(1_900_100)
        for engine in (a, b):
            engine.books['A'] = dict(bid=.49, ask=.51, bid_at=self.at, ask_at=self.at)
        self.assertFalse(a.eligible('A', self.at))
        self.assertTrue(b.eligible('A', self.at))

    def test_after_listing_exact_q7_orders_and_fills(self):
        a, b = self.setup_engines(0)
        tape = [dict(at=self.at, asof=self.at - 60, ticker=t, bid=.49, ask=.51, kind='quote') for t in ('A', 'B')]
        tape += [dict(at=self.at + i + 1, ticker='A', yes_price=.49 if i % 2 else .51,
                      taker_side='no' if i % 2 else 'yes', size=1000, trade_id=str(i)) for i in range(8)]
        for engine in (a, b):
            for row in tape:
                (engine.on_quote if row.get('kind') == 'quote' else engine.on_trade)(row)
            engine.finish(self.ko - 10800 + 300)
        self.assertTrue(a.fills)
        self.assertEqual(a.fills, b.fills)
        self.assertEqual(a.order_records, b.order_records)
        self.assertEqual(a.cash, b.cash)


if __name__ == '__main__':
    unittest.main()
