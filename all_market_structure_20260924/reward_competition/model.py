"""Conditional public scoring model; no exchange/order/account client."""
from decimal import Decimal as D
import datetime as dt
SIDES=('yes','no')
CENT=D('.01')

def stamp(s):return dt.datetime.fromisoformat(s.replace('Z','+00:00')).timestamp()

def admitted(p,now):
    try:
        target=D(p['target_size_fp']);pool=D(p['period_reward'])/10000
        a=stamp(p['start_date']);b=stamp(p['end_date'])
        return not p.get('paid_out') and target>0 and pool>0 and a<=now<b and 0<b-a<=7200 and float(pool/2/target/CENT)/( (b-a)/3600)>=1
    except (KeyError,ValueError,TypeError,ZeroDivisionError):return False

def depth(book):
    out={}
    for side in SIDES:
        levels=book[side+'_dollars']
        if levels is None:raise ValueError('null side')
        out[side]=[(D(p),D(q),False) for p,q in levels if D(q)>0]
        if any(not CENT<=p<=D('.99') or p%CENT!=0 or q<0 for p,q in levels for p,q in [(D(p),D(q))]):raise ValueError('invalid cent-grid depth')
    return out

def score_side(orders,target,discount,mode='capped'):
    if not 0<=discount<=1 or target<=0:raise ValueError('invalid terms')
    rows=sorted(orders,key=lambda x:(-x[0],x[2])) # outsiders ahead at equal prices
    if sum((q for p,q,own in rows),D(0))<target:return None
    cumulative=D(0);reference=None;boundary=None
    for p,q,own in rows:
        cumulative+=q
        if reference is None and cumulative>=target/5:reference=p
        if boundary is None and cumulative>=target:boundary=p
    remaining=target;total=D(0);ours=D(0)
    for p,q,own in rows:
        if mode=='capped':eligible=min(q,max(D(0),remaining));remaining-=eligible
        elif mode=='whole_level':eligible=q if p>=boundary else D(0)
        else:raise ValueError(mode)
        ticks=max(0,int((reference-p)/CENT))
        weight=D(1) if ticks==0 else discount**ticks
        raw=eligible*weight;total+=raw
        if own:ours+=raw
    return {'own_share':float(ours/total),'reference':str(reference),'boundary':str(boundary),'own_raw':str(ours),'total_raw':str(total)}

def proposals(book,target,buffer_fraction=D(0)):
    result={};totals={s:sum((q for p,q,own in book[s]),D(0)) for s in SIDES}
    for s in SIDES:
        if totals[s]<target:result[s]=target-totals[s]+target*buffer_fraction
    if not result:return {},'both_meet'
    for s in result:
        other='no' if s=='yes' else 'yes'
        best=max([p for p,q,own in book[other]]+([CENT] if other in result else [D(0)]))
        if CENT+best>=1:return {},'one_cent_would_cross'
    return result,'resting_completion'

def scenario(book,target,discount,own,kind):
    orders={s:list(book[s])+([(CENT,own[s],True)] if s in own else []) for s in SIDES}
    details={};competitor_cost=D(0)
    for s in own:
        other='no' if s=='yes' else 'yes'
        opposite=max((p for p,q,o in orders[other]),default=D(0))
        if kind=='none':q=D(0);price=CENT
        elif kind.startswith('same_'):q=D(kind[5:]);price=CENT
        elif kind=='better_200':q=D(200);price=D('.02')
        elif kind=='highest_200':q=D(200);price=min(D('.99'),1-opposite-CENT)
        else:raise ValueError(kind)
        if price<CENT or price+opposite>=1:return {'kind':kind,'available':False}
        if q:orders[s].append((price,q,False))
        details[s]={'quantity':str(q),'price':str(price),'quantity_over_target':float(q/target)};competitor_cost+=q*price
    scores={}
    for mode in ('capped','whole_level'):
        scored={s:score_side(orders[s],target,discount,mode) for s in SIDES}
        if any(v is None for v in scored.values()):share=0
        else:share=sum(v['own_share'] for v in scored.values())/2
        scores[mode]={'overall_share':share,'sides':scored}
    return {'kind':kind,'available':True,'competitor_orders':details,'competitor_principal':float(competitor_cost),'scores':scores}

def analyze(t,p,m,b,ns):
    row={'ticker':t,'program':p,'book_received_ns':ns,'class':'unavailable'}
    if not m or b is None or ns is None:return row
    if m.get('status') not in ('active','open') or not stamp(p['start_date'])<=ns/1e9<min(stamp(p['end_date']),stamp(m['close_time'])):
        row['class']='outside_open_window';return row
    row.update(event_ticker=m.get('event_ticker'),title=m.get('title'),close_time=m['close_time'])
    ranges=m.get('price_ranges',[])
    if not (m.get('price_level_structure')=='linear_cent' and len(ranges)==1 and D(ranges[0]['start'])==0 and D(ranges[0]['end'])==1 and D(ranges[0]['step'])==CENT):
        row['class']='unsupported_grid';return row
    try:book=depth(b);target=D(p['target_size_fp']);discount=D(p['discount_factor_bps'])/10000
    except (KeyError,ValueError,TypeError):return row
    if not 0<=discount<=1:row['class']='invalid_discount';return row
    own,status=proposals(book,target);row['class']=status
    row['depth']={s:str(sum((q for _,q,_ in book[s]),D(0))) for s in SIDES}
    if not own:return row
    duration=(stamp(p['end_date'])-stamp(p['start_date']))/3600
    remaining=(min(stamp(p['end_date']),stamp(m['close_time']))-ns/1e9)/3600
    pool=p['period_reward']/10000
    row.update(pool_dollars=pool,duration_hours=duration,remaining_hours=remaining,short_sides=list(own),plans=[])
    for fraction in (D(0),D('.1')):
        qty,_=proposals(book,target,fraction);principal=float(sum(qty.values())*CENT)
        plan={'buffer_fraction':str(fraction),'quantity':{s:str(q) for s,q in qty.items()},'principal':principal,'fee_stress_reserve':float(sum(qty.values())/1000),'scenarios':[]}
        for kind in ('none','same_1','same_100','same_200','same_500','same_1000','better_200','highest_200'):
            case=scenario(book,target,discount,qty,kind)
            if case['available']:
                for mode,x in case['scores'].items():
                    rate=pool/duration*x['overall_share'];reward=rate*remaining
                    x.update(hourly_rate=rate,remaining_gross=reward,remaining_at_half_uptime=reward*.5,remaining_at_quarter_uptime=reward*.25,
                             full_principal_loss_break_even_minutes=principal/rate*60 if rate>0 else None,
                             half_uptime_covers_principal_and_stress=reward*.5>principal+plan['fee_stress_reserve'])
            plan['scenarios'].append(case)
        row['plans'].append(plan)
    return row
