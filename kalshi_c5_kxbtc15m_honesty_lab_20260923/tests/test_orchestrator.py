"""Unit pins for the C5 KXBTC15M fee and queue honesty harness.

Schema and pin locks only. In-memory helper calls are not a score and they
are not profit. Freeze outputs stay null. The subject is the panel stub
until panel_admitted.json appears.
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
        self.assertEqual(binding['experiment_id'], 'C5-KXBTC15M-HONESTY-HARNESS')
        self.assertEqual(binding['knob'], 'honesty_stress_cadence')
        self.assertEqual(binding['panel_version'], '2026-09-22.c5-kxbtc15m-v0')
        self.assertEqual(panel['panel_version'], '2026-09-22.c5-kxbtc15m-v0')
        self.assertIsNone(panel['admitted_at'])
        self.assertIsNone(binding['admitted_at'])
        self.assertEqual(binding['feebook_commit'], frozen['fee_pin'])
        self.assertEqual(binding['rails_commit'], frozen['rails_pin'])
        self.assertEqual(binding['feebook_commit'], '22371178cb2663250b4762f328069571c48cb551')
        self.assertEqual(binding['rails_commit'], '6a28e0d6254327ea4e6451c781bec56215ac6cac')
        self.assertEqual(binding['examiner_formula_id'], feebook.EXAMINER_FORMULA_ID)
        self.assertEqual(binding['fee_credit_rule_id'], rails.FEE_CREDIT_RULE_ID)
        self.assertEqual(binding['fee_source'], 'feebook')
        self.assertEqual(binding['queue_source'], 'rails')
        self.assertEqual(binding['honesty_helpers'], 'hygiene')
        self.assertEqual(binding['probe_formula_id'], feebook.EXAMINER_FORMULA_ID)
        self.assertIs(binding['probe_scorecard_write'], False)
        self.assertNotIn('fee_delta', binding)
        self.assertIsNone(binding['strategy_pointer'])
        self.assertIs(binding['live_crypto_trading'], False)
        self.assertIs(binding['logan_keys_required'], False)
        self.assertIs(binding['live_orders'], False)
        self.assertIs(binding['signal_retune_000'], False)
        self.assertIs(binding['queue_fragility_reopen'], False)
        self.assertIs(binding['bacchus_port'], False)
        self.assertIs(binding['cap_sr_reopen'], False)
        self.assertIs(binding['c3_implemented'], False)
        self.assertIs(binding['fee_is_knob'], False)
        self.assertEqual(binding['examiner_fee_fields'], orchestrator.EXAMINER_FEE_FIELDS)
        self.assertEqual(tuple(frozen['scorecard_fields']), orchestrator.SCORECARD_FIELDS)
        self.assertEqual([arm['id'] for arm in frozen['arms']], list(orchestrator.ARMS))
        self.assertEqual(frozen['arms'][0]['cadence'], 'per_window')
        self.assertEqual(frozen['arms'][1]['cadence'], 'multi_window_stack')
        self.assertEqual(binding['packet_sha256'], orchestrator.PACKET_SHA256)
        self.assertEqual(binding['kernel_sha256'], orchestrator.KERNEL_SHA256)
        self.assertEqual(binding['panel_stub_sha256'], orchestrator.PANEL_STUB_SHA256)
        self.assertEqual(
            orchestrator.sha256_file(orchestrator.PANEL_STUB),
            orchestrator.PANEL_STUB_SHA256,
        )
        self.assertEqual(
            sorted(path.name for path in PARENT.glob('kalshi_c5_kxbtc15m_honesty_lab_*')),
            ['kalshi_c5_kxbtc15m_honesty_lab_20260923'],
        )
        self.assertEqual(Path(feebook.__file__).resolve().parent.name, 'kalshi_feebook_lab_20260922')
        self.assertEqual(Path(rails.__file__).resolve().parent.name, 'kalshi_rails_lab_20260922')
        self.assertEqual(
            Path(orchestrator.hygiene.__file__).resolve().parent.name,
            'kalshi_r2p1_hygiene_000_lab_20260922',
        )

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
            self.assertIs(payload['live_crypto_trading'], False)
            self.assertIs(payload['logan_keys_required'], False)
            self.assertIs(payload['signal_retune_000'], False)
            self.assertIs(payload['queue_fragility_reopen'], False)
            self.assertIs(payload['bacchus_port'], False)
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
        self.assertIsNone(snapshot['empty.turnover_stress_flag'])
        published = orchestrator.published_scorecard()
        orchestrator.assert_null_scorecard(published)
        self.assertEqual(published['status'], 'EMPTY_RESULTS_PRE_EXAMINER')

    def test_stub_loads_and_admitted_panel_is_preferred_when_present(self):
        self.assertEqual(orchestrator.select_panel_path(), orchestrator.PANEL_STUB)
        panel = orchestrator.load_panel()
        self.assertEqual(panel['series_ticker'], 'KXBTC15M')
        self.assertEqual(panel['cohort_counts']['markets_n'], 1)
        self.assertEqual(panel['markets'][0]['market_ticker'], 'KXBTC15M-26SEP222045-45')
        self.assertIsNone(panel['markets'][0]['volume_fp'])
        self.assertIsNone(panel['results'])
        self.assertIsNone(panel['pnl'])
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
            stamped['panel_version'] = '2026-09-22.c5-kxbtc15m-v1'
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
                ['git', 'diff', '--exit-code', orchestrator.CAP_SR_BASE, '--', path],
                cwd=PARENT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(diff.returncode, 0, path + diff.stdout + diff.stderr)

    def test_reused_helpers_agree_and_do_not_fill_the_scorecard(self):
        self.assertEqual(
            orchestrator.sibling_agreement(rails.QUEUE_AHEAD_DEFAULT)['queue_attribution_bin'],
            'q3300',
        )
        self.assertEqual(
            orchestrator.sibling_agreement(rails.STRESS_QUEUE_AHEAD)['queue_attribution_bin'],
            'q10000',
        )
        outside = rails.QUEUE_AHEAD_DEFAULT + 1
        agreed = orchestrator.sibling_agreement(outside)
        self.assertEqual(agreed['queue_attribution_bin'], orchestrator.hygiene.OUTSIDE_BIN)
        self.assertEqual(agreed['examiner_fee_fields'], orchestrator.EXAMINER_FEE_FIELDS)
        quote = feebook.order_fee('taker', '1', '0.50', round_up=True, series='KXBTC15M')
        delta = orchestrator.hygiene.fee_delta(
            'taker', '1', '0.50', quote['rate'], series='KXBTC15M',
        )
        self.assertEqual(delta['examiner_formula_id'], feebook.EXAMINER_FORMULA_ID)
        self.assertIsInstance(delta['fee_delta'], Decimal)
        gap = orchestrator.hygiene.freshness_gap_seconds('90', '45')
        self.assertEqual(gap, Decimal('45'))
        matched = orchestrator.hygiene.queue_bin_mismatch(rails.QUEUE_AHEAD_DEFAULT, 'q3300')
        mismatched = orchestrator.hygiene.queue_bin_mismatch(rails.STRESS_QUEUE_AHEAD, 'q3300')
        self.assertIs(matched['queue_bin_mismatch'], False)
        self.assertIs(mismatched['queue_bin_mismatch'], True)
        self.assertIsNone(orchestrator.turnover_stress_flag(None))
        published = orchestrator.published_scorecard()
        for key in orchestrator.SCORECARD_FIELDS:
            self.assertIsNone(published[key])


class SchemaTests(unittest.TestCase):
    def test_c5h0_and_c5h1_schema_on_the_stub(self):
        before = {path: path.read_bytes() for path in _freeze_paths()}
        per_window = orchestrator.conduct(orchestrator.C5H0)
        stacked = orchestrator.conduct(orchestrator.C5H1)
        self.assertEqual(per_window['cadence'], 'per_window')
        self.assertIs(per_window['stacked'], False)
        self.assertEqual(per_window['window_count'], 1)
        self.assertNotIn('cohort_note', per_window)
        self.assertEqual(stacked['cadence'], 'multi_window_stack')
        self.assertIs(stacked['stacked'], True)
        self.assertEqual(stacked['window_count'], 1)
        self.assertEqual(stacked['cohort_note'], 'stub_n_expand_only_after_admit')
        self.assertEqual(per_window['fee_pin'], stacked['fee_pin'])
        self.assertEqual(per_window['rails_pin'], stacked['rails_pin'])
        self.assertEqual(
            per_window['windows'][0]['market_ticker'],
            'KXBTC15M-26SEP222045-45',
        )
        self.assertEqual(
            stacked['windows'][0]['market_ticker'],
            per_window['windows'][0]['market_ticker'],
        )
        for report in (per_window, stacked):
            orchestrator.assert_null_scorecard(report)
            orchestrator.assert_null_scorecard(report['published'])
            self.assertFalse(report['promoted'])
            self.assertIsNone(report['strategy_pointer'])
            self.assertIs(report['live_crypto_trading'], False)
            self.assertIs(report['bacchus_port'], False)
            self.assertEqual(report['source'], 'panel')
            for key in orchestrator.SCORECARD_FIELDS:
                self.assertIsNone(report['windows'][0][key])
        for path, raw in before.items():
            self.assertEqual(path.read_bytes(), raw)

    def test_c5h1_synthetic_stack_stays_out_of_the_freeze(self):
        before = {path: path.read_bytes() for path in _freeze_paths()}
        stacked = orchestrator.conduct_synthetic(orchestrator.C5H1)
        per_window = orchestrator.conduct_synthetic(orchestrator.C5H0)
        self.assertEqual(stacked['source'], 'synthetic_schema_standin')
        self.assertEqual(stacked['window_count'], 2)
        self.assertIs(stacked['stacked'], True)
        self.assertNotIn('cohort_note', stacked)
        self.assertEqual(
            [row['market_ticker'] for row in stacked['windows']],
            ['KXBTC15M-SYN-A-00', 'KXBTC15M-SYN-B-15'],
        )
        self.assertIs(per_window['stacked'], False)
        self.assertEqual(per_window['cadence'], 'per_window')
        self.assertEqual(per_window['window_count'], 2)
        for report in (stacked, per_window):
            orchestrator.assert_null_scorecard(report)
            for row in report['windows']:
                for key in orchestrator.OUTPUT_KEYS:
                    self.assertIsNone(row[key])
        with self.assertRaises(orchestrator.ScorecardPromotionRefused):
            orchestrator.write_scorecard(stacked['published'])
        with self.assertRaises(orchestrator.UnknownCadence):
            orchestrator.conduct('C5H2')
        for path, raw in before.items():
            self.assertEqual(path.read_bytes(), raw)


class RefuseTests(unittest.TestCase):
    def test_live_crypto_bacchus_and_live_orders_are_refused(self):
        for label in (
            'live_crypto_trading',
            'live_crypto',
            'bacchus_port',
            'bacchus',
            'kxeth15m_strategy_port',
            'kxeth15m',
            'invented_pnl',
        ):
            with self.assertRaises(orchestrator.AdversaryRefused):
                orchestrator.refuse_adversary(label)
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
            'import bacchus',
            'kxeth15m-research',
        ):
            self.assertNotIn(banned, source)
        grok = feebook.grok_unrounded_maker_per_unit('0.50')
        with self.assertRaises(orchestrator.ShadowFeeLiteralRefused):
            orchestrator.assert_examiner_quote(grok)
        with self.assertRaises(orchestrator.ShadowFeeLiteralRefused):
            orchestrator.assert_examiner_quote({
                'formula_id': orchestrator.hygiene.INHERITED_MODEL_ID,
            })
        with self.assertRaises(orchestrator.InventedInventoryRefused):
            orchestrator.turnover_stress_flag('1')
        panel = json.loads(orchestrator.PANEL_STUB.read_text())
        panel['binds']['no_live_crypto_trading'] = False
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'panel_stub.json'
            path.write_text(json.dumps(panel))
            with self.assertRaises(orchestrator.AdversaryRefused):
                orchestrator.load_panel(path, Path(tmp) / 'missing.json')
        panel = json.loads(orchestrator.PANEL_STUB.read_text())
        panel['binds']['no_bacchus_or_kxeth15m_strategy_port'] = False
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'panel_stub.json'
            path.write_text(json.dumps(panel))
            with self.assertRaises(orchestrator.AdversaryRefused):
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
