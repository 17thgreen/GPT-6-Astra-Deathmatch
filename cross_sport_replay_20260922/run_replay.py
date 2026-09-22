"""Run the twelve preregistered M2 alternatives, once, after a Git source freeze."""
import gzip
import json
import time
from dataclasses import replace
from pathlib import Path
from normalize import load, sha, read, ROOT
from transport import ListingRouter, Config


def checked_freeze():
    freeze = read(ROOT / 'FROZEN_REPLAY.json')
    for name, digest in freeze['sha256'].items():
        if sha(ROOT / name) != digest:
            raise ValueError('Frozen source/input mismatch: ' + name)


def save(path, value):
    path.write_text(json.dumps(value, indent=2, allow_nan=False))


def rows(path, values):
    with gzip.open(path, 'wt', compresslevel=1) as stream:
        for row in values:
            stream.write(json.dumps(row, separators=(',', ':'), allow_nan=False) + '\n')


def main():
    checked_freeze()
    records, all_markets, coverage = load()
    outdir = ROOT / 'results'
    outdir.mkdir(exist_ok=True)
    if (outdir / 'experiment_summary.json').exists():
        raise ValueError('Existing outcome record; preserve it and declare a new run path')
    summary = dict(scenarios={}, failures={}, cohort_games=8,
                   evidence='M2_EIGHT_GAME_RETROSPECTIVE_HYPOTHETICAL_Q7_TRANSPORT')
    save(outdir / 'experiment_summary.json', summary)
    for group in ('NCAAF', 'WNBA', 'combined'):
        markets = {t: m for t, m in all_markets.items() if group == 'combined' or m['series'] == 'KX' + group + 'GAME'}
        tape = [r for r in records if r['ticker'] in markets]
        for queue in (3300, 10000):
            for delay in (.25, 5):
                name = f'{group}_q{queue}_d{delay:g}'
                started = time.monotonic()
                try:
                    cfg = replace(Config(), queue_early=queue, quote_source='candles',
                        liquidation_lead_seconds=300, order_delay_seconds=delay, cancel_delay_seconds=delay)
                    engine = ListingRouter(markets, cfg)
                    end = max(m['kickoff'] - 10800 for m in markets.values()) + 300
                    for row in tape:
                        if row['at'] > end:
                            break
                        if row.get('kind') == 'quote':
                            engine.on_quote(row)
                        else:
                            engine.on_trade(row)
                    result = engine.finish(end)
                    result.update(scenario=name, group=group, evidence=summary['evidence'],
                                  elapsed_seconds=time.monotonic() - started)
                    event_sport = {m['event']: m['series'] for m in markets.values()}
                    result['sport_cashflows'] = {s: sum(g['cashflow'] for g in result['per_game']
                        if event_sport[g['event']] == s) for s in sorted(set(event_sport.values()))}
                    result['pair_checks'] = len(engine.pair_records)
                    result['pair_rejections'] = sum(not r['price_check_passes'] for r in engine.pair_records)
                    for suffix, values in [('fills', engine.fills), ('orders', engine.order_records.values()),
                                           ('pairs', engine.pair_records)]:
                        rows(outdir / f'{name}_{suffix}.jsonl.gz', values)
                    save(outdir / f'{name}.json', result)
                    summary['scenarios'][name] = result
                    print(name, 'completed net', result['completed_strategy_pnl'],
                          'residual', result['unresolved_contracts'], flush=True)
                except Exception as error:
                    summary['failures'][name] = dict(error=repr(error), completed_strategy_pnl=None)
                    print(name, 'FAILED', repr(error), flush=True)
                save(outdir / 'experiment_summary.json', summary)
    checked_freeze()
    if summary['failures']:
        raise RuntimeError('Failures retained; no complete matrix claim')


if __name__ == '__main__':
    main()
