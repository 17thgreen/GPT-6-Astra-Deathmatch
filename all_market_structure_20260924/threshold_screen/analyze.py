"""Score every preregistered pair and size; never aggregate overlapping trades."""
import json,itertools,collections,statistics,hashlib
from pathlib import Path
from decimal import Decimal
from economics import pair
ROOT=Path(__file__).resolve().parent
def main():
    for n,h in json.loads((ROOT/'FREEZE.json').read_text()).items():
        assert hashlib.sha256((ROOT/n).read_bytes()).hexdigest()==h,n
    rows=[];groups=json.loads((ROOT/'ADMISSION.json').read_text())['groups']
    for g in groups:
        for rnd in [1,2]:
            for low,high in itertools.combinations(g['markets'],2):
                for q in [1,10,100]:
                    row={'series':g['series'],'round':rnd,'low':low['ticker'],'high':high['ticker'],'quantity':q,'status':'UNSCORED'}
                    paths=[ROOT/'books'/f"{rnd}_{m['ticker']}.json" for m in [low,high]]
                    if not all(p.exists() for p in paths):row['reason']='missing_receipt'
                    else:
                        rs=[json.loads(p.read_text()) for p in paths]
                        if any(r['status']!=200 or r['error'] for r in rs):row['reason']='failed_request'
                        elif g['fee_type'] not in ['quadratic','quadratic_with_maker_fees'] or g['fee_multiplier'] is None:row['reason']='unknown_fee'
                        else:
                            try:
                                calc=pair(*[json.loads(r['raw']) for r in rs],g['strike_type'],q,g['fee_multiplier'])
                                row['receipt_skew_ms']=abs(rs[0]['received_ns']-rs[1]['received_ns'])/1e6
                                row['calculation']=calc
                                row['status']='CONDITIONAL_SCREEN' if calc['complete'] else 'INSUFFICIENT_DEPTH'
                            except (ValueError,KeyError,TypeError) as e:row['reason']='schema_'+type(e).__name__
                    rows.append(row)
    # Detailed legs are saved for reproducibility; compact per-series files for review.
    (ROOT/'SCORES.json').write_text(json.dumps(rows,default=str,indent=2)+'\n')
    summary=[]
    for g in groups:
        rs=[r for r in rows if r['series']==g['series']];valid=[r for r in rs if r['status']=='CONDITIONAL_SCREEN']
        record={'series':g['series'],'category':g['category'],'cases':len(rs),'status_counts':dict(collections.Counter(r['status'] for r in rs)),
          'gross_positive':sum(r['calculation']['gross']>0 for r in valid),'raw_fee_positive':sum(r['calculation']['net_raw_fee']>0 for r in valid),
          'cent_fee_positive':sum(r['calculation']['net_cent_fee']>0 for r in valid)}
        if valid:
            best=max(valid,key=lambda r:r['calculation']['net_raw_fee']/Decimal(r['quantity']))
            record['best_per_unit']={k:str(best['calculation'][k]/Decimal(best['quantity'])) for k in ['gross','net_raw_fee','net_cent_fee']}
            record['best_case']={k:best[k] for k in ['round','low','high','quantity','receipt_skew_ms']}
            record['max_receipt_skew_ms']=max(r['receipt_skew_ms'] for r in valid)
        summary.append(record)
        compact=[{k:v for k,v in r.items() if k!='calculation'} | {k:str(v) for k,v in r.get('calculation',{}).items() if k in ['gross','net_raw_fee','net_cent_fee']} for r in rs]
        (ROOT/('scores_'+g['series']+'.json')).write_text(json.dumps(compact,indent=2)+'\n')
    out={'study':'AMS-002','status':'ASYNCHRONOUS_CONDITIONAL_SCREEN_ONLY','series':summary,
         'total_cases':len(rows),'realized_pnl':None,'simultaneous_executability':None,'latency_edge':None}
    (ROOT/'SUMMARY.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
