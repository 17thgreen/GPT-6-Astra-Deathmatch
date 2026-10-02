"""R1-P1 reciprocal book and order-level fee algebra.

Examiner fees use Decimal cent ceiling. The Grok unrounded maker quote is a
comparator and is not an examiner completed-profit channel. No live orders.
"""
import json
from decimal import Decimal, ROUND_CEILING
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EXAMINER_FORMULA_ID = 'astra.r1p1.feebook.claude_order_level_ceil.v1'
GROK_COMPARATOR_FORMULA_ID = 'grok.fees_ts.unrounded_per_unit.v1'
ONE = Decimal('1')
CENT = Decimal('0.01')
CENTICENT = Decimal('0.0001')
EPS = Decimal('1e-9')
TAKER_FILLS_RESTING = {'yes': 'no', 'no': 'yes'}


class CompletedProfitRefused(Exception):
    """Completed profit was requested without the examiner fee pin."""


class BookIncomplete(Exception):
    """A required bid is missing, so the implied ask is not invented."""


def as_decimal(value, name):
    if isinstance(value, bool) or isinstance(value, float):
        raise TypeError('%s must be Decimal, int, or str' % name)
    if isinstance(value, Decimal):
        return value
    if isinstance(value, int) or isinstance(value, str):
        return Decimal(value)
    raise TypeError(name)


def load_json(name):
    return json.loads((ROOT / name).read_text())


def load_series_table(path=None):
    if path is None:
        path = ROOT / 'series_fee_table.stub.json'
    return json.loads(Path(path).read_text())


def round_up_to_cent(raw):
    """Examiner ceiling: quantize to one cent, away from zero on any remainder."""
    raw = as_decimal(raw, 'raw')
    if raw < 0:
        raise ValueError('fee raw must be non-negative')
    return raw.quantize(CENT, rounding=ROUND_CEILING)


def round_up_to_cent_eps(raw, eps=EPS):
    """Packet float description, evaluated in Decimal: ceil(raw*100 - eps)/100."""
    raw = as_decimal(raw, 'raw')
    if raw < 0:
        raise ValueError('fee raw must be non-negative')
    scaled = raw * 100 - as_decimal(eps, 'eps')
    ceiled = scaled.to_integral_value(rounding=ROUND_CEILING)
    return (ceiled / 100).quantize(CENT)


def round_up_to_centicent(raw):
    """Not the examiner path. Documents the rejected centicent reading."""
    raw = as_decimal(raw, 'raw')
    if raw < 0:
        raise ValueError('fee raw must be non-negative')
    return raw.quantize(CENTICENT, rounding=ROUND_CEILING)


def _flag(merged, key):
    value = merged[key]
    if not isinstance(value, bool):
        raise TypeError('%s must be bool' % key)
    return value


def resolve_terms(table, series, role):
    if role not in ('taker', 'maker'):
        raise ValueError('role')
    default = table['default']
    rates = table['rates']
    overrides = table.get('overrides') or {}
    if series is None:
        merged = dict(default)
        resolution = 'default'
    elif series in overrides:
        merged = dict(default)
        merged.update(overrides[series])
        resolution = 'override'
    else:
        merged = dict(default)
        resolution = 'default_unknown_series'
    rate_key = role + '_rate'
    rate = as_decimal(merged.get(rate_key, rates[role]), rate_key)
    maker_on = _flag(merged, 'maker_fees_enabled')
    specific = role + '_M'
    if role == 'maker' and not maker_on:
        multiplier = Decimal('0')
    elif specific in merged:
        multiplier = as_decimal(merged[specific], specific)
    else:
        multiplier = as_decimal(merged['M'], 'M')
    cap_enabled = _flag(merged, 'per_contract_cap_enabled')
    cap_per = as_decimal(merged.get('per_contract_cap', '0.035'), 'per_contract_cap')
    return {
        'resolution': resolution,
        'multiplier': multiplier,
        'rate': rate,
        'cap_enabled': cap_enabled,
        'cap_per_contract': cap_per,
        'maker_fees_enabled': maker_on,
    }


def _price(price):
    price = as_decimal(price, 'price')
    if price < 0 or price > 1:
        raise ValueError('price must be in [0, 1]')
    return price


def _contracts(contracts):
    contracts = as_decimal(contracts, 'contracts')
    if contracts <= 0:
        raise ValueError('contracts must be positive')
    return contracts


def order_fee(role, contracts, price, round_up=True, series=None, table=None):
    """Claude-shaped order fee. Partials pass round_up=False.

    The optional per-contract cap is applied only on the rounded order path,
    after the cent ceiling.
    """
    if table is None:
        table = load_series_table()
    if not isinstance(round_up, bool):
        raise TypeError('round_up must be bool')
    terms = resolve_terms(table, series, role)
    contracts = _contracts(contracts)
    price = _price(price)
    raw = terms['multiplier'] * terms['rate'] * contracts * price * (ONE - price)
    cap_applied = False
    if round_up:
        fee = round_up_to_cent(raw)
        if terms['cap_enabled']:
            cap = terms['cap_per_contract'] * contracts
            if fee > cap:
                fee = cap
                cap_applied = True
    else:
        fee = raw
    return {
        'role': role,
        'formula_id': EXAMINER_FORMULA_ID,
        'raw': raw,
        'fee': fee,
        'rounded_up': round_up,
        'cap_applied': cap_applied,
        'series_resolution': terms['resolution'],
        'M': terms['multiplier'],
        'rate': terms['rate'],
        'contracts': contracts,
        'price': price,
    }


def grok_unrounded_maker_per_unit(price, series=None, table=None):
    """Grok paper comparator: maker fee per unit, unrounded, no cap, no C.

    Not an examiner quote. Completed-profit classification rejects this id.
    """
    if table is None:
        table = load_series_table()
    terms = resolve_terms(table, series, 'maker')
    price = _price(price)
    raw = terms['multiplier'] * terms['rate'] * price * (ONE - price)
    return {
        'role': 'maker',
        'formula_id': GROK_COMPARATOR_FORMULA_ID,
        'raw': raw,
        'fee': raw,
        'rounded_up': False,
        'cap_applied': False,
        'series_resolution': terms['resolution'],
        'M': terms['multiplier'],
        'rate': terms['rate'],
        'contracts': None,
        'price': price,
    }


def _levels(orderbook, side):
    if 'orderbook_fp' in orderbook:
        orderbook = orderbook['orderbook_fp']
    key = side + '_dollars'
    levels = orderbook.get(key) or []
    parsed = []
    for row in levels:
        if len(row) != 2:
            raise ValueError('level')
        price = _price(row[0])
        size = as_decimal(row[1], 'size')
        if size < 0:
            raise ValueError('size')
        parsed.append((price, size))
    return parsed


def _best(levels):
    positive = [row for row in levels if row[1] > 0]
    if not positive:
        return None, None
    best_price = max(price for price, _size in positive)
    touch = sum((size for price, size in positive if price == best_price), Decimal('0'))
    return best_price, touch


def reciprocal_book(orderbook):
    """Asks and spreads from a bids-only dollar book. Missing bids stay unset."""
    yes_bid, yes_size = _best(_levels(orderbook, 'yes'))
    no_bid, no_size = _best(_levels(orderbook, 'no'))
    ask_yes = None if no_bid is None else ONE - no_bid
    ask_no = None if yes_bid is None else ONE - yes_bid
    if yes_bid is None or no_bid is None:
        spread_yes = None
        spread_no = None
    else:
        spread_yes = ask_yes - yes_bid
        spread_no = ask_no - no_bid
    return {
        'bid_yes': yes_bid,
        'bid_no': no_bid,
        'ask_yes': ask_yes,
        'ask_no': ask_no,
        'spread_yes': spread_yes,
        'spread_no': spread_no,
        'touch_yes_size': yes_size,
        'touch_no_size': no_size,
    }


def polarity_fill(orderbook, taker_side, contracts, round_up=True, series=None, table=None):
    """Fee both sides of one touch trade. Taker YES lifts NO, and the reverse."""
    if taker_side not in TAKER_FILLS_RESTING:
        raise ValueError('taker_side')
    book = reciprocal_book(orderbook)
    resting = TAKER_FILLS_RESTING[taker_side]
    taker_price = book['ask_' + taker_side]
    maker_price = book['bid_' + resting]
    touch = book['touch_' + resting + '_size']
    if taker_price is None or maker_price is None or touch is None:
        raise BookIncomplete('missing %s bid' % resting)
    contracts = _contracts(contracts)
    taker_fee = order_fee('taker', contracts, taker_price, round_up=round_up,
                          series=series, table=table)
    maker_fee = order_fee('maker', contracts, maker_price, round_up=round_up,
                          series=series, table=table)
    return {
        'taker_side': taker_side,
        'resting_side': resting,
        'taker_price': taker_price,
        'maker_price': maker_price,
        'touch_size': touch,
        'contracts': contracts,
        'size_exceeds_touch': contracts > touch,
        'taker_fee': taker_fee,
        'maker_fee': maker_fee,
        'book': book,
    }


def examiner_fee_channel(taker_quote, maker_quote):
    """Build the only fee channel that can support completed_profit."""
    if taker_quote.get('formula_id') != EXAMINER_FORMULA_ID:
        raise CompletedProfitRefused('taker quote is not the examiner formula')
    if maker_quote.get('formula_id') != EXAMINER_FORMULA_ID:
        raise CompletedProfitRefused('maker quote is not the examiner formula')
    if taker_quote.get('role') != 'taker' or maker_quote.get('role') != 'maker':
        raise ValueError('roles')
    return {
        'formula_id': EXAMINER_FORMULA_ID,
        'taker_fee': format(taker_quote['fee'], 'f'),
        'maker_fee': format(maker_quote['fee'], 'f'),
        'rounding': 'order_level_ceil_cent',
    }


def _fee_present(value):
    if value is None or isinstance(value, bool) or isinstance(value, float):
        raise CompletedProfitRefused('taker_fee and maker_fee must be non-null Decimal or str')
    if not isinstance(value, (Decimal, int, str)):
        raise CompletedProfitRefused('taker_fee and maker_fee must be non-null Decimal or str')
    if isinstance(value, str) and value.strip() == '':
        raise CompletedProfitRefused('taker_fee and maker_fee must be non-null Decimal or str')
    return as_decimal(value, 'fee')


def classify_scorecard(scorecard):
    """Return completed_profit only with the examiner fee pin.

    Extrapolations stay projections. Missing or non-examiner fees raise.
    """
    if not isinstance(scorecard, dict):
        raise TypeError('scorecard')
    if scorecard.get('kind') == 'extrapolation':
        return 'projection'
    if scorecard.get('inventory_flat') is False:
        raise CompletedProfitRefused('unresolved inventory is not completed profit')
    channel = scorecard.get('fee_channel')
    if not isinstance(channel, dict):
        raise CompletedProfitRefused('fee channel missing')
    _fee_present(channel.get('taker_fee'))
    _fee_present(channel.get('maker_fee'))
    if channel.get('formula_id') != EXAMINER_FORMULA_ID:
        raise CompletedProfitRefused('formula_id is not the examiner pin')
    return 'completed_profit'
