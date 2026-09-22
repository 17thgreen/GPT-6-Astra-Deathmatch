"""R1-P5 measurement rails.

Queue attribution, venue-rounded maker-credit admission, and a content-fresh
book predicate. The MICRO helper scores a caller-supplied print list as one
role. This module does not place live orders and does not select markets.
"""
import hashlib
import json
import sys
from dataclasses import dataclass
from decimal import Decimal, ROUND_FLOOR
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FEEBOOK_DIR = ROOT.parent / 'kalshi_feebook_lab_20260922'
if str(FEEBOOK_DIR) not in sys.path:
    sys.path.insert(0, str(FEEBOOK_DIR))

import feebook

QUEUE_AHEAD_DEFAULT = Decimal('3300')
FILL_PARTICIPATION_DEFAULT = Decimal('0.5')
STRESS_QUEUE_AHEAD = Decimal('10000')
QUEUE_MODELS = ('measured', 'front')
QUEUE_SCENARIO_LABELS = {
    'q3300': QUEUE_AHEAD_DEFAULT,
    'q10000': STRESS_QUEUE_AHEAD,
}
FEE_CREDIT_RULE_ID = 'astra.r1p5.rails.maker_credit_floor_cent.v1'
EVIDENCE_STAGE = 'HISTORICAL_OUT_OF_SAMPLE'
VERDICTS = ('SURVIVES', 'FAILS', 'THIN', 'CONTROL')
TAKER_FILLS_OUR = feebook.TAKER_FILLS_RESTING


class MakerCreditRefused(Exception):
    """Venue-rounded maker credit floored to one cent is not positive."""

    def __init__(self, evaluation):
        super().__init__('maker credit floors to zero')
        self.evaluation = evaluation


def scenario_queue(label):
    """Q1–Q6 queue magnitude used as an instrument setting."""
    try:
        return QUEUE_SCENARIO_LABELS[label]
    except KeyError as exc:
        raise ValueError('scenario label') from exc


def _price(value):
    price = feebook.as_decimal(value, 'price')
    if price < 0 or price > 1:
        raise ValueError('price must be in [0, 1]')
    return price


def _positive(value, name):
    number = feebook.as_decimal(value, name)
    if number <= 0:
        raise ValueError('%s must be positive' % name)
    return number


def _nonneg(value, name):
    number = feebook.as_decimal(value, name)
    if number < 0:
        raise ValueError('%s must be non-negative' % name)
    return number


@dataclass(frozen=True)
class QuoteIntent:
    ticker: str
    outcome: str
    price: Decimal
    size: Decimal
    kind: str = 'maker'


@dataclass
class RestingOrder:
    intent: QuoteIntent
    queue_ahead: Decimal
    filled: Decimal


@dataclass(frozen=True)
class MakerFill:
    ticker: str
    outcome: str
    price: Decimal
    size: Decimal
    fee: Decimal
    kind: str
    queue_ahead: Decimal
    at: object
    fee_quote: dict


def maker_quote_credit(price, contracts, series=None, table=None):
    """Net quote cash after the examiner maker ceiling, floored to one cent."""
    price = _price(price)
    contracts = _positive(contracts, 'contracts')
    quote = feebook.order_fee(
        'maker', contracts, price, round_up=True, series=series, table=table,
    )
    gross = price * contracts
    net = gross - quote['fee']
    credit = net.quantize(feebook.CENT, rounding=ROUND_FLOOR)
    return {
        'rule_id': FEE_CREDIT_RULE_ID,
        'price': price,
        'contracts': contracts,
        'gross': gross,
        'fee': quote['fee'],
        'fee_quote': quote,
        'net': net,
        'credit': credit,
        'fee_blind_credit': gross.quantize(feebook.CENT, rounding=ROUND_FLOOR),
        'admitted': credit > 0,
    }


def admit_maker_quote(price, contracts, series=None, table=None):
    """Refuse a quote whose floored maker credit is zero or negative."""
    evaluation = maker_quote_credit(price, contracts, series=series, table=table)
    if evaluation['credit'] <= 0:
        raise MakerCreditRefused(evaluation)
    return evaluation


class QueueInstrument:
    """Claude-shaped queue. Same price keeps consumed queue. A new order starts behind it.

    `front` is zero ahead. `measured` uses a supplied book size or the configured
    ahead value. 10000 is the stress ahead value, not a third model.
    """

    def __init__(self, queue_ahead_contracts=QUEUE_AHEAD_DEFAULT,
                 fill_participation=FILL_PARTICIPATION_DEFAULT,
                 queue_model='measured', series=None, table=None):
        if queue_model not in QUEUE_MODELS:
            raise ValueError('queue_model')
        participation = feebook.as_decimal(fill_participation, 'fill_participation')
        if participation <= 0 or participation > 1:
            raise ValueError('fill_participation')
        self.queue_ahead_contracts = _nonneg(queue_ahead_contracts, 'queue_ahead_contracts')
        self.fill_participation = participation
        self.queue_model = queue_model
        self.series = series
        self.table = table
        self._resting = {}

    def _checked_intent(self, raw):
        if not isinstance(raw, QuoteIntent):
            raise TypeError('intent')
        if not isinstance(raw.ticker, str) or raw.ticker == '':
            raise ValueError('ticker')
        if raw.outcome not in ('yes', 'no'):
            raise ValueError('outcome')
        if raw.kind not in ('maker', 'taker'):
            raise ValueError('kind')
        return QuoteIntent(
            raw.ticker,
            raw.outcome,
            _price(raw.price),
            _positive(raw.size, 'size'),
            raw.kind,
        )

    def _book_sizes(self, book_sizes):
        if book_sizes is None:
            return {}
        if not isinstance(book_sizes, dict):
            raise TypeError('book_sizes')
        clean = {}
        for key, value in book_sizes.items():
            if not isinstance(key, tuple) or len(key) != 2:
                raise ValueError('book_sizes key')
            ticker, outcome = key
            if not isinstance(ticker, str) or outcome not in ('yes', 'no'):
                raise ValueError('book_sizes key')
            clean[key] = _nonneg(value, 'book_size')
        return clean

    def _queue_for(self, key, book_sizes):
        if self.queue_model == 'front':
            return Decimal('0')
        if key in book_sizes:
            return book_sizes[key]
        return self.queue_ahead_contracts

    def replace_quotes(self, intents, book_sizes=None):
        """Replace the resting map. A refused quote leaves the previous map in place."""
        book_sizes = self._book_sizes(book_sizes)
        checked = [self._checked_intent(item) for item in intents]
        makers = [item for item in checked if item.kind == 'maker']
        seen = set()
        for item in makers:
            key = (item.ticker, item.outcome)
            if key in seen:
                raise ValueError('duplicate quote')
            seen.add(key)
        for item in makers:
            admit_maker_quote(item.price, item.size, series=self.series, table=self.table)
        new = {}
        for item in makers:
            key = (item.ticker, item.outcome)
            prev = self._resting.get(key)
            remaining = Decimal('0') if prev is None else prev.intent.size - prev.filled
            if prev is not None and prev.intent.price == item.price and remaining > 0:
                kept = QuoteIntent(item.ticker, item.outcome, item.price, remaining, 'maker')
                new[key] = RestingOrder(kept, prev.queue_ahead, Decimal('0'))
            else:
                new[key] = RestingOrder(item, self._queue_for(key, book_sizes), Decimal('0'))
        self._resting = new

    def on_trade(self, trade):
        """Apply one print. Taker YES can fill our NO. Taker NO can fill our YES."""
        if not isinstance(trade, dict):
            raise TypeError('trade')
        taker_side = trade.get('taker_side')
        if taker_side not in TAKER_FILLS_OUR:
            raise ValueError('taker_side')
        ticker = trade.get('ticker')
        if not isinstance(ticker, str) or ticker == '':
            raise ValueError('ticker')
        yes_price, no_price = self._trade_prices(trade)
        volume = _positive(trade.get('size'), 'size')
        our_outcome = TAKER_FILLS_OUR[taker_side]
        resting = self._resting.get((ticker, our_outcome))
        if resting is None:
            return []
        trade_price = no_price if our_outcome == 'no' else yes_price
        if trade_price > resting.intent.price:
            return []
        consumed = min(resting.queue_ahead, volume)
        resting.queue_ahead -= consumed
        post = volume - consumed
        remaining = resting.intent.size - resting.filled
        got = min(remaining, post * self.fill_participation)
        if got <= 0:
            return []
        resting.filled += got
        quote = feebook.order_fee(
            'maker', got, resting.intent.price, round_up=False,
            series=self.series, table=self.table,
        )
        return [MakerFill(
            ticker=ticker,
            outcome=our_outcome,
            price=resting.intent.price,
            size=got,
            fee=quote['fee'],
            kind='maker',
            queue_ahead=resting.queue_ahead,
            at=trade.get('created_time'),
            fee_quote=quote,
        )]

    def _trade_prices(self, trade):
        yes_price = _price(trade['yes_price']) if 'yes_price' in trade else None
        no_price = _price(trade['no_price']) if 'no_price' in trade else None
        if yes_price is None and no_price is None:
            raise ValueError('price')
        if yes_price is None:
            yes_price = feebook.ONE - no_price
        if no_price is None:
            no_price = feebook.ONE - yes_price
        if yes_price + no_price != feebook.ONE:
            raise ValueError('yes_price + no_price must be 1')
        return yes_price, no_price

    def resting(self):
        return [row.intent for row in self._resting.values()]

    def order(self, ticker, outcome):
        return self._resting.get((ticker, outcome))


@dataclass(frozen=True)
class BookObservation:
    content: str
    transaction_time: object


@dataclass(frozen=True)
class Freshness:
    fresh: bool
    reason: str


def canonical_book_content(payload):
    """SHA-256 of sorted-key JSON. A keepalive frame is not a payload."""
    if isinstance(payload, (str, bytes, bytearray)):
        raise TypeError('content')
    encoded = json.dumps(payload, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
    return hashlib.sha256(encoded.encode('utf-8')).hexdigest()


def judge_freshness(previous, current, *, keepalive=False):
    """Content or transaction-time change. A keepalive is never a fresh book."""
    if keepalive:
        return Freshness(False, 'keepalive_ignored')
    if not isinstance(current, BookObservation):
        raise TypeError('current')
    if previous is None:
        return Freshness(True, 'initial')
    if not isinstance(previous, BookObservation):
        raise TypeError('previous')
    if current.content != previous.content:
        return Freshness(True, 'content_changed')
    if current.transaction_time != previous.transaction_time:
        return Freshness(True, 'transaction_time_changed')
    return Freshness(False, 'unchanged')


def load_micro_config(path=None):
    if path is None:
        path = ROOT / 'grok_config_MICRO_V1.json'
    return json.loads(Path(path).read_text())


def _roi(value, name):
    if value is None:
        return None
    return feebook.as_decimal(value, name)


def micro_verdict(kind, n, roi, counterpart_roi, config=None):
    """CONTROL, then THIN, then FAILS, then SURVIVES. Control never survives."""
    if kind not in ('control', 'challenger'):
        raise ValueError('kind')
    if isinstance(n, bool) or not isinstance(n, int) or n < 0:
        raise ValueError('n')
    if config is None:
        config = load_micro_config()
    if kind == 'control':
        return 'CONTROL'
    if n < config['thinN']:
        return 'THIN'
    roi = _roi(roi, 'roi')
    if roi is None:
        return 'FAILS'
    survive = feebook.as_decimal(config['surviveRoi'], 'surviveRoi')
    counterpart = _roi(counterpart_roi, 'counterpart_roi')
    beats = counterpart is None or roi > counterpart
    if roi > survive and beats:
        return 'SURVIVES'
    return 'FAILS'


def role_pnl(taker_side, yes_price, result, role):
    """One-lot role cash. Taker fee is ceiled. Maker fee is the unrounded comparator."""
    if taker_side not in ('yes', 'no'):
        raise ValueError('taker_side')
    if result not in ('yes', 'no'):
        raise ValueError('result')
    if role not in ('maker', 'taker'):
        raise ValueError('role')
    yes_price = _price(yes_price)
    price = yes_price if taker_side == 'yes' else feebook.ONE - yes_price
    taker_wins = taker_side == result
    if role == 'taker':
        fee = feebook.order_fee('taker', '1', price)['fee']
        gross = (feebook.ONE - price) if taker_wins else -price
        win = taker_wins
    else:
        fee = feebook.grok_unrounded_maker_per_unit(price)['fee']
        gross = (price - feebook.ONE) if taker_wins else price
        win = not taker_wins
    return {
        'price': price,
        'fee': fee,
        'gross': gross,
        'profit': gross - fee,
        'win': win,
        'role': role,
    }


def score_role(prints, role, kind, evidence_stage=EVIDENCE_STAGE, config=None):
    """Score each kept print once, as the named role.

    One-lot ROI counts one contract per print. Size-weighted ROI weights that
    same per-contract profit by print size. Picker fields on the config are
    not applied. Block prints are omitted when skipBlockTrades is set.
    """
    if evidence_stage != EVIDENCE_STAGE:
        raise ValueError('evidence stage')
    if role not in ('maker', 'taker'):
        raise ValueError('role')
    if config is None:
        config = load_micro_config()
    if config.get('skipBlockTrades') is not True:
        raise ValueError('skipBlockTrades')
    other = 'taker' if role == 'maker' else 'maker'
    profits = []
    counterpart = []
    weighted = []
    sizes = []
    wins = 0
    markets = set()
    for row in prints:
        if not isinstance(row, dict):
            raise TypeError('print')
        if row.get('is_block') is True:
            continue
        pnl = role_pnl(row['taker_side'], row['yes_price'], row['result'], role)
        other_pnl = role_pnl(row['taker_side'], row['yes_price'], row['result'], other)
        size = _positive(row['size'], 'size')
        ticker = row.get('ticker')
        if not isinstance(ticker, str) or ticker == '':
            raise ValueError('ticker')
        profits.append(pnl['profit'])
        counterpart.append(other_pnl['profit'])
        weighted.append(pnl['profit'] * size)
        sizes.append(size)
        markets.add(ticker)
        if pnl['win']:
            wins += 1
    n = len(profits)
    net = sum(profits, Decimal('0'))
    size_net = sum(weighted, Decimal('0'))
    one_lot_roi = None if n == 0 else net / Decimal(n)
    size_weighted_roi = None if n == 0 else size_net / sum(sizes, Decimal('0'))
    counterpart_net = sum(counterpart, Decimal('0'))
    counterpart_roi = None if n == 0 else counterpart_net / Decimal(n)
    return {
        'role': role,
        'kind': kind,
        'n': n,
        'wins': wins,
        'losses': n - wins,
        'markets': len(markets),
        'one_lot_net': net,
        'one_lot_roi': one_lot_roi,
        'size_weighted_net': size_net,
        'size_weighted_roi': size_weighted_roi,
        'counterpart_roi': counterpart_roi,
        'verdict': micro_verdict(kind, n, one_lot_roi, counterpart_roi, config=config),
        'evidence_stage': EVIDENCE_STAGE,
        'unique_counterparty': True,
        'picker_fields_applied': False,
    }
