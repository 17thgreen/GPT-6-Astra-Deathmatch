"""Development diagnostics at minute resolution; never holdout or realized P&L."""
import argparse
import bisect
import gzip
import hashlib
import importlib.util
import json
import shutil
import statistics
from collections import defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parent
POLICIES=['q1_route','pair_complete']


def extract(source):
    spec=importlib.util.spec_from_file_location('q2_loader',source/'load_data.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    events,markets,counts=module.load_all()['combined']
    target=ROOT/'inputs/historical_quotes.jsonl.gz'
    with gzip.open(target,'wt') as out:
        for r in events:
            if r.get('kind')=='quote':out.write(json.dumps(r,separators=(',',':'))+'\n')
    provenance=dict(source=str(source),cohort=counts,files={})
    for mode in POLICIES:
        src=source/'results'/f'combined_q3300_{mode}_fills.jsonl.gz'
        name=f'{mode}_fills.jsonl.gz';shutil.copyfile(src,ROOT/'inputs'/name)
        provenance['files'][name]=hashlib.sha256(src.read_bytes()).hexdigest()
    provenance['files'][target.name]=hashlib.sha256(target.read_bytes()).hexdigest()
    (ROOT/'inputs/historical_provenance.json').write_text(json.dumps(provenance,indent=2))


def future_mark(quote_times,quotes,fill,horizon):
    target=fill['at']+horizon
    i=bisect.bisect_right(quote_times,target)-1
    if i<0:return None
    q=quotes[i]
    if q['asof']<=fill['at'] or target-q['asof']>120 or not 0<q['bid']<=q['ask']<1:return None
    mid=(q['bid']+q['ask'])/2
    if fill['outcome']=='no':mid=1-mid
    initial=fill.get('outcome_mid_at_fill')
    if initial is None:return None
    return dict(target=target,quote_available_at=q['at'],quote_asof=q['asof'],
                midpoint_change_cents=100*(mid-initial),midpoint_less_fill_cents=100*(mid-fill['price']),
                fee_adjusted_midpoint_markout_cents=100*(mid-fill['price']-fill['fee']/fill['size']))


def main(source=None):
    if source:extract(source)
    provenance=json.loads((ROOT/'inputs/historical_provenance.json').read_text())
    for name,digest in provenance['files'].items():
        assert hashlib.sha256((ROOT/'inputs'/name).read_bytes()).hexdigest()==digest,name
    by=defaultdict(list)
    with gzip.open(ROOT/'inputs/historical_quotes.jsonl.gz','rt') as f:
        for line in f:
            q=json.loads(line);by[q['ticker']].append(q)
    times={t:[q['at'] for q in quotes] for t,quotes in by.items()}
    summaries={};per_game=[]
    with gzip.open(ROOT/'results/historical_markout_rows.jsonl.gz','wt') as out:
        for mode in POLICIES:
            with gzip.open(ROOT/'inputs'/f'{mode}_fills.jsonl.gz','rt') as f:fills=[json.loads(line) for line in f]
            fills=[f for f in fills if f['kind']=='maker'];total=sum(f['size'] for f in fills)
            summaries[mode]={}
            for h in (120,300,600):
                grouped=defaultdict(list);rows=[]
                for f in fills:
                    m=future_mark(times[f['ticker']],by[f['ticker']],f,h)
                    if m is None:continue
                    r=dict(policy=mode,event=f['event'],ticker=f['ticker'],order_id=f['order_id'],
                           fill_at=f['at'],size=f['size'],horizon_seconds=h,**m)
                    rows.append(r);grouped[f['event']].append(r)
                    out.write(json.dumps(r,separators=(',',':'))+'\n')
                volume=sum(r['size'] for r in rows)
                fields=['midpoint_change_cents','midpoint_less_fill_cents','fee_adjusted_midpoint_markout_cents']
                weighted={k:sum(r['size']*r[k] for r in rows)/volume if volume else None for k in fields}
                for event,rr in grouped.items():
                    v=sum(r['size'] for r in rr)
                    per_game.append(dict(policy=mode,event=event,horizon_seconds=h,contracts=v,
                        **{k:sum(r['size']*r[k] for r in rr)/v for k in fields}))
                means=[r['midpoint_change_cents'] for r in per_game if r['policy']==mode and r['horizon_seconds']==h]
                summaries[mode][str(h)]=dict(fill_rows=len(fills),observed_markouts=len(rows),games=len(grouped),
                    maker_contracts=total,covered_contracts=volume,contract_coverage_fraction=volume/total if total else None,
                    adverse_movement_contract_fraction=sum(r['size'] for r in rows if r['midpoint_change_cents']<-1e-7)/volume if volume else None,
                    equal_game_mean_midpoint_change_cents=statistics.mean(means) if means else None,**weighted)
    result=dict(evidence='31_PREVIOUSLY_EXAMINED_GAMES_DEVELOPMENT_ONLY_MINUTE_RESOLUTION',
        summaries=summaries,notes=['Conditional on previous hypothetical maker fills; policies have different fill selections.',
            'Midpoint valuation is not an executable liquidation price or completed net profit.',
            'Missing or pre-fill-only future candles are excluded and coverage is reported.',
            'Many correlated fills per game; no print-level significance claim or filter tuning.'])
    (ROOT/'results/historical_markout_summary.json').write_text(json.dumps(result,indent=2))
    (ROOT/'results/historical_markout_per_game.json').write_text(json.dumps(per_game,indent=2))
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--extract-from',type=Path);args=p.parse_args();main(args.extract_from)
