"""GET-only snapshots for rule/fee discovery; never places orders."""
import json,urllib.request,urllib.parse,datetime,concurrent.futures
from pathlib import Path
BASE='https://api.elections.kalshi.com/trade-api/v2'
SERIES=['KXNFLGAME','KXNBAGAME','KXWNBAGAME','KXNHLGAME','KXMLBGAME','KXNCAAFGAME','KXNCAAMBGAME','KXATPMATCH','KXWTAMATCH','KXUCLGAME','KXNFLSPREAD','KXNFLTOTAL']

def get(path):
    with urllib.request.urlopen(BASE+path,timeout=25) as f:return json.load(f)

def inspect(ticker):
    result=dict(series_ticker=ticker,retrieved_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
    try:
        s=get('/series/'+ticker)['series']
        result['series']={k:s.get(k) for k in ['ticker','title','fee_type','fee_multiplier','contract_terms_url','contract_url','frequency','settlement_sources','last_updated_ts']}
        ms=get('/markets?'+urllib.parse.urlencode(dict(series_ticker=ticker,limit=1)))['markets']
        if ms:
            m=ms[0];result['sample_market']={k:m.get(k) for k in ['ticker','event_ticker','status','rules_primary','rules_secondary','price_level_structure','price_ranges','notional_value_dollars','open_time','close_time','expected_expiration_time']}
            e=get('/events/'+m['event_ticker'])
            result['sample_event']={k:e['event'].get(k) for k in ['event_ticker','title','mutually_exclusive','collateral_return_type','fee_type_override','fee_multiplier_override']}
            result['sample_event']['markets']=[{k:m.get(k) for k in ['ticker','title','yes_sub_title','rules_primary','rules_secondary']} for m in e.get('markets',e['event'].get('markets',[]))]
    except Exception as e:result['error']=str(e)
    return result

if __name__=='__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:results=list(pool.map(inspect,SERIES))
    Path(__file__).with_name('SERIES_SNAPSHOT.json').write_text(json.dumps(dict(base_url=BASE,discovery_only=True,series=results),indent=2))
    for r in results:print(r['series_ticker'],r.get('series',{}).get('fee_type'),r.get('sample_event',{}).get('collateral_return_type'),len(r.get('sample_event',{}).get('markets',[])),r.get('error',''))
