"""C3 KXHIGHNY bordering-strike harness.

Measurement only. Imports the R1-P1 feebook, the R1-P5 rails, and the
hygiene helpers the C5 honesty harness already calls. This module does not
edit those labs, does not edit C5, does not trade, does not read Logan keys,
and does not write scorecard metrics. Ladder rows are a structure hypothesis.
"""
import hashlib
import importlib.util
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

LAB_DIRECTORY = 'kalshi_c3_kxhighny_bordering_lab_20260923'
EXPERIMENT_ID = 'C3-KXHIGHNY-BORDERING-STRIKE-HARNESS'
PANEL_PACKET_ID = 'C3-KXHIGHNY-MEAS'
SERIES = 'KXHIGHNY'
PROOF_SERIES = 'KXHIGHCHI'
PANEL_VERSION = '2026-09-22.c3-kxhighny-v0'
KNOB = 'strike_band'
C3B0 = 'C3B0'
C3B1 = 'C3B1'
ARMS = (C3B0, C3B1)
BANDS = {
    C3B0: 'near_extreme',
    C3B1: 'mid_ladder',
}
NEAR_EXTREME_LOW = Decimal('0.10')
NEAR_EXTREME_HIGH = Decimal('0.90')
FEEBOOK_COMMIT = '22371178cb2663250b4762f328069571c48cb551'
RAILS_COMMIT = '6a28e0d6254327ea4e6451c781bec56215ac6cac'
UNTOUCHED_BASE = 'ee69245a5dba058ee1198c88bb4685893508f273'
PACKET_SHA256 = '27530d6427794a5559e40c7f56d6cd938d8c57cc8f51406fc26a5b0e36a5fdff'
KERNEL_SHA256 = '0e79a0194e2371efae8d8cac0f4f2ec9ce4cf53f60dd870bae1a1ed7acff3604'
PANEL_STUB_SHA256 = '2a5da7fe85ca1adc6b7c4dcf9e09ed5c6bb62be6b5c9b42731e36e31d1e8dfea'
PUBLIC_HOST = 'https://api.elections.kalshi.com/trade-api/v2'
OUT_OF_SCOPE_ROUTE = 'POST /portfolio/orders'
SCORECARD_FIELDS = (
    'adjacent_spread_gap',
    'bordering_depth_imbalance',
    'fee_delta_vs_inherited_model',
    'freshness_gap_sec',
    'multi_city_inventory_join',
)
OUTPUT_KEYS = SCORECARD_FIELDS + ('results', 'pnl')
ADVERSARY_LABELS = {
    'github_weather_spread_ev': 'GitHub weather-spread EV is hypothesis only',
    'github_ev': 'GitHub weather-spread EV is hypothesis only',
    'weather_spread_ev': 'GitHub weather-spread EV is hypothesis only',
    'invented_arb': 'invented cross-city arb is refused',
    'cross_city_arb': 'invented cross-city arb is refused',
    'settlement_penalty_ev': 'settlement-penalty EV is refused',
    'invented_pnl': 'invented pnl is refused',
    'fee_blind_completed_profit': 'fee-blind completed profit is refused',
    'completed_profit': 'fee-blind completed profit is refused',
    'live_order': 'live orders are refused',
    'r3p3_strategy_merge': 'R3-P3 weather preference is cite-only',
}
DOES_NOT_MODIFY = (
    'kalshi_feebook_lab_20260922',
    'kalshi_rails_lab_20260922',
    'kalshi_capital_structure_lab_20260922',
    'kalshi_soft_blended_reserves_000_lab_20260923',
    'kalshi_queue_fragility_000_lab_20260922',
    'kalshi_examiner_fee_queue_honesty_000_lab_20260922',
    'kalshi_c1_kxufcfight_honesty_lab_20260922',
    'kalshi_c5_kxbtc15m_honesty_lab_20260923',
    'kalshi_r2p1_hygiene_000_lab_20260922',
    'kalshi_r3_p1_fee_cost_lab_20260922',
    'kalshi_r3_p4_l2_shape_lab_20260922',
    'nfl_factorial_lab_20260921',
    'nfl_paircheck_lab_20260922',
)
PACKET_NAME = 'C3_KXHIGHNY_BORDERING_STRIKE_HARNESS_FREEZE_2026-09-23.md'
KERNEL_NAME = 'C3_KXHIGHNY_MEASUREMENT_FREEZE_KERNEL_2026-09-22.md'
PACKET = ROOT / PACKET_NAME
KERNEL = ROOT / KERNEL_NAME
LAB_BUNDLE = ROOT / 'C3_KXHIGHNY_BORDERING_STRIKE_HARNESS'
GOVERNANCE_BUNDLE = PARENT / 'packets' / 'C3_KXHIGHNY_BORDERING_STRIKE_HARNESS'
GOVERNANCE_TREE = PARENT / 'lab' / 'governance' / 'astra' / 'packets'
FROZEN_EXPERIMENT = ROOT / 'FROZEN_EXPERIMENT.json'
EMPTY_RESULTS = ROOT / 'results' / 'EMPTY_RESULTS.json'
PANEL_STUB = PARENT / 'lab' / 'astra-capture' / 'c3-kxhighny' / 'panel_stub.json'
PANEL_ADMITTED = PARENT / 'lab' / 'astra-capture' / 'c3-kxhighny' / 'panel_admitted.json'
SYNTHETIC_LADDER = ROOT / 'fixtures' / 'synthetic_ladder.json'
HYGIENE_PATH = PARENT / 'kalshi_r2p1_hygiene_000_lab_20260922' / 'hygiene.py'
C5_FROZEN = (
    PARENT / 'kalshi_c5_kxbtc15m_honesty_lab_20260923' / 'FROZEN_EXPERIMENT.json'
)
INVENTORY_KEYS = ('volume_fp', 'volume_24h_fp', 'open_interest_fp')
STUB_MARKETS_N = 6
STUB_EVENTS_N = 3
STUB_SERIES_N = 2
MID_LADDER_NOTE = 'stub_mid_ladder_pair_absent_expand_only_after_admit'


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
    """GitHub EV, an invented arb, or a strategy merge was requested."""

    def __init__(self, label):
        self.label = label
        super().__init__(label)


class PanelVersionRefused(OrchestratorError):
    """The panel file is not the pinned C3 seed."""

    def __init__(self):
        super().__init__('panel_version')


class ShadowFeeLiteralRefused(OrchestratorError):
    """A fee quote bypassed the examiner feebook formula."""

    def __init__(self):
        super().__init__('shadow fee literal')


class InventedInventoryRefused(OrchestratorError):
    """Volume, open interest, or a result was filled without Examiner."""

    def __init__(self):
        super().__init__('invented open interest')


class UnknownBand(OrchestratorError):
    """The only knob is near_extreme or mid_ladder."""

    def __init__(self):
        super().__init__('strike_band')


def _load_module(module_name, path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise OrchestratorError('sibling import')
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


hygiene = _load_module('c3_hygiene_labels', HYGIENE_PATH)


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


def refuse_adversary(label):
    """Named adversary labels. Nothing is traded and no EV is imported."""
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


def _refuse_evidence_labels(row):
    if not isinstance(row, dict):
        raise OrchestratorError('row')
    if row.get('github_weather_spread_ev') is True:
        raise AdversaryRefused(ADVERSARY_LABELS['github_weather_spread_ev'])
    if row.get('weather_spread_ev') is not None:
        raise AdversaryRefused(ADVERSARY_LABELS['weather_spread_ev'])
    if row.get('arb_pnl') is not None:
        raise AdversaryRefused(ADVERSARY_LABELS['invented_arb'])
    if row.get('settlement_penalty_ev') is not None:
        raise AdversaryRefused(ADVERSARY_LABELS['settlement_penalty_ev'])
    for key in ('results', 'pnl'):
        if key in row and row[key] is not None:
            raise ScorecardPromotionRefused()


def band_from_price(price):
    """Schema cut only. A scout role string is not an input."""
    price = feebook.as_decimal(price, 'price')
    if price < 0 or price > 1:
        raise OrchestratorError('price')
    if price <= NEAR_EXTREME_LOW or price >= NEAR_EXTREME_HIGH:
        return BANDS[C3B0]
    return BANDS[C3B1]


def classify_market(market):
    """Price band, or a declared band that agrees with the price when both exist."""
    _refuse_evidence_labels(market)
    declared = market.get('strike_band')
    price = market.get('last_price_dollars_raw_get')
    if declared is not None and declared not in BANDS.values():
        raise UnknownBand()
    if price is None and declared is None:
        raise UnknownBand()
    inferred = None if price is None else band_from_price(price)
    if declared is not None and inferred is not None and declared != inferred:
        raise OrchestratorError('strike band')
    if declared is not None:
        return declared
    return inferred


def _floor(market):
    floor = market.get('floor_strike')
    if isinstance(floor, bool) or not isinstance(floor, int):
        raise OrchestratorError('floor_strike')
    return floor


def _cap(market):
    cap = market.get('cap_strike')
    if cap is None:
        return None
    if isinstance(cap, bool) or not isinstance(cap, int):
        raise OrchestratorError('cap_strike')
    return cap


def normalize_market(market):
    """Copy ladder identity. Inventory and scorecard fields stay unread as fills."""
    for key in INVENTORY_KEYS:
        if market.get(key) is not None:
            raise InventedInventoryRefused()
    if market.get('result') is not None:
        raise InventedInventoryRefused()
    series = market.get('series_ticker')
    if series not in (SERIES, PROOF_SERIES):
        raise OrchestratorError('series')
    event = market.get('event_ticker')
    ticker = market.get('market_ticker')
    if not isinstance(event, str) or not isinstance(ticker, str):
        raise OrchestratorError('ticker')
    return {
        'event_ticker': event,
        'market_ticker': ticker,
        'series_ticker': series,
        'floor_strike': _floor(market),
        'cap_strike': _cap(market),
        'strike_band': classify_market(market),
        'occurrence_datetime': market.get('occurrence_datetime'),
    }


def bordering_pairs(markets, band):
    """Neighbors in floor_strike order inside one event and one band.

    The pair records structure. Spread, depth, and fee fields stay null.
    """
    if band not in BANDS.values():
        raise UnknownBand()
    grouped = {}
    for market in markets:
        if market['strike_band'] != band:
            continue
        if market['series_ticker'] not in (SERIES, PROOF_SERIES):
            raise OrchestratorError('series')
        grouped.setdefault(market['event_ticker'], []).append(market)
    pairs = []
    for event in sorted(grouped):
        rows = sorted(
            grouped[event],
            key=lambda item: (item['floor_strike'], item['market_ticker']),
        )
        for left, right in zip(rows, rows[1:]):
            if left['series_ticker'] != right['series_ticker']:
                raise OrchestratorError('series')
            pair = {
                'event_ticker': event,
                'series_ticker': left['series_ticker'],
                'left_ticker': left['market_ticker'],
                'right_ticker': right['market_ticker'],
                'left_floor_strike': left['floor_strike'],
                'right_floor_strike': right['floor_strike'],
                'strike_band': band,
                'structure_hyp_only': True,
                'github_weather_spread_ev': False,
            }
            for key in SCORECARD_FIELDS:
                pair[key] = None
            pair['results'] = None
            pair['pnl'] = None
            _refuse_evidence_labels(pair)
            pairs.append(pair)
    return pairs


def presence_from_rows(rows):
    """NY versus CHI calendar presence. The scorecard join stays null."""
    by_day = {}
    for row in rows:
        _refuse_evidence_labels(row)
        stamp = row.get('occurrence_datetime')
        if not isinstance(stamp, str) or len(stamp) < 10 or stamp[4] != '-' or stamp[7] != '-':
            raise OrchestratorError('occurrence')
        series = row.get('series_ticker')
        if series not in (SERIES, PROOF_SERIES):
            raise OrchestratorError('series')
        day = stamp[:10]
        slot = by_day.setdefault(day, {'ny_present': False, 'chi_present': False})
        if series == SERIES:
            slot['ny_present'] = True
        else:
            slot['chi_present'] = True
    days = []
    for day in sorted(by_day):
        slot = by_day[day]
        days.append({
            'calendar_day': day,
            'ny_present': slot['ny_present'],
            'chi_present': slot['chi_present'],
            'multi_city_inventory_join': None,
            'arb_pnl': None,
        })
    payload = {
        'kind': 'ny_chi_presence',
        'note': 'NY vs CHI presence instrument. Not arb PnL.',
        'days': days,
        'arb_pnl': None,
        'pnl': None,
        'multi_city_inventory_join': None,
    }
    _refuse_evidence_labels(payload)
    return payload


def _validate_panel(payload, admitted):
    if not isinstance(payload, dict):
        raise OrchestratorError('panel')
    _refuse_evidence_labels(payload)
    if payload.get('panel_version') != PANEL_VERSION:
        raise PanelVersionRefused()
    if payload.get('packet_id') != PANEL_PACKET_ID:
        raise OrchestratorError('packet')
    if payload.get('series_ticker') != SERIES:
        raise OrchestratorError('series')
    proof = payload.get('multi_city_proof_series') or []
    if PROOF_SERIES not in proof:
        raise OrchestratorError('series')
    cite = payload.get('r3p3_prefer_cite') or ''
    if 'not a strategy merge' not in cite:
        raise AdversaryRefused(ADVERSARY_LABELS['r3p3_strategy_merge'])
    stamp = payload.get('admitted_at')
    if admitted:
        if not isinstance(stamp, str) or not stamp.endswith('Z'):
            raise OrchestratorError('admitted_at')
    elif stamp is not None:
        raise OrchestratorError('admitted_at')
    for key in ('results', 'pnl', 'volume'):
        _require_null(payload, key)
    binds = payload.get('binds') or {}
    if binds.get('fee_lab_sha') != FEEBOOK_COMMIT:
        raise OrchestratorError('feebook commit')
    if binds.get('rails_lab_sha') != RAILS_COMMIT:
        raise OrchestratorError('rails commit')
    if binds.get('fee_formula_id') != feebook.EXAMINER_FORMULA_ID:
        raise OrchestratorError('examiner formula')
    if binds.get('no_live_orders') is not True:
        raise LiveOrdersForbidden()
    if binds.get('no_github_weather_spread_ev_as_evidence') is not True:
        raise AdversaryRefused(ADVERSARY_LABELS['github_weather_spread_ev'])
    if 'hypothesis only' not in (binds.get('structure_hyp_only') or ''):
        raise AdversaryRefused(ADVERSARY_LABELS['github_weather_spread_ev'])
    if binds.get('no_000_retune') is not True:
        raise OrchestratorError('000 retune')
    if binds.get('forbid_inherited_q7_fee_literals') is not True:
        raise ShadowFeeLiteralRefused()
    capture = payload.get('capture') or {}
    if capture.get('mode') != 'GET_only_public':
        raise LiveOrdersForbidden()
    if capture.get('host_allowlist') != [PUBLIC_HOST]:
        raise LiveOrdersForbidden()
    if OUT_OF_SCOPE_ROUTE not in (capture.get('out_of_scope_routes') or []):
        raise LiveOrdersForbidden()
    schedule = capture.get('schedule') or {}
    if schedule.get('recorder_started') is True or schedule.get('admit_py_run') is True:
        raise OrchestratorError('recorder')
    objects = payload.get('measurement_objects') or {}
    for key in (
        'reciprocal_book_threshold_strikes',
        'bordering_strike_ladder_objects',
        'fee_channel_r1p1',
        'multi_city_proof_join',
    ):
        if (objects.get(key) or {}).get('status') is not None:
            raise ScorecardPromotionRefused()
    rails_labels = objects.get('rails_labels') or {}
    for key in (
        'status',
        'content_fresh_flag',
        'maker_credit_floor_zero_refuse',
        'queue_attribution_bin',
    ):
        if rails_labels.get(key) is not None:
            raise ScorecardPromotionRefused()
    events = payload.get('events') or []
    markets = payload.get('markets') or []
    counts = payload.get('cohort_counts') or {}
    if admitted:
        if len(markets) < 1 or len(events) < 1:
            raise OrchestratorError('cohort')
    else:
        if len(markets) != STUB_MARKETS_N or len(events) != STUB_EVENTS_N:
            raise OrchestratorError('cohort')
        if counts.get('markets_n') != STUB_MARKETS_N or counts.get('events_n') != STUB_EVENTS_N:
            raise OrchestratorError('cohort')
        if counts.get('series_n') != STUB_SERIES_N or counts.get('open_list_resolved_n') != 0:
            raise OrchestratorError('cohort')
    for event in events:
        if event.get('series_ticker') not in (SERIES, PROOF_SERIES):
            raise OrchestratorError('series')
        if event.get('panel_version') != PANEL_VERSION:
            raise PanelVersionRefused()
        event_stamp = event.get('admitted_at')
        if admitted:
            if event_stamp not in (None, stamp):
                raise OrchestratorError('admitted_at')
        elif event_stamp is not None:
            raise OrchestratorError('admitted_at')
        for key in ('volume_fp', 'open_interest_fp'):
            _require_null(event, key)
    for market in markets:
        if market.get('series_ticker') not in (SERIES, PROOF_SERIES):
            raise OrchestratorError('series')
        if market.get('panel_version') != PANEL_VERSION:
            raise PanelVersionRefused()
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
        classify_market(market)
    return payload


def load_panel(stub_path=None, admitted_path=None):
    """Stub by default. panel_admitted.json wins when it is on disk."""
    path = select_panel_path(stub_path, admitted_path)
    if path.resolve() == PANEL_STUB.resolve():
        _assert_freeze_bytes()
    payload = json.loads(path.read_text())
    return _validate_panel(payload, admitted=path.name == 'panel_admitted.json')


def arm_table():
    return tuple({'id': arm, 'strike_band': BANDS[arm]} for arm in ARMS)


def instrument_binding(panel=None):
    """One strike-band knob. Fee and rails commits stay fixed. No scorecard fill."""
    if panel is None:
        panel = load_panel()
    quote = feebook.order_fee('taker', '1', '0.50', round_up=True, series=SERIES)
    assert_examiner_quote(quote)
    if quote['series_resolution'] != 'default_unknown_series':
        raise OrchestratorError('series resolution')
    panel_m = feebook.as_decimal(panel['binds']['fee_multiplier_live_get'], 'fee_multiplier')
    if quote['M'] != panel_m:
        raise OrchestratorError('multiplier')
    probe = hygiene.fee_delta(
        'taker', '1', '0.50', quote['rate'], round_up=True, series=SERIES,
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
    return {
        'experiment_id': EXPERIMENT_ID,
        'lab_directory': LAB_DIRECTORY,
        'knob': KNOB,
        'arms': arm_table(),
        'panel_version': panel['panel_version'],
        'admitted_at': panel.get('admitted_at'),
        'series_primary': SERIES,
        'series_proof': PROOF_SERIES,
        'strategy_pointer': None,
        'structure_hyp_only': True,
        'github_weather_spread_ev': False,
        'feebook_commit': FEEBOOK_COMMIT,
        'rails_commit': RAILS_COMMIT,
        'examiner_formula_id': feebook.EXAMINER_FORMULA_ID,
        'fee_credit_rule_id': rails.FEE_CREDIT_RULE_ID,
        'inherited_model_id': hygiene.INHERITED_MODEL_ID,
        'fee_source': 'feebook',
        'rails_source': 'rails',
        'honesty_helpers': 'hygiene',
        'probe_formula_id': probe['examiner_formula_id'],
        'probe_scorecard_write': False,
        'r3p3_prefer_cite': panel.get('r3p3_prefer_cite'),
        'r3p3_strategy_merge': False,
        'logan_keys_required': False,
        'live_orders': False,
        'signal_retune_000': False,
        'queue_fragility_reopen': False,
        'cap_sr_reopen': False,
        'c5_reopen': False,
        'fee_is_knob': False,
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
    scorecard['github_weather_spread_ev'] = False
    scorecard['structure_hyp_only'] = True
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


def _report(arm, markets, presence_rows, source):
    if arm not in BANDS:
        raise UnknownBand()
    if not markets:
        raise OrchestratorError('markets')
    band = BANDS[arm]
    pairs = bordering_pairs(markets, band)
    presence = presence_from_rows(presence_rows)
    published = published_scorecard()
    report = {
        'experiment_id': EXPERIMENT_ID,
        'arm': arm,
        'strike_band': band,
        'source': source,
        'pair_count': len(pairs),
        'pairs': pairs,
        'presence': presence,
        'published': published,
        'promoted': False,
        'structure_hyp_only': True,
        'github_weather_spread_ev': False,
        'r3p3_strategy_merge': False,
        'strategy_pointer': None,
        'live_orders': False,
        'logan_keys_required': False,
        'fee_pin': FEEBOOK_COMMIT,
        'rails_pin': RAILS_COMMIT,
    }
    for key in OUTPUT_KEYS:
        report[key] = None
    if arm == C3B1 and source == 'panel' and len(pairs) == 0:
        report['cohort_note'] = MID_LADDER_NOTE
    assert_null_scorecard(report)
    assert_null_scorecard(published)
    for pair in pairs:
        assert_null_scorecard(pair)
    if presence.get('arb_pnl') is not None or presence.get('pnl') is not None:
        raise AdversaryRefused(ADVERSARY_LABELS['invented_arb'])
    return report


def conduct(arm, panel=None):
    """Schema for one strike band on the loaded panel. Scorecard fields stay null."""
    if arm not in BANDS:
        raise UnknownBand()
    if panel is None:
        panel = load_panel()
    markets = [normalize_market(market) for market in panel['markets']]
    return _report(arm, markets, panel['events'], 'panel')


def load_synthetic_markets(path=None):
    """Band stand-in. Not a live GET and not a panel fill."""
    path = SYNTHETIC_LADDER if path is None else Path(path)
    payload = json.loads(Path(path).read_text())
    if payload.get('source') != 'synthetic_schema_standin':
        raise OrchestratorError('source')
    _refuse_evidence_labels(payload)
    markets = payload.get('markets')
    if not isinstance(markets, list) or len(markets) < 2:
        raise OrchestratorError('synthetic markets')
    normalized = []
    for row in markets:
        for key in INVENTORY_KEYS + OUTPUT_KEYS:
            if key in row and row[key] is not None:
                raise InventedInventoryRefused()
        normalized.append(normalize_market(row))
    return normalized


def conduct_synthetic(arm, path=None):
    """In-memory band schema. Does not write the freeze scorecard."""
    if arm not in BANDS:
        raise UnknownBand()
    markets = load_synthetic_markets(path)
    return _report(arm, markets, markets, 'synthetic_schema_standin')


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
