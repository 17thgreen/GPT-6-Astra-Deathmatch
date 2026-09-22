"""Bounded public capture of the prespecified M3 extension; immutable M2 inputs."""
import concurrent.futures
import gzip
import hashlib
import json
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent
M2 = ROOT.parent / 'cross_sport_replay_20260922'
sys.path.insert(0, str(M2))
from discover import get, epoch


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, obj):
    temp = path.with_suffix(path.suffix + '.partial')
    temp.write_text(json.dumps(obj, indent=2))
    temp.replace(path)


def write_rows(path, rows):
    with gzip.open(path, 'wt') as f:
        for row in rows:
            f.write(json.dumps(row, separators=(',', ':')) + '\n')


def capture(g, ticker):
    root = ROOT / 'data' / ticker
    root.mkdir(parents=True, exist_ok=True)
    prior = json.loads((M2 / 'data' / ticker / 'manifest.json').read_text())
    start, end = prior['end'], g['kickoff'] - 1800 + 300
    seen, trades, sources, cursor, cursors = {}, [], [], None, set()
    for page in range(200):
        params = dict(ticker=ticker, min_ts=int(start), max_ts=int(end), limit=1000, is_block_trade='false')
        if cursor:
            params['cursor'] = cursor
        data, source = get('markets/trades', params)
        sources.append(source)
        for t in data.get('trades', []):
            if t['ticker'] != ticker or t.get('is_block_trade') or not start <= epoch(t['created_time']) <= end:
                raise ValueError('Invalid extension trade')
            identity = t['trade_id']
            if identity in seen and seen[identity] != t:
                raise ValueError('Conflicting duplicate trade')
            if identity not in seen:
                seen[identity] = t
                trades.append(t)
        cursor = data.get('cursor')
        if not cursor:
            break
        if cursor in cursors:
            raise ValueError('Repeated cursor')
        cursors.add(cursor)
    else:
        raise ValueError('Unfinished pagination')
    data, source = get('series/' + g['series'] + '/markets/' + ticker + '/candlesticks',
                       dict(start_ts=int(start), end_ts=int(end), period_interval=1))
    sources.append(source)
    candles = data.get('candlesticks', [])
    for c in candles:
        if not start <= c['end_period_ts'] <= end:
            raise ValueError('Candle outside extension')
    write_rows(root / 'trades.jsonl.gz', trades)
    write_rows(root / 'candles.jsonl.gz', candles)
    result = dict(ticker=ticker, event=g['event'], series=g['series'], start=start, end=end,
        pagination_exhausted=True, trade_pages=page+1, trades=len(trades), candles=len(candles), sources=sources,
        sha256={n: sha(root / n) for n in ('trades.jsonl.gz', 'candles.jsonl.gz')})
    save(root / 'manifest.json', result)
    print(ticker, 'captured', len(trades), 'trades;', len(candles), 'candles', flush=True)
    return result


def main():
    cohort = json.loads((M2 / 'COHORT.json').read_text())
    assert cohort['complete'] and len(cohort['games']) == 8
    out = dict(markets=[], failures=[], complete=False)
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        tasks = {pool.submit(capture, g, t): t for g in cohort['games'] for t in g['tickers']}
        for f in concurrent.futures.as_completed(tasks):
            try:
                out['markets'].append(f.result())
            except Exception as error:
                out['failures'].append(dict(ticker=tasks[f], error=str(error)))
                print('FAILED', tasks[f], str(error), flush=True)
            save(ROOT / 'EXTENSION_CAPTURE.json', out)
    out['complete'] = len(out['markets']) == 16 and not out['failures']
    save(ROOT / 'EXTENSION_CAPTURE.json', out)
    print('COMPLETE', out['complete'], flush=True)


if __name__ == '__main__':
    main()
