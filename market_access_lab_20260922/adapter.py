"""Execution-neutral building blocks; not a broker or portfolio replay."""
from decimal import Decimal
from dataclasses import dataclass
import math


def number(value):
    x=Decimal(str(value))
    if not x.is_finite():raise ValueError('Nonfinite number')
    return x


def maker_coefficient(series,event):
    kind=event.get('fee_type_override')
    if kind is None:kind=series.get('fee_type')
    multiplier=event.get('fee_multiplier_override')
    if multiplier is None:multiplier=series.get('fee_multiplier')
    m=number(multiplier)
    if m<0:raise ValueError('Negative multiplier')
    if kind=='quadratic':return Decimal(0)
    if kind=='quadratic_with_maker_fees':return Decimal('.0175')*m
    raise ValueError('Unsupported fee type: '+str(kind))


@dataclass(frozen=True)
class Schedule:
    event: str
    start: float
    observed_at: float
    source: str


def entry_window(*,event,listed_at,now,schedule,max_schedule_age,entry_lead,stop_lead,state):
    """Schedule must be supplied from a trusted start-time source, never close_time."""
    if schedule is None:return dict(eligible=False,reason='missing_start_time')
    if not schedule.source or schedule.event!=event:return dict(eligible=False,reason='schedule_identity')
    values=[listed_at,now,schedule.start,schedule.observed_at,max_schedule_age,entry_lead,stop_lead]
    if any(not math.isfinite(v) for v in values):raise ValueError('Nonfinite timing')
    if not 0<=stop_lead<entry_lead or max_schedule_age<=0:raise ValueError('Invalid timing profile')
    if not 0<=now-schedule.observed_at<=max_schedule_age:return dict(eligible=False,reason='schedule_not_current')
    if state!='scheduled':return dict(eligible=False,reason='exception_or_inplay_pause')
    opens=max(listed_at,schedule.start-entry_lead);stops=schedule.start-stop_lead
    return dict(eligible=opens<=now<stops,reason='within_window' if opens<=now<stops else 'outside_window',opens=opens,stops=stops)


def settlement_payout(yes_quantity,no_quantity,yes_value):
    """Gross settlement cash only. Acquisition costs/fees belong to the portfolio."""
    y,n,v=map(number,[yes_quantity,no_quantity,yes_value])
    if min(y,n)<0 or not 0<=v<=1:raise ValueError('Invalid settlement input')
    return y*v+n*(1-v)


def best(levels):
    valid=[]
    for p,q in levels:
        p,q=number(p),number(q)
        if not 0<p<1 or q<0:raise ValueError('Invalid book level')
        if q:valid.append((p,q))
    if not valid:return None
    price=max(p for p,q in valid)
    return price,sum(q for p,q in valid if p==price)


def indicative_pair(book,coefficient):
    ob=book.get('orderbook_fp')
    if ob is None:raise ValueError('Missing fixed-point orderbook')
    y,n=best(ob.get('yes_dollars',[])),best(ob.get('no_dollars',[]))
    if y is None or n is None:return dict(two_sided=False)
    c=number(coefficient)
    if c<0:raise ValueError('Negative fee')
    gross=1-y[0]-n[0]
    if gross<=0:return dict(two_sided=True,usable=False,reason='locked_or_crossed')
    fees=sum(c*p*(1-p) for p in [y[0],n[0]])
    margin=gross-fees-Decimal('.0002')-2*Decimal('.0001')/250
    return dict(two_sided=True,usable=True,yes_bid=str(y[0]),no_bid=str(n[0]),
                yes_best_level_size=str(y[1]),no_best_level_size=str(n[1]),
                gross_pair_margin=str(gross),nominal_maker_fees=str(fees),
                buffered_pair_margin=str(margin),positive_margin=margin>0)
