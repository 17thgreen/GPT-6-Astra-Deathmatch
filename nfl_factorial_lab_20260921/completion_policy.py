"""Joint entry-capacity gate and event-level completion controller; no order API."""
import math
from queue_policies import QueueReplay,Policy

def projected_capacity(rate,queue,horizon,participation,limit):
    if any(not math.isfinite(v) or v<0 for v in (rate,queue,horizon,participation,limit)):
        raise ValueError('Invalid service projection')
    return math.floor(min(limit,max(0,rate*horizon-queue)*participation)*100+1e-8)/100

class CompletionReplay(QueueReplay):
    def __init__(self,markets,config,mode='pair_gate'):
        if mode not in ('q1_route','pair_gate','pair_complete'):raise ValueError('Unknown completion policy')
        self.mode=mode;self.completion_ids=set();self.last_pair={}
        super().__init__(markets,config,Policy(name='route'))

    def current_order(self,c):
        o=self.orders.get(c['key'])
        return o if o and o.cancel_at is None and abs(o.price-c['price'])<1e-9 else None

    def candidates(self,event,now):
        result=[]
        for ticker in sorted(self.groups[event]):
            for outcome in ('yes','no'):
                c=self.candidate(ticker,outcome,now)
                if not c:continue
                cutoff=self.markets[ticker]['kickoff']-10800-self.cfg.liquidation_lead_seconds
                horizon=max(0,min(600,cutoff-now-self.cfg.cancel_delay_seconds-self.cfg.order_delay_seconds))
                old=self.current_order(c)
                limit=min(c['wanted'],old.remaining) if old else c['wanted']
                c['capacity']=projected_capacity(c['rate'],c['queue'],horizon,self.cfg.fill_participation,limit)
                c['horizon']=horizon
                result.append(c)
        return result

    def choose_pair(self,candidates):
        plus=[c for c in candidates if c['direction']>0]
        minus=[c for c in candidates if c['direction']<0]
        pairs=[]
        for a in plus:
            for b in minus:
                quantity=min(a['capacity'],b['capacity'])
                if quantity<1:continue
                margin=1-a['cost']-b['cost']-.0002-2*float(self.cfg.balance_precision)/quantity
                if margin<=0:continue
                pairs.append(dict(legs=(a,b),size=quantity,margin=margin,score=margin*quantity,
                                  keys=(a['key'],b['key'])))
        if not pairs:return None
        best=min(pairs,key=lambda p:(-p['score'],p['keys']))
        incumbents=[p for p in pairs if all(self.current_order(c) for c in p['legs'])]
        if incumbents:
            old=min(incumbents,key=lambda p:(-p['score'],p['keys']))
            if best['score']<=self.policy.switch_ratio*old['score']+1e-15:best=old
        return best

    def choose_offset(self,candidates,inventory):
        same=[c for c in candidates if c['direction']*inventory<0]
        if not same:return None
        def service(c):return min(abs(inventory),c['capacity'])
        best=min(same,key=lambda c:(-service(c),c['cost'],c['key']))
        incumbents=[c for c in same if self.current_order(c)]
        if incumbents:
            old=min(incumbents,key=lambda c:(-service(c),c['cost'],c['key']))
            if service(old)>0 and service(best)<=self.policy.switch_ratio*service(old)+1e-15:best=old
            elif service(old)==0 and service(best)==0 and best['cost']>=old['cost']-1e-12:best=old
        return best

    def refresh(self,event,now):
        if self.mode=='q1_route':return super().refresh(event,now)
        candidates=self.candidates(event,now);inventory=self.holdings[event];pair=None
        if self.mode=='pair_complete' and abs(inventory)>=.01:
            self.metrics['inventory_completion_refreshes']+=1
        else:
            self.metrics['entry_gate_checks']+=1
            pair=self.choose_pair(candidates)
            if pair is None:self.metrics['entry_gate_abstentions']+=1
        desired={};offset=False
        if pair:
            desired={c['key']:(c,pair['size']) for c in pair['legs']}
            if event in self.last_pair and self.last_pair[event]!=pair['keys']:self.metrics['pair_switch_decisions']+=1
            self.last_pair[event]=pair['keys']
        elif abs(inventory)>=.01:
            c=self.choose_offset(candidates,inventory)
            if c:
                old=self.orders.get(c['key'])
                reserved=sum(o.remaining for o in self.orders.values() if self.event(o.ticker)==event
                             and o.direction==c['direction'] and o is not old)
                quantity=math.floor(max(0,min(self.cfg.order_size,abs(inventory)-reserved))*100+1e-8)/100
                desired[c['key']]=(c,quantity);offset=True
        for key,o in list(self.orders.items()):
            if self.event(o.ticker)==event and key not in desired:self.cancel(o,now,'completion/entry gate')
        for key,(c,quantity) in desired.items():
            self.quote(*key,c['price'],quantity,now)
            o=self.orders.get(key)
            if o and o.cancel_at is None:
                if offset:self.completion_ids.add(o.identity)
                else:self.completion_ids.discard(o.identity)
        if any(self.eligible(t,now) for t in self.groups[event]):
            at=now+self.cfg.requote_seconds;self.scheduled[event]=at;self.push(at,3,'refresh',event)

    def match(self,row):
        count=len(self.fills)
        super().match(row)
        if self.mode=='pair_complete' and len(self.fills)>count:
            self.refresh(self.event(row['ticker']),row['at'])

    def account_fill(self,order,qty,now,kind,reason):
        completing=order.identity in self.completion_ids
        super().account_fill(order,qty,now,kind,reason)
        self.fills[-1]['completion_instruction']=completing
        if completing:
            self.metrics['completion_filled_contracts']+=qty
            self.metrics['completion_overshoot_contracts']+=max(0,qty-self.fills[-1]['paired'])

    def finish(self,coverage_end):
        result=super().finish(coverage_end);result['completion_policy']=self.mode
        return result
