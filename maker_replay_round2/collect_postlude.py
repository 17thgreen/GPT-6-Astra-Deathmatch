"""Capture five post-cutoff minutes to trigger the unchanged comparator's stop rule."""
from collect_public import ROOT,get
from datetime import datetime,timedelta,timezone
from concurrent.futures import ThreadPoolExecutor,as_completed
import gzip,json,hashlib,time


def capture(game):
    event=game['event'];d=ROOT/'data'/event;d.mkdir(parents=True,exist_ok=True)
    p=d/'event.json'
    j=json.loads(p.read_text()) if p.exists() else get('events/'+event,{'with_nested_markets':'true'})
    markets=j.get('markets') or j['event']['markets'];out=[]
    cutoff=datetime.fromisoformat(game['kickoff'])-timedelta(hours=3);end=cutoff+timedelta(minutes=5)
    for m in markets:
        ticker=m['ticker'];file=d/(ticker+'.postlude.jsonl.gz');mf=d/(ticker+'.postlude.manifest.json')
        if file.exists() and mf.exists():
            item=json.loads(mf.read_text())
            if item['sha256']==hashlib.sha256(file.read_bytes()).hexdigest():out.append(item);continue
        cursor=None;seen=set();n=0;pages=0
        with gzip.open(file,'wt') as f:
            while True:
                q={'ticker':ticker,'limit':1000,'min_ts':int(cutoff.timestamp()),'max_ts':int(end.timestamp()),'is_block_trade':'false'}
                if cursor:q['cursor']=cursor
                body=get('markets/trades',q);pages+=1
                for row in body.get('trades',[]):
                    at=datetime.fromisoformat(row['created_time'].replace('Z','+00:00'))
                    if not cutoff<=at<=end:raise ValueError('Postlude outside window')
                    if row.get('is_block_trade') or row['trade_id'] in seen:continue
                    seen.add(row['trade_id']);f.write(json.dumps(row,separators=(',',':'))+'\n');n+=1
                nxt=body.get('cursor')
                if not nxt:break
                if nxt==cursor or pages>100:raise ValueError('Postlude pagination failed')
                cursor=nxt;time.sleep(.2)
        item={'ticker':ticker,'trades':n,'pages':pages,'pagination_exhausted':True,
              'path':str(file.relative_to(ROOT)),'sha256':hashlib.sha256(file.read_bytes()).hexdigest(),
              'from_utc':cutoff.isoformat(),'through_utc':end.isoformat(),'retrieved_at':datetime.now(timezone.utc).isoformat()}
        mf.write_text(json.dumps(item,indent=2));out.append(item)
    print(event,sum(x['trades'] for x in out),'postlude trades',flush=True)
    return out


if __name__=='__main__':
    games=json.loads((ROOT/'data/cohort.json').read_text());records=[]
    with ThreadPoolExecutor(max_workers=2) as pool:
        for task in as_completed([pool.submit(capture,g) for g in games]):records.extend(task.result())
    (ROOT/'data/postlude_manifest.json').write_text(json.dumps({'purpose':'legacy stop trigger; repaired maker refuses post-cutoff entries','markets':records},indent=2))
