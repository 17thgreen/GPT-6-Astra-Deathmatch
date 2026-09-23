"""Effects-path join of imported Cap-SR arms onto Q6-000 fixtures.

Soft-policy math stays in kalshi_soft_blended_reserves_000_lab_20260923.
This module does not re-implement SR0, SR1, or SR2. It does not place live
orders, does not retune Q6-000, and does not write scorecard metrics.
"""
import gzip
import hashlib
import json
import re
import sys
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PARENT = ROOT.parent
CAP_SR_LAB = 'kalshi_soft_blended_reserves_000_lab_20260923'
CAP_SR_DIR = PARENT / CAP_SR_LAB
if str(CAP_SR_DIR) not in sys.path:
    sys.path.insert(0, str(CAP_SR_DIR))

import soft_policy as soft

EXPERIMENT = 'CAP-SR-EFFECTS-PATH-000'
DIRECTORY = 'kalshi_cap_sr_effects_000_lab_20260923'
FEATURE_FAMILY = 'Cap-SR-FX'
STRATEGY_POINTER = 'Q6-000'
KNOB = 'fixture_stress'
FX0 = 'FX0'
FX1 = 'FX1'
FX_ARMS = (FX0, FX1)
FX0_STRESS = 'q3300_d0.25'
FX1_STRESS = 'synthetic_borrow_stress'
ARM_STRESS = {
    FX0: FX0_STRESS,
    FX1: FX1_STRESS,
}
FEEBOOK_COMMIT = '22371178cb2663250b4762f328069571c48cb551'
RAILS_COMMIT = '6a28e0d6254327ea4e6451c781bec56215ac6cac'
PARENT_CAP_SR_PIN = '45863037a30af6caf9c00361e46fe8bd5444c426'
PARENT_CAP_SR_PIN_PREFIX = '45863037'
PARENT_CAP_SR_FREEZE_SHA256 = '1f263dec7d7810515c3e32c13f3c5eca4344c4951db762a88ea01a8dfde7b1b3'
PARENT_CAPITAL_PIN_PREFIX = 'ce4671b8'
PACKET_SHA256 = 'cd08a93af2659c36f83cd1b9ffc3174364cc767efc374a4e0669e128f6a29074'
BASE_COMMIT = 'cfd5f95a6b2c9bd654ae58bd278f8465b827712b'
SOFT_POLICIES_FIXED = (
    soft.SR0_POLICY,
    soft.SR1_POLICY,
    soft.SR2_POLICY,
)
SCORECARD_FIELDS = (
    'borrow_count_delta_vs_fifo',
    'blend_utilization_gap',
    'soft_breach_or_blend_rate',
    'effects_path_fixture_id',
)
NULL_FIELDS = SCORECARD_FIELDS + ('results', 'pnl')
SIGNAL_RETUNE_000 = False
QUEUE_FRAGILITY_REOPEN = False
DUAL_CAP_SR_LAB = False
LIVE_ORDERS = False
PROMOTION_SCOREBOARD = soft.PROMOTION_SCOREBOARD
FORBIDDEN_COMPARISON = soft.FORBIDDEN_COMPARISON

PACKET = ROOT / 'CAP_SR_EFFECTS_PATH_000_FREEZE_2026-09-23.md'
FROZEN_EXPERIMENT = ROOT / 'FROZEN_EXPERIMENT.json'
EMPTY_RESULTS = ROOT / 'results' / 'EMPTY_RESULTS.json'
LAB_BUNDLE = ROOT / 'CAP_SR_EFFECTS_PATH_000'
GOVERNANCE_PACKET = PARENT / 'packets' / 'CAP_SR_EFFECTS_PATH_000_FREEZE_2026-09-23.md'
GOVERNANCE_BUNDLE = PARENT / 'packets' / 'CAP_SR_EFFECTS_PATH_000'
GOVERNANCE_TREE = PARENT / 'lab' / 'governance' / 'astra' / 'packets'
PARENT_FREEZE = CAP_SR_DIR / 'SOFT_BLENDED_RESERVES_000_FREEZE_2026-09-23.md'

PRIMARY_FILLS_REL = 'nfl_factorial_lab_20260921/results/q3300_d0.25_000_fills.jsonl.gz'
PRIMARY_ORDERS_REL = 'nfl_factorial_lab_20260921/results/q3300_d0.25_000_orders.jsonl.gz'
PRIMARY_FILLS_SHA256 = '9d56f5d3c599e092606be9f4a1ad41ae8baabff4921d3d722adf0b57ac944a3f'
PRIMARY_ORDERS_SHA256 = 'c390801b9a7cf6d182d2d097123ed944792980524a7975e6e59a904a530f4b1c'
SYNTHETIC_FILLS = ROOT / 'fixtures' / 'synthetic_q3300_d0.25_000_fills.jsonl'
SYNTHETIC_ORDERS = ROOT / 'fixtures' / 'synthetic_q3300_d0.25_000_orders.jsonl'
STRESS_FILLS = ROOT / 'fixtures' / 'synthetic_borrow_stress_fills.jsonl'
STRESS_ORDERS = ROOT / 'fixtures' / 'synthetic_borrow_stress_orders.jsonl'

REQUIRED_FILL_KEYS = (
    'at', 'ticker', 'event', 'outcome', 'direction', 'price', 'size', 'fee',
    'kind', 'paired', 'reason', 'inventory_after', 'cash_after', 'order_id',
    'improved', 'resting_seconds', 'queue_remaining', 'completion_instruction',
    'entry_window_open',
)
OPTIONAL_FILL_KEYS = ('outcome_mid_at_fill', 'book', 'transaction_time', 'keepalive')
REQUIRED_ORDER_KEYS = (
    'order_id', 'ticker', 'event', 'outcome', 'direction', 'submitted_at',
    'active_at', 'submitted_quantity', 'price', 'entry_window_open',
    'inventory_at_submission', 'filled_quantity', 'cancel_requested_at',
    'initial_queue',
)
CARRIED_UNREAD = (
    'inventory_after', 'cash_after', 'paired', 'fee', 'queue_remaining',
    'initial_queue',
)
LABEL_KEYS = (
    'fill_index', 'order_id', 'event_id', 'role', 'policies', 'results', 'pnl',
)
POLICY_ROW_KEYS = (
    'soft_policy', 'seated', 'cross_event_borrow', 'blend_draw',
    'formula_id', 'results', 'pnl',
)
_LEDGER_NAME = re.compile(
    r'^(?:synthetic_)?(q3300|q10000)_(d[0-9]+(?:\.[0-9]+)?)_000_(fills|orders)$'
)


class EffectsPathError(Exception):
    """The fixture could not be joined, or a pin disagreed."""


class ScorecardPromotionRefused(EffectsPathError):
    """Filled scorecard metrics stay out of the freeze packet."""

    def __init__(self):
        super().__init__('scorecard metrics stay null until Examiner')


def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def execution_adapter():
    """No live order client lives in this lab."""
    raise soft.capital.LiveOrdersForbidden()


def compare_independent_wallets_to_shared_account(*args, **kwargs):
    """Refuse the forbidden comparison. This function does not add wallets."""
    return soft.compare_independent_wallets_to_shared_account(*args, **kwargs)


def published_scorecard():
    """Examiner fields. This function does not compute them."""
    card = {field: None for field in NULL_FIELDS}
    card['status'] = 'EMPTY_RESULTS_PRE_EXAMINER'
    return card


def assert_null_scorecard(payload):
    """Raise when a caller tries to store a filled metric."""
    if not isinstance(payload, dict):
        raise ScorecardPromotionRefused()
    for key in NULL_FIELDS:
        if key not in payload or payload[key] is not None:
            raise ScorecardPromotionRefused()
    return payload


def write_scorecard(_payload):
    """This harness does not write the freeze packet."""
    raise ScorecardPromotionRefused()


def instrument_binding():
    """Cap-SR import plus the fixture-stress knob. Rates stay in feebook."""
    parent = soft.instrument_binding()
    if parent['fee_source'] != 'feebook' or parent['fee_pin'] != FEEBOOK_COMMIT:
        raise EffectsPathError('fee pin')
    if parent['queue_source'] != 'rails' or parent['rails_pin'] != RAILS_COMMIT:
        raise EffectsPathError('rails pin')
    if parent['strategy_pointer'] != STRATEGY_POINTER:
        raise EffectsPathError('strategy')
    if soft.C_TOTAL != Decimal('5000') or soft.RESIDUAL != Decimal('9'):
        raise EffectsPathError('shared account')
    if soft.R_M != Decimal('161') or soft.N_EVENTS != 31:
        raise EffectsPathError('soft reserve')
    if soft.POLICIES[soft.SR0] != soft.SR0_POLICY:
        raise EffectsPathError('sr0 import')
    if tuple(soft.POLICIES[arm] for arm in soft.ARMS) != SOFT_POLICIES_FIXED:
        raise EffectsPathError('soft policies')
    if not PARENT_CAP_SR_PIN.startswith(PARENT_CAP_SR_PIN_PREFIX):
        raise EffectsPathError('cap-sr pin')
    if not soft.PARENT_CAPITAL_PIN.startswith(PARENT_CAPITAL_PIN_PREFIX):
        raise EffectsPathError('capital pin')
    return {
        'experiment': EXPERIMENT,
        'directory': DIRECTORY,
        'feature_family': FEATURE_FAMILY,
        'knob': KNOB,
        'dual_cap_sr_lab': DUAL_CAP_SR_LAB,
        'cap_sr_lab': CAP_SR_LAB,
        'cap_sr_module': str(Path(soft.__file__).resolve()),
        'cap_sr_pin': PARENT_CAP_SR_PIN,
        'cap_sr_freeze_sha256': PARENT_CAP_SR_FREEZE_SHA256,
        'parent_capital_lab_pin': soft.PARENT_CAPITAL_PIN,
        'fee_source': parent['fee_source'],
        'queue_source': parent['queue_source'],
        'fee_pin': FEEBOOK_COMMIT,
        'rails_pin': RAILS_COMMIT,
        'fee_is_knob': False,
        'queue_is_knob': False,
        'strategy_pointer': STRATEGY_POINTER,
        'signal_retune_000': SIGNAL_RETUNE_000,
        'queue_fragility_reopen': QUEUE_FRAGILITY_REOPEN,
        'live_orders': LIVE_ORDERS,
        'c_total_usd': soft.C_TOTAL,
        'residual_usd': soft.RESIDUAL,
        'residual_policy': soft.RESIDUAL_POLICY,
        'r_m_usd': soft.R_M,
        'promotion_scoreboard': PROMOTION_SCOREBOARD,
        'forbidden': FORBIDDEN_COMPARISON,
        'soft_policies_fixed': SOFT_POLICIES_FIXED,
        'arms': FX_ARMS,
        'primary_stress': FX0_STRESS,
        'primary_queue_ahead': parent['primary_queue_ahead'],
        'examiner_formula_id': parent['examiner_formula_id'],
        'fee_credit_rule_id': parent['fee_credit_rule_id'],
    }


def open_account(arm, event_ids=None):
    """One imported soft-policy account. A1 and A3 stay closed in Cap-SR."""
    return soft.open_account(arm, event_ids)


def promotion_scoreboard(account, wallets=None):
    """Shared-account scoreboard. A wallet list is refused before any total."""
    if wallets is not None:
        raise soft.capital.IndependentWalletSumForbidden()
    board = soft.promotion_scoreboard(account, wallets=None)
    board.update(published_scorecard())
    if board['c_total'] != soft.C_TOTAL or board['pnl'] is not None:
        raise ScorecardPromotionRefused()
    assert_null_scorecard(board)
    return board


def production_paths(root=None):
    base = PARENT if root is None else Path(root)
    return base / PRIMARY_FILLS_REL, base / PRIMARY_ORDERS_REL


def production_present(root=None):
    fills, orders = production_paths(root)
    return fills.is_file() and orders.is_file()


def resolve_fx0(root=None):
    """Production gzip when both pinned files exist and match their sha256.

    Otherwise the synthetic schema stand-in. A present file with the wrong
    hash is refused. The published scorecard stays null either way.
    """
    fills, orders = production_paths(root)
    fills_present = fills.is_file()
    orders_present = orders.is_file()
    if fills_present or orders_present:
        if not (fills_present and orders_present):
            raise EffectsPathError('production pin incomplete')
        if sha256_file(fills) != PRIMARY_FILLS_SHA256:
            raise EffectsPathError('fills sha256')
        if sha256_file(orders) != PRIMARY_ORDERS_SHA256:
            raise EffectsPathError('orders sha256')
        return {
            'arm': FX0,
            'fixture_stress': FX0_STRESS,
            'source': 'production_pin',
            'fills_path': fills,
            'orders_path': orders,
            'production_present': True,
        }
    return {
        'arm': FX0,
        'fixture_stress': FX0_STRESS,
        'source': 'synthetic_schema_standin',
        'fills_path': SYNTHETIC_FILLS,
        'orders_path': SYNTHETIC_ORDERS,
        'production_present': False,
    }


def ledger_decimal(value, name):
    """JSON number to Decimal. Floats are not passed into feebook.as_decimal."""
    if isinstance(value, bool):
        raise TypeError(name)
    if isinstance(value, float):
        return soft.feebook.as_decimal(str(value), name)
    return soft.feebook.as_decimal(value, name)


def ledger_identity(path):
    """Scenario, delay, and strategy label from a Q6-000 ledger filename."""
    name = Path(path).name
    if name.endswith('.jsonl.gz'):
        stem = name[:-len('.jsonl.gz')]
    elif name.endswith('.jsonl'):
        stem = name[:-len('.jsonl')]
    else:
        raise EffectsPathError('ledger name')
    match = _LEDGER_NAME.fullmatch(stem)
    if match is None:
        raise EffectsPathError('ledger name')
    return {
        'assumed_scenario': match.group(1),
        'delay_label': match.group(2),
        'strategy_label': '000',
        'kind': match.group(3),
    }


def load_jsonl(path):
    """One JSON object per line. Gzip when the name ends in .jsonl.gz."""
    path = Path(path)
    if path.name.endswith('.jsonl.gz'):
        opener = gzip.open
    elif path.name.endswith('.jsonl'):
        opener = open
    else:
        raise EffectsPathError('ledger name')
    rows = []
    with opener(path, 'rt', encoding='utf-8') as handle:
        for line_number, line in enumerate(handle, start=1):
            text = line.strip()
            if text == '':
                continue
            row = json.loads(text)
            if not isinstance(row, dict):
                raise EffectsPathError('ledger row %s' % line_number)
            rows.append(row)
    if not rows:
        raise EffectsPathError('empty ledger')
    return rows


def _require_keys(row, required, label):
    missing = [key for key in required if key not in row]
    if missing:
        raise EffectsPathError('%s missing %s' % (label, ','.join(missing)))


def _ignored_keys(rows, required, optional):
    allowed = set(required) | set(optional)
    found = set()
    for row in rows:
        found.update(set(row) - allowed)
    return tuple(sorted(found))


def _index_orders(orders):
    indexed = {}
    for row in orders:
        _require_keys(row, REQUIRED_ORDER_KEYS, 'order')
        if row['outcome'] not in ('yes', 'no'):
            raise EffectsPathError('order outcome')
        order_id = row['order_id']
        if isinstance(order_id, bool) or not isinstance(order_id, int):
            raise EffectsPathError('order_id')
        if order_id in indexed:
            raise EffectsPathError('duplicate order_id')
        indexed[order_id] = row
    return indexed


def _display_path(path):
    path = Path(path)
    try:
        return str(path.resolve().relative_to(PARENT))
    except ValueError:
        return str(path)


def _check_fx0_names(fills_path, orders_path):
    fills_id = ledger_identity(fills_path)
    orders_id = ledger_identity(orders_path)
    if fills_id['kind'] != 'fills' or orders_id['kind'] != 'orders':
        raise EffectsPathError('ledger pair')
    if fills_id['assumed_scenario'] != 'q3300' or orders_id['assumed_scenario'] != 'q3300':
        raise EffectsPathError('fx0 fixture')
    if fills_id['delay_label'] != 'd0.25' or orders_id['delay_label'] != 'd0.25':
        raise EffectsPathError('fx0 fixture')
    if fills_id['strategy_label'] != '000' or orders_id['strategy_label'] != '000':
        raise EffectsPathError('strategy label')
    return fills_id


def _seat_fill(book, event_id, role, size, price, seat_id):
    """One imported fund_quote. Refusal leaves the account unchanged."""
    before_borrow = len(book.borrow_log)
    before_blend = len(book.blend_log)
    try:
        order = book.fund_quote(event_id, role, size, price, seat_id)
    except (soft.capital.InsufficientCapital, soft.rails.MakerCreditRefused):
        seated = False
        formula_id = None
        cross = False
        blend = False
    else:
        seated = True
        formula_id = order.formula_id
        if formula_id != soft.feebook.EXAMINER_FORMULA_ID:
            raise EffectsPathError('examiner formula')
        cross = len(book.borrow_log) > before_borrow
        blend = len(book.blend_log) > before_blend
    if book.identity() != soft.C_TOTAL:
        raise EffectsPathError('identity')
    if book.non_trading_residual_bucket != soft.RESIDUAL:
        raise EffectsPathError('residual')
    return {
        'soft_policy': book.soft_policy,
        'seated': seated,
        'cross_event_borrow': cross,
        'blend_draw': blend,
        'formula_id': formula_id,
        'results': None,
        'pnl': None,
    }


def join_rows(fills, orders, *, arm, fixture_stress, source, fills_path, orders_path):
    """Seat already loaded rows on SR0, SR1, and SR2. Does not write a scorecard."""
    if arm not in FX_ARMS or ARM_STRESS[arm] != fixture_stress:
        raise EffectsPathError('arm')
    if not fills or not orders:
        raise EffectsPathError('empty ledger')
    event_ids = soft.development_cohort_event_ids()
    if len(event_ids) != soft.N_EVENTS:
        raise EffectsPathError('cohort')
    known = set(event_ids)
    indexed = _index_orders(orders)
    accounts = {policy: open_account(policy, event_ids) for policy in soft.ARMS}
    labels = []
    previous_at = None
    for index, fill in enumerate(fills):
        _require_keys(fill, REQUIRED_FILL_KEYS, 'fill')
        if fill['outcome'] not in ('yes', 'no'):
            raise EffectsPathError('fill outcome')
        role = fill['kind']
        if role not in ('maker', 'taker'):
            raise EffectsPathError('kind')
        observed_at = ledger_decimal(fill['at'], 'at')
        if previous_at is not None and observed_at < previous_at:
            raise EffectsPathError('fill time order')
        previous_at = observed_at
        event_id = fill['event']
        if not isinstance(event_id, str) or event_id not in known:
            raise EffectsPathError('event')
        order_id = fill['order_id']
        if isinstance(order_id, bool) or not isinstance(order_id, int):
            raise EffectsPathError('order_id')
        if role == 'maker':
            order = indexed.get(order_id)
            if order is None:
                raise EffectsPathError('maker order_id')
            if order['ticker'] != fill['ticker'] or order['outcome'] != fill['outcome']:
                raise EffectsPathError('maker order_id')
            if order['event'] != event_id:
                raise EffectsPathError('maker order_id')
        price = ledger_decimal(fill['price'], 'price')
        size = ledger_decimal(fill['size'], 'size')
        if size <= 0:
            raise EffectsPathError('size')
        policies = {}
        for policy in soft.ARMS:
            policies[policy] = _seat_fill(
                accounts[policy], event_id, role, size, price,
                'fx-%s-%s' % (index, order_id),
            )
            if policies[policy]['soft_policy'] != soft.POLICIES[policy]:
                raise EffectsPathError('soft policy')
        label = {
            'fill_index': index,
            'order_id': order_id,
            'event_id': event_id,
            'role': role,
            'policies': policies,
            'results': None,
            'pnl': None,
        }
        labels.append(label)
    policy_instrument = {}
    for policy, book in accounts.items():
        if book.identity() != soft.C_TOTAL:
            raise EffectsPathError('identity')
        if book.non_trading_residual_bucket != soft.RESIDUAL:
            raise EffectsPathError('residual')
        if book.c_total != soft.C_TOTAL or book.shared_account is not True:
            raise EffectsPathError('shared account')
        policy_instrument[policy] = {
            'soft_policy': book.soft_policy,
            'borrow_log_nonempty': len(book.borrow_log) > 0,
            'blend_log_nonempty': len(book.blend_log) > 0,
            'seated_fills': sum(1 for row in labels if row['policies'][policy]['seated']),
            'results': None,
            'pnl': None,
        }
    published = assert_null_scorecard(published_scorecard())
    report = {
        'experiment': EXPERIMENT,
        'directory': DIRECTORY,
        'arm': arm,
        'fixture_stress': fixture_stress,
        'source': source,
        'fills_path': _display_path(fills_path),
        'orders_path': _display_path(orders_path),
        'strategy_pointer': STRATEGY_POINTER,
        'soft_policies': SOFT_POLICIES_FIXED,
        'cap_sr_lab': CAP_SR_LAB,
        'cap_sr_pin': PARENT_CAP_SR_PIN,
        'fee_pin': FEEBOOK_COMMIT,
        'rails_pin': RAILS_COMMIT,
        'fee_source': 'feebook',
        'queue_source': 'rails',
        'c_total_usd': soft.C_TOTAL,
        'residual_usd': soft.RESIDUAL,
        'residual_policy': soft.RESIDUAL_POLICY,
        'identity_usd': soft.C_TOTAL,
        'promotion_scoreboard': PROMOTION_SCOREBOARD,
        'row_count': len(labels),
        'ignored_fill_keys': _ignored_keys(fills, REQUIRED_FILL_KEYS, OPTIONAL_FILL_KEYS),
        'carried_unread': CARRIED_UNREAD,
        'labels': labels,
        'policy_instrument': policy_instrument,
        'published': published,
        'promoted': False,
        'dual_cap_sr_lab': False,
        'signal_retune_000': False,
        'queue_fragility_reopen': False,
        'live_orders': False,
    }
    for key in NULL_FIELDS:
        report[key] = None
    assert_null_scorecard(report)
    return EffectsJoin(report, accounts)


class EffectsJoin:
    """In-memory join. `report` is the instrument schema. Accounts stay imported."""

    def __init__(self, report, accounts):
        self.report = report
        self.accounts = accounts


def join_ledgers(fills_path, orders_path, *, arm, fixture_stress, source, q3300_name=False):
    """Load a fill ledger and its order ledger, then seat the join."""
    if q3300_name or arm == FX0:
        _check_fx0_names(fills_path, orders_path)
    elif arm != FX1 or fixture_stress != FX1_STRESS:
        raise EffectsPathError('arm')
    return join_rows(
        load_jsonl(fills_path),
        load_jsonl(orders_path),
        arm=arm,
        fixture_stress=fixture_stress,
        source=source,
        fills_path=fills_path,
        orders_path=orders_path,
    )


def join_fx0(root=None):
    """Join whichever FX0 source resolve_fx0 selected."""
    choice = resolve_fx0(root)
    return join_ledgers(
        choice['fills_path'],
        choice['orders_path'],
        arm=FX0,
        fixture_stress=FX0_STRESS,
        source=choice['source'],
    )


def join_fx1():
    """Unit-only borrow-stress fixture. Does not read the production gzip."""
    return join_ledgers(
        STRESS_FILLS,
        STRESS_ORDERS,
        arm=FX1,
        fixture_stress=FX1_STRESS,
        source='synthetic_borrow_stress',
    )


def join_arm(arm, root=None):
    """FX0 or FX1. Soft policies are not selected here."""
    if arm == FX0:
        return join_fx0(root)
    if arm == FX1:
        return join_fx1()
    raise EffectsPathError('arm')
