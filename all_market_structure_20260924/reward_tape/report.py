import hashlib,json,zipfile
from pathlib import Path
from tape import ROOT,stamp

def main():
    d=json.loads((ROOT/'RESULTS.json').read_text());panel={r['ticker']:r for r in json.loads((ROOT/'PANEL.json').read_text())['rows']}
    for f,h in json.loads((ROOT/'FREEZE.json').read_text())['files'].items():assert hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==h
    receipts=list((ROOT/'capture').glob('*.json'))
    for f in receipts:
        r=json.loads(f.read_text());assert hashlib.sha256(r['raw'].encode()).hexdigest()==r['sha256']
    lines=['# AMS-006: cheap quotes do get hit', '',
        'The public tape confirms three Truflation candidates had full target-sized one-cent executions during their reward periods, with taker direction compatible with selling into the proposed cheap bid. The seven Miami weather candidates had no returned trades within their reward period as of acquisition. Neither finding establishes what would happen after our own quote changes the book.', '',
        '| Market | Contracts returned | Within program | Direction/price compatible within program | Pagination complete |','|---|---:|---:|---:|---|']
    for r in d['rows']:lines.append(f"| {r['ticker']} | {r['contracts']} | {r['within_program_contracts']} | {r['compatible_within_program_contracts']} | {r['complete_returned_pagination']} |")
    lines += ['', '## Timing matters', '',
        '| Compatible print | Time after reward start, minutes | Contract count | Ideal half-pool accrual since program start, dollars |','|---|---:|---:|---:|']
    for r in d['rows']:
        p=panel[r['ticker']]
        for x in r['detail']:
            if x['within_program'] and x['direction_price_compatible_with_quote']:
                elapsed=(stamp(x['trade']['created_time'])-stamp(p['program']['start_date']))/3600
                lines.append(f"| {r['ticker']} at {x['trade']['created_time']} | {elapsed*60:.3f} | {x['trade']['count_fp']} | {elapsed*p['quote']['ideal_rate']:.5f} |")
    lines += ['',
        'Each Truflation market had a 1000-contract print about 2.6–2.8 minutes after its program began. That corresponds to $10 of one-cent purchase principal, while an ideal half-pool quote could have accrued only approximately five cents since program start. One market also had a 14-contract print at the same timestamp. This is substantial evidence against assuming that cheap orders will reliably sit untouched for the roughly nine hours needed to earn back a full losing fill in these programs.', '',
        'We do not know participant identity, entry time, strategy, queue rank, reward credits, terminal outcome or realized P&L. The observed contracts might later win. The calculation is a conditional reward-versus-principal comparison, not a claim that a named maker lost money, that wash trading occurred, or that our own order would receive the same fills.', '',
        'For Miami, five markets returned zero historical prints; two returned one contract each at a YES price of five cents around 03:00 UTC, before the 03:02:14 UTC reward start. No reward-period trades appeared as of these requests. This supports examining the short, high-rate weather programs separately from the slower Truflation programs. It cannot demonstrate safety after adding a new bid.', '',
        '## Decision', '',
        'Deprioritize these three Truflation markets for a subsidy-only strategy without a separate fair-value edge. Advance the high-rate, short-window hypothesis to a fresh-window replication across any newly active reward markets meeting the same rate and duration gates. Do not restrict that search to Miami or to weather. No strategy is admitted for trading.', '',
        '## Verification', '',
        f"Ten public HTTP 200 receipts, ten complete returned pagination sequences, four direction/block/legacy tests passed before acquisition. Frozen files and raw-body hashes verified. Acquisition took {d['elapsed_seconds']:.2f} seconds. No credentials, orders, imputed fills or P&L.", '',
        'Spec commit a59c9e331dcfcd71c957e753bc4fd2460df403c0; acquisition/test freeze 6c5c059043bd8c569711c607c56ae44a8ae6cf82.', '',
        'Sources: https://docs.kalshi.com/api-reference/market/get-trades and https://docs.kalshi.com/openapi.yaml. The schema defines taker_outcome_side as directional exposure; taker_book_side is the equivalent bid/ask vocabulary. Block trades are excluded from order-book compatibility. Returned legacy and new direction fields agreed in observed prints.', '',
        'All acquisition processes ended.']
    (ROOT/'RESULTS.md').write_text('\n'.join(lines)+'\n')
    hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(ROOT.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.name not in ('EVIDENCE_HASHES.json','ARCHIVE.json','AMS_006_Evidence.zip')}
    (ROOT/'EVIDENCE_HASHES.json').write_text(json.dumps(hashes,indent=2)+'\n')
    archive=ROOT/'AMS_006_Evidence.zip'
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for rel in list(hashes)+['EVIDENCE_HASHES.json']:z.write(ROOT/rel,rel)
    with zipfile.ZipFile(archive) as z:assert z.testzip() is None
    arc={'filename':archive.name,'bytes':archive.stat().st_size,'sha256':hashlib.sha256(archive.read_bytes()).hexdigest()}
    (ROOT/'ARCHIVE.json').write_text(json.dumps(arc,indent=2)+'\n');print(json.dumps(arc))

if __name__=='__main__':main()
