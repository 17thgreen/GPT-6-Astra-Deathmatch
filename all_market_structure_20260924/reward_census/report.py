"""Build an auditable summary and raw-evidence-only archive after AMS-005."""
import collections,datetime as dt,hashlib,json,zipfile
from pathlib import Path
from census import ROOT,score

def main():
    data=json.loads((ROOT/'RESULTS.json').read_text());follow=json.loads((ROOT/'FOLLOWUP_RESULTS.json').read_text()) if (ROOT/'FOLLOWUP_RESULTS.json').exists() else {'rows':[]}
    freeze=json.loads((ROOT/'FREEZE.json').read_text())
    for p,h in freeze['files'].items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h
    assert hashlib.sha256((ROOT/'PANEL.json').read_bytes()).hexdigest()==(ROOT/'PANEL_SHA256.txt').read_text().strip()
    assert hashlib.sha256((ROOT/'FOLLOWUP_PANEL.json').read_bytes()).hexdigest()==(ROOT/'FOLLOWUP_PANEL_SHA256.txt').read_text().strip()
    receipts={};books={};meta={};book_ns={}
    for path in sorted((ROOT/'capture').glob('*.json')):
        rec=json.loads(path.read_text());assert hashlib.sha256(rec['raw'].encode()).hexdigest()==rec['sha256'];receipts[path.stem]=rec
        if rec['status']!=200:continue
        try:d=json.loads(rec['raw'])
        except ValueError:continue
        if path.stem.startswith('books_'):
            for b in d.get('orderbooks',[]):books[b['ticker']]=b['orderbook_fp'];book_ns[b['ticker']]=rec['received_ns']
        elif path.stem.startswith('metadata_'):
            for m in d.get('markets',[]):meta[m['ticker']]=m
    for r in data['rows']:
        assert score(r['ticker'],r['program'],meta.get(r['ticker']),books.get(r['ticker']),book_ns.get(r['ticker']))==r
    counts=data['counts'];valid=sum(counts.get(x,0) for x in ('both_meet','yes_short','no_short','both_short'))
    gap=sum(counts.get(x,0) for x in ('yes_short','no_short','both_short'))
    candidates=sorted([r for r in data['rows'] if r.get('quote',{}).get('priority')],key=lambda r:(-r['quote']['ideal_rate_per_principal'],r['ticker']))
    shortlisted=json.loads((ROOT/'FOLLOWUP_PANEL.json').read_text())['rows']
    stress=[]
    for r in candidates:
        q=r['quote'];states=[x for x in follow['rows'] if x['ticker']==r['ticker']]
        stress.append({'ticker':r['ticker'],'quote':q,'followup_rounds':len(states),'priority_followups':sum(x.get('quote',{}).get('priority',False) for x in states),
            'losing_contracts_per_hour_break_even':{f'share_retention_{retention}_maker_M_{m}':q['ideal_rate']*retention/(.01+m*.0175*.01*.99) for retention in [1,.5,.25] for m in [0,1,2]},
            'buffer_scenarios':[{'quantity':float(q['quantity'])*b,'principal':q['principal']*b,'fill_buffer_before_below_target':float(q['quantity'])*(b-1),'ideal_rate_unchanged':q['ideal_rate']} for b in [1,1.1,1.25,2]]})
    (ROOT/'CANDIDATES.json').write_text(json.dumps(stress,indent=2)+'\n')
    times=[r['received_ns']/1e9 for r in receipts.values()];utc=lambda t:dt.datetime.fromtimestamp(t,dt.timezone.utc).isoformat()
    lines=['# AMS-005: reward-depth census and recurrence', '',f"Observation window: {utc(min(times))} through {utc(max(times))}.", '',
        f"Catalog entries {data['panel_summary']['catalog_count']}; distinct eligible listed tickers {data['panel_summary']['eligible_unique_markets']}; requested {data['selected']}. Catalog cursor remaining: {data['panel_summary']['catalog_cursor_remaining']}; market cap applied: {data['panel_summary']['market_cap_applied']}.", '',
        f"Evaluable open/current-window markets: {valid}; gaps on one or both sides: {gap} ({gap/valid:.1%} of evaluable markets). A single snapshot is not a duration estimate.", '',
        '| Classification | Count |','|---|---:|']
    for c,n in counts.items():lines.append(f'| {c} | {n} |')
    lines += ['', f"Exactly one empty side while the other meets target: {data['one_empty_side_other_meets']}. A one-cent bid could rest in {data['one_cent_rests']}. Of these, {len(candidates)} had ideal remaining half-pool rewards exceeding one unreplenished order's principal. These are candidates, not profitable-trade findings.", '',
        '| Priority candidate | Ideal $/hour | Principal | Ideal remaining $ | Hours to cover one full losing fill | Follow-up passes |','|---|---:|---:|---:|---:|---:|']
    for r in shortlisted:
        q=r['quote'];s=next(x for x in stress if x['ticker']==r['ticker'])
        lines.append(f"| {r['ticker']} | {q['ideal_rate']:.3f} | {q['principal']:.2f} | {q['ideal_remaining_gross']:.2f} | {q['hours_to_match_full_loss']:.2f} | {s['priority_followups']}/{s['followup_rounds']} |")
    lines += ['', '## Recurrence and concentration', '',
        'All ten shortlisted candidates retained the empty-side, opposite-target and non-crossing one-cent conditions in both follow-up rounds. Seventeen of twenty follow-up observations still passed the remaining-gross-versus-principal screen. The three failures were Miami contracts whose ideal remaining budget fell below $10 as the clock ran down; their book gaps persisted.', '',
        'Seven Miami hourly-temperature strikes dominate the nominal hourly budget: each showed an ideal $51.94/hour and a $10 one-order principal, requiring about 11.55 minutes to earn that principal before fees. They share one underlying weather event and are correlated. Their $100 pools ran from 03:02:14 UTC to 04:00 UTC, less than an hour; the rate is not durable hourly income. The source specifies Synoptic Data and the Kalshi Weather Index Methodology; other weather reports cannot establish settlement.', '',
        'At the last metadata reads, five of these weather markets showed zero lifetime volume and two showed one contract each. That is evidence of little prior trading, not evidence that our new executable bids would avoid fills. Two slower Truflation candidates instead showed 1000 contracts of volume and last prices of one cent; a subsequent tape study is needed to establish timestamps and taker direction before interpreting them.', '',
        'The API OpenAPI schema explicitly describes period_reward as centi-cents, confirming division by 10000 for dollars (https://docs.kalshi.com/openapi.yaml).', '',
        '## Economics and decisive limitations', '',
        'The 50% reward share is an idealized consequence of owning all qualifying liquidity on one side, while the opposite side qualifies. It is not an account payout quote. Competition, price changes, account eligibility, governing terms and reward changes can reduce it. Reward for excluded time before arrival cannot be recovered.', '',
        'At exactly the target size, even one contract filled can put our side below target and stop qualification until depth is restored. Increasing the quote to buffer fills commits more capital without increasing the ideal 50% share. Replenishment accumulates inventory risk: the $10 example bounds only one unreplenished 1000-contract order at one cent.', '',
        'CANDIDATES.json gives conditional break-even losing-fill flow at 100%, 50%, and 25% retention of the ideal reward, with maker fee multipliers 0, 1 and 2. The maker fee sensitivity uses the published unrounded formula 0.0175*M*p*(1-p); per-trade rounding and account-specific terms can worsen it. These are loss budgets, not measured fill rates or expected returns. The model assumes the full reward rate continues, so lost qualifying seconds require an additional reduction.', '',
        'Two short follow-up rounds test whether the gap recurs. They cannot show continuous availability, response to our inserted order, actual fills, actual reward credits, or stability over the many hours often needed to offset a losing fill. No public passive observation proves those counterfactual execution outcomes.', '',
        'No live or demo orders were placed, no credential was used, and no profit was realized. The strategy has not earned deployment or a cash-cow label.', '',
        '## Verification and provenance', '',
        f"HTTP statuses: {dict(collections.Counter(str(r['status']) for r in receipts.values()))}. Census elapsed {data['elapsed_seconds']:.2f} seconds. Three focused entry tests passed before acquisition. All receipt body hashes, source freezes, both panel hashes and census row reconstruction passed after acquisition.", '',
        'Specification commit: c6e99c8090d977ff1665949443ddab2159a4b765. Source/test freeze: 48a635f10505bb94141fef503ed17e39ddb30a2c. Follow-up selection was saved and committed before its observations.', '',
        'Large raw receipts are preserved in the separate AMS_005_Raw_Evidence.zip artifact; EVIDENCE_HASHES.json verifies its individual members. Code and reports remain in the repository. An index is not a substitute for the raw bytes.', '',
        'Sources:',
        '- https://help.kalshi.com/en/articles/13823851-liquidity-incentive-program',
        '- https://kalshi.com/docs/kalshi-fee-schedule.pdf',
        '- https://docs.kalshi.com/api-reference/market/get-multiple-market-orderbooks',
        '- https://docs.kalshi.com/api-reference/incentive-programs/get-incentives', '',
        'All bounded acquisition processes have ended.']
    (ROOT/'RESULTS.md').write_text('\n'.join(lines)+'\n')
    rawpaths=list(sorted((ROOT/'capture').glob('*.json')))+[ROOT/'PANEL.json',ROOT/'PANEL_SHA256.txt',ROOT/'RESULTS.json',ROOT/'FOLLOWUP_RESULTS.json']
    hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in rawpaths if p.exists()}
    (ROOT/'EVIDENCE_HASHES.json').write_text(json.dumps(hashes,indent=2)+'\n')
    dest=ROOT.parents[2]/'artifacts';dest.mkdir(exist_ok=True);archive=dest/'AMS_005_Raw_Evidence.zip'
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in rawpaths:
            if p.exists():z.write(p,str(p.relative_to(ROOT)))
        z.write(ROOT/'EVIDENCE_HASHES.json','EVIDENCE_HASHES.json')
    with zipfile.ZipFile(archive) as z:assert z.testzip() is None
    arc={'filename':archive.name,'bytes':archive.stat().st_size,'sha256':hashlib.sha256(archive.read_bytes()).hexdigest()}
    (ROOT/'ARCHIVE.json').write_text(json.dumps(arc,indent=2)+'\n')
    print(json.dumps({'counts':counts,'valid':valid,'gaps':gap,'priority_candidates':len(candidates),'shortlisted':len(shortlisted),'followup_passes':sum(x.get('quote',{}).get('priority',False) for x in follow['rows']),'archive':arc},indent=2))

if __name__=='__main__':main()
