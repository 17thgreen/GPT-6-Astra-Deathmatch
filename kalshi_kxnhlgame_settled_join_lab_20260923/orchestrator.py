"""NHL KXNHLGAME settled-resolution join harness.

Measurement only. One knob: join_gate. This module does not edit the
NHL-FQ lab, the C3-RJ lab, the C5-RJ lab, the R3P3-RJ lab, feebook,
rails, Cap-SR, or any FQ sibling. It does not place orders, does not
read Logan keys, does not run admit.py, and does not write scorecard
metrics.

The checkout freeze, scout reget, seed summary, panel stub, settled
reget, and accept match the attached sha256 values. The panel stub keeps
admitted_at null and result empty. The series settled list and the
events settled list stay the honest 429 gaps. Parent SEP26 FQ seeds stay
active with an empty result. Lee-Ready is refused. Settled results,
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
YES_N = 8
NO_N = 9
PARENT_SEED_N = 3
PARENT_FINALIZED_N = 0
REGET_PARENT_N = 4
PANEL_EVENTS_N = 6
PANEL_MARKETS_N = 12
ROW_LABEL_N = 24
SETTLED_LIST_LIMIT = 20
SCOUT_HUNT_SHA256 = '1ab794ad688ba31e0178e78294dcdbe50cf2799a71f40245e5a04a80e9dd5762'
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
REGET_PARENT_TICKERS = (
    'KXNHLGAME-26SEP26COLUTA-UTA',
    'KXNHLGAME-26SEP26TBFLA-FLA',
    'KXNHLGAME-26SEP26TBFLA-TB',
    'KXNHLGAME-26SEP26WSHPHI-WSH',
)
PANEL_EVENT_TICKERS = (
    'KXNHLGAME-26SEP26TBFLA',
    'KXNHLGAME-26SEP26COLUTA',
    'KXNHLGAME-26SEP26WSHPHI',
    'KXNHLGAME-26SEP26ANALA',
    'KXNHLGAME-26SEP26CARNSH',
    'KXNHLGAME-26SEP26PITBUF',
)
PANEL_MARKET_TICKERS = (
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
HONEST_GAPS = (
    'GET /markets?series_ticker=KXNHLGAME&status=settled|finalized|open list 429',
    'GET /events?series_ticker=KXNHLGAME&status=settled list 429',
    'FQ parent SEP26 panel seeds active/empty (not yet settled)',
)
GAP_LIST = HONEST_GAPS[0]
GAP_EVENTS = HONEST_GAPS[1]
GAP_PARENT_NOTE = HONEST_GAPS[2]
LIST_429 = '429_honest'
SCOUT_METHOD = 'GET-only single-market (list status=settled|finalized|open 429 honest)'
REGET_NOTE = 'Authentic GET-only. No invent. List endpoints 429 recorded honest.'
PARENT_NOTE = (
    'FQ parent panel SEP26 seeds still active/empty result (honest; future occ). '
    'Settled join uses overnight SEP22 finalized cohort from prior FQ hunt seed tickers.'
)
PANEL_PURPOSE = 'GET-only NHL game ML fee+queue honesty harness seed from Scout hunt bytes'
COHORT_KIND = 'scout_hunt_subset'
SCOUT_CITE_PANEL = 'packets/scout_cashcow_hunt_2026-09-22/scout_hunt_KXNHLGAME.json'
PANEL_RULES = (
    'measurement_only',
    'GET_only',
    'no_Logan_keys',
    'no_invent_depth_fills_pnl',
    'results_pnl_null',
    'does_not_ungate_S1_S2',
)
COHORT_SUMMARY = {
    'events_n': PANEL_EVENTS_N,
    'markets_n': PANEL_MARKETS_N,
    'source_markets_n': 66,
    'source_events_n': 33,
}
STUBBED_AT = '2026-09-23T13:36:00-04:00'
FEEBOOK_COMMIT = '22371178cb2663250b4762f328069571c48cb551'
RAILS_COMMIT = '6a28e0d6254327ea4e6451c781bec56215ac6cac'
BASE_COMMIT = '2fce8642d1b1961cbe0ef60fae1411cd8906f31a'
FREEZE_SHA256 = 'd1f71cea6df8f6c5a9fac6f9d1aa418ce61aa650794f22b400a01c4f3fd45810'
SCOUT_SHA256 = '99a7f90564ee2150f5edef4efafb7ccb954b87036e0b43f29ff7dc6ed104706f'
SEED_SHA256 = '794e148df5927c64d08b4578b47a7453589f02872af65880922bcb9273194a1a'
PANEL_STUB_SHA256 = '60d183e7bdcf25adbc94eeeb3bb361b5232c19c0fe3e6a115f45ab3fcb100c79'
REGET_SHA256 = '8d597578bc65ea14ab1cbf5aa3c6d121d61431078a755b8419c815aa1d354df0'
ACCEPT_SHA256 = 'ce82d9347c8af6666d96fb5c63be7693f4672306639ce4ba2360ba231c01e698'
FROZEN_SHA256 = 'a882ab8e410b6b5a77b60aa0225dcb932c0a1b0b3bcc692a02a5cfa23b81bd42'
EMPTY_SHA256 = 'cc28e226979959d417ea1b7c6a05c87e6776e96489d57f793249bc42f912934f'
HOLD_SHA256 = '06fed86652d552820fd8336363c89e79b336ec0d7c3a2c406a45140eff3dbd59'
PIN_SHA256 = '222c5d6bc1d1758b224f4ddee92016093cecd883b07cf0f10bcd16ea418161ca'
DIGESTS_SHA256 = '53db62add001a4f9beb21922ed4002394bce037a34d4d7d6c3c85a8e4c5df104'
SOURCE_PINS_SHA256 = 'e1eb1f6504836ddfa1a0a79b0743d51a372895fe19c05b935c7eedc8fa770c3d'
FREEZE_BYTES = 5421
SCOUT_BYTES = 6307
SEED_BYTES = 6066
PANEL_BYTES = 29517
REGET_BYTES = 6922
ACCEPT_BYTES = 1836
FROZEN_BYTES = 1042
EMPTY_BYTES = 181
HOLD_BYTES = 1933
PIN_BYTES = 2431
DIGESTS_BYTES = 1096
SOURCE_PINS_BYTES = 5619
ACCEPT_STAMPED_AT = '2026-09-23T16:14:00-04:00'
FROZEN_STAMPED_AT = '2026-09-23T15:56:00-04:00'
SCOUT_FETCHED_AT = '2026-09-23T15:56:00-04:00'
HOLD_STAMPED_AT = '2026-09-23T15:56:00-04:00'
EMPTY_NOTE = 'pre-ACCEPT empty; NHL-RJ measurement join only'
PUBLIC_HOST = 'https://api.elections.kalshi.com/trade-api/v2'
OUT_OF_SCOPE_ROUTE = 'POST /portfolio/orders'
SCORECARD_FIELDS = (
    'settled_join_n',
    'occurrence_match_n',
    'admit_ready_flag',
)
OUTPUT_KEYS = SCORECARD_FIELDS + ('results', 'pnl')
HOLD_METRICS = (
    'results',
    'pnl',
    'settled_join_n',
    'occurrence_match_n',
    'admit_ready_flag',
)
ACCEPT_HARD_REFUSE = (
    'invent_settled_result',
    'invent_fills',
    'invent_depth',
    'Lee-Ready',
    'FQ_reopen',
    'NHL_FQ_reopen',
    'Cap-SR_reopen',
    'C3_RJ_reopen',
    'C5_RJ_reopen',
    'R3P3_RJ_reopen',
    'ungate_S1_S2_R2P4',
    'Arm_B_touch',
    'admit_py_by_Variants',
    'live_orders',
    'copy_scout_N_into_settled_join_n',
)
DOES_NOT_UNGATE = ('S1', 'S2', 'R2-P4')
COMPARE_FIELDS = ('status', 'result', 'occurrence_datetime', 'close_time')
ADVERSARY_LABELS = {
    'lee_ready': 'Lee-Ready is refused',
    'invent_settled_result': 'invented settled result is refused',
    'invented_result': 'invented settled result is refused',
    'invent_fills': 'invented fills are refused',
    'invented_fills': 'invented fills are refused',
    'invent_depth': 'invented depth is refused',
    'invented_depth': 'invented depth is refused',
    'invented_pnl': 'invented pnl is refused',
    'list_429_backfill': 'series settled list 429 backfill is refused',
    'parent_seed_invent': 'invented parent SEP26 settlement is refused',
    'fq_reopen': 'FQ reopen is refused',
    'nhl_fq_reopen': 'NHL-FQ reopen is refused',
    'cpi_fq_reopen': 'CPI-FQ reopen is refused',
    'atp_fq_reopen': 'ATP-FQ reopen is refused',
    'eth_fq_reopen': 'ETH-FQ reopen is refused',
    'cap_sr_reopen': 'Cap-SR reopen is refused',
    'empty_ob_reopen': 'EMPTY-OB reopen is refused',
    'c3_rj_reopen': 'C3-RJ reopen is refused',
    'c5_rj_reopen': 'C5-RJ reopen is refused',
    'r3p3_rj_reopen': 'R3P3-RJ reopen is refused',
    'arm_b': 'Arm B is refused',
    'q7_arm_b': 'Arm B is refused',
    'admit_py': 'admit.py is refused',
    'live_orders': 'live orders are refused',
    'logan_keys': 'Logan keys are refused',
    'ungate': 'S1 S2 R2-P4 stay gated',
    'copy_scout_n': 'scout N is not settled_join_n',
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
    'lab/astra-capture/c2-kxnhlgame/README.md',
    'lab/governance/astra/packets/r3_p2_queue_position/results/demo_queue_sample_series.json',
)
FREEZE_NAME = 'NHL_KXNHLGAME_SETTLED_RESOLUTION_JOIN_HARNESS_FREEZE_2026-09-23.md'
SCOUT_NAME = 'scout_settled_rejoin_NHL_KXNHLGAME.json'
SEED_NAME = 'SEED_SETTLED_SUMMARY.json'
PANEL_ALIAS = 'C2_KXNHLGAME_PANEL_STUB_2026-09-23.json'
REGET_NAME = 'settled_reget_2026-09-23.json'
ACCEPT_NAME = 'CONDUCTOR_ACCEPT_NHL_KXNHLGAME_SETTLED_JOIN_HARNESS_2026-09-23.json'
HOLD_NAME = 'EXAMINER_HOLD_NHL_KXNHLGAME_SETTLED_JOIN_HARNESS_PRE_PR_2026-09-23.json'
PIN_NAME = 'MAXIMIZE_PIN_2026-09-23_1556ET.md'
DIGESTS_NAME = 'DIGESTS.txt'
SOURCE_PINS_NAME = 'SOURCE_PINS.json'
LAB_BUNDLE = ROOT / 'NHL_KXNHLGAME_SETTLED_RESOLUTION_JOIN_HARNESS'
SCIENCE = PARENT / 'lab' / 'astra-science' / LAB_DIRECTORY
PACKET_DIR = PARENT / 'packets' / 'NHL_KXNHLGAME_SETTLED_JOIN_HARNESS'
GOV = PARENT / 'lab' / 'governance' / 'astra' / 'packets'
SCOUT_CITE_DIR = GOV / 'scout_nhl_settled_rejoin_2026-09-23'
FREEZE_GOV = GOV / FREEZE_NAME
PANEL_GOV = GOV / PANEL_ALIAS
PACKET = ROOT / FREEZE_NAME
SCOUT_PATH = ROOT / SCOUT_NAME
SEED_PATH = ROOT / SEED_NAME
REGET_PATH = ROOT / REGET_NAME
CONDUCTOR_ACCEPT = ROOT / ACCEPT_NAME
FROZEN_EXPERIMENT = ROOT / 'FROZEN_EXPERIMENT.json'
EMPTY_RESULTS = ROOT / 'results' / 'EMPTY_RESULTS.json'
EXAMINER_HOLD = ROOT / HOLD_NAME
MAXIMIZE_PIN = ROOT / PIN_NAME
DIGESTS_PATH = ROOT / DIGESTS_NAME
SOURCE_PINS = ROOT / SOURCE_PINS_NAME
PANEL_CAPTURE = PARENT / 'lab' / 'astra-capture' / 'c2-kxnhlgame' / 'panel_stub.json'
PANEL_EXISTING_ALIAS = PARENT / 'packets' / PANEL_ALIAS
PANEL_ADMITTED = PARENT / 'lab' / 'astra-capture' / 'c2-kxnhlgame' / 'panel_admitted.json'
REGET_CITE = PARENT / 'lab' / 'astra-capture' / 'c2-kxnhlgame' / REGET_NAME
PIN_CITE = PARENT / 'packets' / PIN_NAME
ADMIT_PY = ROOT / 'admit.py'


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
    """Reget, seed, and scout occurrence_datetime disagree."""

    def __init__(self):
        super().__init__('occurrence_datetime')


class AdmitPyRefused(OrchestratorError):
    """Variants does not run admit.py and does not write admitted_at."""

    def __init__(self):
        super().__init__('admit.py refused')


class ExaminerNotReady(OrchestratorError):
    """Examiner stays HOLD pre-PR until after merge and Clock admit."""

    def __init__(self):
        super().__init__('Examiner HOLD pre-PR')


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
    """Examiner HOLD pre-PR until after merge and sha verify."""
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
    """The series and events 429 list gaps stay gaps. Nothing is written."""
    del which, result, occurrence_datetime
    raise InventedResultRefused()


def invent_parent_settlement(ticker=None, result=None):
    """Parent SEP26 seeds stay active with an empty result."""
    del ticker, result
    raise InventedResultRefused()


def assign_occurrence(ticker=None, value=None):
    """A missing occurrence on a 429 list gap stays missing."""
    del ticker, value
    raise InventedSoTRefused()


def copy_scout_n_into_settled_join(value=None):
    """The scout pin is not the scorecard count."""
    del value
    raise ScorecardPromotionRefused()


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
    if label in ('invent_depth', 'invented_depth'):
        raise InventedDepthRefused()
    if label == 'admit_py':
        raise AdmitPyRefused()
    if label == 'live_orders':
        raise LiveOrdersForbidden()
    if label == 'ungate':
        raise UngateRefused()
    if label == 'copy_scout_n':
        raise ScorecardPromotionRefused()
    raise AdversaryRefused(ADVERSARY_LABELS[label])


def owned_dirs():
    return (ROOT, LAB_BUNDLE, SCIENCE, PACKET_DIR)


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
    return value == '' or value is None


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
    if payload.get('examiner_hold_sha256') != HOLD_SHA256:
        raise OrchestratorError('source pins')
    if payload.get('maximize_pin_sha256') != PIN_SHA256:
        raise OrchestratorError('source pins')
    if payload.get('digests_txt_sha256') != DIGESTS_SHA256:
        raise OrchestratorError('source pins')
    if payload.get('knob') != KNOB or payload.get('arms') != JOIN_GATE:
        raise OrchestratorError('source pins')
    if payload.get('admitted_at') is not None:
        raise OrchestratorError('source pins')
    if payload.get('settled_nonempty_result_N_scout') != SCOUT_NONEMPTY_N:
        raise OrchestratorError('source pins')
    if payload.get('scout_n_copied_into_settled_join_n') is not False:
        raise ScorecardPromotionRefused()
    if payload.get('yes_n') != YES_N or payload.get('no_n') != NO_N:
        raise OrchestratorError('source pins')
    if payload.get('parent_seed_tickers') != list(PARENT_SEED_TICKERS):
        raise OrchestratorError('source pins')
    if payload.get('parent_seeds_finalized_nonempty_N') != PARENT_FINALIZED_N:
        raise OrchestratorError('source pins')
    if payload.get('parent_seed_results') != PARENT_SEED_RESULTS:
        raise InventedResultRefused()
    if payload.get('parent_seed_statuses') != PARENT_SEED_STATUSES:
        raise InventedResultRefused()
    if payload.get('seed_panel_result') != '':
        raise InventedResultRefused()
    if payload.get('parent_sep26_active_empty') is not True:
        raise InventedResultRefused()
    if payload.get('reget_parent_active_empty_tickers') != list(REGET_PARENT_TICKERS):
        raise OrchestratorError('source pins')
    if payload.get('reget_parent_active_empty_n') != REGET_PARENT_N:
        raise OrchestratorError('source pins')
    if payload.get('settled_list_429') != LIST_429 or payload.get('open_list_429') != LIST_429:
        raise OrchestratorError('source pins')
    if payload.get('events_settled_list_429') is not True:
        raise InventedResultRefused()
    if payload.get('list_429_backfilled') is not False:
        raise InventedResultRefused()
    if payload.get('honest_gaps') != list(HONEST_GAPS):
        raise InventedResultRefused()
    if payload.get('fee_import_used') is not False or payload.get('rails_import_used') is not False:
        raise OrchestratorError('source pins')
    if payload.get('fee_arms') is not False:
        raise OrchestratorError('source pins')
    if payload.get('feebook_commit_fixed_not_loaded') != FEEBOOK_COMMIT:
        raise OrchestratorError('source pins')
    if payload.get('rails_commit_fixed_not_loaded') != RAILS_COMMIT:
        raise OrchestratorError('source pins')
    if payload.get('does_not_run_admit_py') is not True:
        raise AdmitPyRefused()
    if payload.get('base_commit') != BASE_COMMIT:
        raise OrchestratorError('source pins')
    if payload.get('lee_ready') != 'REFUSED':
        raise LeeReadyRefused()
    if payload.get('nhl_fq_reopen') is not False or payload.get('fq_reopen') is not False:
        raise OrchestratorError('source pins')
    if payload.get('c3_rj_reopen') is not False or payload.get('c5_rj_reopen') is not False:
        raise OrchestratorError('source pins')
    if payload.get('r3p3_rj_reopen') is not False or payload.get('cap_sr_reopen') is not False:
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


def _validate_market_row(row):
    if not isinstance(row, dict):
        raise OrchestratorError('scout market')
    ticker = row.get('ticker')
    if not isinstance(ticker, str) or not ticker.startswith('KXNHLGAME-'):
        raise InventedMarketRefused()
    if row.get('nonempty_result') is not True:
        raise InventedResultRefused()
    if row.get('status') != 'finalized' or not _nonempty_result(row.get('result')):
        raise InventedResultRefused()
    occ = row.get('occurrence_datetime')
    close = row.get('close_time')
    if not isinstance(occ, str) or not occ.endswith('Z'):
        raise OccurrenceIntegrityRefused()
    if not isinstance(close, str) or not close.endswith('Z'):
        raise OccurrenceIntegrityRefused()
    source = row.get('source')
    if not isinstance(source, str) or not source.startswith('market_KXNHLGAME_') or not source.endswith('.json'):
        raise OrchestratorError('scout source')
    if ticker in PARENT_SEED_TICKERS or ticker in REGET_PARENT_TICKERS or ticker in PANEL_MARKET_TICKERS:
        raise InventedMarketRefused()
    return row


def _validate_scout(payload):
    if payload.get('packet') != SCOUT_PACKET or payload.get('feature_family') != FEATURE_FAMILY:
        raise OrchestratorError('scout')
    if payload.get('series') != [SERIES]:
        raise OrchestratorError('scout')
    if payload.get('settled_nonempty_result_N') != SCOUT_NONEMPTY_N:
        raise OrchestratorError('scout N')
    if payload.get('settled_list_limit') != SETTLED_LIST_LIMIT:
        raise OrchestratorError('scout')
    if payload.get('settled_list_http') != LIST_429 or payload.get('open_list_http') != LIST_429:
        raise InventedResultRefused()
    if payload.get('settled_list_cursor_present') is not False:
        raise InventedResultRefused()
    if payload.get('open_list_n') is not None:
        raise InventedMarketRefused()
    if payload.get('method') != SCOUT_METHOD:
        raise OrchestratorError('scout mode')
    if payload.get('host') != PUBLIC_HOST:
        raise OrchestratorError('scout host')
    if payload.get('parent_seeds_finalized_nonempty_N') != PARENT_FINALIZED_N:
        raise InventedResultRefused()
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
    markets = payload.get('markets')
    if not isinstance(markets, list) or len(markets) != SCOUT_NONEMPTY_N:
        raise OrchestratorError('scout markets')
    seen = []
    for row in markets:
        checked = _validate_market_row(row)
        if checked['ticker'] in seen:
            raise InventedMarketRefused()
        seen.append(checked['ticker'])
    return payload


def _validate_seed(payload, scout):
    if payload.get('settled_nonempty_result_N') != SCOUT_NONEMPTY_N:
        raise OrchestratorError('seed N')
    if payload.get('overnight_finalized_nonempty_N') != SCOUT_NONEMPTY_N:
        raise OrchestratorError('seed N')
    if payload.get('settled_list_attempted_KXNHLGAME') != LIST_429:
        raise InventedResultRefused()
    if payload.get('method') != SCOUT_METHOD:
        raise OrchestratorError('seed')
    if payload.get('parent_seed_tickers') != list(PARENT_SEED_TICKERS):
        raise OrchestratorError('seed ticker')
    if payload.get('parent_seeds_finalized_nonempty_N') != PARENT_FINALIZED_N:
        raise InventedResultRefused()
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
    return payload


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
    if 'results' in payload or 'pnl' in payload:
        raise ScorecardPromotionRefused()
    if 'markets' in payload or 'artifacts' in payload:
        raise InventedResultRefused()
    rows = payload.get('markets_nonempty')
    if not isinstance(rows, list) or len(rows) != SCOUT_NONEMPTY_N:
        raise OrchestratorError('reget markets')
    parents = payload.get('parent_seeds_active_empty')
    if not isinstance(parents, list) or len(parents) != REGET_PARENT_N:
        raise OrchestratorError('reget parents')
    scout_rows = {}
    for row in scout.get('markets') or []:
        scout_rows[row['ticker']] = row
    settled = {}
    yes_n = 0
    no_n = 0
    for row in rows:
        if not isinstance(row, dict):
            raise InventedMarketRefused()
        ticker = row.get('ticker')
        if ticker in settled or ticker not in scout_rows:
            raise InventedMarketRefused()
        if row.get('status') != 'finalized' or not _nonempty_result(row.get('result')):
            raise InventedResultRefused()
        if 'orderbook_fp' in row:
            raise InventedDepthRefused()
        scout_row = scout_rows[ticker]
        if scout_row.get('source') != row.get('file'):
            raise OrchestratorError('reget file')
        for field in COMPARE_FIELDS:
            if row.get(field) != scout_row.get(field):
                raise OrchestratorError('scout reget ' + field)
        event = row.get('event_ticker')
        if not isinstance(event, str) or not ticker.startswith(event + '-'):
            raise InventedMarketRefused()
        settled[ticker] = row
        if row.get('result') == 'yes':
            yes_n += 1
        else:
            no_n += 1
    if set(settled) != set(scout_rows) or yes_n != YES_N or no_n != NO_N:
        raise OrchestratorError('reget census')
    seen_parents = []
    for row in parents:
        if not isinstance(row, dict):
            raise InventedMarketRefused()
        ticker = row.get('ticker')
        if ticker in settled or ticker in seen_parents:
            raise InventedMarketRefused()
        if row.get('status') != 'active' or row.get('result') != '':
            raise InventedResultRefused()
        if ticker not in PANEL_MARKET_TICKERS:
            raise InventedMarketRefused()
        occ = row.get('occurrence_datetime')
        if not isinstance(occ, str) or not occ.endswith('Z'):
            raise OccurrenceIntegrityRefused()
        if not isinstance(row.get('file'), str) or not row['file'].endswith('.json'):
            raise OrchestratorError('reget parent file')
        seen_parents.append(ticker)
    if seen_parents != list(REGET_PARENT_TICKERS):
        raise OrchestratorError('reget parents')
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
    if payload.get('series_ticker') != SERIES:
        raise OrchestratorError('panel')
    if payload.get('admitted_at') is not None:
        raise OrchestratorError('admitted_at')
    if payload.get('purpose') != PANEL_PURPOSE or payload.get('cohort_kind') != COHORT_KIND:
        raise OrchestratorError('panel')
    if payload.get('scout_cite') != SCOUT_CITE_PANEL or payload.get('scout_sha256') != SCOUT_HUNT_SHA256:
        raise OrchestratorError('panel')
    if payload.get('rules') != list(PANEL_RULES):
        raise OrchestratorError('panel')
    if payload.get('cohort_summary') != COHORT_SUMMARY:
        raise OrchestratorError('cohort')
    if payload.get('stubbed_at_et') != STUBBED_AT:
        raise OrchestratorError('panel')
    for key in ('results', 'pnl'):
        if key not in payload or payload[key] is not None:
            raise ScorecardPromotionRefused()
    events = payload.get('events')
    markets = payload.get('markets')
    if not isinstance(events, list) or len(events) != PANEL_EVENTS_N:
        raise OrchestratorError('events')
    if not isinstance(markets, list) or len(markets) != PANEL_MARKETS_N:
        raise OrchestratorError('markets')
    event_tickers = []
    for event in events:
        if not isinstance(event, dict):
            raise OrchestratorError('events')
        if event.get('admitted_at') is not None:
            raise OrchestratorError('admitted_at')
        if set(event) != {'event_ticker', 'markets_n', 'occurrence_datetime'}:
            raise OrchestratorError('events')
        if event.get('markets_n') != 2:
            raise OrchestratorError('events')
        occ = event.get('occurrence_datetime')
        if not isinstance(occ, str) or not occ.endswith('Z'):
            raise OccurrenceIntegrityRefused()
        event_tickers.append(event.get('event_ticker'))
    if event_tickers != list(PANEL_EVENT_TICKERS):
        raise OrchestratorError('events')
    seen = []
    for market in markets:
        if not isinstance(market, dict):
            raise OrchestratorError('market')
        if market.get('admitted_at') is not None:
            raise OrchestratorError('admitted_at')
        if market.get('status') != 'active' or market.get('result') != '':
            raise InventedResultRefused()
        if 'orderbook_fp' in market:
            raise InventedDepthRefused()
        ticker = market.get('ticker')
        event = market.get('event_ticker')
        if not isinstance(ticker, str) or not isinstance(event, str):
            raise InventedMarketRefused()
        if not ticker.startswith(event + '-'):
            raise InventedMarketRefused()
        if market.get('occurrence_datetime') != next(
            item.get('occurrence_datetime') for item in events if item.get('event_ticker') == event
        ):
            raise OccurrenceIntegrityRefused()
        seen.append(ticker)
    if seen != list(PANEL_MARKET_TICKERS):
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
    if 'settled_join_n' in payload or 'occurrence_match_n' in payload or 'admit_ready_flag' in payload:
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
    if payload.get('prior_done') != 'R3P3-RJ PR42 main@' + BASE_COMMIT:
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


def _assert_hold(payload):
    if payload.get('id') != 'EXAMINER_HOLD_NHL_KXNHLGAME_SETTLED_JOIN_HARNESS_PRE_PR':
        raise OrchestratorError('examiner hold')
    if payload.get('status') != 'HOLD_PRE_PR' or payload.get('stub_ready') is not True:
        raise ExaminerNotReady()
    if payload.get('packet') != EXPERIMENT_ID or payload.get('feature_family') != FEATURE_FAMILY:
        raise OrchestratorError('examiner hold')
    if payload.get('knob') != KNOB or payload.get('arm_values') != JOIN_GATE:
        raise OrchestratorError('examiner hold')
    if payload.get('arms') != list(ARMS):
        raise OrchestratorError('examiner hold')
    if payload.get('settled_nonempty_result_N_scout') != SCOUT_NONEMPTY_N:
        raise OrchestratorError('examiner hold')
    if payload.get('scout_markets_settled_nonempty') != SCOUT_NONEMPTY_N:
        raise OrchestratorError('examiner hold')
    if payload.get('admitted_at') is not None:
        raise OrchestratorError('admitted_at')
    if payload.get('metrics_null') != list(HOLD_METRICS):
        raise ScorecardPromotionRefused()
    if payload.get('does_not_ungate') != list(DOES_NOT_UNGATE):
        raise UngateRefused()
    if payload.get('stamped_at_et') != HOLD_STAMPED_AT:
        raise OrchestratorError('examiner hold')
    if payload.get('freeze_sha256') != FREEZE_SHA256:
        raise OrchestratorError('examiner hold')
    if payload.get('scout_reget_sha256') != SCOUT_SHA256:
        raise OrchestratorError('examiner hold')
    if payload.get('scout_summary_sha256') != SEED_SHA256:
        raise OrchestratorError('examiner hold')
    if payload.get('panel_stub_sha256') != PANEL_STUB_SHA256:
        raise OrchestratorError('examiner hold')
    if payload.get('settled_reget_capture_sha256') != REGET_SHA256:
        raise OrchestratorError('examiner hold')
    if payload.get('box_digest_match') is not True:
        raise OrchestratorError('examiner hold')
    if payload.get('prior_r3p3_rj_pr42_main') != BASE_COMMIT:
        raise OrchestratorError('examiner hold')
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
    _assert_owned(HOLD_NAME, HOLD_SHA256, HOLD_BYTES)
    _assert_owned(PIN_NAME, PIN_SHA256, PIN_BYTES)
    _assert_owned(DIGESTS_NAME, DIGESTS_SHA256, DIGESTS_BYTES)
    _assert_owned('EMPTY_RESULTS.json', EMPTY_SHA256, EMPTY_BYTES)
    _assert_owned(SOURCE_PINS_NAME, SOURCE_PINS_SHA256, SOURCE_PINS_BYTES)
    _assert_digest(FREEZE_GOV, FREEZE_SHA256, FREEZE_BYTES)
    _assert_digest(SCOUT_CITE_DIR / SCOUT_NAME, SCOUT_SHA256, SCOUT_BYTES)
    _assert_digest(SCOUT_CITE_DIR / SEED_NAME, SEED_SHA256, SEED_BYTES)
    _assert_digest(PANEL_GOV, PANEL_STUB_SHA256, PANEL_BYTES)
    _assert_digest(PANEL_CAPTURE, PANEL_STUB_SHA256, PANEL_BYTES)
    _assert_digest(PANEL_EXISTING_ALIAS, PANEL_STUB_SHA256, PANEL_BYTES)
    _assert_digest(REGET_CITE, REGET_SHA256, REGET_BYTES)
    _assert_digest(PIN_CITE, PIN_SHA256, PIN_BYTES)
    _assert_digest(EMPTY_RESULTS, EMPTY_SHA256, EMPTY_BYTES)
    _assert_digest(LAB_BUNDLE / 'results.json', EMPTY_SHA256, EMPTY_BYTES)
    _assert_digest(LAB_BUNDLE / 'results' / 'EMPTY_RESULTS.json', EMPTY_SHA256, EMPTY_BYTES)
    _assert_digest(SCIENCE / 'results' / 'EMPTY_RESULTS.json', EMPTY_SHA256, EMPTY_BYTES)
    _assert_digest(PACKET_DIR / 'results.json', EMPTY_SHA256, EMPTY_BYTES)
    _assert_digest(PACKET_DIR / 'results' / 'EMPTY_RESULTS.json', EMPTY_SHA256, EMPTY_BYTES)
    scout = _validate_scout(_read_pinned(SCOUT_PATH, SCOUT_SHA256, SCOUT_BYTES))
    _validate_seed(_read_pinned(SEED_PATH, SEED_SHA256, SEED_BYTES), scout)
    _validate_reget(_read_pinned(REGET_PATH, REGET_SHA256, REGET_BYTES), scout)
    _validate_panel(_read_pinned(PANEL_CAPTURE, PANEL_STUB_SHA256, PANEL_BYTES))
    _assert_frozen(_read_pinned(FROZEN_EXPERIMENT, FROZEN_SHA256, FROZEN_BYTES))
    _assert_accept(_read_pinned(CONDUCTOR_ACCEPT, ACCEPT_SHA256, ACCEPT_BYTES))
    _assert_hold(_read_pinned(EXAMINER_HOLD, HOLD_SHA256, HOLD_BYTES))
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
    freeze_match = sha256_file(PACKET) == FREEZE_SHA256 and sha256_file(FREEZE_GOV) == FREEZE_SHA256
    scout_match = sha256_file(SCOUT_PATH) == SCOUT_SHA256 and sha256_file(SCOUT_CITE_DIR / SCOUT_NAME) == SCOUT_SHA256
    seed_match = sha256_file(SEED_PATH) == SEED_SHA256 and sha256_file(SCOUT_CITE_DIR / SEED_NAME) == SEED_SHA256
    panel_match = sha256_file(PANEL_CAPTURE) == PANEL_STUB_SHA256 and sha256_file(PANEL_GOV) == PANEL_STUB_SHA256
    reget_match = sha256_file(REGET_PATH) == REGET_SHA256 and sha256_file(REGET_CITE) == REGET_SHA256
    accept_match = sha256_file(CONDUCTOR_ACCEPT) == ACCEPT_SHA256 and sha256_file(PACKET_DIR / ACCEPT_NAME) == ACCEPT_SHA256
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
        'governance_nhl_cites_present': FREEZE_GOV.is_file() and (SCOUT_CITE_DIR / SCOUT_NAME).is_file(),
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
    canonical = {PANEL_CAPTURE.resolve(), PANEL_EXISTING_ALIAS.resolve(), PANEL_GOV.resolve()}
    for directory in owned_dirs():
        canonical.add((directory / 'panel_stub.json').resolve())
        canonical.add((directory / PANEL_ALIAS).resolve())
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
    parents = {}
    for row in checked['parent_seeds_active_empty']:
        parents[row['ticker']] = row
    view = dict(checked)
    view['markets'] = markets
    view['parent_active'] = parents
    view['honest_gaps'] = list(HONEST_GAPS)
    return view


def load_reget():
    scout = load_scout()
    payload = _read_pinned(REGET_PATH, REGET_SHA256, REGET_BYTES)
    return _settled_view(payload, scout)


def list_429_gaps(reget=None):
    """Series list and events list 429 gaps. No ticker and no result are attached."""
    if reget is None:
        reget = load_reget()
    if reget.get('settled_list_http') != LIST_429:
        raise InventedResultRefused()
    if reget.get('honest_gaps') != list(HONEST_GAPS):
        raise InventedResultRefused()
    if 'markets' in (reget.get('artifacts') or {}):
        raise InventedResultRefused()
    markets = reget.get('markets') or {}
    for key in HONEST_GAPS:
        if key in markets:
            raise InventedResultRefused()
    for ticker, row in markets.items():
        if row.get('status') != 'finalized':
            raise InventedResultRefused()
    return HONEST_GAPS


def assert_occurrence_pair(left, right):
    """Require one shared occurrence_datetime. Does not write a match count."""
    if not isinstance(left, dict) or not isinstance(right, dict):
        raise OccurrenceIntegrityRefused()
    values = (
        left.get('occurrence_datetime'),
        right.get('occurrence_datetime'),
    )
    if any(not isinstance(value, str) or not value.endswith('Z') for value in values):
        raise OccurrenceIntegrityRefused()
    if values[0] != values[1]:
        raise OccurrenceIntegrityRefused()
    return values[0]


def occurrence_agreement_tickers(panel=None):
    """Settled single-market rows whose scout, seed, and reget clocks agree.

    Parent SEP26 rows are not in this tuple. This list is not
    occurrence_match_n and it is not settled_join_n.
    """
    if panel is None:
        panel = load_panel()
    else:
        _validate_panel(panel)
    reget = load_reget()['markets']
    seed_rows = {row['ticker']: row for row in load_seed()['markets']}
    scout_rows = {row['ticker']: row for row in load_scout()['markets']}
    if set(reget) != set(seed_rows) or set(reget) != set(scout_rows):
        raise InventedMarketRefused()
    agreed = []
    for ticker in scout_rows:
        market = reget[ticker]
        assert_occurrence_pair(market, seed_rows[ticker])
        assert_occurrence_pair(market, scout_rows[ticker])
        if ticker in PANEL_MARKET_TICKERS:
            raise InventedMarketRefused()
        agreed.append(ticker)
    if len(agreed) != SCOUT_NONEMPTY_N:
        raise OrchestratorError('occurrence rows')
    return tuple(agreed)


def parent_active_occurrence_tickers(panel=None):
    """Reget parent rows whose panel occurrence matches and whose result stays empty."""
    if panel is None:
        panel = load_panel()
    else:
        _validate_panel(panel)
    parents = load_reget()['parent_active']
    by_ticker = {market.get('ticker'): market for market in panel.get('markets') or []}
    if set(by_ticker) != set(PANEL_MARKET_TICKERS):
        raise InventedMarketRefused()
    agreed = []
    for ticker in REGET_PARENT_TICKERS:
        market = parents[ticker]
        panel_market = by_ticker[ticker]
        assert_occurrence_pair(market, panel_market)
        if panel_market.get('close_time') != market.get('close_time'):
            raise OccurrenceIntegrityRefused()
        if panel_market.get('result') != '' or market.get('result') != '':
            raise InventedResultRefused()
        if panel_market.get('status') != 'active' or market.get('status') != 'active':
            raise InventedResultRefused()
        agreed.append(ticker)
    if len(agreed) != REGET_PARENT_N:
        raise OrchestratorError('parent rows')
    return tuple(agreed)


def structural_rows(panel=None):
    """Label authentic reget rows. Does not write scorecard counts."""
    if panel is None:
        panel = load_panel()
    else:
        _validate_panel(panel)
    list_429_gaps()
    agreed = occurrence_agreement_tickers(panel)
    parent_agreed = parent_active_occurrence_tickers(panel)
    reget = load_reget()
    markets = reget['markets']
    parents = reget['parent_active']
    seed_rows = {row['ticker']: row for row in load_seed()['markets']}
    rows = []
    for ticker in agreed:
        market = markets[ticker]
        result = market.get('result')
        if market.get('status') != 'finalized' or result not in FINALIZED_RESULTS:
            raise InventedResultRefused()
        if seed_rows[ticker].get('source') != market.get('file'):
            raise OrchestratorError('row source')
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
    for ticker in parent_agreed:
        rows.append({
            'key': ticker,
            'panel_ticker': ticker,
            'j0': 'parent_active_empty',
            'j1': 'occurrence_datetime_match',
            'result': None,
            'on_settled_list': False,
            'parent_seed': ticker in PARENT_SEED_TICKERS,
            'single_market_get': True,
        })
        if parents[ticker].get('result') != '':
            raise InventedResultRefused()
    for key in HONEST_GAPS:
        rows.append({
            'key': key,
            'panel_ticker': None,
            'j0': 'honest_gap',
            'j1': 'honest_gap',
            'result': None,
            'on_settled_list': False,
            'parent_seed': False,
            'single_market_get': False,
        })
    if len(rows) != ROW_LABEL_N:
        raise OrchestratorError('row labels')
    passes = [row for row in rows if row['j0'] == 'nonempty_result_required_pass']
    active = [row for row in rows if row['j0'] == 'parent_active_empty']
    gaps = [row for row in rows if row['j0'] == 'honest_gap']
    if len(passes) != SCOUT_NONEMPTY_N or len(active) != REGET_PARENT_N or len(gaps) != len(HONEST_GAPS):
        raise OrchestratorError('row labels')
    if any(row['on_settled_list'] for row in passes):
        raise InventedResultRefused()
    if sum(1 for row in active if row['parent_seed']) != PARENT_SEED_N:
        raise OrchestratorError('row labels')
    if any(row['result'] is not None for row in active):
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
    if pins['governance_nhl_cites_present'] is not True or pins['reget_cite_present'] is not True:
        raise OrchestratorError('governance cite')
    rows = structural_rows(panel)
    agreed = occurrence_agreement_tickers(panel)
    parent_agreed = parent_active_occurrence_tickers(panel)
    if len(agreed) != SCOUT_NONEMPTY_N or len(parent_agreed) != REGET_PARENT_N:
        raise OrchestratorError('occurrence rows')
    panel_results = [market.get('result') for market in panel.get('markets') or []]
    if panel_results != [''] * PANEL_MARKETS_N:
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
        'yes_n': YES_N,
        'no_n': NO_N,
        'parent_seed_tickers': list(PARENT_SEED_TICKERS),
        'parent_seeds_finalized_nonempty_N': PARENT_FINALIZED_N,
        'parent_seed_results': dict(PARENT_SEED_RESULTS),
        'seed_panel_result': '',
        'parent_sep26_active_empty': True,
        'reget_parent_active_empty_n': REGET_PARENT_N,
        'settled_list_429': LIST_429,
        'open_list_429': LIST_429,
        'events_settled_list_429': True,
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
        'c3_rj_reopen': False,
        'c5_rj_reopen': False,
        'r3p3_rj_reopen': False,
        'arm_b_touch': False,
        'admit_py_run': False,
        'does_not_ungate': list(DOES_NOT_UNGATE),
        's1_s2_r2p4_ungated': False,
        'examiner_status': 'HOLD_PRE_PR',
        'stub_ready': True,
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
        'governance_nhl_cites_present': True,
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
    scorecard['examiner_status'] = 'HOLD_PRE_PR'
    scorecard['stub_ready'] = True
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
        'nhl_fq_reopen': False,
        'c3_rj_reopen': False,
        'c5_rj_reopen': False,
        'r3p3_rj_reopen': False,
        'fq_reopen': False,
        'cap_sr_reopen': False,
        'arm_b_touch': False,
        's1_s2_r2p4_ungated': False,
        'examiner_status': 'HOLD_PRE_PR',
        'stub_ready': True,
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
    parent_agreed = parent_active_occurrence_tickers(panel)
    extra = {
        'row_labels': rows,
        'occurrence_agreement_tickers': list(agreed),
        'parent_active_occurrence_tickers': list(parent_agreed),
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
