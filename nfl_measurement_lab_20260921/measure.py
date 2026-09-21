"""Snapshot observables, censored shadow service and markouts; no P&L model."""
import bisect
import json
import math
import statistics
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
GAP = 30.0


def available(row):
    return max(row['received_at'], row.get('recorded_at', row['received_at']))


def best(body, side):
    levels = body.get('orderbook_fp', {}).get(side+'_dollars', [])
    clean = [(float(p),float(q)) for p,q in levels]
    if any(not math.isfinite(p+q) or not 0 <= p <= 1 or q < 0 for p,q in clean):
        raise ValueError('Invalid depth')
    return max((x for x in clean if x[1] > 0), default=None, key=lambda x:x[0])


def normalize(rows):
    books = defaultdict(list); trades = {}; pagegroups=defaultdict(dict); errors=[]
    for row in rows:
        if row['kind']=='error':
            errors.append(row);continue
        if row['kind']=='book':
            y=best(row['body'],'yes');n=best(row['body'],'no')
            valid=bool(y and n and 0<y[0]<1 and 0<n[0]<1 and y[0]+n[0]<=1+1e-9)
            books[row['ticker']].append(dict(at=available(row),request_at=row['request_at'],
                received_at=row['received_at'],yes=y,no=n,valid=valid,
                mid=(y[0]+1-n[0])/2 if valid else None))
        if row['kind']=='trades':
            params=row['params'];key=(row['ticker'],params['min_ts'],params['max_ts'],row.get('poll',-1))
            pagegroups[key][row.get('page',0)]=row
            for t in row['body']['trades']:
                if t.get('is_block_trade'):continue
                if t.get('taker_side') not in ('yes','no'):
                    raise ValueError('Unrecognized taker-side semantics; cannot infer resting side')
                y=float(t['yes_price_dollars']);n=float(t['no_price_dollars']);size=float(t['count_fp'])
                if not math.isfinite(y+n+size) or abs(y+n-1)>1e-6 or size<=0:
                    raise ValueError('Invalid trade')
                outcome='no' if t['taker_side']=='yes' else 'yes'
                at=datetime.fromisoformat(t['created_time'].replace('Z','+00:00')).timestamp()
                v=dict(id=t['trade_id'],ticker=t['ticker'],outcome=outcome,price=y if outcome=='yes' else n,
                       size=size,at=at,known_at=available(row))
                if v['id'] in trades:
                    old=trades[v['id']]
                    if {k:v[k] for k in v if k!='known_at'}!={k:old[k] for k in old if k!='known_at'}:
                        raise ValueError('Conflicting duplicate trade')
                    old['known_at']=min(old['known_at'],v['known_at'])
                else:trades[v['id']]=v
    coverage=defaultdict(list)
    for (ticker,start,end,poll),pages in pagegroups.items():
        last=max(pages)
        if set(pages)==set(range(last+1)) and not pages[last]['body'].get('cursor'):
            coverage[ticker].append((start,end))
    for ticker,spans in coverage.items():
        merged=[]
        for a,b in sorted(spans):
            if merged and a<=merged[-1][1]:merged[-1]=(merged[-1][0],max(b,merged[-1][1]))
            else:merged.append((a,b))
        coverage[ticker]=merged
    for value in books.values():value.sort(key=lambda b:b['at'])
    return books,sorted(trades.values(),key=lambda t:(t['at'],t['id'])),coverage,errors


def matching(trades,ticker,side,price,start,end,known_before=None):
    return [t for t in trades if t['ticker']==ticker and t['outcome']==side and abs(t['price']-price)<1e-8
            and start<t['at']<=end and (known_before is None or t['known_at']<known_before and t['at']<known_before)]


def spans_cover(spans,start,end):
    return any(a<=start and b>=end for a,b in spans)


def service(rows,depth,size=250,participation=.5):
    cumulative=0.;first=None;full=None;filled=0.
    for t in rows:
        cumulative+=t['size'];filled=min(size,max(0,cumulative-depth)*participation)
        if filled>0 and first is None:first=t['at']
        if filled>=size and full is None:full=t['at']
    return dict(exact_price_volume=cumulative,serviced_contracts=filled,first_service_at=first,full_service_at=full)


def outcome_mid(book,side):
    return book['mid'] if side=='yes' else 1-book['mid']


def markout(obs,at,side,price,horizon):
    times=[b['at'] for b in obs];start=bisect.bisect_right(times,at)-1
    target=at+horizon;end=bisect.bisect_left(times,target)
    if start<0 or end>=len(obs):return None
    if at-times[start]>GAP or times[end]-target>GAP:return None
    selected=obs[start:end+1]
    if any(not b['valid'] for b in selected) or any(b['at']-a['at']>GAP for a,b in zip(selected,selected[1:])):return None
    mid=outcome_mid(obs[end],side);initial=outcome_mid(obs[start],side)
    return dict(horizon_seconds=horizon,observed_at=times[end],target_lateness=times[end]-target,
                midpoint_change_cents=100*(mid-initial),midpoint_less_fill_cents=100*(mid-price))


def analyze(rows):
    books,trades,coverage,errors=normalize(rows)
    spells=[];features=[];labels=[];depth_changes=[]
    for ticker,obs in books.items():
        for side in ('yes','no'):
            spell=None;join=None;previous=None
            def finish_spell(reason,upper=None):
                if spell is not None:
                    spells.append(dict(**spell,end_reason=reason,observed_duration=spell['last_at']-spell['start_at'],
                        change_interval_upper=upper,right_censored=reason!='price_change'))
            def finish_join(reason,end):
                if join is None:return
                prints=matching(trades,ticker,side,join['price'],join['arrival_at'],end)
                result=service(prints,join['displayed_depth'])
                complete=end>=join['arrival_at'] and spans_cover(coverage[ticker],join['arrival_at'],end)
                marks=[]
                if result['first_service_at'] is not None:
                    marks=[m for h in (30,60,300) if (m:=markout(obs,result['first_service_at'],side,join['price'],h)) is not None]
                labels.append(dict(join_id=join['join_id'],end_at=end,end_reason=reason,
                    duration=max(0,end-join['arrival_at']),tape_interval_complete=complete,
                    horizon_observed=reason=='horizon',censored_before_full=result['full_service_at'] is None and reason!='horizon',
                    **result,markouts=marks))
            for row in obs:
                gap=previous is not None and row['at']-previous['at']>GAP
                invalid=not row['valid']
                price=row[side][0] if row['valid'] else None
                changed=spell is not None and price!=spell['price']
                reason='gap' if gap else 'invalid_book' if invalid else 'price_change'
                if spell is not None and (gap or invalid or changed):
                    finish_spell(reason,row['at'] if reason=='price_change' else None);spell=None
                if join is not None and (gap or invalid or price!=join['price']):
                    finish_join(reason,previous['at']);join=None
                if row['valid']:
                    if spell is None:
                        spell=dict(ticker=ticker,outcome=side,price=price,start_at=row['at'],last_at=row['at'],
                            left_censored=previous is None or gap or not previous['valid'])
                    else:spell['last_at']=row['at']
                    if join is not None and row['at']>=join['decision_at']+600:
                        finish_join('horizon',join['decision_at']+600);join=None
                    if join is None:
                        prior=matching(trades,ticker,side,price,row['at']-3600,row['at'],row['at'])
                        volume=sum(t['size'] for t in prior);depth=row[side][1]
                        join=dict(join_id=f'{ticker}/{side}/{len(features)}',ticker=ticker,outcome=side,
                            decision_at=row['at'],arrival_at=row['at']+.25,price=price,displayed_depth=depth,
                            prior_hour_received_volume=volume,ten_minute_projected_capacity=max(0,volume/6-depth)*.5,
                            feature_latest_trade_known_at=max((t['known_at'] for t in prior),default=None))
                        features.append(join)
                    if previous and previous['valid'] and not gap and previous[side][0]==price:
                        printed=sum(t['size'] for t in matching(trades,ticker,side,price,previous['at'],row['at']))
                        old_depth=previous[side][1];new_depth=row[side][1]
                        depth_changes.append(dict(ticker=ticker,outcome=side,start_at=previous['at'],end_at=row['at'],
                            prior_depth=old_depth,new_depth=new_depth,exact_price_printed=printed,
                            decline_unexplained_by_prints=max(0,old_depth-new_depth-printed)))
                previous=row
            finish_spell('capture_end')
            if join is not None:finish_join('capture_end',previous['at'])
    allbooks=[b for obs in books.values() for b in obs];lat=[b['received_at']-b['request_at'] for b in allbooks]
    gaps=[b['at']-a['at'] for obs in books.values() for a,b in zip(obs,obs[1:])]
    goodlabels=[l for l in labels if l['tape_interval_complete']]
    queues=[f['displayed_depth'] for f in features]
    med=lambda x:statistics.median(x) if x else None
    marks=[m for l in goodlabels for m in l['markouts']]
    summary=dict(evidence='PUBLIC_OBSERVABLES_AND_CONDITIONAL_SHADOW_SERVICE_NOT_EXECUTED_PNL',
        markets=len(books),book_snapshots=len(allbooks),valid_books=sum(b['valid'] for b in allbooks),
        first_book=min((b['at'] for b in allbooks),default=None),last_book=max((b['at'] for b in allbooks),default=None),
        deduplicated_trades=len(trades),errors=len(errors),
        median_http_seconds=med(lat),p95_http_seconds=sorted(lat)[int(.95*(len(lat)-1))] if lat else None,
        median_observation_gap=med(gaps),max_observation_gap=max(gaps,default=None),
        quote_spells=len(spells),spell_end_reasons=dict(Counter(s['end_reason'] for s in spells)),
        median_observed_spell_seconds=med([s['observed_duration'] for s in spells]),
        left_censored_spells=sum(s['left_censored'] for s in spells),right_censored_spells=sum(s['right_censored'] for s in spells),
        shadow_joins=len(labels),tape_complete_joins=len(goodlabels),
        full_horizon_observed=sum(l['horizon_observed'] for l in goodlabels),
        censored_before_full=sum(l['censored_before_full'] for l in goodlabels),
        any_service_joins=sum(l['serviced_contracts']>0 for l in goodlabels),
        full_service_joins=sum(l['serviced_contracts']>=250 for l in goodlabels),
        join_end_reasons=dict(Counter(l['end_reason'] for l in labels)),
        median_join_depth=med(queues),min_join_depth=min(queues,default=None),max_join_depth=max(queues,default=None),
        joins_above_3300=sum(q>3300 for q in queues),
        depth_intervals=len(depth_changes),intervals_with_unexplained_decline=sum(d['decline_unexplained_by_prints']>1e-7 for d in depth_changes),
        shadow_markouts={str(h):dict(n=len(a:=[m for m in marks if m['horizon_seconds']==h]),
            mean_midpoint_change_cents=statistics.mean(m['midpoint_change_cents'] for m in a) if a else None,
            mean_midpoint_less_fill_cents=statistics.mean(m['midpoint_less_fill_cents'] for m in a) if a else None) for h in (30,60,300)},
        limitations=['Snapshots do not reveal order identity, actual own-queue advancement or unobserved price changes.',
            'Spell durations are censored observations, not estimates of individual-order lifetime.',
            'Shadow fills assume initial depth, no cancellations, arrival delay, exact-price allocation and half participation.',
            'Coverage means cursor exhaustion, not a guarantee against later trade publication.',
            'No service/markout row is an actual own-order fill; overlapping game and outcome risks are correlated.'])
    return summary,features,labels,spells,depth_changes


def main():
    for label,path in [('q1_development',ROOT/'inputs/q1_forward_observations.jsonl'),('q3_development',ROOT/'forward/observations.jsonl')]:
        rows=[json.loads(line) for line in path.read_text().splitlines()]
        result=analyze(rows)
        for suffix,value in zip(['summary','features','labels','spells','depth_changes'],result):
            (ROOT/'results'/f'{label}_{suffix}.json').write_text(json.dumps(value,indent=2,allow_nan=False))
        print(json.dumps(dict(panel=label,**result[0]),indent=2))


if __name__=='__main__':main()
