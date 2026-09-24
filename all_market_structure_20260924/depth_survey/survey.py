"""AMS-004 public read-only survey. No order routes or credentials."""
import concurrent.futures as cf
import datetime as dt
import hashlib
import json
import time
import urllib.error
import urllib.parse
import urllib.request
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BASE = 'https://api.elections.kalshi.com/trade-api/v2'

def stamp(s):
    return dt.datetime.fromisoformat(s.replace('Z', '+00:00')).timestamp()

def classify(book, target):
    target = Decimal(str(target))
    if target <= 0:
        raise ValueError('nonpositive target')
    totals = {}
    for side in ('yes', 'no'):
        # Explicit missing fields are unavailable, not zero depth.
        levels = book[side + '_dollars']
        if levels is None:
            raise ValueError('null book side')
        values = [(Decimal(p), Decimal(q)) for p, q in levels]
        if any(p < 0 or p > 1 or q < 0 for p, q in values):
            raise ValueError('invalid depth')
        totals[side] = sum((q for p, q in values), Decimal(0))
    short = [s for s in ('yes', 'no') if totals[s] < target]
    return {'class': 'both_short' if len(short) == 2 else short[0] + '_short' if short else 'both_meet',
            'depth': {s: str(v) for s, v in totals.items()},
            'shortfall': {s: str(max(Decimal(0), target-v)) for s, v in totals.items()},
            'empty_sides': [s for s, v in totals.items() if v == 0]}

def get(job):
    name, path, params = job
    url = BASE + path + '?' + urllib.parse.urlencode(params)
    wall = time.time_ns(); raw = b''; status = None; error = None
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'AMS-004-public-research'}), timeout=12) as r:
            status = r.status; raw = r.read()
    except urllib.error.HTTPError as e:
        status = e.code; raw = e.read(); error = type(e).__name__
    except Exception as e:
        error = type(e).__name__
    rec = {'url': url, 'sent_ns': wall, 'received_ns': time.time_ns(), 'status': status,
           'error': error, 'sha256': hashlib.sha256(raw).hexdigest(), 'raw': raw.decode(errors='replace')}
    (ROOT/'capture'/f'{name}.json').write_text(json.dumps(rec)+'\n')
    try:
        data = json.loads(rec['raw']) if status == 200 else {}
        if not isinstance(data, dict): data = {}
    except ValueError:
        data = {}
    print(name, status, error, flush=True)
    return name, data, rec['received_ns']

def main():
    start = time.monotonic()
    (ROOT/'capture').mkdir()
    programs = []; cursor = None
    for i in range(2):
        params = {'status':'active', 'type':'liquidity', 'limit':10000}
        if cursor: params['cursor'] = cursor
        _, data, ns = get((f'catalog_{i}', '/incentive_programs', params))
        programs.extend(data.get('incentive_programs', []))
        cursor = data.get('next_cursor')
        if not cursor: break
    selected = {}
    for p in sorted(programs, key=lambda p:p['id']):
        if p.get('paid_out') or Decimal(p.get('target_size_fp', '0')) <= 0 or p['period_reward'] <= 0: continue
        if stamp(p['start_date']) <= ns/1e9 < stamp(p['end_date']): selected.setdefault(p['market_ticker'], p)
    tickers = sorted(selected, key=lambda t:hashlib.sha256(('AMS-004-20260924|'+t).encode()).hexdigest())[:200]
    panel = {'catalog_count':len(programs), 'catalog_cursor_remaining':bool(cursor), 'eligible_unique_markets':len(selected),
             'catalog_last_received_ns':ns, 'selected_before_books_ns':time.time_ns(), 'programs':[selected[t] for t in tickers]}
    (ROOT/'PANEL.json').write_text(json.dumps(panel, indent=2)+'\n')
    (ROOT/'PANEL_SHA256.txt').write_text(hashlib.sha256((ROOT/'PANEL.json').read_bytes()).hexdigest()+'\n')
    books = {}; metadata = {}; book_ns = {}
    jobs = []
    for i in range(0,len(tickers),50):
        ts = tickers[i:i+50]
        jobs.extend([(f'books_{i}', '/markets/orderbooks', {'tickers':','.join(ts)}),
                     (f'metadata_{i}', '/markets', {'tickers':','.join(ts),'limit':1000})])
    with cf.ThreadPoolExecutor(max_workers=4) as ex:
        for name, data, ns in ex.map(get, jobs):
            if name.startswith('books_'):
                for b in data.get('orderbooks', []): books[b['ticker']] = b.get('orderbook_fp', {}); book_ns[b['ticker']] = ns
            else:
                for m in data.get('markets', []): metadata[m['ticker']] = m
        fallback = []
        for t in tickers:
            path = '/markets/'+urllib.parse.quote(t,safe='')
            if t not in books: fallback.append((t+'_book',path+'/orderbook',{'depth':0}))
            if t not in metadata: fallback.append((t+'_metadata',path,{}))
        for i in range(0,len(fallback),4):
            if time.monotonic()-start >= 240: break
            for name,data,ns in ex.map(get,fallback[i:i+4]):
                if name.endswith('_book'):
                    t = name[:-5]
                    if 'orderbook_fp' in data: books[t] = data['orderbook_fp']; book_ns[t] = ns
                else:
                    if 'market' in data: metadata[data['market']['ticker']] = data['market']
    rows = []
    for t in tickers:
        p = selected[t]; m = metadata.get(t, {}); b = books.get(t)
        row = {'ticker':t, 'program':p, 'market_status':m.get('status'), 'book_received_ns':book_ns.get(t), 'class':'unavailable'}
        if b is not None and m:
            ns = book_ns[t]
            if m.get('status') not in ('open','active') or not stamp(p['start_date']) <= ns/1e9 < stamp(p['end_date']) or stamp(m['close_time']) <= ns/1e9:
                row['class'] = 'outside_open_window'
            else:
                try: row.update(classify(b,p['target_size_fp']))
                except (ValueError, KeyError, TypeError): pass
        rows.append(row)
    counts = {c:sum(r['class']==c for r in rows) for c in sorted({r['class'] for r in rows})}
    result = {'panel_summary':{k:v for k,v in panel.items() if k != 'programs'}, 'selected':len(tickers),
              'counts':counts, 'empty_side_markets':sum(bool(r.get('empty_sides')) for r in rows),
              'elapsed_seconds':time.monotonic()-start, 'rows':rows}
    (ROOT/'RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='rows'},indent=2))

if __name__ == '__main__': main()
