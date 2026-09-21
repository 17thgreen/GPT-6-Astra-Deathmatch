"""Predeclared factorial contrasts and deterministic simplification screen."""
import itertools,json,hashlib,datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parent
LABELS=[''.join(map(str,b)) for b in itertools.product([0,1],repeat=3)]
FACTORS=['flow','protection','ranking']

def contrasts(values):
    conditional={};main={};pairwise={};shapley={f:0. for f in FACTORS}
    for index,factor in enumerate(FACTORS):
        rows=[]
        for low in LABELS:
            if low[index]=='1':continue
            high=low[:index]+'1'+low[index+1:]
            rows.append(dict(off=low,on=high,delta=values[high]-values[low]))
        conditional[factor]=rows;main[factor]=sum(r['delta'] for r in rows)/4
    for i,j in itertools.combinations(range(3),2):
        remaining=next(k for k in range(3) if k not in [i,j]);deltas=[]
        for value in [0,1]:
            def get(a,b):
                bits=['0']*3;bits[i]=str(a);bits[j]=str(b);bits[remaining]=str(value)
                return values[''.join(bits)]
            deltas.append(get(1,1)-get(1,0)-get(0,1)+get(0,0))
        pairwise[FACTORS[i]+' × '+FACTORS[j]]=sum(deltas)/2
    three_way=sum((1 if label.count('1')%2 else -1)*values[label] for label in LABELS)
    for order in itertools.permutations(range(3)):
        bits=['0']*3;before=values['000']
        for index in order:
            bits[index]='1';after=values[''.join(bits)]
            shapley[FACTORS[index]]+=(after-before)/6;before=after
    assert abs(sum(shapley.values())-(values['111']-values['000']))<1e-7
    return dict(main_effects=main,conditional_effects=conditional,pairwise_interactions=pairwise,
                three_way_interaction=three_way,shapley=shapley,full_minus_all_off=values['111']-values['000'])

def select(scenarios):
    get=lambda label,q,d:scenarios[f'q{q}_d{d:g}_{label}']
    valid_full=all(get('111',q,d)['completed_strategy_pnl'] is not None and get('111',q,d)['completed_strategy_pnl']>0 for q in [3300,10000] for d in [.25,5])
    screening={}
    for label in LABELS:
        primary=get(label,3300,.25);base=get('baseline',3300,.25)
        rows=[get(label,q,d) for q in [3300,10000] for d in [.25,5]]
        conditions={
            'flat_all':all(r['all_flat'] for r in rows),
            'positive_all':all(r['completed_strategy_pnl'] is not None and r['completed_strategy_pnl']>0 for r in rows),
            'beats_original_all':all(get(label,q,d)['completed_strategy_pnl'] is not None and get('baseline',q,d)['completed_strategy_pnl'] is not None and get(label,q,d)['completed_strategy_pnl']>get('baseline',q,d)['completed_strategy_pnl'] for q in [3300,10000] for d in [.25,5]),
            'improves_both_primary_weeks':all(primary['week_contributions'][w]>base['week_contributions'][w] for w in ['week1','week2']),
            'positive_primary_excluding_top_two':primary['pnl_excluding_top_two_games'] is not None and primary['pnl_excluding_top_two_games']>0,
            'inventory_within_limit':all(get(label,q,d)['unhedged_contract_hours']<=1.25*get('baseline',q,d)['unhedged_contract_hours'] for q in [3300,10000] for d in [.25,5]),
            'retains_95pct_full_everywhere':valid_full and all(get(label,q,d)['completed_strategy_pnl'] is not None and get(label,q,d)['completed_strategy_pnl']>=.95*get('111',q,d)['completed_strategy_pnl'] for q in [3300,10000] for d in [.25,5])}
        ratios=[get(label,q,d)['completed_strategy_pnl']/get('111',q,d)['completed_strategy_pnl'] for q in [3300,10000] for d in [.25,5]] if valid_full and all(r['completed_strategy_pnl'] is not None for r in rows) else []
        screening[label]=dict(conditions=conditions,eligible=all(conditions.values()),enabled=label.count('1'),worst_retention_ratio=min(ratios) if ratios else None)
    passing=[label for label,r in screening.items() if r['eligible']]
    passing.sort(key=lambda label:(screening[label]['enabled'],-screening[label]['worst_retention_ratio'],label))
    return dict(selected=passing[0] if passing else None,screening=screening,
                status='SHADOW_RESEARCH_CANDIDATE_ONLY' if passing else 'NO_CANDIDATE_SELECTED')

def main():
    summary=json.loads((ROOT/'results/experiment_summary.json').read_text());s=summary['scenarios']
    assert len(s)==36 and not summary.get('failures')
    result={}
    for q in [3300,10000]:
        for d in [.25,5]:
            values={label:s[f'q{q}_d{d:g}_{label}']['completed_strategy_pnl'] for label in LABELS}
            if any(v is None for v in values.values()):
                result[f'q{q}_d{d:g}']=dict(status='UNRESOLVED_NO_ATTRIBUTION');continue
            effects=contrasts(values);base=s[f'q{q}_d{d:g}_baseline']['completed_strategy_pnl']
            effects['common_machinery_vs_original']=values['000']-base
            effects['full_vs_original']=values['111']-base
            assert abs(effects['common_machinery_vs_original']+sum(effects['shapley'].values())-effects['full_vs_original'])<1e-7
            result[f'q{q}_d{d:g}']=effects
    selection=select(s)
    (ROOT/'results/factor_effects.json').write_text(json.dumps(result,indent=2))
    (ROOT/'results/selection.json').write_text(json.dumps(selection,indent=2))
    frozen=json.loads((ROOT/'FROZEN_EXPERIMENT.json').read_text())
    candidate=dict(frozen_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),selected=selection['selected'],
        status=selection['status'],source_sha256=frozen['sha256'],
        baseline_sha256=json.loads((ROOT/'BASELINE_HASHES.json').read_text()),
        common_config=s['q3300_d0.25_111']['config'],scenario_stresses=dict(early_queues=[3300,10000],submit_cancel_delays=[.25,5]),
        selection_sha256=hashlib.sha256((ROOT/'results/selection.json').read_bytes()).hexdigest(),
        evidence='Selected after repeated use of 31 development games. Zero fresh completed games. No live promotion.')
    (ROOT/'SHADOW_CANDIDATE_FREEZE.json').write_text(json.dumps(candidate,indent=2))
    print(json.dumps(dict(selected=selection['selected'],status=selection['status'],primary_effects=result['q3300_d0.25']),indent=2))
if __name__=='__main__':main()
