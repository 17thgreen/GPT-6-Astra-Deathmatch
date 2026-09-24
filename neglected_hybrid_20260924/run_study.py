"""Run all frozen NH-001 and amended NH-001A comparisons; no parameter search."""
from pathlib import Path
import argparse,csv,json,hashlib
from core import evaluate,DECISIONS,ARMS

AMENDED=['2024-11-04T22:00:00Z','2024-11-05T16:00:00Z']
def run(dataset, output):
    data=json.loads(dataset.read_text());output.mkdir(parents=True,exist_ok=True)
    all_results={}
    for family in ['house','senate']:
        subset=dict(data,races=[r for r in data['races'] if r['chamber']==family])
        for study,decisions in [('NH-001',DECISIONS),('NH-001A',AMENDED)]:
            result=evaluate(subset,decisions);result['study']=study;result['family']=family
            all_results[f'{study}_{family}']=result
    (output/'scorecard.json').write_text(json.dumps(all_results,indent=2)+'\n')
    fields=['study','family','decision','races','arm','brier','brier_delta_vs_market','signals',
            'hypothetical_net_dollars','capital_dollars','hypothetical_return_on_capital',
            'extra_3c_cost_same_trades_net','excluding_best_two_winners_net']
    table=[];trades=[]
    for result in all_results.values():
        for h in result['horizons']:
            for arm,metrics in (h['summary'] or {}).items():
                row=dict(study=result['study'],family=result['family'],decision=h['decision'],races=h['admitted_races'],arm=arm)
                row.update({k:metrics.get(k) for k in fields if k not in row});table.append(row)
            for race in h['rows']:
                for arm,a in race['arms'].items():
                    t=a['trade']
                    if t:trades.append(dict(study=result['study'],family=result['family'],decision=h['decision'],race_id=race['race_id'],
                       ticker=race['ticker'],arm=arm,probability=a['p'],p_model=race['p_model'],p_market=race['p_market'],outcome_dem=race['outcome_dem'],**t))
    with (output/'summary.csv').open('w') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(table)
    (output/'hypothetical_trades.json').write_text(json.dumps(trades,indent=2)+'\n')
    (output/'dataset_sha256.txt').write_text(hashlib.sha256(dataset.read_bytes()).hexdigest()+'  '+dataset.name+'\n')
    for result in all_results.values():
        for h in result['horizons']:
            print(json.dumps({'study':result['study'],'family':result['family'],'decision':h['decision'],
                'races':h['admitted_races'],'exclusions':h['exclusion_counts'],'summary':h['summary']}))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('dataset',type=Path);p.add_argument('output',type=Path);a=p.parse_args();run(a.dataset,a.output)
