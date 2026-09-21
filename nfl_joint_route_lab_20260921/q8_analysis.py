"""Apply preregistered Q8 selection without fitting thresholds."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def select(scenarios):
    outcomes={}
    for arm in ['rescue','joint']:
        checks={}
        for q in [3300,10000]:
            for d in [.25,5]:
                prefix=f'q{q}_d{d:g}_';a=scenarios[prefix+arm];b=scenarios[prefix+'router_on']
                checks[prefix+'profit']=a['all_flat'] and a['completed_strategy_pnl'] is not None and a['completed_strategy_pnl']>max(0,b['completed_strategy_pnl'])
                checks[prefix+'inventory']=a['unhedged_contract_hours']<=1.25*b['unhedged_contract_hours']
        a=scenarios['q3300_d0.25_'+arm];b=scenarios['q3300_d0.25_router_on']
        checks['both_weeks']=all(a['week_contributions'][w]>b['week_contributions'][w] for w in ['week1','week2'])
        checks['excluding_best_two']=a['pnl_excluding_top_two_games'] is not None and a['pnl_excluding_top_two_games']>0
        outcomes[arm]=dict(passed=all(checks.values()),checks=checks)
    selected=next((a for a in ['rescue','joint'] if outcomes[a]['passed']),'router_on')
    return dict(selected=selected,screen=outcomes,evidence='REUSED_DEVELOPMENT_ONLY')

if __name__=='__main__':
    summary=json.loads((ROOT/'results/experiment_summary.json').read_text())
    assert not summary['failures'] and len(summary['scenarios'])==12
    result=select(summary['scenarios'])
    (ROOT/'results/selection.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))
