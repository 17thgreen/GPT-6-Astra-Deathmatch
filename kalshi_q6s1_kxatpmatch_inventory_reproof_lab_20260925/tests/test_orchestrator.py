"""Unit pins for the Q6S1 KXATPMATCH inventory re-proof harness.

Schema and pin locks only. In-memory helper calls are not a score and they
are not profit. Freeze outputs stay null. The subject is the panel stub.
Transport is the stub. Live GET count stays 0. admit.py is not run.
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


class SeriesGuardTests(unittest.TestCase):
    def test_series_guard_is_kxatpmatch_only(self):
        binding = orchestrator.instrument_binding()
        panel = orchestrator.load_panel()
        frozen = json.loads(orchestrator.FROZEN_EXPERIMENT.read_text())
        self.assertEqual(binding['experiment_id'], 'Q6S1-KXATPMATCH-INVENTORY-REPROOF')
        self.assertEqual(binding['feature_family'], 'Q6S1-ATP-INVENTORY')
        self.assertEqual(binding['series_ticker'], 'KXATPMATCH')
        self.assertEqual(panel['series_ticker'], 'KXATPMATCH')
        self.assertEqual(frozen['series_ticker'], 'KXATPMATCH')
        self.assertEqual(binding['knob'], 'inventory_slice')
        for market in panel['markets']:
            self.assertTrue(market['ticker'].startswith('KXATPMATCH-'))
            orchestrator.assert_series(market['ticker'])
        for foreign in (
            'KXMLBSPREAD',
            'KXMLBGAME',
            'KXNFLGAME',
            'KXNHLGAME',
            'KXCPI',
            '/markets?series_ticker=KXMLBSPREAD',
            'KXMLBSPREAD-26SEP25-SYN',
        ):
            with self.assertRaises(orchestrator.SeriesRefused):
                orchestrator.assert_series(foreign)
            with self.assertRaises(orchestrator.SeriesRefused):
                orchestrator.fee_output(foreign.split('?', 1)[0].split('-', 1)[0]
                                        if foreign.startswith('K') else 'KXMLBSPREAD')
        self.assertEqual(orchestrator.fee_output()['series'], 'KXATPMATCH')
        self.assertIs(binding['atp_fq_closed'], True)
        self.assertIs(binding['atp_rj_closed'], True)
        self.assertIs(binding['analysis_slice_reopened'], False)
        self.assertIs(binding['join_gate_reopened'], False)


class TransportTests(unittest.TestCase):
    def test_live_gets_stay_zero(self):
        transport = orchestrator.StubTransport()
        got = transport.request('GET', '/events?series_ticker=KXATPMATCH')
        self.assertEqual(got['live_gets'], 0)
        self.assertEqual(transport.live_gets, 0)
        self.assertIs(got['live'], False)
        self.assertEqual(got['host'], orchestrator.PUBLIC_HOST)
        direct = orchestrator.public_get('/events')
        self.assertEqual(direct['live_gets'], 0)
        self.assertIs(direct['live'], False)
        binding = orchestrator.instrument_binding()
        self.assertEqual(binding['live_gets'], 0)
        report = orchestrator.conduct(orchestrator.Q6S1A0)
        self.assertEqual(report['live_gets'], 0)
        transport.live_gets = 1
        with self.assertRaises(orchestrator.LiveOrdersForbidden):
            transport.request('GET', '/events?series_ticker=KXATPMATCH')

    def test_orders_and_portfolio_are_refused(self):
        transport = orchestrator.StubTransport()
        for path in (
            '/orders',
            '/portfolio',
            '/portfolio/orders',
            orchestrator.PUBLIC_HOST + '/orders',
            orchestrator.PUBLIC_HOST + '/portfolio/balance',
        ):
            with self.assertRaises(orchestrator.LiveOrdersForbidden):
                transport.request('GET', path)
        with self.assertRaises(orchestrator.LiveOrdersForbidden):
            transport.request('POST', '/events')
        with self.assertRaises(orchestrator.LiveOrdersForbidden):
            transport.request('DELETE', '/events')
        with self.assertRaises(orchestrator.LiveOrdersForbidden):
            orchestrator.assert_public_get('POST')
        with self.assertRaises(orchestrator.LiveOrdersForbidden):
            orchestrator.execution_adapter()
        with self.assertRaises(orchestrator.OrchestratorError):
            transport.request('GET', 'https://example.invalid/trade-api/v2/events')

    def test_hot_markets_prefer_events(self):
        transport = orchestrator.StubTransport(
            bodies={'/events?series_ticker=KXATPMATCH': {'events': [], 'series': 'KXATPMATCH'}},
            markets_hot=True,
        )
        got = transport.request('GET', '/markets?series_ticker=KXATPMATCH')
        self.assertEqual(got['path'], '/events?series_ticker=KXATPMATCH')
        self.assertEqual(got['requested'], '/markets?series_ticker=KXATPMATCH')
        self.assertEqual(got['preferred_because'], 'markets_hot')
        self.assertEqual(got['live_gets'], 0)
        self.assertIs(got['live'], False)
        self.assertEqual(got['body']['series'], 'KXATPMATCH')
        cold = orchestrator.StubTransport(markets_hot=False)
        stayed = cold.request('GET', '/markets?series_ticker=KXATPMATCH')
        self.assertEqual(stayed['path'], '/markets?series_ticker=KXATPMATCH')
        self.assertIsNone(stayed['preferred_because'])
        source = (ROOT / 'orchestrator.py').read_text()
        for banned in ('urlopen', 'urllib', 'socket', 'subprocess', 'import admit', 'requests'):
            self.assertNotIn(banned, source)


class FeeTests(unittest.TestCase):
    def test_fee_is_cache_labeled_multiplier_one(self):
        label = orchestrator.fee_output()
        self.assertEqual(label['fee_type'], 'quadratic_with_maker_fees')
        self.assertEqual(label['multiplier'], 1)
        self.assertEqual(label['label'], 'CACHE-LABELED')
        self.assertIs(label['cache_labeled'], True)
        self.assertIs(label['live_r1p1'], False)
        self.assertIs(label['not_quadratic_x0_5'], True)
        self.assertEqual(label['fee_source'], 'cache')
        self.assertIsNone(label['fee_dollars'])
        self.assertIsNone(label['results'])
        self.assertIsNone(label['pnl'])
        self.assertEqual(label['feebook_resolution_not_series_pin'], 'default_unknown_series')
        same = orchestrator.fee_output_with_multiplier('KXATPMATCH', '1')
        self.assertEqual(same['multiplier'], 1)
        self.assertIs(same['cache_labeled'], True)
        self.assertIs(same['live_r1p1'], False)
        with self.assertRaises(orchestrator.FeeHalfRefused):
            orchestrator.fee_output_with_multiplier('KXATPMATCH', 0.5)
        with self.assertRaises(orchestrator.FeeHalfRefused):
            orchestrator.fee_output_with_multiplier('KXATPMATCH', '0.5')
        with self.assertRaises(orchestrator.CacheNotLiveR1P1):
            orchestrator.claim_live_r1p1({'fee_type': 'quadratic_with_maker_fees'})
        with self.assertRaises(orchestrator.CacheNotLiveR1P1):
            orchestrator.promote_series_fee({'fee_dollars': '1.00'})
        table = feebook.load_series_table()
        self.assertEqual(table.get('overrides'), {})
        terms = feebook.resolve_terms(table, 'KXATPMATCH', 'taker')
        self.assertEqual(terms['resolution'], 'default_unknown_series')
        screen = orchestrator.screen_pin()
        self.assertEqual(screen['fee_type'], 'quadratic_with_maker_fees')
        self.assertEqual(screen['fee_multiplier'], 1)
        self.assertIs(screen['cache_labeled'], True)
        self.assertIs(screen['live_r1p1'], False)
        self.assertIs(screen['copied_into_scorecard'], False)
        self.assertEqual(Path(feebook.__file__).resolve().parent.name, 'kalshi_feebook_lab_20260922')
        self.assertEqual(Path(rails.__file__).resolve().parent.name, 'kalshi_rails_lab_20260922')
        self.assertEqual(orchestrator.instrument_binding()['fee_credit_rule_id'], rails.FEE_CREDIT_RULE_ID)


class ArmTests(unittest.TestCase):
    def test_arms_are_q6s1a0_and_q6s1a1_only(self):
        before = {path: path.read_bytes() for path in _freeze_paths()}
        flat = orchestrator.conduct(orchestrator.Q6S1A0)
        binned = orchestrator.conduct(orchestrator.Q6S1A1)
        self.assertEqual(flat['arm'], 'Q6S1A0')
        self.assertEqual(flat['inventory_slice'], 'flat_control')
        self.assertEqual(binned['arm'], 'Q6S1A1')
        self.assertEqual(binned['inventory_slice'], 'inventory_bin_exposure')
        self.assertEqual(flat['knob'], 'inventory_slice')
        self.assertEqual(binned['knob'], 'inventory_slice')
        self.assertEqual(orchestrator.set_knob('inventory_slice'), {
            'Q6S1A0': 'flat_control',
            'Q6S1A1': 'inventory_bin_exposure',
        })
        for report in (flat, binned):
            self.assertEqual(report['series_ticker'], 'KXATPMATCH')
            self.assertEqual(report['event_count'], 6)
            self.assertEqual(report['market_count'], 12)
            self.assertIsNone(report['position_bucket'])
            self.assertIsNone(report['inventory_bins'])
            self.assertIs(report['strategy'], None)
            self.assertEqual(report['examiner_status'], 'HOLD_PRE_PR')
            self.assertIs(report['stub_ready'], False)
            self.assertIs(report['admit_py_run'], False)
            orchestrator.assert_null_scorecard(report)
            orchestrator.assert_null_scorecard(report['published'])
        with self.assertRaises(orchestrator.UnknownSlice):
            orchestrator.conduct('Q6S1A2')
        with self.assertRaises(orchestrator.ClosedParentRefused):
            orchestrator.conduct('ATPA0')
        with self.assertRaises(orchestrator.ClosedParentRefused):
            orchestrator.conduct('J0')
        with self.assertRaises(orchestrator.ClosedParentRefused):
            orchestrator.conduct('Q6S5A0')
        with self.assertRaises(orchestrator.ClosedParentRefused):
            orchestrator.reopen_analysis_slice()
        with self.assertRaises(orchestrator.ClosedParentRefused):
            orchestrator.reopen_join_gate()
        with self.assertRaises(orchestrator.ClosedParentRefused):
            orchestrator.set_knob('analysis_slice')
        with self.assertRaises(orchestrator.ClosedParentRefused):
            orchestrator.set_knob('join_gate')
        for path, raw in before.items():
            self.assertEqual(path.read_bytes(), raw)

    def test_closed_parents_stay_import_only(self):
        parents = orchestrator.parent_import_status()
        self.assertEqual(parents['atp_fq_freeze_sha256'], orchestrator.ATP_FQ_FREEZE_SHA256)
        self.assertEqual(parents['atp_rj_freeze_sha256'], orchestrator.ATP_RJ_FREEZE_SHA256)
        self.assertIs(parents['import_only'], True)
        self.assertIs(parents['analysis_slice_reopened'], False)
        self.assertIs(parents['join_gate_reopened'], False)
        for label in ('atp_fq_reopen', 'atp_rj_reopen', 'q6s5_reopen', 'cap_sr_reopen', 'pr57_infra'):
            with self.assertRaises((
                orchestrator.ClosedParentRefused,
                orchestrator.AdversaryRefused,
            )):
                orchestrator.refuse_adversary(label)


class NullScorecardTests(unittest.TestCase):
    def test_results_pnl_and_inventory_deltas_stay_null(self):
        frozen = json.loads(orchestrator.FROZEN_EXPERIMENT.read_text())
        empty = json.loads(orchestrator.EMPTY_RESULTS.read_text())
        orchestrator.assert_null_scorecard(frozen)
        orchestrator.assert_null_scorecard(empty)
        orchestrator.assert_v12_null(empty['examiner_scorecard_v1_2'])
        snapshot = orchestrator.frozen_output_snapshot()
        self.assertIsNone(snapshot['frozen.results'])
        self.assertIsNone(snapshot['empty.pnl'])
        self.assertIsNone(snapshot['empty.inventory_delta_flat_vs_binned'])
        self.assertIsNone(snapshot['governance_empty.settled_join_n'])
        self.assertIsNone(snapshot['governance_empty.n_books'])
        self.assertIsNone(snapshot['governance_empty.unresolved_inventory'])
        report = orchestrator.conduct(orchestrator.Q6S1A1)
        for key in orchestrator.OUTPUT_KEYS:
            self.assertIsNone(report[key])
            self.assertIsNone(report['published'][key])
        self.assertIsNone(orchestrator.settled_join(orchestrator.load_panel()))
        with self.assertRaises(orchestrator.InventedFillRefused):
            orchestrator.invent_fill()
        with self.assertRaises(orchestrator.InventedPnlRefused):
            orchestrator.invent_pnl(1)
        with self.assertRaises(orchestrator.InventedInventoryRefused):
            orchestrator.invent_inventory_delta(1)
        with self.assertRaises(orchestrator.InventedDepthRefused):
            orchestrator.quote_depth(orchestrator.load_panel()['markets'][0])
        with self.assertRaises(orchestrator.InventedSettlementRefused):
            orchestrator.invent_settlement_ts(None, '2026-09-25T00:00:00Z')
        with self.assertRaises(orchestrator.ScorecardPromotionRefused):
            orchestrator.write_scorecard(report['published'])
        summary = json.loads(orchestrator.SPORTS_SUMMARY.read_text())
        self.assertEqual(summary['n_markets'], 28)
        self.assertEqual(summary['n_events'], 14)
        self.assertNotEqual(report['unresolved_inventory'], summary['sum_open_interest_fp'])
        self.assertIsNone(report['pnl'])
        with self.assertRaises(orchestrator.InventedMarketRefused):
            orchestrator.copy_screen_counts_into_scorecard(summary)
        self.assertIs(report['screen_counts_copied_into_scorecard'], False)
        self.assertEqual(report['market_count'], 12)
        self.assertNotEqual(report['market_count'], 28)

    def test_scorecard_v12_and_p16_measured_fields_stay_null(self):
        empty = json.loads(orchestrator.EMPTY_RESULTS.read_text())
        block = empty['examiner_scorecard_v1_2']
        self.assertEqual(
            block['template']['json_sha256'],
            '56bcf6269a42031d9d90496e9a65c2292321aed2165033f6fb44ff8cc4d6b1cc',
        )
        self.assertEqual(
            orchestrator.sha256_file(orchestrator.TEMPLATE_V12),
            orchestrator.TEMPLATE_V12_SHA256,
        )
        self.assertIsNone(block['scorecard']['verdict'])
        self.assertEqual(block['scorecard']['status'], 'HOLD_PRE_PR')
        self.assertIsNone(block['preregistration_checklist']['gate_status'])
        self.assertIsNone(block['study_label']['value'])
        checklist = json.loads(orchestrator.P16_CHECKLIST.read_text())
        self.assertEqual(checklist['counts'], {'satisfied': 8, 'n/a': 4, 'missing': 0})
        self.assertIsNone(checklist['gate_status'])
        self.assertEqual(
            checklist['source_template']['sha256'],
            '56bcf6269a42031d9d90496e9a65c2292321aed2165033f6fb44ff8cc4d6b1cc',
        )
        self.assertEqual(len(checklist['items']), 12)
        statuses = [item['status'] for item in checklist['items']]
        self.assertEqual(statuses.count('satisfied'), 8)
        self.assertEqual(statuses.count('n/a'), 4)
        frozen = json.loads(orchestrator.FROZEN_EXPERIMENT.read_text())
        self.assertEqual(
            checklist['counts'],
            frozen['p16_preregistration_checklist']['counts'],
        )
        hold = json.loads(orchestrator.EXAMINER_HOLD.read_text())
        self.assertEqual(hold['status'], 'HOLD_PRE_PR')
        self.assertIs(hold['stub_ready'], False)
        self.assertIs(hold['digest_all_match_claimed'], False)
        stub = json.loads((orchestrator.LAB_BUNDLE / orchestrator.SCORECARD_JSON_NAME).read_text())
        self.assertEqual(stub['status'], 'HOLD_PRE_PR')
        self.assertIs(stub['metrics_all_null'], True)
        self.assertEqual(stub['template_sha256'], orchestrator.TEMPLATE_V12_SHA256)
        self.assertEqual(
            (orchestrator.LAB_BUNDLE / 'p16_preregistration_checklist.json').read_bytes(),
            orchestrator.P16_CHECKLIST.read_bytes(),
        )


class PinAndPathTests(unittest.TestCase):
    def test_digest_all_match_claimed_stays_false_for_absent_pins(self):
        pins = orchestrator.digest_status()
        self.assertIs(pins['digest_all_match_claimed'], False)
        binding = orchestrator.instrument_binding()
        self.assertIs(binding['digest_all_match_claimed'], False)
        for key in (
            'panel_admitted',
            'live_series_fee',
            'fresh_28_14_panel',
            'q6s1_scout_pdf',
            'invented_fills',
        ):
            self.assertIn(key, pins['missing'])
        self.assertEqual(len(binding['absent_pins']), 5)
        by_key = {row['key']: row for row in pins['pins']}
        for key in (
            'conductor_accept',
            'freeze',
            'panel_stub',
            'source_pins',
            'empty_results',
            'template_v12',
            'p16_pdf',
        ):
            self.assertIs(by_key[key]['match'], True)
        present = tuple(spec for spec in orchestrator.CLAIMED_PINS if spec[1])
        matched = orchestrator.digest_status(present)
        self.assertIs(matched['digest_all_match_claimed'], True)
        self.assertEqual(matched['missing'], [])
        flipped = (present[0][0], '0' * 64, present[0][2])
        broken = orchestrator.digest_status((flipped,) + present[1:])
        self.assertIs(broken['digest_all_match_claimed'], False)
        self.assertIn(present[0][0], broken['mismatch'])
        self.assertEqual(
            orchestrator.sha256_file(orchestrator.GOVERNANCE / orchestrator.ACCEPT_NAME),
            '162100624297588516390aab51ba0161cf15d0659c439ec6b60e940b99845635',
        )
        self.assertEqual(
            orchestrator.sha256_file(orchestrator.GOVERNANCE / orchestrator.FREEZE_NAME),
            'd86f7a402ea63fb132d80480f844a954fe9061a27b9b6bed125f9785ae64640e',
        )
        self.assertEqual(
            orchestrator.sha256_file(orchestrator.PANEL_STUB),
            'ed041c502d1f775d33c44bf900ac91b1339d99045bddd2052edd09a139ae2d3f',
        )
        canonical = orchestrator.GOVERNANCE_BUNDLE / 'SOURCE_PINS.json'
        for path in orchestrator.source_pin_paths():
            self.assertEqual(path.read_bytes(), canonical.read_bytes())
        self.assertFalse(orchestrator.PANEL_ADMITTED.exists())

    def test_panel_stub_bytes_and_admitted_at_stay_null(self):
        self.assertEqual(orchestrator.select_panel_path(), orchestrator.PANEL_STUB)
        panel = orchestrator.load_panel()
        self.assertEqual(len(panel['events']), 6)
        self.assertEqual(len(panel['markets']), 12)
        self.assertIsNone(panel['admitted_at'])
        self.assertIsNone(panel['results'])
        self.assertIsNone(panel['pnl'])
        self.assertEqual(panel['panel_version'], '2026-09-23.atp-kxatpmatch-v0')
        self.assertEqual(orchestrator.LAB_PANEL_STUB.read_bytes(), orchestrator.PANEL_STUB.read_bytes())
        self.assertEqual(
            (orchestrator.GOVERNANCE_BUNDLE / 'ATP_KXATPMATCH_PANEL_STUB_2026-09-23.json').read_bytes(),
            orchestrator.PANEL_STUB.read_bytes(),
        )
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
            widened = json.loads(orchestrator.PANEL_STUB.read_text())
            widened['markets'] = widened['markets'] + widened['markets']
            widened['cohort_summary']['markets_n'] = 24
            rejected = root / 'wide.json'
            rejected.write_text(json.dumps(widened))
            with self.assertRaises(orchestrator.InventedMarketRefused):
                orchestrator.load_panel(rejected, root / 'missing_admitted.json')

    def test_path_guards_do_not_touch_closed_labs(self):
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

    def test_admit_py_is_not_invoked(self):
        self.assertFalse((ROOT / 'admit.py').exists())
        self.assertEqual(list(ROOT.rglob('admit.py')), [])
        self.assertFalse(orchestrator.PANEL_ADMITTED.exists())
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / 'panel_admitted.json'
            with self.assertRaises(orchestrator.AdmitPyRefused):
                orchestrator.run_admit(target)
            self.assertFalse(target.exists())
        with self.assertRaises(orchestrator.AdmitPyRefused):
            orchestrator.refuse_adversary('admit_py')
        binding = orchestrator.instrument_binding()
        self.assertIs(binding['admit_py_run'], False)
        self.assertIsNone(binding['admitted_at'])
        self.assertEqual(binding['examiner_status'], 'HOLD_PRE_PR')
        for name in ('S1', 'S2', 'R2-P4', 'Cap-SR', 'ATP-FQ', 'Q6S5', 'PR57', 'Q6-000'):
            with self.assertRaises(orchestrator.UngateRefused):
                orchestrator.ungate(name)
        with self.assertRaises(orchestrator.LeeReadyRefused):
            orchestrator.infer_lee_ready({'classifier': 'lee-ready'})
        with self.assertRaises(orchestrator.AdversaryRefused):
            orchestrator.refuse_adversary('dual_cloud')
        with self.assertRaises(orchestrator.LiveOrdersForbidden):
            orchestrator.refuse_adversary('live_orders')


if __name__ == '__main__':
    unittest.main()
