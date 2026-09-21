import hashlib,json
from pathlib import Path
import run_experiment as run
from adaptive_policy import AdaptiveReplay
ROOT=Path(__file__).resolve().parent

class NeutralRankingReplay(AdaptiveReplay):
    def __init__(self,markets,config,experiment='allocation_neutral'):
        super().__init__(markets,config,'allocation')
    def portfolio_rank(self,candidates,now):
        rank=super().portfolio_rank(candidates,now)
        if rank:rank['adjusted']=1.
        return rank

def main():
    frozen=json.loads((ROOT/'FROZEN_ALLOCATION_DIAGNOSTIC.json').read_text())
    for name,digest in frozen['sha256'].items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,name
    cohort=run.checked_inputs();run.AdaptiveReplay=NeutralRankingReplay
    out=dict(cohort=cohort,scenarios={})
    for q in [3300,10000]:
        r=run.one((q,.25,'allocation_neutral'));out['scenarios'][r['scenario']]=r
        run.atomic_json(ROOT/'results/allocation_diagnostic_summary.json',out)
        print(r['scenario'],'pnl',r['completed_strategy_pnl'],'residual',r['unresolved_contracts'],flush=True)
    print('DONE 2 diagnostic controls',flush=True)

if __name__=='__main__':main()
