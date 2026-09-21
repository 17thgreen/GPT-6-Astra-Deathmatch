"""Q8 pairwise route selection; imports frozen Q7 accounting unchanged."""
import sys
from pathlib import Path
from itertools import product
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'nfl_pair_price_lab_20260921'))
from pair_policy import GuardedRouter, chosen_margin, pair_record
from adaptive_policy import AdaptiveReplay


def rank_pairs(engine, candidates):
    pairs=[]
    for a,b in product([c for c in candidates if c['direction']==-1],
                       [c for c in candidates if c['direction']==1]):
        margin=chosen_margin(engine,[a,b])
        if margin is None or margin<=0:continue
        keys=tuple(sorted((a['key'],b['key'])))
        incumbent=all(c['key'] in engine.orders and
                      engine.orders[c['key']].cancel_at is None and
                      abs(engine.orders[c['key']].price-c['price'])<1e-9 for c in [a,b])
        pairs.append(dict(keys=keys,margin=margin,score=margin*min(a['service'],b['service']),
                          cost=a['cost']+b['cost'],incumbent=incumbent))
    return sorted(pairs,key=lambda p:(-p['score'],p['cost'],p['keys']))


class JointRouter(GuardedRouter):
    def __init__(self,markets,config,mode):
        if mode not in ('rescue','joint'):raise ValueError('Unknown Q8 mode')
        self.route_mode=mode
        super().__init__(markets,config)

    def choose(self,candidates):
        original=AdaptiveReplay.choose(self,candidates)
        margin=chosen_margin(self,[c for c in candidates if c['key'] in original])
        if self.route_mode=='rescue' and margin is not None and margin>0:
            return super().choose(candidates)
        pairs=rank_pairs(self,candidates)
        if not pairs:return super().choose(candidates)
        best=pairs[0]
        incumbents=[p for p in pairs if p['incumbent']]
        if incumbents and best['score']<=self.policy.switch_ratio*incumbents[0]['score']+1e-15:
            best=incumbents[0]
        chosen=set(best['keys'])
        record=pair_record(self,candidates,chosen,self._decision_time,True,'joint_route',sorted(chosen))
        record.update(mode=self.route_mode,original_chosen=sorted(original),original_margin=margin,
                      candidate_pairs=pairs,selected_score=best['score'])
        self.pair_records.append(record)
        return chosen


def make_engine(markets,config,arm):
    if arm=='router_on':return GuardedRouter(markets,config)
    return JointRouter(markets,config,arm)
