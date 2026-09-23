"""Budget fraction, null freeze, and closed Pass-1 cadence. No historical tape and no P&L claim."""
import hashlib
import inspect
import math
import unittest
from dataclasses import replace

from rank_sizing_policy import (ARMS, FEEBOOK_ROOT, InventedPnlRefused, Q6_000, RankSizingReplay,
                                assert_freeze_null, combined_cost_margin, entry_budget_fraction,
                                load_frozen, make_replay, parent_pin_mismatches,
                                refuse_completed_profit_without_fee_channel, refuse_invented_pnl,
                                sized_quantity)
from adaptive_policy import AdaptiveReplay, floor_qty
from factorial_policy import FactorialReplay, Factors
from feebook import CompletedProfitRefused
from paircheck_policy import AllocatorPairCheck, OriginalPairCheck, combined_cost_margin as parent_margin
from positive_controls import evaluate_positive_controls, load_source_pins, parent_ledger_status
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

def two_events(kickoff):
    book = markets(kickoff)
    book.update(C=dict(event='H', direction=1, kickoff=kickoff, verified_mecnet=True),
                D=dict(event='H', direction=-1, kickoff=kickoff, verified_mecnet=True))
    return book

def new(arm, **overrides):
    return make_replay(markets(KO), config(**overrides), arm)

def good_pair(replay, tickers=('A', 'B')):
    for ticker in tickers:
        replay.books[ticker] = dict(bid=.49, ask=.51, bid_at=AT, ask_at=AT)

def bad_pair(replay):
    for ticker in ('A', 'B'):
        replay.books[ticker] = dict(bid=.40, ask=.45, bid_at=AT, ask_at=AT)
    replay.flow.add(dict(ticker='A', at=AT - 1, yes_price=.55, size=100000, taker_side='yes'))
    replay.flow.add(dict(ticker='B', at=AT - 1, yes_price=.45, size=100000, taker_side='yes'))

def order_snapshot(replay):
    return sorted((key, order.price, order.remaining) for key, order in replay.orders.items())

def touch(replay, now, tickers=None):
    names = tickers or list(replay.books)
    for ticker in names:
        replay.books[ticker]['bid_at'] = now
        replay.books[ticker]['ask_at'] = now

def chosen_total(replay, event, now):
    candidates = replay.route_candidates(event, now)
    chosen = replay.choose(candidates)
    selected = [c for c in candidates if c['key'] in chosen]
    total = sum(c['wanted'] * (c['cost'] + .0001) + float(replay.cfg.balance_precision) for c in selected)
    return selected, total

def flat_row(pnl, hours, week):
    return dict(completed_strategy_pnl=pnl, all_flat=True, unresolved_contracts=0,
                unhedged_contract_hours=hours,
                week_contributions=dict(week1=week, week2=week))

def passing_grid():
    scenarios = {}
    for stress in ('q3300_d0.25', 'q3300_d5', 'q10000_d0.25', 'q10000_d5'):
        scenarios[f'{stress}_B0'] = flat_row(10, 4, 1)
        scenarios[f'{stress}_B2'] = flat_row(20, 4, 2)
        scenarios[f'{stress}_D'] = flat_row(20, 4, 2)
    return scenarios

class RankSizingTests(unittest.TestCase):
    def test_budget_fraction_scales_wanted(self):
        self.assertEqual(entry_budget_fraction(0, 0), 0)
        self.assertEqual(entry_budget_fraction(0, 10), 0)
        self.assertEqual(entry_budget_fraction(4, 8), .5)
        self.assertEqual(entry_budget_fraction(8, 8), 1)
        self.assertEqual(entry_budget_fraction(12, 8), 1)
        self.assertEqual(sized_quantity(250, 0, 10), 0)
        self.assertEqual(sized_quantity(100, 5, 10), floor_qty(50))
        rehab = make_replay(two_events(KO), config(), 'B2')
        control = make_replay(two_events(KO), config(), 'B0')
        for replay in (rehab, control):
            good_pair(replay, ('A', 'B', 'C', 'D'))
        selected, total = chosen_total(rehab, 'H', AT)
        rank_g = rehab.portfolio_rank(rehab.event_candidates('G', AT), AT)
        self.assertEqual(rank_g['adjusted'], 1)
        self.assertFalse(rank_g['has_observed_flow'])
        rehab.cash = rank_g['capital'] + .5 * total
        control.cash = rehab.cash
        rehab.refresh('H', AT)
        control.refresh('H', AT)
        self.assertAlmostEqual(rehab.allocations['H'] / total, .5)
        self.assertGreater(rehab.allocations['G'], rehab.allocations['H'])
        self.assertEqual(rehab.decisions[-1]['protected'], 0)
        self.assertTrue(math.isinf(rehab.next_allocation) and rehab.next_allocation < 0)
        self.assertEqual(rehab.experiment, 'baseline')
        for row in selected:
            expected = sized_quantity(row['wanted'], rehab.allocations['H'], total)
            self.assertLess(expected, row['wanted'])
            self.assertEqual(rehab.orders[row['key']].remaining, expected)
            self.assertGreater(control.orders[row['key']].remaining, rehab.orders[row['key']].remaining)
        self.assertEqual(rehab.metrics['portfolio_rebalances'], 1)
        self.assertEqual(control.metrics['portfolio_rebalances'], 0)

    def test_full_budget_matches_baseline_wanted(self):
        rehab = new('B2')
        control = new('B0')
        good_pair(rehab)
        good_pair(control)
        rehab.refresh('G', AT)
        control.refresh('G', AT)
        self.assertEqual(order_snapshot(rehab), order_snapshot(control))
        self.assertEqual(len(rehab.orders), 2)
        self.assertEqual(rehab.portfolio_rank_sizing, True)
        self.assertEqual(control.portfolio_rank_sizing, False)
        self.assertGreaterEqual(rehab.allocations['G'], 0)
        fraction = entry_budget_fraction(rehab.allocations['G'], chosen_total(rehab, 'G', AT)[1])
        self.assertEqual(fraction, 1)

    def test_offset_survives_a_zero_entry_budget(self):
        rehab = new('B2')
        bad_pair(rehab)
        position(rehab, 25)
        cash = rehab.cash
        rehab.refresh('G', AT)
        self.assertEqual(rehab.cash, cash)
        self.assertTrue(rehab.pair_rejections)
        self.assertLessEqual(rehab.pair_rejections[0]['margin'], 0)
        self.assertFalse(rehab.pair_rejections[0]['counted_as_pnl'])
        self.assertTrue(rehab.orders)
        self.assertTrue(all(order.direction * rehab.holdings['G'] < 0 for order in rehab.orders.values()))
        self.assertLessEqual(sum(order.remaining for order in rehab.orders.values()), 25)

    def test_budget_clock_does_not_block_admission(self):
        rehab = new('B2')
        good_pair(rehab)
        rehab.next_allocation = AT + 10_000
        rehab.refresh('G', AT)
        self.assertEqual(len(rehab.orders), 2)
        self.assertEqual(rehab.metrics['portfolio_rebalances'], 1)
        self.assertTrue(math.isinf(rehab.next_allocation) and rehab.next_allocation < 0)
        rehab.orders.clear()
        touch(rehab, AT + 1)
        rehab.next_allocation = AT + 600
        rehab.refresh('G', AT + 1)
        self.assertEqual(len(rehab.orders), 2)
        self.assertEqual(rehab.metrics['portfolio_rebalances'], 2)
        self.assertIsNone(rehab.admission_cadence_seconds)
        self.assertFalse(rehab.pass1_admission_gate)
        self.assertFalse(hasattr(rehab, 'cadence_blocks'))
        source = inspect.getsource(RankSizingReplay)
        self.assertNotIn('RehabCadenceReplay', source)
        self.assertNotIn('ADMISSION_CADENCE_SECONDS', source)
        self.assertIn('FactorialReplay.portfolio_rank', source)
        self.assertIn('FactorialReplay.rebalance', source)
        self.assertNotIn('cadence_policy', inspect.getsource(inspect.getmodule(RankSizingReplay)))

    def test_one_knob_does_not_change_route_or_reopen_cadence(self):
        rehab = new('B2')
        control = new('B0')
        sized = make_replay(markets(KO), scenario_config(3300, .25), 'B2')
        sized_control = make_replay(markets(KO), scenario_config(3300, .25), 'B0')
        self.assertIs(RankSizingReplay.choose, QueueReplay.choose)
        self.assertIs(combined_cost_margin, parent_margin)
        self.assertNotIn(FactorialReplay, RankSizingReplay.mro())
        self.assertIn(OriginalPairCheck, RankSizingReplay.mro())
        self.assertIn(AdaptiveReplay, RankSizingReplay.mro())
        for replay in (rehab, control):
            good_pair(replay)
        self.assertEqual(rehab.choose(rehab.route_candidates('G', AT)),
                         control.choose(control.route_candidates('G', AT)))
        reference = FactorialReplay(markets(KO), config(), Factors(False, False, False))
        good_pair(reference)
        left = rehab.event_candidates('G', AT)
        right = reference.event_candidates('G', AT)
        self.assertEqual(rehab.portfolio_rank(left, AT)['adjusted'], 1)
        self.assertEqual(rehab.portfolio_rank(left, AT), reference.portfolio_rank(right, AT))
        self.assertEqual(rehab.factors, Q6_000)
        self.assertEqual(sized.cfg.order_size, 250)
        self.assertEqual(sized.cfg.exposure_cap, sized_control.cfg.exposure_cap)
        self.assertEqual(sized.cfg.maker_coefficient, sized_control.cfg.maker_coefficient)
        self.assertEqual(rehab.experiment, 'baseline')
        self.assertEqual(combined_cost_margin([.4, .4], 250, '.0001'),
                         1 - .8 - .0002 - 2 * .0001 / 250)
        with self.assertRaises(ValueError):
            new('B1')

    def test_b0_and_d_are_parent_imports(self):
        control = new('B0')
        retention = new('D')
        self.assertIs(type(control), OriginalPairCheck)
        self.assertIs(type(retention), AllocatorPairCheck)
        self.assertNotIn(RankSizingReplay, type(control).mro())
        self.assertNotIn(RankSizingReplay, type(retention).mro())
        self.assertTrue(control.pair_check and retention.pair_check)
        self.assertEqual(retention.factors.label, '000')
        self.assertFalse(retention.factors.flow or retention.factors.protection or retention.factors.ranking)
        self.assertEqual(retention.positive_control, 'Q7_ARM_D')
        self.assertEqual(control.positive_control, 'Q7_ARM_B')
        self.assertIsNone(control.admission_cadence_seconds)
        self.assertEqual(parent_pin_mismatches(), [])

    def test_freeze_results_and_pnl_stay_null(self):
        frozen = load_frozen()
        assert_freeze_null(frozen)
        self.assertIsNone(frozen['results'])
        self.assertIsNone(frozen['pnl'])
        self.assertEqual(frozen['status'], 'IMPLEMENTED_FROZEN_NOT_RUN')
        self.assertEqual(frozen['scenario_count'], 12)
        self.assertEqual(frozen['scenarios'], scenario_grid())
        self.assertEqual(frozen['one_knob'], 'portfolio_rank_sizing')
        self.assertIsNone(frozen['arms']['B0']['admission_cadence_seconds'])
        self.assertIsNone(frozen['arms']['B2']['admission_cadence_seconds'])
        self.assertNotIn('B1', frozen['arms'])
        self.assertTrue(frozen['arms']['B2']['portfolio_rank_sizing'])
        self.assertFalse(frozen['arms']['B2']['pass1_admission_gate'])
        self.assertEqual(frozen['arms']['B2']['q6_factor_label'], '000')
        self.assertFalse(frozen['selection_rule']['live_promotion'])
        self.assertEqual(frozen['selection_rule']['otherwise'], 'NO_NEW_SELECTION')
        self.assertEqual(frozen['selection_rule']['fallback_shadow_candidate'], '000')
        self.assertFalse(frozen['selection_rule']['soften_after_peek'])
        self.assertFalse(frozen['positive_controls']['parent_ledgers_in_checkout'])
        with self.assertRaises(InventedPnlRefused):
            assert_freeze_null(dict(results={'pnl': 1}, pnl=1, score_run_in_this_freeze=False,
                                     status='IMPLEMENTED_FROZEN_NOT_RUN', one_knob='portfolio_rank_sizing',
                                     selection_rule=dict(live_promotion=False,
                                                         require_B2_beats_B0_all_stresses=True,
                                                         require_D_positive_and_B2_at_least_95pct_of_D=True)))
        self.assertEqual(ARMS, ('B0', 'B2', 'D'))

    def test_score_run_and_invented_pnl_are_refused(self):
        with self.assertRaises(ScoreRunRefused):
            execute_score_run()
        with self.assertRaises(InventedPnlRefused):
            refuse_invented_pnl(dict(pnl=1, results=None))
        with self.assertRaises(InventedPnlRefused):
            refuse_invented_pnl(dict(pnl=None, results={'q3300_d0.25_B2': 1}))
        with self.assertRaises(InventedPnlRefused):
            refuse_invented_pnl(dict(pnl=None, results=None, completed_strategy_pnl=12.5))
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
        self.assertIn('q3300_d0.25_B2', document['scenario_grid'])
        self.assertNotIn('q3300_d0.25_B1', document['scenario_grid'])
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
        frozen = load_frozen()
        controls = frozen['positive_controls']
        self.assertFalse(controls['waive_parent_ledger_hash_check'])
        self.assertFalse(controls['parent_ledgers_in_checkout'])
        self.assertFalse(controls['ledger_blobs_committed'])
        self.assertTrue(controls['B0']['absence_is_not_a_pass'])
        self.assertTrue(controls['D']['absence_is_not_a_pass'])
        self.assertEqual(controls['source_pins'],
                         'packets/refiner/PARENT_Q7_BD_LEDGER_SOURCE_PINS_2026-09-23.json')
        pins = load_source_pins()
        self.assertTrue(pins['present'])
        self.assertFalse(pins['waive'])
        self.assertFalse(pins['invented_hashes'])
        self.assertEqual(len(pins['artifacts']), 32)
        match = controls['desk_verified_match']
        self.assertEqual(match['q3300_d0.25_B.json'],
                         '370ccbcf342db59aa1697d448d3274791cf17c015d8e9eead17d788fbe79ffb5')
        self.assertEqual(match['q3300_d0.25_D.json'],
                         'fc38cfbc134ca313a6cd2b8763ef49c3a56f6b5cc763c50f82e2b4545cda898f')
        self.assertEqual(match['paircheck_effects.json'],
                         '5d87ea610f22482c980868d8a31a228ca1931368d9eeab73add4256d2e117fdf')
        self.assertEqual(pins['artifacts']['q3300_d0.25_B.json']['sha256'], match['q3300_d0.25_B.json'])
        self.assertEqual(pins['artifacts']['q3300_d0.25_D.json']['sha256'], match['q3300_d0.25_D.json'])
        self.assertEqual(pins['paircheck_effects']['sha256'], match['paircheck_effects.json'])
        parent_results = ROOT.parent / controls['repo_results_path']
        for name in list(pins['artifacts']) + ['paircheck_effects.json']:
            self.assertFalse((parent_results / name).exists(), name)
        absent = frozen['absent_cites']
        self.assertFalse(absent['present_in_checkout'])
        self.assertFalse(absent['bytes_invented'])
        for key in ('examiner_p1_kill', 'conductor_pass2_kick', 'rehab_policy'):
            self.assertFalse((ROOT.parent / absent[key]).exists(), key)

    def test_selection_bar_does_not_soften_and_does_not_write_pnl(self):
        frozen_before = (ROOT / 'FROZEN_EXPERIMENT.json').read_text()
        passed = select(passing_grid())
        self.assertEqual(passed['status'], 'B2_SHADOW_CANDIDATE')
        self.assertFalse(passed['live_promotion'])
        self.assertIsNone(passed['completed_profit'])
        self.assertIsNone(passed['pnl'])
        self.assertIsNone(passed['results'])
        self.assertFalse(passed['counted_as_experiment_pnl'])
        self.assertEqual(passed['fallback_shadow_candidate'], '000')
        short = passing_grid()
        short['q10000_d5_B2'] = flat_row(10, 4, 2)
        self.assertEqual(select(short)['reason'], 'b2_vs_b0:q10000_d5')
        thin = passing_grid()
        thin['q3300_d5_D'] = flat_row(0, 4, 2)
        self.assertEqual(select(thin)['reason'], 'd_positive:q3300_d5')
        short_d = passing_grid()
        short_d['q10000_d0.25_B2'] = flat_row(18, 4, 2)
        short_d['q10000_d0.25_D'] = flat_row(20, 4, 2)
        self.assertEqual(select(short_d)['reason'], 'b2_vs_d:q10000_d0.25')
        tied = passing_grid()
        tied['q3300_d5_B2'] = flat_row(10, 4, 2)
        self.assertEqual(select(tied)['status'], 'NO_NEW_SELECTION')
        inventory = passing_grid()
        inventory['q10000_d0.25_B2'] = flat_row(20, 6, 2)
        self.assertEqual(select(inventory)['reason'], 'inventory:q10000_d0.25')
        weeks = passing_grid()
        weeks['q3300_d0.25_B2']['week_contributions'] = dict(week1=2, week2=1)
        self.assertEqual(select(weeks)['status'], 'NO_NEW_SELECTION')
        nulls = passing_grid()
        nulls['q3300_d0.25_B2'] = dict(completed_strategy_pnl=None, all_flat=False, unresolved_contracts=1,
                                       unhedged_contract_hours=4, week_contributions=dict(week1=2, week2=2))
        self.assertEqual(select(nulls)['reason'], 'not_flat_or_null_pnl')
        self.assertEqual((ROOT / 'FROZEN_EXPERIMENT.json').read_text(), frozen_before)
        self.assertIsNone(load_frozen()['pnl'])
        self.assertIsNone(load_frozen()['results'])
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
        self.assertNotIn('q3300_d0.25_B1', names)
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
