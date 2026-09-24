"""Verify receipt integrity and publish descriptive AMS-004 results."""
import collections
import datetime as dt
import hashlib
import json
import zipfile
from pathlib import Path
from survey import ROOT, classify

def main():
    data = json.loads((ROOT/'RESULTS.json').read_text())
    freeze = json.loads((ROOT/'FREEZE.json').read_text())
    for name, digest in freeze['files'].items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == digest
    assert hashlib.sha256((ROOT/'PANEL.json').read_bytes()).hexdigest() == (ROOT/'PANEL_SHA256.txt').read_text().strip()
    receipts = {}
    for path in sorted((ROOT/'capture').glob('*.json')):
        rec = json.loads(path.read_text())
        assert hashlib.sha256(rec['raw'].encode()).hexdigest() == rec['sha256']
        receipts[path.stem] = rec
    for row in data['rows']:
        if row['class'] in ('both_meet','yes_short','no_short','both_short'):
            rec = receipts.get(row['ticker']+'_book')
            if rec:
                b = json.loads(rec['raw'])['orderbook_fp']
                assert classify(b,row['program']['target_size_fp'])['class'] == row['class']
    counts = data['counts']
    usable = sum(counts.get(c,0) for c in ('both_meet','yes_short','no_short','both_short'))
    gaps = [r for r in data['rows'] if r['class'] in ('yes_short','no_short','both_short')]
    times = [r['received_ns']/1e9 for r in receipts.values()]
    utc = lambda t:dt.datetime.fromtimestamp(t,dt.timezone.utc).isoformat()
    lines = ['# AMS-004: reward-market depth survey', '',
        f"Captured {utc(min(times))} through {utc(max(times))}.", '',
        f"Fresh API catalog: {data['panel_summary']['catalog_count']} active-liquidity program entries; "
        f"{data['panel_summary']['eligible_unique_markets']} distinct tickers after positive-reward, positive-target, unpaid and current-window filters. "
        f"Cursor remaining at cap: {data['panel_summary']['catalog_cursor_remaining']}.", '',
        f"Selected {data['selected']} tickers by a prespecified hash ordering before observing depth. "
        f"{usable} were open, in their listed reward window, and had usable metadata and full books. "
        f"{len(gaps)} of those ({len(gaps)/usable:.1%}) were below target on at least one side; "
        f"{data['empty_side_markets']} had an entirely empty side.", '',
        '| Classification | Markets |', '|---|---:|']
    for c,n in counts.items(): lines.append(f'| {c} | {n} |')
    lines += ['', '## Observed gaps', '', '| Market | Classification | YES depth | NO depth | Target |', '|---|---|---:|---:|---:|']
    for r in gaps:
        lines.append(f"| {r['ticker']} | {r['class']} | {r['depth']['yes']} | {r['depth']['no']} | {r['program']['target_size_fp']} |")
    lines += ['', '## Post-hoc entry feasibility', '',
        'A separately labelled post-hoc screen (ENTRY_SCREEN.json) considers one target-sized one-cent order only when exactly one side is empty and the other meets target. Of 29 such markets, 16 would cross an opposite 99-cent bid and cannot supply a wholly resting target at that price. Thirteen permit a resting one-cent quote; only three have ideal remaining half-pool rewards exceeding the $10 principal of one full losing fill. These are Netflix top-show views, Claude top-model ranking, and weekly U.S. gas prices. Their ideal gross rates are approximately $0.39, $0.65 and $0.32 per hour respectively. This is a feasibility filter, not a claim that a fill loss occurs only once or that the reward lasts long enough to offset it.', '',
        'The entry screen was selected after seeing the survey and is not an independent holdout. It led to the separately preregistered AMS-005 full-catalog screen.', '',
        '## Interpretation and limitations', '',
        'These are depth gaps, not measured profitable trades. Depth is total resting contract quantity; a candidate still needs valid quote prices, genuine fill exposure, reward scoring, eligibility, and sufficient remaining time. No orders were placed and no reward or profit was realized.', '',
        'The denominator is the sampled current positive-reward market frame, not all Kalshi markets. One snapshot per market cannot measure gap duration. Metadata and books were fetched at different times. Overlapping programs were reduced to one program ID per ticker, so another active program can impose a different target. Account eligibility and governing terms were not independently validated.', '',
        'The batch orderbook requests used comma-joined tickers and received HTTP 400 parameter-validation errors. The prespecified fallback used individual full-depth GETs and preserved the failures. A future collector should use the documented array encoding; frozen code was not changed during acquisition. Missing observations and time-window exclusions remain in the denominator table.', '',
        f"HTTP receipt statuses: {dict(collections.Counter(str(r['status']) for r in receipts.values()))}. Acquisition elapsed {data['elapsed_seconds']:.2f} seconds. Three focused classification tests passed before acquisition; raw-body hashes, frozen sources, panel hash, and individual-book classifications verified after acquisition.", '',
        'Hypothesis/specification commit: 49e46781b7af755f1303123824dee82d067724df. Acquisition/test freeze: 092eb61704cc0a64ca3df2efa899038e32c53759.', '',
        'Public scoring: https://help.kalshi.com/en/articles/13823851-liquidity-incentive-program',
        'Public catalog: https://docs.kalshi.com/api-reference/incentive-programs/get-incentives', '',
        'The archive contains raw receipts, code, tests, frozen specification, fixed panel and results. No process remains running after this bounded survey.']
    (ROOT/'RESULTS.md').write_text('\n'.join(lines)+'\n')
    hashes = {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(ROOT.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.name not in ('EVIDENCE_HASHES.json','ARCHIVE.json','AMS_004_Evidence.zip')}
    (ROOT/'EVIDENCE_HASHES.json').write_text(json.dumps(hashes,indent=2)+'\n')
    archive = ROOT/'AMS_004_Evidence.zip'
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for rel in list(hashes)+['EVIDENCE_HASHES.json']: z.write(ROOT/rel,rel)
    with zipfile.ZipFile(archive) as z: assert z.testzip() is None
    info = {'file':archive.name,'bytes':archive.stat().st_size,'sha256':hashlib.sha256(archive.read_bytes()).hexdigest()}
    (ROOT/'ARCHIVE.json').write_text(json.dumps(info,indent=2)+'\n')
    print(json.dumps({'usable':usable,'gaps':len(gaps),'counts':counts,'archive':info},indent=2))

if __name__ == '__main__': main()
