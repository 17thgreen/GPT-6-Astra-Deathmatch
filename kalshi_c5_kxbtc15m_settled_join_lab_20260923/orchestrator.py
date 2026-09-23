"""C5 KXBTC15M settled-resolution join harness.

Measurement only. One knob: join_gate. This module does not edit the
C5 honesty lab, the C3-RJ lab, feebook, rails, Cap-SR, or any FQ sibling.
It does not place orders, does not read Logan keys, does not run admit.py,
and does not write scorecard metrics. This is not live crypto trading.

The checkout freeze, scout reget, seed summary, panel stub, settled
reget, and accept match the attached sha256 values. The panel stub keeps
admitted_at null and result null. Finalized and closed list filters stay
the honest 429 gaps. Lee-Ready is refused. Settled results, depth, fills,
and PnL are not invented. Scout settled_nonempty_result_N is a pin and
is not copied into settled_join_n.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PARENT = ROOT.parent

LAB_DIRECTORY = 'kalshi_c5_kxbtc15m_settled_join_lab_20260923'
EXPERIMENT_ID = 'C5-KXBTC15M-SETTLED-RESOLUTION-JOIN-HARNESS'
FEATURE_FAMILY = 'C5-RJ'
SCOUT_PACKET = 'C5-KXBTC15M-SETTLED-JOIN'
PARENT_PACKET_ID = 'C5-KXBTC15M-MEAS'
PANEL_VERSION = '2026-09-22.c5-kxbtc15m-v0'
SCHEMA_ID = 'astra.registry.c5_kxbtc15m_panel.v0'
SERIES = 'KXBTC15M'
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
REGET_MARKET_N = 21
YES_N = 10
NO_N = 11
PANEL_EVENTS_N = 1
PANEL_MARKETS_N = 1
ROW_LABEL_N = 23
SETTLED_LIST_SOURCE = 'markets_settled_KXBTC15M_lim20.json'
SEED_SOURCE = 'market_KXBTC15M_26SEP222045_45.json'
SEED_TICKER = 'KXBTC15M-26SEP222045-45'
SEED_RESULT = 'no'
OPEN_TICKER = 'KXBTC15M-26SEP231530-30'
GAP_FINALIZED = 'status_finalized_list'
GAP_CLOSED = 'status_closed_list'
GAP_KEYS = (GAP_FINALIZED, GAP_CLOSED)
GAP_TEXT = '429 too_many_requests'
SCOUT_HONEST_GAPS = (
    'markets?status=finalized 429',
    'markets?status=closed 429',
)
SETTLED_LIST_ROUTE = 'GET /markets?series_ticker=KXBTC15M&status=settled&limit=20'
SEED_ROUTE = 'GET /markets/KXBTC15M-26SEP222045-45'
OPEN_LIST_ROUTE = 'GET /markets?series_ticker=KXBTC15M&status=open&limit=4'
REGET_FETCHED_AT = '2026-09-23 ~15:18 ET'
SCOUT_FETCHED_AT = '2026-09-23T15:18:00-04:00'
FEEBOOK_COMMIT = '22371178cb2663250b4762f328069571c48cb551'
RAILS_COMMIT = '6a28e0d6254327ea4e6451c781bec56215ac6cac'
BASE_COMMIT = '9eba15870e66dcde8ffc17a56c73016245a833c1'
FREEZE_SHA256 = '7f4b36eca39d43ee7403628c2e525d5980fa40bcfc906550c7f00bb06ffd4f21'
SCOUT_SHA256 = '7be17c44aef31abf7a0ab94938d0289f8766670ddacefdec566735818e044796'
SEED_SHA256 = 'b39c919809f709bcb81ff10a3d983b266bc7a1303c0de502c7c20be726415198'
PANEL_STUB_SHA256 = '60f613e8d775b66b9044ad31d2faf77bba84176f214a7bce599aa7a65b6905f8'
REGET_SHA256 = '319d6d3e394089fd21fefbfaa52c58166e78c2d781077a3f876331d2c54de617'
ACCEPT_SHA256 = 'e116bbcb5f9518e6008ef412c8ff212a3170d0e3f26eb978f07a204b327aba7d'
FROZEN_SHA256 = '31db09b93b09dccd449ad2ade56838eb6ccb531990209a5cbe85e91703dfeffc'
EMPTY_SHA256 = '94f5e75928b530516143fcf6b23c6b532701c3afb5da84327adf550a4046d4e3'
SOURCE_PINS_SHA256 = '3b8ca87c3ee89b23aa6cda2b90176060ebb3ebfe4c6b68dbeba917adeb44cb55'
FREEZE_BYTES = 5585
SCOUT_BYTES = 6908
SEED_BYTES = 6675
PANEL_BYTES = 6679
REGET_BYTES = 59151
ACCEPT_BYTES = 1541
FROZEN_BYTES = 1040
EMPTY_BYTES = 166
SOURCE_PINS_BYTES = 4117
ACCEPT_STAMPED_AT = '2026-09-23T15:21:00-04:00'
FROZEN_STAMPED_AT = '2026-09-23T15:18:00-04:00'
EMPTY_NOTE = 'pre-ACCEPT empty; C5-RJ measurement join only'
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
    'C5_honesty_reopen',
    'C3_RJ_reopen',
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
    'list_429_backfill': 'finalized and closed list 429 backfill is refused',
    'open_ticker_invent': 'invented open ticker market is refused',
    'fq_reopen': 'FQ reopen is refused',
    'eth_fq_reopen': 'ETH-FQ reopen is refused',
    'nhl_fq_reopen': 'NHL-FQ reopen is refused',
    'cpi_fq_reopen': 'CPI-FQ reopen is refused',
    'atp_fq_reopen': 'ATP-FQ reopen is refused',
    'cap_sr_reopen': 'Cap-SR reopen is refused',
    'empty_ob_reopen': 'EMPTY-OB reopen is refused',
    'c5_honesty_reopen': 'C5 honesty reopen is refused',
    'c3_rj_reopen': 'C3-RJ reopen is refused',
    'arm_b': 'Arm B is refused',
    'q7_arm_b': 'Arm B is refused',
    'admit_py': 'admit.py is refused',
    'live_orders': 'live orders are refused',
    'logan_keys': 'Logan keys are refused',
    'live_crypto_trading': 'live crypto trading is refused',
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
    'lab/astra-capture/c5-kxbtc15m/panel_stub.json',
    'lab/governance/astra/packets/r3_p2_queue_position/results/demo_queue_sample_series.json',
)
FREEZE_NAME = 'C5_KXBTC15M_SETTLED_RESOLUTION_JOIN_HARNESS_FREEZE_2026-09-23.md'
SCOUT_NAME = 'scout_settled_rejoin_C5_KXBTC15M.json'
SEED_NAME = 'SEED_SETTLED_SUMMARY.json'
PANEL_ALIAS = 'C5_KXBTC15M_PANEL_STUB_2026-09-22.json'
REGET_NAME = 'settled_reget_2026-09-23.json'
ACCEPT_NAME = 'CONDUCTOR_ACCEPT_C5_KXBTC15M_SETTLED_JOIN_HARNESS_2026-09-23.json'
SOURCE_PINS_NAME = 'SOURCE_PINS.json'
LAB_BUNDLE = ROOT / 'C5_KXBTC15M_SETTLED_RESOLUTION_JOIN_HARNESS'
GOVERNANCE_TREE = PARENT / 'lab' / 'governance' / 'astra'
C5_SCOUT_CITE = GOVERNANCE_TREE / 'packets' / 'scout_c5_settled_rejoin_2026-09-23'
C5_PANEL_CITE = GOVERNANCE_TREE / 'packets' / 'C5_KXBTC15M_PANEL_STUB_2026-09-22.json'
PACKET = ROOT / FREEZE_NAME
SCOUT_PATH = ROOT / SCOUT_NAME
SEED_PATH = ROOT / SEED_NAME
REGET_PATH = ROOT / REGET_NAME
CONDUCTOR_ACCEPT = ROOT / ACCEPT_NAME
FROZEN_EXPERIMENT = ROOT / 'FROZEN_EXPERIMENT.json'
EMPTY_RESULTS = ROOT / 'results' / 'EMPTY_RESULTS.json'
SOURCE_PINS = ROOT / SOURCE_PINS_NAME
PANEL_CAPTURE = PARENT / 'lab' / 'astra-capture' / 'c5-kxbtc15m' / 'panel_stub.json'
PANEL_ADMITTED = PARENT / 'lab' / 'astra-capture' / 'c5-kxbtc15m' / 'panel_admitted.json'
REGET_CITE = PARENT / 'lab' / 'astra-capture' / 'c5-kxbtc15m' / REGET_NAME
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
    """The panel file is not the pinned C5 seed."""

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
    """The finalized and closed 429 list gaps stay gaps. Nothing is written."""
    del which, result, occurrence_datetime
    raise InventedResultRefused()


def invent_open_ticker(ticker=None, result=None):
    """The cited open ticker has no settled-reget market object."""
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
    if label == 'live_orders' or label == 'live_crypto_trading':
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
    if payload.get('scout_n_copied_into_settled_join_n') is not False:
        raise ScorecardPromotionRefused()
    if payload.get('seed_ticker') != SEED_TICKER:
        raise OrchestratorError('source pins')
    if payload.get('seed_reget_status') != 'finalized' or payload.get('seed_reget_result') != SEED_RESULT:
        raise InventedResultRefused()
    if payload.get('seed_panel_result') is not None:
        raise InventedResultRefused()
    if payload.get('open_ticker_cited') != OPEN_TICKER or payload.get('open_ticker_market_invented') is not False:
        raise InventedMarketRefused()
    if payload.get('finalized_list_429') != GAP_TEXT or payload.get('closed_list_429') != GAP_TEXT:
        raise OrchestratorError('source pins')
    if payload.get('finalized_closed_429_backfilled') is not False:
        raise InventedResultRefused()
    if payload.get('fee_import_used') is not False or payload.get('rails_import_used') is not False:
        raise OrchestratorError('source pins')
    if payload.get('fee_arms') is not False:
        raise OrchestratorError('source pins')
    if payload.get('feebook_commit_fixed_not_loaded') != FEEBOOK_COMMIT:
        raise OrchestratorError('source pins')
    if payload.get('rails_commit_fixed_not_loaded') != RAILS_COMMIT:
        raise OrchestratorError('source pins')
    if payload.get('governance_c5_cites') != 'absent':
        raise OrchestratorError('source pins')
    if payload.get('does_not_run_admit_py') is not True:
        raise AdmitPyRefused()
    if payload.get('base_commit') != BASE_COMMIT:
        raise OrchestratorError('source pins')
    if payload.get('lee_ready') != 'REFUSED':
        raise LeeReadyRefused()
    if payload.get('c5_honesty_reopen') is not False or payload.get('c3_rj_reopen') is not False:
        raise OrchestratorError('source pins')
    if payload.get('cap_sr_reopen') is not False or payload.get('fq_reopen') is not False:
        raise OrchestratorError('source pins')
    if payload.get('eth_fq_reopen') is not False or payload.get('empty_ob_reopen') is not False:
        raise OrchestratorError('source pins')
    if payload.get('arm_b_touch') is not False or payload.get('live_orders') is not False:
        raise OrchestratorError('source pins')
    if payload.get('not_live_crypto_trading') is not True:
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
    if payload.get('series') != [SERIES]:
        raise OrchestratorError('scout')
    if payload.get('settled_nonempty_result_N') != SCOUT_NONEMPTY_N:
        raise OrchestratorError('scout N')
    if payload.get('settled_list_limit') != SCOUT_NONEMPTY_N:
        raise OrchestratorError('scout N')
    if payload.get('settled_list_cursor_present') is not True:
        raise OrchestratorError('scout')
    if payload.get('parent_seed_finalized_nonempty') is not True:
        raise OrchestratorError('scout')
    if payload.get('open_list_n') != 1 or payload.get('open_tickers') != [OPEN_TICKER]:
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
    seed_rows = []
    for row in markets:
        if not isinstance(row, dict):
            raise OrchestratorError('scout market')
        if row.get('nonempty_result') is not True:
            raise InventedResultRefused()
        if row.get('status') != 'finalized' or row.get('result') not in FINALIZED_RESULTS:
            raise InventedResultRefused()
        if not isinstance(row.get('ticker'), str) or row.get('ticker') == OPEN_TICKER:
            raise InventedMarketRefused()
        if row.get('source') == SETTLED_LIST_SOURCE:
            list_rows.append(row)
        elif row.get('source') == SEED_SOURCE:
            seed_rows.append(row)
        else:
            raise OrchestratorError('scout row')
    if len(list_rows) != SCOUT_NONEMPTY_N or len(seed_rows) != 1:
        raise OrchestratorError('scout census')
    seed_row = seed_rows[0]
    if seed_row.get('ticker') != SEED_TICKER or seed_row.get('result') != SEED_RESULT:
        raise InventedResultRefused()
    if OPEN_TICKER in {row.get('ticker') for row in markets}:
        raise InventedMarketRefused()
    return payload


def _validate_seed(payload, scout):
    if payload.get('settled_nonempty_result_N') != SCOUT_NONEMPTY_N:
        raise OrchestratorError('seed N')
    if payload.get('settled_list_attempted') != SCOUT_NONEMPTY_N:
        raise OrchestratorError('seed attempted')
    if payload.get('parent_seed_ticker') != SEED_TICKER:
        raise OrchestratorError('seed ticker')
    if payload.get('parent_seed_status') != 'finalized' or payload.get('parent_seed_result') != SEED_RESULT:
        raise InventedResultRefused()
    if payload.get('parent_seed_nonempty_result') is not True:
        raise InventedResultRefused()
    if payload.get('open_list_n') != 1:
        raise OrchestratorError('seed')
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
    if payload.get('series_ticker') != SERIES:
        raise OrchestratorError('reget series')
    if payload.get('fetched_at_et') != REGET_FETCHED_AT:
        raise OrchestratorError('reget')
    routes = payload.get('routes')
    if routes != {
        'settled_list': SETTLED_LIST_ROUTE,
        'seed_ticker': SEED_ROUTE,
        'open_list': OPEN_LIST_ROUTE,
    }:
        raise OrchestratorError('reget routes')
    gaps = payload.get('honest_gaps')
    if gaps != {GAP_FINALIZED: GAP_TEXT, GAP_CLOSED: GAP_TEXT}:
        raise InventedResultRefused()
    if payload.get('settled_list_nonempty_result_N') != SCOUT_NONEMPTY_N:
        raise OrchestratorError('reget N')
    if payload.get('seed_ticker_nonempty_result') is not True:
        raise InventedResultRefused()
    markets = payload.get('markets')
    if not isinstance(markets, dict) or len(markets) != REGET_MARKET_N:
        raise OrchestratorError('reget markets')
    for key in GAP_KEYS:
        if key in markets:
            raise InventedResultRefused()
    if OPEN_TICKER in markets:
        raise InventedMarketRefused()
    scout_rows = {}
    for row in scout.get('markets') or []:
        scout_rows[row['ticker']] = row
    if set(scout_rows) != set(markets):
        raise InventedMarketRefused()
    yes_n = 0
    no_n = 0
    for ticker, market in markets.items():
        if not isinstance(market, dict) or market.get('ticker') != ticker:
            raise InventedMarketRefused()
        if 'orderbook_fp' in market:
            raise InventedDepthRefused()
        scout_row = scout_rows[ticker]
        for field in COMPARE_FIELDS:
            if market.get(field) != scout_row.get(field):
                raise OrchestratorError('scout reget ' + field)
        if market.get('status') != 'finalized' or market.get('result') not in FINALIZED_RESULTS:
            raise InventedResultRefused()
        if scout_row.get('nonempty_result') is not True:
            raise InventedResultRefused()
        if market.get('result') == 'yes':
            yes_n += 1
        else:
            no_n += 1
    if yes_n != YES_N or no_n != NO_N:
        raise OrchestratorError('reget census')
    seed_market = markets.get(SEED_TICKER)
    if not isinstance(seed_market, dict) or seed_market.get('result') != SEED_RESULT:
        raise InventedResultRefused()
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
    event = events[0]
    if not isinstance(event, dict):
        raise OrchestratorError('events')
    if event.get('admitted_at') is not None or event.get('panel_version') != PANEL_VERSION:
        raise OrchestratorError('admitted_at')
    if event.get('event_ticker') != 'KXBTC15M-26SEP222045':
        raise OrchestratorError('events')
    if event.get('market_tickers') != [SEED_TICKER]:
        raise InventedMarketRefused()
    market = markets[0]
    if not isinstance(market, dict):
        raise OrchestratorError('market')
    if market.get('admitted_at') is not None or market.get('panel_version') != PANEL_VERSION:
        raise OrchestratorError('admitted_at')
    if market.get('result') is not None:
        raise InventedResultRefused()
    if market.get('status_at_stub') != 'active':
        raise InventedResultRefused()
    if market.get('market_ticker') != SEED_TICKER or market.get('event_ticker') != event.get('event_ticker'):
        raise InventedMarketRefused()
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
    if C5_SCOUT_CITE.exists():
        raise OrchestratorError('governance cite')
    if C5_PANEL_CITE.exists():
        _assert_digest(C5_PANEL_CITE, PANEL_STUB_SHA256, PANEL_BYTES)
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
    cites_present = C5_SCOUT_CITE.exists() or C5_PANEL_CITE.is_file()
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
        'governance_c5_cites_present': cites_present,
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


def list_429_gaps(reget=None):
    """The two list-filter gaps. No ticker and no result are attached."""
    if reget is None:
        reget = load_reget()
    gaps = reget.get('honest_gaps')
    if gaps != {GAP_FINALIZED: GAP_TEXT, GAP_CLOSED: GAP_TEXT}:
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
    """Tickers whose reget and seed timestamps already agree.

    The parent seed ticker also matches the panel stub. The 429 list gaps
    and the cited open ticker are absent. This list is not occurrence_match_n.
    """
    if panel is None:
        panel = load_panel()
    else:
        _validate_panel(panel)
    reget = load_reget()['markets']
    seed_rows = {row['ticker']: row for row in load_seed()['markets']}
    by_ticker = {market.get('market_ticker'): market for market in panel.get('markets') or []}
    if set(by_ticker) != {SEED_TICKER}:
        raise InventedMarketRefused()
    agreed = []
    for ticker, market in reget.items():
        if ticker not in seed_rows:
            raise InventedMarketRefused()
        assert_occurrence_pair(market, seed_rows[ticker])
        if ticker == SEED_TICKER:
            panel_value = by_ticker[ticker].get('occurrence_datetime')
            if panel_value != market.get('occurrence_datetime'):
                raise OccurrenceIntegrityRefused()
        agreed.append(ticker)
    if OPEN_TICKER in agreed or SEED_TICKER not in agreed:
        raise InventedMarketRefused()
    if len(agreed) != REGET_MARKET_N:
        raise OrchestratorError('occurrence rows')
    return tuple(sorted(agreed))


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
        if key not in agreed:
            raise OccurrenceIntegrityRefused()
        result = market.get('result')
        if market.get('status') != 'finalized' or result not in FINALIZED_RESULTS:
            raise InventedResultRefused()
        source = seed_rows[key].get('source')
        on_list = source == SETTLED_LIST_SOURCE
        parent_seed = key == SEED_TICKER and source == SEED_SOURCE
        if on_list == parent_seed:
            raise OrchestratorError('row source')
        rows.append({
            'key': key,
            'panel_ticker': key if parent_seed else None,
            'j0': 'nonempty_result_required_pass',
            'j1': 'occurrence_datetime_match',
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
    if seed_rows_out != [row for row in passes if row['key'] == SEED_TICKER]:
        raise OrchestratorError('row labels')
    if len(seed_rows_out) != 1 or seed_rows_out[0]['result'] != SEED_RESULT:
        raise InventedResultRefused()
    if OPEN_TICKER in {row['key'] for row in rows}:
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
    if pins['governance_c5_cites_present'] is not False:
        raise OrchestratorError('governance cite')
    rows = structural_rows(panel)
    agreed = occurrence_agreement_tickers(panel)
    if len(agreed) != REGET_MARKET_N:
        raise OrchestratorError('occurrence rows')
    if OPEN_TICKER in agreed or SEED_TICKER not in agreed:
        raise InventedMarketRefused()
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
        'seed_ticker': SEED_TICKER,
        'seed_reget_result': SEED_RESULT,
        'seed_panel_result': panel['markets'][0].get('result'),
        'open_ticker_cited': OPEN_TICKER,
        'open_ticker_market_invented': False,
        'finalized_list_429': GAP_TEXT,
        'closed_list_429': GAP_TEXT,
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
        'not_live_crypto_trading': True,
        'cap_sr_reopen': False,
        'fq_reopen': False,
        'eth_fq_reopen': False,
        'empty_ob_reopen': False,
        'c5_honesty_reopen': False,
        'c3_rj_reopen': False,
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
        'governance_c5_cites_present': False,
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
        'c5_honesty_reopen': False,
        'c3_rj_reopen': False,
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
