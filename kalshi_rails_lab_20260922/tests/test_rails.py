"""Unit pins for the R1-P5 queue, fee-credit, freshness, and MICRO helpers.

Synthetic rows check the arithmetic. They are not a historical walk and they
are not profit.
"""
import hashlib
import json
import sys
import unittest
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FEEBOOK = ROOT.parent / 'kalshi_feebook_lab_20260922'
sys.path.insert(0, str(ROOT))

import rails


def intent(price, size, outcome='yes', ticker='MKT', kind='maker'):
    return rails.QuoteIntent(ticker, outcome, Decimal(price), Decimal(size), kind)


def trade(side, yes, size, ticker='MKT', no=None, at=None):
    row = {
        'ticker': ticker,
        'taker_side': side,
        'yes_price': Decimal(yes),
        'size': Decimal(size),
        'created_time': at,
    }
    if no is not None:
        row['no_price'] = Decimal(no)
    return row


class QueuePolarityTests(unittest.TestCase):
    def test_polarity_matches_the_feebook_vector_packet(self):
        packet = json.loads((FEEBOOK / 'fee_fixture_vectors.json').read_text())
        self.assertEqual(rails.TAKER_FILLS_OUR['yes'], packet['taker_side_polarity']['taker_yes_fills'])
        self.assertEqual(rails.TAKER_FILLS_OUR['no'], packet['taker_side_polarity']['taker_no_fills'])
        self.assertEqual(rails.TAKER_FILLS_OUR, {'yes': 'no', 'no': 'yes'})

    def test_taker_yes_fills_our_no_and_leaves_yes_untouched(self):
        book = rails.QueueInstrument(queue_model='front')
        book.replace_quotes([
            intent('0.40', '10', outcome='yes'),
            intent('0.40', '10', outcome='no'),
        ])
        fills = book.on_trade(trade('yes', '0.60', '10', no='0.40'))
        self.assertEqual(len(fills), 1)
        self.assertEqual(fills[0].outcome, 'no')
        self.assertEqual(fills[0].size, Decimal('5'))
        self.assertEqual(fills[0].price, Decimal('0.40'))
        self.assertEqual(book.order('MKT', 'no').filled, Decimal('5'))
        self.assertEqual(book.order('MKT', 'yes').filled, Decimal('0'))
        self.assertEqual(book.order('MKT', 'yes').queue_ahead, Decimal('0'))

    def test_taker_no_fills_our_yes_and_leaves_no_untouched(self):
        book = rails.QueueInstrument(queue_model='front')
        book.replace_quotes([
            intent('0.40', '10', outcome='yes'),
            intent('0.40', '10', outcome='no'),
        ])
        fills = book.on_trade(trade('no', '0.40', '10', no='0.60'))
        self.assertEqual([row.outcome for row in fills], ['yes'])
        self.assertEqual(fills[0].size, Decimal('5'))
        self.assertEqual(book.order('MKT', 'no').filled, Decimal('0'))

    def test_a_higher_print_does_not_consume_queue(self):
        book = rails.QueueInstrument(queue_ahead_contracts='100', queue_model='measured')
        book.replace_quotes([intent('0.40', '10')])
        fills = book.on_trade(trade('no', '0.41', '50', no='0.59'))
        self.assertEqual(fills, [])
        self.assertEqual(book.order('MKT', 'yes').queue_ahead, Decimal('100'))
        self.assertEqual(book.order('MKT', 'yes').filled, Decimal('0'))

    def test_a_trade_through_the_bid_fills_at_our_price(self):
        book = rails.QueueInstrument(queue_model='front')
        book.replace_quotes([intent('0.40', '10')])
        fills = book.on_trade(trade('no', '0.39', '4', no='0.61'))
        self.assertEqual(fills[0].price, Decimal('0.40'))
        self.assertEqual(fills[0].size, Decimal('2'))

    def test_no_bid_uses_the_no_price_and_ignores_a_richer_yes_print(self):
        book = rails.QueueInstrument(queue_model='front')
        book.replace_quotes([intent('0.40', '10', outcome='no')])
        quiet = book.on_trade(trade('yes', '0.59', '10', no='0.41'))
        self.assertEqual(quiet, [])
        self.assertEqual(book.order('MKT', 'no').filled, Decimal('0'))
        fills = book.on_trade(trade('yes', '0.60', '10', no='0.40'))
        self.assertEqual(fills[0].outcome, 'no')
        self.assertEqual(fills[0].price, Decimal('0.40'))


class QueueParticipationTests(unittest.TestCase):
    def test_defaults_and_scenario_labels(self):
        book = rails.QueueInstrument()
        self.assertEqual(book.queue_ahead_contracts, Decimal('3300'))
        self.assertEqual(book.fill_participation, Decimal('0.5'))
        self.assertEqual(book.queue_model, 'measured')
        self.assertEqual(rails.scenario_queue('q3300'), Decimal('3300'))
        self.assertEqual(rails.scenario_queue('q10000'), rails.STRESS_QUEUE_AHEAD)
        self.assertEqual(rails.STRESS_QUEUE_AHEAD, Decimal('10000'))
        with self.assertRaises(ValueError):
            rails.QueueInstrument(queue_model='stress')

    def test_default_queue_consumes_before_participation(self):
        book = rails.QueueInstrument()
        book.replace_quotes([intent('0.50', '5000')])
        self.assertEqual(book.on_trade(trade('no', '0.50', '3300', no='0.50')), [])
        self.assertEqual(book.order('MKT', 'yes').queue_ahead, Decimal('0'))
        fills = book.on_trade(trade('no', '0.50', '200', no='0.50'))
        self.assertEqual(fills[0].size, Decimal('100'))
        self.assertEqual(book.order('MKT', 'yes').filled, Decimal('100'))

    def test_one_print_past_the_default_queue_pays_half_the_excess(self):
        book = rails.QueueInstrument()
        book.replace_quotes([intent('0.50', '5000')])
        fills = book.on_trade(trade('no', '0.50', '3500', no='0.50'))
        self.assertEqual(fills[0].size, Decimal('100'))
        self.assertEqual(book.order('MKT', 'yes').queue_ahead, Decimal('0'))

    def test_stress_queue_is_measured_with_10000_ahead(self):
        book = rails.QueueInstrument(queue_ahead_contracts=rails.scenario_queue('q10000'))
        self.assertEqual(book.queue_model, 'measured')
        book.replace_quotes([intent('0.50', '5000')])
        self.assertEqual(book.on_trade(trade('no', '0.50', '10000', no='0.50')), [])
        fills = book.on_trade(trade('no', '0.50', '20', no='0.50'))
        self.assertEqual(fills[0].size, Decimal('10'))

    def test_front_model_is_zero_ahead_and_ignores_book_size(self):
        book = rails.QueueInstrument(queue_model='front')
        book.replace_quotes(
            [intent('0.50', '100')],
            book_sizes={('MKT', 'yes'): Decimal('100')},
        )
        self.assertEqual(book.order('MKT', 'yes').queue_ahead, Decimal('0'))
        fills = book.on_trade(trade('no', '0.50', '80', no='0.50'))
        self.assertEqual(fills[0].size, Decimal('40'))

    def test_measured_book_size_replaces_the_default_ahead(self):
        book = rails.QueueInstrument()
        book.replace_quotes(
            [intent('0.50', '100')],
            book_sizes={('MKT', 'yes'): Decimal('100')},
        )
        self.assertEqual(book.on_trade(trade('no', '0.50', '100', no='0.50')), [])
        fills = book.on_trade(trade('no', '0.50', '20', no='0.50'))
        self.assertEqual(fills[0].size, Decimal('10'))

    def test_measured_zero_book_size_is_an_empty_level(self):
        book = rails.QueueInstrument()
        book.replace_quotes(
            [intent('0.50', '10')],
            book_sizes={('MKT', 'yes'): Decimal('0')},
        )
        self.assertEqual(book.queue_model, 'measured')
        fills = book.on_trade(trade('no', '0.50', '10', no='0.50'))
        self.assertEqual(fills[0].size, Decimal('5'))

    def test_fill_is_capped_by_remaining_size(self):
        book = rails.QueueInstrument(queue_model='front')
        book.replace_quotes([intent('0.50', '3')])
        fills = book.on_trade(trade('no', '0.50', '100', no='0.50'))
        self.assertEqual(fills[0].size, Decimal('3'))

    def test_fractional_participation_is_not_floored_to_a_cent_contract(self):
        book = rails.QueueInstrument(queue_model='front')
        book.replace_quotes([intent('0.50', '10')])
        fills = book.on_trade(trade('no', '0.50', '1', no='0.50'))
        self.assertEqual(fills[0].size, Decimal('0.5'))

    def test_float_inputs_are_rejected(self):
        with self.assertRaises(TypeError):
            rails.QueueInstrument(fill_participation=0.5)
        with self.assertRaises(TypeError):
            rails.QueueInstrument(queue_ahead_contracts=3300.0)
        book = rails.QueueInstrument(queue_model='front')
        with self.assertRaises(TypeError):
            book.replace_quotes([rails.QuoteIntent('MKT', 'yes', 0.50, Decimal('1'))])
        with self.assertRaises(TypeError):
            book.on_trade({'ticker': 'MKT', 'taker_side': 'no', 'yes_price': 0.50, 'size': '1'})


class SamePriceQueueTests(unittest.TestCase):
    def test_same_price_keeps_consumed_queue_and_the_unfilled_remainder(self):
        book = rails.QueueInstrument()
        book.replace_quotes([intent('0.50', '100')])
        book.on_trade(trade('no', '0.50', '500', no='0.50'))
        self.assertEqual(book.order('MKT', 'yes').queue_ahead, Decimal('2800'))
        book.replace_quotes([intent('0.50', '5')])
        kept = book.order('MKT', 'yes')
        self.assertEqual(kept.queue_ahead, Decimal('2800'))
        self.assertEqual(kept.intent.size, Decimal('100'))
        self.assertEqual(kept.filled, Decimal('0'))

    def test_a_new_price_joins_the_back_of_the_queue(self):
        book = rails.QueueInstrument()
        book.replace_quotes([intent('0.50', '100')])
        book.on_trade(trade('no', '0.50', '500', no='0.50'))
        book.replace_quotes([intent('0.49', '25')])
        reset = book.order('MKT', 'yes')
        self.assertEqual(reset.queue_ahead, Decimal('3300'))
        self.assertEqual(reset.intent.size, Decimal('25'))
        self.assertEqual(reset.intent.price, Decimal('0.49'))

    def test_same_price_after_a_partial_fill_keeps_the_remainder(self):
        book = rails.QueueInstrument(queue_ahead_contracts='10')
        book.replace_quotes([intent('0.50', '10')])
        fills = book.on_trade(trade('no', '0.50', '14', no='0.50'))
        self.assertEqual(fills[0].size, Decimal('2'))
        self.assertEqual(book.order('MKT', 'yes').queue_ahead, Decimal('0'))
        book.replace_quotes([intent('0.50', '10')])
        kept = book.order('MKT', 'yes')
        self.assertEqual(kept.queue_ahead, Decimal('0'))
        self.assertEqual(kept.intent.size, Decimal('8'))
        self.assertEqual(kept.filled, Decimal('0'))

    def test_a_fully_filled_order_is_replaced_at_the_back(self):
        book = rails.QueueInstrument(queue_ahead_contracts='10')
        book.replace_quotes([intent('0.50', '4')])
        fills = book.on_trade(trade('no', '0.50', '18', no='0.50'))
        self.assertEqual(fills[0].size, Decimal('4'))
        self.assertEqual(book.order('MKT', 'yes').queue_ahead, Decimal('0'))
        book.replace_quotes([intent('0.50', '7')])
        replaced = book.order('MKT', 'yes')
        self.assertEqual(replaced.queue_ahead, Decimal('10'))
        self.assertEqual(replaced.intent.size, Decimal('7'))
        self.assertEqual(replaced.filled, Decimal('0'))

    def test_a_duplicate_quote_leaves_the_previous_map(self):
        book = rails.QueueInstrument(queue_model='front')
        book.replace_quotes([intent('0.50', '10')])
        with self.assertRaises(ValueError):
            book.replace_quotes([intent('0.50', '10'), intent('0.49', '10')])
        self.assertEqual(book.order('MKT', 'yes').intent.price, Decimal('0.50'))

    def test_a_new_order_on_an_empty_map_starts_at_the_back(self):
        book = rails.QueueInstrument(queue_ahead_contracts=rails.STRESS_QUEUE_AHEAD)
        book.replace_quotes([intent('0.50', '10')])
        self.assertEqual(book.order('MKT', 'yes').queue_ahead, Decimal('10000'))

    def test_omitting_a_key_cancels_it(self):
        book = rails.QueueInstrument(queue_model='front')
        book.replace_quotes([intent('0.50', '10', outcome='yes'), intent('0.50', '10', outcome='no')])
        book.replace_quotes([intent('0.50', '10', outcome='yes')])
        self.assertIsNone(book.order('MKT', 'no'))
        self.assertIsNotNone(book.order('MKT', 'yes'))

    def test_a_taker_intent_is_not_rested(self):
        book = rails.QueueInstrument(queue_model='front')
        book.replace_quotes([intent('0.50', '10', kind='taker'), intent('0.50', '10', outcome='no')])
        self.assertIsNone(book.order('MKT', 'yes'))
        self.assertEqual(book.order('MKT', 'no').intent.kind, 'maker')

    def test_a_refused_replacement_leaves_the_previous_map(self):
        book = rails.QueueInstrument(queue_model='front')
        book.replace_quotes([intent('0.50', '10')])
        with self.assertRaises(rails.MakerCreditRefused):
            book.replace_quotes([intent('0.01', '1')])
        self.assertEqual(book.order('MKT', 'yes').intent.price, Decimal('0.50'))
        self.assertEqual(book.order('MKT', 'yes').intent.size, Decimal('10'))


class PartialMakerFeeTests(unittest.TestCase):
    def test_fill_fee_uses_the_unrounded_maker_path(self):
        book = rails.QueueInstrument(queue_model='front')
        book.replace_quotes([intent('0.50', '1')])
        fills = book.on_trade(trade('no', '0.50', '2', no='0.50', at='t1'))
        self.assertEqual(fills[0].size, Decimal('1'))
        self.assertFalse(fills[0].fee_quote['rounded_up'])
        self.assertEqual(fills[0].fee_quote['formula_id'], rails.feebook.EXAMINER_FORMULA_ID)
        self.assertEqual(fills[0].fee, Decimal('0.004375'))
        self.assertEqual(fills[0].at, 't1')
        ceiled = rails.feebook.order_fee('maker', '1', '0.50', round_up=True)['fee']
        self.assertEqual(ceiled, Decimal('0.01'))
        self.assertGreater(ceiled, fills[0].fee)

    def test_three_partials_sum_to_the_order_raw(self):
        book = rails.QueueInstrument(queue_model='front', fill_participation='1')
        book.replace_quotes([intent('0.50', '3')])
        fees = []
        for _ in range(3):
            fills = book.on_trade(trade('no', '0.50', '1', no='0.50'))
            self.assertEqual(fills[0].size, Decimal('1'))
            fees.append(fills[0].fee)
        self.assertEqual(sum(fees, Decimal('0')), Decimal('0.013125'))
        whole = rails.feebook.order_fee('maker', '3', '0.50', round_up=True)
        self.assertEqual(whole['raw'], Decimal('0.013125'))
        self.assertEqual(whole['fee'], Decimal('0.02'))


class FeeCreditFloorTests(unittest.TestCase):
    def test_predeclared_rows(self):
        admitted = [
            ('1', '0.50', Decimal('0.01'), Decimal('0.49')),
            ('1', '0.02', Decimal('0.01'), Decimal('0.01')),
        ]
        refused = [
            ('1', '0.015', Decimal('0.01'), Decimal('0.00')),
            ('1', '0.01', Decimal('0.01'), Decimal('0.00')),
        ]
        for contracts, price, fee, credit in admitted:
            row = rails.admit_maker_quote(price, contracts)
            self.assertEqual(row['rule_id'], rails.FEE_CREDIT_RULE_ID)
            self.assertTrue(row['fee_quote']['rounded_up'])
            self.assertEqual(row['fee'], fee)
            self.assertEqual(row['credit'], credit)
        for contracts, price, fee, credit in refused:
            with self.assertRaises(rails.MakerCreditRefused) as caught:
                rails.admit_maker_quote(price, contracts)
            evaluation = caught.exception.evaluation
            self.assertEqual(evaluation['fee'], fee)
            self.assertEqual(evaluation['credit'], credit)
            self.assertFalse(evaluation['admitted'])

    def test_fee_blind_cash_would_admit_the_one_cent_quote(self):
        with self.assertRaises(rails.MakerCreditRefused) as caught:
            rails.admit_maker_quote('0.01', '1')
        evaluation = caught.exception.evaluation
        self.assertEqual(evaluation['fee_blind_credit'], Decimal('0.01'))
        self.assertEqual(evaluation['credit'], Decimal('0.00'))
        self.assertGreater(evaluation['fee_blind_credit'], evaluation['credit'])

    def test_a_disabled_maker_fee_is_evaluated_and_can_admit(self):
        table = rails.feebook.load_series_table()
        table['overrides'] = {'EXAMPLE': {'maker_fees_enabled': False}}
        row = rails.admit_maker_quote('0.01', '1', series='EXAMPLE', table=table)
        self.assertEqual(row['fee'], Decimal('0.00'))
        self.assertEqual(row['fee_quote']['M'], Decimal('0'))
        self.assertEqual(row['credit'], Decimal('0.01'))
        self.assertEqual(row['fee_quote']['series_resolution'], 'override')

    def test_sub_cent_positive_net_still_refuses(self):
        row = rails.maker_quote_credit('0.015', '1')
        self.assertEqual(row['net'], Decimal('0.005'))
        self.assertEqual(row['credit'], Decimal('0.00'))
        self.assertFalse(row['admitted'])


class ContentFreshTests(unittest.TestCase):
    def test_key_order_does_not_change_the_content_token(self):
        left = rails.canonical_book_content({'b': '1', 'a': {'z': 2, 'y': 1}})
        right = rails.canonical_book_content({'a': {'y': 1, 'z': 2}, 'b': '1'})
        self.assertEqual(left, right)
        changed = rails.canonical_book_content({'a': {'y': 1, 'z': 2}, 'b': '2'})
        self.assertNotEqual(left, changed)

    def test_content_or_transaction_time_marks_the_book_fresh(self):
        first = rails.BookObservation('aaa', 'tx-1')
        self.assertEqual(rails.judge_freshness(None, first), rails.Freshness(True, 'initial'))
        same = rails.BookObservation('aaa', 'tx-1')
        self.assertEqual(rails.judge_freshness(first, same), rails.Freshness(False, 'unchanged'))
        content = rails.BookObservation('bbb', 'tx-1')
        self.assertEqual(
            rails.judge_freshness(first, content),
            rails.Freshness(True, 'content_changed'),
        )
        both = rails.BookObservation('bbb', 'tx-2')
        self.assertEqual(
            rails.judge_freshness(first, both),
            rails.Freshness(True, 'content_changed'),
        )
        clock = rails.BookObservation('aaa', 'tx-2')
        self.assertEqual(
            rails.judge_freshness(first, clock),
            rails.Freshness(True, 'transaction_time_changed'),
        )

    def test_keepalive_is_not_a_book_update(self):
        first = rails.BookObservation('aaa', 'tx-1')
        ping = rails.BookObservation('bbb', 'tx-2')
        self.assertEqual(
            rails.judge_freshness(first, ping, keepalive=True),
            rails.Freshness(False, 'keepalive_ignored'),
        )
        self.assertEqual(
            rails.judge_freshness(None, first, keepalive=True),
            rails.Freshness(False, 'keepalive_ignored'),
        )
        local_clocks = ('2026-09-22T22:00:00Z', '2026-09-22T22:00:05Z')
        self.assertEqual(
            rails.judge_freshness(first, rails.BookObservation('aaa', 'tx-1')),
            rails.Freshness(False, 'unchanged'),
        )
        self.assertEqual(len(local_clocks), 2)

    def test_a_string_payload_is_not_treated_as_book_content(self):
        with self.assertRaises(TypeError):
            rails.canonical_book_content('{"a":1}')


class MicroScorecardTests(unittest.TestCase):
    def test_config_pin(self):
        config = rails.load_micro_config()
        pins = json.loads((ROOT / 'SOURCE_PINS.json').read_text())
        self.assertEqual(config['id'], 'micro-tape-v1')
        self.assertEqual(config['hash'], pins['MICRO_V1']['hash'])
        self.assertEqual(config['thinN'], 500)
        self.assertEqual(config['surviveRoi'], 0)
        self.assertTrue(config['skipBlockTrades'])
        self.assertEqual(config['nflInplayHours'], 3.25)
        self.assertEqual(pins['rates']['taker'], 0.07)
        self.assertEqual(pins['rates']['maker'], 0.0175)

    def test_role_fees_follow_the_grok_paper_convention(self):
        maker = rails.role_pnl('yes', '0.50', 'no', 'maker')
        taker = rails.role_pnl('yes', '0.50', 'yes', 'taker')
        self.assertEqual(maker['fee'], Decimal('0.004375'))
        self.assertTrue(maker['win'])
        self.assertEqual(maker['gross'], Decimal('0.50'))
        self.assertEqual(maker['profit'], Decimal('0.495625'))
        self.assertEqual(taker['fee'], Decimal('0.02'))
        self.assertTrue(taker['win'])
        self.assertEqual(taker['gross'], Decimal('0.50'))
        self.assertEqual(taker['profit'], Decimal('0.48'))
        lost = rails.role_pnl('yes', '0.50', 'yes', 'maker')
        self.assertFalse(lost['win'])
        self.assertEqual(lost['gross'], Decimal('-0.50'))
        self.assertEqual(lost['profit'], Decimal('-0.504375'))

    def test_verdict_order(self):
        self.assertEqual(rails.micro_verdict('control', 1, '1', None), 'CONTROL')
        self.assertEqual(rails.micro_verdict('control', 5000, '1', '0'), 'CONTROL')
        self.assertEqual(rails.micro_verdict('challenger', 499, '1', None), 'THIN')
        self.assertEqual(rails.micro_verdict('challenger', 500, None, None), 'FAILS')
        self.assertEqual(rails.micro_verdict('challenger', 500, '0', None), 'FAILS')
        self.assertEqual(rails.micro_verdict('challenger', 500, '0.10', '0.10'), 'FAILS')
        self.assertEqual(rails.micro_verdict('challenger', 500, '0.10', '0.09'), 'SURVIVES')
        self.assertEqual(rails.micro_verdict('challenger', 500, '0.10', None), 'SURVIVES')
        with self.assertRaises(ValueError):
            rails.micro_verdict('strategy', 500, '1', None)

    def test_score_reports_both_rois_and_stays_thin(self):
        prints = [
            {
                'ticker': 'A',
                'taker_side': 'yes',
                'yes_price': '0.10',
                'result': 'yes',
                'size': '1',
                'is_block': False,
            },
            {
                'ticker': 'B',
                'taker_side': 'yes',
                'yes_price': '0.50',
                'result': 'no',
                'size': '9',
            },
            {
                'ticker': 'C',
                'taker_side': 'yes',
                'yes_price': '0.50',
                'result': 'yes',
                'size': '100',
                'is_block': True,
            },
        ]
        scored = rails.score_role(prints, 'maker', 'challenger')
        self.assertEqual(scored['n'], 2)
        self.assertEqual(scored['markets'], 2)
        self.assertEqual(scored['evidence_stage'], 'HISTORICAL_OUT_OF_SAMPLE')
        self.assertTrue(scored['unique_counterparty'])
        self.assertFalse(scored['picker_fields_applied'])
        self.assertEqual(scored['verdict'], 'THIN')
        self.assertNotEqual(scored['one_lot_roi'], scored['size_weighted_roi'])
        self.assertNotIn('pnl', scored)
        self.assertNotIn('completed_profit', scored)
        first = rails.role_pnl('yes', '0.10', 'yes', 'maker')
        second = rails.role_pnl('yes', '0.50', 'no', 'maker')
        net = first['profit'] + second['profit']
        self.assertEqual(scored['one_lot_net'], net)
        self.assertEqual(scored['one_lot_roi'], net / Decimal('2'))
        weighted = first['profit'] * Decimal('1') + second['profit'] * Decimal('9')
        self.assertEqual(scored['size_weighted_net'], weighted)
        self.assertEqual(scored['size_weighted_roi'], weighted / Decimal('10'))

    def test_control_on_a_short_list_stays_control(self):
        prints = [{
            'ticker': 'A',
            'taker_side': 'no',
            'yes_price': '0.40',
            'result': 'no',
            'size': '3',
        }]
        scored = rails.score_role(prints, 'taker', 'control')
        self.assertEqual(scored['verdict'], 'CONTROL')
        self.assertEqual(scored['n'], 1)
        self.assertEqual(scored['counterpart_roi'] is not None, True)

    def test_other_evidence_stages_are_rejected(self):
        with self.assertRaises(ValueError):
            rails.score_role([], 'maker', 'challenger', evidence_stage='FORWARD_PAPER')


class IsolationTests(unittest.TestCase):
    def test_live_adapter_is_absent(self):
        self.assertFalse(hasattr(rails, 'KalshiExecutionAdapter'))

    def test_feebook_source_matches_its_freeze(self):
        frozen = json.loads((FEEBOOK / 'FROZEN_EXPERIMENT.json').read_text())
        digest = hashlib.sha256((FEEBOOK / 'feebook.py').read_bytes()).hexdigest()
        self.assertEqual(digest, frozen['implementation_sha256']['feebook.py'])

    def test_hypothesis_spec_matches_its_freeze(self):
        frozen = json.loads((ROOT / 'FROZEN_EXPERIMENT.json').read_text())
        digest = hashlib.sha256((ROOT / 'EXPERIMENT_SPEC.md').read_bytes()).hexdigest()
        self.assertEqual(digest, frozen['specification_sha256']['EXPERIMENT_SPEC.md'])
        self.assertIsNone(frozen['results'])
        self.assertIsNone(frozen['pnl'])


if __name__ == '__main__':
    unittest.main()
