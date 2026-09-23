"""Unit pins for the Cap-SR effects path.

Synthetic fixtures check the join schema and the imported soft-policy pins.
They are not a historical walk and they are not profit.
"""
import gzip
import hashlib
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

import effects_path as effects
import soft_policy as soft


def _git(args):
    return subprocess.run(
        ['git', *args],
        cwd=PARENT,
        capture_output=True,
        text=True,
        check=False,
    )


class PinTests(unittest.TestCase):
    def test_constants_match_the_freeze(self):
        frozen = json.loads(effects.FROZEN_EXPERIMENT.read_text())
        empty = json.loads(effects.EMPTY_RESULTS.read_text())
        self.assertEqual(frozen['experiment'], effects.EXPERIMENT)
        self.assertEqual(frozen['directory'], effects.DIRECTORY)
        self.assertEqual(frozen['feature_family'], effects.FEATURE_FAMILY)
        self.assertEqual(frozen['knob'], 'fixture_stress')
        self.assertEqual([arm['id'] for arm in frozen['arms']], list(effects.FX_ARMS))
        self.assertEqual(frozen['arms'][0]['fixture_stress'], effects.FX0_STRESS)
        self.assertEqual(frozen['arms'][1]['fixture_stress'], effects.FX1_STRESS)
        self.assertEqual(tuple(frozen['soft_policies_fixed']), effects.SOFT_POLICIES_FIXED)
        self.assertEqual(tuple(frozen['soft_policies_fixed']), (
            soft.SR0_POLICY, soft.SR1_POLICY, soft.SR2_POLICY,
        ))
        self.assertEqual(frozen['C_total_usd'], 5000)
        self.assertEqual(effects.soft.C_TOTAL, Decimal('5000'))
        self.assertEqual(frozen['strategy_pointer'], 'Q6-000')
        self.assertEqual(frozen['fee_pin'], effects.FEEBOOK_COMMIT)
        self.assertEqual(frozen['rails_pin'], effects.RAILS_COMMIT)
        self.assertEqual(frozen['parent_cap_sr_pin'], effects.PARENT_CAP_SR_PIN_PREFIX)
        self.assertTrue(effects.PARENT_CAP_SR_PIN.startswith(frozen['parent_cap_sr_pin']))
        self.assertEqual(frozen['parent_cap_sr_freeze_sha256'], effects.PARENT_CAP_SR_FREEZE_SHA256)
        self.assertEqual(frozen['packet_sha256'], effects.PACKET_SHA256)
        self.assertIs(frozen['signal_retune_000'], False)
        self.assertIs(frozen['queue_fragility_reopen'], False)
        self.assertIs(frozen['dual_cap_sr_lab'], False)
        self.assertEqual(tuple(frozen['scorecard_fields']), effects.SCORECARD_FIELDS)
        self.assertIsNone(frozen['results'])
        self.assertIsNone(frozen['pnl'])
        self.assertEqual(empty['status'], 'EMPTY_RESULTS_PRE_EXAMINER')
        for key in effects.NULL_FIELDS:
            self.assertIsNone(empty[key])
        published = effects.published_scorecard()
        self.assertTrue(all(published[key] is None for key in effects.NULL_FIELDS))
        self.assertIn('cfd5f95a', frozen['go'])

    def test_packet_copies_and_missing_governance_tree(self):
        self.assertFalse(effects.GOVERNANCE_TREE.exists())
        copies = (
            effects.PACKET,
            effects.GOVERNANCE_PACKET,
            effects.LAB_BUNDLE / effects.PACKET.name,
            effects.GOVERNANCE_BUNDLE / effects.PACKET.name,
        )
        digest = hashlib.sha256(effects.PACKET.read_bytes()).hexdigest()
        self.assertEqual(digest, effects.PACKET_SHA256)
        for path in copies:
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), digest)
        parent = hashlib.sha256(effects.PARENT_FREEZE.read_bytes()).hexdigest()
        self.assertEqual(parent, effects.PARENT_CAP_SR_FREEZE_SHA256)
        frozen_bytes = effects.FROZEN_EXPERIMENT.read_bytes()
        for path in (
            effects.FROZEN_EXPERIMENT,
            effects.LAB_BUNDLE / 'FROZEN_EXPERIMENT.json',
            effects.GOVERNANCE_BUNDLE / 'FROZEN_EXPERIMENT.json',
        ):
            self.assertEqual(path.read_bytes(), frozen_bytes)
            payload = json.loads(path.read_text())
            self.assertIsNone(payload['results'])
            self.assertIsNone(payload['pnl'])
        empty_bytes = effects.EMPTY_RESULTS.read_bytes()
        for path in (
            effects.EMPTY_RESULTS,
            effects.LAB_BUNDLE / 'results.json',
            effects.GOVERNANCE_BUNDLE / 'results.json',
        ):
            self.assertEqual(path.read_bytes(), empty_bytes)

    def test_cap_sr_import_pin_and_no_second_soft_policy(self):
        binding = effects.instrument_binding()
        module = Path(soft.__file__).resolve()
        self.assertEqual(module, (PARENT / effects.CAP_SR_LAB / 'soft_policy.py').resolve())
        self.assertEqual(Path(effects.soft.__file__).resolve(), module)
        self.assertIs(effects.soft.open_account, soft.open_account)
        self.assertIs(effects.soft.proportional_takes, soft.proportional_takes)
        self.assertEqual(binding['cap_sr_lab'], effects.CAP_SR_LAB)
        self.assertEqual(binding['cap_sr_pin'], effects.PARENT_CAP_SR_PIN)
        self.assertEqual(binding['soft_policies_fixed'], effects.SOFT_POLICIES_FIXED)
        self.assertIs(binding['dual_cap_sr_lab'], False)
        self.assertEqual(binding['knob'], 'fixture_stress')
        source = (ROOT / 'effects_path.py').read_text()
        for banned in (
            'def proportional_takes',
            'def _plan_blend',
            'def _plan_proportional',
            'class SoftReserveAccount',
            'class KalshiExecutionAdapter',
            'import queue_fragility',
            'factorial_policy',
            'paircheck_policy',
            '0.0175',
            '0.07',
            'Hamilton',
        ):
            self.assertNotIn(banned, source)
        self.assertNotIn("['cash_after']", source)
        self.assertNotIn("['initial_queue']", source)
        found = sorted(path.relative_to(PARENT).as_posix() for path in PARENT.glob('*/soft_policy.py'))
        self.assertEqual(found, ['kalshi_soft_blended_reserves_000_lab_20260923/soft_policy.py'])
        blended = sorted(path.name for path in PARENT.glob('kalshi_soft_blended_*'))
        self.assertEqual(blended, ['kalshi_soft_blended_reserves_000_lab_20260923'])
        self.assertEqual(list(ROOT.rglob('admit.py')), [])

    def test_feebook_rails_and_cap_sr_commits_are_unchanged(self):
        for commit, path in (
            (effects.FEEBOOK_COMMIT, 'kalshi_feebook_lab_20260922'),
            (effects.RAILS_COMMIT, 'kalshi_rails_lab_20260922'),
            (effects.PARENT_CAP_SR_PIN, 'kalshi_soft_blended_reserves_000_lab_20260923'),
        ):
            diff = _git(['diff', '--exit-code', commit, '--', path])
            self.assertEqual(diff.returncode, 0, diff.stdout + diff.stderr)
            ancestor = _git(['merge-base', '--is-ancestor', commit, 'HEAD'])
            self.assertEqual(ancestor.returncode, 0, ancestor.stderr)
        binding = effects.instrument_binding()
        self.assertEqual(binding['fee_source'], 'feebook')
        self.assertEqual(binding['queue_source'], 'rails')
        self.assertEqual(binding['fee_pin'], effects.FEEBOOK_COMMIT)
        self.assertEqual(binding['rails_pin'], effects.RAILS_COMMIT)
        self.assertIs(binding['fee_is_knob'], False)
        self.assertIs(binding['queue_is_knob'], False)
        self.assertEqual(binding['strategy_pointer'], 'Q6-000')
        self.assertEqual(
            binding['primary_queue_ahead'],
            soft.rails.scenario_queue('q3300'),
        )
        self.assertEqual(binding['examiner_formula_id'], soft.feebook.EXAMINER_FORMULA_ID)
        self.assertTrue(binding['parent_capital_lab_pin'].startswith('ce4671b8'))
        manifest = json.loads(
            (PARENT / 'nfl_factorial_lab_20260921' / 'DELIVERY_MANIFEST.json').read_text()
        )
        by_path = {row['path']: row['sha256'] for row in manifest['files']}
        self.assertEqual(
            by_path['results/q3300_d0.25_000_fills.jsonl.gz'],
            effects.PRIMARY_FILLS_SHA256,
        )
        self.assertEqual(
            by_path['results/q3300_d0.25_000_orders.jsonl.gz'],
            effects.PRIMARY_ORDERS_SHA256,
        )

    def test_other_labs_stay_untouched(self):
        untouched = (
            'kalshi_soft_blended_reserves_000_lab_20260923',
            'kalshi_capital_structure_lab_20260922',
            'kalshi_feebook_lab_20260922',
            'kalshi_rails_lab_20260922',
            'nfl_factorial_lab_20260921',
            'nfl_paircheck_lab_20260922',
            'kalshi_queue_fragility_000_lab_20260922',
            'kalshi_c1_kxufcfight_honesty_lab_20260922',
            'kalshi_c3_kxhighny_bordering_lab_20260923',
            'kalshi_c5_kxbtc15m_honesty_lab_20260923',
            'kalshi_r3p3_fl_maker_taker_lab_20260923',
            'kalshi_r3_p1_fee_cost_lab_20260922',
            'kalshi_r3_p4_l2_shape_lab_20260922',
            'lab/astra-capture',
            'packets/SOFT_BLENDED_RESERVES_000',
            'packets/SOFT_BLENDED_RESERVES_000_FREEZE_2026-09-23.md',
        )
        diff = _git(['diff', '--exit-code', effects.BASE_COMMIT, '--', *untouched])
        self.assertEqual(diff.returncode, 0, diff.stdout + diff.stderr)

    def test_fx0_schema_standin_and_resolve(self):
        joined = effects.join_ledgers(
            effects.SYNTHETIC_FILLS,
            effects.SYNTHETIC_ORDERS,
            arm=effects.FX0,
            fixture_stress=effects.FX0_STRESS,
            source='synthetic_schema_standin',
        )
        self._assert_join_schema(
            joined, effects.FX0, effects.FX0_STRESS, 'synthetic_schema_standin',
        )
        report = joined.report
        self.assertEqual(report['row_count'], 2)
        self.assertEqual(report['labels'][0]['role'], 'maker')
        self.assertEqual(report['labels'][1]['role'], 'taker')
        self.assertIn('outcome_mid_at_fill', report['ignored_fill_keys'])
        for policy in soft.ARMS:
            instrument = report['policy_instrument'][policy]
            self.assertFalse(instrument['borrow_log_nonempty'])
            self.assertFalse(instrument['blend_log_nonempty'])
            self.assertEqual(instrument['seated_fills'], 2)
            self.assertIsNone(instrument['results'])
            self.assertIsNone(instrument['pnl'])
        choice = effects.resolve_fx0()
        if choice['production_present']:
            self.assertEqual(choice['source'], 'production_pin')
            self.assertEqual(effects.sha256_file(choice['fills_path']), effects.PRIMARY_FILLS_SHA256)
            self.assertEqual(effects.sha256_file(choice['orders_path']), effects.PRIMARY_ORDERS_SHA256)
        else:
            self.assertEqual(choice['source'], 'synthetic_schema_standin')
            self.assertFalse(effects.production_present())
            live = effects.join_fx0()
            self.assertEqual(live.report['source'], 'synthetic_schema_standin')
            self.assertEqual(live.report['arm'], effects.FX0)
            self.assertIsNone(live.report['effects_path_fixture_id'])

    def test_fx0_refuses_a_bad_or_partial_production_pin(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fills, orders = effects.production_paths(root)
            fills.parent.mkdir(parents=True)
            with gzip.open(fills, 'wt', encoding='utf-8') as handle:
                handle.write('{}\n')
            with self.assertRaises(effects.EffectsPathError) as incomplete:
                effects.resolve_fx0(root)
            self.assertIn('incomplete', str(incomplete.exception))
            with gzip.open(orders, 'wt', encoding='utf-8') as handle:
                handle.write('{}\n')
            with self.assertRaises(effects.EffectsPathError) as mismatched:
                effects.resolve_fx0(root)
            self.assertIn('sha256', str(mismatched.exception))
        with self.assertRaises(effects.EffectsPathError):
            effects.join_ledgers(
                Path('q10000_d0.25_000_fills.jsonl.gz'),
                Path('q10000_d0.25_000_orders.jsonl.gz'),
                arm=effects.FX0,
                fixture_stress=effects.FX0_STRESS,
                source='refused',
            )
        with self.assertRaises(effects.EffectsPathError):
            effects.join_ledgers(
                Path('synthetic_q3300_d0.25_001_fills.jsonl'),
                Path('synthetic_q3300_d0.25_001_orders.jsonl'),
                arm=effects.FX0,
                fixture_stress=effects.FX0_STRESS,
                source='refused',
            )

    def test_fx1_forces_borrow_and_blend_with_null_scorecard(self):
        frozen_before = effects.FROZEN_EXPERIMENT.read_bytes()
        empty_before = effects.EMPTY_RESULTS.read_bytes()
        joined = effects.join_fx1()
        report = joined.report
        self._assert_join_schema(
            joined, effects.FX1, effects.FX1_STRESS, 'synthetic_borrow_stress',
        )
        self.assertEqual(report['row_count'], 2)
        self.assertNotEqual(report['source'], 'production_pin')
        instrument = report['policy_instrument']
        self.assertTrue(instrument[soft.SR0]['borrow_log_nonempty'])
        self.assertFalse(instrument[soft.SR0]['blend_log_nonempty'])
        self.assertTrue(instrument[soft.SR1]['borrow_log_nonempty'])
        self.assertFalse(instrument[soft.SR1]['blend_log_nonempty'])
        self.assertFalse(instrument[soft.SR2]['borrow_log_nonempty'])
        self.assertTrue(instrument[soft.SR2]['blend_log_nonempty'])
        self.assertEqual(instrument[soft.SR0]['seated_fills'], 2)
        first, second = report['labels']
        self.assertFalse(first['policies'][soft.SR0]['cross_event_borrow'])
        self.assertTrue(second['policies'][soft.SR0]['cross_event_borrow'])
        self.assertTrue(second['policies'][soft.SR1]['cross_event_borrow'])
        self.assertFalse(first['policies'][soft.SR2]['blend_draw'])
        self.assertTrue(second['policies'][soft.SR2]['blend_draw'])
        self.assertFalse(second['policies'][soft.SR2]['cross_event_borrow'])
        self.assertIsNone(report['borrow_count_delta_vs_fifo'])
        self.assertIsNone(report['blend_utilization_gap'])
        self.assertIsNone(report['soft_breach_or_blend_rate'])
        self.assertIsNone(report['effects_path_fixture_id'])
        self.assertEqual(effects.FROZEN_EXPERIMENT.read_bytes(), frozen_before)
        self.assertEqual(effects.EMPTY_RESULTS.read_bytes(), empty_before)
        cohort = set(soft.development_cohort_event_ids())
        self.assertIn(report['labels'][0]['event_id'], cohort)

    def test_residual_stays_non_trading(self):
        joined = effects.join_fx1()
        for policy in soft.ARMS:
            book = joined.accounts[policy]
            self.assertIsInstance(book, soft.SoftReserveAccount)
            self.assertEqual(book.non_trading_residual_bucket, Decimal('9'))
            self.assertEqual(book.residual_policy, soft.RESIDUAL_POLICY)
            self.assertEqual(book.identity(), Decimal('5000'))
            self.assertEqual(book.c_total, Decimal('5000'))
            with self.assertRaises(soft.capital.ResidualNotTradable):
                book.draw_residual(Decimal('1'))
            self.assertEqual(book.non_trading_residual_bucket, Decimal('9'))
            self.assertEqual(book.identity(), Decimal('5000'))

    def test_wallet_sum_is_forbidden(self):
        book = effects.open_account(soft.SR0)
        with self.assertRaises(soft.capital.IndependentWalletSumForbidden):
            effects.compare_independent_wallets_to_shared_account(
                [Decimal('2500'), Decimal('2500')],
            )
        with self.assertRaises(soft.capital.IndependentWalletSumForbidden):
            effects.promotion_scoreboard(book, wallets=[Decimal('5000')])
        with self.assertRaises(soft.ClosedArm):
            effects.open_account(soft.capital.A1)
        with self.assertRaises(soft.ClosedArm):
            effects.open_account('A3')
        board = effects.promotion_scoreboard(book)
        self.assertEqual(board['promotion_scoreboard'], 'shared_account_only')
        self.assertEqual(board['c_total'], Decimal('5000'))
        self.assertIsNone(board['pnl'])
        self.assertIsNone(board['borrow_count_delta_vs_fifo'])
        self.assertIsNone(board['effects_path_fixture_id'])
        self.assertNotIn('wallet_total', board)
        source = (ROOT / 'effects_path.py').read_text()
        self.assertNotIn('sum(wallets', source)
        self.assertNotIn('C_TOTAL * 3', source)

    def test_scorecard_write_and_live_orders_are_refused(self):
        with self.assertRaises(effects.ScorecardPromotionRefused):
            effects.write_scorecard(effects.published_scorecard())
        filled = effects.published_scorecard()
        filled['borrow_count_delta_vs_fifo'] = 1
        with self.assertRaises(effects.ScorecardPromotionRefused):
            effects.assert_null_scorecard(filled)
        with self.assertRaises(soft.capital.LiveOrdersForbidden):
            effects.execution_adapter()
        binding = effects.instrument_binding()
        self.assertIs(binding['live_orders'], False)
        self.assertIs(binding['signal_retune_000'], False)
        self.assertIs(binding['queue_fragility_reopen'], False)
        spec = (ROOT / 'EXPERIMENT_SPEC.md').read_text()
        self.assertIn('PANEL_SCHEMA_STUB_EMPTY_EVENTS', spec)
        self.assertIn('not a second soft_policy lab', spec)

    def _assert_join_schema(self, joined, arm, stress, source):
        report = joined.report
        self.assertEqual(report['arm'], arm)
        self.assertEqual(report['fixture_stress'], stress)
        self.assertEqual(report['source'], source)
        self.assertEqual(report['strategy_pointer'], 'Q6-000')
        self.assertEqual(report['cap_sr_lab'], effects.CAP_SR_LAB)
        self.assertEqual(report['cap_sr_pin'], effects.PARENT_CAP_SR_PIN)
        self.assertEqual(report['fee_pin'], effects.FEEBOOK_COMMIT)
        self.assertEqual(report['rails_pin'], effects.RAILS_COMMIT)
        self.assertEqual(report['fee_source'], 'feebook')
        self.assertEqual(report['queue_source'], 'rails')
        self.assertEqual(report['c_total_usd'], Decimal('5000'))
        self.assertEqual(report['residual_usd'], Decimal('9'))
        self.assertEqual(report['identity_usd'], Decimal('5000'))
        self.assertEqual(report['promotion_scoreboard'], 'shared_account_only')
        self.assertEqual(report['residual_policy'], 'non_trading_residual_bucket')
        self.assertIs(report['dual_cap_sr_lab'], False)
        self.assertIs(report['signal_retune_000'], False)
        self.assertIs(report['queue_fragility_reopen'], False)
        self.assertIs(report['live_orders'], False)
        self.assertIs(report['promoted'], False)
        effects.assert_null_scorecard(report)
        effects.assert_null_scorecard(report['published'])
        self.assertEqual(set(report['policy_instrument']), set(soft.ARMS))
        self.assertGreater(report['row_count'], 0)
        for label in report['labels']:
            self.assertEqual(tuple(label.keys()), effects.LABEL_KEYS)
            self.assertEqual(tuple(label['policies'].keys()), soft.ARMS)
            self.assertIsNone(label['results'])
            self.assertIsNone(label['pnl'])
            for policy in soft.ARMS:
                row = label['policies'][policy]
                self.assertEqual(tuple(row.keys()), effects.POLICY_ROW_KEYS)
                self.assertEqual(row['soft_policy'], soft.POLICIES[policy])
                self.assertIsNone(row['results'])
                self.assertIsNone(row['pnl'])
                if row['seated']:
                    self.assertEqual(row['formula_id'], soft.feebook.EXAMINER_FORMULA_ID)
        for policy, book in joined.accounts.items():
            self.assertIs(book.soft_policy, report['policy_instrument'][policy]['soft_policy'])
            self.assertEqual(book.identity(), Decimal('5000'))
            self.assertEqual(book.non_trading_residual_bucket, Decimal('9'))
