"""R2-P1 hygiene labels for Q6-000.

Examiner fees come from kalshi_feebook_lab_20260922. Queue bins, maker-credit
admission, and content freshness come from kalshi_rails_lab_20260922. The
inherited fee is the Q6 fixed-point balance charge, reimplemented here so this
module does not import the factorial replay. This module does not place live
orders and does not record a walk P&L.
"""
import hashlib
import json
import sys
from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR
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

EXPERIMENT_ID = 'r2p1_hygiene_000_20260922'
STRATEGY_POINTER = 'Q6-000'
CANONICAL_FREEZE = 'R2-P1_FEEBOOK_RAILS_HYGIENE_000_FREEZE_2026-09-22.md'
CANONICAL_FREEZE_SHA256_PREFIX = 'ddcd4427'
FEE_SENSITIVITY_STATUS = 'SUPERSEDED_BY_R2-P1'
FEEBOOK_COMMIT = '22371178cb2663250b4762f328069571c48cb551'
RAILS_COMMIT = '6a28e0d6254327ea4e6451c781bec56215ac6cac'
INHERITED_MODEL_ID = 'q6.order_fees.fixed_point_balance.v1'
ASSUMED_SCENARIOS = ('q3300', 'q10000')
OUTSIDE_BIN = 'outside_pinned_bins'
PRIMARY_ASSUMED_SCENARIO = 'q3300'
OTHER_ASSUMED_SCENARIO = 'q10000'
OUTPUT_KEYS = (
    'fee_delta_vs_inherited_model',
    'freshness_gap_sec',
    'queue_bin_mismatch_rate',
)
NOT_JOINED = 'NOT_JOINED'
SYNTHETIC_FIXTURE_ONLY = 'SYNTHETIC_FIXTURE_ONLY'
QUEUE_FRAGILITY_SIBLING = 'kalshi_queue_fragility_000_lab_20260922'
MICRO_CENT = Decimal('0.000001')
BALANCE_PRECISION = Decimal('0.0001')
PRICE_GRID = Decimal('0.0001')
CONTRACT_GRID = Decimal('0.01')
GRID_TOLERANCE = Decimal('0.00000001')

FACTORIAL_INPUTS = PARENT / 'nfl_factorial_lab_20260921' / 'inputs'
WEEK_MEMBERSHIP = FACTORIAL_INPUTS / 'week_membership.json'
TAPE_MANIFEST = FACTORIAL_INPUTS / 'manifest.json'
SHADOW_FREEZE = PARENT / 'nfl_factorial_lab_20260921' / 'SHADOW_CANDIDATE_FREEZE.json'
FROZEN_EXPERIMENT = ROOT / 'FROZEN_EXPERIMENT.json'
EMPTY_RESULTS = ROOT / 'results' / 'EMPTY_RESULTS.json'


class HygieneError(Exception):
    """A hygiene label was refused or a completed net was requested."""


class LiveOrdersForbidden(HygieneError):
    """This lab has no live order path."""

    def __init__(self):
        super().__init__('no live orders and no KalshiExecutionAdapter')


class InheritedCoefficientRefused(HygieneError):
    """The inherited coefficient is not the feebook rate for this quote."""

    def __init__(self):
        super().__init__('inherited coefficient must equal the feebook rate')


def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def development_cohort_event_ids():
    """Sorted event ids from the Q6 development membership file. Read only."""
    payload = json.loads(WEEK_MEMBERSHIP.read_text())
    if not isinstance(payload, dict):
        raise HygieneError('week membership')
    event_ids = tuple(sorted(payload.keys()))
    if len(event_ids) != 31:
        raise HygieneError('N_events')
    return event_ids


def pin_lock():
    """Conductor pin. The canonical freeze file is cited, not substituted."""
    return {
        'canonical_freeze': CANONICAL_FREEZE,
        'canonical_freeze_sha256_prefix': CANONICAL_FREEZE_SHA256_PREFIX,
        'canonical_freeze_bytes': 'not_in_checkout',
        'fee_sensitivity_000_r1p1': FEE_SENSITIVITY_STATUS,
        'second_lab': False,
        'fee_treatment_arms_emitted': False,
        'queue_fragility_twin': False,
        'queue_fragility_sibling': QUEUE_FRAGILITY_SIBLING,
        'live_orders': False,
        'scorecard': empty_pre_settlement(),
    }


def instrument_binding():
    """Rates and queue magnitudes from the imported labs only."""
    table = feebook.load_series_table()
    rates = table['rates']
    return {
        'experiment_id': EXPERIMENT_ID,
        'strategy_pointer': STRATEGY_POINTER,
        'feebook_commit': FEEBOOK_COMMIT,
        'rails_commit': RAILS_COMMIT,
        'examiner_formula_id': feebook.EXAMINER_FORMULA_ID,
        'comparator_formula_id': feebook.GROK_COMPARATOR_FORMULA_ID,
        'fee_credit_rule_id': rails.FEE_CREDIT_RULE_ID,
        'inherited_model_id': INHERITED_MODEL_ID,
        'maker_rate': feebook.as_decimal(rates['maker'], 'maker'),
        'taker_rate': feebook.as_decimal(rates['taker'], 'taker'),
        'primary_queue_ahead': rails.scenario_queue(PRIMARY_ASSUMED_SCENARIO),
        'stress_queue_ahead': rails.scenario_queue(OTHER_ASSUMED_SCENARIO),
        'queue_is_knob': False,
        'capital_arms_reopened': False,
        'signal_retune': False,
        'live_orders': False,
        'queue_fragility_twin': False,
    }


def execution_adapter():
    """No live order client lives in this lab."""
    raise LiveOrdersForbidden()


class InheritedFeeState:
    """Per-order accumulator for the inherited fixed-point charge."""

    def __init__(self, precision=BALANCE_PRECISION):
        self.precision = feebook.as_decimal(precision, 'precision')
        if self.precision <= 0:
            raise ValueError('precision')
        self.accumulator = Decimal('0')


def inherited_order_fee(price, contracts, coefficient, state=None):
    """Q6 fixed-point fee. Decimal in and Decimal out. Not the examiner channel.

    Nominal fee is ceiled to 0.000001. Cash is floored to the balance
    precision. A rebate draws down the per-order accumulator. A missing state
    starts that accumulator at zero.
    """
    if state is None:
        state = InheritedFeeState()
    if not isinstance(state, InheritedFeeState):
        raise TypeError('state')
    price = feebook.as_decimal(price, 'price')
    contracts = feebook.as_decimal(contracts, 'contracts')
    coefficient = feebook.as_decimal(coefficient, 'coefficient')
    if coefficient < 0:
        raise ValueError('coefficient')
    p = price.quantize(PRICE_GRID)
    q = contracts.quantize(CONTRACT_GRID)
    if abs(p - price) > GRID_TOLERANCE or abs(q - contracts) > GRID_TOLERANCE:
        raise ValueError('price/contracts outside the inherited fixed-point grid')
    if q <= 0:
        raise ValueError('contracts')
    if p < 0 or p > 1:
        raise ValueError('price')
    revenue = -p * q
    nominal = (coefficient * q * p * (feebook.ONE - p)).quantize(MICRO_CENT, rounding=ROUND_CEILING)
    aligned = ((revenue - nominal) / state.precision).to_integral_value(rounding=ROUND_FLOOR) * state.precision
    rounding = revenue - nominal - aligned
    state.accumulator += rounding
    available = (state.accumulator / state.precision).to_integral_value(rounding=ROUND_FLOOR) * state.precision
    cap = ((nominal + rounding) / state.precision).to_integral_value(rounding=ROUND_FLOOR) * state.precision
    rebate = min(available, cap)
    state.accumulator -= rebate
    fee = nominal + rounding - rebate
    return {
        'model_id': INHERITED_MODEL_ID,
        'fee': fee,
        'nominal': nominal,
        'rebate': rebate,
        'accumulator': state.accumulator,
    }


def fee_delta(role, contracts, price, coefficient, round_up=True, series=None, table=None, state=None):
    """Examiner fee minus the inherited fee. Same resolved rate on both sides.

    round_up follows the feebook pin: true is the order-level cent ceiling,
    false leaves the raw product for a partial. The Grok comparator is not read.
    """
    if role not in ('maker', 'taker'):
        raise ValueError('role')
    if table is None:
        table = feebook.load_series_table()
    quote = feebook.order_fee(
        role, contracts, price, round_up=round_up, series=series, table=table,
    )
    if quote['formula_id'] != feebook.EXAMINER_FORMULA_ID:
        raise HygieneError('examiner formula')
    supplied = feebook.as_decimal(coefficient, 'coefficient')
    if supplied != quote['rate']:
        raise InheritedCoefficientRefused()
    inherited = inherited_order_fee(price, contracts, supplied, state=state)
    return {
        'role': role,
        'examiner_fee': quote['fee'],
        'examiner_raw': quote['raw'],
        'examiner_formula_id': quote['formula_id'],
        'inherited_fee': inherited['fee'],
        'inherited_model_id': inherited['model_id'],
        'fee_delta': quote['fee'] - inherited['fee'],
        'round_up': quote['rounded_up'],
        'rate': quote['rate'],
    }


def maker_credit_floor_zero_refuse(price, contracts, series=None, table=None):
    """True when the R1-P5 floored maker credit is zero or negative."""
    try:
        evaluation = rails.admit_maker_quote(price, contracts, series=series, table=table)
        refused = False
    except rails.MakerCreditRefused as exc:
        evaluation = exc.evaluation
        refused = True
    if evaluation['rule_id'] != rails.FEE_CREDIT_RULE_ID:
        raise HygieneError('fee credit rule')
    if evaluation['fee_quote']['formula_id'] != feebook.EXAMINER_FORMULA_ID:
        raise HygieneError('examiner formula')
    return {
        'maker_credit_floor_zero_refuse': refused,
        'credit': evaluation['credit'],
        'admitted': evaluation['admitted'],
        'rule_id': rails.FEE_CREDIT_RULE_ID,
        'fee': evaluation['fee'],
        'formula_id': evaluation['fee_quote']['formula_id'],
    }


def content_fresh_flag(previous, current, *, keepalive=False):
    """R1-P5 freshness. A keepalive is never a fresh book."""
    verdict = rails.judge_freshness(previous, current, keepalive=keepalive)
    return {
        'content_fresh_flag': verdict.fresh,
        'reason': verdict.reason,
    }


def freshness_gap_seconds(observed_at, prior_fresh_at):
    """Seconds from the last content-fresh observation to this one.

    A missing anchor returns null. The caller decides whether a keepalive
    moved the anchor. This function only subtracts.
    """
    if observed_at is None or prior_fresh_at is None:
        return None
    observed = feebook.as_decimal(observed_at, 'observed_at')
    prior = feebook.as_decimal(prior_fresh_at, 'prior_fresh_at')
    gap = observed - prior
    if gap < 0:
        raise ValueError('freshness gap')
    return gap


class FreshnessCursor:
    """Tracks the last fresh book. A keepalive does not move the anchor."""

    def __init__(self):
        self.previous = None
        self.prior_fresh_at = None

    def observe(self, current, observed_at, *, keepalive=False):
        flag = content_fresh_flag(self.previous, current, keepalive=keepalive)
        gap = freshness_gap_seconds(observed_at, self.prior_fresh_at)
        if flag['content_fresh_flag']:
            self.prior_fresh_at = feebook.as_decimal(observed_at, 'observed_at')
            if not isinstance(current, rails.BookObservation):
                raise TypeError('current')
            self.previous = current
        return {
            'content_fresh_flag': flag['content_fresh_flag'],
            'reason': flag['reason'],
            'freshness_gap_sec': gap,
            'prior_fresh_at': self.prior_fresh_at,
        }


def queue_attribution_bin(queue_ahead):
    """Exact match to a pinned rails scenario. Other sizes stay outside."""
    ahead = feebook.as_decimal(queue_ahead, 'queue_ahead')
    if ahead < 0:
        raise ValueError('queue_ahead')
    for label in ASSUMED_SCENARIOS:
        if ahead == rails.scenario_queue(label):
            return label
    return OUTSIDE_BIN


def queue_bin_mismatch(queue_ahead, assumed_scenario):
    """Mismatch when the attributed bin is not the row's assumed scenario."""
    if assumed_scenario not in ASSUMED_SCENARIOS:
        raise ValueError('assumed_scenario')
    attributed = queue_attribution_bin(queue_ahead)
    measured = feebook.as_decimal(queue_ahead, 'queue_ahead')
    return {
        'queue_attribution_bin': attributed,
        'assumed_scenario': assumed_scenario,
        'queue_bin_mismatch': attributed != assumed_scenario,
        'measured_ahead': measured,
        'assumed_ahead': rails.scenario_queue(assumed_scenario),
    }


def label_fill(*, role, contracts, price, coefficient, assumed_scenario, queue_ahead,
               round_up=True, series=None, table=None, state=None,
               previous_book=None, current_book=None, keepalive=False,
               observed_at=None, prior_fresh_at=None):
    """One pre-settlement label. The row carries no completed net."""
    delta = fee_delta(
        role, contracts, price, coefficient, round_up=round_up,
        series=series, table=table, state=state,
    )
    credit = None
    if role == 'maker':
        credit = maker_credit_floor_zero_refuse(price, contracts, series=series, table=table)
    fresh = None
    if current_book is not None or keepalive:
        fresh = content_fresh_flag(previous_book, current_book, keepalive=keepalive)
    queue = queue_bin_mismatch(queue_ahead, assumed_scenario)
    return {
        'role': role,
        'fee_delta': delta['fee_delta'],
        'examiner_fee': delta['examiner_fee'],
        'inherited_fee': delta['inherited_fee'],
        'examiner_formula_id': delta['examiner_formula_id'],
        'inherited_model_id': delta['inherited_model_id'],
        'round_up': delta['round_up'],
        'maker_credit_floor_zero_refuse': None if credit is None else credit['maker_credit_floor_zero_refuse'],
        'content_fresh_flag': None if fresh is None else fresh['content_fresh_flag'],
        'freshness_reason': None if fresh is None else fresh['reason'],
        'freshness_gap_sec': freshness_gap_seconds(observed_at, prior_fresh_at),
        'queue_attribution_bin': queue['queue_attribution_bin'],
        'assumed_scenario': queue['assumed_scenario'],
        'queue_bin_mismatch': queue['queue_bin_mismatch'],
        'pnl': None,
    }


def empty_pre_settlement():
    """The three outputs and profit fields before a fixture join."""
    return {
        'fee_delta_vs_inherited_model': None,
        'freshness_gap_sec': None,
        'queue_bin_mismatch_rate': None,
        'results': None,
        'pnl': None,
        'status': NOT_JOINED,
    }


def pre_settlement_outputs(labeled_rows=None, *, joined=False):
    """Cohort hygiene statistics. Null unless the caller marks a fixture join.

    A joined return is still not profit: results and pnl stay null. This
    function does not read or write the freeze file.
    """
    if not joined or not labeled_rows:
        return empty_pre_settlement()
    fee_sum = Decimal('0')
    gaps = []
    mismatches = 0
    for row in labeled_rows:
        fee_sum += row['fee_delta']
        gap = row.get('freshness_gap_sec')
        if gap is not None:
            gaps.append(gap)
        if row['queue_bin_mismatch']:
            mismatches += 1
    count = len(labeled_rows)
    return {
        'fee_delta_vs_inherited_model': fee_sum,
        'freshness_gap_sec': None if not gaps else max(gaps),
        'queue_bin_mismatch_rate': Decimal(mismatches) / Decimal(count),
        'results': None,
        'pnl': None,
        'status': SYNTHETIC_FIXTURE_ONLY,
    }


def historical_completed_net():
    """The 31-game completed net is not computed in this lab."""
    raise HygieneError('Q6-000 historical completed net is not computed here')


def classify_rescore(scorecard):
    """Forward to the examiner gate. The label is not stored as profit."""
    return feebook.classify_scorecard(scorecard)


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
