"""Public book measurements and overlapping hypothetical join diagnostics, never P&L."""
import bisect,json,statistics
from collections import defaultdict,Counter
from datetime import datetime
from pathlib import Path

ROOT=Path(__file__).resolve().parent

def best(row,outcome):
    levels=row['body'].get('orderbook_fp',{}).get(outcome+'_dollars',[])
    if not levels:return None
    p,q=map(float,levels[-1])
    if not 0<p<1 or q<0:raise ValueError('Invalid book level')
    return p,q

def availability(row):return max(row['received_at'],row.get('recorded_at',row['received_at']))

def normalize(rows):
    trades={};bookrows=[];through={};events={};errors=[]
    for row in rows:
        if row['kind']=='book':bookrows.append(row)
        elif row['kind']=='metadata':
            meta=row['body'];event=meta['event'];ms=meta.get('markets') or event.get('markets',[])
            if (len(ms)!=2 or not event.get('mutually_exclusive') or event.get('collateral_return_type')!='MECNET'
                or any(m.get('price_level_structure')!='linear_cent' or '$0.50' not in m.get('rules_secondary','') for m in ms)):
                raise ValueError('Unverified paired market')
            events[event['event_ticker']]=sorted(m['ticker'] for m in ms)
        elif row['kind']=='trades':
            if not row['body'].get('cursor'):through[row['ticker']]=max(through.get(row['ticker'],0),row['params']['max_ts'])
            for t in row['body']['trades']:
                if t.get('is_block_trade'):continue
                side='no' if t['taker_side']=='yes' else 'yes'
                px=float(t['yes_price_dollars']) if side=='yes' else float(t['no_price_dollars'])
                record=dict(ticker=t['ticker'],outcome=side,price=px,size=float(t['count_fp']),
                    at=datetime.fromisoformat(t['created_time'].replace('Z','+00:00')).timestamp(),known_at=availability(row))
                if t['trade_id'] in trades:
                    old=trades[t['trade_id']]
                    if any(old[k]!=record[k] for k in ['ticker','outcome','price','size','at']):raise ValueError('Conflicting trade identity')
                    old['known_at']=min(old['known_at'],record['known_at'])
                else:trades[t['trade_id']]=record
        elif row['kind']=='error':errors.append(row)
    return sorted(bookrows,key=availability),list(trades.values()),through,events,errors

def eligible_volume(trades,ticker,outcome,price,start,end,known_before=None):
    return sum(t['size'] for t in trades if t['ticker']==ticker and t['outcome']==outcome
               and start<=t['at']<end and t['price']<=price+1e-9
               and (known_before is None or t['known_at']<=known_before))

def analyze(rows):
    bookrows,trades,through,events,errors=normalize(rows)
    by_ticker=defaultdict(list)
    for r in bookrows:by_ticker[r['ticker']].append(r)
    summaries=[];joins=[]
    for ticker,observations in sorted(by_ticker.items()):
        for outcome in ('yes','no'):
            values=[];waits=[];zero_flow=0
            for i,row in enumerate(observations):
                pair=best(row,outcome)
                if pair is None:continue
                p,q=pair;now=availability(row);values.append(q)
                volume=eligible_volume(trades,ticker,outcome,p,now-3600,now,now)
                if volume>0:waits.append(q/(volume/3600)/60)
                else:zero_flow+=1
                end=min(now+600,through.get(ticker,now));reason='ten_minute_cap' if end==now+600 else 'coverage_end'
                previous=now
                for later in observations[i+1:]:
                    at=availability(later)
                    if at>end:break
                    if at-previous>30:
                        end=previous;reason='observation_gap';break
                    if best(later,outcome) is None or abs(best(later,outcome)[0]-p)>1e-9:
                        end=at;reason='observed_price_change';break
                    previous=at
                if end>now:
                    flow=eligible_volume(trades,ticker,outcome,p,now,end)
                    service=max(0,(flow-q)*.5)
                    joins.append(dict(ticker=ticker,outcome=outcome,at=now,price=p,initial_queue=q,
                        observed_seconds=end-now,qualifying_volume=flow,
                        hypothetical_serviced_contracts=min(250,service),end_reason=reason))
            depths=sorted(values)
            summaries.append(dict(ticker=ticker,outcome=outcome,observations=len(values),
                queue_min=min(values),queue_median=statistics.median(values),queue_max=max(values),
                queue_above_3300_fraction=sum(q>3300 for q in values)/len(values),
                median_implied_queue_wait_minutes=statistics.median(waits) if waits else None,
                zero_known_eligible_flow_observations=zero_flow,
                wait_note='Queue divided by previously received eligible trailing-hour flow; steady-flow heuristic, not expected execution time.'))
    latency=sorted(r['received_at']-r['request_at'] for r in bookrows)
    spreads=[];gaps=[]
    for obs in by_ticker.values():
        gaps.extend(availability(b)-availability(a) for a,b in zip(obs,obs[1:]))
        for r in obs:
            y=best(r,'yes');n=best(r,'no')
            if y and n:spreads.append(1-y[0]-n[0])
    # Evaluate both verified payoff directions from recently received books.
    mapping={t:(e,1 if i==0 else -1) for e,ts in events.items() for i,t in enumerate(ts)}
    latest={};routes=[]
    for row in bookrows:
        now=availability(row);ticker=row['ticker'];latest[ticker]=row
        event,_=mapping[ticker];ts=events[event]
        if any(t not in latest or now-availability(latest[t])>30 for t in ts):continue
        candidates=[]
        for t in ts:
            for outcome in ('yes','no'):
                level=best(latest[t],outcome)
                if level is None:continue
                price,q=level
                rate=eligible_volume(trades,t,outcome,price,now-3600,now,now)/3600
                candidates.append(dict(ticker=t,outcome=outcome,direction=mapping[t][1]*(1 if outcome=='yes' else -1),
                    price=price,queue=q,flow_per_minute=rate*60,cost=price+.0175*price*(1-price),
                    service=min(1,rate*600/(q+500))))
        for direction in (-1,1):
            same=[c for c in candidates if c['direction']==direction];opposite=[c for c in candidates if c['direction']==-direction]
            if not same or not opposite:continue
            for c in same:
                c['pair_margin']=1-c['cost']-min(o['cost'] for o in opposite)
                c['score']=max(0,c['pair_margin'])*c['service']
            winner=min(same,key=lambda c:(-c['score'],c['cost'],c['ticker'],c['outcome']))
            routes.append(dict(at=now,event=event,direction=direction,selected=winner,
                alternatives=same,note='Fresh-join shadow ranking; no own queue, no incumbent or actual order.'))
    out=dict(evidence='BOUNDED_PUBLIC_REST_MEASUREMENTS_NOT_STRATEGY_EXECUTION',
        book_snapshots=len(bookrows),deduplicated_public_trades=len(trades),errors=errors,
        first_book_received=min(availability(r) for r in bookrows),last_book_received=max(availability(r) for r in bookrows),
        median_request_seconds=statistics.median(latency),p95_request_seconds=latency[int(.95*(len(latency)-1))],
        median_per_ticker_observation_gap_seconds=statistics.median(gaps),max_per_ticker_observation_gap_seconds=max(gaps),
        spreads_two_or_more_ticks=sum(s>=.02-1e-9 for s in spreads),spread_observations=len(spreads),
        legs=summaries,hypothetical_joins=len(joins),joins_with_any_service=sum(j['hypothetical_serviced_contracts']>0 for j in joins),
        joins_with_full_250_service=sum(j['hypothetical_serviced_contracts']>=250 for j in joins),
        join_end_reasons=dict(Counter(j['end_reason'] for j in joins)),shadow_route_decisions=len(routes),
        shadow_selected_counts=dict(Counter(r['selected']['ticker']+'/'+r['selected']['outcome'] for r in routes)),
        restrictions=['Overlapping snapshots are not independent opportunities.',
          'Hypothetical join ignores cancellations ahead; transient price changes between snapshots and arrival-time queue are unknown.',
          'Recorded quotes are current observations, never historical queue replacements.',
          'Short-window service and steady-flow ratios do not validate fill probabilities or P&L.',
          'Workspace/proxy end-to-end latency is not a measurement of exchange matching-engine latency.'])
    return out,joins,routes

def main():
    rows=[json.loads(line) for line in (ROOT/'forward/observations.jsonl').read_text().splitlines()]
    out,joins,routes=analyze(rows)
    for name,value in [('forward_analysis',out),('forward_hypothetical_joins',joins),('forward_shadow_routes',routes)]:
        (ROOT/'results'/f'{name}.json').write_text(json.dumps(value,indent=2,allow_nan=False))
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
