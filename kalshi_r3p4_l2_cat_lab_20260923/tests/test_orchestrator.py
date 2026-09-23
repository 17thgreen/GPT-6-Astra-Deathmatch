"""Unit pins for the R3-P4 L2-CAT category-slice harness.

Schema and pin locks only. In-memory synthetic ladders are not a score and
they are not profit. Freeze outputs stay null. The subject is the panel stub
until panel_admitted.json appears.
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
        orchestrator.KERNEL,
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
        self.assertFalse(orchestrator.LIVE_GET_DIR.exists())
        binding = orchestrator.instrument_binding()
        panel = orchestrator.load_panel()
        frozen = json.loads(orchestrator.FROZEN_EXPERIMENT.read_text())
        stamp = json.loads(orchestrator.CONDUCTOR_STAMP.read_text())
        self.assertEqual(binding['experiment_id'], 'R3-P4-L2-CAT-HARNESS')
        self.assertEqual(binding['feature_family'], 'L2-CAT')
        self.assertEqual(frozen['feature_family'], 'L2-CAT')
        self.assertEqual(stamp['feature_family'], 'L2-CAT')
        self.assertEqual(binding['knob'], 'category_slice')
        self.assertEqual(frozen['knob'], 'category_slice')
        self.assertEqual(binding['panel_version'], '2026-09-22.r3-p4-l2-shape-v0')
        self.assertEqual(panel['panel_version'], '2026-09-22.r3-p4-l2-shape-v0')
        self.assertIsNone(panel['admitted_at'])
        self.assertIsNone(binding['admitted_at'])
        self.assertEqual(binding['events_n'], 4)
        self.assertEqual(binding['markets_n'], 6)
        self.assertEqual(len(panel['events']), 4)
        self.assertEqual(len(panel['markets']), 6)
        self.assertEqual(stamp['panel_events'], 4)
        self.assertEqual(stamp['panel_markets'], 6)
        self.assertEqual(panel['cohort_summary']['sports_n'], 4)
        self.assertEqual(panel['cohort_summary']['non_sports_n'], 2)
        self.assertEqual(panel['freeze_packet_sha256'], orchestrator.KERNEL_SHA256)
        self.assertEqual(binding['feebook_commit'], frozen['fee_pin'])
        self.assertEqual(binding['rails_commit'], frozen['rails_pin'])
        self.assertEqual(binding['feebook_commit'], '22371178cb2663250b4762f328069571c48cb551')
        self.assertEqual(binding['rails_commit'], '6a28e0d6254327ea4e6451c781bec56215ac6cac')
        self.assertEqual(binding['examiner_formula_id'], feebook.EXAMINER_FORMULA_ID)
        self.assertEqual(binding['fee_credit_rule_id'], rails.FEE_CREDIT_RULE_ID)
        self.assertEqual(binding['fee_source'], 'feebook')
        self.assertEqual(binding['rails_source'], 'rails')
        self.assertEqual(binding['shape_source'], 'kalshi_r3_p4_l2_shape_lab_20260922')
        self.assertEqual(binding['lee_ready'], 'REFUSED')
        self.assertEqual(binding['atl_gb'], 'REFUSED')
        self.assertEqual(binding['invented_depth'], 'REFUSED')
        self.assertIs(binding['probe_scorecard_write'], False)
        self.assertIs(binding['live_get_present'], False)
        self.assertIsNone(binding['strategy_pointer'])
        self.assertIs(binding['logan_keys_required'], False)
        self.assertIs(binding['live_orders'], False)
        self.assertIs(binding['signal_retune_000'], False)
        self.assertIs(binding['queue_fragility_reopen'], False)
        self.assertIs(binding['cap_sr_reopen'], False)
        self.assertIs(binding['cap_sr_fx_reopen'], False)
        self.assertIs(binding['admit_py_run'], False)
        self.assertIs(binding['fee_is_knob'], False)
        self.assertIs(binding['base_lab_mutated'], False)
        self.assertEqual(binding['dead_cards'], orchestrator.DEAD_CARDS)
        self.assertEqual(tuple(frozen['scorecard_fields']), orchestrator.SCORECARD_FIELDS)
        self.assertEqual([arm['id'] for arm in frozen['arms']], list(orchestrator.ARMS))
        self.assertEqual(frozen['arms'][0]['category_slice'], 'sports_only')
        self.assertEqual(frozen['arms'][1]['category_slice'], 'nonsports_only')
        self.assertEqual(stamp['arms'], ['R3P4C0', 'R3P4C1'])
        self.assertEqual(
            orchestrator.sha256_file(orchestrator.PACKET),
            '3fc370d93f0ea42864f7bf482d7f6515254999c76e2fc4477df1273bfcdc051f',
        )
        self.assertEqual(
            orchestrator.sha256_file(orchestrator.KERNEL),
            '4a4e7cc61efcb436955c566edc7a2681603a014725bc79047f9d825392064528',
        )
        self.assertEqual(
            orchestrator.sha256_file(orchestrator.PANEL_STUB),
            '7477e023ab70c59a6739650155ddb9d77077766e3afd80443e540d60b5a86cbb',
        )
        self.assertEqual(
            orchestrator.sha256_file(orchestrator.SEED_SUMMARY),
            'e0d5281133d89d5f0215a8f02ae438b688bf53e4a48f2eb4c3727db4a29bb6f2',
        )
        self.assertFalse(orchestrator.PACKET_SHA256.startswith('e7c6b6d5'))
        self.assertFalse(orchestrator.KERNEL_SHA256.startswith('e7c6b6d5'))
        self.assertFalse(orchestrator.PANEL_STUB_SHA256.startswith('e7c6b6d5'))
        self.assertEqual(orchestrator.PACKET_SHA256, orchestrator.CONDUCTOR_PACKET_SHA256)
        self.assertEqual(orchestrator.KERNEL_SHA256, orchestrator.CONDUCTOR_KERNEL_SHA256)
        self.assertEqual(orchestrator.PANEL_STUB_SHA256, orchestrator.CONDUCTOR_PANEL_STUB_SHA256)
        pins = orchestrator.conductor_pin_status()
        self.assertIs(pins['packet_matches_conductor_claim'], True)
        self.assertIs(pins['kernel_matches_conductor_claim'], True)
        self.assertIs(pins['panel_stub_matches_conductor_claim'], True)
        self.assertIs(pins['conductor_bytes_in_checkout'], True)
        self.assertEqual(pins['events_n_claim'], 4)
        self.assertEqual(pins['markets_n_claim'], 6)
        self.assertEqual(pins['sports_n_claim'], 4)
        self.assertEqual(pins['nonsports_n_claim'], 2)
        self.assertIs(pins['live_get_present'], False)
        self.assertIsNone(frozen['results'])
        self.assertIsNone(frozen['pnl'])
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
        self.assertEqual(
            Path(orchestrator.hygiene.__file__).resolve().parent.name,
            'kalshi_r2p1_hygiene_000_lab_20260922',
        )

    def test_packet_copies_match_and_scorecard_stays_null(self):
        frozen_bytes = orchestrator.FROZEN_EXPERIMENT.read_bytes()
        empty_bytes = orchestrator.EMPTY_RESULTS.read_bytes()
        packet_bytes = orchestrator.PACKET.read_bytes()
        kernel_bytes = orchestrator.KERNEL.read_bytes()
        stub_bytes = orchestrator.PANEL_STUB.read_bytes()
        for path in (
            orchestrator.PACKET,
            orchestrator.LAB_BUNDLE / orchestrator.PACKET_NAME,
            PARENT / 'packets' / orchestrator.PACKET_NAME,
            orchestrator.GOVERNANCE_BUNDLE / orchestrator.PACKET_NAME,
        ):
            self.assertEqual(path.read_bytes(), packet_bytes)
        for path in (
            orchestrator.KERNEL,
            orchestrator.LAB_BUNDLE / orchestrator.KERNEL_NAME,
            PARENT / 'packets' / orchestrator.KERNEL_NAME,
            orchestrator.GOVERNANCE_BUNDLE / orchestrator.KERNEL_NAME,
        ):
            self.assertEqual(path.read_bytes(), kernel_bytes)
        for path in (
            orchestrator.PANEL_STUB,
            orchestrator.LAB_BUNDLE / 'panel_stub.json',
            orchestrator.GOVERNANCE_BUNDLE / 'panel_stub.json',
        ):
            self.assertEqual(path.read_bytes(), stub_bytes)
        for path in (
            orchestrator.FROZEN_EXPERIMENT,
            orchestrator.LAB_BUNDLE / 'FROZEN_EXPERIMENT.json',
            orchestrator.GOVERNANCE_BUNDLE / 'FROZEN_EXPERIMENT.json',
        ):
            self.assertEqual(path.read_bytes(), frozen_bytes)
            payload = json.loads(path.read_text())
            self.assertIsNone(payload['results'])
            self.assertIsNone(payload['pnl'])
            self.assertEqual(payload['lee_ready'], 'REFUSED')
            self.assertEqual(payload['invented_depth'], 'REFUSED')
            self.assertIsNone(payload['admitted_at'])
        for path in (
            orchestrator.EMPTY_RESULTS,
            orchestrator.LAB_BUNDLE / 'results.json',
            orchestrator.GOVERNANCE_BUNDLE / 'results.json',
            orchestrator.GOVERNANCE_BUNDLE / 'results' / 'EMPTY_RESULTS.json',
        ):
            self.assertEqual(path.read_bytes(), empty_bytes)
            payload = json.loads(path.read_text())
            self.assertEqual(payload['status'], 'EMPTY_RESULTS_PRE_EXAMINER')
            for key in orchestrator.OUTPUT_KEYS:
                self.assertIsNone(payload[key])
        snapshot = orchestrator.frozen_output_snapshot()
        self.assertIsNone(snapshot['frozen.results'])
        self.assertIsNone(snapshot['empty.pnl'])
        self.assertIsNone(snapshot['empty.sf1_median_half_spread_bps_by_mid_decile'])
        self.assertIsNone(snapshot['empty.n_books'])
        self.assertIsNone(snapshot['empty.n_snapshots'])
        published = orchestrator.published_scorecard()
        orchestrator.assert_null_scorecard(published)
        self.assertEqual(published['status'], 'EMPTY_RESULTS_PRE_EXAMINER')

    def test_stub_partitions_and_prefers_admitted(self):
        self.assertEqual(orchestrator.select_panel_path(), orchestrator.PANEL_STUB)
        panel = orchestrator.load_panel()
        self.assertEqual(
            [market['market_ticker'] for market in panel['markets']],
            list(orchestrator.STUB_MARKETS),
        )
        self.assertEqual(panel['cohort_summary']['orderbook_ok_n'], 6)
        for market in panel['markets']:
            self.assertIsNone(market['half_spread_bps'])
            self.assertIsNone(market['l2_shape'])
            self.assertIsNone(market['volume_fp'])
            self.assertTrue(market['raw_orderbook']['captured_via'].startswith('GET '))
        sports = orchestrator.conduct(orchestrator.R3P4C0, panel)
        nonsports = orchestrator.conduct(orchestrator.R3P4C1, panel)
        self.assertEqual(sports['category_slice'], 'sports_only')
        self.assertEqual(sports['slice'], 'sports')
        self.assertEqual(sports['market_count'], 4)
        self.assertEqual(sports['event_count'], 3)
        self.assertEqual(sports['recorded_orderbook_n'], 4)
        self.assertEqual(nonsports['category_slice'], 'nonsports_only')
        self.assertEqual(nonsports['slice'], 'non_sports')
        self.assertEqual(nonsports['market_count'], 2)
        self.assertEqual(nonsports['event_count'], 1)
        self.assertEqual(nonsports['recorded_orderbook_n'], 2)
        self.assertEqual(
            [row['market_ticker'] for row in nonsports['markets']],
            list(orchestrator.NONSPORTS_MARKETS),
        )
        for report in (sports, nonsports):
            orchestrator.assert_null_scorecard(report)
            self.assertIs(report['schema_scored'], False)
            self.assertIs(report['production_depth_scored'], False)
            self.assertEqual(report['source'], 'panel')
            self.assertEqual(report['panel_note'], 'recorded_books_not_scored')
            self.assertIsNone(report['n_books'])
            self.assertIsNone(report['n_snapshots'])
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
            admitted.unlink()
            self.assertEqual(orchestrator.select_panel_path(stub, admitted), stub)

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
    def test_panel_arms_do_not_score_recorded_books(self):
        before = {path: path.read_bytes() for path in _freeze_paths()}
        sports = orchestrator.conduct(orchestrator.R3P4C0)
        nonsports = orchestrator.conduct(orchestrator.R3P4C1)
        self.assertEqual(sports['fee_pin'], nonsports['fee_pin'])
        self.assertEqual(sports['rails_pin'], nonsports['rails_pin'])
        self.assertIs(sports['schema_scored'], False)
        self.assertIs(nonsports['schema_scored'], False)
        with self.assertRaises(orchestrator.ScorecardPromotionRefused):
            orchestrator.score_recorded_orderbook(orchestrator.load_panel()['markets'][0])
        with self.assertRaises(orchestrator.ScorecardPromotionRefused):
            orchestrator.publish_category_gap(Decimal('200'), Decimal('1'))
        with self.assertRaises(orchestrator.ScorecardPromotionRefused):
            orchestrator.write_scorecard(sports['published'])
        with self.assertRaises(orchestrator.UnknownSlice):
            orchestrator.conduct('R3P4C2')
        for path, raw in before.items():
            self.assertEqual(path.read_bytes(), raw)

    def test_synthetic_ladders_stay_out_of_the_scorecard(self):
        before = {path: path.read_bytes() for path in _freeze_paths()}
        sports = orchestrator.conduct_synthetic(orchestrator.R3P4C0)
        nonsports = orchestrator.conduct_synthetic(orchestrator.R3P4C1)
        self.assertEqual(sports['source'], 'synthetic_schema_standin')
        self.assertEqual(nonsports['source'], 'synthetic_schema_standin')
        self.assertIs(sports['schema_scored'], True)
        self.assertIs(sports['production_depth_scored'], False)
        self.assertIs(sports['public_tape'], False)
        self.assertEqual(sports['book_count'], 1)
        self.assertEqual(nonsports['book_count'], 1)
        sports_row = sports['books'][0]
        nonsports_row = nonsports['books'][0]
        self.assertEqual(sports_row['book_id'], 'synthetic:sports:flat10')
        self.assertEqual(sports_row['schema_half_spread_bps'], Decimal('200'))
        self.assertEqual(sports_row['schema_decile'], 5)
        self.assertEqual(sports_row['schema_mid'], Decimal('0.50'))
        self.assertEqual(sports_row['schema_l1_share'], Fraction(1, 10))
        self.assertEqual(sports_row['schema_kl_nats'], Decimal('0'))
        self.assertEqual(nonsports_row['book_id'], 'synthetic:nonsports:touch')
        self.assertEqual(nonsports_row['schema_mid'], Decimal('0.35'))
        self.assertEqual(nonsports_row['schema_decile'], 3)
        self.assertEqual(
            nonsports_row['schema_half_spread_bps'],
            Decimal('0.05') / Decimal('0.35') * Decimal('10000'),
        )
        self.assertEqual(nonsports_row['schema_l1_share'], Fraction(1))
        self.assertEqual(nonsports_row['schema_kl_nats'], Decimal(10).ln())
        for report in (sports, nonsports):
            orchestrator.assert_null_scorecard(report)
            self.assertIsNone(report['sf1_median_half_spread_bps_by_mid_decile'])
            self.assertIsNone(report['sf2_l1_top10_depth_share'])
            self.assertIsNone(report['sf2_kl_vs_uniform_1_10'])
            self.assertIsNone(report['sports_vs_nonsports_sf_gap'])
            self.assertIsNone(report['n_books'])
            self.assertIsNone(report['n_snapshots'])
            self.assertIsNone(report['results'])
            self.assertIsNone(report['pnl'])
        for path, raw in before.items():
            self.assertEqual(path.read_bytes(), raw)


class RefuseTests(unittest.TestCase):
    def test_invented_depth_lee_ready_recreations_and_atl_are_refused(self):
        for label in (
            'invented_depth',
            'lee_ready',
            'atl_gb',
            'live_orders',
            'logan_keys',
            'invented_pnl',
            'invented_fills',
            'invented_markets',
            'q6_retune',
            '000',
            'qf_reopen',
            'cap_sr_reopen',
            'cap_sr_fx_reopen',
            'admit_py',
            'completed_profit',
        ):
            with self.assertRaises(orchestrator.OrchestratorError):
                orchestrator.refuse_adversary(label)
        with self.assertRaises(orchestrator.InventedDepthRefused):
            orchestrator.refuse_adversary('invented_depth')
        with self.assertRaises(orchestrator.LeeReadyRefused):
            orchestrator.infer_lee_ready({'side': 'buy'})
        with self.assertRaises(orchestrator.LiveOrdersForbidden):
            orchestrator.execution_adapter()
        with self.assertRaises(orchestrator.LiveOrdersForbidden):
            orchestrator.assert_public_get('POST')
        self.assertIsNone(orchestrator.assert_public_get('GET'))
        with self.assertRaises(orchestrator.LiveOrdersForbidden):
            orchestrator.assert_route('POST /portfolio/orders')
        self.assertIsNone(orchestrator.assert_route('GET /markets/{ticker}/orderbook'))
        with self.assertRaises(orchestrator.InventedDepthRefused):
            orchestrator.materialize_live_get()
        with self.assertRaises(orchestrator.InventedDepthRefused):
            orchestrator.classify_depth({'invent_depth': True, 'depth_source': 'recorded_fixture'})
        with self.assertRaises(orchestrator.InventedDepthRefused):
            orchestrator.classify_depth({'depth_source': 'invented'})
        self.assertEqual(
            orchestrator.classify_depth({'depth_source': 'recorded_fixture'}),
            'recorded_fixture',
        )
        with self.assertRaises(orchestrator.SupersededDigestRefused):
            orchestrator.assert_not_superseded('e7c6b6d5' + ('a' * 56))
        one_sided = {
            'book_id': 'synthetic:sports:missing',
            'category_slice': 'sports',
            'depth_source': 'synthetic_schema_standin',
            'invent_depth': False,
            'lee_ready': 'REFUSED',
            'transaction_time': 't0',
            'keepalive': False,
            'orderbook_fp': {'yes_dollars': [['0.40', '10']], 'no_dollars': []},
        }
        with self.assertRaises(orchestrator.InventedDepthRefused):
            orchestrator.schema_book(one_sided)
        stale = dict(orchestrator.load_synthetic_ladder()[0])
        stale['keepalive'] = True
        with self.assertRaises(orchestrator.shape.StaleSnapshotRefused):
            orchestrator.schema_book(stale)
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
        panel['binds']['no_lee_ready'] = False
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'panel_stub.json'
            path.write_text(json.dumps(panel))
            with self.assertRaises(orchestrator.LeeReadyRefused):
                orchestrator.load_panel(path, Path(tmp) / 'missing.json')
        panel = json.loads(orchestrator.PANEL_STUB.read_text())
        panel['markets'][0]['market_ticker'] = 'KXNCAAFGAME-26SEP24ATLGB-ATL'
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'panel_stub.json'
            path.write_text(json.dumps(panel))
            with self.assertRaises(orchestrator.AtlGbRefused):
                orchestrator.load_panel(path, Path(tmp) / 'missing.json')
        panel = json.loads(orchestrator.PANEL_STUB.read_text())
        panel['binds']['forbid_inherited_q7_fee_literals'] = False
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'panel_stub.json'
            path.write_text(json.dumps(panel))
            with self.assertRaises(orchestrator.ShadowFeeLiteralRefused):
                orchestrator.load_panel(path, Path(tmp) / 'missing.json')
        grok = feebook.grok_unrounded_maker_per_unit('0.50')
        with self.assertRaises(orchestrator.ShadowFeeLiteralRefused):
            orchestrator.assert_examiner_quote(grok)
        filled = dict(orchestrator.published_scorecard())
        filled['sf2_l1_top10_depth_share'] = Decimal('1')
        with self.assertRaises(orchestrator.ScorecardPromotionRefused):
            orchestrator.write_scorecard(filled)


if __name__ == '__main__':
    unittest.main()
