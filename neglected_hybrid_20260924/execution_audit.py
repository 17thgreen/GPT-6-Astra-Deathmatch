"""Post-score quote-persistence diagnostic; see EXECUTION_AUDIT_PLAN.md."""
import argparse,json,urllib.parse
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime,timezone
from acquire_v2 import get,BASE
from core import instant,fee,probability

def run(trades_path,raw,output):
    raw.mkdir(parents=True,exist_ok=True)
    signals=[r for r in json.loads(trades_path.read_text()) if r['arm']=='hybrid_50']
    def one(r):
        t=int(instant(r['decision']).timestamp())
        url=BASE+'/historical/markets/'+r['ticker']+'/candlesticks?'+urllib.parse.urlencode(
            {'start_ts':t,'end_ts':t+300,'period_interval':1})
        label=r['ticker']+'_'+str(t)
        x=get(url,raw,label)
        observations=[]
        for c in (x or {}).get('candlesticks',[]):
            dt=c['end_period_ts']-t
            if not 0<dt<=300:continue
            v=c.get('yes_ask' if r['side']=='yes' else 'yes_bid',{}).get('close')
            if v is None:continue
            v=probability(v);price=v if r['side']=='yes' else 1-v
            if not 0<price<1:continue
            observations.append({'delay_seconds':dt,'original_side_ask':price,
                'net_one_contract':r['payout']-price-fee(price)-.02,'bar_trade_volume':c.get('volume')})
        observations.sort(key=lambda r:r['delay_seconds'])
        return {'ticker':r['ticker'],'decision':r['decision'],'side':r['side'],
                'original_price':r['price'],'original_net':r['net'],'request_success':x is not None,
                'observations':observations,'one_minute':next((o for o in observations if o['delay_seconds']==60),None),
                'proves_fill':False,'source_url':url}
    with ThreadPoolExecutor(max_workers=6) as pool:rows=list(pool.map(one,signals))
    result={'classification':'POST_SCORE_QUOTE_PERSISTENCE_DIAGNOSTIC_NOT_EXECUTION',
            'created_at':datetime.now(timezone.utc).isoformat(),'rows':rows}
    output.write_text(json.dumps(result,indent=2)+'\n')
    for r in rows:print(json.dumps({k:v for k,v in r.items() if k not in ('observations','source_url')}))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('trades',type=Path);p.add_argument('raw',type=Path);p.add_argument('output',type=Path)
    a=p.parse_args();run(a.trades,a.raw,a.output)
