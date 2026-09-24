"""C4 KXCPI settled-resolution join harness.

Measurement only. One knob: join_gate. This module does not edit CPI-FQ,
the C1 honesty lab, the C1 EMPTY-OB lab, feebook, rails, Cap-SR, any FQ
sibling, or a closed RJ harness. It does not place orders, does not read
Logan keys, does not run the admit tool, and does not write scorecard
metrics.

J0 requires a nonempty official result on an already-settled market.
J1 uses occurrence_datetime when that field is present. When it is null,
the row is labeled join_source expected_expiration_time_fallback. The
fallback clock is never written into occurrence_datetime. Raw values stay
as returned. Scout N=25 is a pin and is not settled_join_n. admitted_at
stays null. Fee, queue, book, fill, and tape metrics stay held.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent

LAB_DIRECTORY = 'kalshi_c4_kxcpi_settled_join_lab_20260924'
EXPERIMENT_ID = 'C4-KXCPI-SETTLED-RESOLUTION-JOIN-HARNESS'
FEATURE_FAMILY = 'C4-RJ'
PANEL_VERSION = '2026-09-23.c4-kxcpi-v0'
SERIES = 'KXCPI'
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
SCOUT_NONEMPTY_N_DECLARED = 25
PANEL_EVENTS_N = 4
PANEL_MARKETS_N = 44
PARENT_MISSING_OCCURRENCE_N = 21
PANEL_SHA256 = 'b20b0cbee50c127d2e9bb2548b574b7d643cc708f54019d53bd91775f9762c13'
CITED_FREEZE_SHA256 = '5e37f81a8959e83c3d2c0c42739e1ca6c127c748442ac6fe28c0013edee12e2f'
ACCEPT_SHA256 = '8a86ae6b9dfb0e80d80de8404750501e44aeb873e7f31789ece5fddf8dd03fc5'
SCOUT_REGET_SHA256 = 'bb72a2ebfa942026913687e4c040a9def598b5080294a346d71f8f7283ab5f7f'
SEED_SUMMARY_SHA256 = '8b749373c6949a1aa40b6852e313b0c626da0d0623fcafe167a8196ec228e0bf'
SETTLED_REGET_SHA256 = '235c9dad7d244db4c91152c8ae3f6d043f6732d31f99b05bc836abaf2f5d3f56'
EXAMINER_HOLD_SHA256 = '8625cb4906b6dd1dd02bf2648178c8c3ae08c0d407cd9ca29bbe9f67bbb59dfd'
MAXIMIZE_PIN_SHA256 = '4ee450ffe2b99154c08fd8619892ca2dc8efec92fb036fad2ad70d5c6e003e2f'
FEEBOOK_COMMIT = '22371178cb2663250b4762f328069571c48cb551'
RAILS_COMMIT = '6a28e0d6254327ea4e6451c781bec56215ac6cac'
BASE_COMMIT = '34a2720218b4f4f2d6dd0cbde6334ee672a3684b'
OUTPUT_KEYS = (
    'settled_join_n',
    'occurrence_match_n',
    'admit_ready_flag',
    'results',
    'pnl',
)
DOES_NOT_UNGATE = ('S1', 'S2', 'R2-P4')
MISSING_EVENTS = ('KXCPI-26JUN', 'KXCPI-26MAY', 'KXCPI-26APR')
SETTLED_EVENTS = ('KXCPI-26AUG', 'KXCPI-26JUL')
PARENT_EVENTS = ('KXCPI-26OCT', 'KXCPI-26DEC', 'KXCPI-26SEP', 'KXCPI-26NOV')
LIST_BOOK_ROUTES = (
    'GET /markets?series_ticker=KXCPI&status=settled&limit=20',
    'GET /events?series_ticker=KXCPI&status=settled&limit=5&with_nested_markets=true',
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
    'cpi_fq_reopen': 'CPI-FQ stays closed',
    'c1_rj_reopen': 'C1-RJ stays closed',
    'c3_rj_reopen': 'C3-RJ stays closed',
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
    'backfill_missing_events': 'KXCPI-26JUN/26MAY/26APR stay missing',
    'copy_scout_n': 'scout N is not settled_join_n',
    'fee_metric': 'C4 fee metric stays HELD',
    'queue_metric': 'C4 queue metric stays HELD',
    'book_metric': 'C4 book metric stays HELD',
    'fill_metric': 'C4 fill metric stays HELD',
    'tape_metric': 'C4 tape metric stays HELD',
}
CAPTURE_PANEL = REPO / 'lab/astra-capture/c4-kxcpi/panel_stub.json'
GOV_PANEL = REPO / 'lab/governance/astra/packets/C4_KXCPI_PANEL_STUB_2026-09-23.json'
SCOUT_DIR = REPO / 'lab/governance/astra/packets/scout_c4_settled_rejoin_2026-09-24'
SCOUT_PANEL = SCOUT_DIR / 'C4_KXCPI_PANEL_STUB_2026-09-23.json'
SCOUT_PATH = SCOUT_DIR / 'scout_settled_rejoin_C4_KXCPI.json'
REGET_PATH = SCOUT_DIR / 'settled_reget_2026-09-24.json'
CAPTURE_REGET = REPO / 'lab/astra-capture/c4-kxcpi/settled_reget_2026-09-24.json'
SEED_PATH = SCOUT_DIR / 'SEED_SETTLED_SUMMARY.json'
FREEZE_PATH = REPO / 'lab/governance/astra/packets/C4_KXCPI_SETTLED_RESOLUTION_JOIN_HARNESS_FREEZE_2026-09-24.md'
ACCEPT_PATH = REPO / 'lab/governance/astra/packets/CONDUCTOR_ACCEPT_C4_KXCPI_SETTLED_JOIN_HARNESS_2026-09-24.json'
HOLD_PATH = REPO / 'lab/governance/astra/packets/EXAMINER_HOLD_C4_KXCPI_SETTLED_JOIN_HARNESS_PRE_PR_2026-09-24.json'
MAXIMIZE_PATH = REPO / 'lab/governance/astra/packets/MAXIMIZE_PIN_2026-09-24_1926ET.md'
LAB_PANEL = ROOT / 'C4_KXCPI_PANEL_STUB_2026-09-23.json'
PIN_GAP_PATH = ROOT / 'PIN_GAP.json'
EMPTY_RESULTS = ROOT / 'results/EMPTY_RESULTS.json'
FROZEN_EXPERIMENT = ROOT / 'FROZEN_EXPERIMENT.json'
SOURCE_PINS = ROOT / 'SOURCE_PINS.json'
SOURCE_PIN_MIRRORS = (
    ROOT / 'SOURCE_PINS.json',
    ROOT / 'C4_KXCPI_SETTLED_RESOLUTION_JOIN_HARNESS/SOURCE_PINS.json',
    REPO / 'packets/C4_KXCPI_SETTLED_JOIN_HARNESS/SOURCE_PINS.json',
    REPO / 'lab/astra-science/kalshi_c4_kxcpi_settled_join_lab_20260924/SOURCE_PINS.json',
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
    """GET is the only public capture verb. This function does not open a socket."""
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
    """admit_ready_flag stays null."""
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
    """The C4 fee metric stays held."""
    del market, value
    raise AdversaryRefused(ADVERSARY_LABELS['fee_metric'])


def queue_metric(market=None, value=None):
    """The C4 queue metric stays held."""
    del market, value
    raise InventedDepthRefused()


def book_metric(market=None, value=None):
    """The C4 book metric stays held."""
    del market, value
    raise InventedDepthRefused()


def tape_metric(market=None, value=None):
    """The C4 tape metric stays held."""
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


def backfill_missing_events(event_ticker=None, markets=None):
    """KXCPI-26JUN, KXCPI-26MAY, and KXCPI-26APR stay missing."""
    del event_ticker, markets
    raise InventedMarketRefused()


def assign_occurrence(ticker=None, value=None):
    """occurrence_datetime is not invented, and expected_expiration_time is not written into it."""
    del ticker, value
    raise InventedSoTRefused()


def copy_scout_n_into_settled_join(value=None):
    """The declared scout N=25 is not the scorecard count."""
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
    if label == 'backfill_missing_events':
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
    """Governance, scout, and lab copies are the capture panel bytes."""
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
        return row
    row['join_source'] = JOIN_SOURCE_FALLBACK
    row['clock'] = 'expected_expiration_time'
    if row['occurrence_datetime'] is not None:
        raise InventedSoTRefused()
    if row['occurrence_datetime'] == expected and expected is not None:
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
    if tuple(reget.get('events_listed_without_nested_markets') or ()) != MISSING_EVENTS:
        raise InventedMarketRefused()
    if tuple(reget.get('events_with_nested_settled_markets') or ()) != SETTLED_EVENTS:
        raise PinMismatch('settled events')
    if scout.get('settled_list_http') != '429_honest':
        raise PinMismatch('settled list')
    if scout.get('list_embed_vs_single_event_match') is not True:
        raise PinMismatch('list embed')
    if scout.get('occurrence_datetime_present_on_settled_N') != SCOUT_NONEMPTY_N_DECLARED:
        raise PinMismatch('occurrence present')
    if scout.get('occurrence_datetime_equals_expected_expiration_N') != 0:
        raise PinMismatch('clock reconcile')
    reget_index = _index_by_ticker(reget_markets)
    raw_index = {}
    for event_ticker, filename in (
        ('KXCPI-26AUG', 'event_KXCPI_26AUG.json'),
        ('KXCPI-26JUL', 'event_KXCPI_26JUL.json'),
    ):
        raw_index.update(_index_by_ticker(_raw_event_markets(SCOUT_DIR / 'raw' / filename)))
        del event_ticker
    list_payload = json.loads((SCOUT_DIR / 'raw/events_settled_KXCPI_lim5_retry1.json').read_bytes())
    listed = list_payload.get('events') or []
    missing = tuple(
        event.get('event_ticker')
        for event in listed
        if event.get('markets') is None
    )
    if missing != MISSING_EVENTS:
        raise InventedMarketRefused()
    list_index = {}
    for event in listed:
        nested = event.get('markets')
        if nested:
            list_index.update(_index_by_ticker(nested))
    clocks = {}
    for market in markets:
        ticker = market.get('ticker')
        result = market.get('result')
        status = market.get('status')
        if status != 'finalized' or result not in FINALIZED_RESULTS:
            raise InventedResultRefused()
        occurrence = market.get('occurrence_datetime')
        expected = market.get('expected_expiration_time')
        if occurrence is None or expected is None or occurrence == expected:
            raise OccurrenceIntegrityRefused()
        sibling = reget_index.get(ticker)
        raw = raw_index.get(ticker)
        embedded = list_index.get(ticker)
        for other in (sibling, raw, embedded):
            if other is None:
                raise PinMismatch(ticker)
            if other.get('result') != result or other.get('status') != status:
                raise PinMismatch(ticker)
            if other.get('occurrence_datetime') != occurrence:
                raise PinMismatch(ticker)
            if other.get('expected_expiration_time') != expected:
                raise PinMismatch(ticker)
        clocks.setdefault(market.get('event_ticker'), set()).add(occurrence)
    for event_ticker, values in clocks.items():
        if event_ticker not in SETTLED_EVENTS or len(values) != 1:
            raise OccurrenceIntegrityRefused()
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
            raise InventedSoTRefused()
        label['j0'] = j0
        label['cohort'] = 'settled_reget'
        label['result'] = observed
        label['status'] = market.get('status')
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
        if label['join_source'] == JOIN_SOURCE_FALLBACK:
            if label['occurrence_datetime'] is not None:
                raise InventedSoTRefused()
        parent_rows.append(label)
    fallback_n = sum(1 for row in parent_rows if row['join_source'] == JOIN_SOURCE_FALLBACK)
    if len(rows) != SCOUT_NONEMPTY_N_DECLARED:
        raise OrchestratorError('settled rows')
    if len(parent_rows) != PANEL_MARKETS_N or fallback_n != PARENT_MISSING_OCCURRENCE_N:
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
        if accept.get('implement') is not True:
            raise PinMismatch('accept')
        if sha256_file(ACCEPT_PATH) != ACCEPT_SHA256:
            raise PinMismatch('accept')
    hold_present = HOLD_PATH.is_file() and sha256_file(HOLD_PATH) == EXAMINER_HOLD_SHA256
    maximize_present = MAXIMIZE_PATH.is_file() and sha256_file(MAXIMIZE_PATH) == MAXIMIZE_PIN_SHA256
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
        'digest_all_match_claimed': claimed is True,
        'cited_freeze_sha256': CITED_FREEZE_SHA256,
    }


def list_books():
    """Settled-list 429s and the three unlistable events stay empty."""
    return {
        'routes': list(LIST_BOOK_ROUTES),
        'books_present': False,
        'list_429_backfilled': False,
        'markets_invented': False,
        'missing_events': list(MISSING_EVENTS),
        'missing_events_backfilled': False,
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
        'missing_events_backfilled': False,
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
    if listed_digest_match(pins) is not True:
        raise PinMismatch('pins')
    return {
        'frozen.results': None,
        'frozen.pnl': None,
        'empty.settled_join_n': None,
        'empty.occurrence_match_n': None,
        'empty.admit_ready_flag': None,
        'frozen.admitted_at': None,
    }
