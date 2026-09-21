"""Q7 isolated price guard. Inherited Q6 source is imported without edits."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'nfl_factorial_lab_20260921'))
from adaptive_policy import AdaptiveReplay, floor_qty
from factorial_policy import FactorialReplay, Factors


def chosen_margin(engine, legs):
    if len(legs) != 2 or {c['direction'] for c in legs} != {-1, 1}:
        return None
    return 1-sum(c['cost'] for c in legs)-.0002-2*float(engine.cfg.balance_precision)/engine.cfg.order_size


def pair_record(engine, candidates, chosen, now, guard, stage, allowed=None):
    legs = [c for c in candidates if c['key'] in chosen]
    margin = chosen_margin(engine, legs)
    event = engine.event(candidates[0]['key'][0]) if candidates else None
    return dict(at=now, event=event, stage=stage, guard=guard,
                margin=margin, price_check_passes=margin is not None and margin > 0,
                reason='missing_pair' if margin is None else 'nonpositive_margin' if margin <= 0 else 'positive_margin',
                inventory=engine.holdings[event] if event else None,
                candidates=[dict(key=c['key'], direction=c['direction'], price=c['price'],
                                 cost=c['cost'], wanted=c['wanted']) for c in candidates],
                chosen=sorted(chosen), allowed=allowed)


class GuardedRouter(AdaptiveReplay):
    def __init__(self, markets, config):
        self.pair_records=[]
        self._decision_time=None
        super().__init__(markets, config, 'baseline')

    def refresh(self, event, now):
        previous=self._decision_time
        self._decision_time=now
        try:
            return super().refresh(event, now)
        finally:
            self._decision_time=previous

    def choose(self, candidates):
        chosen=super().choose(candidates)
        legs=[c for c in candidates if c['key'] in chosen]
        margin=chosen_margin(self, legs)
        record=pair_record(self, candidates, chosen, self._decision_time, True, 'router_refresh')
        if margin is None or margin <= 0:
            allowed=set()
            quantities={}
            pending_offsets={}
            for c in legs:
                event=self.event(c['key'][0])
                if c['direction']*self.holdings[event] < 0:
                    quantity,pending=self.bounded_quantity(c, 0)
                    pending_offsets['/'.join(c['key'])]=pending
                    if quantity >= .01:
                        c['wanted']=quantity
                        allowed.add(c['key'])
                        quantities['/'.join(c['key'])]=quantity
            record['allowed']=sorted(allowed)
            record['offset_quantities']=quantities
            record['other_pending_offsets']=pending_offsets
            chosen=allowed
        else:
            record['allowed']=sorted(chosen)
        self.pair_records.append(record)
        return chosen


class PairAllocator(FactorialReplay):
    def __init__(self, markets, config, guard):
        if type(guard) is not bool:
            raise ValueError('guard must be bool')
        self.guard=guard
        self.pair_records=[]
        super().__init__(markets, config, Factors(False, False, False))

    def portfolio_rank(self, candidates, now):
        # Guard-on delegates to the frozen Q6 implementation. choose is deterministic
        # and only annotates these transient candidates; the extra call logs its pair.
        if self.guard:
            result=super().portfolio_rank(candidates, now)
        else:
            result=self.rank_without_margin_rejection(candidates, now)
        chosen=self.choose(candidates)
        record=pair_record(self, candidates, chosen, now, self.guard, 'allocator_budget')
        record['budget_eligible']=result is not None
        self.pair_records.append(record)
        return result

    def rank_without_margin_rejection(self, candidates, now):
        # Exact Q6 portfolio_rank, except its margin<=0 rejection is removed.
        chosen=self.choose(candidates);legs=[c for c in candidates if c['key'] in chosen]
        if len(legs)!=2:return None
        has_flow=all(c['rate']>0 for c in legs)
        if self.factors.flow and not has_flow:return None
        quantity=self.cfg.order_size
        margin=1-sum(c['cost'] for c in legs)-.0002-2*float(self.cfg.balance_precision)/quantity
        capital=sum(quantity*(c['cost']+.0001)+float(self.cfg.balance_precision) for c in legs)
        incumbent=any(c['key'] in self.orders and self.orders[c['key']].cancel_at is None for c in legs)
        if has_flow:
            wait=max((c['queue']+quantity/self.cfg.fill_participation)/c['rate'] for c in legs)
            score=quantity*margin/(capital*max(wait/3600,1/60))
            reset_wait=max((self.queue(c['key'][0],now)+quantity/self.cfg.fill_participation)/c['rate'] for c in legs)
            lost=max(0,reset_wait-wait)
        else:
            wait=None;score=0.;lost=None
        adjusted=score*(1.25 if incumbent else 1) if self.factors.ranking else 1.
        return dict(score=score,adjusted=adjusted,capital=capital,wait_seconds=wait,
                    lost_queue_wait_seconds=lost,incumbent=incumbent,has_observed_flow=has_flow)


def make_engine(markets, config, arm):
    if arm=='router_off':return AdaptiveReplay(markets, config, 'baseline')
    if arm=='router_on':return GuardedRouter(markets, config)
    if arm=='allocator_off':return PairAllocator(markets, config, False)
    if arm=='allocator_on':return PairAllocator(markets, config, True)
    raise ValueError('Unknown Q7 arm')
