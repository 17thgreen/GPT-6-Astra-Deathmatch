import gzip
import json
from dataclasses import replace
from pathlib import Path
from extend import ROOT, sha, save, write_rows
from inputs import load
from clock_policy import ClockRouter, Config
from metrics import efficiencies, inventory_cost_hours


class PairCounter:
    def __init__(self):self.count=self.rejections=0
    def append(self,row):
        self.count+=1
        self.rejections+=not row['price_check_passes']


def check_freeze():
    for name,digest in json.loads((ROOT/'FROZEN_REPLAY.json').read_text())['sha256'].items():
        if sha(ROOT/name)!=digest:raise ValueError('Frozen source/input mismatch: '+name)


def main():
    check_freeze();tape,all_markets,audit=load()
    output=ROOT/'results';output.mkdir(exist_ok=True)
    if (output/'summary.json').exists():raise ValueError('Existing M3 outcomes; no overwrite')
    summary=dict(scenarios={},failures={},status='REUSED_DEVELOPMENT_CLOCK_SENSITIVITY_NOT_PROMOTION')
    save(output/'summary.json',summary)
    for sport in ('NCAAF','WNBA'):
        markets={t:m for t,m in all_markets.items() if m['series']=='KX'+sport+'GAME'}
        records=[r for r in tape if r['ticker'] in markets]
        for cutoff in (180,30):
            for profile in ('nfl','constant'):
                for queue in (3300,10000):
                    for delay in (.25,5):
                        name=f'{sport}_t{cutoff}_{profile}_q{queue}_d{delay:g}'
                        try:
                            cfg=replace(Config(),queue_early=queue,quote_source='candles',liquidation_lead_seconds=300,
                                cancel_delay_seconds=delay,order_delay_seconds=delay)
                            engine=ClockRouter(markets,cfg,cutoff,profile)
                            engine.pair_records=PairCounter()
                            end=max(m['kickoff']-cutoff*60 for m in markets.values())+300
                            start=min(max(m['listed_at'],m['kickoff']-604800) for m in markets.values())
                            for row in records:
                                if row['at']>end:break
                                (engine.on_quote if row.get('kind')=='quote' else engine.on_trade)(row)
                            result=engine.finish(end)
                            result.update(scenario=name,sport=sport,cutoff_minutes=cutoff,queue_profile=profile,
                                actual_schedules=markets,engine_clock_anchors={t:m['kickoff'] for t,m in engine.markets.items()},
                                evidence=summary['status'],pair_checks=engine.pair_records.count,
                                pair_rejections=engine.pair_records.rejections,
                                sport_cashflows={'KX'+sport+'GAME':sum(g['cashflow'] for g in result['per_game'])})
                            result['efficiency']=efficiencies(result,(end-300-start)/86400)
                            result['inventory_cost_hours']=inventory_cost_hours(engine.fills,end)
                            write_rows(output/f'{name}_fills.jsonl.gz',engine.fills)
                            write_rows(output/f'{name}_orders.jsonl.gz',engine.order_records.values())
                            save(output/f'{name}.json',result);summary['scenarios'][name]=result
                            print(name, 'net', result['completed_strategy_pnl'],'residual',result['unresolved_contracts'],flush=True)
                        except Exception as error:
                            summary['failures'][name]=dict(error=repr(error),completed_strategy_pnl=None)
                            print(name,'FAILED',repr(error),flush=True)
                        save(output/'summary.json',summary)
    check_freeze()
    if summary['failures']:raise RuntimeError('M3 failures retained')


if __name__=='__main__':main()
