"""Unit pins for the C4 KXCPI fee and queue honesty harness.

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
        self.assertEqual(binding['experiment_id'], 'C4-KXCPI-FEEQUEUE-HARNESS')
        self.assertEqual(binding['feature_family'], 'CPI-FQ')
        self.assertEqual(frozen['feature_family'], 'CPI-FQ')
        self.assertEqual(stamp['feature_family'], 'CPI-FQ')
        self.assertEqual(binding['knob'], 'analysis_slice')
        self.assertEqual(frozen['knob'], 'analysis_slice')
        self.assertEqual(stamp['packet_id'], 'C4-KXCPI-FEEQUEUE-HARNESS')
        self.assertEqual(binding['panel_version'], '2026-09-23.c4-kxcpi-v0')
        self.assertEqual(panel['panel_version'], '2026-09-23.c4-kxcpi-v0')
        self.assertIsNone(panel['admitted_at'])
        self.assertIsNone(binding['admitted_at'])
        self.assertEqual(panel['stub_status'], 'NOT_ADMITTED')
        self.assertEqual(binding['events_n'], 4)
        self.assertEqual(binding['markets_n'], 44)
        self.assertEqual(binding['scout_markets_n'], 44)
        self.assertEqual(binding['scout_events_n'], 4)
        self.assertEqual(len(panel['events']), 4)
        self.assertEqual(len(panel['markets']), 44)
        self.assertIs(binding['panel_full_scout'], True)
        self.assertIs(binding['panel_markets_equal_scout'], True)
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
        self.assertIs(binding['nhl_fq_reopen'], False)
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
        self.assertEqual(frozen['arms'][1]['analysis_slice'], 'sparse_24h_vs_fresh_bin')
        self.assertEqual(binding['freeze_sha256'], orchestrator.FREEZE_SHA256)
        self.assertEqual(binding['scout_hunt_sha256'], orchestrator.SCOUT_SHA256)
        self.assertEqual(binding['panel_stub_sha256'], orchestrator.PANEL_STUB_SHA256)
        self.assertEqual(binding['source_pins_sha256'], orchestrator.SOURCE_PINS_SHA256)
        self.assertEqual(
            orchestrator.sha256_file(orchestrator.PACKET),
            '949b255859196f02d73303a1019e51276c583f8d1e3ffb4f0a64d330467c6f93',
        )
        self.assertEqual(
            orchestrator.sha256_file(orchestrator.SCOUT_CANONICAL),
            '6033907bb739bc00c41c796a3c1ed24553e0b7a44116ec3ea4bbaf39066bdcc8',
        )
        self.assertEqual(
            orchestrator.sha256_file(orchestrator.PANEL_STUB),
            'b20b0cbee50c127d2e9bb2548b574b7d643cc708f54019d53bd91775f9762c13',
        )
        self.assertEqual(
            orchestrator.sha256_file(orchestrator.CONDUCTOR_ACCEPT),
            '19ae0ae1fca66fa5c45bf8c13e013e3d710423c3e04194cc617d8bac1db546d7',
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
        self.assertEqual(binding['base_commit'], '677d5d4f0d5ed1235b4827bf89dd98d82bc34356')
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
        self.assertIsNone(snapshot['empty.sparse_vs_fresh_gap'])
        self.assertIsNone(snapshot['empty.missing_sot_n'])
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
        self.assertEqual(panel['series_ticker'], 'KXCPI')
        self.assertEqual(panel['scout_cite'], orchestrator.SCOUT_CITE)
        self.assertEqual(panel['scout_sha256'], orchestrator.SCOUT_SHA256)
        self.assertEqual(len(panel['events']), 4)
        self.assertEqual(len(panel['markets']), 44)
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
            self.assertEqual(len(loaded['markets']), 44)
            admitted.unlink()
            self.assertEqual(orchestrator.select_panel_path(stub, admitted), stub)
            stamped['panel_version'] = '2026-09-23.c4-kxcpi-v1'
            rejected = root / 'panel_stub.json'
            rejected.write_text(json.dumps(stamped))
            with self.assertRaises(orchestrator.PanelVersionRefused):
                orchestrator.load_panel(rejected, root / 'missing_admitted.json')

    def test_panel_markets_are_the_full_scout(self):
        panel = orchestrator.load_panel()
        index = orchestrator.scout_index()
        self.assertEqual(index['markets_n'], 44)
        self.assertEqual(index['events_n'], 4)
        self.assertEqual(len(panel['markets']), 44)
        self.assertEqual(
            {market['ticker'] for market in panel['markets']},
            set(index['by_ticker']),
        )
        for market in panel['markets']:
            self.assertEqual(market, index['by_ticker'][market['ticker']])
            self.assertEqual(market['result'], '')
            self.assertEqual(market['status'], 'active')
            self.assertNotIn('orderbook_fp', market)
            self.assertNotIn('fill_density', market)
            self.assertTrue(market['ticker'].startswith('KXCPI-'))
        for event in panel['events']:
            self.assertIn(event['event_ticker'], index['events'])
            actual = sum(
                1 for market in panel['markets']
                if market['event_ticker'] == event['event_ticker']
            )
            self.assertEqual(event['markets_n'], actual)
            expected = orchestrator.event_occurrence_from_markets(
                event['event_ticker'],
                panel['markets'],
            )
            self.assertEqual(event['occurrence_datetime'], expected)
        nov = next(event for event in panel['events'] if event['event_ticker'] == 'KXCPI-26NOV')
        self.assertIsNone(nov['occurrence_datetime'])
        nov_markets = [
            market for market in panel['markets']
            if market['event_ticker'] == 'KXCPI-26NOV'
        ]
        self.assertEqual(len(nov_markets), 7)
        for market in nov_markets:
            self.assertIsNone(market['occurrence_datetime'])
        missing = [
            market for market in panel['markets']
            if market['occurrence_datetime'] is None
        ]
        sparse = [
            market for market in panel['markets']
            if market['volume_24h_fp'] == '0.00'
        ]
        self.assertEqual(len(missing), 21)
        self.assertEqual(len(sparse), 21)
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
        self.assertIs(pins['panel_full_scout'], True)
        self.assertIs(pins['panel_markets_equal_scout'], True)
        self.assertEqual(pins['missing_occurrence_datetime_n'], 21)
        self.assertIsNone(pins['kxcpi_26nov_event_occurrence_datetime'])
        self.assertIs(pins['signal_port'], False)
        self.assertIs(pins['claims_s1_green'], False)
        self.assertIs(pins['nhl_fq_reopen'], False)
        for key in orchestrator.OUTPUT_KEYS:
            self.assertIsNone(pins[key])
        hold = json.loads(orchestrator.EXAMINER_HOLD.read_text())
        accept = json.loads(orchestrator.CONDUCTOR_ACCEPT.read_text())
        self.assertEqual(hold['status'], 'NOT_SCORED')
        self.assertIs(hold['stub_ready'], False)
        self.assertEqual(accept['status'], 'ACCEPT_IMPLEMENT_GO')
        self.assertEqual(accept['knob'], 'analysis_slice')
        self.assertIs(accept['panel_full_scout'], True)
        self.assertEqual(accept['missing_occurrence_datetime_n'], 21)
        self.assertIs(accept['integrity']['KXCPI-26NOV_event_occ_null'], True)
        with self.assertRaises(orchestrator.PreAcceptEmptyRefused):
            orchestrator.load_scorecard(orchestrator.PRE_ACCEPT_EMPTY)
        with self.assertRaises(orchestrator.PreAcceptEmptyRefused):
            orchestrator.assert_null_scorecard(json.loads(orchestrator.PRE_ACCEPT_EMPTY.read_text()))


class SchemaTests(unittest.TestCase):
    def test_c4a0_and_c4a1_schema_on_the_panel_stub(self):
        before = {path: path.read_bytes() for path in _freeze_paths()}
        native = orchestrator.conduct(orchestrator.C4A0)
        sparse = orchestrator.conduct(orchestrator.C4A1)
        self.assertEqual(native['analysis_slice'], 'maker_vs_taker_native')
        self.assertEqual(sparse['analysis_slice'], 'sparse_24h_vs_fresh_bin')
        self.assertEqual(native['event_count'], 4)
        self.assertEqual(sparse['event_count'], 4)
        self.assertEqual(native['market_count'], 44)
        self.assertEqual(sparse['market_count'], 44)
        self.assertEqual(native['scout_markets_n'], 44)
        self.assertEqual(sparse['scout_events_n'], 4)
        self.assertIs(sparse['panel_full_scout'], True)
        self.assertEqual(sparse['honesty_bin_count'], 4)
        counts = {
            (row['sparse_24h_refuse'], row['missing_occurrence_datetime_refuse']): row['market_n']
            for row in sparse['honesty_bins']
        }
        self.assertEqual(counts, {
            (True, False): 14,
            (False, True): 14,
            (False, False): 9,
            (True, True): 7,
        })
        for row in sparse['honesty_bins']:
            self.assertIsNone(row['content_fresh_flag'])
            self.assertIsNone(row['sparse_vs_fresh_gap'])
            self.assertIsNone(row['missing_sot_n'])
            self.assertIsNone(row['n_books'])
        self.assertEqual(native['fee_pin'], sparse['fee_pin'])
        self.assertEqual(native['rails_pin'], sparse['rails_pin'])
        self.assertEqual(native['lee_ready'], 'REFUSED')
        self.assertIs(native['signal_port'], False)
        self.assertIs(native['claims_s1_green'], False)
        self.assertIs(native['nhl_fq_reopen'], False)
        for report in (native, sparse):
            orchestrator.assert_null_scorecard(report)
            orchestrator.assert_null_scorecard(report['published'])
            self.assertIsNone(report['n_books'])
            self.assertIsNone(report['settled_join_n'])
            self.assertIsNone(report['missing_sot_n'])
            self.assertIsNone(report['sparse_vs_fresh_gap'])
            self.assertFalse(report['promoted'])
            self.assertEqual(report['source'], 'panel')
        for path, raw in before.items():
            self.assertEqual(path.read_bytes(), raw)

    def test_native_partition_and_sparse_bins_stay_out_of_the_freeze(self):
        before = {path: path.read_bytes() for path in _freeze_paths()}
        native = orchestrator.conduct_native()
        sparse = orchestrator.conduct_sparse()
        self.assertEqual(native['source'], 'synthetic_schema_standin')
        self.assertEqual(native['arm'], 'C4A0')
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
        self.assertEqual(sparse['arm'], 'C4A1')
        self.assertEqual(sparse['bin_count'], 5)
        flags = {
            (
                row['content_fresh_flag'],
                row['sparse_24h_refuse'],
                row['missing_occurrence_datetime_refuse'],
                row['queue_attribution_bin'],
            )
            for row in sparse['bins']
        }
        self.assertEqual(flags, {
            (True, False, False, 'q3300'),
            (False, False, False, 'q3300'),
            (False, False, False, 'q10000'),
            (True, True, False, 'q3300'),
            (True, False, True, 'q3300'),
        })
        for row in sparse['bins']:
            self.assertIsNone(row['sparse_vs_fresh_gap'])
            self.assertIsNone(row['missing_sot_n'])
            self.assertEqual(row['lee_ready'], 'REFUSED')
        for report in (native, sparse):
            orchestrator.assert_null_scorecard(report)
        with self.assertRaises(orchestrator.ScorecardPromotionRefused):
            orchestrator.write_scorecard(native['published'])
        with self.assertRaises(orchestrator.UnknownSlice):
            orchestrator.conduct('C4A2')
        for path, raw in before.items():
            self.assertEqual(path.read_bytes(), raw)

    def test_c4a1_ignores_taker_side_when_binning(self):
        base = {
            'queue_ahead': '3300',
            'previous': None,
            'current': {'yes_bid': '0.40'},
            'transaction_time': '1',
            'keepalive': False,
        }
        yes_row = dict(base, row_id='yes-side', taker_outcome_side='yes')
        no_row = dict(base, row_id='no-side', taker_outcome_side='no')
        bins = orchestrator.partition_sparse([yes_row, no_row])
        self.assertEqual(len(bins), 1)
        self.assertEqual(bins[0]['row_n'], 2)
        self.assertIs(bins[0]['content_fresh_flag'], True)
        self.assertIs(bins[0]['sparse_24h_refuse'], False)
        self.assertIs(bins[0]['missing_occurrence_datetime_refuse'], False)
        self.assertEqual(bins[0]['queue_attribution_bin'], 'q3300')
        self.assertIsNone(bins[0]['sparse_vs_fresh_gap'])


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
                'ticker': 'KXCPI-SYN-FEE',
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

    def test_sparse_tape_missing_sot_and_invented_market_are_refused(self):
        panel = orchestrator.load_panel()
        market = next(
            row for row in panel['markets']
            if row['occurrence_datetime'] is None
        )
        with self.assertRaises(orchestrator.InventedFillRefused):
            orchestrator.classify_native_taker({
                'ticker': market['ticker'],
                'taker_outcome_side': 'yes',
                'taker_book_side': 'bid',
                'taker_side': 'yes',
            })
        with self.assertRaises(orchestrator.InventedDepthRefused):
            orchestrator.quote_depth(market)
        with self.assertRaises(orchestrator.InventedSoTRefused):
            orchestrator.assign_occurrence(market, '2026-11-01T00:00:00Z')
        with self.assertRaises(orchestrator.InventedFillDensityRefused):
            orchestrator.assign_fill_density(market, '1.0')
        with self.assertRaises(orchestrator.InventedDepthRefused):
            orchestrator.classify_sparse_fresh({
                'row_id': 'sized',
                'queue_ahead': '3300',
                'current': {'yes_bid': '0.40'},
                'transaction_time': '1',
                'yes_bid_size_fp': '300.00',
            })
        with self.assertRaises(orchestrator.InventedFillDensityRefused):
            orchestrator.classify_sparse_fresh({
                'row_id': 'density',
                'queue_ahead': '3300',
                'current': {'yes_bid': '0.40'},
                'transaction_time': '1',
                'volume_24h_fp': '0.00',
                'fill_density': '1.5',
            })
        with self.assertRaises(orchestrator.InventedSoTRefused):
            orchestrator.classify_sparse_fresh({
                'row_id': 'bad-occ',
                'queue_ahead': '3300',
                'current': {'yes_bid': '0.40'},
                'transaction_time': '1',
                'occurrence_datetime': 'not-a-timestamp',
            })
        cloned = dict(market)
        cloned['occurrence_datetime'] = '2026-01-01T00:00:00Z'
        with self.assertRaises(orchestrator.InventedMarketRefused):
            orchestrator._assert_market_object(cloned, orchestrator.scout_index())
        with self.assertRaises(orchestrator.InventedMarketRefused):
            orchestrator._assert_market_object({
                'ticker': 'KXCPI-SYN-NOT-IN-HUNT',
                'event_ticker': 'KXCPI-SYN',
                'status': 'active',
                'result': '',
            }, orchestrator.scout_index())


if __name__ == '__main__':
    unittest.main()
