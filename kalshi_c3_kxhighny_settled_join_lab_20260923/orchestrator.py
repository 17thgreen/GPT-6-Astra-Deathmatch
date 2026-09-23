"""C3 KXHIGHNY settled-resolution join harness.

Measurement only. One knob: join_gate. This module does not edit the
bordering lab, feebook, rails, Cap-SR, or any FQ sibling. It does not
place orders, does not read Logan keys, does not run admit.py, and does
not write scorecard metrics.

The checkout freeze, scout reget, seed summary, panel stub, settled
reget, and accept match the attached sha256 values. The panel stub keeps
admitted_at null. CHI B66.5 stays the honest 429 gap. Lee-Ready is
refused. Settled results, depth, fills, and PnL are not invented.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PARENT = ROOT.parent

LAB_DIRECTORY = 'kalshi_c3_kxhighny_settled_join_lab_20260923'
EXPERIMENT_ID = 'C3-KXHIGHNY-SETTLED-RESOLUTION-JOIN-HARNESS'
FEATURE_FAMILY = 'C3-RJ'
PARENT_PACKET_ID = 'C3-KXHIGHNY-MEAS'
PANEL_VERSION = '2026-09-22.c3-kxhighny-v0'
SCHEMA_ID = 'astra.registry.c3_kxhighny_panel.v0'
SERIES = 'KXHIGHNY'
STUB_STATUS = 'PANEL_SCHEMA_STUB_SEED'
KNOB = 'join_gate'
J0 = 'J0'
J1 = 'J1'
ARMS = (J0, J1)
JOIN_GATE = {
    J0: 'nonempty_result_required',
    J1: 'occurrence_datetime_match',
}
FINALIZED_RESULTS = ('yes', 'no')
SCOUT_NONEMPTY_N = 4
SEED_ATTEMPTED = 6
PANEL_EVENTS_N = 3
PANEL_MARKETS_N = 6
AGREEMENT_ROWS_N = 5
GAP_FILE = 'market_KXHIGHCHI_26SEP22_B66_5.json'
GAP_TICKER = 'KXHIGHCHI-26SEP22-B66.5'
GAP_NOTE = 'no market object (likely 429)'
GAP_ERROR_CODE = 'too_many_requests'
ACTIVE_TICKER = 'KXHIGHNY-26SEP23-B67.5'
FEEBOOK_COMMIT = '22371178cb2663250b4762f328069571c48cb551'
RAILS_COMMIT = '6a28e0d6254327ea4e6451c781bec56215ac6cac'
BASE_COMMIT = '82bf7bb99bcc618b912255cc24022b23f9f15047'
FREEZE_SHA256 = '56adcf592239b028aaa8bcffbf09815115b8454f78db39b43c578e64c160a4d5'
SCOUT_SHA256 = 'e8950352745007d3cb565050161430807fa5de70d15321bb00bede6ca9ac18ee'
SEED_SHA256 = 'b32bbf3200649bcea4fb61a98a4869d5123060a57702a9327262cccbc8e1ca93'
PANEL_STUB_SHA256 = '2a5da7fe85ca1adc6b7c4dcf9e09ed5c6bb62be6b5c9b42731e36e31d1e8dfea'
REGET_SHA256 = '0055faae508ba034eb49a12d52713566cbfe20bfbfbd2a16203ef350152ac24a'
ACCEPT_SHA256 = '9adb77ed01fd9ccb894564efa9d5534d2edf189365ca0852fff49dafd3598d69'
FROZEN_SHA256 = '10f75f008f6fb870e212b81f9913b09ab06337973e850d36796f336331d33c23'
EMPTY_SHA256 = '48e5916fff57563d14a6a84b8c6c0ed2515c3172066d565e5a18933faf02f4e6'
SOURCE_PINS_SHA256 = 'a11360f5e62a2142b2064b58279cc507a4068ac9c73f4e4b64af1b781be3c4ff'
FREEZE_BYTES = 5119
SCOUT_BYTES = 2077
SEED_BYTES = 1855
PANEL_BYTES = 13035
REGET_BYTES = 17320
ACCEPT_BYTES = 1098
FROZEN_BYTES = 1039
EMPTY_BYTES = 166
SOURCE_PINS_BYTES = 3829
ACCEPT_STAMPED_AT = '2026-09-23T15:03:00-04:00'
FROZEN_STAMPED_AT = '2026-09-23T15:02:00-04:00'
EMPTY_NOTE = 'pre-ACCEPT empty; C3-RJ measurement join only'
PUBLIC_HOST = 'https://api.elections.kalshi.com/trade-api/v2'
OUT_OF_SCOPE_ROUTE = 'POST /portfolio/orders'
SCORECARD_FIELDS = (
    'settled_join_n',
    'occurrence_match_n',
    'admit_ready_flag',
)
OUTPUT_KEYS = SCORECARD_FIELDS + ('results', 'pnl')
ACCEPT_HARD_REFUSE = (
    'invent_settled_result',
    'invent_fills',
    'Lee-Ready',
    'FQ_reopen',
    'Cap-SR_reopen',
    'ungate_S1_S2_R2P4',
    'Arm_B_touch',
    'admit_py_by_Variants',
    'live_orders',
)
DOES_NOT_UNGATE = ('S1', 'S2', 'R2-P4')
ADVERSARY_LABELS = {
    'lee_ready': 'Lee-Ready is refused',
    'invent_settled_result': 'invented settled result is refused',
    'invented_result': 'invented settled result is refused',
    'invent_fills': 'invented fills are refused',
    'invented_fills': 'invented fills are refused',
    'invented_depth': 'invented depth is refused',
    'invented_pnl': 'invented pnl is refused',
    'chi_429_backfill': 'CHI 429 backfill is refused',
    'fq_reopen': 'FQ reopen is refused',
    'eth_fq_reopen': 'ETH-FQ reopen is refused',
    'nhl_fq_reopen': 'NHL-FQ reopen is refused',
    'cpi_fq_reopen': 'CPI-FQ reopen is refused',
    'atp_fq_reopen': 'ATP-FQ reopen is refused',
    'cap_sr_reopen': 'Cap-SR reopen is refused',
    'empty_ob_reopen': 'EMPTY-OB reopen is refused',
    'c3_bordering_reopen': 'C3 bordering reopen is refused',
    'arm_b': 'Arm B is refused',
    'q7_arm_b': 'Arm B is refused',
    'admit_py': 'admit.py is refused',
    'live_orders': 'live orders are refused',
    'logan_keys': 'Logan keys are refused',
    'ungate': 'S1 S2 R2-P4 stay gated',
}
DOES_NOT_MODIFY = (
    'kalshi_feebook_lab_20260922',
    'kalshi_rails_lab_20260922',
    'kalshi_r2p1_hygiene_000_lab_20260922',
    'kalshi_queue_fragility_000_lab_20260922',
    'kalshi_soft_blended_reserves_000_lab_20260923',
    'kalshi_cap_sr_effects_000_lab_20260923',
    'kalshi_capital_structure_lab_20260922',
    'kalshi_examiner_fee_queue_honesty_000_lab_20260922',
    'kalshi_c1_kxufcfight_honesty_lab_20260922',
    'kalshi_c1_empty_ob_lab_20260923',
    'kalshi_c2_kxnhlgame_feequue_lab_20260923',
    'kalshi_c3_kxhighny_bordering_lab_20260923',
    'kalshi_c4_kxcpi_feequue_lab_20260923',
    'kalshi_c5_kxbtc15m_honesty_lab_20260923',
    'kalshi_atp_kxatpmatch_feequue_lab_20260923',
    'kalshi_eth_kxeth15m_feequue_lab_20260923',
    'kalshi_r3p3_fl_maker_taker_lab_20260923',
    'kalshi_r3p4_l2_cat_lab_20260923',
    'kalshi_r3p4_l2_sf_lab_20260923',
    'kalshi_r3_p4_l2_shape_lab_20260922',
    'kalshi_s4_ncaaf_feequue_lab_20260923',
    'kalshi_s5_mve_filllegs_lab_20260923',
    'kalshi_r2p3_prop_ladder_lab_20260923',
    'kalshi_r2p5_sot_id_lab_20260923',
    'nfl_factorial_lab_20260921',
    'nfl_paircheck_lab_20260922',
    'lab/astra-capture/c3-kxhighny/panel_stub.json',
)
FREEZE_NAME = 'C3_KXHIGHNY_SETTLED_RESOLUTION_JOIN_HARNESS_FREEZE_2026-09-23.md'
SCOUT_NAME = 'scout_settled_rejoin_C3_KXHIGHNY.json'
SEED_NAME = 'SEED_SETTLED_SUMMARY.json'
PANEL_ALIAS = 'C3_KXHIGHNY_PANEL_STUB_2026-09-22.json'
REGET_NAME = 'settled_reget_2026-09-23.json'
ACCEPT_NAME = 'CONDUCTOR_ACCEPT_C3_KXHIGHNY_SETTLED_JOIN_HARNESS_2026-09-23.json'
SOURCE_PINS_NAME = 'SOURCE_PINS.json'
LAB_BUNDLE = ROOT / 'C3_KXHIGHNY_SETTLED_RESOLUTION_JOIN_HARNESS'
GOVERNANCE_TREE = PARENT / 'lab' / 'governance' / 'astra'
PACKET = ROOT / FREEZE_NAME
SCOUT_PATH = ROOT / SCOUT_NAME
SEED_PATH = ROOT / SEED_NAME
REGET_PATH = ROOT / REGET_NAME
CONDUCTOR_ACCEPT = ROOT / ACCEPT_NAME
FROZEN_EXPERIMENT = ROOT / 'FROZEN_EXPERIMENT.json'
EMPTY_RESULTS = ROOT / 'results' / 'EMPTY_RESULTS.json'
SOURCE_PINS = ROOT / SOURCE_PINS_NAME
PANEL_CAPTURE = PARENT / 'lab' / 'astra-capture' / 'c3-kxhighny' / 'panel_stub.json'
PANEL_ADMITTED = PARENT / 'lab' / 'astra-capture' / 'c3-kxhighny' / 'panel_admitted.json'
REGET_CITE = PARENT / 'lab' / 'astra-capture' / 'c3-kxhighny' / REGET_NAME
ADMIT_PY = ROOT / 'admit.py'
COMPARE_FIELDS = ('status', 'result', 'occurrence_datetime', 'close_time')


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


class InventedResultRefused(OrchestratorError):
    """A settled result was invented or the CHI gap was backfilled."""

    def __init__(self):
        super().__init__('invented settled result')


class InventedFillRefused(OrchestratorError):
    """A fill was invented from volume or from the gap."""

    def __init__(self):
        super().__init__('invented fill')


class InventedDepthRefused(OrchestratorError):
    """Quote size is not a depth ladder."""

    def __init__(self):
        super().__init__('invented depth')


class InventedSoTRefused(OrchestratorError):
    """occurrence_datetime is not invented for the 429 gap."""

    def __init__(self):
        super().__init__('invented occurrence_datetime')


class OccurrenceIntegrityRefused(OrchestratorError):
    """Reget, seed, and panel occurrence_datetime disagree."""

    def __init__(self):
        super().__init__('occurrence_datetime')


class AdmitPyRefused(OrchestratorError):
    """Variants does not run admit.py and does not write admitted_at."""

    def __init__(self):
        super().__init__('admit.py refused')


class ExaminerNotReady(OrchestratorError):
    """Examiner stays NOT_SCORED until after merge and Clock admit."""

    def __init__(self):
        super().__init__('Examiner NOT_SCORED')


class UngateRefused(OrchestratorError):
    """S1, S2, and R2-P4 stay gated."""

    def __init__(self):
        super().__init__('does not ungate S1 S2 R2-P4')


class PanelVersionRefused(OrchestratorError):
    """The panel file is not the pinned C3 seed."""

    def __init__(self):
        super().__init__('panel_version')


class UnknownGate(OrchestratorError):
    """The only knob is the two named join gates."""

    def __init__(self):
        super().__init__('join_gate')


class InventedMarketRefused(OrchestratorError):
    """A ticker is outside the authentic reget and panel stub."""

    def __init__(self):
        super().__init__('invented market')


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
    """Variants does not admit the panel."""
    del path
    raise AdmitPyRefused()


def ungate(name):
    """S1, S2, and R2-P4 stay queued."""
    if name in DOES_NOT_UNGATE:
        raise UngateRefused()
    raise OrchestratorError('ungate')


def claim_admit_ready():
    """admit_ready_flag stays null. Clock admit is not this harness."""
    raise ExaminerNotReady()


def claim_examiner_ready():
    """Examiner HOLD / NOT_SCORED until after merge and sha verify."""
    raise ExaminerNotReady()


def quote_depth(market):
    """Public size fields are not a depth ladder."""
    if market is None or isinstance(market, (dict, str, list, tuple)):
        raise InventedDepthRefused()
    raise InventedDepthRefused()


def invent_fill(market=None, value=None):
    """Volume on a market quote is not a fill."""
    del market, value
    raise InventedFillRefused()


def invent_result(ticker=None, result=None):
    """Official result is read from the reget only. Nothing is written."""
    del ticker, result
    raise InventedResultRefused()


def backfill_chi_gap(result=None, occurrence_datetime=None):
    """The 429 body stays a gap. No result and no occurrence are written."""
    del result, occurrence_datetime
    raise InventedResultRefused()


def assign_occurrence(ticker=None, value=None):
    """A missing occurrence on the 429 gap stays missing."""
    del ticker, value
    raise InventedSoTRefused()


def infer_lee_ready(row):
    """Lee-Ready has no success path. Every input is refused."""
    if row is None or isinstance(row, (dict, str, int, float, list, tuple)):
        raise LeeReadyRefused()
    raise LeeReadyRefused()


def refuse_adversary(label):
    """Named refuse labels. Nothing is traded."""
    if label not in ADVERSARY_LABELS:
        raise OrchestratorError('adversary label')
    if label == 'lee_ready':
        raise LeeReadyRefused()
    if label in ('invent_settled_result', 'invented_result', 'chi_429_backfill'):
        raise InventedResultRefused()
    if label in ('invent_fills', 'invented_fills'):
        raise InventedFillRefused()
    if label == 'invented_depth':
        raise InventedDepthRefused()
    if label == 'admit_py':
        raise AdmitPyRefused()
    if label == 'live_orders':
        raise LiveOrdersForbidden()
    if label == 'ungate':
        raise UngateRefused()
    raise AdversaryRefused(ADVERSARY_LABELS[label])


def owned_dirs():
    return (ROOT, LAB_BUNDLE)


def _assert_digest(path, digest, size=None):
    raw = Path(path).read_bytes()
    if hashlib.sha256(raw).hexdigest() != digest:
        raise OrchestratorError(Path(path).name)
    if size is not None and len(raw) != size:
        raise OrchestratorError(Path(path).name)
    return raw


def _assert_owned(name, digest, size=None):
    for directory in owned_dirs():
        _assert_digest(directory / name, digest, size)


def _read_pinned(path, digest, size):
    return json.loads(_assert_digest(path, digest, size))


def _assert_source_pins(payload):
    if payload.get('packet_id') != EXPERIMENT_ID:
        raise OrchestratorError('source pins')
    if payload.get('feature_family') != FEATURE_FAMILY:
        raise OrchestratorError('source pins')
    if payload.get('freeze_sha256') != FREEZE_SHA256:
        raise OrchestratorError('source pins')
    if payload.get('scout_reget_sha256') != SCOUT_SHA256:
        raise OrchestratorError('source pins')
    if payload.get('seed_summary_sha256') != SEED_SHA256:
        raise OrchestratorError('source pins')
    if payload.get('panel_stub_sha256') != PANEL_STUB_SHA256:
        raise OrchestratorError('source pins')
    if payload.get('settled_reget_sha256') != REGET_SHA256:
        raise OrchestratorError('source pins')
    if payload.get('conductor_accept_sha256') != ACCEPT_SHA256:
        raise OrchestratorError('source pins')
    if payload.get('frozen_experiment_sha256') != FROZEN_SHA256:
        raise OrchestratorError('source pins')
    if payload.get('empty_results_sha256') != EMPTY_SHA256:
        raise OrchestratorError('source pins')
    if payload.get('knob') != KNOB or payload.get('arms') != JOIN_GATE:
        raise OrchestratorError('source pins')
    if payload.get('admitted_at') is not None:
        raise OrchestratorError('source pins')
    if payload.get('settled_nonempty_result_N_scout') != SCOUT_NONEMPTY_N:
        raise OrchestratorError('source pins')
    if payload.get('chi_b66_5_file') != GAP_FILE:
        raise OrchestratorError('source pins')
    if payload.get('chi_b66_5_panel_ticker') != GAP_TICKER:
        raise OrchestratorError('source pins')
    if payload.get('chi_b66_5_honest_429_gap') is not True:
        raise OrchestratorError('source pins')
    if payload.get('chi_b66_5_result_invented') is not False:
        raise InventedResultRefused()
    if payload.get('fee_import_used') is not False or payload.get('rails_import_used') is not False:
        raise OrchestratorError('source pins')
    if payload.get('fee_arms') is not False:
        raise OrchestratorError('source pins')
    if payload.get('feebook_commit_fixed_not_loaded') != FEEBOOK_COMMIT:
        raise OrchestratorError('source pins')
    if payload.get('rails_commit_fixed_not_loaded') != RAILS_COMMIT:
        raise OrchestratorError('source pins')
    if payload.get('governance_tree') != 'absent':
        raise OrchestratorError('source pins')
    if payload.get('does_not_run_admit_py') is not True:
        raise AdmitPyRefused()
    if payload.get('base_commit') != BASE_COMMIT:
        raise OrchestratorError('source pins')
    if payload.get('lee_ready') != 'REFUSED':
        raise LeeReadyRefused()
    if payload.get('c3_bordering_reopen') is not False:
        raise OrchestratorError('source pins')
    if payload.get('cap_sr_reopen') is not False or payload.get('fq_reopen') is not False:
        raise OrchestratorError('source pins')
    if payload.get('eth_fq_reopen') is not False or payload.get('empty_ob_reopen') is not False:
        raise OrchestratorError('source pins')
    if payload.get('arm_b_touch') is not False or payload.get('live_orders') is not False:
        raise OrchestratorError('source pins')
    if payload.get('does_not_ungate') != list(DOES_NOT_UNGATE):
        raise UngateRefused()
    if payload.get('panel_version') != PANEL_VERSION:
        raise PanelVersionRefused()
    if payload.get('panel_events_n') != PANEL_EVENTS_N or payload.get('panel_markets_n') != PANEL_MARKETS_N:
        raise OrchestratorError('source pins')
    for key in OUTPUT_KEYS:
        if key not in payload or payload[key] is not None:
            raise ScorecardPromotionRefused()
    return payload


def _validate_scout(payload):
    if payload.get('feature_family') != FEATURE_FAMILY:
        raise OrchestratorError('scout')
    if payload.get('settled_nonempty_result_N') != SCOUT_NONEMPTY_N:
        raise OrchestratorError('scout N')
    if payload.get('results') is not None or payload.get('pnl') is not None:
        raise ScorecardPromotionRefused()
    if payload.get('mode') != 'GET_only_public':
        raise OrchestratorError('scout mode')
    markets = payload.get('markets')
    if not isinstance(markets, list) or len(markets) != SEED_ATTEMPTED:
        raise OrchestratorError('scout markets')
    nonempty = []
    gaps = []
    for row in markets:
        if not isinstance(row, dict):
            raise OrchestratorError('scout market')
        if row.get('nonempty_result') is True:
            if row.get('status') != 'finalized' or row.get('result') not in FINALIZED_RESULTS:
                raise InventedResultRefused()
            if not isinstance(row.get('ticker'), str):
                raise InventedMarketRefused()
            nonempty.append(row)
        elif row.get('file') == GAP_FILE:
            gaps.append(row)
        elif row.get('ticker') == ACTIVE_TICKER:
            if row.get('status') != 'active' or row.get('result') != '' or row.get('nonempty_result') is not False:
                raise InventedResultRefused()
        else:
            raise OrchestratorError('scout row')
    if len(nonempty) != SCOUT_NONEMPTY_N or len(gaps) != 1:
        raise OrchestratorError('scout census')
    gap = gaps[0]
    if gap.get('nonempty_result') is not False or gap.get('note') != GAP_NOTE:
        raise InventedResultRefused()
    if 'ticker' in gap or 'result' in gap or 'occurrence_datetime' in gap:
        raise InventedResultRefused()
    return payload


def _validate_seed(payload, scout):
    if payload.get('settled_nonempty_result_N') != SCOUT_NONEMPTY_N:
        raise OrchestratorError('seed N')
    if payload.get('seed_tickers_attempted') != SEED_ATTEMPTED:
        raise OrchestratorError('seed attempted')
    if payload.get('candidate_won') != FEATURE_FAMILY:
        raise OrchestratorError('seed candidate')
    if payload.get('markets') != scout.get('markets'):
        raise OrchestratorError('seed scout markets')
    return payload


def _validate_reget(payload, scout):
    if payload.get('mode') != 'GET_only':
        raise OrchestratorError('reget mode')
    if payload.get('host') != PUBLIC_HOST:
        raise OrchestratorError('reget host')
    markets = payload.get('markets')
    if not isinstance(markets, dict) or len(markets) != SEED_ATTEMPTED:
        raise OrchestratorError('reget markets')
    gap = markets.get(GAP_FILE)
    if not isinstance(gap, dict) or set(gap.keys()) != {'error_body'}:
        raise InventedResultRefused()
    error = (gap.get('error_body') or {}).get('error') or {}
    if error.get('code') != GAP_ERROR_CODE:
        raise OrchestratorError('reget gap')
    if 'result' in gap or 'ticker' in gap or 'occurrence_datetime' in gap:
        raise InventedResultRefused()
    scout_rows = {}
    for row in scout.get('markets') or []:
        if 'ticker' in row:
            scout_rows[row['ticker']] = row
    if set(scout_rows) != set(markets) - {GAP_FILE}:
        raise InventedMarketRefused()
    nonempty = []
    for ticker, market in markets.items():
        if ticker == GAP_FILE:
            continue
        if not isinstance(market, dict) or market.get('ticker') != ticker:
            raise InventedMarketRefused()
        if 'orderbook_fp' in market:
            raise InventedDepthRefused()
        scout_row = scout_rows[ticker]
        for field in COMPARE_FIELDS:
            if market.get(field) != scout_row.get(field):
                raise OrchestratorError('scout reget ' + field)
        official = market.get('status') == 'finalized' and market.get('result') in FINALIZED_RESULTS
        if official is not scout_row.get('nonempty_result'):
            raise InventedResultRefused()
        if official:
            nonempty.append(ticker)
        elif ticker != ACTIVE_TICKER or market.get('status') != 'active' or market.get('result') != '':
            raise InventedResultRefused()
    if len(nonempty) != SCOUT_NONEMPTY_N:
        raise OrchestratorError('reget nonempty')
    return payload


def _validate_panel(payload):
    if not isinstance(payload, dict):
        raise OrchestratorError('panel')
    if payload.get('panel_version') != PANEL_VERSION:
        raise PanelVersionRefused()
    if payload.get('packet_id') != PARENT_PACKET_ID:
        raise OrchestratorError('packet')
    if payload.get('schema_id') != SCHEMA_ID:
        raise OrchestratorError('schema')
    if payload.get('series_ticker') != SERIES:
        raise OrchestratorError('series')
    if payload.get('stub_status') != STUB_STATUS:
        raise OrchestratorError('stub_status')
    if payload.get('admitted_at') is not None:
        raise OrchestratorError('admitted_at')
    for key in ('results', 'pnl'):
        if key not in payload or payload[key] is not None:
            raise ScorecardPromotionRefused()
    counts = payload.get('cohort_counts') or {}
    if counts.get('events_n') != PANEL_EVENTS_N or counts.get('markets_n') != PANEL_MARKETS_N:
        raise OrchestratorError('cohort')
    events = payload.get('events')
    markets = payload.get('markets')
    if not isinstance(events, list) or len(events) != PANEL_EVENTS_N:
        raise OrchestratorError('events')
    if not isinstance(markets, list) or len(markets) != PANEL_MARKETS_N:
        raise OrchestratorError('markets')
    event_names = []
    for event in events:
        if not isinstance(event, dict):
            raise OrchestratorError('events')
        if event.get('admitted_at') is not None or event.get('panel_version') != PANEL_VERSION:
            raise OrchestratorError('admitted_at')
        name = event.get('event_ticker')
        if not isinstance(name, str):
            raise OrchestratorError('events')
        event_names.append(name)
    if len(set(event_names)) != PANEL_EVENTS_N:
        raise OrchestratorError('events')
    seen = []
    for market in markets:
        if not isinstance(market, dict):
            raise OrchestratorError('market')
        if market.get('admitted_at') is not None or market.get('panel_version') != PANEL_VERSION:
            raise OrchestratorError('admitted_at')
        if market.get('result') is not None:
            raise InventedResultRefused()
        ticker = market.get('market_ticker')
        if not isinstance(ticker, str) or ticker in seen:
            raise InventedMarketRefused()
        if market.get('event_ticker') not in event_names:
            raise InventedMarketRefused()
        seen.append(ticker)
    if GAP_TICKER not in seen or ACTIVE_TICKER not in seen:
        raise OrchestratorError('panel tickers')
    if len(seen) != PANEL_MARKETS_N:
        raise OrchestratorError('markets')
    return payload


def _assert_frozen(payload):
    if payload.get('packet_id') != EXPERIMENT_ID:
        raise OrchestratorError('frozen')
    if payload.get('feature_family') != FEATURE_FAMILY:
        raise OrchestratorError('frozen')
    if payload.get('status') != 'FROZEN_EXPERIMENT':
        raise OrchestratorError('frozen')
    if payload.get('knob') != KNOB:
        raise OrchestratorError('frozen')
    if payload.get('arms') != list(ARMS):
        raise OrchestratorError('frozen')
    if payload.get('arm_values') != JOIN_GATE:
        raise OrchestratorError('frozen')
    if payload.get('results') is not None or payload.get('pnl') is not None:
        raise ScorecardPromotionRefused()
    if payload.get('settled_nonempty_result_N_scout') != SCOUT_NONEMPTY_N:
        raise OrchestratorError('frozen')
    if payload.get('admitted_at') is not None:
        raise OrchestratorError('admitted_at')
    if payload.get('panel_version') != PANEL_VERSION:
        raise PanelVersionRefused()
    if payload.get('does_not_run_admit_py') is not True:
        raise AdmitPyRefused()
    if payload.get('stamped_at_et') != FROZEN_STAMPED_AT:
        raise OrchestratorError('frozen')
    if payload.get('freeze_sha256') != FREEZE_SHA256:
        raise OrchestratorError('frozen')
    if payload.get('scout_reget_sha256') != SCOUT_SHA256:
        raise OrchestratorError('frozen')
    if payload.get('scout_summary_sha256') != SEED_SHA256:
        raise OrchestratorError('frozen')
    if payload.get('panel_stub_sha256') != PANEL_STUB_SHA256:
        raise OrchestratorError('frozen')
    if payload.get('settled_reget_capture_sha256') != REGET_SHA256:
        raise OrchestratorError('frozen')
    return payload


def _assert_accept(payload):
    if payload.get('packet_id') != EXPERIMENT_ID:
        raise OrchestratorError('conductor accept')
    if payload.get('feature_family') != FEATURE_FAMILY:
        raise OrchestratorError('conductor accept')
    if payload.get('decision') != 'ACCEPT' or payload.get('implement') is not True:
        raise OrchestratorError('conductor accept')
    if payload.get('seat') != 'Conductor':
        raise OrchestratorError('conductor accept')
    if payload.get('accepted_at_et') != ACCEPT_STAMPED_AT:
        raise OrchestratorError('conductor accept')
    digest = payload.get('digest_verify')
    if not isinstance(digest, dict):
        raise OrchestratorError('conductor accept')
    if digest.get('freeze') != FREEZE_SHA256:
        raise OrchestratorError('conductor accept')
    if digest.get('scout_reget') != SCOUT_SHA256:
        raise OrchestratorError('conductor accept')
    if digest.get('seed_summary') != SEED_SHA256:
        raise OrchestratorError('conductor accept')
    if digest.get('panel_stub') != PANEL_STUB_SHA256:
        raise OrchestratorError('conductor accept')
    if digest.get('settled_reget') != REGET_SHA256:
        raise OrchestratorError('conductor accept')
    if digest.get('settled_nonempty_result_N') != SCOUT_NONEMPTY_N or digest.get('match') is not True:
        raise OrchestratorError('conductor accept')
    if payload.get('hard_refuse') != list(ACCEPT_HARD_REFUSE):
        raise OrchestratorError('conductor accept')
    return payload


def _assert_authentic_bytes():
    _assert_owned(FREEZE_NAME, FREEZE_SHA256, FREEZE_BYTES)
    _assert_owned(SCOUT_NAME, SCOUT_SHA256, SCOUT_BYTES)
    _assert_owned(SEED_NAME, SEED_SHA256, SEED_BYTES)
    _assert_owned(REGET_NAME, REGET_SHA256, REGET_BYTES)
    _assert_owned(ACCEPT_NAME, ACCEPT_SHA256, ACCEPT_BYTES)
    _assert_owned('FROZEN_EXPERIMENT.json', FROZEN_SHA256, FROZEN_BYTES)
    _assert_owned('panel_stub.json', PANEL_STUB_SHA256, PANEL_BYTES)
    _assert_owned(PANEL_ALIAS, PANEL_STUB_SHA256, PANEL_BYTES)
    _assert_owned(SOURCE_PINS_NAME, SOURCE_PINS_SHA256, SOURCE_PINS_BYTES)
    _assert_digest(PANEL_CAPTURE, PANEL_STUB_SHA256, PANEL_BYTES)
    _assert_digest(EMPTY_RESULTS, EMPTY_SHA256, EMPTY_BYTES)
    _assert_digest(LAB_BUNDLE / 'results.json', EMPTY_SHA256, EMPTY_BYTES)
    _assert_digest(LAB_BUNDLE / 'results' / 'EMPTY_RESULTS.json', EMPTY_SHA256, EMPTY_BYTES)
    if REGET_CITE.exists():
        _assert_digest(REGET_CITE, REGET_SHA256, REGET_BYTES)
    scout = _validate_scout(_read_pinned(SCOUT_PATH, SCOUT_SHA256, SCOUT_BYTES))
    _validate_seed(_read_pinned(SEED_PATH, SEED_SHA256, SEED_BYTES), scout)
    _validate_reget(_read_pinned(REGET_PATH, REGET_SHA256, REGET_BYTES), scout)
    _validate_panel(_read_pinned(PANEL_CAPTURE, PANEL_STUB_SHA256, PANEL_BYTES))
    _assert_frozen(_read_pinned(FROZEN_EXPERIMENT, FROZEN_SHA256, FROZEN_BYTES))
    _assert_accept(_read_pinned(CONDUCTOR_ACCEPT, ACCEPT_SHA256, ACCEPT_BYTES))
    for directory in owned_dirs():
        _assert_source_pins(json.loads(_assert_digest(directory / SOURCE_PINS_NAME, SOURCE_PINS_SHA256, SOURCE_PINS_BYTES)))
    empty = json.loads(EMPTY_RESULTS.read_text())
    if empty.get('note') != EMPTY_NOTE:
        raise OrchestratorError('empty results')
    assert_null_scorecard(empty)
    if ADMIT_PY.exists():
        raise AdmitPyRefused()
    if PANEL_ADMITTED.exists():
        raise AdmitPyRefused()
    if GOVERNANCE_TREE.is_dir():
        raise OrchestratorError('governance tree')
    return True


def conductor_pin_status():
    """Report whether checkout bytes match the attached conductor sha256 values."""
    freeze_match = sha256_file(PACKET) == FREEZE_SHA256
    scout_match = sha256_file(SCOUT_PATH) == SCOUT_SHA256
    seed_match = sha256_file(SEED_PATH) == SEED_SHA256
    panel_match = sha256_file(PANEL_CAPTURE) == PANEL_STUB_SHA256
    reget_match = sha256_file(REGET_PATH) == REGET_SHA256
    accept_match = sha256_file(CONDUCTOR_ACCEPT) == ACCEPT_SHA256
    return {
        'freeze_matches_conductor_claim': freeze_match,
        'scout_reget_matches_conductor_claim': scout_match,
        'seed_summary_matches_conductor_claim': seed_match,
        'panel_stub_matches_conductor_claim': panel_match,
        'settled_reget_matches_conductor_claim': reget_match,
        'accept_matches_conductor_claim': accept_match,
        'conductor_bytes_in_checkout': all((
            freeze_match,
            scout_match,
            seed_match,
            panel_match,
            reget_match,
            accept_match,
        )),
        'admitted_at': None,
        'governance_tree_present': GOVERNANCE_TREE.is_dir(),
        'reget_cite_present': REGET_CITE.is_file(),
    }


def select_panel_path(stub_path=None, admitted_path=None):
    """The committed stub only. A panel_admitted.json file is not consumed."""
    if admitted_path is not None and Path(admitted_path).exists():
        raise AdmitPyRefused()
    if PANEL_ADMITTED.exists():
        raise AdmitPyRefused()
    stub_path = PANEL_CAPTURE if stub_path is None else Path(stub_path)
    if not Path(stub_path).is_file():
        raise OrchestratorError('panel stub')
    return Path(stub_path)


def load_panel(path=None):
    """Load a panel object. The committed stub must match the pin and stay unadmitted."""
    path = select_panel_path() if path is None else Path(path)
    canonical = {
        PANEL_CAPTURE.resolve(),
        (ROOT / 'panel_stub.json').resolve(),
        (ROOT / PANEL_ALIAS).resolve(),
        (LAB_BUNDLE / 'panel_stub.json').resolve(),
        (LAB_BUNDLE / PANEL_ALIAS).resolve(),
    }
    if path.resolve() in canonical:
        _assert_authentic_bytes()
        _assert_digest(path, PANEL_STUB_SHA256, PANEL_BYTES)
    payload = json.loads(path.read_text())
    return _validate_panel(payload)


def load_scout():
    _assert_authentic_bytes()
    return _validate_scout(_read_pinned(SCOUT_PATH, SCOUT_SHA256, SCOUT_BYTES))


def load_seed():
    scout = load_scout()
    return _validate_seed(_read_pinned(SEED_PATH, SEED_SHA256, SEED_BYTES), scout)


def load_reget():
    scout = load_scout()
    return _validate_reget(_read_pinned(REGET_PATH, REGET_SHA256, REGET_BYTES), scout)


def gap_ticker_from_panel(panel):
    """The gap ticker is the stub row whose artifact name is the 429 file."""
    found = []
    for market in panel.get('markets') or []:
        artifact = market.get('live_get_artifact') or ''
        if artifact.endswith(GAP_FILE):
            found.append(market.get('market_ticker'))
    if found != [GAP_TICKER]:
        raise OrchestratorError('gap ticker')
    return GAP_TICKER


def assert_occurrence_triple(reget_market, seed_row, panel_market):
    """Require one shared occurrence_datetime. Does not write a match count."""
    if not isinstance(reget_market, dict) or not isinstance(seed_row, dict) or not isinstance(panel_market, dict):
        raise OccurrenceIntegrityRefused()
    values = (
        reget_market.get('occurrence_datetime'),
        seed_row.get('occurrence_datetime'),
        panel_market.get('occurrence_datetime'),
    )
    if any(not isinstance(value, str) or not value.endswith('Z') for value in values):
        raise OccurrenceIntegrityRefused()
    if len(set(values)) != 1:
        raise OccurrenceIntegrityRefused()
    return values[0]


def occurrence_agreement_tickers(panel=None):
    """Tickers whose reget, seed, and panel timestamps already agree.

    The 429 gap is absent. This list is not occurrence_match_n.
    """
    if panel is None:
        panel = load_panel()
    else:
        _validate_panel(panel)
    reget = load_reget()['markets']
    seed_rows = {row['ticker']: row for row in load_seed()['markets'] if 'ticker' in row}
    by_ticker = {market.get('market_ticker'): market for market in panel.get('markets') or []}
    agreed = []
    for ticker, market in reget.items():
        if ticker == GAP_FILE:
            continue
        if ticker not in seed_rows or ticker not in by_ticker:
            raise InventedMarketRefused()
        assert_occurrence_triple(market, seed_rows[ticker], by_ticker[ticker])
        agreed.append(ticker)
    if GAP_TICKER in agreed:
        raise InventedSoTRefused()
    if len(agreed) != AGREEMENT_ROWS_N:
        raise OrchestratorError('occurrence rows')
    return tuple(sorted(agreed))


def structural_rows(panel=None):
    """Label authentic reget rows. Does not write scorecard counts."""
    if panel is None:
        panel = load_panel()
    else:
        _validate_panel(panel)
    gap_ticker_from_panel(panel)
    agreed = set(occurrence_agreement_tickers(panel))
    reget = load_reget()['markets']
    rows = []
    for key, market in reget.items():
        if key == GAP_FILE:
            rows.append({
                'key': GAP_FILE,
                'panel_ticker': GAP_TICKER,
                'j0': 'honest_429_gap',
                'j1': 'honest_429_gap',
                'result': None,
            })
            continue
        if key not in agreed:
            raise OccurrenceIntegrityRefused()
        result = market.get('result')
        status = market.get('status')
        if status == 'finalized' and result in FINALIZED_RESULTS:
            j0 = 'nonempty_result_required_pass'
        elif status == 'active' and result == '':
            j0 = 'active_empty_result'
            result = ''
        else:
            raise InventedResultRefused()
        rows.append({
            'key': key,
            'panel_ticker': key,
            'j0': j0,
            'j1': 'occurrence_datetime_match',
            'result': result,
        })
    labels = {row['j0'] for row in rows}
    if labels != {'nonempty_result_required_pass', 'active_empty_result', 'honest_429_gap'}:
        raise OrchestratorError('row labels')
    if sum(1 for row in rows if row['j0'] == 'nonempty_result_required_pass') != SCOUT_NONEMPTY_N:
        raise OrchestratorError('row labels')
    if sum(1 for row in rows if row['j0'] == 'honest_429_gap') != 1:
        raise InventedResultRefused()
    return rows


def arm_table():
    return tuple({'id': arm, 'join_gate': JOIN_GATE[arm]} for arm in ARMS)


def instrument_binding(panel=None):
    """One join-gate knob. Fee and rails commits stay unloaded. No scorecard fill."""
    if panel is None:
        panel = load_panel()
    pins = conductor_pin_status()
    if pins['conductor_bytes_in_checkout'] is not True:
        raise OrchestratorError('conductor bytes')
    if pins['governance_tree_present'] is not False:
        raise OrchestratorError('governance tree')
    rows = structural_rows(panel)
    agreed = occurrence_agreement_tickers(panel)
    if len(agreed) != AGREEMENT_ROWS_N:
        raise OrchestratorError('occurrence rows')
    if GAP_TICKER in agreed:
        raise InventedSoTRefused()
    return {
        'experiment_id': EXPERIMENT_ID,
        'lab_directory': LAB_DIRECTORY,
        'feature_family': FEATURE_FAMILY,
        'knob': KNOB,
        'arms': arm_table(),
        'panel_version': panel['panel_version'],
        'admitted_at': panel.get('admitted_at'),
        'parent_packet_id': PARENT_PACKET_ID,
        'events_n': len(panel.get('events') or []),
        'markets_n': len(panel.get('markets') or []),
        'settled_nonempty_result_N_scout': SCOUT_NONEMPTY_N,
        'chi_429_file': GAP_FILE,
        'chi_429_panel_ticker': GAP_TICKER,
        'chi_429_backfilled': False,
        'occurrence_sources_agree': True,
        'fee_import_used': False,
        'rails_import_used': False,
        'fee_arms': False,
        'feebook_commit_fixed_not_loaded': FEEBOOK_COMMIT,
        'rails_commit_fixed_not_loaded': RAILS_COMMIT,
        'lee_ready': 'REFUSED',
        'logan_keys_required': False,
        'live_orders': False,
        'cap_sr_reopen': False,
        'fq_reopen': False,
        'eth_fq_reopen': False,
        'empty_ob_reopen': False,
        'c3_bordering_reopen': False,
        'arm_b_touch': False,
        'admit_py_run': False,
        'does_not_ungate': list(DOES_NOT_UNGATE),
        's1_s2_r2p4_ungated': False,
        'examiner_status': 'NOT_SCORED',
        'stub_ready': False,
        'scorecard_fields': SCORECARD_FIELDS,
        'row_label_count': len(rows),
        'freeze_sha256': FREEZE_SHA256,
        'scout_reget_sha256': SCOUT_SHA256,
        'seed_summary_sha256': SEED_SHA256,
        'panel_stub_sha256': PANEL_STUB_SHA256,
        'settled_reget_sha256': REGET_SHA256,
        'conductor_accept_sha256': ACCEPT_SHA256,
        'frozen_experiment_sha256': FROZEN_SHA256,
        'empty_results_sha256': EMPTY_SHA256,
        'source_pins_sha256': SOURCE_PINS_SHA256,
        'conductor_bytes_in_checkout': True,
        'governance_tree_present': False,
        'base_commit': BASE_COMMIT,
        'results': None,
        'pnl': None,
        'settled_join_n': None,
        'occurrence_match_n': None,
        'admit_ready_flag': None,
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
    scorecard['chi_429_backfilled'] = False
    return scorecard


def assert_null_scorecard(payload):
    """Require every instrument field, results, and pnl, and require null."""
    if not isinstance(payload, dict):
        raise ScorecardPromotionRefused()
    for key in OUTPUT_KEYS:
        if key not in payload or payload[key] is not None:
            raise ScorecardPromotionRefused()
    return payload


def load_scorecard(path):
    """Read a null scorecard. Non-null fields are refused."""
    path = Path(path)
    payload = json.loads(path.read_bytes())
    return assert_null_scorecard(payload)


def write_scorecard(payload):
    """Refuse a missing or non-null measurement field. Nothing is written."""
    assert_null_scorecard(payload)
    raise ScorecardPromotionRefused()


def _report(arm, extra):
    if arm not in JOIN_GATE:
        raise UnknownGate()
    published = published_scorecard()
    report = {
        'experiment_id': EXPERIMENT_ID,
        'arm': arm,
        'join_gate': JOIN_GATE[arm],
        'source': 'authentic_reget',
        'published': published,
        'promoted': False,
        'live_orders': False,
        'lee_ready': 'REFUSED',
        'fee_import_used': False,
        'rails_import_used': False,
        'admit_py_run': False,
        'chi_429_backfilled': False,
        'c3_bordering_reopen': False,
        'fq_reopen': False,
        'cap_sr_reopen': False,
        'arm_b_touch': False,
        's1_s2_r2p4_ungated': False,
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
    """Schema for one join gate. Scorecard fields stay null."""
    if arm not in JOIN_GATE:
        raise UnknownGate()
    if panel is None:
        panel = load_panel()
    rows = structural_rows(panel)
    agreed = occurrence_agreement_tickers(panel)
    extra = {
        'row_labels': rows,
        'occurrence_agreement_tickers': list(agreed),
        'admitted_at': panel.get('admitted_at'),
        'event_count': len(panel.get('events') or []),
        'market_count': len(panel.get('markets') or []),
    }
    return _report(arm, extra)


def frozen_output_snapshot():
    """Read freeze files. Does not modify them."""
    frozen_payloads = {
        'frozen': json.loads(FROZEN_EXPERIMENT.read_text()),
        'bundle_frozen': json.loads((LAB_BUNDLE / 'FROZEN_EXPERIMENT.json').read_text()),
    }
    empty_payloads = {
        'empty': json.loads(EMPTY_RESULTS.read_text()),
        'bundle_results': json.loads((LAB_BUNDLE / 'results.json').read_text()),
        'bundle_empty': json.loads((LAB_BUNDLE / 'results' / 'EMPTY_RESULTS.json').read_text()),
    }
    snapshot = {}
    for name, payload in frozen_payloads.items():
        for key in ('results', 'pnl'):
            if key not in payload or payload[key] is not None:
                raise ScorecardPromotionRefused()
            snapshot['%s.%s' % (name, key)] = None
        if payload.get('admitted_at') is not None:
            raise OrchestratorError('admitted_at')
    for name, payload in empty_payloads.items():
        for key in OUTPUT_KEYS:
            if key not in payload or payload[key] is not None:
                raise ScorecardPromotionRefused()
            snapshot['%s.%s' % (name, key)] = None
    return snapshot
