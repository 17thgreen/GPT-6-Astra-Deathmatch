"""Predeclared quote-source comparison; candle closes become available after 60 seconds."""
from dataclasses import replace
from concurrent.futures import ProcessPoolExecutor,as_completed
import gzip,hashlib,json,time
from run_suite import ROOT,load_capture
from replay_v2 import Replay,Config


def load_quotes():
    manifest=json.loads((ROOT/'data/candle_manifest.json').read_text());quotes=[];missing=0;nulls=0
    if len(manifest['markets'])!=32:raise ValueError('Incomplete candle cohort')
    for record in manifest['markets']:
        file=ROOT/record['path'];missing+=len(record['missing_minutes'])
        if hashlib.sha256(file.read_bytes()).hexdigest()!=record['sha256']:raise ValueError('Candle hash')
        with gzip.open(file,'rt') as f:
            for line in f:
                c=json.loads(line);bid=c.get('yes_bid',{}).get('close_dollars');ask=c.get('yes_ask',{}).get('close_dollars')
                if bid is None or ask is None:nulls+=1;continue
                quotes.append(dict(at=c['end_period_ts']+60,asof=c['end_period_ts'],ticker=record['ticker'],bid=float(bid),ask=float(ask),kind='quote'))
    return quotes,{'quote_records':len(quotes),'missing_minutes':missing,'null_bid_or_ask':nulls,'assumed_publication_delay_seconds':60}


def run_one(name,config,events,markets):
    r=Replay(markets,config);start=time.monotonic()
    end=max(m['kickoff']-10800 for m in markets.values())+300
    for row in events:
        if row['at']>end:break
        if row.get('kind')=='quote':r.on_quote(row)
        else:r.on_trade(row)
    s=r.finish(end);s['scenario']=name;s['seconds']=time.monotonic()-start
    s['evidence']='EXPLORATORY_MINUTE_BID_ASK_REPLAY_DEPTH_AND_RECEIPT_LATENCY_UNOBSERVED'
    s['maker_fills_at_or_after_cutoff']=sum(f['kind']=='maker' and f['at']>=markets[f['ticker']]['kickoff']-10800 for f in r.fills)
    (ROOT/'results'/f'{name}.json').write_text(json.dumps(s,indent=2,allow_nan=False))
    with gzip.open(ROOT/'results'/f'{name}_fills.jsonl.gz','wt') as f:
        for row in r.fills:f.write(json.dumps(row,separators=(',',':'))+'\n')
    return s


def main():
    rows,markets,trade_meta=load_capture();quotes,quote_meta=load_quotes()
    events=rows+quotes
    # Deterministic convention: published quotes before trades at an identical time. No intraminute highs/lows used.
    events.sort(key=lambda r:(r['at'],0 if r.get('kind')=='quote' else 1,r.get('trade_id',r['ticker'])))
    cases={'candles_profile_fixed':replace(Config(),quote_source='candles'),
           'candles_profile_reduce':replace(Config(),quote_source='candles',inventory_reduce_only=True)}
    result={'trade_data':trade_meta,'quote_data':quote_meta,'scenarios':{}}
    with ProcessPoolExecutor(max_workers=2) as pool:
        jobs={pool.submit(run_one,n,c,events,markets):n for n,c in cases.items()}
        for task in as_completed(jobs):
            name=jobs[task];s=task.result();result['scenarios'][name]=s
            print(name,'pnl',s['completed_strategy_pnl'],'bounds',s['terminal_payout_bounds'],'unresolved',s['unresolved_contracts'],flush=True)
    (ROOT/'results/candle_suite_summary.json').write_text(json.dumps(result,indent=2,allow_nan=False))


if __name__=='__main__':main()
