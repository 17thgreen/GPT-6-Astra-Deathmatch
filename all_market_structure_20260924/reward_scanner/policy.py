"""Read-only candidate scoring. No order instructions are sent to any venue."""
from decimal import Decimal as D,ROUND_FLOOR
import importlib.util
from pathlib import Path
BASE_MODEL=Path(__file__).resolve().parents[1]/'reward_competition/model.py'
_spec=importlib.util.spec_from_file_location('ams009_model',BASE_MODEL)
old=importlib.util.module_from_spec(_spec);_spec.loader.exec_module(old)
stamp=old.stamp;SIDES=old.SIDES;CENT=D('.01')

def admission(p,start,now,new=True):
    return old.admitted(p,now) and stamp(p['start_date'])>=start and (not new or now-stamp(p['start_date'])<=300)

def payable(gross):
    rounded=D(str(gross)).quantize(CENT,rounding=ROUND_FLOOR)
    return rounded if rounded>=1 else D(0)

def public_crossed(book):
    best=[max((p for p,q,o in book[s]),default=D(0)) for s in SIDES]
    return all(best) and sum(best)>=1

def stressed(book,target,discount,own,consume=D(0)):
    b={s:list(book[s]) for s in SIDES};removed={}
    for s in own:
        other='no' if s=='yes' else 'yes'
        if other in removed:continue
        if not b[other]:removed[other]={'price':None,'quantity':'0'};continue
        top=max(p for p,q,o in b[other]);qty=sum(q for p,q,o in b[other] if p==top)
        b[other]=[(p,q,o) for p,q,o in b[other] if p<top];removed[other]={'price':str(top),'quantity':str(qty)}
    for s,q in own.items():
        if q-consume>0:b[s].append((CENT,q-consume,True))
    rivals={}
    for s in own:
        other='no' if s=='yes' else 'yes';best=max((p for p,q,o in b[other]),default=D(0))
        price=D('.02') if D('.02')+best<1 else CENT
        if price+best>=1:return {'available':False,'reason':'rival_cannot_rest'}
        q=target/5;b[s].append((price,q,False));rivals[s]={'quantity':str(q),'price':str(price)}
    if public_crossed(b):return {'available':False,'reason':'stressed_book_crossed'}
    scores={}
    for mode in ('capped','whole_level'):
        detail={s:old.score_side(b[s],target,discount,mode) for s in SIDES}
        qualified=all(x is not None for x in detail.values())
        share=sum(x['own_share'] for x in detail.values())/2 if qualified else 0
        scores[mode]={'qualified':qualified,'overall_share':share,'sides':detail}
    return {'available':True,'removed_levels':removed,'rivals':rivals,'assumed_own_quantity_consumed_per_side':str(consume),'scores':scores}

def evaluate(t,p,m,raw,ns):
    r={'ticker':t,'program':p,'book_received_ns':ns,'class':'unavailable','buffered_alert':False}
    if m is None or raw is None or ns is None:return r
    if 'max_reward_per_account' in p and p['max_reward_per_account'] is not None:r['class']='account_cap_unhandled';return r
    if m.get('status') not in ('open','active') or not stamp(p['start_date'])<=ns/1e9<min(stamp(p['end_date']),stamp(m['close_time'])):
        r['class']='outside_open_window';return r
    ranges=m.get('price_ranges',[])
    if not(m.get('price_level_structure')=='linear_cent' and len(ranges)==1 and D(ranges[0]['start'])==0 and D(ranges[0]['end'])==1 and D(ranges[0]['step'])==CENT):r['class']='unsupported_grid';return r
    try:b=old.depth(raw);target=D(p['target_size_fp']);discount=D(p['discount_factor_bps'])/10000
    except (KeyError,ValueError,TypeError):return r
    if not 0<=discount<=1 or target<=0:r['class']='invalid_terms';return r
    if public_crossed(b):r['class']='crossed_public_book';return r
    own,status=old.proposals(b,target);r['class']=status
    r.update(event_ticker=m.get('event_ticker'),close_time=m['close_time'],depth={s:str(sum((q for p,q,o in b[s]),D(0))) for s in SIDES},top={s:{'price':str(max((p for p,q,o in b[s]),default=D(0))),'quantity':str(sum(q for p,q,o in b[s] if p==max((p for p,q,o in b[s]),default=D(0))))} for s in SIDES})
    if not own:return r
    duration=D(str(stamp(p['end_date'])-stamp(p['start_date'])));remaining=D(str(min(stamp(p['end_date']),stamp(m['close_time']))-ns/1e9));pool=D(p['period_reward'])/10000
    r.update(age_minutes=(ns/1e9-stamp(p['start_date']))/60,remaining_minutes=float(remaining/60),short_sides=list(own),plans=[])
    for fraction in (D(0),D('.1')):
        qty,_=old.proposals(b,target,fraction);principal=sum(qty.values())*CENT;reserve=sum(qty.values())/1000
        cases=[stressed(b,target,discount,qty,D(0))]
        if fraction:cases.append(stressed(b,target,discount,qty,target*fraction))
        rewards=[]
        for case in cases:
            if not case['available']:rewards.append(D(0));continue
            for mode,x in case['scores'].items():
                rate=pool/duration*D(str(x['overall_share']))
                amount=payable(rate*remaining*D('.5'))
                x.update(half_uptime_remaining_reward=float(amount),hourly_rate=float(rate*3600),minimum_remaining_minutes=float((principal+reserve)/(rate*D('.5'))/60) if rate else None)
                if mode=='capped':rewards.append(amount)
        conservative=min(rewards);cushion=conservative-principal-reserve
        plan={'buffer_fraction':str(fraction),'quantity':{s:str(q) for s,q in qty.items()},'principal':float(principal),'fee_stress_reserve':float(reserve),'conservative_half_uptime_reward':float(conservative),'conditional_cushion':float(cushion),'cushion_over_principal':float(cushion/principal),'passes':cushion>0,'cases':cases}
        r['plans'].append(plan)
    r['buffered_alert']=r['plans'][1]['passes'];return r
