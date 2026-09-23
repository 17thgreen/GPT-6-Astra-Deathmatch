"""R3-P1 fee honesty: venue fee_cost versus the R1-P1 closed-form model.

fee_model is kalshi_feebook_lab_20260922.order_fee with the examiner cent
ceiling. When a fill reports fee_cost, that venue amount is the accounting
fee. The model remains a comparator. This module does not place live orders
and does not invent a completed net.
"""
import hashlib
import json
import sys
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PARENT = ROOT.parent
FEEBOOK_DIR = PARENT / 'kalshi_feebook_lab_20260922'
if str(FEEBOOK_DIR) not in sys.path:
    sys.path.insert(0, str(FEEBOOK_DIR))

import feebook

PACKET_ID = 'R3-P1-FEE-COST-VS-MODEL'
EXPERIMENT_ID = 'r3_p1_fee_cost_vs_model_20260922'
FEEBOOK_COMMIT = '22371178cb2663250b4762f328069571c48cb551'
FEEBOOK_DIRECTORY = 'kalshi_feebook_lab_20260922'
OUTPUT_KEYS = ('fee_model_minus_venue_delta', 'results', 'pnl')
FILLS_FIXTURE = ROOT / 'fixtures' / 'synthetic_fills.json'
FROZEN_EXPERIMENT = ROOT / 'FROZEN_EXPERIMENT.json'
EMPTY_RESULTS = ROOT / 'results' / 'EMPTY_RESULTS.json'
EMPTY_STATUS = 'EMPTY'
SYNTHETIC_FIXTURE_ONLY = 'SYNTHETIC_FIXTURE_ONLY'


class FeeCostError(Exception):
    """A fill row or a fee-honesty claim was rejected."""


class CompletedNetRefused(FeeCostError):
    """A completed net was requested from a model-only fee."""


class LiveOrdersForbidden(FeeCostError):
    """This lab has no live order path."""

    def __init__(self):
        super().__init__('no live orders and no account endpoint')


def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def instrument_binding():
    """Pins for the imported examiner. Rates are read from the feebook stub."""
    table = feebook.load_series_table()
    rates = table['rates']
    return {
        'packet_id': PACKET_ID,
        'experiment_id': EXPERIMENT_ID,
        'feebook_directory': FEEBOOK_DIRECTORY,
        'feebook_commit': FEEBOOK_COMMIT,
        'feebook_imported': True,
        'feebook_copied': False,
        'examiner_formula_id': feebook.EXAMINER_FORMULA_ID,
        'comparator_formula_id': feebook.GROK_COMPARATOR_FORMULA_ID,
        'fee_model': 'round_up(M*rate*C*P*(1-P))',
        'maker_rate': feebook.as_decimal(rates['maker'], 'maker'),
        'taker_rate': feebook.as_decimal(rates['taker'], 'taker'),
        'symbols': ('order_fee', 'examiner_fee_channel', 'classify_scorecard'),
        'live_orders': False,
        'authenticated_account_calls': False,
        'signal_retune': False,
        'q6_000_retune': False,
    }


def execution_adapter():
    """No live order client lives in this lab."""
    raise LiveOrdersForbidden()


def _require_mapping(row):
    if not isinstance(row, dict):
        raise TypeError('fill')
    return row


def _is_taker(row):
    if 'is_taker' not in row:
        raise FeeCostError('is_taker')
    value = row['is_taker']
    if not isinstance(value, bool):
        raise TypeError('is_taker')
    return value


def _contracts_from_fill(row):
    has_fp = 'count_fp' in row and row['count_fp'] is not None
    has_count = 'count' in row and row['count'] is not None
    if not has_fp and not has_count:
        raise FeeCostError('contracts')
    fp = feebook.as_decimal(row['count_fp'], 'count_fp') if has_fp else None
    count = feebook.as_decimal(row['count'], 'count') if has_count else None
    if fp is not None and count is not None and fp != count:
        raise FeeCostError('count_fp and count disagree')
    return fp if fp is not None else count


def _price_from_fill(row):
    side = row.get('side')
    if side not in ('yes', 'no'):
        raise ValueError('side')
    if 'yes_price_dollars' not in row and 'no_price_dollars' not in row:
        raise FeeCostError('price')
    yes = row.get('yes_price_dollars')
    no = row.get('no_price_dollars')
    yes_price = None if yes is None else feebook.as_decimal(yes, 'yes_price_dollars')
    no_price = None if no is None else feebook.as_decimal(no, 'no_price_dollars')
    if yes_price is not None and no_price is not None and yes_price + no_price != feebook.ONE:
        raise FeeCostError('yes and no prices must sum to 1')
    if side == 'yes':
        if yes_price is None:
            raise FeeCostError('yes_price_dollars')
        return yes_price
    if no_price is None:
        raise FeeCostError('no_price_dollars')
    return no_price


def _fee_cost_from_fill(row):
    if 'fee_cost' not in row:
        raise FeeCostError('fee_cost field missing')
    value = row['fee_cost']
    if value is None:
        return None
    fee = feebook.as_decimal(value, 'fee_cost')
    if fee < 0:
        raise ValueError('fee_cost')
    return fee


def _series_from_fill(row):
    if 'series' not in row or row['series'] is None:
        return None
    series = row['series']
    if not isinstance(series, str) or series.strip() == '':
        raise TypeError('series')
    return series


def join_fill(row, table=None):
    """Join one synthetic Fill to the examiner fee model.

    Returns fee_model, fee_cost, fee_model_minus_venue_delta, and is_taker.
    results and pnl stay null. A null fee_cost does not become a zero delta.
    """
    row = _require_mapping(row)
    if table is None:
        table = feebook.load_series_table()
    is_taker = _is_taker(row)
    role = 'taker' if is_taker else 'maker'
    contracts = _contracts_from_fill(row)
    price = _price_from_fill(row)
    series = _series_from_fill(row)
    quote = feebook.order_fee(
        role, contracts, price, round_up=True, series=series, table=table,
    )
    if quote['formula_id'] != feebook.EXAMINER_FORMULA_ID:
        raise FeeCostError('examiner formula')
    if quote['rounded_up'] is not True:
        raise FeeCostError('fee_model uses the order-level ceiling')
    fee_model = quote['fee']
    fee_cost = _fee_cost_from_fill(row)
    if fee_cost is None:
        delta = None
        preferred_fee_source = 'model_only'
        preferred_fee = fee_model
    else:
        delta = fee_model - fee_cost
        preferred_fee_source = 'venue'
        preferred_fee = fee_cost
    return {
        'case_id': row.get('case_id'),
        'fill_id': row.get('fill_id'),
        'is_taker': is_taker,
        'role': role,
        'side': row['side'],
        'contracts': quote['contracts'],
        'price': quote['price'],
        'series': series,
        'formula_id': quote['formula_id'],
        'M': quote['M'],
        'rate': quote['rate'],
        'raw': quote['raw'],
        'fee_model': fee_model,
        'fee_cost': fee_cost,
        'fee_model_minus_venue_delta': delta,
        'preferred_fee_source': preferred_fee_source,
        'preferred_fee': preferred_fee,
        'projection_only': fee_cost is None,
        'quote': quote,
        'results': None,
        'pnl': None,
    }


def load_fills(path=None):
    if path is None:
        path = FILLS_FIXTURE
    payload = json.loads(Path(path).read_text())
    if not isinstance(payload, dict) or not isinstance(payload.get('fills'), list):
        raise FeeCostError('fills')
    return payload


def score_fixture(path=None, table=None):
    """Score synthetic rows. The delta total is not profit and is not frozen."""
    payload = load_fills(path)
    joined = [join_fill(row, table=table) for row in payload['fills']]
    deltas = [
        row['fee_model_minus_venue_delta']
        for row in joined
        if row['fee_model_minus_venue_delta'] is not None
    ]
    total = None if not deltas else sum(deltas, Decimal('0'))
    model_only = sum(1 for row in joined if row['fee_cost'] is None)
    return {
        'packet_id': payload.get('packet_id', PACKET_ID),
        'rows': joined,
        'fee_model_minus_venue_delta': total,
        'rows_with_venue_fee': len(deltas),
        'rows_model_only': model_only,
        'results': None,
        'pnl': None,
        'status': SYNTHETIC_FIXTURE_ONLY,
    }


def other_role_quote(joined, table=None):
    """Examiner quote for the other role at the same count and price.

    The counterpart fills the examiner channel. It is not a venue fee.
    """
    role = 'maker' if joined['is_taker'] else 'taker'
    if table is None:
        table = feebook.load_series_table()
    quote = feebook.order_fee(
        role,
        joined['contracts'],
        joined['price'],
        round_up=True,
        series=joined.get('series'),
        table=table,
    )
    if quote['formula_id'] != feebook.EXAMINER_FORMULA_ID:
        raise FeeCostError('examiner formula')
    return quote


def examiner_channel(joined, other_role):
    """Examiner channel for one fill plus the other role's model quote."""
    if not isinstance(other_role, dict):
        raise TypeError('other_role_quote')
    expected = 'maker' if joined['is_taker'] else 'taker'
    if other_role.get('role') != expected:
        raise ValueError('other role')
    if joined['is_taker']:
        return feebook.examiner_fee_channel(joined['quote'], other_role)
    return feebook.examiner_fee_channel(other_role, joined['quote'])


def claim_completed_net(joined, *, fee_basis, other_role_quote, kind='execution', inventory_flat=True):
    """Refuse a model-only completed net when fee_cost was available.

    classify_scorecard is consulted and is not sufficient. Extrapolation stays
    a projection. A venue basis binds the accounting fee to fee_cost and still
    returns null results and pnl.
    """
    if fee_basis not in ('model', 'venue'):
        raise ValueError('fee_basis')
    if kind not in ('execution', 'extrapolation'):
        raise ValueError('kind')
    if not isinstance(inventory_flat, bool):
        raise TypeError('inventory_flat')
    channel = examiner_channel(joined, other_role_quote)
    model_label = feebook.classify_scorecard({
        'kind': kind,
        'inventory_flat': inventory_flat,
        'fee_channel': {
            'formula_id': channel['formula_id'],
            'taker_fee': channel['taker_fee'],
            'maker_fee': channel['maker_fee'],
        },
    })
    if model_label == 'projection':
        return {
            'label': 'projection',
            'model_label': model_label,
            'fee_basis': fee_basis,
            'preferred_fee_source': joined['preferred_fee_source'],
            'preferred_fee': joined['preferred_fee'],
            'projection_fee': joined['fee_model'],
            'fee_model_minus_venue_delta': joined['fee_model_minus_venue_delta'],
            'results': None,
            'pnl': None,
        }
    if model_label != 'completed_profit':
        raise FeeCostError('unexpected model label')
    if joined['fee_cost'] is None:
        raise CompletedNetRefused(
            'model-only fee supports projection, not completed-net'
        )
    if fee_basis == 'model':
        raise CompletedNetRefused(
            'model-only completed-net refused while fee_cost was available'
        )
    return {
        'label': 'venue_fee_bound',
        'model_label': model_label,
        'fee_basis': 'venue',
        'accounting_fee': joined['fee_cost'],
        'fee_model': joined['fee_model'],
        'fee_model_minus_venue_delta': joined['fee_model_minus_venue_delta'],
        'results': None,
        'pnl': None,
    }


def empty_outputs():
    """The freeze contract before any unit observation is recorded."""
    return {
        'fee_model_minus_venue_delta': None,
        'results': None,
        'pnl': None,
        'status': EMPTY_STATUS,
    }


def frozen_output_snapshot():
    """Read the freeze file. Does not modify it."""
    payload = json.loads(FROZEN_EXPERIMENT.read_text())
    return {key: payload[key] for key in OUTPUT_KEYS}
