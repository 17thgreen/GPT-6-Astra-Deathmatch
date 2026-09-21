"""Bounded, credential-free GET-only book/flow recorder. No order endpoint exists here."""
import argparse, hashlib, json, time
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = Path(__file__).resolve().parent
BASE = 'https://api.elections.kalshi.com/trade-api/v2/'
EVENTS = ['KXNFLGAME-26SEP21NYGLAR', 'KXNFLGAME-26SEP24ATLGB']

def get(path, params):
    if not (path.startswith('events/') or path.startswith('markets/')):
        raise ValueError('Public market data routes only')
    started = time.time()
    for attempt in range(4):
        try:
            with urlopen(Request(BASE + path + '?' + urlencode(params),
                                 headers={'User-Agent': 'NFLQueueResearch/1.0'}), timeout=20) as r:
                body = json.load(r)
            return dict(request_at=started, received_at=time.time(), path=path, params=params, body=body)
        except HTTPError as e:
            if e.code not in (429, 500, 502, 503, 504) or attempt == 3: raise
            time.sleep(2 ** attempt)

def capture(polls=120, interval=5, resume=False):
    if not 1 <= polls <= 10000 or interval < 1: raise ValueError('Bounded capture required')
    target = ROOT / 'forward'; target.mkdir(exist_ok=True)
    path = target / 'observations.jsonl'
    if path.exists() and not resume: raise ValueError('Use --resume or a new directory')
    prior = [json.loads(line) for line in path.read_text().splitlines()] if resume and path.exists() else []
    start = min((r.get('request_at', time.time()) for r in prior), default=time.time())
    tickers = []; errors = [r for r in prior if r['kind']=='error']
    first_poll = max((r.get('poll', -1) for r in prior), default=-1)+1
    with path.open('a' if resume else 'w') as out, ThreadPoolExecutor(max_workers=4) as pool:
        def save(kind, payload):
            out.write(json.dumps(dict(kind=kind, recorded_at=time.time(), **payload), separators=(',', ':'))+'\n'); out.flush()
        for event in EVENTS:
            found = [r for r in prior if r['kind']=='metadata' and r['path']=='events/'+event]
            if found: payload=found[-1]
            else:
                payload=get('events/'+event, {'with_nested_markets':'true'}); save('metadata', payload)
            meta=payload['body']; ms=meta.get('markets') or meta['event'].get('markets', [])
            if len(ms)!=2 or meta['event'].get('collateral_return_type')!='MECNET':
                raise ValueError('Unverified event structure')
            tickers.extend(m['ticker'] for m in ms)
        through={t:int(start)-3600 for t in tickers}
        for r in prior:
            if r['kind']=='trades' and not r['body'].get('cursor'):
                through[r['ticker']]=max(through[r['ticker']], r['params']['max_ts'])
        if resume:
            save('resume',dict(at=time.time(),next_poll=first_poll,
                note='Sequential capture interrupted for four-worker independent public GETs; raw prior observations retained; partial prior round is not fabricated.'))
        def trade_pages(ticker, until):
            cursor=None; seen=set(); page=0; payloads=[]
            while True:
                params=dict(ticker=ticker,min_ts=through[ticker]-2,max_ts=until,limit=1000,is_block_trade='false')
                if cursor: params['cursor']=cursor
                payload=get('markets/trades',params)
                payloads.append(dict(ticker=ticker,page=page,**payload))
                page+=1; cursor=payload['body'].get('cursor')
                if not cursor: return payloads
                if cursor in seen or page>=100: raise ValueError('Pagination incomplete')
                seen.add(cursor)
        for poll in range(first_poll, polls):
            cycle=time.monotonic()
            jobs={pool.submit(get,'markets/'+t+'/orderbook',{'depth':10}):t for t in tickers}
            for future in as_completed(jobs):
                ticker=jobs[future]
                try: save('book',dict(poll=poll,ticker=ticker,**future.result()))
                except Exception as e:
                    err=dict(poll=poll,ticker=ticker,operation='book',error=repr(e),at=time.time())
                    errors.append(err); save('error',err)
            if poll%6==0 or poll==polls-1:
                until=int(time.time())
                jobs={pool.submit(trade_pages,t,until):t for t in tickers}
                for future in as_completed(jobs):
                    ticker=jobs[future]
                    try:
                        for payload in future.result(): save('trades',dict(poll=poll,**payload))
                        through[ticker]=until
                    except Exception as e:
                        err=dict(poll=poll,ticker=ticker,operation='trades',error=repr(e),at=time.time())
                        errors.append(err); save('error',err)
            if poll%12==0: print(json.dumps({'poll':poll,'elapsed_seconds':round(time.time()-start,1),'errors':len(errors)}),flush=True)
            if poll<polls-1: time.sleep(max(0,interval-(time.monotonic()-cycle)))
    summary=dict(started_utc=datetime.fromtimestamp(start,timezone.utc).isoformat(),
                 ended_utc=datetime.now(timezone.utc).isoformat(),polls=polls,interval=interval,
                 tickers=tickers,errors=errors,resumed=resume,resumed_at_poll=first_poll,
                 sha256=hashlib.sha256(path.read_bytes()).hexdigest())
    (target/'capture_summary.json').write_text(json.dumps(summary,indent=2))
    print(json.dumps(summary),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--polls',type=int,default=120);p.add_argument('--interval',type=float,default=5)
    p.add_argument('--resume',action='store_true')
    a=p.parse_args();capture(a.polls,a.interval,a.resume)
