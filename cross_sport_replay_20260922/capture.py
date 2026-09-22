"""Resumable bounded raw-tape capture for the committed cohort."""
import json,gzip,hashlib,concurrent.futures
from pathlib import Path
from discover import ROOT,get,epoch
DATA=ROOT/'data'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def capture(g,m):
    ticker=m['ticker'];root=DATA/ticker;root.mkdir(parents=True,exist_ok=True);mp=root/'manifest.json'
    if mp.exists():
        old=json.loads(mp.read_text())
        if all(sha(root/n)==h for n,h in old['sha256'].items()):return old
    start=max(g['kickoff']-604800,epoch(m['open_time']));end=g['kickoff']-10800+300
    if start>=end:raise ValueError('No pregame listing window')
    sources=[];ids=set();cursor=None;cursors=set();trades=[]
    for page in range(200):
        params=dict(ticker=ticker,min_ts=int(start),max_ts=int(end),limit=1000,is_block_trade='false')
        if cursor:params['cursor']=cursor
        d,source=get('markets/trades',params);sources.append(source)
        for t in d.get('trades',[]):
            if t['ticker']!=ticker or t.get('is_block_trade') or not start<=epoch(t['created_time'])<=end:raise ValueError('Invalid trade identity/window')
            if t['trade_id'] not in ids:trades.append(t);ids.add(t['trade_id'])
        cursor=d.get('cursor')
        if not cursor:break
        if cursor in cursors:raise ValueError('Repeated trade cursor')
        cursors.add(cursor)
        if page%10==0:print(ticker,'trade pages',page+1,flush=True)
    else:raise ValueError('Incomplete trade pagination at page limit')
    with gzip.open(root/'trades.jsonl.gz','wt') as f:
        for t in trades:f.write(json.dumps(t,separators=(',',':'))+'\n')
    candles={};lo=int(start)
    while lo<end:
        hi=min(int(end),lo+3*86400)
        d,source=get('series/'+g['series']+'/markets/'+ticker+'/candlesticks',dict(start_ts=lo,end_ts=hi,period_interval=1));sources.append(source)
        for c in d.get('candlesticks',[]):
            at=c['end_period_ts']
            if not start<=at<=end:raise ValueError('Candle outside requested window')
            if at in candles and candles[at]!=c:raise ValueError('Conflicting candle boundary')
            candles[at]=c
        lo=hi
    with gzip.open(root/'candles.jsonl.gz','wt') as f:
        for at in sorted(candles):f.write(json.dumps(candles[at],separators=(',',':'))+'\n')
    out=dict(ticker=ticker,event=g['event'],series=g['series'],kickoff=g['kickoff'],start=start,end=end,pagination_exhausted=True,trade_pages=page+1,trades=len(trades),candles=len(candles),sources=sources,sha256={n:sha(root/n) for n in ['trades.jsonl.gz','candles.jsonl.gz']})
    mp.write_text(json.dumps(out,indent=2));print(ticker,'CAPTURED',len(trades),'trades',len(candles),'candles',flush=True);return out

if __name__=='__main__':
    cohort=json.loads((ROOT/'COHORT.json').read_text());assert cohort['complete'],'Incomplete cohort; no shrinking'
    tasks=[(g,m) for g in cohort['games'] for m in g['metadata'].get('markets',g['metadata']['event'].get('markets',[]))]
    out=dict(markets=[],failures=[])
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        fs={pool.submit(capture,g,m):m['ticker'] for g,m in tasks}
        for f in concurrent.futures.as_completed(fs):
            try:out['markets'].append(f.result())
            except Exception as e:out['failures'].append(dict(ticker=fs[f],error=str(e)));print('FAILED',fs[f],str(e),flush=True)
            (ROOT/'CAPTURE.json').write_text(json.dumps(out,indent=2))
    out['complete']=len(out['markets'])==16 and not out['failures'];(ROOT/'CAPTURE.json').write_text(json.dumps(out,indent=2));print('CAPTURE_COMPLETE',out['complete'],flush=True)
