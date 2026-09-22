"""Post-outcome M3 contrasts; no policy changes or promotion selection."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent


def main():
    s=json.loads((ROOT/'results/summary.json').read_text())['scenarios']
    contrasts=[]
    for sport in ['NCAAF','WNBA']:
        for profile in ['nfl','constant']:
            for queue in [3300,10000]:
                for delay in [.25,5]:
                    a=s[f'{sport}_t180_{profile}_q{queue}_d{delay:g}']
                    b=s[f'{sport}_t30_{profile}_q{queue}_d{delay:g}']
                    contrasts.append(dict(sport=sport,queue_profile=profile,queue=queue,delay=delay,
                        old_net=a['completed_strategy_pnl'],later_net=b['completed_strategy_pnl'],
                        cutoff_effect=b['completed_strategy_pnl']-a['completed_strategy_pnl'],
                        later_net_without_best_two=sum(sorted(g['cashflow'] for g in b['per_game'])[:-2]),
                        old_passive_completion=a['passive_pairing_fraction'],new_passive_completion=b['passive_pairing_fraction']))
    latency=[dict(scenario=n,slow_minus_fast=r['completed_strategy_pnl']-s[n[:-1]+'0.25']['completed_strategy_pnl'])
             for n,r in s.items() if n.endswith('_d5')]
    result=dict(post_outcome_descriptive=True,production_promotion=False,
        interpretation='Cutoff effects are compared within an identical assumed environment. No queue calibration or market validation follows.',
        cutoff_contrasts=contrasts,latency_contrasts=latency)
    (ROOT/'results/contrasts.json').write_text(json.dumps(result,indent=2))
    print('Wrote 16 within-environment cutoff contrasts and 16 latency contrasts')


if __name__=='__main__':main()
