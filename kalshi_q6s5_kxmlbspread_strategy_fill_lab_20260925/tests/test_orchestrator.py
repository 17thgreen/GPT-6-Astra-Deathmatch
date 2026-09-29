"""Unit pins for the Q6S5 strategy-fill path.

Schema and refuse checks only. A through observation is not a fill and
not profit. Scorecard fields stay null.
"""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT.parent
sys.path.insert(0, str(ROOT))

import orchestrator


TICKER = 'KXMLBSPREAD-26SEP242140HOUATH-ATH2'


def _row(**overrides):
    base = {
        'ticker': TICKER,
        'quote_ts': '2026-09-26T18:00:00Z',
        'trade_ts': '2026-09-26T18:00:01Z',
        'resting_side': 'bid',
        'resting_price': '0.40',
        'trade_yes_price': '0.39',
    }
    base.update(overrides)
    return base


class AuthorityTests(unittest.TestCase):
    def test_governance_paths_stay_unrecreated_and_vendored_pins_match(self):
        self.assertFalse((PARENT / orchestrator.ACCEPT_PATH).exists())
        self.assertFalse((PARENT / orchestrator.FREEZE_PATH).exists())
        self.assertFalse((PARENT / orchestrator.KICK_PATH).exists())
        bundle = PARENT / 'lab' / 'governance' / 'astra' / 'packets' / 'Q6S5_KXMLBSPREAD_STRATEGY_FILL'
        self.assertFalse(bundle.exists())
        pins = orchestrator.digest_status()
        self.assertIs(pins['digest_all_match_claimed'], True)
        self.assertEqual(pins['missing'], [])
        self.assertEqual(pins['mismatch'], [])
        self.assertIs(pins['bytes_recreated'], False)
        self.assertEqual(len(pins['pins']), 14)
        binding = orchestrator.instrument_binding()
        self.assertEqual(binding['conductor_accept_sha256'], orchestrator.ACCEPT_SHA256)
        self.assertEqual(binding['freeze_sha256'], orchestrator.FREEZE_SHA256)
        self.assertEqual(binding['kick_sha256_prefix'], 'dc19794b')
        self.assertEqual(binding['admit1_ruling_prefix'], 'ac7cfe63')
        self.assertIs(binding['parent_freeze_intact'], True)
        self.assertIs(binding['digest_all_match_claimed'], True)
        self.assertEqual(binding['live_gets'], 0)
        self.assertIsNone(binding['results'])
        self.assertIsNone(binding['pnl'])
        self.assertIsNone(binding['roi'])

    def test_digest_claim_is_true_only_when_every_row_matches(self):
        rows = [
            {'key': 'a', 'match': True, 'present': True, 'claimed_sha256': 'aa', 'on_disk_sha256': 'aa'},
            {'key': 'b', 'match': True, 'present': True, 'claimed_sha256': 'bb', 'on_disk_sha256': 'bb'},
        ]
        matched = orchestrator.digest_status(rows)
        self.assertIs(matched['digest_all_match_claimed'], True)
        self.assertEqual(matched['missing'], [])
        broken = orchestrator.digest_status([
            rows[0],
            {'key': 'b', 'match': False, 'present': True, 'claimed_sha256': 'bb', 'on_disk_sha256': 'cc'},
        ])
        self.assertIs(broken['digest_all_match_claimed'], False)
        self.assertIn('b', broken['mismatch'])


class Admit1Tests(unittest.TestCase):
    def test_window_is_half_open_and_rejects_inside_timestamps(self):
        self.assertIs(orchestrator.in_admit1_window('2026-09-27T00:00:00Z'), True)
        self.assertIs(orchestrator.in_admit1_window('2026-09-30T03:59:59Z'), True)
        self.assertIs(orchestrator.in_admit1_window('2026-09-26T23:59:59Z'), False)
        self.assertIs(orchestrator.in_admit1_window('2026-09-30T04:00:00Z'), False)
        with self.assertRaises(orchestrator.Admit1WindowRejected):
            orchestrator.classify_fill(_row(trade_ts='2026-09-27T00:00:00Z'))
        with self.assertRaises(orchestrator.Admit1WindowRejected):
            orchestrator.classify_fill(_row(
                quote_ts='2026-09-26T12:00:00Z',
                trade_ts='2026-09-30T03:59:59Z',
            ))
        observed = orchestrator.classify_fill(_row(
            quote_ts='2026-09-26T12:00:00Z',
            trade_ts='2026-09-30T04:00:00Z',
        ))
        self.assertEqual(observed['status'], 'THROUGH_OBSERVED_NO_FILL')
        self.assertIsNone(observed['contracts'])

    def test_backfill_and_capture_sqlite_are_refused_unread(self):
        with self.assertRaises(orchestrator.Admit1BackfillRefused):
            orchestrator.classify_fill(_row(backfill=True))
        with self.assertRaises(orchestrator.Admit1BackfillRefused):
            orchestrator.classify_fill(_row(source='admit1_backfill'))
        missing = PARENT / 'lab' / 'astra-capture' / 'not-a-real-dir' / 'capture.sqlite'
        self.assertFalse(missing.exists())
        with self.assertRaises(orchestrator.Admit1CaptureRefused):
            orchestrator.read_admit1_capture(missing)
        with self.assertRaises(orchestrator.Admit1CaptureRefused):
            orchestrator.read_admit1_capture('/data/prospective/capture.sqlite')
        with self.assertRaises(orchestrator.Admit1CaptureRefused):
            orchestrator.classify_fill(_row(db_path='nfl_prospective_recorder_20260922/capture.sqlite'))
        self.assertNotIn('sqlite3', sys.modules)


class LookaheadAndLeeReadyTests(unittest.TestCase):
    def test_lookahead_is_refused(self):
        with self.assertRaises(orchestrator.LookaheadRefused):
            orchestrator.classify_fill(_row(
                quote_ts='2026-09-26T18:00:01Z',
                trade_ts='2026-09-26T18:00:01Z',
            ))
        with self.assertRaises(orchestrator.LookaheadRefused):
            orchestrator.classify_fill(_row(trade_ts='2026-09-26T17:59:59Z'))
        with self.assertRaises(orchestrator.LookaheadRefused):
            orchestrator.classify_fill(_row(settlement_ts='2026-09-26T20:00:00Z'))
        with self.assertRaises(orchestrator.LookaheadRefused):
            orchestrator.classify_fill(_row(book_after_trade={'yes': '0.50'}))

    def test_lee_ready_is_refused_on_every_input(self):
        with self.assertRaises(orchestrator.LeeReadyRefused):
            orchestrator.infer_lee_ready(_row())
        with self.assertRaises(orchestrator.LeeReadyRefused):
            orchestrator.classify_fill(_row(lee_ready=True))
        with self.assertRaises(orchestrator.LeeReadyRefused):
            orchestrator.classify_fill(_row(classifier='lee-ready'))
        with self.assertRaises(orchestrator.LeeReadyRefused):
            orchestrator.classify_fill(_row(aggressor_inference='buy'))


class FillModelTests(unittest.TestCase):
    def test_through_observation_does_not_invent_a_fill(self):
        bid = orchestrator.classify_fill(_row())
        self.assertEqual(bid['fill_model'], 'public_trade_through_conservative')
        self.assertEqual(bid['status'], 'THROUGH_OBSERVED_NO_FILL')
        self.assertIs(bid['through'], True)
        self.assertIsNone(bid['contracts'])
        self.assertIsNone(bid['simulated_fill'])
        self.assertIsNone(bid['pnl'])
        self.assertIsNone(bid['roi'])
        self.assertIsNone(bid['results'])
        self.assertIs(bid['counts_toward_keep'], False)
        self.assertIsNone(bid['formula_id'])
        self.assertIsNone(bid['mechanic_demo_observed'])
        self.assertEqual(bid['mechanic_demo_observed_status'], 'UNAVAILABLE')
        ask = orchestrator.classify_fill(_row(
            resting_side='ask',
            resting_price='0.40',
            trade_yes_price='0.41',
        ))
        self.assertIs(ask['through'], True)
        self.assertIsNone(ask['contracts'])
        touch = orchestrator.classify_fill(_row(trade_yes_price='0.40'))
        self.assertEqual(touch['status'], 'TOUCH_NOT_THROUGH')
        self.assertIs(touch['through'], False)
        self.assertIsNone(touch['contracts'])
        off = orchestrator.classify_fill(_row(resting_side='bid', trade_yes_price='0.41'))
        self.assertEqual(off['status'], 'NOT_THROUGH')
        self.assertIsNone(off['pnl'])

    def test_missing_fields_and_explicit_fills_are_not_invented(self):
        incomplete = orchestrator.classify_fill(_row(trade_yes_price=None))
        self.assertEqual(incomplete['status'], 'INCOMPLETE_NOT_INVENTED')
        self.assertIsNone(incomplete['through'])
        self.assertIsNone(incomplete['contracts'])
        with self.assertRaises(orchestrator.InventedFillRefused):
            orchestrator.classify_fill(_row(invent_fill=True))
        with self.assertRaises(orchestrator.InventedFillRefused):
            orchestrator.classify_fill(_row(contracts='1'))
        with self.assertRaises(orchestrator.InventedFillRefused):
            orchestrator.classify_fill(_row(pnl='0'))
        with self.assertRaises(orchestrator.InventedFillRefused):
            orchestrator.classify_fill(_row(simulated_fill={'contracts': '1'}))
        with self.assertRaises(orchestrator.OrchestratorError):
            orchestrator.classify_fill(_row(resting_price=0.40))

    def test_mechanic_demo_cells_stay_unavailable(self):
        demo = orchestrator.classify_fill(
            _row(demo_fills=[{'contracts': '5', 'pnl': '10'}]),
            model='mechanic_demo_observed',
        )
        self.assertEqual(demo['status'], 'UNAVAILABLE')
        self.assertIsNone(demo['mechanic_demo_observed'])
        self.assertIsNone(demo['public_trade_through_conservative'])
        self.assertIsNone(demo['contracts'])
        self.assertIsNone(demo['pnl'])
        self.assertNotIn('demo_fills', demo)
        with self.assertRaises(orchestrator.InventedFillRefused):
            orchestrator.classify_fill(_row(invent_fill=True), model='mechanic_demo_observed')
        with self.assertRaises(orchestrator.UnknownModel):
            orchestrator.classify_fill(_row(), model='lee_ready_fill')

    def test_missing_queue_bytes_are_not_recreated(self):
        with self.assertRaises(orchestrator.QueueBytesNotRecreated):
            orchestrator.recreate_queue_bytes('08aa54de' + 'ab')
        with self.assertRaises(orchestrator.QueueBytesNotRecreated):
            orchestrator.recreate_queue_bytes(None)
        with self.assertRaises(orchestrator.QueueBytesNotRecreated):
            orchestrator.classify_fill(_row(queue_artifact_sha256='08aa54de' + 'cd'))


class ArmFeeScorecardTests(unittest.TestCase):
    def test_arms_fee_and_scorecard_stay_null(self):
        self.assertEqual(orchestrator.parent_arms(), orchestrator.ARMS)
        self.assertFalse((ROOT / 'admit.py').exists())
        label = orchestrator.fee_output()
        self.assertEqual(label['label'], 'CACHE_NOT_R1P1')
        self.assertEqual(label['fee_type'], 'quadratic')
        self.assertEqual(label['multiplier'], '0.5')
        self.assertIsNone(label['formula_id'])
        self.assertIs(label['cache_labeled'], True)
        self.assertIs(label['live_r1p1'], False)
        self.assertIsNone(label['fee_dollars'])
        with self.assertRaises(orchestrator.CacheNotLiveR1P1):
            orchestrator.claim_live_r1p1(label)
        binding = orchestrator.instrument_binding()
        self.assertEqual(binding['knob'], 'fill_model')
        self.assertEqual(binding['arms'][0]['analysis_slice'], 'maker_vs_taker_native')
        self.assertEqual(binding['arms'][1]['analysis_slice'], 'content_fresh_vs_stale_bin')
        self.assertEqual(binding['examiner_status'], 'HOLD_PRE_PR')
        self.assertIs(binding['stub_ready'], False)
        self.assertEqual(binding['live_gets'], 0)
        for arm in ('Q6S5A0', 'Q6S5A1'):
            report = orchestrator.conduct(arm)
            self.assertIsNone(report['roi'])
            self.assertIsNone(report['results'])
            self.assertIsNone(report['pnl'])
            self.assertIs(report['counts_toward_keep'], False)
            self.assertEqual(report['analysis_slice'], orchestrator.ARMS[arm])
        empty = orchestrator.published_scorecard()
        orchestrator.assert_null_scorecard(empty)
        hold = json.loads(orchestrator.EXAMINER_HOLD.read_text())
        self.assertEqual(hold['status'], 'HOLD_PRE_PR')
        self.assertIs(hold['stub_ready'], False)
        self.assertIs(hold['signed_by_examiner'], False)
        self.assertIsNone(hold['verdict'])
        with self.assertRaises(orchestrator.ScorecardPromotionRefused):
            orchestrator.write_scorecard(empty)
        with self.assertRaises(orchestrator.LiveOrderRefused):
            orchestrator.public_get('/portfolio/orders')
        with self.assertRaises(orchestrator.LiveOrderRefused):
            orchestrator.live_order('/orders')
        with self.assertRaises(orchestrator.AdmitPyRefused):
            orchestrator.run_admit_py()
        with self.assertRaises(orchestrator.DualCloudRefused):
            orchestrator.dual_cloud()
        for name in ('q6-000', 's1', 'cap-sr', 'q6s1'):
            with self.assertRaises(orchestrator.RetuneRefused):
                orchestrator.retune(name)
        stub = orchestrator.public_get('/markets')
        self.assertEqual(stub['live_gets'], 0)
        self.assertIs(stub['network'], False)
        panel = orchestrator.load_panel()
        self.assertIsNone(panel['admitted_at'])
        self.assertEqual(len(panel['markets']), 12)
