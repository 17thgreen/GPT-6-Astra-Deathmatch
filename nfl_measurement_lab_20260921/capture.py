"""Finite public REST capture; GET-only allowlist, no account/order endpoints."""
import argparse
import hashlib
import json
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent
BASE = 'https://api.elections.kalshi.com/trade-api/v2/'


def allowed(path):
    return bool(re.fullmatch(r'events/KXNFLGAME-[A-Z0-9]+|markets/KXNFLGAME-[A-Z0-9]+-[A-Z0-9]+/orderbook|markets/trades', path))


def get(path, params):
    if not allowed(path):
        raise ValueError('Public research GET route required')
    attempts = []
    for attempt in range(2):
        start = time.time()
        try:
            with urlopen(Request(BASE + path + '?' + urlencode(params),
                                 headers={'User-Agent': 'NFLMeasurementResearch/3.0'}), timeout=12) as response:
                body = json.load(response)
            return dict(request_at=start, received_at=time.time(), path=path, params=params,
                        attempts=attempts, body=body)
        except Exception as exc:
            attempts.append(dict(request_at=start, failed_at=time.time(), error=repr(exc)))
    return dict(path=path, params=params, attempts=attempts, error='All bounded attempts failed', received_at=time.time())


def trade_pages(ticker, start, end):
    records = []
    cursor = None
    seen = set()
    for page in range(100):
        params = dict(ticker=ticker, min_ts=start, max_ts=end, limit=1000, is_block_trade='false')
        if cursor:
            params['cursor'] = cursor
        row = get('markets/trades', params)
        records.append(dict(ticker=ticker, page=page, **row))
        if row.get('error'):
            return records, False
        cursor = row['body'].get('cursor')
        if not cursor:
            return records, True
        if cursor in seen:
            break
        seen.add(cursor)
    return records, False


def capture(seconds=720, interval=5):
    if not 30 <= seconds <= 3600 or interval < 1:
        raise ValueError('Use a finite 30–3600 second run and interval >=1')
    manifest = json.loads((ROOT/'HOLDOUT_MANIFEST.json').read_text())
    target = ROOT/'forward'
    target.mkdir(exist_ok=True)
    output = target/'observations.jsonl'
    if output.exists():
        raise ValueError('Existing capture retained; use a separate experiment directory')
    started = time.time()
    tickers = []
    errors = 0
    coverage = []
    with output.open('w') as out, ThreadPoolExecutor(max_workers=8) as pool:
        def save(kind, row):
            out.write(json.dumps(dict(kind=kind, recorded_at=time.time(), **row), separators=(',', ':'))+'\n')
            out.flush()
        for event in manifest['measurement_development_events']:
            row = get('events/'+event, {'with_nested_markets': 'true'})
            save('metadata', row)
            if row.get('error'):
                raise RuntimeError('Metadata unavailable; cannot identify panel')
            body = row['body']; ms = body.get('markets') or body['event'].get('markets', [])
            if len(ms) != 2 or not body['event'].get('mutually_exclusive') or body['event'].get('collateral_return_type') != 'MECNET':
                raise ValueError('Unverified binary event')
            for m in ms:
                if m.get('price_level_structure') != 'linear_cent' or '$0.50' not in m.get('rules_secondary', ''):
                    raise ValueError('Unexpected market rules')
            tickers.extend(sorted(m['ticker'] for m in ms))
        through = {t:int(started)-3600 for t in tickers}
        next_trades = 0
        deadline = time.monotonic()+seconds
        poll = 0
        while time.monotonic() < deadline:
            cycle = time.monotonic()
            jobs = {pool.submit(get, 'markets/'+t+'/orderbook', {'depth':10}):('book',t) for t in tickers}
            until = int(time.time())-2
            if cycle >= next_trades:
                jobs.update({pool.submit(trade_pages,t,through[t]-120,until):('trades',t) for t in tickers})
                next_trades = cycle+30
            for future in as_completed(jobs):
                kind,ticker = jobs[future]
                if kind == 'book':
                    row = future.result()
                    save('error' if row.get('error') else 'book', dict(ticker=ticker,poll=poll,operation=kind,**row))
                    errors += bool(row.get('error'))
                else:
                    records,complete = future.result()
                    for row in records:
                        save('error' if row.get('error') else 'trades', dict(poll=poll,operation=kind,**row))
                        errors += bool(row.get('error'))
                    if complete:
                        span=dict(ticker=ticker,start=through[ticker]-120,end=until,poll=poll)
                        coverage.append(span);save('coverage',span);through[ticker]=until
                    else:
                        save('error',dict(ticker=ticker,poll=poll,operation='pagination',error='Incomplete interval'))
                        errors += 1
            if poll % 12 == 0:
                print(json.dumps(dict(poll=poll,elapsed=round(time.time()-started,1),errors=errors)),flush=True)
            poll += 1
            time.sleep(max(0,min(interval-(time.monotonic()-cycle),deadline-time.monotonic())))
        # Final paginated sweep covers all prior book observations. A later print
        # can still be published after this sweep; do not claim tape finality.
        final_until = int(time.time())
        jobs = {pool.submit(trade_pages,t,through[t]-120,final_until):t for t in tickers}
        for future in as_completed(jobs):
            ticker=jobs[future];records,complete=future.result()
            for row in records:
                save('error' if row.get('error') else 'trades',dict(poll=poll,operation='final_trades',**row))
                errors += bool(row.get('error'))
            if complete:
                span=dict(ticker=ticker,start=through[ticker]-120,end=final_until,poll=poll)
                coverage.append(span);save('coverage',span)
            else:
                errors += 1;save('error',dict(ticker=ticker,operation='final_pagination',error='Incomplete interval'))
    result=dict(started_utc=datetime.fromtimestamp(started,timezone.utc).isoformat(),
                ended_utc=datetime.now(timezone.utc).isoformat(),target_seconds=seconds,polls=poll,
                tickers=tickers,errors=errors,complete_intervals=coverage,
                sha256=hashlib.sha256(output.read_bytes()).hexdigest(),
                status='BOUNDED_CAPTURE_COMPLETE_NO_ORDERS_PLACED')
    (target/'capture_summary.json').write_text(json.dumps(result,indent=2))
    print(json.dumps({k:v for k,v in result.items() if k!='complete_intervals'}),flush=True)


if __name__ == '__main__':
    p=argparse.ArgumentParser();p.add_argument('--seconds',type=int,default=720);p.add_argument('--interval',type=float,default=5)
    args=p.parse_args();capture(args.seconds,args.interval)
