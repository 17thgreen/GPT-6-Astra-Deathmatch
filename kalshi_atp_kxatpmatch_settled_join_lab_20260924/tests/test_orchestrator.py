"""Unit checks for the ATP-RJ join gate. Not an Examiner score."""
import copy
import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

import orchestrator

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent


def _market(ticker, event, result, occurrence, settlement, status='finalized'):
    return {
        'ticker': ticker,
        'event_ticker': event,
        'status': status,
        'result': result,
        'occurrence_datetime': occurrence,
        'expected_expiration_time': '2026-09-25T12:00:00Z',
        'settlement_ts': settlement,
    }


class PinTests(unittest.TestCase):
    def test_panel_parent_bytes_match_and_admitted_at_stays(self):
        before = orchestrator.CAPTURE_PANEL.read_bytes()
        panel = orchestrator.load_panel()
        self.assertIsNone(panel['admitted_at'])
        self.assertEqual(panel['panel_version'], '2026-09-23.atp-kxatpmatch-v0')
        self.assertEqual(panel['stub_status'], 'NOT_ADMITTED')
        self.assertEqual(len(panel['events']), 6)
        self.assertEqual(len(panel['markets']), 12)
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
        self.assertEqual(pins['scorecard_template_v1_2_sha256'], orchestrator.SCORECARD_TEMPLATE_SHA256)
        required = (
            'lab/governance/astra/packets/ATP_KXATPMATCH_SETTLED_RESOLUTION_JOIN_HARNESS_FREEZE_2026-09-24.md',
            'lab/governance/astra/packets/CONDUCTOR_ACCEPT_ATP_KXATPMATCH_SETTLED_RESOLUTION_JOIN_HARNESS_2026-09-24.json',
            'lab/governance/astra/packets/MAXIMIZE_PIN_2026-09-24_1948ET.md',
            'lab/governance/astra/packets/EXAMINER_HOLD_ATP_KXATPMATCH_SETTLED_JOIN_HARNESS_PRE_PR_2026-09-24.json',
            'lab/governance/astra/packets/SUGGESTED_CONDUCTOR_ACCEPT_PING_ATP_RJ_2026-09-24.json',
            'lab/governance/astra/packets/scout_atp_settled_rejoin_2026-09-24/scout_settled_rejoin_ATP_KXATPMATCH.json',
            'lab/governance/astra/packets/scout_atp_settled_rejoin_2026-09-24/SEED_SETTLED_SUMMARY.json',
            'lab/governance/astra/packets/scout_atp_settled_rejoin_2026-09-24/ATP_KXATPMATCH_PANEL_STUB_2026-09-23.json',
            'lab/governance/astra/packets/scout_atp_settled_rejoin_2026-09-24/settled_reget_2026-09-24.json',
            'lab/astra-capture/atp-kxatpmatch/panel_stub.json',
            'lab/astra-capture/atp-kxatpmatch/settled_reget_2026-09-24.json',
            'lab/governance/astra/templates/EXAMINER_KALSHI_SCORECARD_TEMPLATE_v1.2.json',
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
            'lab/governance/astra/packets/EXAMINER_HOLD_ATP_KXATPMATCH_SETTLED_JOIN_HARNESS_PRE_PR_2026-09-24.json'
        ]
        self.assertEqual(hold['location'], 'in_repo')
        self.assertEqual(hold['sha256'], orchestrator.EXAMINER_HOLD_SHA256)
        self.assertEqual(pins['scout_nonempty_result_N_declared'], 30)
        self.assertIsNone(pins['results'])
        self.assertIsNone(pins['pnl'])
        self.assertIsNone(pins['settled_join_n'])
        self.assertIsNone(pins['occurrence_match_n'])
        self.assertIsNone(pins['fallback_join_n'])
        self.assertIsNone(pins['admitted_at'])
        self.assertNotEqual(pins['settled_join_n'], 30)
        self.assertNotEqual(pins['settled_join_n'], pins['scout_nonempty_result_N_declared'])

    def test_empty_results_and_frozen_stay_null(self):
        snapshot = orchestrator.frozen_output_snapshot()
        for value in snapshot.values():
            self.assertIsNone(value)
        empty = json.loads((ROOT / 'results' / 'EMPTY_RESULTS.json').read_text())
        root_empty = json.loads((ROOT / 'EMPTY_RESULTS.json').read_text())
        self.assertEqual(empty, root_empty)
        orchestrator.assert_null_scorecard(empty)
        calibration = empty['examiner_scorecard_v1_2']['common_scorecard']['calibration']
        self.assertIsNone(calibration['value'])
        self.assertFalse(calibration['measured'])
        self.assertFalse(calibration['emits_probabilities'])
        self.assertEqual(
            empty['examiner_scorecard_v1_2']['template']['json_sha256'],
            orchestrator.SCORECARD_TEMPLATE_SHA256,
        )
        hold = json.loads((ROOT / 'EXAMINER_HOLD_ATP_KXATPMATCH_SETTLED_JOIN_HARNESS_PRE_PR_2026-09-24.json').read_text())
        self.assertEqual(
            (ROOT / 'EXAMINER_HOLD_ATP_KXATPMATCH_SETTLED_JOIN_HARNESS_PRE_PR_2026-09-24.json').read_bytes(),
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
        self.assertEqual(j0['event_count'], 6)
        self.assertEqual(j0['market_count'], 12)
        self.assertEqual(j0['settled_label_count'], 30)
        self.assertEqual(j0['fallback_label_count'], 0)
        self.assertIsNone(j0['admitted_at'])
        self.assertFalse(j0['list_429_backfilled'])
        self.assertFalse(j0['events_page2_backfilled'])
        self.assertFalse(j0['outside_list_parent_added_to_n'])
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
            self.assertIsNone(report['fallback_join_n'])
            self.assertIsNone(report['admit_ready_flag'])
            self.assertIsNone(report['results'])
            self.assertIsNone(report['pnl'])
            self.assertIsNone(report['admitted_at'])
            self.assertFalse(report['promoted'])
            self.assertNotEqual(report['settled_join_n'], 30)
            self.assertNotEqual(report['occurrence_match_n'], 30)
        self.assertEqual(orchestrator.CAPTURE_PANEL.read_bytes(), before)

    def test_j1_fallback_is_labeled_and_does_not_write_occurrence(self):
        panel_before = orchestrator.CAPTURE_PANEL.read_bytes()
        raw_parent = (orchestrator.SCOUT_DIR / 'raw/event_KXATPMATCH_26SEP22HARGAL_parent.json').read_bytes()
        panel = orchestrator.load_panel()
        j1 = orchestrator.conduct(orchestrator.J1, panel)
        settled = [row for row in j1['row_labels'] if row['cohort'] == 'settled_reget']
        parent = [row for row in j1['row_labels'] if row['cohort'] == 'parent_panel']
        self.assertEqual(len(settled), 30)
        self.assertEqual(len(parent), 12)
        for row in settled:
            self.assertEqual(row['join_source'], 'occurrence_datetime')
            self.assertEqual(row['clock'], 'occurrence_datetime')
            self.assertIsNotNone(row['occurrence_datetime'])
            self.assertEqual(row['occurrence_datetime'], row['expected_expiration_time'])
            self.assertEqual(row['occurrence_datetime'], row['event_occurrence_datetime'])
            self.assertIn(row['result'], ('yes', 'no'))
            self.assertIsNotNone(row['settlement_ts'])
        for row in parent:
            self.assertEqual(row['join_source'], 'occurrence_datetime')
            self.assertEqual(row['occurrence_datetime'], row['event_occurrence_datetime'])
            self.assertIsNotNone(row['occurrence_datetime'])
        sample = copy.deepcopy(panel['markets'][0])
        sample['occurrence_datetime'] = None
        expected = sample['expected_expiration_time']
        labeled = orchestrator.j1_label(sample, panel['events'][0]['occurrence_datetime'])
        self.assertEqual(labeled['join_source'], 'expected_expiration_time_fallback')
        self.assertEqual(labeled['clock'], 'expected_expiration_time')
        self.assertIsNone(labeled['occurrence_datetime'])
        self.assertEqual(labeled['expected_expiration_time'], expected)
        self.assertIsNone(sample['occurrence_datetime'])
        self.assertNotEqual(labeled['occurrence_datetime'], labeled['expected_expiration_time'])
        self.assertFalse(j1['occurrence_datetime_invented'])
        self.assertFalse(j1['expected_expiration_written_into_occurrence_datetime'])
        binding = orchestrator.instrument_binding(panel)
        self.assertEqual(binding['j1_fallback_join_source'], 'expected_expiration_time_fallback')
        self.assertFalse(binding['expected_expiration_written_into_occurrence_datetime'])
        self.assertEqual(binding['fallback_row_label_count'], 0)
        self.assertIsNone(binding['settled_join_n'])
        self.assertIsNone(binding['fallback_join_n'])
        untouched = {'occurrence_datetime': None, 'expected_expiration_time': expected}
        with self.assertRaises(orchestrator.InventedSoTRefused):
            orchestrator.assign_occurrence('KXATPMATCH-26SEP22HARGAL-HAR', '2026-09-22T12:00:00Z')
        with self.assertRaises(orchestrator.InventedSoTRefused):
            orchestrator.write_expected_expiration_into_occurrence_datetime(untouched)
        self.assertIsNone(untouched['occurrence_datetime'])
        broken = copy.deepcopy(panel)
        broken['markets'][0]['occurrence_datetime'] = '1999-01-01T00:00:00Z'
        with self.assertRaises(orchestrator.OccurrenceIntegrityRefused):
            orchestrator.conduct(orchestrator.J1, broken)
        self.assertEqual(orchestrator.CAPTURE_PANEL.read_bytes(), panel_before)
        self.assertEqual(
            (orchestrator.SCOUT_DIR / 'raw/event_KXATPMATCH_26SEP22HARGAL_parent.json').read_bytes(),
            raw_parent,
        )

    def test_scout_n_is_not_settled_join_n(self):
        binding = orchestrator.instrument_binding()
        self.assertEqual(binding['settled_nonempty_result_N_scout_declared'], 30)
        self.assertTrue(binding['scout_reget_loaded'])
        self.assertFalse(binding['live_fetch'])
        self.assertIsNone(binding['settled_join_n'])
        self.assertIsNone(binding['fallback_join_n'])
        self.assertIsNone(binding['admitted_at'])
        self.assertFalse(binding['scout_n_copied_into_settled_join_n'])
        self.assertEqual(binding['settled_row_label_count'], 30)
        self.assertNotEqual(binding['settled_join_n'], binding['settled_row_label_count'])
        with self.assertRaises(orchestrator.ScorecardPromotionRefused):
            orchestrator.copy_scout_n_into_settled_join(30)

    def test_unknown_gate_and_scorecard_write_are_refused(self):
        with self.assertRaises(orchestrator.UnknownGate):
            orchestrator.conduct('J2')
        with self.assertRaises(orchestrator.ScorecardPromotionRefused):
            orchestrator.write_scorecard(orchestrator.published_scorecard())
        for key in orchestrator.OUTPUT_KEYS:
            broken = dict(orchestrator.published_scorecard())
            broken[key] = 30
            with self.assertRaises(orchestrator.ScorecardPromotionRefused):
                orchestrator.write_scorecard(broken)


class RefuseTests(unittest.TestCase):
    def test_list_gaps_and_fee_queue_book_fill_tape_are_not_filled(self):
        gaps = orchestrator.list_books()
        self.assertFalse(gaps['books_present'])
        self.assertFalse(gaps['list_429_backfilled'])
        self.assertFalse(gaps['markets_invented'])
        self.assertFalse(gaps['events_page2_fetched'])
        self.assertFalse(gaps['events_page2_backfilled'])
        self.assertFalse(gaps['outside_list_parent_added_to_n'])
        self.assertEqual(
            gaps['outside_list_parent_events'],
            ['KXATPMATCH-26SEP22HARGAL', 'KXATPMATCH-26SEP22MOCKOT'],
        )
        self.assertEqual(len(gaps['routes']), 2)
        with self.assertRaises(orchestrator.InventedResultRefused):
            orchestrator.backfill_list_429(
                'markets?series_ticker=KXATPMATCH&status=settled&limit=30',
                result='yes',
                occurrence_datetime='2026-09-24T10:20:00Z',
            )
        with self.assertRaises(orchestrator.InventedMarketRefused):
            orchestrator.backfill_events_page2('CgYInIrP1QYSGEtYQVRQ', markets=[])
        for event_ticker in ('KXATPMATCH-26SEP22HARGAL', 'KXATPMATCH-26SEP22MOCKOT'):
            with self.assertRaises(orchestrator.InventedMarketRefused):
                orchestrator.add_outside_list_parent(event_ticker, markets=[])
        with self.assertRaises(orchestrator.InventedResultRefused):
            orchestrator.invent_result('KXATPMATCH-26SEP24HARKOV-HAR', 'yes')
        with self.assertRaises(orchestrator.InventedDepthRefused):
            orchestrator.quote_depth({'ticker': 'KXATPMATCH-26SEP24HARKOV-HAR'})
        with self.assertRaises(orchestrator.InventedFillRefused):
            orchestrator.invent_fill({'ticker': 'KXATPMATCH-26SEP24HARKOV-HAR'}, 1)
        with self.assertRaises(orchestrator.AdversaryRefused):
            orchestrator.fee_metric({'ticker': 'KXATPMATCH-26SEP24HARKOV-HAR'}, 1)
        with self.assertRaises(orchestrator.InventedDepthRefused):
            orchestrator.queue_metric({'ticker': 'KXATPMATCH-26SEP24HARKOV-HAR'}, 1)
        with self.assertRaises(orchestrator.InventedDepthRefused):
            orchestrator.book_metric({'ticker': 'KXATPMATCH-26SEP24HARKOV-HAR'}, 1)
        with self.assertRaises(orchestrator.InventedFillRefused):
            orchestrator.tape_metric({'ticker': 'KXATPMATCH-26SEP24HARKOV-HAR'}, 1)

    def test_lee_ready_live_orders_admit_ungate_reopens_refused(self):
        for sample in (None, {}, {'result': 'yes'}, 'quote'):
            with self.assertRaises(orchestrator.LeeReadyRefused):
                orchestrator.infer_lee_ready(sample)
        for label in (
            'cap_sr_reopen',
            'fq_reopen',
            'atp_fq_reopen',
            'cpi_fq_reopen',
            'c1_rj_reopen',
            'c3_rj_reopen',
            'c4_rj_reopen',
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
            orchestrator.refuse_adversary('events_page2_backfill')
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
        with self.assertRaises(orchestrator.AdmitPyRefused):
            orchestrator.main(['admit'])
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
            REPO / 'lab/astra-capture/atp-kxatpmatch/panel_stub.json',
            REPO / 'kalshi_atp_kxatpmatch_feequue_lab_20260923/orchestrator.py',
            REPO / 'kalshi_c4_kxcpi_settled_join_lab_20260924/orchestrator.py',
            REPO / 'lab/governance/astra/packets/EXAMINER_HOLD_ATP_KXATPMATCH_SETTLED_JOIN_HARNESS_PRE_PR_2026-09-24.json',
            REPO / 'lab/governance/astra/packets/scout_atp_settled_rejoin_2026-09-24/raw/event_KXATPMATCH_26SEP22HARGAL_parent.json',
            REPO / 'lab/governance/astra/packets/scout_atp_settled_rejoin_2026-09-24/scout_settled_rejoin_ATP_KXATPMATCH.json',
        ]
        before = {path: path.read_bytes() for path in sentinels}
        orchestrator.conduct(orchestrator.J0)
        orchestrator.conduct(orchestrator.J1)
        for path, raw in before.items():
            self.assertEqual(path.read_bytes(), raw)


class MeasurementTests(unittest.TestCase):
    def _transport(self, markets_body, events_pages):
        calls = []

        def transport(url):
            calls.append(url)
            if '/markets?' in url:
                return 200, markets_body
            if 'cursor=' in url:
                status, body = events_pages[1]
                return status, body
            status, body = events_pages[0]
            return status, body

        return transport, calls

    def test_since_filter_and_j0_j1_counts_and_fallback_label(self):
        since = '2026-09-24T23:52:00Z'
        scout_ticker = 'KXATPMATCH-26SEP24HARKOV-HAR'
        markets = [
            _market(scout_ticker, 'KXATPMATCH-26SEP24HARKOV', 'yes', '2026-09-24T10:20:00Z', '2026-09-25T00:00:00Z'),
            _market('KXATPMATCH-26SEP25PRE-A', 'KXATPMATCH-26SEP25PRE', 'yes', '2026-09-24T18:00:00Z', '2026-09-24T23:51:59Z'),
            _market('KXATPMATCH-26SEP25EDGE-A', 'KXATPMATCH-26SEP25EDGE', 'yes', '2026-09-24T18:00:00Z', '2026-09-24T23:52:00Z'),
            _market('KXATPMATCH-26SEP25YES-A', 'KXATPMATCH-26SEP25YES', 'yes', '2026-09-25T15:00:00Z', '2026-09-25T16:00:00Z'),
            _market('KXATPMATCH-26SEP25NO-B', 'KXATPMATCH-26SEP25NO', 'no', None, '2026-09-25T17:00:00Z'),
            _market('KXATPMATCH-26SEP25EMPTY-C', 'KXATPMATCH-26SEP25EMPTY', '', '2026-09-25T15:00:00Z', '2026-09-25T18:00:00Z'),
        ]
        extra = _market('KXATPMATCH-26SEP25EXTRA-D', 'KXATPMATCH-26SEP25EXTRA', 'yes', '2026-09-25T15:00:00Z', '2026-09-25T19:00:00Z')
        markets_body = json.dumps({'cursor': '', 'markets': markets}).encode()
        events_body = json.dumps({
            'cursor': '',
            'events': [
                {'event_ticker': markets[3]['event_ticker'], 'markets': [markets[3]]},
                {'event_ticker': extra['event_ticker'], 'markets': [extra]},
            ],
        }).encode()
        transport, calls = self._transport(markets_body, ((200, events_body), (200, events_body)))
        empty_before = (ROOT / 'results' / 'EMPTY_RESULTS.json').read_bytes()
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / 'measurement.json'
            started = datetime.now(timezone.utc)
            payload = orchestrator.measure(since, out, transport=transport, sleeper=lambda seconds: None)
            self.assertTrue(out.is_file())
            written = json.loads(out.read_text())
            self.assertEqual(written['settled_join_n'], payload['settled_join_n'])
        self.assertEqual((ROOT / 'results' / 'EMPTY_RESULTS.json').read_bytes(), empty_before)
        self.assertFalse(payload['live_fetch'])
        self.assertEqual(payload['since'], since)
        self.assertEqual(payload['cohort_source'], 'markets_list')
        self.assertEqual(payload['settled_join_n'], 2)
        self.assertEqual(payload['occurrence_match_n'], 1)
        self.assertEqual(payload['fallback_join_n'], 1)
        self.assertEqual(payload['cohort_tickers'], ['KXATPMATCH-26SEP25NO-B', 'KXATPMATCH-26SEP25YES-A'])
        self.assertNotIn(scout_ticker, payload['cohort_tickers'])
        self.assertNotIn('KXATPMATCH-26SEP25PRE-A', payload['cohort_tickers'])
        self.assertNotIn('KXATPMATCH-26SEP25EDGE-A', payload['cohort_tickers'])
        self.assertNotIn('KXATPMATCH-26SEP25EXTRA-D', payload['cohort_tickers'])
        self.assertNotEqual(payload['settled_join_n'], 30)
        reasons = {item['ticker']: item['reason'] for item in payload['excluded']}
        self.assertEqual(reasons[scout_ticker], 'scout_pin')
        self.assertEqual(reasons['KXATPMATCH-26SEP25PRE-A'], 'settled_at_or_before_since')
        self.assertEqual(reasons['KXATPMATCH-26SEP25EDGE-A'], 'settled_at_or_before_since')
        self.assertEqual(reasons['KXATPMATCH-26SEP25EMPTY-C'], 'j0_not_nonempty')
        by_key = {row['key']: row for row in payload['rows']}
        yes = by_key['KXATPMATCH-26SEP25YES-A']
        no = by_key['KXATPMATCH-26SEP25NO-B']
        self.assertEqual(yes['join_source'], 'occurrence_datetime')
        self.assertEqual(yes['occurrence_datetime'], '2026-09-25T15:00:00Z')
        self.assertEqual(no['join_source'], 'expected_expiration_time_fallback')
        self.assertIsNone(no['occurrence_datetime'])
        self.assertEqual(no['expected_expiration_time'], '2026-09-25T12:00:00Z')
        self.assertNotEqual(no['occurrence_datetime'], no['expected_expiration_time'])
        self.assertIsNone(payload['admitted_at'])
        self.assertEqual(payload['admit_ready'], 'pending Clock')
        self.assertIsNone(payload['admit_ready_flag'])
        self.assertIsNone(payload['results'])
        self.assertIsNone(payload['pnl'])
        self.assertFalse(payload['scout_n_copied_into_settled_join_n'])
        self.assertTrue(calls)
        self.assertTrue(all(call.startswith('https://api.elections.kalshi.com/trade-api/v2/') for call in calls))
        logged = payload['http_log'][0]['utc']
        stamp = datetime.strptime(logged, '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=timezone.utc)
        self.assertLess(abs((stamp - started).total_seconds()), 30)

    def test_429_gap_is_recorded_and_not_filled(self):
        kept = _market(
            'KXATPMATCH-26SEP26KEEP-A',
            'KXATPMATCH-26SEP26KEEP',
            'yes',
            '2026-09-26T15:00:00Z',
            '2026-09-26T18:00:00Z',
        )
        hidden = _market(
            'KXATPMATCH-26SEP26HIDDEN-B',
            'KXATPMATCH-26SEP26HIDDEN',
            'no',
            '2026-09-26T15:00:00Z',
            '2026-09-26T19:00:00Z',
        )
        events_page = json.dumps({
            'cursor': 'NEXT',
            'events': [{'event_ticker': kept['event_ticker'], 'markets': [kept]}],
        }).encode()
        too_many = b'{"error":{"code":"too_many_requests","message":"too many requests"}}'
        slept = []

        def transport(url):
            if '/markets?' in url:
                return 429, too_many
            if 'cursor=' in url:
                return 429, too_many
            return 200, events_page

        def sleeper(seconds):
            slept.append(seconds)

        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / 'measurement.json'
            payload = orchestrator.measure(
                '2026-09-24T23:52:00Z',
                out,
                transport=transport,
                sleeper=sleeper,
            )
            raw_dir = Path(tmp) / 'measurement_raw'
            self.assertTrue(raw_dir.is_dir())
            saved = list(raw_dir.glob('*.json'))
            self.assertTrue(saved)
            self.assertTrue(any(path.read_bytes() == too_many for path in saved))
            self.assertTrue((raw_dir / 'http_log.jsonl').is_file())
        self.assertEqual(slept, [10, 20, 40, 10, 20, 40])
        self.assertEqual(payload['cohort_source'], 'events_nested')
        self.assertEqual(payload['settled_join_n'], 1)
        self.assertEqual(payload['occurrence_match_n'], 1)
        self.assertEqual(payload['fallback_join_n'], 0)
        self.assertEqual(payload['cohort_tickers'], ['KXATPMATCH-26SEP26KEEP-A'])
        self.assertNotIn(hidden['ticker'], payload['cohort_tickers'])
        self.assertEqual(len(payload['gaps']), 2)
        for gap in payload['gaps']:
            self.assertEqual(gap['http'], 429)
            self.assertEqual(gap['attempts'], 4)
            self.assertEqual(gap['backoffs_s'], [10, 20, 40])
            self.assertFalse(gap['filled'])
            self.assertFalse(gap['markets_invented'])
        self.assertEqual({gap['kind'] for gap in payload['gaps']}, {'markets', 'events'})
        self.assertFalse(payload['list_429_backfilled'])
        self.assertFalse(payload['events_page2_backfilled'])
        self.assertFalse(payload['markets_invented'])
        self.assertIsNone(payload['admitted_at'])
        self.assertEqual(payload['admit_ready'], 'pending Clock')

    def test_get_only_enforcement(self):
        def boom(url):
            raise AssertionError(url)

        with self.assertRaises(orchestrator.LiveOrdersForbidden):
            orchestrator.public_exchange(
                'POST',
                'https://api.elections.kalshi.com/trade-api/v2/orders',
                boom,
            )
        with self.assertRaises(orchestrator.LiveOrdersForbidden):
            orchestrator.public_exchange(
                'GET',
                'https://example.invalid/trade-api/v2/markets',
                boom,
            )
        with self.assertRaises(orchestrator.LiveOrdersForbidden):
            orchestrator.assert_public_get('PUT')
        self.assertIsNone(orchestrator.assert_public_get('GET'))
        with self.assertRaises(orchestrator.ScorecardPromotionRefused):
            orchestrator.measure(
                '2026-09-24T23:52:00Z',
                ROOT / 'results' / 'live.json',
                transport=boom,
                sleeper=lambda seconds: None,
            )


if __name__ == '__main__':
    unittest.main()
