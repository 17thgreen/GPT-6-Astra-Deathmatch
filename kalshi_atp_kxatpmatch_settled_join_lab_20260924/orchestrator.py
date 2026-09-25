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
"""
import hashlib
import http.client
import json
import time
from datetime import datetime, timezone
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


def _markets_url(cursor):
    items = (
        ('limit', PAGE_LIMIT),
        ('series_ticker', SERIES),
        ('status', 'settled'),
    )
    if cursor:
        items = items + (('cursor', cursor),)
    return PUBLIC_ORIGIN + PUBLIC_PREFIX + '/markets?' + _query(items)


def _events_url(cursor):
    items = (
        ('limit', PAGE_LIMIT),
        ('series_ticker', SERIES),
        ('status', 'settled'),
        ('with_nested_markets', 'true'),
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
        return response.status, body
    finally:
        connection.close()


def public_exchange(method, url, transport=None):
    """Dispatch one public GET. Any other verb is refused before a transport call."""
    assert_public_get(method)
    _guard_url(url)
    getter = live_public_get if transport is None else transport
    status, body = getter(url)
    if not isinstance(body, (bytes, bytearray)):
        raise OrchestratorError('body')
    return int(status), bytes(body)


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
        status, body = public_exchange('GET', url, transport)
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


def _gap(kind, url, status, attempts, page_index):
    backoffs = list(BACKOFF_SECONDS[:max(attempts - 1, 0)]) if status == 429 else []
    return {
        'kind': kind,
        'url': url,
        'http': status,
        'attempts': attempts,
        'backoffs_s': backoffs,
        'filled': False,
        'markets_invented': False,
        'page_index': page_index,
    }


def _page_collection(kind, url_for, transport, sleeper, http_log, raw_dir):
    pages = []
    cursor = None
    page_index = 0
    while True:
        url = url_for(cursor)
        status, body, attempts = _get_logged(
            url, transport, sleeper, http_log, raw_dir, f'{kind}_p{page_index}'
        )
        if status != 200:
            return pages, _gap(kind, url, status, attempts, page_index)
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


def measure(since, out, transport=None, sleeper=None):
    """Page settled KXATPMATCH markets and count the post-ACCEPT join.

    Counts are written only to `out`. The committed scorecard is not updated.
    `admitted_at` stays null. Admit stays pending Clock.
    """
    since_utc = _parse_utc(since)
    destination = _assert_measurement_out(out)
    destination.parent.mkdir(parents=True, exist_ok=True)
    raw_dir = destination.with_name(destination.stem + '_raw')
    raw_dir.mkdir(parents=True, exist_ok=True)
    if sleeper is None:
        sleeper = time.sleep
    http_log = []
    market_pages, market_gap = _page_collection(
        'markets', _markets_url, transport, sleeper, http_log, raw_dir
    )
    event_pages, event_gap = _page_collection(
        'events', _events_url, transport, sleeper, http_log, raw_dir
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
    payload = {
        'experiment_id': EXPERIMENT_ID,
        'mode': 'measurement',
        'since': since,
        'since_utc': since_utc.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        'accept_issued_at_utc': ACCEPT_ISSUED_AT_UTC,
        'host': PUBLIC_ORIGIN + PUBLIC_PREFIX,
        'series_ticker': SERIES,
        'method': 'GET',
        'live_fetch': transport is None,
        'cohort_source': cohort_source,
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
    return payload


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
        raise OrchestratorError(args[index])
    if not since or not out:
        raise OrchestratorError('measure')
    return measure(since, out)


if __name__ == '__main__':
    main()
