"""Run only the preregistered alternatives, with original-mode exact controls."""
import sys
from dataclasses import replace
from m4_common import ROOT, M3, read, save, sha, write_rows
from m4_data import load_new
from m4_policy import SizeRouter, ClockRouter, Config
from inputs import load as load_development
from metrics import efficiencies, inventory_cost_hours


class PairCounter:
    def __init__(self):
        self.count=self.rejections=0
    def append(self,row):
        self.count+=1
        self.rejections+=not row['price_check_passes']


def check_freeze():
    for name,digest in read(ROOT/'FROZEN_REPLAY.json')['sha256'].items():
        if sha(ROOT/name)!=digest:
            raise ValueError('Frozen source/input mismatch: '+name)


def specifications():
    cases=[]
    for sport in ('NCAAF','MLB'):
        for cutoff in (180,30):
            for profile in ('nfl','constant'):
                for queue in (3300,10000):
                    for delay in (.25,5):
                        cases.append(dict(name=f'{sport}_new_t{cutoff}_{profile}_q{queue}_d{delay:g}',
                            sport=sport,cohort='new',cutoff=cutoff,profile=profile,queue=queue,delay=delay,
                            size=250,complete_first=False))
    for sport in ('NCAAF','WNBA'):
        for size in (25,100,250):
            for mode in ('original','complete_first'):
                for queue in (3300,10000):
                    for delay in (.25,5):
                        cases.append(dict(name=f'{sport}_dev_s{size}_{mode}_q{queue}_d{delay:g}',
                            sport=sport,cohort='development',cutoff=30,profile='constant',queue=queue,
                            delay=delay,size=size,complete_first=mode=='complete_first'))
    return cases


def simulate(case,dataset):
    tape,markets,audit=dataset
    maker,taker=audit['coefficients']
    cfg=replace(Config(),queue_early=case['queue'],quote_source='candles',liquidation_lead_seconds=300,
        order_delay_seconds=case['delay'],cancel_delay_seconds=case['delay'],
        order_size=case['size'],exposure_cap=case['size'],maker_coefficient=maker,taker_coefficient=taker)
    engine=(SizeRouter(markets,cfg,case['complete_first']) if case['cohort']=='development'
            else ClockRouter(markets,cfg,case['cutoff'],case['profile']))
    engine.pair_records=PairCounter()
    start=min(max(m['listed_at'],m['kickoff']-604800) for m in markets.values())
    end=max(m['kickoff']-case['cutoff']*60 for m in markets.values())+300
    for row in tape:
        if row['at']>end:
            break
        (engine.on_quote if row.get('kind')=='quote' else engine.on_trade)(row)
    result=engine.finish(end)
    result.update(scenario=case['name'],specification=case,actual_schedules=markets,
        engine_clock_anchors={t:m['kickoff'] for t,m in engine.markets.items()},
        pair_checks=engine.pair_records.count,pair_rejections=engine.pair_records.rejections,
        sport_cashflows={'KX'+case['sport']+'GAME':sum(g['cashflow'] for g in result['per_game'])},
        input_status=audit['status'],coefficients=audit['coefficients'])
    result['efficiency']=efficiencies(result,(end-300-start)/86400)
    result['inventory_cost_hours']=inventory_cost_hours(engine.fills,end)
    write_rows(ROOT/'results'/f"{case['name']}_fills.jsonl.gz",engine.fills)
    write_rows(ROOT/'results'/f"{case['name']}_orders.jsonl.gz",engine.order_records.values())
    save(ROOT/'results'/f"{case['name']}.json",result)
    return result


def main():
    check_freeze()
    if (ROOT/'results/summary.json').exists():
        raise ValueError('Existing outcomes; no overwrite')
    datasets={};blocked={}
    for sport in ('NCAAF','MLB'):
        try:
            datasets[sport,'new']=load_new('KX'+sport+'GAME')
        except Exception as error:
            blocked[sport]=str(error)
    tape,markets,audit=load_development()
    for sport in ('NCAAF','WNBA'):
        selected={t:m for t,m in markets.items() if m['series']=='KX'+sport+'GAME'}
        datasets[sport,'development']=([r for r in tape if r['ticker'] in selected],selected,
            dict(coefficients=[.0175,.07],status='REUSED_M3_DEVELOPMENT_NOT_HOLDOUT'))
    cases=specifications()
    out=dict(scenarios={},failures={},blocked_sports=blocked,declared_cases=cases,
             evidence='INDEPENDENT_COUNTERFACTUAL_ALTERNATIVES_NOT_CONCURRENT_FLEET')
    save(ROOT/'results/summary.json',out)
    for case in cases:
        name=case['name']
        key=(case['sport'],case['cohort'])
        if key not in datasets:
            out['failures'][name]=dict(blocked=True,error=blocked[case['sport']],completed_strategy_pnl=None)
        else:
            try:
                result=simulate(case,datasets[key]);out['scenarios'][name]=result
                print(name,'net',result['completed_strategy_pnl'],'residual',result['unresolved_contracts'],flush=True)
            except Exception as error:
                out['failures'][name]=dict(error=repr(error),completed_strategy_pnl=None)
                print(name,'FAILED',repr(error),flush=True)
        save(ROOT/'results/summary.json',out)
    check_freeze()
    if out['failures']:
        raise RuntimeError('M4 blocked/failed slots retained')


if __name__=='__main__':
    main()
