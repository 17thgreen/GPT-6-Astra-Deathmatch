"""Independent order/fill ledger reconciliation and frozen-source regression."""
import gzip,hashlib,json,math
from collections import defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parent


def read(name):return json.loads((ROOT/name).read_text())


def main():
    frozen=read('FROZEN_EXPERIMENT.json')
    for mapping in [frozen['sha256'],read('BASELINE_HASHES.json')]:
        for name,digest in mapping.items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,name
    manifest=read('inputs/manifest.json')
    for name,digest in manifest['sha256'].items():assert hashlib.sha256((ROOT/'inputs'/name).read_bytes()).hexdigest()==digest,name
    s=read('results/experiment_summary.json')['scenarios'];assert len(s)==52
    markets=read('inputs/markets.json');weeks=read('inputs/week_membership.json');checked=[]
    for name,r in s.items():
        assert read('results/'+name+'.json')==r,name
        cash=5000.;inventory=defaultdict(float);flows=defaultdict(float);fees=0.;volume=0.;paired=0.;count=0;last=-math.inf
        order_fills=defaultdict(float)
        with gzip.open(ROOT/'results'/f'{name}_fills.jsonl.gz','rt') as f:
            for line in f:
                row=json.loads(line);count+=1
                assert row['at']>=last;last=row['at']
                assert row['size']>0 and 0<row['price']<1 and row['fee']>=0
                event=row['event'];before=inventory[event]
                expected=min(abs(before),row['size']) if before*row['direction']<0 else 0
                assert abs(expected-row['paired'])<1e-6
                delta=row['paired']-row['price']*row['size']-row['fee'];cash+=delta;flows[event]+=delta
                inventory[event]+=row['direction']*row['size'];volume+=row['size'];paired+=row['paired'];fees+=row['fee']
                assert abs(cash-row['cash_after'])<1e-6 and cash>=-1e-7
                assert abs(inventory[event]-row['inventory_after'])<1e-6
                assert abs(inventory[event])<=r['config']['exposure_cap']+1e-6
                if row['kind']=='maker':
                    assert row['at']<markets[row['ticker']]['kickoff']-10800
                    order_fills[row['order_id']]+=row['size']
        residual=sum(abs(q) for q in inventory.values())
        assert count==r['fills'] and abs(residual-r['unresolved_contracts'])<1e-6
        assert abs(fees-r['metrics'].get('fees',0))<1e-6
        assert abs(volume-r['maker_contracts']-r['taker_contracts'])<1e-5
        assert abs(volume-2*paired-residual)<1e-5
        assert r['config']['assumed_exit_depth']==250 and r['config']['starting_cash']==5000
        if r['completed_strategy_pnl'] is not None:assert residual<.009 and abs(cash-5000-r['completed_strategy_pnl'])<1e-6
        else:
            assert residual>=.009
            assert abs(r['terminal_payout_bounds'][0]-(cash-5000))<1e-6
            assert abs(r['terminal_payout_bounds'][1]-(cash-5000+residual))<1e-6
        for game in r['per_game']:
            assert abs(game['cashflow']-flows[game['event']])<1e-6
            assert abs(game['net_inventory']-inventory[game['event']])<1e-6
        for week,pnl in r['week_contributions'].items():assert abs(pnl-sum(v for event,v in flows.items() if weeks[event]==week))<1e-6
        records=[]
        with gzip.open(ROOT/'results'/f'{name}_orders.jsonl.gz','rt') as f:
            for line in f:
                order=json.loads(line);records.append(order)
                assert order['submitted_quantity']<=r['config']['order_size']+1e-7
                assert abs(order_fills.pop(order['order_id'],0)-order['filled_quantity'])<1e-6
                assert order['filled_quantity']<=order['submitted_quantity']+1e-6
                if not order['entry_window_open']:
                    assert order['direction']*order['inventory_at_submission']<0
        assert not order_fills
        assert len(records)==r['submitted_maker_orders']
        assert sum(o['filled_quantity']>=o['submitted_quantity']-.009 for o in records)==r['fully_filled_submitted_orders']
        checked.append(dict(scenario=name,passed=True,fills=count,orders=len(records),unresolved_contracts=residual))
    references=read('Q2_REGRESSION_REFERENCE.json');regressions={}
    for old_name,old in references.items():
        q=int(old['config']['queue_early']);new=s[f'q{q}_s250_full_route_cap250']
        fields=['completed_strategy_pnl','maker_contracts','taker_contracts','unhedged_contract_hours','max_reserved_cash','min_cash']
        differences={k:new[k]-old[k] for k in fields};assert all(abs(v)<1e-7 for v in differences.values())
        regressions[str(q)]=differences
    result=dict(all_checks_passed=True,cases=checked,q2_regression_differences=regressions,
        note='Internal accounting and data integrity checks; hypothetical historical queues/exits remain unverified.')
    (ROOT/'results/verification.json').write_text(json.dumps(result,indent=2))
    print('PASS 52 order/fill ledgers, input/frozen hashes, and both Q2 regressions')


if __name__=='__main__':main()
