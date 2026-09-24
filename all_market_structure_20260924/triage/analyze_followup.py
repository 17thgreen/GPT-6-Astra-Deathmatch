import json,datetime,hashlib
from pathlib import Path
from decimal import Decimal
from mathcore import basis,side_depth,dec
ROOT=Path(__file__).resolve().parent
def stamp(s):return datetime.datetime.fromisoformat(s.replace('Z','+00:00')).timestamp()
def read(n):
    r=json.loads((ROOT/'followup_capture'/f'{n}.json').read_text())
    if r['status']!=200 or r['error']:return r,None
    try:return r,json.loads(r['raw'])
    except json.JSONDecodeError:return r,None
def main():
    for n,h in json.loads((ROOT/'FOLLOWUP_FREEZE.json').read_text()).items():assert hashlib.sha256((ROOT/n).read_bytes()).hexdigest()==h
    out={'basis':[],'reward_gap':[],'realized_pnl':None}
    program=next(x for x in json.loads((ROOT/'PANEL.json').read_text())['programs'] if x['market_ticker']=='KXAAAGASDFL-26SEP24-4.4400')
    for rnd in [1,2]:
        mr,md=read(f'{rnd}_margin');mapping={m['ticker']:m for m in md['markets']} if md else {}
        for asset,key in [('BTC','XXBTZUSD'),('ETH','XETHZUSD'),('SOL','SOLUSD')]:
            pr,p=read(f'{rnd}_{asset}_kalshi');sr,s=read(f'{rnd}_{asset}_kraken');m=mapping.get('KX'+asset+'PERP')
            row={'round':rnd,'asset':asset,'status':'UNSCORED','timeliness_admitted':False}
            if p is None or s is None or m is None:row['reason']='missing_usable_source'
            elif s.get('error') or key not in s.get('result',{}):row['reason']='kraken_error_or_pair_mapping'
            elif m['status']!='active':row['reason']='inactive'
            else:
                try:
                    row['calculation']=basis(p,s['result'][key],m['contract_size'],m['underlying_multiplier'])
                    row['status']='DESCRIPTIVE_ENTRY_BASIS_ONLY';row['receipt_skew_ms']=abs(pr['received_monotonic_ns']-sr['received_monotonic_ns'])/1e6
                    row['book_source_ages']='unverified; Kraken level times are not whole-book snapshot times'
                except (KeyError,ValueError,TypeError) as e:row['reason']='schema_'+type(e).__name__
            out['basis'].append(row)
        br,b=read(f'{rnd}_gap_book');mr,md=read(f'{rnd}_gap_metadata');row={'round':rnd,'scenario_valid':False}
        if b and md:
            m=md['market'];book=b['orderbook_fp'];q=dec(program['target_size_fp']);price=Decimal('.01');now=br['received_ns']/1e9
            yes=side_depth(book['yes_dollars'],q);no=side_depth(book['no_dollars'],q)
            no_bid=max((dec(p) for p,n in book['no_dollars'] if dec(n)>0),default=Decimal(0))
            tick_ok=any(dec(r['start'])<=price<dec(r['end']) and (price-dec(r['start']))%dec(r['step'])==0 for r in m.get('price_ranges',[]))
            tests={'yes_empty':yes['total_depth']==0,'no_target_met':no['target_met'],'would_rest':price+no_bid<1,'tick_valid':tick_ok,
             'listed_program_active':stamp(program['start_date'])<=now<stamp(program['end_date']),
             'market_open':m['status']=='active' and now<stamp(m['close_time'])}
            row['checks']=tests;row['scenario_valid']=all(tests.values());row['received_ns']=br['received_ns']
            if row['scenario_valid']:
                remaining=dec(max(0,min(stamp(program['end_date']),stamp(m['close_time']))-now))/3600
                rate=dec(program['pool_dollars_per_hour'])/2;principal=q*price
                row.update(hypothetical_quantity=q,hypothetical_price=price,principal_at_risk=principal,ideal_share=Decimal('.5'),
                 ideal_reward_dollars_per_hour=rate,remaining_hours=remaining,ideal_remaining_gross_reward=rate*remaining,
                 time_hours_to_match_full_principal=principal/rate,fees='not included; account-specific',expected_profit=None)
        out['reward_gap'].append(row)
    (ROOT/'FOLLOWUP_RESULTS.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
    print(json.dumps(out,indent=2,default=str))
if __name__=='__main__':main()
