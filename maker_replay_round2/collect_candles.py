"""Public historical bid/ask minute closes; no depth or receipt timestamps are supplied."""
from collect_public import ROOT,get
from datetime import datetime,timedelta,timezone
from concurrent.futures import ThreadPoolExecutor,as_completed
import gzip,hashlib,json


def capture(game):
    d=ROOT/'data'/game['event'];meta=json.loads((d/'event.json').read_text())
    markets=meta.get('markets') or meta['event']['markets'];records=[]
    kickoff=datetime.fromisoformat(game['kickoff']);start=int((kickoff-timedelta(days=7)).timestamp())
    end=int((kickoff-timedelta(hours=3)+timedelta(minutes=5)).timestamp())
    for market in markets:
        ticker=market['ticker'];file=d/(ticker+'.candles.jsonl.gz');manifest=d/(ticker+'.candles.manifest.json')
        if file.exists() and manifest.exists():
            old=json.loads(manifest.read_text())
            if old['sha256']==hashlib.sha256(file.read_bytes()).hexdigest():records.append(old);continue
        rows={};requests=0;lo=start
        while lo<end:
            hi=min(end,lo+3*86400)
            response=get('series/KXNFLGAME/markets/'+ticker+'/candlesticks',{'start_ts':lo,'end_ts':hi,'period_interval':1})
            requests+=1
            for candle in response.get('candlesticks',[]):
                at=candle['end_period_ts']
                if not start<=at<=end:raise ValueError('Out-of-window candle')
                if at in rows and rows[at]!=candle:raise ValueError('Conflicting boundary candle')
                rows[at]=candle
            lo=hi
        with gzip.open(file,'wt') as f:
            for at in sorted(rows):f.write(json.dumps(rows[at],separators=(',',':'))+'\n')
        expected=set(range(start,end+1,60));missing=sorted(expected-set(rows))
        item={'ticker':ticker,'event':game['event'],'candles':len(rows),'requests':requests,'missing_minutes':missing,
              'from_epoch':start,'through_epoch':end,'path':str(file.relative_to(ROOT)),
              'sha256':hashlib.sha256(file.read_bytes()).hexdigest(),'retrieved_at':datetime.now(timezone.utc).isoformat()}
        manifest.write_text(json.dumps(item,indent=2));records.append(item)
        print(ticker,len(rows),'minute candles; missing',len(missing),flush=True)
    return records


if __name__=='__main__':
    cohort=json.loads((ROOT/'data/cohort.json').read_text());rows=[]
    with ThreadPoolExecutor(max_workers=3) as pool:
        for task in as_completed([pool.submit(capture,g) for g in cohort]):rows.extend(task.result())
    (ROOT/'data/candle_manifest.json').write_text(json.dumps({'role':'Historical minute-end bid/ask, publication and queue depth unknown','markets':rows},indent=2))
