"""Run the 16 Q7 scenarios, or record that the historical tape is absent.

No network and no live orders. Missing inputs produce a not-run status with
no scenario P&L.
"""
import gzip, hashlib, json, multiprocessing, time, traceback
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import replace
from pathlib import Path
from paircheck_policy import Q6_ROOT, ARMS, make_replay, q6_pin_mismatches
from replay_v2 import Config

ROOT = Path(__file__).resolve().parent
INPUTS = Q6_ROOT / 'inputs'
QUEUES = (3300, 10000)
DELAYS = (0.25, 5)
EVENTS = MARKETS = WEEKS = None


def scenario_name(queue, delay, arm):
    return f'q{queue}_d{delay:g}_{arm}'


def scenario_grid():
    return [scenario_name(queue, delay, arm) for queue in QUEUES for delay in DELAYS for arm in ARMS]


def scenario_config(queue, delay):
    return replace(Config(), starting_cash=5000, order_size=250, exposure_cap=250,
                   assumed_exit_depth=250, queue_early=queue, quote_source='candles',
                   liquidation_lead_seconds=300, order_delay_seconds=delay,
                   cancel_delay_seconds=delay)


def missing_inputs():
    manifest = json.loads((INPUTS / 'manifest.json').read_text())
    missing = []
    for name, digest in manifest['sha256'].items():
        path = INPUTS / name
        if not path.exists():
            missing.append(name)
            continue
        if hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            missing.append(name + ':HASH_MISMATCH')
    return missing


def not_run_document(missing):
    return dict(status='NOT_RUN_INPUTS_MISSING', scenarios_executed=0, scenario_grid=scenario_grid(),
                pnl=None, results=None, missing_inputs=missing,
                inputs_path='nfl_factorial_lab_20260921/inputs',
                evidence='NOT_RUN_HISTORICAL_INPUTS_MISSING',
                how_to_run=[
                    'Obtain NFL_Allocation_Factorial_Kit.zip from the project owner.',
                    'From the repository root: python3 scripts/restore_kit.py /path/to/NFL_Allocation_Factorial_Kit.zip',
                    'Confirm nfl_factorial_lab_20260921/inputs/events.jsonl.gz matches inputs/manifest.json.',
                    'cd nfl_paircheck_lab_20260922 && python3 run_experiment.py && python3 verify_results.py && python3 analyze.py',
                    'Do not commit restored gzip bytes or the kit zip.'
                ],
                note='No scenario was executed. This file is not a profit result.')


def atomic_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + '.partial')
    tmp.write_text(json.dumps(value, indent=2, allow_nan=False))
    tmp.replace(path)


def save_rows(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + '.partial')
    with gzip.open(tmp, 'wt') as handle:
        for row in rows:
            handle.write(json.dumps(row, separators=(',', ':')) + '\n')
    tmp.replace(path)


def load_inputs():
    global EVENTS, MARKETS, WEEKS
    missing = missing_inputs()
    if missing:
        raise FileNotFoundError('missing inputs: ' + ', '.join(missing))
    with gzip.open(INPUTS / 'events.jsonl.gz', 'rt') as handle:
        EVENTS = [json.loads(line) for line in handle]
    MARKETS = json.loads((INPUTS / 'markets.json').read_text())
    WEEKS = json.loads((INPUTS / 'week_membership.json').read_text())
    cohort = json.loads((INPUTS / 'manifest.json').read_text())['cohort']
    if cohort.get('games') != 31:
        raise RuntimeError('Q7 is frozen to the 31-game development cohort')
    return cohort


def one(case):
    queue, delay, arm = case
    name = scenario_name(queue, delay, arm)
    began = time.monotonic()
    replay = make_replay(MARKETS, scenario_config(queue, delay), arm)
    end = max(market['kickoff'] - 10800 for market in MARKETS.values()) + 300
    for row in EVENTS:
        if row['at'] > end:
            break
        if row.get('kind') == 'quote':
            replay.on_quote(row)
        else:
            replay.on_trade(row)
    result = replay.finish(end)
    result.update(scenario=name, elapsed_seconds=time.monotonic() - began,
                  evidence='Q7_CHOSEN_PAIR_CHECK_REUSED_31_GAME_DEVELOPMENT_HYPOTHETICAL_EXECUTION')
    result['week_contributions'] = {week: sum(game['cashflow'] for game in result['per_game']
                                              if WEEKS[game['event']] == week)
                                    for week in ('week1', 'week2')}
    ranked = sorted((game['cashflow'] for game in result['per_game']), reverse=True)
    result['pnl_excluding_top_two_games'] = sum(ranked[2:]) if result['all_flat'] else None
    for suffix, rows in (('fills', replay.fills), ('orders', replay.order_records.values()),
                         ('decisions', replay.decisions)):
        save_rows(ROOT / 'results' / f'{name}_{suffix}.jsonl.gz', rows)
    atomic_json(ROOT / 'results' / f'{name}.json', result)
    return result


def execute():
    pins = q6_pin_mismatches()
    if pins:
        raise RuntimeError('Frozen Q6 pins do not match: ' + ', '.join(pins))
    missing = missing_inputs()
    if missing:
        document = not_run_document(missing)
        atomic_json(ROOT / 'results' / 'NOT_RUN.json', document)
        return document
    cohort = load_inputs()
    summary = dict(status='RUNNING', cohort=cohort, scenarios={}, failures={}, pnl=None)
    cases = [(queue, delay, arm) for queue in QUEUES for delay in DELAYS for arm in ARMS]
    with ProcessPoolExecutor(max_workers=3, mp_context=multiprocessing.get_context('fork')) as pool:
        futures = {pool.submit(one, case): case for case in cases}
        for future in as_completed(futures):
            queue, delay, arm = futures[future]
            name = scenario_name(queue, delay, arm)
            try:
                result = future.result()
            except Exception as exc:
                failure = dict(scenario=name, status='FAILED_NO_COMPLETED_PNL',
                               traceback=''.join(traceback.format_exception(exc)))
                summary['failures'][name] = failure
                summary['status'] = 'FAILED_NO_COMPLETED_PNL'
                atomic_json(ROOT / 'results' / f'{name}_failure.json', failure)
                atomic_json(ROOT / 'results' / 'experiment_summary.json', summary)
                continue
            summary['scenarios'][result['scenario']] = result
            atomic_json(ROOT / 'results' / 'experiment_summary.json', summary)
    if summary['failures']:
        summary['status'] = 'FAILED_NO_COMPLETED_PNL'
        summary['pnl'] = None
    else:
        summary['status'] = 'COMPLETE'
    atomic_json(ROOT / 'results' / 'experiment_summary.json', summary)
    return summary


def main():
    document = execute()
    print(document.get('status'), 'scenarios_executed',
          len(document.get('scenarios', {})) if document.get('status') == 'COMPLETE' else 0, flush=True)
    if document.get('status') == 'FAILED_NO_COMPLETED_PNL':
        raise SystemExit(1)
    if document.get('status') != 'COMPLETE':
        raise SystemExit(3)
if __name__ == '__main__':
    main()
