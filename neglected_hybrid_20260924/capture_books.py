"""Bounded, unauthenticated GET-only recorder. Never places or recommends orders."""
from decimal import Decimal
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,json,re
from acquire_v2 import get,BASE

def book_summary(data):
    # Refuse old integer-cent schema rather than guess units.
    ob=data['orderbook_fp'];sides={}
    for side in ('yes','no'):
        levels=[]
        for rawp,rawq in ob[side+'_dollars']:
            p,q=Decimal(str(rawp)),Decimal(str(rawq))
            if not p.is_finite() or not q.is_finite() or not 0<p<1 or q<0:
                raise ValueError('Invalid price or quantity')
            if q>0:levels.append((p,q))
        if not levels:raise ValueError('Missing positive depth on a side')
        prices=[p for p,q in levels]
        if len(set(prices))!=len(prices):raise ValueError('Duplicate price levels')
        sides[side]=max(levels,key=lambda x:x[0])
    yb,yq=sides['yes'];nb,nq=sides['no'];ya=1-nb
    if yb>ya:raise ValueError('Crossed book')
    return {'yes_bid':str(yb),'yes_ask':str(ya),'no_bid':str(nb),'no_ask':str(1-yb),
            'yes_ask_visible_quantity':str(nq),'no_ask_visible_quantity':str(yq),
            'spread':str(ya-yb),'quantity_is_not_a_fill':True}

def capture(tickers,root):
    if not tickers or len(tickers)>25 or len(set(tickers))!=len(tickers):
        raise ValueError('Require 1-25 distinct explicit tickers')
    if any(not re.fullmatch(r'[A-Z0-9-]+',t) for t in tickers):raise ValueError('Invalid ticker')
    # Exclusive run directory makes repeat calls new observations, never stale cache.
    root.mkdir(parents=True,exist_ok=False);rows=[]
    for ticker in tickers:
        meta=get(BASE+'/markets/'+ticker,root,ticker+'_market')
        data=get(BASE+'/markets/'+ticker+'/orderbook?depth=100',root,ticker+'_book')
        r={'ticker':ticker,'mode':'OBSERVATION_ONLY','exchange_timestamp_available':False}
        try:
            market=(meta or {})['market']
            if market['status'] not in ('active','open'):raise ValueError('Market not open')
            r['book']=book_summary(data)
            r['rules_sha256']=hashlib.sha256((market.get('rules_primary','')+'\n'+market.get('rules_secondary','')).encode()).hexdigest()
            receipt=json.loads((root/(ticker+'_book.receipt.json')).read_text())
            r['received_at']=receipt['received_at'];r['request_started_at']=receipt['started_at']
            r['book_body_sha256']=receipt['sha256'];r['admitted_book']=True
        except (KeyError,TypeError,ValueError) as e:r.update(admitted_book=False,reason=str(e))
        rows.append(r)
    output={'created_at':datetime.now(timezone.utc).isoformat(),'live_trading':False,
            'forecast_admitted':False,'signals':[], 'reason':'Recorder has no forecast or fee admission and no order capability.',
            'rows':rows}
    (root/'summary.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(output,indent=2));return output

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('output_directory',type=Path);p.add_argument('tickers',nargs='+')
    a=p.parse_args();capture(a.tickers,a.output_directory)
