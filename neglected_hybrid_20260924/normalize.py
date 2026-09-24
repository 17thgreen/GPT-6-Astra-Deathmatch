"""Strict normalized race/forecast/quote adapter. No scoring or fitting."""
from datetime import datetime,timezone
from pathlib import Path
from collections import defaultdict
import argparse,hashlib,json,re
from core import probability

def forecast_rows(root):
    rows=[]
    for file in sorted(root.glob('*latest*.receipt.json')):
        receipt=json.loads(file.read_text())
        if not receipt.get('admitted'):continue
        p=root/receipt['source_file'];body=p.read_bytes()
        if hashlib.sha256(body).hexdigest()!=receipt['decoded_sha256']:raise ValueError('Forecast hash mismatch')
        for f in json.loads(body):
            chamber=receipt['chamber'];state=f['state'];seat=str(f['seat'])
            if chamber=='house':
                seat=str(int(seat))
                rid=f'2024-HOUSE-{state}-{seat}'
            else:
                # Distinguish special seats; never silently merge them with the
                # regular state's contract. The admitted market adapter only
                # recognizes regular-seat SENATEXX and explicitly audits names.
                rid=f'2024-SENATE-{state}-{seat}'
            probs=f['winprob']
            if abs(sum(probs.values())-100)>.06:raise ValueError('Party probabilities do not sum to 100')
            p_dem=sum(float(v) for k,v in probs.items() if re.fullmatch(r'dem\d*',k))/100
            rows.append({'race_id':rid,'p_dem':probability(p_dem),'available_at':receipt['available_at'],
                         'provenance_status':'contemporaneous','source':receipt['url'],
                         'source_sha256':receipt['decoded_sha256'],'candidates':f['candidates']})
    return rows

def race_key(ticker):
    m=re.fullmatch(r'HOUSE(?:PARTY-?)?([A-Z]{2})(\d+|AL)-24-D',ticker)
    if m:return f'2024-HOUSE-{m[1]}-{1 if m[2]=="AL" else int(m[2])}',m[1],'house'
    m=re.fullmatch(r'SENATE(?:PARTY-?)?([A-Z]{2})-24-D',ticker)
    if m:return f'2024-SENATE-{m[1]}-1',m[1],'senate'
    return None

def normalize(raw, forecasts, output):
    metadata=json.loads((raw/'metadata.json').read_text());qraw=json.loads((raw/'quotes.json').read_text())
    source_forecasts=forecast_rows(forecasts)
    fc=defaultdict(list)
    for r in source_forecasts:fc[r['race_id']].append(r)
    candidates=[];rejected=[]
    for m in metadata:
        if not m['ticker'].endswith('-D'):continue
        key=race_key(m['ticker'])
        if key is None:rejected.append({'ticker':m['ticker'],'reason':'unrecognized_race_ticker'});continue
        rid,state,chamber=key
        rule=m.get('rules_primary','');low=rule.lower()
        if 'democratic' not in low or 'sworn in' not in low or '2025' not in low:
            rejected.append({'ticker':m['ticker'],'reason':'affirmative_rule_not_democratic_2025_member','rule':rule});continue
        if 'independent' in low:
            rejected.append({'ticker':m['ticker'],'reason':'independent_party_ambiguity','rule':rule});continue
        # Require Senate's named candidate to match the independent forecast.
        # House rules explicitly name the district and party rather than candidate.
        if chamber=='senate' and fc[rid]:
            latest=max(fc[rid],key=lambda r:r['available_at'])
            name=latest['candidates'].get('dem','').lower()
            if not name or name not in low:
                rejected.append({'ticker':m['ticker'],'reason':'senate_candidate_rule_mismatch','forecast_candidate':name,'rule':rule});continue
        if m.get('result') not in ('yes','no') or m.get('status') not in ('finalized','settled'):
            rejected.append({'ticker':m['ticker'],'reason':'unresolved_or_nonbinary'});continue
        candidates.append({'race_id':rid,'state':state,'chamber':chamber,'ticker':m['ticker'],
                           'mapping_status':'verified_democratic_party_yes','open_at':m['open_time'],'close_at':m['close_time'],
                           'settled_at':m.get('settlement_ts'),'outcome_dem':int(m['result']=='yes'),
                           'resolution_source':f'https://api.elections.kalshi.com/trade-api/v2/historical/markets/{m["ticker"]}',
                           'rules_primary':rule,'rules_secondary':m.get('rules_secondary',''),
                           'definition_basis_risk':'election winner forecast versus party sworn in 2025'})
    groups=defaultdict(list)
    for r in candidates:groups[r['race_id']].append(r)
    races=[]
    for rid,group in groups.items():
        if len(group)>1:
            # Ambiguous duplicate venues/series are refused, not cherry-picked.
            rejected.extend({'ticker':r['ticker'],'reason':'duplicate_race_mapping'} for r in group)
        else:races.extend(group)
    ticker_map={r['ticker']:r['race_id'] for r in races}
    quotes=[];seen=set()
    for packet in qraw:
        if packet['ticker'] not in ticker_map:continue
        for q in packet['candles']:
            bid=q.get('yes_bid',{}).get('close');ask=q.get('yes_ask',{}).get('close')
            if bid is None or ask is None:continue
            key=(packet['ticker'],q['end_period_ts'],bid,ask)
            if key in seen:continue
            seen.add(key)
            quotes.append({'race_id':ticker_map[packet['ticker']],
                'observed_at':datetime.fromtimestamp(q['end_period_ts'],timezone.utc).isoformat(),
                'yes_bid':probability(bid),'yes_ask':probability(ask),'kind':'historical_hourly_quote_close_no_depth',
                'depth_contracts':None,'bar_trade_volume':q.get('volume')})
    dataset={'study':'NH-001/NH-001A','races':sorted(races,key=lambda r:r['race_id']),
             'forecasts':source_forecasts,'quotes':quotes,'mapping_exclusions':rejected}
    output.parent.mkdir(parents=True,exist_ok=True);output.write_text(json.dumps(dataset,indent=2)+'\n')
    return {'races':len(races),'house':sum(r['chamber']=='house' for r in races),'senate':sum(r['chamber']=='senate' for r in races),
            'forecasts':len(source_forecasts),'quotes':len(quotes),'mapping_exclusions':rejected}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('raw',type=Path);p.add_argument('forecasts',type=Path);p.add_argument('output',type=Path)
    a=p.parse_args();print(json.dumps(normalize(a.raw,a.forecasts,a.output),indent=2))
