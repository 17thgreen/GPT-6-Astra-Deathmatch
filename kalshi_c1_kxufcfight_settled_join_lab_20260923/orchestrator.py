"""C1 KXUFCFIGHT settled-resolution join harness.

Measurement only. One knob: join_gate. This module does not edit the C1
honesty lab, the C1 EMPTY-OB lab, feebook, rails, Cap-SR, any FQ sibling,
or the closed RJ harnesses. It does not place orders, does not read Logan
keys, does not run the admit tool, and does not write scorecard metrics.

The cited freeze, Conductor ACCEPT, 1750 ET maximize pin, and scout reget
were absent from this checkout. They are not regenerated. digest ALL_MATCH
is not claimed. The panel parent is the existing admitted-panel bytes.
J1 reads occurrence_datetime on those four seeds and does not invent one.
Scout N=4 is a declared pin and is not copied into settled_join_n.
Settled, finalized, and events list books are not invented. Empty captured
orderbooks are not filled.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent

LAB_DIRECTORY = 'kalshi_c1_kxufcfight_settled_join_lab_20260923'
EXPERIMENT_ID = 'C1-KXUFCFIGHT-SETTLED-RESOLUTION-JOIN-HARNESS'
FEATURE_FAMILY = 'C1-RJ'
PANEL_VERSION = '2026-09-22.c1-kxufcfight-v0'
SERIES = 'KXUFCFIGHT'
KNOB = 'join_gate'
J0 = 'J0'
J1 = 'J1'
ARMS = (J0, J1)
JOIN_GATE = {
    J0: 'nonempty_result_required',
    J1: 'occurrence_datetime_match',
}
FINALIZED_RESULTS = ('yes', 'no')
SCOUT_NONEMPTY_N_DECLARED = 4
PANEL_EVENTS_N = 2
PANEL_MARKETS_N = 4
PANEL_SHA256 = '24426d804c51bde23cf2557a11a8481a12026da10024094c4ae546d1f7d3956e'
PANEL_BYTES = 12396
PRE_ADMIT_STUB_SHA256 = '2cc661d86202d3daf9ffa45320e39d249852a97490f458f72ab7ea8ec5c81a00'
CITED_FREEZE_SHA256 = '3ea3362ad3c16951369d5f90497ec6079213dd54e5556340c4d3738744126cf1'
ADMITTED_AT = '2026-09-23T00:49:43Z'
EMPTY_OB_SHA256 = 'e07d09f130e604a9e1acfc736fb57cbdfc33d8a5a253466a0cbd5c98cf6c9f74'
FEEBOOK_COMMIT = '22371178cb2663250b4762f328069571c48cb551'
RAILS_COMMIT = '6a28e0d6254327ea4e6451c781bec56215ac6cac'
BASE_COMMIT = 'a281adc944e4dacffcdb5677a140fabaed675a81'
OUTPUT_KEYS = (
    'settled_join_n',
    'occurrence_match_n',
    'admit_ready_flag',
    'results',
    'pnl',
)
DOES_NOT_UNGATE = ('S1', 'S2', 'R2-P4')
PARENT_SEED_TICKERS = (
    'KXUFCFIGHT-26SEP22CONGUA-GUA',
    'KXUFCFIGHT-26SEP22CONGUA-CON',
    'KXUFCFIGHT-26SEP22DEGMOR-MOR',
    'KXUFCFIGHT-26SEP22DEGMOR-DEG',
)
PARENT_RESULTS = {
    'KXUFCFIGHT-26SEP22CONGUA-GUA': 'yes',
    'KXUFCFIGHT-26SEP22CONGUA-CON': 'no',
    'KXUFCFIGHT-26SEP22DEGMOR-MOR': 'no',
    'KXUFCFIGHT-26SEP22DEGMOR-DEG': 'yes',
}
PARENT_OCCURRENCE = {
    'KXUFCFIGHT-26SEP22CONGUA': '2026-09-23T04:20:00Z',
    'KXUFCFIGHT-26SEP22DEGMOR': '2026-09-23T04:40:00Z',
}
LIST_BOOK_ROUTES = (
    'GET /markets?series_ticker=KXUFCFIGHT&status=settled',
    'GET /markets?series_ticker=KXUFCFIGHT&status=finalized',
    'GET /events?series_ticker=KXUFCFIGHT&status=settled',
)
ORDERBOOK_NAMES = (
    'KXUFCFIGHT-26SEP22CONGUA-GUA.json',
    'KXUFCFIGHT-26SEP22CONGUA-CON.json',
    'KXUFCFIGHT-26SEP22DEGMOR-MOR.json',
    'KXUFCFIGHT-26SEP22DEGMOR-DEG.json',
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
    'empty_ob_reopen': 'EMPTY-OB stays closed',
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
    'empty_book_invent': 'empty books are not filled',
    'list_429_backfill': 'list books are not invented',
    'copy_scout_n': 'scout N is not settled_join_n',
    'materialize_freeze': 'cited freeze bytes are not regenerated',
    'claim_all_match': 'digest ALL_MATCH is not claimed',
}
CAPTURE_PANEL = REPO / 'lab/astra-capture/c1-kxufcfight/panel_admitted.json'
CAPTURE_STUB = REPO / 'lab/astra-capture/c1-kxufcfight/panel_stub.json'
ORDERBOOK_DIR = REPO / 'lab/astra-capture/c1-kxufcfight/orderbooks'
GOV_PANEL = REPO / 'lab/governance/astra/packets/C1_KXUFCFIGHT_PANEL_STUB_2026-09-22.json'
LAB_PANEL = ROOT / 'C1_KXUFCFIGHT_PANEL_STUB_2026-09-22.json'
FREEZE_PATH = REPO / 'lab/governance/astra/packets/C1_KXUFCFIGHT_SETTLED_RESOLUTION_JOIN_HARNESS_FREEZE_2026-09-23.md'
ACCEPT_PATH = REPO / 'lab/governance/astra/packets/CONDUCTOR_ACCEPT_C1_KXUFCFIGHT_SETTLED_JOIN_HARNESS_2026-09-24.json'
SCOUT_DIR = REPO / 'lab/governance/astra/packets/scout_c1_settled_rejoin_2026-09-23'
PIN_GAP_PATH = ROOT / 'PIN_GAP.json'
EMPTY_RESULTS = ROOT / 'results/EMPTY_RESULTS.json'
FROZEN_EXPERIMENT = ROOT / 'FROZEN_EXPERIMENT.json'
SOURCE_PINS = ROOT / 'SOURCE_PINS.json'


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


class EmptyBookInventRefused(InventedDepthRefused):
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
    """Collector already stamped the parent panel. This lab does not admit."""
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
    """Empty captured books and panel quotes are not a depth ladder."""
    del market
    raise InventedDepthRefused()


def invent_fill(market=None, value=None):
    """No fill is invented from a quote or an empty book."""
    del market, value
    raise InventedFillRefused()


def invent_result(ticker=None, result=None):
    """A settled result is not written. The panel field is read-only."""
    del ticker, result
    raise InventedResultRefused()


def backfill_list_429(which=None, result=None, occurrence_datetime=None):
    """Settled, finalized, and events list books stay absent."""
    del which, result, occurrence_datetime
    raise InventedResultRefused()


def fill_empty_book(ticker=None, bids=None):
    """The four empty orderbooks stay empty."""
    del ticker, bids
    raise EmptyBookInventRefused()


def assign_occurrence(ticker=None, value=None):
    """occurrence_datetime is not invented when it is missing."""
    del ticker, value
    raise InventedSoTRefused()


def copy_scout_n_into_settled_join(value=None):
    """The declared scout N=4 is not the scorecard count."""
    del value
    raise ScorecardPromotionRefused()


def materialize_cited_freeze(text=None):
    """The cited freeze bytes are not regenerated under that path."""
    del text
    raise PinAbsent()


def claim_digest_all_match():
    """ALL_MATCH stays unclaimed while the cited pins are absent."""
    status = digest_status()
    if status['digest_all_match_claimed'] is not False:
        raise PinMismatch()
    raise PinAbsent()


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
    if label == 'invent_fills':
        raise InventedFillRefused()
    if label == 'invent_depth':
        raise InventedDepthRefused()
    if label == 'invent_occurrence':
        raise InventedSoTRefused()
    if label == 'empty_book_invent':
        raise EmptyBookInventRefused()
    if label == 'admit_py':
        raise AdmitPyRefused()
    if label == 'live_orders':
        raise LiveOrdersForbidden()
    if label == 'ungate':
        raise UngateRefused()
    if label == 'copy_scout_n':
        raise ScorecardPromotionRefused()
    if label in ('materialize_freeze', 'claim_all_match'):
        raise PinAbsent()
    raise AdversaryRefused(ADVERSARY_LABELS[label])


def _assert_digest(path, digest, size=None):
    raw = Path(path).read_bytes()
    if hashlib.sha256(raw).hexdigest() != digest:
        raise PinMismatch(Path(path).name)
    if size is not None and len(raw) != size:
        raise PinMismatch(Path(path).name)
    return raw


def assert_panel_copies():
    """The governance and lab copies are the admitted panel bytes."""
    capture = _assert_digest(CAPTURE_PANEL, PANEL_SHA256, PANEL_BYTES)
    for path in (GOV_PANEL, LAB_PANEL, ROOT / 'panel_admitted.json'):
        if Path(path).read_bytes() != capture:
            raise PinMismatch(Path(path).name)
    _assert_digest(CAPTURE_STUB, PRE_ADMIT_STUB_SHA256)
    return capture


def load_panel(path=None):
    """Load the admitted parent. Does not rewrite admitted_at."""
    assert_panel_copies()
    path = CAPTURE_PANEL if path is None else Path(path)
    if path.resolve() == CAPTURE_STUB.resolve():
        raise PinMismatch('pre-admit stub')
    payload = json.loads(path.read_bytes())
    return _validate_panel(payload)


def _validate_panel(payload):
    if payload.get('panel_version') != PANEL_VERSION:
        raise OrchestratorError('panel_version')
    if payload.get('series_ticker') != SERIES:
        raise OrchestratorError('series')
    if payload.get('admitted_at') != ADMITTED_AT:
        raise AdmitPyRefused()
    if payload.get('kickoff_sot') != 'kalshi_occurrence_datetime':
        raise OccurrenceIntegrityRefused()
    events = payload.get('events') or []
    markets = payload.get('markets') or []
    if len(events) != PANEL_EVENTS_N or len(markets) != PANEL_MARKETS_N:
        raise OrchestratorError('cohort')
    event_clocks = {}
    for event in events:
        ticker = event.get('event_ticker')
        clock = event.get('occurrence_datetime')
        if ticker not in PARENT_OCCURRENCE or clock != PARENT_OCCURRENCE[ticker]:
            raise OccurrenceIntegrityRefused()
        if event.get('admitted_at') is not None:
            raise AdmitPyRefused()
        event_clocks[ticker] = clock
    seen = []
    for market in markets:
        ticker = market.get('market_ticker')
        seen.append(ticker)
        if market.get('result_observed_live_get') != PARENT_RESULTS.get(ticker):
            raise InventedResultRefused()
        if market.get('admitted_at') is not None:
            raise AdmitPyRefused()
        if 'result' in market:
            raise InventedResultRefused()
        occurrence = market.get('occurrence_datetime')
        if occurrence is None:
            raise InventedSoTRefused()
        if occurrence != event_clocks.get(market.get('event_ticker')):
            raise OccurrenceIntegrityRefused()
        if market.get('occurrence_source') != 'live_get_market':
            raise OccurrenceIntegrityRefused()
    if tuple(seen) != PARENT_SEED_TICKERS:
        raise OrchestratorError('seed order')
    if payload.get('results') is not None or payload.get('pnl') is not None:
        raise ScorecardPromotionRefused()
    return payload


def digest_status():
    """Report cited pins. A present freeze must match the cited sha256."""
    freeze_present = FREEZE_PATH.is_file()
    freeze_sha = sha256_file(FREEZE_PATH) if freeze_present else None
    if freeze_present and freeze_sha != CITED_FREEZE_SHA256:
        raise PinMismatch('freeze')
    accept_present = ACCEPT_PATH.is_file()
    accept_match = False
    if accept_present:
        accept = json.loads(ACCEPT_PATH.read_bytes())
        if accept.get('implement') is not True:
            raise PinMismatch('accept')
        verify = accept.get('digest_verify') or {}
        accept_match = verify.get('match') is True
        if verify.get('freeze') not in (None, CITED_FREEZE_SHA256):
            raise PinMismatch('accept freeze')
    scout_present = SCOUT_DIR.is_dir() and any(SCOUT_DIR.iterdir())
    maximize_present = any(REPO.rglob('MAXIMIZE_PIN_2026-09-23_1750ET.md'))
    claimed = bool(
        freeze_present
        and freeze_sha == CITED_FREEZE_SHA256
        and accept_present
        and accept_match
        and scout_present
        and maximize_present
    )
    return {
        'freeze_bytes_in_checkout': freeze_present,
        'freeze_sha256': freeze_sha,
        'freeze_matches_cited': freeze_sha == CITED_FREEZE_SHA256,
        'accept_bytes_in_checkout': accept_present,
        'scout_bytes_in_checkout': scout_present,
        'maximize_pin_bytes_in_checkout': maximize_present,
        'digest_all_match_claimed': claimed,
        'cited_freeze_sha256': CITED_FREEZE_SHA256,
    }


def assert_orderbooks_empty():
    """The four captured books stay the pinned empty body."""
    if len(list(ORDERBOOK_DIR.glob('*.json'))) != 4:
        raise EmptyBookInventRefused()
    books = []
    for name in ORDERBOOK_NAMES:
        path = ORDERBOOK_DIR / name
        raw = _assert_digest(path, EMPTY_OB_SHA256)
        payload = json.loads(raw)
        book = payload.get('orderbook_fp') or {}
        if book.get('yes_dollars') or book.get('no_dollars'):
            raise EmptyBookInventRefused()
        books.append(name)
    return tuple(books)


def list_books():
    """No settled, finalized, or events list book is stored or backfilled."""
    return {
        'routes': list(LIST_BOOK_ROUTES),
        'books_present': False,
        'list_429_backfilled': False,
        'markets_invented': False,
    }


def structural_rows(panel=None):
    """Label the four admitted parent seeds. Does not write scorecard counts."""
    if panel is None:
        panel = load_panel()
    else:
        _validate_panel(panel)
    rows = []
    clocks = {
        event['event_ticker']: event['occurrence_datetime']
        for event in panel['events']
    }
    for market in panel['markets']:
        ticker = market['market_ticker']
        observed = market.get('result_observed_live_get')
        occurrence = market.get('occurrence_datetime')
        event_clock = clocks[market['event_ticker']]
        if observed not in FINALIZED_RESULTS:
            j0 = 'honest_empty_result'
        else:
            j0 = 'nonempty_result_required_pass'
        if occurrence is None or event_clock is None:
            raise InventedSoTRefused()
        if occurrence != event_clock:
            raise OccurrenceIntegrityRefused()
        rows.append({
            'key': ticker,
            'panel_ticker': ticker,
            'j0': j0,
            'j1': 'occurrence_datetime_match',
            'result_observed_live_get': observed,
            'clock': 'occurrence_datetime',
            'occurrence_datetime': occurrence,
            'on_settled_list': False,
            'list_book': False,
            'parent_seed': True,
            'source': 'admitted_panel_parent_seeds',
        })
    if len(rows) != PANEL_MARKETS_N:
        raise OrchestratorError('rows')
    passes = [row for row in rows if row['j0'] == 'nonempty_result_required_pass']
    if len(passes) != PANEL_MARKETS_N:
        raise OrchestratorError('j0')
    return rows


def published_scorecard():
    """Every instrument field is present and null."""
    scorecard = {key: None for key in OUTPUT_KEYS}
    scorecard['status'] = 'EMPTY_RESULTS_PRE_EXAMINER'
    scorecard['lee_ready'] = 'REFUSED'
    scorecard['examiner_status'] = 'HOLD_PRE_PR'
    scorecard['stub_ready'] = False
    scorecard['list_429_backfilled'] = False
    scorecard['scout_n_copied_into_settled_join_n'] = False
    scorecard['digest_all_match_claimed'] = False
    return scorecard


def assert_null_scorecard(payload):
    """Require every instrument field and require null."""
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


def instrument_binding(panel=None):
    """One join-gate knob. Fee and rails commits stay unloaded."""
    if panel is None:
        panel = load_panel()
    pins = digest_status()
    if pins['digest_all_match_claimed'] is not False:
        raise PinMismatch()
    rows = structural_rows(panel)
    books = assert_orderbooks_empty()
    gaps = list_books()
    return {
        'experiment_id': EXPERIMENT_ID,
        'lab_directory': LAB_DIRECTORY,
        'feature_family': FEATURE_FAMILY,
        'knob': KNOB,
        'arms': tuple({'id': arm, 'join_gate': JOIN_GATE[arm]} for arm in ARMS),
        'panel_version': panel['panel_version'],
        'admitted_at': panel.get('admitted_at'),
        'events_n': PANEL_EVENTS_N,
        'markets_n': PANEL_MARKETS_N,
        'parent_seed_tickers': list(PARENT_SEED_TICKERS),
        'row_label_count': len(rows),
        'source': 'admitted_panel_parent_seeds',
        'scout_reget_loaded': False,
        'settled_nonempty_result_N_scout_declared': SCOUT_NONEMPTY_N_DECLARED,
        'scout_n_copied_into_settled_join_n': False,
        'j1_clock': 'occurrence_datetime',
        'occurrence_datetime_invented': False,
        'expected_expiration_substituted': False,
        'list_books': gaps,
        'empty_orderbooks': list(books),
        'empty_books_invented': False,
        'fee_import_used': False,
        'rails_import_used': False,
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
        'digest_all_match_claimed': False,
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
        'source': 'admitted_panel_parent_seeds',
        'published': published,
        'promoted': False,
        'live_orders': False,
        'lee_ready': 'REFUSED',
        'admit_py_run': False,
        'list_429_backfilled': False,
        'scout_n_copied_into_settled_join_n': False,
        'scout_reget_loaded': False,
        'digest_all_match_claimed': False,
        'occurrence_datetime_invented': False,
        'empty_books_invented': False,
        'arm_b_touch': False,
        's1_s2_r2p4_ungated': False,
        'examiner_status': 'HOLD_PRE_PR',
        'stub_ready': False,
    }
    report.update(extra)
    for key in OUTPUT_KEYS:
        report[key] = None
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
        'admitted_at': panel.get('admitted_at'),
        'event_count': len(panel.get('events') or []),
        'market_count': PANEL_MARKETS_N,
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
    return {
        'frozen.results': None,
        'frozen.pnl': None,
        'empty.settled_join_n': None,
        'empty.occurrence_match_n': None,
        'empty.admit_ready_flag': None,
    }
