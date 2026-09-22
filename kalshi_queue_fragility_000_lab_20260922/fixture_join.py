"""Read-only join of Q6-000 fill and order fixtures through this lab's arms.

This module lives in kalshi_queue_fragility_000_lab_20260922. There is no
second queue-fragility directory. Pick A fixture loading lives in
kalshi_r2p1_hygiene_000_lab_20260922/fixture_join.py. Examiner fees come from
kalshi_feebook_lab_20260922 through queue_fragility.feebook_binding. Queue
ahead, participation, and queue model come from queue_fragility.arm_queue_params.
This module does not place live orders, does not retune Q6-000, and does not
write scorecard metrics into FROZEN_EXPERIMENT.json.
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
LAB_DIRECTORY = 'kalshi_queue_fragility_000_lab_20260922'
HYGIENE_LAB = 'kalshi_r2p1_hygiene_000_lab_20260922'
HYGIENE_FIXTURE_JOIN = PARENT / HYGIENE_LAB / 'fixture_join.py'
FEEBOOK_DIR = PARENT / 'kalshi_feebook_lab_20260922'
RAILS_DIR = PARENT / 'kalshi_rails_lab_20260922'
for _path in (ROOT, FEEBOOK_DIR, RAILS_DIR):
    if str(_path) not in sys.path:
        sys.path.insert(0, str(_path))

import feebook
import queue_fragility
import rails

EXPERIMENT_ID = 'QF_fixture_join_000_20260922'
STRATEGY_POINTER = 'Q6-000'
PICK = 'B'
SECOND_LAB = False
FEEBOOK_COMMIT = '22371178cb2663250b4762f328069571c48cb551'
RAILS_COMMIT = '6a28e0d6254327ea4e6451c781bec56215ac6cac'
QUEUE_FRAGILITY_PY_COMMIT = 'c33af159d00c07f2d66b2f93174cfcdb4cde8d37'
PRIOR_A_MERGE = '80050e9b6d015cbf394ea8443dd550eea4c2f1ee'
HYGIENE_FIXTURE_JOIN_COMMIT = '79800a82b8ad2c1e10f614f69fd7105d11e0d041'
PACKET = PARENT / 'packets' / 'QF_FIXTURE_JOIN_000_FREEZE_2026-09-22.md'
PACKET_SHA256 = 'd95adb9b7e8aba852134c96b8f0f7d35a76bbf68254b8808f82f99ec82bb6ca4'
PACKET_DIR = PARENT / 'packets' / 'QF_FIXTURE_JOIN_000'
PACKET_RESULTS = PACKET_DIR / 'results.json'
PACKET_FROZEN = PACKET_DIR / 'FROZEN_EXPERIMENT.json'
PACKET_KERNEL = PACKET_DIR / 'freeze.json'
FROZEN_EXPERIMENT = ROOT / 'FROZEN_EXPERIMENT.json'
EMPTY_RESULTS = ROOT / 'results' / 'EMPTY_RESULTS.json'
PRIMARY_FILLS_REL = 'nfl_factorial_lab_20260921/results/q3300_d0.25_000_fills.jsonl.gz'
PRIMARY_ORDERS_REL = 'nfl_factorial_lab_20260921/results/q3300_d0.25_000_orders.jsonl.gz'
PRIMARY_FILLS = PARENT / PRIMARY_FILLS_REL
PRIMARY_ORDERS = PARENT / PRIMARY_ORDERS_REL
PRIMARY_FILLS_SHA256 = '9d56f5d3c599e092606be9f4a1ad41ae8baabff4921d3d722adf0b57ac944a3f'
PRIMARY_ORDERS_SHA256 = 'c390801b9a7cf6d182d2d097123ed944792980524a7975e6e59a904a530f4b1c'
STRESS_FILLS_REL = 'nfl_factorial_lab_20260921/results/q10000_d0.25_000_fills.jsonl.gz'
STRESS_ORDERS_REL = 'nfl_factorial_lab_20260921/results/q10000_d0.25_000_orders.jsonl.gz'
STRESS_FILLS_SHA256 = '678d6cb602fb832f8a77ac7a0cfefd9a4d8390002b0962ddc956ba1f19f4b59d'
STRESS_ORDERS_SHA256 = 'e16632b630058854bfc6ac410cb960d5439fb8a151e180d0793c37e8f92068d9'
STRESS_ROLE = 'queue_label_only_not_a_fee_knob'
SYNTHETIC_FILLS = ROOT / 'fixtures' / 'synthetic_q3300_d0.25_000_fills.jsonl'
SYNTHETIC_ORDERS = ROOT / 'fixtures' / 'synthetic_q3300_d0.25_000_orders.jsonl'
OUTPUT_KEYS = (
    'fill_rate_delta_vs_q3300',
    'adverse_queue_exposure',
    'participation_stress_gap',
    'results',
    'pnl',
)
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
_LEDGER_NAME = re.compile(
    r'^(?:synthetic_)?(q3300|q10000)_(d[0-9]+(?:\.[0-9]+)?)_000_(fills|orders)$'
)


class FixtureJoinError(Exception):
    """The ledger could not be joined, or a scorecard write was requested."""


class ScorecardPromotionRefused(FixtureJoinError):
    """Filled scorecard metrics stay out of the freeze packet."""

    def __init__(self):
        super().__init__('scorecard metrics stay null until Examiner-ready')


def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def execution_adapter():
    """No live order client lives in this lab."""
    raise queue_fragility.LiveOrdersForbidden()


def instrument_binding():
    """Fee binding once. Queue parameters once per arm. Rates stay in feebook."""
    fee = queue_fragility.feebook_binding()
    return {
        'experiment_id': EXPERIMENT_ID,
        'lab_directory': LAB_DIRECTORY,
        'pick': PICK,
        'second_lab': SECOND_LAB,
        'strategy_pointer': STRATEGY_POINTER,
        'feebook_commit': FEEBOOK_COMMIT,
        'rails_commit': RAILS_COMMIT,
        'queue_fragility_py_commit': QUEUE_FRAGILITY_PY_COMMIT,
        'prior_a_merge': PRIOR_A_MERGE,
        'hygiene_fixture_join': str(HYGIENE_FIXTURE_JOIN.relative_to(PARENT)),
        'hygiene_fixture_join_commit': HYGIENE_FIXTURE_JOIN_COMMIT,
        'examiner_formula_id': fee['formula_id'],
        'fee_fixed': FEEBOOK_COMMIT,
        'fee_is_knob': False,
        'arms': {arm: queue_fragility.arm_queue_params(arm) for arm in queue_fragility.ARMS},
        'live_orders': False,
        'signal_retune': False,
        'forbid_capital_A2_A3': True,
        'stress_role': STRESS_ROLE,
    }


def published_scorecard():
    """The freeze outputs. Always null in this harness."""
    scorecard = {key: None for key in OUTPUT_KEYS}
    scorecard['status'] = 'NOT_RUN'
    scorecard['pick'] = PICK
    return scorecard


def assert_null_scorecard(payload):
    """Raise when a caller tries to store a filled metric."""
    if not isinstance(payload, dict):
        raise ScorecardPromotionRefused()
    for key in OUTPUT_KEYS:
        if payload.get(key) is not None:
            raise ScorecardPromotionRefused()
    return payload


def write_scorecard(_payload):
    """This harness does not write the freeze packet."""
    raise ScorecardPromotionRefused()


def stress_pin():
    """Harsh twin paths. The default join does not open them."""
    return {
        'fills': STRESS_FILLS_REL,
        'orders': STRESS_ORDERS_REL,
        'fills_sha256': STRESS_FILLS_SHA256,
        'orders_sha256': STRESS_ORDERS_SHA256,
        'role': STRESS_ROLE,
        'loaded': False,
    }


def production_present():
    return PRIMARY_FILLS.is_file() and PRIMARY_ORDERS.is_file()


def resolve_primary():
    """Production gzip when both pinned files exist and match their sha256.

    Otherwise the synthetic schema stand-in. Either choice is a read source.
    The published scorecard stays null.
    """
    if production_present():
        fills_sha = sha256_file(PRIMARY_FILLS)
        orders_sha = sha256_file(PRIMARY_ORDERS)
        if fills_sha != PRIMARY_FILLS_SHA256 or orders_sha != PRIMARY_ORDERS_SHA256:
            raise FixtureJoinError('production pin sha256')
        return {
            'source': 'production_pin',
            'fills_path': PRIMARY_FILLS,
            'orders_path': PRIMARY_ORDERS,
            'production_present': True,
        }
    return {
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
        return Decimal(str(value))
    return feebook.as_decimal(value, name)


def ledger_identity(path):
    """Scenario, delay, and strategy label from a Q6-000 ledger filename."""
    name = Path(path).name
    if name.endswith('.jsonl.gz'):
        stem = name[:-len('.jsonl.gz')]
    elif name.endswith('.jsonl'):
        stem = name[:-len('.jsonl')]
    else:
        raise FixtureJoinError('ledger name')
    match = _LEDGER_NAME.fullmatch(stem)
    if match is None:
        raise FixtureJoinError('ledger name')
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
        raise FixtureJoinError('ledger name')
    rows = []
    with opener(path, 'rt', encoding='utf-8') as handle:
        for line_number, line in enumerate(handle, start=1):
            text = line.strip()
            if text == '':
                continue
            row = json.loads(text)
            if not isinstance(row, dict):
                raise FixtureJoinError('ledger row %s' % line_number)
            rows.append(row)
    if not rows:
        raise FixtureJoinError('empty ledger')
    return rows


def _require_keys(row, required, label):
    missing = [key for key in required if key not in row]
    if missing:
        raise FixtureJoinError('%s missing %s' % (label, ','.join(missing)))


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
            raise FixtureJoinError('order outcome')
        order_id = row['order_id']
        if isinstance(order_id, bool) or not isinstance(order_id, int):
            raise FixtureJoinError('order_id')
        if order_id in indexed:
            raise FixtureJoinError('duplicate order_id')
        indexed[order_id] = row
    return indexed


def intent_from_order(order):
    """One maker quote. Queue ahead is not taken from the order row."""
    ticker = order['ticker']
    if not isinstance(ticker, str) or ticker == '':
        raise FixtureJoinError('ticker')
    return rails.QuoteIntent(
        ticker,
        order['outcome'],
        ledger_decimal(order['price'], 'price'),
        ledger_decimal(order['submitted_quantity'], 'submitted_quantity'),
    )


def trade_from_fill(fill):
    """One print aimed at the resting outcome. Size is the fill size."""
    outcome = fill['outcome']
    if outcome not in ('yes', 'no'):
        raise FixtureJoinError('fill outcome')
    ticker = fill['ticker']
    if not isinstance(ticker, str) or ticker == '':
        raise FixtureJoinError('ticker')
    price = ledger_decimal(fill['price'], 'price')
    size = ledger_decimal(fill['size'], 'size')
    if size <= 0:
        raise FixtureJoinError('size')
    taker_side = 'no' if outcome == 'yes' else 'yes'
    if feebook.TAKER_FILLS_RESTING[taker_side] != outcome:
        raise FixtureJoinError('polarity')
    yes_price = price if outcome == 'yes' else feebook.ONE - price
    return {
        'ticker': ticker,
        'taker_side': taker_side,
        'yes_price': yes_price,
        'size': size,
        'created_time': fill['at'],
    }


def _ledger_initial_queue(order):
    if order.get('initial_queue') is None:
        return None
    return ledger_decimal(order['initial_queue'], 'initial_queue')


def _arm_slice(arm, intent, trade):
    """One arm on one quote and one print. Profit fields stay null."""
    measured = queue_fragility.measure_arm(arm, [intent], [trade])
    params = measured['queue_params']
    if params != queue_fragility.arm_queue_params(arm):
        raise FixtureJoinError('arm params')
    return {
        'arm': arm,
        'queue_params': params,
        'filled': measured['filled'],
        'requested': measured['requested'],
        'fill_rate': measured['fill_rate'],
        'slice_adverse_contracts': measured['adverse_queue_exposure'],
        'eligible_volume': measured['eligible_volume'],
        'fills': measured['fills'],
        'results': None,
        'pnl': None,
    }


def label_joined_fill(fill, order):
    """One fill through QF0, QF1, and QF2. The row carries no profit."""
    role = fill['kind']
    if role not in ('maker', 'taker'):
        raise FixtureJoinError('kind')
    if role == 'taker':
        return {
            'order_id': fill['order_id'],
            'role': 'taker',
            'arms': None,
            'ledger_initial_queue': None,
            'pnl': None,
        }
    if order is None:
        raise FixtureJoinError('maker order_id')
    if order['ticker'] != fill['ticker'] or order['outcome'] != fill['outcome']:
        raise FixtureJoinError('maker order_id')
    intent = intent_from_order(order)
    trade = trade_from_fill(fill)
    fee = queue_fragility.feebook_binding()
    arms = {}
    for arm in queue_fragility.ARMS:
        labeled = _arm_slice(arm, intent, trade)
        for produced in labeled['fills']:
            if produced['formula_id'] != fee['formula_id']:
                raise FixtureJoinError('examiner formula')
            if produced['rate'] != fee['maker_rate']:
                raise FixtureJoinError('examiner rate')
            if produced['rounded_up'] is not False:
                raise FixtureJoinError('fill round_up')
        arms[arm] = labeled
    return {
        'order_id': order['order_id'],
        'role': 'maker',
        'arms': arms,
        'ledger_initial_queue': _ledger_initial_queue(order),
        'intent': intent,
        'trade': trade,
        'pnl': None,
    }


def join_rows(fills, orders, *, source, fills_path, orders_path, assumed_scenario):
    """Join already loaded rows. Does not write a scorecard."""
    if assumed_scenario not in ('q3300', 'q10000'):
        raise FixtureJoinError('assumed scenario')
    if not fills or not orders:
        raise FixtureJoinError('empty ledger')
    indexed = _index_orders(orders)
    labels = []
    previous_at = None
    maker_rows = 0
    taker_rows = 0
    fee = queue_fragility.feebook_binding()
    for arm in queue_fragility.ARMS:
        if queue_fragility.feebook_binding() != fee:
            raise FixtureJoinError('feebook binding')
    for fill in fills:
        _require_keys(fill, REQUIRED_FILL_KEYS, 'fill')
        if fill['outcome'] not in ('yes', 'no'):
            raise FixtureJoinError('fill outcome')
        observed_at = ledger_decimal(fill['at'], 'at')
        if previous_at is not None and observed_at < previous_at:
            raise FixtureJoinError('fill time order')
        previous_at = observed_at
        role = fill['kind']
        order = None
        if role == 'maker':
            order_id = fill['order_id']
            if order_id not in indexed:
                raise FixtureJoinError('maker order_id')
            order = indexed[order_id]
            maker_rows += 1
        elif role == 'taker':
            taker_rows += 1
        else:
            raise FixtureJoinError('kind')
        labels.append(label_joined_fill(fill, order))
    published = assert_null_scorecard(published_scorecard())
    report = {
        'experiment_id': EXPERIMENT_ID,
        'pick': PICK,
        'lab_directory': LAB_DIRECTORY,
        'source': source,
        'fills_path': str(fills_path),
        'orders_path': str(orders_path),
        'assumed_scenario': assumed_scenario,
        'strategy_label': '000',
        'row_count': len(labels),
        'maker_rows': maker_rows,
        'taker_rows': taker_rows,
        'ignored_fill_keys': _ignored_keys(fills, REQUIRED_FILL_KEYS, OPTIONAL_FILL_KEYS),
        'carried_unread': CARRIED_UNREAD,
        'fee_binding': fee,
        'arms_run': queue_fragility.ARMS,
        'labels': labels,
        'published': published,
        'promoted': False,
        'stress': stress_pin(),
    }
    for key in OUTPUT_KEYS:
        report[key] = None
    return report


def join_ledgers(fills_path, orders_path, *, source):
    """Load a fill ledger and its order ledger, then label the join."""
    fills_id = ledger_identity(fills_path)
    orders_id = ledger_identity(orders_path)
    if fills_id['kind'] != 'fills' or orders_id['kind'] != 'orders':
        raise FixtureJoinError('ledger pair')
    if fills_id['assumed_scenario'] != orders_id['assumed_scenario']:
        raise FixtureJoinError('ledger pair')
    if fills_id['delay_label'] != orders_id['delay_label']:
        raise FixtureJoinError('ledger pair')
    if fills_id['strategy_label'] != '000' or orders_id['strategy_label'] != '000':
        raise FixtureJoinError('strategy label')
    report = join_rows(
        load_jsonl(fills_path),
        load_jsonl(orders_path),
        assumed_scenario=fills_id['assumed_scenario'],
        source=source,
        fills_path=fills_path,
        orders_path=orders_path,
    )
    report['delay_label'] = fills_id['delay_label']
    return report


def join_resolved(choice=None):
    """Join whichever primary source resolve_primary selected."""
    if choice is None:
        choice = resolve_primary()
    return join_ledgers(choice['fills_path'], choice['orders_path'], source=choice['source'])
