"""Post-hoc feasibility screen of AMS-004 observations; no new acquisition."""
from pathlib import Path
from decimal import Decimal as D
import json
from survey import ROOT, stamp

def main():
    result=json.loads((ROOT/'RESULTS.json').read_text()); metadata={}
    for p in (ROOT/'capture').glob('metadata_*.json'):
        for m in json.loads(json.loads(p.read_text())['raw']).get('markets',[]):metadata[m['ticker']]=m
    rows=[]
    for x in result['rows']:
        if x['class'] not in ('yes_short','no_short') or len(x.get('empty_sides',[]))!=1:continue
        t=x['ticker'];side=x['empty_sides'][0];other='no' if side=='yes' else 'yes';p=x['program'];m=metadata[t]
        b=json.loads(json.loads((ROOT/'capture'/f'{t}_book.json').read_text())['raw'])['orderbook_fp']
        best=max((D(a) for a,q in b[other+'_dollars']),default=D(0))
        linear=m.get('price_level_structure')=='linear_cent' and m.get('price_ranges')==[{'end':'1.0000','start':'0.0000','step':'0.0100'}]
        # At equality the new order can match; it is not a resting quote.
        rests=linear and D('.01')+best<D(1)
        hours=(stamp(p['end_date'])-stamp(p['start_date']))/3600
        remaining=max(0,min(stamp(p['end_date']),stamp(m['close_time']))-x['book_received_ns']/1e9)/3600
        rate=p['period_reward']/10000/hours/2
        risk=float(D(p['target_size_fp'])*D('.01'))
        rows.append({'ticker':t,'empty_side':side,'other_best_bid':str(best),'linear_cent_verified':linear,'one_cent_would_rest':rests,
                     'single_order_principal':risk,'ideal_half_pool_dollars_per_hour':rate,'remaining_hours':remaining,
                     'ideal_remaining_gross_if_rests':rate*remaining if rests else None,
                     'hours_to_match_one_full_losing_fill':risk/rate,'remaining_gross_exceeds_principal':rests and rate*remaining>risk})
    out={'designation':'post-hoc descriptive feasibility screen; no payoff or fill validation',
         'one_side_empty_other_meets':len(rows),'one_cent_would_rest':sum(x['one_cent_would_rest'] for x in rows),
         'remaining_gross_exceeds_principal':sum(x['remaining_gross_exceeds_principal'] for x in rows),'rows':rows}
    (ROOT/'ENTRY_SCREEN.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='rows'},indent=2))
    for x in rows:
        if x['remaining_gross_exceeds_principal']:print(json.dumps(x))

if __name__=='__main__':main()
