"""Cadence gate, null freeze, and one-knob checks. No historical tape and no P&L claim."""
import inspect
import math
import unittest
from dataclasses import replace

from cadence_policy import (ADMISSION_CADENCE_SECONDS, ARMS, FEEBOOK_ROOT, InventedPnlRefused,
                            RehabCadenceReplay, assert_freeze_null, combined_cost_margin,
                            load_frozen, make_replay, parent_pin_mismatches,
                            refuse_completed_profit_without_fee_channel)
from adaptive_policy import AdaptiveReplay
from factorial_policy import FactorialReplay, Factors
from feebook import CompletedProfitRefused
from paircheck_policy import AllocatorPairCheck, OriginalPairCheck, combined_cost_margin as parent_margin
from positive_controls import evaluate_positive_controls, parent_ledger_status
from queue_policies import QueueReplay
from replay_v2 import Config
from run_experiment import ROOT, ScoreRunRefused, execute, execute_score_run, scenario_config
from selection import scenario_grid, select
from test_adaptive import AT, KO, position
from test_replay_v2 import markets

def config(**overrides):
    values = dict(quote_source='candles', queue_early=100, queue_last12h=100,
                  liquidation_lead_seconds=300, cancel_delay_seconds=.25, order_delay_seconds=.25)
    values.update(overrides)
    return replace(Config(), **values)

def new(arm, **overrides):
    return make_replay(markets(KO), config(**overrides), arm)

def good_pair(replay):
    for ticker in ('A', 'B'):
        replay.books[ticker] = dict(bid=.49, ask=.51, bid_at=AT, ask_at=AT)

def bad_pair(replay):
    for ticker in ('A', 'B'):
        replay.books[ticker] = dict(bid=.40, ask=.45, bid_at=AT, ask_at=AT)
    replay.flow.add(dict(ticker='A', at=AT - 1, yes_price=.55, size=100000, taker_side='yes'))
    replay.flow.add(dict(ticker='B', at=AT - 1, yes_price=.45, size=100000, taker_side='yes'))

def order_snapshot(replay):
    return sorted((key, order.price, order.remaining) for key, order in replay.orders.items())

def touch(replay, now):
    for ticker in ('A', 'B'):
        replay.books[ticker]['bid_at'] = now
        replay.books[ticker]['ask_at'] = now

def flat_row(pnl, hours, week):
    return dict(completed_strategy_pnl=pnl, all_flat=True, unresolved_contracts=0,
                unhedged_contract_hours=hours,
                week_contributions=dict(week1=week, week2=week))

def passing_grid():
    scenarios = {}
    for stress in ('q3300_d0.25', 'q3300_d5', 'q10000_d0.25', 'q10000_d5'):
        scenarios[f'{stress}_B0'] = flat_row(10, 4, 1)
        scenarios[f'{stress}_B1'] = flat_row(20, 4, 2)
        scenarios[f'{stress}_D'] = flat_row(20, 4, 2)
    return scenarios

class CadenceTests(unittest.TestCase):
    def test_open_window_admits_then_closed_window_blocks_then_next_window_admits(self):
        rehab = new('B1')
        control = new('B0')
        good_pair(rehab)
        good_pair(control)
        rehab.refresh('G', AT)
        control.refresh('G', AT)
        self.assertEqual(order_snapshot(rehab), order_snapshot(control))
        self.assertEqual(len(rehab.orders), 2)
        self.assertEqual(rehab.next_allocation, AT + 600)
        self.assertEqual(rehab.admit_attempts[0]['counted_as_pnl'], False)
        self.assertTrue(math.isinf(control.next_allocation) and control.next_allocation < 0)
        rehab.orders.clear()
        control.orders.clear()
        touch(rehab, AT + 599)
        touch(control, AT + 599)
        rehab.refresh('G', AT + 599)
        control.refresh('G', AT + 599)
        self.assertEqual(rehab.orders, {})
        self.assertEqual(len(control.orders), 2)
        self.assertEqual(rehab.next_allocation, AT + 600)
        self.assertTrue(rehab.cadence_blocks)
        self.assertTrue(all(row['counted_as_pnl'] is False for row in rehab.cadence_blocks))
        self.assertEqual(rehab.cadence_blocks[-1]['reason'], 'admission_cadence')
        self.assertNotIn('cadence_block', {row['kind'] for row in rehab.decisions})
        self.assertEqual(rehab.cash, rehab.cfg.starting_cash)
        touch(rehab, AT + 600)
        rehab.refresh('G', AT + 600)
        self.assertEqual(len(rehab.orders), 2)
        self.assertEqual(rehab.next_allocation, AT + 1200)
        self.assertEqual(rehab.admission_cadence_seconds, 600)
        self.assertEqual(ADMISSION_CADENCE_SECONDS, 600)

    def test_rejected_pair_still_consumes_the_admit_slot(self):
        rehab = new('B1')
        bad_pair(rehab)
        cash = rehab.cash
        rehab.refresh('G', AT)
        self.assertEqual(rehab.orders, {})
        self.assertEqual(rehab.cash, cash)
        self.assertEqual(rehab.next_allocation, AT + 600)
        self.assertEqual(rehab.pair_rejections[0]['counted_as_pnl'], False)
        self.assertLessEqual(rehab.pair_rejections[0]['margin'], 0)
        good_pair(rehab)
        touch(rehab, AT + 1)
        rehab.refresh('G', AT + 1)
        self.assertEqual(rehab.orders, {})
        touch(rehab, AT + 600)
        rehab.refresh('G', AT + 600)
        self.assertEqual(len(rehab.orders), 2)
        self.assertEqual(rehab.next_allocation, AT + 1200)

    def test_closed_cadence_keeps_a_working_order_and_still_quotes_an_offset(self):
        rehab = new('B1')
        control = new('B0')
        good_pair(rehab)
        rehab.refresh('G', AT)
        identities = {key: order.identity for key, order in rehab.orders.items()}
        rehab.refresh('G', AT + 60)
        self.assertEqual({key: order.identity for key, order in rehab.orders.items()}, identities)
        self.assertEqual(rehab.next_allocation, AT + 600)
        for replay in (rehab, control):
            if replay is control:
                good_pair(replay)
                position(replay, 25)
                replay.refresh('G', AT)
        rehab.orders.clear()
        position(rehab, 25)
        rehab.refresh('G', AT + 60)
        self.assertTrue(rehab.orders)
        self.assertTrue(all(order.direction * rehab.holdings['G'] < 0 for order in rehab.orders.values()))
        self.assertLess(len(rehab.orders), len(control.orders))
        self.assertEqual(rehab.next_allocation, AT + 600)

    def test_one_knob_does_not_change_route_rank_or_size(self):
        rehab = new('B1')
        control = new('B0')
        sized = make_replay(markets(KO), scenario_config(3300, .25), 'B1')
        sized_control = make_replay(markets(KO), scenario_config(3300, .25), 'B0')
        self.assertIs(RehabCadenceReplay.choose, QueueReplay.choose)
        self.assertIs(combined_cost_margin, parent_margin)
        self.assertIs(RehabCadenceReplay.portfolio_rank, AdaptiveReplay.portfolio_rank)
        source = inspect.getsource(RehabCadenceReplay)
        self.assertNotIn('order_size', source)
        self.assertNotIn('maker_coefficient', source)
        self.assertNotIn('Factors', source)
        for replay in (rehab, control):
            good_pair(replay)
        self.assertEqual(rehab.choose(rehab.route_candidates('G', AT)),
                         control.choose(control.route_candidates('G', AT)))
        rehab.refresh('G', AT)
        control.refresh('G', AT)
        self.assertEqual(order_snapshot(rehab), order_snapshot(control))
        self.assertEqual(rehab.cfg.order_size, control.cfg.order_size)
        self.assertEqual(sized.cfg.order_size, 250)
        self.assertEqual(sized.cfg.exposure_cap, sized_control.cfg.exposure_cap)
        self.assertEqual(sized.cfg.maker_coefficient, sized_control.cfg.maker_coefficient)
        self.assertEqual(rehab.experiment, 'baseline')
        self.assertEqual(rehab.metrics['portfolio_rebalances'], 0)
        self.assertEqual(combined_cost_margin([.4, .4], 250, '.0001'),
                         1 - .8 - .0002 - 2 * .0001 / 250)
        margin = combined_cost_margin([.55, .55], 250, '.0001')
        self.assertLess(margin, 0)
        self.assertNotEqual(margin, combined_cost_margin([.55, .55], 1, '.0001'))

    def test_b0_and_d_are_parent_imports(self):
        control = new('B0')
        retention = new('D')
        self.assertIs(type(control), OriginalPairCheck)
        self.assertIs(type(retention), AllocatorPairCheck)
        self.assertNotIn(RehabCadenceReplay, type(control).mro())
        self.assertNotIn(RehabCadenceReplay, type(retention).mro())
        self.assertTrue(control.pair_check and retention.pair_check)
        self.assertEqual(retention.factors.label, '000')
        self.assertFalse(retention.factors.flow or retention.factors.protection or retention.factors.ranking)
        self.assertEqual(retention.positive_control, 'Q7_ARM_D')
        self.assertEqual(control.positive_control, 'Q7_ARM_B')
        reference = FactorialReplay(markets(KO), config(), Factors(False, False, False))
        good_pair(retention)
        good_pair(reference)
        left = retention.event_candidates('G', AT)
        right = reference.event_candidates('G', AT)
        for row in left + right:
            row['rate'] = 1
        self.assertEqual(retention.portfolio_rank(left, AT), reference.portfolio_rank(right, AT))
        self.assertEqual(parent_pin_mismatches(), [])

    def test_freeze_results_and_pnl_stay_null(self):
        frozen = load_frozen()
        assert_freeze_null(frozen)
        self.assertIsNone(frozen['results'])
        self.assertIsNone(frozen['pnl'])
        self.assertEqual(frozen['status'], 'IMPLEMENTED_FROZEN_NOT_RUN')
        self.assertEqual(frozen['scenario_count'], 12)
        self.assertEqual(frozen['scenarios'], scenario_grid())
        self.assertEqual(frozen['admission_cadence_seconds'], 600)
        self.assertIsNone(frozen['arms']['B0']['admission_cadence_seconds'])
        self.assertFalse(frozen['selection_rule']['live_promotion'])
        self.assertEqual(frozen['selection_rule']['otherwise'], 'NO_NEW_SELECTION')
        self.assertFalse(frozen['positive_controls']['parent_ledgers_in_checkout'])
        with self.assertRaises(InventedPnlRefused):
            assert_freeze_null(dict(results={'pnl': 1}, pnl=1, score_run_in_this_freeze=False,
                                     status='IMPLEMENTED_FROZEN_NOT_RUN',
                                     selection_rule=dict(live_promotion=False)))
        self.assertEqual(ARMS, ('B0', 'B1', 'D'))

    def test_score_run_and_missing_fee_channel_are_refused(self):
        with self.assertRaises(ScoreRunRefused):
            execute_score_run()
        with self.assertRaises(CompletedProfitRefused):
            refuse_completed_profit_without_fee_channel({'inventory_flat': True, 'completed_strategy_pnl': 1})
        with self.assertRaises(CompletedProfitRefused):
            refuse_completed_profit_without_fee_channel({'inventory_flat': True, 'fee_channel': {}})
        document = execute()
        self.assertEqual(document['status'], 'NOT_RUN_FREEZE_SCORE_REFUSED')
        self.assertEqual(document['scenarios_executed'], 0)
        self.assertIsNone(document['pnl'])
        self.assertIsNone(document['results'])
        self.assertEqual(len(document['scenario_grid']), 12)
        self.assertFalse(any((ROOT / 'results').glob('q*_*.json')))
        self.assertFalse((ROOT / 'results' / 'experiment_summary.json').exists())
        stored = load_json(ROOT / 'results' / 'NOT_RUN.json')
        self.assertIsNone(stored['pnl'])
        self.assertIsNone(stored['results'])

    def test_parent_ledgers_absent_is_not_a_pass(self):
        status = parent_ledger_status()
        self.assertTrue(status['missing'])
        self.assertEqual(status['present'], [])
        self.assertFalse(status['invented_hashes'])
        report = evaluate_positive_controls()
        self.assertEqual(report['status'], 'PARENT_LEDGERS_ABSENT')
        self.assertIsNone(report['all_checks_passed'])
        self.assertIsNone(report['pnl'])
        self.assertIsNone(report['results'])
        self.assertFalse(report['invented_hashes'])
        self.assertIn('q3300_d0.25_B', ' '.join(report['missing']))
        self.assertIn('q10000_d5_D', ' '.join(report['missing']))

    def test_selection_bar_does_not_soften_and_does_not_write_pnl(self):
        frozen_before = (ROOT / 'FROZEN_EXPERIMENT.json').read_text()
        passed = select(passing_grid())
        self.assertEqual(passed['status'], 'B1_SHADOW_CANDIDATE')
        self.assertFalse(passed['live_promotion'])
        self.assertIsNone(passed['completed_profit'])
        self.assertIsNone(passed['pnl'])
        self.assertFalse(passed['counted_as_experiment_pnl'])
        self.assertEqual(passed['fallback_shadow_candidate'], '000')
        short = passing_grid()
        short['q10000_d5_B1'] = flat_row(10, 4, 2)
        self.assertEqual(select(short)['status'], 'NO_NEW_SELECTION')
        thin = passing_grid()
        thin['q3300_d5_D'] = flat_row(0, 4, 2)
        self.assertEqual(select(thin)['reason'], 'd_positive:q3300_d5')
        inventory = passing_grid()
        inventory['q10000_d0.25_B1'] = flat_row(20, 6, 2)
        self.assertEqual(select(inventory)['reason'], 'inventory:q10000_d0.25')
        weeks = passing_grid()
        weeks['q3300_d0.25_B1']['week_contributions'] = dict(week1=2, week2=1)
        self.assertEqual(select(weeks)['status'], 'NO_NEW_SELECTION')
        nulls = passing_grid()
        nulls['q3300_d0.25_B1'] = dict(completed_strategy_pnl=None, all_flat=False, unresolved_contracts=1,
                                       unhedged_contract_hours=4, week_contributions=dict(week1=2, week2=2))
        self.assertEqual(select(nulls)['reason'], 'not_flat_or_null_pnl')
        self.assertEqual((ROOT / 'FROZEN_EXPERIMENT.json').read_text(), frozen_before)
        self.assertIsNone(load_frozen()['pnl'])
        self.assertTrue((FEEBOOK_ROOT / 'feebook.py').exists())

    def test_fixed_scenario_config_and_grid(self):
        cfg = scenario_config(3300, .25)
        self.assertEqual(cfg.starting_cash, 5000)
        self.assertEqual(cfg.order_size, 250)
        self.assertEqual(cfg.exposure_cap, 250)
        self.assertEqual(cfg.assumed_exit_depth, 250)
        self.assertEqual(cfg.queue_early, 3300)
        self.assertEqual(cfg.cancel_delay_seconds, .25)
        self.assertEqual(scenario_config(10000, 5).queue_early, 10000)
        self.assertEqual(scenario_config(10000, 5).cancel_delay_seconds, 5)
        names = scenario_grid()
        self.assertEqual(len(names), 12)
        self.assertEqual(len(set(names)), 12)
        self.assertNotIn('q3300_d0.25_A', names)
        self.assertNotIn('q3300_d0.25_C', names)
        with self.assertRaises(ValueError):
            new('A')
        with self.assertRaises(ValueError):
            new('C')

def load_json(path):
    import json
    return json.loads(path.read_text())

if __name__ == '__main__':
    unittest.main()
