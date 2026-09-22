"""Run only the bounded metadata audit in DISCOVERY_SPEC.md."""
import concurrent.futures
import gzip
import hashlib
import json
import re
from collections import defaultdict
from extend import ROOT, get, epoch, save

SERIES = ['KXNFLGAME','KXNCAAFGAME','KXWNBAGAME','KXMLBGAME','KXNHLGAME','KXNBAGAME']


def select(ids, limit=8):
    by_day = defaultdict(list)
    for event in sorted(set(ids)):
        match = re.search(r'-26SEP(\d{2})', event)
        if match and 1 <= int(match[1]) <= 20:
            by_day[match[1]].append(event)
    chosen = []
    rank = 0
    while len(chosen) < limit:
        added = False
        for day in sorted(by_day):
            if rank < len(by_day[day]):
                chosen.append(by_day[day][rank])
                added = True
                if len(chosen) == limit:
                    break
        if not added:
            break
        rank += 1
    return chosen, by_day


def inspect(series):
    pages, ids, cursors, cursor = [], set(), set(), None
    path = ROOT/'availability'/f'{series}.jsonl.gz'
    path.parent.mkdir(exist_ok=True)
    result = dict(series=series, status='DISCOVERY_FAILED', pages=0)
    try:
        for _ in range(20):
            params=dict(series_ticker=series,min_close_ts=int(epoch('2026-09-01T00:00:00Z')),
                        max_close_ts=int(epoch('2026-09-21T00:00:00Z')),limit=1000)
            if cursor:params['cursor']=cursor
            data,source=get('markets',params)
            pages.append(dict(source=source,response=data))
            ids.update(m['event_ticker'] for m in data.get('markets',[]))
            cursor=data.get('cursor')
            if not cursor:break
            if cursor in cursors:raise ValueError('Repeated discovery cursor')
            cursors.add(cursor)
        else:raise ValueError('Pagination not exhausted')
        selected,by_day=select(ids)
        count=sum(len(events) for events in by_day.values())
        result.update(status='RESERVED_METADATA_ONLY' if len(selected)==8 else 'SPARSE_METADATA' if selected else 'NO_EVENTS_IN_DECLARED_WINDOW',
            event_count=count,date_count=len(by_day),reserved=selected,events_by_day=dict(by_day),pagination_exhausted=True)
    except Exception as error:
        result['failure']=str(error)
    with gzip.open(path,'wt') as f:
        for page in pages:f.write(json.dumps(page,separators=(',',':'))+'\n')
    result.update(pages=len(pages),raw_file=str(path.relative_to(ROOT)),raw_sha256=hashlib.sha256(path.read_bytes()).hexdigest())
    print(series,result['status'],result.get('event_count'), 'events',flush=True)
    return result


if __name__=='__main__':
    results=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        for result in pool.map(inspect,SERIES):
            results.append(result)
            save(ROOT/'MARKET_AVAILABILITY.json',dict(series=results,complete=len(results)==6,
                 note='Metadata availability and deterministic reservations only; no profitability or replay admission.'))
