"""Publish prospective observations without assigning virtual fills or income."""
import collections,hashlib,json,zipfile
from decimal import Decimal as D
from pathlib import Path
from watch import ROOT,stamp

def main():
    d=json.loads((ROOT/'RESULTS.json').read_text())
    for f,h in json.loads((ROOT/'FREEZE.json').read_text())['files'].items():assert hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==h
    receipts=[]
    for f in sorted((ROOT/'capture').glob('*.json')):
        r=json.loads(f.read_text());assert hashlib.sha256(r['raw'].encode()).hexdigest()==r['sha256'];receipts.append(r)
    for f in d['frames']:
        s=json.loads((ROOT/f"SELECTION_{f['cycle']:02d}.json").read_text())
        for r in f['rows']:
            if r['book_received_ns']:assert s['selected_before_books_ns']<r['book_received_ns']
    ever={}
    for f in d['frames']:
        for r in f['rows']:
            if r.get('quote',{}).get('priority'):ever.setdefault(r['ticker'],r)
    evidence=[]
    for t,first in ever.items():
        rows=[r for f in d['frames'] for r in f['rows'] if r['ticker']==t];ns=[r['book_received_ns'] for r in rows if r['book_received_ns']]
        tape=next(r for r in d['trades'] if r['ticker']==t)
        evidence.append({'ticker':t,'observations':len(rows),'strict_priority_passes':sum(r.get('quote',{}).get('priority',False) for r in rows),
            'below_target_observations':sum(r['class'] in ('yes_short','no_short','both_short') for r in rows),
            'observation_span_minutes':(max(ns)-min(ns))/6e10,'ideal_rate':first['quote']['ideal_rate'],
            'principal':first['quote']['principal'],'first_ideal_remaining':first['quote']['ideal_remaining_gross'],
            'last_ideal_remaining':rows[-1].get('quote',{}).get('ideal_remaining_gross'),
            'all_returned_prints':len(tape['detail']),'within_program_prints':sum(x['within_program'] for x in tape['detail']),
            'tape_usable':tape['usable'],'tape_cursor_remaining':tape['cursor_remaining']})
    partial=[]
    for f in d['frames']:
        for r in f['rows']:
            if r['ticker'] not in ever or r['class'] not in ('yes_short','no_short') or r.get('empty_sides'):continue
            side='yes' if r['class']=='yes_short' else 'no';target=D(r['program']['target_size_fp']);existing=D(r['depth'][side])
            # Exploratory extension only: at E<T/5, a completing one-cent quote
            # would set the reference on a cent grid, with all old levels >= it.
            if not 0<existing<target/5:continue
            raw=json.loads(json.loads((ROOT/'capture'/f"{f['cycle']:02d}_books.json").read_text())['raw'])
            b=next(x['orderbook_fp'] for x in raw['orderbooks'] if x['ticker']==r['ticker'])
            mraw=json.loads(json.loads((ROOT/'capture'/f"{f['cycle']:02d}_metadata.json").read_text())['raw'])
            m=next(x for x in mraw['markets'] if x['ticker']==r['ticker'])
            other='no' if side=='yes' else 'yes';best=max(D(p) for p,q in b[other+'_dollars'])
            if m.get('price_level_structure')!='linear_cent' or best+D('.01')>=1 or any(D(p)<D('.01') for p,q in b[side+'_dollars']):continue
            qty=target-existing;share=qty/target/2;hours=(stamp(r['program']['end_date'])-stamp(r['program']['start_date']))/3600
            partial.append({'cycle':f['cycle'],'ticker':r['ticker'],'existing_quantity':str(existing),'hypothetical_completion_quantity':str(qty),
                'principal':str(qty*D('.01')),'ideal_snapshot_share':str(share),'ideal_rate':float(share)*r['program']['period_reward']/10000/hours,
                'designation':'post-hoc model extension, excluded from preregistered strict pass count'})
    summary={'cycles':len(d['frames']),'selected':len(d['selected_programs']),'series':len(set(p['market_ticker'].split('-')[0] for p in d['selected_programs'])),
        'selection_cap_reached':len(d['selected_programs'])==30,'catalog_capped_cycles':sum(f['catalog_cursor_remaining'] for f in d['frames']),
        'market_observations':sum(len(f['rows']) for f in d['frames']),'ever_priority':len(ever),'candidates':evidence,
        'post_hoc_partial_extension':partial,'http_statuses':dict(collections.Counter(str(r['status']) for r in receipts)),
        'all_trade_pages':len(d['trades']),'trade_pages_with_cursor':sum(r['cursor_remaining'] for r in d['trades']),
        'elapsed_seconds':d['elapsed_seconds'],'realized_pnl':None,'hypothetical_fills':None}
    (ROOT/'SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
    lines=['# AMS-007: a fresh hourly reward gap recurs', '',
        f"The bounded watch completed {summary['cycles']} cycles across {summary['selected']} newly active programs in {summary['series']} series. Selection was based on reward duration, start time and rate before each book observation, across all categories. The 30-ticker selection cap was reached; no catalog pagination cap was reached. There were {summary['market_observations']} market observations and {summary['all_trade_pages']} usable final trade pages, with no returned pagination cursors.", '',
        'Seven fresh Miami 1am EDT temperature contracts met the original empty-side, opposite-depth, one-cent-resting and remaining-budget gates. Their $100 pools began at 04:02:16.975350 UTC and ended at 05:00 UTC. This is a different reward window from the midnight contracts discovered in AMS-005, but the same city and mechanism; it is not independent geographic or regime validation.', '',
        '| Candidate | Strict passes / observations | Below-target observations | Snapshot span, minutes | Returned historical trades |','|---|---:|---:|---:|---:|']
    for e in evidence:lines.append(f"| {e['ticker']} | {e['strict_priority_passes']}/{e['observations']} | {e['below_target_observations']} | {e['observation_span_minutes']:.3f} | {e['all_returned_prints']} |")
    lines += ['',
        'Six candidates passed all ten available observations across roughly nine minutes. A seventh passed the first three strict observations; a one-contract competing bid then made its side nonempty while leaving it 999 contracts below target. All seven remained below target in every observed snapshot. None of these seven returned any historical trades as of the final page reads. Nearby central strikes did trade, including one-cent prints, so the absence of trades must not be generalized to the entire weather family.', '',
        'Each original hypothetical 1000-contract one-cent quote committed $10 principal. The ideal full-side reward rate was about $51.98/hour, with approximately $41.78 remaining for each of the six strict candidates at the last book read. That is a conditional budget at a past observation time, not current availability, earned money or an expected return. About 11.54 minutes at the ideal rate would match one full losing fill before fees; the nine-minute observation span did not even cover that duration.', '',
        '## The small competing bid', '',
        'The separately labelled post-hoc extension in SUMMARY.json shows why a single competing contract does not mechanically destroy this mechanism. With 1 existing contract, a 1000-contract target, a cent grid and the opposite book permitting a resting one-cent price, a 999-contract completing bid would set the one-fifth-target reference at one cent. All 1000 contracts would have full distance weight; our conditional side share would be 999/1000 and overall snapshot share 49.95%, for $9.99 principal. This extension was not added to the preregistered pass count and has no account-scoring validation.', '',
        '## What has and has not been learned', '',
        'Repeated, high-rate depth gaps have now been observed in two consecutive Miami hourly reward windows. The setup merits a targeted mechanics validation. Profit has not been established. Our own executable bid would create a better trading opportunity for others, so no-trade history from an empty side cannot estimate fills after insertion. Snapshots are not continuous uptime; changing competition, partial fills, account entitlement and actual credited rewards remain unresolved.', '',
        'At exactly the target, even a partial fill can stop qualification unless other depth or a buffer keeps the total above target. Replenishment increases cumulative exposure. The seven strikes depend on one temperature observation and are correlated. The $100-per-market reward campaigns last less than an hour; multiplying the instantaneous rate across a day would be unsupported.', '',
        '## Verification and evidence', '',
        f"{len(receipts)} HTTP 200 receipts. Four prospective-admission tests passed before acquisition. Frozen source/input hashes, all receipt body hashes and selection-before-book timestamps verified. The watch ended after {d['elapsed_seconds']:.2f} seconds with twelve completed cycles; it was not extended to seek a favorable result.", '',
        'Specification/start commit 82debd0abd99436d9c08565798b632aff277eab7; acquisition/test freeze 2856308905ab0416907002c8034e52e47c5b07d8. Original metrics remain unchanged after observing the one-contract bid.', '',
        'Raw catalogs, book/metadata receipts, trade pages, selections, frames and full results are in AMS_007_Raw_Evidence.zip. Code, summary, report and checksums remain in the repository. Restore the raw artifact into this experiment directory to rerun the report.', '',
        'Primary scoring source: https://help.kalshi.com/en/articles/13823851-liquidity-incentive-program .', '',
        'No credentials, live/demo orders, imputed fills, earned rewards or realized P&L. All bounded processes have ended.']
    (ROOT/'RESULTS.md').write_text('\n'.join(lines)+'\n')
    rawpaths=sorted((ROOT/'capture').glob('*.json'))+sorted(ROOT.glob('SELECTION_*.json'))+sorted(ROOT.glob('FRAME_*.json'))+[ROOT/'RESULTS.json']
    hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in rawpaths}
    (ROOT/'EVIDENCE_HASHES.json').write_text(json.dumps(hashes,indent=2)+'\n')
    dest=ROOT.parents[2]/'artifacts';dest.mkdir(exist_ok=True);archive=dest/'AMS_007_Raw_Evidence.zip'
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in rawpaths:z.write(p,str(p.relative_to(ROOT)))
        z.write(ROOT/'EVIDENCE_HASHES.json','EVIDENCE_HASHES.json')
    with zipfile.ZipFile(archive) as z:assert z.testzip() is None
    a={'filename':archive.name,'bytes':archive.stat().st_size,'sha256':hashlib.sha256(archive.read_bytes()).hexdigest()}
    (ROOT/'ARCHIVE.json').write_text(json.dumps(a,indent=2)+'\n');print(json.dumps({k:v for k,v in summary.items() if k not in ('candidates','post_hoc_partial_extension')},indent=2));print(json.dumps(a))

if __name__=='__main__':main()
