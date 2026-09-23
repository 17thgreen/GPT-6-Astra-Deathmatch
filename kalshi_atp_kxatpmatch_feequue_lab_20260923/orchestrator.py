"""ATP KXATPMATCH fee and queue honesty harness.

Measurement only. Imports the R1-P1 feebook and the R1-P5 rails through the
R2-P1 hygiene helpers. This module does not edit those labs, does not place
orders, does not read Logan keys, and does not write scorecard metrics.

The checkout freeze, scout hunt, and panel stub match the attached sha256
values. Panel markets are the scout-hunt objects. A missing
occurrence_datetime stays missing. Fill density is not invented.
Lee-Ready is refused. The NFL 000 path is a pointer only.
"""
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PARENT = ROOT.parent
FEEBOOK_DIR = PARENT / 'kalshi_feebook_lab_20260922'
RAILS_DIR = PARENT / 'kalshi_rails_lab_20260922'
HYGIENE_PATH = PARENT / 'kalshi_r2p1_hygiene_000_lab_20260922' / 'hygiene.py'
for _path in (FEEBOOK_DIR, RAILS_DIR):
    if str(_path) not in sys.path:
        sys.path.insert(0, str(_path))

import feebook
import rails

LAB_DIRECTORY = 'kalshi_atp_kxatpmatch_feequue_lab_20260923'
EXPERIMENT_ID = 'ATP-KXATPMATCH-FEEQUEUE-HARNESS'
FEATURE_FAMILY = 'ATP-FQ'
SERIES = 'KXATPMATCH'
SCHEMA_ID = 'astra.panel_stub.v0'
PANEL_VERSION = '2026-09-23.atp-kxatpmatch-v0'
COHORT_KIND = 'scout_hunt_subset'
STUB_STATUS = 'NOT_ADMITTED'
PURPOSE = 'GET-only ATP match ML fee+queue honesty harness seed from Scout hunt bytes'
STUBBED_AT = '2026-09-23T14:12:00-04:00'
SCOUT_CITE = 'packets/scout_cashcow_hunt_2026-09-22/scout_hunt_KXATPMATCH.json'
KNOB = 'analysis_slice'
ATPA0 = 'ATPA0'
ATPA1 = 'ATPA1'
ARMS = (ATPA0, ATPA1)
ANALYSIS_SLICE = {
    ATPA0: 'maker_vs_taker_native',
    ATPA1: 'content_fresh_vs_stale_bin',
}
FEEBOOK_COMMIT = '22371178cb2663250b4762f328069571c48cb551'
RAILS_COMMIT = '6a28e0d6254327ea4e6451c781bec56215ac6cac'
BASE_COMMIT = '6e55a99790f4cc09a437d2e16ccf4e8e826a154b'
FREEZE_SHA256 = '4d4ce944946e72dd40567d14388fe11c6145fbbb32505a880bcf80a4c8b4dffe'
SCOUT_SHA256 = '14c99ec8ea00bae507a21d0e6a1879fb94d32ef69ad4b5e3b40a9952821e5da7'
PANEL_STUB_SHA256 = 'ed041c502d1f775d33c44bf900ac91b1339d99045bddd2052edd09a139ae2d3f'
CONDUCTOR_STAMP_SHA256 = 'ae38a793f9478bb4c09dedd2ae63f917f850e9b604f1670716dceb05f433b73b'
PRE_ACCEPT_EMPTY_SHA256 = '88395e7bba510262bcac68565dbacc82ec52400335f5528135bd50fdaa06925b'
CONDUCTOR_ACCEPT_SHA256 = 'b038994585e19d28d014882594239eafc2657b6de7da105f238c90d49954bd8b'
EXAMINER_HOLD_SHA256 = '503ed0e734fe16a87a989193f56f2a61f83a2d123713504795bee8da6e8cdb82'
SOURCE_PINS_SHA256 = 'b9dadbf3a844c20f11468669addb90a22c7f72e28921a123f433f1547a6bbe72'
FREEZE_BYTES = 4893
SCOUT_BYTES = 112834
PANEL_BYTES = 35140
STAMP_BYTES = 498
PRE_ACCEPT_BYTES = 121
ACCEPT_BYTES = 1883
HOLD_BYTES = 817
SCOUT_MARKETS_N = 48
SCOUT_EVENTS_N = 24
PANEL_EVENTS_N = 6
PANEL_MARKETS_N = 12
MISSING_OCCURRENCE_N = 0
FEE_CHANNEL_CITE = 'quadratic_with_maker_fees'
NFL_000_POINTER = 'nfl_factorial_lab_20260921/SHADOW_CANDIDATE_FREEZE.json'
NFL_POINTER_SERIES = 'KXNFLGAME'
FEEBOOK_PIN = 'kalshi_feebook_lab_20260922/@22371178cb2663250b4762f328069571c48cb551'
RAILS_PIN = 'kalshi_rails_lab_20260922/@6a28e0d6254327ea4e6451c781bec56215ac6cac'
NEAREST_DEAD_CARD = 'invent_depth_fills_fill_density_OR_invent_occurrence_datetime_SoT'
PUBLIC_HOST = 'api.elections.kalshi.com'
OUT_OF_SCOPE_ROUTE = 'POST /portfolio/orders'
SCORECARD_FIELDS = (
    'maker_vs_taker_roi_delta',
    'fresh_vs_stale_gap',
    'settled_join_n',
    'n_books',
)
OUTPUT_KEYS = SCORECARD_FIELDS + ('results', 'pnl')
PUBLIC_TAKER_FIELDS = ('taker_outcome_side', 'taker_book_side', 'taker_side')
BOOK_TO_OUTCOME = {'bid': 'yes', 'ask': 'no'}
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
    'source_markets_n': SCOUT_MARKETS_N,
    'source_events_n': SCOUT_EVENTS_N,
}
DOES_NOT_UNGATE = ('S1', 'S2', 'R2-P4')
FEE_LITERAL_KEYS = ('fee', 'fee_cost', 'fee_dollars', 'maker_fee', 'taker_fee')
FILL_DENSITY_KEYS = ('fill_density', 'fills_per_hour', 'invented_fill_density')
DEPTH_KEYS = (
    'orderbook_fp',
    'yes_bid_size_fp',
    'yes_ask_size_fp',
    'no_bid_size_fp',
    'depth',
)
ADVERSARY_LABELS = {
    'lee_ready': 'Lee-Ready is refused on every input',
    'live_orders': 'live orders are refused',
    'logan_keys': 'Logan keys are refused',
    'invented_pnl': 'invented pnl is refused',
    'invented_fills': 'invented fills are refused',
    'invented_fill_density': 'invented fill density is refused',
    'invented_occurrence_datetime': 'invented occurrence_datetime is refused',
    'invented_depth': 'invented depth is refused',
    'invented_markets': 'invented markets are refused',
    'q6_retune': 'Q6-000 retune is refused',
    '000': 'Q6-000 retune is refused',
    'qf_reopen': 'queue-fragility reopen is refused',
    'cap_sr_reopen': 'Cap-SR reopen is refused',
    'cap_sr_fx_reopen': 'Cap-SR-FX reopen is refused',
    'l2_reopen': 'L2 reopen is refused',
    'l2_cat_reopen': 'L2-CAT reopen is refused',
    'l2_sf_reopen': 'L2-SF reopen is refused',
    'empty_ob_reopen': 'EMPTY-OB reopen is refused',
    'sot_id_reopen': 'SOT-ID reopen is refused',
    'nhl_fq_reopen': 'NHL-FQ reopen is refused',
    'cpi_fq_reopen': 'CPI-FQ reopen is refused',
    'prop_lq_reopen': 'PROP-LQ reopen is refused',
    'admit_py': 'admit.py is refused',
    'atl_gb': 'ATL@GB is refused',
    'claim_s1_green': 'S1 green is not claimed',
    'signal_port': 'NFL 000 signal port is refused',
}
DOES_NOT_MODIFY = (
    'kalshi_feebook_lab_20260922',
    'kalshi_rails_lab_20260922',
    'kalshi_r2p1_hygiene_000_lab_20260922',
    'kalshi_queue_fragility_000_lab_20260922',
    'kalshi_soft_blended_reserves_000_lab_20260923',
    'kalshi_cap_sr_effects_000_lab_20260923',
    'kalshi_c1_kxufcfight_honesty_lab_20260922',
    'kalshi_c1_empty_ob_lab_20260923',
    'kalshi_c2_kxnhlgame_feequue_lab_20260923',
    'kalshi_c3_kxhighny_bordering_lab_20260923',
    'kalshi_c4_kxcpi_feequue_lab_20260923',
    'kalshi_c5_kxbtc15m_honesty_lab_20260923',
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
)
FREEZE_NAME = 'ATP_KXATPMATCH_FEEQUEUE_HARNESS_FREEZE_2026-09-23.md'
SCOUT_NAME = 'scout_hunt_KXATPMATCH.json'
PANEL_ALIAS = 'ATP_KXATPMATCH_PANEL_STUB_2026-09-23.json'
STAMP_NAME = 'CONDUCTOR_FROZEN_EXPERIMENT.json'
PRE_ACCEPT_NAME = 'PRE_ACCEPT_EMPTY_RESULTS.json'
ACCEPT_NAME = 'CONDUCTOR_ACCEPT_ATP_KXATPMATCH_FEEQUEUE_HARNESS_2026-09-23.json'
HOLD_NAME = 'EXAMINER_HOLD_ATP_KXATPMATCH_FEEQUEUE_HARNESS_PRE_PR_2026-09-23.json'
SOURCE_PINS_NAME = 'SOURCE_PINS.json'
PACKET = ROOT / FREEZE_NAME
LAB_BUNDLE = ROOT / 'ATP_KXATPMATCH_FEEQUEUE_HARNESS'
GOVERNANCE_BUNDLE = PARENT / 'packets' / 'ATP_KXATPMATCH_FEEQUEUE_HARNESS'
GOVERNANCE_TREE = PARENT / 'lab' / 'governance' / 'astra' / 'packets'
SCOUT_CANONICAL = PARENT / 'packets' / 'scout_cashcow_hunt_2026-09-22' / SCOUT_NAME
FROZEN_EXPERIMENT = ROOT / 'FROZEN_EXPERIMENT.json'
EMPTY_RESULTS = ROOT / 'results' / 'EMPTY_RESULTS.json'
SOURCE_PINS = ROOT / SOURCE_PINS_NAME
CONDUCTOR_STAMP = ROOT / STAMP_NAME
PRE_ACCEPT_EMPTY = ROOT / PRE_ACCEPT_NAME
CONDUCTOR_ACCEPT = ROOT / ACCEPT_NAME
EXAMINER_HOLD = ROOT / HOLD_NAME
PANEL_STUB = PARENT / 'lab' / 'astra-capture' / 'atp-kxatpmatch' / 'panel_stub.json'
PANEL_ADMITTED = PARENT / 'lab' / 'astra-capture' / 'atp-kxatpmatch' / 'panel_admitted.json'
NFL_POINTER_PATH = PARENT / NFL_000_POINTER
SYNTHETIC_TRADES = ROOT / 'fixtures' / 'synthetic_native_trades.json'
SYNTHETIC_FRESH = ROOT / 'fixtures' / 'synthetic_fresh_queue.json'
_SCOUT_INDEX = None


class OrchestratorError(Exception):
    """A pin failed or a measurement write was requested."""


class ScorecardPromotionRefused(OrchestratorError):
    """Filled measurement fields stay out of the freeze packet."""

    def __init__(self):
        super().__init__('scorecard metrics stay null until Examiner')


class PreAcceptEmptyRefused(OrchestratorError):
    """The attached pre-ACCEPT empty payload is not a scorecard."""

    def __init__(self):
        super().__init__('pre-ACCEPT empty')


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
    """Lee-Ready is refused on every input."""

    def __init__(self):
        super().__init__('Lee-Ready refused')


class SignalPortRefused(OrchestratorError):
    """The NFL 000 file is a pointer. No signal is read from it."""

    def __init__(self):
        super().__init__('NFL 000 signal port refused')


class S1GreenClaimRefused(OrchestratorError):
    """This packet does not claim S1 green."""

    def __init__(self):
        super().__init__('S1 green is not claimed')


class UngateRefused(OrchestratorError):
    """S1, S2, and R2-P4 stay gated."""

    def __init__(self):
        super().__init__('does not ungate S1 S2 R2-P4')


class ExaminerNotReady(OrchestratorError):
    """Examiner stays NOT_SCORED until after merge and Clock admit."""

    def __init__(self):
        super().__init__('Examiner NOT_SCORED')


class TakerFieldRefused(OrchestratorError):
    """Native taker fields are missing or disagree."""

    def __init__(self, reason):
        super().__init__(reason)


class PanelVersionRefused(OrchestratorError):
    """The panel file is not the pinned ATP seed."""

    def __init__(self):
        super().__init__('panel_version')


class ShadowFeeLiteralRefused(OrchestratorError):
    """A fee quote bypassed the examiner feebook formula."""

    def __init__(self):
        super().__init__('shadow fee literal')


class InventedFillRefused(OrchestratorError):
    """A fill, settlement, or inventory value was invented."""

    def __init__(self):
        super().__init__('invented fill')


class InventedFillDensityRefused(OrchestratorError):
    """Fill density is not derived from the public tape."""

    def __init__(self):
        super().__init__('invented fill density')


class InventedSoTRefused(OrchestratorError):
    """occurrence_datetime is not invented when the source omits it."""

    def __init__(self):
        super().__init__('invented occurrence_datetime')


class InventedDepthRefused(OrchestratorError):
    """Depth was requested from a market quote or a fabricated ladder."""

    def __init__(self):
        super().__init__('invented depth')


class InventedMarketRefused(OrchestratorError):
    """A market is outside the authentic scout hunt."""

    def __init__(self):
        super().__init__('invented market')


class UnknownSlice(OrchestratorError):
    """The only knob is the two named analysis slices."""

    def __init__(self):
        super().__init__('analysis_slice')


def _load_hygiene():
    spec = importlib.util.spec_from_file_location('atp_kxatpmatch_hygiene', HYGIENE_PATH)
    if spec is None or spec.loader is None:
        raise OrchestratorError('hygiene import')
    module = importlib.util.module_from_spec(spec)
    sys.modules['atp_kxatpmatch_hygiene'] = module
    spec.loader.exec_module(module)
    return module


hygiene = _load_hygiene()


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


def port_nfl_000_signal(payload=None):
    """Pointer only. Every read of a 000 signal is refused."""
    if payload is None or isinstance(payload, (dict, str, int, float, list, tuple)):
        raise SignalPortRefused()
    raise SignalPortRefused()


def claim_s1_green():
    """S1 empty-events stays WAIT. This packet does not claim it green."""
    raise S1GreenClaimRefused()


def ungate(name):
    """S1, S2, and R2-P4 stay queued."""
    if name in DOES_NOT_UNGATE:
        raise UngateRefused()
    raise OrchestratorError('ungate')


def quote_depth(market):
    """Public size fields are not a depth ladder and are not n_books."""
    if market is None or isinstance(market, (dict, str, list, tuple)):
        raise InventedDepthRefused()
    raise InventedDepthRefused()


def assign_fill_density(market, value=None):
    """Public volume is not rewritten as a fill density."""
    del market, value
    raise InventedFillDensityRefused()


def assign_occurrence(market, value=None):
    """A missing occurrence_datetime stays missing."""
    del market, value
    raise InventedSoTRefused()


def settled_join(panel):
    """No settlement join is published. The metric stays null."""
    if not isinstance(panel, dict):
        raise OrchestratorError('panel')
    if panel.get('results') is not None or panel.get('pnl') is not None:
        raise InventedFillRefused()
    return None


def refuse_adversary(label):
    """Named refuse labels. Nothing is traded."""
    if label not in ADVERSARY_LABELS:
        raise OrchestratorError('adversary label')
    if label == 'lee_ready':
        raise LeeReadyRefused()
    if label == 'signal_port':
        raise SignalPortRefused()
    if label == 'invented_depth':
        raise InventedDepthRefused()
    if label == 'invented_markets':
        raise InventedMarketRefused()
    if label == 'invented_fill_density':
        raise InventedFillDensityRefused()
    if label == 'invented_occurrence_datetime':
        raise InventedSoTRefused()
    if label == 'claim_s1_green':
        raise S1GreenClaimRefused()
    raise AdversaryRefused(ADVERSARY_LABELS[label])


def infer_lee_ready(row):
    """Lee-Ready has no success path. Every input is refused."""
    if row is None or isinstance(row, (dict, str, int, float, list, tuple)):
        raise LeeReadyRefused()
    raise LeeReadyRefused()


def _lee_ready_requested(row):
    value = row.get('lee_ready')
    if value is True:
        return True
    if isinstance(value, str) and value not in ('REFUSED',):
        return True
    classifier = row.get('classifier')
    if isinstance(classifier, str) and classifier.lower().replace('_', '-') in (
        'lee-ready',
        'leeready',
    ):
        return True
    if row.get('aggressor_inference') is not None:
        return True
    return False


def _agree(current, value):
    if current is None:
        return value
    if current != value:
        raise TakerFieldRefused('taker_* fields disagree')
    return current


def _refuse_fee_literal(row):
    for key in FEE_LITERAL_KEYS:
        if key in row and row[key] is not None:
            raise ShadowFeeLiteralRefused()


def _refuse_depth_keys(row):
    for key in DEPTH_KEYS:
        if key in row and row[key] is not None:
            raise InventedDepthRefused()


def _refuse_fill_density(row):
    if row.get('invent_fill_density') is True:
        raise InventedFillDensityRefused()
    for key in FILL_DENSITY_KEYS:
        if key in row and row[key] is not None:
            raise InventedFillDensityRefused()


def _refuse_scout_ticker(row):
    ticker = row.get('ticker')
    if isinstance(ticker, str) and ticker in scout_index()['by_ticker']:
        raise InventedFillRefused()


def _occurrence_state(row):
    """Classify an occurrence field without writing one.

    An absent key and a null value are missing. A Z timestamp is present.
    Any other value is an invented source of time.
    """
    if not isinstance(row, dict):
        raise OrchestratorError('occurrence')
    if 'occurrence_datetime' not in row:
        return 'missing'
    occ = row.get('occurrence_datetime')
    if occ is None:
        return 'missing'
    if isinstance(occ, str) and len(occ) >= 20 and 'T' in occ and occ.endswith('Z'):
        return 'present'
    raise InventedSoTRefused()


def occurrence_census(markets):
    """Count missing and present occurrence fields. Does not fill either."""
    if not isinstance(markets, list):
        raise OrchestratorError('markets')
    missing = 0
    present = 0
    for market in markets:
        state = _occurrence_state(market)
        if state == 'missing':
            missing += 1
        else:
            present += 1
    return {
        'missing_occurrence_datetime_n': missing,
        'present_occurrence_datetime_n': present,
    }


def _assert_event_occurrence(event, markets_for_event):
    """The event timestamp must match the market timestamps already on the hunt.

    A null market field requires a null event field. A present market field
    is not replaced and is not dropped.
    """
    states = [_occurrence_state(market) for market in markets_for_event]
    if any(state == 'missing' for state in states):
        if not all(state == 'missing' for state in states):
            raise OrchestratorError('occurrence disagreement')
        if event.get('occurrence_datetime') is not None:
            raise InventedSoTRefused()
        return
    values = {market.get('occurrence_datetime') for market in markets_for_event}
    if len(values) != 1:
        raise OrchestratorError('occurrence disagreement')
    expected = values.pop()
    if event.get('occurrence_datetime') != expected:
        raise InventedSoTRefused()


def classify_native_taker(row):
    """Partition from native taker_* fields. Lee-Ready does not vote."""
    if not isinstance(row, dict):
        raise OrchestratorError('row')
    if _lee_ready_requested(row):
        raise LeeReadyRefused()
    _refuse_fee_literal(row)
    _refuse_depth_keys(row)
    _refuse_fill_density(row)
    _refuse_scout_ticker(row)
    if row.get('invent_occurrence_datetime') is True or 'occurrence_datetime' in row:
        raise InventedSoTRefused()
    unknown = [
        key for key in row
        if key.startswith('taker_') and key not in PUBLIC_TAKER_FIELDS and row.get(key) is not None
    ]
    if unknown:
        raise TakerFieldRefused('unknown taker_* field')
    outcome = None
    present = []
    if row.get('taker_outcome_side') is not None:
        side = row['taker_outcome_side']
        if side not in ('yes', 'no'):
            raise TakerFieldRefused('taker_outcome_side')
        outcome = _agree(outcome, side)
        present.append('taker_outcome_side')
    if row.get('taker_book_side') is not None:
        book = row['taker_book_side']
        if book not in BOOK_TO_OUTCOME:
            raise TakerFieldRefused('taker_book_side')
        outcome = _agree(outcome, BOOK_TO_OUTCOME[book])
        present.append('taker_book_side')
    if row.get('taker_side') is not None:
        side = row['taker_side']
        if side not in ('yes', 'no'):
            raise TakerFieldRefused('taker_side')
        outcome = _agree(outcome, side)
        present.append('taker_side')
    if outcome is None:
        raise TakerFieldRefused('native public taker_* field required')
    if row.get('result') not in (None, ''):
        raise InventedFillRefused()
    if row.get('settlement_ts') is not None:
        raise InventedFillRefused()
    for key in OUTPUT_KEYS:
        if key in row and row[key] is not None:
            raise ScorecardPromotionRefused()
    return {
        'taker_outcome_side': outcome,
        'taker_book_side': 'bid' if outcome == 'yes' else 'ask',
        'maker_outcome_side': feebook.TAKER_FILLS_RESTING[outcome],
        'native_fields': present,
        'classification': 'native_public_taker',
        'lee_ready': 'REFUSED',
        'aggressor_inference': None,
    }


def _observation(payload, transaction_time):
    if payload is None:
        return None
    if not isinstance(payload, dict):
        raise OrchestratorError('book')
    return rails.BookObservation(
        content=rails.canonical_book_content(payload),
        transaction_time=transaction_time,
    )


def classify_fresh_queue(row):
    """Bin on rails content-fresh and queue attribution. Taker fields do not vote.

    A freshness row is not a market record. An occurrence_datetime on that
    row is an invented source of time. Fill density is refused.
    """
    if not isinstance(row, dict):
        raise OrchestratorError('row')
    if _lee_ready_requested(row):
        raise LeeReadyRefused()
    _refuse_fee_literal(row)
    _refuse_depth_keys(row)
    _refuse_fill_density(row)
    _refuse_scout_ticker(row)
    if row.get('invent_occurrence_datetime') is True or 'occurrence_datetime' in row:
        raise InventedSoTRefused()
    if row.get('result') not in (None, ''):
        raise InventedFillRefused()
    for key in OUTPUT_KEYS:
        if key in row and row[key] is not None:
            raise ScorecardPromotionRefused()
    if 'queue_ahead' not in row:
        raise OrchestratorError('queue_ahead')
    previous = _observation(row.get('previous'), row.get('previous_transaction_time'))
    current = _observation(row.get('current'), row.get('transaction_time'))
    if current is None:
        raise OrchestratorError('current book')
    flag = hygiene.content_fresh_flag(
        previous,
        current,
        keepalive=bool(row.get('keepalive')),
    )
    queue_bin = hygiene.queue_attribution_bin(row['queue_ahead'])
    return {
        'row_id': row.get('row_id'),
        'content_fresh_flag': flag['content_fresh_flag'],
        'fresh_reason': flag['reason'],
        'queue_attribution_bin': queue_bin,
        'lee_ready': 'REFUSED',
        'fresh_vs_stale_gap': None,
    }


def _scorecard_row(row):
    for key in OUTPUT_KEYS:
        row[key] = None
    return row


def partition_native(trades):
    """Group by native taker outcome. ROI stays null. Lee-Ready stays refused."""
    if not isinstance(trades, list) or not trades:
        raise OrchestratorError('trades')
    grouped = {}
    for trade in trades:
        classified = classify_native_taker(trade)
        key = (classified['taker_outcome_side'], classified['taker_book_side'])
        grouped.setdefault(key, []).append(trade.get('trade_id'))
    rows = []
    for outcome, book in sorted(grouped):
        row = {
            'taker_outcome_side': outcome,
            'taker_book_side': book,
            'maker_outcome_side': feebook.TAKER_FILLS_RESTING[outcome],
            'trade_n': len(grouped[(outcome, book)]),
            'trade_ids': grouped[(outcome, book)],
            'lee_ready': 'REFUSED',
            'aggressor_inference': None,
            'maker_vs_taker_roi_delta': None,
        }
        rows.append(_scorecard_row(row))
    return rows


def partition_fresh(rows):
    """Group by content-fresh flag and queue bin. The gap stays null."""
    if not isinstance(rows, list) or not rows:
        raise OrchestratorError('rows')
    grouped = {}
    for row in rows:
        classified = classify_fresh_queue(row)
        key = (classified['content_fresh_flag'], classified['queue_attribution_bin'])
        grouped.setdefault(key, []).append(classified['row_id'])
    out = []
    for flag, queue_bin in sorted(grouped, key=lambda item: (str(item[0]), item[1])):
        packed = {
            'content_fresh_flag': flag,
            'queue_attribution_bin': queue_bin,
            'row_n': len(grouped[(flag, queue_bin)]),
            'row_ids': grouped[(flag, queue_bin)],
            'lee_ready': 'REFUSED',
            'fresh_vs_stale_gap': None,
        }
        out.append(_scorecard_row(packed))
    return out


def assert_examiner_quote(quote):
    """Accept only the R1-P1 examiner formula. No series override."""
    if not isinstance(quote, dict):
        raise ShadowFeeLiteralRefused()
    formula = quote.get('formula_id')
    if formula != feebook.EXAMINER_FORMULA_ID:
        raise ShadowFeeLiteralRefused()
    if formula in (feebook.GROK_COMPARATOR_FORMULA_ID, hygiene.INHERITED_MODEL_ID):
        raise ShadowFeeLiteralRefused()
    if quote.get('series_resolution') != 'default_unknown_series':
        raise ShadowFeeLiteralRefused()
    return quote


def probe_examiner_fee(series):
    """Import the pinned feebook formula. The numeric fee is not returned."""
    if series not in (SERIES, NFL_POINTER_SERIES):
        raise OrchestratorError('series')
    quote = feebook.order_fee('taker', '1', '0.50', round_up=True, series=series)
    assert_examiner_quote(quote)
    return {
        'formula_id': quote['formula_id'],
        'series_resolution': quote['series_resolution'],
        'fee_override_applied': False,
    }


def owned_dirs():
    return (ROOT, LAB_BUNDLE, GOVERNANCE_BUNDLE)


def _assert_digest(path, digest, size=None):
    raw = Path(path).read_bytes()
    if hashlib.sha256(raw).hexdigest() != digest:
        raise OrchestratorError(Path(path).name)
    if size is not None and len(raw) != size:
        raise OrchestratorError(Path(path).name)
    return raw


def _assert_owned(name, digest, size=None, packets_root=False):
    for directory in owned_dirs():
        _assert_digest(directory / name, digest, size)
    if packets_root:
        _assert_digest(PARENT / 'packets' / name, digest, size)


def scout_index():
    """Authentic hunt: 48 markets, 24 events. Cached after the digest matches."""
    global _SCOUT_INDEX
    if _SCOUT_INDEX is not None:
        return _SCOUT_INDEX
    payload = json.loads(_assert_digest(SCOUT_CANONICAL, SCOUT_SHA256, SCOUT_BYTES))
    if payload.get('cursor') != '':
        raise OrchestratorError('scout cursor')
    markets = payload.get('markets')
    if not isinstance(markets, list) or len(markets) != SCOUT_MARKETS_N:
        raise OrchestratorError('scout markets')
    by_ticker = {}
    events = set()
    missing_occurrence = 0
    for market in markets:
        if not isinstance(market, dict):
            raise OrchestratorError('scout market')
        ticker = market.get('ticker')
        event = market.get('event_ticker')
        if not isinstance(ticker, str) or not ticker.startswith(SERIES + '-'):
            raise InventedMarketRefused()
        if ticker in by_ticker:
            raise OrchestratorError('duplicate ticker')
        if not isinstance(event, str) or not event.startswith(SERIES + '-'):
            raise InventedMarketRefused()
        if market.get('status') != 'active':
            raise OrchestratorError('scout status')
        if market.get('result') != '':
            raise InventedFillRefused()
        if 'orderbook_fp' in market:
            raise InventedDepthRefused()
        if 'fill_density' in market:
            raise InventedFillDensityRefused()
        if _occurrence_state(market) == 'missing':
            missing_occurrence += 1
        by_ticker[ticker] = market
        events.add(event)
    if len(events) != SCOUT_EVENTS_N:
        raise OrchestratorError('scout events')
    if missing_occurrence != MISSING_OCCURRENCE_N:
        raise OrchestratorError('occurrence census')
    _SCOUT_INDEX = {
        'by_ticker': by_ticker,
        'events': events,
        'markets_n': len(by_ticker),
        'events_n': len(events),
        'missing_occurrence_datetime_n': missing_occurrence,
    }
    return _SCOUT_INDEX


def _assert_market_object(market, index):
    if not isinstance(market, dict):
        raise OrchestratorError('market')
    ticker = market.get('ticker')
    if ticker not in index['by_ticker']:
        raise InventedMarketRefused()
    if market != index['by_ticker'][ticker]:
        raise InventedMarketRefused()
    if market.get('result') != '':
        raise InventedFillRefused()
    if market.get('status') != 'active':
        raise OrchestratorError('market status')
    if 'orderbook_fp' in market:
        raise InventedDepthRefused()
    if 'fill_density' in market:
        raise InventedFillDensityRefused()
    event = market.get('event_ticker')
    if event not in index['events']:
        raise InventedMarketRefused()
    return ticker


def _assert_source_pins(payload):
    if payload.get('freeze_sha256') != FREEZE_SHA256:
        raise OrchestratorError('source pins')
    if payload.get('scout_hunt_sha256') != SCOUT_SHA256:
        raise OrchestratorError('source pins')
    if payload.get('panel_stub_sha256') != PANEL_STUB_SHA256:
        raise OrchestratorError('source pins')
    if payload.get('conductor_stamp_sha256') != CONDUCTOR_STAMP_SHA256:
        raise OrchestratorError('source pins')
    if payload.get('pre_accept_empty_sha256') != PRE_ACCEPT_EMPTY_SHA256:
        raise OrchestratorError('source pins')
    if payload.get('conductor_accept_sha256') != CONDUCTOR_ACCEPT_SHA256:
        raise OrchestratorError('source pins')
    if payload.get('examiner_hold_sha256') != EXAMINER_HOLD_SHA256:
        raise OrchestratorError('source pins')
    if payload.get('feature_family') != FEATURE_FAMILY:
        raise OrchestratorError('source pins')
    if payload.get('knob') != KNOB:
        raise OrchestratorError('source pins')
    if payload.get('arms') != ANALYSIS_SLICE:
        raise OrchestratorError('source pins')
    if payload.get('panel_subset_of_scout') is not True:
        raise OrchestratorError('source pins')
    if payload.get('panel_full_scout') is not False:
        raise OrchestratorError('source pins')
    if payload.get('admitted_at') is not None:
        raise OrchestratorError('source pins')
    if payload.get('missing_occurrence_datetime_n') != MISSING_OCCURRENCE_N:
        raise OrchestratorError('source pins')
    if payload.get('occurrence_datetime_invented') is not False:
        raise InventedSoTRefused()
    if payload.get('fill_density_invented') is not False:
        raise InventedFillDensityRefused()
    if payload.get('signal_port') is not False or payload.get('claims_s1_green') is not False:
        raise OrchestratorError('source pins')
    if payload.get('fee_import_only') is not True or payload.get('rails_import_only') is not True:
        raise OrchestratorError('source pins')
    if payload.get('governance_tree') != 'absent':
        raise OrchestratorError('source pins')
    if payload.get('scout_markets_n') != SCOUT_MARKETS_N:
        raise OrchestratorError('source pins')
    if payload.get('scout_events_n') != SCOUT_EVENTS_N:
        raise OrchestratorError('source pins')
    if payload.get('events_n') != PANEL_EVENTS_N or payload.get('markets_n') != PANEL_MARKETS_N:
        raise OrchestratorError('source pins')
    if payload.get('nhl_fq_reopen') is not False or payload.get('cpi_fq_reopen') is not False:
        raise OrchestratorError('source pins')
    if payload.get('does_not_ungate') != list(DOES_NOT_UNGATE):
        raise UngateRefused()
    if payload.get('nfl_000_pointer') != NFL_000_POINTER:
        raise SignalPortRefused()
    for key in OUTPUT_KEYS:
        if key not in payload or payload[key] is not None:
            raise ScorecardPromotionRefused()
    return payload


def conductor_pin_status():
    """Report whether checkout bytes match the attached conductor sha256 values."""
    freeze_match = sha256_file(PACKET) == FREEZE_SHA256
    scout_match = sha256_file(SCOUT_CANONICAL) == SCOUT_SHA256
    stub_match = sha256_file(PANEL_STUB) == PANEL_STUB_SHA256
    return {
        'freeze_matches_conductor_claim': freeze_match,
        'scout_hunt_matches_conductor_claim': scout_match,
        'panel_stub_matches_conductor_claim': stub_match,
        'conductor_bytes_in_checkout': freeze_match and scout_match and stub_match,
        'scout_markets_n': SCOUT_MARKETS_N,
        'scout_events_n': SCOUT_EVENTS_N,
        'events_n': PANEL_EVENTS_N,
        'markets_n': PANEL_MARKETS_N,
        'missing_occurrence_datetime_n': MISSING_OCCURRENCE_N,
        'admitted_at': None,
        'governance_tree_present': GOVERNANCE_TREE.is_dir(),
    }


def _assert_authentic_bytes():
    _assert_owned(FREEZE_NAME, FREEZE_SHA256, FREEZE_BYTES, packets_root=True)
    _assert_owned(SCOUT_NAME, SCOUT_SHA256, SCOUT_BYTES, packets_root=False)
    _assert_digest(SCOUT_CANONICAL, SCOUT_SHA256, SCOUT_BYTES)
    _assert_owned(ACCEPT_NAME, CONDUCTOR_ACCEPT_SHA256, ACCEPT_BYTES, packets_root=True)
    _assert_owned(HOLD_NAME, EXAMINER_HOLD_SHA256, HOLD_BYTES, packets_root=True)
    _assert_owned(STAMP_NAME, CONDUCTOR_STAMP_SHA256, STAMP_BYTES, packets_root=False)
    _assert_owned(PRE_ACCEPT_NAME, PRE_ACCEPT_EMPTY_SHA256, PRE_ACCEPT_BYTES, packets_root=False)
    _assert_owned('panel_stub.json', PANEL_STUB_SHA256, PANEL_BYTES, packets_root=False)
    _assert_owned(PANEL_ALIAS, PANEL_STUB_SHA256, PANEL_BYTES, packets_root=True)
    _assert_digest(PANEL_STUB, PANEL_STUB_SHA256, PANEL_BYTES)
    for directory in owned_dirs():
        path = directory / SOURCE_PINS_NAME
        _assert_digest(path, SOURCE_PINS_SHA256)
        _assert_source_pins(json.loads(path.read_text()))
    stamp = json.loads(CONDUCTOR_STAMP.read_text())
    if stamp.get('status') != 'FROZEN':
        raise OrchestratorError('conductor stamp')
    if stamp.get('freeze_sha256') != FREEZE_SHA256:
        raise OrchestratorError('conductor stamp')
    if stamp.get('scout_hunt_sha256') != SCOUT_SHA256:
        raise OrchestratorError('conductor stamp')
    if stamp.get('panel_stub_sha256') != PANEL_STUB_SHA256:
        raise OrchestratorError('conductor stamp')
    if stamp.get('arms') != list(ARMS):
        raise OrchestratorError('conductor stamp')
    if stamp.get('feature_family') != FEATURE_FAMILY:
        raise OrchestratorError('conductor stamp')
    if stamp.get('packet_id') != EXPERIMENT_ID:
        raise OrchestratorError('conductor stamp')
    if stamp.get('results') is not None or stamp.get('pnl') is not None:
        raise ScorecardPromotionRefused()
    accept = json.loads(CONDUCTOR_ACCEPT.read_text())
    if accept.get('status') != 'ACCEPT_IMPLEMENT_GO':
        raise OrchestratorError('conductor accept')
    if accept.get('feature_family') != FEATURE_FAMILY:
        raise OrchestratorError('conductor accept')
    if accept.get('packet_id') != EXPERIMENT_ID:
        raise OrchestratorError('conductor accept')
    if accept.get('freeze_sha256') != FREEZE_SHA256:
        raise OrchestratorError('conductor accept')
    if accept.get('scout_hunt_sha256') != SCOUT_SHA256:
        raise OrchestratorError('conductor accept')
    if accept.get('panel_stub_sha256') != PANEL_STUB_SHA256:
        raise OrchestratorError('conductor accept')
    if accept.get('panel_version') != PANEL_VERSION:
        raise OrchestratorError('conductor accept')
    if accept.get('knob') != KNOB:
        raise OrchestratorError('conductor accept')
    if accept.get('arms') != list(ARMS):
        raise OrchestratorError('conductor accept')
    if accept.get('arm_values') != ANALYSIS_SLICE:
        raise OrchestratorError('conductor accept')
    if accept.get('lab_dir') != LAB_DIRECTORY + '/':
        raise OrchestratorError('conductor accept')
    if accept.get('does_not_ungate') != list(DOES_NOT_UNGATE):
        raise UngateRefused()
    if accept.get('nearest_dead_card') != NEAREST_DEAD_CARD:
        raise OrchestratorError('conductor accept')
    if accept.get('feebook_pin') != FEEBOOK_PIN or accept.get('rails_pin') != RAILS_PIN:
        raise OrchestratorError('conductor accept')
    if accept.get('post_cpifq_main') != BASE_COMMIT:
        raise OrchestratorError('conductor accept')
    if accept.get('commit_verbatim') != ['freeze', 'scout_hunt', 'panel_stub']:
        raise OrchestratorError('conductor accept')
    if accept.get('panel_events') != PANEL_EVENTS_N or accept.get('panel_markets') != PANEL_MARKETS_N:
        raise OrchestratorError('conductor accept')
    if accept.get('scout_markets') != SCOUT_MARKETS_N or accept.get('scout_events') != SCOUT_EVENTS_N:
        raise OrchestratorError('conductor accept')
    if accept.get('panel_full_scout') is not False or accept.get('admitted_at') is not None:
        raise OrchestratorError('conductor accept')
    if accept.get('results') is not None or accept.get('pnl') is not None:
        raise ScorecardPromotionRefused()
    hold = json.loads(EXAMINER_HOLD.read_text())
    if hold.get('status') != 'NOT_SCORED' or hold.get('stub_ready') is not False:
        raise ExaminerNotReady()
    if hold.get('feature_family') != FEATURE_FAMILY:
        raise OrchestratorError('examiner hold')
    if hold.get('packet') != EXPERIMENT_ID:
        raise OrchestratorError('examiner hold')
    if hold.get('freeze_sha256') != FREEZE_SHA256:
        raise OrchestratorError('examiner hold')
    if hold.get('arms') != list(ARMS):
        raise OrchestratorError('examiner hold')
    if sorted(hold.get('metrics_null') or []) != sorted(OUTPUT_KEYS):
        raise OrchestratorError('examiner hold')
    pre = json.loads(PRE_ACCEPT_EMPTY.read_text())
    if pre.get('note') != 'pre-ACCEPT empty':
        raise OrchestratorError('pre-accept empty')
    if 'settled_join_n' in pre or 'n_books' in pre:
        raise OrchestratorError('pre-accept empty')
    status = conductor_pin_status()
    if status['conductor_bytes_in_checkout'] is not True:
        raise OrchestratorError('conductor bytes')
    if status['governance_tree_present'] is not False:
        raise OrchestratorError('governance tree')


def select_panel_path(stub_path=None, admitted_path=None):
    """Prefer panel_admitted.json when the file exists. Otherwise the stub."""
    stub_path = PANEL_STUB if stub_path is None else Path(stub_path)
    admitted_path = PANEL_ADMITTED if admitted_path is None else Path(admitted_path)
    if Path(admitted_path).is_file():
        return Path(admitted_path)
    if not Path(stub_path).is_file():
        raise OrchestratorError('panel stub')
    return Path(stub_path)


def _validate_panel(payload, admitted):
    if not isinstance(payload, dict):
        raise OrchestratorError('panel')
    if payload.get('panel_version') != PANEL_VERSION:
        raise PanelVersionRefused()
    if payload.get('packet_id') != EXPERIMENT_ID:
        raise OrchestratorError('packet')
    if payload.get('schema_id') != SCHEMA_ID:
        raise OrchestratorError('schema')
    if payload.get('series_ticker') != SERIES:
        raise OrchestratorError('series')
    if payload.get('cohort_kind') != COHORT_KIND:
        raise OrchestratorError('cohort')
    if payload.get('scout_cite') != SCOUT_CITE:
        raise OrchestratorError('scout cite')
    if payload.get('scout_sha256') != SCOUT_SHA256:
        raise OrchestratorError('scout sha')
    if list(payload.get('rules') or []) != list(PANEL_RULES):
        raise OrchestratorError('rules')
    if payload.get('cohort_summary') != COHORT_SUMMARY:
        raise OrchestratorError('cohort summary')
    stamp = payload.get('admitted_at')
    if admitted:
        if not isinstance(stamp, str) or not stamp.endswith('Z'):
            raise OrchestratorError('admitted_at')
    elif stamp is not None:
        raise OrchestratorError('admitted_at')
    if not admitted:
        if payload.get('stub_status') != STUB_STATUS:
            raise OrchestratorError('stub_status')
        if payload.get('purpose') != PURPOSE:
            raise OrchestratorError('purpose')
        if payload.get('stubbed_at_et') != STUBBED_AT:
            raise OrchestratorError('stubbed_at')
    for key in ('results', 'pnl'):
        if key not in payload or payload[key] is not None:
            raise InventedFillRefused()
    index = scout_index()
    events = payload.get('events')
    markets = payload.get('markets')
    if not isinstance(events, list) or len(events) != PANEL_EVENTS_N:
        raise OrchestratorError('events')
    if not isinstance(markets, list) or len(markets) != PANEL_MARKETS_N:
        raise OrchestratorError('markets')
    seen = []
    event_names = []
    for event in events:
        if not isinstance(event, dict):
            raise OrchestratorError('events')
        name = event.get('event_ticker')
        if name not in index['events']:
            raise InventedMarketRefused()
        if event.get('markets_n') != 2:
            raise OrchestratorError('event markets')
        event_names.append(name)
    if len(set(event_names)) != PANEL_EVENTS_N:
        raise OrchestratorError('events')
    for market in markets:
        seen.append(_assert_market_object(market, index))
    if len(set(seen)) != PANEL_MARKETS_N:
        raise OrchestratorError('markets')
    by_event = {}
    for market in markets:
        by_event.setdefault(market.get('event_ticker'), []).append(market)
    for event in events:
        name = event.get('event_ticker')
        group = by_event.get(name) or []
        scout_n = sum(1 for market in index['by_ticker'].values() if market.get('event_ticker') == name)
        if len(group) != 2 or scout_n != 2:
            raise InventedMarketRefused()
        _assert_event_occurrence(event, group)
    census = occurrence_census(markets)
    if census['missing_occurrence_datetime_n'] != MISSING_OCCURRENCE_N:
        raise OrchestratorError('occurrence census')
    if census['present_occurrence_datetime_n'] != PANEL_MARKETS_N:
        raise OrchestratorError('occurrence census')
    return payload


def load_panel(stub_path=None, admitted_path=None):
    """Stub by default. panel_admitted.json wins when it is on disk."""
    path = select_panel_path(stub_path, admitted_path)
    if path.resolve() == PANEL_STUB.resolve():
        _assert_authentic_bytes()
    payload = json.loads(path.read_text())
    return _validate_panel(payload, admitted=path.name == 'panel_admitted.json')


def arm_table():
    return tuple({'id': arm, 'analysis_slice': ANALYSIS_SLICE[arm]} for arm in ARMS)


def instrument_binding(panel=None):
    """One slice knob. Fee and rails commits stay fixed. No scorecard fill."""
    if panel is None:
        panel = load_panel()
    atp = probe_examiner_fee(SERIES)
    nfl = probe_examiner_fee(NFL_POINTER_SERIES)
    if atp != nfl:
        raise ShadowFeeLiteralRefused()
    if hygiene.FEEBOOK_COMMIT != FEEBOOK_COMMIT or hygiene.RAILS_COMMIT != RAILS_COMMIT:
        raise OrchestratorError('pin')
    ahead_bin = hygiene.queue_attribution_bin(rails.QUEUE_AHEAD_DEFAULT)
    if ahead_bin != 'q3300':
        raise OrchestratorError('queue bin')
    if not NFL_POINTER_PATH.is_file():
        raise OrchestratorError('nfl 000 pointer')
    index = scout_index()
    pins = conductor_pin_status()
    if pins['conductor_bytes_in_checkout'] is not True:
        raise OrchestratorError('conductor bytes')
    census = occurrence_census(panel.get('markets') or [])
    scout_census = occurrence_census(list(index['by_ticker'].values()))
    if census['missing_occurrence_datetime_n'] != MISSING_OCCURRENCE_N:
        raise OrchestratorError('occurrence census')
    if scout_census['missing_occurrence_datetime_n'] != MISSING_OCCURRENCE_N:
        raise OrchestratorError('occurrence census')
    if census['present_occurrence_datetime_n'] != PANEL_MARKETS_N:
        raise OrchestratorError('occurrence census')
    if scout_census['present_occurrence_datetime_n'] != SCOUT_MARKETS_N:
        raise OrchestratorError('occurrence census')
    return {
        'experiment_id': EXPERIMENT_ID,
        'lab_directory': LAB_DIRECTORY,
        'feature_family': FEATURE_FAMILY,
        'knob': KNOB,
        'arms': arm_table(),
        'panel_version': panel['panel_version'],
        'admitted_at': panel.get('admitted_at'),
        'series_ticker': SERIES,
        'events_n': len(panel.get('events') or []),
        'markets_n': len(panel.get('markets') or []),
        'scout_markets_n': index['markets_n'],
        'scout_events_n': index['events_n'],
        'panel_subset_of_scout': True,
        'panel_full_scout': False,
        'missing_occurrence_datetime_n': census['missing_occurrence_datetime_n'],
        'occurrence_datetime_invented': False,
        'fill_density_invented': False,
        'strategy_pointer': None,
        'nfl_000_pointer': NFL_000_POINTER,
        'signal_port': False,
        'feebook_commit': FEEBOOK_COMMIT,
        'rails_commit': RAILS_COMMIT,
        'examiner_formula_id': feebook.EXAMINER_FORMULA_ID,
        'fee_credit_rule_id': rails.FEE_CREDIT_RULE_ID,
        'fee_source': 'feebook',
        'queue_source': 'rails',
        'honesty_helpers': 'hygiene',
        'fee_import_only': True,
        'rails_import_only': True,
        'fee_override_applied': False,
        'freeze_fee_channel_cite': FEE_CHANNEL_CITE,
        'probe_formula_id': atp['formula_id'],
        'probe_series_resolution': atp['series_resolution'],
        'probe_scorecard_write': False,
        'lee_ready': 'REFUSED',
        'logan_keys_required': False,
        'live_orders': False,
        'signal_retune_000': False,
        'queue_fragility_reopen': False,
        'cap_sr_reopen': False,
        'cap_sr_fx_reopen': False,
        'l2_reopen': False,
        'empty_ob_reopen': False,
        'sot_id_reopen': False,
        'l2_sf_reopen': False,
        'nhl_fq_reopen': False,
        'cpi_fq_reopen': False,
        'admit_py_run': False,
        'claims_s1_green': False,
        'does_not_ungate': list(DOES_NOT_UNGATE),
        's1_s2_r2p4_ungated': False,
        'fee_is_knob': False,
        'examiner_status': 'NOT_SCORED',
        'stub_ready': False,
        'scorecard_fields': SCORECARD_FIELDS,
        'freeze_sha256': FREEZE_SHA256,
        'scout_hunt_sha256': SCOUT_SHA256,
        'panel_stub_sha256': PANEL_STUB_SHA256,
        'source_pins_sha256': SOURCE_PINS_SHA256,
        'conductor_stamp_sha256': CONDUCTOR_STAMP_SHA256,
        'conductor_bytes_in_checkout': True,
        'governance_tree_present': False,
        'base_commit': BASE_COMMIT,
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
    return scorecard


def assert_null_scorecard(payload):
    """Require every instrument field, results, and pnl, and require null."""
    if not isinstance(payload, dict):
        raise ScorecardPromotionRefused()
    if payload.get('note') == 'pre-ACCEPT empty':
        raise PreAcceptEmptyRefused()
    for key in OUTPUT_KEYS:
        if key not in payload or payload[key] is not None:
            raise ScorecardPromotionRefused()
    return payload


def load_scorecard(path):
    """Read a null scorecard. The pre-ACCEPT payload is refused."""
    path = Path(path)
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() == PRE_ACCEPT_EMPTY_SHA256:
        raise PreAcceptEmptyRefused()
    payload = json.loads(raw)
    if isinstance(payload, dict) and payload.get('note') == 'pre-ACCEPT empty':
        raise PreAcceptEmptyRefused()
    return assert_null_scorecard(payload)


def write_scorecard(payload):
    """Refuse a missing or non-null measurement field. Nothing is written."""
    assert_null_scorecard(payload)
    raise ScorecardPromotionRefused()


def _report(arm, source, extra):
    if arm not in ANALYSIS_SLICE:
        raise UnknownSlice()
    published = published_scorecard()
    report = {
        'experiment_id': EXPERIMENT_ID,
        'arm': arm,
        'analysis_slice': ANALYSIS_SLICE[arm],
        'source': source,
        'published': published,
        'promoted': False,
        'strategy_pointer': None,
        'signal_port': False,
        'live_orders': False,
        'lee_ready': 'REFUSED',
        'fee_pin': FEEBOOK_COMMIT,
        'rails_pin': RAILS_COMMIT,
        'fee_import_only': True,
        'rails_import_only': True,
        'claims_s1_green': False,
        's1_s2_r2p4_ungated': False,
        'admit_py_run': False,
        'nhl_fq_reopen': False,
        'cpi_fq_reopen': False,
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
    """Schema for one slice on the loaded panel. Scorecard fields stay null."""
    if arm not in ANALYSIS_SLICE:
        raise UnknownSlice()
    if panel is None:
        panel = load_panel()
    events = panel.get('events') or []
    markets = panel.get('markets') or []
    census = occurrence_census(markets)
    extra = {
        'event_count': len(events),
        'market_count': len(markets),
        'scout_markets_n': scout_index()['markets_n'],
        'scout_events_n': scout_index()['events_n'],
        'missing_occurrence_datetime_n': census['missing_occurrence_datetime_n'],
    }
    return _report(arm, 'panel', extra)


def load_synthetic_trades(path=None):
    path = SYNTHETIC_TRADES if path is None else Path(path)
    payload = json.loads(Path(path).read_text())
    if payload.get('source') != 'synthetic_schema_standin':
        raise OrchestratorError('source')
    trades = payload.get('trades')
    if not isinstance(trades, list) or len(trades) < 2:
        raise OrchestratorError('synthetic trades')
    return trades


def load_synthetic_fresh(path=None):
    path = SYNTHETIC_FRESH if path is None else Path(path)
    payload = json.loads(Path(path).read_text())
    if payload.get('source') != 'synthetic_schema_standin':
        raise OrchestratorError('source')
    rows = payload.get('rows')
    if not isinstance(rows, list) or len(rows) < 2:
        raise OrchestratorError('synthetic rows')
    return rows


def conduct_native(path=None):
    """ATPA0 schema on synthetic native rows. Does not write the freeze scorecard."""
    rows = partition_native(load_synthetic_trades(path))
    return _report(ATPA0, 'synthetic_schema_standin', {
        'partitions': rows,
        'partition_count': len(rows),
    })


def conduct_fresh(path=None):
    """ATPA1 schema on synthetic book rows. The gap stays null."""
    rows = partition_fresh(load_synthetic_fresh(path))
    return _report(ATPA1, 'synthetic_schema_standin', {
        'bins': rows,
        'bin_count': len(rows),
    })


def frozen_output_snapshot():
    """Read freeze files. Does not modify them."""
    payloads = {
        'frozen': json.loads(FROZEN_EXPERIMENT.read_text()),
        'empty': json.loads(EMPTY_RESULTS.read_text()),
        'bundle_frozen': json.loads((LAB_BUNDLE / 'FROZEN_EXPERIMENT.json').read_text()),
        'bundle_results': json.loads((LAB_BUNDLE / 'results.json').read_text()),
        'governance_frozen': json.loads((GOVERNANCE_BUNDLE / 'FROZEN_EXPERIMENT.json').read_text()),
        'governance_results': json.loads((GOVERNANCE_BUNDLE / 'results.json').read_text()),
    }
    snapshot = {}
    for name, payload in payloads.items():
        for key in ('results', 'pnl'):
            if key not in payload or payload[key] is not None:
                raise ScorecardPromotionRefused()
            snapshot['%s.%s' % (name, key)] = None
        if name in ('empty', 'bundle_results', 'governance_results'):
            for key in SCORECARD_FIELDS:
                if key not in payload or payload[key] is not None:
                    raise ScorecardPromotionRefused()
                snapshot['%s.%s' % (name, key)] = None
    return snapshot
