"""Post-result synthetic mechanism probe; not a financial attribution experiment."""
import json
from pathlib import Path
from test_factorial import engine,AT

def main():
    r=engine('000');candidates=[]
    for key,d,cost,service in [(('A','yes'),1,.4,.01),(('B','no'),1,.55,1),
                              (('B','yes'),-1,.4,.01),(('A','no'),-1,.55,1)]:
        candidates.append(dict(key=key,direction=d,cost=cost,service=service,rate=1,
            queue=100,wanted=250,price=cost,inside=False))
    chosen=r.choose(candidates);cost=sum(c['cost'] for c in candidates if c['key'] in chosen)
    assert chosen=={('B','no'),('A','no')} and cost>1
    assert r.portfolio_rank(candidates,AT) is None
    result=dict(evidence='POST_RESULT_STRUCTURAL_PROBE_NOT_PROFIT_ATTRIBUTION',
        chosen_routes=sorted(chosen),chosen_pair_unit_cost=cost,
        original_router_selects_both=True,common_allocator_rejects_pair=True,
        interpretation="Original route scores use each direction's cheapest possible counterleg; the two actually chosen routes can jointly be unprofitable. The common allocator adds a check of their combined cost. This probe does not measure its historical P&L contribution.")
    (Path(__file__).resolve().parent/'results/shared_margin_probe.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
