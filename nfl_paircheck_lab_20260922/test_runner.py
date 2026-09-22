"""Scaffolding tests. Fixture numbers here are not Q7 scenario results."""
import json
import unittest
from pathlib import Path
import analyze
import run_experiment
import verify_results
from paircheck_policy import implementation_pin_mismatches
from run_experiment import ROOT, missing_inputs, not_run_document, scenario_config, scenario_grid

def scenario_row(pnl, hours=1, week=1, flat=True):
    return dict(completed_strategy_pnl=pnl if flat else None, all_flat=flat,
                unhedged_contract_hours=hours, unresolved_contracts=0 if flat else 1,
                week_contributions=dict(week1=week, week2=week))

def grid(values):
    scenarios = {}
    for queue in (3300, 10000):
        for delay in (0.25, 5):
            for arm, pnl in values.items():
                scenarios[f'q{queue}_d{delay:g}_{arm}'] = scenario_row(pnl, week=pnl)
    return scenarios

class RunnerTests(unittest.TestCase):
    def test_grid_is_the_frozen_sixteen(self):
        frozen = json.loads((ROOT / 'FROZEN_EXPERIMENT.json').read_text())
        names = scenario_grid()
        self.assertEqual(len(names), 16)
        self.assertEqual(len(set(names)), 16)
        self.assertEqual(names, frozen['scenarios'])
        self.assertEqual(frozen['status'], 'IMPLEMENTED_FROZEN_NOT_RUN')
        self.assertIsNone(frozen['results'])
        self.assertIsNone(frozen['pnl'])

    def test_implementation_and_spec_pins(self):
        self.assertEqual(implementation_pin_mismatches(), [])

    def test_fixed_controls_on_every_scenario_config(self):
        cfg = scenario_config(3300, .25)
        self.assertEqual(cfg.starting_cash, 5000)
        self.assertEqual(cfg.order_size, 250)
        self.assertEqual(cfg.exposure_cap, 250)
        self.assertEqual(cfg.assumed_exit_depth, 250)
        self.assertEqual(cfg.queue_early, 3300)
        self.assertEqual(cfg.cancel_delay_seconds, .25)
        self.assertEqual(cfg.order_delay_seconds, .25)
        self.assertEqual(scenario_config(10000, 5).queue_early, 10000)
        self.assertEqual(scenario_config(10000, 5).cancel_delay_seconds, 5)
        self.assertEqual(cfg.maker_coefficient, .0175)
        self.assertEqual(cfg.queue_last12h, 1327847.005)

    def test_missing_tape_builds_not_run_without_pnl(self):
        missing = missing_inputs()
        self.assertIn('events.jsonl.gz', missing)
        self.assertNotIn('markets.json', missing)
        document = not_run_document(missing)
        self.assertEqual(document['status'], 'NOT_RUN_INPUTS_MISSING')
        self.assertEqual(document['scenarios_executed'], 0)
        self.assertIsNone(document['pnl'])
        self.assertIsNone(document['results'])
        self.assertEqual(len(document['scenario_grid']), 16)

    def test_execute_leaves_scenarios_unrun(self):
        document = run_experiment.execute()
        self.assertEqual(document['status'], 'NOT_RUN_INPUTS_MISSING')
        self.assertFalse((ROOT / 'results' / 'experiment_summary.json').exists())
        self.assertFalse(any(Path(ROOT / 'results').glob('q*_*.json')))
        stored = json.loads((ROOT / 'results' / 'NOT_RUN.json').read_text())
        self.assertIsNone(stored['pnl'])
        self.assertEqual(stored['scenarios_executed'], 0)

    def test_effects_stay_absent_until_a_real_run(self):
        state = dict(status='NOT_RUN_INPUTS_MISSING', scenarios_executed=0, pnl=None)
        document = analyze.evaluate(state)
        self.assertIsNone(document['effects'])
        self.assertIsNone(document['pnl'])
        self.assertIsNone(document['selection'])
        with self.assertRaises(SystemExit) as caught:
            analyze.main()
        self.assertEqual(caught.exception.code, 3)
        self.assertFalse((ROOT / 'results' / 'paircheck_effects.json').exists())
        status = json.loads((ROOT / 'results' / 'analysis_status.json').read_text())
        self.assertIsNone(status['pnl'])

    def test_predeclared_contrasts_and_selection_on_fixtures_only(self):
        compared = analyze.effects_for_stress(grid(dict(A=1, B=3, C=10, D=14)), 3300, .25)
        self.assertEqual(compared['status'], 'COMPARED')
        self.assertEqual(compared['original_guard'], 2)
        self.assertEqual(compared['allocator_guard'], 4)
        self.assertEqual(compared['interaction'], 2)
        unresolved = analyze.effects_for_stress(
            {'q3300_d0.25_A': scenario_row(1, flat=False),
             'q3300_d0.25_B': scenario_row(1),
             'q3300_d0.25_C': scenario_row(1),
             'q3300_d0.25_D': scenario_row(1)}, 3300, .25)
        self.assertEqual(unresolved['status'], 'UNRESOLVED_NO_EFFECT')
        self.assertNotIn('original_guard', unresolved)
        self.assertIsNone(unresolved['pnl']['A'])
        withheld = analyze.select(grid(dict(A=1, B=1, C=1, D=1)))
        self.assertEqual(withheld['status'], 'NO_NEW_SELECTION')
        self.assertIsNone(withheld['selected'])
        passing = analyze.select(grid(dict(A=1, B=10, C=8, D=10)))
        self.assertEqual(passing['selected'], 'B')
        self.assertFalse(passing['live_promotion'])

    def test_verifier_does_not_pass_a_missing_run(self):
        run_experiment.execute()
        document = verify_results.evaluate()
        self.assertIsNone(document['all_checks_passed'])
        self.assertIsNone(document['pnl'])
        self.assertEqual(document['scenarios_executed'], 0)
        with self.assertRaises(SystemExit) as caught:
            verify_results.main()
        self.assertEqual(caught.exception.code, 3)
        stored = json.loads((ROOT / 'results' / 'verification.json').read_text())
        self.assertIsNone(stored['all_checks_passed'])

if __name__ == '__main__':
    unittest.main()
