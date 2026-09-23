"""R3-P3 favorite-longshot maker/taker bands harness.

Measurement only. Imports the R1-P1 feebook for a formula-id schema check.
This module does not edit that lab, does not edit rails, C3, or C5, does not
trade, does not read Logan keys, and does not write scorecard metrics.
Lee-Ready is refused. Native taker fields are the only side partition.
"""
import hashlib
import json
import sys
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PARENT = ROOT.parent
FEEBOOK_DIR = PARENT / 'kalshi_feebook_lab_20260922'
RAILS_DIR = PARENT / 'kalshi_rails_lab_20260922'
for _path in (FEEBOOK_DIR, RAILS_DIR):
    if str(_path) not in sys.path:
        sys.path.insert(0, str(_path))

import feebook
import rails

LAB_DIRECTORY = 'kalshi_r3p3_fl_maker_taker_lab_20260923'
EXPERIMENT_ID = 'R3-P3-FL-MAKER-TAKER-HARNESS'
PANEL_PACKET_ID = 'R3-P3-FL-MAKER-TAKER'
PANEL_VERSION = '2026-09-22.r3-p3-fl-maker-taker-v0'
REGISTRY_ID = 'astra.r3p3.fl_maker_taker.price_bands_10c.v0'
KNOB = 'analysis_slice'
R3P3A0 = 'R3P3A0'
R3P3A1 = 'R3P3A1'
ARMS = (R3P3A0, R3P3A1)
SLICES = {
    R3P3A0: 'maker_vs_taker',
    R3P3A1: 'fl_bands_10c',
}
FEEBOOK_COMMIT = '22371178cb2663250b4762f328069571c48cb551'
RAILS_COMMIT = '6a28e0d6254327ea4e6451c781bec56215ac6cac'
UNTOUCHED_BASE = '637644966bae3737b52ab35826d3a63bf4b9b936'
PACKET_SHA256 = 'fbc58539b7a469d005b7f75b786efddecc1028a3bb0da601bc0082c9d4aab179'
KERNEL_SHA256 = '0ed697149136acb3aa840aeeb79d11c8f6ef80f37ce4dd692a3cb690212206a7'
PANEL_STUB_SHA256 = '6f640dd3a6091ba6b896ded38fdded4676583aa3c885223da21ddf03780250c0'
BANDS_REGISTRY_SHA256 = '0860cbe28d28ecc6142ddf6f1ebb67792084264ed82e0b4d868c3b3138ea5312'
PUBLIC_HOST = 'https://api.elections.kalshi.com/trade-api/v2'
OUT_OF_SCOPE_ROUTE = 'POST /portfolio/orders'
LEE_READY_ROUTE = 'Lee-Ready aggressor inference'
SCORECARD_FIELDS = (
    'mz_alpha',
    'mz_psi',
    'post_fee_roi_by_band',
    'maker_vs_taker_roi_delta',
    'settled_join_n',
)
OUTPUT_KEYS = SCORECARD_FIELDS + ('results', 'pnl')
ADVERSARY_LABELS = {
    'paper_ev': 'paper EV is hypothesis only',
    'paper_26pct': 'paper +2.6% is hypothesis only',
    'paper_maker_50c': 'paper maker at or above 50 cents is hypothesis only',
    'author_pnl': 'author PnL is hypothesis only',
    'lee_ready': 'Lee-Ready aggressor inference is refused',
    'invented_settlement': 'invented settlement is refused',
    'invented_roi': 'invented ROI is refused',
    'invented_pnl': 'invented pnl is refused',
    'live_order': 'live orders are refused',
}
PAPER_KEYS = (
    'paper_ev',
    'author_pnl',
    'paper_26pct',
    'paper_maker_ge_50c',
    'maker_ge_50c_ev',
)
DOES_NOT_MODIFY = (
    'kalshi_feebook_lab_20260922',
    'kalshi_rails_lab_20260922',
    'kalshi_capital_structure_lab_20260922',
    'kalshi_soft_blended_reserves_000_lab_20260923',
    'kalshi_queue_fragility_000_lab_20260922',
    'kalshi_examiner_fee_queue_honesty_000_lab_20260922',
    'kalshi_c1_kxufcfight_honesty_lab_20260922',
    'kalshi_c3_kxhighny_bordering_lab_20260923',
    'kalshi_c5_kxbtc15m_honesty_lab_20260923',
    'kalshi_r2p1_hygiene_000_lab_20260922',
    'kalshi_r3_p1_fee_cost_lab_20260922',
    'kalshi_r3_p4_l2_shape_lab_20260922',
    'nfl_factorial_lab_20260921',
    'nfl_paircheck_lab_20260922',
)
PACKET_NAME = 'R3_P3_FL_MAKER_TAKER_HARNESS_FREEZE_2026-09-23.md'
KERNEL_NAME = 'R3-P3_FL_MAKER_TAKER_BANDS_FREEZE_KERNEL_2026-09-22.md'
PACKET = ROOT / PACKET_NAME
KERNEL = ROOT / KERNEL_NAME
LAB_BUNDLE = ROOT / 'R3_P3_FL_MAKER_TAKER_HARNESS'
GOVERNANCE_BUNDLE = PARENT / 'packets' / 'R3_P3_FL_MAKER_TAKER_HARNESS'
GOVERNANCE_TREE = PARENT / 'lab' / 'governance' / 'astra' / 'packets'
FROZEN_EXPERIMENT = ROOT / 'FROZEN_EXPERIMENT.json'
EMPTY_RESULTS = ROOT / 'results' / 'EMPTY_RESULTS.json'
CAPTURE_DIR = PARENT / 'lab' / 'astra-capture' / 'r3-p3-fl-maker-taker'
PANEL_STUB = CAPTURE_DIR / 'panel_stub.json'
PANEL_ADMITTED = CAPTURE_DIR / 'panel_admitted.json'
BANDS_REGISTRY = CAPTURE_DIR / 'bands_registry_10c.json'
SYNTHETIC_TRADES = ROOT / 'fixtures' / 'synthetic_trades.json'
C3_FROZEN = (
    PARENT / 'kalshi_c3_kxhighny_bordering_lab_20260923' / 'FROZEN_EXPERIMENT.json'
)
C5_FROZEN = (
    PARENT / 'kalshi_c5_kxbtc15m_honesty_lab_20260923' / 'FROZEN_EXPERIMENT.json'
)
STUB_TRADES_N = 15
STUB_MARKETS_N = 3
STUB_EVENTS_N = 2
STUB_SERIES_N = 2
STUB_SETTLED_N = 0
EXPECTED_BANDS = (
    ('b00', '[0-0.10)', '0.0', '0.1', True, False),
    ('b01', '[0.10-0.20)', '0.1', '0.2', True, False),
    ('b02', '[0.20-0.30)', '0.2', '0.3', True, False),
    ('b03', '[0.30-0.40)', '0.3', '0.4', True, False),
    ('b04', '[0.40-0.50)', '0.4', '0.5', True, False),
    ('b05', '[0.50-0.60)', '0.5', '0.6', True, False),
    ('b06', '[0.60-0.70)', '0.6', '0.7', True, False),
    ('b07', '[0.70-0.80)', '0.7', '0.8', True, False),
    ('b08', '[0.80-0.90)', '0.8', '0.9', True, False),
    ('b09', '[0.90-1.00]', '0.9', '1.0', True, True),
)
ROI_KEYS = (
    'post_fee_roi',
    'maker_vs_taker_roi_delta',
    'mz_alpha',
    'mz_psi',
    'results',
    'pnl',
)


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
    """Paper EV, author PnL, or an invented ROI label was requested."""

    def __init__(self, label):
        self.label = label
        super().__init__(label)


class LeeReadyRefused(OrchestratorError):
    """Native taker fields only. Aggressor inference is refused."""

    def __init__(self):
        super().__init__('Lee-Ready refused')


class PanelVersionRefused(OrchestratorError):
    """The panel file is not the pinned R3-P3 seed."""

    def __init__(self):
        super().__init__('panel_version')


class ShadowFeeLiteralRefused(OrchestratorError):
    """A fee quote bypassed the examiner feebook formula."""

    def __init__(self):
        super().__init__('shadow fee literal')


class InventedSettlementRefused(OrchestratorError):
    """A resolution was filled without Examiner."""

    def __init__(self):
        super().__init__('invented settlement')


class InventedRoiRefused(OrchestratorError):
    """An ROI or MZ figure was filled without Examiner."""

    def __init__(self):
        super().__init__('invented ROI')


class InventedFillRefused(OrchestratorError):
    """Volume or open interest was filled without Examiner."""

    def __init__(self):
        super().__init__('invented fill')


class UnknownSlice(OrchestratorError):
    """The only knob is maker_vs_taker or fl_bands_10c."""

    def __init__(self):
        super().__init__('analysis_slice')


class AdmitRefused(OrchestratorError):
    """Clock owns admit. This harness does not run it."""

    def __init__(self):
        super().__init__('admit refused')


def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def execution_adapter():
    """No live order client lives in this lab."""
    raise LiveOrdersForbidden()


def run_admit():
    """Collector and Clock own admit. This function does not run it."""
    raise AdmitRefused()


def assert_public_get(method):
    """GET is the only public capture verb. This function does not open a socket."""
    if method != 'GET':
        raise LiveOrdersForbidden()
    return None


def infer_aggressor(*_args, **_kwargs):
    """Lee-Ready and every other aggressor inference stay refused."""
    raise LeeReadyRefused()


def refuse_adversary(label):
    """Named adversary labels. Nothing is traded and no EV is imported."""
    if label not in ADVERSARY_LABELS:
        raise OrchestratorError('adversary label')
    raise AdversaryRefused(ADVERSARY_LABELS[label])


def assert_examiner_quote(quote):
    """Accept only the R1-P1 examiner formula. The numeric fee is not stored."""
    if not isinstance(quote, dict):
        raise ShadowFeeLiteralRefused()
    if quote.get('formula_id') != feebook.EXAMINER_FORMULA_ID:
        raise ShadowFeeLiteralRefused()
    return quote


def fee_schema_object():
    """Formula id and pin only. ROI and the numeric fee stay off the object."""
    formula_ids = []
    for role in ('maker', 'taker'):
        quote = feebook.order_fee(role, '1', '0.50', round_up=True)
        assert_examiner_quote(quote)
        formula_ids.append(quote['formula_id'])
    if formula_ids[0] != formula_ids[1]:
        raise OrchestratorError('examiner formula')
    return {
        'formula_id': feebook.EXAMINER_FORMULA_ID,
        'fee_pin': FEEBOOK_COMMIT,
        'fee_lab': 'kalshi_feebook_lab_20260922',
        'roles': ('maker', 'taker'),
        'numeric_fee_stored': False,
        'roi': None,
        'post_fee_roi': None,
    }


def _decimal_bound(value, name):
    if isinstance(value, bool):
        raise OrchestratorError(name)
    if isinstance(value, float):
        return Decimal(str(value))
    return feebook.as_decimal(value, name)


def _paper_claimed(value):
    if value is None or value is False:
        return False
    return True


def _refuse_evidence_labels(row):
    if not isinstance(row, dict):
        raise OrchestratorError('row')
    for key in PAPER_KEYS:
        if _paper_claimed(row.get(key)):
            raise AdversaryRefused(ADVERSARY_LABELS['paper_ev'])
    if row.get('live_order') is True:
        raise LiveOrdersForbidden()
    for key in ('results', 'pnl'):
        if key in row and row[key] is not None:
            raise ScorecardPromotionRefused()


def _require_null(payload, key):
    if key not in payload or payload[key] is not None:
        raise ScorecardPromotionRefused()


def _validate_registry(payload):
    if not isinstance(payload, dict):
        raise OrchestratorError('bands')
    _refuse_evidence_labels(payload)
    if payload.get('registry_id') != REGISTRY_ID:
        raise OrchestratorError('bands')
    if payload.get('panel_version') != PANEL_VERSION:
        raise PanelVersionRefused()
    if payload.get('pre_registered_before_outcome_join') is not True:
        raise OrchestratorError('bands')
    if payload.get('measurement_roi_by_band') is not None:
        raise InventedRoiRefused()
    raw_bands = payload.get('bands')
    if not isinstance(raw_bands, list) or len(raw_bands) != len(EXPECTED_BANDS):
        raise OrchestratorError('bands')
    normalized = []
    for raw, expected in zip(raw_bands, EXPECTED_BANDS):
        band_id, label, lo, hi, lo_inclusive, hi_inclusive = expected
        if raw.get('band_id') != band_id or raw.get('label') != label:
            raise OrchestratorError('bands')
        if raw.get('lo_inclusive') is not lo_inclusive or raw.get('hi_inclusive') is not hi_inclusive:
            raise OrchestratorError('bands')
        price_lo = _decimal_bound(raw.get('price_lo'), 'price_lo')
        price_hi = _decimal_bound(raw.get('price_hi'), 'price_hi')
        if price_lo != Decimal(lo) or price_hi != Decimal(hi):
            raise OrchestratorError('bands')
        normalized.append({
            'band_id': band_id,
            'label': label,
            'price_lo': price_lo,
            'price_hi': price_hi,
            'lo_inclusive': lo_inclusive,
            'hi_inclusive': hi_inclusive,
        })
    return normalized


def load_bands_registry(path=None):
    """Pre-registered 10¢ bands. The canonical file is hash-pinned."""
    path = BANDS_REGISTRY if path is None else Path(path)
    if path.resolve() == BANDS_REGISTRY.resolve():
        if sha256_file(path) != BANDS_REGISTRY_SHA256:
            raise OrchestratorError('bands sha256')
    return _validate_registry(json.loads(path.read_text()))


def assign_band(price, bands=None):
    """One registry band for a yes price. No outcome is consulted."""
    if bands is None:
        bands = load_bands_registry()
    price = feebook.as_decimal(price, 'yes_price_dollars')
    if price < 0 or price > 1:
        raise OrchestratorError('price')
    matches = []
    for band in bands:
        if band['lo_inclusive']:
            lo_ok = price >= band['price_lo']
        else:
            lo_ok = price > band['price_lo']
        if band['hi_inclusive']:
            hi_ok = price <= band['price_hi']
        else:
            hi_ok = price < band['price_hi']
        if lo_ok and hi_ok:
            matches.append(band['band_id'])
    if len(matches) != 1:
        raise OrchestratorError('band')
    return matches[0]


def normalize_trade(trade, bands):
    """Native taker fields plus one band id. ROI stays null."""
    _refuse_evidence_labels(trade)
    outcome = trade.get('taker_outcome_side')
    book = trade.get('taker_book_side')
    if outcome not in ('yes', 'no'):
        raise OrchestratorError('taker_outcome_side')
    if book not in ('bid', 'ask'):
        raise OrchestratorError('taker_book_side')
    alias = trade.get('taker_side')
    if alias is not None and alias != outcome:
        raise OrchestratorError('taker_side')
    if trade.get('taker_action') is not None:
        raise OrchestratorError('taker_action')
    if trade.get('lee_ready') != 'REFUSED':
        raise LeeReadyRefused()
    if trade.get('aggressor_inference') is not None:
        raise LeeReadyRefused()
    price = trade.get('yes_price_dollars')
    if price is None:
        raise OrchestratorError('yes_price_dollars')
    band_id = assign_band(price, bands)
    declared = trade.get('band_id')
    if declared is not None and declared != band_id:
        raise OrchestratorError('band')
    for key in ROI_KEYS:
        if key in trade and trade[key] is not None:
            raise InventedRoiRefused()
    if trade.get('result') is not None or trade.get('settlement_ts') is not None:
        raise InventedSettlementRefused()
    trade_id = trade.get('trade_id')
    ticker = trade.get('ticker')
    if not isinstance(trade_id, str) or not isinstance(ticker, str):
        raise OrchestratorError('trade')
    return {
        'trade_id': trade_id,
        'ticker': ticker,
        'taker_outcome_side': outcome,
        'taker_book_side': book,
        'band_id': band_id,
        'lee_ready': 'REFUSED',
        'aggressor_inference': None,
        'post_fee_roi': None,
    }


def _scorecard_row(row):
    for key in OUTPUT_KEYS:
        row[key] = None
    return row


def partition_rows(trades):
    """Group by native taker_outcome_side and taker_book_side."""
    grouped = {}
    for trade in trades:
        key = (trade['taker_outcome_side'], trade['taker_book_side'])
        grouped.setdefault(key, []).append(trade['trade_id'])
    rows = []
    for outcome, book in sorted(grouped):
        trade_ids = grouped[(outcome, book)]
        row = {
            'taker_outcome_side': outcome,
            'taker_book_side': book,
            'trade_n': len(trade_ids),
            'trade_ids': trade_ids,
            'lee_ready': 'REFUSED',
            'aggressor_inference': None,
            'fee_schema': fee_schema_object(),
            'post_fee_roi': None,
        }
        rows.append(_scorecard_row(row))
    return rows


def band_rows(trades, bands):
    """One schema object per pre-registered band, including empty bands."""
    by_band = {band['band_id']: [] for band in bands}
    for trade in trades:
        by_band[trade['band_id']].append(trade['trade_id'])
    rows = []
    for band in bands:
        trade_ids = by_band[band['band_id']]
        row = {
            'band_id': band['band_id'],
            'label': band['label'],
            'price_lo': str(band['price_lo']),
            'price_hi': str(band['price_hi']),
            'lo_inclusive': band['lo_inclusive'],
            'hi_inclusive': band['hi_inclusive'],
            'trade_n': len(trade_ids),
            'trade_ids': trade_ids,
            'lee_ready': 'REFUSED',
            'fee_schema': fee_schema_object(),
            'post_fee_roi': None,
        }
        rows.append(_scorecard_row(row))
    return rows


def _assert_freeze_bytes():
    copies = (
        PACKET,
        LAB_BUNDLE / PACKET_NAME,
        PARENT / 'packets' / PACKET_NAME,
        GOVERNANCE_BUNDLE / PACKET_NAME,
    )
    for path in copies:
        if sha256_file(path) != PACKET_SHA256:
            raise OrchestratorError('packet sha256')
    kernels = (
        KERNEL,
        LAB_BUNDLE / KERNEL_NAME,
        PARENT / 'packets' / KERNEL_NAME,
        GOVERNANCE_BUNDLE / KERNEL_NAME,
    )
    for path in kernels:
        if sha256_file(path) != KERNEL_SHA256:
            raise OrchestratorError('kernel sha256')


def select_panel_path(stub_path=None, admitted_path=None):
    """Prefer panel_admitted.json when the file exists. Otherwise the stub."""
    stub_path = PANEL_STUB if stub_path is None else Path(stub_path)
    admitted_path = PANEL_ADMITTED if admitted_path is None else Path(admitted_path)
    if Path(admitted_path).is_file():
        return Path(admitted_path)
    if not Path(stub_path).is_file():
        raise OrchestratorError('panel stub')
    return Path(stub_path)


def _same_band_bounds(embedded, registry):
    if len(embedded) != len(registry):
        return False
    for raw, band in zip(embedded, registry):
        if raw.get('band_id') != band['band_id']:
            return False
        if _decimal_bound(raw.get('price_lo'), 'price_lo') != band['price_lo']:
            return False
        if _decimal_bound(raw.get('price_hi'), 'price_hi') != band['price_hi']:
            return False
        if raw.get('lo_inclusive') is not band['lo_inclusive']:
            return False
        if raw.get('hi_inclusive') is not band['hi_inclusive']:
            return False
    return True


def _validate_panel(payload, bands, admitted):
    if not isinstance(payload, dict):
        raise OrchestratorError('panel')
    _refuse_evidence_labels(payload)
    if payload.get('panel_version') != PANEL_VERSION:
        raise PanelVersionRefused()
    if payload.get('packet_id') != PANEL_PACKET_ID:
        raise OrchestratorError('packet')
    if payload.get('c3_strategy_merge') is True:
        raise AdversaryRefused(ADVERSARY_LABELS['paper_ev'])
    cite = payload.get('c3_prefer_cite') or ''
    if not isinstance(cite, str) or not cite:
        raise OrchestratorError('c3 cite')
    stamp = payload.get('admitted_at')
    if admitted:
        if not isinstance(stamp, str) or not stamp.endswith('Z'):
            raise OrchestratorError('admitted_at')
    elif stamp is not None:
        raise OrchestratorError('admitted_at')
    for key in ('results', 'pnl', 'volume'):
        _require_null(payload, key)
    binds = payload.get('binds') or {}
    if binds.get('fee_lab_sha') != FEEBOOK_COMMIT:
        raise OrchestratorError('feebook commit')
    if binds.get('rails_lab_sha') != RAILS_COMMIT:
        raise OrchestratorError('rails commit')
    if binds.get('fee_formula_id') != feebook.EXAMINER_FORMULA_ID:
        raise OrchestratorError('examiner formula')
    if binds.get('no_lee_ready') is not True:
        raise LeeReadyRefused()
    if binds.get('no_live_orders') is not True:
        raise LiveOrdersForbidden()
    if binds.get('no_000_retune') is not True:
        raise OrchestratorError('000 retune')
    if binds.get('forbid_inherited_q7_fee_literals') is not True:
        raise ShadowFeeLiteralRefused()
    if binds.get('refuse_paper_26pct_as_evidence') is not True:
        raise AdversaryRefused(ADVERSARY_LABELS['paper_26pct'])
    if binds.get('bands_pre_registered_before_outcome_join') is not True:
        raise OrchestratorError('bands')
    if binds.get('bands_registry') != REGISTRY_ID:
        raise OrchestratorError('bands')
    capture = payload.get('capture') or {}
    if capture.get('mode') != 'GET_only_public':
        raise LiveOrdersForbidden()
    if capture.get('host_allowlist') != [PUBLIC_HOST]:
        raise LiveOrdersForbidden()
    routes = capture.get('out_of_scope_routes') or []
    if OUT_OF_SCOPE_ROUTE not in routes or LEE_READY_ROUTE not in routes:
        raise LiveOrdersForbidden()
    schedule = capture.get('schedule') or {}
    if schedule.get('recorder_started') is True or schedule.get('admit_py_run') is True:
        raise AdmitRefused()
    preferred = (payload.get('series_preference') or {}).get('preferred') or []
    if 'KXHIGHNY' not in preferred or 'KXHIGHCHI' not in preferred:
        raise OrchestratorError('series')
    embedded = (payload.get('bands_registry') or {}).get('bands') or []
    if not _same_band_bounds(embedded, bands):
        raise OrchestratorError('bands')
    if (payload.get('bands_registry') or {}).get('pre_registered_before_outcome_join') is not True:
        raise OrchestratorError('bands')
    objects = payload.get('measurement_objects') or {}
    mz = objects.get('MZ_mincer_zarnowitz') or {}
    roi = objects.get('post_fee_ROI_by_10c_band') or {}
    side = objects.get('maker_vs_taker_slice') or {}
    if mz.get('values') is not None or roi.get('values_by_band') is not None:
        raise ScorecardPromotionRefused()
    if side.get('values') is not None:
        raise ScorecardPromotionRefused()
    if not mz or not roi or not side:
        raise OrchestratorError('measurement')
    events = payload.get('events') or []
    markets = payload.get('markets') or []
    trades = payload.get('trades_sample') or []
    counts = payload.get('cohort_counts') or {}
    if admitted:
        if len(trades) < 1 or len(markets) < 1 or len(events) < 1:
            raise OrchestratorError('cohort')
        if counts.get('settled_markets_resolved_n') not in (None, 0):
            raise InventedSettlementRefused()
    else:
        if len(trades) != STUB_TRADES_N or len(markets) != STUB_MARKETS_N:
            raise OrchestratorError('cohort')
        if len(events) != STUB_EVENTS_N:
            raise OrchestratorError('cohort')
        if counts.get('trades_sampled_n') != STUB_TRADES_N:
            raise OrchestratorError('cohort')
        if counts.get('markets_n') != STUB_MARKETS_N or counts.get('events_n') != STUB_EVENTS_N:
            raise OrchestratorError('cohort')
        if counts.get('series_n') != STUB_SERIES_N:
            raise OrchestratorError('cohort')
        if counts.get('settled_markets_resolved_n') != STUB_SETTLED_N:
            raise InventedSettlementRefused()
    for event in events:
        if event.get('panel_version') != PANEL_VERSION:
            raise PanelVersionRefused()
        event_stamp = event.get('admitted_at')
        if admitted:
            if event_stamp not in (None, stamp):
                raise OrchestratorError('admitted_at')
        elif event_stamp is not None:
            raise OrchestratorError('admitted_at')
        for key in ('volume_fp', 'open_interest_fp'):
            if event.get(key) is not None:
                raise InventedFillRefused()
    for market in markets:
        if market.get('panel_version') != PANEL_VERSION:
            raise PanelVersionRefused()
        market_stamp = market.get('admitted_at')
        if admitted:
            if market_stamp not in (None, stamp):
                raise OrchestratorError('admitted_at')
        elif market_stamp is not None:
            raise OrchestratorError('admitted_at')
        if market.get('result') is not None or market.get('settlement_ts') is not None:
            raise InventedSettlementRefused()
        for key in ('volume_fp', 'open_interest_fp'):
            if market.get(key) is not None:
                raise InventedFillRefused()
    for trade in trades:
        normalize_trade(trade, bands)
    return payload


def load_panel(stub_path=None, admitted_path=None):
    """Stub by default. panel_admitted.json wins when it is on disk."""
    path = select_panel_path(stub_path, admitted_path)
    bands = load_bands_registry()
    if path.resolve() == PANEL_STUB.resolve():
        _assert_freeze_bytes()
        if sha256_file(PANEL_STUB) != PANEL_STUB_SHA256:
            raise OrchestratorError('stub sha256')
    payload = json.loads(path.read_text())
    return _validate_panel(payload, bands, admitted=path.name == 'panel_admitted.json')


def arm_table():
    return tuple({'id': arm, 'slice': SLICES[arm]} for arm in ARMS)


def instrument_binding(panel=None):
    """One analysis-slice knob. Fee commit stays fixed. No scorecard fill."""
    if panel is None:
        panel = load_panel()
    schema = fee_schema_object()
    if schema['formula_id'] != feebook.EXAMINER_FORMULA_ID:
        raise OrchestratorError('examiner formula')
    if schema['numeric_fee_stored'] is not False:
        raise InventedRoiRefused()
    if 'fee' in schema or 'raw' in schema or schema['roi'] is not None:
        raise InventedRoiRefused()
    if rails.FEE_CREDIT_RULE_ID != 'astra.r1p5.rails.maker_credit_floor_cent.v1':
        raise OrchestratorError('rails rule')
    return {
        'experiment_id': EXPERIMENT_ID,
        'lab_directory': LAB_DIRECTORY,
        'knob': KNOB,
        'arms': arm_table(),
        'panel_version': panel['panel_version'],
        'admitted_at': panel.get('admitted_at'),
        'strategy_pointer': None,
        'lee_ready': False,
        'paper_ev': False,
        'feebook_commit': FEEBOOK_COMMIT,
        'rails_commit': RAILS_COMMIT,
        'examiner_formula_id': feebook.EXAMINER_FORMULA_ID,
        'fee_credit_rule_id': rails.FEE_CREDIT_RULE_ID,
        'fee_source': 'feebook',
        'rails_source': 'rails',
        'fee_schema_formula_id': schema['formula_id'],
        'numeric_fee_stored': False,
        'freshness_is_scorecard': False,
        'c3_prefer_cite': panel.get('c3_prefer_cite'),
        'c3_strategy_merge': False,
        'logan_keys_required': False,
        'live_orders': False,
        'signal_retune_000': False,
        'queue_fragility_reopen': False,
        'cap_sr_reopen': False,
        'c3_reopen': False,
        'c5_reopen': False,
        'fee_is_knob': False,
        'scorecard_fields': SCORECARD_FIELDS,
        'kernel_sha256': KERNEL_SHA256,
        'packet_sha256': PACKET_SHA256,
        'panel_stub_sha256': PANEL_STUB_SHA256,
        'bands_registry_sha256': BANDS_REGISTRY_SHA256,
    }


def published_scorecard():
    """Freeze outputs. Every instrument field is present and null."""
    scorecard = {key: None for key in OUTPUT_KEYS}
    for key in OUTPUT_KEYS:
        if scorecard[key] is not None:
            raise ScorecardPromotionRefused()
    scorecard['status'] = 'EMPTY_RESULTS_PRE_EXAMINER'
    scorecard['lee_ready'] = 'REFUSED'
    scorecard['paper_ev'] = False
    return scorecard


def assert_null_scorecard(payload):
    """Require every instrument field, results, and pnl, and require null."""
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


def _assert_schema_rows(rows):
    for row in rows:
        assert_null_scorecard(row)
        schema = row['fee_schema']
        if schema['formula_id'] != feebook.EXAMINER_FORMULA_ID:
            raise OrchestratorError('examiner formula')
        if schema['fee_pin'] != FEEBOOK_COMMIT:
            raise OrchestratorError('feebook commit')
        if schema['roi'] is not None or schema['post_fee_roi'] is not None:
            raise InventedRoiRefused()
        if schema['numeric_fee_stored'] is not False:
            raise InventedRoiRefused()
        if 'fee' in schema or 'raw' in schema:
            raise InventedRoiRefused()
        if row.get('lee_ready') != 'REFUSED' or row.get('aggressor_inference') is not None:
            raise LeeReadyRefused()


def _report(arm, trades, source, panel):
    if arm not in SLICES:
        raise UnknownSlice()
    if not trades:
        raise OrchestratorError('trades')
    bands = load_bands_registry()
    published = published_scorecard()
    report = {
        'experiment_id': EXPERIMENT_ID,
        'arm': arm,
        'slice': SLICES[arm],
        'source': source,
        'fee_pin': FEEBOOK_COMMIT,
        'rails_pin': RAILS_COMMIT,
        'lee_ready': 'REFUSED',
        'paper_ev': False,
        'promoted': False,
        'strategy_pointer': None,
        'live_orders': False,
        'logan_keys_required': False,
        'signal_retune_000': False,
        'queue_fragility_reopen': False,
        'published': published,
        'settled_join': [],
    }
    if source == 'panel':
        report['panel_version'] = panel['panel_version']
        report['admitted_at'] = panel.get('admitted_at')
        report['panel_settled_markets_resolved_n'] = (
            panel.get('cohort_counts') or {}
        ).get('settled_markets_resolved_n')
    if arm == R3P3A0:
        report['partitions'] = partition_rows(trades)
        _assert_schema_rows(report['partitions'])
    else:
        report['bands'] = band_rows(trades, bands)
        _assert_schema_rows(report['bands'])
    for key in OUTPUT_KEYS:
        report[key] = None
    assert_null_scorecard(report)
    assert_null_scorecard(published)
    if report['settled_join'] != []:
        raise InventedSettlementRefused()
    return report


def conduct(arm, panel=None):
    """Schema for one analysis slice. Scorecard fields stay null."""
    if arm not in SLICES:
        raise UnknownSlice()
    if panel is None:
        panel = load_panel()
    bands = load_bands_registry()
    trades = [normalize_trade(trade, bands) for trade in panel['trades_sample']]
    return _report(arm, trades, 'panel', panel)


def load_synthetic_trades(path=None):
    """Band stand-in. Not a live GET and not a panel fill."""
    path = SYNTHETIC_TRADES if path is None else Path(path)
    payload = json.loads(Path(path).read_text())
    if payload.get('source') != 'synthetic_schema_standin':
        raise OrchestratorError('source')
    _refuse_evidence_labels(payload)
    trades = payload.get('trades')
    if not isinstance(trades, list) or len(trades) < 1:
        raise OrchestratorError('synthetic trades')
    bands = load_bands_registry()
    return [normalize_trade(trade, bands) for trade in trades]


def conduct_synthetic(arm, path=None):
    """In-memory slice schema. Does not write the freeze scorecard."""
    if arm not in SLICES:
        raise UnknownSlice()
    trades = load_synthetic_trades(path)
    return _report(arm, trades, 'synthetic_schema_standin', None)


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
        if name not in ('frozen', 'bundle_frozen', 'governance_frozen'):
            for key in SCORECARD_FIELDS:
                if key not in payload or payload[key] is not None:
                    raise ScorecardPromotionRefused()
                snapshot['%s.%s' % (name, key)] = None
    return snapshot
