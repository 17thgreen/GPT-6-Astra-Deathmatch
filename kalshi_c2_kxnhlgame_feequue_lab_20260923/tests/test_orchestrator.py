"""Unit pins for the C2 KXNHLGAME fee and queue honesty harness.

Schema and pin locks only. In-memory helper calls are not a score and they
are not profit. Freeze outputs stay null. The subject is the panel stub
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
        orchestrator.SCOUT_CANONICAL,
        orchestrator.PANEL_STUB,
        orchestrator.SOURCE_PINS,
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
        stamp = json.loads(orchestrator.CONDUCTOR_STAMP.read_text())
        self.assertEqual(binding['experiment_id'], 'C2-KXNHLGAME-FEEQUEUE-HARNESS')
        self.assertEqual(binding['feature_family'], 'NHL-FQ')
        self.assertEqual(frozen['feature_family'], 'NHL-FQ')
        self.assertEqual(stamp['feature_family'], 'NHL-FQ')
        self.assertEqual(binding['knob'], 'analysis_slice')
        self.assertEqual(frozen['knob'], 'analysis_slice')
        self.assertEqual(stamp['packet_id'], 'C2-KXNHLGAME-FEEQUEUE-HARNESS')
        self.assertEqual(binding['panel_version'], '2026-09-23.c2-kxnhlgame-v0')
        self.assertEqual(panel['panel_version'], '2026-09-23.c2-kxnhlgame-v0')
        self.assertIsNone(panel['admitted_at'])
        self.assertIsNone(binding['admitted_at'])
        self.assertEqual(panel['stub_status'], 'NOT_ADMITTED')
        self.assertEqual(binding['events_n'], 6)
        self.assertEqual(binding['markets_n'], 12)
        self.assertEqual(binding['scout_markets_n'], 66)
        self.assertEqual(binding['scout_events_n'], 33)
        self.assertEqual(len(panel['events']), 6)
        self.assertEqual(len(panel['markets']), 12)
        self.assertIs(binding['panel_subset_of_scout'], True)
        self.assertEqual(binding['feebook_commit'], frozen['fee_pin'])
        self.assertEqual(binding['rails_commit'], frozen['rails_pin'])
        self.assertEqual(binding['feebook_commit'], '22371178cb2663250b4762f328069571c48cb551')
        self.assertEqual(binding['rails_commit'], '6a28e0d6254327ea4e6451c781bec56215ac6cac')
        self.assertIs(binding['fee_import_only'], True)
        self.assertIs(binding['rails_import_only'], True)
        self.assertIs(binding['fee_override_applied'], False)
        self.assertEqual(binding['freeze_fee_channel_cite'], 'quadratic_with_maker_fees')
        self.assertEqual(binding['examiner_formula_id'], feebook.EXAMINER_FORMULA_ID)
        self.assertEqual(binding['fee_credit_rule_id'], rails.FEE_CREDIT_RULE_ID)
        self.assertEqual(binding['fee_source'], 'feebook')
        self.assertEqual(binding['queue_source'], 'rails')
        self.assertEqual(binding['honesty_helpers'], 'hygiene')
        self.assertEqual(binding['probe_series_resolution'], 'default_unknown_series')
        self.assertEqual(binding['lee_ready'], 'REFUSED')
        self.assertIs(binding['probe_scorecard_write'], False)
        self.assertIsNone(binding['strategy_pointer'])
        self.assertEqual(
            binding['nfl_000_pointer'],
            'nfl_factorial_lab_20260921/SHADOW_CANDIDATE_FREEZE.json',
        )
        self.assertIs(binding['signal_port'], False)
        self.assertTrue(orchestrator.NFL_POINTER_PATH.is_file())
        self.assertIs(binding['logan_keys_required'], False)
        self.assertIs(binding['live_orders'], False)
        self.assertIs(binding['signal_retune_000'], False)
        self.assertIs(binding['queue_fragility_reopen'], False)
        self.assertIs(binding['cap_sr_reopen'], False)
        self.assertIs(binding['cap_sr_fx_reopen'], False)
        self.assertIs(binding['l2_reopen'], False)
        self.assertIs(binding['empty_ob_reopen'], False)
        self.assertIs(binding['sot_id_reopen'], False)
        self.assertIs(binding['l2_sf_reopen'], False)
        self.assertIs(binding['admit_py_run'], False)
        self.assertIs(binding['claims_s1_green'], False)
        self.assertEqual(binding['does_not_ungate'], ['S1', 'S2', 'R2-P4'])
        self.assertIs(binding['s1_s2_r2p4_ungated'], False)
        self.assertIs(binding['fee_is_knob'], False)
        self.assertEqual(binding['examiner_status'], 'NOT_SCORED')
        self.assertIs(binding['stub_ready'], False)
        self.assertEqual(tuple(frozen['scorecard_fields']), orchestrator.SCORECARD_FIELDS)
        self.assertEqual([arm['id'] for arm in frozen['arms']], list(orchestrator.ARMS))
        self.assertEqual(frozen['arms'][0]['analysis_slice'], 'maker_vs_taker_native')
        self.assertEqual(frozen['arms'][1]['analysis_slice'], 'content_fresh_vs_stale_bin')
        self.assertEqual(binding['freeze_sha256'], orchestrator.FREEZE_SHA256)
        self.assertEqual(binding['scout_hunt_sha256'], orchestrator.SCOUT_SHA256)
        self.assertEqual(binding['panel_stub_sha256'], orchestrator.PANEL_STUB_SHA256)
        self.assertEqual(binding['source_pins_sha256'], orchestrator.SOURCE_PINS_SHA256)
        self.assertEqual(
            orchestrator.sha256_file(orchestrator.PACKET),
            'a36ec35143a32c7cd24e9fdf2a33f645d356b93e34c131bb1b8a94e3f92e38f5',
        )
        self.assertEqual(
            orchestrator.sha256_file(orchestrator.SCOUT_CANONICAL),
            '1ab794ad688ba31e0178e78294dcdbe50cf2799a71f40245e5a04a80e9dd5762',
        )
        self.assertEqual(
            orchestrator.sha256_file(orchestrator.PANEL_STUB),
            '60d183e7bdcf25adbc94eeeb3bb361b5232c19c0fe3e6a115f45ab3fcb100c79',
        )
        pins = orchestrator.conductor_pin_status()
        self.assertIs(pins['freeze_matches_conductor_claim'], True)
        self.assertIs(pins['scout_hunt_matches_conductor_claim'], True)
        self.assertIs(pins['panel_stub_matches_conductor_claim'], True)
        self.assertIs(pins['conductor_bytes_in_checkout'], True)
        self.assertIs(binding['conductor_bytes_in_checkout'], True)
        self.assertIs(frozen['conductor_bytes_in_checkout'], True)
        self.assertEqual(frozen['packet_sha256'], orchestrator.FREEZE_SHA256)
        self.assertEqual(frozen['scout_hunt_sha256'], orchestrator.SCOUT_SHA256)
        self.assertEqual(frozen['panel_stub_sha256'], orchestrator.PANEL_STUB_SHA256)
        self.assertIsNone(frozen['results'])
        self.assertIsNone(frozen['pnl'])
        self.assertIsNone(stamp['results'])
        self.assertIsNone(stamp['pnl'])
        self.assertEqual(binding['base_commit'], 'ead2cb41d5d171d8972a27b98d144849b6f8c371')
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
        scout_bytes = orchestrator.SCOUT_CANONICAL.read_bytes()
        panel_bytes = orchestrator.PANEL_STUB.read_bytes()
        pins_bytes = orchestrator.SOURCE_PINS.read_bytes()
        for path in (
            orchestrator.FROZEN_EXPERIMENT,
            orchestrator.LAB_BUNDLE / 'FROZEN_EXPERIMENT.json',
            orchestrator.GOVERNANCE_BUNDLE / 'FROZEN_EXPERIMENT.json',
        ):
            self.assertEqual(path.read_bytes(), frozen_bytes)
        for path in (
            orchestrator.PACKET,
            orchestrator.LAB_BUNDLE / orchestrator.FREEZE_NAME,
            PARENT / 'packets' / orchestrator.FREEZE_NAME,
            orchestrator.GOVERNANCE_BUNDLE / orchestrator.FREEZE_NAME,
        ):
            self.assertEqual(path.read_bytes(), packet_bytes)
            self.assertEqual(orchestrator.sha256_file(path), orchestrator.FREEZE_SHA256)
        for directory in orchestrator.owned_dirs():
            self.assertEqual((directory / orchestrator.SCOUT_NAME).read_bytes(), scout_bytes)
            self.assertEqual((directory / 'panel_stub.json').read_bytes(), panel_bytes)
            self.assertEqual((directory / orchestrator.PANEL_ALIAS).read_bytes(), panel_bytes)
            self.assertEqual((directory / orchestrator.SOURCE_PINS_NAME).read_bytes(), pins_bytes)
        self.assertEqual(
            (PARENT / 'packets' / orchestrator.PANEL_ALIAS).read_bytes(),
            panel_bytes,
        )
        self.assertEqual(orchestrator.SCOUT_CANONICAL.read_bytes(), scout_bytes)
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
        self.assertIsNone(snapshot['empty.n_books'])
        published = orchestrator.published_scorecard()
        orchestrator.assert_null_scorecard(published)
        loaded = orchestrator.load_scorecard(orchestrator.EMPTY_RESULTS)
        orchestrator.assert_null_scorecard(loaded)
        self.assertEqual(published['status'], 'EMPTY_RESULTS_PRE_EXAMINER')
        self.assertEqual(published['lee_ready'], 'REFUSED')
        self.assertIsNone(orchestrator.settled_join(panel=orchestrator.load_panel()))

    def test_seed_loads_and_admitted_panel_is_preferred_when_present(self):
        self.assertEqual(orchestrator.select_panel_path(), orchestrator.PANEL_STUB)
        panel = orchestrator.load_panel()
        self.assertEqual(panel['series_ticker'], 'KXNHLGAME')
        self.assertEqual(panel['scout_cite'], orchestrator.SCOUT_CITE)
        self.assertEqual(panel['scout_sha256'], orchestrator.SCOUT_SHA256)
        self.assertEqual(len(panel['events']), 6)
        self.assertEqual(len(panel['markets']), 12)
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
            self.assertEqual(len(loaded['markets']), 12)
            admitted.unlink()
            self.assertEqual(orchestrator.select_panel_path(stub, admitted), stub)
            stamped['panel_version'] = '2026-09-23.c2-kxnhlgame-v1'
            rejected = root / 'panel_stub.json'
            rejected.write_text(json.dumps(stamped))
            with self.assertRaises(orchestrator.PanelVersionRefused):
                orchestrator.load_panel(rejected, root / 'missing_admitted.json')

    def test_panel_markets_are_the_scout_subset(self):
        panel = orchestrator.load_panel()
        index = orchestrator.scout_index()
        self.assertEqual(index['markets_n'], 66)
        self.assertEqual(index['events_n'], 33)
        self.assertEqual(len(panel['markets']), 12)
        for market in panel['markets']:
            self.assertEqual(market, index['by_ticker'][market['ticker']])
            self.assertEqual(market['result'], '')
            self.assertEqual(market['status'], 'active')
            self.assertNotIn('orderbook_fp', market)
            self.assertTrue(market['ticker'].startswith('KXNHLGAME-'))
        for event in panel['events']:
            self.assertIn(event['event_ticker'], index['events'])
            self.assertEqual(event['markets_n'], 2)
        self.assertIsNone(orchestrator.settled_join(panel))

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

    def test_source_pins_and_pre_accept_empty(self):
        pins = json.loads(orchestrator.SOURCE_PINS.read_text())
        self.assertEqual(
            orchestrator.sha256_file(orchestrator.SOURCE_PINS),
            orchestrator.SOURCE_PINS_SHA256,
        )
        self.assertEqual(pins['freeze_sha256'], orchestrator.FREEZE_SHA256)
        self.assertEqual(pins['scout_hunt_sha256'], orchestrator.SCOUT_SHA256)
        self.assertEqual(pins['panel_stub_sha256'], orchestrator.PANEL_STUB_SHA256)
        self.assertEqual(pins['governance_tree'], 'absent')
        self.assertIs(pins['panel_subset_of_scout'], True)
        self.assertIs(pins['signal_port'], False)
        self.assertIs(pins['claims_s1_green'], False)
        for key in orchestrator.OUTPUT_KEYS:
            self.assertIsNone(pins[key])
        hold = json.loads(orchestrator.EXAMINER_HOLD.read_text())
        accept = json.loads(orchestrator.CONDUCTOR_ACCEPT.read_text())
        self.assertEqual(hold['status'], 'NOT_SCORED')
        self.assertIs(hold['stub_ready'], False)
        self.assertEqual(accept['status'], 'ACCEPT_IMPLEMENT_GO')
        self.assertEqual(accept['knob'], 'analysis_slice')
        self.assertIs(accept['claims_s1_green'], False)
        with self.assertRaises(orchestrator.PreAcceptEmptyRefused):
            orchestrator.load_scorecard(orchestrator.PRE_ACCEPT_EMPTY)
        with self.assertRaises(orchestrator.PreAcceptEmptyRefused):
            orchestrator.assert_null_scorecard(json.loads(orchestrator.PRE_ACCEPT_EMPTY.read_text()))


class SchemaTests(unittest.TestCase):
    def test_c2a0_and_c2a1_schema_on_the_panel_stub(self):
        before = {path: path.read_bytes() for path in _freeze_paths()}
        native = orchestrator.conduct(orchestrator.C2A0)
        fresh = orchestrator.conduct(orchestrator.C2A1)
        self.assertEqual(native['analysis_slice'], 'maker_vs_taker_native')
        self.assertEqual(fresh['analysis_slice'], 'content_fresh_vs_stale_bin')
        self.assertEqual(native['event_count'], 6)
        self.assertEqual(fresh['event_count'], 6)
        self.assertEqual(native['market_count'], 12)
        self.assertEqual(fresh['market_count'], 12)
        self.assertEqual(native['scout_markets_n'], 66)
        self.assertEqual(fresh['scout_events_n'], 33)
        self.assertEqual(native['fee_pin'], fresh['fee_pin'])
        self.assertEqual(native['rails_pin'], fresh['rails_pin'])
        self.assertEqual(native['lee_ready'], 'REFUSED')
        self.assertIs(native['signal_port'], False)
        self.assertIs(native['claims_s1_green'], False)
        for report in (native, fresh):
            orchestrator.assert_null_scorecard(report)
            orchestrator.assert_null_scorecard(report['published'])
            self.assertIsNone(report['n_books'])
            self.assertIsNone(report['settled_join_n'])
            self.assertFalse(report['promoted'])
            self.assertEqual(report['source'], 'panel')
        for path, raw in before.items():
            self.assertEqual(path.read_bytes(), raw)

    def test_native_partition_and_fresh_bins_stay_out_of_the_freeze(self):
        before = {path: path.read_bytes() for path in _freeze_paths()}
        native = orchestrator.conduct_native()
        fresh = orchestrator.conduct_fresh()
        self.assertEqual(native['source'], 'synthetic_schema_standin')
        self.assertEqual(native['arm'], 'C2A0')
        self.assertEqual(native['partition_count'], 2)
        by_side = {row['taker_outcome_side']: row for row in native['partitions']}
        self.assertEqual(by_side['yes']['taker_book_side'], 'bid')
        self.assertEqual(by_side['yes']['maker_outcome_side'], 'no')
        self.assertEqual(by_side['no']['taker_book_side'], 'ask')
        self.assertEqual(by_side['no']['maker_outcome_side'], 'yes')
        self.assertEqual(by_side['yes']['lee_ready'], 'REFUSED')
        self.assertIsNone(by_side['yes']['aggressor_inference'])
        self.assertIsNone(by_side['yes']['maker_vs_taker_roi_delta'])
        self.assertIsNone(by_side['yes']['n_books'])
        self.assertEqual(fresh['arm'], 'C2A1')
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
        with self.assertRaises(orchestrator.UnknownSlice):
            orchestrator.conduct('C2A2')
        for path, raw in before.items():
            self.assertEqual(path.read_bytes(), raw)

    def test_c2a1_ignores_taker_side_when_binning(self):
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
            '000',
            'qf_reopen',
            'cap_sr_reopen',
            'cap_sr_fx_reopen',
            'l2_reopen',
            'l2_cat_reopen',
            'l2_sf_reopen',
            'empty_ob_reopen',
            'sot_id_reopen',
            'prop_lq_reopen',
            'admit_py',
            'atl_gb',
        ):
            with self.assertRaises(orchestrator.AdversaryRefused):
                orchestrator.refuse_adversary(label)
        with self.assertRaises(orchestrator.LeeReadyRefused):
            orchestrator.refuse_adversary('lee_ready')
        with self.assertRaises(orchestrator.SignalPortRefused):
            orchestrator.refuse_adversary('signal_port')
        with self.assertRaises(orchestrator.SignalPortRefused):
            orchestrator.port_nfl_000_signal()
        with self.assertRaises(orchestrator.InventedDepthRefused):
            orchestrator.refuse_adversary('invented_depth')
        with self.assertRaises(orchestrator.InventedMarketRefused):
            orchestrator.refuse_adversary('invented_markets')
        with self.assertRaises(orchestrator.S1GreenClaimRefused):
            orchestrator.claim_s1_green()
        for name in ('S1', 'S2', 'R2-P4'):
            with self.assertRaises(orchestrator.UngateRefused):
                orchestrator.ungate(name)
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
                'series_resolution': 'default_unknown_series',
            })
        with self.assertRaises(orchestrator.ShadowFeeLiteralRefused):
            orchestrator.classify_native_taker({
                'ticker': 'KXNHLGAME-SYN-FEE',
                'taker_outcome_side': 'yes',
                'taker_book_side': 'bid',
                'fee_cost': '0.01',
            })
        filled = dict(orchestrator.published_scorecard())
        with self.assertRaises(orchestrator.ScorecardPromotionRefused):
            orchestrator.write_scorecard(filled)
        for key in orchestrator.OUTPUT_KEYS:
            broken = dict(orchestrator.published_scorecard())
            broken[key] = 1
            with self.assertRaises(orchestrator.ScorecardPromotionRefused):
                orchestrator.write_scorecard(broken)

    def test_scout_ticker_depth_and_invented_market_are_refused(self):
        panel = orchestrator.load_panel()
        market = panel['markets'][0]
        with self.assertRaises(orchestrator.InventedFillRefused):
            orchestrator.classify_native_taker({
                'ticker': market['ticker'],
                'taker_outcome_side': 'yes',
                'taker_book_side': 'bid',
                'taker_side': 'yes',
            })
        with self.assertRaises(orchestrator.InventedDepthRefused):
            orchestrator.quote_depth(market)
        with self.assertRaises(orchestrator.InventedDepthRefused):
            orchestrator.classify_fresh_queue({
                'row_id': 'sized',
                'queue_ahead': '3300',
                'current': {'yes_bid': '0.40'},
                'transaction_time': '1',
                'yes_bid_size_fp': '300.00',
            })
        with self.assertRaises(orchestrator.InventedMarketRefused):
            orchestrator._assert_market_object({
                'ticker': 'KXNHLGAME-SYN-NOT-IN-HUNT',
                'event_ticker': 'KXNHLGAME-SYN',
                'status': 'active',
                'result': '',
            }, orchestrator.scout_index())


if __name__ == '__main__':
    unittest.main()
