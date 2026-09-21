"""Diagnostic comparison at candle end, not a trading signal or available-at-time assertion."""
from collections import defaultdict
import gzip,json,math
from run_suite import ROOT,load_capture


def main():
    rows,markets,_=load_capture();by=defaultdict(list)
    for row in rows:by[row['ticker']].append(row)
    manifest=json.loads((ROOT/'data/candle_manifest.json').read_text());stats=defaultdict(float);by_market=[]
    for record in manifest['markets']:
        ticker=record['ticker'];trades=by[ticker];i=0;proxy={};s=defaultdict(float)
        with gzip.open(ROOT/record['path'],'rt') as f:
            for line in f:
                c=json.loads(line);at=c['end_period_ts']
                if at>markets[ticker]['kickoff']-10800:continue
                while i<len(trades) and trades[i]['at']<=at:
                    row=trades[i];key='ask' if row['taker_side']=='yes' else 'bid'
                    proxy[key]=row['yes_price'];proxy[key+'_at']=row['at'];i+=1
                bid=c.get('yes_bid',{}).get('close_dollars');ask=c.get('yes_ask',{}).get('close_dollars')
                if bid is None or ask is None:continue
                bid=float(bid);ask=float(ask)
                if not 0<bid<ask<1:continue
                s['valid_candle_quotes']+=1
                if not all(k in proxy for k in ('bid','ask')):s['missing_print_side']+=1;continue
                s['comparable']+=1
                if proxy['ask']<=proxy['bid']:s['crossed_or_locked_print_proxy']+=1
                if abs(proxy['bid']-bid)>.00001 or abs(proxy['ask']-ask)>.00001:s['different_price_pair']+=1
                if at-min(proxy['bid_at'],proxy['ask_at'])>=300:s['at_least_one_print_side_older_than_5m']+=1
                if proxy['ask']-proxy['bid']>ask-bid+.00001:s['print_proxy_wider_than_candle_spread']+=1
                s['absolute_bid_error_cents_sum']+=100*abs(proxy['bid']-bid)
                s['absolute_ask_error_cents_sum']+=100*abs(proxy['ask']-ask)
        by_market.append({'ticker':ticker,**dict(s)})
        for k,v in s.items():stats[k]+=v
    n=stats['comparable'];rates={k:v/n for k,v in stats.items() if k not in ('valid_candle_quotes','missing_print_side','comparable')}
    out={'purpose':'Measure print-proxy disagreement with historical minute-end quotes. Endpoint closes are used ex post here, never as same-minute trading inputs.',
         'counts':dict(stats),'per_comparable_observation':rates,'markets':by_market,
         'inference_limit':'Repeated minutes are correlated. Disagreement is a source diagnostic, not proof of an executable trade.'}
    (ROOT/'results/quote_source_audit.json').write_text(json.dumps(out,indent=2))
    print(json.dumps({'counts':dict(stats),'rates':rates},indent=2))


if __name__=='__main__':main()
