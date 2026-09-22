"""Unit pins for the Q6-000 queue-fragility fixture join.

Synthetic rows exercise QF0, QF1, and QF2. They are not a historical walk
and they are not profit. Freeze outputs stay null.
"""
import gzip
import importlib.util
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

import feebook
import fixture_join
import queue_fragility as qf
import rails


def _hygiene_fixture_join():
    spec = importlib.util.spec_from_file_location(
        'qf_hygiene_fixture_join',
        fixture_join.HYGIENE_FIXTURE_JOIN,
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PinTests(unittest.TestCase):
    def test_binding_imports_this_lab_and_the_hygiene_join_file(self):
        binding = fixture_join.instrument_binding()
        hygiene_join = _hygiene_fixture_join()
        self.assertEqual(Path(feebook.__file__).resolve().parent.name, 'kalshi_feebook_lab_20260922')
        self.assertEqual(Path(rails.__file__).resolve().parent.name, 'kalshi_rails_lab_20260922')
        self.assertEqual(Path(qf.__file__).resolve().parent.name, 'kalshi_queue_fragility_000_lab_20260922')
        self.assertEqual(ROOT.name, 'kalshi_queue_fragility_000_lab_20260922')
        self.assertTrue(fixture_join.HYGIENE_FIXTURE_JOIN.is_file())
        self.assertEqual(binding['experiment_id'], 'QF_fixture_join_000_20260922')
        self.assertEqual(binding['lab_directory'], 'kalshi_queue_fragility_000_lab_20260922')
        self.assertEqual(binding['pick'], 'B')
        self.assertIs(binding['second_lab'], False)
        self.assertEqual(binding['strategy_pointer'], 'Q6-000')
        self.assertEqual(binding['feebook_commit'], '22371178cb2663250b4762f328069571c48cb551')
        self.assertEqual(binding['rails_commit'], '6a28e0d6254327ea4e6451c781bec56215ac6cac')
        self.assertEqual(binding['queue_fragility_py_commit'], 'c33af159d00c07f2d66b2f93174cfcdb4cde8d37')
        self.assertEqual(binding['prior_a_merge'], '80050e9b6d015cbf394ea8443dd550eea4c2f1ee')
        self.assertEqual(
            binding['hygiene_fixture_join'],
            'kalshi_r2p1_hygiene_000_lab_20260922/fixture_join.py',
        )
        self.assertEqual(binding['hygiene_fixture_join_commit'], '79800a82b8ad2c1e10f614f69fd7105d11e0d041')
        self.assertEqual(binding['examiner_formula_id'], feebook.EXAMINER_FORMULA_ID)
        self.assertEqual(binding['examiner_formula_id'], qf.feebook_binding()['formula_id'])
        self.assertIs(binding['fee_is_knob'], False)
        self.assertIs(binding['live_orders'], False)
        self.assertIs(binding['signal_retune'], False)
        self.assertIs(binding['forbid_capital_A2_A3'], True)
        self.assertEqual(set(binding['arms']), set(qf.ARMS))
        self.assertEqual(binding['stress_role'], fixture_join.STRESS_ROLE)
        self.assertEqual(hygiene_join.PRIMARY_FILLS_SHA256, fixture_join.PRIMARY_FILLS_SHA256)
        self.assertEqual(hygiene_join.PRIMARY_ORDERS_SHA256, fixture_join.PRIMARY_ORDERS_SHA256)
        self.assertEqual(hygiene_join.PRIMARY_FILLS_REL, fixture_join.PRIMARY_FILLS_REL)
        self.assertEqual(list(PARENT.glob('kalshi_r2p1_fixture_join_000_lab_*')), [])
        self.assertEqual(
            sorted(path.name for path in PARENT.glob('*queue_fragility*')),
            ['kalshi_queue_fragility_000_lab_20260922'],
        )

    def test_pinned_cores_match_their_commits(self):
        for commit, path in (
            (fixture_join.FEEBOOK_COMMIT, 'kalshi_feebook_lab_20260922'),
            (fixture_join.RAILS_COMMIT, 'kalshi_rails_lab_20260922'),
            (fixture_join.QUEUE_FRAGILITY_PY_COMMIT, 'kalshi_queue_fragility_000_lab_20260922/queue_fragility.py'),
            (fixture_join.HYGIENE_FIXTURE_JOIN_COMMIT, 'kalshi_r2p1_hygiene_000_lab_20260922/fixture_join.py'),
            (fixture_join.HYGIENE_FIXTURE_JOIN_COMMIT, 'kalshi_r2p1_hygiene_000_lab_20260922/hygiene.py'),
        ):
            proc = subprocess.run(
                ['git', 'diff', '--exit-code', commit, '--', path],
                cwd=PARENT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)

    def test_packet_sha_and_pick_b(self):
        self.assertEqual(fixture_join.sha256_file(fixture_join.PACKET), fixture_join.PACKET_SHA256)
        self.assertTrue(fixture_join.PACKET_SHA256.startswith('d95adb9b'))
        frozen = json.loads(fixture_join.FROZEN_EXPERIMENT.read_text())
        packet = json.loads(fixture_join.PACKET_FROZEN.read_text())
        kernel = json.loads(fixture_join.PACKET_KERNEL.read_text())
        acceptance = frozen['fixture_join_acceptance']
        self.assertEqual(frozen['packet_sha256'], qf.PACKET_SHA256)
        self.assertTrue(qf.PACKET_SHA256.startswith('e01d684a'))
        self.assertEqual(acceptance['pick'], 'B')
        self.assertIs(acceptance['second_lab'], False)
        self.assertEqual(acceptance['lab_directory'], fixture_join.LAB_DIRECTORY)
        self.assertEqual(acceptance['packet_sha256'], fixture_join.PACKET_SHA256)
        self.assertEqual(packet['pick'], 'B')
        self.assertEqual(kernel['pick'], 'B')
        self.assertEqual(packet['packet_sha256'], fixture_join.PACKET_SHA256)
        self.assertEqual(kernel['packet_sha256'], fixture_join.PACKET_SHA256)
        self.assertEqual(packet['prior_A_merge'], '80050e9b')
        self.assertIs(acceptance['forbid_000_retune'], True)
        self.assertIs(acceptance['forbid_capital_A2_A3'], True)
        self.assertIs(frozen['live_orders'], False)
        self.assertEqual(frozen['knob'], 'queue_fill_stress_only')
        self.assertEqual(acceptance['knob'], 'qf_fixture_join_wiring_only_metrics_null')

    def test_freeze_outputs_stay_null(self):
        frozen = json.loads(fixture_join.FROZEN_EXPERIMENT.read_text())
        empty = json.loads(fixture_join.EMPTY_RESULTS.read_text())
        packet_results = json.loads(fixture_join.PACKET_RESULTS.read_text())
        packet_frozen = json.loads(fixture_join.PACKET_FROZEN.read_text())
        acceptance = frozen['fixture_join_acceptance']
        for payload in (frozen, empty, packet_results, packet_frozen, acceptance):
            for key in fixture_join.OUTPUT_KEYS:
                self.assertIsNone(payload[key])
        self.assertEqual(empty['status'], 'NOT_RUN')
        self.assertEqual(packet_results['status'], 'NOT_RUN')
        self.assertEqual(packet_results['pick'], 'B')
        self.assertEqual(frozen['status'], 'FROZEN_NOT_RUN')
        self.assertIsNone(qf.frozen_output_snapshot()['fill_rate_delta_vs_q3300'])
        self.assertIsNone(qf.frozen_output_snapshot()['pnl'])

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
        pin = (ROOT / 'fixtures' / 'PIN.md').read_text()
        self.assertIn(fixture_join.PRIMARY_FILLS_REL, pin)
        self.assertIn(fixture_join.PRIMARY_FILLS_SHA256, pin)
        self.assertIn('kalshi_r2p1_hygiene_000_lab_20260922/fixture_join.py', pin)
        self.assertIn(fixture_join.STRESS_ROLE, (ROOT / 'fixture_join.py').read_text())

    def test_shadow_fee_literals_and_the_removed_lab_are_absent(self):
        source = (ROOT / 'fixture_join.py').read_text()
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
            'kalshi_r2p1_fixture_join_000_lab',
            'completed_strategy_pnl',
            'role_pnl',
            'maker_off',
        ):
            self.assertNotIn(banned, source)

    def test_live_orders_and_capital_arms_are_refused(self):
        with self.assertRaises(qf.LiveOrdersForbidden):
            fixture_join.execution_adapter()
        for mode in qf.FORBIDDEN_CAPITAL_MODES:
            with self.assertRaises(qf.CapitalArmForbidden):
                qf.shared_capital(mode)


class JoinTests(unittest.TestCase):
    def setUp(self):
        self.frozen_before = fixture_join.FROZEN_EXPERIMENT.read_bytes()
        self.empty_before = fixture_join.EMPTY_RESULTS.read_bytes()
        self.packet_results_before = fixture_join.PACKET_RESULTS.read_bytes()
        self.packet_frozen_before = fixture_join.PACKET_FROZEN.read_bytes()
        self.packet_before = fixture_join.PACKET.read_bytes()
        self.core_before = (ROOT / 'queue_fragility.py').read_bytes()
        self.hygiene_join_before = fixture_join.HYGIENE_FIXTURE_JOIN.read_bytes()

    def tearDown(self):
        self.assertEqual(fixture_join.FROZEN_EXPERIMENT.read_bytes(), self.frozen_before)
        self.assertEqual(fixture_join.EMPTY_RESULTS.read_bytes(), self.empty_before)
        self.assertEqual(fixture_join.PACKET_RESULTS.read_bytes(), self.packet_results_before)
        self.assertEqual(fixture_join.PACKET_FROZEN.read_bytes(), self.packet_frozen_before)
        self.assertEqual(fixture_join.PACKET.read_bytes(), self.packet_before)
        self.assertEqual((ROOT / 'queue_fragility.py').read_bytes(), self.core_before)
        self.assertEqual(fixture_join.HYGIENE_FIXTURE_JOIN.read_bytes(), self.hygiene_join_before)

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
        self.assertEqual([row['order_id'] for row in orders], [201, 203])
        self.assertEqual(fills[-1]['kind'], 'taker')
        self.assertEqual(fills[-1]['order_id'], -1)

    def test_synthetic_join_wires_arms_without_promoting_metrics(self):
        report = self._synthetic()
        labels = report['labels']
        self.assertEqual(report['source'], 'synthetic_schema_standin')
        self.assertEqual(report['assumed_scenario'], 'q3300')
        self.assertEqual(report['strategy_label'], '000')
        self.assertEqual(report['delay_label'], 'd0.25')
        self.assertEqual(report['row_count'], 3)
        self.assertEqual(report['maker_rows'], 2)
        self.assertEqual(report['taker_rows'], 1)
        self.assertEqual(report['arms_run'], qf.ARMS)
        self.assertFalse(report['promoted'])
        self.assertFalse(report['stress']['loaded'])
        self.assertEqual(report['stress']['fills'], fixture_join.STRESS_FILLS_REL)
        self.assertNotIn('q10000', report['fills_path'])
        self.assertEqual(report['fee_binding'], qf.feebook_binding())
        self.assertIs(report['fee_binding']['fee_is_knob'], False)
        self.assertIs(report['fee_binding']['maker_fees_enabled'], True)
        fixture_join.assert_null_scorecard(report['published'])
        self.assertEqual(report['published']['status'], 'NOT_RUN')
        self.assertEqual(report['published']['pick'], 'B')
        for key in fixture_join.OUTPUT_KEYS:
            self.assertIsNone(report['published'][key])
            self.assertIsNone(report[key])

        wide, partial, taker = labels
        self.assertIsNone(taker['arms'])
        self.assertIsNone(taker['pnl'])
        self.assertEqual(taker['order_id'], -1)
        self.assertEqual(wide['ledger_initial_queue'], Decimal('12'))
        self.assertEqual(partial['ledger_initial_queue'], Decimal('0'))

        for row in (wide, partial):
            self.assertEqual(set(row['arms']), set(qf.ARMS))
            self.assertIsNone(row['pnl'])
            for arm in qf.ARMS:
                labeled = row['arms'][arm]
                params = qf.arm_queue_params(arm)
                direct = qf.measure_arm(arm, [row['intent']], [row['trade']])
                self.assertEqual(labeled['queue_params'], params)
                self.assertEqual(labeled['queue_params']['queue_ahead_contracts'], params['queue_ahead_contracts'])
                self.assertEqual(labeled['queue_params']['fill_participation'], rails.FILL_PARTICIPATION_DEFAULT)
                self.assertEqual(labeled['filled'], direct['filled'])
                self.assertEqual(labeled['slice_adverse_contracts'], direct['adverse_queue_exposure'])
                self.assertEqual(labeled['fill_rate'], direct['fill_rate'])
                self.assertIsNone(labeled['pnl'])
                self.assertIsNone(labeled['results'])
                for produced in labeled['fills']:
                    self.assertEqual(produced['formula_id'], feebook.EXAMINER_FORMULA_ID)
                    self.assertEqual(produced['rate'], qf.feebook_binding()['maker_rate'])
                    self.assertIs(produced['rounded_up'], False)
                    self.assertNotEqual(produced['formula_id'], feebook.GROK_COMPARATOR_FORMULA_ID)

        self.assertEqual(wide['arms'][qf.QF0]['queue_params']['queue_model'], 'measured')
        self.assertEqual(wide['arms'][qf.QF1]['queue_params']['queue_model'], 'measured')
        self.assertEqual(wide['arms'][qf.QF2]['queue_params']['queue_model'], 'front')
        self.assertEqual(wide['arms'][qf.QF0]['queue_params']['queue_ahead_contracts'], rails.scenario_queue('q3300'))
        self.assertEqual(wide['arms'][qf.QF1]['queue_params']['queue_ahead_contracts'], rails.scenario_queue('q10000'))
        self.assertEqual(wide['arms'][qf.QF2]['queue_params']['queue_ahead_contracts'], Decimal('0'))
        for arm in qf.ARMS:
            self.assertNotEqual(
                wide['arms'][arm]['queue_params']['queue_ahead_contracts'],
                wide['ledger_initial_queue'],
            )
        self.assertGreater(wide['arms'][qf.QF2]['filled'], wide['arms'][qf.QF0]['filled'])
        self.assertGreater(wide['arms'][qf.QF0]['filled'], wide['arms'][qf.QF1]['filled'])
        self.assertEqual(wide['arms'][qf.QF1]['filled'], Decimal('0'))
        self.assertEqual(wide['arms'][qf.QF2]['slice_adverse_contracts'], Decimal('0'))
        self.assertGreater(
            wide['arms'][qf.QF1]['slice_adverse_contracts'],
            wide['arms'][qf.QF0]['slice_adverse_contracts'],
        )
        self.assertEqual(wide['arms'][qf.QF0]['fills'][0]['rate'], wide['arms'][qf.QF2]['fills'][0]['rate'])
        self.assertEqual(partial['arms'][qf.QF0]['filled'], Decimal('0'))
        self.assertEqual(partial['arms'][qf.QF1]['filled'], Decimal('0'))
        self.assertGreater(partial['arms'][qf.QF2]['filled'], Decimal('0'))

        preview = qf.pre_settlement_outputs([wide['intent']], [wide['trade']], joined=True)
        self.assertEqual(preview['status'], qf.SYNTHETIC_FIXTURE_ONLY)
        self.assertIsNone(preview['results'])
        self.assertIsNone(preview['pnl'])
        self.assertLess(preview['fill_rate_delta_vs_q3300'][qf.QF1], 0)
        self.assertGreater(preview['fill_rate_delta_vs_q3300'][qf.QF2], 0)
        self.assertEqual(preview['adverse_queue_exposure'][qf.QF2], Decimal('0'))
        self.assertEqual(preview['participation_stress_gap'], rails.FILL_PARTICIPATION_DEFAULT)
        self.assertIsNone(report['published']['fill_rate_delta_vs_q3300'])
        self.assertIsNone(report['published']['adverse_queue_exposure'])
        self.assertIsNone(report['published']['participation_stress_gap'])
        self.assertIsNone(qf.frozen_output_snapshot()['fill_rate_delta_vs_q3300'])
        self.assertIsNone(qf.frozen_output_snapshot()['adverse_queue_exposure'])
        self.assertIsNone(qf.frozen_output_snapshot()['participation_stress_gap'])

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
            self.assertEqual(zipped_row['order_id'], plain_row['order_id'])
            self.assertEqual(zipped_row['role'], plain_row['role'])
            self.assertEqual(zipped_row['arms'], plain_row['arms'])
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
        filled['fill_rate_delta_vs_q3300'] = report['labels'][0]['arms'][qf.QF0]['fill_rate']
        with self.assertRaises(fixture_join.ScorecardPromotionRefused):
            fixture_join.assert_null_scorecard(filled)
        with self.assertRaises(fixture_join.ScorecardPromotionRefused):
            fixture_join.write_scorecard(report['published'])
        with self.assertRaises(fixture_join.ScorecardPromotionRefused):
            fixture_join.write_scorecard(filled)

    def test_floats_reach_the_helpers_as_decimals(self):
        self.assertEqual(fixture_join.ledger_decimal(0.4, 'price'), Decimal('0.4'))
        self.assertEqual(fixture_join.ledger_decimal(3300.0, 'initial_queue'), rails.scenario_queue('q3300'))
        with self.assertRaises(TypeError):
            fixture_join.ledger_decimal(True, 'price')

    def test_a_refused_maker_credit_is_not_rewritten(self):
        fills = fixture_join.load_jsonl(fixture_join.SYNTHETIC_FILLS)
        orders = fixture_join.load_jsonl(fixture_join.SYNTHETIC_ORDERS)
        orders[0] = dict(orders[0])
        orders[0]['price'] = 0.01
        orders[0]['submitted_quantity'] = 1
        fills[0] = dict(fills[0])
        fills[0]['price'] = 0.01
        with self.assertRaises(rails.MakerCreditRefused):
            fixture_join.join_rows(
                fills,
                orders,
                assumed_scenario='q3300',
                source='synthetic_schema_standin',
                fills_path=fixture_join.SYNTHETIC_FILLS,
                orders_path=fixture_join.SYNTHETIC_ORDERS,
            )
