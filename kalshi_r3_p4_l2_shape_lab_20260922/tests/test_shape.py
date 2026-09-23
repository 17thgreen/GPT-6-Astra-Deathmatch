"""Unit pins for SF1 half-spread deciles and SF2 depth shape.

Synthetic books check the arithmetic. They are not a Kalshi panel result and
they are not profit.
"""
import hashlib
import json
import sys
import unittest
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(PARENT / 'kalshi_feebook_lab_20260922'))
sys.path.insert(0, str(PARENT / 'kalshi_rails_lab_20260922'))

import feebook
import rails
import shape


def touch(yes, no, yes_size='10', no_size='10'):
    return {
        'yes_dollars': [[yes, yes_size]],
        'no_dollars': [[no, no_size]],
    }


def ladder(touch_price, sizes, step='0.01'):
    price = Decimal(touch_price)
    step = Decimal(step)
    rows = []
    for index, size in enumerate(sizes):
        rows.append([format(price - step * index, 'f'), str(size)])
    return rows


def book(yes_touch, no_touch, sizes, step='0.01'):
    return {
        'yes_dollars': ladder(yes_touch, sizes, step),
        'no_dollars': ladder(no_touch, sizes, step),
    }


def independent_kl(shares):
    total = Decimal('0')
    for share in shares:
        if share == 0:
            continue
        probability = Decimal(share.numerator) / Decimal(share.denominator)
        total += probability * (probability * 10).ln()
    return total


class HalfSpreadTests(unittest.TestCase):
    def test_half_spread_bps_uses_the_feebook_mid(self):
        quote = shape.quoted_yes(touch('0.49', '0.49'))
        self.assertIs(shape.feebook.reciprocal_book, feebook.reciprocal_book)
        self.assertEqual(quote['book']['bid_yes'], Decimal('0.49'))
        self.assertEqual(quote['book']['ask_yes'], Decimal('0.51'))
        self.assertEqual(quote['book']['spread_yes'], Decimal('0.02'))
        self.assertEqual(quote['mid'], Decimal('0.50'))
        self.assertEqual(quote['spread'], quote['book']['spread_yes'])
        self.assertEqual(quote['half_spread'], Decimal('0.01'))
        self.assertEqual(quote['half_spread_bps'], Decimal('200'))
        self.assertEqual(quote['decile'], 5)

    def test_wider_touch_is_400_bps_at_the_same_mid(self):
        quote = shape.quoted_yes(touch('0.48', '0.48'))
        self.assertEqual(quote['mid'], Decimal('0.50'))
        self.assertEqual(quote['half_spread_bps'], Decimal('400'))

    def test_low_mid_uses_the_same_bps_identity(self):
        quote = shape.quoted_yes(touch('0.030', '0.930'))
        self.assertEqual(quote['mid'], Decimal('0.050'))
        self.assertEqual(quote['spread'], Decimal('0.040'))
        self.assertEqual(quote['half_spread_bps'], Decimal('4000'))
        self.assertEqual(quote['decile'], 0)

    def test_negative_spread_is_not_clamped(self):
        quote = shape.quoted_yes(touch('0.60', '0.50'))
        self.assertEqual(quote['spread'], Decimal('-0.10'))
        self.assertLess(quote['half_spread_bps'], 0)

    def test_a_missing_side_does_not_invent_a_spread(self):
        with self.assertRaises(feebook.BookIncomplete):
            shape.quoted_yes({'yes_dollars': [['0.40', '1']], 'no_dollars': []})

    def test_a_zero_mid_has_no_bps_figure(self):
        with self.assertRaises(shape.ShapeRefused):
            shape.quoted_yes(touch('0', '1'))

    def test_float_prices_are_rejected(self):
        with self.assertRaises(TypeError):
            shape.quoted_yes({'yes_dollars': [[0.49, '10']], 'no_dollars': [['0.49', '10']]})


class DecileTests(unittest.TestCase):
    def test_absolute_bins_match_the_table_edges(self):
        self.assertEqual(shape.mid_decile(Decimal('0')), 0)
        self.assertEqual(shape.mid_decile(Decimal('0.0999')), 0)
        self.assertEqual(shape.mid_decile(Decimal('0.1')), 1)
        self.assertEqual(shape.mid_decile(Decimal('0.25')), 2)
        self.assertEqual(shape.mid_decile(Decimal('0.4')), 4)
        self.assertEqual(shape.mid_decile(Decimal('0.5')), 5)
        self.assertEqual(shape.mid_decile(Decimal('0.65')), 6)
        self.assertEqual(shape.mid_decile(Decimal('0.9')), 9)
        self.assertEqual(shape.mid_decile(Decimal('0.999')), 9)
        self.assertEqual(shape.mid_decile(Decimal('1')), 9)
        with self.assertRaises(ValueError):
            shape.mid_decile(Decimal('1.0001'))

    def test_empty_bins_are_null_not_zero(self):
        table = shape.sf1_table([])
        self.assertEqual(len(table), 10)
        self.assertEqual(table[0]['mid_lo'], Decimal('0'))
        self.assertEqual(table[0]['mid_hi'], Decimal('0.1'))
        self.assertEqual(table[4]['mid_lo'], Decimal('0.4'))
        self.assertEqual(table[9]['mid_hi'], Decimal('1'))
        self.assertEqual(table[3]['n'], 0)
        self.assertIsNone(table[3]['median_half_spread_bps'])

    def test_even_count_median_averages_the_two_central_values(self):
        rows = [
            {'decile': 5, 'median_half_spread_bps': Decimal('200')},
            {'decile': 5, 'median_half_spread_bps': Decimal('400')},
        ]
        bin_five = shape.sf1_table(rows)[5]
        self.assertEqual(bin_five['n'], 2)
        self.assertEqual(bin_five['median_half_spread_bps'], Decimal('300'))


class DepthShareTests(unittest.TestCase):
    def test_flat_shares_sum_to_one_and_kl_is_zero(self):
        sizes = ['10'] * 10
        row = shape.top10_depth(book('0.49', '0.49', sizes))
        self.assertEqual(sum(row['shares']), 1)
        self.assertEqual(row['shares'], tuple(Fraction(1, 10) for _ in range(10)))
        self.assertEqual(row['l1_share'], Fraction(1, 10))
        self.assertEqual(row['kl_nats'], Decimal('0'))
        self.assertEqual(row['kl_nats'], independent_kl(row['shares']))
        self.assertFalse(row['top_heavy'])

    def test_one_level_kl_is_natural_log_ten(self):
        row = shape.top10_depth(touch('0.49', '0.49'))
        self.assertEqual(sum(row['shares']), 1)
        self.assertEqual(row['l1_share'], Fraction(1))
        self.assertEqual(row['depths'][0], Fraction(20))
        self.assertEqual(row['depths'][1:], tuple(Fraction(0) for _ in range(9)))
        self.assertEqual(row['kl_nats'], Decimal(10).ln())
        self.assertEqual(row['kl_nats'], independent_kl(row['shares']))
        self.assertTrue(row['top_heavy'])

    def test_top_heavy_threshold_is_strict(self):
        even = shape.top10_depth(book('0.49', '0.49', ['9'] + ['1'] * 9))
        self.assertEqual(even['l1_share'], Fraction(1, 2))
        self.assertFalse(even['top_heavy'])
        heavy = shape.top10_depth(book('0.49', '0.49', ['10'] + ['1'] * 9))
        self.assertGreater(heavy['l1_share'], Fraction(1, 2))
        self.assertTrue(heavy['top_heavy'])
        self.assertGreater(heavy['kl_nats'], 0)
        self.assertLess(heavy['kl_nats'], Decimal(10).ln())

    def test_short_book_does_not_invent_deeper_size(self):
        row = shape.top10_depth(book('0.64', '0.34', ['5', '5', '5']))
        self.assertEqual(row['depths'], (Fraction(10),) * 3 + (Fraction(0),) * 7)
        self.assertEqual(row['observed_depth'], Fraction(30))
        self.assertEqual(sum(row['shares']), 1)
        self.assertEqual(row['shares'][0], Fraction(1, 3))
        self.assertEqual(row['shares'][3], 0)
        self.assertEqual(row['kl_nats'], independent_kl(row['shares']))

    def test_same_price_rows_are_one_level_and_order_is_ignored(self):
        orderbook = {
            'yes_dollars': [['0.10', '1'], ['0.40', '3'], ['0.40', '7']],
            'no_dollars': [['0.10', '4'], ['0.40', '6']],
        }
        row = shape.top10_depth(orderbook)
        self.assertEqual(row['depths'][0], Fraction(16))
        self.assertEqual(row['depths'][1], Fraction(5))
        self.assertEqual(row['depths'][2], 0)
        self.assertEqual(sum(row['shares']), 1)

    def test_a_missing_side_does_not_invent_a_zero_ladder(self):
        with self.assertRaises(feebook.BookIncomplete):
            shape.top10_depth({'yes_dollars': [['0.40', '5']], 'no_dollars': []})


class FreshnessTests(unittest.TestCase):
    def test_the_gate_is_the_rails_predicate(self):
        self.assertIs(shape.rails.judge_freshness, rails.judge_freshness)
        orderbook = touch('0.49', '0.49')
        current = shape.observation(orderbook, 't1')
        verdict = shape.require_content_fresh(None, current)
        self.assertEqual(verdict, rails.Freshness(True, 'initial'))
        with self.assertRaises(shape.StaleSnapshotRefused) as caught:
            shape.require_content_fresh(current, shape.observation(orderbook, 't1'))
        self.assertEqual(caught.exception.reason, 'unchanged')
        changed = shape.observation(touch('0.48', '0.48'), 't1')
        self.assertEqual(
            shape.require_content_fresh(current, changed).reason,
            'content_changed',
        )
        later = shape.observation(orderbook, 't2')
        self.assertEqual(
            shape.require_content_fresh(current, later).reason,
            'transaction_time_changed',
        )

    def test_keepalive_is_refused_even_on_the_first_frame(self):
        current = shape.observation(touch('0.49', '0.49'), 't1')
        with self.assertRaises(shape.StaleSnapshotRefused) as caught:
            shape.require_content_fresh(None, current, keepalive=True)
        self.assertEqual(caught.exception.reason, 'keepalive_ignored')

    def test_key_order_alone_is_not_a_fresh_book(self):
        left = {'yes_dollars': [['0.49', '10']], 'no_dollars': [['0.49', '10']]}
        right = {'no_dollars': [['0.49', '10']], 'yes_dollars': [['0.49', '10']]}
        with self.assertRaises(shape.StaleSnapshotRefused):
            shape.require_content_fresh(
                shape.observation(left, 't1'),
                shape.observation(right, 't1'),
            )


class FixturePanelTests(unittest.TestCase):
    def setUp(self):
        self.doc = shape.load_fixtures()

    def test_predeclared_fixture_panel(self):
        included, refused = shape.screen_snapshots(self.doc['snapshots'])
        self.assertEqual(len(included), 10)
        self.assertEqual(len(refused), 2)
        self.assertEqual(
            [row['reason'] for row in refused],
            ['unchanged', 'keepalive_ignored'],
        )
        shift = [row['freshness'] for row in included if row['ticker'] == 'SYN-SPORTS-SHIFT']
        self.assertEqual(shift, ['initial', 'content_changed'])
        panel = shape.shape_panel(self.doc['snapshots'])
        self.assertIsNone(panel['results'])
        self.assertIsNone(panel['pnl'])
        self.assertIsNone(panel['lee_ready'])
        self.assertFalse(panel['live_orders'])
        self.assertNotIn('fee', panel)
        self.assertEqual(panel['included_snapshots'], 10)
        self.assertEqual(panel['refused_snapshots'], 2)
        by_ticker = {row['ticker']: row for row in panel['markets']}
        self.assertEqual(len(by_ticker), 9)
        self.assertEqual(by_ticker['SYN-SPORTS-D0']['decile'], 0)
        self.assertEqual(by_ticker['SYN-SPORTS-D0']['median_half_spread_bps'], Decimal('4000'))
        self.assertEqual(by_ticker['SYN-SPORTS-D0']['kl_nats'], Decimal('0'))
        self.assertEqual(by_ticker['SYN-SPORTS-D2']['decile'], 2)
        self.assertEqual(by_ticker['SYN-SPORTS-D2']['median_half_spread_bps'], Decimal('400'))
        self.assertEqual(by_ticker['SYN-SPORTS-D5A']['median_half_spread_bps'], Decimal('200'))
        self.assertEqual(by_ticker['SYN-SPORTS-D5B']['median_half_spread_bps'], Decimal('400'))
        shift_row = by_ticker['SYN-SPORTS-SHIFT']
        self.assertEqual(shift_row['n_snapshots'], 2)
        self.assertEqual(shift_row['mean_mid'], Decimal('0.4'))
        self.assertEqual(shift_row['decile'], 4)
        self.assertEqual(shift_row['median_half_spread_bps'], Decimal('300'))
        self.assertEqual(by_ticker['SYN-SPORTS-SHORT']['decile'], 6)
        self.assertEqual(
            by_ticker['SYN-SPORTS-SHORT']['median_half_spread_bps'],
            Decimal(2000) / Decimal(13),
        )
        self.assertEqual(by_ticker['SYN-SPORTS-SHORT']['shares'][3], 0)
        self.assertEqual(by_ticker['SYN-NON-D1']['decile'], 1)
        self.assertEqual(by_ticker['SYN-NON-D1']['l1_share'], Fraction(16, 25))
        self.assertEqual(
            by_ticker['SYN-NON-D1']['median_half_spread_bps'],
            Decimal(2000) / Decimal(3),
        )
        self.assertTrue(by_ticker['SYN-NON-D1']['top_heavy'])
        self.assertEqual(by_ticker['SYN-NON-D7']['decile'], 7)
        self.assertEqual(
            by_ticker['SYN-NON-D7']['median_half_spread_bps'],
            Decimal(400) / Decimal(3),
        )
        self.assertEqual(by_ticker['SYN-NON-D9']['decile'], 9)
        self.assertEqual(
            by_ticker['SYN-NON-D9']['median_half_spread_bps'],
            Decimal(2000) / Decimal(19),
        )
        self.assertEqual(by_ticker['SYN-NON-D9']['l1_share'], Fraction(1, 10))
        sf1 = panel['sf1']['all']
        self.assertEqual(sf1[0]['n'], 1)
        self.assertEqual(sf1[0]['median_half_spread_bps'], Decimal('4000'))
        self.assertEqual(sf1[3]['n'], 0)
        self.assertIsNone(sf1[3]['median_half_spread_bps'])
        self.assertEqual(sf1[4]['n'], 1)
        self.assertEqual(sf1[4]['median_half_spread_bps'], Decimal('300'))
        self.assertEqual(sf1[5]['n'], 2)
        self.assertEqual(sf1[5]['median_half_spread_bps'], Decimal('300'))
        self.assertEqual(panel['sf1']['sports'][5]['n'], 2)
        self.assertEqual(panel['sf1']['non_sports'][5]['n'], 0)
        self.assertEqual(panel['sf1']['non_sports'][1]['n'], 1)
        self.assertEqual(panel['sf2']['sports']['n'], 6)
        self.assertEqual(panel['sf2']['sports']['median_l1_share'], Fraction(1, 10))
        self.assertEqual(panel['sf2']['sports']['top_heavy_count'], 0)
        self.assertEqual(panel['sf2']['non_sports']['n'], 3)
        self.assertEqual(panel['sf2']['non_sports']['median_l1_share'], Fraction(16, 25))
        self.assertEqual(panel['sf2']['non_sports']['top_heavy_count'], 2)
        self.assertEqual(panel['sf2']['all']['median_l1_share'], Fraction(1, 10))
        self.assertEqual(panel['sf2']['all']['median_kl_nats'], Decimal('0'))
        for summary in panel['sf2'].values():
            for shares in (
                row['shares'] for row in panel['markets']
            ):
                self.assertEqual(sum(shares), 1)
            self.assertEqual(len(summary['level_median_shares']), 10)

    def test_running_the_panel_does_not_fill_results(self):
        empty_path = ROOT / 'results' / 'EMPTY_RESULTS.json'
        freeze_path = ROOT / 'FROZEN_EXPERIMENT.json'
        before_empty = empty_path.read_bytes()
        before_freeze = freeze_path.read_bytes()
        shape.shape_panel(self.doc['snapshots'])
        self.assertEqual(empty_path.read_bytes(), before_empty)
        self.assertEqual(freeze_path.read_bytes(), before_freeze)
        stored = json.loads(before_empty)
        frozen = json.loads(before_freeze)
        self.assertIsNone(stored['results'])
        self.assertIsNone(stored['pnl'])
        self.assertIsNone(stored['sf1'])
        self.assertIsNone(stored['sf2'])
        self.assertEqual(stored['status'], 'NOT_RUN')
        self.assertIsNone(frozen['results'])
        self.assertIsNone(frozen['pnl'])
        self.assertEqual(shape.empty_outputs(), stored)


class RefusalTests(unittest.TestCase):
    def test_no_fee_or_pnl_channel_is_exposed(self):
        source = (ROOT / 'shape.py').read_text()
        self.assertNotIn('order_fee', source)
        self.assertNotIn('classify_scorecard', source)
        self.assertNotIn('urllib', source)
        self.assertNotIn('socket', source)
        self.assertFalse(hasattr(shape, 'order_fee'))
        self.assertFalse(shape.LIVE_ORDERS)
        self.assertFalse(shape.LEE_READY)
        self.assertFalse(shape.SIGNAL_RETUNE_000)
        with self.assertRaises(shape.ShapeProfitRefused):
            shape.completed_profit({'fee': '0.01'})
        with self.assertRaises(shape.LeeReadyRefused):
            shape.infer_trade_sign({'price': '0.50'})

    def test_dependency_files_match_the_pins(self):
        pins = json.loads((ROOT / 'SOURCE_PINS.json').read_text())
        feebook_hash = hashlib.sha256(
            (PARENT / 'kalshi_feebook_lab_20260922' / 'feebook.py').read_bytes()
        ).hexdigest()
        rails_hash = hashlib.sha256(
            (PARENT / 'kalshi_rails_lab_20260922' / 'rails.py').read_bytes()
        ).hexdigest()
        self.assertEqual(feebook_hash, pins['feebook_dependency']['feebook_py_sha256'])
        self.assertEqual(rails_hash, pins['rails_dependency']['rails_py_sha256'])
        self.assertEqual(
            pins['feebook_dependency']['commit'],
            '22371178cb2663250b4762f328069571c48cb551',
        )
        self.assertEqual(
            pins['rails_dependency']['commit'],
            '6a28e0d6254327ea4e6451c781bec56215ac6cac',
        )
        self.assertFalse(pins['feebook_dependency']['used_for_fees'])

    def test_a_ticker_cannot_change_category(self):
        first = {
            'ticker': 'SYN-MIX',
            'category': 'sports',
            'transaction_time': 't1',
            'keepalive': False,
            'orderbook_fp': touch('0.49', '0.49'),
        }
        second = dict(first)
        second['category'] = 'non_sports'
        second['transaction_time'] = 't2'
        second['orderbook_fp'] = touch('0.48', '0.48')
        with self.assertRaises(ValueError):
            shape.shape_panel([first, second])

    def test_unknown_category_is_refused(self):
        snap = {
            'ticker': 'SYN-OTHER',
            'category': 'crypto',
            'transaction_time': 't1',
            'keepalive': False,
            'orderbook_fp': touch('0.49', '0.49'),
        }
        with self.assertRaises(ValueError):
            shape.screen_snapshots([snap])


class ImportTests(unittest.TestCase):
    def test_level_parser_is_the_feebook_parser(self):
        self.assertIs(shape.feebook._levels, feebook._levels)
        orderbook = touch('0.42', '0.56', '13.00', '17.00')
        self.assertEqual(
            shape.bid_ladder(feebook._levels(orderbook, 'yes')),
            [(Decimal('0.42'), Decimal('13.00'))],
        )
