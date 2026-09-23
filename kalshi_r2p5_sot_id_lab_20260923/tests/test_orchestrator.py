"""Unit pins for the R2-P5 SOT-ID kickoff audit harness.

Schema and pin locks only. In-memory refuse checks are not a score and they
are not profit. Freeze outputs stay null. The subject is the attached
ADMIT-1 SoT seed.
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


def _freeze_paths():
    return (
        orchestrator.FROZEN_EXPERIMENT,
        orchestrator.EMPTY_RESULTS,
        orchestrator.PACKET,
        orchestrator.PARENT_ACCEPT,
        orchestrator.SEED,
        orchestrator.SCHEMA,
        orchestrator.PITCLE_CITE,
        orchestrator.LAB_BUNDLE / 'FROZEN_EXPERIMENT.json',
        orchestrator.LAB_BUNDLE / 'results.json',
        orchestrator.GOVERNANCE_BUNDLE / 'FROZEN_EXPERIMENT.json',
        orchestrator.GOVERNANCE_BUNDLE / 'results.json',
        orchestrator.GOVERNANCE_BUNDLE / 'results' / 'EMPTY_RESULTS.json',
    )


def _write_seed(payload):
    directory = tempfile.TemporaryDirectory()
    path = Path(directory.name) / 'seed.json'
    path.write_text(json.dumps(payload))
    return directory, path


class PinTests(unittest.TestCase):
    def test_binding_pins_digests_and_sixteen_rows(self):
        self.assertFalse(orchestrator.GOVERNANCE_TREE.exists())
        binding = orchestrator.instrument_binding()
        seed = orchestrator.load_seed()
        frozen = json.loads(orchestrator.FROZEN_EXPERIMENT.read_text())
        stamp = json.loads(orchestrator.CONDUCTOR_STAMP.read_text())
        schema = json.loads(orchestrator.SCHEMA.read_text())
        self.assertEqual(binding['experiment_id'], 'R2-P5-SOT-ID-HARNESS')
        self.assertEqual(binding['feature_family'], 'SOT-ID')
        self.assertEqual(frozen['feature_family'], 'SOT-ID')
        self.assertEqual(stamp['feature_family'], 'SOT-ID')
        self.assertEqual(stamp['packet_id'], 'R2-P5-SOT-ID-HARNESS')
        self.assertEqual(binding['knob'], 'audit_slice')
        self.assertEqual(frozen['knob'], 'audit_slice')
        self.assertEqual(binding['panel_version'], '2026-09-22.1-kalshi-occurrence-sot')
        self.assertEqual(seed['panel_version'], '2026-09-22.1-kalshi-occurrence-sot')
        self.assertEqual(seed['admit_stamp_utc'], '2026-09-22T21:18:13Z')
        self.assertEqual(binding['admit_stamp_utc'], '2026-09-22T21:18:13Z')
        self.assertIsNone(binding['harness_admitted_at'])
        self.assertIsNone(frozen['harness_admitted_at'])
        self.assertEqual(binding['seed_rows'], 16)
        self.assertEqual(len(seed['rows']), 16)
        self.assertEqual(stamp['seed_rows'], 16)
        self.assertEqual(frozen['seed_rows'], 16)
        self.assertEqual(binding['feebook_commit'], '22371178cb2663250b4762f328069571c48cb551')
        self.assertEqual(binding['rails_commit'], '6a28e0d6254327ea4e6451c781bec56215ac6cac')
        self.assertEqual(binding['feebook_commit'], frozen['fee_pin'])
        self.assertEqual(binding['rails_commit'], frozen['rails_pin'])
        self.assertEqual(binding['examiner_formula_id'], feebook.EXAMINER_FORMULA_ID)
        self.assertEqual(seed['fee_pin_formula_id'], feebook.EXAMINER_FORMULA_ID)
        self.assertEqual(binding['fee_credit_rule_id'], rails.FEE_CREDIT_RULE_ID)
        self.assertEqual(binding['fee_source'], 'feebook')
        self.assertEqual(binding['rails_source'], 'rails')
        self.assertIs(binding['fee_import_only'], True)
        self.assertIs(binding['rails_import_only'], True)
        self.assertIs(binding['fee_applied_to_seed_rows'], False)
        self.assertIs(binding['probe_scorecard_write'], False)
        self.assertIs(binding['hedge_fields_null'], True)
        self.assertIs(binding['s2_r2p4_ungated'], False)
        self.assertIs(frozen['s2_r2p4_ungated'], False)
        self.assertIs(binding['admit_py_run'], False)
        self.assertIs(binding['second_admit_panel'], False)
        self.assertIs(binding['poll_steal'], False)
        self.assertIs(binding['logan_keys_required'], False)
        self.assertIs(binding['live_orders'], False)
        self.assertIs(binding['signal_retune_000'], False)
        self.assertIs(binding['cap_sr_reopen'], False)
        self.assertIs(binding['l2_cat_reopen'], False)
        self.assertIs(binding['fee_is_knob'], False)
        self.assertIsNone(binding['strategy_pointer'])
        self.assertEqual(binding['external_odds_invent'], 'REFUSED')
        self.assertEqual(binding['holdout_rewrite'], 'REFUSED')
        self.assertEqual(binding['silent_holdout_mixed'], 'REFUSED')
        self.assertEqual(binding['labeled_recreation'], 'REFUSED')
        self.assertEqual(binding['empty_seed'], 'REFUSED')
        self.assertEqual(frozen['atl_gb'], 'REFUSED')
        self.assertEqual(binding['dead_cards'], orchestrator.DEAD_CARDS)
        self.assertEqual(tuple(frozen['scorecard_fields']), orchestrator.SCORECARD_FIELDS)
        self.assertEqual([arm['id'] for arm in frozen['arms']], list(orchestrator.ARMS))
        self.assertEqual(frozen['arms'][0]['audit_slice'], 'sot_pin_match')
        self.assertEqual(frozen['arms'][1]['audit_slice'], 'holdout_delta_bin')
        self.assertEqual(stamp['arms'], ['R2P5A0', 'R2P5A1'])
        self.assertEqual(schema['$defs']['event_row']['required'], list(orchestrator.ROW_REQUIRED))
        self.assertEqual(
            schema['$defs']['event_row']['properties']['window_clock_source']['enum'],
            list(orchestrator.CLOCK_ENUM),
        )
        self.assertIsNone(seed['external_odds_path'])
        self.assertIsNone(frozen['results'])
        self.assertIsNone(frozen['pnl'])
        self.assertIsNone(stamp['results'])
        self.assertIsNone(stamp['pnl'])
        pins = orchestrator.conductor_pin_status()
        self.assertIs(pins['conductor_bytes_in_checkout'], True)
        self.assertIs(pins['freeze_matches_conductor_claim'], True)
        self.assertIs(pins['parent_accept_matches_conductor_claim'], True)
        self.assertIs(pins['seed_matches_conductor_claim'], True)
        self.assertIs(pins['schema_matches_conductor_claim'], True)
        self.assertIs(pins['pitcle_matches_conductor_claim'], True)
        self.assertEqual(pins['seed_rows'], 16)
        self.assertEqual(pins['seed_rows_claim'], 16)
        self.assertIs(pins['governance_tree_present'], False)
        self.assertEqual(orchestrator.sha256_file(orchestrator.PACKET), orchestrator.FREEZE_SHA256)
        self.assertEqual(orchestrator.sha256_file(orchestrator.PARENT_ACCEPT), orchestrator.PARENT_ACCEPT_SHA256)
        self.assertEqual(orchestrator.sha256_file(orchestrator.SEED), orchestrator.SEED_SHA256)
        self.assertEqual(orchestrator.sha256_file(orchestrator.SCHEMA), orchestrator.SCHEMA_SHA256)
        self.assertEqual(orchestrator.sha256_file(orchestrator.PITCLE_CITE), orchestrator.PITCLE_SHA256)
        self.assertEqual(
            orchestrator.FREEZE_SHA256,
            '0424455f062b7c46c7c6161b84fb7b29702719acc45bf6a61b4e8f16c5e26457',
        )
        self.assertEqual(
            orchestrator.PARENT_ACCEPT_SHA256,
            '712e4771bf2783dbee1e4c553194cd2896a468184f2849f24e58c3eb350ff499',
        )
        self.assertEqual(
            orchestrator.SEED_SHA256,
            '1edfa91979ab5dac72e28cc5e2ad5ff08aab414b5574fe115f86fb7d85e2ac4b',
        )
        self.assertEqual(
            orchestrator.SCHEMA_SHA256,
            'da7f6badd37d52fbd977681924379c3552f0dbfec94729d86ea411fb473ce53c',
        )
        self.assertEqual(
            orchestrator.PITCLE_SHA256,
            'f5ca19f15940a80476d1590e506951df87df619160b477f1dff06cc3554cb520',
        )
        self.assertEqual(Path(feebook.__file__).resolve().parent.name, 'kalshi_feebook_lab_20260922')
        self.assertEqual(Path(rails.__file__).resolve().parent.name, 'kalshi_rails_lab_20260922')
        self.assertEqual(
            Path(orchestrator.hygiene.__file__).resolve().parent.name,
            'kalshi_r2p1_hygiene_000_lab_20260922',
        )
        self.assertEqual(
            sorted(path.name for path in PARENT.glob('kalshi_r2p5_sot_id_lab_*')),
            ['kalshi_r2p5_sot_id_lab_20260923'],
        )

    def test_packet_copies_match_and_scorecard_stays_null(self):
        frozen_bytes = orchestrator.FROZEN_EXPERIMENT.read_bytes()
        empty_bytes = orchestrator.EMPTY_RESULTS.read_bytes()
        authentic = (
            (orchestrator.FREEZE_NAME, orchestrator.PACKET),
            (orchestrator.PARENT_NAME, orchestrator.PARENT_ACCEPT),
            (orchestrator.SEED_NAME, orchestrator.SEED),
            (orchestrator.SCHEMA_NAME, orchestrator.SCHEMA),
            (orchestrator.PITCLE_NAME, orchestrator.PITCLE_CITE),
        )
        for name, canonical in authentic:
            raw = canonical.read_bytes()
            for path in (
                orchestrator.ROOT / name,
                orchestrator.LAB_BUNDLE / name,
                PARENT / 'packets' / name,
                orchestrator.GOVERNANCE_BUNDLE / name,
            ):
                self.assertEqual(path.read_bytes(), raw)
        for path in (
            orchestrator.FROZEN_EXPERIMENT,
            orchestrator.LAB_BUNDLE / 'FROZEN_EXPERIMENT.json',
            orchestrator.GOVERNANCE_BUNDLE / 'FROZEN_EXPERIMENT.json',
        ):
            self.assertEqual(path.read_bytes(), frozen_bytes)
            payload = json.loads(path.read_text())
            self.assertIsNone(payload['results'])
            self.assertIsNone(payload['pnl'])
            self.assertEqual(payload['seed_rows'], 16)
            self.assertEqual(payload['pre_accept_empty_role'], 'REFUSED_NOT_A_SEED')
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
            for key in orchestrator.OUTPUT_KEYS:
                self.assertIsNone(payload[key])
        pre_accept = json.loads(orchestrator.PRE_ACCEPT_EMPTY.read_text())
        self.assertEqual(pre_accept['note'], 'pre-ACCEPT empty')
        self.assertNotIn('identity_join_ok_n', pre_accept)
        self.assertNotIn('external_odds_invent_refuse_n', pre_accept)
        with self.assertRaises(orchestrator.PreAcceptEmptyRefused):
            orchestrator.assert_null_scorecard(pre_accept)
        snapshot = orchestrator.frozen_output_snapshot()
        self.assertIsNone(snapshot['frozen.results'])
        self.assertIsNone(snapshot['empty.pnl'])
        self.assertIsNone(snapshot['empty.delta_kickoff_sec_mode'])
        self.assertIsNone(snapshot['empty.identity_join_ok_n'])
        published = orchestrator.published_scorecard()
        orchestrator.assert_null_scorecard(published)
        self.assertEqual(published['status'], 'EMPTY_RESULTS_PRE_EXAMINER')

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


class SchemaTests(unittest.TestCase):
    def test_both_arms_audit_the_seed_and_leave_the_scorecard_null(self):
        before = {path: path.read_bytes() for path in _freeze_paths()}
        seed = orchestrator.load_seed()
        pin = orchestrator.conduct(orchestrator.R2P5A0)
        delta = orchestrator.conduct(orchestrator.R2P5A1)
        self.assertEqual(pin['audit_slice'], 'sot_pin_match')
        self.assertEqual(delta['audit_slice'], 'holdout_delta_bin')
        self.assertEqual(pin['rows_n'], 16)
        self.assertEqual(delta['rows_n'], 16)
        self.assertEqual(pin['source'], 'admit1_sot_seed')
        self.assertIs(pin['window_clock_uniform'], True)
        self.assertIs(delta['delta_values_uniform'], True)
        self.assertIs(pin['external_odds_present_all_false'], True)
        self.assertIs(pin['adverse_fields_null'], True)
        self.assertIs(delta['adverse_fields_null'], True)
        self.assertIs(pin['pitcle_identity_checked'], True)
        self.assertIs(pin['pitcle_holdout_unchanged'], True)
        self.assertEqual(pin['pitcle_event_ticker'], 'KXNFLGAME-26OCT01PITCLE')
        self.assertIs(pin['s2_r2p4_ungated'], False)
        self.assertIs(pin['second_admit_panel'], False)
        self.assertIs(pin['poll_steal'], False)
        self.assertIs(pin['admit_py_run'], False)
        self.assertFalse(pin['promoted'])
        self.assertIsNone(pin['strategy_pointer'])
        self.assertEqual(pin['fee_pin'], delta['fee_pin'])
        self.assertEqual(pin['rails_pin'], delta['rails_pin'])
        clocks = {row['window_clock_source'] for row in seed['rows']}
        deltas = {row['delta_kickoff_sec'] for row in seed['rows']}
        series = {row['series_ticker'] for row in seed['rows']}
        self.assertEqual(clocks, {'kalshi_occurrence'})
        self.assertEqual(deltas, {10800})
        self.assertEqual(series, {'KXNFLGAME'})
        self.assertEqual(orchestrator.SEED_DELTA_SEC, 10800)
        pit = seed['rows'][0]
        self.assertEqual(pit['event_ticker'], 'KXNFLGAME-26OCT01PITCLE')
        self.assertEqual(pit['holdout_kickoff_utc'], '2026-10-02T00:15:00Z')
        self.assertEqual(pit['kalshi_occurrence_datetime'], '2026-10-02T03:15:00Z')
        self.assertEqual(pit['sot_pin'], pit['kalshi_occurrence_datetime'])
        self.assertEqual(pit['t_minus_7d_utc'], '2026-09-25T03:15:00Z')
        self.assertEqual(
            [row['event_ticker'] for row in seed['rows']],
            list(orchestrator.CANONICAL_TICKERS),
        )
        for report in (pin, delta):
            orchestrator.assert_null_scorecard(report)
            orchestrator.assert_null_scorecard(report['published'])
            for key in orchestrator.OUTPUT_KEYS:
                self.assertIsNone(report[key])
        for path, raw in before.items():
            self.assertEqual(path.read_bytes(), raw)

    def test_explicit_holdout_mixed_is_loaded_and_silent_mix_is_refused(self):
        seed = json.loads(orchestrator.SEED.read_text())
        mixed = copy.deepcopy(seed)
        mixed['rows'][1]['window_clock_source'] = 'holdout_mixed'
        mixed['rows'][1]['t_minus_7d_utc'] = '2026-09-27T13:30:00Z'
        directory, path = _write_seed(mixed)
        self.addCleanup(directory.cleanup)
        loaded = orchestrator.load_seed(path)
        self.assertEqual(loaded['rows'][1]['window_clock_source'], 'holdout_mixed')
        report = orchestrator.conduct(orchestrator.R2P5A0, loaded)
        self.assertIs(report['window_clock_uniform'], False)
        self.assertIsNone(report['holdout_mixed_refuse_n'])
        self.assertIsNone(report['sot_pin_mismatch_n'])
        silent = copy.deepcopy(seed)
        silent['rows'][1]['t_minus_7d_utc'] = '2026-09-27T13:30:00Z'
        directory_silent, silent_path = _write_seed(silent)
        self.addCleanup(directory_silent.cleanup)
        with self.assertRaises(orchestrator.HoldoutMixedRefused):
            orchestrator.load_seed(silent_path)
        mismatch = copy.deepcopy(seed)
        mismatch['rows'][2]['sot_pin'] = mismatch['rows'][2]['holdout_kickoff_utc']
        directory_mismatch, mismatch_path = _write_seed(mismatch)
        self.addCleanup(directory_mismatch.cleanup)
        with self.assertRaises(orchestrator.SotPinMismatchRefused):
            orchestrator.load_seed(mismatch_path)


class RefuseTests(unittest.TestCase):
    def test_odds_invent_holdout_rewrite_and_delta_mismatch_are_refused(self):
        seed = json.loads(orchestrator.SEED.read_text())
        invented = copy.deepcopy(seed)
        invented['rows'][3]['edge_at_quote'] = 0.01
        directory, path = _write_seed(invented)
        self.addCleanup(directory.cleanup)
        with self.assertRaises(orchestrator.ExternalOddsInventRefused):
            orchestrator.load_seed(path)
        rewritten = copy.deepcopy(seed)
        rewritten['rows'][0]['holdout_rewritten_to_sot'] = True
        directory_rewrite, rewrite_path = _write_seed(rewritten)
        self.addCleanup(directory_rewrite.cleanup)
        with self.assertRaises(orchestrator.RewriteHoldoutRefused):
            orchestrator.load_seed(rewrite_path)
        moved = copy.deepcopy(seed)
        moved['rows'][0]['holdout_kickoff_utc'] = moved['rows'][0]['kalshi_occurrence_datetime']
        moved['rows'][0]['delta_kickoff_sec'] = 0
        directory_moved, moved_path = _write_seed(moved)
        self.addCleanup(directory_moved.cleanup)
        with self.assertRaises(orchestrator.RewriteHoldoutRefused):
            orchestrator.load_seed(moved_path)
        broken_delta = copy.deepcopy(seed)
        broken_delta['rows'][4]['delta_kickoff_sec'] = 0
        directory_delta, delta_path = _write_seed(broken_delta)
        self.addCleanup(directory_delta.cleanup)
        with self.assertRaises(orchestrator.DeltaInconsistentRefused):
            orchestrator.load_seed(delta_path)
        with self.assertRaises(orchestrator.RewriteHoldoutRefused):
            orchestrator.rewrite_holdout_kickoff(seed['rows'][0], seed['rows'][0]['sot_pin'])
        with self.assertRaises(orchestrator.ExternalOddsInventRefused):
            orchestrator.invent_external_odds(seed['rows'][0])
        self.assertEqual(seed['rows'][0]['holdout_kickoff_utc'], '2026-10-02T00:15:00Z')

    def test_empty_recreation_second_panel_and_pre_accept_are_refused(self):
        seed = json.loads(orchestrator.SEED.read_text())
        empty = copy.deepcopy(seed)
        empty['rows'] = []
        directory, path = _write_seed(empty)
        self.addCleanup(directory.cleanup)
        with self.assertRaises(orchestrator.EmptySeedRefused):
            orchestrator.load_seed(path)
        short = copy.deepcopy(seed)
        short['rows'] = short['rows'][:15]
        directory_short, short_path = _write_seed(short)
        self.addCleanup(directory_short.cleanup)
        with self.assertRaises(orchestrator.RecreationRefused):
            orchestrator.load_seed(short_path)
        labeled = copy.deepcopy(seed)
        labeled['labeled_recreation'] = True
        directory_labeled, labeled_path = _write_seed(labeled)
        self.addCleanup(directory_labeled.cleanup)
        with self.assertRaises(orchestrator.RecreationRefused):
            orchestrator.load_seed(labeled_path)
        restamp = copy.deepcopy(seed)
        restamp['admit_stamp_utc'] = '2026-09-23T16:45:00Z'
        directory_stamp, stamp_path = _write_seed(restamp)
        self.addCleanup(directory_stamp.cleanup)
        with self.assertRaises(orchestrator.SecondPanelRefused):
            orchestrator.load_seed(stamp_path)
        with self.assertRaises(orchestrator.PreAcceptEmptyRefused):
            orchestrator.load_seed(orchestrator.PRE_ACCEPT_EMPTY)
        with self.assertRaises(orchestrator.SecondPanelRefused):
            orchestrator.second_admit_panel()
        with self.assertRaises(orchestrator.PollStealRefused):
            orchestrator.steal_admit1_poll()
        with self.assertRaises(orchestrator.PollStealRefused):
            orchestrator.fetch_seed_over_network('https://example.invalid/seed')
        with self.assertRaises(orchestrator.AdmitPyRefused):
            orchestrator.run_admit_py()
        with self.assertRaises(orchestrator.UngateRefused):
            orchestrator.ungate_s2_r2p4()
        atl = copy.deepcopy(seed['rows'][5])
        atl['event_ticker'] = 'KXNFLGAME-26SEP99ATLGB'
        with self.assertRaises(orchestrator.AtlGbRefused):
            orchestrator.audit_row(orchestrator.R2P5A0, atl, None)

    def test_named_refuses_and_live_paths_stay_closed(self):
        for label in (
            'external_odds_invent',
            'invented_odds',
            'holdout_rewrite',
            'silent_holdout_mixed',
            'labeled_recreation',
            'empty_seed',
            'pre_accept_empty',
            'second_admit',
            'poll_steal',
            'admit_py',
            's2_ungate',
            'r2p4_ungate',
            'logan_keys',
            'logan_key',
            'live_orders',
            'invented_pnl',
            'q6_retune',
            '000',
            'cap_sr_reopen',
            'l2_cat_reopen',
            'atl_gb',
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
        self.assertIsNone(orchestrator.assert_route('GET /trade-api/v2/events'))
        with self.assertRaises(orchestrator.UnknownSlice):
            orchestrator.conduct('R2P5A2')
        filled = dict(orchestrator.published_scorecard())
        with self.assertRaises(orchestrator.ScorecardPromotionRefused):
            orchestrator.write_scorecard(filled)
        for key in orchestrator.OUTPUT_KEYS:
            broken = dict(orchestrator.published_scorecard())
            broken[key] = 1
            with self.assertRaises(orchestrator.ScorecardPromotionRefused):
                orchestrator.write_scorecard(broken)
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


if __name__ == '__main__':
    unittest.main()
