"""Unit checks for the C1-RJ join gate. Not an Examiner score."""
import copy
import json
import unittest
from pathlib import Path

import orchestrator

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent


class PinTests(unittest.TestCase):
    def test_panel_parent_bytes_match_and_admitted_at_stays(self):
        before = orchestrator.CAPTURE_PANEL.read_bytes()
        panel = orchestrator.load_panel()
        self.assertEqual(panel['admitted_at'], '2026-09-23T00:49:43Z')
        self.assertEqual(panel['panel_version'], '2026-09-22.c1-kxufcfight-v0')
        self.assertEqual(len(panel['events']), 2)
        self.assertEqual(len(panel['markets']), 4)
        self.assertEqual(orchestrator.CAPTURE_PANEL.read_bytes(), before)
        self.assertEqual(
            orchestrator.sha256_file(orchestrator.GOV_PANEL),
            orchestrator.PANEL_SHA256,
        )
        self.assertEqual(
            orchestrator.sha256_file(orchestrator.CAPTURE_STUB),
            orchestrator.PRE_ADMIT_STUB_SHA256,
        )
        for market in panel['markets']:
            self.assertIsNone(market['admitted_at'])
        with self.assertRaises(orchestrator.AdmitPyRefused):
            orchestrator.run_admit()

    def test_pins_present_and_digests_match(self):
        pins = json.loads((ROOT / 'SOURCE_PINS.json').read_text())
        cited = {
            'C1_KXUFCFIGHT_SETTLED_RESOLUTION_JOIN_HARNESS_FREEZE_2026-09-23.md':
                '3ea3362ad3c16951369d5f90497ec6079213dd54e5556340c4d3738744126cf1',
            'CONDUCTOR_ACCEPT_C1_KXUFCFIGHT_SETTLED_JOIN_HARNESS_2026-09-24.json':
                '5c3d559a055482301340102246835c7657c6b5ba9b1ceb69022dbd04c9895ac3',
            'MAXIMIZE_PIN_2026-09-23_1750ET.md':
                '6fad9acbff410b36432c7f20f6d19adce37ee9703b9e42a7b0ba9e059f3990df',
            'scout_c1_settled_rejoin_2026-09-23/scout_settled_rejoin_C1_KXUFCFIGHT.json':
                '1175029927603a957a2ae2b1fcf1b59bb244118c1e090e53bf8278f4614a686f',
            'scout_c1_settled_rejoin_2026-09-23/SEED_SETTLED_SUMMARY.json':
                'b3e62f5902e5cf536d2635fdaee4613093ce0f397c26b3186b25d9c6eb742600',
            'scout_c1_settled_rejoin_2026-09-23/C1_KXUFCFIGHT_PANEL_STUB_2026-09-22.json':
                '24426d804c51bde23cf2557a11a8481a12026da10024094c4ae546d1f7d3956e',
            'scout_c1_settled_rejoin_2026-09-23/settled_reget_2026-09-23.json':
                '77457212b2427b9ef29499a6619cabf0b43955a569419acbb1abd468e2e79a23',
            'EXAMINER_HOLD_C1_KXUFCFIGHT_SETTLED_JOIN_HARNESS_PRE_PR_2026-09-23.json':
                '7ceb4bedf6a3e132ae410992851eb977e6cbdf85a337949d223be4bdb5de8a0b',
        }
        self.assertTrue(pins['digest_all_match_claimed'])
        self.assertEqual(pins['cited_freeze_sha256'], orchestrator.CITED_FREEZE_SHA256)
        self.assertEqual(cited[
            'C1_KXUFCFIGHT_SETTLED_RESOLUTION_JOIN_HARNESS_FREEZE_2026-09-23.md'
        ], orchestrator.CITED_FREEZE_SHA256)
        self.assertEqual(cited[
            'scout_c1_settled_rejoin_2026-09-23/C1_KXUFCFIGHT_PANEL_STUB_2026-09-22.json'
        ], orchestrator.PANEL_SHA256)
        recorded = pins['pins']
        self.assertEqual(set(recorded), set(cited))
        for name, digest in cited.items():
            entry = recorded[name]
            self.assertEqual(entry['sha256'], digest)
            path = REPO / entry['path']
            self.assertTrue(path.is_file(), entry['path'])
            self.assertEqual(orchestrator.sha256_file(path), digest)
        hold = recorded[
            'EXAMINER_HOLD_C1_KXUFCFIGHT_SETTLED_JOIN_HARNESS_PRE_PR_2026-09-23.json'
        ]
        self.assertEqual(hold['location'], 'in_repo')
        self.assertEqual(pins['scout_nonempty_result_N_declared'], 4)
        self.assertIsNone(pins['results'])
        self.assertIsNone(pins['pnl'])
        self.assertIsNone(pins['settled_join_n'])
        self.assertNotEqual(pins['settled_join_n'], 4)
        self.assertNotEqual(
            pins['settled_join_n'],
            pins['scout_nonempty_result_N_declared'],
        )

    def test_empty_results_and_frozen_stay_null(self):
        snapshot = orchestrator.frozen_output_snapshot()
        for value in snapshot.values():
            self.assertIsNone(value)
        empty = json.loads((ROOT / 'results' / 'EMPTY_RESULTS.json').read_text())
        root_empty = json.loads((ROOT / 'EMPTY_RESULTS.json').read_text())
        self.assertEqual(empty, root_empty)
        orchestrator.assert_null_scorecard(empty)
        hold = json.loads(
            (ROOT / 'EXAMINER_HOLD_C1_KXUFCFIGHT_SETTLED_JOIN_HARNESS_PRE_PR_2026-09-24.json').read_text()
        )
        self.assertEqual(hold['status'], 'HOLD_PRE_PR')
        self.assertFalse(hold['stub_ready'])
        self.assertTrue(hold['digest_all_match_claimed'])


class ArmTests(unittest.TestCase):
    def test_j0_and_j1_leave_the_scorecard_null(self):
        before = orchestrator.CAPTURE_PANEL.read_bytes()
        j0 = orchestrator.conduct(orchestrator.J0)
        j1 = orchestrator.conduct(orchestrator.J1)
        self.assertEqual(j0['join_gate'], 'nonempty_result_required')
        self.assertEqual(j1['join_gate'], 'occurrence_datetime_match')
        self.assertEqual(j0['source'], 'admitted_panel_parent_seeds')
        self.assertEqual(j1['source'], 'admitted_panel_parent_seeds')
        self.assertFalse(j0['scout_reget_loaded'])
        self.assertEqual(j0['event_count'], 2)
        self.assertEqual(j0['market_count'], 4)
        self.assertEqual(len(j0['row_labels']), 4)
        self.assertEqual(j0['admitted_at'], '2026-09-23T00:49:43Z')
        self.assertFalse(j0['list_429_backfilled'])
        self.assertFalse(j0['scout_n_copied_into_settled_join_n'])
        self.assertFalse(j0['admit_py_run'])
        self.assertFalse(j0['digest_all_match_claimed'])
        self.assertEqual(j0['lee_ready'], 'REFUSED')
        self.assertEqual(j0['examiner_status'], 'HOLD_PRE_PR')
        self.assertFalse(j0['stub_ready'])
        for report in (j0, j1):
            orchestrator.assert_null_scorecard(report)
            orchestrator.assert_null_scorecard(report['published'])
            self.assertIsNone(report['settled_join_n'])
            self.assertIsNone(report['occurrence_match_n'])
            self.assertIsNone(report['admit_ready_flag'])
            self.assertIsNone(report['results'])
            self.assertIsNone(report['pnl'])
            self.assertFalse(report['promoted'])
            self.assertNotEqual(report['settled_join_n'], 4)
            self.assertNotEqual(report['occurrence_match_n'], 4)
        self.assertEqual(orchestrator.CAPTURE_PANEL.read_bytes(), before)

    def test_occurrence_present_matches_event_sot_and_is_not_invented(self):
        panel = orchestrator.load_panel()
        j1 = orchestrator.conduct(orchestrator.J1, panel)
        clocks = {
            event['event_ticker']: event['occurrence_datetime']
            for event in panel['events']
        }
        for row in j1['row_labels']:
            self.assertEqual(row['j1'], 'occurrence_datetime_match')
            self.assertEqual(row['clock'], 'occurrence_datetime')
            self.assertIsNotNone(row['occurrence_datetime'])
            market = next(
                item for item in panel['markets']
                if item['market_ticker'] == row['key']
            )
            self.assertEqual(row['occurrence_datetime'], clocks[market['event_ticker']])
            self.assertEqual(market['occurrence_source'], 'live_get_market')
        self.assertFalse(j1['occurrence_datetime_invented'])
        binding = orchestrator.instrument_binding(panel)
        self.assertEqual(binding['j1_clock'], 'occurrence_datetime')
        self.assertFalse(binding['expected_expiration_substituted'])
        with self.assertRaises(orchestrator.InventedSoTRefused):
            orchestrator.assign_occurrence(orchestrator.PARENT_SEED_TICKERS[0], '2026-09-23T04:20:00Z')
        broken = copy.deepcopy(panel)
        broken['markets'][0]['occurrence_datetime'] = None
        with self.assertRaises(orchestrator.InventedSoTRefused):
            orchestrator.conduct(orchestrator.J1, broken)

    def test_scout_n_is_not_settled_join_n(self):
        binding = orchestrator.instrument_binding()
        self.assertEqual(binding['settled_nonempty_result_N_scout_declared'], 4)
        self.assertFalse(binding['scout_reget_loaded'])
        self.assertIsNone(binding['settled_join_n'])
        self.assertFalse(binding['scout_n_copied_into_settled_join_n'])
        with self.assertRaises(orchestrator.ScorecardPromotionRefused):
            orchestrator.copy_scout_n_into_settled_join(4)

    def test_unknown_gate_and_scorecard_write_are_refused(self):
        with self.assertRaises(orchestrator.UnknownGate):
            orchestrator.conduct('J2')
        with self.assertRaises(orchestrator.ScorecardPromotionRefused):
            orchestrator.write_scorecard(orchestrator.published_scorecard())
        for key in orchestrator.OUTPUT_KEYS:
            broken = dict(orchestrator.published_scorecard())
            broken[key] = 4
            with self.assertRaises(orchestrator.ScorecardPromotionRefused):
                orchestrator.write_scorecard(broken)


class RefuseTests(unittest.TestCase):
    def test_list_books_and_empty_orderbooks_are_not_invented(self):
        before = {
            path: path.read_bytes()
            for path in orchestrator.ORDERBOOK_DIR.glob('*.json')
        }
        books = orchestrator.assert_orderbooks_empty()
        self.assertEqual(len(books), 4)
        gaps = orchestrator.list_books()
        self.assertFalse(gaps['books_present'])
        self.assertFalse(gaps['list_429_backfilled'])
        self.assertFalse(gaps['markets_invented'])
        self.assertEqual(len(gaps['routes']), 3)
        with self.assertRaises(orchestrator.InventedResultRefused):
            orchestrator.backfill_list_429(
                'markets?series_ticker=KXUFCFIGHT&status=settled',
                result='yes',
                occurrence_datetime='2026-09-23T04:20:00Z',
            )
        with self.assertRaises(orchestrator.InventedResultRefused):
            orchestrator.invent_result(orchestrator.PARENT_SEED_TICKERS[0], 'yes')
        with self.assertRaises(orchestrator.InventedDepthRefused):
            orchestrator.quote_depth({'ticker': orchestrator.PARENT_SEED_TICKERS[0]})
        with self.assertRaises(orchestrator.InventedFillRefused):
            orchestrator.invent_fill({'ticker': orchestrator.PARENT_SEED_TICKERS[0]}, 1)
        with self.assertRaises(orchestrator.EmptyBookInventRefused):
            orchestrator.fill_empty_book(orchestrator.PARENT_SEED_TICKERS[0], [{'price': '0.50'}])
        after = {
            path: path.read_bytes()
            for path in orchestrator.ORDERBOOK_DIR.glob('*.json')
        }
        self.assertEqual(before, after)

    def test_lee_ready_live_orders_admit_ungate_reopens_refused(self):
        for sample in (None, {}, {'result': 'yes'}, 'quote'):
            with self.assertRaises(orchestrator.LeeReadyRefused):
                orchestrator.infer_lee_ready(sample)
        for label in (
            'cap_sr_reopen',
            'fq_reopen',
            'empty_ob_reopen',
            'c3_rj_reopen',
            'c5_rj_reopen',
            'r3p3_rj_reopen',
            'nhl_rj_reopen',
            's4_rj_reopen',
            'r2p3_rj_reopen',
            's5_rj_reopen',
            'arm_b',
            'q7_arm_b',
            'q6_retune',
        ):
            with self.assertRaises(orchestrator.AdversaryRefused):
                orchestrator.refuse_adversary(label)
        with self.assertRaises(orchestrator.AdmitPyRefused):
            orchestrator.refuse_adversary('admit_py')
        with self.assertRaises(orchestrator.LiveOrdersForbidden):
            orchestrator.execution_adapter()
        with self.assertRaises(orchestrator.LiveOrdersForbidden):
            orchestrator.assert_public_get('POST')
        self.assertIsNone(orchestrator.assert_public_get('GET'))
        for name in ('S1', 'S2', 'R2-P4'):
            with self.assertRaises(orchestrator.UngateRefused):
                orchestrator.ungate(name)
        with self.assertRaises(orchestrator.ExaminerNotReady):
            orchestrator.claim_admit_ready()
        with self.assertRaises(orchestrator.ExaminerNotReady):
            orchestrator.claim_examiner_ready()
        source = (ROOT / 'orchestrator.py').read_text()
        for banned in (
            '0.0175',
            '0.07',
            'class KalshiExecutionAdapter',
            'urlopen',
            'urllib',
            'os.environ',
            'api_key',
            'private_key',
        ):
            self.assertNotIn(banned, source)

    def test_capture_and_sibling_bytes_unchanged(self):
        sentinels = [
            REPO / 'lab/astra-capture/c1-kxufcfight/panel_admitted.json',
            REPO / 'lab/astra-capture/c1-kxufcfight/panel_stub.json',
            REPO / 'kalshi_c1_empty_ob_lab_20260923/orchestrator.py',
            REPO / 'kalshi_c1_kxufcfight_honesty_lab_20260922/orchestrator.py',
            REPO / 'kalshi_s5_kxmvecrosscategory_settled_join_lab_20260923/orchestrator.py',
            REPO / 'nfl_q7_rehab_p2_rank_sizing_20260923/test_rank_sizing.py',
        ]
        sentinels.extend(orchestrator.ORDERBOOK_DIR.glob('*.json'))
        before = {path: path.read_bytes() for path in sentinels}
        orchestrator.conduct(orchestrator.J0)
        orchestrator.conduct(orchestrator.J1)
        for path, raw in before.items():
            self.assertEqual(path.read_bytes(), raw)


if __name__ == '__main__':
    unittest.main()
