"""Unit pins for the ETH KXETH15M fee and queue honesty harness.

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
        self.assertEqual(binding['experiment_id'], 'ETH-KXETH15M-FEEQUEUE-HARNESS')
        self.assertEqual(binding['feature_family'], 'ETH-FQ')
        self.assertEqual(frozen['feature_family'], 'ETH-FQ')
        self.assertEqual(stamp['feature_family'], 'ETH-FQ')
        self.assertEqual(binding['knob'], 'analysis_slice')
        self.assertEqual(frozen['knob'], 'analysis_slice')
        self.assertEqual(stamp['packet_id'], 'ETH-KXETH15M-FEEQUEUE-HARNESS')
        self.assertEqual(stamp['status'], 'FROZEN')
        self.assertEqual(binding['panel_version'], '2026-09-23.eth-kxeth15m-v0')
        self.assertEqual(panel['panel_version'], '2026-09-23.eth-kxeth15m-v0')
        self.assertIsNone(panel['admitted_at'])
        self.assertIsNone(binding['admitted_at'])
        self.assertEqual(panel['stub_status'], 'NOT_ADMITTED')
        self.assertEqual(binding['events_n'], 1)
        self.assertEqual(binding['markets_n'], 1)
        self.assertEqual(binding['scout_markets_n'], 1)
        self.assertEqual(binding['scout_events_n'], 1)
        self.assertEqual(len(panel['events']), 1)
        self.assertEqual(len(panel['markets']), 1)
        self.assertIs(binding['panel_subset_of_scout'], True)
        self.assertIs(binding['panel_full_scout'], True)
        self.assertEqual(binding['missing_occurrence_datetime_n'], 0)
        self.assertIs(binding['occurrence_datetime_invented'], False)
        self.assertIs(binding['fill_density_invented'], False)
        self.assertEqual(binding['feebook_commit'], frozen['fee_pin'])
        self.assertEqual(binding['rails_commit'], frozen['rails_pin'])
        self.assertEqual(binding['feebook_commit'], '22371178cb2663250b4762f328069571c48cb551')
        self.assertEqual(binding['rails_commit'], '6a28e0d6254327ea4e6451c781bec56215ac6cac')
        self.assertIs(binding['fee_import_only'], True)
        self.assertIs(binding['rails_import_only'], True)
        self.assertIs(binding['fee_override_applied'], False)
        self.assertEqual(binding['freeze_fee_channel_cite'], 'quadratic')
        self.assertEqual(binding['series_fee_type'], 'quadratic')
        self.assertEqual(binding['series_fee_multiplier'], 1)
        self.assertIs(binding['c5_reopen'], False)
        self.assertIs(binding['atp_fq_reopen'], False)
        self.assertIs(binding['bacchus_strategy_port'], False)
        self.assertIs(binding['kxeth15m_strategy_port'], False)
        self.assertIs(binding['r3_p1_in_scope'], False)
        self.assertIs(binding['r3_p2_in_scope'], False)
        self.assertIs(binding['live_crypto_trading'], False)
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
        self.assertIs(binding['nhl_fq_reopen'], False)
        self.assertIs(binding['cpi_fq_reopen'], False)
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
            '9cae3bad089e6e18bee22694a36a1a2c18db33935a315766cd6bd8f8476aa83a',
        )
        self.assertEqual(
            orchestrator.sha256_file(orchestrator.SCOUT_CANONICAL),
            '18f70001c8d68418d435e2016b756f90753e374a92d323f8e999f76215d9cf9c',
        )
        self.assertEqual(
            orchestrator.sha256_file(orchestrator.PANEL_STUB),
            'b3379783c84eaa910f6a57f5318b8536f21220cfeaf0f73e9ff73ee0f20dd90d',
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
        self.assertEqual(frozen['missing_occurrence_datetime_n'], 0)
        self.assertIsNone(frozen['results'])
        self.assertIsNone(frozen['pnl'])
        self.assertIsNone(stamp['results'])
        self.assertIsNone(stamp['pnl'])
        self.assertEqual(binding['base_commit'], '438f4abf28a3c0156daf6c96ece5efda9557f1dc')
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
        self.assertEqual(panel['series_ticker'], 'KXETH15M')
        self.assertEqual(panel['scout_cite'], orchestrator.SCOUT_CITE)
        self.assertEqual(panel['scout_sha256'], orchestrator.SCOUT_SHA256)
        self.assertEqual(len(panel['events']), 1)
        self.assertEqual(len(panel['markets']), 1)
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
            self.assertEqual(len(loaded['markets']), 1)
            admitted.unlink()
            self.assertEqual(orchestrator.select_panel_path(stub, admitted), stub)
            stamped['panel_version'] = '2026-09-23.eth-kxeth15m-v1'
            rejected = root / 'panel_stub.json'
            rejected.write_text(json.dumps(stamped))
            with self.assertRaises(orchestrator.PanelVersionRefused):
                orchestrator.load_panel(rejected, root / 'missing_admitted.json')

    def test_panel_markets_are_the_scout_subset(self):
        panel = orchestrator.load_panel()
        index = orchestrator.scout_index()
        self.assertEqual(index['markets_n'], 1)
        self.assertEqual(index['events_n'], 1)
        self.assertEqual(index['missing_occurrence_datetime_n'], 0)
        self.assertEqual(len(panel['markets']), 1)
        for market in panel['markets']:
            self.assertEqual(market, index['by_ticker'][market['ticker']])
            self.assertEqual(market['result'], '')
            self.assertEqual(market['status'], 'active')
            self.assertNotIn('orderbook_fp', market)
            self.assertNotIn('fill_density', market)
            self.assertTrue(market['ticker'].startswith('KXETH15M-'))
            self.assertTrue(market['occurrence_datetime'].endswith('Z'))
        for event in panel['events']:
            self.assertIn(event['event_ticker'], index['events'])
            self.assertEqual(event['markets_n'], 1)
            market_times = {
                market['occurrence_datetime']
                for market in panel['markets']
                if market['event_ticker'] == event['event_ticker']
            }
            self.assertEqual(market_times, {event['occurrence_datetime']})
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
        self.assertIs(pins['panel_full_scout'], True)
        self.assertEqual(pins['missing_occurrence_datetime_n'], 0)
        self.assertIs(pins['signal_port'], False)
        self.assertIs(pins['claims_s1_green'], False)
        self.assertIs(pins['nhl_fq_reopen'], False)
        self.assertIs(pins['cpi_fq_reopen'], False)
        for key in orchestrator.OUTPUT_KEYS:
            self.assertIsNone(pins[key])
        hold = json.loads(orchestrator.EXAMINER_HOLD.read_text())
        accept = json.loads(orchestrator.CONDUCTOR_ACCEPT.read_text())
        self.assertEqual(hold['status'], 'NOT_SCORED')
        self.assertIs(hold['stub_ready'], False)
        self.assertEqual(accept['decision'], 'ACCEPT')
        self.assertIs(accept['implement'], True)
        self.assertEqual(accept['packet_id'], 'ETH-KXETH15M-FEEQUEUE-HARNESS')
        self.assertEqual(accept['digest_verify']['panel_stub_sha256'], orchestrator.PANEL_STUB_SHA256)
        self.assertEqual(
            accept['digest_verify']['scout_hunt_KXETH15M_sha256'],
            orchestrator.SCOUT_SHA256,
        )
        self.assertIs(accept['digest_verify']['panel_stub_match'], True)
        self.assertIs(accept['digest_verify']['hunt_match'], True)
        self.assertEqual(accept['hard_refuse'], list(orchestrator.ACCEPT_HARD_REFUSE))
        self.assertEqual(
            orchestrator.sha256_file(orchestrator.CONDUCTOR_ACCEPT),
            orchestrator.CONDUCTOR_ACCEPT_SHA256,
        )
        with self.assertRaises(orchestrator.PreAcceptEmptyRefused):
            orchestrator.load_scorecard(orchestrator.PRE_ACCEPT_EMPTY)
        with self.assertRaises(orchestrator.PreAcceptEmptyRefused):
            orchestrator.assert_null_scorecard(json.loads(orchestrator.PRE_ACCEPT_EMPTY.read_text()))


class SchemaTests(unittest.TestCase):
    def test_etha0_and_etha1_schema_on_the_panel_stub(self):
        before = {path: path.read_bytes() for path in _freeze_paths()}
        native = orchestrator.conduct(orchestrator.ETHA0)
        fresh = orchestrator.conduct(orchestrator.ETHA1)
        self.assertEqual(native['analysis_slice'], 'maker_vs_taker_native')
        self.assertEqual(fresh['analysis_slice'], 'content_fresh_vs_stale_bin')
        self.assertEqual(native['event_count'], 1)
        self.assertEqual(fresh['event_count'], 1)
        self.assertEqual(native['market_count'], 1)
        self.assertEqual(fresh['market_count'], 1)
        self.assertEqual(native['scout_markets_n'], 1)
        self.assertEqual(fresh['scout_events_n'], 1)
        self.assertEqual(native['missing_occurrence_datetime_n'], 0)
        self.assertEqual(fresh['missing_occurrence_datetime_n'], 0)
        self.assertEqual(native['fee_pin'], fresh['fee_pin'])
        self.assertEqual(native['rails_pin'], fresh['rails_pin'])
        self.assertEqual(native['lee_ready'], 'REFUSED')
        self.assertIs(native['signal_port'], False)
        self.assertIs(native['claims_s1_green'], False)
        self.assertIs(native['nhl_fq_reopen'], False)
        self.assertIs(native['cpi_fq_reopen'], False)
        self.assertIs(native['c5_reopen'], False)
        self.assertIs(native['atp_fq_reopen'], False)
        self.assertIs(native['live_crypto_trading'], False)
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
        self.assertEqual(native['arm'], 'ETHA0')
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
        self.assertEqual(fresh['arm'], 'ETHA1')
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
            orchestrator.conduct('ETHA2')
        for path, raw in before.items():
            self.assertEqual(path.read_bytes(), raw)

    def test_etha1_ignores_taker_side_when_binning(self):
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
            'nhl_fq_reopen',
            'cpi_fq_reopen',
            'c5_reopen',
            'atp_fq_reopen',
            'r3_p1',
            'r3_p2',
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
        with self.assertRaises(orchestrator.StrategyPortRefused):
            orchestrator.refuse_adversary('bacchus_port')
        with self.assertRaises(orchestrator.StrategyPortRefused):
            orchestrator.refuse_adversary('kxeth15m_strategy_port')
        with self.assertRaises(orchestrator.StrategyPortRefused):
            orchestrator.port_strategy('bacchus')
        with self.assertRaises(orchestrator.LiveOrdersForbidden):
            orchestrator.refuse_adversary('live_crypto')
        with self.assertRaises(orchestrator.InventedDepthRefused):
            orchestrator.refuse_adversary('invented_depth')
        with self.assertRaises(orchestrator.InventedMarketRefused):
            orchestrator.refuse_adversary('invented_markets')
        with self.assertRaises(orchestrator.InventedFillDensityRefused):
            orchestrator.refuse_adversary('invented_fill_density')
        with self.assertRaises(orchestrator.InventedSoTRefused):
            orchestrator.refuse_adversary('invented_occurrence_datetime')
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
                'ticker': 'KXETH15M-SYN-FEE',
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
                'ticker': 'KXETH15M-SYN-NOT-IN-HUNT',
                'event_ticker': 'KXETH15M-SYN',
                'status': 'active',
                'result': '',
            }, orchestrator.scout_index())

    def test_missing_occurrence_stays_missing_and_fill_density_is_refused(self):
        panel = orchestrator.load_panel()
        census = orchestrator.occurrence_census(panel['markets'])
        self.assertEqual(census['missing_occurrence_datetime_n'], 0)
        self.assertEqual(census['present_occurrence_datetime_n'], 1)
        scout = orchestrator.occurrence_census(list(orchestrator.scout_index()['by_ticker'].values()))
        self.assertEqual(scout['missing_occurrence_datetime_n'], 0)
        self.assertEqual(scout['present_occurrence_datetime_n'], 1)
        stripped = dict(panel['markets'][0])
        del stripped['occurrence_datetime']
        one = orchestrator.occurrence_census([stripped])
        self.assertEqual(one['missing_occurrence_datetime_n'], 1)
        self.assertNotIn('occurrence_datetime', stripped)
        nulled = dict(panel['markets'][0])
        nulled['occurrence_datetime'] = None
        self.assertEqual(
            orchestrator.occurrence_census([nulled])['missing_occurrence_datetime_n'],
            1,
        )
        self.assertIsNone(nulled['occurrence_datetime'])
        with self.assertRaises(orchestrator.InventedSoTRefused):
            orchestrator.assign_occurrence(stripped, '2026-09-23T00:00:00Z')
        self.assertNotIn('occurrence_datetime', stripped)
        with self.assertRaises(orchestrator.InventedFillDensityRefused):
            orchestrator.assign_fill_density(panel['markets'][0], '1.0')
        self.assertNotIn('fill_density', panel['markets'][0])
        bad = dict(panel['markets'][0])
        bad['occurrence_datetime'] = 'not-a-timestamp'
        with self.assertRaises(orchestrator.InventedSoTRefused):
            orchestrator.occurrence_census([bad])
        with self.assertRaises(orchestrator.InventedSoTRefused):
            orchestrator.classify_fresh_queue({
                'row_id': 'sot',
                'queue_ahead': '3300',
                'current': {'yes_bid': '0.40'},
                'transaction_time': '1',
                'occurrence_datetime': '2026-09-23T00:00:00Z',
            })
        with self.assertRaises(orchestrator.InventedFillDensityRefused):
            orchestrator.classify_native_taker({
                'ticker': 'KXETH15M-SYN-DENSITY',
                'taker_outcome_side': 'yes',
                'taker_book_side': 'bid',
                'fill_density': '1.5',
            })
        mutated = json.loads(orchestrator.PANEL_STUB.read_text())
        mutated['events'][0]['occurrence_datetime'] = '2026-01-01T00:00:00Z'
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'panel_stub.json'
            path.write_text(json.dumps(mutated))
            with self.assertRaises(orchestrator.InventedSoTRefused):
                orchestrator.load_panel(path, Path(tmp) / 'missing_admitted.json')
        cleared = json.loads(orchestrator.PANEL_STUB.read_text())
        event_name = cleared['events'][0]['event_ticker']
        cleared['events'][0]['occurrence_datetime'] = '2026-09-23T00:00:00Z'
        for market in cleared['markets']:
            if market['event_ticker'] == event_name:
                market['occurrence_datetime'] = None
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'panel_stub.json'
            path.write_text(json.dumps(cleared))
            with self.assertRaises(orchestrator.InventedMarketRefused):
                orchestrator.load_panel(path, Path(tmp) / 'missing_admitted.json')


if __name__ == '__main__':
    unittest.main()
