"""Unit pins for the S5 KXMVECROSSCATEGORY fill-vs-legs harness.

Schema and pin locks only. In-memory helper calls are not a score and they
are not profit. Freeze outputs stay null. The subject is the panel stub
until panel_admitted.json appears.
"""
import json
import subprocess
import sys
import tempfile
import unittest
from decimal import Decimal
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
        binding = orchestrator.instrument_binding()
        panel = orchestrator.load_panel()
        frozen = json.loads(orchestrator.FROZEN_EXPERIMENT.read_text())
        self.assertEqual(binding['experiment_id'], 'S5-KXMVECROSSCATEGORY-FILLLEGS-HARNESS')
        self.assertEqual(binding['feature_family'], 'MVE-FL')
        self.assertEqual(frozen['feature_family'], 'MVE-FL')
        self.assertEqual(binding['knob'], 'leg_mid_source')
        self.assertEqual(frozen['knob'], 'leg_mid_source')
        self.assertEqual(binding['panel_version'], '2026-09-22.s5-kxmvecrosscategory-v0')
        self.assertEqual(panel['panel_version'], '2026-09-22.s5-kxmvecrosscategory-v0')
        self.assertIsNone(panel['admitted_at'])
        self.assertIsNone(binding['admitted_at'])
        self.assertEqual(binding['feebook_commit'], frozen['fee_pin'])
        self.assertEqual(binding['rails_commit'], frozen['rails_pin'])
        self.assertEqual(binding['feebook_commit'], '22371178cb2663250b4762f328069571c48cb551')
        self.assertEqual(binding['rails_commit'], '6a28e0d6254327ea4e6451c781bec56215ac6cac')
        self.assertEqual(binding['fee_type_series_override'], 'quadratic_with_combo_maker_fees')
        self.assertEqual(frozen['fee_series_override'], 'quadratic_with_combo_maker_fees')
        self.assertEqual(binding['combo_series_resolution'], 'override')
        self.assertEqual(binding['examiner_formula_id'], feebook.EXAMINER_FORMULA_ID)
        self.assertEqual(binding['fee_credit_rule_id'], rails.FEE_CREDIT_RULE_ID)
        self.assertEqual(binding['fee_source'], 'feebook')
        self.assertEqual(binding['rails_source'], 'rails')
        self.assertEqual(binding['probe_formula_id'], feebook.EXAMINER_FORMULA_ID)
        self.assertIs(binding['probe_scorecard_write'], False)
        self.assertNotIn('fee_delta', binding)
        self.assertNotIn('fill_vs_legs_mid_gap', binding)
        self.assertIsNone(binding['strategy_pointer'])
        self.assertIs(binding['rfq_in_scope'], False)
        self.assertIs(frozen['rfq_in_scope'], False)
        self.assertIs(binding['r1p4_strategy_open'], False)
        self.assertIs(frozen['r1p4_strategy_open'], False)
        self.assertIs(binding['logan_keys_required'], False)
        self.assertIs(frozen['logan_keys_required'], False)
        self.assertIs(binding['live_orders'], False)
        self.assertIs(binding['signal_retune_000'], False)
        self.assertIs(frozen['signal_retune_000'], False)
        self.assertIs(binding['queue_fragility_reopen'], False)
        self.assertIs(frozen['queue_fragility_reopen'], False)
        self.assertIs(binding['cap_sr_reopen'], False)
        self.assertIs(binding['admit_py_run'], False)
        self.assertIs(binding['fee_is_knob'], False)
        self.assertEqual(binding['dead_cards'], orchestrator.DEAD_CARDS)
        self.assertEqual(binding['queued_behind'], ('S4_NCAAF', 'R2-P3_prop_slate'))
        self.assertEqual(tuple(frozen['scorecard_fields']), orchestrator.SCORECARD_FIELDS)
        self.assertEqual([arm['id'] for arm in frozen['arms']], list(orchestrator.ARMS))
        self.assertEqual(frozen['arms'][0]['leg_mid_source'], 'tob_1m')
        self.assertEqual(frozen['arms'][1]['leg_mid_source'], 'synthetic_leg_product')
        self.assertIsNone(frozen['results'])
        self.assertIsNone(frozen['pnl'])
        self.assertEqual(binding['packet_sha256'], orchestrator.PACKET_SHA256)
        self.assertEqual(binding['kernel_sha256'], orchestrator.KERNEL_SHA256)
        self.assertEqual(binding['panel_stub_sha256'], orchestrator.PANEL_STUB_SHA256)
        self.assertEqual(
            orchestrator.sha256_file(orchestrator.PANEL_STUB),
            orchestrator.PANEL_STUB_SHA256,
        )
        self.assertEqual(
            sorted(path.name for path in PARENT.glob('kalshi_s5_mve_filllegs_lab_*')),
            ['kalshi_s5_mve_filllegs_lab_20260923'],
        )
        self.assertEqual(Path(feebook.__file__).resolve().parent.name, 'kalshi_feebook_lab_20260922')
        self.assertEqual(Path(rails.__file__).resolve().parent.name, 'kalshi_rails_lab_20260922')
        self.assertEqual(
            Path(orchestrator.hygiene.__file__).resolve().parent.name,
            'kalshi_r2p1_hygiene_000_lab_20260922',
        )

    def test_packet_copies_match_and_scorecard_stays_null(self):
        frozen_bytes = orchestrator.FROZEN_EXPERIMENT.read_bytes()
        empty_bytes = orchestrator.EMPTY_RESULTS.read_bytes()
        for path in (
            orchestrator.FROZEN_EXPERIMENT,
            orchestrator.LAB_BUNDLE / 'FROZEN_EXPERIMENT.json',
            orchestrator.GOVERNANCE_BUNDLE / 'FROZEN_EXPERIMENT.json',
        ):
            self.assertEqual(path.read_bytes(), frozen_bytes)
            payload = json.loads(path.read_text())
            self.assertIsNone(payload['results'])
            self.assertIsNone(payload['pnl'])
            self.assertIs(payload['rfq_in_scope'], False)
            self.assertIs(payload['r1p4_strategy_open'], False)
            self.assertIs(payload['logan_keys_required'], False)
            self.assertIs(payload['signal_retune_000'], False)
            self.assertIs(payload['queue_fragility_reopen'], False)
            self.assertEqual(payload['panel_version'], orchestrator.PANEL_VERSION)
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
        self.assertIsNone(snapshot['empty.fill_vs_legs_mid_gap'])
        self.assertIsNone(snapshot['empty.legs_join_rate'])
        published = orchestrator.published_scorecard()
        orchestrator.assert_null_scorecard(published)
        self.assertEqual(published['status'], 'EMPTY_RESULTS_PRE_EXAMINER')

    def test_stub_loads_five_markets_and_prefers_admitted(self):
        self.assertEqual(orchestrator.select_panel_path(), orchestrator.PANEL_STUB)
        panel = orchestrator.load_panel()
        self.assertEqual(panel['series_ticker'], 'KXMVECROSSCATEGORY')
        self.assertEqual(len(panel['markets']), 5)
        self.assertEqual(len(panel['events']), 21)
        self.assertEqual(panel['cohort_summary']['legs_join_rate'], '5/5')
        self.assertEqual(
            [market['legs_n'] for market in panel['markets']],
            [3, 27, 4, 4, 4],
        )
        self.assertEqual(
            [market['market_ticker'] for market in panel['markets']],
            panel['cohort_summary']['sample_tickers'],
        )
        for market in panel['markets']:
            self.assertTrue(orchestrator.legs_complete(market))
            self.assertEqual(market['mve_collection_ticker'], 'KXMVECROSSCATEGORY-R')
            self.assertIsNone(market['volume_fp'])
            self.assertIsNone(market['open_interest_fp'])
        probe = panel['resolve_notes']['trades_probe']
        self.assertEqual(len(probe), 3)
        self.assertTrue(all(row['trades_n'] == 0 and row['http'] == 200 for row in probe))
        self.assertTrue(orchestrator.empty_tape(panel))
        self.assertIsNone(panel['results'])
        self.assertIsNone(panel['pnl'])
        self.assertIs(panel['admit_gate']['admit_py_run'], False)
        stamped = json.loads(orchestrator.PANEL_STUB.read_text())
        stamped['admitted_at'] = '2026-09-23T18:00:00Z'
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            stub = root / 'panel_stub.json'
            admitted = root / 'panel_admitted.json'
            stub.write_text(orchestrator.PANEL_STUB.read_text())
            admitted.write_text(json.dumps(stamped))
            chosen = orchestrator.select_panel_path(stub, admitted)
            self.assertEqual(chosen, admitted)
            loaded = orchestrator.load_panel(stub, admitted)
            self.assertEqual(loaded['admitted_at'], '2026-09-23T18:00:00Z')
            self.assertEqual(loaded['panel_version'], orchestrator.PANEL_VERSION)
            self.assertEqual(len(loaded['markets']), 5)
            admitted.unlink()
            self.assertEqual(orchestrator.select_panel_path(stub, admitted), stub)
            stamped['panel_version'] = '2026-09-22.s5-kxmvecrosscategory-v1'
            rejected = root / 'panel_stub.json'
            rejected.write_text(json.dumps(stamped))
            with self.assertRaises(orchestrator.PanelVersionRefused):
                orchestrator.load_panel(rejected, root / 'missing_admitted.json')

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
                ['git', 'diff', '--exit-code', orchestrator.UNTOUCHED_BASE, '--', path],
                cwd=PARENT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(diff.returncode, 0, path + diff.stdout + diff.stderr)
        series_table = PARENT / 'kalshi_feebook_lab_20260922' / 'series_fee_table.stub.json'
        before = series_table.read_bytes()
        panel = orchestrator.load_panel()
        table = orchestrator.combo_fee_table(panel)
        self.assertEqual(series_table.read_bytes(), before)
        self.assertEqual(
            set(table['overrides']),
            set(orchestrator.BOUND_SERIES),
        )
        self.assertTrue(all(
            row['fee_type'] == 'quadratic_with_combo_maker_fees' and row['maker_fees_enabled'] is True
            for row in table['overrides'].values()
        ))


class SchemaTests(unittest.TestCase):
    def test_s5l0_and_s5l1_schema_on_the_stub(self):
        before = {path: path.read_bytes() for path in _freeze_paths()}
        tob = orchestrator.conduct(orchestrator.S5L0)
        synthetic = orchestrator.conduct(orchestrator.S5L1)
        self.assertEqual(tob['leg_mid_source'], 'tob_1m')
        self.assertEqual(tob['cohort_note'], 'empty_tape_no_tob_mids')
        self.assertEqual(synthetic['leg_mid_source'], 'synthetic_leg_product')
        self.assertEqual(synthetic['cohort_note'], 'synthetic_product_fixture_only')
        self.assertIsNone(synthetic['schema_product'])
        self.assertEqual(tob['markets_n'], 5)
        self.assertEqual(tob['legs_complete_n'], 5)
        self.assertEqual(synthetic['markets_n'], 5)
        self.assertEqual(synthetic['legs_complete_n'], 5)
        self.assertIs(tob['empty_tape'], True)
        self.assertIs(synthetic['empty_tape'], True)
        self.assertEqual(tob['fee_pin'], synthetic['fee_pin'])
        self.assertEqual(tob['rails_pin'], synthetic['rails_pin'])
        self.assertEqual(tob['fee_type_series_override'], synthetic['fee_type_series_override'])
        self.assertEqual(
            [row['legs_n'] for row in tob['markets']],
            [3, 27, 4, 4, 4],
        )
        self.assertEqual(
            [row['market_ticker'] for row in synthetic['markets']],
            [row['market_ticker'] for row in tob['markets']],
        )
        for report in (tob, synthetic):
            orchestrator.assert_null_scorecard(report)
            orchestrator.assert_null_scorecard(report['published'])
            self.assertFalse(report['promoted'])
            self.assertIsNone(report['strategy_pointer'])
            self.assertIs(report['rfq_in_scope'], False)
            self.assertIs(report['r1p4_strategy_open'], False)
            self.assertIs(report['logan_keys_required'], False)
            self.assertEqual(report['source'], 'panel')
            for slot in report['markets']:
                self.assertIs(slot['legs_complete'], True)
                self.assertIsNone(slot['fill_price'])
                self.assertIsNone(slot['leg_product'])
                for key in orchestrator.OUTPUT_KEYS:
                    self.assertIsNone(slot[key])
        for path, raw in before.items():
            self.assertEqual(path.read_bytes(), raw)

    def test_s5l1_synthetic_product_stays_out_of_the_scorecard(self):
        before = {path: path.read_bytes() for path in _freeze_paths()}
        report = orchestrator.conduct_synthetic(orchestrator.S5L1)
        self.assertEqual(report['source'], 'synthetic_schema_standin')
        self.assertEqual(report['schema_product'], Decimal('0.10'))
        self.assertIs(report['known_product_match'], True)
        self.assertEqual(report['synthetic_print_count'], 1)
        self.assertIs(report['schema_print_scored'], False)
        self.assertIs(report['public_tape'], False)
        orchestrator.assert_null_scorecard(report)
        self.assertIsNone(report['fill_vs_legs_mid_gap'])
        self.assertIsNone(report['combo_fee_delta_vs_feebook'])
        self.assertIsNone(report['legs_join_rate'])
        self.assertIsNone(report['freshness_gap_sec'])
        with self.assertRaises(orchestrator.SyntheticArmRefused):
            orchestrator.conduct_synthetic(orchestrator.S5L0)
        with self.assertRaises(orchestrator.ScorecardPromotionRefused):
            orchestrator.write_scorecard(report['published'])
        with self.assertRaises(orchestrator.UnknownLegMidSource):
            orchestrator.conduct('S5L2')
        for path, raw in before.items():
            self.assertEqual(path.read_bytes(), raw)

    def test_leg_algebra_flips_no_and_refuses_missing_or_stale(self):
        self.assertEqual(orchestrator.leg_probability('0.20', 'no'), Decimal('0.80'))
        self.assertEqual(orchestrator.leg_probability('0.20', 'yes'), Decimal('0.20'))
        legs = [
            {'side': 'yes', 'mid': '0.50', 'content_fresh': True},
            {'side': 'no', 'mid': '0.20', 'content_fresh': True},
            {'side': 'yes', 'mid': '0.25', 'content_fresh': True},
        ]
        self.assertEqual(orchestrator.independent_leg_product(legs), Decimal('0.10'))
        with self.assertRaises(orchestrator.MissingLegRefused):
            orchestrator.independent_leg_product([{'side': 'yes', 'mid': None, 'content_fresh': True}])
        with self.assertRaises(orchestrator.MissingLegRefused):
            orchestrator.independent_leg_product([])
        with self.assertRaises(orchestrator.StaleLegRefused):
            orchestrator.independent_leg_product([
                {'side': 'yes', 'mid': '0.50', 'content_fresh': False},
            ])
        book = {
            'yes_dollars': [['0.40', '10']],
            'no_dollars': [['0.50', '10']],
        }
        self.assertEqual(orchestrator.tob_yes_mid(book), Decimal('0.45'))
        with self.assertRaises(feebook.BookIncomplete):
            orchestrator.tob_yes_mid({'yes_dollars': [['0.40', '10']], 'no_dollars': []})
        current = rails.BookObservation(rails.canonical_book_content(book), 't0')
        fresh = orchestrator.leg_row_from_book(book, 'no', None, current)
        self.assertEqual(fresh['mid'], Decimal('0.45'))
        self.assertIs(fresh['content_fresh'], True)
        self.assertEqual(
            orchestrator.independent_leg_product([fresh]),
            Decimal('0.55'),
        )
        stale = rails.BookObservation(current.content, current.transaction_time)
        with self.assertRaises(orchestrator.StaleLegRefused):
            orchestrator.leg_row_from_book(book, 'yes', current, stale)
        gap = orchestrator.hygiene.freshness_gap_seconds('90', '45')
        self.assertEqual(gap, Decimal('45'))
        self.assertIsNone(orchestrator.published_scorecard()['freshness_gap_sec'])
        credit = orchestrator.hygiene.maker_credit_floor_zero_refuse(
            '0.01', '1', series='KXMVECROSSCATEGORY', table=orchestrator.combo_fee_table(orchestrator.load_panel()),
        )
        self.assertEqual(credit['rule_id'], rails.FEE_CREDIT_RULE_ID)
        self.assertEqual(credit['formula_id'], feebook.EXAMINER_FORMULA_ID)
        self.assertIsNone(orchestrator.published_scorecard()['combo_fee_delta_vs_feebook'])


class RefuseTests(unittest.TestCase):
    def test_rfq_r1p4_logan_and_invented_fills_are_refused(self):
        for label in (
            'rfq',
            'communications',
            'r1p4_strategy',
            'r1_p4_strategy',
            'logan_keys',
            'logan_key',
            'invented_fill',
            'invented_pnl',
            'kxmvnfl',
            'admit_py',
            'live_order',
            'fee_blind_completed_profit',
            'completed_profit',
        ):
            with self.assertRaises(orchestrator.AdversaryRefused):
                orchestrator.refuse_adversary(label)
        with self.assertRaises(orchestrator.LiveOrdersForbidden):
            orchestrator.execution_adapter()
        with self.assertRaises(orchestrator.LiveOrdersForbidden):
            orchestrator.assert_public_get('POST')
        self.assertIsNone(orchestrator.assert_public_get('GET'))
        with self.assertRaises(orchestrator.RfqRefused):
            orchestrator.assert_route('GET /communications/rfqs')
        with self.assertRaises(orchestrator.LiveOrdersForbidden):
            orchestrator.assert_route('POST /portfolio/orders')
        self.assertIsNone(orchestrator.assert_route('GET /trade-api/v2/markets/{market_ticker}/orderbook'))
        with self.assertRaises(orchestrator.InventedFillRefused):
            orchestrator.assert_tape_honesty({'fill_price': '0.40', 'trades': [], 'trades_n': 0})
        with self.assertRaises(orchestrator.InventedFillRefused):
            orchestrator.assert_tape_honesty({'invent_fill': True, 'trades_n': 0})
        self.assertIsNone(orchestrator.assert_tape_honesty({'trades': [], 'trades_n': 0}))
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
        grok = feebook.grok_unrounded_maker_per_unit('0.50')
        with self.assertRaises(orchestrator.ShadowFeeLiteralRefused):
            orchestrator.assert_examiner_quote(grok)
        with self.assertRaises(orchestrator.ShadowFeeLiteralRefused):
            orchestrator.assert_examiner_quote({
                'formula_id': orchestrator.hygiene.INHERITED_MODEL_ID,
            })
        plain = feebook.order_fee('maker', '1', '0.50', round_up=True, series='KXMVECROSSCATEGORY')
        with self.assertRaises(orchestrator.ShadowFeeLiteralRefused):
            orchestrator.assert_combo_override_quote(plain)
        panel = json.loads(orchestrator.PANEL_STUB.read_text())
        panel['binds']['not_r1_p4_strategy'] = False
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'panel_stub.json'
            path.write_text(json.dumps(panel))
            with self.assertRaises(orchestrator.AdversaryRefused):
                orchestrator.load_panel(path, Path(tmp) / 'missing.json')
        panel = json.loads(orchestrator.PANEL_STUB.read_text())
        panel['binds']['forbid_inherited_q7_fee_literals'] = False
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'panel_stub.json'
            path.write_text(json.dumps(panel))
            with self.assertRaises(orchestrator.ShadowFeeLiteralRefused):
                orchestrator.load_panel(path, Path(tmp) / 'missing.json')
        panel = json.loads(orchestrator.PANEL_STUB.read_text())
        panel['binds']['logan_keys_required'] = True
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'panel_stub.json'
            path.write_text(json.dumps(panel))
            with self.assertRaises(orchestrator.AdversaryRefused):
                orchestrator.load_panel(path, Path(tmp) / 'missing.json')
        panel = json.loads(orchestrator.PANEL_STUB.read_text())
        panel['admit_gate']['admit_py_run'] = True
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'panel_stub.json'
            path.write_text(json.dumps(panel))
            with self.assertRaises(orchestrator.AdmitPyRefused):
                orchestrator.load_panel(path, Path(tmp) / 'missing.json')
        panel = json.loads(orchestrator.PANEL_STUB.read_text())
        panel['capture']['out_of_scope_routes'] = ['POST /portfolio/orders']
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'panel_stub.json'
            path.write_text(json.dumps(panel))
            with self.assertRaises(orchestrator.RfqRefused):
                orchestrator.load_panel(path, Path(tmp) / 'missing.json')
        filled = dict(orchestrator.published_scorecard())
        with self.assertRaises(orchestrator.ScorecardPromotionRefused):
            orchestrator.write_scorecard(filled)
        for key in orchestrator.OUTPUT_KEYS:
            broken = dict(orchestrator.published_scorecard())
            broken[key] = Decimal('1')
            with self.assertRaises(orchestrator.ScorecardPromotionRefused):
                orchestrator.write_scorecard(broken)


if __name__ == '__main__':
    unittest.main()
