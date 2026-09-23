"""Unit pins for the R2-P3 KXNFLPASSYDS prop-ladder harness.

Schema and pin locks only. In-memory ladder fits are not a score and they
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


def _first_strike():
    return dict(orchestrator.load_synthetic_ladder()[0])


class PinTests(unittest.TestCase):
    def test_binding_pins_the_stub_and_the_instruments(self):
        self.assertFalse(orchestrator.PANEL_ADMITTED.exists())
        self.assertFalse(orchestrator.GOVERNANCE_TREE.exists())
        binding = orchestrator.instrument_binding()
        panel = orchestrator.load_panel()
        frozen = json.loads(orchestrator.FROZEN_EXPERIMENT.read_text())
        stamp = json.loads(orchestrator.CONDUCTOR_STAMP.read_text())
        self.assertEqual(binding['experiment_id'], 'R2-P3-KXNFLPASSYDS-PROP-LADDER-HARNESS')
        self.assertEqual(binding['feature_family'], 'PROP-LQ')
        self.assertEqual(frozen['feature_family'], 'PROP-LQ')
        self.assertEqual(binding['knob'], 'residual_monotone_family')
        self.assertEqual(frozen['knob'], 'residual_monotone_family')
        self.assertEqual(binding['panel_version'], '2026-09-22.r2-p3-prop-slate-v0')
        self.assertEqual(panel['panel_version'], '2026-09-22.r2-p3-prop-slate-v0')
        self.assertIsNone(panel['admitted_at'])
        self.assertIsNone(binding['admitted_at'])
        self.assertEqual(binding['events_n'], 6)
        self.assertEqual(len(panel['events']), 6)
        self.assertEqual(binding['conductor_events_n_claim'], 6)
        self.assertEqual(stamp['panel_events'], 6)
        self.assertEqual(panel['freeze_packet_sha256'], orchestrator.KERNEL_SHA256)
        self.assertEqual(binding['feebook_commit'], frozen['fee_pin'])
        self.assertEqual(binding['rails_commit'], frozen['rails_pin'])
        self.assertEqual(binding['feebook_commit'], '22371178cb2663250b4762f328069571c48cb551')
        self.assertEqual(binding['rails_commit'], '6a28e0d6254327ea4e6451c781bec56215ac6cac')
        self.assertEqual(binding['examiner_formula_id'], feebook.EXAMINER_FORMULA_ID)
        self.assertEqual(binding['fee_credit_rule_id'], rails.FEE_CREDIT_RULE_ID)
        self.assertEqual(binding['fee_source'], 'feebook')
        self.assertEqual(binding['queue_source'], 'rails')
        self.assertEqual(binding['honesty_helpers'], 'hygiene')
        self.assertEqual(binding['lee_ready'], 'REFUSED')
        self.assertEqual(binding['atl_gb'], 'REFUSED')
        self.assertIs(binding['probe_scorecard_write'], False)
        self.assertIsNone(binding['strategy_pointer'])
        self.assertIs(binding['logan_keys_required'], False)
        self.assertIs(binding['live_orders'], False)
        self.assertIs(binding['signal_retune_000'], False)
        self.assertIs(binding['queue_fragility_reopen'], False)
        self.assertIs(binding['cap_sr_reopen'], False)
        self.assertIs(binding['cap_sr_fx_reopen'], False)
        self.assertIs(binding['admit_py_run'], False)
        self.assertIs(binding['fee_is_knob'], False)
        self.assertIs(binding['markout_is_knob'], False)
        self.assertEqual(binding['dead_cards'], orchestrator.DEAD_CARDS)
        self.assertEqual(tuple(frozen['scorecard_fields']), orchestrator.SCORECARD_FIELDS)
        self.assertEqual([arm['id'] for arm in frozen['arms']], list(orchestrator.ARMS))
        self.assertEqual(frozen['arms'][0]['family'], 'isotonic')
        self.assertEqual(frozen['arms'][1]['family'], 'logit_monotone')
        self.assertEqual(binding['packet_sha256'], orchestrator.PACKET_SHA256)
        self.assertEqual(binding['kernel_sha256'], orchestrator.KERNEL_SHA256)
        self.assertEqual(binding['panel_stub_sha256'], orchestrator.PANEL_STUB_SHA256)
        self.assertEqual(
            orchestrator.sha256_file(orchestrator.PACKET),
            'f8335eb0080cb1f82b1fad512509749134dd0e6e41ed85795347c3476796e87a',
        )
        self.assertEqual(
            orchestrator.sha256_file(orchestrator.KERNEL),
            'a30108f658359590e170c73ea00d1a1f0852d5751cb15c9f2a9c6389f4dd3eaa',
        )
        self.assertEqual(
            orchestrator.sha256_file(orchestrator.PANEL_STUB),
            '70e879e8738d033f392d821849dee3537af3e7b8a916670779d238f78ce098be',
        )
        self.assertEqual(orchestrator.PACKET_SHA256, orchestrator.CONDUCTOR_PACKET_SHA256)
        self.assertEqual(orchestrator.KERNEL_SHA256, orchestrator.CONDUCTOR_KERNEL_SHA256)
        self.assertEqual(orchestrator.PANEL_STUB_SHA256, orchestrator.CONDUCTOR_PANEL_STUB_SHA256)
        self.assertEqual(stamp['freeze_sha256'], orchestrator.PACKET_SHA256)
        self.assertEqual(stamp['parent_freeze_sha256'], orchestrator.KERNEL_SHA256)
        self.assertEqual(stamp['panel_stub_sha256'], orchestrator.PANEL_STUB_SHA256)
        pins = orchestrator.conductor_pin_status()
        self.assertIs(pins['packet_matches_conductor_claim'], True)
        self.assertIs(pins['kernel_matches_conductor_claim'], True)
        self.assertIs(pins['panel_stub_matches_conductor_claim'], True)
        self.assertIs(pins['conductor_bytes_in_checkout'], True)
        self.assertEqual(pins['events_n_claim'], 6)
        self.assertIs(binding['conductor_bytes_in_checkout'], True)
        self.assertIs(frozen['conductor_bytes_in_checkout'], True)
        self.assertEqual(frozen['packet_sha256'], orchestrator.PACKET_SHA256)
        self.assertEqual(frozen['parent_freeze_sha256'], orchestrator.KERNEL_SHA256)
        self.assertEqual(frozen['panel_stub_sha256'], orchestrator.PANEL_STUB_SHA256)
        self.assertIsNone(frozen['results'])
        self.assertIsNone(frozen['pnl'])
        self.assertIsNone(stamp['results'])
        self.assertIsNone(stamp['pnl'])
        self.assertEqual(binding['base_commit'], 'd7584dd48a67d38d81f5141654b6f498915a70a5')
        self.assertEqual(Path(feebook.__file__).resolve().parent.name, 'kalshi_feebook_lab_20260922')
        self.assertEqual(Path(rails.__file__).resolve().parent.name, 'kalshi_rails_lab_20260922')
        self.assertEqual(
            Path(orchestrator.hygiene.__file__).resolve().parent.name,
            'kalshi_r2p1_hygiene_000_lab_20260922',
        )

    def test_packet_copies_match_and_scorecard_stays_null(self):
        frozen_bytes = orchestrator.FROZEN_EXPERIMENT.read_bytes()
        empty_bytes = orchestrator.EMPTY_RESULTS.read_bytes()
        packet_bytes = orchestrator.PACKET.read_bytes()
        kernel_bytes = orchestrator.KERNEL.read_bytes()
        panel_bytes = orchestrator.PANEL_STUB.read_bytes()
        for path in (
            orchestrator.FROZEN_EXPERIMENT,
            orchestrator.LAB_BUNDLE / 'FROZEN_EXPERIMENT.json',
            orchestrator.GOVERNANCE_BUNDLE / 'FROZEN_EXPERIMENT.json',
        ):
            self.assertEqual(path.read_bytes(), frozen_bytes)
            payload = json.loads(path.read_text())
            self.assertIsNone(payload['results'])
            self.assertIsNone(payload['pnl'])
            self.assertEqual(payload['conductor_events_n_claim'], 6)
        for path in (
            orchestrator.PACKET,
            orchestrator.LAB_BUNDLE / orchestrator.PACKET_NAME,
            PARENT / 'packets' / orchestrator.PACKET_NAME,
            orchestrator.GOVERNANCE_BUNDLE / orchestrator.PACKET_NAME,
        ):
            self.assertEqual(path.read_bytes(), packet_bytes)
            self.assertEqual(orchestrator.sha256_file(path), orchestrator.CONDUCTOR_PACKET_SHA256)
        for path in (
            orchestrator.KERNEL,
            orchestrator.LAB_BUNDLE / orchestrator.KERNEL_NAME,
            PARENT / 'packets' / orchestrator.KERNEL_NAME,
            orchestrator.GOVERNANCE_BUNDLE / orchestrator.KERNEL_NAME,
        ):
            self.assertEqual(path.read_bytes(), kernel_bytes)
            self.assertEqual(orchestrator.sha256_file(path), orchestrator.CONDUCTOR_KERNEL_SHA256)
        for path in (
            orchestrator.PANEL_STUB,
            orchestrator.LAB_BUNDLE / 'panel_stub.json',
            orchestrator.GOVERNANCE_BUNDLE / 'panel_stub.json',
        ):
            self.assertEqual(path.read_bytes(), panel_bytes)
            self.assertEqual(orchestrator.sha256_file(path), orchestrator.CONDUCTOR_PANEL_STUB_SHA256)
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
        self.assertIsNone(snapshot['empty.cross_strike_residual_rms'])
        self.assertIsNone(snapshot['empty.latent_fit_fragmentation'])
        self.assertIsNone(snapshot['empty.maker_credit_floor_zero_n'])
        self.assertIsNone(snapshot['empty.fresh_strike_n'])
        self.assertIsNone(snapshot['empty.settled_join_n'])
        published = orchestrator.published_scorecard()
        orchestrator.assert_null_scorecard(published)
        self.assertEqual(published['status'], 'EMPTY_RESULTS_PRE_EXAMINER')
        self.assertEqual(published['lee_ready'], 'REFUSED')
        self.assertEqual(published['atl_gb'], 'REFUSED')

    def test_stub_loads_six_events_and_prefers_admitted_when_present(self):
        self.assertEqual(orchestrator.select_panel_path(), orchestrator.PANEL_STUB)
        panel = orchestrator.load_panel()
        self.assertEqual(
            [event['event_ticker'] for event in panel['events']],
            list(orchestrator.SLATE_EVENTS),
        )
        self.assertEqual(panel['cohort_kind'], 'sun_2026-09-27_dual_game_prop_slate_LACBUF_BALDAL')
        self.assertIsNone(panel['results'])
        self.assertIsNone(panel['pnl'])
        self.assertIsNone(panel['volume'])
        self.assertIs(panel['admit_gate']['admit_py_run'], False)
        for event in panel['events']:
            self.assertEqual(event['market_tickers'], [])
            self.assertIsNone(event['volume_fp'])
            self.assertIsNone(event['volume_24h_fp'])
            self.assertIsNone(event['open_interest_fp'])
            self.assertNotIn('ATLGB', event['event_ticker'])
        excluded = panel['excluded'][0]['events']
        self.assertEqual(tuple(excluded), orchestrator.EXCLUDED_EVENTS)
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
            self.assertEqual(len(loaded['events']), 6)
            admitted.unlink()
            self.assertEqual(orchestrator.select_panel_path(stub, admitted), stub)
            thin = dict(stamped)
            thin['admitted_at'] = None
            thin['events'] = list(stamped['events'][:5])
            thin['panel_version'] = orchestrator.PANEL_VERSION
            rejected = root / 'thin.json'
            rejected.write_text(json.dumps(thin))
            with self.assertRaises(orchestrator.OrchestratorError) as caught:
                orchestrator.load_panel(rejected, root / 'missing_admitted.json')
            self.assertEqual(str(caught.exception), 'events')
            stamped['admitted_at'] = None
            stamped['panel_version'] = '2026-09-22.r2-p3-prop-slate-v1'
            version_path = root / 'panel_stub.json'
            version_path.write_text(json.dumps(stamped))
            with self.assertRaises(orchestrator.PanelVersionRefused):
                orchestrator.load_panel(version_path, root / 'missing_admitted.json')

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
    def test_both_arms_on_the_panel_stub_leave_the_scorecard_null(self):
        before = {path: path.read_bytes() for path in _freeze_paths()}
        isotonic = orchestrator.conduct(orchestrator.R2P3A0)
        logit = orchestrator.conduct(orchestrator.R2P3A1)
        self.assertEqual(isotonic['family'], 'isotonic')
        self.assertEqual(logit['family'], 'logit_monotone')
        self.assertEqual(isotonic['event_count'], 6)
        self.assertEqual(logit['event_count'], 6)
        self.assertEqual(isotonic['market_count'], 0)
        self.assertIs(isotonic['admitted_markets'], False)
        self.assertEqual(isotonic['panel_note'], 'market_tickers_empty_not_a_cohort')
        self.assertEqual(isotonic['fee_pin'], logit['fee_pin'])
        self.assertEqual(isotonic['rails_pin'], logit['rails_pin'])
        self.assertEqual(isotonic['lee_ready'], 'REFUSED')
        self.assertEqual(isotonic['atl_gb'], 'REFUSED')
        for report in (isotonic, logit):
            orchestrator.assert_null_scorecard(report)
            orchestrator.assert_null_scorecard(report['published'])
            self.assertFalse(report['promoted'])
            self.assertEqual(report['source'], 'panel')
            self.assertNotIn('strikes', report)
        for path, raw in before.items():
            self.assertEqual(path.read_bytes(), raw)

    def test_synthetic_ladders_fit_in_memory_and_stay_out_of_the_freeze(self):
        before = {path: path.read_bytes() for path in _freeze_paths()}
        isotonic = orchestrator.conduct_ladder(orchestrator.R2P3A0)
        logit = orchestrator.conduct_ladder(orchestrator.R2P3A1)
        self.assertEqual(isotonic['source'], 'synthetic_schema_standin')
        self.assertEqual(isotonic['arm'], 'R2P3A0')
        self.assertEqual(logit['arm'], 'R2P3A1')
        self.assertEqual(isotonic['strike_count'], 7)
        self.assertEqual(isotonic['player_ids'], ('SYNTHETIC_A', 'SYNTHETIC_B'))
        by_id = {row['strike_id']: row for row in isotonic['strikes']}
        self.assertEqual(by_id['synthetic:LACBUF:A:250']['mid'], Decimal('0.75'))
        self.assertEqual(by_id['synthetic:LACBUF:A:275']['mid'], Decimal('0.77'))
        self.assertEqual(by_id['synthetic:LACBUF:A:250']['fitted_mid'], Decimal('0.76'))
        self.assertEqual(by_id['synthetic:LACBUF:A:275']['fitted_mid'], Decimal('0.76'))
        self.assertEqual(by_id['synthetic:LACBUF:A:250']['residual'], Decimal('-0.01'))
        self.assertEqual(by_id['synthetic:LACBUF:A:275']['residual'], Decimal('0.01'))
        self.assertEqual(by_id['synthetic:LACBUF:A:300']['residual'], Decimal('0'))
        self.assertEqual(by_id['synthetic:LACBUF:A:325']['residual'], Decimal('0'))
        self.assertEqual(by_id['synthetic:LACBUF:A:325']['mid'], Decimal('0.015'))
        fitted_a = [
            by_id[key]['fitted_mid']
            for key in (
                'synthetic:LACBUF:A:250',
                'synthetic:LACBUF:A:275',
                'synthetic:LACBUF:A:300',
                'synthetic:LACBUF:A:325',
            )
        ]
        self.assertTrue(all(earlier >= later for earlier, later in zip(fitted_a, fitted_a[1:])))
        for key in (
            'synthetic:BALDAL:B:250',
            'synthetic:BALDAL:B:275',
            'synthetic:BALDAL:B:300',
        ):
            self.assertEqual(by_id[key]['residual'], Decimal('0'))
        self.assertIs(by_id['synthetic:LACBUF:A:250']['content_fresh_flag'], True)
        self.assertEqual(by_id['synthetic:LACBUF:A:250']['queue_attribution_bin'], 'q3300')
        self.assertIs(by_id['synthetic:LACBUF:A:250']['maker_credit_floor_zero_refuse'], False)
        self.assertIs(by_id['synthetic:LACBUF:A:275']['content_fresh_flag'], False)
        self.assertIs(by_id['synthetic:LACBUF:A:300']['content_fresh_flag'], False)
        self.assertEqual(by_id['synthetic:LACBUF:A:300']['queue_attribution_bin'], 'q10000')
        self.assertEqual(by_id['synthetic:LACBUF:A:300']['fresh_reason'], 'keepalive_ignored')
        self.assertIs(by_id['synthetic:LACBUF:A:325']['maker_credit_floor_zero_refuse'], True)
        touch = feebook.order_fee(
            'taker', '1', '0.80', round_up=True, series='KXNFLPASSYDS',
        )
        self.assertEqual(by_id['synthetic:LACBUF:A:250']['taker_touch_fee'], touch['fee'])
        self.assertEqual(by_id['synthetic:LACBUF:A:250']['formula_id'], feebook.EXAMINER_FORMULA_ID)
        self.assertEqual(by_id['synthetic:LACBUF:A:250']['series_resolution'], 'default_unknown_series')
        logit_by_id = {row['strike_id']: row for row in logit['strikes']}
        self.assertEqual(
            logit_by_id['synthetic:LACBUF:A:250']['fitted_mid'],
            logit_by_id['synthetic:LACBUF:A:275']['fitted_mid'],
        )
        self.assertNotEqual(
            logit_by_id['synthetic:LACBUF:A:250']['fitted_mid'],
            Decimal('0.76'),
        )
        logit_fitted = [
            logit_by_id[key]['fitted_mid']
            for key in (
                'synthetic:LACBUF:A:250',
                'synthetic:LACBUF:A:275',
                'synthetic:LACBUF:A:300',
                'synthetic:LACBUF:A:325',
            )
        ]
        self.assertTrue(all(earlier >= later for earlier, later in zip(logit_fitted, logit_fitted[1:])))
        for report in (isotonic, logit):
            orchestrator.assert_null_scorecard(report)
            for row in report['strikes']:
                orchestrator.assert_null_scorecard(row)
                self.assertEqual(row['lee_ready'], 'REFUSED')
                self.assertIsNone(row['aggressor_inference'])
                self.assertEqual(row['source'], 'synthetic_schema_standin')
        with self.assertRaises(orchestrator.ScorecardPromotionRefused):
            orchestrator.write_scorecard(isotonic['published'])
        with self.assertRaises(orchestrator.ScorecardPromotionRefused):
            orchestrator.publish_residual_rms(Decimal('0.01'))
        with self.assertRaises(orchestrator.UnknownFamily):
            orchestrator.conduct('R2P3A2')
        for path, raw in before.items():
            self.assertEqual(path.read_bytes(), raw)


class RefuseTests(unittest.TestCase):
    def test_lee_ready_slate_and_fee_invent_are_refused(self):
        samples = (
            None,
            {},
            {'mid': '0.50'},
            {'classifier': 'lee-ready'},
            {'lee_ready': True},
            'quote',
        )
        for sample in samples:
            with self.assertRaises(orchestrator.LeeReadyRefused):
                orchestrator.infer_lee_ready(sample)
        base = _first_strike()
        with self.assertRaises(orchestrator.LeeReadyRefused):
            orchestrator.annotate_strike(dict(base, lee_ready=True))
        with self.assertRaises(orchestrator.LeeReadyRefused):
            orchestrator.annotate_strike(dict(base, classifier='LeeReady'))
        with self.assertRaises(orchestrator.LeeReadyRefused):
            orchestrator.annotate_strike(dict(base, aggressor_inference='buy'))
        atl = dict(base)
        atl['event_ticker'] = 'KXNFLPASSYDS-26SEP24ATLGB'
        atl['game_id'] = 'ATLGB'
        atl['strike_id'] = 'synthetic:ATLGB:A:250'
        with self.assertRaises(orchestrator.SlateRefused):
            orchestrator.annotate_strike(atl)
        with self.assertRaises(orchestrator.ShadowFeeLiteralRefused):
            orchestrator.annotate_strike(dict(base, fee='1'))
        with self.assertRaises(orchestrator.AdversaryRefused):
            orchestrator.annotate_strike(dict(base, freshness_source='ws_ping'))
        with self.assertRaises(orchestrator.InventedFillRefused):
            orchestrator.annotate_strike(dict(base, result='yes'))
        with self.assertRaises(orchestrator.InventedFillRefused):
            orchestrator.annotate_strike(dict(base, player_id='LACJHERBERT10'))
        with self.assertRaises(orchestrator.AdversaryRefused):
            orchestrator.select_markout('1m')
        with self.assertRaises(orchestrator.LeeReadyRefused):
            orchestrator.refuse_adversary('lee_ready')
        with self.assertRaises(orchestrator.SlateRefused):
            orchestrator.refuse_adversary('atl_gb')

    def test_live_orders_reopens_and_shadow_fees_are_refused(self):
        for label in (
            'logan_keys',
            'invented_pnl',
            'invented_fills',
            'invented_cohort',
            'invented_volume',
            'q6_retune',
            'qf_reopen',
            'cap_sr_reopen',
            'cap_sr_fx_reopen',
            'admit_py',
            'ws_ping',
            'q7_arm_b',
            'markout_knob',
            'completed_profit',
        ):
            with self.assertRaises(orchestrator.AdversaryRefused):
                orchestrator.refuse_adversary(label)
        with self.assertRaises(orchestrator.LiveOrdersForbidden):
            orchestrator.refuse_adversary('live_orders')
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
        ):
            self.assertNotIn(banned, source)
        grok = feebook.grok_unrounded_maker_per_unit('0.50')
        with self.assertRaises(orchestrator.ShadowFeeLiteralRefused):
            orchestrator.assert_examiner_quote(grok)
        with self.assertRaises(orchestrator.ShadowFeeLiteralRefused):
            orchestrator.assert_examiner_quote({
                'formula_id': orchestrator.hygiene.INHERITED_MODEL_ID,
            })
        filled = dict(orchestrator.published_scorecard())
        with self.assertRaises(orchestrator.ScorecardPromotionRefused):
            orchestrator.write_scorecard(filled)
        for key in orchestrator.OUTPUT_KEYS:
            broken = dict(orchestrator.published_scorecard())
            broken[key] = 1
            with self.assertRaises(orchestrator.ScorecardPromotionRefused):
                orchestrator.write_scorecard(broken)


if __name__ == '__main__':
    unittest.main()
