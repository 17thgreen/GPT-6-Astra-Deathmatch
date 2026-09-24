"""Unit checks for the C4-RJ join gate. Not an Examiner score."""
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
        self.assertIsNone(panel['admitted_at'])
        self.assertEqual(panel['panel_version'], '2026-09-23.c4-kxcpi-v0')
        self.assertEqual(panel['stub_status'], 'NOT_ADMITTED')
        self.assertEqual(len(panel['events']), 4)
        self.assertEqual(len(panel['markets']), 44)
        self.assertEqual(orchestrator.CAPTURE_PANEL.read_bytes(), before)
        self.assertEqual(orchestrator.sha256_file(orchestrator.GOV_PANEL), orchestrator.PANEL_SHA256)
        self.assertEqual(orchestrator.sha256_file(orchestrator.SCOUT_PANEL), orchestrator.PANEL_SHA256)
        with self.assertRaises(orchestrator.AdmitPyRefused):
            orchestrator.run_admit()

    def test_pins_present_and_digests_match(self):
        blobs = [path.read_bytes() for path in orchestrator.SOURCE_PIN_MIRRORS]
        self.assertEqual(len(blobs), 4)
        self.assertTrue(all(blob == blobs[0] for blob in blobs[1:]))
        pins = json.loads(blobs[0])
        self.assertTrue(pins['digest_all_match_claimed'])
        self.assertTrue(orchestrator.listed_digest_match(pins))
        self.assertEqual(pins['cited_freeze_sha256'], orchestrator.CITED_FREEZE_SHA256)
        self.assertEqual(pins['accept_sha256'], orchestrator.ACCEPT_SHA256)
        required = (
            'lab/governance/astra/packets/C4_KXCPI_SETTLED_RESOLUTION_JOIN_HARNESS_FREEZE_2026-09-24.md',
            'lab/governance/astra/packets/CONDUCTOR_ACCEPT_C4_KXCPI_SETTLED_JOIN_HARNESS_2026-09-24.json',
            'lab/governance/astra/packets/MAXIMIZE_PIN_2026-09-24_1926ET.md',
            'lab/governance/astra/packets/EXAMINER_HOLD_C4_KXCPI_SETTLED_JOIN_HARNESS_PRE_PR_2026-09-24.json',
            'lab/governance/astra/packets/scout_c4_settled_rejoin_2026-09-24/scout_settled_rejoin_C4_KXCPI.json',
            'lab/governance/astra/packets/scout_c4_settled_rejoin_2026-09-24/SEED_SETTLED_SUMMARY.json',
            'lab/governance/astra/packets/scout_c4_settled_rejoin_2026-09-24/C4_KXCPI_PANEL_STUB_2026-09-23.json',
            'lab/governance/astra/packets/scout_c4_settled_rejoin_2026-09-24/settled_reget_2026-09-24.json',
            'lab/astra-capture/c4-kxcpi/panel_stub.json',
            'lab/astra-capture/c4-kxcpi/settled_reget_2026-09-24.json',
        )
        recorded = pins['pins']
        for name in required:
            self.assertIn(name, recorded)
        for name, entry in recorded.items():
            path = REPO / entry['path']
            self.assertTrue(path.is_file(), entry['path'])
            self.assertEqual(orchestrator.sha256_file(path), entry['sha256'])
            self.assertEqual(path.stat().st_size, entry['bytes'])
            self.assertEqual(entry['path'], name)
        hold = recorded[
            'lab/governance/astra/packets/EXAMINER_HOLD_C4_KXCPI_SETTLED_JOIN_HARNESS_PRE_PR_2026-09-24.json'
        ]
        self.assertEqual(hold['location'], 'in_repo')
        self.assertEqual(hold['sha256'], orchestrator.EXAMINER_HOLD_SHA256)
        self.assertEqual(pins['scout_nonempty_result_N_declared'], 25)
        self.assertIsNone(pins['results'])
        self.assertIsNone(pins['pnl'])
        self.assertIsNone(pins['settled_join_n'])
        self.assertIsNone(pins['admitted_at'])
        self.assertNotEqual(pins['settled_join_n'], 25)
        self.assertNotEqual(pins['settled_join_n'], pins['scout_nonempty_result_N_declared'])

    def test_empty_results_and_frozen_stay_null(self):
        snapshot = orchestrator.frozen_output_snapshot()
        for value in snapshot.values():
            self.assertIsNone(value)
        empty = json.loads((ROOT / 'results' / 'EMPTY_RESULTS.json').read_text())
        root_empty = json.loads((ROOT / 'EMPTY_RESULTS.json').read_text())
        self.assertEqual(empty, root_empty)
        orchestrator.assert_null_scorecard(empty)
        hold = json.loads((ROOT / 'EXAMINER_HOLD_C4_KXCPI_SETTLED_JOIN_HARNESS_PRE_PR_2026-09-24.json').read_text())
        self.assertEqual(
            (ROOT / 'EXAMINER_HOLD_C4_KXCPI_SETTLED_JOIN_HARNESS_PRE_PR_2026-09-24.json').read_bytes(),
            orchestrator.HOLD_PATH.read_bytes(),
        )
        self.assertEqual(hold['status'], 'HOLD_PRE_PR')
        self.assertFalse(hold['stub_ready'])
        self.assertIsNone(hold['admitted_at'])


class ArmTests(unittest.TestCase):
    def test_j0_and_j1_leave_the_scorecard_null(self):
        before = orchestrator.CAPTURE_PANEL.read_bytes()
        j0 = orchestrator.conduct(orchestrator.J0)
        j1 = orchestrator.conduct(orchestrator.J1)
        self.assertEqual(j0['join_gate'], 'nonempty_result_required')
        self.assertEqual(j1['join_gate'], 'occurrence_datetime_match')
        self.assertTrue(j0['scout_reget_loaded'])
        self.assertFalse(j0['live_fetch'])
        self.assertEqual(j0['event_count'], 4)
        self.assertEqual(j0['market_count'], 44)
        self.assertEqual(j0['settled_label_count'], 25)
        self.assertEqual(j0['fallback_label_count'], 21)
        self.assertIsNone(j0['admitted_at'])
        self.assertFalse(j0['list_429_backfilled'])
        self.assertFalse(j0['missing_events_backfilled'])
        self.assertFalse(j0['scout_n_copied_into_settled_join_n'])
        self.assertFalse(j0['admit_py_run'])
        self.assertTrue(j0['digest_all_match_claimed'])
        self.assertEqual(j0['lee_ready'], 'REFUSED')
        self.assertEqual(j0['examiner_status'], 'HOLD_PRE_PR')
        self.assertFalse(j0['stub_ready'])
        self.assertEqual(j0['fee_queue_book_fill_tape'], 'HELD')
        for report in (j0, j1):
            orchestrator.assert_null_scorecard(report)
            orchestrator.assert_null_scorecard(report['published'])
            self.assertIsNone(report['settled_join_n'])
            self.assertIsNone(report['occurrence_match_n'])
            self.assertIsNone(report['admit_ready_flag'])
            self.assertIsNone(report['results'])
            self.assertIsNone(report['pnl'])
            self.assertIsNone(report['admitted_at'])
            self.assertFalse(report['promoted'])
            self.assertNotEqual(report['settled_join_n'], 25)
            self.assertNotEqual(report['occurrence_match_n'], 25)
        self.assertEqual(orchestrator.CAPTURE_PANEL.read_bytes(), before)

    def test_j1_fallback_is_labeled_and_does_not_write_occurrence(self):
        panel_before = orchestrator.CAPTURE_PANEL.read_bytes()
        raw_sep = (orchestrator.SCOUT_DIR / 'raw/event_KXCPI_26SEP_parent.json').read_bytes()
        panel = orchestrator.load_panel()
        j1 = orchestrator.conduct(orchestrator.J1, panel)
        settled = [row for row in j1['row_labels'] if row['cohort'] == 'settled_reget']
        parent = [row for row in j1['row_labels'] if row['cohort'] == 'parent_panel']
        self.assertEqual(len(settled), 25)
        self.assertEqual(len(parent), 44)
        for row in settled:
            self.assertEqual(row['join_source'], 'occurrence_datetime')
            self.assertEqual(row['clock'], 'occurrence_datetime')
            self.assertIsNotNone(row['occurrence_datetime'])
            self.assertNotEqual(row['occurrence_datetime'], row['expected_expiration_time'])
            self.assertEqual(row['occurrence_datetime'], row['event_occurrence_datetime'])
            self.assertIn(row['result'], ('yes', 'no'))
        fallback = [row for row in parent if row['occurrence_datetime'] is None]
        self.assertEqual(len(fallback), 21)
        for row in fallback:
            self.assertEqual(row['join_source'], 'expected_expiration_time_fallback')
            self.assertEqual(row['clock'], 'expected_expiration_time')
            self.assertIsNone(row['occurrence_datetime'])
            self.assertIsNotNone(row['expected_expiration_time'])
            self.assertNotEqual(row['occurrence_datetime'], row['expected_expiration_time'])
        direct = [row for row in parent if row['occurrence_datetime'] is not None]
        self.assertEqual(len(direct), 23)
        for row in direct:
            self.assertEqual(row['join_source'], 'occurrence_datetime')
            self.assertEqual(row['occurrence_datetime'], row['event_occurrence_datetime'])
        sep = [row for row in fallback if row['event_ticker'] == 'KXCPI-26SEP']
        self.assertEqual(len(sep), 7)
        self.assertFalse(j1['occurrence_datetime_invented'])
        self.assertFalse(j1['expected_expiration_written_into_occurrence_datetime'])
        binding = orchestrator.instrument_binding(panel)
        self.assertEqual(binding['j1_fallback_join_source'], 'expected_expiration_time_fallback')
        self.assertFalse(binding['expected_expiration_written_into_occurrence_datetime'])
        self.assertIsNone(binding['settled_join_n'])
        with self.assertRaises(orchestrator.InventedSoTRefused):
            orchestrator.assign_occurrence('KXCPI-26SEP-T0.1', '2026-10-14T13:56:00Z')
        broken = copy.deepcopy(panel)
        broken['markets'][0]['occurrence_datetime'] = '1999-01-01T00:00:00Z'
        with self.assertRaises(orchestrator.OccurrenceIntegrityRefused):
            orchestrator.conduct(orchestrator.J1, broken)
        self.assertEqual(orchestrator.CAPTURE_PANEL.read_bytes(), panel_before)
        self.assertEqual(
            (orchestrator.SCOUT_DIR / 'raw/event_KXCPI_26SEP_parent.json').read_bytes(),
            raw_sep,
        )

    def test_scout_n_is_not_settled_join_n(self):
        binding = orchestrator.instrument_binding()
        self.assertEqual(binding['settled_nonempty_result_N_scout_declared'], 25)
        self.assertTrue(binding['scout_reget_loaded'])
        self.assertFalse(binding['live_fetch'])
        self.assertIsNone(binding['settled_join_n'])
        self.assertIsNone(binding['admitted_at'])
        self.assertFalse(binding['scout_n_copied_into_settled_join_n'])
        self.assertEqual(binding['settled_row_label_count'], 25)
        self.assertNotEqual(binding['settled_join_n'], binding['settled_row_label_count'])
        with self.assertRaises(orchestrator.ScorecardPromotionRefused):
            orchestrator.copy_scout_n_into_settled_join(25)

    def test_unknown_gate_and_scorecard_write_are_refused(self):
        with self.assertRaises(orchestrator.UnknownGate):
            orchestrator.conduct('J2')
        with self.assertRaises(orchestrator.ScorecardPromotionRefused):
            orchestrator.write_scorecard(orchestrator.published_scorecard())
        for key in orchestrator.OUTPUT_KEYS:
            broken = dict(orchestrator.published_scorecard())
            broken[key] = 25
            with self.assertRaises(orchestrator.ScorecardPromotionRefused):
                orchestrator.write_scorecard(broken)


class RefuseTests(unittest.TestCase):
    def test_list_gaps_and_fee_queue_book_fill_tape_are_not_filled(self):
        gaps = orchestrator.list_books()
        self.assertFalse(gaps['books_present'])
        self.assertFalse(gaps['list_429_backfilled'])
        self.assertFalse(gaps['markets_invented'])
        self.assertFalse(gaps['missing_events_backfilled'])
        self.assertEqual(gaps['missing_events'], ['KXCPI-26JUN', 'KXCPI-26MAY', 'KXCPI-26APR'])
        self.assertEqual(len(gaps['routes']), 2)
        with self.assertRaises(orchestrator.InventedResultRefused):
            orchestrator.backfill_list_429(
                'markets?series_ticker=KXCPI&status=settled&limit=20',
                result='yes',
                occurrence_datetime='2026-09-11T13:11:28.126Z',
            )
        for event_ticker in ('KXCPI-26JUN', 'KXCPI-26MAY', 'KXCPI-26APR'):
            with self.assertRaises(orchestrator.InventedMarketRefused):
                orchestrator.backfill_missing_events(event_ticker, markets=[])
        with self.assertRaises(orchestrator.InventedResultRefused):
            orchestrator.invent_result('KXCPI-26AUG-T0.4', 'yes')
        with self.assertRaises(orchestrator.InventedDepthRefused):
            orchestrator.quote_depth({'ticker': 'KXCPI-26AUG-T0.4'})
        with self.assertRaises(orchestrator.InventedFillRefused):
            orchestrator.invent_fill({'ticker': 'KXCPI-26AUG-T0.4'}, 1)
        with self.assertRaises(orchestrator.AdversaryRefused):
            orchestrator.fee_metric({'ticker': 'KXCPI-26AUG-T0.4'}, 1)
        with self.assertRaises(orchestrator.InventedDepthRefused):
            orchestrator.queue_metric({'ticker': 'KXCPI-26AUG-T0.4'}, 1)
        with self.assertRaises(orchestrator.InventedDepthRefused):
            orchestrator.book_metric({'ticker': 'KXCPI-26AUG-T0.4'}, 1)
        with self.assertRaises(orchestrator.InventedFillRefused):
            orchestrator.tape_metric({'ticker': 'KXCPI-26AUG-T0.4'}, 1)

    def test_lee_ready_live_orders_admit_ungate_reopens_refused(self):
        for sample in (None, {}, {'result': 'yes'}, 'quote'):
            with self.assertRaises(orchestrator.LeeReadyRefused):
                orchestrator.infer_lee_ready(sample)
        for label in (
            'cap_sr_reopen',
            'fq_reopen',
            'cpi_fq_reopen',
            'c1_rj_reopen',
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
        with self.assertRaises(orchestrator.InventedFillRefused):
            orchestrator.refuse_adversary('fill_metric')
        with self.assertRaises(orchestrator.InventedFillRefused):
            orchestrator.refuse_adversary('tape_metric')
        with self.assertRaises(orchestrator.InventedDepthRefused):
            orchestrator.refuse_adversary('book_metric')
        with self.assertRaises(orchestrator.InventedMarketRefused):
            orchestrator.refuse_adversary('backfill_missing_events')
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
            REPO / 'lab/astra-capture/c4-kxcpi/panel_stub.json',
            REPO / 'kalshi_c4_kxcpi_feequue_lab_20260923/orchestrator.py',
            REPO / 'kalshi_c1_kxufcfight_settled_join_lab_20260923/orchestrator.py',
            REPO / 'lab/governance/astra/packets/EXAMINER_HOLD_C4_KXCPI_SETTLED_JOIN_HARNESS_PRE_PR_2026-09-24.json',
            REPO / 'lab/governance/astra/packets/scout_c4_settled_rejoin_2026-09-24/raw/event_KXCPI_26SEP_parent.json',
            REPO / 'lab/governance/astra/packets/scout_c4_settled_rejoin_2026-09-24/scout_settled_rejoin_C4_KXCPI.json',
        ]
        before = {path: path.read_bytes() for path in sentinels}
        orchestrator.conduct(orchestrator.J0)
        orchestrator.conduct(orchestrator.J1)
        for path, raw in before.items():
            self.assertEqual(path.read_bytes(), raw)


if __name__ == '__main__':
    unittest.main()
