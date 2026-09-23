"""Unit pins for the S5 KXMVECROSSCATEGORY settled-resolution join harness.

Schema and pin locks only. In-memory row labels are not a score and they
are not profit. Freeze outputs stay null. admitted_at stays null.
Scout settled_nonempty_result_N is not copied into settled_join_n.
"""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT.parent
sys.path.insert(0, str(ROOT))

import orchestrator


def _freeze_paths():
    return (
        orchestrator.FROZEN_EXPERIMENT,
        orchestrator.EMPTY_RESULTS,
        orchestrator.PACKET,
        orchestrator.SCOUT_PATH,
        orchestrator.SEED_PATH,
        orchestrator.REGET_PATH,
        orchestrator.PANEL_CAPTURE,
        orchestrator.SOURCE_PINS,
        orchestrator.CONDUCTOR_ACCEPT,
        orchestrator.LAB_BUNDLE / 'FROZEN_EXPERIMENT.json',
        orchestrator.LAB_BUNDLE / 'results.json',
        orchestrator.LAB_BUNDLE / 'results' / 'EMPTY_RESULTS.json',
    )


class PinTests(unittest.TestCase):
    def test_binding_pins_the_seed_and_leaves_the_scorecard_null(self):
        self.assertFalse(orchestrator.PANEL_ADMITTED.exists())
        self.assertFalse(orchestrator.ADMIT_PY.exists())
        binding = orchestrator.instrument_binding()
        panel = orchestrator.load_panel()
        frozen = json.loads(orchestrator.FROZEN_EXPERIMENT.read_text())
        self.assertEqual(binding['experiment_id'], 'S5-KXMVECROSSCATEGORY-SETTLED-RESOLUTION-JOIN-HARNESS')
        self.assertEqual(binding['feature_family'], 'S5-RJ')
        self.assertEqual(frozen['feature_family'], 'S5-RJ')
        self.assertEqual(frozen['status'], 'FROZEN_EXPERIMENT')
        self.assertEqual(binding['knob'], 'join_gate')
        self.assertEqual(frozen['knob'], 'join_gate')
        self.assertEqual(frozen['arm_values'], {
            'J0': 'nonempty_result_required',
            'J1': 'occurrence_datetime_match',
        })
        self.assertEqual(
            [row['join_gate'] for row in binding['arms']],
            ['nonempty_result_required', 'occurrence_datetime_match'],
        )
        self.assertEqual(binding['panel_version'], '2026-09-22.s5-kxmvecrosscategory-v0')
        self.assertEqual(panel['panel_version'], '2026-09-22.s5-kxmvecrosscategory-v0')
        self.assertIsNone(panel['admitted_at'])
        self.assertIsNone(binding['admitted_at'])
        self.assertIsNone(frozen['admitted_at'])
        self.assertEqual(panel['stub_status'], 'PANEL_SCHEMA_STUB_SEED_NOT_ADMITTED')
        self.assertEqual(binding['events_n'], 21)
        self.assertEqual(binding['markets_n'], 5)
        self.assertEqual(binding['settled_nonempty_result_N_scout'], 20)
        self.assertEqual(frozen['settled_nonempty_result_N_scout'], 20)
        self.assertIs(binding['scout_n_copied_into_settled_join_n'], False)
        self.assertEqual(binding['yes_n'], 4)
        self.assertEqual(binding['no_n'], 16)
        self.assertEqual(binding['settled_list_row_n'], 20)
        self.assertEqual(binding['parent_seed_tickers'], list(orchestrator.PARENT_SEED_TICKERS))
        self.assertEqual(binding['parent_seeds_finalized_nonempty_N'], 5)
        self.assertEqual(binding['parent_seed_results'], dict(orchestrator.PARENT_SEED_RESULTS))
        self.assertIsNone(binding['seed_panel_result'])
        self.assertIs(binding['parent_results_copied_onto_panel'], False)
        self.assertEqual(binding['panel_stub_active_n'], 2)
        self.assertEqual(binding['panel_stub_finalized_status_n'], 3)
        self.assertIs(binding['parent_reget_occurrence_present'], False)
        self.assertEqual(binding['occurrence_datetime_present_on_settled_N'], 0)
        self.assertEqual(binding['expected_expiration_time_present_on_settled_N'], 20)
        self.assertEqual(binding['j1_null_occurrence_clock'], 'expected_expiration_time')
        self.assertEqual(binding['related_series_settled_N'], 20)
        self.assertEqual(binding['related_series_settled_http'], '200')
        self.assertIs(binding['related_series_markets_invented'], False)
        self.assertIs(binding['list_429_backfilled'], False)
        self.assertIs(binding['cursor_followed'], False)
        self.assertEqual(binding['settled_list_http'], '200')
        self.assertIs(binding['settled_list_cursor_present'], True)
        self.assertIsNone(binding['open_list_http'])
        self.assertIsNone(binding['open_list_n'])
        self.assertEqual(binding['settled_list_earlier_429'], '429_honest')
        self.assertEqual(binding['finalized_list_429'], '429_honest')
        self.assertEqual(binding['finalized_list_scout_attempts'], '429_honest_then_not_required')
        self.assertEqual(binding['events_closed_settled_429'], '429_honest')
        self.assertEqual(binding['shard1_series_429'], '429_honest')
        self.assertEqual(binding['honest_gap_n'], 4)
        self.assertIs(binding['occurrence_sources_agree'], True)
        self.assertIs(binding['fee_import_used'], False)
        self.assertIs(binding['rails_import_used'], False)
        self.assertIs(binding['fee_arms'], False)
        self.assertEqual(
            binding['feebook_commit_fixed_not_loaded'],
            '22371178cb2663250b4762f328069571c48cb551',
        )
        self.assertEqual(
            binding['rails_commit_fixed_not_loaded'],
            '6a28e0d6254327ea4e6451c781bec56215ac6cac',
        )
        self.assertEqual(binding['lee_ready'], 'REFUSED')
        self.assertIs(binding['logan_keys_required'], False)
        self.assertIs(binding['live_orders'], False)
        self.assertIs(binding['cap_sr_reopen'], False)
        self.assertIs(binding['fq_reopen'], False)
        self.assertIs(binding['filllegs_reopen'], False)
        self.assertIs(binding['mve_fl_reopen'], False)
        self.assertIs(binding['s4_rj_reopen'], False)
        self.assertIs(binding['nhl_rj_reopen'], False)
        self.assertIs(binding['c3_rj_reopen'], False)
        self.assertIs(binding['c5_rj_reopen'], False)
        self.assertIs(binding['r3p3_rj_reopen'], False)
        self.assertIs(binding['r2p3_rj_reopen'], False)
        self.assertIs(binding['arm_b_touch'], False)
        self.assertIs(binding['conductor_cloud_kick'], False)
        self.assertIs(binding['admit_py_run'], False)
        self.assertEqual(binding['does_not_ungate'], ['S1', 'S2', 'R2-P4'])
        self.assertIs(binding['s1_s2_r2p4_ungated'], False)
        self.assertEqual(binding['examiner_status'], 'HOLD_PRE_PR')
        self.assertIs(binding['stub_ready'], False)
        self.assertEqual(tuple(frozen['arms']), orchestrator.ARMS)
        self.assertEqual(binding['freeze_sha256'], orchestrator.FREEZE_SHA256)
        self.assertEqual(binding['scout_reget_sha256'], orchestrator.SCOUT_SHA256)
        self.assertEqual(binding['seed_summary_sha256'], orchestrator.SEED_SHA256)
        self.assertEqual(binding['panel_stub_sha256'], orchestrator.PANEL_STUB_SHA256)
        self.assertEqual(binding['settled_reget_sha256'], orchestrator.REGET_SHA256)
        self.assertEqual(binding['conductor_accept_sha256'], orchestrator.ACCEPT_SHA256)
        self.assertEqual(binding['source_pins_sha256'], orchestrator.SOURCE_PINS_SHA256)
        self.assertEqual(binding['base_commit'], orchestrator.BASE_COMMIT)
        self.assertEqual(binding['row_label_count'], 29)
        self.assertIsNone(binding['results'])
        self.assertIsNone(binding['pnl'])
        self.assertIsNone(binding['settled_join_n'])
        self.assertIsNone(binding['occurrence_match_n'])
        self.assertIsNone(binding['admit_ready_flag'])
        self.assertIsNone(frozen['results'])
        self.assertIsNone(frozen['pnl'])
        self.assertNotIn('settled_join_n', frozen)
        self.assertNotEqual(binding['settled_join_n'], binding['settled_nonempty_result_N_scout'])
        self.assertNotEqual(binding['settled_join_n'], 20)
        self.assertNotEqual(binding['settled_join_n'], 5)
        self.assertNotEqual(binding['occurrence_match_n'], 20)
        pins = orchestrator.conductor_pin_status()
        self.assertIs(pins['conductor_bytes_in_checkout'], True)
        self.assertIs(pins['accept_matches_conductor_claim'], True)
        self.assertIs(pins['governance_s5_cites_present'], True)
        self.assertIs(pins['reget_cite_present'], True)
        self.assertIs(binding['conductor_bytes_in_checkout'], True)
        source = (ROOT / 'orchestrator.py').read_text()
        self.assertNotIn('import feebook', source)
        self.assertNotIn('import rails', source)
        self.assertNotIn('importlib', source)
        self.assertNotIn('urlopen', source)
        self.assertNotIn('urllib', source)

    def test_packet_copies_match_and_scorecard_stays_null(self):
        frozen_bytes = orchestrator.FROZEN_EXPERIMENT.read_bytes()
        empty_bytes = orchestrator.EMPTY_RESULTS.read_bytes()
        packet_bytes = orchestrator.PACKET.read_bytes()
        scout_bytes = orchestrator.SCOUT_PATH.read_bytes()
        seed_bytes = orchestrator.SEED_PATH.read_bytes()
        reget_bytes = orchestrator.REGET_PATH.read_bytes()
        panel_bytes = orchestrator.PANEL_CAPTURE.read_bytes()
        pins_bytes = orchestrator.SOURCE_PINS.read_bytes()
        accept_bytes = orchestrator.CONDUCTOR_ACCEPT.read_bytes()
        hold_bytes = orchestrator.EXAMINER_HOLD.read_bytes()
        pin_bytes = orchestrator.MAXIMIZE_PIN.read_bytes()
        digest_bytes = orchestrator.DIGESTS_PATH.read_bytes()
        self.assertEqual(orchestrator.sha256_file(orchestrator.PACKET), orchestrator.FREEZE_SHA256)
        self.assertEqual(orchestrator.sha256_file(orchestrator.SCOUT_PATH), orchestrator.SCOUT_SHA256)
        self.assertEqual(orchestrator.sha256_file(orchestrator.SEED_PATH), orchestrator.SEED_SHA256)
        self.assertEqual(orchestrator.sha256_file(orchestrator.PANEL_CAPTURE), orchestrator.PANEL_STUB_SHA256)
        self.assertEqual(orchestrator.sha256_file(orchestrator.REGET_PATH), orchestrator.REGET_SHA256)
        self.assertEqual(orchestrator.sha256_file(orchestrator.CONDUCTOR_ACCEPT), orchestrator.ACCEPT_SHA256)
        self.assertEqual(orchestrator.sha256_file(orchestrator.ACCEPT_ROOT), orchestrator.ACCEPT_SHA256)
        self.assertEqual(orchestrator.sha256_file(orchestrator.FROZEN_EXPERIMENT), orchestrator.FROZEN_SHA256)
        self.assertEqual(orchestrator.sha256_file(orchestrator.EMPTY_RESULTS), orchestrator.EMPTY_SHA256)
        self.assertEqual(orchestrator.sha256_file(orchestrator.SOURCE_PINS), orchestrator.SOURCE_PINS_SHA256)
        self.assertEqual(orchestrator.sha256_file(orchestrator.FREEZE_GOV), orchestrator.FREEZE_SHA256)
        self.assertEqual(orchestrator.sha256_file(orchestrator.REGET_CITE), orchestrator.REGET_SHA256)
        self.assertEqual(orchestrator.sha256_file(orchestrator.PANEL_GOV), orchestrator.PANEL_STUB_SHA256)
        for directory in orchestrator.owned_dirs():
            self.assertEqual((directory / orchestrator.FREEZE_NAME).read_bytes(), packet_bytes)
            self.assertEqual((directory / orchestrator.SCOUT_NAME).read_bytes(), scout_bytes)
            self.assertEqual((directory / orchestrator.SEED_NAME).read_bytes(), seed_bytes)
            self.assertEqual((directory / orchestrator.REGET_NAME).read_bytes(), reget_bytes)
            self.assertEqual((directory / orchestrator.ACCEPT_NAME).read_bytes(), accept_bytes)
            self.assertEqual((directory / 'FROZEN_EXPERIMENT.json').read_bytes(), frozen_bytes)
            self.assertEqual((directory / 'panel_stub.json').read_bytes(), panel_bytes)
            self.assertEqual((directory / orchestrator.PANEL_ALIAS).read_bytes(), panel_bytes)
            self.assertEqual((directory / orchestrator.SOURCE_PINS_NAME).read_bytes(), pins_bytes)
            self.assertEqual((directory / orchestrator.HOLD_NAME).read_bytes(), hold_bytes)
            self.assertEqual((directory / orchestrator.PIN_NAME).read_bytes(), pin_bytes)
            self.assertEqual((directory / orchestrator.DIGESTS_NAME).read_bytes(), digest_bytes)
            self.assertEqual((directory / 'EMPTY_RESULTS.json').read_bytes(), empty_bytes)
        for path in (
            orchestrator.EMPTY_RESULTS,
            orchestrator.LAB_BUNDLE / 'results.json',
            orchestrator.LAB_BUNDLE / 'results' / 'EMPTY_RESULTS.json',
            orchestrator.SCIENCE / 'results' / 'EMPTY_RESULTS.json',
            orchestrator.PACKET_DIR / 'results.json',
        ):
            self.assertEqual(path.read_bytes(), empty_bytes)
            payload = json.loads(path.read_text())
            self.assertEqual(payload['note'], orchestrator.EMPTY_NOTE)
            for key in orchestrator.OUTPUT_KEYS:
                self.assertIsNone(payload[key])
        snapshot = orchestrator.frozen_output_snapshot()
        self.assertIsNone(snapshot['frozen.results'])
        self.assertIsNone(snapshot['frozen.pnl'])
        self.assertIsNone(snapshot['empty.settled_join_n'])
        self.assertIsNone(snapshot['empty.occurrence_match_n'])
        self.assertIsNone(snapshot['empty.admit_ready_flag'])
        self.assertIsNone(snapshot['empty.results'])
        self.assertIsNone(snapshot['empty.pnl'])
        published = orchestrator.published_scorecard()
        orchestrator.assert_null_scorecard(published)
        loaded = orchestrator.load_scorecard(orchestrator.EMPTY_RESULTS)
        orchestrator.assert_null_scorecard(loaded)
        self.assertEqual(published['examiner_status'], 'HOLD_PRE_PR')
        self.assertIs(published['stub_ready'], False)
        self.assertEqual(published['lee_ready'], 'REFUSED')
        self.assertIs(published['scout_n_copied_into_settled_join_n'], False)

    def test_panel_stub_admitted_at_stays_null(self):
        self.assertEqual(orchestrator.select_panel_path(), orchestrator.PANEL_CAPTURE)
        panel = orchestrator.load_panel()
        self.assertEqual(panel['packet_id'], 'S5-KXMVECROSSCATEGORY-MEAS')
        self.assertIsNone(panel['results'])
        self.assertIsNone(panel['pnl'])
        self.assertIsNone(panel['volume'])
        self.assertEqual(len(panel['events']), 21)
        self.assertEqual(len(panel['markets']), 5)
        self.assertEqual(panel['ineligible'], [])
        active = 0
        finalized = 0
        for market in panel['markets']:
            self.assertNotIn('result', market)
            self.assertIsNone(market['admitted_at'])
            if market['status_observed'] == 'active':
                active += 1
            if market['status_observed'] == 'finalized':
                finalized += 1
        self.assertEqual(active, 2)
        self.assertEqual(finalized, 3)
        for event in panel['events']:
            self.assertIsNone(event['kalshi_occurrence_datetime'])
            self.assertIsNone(event['admitted_at'])
        self.assertIs(panel['admit_gate']['admit_py_run'], False)
        stamped = json.loads(orchestrator.PANEL_CAPTURE.read_text())
        stamped['admitted_at'] = '2026-09-23T19:00:00Z'
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            stub = root / 'panel_stub.json'
            admitted = root / 'panel_admitted.json'
            stub.write_text(json.dumps(stamped))
            admitted.write_text(json.dumps(stamped))
            with self.assertRaises(orchestrator.AdmitPyRefused):
                orchestrator.select_panel_path(stub, admitted)
            with self.assertRaises(orchestrator.OrchestratorError):
                orchestrator.load_panel(stub)
            version = json.loads(orchestrator.PANEL_CAPTURE.read_text())
            version['panel_version'] = '2026-09-22.s5-kxmvecrosscategory-v1'
            rejected = root / 'panel_version.json'
            rejected.write_text(json.dumps(version))
            with self.assertRaises(orchestrator.PanelVersionRefused):
                orchestrator.load_panel(rejected)

    def test_reget_honesty_keeps_the_list_429_gaps(self):
        scout = orchestrator.load_scout()
        seed = orchestrator.load_seed()
        reget = orchestrator.load_reget()
        panel = orchestrator.load_panel()
        self.assertEqual(scout['settled_nonempty_result_N'], 20)
        self.assertEqual(seed['settled_nonempty_result_N'], 20)
        self.assertEqual(reget['settled_nonempty_result_N'], 20)
        self.assertEqual(seed['markets'], scout['markets'])
        self.assertEqual(scout['settled_list_http'], '200')
        self.assertIs(scout['settled_list_cursor_present'], True)
        self.assertIsNone(scout['open_list_http'])
        self.assertIsNone(scout['open_list_n'])
        self.assertEqual(scout['parent_seeds_finalized_nonempty_N'], 5)
        self.assertEqual(scout['occurrence_datetime_present_on_settled_N'], 0)
        self.assertEqual(scout['expected_expiration_time_present_on_settled_N'], 20)
        self.assertIsNone(scout['occurrence_datetime_sot_match_all_settled_seeds'])
        self.assertIs(scout['expected_expiration_time_present_all_settled'], True)
        self.assertEqual(scout['http_honesty']['series_SHARD1'], '429_honest')
        self.assertEqual(scout['http_honesty']['finalized_list_KXMVECROSSCATEGORY_attempts'], '429_honest_then_not_required')
        self.assertEqual(seed['finalized_list_attempted_KXMVECROSSCATEGORY'], '429_honest')
        self.assertEqual(seed['settled_list_earlier_attempts'], '429_honest')
        self.assertIsNone(seed['occurrence_datetime_match_all_settled_seeds'])
        self.assertEqual(len(reget['markets']), 20)
        self.assertEqual(reget['honest_gaps'], list(orchestrator.HONEST_GAPS))
        self.assertEqual(orchestrator.list_429_gaps(reget), orchestrator.HONEST_GAPS)
        self.assertIs(reget['occurrence_datetime_key_present'], False)
        self.assertIs(reget['cursor_followed'], False)
        self.assertNotIn('occurrence_datetime', reget)
        self.assertTrue(reget['cursor'])
        for ticker in orchestrator.PARENT_SEED_TICKERS:
            self.assertEqual(scout['parent_seed_results'][ticker], 'no')
            self.assertEqual(scout['parent_seed_statuses'][ticker], 'finalized')
            self.assertNotIn(ticker, reget['markets'])
        self.assertIsNone(panel['results'])
        agreed = orchestrator.occurrence_agreement_tickers(panel)
        self.assertEqual(agreed, orchestrator.SETTLED_TICKERS)
        self.assertEqual(len(agreed), 20)
        parent_agreed = orchestrator.parent_finalized_tickers(panel)
        self.assertEqual(parent_agreed, orchestrator.PARENT_SEED_TICKERS)
        for ticker in orchestrator.PARENT_SEED_TICKERS:
            self.assertNotIn(ticker, agreed)
        for ticker, market in reget['markets'].items():
            self.assertNotIn('occurrence_datetime', market)
            self.assertEqual(orchestrator.clock_pin(market)[0], 'expected_expiration_time')
            self.assertTrue(orchestrator.clock_pin(market)[1].endswith('Z'))
        rows = orchestrator.structural_rows(panel)
        self.assertEqual(len(rows), 29)
        passes = [row for row in rows if row['j0'] == 'nonempty_result_required_pass']
        parents = [row for row in rows if row['j0'] == 'parent_ticker_get_nonempty']
        gaps = [row for row in rows if row['j0'] == 'honest_gap']
        self.assertEqual(len(passes), 20)
        self.assertEqual(len(parents), 5)
        self.assertEqual(len(gaps), 4)
        self.assertEqual(sum(1 for row in passes if row['on_settled_list']), 20)
        self.assertEqual(sum(1 for row in passes if row['j1'] == 'expected_expiration_time_match'), 20)
        self.assertEqual(sum(1 for row in passes if row['single_market_get']), 0)
        self.assertEqual(sum(1 for row in passes if row['result'] == 'yes'), 4)
        self.assertEqual(sum(1 for row in passes if row['result'] == 'no'), 16)
        self.assertTrue(all(row['panel_ticker'] is None for row in passes))
        self.assertEqual(sum(1 for row in parents if row['parent_seed']), 5)
        self.assertEqual(sum(1 for row in parents if row['single_market_get']), 5)
        self.assertTrue(all(row['j1'] == 'occurrence_null_expected_expiration_on_ticker_get' for row in parents))
        self.assertTrue(all(row['panel_ticker'] == row['key'] for row in parents))
        self.assertTrue(all(row['result'] == 'no' for row in parents))
        self.assertEqual({row['key'] for row in gaps}, set(orchestrator.HONEST_GAPS))
        for gap in gaps:
            self.assertIsNone(gap['result'])
            self.assertIsNone(gap['panel_ticker'])
        self.assertIsNone(orchestrator.published_scorecard()['settled_join_n'])
        self.assertIsNone(orchestrator.published_scorecard()['occurrence_match_n'])
        self.assertIsNone(orchestrator.published_scorecard()['admit_ready_flag'])
        present = {'occurrence_datetime': '2026-09-23T21:30:00Z', 'expected_expiration_time': '2026-09-23T21:35:00Z'}
        self.assertEqual(orchestrator.clock_pin(present), ('occurrence_datetime', '2026-09-23T21:30:00Z'))
        absent = {'occurrence_datetime': None, 'expected_expiration_time': '2026-09-23T21:35:00Z'}
        self.assertEqual(orchestrator.clock_pin(absent)[0], 'expected_expiration_time')
        with self.assertRaises(orchestrator.OccurrenceIntegrityRefused):
            orchestrator.clock_pin({'occurrence_datetime': None})

    def test_source_pins_and_accept(self):
        pins = json.loads(orchestrator.SOURCE_PINS.read_text())
        self.assertEqual(pins['freeze_sha256'], orchestrator.FREEZE_SHA256)
        self.assertEqual(pins['scout_reget_sha256'], orchestrator.SCOUT_SHA256)
        self.assertEqual(pins['seed_summary_sha256'], orchestrator.SEED_SHA256)
        self.assertEqual(pins['panel_stub_sha256'], orchestrator.PANEL_STUB_SHA256)
        self.assertEqual(pins['settled_reget_sha256'], orchestrator.REGET_SHA256)
        self.assertEqual(pins['conductor_accept_sha256'], orchestrator.ACCEPT_SHA256)
        self.assertEqual(pins['frozen_experiment_sha256'], orchestrator.FROZEN_SHA256)
        self.assertEqual(pins['empty_results_sha256'], orchestrator.EMPTY_SHA256)
        self.assertIsNone(pins['admitted_at'])
        self.assertIs(pins['does_not_run_admit_py'], True)
        self.assertIs(pins['scout_n_copied_into_settled_join_n'], False)
        self.assertEqual(pins['settled_nonempty_result_N_scout'], 20)
        self.assertIsNone(pins['settled_join_n'])
        self.assertEqual(pins['parent_seed_tickers'], list(orchestrator.PARENT_SEED_TICKERS))
        self.assertEqual(pins['parent_seed_results'], dict(orchestrator.PARENT_SEED_RESULTS))
        self.assertIsNone(pins['seed_panel_result'])
        self.assertEqual(pins['parent_seeds_finalized_nonempty_N'], 5)
        self.assertIs(pins['parent_reget_occurrence_present'], False)
        self.assertEqual(pins['j1_null_occurrence_clock'], 'expected_expiration_time')
        self.assertEqual(pins['occurrence_datetime_present_on_settled_N'], 0)
        self.assertIs(pins['list_429_backfilled'], False)
        self.assertIs(pins['cursor_followed'], False)
        self.assertEqual(pins['settled_list_http'], '200')
        self.assertEqual(pins['finalized_list_429'], '429_honest')
        self.assertEqual(pins['shard1_series_429'], '429_honest')
        self.assertIs(pins['fee_import_used'], False)
        self.assertIs(pins['rails_import_used'], False)
        self.assertIs(pins['filllegs_reopen'], False)
        self.assertIs(pins['mve_fl_reopen'], False)
        self.assertIs(pins['s4_rj_reopen'], False)
        self.assertIs(pins['nhl_rj_reopen'], False)
        self.assertIs(pins['c3_rj_reopen'], False)
        self.assertIs(pins['c5_rj_reopen'], False)
        self.assertIs(pins['r3p3_rj_reopen'], False)
        self.assertIs(pins['r2p3_rj_reopen'], False)
        self.assertIs(pins['conductor_cloud_kick'], False)
        self.assertEqual(pins['arms']['J1'], 'occurrence_datetime_match')
        for key in orchestrator.OUTPUT_KEYS:
            self.assertIsNone(pins[key])
        accept = json.loads(orchestrator.CONDUCTOR_ACCEPT.read_text())
        self.assertEqual(accept['decision'], 'ACCEPT')
        self.assertIs(accept['implement'], True)
        self.assertEqual(accept['hard_refuse'], list(orchestrator.ACCEPT_HARD_REFUSE))
        self.assertIn('copy_scout_N_into_settled_join_n', accept['hard_refuse'])
        self.assertIn('S5_FILLLEGS_reopen', accept['hard_refuse'])
        self.assertIn('MVE_FL_reopen', accept['hard_refuse'])
        self.assertIn('R2P3_RJ_reopen', accept['hard_refuse'])
        self.assertIn('Conductor_pulse_cloud_kick', accept['hard_refuse'])
        self.assertEqual(accept['arms'], dict(orchestrator.ACCEPT_ARMS))
        self.assertIs(accept['digest_verify']['match'], True)
        self.assertEqual(accept['digest_verify']['settled_nonempty_result_N'], 20)
        self.assertEqual(
            accept['digest_verify']['freeze'],
            'cd264a4d41ef055d1cbca80a5dbe6756746211537fb24799dca9dde8980cb799',
        )
        self.assertEqual(
            accept['digest_verify']['scout_reget'],
            '33db60a50f2e7746315f4603b9f78a9260145cb49d0250e141471de46f4df9e3',
        )
        self.assertEqual(
            accept['digest_verify']['settled_reget'],
            '91111f20586a1b684e430baa0e8b62a3fffc7d510de99e43bab7d213dfeb26da',
        )
        hold = json.loads(orchestrator.EXAMINER_HOLD.read_text())
        self.assertEqual(hold['status'], 'HOLD_PRE_PR')
        self.assertIs(hold['stub_ready'], False)
        self.assertIsNone(hold['admitted_at'])
        self.assertEqual(hold['metrics_null'], list(orchestrator.HOLD_METRICS))
        self.assertEqual(hold['settled_list_http'], '200')
        self.assertEqual(hold['finalized_list_http'], '429_honest')
        self.assertEqual(hold['occurrence_datetime_present_on_settled_N'], 0)
        self.assertEqual(hold['expected_expiration_time_present_on_settled_N'], 20)

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
    def test_j0_and_j1_schema_leave_the_scorecard_null(self):
        before = {path: path.read_bytes() for path in _freeze_paths()}
        j0 = orchestrator.conduct(orchestrator.J0)
        j1 = orchestrator.conduct(orchestrator.J1)
        self.assertEqual(j0['join_gate'], 'nonempty_result_required')
        self.assertEqual(j1['join_gate'], 'occurrence_datetime_match')
        self.assertEqual(j0['source'], 'authentic_reget')
        self.assertEqual(j1['source'], 'authentic_reget')
        self.assertEqual(j0['event_count'], 21)
        self.assertEqual(j0['market_count'], 5)
        self.assertEqual(len(j0['row_labels']), 29)
        self.assertEqual(len(j1['occurrence_agreement_tickers']), 20)
        self.assertEqual(len(j1['parent_finalized_tickers']), 5)
        for ticker in orchestrator.PARENT_SEED_TICKERS:
            self.assertNotIn(ticker, j1['occurrence_agreement_tickers'])
            self.assertIn(ticker, j1['parent_finalized_tickers'])
        self.assertIsNone(j0['admitted_at'])
        self.assertIs(j0['list_429_backfilled'], False)
        self.assertIs(j0['cursor_followed'], False)
        self.assertIs(j0['scout_n_copied_into_settled_join_n'], False)
        self.assertIs(j0['admit_py_run'], False)
        self.assertEqual(j0['lee_ready'], 'REFUSED')
        self.assertEqual(j0['examiner_status'], 'HOLD_PRE_PR')
        self.assertIs(j0['stub_ready'], False)
        for report in (j0, j1):
            orchestrator.assert_null_scorecard(report)
            orchestrator.assert_null_scorecard(report['published'])
            self.assertIsNone(report['settled_join_n'])
            self.assertIsNone(report['occurrence_match_n'])
            self.assertIsNone(report['admit_ready_flag'])
            self.assertIsNone(report['results'])
            self.assertIsNone(report['pnl'])
            self.assertFalse(report['promoted'])
            self.assertNotEqual(report['settled_join_n'], 20)
            self.assertNotEqual(report['occurrence_match_n'], 20)
            self.assertNotEqual(report['occurrence_match_n'], 5)
        for path, raw in before.items():
            self.assertEqual(path.read_bytes(), raw)

    def test_unknown_gate_and_scorecard_write_are_refused(self):
        before = {path: path.read_bytes() for path in _freeze_paths()}
        with self.assertRaises(orchestrator.UnknownGate):
            orchestrator.conduct('J2')
        with self.assertRaises(orchestrator.ScorecardPromotionRefused):
            orchestrator.write_scorecard(orchestrator.published_scorecard())
        with self.assertRaises(orchestrator.ScorecardPromotionRefused):
            orchestrator.copy_scout_n_into_settled_join(20)
        for key in orchestrator.OUTPUT_KEYS:
            broken = dict(orchestrator.published_scorecard())
            broken[key] = 1
            with self.assertRaises(orchestrator.ScorecardPromotionRefused):
                orchestrator.write_scorecard(broken)
            broken[key] = 20
            with self.assertRaises(orchestrator.ScorecardPromotionRefused):
                orchestrator.write_scorecard(broken)
        for path, raw in before.items():
            self.assertEqual(path.read_bytes(), raw)


class RefuseTests(unittest.TestCase):
    def test_lee_ready_live_orders_admit_and_reopens_are_refused(self):
        for sample in (None, {}, {'result': 'yes'}, 'quote'):
            with self.assertRaises(orchestrator.LeeReadyRefused):
                orchestrator.infer_lee_ready(sample)
        with self.assertRaises(orchestrator.LeeReadyRefused):
            orchestrator.refuse_adversary('lee_ready')
        for label in (
            'fq_reopen',
            'filllegs_reopen',
            'mve_fl_reopen',
            's4_fq_reopen',
            's4_rj_reopen',
            'nhl_fq_reopen',
            'cpi_fq_reopen',
            'atp_fq_reopen',
            'eth_fq_reopen',
            'cap_sr_reopen',
            'empty_ob_reopen',
            'c3_rj_reopen',
            'c5_rj_reopen',
            'r3p3_rj_reopen',
            'nhl_rj_reopen',
            'r2p3_rj_reopen',
            'arm_b',
            'q7_arm_b',
            'logan_keys',
            'invented_pnl',
            'conductor_pulse_cloud',
        ):
            with self.assertRaises(orchestrator.AdversaryRefused):
                orchestrator.refuse_adversary(label)
        with self.assertRaises(orchestrator.AdmitPyRefused):
            orchestrator.refuse_adversary('admit_py')
        with self.assertRaises(orchestrator.AdmitPyRefused):
            orchestrator.run_admit()
        with self.assertRaises(orchestrator.ScorecardPromotionRefused):
            orchestrator.refuse_adversary('copy_scout_n')
        with self.assertRaises(orchestrator.ExaminerNotReady):
            orchestrator.claim_admit_ready()
        with self.assertRaises(orchestrator.ExaminerNotReady):
            orchestrator.claim_examiner_ready()
        with self.assertRaises(orchestrator.LiveOrdersForbidden):
            orchestrator.execution_adapter()
        with self.assertRaises(orchestrator.LiveOrdersForbidden):
            orchestrator.assert_public_get('POST')
        self.assertIsNone(orchestrator.assert_public_get('GET'))
        for name in ('S1', 'S2', 'R2-P4'):
            with self.assertRaises(orchestrator.UngateRefused):
                orchestrator.ungate(name)
        source = (ROOT / 'orchestrator.py').read_text()
        for banned in (
            '0.0175',
            '0.07',
            'class KalshiExecutionAdapter',
            'urlopen',
            'urllib',
            'os.environ',
            'api_key',
            'private_key',
        ):
            self.assertNotIn(banned, source)

    def test_invented_result_depth_fills_and_list_429_backfill_are_refused(self):
        panel = orchestrator.load_panel()
        reget = orchestrator.load_reget()
        market = next(iter(reget['markets'].values()))
        with self.assertRaises(orchestrator.InventedDepthRefused):
            orchestrator.quote_depth(market)
        self.assertNotIn('orderbook_fp', market)
        with self.assertRaises(orchestrator.InventedFillRefused):
            orchestrator.invent_fill(market, market.get('volume_fp'))
        with self.assertRaises(orchestrator.InventedResultRefused):
            orchestrator.invent_result(market['ticker'], 'no')
        with self.assertRaises(orchestrator.InventedResultRefused):
            orchestrator.backfill_list_429(
                'markets?series_ticker=KXMVECROSSCATEGORY&status=finalized',
                result='yes',
                occurrence_datetime='2026-09-23T21:30:00Z',
            )
        with self.assertRaises(orchestrator.InventedResultRefused):
            orchestrator.backfill_shard1('KXMVECROSSCATEGORY-SHARD1', result='yes')
        with self.assertRaises(orchestrator.InventedMarketRefused):
            orchestrator.follow_settled_cursor(reget['cursor'])
        with self.assertRaises(orchestrator.InventedMarketRefused):
            orchestrator.invent_related_series('KXMVESPORTSMULTIGAMEEXTENDED-EXAMPLE', 'yes')
        with self.assertRaises(orchestrator.InventedResultRefused):
            orchestrator.invent_parent_settlement(orchestrator.PARENT_SEED_TICKERS[0], 'yes')
        with self.assertRaises(orchestrator.InventedResultRefused):
            orchestrator.stamp_panel_result(orchestrator.PARENT_SEED_TICKERS[0], 'no')
        with self.assertRaises(orchestrator.InventedSoTRefused):
            orchestrator.assign_occurrence(orchestrator.SETTLED_TICKERS[0], '2026-09-23T21:35:00Z')
        with self.assertRaises(orchestrator.InventedResultRefused):
            orchestrator.refuse_adversary('list_429_backfill')
        with self.assertRaises(orchestrator.InventedResultRefused):
            orchestrator.refuse_adversary('shard1_backfill')
        with self.assertRaises(orchestrator.InventedResultRefused):
            orchestrator.refuse_adversary('parent_seed_invent')
        with self.assertRaises(orchestrator.InventedMarketRefused):
            orchestrator.refuse_adversary('cursor_follow')
        with self.assertRaises(orchestrator.InventedMarketRefused):
            orchestrator.refuse_adversary('related_series_invent')
        with self.assertRaises(orchestrator.InventedSoTRefused):
            orchestrator.refuse_adversary('invent_occurrence')
        filled = json.loads(orchestrator.PANEL_CAPTURE.read_text())
        filled['events'][0]['result'] = 'yes'
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'panel_stub.json'
            path.write_text(json.dumps(filled))
            with self.assertRaises(orchestrator.InventedResultRefused):
                orchestrator.load_panel(path)
        shifted = json.loads(orchestrator.PANEL_CAPTURE.read_text())
        shifted['events'][0]['kalshi_occurrence_datetime'] = '2026-01-01T00:00:00Z'
        with self.assertRaises(orchestrator.InventedSoTRefused):
            orchestrator.parent_finalized_tickers(shifted)
        invented = json.loads(orchestrator.PANEL_CAPTURE.read_text())
        invented['events'][16]['market_tickers'] = ['KXMVECROSSCATEGORY-SHARD1-INVENTED']
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'panel_markets.json'
            path.write_text(json.dumps(invented))
            with self.assertRaises(orchestrator.InventedMarketRefused):
                orchestrator.load_panel(path)
        rewritten = json.loads(orchestrator.PANEL_CAPTURE.read_text())
        rewritten['markets'][0]['status_observed'] = 'finalized'
        rewritten['markets'][0]['result'] = 'no'
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'panel_result.json'
            path.write_text(json.dumps(rewritten))
            with self.assertRaises(orchestrator.InventedResultRefused):
                orchestrator.load_panel(path)
        self.assertIsNone(panel['results'])
        self.assertEqual(
            orchestrator.PANEL_CAPTURE.read_bytes(),
            (ROOT / 'panel_stub.json').read_bytes(),
        )


if __name__ == '__main__':
    unittest.main()
