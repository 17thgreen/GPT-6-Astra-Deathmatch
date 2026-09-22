"""Bounded GET-only census. Preserves errors; no orders, loops or retries."""
import json,urllib.request,urllib.parse,datetime,concurrent.futures,statistics
from pathlib import Path
from adapter import maker_coefficient,indicative_pair
BASE='https://api.elections.kalshi.com/trade-api/v2'
SERIES=['KXNFLGAME','KXNCAAFGAME','KXNBAGAME','KXWNBAGAME','KXMLBGAME','KXNHLGAME']
ROOT=Path(__file__).resolve().parent

def stamp():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def get(path):
    url=BASE+path
    with urllib.request.urlopen(url,timeout=15) as f:d=json.load(f)
    return d,dict(url=url,received_at=stamp())
def one(ticker):
    out=dict(series=ticker,requests=[],events=[],errors=[])
    try:
        s,source=get('/series/'+ticker);out['series_metadata']=s['series'];out['requests'].append(source)
        response,source=get('/events?'+urllib.parse.urlencode(dict(series_ticker=ticker,status='open',limit=5,with_nested_markets='true')));out['requests'].append(source)
        for e in response['events'][:5]:
            er=dict(metadata=e,markets=[]);out['events'].append(er)
            for m in sorted(e.get('markets',[]),key=lambda x:x['ticker'])[:2]:
                r=dict(ticker=m['ticker'],pregame_admitted=False,admission_reason='independent_start_time_not_supplied');er['markets'].append(r)
                try:
                    if m.get('market_type')!='binary' or str(m.get('notional_value_dollars')) not in ('1','1.0','1.00','1.0000'):raise ValueError('Unsupported or missing binary $1 notional')
                    coefficient=maker_coefficient(s['series'],e);r['maker_coefficient']=str(coefficient)
                    book,source=get('/markets/'+urllib.parse.quote(m['ticker'])+'/orderbook');out['requests'].append(source)
                    r.update(book=book,source=source,diagnostic=indicative_pair(book,coefficient))
                except Exception as exc:r['error']=str(exc);out['errors'].append(dict(ticker=m['ticker'],error=str(exc)))
    except Exception as exc:out['errors'].append(dict(series=ticker,error=str(exc)))
    return out

def summarize(out):
    rows=[r for e in out['events'] for r in e['markets']]
    usable=[r['diagnostic'] for r in rows if r.get('diagnostic',{}).get('usable')]
    return dict(series=out['series'],events=len(out['events']),tickers=len(rows),two_sided=sum(r.get('diagnostic',{}).get('two_sided',False) for r in rows),usable=len(usable),positive_margin=sum(d['positive_margin'] for d in usable),median_margin_cents=statistics.median(float(d['buffered_pair_margin'])*100 for d in usable) if usable else None,median_larger_best_level_size=statistics.median(max(float(d['yes_best_level_size']),float(d['no_best_level_size'])) for d in usable) if usable else None,errors=len(out['errors']))

if __name__=='__main__':
    started=stamp()
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:results=list(pool.map(one,SERIES))
    result=dict(started_at=started,finished_at=stamp(),evidence='DESCRIPTIVE_SNAPSHOT_NOT_PROFIT_OR_QUEUE_PROBABILITY',selection='First 5 open events in API order, first 2 sorted tickers per event',series=results,summary=[summarize(r) for r in results])
    (ROOT/'CENSUS.json').write_text(json.dumps(result,indent=2,allow_nan=False))
    for r in result['summary']:print(json.dumps(r),flush=True)
