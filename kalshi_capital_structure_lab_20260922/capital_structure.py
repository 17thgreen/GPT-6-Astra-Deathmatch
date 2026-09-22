"""Capital-structure measurement for one shared 5000 USD account.

Arms A1, A2, and A3 differ in how that account partitions cash. Examiner fees
come from kalshi_feebook_lab_20260922. Queue labels and maker-credit admission
come from kalshi_rails_lab_20260922. This module does not place live orders
and does not record a walk P&L.
"""
import hashlib
import json
import sys
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PARENT = ROOT.parent
FEEBOOK_DIR = PARENT / 'kalshi_feebook_lab_20260922'
RAILS_DIR = PARENT / 'kalshi_rails_lab_20260922'
for _path in (FEEBOOK_DIR, RAILS_DIR):
    if str(_path) not in sys.path:
        sys.path.insert(0, str(_path))

import feebook
import rails

C_TOTAL = Decimal('5000')
N_EVENTS = 31
SLICE = C_TOTAL // Decimal(N_EVENTS)
RESIDUAL = C_TOTAL - SLICE * Decimal(N_EVENTS)
A1 = 'A1_shared_pool'
A2 = 'A2_shared_soft_reserve'
A3 = 'A3_hard_equal_slices'
ARMS = (A1, A2, A3)
SOFT_POLICY = 'borrow_unused_event_id_FIFO'
RESIDUAL_POLICY = 'non_trading_residual_bucket'
PROMOTION_SCOREBOARD = 'shared_account_only'
FORBIDDEN_COMPARISON = 'sum_of_N_independent_wallets_vs_one_5k'
STRATEGY_POINTER = 'Q6-000'
PRIMARY_STRESS = 'q3300_d0.25'
HARSH_TWIN_STRESS = 'q10000_d0.25'
PAIRCHECK_VARIED = False
SIGNAL_RETUNE = False
LIVE_ORDERS = False

FACTORIAL_INPUTS = PARENT / 'nfl_factorial_lab_20260921' / 'inputs'
WEEK_MEMBERSHIP = FACTORIAL_INPUTS / 'week_membership.json'
TAPE_MANIFEST = FACTORIAL_INPUTS / 'manifest.json'
SHADOW_FREEZE = PARENT / 'nfl_factorial_lab_20260921' / 'SHADOW_CANDIDATE_FREEZE.json'


class CapitalError(Exception):
    """Capital partition refused or the account books diverged."""


class InsufficientCapital(CapitalError):
    """The request would take more cash than the shared pool has."""

    def __init__(self, shortfall):
        super().__init__('pool cash would be exceeded')
        self.shortfall = shortfall


class CrossEventBorrowForbidden(CapitalError):
    """A3 hard slices cannot spend another event's cash."""

    def __init__(self, event_id, shortfall):
        super().__init__('A3 hard slices do not borrow')
        self.event_id = event_id
        self.shortfall = shortfall


class ResidualNotTradable(CapitalError):
    """The A3 residual bucket cannot fund an order."""

    def __init__(self):
        super().__init__('non_trading_residual_bucket cannot fund orders')


class UnknownEvent(CapitalError):
    """The event id is outside the 31-event cohort."""


class DuplicateOrder(CapitalError):
    """An order id is already on the account."""


class UnknownOrder(CapitalError):
    """The order id is not an open fund on this account."""


class IndependentWalletSumForbidden(CapitalError):
    """Promotion cannot compare N independent wallets with one shared account."""

    def __init__(self):
        super().__init__(FORBIDDEN_COMPARISON)
        self.code = FORBIDDEN_COMPARISON


class LiveOrdersForbidden(CapitalError):
    """This lab has no live order path."""

    def __init__(self):
        super().__init__('no live orders and no KalshiExecutionAdapter')


def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def development_cohort_event_ids():
    """Sorted event ids from the Q6 development membership file. Read only."""
    payload = json.loads(WEEK_MEMBERSHIP.read_text())
    if not isinstance(payload, dict):
        raise CapitalError('week membership')
    event_ids = tuple(sorted(payload.keys()))
    if len(event_ids) != N_EVENTS:
        raise CapitalError('N_events')
    return event_ids


def _money(value, name):
    amount = feebook.as_decimal(value, name)
    if amount <= 0:
        raise ValueError('%s must be positive' % name)
    return amount


def _event_ids(event_ids):
    if event_ids is None:
        return development_cohort_event_ids()
    if isinstance(event_ids, (str, bytes)) or not isinstance(event_ids, (list, tuple)):
        raise TypeError('event_ids')
    cleaned = []
    seen = set()
    for raw in event_ids:
        if not isinstance(raw, str) or raw == '':
            raise ValueError('event_id')
        if raw in seen:
            raise ValueError('duplicate event_id')
        seen.add(raw)
        cleaned.append(raw)
    ordered = tuple(sorted(cleaned))
    if len(ordered) != N_EVENTS:
        raise CapitalError('N_events')
    return ordered


def instrument_binding():
    """Fee rates and queue magnitudes from the merged labs, not from Q6 config."""
    rates = feebook.load_series_table()['rates']
    return {
        'fee_lab': 'kalshi_feebook_lab_20260922',
        'rails_lab': 'kalshi_rails_lab_20260922',
        'examiner_formula_id': feebook.EXAMINER_FORMULA_ID,
        'fee_credit_rule_id': rails.FEE_CREDIT_RULE_ID,
        'taker_rate': feebook.as_decimal(rates['taker'], 'taker'),
        'maker_rate': feebook.as_decimal(rates['maker'], 'maker'),
        'primary_stress': PRIMARY_STRESS,
        'primary_queue_ahead': rails.scenario_queue('q3300'),
        'harsh_twin_stress': HARSH_TWIN_STRESS,
        'harsh_twin_queue_ahead': rails.scenario_queue('q10000'),
        'harsh_twin_is_capital_knob': False,
        'strategy_pointer': STRATEGY_POINTER,
        'paircheck_varied': PAIRCHECK_VARIED,
        'signal_retune': SIGNAL_RETUNE,
        'live_orders': LIVE_ORDERS,
    }


def quote_lock(role, contracts, price, series=None):
    """Cash a quote locks. Maker admission is the rails credit. Fees are feebook."""
    if role == 'maker':
        evaluation = rails.admit_maker_quote(price, contracts, series=series)
        formula_id = evaluation['fee_quote']['formula_id']
        if formula_id != feebook.EXAMINER_FORMULA_ID:
            raise CapitalError('maker fee is not the examiner formula')
        if evaluation['rule_id'] != rails.FEE_CREDIT_RULE_ID:
            raise CapitalError('maker admission is not the rails credit rule')
        return {
            'role': 'maker',
            'lock': evaluation['gross'],
            'fee': evaluation['fee'],
            'gross': evaluation['gross'],
            'formula_id': formula_id,
            'rule_id': evaluation['rule_id'],
        }
    if role == 'taker':
        quote = feebook.order_fee(
            'taker', contracts, price, round_up=True, series=series,
        )
        if quote['formula_id'] != feebook.EXAMINER_FORMULA_ID:
            raise CapitalError('taker fee is not the examiner formula')
        gross = quote['price'] * quote['contracts']
        return {
            'role': 'taker',
            'lock': gross + quote['fee'],
            'fee': quote['fee'],
            'gross': gross,
            'formula_id': quote['formula_id'],
            'rule_id': None,
        }
    raise ValueError('role')


def execution_adapter():
    """There is no live adapter in this lab."""
    raise LiveOrdersForbidden()


def compare_independent_wallets_to_shared_account(*_args, **_kwargs):
    """Refuse the forbidden comparison. This function does not add wallets."""
    raise IndependentWalletSumForbidden()


class FundedOrder:
    def __init__(self, order_id, event_id, amount, own, borrows, unreserved, quote):
        self.order_id = order_id
        self.event_id = event_id
        self.amount = amount
        self.own = own
        self.borrows = borrows
        self.unreserved = unreserved
        self.quote = quote
        self.released = False

    @property
    def lock(self):
        return self.amount

    @property
    def fee(self):
        if self.quote is None:
            return None
        return self.quote['fee']

    @property
    def formula_id(self):
        if self.quote is None:
            return None
        return self.quote['formula_id']


class CapitalAccount:
    """One shared account. A1, A2, and A3 are partition rules on the same total."""

    def __init__(self, arm, event_ids=None):
        if arm not in ARMS:
            raise ValueError('arm')
        self.arm = arm
        self.event_ids = _event_ids(event_ids)
        self._index = {event_id: position for position, event_id in enumerate(self.event_ids)}
        self.c_total = C_TOTAL
        self.slice = SLICE
        self.soft_policy = SOFT_POLICY if arm == A2 else None
        self.residual_policy = RESIDUAL_POLICY if arm == A3 else None
        self.shared_account = True
        self._own_used = {event_id: Decimal('0') for event_id in self.event_ids}
        self._borrowed_out = {event_id: Decimal('0') for event_id in self.event_ids}
        self._pool_used = Decimal('0')
        if arm == A2:
            self._unreserved_capacity = RESIDUAL
        else:
            self._unreserved_capacity = Decimal('0')
        self._unreserved_used = Decimal('0')
        if arm == A3:
            self.non_trading_residual_bucket = RESIDUAL
        else:
            self.non_trading_residual_bucket = Decimal('0')
        self._orders = {}
        self.borrow_log = []
        self.unreserved_draws = []
        self._borrow_sequence = 0
        self.binding = instrument_binding()

    def _require_event(self, event_id):
        if event_id not in self._index:
            raise UnknownEvent(event_id)
        return event_id

    def unused_reserve(self, event_id):
        event_id = self._require_event(event_id)
        if self.arm == A1:
            return None
        return self.slice - self._own_used[event_id] - self._borrowed_out[event_id]

    @property
    def unreserved_available(self):
        return self._unreserved_capacity - self._unreserved_used

    @property
    def available(self):
        if self.arm == A1:
            return self.c_total - self._pool_used
        if self.arm == A2:
            reserved = sum(
                (self.unused_reserve(event_id) for event_id in self.event_ids),
                Decimal('0'),
            )
            return reserved + self.unreserved_available
        return sum(
            (self.slice - self._own_used[event_id] for event_id in self.event_ids),
            Decimal('0'),
        )

    @property
    def committed(self):
        if self.arm == A1:
            return self._pool_used
        if self.arm == A2:
            own = sum(self._own_used.values(), Decimal('0'))
            lent = sum(self._borrowed_out.values(), Decimal('0'))
            return own + lent + self._unreserved_used
        return sum(self._own_used.values(), Decimal('0'))

    def identity(self):
        return self.available + self.committed + self.non_trading_residual_bucket

    def order(self, order_id):
        try:
            return self._orders[order_id]
        except KeyError as exc:
            raise UnknownOrder(order_id) from exc

    def fund(self, event_id, amount, order_id, quote=None):
        return self.fund_many([{
            'event_id': event_id,
            'amount': amount,
            'order_id': order_id,
            'quote': quote,
        }])[0]

    def fund_quote(self, event_id, role, contracts, price, order_id, series=None):
        locked = quote_lock(role, contracts, price, series=series)
        return self.fund(event_id, locked['lock'], order_id, quote=locked)

    def fund_many(self, requests):
        """Admit several draws. Borrowers run in ascending event_id."""
        if not isinstance(requests, (list, tuple)) or len(requests) == 0:
            raise ValueError('requests')
        parsed = []
        seen_orders = set(self._orders)
        for index, raw in enumerate(requests):
            if not isinstance(raw, dict):
                raise TypeError('request')
            event_id = self._require_event(raw['event_id'])
            amount = _money(raw['amount'], 'amount')
            order_id = raw['order_id']
            if not isinstance(order_id, str) or order_id == '':
                raise ValueError('order_id')
            if order_id in seen_orders:
                raise DuplicateOrder(order_id)
            seen_orders.add(order_id)
            parsed.append((event_id, index, amount, order_id, raw.get('quote')))
        ordered = sorted(parsed, key=lambda row: (row[0], row[1]))
        shadow_own = dict(self._own_used)
        shadow_lent = dict(self._borrowed_out)
        shadow_pool = self._pool_used
        shadow_unreserved = self._unreserved_used
        plans = []
        for event_id, _index, amount, order_id, quote in ordered:
            plan = self._plan(
                event_id, amount, order_id, quote,
                shadow_own, shadow_lent, shadow_pool, shadow_unreserved,
            )
            shadow_own = plan['shadow_own']
            shadow_lent = plan['shadow_lent']
            shadow_pool = plan['shadow_pool']
            shadow_unreserved = plan['shadow_unreserved']
            plans.append(plan)
        return [self._apply(plan) for plan in plans]

    def _plan(self, event_id, amount, order_id, quote,
              shadow_own, shadow_lent, shadow_pool, shadow_unreserved):
        if self.arm == A1:
            available = self.c_total - shadow_pool
            if amount > available:
                raise InsufficientCapital(amount - available)
            return {
                'event_id': event_id,
                'amount': amount,
                'order_id': order_id,
                'quote': quote,
                'own': amount,
                'borrows': (),
                'unreserved': Decimal('0'),
                'shadow_own': shadow_own,
                'shadow_lent': shadow_lent,
                'shadow_pool': shadow_pool + amount,
                'shadow_unreserved': shadow_unreserved,
            }
        if self.arm == A3:
            unused = self.slice - shadow_own[event_id]
            if amount > unused:
                raise CrossEventBorrowForbidden(event_id, amount - unused)
            updated_own = dict(shadow_own)
            updated_own[event_id] = shadow_own[event_id] + amount
            return {
                'event_id': event_id,
                'amount': amount,
                'order_id': order_id,
                'quote': quote,
                'own': amount,
                'borrows': (),
                'unreserved': Decimal('0'),
                'shadow_own': updated_own,
                'shadow_lent': shadow_lent,
                'shadow_pool': shadow_pool,
                'shadow_unreserved': shadow_unreserved,
            }
        remaining = amount
        own_unused = self.slice - shadow_own[event_id] - shadow_lent[event_id]
        take_own = min(remaining, own_unused)
        remaining -= take_own
        borrows = []
        updated_lent = dict(shadow_lent)
        for donor in self.event_ids:
            if remaining == 0:
                break
            if donor == event_id:
                continue
            donor_unused = self.slice - shadow_own[donor] - updated_lent[donor]
            if donor_unused <= 0:
                continue
            take = min(remaining, donor_unused)
            borrows.append((donor, take))
            updated_lent[donor] = updated_lent[donor] + take
            remaining -= take
        unreserved = Decimal('0')
        slack = self._unreserved_capacity - shadow_unreserved
        if remaining > 0 and slack > 0:
            unreserved = min(remaining, slack)
            remaining -= unreserved
        if remaining > 0:
            raise InsufficientCapital(remaining)
        updated_own = dict(shadow_own)
        updated_own[event_id] = shadow_own[event_id] + take_own
        return {
            'event_id': event_id,
            'amount': amount,
            'order_id': order_id,
            'quote': quote,
            'own': take_own,
            'borrows': tuple(borrows),
            'unreserved': unreserved,
            'shadow_own': updated_own,
            'shadow_lent': updated_lent,
            'shadow_pool': shadow_pool,
            'shadow_unreserved': shadow_unreserved + unreserved,
        }

    def _apply(self, plan):
        order = FundedOrder(
            plan['order_id'],
            plan['event_id'],
            plan['amount'],
            plan['own'],
            plan['borrows'],
            plan['unreserved'],
            plan['quote'],
        )
        if self.arm == A1:
            self._pool_used += plan['amount']
        else:
            self._own_used[plan['event_id']] += plan['own']
            for donor, take in plan['borrows']:
                self._borrowed_out[donor] += take
                self._borrow_sequence += 1
                self.borrow_log.append({
                    'policy': SOFT_POLICY,
                    'borrower_event_id': plan['event_id'],
                    'donor_event_id': donor,
                    'amount': take,
                    'order_id': plan['order_id'],
                    'sequence': self._borrow_sequence,
                })
            if plan['unreserved'] > 0:
                self._unreserved_used += plan['unreserved']
                self.unreserved_draws.append({
                    'event_id': plan['event_id'],
                    'amount': plan['unreserved'],
                    'order_id': plan['order_id'],
                })
        self._orders[order.order_id] = order
        if self.identity() != self.c_total:
            raise CapitalError('identity')
        return order

    def release(self, order_id):
        order = self.order(order_id)
        if order.released:
            raise UnknownOrder(order_id)
        if self.arm == A1:
            self._pool_used -= order.amount
        else:
            self._own_used[order.event_id] -= order.own
            for donor, take in order.borrows:
                self._borrowed_out[donor] -= take
            if order.unreserved > 0:
                self._unreserved_used -= order.unreserved
        order.released = True
        if self.identity() != self.c_total:
            raise CapitalError('identity')
        return order

    def draw_residual(self, amount):
        _money(amount, 'amount')
        raise ResidualNotTradable()


def open_account(arm, event_ids=None):
    return CapitalAccount(arm, event_ids)


def promotion_scoreboard(account, wallets=None):
    """Shared-account scoreboard. A wallet list is refused before any total."""
    if wallets is not None:
        raise IndependentWalletSumForbidden()
    if not isinstance(account, CapitalAccount) or not account.shared_account:
        raise IndependentWalletSumForbidden()
    return {
        'promotion_scoreboard': PROMOTION_SCOREBOARD,
        'arm': account.arm,
        'c_total': account.c_total,
        'identity': account.identity(),
        'pnl': None,
        'borrow_count': len(account.borrow_log),
        'formula_id': feebook.EXAMINER_FORMULA_ID,
    }


def measurement_scorecard(account, fee_channel=None, inventory_flat=None, kind='measurement'):
    """Classify through the feebook gate. The account stores no walk P&L."""
    if not isinstance(account, CapitalAccount):
        raise TypeError('account')
    card = {
        'kind': kind,
        'arm': account.arm,
        'c_total': format(account.c_total, 'f'),
        'pnl': None,
    }
    if inventory_flat is not None:
        card['inventory_flat'] = inventory_flat
    if fee_channel is not None:
        card['fee_channel'] = fee_channel
    return feebook.classify_scorecard(card)
