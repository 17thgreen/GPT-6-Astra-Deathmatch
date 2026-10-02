"""Q6S5 KXMLBSPREAD strategy-fill measurement path.

One knob: fill_model. The implemented model is
public_trade_through_conservative. mechanic_demo_observed cells stay
null. Parent arms Q6S5A0 and Q6S5A1 keep the fee+queue slices.

This module does not place orders, does not read Logan keys, does not
open ADMIT-1 capture.sqlite, does not recreate missing queue bytes, and
does not write results, pnl, or arm ROI.
"""
import hashlib
import importlib.util
import json
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PARENT = ROOT.parent
LAB_DIRECTORY = 'kalshi_q6s5_kxmlbspread_strategy_fill_lab_20260925'
EXPERIMENT_ID = 'Q6S5-KXMLBSPREAD-STRATEGY-FILL'
FEATURE_FAMILY = 'Q6S5-MLBSPREAD-STRATEGY-FILL'
SERIES = 'KXMLBSPREAD'
FORBIDDEN_SERIES = 'KXMLBGAME'
KNOB = 'fill_model'
IMPLEMENTED_MODEL = 'public_trade_through_conservative'
UNAVAILABLE_MODEL = 'mechanic_demo_observed'
Q6S5A0 = 'Q6S5A0'
Q6S5A1 = 'Q6S5A1'
ARMS = {
    Q6S5A0: 'maker_vs_taker_native',
    Q6S5A1: 'content_fresh_vs_stale_bin',
}
FEEBOOK_COMMIT = '22371178cb2663250b4762f328069571c48cb551'
RAILS_COMMIT = '6a28e0d6254327ea4e6451c781bec56215ac6cac'
PARENT_FREEZE_SHA256 = '4f65dcdf536755b9f7dc2449c2dcd90b2df74cdf99a441b676f1a71c4d709c6e'
PANEL_STUB_SHA256 = 'c7f1f1f4ca263838c4600ed46db8f525b68efc5399a567bd60929d18d76803cc'
PANEL_VERSION = '2026-09-25.q6s5-kxmlbspread-v0'
ACCEPT_SHA256 = 'c6f95b32a9224a6beede1a8c0e3d7f0a5a4530cc8b3d0b9d997995f65d64f8f3'
FREEZE_SHA256 = '9f50ba19694083c774bbe2a6cff491d1a2f81ed3a6f9cc21a3641a938c84955d'
KICK_SHA256_PREFIX = 'dc19794b'
ADMIT1_RULING_PREFIX = 'ac7cfe63'
MISSING_QUEUE_PREFIX = '08aa54de'
FEE_TYPE = 'quadratic'
FEE_MULTIPLIER = '0.5'
FEE_LABEL = 'CACHE_NOT_R1P1'
ADMIT1_WINDOW_START = datetime(2026, 9, 27, 0, 0, tzinfo=timezone.utc)
ADMIT1_WINDOW_END = datetime(2026, 9, 30, 4, 0, tzinfo=timezone.utc)
OUTPUT_KEYS = ('results', 'pnl', 'roi')
COMMON_SCORECARD_KEYS = (
    'net_pnl_without_rewards',
    'net_pnl_with_rewards',
    'rewards_actually_earned',
    'calibration',
    'fill_rate',
    'adverse_selection_after_fills',
    'feasible_vs_requested_size',
    'unresolved_inventory',
    'capital_hours',
    'drawdown',
    'event_concentration',
)
LOOKAHEAD_KEYS = (
    'settlement_ts',
    'future_book',
    'book_after_trade',
    'post_trade_mid',
    'lookahead',
)
INVENT_FILL_KEYS = ('fill', 'fills', 'contracts', 'pnl', 'roi', 'simulated_fill')
P16_COUNTS = {'satisfied': 9, 'n/a': 3, 'missing': 0}

AUTHORITY = ROOT / 'AUTHORITY_VERIFICATION.json'
FROZEN_EXPERIMENT = ROOT / 'FROZEN_EXPERIMENT.json'
EMPTY_RESULTS = ROOT / 'results' / 'EMPTY_RESULTS.json'
SOURCE_PINS = ROOT / 'SOURCE_PINS.json'
EXAMINER_HOLD = ROOT / 'EXAMINER_HOLD_Q6S5_KXMLBSPREAD_STRATEGY_FILL_PRE_PR_2026-09-29.json'
PANEL_STUB = PARENT / 'lab' / 'astra-capture' / 'q6s5-kxmlbspread' / 'panel_stub.json'
PANEL_ADMITTED = PARENT / 'lab' / 'astra-capture' / 'q6s5-kxmlbspread' / 'panel_admitted.json'
PARENT_LAB = PARENT / 'kalshi_q6s5_kxmlbspread_feequue_lab_20260925'
PARENT_FREEZE = (
    PARENT / 'lab' / 'governance' / 'astra' / 'packets'
    / 'Q6S5_KXMLBSPREAD_FEEQUEUE_HARNESS_FREEZE_2026-09-25.md'
)
PARENT_ORCHESTRATOR = PARENT_LAB / 'orchestrator.py'
ACCEPT_PATH = (
    'lab/governance/astra/packets/'
    'CONDUCTOR_ACCEPT_VARIANTS_Q6S5_STRATEGY_FILL_FREEZE_2026-09-29.json'
)
FREEZE_PATH = (
    'lab/governance/astra/packets/Q6S5_KXMLBSPREAD_STRATEGY_FILL_FREEZE_2026-09-25.md'
)
KICK_PATH = (
    'lab/governance/astra/packets/'
    'CONDUCTOR_KICK_VARIANTS_Q6S5_STRATEGY_FILL_FREEZE_2026-09-25.json'
)

_PARENT = None


class OrchestratorError(Exception):
    """The strategy-fill path refused the input."""


class Admit1WindowRejected(OrchestratorError):
    """A timestamp falls inside the ADMIT-1 exclusion window."""


class Admit1BackfillRefused(OrchestratorError):
    """Backfill into the ADMIT-1 gap is refused."""


class Admit1CaptureRefused(OrchestratorError):
    """ADMIT-1 capture.sqlite is not read."""


class LookaheadRefused(OrchestratorError):
    """The row uses information from after the quote, or a trade that is not later."""


class LeeReadyRefused(OrchestratorError):
    """Lee-Ready is refused on every input."""


class InventedFillRefused(OrchestratorError):
    """Fills, contract counts, and PnL are not invented."""


class InventedMarketRefused(OrchestratorError):
    """A ticker outside the pinned panel is refused."""


class QueueBytesNotRecreated(OrchestratorError):
    """Missing queue bytes prefixed 08aa54de are not recreated."""


class CacheNotLiveR1P1(OrchestratorError):
    """The cache fee label is not a live R1-P1 series pin."""


class LiveOrderRefused(OrchestratorError):
    """Live orders and account routes are refused."""


class AdmitPyRefused(OrchestratorError):
    """admit.py is not run."""


class DualCloudRefused(OrchestratorError):
    """A second cloud implement is refused."""


class RetuneRefused(OrchestratorError):
    """Q6-000, S1, Cap-SR, and Q6S1 stay closed."""


class ScorecardPromotionRefused(OrchestratorError):
    """results, pnl, and arm ROI stay null."""


class UnknownModel(OrchestratorError):
    """fill_model is only the declared pair."""


class UnknownArm(OrchestratorError):
    """Arms stay Q6S5A0 and Q6S5A1."""


def sha256_file(path):
    digest = hashlib.sha256()
    digest.update(Path(path).read_bytes())
    return digest.hexdigest()


def parse_ts(value):
    """Parse a UTC Z timestamp. Other shapes are refused."""
    if not isinstance(value, str) or not value.endswith('Z') or 'T' not in value:
        raise OrchestratorError('timestamp')
    try:
        parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
    except ValueError as exc:
        raise OrchestratorError('timestamp') from exc
    if parsed.tzinfo is None:
        raise OrchestratorError('timestamp')
    return parsed.astimezone(timezone.utc)


def in_admit1_window(ts):
    """Half-open window [2026-09-27T00:00:00Z, 2026-09-30T04:00:00Z)."""
    if not isinstance(ts, datetime):
        ts = parse_ts(ts)
    return ADMIT1_WINDOW_START <= ts < ADMIT1_WINDOW_END


def _parent_module():
    global _PARENT
    if _PARENT is None:
        spec = importlib.util.spec_from_file_location(
            'q6s5_feequue_orchestrator',
            PARENT_ORCHESTRATOR,
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        _PARENT = module
    return _PARENT


def parent_arms():
    """Read the fee+queue arm table. This lab does not write that module."""
    arms = dict(_parent_module().ANALYSIS_SLICE)
    if arms != ARMS:
        raise RetuneRefused('parent arms changed')
    return arms


def fee_output():
    """Cache label only. formula_id stays null. No dollar fee is returned."""
    label = {
        'series': SERIES,
        'fee_type': FEE_TYPE,
        'multiplier': FEE_MULTIPLIER,
        'label': FEE_LABEL,
        'formula_id': None,
        'cache_labeled': True,
        'live_r1p1': False,
        'fee_dollars': None,
        'results': None,
        'pnl': None,
    }
    if label['formula_id'] is not None or label['live_r1p1'] is not False:
        raise CacheNotLiveR1P1()
    if label['label'] != FEE_LABEL or label['cache_labeled'] is not True:
        raise CacheNotLiveR1P1()
    return label


def claim_live_r1p1(quote=None):
    del quote
    raise CacheNotLiveR1P1()


def live_order(path='/orders'):
    del path
    raise LiveOrderRefused()


def run_admit_py():
    raise AdmitPyRefused()


def dual_cloud():
    raise DualCloudRefused()


def retune(name):
    allowed = ('q6-000', 'q6_000', 's1', 'kxmlbgame', 'cap-sr', 'cap_sr', 'q6s1')
    if str(name).lower() not in allowed:
        raise OrchestratorError('retune')
    raise RetuneRefused(str(name))


def recreate_queue_bytes(digest=None):
    """No success path. The missing 08aa54de artifact is not rebuilt."""
    del digest
    raise QueueBytesNotRecreated()


def read_admit1_capture(path):
    """Refuse the path before any file open."""
    text = str(path).replace('\\', '/')
    if 'capture.sqlite' not in text.split('/')[-1] and not text.endswith('capture.sqlite'):
        if 'capture.sqlite' not in text:
            raise Admit1CaptureRefused()
    raise Admit1CaptureRefused()


def _mentions_capture(value):
    if not isinstance(value, str):
        return False
    return 'capture.sqlite' in value.replace('\\', '/').lower()


def _mentions_missing_queue(value):
    return isinstance(value, str) and value.lower().startswith(MISSING_QUEUE_PREFIX)


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


def infer_lee_ready(row):
    del row
    raise LeeReadyRefused()


def _as_price(value):
    if isinstance(value, bool) or isinstance(value, float):
        raise OrchestratorError('price')
    if isinstance(value, int):
        value = str(value)
    if not isinstance(value, str):
        raise OrchestratorError('price')
    try:
        price = Decimal(value)
    except Exception as exc:
        raise OrchestratorError('price') from exc
    if price < 0 or price > 1:
        raise OrchestratorError('price')
    return price


def _timestamp_fields(row):
    found = []
    for key, value in row.items():
        if not key.endswith('_ts') or value is None:
            continue
        found.append((key, parse_ts(value)))
    return found


def _guard_row(row):
    if not isinstance(row, dict):
        raise OrchestratorError('row')
    if _lee_ready_requested(row):
        raise LeeReadyRefused()
    if row.get('invent_fill') is True or row.get('invent_pnl') is True:
        raise InventedFillRefused()
    for key in INVENT_FILL_KEYS:
        if key in row and row[key] is not None:
            raise InventedFillRefused()
    for key, value in row.items():
        if _mentions_missing_queue(value) or (
            'queue' in key and _mentions_missing_queue(str(value) if value is not None else '')
        ):
            raise QueueBytesNotRecreated()
        if _mentions_capture(value):
            raise Admit1CaptureRefused()
    if row.get('backfill') is True or row.get('source') in ('admit1_backfill', 'backfill'):
        raise Admit1BackfillRefused()
    for _key, ts in _timestamp_fields(row):
        if in_admit1_window(ts):
            raise Admit1WindowRejected()
    for key in LOOKAHEAD_KEYS:
        if key in row and row[key] is not None:
            raise LookaheadRefused()
    ticker = row.get('ticker')
    if isinstance(ticker, str) and (
        ticker.startswith(FORBIDDEN_SERIES + '-') or ticker == FORBIDDEN_SERIES
    ):
        raise RetuneRefused('KXMLBGAME')
    return row


def _null_fill_cells():
    return {
        'contracts': None,
        'price': None,
        'simulated_fill': None,
        'pnl': None,
        'roi': None,
        'results': None,
        'counts_toward_keep': False,
        'formula_id': None,
        'invented': False,
    }


def mechanic_demo_observed(row):
    """Demo mechanic cells stay null. Observations are not invented."""
    _guard_row(row if isinstance(row, dict) else {})
    cells = _null_fill_cells()
    cells.update({
        'fill_model': UNAVAILABLE_MODEL,
        'status': 'UNAVAILABLE',
        'cells': None,
        'through': None,
    })
    return cells


def _through(resting_side, resting_price, trade_price):
    if resting_side == 'bid':
        if trade_price < resting_price:
            return True
        if trade_price == resting_price:
            return False
        return False
    if resting_side == 'ask':
        if trade_price > resting_price:
            return True
        return False
    raise OrchestratorError('resting_side')


def public_trade_through_conservative(row):
    """Classify a public print. A through flag is not a fill and not PnL."""
    row = _guard_row(row)
    base = _null_fill_cells()
    base.update({
        'fill_model': IMPLEMENTED_MODEL,
        'cells': None,
        'through': None,
        'lee_ready': 'REFUSED',
    })
    quote_ts = row.get('quote_ts')
    trade_ts = row.get('trade_ts')
    if quote_ts is not None and trade_ts is not None:
        if parse_ts(trade_ts) <= parse_ts(quote_ts):
            raise LookaheadRefused()
    required = ('quote_ts', 'trade_ts', 'resting_side', 'resting_price', 'trade_yes_price', 'ticker')
    if any(row.get(key) is None for key in required):
        base['status'] = 'INCOMPLETE_NOT_INVENTED'
        return base
    ticker = row['ticker']
    if not isinstance(ticker, str) or not ticker.startswith(SERIES + '-'):
        raise OrchestratorError('series')
    if ticker not in panel_tickers():
        raise InventedMarketRefused()
    side = row['resting_side']
    if side not in ('bid', 'ask'):
        raise OrchestratorError('resting_side')
    resting_price = _as_price(row['resting_price'])
    trade_price = _as_price(row['trade_yes_price'])
    through = _through(side, resting_price, trade_price)
    base['through'] = through
    if resting_price == trade_price:
        base['status'] = 'TOUCH_NOT_THROUGH'
    elif through:
        base['status'] = 'THROUGH_OBSERVED_NO_FILL'
    else:
        base['status'] = 'NOT_THROUGH'
    return base


def classify_fill(row, model=IMPLEMENTED_MODEL):
    """Run the implemented model. mechanic_demo_observed stays unavailable."""
    if model == UNAVAILABLE_MODEL:
        demo = mechanic_demo_observed(row)
        return {
            'knob': KNOB,
            'fill_model': UNAVAILABLE_MODEL,
            'public_trade_through_conservative': None,
            'mechanic_demo_observed': None,
            'mechanic_demo_observed_status': 'UNAVAILABLE',
            'status': demo['status'],
            'through': None,
            'contracts': None,
            'simulated_fill': None,
            'pnl': None,
            'roi': None,
            'results': None,
            'counts_toward_keep': False,
            'formula_id': None,
            'lee_ready': 'REFUSED',
        }
    if model != IMPLEMENTED_MODEL:
        raise UnknownModel()
    observed = public_trade_through_conservative(row)
    return {
        'knob': KNOB,
        'fill_model': IMPLEMENTED_MODEL,
        'public_trade_through_conservative': observed,
        'mechanic_demo_observed': None,
        'mechanic_demo_observed_status': 'UNAVAILABLE',
        'status': observed['status'],
        'through': observed['through'],
        'contracts': None,
        'simulated_fill': None,
        'pnl': None,
        'roi': None,
        'results': None,
        'counts_toward_keep': False,
        'formula_id': None,
        'lee_ready': 'REFUSED',
    }


def public_get(path, transport=None):
    """Stub transport. Order and portfolio routes are refused. live_gets stays 0."""
    if not isinstance(path, str) or not path.startswith('/'):
        raise OrchestratorError('path')
    lowered = path.lower()
    if '/orders' in lowered or '/portfolio' in lowered or 'api_key' in lowered:
        raise LiveOrderRefused()
    if transport is not None:
        raise OrchestratorError('network')
    return {'live_gets': 0, 'body': None, 'network': False, 'path': path}


def load_panel():
    """Hash-check the parent stub. admitted_at stays null. Bytes are not rewritten."""
    if PANEL_ADMITTED.exists():
        raise OrchestratorError('panel_admitted')
    if sha256_file(PANEL_STUB) != PANEL_STUB_SHA256:
        raise OrchestratorError('panel stub')
    payload = json.loads(PANEL_STUB.read_text())
    if payload.get('series_ticker') != SERIES:
        raise OrchestratorError('series')
    if payload.get('panel_version') != PANEL_VERSION:
        raise OrchestratorError('panel_version')
    if payload.get('admitted_at') is not None:
        raise OrchestratorError('admitted_at')
    if len(payload.get('events') or []) != 6 or len(payload.get('markets') or []) != 12:
        raise OrchestratorError('panel size')
    return payload


def panel_tickers():
    payload = load_panel()
    return {market['ticker'] for market in payload['markets']}


def _pin_row(pin):
    path = pin.get('path')
    claimed = pin.get('claimed_sha256')
    if not path:
        return {
            'key': pin['key'],
            'path': path,
            'claimed_sha256': claimed,
            'claimed_sha256_prefix': pin.get('claimed_sha256_prefix'),
            'present': False,
            'match': False,
            'on_disk_sha256': None,
        }
    file_path = PARENT / path
    present = file_path.is_file()
    on_disk = sha256_file(file_path) if present else None
    match = bool(claimed) and present and on_disk == claimed
    return {
        'key': pin['key'],
        'path': path,
        'claimed_sha256': claimed,
        'claimed_sha256_prefix': pin.get('claimed_sha256_prefix'),
        'present': present,
        'match': match,
        'on_disk_sha256': on_disk,
    }


def digest_status(rows=None):
    """Re-hash claimed authority pins. Absent bytes stay absent."""
    if rows is None:
        claimed = json.loads(AUTHORITY.read_text())
        rows = [_pin_row(pin) for pin in claimed['pins'] if pin.get('key') != 'missing_queue_bytes']
    missing = []
    mismatch = []
    for row in rows:
        if row.get('match') is True:
            continue
        if row.get('present') and row.get('claimed_sha256') and row.get('on_disk_sha256') not in (
            None,
            row.get('claimed_sha256'),
        ):
            mismatch.append(row['key'])
        else:
            missing.append(row['key'])
    return {
        'digest_all_match_claimed': not missing and not mismatch,
        'missing': missing,
        'mismatch': mismatch,
        'pins': rows,
        'bytes_recreated': False,
    }


def parent_freeze_intact():
    return PARENT_FREEZE.is_file() and sha256_file(PARENT_FREEZE) == PARENT_FREEZE_SHA256


def assert_null_scorecard(payload):
    if not isinstance(payload, dict):
        raise ScorecardPromotionRefused()
    for key in OUTPUT_KEYS:
        if key not in payload or payload[key] is not None:
            raise ScorecardPromotionRefused()
    return payload


def assert_v12_null(block):
    if not isinstance(block, dict):
        raise ScorecardPromotionRefused()
    card = block.get('scorecard') or {}
    if card.get('status') != 'HOLD_PRE_PR' or card.get('verdict') is not None:
        raise ScorecardPromotionRefused()
    if card.get('stub_ready') is not False or card.get('scored') is not False:
        raise ScorecardPromotionRefused()
    metrics = card.get('metrics') or {}
    for key in ('results', 'pnl', 'Q6S5A0_roi', 'Q6S5A1_roi'):
        if metrics.get(key) is not None:
            raise ScorecardPromotionRefused()
    common = block.get('common_scorecard') or {}
    if tuple(common.keys()) != COMMON_SCORECARD_KEYS:
        raise ScorecardPromotionRefused()
    for name, metric in common.items():
        if metric.get('value') is not None or metric.get('measured') is not False:
            raise ScorecardPromotionRefused()
        if name == 'calibration' and metric.get('emits_probabilities') is not False:
            raise ScorecardPromotionRefused()
    if (block.get('study_label') or {}).get('value') is not None:
        raise ScorecardPromotionRefused()
    checklist = block.get('preregistration_checklist') or {}
    if checklist.get('gate_status') is not None:
        raise ScorecardPromotionRefused()
    counts = checklist.get('variants_declared_counts') or {}
    if counts.get('satisfied') != 9 or counts.get('n/a') != 3 or counts.get('missing') != 0:
        raise OrchestratorError('p16')
    fills = block.get('simulated_fills') or {}
    if fills.get('counts_toward_keep') is not False:
        raise ScorecardPromotionRefused()
    if (fills.get('fill_rate_simulated') or {}).get('value') is not None:
        raise ScorecardPromotionRefused()
    if fills.get('fill_model_ref') is not None:
        raise ScorecardPromotionRefused()
    fee = block.get('fee_regime') or {}
    if fee.get('formula_id') is not None:
        raise CacheNotLiveR1P1()
    if fee.get('label') != FEE_LABEL:
        raise CacheNotLiveR1P1()
    if block.get('all_score_values_null') is not True:
        raise ScorecardPromotionRefused()
    return block


def instrument_binding():
    panel = load_panel()
    pins = digest_status()
    label = fee_output()
    arms = parent_arms()
    return {
        'experiment_id': EXPERIMENT_ID,
        'feature_family': FEATURE_FAMILY,
        'lab_directory': LAB_DIRECTORY,
        'knob': KNOB,
        'fill_model': IMPLEMENTED_MODEL,
        'mechanic_demo_observed': 'UNAVAILABLE',
        'arms': [{'id': arm, 'analysis_slice': arms[arm]} for arm in (Q6S5A0, Q6S5A1)],
        'series_ticker': SERIES,
        'panel_version': panel['panel_version'],
        'admitted_at': None,
        'events_n': 6,
        'markets_n': 12,
        'fee_cache': label,
        'formula_id': None,
        'cache_labeled': True,
        'live_r1p1': False,
        'counts_toward_keep': False,
        'lee_ready': 'REFUSED',
        'live_gets': 0,
        'live_orders': False,
        'dual_cloud': False,
        'admit_py_run': False,
        'examiner_status': 'HOLD_PRE_PR',
        'stub_ready': False,
        'digest_all_match_claimed': pins['digest_all_match_claimed'],
        'digest_missing': pins['missing'],
        'conductor_accept_sha256': ACCEPT_SHA256,
        'freeze_sha256': FREEZE_SHA256,
        'kick_sha256_prefix': KICK_SHA256_PREFIX,
        'admit1_ruling_prefix': ADMIT1_RULING_PREFIX,
        'parent_freeze_intact': parent_freeze_intact(),
        'panel_stub_sha256': PANEL_STUB_SHA256,
        'feebook_commit': FEEBOOK_COMMIT,
        'rails_commit': RAILS_COMMIT,
        'results': None,
        'pnl': None,
        'roi': None,
    }


def conduct(arm):
    """Arm schema on the pinned panel. ROI stays null."""
    arms = parent_arms()
    if arm not in arms:
        raise UnknownArm()
    panel = load_panel()
    report = {
        'experiment_id': EXPERIMENT_ID,
        'arm': arm,
        'analysis_slice': arms[arm],
        'knob': KNOB,
        'fill_model': IMPLEMENTED_MODEL,
        'mechanic_demo_observed': 'UNAVAILABLE',
        'series_ticker': panel['series_ticker'],
        'results': None,
        'pnl': None,
        'roi': None,
        'counts_toward_keep': False,
        'formula_id': None,
        'lee_ready': 'REFUSED',
        'live_gets': 0,
        'live_orders': False,
        'examiner_status': 'HOLD_PRE_PR',
        'stub_ready': False,
        'fee_cache': fee_output(),
    }
    assert_null_scorecard(report)
    return report


def published_scorecard():
    payload = json.loads(EMPTY_RESULTS.read_text())
    assert_null_scorecard(payload)
    assert_v12_null(payload['examiner_scorecard_v1_2'])
    return payload


def write_scorecard(payload):
    assert_null_scorecard(payload)
    raise ScorecardPromotionRefused()
