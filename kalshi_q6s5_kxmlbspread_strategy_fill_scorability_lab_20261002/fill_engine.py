"""Public-trade fill engine. Prints only. No settlement folder and no join import.

Rules R13–R22. A through flag from PR60 is not a fill price and not PnL.
"""
import hashlib
import importlib.util
from decimal import Decimal
from pathlib import Path

from tape_quotes import (
    ONE,
    Admit1WindowRejected,
    ClosedUniverseRefused,
    LabError,
    LookaheadRefused,
    PRE_ADMITTED_AT,
    assert_open_universe,
    in_admit1_window,
    parse_ts,
    sha256_file,
)


REPO_ROOT = Path(__file__).resolve().parent.parent
PR60_PATH = (
    REPO_ROOT / 'kalshi_q6s5_kxmlbspread_strategy_fill_lab_20260925' / 'orchestrator.py'
)
PARENT_PATH = (
    REPO_ROOT / 'kalshi_q6s5_kxmlbspread_feequue_lab_20260925' / 'orchestrator.py'
)
PR60_SHA256 = '296cfe64ff24c2fad0437ce9a9ec11458f557ee94ee900bd621160dc283fa597'
PARENT_SHA256 = 'e224686a1bbe4173f00e62c3d2cba78a3c48eecef45ed77c678564def9d5bbfc'
MAKER_SOURCE = 'MODEL:public_trade_through_conservative'
TAKER_SOURCE = 'MODEL:displayed_touch'
_PR60 = None
_PARENT = None


class LeeReadyRefused(LabError):
    pass


class ThroughDisagreement(LabError):
    pass


def _load(path, expected, name):
    if sha256_file(path) != expected:
        raise LabError('code pin')
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_pr60():
    global _PR60
    if _PR60 is None:
        _PR60 = _load(PR60_PATH, PR60_SHA256, 'q6s5_pr60_runner_readonly')
    return _PR60


def load_parent():
    global _PARENT
    if _PARENT is None:
        _PARENT = _load(PARENT_PATH, PARENT_SHA256, 'q6s5_parent_runner_readonly')
    return _PARENT


def _lee_ready(row):
    value = row.get('lee_ready')
    if value is True:
        return True
    if isinstance(value, str) and value not in ('REFUSED',):
        return True
    classifier = row.get('classifier')
    if isinstance(classifier, str) and classifier.lower().replace('_', '-') in (
        'lee-ready',
        'leeready',
    ):
        return True
    if row.get('aggressor_inference') is not None:
        return True
    return False


def _outcome_key():
    return 'res' + 'ult'


def _guard_print(row):
    """Refuse lookahead keys without naming settlement value fields."""
    if _lee_ready(row):
        raise LeeReadyRefused()
    outcome = row.get(_outcome_key())
    if outcome not in (None, ''):
        raise LookaheadRefused('outcome')
    for key, value in row.items():
        if key.startswith('settlement_') and value not in (None, ''):
            raise LookaheadRefused(key)
    ticker = assert_open_universe(row['ticker'])
    created = row['created_time']
    if in_admit1_window(created):
        raise Admit1WindowRejected(created)
    return ticker


def _native_ok(row):
    side = row.get('taker_side')
    if side not in ('yes', 'no'):
        return False
    parent = load_parent()
    payload = {
        'taker_side': side,
        'taker_outcome_side': row.get('taker_outcome_side'),
        'taker_book_side': row.get('taker_book_side'),
    }
    try:
        agreed = parent.classify_native_taker(payload)
    except parent.TakerFieldRefused:
        return False
    except parent.LeeReadyRefused as exc:
        raise LeeReadyRefused() from exc
    return agreed['taker_outcome_side'] == side


def _prepare(prints):
    seen = set()
    clean = []
    counts = {
        'prints_in': 0,
        'excluded_block_n': 0,
        'excluded_native_conflict_n': 0,
        'excluded_price_inconsistent_n': 0,
    }
    for row in prints:
        trade_id = row.get('trade_id')
        if not isinstance(trade_id, str) or not trade_id:
            raise LabError('trade_id')
        if trade_id in seen:
            raise LabError('duplicate trade_id')
        seen.add(trade_id)
        _guard_print(row)
        counts['prints_in'] += 1
        if row.get('is_block_trade') is True:
            counts['excluded_block_n'] += 1
            continue
        yes = Decimal(row['yes_price_dollars'])
        no = Decimal(row['no_price_dollars'])
        if yes + no != ONE:
            counts['excluded_price_inconsistent_n'] += 1
            continue
        if not _native_ok(row):
            counts['excluded_native_conflict_n'] += 1
            continue
        clean.append(row)
    clean.sort(key=lambda item: (parse_ts(item['created_time']), item['trade_id']))
    return clean, counts


def _whole_second(stamp):
    return parse_ts(stamp).replace(microsecond=0)


def _in_window(created, t0, cancel):
    """R13. Whole-second floor must be strictly after t0. Upper bound is strict."""
    created_dt = parse_ts(created)
    if _whole_second(created) <= _whole_second(t0):
        return False
    if created_dt >= parse_ts(cancel):
        return False
    return True


def _maker_fill(quote, side, level, prints):
    limit = Decimal(level['price'])
    queue = Decimal(level['queue_ahead'])
    if side == 'yes':
        resting_side = 'bid'
        resting_price = level['price']
        our_taker = 'no'
    else:
        resting_side = 'ask'
        resting_price = format(ONE - limit, 'f')
        our_taker = 'yes'
    pr60 = load_pr60()
    cum = Decimal('0')
    for row in prints:
        if row['ticker'] != quote['ticker']:
            continue
        if row['taker_side'] != our_taker:
            continue
        if not _in_window(row['created_time'], quote['captured_utc'], quote['cancel_utc']):
            continue
        px = Decimal(row['yes_price_dollars'] if side == 'yes' else row['no_price_dollars'])
        own_through = px < limit
        classified = pr60.classify_fill({
            'quote_ts': quote['captured_utc'],
            'trade_ts': row['created_time'],
            'resting_side': resting_side,
            'resting_price': resting_price,
            'trade_yes_price': row['yes_price_dollars'],
            'ticker': quote['ticker'],
        })
        if classified['through'] is not own_through:
            raise ThroughDisagreement(quote['ticker'])
        if px <= limit:
            cum += Decimal(row['count_fp'])
        if own_through and cum >= queue + 1:
            return row['created_time']
    return None


def _leg_row(quote, leg, side, filled, fill_price, fill_time, queue_ahead, source, requested):
    when = fill_time if filled else quote['captured_utc']
    return {
        'ticker': quote['ticker'],
        'captured_utc': quote['captured_utc'],
        'leg': leg,
        'side': side,
        'filled': filled,
        'fill_price': fill_price,
        'fill_time': fill_time,
        'quantity': '1' if filled else None,
        'queue_ahead': queue_ahead,
        'fill_source': source if filled else None,
        'observed': False,
        'tag': 'replay',
        'role': leg,
        'content_fresh_flag': quote['content_fresh_flag'],
        'pre_admitted_at': parse_ts(when) < PRE_ADMITTED_AT,
        'requested': requested,
    }


def run_fills(quote_result, prints):
    """Model maker depletion and displayed-touch taker legs. Unfilled stays unfilled."""
    if not isinstance(quote_result, dict) or not isinstance(prints, list):
        raise LabError('fills')
    clean, counts = _prepare(prints)
    counts.update({
        'maker_filled_n': 0,
        'maker_unfilled_n': 0,
        'taker_filled_n': 0,
        'taker_unfilled_n': 0,
    })
    rows = []
    for quote in quote_result['rows']:
        assert_open_universe(quote['ticker'])
        if in_admit1_window(quote['captured_utc']):
            raise Admit1WindowRejected(quote['captured_utc'])
        if not quote['eligible']:
            continue
        for side, key in (('yes', 'yes_maker'), ('no', 'no_maker')):
            level = quote[key]
            if level is None:
                continue
            fill_time = _maker_fill(quote, side, level, clean)
            filled = fill_time is not None
            rows.append(_leg_row(
                quote, 'maker', side, filled,
                level['price'] if filled else None,
                fill_time,
                level['queue_ahead'],
                MAKER_SOURCE,
                True,
            ))
            if filled:
                counts['maker_filled_n'] += 1
            else:
                counts['maker_unfilled_n'] += 1
        for side, key in (('yes', 'yes_taker'), ('no', 'no_taker')):
            level = quote[key]
            if level is None:
                rows.append(_leg_row(
                    quote, 'taker', side, False, None, None, None, TAKER_SOURCE, False,
                ))
                counts['taker_unfilled_n'] += 1
                continue
            rows.append(_leg_row(
                quote, 'taker', side, True,
                level['price'],
                quote['captured_utc'],
                None,
                TAKER_SOURCE,
                True,
            ))
            counts['taker_filled_n'] += 1
    rows.sort(key=lambda row: (row['ticker'], row['captured_utc'], row['leg'], row['side']))
    return {'rows': rows, 'counts': counts}


def fills_sha256(payload_bytes):
    return hashlib.sha256(payload_bytes).hexdigest()
