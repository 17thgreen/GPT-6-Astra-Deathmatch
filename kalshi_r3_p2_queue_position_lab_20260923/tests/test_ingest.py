"""Unit pins for the R3-P2 queue_position ingest.

Load the sanitized Mechanic fixtures. Calibration metrics stay null.
"""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(PARENT / 'kalshi_rails_lab_20260922'))

import ingest
import rails


class FixtureTests(unittest.TestCase):
    def test_load_fixture_queue_position_and_cancel(self):
        poll = ingest.load_first_poll()
        series = ingest.load_series()
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
        self.assertEqual(series['host'], 'demo-api.kalshi.co')
        self.assertIs(series['host_only'], True)
        self.assertEqual(series['leftover_resting'], 'no')
        self.assertEqual(series['n_success_this_run'], 4)
        self.assertIs(series['prior_first_included'], True)
        self.assertEqual(series['rows_total'], 26)
        self.assertEqual(series['embedded_sample_bodies'], 1)
        self.assertEqual(series['unembedded_row_bodies'], 25)
        self.assertIs(series['this_run_success_bodies_embedded'], False)
        self.assertIs(series['checkout_contained_desk_bytes'], False)
        self.assertNotIn('rows', series)

    def test_ingest_joins_rails_label_and_keeps_scorecard_null(self):
        report = ingest.ingest()
        frozen = json.loads(ingest.FROZEN_EXPERIMENT.read_text())
        empty = json.loads(ingest.EMPTY_RESULTS.read_text())
        self.assertEqual(report['status'], 'SAMPLE_INGESTED_CALIBRATION_NOT_RUN')
        self.assertEqual(report['queue_position_fp'], '4207.00')
        self.assertIs(report['order_canceled_clean'], True)
        self.assertIs(report['is_fill'], False)
        self.assertEqual(report['n_success_this_run'], 4)
        self.assertEqual(report['rows_total'], 26)
        self.assertEqual(report['queue_label']['queue_attribution_bin'], 'outside_pinned_bins')
        self.assertEqual(report['queue_label']['rails_commit'], ingest.RAILS_COMMIT)
        self.assertEqual(rails.QUEUE_AHEAD_DEFAULT, ingest.RAILS_QUEUE_AHEAD)
        self.assertEqual(rails.STRESS_QUEUE_AHEAD, ingest.RAILS_STRESS_AHEAD)
        self.assertEqual(rails.scenario_queue('q3300'), ingest.RAILS_QUEUE_AHEAD)
        self.assertEqual(rails.scenario_queue('q10000'), ingest.RAILS_STRESS_AHEAD)
        self.assertIs(report['queue_label']['q6_retune'], False)
        self.assertIs(report['queue_label']['scorecard_write'], False)
        self.assertIs(report['live_orders'], False)
        self.assertIs(report['signal_retune_000'], False)
        for payload in (report['scorecard'], frozen, empty):
            ingest.assert_null_scorecard(payload)
            self.assertEqual(payload['status'], 'SAMPLE_INGESTED_CALIBRATION_NOT_RUN')
            for key in ingest.SCORECARD_FIELDS:
                self.assertIsNone(payload[key])

    def test_refuse_estimate_metrics_and_profit_labels(self):
        with self.assertRaises(ingest.CalibrationNotRun):
            ingest.refuse_estimate_metrics()
        with self.assertRaises(ingest.CalibrationNotRun):
            ingest.refuse_estimate_metrics({'abs_err_contracts': '1'})
        with self.assertRaises(ingest.CalibrationNotRun):
            ingest.refuse_estimate_metrics({'signed_bias': '0'})
        with self.assertRaises(ingest.CalibrationNotRun):
            ingest.refuse_estimate_metrics({'brier': '0.25'})
        with self.assertRaises(ingest.CalibrationNotRun):
            ingest.refuse_estimate_metrics({'mz': '0'})
        with self.assertRaises(ingest.ProfitLabelRefused):
            ingest.refuse_profit_label()
        with self.assertRaises(ingest.ProfitLabelRefused):
            ingest.refuse_profit_label({'pnl': '1'})
        with self.assertRaises(ingest.ProfitLabelRefused):
            ingest.refuse_profit_label({'roi': '0.1'})
        with self.assertRaises(ingest.ProfitLabelRefused):
            ingest.refuse_profit_label({'profit': '1'})
        with self.assertRaises(ingest.ProfitLabelRefused):
            ingest.refuse_profit_label({'is_profit': True})
        filled = ingest.null_scorecard()
        filled['abs_err_contracts'] = '0'
        with self.assertRaises(ingest.CalibrationNotRun):
            ingest.assert_null_scorecard(filled)
        filled = ingest.null_scorecard()
        filled['pnl'] = '0'
        with self.assertRaises(ingest.ProfitLabelRefused):
            ingest.assert_null_scorecard(filled)
        with self.assertRaises(ingest.IngestError):
            ingest.refuse_live_order()
        with self.assertRaises(ingest.IngestError):
            ingest.refuse_q6_retune()

    def test_cancel_is_not_a_fill_and_other_hosts_fail(self):
        poll = ingest.load_first_poll()
        self.assertIs(poll['order_canceled_clean'], True)
        self.assertIs(poll['is_fill'], False)
        poll['is_fill'] = True
        path = ingest.FIRST_POLL_PATH
        original = path.read_text()
        try:
            path.write_text(json.dumps(poll))
            with self.assertRaises(ingest.IngestError):
                ingest.load_first_poll()
        finally:
            path.write_text(original)
        series = ingest.load_series()
        original_series = ingest.SERIES_PATH.read_text()
        try:
            other_host = dict(series)
            other_host['host'] = 'trading-api.kalshi.com'
            ingest.SERIES_PATH.write_text(json.dumps(other_host))
            with self.assertRaises(ingest.IngestError):
                ingest.load_series()
            resting = dict(series)
            resting['leftover_resting'] = 'yes'
            ingest.SERIES_PATH.write_text(json.dumps(resting))
            with self.assertRaises(ingest.IngestError):
                ingest.load_series()
        finally:
            ingest.SERIES_PATH.write_text(original_series)
