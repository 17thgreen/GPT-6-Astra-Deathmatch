"""Recompute financial ledgers without importing the replay accounting engine."""
import gzip,hashlib,json,math
from decimal import Decimal,ROUND_CEILING,ROUND_FLOOR
from collections import defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def read(name):return json.loads((ROOT/name).read_text())
def close(a,b,tol=1e-6):assert abs(a-b)<tol,(a,b)
def rows(name,suffix):
    with gzip.open(ROOT/'results'/f'{name}_{suffix}.jsonl.gz','rt') as f:
        for line in f:yield json.loads(line)

def main():
    frozen=read('FROZEN_EXPERIMENT.json')
    for mapping in [frozen['sha256'],read('FROZEN_CAPITAL_CONTROLS.json')['sha256'],read('FROZEN_ALLOCATION_DIAGNOSTIC.json')['sha256'],read('BASELINE_HASHES.json')]:
        for name,digest in mapping.items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,name
    for name,digest in read('inputs/manifest.json')['sha256'].items():assert hashlib.sha256((ROOT/'inputs'/name).read_bytes()).hexdigest()==digest,name
    summary=read('results/experiment_summary.json');scenarios=summary['scenarios'];assert len(scenarios)==16
    scenarios.update(read('results/capital_controls_summary.json')['scenarios']);assert len(scenarios)==19
    scenarios.update(read('results/allocation_diagnostic_summary.json')['scenarios']);assert len(scenarios)==21
    markets=read('inputs/markets.json');weeks=read('inputs/week_membership.json');checked=[]
    for name,result in scenarios.items():
        assert read('results/'+name+'.json')==result
        initial=result['config']['starting_cash'];cash=float(initial);inv=defaultdict(float);flow=defaultdict(float);maker=taker=fee_total=pairs=0.;last=-math.inf;count=0
        order_fills=defaultdict(float);remainders=defaultdict(Decimal);exit_qty=defaultdict(float)
        order_records={o['order_id']:o for o in rows(name,'orders')}
        for f in rows(name,'fills'):
            count+=1;assert f['at']>=last;last=f['at'];assert f['size']>0 and 0<f['price']<1
            assert f['event']==markets[f['ticker']]['event']
            direction=markets[f['ticker']]['direction']*(1 if f['outcome']=='yes' else -1)
            assert direction==f['direction'];event=f['event']
            expected=min(abs(inv[event]),f['size']) if inv[event]*direction<0 else 0
            close(expected,f['paired'])
            # Independent implementation of the documented fixed-point fee arithmetic.
            precision=Decimal(result['config']['balance_precision']);p=Decimal(str(f['price'])).quantize(Decimal('.0001'));q=Decimal(str(f['size'])).quantize(Decimal('.01'))
            coefficient=Decimal(str(result['config']['maker_coefficient'] if f['kind']=='maker' else result['config']['taker_coefficient']))
            nominal=(coefficient*q*p*(1-p)).quantize(Decimal('.000001'),rounding=ROUND_CEILING)
            debit=(-p*q-nominal)/precision
            aligned=debit.to_integral_value(rounding=ROUND_FLOOR)*precision
            rounding=-p*q-nominal-aligned
            identity=f['order_id'] if f['kind']=='maker' else ('taker',count)
            remainder=remainders[identity]+rounding
            rebate=min((remainder/precision).to_integral_value(rounding=ROUND_FLOOR)*precision,
                       ((nominal+rounding)/precision).to_integral_value(rounding=ROUND_FLOOR)*precision)
            remainders[identity]=remainder-rebate
            close(float(nominal+rounding-rebate),f['fee'],1e-8)
            change=expected-f['price']*f['size']-f['fee'];cash+=change;flow[event]+=change
            inv[event]+=direction*f['size'];fee_total+=f['fee'];pairs+=expected
            close(cash,f['cash_after']);close(inv[event],f['inventory_after']);assert cash>=-1e-7
            assert abs(inv[event])<=250+1e-6
            if f['kind']=='maker':
                maker+=f['size'];order_fills[f['order_id']]+=f['size'];o=order_records[f['order_id']]
                assert f['at']>=o['active_at'];assert f['at']<markets[f['ticker']]['kickoff']-10800
                assert f['price']==o['price'] and f['ticker']==o['ticker'] and f['outcome']==o['outcome']
                if o['cancel_requested_at'] is not None:assert f['at']<o['cancel_requested_at']+result['config']['cancel_delay_seconds']+1e-8
            else:taker+=f['size'];exit_qty[event]+=f['size']
        residual=sum(abs(v) for v in inv.values())
        assert count==result['fills'];close(maker,result['maker_contracts'],1e-5);close(taker,result['taker_contracts'],1e-5)
        close(fee_total,result['metrics'].get('fees',0));close(residual,result['unresolved_contracts']);close(maker+taker-2*pairs,residual,1e-5)
        assert max(exit_qty.values(),default=0)<=250+1e-6
        assert initial in [1000,4000,5000] and result['config']['exposure_cap']==250 and result['config']['assumed_exit_depth']==250
        if result['completed_strategy_pnl'] is not None:assert residual<.009;close(cash-initial,result['completed_strategy_pnl'])
        else:assert residual>=.009
        close(result['terminal_payout_bounds'][0],cash-initial);close(result['terminal_payout_bounds'][1],cash-initial+residual)
        for g in result['per_game']:close(g['cashflow'],flow[g['event']]);close(g['net_inventory'],inv[g['event']])
        for week,pnl in result['week_contributions'].items():close(pnl,sum(v for e,v in flow.items() if weeks[e]==week))
        for identity,o in order_records.items():
            assert o['submitted_quantity']<=250+1e-8 and o['filled_quantity']<=o['submitted_quantity']+1e-6
            close(o['filled_quantity'],order_fills.pop(identity,0));assert o['entry_window_open']
        assert not order_fills and len(order_records)==result['submitted_maker_orders']
        decisions=0
        for d in rows(name,'decisions'):
            decisions+=1
            if d['kind']=='allocation':
                assert sum(d['allocations'].values())<=max(0,d['cash']-d['protected'])+1e-6
                for rank in d['ranks']:assert rank['score']>0 and rank['wait_seconds']>0 and rank['lost_queue_wait_seconds']>=0
            elif d['kind']=='inventory_target':
                assert 0<=d['target']<=250 and d['other_reserved']>=0
                direction=markets[d['key'][0]]['direction']*(1 if d['key'][1]=='yes' else -1)
                assert d['quantity']<=max(0,d['target']-direction*d['inventory']-d['other_reserved'])+1e-7
        assert decisions==result['decision_records']
        checked.append(dict(scenario=name,fills=count,orders=len(order_records),decisions=decisions,passed=True))
    regressions={}
    for old in read('Q2_REGRESSION_REFERENCE.json').values():
        q=int(old['config']['queue_early']);new=scenarios[f'q{q}_d0.25_baseline']
        fields=['completed_strategy_pnl','maker_contracts','taker_contracts','unhedged_contract_hours','max_reserved_cash','min_cash']
        differences={k:new[k]-old[k] for k in fields};assert all(abs(v)<1e-7 for v in differences.values());regressions[str(q)]=differences
    out=dict(all_checks_passed=True,cases=checked,q2_regressions=regressions,
             caveat='Independent accounting checks do not verify historical queue positions or executable fills.')
    (ROOT/'results/verification.json').write_text(json.dumps(out,indent=2));print('PASS all 21 ledgers, per-fill fees, decision budgets, frozen hashes and Q2 regressions')

if __name__=='__main__':main()
