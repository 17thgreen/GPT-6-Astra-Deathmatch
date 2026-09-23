"""Unit pins for the S4 KXNCAAFGAME fee and queue honesty harness.

Schema and pin locks only. In-memory helper calls are not a score and they
are not profit. Freeze outputs stay null. The subject is the panel seed
until panel_admitted.json appears.
"""
import json
import subprocess
import sys
import tempfile
import unittest
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
    def test_binding_pins_the_seed_and_the_instruments(self):
        self.assertFalse(orchestrator.PANEL_ADMITTED.exists())
        self.assertFalse(orchestrator.GOVERNANCE_TREE.exists())
        binding = orchestrator.instrument_binding()
        panel = orchestrator.load_panel()
        frozen = json.loads(orchestrator.FROZEN_EXPERIMENT.read_text())
        self.assertEqual(binding['experiment_id'], 'S4-KXNCAAFGAME-FEEQUEUE-HARNESS')
        self.assertEqual(binding['feature_family'], 'NCAAF-FQ')
        self.assertEqual(binding['knob'], 'honesty_partition')
        self.assertEqual(binding['panel_version'], '2026-09-22.s4-kxncaafgame-v0')
        self.assertEqual(panel['panel_version'], '2026-09-22.s4-kxncaafgame-v0')
        self.assertIsNone(panel['admitted_at'])
        self.assertIsNone(binding['admitted_at'])
        self.assertEqual(binding['events_n'], 113)
        self.assertEqual(len(panel['events']), 113)
        self.assertIsNone(panel.get('markets'))
        self.assertIsNone(panel.get('cohort_counts'))
        self.assertEqual(panel['freeze_packet_sha256'], orchestrator.KERNEL_SHA256)
        self.assertEqual(binding['conductor_events_n_claim'], 113)
        self.assertEqual(binding['feebook_commit'], frozen['fee_pin'])
        self.assertEqual(binding['rails_commit'], frozen['rails_pin'])
        self.assertEqual(binding['feebook_commit'], '22371178cb2663250b4762f328069571c48cb551')
        self.assertEqual(binding['rails_commit'], '6a28e0d6254327ea4e6451c781bec56215ac6cac')
        self.assertEqual(binding['examiner_formula_id'], feebook.EXAMINER_FORMULA_ID)
        self.assertEqual(binding['fee_credit_rule_id'], rails.FEE_CREDIT_RULE_ID)
        self.assertEqual(binding['fee_source'], 'feebook')
        self.assertEqual(binding['queue_source'], 'rails')
        self.assertEqual(binding['honesty_helpers'], 'hygiene')
        self.assertEqual(binding['lee_ready'], 'REFUSED')
        self.assertIs(binding['probe_scorecard_write'], False)
        self.assertIsNone(binding['strategy_pointer'])
        self.assertIs(binding['logan_keys_required'], False)
        self.assertIs(binding['live_orders'], False)
        self.assertIs(binding['signal_retune_000'], False)
        self.assertIs(binding['queue_fragility_reopen'], False)
        self.assertIs(binding['cap_sr_reopen'], False)
        self.assertIs(binding['admit_py_run'], False)
        self.assertIs(binding['r1_p2_challenger_bakeoff'], False)
        self.assertIs(binding['fee_is_knob'], False)
        self.assertEqual(tuple(frozen['scorecard_fields']), orchestrator.SCORECARD_FIELDS)
        self.assertEqual([arm['id'] for arm in frozen['arms']], list(orchestrator.ARMS))
        self.assertEqual(frozen['arms'][0]['partition'], 'maker_vs_taker_native')
        self.assertEqual(frozen['arms'][1]['partition'], 'content_fresh_vs_stale_bin')
        self.assertEqual(binding['packet_sha256'], orchestrator.PACKET_SHA256)
        self.assertEqual(binding['kernel_sha256'], orchestrator.KERNEL_SHA256)
        self.assertEqual(binding['panel_stub_sha256'], orchestrator.PANEL_STUB_SHA256)
        self.assertEqual(
            orchestrator.sha256_file(orchestrator.PACKET),
            orchestrator.PACKET_SHA256,
        )
        self.assertEqual(
            orchestrator.sha256_file(orchestrator.KERNEL),
            orchestrator.KERNEL_SHA256,
        )
        self.assertEqual(
            orchestrator.sha256_file(orchestrator.PANEL_STUB),
            orchestrator.PANEL_STUB_SHA256,
        )
        self.assertEqual(
            binding['conductor_packet_sha256_claim'],
            '3318204bf6e962f4f3372dad8c0f302e62d85c26b855de7369718654d0114728',
        )
        self.assertEqual(
            binding['conductor_parent_freeze_sha256_claim'],
            '9e6556c150c726b679ac8393f1f5338cf983489259b0f34cdedf221c030be795',
        )
        self.assertEqual(
            binding['conductor_panel_stub_sha256_claim'],
            '38167d11da5842bc4d39e6e7dcaab20a67294c735ba14d8bbeafde3154c6342a',
        )
        self.assertEqual(orchestrator.PACKET_SHA256, orchestrator.CONDUCTOR_PACKET_SHA256)
        self.assertEqual(orchestrator.KERNEL_SHA256, orchestrator.CONDUCTOR_KERNEL_SHA256)
        self.assertEqual(orchestrator.PANEL_STUB_SHA256, orchestrator.CONDUCTOR_PANEL_STUB_SHA256)
        pins = orchestrator.conductor_pin_status()
        self.assertIs(pins['packet_matches_conductor_claim'], True)
        self.assertIs(pins['kernel_matches_conductor_claim'], True)
        self.assertIs(pins['panel_stub_matches_conductor_claim'], True)
        self.assertIs(pins['conductor_bytes_in_checkout'], True)
        self.assertIs(binding['conductor_bytes_in_checkout'], True)
        self.assertIs(binding['packet_matches_conductor_claim'], True)
        self.assertIs(frozen['conductor_bytes_in_checkout'], True)
        self.assertEqual(frozen['packet_sha256'], orchestrator.PACKET_SHA256)
        self.assertEqual(frozen['parent_freeze_sha256'], orchestrator.KERNEL_SHA256)
        self.assertEqual(frozen['panel_stub_sha256'], orchestrator.PANEL_STUB_SHA256)
        self.assertIsNone(frozen['results'])
        self.assertIsNone(frozen['pnl'])
        self.assertEqual(binding['base_commit'], '6626c6892298b015cf63688081545e27363226bc')
        self.assertEqual(Path(feebook.__file__).resolve().parent.name, 'kalshi_feebook_lab_20260922')
        self.assertEqual(Path(rails.__file__).resolve().parent.name, 'kalshi_rails_lab_20260922')
        self.assertEqual(
            Path(orchestrator.hygiene.__file__).resolve().parent.name,
            'kalshi_r2p1_hygiene_000_lab_20260922',
        )

    def test_packet_copies_match_and_scorecard_stays_null(self):
        frozen_bytes = orchestrator.FROZEN_EXPERIMENT.read_bytes()
        empty_bytes = orchestrator.EMPTY_RESULTS.read_bytes()
        packet_bytes = orchestrator.PACKET.read_bytes()
        kernel_bytes = orchestrator.KERNEL.read_bytes()
        for path in (
            orchestrator.FROZEN_EXPERIMENT,
            orchestrator.LAB_BUNDLE / 'FROZEN_EXPERIMENT.json',
            orchestrator.GOVERNANCE_BUNDLE / 'FROZEN_EXPERIMENT.json',
        ):
            self.assertEqual(path.read_bytes(), frozen_bytes)
        for path in (
            orchestrator.PACKET,
            orchestrator.LAB_BUNDLE / orchestrator.PACKET_NAME,
            PARENT / 'packets' / orchestrator.PACKET_NAME,
            orchestrator.GOVERNANCE_BUNDLE / orchestrator.PACKET_NAME,
        ):
            self.assertEqual(path.read_bytes(), packet_bytes)
        for path in (
            orchestrator.KERNEL,
            orchestrator.LAB_BUNDLE / orchestrator.KERNEL_NAME,
            PARENT / 'packets' / orchestrator.KERNEL_NAME,
            orchestrator.GOVERNANCE_BUNDLE / orchestrator.KERNEL_NAME,
        ):
            self.assertEqual(path.read_bytes(), kernel_bytes)
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
        self.assertIsNone(snapshot['empty.maker_vs_taker_roi_delta'])
        self.assertIsNone(snapshot['empty.fresh_vs_stale_gap'])
        self.assertIsNone(snapshot['empty.settled_join_n'])
        published = orchestrator.published_scorecard()
        orchestrator.assert_null_scorecard(published)
        self.assertEqual(published['status'], 'EMPTY_RESULTS_PRE_EXAMINER')
        self.assertEqual(published['lee_ready'], 'REFUSED')

    def test_seed_loads_and_admitted_panel_is_preferred_when_present(self):
        self.assertEqual(orchestrator.select_panel_path(), orchestrator.PANEL_STUB)
        panel = orchestrator.load_panel()
        self.assertEqual(panel['series_ticker'], 'KXNCAAFGAME')
        self.assertNotIn('cohort_counts', panel)
        self.assertNotIn('markets', panel)
        self.assertEqual(len(panel['events']), 113)
        self.assertIsNone(panel['results'])
        self.assertIsNone(panel['pnl'])
        self.assertIsNone(panel['volume'])
        for event in panel['events']:
            self.assertIsNone(event['volume_fp'])
            self.assertIsNone(event['volume_24h_fp'])
            self.assertIsNone(event['open_interest_fp'])
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
            stamped['panel_version'] = '2026-09-22.s4-kxncaafgame-v1'
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
                ['git', 'diff', '--exit-code', orchestrator.BASE_COMMIT, '--', path],
                cwd=PARENT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(diff.returncode, 0, path + diff.stdout + diff.stderr)


class SchemaTests(unittest.TestCase):
    def test_s4a0_and_s4a1_schema_on_the_panel_stub(self):
        before = {path: path.read_bytes() for path in _freeze_paths()}
        native = orchestrator.conduct(orchestrator.S4A0)
        fresh = orchestrator.conduct(orchestrator.S4A1)
        self.assertEqual(native['partition'], 'maker_vs_taker_native')
        self.assertEqual(fresh['partition'], 'content_fresh_vs_stale_bin')
        self.assertEqual(native['event_count'], 113)
        self.assertEqual(fresh['event_count'], 113)
        self.assertIsNone(native['market_count'])
        self.assertIsNone(fresh['market_count'])
        self.assertNotIn('cohort_note', native)
        self.assertNotIn('cohort_note', fresh)
        self.assertEqual(native['fee_pin'], fresh['fee_pin'])
        self.assertEqual(native['rails_pin'], fresh['rails_pin'])
        self.assertEqual(native['lee_ready'], 'REFUSED')
        for report in (native, fresh):
            orchestrator.assert_null_scorecard(report)
            orchestrator.assert_null_scorecard(report['published'])
            self.assertFalse(report['promoted'])
            self.assertEqual(report['source'], 'panel')
        for path, raw in before.items():
            self.assertEqual(path.read_bytes(), raw)

    def test_native_partition_and_fresh_bins_stay_out_of_the_freeze(self):
        before = {path: path.read_bytes() for path in _freeze_paths()}
        native = orchestrator.conduct_native()
        fresh = orchestrator.conduct_fresh()
        self.assertEqual(native['source'], 'synthetic_schema_standin')
        self.assertEqual(native['arm'], 'S4A0')
        self.assertEqual(native['partition_count'], 2)
        by_side = {row['taker_outcome_side']: row for row in native['partitions']}
        self.assertEqual(by_side['yes']['taker_book_side'], 'bid')
        self.assertEqual(by_side['yes']['maker_outcome_side'], 'no')
        self.assertEqual(by_side['no']['taker_book_side'], 'ask')
        self.assertEqual(by_side['no']['maker_outcome_side'], 'yes')
        self.assertEqual(by_side['yes']['lee_ready'], 'REFUSED')
        self.assertIsNone(by_side['yes']['aggressor_inference'])
        self.assertIsNone(by_side['yes']['maker_vs_taker_roi_delta'])
        self.assertEqual(fresh['arm'], 'S4A1')
        self.assertEqual(fresh['bin_count'], 3)
        flags = {(row['content_fresh_flag'], row['queue_attribution_bin']) for row in fresh['bins']}
        self.assertEqual(flags, {(True, 'q3300'), (False, 'q3300'), (False, 'q10000')})
        for row in fresh['bins']:
            self.assertIsNone(row['fresh_vs_stale_gap'])
            self.assertEqual(row['lee_ready'], 'REFUSED')
        for report in (native, fresh):
            orchestrator.assert_null_scorecard(report)
        with self.assertRaises(orchestrator.ScorecardPromotionRefused):
            orchestrator.write_scorecard(native['published'])
        with self.assertRaises(orchestrator.UnknownPartition):
            orchestrator.conduct('S4A2')
        for path, raw in before.items():
            self.assertEqual(path.read_bytes(), raw)

    def test_s4a1_ignores_taker_side_when_binning(self):
        base = {
            'queue_ahead': '3300',
            'previous': None,
            'current': {'yes_bid': '0.40'},
            'transaction_time': '1',
            'keepalive': False,
        }
        yes_row = dict(base, row_id='yes-side', taker_outcome_side='yes')
        no_row = dict(base, row_id='no-side', taker_outcome_side='no')
        bins = orchestrator.partition_fresh([yes_row, no_row])
        self.assertEqual(len(bins), 1)
        self.assertEqual(bins[0]['row_n'], 2)
        self.assertIs(bins[0]['content_fresh_flag'], True)
        self.assertEqual(bins[0]['queue_attribution_bin'], 'q3300')
        self.assertIsNone(bins[0]['fresh_vs_stale_gap'])


class RefuseTests(unittest.TestCase):
    def test_lee_ready_is_refused_on_every_input(self):
        samples = (
            None,
            {},
            {'taker_outcome_side': 'yes', 'taker_book_side': 'bid', 'taker_side': 'yes'},
            {'classifier': 'lee-ready'},
            {'lee_ready': True},
            'quote',
        )
        for sample in samples:
            with self.assertRaises(orchestrator.LeeReadyRefused):
                orchestrator.infer_lee_ready(sample)
        with self.assertRaises(orchestrator.LeeReadyRefused):
            orchestrator.classify_native_taker({
                'taker_outcome_side': 'yes',
                'taker_book_side': 'bid',
                'lee_ready': True,
            })
        with self.assertRaises(orchestrator.LeeReadyRefused):
            orchestrator.classify_native_taker({
                'taker_outcome_side': 'yes',
                'taker_book_side': 'bid',
                'classifier': 'LeeReady',
            })
        with self.assertRaises(orchestrator.LeeReadyRefused):
            orchestrator.classify_native_taker({
                'taker_outcome_side': 'no',
                'taker_book_side': 'ask',
                'aggressor_inference': 'buy',
            })
        with self.assertRaises(orchestrator.TakerFieldRefused):
            orchestrator.classify_native_taker({
                'taker_outcome_side': 'yes',
                'taker_book_side': 'ask',
                'lee_ready': 'REFUSED',
            })
        with self.assertRaises(orchestrator.TakerFieldRefused):
            orchestrator.classify_native_taker({'yes_price_dollars': '0.40'})
        with self.assertRaises(orchestrator.InventedFillRefused):
            orchestrator.classify_native_taker({
                'taker_outcome_side': 'yes',
                'taker_book_side': 'bid',
                'result': 'yes',
            })

    def test_live_orders_fee_literals_and_reopens_are_refused(self):
        for label in (
            'live_orders',
            'logan_keys',
            'invented_pnl',
            'invented_fills',
            'q6_retune',
            'qf_reopen',
            'cap_sr_reopen',
            'admit_py',
            'r1_p2_challenger',
            'q7_arm_b',
        ):
            with self.assertRaises(orchestrator.AdversaryRefused):
                orchestrator.refuse_adversary(label)
        with self.assertRaises(orchestrator.LeeReadyRefused):
            orchestrator.refuse_adversary('lee_ready')
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
        ):
            self.assertNotIn(banned, source)
        grok = feebook.grok_unrounded_maker_per_unit('0.50')
        with self.assertRaises(orchestrator.ShadowFeeLiteralRefused):
            orchestrator.assert_examiner_quote(grok)
        with self.assertRaises(orchestrator.ShadowFeeLiteralRefused):
            orchestrator.assert_examiner_quote({
                'formula_id': orchestrator.hygiene.INHERITED_MODEL_ID,
            })
        filled = dict(orchestrator.published_scorecard())
        with self.assertRaises(orchestrator.ScorecardPromotionRefused):
            orchestrator.write_scorecard(filled)
        for key in orchestrator.OUTPUT_KEYS:
            broken = dict(orchestrator.published_scorecard())
            broken[key] = 1
            with self.assertRaises(orchestrator.ScorecardPromotionRefused):
                orchestrator.write_scorecard(broken)


if __name__ == '__main__':
    unittest.main()
