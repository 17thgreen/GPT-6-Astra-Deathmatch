"""Unit pins for the R3-P3 FL settled-resolution join harness.

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
        self.assertFalse(orchestrator.R3P3_SCOUT_CITE.exists())
        self.assertFalse(orchestrator.R3P3_PANEL_CITE.exists())
        binding = orchestrator.instrument_binding()
        panel = orchestrator.load_panel()
        frozen = json.loads(orchestrator.FROZEN_EXPERIMENT.read_text())
        self.assertEqual(binding['experiment_id'], 'R3P3-FL-MAKER-TAKER-SETTLED-RESOLUTION-JOIN-HARNESS')
        self.assertEqual(binding['feature_family'], 'R3P3-RJ')
        self.assertEqual(frozen['feature_family'], 'R3P3-RJ')
        self.assertEqual(frozen['status'], 'FROZEN_EXPERIMENT')
        self.assertEqual(binding['knob'], 'join_gate')
        self.assertEqual(frozen['knob'], 'join_gate')
        self.assertEqual(frozen['arm_values'], {
            'J0': 'nonempty_result_required',
            'J1': 'occurrence_datetime_match',
        })
        self.assertEqual(binding['panel_version'], '2026-09-22.r3-p3-fl-maker-taker-v0')
        self.assertEqual(panel['panel_version'], '2026-09-22.r3-p3-fl-maker-taker-v0')
        self.assertIsNone(panel['admitted_at'])
        self.assertIsNone(binding['admitted_at'])
        self.assertIsNone(frozen['admitted_at'])
        self.assertEqual(panel['stub_status'], 'PANEL_SCHEMA_STUB_SEED')
        self.assertEqual(binding['events_n'], 2)
        self.assertEqual(binding['markets_n'], 3)
        self.assertEqual(binding['settled_nonempty_result_N_scout'], 20)
        self.assertEqual(frozen['settled_nonempty_result_N_scout'], 20)
        self.assertIs(binding['scout_n_copied_into_settled_join_n'], False)
        self.assertEqual(binding['parent_seed_tickers'], list(orchestrator.PARENT_SEED_TICKERS))
        self.assertEqual(binding['parent_seeds_finalized_nonempty_N'], 3)
        self.assertEqual(binding['parent_seed_results'], dict(orchestrator.PARENT_SEED_RESULTS))
        self.assertIsNone(binding['seed_panel_result'])
        self.assertEqual(binding['occurrence_datetime_panel_sot'], '2026-09-23T14:00:00Z')
        self.assertIs(binding['list_429_backfilled'], False)
        self.assertEqual(binding['chi_settled_list_429'], '429 too_many_requests')
        self.assertEqual(binding['ny_open_list_429'], '429 too_many_requests')
        self.assertIs(binding['open_ticker_market_invented'], False)
        self.assertEqual(binding['open_tickers_cited'], list(orchestrator.OPEN_TICKERS))
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
        self.assertIs(binding['empty_ob_reopen'], False)
        self.assertIs(binding['r3p3_fee_reopen'], False)
        self.assertIs(binding['c3_rj_reopen'], False)
        self.assertIs(binding['c5_rj_reopen'], False)
        self.assertIs(binding['arm_b_touch'], False)
        self.assertIs(binding['admit_py_run'], False)
        self.assertEqual(binding['does_not_ungate'], ['S1', 'S2', 'R2-P4'])
        self.assertIs(binding['s1_s2_r2p4_ungated'], False)
        self.assertEqual(binding['examiner_status'], 'NOT_SCORED')
        self.assertIs(binding['stub_ready'], False)
        self.assertEqual(tuple(frozen['arms']), orchestrator.ARMS)
        self.assertEqual(binding['freeze_sha256'], orchestrator.FREEZE_SHA256)
        self.assertEqual(binding['scout_reget_sha256'], orchestrator.SCOUT_SHA256)
        self.assertEqual(binding['seed_summary_sha256'], orchestrator.SEED_SHA256)
        self.assertEqual(binding['panel_stub_sha256'], orchestrator.PANEL_STUB_SHA256)
        self.assertEqual(binding['settled_reget_sha256'], orchestrator.REGET_SHA256)
        self.assertEqual(binding['source_pins_sha256'], orchestrator.SOURCE_PINS_SHA256)
        self.assertEqual(binding['base_commit'], orchestrator.BASE_COMMIT)
        self.assertEqual(binding['row_label_count'], 23)
        self.assertIsNone(binding['results'])
        self.assertIsNone(binding['pnl'])
        self.assertIsNone(binding['settled_join_n'])
        self.assertIsNone(binding['occurrence_match_n'])
        self.assertIsNone(binding['admit_ready_flag'])
        self.assertIsNone(frozen['results'])
        self.assertIsNone(frozen['pnl'])
        self.assertNotEqual(binding['settled_join_n'], binding['settled_nonempty_result_N_scout'])
        self.assertNotEqual(binding['settled_join_n'], binding['parent_seeds_finalized_nonempty_N'])
        self.assertNotEqual(binding['occurrence_match_n'], 3)
        pins = orchestrator.conductor_pin_status()
        self.assertIs(pins['conductor_bytes_in_checkout'], True)
        self.assertIs(pins['governance_r3p3_cites_present'], False)
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
        self.assertEqual(orchestrator.sha256_file(orchestrator.PACKET), orchestrator.FREEZE_SHA256)
        self.assertEqual(orchestrator.sha256_file(orchestrator.SCOUT_PATH), orchestrator.SCOUT_SHA256)
        self.assertEqual(orchestrator.sha256_file(orchestrator.SEED_PATH), orchestrator.SEED_SHA256)
        self.assertEqual(orchestrator.sha256_file(orchestrator.PANEL_CAPTURE), orchestrator.PANEL_STUB_SHA256)
        self.assertEqual(orchestrator.sha256_file(orchestrator.REGET_PATH), orchestrator.REGET_SHA256)
        self.assertEqual(orchestrator.sha256_file(orchestrator.CONDUCTOR_ACCEPT), orchestrator.ACCEPT_SHA256)
        self.assertEqual(orchestrator.sha256_file(orchestrator.FROZEN_EXPERIMENT), orchestrator.FROZEN_SHA256)
        self.assertEqual(orchestrator.sha256_file(orchestrator.EMPTY_RESULTS), orchestrator.EMPTY_SHA256)
        self.assertEqual(orchestrator.sha256_file(orchestrator.SOURCE_PINS), orchestrator.SOURCE_PINS_SHA256)
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
        for path in (
            orchestrator.EMPTY_RESULTS,
            orchestrator.LAB_BUNDLE / 'results.json',
            orchestrator.LAB_BUNDLE / 'results' / 'EMPTY_RESULTS.json',
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
        self.assertEqual(published['examiner_status'], 'NOT_SCORED')
        self.assertIs(published['stub_ready'], False)
        self.assertEqual(published['lee_ready'], 'REFUSED')
        self.assertIs(published['scout_n_copied_into_settled_join_n'], False)

    def test_panel_stub_admitted_at_stays_null(self):
        self.assertEqual(orchestrator.select_panel_path(), orchestrator.PANEL_CAPTURE)
        panel = orchestrator.load_panel()
        self.assertEqual(panel['packet_id'], 'R3-P3-FL-MAKER-TAKER')
        self.assertIsNone(panel['results'])
        self.assertIsNone(panel['pnl'])
        self.assertEqual(panel['cohort_counts']['settled_markets_resolved_n'], 0)
        self.assertEqual(len(panel['events']), 2)
        self.assertEqual(len(panel['markets']), 3)
        for event in panel['events']:
            self.assertIsNone(event['admitted_at'])
            self.assertEqual(event['occurrence_datetime'], orchestrator.OCCURRENCE_SOT)
        for market in panel['markets']:
            self.assertIsNone(market['admitted_at'])
            self.assertIsNone(market['result'])
            self.assertEqual(market['status_at_stub'], 'active')
            self.assertEqual(market['occurrence_datetime'], orchestrator.OCCURRENCE_SOT)
        self.assertEqual(
            [market['market_ticker'] for market in panel['markets']],
            list(orchestrator.PARENT_SEED_TICKERS),
        )
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
            version['panel_version'] = '2026-09-22.r3-p3-fl-maker-taker-v1'
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
        self.assertEqual(len(reget['markets']), 21)
        self.assertEqual(reget['honest_gaps'], {
            'markets_settled_KXHIGHCHI': '429 too_many_requests',
            'markets_open_KXHIGHNY': '429 too_many_requests',
        })
        self.assertEqual(orchestrator.list_429_gaps(reget), orchestrator.GAP_KEYS)
        for key in orchestrator.GAP_KEYS:
            self.assertNotIn(key, reget['markets'])
        chi_gap = reget['artifacts']['markets_settled_KXHIGHCHI_lim20.json']
        ny_open_gap = reget['artifacts']['markets_open_KXHIGHNY_lim4.json']
        self.assertEqual(chi_gap['error']['code'], 'too_many_requests')
        self.assertEqual(ny_open_gap['error']['code'], 'too_many_requests')
        self.assertNotIn('markets', chi_gap)
        self.assertNotIn('markets', ny_open_gap)
        opens = reget['artifacts']['markets_open_KXHIGHCHI_lim4.json']['markets']
        self.assertEqual([market['ticker'] for market in opens], list(orchestrator.OPEN_TICKERS))
        self.assertEqual([market['status'] for market in opens], ['active', 'active', 'active', 'active'])
        self.assertEqual([market['result'] for market in opens], ['', '', '', ''])
        for ticker in orchestrator.OPEN_TICKERS:
            self.assertNotIn(ticker, reget['markets'])
        for ticker, result in orchestrator.PARENT_SEED_RESULTS.items():
            market = reget['markets'][ticker]
            self.assertEqual(market['status'], 'finalized')
            self.assertEqual(market['result'], result)
            self.assertEqual(market['occurrence_datetime'], orchestrator.OCCURRENCE_SOT)
            self.assertNotIn('orderbook_fp', market)
        for market in panel['markets']:
            self.assertIsNone(market['result'])
        agreed = orchestrator.occurrence_agreement_tickers(panel)
        self.assertEqual(len(agreed), 3)
        self.assertEqual(agreed, orchestrator.PARENT_SEED_TICKERS)
        for ticker in orchestrator.OPEN_TICKERS:
            self.assertNotIn(ticker, agreed)
        rows = orchestrator.structural_rows(panel)
        self.assertEqual(len(rows), 23)
        passes = [row for row in rows if row['j0'] == 'nonempty_result_required_pass']
        gaps = [row for row in rows if row['j0'] == 'honest_429_gap']
        self.assertEqual(len(passes), 21)
        self.assertEqual(sum(1 for row in passes if row['on_settled_list']), 20)
        seed_rows = [row for row in passes if row['parent_seed']]
        self.assertEqual(len(seed_rows), 3)
        self.assertEqual({row['key'] for row in seed_rows}, set(orchestrator.PARENT_SEED_TICKERS))
        chi = [row for row in seed_rows if row['key'] == orchestrator.CHI_SEED][0]
        self.assertIs(chi['on_settled_list'], False)
        self.assertEqual(chi['result'], 'yes')
        self.assertEqual(chi['j1'], 'occurrence_datetime_match')
        self.assertEqual({row['key'] for row in gaps}, set(orchestrator.GAP_KEYS))
        for gap in gaps:
            self.assertIsNone(gap['result'])
            self.assertIsNone(gap['panel_ticker'])
            self.assertEqual(gap['j1'], 'honest_429_gap')
        self.assertEqual(sum(1 for row in passes if row['result'] == 'yes'), 4)
        self.assertEqual(sum(1 for row in passes if row['result'] == 'no'), 17)
        self.assertIsNone(orchestrator.published_scorecard()['settled_join_n'])
        self.assertIsNone(orchestrator.published_scorecard()['occurrence_match_n'])
        self.assertIsNone(orchestrator.published_scorecard()['admit_ready_flag'])

    def test_source_pins_and_accept(self):
        pins = json.loads(orchestrator.SOURCE_PINS.read_text())
        self.assertEqual(pins['freeze_sha256'], orchestrator.FREEZE_SHA256)
        self.assertEqual(pins['scout_reget_sha256'], orchestrator.SCOUT_SHA256)
        self.assertEqual(pins['seed_summary_sha256'], orchestrator.SEED_SHA256)
        self.assertEqual(pins['panel_stub_sha256'], orchestrator.PANEL_STUB_SHA256)
        self.assertEqual(pins['settled_reget_sha256'], orchestrator.REGET_SHA256)
        self.assertEqual(pins['frozen_experiment_sha256'], orchestrator.FROZEN_SHA256)
        self.assertEqual(pins['empty_results_sha256'], orchestrator.EMPTY_SHA256)
        self.assertEqual(pins['governance_r3p3_cites'], 'absent')
        self.assertIsNone(pins['admitted_at'])
        self.assertIs(pins['does_not_run_admit_py'], True)
        self.assertIs(pins['scout_n_copied_into_settled_join_n'], False)
        self.assertEqual(pins['settled_nonempty_result_N_scout'], 20)
        self.assertIsNone(pins['settled_join_n'])
        self.assertEqual(pins['parent_seed_tickers'], list(orchestrator.PARENT_SEED_TICKERS))
        self.assertEqual(pins['parent_seed_results'], dict(orchestrator.PARENT_SEED_RESULTS))
        self.assertIsNone(pins['seed_panel_result'])
        self.assertIs(pins['list_429_backfilled'], False)
        self.assertEqual(pins['chi_settled_list_429'], '429 too_many_requests')
        self.assertEqual(pins['ny_open_list_429'], '429 too_many_requests')
        self.assertIs(pins['open_ticker_market_invented'], False)
        self.assertIs(pins['fee_import_used'], False)
        self.assertIs(pins['rails_import_used'], False)
        self.assertIs(pins['r3p3_fee_reopen'], False)
        self.assertIs(pins['c3_rj_reopen'], False)
        self.assertIs(pins['c5_rj_reopen'], False)
        for key in orchestrator.OUTPUT_KEYS:
            self.assertIsNone(pins[key])
        accept = json.loads(orchestrator.CONDUCTOR_ACCEPT.read_text())
        self.assertEqual(accept['decision'], 'ACCEPT')
        self.assertIs(accept['implement'], True)
        self.assertEqual(accept['hard_refuse'], list(orchestrator.ACCEPT_HARD_REFUSE))
        self.assertIn('C3_RJ_reopen', accept['hard_refuse'])
        self.assertIn('C5_RJ_reopen', accept['hard_refuse'])
        self.assertIs(accept['digest_verify']['match'], True)
        self.assertEqual(accept['digest_verify']['settled_nonempty_result_N'], 20)

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
        self.assertEqual(j0['event_count'], 2)
        self.assertEqual(j0['market_count'], 3)
        self.assertEqual(len(j0['row_labels']), 23)
        self.assertEqual(len(j1['occurrence_agreement_tickers']), 3)
        for ticker in orchestrator.PARENT_SEED_TICKERS:
            self.assertIn(ticker, j1['occurrence_agreement_tickers'])
        for ticker in orchestrator.OPEN_TICKERS:
            self.assertNotIn(ticker, j1['occurrence_agreement_tickers'])
        self.assertIsNone(j0['admitted_at'])
        self.assertIs(j0['list_429_backfilled'], False)
        self.assertIs(j0['scout_n_copied_into_settled_join_n'], False)
        self.assertIs(j0['admit_py_run'], False)
        self.assertEqual(j0['lee_ready'], 'REFUSED')
        self.assertEqual(j0['examiner_status'], 'NOT_SCORED')
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
            self.assertNotEqual(report['settled_join_n'], 21)
            self.assertNotEqual(report['occurrence_match_n'], 3)
        for path, raw in before.items():
            self.assertEqual(path.read_bytes(), raw)

    def test_unknown_gate_and_scorecard_write_are_refused(self):
        before = {path: path.read_bytes() for path in _freeze_paths()}
        with self.assertRaises(orchestrator.UnknownGate):
            orchestrator.conduct('J2')
        with self.assertRaises(orchestrator.ScorecardPromotionRefused):
            orchestrator.write_scorecard(orchestrator.published_scorecard())
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
            'eth_fq_reopen',
            'nhl_fq_reopen',
            'cpi_fq_reopen',
            'atp_fq_reopen',
            'cap_sr_reopen',
            'empty_ob_reopen',
            'r3p3_fee_reopen',
            'c3_rj_reopen',
            'c5_rj_reopen',
            'arm_b',
            'q7_arm_b',
            'logan_keys',
            'invented_pnl',
        ):
            with self.assertRaises(orchestrator.AdversaryRefused):
                orchestrator.refuse_adversary(label)
        with self.assertRaises(orchestrator.AdmitPyRefused):
            orchestrator.refuse_adversary('admit_py')
        with self.assertRaises(orchestrator.AdmitPyRefused):
            orchestrator.run_admit()
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
        market = reget['markets'][orchestrator.CHI_SEED]
        with self.assertRaises(orchestrator.InventedDepthRefused):
            orchestrator.quote_depth(market)
        self.assertNotIn('orderbook_fp', market)
        with self.assertRaises(orchestrator.InventedFillRefused):
            orchestrator.invent_fill(market, market.get('volume_fp'))
        with self.assertRaises(orchestrator.InventedResultRefused):
            orchestrator.invent_result(orchestrator.CHI_SEED, 'no')
        with self.assertRaises(orchestrator.InventedResultRefused):
            orchestrator.backfill_list_429(
                'markets_settled_KXHIGHCHI',
                result='yes',
                occurrence_datetime='2026-09-23T14:00:00Z',
            )
        with self.assertRaises(orchestrator.InventedSoTRefused):
            orchestrator.assign_occurrence('markets_open_KXHIGHNY', '2026-09-23T14:00:00Z')
        with self.assertRaises(orchestrator.InventedMarketRefused):
            orchestrator.invent_open_ticker(orchestrator.OPEN_TICKERS[0], 'yes')
        with self.assertRaises(orchestrator.InventedResultRefused):
            orchestrator.refuse_adversary('list_429_backfill')
        with self.assertRaises(orchestrator.InventedMarketRefused):
            orchestrator.refuse_adversary('open_ticker_invent')
        filled = json.loads(orchestrator.PANEL_CAPTURE.read_text())
        filled['markets'][0]['result'] = 'yes'
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'panel_stub.json'
            path.write_text(json.dumps(filled))
            with self.assertRaises(orchestrator.InventedResultRefused):
                orchestrator.load_panel(path)
        shifted = json.loads(orchestrator.PANEL_CAPTURE.read_text())
        shifted['markets'][0]['occurrence_datetime'] = '2026-01-01T00:00:00Z'
        with self.assertRaises(orchestrator.OccurrenceIntegrityRefused):
            orchestrator.occurrence_agreement_tickers(shifted)
        self.assertIsNone(panel['markets'][0]['result'])
        self.assertEqual(
            orchestrator.PANEL_CAPTURE.read_bytes(),
            (ROOT / 'panel_stub.json').read_bytes(),
        )


if __name__ == '__main__':
    unittest.main()
