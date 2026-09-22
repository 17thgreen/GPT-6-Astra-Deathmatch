"""Normalize existing records without claiming matched cohorts or reinvestment."""
import json
from pathlib import Path
from metrics import efficiencies
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parent


def main():
    rows=[]
    for sport in ('NFL','NCAAF','WNBA'):
        for queue in (3300,10000):
            if sport=='NFL':
                path=REPO/'nfl_pair_price_lab_20260921/results'/f'q{queue}_d0.25_router_on.json'
                markets=json.loads((REPO/'nfl_pair_price_lab_20260921/inputs/markets.json').read_text())
                start=min(m['kickoff']-604800 for m in markets.values())
                end=max(m['kickoff']-10800 for m in markets.values())
                span_label='Nominal seven-day NFL window; per-market historical listing receipt not verified'
            else:
                path=REPO/'cross_sport_replay_20260922/results'/f'{sport}_q{queue}_d0.25.json'
                capture=json.loads((REPO/'cross_sport_replay_20260922/CAPTURE.json').read_text())
                markets=[m for m in capture['markets'] if m['series']=='KX'+sport+'GAME']
                start=min(m['start'] for m in markets);end=max(m['kickoff']-10800 for m in markets)
                span_label='Listing-bounded reconstructed market window'
            result=json.loads(path.read_text())
            rows.append(dict(sport=sport,queue=queue,games=len(result['per_game']),
                net=result['completed_strategy_pnl'],passive_pairing_fraction=result['passive_pairing_fraction'],
                median_pairing_minutes=result['pair_holding_time_seconds'].get('weighted_median',0)/60
                    if result['pair_holding_time_seconds'].get('weighted_median') is not None else None,
                source=str(path.relative_to(REPO)),window_start=start,window_end=end,span_label=span_label,
                **efficiencies(result,(end-start)/86400)))
    out=dict(rows=rows,qualification='Descriptive normalization of unequal cohorts. Initial-cash daily averages are observed span arithmetic, not matched opportunity, invested-capital returns or a compounding forecast.',
             unscored=['NBA','MLB','NHL'])
    (ROOT/'EXISTING_COMPARISON.json').write_text(json.dumps(out,indent=2))
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
