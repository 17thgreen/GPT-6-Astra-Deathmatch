"""NHL KXNHLGAME settled-resolution join harness.

Measurement only. One knob: join_gate. This module does not edit the
NHL-FQ lab, the C3-RJ lab, the C5-RJ lab, the R3P3-RJ lab, feebook,
rails, Cap-SR, or any FQ sibling. It does not place orders, does not
read Logan keys, does not run admit.py, and does not write scorecard
metrics.

The checkout freeze, scout reget, seed summary, panel stub, settled
reget, and accept match the attached sha256 values. The panel stub keeps
admitted_at null and result empty. The series settled/finalized/open
list stays the honest 429 gap. Lee-Ready is refused. Settled results,
depth, fills, and PnL are not invented. Scout settled_nonempty_result_N
is a pin and is not copied into settled_join_n.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PARENT = ROOT.parent

LAB_DIRECTORY = 'kalshi_kxnhlgame_settled_join_lab_20260923'
EXPERIMENT_ID = 'NHL-KXNHLGAME-SETTLED-RESOLUTION-JOIN-HARNESS'
FEATURE_FAMILY = 'NHL-RJ'
SCOUT_PACKET = 'NHL-KXNHLGAME-SETTLED-JOIN'
PARENT_PACKET_ID = 'C2-KXNHLGAME-FEEQUEUE-HARNESS'
PANEL_VERSION = '2026-09-23.c2-kxnhlgame-v0'
SCHEMA_ID = 'astra.panel_stub.v0'
SERIES = 'KXNHLGAME'
STUB_STATUS = 'NOT_ADMITTED'
KNOB = 'join_gate'
J0 = 'J0'
J1 = 'J1'
ARMS = (J0, J1)
JOIN_GATE = {
    J0: 'nonempty_result_required',
    J1: 'occurrence_datetime_match',
}
FINALIZED_RESULTS = ('yes', 'no')
SCOUT_NONEMPTY_N = 17
OVERNIGHT_N = 17
YES_N = 8
NO_N = 9
PARENT_SEED_N = 3
PARENT_FINALIZED_N = 0
REGET_ACTIVE_EMPTY_N = 4
PANEL_EVENTS_N = 6
PANEL_MARKETS_N = 12
PANEL_ABSENT_N = 8
SOURCE_MARKETS_N = 66
SOURCE_EVENTS_N = 33
ROW_LABEL_N = 23
ONE_SIDED_N = 3
SETTLED_LIST_LIMIT = 20
METHOD = 'GET-only single-market (list status=settled|finalized|open 429 honest)'
PARENT_NOTE = (
    'FQ parent panel SEP26 seeds still active/empty result (honest; future occ). '
    'Settled join uses overnight SEP22 finalized cohort from prior FQ hunt seed tickers.'
)
REGET_NOTE = 'Authentic GET-only. No invent. List endpoints 429 recorded honest.'
LIST_429 = '429_honest'
GAP_MARKETS = 'GET /markets?series_ticker=KXNHLGAME&status=settled|finalized|open list 429'
GAP_EVENTS = 'GET /events?series_ticker=KXNHLGAME&status=settled list 429'
PARENT_EMPTY_GAP = 'FQ parent SEP26 panel seeds active/empty (not yet settled)'
GAP_KEYS = (GAP_MARKETS, GAP_EVENTS)
HONEST_GAPS = (GAP_MARKETS, GAP_EVENTS, PARENT_EMPTY_GAP)
PANEL_RULES = (
    'measurement_only',
    'GET_only',
    'no_Logan_keys',
    'no_invent_depth_fills_pnl',
    'results_pnl_null',
    'does_not_ungate_S1_S2',
)
EVENT_TICKERS = (
    'KXNHLGAME-26SEP26TBFLA',
    'KXNHLGAME-26SEP26COLUTA',
    'KXNHLGAME-26SEP26WSHPHI',
    'KXNHLGAME-26SEP26ANALA',
    'KXNHLGAME-26SEP26CARNSH',
    'KXNHLGAME-26SEP26PITBUF',
)
PANEL_TICKERS = (
    'KXNHLGAME-26SEP26TBFLA-TB',
    'KXNHLGAME-26SEP26TBFLA-FLA',
    'KXNHLGAME-26SEP26COLUTA-UTA',
    'KXNHLGAME-26SEP26COLUTA-COL',
    'KXNHLGAME-26SEP26WSHPHI-WSH',
    'KXNHLGAME-26SEP26WSHPHI-PHI',
    'KXNHLGAME-26SEP26ANALA-LA',
    'KXNHLGAME-26SEP26ANALA-ANA',
    'KXNHLGAME-26SEP26CARNSH-NSH',
    'KXNHLGAME-26SEP26CARNSH-CAR',
    'KXNHLGAME-26SEP26PITBUF-PIT',
    'KXNHLGAME-26SEP26PITBUF-BUF',
)
PARENT_SEED_TICKERS = (
    'KXNHLGAME-26SEP26TBFLA-TB',
    'KXNHLGAME-26SEP26TBFLA-FLA',
    'KXNHLGAME-26SEP26COLUTA-UTA',
)
PARENT_SEED_RESULTS = {
    'KXNHLGAME-26SEP26TBFLA-TB': None,
    'KXNHLGAME-26SEP26TBFLA-FLA': None,
    'KXNHLGAME-26SEP26COLUTA-UTA': None,
}
PARENT_SEED_STATUSES = {
    'KXNHLGAME-26SEP26TBFLA-TB': 'active',
    'KXNHLGAME-26SEP26TBFLA-FLA': 'active',
    'KXNHLGAME-26SEP26COLUTA-UTA': 'active',
}
REGET_ACTIVE_EMPTY_TICKERS = (
    'KXNHLGAME-26SEP26COLUTA-UTA',
    'KXNHLGAME-26SEP26TBFLA-FLA',
    'KXNHLGAME-26SEP26TBFLA-TB',
    'KXNHLGAME-26SEP26WSHPHI-WSH',
)
PANEL_ABSENT_FROM_REGET = (
    'KXNHLGAME-26SEP26COLUTA-COL',
    'KXNHLGAME-26SEP26WSHPHI-PHI',
    'KXNHLGAME-26SEP26ANALA-LA',
    'KXNHLGAME-26SEP26ANALA-ANA',
    'KXNHLGAME-26SEP26CARNSH-NSH',
    'KXNHLGAME-26SEP26CARNSH-CAR',
    'KXNHLGAME-26SEP26PITBUF-PIT',
    'KXNHLGAME-26SEP26PITBUF-BUF',
)
OVERNIGHT_TICKERS = (
    'KXNHLGAME-26SEP22CBJBUF-BUF',
    'KXNHLGAME-26SEP22CBJBUF-CBJ',
    'KXNHLGAME-26SEP22DETPIT-DET',
    'KXNHLGAME-26SEP22DETPIT-PIT',
    'KXNHLGAME-26SEP22EDMWPG-EDM',
    'KXNHLGAME-26SEP22EDMWPG-WPG',
    'KXNHLGAME-26SEP22FLACAR-CAR',
    'KXNHLGAME-26SEP22FLACAR-FLA',
    'KXNHLGAME-26SEP22NYINYR-NYI',
    'KXNHLGAME-26SEP22NYINYR-NYR',
    'KXNHLGAME-26SEP22PHIBOS-BOS',
    'KXNHLGAME-26SEP22PHIBOS-PHI',
    'KXNHLGAME-26SEP22TBNSH-TB',
    'KXNHLGAME-26SEP22UTALA-LA',
    'KXNHLGAME-26SEP22VANCGY-CGY',
    'KXNHLGAME-26SEP22VANCGY-VAN',
    'KXNHLGAME-26SEP22VGKSJ-VGK',
)
OVERNIGHT_RESULTS = {
    'KXNHLGAME-26SEP22CBJBUF-BUF': 'yes',
    'KXNHLGAME-26SEP22CBJBUF-CBJ': 'no',
    'KXNHLGAME-26SEP22DETPIT-DET': 'yes',
    'KXNHLGAME-26SEP22DETPIT-PIT': 'no',
    'KXNHLGAME-26SEP22EDMWPG-EDM': 'yes',
    'KXNHLGAME-26SEP22EDMWPG-WPG': 'no',
    'KXNHLGAME-26SEP22FLACAR-CAR': 'yes',
    'KXNHLGAME-26SEP22FLACAR-FLA': 'no',
    'KXNHLGAME-26SEP22NYINYR-NYI': 'yes',
    'KXNHLGAME-26SEP22NYINYR-NYR': 'no',
    'KXNHLGAME-26SEP22PHIBOS-BOS': 'yes',
    'KXNHLGAME-26SEP22PHIBOS-PHI': 'no',
    'KXNHLGAME-26SEP22TBNSH-TB': 'no',
    'KXNHLGAME-26SEP22UTALA-LA': 'no',
    'KXNHLGAME-26SEP22VANCGY-CGY': 'yes',
    'KXNHLGAME-26SEP22VANCGY-VAN': 'no',
    'KXNHLGAME-26SEP22VGKSJ-VGK': 'yes',
}
ONE_SIDED_EVENTS = (
    'KXNHLGAME-26SEP22TBNSH',
    'KXNHLGAME-26SEP22UTALA',
    'KXNHLGAME-26SEP22VGKSJ',
)
FEEBOOK_COMMIT = '22371178cb2663250b4762f328069571c48cb551'
RAILS_COMMIT = '6a28e0d6254327ea4e6451c781bec56215ac6cac'
BASE_COMMIT = '2fce8642d1b1961cbe0ef60fae1411cd8906f31a'
FREEZE_SHA256 = 'd1f71cea6df8f6c5a9fac6f9d1aa418ce61aa650794f22b400a01c4f3fd45810'
SCOUT_SHA256 = '99a7f90564ee2150f5edef4efafb7ccb954b87036e0b43f29ff7dc6ed104706f'
SEED_SHA256 = '794e148df5927c64d08b4578b47a7453589f02872af65880922bcb9273194a1a'
PANEL_STUB_SHA256 = '60d183e7bdcf25adbc94eeeb3bb361b5232c19c0fe3e6a115f45ab3fcb100c79'
REGET_SHA256 = '8d597578bc65ea14ab1cbf5aa3c6d121d61431078a755b8419c815aa1d354df0'
ACCEPT_SHA256 = 'cee2705a620ef9aef8316fa8629d6c025e7ac8489022bc35559994736be63eaf'
FROZEN_SHA256 = 'a882ab8e410b6b5a77b60aa0225dcb932c0a1b0b3bcc692a02a5cfa23b81bd42'
EMPTY_SHA256 = 'cc28e226979959d417ea1b7c6a05c87e6776e96489d57f793249bc42f912934f'
SOURCE_PINS_SHA256 = 'fa314d759d39f1700639024132c800d38824a05c83cc210fa7a4f1f84ebbcc69'
SCOUT_HUNT_SHA256 = '1ab794ad688ba31e0178e78294dcdbe50cf2799a71f40245e5a04a80e9dd5762'
FREEZE_BYTES = 5421
SCOUT_BYTES = 6307
SEED_BYTES = 6066
PANEL_BYTES = 29517
REGET_BYTES = 6922
ACCEPT_BYTES = 1693
FROZEN_BYTES = 1042
EMPTY_BYTES = 181
SOURCE_PINS_BYTES = 5286
ACCEPT_STAMPED_AT = '2026-09-23T16:14:00-04:00'
FROZEN_STAMPED_AT = '2026-09-23T15:56:00-04:00'
SCOUT_FETCHED_AT = '2026-09-23T15:56:00-04:00'
PANEL_STUBBED_AT = '2026-09-23T13:36:00-04:00'
EMPTY_NOTE = 'pre-ACCEPT empty; NHL-RJ measurement join only'
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
    'R3P3_RJ_reopen',
    'NHL_FQ_reopen',
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
    'list_429_backfill': 'series settled finalized open list 429 backfill is refused',
    'parent_seed_invent': 'invented SEP26 parent settle is refused',
    'missing_side_invent': 'invented one-sided market is refused',
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
    'r3p3_rj_reopen': 'R3P3-RJ reopen is refused',
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
    'kalshi_r3p3_fl_settled_join_lab_20260923',
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
    'packets/C2_KXNHLGAME_FEEQUEUE_HARNESS',
    'packets/C2_KXNHLGAME_PANEL_STUB_2026-09-23.json',
    'lab/astra-capture/c2-kxnhlgame/panel_stub.json',
    'lab/governance/astra/packets/r3_p2_queue_position/results/demo_queue_sample_series.json',
)
FREEZE_NAME = 'NHL_KXNHLGAME_SETTLED_RESOLUTION_JOIN_HARNESS_FREEZE_2026-09-23.md'
SCOUT_NAME = 'scout_settled_rejoin_NHL_KXNHLGAME.json'
SEED_NAME = 'SEED_SETTLED_SUMMARY.json'
PANEL_ALIAS = 'C2_KXNHLGAME_PANEL_STUB_2026-09-23.json'
REGET_NAME = 'settled_reget_2026-09-23.json'
ACCEPT_NAME = 'CONDUCTOR_ACCEPT_NHL_KXNHLGAME_SETTLED_JOIN_HARNESS_2026-09-23.json'
SOURCE_PINS_NAME = 'SOURCE_PINS.json'
LAB_BUNDLE = ROOT / 'NHL_KXNHLGAME_SETTLED_RESOLUTION_JOIN_HARNESS'
GOVERNANCE_TREE = PARENT / 'lab' / 'governance' / 'astra'
NHL_SCOUT_CITE = GOVERNANCE_TREE / 'packets' / 'scout_nhl_settled_rejoin_2026-09-23'
NHL_PANEL_CITE = GOVERNANCE_TREE / 'packets' / 'C2_KXNHLGAME_PANEL_STUB_2026-09-23.json'
PACKET = ROOT / FREEZE_NAME
SCOUT_PATH = ROOT / SCOUT_NAME
SEED_PATH = ROOT / SEED_NAME
REGET_PATH = ROOT / REGET_NAME
CONDUCTOR_ACCEPT = ROOT / ACCEPT_NAME
FROZEN_EXPERIMENT = ROOT / 'FROZEN_EXPERIMENT.json'
EMPTY_RESULTS = ROOT / 'results' / 'EMPTY_RESULTS.json'
SOURCE_PINS = ROOT / SOURCE_PINS_NAME
PANEL_CAPTURE = PARENT / 'lab' / 'astra-capture' / 'c2-kxnhlgame' / 'panel_stub.json'
PANEL_ADMITTED = PARENT / 'lab' / 'astra-capture' / 'c2-kxnhlgame' / 'panel_admitted.json'
REGET_CITE = PARENT / 'lab' / 'astra-capture' / 'c2-kxnhlgame' / REGET_NAME
ADMIT_PY = ROOT / 'admit.py'
COMPARE_FIELDS = ('status', 'result', 'occurrence_datetime', 'close_time')
EMPTY_RESULT = ''


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
    """The panel file is not the pinned C2 seed."""

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
    """The series list 429 gaps stay gaps. Nothing is written."""
    del which, result, occurrence_datetime
    raise InventedResultRefused()


def invent_parent_settle(ticker=None, result=None):
    """SEP26 parent seeds stay active with an empty result."""
    del ticker, result
    raise InventedResultRefused()


def invent_missing_side(event_ticker=None, ticker=None, result=None):
    """A one-sided overnight event stays one-sided."""
    del event_ticker, ticker, result
    raise InventedMarketRefused()


def invent_open_ticker(ticker=None, result=None):
    """Panel markets absent from the reget are not settled-join markets."""
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
    if label in ('invent_settled_result', 'invented_result', 'list_429_backfill', 'parent_seed_invent'):
        raise InventedResultRefused()
    if label in ('invent_fills', 'invented_fills'):
        raise InventedFillRefused()
    if label == 'invented_depth':
        raise InventedDepthRefused()
    if label in ('open_ticker_invent', 'missing_side_invent'):
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


def _empty_result(value):
    return value in (None, EMPTY_RESULT)


def _zulu(value):
    return isinstance(value, str) and value.endswith('Z')


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
    if payload.get('overnight_finalized_nonempty_N') != OVERNIGHT_N:
        raise OrchestratorError('source pins')
    if payload.get('scout_n_copied_into_settled_join_n') is not False:
        raise ScorecardPromotionRefused()
    if payload.get('parent_seed_tickers') != list(PARENT_SEED_TICKERS):
        raise OrchestratorError('source pins')
    if payload.get('parent_seeds_finalized_nonempty_N') != PARENT_FINALIZED_N:
        raise OrchestratorError('source pins')
    if payload.get('parent_seed_results') != PARENT_SEED_RESULTS:
        raise InventedResultRefused()
    if payload.get('parent_seed_statuses') != PARENT_SEED_STATUSES:
        raise InventedResultRefused()
    if payload.get('parent_panel_result') != EMPTY_RESULT:
        raise InventedResultRefused()
    if payload.get('reget_active_empty_tickers') != list(REGET_ACTIVE_EMPTY_TICKERS):
        raise OrchestratorError('source pins')
    if payload.get('reget_active_empty_result') != EMPTY_RESULT:
        raise InventedResultRefused()
    if payload.get('panel_markets_absent_from_reget') != list(PANEL_ABSENT_FROM_REGET):
        raise InventedMarketRefused()
    if payload.get('series_list_settled_finalized_open_429') != LIST_429:
        raise OrchestratorError('source pins')
    if payload.get('list_429_backfilled') is not False:
        raise InventedResultRefused()
    if payload.get('honest_gaps') != list(HONEST_GAPS):
        raise InventedResultRefused()
    if payload.get('one_sided_event_tickers') != list(ONE_SIDED_EVENTS):
        raise InventedMarketRefused()
    if payload.get('missing_side_invented') is not False:
        raise InventedMarketRefused()
    if payload.get('fee_import_used') is not False or payload.get('rails_import_used') is not False:
        raise OrchestratorError('source pins')
    if payload.get('fee_arms') is not False:
        raise OrchestratorError('source pins')
    if payload.get('feebook_commit_fixed_not_loaded') != FEEBOOK_COMMIT:
        raise OrchestratorError('source pins')
    if payload.get('rails_commit_fixed_not_loaded') != RAILS_COMMIT:
        raise OrchestratorError('source pins')
    if payload.get('governance_nhl_cites') != 'absent':
        raise OrchestratorError('source pins')
    if payload.get('does_not_run_admit_py') is not True:
        raise AdmitPyRefused()
    if payload.get('base_commit') != BASE_COMMIT:
        raise OrchestratorError('source pins')
    if payload.get('lee_ready') != 'REFUSED':
        raise LeeReadyRefused()
    if payload.get('nhl_fq_reopen') is not False or payload.get('c3_rj_reopen') is not False:
        raise OrchestratorError('source pins')
    if payload.get('c5_rj_reopen') is not False or payload.get('r3p3_rj_reopen') is not False:
        raise OrchestratorError('source pins')
    if payload.get('cap_sr_reopen') is not False or payload.get('fq_reopen') is not False:
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


def _validate_scout_markets(markets):
    if not isinstance(markets, list) or len(markets) != OVERNIGHT_N:
        raise OrchestratorError('scout markets')
    seen = []
    for row in markets:
        if not isinstance(row, dict):
            raise OrchestratorError('scout market')
        ticker = row.get('ticker')
        if ticker not in OVERNIGHT_RESULTS or ticker in seen:
            raise InventedMarketRefused()
        if row.get('nonempty_result') is not True:
            raise InventedResultRefused()
        if row.get('status') != 'finalized' or row.get('result') != OVERNIGHT_RESULTS[ticker]:
            raise InventedResultRefused()
        if not _zulu(row.get('occurrence_datetime')) or not _zulu(row.get('close_time')):
            raise OccurrenceIntegrityRefused()
        source = row.get('source')
        if not isinstance(source, str) or not source.endswith('.json'):
            raise OrchestratorError('scout source')
        if ticker in PARENT_SEED_TICKERS or ticker in PANEL_TICKERS:
            raise InventedMarketRefused()
        seen.append(ticker)
    if tuple(seen) != OVERNIGHT_TICKERS:
        raise InventedMarketRefused()
    return markets


def _validate_scout(payload):
    if payload.get('packet') != SCOUT_PACKET or payload.get('feature_family') != FEATURE_FAMILY:
        raise OrchestratorError('scout')
    if payload.get('series') != [SERIES]:
        raise OrchestratorError('scout')
    if payload.get('settled_nonempty_result_N') != SCOUT_NONEMPTY_N:
        raise OrchestratorError('scout N')
    if payload.get('settled_list_limit') != SETTLED_LIST_LIMIT:
        raise OrchestratorError('scout N')
    if payload.get('settled_list_http') != LIST_429 or payload.get('open_list_http') != LIST_429:
        raise InventedResultRefused()
    if payload.get('settled_list_cursor_present') is not False:
        raise InventedResultRefused()
    if payload.get('open_list_n') is not None:
        raise InventedMarketRefused()
    if payload.get('method') != METHOD:
        raise OrchestratorError('scout mode')
    if payload.get('host') != PUBLIC_HOST:
        raise OrchestratorError('scout host')
    if payload.get('parent_seeds_finalized_nonempty_N') != PARENT_FINALIZED_N:
        raise OrchestratorError('scout')
    if payload.get('parent_seed_tickers') != list(PARENT_SEED_TICKERS):
        raise OrchestratorError('scout')
    if payload.get('parent_seed_results') != PARENT_SEED_RESULTS:
        raise InventedResultRefused()
    if payload.get('parent_seed_statuses') != PARENT_SEED_STATUSES:
        raise InventedResultRefused()
    if payload.get('parent_panel_seeds_note') != PARENT_NOTE:
        raise OrchestratorError('scout')
    if payload.get('occurrence_datetime_sot_match_all_settled_seeds') is not True:
        raise OccurrenceIntegrityRefused()
    if payload.get('scouted_at_et') != SCOUT_FETCHED_AT:
        raise OrchestratorError('scout')
    if payload.get('results') is not None or payload.get('pnl') is not None:
        raise ScorecardPromotionRefused()
    _validate_scout_markets(payload.get('markets'))
    return payload


def _validate_seed(payload, scout):
    if payload.get('settled_nonempty_result_N') != SCOUT_NONEMPTY_N:
        raise OrchestratorError('seed N')
    if payload.get('overnight_finalized_nonempty_N') != OVERNIGHT_N:
        raise OrchestratorError('seed N')
    if payload.get('settled_list_attempted_KXNHLGAME') != LIST_429:
        raise InventedResultRefused()
    if payload.get('method') != METHOD:
        raise OrchestratorError('seed')
    if payload.get('parent_seed_tickers') != list(PARENT_SEED_TICKERS):
        raise OrchestratorError('seed ticker')
    if payload.get('parent_seeds_finalized_nonempty_N') != PARENT_FINALIZED_N:
        raise OrchestratorError('seed')
    if payload.get('parent_seed_results') != PARENT_SEED_RESULTS:
        raise InventedResultRefused()
    if payload.get('parent_seed_statuses') != PARENT_SEED_STATUSES:
        raise InventedResultRefused()
    if payload.get('occurrence_datetime_match_all_settled_seeds') is not True:
        raise OccurrenceIntegrityRefused()
    if payload.get('honest_gaps') != list(HONEST_GAPS):
        raise InventedResultRefused()
    if payload.get('markets') != scout.get('markets'):
        raise OrchestratorError('seed scout markets')
    if payload.get('results') is not None or payload.get('pnl') is not None:
        raise ScorecardPromotionRefused()
    return payload


def _validate_reget_row(row, ticker, finalized):
    if not isinstance(row, dict) or row.get('ticker') != ticker:
        raise InventedMarketRefused()
    event = row.get('event_ticker')
    if not isinstance(event, str) or not ticker.startswith(event + '-'):
        raise InventedMarketRefused()
    source = row.get('file')
    if not isinstance(source, str) or not source.endswith('.json'):
        raise OrchestratorError('reget file')
    if 'orderbook_fp' in row:
        raise InventedDepthRefused()
    if finalized:
        if row.get('status') != 'finalized' or row.get('result') != OVERNIGHT_RESULTS[ticker]:
            raise InventedResultRefused()
    else:
        if row.get('status') != 'active' or row.get('result') != EMPTY_RESULT:
            raise InventedResultRefused()
    if not _zulu(row.get('occurrence_datetime')) or not _zulu(row.get('close_time')):
        raise OccurrenceIntegrityRefused()
    return row


def _validate_reget(payload, scout):
    if payload.get('series') != SERIES or payload.get('feature_family') != FEATURE_FAMILY:
        raise OrchestratorError('reget')
    if payload.get('host') != PUBLIC_HOST:
        raise OrchestratorError('reget host')
    if payload.get('fetched_at_et') != SCOUT_FETCHED_AT:
        raise OrchestratorError('reget')
    if payload.get('settled_nonempty_result_N') != SCOUT_NONEMPTY_N:
        raise OrchestratorError('reget N')
    if payload.get('settled_list_http') != LIST_429:
        raise InventedResultRefused()
    if payload.get('note') != REGET_NOTE:
        raise OrchestratorError('reget')
    if 'artifacts' in payload or 'http_log' in payload or 'markets' in payload:
        raise InventedResultRefused()
    if payload.get('results') is not None or payload.get('pnl') is not None:
        raise ScorecardPromotionRefused()
    rows = payload.get('markets_nonempty')
    if not isinstance(rows, list) or len(rows) != OVERNIGHT_N:
        raise OrchestratorError('reget markets')
    scout_rows = {}
    for row in scout.get('markets') or []:
        scout_rows[row['ticker']] = row
    settled = {}
    event_counts = {}
    yes_n = 0
    no_n = 0
    for expected, row in zip(OVERNIGHT_TICKERS, rows):
        checked = _validate_reget_row(row, expected, True)
        scout_row = scout_rows[expected]
        if checked.get('file') != scout_row.get('source'):
            raise OrchestratorError('scout reget file')
        for field in COMPARE_FIELDS:
            if checked.get(field) != scout_row.get(field):
                raise OrchestratorError('scout reget ' + field)
        settled[expected] = checked
        event = checked['event_ticker']
        event_counts[event] = event_counts.get(event, 0) + 1
        if checked.get('result') == 'yes':
            yes_n += 1
        else:
            no_n += 1
    if yes_n != YES_N or no_n != NO_N:
        raise OrchestratorError('reget census')
    one_sided = tuple(event for event, count in event_counts.items() if count == 1)
    if one_sided != ONE_SIDED_EVENTS:
        raise InventedMarketRefused()
    if any(count not in (1, 2) for count in event_counts.values()):
        raise InventedMarketRefused()
    active_rows = payload.get('parent_seeds_active_empty')
    if not isinstance(active_rows, list) or len(active_rows) != REGET_ACTIVE_EMPTY_N:
        raise OrchestratorError('reget active')
    active = {}
    for expected, row in zip(REGET_ACTIVE_EMPTY_TICKERS, active_rows):
        active[expected] = _validate_reget_row(row, expected, False)
    if set(active) & set(settled):
        raise InventedMarketRefused()
    if not set(PARENT_SEED_TICKERS) <= set(active):
        raise OrchestratorError('reget active')
    for ticker in PANEL_ABSENT_FROM_REGET:
        if ticker in settled or ticker in active:
            raise InventedMarketRefused()
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
    if payload.get('scout_sha256') != SCOUT_HUNT_SHA256:
        raise OrchestratorError('scout hunt')
    if payload.get('rules') != list(PANEL_RULES):
        raise OrchestratorError('rules')
    if payload.get('stubbed_at_et') != PANEL_STUBBED_AT:
        raise OrchestratorError('panel')
    if 'trades_sample' in payload:
        raise InventedFillRefused()
    for key in ('results', 'pnl'):
        if key not in payload or payload[key] is not None:
            raise ScorecardPromotionRefused()
    counts = payload.get('cohort_summary') or {}
    if counts.get('events_n') != PANEL_EVENTS_N or counts.get('markets_n') != PANEL_MARKETS_N:
        raise OrchestratorError('cohort')
    if counts.get('source_markets_n') != SOURCE_MARKETS_N or counts.get('source_events_n') != SOURCE_EVENTS_N:
        raise OrchestratorError('cohort')
    events = payload.get('events')
    markets = payload.get('markets')
    if not isinstance(events, list) or len(events) != PANEL_EVENTS_N:
        raise OrchestratorError('events')
    if not isinstance(markets, list) or len(markets) != PANEL_MARKETS_N:
        raise OrchestratorError('markets')
    event_tickers = []
    event_occ = {}
    for event in events:
        if not isinstance(event, dict):
            raise OrchestratorError('events')
        if event.get('admitted_at') is not None:
            raise OrchestratorError('admitted_at')
        name = event.get('event_ticker')
        if event.get('markets_n') != 2 or not _zulu(event.get('occurrence_datetime')):
            raise OccurrenceIntegrityRefused()
        event_tickers.append(name)
        event_occ[name] = event.get('occurrence_datetime')
    if tuple(event_tickers) != EVENT_TICKERS:
        raise OrchestratorError('events')
    seen = []
    per_event = {}
    for market in markets:
        if not isinstance(market, dict):
            raise OrchestratorError('market')
        if market.get('admitted_at') is not None:
            raise OrchestratorError('admitted_at')
        if market.get('result') != EMPTY_RESULT or market.get('status') != 'active':
            raise InventedResultRefused()
        if 'orderbook_fp' in market:
            raise InventedDepthRefused()
        ticker = market.get('ticker')
        event = market.get('event_ticker')
        if event not in event_occ or not isinstance(ticker, str) or not ticker.startswith(event + '-'):
            raise InventedMarketRefused()
        if market.get('occurrence_datetime') != event_occ[event]:
            raise OccurrenceIntegrityRefused()
        if not _zulu(market.get('close_time')):
            raise OccurrenceIntegrityRefused()
        seen.append(ticker)
        per_event[event] = per_event.get(event, 0) + 1
    if tuple(seen) != PANEL_TICKERS:
        raise InventedMarketRefused()
    if any(count != 2 for count in per_event.values()) or len(per_event) != PANEL_EVENTS_N:
        raise OrchestratorError('events')
    if set(OVERNIGHT_TICKERS) & set(seen):
        raise InventedResultRefused()
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
    if NHL_SCOUT_CITE.exists():
        raise OrchestratorError('governance cite')
    if NHL_PANEL_CITE.exists():
        _assert_digest(NHL_PANEL_CITE, PANEL_STUB_SHA256, PANEL_BYTES)
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
    cites_present = NHL_SCOUT_CITE.exists() or NHL_PANEL_CITE.is_file()
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
        'governance_nhl_cites_present': cites_present,
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
    markets = {}
    for row in checked['markets_nonempty']:
        markets[row['ticker']] = row
    active = {}
    for row in checked['parent_seeds_active_empty']:
        active[row['ticker']] = row
    view = dict(checked)
    view['markets'] = markets
    view['active_empty'] = active
    view['honest_gaps'] = {
        GAP_MARKETS: LIST_429,
        GAP_EVENTS: LIST_429,
    }
    return view


def load_reget():
    scout = load_scout()
    payload = _read_pinned(REGET_PATH, REGET_SHA256, REGET_BYTES)
    return _settled_view(payload, scout)


def list_429_gaps(reget=None):
    """Series settled/finalized/open and events settled lists. No ticker is attached."""
    if reget is None:
        reget = load_reget()
    gaps = reget.get('honest_gaps')
    if gaps != {GAP_MARKETS: LIST_429, GAP_EVENTS: LIST_429}:
        raise InventedResultRefused()
    if reget.get('settled_list_http') != LIST_429:
        raise InventedResultRefused()
    markets = reget.get('markets') or {}
    active = reget.get('active_empty') or {}
    for key in GAP_KEYS:
        if key in markets or key in active:
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
    if any(not _zulu(value) for value in values):
        raise OccurrenceIntegrityRefused()
    if values[0] != values[1]:
        raise OccurrenceIntegrityRefused()
    return values[0]


def occurrence_agreement_tickers(panel=None):
    """Overnight rows whose scout, seed, and reget timestamps agree.

    Parent SEP26 seeds are checked against the panel and stay out of this
    tuple. The 429 gaps and the panel markets absent from the reget are
    absent. This list is not occurrence_match_n.
    """
    if panel is None:
        panel = load_panel()
    else:
        _validate_panel(panel)
    reget = load_reget()
    settled = reget['markets']
    active = reget['active_empty']
    seed_rows = {row['ticker']: row for row in load_seed()['markets']}
    if set(settled) != set(OVERNIGHT_TICKERS) or set(seed_rows) != set(OVERNIGHT_TICKERS):
        raise InventedMarketRefused()
    agreed = []
    for ticker in OVERNIGHT_TICKERS:
        market = settled[ticker]
        assert_occurrence_pair(market, seed_rows[ticker])
        if market.get('close_time') != seed_rows[ticker].get('close_time'):
            raise OccurrenceIntegrityRefused()
        agreed.append(ticker)
    panel_by = {market.get('ticker'): market for market in panel.get('markets') or []}
    if set(panel_by) != set(PANEL_TICKERS):
        raise InventedMarketRefused()
    for ticker, market in active.items():
        panel_market = panel_by[ticker]
        if panel_market.get('occurrence_datetime') != market.get('occurrence_datetime'):
            raise OccurrenceIntegrityRefused()
        if panel_market.get('close_time') != market.get('close_time'):
            raise OccurrenceIntegrityRefused()
        if panel_market.get('result') != EMPTY_RESULT or market.get('result') != EMPTY_RESULT:
            raise InventedResultRefused()
    for ticker in PANEL_ABSENT_FROM_REGET:
        if ticker in settled or ticker in active:
            raise InventedMarketRefused()
        if panel_by[ticker].get('result') != EMPTY_RESULT:
            raise InventedResultRefused()
    if any(ticker in agreed for ticker in PARENT_SEED_TICKERS):
        raise InventedMarketRefused()
    if len(agreed) != OVERNIGHT_N:
        raise OrchestratorError('occurrence rows')
    return tuple(agreed)


def structural_rows(panel=None):
    """Label authentic reget rows. Does not write scorecard counts."""
    if panel is None:
        panel = load_panel()
    else:
        _validate_panel(panel)
    list_429_gaps()
    agreed = occurrence_agreement_tickers(panel)
    reget = load_reget()
    settled = reget['markets']
    active = reget['active_empty']
    if tuple(agreed) != OVERNIGHT_TICKERS:
        raise OccurrenceIntegrityRefused()
    rows = []
    for ticker in OVERNIGHT_TICKERS:
        market = settled[ticker]
        result = market.get('result')
        if market.get('status') != 'finalized' or result not in FINALIZED_RESULTS:
            raise InventedResultRefused()
        rows.append({
            'key': ticker,
            'panel_ticker': None,
            'j0': 'nonempty_result_required_pass',
            'j1': 'occurrence_datetime_match',
            'result': result,
            'on_settled_list': False,
            'parent_seed': False,
            'single_market_get': True,
        })
    for ticker in REGET_ACTIVE_EMPTY_TICKERS:
        market = active[ticker]
        if market.get('status') != 'active' or market.get('result') != EMPTY_RESULT:
            raise InventedResultRefused()
        rows.append({
            'key': ticker,
            'panel_ticker': ticker,
            'j0': 'active_empty_honest',
            'j1': 'parent_active_empty',
            'result': EMPTY_RESULT,
            'on_settled_list': False,
            'parent_seed': ticker in PARENT_SEED_TICKERS,
            'single_market_get': True,
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
            'single_market_get': False,
        })
    if len(rows) != ROW_LABEL_N:
        raise OrchestratorError('row labels')
    passes = [row for row in rows if row['j0'] == 'nonempty_result_required_pass']
    empties = [row for row in rows if row['j0'] == 'active_empty_honest']
    gaps = [row for row in rows if row['j0'] == 'honest_429_gap']
    if len(passes) != OVERNIGHT_N or len(empties) != REGET_ACTIVE_EMPTY_N or len(gaps) != len(GAP_KEYS):
        raise OrchestratorError('row labels')
    if any(row['on_settled_list'] or row['parent_seed'] for row in passes):
        raise OrchestratorError('row labels')
    if sum(1 for row in passes if row['result'] == 'yes') != YES_N:
        raise OrchestratorError('row labels')
    if sum(1 for row in passes if row['result'] == 'no') != NO_N:
        raise OrchestratorError('row labels')
    parent_rows = [row for row in empties if row['parent_seed']]
    if len(parent_rows) != PARENT_SEED_N:
        raise OrchestratorError('row labels')
    if {row['key'] for row in parent_rows} != set(PARENT_SEED_TICKERS):
        raise OrchestratorError('row labels')
    if any(row['result'] != EMPTY_RESULT for row in empties):
        raise InventedResultRefused()
    for ticker in PANEL_ABSENT_FROM_REGET:
        if ticker in {row['key'] for row in rows}:
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
    if pins['governance_nhl_cites_present'] is not False:
        raise OrchestratorError('governance cite')
    rows = structural_rows(panel)
    agreed = occurrence_agreement_tickers(panel)
    if len(agreed) != OVERNIGHT_N:
        raise OrchestratorError('occurrence rows')
    if any(ticker in agreed for ticker in PARENT_SEED_TICKERS):
        raise InventedMarketRefused()
    panel_results = [market.get('result') for market in panel.get('markets') or []]
    if panel_results != [EMPTY_RESULT] * PANEL_MARKETS_N:
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
        'overnight_finalized_nonempty_N': OVERNIGHT_N,
        'scout_n_copied_into_settled_join_n': False,
        'parent_seed_tickers': list(PARENT_SEED_TICKERS),
        'parent_seeds_finalized_nonempty_N': PARENT_FINALIZED_N,
        'parent_seed_results': dict(PARENT_SEED_RESULTS),
        'parent_seed_statuses': dict(PARENT_SEED_STATUSES),
        'parent_panel_result': EMPTY_RESULT,
        'reget_active_empty_tickers': list(REGET_ACTIVE_EMPTY_TICKERS),
        'reget_active_empty_result': EMPTY_RESULT,
        'panel_markets_absent_from_reget': list(PANEL_ABSENT_FROM_REGET),
        'one_sided_event_tickers': list(ONE_SIDED_EVENTS),
        'missing_side_invented': False,
        'series_list_settled_finalized_open_429': LIST_429,
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
        'nhl_fq_reopen': False,
        'empty_ob_reopen': False,
        'c3_rj_reopen': False,
        'c5_rj_reopen': False,
        'r3p3_rj_reopen': False,
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
        'governance_nhl_cites_present': False,
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
    scorecard['missing_side_invented'] = False
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
        'missing_side_invented': False,
        'nhl_fq_reopen': False,
        'c3_rj_reopen': False,
        'c5_rj_reopen': False,
        'r3p3_rj_reopen': False,
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
