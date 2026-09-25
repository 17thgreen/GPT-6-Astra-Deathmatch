"""Stub-transport checks for the ATP-RJ measure hardening. No network."""
import hashlib
import inspect
import json
import sqlite3
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

import orchestrator

SINCE = '2026-09-24T23:52:00Z'
MIN_SETTLED_TS = 1790293920
MIN_CLOSE_TS = MIN_SETTLED_TS - 172800
PHASE_A = datetime(2026, 9, 25, 12, 0, tzinfo=timezone.utc)
EXACT_429_FIELDS = {
    'ts_utc',
    'poller',
    'path',
    'status',
    'retry_after',
    'spacing_now_s',
    'cooldown_s',
}


def _market(ticker, event, result, occurrence, settlement, status='finalized', close_time=None):
    row = {
        'ticker': ticker,
        'event_ticker': event,
        'status': status,
        'result': result,
        'occurrence_datetime': occurrence,
        'expected_expiration_time': '2026-09-25T12:00:00Z',
        'settlement_ts': settlement,
    }
    if close_time is not None:
        row['close_time'] = close_time
    return row


def _grant(**extra):
    payload = {
        'seat': 'Collector',
        'poller': 'atp_rj_measure',
        'total_rpm_max': 100,
        'list_endpoint_rpm_max': 100,
        'min_spacing_s': 1,
    }
    payload.update(extra)
    return payload


class Clock:
    def __init__(self, moment):
        self.now = moment
        self.sleeps = []

    def __call__(self):
        return self.now

    def sleep(self, seconds):
        self.sleeps.append(seconds)
        self.now = self.now + timedelta(seconds=seconds)


def _empty_capture(path):
    connection = sqlite3.connect(path)
    connection.execute(
        'CREATE TABLE responses (id INTEGER PRIMARY KEY, ok INTEGER, payload TEXT, received REAL)'
    )
    connection.commit()
    connection.close()
    return path


def _insert_429(path, received, error='HTTPError 429'):
    connection = sqlite3.connect(path)
    payload = json.dumps({'attempts': [{'error': error}]})
    connection.execute(
        'INSERT INTO responses (ok, payload, received) VALUES (0, ?, ?)',
        (payload, received),
    )
    connection.commit()
    connection.close()


def _limiter(clock, root, grant=None, audit_slice=False, phase_b_approval=None, capture=True):
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)
    db = None
    if capture:
        db = _empty_capture(root / 'capture.sqlite')
    return orchestrator.CollectorBudgetLimiter(
        grant if grant is not None else _grant(),
        clock,
        clock.sleep,
        raw_dir=Path(root) / 'raw',
        recorder_capture=db,
        flag_dir=root,
        audit_slice=audit_slice,
        phase_b_approval=phase_b_approval,
    )


class FilterTests(unittest.TestCase):
    def test_markets_url_has_min_settled_ts_and_no_min_close_ts(self):
        calls = []

        def transport(url):
            calls.append(url)
            body = json.dumps({'cursor': '', 'markets': []}).encode()
            return 200, body

        with tempfile.TemporaryDirectory() as tmp:
            orchestrator.measure(SINCE, Path(tmp) / 'out.json', transport=transport, sleeper=lambda seconds: None)
        self.assertEqual(len(calls), 1)
        self.assertIn('/markets?', calls[0])
        self.assertIn(f'min_settled_ts={MIN_SETTLED_TS}', calls[0])
        self.assertNotIn('min_close_ts', calls[0])
        self.assertNotIn('/events?', calls[0])

    def test_events_called_only_on_markets_gap_with_min_close_ts_48h_lookback(self):
        success_calls = []

        def success(url):
            success_calls.append(url)
            return 200, json.dumps({'cursor': '', 'markets': []}).encode()

        with tempfile.TemporaryDirectory() as tmp:
            orchestrator.measure(SINCE, Path(tmp) / 'ok.json', transport=success, sleeper=lambda seconds: None)
        self.assertTrue(all('/events?' not in url for url in success_calls))

        gap_calls = []

        def gap(url):
            gap_calls.append(url)
            if '/markets?' in url:
                return 429, b'{}'
            return 200, json.dumps({'cursor': '', 'events': []}).encode()

        with tempfile.TemporaryDirectory() as tmp:
            orchestrator.measure(SINCE, Path(tmp) / 'gap.json', transport=gap, sleeper=lambda seconds: None)
        event_urls = [url for url in gap_calls if '/events?' in url]
        market_urls = [url for url in gap_calls if '/markets?' in url]
        self.assertTrue(market_urls)
        self.assertTrue(event_urls)
        self.assertLess(gap_calls.index(market_urls[0]), gap_calls.index(event_urls[0]))
        self.assertTrue(all(f'min_close_ts={MIN_CLOSE_TS}' in url for url in event_urls))
        self.assertTrue(all('min_settled_ts' not in url for url in event_urls))
        self.assertEqual(MIN_CLOSE_TS, MIN_SETTLED_TS - 172800)

    def test_server_filter_ignored_detected_client_since_gate_still_authoritative(self):
        early = _market(
            'KXATPMATCH-26SEP25EARLY-A', 'KXATPMATCH-26SEP25EARLY', 'yes',
            '2026-09-24T18:00:00Z', '2026-09-24T23:00:00Z',
        )
        exact = _market(
            'KXATPMATCH-26SEP25EXACT-A', 'KXATPMATCH-26SEP25EXACT', 'yes',
            '2026-09-24T18:00:00Z', SINCE,
        )
        kept = _market(
            'KXATPMATCH-26SEP25KEEP-A', 'KXATPMATCH-26SEP25KEEP', 'yes',
            '2026-09-25T15:00:00Z', '2026-09-25T16:00:00Z',
        )

        def transport(url):
            self.assertIn(f'min_settled_ts={MIN_SETTLED_TS}', url)
            body = json.dumps({'cursor': '', 'markets': [early, exact, kept]}).encode()
            return 200, body

        with tempfile.TemporaryDirectory() as tmp:
            payload = orchestrator.measure(
                SINCE, Path(tmp) / 'out.json', transport=transport, sleeper=lambda seconds: None,
            )
        observed = payload['pull_status']['markets']['server_filter']
        self.assertEqual(observed['param'], 'min_settled_ts')
        self.assertEqual(observed['value'], MIN_SETTLED_TS)
        self.assertEqual(observed['observed'], 'OBSERVED_IGNORED')
        self.assertEqual(payload['settled_join_n'], 1)
        self.assertEqual(payload['cohort_tickers'], ['KXATPMATCH-26SEP25KEEP-A'])
        reasons = {item['ticker']: item['reason'] for item in payload['excluded']}
        self.assertEqual(reasons['KXATPMATCH-26SEP25EARLY-A'], 'settled_at_or_before_since')
        self.assertEqual(reasons['KXATPMATCH-26SEP25EXACT-A'], 'settled_at_or_before_since')
        self.assertEqual(payload['cohort_completeness'], 'COMPLETE')
        self.assertFalse(payload['zero_with_gaps'])

    def test_filter_400_no_unfiltered_full_history_resweep(self):
        calls = []
        kept = _market(
            'KXATPMATCH-26SEP25KEEP-A', 'KXATPMATCH-26SEP25KEEP', 'yes',
            '2026-09-25T15:00:00Z', '2026-09-25T16:00:00Z',
            close_time='2026-09-24T22:00:00Z',
        )

        def transport(url):
            calls.append(url)
            if '/markets?' in url:
                self.assertIn(f'min_settled_ts={MIN_SETTLED_TS}', url)
                self.assertNotIn('min_close_ts', url)
                return 400, b'{"error":"bad_filter"}'
            self.assertIn(f'min_close_ts={MIN_CLOSE_TS}', url)
            self.assertNotIn('min_settled_ts', url)
            body = json.dumps({
                'cursor': '',
                'events': [{'event_ticker': kept['event_ticker'], 'markets': [kept]}],
            }).encode()
            return 200, body

        with tempfile.TemporaryDirectory() as tmp:
            payload = orchestrator.measure(
                SINCE, Path(tmp) / 'out.json', transport=transport, sleeper=lambda seconds: None,
            )
        market_urls = [url for url in calls if '/markets?' in url]
        self.assertEqual(len(market_urls), 1)
        self.assertTrue(all('min_settled_ts=' in url for url in market_urls))
        self.assertFalse(any('min_settled_ts' not in url and '/markets?' in url for url in calls))
        self.assertEqual(payload['pull_status']['markets']['server_filter']['observed'], 'REJECTED_400')
        self.assertEqual(payload['pull_status']['markets']['last_http'], 400)
        self.assertEqual(payload['cohort_source'], 'events_nested')
        self.assertEqual(payload['counts_label'], 'INCOMPLETE')
        self.assertEqual(payload['settled_join_n'], 1)
        self.assertEqual(payload['gaps'][0]['http'], 400)
        self.assertEqual(payload['gaps'][0]['attempts'], 1)


class LimiterTests(unittest.TestCase):
    def test_limiter_phase_a_caps_list_4rpm_total_10rpm_6s_floor(self):
        with tempfile.TemporaryDirectory() as tmp:
            clock = Clock(PHASE_A)
            limiter = _limiter(clock, tmp)
            spacings = []
            for _ in range(4):
                decision = limiter.acquire('/markets')
                self.assertTrue(decision['ok'])
                spacings.append(decision['spacing_now_s'])
                limiter.note_success()
            self.assertEqual(spacings, [15.0, 15.0, 15.0, 15.0])
            self.assertEqual(clock.sleeps, [15.0, 15.0, 15.0])
            self.assertEqual(limiter.phase_at_end, 'A')

            non_list = Clock(PHASE_A)
            other = _limiter(non_list, Path(tmp) / 'nonlist')
            decision = other.acquire('/exchange/status')
            self.assertTrue(decision['ok'])
            self.assertEqual(decision['spacing_now_s'], 6.0)
            other.note_success()
            decision = other.acquire('/exchange/status')
            self.assertEqual(decision['spacing_now_s'], 6.0)
            self.assertEqual(non_list.sleeps, [6.0])

            quiet = Clock(datetime(2026, 9, 25, 22, 53, tzinfo=timezone.utc))
            quiet_limiter = _limiter(quiet, Path(tmp) / 'quiet')
            decision = quiet_limiter.acquire('/markets')
            self.assertTrue(decision['ok'])
            self.assertEqual(quiet.sleeps, [180.0])
            self.assertEqual(quiet.now, datetime(2026, 9, 25, 22, 56, tzinfo=timezone.utc))

            tight = Clock(PHASE_A)
            tight_limiter = _limiter(tight, Path(tmp) / 'tight', grant=_grant(list_endpoint_rpm_max=2))
            tight_limiter.acquire('/markets')
            decision = tight_limiter.acquire('/markets')
            self.assertEqual(decision['spacing_now_s'], 30.0)

    def test_limiter_collector_audit_slice_3rpm_20s(self):
        with tempfile.TemporaryDirectory() as tmp:
            clock = Clock(PHASE_A)
            limiter = _limiter(clock, tmp, grant=_grant(audit_slice=True), audit_slice=True)
            spacings = []
            for _ in range(3):
                decision = limiter.acquire('/markets')
                self.assertTrue(decision['ok'])
                spacings.append(decision['spacing_now_s'])
                limiter.note_success()
            self.assertEqual(spacings, [20.0, 20.0, 20.0])
            self.assertEqual(clock.sleeps, [20.0, 20.0])
            refused = limiter.acquire('/exchange/status')
            self.assertFalse(refused['ok'])
            self.assertEqual(refused['reason'], 'audit_list_only')

            phase_b = Clock(datetime(2026, 9, 27, 16, 30, tzinfo=timezone.utc))
            paused = _limiter(phase_b, Path(tmp) / 'b', grant=_grant(audit_slice=True), audit_slice=True)
            decision = paused.acquire('/markets')
            self.assertFalse(decision['ok'])
            self.assertEqual(decision['reason'], 'audit_phase_b_pause')
            self.assertEqual(phase_b.sleeps, [])

            approved = _limiter(
                Clock(datetime(2026, 9, 27, 16, 30, tzinfo=timezone.utc)),
                Path(tmp) / 'approved',
                grant=_grant(audit_slice=True),
                audit_slice=True,
                phase_b_approval={'seat': 'Conductor', 'approves': 'atp_rj_measure_audit_phase_b'},
            )
            decision = approved.acquire('/markets')
            self.assertTrue(decision['ok'])
            self.assertEqual(decision['spacing_now_s'], 30.0)
            self.assertEqual(decision['phase'], 'B')

    def test_limiter_steps_down_at_2026_09_27T16_30Z(self):
        with tempfile.TemporaryDirectory() as tmp:
            start = datetime(2026, 9, 27, 16, 29, 50, tzinfo=timezone.utc)
            clock = Clock(start)
            limiter = _limiter(clock, tmp)
            first = limiter.acquire('/markets')
            self.assertTrue(first['ok'])
            self.assertEqual(first['phase'], 'A')
            self.assertEqual(first['spacing_now_s'], 15.0)
            limiter.note_success()
            second = limiter.acquire('/markets')
            self.assertTrue(second['ok'])
            self.assertEqual(second['phase'], 'B')
            self.assertEqual(second['spacing_now_s'], 30.0)
            self.assertEqual(clock.now, start + timedelta(seconds=30))
            self.assertEqual(limiter.phase_at_start, 'A')
            self.assertEqual(limiter.phase_at_end, 'B')

            at_switch = Clock(datetime(2026, 9, 27, 16, 30, tzinfo=timezone.utc))
            switched = _limiter(at_switch, Path(tmp) / 'switch')
            decision = switched.acquire('/markets')
            self.assertEqual(decision['phase'], 'B')
            self.assertEqual(decision['spacing_now_s'], 30.0)
            self.assertEqual(at_switch.sleeps, [])

    def test_limiter_refuses_after_2026_10_02T06_15Z_and_without_grant(self):
        with tempfile.TemporaryDirectory() as tmp:
            clock = Clock(datetime(2026, 10, 2, 6, 15, tzinfo=timezone.utc))
            limiter = _limiter(clock, tmp)
            decision = limiter.acquire('/markets')
            self.assertFalse(decision['ok'])
            self.assertEqual(decision['reason'], 'budget_closed')
            self.assertEqual(clock.sleeps, [])
            self.assertEqual(limiter.skipped_budget, 1)

            before = Clock(datetime(2026, 10, 2, 6, 14, 59, tzinfo=timezone.utc))
            still = _limiter(before, Path(tmp) / 'before')
            decision = still.acquire('/markets')
            self.assertTrue(decision['ok'])
            self.assertEqual(decision['phase'], 'B')

            def explode(url):
                raise AssertionError(url)

            original = orchestrator.live_public_get
            orchestrator.live_public_get = explode
            try:
                out = Path(tmp) / 'missing.json'
                payload = orchestrator.measure(SINCE, out, transport=None, sleeper=explode)
            finally:
                orchestrator.live_public_get = original
            self.assertEqual(payload['stop_reason'], 'BUDGET_GRANT_MISSING')
            self.assertEqual(payload['cohort_completeness'], 'INCOMPLETE')
            self.assertEqual(payload['counts_label'], 'INCOMPLETE')
            self.assertTrue(payload['zero_with_gaps'])
            self.assertEqual(payload['settled_join_n'], 0)
            self.assertEqual(payload['http_log'], [])
            self.assertEqual(payload['gaps'][0]['reason'], 'BUDGET_GRANT_MISSING')
            self.assertIsNone(payload['results'])
            self.assertIsNone(payload['pnl'])
            self.assertIsNone(payload['admitted_at'])
            self.assertTrue(out.is_file())
            with self.assertRaises(orchestrator.BudgetGrantMissing):
                orchestrator.CollectorBudgetLimiter(None, clock, clock.sleep)

    def test_nfl_tripwire_flag_or_recorder_429_forces_phase_b_unreadable_assumes_b(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            flagged_dir = root / 'flag'
            flagged_dir.mkdir()
            (flagged_dir / 'FORCE_PHASE_B').write_text('1')
            flagged = _limiter(Clock(PHASE_A), flagged_dir)
            decision = flagged.acquire('/markets')
            self.assertTrue(flagged.forced_phase_b)
            self.assertEqual(flagged.force_reason, 'FORCE_PHASE_B')
            self.assertEqual(decision['phase'], 'B')
            self.assertEqual(decision['spacing_now_s'], 30.0)

            fresh = root / 'fresh'
            fresh.mkdir()
            seen = _limiter(Clock(PHASE_A), fresh)
            self.assertFalse(seen.forced_phase_b)
            _insert_429(seen.recorder_capture, seen.run_started_unix + 1)
            decision = seen.acquire('/markets')
            self.assertTrue(seen.forced_phase_b)
            self.assertEqual(seen.force_reason, 'recorder_429')
            self.assertEqual(decision['spacing_now_s'], 30.0)

            old = root / 'old'
            old.mkdir()
            capture = _empty_capture(old / 'capture.sqlite')
            _insert_429(capture, PHASE_A.timestamp() - 100)
            prior = orchestrator.CollectorBudgetLimiter(
                _grant(), Clock(PHASE_A), Clock(PHASE_A).sleep,
                raw_dir=old / 'raw', recorder_capture=capture, flag_dir=old,
            )
            decision = prior.acquire('/markets')
            self.assertFalse(prior.forced_phase_b)
            self.assertEqual(decision['phase'], 'A')
            self.assertEqual(decision['spacing_now_s'], 15.0)

            missing = orchestrator.CollectorBudgetLimiter(
                _grant(), Clock(PHASE_A), Clock(PHASE_A).sleep,
                raw_dir=root / 'missing-raw', recorder_capture=root / 'no-such.sqlite', flag_dir=root / 'missing',
            )
            decision = missing.acquire('/markets')
            self.assertTrue(missing.forced_phase_b)
            self.assertEqual(missing.force_reason, 'unreadable')
            self.assertEqual(decision['phase'], 'B')
            self.assertEqual(decision['spacing_now_s'], 30.0)

            before = (Path(seen.recorder_capture)).read_bytes()
            seen.acquire('/series')
            self.assertEqual(Path(seen.recorder_capture).read_bytes(), before)

    def test_429_one_retry_cooldown_30_60_120_240_cap600_penalty_storm_pause(self):
        with tempfile.TemporaryDirectory() as tmp:
            clock = Clock(PHASE_A)
            limiter = _limiter(clock, tmp)
            cooldowns = []
            for _ in range(7):
                decision = limiter.acquire('/markets')
                self.assertTrue(decision['ok'])
                cooldowns.append(limiter.note_429('/markets', None, decision['spacing_now_s']))
            self.assertEqual(cooldowns, [30, 60, 120, 240, 480, 600, 600])
            self.assertTrue(all(value <= 600 for value in cooldowns))
            self.assertIn(600.0, clock.sleeps)
            self.assertGreaterEqual(limiter.storm_pauses, 1)
            self.assertTrue((Path(tmp) / 'raw' / 'pause_429_storm.jsonl').is_file())
            storm = json.loads((Path(tmp) / 'raw' / 'pause_429_storm.jsonl').read_text().splitlines()[0])
            self.assertEqual(storm['event'], 'PAUSE_429_STORM')
            self.assertGreaterEqual(storm['counts'], 3)
            retry = limiter.acquire('/markets')
            self.assertEqual(retry['spacing_now_s'], 17.0)

            reset_clock = Clock(PHASE_A)
            reset = _limiter(reset_clock, Path(tmp) / 'reset')
            first = reset.acquire('/markets')
            self.assertEqual(reset.note_429('/markets', 90, first['spacing_now_s']), 90)
            nxt = reset.acquire('/markets')
            self.assertEqual(reset_clock.sleeps, [90.0])
            reset.note_success()
            reset.acquire('/markets')
            self.assertEqual(reset.note_429('/markets', None, nxt['spacing_now_s']), 30)

            calls = {'markets': 0}

            def transport(url):
                if '/markets?' in url:
                    calls['markets'] += 1
                    return 429, b'{}'
                return 429, b'{}'

            measure_clock = Clock(PHASE_A)
            measure_limiter = _limiter(measure_clock, Path(tmp) / 'measure')
            payload = orchestrator.measure(
                SINCE,
                Path(tmp) / 'measure.json',
                transport=transport,
                sleeper=measure_clock.sleep,
                limiter=measure_limiter,
                clock=measure_clock,
            )
            self.assertTrue(all(gap['attempts'] <= 2 for gap in payload['gaps']))
            self.assertTrue(all(gap['attempts'] == 2 for gap in payload['gaps']))
            self.assertLess(calls['markets'], 4)
            self.assertEqual(payload['rate_policy'], 'collector_budget_2026-09-24')
            self.assertFalse(any(gap.get('filled') for gap in payload['gaps']))

    def test_429_jsonl_fields_exact_and_hourly_rollup(self):
        kept = _market(
            'KXATPMATCH-26SEP25KEEP-A', 'KXATPMATCH-26SEP25KEEP', 'yes',
            '2026-09-25T15:00:00Z', '2026-09-25T16:00:00Z',
        )
        state = {'n': 0}

        def transport(url):
            state['n'] += 1
            if state['n'] == 1:
                return 429, b'{}', {'Retry-After': '7'}
            return 200, json.dumps({'cursor': '', 'markets': [kept]}).encode()

        with tempfile.TemporaryDirectory() as tmp:
            clock = Clock(PHASE_A)
            limiter = _limiter(clock, tmp)
            out = Path(tmp) / 'measurement.json'
            payload = orchestrator.measure(
                SINCE, out, transport=transport, sleeper=clock.sleep, limiter=limiter, clock=clock,
            )
            raw = Path(tmp) / 'measurement_raw'
            lines = (raw / 'http_429.jsonl').read_text().splitlines()
            self.assertEqual(len(lines), 1)
            record = json.loads(lines[0])
            self.assertEqual(set(record), EXACT_429_FIELDS)
            self.assertEqual(record['poller'], 'atp_rj_measure')
            self.assertEqual(record['path'], '/markets')
            self.assertEqual(record['status'], 429)
            self.assertEqual(record['retry_after'], 7)
            self.assertEqual(record['cooldown_s'], 7)
            self.assertEqual(record['spacing_now_s'], 15.0)
            self.assertTrue(record['ts_utc'].endswith('Z'))
            hourly = json.loads((raw / 'hourly.json').read_text())
            self.assertEqual(hourly['poller'], 'atp_rj_measure')
            self.assertEqual(hourly['hours'][0]['requests'], 2)
            self.assertEqual(hourly['hours'][0]['ok'], 1)
            self.assertEqual(hourly['hours'][0]['http_429'], 1)
            self.assertTrue((raw / 'http_log.jsonl').is_file())
            self.assertEqual(payload['rate_policy'], 'collector_budget_2026-09-24')


class LabelTests(unittest.TestCase):
    def test_partial_events_after_markets_fail_is_PARTIAL_counts_INCOMPLETE(self):
        kept = _market(
            'KXATPMATCH-26SEP26KEEP-A', 'KXATPMATCH-26SEP26KEEP', 'yes',
            '2026-09-26T15:00:00Z', '2026-09-26T18:00:00Z',
            close_time='2026-09-26T12:00:00Z',
        )

        def transport(url):
            if '/markets?' in url:
                return 429, b'{}'
            if 'cursor=' in url:
                return 429, b'{}'
            body = json.dumps({
                'cursor': 'NEXT',
                'events': [{'event_ticker': kept['event_ticker'], 'markets': [kept]}],
            }).encode()
            return 200, body

        with tempfile.TemporaryDirectory() as tmp:
            payload = orchestrator.measure(
                SINCE, Path(tmp) / 'out.json', transport=transport, sleeper=lambda seconds: None,
            )
        self.assertEqual(payload['cohort_source'], 'events_nested')
        self.assertEqual(payload['cohort_completeness'], 'PARTIAL')
        self.assertEqual(payload['cohort_source_qualified'], 'events_nested:PARTIAL')
        self.assertEqual(payload['counts_label'], 'INCOMPLETE')
        self.assertTrue(payload['counts_are_lower_bounds'])
        self.assertFalse(payload['zero_with_gaps'])
        self.assertEqual(payload['settled_join_n'], 1)
        self.assertEqual(payload['pull_status']['markets']['status'], 'FAILED')
        self.assertEqual(payload['pull_status']['events']['status'], 'PARTIAL')
        self.assertEqual(payload['pull_status']['events']['pages_ok'], 1)
        self.assertEqual(payload['rate_policy'], 'legacy_stub_unit_only')

    def test_zero_with_gaps_is_INCOMPLETE_not_zero(self):
        def transport(url):
            return 429, b'{}'

        with tempfile.TemporaryDirectory() as tmp:
            payload = orchestrator.measure(
                SINCE, Path(tmp) / 'out.json', transport=transport, sleeper=lambda seconds: None,
            )
        self.assertEqual(payload['settled_join_n'], 0)
        self.assertEqual(payload['occurrence_match_n'], 0)
        self.assertEqual(payload['fallback_join_n'], 0)
        self.assertTrue(payload['zero_with_gaps'])
        self.assertEqual(payload['cohort_completeness'], 'INCOMPLETE')
        self.assertEqual(payload['counts_label'], 'INCOMPLETE')
        self.assertTrue(payload['counts_are_lower_bounds'])
        self.assertNotEqual(payload['counts_label'], 'COMPLETE')
        self.assertTrue(payload['gaps'])
        self.assertIsNone(payload['results'])
        self.assertIsNone(payload['pnl'])

    def test_complete_single_endpoint_pull_is_COMPLETE(self):
        kept = _market(
            'KXATPMATCH-26SEP25KEEP-A', 'KXATPMATCH-26SEP25KEEP', 'yes',
            '2026-09-25T15:00:00Z', '2026-09-25T16:00:00Z',
        )
        calls = []

        def transport(url):
            calls.append(url)
            return 200, json.dumps({'cursor': '', 'markets': [kept]}).encode()

        with tempfile.TemporaryDirectory() as tmp:
            payload = orchestrator.measure(
                SINCE, Path(tmp) / 'out.json', transport=transport, sleeper=lambda seconds: None,
            )
        self.assertTrue(all('/events?' not in url for url in calls))
        self.assertEqual(payload['cohort_source'], 'markets_list')
        self.assertEqual(payload['cohort_completeness'], 'COMPLETE')
        self.assertEqual(payload['cohort_source_qualified'], 'markets_list:COMPLETE')
        self.assertEqual(payload['counts_label'], 'COMPLETE')
        self.assertFalse(payload['counts_are_lower_bounds'])
        self.assertFalse(payload['zero_with_gaps'])
        self.assertEqual(payload['settled_join_n'], 1)
        self.assertEqual(payload['pull_status']['markets']['status'], 'COMPLETE')
        self.assertEqual(payload['pull_status']['markets']['server_filter']['observed'], 'OBSERVED_HONORED')
        self.assertEqual(payload['pull_status']['events']['status'], 'NOT_REQUESTED')
        self.assertEqual(payload['pull_status']['events']['server_filter']['observed'], 'NOT_APPLIED')
        self.assertEqual(payload['gaps'], [])

        def empty(url):
            return 200, json.dumps({'cursor': '', 'markets': []}).encode()

        with tempfile.TemporaryDirectory() as tmp:
            payload = orchestrator.measure(
                SINCE, Path(tmp) / 'empty.json', transport=empty, sleeper=lambda seconds: None,
            )
        self.assertEqual(payload['settled_join_n'], 0)
        self.assertFalse(payload['zero_with_gaps'])
        self.assertEqual(payload['cohort_completeness'], 'COMPLETE')
        self.assertEqual(payload['counts_label'], 'COMPLETE')
        self.assertEqual(payload['pull_status']['markets']['server_filter']['observed'], 'UNOBSERVED')

    def test_join_rows_and_counts_identical_to_e8770f1e_fixture(self):
        scout_ticker = 'KXATPMATCH-26SEP24HARKOV-HAR'
        markets = [
            _market(scout_ticker, 'KXATPMATCH-26SEP24HARKOV', 'yes', '2026-09-24T10:20:00Z', '2026-09-25T00:00:00Z'),
            _market('KXATPMATCH-26SEP25PRE-A', 'KXATPMATCH-26SEP25PRE', 'yes', '2026-09-24T18:00:00Z', '2026-09-24T23:51:59Z'),
            _market('KXATPMATCH-26SEP25EDGE-A', 'KXATPMATCH-26SEP25EDGE', 'yes', '2026-09-24T18:00:00Z', '2026-09-24T23:52:00Z'),
            _market('KXATPMATCH-26SEP25YES-A', 'KXATPMATCH-26SEP25YES', 'yes', '2026-09-25T15:00:00Z', '2026-09-25T16:00:00Z'),
            _market('KXATPMATCH-26SEP25NO-B', 'KXATPMATCH-26SEP25NO', 'no', None, '2026-09-25T17:00:00Z'),
            _market('KXATPMATCH-26SEP25EMPTY-C', 'KXATPMATCH-26SEP25EMPTY', '', '2026-09-25T15:00:00Z', '2026-09-25T18:00:00Z'),
        ]

        def transport(url):
            self.assertIn('/markets?', url)
            self.assertNotIn('/events?', url)
            return 200, json.dumps({'cursor': '', 'markets': markets}).encode()

        with tempfile.TemporaryDirectory() as tmp:
            payload = orchestrator.measure(
                SINCE, Path(tmp) / 'out.json', transport=transport, sleeper=lambda seconds: None,
            )
        self.assertEqual(payload['cohort_source'], 'markets_list')
        self.assertEqual(payload['settled_join_n'], 2)
        self.assertEqual(payload['occurrence_match_n'], 1)
        self.assertEqual(payload['fallback_join_n'], 1)
        self.assertEqual(payload['cohort_tickers'], ['KXATPMATCH-26SEP25NO-B', 'KXATPMATCH-26SEP25YES-A'])
        by_key = {row['key']: row for row in payload['rows']}
        yes = by_key['KXATPMATCH-26SEP25YES-A']
        no = by_key['KXATPMATCH-26SEP25NO-B']
        self.assertEqual(yes['join_source'], 'occurrence_datetime')
        self.assertEqual(yes['occurrence_datetime'], '2026-09-25T15:00:00Z')
        self.assertEqual(no['join_source'], 'expected_expiration_time_fallback')
        self.assertIsNone(no['occurrence_datetime'])
        self.assertEqual(no['expected_expiration_time'], '2026-09-25T12:00:00Z')
        self.assertNotEqual(no['occurrence_datetime'], no['expected_expiration_time'])
        reasons = {item['ticker']: item['reason'] for item in payload['excluded']}
        self.assertEqual(reasons[scout_ticker], 'scout_pin')
        self.assertEqual(reasons['KXATPMATCH-26SEP25PRE-A'], 'settled_at_or_before_since')
        self.assertEqual(reasons['KXATPMATCH-26SEP25EDGE-A'], 'settled_at_or_before_since')
        self.assertEqual(reasons['KXATPMATCH-26SEP25EMPTY-C'], 'j0_not_nonempty')
        self.assertIsNone(payload['admitted_at'])
        self.assertIsNone(payload['results'])
        self.assertIsNone(payload['pnl'])

    def test_join_function_sources_match_pinned_sha256(self):
        for name, expected in orchestrator.JOIN_FUNCTION_SHA256.items():
            source = inspect.getsource(getattr(orchestrator, name)).rstrip('\n')
            digest = hashlib.sha256(source.encode()).hexdigest()
            self.assertEqual(digest, expected, name)
        pinned = (
            orchestrator.SCOUT_PATH.read_bytes(),
        )
        self.assertEqual(hashlib.sha256(pinned[0]).hexdigest(), orchestrator.SCOUT_REGET_SHA256)

    def test_legacy_stub_policy_refused_on_live_fetch(self):
        def explode(url):
            raise AssertionError(url)

        original = orchestrator.live_public_get
        orchestrator.live_public_get = explode
        try:
            with tempfile.TemporaryDirectory() as tmp:
                with self.assertRaises(orchestrator.LegacyStubLiveRefused):
                    orchestrator.measure(
                        SINCE,
                        Path(tmp) / 'out.json',
                        transport=None,
                        rate_policy='legacy_stub_unit_only',
                        sleeper=explode,
                    )
                payload = orchestrator.measure(
                    SINCE,
                    Path(tmp) / 'stub.json',
                    transport=lambda url: (200, json.dumps({'cursor': '', 'markets': []}).encode()),
                    sleeper=lambda seconds: None,
                )
        finally:
            orchestrator.live_public_get = original
        self.assertEqual(payload['rate_policy'], 'legacy_stub_unit_only')
        self.assertFalse(payload['live_fetch'])


if __name__ == '__main__':
    unittest.main()
