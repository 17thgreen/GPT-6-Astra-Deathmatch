"""Unit pins for reciprocal books, fee ceilings, and the profit refuse gate.

Claude examiner quotes are order-level and cent-ceiled. Grok maker quotes are
unrounded per unit and are a comparator only. Astra completed_profit uses the
Claude-shaped formula id.
"""
import hashlib
import json
import sys
import unittest
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import feebook


def _money(value):
    return Decimal(value)


class ReciprocalBookTests(unittest.TestCase):
    def setUp(self):
        self.fixture = json.loads((ROOT / 'bids_only_fixture.json').read_text())

    def test_documented_example_reconstructs_asks(self):
        book = feebook.reciprocal_book(self.fixture)
        expected = self.fixture['documented_result']
        self.assertEqual(book['bid_yes'], _money(expected['best_yes_bid']))
        self.assertEqual(book['bid_no'], _money(expected['best_no_bid']))
        self.assertEqual(book['ask_yes'], _money(expected['ask_yes']))
        self.assertEqual(book['ask_no'], _money(expected['ask_no']))
        self.assertEqual(book['spread_yes'], _money(expected['spread_yes']))
        self.assertEqual(book['spread_no'], _money(expected['spread_no']))
        self.assertEqual(book['ask_yes'], feebook.ONE - book['bid_no'])
        self.assertEqual(book['ask_no'], feebook.ONE - book['bid_yes'])
        self.assertEqual(book['spread_yes'], feebook.ONE - book['bid_no'] - book['bid_yes'])
        self.assertEqual(book['spread_no'], book['spread_yes'])
        self.assertEqual(book['touch_yes_size'], Decimal('13.00'))
        self.assertEqual(book['touch_no_size'], Decimal('17.00'))

    def test_best_bid_is_max_price_not_array_order(self):
        book = feebook.reciprocal_book({
            'yes_dollars': [['0.4200', '13.00'], ['0.1000', '5.00']],
            'no_dollars': [['0.5600', '17.00'], ['0.0100', '1.00']],
        })
        self.assertEqual(book['bid_yes'], Decimal('0.4200'))
        self.assertEqual(book['bid_no'], Decimal('0.5600'))
        self.assertEqual(book['ask_yes'], Decimal('0.4400'))

    def test_tied_best_price_sums_touch_size(self):
        book = feebook.reciprocal_book({
            'yes_dollars': [['0.4000', '2.00'], ['0.4000', '3.00']],
            'no_dollars': [['0.5000', '1.00']],
        })
        self.assertEqual(book['touch_yes_size'], Decimal('5.00'))

    def test_missing_side_does_not_invent_an_ask(self):
        book = feebook.reciprocal_book({
            'yes_dollars': [['0.4200', '13.00']],
            'no_dollars': [],
        })
        self.assertEqual(book['bid_yes'], Decimal('0.4200'))
        self.assertIsNone(book['bid_no'])
        self.assertIsNone(book['ask_yes'])
        self.assertEqual(book['ask_no'], Decimal('0.5800'))
        self.assertIsNone(book['spread_yes'])
        self.assertIsNone(book['spread_no'])

    def test_crossed_book_keeps_negative_spread(self):
        book = feebook.reciprocal_book({
            'yes_dollars': [['0.6000', '1']],
            'no_dollars': [['0.5000', '1']],
        })
        self.assertEqual(book['spread_yes'], Decimal('-0.1000'))
        self.assertEqual(book['ask_yes'], Decimal('0.5000'))
        self.assertLess(book['ask_yes'], book['bid_yes'])

    def test_zero_size_level_is_not_the_touch(self):
        book = feebook.reciprocal_book({
            'yes_dollars': [['0.9000', '0'], ['0.4000', '2']],
            'no_dollars': [['0.5000', '1']],
        })
        self.assertEqual(book['bid_yes'], Decimal('0.4000'))


class PolarityFeeTests(unittest.TestCase):
    def setUp(self):
        self.fixture = json.loads((ROOT / 'bids_only_fixture.json').read_text())

    def test_taker_yes_lifts_no_bid(self):
        fill = feebook.polarity_fill(self.fixture, 'yes', '1')
        self.assertEqual(fill['resting_side'], 'no')
        self.assertEqual(fill['taker_price'], Decimal('0.4400'))
        self.assertEqual(fill['maker_price'], Decimal('0.5600'))
        self.assertEqual(fill['taker_price'] + fill['maker_price'], feebook.ONE)
        self.assertEqual(fill['taker_fee']['formula_id'], feebook.EXAMINER_FORMULA_ID)
        self.assertEqual(fill['maker_fee']['formula_id'], feebook.EXAMINER_FORMULA_ID)
        self.assertEqual(fill['taker_fee']['raw'], Decimal('0.07') * Decimal('0.44') * Decimal('0.56'))
        self.assertEqual(fill['taker_fee']['fee'], Decimal('0.02'))
        self.assertEqual(fill['maker_fee']['fee'], Decimal('0.01'))
        self.assertFalse(fill['size_exceeds_touch'])

    def test_taker_no_lifts_yes_bid(self):
        fill = feebook.polarity_fill(self.fixture, 'no', '1')
        self.assertEqual(fill['resting_side'], 'yes')
        self.assertEqual(fill['taker_price'], Decimal('0.5800'))
        self.assertEqual(fill['maker_price'], Decimal('0.4200'))
        self.assertEqual(fill['taker_price'] + fill['maker_price'], feebook.ONE)
        self.assertEqual(
            fill['taker_fee']['raw'],
            Decimal('0.07') * Decimal('0.58') * Decimal('0.42'),
        )

    def test_size_above_touch_is_flagged_and_not_walked(self):
        fill = feebook.polarity_fill(self.fixture, 'yes', '18')
        self.assertTrue(fill['size_exceeds_touch'])
        self.assertEqual(fill['taker_price'], Decimal('0.4400'))
        self.assertEqual(fill['taker_fee']['contracts'], Decimal('18'))

    def test_missing_resting_bid_refuses_the_fill(self):
        with self.assertRaises(feebook.BookIncomplete):
            feebook.polarity_fill({'yes_dollars': [['0.40', '1']], 'no_dollars': []}, 'yes', '1')

    def test_quadratic_is_symmetric_in_price(self):
        low = feebook.order_fee('taker', '10', '0.20')
        high = feebook.order_fee('taker', '10', '0.80')
        self.assertEqual(low['raw'], high['raw'])
        self.assertEqual(low['fee'], high['fee'])


class FeeCeilingTests(unittest.TestCase):
    def test_hand_vectors_match_order_level_ceil(self):
        packet = json.loads((ROOT / 'fee_fixture_vectors.json').read_text())
        self.assertEqual(packet['eps'], 1e-9)
        for row in packet['vectors']:
            quote = feebook.order_fee(row['role'], str(row['C']), str(row['P']))
            self.assertEqual(quote['rate'], _money(str(row['rate'])))
            self.assertEqual(quote['raw'], _money(str(row['raw'])))
            self.assertEqual(quote['fee'], _money(str(row['ceil_cent'])))
            self.assertEqual(feebook.round_up_to_cent_eps(quote['raw']), quote['fee'])
            self.assertEqual(quote['formula_id'], feebook.EXAMINER_FORMULA_ID)

    def test_general_taker_table_matches_cent_ceiling(self):
        table = json.loads((ROOT / 'kalshi_general_fee_table.json').read_text())
        self.assertEqual(table['role'], 'taker')
        self.assertEqual(len(table['rows']), 21)
        for row in table['rows']:
            one = feebook.order_fee('taker', '1', row['price'])
            hundred = feebook.order_fee('taker', '100', row['price'])
            self.assertEqual(one['fee'], _money(row['fee_one_contract']), row['price'])
            self.assertEqual(hundred['fee'], _money(row['fee_hundred_contracts']), row['price'])
            self.assertFalse(one['cap_applied'])

    def test_centicent_ceiling_disagrees_with_the_published_nickel_cell(self):
        raw = Decimal('0.07') * Decimal('0.05') * Decimal('0.95')
        self.assertEqual(raw, Decimal('0.003325'))
        self.assertEqual(feebook.round_up_to_centicent(raw), Decimal('0.0034'))
        self.assertEqual(feebook.order_fee('taker', '1', '0.05')['fee'], Decimal('0.01'))

    def test_exact_cent_is_not_rounded_further(self):
        quote = feebook.order_fee('taker', '100', '0.50')
        self.assertEqual(quote['raw'], Decimal('1.75'))
        self.assertEqual(quote['fee'], Decimal('1.75'))

    def test_boundary_prices_have_zero_fee(self):
        for price in ('0', '1', '0.00', '1.00'):
            quote = feebook.order_fee('taker', '5', price)
            self.assertEqual(quote['raw'], Decimal('0'))
            self.assertEqual(quote['fee'], Decimal('0.00'))

    def test_float_inputs_are_rejected(self):
        with self.assertRaises(TypeError):
            feebook.order_fee('taker', 1.0, '0.50')
        with self.assertRaises(TypeError):
            feebook.order_fee('taker', '1', 0.50)

    def test_partials_skip_the_cent_ceiling(self):
        partials = [
            feebook.order_fee('maker', '1', '0.50', round_up=False)
            for _ in range(10)
        ]
        order = feebook.order_fee('maker', '10', '0.50', round_up=True)
        raw_sum = sum((row['fee'] for row in partials), Decimal('0'))
        self.assertEqual(raw_sum, order['raw'])
        self.assertEqual(order['raw'], Decimal('0.04375'))
        self.assertEqual(order['fee'], Decimal('0.05'))
        omitted = order['fee'] - order['raw']
        self.assertGreaterEqual(omitted, 0)
        self.assertLess(omitted, Decimal('0.01'))
        per_partial_ceil = sum(
            (feebook.order_fee('maker', '1', '0.50')['fee'] for _ in range(10)),
            Decimal('0'),
        )
        self.assertEqual(per_partial_ceil, Decimal('0.10'))
        self.assertGreater(per_partial_ceil - order['fee'], Decimal('0.01'))

    def test_three_maker_partials_would_add_an_extra_cent_if_ceiled(self):
        order = feebook.order_fee('maker', '3', '0.50')
        self.assertEqual(order['raw'], Decimal('0.013125'))
        self.assertEqual(order['fee'], Decimal('0.02'))
        ceiled_each = feebook.order_fee('maker', '1', '0.50')['fee'] * 3
        self.assertEqual(ceiled_each, Decimal('0.03'))

    def test_cap_is_off_by_default_and_binds_only_after_ceiling(self):
        plain = feebook.order_fee('taker', '1', '0.50')
        self.assertEqual(plain['fee'], Decimal('0.02'))
        self.assertFalse(plain['cap_applied'])
        table = feebook.load_series_table()
        table['default'] = dict(table['default'])
        table['default']['M'] = '3'
        table['default']['per_contract_cap_enabled'] = True
        capped = feebook.order_fee('taker', '1', '0.50', table=table)
        unrounded = feebook.order_fee('taker', '1', '0.50', round_up=False, table=table)
        self.assertEqual(capped['raw'], Decimal('0.0525'))
        self.assertEqual(capped['fee'], Decimal('0.035'))
        self.assertTrue(capped['cap_applied'])
        self.assertEqual(unrounded['fee'], Decimal('0.0525'))
        self.assertFalse(unrounded['cap_applied'])
        table['default']['per_contract_cap_enabled'] = False
        open_cap = feebook.order_fee('taker', '1', '0.50', table=table)
        self.assertEqual(open_cap['fee'], Decimal('0.06'))

    def test_m2_without_cap_ceils_the_exact_three_and_a_half_cents(self):
        table = feebook.load_series_table()
        table['default'] = dict(table['default'])
        table['default']['M'] = '2'
        quote = feebook.order_fee('taker', '1', '0.50', table=table)
        self.assertEqual(quote['raw'], Decimal('0.035'))
        self.assertEqual(quote['fee'], Decimal('0.04'))

    def test_maker_disabled_zeros_maker_only(self):
        table = feebook.load_series_table()
        table['overrides'] = {'KXBTCY': {'maker_fees_enabled': False}}
        maker = feebook.order_fee('maker', '100', '0.50', series='KXBTCY', table=table)
        taker = feebook.order_fee('taker', '1', '0.50', series='KXBTCY', table=table)
        self.assertEqual(maker['series_resolution'], 'override')
        self.assertEqual(maker['M'], Decimal('0'))
        self.assertEqual(maker['fee'], Decimal('0.00'))
        self.assertEqual(taker['fee'], Decimal('0.02'))
        self.assertEqual(taker['M'], Decimal('1'))

    def test_unknown_series_uses_default_and_says_so(self):
        quote = feebook.order_fee('taker', '1', '0.50', series='KXNFLGAME')
        self.assertEqual(quote['series_resolution'], 'default_unknown_series')
        self.assertEqual(quote['M'], Decimal('1'))
        self.assertEqual(quote['fee'], Decimal('0.02'))

    def test_split_multiplier_override_is_not_in_the_stub(self):
        stub = feebook.load_series_table()
        self.assertEqual(stub['default']['M'], '1')
        self.assertTrue(stub['default']['maker_fees_enabled'])
        self.assertFalse(stub['default']['per_contract_cap_enabled'])
        self.assertEqual(stub['overrides'], {})
        self.assertNotIn('maker_M', stub['default'])
        table = feebook.load_series_table()
        table['overrides'] = {'EXAMPLE': {'maker_M': '2', 'taker_M': '1'}}
        maker = feebook.order_fee('maker', '1', '0.50', series='EXAMPLE', table=table)
        taker = feebook.order_fee('taker', '1', '0.50', series='EXAMPLE', table=table)
        self.assertEqual(maker['M'], Decimal('2'))
        self.assertEqual(taker['M'], Decimal('1'))
        self.assertEqual(maker['raw'], Decimal('0.00875'))


class ClaudeGrokDiscrepancyTests(unittest.TestCase):
    def test_examiner_ceil_differs_from_unrounded_grok_maker(self):
        """Claude is order-level + ceil. Grok maker is unrounded per unit.

        The examiner channel is Claude-shaped. Grok unrounded is comparator only.
        """
        claude = feebook.order_fee('maker', '1', '0.50')
        grok = feebook.grok_unrounded_maker_per_unit('0.50')
        self.assertEqual(claude['fee'], Decimal('0.01'))
        self.assertEqual(grok['fee'], Decimal('0.004375'))
        self.assertIsNone(grok['contracts'])
        self.assertNotEqual(claude['formula_id'], grok['formula_id'])
        self.assertEqual(claude['formula_id'], feebook.EXAMINER_FORMULA_ID)
        self.assertEqual(grok['formula_id'], feebook.GROK_COMPARATOR_FORMULA_ID)
        large = feebook.order_fee('maker', '1000', '0.50')
        self.assertEqual(large['fee'], Decimal('4.38'))
        self.assertEqual(grok['fee'], Decimal('0.004375'))
        self.assertNotEqual(large['fee'], grok['fee'])

    def test_grok_quote_cannot_build_the_examiner_channel(self):
        taker = feebook.order_fee('taker', '1', '0.50')
        grok = feebook.grok_unrounded_maker_per_unit('0.50')
        with self.assertRaises(feebook.CompletedProfitRefused):
            feebook.examiner_fee_channel(taker, grok)
        with self.assertRaises(feebook.CompletedProfitRefused):
            feebook.classify_scorecard({
                'kind': 'execution',
                'fee_channel': {
                    'formula_id': grok['formula_id'],
                    'taker_fee': '0.02',
                    'maker_fee': format(grok['fee'], 'f'),
                },
            })

    def test_polarity_fill_builds_a_completed_profit_channel(self):
        fixture = json.loads((ROOT / 'bids_only_fixture.json').read_text())
        fill = feebook.polarity_fill(fixture, 'yes', '1')
        channel = feebook.examiner_fee_channel(fill['taker_fee'], fill['maker_fee'])
        label = feebook.classify_scorecard({
            'kind': 'execution',
            'inventory_flat': True,
            'fee_channel': channel,
        })
        self.assertEqual(label, 'completed_profit')
        self.assertEqual(channel['formula_id'], feebook.EXAMINER_FORMULA_ID)
        self.assertEqual(channel['taker_fee'], '0.02')
        self.assertEqual(channel['maker_fee'], '0.01')


class RefuseGateTests(unittest.TestCase):
    def _channel(self):
        return feebook.examiner_fee_channel(
            feebook.order_fee('taker', '1', '0.50'),
            feebook.order_fee('maker', '1', '0.50'),
        )

    def test_missing_channel_is_refused(self):
        with self.assertRaises(feebook.CompletedProfitRefused):
            feebook.classify_scorecard({'kind': 'execution'})

    def test_null_fee_fields_are_refused(self):
        with self.assertRaises(feebook.CompletedProfitRefused):
            feebook.classify_scorecard({
                'fee_channel': {
                    'formula_id': feebook.EXAMINER_FORMULA_ID,
                    'taker_fee': '0.02',
                    'maker_fee': None,
                },
            })

    def test_missing_formula_id_is_refused(self):
        with self.assertRaises(feebook.CompletedProfitRefused):
            feebook.classify_scorecard({
                'fee_channel': {'taker_fee': '0.02', 'maker_fee': '0.01'},
            })

    def test_float_fee_is_refused(self):
        with self.assertRaises(feebook.CompletedProfitRefused):
            feebook.classify_scorecard({
                'fee_channel': {
                    'formula_id': feebook.EXAMINER_FORMULA_ID,
                    'taker_fee': 0.02,
                    'maker_fee': '0.01',
                },
            })

    def test_zero_fee_is_a_real_fee(self):
        label = feebook.classify_scorecard({
            'kind': 'execution',
            'fee_channel': {
                'formula_id': feebook.EXAMINER_FORMULA_ID,
                'taker_fee': '0.02',
                'maker_fee': '0.00',
            },
        })
        self.assertEqual(label, 'completed_profit')

    def test_extrapolation_stays_a_projection(self):
        self.assertEqual(
            feebook.classify_scorecard({'kind': 'extrapolation'}),
            'projection',
        )
        self.assertEqual(
            feebook.classify_scorecard({
                'kind': 'extrapolation',
                'fee_channel': self._channel(),
            }),
            'projection',
        )

    def test_unresolved_inventory_is_not_profit(self):
        with self.assertRaises(feebook.CompletedProfitRefused):
            feebook.classify_scorecard({
                'kind': 'execution',
                'inventory_flat': False,
                'fee_channel': self._channel(),
            })

    def test_absent_inventory_flag_is_not_treated_as_flat_proof(self):
        scorecard = {'kind': 'execution', 'fee_channel': self._channel()}
        self.assertNotIn('inventory_flat', scorecard)
        self.assertEqual(feebook.classify_scorecard(scorecard), 'completed_profit')


class FreezePinTests(unittest.TestCase):
    def test_freeze_matches_specification_and_source_hashes(self):
        freeze = json.loads((ROOT / 'FROZEN_EXPERIMENT.json').read_text())
        self.assertIsNone(freeze['results'])
        self.assertIsNone(freeze['pnl'])
        self.assertIsNotNone(freeze['implementation_sha256'])
        self.assertEqual(
            freeze['examiner_formula_id'],
            feebook.EXAMINER_FORMULA_ID,
        )
        for name, digest in freeze['specification_sha256'].items():
            got = hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
            self.assertEqual(got, digest, name)
        for name, digest in freeze['implementation_sha256'].items():
            got = hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
            self.assertEqual(got, digest, name)
        self.assertNotIn('nfl_factorial_lab_20260921', freeze['implementation_sha256'])

    def test_packet_polarity_matches_the_helper(self):
        packet = json.loads((ROOT / 'fee_fixture_vectors.json').read_text())
        self.assertEqual(packet['taker_side_polarity'], {
            'taker_yes_fills': 'no',
            'taker_no_fills': 'yes',
        })
        self.assertEqual(feebook.TAKER_FILLS_RESTING, {'yes': 'no', 'no': 'yes'})


if __name__ == '__main__':
    unittest.main()
