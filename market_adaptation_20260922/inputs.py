import json
from pathlib import Path
from extend import ROOT, M2, sha
from normalize import load as load_m2, lines, normalize_trade, normalize_quote


def merge(base, extra):
    indexed = {}
    overlaps = 0
    for r in base + extra:
        key = ('quote', r['ticker'], r['asof']) if r.get('kind') == 'quote' else ('trade', r['trade_id'])
        if key in indexed:
            if indexed[key] != r:
                raise ValueError('Conflicting overlap: ' + str(key))
            overlaps += 1
        else:
            indexed[key] = r
    return sorted(indexed.values(), key=lambda r: (r['at'], 0 if r.get('kind') == 'quote' else 1,
                                                   r.get('trade_id', r['ticker']))), overlaps


def load():
    base, markets, old_audit = load_m2()
    capture = json.loads((ROOT / 'EXTENSION_CAPTURE.json').read_text())
    if not capture['complete'] or capture['failures'] or len(capture['markets']) != 16:
        raise ValueError('Incomplete extension; no subset replay')
    if {m['ticker'] for m in capture['markets']} != set(markets):
        raise ValueError('Changed extension cohort')
    extra, coverage, hashes = [], [], {'EXTENSION_CAPTURE.json': sha(ROOT / 'EXTENSION_CAPTURE.json')}
    for m in capture['markets']:
        t = m['ticker']
        actual = markets[t]['kickoff']
        if (m['start'], m['end'], m['event']) != (actual-10500, actual-1500, markets[t]['event']):
            raise ValueError('Changed extension window/identity')
        folder = ROOT / 'data' / t
        if json.loads((folder / 'manifest.json').read_text()) != m or not m['pagination_exhausted']:
            raise ValueError('Manifest changed')
        for n, digest in m['sha256'].items():
            if sha(folder / n) != digest:
                raise ValueError('Extension hash mismatch')
            hashes[str((folder / n).relative_to(ROOT))] = digest
        raw_trades = list(lines(folder / 'trades.jsonl.gz'))
        candles = list(lines(folder / 'candles.jsonl.gz'))
        if len(raw_trades) != m['trades'] or len(candles) != m['candles']:
            raise ValueError('Extension count mismatch')
        if len({c['end_period_ts'] for c in candles}) != len(candles):
            raise ValueError('Duplicate extension minute')
        if len({t['trade_id'] for t in raw_trades}) != len(raw_trades):
            raise ValueError('Duplicate extension trade')
        extra.extend(normalize_trade(row, t, m['start'], m['end']) for row in raw_trades)
        quotes = [normalize_quote(c, t, m['start'], m['end']) for c in candles]
        extra.extend(q for q in quotes if q is not None)
        coverage.append(dict(ticker=t, trades=len(raw_trades), minutes=len(candles),
            expected_minutes=151, missing_minutes=151-len(candles), null_prices=sum(q is None for q in quotes)))
    records, overlaps = merge(base, extra)
    return records, markets, dict(extension=coverage, overlaps=overlaps, old_input_hashes=old_audit['sha256'],
        sha256=hashes, records=len(records))


if __name__ == '__main__':
    records, markets, audit = load()
    (ROOT / 'INPUT_AUDIT.json').write_text(json.dumps(audit, indent=2))
    print('Verified M3 tape:', len(records), 'observations;', audit['overlaps'], 'identical overlap records')
