"""Unit pins for the R2-P1 hygiene helpers.

Synthetic rows check fee rounding, freshness, and queue bins. They are not a
historical walk and they are not profit.
"""
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
import hygiene
import rails


def _rate(role):
    rates = feebook.load_series_table()['rates']
    return feebook.as_decimal(rates[role], role)


class PinTests(unittest.TestCase):
    def test_binding_comes_from_feebook_and_rails(self):
        binding = hygiene.instrument_binding()
        self.assertEqual(Path(feebook.__file__).resolve().parent.name, 'kalshi_feebook_lab_20260922')
        self.assertEqual(Path(rails.__file__).resolve().parent.name, 'kalshi_rails_lab_20260922')
        self.assertEqual(binding['experiment_id'], 'r2p1_hygiene_000_20260922')
        self.assertEqual(binding['strategy_pointer'], 'Q6-000')
        self.assertEqual(binding['feebook_commit'], '22371178cb2663250b4762f328069571c48cb551')
        self.assertEqual(binding['rails_commit'], '6a28e0d6254327ea4e6451c781bec56215ac6cac')
        self.assertEqual(binding['examiner_formula_id'], feebook.EXAMINER_FORMULA_ID)
        self.assertEqual(binding['fee_credit_rule_id'], rails.FEE_CREDIT_RULE_ID)
        self.assertEqual(binding['maker_rate'], _rate('maker'))
        self.assertEqual(binding['taker_rate'], _rate('taker'))
        self.assertEqual(binding['primary_queue_ahead'], rails.scenario_queue('q3300'))
        self.assertEqual(binding['stress_queue_ahead'], rails.scenario_queue('q10000'))
        self.assertEqual(binding['primary_queue_ahead'], rails.QUEUE_AHEAD_DEFAULT)
        self.assertEqual(binding['stress_queue_ahead'], rails.STRESS_QUEUE_AHEAD)
        self.assertIs(binding['queue_is_knob'], False)
        self.assertIs(binding['capital_arms_reopened'], False)
        self.assertIs(binding['signal_retune'], False)
        self.assertIs(binding['live_orders'], False)
        self.assertIs(binding['queue_fragility_twin'], False)
        self.assertNotEqual(binding['examiner_formula_id'], binding['comparator_formula_id'])

    def test_pinned_labs_match_their_commits(self):
        for commit, path in (
            (hygiene.FEEBOOK_COMMIT, 'kalshi_feebook_lab_20260922'),
            (hygiene.RAILS_COMMIT, 'kalshi_rails_lab_20260922'),
        ):
            proc = subprocess.run(
                ['git', 'diff', '--exit-code', commit, '--', path],
                cwd=PARENT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)

    def test_shadow_fee_literals_are_absent_from_source(self):
        source = (ROOT / 'hygiene.py').read_text()
        for banned in (
            'maker_coefficient',
            'taker_coefficient',
            'common_config',
            '0.0175',
            '0.07',
            '.0175',
            'factorial_policy',
            'paircheck_policy',
            'replay_v2',
            'class KalshiExecutionAdapter',
            'capital_structure',
        ):
            self.assertNotIn(banned, source)

    def test_freeze_and_empty_results_stay_null(self):
        frozen = json.loads(hygiene.FROZEN_EXPERIMENT.read_text())
        empty = json.loads(hygiene.EMPTY_RESULTS.read_text())
        for key in ('results', 'pnl', *hygiene.OUTPUT_KEYS):
            self.assertIsNone(frozen[key])
            self.assertIsNone(empty[key])
        self.assertEqual(empty['status'], 'NOT_JOINED')
        self.assertEqual(hygiene.frozen_output_snapshot()['pnl'], None)
        self.assertIs(frozen['signal_retune'], False)
        self.assertIs(frozen['capital_structure_reopened'], False)
        self.assertIs(frozen['queue_fragility_twin'], False)
        self.assertIs(frozen['live_orders'], False)
        self.assertIs(frozen['forbid_shadow_fee_literals'], True)
        self.assertEqual(frozen['strategy_pointer'], 'Q6-000')
        self.assertEqual(frozen['admission'], 'Conductor ADMIT R2-P1')

    def test_pin_lock_is_one_lab_and_fee_sensitivity_is_superseded(self):
        frozen = json.loads(hygiene.FROZEN_EXPERIMENT.read_text())
        lock = hygiene.pin_lock()
        self.assertEqual(lock['canonical_freeze'], hygiene.CANONICAL_FREEZE)
        self.assertEqual(
            lock['canonical_freeze'],
            'R2-P1_FEEBOOK_RAILS_HYGIENE_000_FREEZE_2026-09-22.md',
        )
        self.assertEqual(lock['canonical_freeze_sha256_prefix'], 'ddcd4427')
        self.assertTrue(lock['canonical_freeze_sha256_prefix'].startswith('ddcd4427'))
        self.assertEqual(lock['canonical_freeze_bytes'], 'not_in_checkout')
        self.assertEqual(frozen['packet'], lock['canonical_freeze'])
        self.assertEqual(frozen['canonical_freeze_sha256_prefix'], 'ddcd4427')
        self.assertEqual(frozen['canonical_freeze_bytes'], 'not_in_checkout')
        self.assertFalse((ROOT / hygiene.CANONICAL_FREEZE).exists())
        self.assertEqual(lock['fee_sensitivity_000_r1p1'], 'SUPERSEDED_BY_R2-P1')
        self.assertEqual(frozen['fee_sensitivity_000_r1p1'], 'SUPERSEDED_BY_R2-P1')
        self.assertIs(lock['second_lab'], False)
        self.assertIs(frozen['second_lab'], False)
        self.assertIs(lock['fee_treatment_arms_emitted'], False)
        self.assertIs(frozen['fee_treatment_arms_emitted'], False)
        self.assertIs(lock['queue_fragility_twin'], False)
        self.assertEqual(lock['queue_fragility_sibling'], hygiene.QUEUE_FRAGILITY_SIBLING)
        self.assertEqual(
            lock['queue_fragility_sibling'],
            'kalshi_queue_fragility_000_lab_20260922',
        )
        self.assertIs(lock['live_orders'], False)
        for key in ('results', 'pnl', *hygiene.OUTPUT_KEYS):
            self.assertIsNone(lock['scorecard'][key])
            self.assertIsNone(frozen[key])
        for arm in ('FS0', 'FS1', 'FS2'):
            self.assertNotIn(arm, frozen)
        self.assertFalse((PARENT / 'kalshi_fee_sensitivity_000_lab_20260922').exists())
        self.assertEqual(list(PARENT.glob('*fee_sensitivity*')), [])
        sibling = hygiene.QUEUE_FRAGILITY_SIBLING
        underscore = sorted(path.name for path in PARENT.glob('*queue_fragility*'))
        hyphen = sorted(path.name for path in PARENT.glob('*queue-fragility*'))
        self.assertEqual(underscore, [sibling])
        self.assertEqual(hyphen, [])
        self.assertTrue((PARENT / sibling).is_dir())
        labs = sorted(path.name for path in PARENT.glob('kalshi_r2p1_hygiene_000_lab_*'))
        self.assertEqual(labs, ['kalshi_r2p1_hygiene_000_lab_20260922'])

    def test_shadow_manifest_and_cohort_pins(self):
        frozen = json.loads(hygiene.FROZEN_EXPERIMENT.read_text())
        self.assertEqual(hygiene.sha256_file(hygiene.SHADOW_FREEZE), frozen['shadow_freeze_sha256'])
        self.assertEqual(hygiene.sha256_file(hygiene.TAPE_MANIFEST), frozen['tape_manifest_sha256'])
        shadow = json.loads(hygiene.SHADOW_FREEZE.read_text())
        self.assertEqual(shadow['selected'], '000')
        self.assertEqual(len(hygiene.development_cohort_event_ids()), 31)

    def test_live_orders_are_refused(self):
        with self.assertRaises(hygiene.LiveOrdersForbidden):
            hygiene.execution_adapter()


class FeeDeltaTests(unittest.TestCase):
    def test_order_level_examiner_differs_from_inherited_maker_fee(self):
        rate = _rate('maker')
        price = Decimal('0.50')
        contracts = Decimal('1')
        raw = rate * contracts * price * (feebook.ONE - price)
        examiner = feebook.order_fee('maker', contracts, price, round_up=True)
        self.assertEqual(examiner['formula_id'], feebook.EXAMINER_FORMULA_ID)
        self.assertEqual(examiner['fee'], feebook.round_up_to_cent(raw))
        self.assertEqual(examiner['fee'], Decimal('0.01'))
        inherited = hygiene.inherited_order_fee(price, contracts, rate)
        self.assertEqual(inherited['model_id'], hygiene.INHERITED_MODEL_ID)
        self.assertEqual(inherited['fee'], Decimal('0.0044'))
        delta = hygiene.fee_delta('maker', contracts, price, rate, round_up=True)
        self.assertEqual(delta['examiner_fee'], examiner['fee'])
        self.assertEqual(delta['inherited_fee'], inherited['fee'])
        self.assertEqual(delta['fee_delta'], examiner['fee'] - inherited['fee'])
        self.assertNotEqual(delta['examiner_fee'], delta['inherited_fee'])
        self.assertGreater(delta['fee_delta'], 0)
        self.assertEqual(delta['examiner_formula_id'], feebook.EXAMINER_FORMULA_ID)
        self.assertNotEqual(delta['examiner_formula_id'], feebook.GROK_COMPARATOR_FORMULA_ID)

    def test_taker_order_ceiling_differs_from_inherited_nominal(self):
        rate = _rate('taker')
        price = Decimal('0.50')
        contracts = Decimal('1')
        raw = rate * contracts * price * (feebook.ONE - price)
        delta = hygiene.fee_delta('taker', contracts, price, rate, round_up=True)
        self.assertEqual(delta['examiner_fee'], Decimal('0.02'))
        self.assertEqual(delta['examiner_fee'], feebook.round_up_to_cent(raw))
        self.assertEqual(delta['inherited_fee'], raw)
        self.assertEqual(delta['fee_delta'], delta['examiner_fee'] - raw)
        self.assertNotEqual(delta['examiner_fee'], delta['inherited_fee'])

    def test_partial_keeps_raw_examiner_fee_and_still_differs(self):
        rate = _rate('maker')
        price = Decimal('0.50')
        contracts = Decimal('1')
        raw = rate * contracts * price * (feebook.ONE - price)
        partial = hygiene.fee_delta('maker', contracts, price, rate, round_up=False)
        order = hygiene.fee_delta('maker', contracts, price, rate, round_up=True)
        self.assertFalse(partial['round_up'])
        self.assertEqual(partial['examiner_fee'], raw)
        self.assertNotEqual(partial['examiner_fee'], partial['inherited_fee'])
        self.assertNotEqual(partial['examiner_fee'], order['examiner_fee'])
        self.assertEqual(partial['examiner_formula_id'], feebook.EXAMINER_FORMULA_ID)

    def test_inherited_partials_sum_to_the_whole_order(self):
        rate = _rate('maker')
        price = Decimal('0.50')
        state = hygiene.InheritedFeeState()
        parts = [
            hygiene.inherited_order_fee(price, Decimal('1'), rate, state=state)['fee']
            for _ in range(4)
        ]
        whole = hygiene.inherited_order_fee(price, Decimal('4'), rate)['fee']
        self.assertEqual(sum(parts, Decimal('0')), whole)
        self.assertNotEqual(parts[0], parts[-1])

    def test_a_coefficient_other_than_the_feebook_rate_is_refused(self):
        with self.assertRaises(hygiene.InheritedCoefficientRefused):
            hygiene.fee_delta('maker', Decimal('1'), Decimal('0.50'), Decimal('1'))

    def test_floats_are_rejected(self):
        rate = _rate('maker')
        with self.assertRaises(TypeError):
            hygiene.fee_delta('maker', 1.0, Decimal('0.50'), rate)


class RailLabelTests(unittest.TestCase):
    def test_maker_credit_floor_zero_is_refused(self):
        refused = hygiene.maker_credit_floor_zero_refuse(Decimal('0.01'), Decimal('1'))
        admitted = hygiene.maker_credit_floor_zero_refuse(Decimal('0.50'), Decimal('1'))
        self.assertTrue(refused['maker_credit_floor_zero_refuse'])
        self.assertFalse(refused['admitted'])
        self.assertEqual(refused['credit'], Decimal('0.00'))
        self.assertEqual(refused['rule_id'], rails.FEE_CREDIT_RULE_ID)
        self.assertEqual(refused['formula_id'], feebook.EXAMINER_FORMULA_ID)
        self.assertFalse(admitted['maker_credit_floor_zero_refuse'])
        self.assertTrue(admitted['admitted'])
        self.assertGreater(admitted['credit'], 0)

    def test_keepalive_is_not_content_fresh_and_does_not_reset_the_gap(self):
        content_a = rails.canonical_book_content({'yes_dollars': [['0.42', '1']]})
        content_b = rails.canonical_book_content({'yes_dollars': [['0.43', '1']]})
        cursor = hygiene.FreshnessCursor()
        first = cursor.observe(rails.BookObservation(content_a, 'tx-1'), '0')
        self.assertTrue(first['content_fresh_flag'])
        self.assertEqual(first['reason'], 'initial')
        self.assertIsNone(first['freshness_gap_sec'])
        self.assertEqual(cursor.prior_fresh_at, Decimal('0'))

        ping = cursor.observe(rails.BookObservation(content_b, 'tx-2'), '10', keepalive=True)
        self.assertFalse(ping['content_fresh_flag'])
        self.assertEqual(ping['reason'], 'keepalive_ignored')
        self.assertEqual(ping['freshness_gap_sec'], Decimal('10'))
        self.assertEqual(cursor.prior_fresh_at, Decimal('0'))
        self.assertEqual(cursor.previous.content, content_a)

        changed = cursor.observe(rails.BookObservation(content_b, 'tx-2'), '25')
        self.assertTrue(changed['content_fresh_flag'])
        self.assertEqual(changed['reason'], 'content_changed')
        self.assertEqual(changed['freshness_gap_sec'], Decimal('25'))
        self.assertEqual(cursor.prior_fresh_at, Decimal('25'))

        direct = hygiene.content_fresh_flag(
            rails.BookObservation(content_a, 'tx-1'),
            rails.BookObservation(content_b, 'tx-9'),
            keepalive=True,
        )
        self.assertFalse(direct['content_fresh_flag'])
        self.assertEqual(direct['reason'], 'keepalive_ignored')

    def test_queue_bin_mismatch_uses_the_fixed_rails_scenarios(self):
        primary = rails.scenario_queue('q3300')
        stress = rails.scenario_queue('q10000')
        match = hygiene.queue_bin_mismatch(primary, 'q3300')
        crossed = hygiene.queue_bin_mismatch(stress, 'q3300')
        outside = hygiene.queue_bin_mismatch(primary + Decimal('1'), 'q3300')
        self.assertEqual(match['queue_attribution_bin'], 'q3300')
        self.assertFalse(match['queue_bin_mismatch'])
        self.assertEqual(crossed['queue_attribution_bin'], 'q10000')
        self.assertTrue(crossed['queue_bin_mismatch'])
        self.assertEqual(outside['queue_attribution_bin'], hygiene.OUTSIDE_BIN)
        self.assertTrue(outside['queue_bin_mismatch'])
        self.assertEqual(hygiene.queue_attribution_bin(stress), 'q10000')
        before = rails.QUEUE_AHEAD_DEFAULT
        hygiene.queue_bin_mismatch(stress, 'q10000')
        self.assertEqual(rails.QUEUE_AHEAD_DEFAULT, before)
        self.assertEqual(rails.scenario_queue('q3300'), rails.scenario_queue('q3300'))
        with self.assertRaises(ValueError):
            hygiene.queue_bin_mismatch(primary, 'q5000')


class PreSettlementTests(unittest.TestCase):
    def _row(self, queue_ahead, assumed, gap, price=Decimal('0.50')):
        rate = _rate('maker')
        content = rails.canonical_book_content({'bid': format(price, 'f')})
        return hygiene.label_fill(
            role='maker',
            contracts=Decimal('1'),
            price=price,
            coefficient=rate,
            assumed_scenario=assumed,
            queue_ahead=queue_ahead,
            round_up=True,
            current_book=rails.BookObservation(content, 'tx'),
            observed_at=Decimal('40'),
            prior_fresh_at=Decimal('40') - gap,
        )

    def test_unjoined_outputs_are_null(self):
        row = self._row(rails.scenario_queue('q3300'), 'q3300', Decimal('5'))
        blank = hygiene.pre_settlement_outputs([row], joined=False)
        self.assertEqual(blank, hygiene.empty_pre_settlement())
        for key in ('results', 'pnl', *hygiene.OUTPUT_KEYS):
            self.assertIsNone(blank[key])
        self.assertEqual(blank['status'], hygiene.NOT_JOINED)
        self.assertIsNone(hygiene.pre_settlement_outputs(joined=True)['fee_delta_vs_inherited_model'])

    def test_synthetic_join_computes_helpers_without_touching_the_freeze(self):
        before = hygiene.FROZEN_EXPERIMENT.read_bytes()
        empty_before = hygiene.EMPTY_RESULTS.read_bytes()
        rows = [
            self._row(rails.scenario_queue('q3300'), 'q3300', Decimal('5')),
            self._row(rails.scenario_queue('q10000'), 'q3300', Decimal('12')),
        ]
        report = hygiene.pre_settlement_outputs(rows, joined=True)
        self.assertEqual(report['status'], hygiene.SYNTHETIC_FIXTURE_ONLY)
        self.assertIsNone(report['results'])
        self.assertIsNone(report['pnl'])
        self.assertEqual(report['fee_delta_vs_inherited_model'], rows[0]['fee_delta'] + rows[1]['fee_delta'])
        self.assertGreater(report['fee_delta_vs_inherited_model'], 0)
        self.assertEqual(report['freshness_gap_sec'], Decimal('12'))
        self.assertEqual(report['queue_bin_mismatch_rate'], Decimal('1') / Decimal('2'))
        self.assertFalse(rows[0]['queue_bin_mismatch'])
        self.assertTrue(rows[1]['queue_bin_mismatch'])
        self.assertFalse(rows[0]['maker_credit_floor_zero_refuse'])
        self.assertTrue(rows[0]['content_fresh_flag'])
        self.assertIsNone(rows[0]['pnl'])
        self.assertEqual(hygiene.FROZEN_EXPERIMENT.read_bytes(), before)
        self.assertEqual(hygiene.EMPTY_RESULTS.read_bytes(), empty_before)
        self.assertIsNone(hygiene.frozen_output_snapshot()['fee_delta_vs_inherited_model'])
        self.assertIsNone(hygiene.frozen_output_snapshot()['freshness_gap_sec'])
        self.assertIsNone(hygiene.frozen_output_snapshot()['queue_bin_mismatch_rate'])
        self.assertIsNone(hygiene.frozen_output_snapshot()['pnl'])
        self.assertIsNone(hygiene.frozen_output_snapshot()['results'])

    def test_historical_completed_net_is_not_computed(self):
        with self.assertRaises(hygiene.HygieneError):
            hygiene.historical_completed_net()

    def test_completed_profit_still_requires_the_examiner_channel(self):
        taker = feebook.order_fee('taker', Decimal('1'), Decimal('0.50'), round_up=True)
        maker = feebook.order_fee('maker', Decimal('1'), Decimal('0.50'), round_up=True)
        channel = feebook.examiner_fee_channel(taker, maker)
        self.assertEqual(
            hygiene.classify_rescore({'fee_channel': channel, 'inventory_flat': True}),
            'completed_profit',
        )
        grok = feebook.grok_unrounded_maker_per_unit(Decimal('0.50'))
        with self.assertRaises(feebook.CompletedProfitRefused):
            hygiene.classify_rescore({
                'fee_channel': {
                    'formula_id': grok['formula_id'],
                    'taker_fee': '0.01',
                    'maker_fee': format(grok['fee'], 'f'),
                },
            })
        self.assertIsNone(json.loads(hygiene.FROZEN_EXPERIMENT.read_text())['pnl'])
