"""C5 KXBTC15M fee and queue honesty stress.

Measurement only. Imports the R1-P1 feebook, the R1-P5 rails, the Examiner
fee-channel field list, and the hygiene helpers that Examiner join already
calls. The C1 queue-bin helper is imported for a sibling agreement check.
This module does not edit those labs, does not trade crypto, does not read
Logan keys, and does not write scorecard metrics.
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

LAB_DIRECTORY = 'kalshi_c5_kxbtc15m_honesty_lab_20260923'
EXPERIMENT_ID = 'C5-KXBTC15M-HONESTY-HARNESS'
PANEL_PACKET_ID = 'C5-KXBTC15M-MEAS'
SERIES = 'KXBTC15M'
PANEL_VERSION = '2026-09-22.c5-kxbtc15m-v0'
KNOB = 'honesty_stress_cadence'
C5H0 = 'C5H0'
C5H1 = 'C5H1'
ARMS = (C5H0, C5H1)
CADENCE = {
    C5H0: 'per_window',
    C5H1: 'multi_window_stack',
}
FEEBOOK_COMMIT = '22371178cb2663250b4762f328069571c48cb551'
RAILS_COMMIT = '6a28e0d6254327ea4e6451c781bec56215ac6cac'
CAP_SR_BASE = '45863037a30af6caf9c00361e46fe8bd5444c426'
PACKET_SHA256 = '23b908af6e9a7799c9bbdac04b27e683dfccd0c0c25d691df84ff715202d3cab'
KERNEL_SHA256 = '4d1b72a38603de181e71f80b3cc6515b170a2bffe11f8770dac1296373e50263'
PANEL_STUB_SHA256 = '60f613e8d775b66b9044ad31d2faf77bba84176f214a7bce599aa7a65b6905f8'
PUBLIC_HOST = 'https://api.elections.kalshi.com/trade-api/v2'
OUT_OF_SCOPE_ROUTE = 'POST /portfolio/orders'
SCORECARD_FIELDS = (
    'freshness_gap_sec',
    'queue_bin_mismatch_rate',
    'fee_delta_vs_inherited_model',
    'turnover_stress_flag',
)
OUTPUT_KEYS = SCORECARD_FIELDS + ('results', 'pnl')
EXAMINER_FEE_FIELDS = (
    'fee_delta_vs_inherited_model',
    'freshness_gap_sec',
    'queue_bin_mismatch_rate',
)
ADVERSARY_LABELS = {
    'live_crypto_trading': 'live crypto trading is refused',
    'live_crypto': 'live crypto trading is refused',
    'bacchus_port': 'bacchus strategy port is refused',
    'bacchus': 'bacchus strategy port is refused',
    'kxeth15m_strategy_port': 'kxeth15m strategy port is refused',
    'kxeth15m': 'kxeth15m strategy port is refused',
    'invented_pnl': 'invented pnl is refused',
}
DOES_NOT_MODIFY = (
    'kalshi_feebook_lab_20260922',
    'kalshi_rails_lab_20260922',
    'kalshi_capital_structure_lab_20260922',
    'kalshi_soft_blended_reserves_000_lab_20260923',
    'kalshi_queue_fragility_000_lab_20260922',
    'kalshi_examiner_fee_queue_honesty_000_lab_20260922',
    'kalshi_c1_kxufcfight_honesty_lab_20260922',
    'kalshi_r2p1_hygiene_000_lab_20260922',
    'kalshi_r3_p1_fee_cost_lab_20260922',
    'kalshi_r3_p4_l2_shape_lab_20260922',
    'nfl_factorial_lab_20260921',
    'nfl_paircheck_lab_20260922',
)
PACKET_NAME = 'C5_KXBTC15M_HONESTY_HARNESS_FREEZE_2026-09-23.md'
KERNEL_NAME = 'C5_KXBTC15M_MEASUREMENT_FREEZE_KERNEL_2026-09-22.md'
PACKET = ROOT / PACKET_NAME
KERNEL = ROOT / KERNEL_NAME
LAB_BUNDLE = ROOT / 'C5_KXBTC15M_HONESTY_HARNESS'
GOVERNANCE_BUNDLE = PARENT / 'packets' / 'C5_KXBTC15M_HONESTY_HARNESS'
GOVERNANCE_TREE = PARENT / 'lab' / 'governance' / 'astra' / 'packets'
FROZEN_EXPERIMENT = ROOT / 'FROZEN_EXPERIMENT.json'
EMPTY_RESULTS = ROOT / 'results' / 'EMPTY_RESULTS.json'
PANEL_STUB = PARENT / 'lab' / 'astra-capture' / 'c5-kxbtc15m' / 'panel_stub.json'
PANEL_ADMITTED = PARENT / 'lab' / 'astra-capture' / 'c5-kxbtc15m' / 'panel_admitted.json'
SYNTHETIC_WINDOWS = ROOT / 'fixtures' / 'synthetic_multi_window.json'
EXAMINER_ORCH = (
    PARENT / 'kalshi_examiner_fee_queue_honesty_000_lab_20260922' / 'orchestrator.py'
)
C1_ORCH = PARENT / 'kalshi_c1_kxufcfight_honesty_lab_20260922' / 'orchestrator.py'
INVENTORY_KEYS = ('volume_fp', 'volume_24h_fp', 'open_interest_fp')


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
    """Live crypto, a bacchus port, or an invented PnL was requested."""

    def __init__(self, label):
        self.label = label
        super().__init__(label)


class PanelVersionRefused(OrchestratorError):
    """The panel file is not the pinned C5 seed."""

    def __init__(self):
        super().__init__('panel_version')


class ShadowFeeLiteralRefused(OrchestratorError):
    """A fee quote bypassed the examiner feebook formula."""

    def __init__(self):
        super().__init__('shadow fee literal')


class InventedInventoryRefused(OrchestratorError):
    """Volume, open interest, or turnover was filled without Examiner."""

    def __init__(self):
        super().__init__('invented open interest')


class UnknownCadence(OrchestratorError):
    """The only knob is per_window or multi_window_stack."""

    def __init__(self):
        super().__init__('honesty_stress_cadence')


def _load_module(module_name, path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise OrchestratorError('sibling import')
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


examiner = _load_module('c5_examiner_honesty', EXAMINER_ORCH)
hygiene = examiner.hygiene_join.hygiene
c1 = _load_module('c5_c1_harness', C1_ORCH)


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
    """Named adversary labels from the C1/C3/C5 refuse bind. Nothing is traded."""
    if label not in ADVERSARY_LABELS:
        raise OrchestratorError('adversary label')
    raise AdversaryRefused(ADVERSARY_LABELS[label])


def turnover_stress_flag(volume_fp):
    """The flag stays null while volume is unset. Examiner owns a later fill."""
    if volume_fp is not None:
        raise InventedInventoryRefused()
    return None


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


def sibling_agreement(queue_ahead):
    """Hygiene and C1 attribute the same rails bin. The scorecard stays null."""
    hygiene_bin = hygiene.queue_attribution_bin(queue_ahead)
    c1_bin = c1.queue_attribution_bin(queue_ahead)
    if hygiene_bin != c1_bin:
        raise OrchestratorError('queue bin')
    fee_names = tuple(
        name for name, _value_type in examiner.channel_fields(examiner.FEE_CHANNEL)
    )
    if fee_names != EXAMINER_FEE_FIELDS:
        raise OrchestratorError('examiner fee fields')
    for name in EXAMINER_FEE_FIELDS:
        if name not in SCORECARD_FIELDS:
            raise OrchestratorError('scorecard')
    return {
        'queue_attribution_bin': hygiene_bin,
        'examiner_fee_fields': fee_names,
        'c1_matches_hygiene': True,
    }


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


def _validate_panel(payload, admitted):
    if not isinstance(payload, dict):
        raise OrchestratorError('panel')
    if payload.get('panel_version') != PANEL_VERSION:
        raise PanelVersionRefused()
    if payload.get('packet_id') != PANEL_PACKET_ID:
        raise OrchestratorError('packet')
    if payload.get('series_ticker') != SERIES:
        raise OrchestratorError('series')
    stamp = payload.get('admitted_at')
    if admitted:
        if not isinstance(stamp, str) or not stamp.endswith('Z'):
            raise OrchestratorError('admitted_at')
    elif stamp is not None:
        raise OrchestratorError('admitted_at')
    for key in ('results', 'pnl', 'volume'):
        _require_null(payload, key)
    hard_rule = payload.get('hard_rule') or ''
    if 'NOT live crypto trading' not in hard_rule:
        raise AdversaryRefused(ADVERSARY_LABELS['live_crypto_trading'])
    binds = payload.get('binds') or {}
    if binds.get('fee_lab_sha') != FEEBOOK_COMMIT:
        raise OrchestratorError('feebook commit')
    if binds.get('rails_lab_sha') != RAILS_COMMIT:
        raise OrchestratorError('rails commit')
    if binds.get('fee_formula_id') != feebook.EXAMINER_FORMULA_ID:
        raise OrchestratorError('examiner formula')
    if binds.get('no_live_orders') is not True:
        raise LiveOrdersForbidden()
    if binds.get('no_live_crypto_trading') is not True:
        raise AdversaryRefused(ADVERSARY_LABELS['live_crypto_trading'])
    if binds.get('no_bacchus_or_kxeth15m_strategy_port') is not True:
        raise AdversaryRefused(ADVERSARY_LABELS['bacchus_port'])
    if binds.get('kxeth15m_watch_only') is not True:
        raise AdversaryRefused(ADVERSARY_LABELS['kxeth15m_strategy_port'])
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
        'reciprocal_book_high_turnover',
        'fee_channel_r1p1',
        'turnover_honesty_objects',
    ):
        if (objects.get(key) or {}).get('status') is not None:
            raise ScorecardPromotionRefused()
    rails_stress = objects.get('rails_stress') or {}
    for key in (
        'status',
        'content_fresh_flag',
        'queue_attribution_bin',
        'maker_credit_floor_zero_refuse',
    ):
        if rails_stress.get(key) is not None:
            raise ScorecardPromotionRefused()
    events = payload.get('events') or []
    markets = payload.get('markets') or []
    counts = payload.get('cohort_counts') or {}
    if admitted:
        if len(markets) < 1 or len(events) < 1:
            raise OrchestratorError('cohort')
    else:
        if len(markets) != 1 or len(events) != 1:
            raise OrchestratorError('cohort')
        if counts.get('markets_n') != 1 or counts.get('events_n') != 1:
            raise OrchestratorError('cohort')
    for event in events:
        if event.get('series_ticker') != SERIES:
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
        if market.get('series_ticker') != SERIES:
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
    return payload


def load_panel(stub_path=None, admitted_path=None):
    """Stub by default. panel_admitted.json wins when it is on disk."""
    path = select_panel_path(stub_path, admitted_path)
    if path.resolve() == PANEL_STUB.resolve():
        _assert_freeze_bytes()
    payload = json.loads(path.read_text())
    return _validate_panel(payload, admitted=path.name == 'panel_admitted.json')


def arm_table():
    return tuple({'id': arm, 'cadence': CADENCE[arm]} for arm in ARMS)


def instrument_binding(panel=None):
    """One cadence knob. Fee and rails commits stay fixed. No scorecard fill."""
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
    if hygiene.FEEBOOK_COMMIT != FEEBOOK_COMMIT or examiner.FEEBOOK_COMMIT != FEEBOOK_COMMIT:
        raise OrchestratorError('feebook commit')
    if c1.FEEBOOK_COMMIT != FEEBOOK_COMMIT:
        raise OrchestratorError('feebook commit')
    if hygiene.RAILS_COMMIT != RAILS_COMMIT or examiner.RAILS_COMMIT != RAILS_COMMIT:
        raise OrchestratorError('rails commit')
    if c1.RAILS_COMMIT != RAILS_COMMIT:
        raise OrchestratorError('rails commit')
    agreement = sibling_agreement(rails.QUEUE_AHEAD_DEFAULT)
    if agreement['queue_attribution_bin'] != 'q3300':
        raise OrchestratorError('queue bin')
    return {
        'experiment_id': EXPERIMENT_ID,
        'lab_directory': LAB_DIRECTORY,
        'knob': KNOB,
        'arms': arm_table(),
        'panel_version': panel['panel_version'],
        'admitted_at': panel.get('admitted_at'),
        'series_ticker': SERIES,
        'strategy_pointer': None,
        'feebook_commit': FEEBOOK_COMMIT,
        'rails_commit': RAILS_COMMIT,
        'examiner_formula_id': feebook.EXAMINER_FORMULA_ID,
        'fee_credit_rule_id': rails.FEE_CREDIT_RULE_ID,
        'inherited_model_id': hygiene.INHERITED_MODEL_ID,
        'fee_source': 'feebook',
        'queue_source': 'rails',
        'honesty_helpers': 'hygiene',
        'probe_formula_id': probe['examiner_formula_id'],
        'probe_scorecard_write': False,
        'examiner_fee_fields': agreement['examiner_fee_fields'],
        'live_crypto_trading': False,
        'logan_keys_required': False,
        'live_orders': False,
        'signal_retune_000': False,
        'queue_fragility_reopen': False,
        'bacchus_port': False,
        'cap_sr_reopen': False,
        'c3_implemented': False,
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
    scorecard['live_crypto_trading'] = False
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


def windows_from_panel(panel):
    """One slot per market already on the panel. The stub is not expanded."""
    rows = []
    for market in panel.get('markets') or []:
        if market.get('series_ticker') != SERIES:
            raise OrchestratorError('series')
        for key in INVENTORY_KEYS:
            if market.get(key) is not None:
                raise InventedInventoryRefused()
        rows.append({
            'event_ticker': market['event_ticker'],
            'market_ticker': market['market_ticker'],
            'series_ticker': SERIES,
            'occurrence_datetime': market.get('occurrence_datetime'),
        })
    if not rows:
        raise OrchestratorError('windows')
    return rows


def _window_slot(window):
    slot = {
        'event_ticker': window['event_ticker'],
        'market_ticker': window['market_ticker'],
        'series_ticker': window.get('series_ticker', SERIES),
    }
    for key in SCORECARD_FIELDS:
        slot[key] = None
    slot['results'] = None
    slot['pnl'] = None
    if turnover_stress_flag(None) is not None:
        raise ScorecardPromotionRefused()
    return slot


def _report(arm, windows, source):
    if arm not in CADENCE:
        raise UnknownCadence()
    if not windows:
        raise OrchestratorError('windows')
    slots = [_window_slot(window) for window in windows]
    published = published_scorecard()
    report = {
        'experiment_id': EXPERIMENT_ID,
        'arm': arm,
        'cadence': CADENCE[arm],
        'stacked': arm == C5H1,
        'source': source,
        'window_count': len(slots),
        'windows': slots,
        'published': published,
        'promoted': False,
        'strategy_pointer': None,
        'live_crypto_trading': False,
        'live_orders': False,
        'bacchus_port': False,
        'fee_pin': FEEBOOK_COMMIT,
        'rails_pin': RAILS_COMMIT,
    }
    for key in OUTPUT_KEYS:
        report[key] = None
    if arm == C5H1 and source == 'panel' and len(slots) < 2:
        report['cohort_note'] = 'stub_n_expand_only_after_admit'
    assert_null_scorecard(report)
    assert_null_scorecard(published)
    return report


def conduct(arm, panel=None):
    """Schema for one cadence on the loaded panel. Scorecard fields stay null."""
    if arm not in CADENCE:
        raise UnknownCadence()
    if panel is None:
        panel = load_panel()
    return _report(arm, windows_from_panel(panel), 'panel')


def load_synthetic_windows(path=None):
    """Multi-window stand-in for C5H1. Not a live GET and not a panel fill."""
    path = SYNTHETIC_WINDOWS if path is None else Path(path)
    payload = json.loads(Path(path).read_text())
    if payload.get('source') != 'synthetic_schema_standin':
        raise OrchestratorError('source')
    windows = payload.get('windows')
    if not isinstance(windows, list) or len(windows) < 2:
        raise OrchestratorError('synthetic windows')
    for row in windows:
        if row.get('series_ticker') != SERIES:
            raise OrchestratorError('series')
        for key in INVENTORY_KEYS + OUTPUT_KEYS:
            if key in row and row[key] is not None:
                raise InventedInventoryRefused()
    return windows


def conduct_synthetic(arm, path=None):
    """In-memory cadence schema. Does not write the freeze scorecard."""
    if arm not in CADENCE:
        raise UnknownCadence()
    return _report(arm, load_synthetic_windows(path), 'synthetic_schema_standin')


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
        if name != 'frozen' and name != 'bundle_frozen' and name != 'governance_frozen':
            for key in SCORECARD_FIELDS:
                if key not in payload or payload[key] is not None:
                    raise ScorecardPromotionRefused()
                snapshot['%s.%s' % (name, key)] = None
    return snapshot
