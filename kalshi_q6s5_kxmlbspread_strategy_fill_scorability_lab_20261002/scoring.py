"""Arm metrics and the PR62 cache fee, copied verbatim.

Empty bins and zero denominators stay null. Stresses do not change fills.
"""
import copy
import hashlib
import sys
from decimal import Decimal
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
FEEBOOK_PATH = REPO_ROOT / 'kalshi_feebook_lab_20260922' / 'feebook.py'
FEE_STUB_PATH = REPO_ROOT / 'kalshi_feebook_lab_20260922' / 'series_fee_table.stub.json'
FEEBOOK_SHA256 = 'eaf5aac7126efcd574c972fa77438c4118d44d50acafa17c504bdd48768bebe7'
FEE_STUB_SHA256 = '600d56beda64c2edd9af2c9d220398ff1a7158dba140603a42f7cb7f95212384'
SERIES = 'KXMLBSPREAD'
FEE_TYPE = 'quadratic'
FEE_MULTIPLIER = '0.5'
FEE_LABEL = 'CACHE_NOT_R1P1'
ONE = Decimal('1')
ONE_TICK = Decimal('0.01')


class OrchestratorError(Exception):
    pass


class CacheNotLiveR1P1(OrchestratorError):
    pass


def _sha256_file(path):
    digest = hashlib.sha256()
    digest.update(Path(path).read_bytes())
    return digest.hexdigest()


def _load_feebook():
    if _sha256_file(FEEBOOK_PATH) != FEEBOOK_SHA256:
        raise OrchestratorError('feebook pin')
    if _sha256_file(FEE_STUB_PATH) != FEE_STUB_SHA256:
        raise OrchestratorError('fee stub pin')
    folder = str(FEEBOOK_PATH.parent)
    if folder not in sys.path:
        sys.path.insert(0, folder)
    import feebook
    return feebook


feebook = _load_feebook()


def cache_fee_table():
    """FEE_PIN multiplier on the feebook table. formula_id is not claimed."""
    table = copy.deepcopy(feebook.load_series_table())
    table['default'] = dict(table['default'])
    table['default']['M'] = FEE_MULTIPLIER
    table['formula_id'] = None
    return table


def cache_order_fee(role, contracts, price, times=1):
    """CACHE secondary quote. Resolved maker terms are not asserted."""
    if times not in (1, 2):
        raise OrchestratorError('fee times')
    table = cache_fee_table()
    resolved = feebook.resolve_terms(table, SERIES, role)
    if 'multiplier' not in resolved:
        raise CacheNotLiveR1P1()
    quote = feebook.order_fee(
        role,
        contracts,
        price,
        round_up=True,
        series=SERIES,
        table=table,
    )
    fee = quote['fee'] * Decimal(times)
    labeled = {
        'role': role,
        'fee': fee,
        'fee_type': FEE_TYPE,
        'fee_multiplier': FEE_MULTIPLIER,
        'label': FEE_LABEL,
        'formula_id': None,
        'cache_labeled': True,
        'fee_honest': False,
        'claim_as_live_R1P1': False,
        'resolved_terms_asserted': False,
        'results': None,
        'pnl': None,
    }
    if labeled['formula_id'] is not None or labeled['claim_as_live_R1P1'] is not False:
        raise CacheNotLiveR1P1()
    if labeled['label'] != FEE_LABEL or labeled['fee_honest'] is not False:
        raise CacheNotLiveR1P1()
    return labeled


def _fee(role, price, times=1):
    labeled = cache_order_fee(role, 1, price, times=times)
    if labeled['formula_id'] is not None or labeled['label'] != FEE_LABEL:
        raise CacheNotLiveR1P1()
    return labeled['fee']


def _settle(side, value):
    if side == 'yes':
        return value
    if side == 'no':
        return ONE - value
    raise OrchestratorError('side')


def _resolved(fill_document, settlement_values):
    rows = []
    unresolved = []
    for row in fill_document.get('rows') or []:
        if not row.get('filled'):
            continue
        ticker = row['ticker']
        if ticker not in settlement_values:
            unresolved.append(row)
            continue
        value = settlement_values[ticker]
        if not isinstance(value, Decimal):
            value = Decimal(value)
        price = Decimal(row['fill_price'])
        fee = _fee(row['role'], row['fill_price'], times=1)
        pnl = _settle(row['side'], value) - price - fee
        rows.append({
            'ticker': ticker,
            'captured_utc': row['captured_utc'],
            'leg': row['leg'],
            'side': row['side'],
            'role': row['role'],
            'fill_price': price,
            'fee': fee,
            'pnl': pnl,
            'content_fresh_flag': bool(row['content_fresh_flag']),
            'filled': True,
        })
    return rows, unresolved


def _roi(rows):
    if not rows:
        return None, 'empty_bin'
    denom = sum((row['fill_price'] + row['fee'] for row in rows), Decimal('0'))
    if denom == 0:
        return None, 'zero_denominator'
    total = sum((row['pnl'] for row in rows), Decimal('0'))
    return total / denom, None


def _pnl(rows):
    if not rows:
        return None
    return sum((row['pnl'] for row in rows), Decimal('0'))


def _gap(left, right, left_reason, right_reason, stale_empty_reason=None):
    if stale_empty_reason is not None and right_reason == 'empty_bin':
        return None, stale_empty_reason
    if left is None or right is None:
        return None, left_reason or right_reason
    return left - right, None


def _stress_pnl(rows, settlement_values, mode):
    if not rows:
        return None
    total = Decimal('0')
    for row in rows:
        value = settlement_values[row['ticker']]
        if not isinstance(value, Decimal):
            value = Decimal(value)
        price = row['fill_price']
        if mode == 'fees_2x':
            fee = _fee(row['role'], format(price, 'f'), times=2)
            cost = price
        elif mode == 'one_tick_worse':
            worse = price + ONE_TICK
            fee_now = _fee(row['role'], format(price, 'f'), times=1)
            fee_worse = _fee(row['role'], format(worse, 'f'), times=1)
            fee = fee_now if fee_now >= fee_worse else fee_worse
            cost = worse
        else:
            raise OrchestratorError('stress')
        total += _settle(row['side'], value) - cost - fee
    return total


def _rate(filled, requested):
    if requested == 0:
        return None
    return Decimal(filled) / Decimal(requested)


def score(fill_document, settlement_values):
    """Co-primary arm metrics. Does not write a file and does not mutate fills."""
    if not isinstance(fill_document, dict) or not isinstance(settlement_values, dict):
        raise OrchestratorError('score')
    before = [
        (row.get('ticker'), row.get('captured_utc'), row.get('leg'), row.get('side'), row.get('filled'))
        for row in (fill_document.get('rows') or [])
    ]
    resolved, unresolved = _resolved(fill_document, settlement_values)
    maker = [row for row in resolved if row['leg'] == 'maker']
    taker = [row for row in resolved if row['leg'] == 'taker']
    fresh = [row for row in resolved if row['content_fresh_flag']]
    stale = [row for row in resolved if not row['content_fresh_flag']]
    maker_roi, maker_reason = _roi(maker)
    taker_roi, taker_reason = _roi(taker)
    fresh_roi, fresh_reason = _roi(fresh)
    stale_roi, stale_reason = _roi(stale)
    a0, a0_reason = _gap(maker_roi, taker_roi, maker_reason, taker_reason)
    a1, a1_reason = _gap(
        fresh_roi, stale_roi, fresh_reason, stale_reason, stale_empty_reason='STALE_BIN_EMPTY',
    )
    requested = 0
    filled = 0
    for row in fill_document.get('rows') or []:
        if row.get('requested'):
            requested += 1
        if row.get('filled'):
            filled += 1
    after = [
        (row.get('ticker'), row.get('captured_utc'), row.get('leg'), row.get('side'), row.get('filled'))
        for row in (fill_document.get('rows') or [])
    ]
    if after != before:
        raise OrchestratorError('fill set')
    pnl = _pnl(resolved)
    return {
        'pnl': pnl,
        'roi': None if pnl is None else _roi(resolved)[0],
        'Q6S5A0_maker_vs_taker_roi_delta': a0,
        'A0_null_reason': a0_reason,
        'Q6S5A1_fresh_vs_stale_gap': a1,
        'A1_null_reason': a1_reason,
        'fees_2x': {'pnl': _stress_pnl(resolved, settlement_values, 'fees_2x')},
        'one_tick_worse': {'pnl': _stress_pnl(resolved, settlement_values, 'one_tick_worse')},
        'unresolved_inventory': len(unresolved),
        'unresolved_tickers': sorted({row['ticker'] for row in unresolved}),
        'requested_contracts_simulated': requested,
        'filled_contracts_simulated': filled,
        'fill_rate_simulated': _rate(filled, requested),
        'counts_toward_keep': False,
        'promote': False,
        'formula_id': None,
        'fee': FEE_LABEL,
        'common_scorecard': {
            'net_pnl_without_rewards': None,
            'net_pnl_with_rewards': None,
            'rewards_actually_earned': None,
            'calibration': None,
            'fill_rate': None,
            'adverse_selection_after_fills': None,
            'feasible_vs_requested_size': None,
            'unresolved_inventory': None,
            'capital_hours': None,
            'drawdown': None,
            'event_concentration': None,
        },
        'verdict': None,
    }
