"""Unit pins for the Q6-000 fixture join.

Synthetic rows exercise the hygiene helpers. They are not a historical walk
and they are not profit. Freeze outputs stay null.
"""
import gzip
import json
import subprocess
import sys
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(PARENT / 'kalshi_feebook_lab_20260922'))
sys.path.insert(0, str(PARENT / 'kalshi_rails_lab_20260922'))
sys.path.insert(0, str(PARENT / 'kalshi_r2p1_hygiene_000_lab_20260922'))

import feebook
import fixture_join
import hygiene
import rails


def _rate(role):
    rates = feebook.load_series_table()['rates']
    return feebook.as_decimal(rates[role], role)


class PinTests(unittest.TestCase):
    def test_binding_imports_feebook_rails_and_hygiene(self):
        binding = fixture_join.instrument_binding()
        self.assertEqual(Path(feebook.__file__).resolve().parent.name, 'kalshi_feebook_lab_20260922')
        self.assertEqual(Path(rails.__file__).resolve().parent.name, 'kalshi_rails_lab_20260922')
        self.assertEqual(Path(hygiene.__file__).resolve().parent.name, 'kalshi_r2p1_hygiene_000_lab_20260922')
        self.assertEqual(binding['experiment_id'], 'R2-P1_fixture_join_000_20260922')
        self.assertEqual(binding['pick'], 'A')
        self.assertEqual(binding['strategy_pointer'], 'Q6-000')
        self.assertEqual(binding['feebook_commit'], '22371178cb2663250b4762f328069571c48cb551')
        self.assertEqual(binding['rails_commit'], '6a28e0d6254327ea4e6451c781bec56215ac6cac')
        self.assertEqual(binding['hygiene_commit'], 'c33af159d00c07f2d66b2f93174cfcdb4cde8d37')
        self.assertEqual(binding['hygiene_lab_merge'], '25ec05381207252abb8abec8f6f99e30765f9704')
        self.assertEqual(binding['examiner_formula_id'], feebook.EXAMINER_FORMULA_ID)
        self.assertEqual(binding['fee_credit_rule_id'], rails.FEE_CREDIT_RULE_ID)
        self.assertEqual(binding['inherited_model_id'], hygiene.INHERITED_MODEL_ID)
        self.assertIs(binding['live_orders'], False)
        self.assertIs(binding['signal_retune'], False)
        self.assertIs(binding['forbid_capital_A2_A3'], True)
        self.assertEqual(binding['deferred_pick_B'], 'queue_fragility_fixture_join')
        self.assertEqual(binding['stress_role'], fixture_join.STRESS_ROLE)

    def test_pinned_labs_match_their_commits(self):
        for commit, path in (
            (fixture_join.FEEBOOK_COMMIT, 'kalshi_feebook_lab_20260922'),
            (fixture_join.RAILS_COMMIT, 'kalshi_rails_lab_20260922'),
            (fixture_join.HYGIENE_COMMIT, 'kalshi_r2p1_hygiene_000_lab_20260922'),
            (fixture_join.HYGIENE_COMMIT, 'kalshi_queue_fragility_000_lab_20260922'),
            (fixture_join.HYGIENE_COMMIT, 'kalshi_capital_structure_lab_20260922'),
            (fixture_join.HYGIENE_COMMIT, 'nfl_factorial_lab_20260921'),
            (fixture_join.HYGIENE_COMMIT, 'nfl_paircheck_lab_20260922'),
        ):
            proc = subprocess.run(
                ['git', 'diff', '--exit-code', commit, '--', path],
                cwd=PARENT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)

    def test_packet_sha_and_pick_a(self):
        self.assertEqual(fixture_join.sha256_file(fixture_join.PACKET), fixture_join.PACKET_SHA256)
        self.assertTrue(fixture_join.PACKET_SHA256.startswith('e9bac91c'))
        frozen = json.loads(fixture_join.FROZEN_EXPERIMENT.read_text())
        packet = json.loads(fixture_join.PACKET_FROZEN.read_text())
        kernel = json.loads((PARENT / 'packets' / 'R2-P1_FIXTURE_JOIN_000' / 'freeze.json').read_text())
        self.assertEqual(frozen['pick'], 'A')
        self.assertEqual(packet['pick'], 'A')
        self.assertEqual(kernel['pick'], 'A')
        self.assertEqual(frozen['packet_sha256'], fixture_join.PACKET_SHA256)
        self.assertEqual(kernel['packet_sha256'], fixture_join.PACKET_SHA256)
        self.assertEqual(frozen['deferred_pick_B'], 'queue_fragility_fixture_join')
        self.assertIs(frozen['forbid_000_retune'], True)
        self.assertIs(frozen['forbid_capital_A2_A3'], True)
        self.assertIs(frozen['live_orders'], False)

    def test_freeze_outputs_stay_null(self):
        frozen = json.loads(fixture_join.FROZEN_EXPERIMENT.read_text())
        empty = json.loads(fixture_join.EMPTY_RESULTS.read_text())
        packet_results = json.loads(fixture_join.PACKET_RESULTS.read_text())
        packet_frozen = json.loads(fixture_join.PACKET_FROZEN.read_text())
        hygiene_frozen = json.loads(hygiene.FROZEN_EXPERIMENT.read_text())
        for payload in (frozen, empty, packet_results, packet_frozen, hygiene_frozen):
            for key in fixture_join.OUTPUT_KEYS:
                self.assertIsNone(payload[key])
        self.assertEqual(empty['status'], 'NOT_RUN')
        self.assertEqual(empty['pick'], 'A')
        self.assertEqual(packet_results, empty)

    def test_production_pin_matches_the_delivery_manifest(self):
        manifest = json.loads((PARENT / 'nfl_factorial_lab_20260921' / 'DELIVERY_MANIFEST.json').read_text())
        by_path = {item['path']: item for item in manifest['files']}
        expected = {
            'results/q3300_d0.25_000_fills.jsonl.gz': fixture_join.PRIMARY_FILLS_SHA256,
            'results/q3300_d0.25_000_orders.jsonl.gz': fixture_join.PRIMARY_ORDERS_SHA256,
            'results/q10000_d0.25_000_fills.jsonl.gz': fixture_join.STRESS_FILLS_SHA256,
            'results/q10000_d0.25_000_orders.jsonl.gz': fixture_join.STRESS_ORDERS_SHA256,
        }
        for path, digest in expected.items():
            self.assertEqual(by_path[path]['sha256'], digest)
        self.assertEqual(fixture_join.PRIMARY_FILLS_REL.endswith('q3300_d0.25_000_fills.jsonl.gz'), True)
        pin = (ROOT / 'fixtures' / 'PIN.md').read_text()
        self.assertIn(fixture_join.PRIMARY_FILLS_REL, pin)
        self.assertIn(fixture_join.PRIMARY_FILLS_SHA256, pin)
        self.assertIn(fixture_join.STRESS_ROLE, (ROOT / 'fixture_join.py').read_text())

    def test_shadow_fee_literals_are_absent_from_the_harness(self):
        source = (ROOT / 'fixture_join.py').read_text()
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
            'completed_strategy_pnl',
            "Decimal('3300')",
            "Decimal('10000')",
            'import queue_fragility',
        ):
            self.assertNotIn(banned, source)

    def test_live_orders_are_refused(self):
        with self.assertRaises(hygiene.LiveOrdersForbidden):
            fixture_join.execution_adapter()


class JoinTests(unittest.TestCase):
    def setUp(self):
        self.frozen_before = fixture_join.FROZEN_EXPERIMENT.read_bytes()
        self.empty_before = fixture_join.EMPTY_RESULTS.read_bytes()
        self.packet_results_before = fixture_join.PACKET_RESULTS.read_bytes()
        self.packet_frozen_before = fixture_join.PACKET_FROZEN.read_bytes()
        self.hygiene_before = hygiene.FROZEN_EXPERIMENT.read_bytes()
        self.hygiene_empty_before = hygiene.EMPTY_RESULTS.read_bytes()

    def tearDown(self):
        self.assertEqual(fixture_join.FROZEN_EXPERIMENT.read_bytes(), self.frozen_before)
        self.assertEqual(fixture_join.EMPTY_RESULTS.read_bytes(), self.empty_before)
        self.assertEqual(fixture_join.PACKET_RESULTS.read_bytes(), self.packet_results_before)
        self.assertEqual(fixture_join.PACKET_FROZEN.read_bytes(), self.packet_frozen_before)
        self.assertEqual(hygiene.FROZEN_EXPERIMENT.read_bytes(), self.hygiene_before)
        self.assertEqual(hygiene.EMPTY_RESULTS.read_bytes(), self.hygiene_empty_before)

    def _synthetic(self):
        return fixture_join.join_ledgers(
            fixture_join.SYNTHETIC_FILLS,
            fixture_join.SYNTHETIC_ORDERS,
            source='synthetic_schema_standin',
        )

    def test_resolver_uses_the_stand_in_when_the_gzip_is_absent(self):
        choice = fixture_join.resolve_primary()
        if fixture_join.production_present():
            self.assertEqual(choice['source'], 'production_pin')
            self.assertEqual(fixture_join.sha256_file(fixture_join.PRIMARY_FILLS), fixture_join.PRIMARY_FILLS_SHA256)
            self.assertEqual(fixture_join.sha256_file(fixture_join.PRIMARY_ORDERS), fixture_join.PRIMARY_ORDERS_SHA256)
        else:
            self.assertFalse(choice['production_present'])
            self.assertEqual(choice['source'], 'synthetic_schema_standin')
            self.assertEqual(choice['fills_path'], fixture_join.SYNTHETIC_FILLS)
            self.assertEqual(choice['orders_path'], fixture_join.SYNTHETIC_ORDERS)
            self.assertFalse(fixture_join.PRIMARY_FILLS.exists())
            self.assertFalse(fixture_join.PRIMARY_ORDERS.exists())

    def test_synthetic_rows_use_the_factorial_schema(self):
        fills = fixture_join.load_jsonl(fixture_join.SYNTHETIC_FILLS)
        orders = fixture_join.load_jsonl(fixture_join.SYNTHETIC_ORDERS)
        for row in fills:
            for key in fixture_join.REQUIRED_FILL_KEYS:
                self.assertIn(key, row)
        for row in orders:
            for key in fixture_join.REQUIRED_ORDER_KEYS:
                self.assertIn(key, row)
        self.assertEqual([row['order_id'] for row in orders], [101, 102, 103])
        self.assertEqual(fills[-1]['kind'], 'taker')
        self.assertEqual(fills[-1]['order_id'], -1)

    def test_synthetic_join_wires_helpers_without_promoting_metrics(self):
        report = self._synthetic()
        labels = report['labels']
        self.assertEqual(report['source'], 'synthetic_schema_standin')
        self.assertEqual(report['assumed_scenario'], 'q3300')
        self.assertEqual(report['strategy_label'], '000')
        self.assertEqual(report['delay_label'], 'd0.25')
        self.assertEqual(report['row_count'], 4)
        self.assertEqual(report['maker_rows'], 3)
        self.assertEqual(report['taker_rows'], 1)
        self.assertFalse(report['promoted'])
        self.assertFalse(report['stress']['loaded'])
        self.assertEqual(report['stress']['fills'], fixture_join.STRESS_FILLS_REL)
        self.assertNotIn('q10000', report['fills_path'])
        fixture_join.assert_null_scorecard(report['published'])
        self.assertEqual(report['published']['status'], 'NOT_RUN')
        self.assertEqual(report['published']['pick'], 'A')
        self.assertIsNone(report['results'])
        self.assertIsNone(report['pnl'])
        for key in fixture_join.OUTPUT_KEYS:
            self.assertIsNone(report['published'][key])
            self.assertIsNone(report[key])

        matched, crossed, outside, taker = labels
        primary = rails.scenario_queue('q3300')
        stress = rails.scenario_queue('q10000')
        self.assertEqual(matched['measured_queue_ahead'], primary)
        self.assertEqual(matched['queue_attribution_bin'], 'q3300')
        self.assertFalse(matched['queue_bin_mismatch'])
        self.assertNotEqual(matched['measured_queue_ahead'], Decimal('100'))
        self.assertEqual(crossed['measured_queue_ahead'], stress)
        self.assertEqual(crossed['queue_attribution_bin'], 'q10000')
        self.assertTrue(crossed['queue_bin_mismatch'])
        self.assertEqual(outside['queue_attribution_bin'], hygiene.OUTSIDE_BIN)
        self.assertTrue(outside['queue_bin_mismatch'])
        self.assertIsNone(taker['queue_attribution_bin'])
        self.assertIsNone(taker['queue_bin_mismatch'])
        self.assertIsNone(taker['measured_queue_ahead'])

        self.assertFalse(matched['maker_credit_floor_zero_refuse'])
        self.assertTrue(crossed['maker_credit_floor_zero_refuse'])
        self.assertEqual(
            crossed['maker_credit_floor_zero_refuse'],
            hygiene.maker_credit_floor_zero_refuse(Decimal('0.01'), Decimal('1'))['maker_credit_floor_zero_refuse'],
        )
        self.assertFalse(outside['maker_credit_floor_zero_refuse'])
        self.assertIsNone(taker['maker_credit_floor_zero_refuse'])

        self.assertTrue(matched['content_fresh_flag'])
        self.assertEqual(matched['freshness_reason'], 'initial')
        self.assertIsNone(matched['freshness_gap_sec'])
        self.assertFalse(crossed['content_fresh_flag'])
        self.assertEqual(crossed['freshness_reason'], 'keepalive_ignored')
        self.assertEqual(crossed['freshness_gap_sec'], Decimal('10'))
        self.assertTrue(outside['content_fresh_flag'])
        self.assertEqual(outside['freshness_reason'], 'content_changed')
        self.assertEqual(outside['freshness_gap_sec'], Decimal('25'))
        self.assertIsNone(taker['content_fresh_flag'])
        self.assertIsNone(taker['freshness_gap_sec'])

        self.assertTrue(matched['round_up'])
        self.assertTrue(crossed['round_up'])
        self.assertFalse(outside['round_up'])
        self.assertTrue(taker['round_up'])
        self.assertEqual(matched['examiner_formula_id'], feebook.EXAMINER_FORMULA_ID)
        self.assertEqual(taker['examiner_formula_id'], feebook.EXAMINER_FORMULA_ID)
        maker_rate = _rate('maker')
        taker_rate = _rate('taker')
        direct_maker = hygiene.fee_delta('maker', Decimal('1.0'), Decimal('0.5'), maker_rate, round_up=True)
        direct_partial = hygiene.fee_delta('maker', Decimal('1.0'), Decimal('0.4'), maker_rate, round_up=False)
        direct_taker = hygiene.fee_delta('taker', Decimal('2.0'), Decimal('0.6'), taker_rate, round_up=True)
        self.assertEqual(matched['fee_delta'], direct_maker['fee_delta'])
        self.assertEqual(outside['fee_delta'], direct_partial['fee_delta'])
        self.assertEqual(taker['fee_delta'], direct_taker['fee_delta'])
        self.assertGreater(matched['fee_delta'], 0)
        self.assertIsNone(matched['pnl'])
        self.assertIsNone(taker['pnl'])

        makers = [row for row in labels if row['queue_bin_mismatch'] is not None]
        preview = hygiene.pre_settlement_outputs(makers, joined=True)
        self.assertEqual(preview['status'], hygiene.SYNTHETIC_FIXTURE_ONLY)
        self.assertIsNone(preview['results'])
        self.assertIsNone(preview['pnl'])
        self.assertEqual(
            preview['fee_delta_vs_inherited_model'],
            makers[0]['fee_delta'] + makers[1]['fee_delta'] + makers[2]['fee_delta'],
        )
        self.assertEqual(preview['freshness_gap_sec'], Decimal('25'))
        self.assertEqual(preview['queue_bin_mismatch_rate'], Decimal('2') / Decimal('3'))
        self.assertIsNone(report['published']['fee_delta_vs_inherited_model'])
        self.assertIsNone(report['published']['freshness_gap_sec'])
        self.assertIsNone(report['published']['queue_bin_mismatch_rate'])

    def test_gzip_reader_matches_the_plain_stand_in(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            fills = folder / 'q3300_d0.25_000_fills.jsonl.gz'
            orders = folder / 'q3300_d0.25_000_orders.jsonl.gz'
            with gzip.open(fills, 'wb') as handle:
                handle.write(fixture_join.SYNTHETIC_FILLS.read_bytes())
            with gzip.open(orders, 'wb') as handle:
                handle.write(fixture_join.SYNTHETIC_ORDERS.read_bytes())
            zipped = fixture_join.join_ledgers(fills, orders, source='synthetic_schema_standin')
        plain = self._synthetic()
        self.assertEqual(len(zipped['labels']), len(plain['labels']))
        for zipped_row, plain_row in zip(zipped['labels'], plain['labels']):
            self.assertEqual(zipped_row, plain_row)
        fixture_join.assert_null_scorecard(zipped['published'])

    def test_non_000_and_unjoined_maker_are_refused(self):
        with self.assertRaises(fixture_join.FixtureJoinError):
            fixture_join.ledger_identity('q3300_d0.25_001_fills.jsonl.gz')
        with self.assertRaises(fixture_join.FixtureJoinError):
            fixture_join.ledger_identity('q5000_d0.25_000_fills.jsonl.gz')
        fills = fixture_join.load_jsonl(fixture_join.SYNTHETIC_FILLS)
        orders = fixture_join.load_jsonl(fixture_join.SYNTHETIC_ORDERS)
        with self.assertRaises(fixture_join.FixtureJoinError):
            fixture_join.join_rows(
                fills,
                orders[:1],
                assumed_scenario='q3300',
                source='synthetic_schema_standin',
                fills_path=fixture_join.SYNTHETIC_FILLS,
                orders_path=fixture_join.SYNTHETIC_ORDERS,
            )

    def test_scorecard_promotion_is_refused(self):
        report = self._synthetic()
        filled = dict(report['published'])
        filled['fee_delta_vs_inherited_model'] = report['labels'][0]['fee_delta']
        with self.assertRaises(fixture_join.ScorecardPromotionRefused):
            fixture_join.assert_null_scorecard(filled)
        with self.assertRaises(fixture_join.ScorecardPromotionRefused):
            fixture_join.write_scorecard(report['published'])
        with self.assertRaises(fixture_join.ScorecardPromotionRefused):
            fixture_join.write_scorecard(filled)

    def test_floats_reach_the_helpers_as_decimals(self):
        self.assertEqual(fixture_join.ledger_decimal(0.5, 'price'), Decimal('0.5'))
        self.assertEqual(fixture_join.ledger_decimal(3300.0, 'initial_queue'), rails.scenario_queue('q3300'))
        with self.assertRaises(TypeError):
            fixture_join.ledger_decimal(True, 'price')
