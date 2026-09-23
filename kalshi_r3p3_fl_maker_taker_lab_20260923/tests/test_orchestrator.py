"""Unit pins for the R3-P3 maker/taker and 10c bands harness.

Schema and pin locks only. Band membership and the native taker partition
are not a score and they are not profit. Freeze outputs stay null. The
subject is the panel stub until panel_admitted.json appears. Lee-Ready is
refused.
"""
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
import orchestrator
import rails


def _freeze_paths():
    return (
        orchestrator.FROZEN_EXPERIMENT,
        orchestrator.EMPTY_RESULTS,
        orchestrator.PACKET,
        orchestrator.KERNEL,
        orchestrator.PANEL_STUB,
        orchestrator.BANDS_REGISTRY,
        orchestrator.LAB_BUNDLE / 'FROZEN_EXPERIMENT.json',
        orchestrator.LAB_BUNDLE / 'results.json',
        orchestrator.GOVERNANCE_BUNDLE / 'FROZEN_EXPERIMENT.json',
        orchestrator.GOVERNANCE_BUNDLE / 'results.json',
        orchestrator.GOVERNANCE_BUNDLE / 'results' / 'EMPTY_RESULTS.json',
    )


class PinTests(unittest.TestCase):
    def test_binding_pins_the_stub_and_the_instruments(self):
        self.assertFalse(orchestrator.PANEL_ADMITTED.exists())
        self.assertFalse(orchestrator.GOVERNANCE_TREE.exists())
        binding = orchestrator.instrument_binding()
        panel = orchestrator.load_panel()
        frozen = json.loads(orchestrator.FROZEN_EXPERIMENT.read_text())
        self.assertEqual(binding['experiment_id'], 'R3-P3-FL-MAKER-TAKER-HARNESS')
        self.assertEqual(binding['knob'], 'analysis_slice')
        self.assertEqual(binding['panel_version'], '2026-09-22.r3-p3-fl-maker-taker-v0')
        self.assertEqual(panel['panel_version'], '2026-09-22.r3-p3-fl-maker-taker-v0')
        self.assertIsNone(panel['admitted_at'])
        self.assertIsNone(binding['admitted_at'])
        self.assertEqual(binding['feebook_commit'], frozen['fee_pin'])
        self.assertEqual(binding['rails_commit'], frozen['rails_pin'])
        self.assertEqual(binding['feebook_commit'], '22371178cb2663250b4762f328069571c48cb551')
        self.assertEqual(binding['rails_commit'], '6a28e0d6254327ea4e6451c781bec56215ac6cac')
        self.assertEqual(binding['examiner_formula_id'], feebook.EXAMINER_FORMULA_ID)
        self.assertEqual(binding['fee_credit_rule_id'], rails.FEE_CREDIT_RULE_ID)
        self.assertEqual(binding['fee_source'], 'feebook')
        self.assertEqual(binding['rails_source'], 'rails')
        self.assertEqual(binding['fee_schema_formula_id'], feebook.EXAMINER_FORMULA_ID)
        self.assertIs(binding['numeric_fee_stored'], False)
        self.assertIs(binding['freshness_is_scorecard'], False)
        self.assertIsNone(binding['strategy_pointer'])
        self.assertIs(binding['lee_ready'], False)
        self.assertIs(frozen['lee_ready'], False)
        self.assertIs(binding['paper_ev'], False)
        self.assertIs(binding['logan_keys_required'], False)
        self.assertIs(binding['live_orders'], False)
        self.assertIs(binding['signal_retune_000'], False)
        self.assertIs(binding['queue_fragility_reopen'], False)
        self.assertIs(binding['cap_sr_reopen'], False)
        self.assertIs(binding['c3_reopen'], False)
        self.assertIs(binding['c5_reopen'], False)
        self.assertIs(binding['c3_strategy_merge'], False)
        self.assertIs(binding['fee_is_knob'], False)
        self.assertTrue(binding['c3_prefer_cite'])
        self.assertEqual(tuple(frozen['scorecard_fields']), orchestrator.SCORECARD_FIELDS)
        self.assertEqual([arm['id'] for arm in frozen['arms']], list(orchestrator.ARMS))
        self.assertEqual(frozen['arms'][0]['slice'], 'maker_vs_taker')
        self.assertEqual(frozen['arms'][1]['slice'], 'fl_bands_10c')
        self.assertIsNone(frozen['results'])
        self.assertIsNone(frozen['pnl'])
        self.assertIs(frozen['logan_keys_required'], False)
        self.assertIs(frozen['signal_retune_000'], False)
        self.assertIs(frozen['queue_fragility_reopen'], False)
        self.assertEqual(binding['packet_sha256'], orchestrator.PACKET_SHA256)
        self.assertEqual(binding['kernel_sha256'], orchestrator.KERNEL_SHA256)
        self.assertEqual(binding['panel_stub_sha256'], orchestrator.PANEL_STUB_SHA256)
        self.assertEqual(binding['bands_registry_sha256'], orchestrator.BANDS_REGISTRY_SHA256)
        self.assertEqual(
            orchestrator.sha256_file(orchestrator.PANEL_STUB),
            orchestrator.PANEL_STUB_SHA256,
        )
        self.assertEqual(
            orchestrator.sha256_file(orchestrator.BANDS_REGISTRY),
            orchestrator.BANDS_REGISTRY_SHA256,
        )
        self.assertEqual(
            sorted(path.name for path in PARENT.glob('kalshi_r3p3_fl_maker_taker_lab_*')),
            ['kalshi_r3p3_fl_maker_taker_lab_20260923'],
        )
        self.assertEqual(Path(feebook.__file__).resolve().parent.name, 'kalshi_feebook_lab_20260922')
        self.assertEqual(Path(rails.__file__).resolve().parent.name, 'kalshi_rails_lab_20260922')
        c3_frozen = json.loads(orchestrator.C3_FROZEN.read_text())
        c5_frozen = json.loads(orchestrator.C5_FROZEN.read_text())
        self.assertIsNone(c3_frozen['results'])
        self.assertIsNone(c3_frozen['pnl'])
        self.assertIsNone(c5_frozen['results'])
        self.assertIsNone(c5_frozen['pnl'])

    def test_packet_copies_match_and_scorecard_stays_null(self):
        frozen_bytes = orchestrator.FROZEN_EXPERIMENT.read_bytes()
        empty_bytes = orchestrator.EMPTY_RESULTS.read_bytes()
        for path in (
            orchestrator.FROZEN_EXPERIMENT,
            orchestrator.LAB_BUNDLE / 'FROZEN_EXPERIMENT.json',
            orchestrator.GOVERNANCE_BUNDLE / 'FROZEN_EXPERIMENT.json',
        ):
            self.assertEqual(path.read_bytes(), frozen_bytes)
            payload = json.loads(path.read_text())
            self.assertIsNone(payload['results'])
            self.assertIsNone(payload['pnl'])
            self.assertIs(payload['lee_ready'], False)
            self.assertIs(payload['logan_keys_required'], False)
            self.assertIs(payload['signal_retune_000'], False)
            self.assertIs(payload['queue_fragility_reopen'], False)
            self.assertEqual(payload['panel_version'], orchestrator.PANEL_VERSION)
            self.assertIsNone(payload['admitted_at'])
        for path in (
            orchestrator.EMPTY_RESULTS,
            orchestrator.LAB_BUNDLE / 'results.json',
            orchestrator.GOVERNANCE_BUNDLE / 'results.json',
            orchestrator.GOVERNANCE_BUNDLE / 'results' / 'EMPTY_RESULTS.json',
        ):
            self.assertEqual(path.read_bytes(), empty_bytes)
            payload = json.loads(path.read_text())
            self.assertEqual(payload['status'], 'EMPTY_RESULTS_PRE_EXAMINER')
            for key in orchestrator.OUTPUT_KEYS:
                self.assertIsNone(payload[key])
        snapshot = orchestrator.frozen_output_snapshot()
        self.assertIsNone(snapshot['frozen.results'])
        self.assertIsNone(snapshot['empty.pnl'])
        self.assertIsNone(snapshot['empty.mz_alpha'])
        self.assertIsNone(snapshot['empty.post_fee_roi_by_band'])
        self.assertIsNone(snapshot['empty.maker_vs_taker_roi_delta'])
        self.assertIsNone(snapshot['empty.settled_join_n'])
        published = orchestrator.published_scorecard()
        orchestrator.assert_null_scorecard(published)
        self.assertEqual(published['status'], 'EMPTY_RESULTS_PRE_EXAMINER')
        self.assertEqual(published['lee_ready'], 'REFUSED')
        self.assertIs(published['paper_ev'], False)

    def test_stub_loads_and_admitted_panel_is_preferred_when_present(self):
        self.assertEqual(orchestrator.select_panel_path(), orchestrator.PANEL_STUB)
        panel = orchestrator.load_panel()
        self.assertEqual(panel['cohort_counts']['trades_sampled_n'], 15)
        self.assertEqual(panel['cohort_counts']['settled_markets_resolved_n'], 0)
        self.assertEqual(panel['cohort_counts']['markets_n'], 3)
        self.assertEqual(len(panel['trades_sample']), 15)
        self.assertIsNone(panel['results'])
        self.assertIsNone(panel['pnl'])
        self.assertIsNone(panel['volume'])
        self.assertIs(panel['binds']['no_lee_ready'], True)
        bands = orchestrator.load_bands_registry()
        self.assertEqual([band['band_id'] for band in bands], ['b%02d' % i for i in range(10)])
        self.assertIsNone(json.loads(orchestrator.BANDS_REGISTRY.read_text())['measurement_roi_by_band'])
        stamped = json.loads(orchestrator.PANEL_STUB.read_text())
        stamped['admitted_at'] = '2026-09-23T18:00:00Z'
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            stub = root / 'panel_stub.json'
            admitted = root / 'panel_admitted.json'
            stub.write_text(orchestrator.PANEL_STUB.read_text())
            admitted.write_text(json.dumps(stamped))
            chosen = orchestrator.select_panel_path(stub, admitted)
            self.assertEqual(chosen, admitted)
            loaded = orchestrator.load_panel(stub, admitted)
            self.assertEqual(loaded['admitted_at'], '2026-09-23T18:00:00Z')
            self.assertEqual(loaded['panel_version'], orchestrator.PANEL_VERSION)
            admitted.unlink()
            self.assertEqual(orchestrator.select_panel_path(stub, admitted), stub)
            stamped['panel_version'] = '2026-09-22.r3-p3-fl-maker-taker-v1'
            rejected = root / 'panel_stub.json'
            rejected.write_text(json.dumps(stamped))
            with self.assertRaises(orchestrator.PanelVersionRefused):
                orchestrator.load_panel(rejected, root / 'missing_admitted.json')

    def test_pinned_labs_are_unmodified(self):
        for commit, path in (
            (orchestrator.FEEBOOK_COMMIT, 'kalshi_feebook_lab_20260922'),
            (orchestrator.RAILS_COMMIT, 'kalshi_rails_lab_20260922'),
        ):
            diff = subprocess.run(
                ['git', 'diff', '--exit-code', commit, '--', path],
                cwd=PARENT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(diff.returncode, 0, diff.stdout + diff.stderr)
            ancestor = subprocess.run(
                ['git', 'merge-base', '--is-ancestor', commit, 'HEAD'],
                cwd=PARENT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(ancestor.returncode, 0, ancestor.stderr)
        for path in orchestrator.DOES_NOT_MODIFY:
            diff = subprocess.run(
                ['git', 'diff', '--exit-code', orchestrator.UNTOUCHED_BASE, '--', path],
                cwd=PARENT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(diff.returncode, 0, path + diff.stdout + diff.stderr)


class SchemaTests(unittest.TestCase):
    def test_native_partition_and_band_membership_keep_roi_null(self):
        before = {path: path.read_bytes() for path in _freeze_paths()}
        maker = orchestrator.conduct(orchestrator.R3P3A0)
        bands = orchestrator.conduct(orchestrator.R3P3A1)
        self.assertEqual(maker['slice'], 'maker_vs_taker')
        self.assertEqual(bands['slice'], 'fl_bands_10c')
        self.assertEqual(maker['fee_pin'], bands['fee_pin'])
        self.assertEqual(maker['rails_pin'], bands['rails_pin'])
        self.assertEqual(maker['source'], 'panel')
        self.assertEqual(bands['source'], 'panel')
        self.assertEqual(maker['panel_settled_markets_resolved_n'], 0)
        self.assertEqual(bands['panel_settled_markets_resolved_n'], 0)
        self.assertEqual(maker['settled_join'], [])
        self.assertEqual(bands['settled_join'], [])
        partitions = {
            (row['taker_outcome_side'], row['taker_book_side']): row
            for row in maker['partitions']
        }
        self.assertEqual(set(partitions), {('no', 'ask'), ('yes', 'bid')})
        self.assertEqual(partitions[('no', 'ask')]['trade_n'], 13)
        self.assertEqual(
            partitions[('yes', 'bid')]['trade_ids'],
            [
                '0723e1ff-5c69-b02e-aa45-1e0cff96d64a',
                '0723e746-dff9-887f-dbaf-9f56384e3d6c',
            ],
        )
        by_band = {row['band_id']: row for row in bands['bands']}
        self.assertEqual(list(by_band), ['b%02d' % i for i in range(10)])
        self.assertEqual(
            by_band['b00']['trade_ids'],
            [
                '0723e1ff-5c69-b02e-aa45-1e0cff96d64a',
                '0723e061-8fd9-9d72-42c7-9974d9ac42b8',
                '0723e061-8fd9-8222-0dfc-2903b54d9130',
                '0723e07b-2ac1-96cc-ab8e-f78e7353d7d5',
                '0723e061-8fd9-93b6-9ee5-b0be8079e0e0',
            ],
        )
        self.assertEqual(by_band['b09']['trade_n'], 10)
        for band_id in ('b01', 'b02', 'b03', 'b04', 'b05', 'b06', 'b07', 'b08'):
            self.assertEqual(by_band[band_id]['trade_n'], 0)
            self.assertEqual(by_band[band_id]['trade_ids'], [])
            self.assertIsNone(by_band[band_id]['post_fee_roi'])
        for report in (maker, bands):
            orchestrator.assert_null_scorecard(report)
            orchestrator.assert_null_scorecard(report['published'])
            self.assertFalse(report['promoted'])
            self.assertIsNone(report['strategy_pointer'])
            self.assertEqual(report['lee_ready'], 'REFUSED')
            self.assertIs(report['paper_ev'], False)
            self.assertIs(report['live_orders'], False)
            self.assertIsNone(report['settled_join_n'])
            self.assertIsNone(report['post_fee_roi_by_band'])
            self.assertIsNone(report['maker_vs_taker_roi_delta'])
            self.assertIsNone(report['mz_alpha'])
            self.assertIsNone(report['mz_psi'])
        for row in list(maker['partitions']) + list(bands['bands']):
            orchestrator.assert_null_scorecard(row)
            self.assertEqual(row['fee_schema']['formula_id'], feebook.EXAMINER_FORMULA_ID)
            self.assertIs(row['fee_schema']['numeric_fee_stored'], False)
            self.assertIsNone(row['fee_schema']['roi'])
            self.assertIsNone(row['fee_schema']['post_fee_roi'])
            self.assertNotIn('fee', row['fee_schema'])
            self.assertNotIn('raw', row['fee_schema'])
            self.assertEqual(row['lee_ready'], 'REFUSED')
            self.assertIsNone(row['aggressor_inference'])
        for path, raw in before.items():
            self.assertEqual(path.read_bytes(), raw)

    def test_band_edges_and_synthetic_stay_out_of_the_freeze(self):
        before = {path: path.read_bytes() for path in _freeze_paths()}
        registry = orchestrator.load_bands_registry()
        self.assertEqual(orchestrator.assign_band('0', registry), 'b00')
        self.assertEqual(orchestrator.assign_band('0.0999', registry), 'b00')
        self.assertEqual(orchestrator.assign_band('0.10', registry), 'b01')
        self.assertEqual(orchestrator.assign_band('0.50', registry), 'b05')
        self.assertEqual(orchestrator.assign_band('0.8999', registry), 'b08')
        self.assertEqual(orchestrator.assign_band('0.90', registry), 'b09')
        self.assertEqual(orchestrator.assign_band('1', registry), 'b09')
        with self.assertRaises(orchestrator.OrchestratorError):
            orchestrator.assign_band('1.0001', registry)
        with self.assertRaises(orchestrator.OrchestratorError):
            orchestrator.assign_band('-0.01', registry)
        maker = orchestrator.conduct_synthetic(orchestrator.R3P3A0)
        bands = orchestrator.conduct_synthetic(orchestrator.R3P3A1)
        self.assertEqual(maker['source'], 'synthetic_schema_standin')
        self.assertEqual(bands['source'], 'synthetic_schema_standin')
        self.assertNotIn('panel_settled_markets_resolved_n', maker)
        by_band = {row['band_id']: row['trade_ids'] for row in bands['bands']}
        self.assertEqual(by_band['b00'], ['syn-b00'])
        self.assertEqual(by_band['b01'], ['syn-b01'])
        self.assertEqual(by_band['b05'], ['syn-b05'])
        self.assertEqual(by_band['b08'], ['syn-b08'])
        self.assertEqual(by_band['b09'], ['syn-b09'])
        for band_id in ('b02', 'b03', 'b04', 'b06', 'b07'):
            self.assertEqual(by_band[band_id], [])
        for report in (maker, bands):
            orchestrator.assert_null_scorecard(report)
            self.assertIsNone(report['post_fee_roi_by_band'])
            self.assertIsNone(report['maker_vs_taker_roi_delta'])
            self.assertEqual(report['settled_join'], [])
        with self.assertRaises(orchestrator.ScorecardPromotionRefused):
            orchestrator.write_scorecard(bands['published'])
        with self.assertRaises(orchestrator.UnknownSlice):
            orchestrator.conduct('R3P3A2')
        for path, raw in before.items():
            self.assertEqual(path.read_bytes(), raw)

    def test_reused_feebook_does_not_fill_the_scorecard(self):
        quote = feebook.order_fee('taker', '1', '0.50', round_up=True)
        self.assertEqual(quote['formula_id'], feebook.EXAMINER_FORMULA_ID)
        self.assertIsInstance(quote['fee'], Decimal)
        schema = orchestrator.fee_schema_object()
        self.assertEqual(schema['formula_id'], feebook.EXAMINER_FORMULA_ID)
        self.assertIs(schema['numeric_fee_stored'], False)
        self.assertNotIn('fee', schema)
        published = orchestrator.published_scorecard()
        for key in orchestrator.SCORECARD_FIELDS:
            self.assertIsNone(published[key])
        self.assertIsNone(published['post_fee_roi_by_band'])
        self.assertIsNone(published['maker_vs_taker_roi_delta'])


class RefuseTests(unittest.TestCase):
    def test_paper_ev_lee_ready_and_invented_settlement_are_refused(self):
        for label in (
            'paper_ev',
            'paper_26pct',
            'paper_maker_50c',
            'author_pnl',
            'lee_ready',
            'invented_settlement',
            'invented_roi',
            'invented_pnl',
            'live_order',
        ):
            with self.assertRaises(orchestrator.AdversaryRefused):
                orchestrator.refuse_adversary(label)
        with self.assertRaises(orchestrator.LeeReadyRefused):
            orchestrator.infer_aggressor('0.99', '0.98', '0.97')
        with self.assertRaises(orchestrator.AdmitRefused):
            orchestrator.run_admit()
        with self.assertRaises(orchestrator.LiveOrdersForbidden):
            orchestrator.execution_adapter()
        with self.assertRaises(orchestrator.LiveOrdersForbidden):
            orchestrator.assert_public_get('POST')
        self.assertIsNone(orchestrator.assert_public_get('GET'))
        source = (ROOT / 'orchestrator.py').read_text()
        for banned in (
            '0.0175',
            '0.07',
            'maker_coefficient',
            'taker_coefficient',
            'common_config',
            'class KalshiExecutionAdapter',
            'urlopen',
            'import queue_fragility',
            'os.environ',
            'api_key',
            'private_key',
            'urllib',
            'requests',
            'midpoint',
            'tick_test',
        ):
            self.assertNotIn(banned, source)
        grok = feebook.grok_unrounded_maker_per_unit('0.50')
        with self.assertRaises(orchestrator.ShadowFeeLiteralRefused):
            orchestrator.assert_examiner_quote(grok)
        with self.assertRaises(orchestrator.ShadowFeeLiteralRefused):
            orchestrator.assert_examiner_quote(Decimal('0.07'))
        bands = orchestrator.load_bands_registry()
        disagreed = {
            'trade_id': 'syn-bad-side',
            'ticker': 'SYN-BAD',
            'yes_price_dollars': '0.50',
            'taker_outcome_side': 'yes',
            'taker_book_side': 'bid',
            'taker_side': 'no',
            'taker_action': None,
            'lee_ready': 'REFUSED',
            'aggressor_inference': None,
            'post_fee_roi': None,
        }
        with self.assertRaises(orchestrator.OrchestratorError):
            orchestrator.normalize_trade(disagreed, bands)
        inferred = dict(disagreed)
        inferred['taker_side'] = 'yes'
        inferred['aggressor_inference'] = 'buy'
        with self.assertRaises(orchestrator.LeeReadyRefused):
            orchestrator.normalize_trade(inferred, bands)
        labeled = dict(disagreed)
        labeled['taker_side'] = 'yes'
        labeled['paper_ev'] = '0.026'
        with self.assertRaises(orchestrator.AdversaryRefused):
            orchestrator.normalize_trade(labeled, bands)
        settled = dict(disagreed)
        settled['taker_side'] = 'yes'
        settled['result'] = 'yes'
        with self.assertRaises(orchestrator.InventedSettlementRefused):
            orchestrator.normalize_trade(settled, bands)
        priced = dict(disagreed)
        priced['taker_side'] = 'yes'
        priced['post_fee_roi'] = '0.01'
        with self.assertRaises(orchestrator.InventedRoiRefused):
            orchestrator.normalize_trade(priced, bands)
        rebinned = dict(disagreed)
        rebinned['taker_side'] = 'yes'
        rebinned['band_id'] = 'b09'
        with self.assertRaises(orchestrator.OrchestratorError):
            orchestrator.normalize_trade(rebinned, bands)
        panel = json.loads(orchestrator.PANEL_STUB.read_text())
        panel['binds']['no_lee_ready'] = False
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'panel_stub.json'
            path.write_text(json.dumps(panel))
            with self.assertRaises(orchestrator.LeeReadyRefused):
                orchestrator.load_panel(path, Path(tmp) / 'missing.json')
        panel = json.loads(orchestrator.PANEL_STUB.read_text())
        panel['binds']['no_live_orders'] = False
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'panel_stub.json'
            path.write_text(json.dumps(panel))
            with self.assertRaises(orchestrator.LiveOrdersForbidden):
                orchestrator.load_panel(path, Path(tmp) / 'missing.json')
        panel = json.loads(orchestrator.PANEL_STUB.read_text())
        panel['markets'][0]['result'] = 'yes'
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'panel_stub.json'
            path.write_text(json.dumps(panel))
            with self.assertRaises(orchestrator.InventedSettlementRefused):
                orchestrator.load_panel(path, Path(tmp) / 'missing.json')
        panel = json.loads(orchestrator.PANEL_STUB.read_text())
        panel['markets'][0]['volume_fp'] = '1'
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'panel_stub.json'
            path.write_text(json.dumps(panel))
            with self.assertRaises(orchestrator.InventedFillRefused):
                orchestrator.load_panel(path, Path(tmp) / 'missing.json')
        panel = json.loads(orchestrator.PANEL_STUB.read_text())
        panel['binds']['refuse_paper_26pct_as_evidence'] = False
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'panel_stub.json'
            path.write_text(json.dumps(panel))
            with self.assertRaises(orchestrator.AdversaryRefused):
                orchestrator.load_panel(path, Path(tmp) / 'missing.json')
        panel = json.loads(orchestrator.PANEL_STUB.read_text())
        panel['measurement_objects']['post_fee_ROI_by_10c_band']['values_by_band'] = {'b09': '0.01'}
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'panel_stub.json'
            path.write_text(json.dumps(panel))
            with self.assertRaises(orchestrator.ScorecardPromotionRefused):
                orchestrator.load_panel(path, Path(tmp) / 'missing.json')
        filled = dict(orchestrator.published_scorecard())
        with self.assertRaises(orchestrator.ScorecardPromotionRefused):
            orchestrator.write_scorecard(filled)
        for key in orchestrator.OUTPUT_KEYS:
            broken = dict(orchestrator.published_scorecard())
            broken[key] = Decimal('1')
            with self.assertRaises(orchestrator.ScorecardPromotionRefused):
                orchestrator.write_scorecard(broken)


if __name__ == '__main__':
    unittest.main()
