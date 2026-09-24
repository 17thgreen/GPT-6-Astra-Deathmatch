import hashlib,json,zipfile
from decimal import Decimal as D
from screen import ROOT,buy,template

def main():
    for name in ['FREEZE.json','FOLLOWUP_FREEZE.json']:
        for f,h in json.loads((ROOT/name).read_text())['files'].items():assert hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==h
    def read(name):
        r=json.loads((ROOT/'capture'/name).read_text());assert hashlib.sha256(r['raw'].encode()).hexdigest()==r['sha256'];assert r['status']==200;return json.loads(r['raw'])
    d=json.loads((ROOT/'RESULTS.json').read_text());programs=[];cursor=False
    for f in sorted((ROOT/'capture').glob('volume_*.json')):
        x=read(f.name);programs+=x['incentive_programs'];cursor=bool(x.get('next_cursor'))
    follow=[]
    for series,low,high in [('KXMSCOTTON','KXMSCOTTON-28JAN31-T800000','KXMSCOTTON-28JAN31-T900000'),('KXTEENCLOTHADS','KXTEENCLOTHADS-26OCT06-T136','KXTEENCLOTHADS-26OCT06-T140')]:
        s=read(series+'.json')['series'];b={t:read(t+'_book.json')['orderbook_fp'] for t in [low,high]};m={t:read(t+'_metadata.json')['market'] for t in [low,high]}
        same=all(m[low].get(k)==m[high].get(k) for k in ['event_ticker','strike_type','close_time','expiration_time'])
        same=same and all(template(m[low].get(k),D(str(m[low]['floor_strike'])))[0]==template(m[high].get(k),D(str(m[high]['floor_strike'])))[0] for k in ['rules_primary','rules_secondary'])
        for q in (1,10,100):
            a=buy(b[low],'yes',q);c=buy(b[high],'no',q)
            row={'series':series,'low':low,'high':high,'qty':q,'fee_type':s['fee_type'],'fee_multiplier':s['fee_multiplier'],'rule_templates_still_match':same,'active_volume_programs_found':sum(p['market_ticker'] in (low,high) for p in programs),'complete':a is not None and c is not None}
            if row['complete']:
                gross=D(q)-a[0]-c[0];fees=(a[1]+c[1])*D(str(s['fee_multiplier']))
                row.update({'gross_margin':str(gross),'standard_raw_fee_margin':str(gross-fees),'optimistic_volume_cap_if_eligible':str(D('.01')*q),'volume_cap_admitted':False})
            follow.append(row)
    (ROOT/'FOLLOWUP_RESULTS.json').write_text(json.dumps({'active_volume_entries':len(programs),'cursor_remaining':cursor,'rows':follow},indent=2)+'\n')
    lines=['# AMS-008: broad static price discrepancies fail current fees', '',
        f"Retained development snapshot: {d['open_usable_markets']} open usable markets, {d['grouped_contracts']} threshold contracts admitted, {d['pairable_groups']} pairable rule/expiry groups, {d['pairs']} pairs at three quantities. {d['counts']['complete']} depth-complete cases and {d['counts']['missing_depth']} insufficient-depth cases.", '',
        'Five cases across two pairs had positive gross floor margins. None survived the ordinary M=1 unrounded taker-fee benchmark. The fixed follow-up confirmed both series currently report quadratic fees with multiplier 1, and refreshed quotes still failed after fees. Matching rule templates remained intact. No profitable opportunity was established.', '',
        '| Pair series | Quantity per leg | Fresh gross margin | Fresh margin after standard raw fees |','|---|---:|---:|---:|']
    for r in follow:
        if r['complete']:lines.append(f"| {r['series']} | {r['qty']} | {r['gross_margin']} | {r['standard_raw_fee_margin']} |")
    lines += ['',
        f"The active public event-volume catalog returned {len(programs)} programs with no remaining cursor. We could not establish an applicable volume subsidy to offset these costs. The theoretical two-leg cap of one cent per paired unit is not admitted revenue. Private fee terms and account-specific eligibility were not inspected.", '',
        'Decision: keep the static taker threshold lane parked. This broader check justified one revisit; do not continue scanning the same retained data for a desired answer.', '',
        'This is reused development data, not an independent holdout. Quotes are asynchronous; even same-response receipt times do not imply atomic multi-market execution. The payoff floor assumes ordinary, common-source binary resolution and excludes explicit fair-value language, but source metadata and normalized text do not substitute for a complete contractual settlement proof. These limitations would matter for a positive result. No inventory, reward or realized P&L was booked.', '',
        'Four focused tests passed before analysis. All original and follow-up freeze hashes and eleven HTTP 200 follow-up receipts verified. CASES.jsonl preserves all 49,308 cases. The archive includes cases, code, freezes, follow-up receipts and results; reproducing the original screen additionally needs the AMS-005 raw-evidence artifact referenced in ../reward_census/ARCHIVE.json.', '',
        'Original source freeze: 08a6cb8bd7cc3c005c4b2fbb97ec45d1b0efc66b. Follow-up freeze: 29bfce1fc2e1dfdb463d4b1cd7aa62b1055eb13b.', '',
        'Sources: https://kalshi.com/docs/kalshi-fee-schedule.pdf ; https://help.kalshi.com/en/articles/13823850-what-is-the-kalshi-volume-incentive-program ; https://docs.kalshi.com/api-reference/market/get-market-orderbook .', '',
        'No acquisition or analysis process remains running for AMS-008.']
    (ROOT/'RESULTS.md').write_text('\n'.join(lines)+'\n')
    hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(ROOT.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.name not in ('EVIDENCE_HASHES.json','ARCHIVE.json','AMS_008_Evidence.zip')}
    (ROOT/'EVIDENCE_HASHES.json').write_text(json.dumps(hashes,indent=2)+'\n')
    archive=ROOT/'AMS_008_Evidence.zip'
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for rel in list(hashes)+['EVIDENCE_HASHES.json']:z.write(ROOT/rel,rel)
    with zipfile.ZipFile(archive) as z:assert z.testzip() is None
    a={'filename':archive.name,'bytes':archive.stat().st_size,'sha256':hashlib.sha256(archive.read_bytes()).hexdigest()}
    (ROOT/'ARCHIVE.json').write_text(json.dumps(a,indent=2)+'\n');print(json.dumps(a))

if __name__=='__main__':main()
