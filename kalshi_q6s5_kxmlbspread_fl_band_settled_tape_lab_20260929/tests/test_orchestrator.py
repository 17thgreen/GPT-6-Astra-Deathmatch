"""Unit pins for the Q6S5 FL-band settled-tape path.

Band assignment, exclusions, and refuse checks. Synthetic rows exercise
the algebra. The pinned tape is counted, not scored. results and pnl
stay null.
"""
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT.parent
sys.path.insert(0, str(ROOT))

import orchestrator


TICKER = 'KXMLBSPREAD-26SEP242140HOUATH-ATH2'
EVENT = 'KXMLBSPREAD-26SEP242140HOUATH'


def _market(**overrides):
    body = {
        'ticker': TICKER,
        'event_ticker': EVENT,
        'status': 'finalized',
        'result': 'no',
        'close_time': '2026-09-25T04:30:17Z',
        'settlement_ts': '2026-09-25T04:32:18Z',
    }
    body.update(overrides)
    return {'market': body}


def _trade(**overrides):
    row = {
        'ticker': TICKER,
        'created_time': '2026-09-25T04:29:41Z',
        'is_block_trade': False,
        'taker_outcome_side': 'yes',
        'taker_side': 'yes',
        'taker_book_side': 'bid',
        'yes_price_dollars': '0.1000',
        'no_price_dollars': '0.9000',
        'count_fp': '1.00',
    }
    row.update(overrides)
    return row


def _obs(arm, band_id, price, outcome, event, ticker, quantity='1'):
    return {
        'arm': arm,
        'band_id': band_id,
        'p_taker': Decimal(price),
        'q': Decimal(quantity),
        'y_s': outcome,
        'event': event,
        'ticker': ticker,
    }


class PinTests(unittest.TestCase):
    def test_authority_hashes_and_manifest(self):
        digest = orchestrator.digest_status()
        self.assertIs(digest['digest_all_match_claimed'], True)
        self.assertEqual(digest['missing'], [])
        self.assertEqual(digest['mismatch'], [])
        self.assertIsNone(digest['results'])
        self.assertIsNone(digest['pnl'])
        for item in digest['absent_not_invented']:
            self.assertIs(item['present'], False)
            self.assertIs(item['invented'], False)
        self.assertFalse(orchestrator.GOVERNANCE_PACKET.exists())
        authority = json.loads(orchestrator.AUTHORITY.read_text(encoding='utf-8'))
        self.assertIs(authority['digest_all_match_claimed'], True)
        self.assertEqual(authority['accept_sha256'], orchestrator.ACCEPT_SHA256)
        self.assertEqual(authority['freeze_sha256'], orchestrator.FREEZE_SHA256)
        self.assertEqual(authority['authentic_bundle_sha256'], orchestrator.BUNDLE_SHA256)
        self.assertEqual(authority['band_registry_sha256'], orchestrator.BAND_REGISTRY_SHA256)
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
        capture_copy = PARENT / 'lab' / 'astra-capture' / 'r3-p3-fl-maker-taker' / 'bands_registry_10c.json'
        self.assertEqual(orchestrator.sha256_file(capture_copy), orchestrator.BAND_REGISTRY_SHA256)

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


class BandTests(unittest.TestCase):
    def test_boundaries_follow_registry_inclusivity(self):
        registry = orchestrator.load_band_registry()
        cases = (
            ('0.00', 'b00', 'Q6S5FL0'),
            ('0.10', 'b01', 'Q6S5FL0'),
            ('0.1999999999', 'b01', 'Q6S5FL0'),
            ('0.20', 'b02', 'Q6S5FL1'),
            ('0.50', 'b05', 'Q6S5FL1'),
            ('0.7999999999', 'b07', 'Q6S5FL1'),
            ('0.80', 'b08', 'Q6S5FL2'),
            ('0.90', 'b09', 'Q6S5FL2'),
            ('1.00', 'b09', 'Q6S5FL2'),
        )
        for price, band_id, arm in cases:
            got_arm, got_band = orchestrator.assign_arm(price, registry)
            self.assertEqual(got_band, band_id, price)
            self.assertEqual(got_arm, arm, price)
        with self.assertRaises(orchestrator.RebinRefused):
            orchestrator.rebin([{'band_id': 'custom'}])
        shifted = json.loads(json.dumps(registry))
        shifted['bands'][1]['hi_inclusive'] = True
        with self.assertRaises(orchestrator.RebinRefused):
            orchestrator.assign_registry_band('0.20', shifted)


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
        boundary = orchestrator.classify_trade(
            _trade(created_time='2026-09-26T23:59:59Z'),
            _market(close_time='2026-09-26T23:59:59.001Z'),
        )
        self.assertIs(boundary['included'], True)

    def test_post_close_block_conflict_and_price(self):
        post = orchestrator.classify_trade(
            _trade(created_time='2026-09-25T04:30:17Z'),
            _market(),
        )
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

    def test_lee_ready_backfill_lookahead_and_capture_are_refused(self):
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
        with self.assertRaises(orchestrator.NoInvent):
            orchestrator.classify_trade(_trade(pnl='1'), _market())
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'capture.sqlite'
            path.write_bytes(b'not-a-database')
            before = path.read_bytes()
            with self.assertRaises(orchestrator.Admit1CaptureRefused):
                orchestrator.read_admit1_capture(path)
            self.assertEqual(path.read_bytes(), before)

    def test_sep25_markets_stay_out_of_scope(self):
        ticker = 'KXMLBSPREAD-26SEP251840PITDET-DET2'
        got = orchestrator.classify_trade(
            _trade(ticker=ticker),
            _market(ticker=ticker, result='yes', status='finalized'),
        )
        self.assertEqual(got['reason'], 'out_of_scope_sep25')
        self.assertIsNone(got['row'])
        self.assertNotIn('result', got)


class AlgebraTests(unittest.TestCase):
    def _sample(self):
        rows = []
        events = (
            ('E1', 'M1'),
            ('E2', 'M2'),
            ('E3', 'M3'),
        )
        for event, ticker in events:
            rows.append(_obs('Q6S5FL0', 'b01', '0.10', 0, event, ticker))
            rows.append(_obs('Q6S5FL1', 'b05', '0.50', 1, event, ticker + 'B'))
            rows.append(_obs('Q6S5FL2', 'b09', '0.90', 0, event, ticker + 'C'))
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
        fl0 = measured['arms']['Q6S5FL0']['maker_gross_roi']
        fl1 = measured['arms']['Q6S5FL1']['maker_gross_roi']
        fl2 = measured['arms']['Q6S5FL2']['maker_gross_roi']
        self.assertEqual(fl0, Decimal('0.10') / Decimal('0.90'))
        self.assertEqual(fl1, Decimal('-1'))
        self.assertEqual(fl2, Decimal('0.90') / Decimal('0.10'))
        self.assertEqual(
            measured['maker_gross_roi_delta_FL0_minus_FL1'],
            fl0 - fl1,
        )
        self.assertEqual(
            measured['maker_gross_roi_delta_FL2_minus_FL1'],
            fl2 - fl1,
        )
        self.assertEqual(len(measured['loeo']), 3)
        self.assertEqual(len(measured['lomo']), 9)
        self.assertEqual(
            measured['stress_one_tick_worse']['maker_gross_roi_delta_FL0_minus_FL1'],
            (Decimal('0.09') / Decimal('0.91')) - (Decimal('-0.51') / Decimal('0.51')),
        )
        fee = orchestrator.cache_order_fee('maker', '1', '0.90')
        doubled = orchestrator.cache_order_fee('maker', '1', '0.90', times=2)
        self.assertIsNone(fee['formula_id'])
        self.assertIs(fee['fee_honest'], False)
        self.assertIs(fee['claim_as_live_R1P1'], False)
        self.assertEqual(fee['label'], 'CACHE_NOT_R1P1')
        self.assertEqual(doubled['fee'], fee['fee'] * 2)
        self.assertIsNone(fee['pnl'])
        net = (Decimal('0.30') - (fee['fee'] * 3)) / Decimal('2.70')
        self.assertEqual(measured['arms']['Q6S5FL0']['maker_net_roi_cache'], net)
        reading = orchestrator.reading_rule(
            measured['maker_gross_roi_delta_FL0_minus_FL1'],
            [
                item['maker_gross_roi_delta_FL0_minus_FL1']
                for item in measured['loeo']
            ],
        )
        self.assertEqual(reading, 'supports_H1')
        self.assertEqual(orchestrator.verdict_for(reading), 'ITERATE')
        self.assertEqual(
            orchestrator.reading_rule(Decimal('-1'), [Decimal('-1'), Decimal('1'), Decimal('-0.1')]),
            'contradicts_H1',
        )
        self.assertEqual(
            orchestrator.reading_rule(Decimal('1'), [Decimal('1'), Decimal('-1'), None]),
            'inconclusive',
        )

    def test_classified_row_uses_native_price_only(self):
        yes_row = orchestrator.classify_trade(_trade(), _market(result='no'))
        no_row = orchestrator.classify_trade(
            _trade(
                taker_outcome_side='no',
                taker_side='no',
                taker_book_side='ask',
                yes_price_dollars='0.1000',
                no_price_dollars='0.9000',
            ),
            _market(result='no'),
        )
        self.assertEqual(yes_row['row']['band_id'], 'b01')
        self.assertEqual(yes_row['row']['arm'], 'Q6S5FL0')
        self.assertEqual(yes_row['row']['p_taker'], Decimal('0.1000'))
        self.assertEqual(yes_row['row']['y_s'], 0)
        self.assertEqual(no_row['row']['band_id'], 'b09')
        self.assertEqual(no_row['row']['arm'], 'Q6S5FL2')
        self.assertEqual(no_row['row']['p_taker'], Decimal('0.9000'))
        self.assertEqual(no_row['row']['y_s'], 1)
        same_band = orchestrator.classify_trade(_trade(), _market(result='yes'))
        self.assertEqual(same_band['row']['band_id'], yes_row['row']['band_id'])
        self.assertEqual(same_band['row']['y_s'], 1)


class ScorecardTests(unittest.TestCase):
    def test_published_card_stays_null_and_refuses_are_closed(self):
        card = orchestrator.published_scorecard()
        hold = orchestrator.examiner_status()
        self.assertIsNone(card['results'])
        self.assertIsNone(card['pnl'])
        self.assertIsNone(card['metrics']['maker_gross_roi_delta_FL0_minus_FL1'])
        self.assertIsNone(card['metrics']['reading'])
        self.assertEqual(hold['status'], 'HOLD_PRE_PR')
        self.assertEqual(hold['examiner_path_after_pr'], 'READY_NOT_SCORED')
        self.assertIs(hold['scored'], False)
        self.assertIs(hold['stub_ready'], False)
        self.assertIs(hold['signed_by_examiner'], False)
        self.assertIsNone(hold['results'])
        self.assertIsNone(hold['pnl'])
        with self.assertRaises(orchestrator.ScorecardPromotionRefused):
            orchestrator.write_scorecard({'results': '1', 'pnl': None, 'metrics': {}}, '/tmp/x')
        with self.assertRaises(orchestrator.ScorecardPromotionRefused):
            orchestrator.write_scorecard(
                {'results': None, 'pnl': None, 'metrics': {'reading': 'supports_H1'}},
                '/tmp/x',
            )
        with self.assertRaises(orchestrator.LiveOrderRefused):
            orchestrator.live_order()
        with self.assertRaises(orchestrator.AdmitPyRefused):
            orchestrator.run_admit_py()
        with self.assertRaises(orchestrator.DualCloudRefused):
            orchestrator.dual_cloud()
        with self.assertRaises(orchestrator.RetuneRefused):
            orchestrator.retune('q6-000')
        with self.assertRaises(orchestrator.RetuneRefused):
            orchestrator.retune('cap-sr')
        with self.assertRaises(orchestrator.RetuneRefused):
            orchestrator.retune('q6s1')
        with self.assertRaises(orchestrator.KeepRefused):
            orchestrator.claim_keep()
        with self.assertRaises(orchestrator.CacheNotLiveR1P1):
            orchestrator.claim_live_r1p1()
        with self.assertRaises(orchestrator.OrthogonalKnobRefused):
            orchestrator.set_knob('analysis_slice')
        with self.assertRaises(orchestrator.OrthogonalKnobRefused):
            orchestrator.set_knob('fill_model')
        self.assertEqual(orchestrator.set_knob('price_band'), 'price_band')

    def test_pinned_print_count_is_a_pin_and_conduct_does_not_score(self):
        report = orchestrator.conduct()
        self.assertEqual(report['n_prints_pinned'], 11723)
        self.assertEqual(report['arms'], ['Q6S5FL0', 'Q6S5FL1', 'Q6S5FL2'])
        self.assertEqual(report['knob'], 'price_band')
        self.assertEqual(report['examiner_status'], 'HOLD_PRE_PR')
        self.assertIs(report['scored'], False)
        self.assertIs(report['digest_all_match_claimed'], True)
        self.assertIsNone(report['results'])
        self.assertIsNone(report['pnl'])
        self.assertIsNone(report['maker_gross_roi_delta_FL0_minus_FL1'])
        self.assertIsNone(report['reading'])
        self.assertEqual(report['live_gets'], 0)
        self.assertEqual(report['orders'], 0)
        self.assertEqual(report['fee_label'], 'CACHE_NOT_R1P1')
        source = (ROOT / 'orchestrator.py').read_text(encoding='utf-8')
        for banned in ('urlopen', 'import sqlite3', 'requests.get'):
            self.assertNotIn(banned, source)
