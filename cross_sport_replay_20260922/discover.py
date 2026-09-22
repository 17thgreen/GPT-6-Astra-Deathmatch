"""GET-only deterministic cohort resolution. Does not inspect price tapes."""
import json,time,urllib.request,urllib.parse,datetime,concurrent.futures,re
from pathlib import Path
ROOT=Path(__file__).resolve().parent
BASE='https://api.elections.kalshi.com/trade-api/v2/'
SERIES=['KXNCAAFGAME','KXWNBAGAME']

def epoch(s):return datetime.datetime.fromisoformat(s.replace('Z','+00:00')).timestamp()
def get(path,params=None):
    url=BASE+path+('?' + urllib.parse.urlencode(params) if params else '')
    errors=[]
    for attempt in range(3):
        try:
            with urllib.request.urlopen(url,timeout=15) as f:body=json.load(f)
            return body,dict(url=url,received_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),prior_errors=errors)
        except Exception as e:
            errors.append(str(e))
            if attempt==2:raise RuntimeError(json.dumps(dict(url=url,errors=errors)))
            time.sleep(1)

def listing(series):
    pages=[];cursor=None;seen=set();markets=[]
    for _ in range(20):
        p=dict(series_ticker=series,min_close_ts=int(epoch('2026-09-14T00:00:00Z')),max_close_ts=int(epoch('2026-09-22T00:00:00Z')),limit=1000)
        if cursor:p['cursor']=cursor
        d,source=get('markets',p);pages.append(dict(source=source,response=d));markets.extend(d['markets'])
        cursor=d.get('cursor')
        if not cursor:break
        if cursor in seen:raise ValueError('Repeated discovery cursor')
        seen.add(cursor)
    else:raise ValueError('Unfinished discovery pagination')
    ids=sorted({m['event_ticker'] for m in markets if re.match(series+r'-26SEP(14|15|16|17|18|19|20)',m['event_ticker'])})
    (ROOT/(series+'_discovery.json')).write_text(json.dumps(dict(pages=pages,candidate_events=ids),indent=2))
    print(series,'candidates',len(ids),'reserved',ids[:4],flush=True)
    return [(series,e) for e in ids[:4]]

def resolve(pair):
    series,event=pair;r=dict(series=series,event=event,admitted=False)
    try:
        body,source=get('events/'+event);r['metadata']=body;r['metadata_source']=source
        milestones,source=get('milestones',dict(related_event_ticker=event,limit=100));r['milestones']=milestones;r['schedule_source']=source
        kind='football_game' if series=='KXNCAAFGAME' else 'basketball_game'
        ms=[m for m in milestones.get('milestones',[]) if m.get('type')==kind and event in m.get('related_event_tickers',[]) and m.get('category')=='Sports']
        if milestones.get('cursor') or len(ms)!=1:raise ValueError('Missing, ambiguous or unexhausted schedule')
        r['kickoff']=epoch(ms[0]['start_date'])
        e=body['event'];markets=body.get('markets',e.get('markets',[]))
        if len(markets)!=2 or e.get('collateral_return_type')!='MECNET' or not e.get('mutually_exclusive'):raise ValueError('Unsupported event structure')
        for m in markets:
            if m['market_type']!='binary' or float(m['notional_value_dollars'])!=1 or m.get('price_level_structure')!='linear_cent':raise ValueError('Unsupported market type, notional or grid')
        r['tickers']=sorted(m['ticker'] for m in markets);r['admitted']=True
    except Exception as ex:r['failure']=str(ex)
    print(event,'ADMITTED' if r['admitted'] else r['failure'],flush=True)
    return r

if __name__=='__main__':
    failures=[];pairs=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as p:
        fs={p.submit(listing,s):s for s in SERIES}
        for f in concurrent.futures.as_completed(fs):
            try:pairs.extend(f.result())
            except Exception as e:failures.append(dict(series=fs[f],error=str(e)))
    out=dict(expected_slots=8,selection='First four lexicographic reserved event IDs per series; no replacements',discovery_failures=failures,games=[])
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as p:
        for result in p.map(resolve,sorted(pairs)):
            out['games'].append(result);(ROOT/'COHORT.json').write_text(json.dumps(out,indent=2))
    out['complete']=len(out['games'])==8 and all(g['admitted'] for g in out['games']) and not failures
    (ROOT/'COHORT.json').write_text(json.dumps(out,indent=2));print('COHORT_COMPLETE',out['complete'],flush=True)
