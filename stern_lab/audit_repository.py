"""Reproduce the committed ledger summary and a verified scalar-settlement correction.

Requires an existing local repository checkout/source snapshot with the pinned artifact.
Does not overwrite repository files. No inference about the rest of the tape is made.
"""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd

REL='artifacts/experiments/inplay_criteria_20260921T033123_b0fb2e/per_game.csv'
EXPECTED='297029ac23371851eaddfc18704984faca84e41fc3f4a58430634e2afb73e2d2'

def metrics(d):
    rng=np.random.default_rng(20260920)
    b=np.array([rng.choice(d.roi.to_numpy(),len(d),replace=True).mean() for _ in range(10000)])
    return dict(games=len(d),tickets=int(d.tickets.sum()),pnl=float(d.pnl.sum()),
                dollar_roi=float(d.pnl.sum()/d.cost.sum()),mean_game_roi=float(d.roi.mean()),
                median_game_roi=float(d.roi.median()),wins=int((d.pnl>0).sum()),
                top3_profit_share=float(d.pnl.nlargest(3).sum()/d.pnl.sum()),
                game_bootstrap_ci95=np.quantile(b,[.025,.975]).tolist())

def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True)
    p.add_argument('--out',type=Path,default=Path('audit_results'));args=p.parse_args()
    path=args.repo/REL
    if hashlib.sha256(path.read_bytes()).hexdigest()!=EXPECTED:
        raise ValueError('Ledger differs from reviewed commit; re-ground rather than silently continuing')
    d=pd.read_csv(path);result={'original':metrics(d)}
    source=json.loads(Path(__file__).with_name('results').joinpath('tied_market_source.json').read_text())
    m=source['response']['market']
    if m['ticker']!='KXNFLGAME-25SEP28GBDAL-DAL' or m['settlement_value_dollars']!='0.5000':
        raise ValueError('Unexpected settlement evidence')
    i=d.index[d.gid=='2025_04_GB_DAL']
    if len(i)!=1:raise ValueError('Expected exactly one tied-game row')
    i=i[0];before=float(d.loc[i,'pnl'])
    d.loc[i,'pnl']=.5*d.loc[i,'tickets']-d.loc[i,'cost']
    d.loc[i,'roi']=d.loc[i,'pnl']/d.loc[i,'cost']
    result['corrected_one_tie']=metrics(d)
    result['correction']={'old_pnl':before,'new_pnl':float(d.loc[i,'pnl']),
                          'status':'PARTIAL_CORRECTION_NOT_FULL_TAPE_REPLAY'}
    args.out.mkdir(parents=True,exist_ok=True)
    (args.out/'reproduction.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
