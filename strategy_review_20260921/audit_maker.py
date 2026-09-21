"""Reproduce arithmetic from the committed artifact; no trade-tape replay or profit claim."""
from pathlib import Path
import hashlib
import json
import numpy as np
import pandas as pd

ROOT=Path(__file__).parent
SOURCE=ROOT/'repo/artifacts/experiments/diagnostics/paper_mm_validation.json'
REF='f4ad8e8bfba2db2a5e8e1ecf80f935424f60f175'


def statistics(g):
    contracts=float(g.contracts.sum()); pnl=float(g.pnl.sum())
    return dict(games=len(g),games_with_fills=int((g.fills>0).sum()),pnl=pnl,
                contracts=contracts,contract_weighted_cents=100*pnl/contracts if contracts else None,
                mean_game_ratio_cents=float(g.cents_per_contract.mean()) if g.cents_per_contract.notna().any() else None,
                mean_game_pnl=float(g.pnl.mean()),median_game_pnl=float(g.pnl.median()),
                positive_games=int((g.pnl>0).sum()),negative_games=int((g.pnl<0).sum()))


def clustered(g):
    # Use official NFL season/week; a late Sunday UTC Monday belongs to the same league week.
    frame=g.assign(block=g.season.astype(str)+'-'+g.week.astype(str))
    blocks=frame.groupby('block').agg(pnl=('pnl','sum'),contracts=('contracts','sum'),games=('pnl','size'))
    if len(blocks)<5:
        return {'blocks':len(blocks),'status':'INSUFFICIENT_BLOCKS_FOR_RELIABLE_INTERVAL',
                'block_totals':blocks.reset_index().to_dict('records')}
    a=blocks.to_numpy();rng=np.random.default_rng(20260921)
    draws=a[rng.integers(0,len(a),(5000,len(a)))].sum(axis=1)
    return {'blocks':len(blocks),'status':'DESCRIPTIVE_BOOTSTRAP_ONLY',
            'mean_game_pnl_ci95':np.quantile(draws[:,0]/draws[:,2],[.025,.975]).tolist(),
            'contract_weighted_cents_ci95':np.quantile(100*draws[:,0]/draws[:,1],[.025,.975]).tolist()}


def main():
    raw=json.loads(SOURCE.read_text());asof=pd.Timestamp(raw['generated_at_utc'])
    out={'repo_commit':REF,'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
         'artifact_time':str(asof),'artifact_policy':raw['policy_fingerprint'],
         'scope':'Arithmetic audit of saved simulated fills; not a corrected replay or achieved return',
         'scenarios':{}}
    for name,s in raw['scenarios'].items():
        d=pd.DataFrame(s['per_game']);d['kickoff']=pd.to_datetime(d.kickoff,utc=True)
        if 'week' in d.columns:
            d=d.rename(columns={'week':'source_week_label'})
        schedule=pd.read_csv(ROOT/'inputs/nfl_schedule_keys.csv')
        d=d.merge(schedule[['event','season','week']],on='event',how='left',validate='one_to_one')
        if d[['season','week']].isna().any().any():raise ValueError('Unmatched NFL schedule key')
        d['window_complete_at_artifact']=d.kickoff-pd.Timedelta(hours=3)<=asof
        groups={}
        for season,g in d.groupby('season'):
            groups[str(season)]={'all':statistics(g),'clustered_all':clustered(g)}
            for status,mask in [('complete',g.window_complete_at_artifact),('still_open',~g.window_complete_at_artifact)]:
                x=g[mask]
                if len(x):groups[str(season)][status]=statistics(x)|{'clustered':clustered(x)}
        iso=d.kickoff.dt.isocalendar()
        groups['block_construction']={
            'reported':s['block_bootstrap_over_weeks']['blocks'],
            'year_week_including_all_games':len(d.assign(block=iso.year.astype(str)+'-'+iso.week.astype(str)).groupby('block')),
            'league_season_week_including_all_games':len(d.groupby(['season','week'])),
            'problem':'Original groups only by week number across years and excludes blocks with fewer than three games.'}
        out['scenarios'][name]=groups
        d.to_csv(ROOT/f'results/{name}_audited_games.csv',index=False)
    q=json.loads((ROOT/'repo/artifacts/experiments/diagnostics/kalshi_queue_depth_by_series.json').read_text())['series']['KXNFLGAME']
    thin=q['pre_game_later']['median_best_level_contracts'];thick=q['pre_game_same_day']['median_best_level_contracts']
    out['queue_bucket_issue']={'3_to_24h_applied_queue':thin,'under_12h_profile_queue':thick,
        'ratio':thick/thin,'sample_time':'2026-09-20T18:48:55.379670+00:00',
        'note':'The window runner chooses one depth at 13.5h and applies it throughout 3–24h; both depths are snapshot assumptions.'}
    (ROOT/'results/artifact_audit.json').write_text(json.dumps(out,indent=2,allow_nan=False))
    for name,s in out['scenarios'].items():
        print(name,json.dumps(s['2026'],indent=2))
    print('queue issue',out['queue_bucket_issue'])


if __name__=='__main__':
    (ROOT/'results').mkdir(exist_ok=True)
    main()
