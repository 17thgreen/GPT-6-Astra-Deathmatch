"""C4 KXCPI fee and queue honesty harness.

Measurement only. Imports the R1-P1 feebook and the R1-P5 rails through the
R2-P1 hygiene helpers. This module does not edit those labs, does not place
orders, does not read Logan keys, and does not write scorecard metrics.

The checkout freeze, scout hunt, and panel stub match the attached sha256
values. Panel markets are the full scout-hunt objects. Missing
occurrence_datetime stays missing. Sparse 24h tape is a refuse bin.
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

LAB_DIRECTORY = 'kalshi_c4_kxcpi_feequue_lab_20260923'
EXPERIMENT_ID = 'C4-KXCPI-FEEQUEUE-HARNESS'
FEATURE_FAMILY = 'CPI-FQ'
SERIES = 'KXCPI'
SCHEMA_ID = 'astra.panel_stub.v0'
PANEL_VERSION = '2026-09-23.c4-kxcpi-v0'
COHORT_KIND = 'scout_hunt_subset'
STUB_STATUS = 'NOT_ADMITTED'
PURPOSE = 'GET-only CPI threshold-ladder fee+queue honesty harness seed from Scout hunt bytes'
SCOUT_CITE = 'packets/scout_cashcow_hunt_2026-09-22/scout_hunt_KXCPI.json'
KNOB = 'analysis_slice'
C4A0 = 'C4A0'
C4A1 = 'C4A1'
ARMS = (C4A0, C4A1)
ANALYSIS_SLICE = {
    C4A0: 'maker_vs_taker_native',
    C4A1: 'sparse_24h_vs_fresh_bin',
}
FEEBOOK_COMMIT = '22371178cb2663250b4762f328069571c48cb551'
RAILS_COMMIT = '6a28e0d6254327ea4e6451c781bec56215ac6cac'
BASE_COMMIT = '677d5d4f0d5ed1235b4827bf89dd98d82bc34356'
FREEZE_SHA256 = '949b255859196f02d73303a1019e51276c583f8d1e3ffb4f0a64d330467c6f93'
SCOUT_SHA256 = '6033907bb739bc00c41c796a3c1ed24553e0b7a44116ec3ea4bbaf39066bdcc8'
PANEL_STUB_SHA256 = 'b20b0cbee50c127d2e9bb2548b574b7d643cc708f54019d53bd91775f9762c13'
CONDUCTOR_STAMP_SHA256 = '3b74b2a638be8c26394be2a2a3149e77499255bfea18aed95e67713118e4ba6c'
PRE_ACCEPT_EMPTY_SHA256 = '6aafb9d82d93bd9210b1f822616f42dd8a8286b9191a5d8f765b113142e13b7b'
CONDUCTOR_ACCEPT_SHA256 = '19ae0ae1fca66fa5c45bf8c13e013e3d710423c3e04194cc617d8bac1db546d7'
EXAMINER_HOLD_SHA256 = 'e5665a66ffebf95a1e74396263a1c91aa127f7ae0c9373291d7342bc759899d3'
SOURCE_PINS_SHA256 = '6560d7bf40cd6470f3cae52504ee3079c8b7bbf7404c84f66fa77d84d66fceb9'
FREEZE_BYTES = 4860
SCOUT_BYTES = 82096
PANEL_BYTES = 101481
STAMP_BYTES = 490
PRE_ACCEPT_BYTES = 122
ACCEPT_BYTES = 1810
HOLD_BYTES = 852
SCOUT_MARKETS_N = 44
SCOUT_EVENTS_N = 4
PANEL_EVENTS_N = 4
PANEL_MARKETS_N = 44
MISSING_OCC_N = 21
SPARSE_24H_N = 21
SPARSE_24H_TOKEN = '0.00'
NOV_EVENT = 'KXCPI-26NOV'
FEE_CHANNEL_CITE = 'quadratic_with_maker_fees'
NFL_000_POINTER = 'nfl_factorial_lab_20260921/SHADOW_CANDIDATE_FREEZE.json'
NFL_POINTER_SERIES = 'KXNFLGAME'
PUBLIC_HOST = 'api.elections.kalshi.com'
OUT_OF_SCOPE_ROUTE = 'POST /portfolio/orders'
SCORECARD_FIELDS = (
    'maker_vs_taker_roi_delta',
    'sparse_vs_fresh_gap',
    'missing_sot_n',
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
    'no_invent_fill_density',
    'no_invent_depth_fills_pnl',
    'results_pnl_null',
    'does_not_ungate_S1_S2',
)
COHORT_SUMMARY = {
    'events_n': PANEL_EVENTS_N,
    'markets_n': PANEL_MARKETS_N,
    'source_markets_n': SCOUT_MARKETS_N,
    'source_events_n': SCOUT_EVENTS_N,
    'missing_occurrence_datetime_n': MISSING_OCC_N,
    'note': 'sparse_24h_honesty_stress — do not invent fills',
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
FREEZE_NAME = 'C4_KXCPI_FEEQUEUE_HARNESS_FREEZE_2026-09-23.md'
SCOUT_NAME = 'scout_hunt_KXCPI.json'
PANEL_ALIAS = 'C4_KXCPI_PANEL_STUB_2026-09-23.json'
STAMP_NAME = 'CONDUCTOR_FROZEN_EXPERIMENT.json'
PRE_ACCEPT_NAME = 'PRE_ACCEPT_EMPTY_RESULTS.json'
ACCEPT_NAME = 'CONDUCTOR_ACCEPT_C4_KXCPI_FEEQUEUE_HARNESS_2026-09-23.json'
HOLD_NAME = 'EXAMINER_HOLD_C4_KXCPI_FEEQUEUE_HARNESS_PRE_PR_2026-09-23.json'
SOURCE_PINS_NAME = 'SOURCE_PINS.json'
PACKET = ROOT / FREEZE_NAME
LAB_BUNDLE = ROOT / 'C4_KXCPI_FEEQUEUE_HARNESS'
GOVERNANCE_BUNDLE = PARENT / 'packets' / 'C4_KXCPI_FEEQUEUE_HARNESS'
GOVERNANCE_TREE = PARENT / 'lab' / 'governance' / 'astra' / 'packets'
SCOUT_CANONICAL = PARENT / 'packets' / 'scout_cashcow_hunt_2026-09-22' / SCOUT_NAME
FROZEN_EXPERIMENT = ROOT / 'FROZEN_EXPERIMENT.json'
EMPTY_RESULTS = ROOT / 'results' / 'EMPTY_RESULTS.json'
SOURCE_PINS = ROOT / SOURCE_PINS_NAME
CONDUCTOR_STAMP = ROOT / STAMP_NAME
PRE_ACCEPT_EMPTY = ROOT / PRE_ACCEPT_NAME
CONDUCTOR_ACCEPT = ROOT / ACCEPT_NAME
EXAMINER_HOLD = ROOT / HOLD_NAME
PANEL_STUB = PARENT / 'lab' / 'astra-capture' / 'c4-kxcpi' / 'panel_stub.json'
PANEL_ADMITTED = PARENT / 'lab' / 'astra-capture' / 'c4-kxcpi' / 'panel_admitted.json'
NFL_POINTER_PATH = PARENT / NFL_000_POINTER
SYNTHETIC_TRADES = ROOT / 'fixtures' / 'synthetic_native_trades.json'
SYNTHETIC_SPARSE = ROOT / 'fixtures' / 'synthetic_sparse_fresh.json'
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
    """The panel file is not the pinned C4 seed."""

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
    """Fill density on sparse 24h tape is refused."""

    def __init__(self):
        super().__init__('invented fill density')


class InventedSoTRefused(OrchestratorError):
    """occurrence_datetime is not invented for a missing source of time."""

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
    spec = importlib.util.spec_from_file_location('c4_kxcpi_hygiene', HYGIENE_PATH)
    if spec is None or spec.loader is None:
        raise OrchestratorError('hygiene import')
    module = importlib.util.module_from_spec(spec)
    sys.modules['c4_kxcpi_hygiene'] = module
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
    """Sparse 24h tape does not receive an invented fill density."""
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
    if row.get('invent_occurrence_datetime') is True:
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


def _sparse_24h_refuse(row):
    if 'volume_24h_fp' not in row or row.get('volume_24h_fp') is None:
        return False
    volume = row.get('volume_24h_fp')
    if volume == SPARSE_24H_TOKEN:
        return True
    if isinstance(volume, str):
        return False
    raise OrchestratorError('volume_24h')


def _missing_occurrence_refuse(row, absent_is_missing=False):
    """A null value is a missing source of time.

    Authentic scout markets omit the key. That omission is missing when
    absent_is_missing is true. Synthetic book rows omit the key because they
    are not market records, so the omission is not a SoT bin there.
    """
    if 'occurrence_datetime' not in row:
        return absent_is_missing
    occ = row.get('occurrence_datetime')
    if occ is None:
        return True
    if isinstance(occ, str) and occ.endswith('Z'):
        return False
    raise InventedSoTRefused()


def classify_sparse_fresh(row):
    """Bin on rails content-fresh plus sparse-24h and missing-SoT refuse labels.

    Taker fields do not vote. A zero 24h volume does not become a fill.
    A null occurrence_datetime does not become a timestamp.
    """
    if not isinstance(row, dict):
        raise OrchestratorError('row')
    if _lee_ready_requested(row):
        raise LeeReadyRefused()
    _refuse_fee_literal(row)
    _refuse_depth_keys(row)
    _refuse_fill_density(row)
    _refuse_scout_ticker(row)
    if row.get('invent_occurrence_datetime') is True:
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
        'sparse_24h_refuse': _sparse_24h_refuse(row),
        'missing_occurrence_datetime_refuse': _missing_occurrence_refuse(row),
        'lee_ready': 'REFUSED',
        'sparse_vs_fresh_gap': None,
        'missing_sot_n': None,
    }


def label_market_honesty(market):
    """Read authentic public fields. Do not fill nulls or derive a density."""
    if not isinstance(market, dict):
        raise OrchestratorError('market')
    _refuse_fill_density(market)
    if 'orderbook_fp' in market:
        raise InventedDepthRefused()
    return {
        'ticker': market.get('ticker'),
        'sparse_24h_refuse': _sparse_24h_refuse(market),
        'missing_occurrence_datetime_refuse': _missing_occurrence_refuse(
            market,
            absent_is_missing=True,
        ),
        'content_fresh_flag': None,
        'lee_ready': 'REFUSED',
        'sparse_vs_fresh_gap': None,
        'missing_sot_n': None,
        'n_books': None,
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


def partition_sparse(rows):
    """Group by fresh flag, sparse-24h refuse, missing-SoT refuse, and queue bin.

    The gap stays null. missing_sot_n stays null.
    """
    if not isinstance(rows, list) or not rows:
        raise OrchestratorError('rows')
    grouped = {}
    for row in rows:
        classified = classify_sparse_fresh(row)
        key = (
            classified['content_fresh_flag'],
            classified['sparse_24h_refuse'],
            classified['missing_occurrence_datetime_refuse'],
            classified['queue_attribution_bin'],
        )
        grouped.setdefault(key, []).append(classified['row_id'])
    out = []
    for key in sorted(grouped, key=lambda item: (str(item[0]), str(item[1]), str(item[2]), item[3])):
        flag, sparse, missing, queue_bin = key
        packed = {
            'content_fresh_flag': flag,
            'sparse_24h_refuse': sparse,
            'missing_occurrence_datetime_refuse': missing,
            'queue_attribution_bin': queue_bin,
            'row_n': len(grouped[key]),
            'row_ids': grouped[key],
            'lee_ready': 'REFUSED',
            'sparse_vs_fresh_gap': None,
            'missing_sot_n': None,
        }
        out.append(_scorecard_row(packed))
    return out


def panel_honesty_bins(panel):
    """Refuse bins on the authentic stub. Content-fresh stays unset.

    The stub has quotes, not a book-pair. Freshness is not invented from them.
    """
    if not isinstance(panel, dict):
        raise OrchestratorError('panel')
    markets = panel.get('markets')
    if not isinstance(markets, list) or not markets:
        raise OrchestratorError('markets')
    grouped = {}
    for market in markets:
        label = label_market_honesty(market)
        key = (label['sparse_24h_refuse'], label['missing_occurrence_datetime_refuse'])
        grouped.setdefault(key, []).append(label['ticker'])
    out = []
    for sparse, missing in sorted(grouped):
        packed = {
            'sparse_24h_refuse': sparse,
            'missing_occurrence_datetime_refuse': missing,
            'content_fresh_flag': None,
            'market_n': len(grouped[(sparse, missing)]),
            'tickers': grouped[(sparse, missing)],
            'lee_ready': 'REFUSED',
            'sparse_vs_fresh_gap': None,
            'missing_sot_n': None,
            'n_books': None,
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
    """Authentic hunt: 44 markets, 4 events. Cached after the digest matches."""
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
        by_ticker[ticker] = market
        events.add(event)
    if len(events) != SCOUT_EVENTS_N:
        raise OrchestratorError('scout events')
    _SCOUT_INDEX = {
        'by_ticker': by_ticker,
        'events': events,
        'markets_n': len(by_ticker),
        'events_n': len(events),
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


def event_occurrence_from_markets(event_ticker, markets):
    """Event occurrence is the shared non-null market occurrence, or null.

    Null market rows are not filled. Disagreeing timestamps are refused.
    """
    rows = [market for market in markets if market.get('event_ticker') == event_ticker]
    if not rows:
        raise OrchestratorError('events')
    non_null = []
    for market in rows:
        occ = market.get('occurrence_datetime')
        if occ is None:
            continue
        if not isinstance(occ, str) or not occ.endswith('Z'):
            raise InventedSoTRefused()
        non_null.append(occ)
    unique = set(non_null)
    if len(unique) > 1:
        raise OrchestratorError('occurrence')
    if not unique:
        return None
    return next(iter(unique))


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
    if payload.get('panel_full_scout') is not True:
        raise OrchestratorError('source pins')
    if payload.get('panel_markets_equal_scout') is not True:
        raise OrchestratorError('source pins')
    if payload.get('admitted_at') is not None:
        raise OrchestratorError('source pins')
    if payload.get('signal_port') is not False or payload.get('claims_s1_green') is not False:
        raise OrchestratorError('source pins')
    if payload.get('nhl_fq_reopen') is not False:
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
    if payload.get('missing_occurrence_datetime_n') != MISSING_OCC_N:
        raise OrchestratorError('source pins')
    if payload.get('sparse_24h_zero_volume_n') != SPARSE_24H_N:
        raise OrchestratorError('source pins')
    if payload.get('kxcpi_26nov_event_occurrence_datetime') is not None:
        raise InventedSoTRefused()
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
        'panel_full_scout': True,
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
    if stamp.get('status') != 'FROZEN':
        raise OrchestratorError('conductor stamp')
    if stamp.get('results') is not None or stamp.get('pnl') is not None:
        raise ScorecardPromotionRefused()
    accept = json.loads(CONDUCTOR_ACCEPT.read_text())
    if accept.get('status') != 'ACCEPT_IMPLEMENT_GO':
        raise OrchestratorError('conductor accept')
    if accept.get('freeze_sha256') != FREEZE_SHA256:
        raise OrchestratorError('conductor accept')
    if accept.get('scout_hunt_sha256') != SCOUT_SHA256:
        raise OrchestratorError('conductor accept')
    if accept.get('panel_stub_sha256') != PANEL_STUB_SHA256:
        raise OrchestratorError('conductor accept')
    if accept.get('knob') != KNOB:
        raise OrchestratorError('conductor accept')
    if accept.get('arm_values') != ANALYSIS_SLICE:
        raise OrchestratorError('conductor accept')
    if accept.get('does_not_ungate') != list(DOES_NOT_UNGATE):
        raise UngateRefused()
    if accept.get('post_nhlfq_main') != BASE_COMMIT:
        raise OrchestratorError('conductor accept')
    if accept.get('lab_dir') != LAB_DIRECTORY + '/':
        raise OrchestratorError('conductor accept')
    if accept.get('panel_version') != PANEL_VERSION:
        raise OrchestratorError('conductor accept')
    if accept.get('panel_events') != PANEL_EVENTS_N or accept.get('panel_markets') != PANEL_MARKETS_N:
        raise OrchestratorError('conductor accept')
    if accept.get('scout_markets') != SCOUT_MARKETS_N or accept.get('scout_events') != SCOUT_EVENTS_N:
        raise OrchestratorError('conductor accept')
    if accept.get('panel_full_scout') is not True or accept.get('admitted_at') is not None:
        raise OrchestratorError('conductor accept')
    if accept.get('missing_occurrence_datetime_n') != MISSING_OCC_N:
        raise OrchestratorError('conductor accept')
    integrity = accept.get('integrity') or {}
    for key in (
        'panel_markets_equal_scout',
        'missing_occ_kept',
        'event_occ_from_market_occ_only',
        'KXCPI-26NOV_event_occ_null',
    ):
        if integrity.get(key) is not True:
            raise OrchestratorError('conductor accept')
    if accept.get('results') is not None or accept.get('pnl') is not None:
        raise ScorecardPromotionRefused()
    hold = json.loads(EXAMINER_HOLD.read_text())
    if hold.get('status') != 'NOT_SCORED' or hold.get('stub_ready') is not False:
        raise ExaminerNotReady()
    if hold.get('packet') != EXPERIMENT_ID or hold.get('feature_family') != FEATURE_FAMILY:
        raise OrchestratorError('examiner hold')
    if hold.get('freeze_sha256') != FREEZE_SHA256:
        raise OrchestratorError('examiner hold')
    if sorted(hold.get('metrics_null') or []) != sorted(OUTPUT_KEYS):
        raise OrchestratorError('examiner hold')
    pre = json.loads(PRE_ACCEPT_EMPTY.read_text())
    if pre.get('note') != 'pre-ACCEPT empty':
        raise OrchestratorError('pre-accept empty')
    if 'missing_sot_n' in pre or 'settled_join_n' in pre or 'n_books' in pre:
        raise OrchestratorError('pre-accept empty')
    if pre.get('maker_vs_taker_roi_delta') is not None or pre.get('sparse_vs_fresh_gap') is not None:
        raise ScorecardPromotionRefused()
    if pre.get('results') is not None or pre.get('pnl') is not None:
        raise ScorecardPromotionRefused()
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
    if payload.get('purpose') != PURPOSE:
        raise OrchestratorError('purpose')
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
    if not admitted and payload.get('stub_status') != STUB_STATUS:
        raise OrchestratorError('stub_status')
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
        expected = event_occurrence_from_markets(name, markets)
        if event.get('occurrence_datetime') != expected:
            raise InventedSoTRefused()
        if name == NOV_EVENT and expected is not None:
            raise InventedSoTRefused()
        claimed = event.get('markets_n')
        actual = sum(1 for market in markets if market.get('event_ticker') == name)
        if claimed != actual:
            raise OrchestratorError('event markets')
        event_names.append(name)
    if set(event_names) != index['events']:
        raise OrchestratorError('events')
    for market in markets:
        seen.append(_assert_market_object(market, index))
    if set(seen) != set(index['by_ticker']):
        raise InventedMarketRefused()
    missing = 0
    sparse = 0
    for market in markets:
        if 'occurrence_datetime' not in market:
            missing += 1
        elif market.get('occurrence_datetime') is None:
            missing += 1
        elif not isinstance(market.get('occurrence_datetime'), str) or not market.get('occurrence_datetime').endswith('Z'):
            raise InventedSoTRefused()
        if market.get('volume_24h_fp') == SPARSE_24H_TOKEN:
            sparse += 1
    if missing != MISSING_OCC_N:
        raise OrchestratorError('missing occurrence')
    if sparse != SPARSE_24H_N:
        raise OrchestratorError('sparse 24h')
    nov = [event for event in events if event.get('event_ticker') == NOV_EVENT]
    if len(nov) != 1 or nov[0].get('occurrence_datetime') is not None:
        raise InventedSoTRefused()
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
    cpi = probe_examiner_fee(SERIES)
    nfl = probe_examiner_fee(NFL_POINTER_SERIES)
    if cpi != nfl:
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
    if set(market['ticker'] for market in panel['markets']) != set(index['by_ticker']):
        raise InventedMarketRefused()
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
        'panel_full_scout': True,
        'panel_markets_equal_scout': True,
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
        'probe_formula_id': cpi['formula_id'],
        'probe_series_resolution': cpi['series_resolution'],
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
        'nhl_fq_reopen': False,
        'admit_py_run': False,
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
    extra = {
        'event_count': len(events),
        'market_count': len(markets),
        'scout_markets_n': scout_index()['markets_n'],
        'scout_events_n': scout_index()['events_n'],
        'panel_full_scout': True,
    }
    if arm == C4A1:
        bins = panel_honesty_bins(panel)
        extra['honesty_bins'] = bins
        extra['honesty_bin_count'] = len(bins)
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


def load_synthetic_sparse(path=None):
    path = SYNTHETIC_SPARSE if path is None else Path(path)
    payload = json.loads(Path(path).read_text())
    if payload.get('source') != 'synthetic_schema_standin':
        raise OrchestratorError('source')
    rows = payload.get('rows')
    if not isinstance(rows, list) or len(rows) < 2:
        raise OrchestratorError('synthetic rows')
    return rows


def conduct_native(path=None):
    """C4A0 schema on synthetic native rows. Does not write the freeze scorecard."""
    rows = partition_native(load_synthetic_trades(path))
    return _report(C4A0, 'synthetic_schema_standin', {
        'partitions': rows,
        'partition_count': len(rows),
    })


def conduct_sparse(path=None):
    """C4A1 schema on synthetic book rows. The gap stays null."""
    rows = partition_sparse(load_synthetic_sparse(path))
    return _report(C4A1, 'synthetic_schema_standin', {
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
