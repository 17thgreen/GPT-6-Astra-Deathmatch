"""Predeclared Q7 contrasts. Does not invent P&L when the replay was not run."""
import json
from pathlib import Path
from run_experiment import DELAYS, QUEUES, ROOT, scenario_name

ARMS = ('A', 'B', 'C', 'D')


def _row(scenarios, queue, delay, arm):
    return scenarios[scenario_name(queue, delay, arm)]


def _completed_pnl(row):
    if not row or not row.get('all_flat'):
        return None
    value = row.get('completed_strategy_pnl')
    if value is None:
        return None
    return value


def effects_for_stress(scenarios, queue, delay):
    values = {arm: _completed_pnl(_row(scenarios, queue, delay, arm)) for arm in ARMS}
    if any(value is None for value in values.values()):
        return dict(status='UNRESOLVED_NO_EFFECT', pnl=values)
    original = values['B'] - values['A']
    allocator = values['D'] - values['C']
    return dict(status='COMPARED', pnl=values,
                original_guard=original, allocator_guard=allocator,
                interaction=allocator - original,
                architecture_check_off=values['C'] - values['A'],
                architecture_check_on=values['D'] - values['B'])


def select(scenarios):
    """Arm B only, under the rule frozen in EXPERIMENT_SPEC.md."""
    stresses = [(queue, delay) for queue in QUEUES for delay in DELAYS]
    complete = True
    for queue, delay in stresses:
        for arm in ARMS:
            if _completed_pnl(_row(scenarios, queue, delay, arm)) is None:
                complete = False
    if not complete:
        return dict(selected=None, status='NO_NEW_SELECTION',
                    reason='unresolved_or_incomplete_inventory')
    def pnl(arm, queue, delay):
        return _completed_pnl(_row(scenarios, queue, delay, arm))
    beats = all(pnl('B', queue, delay) > pnl('A', queue, delay) for queue, delay in stresses)
    retains = all(pnl('D', queue, delay) > 0 and pnl('B', queue, delay) >= .95 * pnl('D', queue, delay)
                  for queue, delay in stresses)
    primary_b = _row(scenarios, 3300, .25, 'B')['week_contributions']
    primary_a = _row(scenarios, 3300, .25, 'A')['week_contributions']
    weeks = all(primary_b[week] > primary_a[week] for week in ('week1', 'week2'))
    hours = all(_row(scenarios, queue, delay, 'B')['unhedged_contract_hours']
                <= 1.25 * _row(scenarios, queue, delay, 'A')['unhedged_contract_hours']
                for queue, delay in stresses)
    passed = beats and retains and weeks and hours
    return dict(selected='B' if passed else None,
                status='SHADOW_RESEARCH_CANDIDATE_ONLY' if passed else 'NO_NEW_SELECTION',
                conditions=dict(beats_original_all=beats, retains_95pct_of_D=retains,
                                improves_both_primary_weeks=weeks, inventory_within_limit=hours),
                live_promotion=False, fallback_shadow_candidate='000')


def load_state(root=ROOT):
    summary_path = root / 'results' / 'experiment_summary.json'
    if summary_path.exists():
        return json.loads(summary_path.read_text())
    not_run_path = root / 'results' / 'NOT_RUN.json'
    if not_run_path.exists():
        return json.loads(not_run_path.read_text())
    return dict(status='NOT_RUN_NO_OUTPUT', scenarios_executed=0, pnl=None, results=None)


def evaluate(state):
    if state.get('status') != 'COMPLETE' or not state.get('scenarios'):
        return dict(status=state.get('status', 'NOT_RUN_NO_OUTPUT'), scenarios_executed=0,
                    pnl=None, effects=None, selection=None,
                    note='No Q7 contrasts. Missing output is not a zero effect.')
    scenarios = state['scenarios']
    effects = {f'q{queue}_d{delay:g}': effects_for_stress(scenarios, queue, delay)
               for queue in QUEUES for delay in DELAYS}
    return dict(status='COMPLETE', scenarios_executed=len(scenarios), effects=effects,
                selection=select(scenarios), pnl=None,
                note='pnl on this document is not a headline result; read effects.pnl per arm.')


def main():
    state = load_state()
    document = evaluate(state)
    path = ROOT / 'results' / ('paircheck_effects.json' if document['status'] == 'COMPLETE'
                               else 'analysis_status.json')
    if document['status'] != 'COMPLETE':
        effects = ROOT / 'results' / 'paircheck_effects.json'
        if effects.exists():
            raise RuntimeError('Refusing to leave an effects file beside a not-run analysis')
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(document, indent=2, allow_nan=False))
    print(document['status'], flush=True)
    if document['status'] != 'COMPLETE':
        raise SystemExit(3)
if __name__ == '__main__':
    main()
