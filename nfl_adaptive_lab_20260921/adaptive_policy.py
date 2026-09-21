"""Three isolated research interventions. No network or live-order capability."""
import math
from collections import defaultdict, deque
from timing_policy import TimingReplay

MODES=('baseline','inventory','patience','allocation')

def floor_qty(q):
    return math.floor(max(0,q)*100+1e-8)/100

class AdaptiveReplay(TimingReplay):
    def __init__(self,markets,config,experiment='baseline'):
        if experiment not in MODES:raise ValueError('Unknown experiment')
        self.experiment=experiment
        self.decisions=[];self.pending_marks=defaultdict(deque);self.marks=defaultdict(deque)
        self.cooldown={};self.next_allocation=-math.inf;self.allocations={}
        super().__init__(markets,config,'full','route')

    def event_candidates(self,event,now):
        return [c for t in sorted(self.groups[event]) for side in ('yes','no')
                if (c:=self.candidate(t,side,now)) is not None]

    def direction_rates(self,candidates):
        # Equivalent team-market routes are alternatives, not independent liquidity.
        return {d:max((c['rate'] for c in candidates if c['direction']==d),default=0.) for d in (-1,1)}

    def record(self,kind,now,**kwargs):
        self.decisions.append(dict(kind=kind,at=now,**kwargs))

    def inventory_target(self,c,candidates,now):
        horizon=max(0,min(1800,self.markets[c['key'][0]]['kickoff']-10800-
                         self.cfg.liquidation_lead_seconds-now-self.cfg.cancel_delay_seconds))
        opposing=max((max(0,x['rate']*horizon-x['queue'])*self.cfg.fill_participation
                       for x in candidates if x['direction']==-c['direction']),default=0)
        return floor_qty(min(self.cfg.exposure_cap,self.exit_remaining[self.event(c['key'][0])],max(25,opposing)))

    def bounded_quantity(self,c,target):
        event=self.event(c['key'][0]);old=self.orders.get(c['key'])
        pending=sum(o.remaining for o in self.orders.values() if self.event(o.ticker)==event
                    and o.direction==c['direction'] and o is not old)
        room=target-c['direction']*self.holdings[event]-pending
        return floor_qty(min(c['wanted'],room)),pending

    def mature_marks(self,row):
        ticker=row['ticker'];pending=self.pending_marks[ticker]
        while pending and pending[0]['due']<=row['asof']:
            m=pending.popleft()
            if row['asof']>m['due']+300 or not 0<row['bid']<row['ask']<1:
                self.metrics['markouts_missing']+=1;continue
            midpoint=(row['bid']+row['ask'])/2
            value=(midpoint if m['outcome']=='yes' else 1-midpoint)-m['price']
            key=(ticker,m['outcome'])
            self.marks[key].append(dict(observed_at=row['at'],markout=value,size=m['size']))
            self.metrics['markouts_observed']+=1

    def markout_mean(self,key,now):
        samples=self.marks[key]
        while samples and samples[0]['observed_at']<now-3600:samples.popleft()
        usable=[s for s in samples if s['observed_at']<now]
        size=sum(s['size'] for s in usable)
        if len(usable)<5 or size<25:return None
        return sum(s['size']*s['markout'] for s in usable)/size

    def on_quote(self,row):
        if self.experiment=='patience':
            self.advance(row['at']) # Timers cannot see this newly arriving quote.
            self.mature_marks(row)
        return super().on_quote(row)

    def account_fill(self,order,qty,now,kind,reason):
        super().account_fill(order,qty,now,kind,reason)
        if self.experiment=='patience' and kind=='maker':
            added=max(0,qty-self.fills[-1]['paired'])
            if added>=.01:
                self.pending_marks[order.ticker].append(dict(due=now+300,price=order.price,
                    outcome=order.outcome,size=added))

    def patience_decision(self,c,candidates,now):
        event=self.event(c['key'][0]);inventory=self.holdings[event]
        if c['direction']*inventory<0:return True,'offset',None
        if self.cooldown.get(c['key'],-math.inf)>now:return False,'cooldown',None
        rates=self.direction_rates(candidates);own=rates[c['direction']];opposite=rates[-c['direction']]
        imbalance=own>3*opposite and own>0
        mean=self.markout_mean(c['key'],now)
        if mean is not None and (mean<-.02 or (mean<-.005 and imbalance)):
            return False,'adverse_markout',dict(markout=mean,own_rate=own,opposite_rate=opposite)
        old=self.orders.get(c['key'])
        if old is None or old.cancel_at is not None:return True,'new',None
        initial=self.order_records.get(old.identity,{}).get('initial_queue',self.queue(old.ticker,old.active_at))
        progress=max(0,min(1,1-old.queue/initial)) if initial else 1
        service=min(1,own*600/(old.queue+old.remaining/self.cfg.fill_participation))
        patience=1800 if progress>=.5 and not imbalance else 120+1680*service
        if old.queue>0 and now-old.active_at>=patience:
            self.cooldown[c['key']]=now+60
            return False,'patience_expired',dict(patience=patience,queue=old.queue,progress=progress,
                                                own_rate=own,opposite_rate=opposite)
        return True,'wait',None

    def portfolio_rank(self,candidates,now):
        chosen=self.choose(candidates)
        legs=[c for c in candidates if c['key'] in chosen]
        if len(legs)!=2 or any(c['rate']<=0 for c in legs):return None
        quantity=self.cfg.order_size
        margin=1-sum(c['cost'] for c in legs)-.0002-2*float(self.cfg.balance_precision)/quantity
        if margin<=0:return None
        wait=max((c['queue']+quantity/self.cfg.fill_participation)/c['rate'] for c in legs)
        capital=sum(quantity*(c['cost']+.0001)+float(self.cfg.balance_precision) for c in legs)
        score=quantity*margin/(capital*max(wait/3600,1/60))
        incumbent=any(c['key'] in self.orders and self.orders[c['key']].cancel_at is None for c in legs)
        # A new order always uses the back-of-queue estimate. Incumbents retain their remaining queue.
        adjusted=score*(1.25 if incumbent else 1)
        reset_wait=max((self.queue(c['key'][0],now)+quantity/self.cfg.fill_participation)/c['rate'] for c in legs)
        return dict(score=score,adjusted=adjusted,capital=capital,wait_seconds=wait,
                    lost_queue_wait_seconds=max(0,reset_wait-wait),incumbent=incumbent)

    def rebalance(self,now):
        if now<self.next_allocation:return
        self.next_allocation=now+600
        candidates={event:self.event_candidates(event,now) for event in self.groups}
        ranks=[];protected=0.
        for event,cs in candidates.items():
            inventory=self.holdings[event]
            # Protect all currently reserved offset orders (even if cancel pending), and enough
            # estimated cash for a whole inventory offset at the most expensive current candidate.
            offset=[c for c in cs if c['direction']*inventory<0]
            outstanding=sum(self.reserve_cost(o) for o in self.orders.values()
                            if self.event(o.ticker)==event and o.direction*inventory<0)
            offset_cost=abs(inventory)*max((c['cost']+.0001 for c in offset),default=1.)
            protected+=max(outstanding,offset_cost)
            rank=self.portfolio_rank(cs,now)
            if rank:ranks.append((event,rank))
        available=max(0,self.cash-protected);budgets={}
        for event,rank in sorted(ranks,key=lambda x:(-x[1]['adjusted'],x[0])):
            budget=min(available,rank['capital']);budgets[event]=budget;available-=budget
        self.allocations=budgets
        self.record('allocation',now,cash=self.cash,protected=protected,unallocated=available,
                    allocations=budgets.copy(),ranks=[dict(event=e,**r) for e,r in ranks])
        self.metrics['portfolio_rebalances']+=1

    def refresh(self,event,now):
        if self.experiment=='baseline':return super().refresh(event,now)
        if self.experiment=='allocation':self.rebalance(now)
        candidates=self.event_candidates(event,now);chosen=self.choose(candidates)
        desired={}
        for c in candidates:
            if c['key'] not in chosen:continue
            quantity=c['wanted'];detail=None
            if self.experiment=='inventory':
                target=self.inventory_target(c,candidates,now)
                quantity,pending=self.bounded_quantity(c,target)
                detail=dict(target=target,inventory=self.holdings[event],other_reserved=pending)
            elif self.experiment=='patience':
                allow,reason,info=self.patience_decision(c,candidates,now)
                if not allow:
                    self.metrics[reason+'_decisions']+=1
                    old=self.orders.get(c['key'])
                    if old and old.cancel_at is None:self.record(reason,now,event=event,key=c['key'],order_id=old.identity,details=info)
                    continue
            else:
                # An entry allowance covers both directions proportionately. Offsetting inventory
                # is independently protected; old pending reservations still constrain actual orders.
                selected=[x for x in candidates if x['key'] in chosen]
                total=sum(x['wanted']*(x['cost']+.0001)+float(self.cfg.balance_precision) for x in selected)
                fraction=min(1,self.allocations.get(event,0)/total) if total else 0
                quantity=floor_qty(quantity*fraction)
                if c['direction']*self.holdings[event]<0:
                    offset,_=self.bounded_quantity(c,0)
                    quantity=max(quantity,offset)
            if quantity>=.01:desired[c['key']]=(c,quantity,detail)
        for key,old in list(self.orders.items()):
            if self.event(old.ticker)==event and key not in desired:self.cancel(old,now,self.experiment)
        for key,(c,quantity,detail) in desired.items():
            old=self.orders.get(key)
            if self.experiment=='inventory' and (old is None or quantity<old.remaining-.009):
                self.record('inventory_target',now,event=event,key=key,quantity=quantity,**detail)
            self.quote(*key,c['price'],quantity,now)
        if any(self.eligible(t,now) for t in self.groups[event]):
            at=now+self.cfg.requote_seconds;self.scheduled[event]=at;self.push(at,3,'refresh',event)

    def quote(self,ticker,outcome,price,wanted,now):
        super().quote(ticker,outcome,price,wanted,now)
        old=self.orders.get((ticker,outcome))
        if old and old.identity in self.order_records:
            self.order_records[old.identity].setdefault('initial_queue',old.queue)

    def match(self,row):
        before=len(self.fills);super().match(row)
        if self.experiment=='inventory' and len(self.fills)>before:
            self.refresh(self.event(row['ticker']),row['at'])

    def finish(self,end):
        result=super().finish(end)
        result.update(experiment=self.experiment,decision_records=len(self.decisions))
        return result
