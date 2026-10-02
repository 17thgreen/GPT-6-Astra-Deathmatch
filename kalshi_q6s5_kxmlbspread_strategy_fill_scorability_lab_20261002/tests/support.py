"""Shared fixtures. Synthetic clocks stay outside the ADMIT-1 window."""
import hashlib
import json
import sys
from pathlib import Path

LAB = Path(__file__).resolve().parents[1]
if str(LAB) not in sys.path:
    sys.path.insert(0, str(LAB))

import tape_quotes
from tape_quotes import canonical_bytes

DET = 'KXMLBSPREAD-26SEP251840PITDET-DET2'
PIT = 'KXMLBSPREAD-26SEP251840PITDET-PIT2'
SEP24 = 'KXMLBSPREAD-26SEP242140HOUATH-ATH2'
T0 = '2026-09-25T05:00:00Z'
T1 = '2026-09-25T05:10:00Z'
TAPE_END = '2026-09-25T06:00:00Z'
CLOSE = '2026-09-26T02:00:40Z'
SETTLE = '2026-09-26T02:02:46.599505Z'
RESPONSE = '2026-10-02T03:29:21.110655Z'


def snapshot(ticker, captured, yes=('0.4000', '2.00'), no=('0.4000', '2.00'), path=None):
    book = {'yes_dollars': [], 'no_dollars': []}
    if yes is not None:
        book['yes_dollars'] = [[yes[0], yes[1]]]
    if no is not None:
        book['no_dollars'] = [[no[0], no[1]]]
    return {
        'ticker': ticker,
        'captured_utc': captured,
        'orderbook_fp': book,
        'path': path or (ticker + '|' + captured),
    }


def market(ticker, captured, status='active'):
    return {
        'ticker': ticker,
        'captured_utc': captured,
        'status': status,
        'path': 'get|' + ticker + '|' + captured,
    }


def trade(ticker, created, taker_side, yes, no, count='3.00', trade_id='t1', block=False):
    if taker_side == 'yes':
        outcome, book_side = 'yes', 'bid'
    else:
        outcome, book_side = 'no', 'ask'
    return {
        'ticker': ticker,
        'created_time': created,
        'taker_side': taker_side,
        'taker_outcome_side': outcome,
        'taker_book_side': book_side,
        'yes_price_dollars': yes,
        'no_price_dollars': no,
        'count_fp': count,
        'trade_id': trade_id,
        'is_block_trade': block,
    }


def quote(snapshots, gets=None, ends=None):
    tickers = []
    for row in snapshots:
        if row['ticker'] not in tickers:
            tickers.append(row['ticker'])
    if gets is None:
        gets = [market(ticker, '2026-09-25T04:50:00Z') for ticker in tickers]
    if ends is None:
        ends = {ticker: TAPE_END for ticker in tickers}
    return tape_quotes.build_quotes(snapshots, gets, ends, trades=None)


def filled_row(ticker, fill_time, filled=True):
    return {
        'ticker': ticker,
        'captured_utc': T0,
        'leg': 'maker',
        'side': 'yes',
        'filled': filled,
        'fill_price': '0.4000' if filled else None,
        'fill_time': fill_time if filled else None,
        'quantity': '1' if filled else None,
        'requested': True,
        'role': 'maker',
        'content_fresh_flag': True,
        'observed': False,
        'tag': 'replay',
    }


def fills_bytes(rows):
    return canonical_bytes({'rows': rows, 'counts': {}})


def _sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_settlement(
    directory,
    ticker=DET,
    value='0.0000',
    status='finalized',
    close_time=CLOSE,
    settlement_ts=SETTLE,
    response_utc=RESPONSE,
    contradict=False,
):
    """Internally consistent settlement directory. Digests are recomputed after the body."""
    root = Path(directory)
    raw_dir = root / 'raw'
    raw_dir.mkdir(parents=True, exist_ok=True)
    market_body = {
        'ticker': ticker,
        'status': status,
        'settlement_value_dollars': value,
    }
    if close_time is not None:
        market_body['close_time'] = close_time
    if settlement_ts is not None:
        market_body['settlement_ts'] = settlement_ts
    if contradict:
        market_body['result'] = 'yes' if str(value).startswith('0') else 'no'
    raw_path = raw_dir / (ticker + '.json')
    raw_path.write_text(json.dumps({'market': market_body}))
    summary = root / 'SETTLEMENT_SUMMARY.json'
    summary.write_text('{}\n')
    raw_sha = _sha(raw_path)
    request = {
        'ticker': ticker,
        'response_utc': response_utc,
        'http_status': 200,
        'sha256': raw_sha,
        'raw_path': 'raw/' + ticker + '.json',
    }
    requests_path = root / 'requests.jsonl'
    requests_path.write_text(json.dumps(request) + '\n')
    lines = [
        '%s  %s\n' % (_sha(summary), 'SETTLEMENT_SUMMARY.json'),
        '%s  %s\n' % (raw_sha, 'raw/' + ticker + '.json'),
        '%s  %s\n' % (_sha(requests_path), 'requests.jsonl'),
    ]
    digests = root / 'DIGESTS.txt'
    digests.write_text(''.join(lines))
    ready = {
        'digests_txt_sha256': _sha(digests),
        'n_200': 1,
    }
    (root / 'COLLECTOR_READY_SETTLEMENT_ONLY.json').write_text(json.dumps(ready))
    return root
