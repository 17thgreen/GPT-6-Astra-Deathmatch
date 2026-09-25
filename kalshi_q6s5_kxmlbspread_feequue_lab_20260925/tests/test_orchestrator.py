"""Unit pins for the Q6S5 KXMLBSPREAD fee and queue honesty harness.

Schema and pin locks only. In-memory helper calls are not a score and they
are not profit. Freeze outputs stay null. The subject is the panel stub
until panel_admitted.json appears. Transport is the stub. Live GET count
stays 0.
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
        orchestrator.PANEL_STUB,
        orchestrator.SOURCE_PINS,
        orchestrator.CONDUCTOR_ACCEPT,
        orchestrator.EXAMINER_HOLD,
        orchestrator.LAB_BUNDLE / 'FROZEN_EXPERIMENT.json',
        orchestrator.LAB_BUNDLE / 'results.json',
        orchestrator.GOVERNANCE_BUNDLE / 'FROZEN_EXPERIMENT.json',
        orchestrator.GOVERNANCE_BUNDLE / 'EMPTY_RESULTS.json',
    )


class PinTests(unittest.TestCase):
    def test_binding_pins_kxmlbspread_cache_fee_and_null_scorecard(self):
        self.assertFalse(orchestrator.PANEL_ADMITTED.exists())
        self.assertFalse((ROOT / 'admit.py').exists())
        binding = orchestrator.instrument_binding()
        panel = orchestrator.load_panel()
        frozen = json.loads(orchestrator.FROZEN_EXPERIMENT.read_text())
        self.assertEqual(binding['experiment_id'], 'Q6S5-KXMLBSPREAD-FEEQUEUE-HARNESS')
        self.assertEqual(binding['feature_family'], 'Q6S5-MLBSPREAD-FEEQUEUE')
        self.assertEqual(binding['series_ticker'], 'KXMLBSPREAD')
        self.assertEqual(panel['series_ticker'], 'KXMLBSPREAD')
        self.assertEqual(frozen['series_ticker'], 'KXMLBSPREAD')
        self.assertEqual(binding['knob'], 'analysis_slice')
        self.assertEqual(binding['panel_version'], '2026-09-25.q6s5-kxmlbspread-v0')
        self.assertIsNone(panel['admitted_at'])
        self.assertIsNone(binding['admitted_at'])
        self.assertIsNone(frozen['admitted_at'])
        self.assertEqual(binding['events_n'], 6)
        self.assertEqual(binding['markets_n'], 12)
        self.assertEqual(binding['source_markets_n'], 93)
        self.assertEqual(binding['source_events_n'], 15)
        self.assertIs(binding['scout_raw_present'], False)
        self.assertIs(binding['panel_full_scout'], False)
        self.assertEqual(binding['feebook_commit'], '22371178cb2663250b4762f328069571c48cb551')
        self.assertEqual(binding['rails_commit'], '6a28e0d6254327ea4e6451c781bec56215ac6cac')
        self.assertEqual(binding['fee_cache']['fee_type'], 'quadratic')
        self.assertEqual(binding['fee_cache']['multiplier'], '0.5')
        self.assertEqual(binding['fee_cache']['label'], 'CACHE-LABELED')
        self.assertIs(binding['fee_cache']['cache_labeled'], True)
        self.assertIs(binding['cache_labeled'], True)
        self.assertIs(binding['live_r1p1'], False)
        self.assertIs(binding['examiner_formula_used_as_series_pin'], False)
        self.assertIsNone(binding['fee_cache']['fee_dollars'])
        self.assertIsNone(binding['fee_cache']['results'])
        self.assertIsNone(binding['fee_cache']['pnl'])
        self.assertEqual(binding['fee_source'], 'cache')
        self.assertEqual(binding['queue_source'], 'rails')
        self.assertEqual(binding['fee_credit_rule_id'], rails.FEE_CREDIT_RULE_ID)
        self.assertEqual(binding['lee_ready'], 'REFUSED')
        self.assertEqual(binding['live_gets'], 0)
        self.assertIs(binding['kxmlbgame_ml_retune'], False)
        self.assertIs(binding['dual_cloud'], False)
        self.assertEqual(binding['examiner_status'], 'HOLD_PRE_PR')
        self.assertIs(binding['stub_ready'], False)
        self.assertIsNone(frozen['results'])
        self.assertIsNone(frozen['pnl'])
        self.assertIsNone(frozen['maker_vs_taker_roi_delta'])
        self.assertIsNone(frozen['fresh_vs_stale_gap'])
        self.assertIsNone(frozen['settled_join_n'])
        self.assertIsNone(frozen['n_books'])
        self.assertEqual(binding['freeze_sha256'], orchestrator.FREEZE_SHA256)
        self.assertEqual(binding['panel_stub_sha256'], orchestrator.PANEL_STUB_SHA256)
        self.assertEqual(binding['conductor_accept_sha256'], orchestrator.ACCEPT_SHA256)
        self.assertEqual(
            orchestrator.sha256_file(orchestrator.CONDUCTOR_ACCEPT),
            '5adc42f9c9533238a2187aafe7593bdf1b8cdec6d12b8d3e9b12cb5ab29000fc',
        )
        self.assertEqual(
            orchestrator.sha256_file(orchestrator.PACKET),
            '4f65dcdf536755b9f7dc2449c2dcd90b2df74cdf99a441b676f1a71c4d709c6e',
        )
        self.assertEqual(
            orchestrator.sha256_file(orchestrator.PANEL_STUB),
            'c7f1f1f4ca263838c4600ed46db8f525b68efc5399a567bd60929d18d76803cc',
        )
        pins = orchestrator.digest_status()
        self.assertIs(pins['digest_all_match_claimed'], False)
        self.assertIs(binding['digest_all_match_claimed'], False)
        for key in ('scout_markets', 'scout_summary', 'p16_pdf', 'archivist_ping'):
            self.assertIn(key, pins['missing'])
        by_key = {row['key']: row for row in pins['pins']}
        for key in ('conductor_accept', 'freeze', 'panel_stub', 'source_pins', 'empty_results'):
            self.assertIs(by_key[key]['match'], True)
        self.assertEqual(binding['base_commit'], orchestrator.BASE_COMMIT)
        self.assertEqual(Path(feebook.__file__).resolve().parent.name, 'kalshi_feebook_lab_20260922')
        self.assertEqual(Path(rails.__file__).resolve().parent.name, 'kalshi_rails_lab_20260922')
        self.assertEqual(
            Path(orchestrator.hygiene.__file__).resolve().parent.name,
            'kalshi_r2p1_hygiene_000_lab_20260922',
        )
        self.assertIsNone(orchestrator.settled_join(panel))
        for market in panel['markets']:
            self.assertTrue(market['ticker'].startswith('KXMLBSPREAD-'))
            self.assertNotIn('KXMLBGAME-', market['ticker'])

    def test_source_pin_copies_match_and_scorecard_v12_stays_null(self):
        canonical = orchestrator.GOVERNANCE_BUNDLE / 'SOURCE_PINS.json'
        for path in orchestrator.source_pin_paths():
            self.assertEqual(path.read_bytes(), canonical.read_bytes())
            self.assertEqual(orchestrator.sha256_file(path), orchestrator.SOURCE_PINS_SHA256)
        frozen_bytes = orchestrator.FROZEN_EXPERIMENT.read_bytes()
        for path in (
            orchestrator.FROZEN_EXPERIMENT,
            orchestrator.LAB_BUNDLE / 'FROZEN_EXPERIMENT.json',
            orchestrator.GOVERNANCE_BUNDLE / 'FROZEN_EXPERIMENT.json',
        ):
            self.assertEqual(path.read_bytes(), frozen_bytes)
        empty_bytes = orchestrator.EMPTY_RESULTS.read_bytes()
        for path in (
            orchestrator.EMPTY_RESULTS,
            orchestrator.LAB_BUNDLE / 'results.json',
            orchestrator.LAB_BUNDLE / 'results' / 'EMPTY_RESULTS.json',
            orchestrator.GOVERNANCE_BUNDLE / 'EMPTY_RESULTS.json',
        ):
            self.assertEqual(path.read_bytes(), empty_bytes)
            payload = json.loads(path.read_text())
            orchestrator.assert_null_scorecard(payload)
            orchestrator.assert_v12_null(payload['examiner_scorecard_v1_2'])
        hold = json.loads(orchestrator.EXAMINER_HOLD.read_text())
        self.assertEqual(hold['status'], 'HOLD_PRE_PR')
        self.assertIs(hold['stub_ready'], False)
        orchestrator.assert_v12_null(hold['examiner_scorecard_v1_2'])
        self.assertIsNone(hold['examiner_scorecard_v1_2']['scorecard']['verdict'])
        self.assertIsNone(hold['examiner_scorecard_v1_2']['preregistration_checklist']['gate_status'])
        checklist = json.loads(orchestrator.P16_CHECKLIST.read_text())
        frozen = json.loads(frozen_bytes)
        self.assertEqual(checklist, frozen['p16_preregistration_checklist'])
        self.assertEqual(
            (orchestrator.LAB_BUNDLE / 'p16_preregistration_checklist.json').read_bytes(),
            orchestrator.P16_CHECKLIST.read_bytes(),
        )
        self.assertEqual(checklist['counts'], {'satisfied': 8, 'n/a': 4, 'missing': 0})
        snapshot = orchestrator.frozen_output_snapshot()
        self.assertIsNone(snapshot['frozen.results'])
        self.assertIsNone(snapshot['empty.pnl'])
        self.assertIsNone(snapshot['empty.maker_vs_taker_roi_delta'])
        self.assertIsNone(snapshot['governance_empty.n_books'])

    def test_digest_all_match_is_true_only_when_every_pin_rehashes(self):
        present = tuple(
            (row['key'], orchestrator.sha256_file(PARENT / row['path']), row['path'])
            for row in orchestrator.digest_status()['pins']
            if row['present']
        )
        self.assertGreater(len(present), 0)
        matched = orchestrator.digest_status(present)
        self.assertIs(matched['digest_all_match_claimed'], True)
        self.assertEqual(matched['missing'], [])
        self.assertEqual(matched['mismatch'], [])
        flipped = (present[0][0], '0' * 64, present[0][2])
        broken = orchestrator.digest_status((flipped,) + present[1:])
        self.assertIs(broken['digest_all_match_claimed'], False)
        self.assertIn(present[0][0], broken['mismatch'])
        full = orchestrator.digest_status()
        self.assertIs(full['digest_all_match_claimed'], False)

    def test_panel_stub_is_the_pinned_subset_and_admitted_is_preferred(self):
        self.assertEqual(orchestrator.select_panel_path(), orchestrator.PANEL_STUB)
        panel = orchestrator.load_panel()
        self.assertEqual(len(panel['events']), 6)
        self.assertEqual(len(panel['markets']), 12)
        self.assertIsNone(panel['results'])
        self.assertIsNone(panel['pnl'])
        index = orchestrator.panel_market_index()
        for market in panel['markets']:
            self.assertEqual(market, index['by_ticker'][market['ticker']])
            self.assertEqual(market['status'], 'active')
            self.assertEqual(market['result'], '')
        stamped = json.loads(orchestrator.PANEL_STUB.read_text())
        stamped['admitted_at'] = '2026-09-25T12:00:00Z'
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            stub = root / 'panel_stub.json'
            admitted = root / 'panel_admitted.json'
            stub.write_text(orchestrator.PANEL_STUB.read_text())
            admitted.write_text(json.dumps(stamped))
            self.assertEqual(orchestrator.select_panel_path(stub, admitted), admitted)
            loaded = orchestrator.load_panel(stub, admitted)
            self.assertEqual(loaded['admitted_at'], '2026-09-25T12:00:00Z')
            self.assertEqual(loaded['panel_version'], orchestrator.PANEL_VERSION)
            admitted.unlink()
            self.assertEqual(orchestrator.select_panel_path(stub, admitted), stub)
            stamped['panel_version'] = '2026-09-25.q6s5-kxmlbspread-v1'
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
    def test_arms_on_the_panel_keep_metrics_null(self):
        before = {path: path.read_bytes() for path in _freeze_paths()}
        native = orchestrator.conduct(orchestrator.Q6S5A0)
        fresh = orchestrator.conduct(orchestrator.Q6S5A1)
        self.assertEqual(native['analysis_slice'], 'maker_vs_taker_native')
        self.assertEqual(fresh['analysis_slice'], 'content_fresh_vs_stale_bin')
        self.assertEqual(native['series_ticker'], 'KXMLBSPREAD')
        self.assertEqual(fresh['series_ticker'], 'KXMLBSPREAD')
        self.assertEqual(native['event_count'], 6)
        self.assertEqual(native['market_count'], 12)
        self.assertIs(native['scout_raw_present'], False)
        self.assertIs(native['cache_labeled'], True)
        self.assertIs(fresh['fee_cache']['cache_labeled'], True)
        self.assertIs(fresh['live_r1p1'], False)
        self.assertEqual(native['live_gets'], 0)
        for report in (native, fresh):
            orchestrator.assert_null_scorecard(report)
            orchestrator.assert_null_scorecard(report['published'])
            self.assertFalse(report['promoted'])
            self.assertEqual(report['source'], 'panel')
            self.assertEqual(report['examiner_status'], 'HOLD_PRE_PR')
        for path, raw in before.items():
            self.assertEqual(path.read_bytes(), raw)

    def test_native_partition_and_fresh_bins_stay_out_of_the_freeze(self):
        before = {path: path.read_bytes() for path in _freeze_paths()}
        native = orchestrator.conduct_native()
        fresh = orchestrator.conduct_fresh()
        self.assertEqual(native['arm'], 'Q6S5A0')
        self.assertEqual(native['partition_count'], 2)
        by_side = {row['taker_outcome_side']: row for row in native['partitions']}
        self.assertEqual(by_side['yes']['taker_book_side'], 'bid')
        self.assertEqual(by_side['yes']['maker_outcome_side'], 'no')
        self.assertEqual(by_side['yes']['series'], 'KXMLBSPREAD')
        self.assertEqual(by_side['no']['maker_outcome_side'], 'yes')
        self.assertIsNone(by_side['yes']['maker_vs_taker_roi_delta'])
        self.assertIsNone(by_side['yes']['pnl'])
        self.assertEqual(fresh['arm'], 'Q6S5A1')
        self.assertEqual(fresh['bin_count'], 3)
        flags = {(row['content_fresh_flag'], row['queue_attribution_bin']) for row in fresh['bins']}
        self.assertEqual(flags, {(True, 'q3300'), (False, 'q3300'), (False, 'q10000')})
        for row in fresh['bins']:
            self.assertIsNone(row['fresh_vs_stale_gap'])
            self.assertEqual(row['series'], 'KXMLBSPREAD')
        with self.assertRaises(orchestrator.ScorecardPromotionRefused):
            orchestrator.write_scorecard(native['published'])
        with self.assertRaises(orchestrator.UnknownSlice):
            orchestrator.conduct('Q6S5A2')
        for path, raw in before.items():
            self.assertEqual(path.read_bytes(), raw)

    def test_fresh_bin_ignores_taker_side(self):
        base = {
            'queue_ahead': '3300',
            'previous': None,
            'current': {'yes_bid': '0.40'},
            'transaction_time': '1',
            'keepalive': False,
        }
        bins = orchestrator.partition_fresh([
            dict(base, row_id='yes-side', taker_outcome_side='yes'),
            dict(base, row_id='no-side', taker_outcome_side='no'),
        ])
        self.assertEqual(len(bins), 1)
        self.assertEqual(bins[0]['row_n'], 2)
        self.assertIs(bins[0]['content_fresh_flag'], True)
        self.assertIsNone(bins[0]['fresh_vs_stale_gap'])


class RefuseTests(unittest.TestCase):
    def test_lee_ready_is_refused_on_every_input(self):
        for sample in (None, {}, {'taker_outcome_side': 'yes'}, {'classifier': 'lee-ready'}, 'quote'):
            with self.assertRaises(orchestrator.LeeReadyRefused):
                orchestrator.infer_lee_ready(sample)
        with self.assertRaises(orchestrator.LeeReadyRefused):
            orchestrator.classify_native_taker({
                'ticker': 'KXMLBSPREAD-SYN-LEE',
                'taker_outcome_side': 'yes',
                'taker_book_side': 'bid',
                'lee_ready': True,
            })
        with self.assertRaises(orchestrator.TakerFieldRefused):
            orchestrator.classify_native_taker({
                'ticker': 'KXMLBSPREAD-SYN-DISAGREE',
                'taker_outcome_side': 'yes',
                'taker_book_side': 'ask',
                'lee_ready': 'REFUSED',
            })
        with self.assertRaises(orchestrator.InventedFillRefused):
            orchestrator.classify_native_taker({
                'ticker': 'KXMLBSPREAD-SYN-RESULT',
                'taker_outcome_side': 'yes',
                'taker_book_side': 'bid',
                'result': 'yes',
            })

    def test_stub_transport_does_not_live_get_and_refuses_orders(self):
        transport = orchestrator.StubTransport(
            bodies={'/events?series_ticker=KXMLBSPREAD': {'events': [], 'series': 'KXMLBSPREAD'}},
            markets_hot=True,
        )
        got = transport.request('GET', '/markets?series_ticker=KXMLBSPREAD')
        self.assertEqual(got['path'], '/events?series_ticker=KXMLBSPREAD')
        self.assertEqual(got['preferred_because'], 'markets_hot')
        self.assertIs(got['live'], False)
        self.assertEqual(got['live_gets'], 0)
        self.assertEqual(transport.live_gets, 0)
        self.assertEqual(got['body']['series'], 'KXMLBSPREAD')
        direct = orchestrator.public_get('/events')
        self.assertEqual(direct['live_gets'], 0)
        self.assertIs(direct['live'], False)
        with self.assertRaises(orchestrator.LiveOrdersForbidden):
            transport.request('POST', '/events')
        with self.assertRaises(orchestrator.LiveOrdersForbidden):
            transport.request('GET', '/portfolio/orders')
        with self.assertRaises(orchestrator.LiveOrdersForbidden):
            transport.request('GET', PUBLIC_ORDERS)
        with self.assertRaises(orchestrator.KXMLBGameRetuneRefused):
            transport.request('GET', '/markets?series_ticker=KXMLBGAME')
        with self.assertRaises(orchestrator.OrchestratorError):
            transport.request('GET', 'https://example.invalid/trade-api/v2/events')
        source = (ROOT / 'orchestrator.py').read_text()
        for banned in (
            '0.0175',
            '0.07',
            'class KalshiExecutionAdapter',
            'urlopen',
            'import queue_fragility',
            'os.environ',
            'api_key',
            'private_key',
            'urllib',
            'socket',
        ):
            self.assertNotIn(banned, source)
        with self.assertRaises(orchestrator.CacheNotLiveR1P1):
            orchestrator.claim_live_r1p1()
        with self.assertRaises(orchestrator.CacheNotLiveR1P1):
            orchestrator.promote_series_fee(
                feebook.order_fee('taker', '1', '0.50', round_up=True, series='KXMLBSPREAD')
            )
        with self.assertRaises(orchestrator.KXMLBGameRetuneRefused):
            orchestrator.fee_output('KXMLBGAME')
        label = orchestrator.fee_output()
        self.assertIs(label['cache_labeled'], True)
        self.assertEqual(label['series'], 'KXMLBSPREAD')

    def test_reopens_signal_port_and_fee_literals_are_refused(self):
        for label in (
            'live_orders',
            'logan_keys',
            'invented_pnl',
            'invented_fills',
            'q6_retune',
            'cap_sr_reopen',
            'dual_cloud',
            'admit_py',
            'card06_reopen',
        ):
            with self.assertRaises(orchestrator.AdversaryRefused):
                orchestrator.refuse_adversary(label)
        with self.assertRaises(orchestrator.KXMLBGameRetuneRefused):
            orchestrator.refuse_adversary('kxmlbgame_ml_retune')
        with self.assertRaises(orchestrator.SignalPortRefused):
            orchestrator.port_nfl_000_signal({'edge': 1})
        with self.assertRaises(orchestrator.S1GreenClaimRefused):
            orchestrator.claim_s1_green()
        for name in ('S1', 'S2', 'R2-P4', 'KXMLBGAME', 'Q6-000', 'Cap-SR'):
            with self.assertRaises(orchestrator.UngateRefused):
                orchestrator.ungate(name)
        with self.assertRaises(orchestrator.LiveOrdersForbidden):
            orchestrator.execution_adapter()
        with self.assertRaises(orchestrator.ShadowFeeLiteralRefused):
            orchestrator.classify_native_taker({
                'ticker': 'KXMLBSPREAD-SYN-FEE',
                'taker_outcome_side': 'yes',
                'taker_book_side': 'bid',
                'fee_cost': '0.01',
            })
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
        with self.assertRaises(orchestrator.KXMLBGameRetuneRefused):
            orchestrator.classify_native_taker({
                'ticker': 'KXMLBGAME-26SEP25-SYN',
                'taker_outcome_side': 'yes',
                'taker_book_side': 'bid',
            })
        with self.assertRaises(orchestrator.InventedMarketRefused):
            orchestrator._assert_market_object({
                'ticker': 'KXMLBSPREAD-SYN-NOT-IN-PANEL',
                'event_ticker': 'KXMLBSPREAD-SYN',
                'status': 'active',
                'result': '',
            }, orchestrator.panel_market_index())

    def test_occurrence_is_not_invented_and_fill_density_is_refused(self):
        panel = orchestrator.load_panel()
        census = orchestrator.occurrence_census(panel['markets'])
        self.assertEqual(census['missing_occurrence_datetime_n'], 0)
        self.assertEqual(census['present_occurrence_datetime_n'], 12)
        stripped = dict(panel['markets'][0])
        del stripped['occurrence_datetime']
        self.assertEqual(
            orchestrator.occurrence_census([stripped])['missing_occurrence_datetime_n'],
            1,
        )
        with self.assertRaises(orchestrator.InventedSoTRefused):
            orchestrator.assign_occurrence(stripped, '2026-09-25T00:00:00Z')
        with self.assertRaises(orchestrator.InventedFillDensityRefused):
            orchestrator.assign_fill_density(panel['markets'][0], '1.0')
        mutated = json.loads(orchestrator.PANEL_STUB.read_text())
        mutated['events'][0]['occurrence_datetime'] = '2026-01-01T00:00:00Z'
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'panel_stub.json'
            path.write_text(json.dumps(mutated))
            with self.assertRaises(orchestrator.InventedSoTRefused):
                orchestrator.load_panel(path, Path(tmp) / 'missing_admitted.json')


PUBLIC_ORDERS = orchestrator.PUBLIC_HOST + '/portfolio/orders'


if __name__ == '__main__':
    unittest.main()
