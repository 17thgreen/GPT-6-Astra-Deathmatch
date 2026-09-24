import json,datetime,hashlib
from pathlib import Path
from decimal import Decimal
from mathcore import basis,side_depth,volume_bound,dec
ROOT=Path(__file__).resolve().parent
def stamp(s):return datetime.datetime.fromisoformat(s.replace('Z','+00:00')).timestamp()
def read(name):
    r=json.loads((ROOT/'capture'/f'{name}.json').read_text())
    if r['status']!=200 or r['error']:return r,None
    try:return r,json.loads(r['raw'])
    except json.JSONDecodeError:
        r['analysis_error']='non_json_response'
        return r,None
def main():
    for n,h in json.loads((ROOT/'FREEZE.json').read_text()).items():assert hashlib.sha256((ROOT/n).read_bytes()).hexdigest()==h,n
    panel=json.loads((ROOT/'PANEL.json').read_text());basis_rows=[];reward_rows=[]
    for rnd in [1,2,3]:
        mr,md=read(f'{rnd}_margin');mapping={x['ticker']:x for x in md['markets']} if md else {}
        for asset,ticker in panel['perps'].items():
            kr,k=read(f'{rnd}_{asset}_kalshi');cr,c=read(f'{rnd}_{asset}_coinbase');m=mapping.get(ticker)
            r={'round':rnd,'asset':asset,'ticker':ticker,'status':'UNSCORED'}
            if m is None or k is None or c is None:r['reason']='missing_successful_source'
            elif m.get('status')!='active':r['reason']='inactive'
            else:
                try:
                    r['calculation']=basis(k,c,m['contract_size'],m['underlying_multiplier'])
                    r['status']='DESCRIPTIVE_ONLY'
                    r['receipt_skew_ms']=abs(kr['received_monotonic_ns']-cr['received_monotonic_ns'])/1e6
                    r['contract_size']=m['contract_size'];r['underlying_multiplier']=m['underlying_multiplier']
                    r['coinbase_source_time']=c.get('time')
                    r['coinbase_age_seconds']=cr['received_ns']/1e9-stamp(c['time']) if c.get('time') else None
                    reference=m.get('reference_price') or {}
                    r['kalshi_reference_age_seconds']=mr['received_ns']/1e9-reference['ts_ms']/1000 if 'ts_ms' in reference else None
                    r['kalshi_book_source_age']='UNVERIFIED'
                    r['timeliness_admitted']=False
                    ages=[r['coinbase_age_seconds'],r['kalshi_reference_age_seconds']]
                    r['timestamp_warning']=any(x is not None and (x>10 or x < -1) for x in ages)
                    r['latency_edge']=None
                except (ValueError,KeyError,TypeError) as e:r['reason']='schema_'+type(e).__name__
            basis_rows.append(r)
    for x in panel['programs']:
        t=x['market_ticker'];mr,md=read(t+'_metadata');br,b=read(t+'_book')
        r={'market':t,'category':x['category'],'program_id':x['id'],'pool_dollars':dec(x['period_reward'])/10000,
           'pool_dollars_per_hour':x['pool_dollars_per_hour'],'target_size':x['target_size_fp'],'discount_factor_bps':x['discount_factor_bps'],
           'program_freshness':'retained AMS-001 definition; current program/account eligibility unverified'}
        received=br['received_ns']/1e9;within=stamp(x['start_date'])<=received<stamp(x['end_date'])
        r['within_listed_window']=within;r['hours_remaining_in_listed_window']=max(0,(stamp(x['end_date'])-received)/3600)
        if md and b:
            try:
                m=md['market'];r['market_status']=m['status'];r['close_time']=m['close_time'];r['market_open_at_receipt']=m['status']=='active' and received<stamp(m['close_time'])
                r['sides']={s:side_depth(b['orderbook_fp'][s+'_dollars'],x['target_size_fp']) for s in ['yes','no']}
                r['depth_condition_met']=all(a['target_met'] for a in r['sides'].values())
                r['snapshot_conditions_met']=r['depth_condition_met'] and r['market_open_at_receipt'] and within
            except (ValueError,KeyError,TypeError) as e:r['error']='schema_'+type(e).__name__
        else:r['error']='request_failed'
        rate=dec(x['pool_dollars_per_hour'])
        r['hypothetical_budget_per_hour']={str(share):{str(qual):rate*dec(share)*dec(qual) for qual in ['1','.5']} for share in ['.01','.05','.10']}
        r['expected_reward']=None;reward_rows.append(r)
    root=(Decimal(1)-(Decimal(1)-4*Decimal('.005')/Decimal('.07')).sqrt())/2
    volume={'multiplier':1,'lower_root':root,'upper_root':1-root,
      'examples':{str(p):volume_bound(p) for p in ['.03','.05','.10','.25','.50','.75','.90','.95','.97']},
      'interpretation':'Within roots, unrounded taker fee alone exceeds maximum reward. No spread or adverse movement needed to fail subsidy-only zero-edge trade.'}
    out={'study':'AMS-003','basis':basis_rows,'liquidity':reward_rows,'volume_bound':volume,'realized_pnl':None}
    (ROOT/'RESULTS.json').write_text(json.dumps(out,default=str,indent=2)+'\n')
    print(json.dumps({'basis':basis_rows,'liquidity':[{k:r.get(k) for k in ['market','category','pool_dollars_per_hour','snapshot_conditions_met','error']} for r in reward_rows],'volume_roots':[str(root),str(1-root)]},default=str,indent=2))
if __name__=='__main__':main()
