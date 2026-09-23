"""Unit pins for the C3 KXHIGHNY bordering-strike harness.

Schema and pin locks only. In-memory helper calls are not a score and they
are not profit. Freeze outputs stay null. The subject is the panel stub
until panel_admitted.json appears. Ladder objects are a structure hypothesis.
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
        self.assertEqual(binding['experiment_id'], 'C3-KXHIGHNY-BORDERING-STRIKE-HARNESS')
        self.assertEqual(binding['knob'], 'strike_band')
        self.assertEqual(binding['panel_version'], '2026-09-22.c3-kxhighny-v0')
        self.assertEqual(panel['panel_version'], '2026-09-22.c3-kxhighny-v0')
        self.assertIsNone(panel['admitted_at'])
        self.assertIsNone(binding['admitted_at'])
        self.assertEqual(binding['series_primary'], 'KXHIGHNY')
        self.assertEqual(binding['series_proof'], 'KXHIGHCHI')
        self.assertEqual(binding['feebook_commit'], frozen['fee_pin'])
        self.assertEqual(binding['rails_commit'], frozen['rails_pin'])
        self.assertEqual(binding['feebook_commit'], '22371178cb2663250b4762f328069571c48cb551')
        self.assertEqual(binding['rails_commit'], '6a28e0d6254327ea4e6451c781bec56215ac6cac')
        self.assertEqual(binding['examiner_formula_id'], feebook.EXAMINER_FORMULA_ID)
        self.assertEqual(binding['fee_credit_rule_id'], rails.FEE_CREDIT_RULE_ID)
        self.assertEqual(binding['fee_source'], 'feebook')
        self.assertEqual(binding['rails_source'], 'rails')
        self.assertEqual(binding['honesty_helpers'], 'hygiene')
        self.assertEqual(binding['probe_formula_id'], feebook.EXAMINER_FORMULA_ID)
        self.assertIs(binding['probe_scorecard_write'], False)
        self.assertNotIn('fee_delta', binding)
        self.assertIsNone(binding['strategy_pointer'])
        self.assertIs(binding['structure_hyp_only'], True)
        self.assertIs(binding['github_weather_spread_ev'], False)
        self.assertIs(binding['logan_keys_required'], False)
        self.assertIs(binding['live_orders'], False)
        self.assertIs(binding['signal_retune_000'], False)
        self.assertIs(binding['queue_fragility_reopen'], False)
        self.assertIs(binding['cap_sr_reopen'], False)
        self.assertIs(binding['c5_reopen'], False)
        self.assertIs(binding['r3p3_strategy_merge'], False)
        self.assertIs(binding['fee_is_knob'], False)
        self.assertIn('not a strategy merge', binding['r3p3_prefer_cite'])
        self.assertEqual(tuple(frozen['scorecard_fields']), orchestrator.SCORECARD_FIELDS)
        self.assertEqual([arm['id'] for arm in frozen['arms']], list(orchestrator.ARMS))
        self.assertEqual(frozen['arms'][0]['strike_band'], 'near_extreme')
        self.assertEqual(frozen['arms'][1]['strike_band'], 'mid_ladder')
        self.assertIsNone(frozen['results'])
        self.assertIsNone(frozen['pnl'])
        self.assertIs(frozen['github_weather_spread_ev'], False)
        self.assertIs(frozen['structure_hyp_only'], True)
        self.assertIs(frozen['logan_keys_required'], False)
        self.assertEqual(binding['packet_sha256'], orchestrator.PACKET_SHA256)
        self.assertEqual(binding['kernel_sha256'], orchestrator.KERNEL_SHA256)
        self.assertEqual(binding['panel_stub_sha256'], orchestrator.PANEL_STUB_SHA256)
        self.assertEqual(
            orchestrator.sha256_file(orchestrator.PANEL_STUB),
            orchestrator.PANEL_STUB_SHA256,
        )
        self.assertEqual(
            sorted(path.name for path in PARENT.glob('kalshi_c3_kxhighny_bordering_lab_*')),
            ['kalshi_c3_kxhighny_bordering_lab_20260923'],
        )
        self.assertEqual(Path(feebook.__file__).resolve().parent.name, 'kalshi_feebook_lab_20260922')
        self.assertEqual(Path(rails.__file__).resolve().parent.name, 'kalshi_rails_lab_20260922')
        self.assertEqual(
            Path(orchestrator.hygiene.__file__).resolve().parent.name,
            'kalshi_r2p1_hygiene_000_lab_20260922',
        )
        c5_frozen = json.loads(orchestrator.C5_FROZEN.read_text())
        self.assertIsNone(c5_frozen['results'])
        self.assertIsNone(c5_frozen['pnl'])

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
            self.assertIs(payload['github_weather_spread_ev'], False)
            self.assertIs(payload['logan_keys_required'], False)
            self.assertIs(payload['signal_retune_000'], False)
            self.assertIs(payload['queue_fragility_reopen'], False)
            self.assertIs(payload['structure_hyp_only'], True)
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
        self.assertIsNone(snapshot['empty.multi_city_inventory_join'])
        self.assertIsNone(snapshot['empty.adjacent_spread_gap'])
        published = orchestrator.published_scorecard()
        orchestrator.assert_null_scorecard(published)
        self.assertEqual(published['status'], 'EMPTY_RESULTS_PRE_EXAMINER')
        self.assertIs(published['github_weather_spread_ev'], False)

    def test_stub_loads_and_admitted_panel_is_preferred_when_present(self):
        self.assertEqual(orchestrator.select_panel_path(), orchestrator.PANEL_STUB)
        panel = orchestrator.load_panel()
        self.assertEqual(panel['series_ticker'], 'KXHIGHNY')
        self.assertEqual(panel['cohort_counts']['markets_n'], 6)
        self.assertEqual(panel['cohort_counts']['events_n'], 3)
        self.assertIn('KXHIGHCHI', panel['multi_city_proof_series'])
        self.assertIsNone(panel['markets'][0]['volume_fp'])
        self.assertIsNone(panel['results'])
        self.assertIsNone(panel['pnl'])
        self.assertIsNone(panel['volume'])
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
            admitted.unlink()
            self.assertEqual(orchestrator.select_panel_path(stub, admitted), stub)
            stamped['panel_version'] = '2026-09-22.c3-kxhighny-v1'
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

    def test_reused_helpers_do_not_fill_the_scorecard(self):
        quote = feebook.order_fee('taker', '1', '0.50', round_up=True, series='KXHIGHNY')
        delta = orchestrator.hygiene.fee_delta(
            'taker', '1', '0.50', quote['rate'], series='KXHIGHNY',
        )
        self.assertEqual(delta['examiner_formula_id'], feebook.EXAMINER_FORMULA_ID)
        self.assertIsInstance(delta['fee_delta'], Decimal)
        gap = orchestrator.hygiene.freshness_gap_seconds('90', '45')
        self.assertEqual(gap, Decimal('45'))
        self.assertEqual(orchestrator.band_from_price('0.0100'), 'near_extreme')
        self.assertEqual(orchestrator.band_from_price('0.9900'), 'near_extreme')
        self.assertEqual(orchestrator.band_from_price('0.10'), 'near_extreme')
        self.assertEqual(orchestrator.band_from_price('0.90'), 'near_extreme')
        self.assertEqual(orchestrator.band_from_price('0.5200'), 'mid_ladder')
        self.assertEqual(orchestrator.band_from_price('0.11'), 'mid_ladder')
        published = orchestrator.published_scorecard()
        for key in orchestrator.SCORECARD_FIELDS:
            self.assertIsNone(published[key])
        self.assertIsNone(published['fee_delta_vs_inherited_model'])
        self.assertIsNone(published['freshness_gap_sec'])


class SchemaTests(unittest.TestCase):
    def test_c3b0_and_c3b1_schema_on_the_stub(self):
        before = {path: path.read_bytes() for path in _freeze_paths()}
        near = orchestrator.conduct(orchestrator.C3B0)
        mid = orchestrator.conduct(orchestrator.C3B1)
        self.assertEqual(near['strike_band'], 'near_extreme')
        self.assertEqual(mid['strike_band'], 'mid_ladder')
        self.assertEqual(near['pair_count'], 3)
        self.assertEqual(mid['pair_count'], 0)
        self.assertNotIn('cohort_note', near)
        self.assertEqual(mid['cohort_note'], orchestrator.MID_LADDER_NOTE)
        self.assertEqual(near['fee_pin'], mid['fee_pin'])
        self.assertEqual(near['rails_pin'], mid['rails_pin'])
        self.assertEqual(
            [(pair['left_ticker'], pair['right_ticker']) for pair in near['pairs']],
            [
                ('KXHIGHCHI-26SEP22-B64.5', 'KXHIGHCHI-26SEP22-B66.5'),
                ('KXHIGHNY-26SEP22-B65.5', 'KXHIGHNY-26SEP22-B67.5'),
                ('KXHIGHNY-26SEP22-B67.5', 'KXHIGHNY-26SEP22-T70'),
            ],
        )
        anchor = next(
            row for row in orchestrator.load_panel()['markets']
            if row['market_ticker'] == 'KXHIGHNY-26SEP22-B67.5'
        )
        self.assertEqual(anchor['bordering_strike_role'], 'mid_ladder_anchor')
        self.assertEqual(orchestrator.classify_market(anchor), 'near_extreme')
        for report in (near, mid):
            orchestrator.assert_null_scorecard(report)
            orchestrator.assert_null_scorecard(report['published'])
            self.assertFalse(report['promoted'])
            self.assertIsNone(report['strategy_pointer'])
            self.assertIs(report['github_weather_spread_ev'], False)
            self.assertIs(report['structure_hyp_only'], True)
            self.assertIs(report['r3p3_strategy_merge'], False)
            self.assertIs(report['live_orders'], False)
            self.assertEqual(report['source'], 'panel')
            self.assertIsNone(report['multi_city_inventory_join'])
            self.assertIsNone(report['presence']['arb_pnl'])
            self.assertIsNone(report['presence']['pnl'])
            self.assertIsNone(report['presence']['multi_city_inventory_join'])
            self.assertEqual(
                [(day['calendar_day'], day['ny_present'], day['chi_present'])
                 for day in report['presence']['days']],
                [
                    ('2026-09-23', True, True),
                    ('2026-09-24', True, False),
                ],
            )
            for day in report['presence']['days']:
                self.assertIsNone(day['arb_pnl'])
                self.assertIsNone(day['multi_city_inventory_join'])
        for pair in near['pairs']:
            orchestrator.assert_null_scorecard(pair)
            self.assertIs(pair['structure_hyp_only'], True)
            self.assertIs(pair['github_weather_spread_ev'], False)
        for path, raw in before.items():
            self.assertEqual(path.read_bytes(), raw)

    def test_synthetic_bands_stay_out_of_the_freeze(self):
        before = {path: path.read_bytes() for path in _freeze_paths()}
        near = orchestrator.conduct_synthetic(orchestrator.C3B0)
        mid = orchestrator.conduct_synthetic(orchestrator.C3B1)
        self.assertEqual(near['source'], 'synthetic_schema_standin')
        self.assertEqual(mid['source'], 'synthetic_schema_standin')
        self.assertEqual(near['pair_count'], 1)
        self.assertEqual(mid['pair_count'], 1)
        self.assertNotIn('cohort_note', near)
        self.assertNotIn('cohort_note', mid)
        self.assertEqual(
            (near['pairs'][0]['left_ticker'], near['pairs'][0]['right_ticker']),
            ('KXHIGHNY-SYN-EXT-A', 'KXHIGHNY-SYN-EXT-B'),
        )
        self.assertEqual(
            (mid['pairs'][0]['left_ticker'], mid['pairs'][0]['right_ticker']),
            ('KXHIGHNY-SYN-MID-A', 'KXHIGHNY-SYN-MID-B'),
        )
        self.assertEqual(mid['presence']['days'][0]['calendar_day'], '2026-09-25')
        self.assertIs(mid['presence']['days'][0]['ny_present'], True)
        self.assertIs(mid['presence']['days'][0]['chi_present'], True)
        self.assertIsNone(mid['presence']['days'][0]['arb_pnl'])
        for report in (near, mid):
            orchestrator.assert_null_scorecard(report)
            for pair in report['pairs']:
                for key in orchestrator.OUTPUT_KEYS:
                    self.assertIsNone(pair[key])
        with self.assertRaises(orchestrator.ScorecardPromotionRefused):
            orchestrator.write_scorecard(mid['published'])
        with self.assertRaises(orchestrator.UnknownBand):
            orchestrator.conduct('C3B2')
        for path, raw in before.items():
            self.assertEqual(path.read_bytes(), raw)


class RefuseTests(unittest.TestCase):
    def test_github_ev_live_order_and_invented_arb_are_refused(self):
        for label in (
            'github_weather_spread_ev',
            'github_ev',
            'weather_spread_ev',
            'invented_arb',
            'cross_city_arb',
            'settlement_penalty_ev',
            'invented_pnl',
            'fee_blind_completed_profit',
            'completed_profit',
            'live_order',
            'r3p3_strategy_merge',
        ):
            with self.assertRaises(orchestrator.AdversaryRefused):
                orchestrator.refuse_adversary(label)
        with self.assertRaises(orchestrator.LiveOrdersForbidden):
            orchestrator.execution_adapter()
        with self.assertRaises(orchestrator.LiveOrdersForbidden):
            orchestrator.assert_public_get('POST')
        self.assertIsNone(orchestrator.assert_public_get('GET'))
        source = (ROOT / 'orchestrator.py').read_text()
        for banned in (
            '0.0175',
            '0.07',
            'maker_coefficient',
            'taker_coefficient',
            'common_config',
            'class KalshiExecutionAdapter',
            'urlopen',
            'import queue_fragility',
            'os.environ',
            'api_key',
            'private_key',
            'urllib',
            'requests',
        ):
            self.assertNotIn(banned, source)
        grok = feebook.grok_unrounded_maker_per_unit('0.50')
        with self.assertRaises(orchestrator.ShadowFeeLiteralRefused):
            orchestrator.assert_examiner_quote(grok)
        with self.assertRaises(orchestrator.ShadowFeeLiteralRefused):
            orchestrator.assert_examiner_quote({
                'formula_id': orchestrator.hygiene.INHERITED_MODEL_ID,
            })
        disagreed = {
            'market_ticker': 'KXHIGHNY-SYN-BAD',
            'last_price_dollars_raw_get': '0.5200',
            'strike_band': 'near_extreme',
        }
        with self.assertRaises(orchestrator.OrchestratorError):
            orchestrator.classify_market(disagreed)
        labeled = {
            'market_ticker': 'KXHIGHNY-SYN-EV',
            'weather_spread_ev': '1',
            'strike_band': 'mid_ladder',
        }
        with self.assertRaises(orchestrator.AdversaryRefused):
            orchestrator.classify_market(labeled)
        with self.assertRaises(orchestrator.AdversaryRefused):
            orchestrator.presence_from_rows([{
                'series_ticker': 'KXHIGHNY',
                'occurrence_datetime': '2026-09-23T14:00:00Z',
                'arb_pnl': '1',
            }])
        panel = json.loads(orchestrator.PANEL_STUB.read_text())
        panel['binds']['no_github_weather_spread_ev_as_evidence'] = False
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'panel_stub.json'
            path.write_text(json.dumps(panel))
            with self.assertRaises(orchestrator.AdversaryRefused):
                orchestrator.load_panel(path, Path(tmp) / 'missing.json')
        panel = json.loads(orchestrator.PANEL_STUB.read_text())
        panel['binds']['no_live_orders'] = False
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'panel_stub.json'
            path.write_text(json.dumps(panel))
            with self.assertRaises(orchestrator.LiveOrdersForbidden):
                orchestrator.load_panel(path, Path(tmp) / 'missing.json')
        panel = json.loads(orchestrator.PANEL_STUB.read_text())
        panel['markets'][0]['volume_fp'] = '1'
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'panel_stub.json'
            path.write_text(json.dumps(panel))
            with self.assertRaises(orchestrator.InventedInventoryRefused):
                orchestrator.load_panel(path, Path(tmp) / 'missing.json')
        panel = json.loads(orchestrator.PANEL_STUB.read_text())
        panel['r3p3_prefer_cite'] = 'merge the kernels as one strategy'
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'panel_stub.json'
            path.write_text(json.dumps(panel))
            with self.assertRaises(orchestrator.AdversaryRefused):
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
