"""C1 EMPTY-OB harness.

Measurement only. One knob: empty_book_gate. Imports the R1-P1 feebook and
the R1-P5 rails. Hygiene content_fresh_flag is the rails freshness label.
This module does not edit those labs, does not place orders, does not read
Logan keys, does not run admit.py, and does not write scorecard metrics.

The checkout freeze, parent kernel, admitted panel, empty orderbooks, and
PIN_SHA256.json match the attached conductor sha256 values. All four books
are the same empty orderbook_fp. A labeled recreation and a filled-in book
are refused. Lee-Ready is refused. Depth and fills are not invented.
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
for _path in (FEEBOOK_DIR, RAILS_DIR):
    if str(_path) not in sys.path:
        sys.path.insert(0, str(_path))

import feebook
import rails

LAB_DIRECTORY = 'kalshi_c1_empty_ob_lab_20260923'
EXPERIMENT_ID = 'C1-EMPTY-OB-HARNESS'
FEATURE_FAMILY = 'EMPTY-OB'
PANEL_VERSION = '2026-09-22.c1-kxufcfight-v0'
ADMITTED_AT = '2026-09-23T00:49:43Z'
SERIES = 'KXUFCFIGHT'
SCHEMA_ID = 'astra.registry.c1_kxufcfight_panel.v0'
KNOB = 'empty_book_gate'
C1E0 = 'C1E0'
C1E1 = 'C1E1'
ARMS = (C1E0, C1E1)
GATES = {
    C1E0: 'refuse_scorecard',
    C1E1: 'wait_fresh_depth',
}
EVENTS_N = 2
MARKETS_N = 4
EVENT_TICKERS = (
    'KXUFCFIGHT-26SEP22CONGUA',
    'KXUFCFIGHT-26SEP22DEGMOR',
)
TICKERS = (
    'KXUFCFIGHT-26SEP22CONGUA-CON',
    'KXUFCFIGHT-26SEP22CONGUA-GUA',
    'KXUFCFIGHT-26SEP22DEGMOR-DEG',
    'KXUFCFIGHT-26SEP22DEGMOR-MOR',
)
FEEBOOK_COMMIT = '22371178cb2663250b4762f328069571c48cb551'
RAILS_COMMIT = '6a28e0d6254327ea4e6451c781bec56215ac6cac'
BASE_COMMIT = '6f1e22e15d8841605be5c34711f202277f4b685d'
FREEZE_SHA256 = '1b9f8fbec8bad866e055bcabd38c8c633835d505cbd25c367ff0675bff3a4b27'
PARENT_SHA256 = 'a191c9b3f71030445d1d32684feb6dc1bf09abb7e09403d5dbdf1927eafc63c9'
PANEL_SHA256 = '24426d804c51bde23cf2557a11a8481a12026da10024094c4ae546d1f7d3956e'
EMPTY_OB_SHA256 = 'e07d09f130e604a9e1acfc736fb57cbdfc33d8a5a253466a0cbd5c98cf6c9f74'
PIN_META_SHA256 = '241d745e6ddfb6cccdc8f123e4d57d627635065c3406df8f66d0d0d2e168f4ca'
CONDUCTOR_STAMP_SHA256 = '9adb8a8d30884abac8f4a82aafc0c2b57418a6f1e02341ff54bc46f2595456f5'
PRE_ACCEPT_EMPTY_SHA256 = 'b5ea41454dbb56be5456a2d9602304fcc249a2e3db8cba3cbb7e8eb7c080a4e1'
CONDUCTOR_ACCEPT_SHA256 = '2696b1e85e7f3329eaba0bdeaa8cd5ada6a52d1ebe0ff9d839fe80bb0a70e5a5'
EXAMINER_HOLD_SHA256 = '07deb88a91a65b6f4f7cea6bfd01a7169f5935fdcd698750d93a8d1a2f15b087'
EMPTY_OB_BYTES = 51
SCORECARD_FIELDS = (
    'empty_book_n',
    'scorecard_refuse_n',
    'wait_fresh_depth_n',
    'depth_present_n',
)
OUTPUT_KEYS = SCORECARD_FIELDS + ('results', 'pnl')
ADVERSARY_LABELS = {
    'lee_ready': 'Lee-Ready is refused',
    'invent_depth': 'invented depth is refused',
    'invented_depth': 'invented depth is refused',
    'invent_fills': 'invented fills are refused',
    'invented_fills': 'invented fills are refused',
    'invented_pnl': 'invented pnl is refused',
    'labeled_recreation': 'labeled recreation is refused',
    'pre_accept_empty': 'pre-ACCEPT empty payload is refused',
    'empty_pin_promotion': 'empty pin is not a scorecard',
    'admit_py': 'admit.py is refused',
    'poll_steal': 'ADMIT-1 poll steal is refused',
    's2_ungate': 'S2 ungate is refused',
    'r2p4_ungate': 'R2-P4 ungate is refused',
    'logan_keys': 'Logan keys are refused',
    'logan_key': 'Logan keys are refused',
    'live_orders': 'live orders are refused',
    'q6_retune': 'Q6-000 retune is refused',
    '000': 'Q6-000 retune is refused',
    'cap_sr_reopen': 'Cap-SR reopen is refused',
    'qf_reopen': 'queue-fragility reopen is refused',
    'l2_cat_reopen': 'L2-CAT reopen is refused',
    'prop_lq_reopen': 'PROP-LQ reopen is refused',
    'sot_id_reopen': 'SOT-ID reopen is refused',
    'examiner_ready': 'Examiner READY is not stamped before merge',
}
DEAD_CARDS = (
    'invent_depth',
    'invent_fills',
    'empty_pin_scorecard',
    'LeeReady_REFUSED',
    'Q6-000_retune_REFUSED',
    'Cap-SR_reopen_DENIED',
    'QF_reopen_DENIED',
    'L2-CAT_reopen_DENIED',
    'PROP-LQ_reopen_DENIED',
    'SOT-ID_reopen_DENIED',
    'S2_R2-P4_WAIT',
)
DOES_NOT_MODIFY = (
    'kalshi_feebook_lab_20260922',
    'kalshi_rails_lab_20260922',
    'kalshi_c1_kxufcfight_honesty_lab_20260922',
    'kalshi_r2p5_sot_id_lab_20260923',
    'kalshi_r3p4_l2_cat_lab_20260923',
    'kalshi_r3_p4_l2_shape_lab_20260922',
    'kalshi_r2p3_prop_ladder_lab_20260923',
    'kalshi_s4_ncaaf_feequue_lab_20260923',
    'kalshi_s5_mve_filllegs_lab_20260923',
    'kalshi_r3p3_fl_maker_taker_lab_20260923',
    'kalshi_c3_kxhighny_bordering_lab_20260923',
    'kalshi_c5_kxbtc15m_honesty_lab_20260923',
    'kalshi_soft_blended_reserves_000_lab_20260923',
    'kalshi_cap_sr_effects_000_lab_20260923',
    'kalshi_queue_fragility_000_lab_20260922',
    'kalshi_capital_structure_lab_20260922',
    'kalshi_examiner_fee_queue_honesty_000_lab_20260922',
    'kalshi_r2p1_hygiene_000_lab_20260922',
    'nfl_prospective_recorder_20260922',
    'nfl_factorial_lab_20260921',
    'nfl_paircheck_lab_20260922',
)
FREEZE_NAME = 'C1_EMPTY_OB_HARNESS_FREEZE_2026-09-23.md'
PARENT_NAME = 'C1_KXUFCFIGHT_MEASUREMENT_FREEZE_KERNEL_2026-09-22.md'
PANEL_NAME = 'C1_KXUFCFIGHT_PANEL_ADMITTED_2026-09-22.json'
PIN_NAME = 'PIN_SHA256.json'
STAMP_NAME = 'CONDUCTOR_FROZEN_EXPERIMENT.json'
PRE_ACCEPT_NAME = 'PRE_ACCEPT_EMPTY_RESULTS.json'
ACCEPT_NAME = 'CONDUCTOR_ACCEPT_C1_EMPTY_OB_HARNESS_2026-09-23.json'
HOLD_NAME = 'EXAMINER_HOLD_C1_EMPTY_OB_HARNESS_PRE_PR_2026-09-23.json'
LAB_BUNDLE = ROOT / 'C1_EMPTY_OB_HARNESS'
GOVERNANCE_BUNDLE = PARENT / 'packets' / 'C1_EMPTY_OB_HARNESS'
GOVERNANCE_TREE = PARENT / 'lab' / 'governance' / 'astra'
PACKET = ROOT / FREEZE_NAME
PARENT_FREEZE = ROOT / PARENT_NAME
PANEL_COPY = ROOT / PANEL_NAME
PIN_META = ROOT / PIN_NAME
CONDUCTOR_STAMP = ROOT / STAMP_NAME
PRE_ACCEPT_EMPTY = ROOT / PRE_ACCEPT_NAME
CONDUCTOR_ACCEPT = ROOT / ACCEPT_NAME
EXAMINER_HOLD = ROOT / HOLD_NAME
FROZEN_EXPERIMENT = ROOT / 'FROZEN_EXPERIMENT.json'
EMPTY_RESULTS = ROOT / 'results' / 'EMPTY_RESULTS.json'
SOURCE_PINS = ROOT / 'SOURCE_PINS.json'
PANEL_PRODUCTION = PARENT / 'lab' / 'astra-capture' / 'c1-kxufcfight' / 'panel_admitted.json'
PANEL_STUB = PARENT / 'lab' / 'astra-capture' / 'c1-kxufcfight' / 'panel_stub.json'
ORDERBOOK_PRODUCTION = PARENT / 'lab' / 'astra-capture' / 'c1-kxufcfight' / 'orderbooks'
BID_FIELDS = (
    'bid_yes',
    'bid_no',
    'ask_yes',
    'ask_no',
    'spread_yes',
    'spread_no',
    'touch_yes_size',
    'touch_no_size',
)


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
    """Lee-Ready has no success path."""

    def __init__(self):
        super().__init__('Lee-Ready refused')


class InventDepthRefused(OrchestratorError):
    """Empty bid lists stay empty."""

    def __init__(self):
        super().__init__(ADVERSARY_LABELS['invent_depth'])


class InventFillRefused(OrchestratorError):
    """No fill is created from an empty or pinned book."""

    def __init__(self):
        super().__init__(ADVERSARY_LABELS['invent_fills'])


class RecreationRefused(OrchestratorError):
    """A labeled recreation of the conductor bytes is refused."""

    def __init__(self):
        super().__init__(ADVERSARY_LABELS['labeled_recreation'])


class PreAcceptEmptyRefused(OrchestratorError):
    """The pre-ACCEPT payload is not the scorecard."""

    def __init__(self):
        super().__init__(ADVERSARY_LABELS['pre_accept_empty'])


class PanelStubRefused(OrchestratorError):
    """The pre-admit stub is not the subject."""

    def __init__(self):
        super().__init__('panel stub refused')


class PanelVersionRefused(OrchestratorError):
    """The panel is not the pinned C1 version."""

    def __init__(self):
        super().__init__('panel_version')


class PanelNotAdmitted(OrchestratorError):
    """admitted_at must be the pinned stamp."""

    def __init__(self):
        super().__init__('panel admitted_at')


class AdmitPyRefused(OrchestratorError):
    """admit.py is not run from this harness."""

    def __init__(self):
        super().__init__(ADVERSARY_LABELS['admit_py'])


class PollStealRefused(OrchestratorError):
    """ADMIT-1 and PIT@CLE poll budget stays put."""

    def __init__(self):
        super().__init__(ADVERSARY_LABELS['poll_steal'])


class UngateRefused(OrchestratorError):
    """S2 and R2-P4 stay queued."""

    def __init__(self):
        super().__init__('S2 and R2-P4 stay queued')


class UnknownGate(OrchestratorError):
    """The only knob is refuse_scorecard or wait_fresh_depth."""

    def __init__(self):
        super().__init__('empty_book_gate')


class ExaminerNotReady(OrchestratorError):
    """READY is not stamped from this implement pass."""

    def __init__(self):
        super().__init__(ADVERSARY_LABELS['examiner_ready'])


def _load_hygiene():
    spec = importlib.util.spec_from_file_location('c1_empty_ob_hygiene', HYGIENE_PATH)
    if spec is None or spec.loader is None:
        raise OrchestratorError('hygiene import')
    module = importlib.util.module_from_spec(spec)
    sys.modules['c1_empty_ob_hygiene'] = module
    spec.loader.exec_module(module)
    return module


hygiene = _load_hygiene()


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
    if label == 'lee_ready':
        raise LeeReadyRefused()
    if label in ('invent_depth', 'invented_depth'):
        raise InventDepthRefused()
    if label in ('invent_fills', 'invented_fills'):
        raise InventFillRefused()
    if label == 'labeled_recreation':
        raise RecreationRefused()
    if label == 'pre_accept_empty':
        raise PreAcceptEmptyRefused()
    if label == 'empty_pin_promotion':
        raise ScorecardPromotionRefused()
    if label == 'admit_py':
        raise AdmitPyRefused()
    if label == 'poll_steal':
        raise PollStealRefused()
    if label in ('s2_ungate', 'r2p4_ungate'):
        raise UngateRefused()
    if label == 'live_orders':
        raise LiveOrdersForbidden()
    if label == 'examiner_ready':
        raise ExaminerNotReady()
    raise AdversaryRefused(ADVERSARY_LABELS[label])


def infer_lee_ready(row):
    """Lee-Ready has no success path. Every input is refused."""
    if row is None or isinstance(row, (dict, str, int, float, list, tuple)):
        raise LeeReadyRefused()
    raise LeeReadyRefused()


def invent_depth(payload):
    """Does not add bids. The argument is not written back."""
    if payload is None or isinstance(payload, (dict, str, list, tuple)):
        raise InventDepthRefused()
    raise InventDepthRefused()


def attempt_fill(payload, taker_side=None, contracts=None):
    """Does not build a fill. Empty touch and present depth both stop here."""
    if payload is None or isinstance(payload, (dict, str)):
        raise InventFillRefused()
    if taker_side is None or contracts is None or taker_side is not None:
        raise InventFillRefused()
    raise InventFillRefused()


def ungate_s2_r2p4():
    """This packet does not ungate S2 or R2-P4."""
    raise UngateRefused()


def run_admit_py():
    """admit.py is not an entry point of this harness."""
    raise AdmitPyRefused()


def steal_poll():
    """The recorder poll budget stays on ADMIT-1."""
    raise PollStealRefused()


def fetch_over_network(url=None):
    """Books are the offline pin. This harness does not poll."""
    if url is None or isinstance(url, str):
        raise PollStealRefused()
    raise PollStealRefused()


def stamp_examiner_ready():
    """The pre-PR hold stays NOT_SCORED."""
    raise ExaminerNotReady()


def _lee_ready_requested(payload):
    if not isinstance(payload, dict):
        return False
    value = payload.get('lee_ready')
    if value is True:
        return True
    if isinstance(value, str) and value not in ('REFUSED',):
        return True
    inference = payload.get('aggressor_inference')
    if inference not in (None, 'REFUSED'):
        return True
    return False


def _labeled_recreation(payload):
    if not isinstance(payload, dict):
        return False
    if payload.get('recreation') is True or payload.get('labeled_recreation') is True:
        return True
    source = payload.get('source')
    if source in ('labeled_recreation', 'recreation'):
        return True
    note = payload.get('note')
    if isinstance(note, str) and 'recreation' in note.lower():
        return True
    return False


def _bid_lists(payload):
    if not isinstance(payload, dict):
        raise OrchestratorError('orderbook')
    if payload.get('results') is not None or payload.get('pnl') is not None:
        raise ScorecardPromotionRefused()
    wrapped = payload.get('orderbook_fp')
    if isinstance(wrapped, dict):
        yes = wrapped.get('yes_dollars')
        no = wrapped.get('no_dollars')
    else:
        book = payload.get('orderbook')
        if not isinstance(book, dict):
            raise OrchestratorError('orderbook')
        yes = book.get('yes')
        no = book.get('no')
    if not isinstance(yes, list) or not isinstance(no, list):
        raise OrchestratorError('orderbook')
    return yes, no


def book_is_empty(payload):
    """True when both bid lists are empty. Missing lists are an error."""
    yes, no = _bid_lists(payload)
    return len(yes) == 0 and len(no) == 0


def depth_present(payload):
    """True when either bid list has a level. Emptiness is not depth."""
    yes, no = _bid_lists(payload)
    return len(yes) > 0 or len(no) > 0


def assert_no_invented_depth(payload):
    """Feebook leaves asks unset when both bid lists are empty."""
    if not book_is_empty(payload):
        raise InventDepthRefused()
    book = feebook.reciprocal_book(payload)
    for key in BID_FIELDS:
        if book[key] is not None:
            raise InventDepthRefused()
    return book


def assert_empty_book_has_no_touch(payload):
    """An empty book has no touch. A returned fill would be an invention."""
    assert_no_invented_depth(payload)
    try:
        feebook.polarity_fill(payload, 'yes', '1', series=SERIES)
    except feebook.BookIncomplete:
        return None
    raise InventFillRefused()


def document_paths(name):
    return (
        ROOT / name,
        LAB_BUNDLE / name,
        PARENT / 'packets' / name,
        GOVERNANCE_BUNDLE / name,
    )


def orderbook_directories():
    return (
        ORDERBOOK_PRODUCTION,
        ROOT / 'orderbooks',
        LAB_BUNDLE / 'orderbooks',
        GOVERNANCE_BUNDLE / 'orderbooks',
    )


def _assert_copies(name, digest):
    for path in document_paths(name):
        if sha256_file(path) != digest:
            raise OrchestratorError(name)


def _assert_pin_meta(payload):
    if not isinstance(payload, dict):
        raise OrchestratorError('pin meta')
    if payload.get('empty_object_sha256') != EMPTY_OB_SHA256:
        raise OrchestratorError('pin meta')
    if payload.get('pnl') is not None or payload.get('results') is not None:
        raise ScorecardPromotionRefused()
    files = payload.get('files')
    if not isinstance(files, list) or len(files) != MARKETS_N:
        raise OrchestratorError('pin meta')
    names = []
    for row in files:
        if row.get('sha256') != EMPTY_OB_SHA256 or row.get('bytes') != EMPTY_OB_BYTES:
            raise OrchestratorError('pin meta')
        names.append(row.get('file'))
    if tuple(names) != tuple(ticker + '.json' for ticker in TICKERS):
        raise OrchestratorError('pin meta')
    return payload


def _assert_orderbook_copies():
    for directory in orderbook_directories():
        for ticker in TICKERS:
            path = directory / (ticker + '.json')
            raw = path.read_bytes()
            if len(raw) != EMPTY_OB_BYTES or hashlib.sha256(raw).hexdigest() != EMPTY_OB_SHA256:
                raise OrchestratorError('empty orderbook pin')


def _assert_source_pins(payload):
    if payload.get('freeze_sha256') != FREEZE_SHA256:
        raise OrchestratorError('source pins')
    if payload.get('parent_freeze_sha256') != PARENT_SHA256:
        raise OrchestratorError('source pins')
    if payload.get('panel_admitted_sha256') != PANEL_SHA256:
        raise OrchestratorError('source pins')
    if payload.get('empty_ob_pin_sha256') != EMPTY_OB_SHA256:
        raise OrchestratorError('source pins')
    if payload.get('pin_meta_sha256') != PIN_META_SHA256:
        raise OrchestratorError('source pins')
    if payload.get('results') is not None or payload.get('pnl') is not None:
        raise ScorecardPromotionRefused()
    for key in SCORECARD_FIELDS:
        if payload.get(key) is not None:
            raise ScorecardPromotionRefused()
    return payload


def conductor_pin_status():
    """Report whether checkout bytes match the attached conductor sha256 values."""
    freeze_match = sha256_file(PACKET) == FREEZE_SHA256
    parent_match = sha256_file(PARENT_FREEZE) == PARENT_SHA256
    panel_match = sha256_file(PANEL_COPY) == PANEL_SHA256 and sha256_file(PANEL_PRODUCTION) == PANEL_SHA256
    pin_match = sha256_file(PIN_META) == PIN_META_SHA256
    books_match = True
    try:
        _assert_orderbook_copies()
    except OrchestratorError:
        books_match = False
    return {
        'freeze_matches_conductor_claim': freeze_match,
        'parent_freeze_matches_conductor_claim': parent_match,
        'panel_matches_conductor_claim': panel_match,
        'pin_meta_matches_conductor_claim': pin_match,
        'empty_books_match_conductor_claim': books_match,
        'conductor_bytes_in_checkout': all((
            freeze_match, parent_match, panel_match, pin_match, books_match,
        )),
        'events_n': EVENTS_N,
        'markets_n': MARKETS_N,
        'admitted_at': ADMITTED_AT,
        'governance_tree_present': GOVERNANCE_TREE.is_dir(),
    }


def _assert_authentic_bytes():
    _assert_copies(FREEZE_NAME, FREEZE_SHA256)
    _assert_copies(PARENT_NAME, PARENT_SHA256)
    _assert_copies(PANEL_NAME, PANEL_SHA256)
    _assert_copies(PIN_NAME, PIN_META_SHA256)
    _assert_copies(STAMP_NAME, CONDUCTOR_STAMP_SHA256)
    _assert_copies(PRE_ACCEPT_NAME, PRE_ACCEPT_EMPTY_SHA256)
    _assert_copies(ACCEPT_NAME, CONDUCTOR_ACCEPT_SHA256)
    _assert_copies(HOLD_NAME, EXAMINER_HOLD_SHA256)
    if sha256_file(PANEL_PRODUCTION) != PANEL_SHA256:
        raise OrchestratorError('panel sha256')
    _assert_orderbook_copies()
    _assert_pin_meta(json.loads(PIN_META.read_text()))
    stamp = json.loads(CONDUCTOR_STAMP.read_text())
    if stamp.get('freeze_sha256') != FREEZE_SHA256:
        raise OrchestratorError('conductor stamp')
    if stamp.get('parent_freeze_sha256') != PARENT_SHA256:
        raise OrchestratorError('conductor stamp')
    if stamp.get('panel_admitted_sha256') != PANEL_SHA256:
        raise OrchestratorError('conductor stamp')
    if stamp.get('empty_ob_pin_sha256') != EMPTY_OB_SHA256:
        raise OrchestratorError('conductor stamp')
    if stamp.get('pin_meta_sha256') != PIN_META_SHA256:
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
    if accept.get('does_not_ungate') != ['S2', 'R2-P4']:
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
    for path in (SOURCE_PINS, LAB_BUNDLE / 'SOURCE_PINS.json', GOVERNANCE_BUNDLE / 'SOURCE_PINS.json'):
        _assert_source_pins(json.loads(path.read_text()))
    status = conductor_pin_status()
    if status['conductor_bytes_in_checkout'] is not True:
        raise OrchestratorError('conductor bytes')
    if status['governance_tree_present'] is not False:
        raise OrchestratorError('governance tree')


def _validate_panel(payload):
    if not isinstance(payload, dict):
        raise OrchestratorError('panel')
    if payload.get('note') == 'pre-ACCEPT empty':
        raise PreAcceptEmptyRefused()
    if _labeled_recreation(payload):
        raise RecreationRefused()
    if payload.get('schema_id') != SCHEMA_ID:
        raise OrchestratorError('schema')
    if payload.get('panel_version') != PANEL_VERSION:
        raise PanelVersionRefused()
    if payload.get('admitted_at') != ADMITTED_AT:
        raise PanelNotAdmitted()
    if payload.get('series_ticker') != SERIES:
        raise OrchestratorError('series')
    if payload.get('results') is not None or payload.get('pnl') is not None:
        raise ScorecardPromotionRefused()
    counts = payload.get('cohort_counts') or {}
    if counts.get('events_n') != EVENTS_N or counts.get('markets_n') != MARKETS_N:
        raise OrchestratorError('cohort')
    events = payload.get('events')
    markets = payload.get('markets')
    if not isinstance(events, list) or len(events) != EVENTS_N:
        raise OrchestratorError('events')
    if not isinstance(markets, list) or len(markets) != MARKETS_N:
        raise OrchestratorError('markets')
    event_tickers = []
    for event in events:
        if event.get('series_ticker') != SERIES:
            raise OrchestratorError('series')
        if event.get('volume_fp') is not None:
            raise ScorecardPromotionRefused()
        event_tickers.append(event.get('event_ticker'))
        listed = event.get('market_tickers')
        if not isinstance(listed, list) or len(listed) != 2:
            raise OrchestratorError('markets')
    if tuple(event_tickers) != EVENT_TICKERS:
        raise OrchestratorError('events')
    market_tickers = []
    for market in markets:
        if market.get('series_ticker') != SERIES:
            raise OrchestratorError('series')
        if market.get('panel_version') != PANEL_VERSION:
            raise PanelVersionRefused()
        if market.get('admitted_at') is not None:
            raise PanelNotAdmitted()
        for key in ('volume_fp', 'volume_24h_fp', 'open_interest_fp', 'content_fresh_flag'):
            if key in market and market[key] is not None:
                raise ScorecardPromotionRefused()
        market_tickers.append(market.get('market_ticker'))
    if tuple(sorted(market_tickers)) != tuple(sorted(TICKERS)):
        raise OrchestratorError('markets')
    binds = payload.get('binds') or {}
    if binds.get('fee_lab_sha') != FEEBOOK_COMMIT:
        raise OrchestratorError('feebook commit')
    if binds.get('rails_lab_sha') != RAILS_COMMIT:
        raise OrchestratorError('rails commit')
    if binds.get('fee_formula_id') != feebook.EXAMINER_FORMULA_ID:
        raise OrchestratorError('examiner formula')
    if binds.get('no_000_retune') is not True:
        raise AdversaryRefused(ADVERSARY_LABELS['q6_retune'])
    if binds.get('no_live_orders') is not True:
        raise LiveOrdersForbidden()
    capture = payload.get('capture') or {}
    if capture.get('mode') != 'GET_only_public':
        raise LiveOrdersForbidden()
    schedule = capture.get('schedule') or {}
    if schedule.get('admit_py_run') is True or schedule.get('recorder_started') is True:
        raise AdmitPyRefused()
    gate = payload.get('admit_gate') or {}
    if gate.get('admit_py_nfl_prospective') is True:
        raise AdmitPyRefused()
    return payload


def load_panel(path=None):
    """Admitted C1 panel. The stub and the pre-ACCEPT payload are refused."""
    path = PANEL_PRODUCTION if path is None else Path(path)
    if path.name == 'panel_stub.json' or path.resolve() == PANEL_STUB.resolve():
        raise PanelStubRefused()
    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if digest == PRE_ACCEPT_EMPTY_SHA256:
        raise PreAcceptEmptyRefused()
    canonical_names = {PANEL_PRODUCTION.resolve(), PANEL_COPY.resolve()}
    for copy in document_paths(PANEL_NAME):
        canonical_names.add(copy.resolve())
    if path.resolve() in canonical_names:
        _assert_authentic_bytes()
        if digest != PANEL_SHA256:
            raise OrchestratorError('panel sha256')
    payload = json.loads(raw)
    if isinstance(payload, dict) and payload.get('note') == 'pre-ACCEPT empty':
        raise PreAcceptEmptyRefused()
    return _validate_panel(payload)


def _canonical_book_dirs():
    return {directory.resolve() for directory in orderbook_directories()}


def load_orderbooks(directory=None):
    """Offline pinned books. Canonical directories must match the empty digest."""
    directory = ORDERBOOK_PRODUCTION if directory is None else Path(directory)
    canonical = directory.resolve() in _canonical_book_dirs()
    if canonical:
        _assert_authentic_bytes()
    rows = []
    for ticker in TICKERS:
        path = directory / (ticker + '.json')
        if not path.is_file():
            raise OrchestratorError('empty orderbook pin')
        raw = path.read_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        if canonical and (digest != EMPTY_OB_SHA256 or len(raw) != EMPTY_OB_BYTES):
            raise OrchestratorError('empty orderbook pin')
        payload = json.loads(raw)
        if _labeled_recreation(payload):
            raise RecreationRefused()
        if isinstance(payload, dict) and payload.get('note') == 'pre-ACCEPT empty':
            raise PreAcceptEmptyRefused()
        rows.append({
            'ticker': ticker,
            'sha256': digest,
            'payload': payload,
            'empty': book_is_empty(payload),
            'depth_present': depth_present(payload),
        })
    if canonical:
        for row in rows:
            if row['sha256'] != EMPTY_OB_SHA256 or not row['empty'] or row['depth_present']:
                raise InventDepthRefused()
    return rows


def _coerce_books(books):
    if books is None:
        return load_orderbooks()
    rows = []
    for row in books:
        if not isinstance(row, dict):
            raise OrchestratorError('orderbook')
        payload = row['payload'] if 'payload' in row else row
        if _labeled_recreation(payload):
            raise RecreationRefused()
        rows.append({
            'ticker': row.get('ticker'),
            'sha256': row.get('sha256'),
            'payload': payload,
            'empty': book_is_empty(payload),
            'depth_present': depth_present(payload),
        })
    return rows


def _observation(payload, transaction_time):
    return rails.BookObservation(
        content=rails.canonical_book_content(payload),
        transaction_time=transaction_time,
    )


def classify_wait(row, *, keepalive=False):
    """Wait bin for an empty book. Rails freshness is not depth and not a fill."""
    if not isinstance(row, dict) or 'payload' not in row:
        raise OrchestratorError('orderbook')
    payload = row['payload']
    if _lee_ready_requested(payload):
        raise LeeReadyRefused()
    if payload.get('fills') is not None:
        raise InventFillRefused()
    current = _observation(payload, row.get('ticker'))
    flag = hygiene.content_fresh_flag(None, current, keepalive=bool(keepalive))
    direct = rails.judge_freshness(None, current, keepalive=bool(keepalive))
    if flag['content_fresh_flag'] is not direct.fresh or flag['reason'] != direct.reason:
        raise OrchestratorError('content_fresh_flag')
    empty = book_is_empty(payload)
    present = depth_present(payload)
    if empty == present:
        raise OrchestratorError('orderbook')
    return {
        'ticker': row.get('ticker'),
        'bin': 'wait_fresh_depth' if empty else 'depth_present_unscored',
        'empty': empty,
        'depth_present': present,
        'content_fresh_flag': flag['content_fresh_flag'],
        'fresh_reason': flag['reason'],
        'freshness_is_not_depth': True,
        'fills': None,
        'lee_ready': 'REFUSED',
    }


def arm_table():
    return tuple({'id': arm, 'empty_book_gate': GATES[arm]} for arm in ARMS)


def instrument_binding(panel=None):
    """One empty-book gate. Fee and rails commits stay import-only."""
    if panel is None:
        panel = load_panel()
    books = load_orderbooks()
    quote = feebook.order_fee('taker', '1', '0.50', round_up=True, series=SERIES)
    if quote['formula_id'] != feebook.EXAMINER_FORMULA_ID:
        raise OrchestratorError('examiner formula')
    if quote['series_resolution'] != 'default_unknown_series':
        raise OrchestratorError('series resolution')
    if hygiene.FEEBOOK_COMMIT != FEEBOOK_COMMIT or hygiene.RAILS_COMMIT != RAILS_COMMIT:
        raise OrchestratorError('pin')
    pins = conductor_pin_status()
    return {
        'experiment_id': EXPERIMENT_ID,
        'lab_directory': LAB_DIRECTORY,
        'feature_family': FEATURE_FAMILY,
        'knob': KNOB,
        'arms': arm_table(),
        'panel_version': panel['panel_version'],
        'admitted_at': panel['admitted_at'],
        'events_n': EVENTS_N,
        'markets_n': MARKETS_N,
        'books_n': len(books),
        'books_all_empty': all(row['empty'] and not row['depth_present'] for row in books),
        'strategy_pointer': None,
        'feebook_commit': FEEBOOK_COMMIT,
        'rails_commit': RAILS_COMMIT,
        'examiner_formula_id': feebook.EXAMINER_FORMULA_ID,
        'fee_credit_rule_id': rails.FEE_CREDIT_RULE_ID,
        'fee_source': 'feebook',
        'rails_source': 'rails',
        'fee_import_only': True,
        'rails_import_only': True,
        'fee_applied_to_books': False,
        'probe_formula_id': quote['formula_id'],
        'probe_series_resolution': quote['series_resolution'],
        'probe_scorecard_write': False,
        'lee_ready': 'REFUSED',
        'labeled_recreation': 'REFUSED',
        'pre_accept_empty': 'REFUSED',
        's2_r2p4_ungated': False,
        'admit_py_run': False,
        'poll_steal': False,
        'logan_keys_required': False,
        'live_orders': False,
        'signal_retune_000': False,
        'cap_sr_reopen': False,
        'qf_reopen': False,
        'l2_cat_reopen': False,
        'prop_lq_reopen': False,
        'sot_id_reopen': False,
        'fee_is_knob': False,
        'examiner_status': 'NOT_SCORED',
        'stub_ready': False,
        'dead_cards': DEAD_CARDS,
        'scorecard_fields': SCORECARD_FIELDS,
        'freeze_sha256': FREEZE_SHA256,
        'parent_freeze_sha256': PARENT_SHA256,
        'panel_admitted_sha256': PANEL_SHA256,
        'empty_ob_pin_sha256': EMPTY_OB_SHA256,
        'pin_meta_sha256': PIN_META_SHA256,
        'conductor_bytes_in_checkout': pins['conductor_bytes_in_checkout'],
        'base_commit': BASE_COMMIT,
    }


def published_scorecard():
    """Freeze outputs. Every instrument field is present and null."""
    scorecard = {key: None for key in OUTPUT_KEYS}
    for key in OUTPUT_KEYS:
        if scorecard[key] is not None:
            raise ScorecardPromotionRefused()
    scorecard['status'] = 'EMPTY_RESULTS_PRE_EXAMINER'
    scorecard['lee_ready'] = 'REFUSED'
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


def _null_report(arm, extra):
    if arm not in GATES:
        raise UnknownGate()
    published = published_scorecard()
    report = {
        'experiment_id': EXPERIMENT_ID,
        'arm': arm,
        'empty_book_gate': GATES[arm],
        'published': published,
        'promoted': False,
        'strategy_pointer': None,
        'live_orders': False,
        'lee_ready': 'REFUSED',
        'fee_import_only': True,
        'rails_import_only': True,
        'fee_applied_to_books': False,
        'fee_pin': FEEBOOK_COMMIT,
        'rails_pin': RAILS_COMMIT,
        's2_r2p4_ungated': False,
        'admit_py_run': False,
        'poll_steal': False,
        'examiner_status': 'NOT_SCORED',
        'stub_ready': False,
    }
    report.update(extra)
    for key in OUTPUT_KEYS:
        report[key] = None
    assert_null_scorecard(report)
    assert_null_scorecard(published)
    return report


def conduct_refuse(books):
    """C1E0. Empty books refuse the scorecard. Lee-Ready and depth stay refused."""
    if not isinstance(books, list) or len(books) == 0:
        raise OrchestratorError('orderbooks')
    for row in books:
        payload = row['payload']
        if _lee_ready_requested(payload):
            raise LeeReadyRefused()
        if not row['empty'] or row['depth_present']:
            raise ScorecardPromotionRefused()
        assert_empty_book_has_no_touch(payload)
    raise ScorecardPromotionRefused()


def conduct_wait(books, *, keepalive=False):
    """C1E1. Empty books land in the wait bin. Counts and pnl stay null."""
    if not isinstance(books, list) or len(books) == 0:
        raise OrchestratorError('orderbooks')
    bins = [classify_wait(row, keepalive=keepalive) for row in books]
    for row in bins:
        for key in OUTPUT_KEYS:
            if key in row and row[key] is not None:
                raise ScorecardPromotionRefused()
        if row['fills'] is not None:
            raise InventFillRefused()
    return _null_report(C1E1, {
        'bins': bins,
        'book_count': len(bins),
        'all_empty': all(row['empty'] for row in bins),
        'keepalive': bool(keepalive),
    })


def conduct(arm, books=None, panel=None, keepalive=False):
    """Apply the one gate. C1E0 raises. C1E1 returns a null scorecard."""
    if arm not in GATES:
        raise UnknownGate()
    if panel is None:
        panel = load_panel()
    if panel.get('results') is not None or panel.get('pnl') is not None:
        raise ScorecardPromotionRefused()
    rows = _coerce_books(books)
    if arm == C1E0:
        return conduct_refuse(rows)
    return conduct_wait(rows, keepalive=keepalive)


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
        for key in OUTPUT_KEYS:
            if key not in payload or payload[key] is not None:
                raise ScorecardPromotionRefused()
            snapshot['%s.%s' % (name, key)] = None
    return snapshot
