"""Unit pins for the R3-P2 queue_position ingest.

The desk series is {meta, samples[]}. A missing desk file is not filled in.
Calibration metrics stay null.
"""
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(PARENT / 'kalshi_rails_lab_20260922'))

import ingest
import rails


def _series(samples_n=2, brier=None, leftover=False, fp0='4207.00', fp1='10.00'):
    samples = []
    batch = []
    for index in range(samples_n):
        fp = fp0 if index == 0 else fp1
        order_id = 'ord-%d' % index
        samples.append({
            'sample_id': index,
            'order_id': order_id,
            'ticker': ingest.TICKER if index == 0 else 'KXNFLGAME-26OCT01PITCLE-CLE',
            'queue_position_fp': fp,
            'order_canceled_clean': True,
            'is_fill': False,
            'fill': None,
            'abs_err_contracts': None,
            'signed_bias': None,
            'brier': brier,
        })
        batch.append({'order_id': order_id, 'queue_position_fp': fp})
    return {
        'meta': {
            'host': 'demo-api.kalshi.co',
            'leftover_resting': leftover,
            'n_success_including_prior': samples_n,
            'n_success_new_total': samples_n - 1,
            'abs_err_contracts': None,
            'signed_bias': None,
            'brier': None,
        },
        'samples': samples,
        'queue_positions': batch,
    }


class FixtureTests(unittest.TestCase):
    def test_first_poll_queue_position_and_cancel(self):
        poll = ingest.load_first_poll()
        self.assertIn('queue_position_fp', poll)
        self.assertEqual(poll['queue_position_fp'], '4207.00')
        self.assertEqual(poll['ticker'], 'KXNFLGAME-26OCT01PITCLE-PIT')
        self.assertEqual(poll['verdict'], 'POLL_OK')
        self.assertEqual(poll['host'], 'demo-api.kalshi.co')
        self.assertIs(poll['order_canceled_clean'], True)
        self.assertIs(poll['is_fill'], False)
        self.assertIsNone(poll['fill'])
        self.assertEqual(poll['l2_top']['price'], '0.01')
        self.assertEqual(poll['l2_top']['size_narrative'], '~4208')
        self.assertIsNone(poll['l2_top']['size_exact'])
        self.assertIsNone(poll['secrets'])
        self.assertIsNone(poll['live_keys'])

    def test_desk_series_absent_is_not_invented(self):
        self.assertFalse(ingest.DESK_SERIES_PATH.is_file())
        self.assertFalse(ingest.SERIES_PATH.is_file())
        with self.assertRaises(ingest.SeriesSourceAbsent):
            ingest.embed_desk_series()
        with self.assertRaises(ingest.SeriesSourceAbsent):
            ingest.load_series()
        report = ingest.ingest()
        self.assertEqual(report['status'], 'SAMPLE_INGESTED_CALIBRATION_NOT_RUN')
        self.assertIs(report['series_embedded'], False)
        self.assertIs(report['series_source_absent'], True)
        self.assertIsNone(report['samples_n'])
        self.assertIsNone(report['series_sha256'])
        self.assertIsNone(report['n_success_including_prior'])
        self.assertIsNone(report['n_success_new_total'])
        self.assertEqual(report['queue_position_fp'], '4207.00')
        self.assertIs(report['order_canceled_clean'], True)
        self.assertIs(report['is_fill'], False)
        self.assertIs(report['sample_id_0_cross_check'], True)
        self.assertFalse(ingest.SERIES_PATH.exists())

    def test_series_schema_matches_queue_position_by_order_id(self):
        poll = ingest.load_first_poll()
        payload = _series()
        summary = ingest.assert_series_document(payload, first_poll=poll)
        self.assertEqual(summary['samples_n'], 2)
        self.assertEqual(summary['n_success_including_prior'], 2)
        self.assertEqual(summary['n_success_new_total'], 1)
        self.assertEqual(summary['sample_id_0_queue_position_fp'], '4207.00')
        self.assertIs(summary['leftover_resting'], False)
        payload['samples'][1]['queue_position_fp'] = '11.00'
        with self.assertRaises(ingest.IngestError):
            ingest.assert_series_document(payload, first_poll=poll)
        payload = _series()
        payload['samples'][0]['brier'] = '0.2'
        with self.assertRaises(ingest.CalibrationNotRun):
            ingest.assert_series_document(payload, first_poll=poll)
        payload = _series()
        payload['samples'][1]['is_fill'] = True
        with self.assertRaises(ingest.IngestError):
            ingest.assert_series_document(payload, first_poll=poll)
        payload = _series(leftover='yes')
        with self.assertRaises(ingest.IngestError):
            ingest.assert_series_document(payload, first_poll=poll)
        with self.assertRaises(ingest.IngestError):
            ingest.load_json_text('{"sample_id": 0}\n{"sample_id": 1}\n')

    def test_ingest_keeps_scorecard_null_and_rails_fixed(self):
        report = ingest.ingest()
        frozen = json.loads(ingest.FROZEN_EXPERIMENT.read_text())
        empty = json.loads(ingest.EMPTY_RESULTS.read_text())
        self.assertEqual(report['queue_label']['queue_attribution_bin'], 'outside_pinned_bins')
        self.assertEqual(report['queue_label']['rails_commit'], ingest.RAILS_COMMIT)
        self.assertEqual(rails.QUEUE_AHEAD_DEFAULT, ingest.RAILS_QUEUE_AHEAD)
        self.assertEqual(rails.STRESS_QUEUE_AHEAD, ingest.RAILS_STRESS_AHEAD)
        self.assertIs(report['queue_label']['q6_retune'], False)
        self.assertIs(report['live_orders'], False)
        self.assertIs(report['signal_retune_000'], False)
        self.assertIs(frozen['series_embedded'], False)
        self.assertIsNone(frozen['series_sha256'])
        self.assertIsNone(frozen['samples_n'])
        for payload in (report['scorecard'], frozen, empty):
            ingest.assert_null_scorecard(payload)
            for key in ingest.SCORECARD_FIELDS:
                self.assertIsNone(payload[key])

    def test_refuse_estimate_metrics_profit_and_orders(self):
        with self.assertRaises(ingest.CalibrationNotRun):
            ingest.refuse_estimate_metrics({'abs_err_contracts': '1'})
        with self.assertRaises(ingest.CalibrationNotRun):
            ingest.refuse_estimate_metrics({'signed_bias': '0'})
        with self.assertRaises(ingest.CalibrationNotRun):
            ingest.refuse_estimate_metrics({'brier': '0.25'})
        with self.assertRaises(ingest.ProfitLabelRefused):
            ingest.refuse_profit_label({'pnl': '1'})
        with self.assertRaises(ingest.ProfitLabelRefused):
            ingest.refuse_profit_label({'roi': '0.1'})
        with self.assertRaises(ingest.ProfitLabelRefused):
            ingest.refuse_profit_label({'is_profit': True})
        with self.assertRaises(ingest.IngestError):
            ingest.refuse_live_order()
        with self.assertRaises(ingest.IngestError):
            ingest.refuse_q6_retune()
        directory = tempfile.TemporaryDirectory()
        path = Path(directory.name) / 'series.json'
        raw = (json.dumps(_series(), indent=2, sort_keys=True) + '\n').encode('utf-8')
        path.write_bytes(raw)
        loaded = ingest.load_series(path, first_poll=ingest.load_first_poll())
        self.assertEqual(loaded['sha256'], ingest.sha256_bytes(raw))
        self.assertEqual(loaded['samples_n'], 2)
        self.assertFalse(ingest.SERIES_PATH.exists())
        directory.cleanup()
