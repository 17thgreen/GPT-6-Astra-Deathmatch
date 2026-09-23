"""Frozen B1 selection bar. Fixture arithmetic is not a rehab P&L."""
from decimal import Decimal

STRESSES = ('q3300_d0.25', 'q3300_d5', 'q10000_d0.25', 'q10000_d5')
ARMS = ('B0', 'B1', 'D')


def scenario_name(stress, arm):
    return f'{stress}_{arm}'


def scenario_grid():
    return [scenario_name(stress, arm) for stress in STRESSES for arm in ARMS]


def _money(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    return Decimal(str(value))


def _decision(status, reason):
    return dict(status=status, reason=reason, candidate_arm=None if status == 'NO_NEW_SELECTION' else 'B1',
                live_promotion=False, fallback_shadow_candidate='000', completed_profit=None,
                counted_as_experiment_pnl=False, results=None, pnl=None)


def select(scenarios):
    """Return the predeclared bar. Does not write a scorecard."""
    if not isinstance(scenarios, dict) or set(scenarios) != set(scenario_grid()):
        return _decision('NO_NEW_SELECTION', 'scenario_grid')
    for name in scenario_grid():
        row = scenarios[name]
        if not isinstance(row, dict):
            return _decision('NO_NEW_SELECTION', 'row')
        if row.get('all_flat') is not True or _money(row.get('completed_strategy_pnl')) is None:
            return _decision('NO_NEW_SELECTION', 'not_flat_or_null_pnl')
        unresolved = row.get('unresolved_contracts')
        if unresolved is None or unresolved >= .009:
            return _decision('NO_NEW_SELECTION', 'unresolved_inventory')
    for stress in STRESSES:
        b0 = _money(scenarios[scenario_name(stress, 'B0')]['completed_strategy_pnl'])
        b1 = _money(scenarios[scenario_name(stress, 'B1')]['completed_strategy_pnl'])
        dee = _money(scenarios[scenario_name(stress, 'D')]['completed_strategy_pnl'])
        if not (b1 > b0):
            return _decision('NO_NEW_SELECTION', 'b1_vs_b0:' + stress)
        if not (dee > 0):
            return _decision('NO_NEW_SELECTION', 'd_positive:' + stress)
        if b1 < Decimal('0.95') * dee:
            return _decision('NO_NEW_SELECTION', 'b1_vs_d:' + stress)
        hours_b0 = _money(scenarios[scenario_name(stress, 'B0')].get('unhedged_contract_hours'))
        hours_b1 = _money(scenarios[scenario_name(stress, 'B1')].get('unhedged_contract_hours'))
        if hours_b0 is None or hours_b1 is None or hours_b1 > Decimal('1.25') * hours_b0:
            return _decision('NO_NEW_SELECTION', 'inventory:' + stress)
    primary = 'q3300_d0.25'
    left = scenarios[scenario_name(primary, 'B0')].get('week_contributions')
    right = scenarios[scenario_name(primary, 'B1')].get('week_contributions')
    if not isinstance(left, dict) or not isinstance(right, dict):
        return _decision('NO_NEW_SELECTION', 'primary_weeks')
    for week in ('week1', 'week2'):
        base = _money(left.get(week))
        rehab = _money(right.get(week))
        if base is None or rehab is None or not (rehab > base):
            return _decision('NO_NEW_SELECTION', 'primary_weeks:' + week)
    return _decision('B1_SHADOW_CANDIDATE', 'bar_passed_on_supplied_rows')
