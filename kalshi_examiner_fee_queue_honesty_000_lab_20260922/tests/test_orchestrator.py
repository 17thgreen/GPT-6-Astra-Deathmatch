"""Unit pins for the Q6-000 Examiner fee and queue orchestrator.

Both joins run on one fills stream. In-memory labels are not a historical
walk and they are not profit. Freeze outputs stay null.
"""
import gzip
import json
import subprocess
import sys
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT.parent
sys.path.insert(0, str(ROOT))

import orchestrator


class PinTests(unittest.TestCase):
    def test_binding_imports_both_joins(self):
        binding = orchestrator.instrument_binding()
        self.assertEqual(ROOT.name, orchestrator.LAB_DIRECTORY)
        self.assertTrue(orchestrator.HYGIENE_FIXTURE_JOIN.is_file())
        self.assertTrue(orchestrator.QF_FIXTURE_JOIN.is_file())
        self.assertEqual(
            Path(orchestrator.hygiene_join.__file__).resolve(),
            orchestrator.HYGIENE_FIXTURE_JOIN.resolve(),
        )
        self.assertEqual(
            Path(orchestrator.qf_join.__file__).resolve(),
            orchestrator.QF_FIXTURE_JOIN.resolve(),
        )
        self.assertEqual(binding['experiment_id'], 'examiner_fee_queue_honesty_000_20260922')
        self.assertIs(binding['single_examiner_packet'], True)
        self.assertEqual(binding['strategy_pointer'], 'Q6-000')
        self.assertEqual(binding['feebook_commit'], '22371178cb2663250b4762f328069571c48cb551')
        self.assertEqual(binding['rails_commit'], '6a28e0d6254327ea4e6451c781bec56215ac6cac')
        self.assertEqual(binding['hygiene_join_commit'], orchestrator.HYGIENE_JOIN_COMMIT)
        self.assertEqual(binding['qf_join_commit'], orchestrator.QF_JOIN_COMMIT)
        self.assertEqual(
            binding['hygiene_join'],
            'kalshi_r2p1_hygiene_000_lab_20260922/fixture_join.py',
        )
        self.assertEqual(
            binding['qf_join'],
            'kalshi_queue_fragility_000_lab_20260922/fixture_join.py',
        )
        self.assertEqual(
            binding['examiner_formula_id'],
            binding['hygiene_binding']['examiner_formula_id'],
        )
        self.assertEqual(
            binding['examiner_formula_id'],
            binding['qf_binding']['examiner_formula_id'],
        )
        self.assertIs(binding['live_orders'], False)
        self.assertIs(binding['signal_retune'], False)
        self.assertIs(binding['forbid_capital_A2_A3'], True)
        self.assertIs(binding['forbid_000_retune'], True)
        self.assertIs(binding['fee_is_knob'], False)
        self.assertEqual(binding['capital']['mode'], 'A1_shared_pool')
        self.assertEqual(binding['capital']['C_total_usd'], Decimal('5000'))
        self.assertEqual(binding['stress_role'], orchestrator.STRESS_ROLE)
        self.assertEqual(
            sorted(path.name for path in PARENT.glob('kalshi_examiner_fee_queue_honesty_000_lab_*')),
            ['kalshi_examiner_fee_queue_honesty_000_lab_20260922'],
        )

    def test_pinned_cores_match_their_commits(self):
        for commit, path in (
            (orchestrator.FEEBOOK_COMMIT, 'kalshi_feebook_lab_20260922'),
            (orchestrator.RAILS_COMMIT, 'kalshi_rails_lab_20260922'),
            (orchestrator.HYGIENE_JOIN_COMMIT, 'kalshi_r2p1_hygiene_000_lab_20260922/hygiene.py'),
            (orchestrator.HYGIENE_JOIN_COMMIT, 'kalshi_r2p1_hygiene_000_lab_20260922/fixture_join.py'),
            (orchestrator.QF_JOIN_COMMIT, 'kalshi_queue_fragility_000_lab_20260922/queue_fragility.py'),
            (orchestrator.QF_JOIN_COMMIT, 'kalshi_queue_fragility_000_lab_20260922/fixture_join.py'),
        ):
            proc = subprocess.run(
                ['git', 'diff', '--exit-code', commit, '--', path],
                cwd=PARENT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)

    def test_packet_sha_and_single_channel(self):
        self.assertEqual(orchestrator.sha256_file(orchestrator.PACKET), orchestrator.PACKET_SHA256)
        self.assertTrue(orchestrator.PACKET_SHA256.startswith('4799642e'))
        frozen = json.loads(orchestrator.FROZEN_EXPERIMENT.read_text())
        kernel = json.loads(orchestrator.PACKET_KERNEL.read_text())
        packet = json.loads(orchestrator.PACKET_FROZEN.read_text())
        self.assertEqual(frozen['packet_sha256'], orchestrator.PACKET_SHA256)
        self.assertEqual(kernel['packet_sha256'], orchestrator.PACKET_SHA256)
        self.assertEqual(packet['packet_sha256'], orchestrator.PACKET_SHA256)
        self.assertIs(frozen['single_examiner_packet'], True)
        self.assertIs(frozen['forbid_000_retune'], True)
        self.assertIs(frozen['forbid_capital_A2_A3'], True)
        self.assertIs(frozen['live_orders'], False)
        self.assertEqual(frozen['strategy_pointer'], 'Q6-000')
        self.assertEqual(kernel['strategy_pointer'], 'Q6-000')
        self.assertEqual(packet['strategy_pointer'], 'Q6-000')
        self.assertEqual(
            kernel['consumes_joins'],
            [
                'kalshi_r2p1_hygiene_000_lab_20260922',
                'kalshi_queue_fragility_000_lab_20260922',
            ],
        )
        self.assertTrue(kernel['production_fills_present_at_freeze'])
        self.assertEqual(kernel['prior_qf_join_merge'], '7026be51')
        shadow = json.loads(orchestrator.SHADOW_FREEZE.read_text())
        self.assertEqual(shadow['selected'], '000')
        self.assertEqual(orchestrator.sha256_file(orchestrator.SHADOW_FREEZE), orchestrator.SHADOW_FREEZE_SHA256)

    def test_freeze_outputs_stay_null(self):
        frozen = json.loads(orchestrator.FROZEN_EXPERIMENT.read_text())
        empty = json.loads(orchestrator.EMPTY_RESULTS.read_text())
        packet_frozen = json.loads(orchestrator.PACKET_FROZEN.read_text())
        packet_results = json.loads(orchestrator.PACKET_RESULTS.read_text())
        for payload in (frozen, empty, packet_frozen):
            for key in orchestrator.OUTPUT_KEYS:
                self.assertIsNone(payload[key])
        self.assertIsNone(packet_results['results'])
        self.assertIsNone(packet_results['pnl'])
        self.assertIsNone(packet_results['metrics'])
        self.assertEqual(empty['status'], 'NOT_SCORED')
        self.assertEqual(packet_results['status'], 'NOT_SCORED')
        self.assertIs(empty['live_promotion'], False)
        snapshot = orchestrator.frozen_output_snapshot()
        for key in orchestrator.OUTPUT_KEYS:
            self.assertIsNone(snapshot['frozen.%s' % key])
            self.assertIsNone(snapshot['empty.%s' % key])
            self.assertIsNone(snapshot['packet_frozen.%s' % key])

    def test_production_pin_matches_the_delivery_manifest(self):
        manifest = json.loads((PARENT / 'nfl_factorial_lab_20260921' / 'DELIVERY_MANIFEST.json').read_text())
        by_path = {item['path']: item for item in manifest['files']}
        self.assertEqual(by_path['results/q3300_d0.25_000_fills.jsonl.gz']['sha256'], orchestrator.PRIMARY_FILLS_SHA256)
        self.assertEqual(by_path['results/q3300_d0.25_000_orders.jsonl.gz']['sha256'], orchestrator.PRIMARY_ORDERS_SHA256)
        self.assertEqual(orchestrator.hygiene_join.PRIMARY_FILLS_SHA256, orchestrator.PRIMARY_FILLS_SHA256)
        self.assertEqual(orchestrator.qf_join.PRIMARY_FILLS_SHA256, orchestrator.PRIMARY_FILLS_SHA256)
        self.assertEqual(orchestrator.hygiene_join.PRIMARY_ORDERS_SHA256, orchestrator.PRIMARY_ORDERS_SHA256)
        self.assertEqual(orchestrator.qf_join.PRIMARY_ORDERS_SHA256, orchestrator.PRIMARY_ORDERS_SHA256)
        self.assertEqual(orchestrator.hygiene_join.PRIMARY_FILLS_REL, orchestrator.PRIMARY_FILLS_REL)
        self.assertEqual(orchestrator.qf_join.PRIMARY_ORDERS_REL, orchestrator.PRIMARY_ORDERS_REL)
        pin = (ROOT / 'fixtures' / 'PIN.md').read_text()
        self.assertIn(orchestrator.PRIMARY_FILLS_REL, pin)
        self.assertIn(orchestrator.PRIMARY_FILLS_SHA256, pin)
        self.assertIn(orchestrator.PRIMARY_ORDERS_SHA256, pin)

    def test_same_stream_wires_both_joins_and_leaves_the_freeze_null(self):
        before = {
            path: path.read_bytes()
            for path in (
                orchestrator.FROZEN_EXPERIMENT,
                orchestrator.EMPTY_RESULTS,
                orchestrator.PACKET_FROZEN,
                orchestrator.PACKET_RESULTS,
                orchestrator.PACKET,
                orchestrator.PACKET_KERNEL,
            )
        }
        choice = orchestrator.resolve_primary()
        report = orchestrator.conduct(choice)
        direct_hygiene = orchestrator.hygiene_join.join_ledgers(
            choice['fills_path'], choice['orders_path'], source=choice['source'],
        )
        direct_qf = orchestrator.qf_join.join_ledgers(
            choice['fills_path'], choice['orders_path'], source=choice['source'],
        )
        self.assertEqual(report['hygiene_join']['labels'], direct_hygiene['labels'])
        self.assertEqual(report['qf_join']['labels'], direct_qf['labels'])
        self.assertGreater(report['row_count'], 0)
        self.assertEqual(report['fills_path'], str(choice['fills_path']))
        self.assertEqual(report['orders_path'], str(choice['orders_path']))
        self.assertEqual(Path(report['hygiene_join']['fills_path']), Path(report['qf_join']['fills_path']))
        self.assertEqual(Path(report['hygiene_join']['orders_path']), Path(report['qf_join']['orders_path']))
        self.assertFalse(report['promoted'])
        self.assertFalse(report['stress']['loaded'])
        self.assertNotIn('q10000', report['fills_path'])
        self.assertIs(report['single_examiner_packet'], True)
        orchestrator.assert_null_scorecard(report)
        orchestrator.assert_null_scorecard(report['published'])
        for key in orchestrator.OUTPUT_KEYS:
            self.assertIn(key, report)
            self.assertIn(key, report['published'])
            self.assertIsNone(report[key])
            self.assertIsNone(report['published'][key])
        for name, _value_type in orchestrator.channel_fields(orchestrator.FEE_CHANNEL):
            self.assertIn(name, report['hygiene_join'])
            self.assertIsNone(report['hygiene_join'][name])
        for name, _value_type in orchestrator.channel_fields(orchestrator.QUEUE_CHANNEL):
            self.assertIn(name, report['qf_join'])
            self.assertIsNone(report['qf_join'][name])
        self.assertIs(report['channels'][orchestrator.FEE_CHANNEL]['wired'], True)
        self.assertIs(report['channels'][orchestrator.QUEUE_CHANNEL]['wired'], True)
        self.assertEqual(
            report['channels'][orchestrator.FEE_CHANNEL]['row_count'],
            report['channels'][orchestrator.QUEUE_CHANNEL]['row_count'],
        )
        self.assertEqual(len(report['published']['fee_fields']), 3)
        self.assertEqual(len(report['published']['queue_fields']), 3)
        self.assertEqual(report['published']['status'], 'NOT_SCORED')
        if choice['production_present']:
            self.assertEqual(choice['source'], 'production_pin')
            self.assertEqual(report['source'], 'production_pin')
        else:
            self.assertEqual(choice['source'], 'synthetic_schema_standin')
            self.assertEqual(report['source'], 'synthetic_schema_standin')
            self.assertEqual(Path(choice['fills_path']), orchestrator.qf_join.SYNTHETIC_FILLS)
            self.assertEqual(Path(choice['orders_path']), orchestrator.qf_join.SYNTHETIC_ORDERS)
        for path, payload in before.items():
            self.assertEqual(path.read_bytes(), payload)

    def test_queue_fields_are_equal_to_fee_fields(self):
        fee = orchestrator.channel_fields(orchestrator.FEE_CHANNEL)
        queue = orchestrator.channel_fields(orchestrator.QUEUE_CHANNEL)
        self.assertEqual(
            [name for name, _value_type in fee],
            [
                'fee_delta_vs_inherited_model',
                'freshness_gap_sec',
                'queue_bin_mismatch_rate',
            ],
        )
        self.assertEqual(
            [name for name, _value_type in queue],
            [
                'fill_rate_delta_vs_q3300',
                'adverse_queue_exposure',
                'participation_stress_gap',
            ],
        )
        self.assertEqual([value_type for _name, value_type in fee], ['Decimal', 'Decimal', 'Decimal'])
        self.assertEqual(
            [value_type for _name, value_type in queue],
            ['mapping[arm, Decimal]', 'mapping[arm, Decimal]', 'Decimal'],
        )
        self.assertIn(orchestrator.DECIMAL_TYPE, [value_type for _name, value_type in queue])
        self.assertEqual(
            [value_type for _name, value_type in queue].count(orchestrator.ARM_DECIMAL_MAP_TYPE),
            2,
        )
        binding = orchestrator.instrument_binding()
        self.assertEqual(binding['fee_fields'], fee)
        self.assertEqual(binding['queue_fields'], queue)
        self.assertEqual(len(binding['queue_fields']), len(binding['fee_fields']))
        report = orchestrator.conduct()
        self.assertEqual(report['published']['fee_fields'], fee)
        self.assertEqual(report['published']['queue_fields'], queue)
        fee_filled = dict(report['published'])
        fee_filled[fee[0][0]] = Decimal('1')
        with self.assertRaises(orchestrator.ScorecardPromotionRefused) as fee_caught:
            orchestrator.write_scorecard(fee_filled)
        makers = [row for row in report['qf_join']['labels'] if row['role'] == 'maker']
        self.assertGreater(len(makers), 0)
        arms = orchestrator.queue_fragility_core.ARMS
        for row in makers:
            self.assertEqual(set(row['arms']), set(arms))
            for arm in arms:
                self.assertIn('fill_rate', row['arms'][arm])
                self.assertIn('slice_adverse_contracts', row['arms'][arm])
                self.assertIsNone(row['arms'][arm]['results'])
                self.assertIsNone(row['arms'][arm]['pnl'])
        for name, _value_type in queue:
            filled = dict(report['published'])
            filled[name] = {arms[0]: Decimal('1')}
            with self.assertRaises(orchestrator.ScorecardPromotionRefused) as caught:
                orchestrator.write_scorecard(filled)
            self.assertIs(type(caught.exception), type(fee_caught.exception))
            self.assertIsNone(report['published'][name])
            self.assertIsNone(report[name])
        for path in (
            ROOT / 'orchestrator.py',
            ROOT / 'EXPERIMENT_SPEC.md',
            ROOT / 'README.md',
            ROOT / 'FROZEN_EXPERIMENT.json',
            ROOT / 'results' / 'EMPTY_RESULTS.json',
        ):
            text = path.read_text()
            self.assertNotIn('110%', text)
            self.assertNotIn('110 %', text)

    def test_omitted_queue_field_is_refused_like_an_omitted_fee_field(self):
        published = orchestrator.published_scorecard()
        fee_name = orchestrator.channel_fields(orchestrator.FEE_CHANNEL)[0][0]
        dropped_fee = dict(published)
        del dropped_fee[fee_name]
        with self.assertRaises(orchestrator.ScorecardPromotionRefused) as fee_caught:
            orchestrator.assert_null_scorecard(dropped_fee)
        with self.assertRaises(orchestrator.ScorecardPromotionRefused):
            orchestrator.write_scorecard(dropped_fee)
        for name, _value_type in orchestrator.channel_fields(orchestrator.QUEUE_CHANNEL):
            dropped = dict(published)
            del dropped[name]
            with self.assertRaises(orchestrator.ScorecardPromotionRefused) as caught:
                orchestrator.assert_null_scorecard(dropped)
            self.assertIs(type(caught.exception), type(fee_caught.exception))
            self.assertEqual(str(caught.exception), str(fee_caught.exception))
            with self.assertRaises(orchestrator.ScorecardPromotionRefused):
                orchestrator.write_scorecard(dropped)
        self.assertIsNone(published['fill_rate_delta_vs_q3300'])
        self.assertIsNone(published['adverse_queue_exposure'])
        self.assertIsNone(published['participation_stress_gap'])

    def test_scorecard_promotion_is_refused(self):
        report = orchestrator.conduct()
        for key in orchestrator.OUTPUT_KEYS:
            filled = dict(report['published'])
            filled[key] = Decimal('1')
            with self.assertRaises(orchestrator.ScorecardPromotionRefused):
                orchestrator.assert_null_scorecard(filled)
            with self.assertRaises(orchestrator.ScorecardPromotionRefused):
                orchestrator.write_scorecard(filled)
        with self.assertRaises(orchestrator.ScorecardPromotionRefused):
            orchestrator.write_scorecard(report['published'])
        with self.assertRaises(orchestrator.ScorecardPromotionRefused):
            orchestrator.write_scorecard(report)
        self.assertIsNone(orchestrator.frozen_output_snapshot()['frozen.fee_delta_vs_inherited_model'])
        self.assertIsNone(orchestrator.frozen_output_snapshot()['frozen.pnl'])

    def test_live_orders_and_capital_arms_are_refused(self):
        with self.assertRaises(orchestrator.LiveOrdersForbidden):
            orchestrator.execution_adapter()
        with self.assertRaises(orchestrator.hygiene_join.hygiene.LiveOrdersForbidden):
            orchestrator.hygiene_join.execution_adapter()
        with self.assertRaises(orchestrator.queue_fragility_core.LiveOrdersForbidden):
            orchestrator.qf_join.execution_adapter()
        with self.assertRaises(orchestrator.queue_fragility_core.CapitalArmForbidden):
            orchestrator.shared_capital('A2_shared_soft_reserve')
        with self.assertRaises(orchestrator.queue_fragility_core.CapitalArmForbidden):
            orchestrator.shared_capital('A3_hard_equal_slices')

    def test_non_000_ledger_is_refused(self):
        for name in ('q3300_d0.25_001_fills.jsonl.gz', 'q5000_d0.25_000_fills.jsonl.gz'):
            with self.assertRaises(orchestrator.hygiene_join.FixtureJoinError):
                orchestrator.hygiene_join.ledger_identity(name)
            with self.assertRaises(orchestrator.qf_join.FixtureJoinError):
                orchestrator.qf_join.ledger_identity(name)
            with self.assertRaises(orchestrator.hygiene_join.FixtureJoinError):
                orchestrator.ledger_identity(name)

    def _freeze_bytes(self):
        return {
            path: path.read_bytes()
            for path in (
                orchestrator.FROZEN_EXPERIMENT,
                orchestrator.EMPTY_RESULTS,
                orchestrator.PACKET_FROZEN,
                orchestrator.PACKET_RESULTS,
                orchestrator.PACKET,
                orchestrator.PACKET_KERNEL,
            )
        }

    def _write_gzip(self, path, payload):
        path.parent.mkdir(parents=True, exist_ok=True)
        with gzip.open(path, 'wb') as handle:
            handle.write(payload)

    def test_production_layout_is_selected_when_the_pin_matches(self):
        """Select the q3300 gzip pair when the name layout and sha256 match.

        The temporary bytes are the queue-fragility schema stand-in. They are
        not the indexed factorial ledger. The pin is aligned to those bytes
        for this test so the production branch can run. In-memory labels stay
        out of the freeze files.
        """
        before = self._freeze_bytes()
        indexed_fills = '9d56f5d3c599e092606be9f4a1ad41ae8baabff4921d3d722adf0b57ac944a3f'
        indexed_orders = 'c390801b9a7cf6d182d2d097123ed944792980524a7975e6e59a904a530f4b1c'
        self.assertEqual(orchestrator.PRIMARY_FILLS_SHA256, indexed_fills)
        self.assertEqual(orchestrator.PRIMARY_ORDERS_SHA256, indexed_orders)
        qf = orchestrator.qf_join
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fills = root / orchestrator.PRIMARY_FILLS_REL
            orders = root / orchestrator.PRIMARY_ORDERS_REL
            self._write_gzip(fills, qf.SYNTHETIC_FILLS.read_bytes())
            self._write_gzip(orders, qf.SYNTHETIC_ORDERS.read_bytes())
            harsh = fills.parent / 'q10000_d0.25_000_fills.jsonl.gz'
            harsh.write_bytes(fills.read_bytes())
            misplaced = root / fills.name
            misplaced.write_bytes(fills.read_bytes())
            fills_sha = orchestrator.sha256_file(fills)
            orders_sha = orchestrator.sha256_file(orders)
            self.assertNotEqual(fills_sha, indexed_fills)
            with self.assertRaises(orchestrator.OrchestratorError) as refused:
                orchestrator.resolve_primary(root)
            self.assertEqual(str(refused.exception), 'fills sha256')
            partial_root = root / 'partial'
            partial_fills = partial_root / orchestrator.PRIMARY_FILLS_REL
            self._write_gzip(partial_fills, qf.SYNTHETIC_FILLS.read_bytes())
            partial = orchestrator.resolve_primary(partial_root)
            self.assertEqual(partial['source'], 'synthetic_schema_standin')
            self.assertFalse(partial['production_present'])
            self.assertNotEqual(Path(partial['fills_path']), partial_fills)
            self.assertEqual(Path(partial['fills_path']), qf.SYNTHETIC_FILLS)
            with patch.object(orchestrator, 'PRIMARY_FILLS_SHA256', fills_sha), \
                 patch.object(orchestrator, 'PRIMARY_ORDERS_SHA256', orders_sha):
                choice = orchestrator.resolve_primary(root)
                self.assertEqual(choice['source'], 'production_pin')
                self.assertIs(choice['production_present'], True)
                self.assertEqual(Path(choice['fills_path']), fills)
                self.assertEqual(Path(choice['orders_path']), orders)
                self.assertEqual(choice['fills_sha256'], fills_sha)
                self.assertEqual(choice['orders_sha256'], orders_sha)
                self.assertEqual(orchestrator.sha256_file(choice['fills_path']), fills_sha)
                self.assertEqual(orchestrator.sha256_file(choice['orders_path']), orders_sha)
                self.assertTrue(str(choice['fills_path']).endswith(
                    'nfl_factorial_lab_20260921/results/q3300_d0.25_000_fills.jsonl.gz'
                ))
                self.assertNotIn('q10000', str(choice['fills_path']))
                self.assertNotEqual(Path(choice['fills_path']), qf.SYNTHETIC_FILLS)
                report = orchestrator.conduct(choice)
            self.assertEqual(report['source'], 'production_pin')
            self.assertIs(report['production_present'], True)
            self.assertEqual(Path(report['fills_path']), fills)
            self.assertEqual(Path(report['orders_path']), orders)
            self.assertEqual(Path(report['hygiene_join']['fills_path']), fills)
            self.assertEqual(Path(report['qf_join']['fills_path']), fills)
            self.assertEqual(Path(report['hygiene_join']['orders_path']), orders)
            self.assertEqual(Path(report['qf_join']['orders_path']), orders)
            self.assertGreater(report['row_count'], 0)
            self.assertFalse(report['promoted'])
            self.assertFalse(report['stress']['loaded'])
            self.assertNotIn('q10000', report['fills_path'])
            fee_delta = report['hygiene_join']['labels'][0]['fee_delta']
            self.assertIsInstance(fee_delta, Decimal)
            makers = [row for row in report['qf_join']['labels'] if row['role'] == 'maker']
            self.assertGreater(len(makers), 0)
            arm = orchestrator.queue_fragility_core.ARMS[0]
            self.assertIsInstance(makers[0]['arms'][arm]['fill_rate'], Decimal)
            orchestrator.assert_null_scorecard(report)
            orchestrator.assert_null_scorecard(report['published'])
            for key in orchestrator.OUTPUT_KEYS:
                self.assertIsNone(report[key])
                self.assertIsNone(report['published'][key])
            for name, _value_type in orchestrator.channel_fields(orchestrator.FEE_CHANNEL):
                self.assertIn(name, report['hygiene_join'])
                self.assertIsNone(report['hygiene_join'][name])
            for name, _value_type in orchestrator.channel_fields(orchestrator.QUEUE_CHANNEL):
                self.assertIn(name, report['qf_join'])
                self.assertIsNone(report['qf_join'][name])
            with self.assertRaises(orchestrator.ScorecardPromotionRefused):
                orchestrator.write_scorecard(report['published'])
            filled = dict(report['published'])
            filled['fee_delta_vs_inherited_model'] = fee_delta
            with self.assertRaises(orchestrator.ScorecardPromotionRefused):
                orchestrator.write_scorecard(filled)
            filled_queue = dict(report['published'])
            filled_queue['fill_rate_delta_vs_q3300'] = {
                arm: makers[0]['arms'][arm]['fill_rate'],
            }
            with self.assertRaises(orchestrator.ScorecardPromotionRefused):
                orchestrator.write_scorecard(filled_queue)
        self.assertEqual(orchestrator.PRIMARY_FILLS_SHA256, indexed_fills)
        self.assertEqual(orchestrator.PRIMARY_ORDERS_SHA256, indexed_orders)
        for path, payload in before.items():
            self.assertEqual(path.read_bytes(), payload)
        for key in orchestrator.OUTPUT_KEYS:
            self.assertIsNone(json.loads(orchestrator.FROZEN_EXPERIMENT.read_text())[key])
            self.assertIsNone(json.loads(orchestrator.EMPTY_RESULTS.read_text())[key])
            self.assertIsNone(json.loads(orchestrator.PACKET_FROZEN.read_text())[key])

    def test_implementation_hashes_match_source(self):
        frozen = json.loads(orchestrator.FROZEN_EXPERIMENT.read_text())
        recorded = frozen['implementation_sha256']
        self.assertIsInstance(recorded, dict)
        for name, digest in recorded.items():
            self.assertEqual(orchestrator.sha256_file(ROOT / name), digest)
        spec = frozen['specification_sha256']
        self.assertEqual(orchestrator.sha256_file(ROOT / 'EXPERIMENT_SPEC.md'), spec['EXPERIMENT_SPEC.md'])
        self.assertEqual(orchestrator.sha256_file(orchestrator.EMPTY_RESULTS), spec['results/EMPTY_RESULTS.json'])
