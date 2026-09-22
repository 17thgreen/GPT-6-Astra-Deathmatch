"""Queue-fragility instrument for Q6-000 under R1-P5.

Arms differ in rails queue parameters. Examiner fees stay on the imported
R1-P1 feebook channel. This module does not place live orders and does not
record a walk P&L.
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

EXPERIMENT_ID = 'queue_fragility_000_r1p5_20260922'
STRATEGY_POINTER = 'Q6-000'
FEEBOOK_COMMIT = '22371178cb2663250b4762f328069571c48cb551'
RAILS_COMMIT = '6a28e0d6254327ea4e6451c781bec56215ac6cac'
PRIOR_R2P1_MERGE = '25ec05381207252abb8abec8f6f99e30765f9704'
PACKET_SHA256 = 'e01d684abefd2d919ac6546f85619a246ce73098c04f7b24c84451ff49b00308'
KNOB = 'queue_fill_stress_only'
QF0 = 'QF0_q3300_measured'
QF1 = 'QF1_q10000_stress'
QF2 = 'QF2_front_optimistic'
ARMS = (QF0, QF1, QF2)
QUEUE_PARAM_KEYS = ('queue_ahead_contracts', 'fill_participation', 'queue_model')
OUTPUT_KEYS = (
    'fill_rate_delta_vs_q3300',
    'adverse_queue_exposure',
    'participation_stress_gap',
)
CAPITAL_MODE = 'A1_shared_pool'
FORBIDDEN_CAPITAL_MODES = ('A2_shared_soft_reserve', 'A3_hard_equal_slices')
C_TOTAL = Decimal('5000')
NOT_RUN = 'NOT_RUN'
SYNTHETIC_FIXTURE_ONLY = 'SYNTHETIC_FIXTURE_ONLY'

FACTORIAL_INPUTS = PARENT / 'nfl_factorial_lab_20260921' / 'inputs'
WEEK_MEMBERSHIP = FACTORIAL_INPUTS / 'week_membership.json'
TAPE_MANIFEST = FACTORIAL_INPUTS / 'manifest.json'
SHADOW_FREEZE = PARENT / 'nfl_factorial_lab_20260921' / 'SHADOW_CANDIDATE_FREEZE.json'
FROZEN_EXPERIMENT = ROOT / 'FROZEN_EXPERIMENT.json'
EMPTY_RESULTS = ROOT / 'results' / 'EMPTY_RESULTS.json'
PACKET = ROOT / 'QUEUE_FRAGILITY_000_R1P5_FREEZE_2026-09-22.md'


class QueueFragilityError(Exception):
    """A queue-fragility pin was refused or a completed net was requested."""


class LiveOrdersForbidden(QueueFragilityError):
    """This lab has no live order path."""

    def __init__(self):
        super().__init__('no live orders and no KalshiExecutionAdapter')


class CapitalArmForbidden(QueueFragilityError):
    """A2 and A3 stay closed. The pool is the shared A1 equivalent."""

    def __init__(self):
        super().__init__('capital arms A2 and A3 stay closed')


def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def development_cohort_event_ids():
    """Sorted event ids from the Q6 development membership file. Read only."""
    payload = json.loads(WEEK_MEMBERSHIP.read_text())
    if not isinstance(payload, dict):
        raise QueueFragilityError('week membership')
    event_ids = tuple(sorted(payload.keys()))
    if len(event_ids) != 31:
        raise QueueFragilityError('N_events')
    return event_ids


def execution_adapter():
    """No live order client lives in this lab."""
    raise LiveOrdersForbidden()


def shared_capital(mode=CAPITAL_MODE):
    """One shared 5000 USD pool. A2 and A3 are refused."""
    if mode != CAPITAL_MODE or mode in FORBIDDEN_CAPITAL_MODES:
        raise CapitalArmForbidden()
    return {
        'mode': CAPITAL_MODE,
        'C_total_usd': C_TOTAL,
        'shared_pool': True,
        'a2_reopened': False,
        'a3_reopened': False,
    }


def feebook_binding():
    """Examiner channel from the imported series table. Identical for every arm."""
    table = feebook.load_series_table()
    if table.get('formula_id') != feebook.EXAMINER_FORMULA_ID:
        raise QueueFragilityError('examiner formula')
    default = table['default']
    if default.get('maker_fees_enabled') is not True:
        raise QueueFragilityError('examiner channel keeps maker fees enabled')
    rates = table['rates']
    return {
        'directory': 'kalshi_feebook_lab_20260922',
        'commit': FEEBOOK_COMMIT,
        'formula_id': feebook.EXAMINER_FORMULA_ID,
        'maker_rate': feebook.as_decimal(rates['maker'], 'maker'),
        'taker_rate': feebook.as_decimal(rates['taker'], 'taker'),
        'maker_fees_enabled': True,
        'fill_round_up': False,
        'admission_round_up': True,
        'comparator_formula_id': feebook.GROK_COMPARATOR_FORMULA_ID,
        'fee_is_knob': False,
    }


def arm_queue_params(arm):
    """Rails constructor fields for one arm. Fee fields are absent."""
    participation = rails.FILL_PARTICIPATION_DEFAULT
    if arm == QF0:
        ahead = rails.scenario_queue('q3300')
        model = 'measured'
        if ahead != rails.QUEUE_AHEAD_DEFAULT:
            raise QueueFragilityError('q3300')
    elif arm == QF1:
        ahead = rails.scenario_queue('q10000')
        model = 'measured'
        if ahead != rails.STRESS_QUEUE_AHEAD:
            raise QueueFragilityError('q10000')
    elif arm == QF2:
        ahead = Decimal('0')
        model = 'front'
    else:
        raise ValueError('arm')
    if model == 'front' and ahead != Decimal('0'):
        raise QueueFragilityError('front ahead')
    return {
        'queue_ahead_contracts': ahead,
        'fill_participation': participation,
        'queue_model': model,
    }


def queue_param_changes(left, right):
    """Names of rails queue fields that differ between two arms."""
    left_params = arm_queue_params(left)
    right_params = arm_queue_params(right)
    return tuple(key for key in QUEUE_PARAM_KEYS if left_params[key] != right_params[key])


def open_instrument(arm):
    """QueueInstrument for one arm. The fee table is the feebook default."""
    params = arm_queue_params(arm)
    book = rails.QueueInstrument(
        queue_ahead_contracts=params['queue_ahead_contracts'],
        fill_participation=params['fill_participation'],
        queue_model=params['queue_model'],
    )
    if book.series is not None or book.table is not None:
        raise QueueFragilityError('fee override')
    if book.fill_participation != rails.FILL_PARTICIPATION_DEFAULT:
        raise QueueFragilityError('participation')
    if book.queue_model != params['queue_model']:
        raise QueueFragilityError('queue_model')
    if book.queue_ahead_contracts != params['queue_ahead_contracts']:
        raise QueueFragilityError('queue_ahead')
    return book


def instrument_binding():
    """Fee binding once, queue parameters once per arm."""
    fee = feebook_binding()
    return {
        'experiment_id': EXPERIMENT_ID,
        'strategy_pointer': STRATEGY_POINTER,
        'knob': KNOB,
        'fee_fixed': FEEBOOK_COMMIT,
        'rails_knob': RAILS_COMMIT,
        'prior_r2p1_merge': PRIOR_R2P1_MERGE,
        'fee': fee,
        'arms': {arm: arm_queue_params(arm) for arm in ARMS},
        'capital': shared_capital(),
        'signal_retune': False,
        'live_orders': False,
        'fee_is_knob': False,
    }


def _eligible(book, trade):
    """True when rails would consider this print against a resting order."""
    taker_side = trade.get('taker_side')
    if taker_side not in feebook.TAKER_FILLS_RESTING:
        raise ValueError('taker_side')
    ticker = trade.get('ticker')
    if not isinstance(ticker, str) or ticker == '':
        raise ValueError('ticker')
    outcome = feebook.TAKER_FILLS_RESTING[taker_side]
    resting = book.order(ticker, outcome)
    if resting is None:
        return False, outcome
    yes_price, no_price = book._trade_prices(trade)
    trade_price = no_price if outcome == 'no' else yes_price
    return trade_price <= resting.intent.price, outcome


def measure_arm(arm, intents, trades):
    """Fill and queue-consumption totals for one arm. Cash profit stays null."""
    if arm not in ARMS:
        raise ValueError('arm')
    book = open_instrument(arm)
    book.replace_quotes(intents)
    requested = Decimal('0')
    for intent in book.resting():
        requested += intent.size
    if requested <= 0:
        raise QueueFragilityError('requested size')
    filled = Decimal('0')
    adverse = Decimal('0')
    eligible = Decimal('0')
    fills = []
    for trade in trades:
        if not isinstance(trade, dict):
            raise TypeError('trade')
        through, outcome = _eligible(book, trade)
        ticker = trade['ticker']
        before = book.order(ticker, outcome)
        before_ahead = None if before is None else before.queue_ahead
        produced = book.on_trade(trade)
        after = book.order(ticker, outcome)
        if through:
            eligible += feebook.as_decimal(trade.get('size'), 'size')
        if before_ahead is not None and after is not None:
            adverse += before_ahead - after.queue_ahead
        for fill in produced:
            if fill.fee_quote['formula_id'] != feebook.EXAMINER_FORMULA_ID:
                raise QueueFragilityError('examiner formula')
            if fill.fee_quote['rounded_up'] is not False:
                raise QueueFragilityError('fill round_up')
            filled += fill.size
            fills.append({
                'size': fill.size,
                'formula_id': fill.fee_quote['formula_id'],
                'rate': fill.fee_quote['rate'],
                'rounded_up': fill.fee_quote['rounded_up'],
                'fee': fill.fee_quote['fee'],
            })
    return {
        'arm': arm,
        'queue_params': arm_queue_params(arm),
        'filled': filled,
        'requested': requested,
        'fill_rate': filled / requested,
        'adverse_queue_exposure': adverse,
        'eligible_volume': eligible,
        'fills': tuple(fills),
        'results': None,
        'pnl': None,
    }


def empty_pre_settlement():
    """The three outputs and profit fields before a fixture join."""
    return {
        'fill_rate_delta_vs_q3300': None,
        'adverse_queue_exposure': None,
        'participation_stress_gap': None,
        'results': None,
        'pnl': None,
        'status': NOT_RUN,
    }


def pre_settlement_outputs(intents=None, trades=None, *, joined=False):
    """Cohort queue statistics. Null unless the caller marks a fixture join.

    A joined return is still not profit: results and pnl stay null. This
    function does not read or write the freeze file.
    """
    if not joined or not intents or not trades:
        return empty_pre_settlement()
    measured = {arm: measure_arm(arm, intents, trades) for arm in ARMS}
    base = measured[QF0]['fill_rate']
    deltas = {
        QF1: measured[QF1]['fill_rate'] - base,
        QF2: measured[QF2]['fill_rate'] - base,
    }
    exposure = {arm: measured[arm]['adverse_queue_exposure'] for arm in ARMS}
    eligible = measured[QF1]['eligible_volume']
    if eligible == 0:
        gap = None
    else:
        realized = measured[QF1]['filled'] / eligible
        gap = rails.FILL_PARTICIPATION_DEFAULT - realized
    fee = feebook_binding()
    for arm in ARMS:
        for fill in measured[arm]['fills']:
            if fill['formula_id'] != fee['formula_id'] or fill['rate'] != fee['maker_rate']:
                raise QueueFragilityError('feebook binding')
    return {
        'fill_rate_delta_vs_q3300': deltas,
        'adverse_queue_exposure': exposure,
        'participation_stress_gap': gap,
        'results': None,
        'pnl': None,
        'status': SYNTHETIC_FIXTURE_ONLY,
    }


def historical_completed_net():
    """The 31-game completed net is not computed in this lab."""
    raise QueueFragilityError('Q6-000 historical completed net is not computed here')


def frozen_output_snapshot():
    """Read the freeze file. Does not modify it."""
    payload = json.loads(FROZEN_EXPERIMENT.read_text())
    snapshot = {
        'results': payload['results'],
        'pnl': payload['pnl'],
    }
    for key in OUTPUT_KEYS:
        snapshot[key] = payload[key]
    return snapshot
