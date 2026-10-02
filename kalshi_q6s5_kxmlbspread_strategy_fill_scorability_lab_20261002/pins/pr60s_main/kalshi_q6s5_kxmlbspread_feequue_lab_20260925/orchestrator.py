"""Q6S5 KXMLBSPREAD fee and queue honesty harness.

Measurement only. Series is KXMLBSPREAD. Feebook and rails stay at the
pinned commits and are imported, not edited. The series fee is the
cache-labeled quadratic multiplier pin. It is not a live R1-P1 /series
pin. This module does not place orders, does not read Logan keys, does not
open a network client, and does not write scorecard metrics.

The panel stub is the pinned 6-event / 12-market subset. Scout raw bytes
are cited and are not invented when they are absent. Lee-Ready is refused.
The NFL 000 path is a pointer only.
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

LAB_DIRECTORY = 'kalshi_q6s5_kxmlbspread_feequue_lab_20260925'
EXPERIMENT_ID = 'Q6S5-KXMLBSPREAD-FEEQUEUE-HARNESS'
FEATURE_FAMILY = 'Q6S5-MLBSPREAD-FEEQUEUE'
SERIES = 'KXMLBSPREAD'
FORBIDDEN_SERIES = 'KXMLBGAME'
SCHEMA_ID = 'astra.panel_stub.v0'
PANEL_VERSION = '2026-09-25.q6s5-kxmlbspread-v0'
COHORT_KIND = 'scout_screen_subset'
STUB_STATUS = 'NOT_ADMITTED'
PURPOSE = (
    'GET-only MLB spread fee+queue honesty harness seed from Scout sports '
    'Q6 screen KXMLBSPREAD raw markets (authentic subset)'
)
STUBBED_AT = '2026-09-25T00:15:00-04:00'
SCOUT_CITE = 'packets/scout_sports_q6_screen/raw/markets_open_KXMLBSPREAD.json'
SCOUT_SUMMARY_CITE = 'packets/scout_sports_q6_screen/raw/markets_open_KXMLBSPREAD_SUMMARY.json'
KNOB = 'analysis_slice'
Q6S5A0 = 'Q6S5A0'
Q6S5A1 = 'Q6S5A1'
ARMS = (Q6S5A0, Q6S5A1)
ANALYSIS_SLICE = {
    Q6S5A0: 'maker_vs_taker_native',
    Q6S5A1: 'content_fresh_vs_stale_bin',
}
FEEBOOK_COMMIT = '22371178cb2663250b4762f328069571c48cb551'
RAILS_COMMIT = '6a28e0d6254327ea4e6451c781bec56215ac6cac'
BASE_COMMIT = '1c5288b4c96fc5dc49ffd6c13ffd690767cadf6f'
FREEZE_SHA256 = '4f65dcdf536755b9f7dc2449c2dcd90b2df74cdf99a441b676f1a71c4d709c6e'
ACCEPT_SHA256 = '5adc42f9c9533238a2187aafe7593bdf1b8cdec6d12b8d3e9b12cb5ab29000fc'
PANEL_STUB_SHA256 = 'c7f1f1f4ca263838c4600ed46db8f525b68efc5399a567bd60929d18d76803cc'
SOURCE_PINS_SHA256 = '588fdbd0a293823cf96b66ace00145ad10f56efb40badc4b2007b5e4bc832fde'
FROZEN_EXPERIMENT_SHA256 = '55472bb9c6262f75f3e135456e4afbf3f2054b9ed8277cd082cfc4a987745b83'
EMPTY_RESULTS_SHA256 = '2b9421931ef40b8f283149ac1e488d05e40a3783d1d83bdf79da6d34498d0e12'
HOLD_SHA256 = '57bbd3ddf8e99fe790eb827f3167f529528f0a30ae27ece1ff909617b2091aa8'
TEMPLATE_V12_SHA256 = '56bcf6269a42031d9d90496e9a65c2292321aed2165033f6fb44ff8cc4d6b1cc'
SCOUT_MARKETS_SHA256 = '80b52f47c836248d5869806d7f59617535e6b78258367ebe6045af4275fff7e7'
SCOUT_SUMMARY_SHA256 = 'c9e871b3c4edbc648972f9313b3bbcd6784efc46ca847e1f0de4c2847ce85ebe'
PANEL_EVENTS_N = 6
PANEL_MARKETS_N = 12
SOURCE_EVENTS_N = 15
SOURCE_MARKETS_N = 93
FEE_TYPE = 'quadratic'
FEE_MULTIPLIER = '0.5'
FEE_LABEL = 'CACHE-LABELED'
PUBLIC_HOST = 'https://api.elections.kalshi.com/trade-api/v2'
NFL_000_POINTER = 'nfl_factorial_lab_20260921/SHADOW_CANDIDATE_FREEZE.json'
NFL_POINTER_SERIES = 'KXNFLGAME'
FEEBOOK_PIN = 'kalshi_feebook_lab_20260922/@22371178cb2663250b4762f328069571c48cb551'
RAILS_PIN = 'kalshi_rails_lab_20260922/@6a28e0d6254327ea4e6451c781bec56215ac6cac'
SCORECARD_FIELDS = (
    'maker_vs_taker_roi_delta',
    'fresh_vs_stale_gap',
    'settled_join_n',
    'n_books',
)
OUTPUT_KEYS = SCORECARD_FIELDS + ('results', 'pnl')
COMMON_SCORECARD_KEYS = (
    'net_pnl_without_rewards',
    'net_pnl_with_rewards',
    'rewards_actually_earned',
    'calibration',
    'fill_rate',
    'adverse_selection_after_fills',
    'feasible_vs_requested_size',
    'unresolved_inventory',
    'capital_hours',
    'drawdown',
    'event_concentration',
)
PUBLIC_TAKER_FIELDS = ('taker_outcome_side', 'taker_book_side', 'taker_side')
BOOK_TO_OUTCOME = {'bid': 'yes', 'ask': 'no'}
PANEL_RULES = (
    'measurement_only',
    'GET_only',
    'no_Logan_keys',
    'no_invent_depth_fills_pnl',
    'results_pnl_null',
    'does_not_ungate_S1_S2',
    'not_KXMLBGAME_ML_retune',
    'fee_cache_quadratic_x0.5_not_live_R1P1_until_Examiner',
)
COHORT_SUMMARY = {
    'events_n': PANEL_EVENTS_N,
    'markets_n': PANEL_MARKETS_N,
    'source_markets_n': SOURCE_MARKETS_N,
    'source_events_n': SOURCE_EVENTS_N,
}
DOES_NOT_UNGATE = (
    'S1_KXMLBGAME_ML',
    'S2',
    'R2-P4',
    'Card06_open_window',
    'Q6-000_retune',
    'Cap-SR',
)
UNGATE_ALIASES = {
    'S1': 'S1_KXMLBGAME_ML',
    'KXMLBGAME': 'S1_KXMLBGAME_ML',
    'Card 06': 'Card06_open_window',
    'Q6-000': 'Q6-000_retune',
}
FEE_LITERAL_KEYS = ('fee', 'fee_cost', 'fee_dollars', 'maker_fee', 'taker_fee')
FILL_DENSITY_KEYS = ('fill_density', 'fills_per_hour', 'invented_fill_density')
DEPTH_KEYS = (
    'orderbook_fp',
    'yes_bid_size_fp',
    'yes_ask_size_fp',
    'no_bid_size_fp',
    'depth',
)
ADVERSARY_LABELS = {
    'lee_ready': 'Lee-Ready is refused on every input',
    'live_orders': 'live orders are refused',
    'logan_keys': 'Logan keys are refused',
    'invented_pnl': 'invented pnl is refused',
    'invented_fills': 'invented fills are refused',
    'invented_fill_density': 'invented fill density is refused',
    'invented_occurrence_datetime': 'invented occurrence_datetime is refused',
    'invented_depth': 'invented depth is refused',
    'invented_markets': 'invented markets are refused',
    'q6_retune': 'Q6-000 retune is refused',
    '000': 'Q6-000 retune is refused',
    'qf_reopen': 'queue-fragility reopen is refused',
    'cap_sr_reopen': 'Cap-SR reopen is refused',
    'cap_sr_fx_reopen': 'Cap-SR-FX reopen is refused',
    'l2_reopen': 'L2 reopen is refused',
    'l2_cat_reopen': 'L2-CAT reopen is refused',
    'l2_sf_reopen': 'L2-SF reopen is refused',
    'empty_ob_reopen': 'EMPTY-OB reopen is refused',
    'sot_id_reopen': 'SOT-ID reopen is refused',
    'kxmlbgame_ml_retune': 'KXMLBGAME ML retune is refused',
    'card06_reopen': 'Card 06 open-window reopen is refused',
    'dual_cloud': 'dual-cloud is refused',
    'admit_py': 'admit.py is refused',
    'claim_s1_green': 'S1 green is not claimed',
    'signal_port': 'NFL 000 signal port is refused',
    'claim_live_r1p1': 'cache fee is not live R1-P1',
}
DOES_NOT_MODIFY = (
    'kalshi_feebook_lab_20260922',
    'kalshi_rails_lab_20260922',
    'kalshi_r2p1_hygiene_000_lab_20260922',
    'kalshi_queue_fragility_000_lab_20260922',
    'kalshi_soft_blended_reserves_000_lab_20260923',
    'kalshi_cap_sr_effects_000_lab_20260923',
    'kalshi_c1_kxufcfight_honesty_lab_20260922',
    'kalshi_c1_empty_ob_lab_20260923',
    'kalshi_c2_kxnhlgame_feequue_lab_20260923',
    'kalshi_c4_kxcpi_feequue_lab_20260923',
    'kalshi_atp_kxatpmatch_feequue_lab_20260923',
    'kalshi_s4_ncaaf_feequue_lab_20260923',
    'nfl_factorial_lab_20260921',
    'nfl_paircheck_lab_20260922',
)
FREEZE_NAME = 'Q6S5_KXMLBSPREAD_FEEQUEUE_HARNESS_FREEZE_2026-09-25.md'
ACCEPT_NAME = 'CONDUCTOR_ACCEPT_Q6S5_KXMLBSPREAD_FEEQUEUE_HARNESS_2026-09-25.json'
HOLD_NAME = 'EXAMINER_HOLD_Q6S5_KXMLBSPREAD_FEEQUEUE_HARNESS_PRE_PR_2026-09-25.json'
SOURCE_PINS_NAME = 'SOURCE_PINS.json'
SCORECARD_JSON_NAME = (
    'EXAMINER_SCORECARD_STUB_Q6S5_KXMLBSPREAD_FEEQUEUE_HARNESS_2026-09-25.json'
)
SCORECARD_MD_NAME = (
    'EXAMINER_SCORECARD_STUB_Q6S5_KXMLBSPREAD_FEEQUEUE_HARNESS_2026-09-25.md'
)
PACKET = ROOT / FREEZE_NAME
LAB_BUNDLE = ROOT / 'Q6S5_KXMLBSPREAD_FEEQUEUE_HARNESS'
GOVERNANCE = PARENT / 'lab' / 'governance' / 'astra' / 'packets'
GOVERNANCE_BUNDLE = GOVERNANCE / 'Q6S5_KXMLBSPREAD_FEEQUEUE_HARNESS'
FROZEN_EXPERIMENT = ROOT / 'FROZEN_EXPERIMENT.json'
EMPTY_RESULTS = ROOT / 'results' / 'EMPTY_RESULTS.json'
SOURCE_PINS = ROOT / SOURCE_PINS_NAME
CONDUCTOR_ACCEPT = ROOT / ACCEPT_NAME
EXAMINER_HOLD = ROOT / HOLD_NAME
PANEL_STUB = PARENT / 'lab' / 'astra-capture' / 'q6s5-kxmlbspread' / 'panel_stub.json'
PANEL_ADMITTED = PARENT / 'lab' / 'astra-capture' / 'q6s5-kxmlbspread' / 'panel_admitted.json'
NFL_POINTER_PATH = PARENT / NFL_000_POINTER
P16_CHECKLIST = ROOT / 'p16_preregistration_checklist.json'
SYNTHETIC_TRADES = ROOT / 'fixtures' / 'synthetic_native_trades.json'
SYNTHETIC_FRESH = ROOT / 'fixtures' / 'synthetic_fresh_queue.json'
TEMPLATE_V12 = (
    PARENT / 'lab' / 'governance' / 'astra' / 'templates'
    / 'EXAMINER_KALSHI_SCORECARD_TEMPLATE_v1.2.json'
)
CLAIMED_PINS = (
    ('conductor_accept', ACCEPT_SHA256, 'lab/governance/astra/packets/' + ACCEPT_NAME),
    ('freeze', FREEZE_SHA256, 'lab/governance/astra/packets/' + FREEZE_NAME),
    ('panel_stub', PANEL_STUB_SHA256, 'lab/astra-capture/q6s5-kxmlbspread/panel_stub.json'),
    (
        'sports_screen_freeze',
        '552314d2822f86bf4127be5de03b8d64aa8c16d6c0c81887bdc0cfbd411571df',
        'lab/governance/astra/packets/scout_sports_q6_screen/FREEZE_SPORTS_Q6_SCREEN_2026-09-24.md',
    ),
    (
        'sports_screen_accept',
        '2aefbc1712a0389d65f565439d5599a7275688e872e8bc67d5c6dde3b1cd81f8',
        'lab/governance/astra/packets/CONDUCTOR_ACCEPT_SPORTS_Q6_SCREEN_2026-09-24.json',
    ),
    (
        'kick',
        '9c68ab12f6f5561ee176c5669b17ef40c4f5be20299687823ad7f0e9b67701c8',
        'lab/governance/astra/packets/CONDUCTOR_KICK_VARIANTS_Q6S5_KXMLBSPREAD_FEEQUEUE_FREEZE_2026-09-25.json',
    ),
    ('scout_markets', SCOUT_MARKETS_SHA256, SCOUT_CITE),
    ('scout_summary', SCOUT_SUMMARY_SHA256, SCOUT_SUMMARY_CITE),
    (
        'frozen_experiment',
        FROZEN_EXPERIMENT_SHA256,
        'lab/governance/astra/packets/Q6S5_KXMLBSPREAD_FEEQUEUE_HARNESS/FROZEN_EXPERIMENT.json',
    ),
    (
        'empty_results',
        EMPTY_RESULTS_SHA256,
        'lab/governance/astra/packets/Q6S5_KXMLBSPREAD_FEEQUEUE_HARNESS/EMPTY_RESULTS.json',
    ),
    (
        'capture_plan',
        'b7ab235ebf4baf198cca2c48103395c611b0f99c36640b17f442ca2f0d377814',
        'lab/governance/astra/packets/Q6S5_KXMLBSPREAD_CAPTURE_PLAN_2026-09-25.md',
    ),
    (
        'scorecard_template_v1_2',
        TEMPLATE_V12_SHA256,
        'lab/governance/astra/templates/EXAMINER_KALSHI_SCORECARD_TEMPLATE_v1.2.json',
    ),
    (
        'scorecard_template_v1_2_md',
        'ad1dd2834652b8e9be331ddf2f3ec900ea587efb042251fde6452532b2e36394',
        'lab/governance/astra/templates/EXAMINER_KALSHI_SCORECARD_TEMPLATE_v1.2.md',
    ),
    (
        'p16_pdf',
        '7e55bc260526aa5088ee31f74475851219ab2cd7f19fdd2f0dd5e9f998c8b45e',
        'lab/governance/astra/research/KALSHI_EDGE_RESEARCH_2026-09-24.pdf',
    ),
    (
        'maximize_pin',
        '917ec545c0dc1cca5c32a3cdf9da0615d09b3871d782dbd4b8ee57ac733b83b9',
        'lab/governance/astra/packets/MAXIMIZE_PIN_2026-09-25_0022ET.md',
    ),
    ('examiner_hold', HOLD_SHA256, 'lab/governance/astra/packets/' + HOLD_NAME),
    (
        'variants_accept_ping',
        'bdbe46edbf04b985c907f8690afe736bd66a5e8de4e69d6594f7117b9363221f',
        'lab/governance/astra/packets/VARIANTS_ACCEPT_PING_Q6S5_KXMLBSPREAD_FEEQUEUE_HARNESS_2026-09-25.json',
    ),
    (
        'scorecard_stub_md',
        '4b33ecceebf6383073ecb260b319778ca37c1b8c7e46d64c09a91137d7116957',
        'lab/governance/astra/packets/Q6S5_KXMLBSPREAD_FEEQUEUE_HARNESS/' + SCORECARD_MD_NAME,
    ),
    (
        'scorecard_stub_json',
        '4da3c3709ffb8783c8e4b2117581d722789e132cf142d151c7ee7bfa15949926',
        'lab/governance/astra/packets/Q6S5_KXMLBSPREAD_FEEQUEUE_HARNESS/' + SCORECARD_JSON_NAME,
    ),
    (
        'source_pins',
        SOURCE_PINS_SHA256,
        'lab/governance/astra/packets/Q6S5_KXMLBSPREAD_FEEQUEUE_HARNESS/SOURCE_PINS.json',
    ),
    (
        'digests',
        'ecd6f9e04bba99c41f0fefcb93c9f047776ee7e8c3e80f97bb08845e284c7d8c',
        'lab/governance/astra/packets/Q6S5_KXMLBSPREAD_FEEQUEUE_HARNESS/DIGESTS.txt',
    ),
    (
        'freeze_digest',
        '982d6bc1e5fb2c43ceb797487b6bcbcafccab698a171283d6c9e5fc793267257',
        'lab/governance/astra/packets/Q6S5_KXMLBSPREAD_FEEQUEUE_FREEZE_DIGEST_2026-09-25.json',
    ),
    (
        'archivist_ping',
        '80ed8dd1bfce3316d5a7086d3ca52fc0dd68bfe2ca777545a1e92e0ffbe8119a',
        'lab/governance/astra/packets/VARIANTS_ARCHIVIST_REGISTRY_PING_Q6S5_KXMLBSPREAD_FEEQUEUE_HARNESS_2026-09-25.json',
    ),
    (
        'feebook_commit_file',
        '4b6686fabcfa246291104333bbe1299ab9623543d6c420778f5fc0fcfb3637a6',
        'pins/feebook_commit.txt',
    ),
    (
        'feebook_source_pins',
        '0db29e296af1b81af64720af26606bd8b193d2ea8fd95ec37d7a83594d1a733a',
        'pins/feebook_SOURCE_PINS.json',
    ),
    (
        'rails_commit_file',
        '6fda6f36c6843e435a685c821d8630b2f977e84b10a4cf54dbdba74199d70fde',
        'pins/rails_commit.txt',
    ),
    (
        'rails_source_pins',
        '78d97a2085fbd826c1312da86131f23a3dc3a4345cccb301d924a97675496c9a',
        'pins/rails_SOURCE_PINS.json',
    ),
)
_PANEL_INDEX = None


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


class SignalPortRefused(OrchestratorError):
    """The NFL 000 file is a pointer. No signal is read from it."""

    def __init__(self):
        super().__init__('NFL 000 signal port refused')


class S1GreenClaimRefused(OrchestratorError):
    """This packet does not claim S1 green."""

    def __init__(self):
        super().__init__('S1 green is not claimed')


class UngateRefused(OrchestratorError):
    """S1 KXMLBGAME ML, S2, R2-P4, Card 06, Q6-000, and Cap-SR stay closed."""

    def __init__(self):
        super().__init__('does not ungate S1 KXMLBGAME ML S2 R2-P4')


class KXMLBGameRetuneRefused(OrchestratorError):
    """KXMLBGAME moneyline retune is forbidden."""

    def __init__(self):
        super().__init__('KXMLBGAME ML retune refused')


class CacheNotLiveR1P1(OrchestratorError):
    """The cache fee label is not a live /series R1-P1 pin."""

    def __init__(self):
        super().__init__('cache fee is not live R1-P1')


class ExaminerNotReady(OrchestratorError):
    """Examiner stays HOLD_PRE_PR until after merge and Clock admit."""

    def __init__(self):
        super().__init__('Examiner HOLD_PRE_PR')


class TakerFieldRefused(OrchestratorError):
    """Native taker fields are missing or disagree."""

    def __init__(self, reason):
        super().__init__(reason)


class PanelVersionRefused(OrchestratorError):
    """The panel file is not the pinned KXMLBSPREAD seed."""

    def __init__(self):
        super().__init__('panel_version')


class ShadowFeeLiteralRefused(OrchestratorError):
    """A fee quote bypassed the cache label."""

    def __init__(self):
        super().__init__('shadow fee literal')


class InventedFillRefused(OrchestratorError):
    """A fill, settlement, or inventory value was invented."""

    def __init__(self):
        super().__init__('invented fill')


class InventedFillDensityRefused(OrchestratorError):
    """Fill density is not derived from the public tape."""

    def __init__(self):
        super().__init__('invented fill density')


class InventedSoTRefused(OrchestratorError):
    """occurrence_datetime is not invented when the source omits it."""

    def __init__(self):
        super().__init__('invented occurrence_datetime')


class InventedDepthRefused(OrchestratorError):
    """Depth was requested from a market quote or a fabricated ladder."""

    def __init__(self):
        super().__init__('invented depth')


class InventedMarketRefused(OrchestratorError):
    """A market is outside the pinned panel stub."""

    def __init__(self):
        super().__init__('invented market')


class UnknownSlice(OrchestratorError):
    """The only knob is the two named analysis slices."""

    def __init__(self):
        super().__init__('analysis_slice')


def _load_hygiene():
    spec = importlib.util.spec_from_file_location('q6s5_kxmlbspread_hygiene', HYGIENE_PATH)
    if spec is None or spec.loader is None:
        raise OrchestratorError('hygiene import')
    module = importlib.util.module_from_spec(spec)
    sys.modules['q6s5_kxmlbspread_hygiene'] = module
    spec.loader.exec_module(module)
    return module


hygiene = _load_hygiene()


def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def execution_adapter():
    """No live order client lives in this lab."""
    raise LiveOrdersForbidden()


def _normalize_public_path(path):
    if not isinstance(path, str) or not path:
        raise OrchestratorError('path')
    if path.startswith('http://') or path.startswith('https://'):
        if not path.startswith(PUBLIC_HOST + '/') and path != PUBLIC_HOST:
            raise OrchestratorError('host')
        path = path[len(PUBLIC_HOST):] or '/'
    if not path.startswith('/'):
        path = '/' + path
    lowered = path.lower()
    if '/orders' in lowered or '/portfolio' in lowered:
        raise LiveOrdersForbidden()
    if FORBIDDEN_SERIES in path and SERIES not in path:
        raise KXMLBGameRetuneRefused()
    return path


class StubTransport:
    """In-memory GET stand-in. live_gets stays 0. No network client is opened."""

    def __init__(self, bodies=None, markets_hot=False):
        self.bodies = {} if bodies is None else dict(bodies)
        self.markets_hot = bool(markets_hot)
        self.calls = []
        self.live_gets = 0

    def request(self, method, path):
        if method != 'GET':
            raise LiveOrdersForbidden()
        normalized = _normalize_public_path(path)
        self.calls.append(('GET', normalized))
        chosen = normalized
        preferred = None
        if self.markets_hot and (
            normalized == '/markets' or normalized.startswith('/markets?')
        ):
            chosen = '/events' + normalized[len('/markets'):]
            preferred = 'markets_hot'
            self.calls.append(('GET', chosen))
        if self.live_gets != 0:
            raise LiveOrdersForbidden()
        return {
            'method': 'GET',
            'path': chosen,
            'requested': normalized,
            'preferred_because': preferred,
            'body': self.bodies.get(chosen),
            'live': False,
            'live_gets': self.live_gets,
            'host': PUBLIC_HOST,
        }


def public_get(path, transport=None):
    """GET through the stub transport. The default transport performs no live GET."""
    if transport is None:
        transport = StubTransport()
    return transport.request('GET', path)


def assert_public_get(method):
    """GET is the only public capture verb. This function does not open a network client."""
    if method != 'GET':
        raise LiveOrdersForbidden()
    return None


def port_nfl_000_signal(payload=None):
    """Pointer only. Every read of a 000 signal is refused."""
    del payload
    raise SignalPortRefused()


def claim_s1_green():
    """S1 KXMLBGAME ML stays forbidden. This packet does not claim it green."""
    raise S1GreenClaimRefused()


def ungate(name):
    """Named closed cards stay closed."""
    target = UNGATE_ALIASES.get(name, name)
    if target in DOES_NOT_UNGATE or name in DOES_NOT_UNGATE:
        raise UngateRefused()
    raise OrchestratorError('ungate')


def quote_depth(market):
    """Public size fields are not a depth ladder and are not n_books."""
    del market
    raise InventedDepthRefused()


def assign_fill_density(market, value=None):
    """Public volume is not rewritten as a fill density."""
    del market, value
    raise InventedFillDensityRefused()


def assign_occurrence(market, value=None):
    """A missing occurrence_datetime stays missing."""
    del market, value
    raise InventedSoTRefused()


def settled_join(panel):
    """No settlement join is published. The metric stays null."""
    if not isinstance(panel, dict):
        raise OrchestratorError('panel')
    if panel.get('results') is not None or panel.get('pnl') is not None:
        raise InventedFillRefused()
    return None


def claim_live_r1p1(quote=None):
    """Refuse every promotion of the cache label to a live /series pin."""
    del quote
    raise CacheNotLiveR1P1()


def promote_series_fee(quote):
    """An examiner formula quote is not the KXMLBSPREAD series pin."""
    del quote
    raise CacheNotLiveR1P1()


def fee_output(series=SERIES):
    """Cache-labeled quadratic fee. Every fee output sets cache_labeled true.

    No dollar fee is returned. results and pnl stay null.
    """
    if series == FORBIDDEN_SERIES or (
        isinstance(series, str) and series.startswith(FORBIDDEN_SERIES)
    ):
        raise KXMLBGameRetuneRefused()
    if series != SERIES:
        raise OrchestratorError('series')
    label = {
        'series': SERIES,
        'fee_type': FEE_TYPE,
        'multiplier': FEE_MULTIPLIER,
        'label': FEE_LABEL,
        'cache_labeled': True,
        'live_r1p1': False,
        'examiner_formula_used_as_series_pin': False,
        'fee_source': 'cache',
        'fee_dollars': None,
        'results': None,
        'pnl': None,
    }
    if label['cache_labeled'] is not True:
        raise CacheNotLiveR1P1()
    if label['live_r1p1'] is not False:
        raise CacheNotLiveR1P1()
    if label['series'] != SERIES:
        raise OrchestratorError('series')
    return label


def refuse_adversary(label):
    """Named refuse labels. Nothing is traded."""
    if label not in ADVERSARY_LABELS:
        raise OrchestratorError('adversary label')
    if label == 'lee_ready':
        raise LeeReadyRefused()
    if label == 'signal_port':
        raise SignalPortRefused()
    if label == 'invented_depth':
        raise InventedDepthRefused()
    if label == 'invented_markets':
        raise InventedMarketRefused()
    if label == 'invented_fill_density':
        raise InventedFillDensityRefused()
    if label == 'invented_occurrence_datetime':
        raise InventedSoTRefused()
    if label == 'claim_s1_green':
        raise S1GreenClaimRefused()
    if label == 'kxmlbgame_ml_retune':
        raise KXMLBGameRetuneRefused()
    if label == 'claim_live_r1p1':
        raise CacheNotLiveR1P1()
    raise AdversaryRefused(ADVERSARY_LABELS[label])


def infer_lee_ready(row):
    """Lee-Ready has no success path. Every input is refused."""
    del row
    raise LeeReadyRefused()


def _lee_ready_requested(row):
    value = row.get('lee_ready')
    if value is True:
        return True
    if isinstance(value, str) and value not in ('REFUSED',):
        return True
    classifier = row.get('classifier')
    if isinstance(classifier, str) and classifier.lower().replace('_', '-') in (
        'lee-ready',
        'leeready',
    ):
        return True
    if row.get('aggressor_inference') is not None:
        return True
    return False


def _agree(current, value):
    if current is None:
        return value
    if current != value:
        raise TakerFieldRefused('taker_* fields disagree')
    return current


def _refuse_fee_literal(row):
    for key in FEE_LITERAL_KEYS:
        if key in row and row[key] is not None:
            raise ShadowFeeLiteralRefused()


def _refuse_depth_keys(row):
    for key in DEPTH_KEYS:
        if key in row and row[key] is not None:
            raise InventedDepthRefused()


def _refuse_fill_density(row):
    if row.get('invent_fill_density') is True:
        raise InventedFillDensityRefused()
    for key in FILL_DENSITY_KEYS:
        if key in row and row[key] is not None:
            raise InventedFillDensityRefused()


def _refuse_series_ticker(row):
    ticker = row.get('ticker')
    if isinstance(ticker, str) and (
        ticker.startswith(FORBIDDEN_SERIES + '-') or ticker.startswith(FORBIDDEN_SERIES)
    ):
        raise KXMLBGameRetuneRefused()
    if isinstance(ticker, str) and ticker in panel_market_index()['by_ticker']:
        raise InventedFillRefused()


def _occurrence_state(row):
    if not isinstance(row, dict):
        raise OrchestratorError('occurrence')
    if 'occurrence_datetime' not in row:
        return 'missing'
    occ = row.get('occurrence_datetime')
    if occ is None:
        return 'missing'
    if isinstance(occ, str) and len(occ) >= 20 and 'T' in occ and occ.endswith('Z'):
        return 'present'
    raise InventedSoTRefused()


def occurrence_census(markets):
    """Count missing and present occurrence fields. Does not fill either."""
    if not isinstance(markets, list):
        raise OrchestratorError('markets')
    missing = 0
    present = 0
    for market in markets:
        state = _occurrence_state(market)
        if state == 'missing':
            missing += 1
        else:
            present += 1
    return {
        'missing_occurrence_datetime_n': missing,
        'present_occurrence_datetime_n': present,
    }


def _assert_event_occurrence(event, markets_for_event):
    states = [_occurrence_state(market) for market in markets_for_event]
    if any(state == 'missing' for state in states):
        if not all(state == 'missing' for state in states):
            raise OrchestratorError('occurrence disagreement')
        if event.get('occurrence_datetime') is not None:
            raise InventedSoTRefused()
        return
    values = {market.get('occurrence_datetime') for market in markets_for_event}
    if len(values) != 1:
        raise OrchestratorError('occurrence disagreement')
    expected = values.pop()
    if event.get('occurrence_datetime') != expected:
        raise InventedSoTRefused()


def classify_native_taker(row):
    """Partition from native taker_* fields. Lee-Ready does not vote."""
    if not isinstance(row, dict):
        raise OrchestratorError('row')
    if _lee_ready_requested(row):
        raise LeeReadyRefused()
    _refuse_fee_literal(row)
    _refuse_depth_keys(row)
    _refuse_fill_density(row)
    _refuse_series_ticker(row)
    if row.get('invent_occurrence_datetime') is True or 'occurrence_datetime' in row:
        raise InventedSoTRefused()
    unknown = [
        key for key in row
        if key.startswith('taker_') and key not in PUBLIC_TAKER_FIELDS and row.get(key) is not None
    ]
    if unknown:
        raise TakerFieldRefused('unknown taker_* field')
    outcome = None
    present = []
    if row.get('taker_outcome_side') is not None:
        side = row['taker_outcome_side']
        if side not in ('yes', 'no'):
            raise TakerFieldRefused('taker_outcome_side')
        outcome = _agree(outcome, side)
        present.append('taker_outcome_side')
    if row.get('taker_book_side') is not None:
        book = row['taker_book_side']
        if book not in BOOK_TO_OUTCOME:
            raise TakerFieldRefused('taker_book_side')
        outcome = _agree(outcome, BOOK_TO_OUTCOME[book])
        present.append('taker_book_side')
    if row.get('taker_side') is not None:
        side = row['taker_side']
        if side not in ('yes', 'no'):
            raise TakerFieldRefused('taker_side')
        outcome = _agree(outcome, side)
        present.append('taker_side')
    if outcome is None:
        raise TakerFieldRefused('native public taker_* field required')
    if row.get('result') not in (None, ''):
        raise InventedFillRefused()
    if row.get('settlement_ts') is not None:
        raise InventedFillRefused()
    for key in OUTPUT_KEYS:
        if key in row and row[key] is not None:
            raise ScorecardPromotionRefused()
    return {
        'taker_outcome_side': outcome,
        'taker_book_side': 'bid' if outcome == 'yes' else 'ask',
        'maker_outcome_side': feebook.TAKER_FILLS_RESTING[outcome],
        'native_fields': present,
        'classification': 'native_public_taker',
        'lee_ready': 'REFUSED',
        'aggressor_inference': None,
        'series': SERIES,
    }


def _observation(payload, transaction_time):
    if payload is None:
        return None
    if not isinstance(payload, dict):
        raise OrchestratorError('book')
    return rails.BookObservation(
        content=rails.canonical_book_content(payload),
        transaction_time=transaction_time,
    )


def classify_fresh_queue(row):
    """Bin on rails content-fresh and queue attribution. Taker fields do not vote."""
    if not isinstance(row, dict):
        raise OrchestratorError('row')
    if _lee_ready_requested(row):
        raise LeeReadyRefused()
    _refuse_fee_literal(row)
    _refuse_depth_keys(row)
    _refuse_fill_density(row)
    _refuse_series_ticker(row)
    if row.get('invent_occurrence_datetime') is True or 'occurrence_datetime' in row:
        raise InventedSoTRefused()
    if row.get('result') not in (None, ''):
        raise InventedFillRefused()
    for key in OUTPUT_KEYS:
        if key in row and row[key] is not None:
            raise ScorecardPromotionRefused()
    if 'queue_ahead' not in row:
        raise OrchestratorError('queue_ahead')
    previous = _observation(row.get('previous'), row.get('previous_transaction_time'))
    current = _observation(row.get('current'), row.get('transaction_time'))
    if current is None:
        raise OrchestratorError('current book')
    flag = hygiene.content_fresh_flag(
        previous,
        current,
        keepalive=bool(row.get('keepalive')),
    )
    queue_bin = hygiene.queue_attribution_bin(row['queue_ahead'])
    return {
        'row_id': row.get('row_id'),
        'content_fresh_flag': flag['content_fresh_flag'],
        'fresh_reason': flag['reason'],
        'queue_attribution_bin': queue_bin,
        'lee_ready': 'REFUSED',
        'fresh_vs_stale_gap': None,
        'series': SERIES,
    }


def _scorecard_row(row):
    for key in OUTPUT_KEYS:
        row[key] = None
    return row


def partition_native(trades):
    """Group by native taker outcome. ROI stays null. Lee-Ready stays refused."""
    if not isinstance(trades, list) or not trades:
        raise OrchestratorError('trades')
    grouped = {}
    for trade in trades:
        classified = classify_native_taker(trade)
        key = (classified['taker_outcome_side'], classified['taker_book_side'])
        grouped.setdefault(key, []).append(trade.get('trade_id'))
    rows = []
    for outcome, book in sorted(grouped):
        row = {
            'taker_outcome_side': outcome,
            'taker_book_side': book,
            'maker_outcome_side': feebook.TAKER_FILLS_RESTING[outcome],
            'trade_n': len(grouped[(outcome, book)]),
            'trade_ids': grouped[(outcome, book)],
            'lee_ready': 'REFUSED',
            'aggressor_inference': None,
            'maker_vs_taker_roi_delta': None,
            'series': SERIES,
        }
        rows.append(_scorecard_row(row))
    return rows


def partition_fresh(rows):
    """Group by content-fresh flag and queue bin. The gap stays null."""
    if not isinstance(rows, list) or not rows:
        raise OrchestratorError('rows')
    grouped = {}
    for row in rows:
        classified = classify_fresh_queue(row)
        key = (classified['content_fresh_flag'], classified['queue_attribution_bin'])
        grouped.setdefault(key, []).append(classified['row_id'])
    out = []
    for flag, queue_bin in sorted(grouped, key=lambda item: (str(item[0]), item[1])):
        packed = {
            'content_fresh_flag': flag,
            'queue_attribution_bin': queue_bin,
            'row_n': len(grouped[(flag, queue_bin)]),
            'row_ids': grouped[(flag, queue_bin)],
            'lee_ready': 'REFUSED',
            'fresh_vs_stale_gap': None,
            'series': SERIES,
        }
        out.append(_scorecard_row(packed))
    return out


def owned_dirs():
    return (ROOT, LAB_BUNDLE)


def source_pin_paths():
    return (
        GOVERNANCE_BUNDLE / SOURCE_PINS_NAME,
        ROOT / SOURCE_PINS_NAME,
        LAB_BUNDLE / SOURCE_PINS_NAME,
    )


def _assert_digest(path, digest):
    raw = Path(path).read_bytes()
    if hashlib.sha256(raw).hexdigest() != digest:
        raise OrchestratorError(str(path))
    return raw


def digest_status(pin_specs=None):
    """Re-hash every claimed pin. True only when every pin is present and matches."""
    specs = CLAIMED_PINS if pin_specs is None else tuple(pin_specs)
    rows = []
    for key, digest, rel in specs:
        path = PARENT / rel
        if not path.is_file():
            rows.append({
                'key': key,
                'present': False,
                'match': False,
                'path': rel,
            })
            continue
        actual = sha256_file(path)
        rows.append({
            'key': key,
            'present': True,
            'match': actual == digest,
            'path': rel,
        })
    claimed = bool(rows) and all(row['match'] for row in rows)
    return {
        'pins': rows,
        'digest_all_match_claimed': claimed is True and all(row['match'] for row in rows),
        'missing': [row['key'] for row in rows if not row['present']],
        'mismatch': [row['key'] for row in rows if row['present'] and not row['match']],
    }


def _assert_source_pins(payload):
    if payload.get('freeze_sha256') != FREEZE_SHA256:
        raise OrchestratorError('source pins')
    if payload.get('panel_stub_sha256') != PANEL_STUB_SHA256:
        raise OrchestratorError('source pins')
    if payload.get('scout_markets_sha256') != SCOUT_MARKETS_SHA256:
        raise OrchestratorError('source pins')
    if payload.get('scout_summary_sha256') != SCOUT_SUMMARY_SHA256:
        raise OrchestratorError('source pins')
    if payload.get('series_ticker') != SERIES:
        raise OrchestratorError('source pins')
    if payload.get('feature_family') != FEATURE_FAMILY:
        raise OrchestratorError('source pins')
    if payload.get('packet_id') != EXPERIMENT_ID:
        raise OrchestratorError('source pins')
    if payload.get('lab_dir') != LAB_DIRECTORY + '/':
        raise OrchestratorError('source pins')
    if payload.get('panel_version') != PANEL_VERSION:
        raise OrchestratorError('source pins')
    if payload.get('panel_events_n') != PANEL_EVENTS_N:
        raise OrchestratorError('source pins')
    if payload.get('panel_markets_n') != PANEL_MARKETS_N:
        raise OrchestratorError('source pins')
    if payload.get('source_events_n') != SOURCE_EVENTS_N:
        raise OrchestratorError('source pins')
    if payload.get('source_markets_n') != SOURCE_MARKETS_N:
        raise OrchestratorError('source pins')
    if payload.get('feebook_pin') != FEEBOOK_COMMIT or payload.get('rails_pin') != RAILS_COMMIT:
        raise OrchestratorError('source pins')
    fee = payload.get('fee_cache') or {}
    if fee.get('fee_type') != FEE_TYPE or fee.get('label') != FEE_LABEL:
        raise OrchestratorError('source pins')
    if fee.get('multiplier') != 0.5:
        raise OrchestratorError('source pins')
    if payload.get('admitted_at') is not None:
        raise OrchestratorError('source pins')
    if payload.get('examiner_scorecard_template_v1_2_sha256') != TEMPLATE_V12_SHA256:
        raise OrchestratorError('source pins')
    for key in ('results', 'pnl'):
        if key not in payload or payload[key] is not None:
            raise ScorecardPromotionRefused()
    return payload


def _assert_authentic_bytes():
    _assert_digest(GOVERNANCE / FREEZE_NAME, FREEZE_SHA256)
    _assert_digest(PACKET, FREEZE_SHA256)
    _assert_digest(LAB_BUNDLE / FREEZE_NAME, FREEZE_SHA256)
    _assert_digest(PANEL_STUB, PANEL_STUB_SHA256)
    _assert_digest(ROOT / 'panel_stub.json', PANEL_STUB_SHA256)
    _assert_digest(LAB_BUNDLE / 'panel_stub.json', PANEL_STUB_SHA256)
    _assert_digest(GOVERNANCE / ACCEPT_NAME, ACCEPT_SHA256)
    _assert_digest(CONDUCTOR_ACCEPT, ACCEPT_SHA256)
    _assert_digest(LAB_BUNDLE / ACCEPT_NAME, ACCEPT_SHA256)
    _assert_digest(GOVERNANCE / HOLD_NAME, HOLD_SHA256)
    _assert_digest(EXAMINER_HOLD, HOLD_SHA256)
    _assert_digest(LAB_BUNDLE / HOLD_NAME, HOLD_SHA256)
    _assert_digest(GOVERNANCE_BUNDLE / 'FROZEN_EXPERIMENT.json', FROZEN_EXPERIMENT_SHA256)
    _assert_digest(FROZEN_EXPERIMENT, FROZEN_EXPERIMENT_SHA256)
    _assert_digest(LAB_BUNDLE / 'FROZEN_EXPERIMENT.json', FROZEN_EXPERIMENT_SHA256)
    _assert_digest(GOVERNANCE_BUNDLE / 'EMPTY_RESULTS.json', EMPTY_RESULTS_SHA256)
    _assert_digest(EMPTY_RESULTS, EMPTY_RESULTS_SHA256)
    _assert_digest(LAB_BUNDLE / 'results.json', EMPTY_RESULTS_SHA256)
    _assert_digest(LAB_BUNDLE / 'results' / 'EMPTY_RESULTS.json', EMPTY_RESULTS_SHA256)
    canonical_pins = None
    for path in source_pin_paths():
        raw = _assert_digest(path, SOURCE_PINS_SHA256)
        if canonical_pins is None:
            canonical_pins = raw
        elif raw != canonical_pins:
            raise OrchestratorError('source pins')
        _assert_source_pins(json.loads(raw))
    _assert_digest(TEMPLATE_V12, TEMPLATE_V12_SHA256)
    accept = json.loads(CONDUCTOR_ACCEPT.read_text())
    if accept.get('status') != 'ACCEPT_IMPLEMENT_GO':
        raise OrchestratorError('conductor accept')
    if accept.get('series') != SERIES or accept.get('packet_id') != EXPERIMENT_ID:
        raise OrchestratorError('conductor accept')
    if accept.get('feature_family') != FEATURE_FAMILY:
        raise OrchestratorError('conductor accept')
    if accept.get('freeze_sha256') != FREEZE_SHA256:
        raise OrchestratorError('conductor accept')
    if accept.get('panel_stub_sha256') != PANEL_STUB_SHA256:
        raise OrchestratorError('conductor accept')
    if accept.get('implement') is not True or accept.get('dual_cloud') is not False:
        raise OrchestratorError('conductor accept')
    if accept.get('admitted_at') is not None:
        raise OrchestratorError('conductor accept')
    if accept.get('results') is not None or accept.get('pnl') is not None:
        raise ScorecardPromotionRefused()
    if accept.get('arms') != list(ARMS) or accept.get('arm_values') != ANALYSIS_SLICE:
        raise OrchestratorError('conductor accept')
    if accept.get('knob') != KNOB or accept.get('lab_dir') != LAB_DIRECTORY + '/':
        raise OrchestratorError('conductor accept')
    if accept.get('panel_events') != PANEL_EVENTS_N or accept.get('panel_markets') != PANEL_MARKETS_N:
        raise OrchestratorError('conductor accept')
    if accept.get('does_not_ungate') != list(DOES_NOT_UNGATE):
        raise UngateRefused()
    fee = accept.get('fee_cache') or {}
    if fee.get('fee_type') != FEE_TYPE or fee.get('label') != FEE_LABEL:
        raise OrchestratorError('conductor accept')
    if fee.get('not_live_R1_P1') is not True:
        raise CacheNotLiveR1P1()
    hold = json.loads(EXAMINER_HOLD.read_text())
    if hold.get('status') != 'HOLD_PRE_PR' or hold.get('stub_ready') is not False:
        raise ExaminerNotReady()
    if hold.get('packet') != EXPERIMENT_ID or hold.get('feature_family') != FEATURE_FAMILY:
        raise OrchestratorError('examiner hold')
    if sorted(hold.get('metrics_null') or []) != sorted(OUTPUT_KEYS):
        raise OrchestratorError('examiner hold')
    if hold.get('admitted_at') is not None:
        raise OrchestratorError('examiner hold')
    assert_v12_null(hold.get('examiner_scorecard_v1_2'))
    frozen = json.loads(FROZEN_EXPERIMENT.read_text())
    if frozen.get('status') != 'FROZEN' or frozen.get('series_ticker') != SERIES:
        raise OrchestratorError('frozen')
    if frozen.get('knob') != KNOB or frozen.get('arms') != list(ARMS):
        raise OrchestratorError('frozen')
    if frozen.get('arm_values') != ANALYSIS_SLICE:
        raise OrchestratorError('frozen')
    for key in OUTPUT_KEYS:
        if key not in frozen or frozen[key] is not None:
            raise ScorecardPromotionRefused()
    checklist = frozen.get('p16_preregistration_checklist') or {}
    counts = checklist.get('counts') or {}
    if counts.get('satisfied') != 8 or counts.get('n/a') != 4 or counts.get('missing') != 0:
        raise OrchestratorError('p16')
    if len(checklist.get('items') or []) != 12:
        raise OrchestratorError('p16')
    on_disk = json.loads(P16_CHECKLIST.read_text())
    if on_disk != checklist:
        raise OrchestratorError('p16')
    empty = json.loads(EMPTY_RESULTS.read_text())
    assert_null_scorecard(empty)
    assert_v12_null(empty.get('examiner_scorecard_v1_2'))


def select_panel_path(stub_path=None, admitted_path=None):
    """Prefer panel_admitted.json when the file exists. Otherwise the stub."""
    stub_path = PANEL_STUB if stub_path is None else Path(stub_path)
    admitted_path = PANEL_ADMITTED if admitted_path is None else Path(admitted_path)
    if Path(admitted_path).is_file():
        return Path(admitted_path)
    if not Path(stub_path).is_file():
        raise OrchestratorError('panel stub')
    return Path(stub_path)


def panel_market_index():
    """Pinned stub markets. Does not invent the 93-market scout raw file."""
    global _PANEL_INDEX
    if _PANEL_INDEX is not None:
        return _PANEL_INDEX
    payload = json.loads(_assert_digest(PANEL_STUB, PANEL_STUB_SHA256))
    markets = payload.get('markets')
    if not isinstance(markets, list) or len(markets) != PANEL_MARKETS_N:
        raise OrchestratorError('panel markets')
    by_ticker = {}
    events = set()
    for market in markets:
        ticker = market.get('ticker')
        event = market.get('event_ticker')
        if not isinstance(ticker, str) or not ticker.startswith(SERIES + '-'):
            raise InventedMarketRefused()
        if FORBIDDEN_SERIES in ticker:
            raise KXMLBGameRetuneRefused()
        if ticker in by_ticker:
            raise OrchestratorError('duplicate ticker')
        if not isinstance(event, str) or not event.startswith(SERIES + '-'):
            raise InventedMarketRefused()
        if market.get('status') != 'active' or market.get('result') != '':
            raise OrchestratorError('panel market')
        if 'orderbook_fp' in market:
            raise InventedDepthRefused()
        by_ticker[ticker] = market
        events.add(event)
    if len(events) != PANEL_EVENTS_N:
        raise OrchestratorError('panel events')
    _PANEL_INDEX = {'by_ticker': by_ticker, 'events': events}
    return _PANEL_INDEX


def _assert_market_object(market, index):
    if not isinstance(market, dict):
        raise OrchestratorError('market')
    ticker = market.get('ticker')
    if isinstance(ticker, str) and ticker.startswith(FORBIDDEN_SERIES):
        raise KXMLBGameRetuneRefused()
    if ticker not in index['by_ticker']:
        raise InventedMarketRefused()
    if market != index['by_ticker'][ticker]:
        raise InventedMarketRefused()
    if market.get('result') != '':
        raise InventedFillRefused()
    if market.get('status') != 'active':
        raise OrchestratorError('market status')
    if 'orderbook_fp' in market:
        raise InventedDepthRefused()
    return ticker


def _validate_panel(payload, admitted):
    if not isinstance(payload, dict):
        raise OrchestratorError('panel')
    if payload.get('panel_version') != PANEL_VERSION:
        raise PanelVersionRefused()
    if payload.get('packet_id') != EXPERIMENT_ID:
        raise OrchestratorError('packet')
    if payload.get('schema_id') != SCHEMA_ID:
        raise OrchestratorError('schema')
    if payload.get('series_ticker') != SERIES:
        raise OrchestratorError('series')
    if payload.get('cohort_kind') != COHORT_KIND:
        raise OrchestratorError('cohort')
    if payload.get('scout_cite') != SCOUT_CITE:
        raise OrchestratorError('scout cite')
    if payload.get('scout_sha256') != SCOUT_MARKETS_SHA256:
        raise OrchestratorError('scout sha')
    if payload.get('scout_summary_cite') != SCOUT_SUMMARY_CITE:
        raise OrchestratorError('scout summary cite')
    if list(payload.get('rules') or []) != list(PANEL_RULES):
        raise OrchestratorError('rules')
    if payload.get('cohort_summary') != COHORT_SUMMARY:
        raise OrchestratorError('cohort summary')
    stamp = payload.get('admitted_at')
    if admitted:
        if not isinstance(stamp, str) or not stamp.endswith('Z'):
            raise OrchestratorError('admitted_at')
    elif stamp is not None:
        raise OrchestratorError('admitted_at')
    if not admitted:
        if payload.get('stub_status') != STUB_STATUS:
            raise OrchestratorError('stub_status')
        if payload.get('purpose') != PURPOSE:
            raise OrchestratorError('purpose')
        if payload.get('stubbed_at_et') != STUBBED_AT:
            raise OrchestratorError('stubbed_at')
    for key in ('results', 'pnl'):
        if key not in payload or payload[key] is not None:
            raise InventedFillRefused()
    index = panel_market_index()
    events = payload.get('events')
    markets = payload.get('markets')
    if not isinstance(events, list) or len(events) != PANEL_EVENTS_N:
        raise OrchestratorError('events')
    if not isinstance(markets, list) or len(markets) != PANEL_MARKETS_N:
        raise OrchestratorError('markets')
    seen = []
    event_names = []
    for event in events:
        if not isinstance(event, dict):
            raise OrchestratorError('events')
        name = event.get('event_ticker')
        if name not in index['events']:
            raise InventedMarketRefused()
        if event.get('markets_n') != 2:
            raise OrchestratorError('event markets')
        event_names.append(name)
    if len(set(event_names)) != PANEL_EVENTS_N:
        raise OrchestratorError('events')
    for market in markets:
        seen.append(_assert_market_object(market, index))
    if len(set(seen)) != PANEL_MARKETS_N:
        raise OrchestratorError('markets')
    picked = []
    for row in (payload.get('subset_selection') or {}).get('rows') or []:
        picked.extend(row.get('picked_tickers') or [])
    if picked != seen:
        raise InventedMarketRefused()
    by_event = {}
    for market in markets:
        by_event.setdefault(market.get('event_ticker'), []).append(market)
    for event in events:
        name = event.get('event_ticker')
        group = by_event.get(name) or []
        if len(group) != 2:
            raise InventedMarketRefused()
        _assert_event_occurrence(event, group)
    census = occurrence_census(markets)
    if census['missing_occurrence_datetime_n'] != 0:
        raise OrchestratorError('occurrence census')
    if census['present_occurrence_datetime_n'] != PANEL_MARKETS_N:
        raise OrchestratorError('occurrence census')
    return payload


def load_panel(stub_path=None, admitted_path=None):
    """Stub by default. panel_admitted.json wins when it is on disk."""
    path = select_panel_path(stub_path, admitted_path)
    if path.resolve() == PANEL_STUB.resolve():
        _assert_authentic_bytes()
    payload = json.loads(path.read_text())
    return _validate_panel(payload, admitted=path.name == 'panel_admitted.json')


def arm_table():
    return tuple({'id': arm, 'analysis_slice': ANALYSIS_SLICE[arm]} for arm in ARMS)


def instrument_binding(panel=None):
    """One slice knob. Fee cache and rails commits stay fixed. No scorecard fill."""
    if panel is None:
        panel = load_panel()
    label = fee_output(SERIES)
    if hygiene.FEEBOOK_COMMIT != FEEBOOK_COMMIT or hygiene.RAILS_COMMIT != RAILS_COMMIT:
        raise OrchestratorError('pin')
    ahead_bin = hygiene.queue_attribution_bin(rails.QUEUE_AHEAD_DEFAULT)
    if ahead_bin != 'q3300':
        raise OrchestratorError('queue bin')
    if not NFL_POINTER_PATH.is_file():
        raise OrchestratorError('nfl 000 pointer')
    pins = digest_status()
    census = occurrence_census(panel.get('markets') or [])
    scout_path = PARENT / SCOUT_CITE
    return {
        'experiment_id': EXPERIMENT_ID,
        'lab_directory': LAB_DIRECTORY,
        'feature_family': FEATURE_FAMILY,
        'knob': KNOB,
        'arms': arm_table(),
        'panel_version': panel['panel_version'],
        'admitted_at': panel.get('admitted_at'),
        'series_ticker': SERIES,
        'events_n': len(panel.get('events') or []),
        'markets_n': len(panel.get('markets') or []),
        'source_markets_n': SOURCE_MARKETS_N,
        'source_events_n': SOURCE_EVENTS_N,
        'scout_raw_present': scout_path.is_file(),
        'panel_subset_of_scout': True,
        'panel_full_scout': False,
        'missing_occurrence_datetime_n': census['missing_occurrence_datetime_n'],
        'strategy_pointer': None,
        'nfl_000_pointer': NFL_000_POINTER,
        'signal_port': False,
        'feebook_commit': FEEBOOK_COMMIT,
        'rails_commit': RAILS_COMMIT,
        'fee_cache': label,
        'cache_labeled': True,
        'live_r1p1': False,
        'fee_credit_rule_id': rails.FEE_CREDIT_RULE_ID,
        'fee_source': 'cache',
        'queue_source': 'rails',
        'honesty_helpers': 'hygiene',
        'fee_import_only': True,
        'rails_import_only': True,
        'fee_override_applied': False,
        'examiner_formula_used_as_series_pin': False,
        'lee_ready': 'REFUSED',
        'logan_keys_required': False,
        'live_orders': False,
        'live_gets': 0,
        'signal_retune_000': False,
        'kxmlbgame_ml_retune': False,
        'cap_sr_reopen': False,
        'admit_py_run': False,
        'claims_s1_green': False,
        'dual_cloud': False,
        'does_not_ungate': list(DOES_NOT_UNGATE),
        'fee_is_knob': False,
        'examiner_status': 'HOLD_PRE_PR',
        'stub_ready': False,
        'scorecard_fields': SCORECARD_FIELDS,
        'freeze_sha256': FREEZE_SHA256,
        'panel_stub_sha256': PANEL_STUB_SHA256,
        'conductor_accept_sha256': ACCEPT_SHA256,
        'source_pins_sha256': SOURCE_PINS_SHA256,
        'digest_all_match_claimed': pins['digest_all_match_claimed'],
        'digest_missing': pins['missing'],
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
    scorecard['examiner_status'] = 'HOLD_PRE_PR'
    scorecard['stub_ready'] = False
    scorecard['series_ticker'] = SERIES
    scorecard['fee_cache'] = fee_output()
    scorecard['cache_labeled'] = True
    return scorecard


def assert_null_scorecard(payload):
    """Require every instrument field, results, and pnl, and require null."""
    if not isinstance(payload, dict):
        raise ScorecardPromotionRefused()
    for key in OUTPUT_KEYS:
        if key not in payload or payload[key] is not None:
            raise ScorecardPromotionRefused()
    return payload


def assert_v12_null(block):
    """Examiner scorecard v1.2 fields stay null and unmeasured."""
    if not isinstance(block, dict):
        raise ScorecardPromotionRefused()
    card = block.get('scorecard') or {}
    if card.get('verdict') is not None or card.get('status') != 'HOLD_PRE_PR':
        raise ScorecardPromotionRefused()
    if card.get('stub_ready') is not False or card.get('scored') is not False:
        raise ScorecardPromotionRefused()
    metrics = card.get('metrics') or {}
    for key in OUTPUT_KEYS:
        if key not in metrics or metrics[key] is not None:
            raise ScorecardPromotionRefused()
    common = block.get('common_scorecard') or {}
    if tuple(common.keys()) != COMMON_SCORECARD_KEYS:
        raise ScorecardPromotionRefused()
    for name, metric in common.items():
        if metric.get('value') is not None or metric.get('measured') is not False:
            raise ScorecardPromotionRefused()
        if name == 'calibration' and metric.get('emits_probabilities') is not False:
            raise ScorecardPromotionRefused()
    if block.get('study_label', {}).get('value') is not None:
        raise ScorecardPromotionRefused()
    gate = (block.get('preregistration_checklist') or {}).get('gate_status')
    if gate is not None:
        raise ScorecardPromotionRefused()
    counts = (block.get('preregistration_checklist') or {}).get('variants_declared_counts') or {}
    if counts.get('satisfied') != 8 or counts.get('n/a') != 4 or counts.get('missing') != 0:
        raise OrchestratorError('p16')
    stress = block.get('stress_sensitivity') or {}
    for name in ('one_tick_worse', 'fees_2x'):
        row = stress.get(name) or {}
        if row.get('measured') is not False:
            raise ScorecardPromotionRefused()
        if row.get('net_pnl_without_rewards') is not None or row.get('net_pnl_with_rewards') is not None:
            raise ScorecardPromotionRefused()
    dollars = block.get('executable_dollars_per_day') or {}
    if dollars.get('measured') is not False or dollars.get('value') is not None:
        raise ScorecardPromotionRefused()
    if dollars.get('median_day') is not None or dollars.get('p10_day') is not None:
        raise ScorecardPromotionRefused()
    fills = block.get('simulated_fills') or {}
    if fills.get('counts_toward_keep') is not False:
        raise ScorecardPromotionRefused()
    if (fills.get('fill_rate_simulated') or {}).get('value') is not None:
        raise ScorecardPromotionRefused()
    if block.get('all_score_values_null') is not True:
        raise ScorecardPromotionRefused()
    fee = block.get('fee_regime') or {}
    if fee.get('feebook_pin') != FEEBOOK_COMMIT or fee.get('rails_pin') != RAILS_COMMIT:
        raise OrchestratorError('fee regime')
    return block


def load_scorecard(path):
    """Read a null scorecard. A non-null metric is refused."""
    payload = json.loads(Path(path).read_bytes())
    return assert_null_scorecard(payload)


def write_scorecard(payload):
    """Refuse a missing or non-null measurement field. Nothing is written."""
    assert_null_scorecard(payload)
    raise ScorecardPromotionRefused()


def _report(arm, source, extra):
    if arm not in ANALYSIS_SLICE:
        raise UnknownSlice()
    published = published_scorecard()
    label = fee_output()
    report = {
        'experiment_id': EXPERIMENT_ID,
        'arm': arm,
        'analysis_slice': ANALYSIS_SLICE[arm],
        'source': source,
        'series_ticker': SERIES,
        'published': published,
        'promoted': False,
        'strategy_pointer': None,
        'signal_port': False,
        'live_orders': False,
        'live_gets': 0,
        'lee_ready': 'REFUSED',
        'fee_pin': FEEBOOK_COMMIT,
        'rails_pin': RAILS_COMMIT,
        'fee_cache': label,
        'cache_labeled': label['cache_labeled'],
        'live_r1p1': False,
        'fee_import_only': True,
        'rails_import_only': True,
        'claims_s1_green': False,
        'kxmlbgame_ml_retune': False,
        'admit_py_run': False,
        'dual_cloud': False,
        'examiner_status': 'HOLD_PRE_PR',
        'stub_ready': False,
    }
    report.update(extra)
    for key in OUTPUT_KEYS:
        report[key] = None
    assert_null_scorecard(report)
    assert_null_scorecard(published)
    if report['cache_labeled'] is not True or report['series_ticker'] != SERIES:
        raise OrchestratorError('series')
    return report


def conduct(arm, panel=None):
    """Schema for one slice on the loaded panel. Scorecard fields stay null."""
    if arm not in ANALYSIS_SLICE:
        raise UnknownSlice()
    if panel is None:
        panel = load_panel()
    events = panel.get('events') or []
    markets = panel.get('markets') or []
    census = occurrence_census(markets)
    for market in markets:
        if not str(market.get('ticker', '')).startswith(SERIES + '-'):
            raise OrchestratorError('series')
    extra = {
        'event_count': len(events),
        'market_count': len(markets),
        'source_markets_n': SOURCE_MARKETS_N,
        'source_events_n': SOURCE_EVENTS_N,
        'scout_raw_present': (PARENT / SCOUT_CITE).is_file(),
        'missing_occurrence_datetime_n': census['missing_occurrence_datetime_n'],
    }
    return _report(arm, 'panel', extra)


def load_synthetic_trades(path=None):
    path = SYNTHETIC_TRADES if path is None else Path(path)
    payload = json.loads(Path(path).read_text())
    if payload.get('source') != 'synthetic_schema_standin':
        raise OrchestratorError('source')
    trades = payload.get('trades')
    if not isinstance(trades, list) or len(trades) < 2:
        raise OrchestratorError('synthetic trades')
    return trades


def load_synthetic_fresh(path=None):
    path = SYNTHETIC_FRESH if path is None else Path(path)
    payload = json.loads(Path(path).read_text())
    if payload.get('source') != 'synthetic_schema_standin':
        raise OrchestratorError('source')
    rows = payload.get('rows')
    if not isinstance(rows, list) or len(rows) < 2:
        raise OrchestratorError('synthetic rows')
    return rows


def conduct_native(path=None):
    """Q6S5A0 schema on synthetic native rows. Does not write the freeze scorecard."""
    rows = partition_native(load_synthetic_trades(path))
    return _report(Q6S5A0, 'synthetic_schema_standin', {
        'partitions': rows,
        'partition_count': len(rows),
    })


def conduct_fresh(path=None):
    """Q6S5A1 schema on synthetic book rows. The gap stays null."""
    rows = partition_fresh(load_synthetic_fresh(path))
    return _report(Q6S5A1, 'synthetic_schema_standin', {
        'bins': rows,
        'bin_count': len(rows),
    })


def frozen_output_snapshot():
    """Read freeze files. Does not modify them."""
    payloads = {
        'frozen': json.loads(FROZEN_EXPERIMENT.read_text()),
        'empty': json.loads(EMPTY_RESULTS.read_text()),
        'bundle_frozen': json.loads((LAB_BUNDLE / 'FROZEN_EXPERIMENT.json').read_text()),
        'bundle_results': json.loads((LAB_BUNDLE / 'results.json').read_text()),
        'governance_frozen': json.loads((GOVERNANCE_BUNDLE / 'FROZEN_EXPERIMENT.json').read_text()),
        'governance_empty': json.loads((GOVERNANCE_BUNDLE / 'EMPTY_RESULTS.json').read_text()),
    }
    snapshot = {}
    for name, payload in payloads.items():
        for key in OUTPUT_KEYS:
            if key not in payload or payload[key] is not None:
                raise ScorecardPromotionRefused()
            snapshot['%s.%s' % (name, key)] = None
        if payload.get('series_ticker') not in (None, SERIES) and payload.get('scorecard', {}).get('packet') != EXPERIMENT_ID:
            if name.startswith('frozen') or name.endswith('frozen'):
                if payload.get('series_ticker') != SERIES:
                    raise OrchestratorError('series')
    return snapshot
