"""Unit pins for the Q6S5 game-phase settled-tape path.

Schedule parsing, phase boundaries, exclusions, and refuse checks.
Synthetic rows exercise the algebra. The pinned tape is counted, not
scored. results and pnl stay null.
"""
import inspect
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from datetime import timedelta
from decimal import Decimal
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT.parent
sys.path.insert(0, str(ROOT))

import orchestrator


TICKER = 'KXMLBSPREAD-26SEP242140HOUATH-ATH2'
EVENT = 'KXMLBSPREAD-26SEP242140HOUATH'
RULES = (
    'more than 1.5 runs in the Houston vs A\'s professional baseball game '
    'originally scheduled for Sep 24, 2026 at 9:40 PM EDT, then the market '
    'resolves to Yes.'
)
START = '2026-09-25T01:40:00Z'
CLOSE = '2026-09-25T04:30:17Z'


def _market(**overrides):
    body = {
        'ticker': TICKER,
        'event_ticker': EVENT,
        'status': 'finalized',
        'result': 'no',
        'rules_primary': RULES,
        'close_time': CLOSE,
        'settlement_ts': '2026-09-25T04:32:18Z',
        'occurrence_datetime': '2026-09-25T04:40:00Z',
        'expected_expiration_time': '2026-09-25T04:40:00Z',
    }
    body.update(overrides)
    return {'market': body}


def _trade(**overrides):
    row = {
        'ticker': TICKER,
        'created_time': '2026-09-25T02:30:00Z',
        'is_block_trade': False,
        'taker_outcome_side': 'yes',
        'taker_side': 'yes',
        'taker_book_side': 'bid',
        'yes_price_dollars': '0.4000',
        'no_price_dollars': '0.6000',
        'count_fp': '1.00',
    }
    row.update(overrides)
    return row


def _obs(arm, created, price, outcome, event, ticker, quantity='1'):
    return {
        'arm': arm,
        'band_id': 'b04' if Decimal(price) == Decimal('0.40') else 'b01',
        'p_taker': Decimal(price),
        'q': Decimal(quantity),
        'y_s': outcome,
        'event': event,
        'ticker': ticker,
        'created_time': created,
        'scheduled_start': START,
        'close_time': '2026-09-25T05:00:00Z',
        'first_pitch_source': 'SCHEDULED_START_PROXY',
    }


class PinTests(unittest.TestCase):
    def test_authority_hashes_and_manifest(self):
        digest = orchestrator.digest_status()
        self.assertIs(digest['digest_all_match_claimed'], True)
        self.assertEqual(digest['missing'], [])
        self.assertEqual(digest['mismatch'], [])
        self.assertIsNone(digest['results'])
        self.assertIsNone(digest['pnl'])
        self.assertEqual(digest['family_size'], 4)
        self.assertEqual(digest['first_pitch_source'], 'SCHEDULED_START_PROXY')
        self.assertEqual(digest['evidence_class'], 'IN_SAMPLE_DEV')
        for item in digest['absent_not_invented']:
            self.assertIs(item['present'], False)
            self.assertIs(item['invented'], False)
        self.assertFalse(orchestrator.GOVERNANCE_PACKET.exists())
        self.assertFalse(orchestrator.CAPTURE_SQLITE.exists())
        authority = json.loads(orchestrator.AUTHORITY.read_text(encoding='utf-8'))
        self.assertIs(authority['digest_all_match_claimed'], True)
        self.assertEqual(authority['accept_sha256'], orchestrator.ACCEPT_SHA256)
        self.assertEqual(authority['freeze_sha256'], orchestrator.FREEZE_SHA256)
        self.assertEqual(authority['authentic_bundle_sha256'], orchestrator.BUNDLE_SHA256)
        self.assertEqual(authority['band_registry_sha256'], orchestrator.BAND_REGISTRY_SHA256)
        self.assertEqual(authority['packet_manifest_sha256'], orchestrator.PACKET_MANIFEST_SHA256)
        self.assertEqual(authority['in_sample_dev_addendum_sha256'], orchestrator.ADDENDUM_SHA256)
        self.assertEqual(authority['family_size'], 4)
        self.assertIs(authority['hypothesis_generating_only'], True)
        self.assertIs(authority['universe_cap_last_knob'], True)
        self.assertEqual(authority['first_pitch_source'], 'SCHEDULED_START_PROXY')
        self.assertIsNone(authority['results'])
        self.assertIsNone(authority['pnl'])
        completed = subprocess.run(
            ['sha256sum', '-c', 'MANIFEST.sha256'],
            cwd=str(orchestrator.BUNDLE),
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr[-500:])
        self.assertIn('MANIFEST.json: OK', completed.stdout)
        packet = subprocess.run(
            ['sha256sum', '-c', 'MANIFEST.sha256'],
            cwd=str(orchestrator.BUNDLE / orchestrator.PACKET_REL),
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(packet.returncode, 0, packet.stderr[-500:])
        pins_manifest = subprocess.run(
            ['sha256sum', '-c', 'MANIFEST.sha256'],
            cwd=str(orchestrator.PINS),
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(pins_manifest.returncode, 0, pins_manifest.stderr[-500:])
        self.assertIn(orchestrator.ACCEPT_PATH.name + ': OK', pins_manifest.stdout)
        self.assertIn(orchestrator.ADDENDUM_PATH.name + ': OK', pins_manifest.stdout)
        self.assertIn(orchestrator.BUNDLE_TGZ.name + ': OK', pins_manifest.stdout)
        capture_copy = PARENT / 'lab' / 'astra-capture' / 'r3-p3-fl-maker-taker' / 'bands_registry_10c.json'
        self.assertEqual(orchestrator.sha256_file(capture_copy), orchestrator.BAND_REGISTRY_SHA256)
        checked = orchestrator.verify_pins_manifest()
        self.assertEqual(checked['accept']['decision'], 'ACCEPT_FREEZE_IMPLEMENT_GO')
        self.assertEqual(
            checked['ruling']['ruling']['evidence_class'],
            'IN_SAMPLE_DEV',
        )

    def test_sha_mismatch_fails_closed_before_parse(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'broken.json'
            path.write_bytes(b'not-json{')
            with self.assertRaises(orchestrator.ManifestShaMismatch):
                orchestrator.load_pinned_json(path, '0' * 64)
            with self.assertRaises(orchestrator.ManifestShaMismatch):
                orchestrator.assert_pinned_sha(path, '0' * 64)

    def test_closed_manifest_rejects_a_tampered_input(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / 'bundle'
            shutil.copytree(orchestrator.BUNDLE, dest)
            target = dest / orchestrator.SOURCE_PINS_REL
            data = bytearray(target.read_bytes())
            data[0] ^= 0xFF
            target.write_bytes(data)
            with self.assertRaises(orchestrator.ManifestShaMismatch):
                orchestrator.verify_closed_manifest(dest)

    def test_pins_manifest_fails_closed_on_a_tampered_byte(self):
        self.assertEqual(orchestrator.sha256_file(orchestrator.ACCEPT_PATH), orchestrator.ACCEPT_SHA256)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / orchestrator.ACCEPT_PATH.name
            data = bytearray(orchestrator.ACCEPT_PATH.read_bytes())
            data[0] ^= 0xFF
            target.write_bytes(data)
            manifest = root / 'MANIFEST.sha256'
            manifest.write_text(
                '%s  %s\n' % (orchestrator.ACCEPT_SHA256, orchestrator.ACCEPT_PATH.name),
                encoding='utf-8',
            )
            with self.assertRaises(orchestrator.ManifestShaMismatch):
                orchestrator.verify_pins_manifest(manifest)
            with self.assertRaises(orchestrator.ManifestShaMismatch):
                orchestrator.load_pinned_json(target, orchestrator.ACCEPT_SHA256)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / orchestrator.ADDENDUM_PATH.name
            data = bytearray(orchestrator.ADDENDUM_PATH.read_bytes())
            data[-1] ^= 0xFF
            target.write_bytes(data)
            manifest = root / 'MANIFEST.sha256'
            lines = [
                '%s  %s' % (orchestrator.BUNDLE_SHA256, orchestrator.BUNDLE_TGZ.name),
                '%s  %s' % (orchestrator.ACCEPT_SHA256, orchestrator.ACCEPT_PATH.name),
                '%s  %s' % (orchestrator.ADDENDUM_SHA256, orchestrator.ADDENDUM_PATH.name),
            ]
            (root / orchestrator.BUNDLE_TGZ.name).write_bytes(orchestrator.BUNDLE_TGZ.read_bytes())
            (root / orchestrator.ACCEPT_PATH.name).write_bytes(orchestrator.ACCEPT_PATH.read_bytes())
            manifest.write_text('\n'.join(lines) + '\n', encoding='utf-8')
            with self.assertRaises(orchestrator.ManifestShaMismatch):
                orchestrator.verify_pins_manifest(manifest)


class ScheduleTests(unittest.TestCase):
    def test_scheduled_start_parses_and_cross_checks_ticker(self):
        self.assertEqual(orchestrator.scheduled_start_utc(RULES, EVENT), START)
        sd_rules = 'originally scheduled for Sep 24, 2026 at 10:10 PM EDT'
        sd_event = 'KXMLBSPREAD-26SEP242210SDLAD'
        self.assertEqual(
            orchestrator.scheduled_start_utc(sd_rules, sd_event),
            '2026-09-25T02:10:00Z',
        )
        la_rules = 'originally scheduled for Sep 24, 2026 at 9:40 PM EDT'
        self.assertEqual(
            orchestrator.scheduled_start_utc(la_rules, 'KXMLBSPREAD-26SEP242140LAASEA'),
            '2026-09-25T01:40:00Z',
        )
        clocks = orchestrator._load_market_clocks(orchestrator.BUNDLE)
        self.assertEqual(
            {clocks[ticker]['event_ticker']: clocks[ticker]['scheduled_start_utc'] for ticker in clocks},
            orchestrator.DECLARED_STARTS,
        )
        self.assertEqual(orchestrator.FIRST_PITCH_SOURCE, 'SCHEDULED_START_PROXY')

    def test_rules_ticker_mismatch_and_missing_pattern_hard_fail(self):
        with self.assertRaises(orchestrator.ScheduledStartRefused) as mismatch:
            orchestrator.scheduled_start_utc(
                'originally scheduled for Sep 24, 2026 at 9:41 PM EDT',
                EVENT,
            )
        self.assertIn('mismatch', str(mismatch.exception))
        with self.assertRaises(orchestrator.ScheduledStartRefused) as missing:
            orchestrator.scheduled_start_utc('no schedule in this text', EVENT)
        self.assertIn('missing', str(missing.exception))
        with self.assertRaises(orchestrator.ScheduledStartRefused):
            orchestrator.scheduled_start_utc(RULES, 'KXMLBSPREAD-26SEP242141HOUATH')
        with self.assertRaises(orchestrator.ScheduledStartRefused):
            orchestrator.classify_trade(
                _trade(),
                _market(rules_primary='originally scheduled for Sep 24, 2026 at 9:41 PM EDT'),
            )
        with self.assertRaises(orchestrator.ScheduledStartRefused):
            orchestrator.use_occurrence_datetime('2026-09-25T04:40:00Z')
        with self.assertRaises(orchestrator.ScheduledStartRefused):
            orchestrator.use_expected_expiration('2026-09-25T04:40:00Z')

    def test_phase_boundary_at_first_pitch_and_close(self):
        params = list(inspect.signature(orchestrator.assign_phase).parameters)
        self.assertEqual(params, ['created_time', 'scheduled_start', 'close_time'])
        self.assertEqual(orchestrator.assign_phase(START, START, CLOSE), 'Q6S5GP1')
        self.assertEqual(
            orchestrator.assign_phase('2026-09-25T01:39:59.999999Z', START, CLOSE),
            'Q6S5GP0',
        )
        self.assertIsNone(orchestrator.assign_phase(CLOSE, START, CLOSE))
        self.assertEqual(
            orchestrator.assign_phase('2026-09-25T04:30:16.999999Z', START, CLOSE),
            'Q6S5GP1',
        )
        exact = orchestrator.classify_trade(_trade(created_time=START), _market())
        self.assertEqual(exact['row']['arm'], 'Q6S5GP1')
        self.assertEqual(exact['row']['first_pitch_source'], 'SCHEDULED_START_PROXY')
        self.assertEqual(exact['row']['scheduled_start_utc'], START)
        before = orchestrator.classify_trade(
            _trade(created_time='2026-09-25T01:39:59.999999Z'),
            _market(),
        )
        self.assertEqual(before['row']['arm'], 'Q6S5GP0')
        at_close = orchestrator.classify_trade(_trade(created_time=CLOSE), _market())
        self.assertEqual(at_close['reason'], 'post_close')
        self.assertIsNone(at_close['row'])
        shifted = orchestrator.parse_ts(START) + timedelta(minutes=30)
        self.assertEqual(orchestrator.assign_phase(shifted, shifted, CLOSE), 'Q6S5GP1')
        self.assertEqual(
            orchestrator.assign_phase(shifted - timedelta(microseconds=1), shifted, CLOSE),
            'Q6S5GP0',
        )
        self.assertEqual(orchestrator.ARMS, ('Q6S5GP0', 'Q6S5GP1'))

    def test_occurrence_datetime_does_not_assign_the_phase(self):
        got = orchestrator.classify_trade(_trade(created_time=START), _market())
        self.assertEqual(got['row']['scheduled_start_utc'], START)
        self.assertNotEqual(got['row']['scheduled_start_utc'], '2026-09-25T04:40:00Z')
        sneaky = _trade(created_time='2026-09-25T01:00:00Z', scheduled_start_override='2026-09-25T00:00:00Z')
        row = orchestrator.classify_trade(sneaky, _market())
        self.assertEqual(row['row']['arm'], 'Q6S5GP0')
        self.assertEqual(row['row']['scheduled_start_utc'], START)


class ExclusionTests(unittest.TestCase):
    def test_market_without_result_produces_no_row(self):
        for result in (None, '', 'yes '):
            got = orchestrator.classify_trade(_trade(), _market(result=result, status='finalized'))
            self.assertIs(got['included'], False)
            self.assertEqual(got['reason'], 'market_result_not_yes_no')
            self.assertIsNone(got['row'])
            self.assertNotIn('y_s', got)
            self.assertNotIn('result', got)
        active = orchestrator.classify_trade(_trade(), _market(status='active', result='yes'))
        self.assertIsNone(active['row'])

    def test_admit1_window_rejects_trade_and_settlement(self):
        self.assertIs(orchestrator.in_admit1_window('2026-09-27T00:00:00Z'), True)
        self.assertIs(orchestrator.in_admit1_window('2026-09-30T03:59:59Z'), True)
        self.assertIs(orchestrator.in_admit1_window('2026-09-26T23:59:59Z'), False)
        self.assertIs(orchestrator.in_admit1_window('2026-09-30T04:00:00Z'), False)
        with self.assertRaises(orchestrator.Admit1WindowRejected) as trade_ctx:
            orchestrator.classify_trade(
                _trade(created_time='2026-09-27T00:00:00Z'),
                _market(),
            )
        self.assertIn('trades', str(trade_ctx.exception))
        with self.assertRaises(orchestrator.Admit1WindowRejected) as settle_ctx:
            orchestrator.classify_trade(
                _trade(),
                _market(settlement_ts='2026-09-28T00:00:00Z'),
            )
        self.assertIn('settlement', str(settle_ctx.exception))
        with self.assertRaises(orchestrator.Admit1WindowRejected):
            orchestrator.classify_trade(
                _trade(),
                _market(),
                captured_utc='2026-09-29T00:00:00Z',
            )

    def test_post_close_block_conflict_and_price(self):
        post = orchestrator.classify_trade(_trade(created_time=CLOSE), _market())
        self.assertEqual(post['reason'], 'post_close')
        self.assertIsNone(post['row'])
        block = orchestrator.classify_trade(_trade(is_block_trade=True), _market())
        self.assertEqual(block['reason'], 'block')
        self.assertIsNone(block['row'])
        conflict = orchestrator.classify_trade(
            _trade(taker_side='no', taker_outcome_side='yes', taker_book_side='bid'),
            _market(),
        )
        self.assertEqual(conflict['reason'], 'taker_conflict')
        self.assertIsNone(conflict['row'])
        self.assertNotIn('inferred_side', conflict)
        price = orchestrator.classify_trade(
            _trade(yes_price_dollars='0.4000', no_price_dollars='0.5000'),
            _market(),
        )
        self.assertEqual(price['reason'], 'price_inconsistent')
        self.assertIsNone(price['row'])

    def test_lee_ready_backfill_lookahead_capture_orders_and_network_are_refused(self):
        with self.assertRaises(orchestrator.LeeReadyRefused):
            orchestrator.classify_trade(_trade(lee_ready=True), _market())
        with self.assertRaises(orchestrator.LeeReadyRefused):
            orchestrator.infer_lee_ready(_trade())
        with self.assertRaises(orchestrator.LeeReadyRefused):
            orchestrator.classify_trade(_trade(direction_method='Lee-Ready'), _market())
        with self.assertRaises(orchestrator.GapBackfillRefused):
            orchestrator.classify_trade(_trade(backfill=True), _market())
        with self.assertRaises(orchestrator.GapBackfillRefused):
            orchestrator.backfill_gap({'gap': True})
        with self.assertRaises(orchestrator.LookaheadRefused):
            orchestrator.classify_trade(_trade(use_future_print=True), _market())
        with self.assertRaises(orchestrator.LookaheadRefused):
            orchestrator.classify_trade(_trade(use_result_for_phase=True), _market())
        with self.assertRaises(orchestrator.NoInvent):
            orchestrator.classify_trade(_trade(pnl='1'), _market())
        with self.assertRaises(orchestrator.NoInvent):
            orchestrator.classify_trade(_trade(depth='1'), _market())
        with self.assertRaises(orchestrator.NoInvent):
            orchestrator.classify_trade(_trade(invent_settlement='2026-09-25T04:32:18Z'), _market())
        with self.assertRaises(orchestrator.NoInvent):
            orchestrator.classify_trade(_trade(invented_market='KXMLBSPREAD-NEW'), _market())
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'capture.sqlite'
            path.write_bytes(b'not-a-database')
            before = path.read_bytes()
            with self.assertRaises(orchestrator.Admit1CaptureRefused):
                orchestrator.read_admit1_capture(path)
            self.assertEqual(path.read_bytes(), before)
        with self.assertRaises(orchestrator.LiveOrderRefused):
            orchestrator.live_order()
        with self.assertRaises(orchestrator.LiveHttpRefused):
            orchestrator.live_http_get('https://api.elections.kalshi.com/trade-api/v2/markets')
        with self.assertRaises(orchestrator.AdmitPyRefused):
            orchestrator.run_admit_py()
        source = (ROOT / 'orchestrator.py').read_text(encoding='utf-8')
        for banned in (
            'urlopen',
            'import sqlite3',
            'import urllib',
            'import requests',
            'import http.client',
            'import socket',
            'import httpx',
            'api.elections.kalshi.com',
        ):
            self.assertNotIn(banned, source)

    def test_sep25_markets_stay_out_of_scope(self):
        ticker = 'KXMLBSPREAD-26SEP251840PITDET-DET2'
        got = orchestrator.classify_trade(
            _trade(ticker=ticker),
            _market(ticker=ticker, result='yes', status='finalized'),
        )
        self.assertEqual(got['reason'], 'out_of_scope_sep25')
        self.assertIsNone(got['row'])
        self.assertNotIn('result', got)

    def test_rebin_orthogonal_knobs_and_universe_cap_are_refused(self):
        registry = orchestrator.load_band_registry()
        self.assertEqual(orchestrator.assign_registry_band('0.20', registry), 'b02')
        self.assertEqual(orchestrator.assign_registry_band('0.7999999999', registry), 'b07')
        self.assertEqual(orchestrator.assign_registry_band('0.80', registry), 'b08')
        self.assertIs(orchestrator.in_fl1('0.20', registry), True)
        self.assertIs(orchestrator.in_fl1('0.1999999999', registry), False)
        self.assertIs(orchestrator.in_fl1('0.80', registry), False)
        with self.assertRaises(orchestrator.RebinRefused):
            orchestrator.rebin([{'band_id': 'custom'}])
        shifted = json.loads(json.dumps(registry))
        shifted['bands'][2]['lo_inclusive'] = False
        with self.assertRaises(orchestrator.RebinRefused):
            orchestrator.assign_registry_band('0.20', shifted)
        for name in ('analysis_slice', 'fill_model', 'price_band'):
            with self.assertRaises(orchestrator.OrthogonalKnobRefused):
                orchestrator.set_knob(name)
            with self.assertRaises(orchestrator.RetuneRefused):
                orchestrator.retune(name)
        self.assertEqual(orchestrator.set_knob('game_phase'), 'game_phase')
        with self.assertRaises(orchestrator.UniverseCapRefused):
            orchestrator.open_fifth_freeze('fifth')
        with self.assertRaises(orchestrator.KeepRefused):
            orchestrator.claim_keep()
        with self.assertRaises(orchestrator.CacheNotLiveR1P1):
            orchestrator.claim_live_r1p1()
        with self.assertRaises(orchestrator.DualCloudRefused):
            orchestrator.dual_cloud()


class AlgebraTests(unittest.TestCase):
    def _sample(self):
        rows = []
        events = (
            ('KXMLBSPREAD-26SEP242140HOUATH', 'KXMLBSPREAD-26SEP242140HOUATH-ATH2', 'KXMLBSPREAD-26SEP242140HOUATH-HOU2'),
            ('KXMLBSPREAD-26SEP242140LAASEA', 'KXMLBSPREAD-26SEP242140LAASEA-LAA2', 'KXMLBSPREAD-26SEP242140LAASEA-SEA2'),
            ('KXMLBSPREAD-26SEP242210SDLAD', 'KXMLBSPREAD-26SEP242210SDLAD-LAD2', 'KXMLBSPREAD-26SEP242210SDLAD-SD2'),
        )
        for event, left, right in events:
            rows.append(_obs('Q6S5GP0', '2026-09-25T01:00:00Z', '0.40', 0, event, left))
            rows.append(_obs('Q6S5GP1', '2026-09-25T02:30:00Z', '0.40', 1, event, right))
        return rows

    def test_synthetic_deltas_stresses_and_reading_stay_off_the_card(self):
        measured = orchestrator.measure_rows(self._sample())
        self.assertEqual(measured['label'], 'public_counterparty_realized')
        self.assertIsNone(measured['results'])
        self.assertIsNone(measured['pnl'])
        self.assertIsNone(measured['reading'])
        self.assertIs(measured['promote'], False)
        self.assertIs(measured['counts_toward_keep'], False)
        self.assertEqual(measured['verdict_ceiling'], 'ITERATE')
        self.assertEqual(measured['fee_label'], 'CACHE_NOT_R1P1')
        self.assertEqual(measured['family_size'], 4)
        self.assertIs(measured['hypothesis_generating_only'], True)
        self.assertIs(measured['universe_cap_last_knob'], True)
        self.assertEqual(measured['first_pitch_source'], 'SCHEDULED_START_PROXY')
        self.assertEqual(measured['evidence_class'], 'IN_SAMPLE_DEV')
        self.assertEqual(measured['arm_names'], ['Q6S5GP0', 'Q6S5GP1'])
        self.assertNotIn('maker_gross_roi_delta_FL0_minus_FL1', measured)
        gp0 = measured['arms']['Q6S5GP0']['maker_gross_roi']
        gp1 = measured['arms']['Q6S5GP1']['maker_gross_roi']
        self.assertEqual(gp0, Decimal('0.40') / Decimal('0.60'))
        self.assertEqual(gp1, Decimal('-1'))
        self.assertEqual(measured['maker_gross_roi_delta_GP1_minus_GP0'], gp1 - gp0)
        self.assertEqual(
            measured['maker_gross_roi_delta_GP1_minus_GP0_within_FL1'],
            gp1 - gp0,
        )
        self.assertEqual(len(measured['logo']), 3)
        self.assertEqual(measured['loeo'], measured['logo'])
        self.assertEqual(len(measured['lomo']), 6)
        self.assertIs(measured['stress_start_shift_plus_30m']['is_arm'], False)
        self.assertEqual(
            measured['stress_start_shift_plus_30m']['maker_gross_roi_delta_GP1_minus_GP0'],
            gp1 - gp0,
        )
        tick_gp0 = Decimal('0.39') / Decimal('0.61')
        tick_gp1 = Decimal('-0.61') / Decimal('0.61')
        self.assertEqual(
            measured['stress_one_tick_worse']['maker_gross_roi_delta_GP1_minus_GP0'],
            tick_gp1 - tick_gp0,
        )
        self.assertIs(measured['stress_one_tick_worse']['is_arm'], False)
        fee = orchestrator.cache_order_fee('maker', '1', '0.60')
        doubled = orchestrator.cache_order_fee('maker', '1', '0.60', times=2)
        self.assertIsNone(fee['formula_id'])
        self.assertIs(fee['fee_honest'], False)
        self.assertIs(fee['claim_as_live_R1P1'], False)
        self.assertIs(fee['resolved_terms_asserted'], False)
        self.assertEqual(fee['label'], 'CACHE_NOT_R1P1')
        self.assertEqual(doubled['fee'], fee['fee'] * 2)
        self.assertIsNone(fee['pnl'])
        self.assertEqual(
            measured['stress_fees_2x_cache']['label'],
            'CACHE_NOT_R1P1',
        )
        self.assertIs(measured['stress_fees_2x_cache']['fee_honest'], False)
        net0 = (Decimal('1.20') - (fee['fee'] * 3)) / Decimal('1.80')
        net1 = (Decimal('-1.80') - (fee['fee'] * 3)) / Decimal('1.80')
        self.assertEqual(measured['arms']['Q6S5GP0']['maker_net_roi_cache'], net0)
        self.assertEqual(
            measured['stress_fees_2x_cache']['maker_net_roi_cache_delta_GP1_minus_GP0'],
            (Decimal('-1.80') - (doubled['fee'] * 3)) / Decimal('1.80')
            - (Decimal('1.20') - (doubled['fee'] * 3)) / Decimal('1.80'),
        )
        self.assertEqual(net1 - net0, gp1 - gp0)
        reading = orchestrator.reading_rule(
            measured['maker_gross_roi_delta_GP1_minus_GP0'],
            [item['maker_gross_roi_delta_GP1_minus_GP0'] for item in measured['loeo']],
            measured['maker_gross_roi_delta_GP1_minus_GP0_within_FL1'],
        )
        self.assertEqual(reading, 'supports_H1')
        self.assertEqual(orchestrator.verdict_for(reading), 'ITERATE')
        self.assertEqual(
            orchestrator.reading_rule(
                Decimal('1'),
                [Decimal('1'), Decimal('0'), Decimal('-0.1')],
                Decimal('1'),
            ),
            'contradicts_H1',
        )
        self.assertEqual(
            orchestrator.reading_rule(
                Decimal('-1'),
                [Decimal('-1'), Decimal('-1'), Decimal('-1')],
                Decimal('0.5'),
            ),
            'inconclusive_price_confounded',
        )
        self.assertEqual(
            orchestrator.reading_rule(Decimal('1'), [Decimal('1'), Decimal('-1'), None]),
            'inconclusive',
        )
        flip = _obs(
            'Q6S5GP1',
            '2026-09-25T01:50:00Z',
            '0.40',
            1,
            'KXMLBSPREAD-26SEP242140HOUATH',
            'KXMLBSPREAD-26SEP242140HOUATH-HOU2',
        )
        stay = _obs(
            'Q6S5GP0',
            '2026-09-25T01:00:00Z',
            '0.40',
            0,
            'KXMLBSPREAD-26SEP242140HOUATH',
            'KXMLBSPREAD-26SEP242140HOUATH-ATH2',
        )
        shifted = orchestrator.measure_rows([stay, flip])
        self.assertIsNone(
            shifted['stress_start_shift_plus_30m']['maker_gross_roi_delta_GP1_minus_GP0'],
        )
        self.assertIs(shifted['stress_start_shift_plus_30m']['is_arm'], False)
        self.assertEqual(shifted['arm_names'], ['Q6S5GP0', 'Q6S5GP1'])
        card = orchestrator.published_scorecard()
        self.assertIsNone(card['metrics']['maker_gross_roi_delta_GP1_minus_GP0'])
        self.assertIsNone(card['metrics']['stress_start_shift_plus_30m'])
        self.assertIsNone(card['metrics']['stress_fees_2x_cache'])
        self.assertIsNone(card['metrics']['reading'])

    def test_pre_admitted_at_is_strictly_before_the_panel_instant(self):
        market = _market(
            close_time='2026-09-25T06:00:00Z',
            settlement_ts='2026-09-25T06:01:00Z',
        )
        cases = (
            ('2026-09-25T04:37:46Z', True),
            ('2026-09-25T04:37:46.999999Z', True),
            ('2026-09-25T04:37:47Z', False),
            ('2026-09-25T04:37:47.000000Z', False),
            ('2026-09-25T04:37:47.000001Z', False),
            ('2026-09-25T04:37:48Z', False),
        )
        for created, expected in cases:
            self.assertIs(orchestrator.pre_admitted_at(created), expected, created)
            got = orchestrator.classify_trade(_trade(created_time=created), market)
            self.assertIs(got['included'], True, created)
            self.assertIs(got['row']['pre_admitted_at'], expected, created)
            self.assertEqual(got['row']['evidence_class'], 'IN_SAMPLE_DEV')
            self.assertEqual(got['row']['family_size'], 4)
            self.assertEqual(got['row']['first_pitch_source'], 'SCHEDULED_START_PROXY')
            self.assertEqual(got['row']['arm'], 'Q6S5GP1')
            self.assertNotIn('pnl', got['row'])

    def test_lookahead_arm_must_match_the_print_timestamp(self):
        row = _obs(
            'Q6S5GP1',
            '2026-09-25T01:00:00Z',
            '0.40',
            0,
            EVENT,
            TICKER,
        )
        with self.assertRaises(orchestrator.LookaheadRefused):
            orchestrator.measure_rows([row])


class ScorecardTests(unittest.TestCase):
    def test_published_card_stays_null_with_family_and_proxy_labels(self):
        card = orchestrator.published_scorecard()
        hold = orchestrator.examiner_status()
        self.assertEqual(
            orchestrator.sha256_file(orchestrator.EMPTY_RESULTS),
            orchestrator.EMPTY_RESULTS_SHA256,
        )
        self.assertIsNone(card['results'])
        self.assertIsNone(card['pnl'])
        self.assertEqual(card['evidence_class'], 'IN_SAMPLE_DEV')
        self.assertEqual(card['family_size'], 4)
        self.assertEqual(
            card['family_knobs'],
            ['analysis_slice', 'fill_model', 'price_band', 'game_phase'],
        )
        self.assertIs(card['hypothesis_generating_only'], True)
        self.assertIs(card['universe_cap_last_knob'], True)
        self.assertEqual(card['first_pitch_source'], 'SCHEDULED_START_PROXY')
        self.assertIs(card['promote'], False)
        self.assertIs(card['counts_toward_keep'], False)
        self.assertEqual(card['verdict_ceiling'], 'ITERATE')
        for key in orchestrator.NULL_METRIC_KEYS:
            self.assertIsNone(card['metrics'][key], key)
        self.assertEqual(card['metrics']['evidence_class'], 'IN_SAMPLE_DEV')
        stub = card['examiner_scorecard_v1_2']['scorecard']
        self.assertEqual(stub['evidence_class'], 'IN_SAMPLE_DEV')
        self.assertEqual(stub['family_size'], 4)
        self.assertIs(stub['hypothesis_generating_only'], True)
        self.assertIs(stub['universe_cap_last_knob'], True)
        self.assertEqual(stub['first_pitch_source'], 'SCHEDULED_START_PROXY')
        self.assertIsNone(stub['results'])
        self.assertIsNone(stub['pnl'])
        self.assertIsNone(stub['metrics']['maker_gross_roi_delta_GP1_minus_GP0'])
        self.assertIsNone(stub['metrics']['reading'])
        for arm in ('Q6S5GP0', 'Q6S5GP1'):
            self.assertIsNone(card['grid_cells'][arm]['maker_gross_roi'])
            self.assertIsNone(card['grid_cells'][arm]['pre_admitted_at_n'])
            self.assertIsNone(card['grid_cells'][arm]['post_admitted_at_n'])
        self.assertEqual(hold['status'], 'HOLD_PRE_PR')
        self.assertEqual(hold['examiner_path_after_pr'], 'READY_NOT_SCORED')
        self.assertIs(hold['scored'], False)
        self.assertIs(hold['stub_ready'], False)
        self.assertIs(hold['signed_by_examiner'], False)
        self.assertEqual(hold['evidence_class'], 'IN_SAMPLE_DEV')
        self.assertEqual(hold['family_size'], 4)
        self.assertEqual(hold['first_pitch_source'], 'SCHEDULED_START_PROXY')
        self.assertIsNone(hold['results'])
        self.assertIsNone(hold['pnl'])
        with self.assertRaises(orchestrator.ScorecardPromotionRefused):
            orchestrator.write_scorecard({'results': '1', 'pnl': None, 'metrics': {}}, '/tmp/x')
        with self.assertRaises(orchestrator.ScorecardPromotionRefused):
            orchestrator.write_scorecard(
                {
                    'results': None,
                    'pnl': None,
                    'metrics': {'maker_gross_roi_delta_GP1_minus_GP0': '1'},
                },
                '/tmp/x',
            )
        summary = orchestrator.measure_rows([])
        self.assertEqual(summary['evidence_class'], 'IN_SAMPLE_DEV')
        self.assertEqual(summary['family_size'], 4)
        self.assertIsNone(summary['results'])
        self.assertIsNone(summary['pnl'])
        self.assertIsNone(summary['reading'])

    def test_timestamp_only_arm_counts_match_the_freeze(self):
        phases = orchestrator.timestamp_only_phase_counts()
        self.assertEqual(phases['arms']['Q6S5GP0'], 1865)
        self.assertEqual(phases['arms']['Q6S5GP1'], 9852)
        self.assertEqual(phases['post_close'], 6)
        self.assertEqual(phases['evidence_class'], 'IN_SAMPLE_DEV')
        self.assertEqual(phases['family_size'], 4)
        self.assertEqual(phases['first_pitch_source'], 'SCHEDULED_START_PROXY')
        self.assertIs(phases['counts_only'], True)
        self.assertIsNone(phases['results'])
        self.assertIsNone(phases['pnl'])
        self.assertIsNone(phases['maker_gross_roi_delta_GP1_minus_GP0'])
        total_pre = 0
        total_post = 0
        for arm in ('Q6S5GP0', 'Q6S5GP1'):
            block = phases['pre_admitted_at_by_arm'][arm]
            self.assertEqual(set(block), {'pre_admitted_at', 'post_admitted_at'})
            self.assertEqual(block['pre_admitted_at'] + block['post_admitted_at'], phases['arms'][arm])
            total_pre += block['pre_admitted_at']
            total_post += block['post_admitted_at']
        self.assertEqual(total_pre + total_post, 1865 + 9852)
        for ticker, expected in orchestrator.EXPECTED_PHASE_COUNTS.items():
            got = phases['per_market'][ticker]
            self.assertEqual((got['Q6S5GP0'], got['Q6S5GP1'], got['post_close']), expected)
        for forbidden in ('y_s', 'result', 'p_taker', 'maker_gross_roi', 'win_rate'):
            self.assertNotIn(forbidden, phases)
        output = orchestrator.output_row_admission_counts()
        self.assertEqual(output['evidence_class'], 'IN_SAMPLE_DEV')
        self.assertEqual(output['family_size'], 4)
        self.assertEqual(output['first_pitch_source'], 'SCHEDULED_START_PROXY')
        self.assertIs(output['counts_only'], True)
        self.assertIsNone(output['results'])
        self.assertIsNone(output['pnl'])
        self.assertIsNone(output['maker_gross_roi_delta_GP1_minus_GP0'])
        for arm in ('Q6S5GP0', 'Q6S5GP1'):
            block = output['arms'][arm]
            self.assertEqual(
                block['pre_admitted_at'] + block['post_admitted_at'],
                output['included_n'][arm],
            )
            self.assertLessEqual(output['included_n'][arm], phases['arms'][arm])
        self.assertEqual(output['excluded_n']['post_close'], 6)
        accounted = sum(output['included_n'].values()) + sum(output['excluded_n'].values())
        self.assertEqual(accounted, 11723)
        for forbidden in ('y_s', 'result', 'p_taker', 'maker_gross_roi', 'win_rate'):
            self.assertNotIn(forbidden, output)

    def test_conduct_does_not_score(self):
        report = orchestrator.conduct()
        self.assertEqual(report['n_prints_pinned'], 11723)
        self.assertEqual(report['arms'], ['Q6S5GP0', 'Q6S5GP1'])
        self.assertEqual(report['knob'], 'game_phase')
        self.assertEqual(report['timestamp_only_arms'], {'Q6S5GP0': 1865, 'Q6S5GP1': 9852})
        self.assertEqual(report['post_close'], 6)
        self.assertEqual(report['examiner_status'], 'HOLD_PRE_PR')
        self.assertEqual(report['examiner_path_after_pr'], 'READY_NOT_SCORED')
        self.assertIs(report['scored'], False)
        self.assertIs(report['digest_all_match_claimed'], True)
        self.assertIsNone(report['results'])
        self.assertIsNone(report['pnl'])
        self.assertIsNone(report['maker_gross_roi_delta_GP1_minus_GP0'])
        self.assertIsNone(report['maker_gross_roi_delta_GP1_minus_GP0_within_FL1'])
        self.assertIsNone(report['reading'])
        self.assertEqual(report['live_gets'], 0)
        self.assertEqual(report['orders'], 0)
        self.assertEqual(report['fee_label'], 'CACHE_NOT_R1P1')
        self.assertEqual(report['evidence_class'], 'IN_SAMPLE_DEV')
        self.assertEqual(report['family_size'], 4)
        self.assertIs(report['hypothesis_generating_only'], True)
        self.assertIs(report['universe_cap_last_knob'], True)
        self.assertEqual(report['first_pitch_source'], 'SCHEDULED_START_PROXY')
        self.assertEqual(report['scorecard_family_size'], 4)
        self.assertEqual(report['scorecard_first_pitch_source'], 'SCHEDULED_START_PROXY')
        self.assertIsNone(report['scorecard_results'])
        self.assertIsNone(report['scorecard_pnl'])
