"""R3-P3 FL maker/taker settled-resolution join harness.

Measurement only. One knob: join_gate. This module does not edit the
R3-P3 fee lab, the C3-RJ lab, the C5-RJ lab, feebook, rails, Cap-SR, or
any FQ sibling. It does not place orders, does not read Logan keys, does
not run admit.py, and does not write scorecard metrics.

The checkout freeze, scout reget, seed summary, panel stub, settled
reget, and accept match the attached sha256 values. The panel stub keeps
admitted_at null and result null. The CHI settled list and the NY open
list stay the honest 429 gaps. Lee-Ready is refused. Settled results,
depth, fills, and PnL are not invented. Scout settled_nonempty_result_N
is a pin and is not copied into settled_join_n.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PARENT = ROOT.parent

LAB_DIRECTORY = 'kalshi_r3p3_fl_settled_join_lab_20260923'
EXPERIMENT_ID = 'R3P3-FL-MAKER-TAKER-SETTLED-RESOLUTION-JOIN-HARNESS'
FEATURE_FAMILY = 'R3P3-RJ'
SCOUT_PACKET = 'R3P3-FL-MAKER-TAKER-SETTLED-JOIN'
PARENT_PACKET_ID = 'R3-P3-FL-MAKER-TAKER'
PANEL_VERSION = '2026-09-22.r3-p3-fl-maker-taker-v0'
SCHEMA_ID = 'astra.registry.r3_p3_fl_maker_taker_panel.v0'
SERIES = ('KXHIGHNY', 'KXHIGHCHI')
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
SCOUT_NONEMPTY_N = 20
PARENT_SEED_N = 3
REGET_MARKET_N = 21
YES_N = 4
NO_N = 17
PANEL_EVENTS_N = 2
PANEL_MARKETS_N = 3
PANEL_TRADES_N = 15
ROW_LABEL_N = 23
OPEN_LIST_N = 4
OCCURRENCE_SOT = '2026-09-23T14:00:00Z'
NY_SETTLED_FILE = 'markets_settled_KXHIGHNY_lim20.json'
CHI_SETTLED_FILE = 'markets_settled_KXHIGHCHI_lim20.json'
NY_OPEN_FILE = 'markets_open_KXHIGHNY_lim4.json'
CHI_OPEN_FILE = 'markets_open_KXHIGHCHI_lim4.json'
NY_SERIES_FILE = 'series_KXHIGHNY.json'
CHI_SERIES_FILE = 'series_KXHIGHCHI.json'
SEED_FILES = {
    'KXHIGHNY-26SEP22-B67.5': 'market_KXHIGHNY_26SEP22_B67_5.json',
    'KXHIGHNY-26SEP22-T70': 'market_KXHIGHNY_26SEP22_T70.json',
    'KXHIGHCHI-26SEP22-B64.5': 'market_KXHIGHCHI_26SEP22_B64_5.json',
}
ARTIFACT_NAMES = (
    NY_SERIES_FILE,
    CHI_SERIES_FILE,
    NY_SETTLED_FILE,
    CHI_SETTLED_FILE,
    NY_OPEN_FILE,
    CHI_OPEN_FILE,
    'market_KXHIGHNY_26SEP22_B67_5.json',
    'market_KXHIGHNY_26SEP22_T70.json',
    'market_KXHIGHCHI_26SEP22_B64_5.json',
    'events_settled_KXHIGHNY_lim5.json',
    'events_settled_KXHIGHCHI_lim5.json',
)
PARENT_SEED_TICKERS = (
    'KXHIGHNY-26SEP22-B67.5',
    'KXHIGHNY-26SEP22-T70',
    'KXHIGHCHI-26SEP22-B64.5',
)
PARENT_SEED_RESULTS = {
    'KXHIGHNY-26SEP22-B67.5': 'yes',
    'KXHIGHNY-26SEP22-T70': 'no',
    'KXHIGHCHI-26SEP22-B64.5': 'yes',
}
CHI_SEED = 'KXHIGHCHI-26SEP22-B64.5'
NY_SEED_TICKERS = (
    'KXHIGHNY-26SEP22-B67.5',
    'KXHIGHNY-26SEP22-T70',
)
OPEN_TICKERS = (
    'KXHIGHCHI-26SEP24-T73',
    'KXHIGHCHI-26SEP24-T66',
    'KXHIGHCHI-26SEP24-B72.5',
    'KXHIGHCHI-26SEP24-B70.5',
)
SCOUT_LIST_SOURCE = 'markets_settled_KXHIGHNY_lim20.json'
SCOUT_CHI_SOURCE = 'market_KXHIGHCHI_26SEP22_B64_5.json'
GAP_CHI_SETTLED = 'markets_settled_KXHIGHCHI'
GAP_NY_OPEN = 'markets_open_KXHIGHNY'
GAP_KEYS = (GAP_CHI_SETTLED, GAP_NY_OPEN)
GAP_TEXT = '429 too_many_requests'
SCOUT_HONEST_GAPS = (
    'markets?series_ticker=KXHIGHCHI&status=settled 429',
    'markets?series_ticker=KXHIGHNY&status=open 429',
)
RESOLUTION_JOIN_STATUS = (
    'PRE_SETTLEMENT — result empty; close_time future vs stub clock; not joined'
)
HTTP_LOG_N = 18
RATE_LIMIT_ERROR = {'code': 'too_many_requests', 'message': 'too many requests'}
FEEBOOK_COMMIT = '22371178cb2663250b4762f328069571c48cb551'
RAILS_COMMIT = '6a28e0d6254327ea4e6451c781bec56215ac6cac'
BASE_COMMIT = '8cfcd17a62d3793dee554a4da422e8075bde9cf6'
FREEZE_SHA256 = '7fcfc36ab4761e2dec56018b498372fb63c402f2582fe848e8775e28f9b720b9'
SCOUT_SHA256 = 'f675d7c40ccad37173b2cb54837349cd3053b7b76606c43efba5759a1bde551f'
SEED_SHA256 = 'b43d4ab065b712f5bf1b87eb164bccb00e8e9993f97db9d86a8d1619ce9ec13d'
PANEL_STUB_SHA256 = '6f640dd3a6091ba6b896ded38fdded4676583aa3c885223da21ddf03780250c0'
REGET_SHA256 = 'c5f680e4ff66af67691672c4b8c43eb57906f25b4d79fdeb65f61e031c13efda'
ACCEPT_SHA256 = 'a6434fe4854b850df24a0a081168ba5d90d4646ba9a409418d7b874262a5fa9c'
FROZEN_SHA256 = 'dd2a4217de4476d9c54a4487e68fe7bd912914bb55a5a1be4bc00126199f19e0'
EMPTY_SHA256 = 'd0f5fbfa3e01fca5f047f42ecc7e1bb5b1d4097ee455d6ce62a4b8a861d4a613'
SOURCE_PINS_SHA256 = '4b94c1823017f7fe725e98ece11ac42dd16fabd415e81b2f3c4d08b0f1c5eb3a'
FREEZE_BYTES = 5735
SCOUT_BYTES = 7452
SEED_BYTES = 7282
PANEL_BYTES = 21386
REGET_BYTES = 114109
ACCEPT_BYTES = 1569
FROZEN_BYTES = 1055
EMPTY_BYTES = 168
SOURCE_PINS_BYTES = 4415
ACCEPT_STAMPED_AT = '2026-09-23T15:43:00-04:00'
FROZEN_STAMPED_AT = '2026-09-23T15:33:00-04:00'
SCOUT_FETCHED_AT = '2026-09-23T15:41:00-04:00'
EMPTY_NOTE = 'pre-ACCEPT empty; R3P3-RJ measurement join only'
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
    'C3_RJ_reopen',
    'C5_RJ_reopen',
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
    'list_429_backfill': 'CHI settled and NY open list 429 backfill is refused',
    'open_ticker_invent': 'invented open ticker market is refused',
    'fq_reopen': 'FQ reopen is refused',
    'eth_fq_reopen': 'ETH-FQ reopen is refused',
    'nhl_fq_reopen': 'NHL-FQ reopen is refused',
    'cpi_fq_reopen': 'CPI-FQ reopen is refused',
    'atp_fq_reopen': 'ATP-FQ reopen is refused',
    'cap_sr_reopen': 'Cap-SR reopen is refused',
    'empty_ob_reopen': 'EMPTY-OB reopen is refused',
    'c3_rj_reopen': 'C3-RJ reopen is refused',
    'c5_rj_reopen': 'C5-RJ reopen is refused',
    'r3p3_fee_reopen': 'R3-P3 fee-arm reopen is refused',
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
    'kalshi_c3_kxhighny_settled_join_lab_20260923',
    'kalshi_c4_kxcpi_feequue_lab_20260923',
    'kalshi_c5_kxbtc15m_honesty_lab_20260923',
    'kalshi_c5_kxbtc15m_settled_join_lab_20260923',
    'kalshi_atp_kxatpmatch_feequue_lab_20260923',
    'kalshi_eth_kxeth15m_feequue_lab_20260923',
    'kalshi_r3p3_fl_maker_taker_lab_20260923',
    'kalshi_r3p4_l2_cat_lab_20260923',
    'kalshi_r3p4_l2_sf_lab_20260923',
    'kalshi_r3_p4_l2_shape_lab_20260922',
    'kalshi_r3_p2_queue_position_lab_20260923',
    'kalshi_s4_ncaaf_feequue_lab_20260923',
    'kalshi_s5_mve_filllegs_lab_20260923',
    'kalshi_r2p3_prop_ladder_lab_20260923',
    'kalshi_r2p5_sot_id_lab_20260923',
    'nfl_factorial_lab_20260921',
    'nfl_paircheck_lab_20260922',
    'nfl_q7_rehab_p1_cadence_20260923',
    'packets/R3_P3_FL_MAKER_TAKER_HARNESS',
    'lab/astra-capture/r3-p3-fl-maker-taker/panel_stub.json',
    'lab/governance/astra/packets/r3_p2_queue_position/results/demo_queue_sample_series.json',
)
FREEZE_NAME = 'R3_P3_FL_SETTLED_RESOLUTION_JOIN_HARNESS_FREEZE_2026-09-23.md'
SCOUT_NAME = 'scout_settled_rejoin_R3P3_FL_MAKER_TAKER.json'
SEED_NAME = 'SEED_SETTLED_SUMMARY.json'
PANEL_ALIAS = 'R3_P3_FL_MAKER_TAKER_PANEL_STUB_2026-09-22.json'
REGET_NAME = 'settled_reget_2026-09-23.json'
ACCEPT_NAME = 'CONDUCTOR_ACCEPT_R3P3_FL_SETTLED_JOIN_HARNESS_2026-09-23.json'
SOURCE_PINS_NAME = 'SOURCE_PINS.json'
LAB_BUNDLE = ROOT / 'R3_P3_FL_SETTLED_RESOLUTION_JOIN_HARNESS'
GOVERNANCE_TREE = PARENT / 'lab' / 'governance' / 'astra'
R3P3_SCOUT_CITE = GOVERNANCE_TREE / 'packets' / 'scout_r3p3_settled_rejoin_2026-09-23'
R3P3_PANEL_CITE = GOVERNANCE_TREE / 'packets' / 'R3_P3_FL_MAKER_TAKER_PANEL_STUB_2026-09-22.json'
PACKET = ROOT / FREEZE_NAME
SCOUT_PATH = ROOT / SCOUT_NAME
SEED_PATH = ROOT / SEED_NAME
REGET_PATH = ROOT / REGET_NAME
CONDUCTOR_ACCEPT = ROOT / ACCEPT_NAME
FROZEN_EXPERIMENT = ROOT / 'FROZEN_EXPERIMENT.json'
EMPTY_RESULTS = ROOT / 'results' / 'EMPTY_RESULTS.json'
SOURCE_PINS = ROOT / SOURCE_PINS_NAME
PANEL_CAPTURE = PARENT / 'lab' / 'astra-capture' / 'r3-p3-fl-maker-taker' / 'panel_stub.json'
PANEL_ADMITTED = PARENT / 'lab' / 'astra-capture' / 'r3-p3-fl-maker-taker' / 'panel_admitted.json'
REGET_CITE = PARENT / 'lab' / 'astra-capture' / 'r3-p3-fl-maker-taker' / REGET_NAME
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
    """A settled result was invented or a 429 list gap was backfilled."""

    def __init__(self):
        super().__init__('invented settled result')


class InventedFillRefused(OrchestratorError):
    """A fill was invented from volume or from a gap."""

    def __init__(self):
        super().__init__('invented fill')


class InventedDepthRefused(OrchestratorError):
    """Quote size is not a depth ladder."""

    def __init__(self):
        super().__init__('invented depth')


class InventedSoTRefused(OrchestratorError):
    """occurrence_datetime is not invented for a 429 list gap."""

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
    """The panel file is not the pinned R3-P3 seed."""

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


def backfill_list_429(which=None, result=None, occurrence_datetime=None):
    """The CHI settled and NY open 429 list gaps stay gaps. Nothing is written."""
    del which, result, occurrence_datetime
    raise InventedResultRefused()


def invent_open_ticker(ticker=None, result=None):
    """Cited open tickers are not settled-join markets."""
    del ticker, result
    raise InventedMarketRefused()


def assign_occurrence(ticker=None, value=None):
    """A missing occurrence on a 429 list gap stays missing."""
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
    if label in ('invent_settled_result', 'invented_result', 'list_429_backfill'):
        raise InventedResultRefused()
    if label in ('invent_fills', 'invented_fills'):
        raise InventedFillRefused()
    if label == 'invented_depth':
        raise InventedDepthRefused()
    if label == 'open_ticker_invent':
        raise InventedMarketRefused()
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


def _nonempty_result(value):
    return value in FINALIZED_RESULTS


def _is_rate_limit(artifact):
    return isinstance(artifact, dict) and artifact.get('error') == RATE_LIMIT_ERROR and 'markets' not in artifact


def _last_http(http_log, filename):
    hits = [row for row in http_log if row.get('file') == filename]
    if not hits:
        raise OrchestratorError('http log')
    return hits[-1].get('http')


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
    if payload.get('scout_n_copied_into_settled_join_n') is not False:
        raise ScorecardPromotionRefused()
    if payload.get('parent_seed_tickers') != list(PARENT_SEED_TICKERS):
        raise OrchestratorError('source pins')
    if payload.get('parent_seeds_finalized_nonempty_N') != PARENT_SEED_N:
        raise OrchestratorError('source pins')
    if payload.get('parent_seed_results') != PARENT_SEED_RESULTS:
        raise InventedResultRefused()
    if payload.get('seed_panel_result') is not None:
        raise InventedResultRefused()
    if payload.get('occurrence_datetime_panel_sot') != OCCURRENCE_SOT:
        raise OccurrenceIntegrityRefused()
    if payload.get('chi_settled_list_429') != GAP_TEXT or payload.get('ny_open_list_429') != GAP_TEXT:
        raise OrchestratorError('source pins')
    if payload.get('list_429_backfilled') is not False:
        raise InventedResultRefused()
    if payload.get('open_tickers_cited') != list(OPEN_TICKERS) or payload.get('open_ticker_market_invented') is not False:
        raise InventedMarketRefused()
    if payload.get('fee_import_used') is not False or payload.get('rails_import_used') is not False:
        raise OrchestratorError('source pins')
    if payload.get('fee_arms') is not False:
        raise OrchestratorError('source pins')
    if payload.get('feebook_commit_fixed_not_loaded') != FEEBOOK_COMMIT:
        raise OrchestratorError('source pins')
    if payload.get('rails_commit_fixed_not_loaded') != RAILS_COMMIT:
        raise OrchestratorError('source pins')
    if payload.get('governance_r3p3_cites') != 'absent':
        raise OrchestratorError('source pins')
    if payload.get('does_not_run_admit_py') is not True:
        raise AdmitPyRefused()
    if payload.get('base_commit') != BASE_COMMIT:
        raise OrchestratorError('source pins')
    if payload.get('lee_ready') != 'REFUSED':
        raise LeeReadyRefused()
    if payload.get('r3p3_fee_reopen') is not False or payload.get('c3_rj_reopen') is not False:
        raise OrchestratorError('source pins')
    if payload.get('c5_rj_reopen') is not False or payload.get('cap_sr_reopen') is not False:
        raise OrchestratorError('source pins')
    if payload.get('fq_reopen') is not False or payload.get('arm_b_touch') is not False:
        raise OrchestratorError('source pins')
    if payload.get('live_orders') is not False:
        raise LiveOrdersForbidden()
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
    if payload.get('packet') != SCOUT_PACKET or payload.get('feature_family') != FEATURE_FAMILY:
        raise OrchestratorError('scout')
    if payload.get('series') != list(SERIES):
        raise OrchestratorError('scout')
    if payload.get('settled_nonempty_result_N') != SCOUT_NONEMPTY_N:
        raise OrchestratorError('scout N')
    if payload.get('settled_list_limit') != SCOUT_NONEMPTY_N:
        raise OrchestratorError('scout N')
    if payload.get('settled_list_cursor_present') is not True:
        raise OrchestratorError('scout')
    if payload.get('settled_KXHIGHNY_nonempty_N') != SCOUT_NONEMPTY_N:
        raise OrchestratorError('scout N')
    if payload.get('settled_KXHIGHCHI_list') != '429_honest':
        raise InventedResultRefused()
    if payload.get('parent_seeds_finalized_nonempty_N') != PARENT_SEED_N:
        raise OrchestratorError('scout')
    if payload.get('parent_seed_tickers') != list(PARENT_SEED_TICKERS):
        raise OrchestratorError('scout')
    if payload.get('parent_seed_results') != PARENT_SEED_RESULTS:
        raise InventedResultRefused()
    if payload.get('occurrence_datetime_sot_match_all_seeds') is not True:
        raise OccurrenceIntegrityRefused()
    if payload.get('open_list_n') != OPEN_LIST_N or payload.get('open_tickers') != list(OPEN_TICKERS):
        raise InventedMarketRefused()
    if payload.get('honest_gaps') != list(SCOUT_HONEST_GAPS):
        raise InventedResultRefused()
    if payload.get('results') is not None or payload.get('pnl') is not None:
        raise ScorecardPromotionRefused()
    if payload.get('mode') != 'GET_only_public':
        raise OrchestratorError('scout mode')
    if payload.get('fetched_at_et') != SCOUT_FETCHED_AT:
        raise OrchestratorError('scout')
    if payload.get('candidate_won') != FEATURE_FAMILY:
        raise OrchestratorError('scout')
    markets = payload.get('markets')
    if not isinstance(markets, list) or len(markets) != REGET_MARKET_N:
        raise OrchestratorError('scout markets')
    list_rows = []
    chi_rows = []
    for row in markets:
        if not isinstance(row, dict):
            raise OrchestratorError('scout market')
        if row.get('nonempty_result') is not True:
            raise InventedResultRefused()
        if row.get('status') != 'finalized' or not _nonempty_result(row.get('result')):
            raise InventedResultRefused()
        ticker = row.get('ticker')
        if not isinstance(ticker, str) or ticker in OPEN_TICKERS:
            raise InventedMarketRefused()
        if row.get('source') == SCOUT_LIST_SOURCE:
            list_rows.append(row)
        elif row.get('source') == SCOUT_CHI_SOURCE and ticker == CHI_SEED:
            chi_rows.append(row)
        else:
            raise OrchestratorError('scout row')
    if len(list_rows) != SCOUT_NONEMPTY_N or len(chi_rows) != 1:
        raise OrchestratorError('scout census')
    if chi_rows[0].get('result') != PARENT_SEED_RESULTS[CHI_SEED]:
        raise InventedResultRefused()
    return payload


def _validate_seed(payload, scout):
    if payload.get('settled_nonempty_result_N') != SCOUT_NONEMPTY_N:
        raise OrchestratorError('seed N')
    if payload.get('settled_list_attempted_KXHIGHNY') != SCOUT_NONEMPTY_N:
        raise OrchestratorError('seed attempted')
    if payload.get('settled_KXHIGHCHI_list_429') is not True:
        raise InventedResultRefused()
    if payload.get('parent_seed_tickers') != list(PARENT_SEED_TICKERS):
        raise OrchestratorError('seed ticker')
    if payload.get('parent_seeds_finalized_nonempty_N') != PARENT_SEED_N:
        raise OrchestratorError('seed')
    if payload.get('parent_seed_results') != PARENT_SEED_RESULTS:
        raise InventedResultRefused()
    statuses = payload.get('parent_seed_statuses')
    if statuses != {ticker: 'finalized' for ticker in PARENT_SEED_TICKERS}:
        raise InventedResultRefused()
    if payload.get('occurrence_datetime_panel_sot') != OCCURRENCE_SOT:
        raise OccurrenceIntegrityRefused()
    if payload.get('occurrence_datetime_match_all_seeds') is not True:
        raise OccurrenceIntegrityRefused()
    if payload.get('open_list_n') != OPEN_LIST_N or payload.get('open_tickers') != list(OPEN_TICKERS):
        raise InventedMarketRefused()
    if payload.get('candidate_won') != FEATURE_FAMILY:
        raise OrchestratorError('seed candidate')
    if payload.get('markets') != scout.get('markets'):
        raise OrchestratorError('seed scout markets')
    return payload


def _market_object(artifact, ticker):
    market = artifact.get('market') if isinstance(artifact, dict) else None
    if not isinstance(market, dict) or market.get('ticker') != ticker:
        raise InventedMarketRefused()
    if 'orderbook_fp' in market:
        raise InventedDepthRefused()
    return market


def _validate_reget(payload, scout):
    if payload.get('packet') != SCOUT_PACKET or payload.get('feature_family') != FEATURE_FAMILY:
        raise OrchestratorError('reget')
    if payload.get('mode') != 'GET_only_public':
        raise OrchestratorError('reget mode')
    if payload.get('fetched_at_et') != SCOUT_FETCHED_AT:
        raise OrchestratorError('reget')
    if payload.get('settled_nonempty_result_N') != SCOUT_NONEMPTY_N:
        raise OrchestratorError('reget N')
    if payload.get('results') is not None or payload.get('pnl') is not None:
        raise ScorecardPromotionRefused()
    artifacts = payload.get('artifacts')
    if not isinstance(artifacts, dict) or tuple(artifacts) != ARTIFACT_NAMES:
        raise OrchestratorError('reget artifacts')
    http_log = payload.get('http_log')
    if not isinstance(http_log, list) or len(http_log) != HTTP_LOG_N:
        raise OrchestratorError('http log')
    for row in http_log:
        if not isinstance(row, dict):
            raise OrchestratorError('http log')
        url = row.get('url')
        if not isinstance(url, str) or not url.startswith(PUBLIC_HOST + '/'):
            raise OrchestratorError('reget host')
        if 'portfolio/orders' in url:
            raise LiveOrdersForbidden()
        if row.get('http') not in (200, 429):
            raise OrchestratorError('http log')
    if not _is_rate_limit(artifacts.get(CHI_SETTLED_FILE)) or not _is_rate_limit(artifacts.get(NY_OPEN_FILE)):
        raise InventedResultRefused()
    if _last_http(http_log, CHI_SETTLED_FILE) != 429 or _last_http(http_log, NY_OPEN_FILE) != 429:
        raise InventedResultRefused()
    if _last_http(http_log, NY_SETTLED_FILE) != 200:
        raise OrchestratorError('reget')
    for filename in SEED_FILES.values():
        if _last_http(http_log, filename) != 200:
            raise OrchestratorError('reget')
    if _last_http(http_log, CHI_OPEN_FILE) != 200:
        raise OrchestratorError('reget')
    for series_file, series_name in ((NY_SERIES_FILE, 'KXHIGHNY'), (CHI_SERIES_FILE, 'KXHIGHCHI')):
        series = (artifacts.get(series_file) or {}).get('series')
        if not isinstance(series, dict) or series.get('ticker') != series_name:
            raise OrchestratorError('reget series')
    ny_page = artifacts.get(NY_SETTLED_FILE)
    if not isinstance(ny_page, dict) or not ny_page.get('cursor'):
        raise OrchestratorError('reget')
    ny_markets = ny_page.get('markets')
    if not isinstance(ny_markets, list) or len(ny_markets) != SCOUT_NONEMPTY_N:
        raise OrchestratorError('reget markets')
    settled = {}
    for market in ny_markets:
        if not isinstance(market, dict):
            raise InventedMarketRefused()
        ticker = market.get('ticker')
        if not isinstance(ticker, str) or ticker in settled or ticker in OPEN_TICKERS:
            raise InventedMarketRefused()
        if 'orderbook_fp' in market:
            raise InventedDepthRefused()
        if market.get('status') != 'finalized' or not _nonempty_result(market.get('result')):
            raise InventedResultRefused()
        settled[ticker] = market
    if CHI_SEED in settled:
        raise InventedMarketRefused()
    for ticker, filename in SEED_FILES.items():
        direct = _market_object(artifacts.get(filename), ticker)
        if direct.get('status') != 'finalized' or direct.get('result') != PARENT_SEED_RESULTS[ticker]:
            raise InventedResultRefused()
        if direct.get('occurrence_datetime') != OCCURRENCE_SOT:
            raise OccurrenceIntegrityRefused()
        if ticker in settled:
            for field in COMPARE_FIELDS:
                if settled[ticker].get(field) != direct.get(field):
                    raise OrchestratorError('seed list ' + field)
        else:
            settled[ticker] = direct
    if len(settled) != REGET_MARKET_N:
        raise OrchestratorError('reget census')
    chi_open = artifacts.get(CHI_OPEN_FILE)
    if not isinstance(chi_open, dict) or not chi_open.get('cursor'):
        raise OrchestratorError('reget')
    open_markets = chi_open.get('markets')
    if not isinstance(open_markets, list) or len(open_markets) != OPEN_LIST_N:
        raise InventedMarketRefused()
    open_tickers = []
    for market in open_markets:
        if not isinstance(market, dict):
            raise InventedMarketRefused()
        if market.get('status') != 'active' or market.get('result') != '':
            raise InventedResultRefused()
        open_tickers.append(market.get('ticker'))
    if open_tickers != list(OPEN_TICKERS):
        raise InventedMarketRefused()
    for ticker in OPEN_TICKERS:
        if ticker in settled:
            raise InventedMarketRefused()
    scout_rows = {}
    for row in scout.get('markets') or []:
        scout_rows[row['ticker']] = row
    if set(scout_rows) != set(settled):
        raise InventedMarketRefused()
    yes_n = 0
    no_n = 0
    for ticker, market in settled.items():
        scout_row = scout_rows[ticker]
        for field in COMPARE_FIELDS:
            if market.get(field) != scout_row.get(field):
                raise OrchestratorError('scout reget ' + field)
        if scout_row.get('nonempty_result') is not True:
            raise InventedResultRefused()
        if market.get('result') == 'yes':
            yes_n += 1
        else:
            no_n += 1
    if yes_n != YES_N or no_n != NO_N:
        raise OrchestratorError('reget census')
    for ticker in PARENT_SEED_TICKERS:
        if settled[ticker].get('result') != PARENT_SEED_RESULTS[ticker]:
            raise InventedResultRefused()
        if settled[ticker].get('occurrence_datetime') != OCCURRENCE_SOT:
            raise OccurrenceIntegrityRefused()
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
    if payload.get('stub_status') != STUB_STATUS:
        raise OrchestratorError('stub_status')
    if payload.get('admitted_at') is not None:
        raise OrchestratorError('admitted_at')
    for key in ('results', 'pnl', 'volume'):
        if key not in payload or payload[key] is not None:
            raise ScorecardPromotionRefused()
    counts = payload.get('cohort_counts') or {}
    if counts.get('events_n') != PANEL_EVENTS_N or counts.get('markets_n') != PANEL_MARKETS_N:
        raise OrchestratorError('cohort')
    if counts.get('series_n') != 2 or counts.get('trades_sampled_n') != PANEL_TRADES_N:
        raise OrchestratorError('cohort')
    if counts.get('settled_markets_resolved_n') != 0:
        raise InventedResultRefused()
    events = payload.get('events')
    markets = payload.get('markets')
    trades = payload.get('trades_sample')
    if not isinstance(events, list) or len(events) != PANEL_EVENTS_N:
        raise OrchestratorError('events')
    if not isinstance(markets, list) or len(markets) != PANEL_MARKETS_N:
        raise OrchestratorError('markets')
    if not isinstance(trades, list) or len(trades) != PANEL_TRADES_N:
        raise OrchestratorError('trades')
    for trade in trades:
        if not isinstance(trade, dict) or trade.get('lee_ready') != 'REFUSED':
            raise LeeReadyRefused()
    event_tickers = []
    covered = []
    for event in events:
        if not isinstance(event, dict):
            raise OrchestratorError('events')
        if event.get('admitted_at') is not None or event.get('panel_version') != PANEL_VERSION:
            raise OrchestratorError('admitted_at')
        if event.get('occurrence_datetime') != OCCURRENCE_SOT:
            raise OccurrenceIntegrityRefused()
        names = event.get('market_tickers')
        if not isinstance(names, list):
            raise InventedMarketRefused()
        event_tickers.append(event.get('event_ticker'))
        covered.extend(names)
    if event_tickers != ['KXHIGHNY-26SEP22', 'KXHIGHCHI-26SEP22']:
        raise OrchestratorError('events')
    if covered != list(PARENT_SEED_TICKERS):
        raise InventedMarketRefused()
    seen = []
    for market in markets:
        if not isinstance(market, dict):
            raise OrchestratorError('market')
        if market.get('admitted_at') is not None or market.get('panel_version') != PANEL_VERSION:
            raise OrchestratorError('admitted_at')
        if market.get('result') is not None:
            raise InventedResultRefused()
        if market.get('status_at_stub') != 'active':
            raise InventedResultRefused()
        if market.get('resolution_join_status') != RESOLUTION_JOIN_STATUS:
            raise InventedResultRefused()
        if market.get('occurrence_datetime') != OCCURRENCE_SOT:
            raise OccurrenceIntegrityRefused()
        seen.append(market.get('market_ticker'))
    if seen != list(PARENT_SEED_TICKERS):
        raise InventedMarketRefused()
    return payload


def _assert_frozen(payload):
    if payload.get('packet_id') != EXPERIMENT_ID:
        raise OrchestratorError('frozen')
    if payload.get('feature_family') != FEATURE_FAMILY:
        raise OrchestratorError('frozen')
    if payload.get('status') != 'FROZEN_EXPERIMENT':
        raise OrchestratorError('frozen')
    if payload.get('lab_dir') != LAB_DIRECTORY + '/':
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
    if payload.get('lab') != LAB_DIRECTORY + '/':
        raise OrchestratorError('conductor accept')
    if payload.get('knob') != KNOB or payload.get('arms') != JOIN_GATE:
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
    if R3P3_SCOUT_CITE.exists():
        raise OrchestratorError('governance cite')
    if R3P3_PANEL_CITE.exists():
        _assert_digest(R3P3_PANEL_CITE, PANEL_STUB_SHA256, PANEL_BYTES)
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
    return True


def conductor_pin_status():
    """Report whether checkout bytes match the attached conductor sha256 values."""
    freeze_match = sha256_file(PACKET) == FREEZE_SHA256
    scout_match = sha256_file(SCOUT_PATH) == SCOUT_SHA256
    seed_match = sha256_file(SEED_PATH) == SEED_SHA256
    panel_match = sha256_file(PANEL_CAPTURE) == PANEL_STUB_SHA256
    reget_match = sha256_file(REGET_PATH) == REGET_SHA256
    accept_match = sha256_file(CONDUCTOR_ACCEPT) == ACCEPT_SHA256
    cites_present = R3P3_SCOUT_CITE.exists() or R3P3_PANEL_CITE.is_file()
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
        'governance_r3p3_cites_present': cites_present,
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


def _settled_view(payload, scout):
    """In-memory settled index. This view is not written back to the reget file."""
    checked = _validate_reget(payload, scout)
    artifacts = checked['artifacts']
    markets = {}
    for market in artifacts[NY_SETTLED_FILE]['markets']:
        markets[market['ticker']] = market
    chi = artifacts[SEED_FILES[CHI_SEED]]['market']
    markets[chi['ticker']] = chi
    view = dict(checked)
    view['markets'] = markets
    view['honest_gaps'] = {
        GAP_CHI_SETTLED: GAP_TEXT,
        GAP_NY_OPEN: GAP_TEXT,
    }
    return view


def load_reget():
    scout = load_scout()
    payload = _read_pinned(REGET_PATH, REGET_SHA256, REGET_BYTES)
    return _settled_view(payload, scout)


def list_429_gaps(reget=None):
    """The CHI settled list and the NY open list. No ticker and no result are attached."""
    if reget is None:
        reget = load_reget()
    gaps = reget.get('honest_gaps')
    if gaps != {GAP_CHI_SETTLED: GAP_TEXT, GAP_NY_OPEN: GAP_TEXT}:
        raise InventedResultRefused()
    artifacts = reget.get('artifacts') or {}
    if not _is_rate_limit(artifacts.get(CHI_SETTLED_FILE)) or not _is_rate_limit(artifacts.get(NY_OPEN_FILE)):
        raise InventedResultRefused()
    markets = reget.get('markets') or {}
    for key in GAP_KEYS:
        if key in markets:
            raise InventedResultRefused()
    return GAP_KEYS


def assert_occurrence_pair(reget_market, seed_row):
    """Require one shared occurrence_datetime. Does not write a match count."""
    if not isinstance(reget_market, dict) or not isinstance(seed_row, dict):
        raise OccurrenceIntegrityRefused()
    values = (
        reget_market.get('occurrence_datetime'),
        seed_row.get('occurrence_datetime'),
    )
    if any(not isinstance(value, str) or not value.endswith('Z') for value in values):
        raise OccurrenceIntegrityRefused()
    if values[0] != values[1]:
        raise OccurrenceIntegrityRefused()
    return values[0]


def occurrence_agreement_tickers(panel=None):
    """Parent seeds whose panel, reget, and seed timestamps are the SoT.

    Other settled-list rows may share a clock with the reget and the seed
    summary. They are not this panel SoT set. The 429 gaps and the cited
    open tickers are absent. This list is not occurrence_match_n.
    """
    if panel is None:
        panel = load_panel()
    else:
        _validate_panel(panel)
    reget = load_reget()['markets']
    seed_rows = {row['ticker']: row for row in load_seed()['markets']}
    by_ticker = {market.get('market_ticker'): market for market in panel.get('markets') or []}
    if set(by_ticker) != set(PARENT_SEED_TICKERS):
        raise InventedMarketRefused()
    if set(reget) != set(seed_rows):
        raise InventedMarketRefused()
    for ticker, market in reget.items():
        assert_occurrence_pair(market, seed_rows[ticker])
    agreed = []
    for ticker in PARENT_SEED_TICKERS:
        market = reget[ticker]
        panel_market = by_ticker[ticker]
        if panel_market.get('occurrence_datetime') != market.get('occurrence_datetime'):
            raise OccurrenceIntegrityRefused()
        if market.get('occurrence_datetime') != OCCURRENCE_SOT:
            raise OccurrenceIntegrityRefused()
        if panel_market.get('close_time') != market.get('close_time'):
            raise OccurrenceIntegrityRefused()
        if panel_market.get('result') is not None:
            raise InventedResultRefused()
        agreed.append(ticker)
    if any(ticker in agreed for ticker in OPEN_TICKERS):
        raise InventedMarketRefused()
    if len(agreed) != PARENT_SEED_N:
        raise OrchestratorError('occurrence rows')
    return tuple(agreed)


def structural_rows(panel=None):
    """Label authentic reget rows. Does not write scorecard counts."""
    if panel is None:
        panel = load_panel()
    else:
        _validate_panel(panel)
    list_429_gaps()
    agreed = set(occurrence_agreement_tickers(panel))
    reget = load_reget()['markets']
    seed_rows = {row['ticker']: row for row in load_seed()['markets']}
    rows = []
    for key, market in reget.items():
        result = market.get('result')
        if market.get('status') != 'finalized' or result not in FINALIZED_RESULTS:
            raise InventedResultRefused()
        source = seed_rows[key].get('source')
        on_list = source == SCOUT_LIST_SOURCE
        parent_seed = key in PARENT_SEED_TICKERS
        if parent_seed and key not in agreed:
            raise OccurrenceIntegrityRefused()
        if on_list and parent_seed and key not in NY_SEED_TICKERS:
            raise OrchestratorError('row source')
        if parent_seed and not on_list and key != CHI_SEED:
            raise OrchestratorError('row source')
        if not parent_seed and not on_list:
            raise OrchestratorError('row source')
        if parent_seed:
            j1 = 'occurrence_datetime_match'
        else:
            j1 = 'list_occurrence_not_panel_seed'
        rows.append({
            'key': key,
            'panel_ticker': key if parent_seed else None,
            'j0': 'nonempty_result_required_pass',
            'j1': j1,
            'result': result,
            'on_settled_list': on_list,
            'parent_seed': parent_seed,
        })
    for key in GAP_KEYS:
        rows.append({
            'key': key,
            'panel_ticker': None,
            'j0': 'honest_429_gap',
            'j1': 'honest_429_gap',
            'result': None,
            'on_settled_list': False,
            'parent_seed': False,
        })
    if len(rows) != ROW_LABEL_N:
        raise OrchestratorError('row labels')
    passes = [row for row in rows if row['j0'] == 'nonempty_result_required_pass']
    gaps = [row for row in rows if row['j0'] == 'honest_429_gap']
    if len(passes) != REGET_MARKET_N or len(gaps) != len(GAP_KEYS):
        raise OrchestratorError('row labels')
    if sum(1 for row in passes if row['on_settled_list']) != SCOUT_NONEMPTY_N:
        raise OrchestratorError('row labels')
    seed_rows_out = [row for row in passes if row['parent_seed']]
    if len(seed_rows_out) != PARENT_SEED_N:
        raise OrchestratorError('row labels')
    if {row['key'] for row in seed_rows_out} != set(PARENT_SEED_TICKERS):
        raise OrchestratorError('row labels')
    for row in seed_rows_out:
        if row['result'] != PARENT_SEED_RESULTS[row['key']]:
            raise InventedResultRefused()
        if row['panel_ticker'] != row['key']:
            raise OrchestratorError('row labels')
    if any(ticker in {row['key'] for row in rows} for ticker in OPEN_TICKERS):
        raise InventedMarketRefused()
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
    if pins['governance_r3p3_cites_present'] is not False:
        raise OrchestratorError('governance cite')
    rows = structural_rows(panel)
    agreed = occurrence_agreement_tickers(panel)
    if len(agreed) != PARENT_SEED_N:
        raise OrchestratorError('occurrence rows')
    if any(ticker in agreed for ticker in OPEN_TICKERS):
        raise InventedMarketRefused()
    panel_results = [market.get('result') for market in panel.get('markets') or []]
    if panel_results != [None, None, None]:
        raise InventedResultRefused()
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
        'scout_n_copied_into_settled_join_n': False,
        'parent_seed_tickers': list(PARENT_SEED_TICKERS),
        'parent_seeds_finalized_nonempty_N': PARENT_SEED_N,
        'parent_seed_results': dict(PARENT_SEED_RESULTS),
        'seed_panel_result': None,
        'occurrence_datetime_panel_sot': OCCURRENCE_SOT,
        'open_tickers_cited': list(OPEN_TICKERS),
        'open_ticker_market_invented': False,
        'chi_settled_list_429': GAP_TEXT,
        'ny_open_list_429': GAP_TEXT,
        'list_429_backfilled': False,
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
        'empty_ob_reopen': False,
        'r3p3_fee_reopen': False,
        'c3_rj_reopen': False,
        'c5_rj_reopen': False,
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
        'governance_r3p3_cites_present': False,
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
    scorecard['list_429_backfilled'] = False
    scorecard['scout_n_copied_into_settled_join_n'] = False
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
        'list_429_backfilled': False,
        'scout_n_copied_into_settled_join_n': False,
        'r3p3_fee_reopen': False,
        'c3_rj_reopen': False,
        'c5_rj_reopen': False,
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
