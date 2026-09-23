"""S4 KXNCAAFGAME settled-resolution join harness.

Measurement only. One knob: join_gate. This module does not edit the
S4-FQ lab, the NHL-RJ lab, the C3-RJ lab, the C5-RJ lab, the R3P3-RJ
lab, feebook, rails, Cap-SR, or any FQ sibling. It does not place
orders, does not read Logan keys, does not run admit.py, and does not
write scorecard metrics.

The checkout freeze, scout reget, seed summary, panel stub, settled
reget, and accept match the attached sha256 values. The panel stub keeps
admitted_at null. The series settled list and the events settled list
stay the honest 429 gaps. Named event and market GET gaps stay gaps.
Parent SEP26 FQ seeds stay active with a null result. The reget does
not carry occurrence_datetime for those seeds, and this module does not
invent one. Lee-Ready is refused. Settled results, depth, fills, and
PnL are not invented. Scout settled_nonempty_result_N is a pin and is
not copied into settled_join_n.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PARENT = ROOT.parent

LAB_DIRECTORY = 'kalshi_kxncaafgame_settled_join_lab_20260923'
EXPERIMENT_ID = 'S4-KXNCAAFGAME-SETTLED-RESOLUTION-JOIN-HARNESS'
FEATURE_FAMILY = 'S4-RJ'
SCOUT_PACKET = 'S4-KXNCAAFGAME-SETTLED-JOIN'
PARENT_PACKET_ID = 'S4-KXNCAAFGAME-MEAS'
PANEL_VERSION = '2026-09-22.s4-kxncaafgame-v0'
SCHEMA_ID = 'astra.registry.s4_kxncaafgame_panel.v0'
SERIES = 'KXNCAAFGAME'
STUB_STATUS = 'PANEL_SCHEMA_STUB_SEED_NOT_ADMITTED'
PANEL_PURPOSE = 'measurement_gate'
COHORT_KIND = 'sat_2026-09-26_kxncaafgame_ticker_26SEP26'
KNOB = 'join_gate'
J0 = 'J0'
J1 = 'J1'
ARMS = (J0, J1)
JOIN_GATE = {
    J0: 'nonempty_result_required',
    J1: 'occurrence_datetime_match',
}
FINALIZED_RESULTS = ('yes', 'no')
SCOUT_NONEMPTY_N = 18
YES_N = 9
NO_N = 9
EVENT_EMBED_N = 10
MARKET_GET_N = 8
PARENT_SEED_N = 3
PARENT_FINALIZED_N = 0
PANEL_EVENTS_N = 113
PANEL_MARKET_TICKERS_N = 226
HONEST_GAP_N = 15
NAMED_GET_GAP_N = 12
ROW_LABEL_N = 36
SETTLED_LIST_LIMIT = 20
KERNEL_SHA256 = '9e6556c150c726b679ac8393f1f5338cf983489259b0f34cdedf221c030be795'
SCOUT_CITE_PANEL = 'lab/governance/astra/packets/scout_s4_kxncaafgame/'
STUBBED_AT = '2026-09-22T23:49:34Z'
ADMIT_GATE_STATUS = 'WAIT_CLOCK_JOIN'
INELIGIBLE_EVENT = 'KXNCAAFGAME-26SEP25CLEMCAL'
PARENT_SEED_TICKERS = (
    'KXNCAAFGAME-26SEP26BUCKPITT-PITT',
    'KXNCAAFGAME-26SEP26BUCKPITT-BUCK',
    'KXNCAAFGAME-26SEP26TEXTENN-TEX',
)
PARENT_SEED_RESULTS = {
    'KXNCAAFGAME-26SEP26BUCKPITT-PITT': None,
    'KXNCAAFGAME-26SEP26BUCKPITT-BUCK': None,
    'KXNCAAFGAME-26SEP26TEXTENN-TEX': None,
}
PARENT_SEED_STATUSES = {
    'KXNCAAFGAME-26SEP26BUCKPITT-PITT': 'active',
    'KXNCAAFGAME-26SEP26BUCKPITT-BUCK': 'active',
    'KXNCAAFGAME-26SEP26TEXTENN-TEX': 'active',
}
PARENT_EVENT_OCCURRENCE = {
    'KXNCAAFGAME-26SEP26BUCKPITT': '2026-09-26T19:00:00Z',
    'KXNCAAFGAME-26SEP26TEXTENN': '2026-09-26T19:00:00Z',
}
PARENT_EVENT_MARKETS = {
    'KXNCAAFGAME-26SEP26BUCKPITT': (
        'KXNCAAFGAME-26SEP26BUCKPITT-PITT',
        'KXNCAAFGAME-26SEP26BUCKPITT-BUCK',
    ),
    'KXNCAAFGAME-26SEP26TEXTENN': (
        'KXNCAAFGAME-26SEP26TEXTENN-TENN',
        'KXNCAAFGAME-26SEP26TEXTENN-TEX',
    ),
}
SETTLED_TICKERS = (
    'KXNCAAFGAME-26SEP05UCLACAL-CAL',
    'KXNCAAFGAME-26SEP05UCLACAL-UCLA',
    'KXNCAAFGAME-26SEP12CAMPFLA-CAMP',
    'KXNCAAFGAME-26SEP12CAMPFLA-FLA',
    'KXNCAAFGAME-26SEP12OKLAMICH-MICH',
    'KXNCAAFGAME-26SEP12OKLAMICH-OKLA',
    'KXNCAAFGAME-26SEP12OSUTEX-OSU',
    'KXNCAAFGAME-26SEP12OSUTEX-TEX',
    'KXNCAAFGAME-26SEP19COLONW-COLO',
    'KXNCAAFGAME-26SEP19COLONW-NW',
    'KXNCAAFGAME-26SEP19FSUALA-ALA',
    'KXNCAAFGAME-26SEP19FSUALA-FSU',
    'KXNCAAFGAME-26SEP19KENTOSU-KENT',
    'KXNCAAFGAME-26SEP19KENTOSU-OSU',
    'KXNCAAFGAME-26SEP19MEBC-BC',
    'KXNCAAFGAME-26SEP19MEBC-ME',
    'KXNCAAFGAME-26SEP19STANDUKE-DUKE',
    'KXNCAAFGAME-26SEP19STANDUKE-STAN',
)
HONEST_GAPS = (
    'GET /markets?series_ticker=KXNCAAFGAME&status=settled|finalized|open list 429',
    'GET /events?series_ticker=KXNCAAFGAME&status=settled list 429',
    'FQ parent SEP26 panel seeds active/empty (not yet settled)',
    "event_get event_KXNCAAFGAME_26SEP19AUBOM.json error={'code': 'not_found', 'message': 'not found'}",
    "event_get event_KXNCAAFGAME_26SEP19EMUSTAN.json error={'code': 'too_many_requests', 'message': 'too many requests'}",
    "event_get event_KXNCAAFGAME_26SEP19LSUFLA.json error={'code': 'too_many_requests', 'message': 'too many requests'}",
    "event_get event_KXNCAAFGAME_26SEP19MIAMISF.json error={'code': 'not_found', 'message': 'not found'}",
    "event_get event_KXNCAAFGAME_26SEP19NDARK.json error={'code': 'not_found', 'message': 'not found'}",
    "event_get event_KXNCAAFGAME_26SEP19NDTEX.json error={'code': 'too_many_requests', 'message': 'too many requests'}",
    "event_get event_KXNCAAFGAME_26SEP19OSUIL.json error={'code': 'too_many_requests', 'message': 'too many requests'}",
    "event_get event_KXNCAAFGAME_26SEP19SELAULM.json error={'code': 'too_many_requests', 'message': 'too many requests'}",
    "event_get event_KXNCAAFGAME_26SEP19UGAARK.json error={'code': 'too_many_requests', 'message': 'too many requests'}",
    "event_get event_KXNCAAFGAME_26SEP19USCMSU.json error={'code': 'not_found', 'message': 'not found'}",
    "market_get market_KXNCAAFGAME_26SEP12CAMPFLA_CAMP.json error={'code': 'too_many_requests', 'message': 'too many requests'}",
    "market_get market_KXNCAAFGAME_26SEP19COLONW_NW.json error={'code': 'too_many_requests', 'message': 'too many requests'}",
)
GAP_LIST = HONEST_GAPS[0]
GAP_EVENTS = HONEST_GAPS[1]
LIST_429 = '429_honest'
LIST_HTTP = {
    'settled': LIST_429,
    'finalized': LIST_429,
    'open': LIST_429,
    'events_settled': LIST_429,
}
HTTP_COUNTS = {'200': 21, '429': 17, '404': 4}
SCOUT_METHOD = 'GET-only event embeds + single-market (list status=settled|finalized|open 429 honest)'
PARENT_NOTE = (
    'FQ parent panel SEP26 seeds still active/empty result (honest; future occ). '
    'Settled join uses prior-weekend SEP05/SEP12/SEP19 finalized cohort via GET /events embeds + single-market reget.'
)
FEEBOOK_COMMIT = '22371178cb2663250b4762f328069571c48cb551'
RAILS_COMMIT = '6a28e0d6254327ea4e6451c781bec56215ac6cac'
BASE_COMMIT = 'b450e780fd9752887579ee8d217b6dee76d918f8'
NHL_ACCEPT_SHA256 = 'ce82d9347c8af6666d96fb5c63be7693f4672306639ce4ba2360ba231c01e698'
FREEZE_SHA256 = '3a8e8ba52edd6acdc342c6a2faabb08665fe8a7a76e1b28af1c8e18850b03d99'
SCOUT_SHA256 = '57fa0b28325ac13015f49521a87661b3cc064d22a13cf960f4fcdfd9badaa3dc'
SEED_SHA256 = '9e67cd16f3ec6536d5dae3fe07de6e6b073c1c8d1adc9bb7e9297090ef567ce1'
PANEL_STUB_SHA256 = '38167d11da5842bc4d39e6e7dcaab20a67294c735ba14d8bbeafde3154c6342a'
REGET_SHA256 = '5bb0acfaa429e2ec1ad22e2e35e296540ac5b8e66eba4df6a0b2419d43257528'
ACCEPT_SHA256 = '87bb8d44e8ac50099cc66d0469dcd4a5cfafb78d92dd24e7a218100a6254da4a'
FROZEN_SHA256 = '273c59f2af1d18c840121923f07c3d557abb5b8b1a0fefa9bdb048ce89fc6abb'
EMPTY_SHA256 = '4a67cd4f8d62bbffc7d2b3f7acdc1639dc01cbab058b86a8e8c74fe56da69e43'
HOLD_SHA256 = '082921d6a9f202542792b4b34ae827835b2652b7b1c127466e9988a58e6d2d55'
PIN_SHA256 = 'bd72d0d807d3854a1dfd9c3162c177850d682ad46af1ed77e4e824d5a657fa01'
DIGESTS_SHA256 = 'd37a288ca0bd7d5209213461c15c48f3292afc36d55a6fc6946602a137e0ba6f'
SOURCE_PINS_SHA256 = '8c845b52335819448db146e1abc23cdbee2f314552eb8aad859549ae37dc766a'
FREEZE_BYTES = 5638
SCOUT_BYTES = 8481
SEED_BYTES = 7905
PANEL_BYTES = 94629
REGET_BYTES = 6366
ACCEPT_BYTES = 2018
FROZEN_BYTES = 1046
EMPTY_BYTES = 180
HOLD_BYTES = 2591
PIN_BYTES = 2560
DIGESTS_BYTES = 1103
SOURCE_PINS_BYTES = 5576
ACCEPT_STAMPED_AT = '2026-09-23T16:44:00-04:00'
FROZEN_STAMPED_AT = '2026-09-23T16:43:00-04:00'
SCOUT_FETCHED_AT = '2026-09-23T16:42:53-04:00'
HOLD_STAMPED_AT = '2026-09-23T16:43:00-04:00'
EMPTY_NOTE = 'pre-ACCEPT empty; S4-RJ measurement join only'
PUBLIC_HOST = 'https://api.elections.kalshi.com/trade-api/v2'
PANEL_HOST = 'api.elections.kalshi.com'
OUT_OF_SCOPE_ROUTE = 'POST /portfolio/orders'
ORTHOGONAL_PIN = 'packets/MAXIMIZE_PIN_2026-09-23_1643ET.md'
PRIOR_DONE = 'NHL-RJ PR44 main@' + BASE_COMMIT
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
    'S4_FQ_reopen',
    'NCAAF_FQ_reopen',
    'Cap-SR_reopen',
    'C3_RJ_reopen',
    'C5_RJ_reopen',
    'R3P3_RJ_reopen',
    'NHL_RJ_reopen',
    'ungate_S1_S2_R2P4',
    'Arm_B_touch',
    'admit_py_by_Variants',
    'live_orders',
    'copy_scout_N_into_settled_join_n',
    'Conductor_pulse_cloud_kick',
)
DOES_NOT_UNGATE = ('S1', 'S2', 'R2-P4')
ORTHOGONAL_TO = ('S4-FQ', 'NCAAF-FQ')
COMPARE_FIELDS = ('status', 'result', 'occurrence_datetime', 'close_time', 'source')
VOLUME_FIELDS = ('volume_fp', 'volume_24h_fp', 'open_interest_fp')
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
    's4_fq_reopen': 'S4-FQ reopen is refused',
    'ncaaf_fq_reopen': 'NCAAF-FQ reopen is refused',
    'nhl_fq_reopen': 'NHL-FQ reopen is refused',
    'cpi_fq_reopen': 'CPI-FQ reopen is refused',
    'atp_fq_reopen': 'ATP-FQ reopen is refused',
    'eth_fq_reopen': 'ETH-FQ reopen is refused',
    'cap_sr_reopen': 'Cap-SR reopen is refused',
    'empty_ob_reopen': 'EMPTY-OB reopen is refused',
    'c3_rj_reopen': 'C3-RJ reopen is refused',
    'c5_rj_reopen': 'C5-RJ reopen is refused',
    'r3p3_rj_reopen': 'R3P3-RJ reopen is refused',
    'nhl_rj_reopen': 'NHL-RJ reopen is refused',
    'arm_b': 'Arm B is refused',
    'q7_arm_b': 'Arm B is refused',
    'admit_py': 'admit.py is refused',
    'live_orders': 'live orders are refused',
    'logan_keys': 'Logan keys are refused',
    'ungate': 'S1 S2 R2-P4 stay gated',
    'copy_scout_n': 'scout N is not settled_join_n',
    'conductor_pulse_cloud': 'Conductor pulse cloud is refused',
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
    'kalshi_kxnhlgame_settled_join_lab_20260923',
    'nfl_factorial_lab_20260921',
    'nfl_paircheck_lab_20260922',
    'nfl_q7_rehab_p1_cadence_20260923',
    'packets/S4_KXNCAAFGAME_FEEQUEUE_HARNESS',
    'packets/S4_KXNCAAFGAME_FEEQUEUE_HARNESS_FREEZE_2026-09-23.md',
    'packets/S4_KXNCAAFGAME_MEASUREMENT_FREEZE_KERNEL_2026-09-22.md',
    'lab/astra-capture/s4-kxncaafgame/panel_stub.json',
    'lab/astra-capture/s4-kxncaafgame/README.md',
    'lab/governance/astra/packets/r3_p2_queue_position/results/demo_queue_sample_series.json',
)
FREEZE_NAME = 'S4_KXNCAAFGAME_SETTLED_RESOLUTION_JOIN_HARNESS_FREEZE_2026-09-23.md'
SCOUT_NAME = 'scout_settled_rejoin_S4_KXNCAAFGAME.json'
SEED_NAME = 'SEED_SETTLED_SUMMARY.json'
PANEL_ALIAS = 'S4_KXNCAAFGAME_PANEL_STUB_2026-09-22.json'
REGET_NAME = 'settled_reget_2026-09-23.json'
ACCEPT_NAME = 'CONDUCTOR_ACCEPT_S4_KXNCAAFGAME_SETTLED_JOIN_HARNESS_2026-09-23.json'
HOLD_NAME = 'EXAMINER_HOLD_S4_KXNCAAFGAME_SETTLED_JOIN_HARNESS_PRE_PR_2026-09-23.json'
PIN_NAME = 'MAXIMIZE_PIN_2026-09-23_1643ET.md'
DIGESTS_NAME = 'DIGESTS.txt'
SOURCE_PINS_NAME = 'SOURCE_PINS.json'
LAB_BUNDLE = ROOT / 'S4_KXNCAAFGAME_SETTLED_RESOLUTION_JOIN_HARNESS'
SCIENCE = PARENT / 'lab' / 'astra-science' / LAB_DIRECTORY
PACKET_DIR = PARENT / 'packets' / 'S4_KXNCAAFGAME_SETTLED_JOIN_HARNESS'
GOV = PARENT / 'lab' / 'governance' / 'astra' / 'packets'
SCOUT_CITE_DIR = GOV / 'scout_s4_settled_rejoin_2026-09-23'
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
PANEL_CAPTURE = PARENT / 'lab' / 'astra-capture' / 's4-kxncaafgame' / 'panel_stub.json'
PANEL_EXISTING_ALIAS = PARENT / 'packets' / PANEL_ALIAS
PANEL_ADMITTED = PARENT / 'lab' / 'astra-capture' / 's4-kxncaafgame' / 'panel_admitted.json'
REGET_CITE = PARENT / 'lab' / 'astra-capture' / 's4-kxncaafgame' / REGET_NAME
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
    """occurrence_datetime is not invented for a parent seed or a 429 gap."""

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
    """The panel file is not the pinned S4 seed."""

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
    """Parent SEP26 seeds stay active with a null result."""
    del ticker, result
    raise InventedResultRefused()


def assign_occurrence(ticker=None, value=None):
    """A missing occurrence on a parent seed or a 429 gap stays missing."""
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


def named_gap_files():
    """Filenames inside honest event_get and market_get gaps. Not market objects."""
    files = []
    for gap in HONEST_GAPS:
        if gap.startswith('event_get ') or gap.startswith('market_get '):
            files.append(gap.split(' ', 2)[1])
    if len(files) != NAMED_GET_GAP_N:
        raise OrchestratorError('honest gaps')
    return tuple(files)


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


def _source_kind(source):
    if not isinstance(source, str) or not source.endswith('.json'):
        raise OrchestratorError('scout source')
    if source.startswith('market_KXNCAAFGAME_'):
        return 'market'
    if source.startswith('event_KXNCAAFGAME_'):
        return 'event'
    raise OrchestratorError('scout source')


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
    if payload.get('event_embed_n') != EVENT_EMBED_N or payload.get('market_get_n') != MARKET_GET_N:
        raise OrchestratorError('source pins')
    if payload.get('parent_seed_tickers') != list(PARENT_SEED_TICKERS):
        raise OrchestratorError('source pins')
    if payload.get('parent_seeds_finalized_nonempty_N') != PARENT_FINALIZED_N:
        raise OrchestratorError('source pins')
    if payload.get('parent_seed_results') != PARENT_SEED_RESULTS:
        raise InventedResultRefused()
    if payload.get('parent_seed_statuses') != PARENT_SEED_STATUSES:
        raise InventedResultRefused()
    if payload.get('seed_panel_result') is not None:
        raise InventedResultRefused()
    if payload.get('parent_sep26_active_empty') is not True:
        raise InventedResultRefused()
    if payload.get('parent_reget_occurrence_present') is not False:
        raise InventedSoTRefused()
    if payload.get('settled_list_429') != LIST_429 or payload.get('open_list_429') != LIST_429:
        raise OrchestratorError('source pins')
    if payload.get('finalized_list_429') != LIST_429:
        raise InventedResultRefused()
    if payload.get('events_settled_list_429') is not True:
        raise InventedResultRefused()
    if payload.get('list_429_backfilled') is not False:
        raise InventedResultRefused()
    if payload.get('http_counts') != HTTP_COUNTS:
        raise OrchestratorError('source pins')
    if payload.get('honest_gap_n') != HONEST_GAP_N or payload.get('named_get_gap_n') != NAMED_GET_GAP_N:
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
    if payload.get('s4_fq_reopen') is not False or payload.get('ncaaf_fq_reopen') is not False:
        raise OrchestratorError('source pins')
    if payload.get('nhl_rj_reopen') is not False or payload.get('fq_reopen') is not False:
        raise OrchestratorError('source pins')
    if payload.get('c3_rj_reopen') is not False or payload.get('c5_rj_reopen') is not False:
        raise OrchestratorError('source pins')
    if payload.get('r3p3_rj_reopen') is not False or payload.get('cap_sr_reopen') is not False:
        raise OrchestratorError('source pins')
    if payload.get('arm_b_touch') is not False or payload.get('live_orders') is not False:
        raise OrchestratorError('source pins')
    if payload.get('conductor_cloud_kick') is not False:
        raise OrchestratorError('source pins')
    if payload.get('does_not_ungate') != list(DOES_NOT_UNGATE):
        raise UngateRefused()
    if payload.get('panel_version') != PANEL_VERSION:
        raise PanelVersionRefused()
    if payload.get('panel_events_n') != PANEL_EVENTS_N:
        raise OrchestratorError('source pins')
    if payload.get('panel_market_tickers_n') != PANEL_MARKET_TICKERS_N:
        raise OrchestratorError('source pins')
    for key in OUTPUT_KEYS:
        if key not in payload or payload[key] is not None:
            raise ScorecardPromotionRefused()
    return payload


def _validate_market_row(row, panel_tickers):
    if not isinstance(row, dict):
        raise OrchestratorError('scout market')
    ticker = row.get('ticker')
    if not isinstance(ticker, str) or not ticker.startswith('KXNCAAFGAME-'):
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
    kind = _source_kind(row.get('source'))
    if row.get('source') in named_gap_files():
        raise InventedResultRefused()
    if ticker in PARENT_SEED_TICKERS or ticker in panel_tickers:
        raise InventedMarketRefused()
    if 'orderbook_fp' in row or 'occurrence_datetime' not in row:
        raise InventedDepthRefused()
    return kind


def _parent_block(payload, require_finalized_n):
    if payload.get('parent_seed_tickers') != list(PARENT_SEED_TICKERS):
        raise OrchestratorError('parent seeds')
    if payload.get('parent_seed_results') != PARENT_SEED_RESULTS:
        raise InventedResultRefused()
    if payload.get('parent_seed_statuses') != PARENT_SEED_STATUSES:
        raise InventedResultRefused()
    present = 'parent_seeds_finalized_nonempty_N' in payload
    if require_finalized_n:
        if payload.get('parent_seeds_finalized_nonempty_N') != PARENT_FINALIZED_N:
            raise InventedResultRefused()
    elif present:
        raise InventedResultRefused()
    return payload


def _validate_scout(payload, panel_tickers):
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
    _parent_block(payload, True)
    if payload.get('parent_panel_seeds_note') != PARENT_NOTE:
        raise OrchestratorError('scout')
    if payload.get('occurrence_datetime_sot_match_all_settled_seeds') is not True:
        raise OccurrenceIntegrityRefused()
    if payload.get('scouted_at_et') != SCOUT_FETCHED_AT:
        raise OrchestratorError('scout')
    if payload.get('honest_gaps') != list(HONEST_GAPS):
        raise InventedResultRefused()
    if payload.get('http_counts') != HTTP_COUNTS:
        raise OrchestratorError('scout http')
    markets = payload.get('markets')
    if not isinstance(markets, list) or len(markets) != SCOUT_NONEMPTY_N:
        raise OrchestratorError('scout markets')
    seen = []
    event_n = 0
    market_n = 0
    for row in markets:
        kind = _validate_market_row(row, panel_tickers)
        if row['ticker'] in seen:
            raise InventedMarketRefused()
        seen.append(row['ticker'])
        if kind == 'event':
            event_n += 1
        else:
            market_n += 1
    if seen != list(SETTLED_TICKERS) or event_n != EVENT_EMBED_N or market_n != MARKET_GET_N:
        raise OrchestratorError('scout census')
    return payload


def _validate_seed(payload, scout):
    if payload.get('settled_nonempty_result_N') != SCOUT_NONEMPTY_N:
        raise OrchestratorError('seed N')
    if payload.get('overnight_finalized_nonempty_N') != SCOUT_NONEMPTY_N:
        raise OrchestratorError('seed N')
    if payload.get('settled_list_attempted_KXNCAAFGAME') != LIST_429:
        raise InventedResultRefused()
    if payload.get('method') != SCOUT_METHOD:
        raise OrchestratorError('seed')
    _parent_block(payload, True)
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
    if payload.get('captured_at_et') != SCOUT_FETCHED_AT:
        raise OrchestratorError('reget')
    if payload.get('method') != SCOUT_METHOD:
        raise OrchestratorError('reget')
    if payload.get('settled_nonempty_result_N') != SCOUT_NONEMPTY_N:
        raise OrchestratorError('reget N')
    if payload.get('list_http') != LIST_HTTP:
        raise InventedResultRefused()
    if 'results' in payload or 'pnl' in payload:
        raise ScorecardPromotionRefused()
    if 'parent_seeds_active_empty' in payload or 'artifacts' in payload:
        raise InventedResultRefused()
    if 'occurrence_datetime' in payload:
        raise InventedSoTRefused()
    _parent_block(payload, False)
    if payload.get('markets') != scout.get('markets'):
        raise OrchestratorError('reget markets')
    yes_n = 0
    no_n = 0
    for row in payload['markets']:
        if 'orderbook_fp' in row:
            raise InventedDepthRefused()
        if row.get('result') == 'yes':
            yes_n += 1
        elif row.get('result') == 'no':
            no_n += 1
        else:
            raise InventedResultRefused()
    if yes_n != YES_N or no_n != NO_N:
        raise OrchestratorError('reget census')
    return payload


def _panel_tickers(events):
    tickers = []
    for event in events:
        markets = event.get('market_tickers')
        if not isinstance(markets, list) or not markets:
            raise OrchestratorError('events')
        if event.get('market_count') != len(markets):
            raise OrchestratorError('events')
        for ticker in markets:
            if not isinstance(ticker, str) or not ticker.startswith(event.get('event_ticker') + '-'):
                raise InventedMarketRefused()
            tickers.append(ticker)
    return tickers


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
    if payload.get('purpose') != PANEL_PURPOSE or payload.get('cohort_kind') != COHORT_KIND:
        raise OrchestratorError('panel')
    if payload.get('admitted_at') is not None:
        raise OrchestratorError('admitted_at')
    if payload.get('stubbed_at_utc') != STUBBED_AT:
        raise OrchestratorError('panel')
    if payload.get('freeze_packet_sha256') != KERNEL_SHA256:
        raise OrchestratorError('panel')
    if payload.get('scout_cite') != SCOUT_CITE_PANEL:
        raise OrchestratorError('panel')
    if payload.get('football_oos_vs_000') is not True:
        raise OrchestratorError('panel')
    for key in ('results', 'pnl', 'volume'):
        if key not in payload or payload[key] is not None:
            raise ScorecardPromotionRefused()
    if 'markets' in payload:
        raise OrchestratorError('markets')
    admit = payload.get('admit_gate')
    if not isinstance(admit, dict):
        raise OrchestratorError('admit_gate')
    if admit.get('status') != ADMIT_GATE_STATUS or admit.get('admit_py_run') is not False:
        raise AdmitPyRefused()
    if admit.get('cohort_event_count') != PANEL_EVENTS_N:
        raise OrchestratorError('admit_gate')
    if admit.get('cohort_market_count') != PANEL_MARKET_TICKERS_N:
        raise OrchestratorError('admit_gate')
    binds = payload.get('binds') or {}
    if binds.get('fee_lab_sha') != FEEBOOK_COMMIT or binds.get('rails_lab_sha') != RAILS_COMMIT:
        raise OrchestratorError('panel binds')
    capture = payload.get('capture') or {}
    if capture.get('mode') != 'GET_only_public':
        raise LiveOrdersForbidden()
    if capture.get('host_allowlist') != [PANEL_HOST]:
        raise LiveOrdersForbidden()
    routes = capture.get('routes_allowlist')
    if not isinstance(routes, list) or not routes:
        raise LiveOrdersForbidden()
    for route in routes:
        if not isinstance(route, str) or not route.startswith('GET '):
            raise LiveOrdersForbidden()
        if OUT_OF_SCOPE_ROUTE in route or 'portfolio/orders' in route:
            raise LiveOrdersForbidden()
    schedule = capture.get('schedule') or {}
    if schedule.get('recorder_started') is True or schedule.get('admit_py_run') is True:
        raise AdmitPyRefused()
    events = payload.get('events')
    if not isinstance(events, list) or len(events) != PANEL_EVENTS_N:
        raise OrchestratorError('events')
    ineligible = payload.get('ineligible')
    if not isinstance(ineligible, list) or len(ineligible) != 1:
        raise OrchestratorError('ineligible')
    if ineligible[0].get('event_ticker') != INELIGIBLE_EVENT:
        raise OrchestratorError('ineligible')
    if ineligible[0].get('result') not in (None,):
        raise InventedResultRefused()
    seen_events = []
    for event in events:
        if not isinstance(event, dict):
            raise OrchestratorError('events')
        if event.get('admitted_at') is not None:
            raise OrchestratorError('admitted_at')
        if event.get('series_ticker') != SERIES:
            raise OrchestratorError('events')
        if event.get('panel_version') != PANEL_VERSION:
            raise PanelVersionRefused()
        if event.get('result') not in (None,) or 'result' in event:
            raise InventedResultRefused()
        if 'orderbook_fp' in event:
            raise InventedDepthRefused()
        for key in VOLUME_FIELDS:
            if key in event and event[key] is not None:
                raise InventedFillRefused()
        occ = event.get('kalshi_occurrence_datetime')
        if not isinstance(occ, str) or not occ.endswith('Z'):
            raise OccurrenceIntegrityRefused()
        seen_events.append(event.get('event_ticker'))
    if len(seen_events) != len(set(seen_events)):
        raise InventedMarketRefused()
    tickers = _panel_tickers(events)
    if len(tickers) != PANEL_MARKET_TICKERS_N or len(tickers) != len(set(tickers)):
        raise OrchestratorError('markets')
    for ticker in SETTLED_TICKERS:
        if ticker in tickers:
            raise InventedMarketRefused()
    by_event = {event.get('event_ticker'): event for event in events}
    for event_ticker, occurrence in PARENT_EVENT_OCCURRENCE.items():
        event = by_event.get(event_ticker)
        if event is None:
            raise OrchestratorError('parent event')
        if event.get('kalshi_occurrence_datetime') != occurrence:
            raise OccurrenceIntegrityRefused()
        if tuple(event.get('market_tickers')) != PARENT_EVENT_MARKETS[event_ticker]:
            raise InventedMarketRefused()
    for ticker in PARENT_SEED_TICKERS:
        if ticker not in tickers:
            raise OrchestratorError('parent seeds')
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
    if payload.get('prior_done') != PRIOR_DONE:
        raise OrchestratorError('conductor accept')
    if payload.get('orthogonal_pin') != ORTHOGONAL_PIN:
        raise OrchestratorError('conductor accept')
    if payload.get('implement_owner') != 'R&D Variants':
        raise OrchestratorError('conductor accept')
    if payload.get('conductor_cloud_kick') is not False:
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
    if payload.get('id') != 'EXAMINER_HOLD_S4_KXNCAAFGAME_SETTLED_JOIN_HARNESS_PRE_PR':
        raise OrchestratorError('examiner hold')
    if payload.get('status') != 'HOLD_PRE_PR' or payload.get('stub_ready') is not False:
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
    if payload.get('panel_version') != PANEL_VERSION:
        raise PanelVersionRefused()
    if payload.get('metrics_null') != list(HOLD_METRICS):
        raise ScorecardPromotionRefused()
    if payload.get('does_not_ungate') != list(DOES_NOT_UNGATE):
        raise UngateRefused()
    if payload.get('orthogonal_to') != list(ORTHOGONAL_TO):
        raise OrchestratorError('examiner hold')
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
    if payload.get('note_scout_N_not_copied_into_settled_join_n') is not True:
        raise ScorecardPromotionRefused()
    if payload.get('settled_list_http') != LIST_429 or payload.get('open_list_http') != LIST_429:
        raise InventedResultRefused()
    if payload.get('prior_nhl_rj_pr44_main') != BASE_COMMIT:
        raise OrchestratorError('examiner hold')
    if payload.get('prior_nhl_rj_accept_sha256') != NHL_ACCEPT_SHA256:
        raise OrchestratorError('examiner hold')
    return payload


def _panel_ticker_set(panel):
    return set(_panel_tickers(panel.get('events') or []))


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
    panel = _validate_panel(_read_pinned(PANEL_CAPTURE, PANEL_STUB_SHA256, PANEL_BYTES))
    panel_tickers = _panel_ticker_set(panel)
    scout = _validate_scout(_read_pinned(SCOUT_PATH, SCOUT_SHA256, SCOUT_BYTES), panel_tickers)
    _validate_seed(_read_pinned(SEED_PATH, SEED_SHA256, SEED_BYTES), scout)
    _validate_reget(_read_pinned(REGET_PATH, REGET_SHA256, REGET_BYTES), scout)
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
        'governance_s4_cites_present': FREEZE_GOV.is_file() and (SCOUT_CITE_DIR / SCOUT_NAME).is_file(),
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
    panel = _validate_panel(_read_pinned(PANEL_CAPTURE, PANEL_STUB_SHA256, PANEL_BYTES))
    return _validate_scout(_read_pinned(SCOUT_PATH, SCOUT_SHA256, SCOUT_BYTES), _panel_ticker_set(panel))


def load_seed():
    scout = load_scout()
    return _validate_seed(_read_pinned(SEED_PATH, SEED_SHA256, SEED_BYTES), scout)


def _settled_view(payload, scout):
    """In-memory settled index. This view is not written back to the reget file."""
    checked = _validate_reget(payload, scout)
    markets = {}
    for row in checked['markets']:
        markets[row['ticker']] = row
    view = dict(checked)
    view['markets'] = markets
    view['honest_gaps'] = list(HONEST_GAPS)
    view['parent_reget_occurrence_present'] = False
    return view


def load_reget():
    scout = load_scout()
    payload = _read_pinned(REGET_PATH, REGET_SHA256, REGET_BYTES)
    return _settled_view(payload, scout)


def list_429_gaps(reget=None):
    """Series, finalized, open, and events list 429 gaps. No ticker is attached."""
    if reget is None:
        reget = load_reget()
    if reget.get('list_http') != LIST_HTTP:
        raise InventedResultRefused()
    if reget.get('honest_gaps') != list(HONEST_GAPS):
        raise InventedResultRefused()
    markets = reget.get('markets') or {}
    for key in HONEST_GAPS:
        if key in markets:
            raise InventedResultRefused()
    for row in markets.values():
        if row.get('status') != 'finalized':
            raise InventedResultRefused()
        if row.get('source') in named_gap_files():
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
    """Settled rows whose scout, seed, and reget clocks agree.

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
    if tuple(scout_rows) != SETTLED_TICKERS and list(scout_rows) != list(SETTLED_TICKERS):
        raise OrchestratorError('occurrence rows')
    panel_tickers = _panel_ticker_set(panel)
    agreed = []
    for ticker in SETTLED_TICKERS:
        market = reget[ticker]
        assert_occurrence_pair(market, seed_rows[ticker])
        assert_occurrence_pair(market, scout_rows[ticker])
        for field in COMPARE_FIELDS:
            if market.get(field) != seed_rows[ticker].get(field):
                raise OrchestratorError('seed reget ' + field)
            if market.get(field) != scout_rows[ticker].get(field):
                raise OrchestratorError('scout reget ' + field)
        if ticker in panel_tickers or ticker in PARENT_SEED_TICKERS:
            raise InventedMarketRefused()
        agreed.append(ticker)
    if len(agreed) != SCOUT_NONEMPTY_N:
        raise OrchestratorError('occurrence rows')
    return tuple(agreed)


def parent_active_tickers(panel=None):
    """Parent SEP26 seeds that stay active with a null result.

    The reget has no occurrence_datetime for these tickers. The panel
    clock is the stub pin. This tuple is not occurrence_match_n.
    """
    if panel is None:
        panel = load_panel()
    else:
        _validate_panel(panel)
    reget = load_reget()
    if reget.get('parent_reget_occurrence_present') is not False:
        raise InventedSoTRefused()
    if 'occurrence_datetime' in reget:
        raise InventedSoTRefused()
    _parent_block(reget, False)
    by_event = {event.get('event_ticker'): event for event in panel.get('events') or []}
    agreed = []
    for ticker in PARENT_SEED_TICKERS:
        if reget['parent_seed_results'][ticker] is not None:
            raise InventedResultRefused()
        if reget['parent_seed_statuses'][ticker] != 'active':
            raise InventedResultRefused()
        event_ticker = None
        for candidate, markets in PARENT_EVENT_MARKETS.items():
            if ticker in markets:
                event_ticker = candidate
        event = by_event.get(event_ticker)
        if event is None:
            raise OrchestratorError('parent event')
        if event.get('kalshi_occurrence_datetime') != PARENT_EVENT_OCCURRENCE[event_ticker]:
            raise OccurrenceIntegrityRefused()
        if ticker not in event.get('market_tickers'):
            raise InventedMarketRefused()
        agreed.append(ticker)
    if len(agreed) != PARENT_SEED_N:
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
    parents = parent_active_tickers(panel)
    reget = load_reget()
    markets = reget['markets']
    rows = []
    for ticker in agreed:
        market = markets[ticker]
        result = market.get('result')
        source = market.get('source')
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
            'single_market_get': _source_kind(source) == 'market',
            'event_embed': _source_kind(source) == 'event',
        })
    for ticker in parents:
        rows.append({
            'key': ticker,
            'panel_ticker': ticker,
            'j0': 'parent_active_empty',
            'j1': 'parent_occurrence_not_on_reget',
            'result': None,
            'on_settled_list': False,
            'parent_seed': True,
            'single_market_get': False,
            'event_embed': False,
        })
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
            'event_embed': False,
        })
    if len(rows) != ROW_LABEL_N:
        raise OrchestratorError('row labels')
    passes = [row for row in rows if row['j0'] == 'nonempty_result_required_pass']
    active = [row for row in rows if row['j0'] == 'parent_active_empty']
    gaps = [row for row in rows if row['j0'] == 'honest_gap']
    if len(passes) != SCOUT_NONEMPTY_N or len(active) != PARENT_SEED_N or len(gaps) != HONEST_GAP_N:
        raise OrchestratorError('row labels')
    if any(row['on_settled_list'] for row in passes):
        raise InventedResultRefused()
    if sum(1 for row in passes if row['single_market_get']) != MARKET_GET_N:
        raise OrchestratorError('row labels')
    if sum(1 for row in passes if row['event_embed']) != EVENT_EMBED_N:
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
    if pins['governance_s4_cites_present'] is not True or pins['reget_cite_present'] is not True:
        raise OrchestratorError('governance cite')
    rows = structural_rows(panel)
    agreed = occurrence_agreement_tickers(panel)
    parent_agreed = parent_active_tickers(panel)
    if len(agreed) != SCOUT_NONEMPTY_N or len(parent_agreed) != PARENT_SEED_N:
        raise OrchestratorError('occurrence rows')
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
        'market_tickers_n': PANEL_MARKET_TICKERS_N,
        'settled_nonempty_result_N_scout': SCOUT_NONEMPTY_N,
        'scout_n_copied_into_settled_join_n': False,
        'yes_n': YES_N,
        'no_n': NO_N,
        'event_embed_n': EVENT_EMBED_N,
        'market_get_n': MARKET_GET_N,
        'parent_seed_tickers': list(PARENT_SEED_TICKERS),
        'parent_seeds_finalized_nonempty_N': PARENT_FINALIZED_N,
        'parent_seed_results': dict(PARENT_SEED_RESULTS),
        'seed_panel_result': None,
        'parent_sep26_active_empty': True,
        'parent_reget_occurrence_present': False,
        'settled_list_429': LIST_429,
        'open_list_429': LIST_429,
        'finalized_list_429': LIST_429,
        'events_settled_list_429': True,
        'list_429_backfilled': False,
        'http_counts': dict(HTTP_COUNTS),
        'honest_gap_n': HONEST_GAP_N,
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
        's4_fq_reopen': False,
        'ncaaf_fq_reopen': False,
        'nhl_rj_reopen': False,
        'c3_rj_reopen': False,
        'c5_rj_reopen': False,
        'r3p3_rj_reopen': False,
        'arm_b_touch': False,
        'conductor_cloud_kick': False,
        'admit_py_run': False,
        'does_not_ungate': list(DOES_NOT_UNGATE),
        's1_s2_r2p4_ungated': False,
        'examiner_status': 'HOLD_PRE_PR',
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
        'governance_s4_cites_present': True,
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
        's4_fq_reopen': False,
        'ncaaf_fq_reopen': False,
        'nhl_rj_reopen': False,
        'c3_rj_reopen': False,
        'c5_rj_reopen': False,
        'r3p3_rj_reopen': False,
        'fq_reopen': False,
        'cap_sr_reopen': False,
        'arm_b_touch': False,
        'conductor_cloud_kick': False,
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
    rows = structural_rows(panel)
    agreed = occurrence_agreement_tickers(panel)
    parent_agreed = parent_active_tickers(panel)
    extra = {
        'row_labels': rows,
        'occurrence_agreement_tickers': list(agreed),
        'parent_active_tickers': list(parent_agreed),
        'admitted_at': panel.get('admitted_at'),
        'event_count': len(panel.get('events') or []),
        'market_ticker_count': PANEL_MARKET_TICKERS_N,
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
