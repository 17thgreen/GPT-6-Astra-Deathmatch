"""Unit pins for the R3-P4 L2-SF shape-object harness.

Schema and pin locks only. In-memory synthetic ladders are not a score and
they are not profit. Freeze outputs stay null. The subject is the panel stub
until panel_admitted.json appears. Category slice is not an arm.
"""
import json
import subprocess
import sys
import tempfile
import unittest
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(PARENT / 'kalshi_feebook_lab_20260922'))
sys.path.insert(0, str(PARENT / 'kalshi_rails_lab_20260922'))

import feebook
import orchestrator
import rails


def _freeze_paths():
    return (
        orchestrator.FROZEN_EXPERIMENT,
        orchestrator.EMPTY_RESULTS,
        orchestrator.PACKET,
        orchestrator.PARENT_FREEZE,
        orchestrator.PANEL_STUB,
        orchestrator.LAB_BUNDLE / 'FROZEN_EXPERIMENT.json',
        orchestrator.LAB_BUNDLE / 'results.json',
        orchestrator.GOVERNANCE_BUNDLE / 'FROZEN_EXPERIMENT.json',
        orchestrator.GOVERNANCE_BUNDLE / 'results.json',
        orchestrator.GOVERNANCE_BUNDLE / 'results' / 'EMPTY_RESULTS.json',
    )


class PinTests(unittest.TestCase):
    def test_binding_pins_the_stub_and_the_instruments(self):
        self.assertFalse(orchestrator.PANEL_ADMITTED.exists())
        self.assertFalse(orchestrator.GOVERNANCE_TREE.exists())
        self.assertFalse(orchestrator.CLOSED_LIVE_GET.exists())
        binding = orchestrator.instrument_binding()
        panel = orchestrator.load_panel()
        books = orchestrator.load_orderbooks()
        frozen = json.loads(orchestrator.FROZEN_EXPERIMENT.read_text())
        stamp = json.loads(orchestrator.CONDUCTOR_STAMP.read_text())
        pins = json.loads(orchestrator.SOURCE_PINS.read_text())
        self.assertEqual(binding['experiment_id'], 'R3-P4-L2-SF-HARNESS')
        self.assertEqual(binding['feature_family'], 'L2-SF')
        self.assertEqual(frozen['feature_family'], 'L2-SF')
        self.assertEqual(stamp['feature_family'], 'L2-SF')
        self.assertEqual(binding['knob'], 'shape_object')
        self.assertEqual(frozen['knob'], 'shape_object')
        self.assertIs(binding['category_slice_is_arm'], False)
        self.assertIs(frozen['category_slice_is_arm'], False)
        self.assertEqual(binding['panel_version'], '2026-09-22.r3-p4-l2-shape-v0')
        self.assertIsNone(panel['admitted_at'])
        self.assertIsNone(binding['admitted_at'])
        self.assertEqual(binding['events_n'], 4)
        self.assertEqual(binding['markets_n'], 6)
        self.assertEqual(binding['recorded_orderbook_n'], 6)
        self.assertEqual(binding['two_sided_recorded_n'], 2)
        self.assertEqual(binding['one_sided_recorded_n'], 4)
        self.assertEqual(len(books), 6)
        self.assertEqual([row['ticker'] for row in books], list(orchestrator.STUB_MARKETS))
        self.assertEqual(panel['cohort_summary']['sports_n'], 4)
        self.assertEqual(panel['cohort_summary']['non_sports_n'], 2)
        self.assertEqual(binding['feebook_commit'], '22371178cb2663250b4762f328069571c48cb551')
        self.assertEqual(binding['rails_commit'], '6a28e0d6254327ea4e6451c781bec56215ac6cac')
        self.assertEqual(binding['feebook_commit'], frozen['fee_pin'])
        self.assertEqual(binding['rails_commit'], frozen['rails_pin'])
        self.assertEqual(binding['examiner_formula_id'], feebook.EXAMINER_FORMULA_ID)
        self.assertEqual(binding['fee_credit_rule_id'], rails.FEE_CREDIT_RULE_ID)
        self.assertEqual(binding['fee_source'], 'feebook')
        self.assertEqual(binding['rails_source'], 'rails')
        self.assertEqual(binding['shape_source'], 'kalshi_r3_p4_l2_shape_lab_20260922')
        self.assertIs(binding['fee_import_only'], True)
        self.assertIs(binding['rails_import_only'], True)
        self.assertIs(binding['fee_applied_to_books'], False)
        self.assertIs(binding['probe_scorecard_write'], False)
        self.assertEqual(binding['lee_ready'], 'REFUSED')
        self.assertEqual(binding['invented_depth'], 'REFUSED')
        self.assertIs(binding['l2_cat_reopen'], False)
        self.assertIs(binding['empty_ob_reopen'], False)
        self.assertIs(binding['pr13_dual_edit'], False)
        self.assertIs(binding['s2_r2p4_ungated'], False)
        self.assertIs(binding['admit_py_run'], False)
        self.assertIs(binding['logan_keys_required'], False)
        self.assertIs(binding['live_orders'], False)
        self.assertIs(binding['signal_retune_000'], False)
        self.assertIs(binding['queue_fragility_reopen'], False)
        self.assertIs(binding['cap_sr_reopen'], False)
        self.assertIs(binding['cap_sr_fx_reopen'], False)
        self.assertIs(binding['prop_lq_reopen'], False)
        self.assertIs(binding['sot_id_reopen'], False)
        self.assertIs(binding['stub_ready'], False)
        self.assertEqual(binding['examiner_status'], 'NOT_SCORED')
        self.assertIsNone(binding['strategy_pointer'])
        self.assertEqual(binding['dead_cards'], orchestrator.DEAD_CARDS)
        self.assertEqual(tuple(frozen['scorecard_fields']), orchestrator.SCORECARD_FIELDS)
        self.assertEqual([arm['id'] for arm in frozen['arms']], list(orchestrator.ARMS))
        self.assertEqual(frozen['arms'][0]['shape_object'], 'sf1_half_spread')
        self.assertEqual(frozen['arms'][1]['shape_object'], 'sf2_depth_kl')
        self.assertEqual(stamp['arms'], ['R3P4S0', 'R3P4S1'])
        self.assertEqual(orchestrator.sha256_file(orchestrator.PACKET), orchestrator.FREEZE_SHA256)
        self.assertEqual(orchestrator.sha256_file(orchestrator.PARENT_FREEZE), orchestrator.PARENT_SHA256)
        self.assertEqual(orchestrator.sha256_file(orchestrator.PANEL_STUB), orchestrator.PANEL_STUB_SHA256)
        self.assertEqual(orchestrator.sha256_file(orchestrator.SOURCE_PINS), orchestrator.SOURCE_PINS_SHA256)
        self.assertEqual(pins['orderbooks'][0]['sha256'], orchestrator.ORDERBOOK_PINS[0][2])
        for key in orchestrator.OUTPUT_KEYS:
            self.assertIsNone(pins[key])
            self.assertIsNone(frozen[key])
        status = orchestrator.conductor_pin_status()
        self.assertIs(status['conductor_bytes_in_checkout'], True)
        self.assertIs(status['governance_tree_present'], False)
        self.assertIs(status['l2_cat_live_get_present'], False)
        self.assertEqual(
            Path(feebook.__file__).resolve().parent.name,
            'kalshi_feebook_lab_20260922',
        )
        self.assertEqual(
            Path(rails.__file__).resolve().parent.name,
            'kalshi_rails_lab_20260922',
        )
        self.assertEqual(
            Path(orchestrator.shape.__file__).resolve().parent.name,
            'kalshi_r3_p4_l2_shape_lab_20260922',
        )

    def test_packet_copies_match_and_scorecard_stays_null(self):
        frozen_bytes = orchestrator.FROZEN_EXPERIMENT.read_bytes()
        empty_bytes = orchestrator.EMPTY_RESULTS.read_bytes()
        packet_bytes = orchestrator.PACKET.read_bytes()
        for path in (
            orchestrator.PACKET,
            orchestrator.LAB_BUNDLE / orchestrator.FREEZE_NAME,
            PARENT / 'packets' / orchestrator.FREEZE_NAME,
            orchestrator.GOVERNANCE_BUNDLE / orchestrator.FREEZE_NAME,
        ):
            self.assertEqual(path.read_bytes(), packet_bytes)
        for path in (
            orchestrator.FROZEN_EXPERIMENT,
            orchestrator.LAB_BUNDLE / 'FROZEN_EXPERIMENT.json',
            orchestrator.GOVERNANCE_BUNDLE / 'FROZEN_EXPERIMENT.json',
        ):
            self.assertEqual(path.read_bytes(), frozen_bytes)
            payload = json.loads(path.read_text())
            self.assertIsNone(payload['results'])
            self.assertIsNone(payload['pnl'])
            self.assertIsNone(payload['n_books'])
            self.assertIsNone(payload['n_snapshots'])
        for path in (
            orchestrator.EMPTY_RESULTS,
            orchestrator.LAB_BUNDLE / 'results.json',
            orchestrator.LAB_BUNDLE / 'results' / 'EMPTY_RESULTS.json',
            orchestrator.GOVERNANCE_BUNDLE / 'results.json',
            orchestrator.GOVERNANCE_BUNDLE / 'results' / 'EMPTY_RESULTS.json',
        ):
            self.assertEqual(path.read_bytes(), empty_bytes)
            payload = json.loads(path.read_text())
            for key in orchestrator.OUTPUT_KEYS:
                self.assertIsNone(payload[key])
        shared_stamp = PARENT / 'packets' / 'CONDUCTOR_FROZEN_EXPERIMENT.json'
        shared_empty = PARENT / 'packets' / 'PRE_ACCEPT_EMPTY_RESULTS.json'
        self.assertNotEqual(shared_stamp.read_bytes(), orchestrator.CONDUCTOR_STAMP.read_bytes())
        self.assertNotEqual(shared_empty.read_bytes(), orchestrator.PRE_ACCEPT_EMPTY.read_bytes())
        snapshot = orchestrator.frozen_output_snapshot()
        self.assertIsNone(snapshot['frozen.results'])
        self.assertIsNone(snapshot['empty.pnl'])
        self.assertIsNone(snapshot['empty.sf1_median_half_spread_bps_by_mid_decile'])
        self.assertIsNone(snapshot['empty.n_books'])
        self.assertIsNone(snapshot['empty.n_snapshots'])
        published = orchestrator.published_scorecard()
        orchestrator.assert_null_scorecard(published)
        self.assertEqual(orchestrator.load_scorecard(orchestrator.EMPTY_RESULTS)['status'], 'EMPTY_RESULTS_PRE_EXAMINER')

    def test_arms_keep_the_natural_panel_and_prefer_admitted(self):
        self.assertEqual(orchestrator.select_panel_path(), orchestrator.PANEL_STUB)
        panel = orchestrator.load_panel()
        books = {row['ticker']: row for row in orchestrator.load_orderbooks()}
        sf1 = orchestrator.conduct(orchestrator.R3P4S0, panel)
        sf2 = orchestrator.conduct(orchestrator.R3P4S1, panel)
        self.assertEqual(sf1['shape_object'], 'sf1_half_spread')
        self.assertEqual(sf2['shape_object'], 'sf2_depth_kl')
        self.assertEqual(sf1['market_count'], 6)
        self.assertEqual(sf2['market_count'], 6)
        self.assertEqual(sf1['event_count'], 4)
        self.assertIs(sf1['category_slice_is_arm'], False)
        self.assertEqual(sf1['two_sided_recorded_n'], 2)
        self.assertEqual(sf1['one_sided_recorded_n'], 4)
        for report in (sf1, sf2):
            orchestrator.assert_null_scorecard(report)
            self.assertIs(report['schema_scored'], False)
            self.assertIs(report['production_depth_scored'], False)
            self.assertEqual(report['panel_note'], 'recorded_books_not_promoted')
            self.assertEqual(
                {row['category_slice'] for row in report['markets']},
                {'sports', 'non_sports'},
            )
        by_ticker = {row['market_ticker']: row for row in sf1['markets']}
        for ticker in (
            'KXNCAAFGAME-26SEP26TEXTENN-TENN',
            'KXNCAAFGAME-26SEP26PREMRST-MRST',
        ):
            slot = by_ticker[ticker]
            book = books[ticker]['orderbook_fp']
            quote = orchestrator.shape.quoted_yes(book)
            self.assertIs(slot['schema_scored'], True)
            self.assertIs(slot['two_sided'], True)
            self.assertEqual(slot['schema_half_spread_bps'], quote['half_spread_bps'])
            self.assertEqual(slot['schema_decile'], quote['decile'])
            self.assertNotIn('schema_kl_nats', slot)
        sf2_by_ticker = {row['market_ticker']: row for row in sf2['markets']}
        for ticker in (
            'KXNCAAFGAME-26SEP26TEXTENN-TENN',
            'KXNCAAFGAME-26SEP26PREMRST-MRST',
        ):
            slot = sf2_by_ticker[ticker]
            depth = orchestrator.shape.top10_depth(books[ticker]['orderbook_fp'])
            self.assertEqual(slot['schema_l1_share'], depth['l1_share'])
            self.assertEqual(slot['schema_kl_nats'], depth['kl_nats'])
            self.assertNotIn('schema_half_spread_bps', slot)
        pitt = by_ticker['KXNCAAFGAME-26SEP26BUCKPITT-PITT']
        buck = by_ticker['KXNCAAFGAME-26SEP26BUCKPITT-BUCK']
        btc = sf2_by_ticker['KXBTC-26SEP2317-T76250']
        self.assertEqual(pitt['no_levels'], 0)
        self.assertGreater(pitt['yes_levels'], 0)
        self.assertEqual(buck['yes_levels'], 0)
        self.assertGreater(buck['no_levels'], 0)
        self.assertIs(pitt['missing_side_not_invented'], True)
        self.assertIs(btc['schema_scored'], False)
        self.assertIs(pitt['schema_scored'], False)
        with self.assertRaises(feebook.BookIncomplete):
            orchestrator.shape.quoted_yes(books['KXNCAAFGAME-26SEP26BUCKPITT-PITT']['orderbook_fp'])
        stamped = json.loads(orchestrator.PANEL_STUB.read_text())
        stamped['admitted_at'] = '2026-09-23T18:00:00Z'
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            stub = root / 'panel_stub.json'
            admitted = root / 'panel_admitted.json'
            stub.write_text(orchestrator.PANEL_STUB.read_text())
            admitted.write_text(json.dumps(stamped))
            self.assertEqual(orchestrator.select_panel_path(stub, admitted), admitted)
            loaded = orchestrator.load_panel(stub, admitted)
            self.assertEqual(loaded['admitted_at'], '2026-09-23T18:00:00Z')
            self.assertEqual(len(loaded['markets']), 6)

    def test_pinned_labs_are_unmodified(self):
        for commit, path in (
            (orchestrator.FEEBOOK_COMMIT, 'kalshi_feebook_lab_20260922'),
            (orchestrator.RAILS_COMMIT, 'kalshi_rails_lab_20260922'),
        ):
            diff = subprocess.run(
                ['git', 'diff', '--exit-code', commit, '--', path],
                cwd=PARENT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(diff.returncode, 0, diff.stdout + diff.stderr)
            ancestor = subprocess.run(
                ['git', 'merge-base', '--is-ancestor', commit, 'HEAD'],
                cwd=PARENT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(ancestor.returncode, 0, ancestor.stderr)
        for path in orchestrator.DOES_NOT_MODIFY:
            diff = subprocess.run(
                ['git', 'diff', '--exit-code', orchestrator.BASE_COMMIT, '--', path],
                cwd=PARENT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(diff.returncode, 0, path + diff.stdout + diff.stderr)


class SchemaTests(unittest.TestCase):
    def test_panel_arms_do_not_promote_recorded_books(self):
        before = {path: path.read_bytes() for path in _freeze_paths()}
        sf1 = orchestrator.conduct(orchestrator.R3P4S0)
        sf2 = orchestrator.conduct(orchestrator.R3P4S1)
        self.assertEqual(sf1['fee_pin'], sf2['fee_pin'])
        with self.assertRaises(orchestrator.ScorecardPromotionRefused):
            orchestrator.score_recorded_orderbook(orchestrator.load_panel()['markets'][0])
        with self.assertRaises(orchestrator.ScorecardPromotionRefused):
            orchestrator.publish_shape_metric('sf1_half_spread', Decimal('200'))
        with self.assertRaises(orchestrator.ScorecardPromotionRefused):
            orchestrator.write_scorecard(sf1['published'])
        with self.assertRaises(orchestrator.CategorySliceNotAnArm):
            orchestrator.conduct('R3P4C0')
        with self.assertRaises(orchestrator.CategorySliceNotAnArm):
            orchestrator.conduct('sports_only')
        with self.assertRaises(orchestrator.UnknownShape):
            orchestrator.conduct('R3P4S2')
        for path, raw in before.items():
            self.assertEqual(path.read_bytes(), raw)

    def test_synthetic_ladders_stay_out_of_the_scorecard(self):
        before = {path: path.read_bytes() for path in _freeze_paths()}
        sf1 = orchestrator.conduct_synthetic(orchestrator.R3P4S0)
        sf2 = orchestrator.conduct_synthetic(orchestrator.R3P4S1)
        self.assertEqual(sf1['source'], 'synthetic_schema_standin')
        self.assertIs(sf1['schema_scored'], True)
        self.assertIs(sf1['production_depth_scored'], False)
        self.assertIs(sf1['category_filtered'], False)
        self.assertEqual(sf1['book_count'], 2)
        self.assertEqual(sf2['book_count'], 2)
        self.assertEqual(
            {row['category_slice'] for row in sf1['books']},
            {'sports', 'non_sports'},
        )
        for row in sf1['books']:
            self.assertEqual(row['schema_half_spread_bps'], Decimal('200'))
            self.assertEqual(row['schema_decile'], 5)
            self.assertEqual(row['schema_mid'], Decimal('0.50'))
            self.assertNotIn('schema_kl_nats', row)
        for row in sf2['books']:
            self.assertEqual(row['schema_l1_share'], Fraction(1, 10))
            self.assertEqual(row['schema_kl_nats'], Decimal('0'))
            self.assertNotIn('schema_half_spread_bps', row)
        for report in (sf1, sf2):
            orchestrator.assert_null_scorecard(report)
            self.assertIsNone(report['sf1_median_half_spread_bps_by_mid_decile'])
            self.assertIsNone(report['sf2_l1_top10_depth_share'])
            self.assertIsNone(report['sf2_kl_vs_uniform_1_10'])
            self.assertIsNone(report['n_books'])
            self.assertIsNone(report['n_snapshots'])
            self.assertIsNone(report['results'])
            self.assertIsNone(report['pnl'])
        for path, raw in before.items():
            self.assertEqual(path.read_bytes(), raw)


class RefuseTests(unittest.TestCase):
    def test_invented_depth_lee_ready_recreations_and_reopens_are_refused(self):
        for label in (
            'invented_depth',
            'invent_depth',
            'lee_ready',
            'atl_gb',
            'live_orders',
            'logan_keys',
            'invented_pnl',
            'invented_fills',
            'invent_fills',
            'invented_markets',
            'q6_retune',
            '000',
            'qf_reopen',
            'cap_sr_reopen',
            'cap_sr_fx_reopen',
            'l2_cat_reopen',
            'empty_ob_reopen',
            'prop_lq_reopen',
            'sot_id_reopen',
            'pr13_dual_edit',
            'admit_py',
            'ungate_s2_r2p4',
            'completed_profit',
            'category_slice_arm',
        ):
            with self.assertRaises(orchestrator.OrchestratorError):
                orchestrator.refuse_adversary(label)
        with self.assertRaises(orchestrator.LeeReadyRefused):
            orchestrator.infer_lee_ready({'side': 'buy'})
        with self.assertRaises(orchestrator.InventedDepthRefused):
            orchestrator.fill_missing_side({'yes_dollars': [], 'no_dollars': [['0.40', '1']]})
        with self.assertRaises(orchestrator.InventFillRefused):
            orchestrator.attempt_fill({'orderbook_fp': {}}, 'yes', 1)
        with self.assertRaises(orchestrator.UngateRefused):
            orchestrator.ungate_s2_r2p4()
        with self.assertRaises(orchestrator.Pr13DualEditRefused):
            orchestrator.dual_edit_pr13()
        with self.assertRaises(orchestrator.ExaminerNotReady):
            orchestrator.stamp_examiner_ready()
        with self.assertRaises(orchestrator.LiveOrdersForbidden):
            orchestrator.execution_adapter()
        with self.assertRaises(orchestrator.LiveOrdersForbidden):
            orchestrator.fetch_over_network('https://api.elections.kalshi.com')
        with self.assertRaises(orchestrator.LiveOrdersForbidden):
            orchestrator.assert_public_get('POST')
        self.assertIsNone(orchestrator.assert_public_get('GET'))
        with self.assertRaises(orchestrator.PreAcceptEmptyRefused):
            orchestrator.load_scorecard(orchestrator.PRE_ACCEPT_EMPTY)
        with self.assertRaises(orchestrator.EmptyBookRefused):
            orchestrator.side_status({'yes_dollars': [], 'no_dollars': []})
        one_sided = {
            'book_id': 'synthetic:flat10:missing',
            'category_slice': 'sports',
            'depth_source': 'synthetic_schema_standin',
            'invent_depth': False,
            'lee_ready': 'REFUSED',
            'transaction_time': 't0',
            'keepalive': False,
            'orderbook_fp': {'yes_dollars': [['0.40', '10']], 'no_dollars': []},
        }
        with self.assertRaises(orchestrator.InventedDepthRefused):
            orchestrator.schema_book(orchestrator.R3P4S0, one_sided)
        stale = dict(orchestrator.load_synthetic_ladder()[0])
        stale['keepalive'] = True
        with self.assertRaises(orchestrator.shape.StaleSnapshotRefused):
            orchestrator.schema_book(orchestrator.R3P4S1, stale)
        source = (ROOT / 'orchestrator.py').read_text()
        for banned in (
            '0.0175',
            '0.07',
            'urlopen',
            'urllib',
            'os.environ',
            'api_key',
            'private_key',
            'import queue_fragility',
            'import admit',
            'class KalshiExecutionAdapter',
            'subprocess',
        ):
            self.assertNotIn(banned, source)
        panel = json.loads(orchestrator.PANEL_STUB.read_text())
        panel['markets'] = panel['markets'][:-1]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'panel_stub.json'
            path.write_text(json.dumps(panel))
            with self.assertRaises(orchestrator.RecreationRefused):
                orchestrator.load_panel(path, Path(tmp) / 'missing.json')
        panel = json.loads(orchestrator.PANEL_STUB.read_text())
        panel['markets'] = []
        panel['events'] = []
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'panel_stub.json'
            path.write_text(json.dumps(panel))
            with self.assertRaises(orchestrator.EmptySeedRefused):
                orchestrator.load_panel(path, Path(tmp) / 'missing.json')
        panel = json.loads(orchestrator.PANEL_STUB.read_text())
        panel['freeze_packet_sha256'] = 'e7c6b6d5' + ('b' * 56)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'panel_stub.json'
            path.write_text(json.dumps(panel))
            with self.assertRaises(orchestrator.SupersededDigestRefused):
                orchestrator.load_panel(path, Path(tmp) / 'missing.json')
        panel = json.loads(orchestrator.PANEL_STUB.read_text())
        panel['panel_version'] = '2026-09-22.r3-p4-l2-shape-v1'
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'panel_stub.json'
            path.write_text(json.dumps(panel))
            with self.assertRaises(orchestrator.PanelVersionRefused):
                orchestrator.load_panel(path, Path(tmp) / 'missing.json')
        panel = json.loads(orchestrator.PANEL_STUB.read_text())
        panel['markets'][0]['market_ticker'] = 'KXNCAAFGAME-26SEP24ATLGB-ATL'
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'panel_stub.json'
            path.write_text(json.dumps(panel))
            with self.assertRaises(orchestrator.AtlGbRefused):
                orchestrator.load_panel(path, Path(tmp) / 'missing.json')
        grok = feebook.grok_unrounded_maker_per_unit('0.50')
        with self.assertRaises(orchestrator.ShadowFeeLiteralRefused):
            orchestrator.assert_examiner_quote(grok)
        filled = dict(orchestrator.published_scorecard())
        filled['sf2_kl_vs_uniform_1_10'] = Decimal('1')
        with self.assertRaises(orchestrator.ScorecardPromotionRefused):
            orchestrator.write_scorecard(filled)


if __name__ == '__main__':
    unittest.main()
