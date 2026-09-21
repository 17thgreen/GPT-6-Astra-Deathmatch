"""Bounded public REST book recorder. No credentials, account calls or orders."""
from datetime import datetime,timezone
from pathlib import Path
import argparse,json,time
from collect_public import get,ROOT


def main():
    p=argparse.ArgumentParser();p.add_argument('--events',nargs='+',required=True)
    p.add_argument('--polls',type=int,default=1);p.add_argument('--interval',type=float,default=5)
    p.add_argument('--output',type=Path,default=ROOT/'data/forward_books.jsonl')
    args=p.parse_args()
    if not 1<=args.polls<=10000 or args.interval<1:raise ValueError('Bounded polls and at least one-second interval required')
    tickers=[]
    for event in args.events:
        if not event.startswith('KXNFLGAME-'):raise ValueError('NFL game events only')
        meta=get('events/'+event,{'with_nested_markets':'true'})
        for m in meta.get('markets') or meta['event'].get('markets',[]):tickers.append(m['ticker'])
    args.output.parent.mkdir(parents=True,exist_ok=True)
    with args.output.open('a') as f:
        for poll in range(args.polls):
            for ticker in tickers:
                before=datetime.now(timezone.utc).isoformat();start=time.monotonic()
                raw=get('markets/'+ticker+'/orderbook',{'depth':5})
                item={'ticker':ticker,'request_started_utc':before,'received_utc':datetime.now(timezone.utc).isoformat(),
                      'round_trip_seconds':time.monotonic()-start,'response':raw}
                f.write(json.dumps(item,separators=(',',':'))+'\n');f.flush()
                book=raw.get('orderbook_fp') or raw.get('orderbook') or {}
                best={side:book.get(side,[])[-1] if book.get(side) else None for side in ['yes_dollars','no_dollars']}
                print(ticker,best,flush=True)
            if poll+1<args.polls:time.sleep(args.interval)


if __name__=='__main__':main()
