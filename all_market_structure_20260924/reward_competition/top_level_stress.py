"""Post-hoc mechanical sensitivity, explicitly excluded from frozen scenarios.

Remove the best opposite price level for every final-frame one-sided completion.
Do not call disappearance a trade, cancellation, or simulated fill. Reapply the
same original quantities and a 200-contract two-cent competitor if it can rest.
"""
import hashlib,json
from decimal import Decimal as D
from pathlib import Path
from model import depth,scenario,SIDES
ROOT=Path(__file__).resolve().parent

def main():
    frame=json.loads((ROOT/'FRAME_2.json').read_text());books={};inputs={}
    for f in sorted((ROOT/'capture').glob('2_books_*.json')):
        r=json.loads(f.read_text());assert hashlib.sha256(r['raw'].encode()).hexdigest()==r['sha256'];inputs[f.name]=hashlib.sha256(f.read_bytes()).hexdigest()
        if r['status']==200:
            for b in json.loads(r['raw']).get('orderbooks',[]):books[b['ticker']]=b['orderbook_fp']
    rows=[]
    for r in frame['rows']:
        if r['class']!='resting_completion' or len(r['short_sides'])!=1:continue
        side=r['short_sides'][0];other='no' if side=='yes' else 'yes';b=depth(books[r['ticker']]);top=max(p for p,q,o in b[other]);removed=sum(q for p,q,o in b[other] if p==top)
        b[other]=[(p,q,o) for p,q,o in b[other] if p<top]
        item={'ticker':r['ticker'],'book_received_ns':r['book_received_ns'],'removed_side':other,'removed_price':str(top),'removed_quantity':str(removed),'remaining_opposite_depth':str(sum(q for p,q,o in b[other])),'plans':[]}
        for plan in r['plans']:
            own={s:D(q) for s,q in plan['quantity'].items()};case=scenario(b,D(r['program']['target_size_fp']),D(r['program']['discount_factor_bps'])/10000,own,'better_200')
            row={'buffer_fraction':plan['buffer_fraction'],'principal':plan['principal'],'fee_stress_reserve':plan['fee_stress_reserve'],'scenario':case}
            if case['available']:
                rate=r['pool_dollars']/r['duration_hours']*case['scores']['capped']['overall_share'];reward=rate*r['remaining_hours']
                row.update(capped_rate=rate,capped_remaining_gross=reward,capped_half_uptime_remaining=reward/2,minimum_remaining_minutes_at_half_uptime=(plan['principal']+plan['fee_stress_reserve'])/(rate/2)*60 if rate else None)
            item['plans'].append(row)
        rows.append(item)
    out={'designation':'post-hoc structural sensitivity after observing 12-contract top levels; not a preregistered success metric or fill simulation','input_hashes':inputs,'rows':rows}
    (ROOT/'TOP_LEVEL_STRESS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

if __name__=='__main__':main()
