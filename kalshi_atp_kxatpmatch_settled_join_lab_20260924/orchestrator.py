"""ATP KXATPMATCH settled-resolution join harness.

Measurement only. One knob: join_gate. This module does not edit ATP-FQ,
C4-RJ, feebook, rails, Cap-SR, any FQ sibling, or a closed RJ harness. It
does not place orders, does not read Logan keys, does not run the admit
tool, and does not write the committed scorecard.

J0 requires a nonempty official result on an already-settled market.
J1 uses occurrence_datetime when that field is present. When it is null,
the row is labeled join_source expected_expiration_time_fallback. The
fallback clock is never written into occurrence_datetime. Raw values stay
as returned. Scout N=30 is a pin and is not settled_join_n. admitted_at
stays null. Fee, queue, book, fill, and tape metrics stay held.

Measurement mode pages public GET reads for markets settled strictly after
the Conductor ACCEPT instant. It logs every attempt, keeps 429 gaps empty,
and writes counts only to the caller-supplied output path.

The measure transport path asks /markets for min_settled_ts first and calls
/events only after a /markets gap. Live GETs follow the Collector budget and
fail closed without a grant. Join labelling is unchanged.
"""
import hashlib
import http.client
import json
import sqlite3
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent

LAB_DIRECTORY = 'kalshi_atp_kxatpmatch_settled_join_lab_20260924'
EXPERIMENT_ID = 'ATP-KXATPMATCH-SETTLED-RESOLUTION-JOIN-HARNESS'
FEATURE_FAMILY = 'ATP-RJ'
PANEL_VERSION = '2026-09-23.atp-kxatpmatch-v0'
SERIES = 'KXATPMATCH'
KNOB = 'join_gate'
J0 = 'J0'
J1 = 'J1'
ARMS = (J0, J1)
JOIN_GATE = {
    J0: 'nonempty_result_required',
    J1: 'occurrence_datetime_match',
}
JOIN_SOURCE_OCCURRENCE = 'occurrence_datetime'
JOIN_SOURCE_FALLBACK = 'expected_expiration_time_fallback'
FINALIZED_RESULTS = ('yes', 'no')
FINALIZED_STATUSES = ('finalized', 'settled')
SCOUT_NONEMPTY_N_DECLARED = 30
PANEL_EVENTS_N = 6
PANEL_MARKETS_N = 12
PARENT_MISSING_OCCURRENCE_N = 0
SCOUT_OCCURRENCE_EQUALS_EXPECTED_N = 30
SCOUT_SETTLEMENT_BEFORE_OCCURRENCE_N = 8
PANEL_SHA256 = 'ed041c502d1f775d33c44bf900ac91b1339d99045bddd2052edd09a139ae2d3f'
CITED_FREEZE_SHA256 = 'dc9fcb326a97ce24267ed96438bf403687bc9aef6b79dccef3483d0e4cdeeb69'
ACCEPT_SHA256 = 'e42d75834086f34090581aee88563ab9849d60864c2d9e59c4ef495b3e8e5af5'
SCOUT_REGET_SHA256 = '2982a245ebd4ff8430ef4b2fe13692c15211c2077e2460d6c0246480f59736df'
SEED_SUMMARY_SHA256 = '913fc5d646c51192e40869a68a64b4fe2b66f8231dd75b90f5467bd50559700e'
SETTLED_REGET_SHA256 = '068ff00fe420d3365cc798549ef2e89aac96fa7e841846f73e67d5103c49760a'
EXAMINER_HOLD_SHA256 = '214fb8c1b54d1dfd14cdcff39c4a35e227eafe7e35ba96ff2e6e636b04f2ba76'
MAXIMIZE_PIN_SHA256 = '70020baf5599f7afcd4c8335d5f084c34784c5b4b1b44ffabce1041e41cbc84a'
PING_SHA256 = 'a666102da44910288756896aaa30b3d2bfde4fff867fca9fff0cd1b75420c28b'
SCORECARD_TEMPLATE_SHA256 = '56bcf6269a42031d9d90496e9a65c2292321aed2165033f6fb44ff8cc4d6b1cc'
FEEBOOK_COMMIT = '22371178cb2663250b4762f328069571c48cb551'
RAILS_COMMIT = '6a28e0d6254327ea4e6451c781bec56215ac6cac'
BASE_COMMIT = '959c3f2beaec5f999b4852c428a3c4cdae1e9603'
BRANCH_BASE_COMMIT = '37ad5b7b366c10dcdf278c2325611e6f426a62c6'
ACCEPT_ISSUED_AT_ET = '2026-09-24T19:52-04:00'
ACCEPT_ISSUED_AT_UTC = '2026-09-24T23:52:00Z'
PUBLIC_ORIGIN = 'https://api.elections.kalshi.com'
PUBLIC_PREFIX = '/trade-api/v2'
PAGE_LIMIT = '100'
BACKOFF_SECONDS = (10, 20, 40)
MAX_GET_ATTEMPTS = 4
MAX_LIVE_GET_ATTEMPTS = 2
PAGE_CAP = 20
EVENTS_LOOKBACK_S = 172800
POLLER_NAME = 'atp_rj_measure'
RATE_POLICY_BUDGET = 'collector_budget_2026-09-24'
RATE_POLICY_LEGACY = 'legacy_stub_unit_only'
BUDGET_DOC_REL = 'lab/governance/astra/COLLECTOR_KALSHI_GET_BUDGET_2026-09-24.md'
BUDGET_DOC_SHA256 = '7cb4388681b950cf535a0d30a4bec44191ef809c40ef6f36b887de399fa30d22'
MEASURE_HARDENING_FREEZE_SHA256 = '1b7f3ab4705e00b9d2835ec759d23ef9434999b8e070d02010008dd653347c58'
MEASURE_HARDENING_ACCEPT_SHA256 = '8c350baaffa0fae822ba86481eed2362bebd919413c0d3f42847264244ad5411'
PHASE_B_START = datetime(2026, 9, 27, 16, 30, tzinfo=timezone.utc)
BUDGET_CLOSED_AT = datetime(2026, 10, 2, 6, 15, tzinfo=timezone.utc)
LIST_ENDPOINT_PATHS = ('/markets', '/events', '/markets/trades', '/series')
COOLDOWN_BASE_S = 30
COOLDOWN_CAP_S = 600
PENALTY_SPACING_S = 2.0
PENALTY_WINDOW_S = 30 * 60
STORM_429_COUNT = 3
STORM_WINDOW_S = 10 * 60
STORM_PAUSE_S = 10 * 60
QUIET_START = (22, 52)
QUIET_END = (22, 56)
PHASE_CEILING = {
    'A': {'total_rpm': 10, 'min_spacing': 6.0, 'list_rpm': 4},
    'B': {'total_rpm': 5, 'min_spacing': 12.0, 'list_rpm': 2},
}
AUDIT_CEILING = {'total_rpm': 3, 'min_spacing': 20.0, 'list_rpm': 3}
JOIN_FUNCTION_SHA256 = {
    '_occurrence_value': '39693e779790b6fc3443663ad2128582dc4075ae32b023d5bea8290a274e610d',
    'j1_label': '86ac3b0ae29c144e25d29bbdffc7a54f8c13b63156a197a62094555e2832d843',
    '_j0_pass': '4f2cb52cfcb024776e3dd48e09435ea4140a28f8100413844addff37c596b71d',
    '_event_clocks_from': '8d46856dcec7ae7e7cf3986dc9c60b0138e8148559b6706322c216745a06c326',
    'scout_pin_tickers': '4566c18e6d75609f92ea527ef0922c7b1959c34705c287c2df4792d605b35c57',
    '_markets_from_pages': 'd8fb0d6e0a1670ec0a1e0ccf7a5f7c0a5c8005cd89418ee5652700d597ed735e',
    '_markets_from_events': '1f2faf61af08cb4ccfcd80fff50f6d2608bcfc2ba34ce85e0cb057bf72fa7240',
    '_agree': 'bda3de69db1082bf4e403cad8137aa2947d10a5b1e79e8560448ab2d8fda734b',
    '_parse_utc': '06cd00597f05fb45f066159e2d38ab748b380632c43c5ada537d5dbcde21628d',
}
ADMIT_READY_PENDING = 'pending Clock'
OUTPUT_KEYS = (
    'settled_join_n',
    'occurrence_match_n',
    'fallback_join_n',
    'admit_ready_flag',
    'results',
    'pnl',
)
AGREE_FIELDS = (
    'result',
    'status',
    'occurrence_datetime',
    'expected_expiration_time',
    'settlement_ts',
)
DOES_NOT_UNGATE = ('S1', 'S2', 'R2-P4')
OUTSIDE_LIST_PARENT_EVENTS = (
    'KXATPMATCH-26SEP22HARGAL',
    'KXATPMATCH-26SEP22MOCKOT',
)
PARENT_EVENTS = (
    'KXATPMATCH-26SEP23BASCIN',
    'KXATPMATCH-26SEP23TOMSUN',
    'KXATPMATCH-26SEP22MOCKOT',
    'KXATPMATCH-26SEP22SVRNOG',
    'KXATPMATCH-26SEP22HARGAL',
    'KXATPMATCH-26SEP23DANMAT',
)
LIST_BOOK_ROUTES = (
    'GET /markets?series_ticker=KXATPMATCH&status=settled&limit=30',
    'GET /events?series_ticker=KXATPMATCH&status=settled&limit=15&with_nested_markets=true',
)
ADVERSARY_LABELS = {
    'lee_ready': 'Lee-Ready refused',
    'live_orders': 'live orders refused',
    'admit_py': 'admit.py refused',
    'ungate': 'S1/S2/R2-P4 stay gated',
    'arm_b': 'Arm B stays with Refiner',
    'q7_arm_b': 'Arm B stays with Refiner',
    'cap_sr_reopen': 'Cap-SR stays closed',
    'fq_reopen': 'FQ siblings stay closed',
    'atp_fq_reopen': 'ATP-FQ stays closed',
    'cpi_fq_reopen': 'CPI-FQ stays closed',
    'c1_rj_reopen': 'C1-RJ stays closed',
    'c3_rj_reopen': 'C3-RJ stays closed',
    'c4_rj_reopen': 'C4-RJ stays closed',
    'c5_rj_reopen': 'C5-RJ stays closed',
    'r3p3_rj_reopen': 'R3P3-RJ stays closed',
    'nhl_rj_reopen': 'NHL-RJ stays closed',
    's4_rj_reopen': 'S4-RJ stays closed',
    'r2p3_rj_reopen': 'R2P3-RJ stays closed',
    's5_rj_reopen': 'S5-RJ stays closed',
    'q6_retune': 'Q6-000 stays frozen',
    'invent_settled_result': 'settled result is not invented',
    'invent_fills': 'fills are not invented',
    'invent_depth': 'depth is not invented',
    'invent_occurrence': 'occurrence_datetime is not invented',
    'list_429_backfill': 'list books are not invented',
    'events_page2_backfill': 'events page 2 is not backfilled',
    'outside_list_parent': 'outside-list parent rows stay out of N',
    'copy_scout_n': 'scout N is not settled_join_n',
    'fee_metric': 'ATP fee metric stays HELD',
    'queue_metric': 'ATP queue metric stays HELD',
    'book_metric': 'ATP book metric stays HELD',
    'fill_metric': 'ATP fill metric stays HELD',
    'tape_metric': 'ATP tape metric stays HELD',
}
CAPTURE_PANEL = REPO / 'lab/astra-capture/atp-kxatpmatch/panel_stub.json'
GOV_PANEL = REPO / 'lab/governance/astra/packets/ATP_KXATPMATCH_PANEL_STUB_2026-09-23.json'
SCOUT_DIR = REPO / 'lab/governance/astra/packets/scout_atp_settled_rejoin_2026-09-24'
SCOUT_PANEL = SCOUT_DIR / 'ATP_KXATPMATCH_PANEL_STUB_2026-09-23.json'
SCOUT_PATH = SCOUT_DIR / 'scout_settled_rejoin_ATP_KXATPMATCH.json'
REGET_PATH = SCOUT_DIR / 'settled_reget_2026-09-24.json'
CAPTURE_REGET = REPO / 'lab/astra-capture/atp-kxatpmatch/settled_reget_2026-09-24.json'
SEED_PATH = SCOUT_DIR / 'SEED_SETTLED_SUMMARY.json'
FREEZE_PATH = REPO / 'lab/governance/astra/packets/ATP_KXATPMATCH_SETTLED_RESOLUTION_JOIN_HARNESS_FREEZE_2026-09-24.md'
ACCEPT_PATH = REPO / 'lab/governance/astra/packets/CONDUCTOR_ACCEPT_ATP_KXATPMATCH_SETTLED_RESOLUTION_JOIN_HARNESS_2026-09-24.json'
HOLD_PATH = REPO / 'lab/governance/astra/packets/EXAMINER_HOLD_ATP_KXATPMATCH_SETTLED_JOIN_HARNESS_PRE_PR_2026-09-24.json'
MAXIMIZE_PATH = REPO / 'lab/governance/astra/packets/MAXIMIZE_PIN_2026-09-24_1948ET.md'
PING_PATH = REPO / 'lab/governance/astra/packets/SUGGESTED_CONDUCTOR_ACCEPT_PING_ATP_RJ_2026-09-24.json'
TEMPLATE_PATH = REPO / 'lab/governance/astra/templates/EXAMINER_KALSHI_SCORECARD_TEMPLATE_v1.2.json'
LAB_PANEL = ROOT / 'ATP_KXATPMATCH_PANEL_STUB_2026-09-23.json'
PIN_GAP_PATH = ROOT / 'PIN_GAP.json'
EMPTY_RESULTS = ROOT / 'results/EMPTY_RESULTS.json'
FROZEN_EXPERIMENT = ROOT / 'FROZEN_EXPERIMENT.json'
SOURCE_PINS = ROOT / 'SOURCE_PINS.json'
SOURCE_PIN_MIRRORS = (
    ROOT / 'SOURCE_PINS.json',
    ROOT / 'ATP_KXATPMATCH_SETTLED_RESOLUTION_JOIN_HARNESS/SOURCE_PINS.json',
    REPO / 'packets/ATP_KXATPMATCH_SETTLED_JOIN_HARNESS/SOURCE_PINS.json',
    REPO / 'lab/astra-science/kalshi_atp_kxatpmatch_settled_join_lab_20260924/SOURCE_PINS.json',
)


class OrchestratorError(Exception):
    pass


class UnknownGate(OrchestratorError):
    pass


class ScorecardPromotionRefused(OrchestratorError):
    pass


class LeeReadyRefused(OrchestratorError):
    pass


class AdversaryRefused(OrchestratorError):
    pass


class AdmitPyRefused(OrchestratorError):
    pass


class LiveOrdersForbidden(OrchestratorError):
    pass


class UngateRefused(OrchestratorError):
    pass


class InventedDepthRefused(OrchestratorError):
    pass


class InventedFillRefused(OrchestratorError):
    pass


class InventedResultRefused(OrchestratorError):
    pass


class InventedSoTRefused(OrchestratorError):
    pass


class InventedMarketRefused(OrchestratorError):
    pass


class OccurrenceIntegrityRefused(OrchestratorError):
    pass


class ExaminerNotReady(OrchestratorError):
    pass


class PinAbsent(OrchestratorError):
    pass


class PinMismatch(OrchestratorError):
    pass


class BudgetGrantMissing(OrchestratorError):
    pass


class LegacyStubLiveRefused(OrchestratorError):
    pass


def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def execution_adapter():
    """No live order client lives in this lab."""
    raise LiveOrdersForbidden()


def assert_public_get(method):
    """GET is the only public capture verb."""
    if method != 'GET':
        raise LiveOrdersForbidden()
    return None


def run_admit(path=None):
    """The parent panel is not admitted. This lab does not admit."""
    del path
    raise AdmitPyRefused()


def ungate(name):
    """S1, S2, and R2-P4 stay queued."""
    if name in DOES_NOT_UNGATE:
        raise UngateRefused()
    raise OrchestratorError('ungate')


def claim_admit_ready():
    """admit_ready_flag stays null until Clock admit."""
    raise ExaminerNotReady()


def claim_examiner_ready():
    """HOLD pre-PR. READY NOT_SCORED is a post-merge state and is still unscored."""
    raise ExaminerNotReady()


def quote_depth(market):
    """Book quantity is held. No depth ladder is read or written."""
    del market
    raise InventedDepthRefused()


def invent_fill(market=None, value=None):
    """Fill quantity is held. No fill is invented."""
    del market, value
    raise InventedFillRefused()


def fee_metric(market=None, value=None):
    """The ATP fee metric stays held."""
    del market, value
    raise AdversaryRefused(ADVERSARY_LABELS['fee_metric'])


def queue_metric(market=None, value=None):
    """The ATP queue metric stays held."""
    del market, value
    raise InventedDepthRefused()


def book_metric(market=None, value=None):
    """The ATP book metric stays held."""
    del market, value
    raise InventedDepthRefused()


def tape_metric(market=None, value=None):
    """The ATP tape metric stays held."""
    del market, value
    raise InventedFillRefused()


def invent_result(ticker=None, result=None):
    """A settled result is not written."""
    del ticker, result
    raise InventedResultRefused()


def backfill_list_429(which=None, result=None, occurrence_datetime=None):
    """The settled markets list 429 stays an honest gap."""
    del which, result, occurrence_datetime
    raise InventedResultRefused()


def backfill_events_page2(cursor=None, markets=None):
    """Events-list page 2 stays unfetched."""
    del cursor, markets
    raise InventedMarketRefused()


def add_outside_list_parent(event_ticker=None, markets=None):
    """HARGAL and MOCKOT stay outside N."""
    del event_ticker, markets
    raise InventedMarketRefused()


def assign_occurrence(ticker=None, value=None):
    """occurrence_datetime is not invented."""
    del ticker, value
    raise InventedSoTRefused()


def write_expected_expiration_into_occurrence_datetime(market=None):
    """expected_expiration_time is never copied into occurrence_datetime."""
    del market
    raise InventedSoTRefused()


def copy_scout_n_into_settled_join(value=None):
    """The declared scout N=30 is not the scorecard count."""
    del value
    raise ScorecardPromotionRefused()


def infer_lee_ready(row):
    """Lee-Ready has no success path."""
    del row
    raise LeeReadyRefused()


def refuse_adversary(label):
    """Named refuse labels. Nothing is traded."""
    if label not in ADVERSARY_LABELS:
        raise OrchestratorError('adversary label')
    if label == 'lee_ready':
        raise LeeReadyRefused()
    if label in ('invent_settled_result', 'list_429_backfill'):
        raise InventedResultRefused()
    if label in ('invent_fills', 'fill_metric', 'tape_metric'):
        raise InventedFillRefused()
    if label in ('invent_depth', 'book_metric', 'queue_metric'):
        raise InventedDepthRefused()
    if label == 'invent_occurrence':
        raise InventedSoTRefused()
    if label in ('events_page2_backfill', 'outside_list_parent'):
        raise InventedMarketRefused()
    if label == 'admit_py':
        raise AdmitPyRefused()
    if label == 'live_orders':
        raise LiveOrdersForbidden()
    if label == 'ungate':
        raise UngateRefused()
    if label == 'copy_scout_n':
        raise ScorecardPromotionRefused()
    if label == 'fee_metric':
        raise AdversaryRefused(ADVERSARY_LABELS[label])
    raise AdversaryRefused(ADVERSARY_LABELS[label])


def _assert_digest(path, digest):
    raw = Path(path).read_bytes()
    if hashlib.sha256(raw).hexdigest() != digest:
        raise PinMismatch(Path(path).name)
    return raw


def assert_panel_copies():
    """Capture, governance, scout, and lab copies are the same panel bytes."""
    capture = _assert_digest(CAPTURE_PANEL, PANEL_SHA256)
    for path in (GOV_PANEL, SCOUT_PANEL, LAB_PANEL):
        if Path(path).read_bytes() != capture:
            raise PinMismatch(Path(path).name)
    return capture


def load_panel(path=None):
    """Load the unadmitted parent. Does not write admitted_at."""
    assert_panel_copies()
    path = CAPTURE_PANEL if path is None else Path(path)
    payload = json.loads(path.read_bytes())
    return _validate_panel(payload)


def _validate_panel(payload):
    if payload.get('panel_version') != PANEL_VERSION:
        raise OrchestratorError('panel_version')
    if payload.get('series_ticker') != SERIES:
        raise OrchestratorError('series')
    if payload.get('admitted_at') is not None:
        raise AdmitPyRefused()
    if payload.get('stub_status') != 'NOT_ADMITTED':
        raise AdmitPyRefused()
    events = payload.get('events') or []
    markets = payload.get('markets') or []
    if len(events) != PANEL_EVENTS_N or len(markets) != PANEL_MARKETS_N:
        raise OrchestratorError('cohort')
    if tuple(event.get('event_ticker') for event in events) != PARENT_EVENTS:
        raise OrchestratorError('parent events')
    missing = 0
    for market in markets:
        if market.get('status') != 'active':
            raise InventedResultRefused()
        if market.get('result') not in ('', None):
            raise InventedResultRefused()
        if 'admitted_at' in market and market.get('admitted_at') is not None:
            raise AdmitPyRefused()
        if market.get('occurrence_datetime') is None:
            missing += 1
    if missing != PARENT_MISSING_OCCURRENCE_N:
        raise OrchestratorError('missing occurrence')
    if payload.get('results') is not None or payload.get('pnl') is not None:
        raise ScorecardPromotionRefused()
    return payload


def _event_clocks(panel):
    return {
        event['event_ticker']: event.get('occurrence_datetime')
        for event in panel['events']
    }


def _occurrence_value(market):
    """Return the raw occurrence_datetime. A missing key stays null."""
    if 'occurrence_datetime' not in market:
        return None
    return market.get('occurrence_datetime')


def j1_label(market, event_occurrence):
    """Label one J1 row. Does not mutate the market."""
    before_present = 'occurrence_datetime' in market
    before = market.get('occurrence_datetime') if before_present else None
    occurrence = _occurrence_value(market)
    expected = market.get('expected_expiration_time')
    row = {
        'key': market.get('ticker') or market.get('market_ticker'),
        'event_ticker': market.get('event_ticker'),
        'j1': 'occurrence_datetime_match',
        'occurrence_datetime': occurrence,
        'expected_expiration_time': expected,
        'event_occurrence_datetime': event_occurrence,
    }
    if occurrence is not None:
        if event_occurrence is not None and occurrence != event_occurrence:
            raise OccurrenceIntegrityRefused()
        row['join_source'] = JOIN_SOURCE_OCCURRENCE
        row['clock'] = 'occurrence_datetime'
    else:
        row['join_source'] = JOIN_SOURCE_FALLBACK
        row['clock'] = 'expected_expiration_time'
        if row['occurrence_datetime'] is not None:
            raise InventedSoTRefused()
        if row['occurrence_datetime'] == expected and expected is not None:
            raise InventedSoTRefused()
    if before_present and market.get('occurrence_datetime') != before:
        raise InventedSoTRefused()
    if not before_present and 'occurrence_datetime' in market:
        raise InventedSoTRefused()
    if row['join_source'] == JOIN_SOURCE_FALLBACK and row['occurrence_datetime'] is not None:
        raise InventedSoTRefused()
    return row


def _raw_event_markets(path):
    payload = json.loads(Path(path).read_bytes())
    event = payload.get('event') or {}
    markets = event.get('markets')
    if markets is None:
        markets = payload.get('markets') or []
    return markets


def _index_by_ticker(markets):
    indexed = {}
    for market in markets:
        ticker = market.get('ticker')
        if ticker in indexed:
            raise PinMismatch(ticker)
        indexed[ticker] = market
    return indexed


def load_scout():
    """Read the pinned scout and reget. Does not open a socket."""
    _assert_digest(SCOUT_PATH, SCOUT_REGET_SHA256)
    _assert_digest(REGET_PATH, SETTLED_REGET_SHA256)
    _assert_digest(CAPTURE_REGET, SETTLED_REGET_SHA256)
    _assert_digest(SEED_PATH, SEED_SUMMARY_SHA256)
    scout = json.loads(SCOUT_PATH.read_bytes())
    reget = json.loads(REGET_PATH.read_bytes())
    if scout.get('settled_nonempty_result_N') != SCOUT_NONEMPTY_N_DECLARED:
        raise PinMismatch('scout N')
    if reget.get('settled_nonempty_result_N') != SCOUT_NONEMPTY_N_DECLARED:
        raise PinMismatch('reget N')
    markets = scout.get('markets') or []
    reget_markets = reget.get('markets_nonempty') or []
    if len(markets) != SCOUT_NONEMPTY_N_DECLARED or len(reget_markets) != SCOUT_NONEMPTY_N_DECLARED:
        raise OrchestratorError('settled cohort')
    if tuple(reget.get('events_listed_without_nested_markets') or ()) != ():
        raise InventedMarketRefused()
    settled_events = tuple(reget.get('events_with_nested_settled_markets') or ())
    if len(settled_events) != 15:
        raise PinMismatch('settled events')
    if scout.get('settled_list_http') != '429_honest':
        raise PinMismatch('settled list')
    if scout.get('settled_events_list_http') != '200_first_attempt':
        raise PinMismatch('events list')
    if scout.get('settled_events_list_cursor_present') is not True:
        raise PinMismatch('events cursor')
    if scout.get('list_embed_vs_single_event_match') is not True:
        raise PinMismatch('list embed')
    if scout.get('occurrence_datetime_present_on_settled_N') != SCOUT_NONEMPTY_N_DECLARED:
        raise PinMismatch('occurrence present')
    if scout.get('occurrence_datetime_null_on_settled_N') != 0:
        raise PinMismatch('occurrence null')
    if scout.get('occurrence_datetime_equals_expected_expiration_N') != SCOUT_OCCURRENCE_EQUALS_EXPECTED_N:
        raise PinMismatch('clock reconcile')
    if scout.get('settlement_ts_before_occurrence_datetime_N') != SCOUT_SETTLEMENT_BEFORE_OCCURRENCE_N:
        raise PinMismatch('settlement drift')
    reget_index = _index_by_ticker(reget_markets)
    raw_index = {}
    for filename in (
        'event_KXATPMATCH_26SEP23BASCIN_parent.json',
        'event_KXATPMATCH_26SEP23TOMSUN_parent.json',
        'event_KXATPMATCH_26SEP23DANMAT_parent.json',
        'event_KXATPMATCH_26SEP22SVRNOG_parent.json',
        'event_KXATPMATCH_26SEP22HARGAL_parent.json',
        'event_KXATPMATCH_26SEP22MOCKOT_parent.json',
    ):
        raw_index.update(_index_by_ticker(_raw_event_markets(SCOUT_DIR / 'raw' / filename)))
    list_payload = json.loads((SCOUT_DIR / 'raw/events_settled_KXATPMATCH_lim15.json').read_bytes())
    if not list_payload.get('cursor'):
        raise PinMismatch('events cursor')
    if (SCOUT_DIR / 'raw/events_settled_KXATPMATCH_lim15_page2.json').exists():
        raise InventedMarketRefused()
    listed = list_payload.get('events') or []
    if len(listed) != 15:
        raise PinMismatch('events page')
    list_index = {}
    for event in listed:
        nested = event.get('markets')
        if not nested:
            raise InventedMarketRefused()
        list_index.update(_index_by_ticker(nested))
    if len(list_index) != SCOUT_NONEMPTY_N_DECLARED:
        raise OrchestratorError('list embed')
    for name in (
        'markets_settled_KXATPMATCH_lim30.json',
        'markets_settled_KXATPMATCH_lim30_retry1.json',
        'markets_settled_KXATPMATCH_lim30_retry2.json',
        'markets_settled_KXATPMATCH_lim30_retry3.json',
    ):
        body = json.loads((SCOUT_DIR / 'raw' / name).read_bytes())
        if (body.get('error') or {}).get('code') != 'too_many_requests':
            raise PinMismatch(name)
    clocks = {}
    before = 0
    seen = set()
    for market in markets:
        ticker = market.get('ticker')
        if ticker in seen:
            raise PinMismatch(ticker)
        seen.add(ticker)
        result = market.get('result')
        status = market.get('status')
        if status != 'finalized' or result not in FINALIZED_RESULTS:
            raise InventedResultRefused()
        occurrence = market.get('occurrence_datetime')
        expected = market.get('expected_expiration_time')
        settlement = market.get('settlement_ts')
        if occurrence is None or expected is None or settlement is None:
            raise OccurrenceIntegrityRefused()
        if occurrence != expected:
            raise PinMismatch('clock reconcile')
        if market.get('event_ticker') in OUTSIDE_LIST_PARENT_EVENTS:
            raise InventedMarketRefused()
        if _parse_utc(settlement) < _parse_utc(occurrence):
            before += 1
        sibling = reget_index.get(ticker)
        embedded = list_index.get(ticker)
        for other in (sibling, embedded):
            if other is None:
                raise PinMismatch(ticker)
            for field in AGREE_FIELDS:
                if other.get(field) != market.get(field):
                    raise PinMismatch(ticker)
        raw = raw_index.get(ticker)
        if raw is not None:
            for field in AGREE_FIELDS:
                if raw.get(field) != market.get(field):
                    raise PinMismatch(ticker)
        clocks.setdefault(market.get('event_ticker'), set()).add(occurrence)
    if before != SCOUT_SETTLEMENT_BEFORE_OCCURRENCE_N:
        raise PinMismatch('settlement drift')
    if set(clocks) != set(settled_events):
        raise PinMismatch('settled events')
    for event_ticker, values in clocks.items():
        if len(values) != 1:
            raise OccurrenceIntegrityRefused()
        del event_ticker
    outside = []
    for ticker, raw in raw_index.items():
        if raw.get('event_ticker') not in OUTSIDE_LIST_PARENT_EVENTS:
            continue
        outside.append(ticker)
        if ticker in seen:
            raise InventedMarketRefused()
        if raw.get('status') != 'finalized' or raw.get('result') not in FINALIZED_RESULTS:
            raise PinMismatch(ticker)
    if len(outside) != 4:
        raise PinMismatch('outside list')
    return scout


def structural_rows(panel=None, scout=None):
    """Label settled rows and parent rows. Does not write scorecard counts."""
    if panel is None:
        panel = load_panel()
    else:
        _validate_panel(panel)
    if scout is None:
        scout = load_scout()
    settled_clocks = {}
    for market in scout['markets']:
        settled_clocks.setdefault(market['event_ticker'], market['occurrence_datetime'])
    rows = []
    for market in scout['markets']:
        observed = market.get('result')
        if observed not in FINALIZED_RESULTS or market.get('status') != 'finalized':
            j0 = 'honest_empty_result'
        else:
            j0 = 'nonempty_result_required_pass'
        label = j1_label(market, settled_clocks[market['event_ticker']])
        if label['join_source'] != JOIN_SOURCE_OCCURRENCE:
            raise PinMismatch('fallback on scout pin')
        if label['occurrence_datetime'] != label['expected_expiration_time']:
            raise PinMismatch('clock reconcile')
        label['j0'] = j0
        label['cohort'] = 'settled_reget'
        label['result'] = observed
        label['status'] = market.get('status')
        label['settlement_ts'] = market.get('settlement_ts')
        label['parent_seed'] = False
        rows.append(label)
    parent_clocks = _event_clocks(panel)
    parent_rows = []
    for market in panel['markets']:
        if market.get('result') not in ('', None):
            raise InventedResultRefused()
        label = j1_label(market, parent_clocks.get(market.get('event_ticker')))
        label['j0'] = 'honest_empty_result'
        label['cohort'] = 'parent_panel'
        label['result'] = market.get('result')
        label['status'] = market.get('status')
        label['parent_seed'] = True
        if label['join_source'] != JOIN_SOURCE_OCCURRENCE:
            raise PinMismatch('parent fallback')
        parent_rows.append(label)
    if len(rows) != SCOUT_NONEMPTY_N_DECLARED:
        raise OrchestratorError('settled rows')
    if len(parent_rows) != PANEL_MARKETS_N:
        raise OrchestratorError('parent rows')
    passes = [row for row in rows if row['j0'] == 'nonempty_result_required_pass']
    if len(passes) != SCOUT_NONEMPTY_N_DECLARED:
        raise OrchestratorError('j0')
    return rows + parent_rows


def listed_digest_match(pins=None):
    """True only when every listed SOURCE_PINS hash matches the in-repo bytes."""
    if pins is None:
        if not SOURCE_PINS.is_file():
            raise PinAbsent()
        pins = json.loads(SOURCE_PINS.read_bytes())
    recorded = pins.get('pins') or {}
    if not recorded:
        raise PinAbsent()
    matched = True
    for name, entry in recorded.items():
        path = REPO / entry['path']
        if not path.is_file():
            raise PinAbsent(name)
        digest = sha256_file(path)
        size = path.stat().st_size
        if digest != entry.get('sha256') or size != entry.get('bytes'):
            matched = False
    claimed = pins.get('digest_all_match_claimed')
    if claimed is True and matched is not True:
        raise PinMismatch('digest_all_match_claimed')
    if claimed is not True and matched is True:
        raise PinMismatch('digest_all_match_claimed')
    mirrors = [path.read_bytes() for path in SOURCE_PIN_MIRRORS]
    if any(blob != mirrors[0] for blob in mirrors[1:]):
        raise PinMismatch('SOURCE_PINS mirror')
    return matched


def digest_status():
    """Re-hash the cited pins. The claim follows the bytes."""
    freeze_present = FREEZE_PATH.is_file()
    freeze_sha = sha256_file(FREEZE_PATH) if freeze_present else None
    if freeze_present and freeze_sha != CITED_FREEZE_SHA256:
        raise PinMismatch('freeze')
    accept_present = ACCEPT_PATH.is_file()
    if accept_present:
        accept = json.loads(ACCEPT_PATH.read_bytes())
        if accept.get('decision') != 'ACCEPT + IMPLEMENT GO':
            raise PinMismatch('accept')
        if accept.get('issued_at_et') != ACCEPT_ISSUED_AT_ET:
            raise PinMismatch('accept')
        if sha256_file(ACCEPT_PATH) != ACCEPT_SHA256:
            raise PinMismatch('accept')
    if not (TEMPLATE_PATH.is_file() and sha256_file(TEMPLATE_PATH) == SCORECARD_TEMPLATE_SHA256):
        raise PinMismatch('scorecard template')
    hold_present = HOLD_PATH.is_file() and sha256_file(HOLD_PATH) == EXAMINER_HOLD_SHA256
    maximize_present = MAXIMIZE_PATH.is_file() and sha256_file(MAXIMIZE_PATH) == MAXIMIZE_PIN_SHA256
    ping_present = PING_PATH.is_file() and sha256_file(PING_PATH) == PING_SHA256
    scout_present = SCOUT_PATH.is_file() and sha256_file(SCOUT_PATH) == SCOUT_REGET_SHA256
    claimed = listed_digest_match()
    return {
        'freeze_bytes_in_checkout': freeze_present,
        'freeze_sha256': freeze_sha,
        'freeze_matches_cited': freeze_sha == CITED_FREEZE_SHA256,
        'accept_bytes_in_checkout': accept_present,
        'examiner_hold_bytes_in_checkout': hold_present,
        'scout_bytes_in_checkout': scout_present,
        'maximize_pin_bytes_in_checkout': maximize_present,
        'suggested_ping_bytes_in_checkout': ping_present,
        'scorecard_template_bytes_in_checkout': True,
        'digest_all_match_claimed': claimed is True,
        'cited_freeze_sha256': CITED_FREEZE_SHA256,
    }


def list_books():
    """Settled-list 429s and events page 2 stay empty."""
    return {
        'routes': list(LIST_BOOK_ROUTES),
        'books_present': False,
        'list_429_backfilled': False,
        'markets_invented': False,
        'events_page2_fetched': False,
        'events_page2_backfilled': False,
        'outside_list_parent_events': list(OUTSIDE_LIST_PARENT_EVENTS),
        'outside_list_parent_added_to_n': False,
    }


def published_scorecard():
    """Every instrument field is present and null."""
    scorecard = {key: None for key in OUTPUT_KEYS}
    scorecard['status'] = 'EMPTY_RESULTS_PRE_EXAMINER'
    scorecard['lee_ready'] = 'REFUSED'
    scorecard['examiner_status'] = 'HOLD_PRE_PR'
    scorecard['stub_ready'] = False
    scorecard['admitted_at'] = None
    scorecard['list_429_backfilled'] = False
    scorecard['events_page2_backfilled'] = False
    scorecard['scout_n_copied_into_settled_join_n'] = False
    scorecard['fee_queue_book_fill_tape'] = 'HELD'
    scorecard['digest_all_match_claimed'] = digest_status()['digest_all_match_claimed']
    return scorecard


def assert_null_scorecard(payload):
    """Require every instrument field and require null."""
    if not isinstance(payload, dict):
        raise ScorecardPromotionRefused()
    for key in OUTPUT_KEYS:
        if key not in payload or payload[key] is not None:
            raise ScorecardPromotionRefused()
    if 'admitted_at' in payload and payload['admitted_at'] is not None:
        raise AdmitPyRefused()
    return payload


def write_scorecard(payload):
    """Refuse a missing or non-null measurement field. Nothing is written."""
    assert_null_scorecard(payload)
    raise ScorecardPromotionRefused()


def instrument_binding(panel=None):
    """One join-gate knob. Fee, queue, book, fill, and tape stay unloaded."""
    if panel is None:
        panel = load_panel()
    pins = digest_status()
    rows = structural_rows(panel)
    gaps = list_books()
    settled = [row for row in rows if row['cohort'] == 'settled_reget']
    fallback = [row for row in rows if row['join_source'] == JOIN_SOURCE_FALLBACK]
    return {
        'experiment_id': EXPERIMENT_ID,
        'lab_directory': LAB_DIRECTORY,
        'feature_family': FEATURE_FAMILY,
        'knob': KNOB,
        'arms': tuple({'id': arm, 'join_gate': JOIN_GATE[arm]} for arm in ARMS),
        'panel_version': panel['panel_version'],
        'admitted_at': None,
        'events_n': PANEL_EVENTS_N,
        'markets_n': PANEL_MARKETS_N,
        'row_label_count': len(rows),
        'settled_row_label_count': len(settled),
        'fallback_row_label_count': len(fallback),
        'source': 'pinned_scout_reget_and_parent_panel',
        'scout_reget_loaded': True,
        'live_fetch': False,
        'settled_nonempty_result_N_scout_declared': SCOUT_NONEMPTY_N_DECLARED,
        'scout_n_copied_into_settled_join_n': False,
        'j1_clock': 'occurrence_datetime',
        'j1_fallback_join_source': JOIN_SOURCE_FALLBACK,
        'occurrence_datetime_invented': False,
        'expected_expiration_written_into_occurrence_datetime': False,
        'list_books': gaps,
        'fee_import_used': False,
        'rails_import_used': False,
        'fee_queue_book_fill_tape': 'HELD',
        'feebook_commit_fixed_not_loaded': FEEBOOK_COMMIT,
        'rails_commit_fixed_not_loaded': RAILS_COMMIT,
        'lee_ready': 'REFUSED',
        'live_orders': False,
        'admit_py_run': False,
        'arm_b_touch': False,
        'does_not_ungate': list(DOES_NOT_UNGATE),
        's1_s2_r2p4_ungated': False,
        'examiner_status': 'HOLD_PRE_PR',
        'stub_ready': False,
        'freeze_sha256_cited': CITED_FREEZE_SHA256,
        'freeze_bytes_in_checkout': pins['freeze_bytes_in_checkout'],
        'digest_all_match_claimed': pins['digest_all_match_claimed'],
        'panel_parent_sha256': PANEL_SHA256,
        'base_commit': BASE_COMMIT,
        'results': None,
        'pnl': None,
        'settled_join_n': None,
        'occurrence_match_n': None,
        'fallback_join_n': None,
        'admit_ready_flag': None,
    }


def _report(arm, extra):
    if arm not in JOIN_GATE:
        raise UnknownGate()
    published = published_scorecard()
    report = {
        'experiment_id': EXPERIMENT_ID,
        'arm': arm,
        'join_gate': JOIN_GATE[arm],
        'source': 'pinned_scout_reget_and_parent_panel',
        'published': published,
        'promoted': False,
        'live_orders': False,
        'live_fetch': False,
        'lee_ready': 'REFUSED',
        'admit_py_run': False,
        'list_429_backfilled': False,
        'events_page2_backfilled': False,
        'outside_list_parent_added_to_n': False,
        'scout_n_copied_into_settled_join_n': False,
        'scout_reget_loaded': True,
        'digest_all_match_claimed': published['digest_all_match_claimed'],
        'occurrence_datetime_invented': False,
        'expected_expiration_written_into_occurrence_datetime': False,
        'fee_queue_book_fill_tape': 'HELD',
        'arm_b_touch': False,
        's1_s2_r2p4_ungated': False,
        'examiner_status': 'HOLD_PRE_PR',
        'stub_ready': False,
        'admitted_at': None,
    }
    report.update(extra)
    for key in OUTPUT_KEYS:
        report[key] = None
    report['admitted_at'] = None
    assert_null_scorecard(report)
    assert_null_scorecard(published)
    return report


def conduct(arm, panel=None):
    """Schema for one join gate. Scorecard fields stay null."""
    if arm not in JOIN_GATE:
        raise UnknownGate()
    if panel is None:
        panel = load_panel()
    else:
        _validate_panel(panel)
    rows = structural_rows(panel)
    extra = {
        'row_labels': rows,
        'admitted_at': None,
        'event_count': len(panel.get('events') or []),
        'market_count': PANEL_MARKETS_N,
        'settled_label_count': sum(1 for row in rows if row['cohort'] == 'settled_reget'),
        'fallback_label_count': sum(
            1 for row in rows if row['join_source'] == JOIN_SOURCE_FALLBACK
        ),
    }
    return _report(arm, extra)


def frozen_output_snapshot():
    """Read the null scorecard files. Does not modify them."""
    frozen = json.loads(FROZEN_EXPERIMENT.read_text())
    empty = json.loads(EMPTY_RESULTS.read_text())
    gap = json.loads(PIN_GAP_PATH.read_text())
    pins = json.loads(SOURCE_PINS.read_text())
    for payload in (frozen, empty, pins):
        assert_null_scorecard(payload)
    calibration = (
        empty.get('examiner_scorecard_v1_2', {})
        .get('common_scorecard', {})
        .get('calibration', {})
    )
    if calibration.get('value') is not None or calibration.get('emits_probabilities') is not False:
        raise ScorecardPromotionRefused()
    if gap.get('freeze_bytes_in_checkout') is not True:
        raise PinMismatch('pin gap')
    if gap.get('digest_all_match_claimed') is not True:
        raise PinMismatch('pin gap')
    if gap.get('cited_freeze_sha256') != CITED_FREEZE_SHA256:
        raise PinMismatch('pin gap')
    if gap.get('panel_parent_sha256') != PANEL_SHA256:
        raise PinMismatch('pin gap')
    if gap.get('scout_n_copied_into_settled_join_n') is not False:
        raise ScorecardPromotionRefused()
    if gap.get('admitted_at') is not None or frozen.get('admitted_at') is not None:
        raise AdmitPyRefused()
    if empty.get('fallback_join_n') is not None:
        raise ScorecardPromotionRefused()
    if listed_digest_match(pins) is not True:
        raise PinMismatch('pins')
    return {
        'frozen.results': None,
        'frozen.pnl': None,
        'empty.settled_join_n': None,
        'empty.occurrence_match_n': None,
        'empty.fallback_join_n': None,
        'empty.admit_ready_flag': None,
        'frozen.admitted_at': None,
    }


def _format_utc(moment):
    return moment.astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%fZ')


def _floor_epoch(moment):
    return int(moment.timestamp() // 1)


def _default_clock():
    return datetime.now(timezone.utc)


def _budget_doc_matches():
    path = REPO / BUDGET_DOC_REL
    return path.is_file() and sha256_file(path) == BUDGET_DOC_SHA256


def _grant_authorizes(grant, audit_slice=False):
    if not isinstance(grant, dict):
        return False
    seat = grant.get('seat') or grant.get('author')
    if seat != 'Collector':
        return False
    poller = grant.get('poller')
    audit = bool(audit_slice or grant.get('audit_slice') is True or grant.get('mode') == 'audit_slice')
    if poller == POLLER_NAME:
        return True
    return audit and poller in (None, POLLER_NAME, 'collector_audit')


def _approval_ok(value):
    return (
        isinstance(value, dict)
        and value.get('seat') == 'Conductor'
        and value.get('approves') == 'atp_rj_measure_audit_phase_b'
    )


def load_collector_grant(path, expected_sha):
    """Load a Collector grant. A sha mismatch or a non-Collector file fails closed."""
    if not isinstance(expected_sha, str) or len(expected_sha) != 64:
        raise BudgetGrantMissing('sha')
    raw = Path(path).read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if digest != expected_sha.lower():
        raise BudgetGrantMissing('sha')
    payload = json.loads(raw.decode('utf-8'))
    if not _grant_authorizes(payload):
        raise BudgetGrantMissing('grant')
    granted = dict(payload)
    granted['_path'] = str(Path(path))
    granted['_sha256'] = digest
    return granted


def _optional_number(value, default):
    if value is None:
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _endpoint_path(url):
    path = url.split('?', 1)[0]
    prefix = PUBLIC_ORIGIN + PUBLIC_PREFIX
    if path.startswith(prefix):
        path = path[len(prefix):]
    return path or '/'


def _is_list_endpoint(path):
    if path in LIST_ENDPOINT_PATHS:
        return True
    return path.startswith('/markets/') or path.startswith('/events/')


def _retry_after_seconds(headers):
    if not isinstance(headers, dict):
        return None
    raw = headers.get('Retry-After')
    if raw is None or raw == '':
        return None
    try:
        value = float(raw)
    except (TypeError, ValueError):
        return None
    if value < 0:
        return None
    if value == int(value):
        return int(value)
    return value


def _quiet_push(candidate):
    start = candidate.replace(hour=QUIET_START[0], minute=QUIET_START[1], second=0, microsecond=0)
    end = candidate.replace(hour=QUIET_END[0], minute=QUIET_END[1], second=0, microsecond=0)
    if start <= candidate < end:
        return end
    return candidate


class CollectorBudgetLimiter:
    """Pace atp_rj_measure at or below the Collector ceiling. Never above it."""

    def __init__(
        self,
        grant,
        clock,
        sleeper,
        raw_dir=None,
        recorder_capture=None,
        flag_dir=None,
        audit_slice=False,
        phase_b_approval=None,
    ):
        audit = bool(audit_slice or (isinstance(grant, dict) and grant.get('audit_slice') is True))
        if not _grant_authorizes(grant, audit_slice=audit):
            raise BudgetGrantMissing()
        self.grant = dict(grant)
        self.clock = clock or _default_clock
        self.sleeper = sleeper
        self.raw_dir = raw_dir
        self.recorder_capture = recorder_capture
        self.flag_dir = flag_dir
        self.audit_slice = audit or self.grant.get('mode') == 'audit_slice'
        approval = phase_b_approval if phase_b_approval is not None else self.grant.get('phase_b_approval')
        self.phase_b_approved = bool(self.grant.get('phase_b_audit_approved') is True or _approval_ok(approval))
        self.issued = []
        self.last_request_at = None
        self.cooldown_step = 0
        self.cooldown_until = None
        self.penalty_until = None
        self.storm_until = None
        self.recent_429s = []
        self.forced_phase_b = False
        self.force_reason = None
        self.storm_pauses = 0
        self.skipped_budget = 0
        self.skipped_cooldown = 0
        self.hours = {}
        self.run_started_unix = self.clock().timestamp()
        self._refresh_tripwire()
        self.phase_at_start = self._effective_phase(self.clock())
        self.phase_at_end = self.phase_at_start

    def _now(self):
        moment = self.clock()
        if moment.tzinfo is None:
            raise OrchestratorError('clock')
        return moment.astimezone(timezone.utc)

    def _refresh_tripwire(self):
        if self.forced_phase_b:
            return
        if self._flag_present():
            self.forced_phase_b = True
            self.force_reason = 'FORCE_PHASE_B'
            return
        try:
            count = self._recorder_429_since_start()
        except OrchestratorError:
            self.forced_phase_b = True
            self.force_reason = 'unreadable'
            return
        if count:
            self.forced_phase_b = True
            self.force_reason = 'recorder_429'

    def _flag_present(self):
        for folder in (self.flag_dir, self.raw_dir):
            if folder and (Path(folder) / 'FORCE_PHASE_B').is_file():
                return True
        return False

    def _recorder_429_since_start(self):
        if not self.recorder_capture:
            raise OrchestratorError('unreadable')
        path = Path(self.recorder_capture)
        if not path.is_file():
            raise OrchestratorError('unreadable')
        uri = 'file:' + path.resolve().as_posix() + '?mode=ro'
        try:
            connection = sqlite3.connect(uri, uri=True)
        except sqlite3.Error as exc:
            raise OrchestratorError('unreadable') from exc
        try:
            rows = connection.execute(
                'SELECT payload FROM responses WHERE ok=0 AND received >= ?',
                (self.run_started_unix,),
            ).fetchall()
        except sqlite3.Error as exc:
            raise OrchestratorError('unreadable') from exc
        finally:
            connection.close()
        count = 0
        for (payload,) in rows:
            if isinstance(payload, str) and 'HTTPError 429' in payload:
                count += 1
        return count

    def _calendar_phase(self, now):
        if now >= BUDGET_CLOSED_AT:
            return 'CLOSED'
        if now >= PHASE_B_START:
            return 'B'
        return 'A'

    def _effective_phase(self, now):
        phase = self._calendar_phase(now)
        if phase == 'CLOSED':
            return 'CLOSED'
        if phase == 'B' or self.forced_phase_b:
            return 'B'
        return 'A'

    def _penalty_active(self, now):
        return self.penalty_until is not None and now < self.penalty_until

    def _caps(self, phase, path, now):
        ceiling = PHASE_CEILING[phase]
        total_rpm = min(ceiling['total_rpm'], _optional_number(self.grant.get('total_rpm_max'), ceiling['total_rpm']))
        list_rpm = min(ceiling['list_rpm'], _optional_number(self.grant.get('list_endpoint_rpm_max'), ceiling['list_rpm']))
        floor = max(ceiling['min_spacing'], _optional_number(self.grant.get('min_spacing_s'), ceiling['min_spacing']))
        if self.audit_slice:
            total_rpm = min(total_rpm, AUDIT_CEILING['total_rpm'])
            list_rpm = min(list_rpm, AUDIT_CEILING['list_rpm'])
            floor = max(floor, AUDIT_CEILING['min_spacing'])
        if total_rpm <= 0 or ( _is_list_endpoint(path) and list_rpm <= 0):
            return None
        if _is_list_endpoint(path):
            spacing = max(floor, 60.0 / list_rpm, 60.0 / total_rpm)
        else:
            spacing = max(floor, 60.0 / total_rpm)
            list_rpm = None
        if self._penalty_active(now):
            spacing += PENALTY_SPACING_S
        return {
            'spacing': spacing,
            'list_rpm': list_rpm,
            'total_rpm': total_rpm,
        }

    def _in_window(self, now, only_list):
        found = []
        for moment, is_list in self.issued:
            if (now - moment).total_seconds() >= 60:
                continue
            if only_list and not is_list:
                continue
            found.append(moment)
        return found

    def _rpm_ready(self, now, cap, only_list):
        if cap is None:
            return now
        window = self._in_window(now, only_list)
        if len(window) < cap:
            return now
        ordered = sorted(window)
        boundary = ordered[len(ordered) - int(cap)]
        return boundary + timedelta(seconds=60)

    def _refusal(self, now, path):
        phase = self._effective_phase(now)
        if phase == 'CLOSED':
            return 'budget_closed'
        if self.audit_slice and phase == 'B' and not self.phase_b_approved:
            return 'audit_phase_b_pause'
        if self.audit_slice and not _is_list_endpoint(path):
            return 'audit_list_only'
        if self._caps(phase, path, now) is None:
            return 'grant_rpm_zero'
        return None

    def acquire(self, path):
        """Wait until a GET is inside the cap, or refuse without sending."""
        waited = 0.0
        while True:
            self._refresh_tripwire()
            now = self._now()
            phase = self._effective_phase(now)
            self.phase_at_end = phase
            refusal = self._refusal(now, path)
            if refusal:
                self.skipped_budget += 1
                return {
                    'ok': False,
                    'reason': refusal,
                    'spacing_now_s': None,
                    'waited_s': waited,
                    'phase': phase,
                }
            caps = self._caps(phase, path, now)
            earliest = now
            if self.last_request_at is not None:
                earliest = max(earliest, self.last_request_at + timedelta(seconds=caps['spacing']))
            earliest = max(earliest, self._rpm_ready(now, caps['total_rpm'], False))
            if caps['list_rpm'] is not None:
                earliest = max(earliest, self._rpm_ready(now, caps['list_rpm'], True))
            cooldown_hit = self.cooldown_until is not None and self.cooldown_until > now
            if cooldown_hit:
                earliest = max(earliest, self.cooldown_until)
            if self.storm_until is not None and self.storm_until > now:
                earliest = max(earliest, self.storm_until)
            earliest = _quiet_push(earliest)
            delay = (earliest - now).total_seconds()
            if delay <= 1e-9:
                self.issued.append((now, _is_list_endpoint(path)))
                self.last_request_at = now
                self._count_hour(now, 'requests')
                return {
                    'ok': True,
                    'reason': None,
                    'spacing_now_s': caps['spacing'],
                    'waited_s': waited,
                    'phase': phase,
                }
            if cooldown_hit:
                self.skipped_cooldown += 1
            before = now
            self.sleeper(delay)
            after = self._now()
            if after <= before:
                raise OrchestratorError('clock')
            waited += delay

    def _next_cooldown(self):
        value = COOLDOWN_BASE_S * (2 ** self.cooldown_step)
        if value > COOLDOWN_CAP_S:
            return COOLDOWN_CAP_S
        return value

    def note_429(self, path, retry_after, spacing_now_s):
        now = self._now()
        if retry_after is None:
            cooldown = self._next_cooldown()
        else:
            cooldown = retry_after
        self.cooldown_step += 1
        self.cooldown_until = now + timedelta(seconds=float(cooldown))
        self.penalty_until = now + timedelta(seconds=PENALTY_WINDOW_S)
        self.recent_429s.append(now)
        self._count_hour(now, 'http_429')
        self._append_jsonl('http_429.jsonl', {
            'ts_utc': _format_utc(now),
            'poller': POLLER_NAME,
            'path': path,
            'status': 429,
            'retry_after': retry_after,
            'spacing_now_s': spacing_now_s,
            'cooldown_s': cooldown,
        })
        self._maybe_storm(now)
        return cooldown

    def note_success(self):
        now = self._now()
        self.cooldown_step = 0
        self.cooldown_until = None
        self._count_hour(now, 'ok')

    def note_other(self):
        return None

    def _recent_429_count(self, now):
        return sum(1 for moment in self.recent_429s if (now - moment).total_seconds() <= STORM_WINDOW_S)

    def _maybe_storm(self, now):
        if self._recent_429_count(now) < STORM_429_COUNT:
            return
        if self.storm_until is not None and now < self.storm_until:
            return
        self.storm_until = now + timedelta(seconds=STORM_PAUSE_S)
        self.storm_pauses += 1
        self._append_jsonl('pause_429_storm.jsonl', {
            'event': 'PAUSE_429_STORM',
            'counts': self._recent_429_count(now),
            'pause_s': STORM_PAUSE_S,
            'ts_utc': _format_utc(now),
            'poller': POLLER_NAME,
        })

    def _count_hour(self, now, key):
        hour = now.strftime('%Y-%m-%dT%H')
        bucket = self.hours.setdefault(hour, {'requests': 0, 'ok': 0, 'http_429': 0})
        bucket[key] += 1

    def _append_jsonl(self, name, payload):
        if not self.raw_dir:
            return
        path = Path(self.raw_dir)
        path.mkdir(parents=True, exist_ok=True)
        with (path / name).open('a') as handle:
            handle.write(json.dumps(payload, sort_keys=True) + '\n')

    def write_hourly(self, raw_dir=None):
        folder = Path(raw_dir or self.raw_dir)
        folder.mkdir(parents=True, exist_ok=True)
        payload = {
            'poller': POLLER_NAME,
            'hours': [
                {'hour_utc': hour, 'requests': counts['requests'], 'ok': counts['ok'], 'http_429': counts['http_429']}
                for hour, counts in sorted(self.hours.items())
            ],
        }
        (folder / 'hourly.json').write_text(json.dumps(payload, indent=2, sort_keys=True) + '\n')

    def budget_report(self):
        return {
            'budget_doc_sha256': BUDGET_DOC_SHA256,
            'grant_path': self.grant.get('_path'),
            'grant_sha256': self.grant.get('_sha256'),
            'phase_at_start': self.phase_at_start,
            'phase_at_end': self.phase_at_end,
            'forced_phase_b': self.forced_phase_b,
            'storm_pauses': self.storm_pauses,
            'skipped_budget': self.skipped_budget,
            'skipped_cooldown': self.skipped_cooldown,
        }


def _empty_budget(grant=None):
    return {
        'budget_doc_sha256': BUDGET_DOC_SHA256,
        'grant_path': None if not isinstance(grant, dict) else grant.get('_path'),
        'grant_sha256': None if not isinstance(grant, dict) else grant.get('_sha256'),
        'phase_at_start': None,
        'phase_at_end': None,
        'forced_phase_b': False,
        'storm_pauses': 0,
        'skipped_budget': 0,
        'skipped_cooldown': 0,
    }


def _pct(value):
    encoded = []
    for byte in str(value).encode('utf-8'):
        if (48 <= byte <= 57) or (65 <= byte <= 90) or (97 <= byte <= 122) or byte in b'-._~':
            encoded.append(chr(byte))
        else:
            encoded.append(f'%{byte:02X}')
    return ''.join(encoded)


def _query(items):
    return '&'.join(f'{key}={_pct(value)}' for key, value in items)


def _markets_url(cursor, min_settled_ts):
    items = (
        ('limit', PAGE_LIMIT),
        ('series_ticker', SERIES),
        ('status', 'settled'),
        ('min_settled_ts', str(int(min_settled_ts))),
    )
    if cursor:
        items = items + (('cursor', cursor),)
    return PUBLIC_ORIGIN + PUBLIC_PREFIX + '/markets?' + _query(items)


def _events_url(cursor, min_close_ts):
    items = (
        ('limit', PAGE_LIMIT),
        ('series_ticker', SERIES),
        ('status', 'settled'),
        ('with_nested_markets', 'true'),
        ('min_close_ts', str(int(min_close_ts))),
    )
    if cursor:
        items = items + (('cursor', cursor),)
    return PUBLIC_ORIGIN + PUBLIC_PREFIX + '/events?' + _query(items)


def _guard_url(url):
    if not isinstance(url, str) or not url.startswith(PUBLIC_ORIGIN + PUBLIC_PREFIX + '/'):
        raise LiveOrdersForbidden()
    path = url.split('?', 1)[0]
    if path.rstrip('/').endswith('/orders') or '/orders/' in path:
        raise LiveOrdersForbidden()
    if path.rstrip('/').endswith('/portfolio') or '/portfolio/' in path:
        raise LiveOrdersForbidden()
    return url


def _split_https(url):
    prefix = 'https://'
    if not url.startswith(prefix):
        raise LiveOrdersForbidden()
    rest = url[len(prefix):]
    slash = rest.find('/')
    if slash < 0:
        raise LiveOrdersForbidden()
    return rest[:slash], rest[slash:]


def live_public_get(url):
    """One public GET. No auth header and no order route."""
    assert_public_get('GET')
    _guard_url(url)
    host, target = _split_https(url)
    if host != 'api.elections.kalshi.com':
        raise LiveOrdersForbidden()
    connection = http.client.HTTPSConnection(host, timeout=30)
    try:
        connection.request('GET', target, headers={'Accept': 'application/json'})
        response = connection.getresponse()
        body = response.read()
        retry_after = response.getheader('Retry-After')
        headers = {}
        if retry_after is not None:
            headers['Retry-After'] = retry_after
        return response.status, body, headers
    finally:
        connection.close()


def public_exchange(method, url, transport=None):
    """Dispatch one public GET. Any other verb is refused before a transport call."""
    assert_public_get(method)
    _guard_url(url)
    getter = live_public_get if transport is None else transport
    result = getter(url)
    if isinstance(result, (tuple, list)) and len(result) == 2:
        status, body = result
        headers = {}
    elif isinstance(result, (tuple, list)) and len(result) == 3:
        status, body, headers = result
        if headers is None:
            headers = {}
    else:
        raise OrchestratorError('body')
    if not isinstance(body, (bytes, bytearray)):
        raise OrchestratorError('body')
    if not isinstance(headers, dict):
        raise OrchestratorError('headers')
    return int(status), bytes(body), headers


def _utc_now():
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%fZ')


def _parse_utc(value):
    if not isinstance(value, str) or not value:
        raise OrchestratorError('timestamp')
    text = value[:-1] + '+00:00' if value.endswith('Z') else value
    parsed = datetime.fromisoformat(text)
    if parsed.tzinfo is None:
        raise OrchestratorError('timestamp')
    return parsed.astimezone(timezone.utc)


def _assert_measurement_out(path):
    candidate = Path(path)
    if not candidate.is_absolute():
        candidate = Path.cwd() / candidate
    resolved = candidate.resolve()
    repo = REPO.resolve()
    if resolved == repo or repo in resolved.parents:
        raise ScorecardPromotionRefused()
    return resolved


def _get_logged(url, transport, sleeper, http_log, raw_dir, label):
    last_status = None
    last_body = b''
    for attempt in range(MAX_GET_ATTEMPTS):
        backoff = None
        if attempt:
            backoff = BACKOFF_SECONDS[attempt - 1]
            sleeper(backoff)
        status, body, _headers = public_exchange('GET', url, transport)
        http_log.append({
            'utc': _utc_now(),
            'method': 'GET',
            'url': url,
            'http': status,
            'attempt': attempt,
            'bytes': len(body),
            'backoff_s': backoff,
            'label': label,
        })
        (Path(raw_dir) / f'{label}_attempt{attempt}.json').write_bytes(body)
        last_status = status
        last_body = body
        if status != 429:
            return status, body, attempt + 1
    return last_status, last_body, MAX_GET_ATTEMPTS


def _gap(kind, url, status, attempts, page_index, reason=None, backoffs=None):
    if backoffs is None:
        backoffs = list(BACKOFF_SECONDS[:max(attempts - 1, 0)]) if status == 429 else []
    gap = {
        'kind': kind,
        'url': url,
        'http': status,
        'attempts': attempts,
        'backoffs_s': list(backoffs),
        'filled': False,
        'markets_invented': False,
        'page_index': page_index,
    }
    if reason:
        gap['reason'] = reason
    return gap


def _split_get(result):
    if len(result) == 3:
        status, body, attempts = result
        return status, body, attempts, None, None
    if len(result) != 5:
        raise OrchestratorError('get')
    return result


def _get_logged_budget(url, transport, sleeper, http_log, raw_dir, label, limiter):
    """One logical GET under the Collector budget: at most one retry."""
    del sleeper
    path = _endpoint_path(url)
    backoffs = []
    last_status = None
    last_body = b''
    attempts_used = 0
    for attempt in range(MAX_LIVE_GET_ATTEMPTS):
        decision = limiter.acquire(path)
        if not decision['ok']:
            if attempts_used == 0:
                return None, b'', 0, backoffs, decision['reason']
            return last_status, last_body, attempts_used, backoffs, decision['reason']
        waited = decision.get('waited_s') or 0
        if attempt and waited:
            backoffs.append(waited)
        status, body, headers = public_exchange('GET', url, transport)
        attempts_used = attempt + 1
        http_log.append({
            'utc': _utc_now(),
            'method': 'GET',
            'url': url,
            'http': status,
            'attempt': attempt,
            'bytes': len(body),
            'backoff_s': waited if attempt else None,
            'label': label,
        })
        (Path(raw_dir) / f'{label}_attempt{attempt}.json').write_bytes(body)
        last_status = status
        last_body = body
        if status == 429:
            retry_after = _retry_after_seconds(headers)
            limiter.note_429(path, retry_after, decision['spacing_now_s'])
            if attempt + 1 < MAX_LIVE_GET_ATTEMPTS:
                continue
            return status, body, attempts_used, backoffs, None
        if status == 200:
            limiter.note_success()
        else:
            limiter.note_other()
        return status, body, attempts_used, backoffs, None
    return last_status, last_body, attempts_used, backoffs, None


def _page_collection(kind, url_for, transport, sleeper, http_log, raw_dir, getter=None):
    fetch = getter or _get_logged
    pages = []
    cursor = None
    page_index = 0
    while True:
        if page_index >= PAGE_CAP:
            url = url_for(cursor)
            return pages, _gap(kind, url, None, 0, page_index, reason='page_cap', backoffs=[])
        url = url_for(cursor)
        status, body, attempts, backoffs, stop_reason = _split_get(fetch(
            url, transport, sleeper, http_log, raw_dir, f'{kind}_p{page_index}'
        ))
        if status is None:
            return pages, _gap(
                kind, url, None, attempts, page_index,
                reason=stop_reason or 'not_sent', backoffs=backoffs or [],
            )
        if status != 200:
            return pages, _gap(kind, url, status, attempts, page_index, reason=stop_reason, backoffs=backoffs)
        try:
            payload = json.loads(body.decode('utf-8'))
        except json.JSONDecodeError:
            return pages, _gap(kind, url, status, attempts, page_index)
        if not isinstance(payload, dict):
            return pages, _gap(kind, url, status, attempts, page_index)
        pages.append(payload)
        cursor = payload.get('cursor') or ''
        if not cursor:
            return pages, None
        page_index += 1


def _markets_from_pages(pages):
    indexed = {}
    for page in pages:
        for market in page.get('markets') or []:
            if not isinstance(market, dict) or not market.get('ticker'):
                raise OrchestratorError('market')
            ticker = market['ticker']
            prior = indexed.get(ticker)
            if prior is not None and any(prior.get(field) != market.get(field) for field in AGREE_FIELDS):
                raise PinMismatch(ticker)
            indexed[ticker] = market
    return indexed


def _markets_from_events(pages):
    indexed = {}
    for page in pages:
        for event in page.get('events') or []:
            for market in event.get('markets') or []:
                if not isinstance(market, dict) or not market.get('ticker'):
                    raise OrchestratorError('market')
                ticker = market['ticker']
                prior = indexed.get(ticker)
                if prior is not None and any(prior.get(field) != market.get(field) for field in AGREE_FIELDS):
                    raise PinMismatch(ticker)
                indexed[ticker] = market
    return indexed


def _agree(left, right):
    for ticker, market in left.items():
        other = right.get(ticker)
        if other is None:
            continue
        for field in AGREE_FIELDS:
            if market.get(field) != other.get(field):
                raise PinMismatch(ticker)


def scout_pin_tickers():
    """The 30 scout tickers. They are excluded from the post-ACCEPT cohort."""
    _assert_digest(SCOUT_PATH, SCOUT_REGET_SHA256)
    scout = json.loads(SCOUT_PATH.read_bytes())
    tickers = [market.get('ticker') for market in scout.get('markets') or []]
    if len(tickers) != SCOUT_NONEMPTY_N_DECLARED or len(set(tickers)) != SCOUT_NONEMPTY_N_DECLARED:
        raise PinMismatch('scout N')
    return set(tickers)


def _j0_pass(market):
    return market.get('status') in FINALIZED_STATUSES and market.get('result') in FINALIZED_RESULTS


def _event_clocks_from(markets):
    clocks = {}
    for market in markets:
        occurrence = _occurrence_value(market)
        if occurrence is None:
            continue
        event = market.get('event_ticker')
        if event in clocks and clocks[event] != occurrence:
            raise OccurrenceIntegrityRefused()
        clocks[event] = occurrence
    return clocks


def _select_source(market_pages, market_gap, event_pages):
    from_markets = _markets_from_pages(market_pages)
    from_events = _markets_from_events(event_pages)
    _agree(from_markets, from_events)
    if market_gap is None:
        return list(from_markets.values()), 'markets_list'
    if not from_markets:
        return list(from_events.values()), 'events_nested'
    return list(from_markets.values()), 'markets_list_partial'


def _rows_of(pages, key):
    rows = []
    for page in pages:
        if key == 'markets':
            found = page.get('markets') or []
        else:
            found = []
            for event in page.get('events') or []:
                found.extend(event.get('markets') or [])
        for row in found:
            if isinstance(row, dict):
                rows.append(row)
    return rows


def _filter_observed(rows, predicate):
    if not rows:
        return 'UNOBSERVED'
    for row in rows:
        if not predicate(row):
            return 'OBSERVED_IGNORED'
    return 'OBSERVED_HONORED'


def _settlement_honors(min_settled_ts, market):
    raw = market.get('settlement_ts')
    if not raw:
        return False
    try:
        when = _parse_utc(raw)
    except OrchestratorError:
        return False
    return when.timestamp() > min_settled_ts


def _close_honors(min_close_ts, market):
    raw = market.get('close_time')
    if raw is None:
        raw = market.get('close_ts')
    if not raw:
        return False
    try:
        when = _parse_utc(raw) if isinstance(raw, str) else None
    except OrchestratorError:
        return False
    if when is None:
        try:
            stamp = float(raw)
        except (TypeError, ValueError):
            return False
        return stamp > min_close_ts
    return when.timestamp() > min_close_ts


def _server_filter(kind, pages, gap, min_settled_ts, min_close_ts, requested):
    if not requested:
        return {'param': None, 'value': None, 'observed': 'NOT_APPLIED'}
    if gap is not None and gap.get('http') == 400:
        if kind == 'markets':
            return {'param': 'min_settled_ts', 'value': int(min_settled_ts), 'observed': 'REJECTED_400'}
        return {'param': 'min_close_ts', 'value': int(min_close_ts), 'observed': 'REJECTED_400'}
    if kind == 'markets':
        observed = _filter_observed(_rows_of(pages, 'markets'), lambda row: _settlement_honors(min_settled_ts, row))
        return {'param': 'min_settled_ts', 'value': int(min_settled_ts), 'observed': observed}
    observed = _filter_observed(_rows_of(pages, 'events'), lambda row: _close_honors(min_close_ts, row))
    return {'param': 'min_close_ts', 'value': int(min_close_ts), 'observed': observed}


def _endpoint_pull_status(requested, pages, gap, server_filter):
    if not requested:
        return {
            'requested': False,
            'status': 'NOT_REQUESTED',
            'pages_ok': 0,
            'last_http': None,
            'gap_page_index': None,
            'server_filter': server_filter,
        }
    pages_ok = len(pages)
    if gap is None:
        status = 'COMPLETE'
        gap_page = None
        last_http = 200 if pages_ok else None
    else:
        status = 'PARTIAL' if pages_ok else 'FAILED'
        gap_page = gap.get('page_index')
        last_http = gap.get('http')
    return {
        'requested': True,
        'status': status,
        'pages_ok': pages_ok,
        'last_http': last_http,
        'gap_page_index': gap_page,
        'server_filter': server_filter,
    }


def _cohort_completeness(cohort_source, market_pages, market_gap, event_pages, event_gap):
    gaps = [gap for gap in (market_gap, event_gap) if gap is not None]
    if cohort_source == 'events_nested':
        selected_pages = event_pages
    else:
        selected_pages = market_pages
    if not market_pages and not event_pages:
        return 'INCOMPLETE'
    if not gaps:
        return 'COMPLETE'
    if selected_pages:
        return 'PARTIAL'
    return 'INCOMPLETE'


def _not_requested_filter():
    return {'param': None, 'value': None, 'observed': 'NOT_APPLIED'}


def _write_measure(destination, raw_dir, payload, http_log, limiter):
    if payload['admitted_at'] is not None or payload['results'] is not None or payload['pnl'] is not None:
        raise ScorecardPromotionRefused()
    if payload['scout_n_copied_into_settled_join_n'] is not False:
        raise ScorecardPromotionRefused()
    text = json.dumps(payload, indent=2, sort_keys=True) + '\n'
    destination.write_text(text)
    log_path = raw_dir / 'http_log.jsonl'
    with log_path.open('w') as handle:
        for entry in http_log:
            handle.write(json.dumps(entry, sort_keys=True) + '\n')
    if limiter is not None:
        limiter.write_hourly(raw_dir)
    return payload


def _stopped_measure(since, since_utc, destination, raw_dir, live_fetch, stop_reason, grant, rate_policy):
    gap = _gap('budget', None, None, 0, None, reason=stop_reason, backoffs=[])
    pull = _endpoint_pull_status(False, [], None, _not_requested_filter())
    payload = {
        'experiment_id': EXPERIMENT_ID,
        'mode': 'measurement',
        'since': since,
        'since_utc': since_utc.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        'accept_issued_at_utc': ACCEPT_ISSUED_AT_UTC,
        'host': PUBLIC_ORIGIN + PUBLIC_PREFIX,
        'series_ticker': SERIES,
        'method': 'GET',
        'live_fetch': live_fetch,
        'cohort_source': None,
        'cohort_source_qualified': 'INCOMPLETE',
        'cohort_completeness': 'INCOMPLETE',
        'pull_status': {'markets': pull, 'events': pull},
        'counts_label': 'INCOMPLETE',
        'counts_are_lower_bounds': True,
        'zero_with_gaps': True,
        'rate_policy': rate_policy,
        'budget': _empty_budget(grant),
        'stop_reason': stop_reason,
        'settled_join_n': 0,
        'occurrence_match_n': 0,
        'fallback_join_n': 0,
        'cohort_tickers': [],
        'rows': [],
        'excluded': [],
        'gaps': [gap],
        'events_page2_backfilled': False,
        'list_429_backfilled': False,
        'markets_invented': False,
        'scout_nonempty_result_N_declared': SCOUT_NONEMPTY_N_DECLARED,
        'scout_n_copied_into_settled_join_n': False,
        'admitted_at': None,
        'admit_ready': ADMIT_READY_PENDING,
        'admit_ready_flag': None,
        'results': None,
        'pnl': None,
        'http_log': [],
    }
    return _write_measure(destination, raw_dir, payload, [], None)


def _resolve_grant(grant, budget_grant, budget_grant_sha256):
    if grant is not None:
        return grant
    if not budget_grant:
        return None
    try:
        return load_collector_grant(budget_grant, budget_grant_sha256)
    except (OSError, json.JSONDecodeError, BudgetGrantMissing, UnicodeError):
        return None


def measure(
    since,
    out,
    transport=None,
    sleeper=None,
    limiter=None,
    clock=None,
    grant=None,
    budget_grant=None,
    budget_grant_sha256=None,
    recorder_capture=None,
    audit_slice=False,
    phase_b_approval=None,
    rate_policy=None,
):
    """Page settled KXATPMATCH markets and count the post-ACCEPT join.

    Counts are written only to `out`. The committed scorecard is not updated.
    `admitted_at` stays null. Admit stays pending Clock.
    """
    since_utc = _parse_utc(since)
    live_fetch = transport is None
    if rate_policy == RATE_POLICY_LEGACY and live_fetch:
        raise LegacyStubLiveRefused(RATE_POLICY_LEGACY)
    destination = _assert_measurement_out(out)
    destination.parent.mkdir(parents=True, exist_ok=True)
    raw_dir = destination.with_name(destination.stem + '_raw')
    raw_dir.mkdir(parents=True, exist_ok=True)
    if sleeper is None:
        sleeper = time.sleep
    resolved_grant = _resolve_grant(grant, budget_grant, budget_grant_sha256)
    use_legacy = limiter is None and not live_fetch and rate_policy != RATE_POLICY_BUDGET
    if rate_policy == RATE_POLICY_LEGACY:
        use_legacy = True
    if live_fetch:
        use_legacy = False
        if not _budget_doc_matches() or resolved_grant is None:
            reason = 'BUDGET_GRANT_MISSING' if _budget_doc_matches() else 'BUDGET_DOC_MISMATCH'
            return _stopped_measure(
                since, since_utc, destination, raw_dir, True, reason, resolved_grant, RATE_POLICY_BUDGET,
            )
        if limiter is None:
            limiter = CollectorBudgetLimiter(
                resolved_grant,
                clock or _default_clock,
                sleeper,
                raw_dir=raw_dir,
                recorder_capture=recorder_capture,
                flag_dir=destination.parent,
                audit_slice=audit_slice,
                phase_b_approval=phase_b_approval,
            )
    if limiter is not None and not use_legacy:
        limiter.raw_dir = raw_dir
        if limiter.flag_dir is None:
            limiter.flag_dir = destination.parent
        if recorder_capture and limiter.recorder_capture is None:
            limiter.recorder_capture = recorder_capture
        if limiter.sleeper is None:
            limiter.sleeper = sleeper
        limiter._refresh_tripwire()
        if not limiter.issued:
            limiter.phase_at_start = limiter._effective_phase(limiter._now())
            limiter.phase_at_end = limiter.phase_at_start

        def getter(url, transport, sleeper, http_log, raw_dir, label, _limiter=limiter):
            return _get_logged_budget(url, transport, sleeper, http_log, raw_dir, label, _limiter)

        active_policy = RATE_POLICY_BUDGET
    else:
        getter = None
        active_policy = RATE_POLICY_LEGACY
        limiter = None
    min_settled_ts = _floor_epoch(since_utc)
    min_close_ts = min_settled_ts - EVENTS_LOOKBACK_S

    def markets_url(cursor, _ts=min_settled_ts):
        return _markets_url(cursor, _ts)

    def events_url(cursor, _ts=min_close_ts):
        return _events_url(cursor, _ts)

    http_log = []
    market_pages, market_gap = _page_collection(
        'markets', markets_url, transport, sleeper, http_log, raw_dir, getter=getter,
    )
    event_pages = []
    event_gap = None
    events_requested = market_gap is not None
    if events_requested:
        event_pages, event_gap = _page_collection(
            'events', events_url, transport, sleeper, http_log, raw_dir, getter=getter,
        )
    received, cohort_source = _select_source(market_pages, market_gap, event_pages)
    scout_tickers = scout_pin_tickers()
    excluded = []
    cohort = []
    for market in received:
        ticker = market.get('ticker')
        if ticker in scout_tickers:
            excluded.append({'ticker': ticker, 'reason': 'scout_pin'})
            continue
        settlement = market.get('settlement_ts')
        if not settlement:
            excluded.append({'ticker': ticker, 'reason': 'settlement_ts_absent'})
            continue
        try:
            when = _parse_utc(settlement)
        except OrchestratorError:
            excluded.append({'ticker': ticker, 'reason': 'settlement_ts_absent'})
            continue
        if when <= since_utc:
            excluded.append({'ticker': ticker, 'reason': 'settled_at_or_before_since'})
            continue
        if not _j0_pass(market):
            excluded.append({'ticker': ticker, 'reason': 'j0_not_nonempty'})
            continue
        cohort.append(market)
    clocks = _event_clocks_from(cohort)
    rows = []
    for market in cohort:
        label = j1_label(market, clocks.get(market.get('event_ticker')))
        label['j0'] = 'nonempty_result_required_pass'
        label['result'] = market.get('result')
        label['status'] = market.get('status')
        label['settlement_ts'] = market.get('settlement_ts')
        rows.append(label)
    if any(row['key'] in scout_tickers for row in rows):
        raise ScorecardPromotionRefused()
    rows.sort(key=lambda row: row['key'] or '')
    occurrence_match_n = sum(1 for row in rows if row['join_source'] == JOIN_SOURCE_OCCURRENCE)
    fallback_join_n = sum(1 for row in rows if row['join_source'] == JOIN_SOURCE_FALLBACK)
    settled_join_n = len(rows)
    if occurrence_match_n + fallback_join_n != settled_join_n:
        raise OrchestratorError('j1 partition')
    gaps = [gap for gap in (market_gap, event_gap) if gap is not None]
    for gap in gaps:
        if gap.get('filled') is not False or gap.get('markets_invented') is not False:
            raise InventedMarketRefused()
    completeness = _cohort_completeness(cohort_source, market_pages, market_gap, event_pages, event_gap)
    counts_label = 'COMPLETE' if completeness == 'COMPLETE' else 'INCOMPLETE'
    markets_filter = _server_filter('markets', market_pages, market_gap, min_settled_ts, min_close_ts, True)
    events_filter = _server_filter(
        'events', event_pages, event_gap, min_settled_ts, min_close_ts, events_requested,
    )
    payload = {
        'experiment_id': EXPERIMENT_ID,
        'mode': 'measurement',
        'since': since,
        'since_utc': since_utc.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        'accept_issued_at_utc': ACCEPT_ISSUED_AT_UTC,
        'host': PUBLIC_ORIGIN + PUBLIC_PREFIX,
        'series_ticker': SERIES,
        'method': 'GET',
        'live_fetch': live_fetch,
        'cohort_source': cohort_source,
        'cohort_source_qualified': f'{cohort_source}:{completeness}',
        'cohort_completeness': completeness,
        'pull_status': {
            'markets': _endpoint_pull_status(True, market_pages, market_gap, markets_filter),
            'events': _endpoint_pull_status(events_requested, event_pages, event_gap, events_filter),
        },
        'counts_label': counts_label,
        'counts_are_lower_bounds': bool(gaps),
        'zero_with_gaps': settled_join_n == 0 and bool(gaps),
        'rate_policy': active_policy,
        'budget': limiter.budget_report() if limiter is not None else _empty_budget(resolved_grant),
        'stop_reason': None,
        'settled_join_n': settled_join_n,
        'occurrence_match_n': occurrence_match_n,
        'fallback_join_n': fallback_join_n,
        'cohort_tickers': [row['key'] for row in rows],
        'rows': rows,
        'excluded': excluded,
        'gaps': gaps,
        'events_page2_backfilled': False,
        'list_429_backfilled': False,
        'markets_invented': False,
        'scout_nonempty_result_N_declared': SCOUT_NONEMPTY_N_DECLARED,
        'scout_n_copied_into_settled_join_n': False,
        'admitted_at': None,
        'admit_ready': ADMIT_READY_PENDING,
        'admit_ready_flag': None,
        'results': None,
        'pnl': None,
        'http_log': http_log,
    }
    return _write_measure(destination, raw_dir, payload, http_log, limiter)


def main(argv=None):
    """CLI. `measure` writes an output file. `admit` is refused."""
    import sys
    args = list(sys.argv[1:] if argv is None else argv)
    if not args:
        raise SystemExit(2)
    if args[0] in ('admit', 'admit.py'):
        run_admit()
    if args[0] != 'measure':
        raise OrchestratorError(args[0])
    since = None
    out = None
    budget_grant = None
    budget_grant_sha256 = None
    recorder_capture = None
    phase_b_approval = None
    audit_slice = False
    index = 1
    while index < len(args):
        if args[index] == '--since' and index + 1 < len(args):
            since = args[index + 1]
            index += 2
            continue
        if args[index] == '--out' and index + 1 < len(args):
            out = args[index + 1]
            index += 2
            continue
        if args[index] == '--budget-grant' and index + 1 < len(args):
            budget_grant = args[index + 1]
            index += 2
            continue
        if args[index] == '--budget-grant-sha256' and index + 1 < len(args):
            budget_grant_sha256 = args[index + 1]
            index += 2
            continue
        if args[index] == '--recorder-capture' and index + 1 < len(args):
            recorder_capture = args[index + 1]
            index += 2
            continue
        if args[index] == '--audit-slice':
            audit_slice = True
            index += 1
            continue
        if args[index] == '--phase-b-approval' and index + 1 < len(args):
            approval_path = args[index + 1]
            index += 2
            if index >= len(args) or args[index] != '--phase-b-approval-sha256' or index + 1 >= len(args):
                raise OrchestratorError('phase-b-approval')
            expected = args[index + 1]
            index += 2
            raw = Path(approval_path).read_bytes()
            digest = hashlib.sha256(raw).hexdigest()
            if digest != expected or not _approval_ok(json.loads(raw.decode('utf-8'))):
                raise BudgetGrantMissing('approval')
            phase_b_approval = json.loads(raw.decode('utf-8'))
            continue
        raise OrchestratorError(args[index])
    if not since or not out:
        raise OrchestratorError('measure')
    payload = measure(
        since,
        out,
        budget_grant=budget_grant,
        budget_grant_sha256=budget_grant_sha256,
        recorder_capture=recorder_capture,
        audit_slice=audit_slice,
        phase_b_approval=phase_b_approval,
    )
    if payload.get('stop_reason') == 'BUDGET_GRANT_MISSING':
        raise SystemExit('BUDGET_GRANT_MISSING')
    return payload


if __name__ == '__main__':
    main()
