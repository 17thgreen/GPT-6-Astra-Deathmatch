"""Run the frozen public-print sensitivity suite. Never sends orders."""
from pathlib import Path
from dataclasses import replace,asdict
from datetime import datetime,timezone
from concurrent.futures import ProcessPoolExecutor,as_completed
import argparse,csv,gzip,hashlib,json,sys,time
from replay_v2 import Replay,Config

ROOT=Path(__file__).resolve().parent


def load_capture():
    capture=json.loads((ROOT/'data/capture_manifest.json').read_text())
    if capture['failures'] or len(capture['games'])!=16:raise ValueError('Full frozen cohort is required')
    post=json.loads((ROOT/'data/postlude_manifest.json').read_text())
    if len(post['markets'])!=32:raise ValueError('Complete postlude required')
    games={g['event']:g for g in json.loads((ROOT/'data/cohort.json').read_text())}
    rows=[];markets={};ids=set();raw_rows=0
    for g in capture['games']:
        event=g['event'];j=json.loads((ROOT/'data'/event/'event.json').read_text());meta=j['event']
        ms=j.get('markets') or meta['markets'];tickers=sorted(m['ticker'] for m in ms)
        verified=meta.get('collateral_return_type')=='MECNET' and meta.get('mutually_exclusive') is True and len(ms)==2
        for m in ms:
            if m.get('price_level_structure')!='linear_cent':raise ValueError('Unmodeled price grid')
            if 'tie' not in m.get('rules_secondary','').lower() or '$0.50' not in m.get('rules_secondary',''):raise ValueError('Unverified tie rules')
            markets[m['ticker']]={'event':event,'direction':1 if m['ticker']==tickers[0] else -1,
                'kickoff':datetime.fromisoformat(games[event]['kickoff']).timestamp(),'verified_mecnet':verified}
    records=[m for g in capture['games'] for m in g['markets']]+post['markets']
    for item in records:
        p=ROOT/item['path']
        if not item['pagination_exhausted'] or hashlib.sha256(p.read_bytes()).hexdigest()!=item['sha256']:raise ValueError('Incomplete/corrupt capture')
        with gzip.open(p,'rt') as f:
            for line in f:
                t=json.loads(line);raw_rows+=1
                identity=t['trade_id']
                if identity in ids:continue
                ids.add(identity)
                if t.get('is_block_trade'):raise ValueError('Unexpected block trade')
                yes=float(t['yes_price_dollars']);no=float(t['no_price_dollars']);size=float(t['count_fp'])
                if abs(yes+no-1)>1e-6:raise ValueError('Non-complementary trade prices')
                if abs(size*100-round(size*100))>1e-5:raise ValueError('Unexpected quantity increment')
                rows.append({'at':datetime.fromisoformat(t['created_time'].replace('Z','+00:00')).timestamp(),
                             'ticker':t['ticker'],'taker_side':t['taker_side'],'yes_price':yes,'size':size,'trade_id':identity})
    rows.sort(key=lambda x:(x['at'],x['trade_id']))
    return rows,markets,{'raw_rows':raw_rows,'deduplicated_rows':len(rows),'games':16,'markets':32,
                         'start':datetime.fromtimestamp(rows[0]['at'],timezone.utc).isoformat(),'end':datetime.fromtimestamp(rows[-1]['at'],timezone.utc).isoformat(),
                         'tie_order':'trade_id lexical ordering for identical timestamps; receipt ordering unavailable'}


def run_one(name,config,rows,markets):
    start=time.monotonic();r=Replay(markets,config)
    for row in rows:r.on_trade(row)
    end=max(m['kickoff']-10800 for m in markets.values())+300
    summary=r.finish(end);summary['seconds']=time.monotonic()-start;summary['scenario']=name
    summary['maker_fills_at_or_after_cutoff']=sum(f['kind']=='maker' and f['at']>=markets[f['ticker']]['kickoff']-10800 for f in r.fills)
    (ROOT/'results'/f'{name}.json').write_text(json.dumps(summary,indent=2,allow_nan=False))
    with gzip.open(ROOT/'results'/f'{name}_fills.jsonl.gz','wt') as f:
        for row in r.fills:f.write(json.dumps(row,separators=(',',':'))+'\n')
    return summary


def legacy(rows,markets):
    import pandas as pd
    # Uses the previous audit's unchanged, pinned function-body loader; never modifies repository code.
    from legacy_loader import original_replay,MarketMakerPolicy,PolicyConfig
    tape=pd.DataFrame(rows);tape['created_time']=pd.to_datetime(tape['at'],unit='s',utc=True)
    tape['no_price']=1-tape.yes_price
    def queue(ticker,now):return 1327847.005 if markets[ticker]['kickoff']-now.timestamp()<43200 else 290.595
    policy=MarketMakerPolicy(PolicyConfig(order_size=250,max_event_exposure=250,flatten_seconds_before_close=10800,
                                        quote_from_seconds_before_start=604800))
    result=original_replay()(tape,policy,starting_cash=5000,queue_ahead=queue,fill_participation=.5,
                             requote_seconds=60,close_times={t:pd.Timestamp(m['kickoff'],unit='s',tz='UTC') for t,m in markets.items()},
                             require_close_time=True)
    out={'scenario':'legacy_exact_window','evidence':'UNCHANGED_REPOSITORY_ENGINE_ON_RECOVERED_COHORT',
         'config':result['config'],'result':result['result'],
         'comparison_note':'Bundle of changes: event loop, latency, reservations, fee rounding, stale proxy/exit controls. Not a single-bug ablation.'}
    fills=result['fills'];out['maker_fills_at_or_after_cutoff']=int(sum(row.kind=='maker' and row.at.timestamp()>=markets[row.ticker]['kickoff']-10800 for row in fills.itertuples()))
    (ROOT/'results/legacy_exact_window.json').write_text(json.dumps(out,indent=2,default=str))
    fills.to_csv(ROOT/'results/legacy_exact_window_fills.csv.gz',index=False)
    return out


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--legacy',action='store_true');args=parser.parse_args()
    rows,markets,data=load_capture();(ROOT/'results/data_summary.json').write_text(json.dumps(data,indent=2))
    print('INPUT',json.dumps(data),flush=True)
    base=Config()
    cases={'profile_fixed':base,'profile_reduce':replace(base,inventory_reduce_only=True),
           'queue3300_fixed':replace(base,queue_early=3300,queue_last12h=3300),
           'queue3300_reduce':replace(base,queue_early=3300,queue_last12h=3300,inventory_reduce_only=True),
           'thin_queue_optimistic':replace(base,queue_last12h=290.595),
           'profile_nondirect_precision':replace(base,balance_precision='.01'),
           'profile_exit_depth50':replace(base,assumed_exit_depth=50)}
    results={}
    with ProcessPoolExecutor(max_workers=3) as pool:
        futures={pool.submit(run_one,n,c,rows,markets):n for n,c in cases.items()}
        for future in as_completed(futures):
            name=futures[future];s=future.result();results[name]=s
            print(name,'pnl',s['completed_strategy_pnl'],'bounds',s['terminal_payout_bounds'],'unresolved',s['unresolved_contracts'],flush=True)
    if args.legacy:
        results['legacy_exact_window']=legacy(rows,markets)
        print('legacy_exact_window',results['legacy_exact_window']['result']['pnl'],flush=True)
    (ROOT/'results/suite_summary.json').write_text(json.dumps({'data':data,'scenarios':results},indent=2,allow_nan=False))


if __name__=='__main__':main()
