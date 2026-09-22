"""Unit pins for the Q6-000 queue-fragility arms.

Synthetic prints check rails queue parameters and the fixed examiner channel.
They are not a historical walk and they are not profit.
"""
import hashlib
import inspect
import json
import subprocess
import sys
import unittest
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(PARENT / 'kalshi_feebook_lab_20260922'))
sys.path.insert(0, str(PARENT / 'kalshi_rails_lab_20260922'))

import feebook
import queue_fragility as qf
import rails


def _intent(price, size, outcome='yes', ticker='MKT'):
    return rails.QuoteIntent(ticker, outcome, Decimal(price), Decimal(size))


def _trade(size, taker_side='no', yes_price='0.40', ticker='MKT'):
    return {
        'ticker': ticker,
        'taker_side': taker_side,
        'yes_price': yes_price,
        'size': size,
        'created_time': 't0',
    }


def _rails_fill(queue_ahead, model, volume, remaining, participation):
    """The R1-P5 one-print rule, restated so the lab can be checked against it."""
    ahead = Decimal('0') if model == 'front' else queue_ahead
    consumed = min(ahead, volume)
    post = volume - consumed
    return min(remaining, post * participation), consumed


class PinTests(unittest.TestCase):
    def test_arms_differ_only_in_rails_queue_params(self):
        books = {}
        fees = []
        for arm in qf.ARMS:
            params = qf.arm_queue_params(arm)
            self.assertEqual(set(params), set(qf.QUEUE_PARAM_KEYS))
            book = qf.open_instrument(arm)
            books[arm] = book
            self.assertEqual(book.queue_ahead_contracts, params['queue_ahead_contracts'])
            self.assertEqual(book.fill_participation, params['fill_participation'])
            self.assertEqual(book.queue_model, params['queue_model'])
            self.assertEqual(book.fill_participation, rails.FILL_PARTICIPATION_DEFAULT)
            self.assertIsNone(book.series)
            self.assertIsNone(book.table)
            fees.append(qf.feebook_binding())
        self.assertEqual(fees[0], fees[1])
        self.assertEqual(fees[1], fees[2])
        self.assertEqual(qf.queue_param_changes(qf.QF0, qf.QF1), ('queue_ahead_contracts',))
        self.assertEqual(
            qf.queue_param_changes(qf.QF0, qf.QF2),
            ('queue_ahead_contracts', 'queue_model'),
        )
        self.assertEqual(
            qf.queue_param_changes(qf.QF1, qf.QF2),
            ('queue_ahead_contracts', 'queue_model'),
        )
        self.assertEqual(books[qf.QF0].queue_ahead_contracts, rails.scenario_queue('q3300'))
        self.assertEqual(books[qf.QF0].queue_ahead_contracts, rails.QUEUE_AHEAD_DEFAULT)
        self.assertEqual(books[qf.QF0].queue_model, 'measured')
        self.assertEqual(books[qf.QF1].queue_ahead_contracts, rails.scenario_queue('q10000'))
        self.assertEqual(books[qf.QF1].queue_ahead_contracts, rails.STRESS_QUEUE_AHEAD)
        self.assertEqual(books[qf.QF1].queue_model, 'measured')
        self.assertEqual(books[qf.QF2].queue_model, 'front')
        self.assertEqual(books[qf.QF2].queue_ahead_contracts, Decimal('0'))
        self.assertEqual(inspect.signature(qf.open_instrument).parameters.keys(), {'arm'})
        binding = qf.instrument_binding()
        self.assertEqual(binding['fee'], fees[0])
        self.assertIs(binding['fee_is_knob'], False)
        self.assertEqual(binding['knob'], 'queue_fill_stress_only')

    def test_feebook_binding_is_the_examiner_channel_on_every_arm(self):
        binding = qf.feebook_binding()
        self.assertEqual(Path(feebook.__file__).resolve().parent.name, 'kalshi_feebook_lab_20260922')
        self.assertEqual(Path(rails.__file__).resolve().parent.name, 'kalshi_rails_lab_20260922')
        self.assertEqual(binding['commit'], '22371178cb2663250b4762f328069571c48cb551')
        self.assertEqual(binding['formula_id'], feebook.EXAMINER_FORMULA_ID)
        self.assertEqual(binding['formula_id'], 'astra.r1p1.feebook.claude_order_level_ceil.v1')
        self.assertNotEqual(binding['formula_id'], binding['comparator_formula_id'])
        self.assertNotEqual(binding['comparator_formula_id'], feebook.EXAMINER_FORMULA_ID)
        rates = feebook.load_series_table()['rates']
        self.assertEqual(binding['maker_rate'], feebook.as_decimal(rates['maker'], 'maker'))
        self.assertEqual(binding['taker_rate'], feebook.as_decimal(rates['taker'], 'taker'))
        self.assertIs(binding['maker_fees_enabled'], True)
        self.assertIs(binding['fill_round_up'], False)
        self.assertIs(binding['admission_round_up'], True)
        self.assertIs(binding['fee_is_knob'], False)
        for arm in qf.ARMS:
            self.assertEqual(qf.feebook_binding(), binding)
            book = qf.open_instrument(arm)
            with self.assertRaises(rails.MakerCreditRefused):
                book.replace_quotes([_intent('0.01', '1')])

    def test_pinned_labs_match_their_commits_and_stay_unedited(self):
        for commit, path in (
            (qf.FEEBOOK_COMMIT, 'kalshi_feebook_lab_20260922'),
            (qf.RAILS_COMMIT, 'kalshi_rails_lab_20260922'),
        ):
            proc = subprocess.run(
                ['git', 'diff', '--exit-code', commit, '--', path],
                cwd=PARENT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        frozen = json.loads(qf.FROZEN_EXPERIMENT.read_text())
        names = subprocess.run(
            ['git', 'diff', '--name-only', qf.PRIOR_R2P1_MERGE],
            cwd=PARENT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(names.returncode, 0, names.stderr)
        changed = set(names.stdout.split())
        sibling_pin = set(frozen['r2p1_sibling_pin_files'])
        for path in frozen['does_not_modify']:
            hits = {item for item in changed if item == path or item.startswith(path + '/')}
            if path == 'kalshi_r2p1_hygiene_000_lab_20260922':
                self.assertTrue(hits <= sibling_pin, hits - sibling_pin)
            else:
                self.assertEqual(hits, set())
        ancestor = subprocess.run(
            ['git', 'merge-base', '--is-ancestor', qf.PRIOR_R2P1_MERGE, 'HEAD'],
            cwd=PARENT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(ancestor.returncode, 0, ancestor.stderr)

    def test_shadow_fee_literals_are_absent_from_source(self):
        source = (ROOT / 'queue_fragility.py').read_text()
        for banned in (
            'maker_coefficient',
            'taker_coefficient',
            'common_config',
            '0.0175',
            '0.07',
            '.0175',
            "Decimal('3300')",
            "Decimal('10000')",
            "Decimal('0.5')",
            'round_up=',
            'replay_v2',
            'factorial_policy',
            'paircheck_policy',
            'capital_structure',
            'class KalshiExecutionAdapter',
            'grok_unrounded',
            'role_pnl',
            'score_role',
        ):
            self.assertNotIn(banned, source)

    def test_freeze_packet_and_empty_results_stay_null(self):
        frozen = json.loads(qf.FROZEN_EXPERIMENT.read_text())
        empty = json.loads(qf.EMPTY_RESULTS.read_text())
        packet = (ROOT / 'QUEUE_FRAGILITY_000_R1P5_FREEZE_2026-09-22.md').read_bytes()
        self.assertEqual(qf.sha256_file(qf.PACKET), qf.PACKET_SHA256)
        self.assertEqual(hashlib.sha256(packet).hexdigest(), qf.PACKET_SHA256)
        self.assertEqual(frozen['packet_sha256'], qf.PACKET_SHA256)
        self.assertEqual(frozen['fee_fixed'], 'kalshi_feebook_lab_20260922@22371178cb2663250b4762f328069571c48cb551')
        self.assertEqual(frozen['rails_knob'], 'kalshi_rails_lab_20260922@6a28e0d6254327ea4e6451c781bec56215ac6cac')
        self.assertEqual(frozen['knob'], 'queue_fill_stress_only')
        self.assertEqual(frozen['arms'], list(qf.ARMS))
        self.assertEqual(frozen['strategy_pointer'], 'Q6-000')
        self.assertEqual(frozen['status'], 'FROZEN_NOT_RUN')
        self.assertIs(frozen['forbid_capital_A2_A3'], True)
        self.assertIs(frozen['forbid_000_retune'], True)
        self.assertIs(frozen['live_orders'], False)
        self.assertIs(frozen['forbid_shadow_fee_literals'], True)
        self.assertIs(frozen['fee_is_knob'], False)
        self.assertIs(frozen['signal_retune'], False)
        for key in ('results', 'pnl', *qf.OUTPUT_KEYS):
            self.assertIsNone(frozen[key])
            self.assertIsNone(empty[key])
        self.assertEqual(empty['status'], 'NOT_RUN')
        self.assertEqual(qf.frozen_output_snapshot()['pnl'], None)
        self.assertEqual(qf.sha256_file(qf.SHADOW_FREEZE), frozen['shadow_freeze_sha256'])
        self.assertEqual(qf.sha256_file(qf.TAPE_MANIFEST), frozen['tape_manifest_sha256'])
        shadow = json.loads(qf.SHADOW_FREEZE.read_text())
        self.assertEqual(shadow['selected'], '000')
        self.assertEqual(len(qf.development_cohort_event_ids()), 31)
        self.assertNotIn('common_config', (ROOT / 'queue_fragility.py').read_text())

    def test_capital_is_shared_a1_only(self):
        pool = qf.shared_capital()
        self.assertEqual(pool['mode'], 'A1_shared_pool')
        self.assertEqual(pool['C_total_usd'], Decimal('5000'))
        self.assertIs(pool['shared_pool'], True)
        self.assertIs(pool['a2_reopened'], False)
        self.assertIs(pool['a3_reopened'], False)
        for mode in qf.FORBIDDEN_CAPITAL_MODES:
            with self.assertRaises(qf.CapitalArmForbidden):
                qf.shared_capital(mode)
        with self.assertRaises(qf.CapitalArmForbidden):
            qf.shared_capital('A2')

    def test_live_orders_and_historical_net_are_refused(self):
        with self.assertRaises(qf.LiveOrdersForbidden):
            qf.execution_adapter()
        with self.assertRaises(qf.QueueFragilityError):
            qf.historical_completed_net()


class InstrumentTests(unittest.TestCase):
    def test_one_print_matches_the_rails_fill_rule_and_shares_the_fee(self):
        remaining = Decimal('10000')
        volume = Decimal('4000')
        participation = rails.FILL_PARTICIPATION_DEFAULT
        intents = [_intent('0.40', '10000')]
        trades = [_trade('4000')]
        expected = {}
        for arm in qf.ARMS:
            params = qf.arm_queue_params(arm)
            got, consumed = _rails_fill(
                params['queue_ahead_contracts'],
                params['queue_model'],
                volume,
                remaining,
                participation,
            )
            measured = qf.measure_arm(arm, intents, trades)
            expected[arm] = (got, consumed)
            self.assertEqual(measured['filled'], got)
            self.assertEqual(measured['adverse_queue_exposure'], consumed)
            self.assertEqual(measured['requested'], remaining)
            self.assertEqual(measured['fill_rate'], got / remaining)
            self.assertEqual(measured['eligible_volume'], volume)
            self.assertIsNone(measured['pnl'])
            self.assertIsNone(measured['results'])
            if got == 0:
                self.assertEqual(measured['fills'], ())
            else:
                self.assertEqual(len(measured['fills']), 1)
                fill = measured['fills'][0]
                quote = feebook.order_fee('maker', got, Decimal('0.40'), round_up=False)
                self.assertEqual(fill['formula_id'], feebook.EXAMINER_FORMULA_ID)
                self.assertEqual(fill['formula_id'], qf.feebook_binding()['formula_id'])
                self.assertEqual(fill['rate'], qf.feebook_binding()['maker_rate'])
                self.assertEqual(fill['rate'], quote['rate'])
                self.assertIs(fill['rounded_up'], False)
                self.assertEqual(fill['fee'], quote['fee'])
                self.assertNotEqual(fill['formula_id'], feebook.GROK_COMPARATOR_FORMULA_ID)
        self.assertGreater(expected[qf.QF2][0], expected[qf.QF0][0])
        self.assertGreater(expected[qf.QF0][0], expected[qf.QF1][0])
        self.assertEqual(expected[qf.QF1][0], Decimal('0'))
        self.assertEqual(expected[qf.QF2][1], Decimal('0'))
        self.assertGreater(expected[qf.QF1][1], expected[qf.QF0][1])
        rates = []
        for arm in (qf.QF0, qf.QF2):
            rates.append(qf.measure_arm(arm, intents, trades)['fills'][0]['rate'])
        self.assertEqual(rates[0], rates[1])

    def test_polarity_same_price_keep_and_new_price_back(self):
        ahead = rails.scenario_queue('q3300')
        book = qf.open_instrument(qf.QF0)
        book.replace_quotes([_intent('0.40', '10', 'yes'), _intent('0.60', '10', 'no')])
        burns = book.on_trade(_trade('10', taker_side='yes', yes_price='0.40'))
        self.assertEqual(burns, [])
        self.assertEqual(book.order('MKT', 'no').queue_ahead, ahead - Decimal('10'))
        self.assertEqual(book.order('MKT', 'yes').queue_ahead, ahead)
        self.assertEqual(book.order('MKT', 'yes').filled, Decimal('0'))
        self.assertEqual(book.order('MKT', 'no').filled, Decimal('0'))

        front = qf.open_instrument(qf.QF2)
        front.replace_quotes([_intent('0.40', '10', 'yes'), _intent('0.60', '10', 'no')])
        filled = front.on_trade(_trade('10', taker_side='yes', yes_price='0.40'))
        self.assertEqual(len(filled), 1)
        self.assertEqual(filled[0].outcome, 'no')
        self.assertEqual(filled[0].size, Decimal('10') * rails.FILL_PARTICIPATION_DEFAULT)
        self.assertEqual(filled[0].fee_quote['formula_id'], feebook.EXAMINER_FORMULA_ID)
        self.assertEqual(front.order('MKT', 'yes').filled, Decimal('0'))
        self.assertEqual(front.order('MKT', 'yes').queue_ahead, Decimal('0'))

        kept = qf.open_instrument(qf.QF0)
        kept.replace_quotes([_intent('0.40', '10')])
        self.assertEqual(kept.on_trade(_trade('300')), [])
        consumed_to = ahead - Decimal('300')
        self.assertEqual(kept.order('MKT', 'yes').queue_ahead, consumed_to)
        kept.replace_quotes([_intent('0.40', '99')])
        self.assertEqual(kept.order('MKT', 'yes').queue_ahead, consumed_to)
        self.assertEqual(kept.order('MKT', 'yes').intent.size, Decimal('10'))
        kept.replace_quotes([_intent('0.41', '25')])
        self.assertEqual(kept.order('MKT', 'yes').queue_ahead, ahead)
        self.assertEqual(kept.order('MKT', 'yes').intent.size, Decimal('25'))

        stress = qf.open_instrument(qf.QF1)
        stress.replace_quotes([_intent('0.40', '10')])
        stress.replace_quotes([_intent('0.41', '10')])
        self.assertEqual(stress.order('MKT', 'yes').queue_ahead, rails.STRESS_QUEUE_AHEAD)

        optimistic = qf.open_instrument(qf.QF2)
        optimistic.replace_quotes([_intent('0.40', '10')])
        optimistic.replace_quotes([_intent('0.40', '10')])
        self.assertEqual(optimistic.order('MKT', 'yes').queue_ahead, Decimal('0'))
        optimistic.replace_quotes([_intent('0.55', '4')])
        self.assertEqual(optimistic.order('MKT', 'yes').queue_ahead, Decimal('0'))
        self.assertEqual(optimistic.order('MKT', 'yes').intent.size, Decimal('4'))
        front_book = qf.open_instrument(qf.QF2)
        front_book.replace_quotes(
            [_intent('0.40', '10')],
            book_sizes={('MKT', 'yes'): Decimal('5000')},
        )
        self.assertEqual(front_book.order('MKT', 'yes').queue_ahead, Decimal('0'))
        self.assertEqual(front_book.queue_model, 'front')

    def test_a_price_above_the_bid_does_not_consume_queue(self):
        book = qf.open_instrument(qf.QF0)
        book.replace_quotes([_intent('0.40', '10')])
        before = book.order('MKT', 'yes').queue_ahead
        self.assertEqual(book.on_trade(_trade('100', yes_price='0.50')), [])
        self.assertEqual(book.order('MKT', 'yes').queue_ahead, before)


class PreSettlementTests(unittest.TestCase):
    def _slice(self):
        return [_intent('0.40', '10000')], [_trade('4000')]

    def test_unjoined_outputs_are_null_and_do_not_touch_the_freeze(self):
        before = qf.FROZEN_EXPERIMENT.read_bytes()
        empty_before = qf.EMPTY_RESULTS.read_bytes()
        intents, trades = self._slice()
        blank = qf.pre_settlement_outputs(intents, trades, joined=False)
        self.assertEqual(blank, qf.empty_pre_settlement())
        for key in ('results', 'pnl', *qf.OUTPUT_KEYS):
            self.assertIsNone(blank[key])
        self.assertEqual(blank['status'], qf.NOT_RUN)
        self.assertEqual(qf.pre_settlement_outputs(joined=True), qf.empty_pre_settlement())
        self.assertEqual(qf.FROZEN_EXPERIMENT.read_bytes(), before)
        self.assertEqual(qf.EMPTY_RESULTS.read_bytes(), empty_before)

    def test_synthetic_join_computes_queue_gaps_without_writing_profit(self):
        before = qf.FROZEN_EXPERIMENT.read_bytes()
        empty_before = qf.EMPTY_RESULTS.read_bytes()
        intents, trades = self._slice()
        report = qf.pre_settlement_outputs(intents, trades, joined=True)
        self.assertEqual(report['status'], qf.SYNTHETIC_FIXTURE_ONLY)
        self.assertIsNone(report['results'])
        self.assertIsNone(report['pnl'])
        base = qf.measure_arm(qf.QF0, intents, trades)
        stress = qf.measure_arm(qf.QF1, intents, trades)
        front = qf.measure_arm(qf.QF2, intents, trades)
        self.assertEqual(
            report['fill_rate_delta_vs_q3300'][qf.QF1],
            stress['fill_rate'] - base['fill_rate'],
        )
        self.assertEqual(
            report['fill_rate_delta_vs_q3300'][qf.QF2],
            front['fill_rate'] - base['fill_rate'],
        )
        self.assertLess(report['fill_rate_delta_vs_q3300'][qf.QF1], 0)
        self.assertGreater(report['fill_rate_delta_vs_q3300'][qf.QF2], 0)
        self.assertEqual(set(report['fill_rate_delta_vs_q3300']), {qf.QF1, qf.QF2})
        self.assertEqual(report['adverse_queue_exposure'][qf.QF0], base['adverse_queue_exposure'])
        self.assertEqual(report['adverse_queue_exposure'][qf.QF1], stress['adverse_queue_exposure'])
        self.assertEqual(report['adverse_queue_exposure'][qf.QF2], Decimal('0'))
        self.assertGreater(
            report['adverse_queue_exposure'][qf.QF1],
            report['adverse_queue_exposure'][qf.QF0],
        )
        realized = stress['filled'] / stress['eligible_volume']
        self.assertEqual(
            report['participation_stress_gap'],
            rails.FILL_PARTICIPATION_DEFAULT - realized,
        )
        self.assertEqual(report['participation_stress_gap'], rails.FILL_PARTICIPATION_DEFAULT)
        self.assertEqual(qf.FROZEN_EXPERIMENT.read_bytes(), before)
        self.assertEqual(qf.EMPTY_RESULTS.read_bytes(), empty_before)
        self.assertIsNone(qf.frozen_output_snapshot()['fill_rate_delta_vs_q3300'])
        self.assertIsNone(qf.frozen_output_snapshot()['adverse_queue_exposure'])
        self.assertIsNone(qf.frozen_output_snapshot()['participation_stress_gap'])
        self.assertIsNone(qf.frozen_output_snapshot()['pnl'])
        self.assertIsNone(qf.frozen_output_snapshot()['results'])
