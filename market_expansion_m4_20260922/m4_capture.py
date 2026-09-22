"""Complete fixed cohorts across historical/live boundaries with failure retention."""
import concurrent.futures
import math
from decimal import Decimal
from m4_common import ROOT, get, epoch, read, save, sha, write_rows


def trade_intervals(start, end, cutoff):
    if not all(math.isfinite(x) for x in (start, end, cutoff)) or end < start:
        raise ValueError('Invalid storage interval')
    intervals = []
    # The boundary second is queried on both tiers and deduplicated by trade ID.
    if start <= cutoff:
        intervals.append(('historical/trades', start, min(end, cutoff)))
    if end >= cutoff:
        intervals.append(('markets/trades', max(start, cutoff), end))
    return intervals


def quote_schema(candle, historical):
    result = dict(candle)
    if historical:
        for side in ('yes_bid', 'yes_ask'):
            data = dict(candle.get(side, {}))
            if 'close_dollars' not in data and 'close' in data:
                value = data['close']
                # Historical docs specify dollar strings, never guess cents.
                if value is not None and (not isinstance(value, str) or not 0 <= Decimal(value) <= 1):
                    raise ValueError('Ambiguous historical quote units')
                data['close_dollars'] = value
            elif 'close_dollars' in data and 'close' in data and data['close'] is not None:
                if Decimal(str(data['close'])) != Decimal(str(data['close_dollars'])):
                    raise ValueError('Conflicting historical quote fields')
            result[side] = data
    return result


def capture(game, market, cutoffs):
    ticker = market['ticker']
    folder = ROOT/'data'/ticker
    folder.mkdir(parents=True, exist_ok=True)
    manifest_path = folder/'manifest.json'
    if manifest_path.exists():
        manifest = read(manifest_path)
        if all(sha(folder/name) == digest for name,digest in manifest['sha256'].items()):
            return manifest
        raise ValueError('Existing capture changed')
    start = max(game['kickoff']-604800, epoch(market['open_time']))
    end = game['kickoff']-1500
    sources, trades, candles, raw_pages = [], {}, {}, []
    trade_cutoff = epoch(cutoffs['trades_created_ts'])
    settled = market.get('settlement_ts')
    archived = bool(settled and epoch(settled) < epoch(cutoffs['market_settled_ts']))
    try:
        for path, lo, hi in trade_intervals(start, end, trade_cutoff):
            cursor, seen = None, set()
            for _ in range(200):
                params = dict(ticker=ticker, min_ts=int(lo), max_ts=int(hi), limit=1000, is_block_trade='false')
                if cursor:
                    params['cursor'] = cursor
                data, source = get(path, params)
                sources.append(source)
                raw_pages.append(dict(source=source, response=data))
                for trade in data.get('trades', []):
                    at = epoch(trade['created_time'])
                    if trade['ticker'] != ticker or trade.get('is_block_trade') or not start <= at <= end:
                        raise ValueError('Trade identity/block/window mismatch')
                    key = trade['trade_id']
                    if key in trades and trades[key] != trade:
                        raise ValueError('Conflicting duplicate trade')
                    trades[key] = trade
                cursor = data.get('cursor')
                if not cursor:
                    break
                if cursor in seen:
                    raise ValueError('Repeated trade cursor')
                seen.add(cursor)
            else:
                raise ValueError('Trade pagination incomplete')
        path = ('historical/markets/'+ticker+'/candlesticks' if archived else
                'series/'+game['series']+'/markets/'+ticker+'/candlesticks')
        lo = int(start)
        while lo < end:
            hi = min(int(end), lo+3*86400)
            data, source = get(path, dict(start_ts=lo, end_ts=hi, period_interval=1))
            sources.append(source)
            raw_pages.append(dict(source=source, response=data))
            if data.get('ticker', ticker) != ticker:
                raise ValueError('Candle market mismatch')
            for candle in data.get('candlesticks', []):
                at = candle['end_period_ts']
                if not start <= at <= end:
                    raise ValueError('Candle outside declared window')
                if at in candles and candles[at] != candle:
                    raise ValueError('Conflicting candle boundary')
                candles[at] = candle
            lo = hi
    except Exception as error:
        write_rows(folder/'partial_responses.jsonl.gz', raw_pages)
        save(folder/'failure.json', dict(error=str(error), sources=sources,
             partial_sha256=sha(folder/'partial_responses.jsonl.gz')))
        raise
    write_rows(folder/'trades.jsonl.gz', sorted(trades.values(), key=lambda t:(t['created_time'],t['trade_id'])))
    write_rows(folder/'candles.jsonl.gz', [candles[t] for t in sorted(candles)])
    # Parsed original row values are retained; request/response envelopes aren't
    # duplicated after complete success. Partial envelopes survive failed capture.
    manifest = dict(ticker=ticker, event=game['event'], series=game['series'],
        kickoff=game['kickoff'], start=start, end=end, pagination_exhausted=True,
        archived_candles=archived, trades=len(trades), candles=len(candles), sources=sources,
        sha256={name:sha(folder/name) for name in ('trades.jsonl.gz','candles.jsonl.gz')})
    save(manifest_path, manifest)
    print(ticker, len(trades), 'trades', len(candles), 'candles', flush=True)
    return manifest


def main():
    cohort = read(ROOT/'COHORT.json')
    out = dict(markets=[], failures=[], sports={})
    tasks = [(g,m) for g in cohort['games'] if g['replay_admitted'] for m in g['markets']]
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        futures = {pool.submit(capture,g,m,cohort['cutoffs']['response']):(g['series'],m['ticker']) for g,m in tasks}
        for future in concurrent.futures.as_completed(futures):
            try:
                out['markets'].append(future.result())
            except Exception as error:
                series,ticker = futures[future]
                out['failures'].append(dict(series=series,ticker=ticker,error=str(error)))
                print('FAILED', ticker, str(error), flush=True)
            save(ROOT/'CAPTURE.partial.json', out)
    for series in ('KXNCAAFGAME','KXMLBGAME'):
        expected = {m['ticker'] for g in cohort['games'] if g['series']==series and g['replay_admitted'] for m in g['markets']}
        actual = {m['ticker'] for m in out['markets'] if m['series']==series}
        out['sports'][series] = dict(complete=len(expected)==16 and actual==expected and
            not any(f['series']==series for f in out['failures']), expected_markets=len(expected), captured_markets=len(actual))
    save(ROOT/'CAPTURE.json',out)
    print('CAPTURE_STATUS', out['sports'], flush=True)


if __name__ == '__main__':
    main()
