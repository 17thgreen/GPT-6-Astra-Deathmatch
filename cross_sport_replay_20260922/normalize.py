"""Validate the entire frozen M2 cohort and normalize observations for Q7.

No winner, final price, candle volume or future mark enters the strategy tape.
Missing minutes remain missing. The 60-second quote delay is hypothetical.
"""
import gzip
import hashlib
import json
import math
from collections import Counter
from decimal import Decimal
from pathlib import Path
from discover import epoch

ROOT = Path(__file__).resolve().parent


def read(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def lines(path):
    with gzip.open(path, 'rt') as stream:
        yield from (json.loads(line) for line in stream)


def number(value, grid=None):
    value = Decimal(str(value))
    if not value.is_finite() or (grid and value % Decimal(grid)):
        raise ValueError('Nonfinite or unsupported fixed-point value')
    return float(value)


def normalize_trade(t, ticker, start, end):
    at = epoch(t['created_time'])
    if t['ticker'] != ticker or t.get('is_block_trade') or not start <= at <= end:
        raise ValueError('Trade identity, block or window mismatch')
    yes = number(t['yes_price_dollars'], '.0001')
    no = number(t['no_price_dollars'], '.0001')
    size = number(t['count_fp'], '.01')
    side = t.get('taker_side')
    if side not in ('yes', 'no') or not 0 < yes < 1 or size <= 0 or abs(yes + no - 1) > 1e-9:
        raise ValueError('Invalid trade price, quantity or aggressor side')
    if not t.get('trade_id'):
        raise ValueError('Missing trade ID')
    return dict(at=at, ticker=ticker, taker_side=side, yes_price=yes,
                size=size, trade_id=t['trade_id'])


def normalize_quote(c, ticker, start, end):
    at = c['end_period_ts']
    if not math.isfinite(at) or at % 60 or not start <= at <= end:
        raise ValueError('Candle time outside window or minute grid')
    bid = c.get('yes_bid', {}).get('close_dollars')
    ask = c.get('yes_ask', {}).get('close_dollars')
    if bid is None or ask is None:
        return None
    bid, ask = number(bid, '.0001'), number(ask, '.0001')
    if not 0 <= bid <= 1 or not 0 <= ask <= 1:
        raise ValueError('Quote outside price bounds')
    # Retain crossed/locked/endpoint prices: they invalidate the engine book.
    return dict(at=at + 60, asof=at, ticker=ticker, bid=bid, ask=ask, kind='quote')


def covered_seconds(quotes, start, end):
    """Exact time with a usable received book, clipped to the declared interval."""
    quotes = sorted(quotes, key=lambda q: q['at'])
    total = 0.
    for i, q in enumerate(quotes):
        if not 0 < q['bid'] < q['ask'] < 1:
            continue
        stop = min(end, q['asof'] + 300,
                   quotes[i + 1]['at'] if i + 1 < len(quotes) else end)
        total += max(0, stop - max(start, q['at']))
    return total


def load(root=ROOT):
    cohort, capture = read(root / 'COHORT.json'), read(root / 'CAPTURE.json')
    if not cohort['complete'] or len(cohort['games']) != 8 or not capture.get('complete') or capture['failures']:
        raise ValueError('Incomplete frozen cohort/capture; no subset replay permitted')
    if Counter(g['series'] for g in cohort['games']) != {'KXNCAAFGAME': 4, 'KXWNBAGAME': 4}:
        raise ValueError('Sport composition changed')
    expected = {t for g in cohort['games'] for t in g['tickers']}
    captured = [m['ticker'] for m in capture['markets']]
    if len(captured) != 16 or set(captured) != expected:
        raise ValueError('Missing, duplicate or substituted market capture')
    indexes = {m['ticker']: m for m in capture['markets']}
    markets, records, coverage, seen = {}, [], [], {}
    hashes = {'COHORT.json': sha(root / 'COHORT.json'), 'CAPTURE.json': sha(root / 'CAPTURE.json')}
    for g in cohort['games']:
        ms = g['metadata'].get('markets', g['metadata']['event'].get('markets', []))
        if not g['admitted'] or len(ms) != 2 or sorted(m['ticker'] for m in ms) != g['tickers']:
            raise ValueError('Unadmitted or changed event')
        for m in sorted(ms, key=lambda m: m['ticker']):
            ticker, kickoff = m['ticker'], g['kickoff']
            start, end = max(kickoff - 604800, epoch(m['open_time'])), kickoff - 10800 + 300
            if start >= kickoff - 10800 - 300:
                raise ValueError('No opening window for reserved market')
            folder = root / 'data' / ticker
            manifest = read(folder / 'manifest.json')
            if manifest != indexes[ticker] or not manifest['pagination_exhausted']:
                raise ValueError('Manifest mismatch or unfinished pagination')
            for key, val in dict(event=g['event'], series=g['series'], ticker=ticker,
                                 kickoff=kickoff, start=start, end=end).items():
                if manifest[key] != val:
                    raise ValueError('Capture identity/window changed: ' + key)
            for name, digest in manifest['sha256'].items():
                if name not in ('trades.jsonl.gz', 'candles.jsonl.gz') or sha(folder / name) != digest:
                    raise ValueError('Raw input checksum mismatch')
                hashes[str((folder / name).relative_to(root))] = digest
            if set(manifest['sha256']) != {'trades.jsonl.gz', 'candles.jsonl.gz'}:
                raise ValueError('Incomplete raw input hashes')
            hashes[str((folder / 'manifest.json').relative_to(root))] = sha(folder / 'manifest.json')
            markets[ticker] = dict(event=g['event'], direction=1 if ticker == g['tickers'][0] else -1,
                                   kickoff=kickoff, listed_at=epoch(m['open_time']),
                                   series=g['series'], verified_mecnet=True)
            trades, quotes, minutes = [], [], set()
            nulls = 0
            for t in lines(folder / 'trades.jsonl.gz'):
                row = normalize_trade(t, ticker, start, end)
                if row['trade_id'] in seen:
                    raise ValueError('Duplicate trade ID in finalized capture')
                seen[row['trade_id']] = row
                trades.append(row)
            for c in lines(folder / 'candles.jsonl.gz'):
                if c['end_period_ts'] in minutes:
                    raise ValueError('Duplicate candle minute')
                minutes.add(c['end_period_ts'])
                row = normalize_quote(c, ticker, start, end)
                if row is None:
                    nulls += 1
                else:
                    quotes.append(row)
            if len(trades) != manifest['trades'] or len(minutes) != manifest['candles']:
                raise ValueError('Raw row count mismatch')
            stop = kickoff - 10800 - 300
            expected_minutes = set(range(math.ceil(start / 60) * 60, math.floor(end / 60) * 60 + 1, 60))
            coverage.append(dict(ticker=ticker, event=g['event'], series=g['series'],
                listing_window_hours=(kickoff - 10800 - start) / 3600,
                expected_candle_minutes=len(expected_minutes), observed_candle_minutes=len(minutes),
                missing_candle_minutes=len(expected_minutes - minutes), null_quotes=nulls,
                usable_quote_seconds=covered_seconds(quotes, start, stop),
                entry_window_seconds=stop - start, trades=len(trades), quotes=len(quotes),
                first_trade=min(t['at'] for t in trades) if trades else None,
                quote_coverage_fraction=covered_seconds(quotes, start, stop) / (stop - start)))
            records.extend(trades)
            records.extend(quotes)
    records.sort(key=lambda r: (r['at'], 0 if r.get('kind') == 'quote' else 1, r.get('trade_id', r['ticker'])))
    return records, markets, dict(markets=coverage, sha256=hashes,
        evidence='RETROSPECTIVE_RECONSTRUCTED_SCHEDULE_AND_DELAYED_CANDLE_QUOTES')


if __name__ == '__main__':
    records, markets, report = load()
    (ROOT / 'INPUT_AUDIT.json').write_text(json.dumps(report, indent=2))
    print('Validated', len(markets), 'markets and', len(records), 'observations')
