"""One pass over retained development books; conditional payoff-floor screen."""
import collections,hashlib,itertools,json,re
from decimal import Decimal as D
from pathlib import Path
ROOT=Path(__file__).resolve().parent;SOURCE=ROOT.parent/'reward_census'
NUM=re.compile(r'-?\d[\d,]*(?:\.\d+)?')

def template(text,strike):
    n=0
    def sub(m):
        nonlocal n
        try:equal=D(m.group().replace(',',''))==strike
        except Exception:equal=False
        if equal:n+=1;return '<STRIKE>'
        return m.group()
    s=NUM.sub(sub,' '.join((text or '').lower().split()))
    return s,n

def buy(book,side,qty):
    other='no' if side=='yes' else 'yes';left=D(qty);cost=D(0);fee=D(0)
    levels=[(D(p),D(q)) for p,q in book[other+'_dollars']]
    if any(not (0<p<1) or q<0 for p,q in levels):return None
    for bid,size in sorted(levels,reverse=True):
        fill=min(left,size);ask=1-bid;cost+=fill*ask;fee+=D('.07')*fill*ask*(1-ask);left-=fill
        if left==0:return cost,fee
    return None

def main():
    results=json.loads((SOURCE/'RESULTS.json').read_text())
    admitted={r['ticker'] for r in results['rows'] if r['class'] in ('both_meet','yes_short','no_short','both_short')}
    metadata={};books={};times={}
    for f in (SOURCE/'capture').glob('*.json'):
        if not f.name.startswith(('metadata_','books_')):continue
        rec=json.loads(f.read_text())
        if rec['status']!=200:continue
        data=json.loads(rec['raw'])
        if f.name.startswith('metadata_'):
            for m in data['markets']:metadata[m['ticker']]=m
        else:
            for b in data['orderbooks']:books[b['ticker']]=b['orderbook_fp'];times[b['ticker']]=rec['received_ns']
    groups=collections.defaultdict(list);exclusions=collections.Counter()
    for t in sorted(admitted):
        m=metadata[t]
        if m.get('market_type')!='binary' or m.get('strike_type') not in ('greater','greater_or_equal') or m.get('cap_strike') is not None or m.get('floor_strike') is None:
            exclusions['not_simple_upper_threshold']+=1;continue
        strike=D(str(m['floor_strike']))
        if not strike.is_finite():exclusions['nonfinite_strike']+=1;continue
        primary,count=template(m.get('rules_primary'),strike);secondary,_=template(m.get('rules_secondary'),strike)
        if not count:exclusions['no_primary_strike_match']+=1;continue
        if re.search(r'fair[ -]?value',primary+' '+secondary):exclusions['explicit_fair_value']+=1;continue
        key=(m['event_ticker'],m['strike_type'],m['close_time'],m['expiration_time'],primary,secondary)
        groups[key].append((strike,t))
    counts=collections.Counter();best=[];positive=[];pairs=0
    with (ROOT/'CASES.jsonl').open('w') as output:
        for key,items in groups.items():
            for (a,low),(b,high) in itertools.combinations(sorted(items),2):
                if a>=b:continue
                pairs+=1
                for qty in (1,10,100):
                    l=buy(books[low],'yes',qty);h=buy(books[high],'no',qty)
                    row={'low':low,'high':high,'qty':qty,'receipt_skew_seconds':abs(times[low]-times[high])/1e9,'rule_template_sha256':hashlib.sha256(json.dumps(key).encode()).hexdigest(),'class':'missing_depth'}
                    if l is not None and h is not None:
                        cost=l[0]+h[0];fee=l[1]+h[1];gross=D(qty)-cost
                        row.update({'class':'complete','entry_cost':str(cost),'gross_floor_margin':str(gross),'M1_raw_fee':str(fee),'M1_raw_fee_margin':str(gross-fee)})
                        best.append(row);best=sorted(best,key=lambda r:(-D(r['gross_floor_margin'])/D(r['qty']),r['low'],r['high'],r['qty']))[:10]
                        if gross>0:positive.append(row)
                    counts[row['class']]+=1;output.write(json.dumps(row)+'\n')
    out={'designation':'reused development snapshot; not independent holdout','open_usable_markets':len(admitted),
         'grouped_contracts':sum(map(len,groups.values())),'pairable_groups':sum(len(v)>1 for v in groups.values()),'pairs':pairs,
         'counts':dict(counts),'positive_gross_cases':len(positive),'positive_M1_fee_cases':sum(D(r['M1_raw_fee_margin'])>0 for r in positive),
         'exclusions':dict(exclusions),'best_complete_cases':best,'positive_cases':positive,'pnl':None}
    (ROOT/'RESULTS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('best_complete_cases','positive_cases')},indent=2))

if __name__=='__main__':main()
