"""Tape-to-quote builder for the Sep-25 KXMLBSPREAD scorability lab.

Rules R01 and R03–R12, R20–R21, R26, and R29–R30. The builder reads books,
market-status GETs, and tape-end stamps only. It takes no trades argument.
Settlement fields are not read here.
"""
import hashlib
import importlib.util
import re
import sys
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path


LAB_ROOT = Path(__file__).resolve().parent
REPO_ROOT = LAB_ROOT.parent
ONE = Decimal('1')
CONTRACTS = '1'
PRE_ADMITTED_AT = datetime(2026, 9, 25, 4, 37, 47, tzinfo=timezone.utc)
ADMIT1_START = datetime(2026, 9, 27, 0, 0, tzinfo=timezone.utc)
ADMIT1_END = datetime(2026, 9, 30, 4, 0, tzinfo=timezone.utc)
UNIVERSE = (
    'KXMLBSPREAD-26SEP251840PITDET-DET2',
    'KXMLBSPREAD-26SEP251840PITDET-PIT2',
    'KXMLBSPREAD-26SEP251840TBPHI-PHI2',
    'KXMLBSPREAD-26SEP251840TBPHI-TB2',
    'KXMLBSPREAD-26SEP251845NYMWSH-NYM2',
    'KXMLBSPREAD-26SEP251845NYMWSH-WSH2',
)
UNIVERSE_SET = frozenset(UNIVERSE)
SEP24_TOKENS = ('26SEP24', 'HOUATH', 'LAASEA', 'SDLAD')
NAME_RE = re.compile(r'__(20\d{6}T\d{6}Z)__([A-Za-z0-9.-]+)\.json$')
FEEBOOK_SHA256 = 'eaf5aac7126efcd574c972fa77438c4118d44d50acafa17c504bdd48768bebe7'
FEE_STUB_SHA256 = '600d56beda64c2edd9af2c9d220398ff1a7158dba140603a42f7cb7f95212384'
RAILS_SHA256 = '834386506dd72210d77ee063d4a96248d76ce09a4be6ce771b9609337d3388e1'
HYGIENE_SHA256 = '65310a88ec7602a3fa2e50f2444e64c431dd29ef648992cb7861a5b74ca3b69f'
SNAPSHOT_KEYS = frozenset(('ticker', 'captured_utc', 'orderbook_fp', 'path'))
MARKET_GET_KEYS = frozenset(('ticker', 'captured_utc', 'status', 'path'))

_FRESH = None


class LabError(Exception):
    pass


class ClosedUniverseRefused(LabError):
    pass


class LookaheadRefused(LabError):
    pass


class Admit1WindowRejected(LabError):
    pass


class PinMismatch(LabError):
    pass


class CaptureSqliteRefused(LabError):
    pass


def sha256_file(path):
    digest = hashlib.sha256()
    digest.update(Path(path).read_bytes())
    return digest.hexdigest()


def parse_ts(value):
    if not isinstance(value, str) or not value.endswith('Z') or 'T' not in value:
        raise LabError('timestamp')
    parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if parsed.tzinfo is None:
        raise LabError('timestamp')
    return parsed.astimezone(timezone.utc)


def in_admit1_window(value):
    """R30. Half-open window [2026-09-27T00:00:00Z, 2026-09-30T04:00:00Z)."""
    stamp = value if isinstance(value, datetime) else parse_ts(value)
    return ADMIT1_START <= stamp < ADMIT1_END


def assert_open_universe(ticker):
    """R01. Sep-24 KXMLBSPREAD and the KXHIGH snapshot are closed."""
    if not isinstance(ticker, str) or ticker not in UNIVERSE_SET:
        raise ClosedUniverseRefused(ticker)
    upper = ticker.upper()
    if upper.startswith('KXHIGH') or any(token in upper for token in SEP24_TOKENS):
        raise ClosedUniverseRefused(ticker)
    return ticker


def refuse_sqlite_path(path):
    """Refuse capture.sqlite and the weather archive without opening them."""
    text = str(path).replace('\\', '/')
    name = text.rstrip('/').split('/')[-1]
    if (
        name == 'capture.sqlite'
        or name == 'archive.sqlite'
        or text.endswith('capture.sqlite')
        or text.endswith('archive.sqlite')
        or 'weather-nowcast/archive.sqlite' in text
    ):
        raise CaptureSqliteRefused(text)
    return text


def stamp_from_name(name):
    """R04. captured_utc is the filename stamp YYYYMMDDTHHMMSSZ."""
    match = NAME_RE.search(str(name).replace('\\', '/'))
    if match is None:
        return None
    raw = match.group(1)
    ticker = match.group(2)
    iso = (
        raw[0:4] + '-' + raw[4:6] + '-' + raw[6:8]
        + 'T' + raw[9:11] + ':' + raw[11:13] + ':' + raw[13:15] + 'Z'
    )
    return iso, ticker


def canonical_bytes(payload):
    import json
    return json.dumps(
        payload, sort_keys=True, separators=(',', ':'), ensure_ascii=False,
    ).encode('utf-8')


def _require_sha(path, expected):
    refuse_sqlite_path(path)
    got = sha256_file(path)
    if got != expected:
        raise PinMismatch(path)
    return got


def freshness_modules():
    """R26. rails canonical content and hygiene content_fresh_flag."""
    global _FRESH
    if _FRESH is not None:
        return _FRESH
    feebook_path = REPO_ROOT / 'kalshi_feebook_lab_20260922' / 'feebook.py'
    stub_path = REPO_ROOT / 'kalshi_feebook_lab_20260922' / 'series_fee_table.stub.json'
    rails_path = REPO_ROOT / 'kalshi_rails_lab_20260922' / 'rails.py'
    hygiene_path = REPO_ROOT / 'kalshi_r2p1_hygiene_000_lab_20260922' / 'hygiene.py'
    _require_sha(feebook_path, FEEBOOK_SHA256)
    _require_sha(stub_path, FEE_STUB_SHA256)
    _require_sha(rails_path, RAILS_SHA256)
    _require_sha(hygiene_path, HYGIENE_SHA256)
    for directory in (feebook_path.parent, rails_path.parent):
        text = str(directory)
        if text not in sys.path:
            sys.path.insert(0, text)
    spec = importlib.util.spec_from_file_location('q6s5_hygiene_r26', hygiene_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules['q6s5_hygiene_r26'] = module
    spec.loader.exec_module(module)
    rails = sys.modules['rails']
    _FRESH = (module, rails)
    return _FRESH


def _best_level(levels):
    """R06–R07. Maker price is the max displayed bid. Size at that price is as-is."""
    if not levels:
        return None
    grouped = {}
    for pair in levels:
        price_text = pair[0]
        size_text = pair[1]
        price = Decimal(price_text)
        slot = grouped.get(price)
        if slot is None:
            grouped[price] = {
                'text': price_text,
                'size': Decimal(size_text),
                'size_text': size_text,
                'n': 1,
            }
        else:
            slot['size'] += Decimal(size_text)
            slot['n'] += 1
    best = max(grouped)
    slot = grouped[best]
    if slot['n'] == 1:
        size_text = slot['size_text']
    else:
        size_text = format(slot['size'], 'f')
    return {
        'price_text': slot['text'],
        'price': best,
        'size_text': size_text,
        'size': slot['size'],
    }


def _reject_extra(record, allowed, kind):
    extra = set(record) - allowed
    if extra:
        raise LookaheadRefused(kind)


def _status_at(ticker, captured_utc, market_gets):
    """R05. Latest dated market GET with stamp <= captured_utc."""
    t0 = parse_ts(captured_utc)
    chosen = None
    for row in market_gets:
        _reject_extra(row, MARKET_GET_KEYS, 'market get')
        assert_open_universe(row['ticker'])
        if in_admit1_window(row['captured_utc']):
            raise Admit1WindowRejected(row['captured_utc'])
        if row['ticker'] != ticker:
            continue
        stamp = parse_ts(row['captured_utc'])
        if stamp <= t0:
            key = (stamp, row.get('path') or '')
            if chosen is None or key >= chosen[0]:
                chosen = (key, row['status'])
    if chosen is None:
        return None
    return chosen[1]


def _cancel(index, series, market_gets, tape_end):
    """R11 for a later snapshot. R12 for the last order."""
    current = series[index]
    if index + 1 < len(series):
        return series[index + 1]['captured_utc'], 'next_snapshot'
    t0 = parse_ts(current['captured_utc'])
    end = parse_ts(tape_end)
    if in_admit1_window(end):
        raise Admit1WindowRejected(tape_end)
    best = (end, tape_end, 'tape_end')
    for row in market_gets:
        if row['ticker'] != current['ticker']:
            continue
        stamp = parse_ts(row['captured_utc'])
        if stamp <= t0:
            continue
        if row['status'] != 'active' and stamp < best[0]:
            best = (stamp, row['captured_utc'], 'status_not_active')
    return best[1], best[2]


def _taker_leg(opposite):
    """R20. Best opposite level only. Size must be >= 1. No book walk."""
    if opposite is None or opposite['size'] < 1:
        return None
    price = ONE - opposite['price']
    return {
        'price': format(price, 'f'),
        'opposite_best_size': opposite['size_text'],
        'size': CONTRACTS,
    }


def build_quotes(snapshots, market_gets, tape_ends, trades=None):
    """Place both sides at each dated snapshot. Passing trades is lookahead."""
    if trades is not None:
        raise LookaheadRefused('trades')
    if snapshots is None or market_gets is None or tape_ends is None:
        raise LabError('inputs')
    hygiene, rails = freshness_modules()
    ordered = sorted(
        snapshots,
        key=lambda row: (
            row.get('ticker') or '',
            row.get('captured_utc') or '',
            row.get('path') or '',
        ),
    )
    by_ticker = {ticker: [] for ticker in UNIVERSE}
    previous = {}
    annotated = []
    for row in ordered:
        _reject_extra(row, SNAPSHOT_KEYS, 'snapshot')
        ticker = assert_open_universe(row['ticker'])
        if in_admit1_window(row['captured_utc']):
            raise Admit1WindowRejected(row['captured_utc'])
        book = row['orderbook_fp']
        if not isinstance(book, dict):
            raise LabError('orderbook_fp')
        content = rails.canonical_book_content(book)
        current = rails.BookObservation(content=content, transaction_time=None)
        flag = hygiene.content_fresh_flag(previous.get(ticker), current, keepalive=False)
        previous[ticker] = current
        yes = _best_level(book.get('yes_dollars') or [])
        no = _best_level(book.get('no_dollars') or [])
        item = {
            'ticker': ticker,
            'captured_utc': row['captured_utc'],
            'path': row.get('path') or '',
            'yes': yes,
            'no': no,
            'content_fresh_flag': bool(flag['content_fresh_flag']),
            'fresh_reason': flag['reason'],
        }
        annotated.append(item)
        by_ticker[ticker].append(item)
    for ticker, series in by_ticker.items():
        series.sort(key=lambda row: (parse_ts(row['captured_utc']), row['path']))
    rows = []
    counts = {
        'n_books': len(annotated),
        'eligible_placements': 0,
        'crossed_or_locked_n': 0,
        'empty_side_n': 0,
        'fresh_n': 0,
        'stale_n': 0,
        'requested_maker_contracts': 0,
        'requested_taker_contracts': 0,
    }
    for item in annotated:
        ticker = item['ticker']
        series = by_ticker[ticker]
        index = series.index(item)
        if ticker not in tape_ends:
            raise LabError('tape end missing')
        cancel_utc, cancel_reason = _cancel(index, series, market_gets, tape_ends[ticker])
        status = _status_at(ticker, item['captured_utc'], market_gets)
        crossed = False
        if item['yes'] is not None and item['no'] is not None:
            if item['yes']['price'] + item['no']['price'] >= ONE:
                crossed = True
        skip = None
        eligible = False
        if status != 'active':
            skip = 'no_status_get' if status is None else 'status_not_active'
        elif crossed:
            skip = 'crossed_or_locked'
            counts['crossed_or_locked_n'] += 1
        else:
            eligible = True
            counts['eligible_placements'] += 1
            if item['content_fresh_flag']:
                counts['fresh_n'] += 1
            else:
                counts['stale_n'] += 1
        yes_maker = None
        no_maker = None
        yes_taker = None
        no_taker = None
        if eligible:
            if item['yes'] is None:
                counts['empty_side_n'] += 1
            else:
                yes_maker = {
                    'price': item['yes']['price_text'],
                    'queue_ahead': item['yes']['size_text'],
                    'size': CONTRACTS,
                }
                counts['requested_maker_contracts'] += 1
            if item['no'] is None:
                counts['empty_side_n'] += 1
            else:
                no_maker = {
                    'price': item['no']['price_text'],
                    'queue_ahead': item['no']['size_text'],
                    'size': CONTRACTS,
                }
                counts['requested_maker_contracts'] += 1
            yes_taker = _taker_leg(item['no'])
            no_taker = _taker_leg(item['yes'])
            if yes_taker is not None:
                counts['requested_taker_contracts'] += 1
            if no_taker is not None:
                counts['requested_taker_contracts'] += 1
        placed_at = parse_ts(item['captured_utc'])
        rows.append({
            'ticker': ticker,
            'captured_utc': item['captured_utc'],
            'cancel_utc': cancel_utc,
            'cancel_reason': cancel_reason,
            'eligible': eligible,
            'skip_reason': skip,
            'crossed_or_locked': crossed,
            'content_fresh_flag': item['content_fresh_flag'],
            'fresh_reason': item['fresh_reason'],
            'pre_admitted_at': placed_at < PRE_ADMITTED_AT,
            'yes_maker': yes_maker,
            'no_maker': no_maker,
            'yes_taker': yes_taker,
            'no_taker': no_taker,
        })
    rows.sort(key=lambda row: (row['ticker'], row['captured_utc']))
    return {'rows': rows, 'counts': counts}
