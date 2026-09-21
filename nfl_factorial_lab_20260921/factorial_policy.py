"""2^3 allocator ablation. Inherited execution code is unchanged."""
from dataclasses import dataclass,asdict
from adaptive_policy import AdaptiveReplay

@dataclass(frozen=True)
class Factors:
    flow: bool=True
    protection: bool=True
    ranking: bool=True
    def __post_init__(self):
        if any(type(v) is not bool for v in asdict(self).values()):raise ValueError('Factors must be bool')
    @property
    def label(self):return ''.join(str(int(v)) for v in (self.flow,self.protection,self.ranking))

class FactorialReplay(AdaptiveReplay):
    def __init__(self,markets,config,factors=Factors()):
        self.factors=factors
        super().__init__(markets,config,'allocation')

    def portfolio_rank(self,candidates,now):
        chosen=self.choose(candidates);legs=[c for c in candidates if c['key'] in chosen]
        if len(legs)!=2:return None
        has_flow=all(c['rate']>0 for c in legs)
        if self.factors.flow and not has_flow:return None
        quantity=self.cfg.order_size
        margin=1-sum(c['cost'] for c in legs)-.0002-2*float(self.cfg.balance_precision)/quantity
        if margin<=0:return None
        capital=sum(quantity*(c['cost']+.0001)+float(self.cfg.balance_precision) for c in legs)
        incumbent=any(c['key'] in self.orders and self.orders[c['key']].cancel_at is None for c in legs)
        if has_flow:
            wait=max((c['queue']+quantity/self.cfg.fill_participation)/c['rate'] for c in legs)
            score=quantity*margin/(capital*max(wait/3600,1/60))
            reset_wait=max((self.queue(c['key'][0],now)+quantity/self.cfg.fill_participation)/c['rate'] for c in legs)
            lost=max(0,reset_wait-wait)
        else:
            # Missing flow is not invented. Gate-off admits the pair; ranking-on puts it last.
            wait=None;score=0.;lost=None
        adjusted=score*(1.25 if incumbent else 1) if self.factors.ranking else 1.
        return dict(score=score,adjusted=adjusted,capital=capital,wait_seconds=wait,
                    lost_queue_wait_seconds=lost,incumbent=incumbent,has_observed_flow=has_flow)

    def rebalance(self,now):
        if now<self.next_allocation:return
        self.next_allocation=now+600
        candidates={event:self.event_candidates(event,now) for event in self.groups}
        ranks=[];need=0.
        for event,cs in candidates.items():
            inventory=self.holdings[event]
            offset=[c for c in cs if c['direction']*inventory<0]
            outstanding=sum(self.reserve_cost(o) for o in self.orders.values()
                            if self.event(o.ticker)==event and o.direction*inventory<0)
            offset_cost=abs(inventory)*max((c['cost']+.0001 for c in offset),default=1.)
            need+=max(outstanding,offset_cost)
            rank=self.portfolio_rank(cs,now)
            if rank:ranks.append((event,rank))
        protected=need if self.factors.protection else 0.
        available=max(0,self.cash-protected);budgets={}
        for event,rank in sorted(ranks,key=lambda x:(-x[1]['adjusted'],x[0])):
            budget=min(available,rank['capital']);budgets[event]=budget;available-=budget
        self.allocations=budgets
        self.record('allocation',now,cash=self.cash,protected=protected,offset_cash_need=need,
                    unallocated=available,allocations=budgets.copy(),
                    ranks=[dict(event=e,**r) for e,r in ranks])
        self.metrics['portfolio_rebalances']+=1

    def finish(self,end):
        result=super().finish(end)
        result['factors']=asdict(self.factors);result['factor_label']=self.factors.label
        return result
