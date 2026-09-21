"""Capital-only control; explicitly NOT a multi-wallet or multi-bot simulation."""
import hashlib,json,time
from dataclasses import replace
from pathlib import Path
import run_experiment as run
from replay_v2 import Config
from adaptive_policy import AdaptiveReplay,floor_qty
ROOT=Path(__file__).resolve().parent

class CapitalBufferReplay(AdaptiveReplay):
    """Uniform $.02 idle cash buffer, only for these supplemental capital controls."""
    def quote(self,ticker,outcome,price,wanted,now):
        if (ticker,outcome) not in self.orders:
            cost=price+self.cfg.maker_coefficient*price*(1-price)+.0001
            budget=max(0,self.cash-self.reservations()-.02-float(self.cfg.balance_precision))
            wanted=min(wanted,floor_qty(budget/cost))
        return super().quote(ticker,outcome,price,wanted,now)

def main():
    freeze=json.loads((ROOT/'FROZEN_CAPITAL_CONTROLS.json').read_text())
    for name,digest in freeze['sha256'].items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,name
    cohort=run.checked_inputs();out=dict(cohort=cohort,scenarios={})
    for capital in [1000,4000,5000]:
        began=time.monotonic();name=f'q3300_d0.25_baseline_cash{capital}'
        cfg=replace(Config(),starting_cash=capital,queue_early=3300,quote_source='candles',liquidation_lead_seconds=300)
        r=CapitalBufferReplay(run.MARKETS,cfg,'baseline');end=max(m['kickoff']-10800 for m in run.MARKETS.values())+300
        for row in run.EVENTS:
            if row['at']>end:break
            if row.get('kind')=='quote':r.on_quote(row)
            else:r.on_trade(row)
        result=r.finish(end)
        result.update(scenario=name,elapsed_seconds=time.monotonic()-began,evidence='CAPITAL_ONLY_SINGLE_ACCOUNT_NOT_MULTIBOT',extra_idle_cash_buffer=.02)
        result['week_contributions']={w:sum(g['cashflow'] for g in result['per_game'] if run.WEEKS[g['event']]==w) for w in ['week1','week2']}
        ranked=sorted((g['cashflow'] for g in result['per_game']),reverse=True)
        result['pnl_excluding_top_two_games']=sum(ranked[2:]) if result['all_flat'] else None
        for suffix,rows in [('fills',r.fills),('orders',r.order_records.values()),('decisions',r.decisions)]:run.save_rows(ROOT/'results'/f'{name}_{suffix}.jsonl.gz',rows)
        run.atomic_json(ROOT/'results'/f'{name}.json',result);out['scenarios'][name]=result
        run.atomic_json(ROOT/'results/capital_controls_summary.json',out)
        print(name,'pnl',result['completed_strategy_pnl'],'residual',result['unresolved_contracts'],flush=True)
    print('DONE 3 buffered capital controls',flush=True)

if __name__=='__main__':main()
