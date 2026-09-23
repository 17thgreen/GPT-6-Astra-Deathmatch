"""R3-P4 L2-CAT sports-versus-nonsports category-slice harness.

Measurement only. Imports the R1-P1 feebook, the R1-P5 rails, and the
read-only SF1/SF2 algebra in the PR13 base shape lab. This module does not
edit those labs, does not place orders, does not read Logan keys, does not
run admit.py, and does not write scorecard metrics.

The checkout harness freeze, parent kernel, and panel stub match the attached
conductor sha256 values. The stub has 4 events and 6 markets (sports 4,
nonsports 2). Invented depth is refused. Lee-Ready is refused. ATL@GB is
refused. The superseded digest prefix e7c6b6d5 is not a pin.
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
HYGIENE_PATH = PARENT / 'kalshi_r2p1_hygiene_000_lab_20260922' / 'hygiene.py'
SHAPE_PATH = PARENT / 'kalshi_r3_p4_l2_shape_lab_20260922' / 'shape.py'
for _path in (FEEBOOK_DIR, RAILS_DIR):
    if str(_path) not in sys.path:
        sys.path.insert(0, str(_path))

import feebook
import rails

LAB_DIRECTORY = 'kalshi_r3p4_l2_cat_lab_20260923'
EXPERIMENT_ID = 'R3-P4-L2-CAT-HARNESS'
PANEL_PACKET_ID = 'R3-P4-L2-SHAPE-SF1-SF2'
FEATURE_FAMILY = 'L2-CAT'
SCHEMA_ID = 'astra.registry.r3_p4_l2_shape_panel.v0'
PANEL_VERSION = '2026-09-22.r3-p4-l2-shape-v0'
KNOB = 'category_slice'
R3P4C0 = 'R3P4C0'
R3P4C1 = 'R3P4C1'
ARMS = (R3P4C0, R3P4C1)
CATEGORY_SLICE = {
    R3P4C0: 'sports_only',
    R3P4C1: 'nonsports_only',
}
SLICE_VALUE = {
    R3P4C0: 'sports',
    R3P4C1: 'non_sports',
}
SPORTS_SERIES = 'KXNCAAFGAME'
NONSPORTS_SERIES = 'KXBTC'
SERIES_BY_SLICE = {
    'sports': SPORTS_SERIES,
    'non_sports': NONSPORTS_SERIES,
}
SPORTS_EVENTS = (
    'KXNCAAFGAME-26SEP26BUCKPITT',
    'KXNCAAFGAME-26SEP26TEXTENN',
    'KXNCAAFGAME-26SEP26PREMRST',
)
NONSPORTS_EVENTS = (
    'KXBTC-26SEP2317',
)
STUB_EVENTS = SPORTS_EVENTS + NONSPORTS_EVENTS
SPORTS_MARKETS = (
    'KXNCAAFGAME-26SEP26BUCKPITT-PITT',
    'KXNCAAFGAME-26SEP26BUCKPITT-BUCK',
    'KXNCAAFGAME-26SEP26TEXTENN-TENN',
    'KXNCAAFGAME-26SEP26PREMRST-MRST',
)
NONSPORTS_MARKETS = (
    'KXBTC-26SEP2317-T76250',
    'KXBTC-26SEP2317-T95749.99',
)
STUB_MARKETS = SPORTS_MARKETS + NONSPORTS_MARKETS
EXCLUDED_PROBES = (
    'KXBTC15M-26SEP111930-30',
    'KXBTC15M-26SEP111945-45',
)
FEEBOOK_COMMIT = '22371178cb2663250b4762f328069571c48cb551'
RAILS_COMMIT = '6a28e0d6254327ea4e6451c781bec56215ac6cac'
BASE_COMMIT = '3b0d1429b9ea702f2cb242e79f21f5ab5d3f18a6'
CONDUCTOR_PACKET_SHA256 = '3fc370d93f0ea42864f7bf482d7f6515254999c76e2fc4477df1273bfcdc051f'
CONDUCTOR_KERNEL_SHA256 = '4a4e7cc61efcb436955c566edc7a2681603a014725bc79047f9d825392064528'
CONDUCTOR_PANEL_STUB_SHA256 = '7477e023ab70c59a6739650155ddb9d77077766e3afd80443e540d60b5a86cbb'
CONDUCTOR_STAMP_SHA256 = '6108488d33a4be6ece3235fa5b5a39cf563e97a543e3d8ec9828c4f5bea8ba9e'
SEED_SUMMARY_SHA256 = 'e0d5281133d89d5f0215a8f02ae438b688bf53e4a48f2eb4c3727db4a29bb6f2'
PACKET_SHA256 = CONDUCTOR_PACKET_SHA256
KERNEL_SHA256 = CONDUCTOR_KERNEL_SHA256
PANEL_STUB_SHA256 = CONDUCTOR_PANEL_STUB_SHA256
SUPERSEDED_DIGEST_PREFIX = 'e7c6b6d5'
CONDUCTOR_EVENTS_N_CLAIM = 4
CONDUCTOR_MARKETS_N_CLAIM = 6
CONDUCTOR_SPORTS_N_CLAIM = 4
CONDUCTOR_NONSPORTS_N_CLAIM = 2
PUBLIC_HOST_ALLOWLIST = ['https://api.elections.kalshi.com/trade-api/v2']
OUT_OF_SCOPE_ROUTE = 'POST /portfolio/orders'
SCORECARD_FIELDS = (
    'sf1_median_half_spread_bps_by_mid_decile',
    'sf2_l1_top10_depth_share',
    'sf2_kl_vs_uniform_1_10',
    'sports_vs_nonsports_sf_gap',
    'n_books',
    'n_snapshots',
)
OUTPUT_KEYS = SCORECARD_FIELDS + ('results', 'pnl')
EVENT_INVENTORY_KEYS = ('volume_fp', 'open_interest_fp')
MARKET_INVENTORY_KEYS = ('volume_fp', 'volume_24h_fp', 'open_interest_fp')
ADVERSARY_LABELS = {
    'invented_depth': 'invented depth is refused',
    'lee_ready': 'Lee-Ready is refused on every input',
    'atl_gb': 'ATL@GB enrichment is refused',
    'live_orders': 'live orders are refused',
    'logan_keys': 'Logan keys are refused',
    'invented_pnl': 'invented pnl is refused',
    'invented_fills': 'invented fills are refused',
    'invented_markets': 'invented markets are refused',
    'q6_retune': 'Q6-000 retune is refused',
    '000': 'Q6-000 retune is refused',
    'qf_reopen': 'queue-fragility reopen is refused',
    'cap_sr_reopen': 'Cap-SR reopen is refused',
    'cap_sr_fx_reopen': 'Cap-SR-FX reopen is refused',
    'admit_py': 'admit.py is refused',
    'completed_profit': 'completed profit is refused',
}
DEAD_CARDS = (
    'invented_depth_PRIMARY',
    'Lee-Ready_REFUSED',
    '000_retune_REFUSED',
    'QF_reopen_DENIED',
    'Cap-SR_reopen_DENIED',
    'Cap-SR-FX_closed',
    'ATL@GB_REFUSED',
)
DOES_NOT_MODIFY = (
    'kalshi_feebook_lab_20260922',
    'kalshi_rails_lab_20260922',
    'kalshi_r3_p4_l2_shape_lab_20260922',
    'kalshi_r2p1_hygiene_000_lab_20260922',
    'kalshi_queue_fragility_000_lab_20260922',
    'kalshi_soft_blended_reserves_000_lab_20260923',
    'kalshi_cap_sr_effects_000_lab_20260923',
    'kalshi_c3_kxhighny_bordering_lab_20260923',
    'kalshi_c5_kxbtc15m_honesty_lab_20260923',
    'kalshi_r3p3_fl_maker_taker_lab_20260923',
    'kalshi_s4_ncaaf_feequue_lab_20260923',
    'kalshi_s5_mve_filllegs_lab_20260923',
    'kalshi_r2p3_prop_ladder_lab_20260923',
    'nfl_factorial_lab_20260921',
    'nfl_paircheck_lab_20260922',
)
PACKET_NAME = 'R3_P4_L2_CAT_HARNESS_FREEZE_2026-09-23_2259.md'
KERNEL_NAME = 'R3-P4_L2_SHAPE_LONGSHOT_DEPTH_FREEZE_KERNEL_2026-09-22.md'
STAMP_NAME = 'CONDUCTOR_FROZEN_EXPERIMENT.json'
SEED_NAME = 'SEED_SUMMARY.json'
PACKET = ROOT / PACKET_NAME
KERNEL = ROOT / KERNEL_NAME
CONDUCTOR_STAMP = ROOT / STAMP_NAME
LAB_BUNDLE = ROOT / 'R3_P4_L2_CAT_HARNESS'
GOVERNANCE_BUNDLE = PARENT / 'packets' / 'R3_P4_L2_CAT_HARNESS'
GOVERNANCE_TREE = PARENT / 'lab' / 'governance' / 'astra' / 'packets'
FROZEN_EXPERIMENT = ROOT / 'FROZEN_EXPERIMENT.json'
EMPTY_RESULTS = ROOT / 'results' / 'EMPTY_RESULTS.json'
CAPTURE_DIR = PARENT / 'lab' / 'astra-capture' / 'r3-p4-l2-shape'
PANEL_STUB = CAPTURE_DIR / 'panel_stub.json'
PANEL_ADMITTED = CAPTURE_DIR / 'panel_admitted.json'
SEED_SUMMARY = ROOT / 'fixtures' / SEED_NAME
SYNTHETIC_LADDER = ROOT / 'fixtures' / 'synthetic_mid_depth_ladder.json'
LIVE_GET_DIR = PARENT / 'packets' / 'r3_p4_l2_shape' / 'live_get_2026-09-22'


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
    """A named out-of-scope label was requested."""

    def __init__(self, label):
        self.label = label
        super().__init__(label)


class LeeReadyRefused(OrchestratorError):
    """Lee-Ready is refused on every input."""

    def __init__(self):
        super().__init__('Lee-Ready refused')


class AtlGbRefused(OrchestratorError):
    """ATL@GB is excluded from this panel."""

    def __init__(self):
        super().__init__(ADVERSARY_LABELS['atl_gb'])


class PanelVersionRefused(OrchestratorError):
    """The panel file is not the pinned R3-P4 L2 seed."""

    def __init__(self):
        super().__init__('panel_version')


class ShadowFeeLiteralRefused(OrchestratorError):
    """A fee quote bypassed the examiner feebook formula."""

    def __init__(self):
        super().__init__('shadow fee literal')


class InventedDepthRefused(OrchestratorError):
    """Depth was invented beyond the recorded fixture or the synthetic stand-in."""

    def __init__(self):
        super().__init__(ADVERSARY_LABELS['invented_depth'])


class EmptySeedRefused(OrchestratorError):
    """An empty market seed is not this panel."""

    def __init__(self):
        super().__init__('empty seed refused')


class RecreationRefused(OrchestratorError):
    """A labeled recreation of the conductor stub is refused."""

    def __init__(self):
        super().__init__('labeled recreation refused')


class SupersededDigestRefused(OrchestratorError):
    """The superseded e7c6b6d5 digest is not a pin."""

    def __init__(self):
        super().__init__('superseded digest')


class UnknownSlice(OrchestratorError):
    """The only knob is sports_only or nonsports_only."""

    def __init__(self):
        super().__init__('category_slice')


class AdmitPyRefused(OrchestratorError):
    """admit.py is not run from this harness."""

    def __init__(self):
        super().__init__(ADVERSARY_LABELS['admit_py'])


def _load_module(module_name, path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise OrchestratorError('sibling import')
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


hygiene = _load_module('r3p4cat_hygiene', HYGIENE_PATH)
shape = _load_module('r3p4cat_shape_algebra', SHAPE_PATH)


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
    """Allowlisted public GETs. Portfolio and order routes raise."""
    if not isinstance(route, str) or route == '':
        raise LiveOrdersForbidden()
    if not route.startswith('GET '):
        raise LiveOrdersForbidden()
    lowered = route.lower()
    if '/portfolio' in lowered or '/orders' in lowered:
        raise LiveOrdersForbidden()
    return None


def refuse_adversary(label):
    """Named refuse labels. Nothing is traded and no depth is invented."""
    if label not in ADVERSARY_LABELS:
        raise OrchestratorError('adversary label')
    if label == 'invented_depth':
        raise InventedDepthRefused()
    if label == 'lee_ready':
        raise LeeReadyRefused()
    if label == 'atl_gb':
        raise AtlGbRefused()
    if label == 'live_orders':
        raise LiveOrdersForbidden()
    if label == 'admit_py':
        raise AdmitPyRefused()
    raise AdversaryRefused(ADVERSARY_LABELS[label])


def infer_lee_ready(row):
    """Lee-Ready has no success path. Every input is refused."""
    if row is None or isinstance(row, (dict, str, int, float, list, tuple)):
        raise LeeReadyRefused()
    raise LeeReadyRefused()


def assert_not_superseded(digest):
    """Refuse the superseded digest prefix. Do not pin it."""
    if isinstance(digest, str) and digest.startswith(SUPERSEDED_DIGEST_PREFIX):
        raise SupersededDigestRefused()
    return digest


def materialize_live_get():
    """The live_get directory is import-only. This harness does not create it."""
    raise InventedDepthRefused()


def score_recorded_orderbook(market):
    """Recorded GET depth stays in the fixture. It is not an Examiner SF row."""
    if market is None or isinstance(market, (dict, list, str)):
        raise ScorecardPromotionRefused()
    raise ScorecardPromotionRefused()


def publish_category_gap(sports_value, nonsports_value):
    """The sports-versus-nonsports gap is an Examiner field."""
    if sports_value is None or sports_value is not None or nonsports_value is None:
        raise ScorecardPromotionRefused()
    raise ScorecardPromotionRefused()


def classify_depth(row):
    """Accept a declared source label. Invented depth raises. Nothing is scored."""
    if not isinstance(row, dict):
        raise InventedDepthRefused()
    if row.get('invent_depth') is True or row.get('depth_source') == 'invented':
        raise InventedDepthRefused()
    source = row.get('depth_source')
    if source == 'synthetic_schema_standin':
        return source
    if source == 'recorded_fixture':
        return source
    raise InventedDepthRefused()


def _atl_banned(value):
    if not isinstance(value, str):
        return False
    token = value.upper().replace(' ', '')
    return 'ATLGB' in token or 'ATL@GB' in value.upper()


def _require_null(payload, key):
    if key not in payload or payload[key] is not None:
        raise ScorecardPromotionRefused()


def _walk_digests(payload):
    if isinstance(payload, dict):
        for key, value in payload.items():
            if isinstance(key, str) and key.endswith('sha256') and isinstance(value, str):
                assert_not_superseded(value)
            else:
                _walk_digests(value)
    elif isinstance(payload, list):
        for item in payload:
            _walk_digests(item)


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


def _slice_value(arm):
    if arm not in SLICE_VALUE:
        raise UnknownSlice()
    return SLICE_VALUE[arm]


def _category_name(arm):
    if arm not in CATEGORY_SLICE:
        raise UnknownSlice()
    return CATEGORY_SLICE[arm]


def conductor_pin_status():
    """Report whether checkout bytes match the attached conductor sha256 values."""
    packet_match = sha256_file(PACKET) == CONDUCTOR_PACKET_SHA256 == PACKET_SHA256
    kernel_match = sha256_file(KERNEL) == CONDUCTOR_KERNEL_SHA256 == KERNEL_SHA256
    stub_match = sha256_file(PANEL_STUB) == CONDUCTOR_PANEL_STUB_SHA256 == PANEL_STUB_SHA256
    for digest in (PACKET_SHA256, KERNEL_SHA256, PANEL_STUB_SHA256):
        assert_not_superseded(digest)
    return {
        'packet_matches_conductor_claim': packet_match,
        'kernel_matches_conductor_claim': kernel_match,
        'panel_stub_matches_conductor_claim': stub_match,
        'conductor_bytes_in_checkout': packet_match and kernel_match and stub_match,
        'events_n_claim': CONDUCTOR_EVENTS_N_CLAIM,
        'markets_n_claim': CONDUCTOR_MARKETS_N_CLAIM,
        'sports_n_claim': CONDUCTOR_SPORTS_N_CLAIM,
        'nonsports_n_claim': CONDUCTOR_NONSPORTS_N_CLAIM,
        'superseded_digest_prefix': SUPERSEDED_DIGEST_PREFIX,
        'live_get_present': LIVE_GET_DIR.is_dir(),
    }


def _assert_named_copies(name, digest):
    copies = (
        ROOT / name,
        LAB_BUNDLE / name,
        PARENT / 'packets' / name,
        GOVERNANCE_BUNDLE / name,
    )
    for path in copies:
        if sha256_file(path) != digest:
            raise OrchestratorError(name)


def _assert_seed_copies():
    copies = (
        SEED_SUMMARY,
        CAPTURE_DIR / SEED_NAME,
        LAB_BUNDLE / SEED_NAME,
        GOVERNANCE_BUNDLE / SEED_NAME,
    )
    for path in copies:
        if sha256_file(path) != SEED_SUMMARY_SHA256:
            raise OrchestratorError('seed summary sha256')
    payload = json.loads(SEED_SUMMARY.read_text())
    if payload.get('panel_version') != PANEL_VERSION:
        raise OrchestratorError('seed summary')
    if payload.get('freeze_packet_sha256') != KERNEL_SHA256:
        raise OrchestratorError('seed summary')
    cohort = payload.get('cohort') or {}
    if cohort.get('markets_seed_n') != CONDUCTOR_MARKETS_N_CLAIM:
        raise OrchestratorError('seed summary')
    if cohort.get('sports_n') != CONDUCTOR_SPORTS_N_CLAIM:
        raise OrchestratorError('seed summary')
    if cohort.get('non_sports_n') != CONDUCTOR_NONSPORTS_N_CLAIM:
        raise OrchestratorError('seed summary')
    if cohort.get('events_n') != CONDUCTOR_EVENTS_N_CLAIM:
        raise OrchestratorError('seed summary')
    if cohort.get('orderbook_ok_n') != CONDUCTOR_MARKETS_N_CLAIM:
        raise OrchestratorError('seed summary')
    if tuple(payload.get('primary_tickers') or ()) != STUB_MARKETS:
        raise OrchestratorError('seed summary')


def _assert_freeze_bytes():
    _assert_named_copies(PACKET_NAME, PACKET_SHA256)
    _assert_named_copies(KERNEL_NAME, KERNEL_SHA256)
    for path in (
        PANEL_STUB,
        LAB_BUNDLE / 'panel_stub.json',
        GOVERNANCE_BUNDLE / 'panel_stub.json',
    ):
        if sha256_file(path) != PANEL_STUB_SHA256:
            raise OrchestratorError('stub sha256')
    for path in (CONDUCTOR_STAMP, LAB_BUNDLE / STAMP_NAME, GOVERNANCE_BUNDLE / STAMP_NAME):
        if sha256_file(path) != CONDUCTOR_STAMP_SHA256:
            raise OrchestratorError('conductor stamp sha256')
    stamp = json.loads(CONDUCTOR_STAMP.read_text())
    if stamp.get('freeze_sha256') != PACKET_SHA256:
        raise OrchestratorError('conductor stamp')
    if stamp.get('parent_freeze_sha256') != KERNEL_SHA256:
        raise OrchestratorError('conductor stamp')
    if stamp.get('panel_stub_sha256') != PANEL_STUB_SHA256:
        raise OrchestratorError('conductor stamp')
    if stamp.get('panel_events') != CONDUCTOR_EVENTS_N_CLAIM:
        raise OrchestratorError('conductor stamp')
    if stamp.get('panel_markets') != CONDUCTOR_MARKETS_N_CLAIM:
        raise OrchestratorError('conductor stamp')
    if stamp.get('arms') != list(ARMS):
        raise OrchestratorError('conductor stamp')
    if stamp.get('feature_family') != FEATURE_FAMILY:
        raise OrchestratorError('conductor stamp')
    if stamp.get('results') is not None or stamp.get('pnl') is not None:
        raise ScorecardPromotionRefused()
    _assert_seed_copies()


def select_panel_path(stub_path=None, admitted_path=None):
    """Prefer panel_admitted.json when the file exists. Otherwise the stub."""
    stub_path = PANEL_STUB if stub_path is None else Path(stub_path)
    admitted_path = PANEL_ADMITTED if admitted_path is None else Path(admitted_path)
    if Path(admitted_path).is_file():
        return Path(admitted_path)
    if not Path(stub_path).is_file():
        raise OrchestratorError('panel stub')
    return Path(stub_path)


def _stamp_ok(stamp, admitted, panel_stamp):
    if admitted:
        if stamp not in (None, panel_stamp):
            raise OrchestratorError('admitted_at')
        return
    if stamp is not None:
        raise OrchestratorError('admitted_at')


def _validate_market(market, admitted):
    if not isinstance(market, dict):
        raise OrchestratorError('markets')
    ticker = market.get('market_ticker')
    if _atl_banned(ticker) or _atl_banned(market.get('event_ticker')):
        raise AtlGbRefused()
    if ticker in EXCLUDED_PROBES:
        raise RecreationRefused()
    slice_value = market.get('category_slice')
    if slice_value not in SERIES_BY_SLICE:
        raise OrchestratorError('category_slice')
    if market.get('series_ticker') != SERIES_BY_SLICE[slice_value]:
        raise RecreationRefused()
    if market.get('invent_depth') is True:
        raise InventedDepthRefused()
    for key in MARKET_INVENTORY_KEYS:
        _require_null(market, key)
    for key in ('half_spread_bps', 'l2_shape', 'results', 'pnl'):
        if key in market:
            _require_null(market, key)
    book = market.get('raw_orderbook')
    if not isinstance(book, dict):
        raise EmptySeedRefused()
    captured = book.get('captured_via')
    if not isinstance(captured, str) or not captured.startswith('GET '):
        raise LiveOrdersForbidden()
    if not isinstance(book.get('orderbook_fp'), dict):
        raise EmptySeedRefused()
    return ticker


def _validate_unadmitted_counts(payload, events, markets):
    summary = payload.get('cohort_summary') or {}
    if len(events) != CONDUCTOR_EVENTS_N_CLAIM or len(markets) != CONDUCTOR_MARKETS_N_CLAIM:
        if len(markets) == 0 or len(events) == 0:
            raise EmptySeedRefused()
        raise RecreationRefused()
    if summary.get('markets_seed_n') != CONDUCTOR_MARKETS_N_CLAIM:
        raise RecreationRefused()
    if summary.get('sports_n') != CONDUCTOR_SPORTS_N_CLAIM:
        raise RecreationRefused()
    if summary.get('non_sports_n') != CONDUCTOR_NONSPORTS_N_CLAIM:
        raise RecreationRefused()
    if summary.get('events_n') != CONDUCTOR_EVENTS_N_CLAIM:
        raise RecreationRefused()
    if summary.get('orderbook_ok_n') != CONDUCTOR_MARKETS_N_CLAIM:
        raise RecreationRefused()
    event_tickers = tuple(event.get('event_ticker') for event in events)
    market_tickers = tuple(market.get('market_ticker') for market in markets)
    if event_tickers != STUB_EVENTS or market_tickers != STUB_MARKETS:
        raise RecreationRefused()
    sports_n = sum(1 for market in markets if market.get('category_slice') == 'sports')
    nonsports_n = sum(1 for market in markets if market.get('category_slice') == 'non_sports')
    if sports_n != CONDUCTOR_SPORTS_N_CLAIM or nonsports_n != CONDUCTOR_NONSPORTS_N_CLAIM:
        raise RecreationRefused()
    log = payload.get('http_seed_log') or []
    if len(log) != CONDUCTOR_MARKETS_N_CLAIM:
        raise RecreationRefused()
    if any(row.get('orderbook') != 200 for row in log):
        raise RecreationRefused()
    probes = payload.get('scout_probes_finalized_empty_ob') or []
    probe_tickers = tuple(row.get('market_ticker') for row in probes)
    if probe_tickers != EXCLUDED_PROBES:
        raise RecreationRefused()


def _validate_panel(payload, admitted):
    if not isinstance(payload, dict):
        raise OrchestratorError('panel')
    _walk_digests(payload)
    if payload.get('schema_id') != SCHEMA_ID:
        raise OrchestratorError('schema')
    if payload.get('panel_version') != PANEL_VERSION:
        raise PanelVersionRefused()
    if payload.get('packet_id') != PANEL_PACKET_ID:
        raise OrchestratorError('packet')
    if payload.get('cohort_kind') != 'stratified_sports_vs_nonsports_l2_seed':
        raise OrchestratorError('cohort')
    freeze_sha = payload.get('freeze_packet_sha256')
    assert_not_superseded(freeze_sha)
    if freeze_sha != KERNEL_SHA256:
        raise OrchestratorError('freeze_packet_sha256')
    stamp = payload.get('admitted_at')
    if admitted:
        if not isinstance(stamp, str) or not stamp.endswith('Z'):
            raise OrchestratorError('admitted_at')
    elif stamp is not None:
        raise OrchestratorError('admitted_at')
    for key in ('results', 'pnl', 'volume'):
        _require_null(payload, key)
    objects = payload.get('measurement_objects') or {}
    sf1 = objects.get('SF1_half_spread_bps_by_mid_decile') or {}
    sf2 = objects.get('SF2_l1_top10_depth_share_kl_vs_uniform') or {}
    if sf1.get('status') is not None or sf1.get('values') is not None:
        raise ScorecardPromotionRefused()
    if sf2.get('status') is not None or sf2.get('l1_share') is not None:
        raise ScorecardPromotionRefused()
    if sf2.get('kl_vs_uniform') is not None or sf2.get('top10_shares') is not None:
        raise ScorecardPromotionRefused()
    binds = payload.get('binds') or {}
    if binds.get('fee_lab_sha') != FEEBOOK_COMMIT:
        raise OrchestratorError('feebook commit')
    if binds.get('rails_lab_sha') != RAILS_COMMIT:
        raise OrchestratorError('rails commit')
    if binds.get('fee_formula_id') != feebook.EXAMINER_FORMULA_ID:
        raise OrchestratorError('examiner formula')
    if binds.get('forbid_inherited_q7_fee_literals') is not True:
        raise ShadowFeeLiteralRefused()
    if binds.get('no_lee_ready') is not True:
        raise LeeReadyRefused()
    if binds.get('no_live_orders') is not True:
        raise LiveOrdersForbidden()
    if binds.get('no_000_retune') is not True:
        raise AdversaryRefused(ADVERSARY_LABELS['q6_retune'])
    if binds.get('logan_keys_required') is True:
        raise AdversaryRefused(ADVERSARY_LABELS['logan_keys'])
    capture = payload.get('capture') or {}
    if capture.get('mode') != 'GET_only_public':
        raise LiveOrdersForbidden()
    if capture.get('host_allowlist') != PUBLIC_HOST_ALLOWLIST:
        raise LiveOrdersForbidden()
    routes = capture.get('routes_allowlist')
    if not isinstance(routes, list) or not routes:
        raise LiveOrdersForbidden()
    for route in routes:
        assert_route(route)
    out_of_scope = capture.get('out_of_scope_routes') or []
    if OUT_OF_SCOPE_ROUTE not in out_of_scope:
        raise LiveOrdersForbidden()
    gate = payload.get('admit_gate')
    if isinstance(gate, dict) and gate.get('admit_py_run') is True:
        raise AdmitPyRefused()
    if isinstance(gate, str) and 'do not run admit.py' not in gate:
        raise AdmitPyRefused()
    events = payload.get('events')
    markets = payload.get('markets')
    if not isinstance(events, list) or not isinstance(markets, list):
        raise OrchestratorError('panel')
    if len(markets) == 0 or len(events) == 0:
        raise EmptySeedRefused()
    for event in events:
        if not isinstance(event, dict):
            raise OrchestratorError('events')
        if _atl_banned(event.get('event_ticker')) or _atl_banned(event.get('game_id')):
            raise AtlGbRefused()
        _stamp_ok(event.get('admitted_at'), admitted, stamp)
        for key in EVENT_INVENTORY_KEYS:
            _require_null(event, key)
        if 'volume_24h_fp' in event:
            _require_null(event, 'volume_24h_fp')
    for market in markets:
        _validate_market(market, admitted)
        _stamp_ok(market.get('admitted_at'), admitted, stamp)
    if not admitted:
        _validate_unadmitted_counts(payload, events, markets)
    return payload


def load_panel(stub_path=None, admitted_path=None):
    """Stub by default. panel_admitted.json wins when it is on disk."""
    path = select_panel_path(stub_path, admitted_path)
    if path.resolve() == PANEL_STUB.resolve():
        _assert_freeze_bytes()
    payload = json.loads(path.read_text())
    return _validate_panel(payload, admitted=path.name == 'panel_admitted.json')


def partition_rows(rows, arm, ticker_key):
    """Keep rows whose category_slice matches the arm. Other slices stay out."""
    target = _slice_value(arm)
    chosen = []
    for row in rows:
        if not isinstance(row, dict):
            raise OrchestratorError('partition')
        if _atl_banned(row.get(ticker_key)) or _atl_banned(row.get('event_ticker')):
            raise AtlGbRefused()
        if row.get('category_slice') == target:
            chosen.append(row)
    return chosen


def arm_table():
    return tuple(
        {'id': arm, 'category_slice': CATEGORY_SLICE[arm]} for arm in ARMS
    )


def instrument_binding(panel=None):
    """One category-slice knob. Fee and rails commits stay fixed."""
    if panel is None:
        panel = load_panel()
    quote = feebook.order_fee(
        'taker', '1', '0.50', round_up=True, series=SPORTS_SERIES,
    )
    assert_examiner_quote(quote)
    if quote['series_resolution'] != 'default_unknown_series':
        raise OrchestratorError('series resolution')
    probe_book = {
        'yes_dollars': [['0.49', '1']],
        'no_dollars': [['0.49', '1']],
    }
    reciprocal = feebook.reciprocal_book(probe_book)
    if reciprocal['spread_yes'] != feebook.as_decimal('0.02', 'spread'):
        raise OrchestratorError('reciprocal book')
    if hygiene.FEEBOOK_COMMIT != FEEBOOK_COMMIT or hygiene.RAILS_COMMIT != RAILS_COMMIT:
        raise OrchestratorError('pin')
    if rails.FEE_CREDIT_RULE_ID != 'astra.r1p5.rails.maker_credit_floor_cent.v1':
        raise OrchestratorError('rails rule')
    observation = rails.BookObservation(
        rails.canonical_book_content({'schema': 'r3p4-cat-probe'}),
        't0',
    )
    verdict = rails.judge_freshness(None, observation)
    if not verdict.fresh:
        raise OrchestratorError('freshness')
    pins = conductor_pin_status()
    if pins['conductor_bytes_in_checkout'] is not True:
        raise OrchestratorError('conductor bytes')
    markets = panel.get('markets') or []
    if len(markets) < 1:
        raise EmptySeedRefused()
    return {
        'experiment_id': EXPERIMENT_ID,
        'lab_directory': LAB_DIRECTORY,
        'feature_family': FEATURE_FAMILY,
        'knob': KNOB,
        'arms': arm_table(),
        'panel_version': panel['panel_version'],
        'admitted_at': panel.get('admitted_at'),
        'events_n': len(panel.get('events') or []),
        'markets_n': len(markets),
        'conductor_events_n_claim': CONDUCTOR_EVENTS_N_CLAIM,
        'conductor_markets_n_claim': CONDUCTOR_MARKETS_N_CLAIM,
        'conductor_sports_n_claim': CONDUCTOR_SPORTS_N_CLAIM,
        'conductor_nonsports_n_claim': CONDUCTOR_NONSPORTS_N_CLAIM,
        'strategy_pointer': None,
        'feebook_commit': FEEBOOK_COMMIT,
        'rails_commit': RAILS_COMMIT,
        'examiner_formula_id': feebook.EXAMINER_FORMULA_ID,
        'fee_credit_rule_id': rails.FEE_CREDIT_RULE_ID,
        'fee_source': 'feebook',
        'rails_source': 'rails',
        'shape_source': 'kalshi_r3_p4_l2_shape_lab_20260922',
        'probe_formula_id': quote['formula_id'],
        'probe_scorecard_write': False,
        'lee_ready': 'REFUSED',
        'atl_gb': 'REFUSED',
        'invented_depth': 'REFUSED',
        'logan_keys_required': False,
        'live_orders': False,
        'signal_retune_000': False,
        'queue_fragility_reopen': False,
        'cap_sr_reopen': False,
        'cap_sr_fx_reopen': False,
        'admit_py_run': False,
        'fee_is_knob': False,
        'dead_cards': DEAD_CARDS,
        'scorecard_fields': SCORECARD_FIELDS,
        'kernel_sha256': KERNEL_SHA256,
        'packet_sha256': PACKET_SHA256,
        'panel_stub_sha256': PANEL_STUB_SHA256,
        'conductor_stamp_sha256': CONDUCTOR_STAMP_SHA256,
        'seed_summary_sha256': SEED_SUMMARY_SHA256,
        'conductor_packet_sha256_claim': CONDUCTOR_PACKET_SHA256,
        'conductor_parent_freeze_sha256_claim': CONDUCTOR_KERNEL_SHA256,
        'conductor_panel_stub_sha256_claim': CONDUCTOR_PANEL_STUB_SHA256,
        'conductor_bytes_in_checkout': True,
        'packet_matches_conductor_claim': True,
        'live_get_present': pins['live_get_present'],
        'base_commit': BASE_COMMIT,
        'base_lab_mutated': False,
    }


def published_scorecard():
    """Freeze outputs. Every instrument field is present and null."""
    scorecard = {key: None for key in OUTPUT_KEYS}
    for key in OUTPUT_KEYS:
        if scorecard[key] is not None:
            raise ScorecardPromotionRefused()
    scorecard['status'] = 'EMPTY_RESULTS_PRE_EXAMINER'
    scorecard['lee_ready'] = 'REFUSED'
    scorecard['atl_gb'] = 'REFUSED'
    scorecard['invented_depth'] = 'REFUSED'
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


def _report(arm, source, extra):
    published = published_scorecard()
    report = {
        'experiment_id': EXPERIMENT_ID,
        'arm': arm,
        'category_slice': _category_name(arm),
        'slice': _slice_value(arm),
        'source': source,
        'published': published,
        'promoted': False,
        'strategy_pointer': None,
        'live_orders': False,
        'lee_ready': 'REFUSED',
        'atl_gb': 'REFUSED',
        'invented_depth': 'REFUSED',
        'fee_pin': FEEBOOK_COMMIT,
        'rails_pin': RAILS_COMMIT,
        'schema_scored': False,
        'production_depth_scored': False,
    }
    report.update(extra)
    for key in OUTPUT_KEYS:
        report[key] = None
    assert_null_scorecard(report)
    assert_null_scorecard(published)
    return report


def conduct(arm, panel=None):
    """Partition the loaded panel by category slice. Recorded books are not scored."""
    if arm not in SLICE_VALUE:
        raise UnknownSlice()
    if panel is None:
        panel = load_panel()
    events = partition_rows(panel.get('events') or [], arm, 'event_ticker')
    markets = partition_rows(panel.get('markets') or [], arm, 'market_ticker')
    if not markets:
        raise EmptySeedRefused()
    recorded = 0
    slots = []
    for market in markets:
        book = (market.get('raw_orderbook') or {}).get('orderbook_fp')
        if isinstance(book, dict):
            recorded += 1
        slots.append({
            'market_ticker': market.get('market_ticker'),
            'event_ticker': market.get('event_ticker'),
            'category_slice': market.get('category_slice'),
            'depth_source': 'recorded_fixture',
            'orderbook_recorded': isinstance(book, dict),
        })
    extra = {
        'event_count': len(events),
        'market_count': len(markets),
        'recorded_orderbook_n': recorded,
        'markets': slots,
        'panel_note': 'recorded_books_not_scored',
    }
    report = _report(arm, 'panel', extra)
    report['schema_scored'] = False
    report['production_depth_scored'] = False
    assert_null_scorecard(report)
    return report


def load_synthetic_ladder(path=None):
    """Known-identity stand-in. Not a live GET and not the conductor panel."""
    path = SYNTHETIC_LADDER if path is None else Path(path)
    payload = json.loads(Path(path).read_text())
    if payload.get('source') != 'synthetic_schema_standin':
        raise OrchestratorError('source')
    books = payload.get('books')
    if not isinstance(books, list) or len(books) < 2:
        raise OrchestratorError('synthetic ladder')
    return books


def schema_book(row):
    """SF1/SF2 algebra on one synthetic book. The scorecard is not written."""
    if classify_depth(row) != 'synthetic_schema_standin':
        raise InventedDepthRefused()
    book_id = row.get('book_id')
    if not isinstance(book_id, str) or not book_id.startswith('synthetic:'):
        raise InventedDepthRefused()
    if _atl_banned(book_id):
        raise AtlGbRefused()
    if row.get('lee_ready') != 'REFUSED':
        raise LeeReadyRefused()
    slice_value = row.get('category_slice')
    if slice_value not in SERIES_BY_SLICE:
        raise UnknownSlice()
    orderbook = row.get('orderbook_fp')
    if not isinstance(orderbook, dict):
        raise InventedDepthRefused()
    current = shape.observation(orderbook, row.get('transaction_time'))
    shape.require_content_fresh(
        None, current, keepalive=bool(row.get('keepalive', False)),
    )
    try:
        quote = shape.quoted_yes(orderbook)
        depth = shape.top10_depth(orderbook)
    except (feebook.BookIncomplete, shape.ShapeRefused) as exc:
        raise InventedDepthRefused() from exc
    return {
        'book_id': book_id,
        'category_slice': slice_value,
        'schema_half_spread_bps': quote['half_spread_bps'],
        'schema_decile': quote['decile'],
        'schema_mid': quote['mid'],
        'schema_l1_share': depth['l1_share'],
        'schema_kl_nats': depth['kl_nats'],
        'schema_scored': True,
        'production_depth': False,
    }


def conduct_synthetic(arm, path=None):
    """In-memory SF algebra on the synthetic ladder. Scorecard fields stay null."""
    if arm not in SLICE_VALUE:
        raise UnknownSlice()
    books = partition_rows(load_synthetic_ladder(path), arm, 'book_id')
    if not books:
        raise EmptySeedRefused()
    rows = [schema_book(book) for book in books]
    report = _report(arm, 'synthetic_schema_standin', {
        'books': rows,
        'book_count': len(rows),
        'public_tape': False,
    })
    report['schema_scored'] = True
    report['production_depth_scored'] = False
    assert_null_scorecard(report)
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
        'stamp': json.loads(CONDUCTOR_STAMP.read_text()),
    }
    snapshot = {}
    for name, payload in payloads.items():
        for key in ('results', 'pnl'):
            if key not in payload or payload[key] is not None:
                raise ScorecardPromotionRefused()
            snapshot['%s.%s' % (name, key)] = None
        if name in ('empty', 'bundle_results', 'governance_results'):
            for key in SCORECARD_FIELDS:
                if key not in payload or payload[key] is not None:
                    raise ScorecardPromotionRefused()
                snapshot['%s.%s' % (name, key)] = None
    return snapshot
