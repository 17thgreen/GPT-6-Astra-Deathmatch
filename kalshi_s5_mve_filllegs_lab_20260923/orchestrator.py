"""S5 KXMVECROSSCATEGORY fill versus independent-leg product.

Measurement only. Imports the R1-P1 feebook and the R1-P5 rails. The combo
series override is applied in memory. This module does not edit those labs,
does not open RFQ, does not read Logan keys, does not run admit.py, and does
not write scorecard metrics.
"""
import hashlib
import importlib.util
import json
import sys
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

LAB_DIRECTORY = 'kalshi_s5_mve_filllegs_lab_20260923'
EXPERIMENT_ID = 'S5-KXMVECROSSCATEGORY-FILLLEGS-HARNESS'
PANEL_PACKET_ID = 'S5-KXMVECROSSCATEGORY-MEAS'
SERIES = 'KXMVECROSSCATEGORY'
PANEL_VERSION = '2026-09-22.s5-kxmvecrosscategory-v0'
SCHEMA_ID = 'astra.registry.s5_kxmvecrosscategory_panel.v0'
KNOB = 'leg_mid_source'
S5L0 = 'S5L0'
S5L1 = 'S5L1'
ARMS = (S5L0, S5L1)
LEG_MID_SOURCE = {
    S5L0: 'tob_1m',
    S5L1: 'synthetic_leg_product',
}
FEE_TYPE_OVERRIDE = 'quadratic_with_combo_maker_fees'
BOUND_SERIES = (
    'KXMVECROSSCATEGORY',
    'KXMVECROSSCATEGORY-SHARD1',
    'KXMVESPORTSMULTIGAMEEXTENDED',
)
PREFER_OVER = (
    'KXMVENFLSINGLEGAME',
    'KXMVENFLMULTIGAME',
    'KXMVENFLEXTENDED',
)
FEEBOOK_COMMIT = '22371178cb2663250b4762f328069571c48cb551'
RAILS_COMMIT = '6a28e0d6254327ea4e6451c781bec56215ac6cac'
UNTOUCHED_BASE = '79347f0ed8562f7df8d539e79a1cb15985d8abfe'
PACKET_SHA256 = '8a118e6f1fdc8c22c6e559f395667aedffa5d270d067e39b6ae3ee24b2046d16'
KERNEL_SHA256 = 'a28932ba13b4913b69c48b73dde8ba066cebd212670d0b1cbb5ea8e93734b8ba'
PANEL_STUB_SHA256 = '4918b820d454c5f997ea100917859f7e9467d92933bed1bc8a55c81ab8ce5b8e'
PUBLIC_HOST = 'api.elections.kalshi.com'
STUB_MARKETS_N = 5
STUB_EVENTS_N = 21
STUB_LEGS_JOIN = '5/5'
SCORECARD_FIELDS = (
    'fill_vs_legs_mid_gap',
    'combo_fee_delta_vs_feebook',
    'legs_join_rate',
    'freshness_gap_sec',
)
OUTPUT_KEYS = SCORECARD_FIELDS + ('results', 'pnl')
ADVERSARY_LABELS = {
    'rfq': 'RFQ communications are out of scope',
    'communications': 'RFQ communications are out of scope',
    'r1p4_strategy': 'R1-P4 strategy open is refused',
    'r1_p4_strategy': 'R1-P4 strategy open is refused',
    'logan_keys': 'Logan keys are refused',
    'logan_key': 'Logan keys are refused',
    'invented_fill': 'invented fills are refused',
    'invented_pnl': 'invented pnl is refused',
    'kxmvnfl': 'empty KXMVENFL preference is refused',
    'admit_py': 'admit.py is not run in this harness',
    'live_order': 'live orders are refused',
    'fee_blind_completed_profit': 'fee-blind completed profit is refused',
    'completed_profit': 'fee-blind completed profit is refused',
}
DEAD_CARDS = (
    'Cap-SR',
    'Cap-SR-FX',
    'S1_empty_events',
    'S2_R2-P4_WAIT',
    'R3-P2_HOLD',
    'QF_reopen_DENIED',
    'RFQ_401',
    'KXMVENFL_empty',
    'C1_empty_book',
    'Q7_Arm_B',
)
QUEUED_BEHIND = (
    'S4_NCAAF',
    'R2-P3_prop_slate',
)
DOES_NOT_MODIFY = (
    'kalshi_feebook_lab_20260922',
    'kalshi_rails_lab_20260922',
    'kalshi_capital_structure_lab_20260922',
    'kalshi_soft_blended_reserves_000_lab_20260923',
    'kalshi_cap_sr_effects_000_lab_20260923',
    'kalshi_queue_fragility_000_lab_20260922',
    'kalshi_c3_kxhighny_bordering_lab_20260923',
    'kalshi_c5_kxbtc15m_honesty_lab_20260923',
    'kalshi_r3p3_fl_maker_taker_lab_20260923',
    'kalshi_r2p1_hygiene_000_lab_20260922',
    'kalshi_examiner_fee_queue_honesty_000_lab_20260922',
    'nfl_queue_lab_20260921',
    'nfl_completion_lab_20260921',
    'nfl_measurement_lab_20260921',
    'nfl_timing_lab_20260921',
    'nfl_adaptive_lab_20260921',
    'nfl_factorial_lab_20260921',
    'nfl_paircheck_lab_20260922',
)
PACKET_NAME = 'S5_KXMVECROSSCATEGORY_FILLLEGS_HARNESS_FREEZE_2026-09-23.md'
KERNEL_NAME = 'S5_KXMVECROSSCATEGORY_MEASUREMENT_FREEZE_KERNEL_2026-09-22.md'
PACKET = ROOT / PACKET_NAME
KERNEL = ROOT / KERNEL_NAME
LAB_BUNDLE = ROOT / 'S5_KXMVECROSSCATEGORY_FILLLEGS_HARNESS'
GOVERNANCE_BUNDLE = PARENT / 'packets' / 'S5_KXMVECROSSCATEGORY_FILLLEGS_HARNESS'
GOVERNANCE_TREE = PARENT / 'lab' / 'governance' / 'astra' / 'packets'
FROZEN_EXPERIMENT = ROOT / 'FROZEN_EXPERIMENT.json'
EMPTY_RESULTS = ROOT / 'results' / 'EMPTY_RESULTS.json'
PANEL_STUB = PARENT / 'lab' / 'astra-capture' / 's5-kxmvecrosscategory' / 'panel_stub.json'
PANEL_ADMITTED = PARENT / 'lab' / 'astra-capture' / 's5-kxmvecrosscategory' / 'panel_admitted.json'
SYNTHETIC_PRODUCT = ROOT / 'fixtures' / 'synthetic_leg_product.json'
HYGIENE_PATH = PARENT / 'kalshi_r2p1_hygiene_000_lab_20260922' / 'hygiene.py'
INVENTORY_KEYS = ('volume_fp', 'volume_24h_fp', 'open_interest_fp')
SYNTHETIC_PRINT_LABEL = 'synthetic_print_schema_only'


class OrchestratorError(Exception):
    """A pin failed or a measurement write was requested."""


class ScorecardPromotionRefused(OrchestratorError):
    """Filled measurement fields stay out of the freeze packet."""

    def __init__(self):
        super().__init__('scorecard metrics stay null until Examiner')


class LiveOrdersForbidden(OrchestratorError):
    """This lab has no live order path."""

    def __init__(self):
        super().__init__('no live orders and no KalshiExecutionAdapter')


class AdversaryRefused(OrchestratorError):
    """RFQ, an R1-P4 strategy, a Logan key, or an invented fill was requested."""

    def __init__(self, label):
        self.label = label
        super().__init__(label)


class RfqRefused(OrchestratorError):
    """RFQ /communications stays out of scope."""

    def __init__(self):
        super().__init__(ADVERSARY_LABELS['rfq'])


class PanelVersionRefused(OrchestratorError):
    """The panel file is not the pinned S5 seed."""

    def __init__(self):
        super().__init__('panel_version')


class ShadowFeeLiteralRefused(OrchestratorError):
    """A fee quote bypassed the examiner feebook formula or the combo override."""

    def __init__(self):
        super().__init__('shadow fee literal')


class InventedFillRefused(OrchestratorError):
    """A fill was supplied on an empty tape or labeled as invented."""

    def __init__(self):
        super().__init__(ADVERSARY_LABELS['invented_fill'])


class InventedInventoryRefused(OrchestratorError):
    """Volume or open interest was filled without Examiner."""

    def __init__(self):
        super().__init__('invented open interest')


class MissingLegRefused(OrchestratorError):
    """A combo market is missing a selected leg or a leg mid."""

    def __init__(self):
        super().__init__('missing leg')


class StaleLegRefused(OrchestratorError):
    """Rails did not call this leg book content-fresh."""

    def __init__(self, reason='stale leg'):
        super().__init__(reason)
        self.reason = reason


class AdmitPyRefused(OrchestratorError):
    """admit.py is not run from this harness."""

    def __init__(self):
        super().__init__(ADVERSARY_LABELS['admit_py'])


class UnknownLegMidSource(OrchestratorError):
    """The only knob is tob_1m or synthetic_leg_product."""

    def __init__(self):
        super().__init__('leg_mid_source')


class SyntheticArmRefused(OrchestratorError):
    """The known-product fixture belongs to S5L1."""

    def __init__(self):
        super().__init__('synthetic_leg_product')


def _load_module(module_name, path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise OrchestratorError('sibling import')
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


hygiene = _load_module('s5_hygiene_labels', HYGIENE_PATH)


def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def execution_adapter():
    """No live order client lives in this lab."""
    raise LiveOrdersForbidden()


def assert_public_get(method):
    """GET is the only public capture verb. This function does not open a socket."""
    if method != 'GET':
        raise LiveOrdersForbidden()
    return None


def assert_route(route):
    """Allowlisted public GETs. RFQ communications and portfolio routes raise."""
    if not isinstance(route, str) or route == '':
        raise LiveOrdersForbidden()
    lowered = route.lower()
    if 'communications' in lowered or 'rfq' in lowered:
        raise RfqRefused()
    if not route.startswith('GET '):
        raise LiveOrdersForbidden()
    if '/portfolio' in lowered or '/orders' in lowered:
        raise LiveOrdersForbidden()
    return None


def refuse_adversary(label):
    """Named adversary labels. Nothing is traded and no fill is invented."""
    if label not in ADVERSARY_LABELS:
        raise OrchestratorError('adversary label')
    raise AdversaryRefused(ADVERSARY_LABELS[label])


def assert_examiner_quote(quote):
    """Accept only the R1-P1 examiner formula."""
    if not isinstance(quote, dict):
        raise ShadowFeeLiteralRefused()
    formula = quote.get('formula_id')
    if formula != feebook.EXAMINER_FORMULA_ID:
        raise ShadowFeeLiteralRefused()
    if formula in (feebook.GROK_COMPARATOR_FORMULA_ID, hygiene.INHERITED_MODEL_ID):
        raise ShadowFeeLiteralRefused()
    return quote


def assert_combo_override_quote(quote):
    """The bound combo series must resolve through the in-memory override."""
    assert_examiner_quote(quote)
    if quote.get('series_resolution') != 'override':
        raise ShadowFeeLiteralRefused()
    if quote.get('M') != feebook.ONE:
        raise OrchestratorError('multiplier')
    return quote


def leg_probability(mid, side):
    """YES keeps the mid. NO flips to 1 - mid."""
    mid = feebook.as_decimal(mid, 'mid')
    if mid < 0 or mid > feebook.ONE:
        raise ValueError('mid')
    if side == 'yes':
        return mid
    if side == 'no':
        return feebook.ONE - mid
    raise ValueError('side')


def independent_leg_product(legs):
    """Product of independent-leg probabilities. Missing or stale legs raise."""
    if not isinstance(legs, list) or len(legs) == 0:
        raise MissingLegRefused()
    product = feebook.ONE
    for leg in legs:
        if not isinstance(leg, dict) or leg.get('mid') is None:
            raise MissingLegRefused()
        if leg.get('content_fresh') is not True:
            raise StaleLegRefused()
        product *= leg_probability(leg['mid'], leg.get('side'))
    return product


def tob_yes_mid(orderbook):
    """YES mid from a bids-only TOB. A missing side stays unset."""
    book = feebook.reciprocal_book(orderbook)
    if book['bid_yes'] is None or book['ask_yes'] is None:
        raise feebook.BookIncomplete('missing bid')
    return (book['bid_yes'] + book['ask_yes']) / 2


def leg_row_from_book(orderbook, side, previous, current):
    """One TOB leg after the rails freshness gate. The scorecard is not written."""
    if side not in ('yes', 'no'):
        raise ValueError('side')
    verdict = rails.judge_freshness(previous, current)
    if not verdict.fresh:
        raise StaleLegRefused(verdict.reason)
    return {
        'side': side,
        'mid': tob_yes_mid(orderbook),
        'content_fresh': True,
        'freshness_reason': verdict.reason,
    }


def legs_complete(market):
    """True when mve_selected_legs matches legs_n and every leg has a side."""
    legs = market.get('mve_selected_legs')
    if not isinstance(legs, list) or len(legs) == 0:
        return False
    if market.get('legs_n') != len(legs):
        return False
    for leg in legs:
        if not isinstance(leg, dict):
            return False
        event_ticker = leg.get('event_ticker')
        market_ticker = leg.get('market_ticker')
        if not isinstance(event_ticker, str) or event_ticker == '':
            return False
        if not isinstance(market_ticker, str) or market_ticker == '':
            return False
        if leg.get('side') not in ('yes', 'no'):
            return False
    return True


def assert_tape_honesty(row):
    """An empty tape cannot carry a fill price. Invent flags raise."""
    if not isinstance(row, dict):
        raise InventedFillRefused()
    if row.get('invent_fill') is True:
        raise InventedFillRefused()
    filled = row.get('fill_price') is not None or row.get('print_price') is not None
    trades = row.get('trades')
    trades_n = row.get('trades_n', 0)
    empty = trades in (None, []) and trades_n in (0, None)
    if filled and empty:
        raise InventedFillRefused()
    return None


def empty_tape(panel):
    """True when every recorded trade probe is empty. Missing probes stay empty."""
    probe = (panel.get('resolve_notes') or {}).get('trades_probe') or []
    return all(row.get('trades_n') in (0, None) for row in probe)


def _require_null(payload, key):
    if key not in payload or payload[key] is not None:
        raise InventedInventoryRefused()


def _assert_freeze_bytes():
    copies = (
        PACKET,
        LAB_BUNDLE / PACKET_NAME,
        PARENT / 'packets' / PACKET_NAME,
        GOVERNANCE_BUNDLE / PACKET_NAME,
    )
    for path in copies:
        if sha256_file(path) != PACKET_SHA256:
            raise OrchestratorError('packet sha256')
    kernels = (
        KERNEL,
        LAB_BUNDLE / KERNEL_NAME,
        PARENT / 'packets' / KERNEL_NAME,
        GOVERNANCE_BUNDLE / KERNEL_NAME,
    )
    for path in kernels:
        if sha256_file(path) != KERNEL_SHA256:
            raise OrchestratorError('kernel sha256')
    if sha256_file(PANEL_STUB) != PANEL_STUB_SHA256:
        raise OrchestratorError('stub sha256')


def select_panel_path(stub_path=None, admitted_path=None):
    """Prefer panel_admitted.json when the file exists. Otherwise the stub."""
    stub_path = PANEL_STUB if stub_path is None else Path(stub_path)
    admitted_path = PANEL_ADMITTED if admitted_path is None else Path(admitted_path)
    if Path(admitted_path).is_file():
        return Path(admitted_path)
    if not Path(stub_path).is_file():
        raise OrchestratorError('panel stub')
    return Path(stub_path)


def _validate_series_row(row):
    series = row.get('series_ticker')
    if series not in BOUND_SERIES:
        raise OrchestratorError('series')
    for blocked in PREFER_OVER:
        if series == blocked or (isinstance(series, str) and series.startswith('KXMVENFL')):
            raise AdversaryRefused(ADVERSARY_LABELS['kxmvnfl'])
    if row.get('panel_version') != PANEL_VERSION:
        raise PanelVersionRefused()


def _validate_panel(payload, admitted):
    if not isinstance(payload, dict):
        raise OrchestratorError('panel')
    if payload.get('schema_id') != SCHEMA_ID:
        raise OrchestratorError('schema')
    if payload.get('panel_version') != PANEL_VERSION:
        raise PanelVersionRefused()
    if payload.get('packet_id') != PANEL_PACKET_ID:
        raise OrchestratorError('packet')
    if payload.get('series_ticker') != SERIES:
        raise OrchestratorError('series')
    prefer = payload.get('prefer_over') or []
    for series in PREFER_OVER:
        if series not in prefer:
            raise OrchestratorError('prefer_over')
    stamp = payload.get('admitted_at')
    if admitted:
        if not isinstance(stamp, str) or not stamp.endswith('Z'):
            raise OrchestratorError('admitted_at')
    elif stamp is not None:
        raise OrchestratorError('admitted_at')
    for key in ('results', 'pnl', 'volume'):
        _require_null(payload, key)
    gate = payload.get('admit_gate') or {}
    if gate.get('admit_py_run') is not False:
        raise AdmitPyRefused()
    if gate.get('not_r1_p4_strategy') is not True:
        raise AdversaryRefused(ADVERSARY_LABELS['r1p4_strategy'])
    binds = payload.get('binds') or {}
    if binds.get('fee_lab_sha') != FEEBOOK_COMMIT:
        raise OrchestratorError('feebook commit')
    if binds.get('rails_lab_sha') != RAILS_COMMIT:
        raise OrchestratorError('rails commit')
    if binds.get('fee_formula_id') != feebook.EXAMINER_FORMULA_ID:
        raise OrchestratorError('examiner formula')
    if binds.get('fee_type_series_override') != FEE_TYPE_OVERRIDE:
        raise OrchestratorError('fee type')
    if binds.get('forbid_inherited_q7_fee_literals') is not True:
        raise ShadowFeeLiteralRefused()
    if binds.get('not_r1_p4_strategy') is not True:
        raise AdversaryRefused(ADVERSARY_LABELS['r1p4_strategy'])
    if binds.get('logan_keys_required') is True:
        raise AdversaryRefused(ADVERSARY_LABELS['logan_keys'])
    confirmed = binds.get('fee_confirmed_live_get') or {}
    for series in BOUND_SERIES:
        row = confirmed.get(series) or {}
        if row.get('fee_type') != FEE_TYPE_OVERRIDE:
            raise OrchestratorError('fee type')
        if row.get('fee_multiplier') != 1:
            raise OrchestratorError('multiplier')
    capture = payload.get('capture') or {}
    if capture.get('mode') != 'GET_only_public':
        raise LiveOrdersForbidden()
    if capture.get('host_allowlist') != [PUBLIC_HOST]:
        raise LiveOrdersForbidden()
    routes = capture.get('routes_allowlist') or []
    if not routes:
        raise LiveOrdersForbidden()
    for route in routes:
        assert_route(route)
    out_of_scope = capture.get('out_of_scope_routes') or []
    if not any('communications' in route for route in out_of_scope):
        raise RfqRefused()
    schedule = capture.get('schedule') or {}
    if schedule.get('recorder_started') is True:
        raise OrchestratorError('recorder')
    events = payload.get('events') or []
    markets = payload.get('markets') or []
    summary = payload.get('cohort_summary') or {}
    if admitted:
        if len(markets) < 1 or len(events) < 1:
            raise OrchestratorError('cohort')
    else:
        if len(markets) != STUB_MARKETS_N or len(events) != STUB_EVENTS_N:
            raise OrchestratorError('cohort')
        if summary.get('markets_seed_n') != STUB_MARKETS_N:
            raise OrchestratorError('cohort')
        if summary.get('events_seed_n') != STUB_EVENTS_N:
            raise OrchestratorError('cohort')
        if summary.get('legs_join_rate') != STUB_LEGS_JOIN:
            raise OrchestratorError('legs join')
        probe = (payload.get('resolve_notes') or {}).get('trades_probe') or []
        if not probe or any(row.get('trades_n') not in (0, None) for row in probe):
            raise InventedFillRefused()
    for event in events:
        _validate_series_row(event)
        event_stamp = event.get('admitted_at')
        if admitted:
            if event_stamp not in (None, stamp):
                raise OrchestratorError('admitted_at')
        elif event_stamp is not None:
            raise OrchestratorError('admitted_at')
        for key in INVENTORY_KEYS:
            _require_null(event, key)
    complete = 0
    for market in markets:
        _validate_series_row(market)
        market_stamp = market.get('admitted_at')
        if admitted:
            if market_stamp not in (None, stamp):
                raise OrchestratorError('admitted_at')
        elif market_stamp is not None:
            raise OrchestratorError('admitted_at')
        if market.get('result') is not None:
            raise InventedInventoryRefused()
        for key in INVENTORY_KEYS:
            _require_null(market, key)
        if market.get('content_fresh_flag') is not None:
            raise ScorecardPromotionRefused()
        for key in SCORECARD_FIELDS:
            if market.get(key) is not None:
                raise ScorecardPromotionRefused()
        assert_tape_honesty(market)
        if not legs_complete(market):
            raise MissingLegRefused()
        complete += 1
    if not admitted and complete != STUB_MARKETS_N:
        raise MissingLegRefused()
    return payload


def load_panel(stub_path=None, admitted_path=None):
    """Stub by default. panel_admitted.json wins when it is on disk."""
    path = select_panel_path(stub_path, admitted_path)
    if path.resolve() == PANEL_STUB.resolve():
        _assert_freeze_bytes()
    payload = json.loads(path.read_text())
    return _validate_panel(payload, admitted=path.name == 'panel_admitted.json')


def combo_fee_table(panel):
    """In-memory series override. The feebook file on disk is not written."""
    loaded = feebook.load_series_table()
    if loaded.get('formula_id') != feebook.EXAMINER_FORMULA_ID:
        raise OrchestratorError('examiner formula')
    binds = panel['binds']
    if binds.get('fee_type_series_override') != FEE_TYPE_OVERRIDE:
        raise OrchestratorError('fee type')
    if binds.get('forbid_inherited_q7_fee_literals') is not True:
        raise ShadowFeeLiteralRefused()
    multiplier = feebook.as_decimal(binds['fee_multiplier'], 'fee_multiplier')
    if multiplier != feebook.ONE:
        raise OrchestratorError('multiplier')
    table = {
        'schema': loaded['schema'],
        'formula_id': loaded['formula_id'],
        'rates': dict(loaded['rates']),
        'default': dict(loaded['default']),
        'overrides': {},
    }
    for series in BOUND_SERIES:
        table['overrides'][series] = {
            'M': format(multiplier, 'f'),
            'maker_fees_enabled': True,
            'fee_type': FEE_TYPE_OVERRIDE,
        }
    return table


def arm_table():
    return tuple({'id': arm, 'leg_mid_source': LEG_MID_SOURCE[arm]} for arm in ARMS)


def instrument_binding(panel=None):
    """One leg-mid knob. Combo fee override and rails commits stay fixed."""
    if panel is None:
        panel = load_panel()
    table = combo_fee_table(panel)
    quote = feebook.order_fee(
        'maker', '1', '0.50', round_up=True, series=SERIES, table=table,
    )
    assert_combo_override_quote(quote)
    unbound = feebook.order_fee(
        'maker', '1', '0.50', round_up=True, series='KXNFLGAME', table=table,
    )
    if unbound['series_resolution'] != 'default_unknown_series':
        raise OrchestratorError('series resolution')
    probe = hygiene.fee_delta(
        'maker', '1', '0.50', quote['rate'], round_up=True, series=SERIES, table=table,
    )
    if probe['examiner_formula_id'] != feebook.EXAMINER_FORMULA_ID:
        raise OrchestratorError('examiner formula')
    if probe['inherited_model_id'] != hygiene.INHERITED_MODEL_ID:
        raise OrchestratorError('inherited model')
    if hygiene.FEEBOOK_COMMIT != FEEBOOK_COMMIT:
        raise OrchestratorError('feebook commit')
    if hygiene.RAILS_COMMIT != RAILS_COMMIT:
        raise OrchestratorError('rails commit')
    if rails.FEE_CREDIT_RULE_ID != 'astra.r1p5.rails.maker_credit_floor_cent.v1':
        raise OrchestratorError('rails rule')
    observation = rails.BookObservation(
        rails.canonical_book_content({'schema': 's5-leg'}),
        't0',
    )
    verdict = rails.judge_freshness(None, observation)
    if not verdict.fresh:
        raise OrchestratorError('freshness')
    for series, override in table['overrides'].items():
        if series not in BOUND_SERIES:
            raise OrchestratorError('series')
        if override['fee_type'] != FEE_TYPE_OVERRIDE:
            raise OrchestratorError('fee type')
    return {
        'experiment_id': EXPERIMENT_ID,
        'lab_directory': LAB_DIRECTORY,
        'knob': KNOB,
        'arms': arm_table(),
        'panel_version': panel['panel_version'],
        'admitted_at': panel.get('admitted_at'),
        'series_ticker': SERIES,
        'feature_family': 'MVE-FL',
        'strategy_pointer': None,
        'feebook_commit': FEEBOOK_COMMIT,
        'rails_commit': RAILS_COMMIT,
        'fee_type_series_override': FEE_TYPE_OVERRIDE,
        'combo_series_resolution': quote['series_resolution'],
        'examiner_formula_id': feebook.EXAMINER_FORMULA_ID,
        'fee_credit_rule_id': rails.FEE_CREDIT_RULE_ID,
        'inherited_model_id': hygiene.INHERITED_MODEL_ID,
        'fee_source': 'feebook',
        'rails_source': 'rails',
        'probe_formula_id': probe['examiner_formula_id'],
        'probe_scorecard_write': False,
        'rfq_in_scope': False,
        'r1p4_strategy_open': False,
        'logan_keys_required': False,
        'live_orders': False,
        'signal_retune_000': False,
        'queue_fragility_reopen': False,
        'cap_sr_reopen': False,
        'admit_py_run': False,
        'fee_is_knob': False,
        'dead_cards': DEAD_CARDS,
        'queued_behind': QUEUED_BEHIND,
        'scorecard_fields': SCORECARD_FIELDS,
        'kernel_sha256': KERNEL_SHA256,
        'packet_sha256': PACKET_SHA256,
        'panel_stub_sha256': PANEL_STUB_SHA256,
    }


def published_scorecard():
    """Freeze outputs. Every instrument field is present and null."""
    scorecard = {key: None for key in OUTPUT_KEYS}
    for key in OUTPUT_KEYS:
        if scorecard[key] is not None:
            raise ScorecardPromotionRefused()
    scorecard['status'] = 'EMPTY_RESULTS_PRE_EXAMINER'
    scorecard['rfq_in_scope'] = False
    scorecard['r1p4_strategy_open'] = False
    scorecard['logan_keys_required'] = False
    return scorecard


def assert_null_scorecard(payload):
    """Require every instrument field, results, and pnl, and require null."""
    if not isinstance(payload, dict):
        raise ScorecardPromotionRefused()
    for key in OUTPUT_KEYS:
        if key not in payload or payload[key] is not None:
            raise ScorecardPromotionRefused()
    return payload


def write_scorecard(payload):
    """Refuse a missing or non-null measurement field. Nothing is written."""
    assert_null_scorecard(payload)
    raise ScorecardPromotionRefused()


def _market_slot(market):
    if not legs_complete(market):
        raise MissingLegRefused()
    assert_tape_honesty(market)
    slot = {
        'market_ticker': market['market_ticker'],
        'event_ticker': market['event_ticker'],
        'series_ticker': market['series_ticker'],
        'mve_collection_ticker': market.get('mve_collection_ticker'),
        'legs_n': market['legs_n'],
        'legs_complete': True,
        'fill_price': None,
        'leg_product': None,
    }
    for key in OUTPUT_KEYS:
        slot[key] = None
    return slot


def _panel_report(arm, panel):
    if arm not in LEG_MID_SOURCE:
        raise UnknownLegMidSource()
    markets = panel.get('markets') or []
    if not markets:
        raise OrchestratorError('markets')
    slots = [_market_slot(market) for market in markets]
    complete = sum(1 for slot in slots if slot['legs_complete'])
    published = published_scorecard()
    report = {
        'experiment_id': EXPERIMENT_ID,
        'arm': arm,
        'leg_mid_source': LEG_MID_SOURCE[arm],
        'source': 'panel',
        'markets_n': len(slots),
        'legs_complete_n': complete,
        'empty_tape': empty_tape(panel),
        'markets': slots,
        'schema_product': None,
        'published': published,
        'promoted': False,
        'strategy_pointer': None,
        'rfq_in_scope': False,
        'r1p4_strategy_open': False,
        'logan_keys_required': False,
        'live_orders': False,
        'fee_pin': FEEBOOK_COMMIT,
        'rails_pin': RAILS_COMMIT,
        'fee_type_series_override': FEE_TYPE_OVERRIDE,
    }
    for key in OUTPUT_KEYS:
        report[key] = None
    if arm == S5L0:
        report['cohort_note'] = 'empty_tape_no_tob_mids'
    if arm == S5L1:
        report['cohort_note'] = 'synthetic_product_fixture_only'
    assert_null_scorecard(report)
    assert_null_scorecard(published)
    for slot in slots:
        assert_null_scorecard(slot)
        if slot['fill_price'] is not None or slot['leg_product'] is not None:
            raise InventedFillRefused()
    return report


def conduct(arm, panel=None):
    """Schema for one leg-mid source on the loaded panel. Scorecard fields stay null."""
    if arm not in LEG_MID_SOURCE:
        raise UnknownLegMidSource()
    if panel is None:
        panel = load_panel()
    return _panel_report(arm, panel)


def load_synthetic_product(path=None):
    """Known-product stand-in for S5L1. Not a live GET and not a panel fill."""
    path = SYNTHETIC_PRODUCT if path is None else Path(path)
    payload = json.loads(Path(path).read_text())
    if payload.get('source') != 'synthetic_schema_standin':
        raise OrchestratorError('source')
    legs = payload.get('legs')
    if not isinstance(legs, list) or len(legs) < 2:
        raise MissingLegRefused()
    for leg in legs:
        for key in OUTPUT_KEYS:
            if key in leg and leg[key] is not None:
                raise ScorecardPromotionRefused()
        if leg.get('fill_price') is not None or leg.get('print_price') is not None:
            raise InventedFillRefused()
    prints = payload.get('prints') or []
    if not isinstance(prints, list) or len(prints) < 1:
        raise OrchestratorError('synthetic prints')
    for row in prints:
        if row.get('label') != SYNTHETIC_PRINT_LABEL:
            raise InventedFillRefused()
        for key in OUTPUT_KEYS:
            if key in row and row[key] is not None:
                raise ScorecardPromotionRefused()
    if 'known_product' not in payload:
        raise OrchestratorError('known product')
    return payload


def conduct_synthetic(arm, path=None):
    """In-memory S5L1 product. Does not write the freeze scorecard."""
    if arm != S5L1:
        raise SyntheticArmRefused()
    payload = load_synthetic_product(path)
    product = independent_leg_product(payload['legs'])
    expected = feebook.as_decimal(payload['known_product'], 'known_product')
    if product != expected:
        raise OrchestratorError('known product')
    prints = payload['prints']
    published = published_scorecard()
    report = {
        'experiment_id': EXPERIMENT_ID,
        'arm': S5L1,
        'leg_mid_source': LEG_MID_SOURCE[S5L1],
        'source': 'synthetic_schema_standin',
        'schema_product': product,
        'known_product_match': True,
        'synthetic_print_count': len(prints),
        'schema_print_scored': False,
        'public_tape': False,
        'published': published,
        'promoted': False,
        'strategy_pointer': None,
        'rfq_in_scope': False,
        'r1p4_strategy_open': False,
        'logan_keys_required': False,
        'live_orders': False,
        'fee_pin': FEEBOOK_COMMIT,
        'rails_pin': RAILS_COMMIT,
        'fee_type_series_override': FEE_TYPE_OVERRIDE,
    }
    for key in OUTPUT_KEYS:
        report[key] = None
    assert_null_scorecard(report)
    assert_null_scorecard(published)
    return report


def frozen_output_snapshot():
    """Read freeze files. Does not modify them."""
    payloads = {
        'frozen': json.loads(FROZEN_EXPERIMENT.read_text()),
        'empty': json.loads(EMPTY_RESULTS.read_text()),
        'bundle_frozen': json.loads((LAB_BUNDLE / 'FROZEN_EXPERIMENT.json').read_text()),
        'bundle_results': json.loads((LAB_BUNDLE / 'results.json').read_text()),
        'governance_frozen': json.loads((GOVERNANCE_BUNDLE / 'FROZEN_EXPERIMENT.json').read_text()),
        'governance_results': json.loads((GOVERNANCE_BUNDLE / 'results.json').read_text()),
    }
    snapshot = {}
    for name, payload in payloads.items():
        for key in ('results', 'pnl'):
            if key not in payload or payload[key] is not None:
                raise ScorecardPromotionRefused()
            snapshot['%s.%s' % (name, key)] = None
        if name not in ('frozen', 'bundle_frozen', 'governance_frozen'):
            for key in SCORECARD_FIELDS:
                if key not in payload or payload[key] is not None:
                    raise ScorecardPromotionRefused()
                snapshot['%s.%s' % (name, key)] = None
    return snapshot
