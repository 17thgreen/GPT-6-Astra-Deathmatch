"""Soft-policy measurement on one shared 5000 USD A2 account.

SR0 reuses the capital-structure A2 engine for unused-only FIFO borrows.
SR1 and SR2 change donor selection only. Examiner fees come from
kalshi_feebook_lab_20260922. Queue labels come from
kalshi_rails_lab_20260922. This module does not place live orders and does
not record a walk P&L.
"""
import sys
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PARENT = ROOT.parent
CAPITAL_DIR = PARENT / 'kalshi_capital_structure_lab_20260922'
FEEBOOK_DIR = PARENT / 'kalshi_feebook_lab_20260922'
RAILS_DIR = PARENT / 'kalshi_rails_lab_20260922'
for _path in (CAPITAL_DIR, FEEBOOK_DIR, RAILS_DIR):
    if str(_path) not in sys.path:
        sys.path.insert(0, str(_path))

import capital_structure as capital
import feebook
import rails

SR0 = 'SR0'
SR1 = 'SR1'
SR2 = 'SR2'
ARMS = (SR0, SR1, SR2)
SR0_POLICY = 'borrow_unused_event_id_FIFO'
SR1_POLICY = 'borrow_unused_proportional'
SR2_POLICY = 'soft_blend_pool_fraction_0_5'
POLICIES = {
    SR0: SR0_POLICY,
    SR1: SR1_POLICY,
    SR2: SR2_POLICY,
}
CLOSED_ARMS = (capital.A1, capital.A3)
RESIDUAL_POLICY = 'non_trading_residual_bucket'
PROMOTION_SCOREBOARD = capital.PROMOTION_SCOREBOARD
FORBIDDEN_COMPARISON = capital.FORBIDDEN_COMPARISON
FEATURE_FAMILY = 'Cap-SR'
NOT_FEATURE_FAMILIES = ('F1', 'F2', 'F3')
NEAREST_DEAD_CARDS = ('C1_empty_book', 'Q7_Arm_B_kill')
SCORECARD_FIELDS = (
    'borrow_count_delta_vs_fifo',
    'blend_utilization_gap',
    'soft_breach_or_blend_rate',
)
FEEBOOK_COMMIT = '22371178cb2663250b4762f328069571c48cb551'
RAILS_COMMIT = '6a28e0d6254327ea4e6451c781bec56215ac6cac'
PARENT_CAPITAL_PIN = 'ce4671b8201b3fe49ecab91d684815fe6bd51447'
PACKET_SHA256 = '1f263dec7d7810515c3e32c13f3c5eca4344c4951db762a88ea01a8dfde7b1b3'
STRATEGY_POINTER = capital.STRATEGY_POINTER
CAPITAL_SUBSTRATE = 'A2_shared_soft_reserve'
KNOB = 'soft_policy_only'
ALLOCATION_SCALE = 8
C_TOTAL = capital.C_TOTAL
N_EVENTS = capital.N_EVENTS
R_M = capital.SLICE
RESIDUAL = capital.RESIDUAL
BLEND_SEAT = R_M // 2
LOCAL_SEAT = R_M - BLEND_SEAT
SIGNAL_RETUNE = False
LIVE_ORDERS = False
QUEUE_FRAGILITY_REOPEN = False

PACKET = ROOT / 'SOFT_BLENDED_RESERVES_000_FREEZE_2026-09-23.md'
FROZEN_EXPERIMENT = ROOT / 'FROZEN_EXPERIMENT.json'
EMPTY_RESULTS = ROOT / 'results' / 'EMPTY_RESULTS.json'
LAB_BUNDLE = ROOT / 'SOFT_BLENDED_RESERVES_000'
GOVERNANCE_PACKET = PARENT / 'packets' / 'SOFT_BLENDED_RESERVES_000_FREEZE_2026-09-23.md'
GOVERNANCE_BUNDLE = PARENT / 'packets' / 'SOFT_BLENDED_RESERVES_000'
GOVERNANCE_TREE = PARENT / 'lab' / 'governance' / 'astra' / 'packets'
SHADOW_FREEZE = capital.SHADOW_FREEZE
TAPE_MANIFEST = capital.TAPE_MANIFEST
WEEK_MEMBERSHIP = capital.WEEK_MEMBERSHIP


class SoftReserveError(capital.CapitalError):
    """Soft-policy seating or pro-rata allocation failed."""


class ClosedArm(SoftReserveError):
    """A1 and A3 are not arms of this lab."""

    def __init__(self, arm):
        super().__init__('A1 and A3 stay closed')
        self.arm = arm


class SeatedOrder:
    def __init__(self, order_id, event_id, amount, own, borrows, blend, quote):
        self.order_id = order_id
        self.event_id = event_id
        self.amount = amount
        self.own = own
        self.borrows = borrows
        self.blend = blend
        self.unreserved = Decimal('0')
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


def sha256_file(path):
    return capital.sha256_file(path)


def development_cohort_event_ids():
    return capital.development_cohort_event_ids()


def _money(value, name):
    amount = feebook.as_decimal(value, name)
    if amount <= 0:
        raise ValueError('%s must be positive' % name)
    return amount


def _quantum():
    return Decimal(1).scaleb(-ALLOCATION_SCALE)


def _scaled_units(amount, name):
    units = amount / _quantum()
    if units != units.to_integral_value():
        raise ValueError('%s finer than allocation quantum' % name)
    return int(units)


def _from_units(units):
    return Decimal(units).scaleb(-ALLOCATION_SCALE)


def proportional_takes(donors, need):
    """Pro-rata to unused reserve. Hamilton remainder, event_id tie break.

    donors are (event_id, unused) in ascending event_id. Positive takes sum
    to need and never exceed that donor's unused reserve.
    """
    need_units = _scaled_units(need, 'need')
    parsed = []
    for event_id, unused in donors:
        units = _scaled_units(unused, 'unused')
        if units < 0:
            raise SoftReserveError('unused')
        if units == 0:
            continue
        parsed.append((event_id, units))
    total = sum(units for _event_id, units in parsed)
    if need_units > total:
        raise capital.InsufficientCapital(need - _from_units(total))
    if need_units == 0:
        return []
    if need_units == total:
        return [(event_id, _from_units(units)) for event_id, units in parsed]
    rows = []
    floor_sum = 0
    for event_id, units in parsed:
        numer = need_units * units
        base = numer // total
        remainder = numer % total
        rows.append([event_id, units, base, remainder])
        floor_sum += base
    leftover = need_units - floor_sum
    order = sorted(range(len(rows)), key=lambda index: (-rows[index][3], rows[index][0]))
    for index in order:
        if leftover == 0:
            break
        if rows[index][3] == 0 or rows[index][2] >= rows[index][1]:
            continue
        rows[index][2] += 1
        leftover -= 1
    if leftover != 0:
        raise SoftReserveError('pro-rata leftover')
    takes = []
    taken = 0
    for event_id, units, base, _remainder in rows:
        if base < 0 or base > units:
            raise SoftReserveError('pro-rata cap')
        if base == 0:
            continue
        takes.append((event_id, _from_units(base)))
        taken += base
    if taken != need_units:
        raise SoftReserveError('pro-rata sum')
    return takes


def _seat_fifo_control(event_ids):
    """A2 FIFO engine with the 9 USD residual seated as non-trading."""
    if capital.SOFT_POLICY != SR0_POLICY:
        raise SoftReserveError('A2 soft_policy pin')
    book = capital.CapitalAccount(capital.A2, event_ids)
    if book.arm != capital.A2 or book.soft_policy != SR0_POLICY:
        raise SoftReserveError('A2 control')
    book.non_trading_residual_bucket = RESIDUAL
    book._unreserved_capacity = Decimal('0')
    book._unreserved_used = Decimal('0')
    book.residual_policy = RESIDUAL_POLICY
    if book.identity() != C_TOTAL:
        raise capital.CapitalError('identity')
    if book.non_trading_residual_bucket != RESIDUAL:
        raise SoftReserveError('residual')
    return book


def instrument_binding():
    """State feebook and rails as the fee and queue sources. Rates stay imported."""
    parent = capital.instrument_binding()
    if parent['fee_lab'] != 'kalshi_feebook_lab_20260922':
        raise SoftReserveError('fee_source')
    if parent['rails_lab'] != 'kalshi_rails_lab_20260922':
        raise SoftReserveError('queue_source')
    if parent['examiner_formula_id'] != feebook.EXAMINER_FORMULA_ID:
        raise SoftReserveError('fee_source')
    if parent['fee_credit_rule_id'] != rails.FEE_CREDIT_RULE_ID:
        raise SoftReserveError('queue_source')
    if parent['primary_queue_ahead'] != rails.scenario_queue('q3300'):
        raise SoftReserveError('queue_source')
    if parent['harsh_twin_queue_ahead'] != rails.scenario_queue('q10000'):
        raise SoftReserveError('queue_source')
    return {
        'fee_source': 'feebook',
        'queue_source': 'rails',
        'fee_lab': parent['fee_lab'],
        'rails_lab': parent['rails_lab'],
        'fee_pin': FEEBOOK_COMMIT,
        'rails_pin': RAILS_COMMIT,
        'parent_capital_lab_pin': PARENT_CAPITAL_PIN,
        'knob': KNOB,
        'capital_substrate': CAPITAL_SUBSTRATE,
        'closed_arms': CLOSED_ARMS,
        'fee_is_knob': False,
        'queue_is_knob': False,
        'signal_retune': SIGNAL_RETUNE,
        'live_orders': LIVE_ORDERS,
        'queue_fragility_reopen': QUEUE_FRAGILITY_REOPEN,
        'primary_stress': parent['primary_stress'],
        'primary_queue_ahead': parent['primary_queue_ahead'],
        'harsh_twin_stress': parent['harsh_twin_stress'],
        'harsh_twin_queue_ahead': parent['harsh_twin_queue_ahead'],
        'harsh_twin_is_capital_knob': False,
        'examiner_formula_id': parent['examiner_formula_id'],
        'fee_credit_rule_id': parent['fee_credit_rule_id'],
        'taker_rate': parent['taker_rate'],
        'maker_rate': parent['maker_rate'],
        'strategy_pointer': STRATEGY_POINTER,
        'paircheck_varied': False,
        'feature_family': FEATURE_FAMILY,
    }


def execution_adapter():
    """There is no live adapter in this lab."""
    raise capital.LiveOrdersForbidden()


def compare_independent_wallets_to_shared_account(*_args, **_kwargs):
    """Refuse the forbidden comparison. This function does not add wallets."""
    raise capital.IndependentWalletSumForbidden()


def published_scorecard():
    """Examiner fields. This function does not compute them."""
    card = {field: None for field in SCORECARD_FIELDS}
    card['results'] = None
    card['pnl'] = None
    return card


def _parse_requests(account, requests):
    if not isinstance(requests, (list, tuple)) or len(requests) == 0:
        raise ValueError('requests')
    parsed = []
    seen_orders = set(account._orders)
    for index, raw in enumerate(requests):
        if not isinstance(raw, dict):
            raise TypeError('request')
        event_id = account._require_event(raw['event_id'])
        amount = _money(raw['amount'], 'amount')
        order_id = raw['order_id']
        if not isinstance(order_id, str) or order_id == '':
            raise ValueError('order_id')
        if order_id in seen_orders:
            raise capital.DuplicateOrder(order_id)
        seen_orders.add(order_id)
        parsed.append((event_id, index, amount, order_id, raw.get('quote')))
    return sorted(parsed, key=lambda row: (row[0], row[1]))


class SoftReserveAccount:
    """One shared account. The arm is a soft_policy on the A2 substrate."""

    def __init__(self, arm, event_ids=None):
        if arm in CLOSED_ARMS:
            raise ClosedArm(arm)
        if arm not in ARMS:
            raise ValueError('arm')
        self.arm = arm
        self.soft_policy = POLICIES[arm]
        self.event_ids = capital._event_ids(event_ids)
        self._index = {event_id: position for position, event_id in enumerate(self.event_ids)}
        self.c_total = C_TOTAL
        self.slice = R_M
        self.residual_policy = RESIDUAL_POLICY
        self.shared_account = True
        self.binding = instrument_binding()
        self._orders = {}
        self._borrow_log = []
        self._blend_log = []
        self._borrow_sequence = 0
        self._blend_sequence = 0
        if arm == SR0:
            self._control = _seat_fifo_control(self.event_ids)
            self._own_used = None
            self._borrowed_out = None
            self._local_used = None
            self._blend_used = None
            return
        self._control = None
        self.non_trading_residual_bucket = RESIDUAL
        if arm == SR1:
            self._own_used = {event_id: Decimal('0') for event_id in self.event_ids}
            self._borrowed_out = {event_id: Decimal('0') for event_id in self.event_ids}
            self._local_used = None
            self._blend_used = None
        else:
            if BLEND_SEAT * N_EVENTS + LOCAL_SEAT * N_EVENTS + RESIDUAL != C_TOTAL:
                raise SoftReserveError('seat')
            self._own_used = None
            self._borrowed_out = None
            self._local_used = {event_id: Decimal('0') for event_id in self.event_ids}
            self._blend_used = Decimal('0')
            self.blend_capacity = BLEND_SEAT * N_EVENTS
            self.local_capacity = LOCAL_SEAT
        if self.identity() != self.c_total:
            raise capital.CapitalError('identity')

    def _require_event(self, event_id):
        if event_id not in self._index:
            raise capital.UnknownEvent(event_id)
        return event_id

    @property
    def a2_control(self):
        if self._control is None:
            raise SoftReserveError('a2 control')
        return self._control

    @property
    def borrow_log(self):
        if self._control is not None:
            return self._control.borrow_log
        return self._borrow_log

    @property
    def blend_log(self):
        return self._blend_log

    @property
    def unreserved_draws(self):
        if self._control is not None:
            return self._control.unreserved_draws
        return []

    def unused_reserve(self, event_id):
        event_id = self._require_event(event_id)
        if self._control is not None:
            return self._control.unused_reserve(event_id)
        if self.arm == SR1:
            return self.slice - self._own_used[event_id] - self._borrowed_out[event_id]
        return self.local_capacity - self._local_used[event_id]

    @property
    def blend_available(self):
        if self.arm != SR2:
            return Decimal('0')
        return self.blend_capacity - self._blend_used

    @property
    def non_trading_residual_bucket(self):
        if self._control is not None:
            return self._control.non_trading_residual_bucket
        return self._residual_bucket

    @non_trading_residual_bucket.setter
    def non_trading_residual_bucket(self, amount):
        self._residual_bucket = amount

    @property
    def available(self):
        if self._control is not None:
            return self._control.available
        if self.arm == SR1:
            return sum(
                (self.unused_reserve(event_id) for event_id in self.event_ids),
                Decimal('0'),
            )
        local = sum(
            (self.unused_reserve(event_id) for event_id in self.event_ids),
            Decimal('0'),
        )
        return local + self.blend_available

    @property
    def committed(self):
        if self._control is not None:
            return self._control.committed
        if self.arm == SR1:
            own = sum(self._own_used.values(), Decimal('0'))
            lent = sum(self._borrowed_out.values(), Decimal('0'))
            return own + lent
        local = sum(self._local_used.values(), Decimal('0'))
        return local + self._blend_used

    def identity(self):
        if self._control is not None:
            return self._control.identity()
        return self.available + self.committed + self.non_trading_residual_bucket

    def order(self, order_id):
        if self._control is not None:
            return self._control.order(order_id)
        try:
            return self._orders[order_id]
        except KeyError as exc:
            raise capital.UnknownOrder(order_id) from exc

    def fund(self, event_id, amount, order_id, quote=None):
        return self.fund_many([{
            'event_id': event_id,
            'amount': amount,
            'order_id': order_id,
            'quote': quote,
        }])[0]

    def fund_quote(self, event_id, role, contracts, price, order_id, series=None):
        locked = capital.quote_lock(role, contracts, price, series=series)
        return self.fund(event_id, locked['lock'], order_id, quote=locked)

    def fund_many(self, requests):
        if self._control is not None:
            return self._control.fund_many(requests)
        ordered = _parse_requests(self, requests)
        if self.arm == SR1:
            shadow_own = dict(self._own_used)
            shadow_lent = dict(self._borrowed_out)
            plans = []
            for event_id, _index, amount, order_id, quote in ordered:
                plan = self._plan_proportional(
                    event_id, amount, order_id, quote, shadow_own, shadow_lent,
                )
                shadow_own = plan['shadow_own']
                shadow_lent = plan['shadow_lent']
                plans.append(plan)
            return [self._apply_proportional(plan) for plan in plans]
        shadow_local = dict(self._local_used)
        shadow_blend = self._blend_used
        plans = []
        for event_id, _index, amount, order_id, quote in ordered:
            plan = self._plan_blend(
                event_id, amount, order_id, quote, shadow_local, shadow_blend,
            )
            shadow_local = plan['shadow_local']
            shadow_blend = plan['shadow_blend']
            plans.append(plan)
        return [self._apply_blend(plan) for plan in plans]

    def _plan_proportional(self, event_id, amount, order_id, quote, shadow_own, shadow_lent):
        remaining = amount
        own_unused = self.slice - shadow_own[event_id] - shadow_lent[event_id]
        take_own = min(remaining, own_unused)
        remaining -= take_own
        donors = []
        for donor in self.event_ids:
            if donor == event_id:
                continue
            unused = self.slice - shadow_own[donor] - shadow_lent[donor]
            if unused > 0:
                donors.append((donor, unused))
        if remaining > 0:
            borrows = proportional_takes(donors, remaining)
        else:
            borrows = []
        updated_own = dict(shadow_own)
        updated_own[event_id] = shadow_own[event_id] + take_own
        updated_lent = dict(shadow_lent)
        for donor, take in borrows:
            updated_lent[donor] = updated_lent[donor] + take
        return {
            'event_id': event_id,
            'amount': amount,
            'order_id': order_id,
            'quote': quote,
            'own': take_own,
            'borrows': tuple(borrows),
            'shadow_own': updated_own,
            'shadow_lent': updated_lent,
        }

    def _apply_proportional(self, plan):
        order = SeatedOrder(
            plan['order_id'], plan['event_id'], plan['amount'], plan['own'],
            plan['borrows'], Decimal('0'), plan['quote'],
        )
        self._own_used[plan['event_id']] += plan['own']
        for donor, take in plan['borrows']:
            self._borrowed_out[donor] += take
            self._borrow_sequence += 1
            self._borrow_log.append({
                'policy': self.soft_policy,
                'borrower_event_id': plan['event_id'],
                'donor_event_id': donor,
                'amount': take,
                'order_id': plan['order_id'],
                'sequence': self._borrow_sequence,
            })
        self._orders[order.order_id] = order
        if self.identity() != self.c_total:
            raise capital.CapitalError('identity')
        return order

    def _plan_blend(self, event_id, amount, order_id, quote, shadow_local, shadow_blend):
        remaining = amount
        local_unused = self.local_capacity - shadow_local[event_id]
        take_local = min(remaining, local_unused)
        remaining -= take_local
        blend_unused = self.blend_capacity - shadow_blend
        take_blend = min(remaining, blend_unused)
        remaining -= take_blend
        if remaining > 0:
            raise capital.InsufficientCapital(remaining)
        updated_local = dict(shadow_local)
        updated_local[event_id] = shadow_local[event_id] + take_local
        return {
            'event_id': event_id,
            'amount': amount,
            'order_id': order_id,
            'quote': quote,
            'own': take_local,
            'blend': take_blend,
            'shadow_local': updated_local,
            'shadow_blend': shadow_blend + take_blend,
        }

    def _apply_blend(self, plan):
        order = SeatedOrder(
            plan['order_id'], plan['event_id'], plan['amount'], plan['own'],
            (), plan['blend'], plan['quote'],
        )
        self._local_used[plan['event_id']] += plan['own']
        if plan['blend'] > 0:
            self._blend_used += plan['blend']
            self._blend_sequence += 1
            self._blend_log.append({
                'policy': self.soft_policy,
                'borrower_event_id': plan['event_id'],
                'source': 'blend_pool',
                'amount': plan['blend'],
                'order_id': plan['order_id'],
                'sequence': self._blend_sequence,
            })
        self._orders[order.order_id] = order
        if self.identity() != self.c_total:
            raise capital.CapitalError('identity')
        if self.borrow_log:
            raise SoftReserveError('blend has no cross-event donor')
        return order

    def release(self, order_id):
        if self._control is not None:
            order = self._control.release(order_id)
            if self.identity() != self.c_total:
                raise capital.CapitalError('identity')
            return order
        order = self.order(order_id)
        if order.released:
            raise capital.UnknownOrder(order_id)
        if self.arm == SR1:
            self._own_used[order.event_id] -= order.own
            for donor, take in order.borrows:
                self._borrowed_out[donor] -= take
        else:
            self._local_used[order.event_id] -= order.own
            if order.blend > 0:
                self._blend_used -= order.blend
        order.released = True
        if self.identity() != self.c_total:
            raise capital.CapitalError('identity')
        return order

    def draw_residual(self, amount):
        _money(amount, 'amount')
        raise capital.ResidualNotTradable()


def open_account(arm, event_ids=None):
    if arm in CLOSED_ARMS or arm in ('A1', 'A3'):
        raise ClosedArm(arm)
    return SoftReserveAccount(arm, event_ids)


def promotion_scoreboard(account, wallets=None):
    """Shared-account scoreboard. A wallet list is refused before any total."""
    if wallets is not None:
        raise capital.IndependentWalletSumForbidden()
    if not isinstance(account, SoftReserveAccount) or not account.shared_account:
        raise capital.IndependentWalletSumForbidden()
    board = {
        'promotion_scoreboard': PROMOTION_SCOREBOARD,
        'arm': account.arm,
        'soft_policy': account.soft_policy,
        'c_total': account.c_total,
        'identity': account.identity(),
        'pnl': None,
    }
    board.update(published_scorecard())
    return board


def measurement_scorecard(account, fee_channel=None, inventory_flat=None, kind='measurement'):
    """Classify through the feebook gate. The account stores no walk P&L."""
    if not isinstance(account, SoftReserveAccount):
        raise TypeError('account')
    card = {
        'kind': kind,
        'arm': account.arm,
        'soft_policy': account.soft_policy,
        'c_total': format(account.c_total, 'f'),
        'pnl': None,
    }
    card.update(published_scorecard())
    if inventory_flat is not None:
        card['inventory_flat'] = inventory_flat
    if fee_channel is not None:
        card['fee_channel'] = fee_channel
    return feebook.classify_scorecard(card)
