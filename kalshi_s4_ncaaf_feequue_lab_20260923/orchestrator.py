"""S4 KXNCAAFGAME fee and queue honesty harness.

Measurement only. Imports the R1-P1 feebook, the R1-P5 rails, and the R2-P1
hygiene helpers those joins already call. This module does not edit those
labs, does not place orders, does not read Logan keys, and does not write
scorecard metrics.

The conductor-box freeze bytes were not in this checkout. Copy hashes are
the recreation hashes. Conductor claims stay recorded and are not relabeled
as the recreation hashes.
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

LAB_DIRECTORY = 'kalshi_s4_ncaaf_feequue_lab_20260923'
EXPERIMENT_ID = 'S4-KXNCAAFGAME-FEEQUEUE-HARNESS'
PANEL_PACKET_ID = 'S4-KXNCAAFGAME-MEAS'
SERIES = 'KXNCAAFGAME'
PANEL_VERSION = '2026-09-22.s4-kxncaafgame-v0'
KNOB = 'honesty_partition'
S4A0 = 'S4A0'
S4A1 = 'S4A1'
ARMS = (S4A0, S4A1)
PARTITIONS = {
    S4A0: 'maker_vs_taker_native',
    S4A1: 'content_fresh_vs_stale_bin',
}
FEEBOOK_COMMIT = '22371178cb2663250b4762f328069571c48cb551'
RAILS_COMMIT = '6a28e0d6254327ea4e6451c781bec56215ac6cac'
BASE_COMMIT = '6626c6892298b015cf63688081545e27363226bc'
PACKET_SHA256 = '00117c348573076bc35af422e6618d750c1e6b89c3387f2b7c0b0f259d3fe2a2'
KERNEL_SHA256 = 'f0e502264ce79d8e958c54cace387aa0521f616dd59290356aaafc33e9096847'
PANEL_STUB_SHA256 = 'eb0a9ea7e4cf24d6f805f63688dbb48c71dc91a81bcea4afb2c88f73588b8112'
CONDUCTOR_PACKET_SHA256 = '3318204bf6e962f4f3372dad8c0f302e62d85c26b855de7369718654d0114728'
CONDUCTOR_KERNEL_SHA256 = '9e6556c150c726b679ac8393f1f5338cf983489259b0f34cdedf221c030be795'
CONDUCTOR_PANEL_STUB_SHA256 = '38167d11da5842bc4d39e6e7dcaab20a67294c735ba14d8bbeafde3154c6342a'
CONDUCTOR_EVENTS_N_CLAIM = 113
PUBLIC_HOST = 'https://api.elections.kalshi.com/trade-api/v2'
OUT_OF_SCOPE_ROUTE = 'POST /portfolio/orders'
SCORECARD_FIELDS = (
    'maker_vs_taker_roi_delta',
    'fresh_vs_stale_gap',
    'settled_join_n',
)
OUTPUT_KEYS = SCORECARD_FIELDS + ('results', 'pnl')
PUBLIC_TAKER_FIELDS = ('taker_outcome_side', 'taker_book_side', 'taker_side')
BOOK_TO_OUTCOME = {'bid': 'yes', 'ask': 'no'}
ADVERSARY_LABELS = {
    'lee_ready': 'Lee-Ready is refused on every input',
    'live_orders': 'live orders are refused',
    'logan_keys': 'Logan keys are refused',
    'invented_pnl': 'invented pnl is refused',
    'invented_fills': 'invented fills are refused',
    'q6_retune': 'Q6-000 retune is refused',
    'qf_reopen': 'queue-fragility reopen is refused',
    'cap_sr_reopen': 'Cap-SR reopen is refused',
    'admit_py': 'admit.py is refused',
    'r1_p2_challenger': 'R1-P2 challenger bakeoff is refused',
    'q7_arm_b': 'Q7 Arm B stays killed',
}
DOES_NOT_MODIFY = (
    'kalshi_feebook_lab_20260922',
    'kalshi_rails_lab_20260922',
    'kalshi_queue_fragility_000_lab_20260922',
    'kalshi_soft_blended_reserves_000_lab_20260923',
    'kalshi_cap_sr_effects_000_lab_20260923',
    'kalshi_c3_kxhighny_bordering_lab_20260923',
    'kalshi_c5_kxbtc15m_honesty_lab_20260923',
    'kalshi_r3p3_fl_maker_taker_lab_20260923',
    'kalshi_s5_mve_filllegs_lab_20260923',
    'nfl_factorial_lab_20260921',
    'nfl_paircheck_lab_20260922',
)
PACKET_NAME = 'S4_KXNCAAFGAME_FEEQUEUE_HARNESS_FREEZE_2026-09-23.md'
KERNEL_NAME = 'S4_KXNCAAFGAME_MEASUREMENT_FREEZE_KERNEL_2026-09-22.md'
PACKET = ROOT / PACKET_NAME
KERNEL = ROOT / KERNEL_NAME
LAB_BUNDLE = ROOT / 'S4_KXNCAAFGAME_FEEQUEUE_HARNESS'
GOVERNANCE_BUNDLE = PARENT / 'packets' / 'S4_KXNCAAFGAME_FEEQUEUE_HARNESS'
GOVERNANCE_TREE = PARENT / 'lab' / 'governance' / 'astra' / 'packets'
FROZEN_EXPERIMENT = ROOT / 'FROZEN_EXPERIMENT.json'
EMPTY_RESULTS = ROOT / 'results' / 'EMPTY_RESULTS.json'
PANEL_STUB = PARENT / 'lab' / 'astra-capture' / 's4-kxncaafgame' / 'panel_stub.json'
PANEL_ADMITTED = PARENT / 'lab' / 'astra-capture' / 's4-kxncaafgame' / 'panel_admitted.json'
SYNTHETIC_TRADES = ROOT / 'fixtures' / 'synthetic_native_trades.json'
SYNTHETIC_FRESH = ROOT / 'fixtures' / 'synthetic_fresh_queue.json'


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
    """Lee-Ready is refused on every input."""

    def __init__(self):
        super().__init__('Lee-Ready refused')


class TakerFieldRefused(OrchestratorError):
    """Native taker fields are missing or disagree."""

    def __init__(self, reason):
        super().__init__(reason)


class PanelVersionRefused(OrchestratorError):
    """The panel file is not the pinned S4 seed."""

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


class UnknownPartition(OrchestratorError):
    """The only knob is the two named partitions."""

    def __init__(self):
        super().__init__('honesty_partition')


def _load_hygiene():
    spec = importlib.util.spec_from_file_location('s4_hygiene', HYGIENE_PATH)
    if spec is None or spec.loader is None:
        raise OrchestratorError('hygiene import')
    module = importlib.util.module_from_spec(spec)
    sys.modules['s4_hygiene'] = module
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


def refuse_adversary(label):
    """Named refuse labels. Nothing is traded."""
    if label not in ADVERSARY_LABELS:
        raise OrchestratorError('adversary label')
    if label == 'lee_ready':
        raise LeeReadyRefused()
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


def classify_native_taker(row):
    """Partition from native taker_* fields. Lee-Ready does not vote."""
    if not isinstance(row, dict):
        raise OrchestratorError('row')
    if _lee_ready_requested(row):
        raise LeeReadyRefused()
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
    if row.get('result') is not None or row.get('settlement_ts') is not None:
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
    """Bin on rails content-fresh and queue attribution. Taker fields do not vote."""
    if not isinstance(row, dict):
        raise OrchestratorError('row')
    if _lee_ready_requested(row):
        raise LeeReadyRefused()
    if row.get('result') is not None:
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
    """Accept only the R1-P1 examiner formula."""
    if not isinstance(quote, dict):
        raise ShadowFeeLiteralRefused()
    formula = quote.get('formula_id')
    if formula != feebook.EXAMINER_FORMULA_ID:
        raise ShadowFeeLiteralRefused()
    if formula in (feebook.GROK_COMPARATOR_FORMULA_ID, hygiene.INHERITED_MODEL_ID):
        raise ShadowFeeLiteralRefused()
    return quote


def _require_null(payload, key):
    if key not in payload or payload[key] is not None:
        raise InventedFillRefused()


def conductor_pin_status():
    """Compare checkout bytes with the conductor claims. Do not relabel a miss."""
    packet_match = sha256_file(PACKET) == CONDUCTOR_PACKET_SHA256
    kernel_match = sha256_file(KERNEL) == CONDUCTOR_KERNEL_SHA256
    stub_match = sha256_file(PANEL_STUB) == CONDUCTOR_PANEL_STUB_SHA256
    return {
        'packet_matches_conductor_claim': packet_match,
        'kernel_matches_conductor_claim': kernel_match,
        'panel_stub_matches_conductor_claim': stub_match,
        'conductor_bytes_in_checkout': packet_match and kernel_match and stub_match,
    }


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
    if sha256_file(PANEL_STUB) != PANEL_STUB_SHA256:
        raise OrchestratorError('stub sha256')


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
    if payload.get('packet_id') != PANEL_PACKET_ID:
        raise OrchestratorError('packet')
    if payload.get('series_ticker') != SERIES:
        raise OrchestratorError('series')
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
    if binds.get('no_live_orders') is not True:
        raise LiveOrdersForbidden()
    if binds.get('no_logan_keys') is not True:
        raise AdversaryRefused(ADVERSARY_LABELS['logan_keys'])
    if binds.get('no_000_retune') is not True:
        raise AdversaryRefused(ADVERSARY_LABELS['q6_retune'])
    if binds.get('no_qf_reopen') is not True:
        raise AdversaryRefused(ADVERSARY_LABELS['qf_reopen'])
    if binds.get('no_cap_sr_reopen') is not True:
        raise AdversaryRefused(ADVERSARY_LABELS['cap_sr_reopen'])
    if binds.get('no_admit_py') is not True:
        raise AdversaryRefused(ADVERSARY_LABELS['admit_py'])
    if binds.get('no_r1p2_challenger_bakeoff') is not True:
        raise AdversaryRefused(ADVERSARY_LABELS['r1_p2_challenger'])
    if binds.get('lee_ready') != 'REFUSED':
        raise LeeReadyRefused()
    if binds.get('forbid_inherited_q7_fee_literals') is not True:
        raise ShadowFeeLiteralRefused()
    capture = payload.get('capture') or {}
    if capture.get('mode') != 'GET_only_public':
        raise LiveOrdersForbidden()
    if capture.get('host_allowlist') != [PUBLIC_HOST]:
        raise LiveOrdersForbidden()
    if OUT_OF_SCOPE_ROUTE not in (capture.get('out_of_scope_routes') or []):
        raise LiveOrdersForbidden()
    schedule = capture.get('schedule') or {}
    if schedule.get('recorder_started') is True or schedule.get('admit_py_run') is True:
        raise OrchestratorError('recorder')
    events = payload.get('events') or []
    markets = payload.get('markets') or []
    counts = payload.get('cohort_counts') or {}
    if not admitted:
        if payload.get('conductor_panel_stub_sha256_claim') != CONDUCTOR_PANEL_STUB_SHA256:
            raise OrchestratorError('conductor stub claim')
        if payload.get('conductor_events_n_claim') != CONDUCTOR_EVENTS_N_CLAIM:
            raise OrchestratorError('conductor events claim')
        if counts.get('events_n') != len(events) or counts.get('markets_n') != len(markets):
            raise OrchestratorError('cohort')
    for event in events:
        if event.get('series_ticker') != SERIES:
            raise OrchestratorError('series')
        if event.get('admitted_at') not in (None, stamp):
            raise OrchestratorError('admitted_at')
        for key in ('volume_fp', 'open_interest_fp', 'results', 'pnl'):
            if key in event and event[key] is not None:
                raise InventedFillRefused()
    for market in markets:
        if market.get('series_ticker') != SERIES:
            raise OrchestratorError('series')
        if market.get('result') is not None:
            raise InventedFillRefused()
    objects = payload.get('measurement_objects') or {}
    native = objects.get('native_taker_partition') or {}
    fresh = objects.get('rails_freshness_bin') or {}
    if native.get('status') is not None or fresh.get('status') is not None:
        raise ScorecardPromotionRefused()
    if fresh.get('content_fresh_flag') is not None or fresh.get('queue_attribution_bin') is not None:
        raise ScorecardPromotionRefused()
    return payload


def load_panel(stub_path=None, admitted_path=None):
    """Stub by default. panel_admitted.json wins when it is on disk."""
    path = select_panel_path(stub_path, admitted_path)
    if path.resolve() == PANEL_STUB.resolve():
        _assert_freeze_bytes()
    payload = json.loads(path.read_text())
    return _validate_panel(payload, admitted=path.name == 'panel_admitted.json')


def arm_table():
    return tuple({'id': arm, 'partition': PARTITIONS[arm]} for arm in ARMS)


def instrument_binding(panel=None):
    """One partition knob. Fee and rails commits stay fixed. No scorecard fill."""
    if panel is None:
        panel = load_panel()
    quote = feebook.order_fee('taker', '1', '0.50', round_up=True, series=SERIES)
    assert_examiner_quote(quote)
    if quote['series_resolution'] != 'default_unknown_series':
        raise OrchestratorError('series resolution')
    if hygiene.FEEBOOK_COMMIT != FEEBOOK_COMMIT or hygiene.RAILS_COMMIT != RAILS_COMMIT:
        raise OrchestratorError('pin')
    ahead_bin = hygiene.queue_attribution_bin(rails.QUEUE_AHEAD_DEFAULT)
    if ahead_bin != 'q3300':
        raise OrchestratorError('queue bin')
    pins = conductor_pin_status()
    return {
        'experiment_id': EXPERIMENT_ID,
        'lab_directory': LAB_DIRECTORY,
        'feature_family': 'NCAAF-FQ',
        'knob': KNOB,
        'arms': arm_table(),
        'panel_version': panel['panel_version'],
        'admitted_at': panel.get('admitted_at'),
        'series_ticker': SERIES,
        'events_n': len(panel.get('events') or []),
        'conductor_events_n_claim': CONDUCTOR_EVENTS_N_CLAIM,
        'strategy_pointer': None,
        'feebook_commit': FEEBOOK_COMMIT,
        'rails_commit': RAILS_COMMIT,
        'examiner_formula_id': feebook.EXAMINER_FORMULA_ID,
        'fee_credit_rule_id': rails.FEE_CREDIT_RULE_ID,
        'fee_source': 'feebook',
        'queue_source': 'rails',
        'honesty_helpers': 'hygiene',
        'probe_formula_id': quote['formula_id'],
        'probe_scorecard_write': False,
        'lee_ready': 'REFUSED',
        'logan_keys_required': False,
        'live_orders': False,
        'signal_retune_000': False,
        'queue_fragility_reopen': False,
        'cap_sr_reopen': False,
        'admit_py_run': False,
        'r1_p2_challenger_bakeoff': False,
        'fee_is_knob': False,
        'scorecard_fields': SCORECARD_FIELDS,
        'kernel_sha256': KERNEL_SHA256,
        'packet_sha256': PACKET_SHA256,
        'panel_stub_sha256': PANEL_STUB_SHA256,
        'conductor_packet_sha256_claim': CONDUCTOR_PACKET_SHA256,
        'conductor_parent_freeze_sha256_claim': CONDUCTOR_KERNEL_SHA256,
        'conductor_panel_stub_sha256_claim': CONDUCTOR_PANEL_STUB_SHA256,
        'conductor_bytes_in_checkout': pins['conductor_bytes_in_checkout'],
        'packet_matches_conductor_claim': pins['packet_matches_conductor_claim'],
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


def _report(arm, source, extra):
    if arm not in PARTITIONS:
        raise UnknownPartition()
    published = published_scorecard()
    report = {
        'experiment_id': EXPERIMENT_ID,
        'arm': arm,
        'partition': PARTITIONS[arm],
        'source': source,
        'published': published,
        'promoted': False,
        'strategy_pointer': None,
        'live_orders': False,
        'lee_ready': 'REFUSED',
        'fee_pin': FEEBOOK_COMMIT,
        'rails_pin': RAILS_COMMIT,
    }
    report.update(extra)
    for key in OUTPUT_KEYS:
        report[key] = None
    assert_null_scorecard(report)
    assert_null_scorecard(published)
    return report


def conduct(arm, panel=None):
    """Schema for one partition on the loaded panel. Scorecard fields stay null."""
    if arm not in PARTITIONS:
        raise UnknownPartition()
    if panel is None:
        panel = load_panel()
    events = panel.get('events') or []
    extra = {
        'event_count': len(events),
        'market_count': len(panel.get('markets') or []),
    }
    if not events:
        extra['cohort_note'] = 'conductor_stub_absent_seed_not_invented'
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
    """S4A0 schema on synthetic native rows. Does not write the freeze scorecard."""
    rows = partition_native(load_synthetic_trades(path))
    return _report(S4A0, 'synthetic_schema_standin', {
        'partitions': rows,
        'partition_count': len(rows),
    })


def conduct_fresh(path=None):
    """S4A1 schema on synthetic book rows. The gap stays null."""
    rows = partition_fresh(load_synthetic_fresh(path))
    return _report(S4A1, 'synthetic_schema_standin', {
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
        if name != 'frozen' and name != 'bundle_frozen' and name != 'governance_frozen':
            for key in SCORECARD_FIELDS:
                if key not in payload or payload[key] is not None:
                    raise ScorecardPromotionRefused()
                snapshot['%s.%s' % (name, key)] = None
    return snapshot
