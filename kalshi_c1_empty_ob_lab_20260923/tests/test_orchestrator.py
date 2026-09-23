"""Unit pins for the C1 EMPTY-OB harness.

Pin locks and in-memory refuse checks only. Freeze outputs stay null.
The subject is the attached admitted panel and the four empty orderbooks.
"""
import copy
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


def _write_books(payloads):
    directory = tempfile.TemporaryDirectory()
    root = Path(directory.name)
    for ticker, payload in payloads:
        (root / (ticker + '.json')).write_text(json.dumps(payload))
    return directory, root


class PinTests(unittest.TestCase):
    def test_binding_pins_digests_and_four_empty_books(self):
        self.assertFalse(orchestrator.GOVERNANCE_TREE.exists())
        binding = orchestrator.instrument_binding()
        panel = orchestrator.load_panel()
        books = orchestrator.load_orderbooks()
        frozen = json.loads(orchestrator.FROZEN_EXPERIMENT.read_text())
        stamp = json.loads(orchestrator.CONDUCTOR_STAMP.read_text())
        pins = json.loads(orchestrator.SOURCE_PINS.read_text())
        self.assertEqual(binding['experiment_id'], 'C1-EMPTY-OB-HARNESS')
        self.assertEqual(binding['feature_family'], 'EMPTY-OB')
        self.assertEqual(frozen['feature_family'], 'EMPTY-OB')
        self.assertEqual(stamp['feature_family'], 'EMPTY-OB')
        self.assertEqual(stamp['packet_id'], 'C1-EMPTY-OB-HARNESS')
        self.assertEqual(binding['knob'], 'empty_book_gate')
        self.assertEqual(frozen['knob'], 'empty_book_gate')
        self.assertEqual(binding['panel_version'], '2026-09-22.c1-kxufcfight-v0')
        self.assertEqual(panel['panel_version'], '2026-09-22.c1-kxufcfight-v0')
        self.assertEqual(panel['admitted_at'], '2026-09-23T00:49:43Z')
        self.assertEqual(binding['admitted_at'], '2026-09-23T00:49:43Z')
        self.assertEqual(binding['events_n'], 2)
        self.assertEqual(binding['markets_n'], 4)
        self.assertEqual(len(panel['events']), 2)
        self.assertEqual(len(panel['markets']), 4)
        self.assertEqual(binding['books_n'], 4)
        self.assertIs(binding['books_all_empty'], True)
        self.assertEqual(len(books), 4)
        self.assertEqual([row['ticker'] for row in books], list(orchestrator.TICKERS))
        for row in books:
            self.assertEqual(row['sha256'], orchestrator.EMPTY_OB_SHA256)
            self.assertIs(row['empty'], True)
            self.assertIs(row['depth_present'], False)
            self.assertEqual(row['payload'], {'orderbook_fp': {'no_dollars': [], 'yes_dollars': []}})
        self.assertEqual(binding['feebook_commit'], '22371178cb2663250b4762f328069571c48cb551')
        self.assertEqual(binding['rails_commit'], '6a28e0d6254327ea4e6451c781bec56215ac6cac')
        self.assertEqual(binding['feebook_commit'], frozen['fee_pin'])
        self.assertEqual(binding['rails_commit'], frozen['rails_pin'])
        self.assertEqual(binding['examiner_formula_id'], feebook.EXAMINER_FORMULA_ID)
        self.assertEqual(binding['fee_credit_rule_id'], rails.FEE_CREDIT_RULE_ID)
        self.assertEqual(binding['probe_formula_id'], feebook.EXAMINER_FORMULA_ID)
        self.assertEqual(binding['probe_series_resolution'], 'default_unknown_series')
        self.assertEqual(binding['fee_source'], 'feebook')
        self.assertEqual(binding['rails_source'], 'rails')
        self.assertIs(binding['fee_import_only'], True)
        self.assertIs(binding['rails_import_only'], True)
        self.assertIs(binding['fee_applied_to_books'], False)
        self.assertIs(binding['probe_scorecard_write'], False)
        self.assertIs(binding['s2_r2p4_ungated'], False)
        self.assertIs(frozen['s2_r2p4_ungated'], False)
        self.assertIs(binding['admit_py_run'], False)
        self.assertIs(binding['poll_steal'], False)
        self.assertIs(binding['logan_keys_required'], False)
        self.assertIs(binding['live_orders'], False)
        self.assertIs(binding['signal_retune_000'], False)
        self.assertIs(binding['cap_sr_reopen'], False)
        self.assertIs(binding['qf_reopen'], False)
        self.assertIs(binding['l2_cat_reopen'], False)
        self.assertIs(binding['prop_lq_reopen'], False)
        self.assertIs(binding['sot_id_reopen'], False)
        self.assertIs(binding['fee_is_knob'], False)
        self.assertIs(binding['stub_ready'], False)
        self.assertEqual(binding['examiner_status'], 'NOT_SCORED')
        self.assertEqual(binding['lee_ready'], 'REFUSED')
        self.assertIsNone(binding['strategy_pointer'])
        self.assertEqual(binding['dead_cards'], orchestrator.DEAD_CARDS)
        self.assertEqual(tuple(frozen['scorecard_fields']), orchestrator.SCORECARD_FIELDS)
        self.assertEqual([arm['id'] for arm in frozen['arms']], list(orchestrator.ARMS))
        self.assertEqual(frozen['arms'][0]['empty_book_gate'], 'refuse_scorecard')
        self.assertEqual(frozen['arms'][1]['empty_book_gate'], 'wait_fresh_depth')
        self.assertEqual(stamp['arms'], ['C1E0', 'C1E1'])
        self.assertIsNone(panel['results'])
        self.assertIsNone(panel['pnl'])
        self.assertIsNone(frozen['results'])
        self.assertIsNone(frozen['pnl'])
        self.assertIsNone(stamp['results'])
        self.assertIsNone(stamp['pnl'])
        self.assertEqual(pins['freeze_sha256'], orchestrator.FREEZE_SHA256)
        self.assertEqual(pins['parent_freeze_sha256'], orchestrator.PARENT_SHA256)
        self.assertEqual(pins['panel_admitted_sha256'], orchestrator.PANEL_SHA256)
        self.assertEqual(pins['empty_ob_pin_sha256'], orchestrator.EMPTY_OB_SHA256)
        self.assertEqual(pins['pin_meta_sha256'], orchestrator.PIN_META_SHA256)
        self.assertIsNone(pins['results'])
        self.assertIsNone(pins['pnl'])
        for key in orchestrator.SCORECARD_FIELDS:
            self.assertIsNone(pins[key])
            self.assertIsNone(frozen[key])
        status = orchestrator.conductor_pin_status()
        self.assertIs(status['conductor_bytes_in_checkout'], True)
        self.assertIs(status['freeze_matches_conductor_claim'], True)
        self.assertIs(status['parent_freeze_matches_conductor_claim'], True)
        self.assertIs(status['panel_matches_conductor_claim'], True)
        self.assertIs(status['pin_meta_matches_conductor_claim'], True)
        self.assertIs(status['empty_books_match_conductor_claim'], True)
        self.assertIs(status['governance_tree_present'], False)
        self.assertEqual(orchestrator.sha256_file(orchestrator.PACKET), orchestrator.FREEZE_SHA256)
        self.assertEqual(orchestrator.sha256_file(orchestrator.PARENT_FREEZE), orchestrator.PARENT_SHA256)
        self.assertEqual(orchestrator.sha256_file(orchestrator.PANEL_COPY), orchestrator.PANEL_SHA256)
        self.assertEqual(orchestrator.sha256_file(orchestrator.PANEL_PRODUCTION), orchestrator.PANEL_SHA256)
        self.assertEqual(orchestrator.sha256_file(orchestrator.PIN_META), orchestrator.PIN_META_SHA256)
        self.assertEqual(
            orchestrator.FREEZE_SHA256,
            '1b9f8fbec8bad866e055bcabd38c8c633835d505cbd25c367ff0675bff3a4b27',
        )
        self.assertEqual(
            orchestrator.PARENT_SHA256,
            'a191c9b3f71030445d1d32684feb6dc1bf09abb7e09403d5dbdf1927eafc63c9',
        )
        self.assertEqual(
            orchestrator.PANEL_SHA256,
            '24426d804c51bde23cf2557a11a8481a12026da10024094c4ae546d1f7d3956e',
        )
        self.assertEqual(
            orchestrator.EMPTY_OB_SHA256,
            'e07d09f130e604a9e1acfc736fb57cbdfc33d8a5a253466a0cbd5c98cf6c9f74',
        )
        self.assertEqual(
            orchestrator.PIN_META_SHA256,
            '241d745e6ddfb6cccdc8f123e4d57d627635065c3406df8f66d0d0d2e168f4ca',
        )
        self.assertEqual(Path(feebook.__file__).resolve().parent.name, 'kalshi_feebook_lab_20260922')
        self.assertEqual(Path(rails.__file__).resolve().parent.name, 'kalshi_rails_lab_20260922')
        self.assertEqual(
            Path(orchestrator.hygiene.__file__).resolve().parent.name,
            'kalshi_r2p1_hygiene_000_lab_20260922',
        )
        self.assertEqual(
            sorted(path.name for path in PARENT.glob('kalshi_c1_empty_ob_lab_*')),
            ['kalshi_c1_empty_ob_lab_20260923'],
        )

    def test_packet_copies_match_and_scorecard_stays_null(self):
        frozen_bytes = orchestrator.FROZEN_EXPERIMENT.read_bytes()
        empty_bytes = orchestrator.EMPTY_RESULTS.read_bytes()
        pins_bytes = orchestrator.SOURCE_PINS.read_bytes()
        authentic = (
            (orchestrator.FREEZE_NAME, orchestrator.FREEZE_SHA256),
            (orchestrator.PARENT_NAME, orchestrator.PARENT_SHA256),
            (orchestrator.PANEL_NAME, orchestrator.PANEL_SHA256),
            (orchestrator.PIN_NAME, orchestrator.PIN_META_SHA256),
            (orchestrator.STAMP_NAME, orchestrator.CONDUCTOR_STAMP_SHA256),
            (orchestrator.PRE_ACCEPT_NAME, orchestrator.PRE_ACCEPT_EMPTY_SHA256),
            (orchestrator.ACCEPT_NAME, orchestrator.CONDUCTOR_ACCEPT_SHA256),
            (orchestrator.HOLD_NAME, orchestrator.EXAMINER_HOLD_SHA256),
        )
        for name, digest in authentic:
            for path in orchestrator.document_paths(name):
                self.assertEqual(orchestrator.sha256_file(path), digest)
        for directory in orchestrator.orderbook_directories():
            bodies = []
            for ticker in orchestrator.TICKERS:
                raw = (directory / (ticker + '.json')).read_bytes()
                self.assertEqual(hashlib_sha(raw), orchestrator.EMPTY_OB_SHA256)
                self.assertEqual(len(raw), 51)
                bodies.append(raw)
            self.assertEqual(len(set(bodies)), 1)
        for path in (
            orchestrator.FROZEN_EXPERIMENT,
            orchestrator.LAB_BUNDLE / 'FROZEN_EXPERIMENT.json',
            orchestrator.GOVERNANCE_BUNDLE / 'FROZEN_EXPERIMENT.json',
        ):
            self.assertEqual(path.read_bytes(), frozen_bytes)
            payload = json.loads(path.read_text())
            orchestrator.assert_null_scorecard(payload)
        for path in (
            orchestrator.EMPTY_RESULTS,
            orchestrator.LAB_BUNDLE / 'results.json',
            orchestrator.LAB_BUNDLE / 'results' / 'EMPTY_RESULTS.json',
            orchestrator.GOVERNANCE_BUNDLE / 'results.json',
            orchestrator.GOVERNANCE_BUNDLE / 'results' / 'EMPTY_RESULTS.json',
        ):
            self.assertEqual(path.read_bytes(), empty_bytes)
            payload = json.loads(path.read_text())
            self.assertEqual(payload['status'], 'EMPTY_RESULTS_PRE_EXAMINER')
            orchestrator.assert_null_scorecard(payload)
        for path in (
            orchestrator.SOURCE_PINS,
            orchestrator.LAB_BUNDLE / 'SOURCE_PINS.json',
            orchestrator.GOVERNANCE_BUNDLE / 'SOURCE_PINS.json',
        ):
            self.assertEqual(path.read_bytes(), pins_bytes)
        snapshot = orchestrator.frozen_output_snapshot()
        for key in orchestrator.OUTPUT_KEYS:
            self.assertIsNone(snapshot['empty.%s' % key])
            self.assertIsNone(snapshot['frozen.%s' % key])
        hold = json.loads(orchestrator.EXAMINER_HOLD.read_text())
        self.assertEqual(hold['status'], 'NOT_SCORED')
        self.assertIs(hold['stub_ready'], False)
        self.assertEqual(sorted(hold['metrics_null']), sorted(orchestrator.OUTPUT_KEYS))


class ArmTests(unittest.TestCase):
    def test_c1e0_empty_books_refuse_scorecard_without_inventing_depth(self):
        before = {
            path: path.read_bytes()
            for directory in orchestrator.orderbook_directories()
            for path in directory.glob('*.json')
        }
        books = orchestrator.load_orderbooks()
        touched = orchestrator.assert_empty_book_has_no_touch(books[0]['payload'])
        self.assertIsNone(touched)
        reciprocal = feebook.reciprocal_book(books[0]['payload'])
        for key in orchestrator.BID_FIELDS:
            self.assertIsNone(reciprocal[key])
        with self.assertRaises(orchestrator.ScorecardPromotionRefused):
            orchestrator.conduct(orchestrator.C1E0)
        with self.assertRaises(orchestrator.LeeReadyRefused):
            orchestrator.infer_lee_ready(books[0]['payload'])
        with self.assertRaises(orchestrator.InventDepthRefused):
            orchestrator.invent_depth(books[0]['payload'])
        self.assertEqual(books[0]['payload'], {'orderbook_fp': {'no_dollars': [], 'yes_dollars': []}})
        for path, raw in before.items():
            self.assertEqual(path.read_bytes(), raw)

    def test_c1e1_wait_bin_uses_rails_freshness_and_leaves_counts_null(self):
        books = orchestrator.load_orderbooks()
        report = orchestrator.conduct(orchestrator.C1E1)
        self.assertEqual(report['arm'], 'C1E1')
        self.assertEqual(report['empty_book_gate'], 'wait_fresh_depth')
        self.assertEqual(report['book_count'], 4)
        self.assertIs(report['all_empty'], True)
        self.assertIs(report['promoted'], False)
        self.assertIs(report['keepalive'], False)
        self.assertEqual(report['lee_ready'], 'REFUSED')
        self.assertIs(report['fee_applied_to_books'], False)
        orchestrator.assert_null_scorecard(report)
        orchestrator.assert_null_scorecard(report['published'])
        self.assertEqual(len(report['bins']), 4)
        for row in report['bins']:
            self.assertEqual(row['bin'], 'wait_fresh_depth')
            self.assertIs(row['empty'], True)
            self.assertIs(row['depth_present'], False)
            self.assertIs(row['content_fresh_flag'], True)
            self.assertEqual(row['fresh_reason'], 'initial')
            self.assertIs(row['freshness_is_not_depth'], True)
            self.assertIsNone(row['fills'])
            self.assertEqual(row['lee_ready'], 'REFUSED')
        held = orchestrator.conduct(orchestrator.C1E1, keepalive=True)
        for row in held['bins']:
            self.assertIs(row['content_fresh_flag'], False)
            self.assertEqual(row['fresh_reason'], 'keepalive_ignored')
            self.assertEqual(row['bin'], 'wait_fresh_depth')
            self.assertIsNone(row['fills'])
        orchestrator.assert_null_scorecard(held)
        current = rails.BookObservation(
            content=rails.canonical_book_content(books[0]['payload']),
            transaction_time=books[0]['ticker'],
        )
        flag = orchestrator.hygiene.content_fresh_flag(None, current, keepalive=False)
        direct = rails.judge_freshness(None, current, keepalive=False)
        self.assertIs(flag['content_fresh_flag'], direct.fresh)
        self.assertEqual(report['bins'][0]['content_fresh_flag'], flag['content_fresh_flag'])

    def test_depth_book_does_not_promote_or_invent_a_fill(self):
        empty = json.loads(
            (orchestrator.ORDERBOOK_PRODUCTION / (orchestrator.TICKERS[0] + '.json')).read_text()
        )
        depth = {'orderbook_fp': {'yes_dollars': [['0.4200', '1.00']], 'no_dollars': []}}
        payloads = []
        for index, ticker in enumerate(orchestrator.TICKERS):
            payloads.append((ticker, depth if index == 0 else empty))
        directory, root = _write_books(payloads)
        self.addCleanup(directory.cleanup)
        books = orchestrator.load_orderbooks(root)
        self.assertIs(books[0]['depth_present'], True)
        self.assertIs(books[0]['empty'], False)
        self.assertIs(books[1]['empty'], True)
        before = copy.deepcopy(books[0]['payload'])
        with self.assertRaises(orchestrator.ScorecardPromotionRefused):
            orchestrator.conduct(orchestrator.C1E0, books)
        report = orchestrator.conduct(orchestrator.C1E1, books)
        self.assertEqual(report['bins'][0]['bin'], 'depth_present_unscored')
        self.assertIs(report['bins'][0]['depth_present'], True)
        self.assertIsNone(report['bins'][0]['fills'])
        self.assertEqual(report['bins'][1]['bin'], 'wait_fresh_depth')
        self.assertIsNone(report['depth_present_n'])
        self.assertIsNone(report['wait_fresh_depth_n'])
        self.assertIsNone(report['empty_book_n'])
        self.assertIsNone(report['scorecard_refuse_n'])
        self.assertIsNone(report['results'])
        self.assertIsNone(report['pnl'])
        with self.assertRaises(orchestrator.InventFillRefused):
            orchestrator.attempt_fill(depth, 'yes', '1')
        with self.assertRaises(orchestrator.InventDepthRefused):
            orchestrator.invent_depth(empty)
        self.assertEqual(books[0]['payload'], before)
        with self.assertRaises(feebook.BookIncomplete):
            feebook.polarity_fill(empty, 'yes', '1', series=orchestrator.SERIES)


class RefuseTests(unittest.TestCase):
    def test_pre_accept_stub_recreation_and_lee_ready_are_refused(self):
        with self.assertRaises(orchestrator.PreAcceptEmptyRefused):
            orchestrator.load_scorecard(orchestrator.PRE_ACCEPT_EMPTY)
        with self.assertRaises(orchestrator.PanelStubRefused):
            orchestrator.load_panel(orchestrator.PANEL_STUB)
        labeled = {
            'orderbook_fp': {'yes_dollars': [], 'no_dollars': []},
            'labeled_recreation': True,
        }
        payloads = [(ticker, labeled) for ticker in orchestrator.TICKERS]
        directory, root = _write_books(payloads)
        self.addCleanup(directory.cleanup)
        with self.assertRaises(orchestrator.RecreationRefused):
            orchestrator.load_orderbooks(root)
        requested = {
            'ticker': orchestrator.TICKERS[0],
            'payload': {
                'orderbook_fp': {'yes_dollars': [], 'no_dollars': []},
                'lee_ready': True,
            },
            'empty': True,
            'depth_present': False,
        }
        with self.assertRaises(orchestrator.LeeReadyRefused):
            orchestrator.conduct(orchestrator.C1E0, [requested])
        with self.assertRaises(orchestrator.LeeReadyRefused):
            orchestrator.conduct(orchestrator.C1E1, [requested])
        with self.assertRaises(orchestrator.ScorecardPromotionRefused):
            orchestrator.write_scorecard(orchestrator.published_scorecard())
        for key in orchestrator.OUTPUT_KEYS:
            broken = dict(orchestrator.published_scorecard())
            broken[key] = 1
            with self.assertRaises(orchestrator.ScorecardPromotionRefused):
                orchestrator.write_scorecard(broken)
        with self.assertRaises(orchestrator.UnknownGate):
            orchestrator.conduct('C1E2')

    def test_named_refuses_live_paths_and_sibling_trees_stay_closed(self):
        for label in (
            'lee_ready',
            'invent_depth',
            'invented_depth',
            'invent_fills',
            'invented_fills',
            'invented_pnl',
            'labeled_recreation',
            'pre_accept_empty',
            'empty_pin_promotion',
            'admit_py',
            'poll_steal',
            's2_ungate',
            'r2p4_ungate',
            'logan_keys',
            'logan_key',
            'live_orders',
            'q6_retune',
            '000',
            'cap_sr_reopen',
            'qf_reopen',
            'l2_cat_reopen',
            'prop_lq_reopen',
            'sot_id_reopen',
            'examiner_ready',
        ):
            with self.assertRaises(orchestrator.OrchestratorError):
                orchestrator.refuse_adversary(label)
        with self.assertRaises(orchestrator.LiveOrdersForbidden):
            orchestrator.execution_adapter()
        with self.assertRaises(orchestrator.LiveOrdersForbidden):
            orchestrator.assert_public_get('POST')
        self.assertIsNone(orchestrator.assert_public_get('GET'))
        with self.assertRaises(orchestrator.LiveOrdersForbidden):
            orchestrator.assert_route('POST /portfolio/orders')
        self.assertIsNone(orchestrator.assert_route('GET /trade-api/v2/markets/%s/orderbook' % orchestrator.TICKERS[0]))
        with self.assertRaises(orchestrator.UngateRefused):
            orchestrator.ungate_s2_r2p4()
        with self.assertRaises(orchestrator.AdmitPyRefused):
            orchestrator.run_admit_py()
        with self.assertRaises(orchestrator.PollStealRefused):
            orchestrator.steal_poll()
        with self.assertRaises(orchestrator.PollStealRefused):
            orchestrator.fetch_over_network('https://example.invalid/orderbook')
        with self.assertRaises(orchestrator.ExaminerNotReady):
            orchestrator.stamp_examiner_ready()
        source = (ROOT / 'orchestrator.py').read_text()
        for banned in (
            '0.0175',
            '0.07',
            'maker_coefficient',
            'taker_coefficient',
            'common_config',
            'class KalshiExecutionAdapter',
            'urlopen',
            'urllib',
            'os.environ',
            'api_key',
            'private_key',
            'import queue_fragility',
            'import admit',
            'subprocess',
        ):
            self.assertNotIn(banned, source)
        diff = subprocess.check_output(
            ['git', 'diff', '--name-only', orchestrator.BASE_COMMIT, '--', *orchestrator.DOES_NOT_MODIFY],
            cwd=str(PARENT),
            text=True,
        )
        self.assertEqual(diff, '')


def hashlib_sha(raw):
    import hashlib
    return hashlib.sha256(raw).hexdigest()


if __name__ == '__main__':
    unittest.main()
