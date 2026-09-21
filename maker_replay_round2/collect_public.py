"""Read-only, resumable public REST capture of the frozen 2026 NFL week-one cohort."""
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.parse import urlencode
from urllib.error import HTTPError
from datetime import datetime, timedelta, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed
import gzip, hashlib, json, time

ROOT=Path(__file__).resolve().parent
BASE='https://api.elections.kalshi.com/trade-api/v2/'


def get(path,params=None):
    url=BASE+path+('?' + urlencode(params) if params else '')
    for retry in range(5):
        try:
            with urlopen(Request(url,headers={'User-Agent':'NFLResearchAudit/2.0'}),timeout=40) as r:
                return json.load(r)
        except HTTPError as e:
            if e.code not in (429,500,502,503,504):raise
            if retry==4:raise
            time.sleep(min(2**retry,8))
    raise RuntimeError('Unreachable')


def capture_game(game):
    event=game['event']; kickoff=datetime.fromisoformat(game['kickoff'])
    start=kickoff-timedelta(days=7);end=kickoff-timedelta(hours=3)
    d=ROOT/'data'/event;d.mkdir(parents=True,exist_ok=True)
    metadata=d/'event.json'
    if not metadata.exists():metadata.write_text(json.dumps(get('events/'+event,{'with_nested_markets':'true'}),indent=2))
    meta=json.loads(metadata.read_text());markets=meta.get('markets') or meta['event'].get('markets',[])
    if len(markets)!=2:raise ValueError(f'{event}: expected exactly two team markets')
    rows=[]
    for market in markets:
        ticker=market['ticker'];raw=d/(ticker+'.jsonl.gz');manifest=d/(ticker+'.manifest.json')
        if raw.exists() and manifest.exists():
            record=json.loads(manifest.read_text())
            if record.get('pagination_exhausted') and record['sha256']==hashlib.sha256(raw.read_bytes()).hexdigest():
                rows.append(record);continue
        ids=set();pages=0;seen_cursors=set();cursor=None;captured=0;block=0
        with gzip.open(raw,'wt',encoding='utf-8') as f:
            while True:
                params={'ticker':ticker,'limit':1000,'min_ts':int(start.timestamp()),
                        'max_ts':int(end.timestamp()),'is_block_trade':'false'}
                if cursor:params['cursor']=cursor
                body=get('markets/trades',params);pages+=1
                for trade in body.get('trades',[]):
                    if trade.get('is_block_trade'):
                        block+=1;continue
                    identity=trade['trade_id']
                    if identity in ids:continue
                    at=datetime.fromisoformat(trade['created_time'].replace('Z','+00:00'))
                    if not start<=at<=end:raise ValueError('API returned an out-of-window print')
                    if trade['ticker']!=ticker:raise ValueError('Wrong ticker')
                    ids.add(identity);captured+=1;f.write(json.dumps(trade,separators=(',',':'))+'\n')
                cursor=body.get('cursor')
                if not cursor:break
                if cursor in seen_cursors or pages>=2000:raise RuntimeError('Pagination incomplete/repeated')
                seen_cursors.add(cursor);time.sleep(.20)
        record=dict(event=event,ticker=ticker,kickoff=game['kickoff'],from_utc=start.isoformat(),
                    through_utc=end.isoformat(),pages=pages,trades=captured,excluded_block_trades=block,
                    pagination_exhausted=True,sha256=hashlib.sha256(raw.read_bytes()).hexdigest(),
                    retrieved_at=datetime.now(timezone.utc).isoformat(),path=str(raw.relative_to(ROOT)))
        manifest.write_text(json.dumps(record,indent=2));rows.append(record)
        print(ticker,captured,'trades',pages,'pages',flush=True)
    return {'event':event,'metadata_sha256':hashlib.sha256(metadata.read_bytes()).hexdigest(),
            'collateral_return_type':meta['event'].get('collateral_return_type'),
            'mutually_exclusive':meta['event'].get('mutually_exclusive'),'markets':rows}


def main():
    cohort=json.loads((ROOT/'data/cohort.json').read_text())
    out={'cohort_rule':'All sixteen games in NFL season 2026 week 1, from the previous audit schedule; not selected by results.',
         'source':BASE,'window':'T-7 days through T-3 hours; no historical order books',
         'games':[],'failures':[]}
    with ThreadPoolExecutor(max_workers=2) as pool:
        pending={pool.submit(capture_game,g):g['event'] for g in cohort}
        for future in as_completed(pending):
            try:out['games'].append(future.result())
            except Exception as e:out['failures'].append({'event':pending[future],'error':repr(e)})
            (ROOT/'data/capture_manifest.json').write_text(json.dumps(out,indent=2))
    print(json.dumps({'complete_games':len(out['games']),'trades':sum(m['trades'] for g in out['games'] for m in g['markets']),'failures':out['failures']},indent=2),flush=True)
    if out['failures']:raise SystemExit(1)


if __name__=='__main__':main()
