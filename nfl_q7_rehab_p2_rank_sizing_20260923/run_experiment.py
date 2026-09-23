"""Freeze entry point. The 12-scenario tape walk is refused in this PR.

No network and no live orders. execute() records a not-run document.
execute_score_run() raises. It does not invent fills, cash, or P&L.
"""
import json
from pathlib import Path

from rank_sizing_policy import InventedPnlRefused, refuse_invented_pnl
from selection import scenario_grid

ROOT = Path(__file__).resolve().parent


class ScoreRunRefused(RuntimeError):
    """The Examiner runs the twelve scenarios after this freeze."""


def scenario_config(queue, delay):
    from dataclasses import replace
    from replay_v2 import Config
    return replace(Config(), starting_cash=5000, order_size=250, exposure_cap=250,
                   assumed_exit_depth=250, queue_early=queue, quote_source='candles',
                   liquidation_lead_seconds=300, order_delay_seconds=delay,
                   cancel_delay_seconds=delay)


def not_run_document():
    return dict(status='NOT_RUN_FREEZE_SCORE_REFUSED', scenarios_executed=0,
                scenario_grid=scenario_grid(), pnl=None, results=None,
                score_run_in_this_freeze=False,
                evidence='NOT_RUN_FREEZE_BEFORE_EXAMINER',
                note='No scenario was executed. This file is not a profit result.')


def atomic_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + '.partial')
    tmp.write_text(json.dumps(value, indent=2, allow_nan=False) + '\n')
    tmp.replace(path)


def execute():
    document = not_run_document()
    refuse_invented_pnl(document)
    if document.get('scenarios_executed') != 0:
        raise InventedPnlRefused('scenarios_executed')
    atomic_json(ROOT / 'results' / 'NOT_RUN.json', document)
    return document


def execute_score_run():
    raise ScoreRunRefused(
        '12-scenario score run is not part of the freeze PR. '
        'Examiner invokes it only after this freeze is accepted.')


def main():
    document = execute()
    print(document['status'], 'scenarios_executed', document['scenarios_executed'], flush=True)
    raise SystemExit(3)


if __name__ == '__main__':
    main()
