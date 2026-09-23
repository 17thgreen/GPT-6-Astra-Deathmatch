"""R3-P4 L2-SF half-spread versus depth-KL harness.

Measurement only. Imports the R1-P1 feebook, the R1-P5 rails, and the
read-only SF1/SF2 algebra in the PR13 base shape lab. This module does not
edit those labs, does not place orders, does not read Logan keys, does not
run admit.py, and does not write scorecard metrics.

Category slice is the panel's natural sports-plus-nonsports seed. It is not
an arm. One-sided recorded books keep the empty side empty.
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

LAB_DIRECTORY = 'kalshi_r3p4_l2_sf_lab_20260923'
EXPERIMENT_ID = 'R3-P4-L2-SF-HARNESS'
PANEL_PACKET_ID = 'R3-P4-L2-SHAPE-SF1-SF2'
FEATURE_FAMILY = 'L2-SF'
SCHEMA_ID = 'astra.registry.r3_p4_l2_shape_panel.v0'
PANEL_VERSION = '2026-09-22.r3-p4-l2-shape-v0'
KNOB = 'shape_object'
R3P4S0 = 'R3P4S0'
R3P4S1 = 'R3P4S1'
ARMS = (R3P4S0, R3P4S1)
SHAPE_OBJECT = {
    R3P4S0: 'sf1_half_spread',
    R3P4S1: 'sf2_depth_kl',
}
CLOSED_CATEGORY_ARMS = ('R3P4C0', 'R3P4C1', 'sports_only', 'nonsports_only')
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
STUB_MARKETS = (
    'KXNCAAFGAME-26SEP26BUCKPITT-PITT',
    'KXNCAAFGAME-26SEP26BUCKPITT-BUCK',
    'KXNCAAFGAME-26SEP26TEXTENN-TENN',
    'KXNCAAFGAME-26SEP26PREMRST-MRST',
    'KXBTC-26SEP2317-T76250',
    'KXBTC-26SEP2317-T95749.99',
)
ORDERBOOK_PINS = (
    ('KXNCAAFGAME-26SEP26BUCKPITT-PITT', 'ob_KXNCAAFGAME-26SEP26BUCKPITT-PITT.json', '9ab18dcdcb90ae60a41a264ddc91638783681473ce6d4136cee6f554437a2301', 916),
    ('KXNCAAFGAME-26SEP26BUCKPITT-BUCK', 'ob_KXNCAAFGAME-26SEP26BUCKPITT-BUCK.json', '05c0e9e4725f79a8ce223eae3d5acd27f02319ec1e268eb9f65c2f8a3f3d1f45', 1279),
    ('KXNCAAFGAME-26SEP26TEXTENN-TENN', 'ob_KXNCAAFGAME-26SEP26TEXTENN-TENN.json', 'f7fa72f7c052caf93bd07c98117d09e68cefcbfa1298045a701fbffbe61d1d1c', 2079),
    ('KXNCAAFGAME-26SEP26PREMRST-MRST', 'ob_KXNCAAFGAME-26SEP26PREMRST-MRST.json', 'b71b8d9d4bd478c5ea3a6fb5f6cc56e3f734d73f47881ebb7580d8569b4bc824', 603),
    ('KXBTC-26SEP2317-T76250', 'ob_KXBTC-26SEP2317-T76250.json', '3a2bcb5f8071d39688c765534366b94f3cea01064cda7393d37f06b85e64a2fd', 295),
    ('KXBTC-26SEP2317-T95749.99', 'ob_KXBTC-26SEP2317-T95749.99.json', 'dae4ef2855b9ce14092d9c1a14962348dcf70f2e78cccb137f9a8e0c70140839', 293),
)
EXCLUDED_PROBES = (
    'KXBTC15M-26SEP111930-30',
    'KXBTC15M-26SEP111945-45',
)
FEEBOOK_COMMIT = '22371178cb2663250b4762f328069571c48cb551'
RAILS_COMMIT = '6a28e0d6254327ea4e6451c781bec56215ac6cac'
BASE_COMMIT = 'd7b935951c9ddd5e6c4d813fad69e401b6a7b6a3'
FREEZE_SHA256 = 'f00425261f085aef90e93b186810a0248165273f8bb923ef3597940a9e8345de'
PARENT_SHA256 = '4a4e7cc61efcb436955c566edc7a2681603a014725bc79047f9d825392064528'
PANEL_STUB_SHA256 = '7477e023ab70c59a6739650155ddb9d77077766e3afd80443e540d60b5a86cbb'
CONDUCTOR_STAMP_SHA256 = 'df5f52aa191ae31df81b95da3346b39e27f8870484f83826d3a9370f84835762'
PRE_ACCEPT_EMPTY_SHA256 = '1362153d8ebb96d348184580a1d4fc4e5e6a0c030de3baf683f4664cef05fac0'
CONDUCTOR_ACCEPT_SHA256 = '4ebf316fce4dc9c6ce08893c7d09cdac9dc54b599bfd494c2f1e614c32172dcc'
EXAMINER_HOLD_SHA256 = 'ab69b4665f75fb468bac75c9a193bdee8f89bd2f0d4aca6a5f9d48582deadf80'
SOURCE_PINS_SHA256 = '6ac2f00e75b60bc5b3b865d55f68b332cd87998e44c61d214445d66e348e84fa'
EVENTS_N = 4
MARKETS_N = 6
SPORTS_N = 4
NONSPORTS_N = 2
PUBLIC_HOST_ALLOWLIST = ['https://api.elections.kalshi.com/trade-api/v2']
OUT_OF_SCOPE_ROUTE = 'POST /portfolio/orders'
LIVE_GET_DIRNAME = 'live_get_2026-09-22'
SCORECARD_FIELDS = (
    'sf1_median_half_spread_bps_by_mid_decile',
    'sf2_l1_top10_depth_share',
    'sf2_kl_vs_uniform_1_10',
    'n_books',
    'n_snapshots',
)
OUTPUT_KEYS = SCORECARD_FIELDS + ('results', 'pnl')
EVENT_INVENTORY_KEYS = ('volume_fp', 'open_interest_fp')
MARKET_INVENTORY_KEYS = ('volume_fp', 'volume_24h_fp', 'open_interest_fp')
ADVERSARY_LABELS = {
    'invented_depth': 'invented depth is refused',
    'invent_depth': 'invented depth is refused',
    'lee_ready': 'Lee-Ready is refused on every input',
    'atl_gb': 'ATL@GB enrichment is refused',
    'live_orders': 'live orders are refused',
    'logan_keys': 'Logan keys are refused',
    'invented_pnl': 'invented pnl is refused',
    'invented_fills': 'invented fills are refused',
    'invent_fills': 'invented fills are refused',
    'invented_markets': 'invented markets are refused',
    'q6_retune': 'Q6-000 retune is refused',
    '000': 'Q6-000 retune is refused',
    'qf_reopen': 'queue-fragility reopen is refused',
    'cap_sr_reopen': 'Cap-SR reopen is refused',
    'cap_sr_fx_reopen': 'Cap-SR-FX reopen is refused',
    'l2_cat_reopen': 'L2-CAT reopen is refused',
    'empty_ob_reopen': 'EMPTY-OB reopen is refused',
    'prop_lq_reopen': 'PROP-LQ reopen is refused',
    'sot_id_reopen': 'SOT-ID reopen is refused',
    'pr13_dual_edit': 'PR13 dual-edit into PnL is refused',
    'admit_py': 'admit.py is refused',
    'ungate_s2_r2p4': 'S2 and R2-P4 stay queued',
    'completed_profit': 'completed profit is refused',
    'category_slice_arm': 'category slice is not an arm',
}
DEAD_CARDS = (
    'invent_depth_fills_EMPTY_OB_just_gated',
    'Lee-Ready_REFUSED',
    'L2-CAT_reopen_DENIED',
    'EMPTY-OB_reopen_DENIED',
    'PR13_dual_edit_DENIED',
    'Cap-SR_reopen_DENIED',
    'QF_reopen_DENIED',
    'PROP-LQ_reopen_DENIED',
    'SOT-ID_reopen_DENIED',
    '000_retune_REFUSED',
    'ATL@GB_REFUSED',
    'S2_R2-P4_ungate_DENIED',
)
DOES_NOT_MODIFY = (
    'kalshi_feebook_lab_20260922',
    'kalshi_rails_lab_20260922',
    'kalshi_r3_p4_l2_shape_lab_20260922',
    'kalshi_r3p4_l2_cat_lab_20260923',
    'kalshi_c1_empty_ob_lab_20260923',
    'kalshi_r2p5_sot_id_lab_20260923',
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
    'lab/astra-capture/r3-p4-l2-shape',
    'packets/R3_P4_L2_CAT_HARNESS',
    'packets/C1_EMPTY_OB_HARNESS',
    'packets/R2_P5_SOT_ID_HARNESS',
    'nfl_factorial_lab_20260921',
)
FREEZE_NAME = 'R3_P4_L2_SF_HARNESS_FREEZE_2026-09-23.md'
PARENT_NAME = 'R3-P4_L2_SHAPE_LONGSHOT_DEPTH_FREEZE_KERNEL_2026-09-22.md'
STAMP_NAME = 'CONDUCTOR_FROZEN_EXPERIMENT.json'
PRE_ACCEPT_NAME = 'PRE_ACCEPT_EMPTY_RESULTS.json'
ACCEPT_NAME = 'CONDUCTOR_ACCEPT_R3_P4_L2_SF_HARNESS_2026-09-23.json'
HOLD_NAME = 'EXAMINER_HOLD_R3_P4_L2_SF_HARNESS_PRE_PR_2026-09-23.json'
SOURCE_PINS_NAME = 'SOURCE_PINS.json'
PACKETS_ROOT_NAMES = (FREEZE_NAME, ACCEPT_NAME, HOLD_NAME)
LAB_BUNDLE = ROOT / 'R3_P4_L2_SF_HARNESS'
GOVERNANCE_BUNDLE = PARENT / 'packets' / 'R3_P4_L2_SF_HARNESS'
GOVERNANCE_TREE = PARENT / 'lab' / 'governance' / 'astra'
PACKET = ROOT / FREEZE_NAME
PARENT_FREEZE = ROOT / PARENT_NAME
CONDUCTOR_STAMP = ROOT / STAMP_NAME
PRE_ACCEPT_EMPTY = ROOT / PRE_ACCEPT_NAME
CONDUCTOR_ACCEPT = ROOT / ACCEPT_NAME
EXAMINER_HOLD = ROOT / HOLD_NAME
SOURCE_PINS = ROOT / SOURCE_PINS_NAME
FROZEN_EXPERIMENT = ROOT / 'FROZEN_EXPERIMENT.json'
EMPTY_RESULTS = ROOT / 'results' / 'EMPTY_RESULTS.json'
CAPTURE_DIR = PARENT / 'lab' / 'astra-capture' / 'r3-p4-l2-shape'
PANEL_STUB = CAPTURE_DIR / 'panel_stub.json'
PANEL_ADMITTED = CAPTURE_DIR / 'panel_admitted.json'
SYNTHETIC_LADDER = ROOT / 'fixtures' / 'synthetic_two_sided_ladder.json'
CLOSED_LIVE_GET = PARENT / 'packets' / 'r3_p4_l2_shape' / 'live_get_2026-09-22'
SUPERSEDED_DIGEST_PREFIX = 'e7c6b6d5'


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
    """Depth was invented beyond the recorded fixture."""

    def __init__(self):
        super().__init__(ADVERSARY_LABELS['invented_depth'])


class InventFillRefused(OrchestratorError):
    """Fills are not invented from a quote book."""

    def __init__(self):
        super().__init__(ADVERSARY_LABELS['invented_fills'])


class EmptyBookRefused(OrchestratorError):
    """A both-sides-empty book is the EMPTY-OB gate, not this seed."""

    def __init__(self):
        super().__init__('empty book refused')


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


class UnknownShape(OrchestratorError):
    """The only knob is sf1_half_spread or sf2_depth_kl."""

    def __init__(self):
        super().__init__('shape_object')


class CategorySliceNotAnArm(OrchestratorError):
    """L2-CAT owns category slice. This harness does not reopen it."""

    def __init__(self):
        super().__init__(ADVERSARY_LABELS['category_slice_arm'])


class AdmitPyRefused(OrchestratorError):
    """admit.py is not run from this harness."""

    def __init__(self):
        super().__init__(ADVERSARY_LABELS['admit_py'])


class UngateRefused(OrchestratorError):
    """S2 and R2-P4 stay queued."""

    def __init__(self):
        super().__init__(ADVERSARY_LABELS['ungate_s2_r2p4'])


class Pr13DualEditRefused(OrchestratorError):
    """The PR13 base lab is not edited into PnL."""

    def __init__(self):
        super().__init__(ADVERSARY_LABELS['pr13_dual_edit'])


class PreAcceptEmptyRefused(OrchestratorError):
    """The attached pre-ACCEPT empty payload is not a scorecard."""

    def __init__(self):
        super().__init__('pre-ACCEPT empty refused')


class ExaminerNotReady(OrchestratorError):
    """Examiner stays NOT_SCORED. stub_ready stays false."""

    def __init__(self):
        super().__init__('examiner NOT_SCORED')


def _load_module(module_name, path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise OrchestratorError('sibling import')
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


hygiene = _load_module('r3p4sf_hygiene', HYGIENE_PATH)
shape = _load_module('r3p4sf_shape_algebra', SHAPE_PATH)


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


def fetch_over_network(url=None):
    """Offline pins only. This function does not open a socket."""
    if url is None or isinstance(url, str):
        raise LiveOrdersForbidden()
    raise LiveOrdersForbidden()


def refuse_adversary(label):
    """Named refuse labels. Nothing is traded and no depth is invented."""
    if label not in ADVERSARY_LABELS:
        raise OrchestratorError('adversary label')
    if label in ('invented_depth', 'invent_depth'):
        raise InventedDepthRefused()
    if label == 'lee_ready':
        raise LeeReadyRefused()
    if label == 'atl_gb':
        raise AtlGbRefused()
    if label == 'live_orders':
        raise LiveOrdersForbidden()
    if label == 'admit_py':
        raise AdmitPyRefused()
    if label in ('invented_fills', 'invent_fills'):
        raise InventFillRefused()
    if label == 'ungate_s2_r2p4':
        raise UngateRefused()
    if label == 'pr13_dual_edit':
        raise Pr13DualEditRefused()
    if label == 'category_slice_arm':
        raise CategorySliceNotAnArm()
    raise AdversaryRefused(ADVERSARY_LABELS[label])


def infer_lee_ready(row):
    """Lee-Ready has no success path. Every input is refused."""
    if row is None or isinstance(row, (dict, str, int, float, list, tuple)):
        raise LeeReadyRefused()
    raise LeeReadyRefused()


def invent_depth(payload):
    """There is no depth-invention path."""
    if payload is None or isinstance(payload, (dict, list, str)):
        raise InventedDepthRefused()
    raise InventedDepthRefused()


def fill_missing_side(orderbook):
    """An empty yes or no ladder stays empty."""
    if orderbook is None or isinstance(orderbook, dict):
        raise InventedDepthRefused()
    raise InventedDepthRefused()


def attempt_fill(payload, taker_side=None, contracts=None):
    """Quote books do not become fills."""
    if payload is None or taker_side is None or contracts is None:
        raise InventFillRefused()
    raise InventFillRefused()


def ungate_s2_r2p4():
    """This packet does not ungate S2 or R2-P4."""
    raise UngateRefused()


def run_admit_py():
    """admit.py is not run from this harness."""
    raise AdmitPyRefused()


def dual_edit_pr13(payload=None):
    """The PR13 base shape lab is import-only."""
    if payload is None or isinstance(payload, dict):
        raise Pr13DualEditRefused()
    raise Pr13DualEditRefused()


def stamp_examiner_ready():
    """Examiner stays NOT_SCORED until a later seat after merge."""
    raise ExaminerNotReady()


def assert_not_superseded(digest):
    """Refuse the superseded digest prefix. Do not pin it."""
    if isinstance(digest, str) and digest.startswith(SUPERSEDED_DIGEST_PREFIX):
        raise SupersededDigestRefused()
    return digest


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


def _shape_name(arm):
    if arm in CLOSED_CATEGORY_ARMS:
        raise CategorySliceNotAnArm()
    if arm not in SHAPE_OBJECT:
        raise UnknownShape()
    return SHAPE_OBJECT[arm]


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


def side_status(orderbook):
    """Classify recorded ladders. An empty side is not filled."""
    if not isinstance(orderbook, dict):
        raise InventedDepthRefused()
    yes = orderbook.get('yes_dollars')
    no = orderbook.get('no_dollars')
    if not isinstance(yes, list) or not isinstance(no, list):
        raise InventedDepthRefused()
    if len(yes) == 0 and len(no) == 0:
        raise EmptyBookRefused()
    two_sided = len(yes) > 0 and len(no) > 0
    return {
        'yes_levels': len(yes),
        'no_levels': len(no),
        'two_sided': two_sided,
        'missing_side_not_invented': not two_sided,
    }


def schema_probe(arm, orderbook):
    """Run the selected algebra in memory. The scorecard is not written.

    A one-sided book returns without a fabricated opposite ladder.
    """
    shape_name = _shape_name(arm)
    status = side_status(orderbook)
    row = {
        'shape_object': shape_name,
        'schema_scored': False,
        'production_depth_scored': False,
        'value_withheld_from_scorecard': True,
        'lee_ready': 'REFUSED',
    }
    row.update(status)
    if not status['two_sided']:
        return row
    try:
        if arm == R3P4S0:
            quote = shape.quoted_yes(orderbook)
            row['schema_half_spread_bps'] = quote['half_spread_bps']
            row['schema_decile'] = quote['decile']
            row['schema_mid'] = quote['mid']
        else:
            depth = shape.top10_depth(orderbook)
            row['schema_l1_share'] = depth['l1_share']
            row['schema_kl_nats'] = depth['kl_nats']
    except (feebook.BookIncomplete, shape.ShapeRefused) as exc:
        raise InventedDepthRefused() from exc
    row['schema_scored'] = True
    return row


def score_recorded_orderbook(market):
    """Recorded GET depth stays in the fixture. It is not an Examiner SF row."""
    if market is None or isinstance(market, (dict, list, str)):
        raise ScorecardPromotionRefused()
    raise ScorecardPromotionRefused()


def publish_shape_metric(shape_name, value):
    """Named SF aggregates stay null."""
    if shape_name in SHAPE_OBJECT.values() or value is None or value is not None:
        raise ScorecardPromotionRefused()
    raise ScorecardPromotionRefused()


def owned_dirs():
    return (ROOT, LAB_BUNDLE, GOVERNANCE_BUNDLE)


def live_get_directories():
    return tuple(directory / LIVE_GET_DIRNAME for directory in owned_dirs())


def _assert_digest(path, digest):
    if sha256_file(path) != digest:
        raise OrchestratorError(Path(path).name)


def _assert_owned(name, digest, packets_root=False):
    for directory in owned_dirs():
        _assert_digest(directory / name, digest)
    if packets_root:
        _assert_digest(PARENT / 'packets' / name, digest)


def _assert_orderbook_copies():
    if CLOSED_LIVE_GET.exists():
        raise OrchestratorError('l2-cat live_get path')
    for directory in live_get_directories():
        for ticker, filename, digest, size in ORDERBOOK_PINS:
            path = directory / filename
            raw = path.read_bytes()
            if len(raw) != size or hashlib.sha256(raw).hexdigest() != digest:
                raise OrchestratorError(filename)
            payload = json.loads(raw)
            book = payload.get('orderbook_fp')
            status = side_status(book)
            if status['yes_levels'] + status['no_levels'] <= 0:
                raise EmptyBookRefused()


def _assert_source_pins(payload):
    if payload.get('freeze_sha256') != FREEZE_SHA256:
        raise OrchestratorError('source pins')
    if payload.get('parent_freeze_sha256') != PARENT_SHA256:
        raise OrchestratorError('source pins')
    if payload.get('panel_stub_sha256') != PANEL_STUB_SHA256:
        raise OrchestratorError('source pins')
    if payload.get('conductor_stamp_sha256') != CONDUCTOR_STAMP_SHA256:
        raise OrchestratorError('source pins')
    if payload.get('pre_accept_empty_sha256') != PRE_ACCEPT_EMPTY_SHA256:
        raise OrchestratorError('source pins')
    if payload.get('conductor_accept_sha256') != CONDUCTOR_ACCEPT_SHA256:
        raise OrchestratorError('source pins')
    if payload.get('examiner_hold_sha256') != EXAMINER_HOLD_SHA256:
        raise OrchestratorError('source pins')
    if payload.get('feature_family') != FEATURE_FAMILY:
        raise OrchestratorError('source pins')
    if payload.get('category_slice_is_arm') is not False:
        raise CategorySliceNotAnArm()
    if payload.get('l2_cat_live_get_path_left_absent') is not True:
        raise OrchestratorError('source pins')
    if payload.get('admitted_at') is not None:
        raise OrchestratorError('source pins')
    books = payload.get('orderbooks')
    if not isinstance(books, list) or len(books) != MARKETS_N:
        raise OrchestratorError('source pins')
    expected = [
        {'file': filename, 'ticker': ticker, 'sha256': digest, 'bytes': size}
        for ticker, filename, digest, size in ORDERBOOK_PINS
    ]
    if books != expected:
        raise OrchestratorError('source pins')
    for key in OUTPUT_KEYS:
        if key not in payload or payload[key] is not None:
            raise ScorecardPromotionRefused()
    return payload


def conductor_pin_status():
    """Report whether checkout bytes match the attached conductor sha256 values."""
    freeze_match = sha256_file(PACKET) == FREEZE_SHA256
    parent_match = sha256_file(PARENT_FREEZE) == PARENT_SHA256
    panel_match = sha256_file(PANEL_STUB) == PANEL_STUB_SHA256
    books_match = True
    try:
        _assert_orderbook_copies()
    except OrchestratorError:
        books_match = False
    for digest in (FREEZE_SHA256, PARENT_SHA256, PANEL_STUB_SHA256):
        assert_not_superseded(digest)
    return {
        'freeze_matches_conductor_claim': freeze_match,
        'parent_freeze_matches_conductor_claim': parent_match,
        'panel_stub_matches_conductor_claim': panel_match,
        'orderbooks_match_conductor_claim': books_match,
        'conductor_bytes_in_checkout': all((
            freeze_match, parent_match, panel_match, books_match,
        )),
        'events_n': EVENTS_N,
        'markets_n': MARKETS_N,
        'sports_n': SPORTS_N,
        'nonsports_n': NONSPORTS_N,
        'admitted_at': None,
        'governance_tree_present': GOVERNANCE_TREE.is_dir(),
        'l2_cat_live_get_present': CLOSED_LIVE_GET.exists(),
    }


def _assert_authentic_bytes():
    _assert_owned(FREEZE_NAME, FREEZE_SHA256, packets_root=True)
    _assert_owned(PARENT_NAME, PARENT_SHA256, packets_root=True)
    _assert_owned(ACCEPT_NAME, CONDUCTOR_ACCEPT_SHA256, packets_root=True)
    _assert_owned(HOLD_NAME, EXAMINER_HOLD_SHA256, packets_root=True)
    _assert_owned(STAMP_NAME, CONDUCTOR_STAMP_SHA256, packets_root=False)
    _assert_owned(PRE_ACCEPT_NAME, PRE_ACCEPT_EMPTY_SHA256, packets_root=False)
    _assert_owned('panel_stub.json', PANEL_STUB_SHA256, packets_root=False)
    _assert_digest(PANEL_STUB, PANEL_STUB_SHA256)
    _assert_orderbook_copies()
    for directory in owned_dirs():
        path = directory / SOURCE_PINS_NAME
        _assert_digest(path, SOURCE_PINS_SHA256)
        _assert_source_pins(json.loads(path.read_text()))
    stamp = json.loads(CONDUCTOR_STAMP.read_text())
    if stamp.get('freeze_sha256') != FREEZE_SHA256:
        raise OrchestratorError('conductor stamp')
    if stamp.get('parent_freeze_sha256') != PARENT_SHA256:
        raise OrchestratorError('conductor stamp')
    if stamp.get('panel_stub_sha256') != PANEL_STUB_SHA256:
        raise OrchestratorError('conductor stamp')
    if stamp.get('arms') != list(ARMS):
        raise OrchestratorError('conductor stamp')
    if stamp.get('feature_family') != FEATURE_FAMILY:
        raise OrchestratorError('conductor stamp')
    if stamp.get('packet_id') != EXPERIMENT_ID:
        raise OrchestratorError('conductor stamp')
    if stamp.get('results') is not None or stamp.get('pnl') is not None:
        raise ScorecardPromotionRefused()
    accept = json.loads(CONDUCTOR_ACCEPT.read_text())
    if accept.get('status') != 'ACCEPT_IMPLEMENT_GO':
        raise OrchestratorError('conductor accept')
    if accept.get('freeze_sha256') != FREEZE_SHA256:
        raise OrchestratorError('conductor accept')
    if accept.get('knob') != KNOB:
        raise OrchestratorError('conductor accept')
    if accept.get('arm_values') != SHAPE_OBJECT:
        raise OrchestratorError('conductor accept')
    if accept.get('category_slice_is_arm') is not False:
        raise CategorySliceNotAnArm()
    if accept.get('l2_cat_reopen') is not False or accept.get('empty_ob_reopen') is not False:
        raise AdversaryRefused(ADVERSARY_LABELS['l2_cat_reopen'])
    if accept.get('does_not_ungate') != ['S2', 'R2-P4']:
        raise UngateRefused()
    if accept.get('post_empty_ob_main') != BASE_COMMIT:
        raise OrchestratorError('conductor accept')
    if accept.get('results') is not None or accept.get('pnl') is not None:
        raise ScorecardPromotionRefused()
    hold = json.loads(EXAMINER_HOLD.read_text())
    if hold.get('status') != 'NOT_SCORED' or hold.get('stub_ready') is not False:
        raise ExaminerNotReady()
    if hold.get('freeze_sha256') != FREEZE_SHA256:
        raise OrchestratorError('examiner hold')
    if sorted(hold.get('metrics_null') or []) != sorted(OUTPUT_KEYS):
        raise OrchestratorError('examiner hold')
    pre = json.loads(PRE_ACCEPT_EMPTY.read_text())
    if pre.get('note') != 'pre-ACCEPT empty':
        raise OrchestratorError('pre-accept empty')
    if 'n_books' in pre or 'n_snapshots' in pre:
        raise OrchestratorError('pre-accept empty')
    status = conductor_pin_status()
    if status['conductor_bytes_in_checkout'] is not True:
        raise OrchestratorError('conductor bytes')
    if status['governance_tree_present'] is not False:
        raise OrchestratorError('governance tree')
    if status['l2_cat_live_get_present'] is not False:
        raise OrchestratorError('l2-cat live_get path')


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
    orderbook = book.get('orderbook_fp')
    if not isinstance(orderbook, dict):
        raise EmptySeedRefused()
    side_status(orderbook)
    return ticker


def _validate_unadmitted_counts(payload, events, markets):
    summary = payload.get('cohort_summary') or {}
    if len(events) != EVENTS_N or len(markets) != MARKETS_N:
        if len(markets) == 0 or len(events) == 0:
            raise EmptySeedRefused()
        raise RecreationRefused()
    if summary.get('markets_seed_n') != MARKETS_N:
        raise RecreationRefused()
    if summary.get('sports_n') != SPORTS_N:
        raise RecreationRefused()
    if summary.get('non_sports_n') != NONSPORTS_N:
        raise RecreationRefused()
    if summary.get('events_n') != EVENTS_N:
        raise RecreationRefused()
    if summary.get('orderbook_ok_n') != MARKETS_N:
        raise RecreationRefused()
    event_tickers = tuple(event.get('event_ticker') for event in events)
    market_tickers = tuple(market.get('market_ticker') for market in markets)
    if event_tickers != STUB_EVENTS or market_tickers != STUB_MARKETS:
        raise RecreationRefused()
    sports_n = sum(1 for market in markets if market.get('category_slice') == 'sports')
    nonsports_n = sum(1 for market in markets if market.get('category_slice') == 'non_sports')
    if sports_n != SPORTS_N or nonsports_n != NONSPORTS_N:
        raise RecreationRefused()
    log = payload.get('http_seed_log') or []
    if len(log) != MARKETS_N:
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
    if payload.get('note') == 'pre-ACCEPT empty':
        raise PreAcceptEmptyRefused()
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
    if freeze_sha != PARENT_SHA256:
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
    elif tuple(market.get('market_ticker') for market in markets) != STUB_MARKETS:
        raise RecreationRefused()
    return payload


def load_panel(stub_path=None, admitted_path=None):
    """Stub by default. panel_admitted.json wins when it is on disk."""
    path = select_panel_path(stub_path, admitted_path)
    if path.resolve() == PANEL_STUB.resolve():
        _assert_authentic_bytes()
    payload = json.loads(path.read_text())
    return _validate_panel(payload, admitted=path.name == 'panel_admitted.json')


def load_orderbooks():
    """Read the pinned live_get copies. Does not open a socket."""
    _assert_orderbook_copies()
    directory = ROOT / LIVE_GET_DIRNAME
    rows = []
    for ticker, filename, digest, size in ORDERBOOK_PINS:
        path = directory / filename
        raw = path.read_bytes()
        payload = json.loads(raw)
        orderbook = payload['orderbook_fp']
        row = {
            'ticker': ticker,
            'file': filename,
            'sha256': digest,
            'bytes': size,
            'payload': payload,
            'orderbook_fp': orderbook,
            'depth_source': 'recorded_fixture',
        }
        row.update(side_status(orderbook))
        if len(raw) != size:
            raise OrchestratorError(filename)
        rows.append(row)
    return rows


def arm_table():
    return tuple({'id': arm, 'shape_object': SHAPE_OBJECT[arm]} for arm in ARMS)


def instrument_binding(panel=None):
    """One shape-object knob. Fee and rails commits stay fixed."""
    if panel is None:
        panel = load_panel()
    books = load_orderbooks()
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
    probe_quote = shape.quoted_yes(probe_book)
    probe_depth = shape.top10_depth(probe_book)
    if probe_quote['decile'] != 5 or probe_depth['l1_share'] != 1:
        raise OrchestratorError('shape import')
    if hygiene.FEEBOOK_COMMIT != FEEBOOK_COMMIT or hygiene.RAILS_COMMIT != RAILS_COMMIT:
        raise OrchestratorError('pin')
    if rails.FEE_CREDIT_RULE_ID != 'astra.r1p5.rails.maker_credit_floor_cent.v1':
        raise OrchestratorError('rails rule')
    observation = rails.BookObservation(
        rails.canonical_book_content({'schema': 'r3p4-sf-probe'}),
        't0',
    )
    verdict = rails.judge_freshness(None, observation)
    if not verdict.fresh:
        raise OrchestratorError('freshness')
    pins = conductor_pin_status()
    if pins['conductor_bytes_in_checkout'] is not True:
        raise OrchestratorError('conductor bytes')
    two_sided = sum(1 for row in books if row['two_sided'])
    one_sided = sum(1 for row in books if row['missing_side_not_invented'])
    if two_sided + one_sided != MARKETS_N or two_sided == 0:
        raise OrchestratorError('orderbooks')
    return {
        'experiment_id': EXPERIMENT_ID,
        'lab_directory': LAB_DIRECTORY,
        'feature_family': FEATURE_FAMILY,
        'knob': KNOB,
        'arms': arm_table(),
        'category_slice_is_arm': False,
        'panel_version': panel['panel_version'],
        'admitted_at': panel.get('admitted_at'),
        'events_n': len(panel.get('events') or []),
        'markets_n': len(panel.get('markets') or []),
        'recorded_orderbook_n': len(books),
        'two_sided_recorded_n': two_sided,
        'one_sided_recorded_n': one_sided,
        'strategy_pointer': None,
        'feebook_commit': FEEBOOK_COMMIT,
        'rails_commit': RAILS_COMMIT,
        'examiner_formula_id': feebook.EXAMINER_FORMULA_ID,
        'fee_credit_rule_id': rails.FEE_CREDIT_RULE_ID,
        'fee_source': 'feebook',
        'rails_source': 'rails',
        'shape_source': 'kalshi_r3_p4_l2_shape_lab_20260922',
        'fee_import_only': True,
        'rails_import_only': True,
        'fee_applied_to_books': False,
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
        'l2_cat_reopen': False,
        'empty_ob_reopen': False,
        'prop_lq_reopen': False,
        'sot_id_reopen': False,
        'pr13_dual_edit': False,
        's2_r2p4_ungated': False,
        'admit_py_run': False,
        'fee_is_knob': False,
        'examiner_status': 'NOT_SCORED',
        'stub_ready': False,
        'dead_cards': DEAD_CARDS,
        'scorecard_fields': SCORECARD_FIELDS,
        'freeze_sha256': FREEZE_SHA256,
        'parent_freeze_sha256': PARENT_SHA256,
        'panel_stub_sha256': PANEL_STUB_SHA256,
        'source_pins_sha256': SOURCE_PINS_SHA256,
        'conductor_stamp_sha256': CONDUCTOR_STAMP_SHA256,
        'conductor_bytes_in_checkout': True,
        'l2_cat_live_get_present': False,
        'governance_tree_present': False,
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
    scorecard['invented_depth'] = 'REFUSED'
    scorecard['examiner_status'] = 'NOT_SCORED'
    scorecard['stub_ready'] = False
    return scorecard


def assert_null_scorecard(payload):
    """Require every instrument field, results, and pnl, and require null."""
    if not isinstance(payload, dict):
        raise ScorecardPromotionRefused()
    if payload.get('note') == 'pre-ACCEPT empty':
        raise PreAcceptEmptyRefused()
    for key in OUTPUT_KEYS:
        if key not in payload or payload[key] is not None:
            raise ScorecardPromotionRefused()
    return payload


def load_scorecard(path):
    """Read a null scorecard. The pre-ACCEPT payload is refused."""
    path = Path(path)
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() == PRE_ACCEPT_EMPTY_SHA256:
        raise PreAcceptEmptyRefused()
    payload = json.loads(raw)
    if isinstance(payload, dict) and payload.get('note') == 'pre-ACCEPT empty':
        raise PreAcceptEmptyRefused()
    return assert_null_scorecard(payload)


def write_scorecard(payload):
    """Refuse a missing or non-null measurement field. Nothing is written."""
    assert_null_scorecard(payload)
    raise ScorecardPromotionRefused()


def _report(arm, source, extra):
    shape_name = _shape_name(arm)
    published = published_scorecard()
    report = {
        'experiment_id': EXPERIMENT_ID,
        'arm': arm,
        'shape_object': shape_name,
        'category_slice_is_arm': False,
        'source': source,
        'published': published,
        'promoted': False,
        'strategy_pointer': None,
        'live_orders': False,
        'lee_ready': 'REFUSED',
        'invented_depth': 'REFUSED',
        'fee_pin': FEEBOOK_COMMIT,
        'rails_pin': RAILS_COMMIT,
        'fee_import_only': True,
        'rails_import_only': True,
        'schema_scored': False,
        'production_depth_scored': False,
        's2_r2p4_ungated': False,
        'admit_py_run': False,
        'examiner_status': 'NOT_SCORED',
        'stub_ready': False,
    }
    report.update(extra)
    for key in OUTPUT_KEYS:
        report[key] = None
    assert_null_scorecard(report)
    assert_null_scorecard(published)
    return report


def conduct(arm, panel=None):
    """Select one shape object on the full natural panel. Scorecard stays null."""
    shape_name = _shape_name(arm)
    if panel is None:
        panel = load_panel()
    books = {row['ticker']: row for row in load_orderbooks()}
    if tuple(books) != STUB_MARKETS:
        raise OrchestratorError('orderbooks')
    slots = []
    for market in panel.get('markets') or []:
        ticker = market.get('market_ticker')
        recorded = books.get(ticker)
        if recorded is None:
            raise OrchestratorError('orderbooks')
        embedded = (market.get('raw_orderbook') or {}).get('orderbook_fp')
        if embedded != recorded['orderbook_fp']:
            raise OrchestratorError('orderbook drift')
        probe = schema_probe(arm, embedded)
        slot = {
            'market_ticker': ticker,
            'event_ticker': market.get('event_ticker'),
            'category_slice': market.get('category_slice'),
            'depth_source': 'recorded_fixture',
            'sha256': recorded['sha256'],
        }
        slot.update(probe)
        for key in OUTPUT_KEYS:
            if key in slot:
                raise ScorecardPromotionRefused()
        slots.append(slot)
    slices = {slot['category_slice'] for slot in slots}
    if slices != {'sports', 'non_sports'}:
        raise OrchestratorError('category seed')
    two_sided = sum(1 for slot in slots if slot['two_sided'])
    report = _report(arm, 'panel', {
        'event_count': len(panel.get('events') or []),
        'market_count': len(slots),
        'recorded_orderbook_n': len(slots),
        'two_sided_recorded_n': two_sided,
        'one_sided_recorded_n': len(slots) - two_sided,
        'markets': slots,
        'panel_note': 'recorded_books_not_promoted',
        'shape_object': shape_name,
    })
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


def schema_book(arm, row):
    """Selected algebra on one synthetic book. The scorecard is not written."""
    _shape_name(arm)
    if not isinstance(row, dict) or row.get('depth_source') != 'synthetic_schema_standin':
        raise InventedDepthRefused()
    if row.get('invent_depth') is True:
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
        raise OrchestratorError('category seed')
    orderbook = row.get('orderbook_fp')
    status = side_status(orderbook)
    if not status['two_sided']:
        raise InventedDepthRefused()
    current = shape.observation(orderbook, row.get('transaction_time'))
    shape.require_content_fresh(
        None, current, keepalive=bool(row.get('keepalive', False)),
    )
    probe = schema_probe(arm, orderbook)
    probe['book_id'] = book_id
    probe['category_slice'] = slice_value
    probe['schema_scored'] = True
    probe['production_depth'] = False
    return probe


def conduct_synthetic(arm, path=None):
    """In-memory algebra on the synthetic ladder. Scorecard fields stay null.

    Category labels stay on the rows. They do not filter the arm.
    """
    _shape_name(arm)
    books = load_synthetic_ladder(path)
    rows = [schema_book(arm, book) for book in books]
    slices = {row['category_slice'] for row in rows}
    if slices != {'sports', 'non_sports'}:
        raise OrchestratorError('category seed')
    report = _report(arm, 'synthetic_schema_standin', {
        'books': rows,
        'book_count': len(rows),
        'public_tape': False,
        'category_filtered': False,
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
