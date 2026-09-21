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
    for mapping in [frozen['sha256'],read('BASELINE_HASHES.json')]:
        for name,digest in mapping.items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,name
    for name,digest in read('inputs/manifest.json')['sha256'].items():assert hashlib.sha256((ROOT/'inputs'/name).read_bytes()).hexdigest()==digest,name
    summary=read('results/experiment_summary.json');scenarios=summary['scenarios'];assert len(scenarios)==16 and not summary.get('failures')
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
        assert initial==5000 and result['config']['exposure_cap']==250 and result['config']['assumed_exit_depth']==250
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
        funding=dict(rebalances=0,shortfall_rebalances=0,empty_pair_sets=0,total_requested=0.,total_unfunded=0.,peak_shortfall=0.,protected_cash_sum=0.)
        for d in rows(name,'decisions'):
            decisions+=1
            if d['kind']=='allocation':
                assert sum(d['allocations'].values())<=max(0,d['cash']-d['protected'])+1e-6
                requested=sum(rank['capital'] for rank in d['ranks']);funded=sum(d['allocations'].values())
                shortfall=max(0,requested-funded)
                funding['rebalances']+=1;funding['shortfall_rebalances']+=shortfall>1e-6
                funding['empty_pair_sets']+=not d['ranks'];funding['total_requested']+=requested
                funding['total_unfunded']+=shortfall;funding['peak_shortfall']=max(funding['peak_shortfall'],shortfall)
                funding['protected_cash_sum']+=d['protected']
                factors=result['factors']
                close(d['protected'],d['offset_cash_need'] if factors['protection'] else 0)
                for rank in d['ranks']:
                    if result['arm']!='allocator_off':assert rank['score']>=0
                    if factors['flow']:assert rank['has_observed_flow']
                    if not factors['ranking']:assert rank['adjusted']==1
                    if rank['has_observed_flow']:
                        assert rank['wait_seconds']>0 and rank['lost_queue_wait_seconds']>=0
                        if result['arm']!='allocator_off':assert rank['score']>0
                    else:
                        assert not factors['flow'] and rank['score']==0 and rank['wait_seconds'] is None
            elif d['kind']=='inventory_target':
                assert 0<=d['target']<=250 and d['other_reserved']>=0
                direction=markets[d['key'][0]]['direction']*(1 if d['key'][1]=='yes' else -1)
                assert d['quantity']<=max(0,d['target']-direction*d['inventory']-d['other_reserved'])+1e-7
        assert decisions==result['decision_records']
        checked.append(dict(scenario=name,fills=count,orders=len(order_records),decisions=decisions,passed=True,funding_diagnostics=funding))
    regressions={}
    for name,reference in read('Q6_REFERENCES.json').items():
        old=reference['summary'];new=scenarios[name]
        fields=['completed_strategy_pnl','maker_contracts','taker_contracts','unhedged_contract_hours','max_reserved_cash','min_cash']
        differences={k:new[k]-old[k] for k in fields};assert all(abs(v)<1e-7 for v in differences.values())
        hashes={suffix:hashlib.sha256(gzip.decompress((ROOT/'results'/f'{name}_{suffix}.jsonl.gz').read_bytes())).hexdigest() for suffix in ['fills','orders']}
        assert hashes==reference['ledger_uncompressed_sha256'],name
        regressions[name]=dict(differences=differences,exact_ledger_hashes_match=True)
    assert len(regressions)==8
    guard_diagnostics={}
    for name,result in scenarios.items():
        count=rejects=0
        reasons=defaultdict(int)
        for d in rows(name,'pairs'):
            count+=1;selected=[c for c in d['candidates'] if list(c['key']) in d['chosen']]
            margin=1-sum(c['cost'] for c in selected)-.0002-2*float(result['config']['balance_precision'])/result['config']['order_size'] if len(selected)==2 and {c['direction'] for c in selected}=={-1,1} else None
            if margin is None:assert d['margin'] is None
            else:close(margin,d['margin'],1e-12)
            passed=margin is not None and margin>0
            assert d['price_check_passes']==passed
            if not passed:rejects+=1;reasons[d['reason']]+=1
            if result['arm']=='router_on' and not passed:
                for key in d['allowed']:
                    c=next(c for c in selected if list(c['key'])==key)
                    assert c['direction']*d['inventory']<0
                    qty=d['offset_quantities']['/'.join(key)]
                    room=max(0,abs(d['inventory'])-d['other_pending_offsets']['/'.join(key)])
                    assert .01<=qty<=min(c['wanted'],room)+1e-8
            elif result['arm']=='allocator_on':assert d['budget_eligible']==passed
            elif result['arm']=='allocator_off':assert d['budget_eligible']==(len(selected)==2)
        assert count==result['pair_diagnostics']
        guard_diagnostics[name]=dict(checks=count,nonpassing_checks=rejects,reasons=dict(reasons))
    out=dict(all_checks_passed=True,cases=checked,q6_regressions=regressions,guard_diagnostics=guard_diagnostics,
             caveat='Accounting and exact reference reproduction do not verify historical queue positions or executable fills.')
    (ROOT/'results/verification.json').write_text(json.dumps(out,indent=2));print('PASS all 16 ledgers, per-fill fees, decision budgets, guard controls, frozen hashes and 8 exact Q6 ledger regressions')

if __name__=='__main__':main()
