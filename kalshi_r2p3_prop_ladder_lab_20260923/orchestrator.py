"""R2-P3 KXNFLPASSYDS prop-ladder fee and queue honesty harness.

Measurement only. Imports the R1-P1 feebook, the R1-P5 rails, and the R2-P1
hygiene helpers those joins already call. This module does not edit those
labs, does not place orders, does not read Logan keys, does not run admit.py,
and does not write scorecard metrics.

The checkout harness freeze, parent kernel, and panel stub match the
conductor sha256 values. Event count on the stub is 6. Lee-Ready is refused.
ATL@GB is refused. Fee amounts come from the feebook import only.
"""
import hashlib
import importlib.util
import json
import sys
from decimal import Decimal
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

LAB_DIRECTORY = 'kalshi_r2p3_prop_ladder_lab_20260923'
EXPERIMENT_ID = 'R2-P3-KXNFLPASSYDS-PROP-LADDER-HARNESS'
PANEL_PACKET_ID = 'R2-P3-KXNFLPASSYDS-MEAS'
FEATURE_FAMILY = 'PROP-LQ'
SCHEMA_ID = 'astra.registry.r2_p3_prop_slate_panel.v0'
PANEL_VERSION = '2026-09-22.r2-p3-prop-slate-v0'
KERNEL_SERIES = 'KXNFLPASSYDS'
SIBLING_SERIES = ('KXNFLRECYDS', 'KXNFLRSHYDS')
SERIES_TICKERS = (KERNEL_SERIES,) + SIBLING_SERIES
SLATE_GAMES = ('LACBUF', 'BALDAL')
SLATE_EVENTS = (
    'KXNFLPASSYDS-26SEP27LACBUF',
    'KXNFLRECYDS-26SEP27LACBUF',
    'KXNFLRSHYDS-26SEP27LACBUF',
    'KXNFLPASSYDS-26SEP27BALDAL',
    'KXNFLRECYDS-26SEP27BALDAL',
    'KXNFLRSHYDS-26SEP27BALDAL',
)
EXCLUDED_EVENTS = (
    'KXNFLPASSYDS-26SEP24ATLGB',
    'KXNFLRECYDS-26SEP24ATLGB',
    'KXNFLRSHYDS-26SEP24ATLGB',
)
OCCURRENCE_BY_GAME = {
    'LACBUF': '2026-09-27T20:00:00Z',
    'BALDAL': '2026-09-27T23:25:00Z',
}
KNOB = 'residual_monotone_family'
R2P3A0 = 'R2P3A0'
R2P3A1 = 'R2P3A1'
ARMS = (R2P3A0, R2P3A1)
FAMILIES = {
    R2P3A0: 'isotonic',
    R2P3A1: 'logit_monotone',
}
FEEBOOK_COMMIT = '22371178cb2663250b4762f328069571c48cb551'
RAILS_COMMIT = '6a28e0d6254327ea4e6451c781bec56215ac6cac'
BASE_COMMIT = 'd7584dd48a67d38d81f5141654b6f498915a70a5'
CONDUCTOR_PACKET_SHA256 = 'f8335eb0080cb1f82b1fad512509749134dd0e6e41ed85795347c3476796e87a'
CONDUCTOR_KERNEL_SHA256 = 'a30108f658359590e170c73ea00d1a1f0852d5751cb15c9f2a9c6389f4dd3eaa'
CONDUCTOR_PANEL_STUB_SHA256 = '70e879e8738d033f392d821849dee3537af3e7b8a916670779d238f78ce098be'
CONDUCTOR_STAMP_SHA256 = '9c4919c968a2cb1e9c70995ebc454da709109e2866ffb02668c9e803570f31bc'
ADVERSARY_SHA256 = '2c56d92d1b18544c640eedd7e76ae5978d3c7108a8c99faeb2a21364a92d6fad'
PACKET_SHA256 = CONDUCTOR_PACKET_SHA256
KERNEL_SHA256 = CONDUCTOR_KERNEL_SHA256
PANEL_STUB_SHA256 = CONDUCTOR_PANEL_STUB_SHA256
CONDUCTOR_EVENTS_N_CLAIM = 6
PUBLIC_HOST = 'api.elections.kalshi.com'
OUT_OF_SCOPE_ROUTE = 'POST /portfolio/orders'
ONE = Decimal('1')
SCORECARD_FIELDS = (
    'cross_strike_residual_rms',
    'latent_fit_fragmentation',
    'maker_credit_floor_zero_n',
    'fresh_strike_n',
    'settled_join_n',
)
OUTPUT_KEYS = SCORECARD_FIELDS + ('results', 'pnl')
INVENTORY_KEYS = ('volume_fp', 'volume_24h_fp', 'open_interest_fp')
FEE_INPUT_KEYS = ('fee', 'order_fee', 'fee_literal', 'inherited_fee', 'coefficient')
ADVERSARY_LABELS = {
    'lee_ready': 'Lee-Ready is refused on every input',
    'live_orders': 'live orders are refused',
    'logan_keys': 'Logan keys are refused',
    'invented_pnl': 'invented pnl is refused',
    'invented_fills': 'invented fills are refused',
    'invented_cohort': 'invented cohort is refused',
    'invented_volume': 'invented volume is refused',
    'q6_retune': 'Q6-000 retune is refused',
    'qf_reopen': 'queue-fragility reopen is refused',
    'cap_sr_reopen': 'Cap-SR reopen is refused',
    'cap_sr_fx_reopen': 'Cap-SR-FX reopen is refused',
    'atl_gb': 'ATL@GB enrichment is refused',
    'admit_py': 'admit.py is refused',
    'ws_ping': 'freshness from WS ping is refused',
    'q7_arm_b': 'Q7 Arm B stays killed',
    'markout_knob': 'markout horizon is not the knob',
    'completed_profit': 'completed profit without the feebook channel is refused',
}
DEAD_CARDS = (
    'QF_reopen_DENIED',
    'Cap-SR_reopen_DENIED',
    'Cap-SR-FX_closed',
    '000_retune_REFUSED',
    'ATL@GB_REFUSED',
    'Q7_Arm_B_KILL',
)
DOES_NOT_MODIFY = (
    'kalshi_feebook_lab_20260922',
    'kalshi_rails_lab_20260922',
    'kalshi_queue_fragility_000_lab_20260922',
    'kalshi_soft_blended_reserves_000_lab_20260923',
    'kalshi_cap_sr_effects_000_lab_20260923',
    'kalshi_c3_kxhighny_bordering_lab_20260923',
    'kalshi_c5_kxbtc15m_honesty_lab_20260923',
    'kalshi_r3p3_fl_maker_taker_lab_20260923',
    'kalshi_s4_ncaaf_feequue_lab_20260923',
    'kalshi_s5_mve_filllegs_lab_20260923',
    'nfl_factorial_lab_20260921',
    'nfl_paircheck_lab_20260922',
)
PACKET_NAME = 'R2_P3_KXNFLPASSYDS_PROP_LADDER_HARNESS_FREEZE_2026-09-23.md'
KERNEL_NAME = 'R2-P3_KXNFLPASSYDS_MEASUREMENT_FREEZE_KERNEL_2026-09-22.md'
ADVERSARY_NAME = 'R2-P3_ADVERSARY_REFUSE_BIND_2026-09-22.md'
STAMP_NAME = 'CONDUCTOR_FROZEN_EXPERIMENT.json'
PACKET = ROOT / PACKET_NAME
KERNEL = ROOT / KERNEL_NAME
ADVERSARY_BIND = ROOT / ADVERSARY_NAME
CONDUCTOR_STAMP = ROOT / STAMP_NAME
LAB_BUNDLE = ROOT / 'R2_P3_PROP_LADDER_HARNESS'
GOVERNANCE_BUNDLE = PARENT / 'packets' / 'R2_P3_PROP_LADDER_HARNESS'
GOVERNANCE_TREE = PARENT / 'lab' / 'governance' / 'astra' / 'packets'
FROZEN_EXPERIMENT = ROOT / 'FROZEN_EXPERIMENT.json'
EMPTY_RESULTS = ROOT / 'results' / 'EMPTY_RESULTS.json'
PANEL_STUB = PARENT / 'lab' / 'astra-capture' / 'r2-p3-prop-slate' / 'panel_stub.json'
PANEL_ADMITTED = PARENT / 'lab' / 'astra-capture' / 'r2-p3-prop-slate' / 'panel_admitted.json'
SYNTHETIC_LADDER = ROOT / 'fixtures' / 'synthetic_mid_ladder.json'


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


class SlateRefused(OrchestratorError):
    """The slate is LAC@BUF and BAL@DAL. ATL@GB is excluded."""

    def __init__(self):
        super().__init__(ADVERSARY_LABELS['atl_gb'])


class PanelVersionRefused(OrchestratorError):
    """The panel file is not the pinned R2-P3 seed."""

    def __init__(self):
        super().__init__('panel_version')


class ShadowFeeLiteralRefused(OrchestratorError):
    """A fee quote bypassed the examiner feebook formula."""

    def __init__(self):
        super().__init__('shadow fee literal')


class InventedFillRefused(OrchestratorError):
    """A fill, settlement, volume, or cohort was invented."""

    def __init__(self):
        super().__init__('invented fill')


class UnknownFamily(OrchestratorError):
    """The only knob is isotonic or logit_monotone."""

    def __init__(self):
        super().__init__('residual_monotone_family')


def _load_hygiene():
    spec = importlib.util.spec_from_file_location('r2p3_hygiene', HYGIENE_PATH)
    if spec is None or spec.loader is None:
        raise OrchestratorError('hygiene import')
    module = importlib.util.module_from_spec(spec)
    sys.modules['r2p3_hygiene'] = module
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
    if label == 'atl_gb':
        raise SlateRefused()
    if label == 'live_orders':
        raise LiveOrdersForbidden()
    raise AdversaryRefused(ADVERSARY_LABELS[label])


def infer_lee_ready(row):
    """Lee-Ready has no success path. Every input is refused."""
    if row is None or isinstance(row, (dict, str, int, float, list, tuple)):
        raise LeeReadyRefused()
    raise LeeReadyRefused()


def select_markout(horizon):
    """Markout horizon is not this packet's knob."""
    if horizon is None or isinstance(horizon, str):
        raise AdversaryRefused(ADVERSARY_LABELS['markout_knob'])
    raise AdversaryRefused(ADVERSARY_LABELS['markout_knob'])


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


def _slate_banned(value):
    if not isinstance(value, str):
        return False
    token = value.upper().replace(' ', '')
    return 'ATLGB' in token or 'ATL@GB' in value.upper()


def _require_null(payload, key):
    if key not in payload or payload[key] is not None:
        raise InventedFillRefused()


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


def _logit(probability):
    if probability <= 0 or probability >= 1:
        raise OrchestratorError('logit domain')
    return (probability / (ONE - probability)).ln()


def _expit(value):
    return ONE / (ONE + (-value).exp())


def _pav_nonincreasing(values):
    """Pool-adjacent-violators. Fitted values are non-increasing in strike order."""
    if not values:
        raise OrchestratorError('ladder')
    blocks = [[value, ONE] for value in values]
    index = 0
    while index < len(blocks) - 1:
        left = blocks[index][0] / blocks[index][1]
        right = blocks[index + 1][0] / blocks[index + 1][1]
        if left < right:
            blocks[index][0] += blocks[index + 1][0]
            blocks[index][1] += blocks[index + 1][1]
            del blocks[index + 1]
            if index > 0:
                index -= 1
        else:
            index += 1
    fitted = []
    for total, weight in blocks:
        mean = total / weight
        count = int(weight)
        if Decimal(count) != weight:
            raise OrchestratorError('pav weight')
        fitted.extend([mean] * count)
    if len(fitted) != len(values):
        raise OrchestratorError('pav length')
    for earlier, later in zip(fitted, fitted[1:]):
        if earlier < later:
            raise OrchestratorError('monotone')
    return fitted


def _family_name(arm):
    if arm not in FAMILIES:
        raise UnknownFamily()
    return FAMILIES[arm]


def _fit_values(mids, family):
    if family == 'isotonic':
        return _pav_nonincreasing(mids)
    if family == 'logit_monotone':
        fitted_logits = _pav_nonincreasing([_logit(mid) for mid in mids])
        return [_expit(value) for value in fitted_logits]
    raise UnknownFamily()


def _observation(payload, transaction_time):
    if payload is None:
        return None
    if not isinstance(payload, dict):
        raise OrchestratorError('book')
    return rails.BookObservation(
        content=rails.canonical_book_content(payload),
        transaction_time=transaction_time,
    )


def _scorecard_row(row):
    for key in OUTPUT_KEYS:
        row[key] = None
    return row


def annotate_strike(row):
    """TOB mid, feebook touch, and rails labels for one synthetic strike.

    The returned row is an in-memory code path. Scorecard aggregates stay null.
    """
    if not isinstance(row, dict):
        raise OrchestratorError('row')
    if _lee_ready_requested(row):
        raise LeeReadyRefused()
    if row.get('freshness_source') == 'ws_ping' or row.get('keepalive_as_fresh') is True:
        raise AdversaryRefused(ADVERSARY_LABELS['ws_ping'])
    for key in ('event_ticker', 'game_id', 'series_ticker', 'strike_id', 'player_id'):
        if _slate_banned(row.get(key)):
            raise SlateRefused()
    for key in FEE_INPUT_KEYS:
        if key in row and row[key] is not None:
            raise ShadowFeeLiteralRefused()
    if row.get('result') is not None or row.get('settlement_ts') is not None:
        raise InventedFillRefused()
    for key in INVENTORY_KEYS:
        if key in row and row[key] is not None:
            raise InventedFillRefused()
    for key in OUTPUT_KEYS:
        if key in row and row[key] is not None:
            raise ScorecardPromotionRefused()
    if row.get('markout_horizon') is not None:
        raise AdversaryRefused(ADVERSARY_LABELS['markout_knob'])
    event = row.get('event_ticker')
    if event not in SLATE_EVENTS:
        raise SlateRefused()
    series = row.get('series_ticker')
    if series not in SERIES_TICKERS:
        raise OrchestratorError('series')
    game = row.get('game_id')
    if game not in SLATE_GAMES or game not in event:
        raise SlateRefused()
    player = row.get('player_id')
    if not isinstance(player, str) or not player.startswith('SYNTHETIC_'):
        raise InventedFillRefused()
    orderbook = row.get('orderbook_fp')
    if not isinstance(orderbook, dict):
        raise OrchestratorError('orderbook')
    book = feebook.reciprocal_book({'orderbook_fp': orderbook})
    bid = book['bid_yes']
    ask = book['ask_yes']
    if bid is None or ask is None:
        raise OrchestratorError('touch')
    if ask < bid:
        raise OrchestratorError('crossed book')
    mid = (bid + ask) / 2
    contracts = row.get('contracts', '1')
    taker = feebook.order_fee('taker', contracts, ask, round_up=True, series=series)
    maker = feebook.order_fee('maker', contracts, bid, round_up=True, series=series)
    assert_examiner_quote(taker)
    assert_examiner_quote(maker)
    if taker['series_resolution'] != 'default_unknown_series':
        raise OrchestratorError('series resolution')
    if maker['series_resolution'] != 'default_unknown_series':
        raise OrchestratorError('series resolution')
    credit = hygiene.maker_credit_floor_zero_refuse(bid, contracts, series=series)
    if credit['formula_id'] != feebook.EXAMINER_FORMULA_ID:
        raise ShadowFeeLiteralRefused()
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
    packed = {
        'strike_id': row.get('strike_id'),
        'player_id': player,
        'event_ticker': event,
        'game_id': game,
        'series_ticker': series,
        'strike': feebook.as_decimal(row.get('strike'), 'strike'),
        'mid': mid,
        'bid_yes': bid,
        'ask_yes': ask,
        'taker_touch_fee': taker['fee'],
        'maker_touch_fee': maker['fee'],
        'formula_id': taker['formula_id'],
        'series_resolution': taker['series_resolution'],
        'maker_credit_floor_zero_refuse': credit['maker_credit_floor_zero_refuse'],
        'content_fresh_flag': flag['content_fresh_flag'],
        'fresh_reason': flag['reason'],
        'queue_attribution_bin': queue_bin,
        'lee_ready': 'REFUSED',
        'aggressor_inference': None,
        'source': 'synthetic_schema_standin',
    }
    return _scorecard_row(packed)


def fit_player(strikes, family):
    """Monotone fit for one synthetic player ladder. RMS is not returned."""
    if family not in ('isotonic', 'logit_monotone'):
        raise UnknownFamily()
    if not isinstance(strikes, list) or len(strikes) < 2:
        raise OrchestratorError('ladder')
    ordered = sorted(strikes, key=lambda item: item['strike'])
    seen = set()
    for item in ordered:
        token = item['strike']
        if token in seen:
            raise OrchestratorError('strike')
        seen.add(token)
    fitted = _fit_values([item['mid'] for item in ordered], family)
    rows = []
    for item, value in zip(ordered, fitted):
        packed = dict(item)
        packed['family'] = family
        packed['fitted_mid'] = value
        packed['residual'] = item['mid'] - value
        rows.append(_scorecard_row(packed))
    return rows


def partition_ladder(strikes, arm):
    """Group synthetic strikes by event and player, then fit one family."""
    family = _family_name(arm)
    if not isinstance(strikes, list) or not strikes:
        raise OrchestratorError('ladder')
    grouped = {}
    for row in strikes:
        annotated = annotate_strike(row)
        key = (annotated['event_ticker'], annotated['player_id'])
        grouped.setdefault(key, []).append(annotated)
    fitted = []
    for key in sorted(grouped):
        fitted.extend(fit_player(grouped[key], family))
    return fitted


def conductor_pin_status():
    """Report whether checkout bytes match the conductor sha256 values."""
    packet_match = sha256_file(PACKET) == CONDUCTOR_PACKET_SHA256 == PACKET_SHA256
    kernel_match = sha256_file(KERNEL) == CONDUCTOR_KERNEL_SHA256 == KERNEL_SHA256
    stub_match = sha256_file(PANEL_STUB) == CONDUCTOR_PANEL_STUB_SHA256 == PANEL_STUB_SHA256
    return {
        'packet_matches_conductor_claim': packet_match,
        'kernel_matches_conductor_claim': kernel_match,
        'panel_stub_matches_conductor_claim': stub_match,
        'conductor_bytes_in_checkout': packet_match and kernel_match and stub_match,
        'events_n_claim': CONDUCTOR_EVENTS_N_CLAIM,
    }


def _assert_named_copies(name, digest):
    copies = (
        ROOT / name,
        LAB_BUNDLE / name,
        PARENT / 'packets' / name,
        GOVERNANCE_BUNDLE / name,
    )
    for path in copies:
        if sha256_file(path) != digest:
            raise OrchestratorError(name)


def _assert_freeze_bytes():
    _assert_named_copies(PACKET_NAME, PACKET_SHA256)
    _assert_named_copies(KERNEL_NAME, KERNEL_SHA256)
    for path in (
        PANEL_STUB,
        LAB_BUNDLE / 'panel_stub.json',
        GOVERNANCE_BUNDLE / 'panel_stub.json',
    ):
        if sha256_file(path) != PANEL_STUB_SHA256:
            raise OrchestratorError('stub sha256')
    for path in (ADVERSARY_BIND, LAB_BUNDLE / ADVERSARY_NAME, GOVERNANCE_BUNDLE / ADVERSARY_NAME):
        if sha256_file(path) != ADVERSARY_SHA256:
            raise OrchestratorError('adversary sha256')
    for path in (CONDUCTOR_STAMP, LAB_BUNDLE / STAMP_NAME, GOVERNANCE_BUNDLE / STAMP_NAME):
        if sha256_file(path) != CONDUCTOR_STAMP_SHA256:
            raise OrchestratorError('conductor stamp sha256')
    stamp = json.loads(CONDUCTOR_STAMP.read_text())
    if stamp.get('freeze_sha256') != PACKET_SHA256:
        raise OrchestratorError('conductor stamp')
    if stamp.get('parent_freeze_sha256') != KERNEL_SHA256:
        raise OrchestratorError('conductor stamp')
    if stamp.get('panel_stub_sha256') != PANEL_STUB_SHA256:
        raise OrchestratorError('conductor stamp')
    if stamp.get('panel_events') != CONDUCTOR_EVENTS_N_CLAIM:
        raise OrchestratorError('conductor stamp')
    if stamp.get('results') is not None or stamp.get('pnl') is not None:
        raise ScorecardPromotionRefused()


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
    if payload.get('schema_id') != SCHEMA_ID:
        raise OrchestratorError('schema')
    if payload.get('panel_version') != PANEL_VERSION:
        raise PanelVersionRefused()
    if payload.get('packet_id') != PANEL_PACKET_ID:
        raise OrchestratorError('packet')
    if payload.get('series_tickers') != list(SERIES_TICKERS):
        raise OrchestratorError('series')
    if payload.get('cohort_kind') != 'sun_2026-09-27_dual_game_prop_slate_LACBUF_BALDAL':
        raise OrchestratorError('cohort')
    stamp = payload.get('admitted_at')
    if admitted:
        if not isinstance(stamp, str) or not stamp.endswith('Z'):
            raise OrchestratorError('admitted_at')
    elif stamp is not None:
        raise OrchestratorError('admitted_at')
    for key in ('results', 'pnl', 'volume'):
        _require_null(payload, key)
    if payload.get('freeze_packet_sha256') != KERNEL_SHA256:
        raise OrchestratorError('freeze_packet_sha256')
    binds = payload.get('binds') or {}
    if binds.get('fee_lab_sha') != FEEBOOK_COMMIT:
        raise OrchestratorError('feebook commit')
    if binds.get('rails_lab_sha') != RAILS_COMMIT:
        raise OrchestratorError('rails commit')
    if binds.get('fee_formula_id') != feebook.EXAMINER_FORMULA_ID:
        raise OrchestratorError('examiner formula')
    if binds.get('forbid_inherited_q7_fee_literals') is not True:
        raise ShadowFeeLiteralRefused()
    capture = payload.get('capture') or {}
    if capture.get('mode') != 'GET_only_public':
        raise LiveOrdersForbidden()
    if capture.get('host_allowlist') != [PUBLIC_HOST]:
        raise LiveOrdersForbidden()
    routes = capture.get('routes_allowlist')
    if not isinstance(routes, list) or not routes:
        raise LiveOrdersForbidden()
    for route in routes:
        if not isinstance(route, str) or not route.startswith('GET '):
            raise LiveOrdersForbidden()
        if OUT_OF_SCOPE_ROUTE in route or 'portfolio/orders' in route:
            raise LiveOrdersForbidden()
    gate = payload.get('admit_gate') or {}
    if gate.get('admit_py_run') is True:
        raise AdversaryRefused(ADVERSARY_LABELS['admit_py'])
    events = payload.get('events')
    if not isinstance(events, list) or len(events) != CONDUCTOR_EVENTS_N_CLAIM:
        raise OrchestratorError('events')
    tickers = []
    for event in events:
        if not isinstance(event, dict):
            raise OrchestratorError('events')
        ticker = event.get('event_ticker')
        if _slate_banned(ticker) or _slate_banned(event.get('game_id')):
            raise SlateRefused()
        if event.get('series_ticker') not in SERIES_TICKERS:
            raise OrchestratorError('series')
        game = event.get('game_id')
        if game not in SLATE_GAMES or game not in ticker:
            raise SlateRefused()
        if event.get('kalshi_occurrence_datetime') != OCCURRENCE_BY_GAME[game]:
            raise OrchestratorError('occurrence')
        markets = event.get('market_tickers')
        if not isinstance(markets, list):
            raise OrchestratorError('market_tickers')
        if not admitted and markets:
            raise InventedFillRefused()
        for key in INVENTORY_KEYS + ('results', 'pnl'):
            if key in event and event[key] is not None:
                raise InventedFillRefused()
        tickers.append(ticker)
    if tuple(tickers) != SLATE_EVENTS:
        raise OrchestratorError('events')
    excluded = payload.get('excluded')
    if not isinstance(excluded, list) or not excluded:
        raise SlateRefused()
    excluded_events = []
    for block in excluded:
        if not isinstance(block, dict):
            raise SlateRefused()
        names = block.get('events')
        if not isinstance(names, list):
            raise SlateRefused()
        excluded_events.extend(names)
    if tuple(excluded_events) != EXCLUDED_EVENTS:
        raise SlateRefused()
    return payload


def load_panel(stub_path=None, admitted_path=None):
    """Stub by default. panel_admitted.json wins when it is on disk."""
    path = select_panel_path(stub_path, admitted_path)
    if path.resolve() == PANEL_STUB.resolve():
        _assert_freeze_bytes()
    payload = json.loads(path.read_text())
    return _validate_panel(payload, admitted=path.name == 'panel_admitted.json')


def arm_table():
    return tuple({'id': arm, 'family': FAMILIES[arm]} for arm in ARMS)


def instrument_binding(panel=None):
    """One residual-family knob. Fee and rails commits stay fixed."""
    if panel is None:
        panel = load_panel()
    quote = feebook.order_fee('taker', '1', '0.50', round_up=True, series=KERNEL_SERIES)
    assert_examiner_quote(quote)
    if quote['series_resolution'] != 'default_unknown_series':
        raise OrchestratorError('series resolution')
    if hygiene.FEEBOOK_COMMIT != FEEBOOK_COMMIT or hygiene.RAILS_COMMIT != RAILS_COMMIT:
        raise OrchestratorError('pin')
    ahead_bin = hygiene.queue_attribution_bin(rails.QUEUE_AHEAD_DEFAULT)
    if ahead_bin != 'q3300':
        raise OrchestratorError('queue bin')
    pins = conductor_pin_status()
    if pins['conductor_bytes_in_checkout'] is not True:
        raise OrchestratorError('conductor bytes')
    if len(panel.get('events') or []) != CONDUCTOR_EVENTS_N_CLAIM:
        raise OrchestratorError('events')
    return {
        'experiment_id': EXPERIMENT_ID,
        'lab_directory': LAB_DIRECTORY,
        'feature_family': FEATURE_FAMILY,
        'knob': KNOB,
        'arms': arm_table(),
        'panel_version': panel['panel_version'],
        'admitted_at': panel.get('admitted_at'),
        'series_tickers': SERIES_TICKERS,
        'events_n': len(panel.get('events') or []),
        'conductor_events_n_claim': CONDUCTOR_EVENTS_N_CLAIM,
        'slate_games': SLATE_GAMES,
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
        'cap_sr_fx_reopen': False,
        'atl_gb': 'REFUSED',
        'admit_py_run': False,
        'fee_is_knob': False,
        'markout_is_knob': False,
        'dead_cards': DEAD_CARDS,
        'scorecard_fields': SCORECARD_FIELDS,
        'kernel_sha256': KERNEL_SHA256,
        'packet_sha256': PACKET_SHA256,
        'panel_stub_sha256': PANEL_STUB_SHA256,
        'conductor_stamp_sha256': CONDUCTOR_STAMP_SHA256,
        'adversary_sha256': ADVERSARY_SHA256,
        'conductor_packet_sha256_claim': CONDUCTOR_PACKET_SHA256,
        'conductor_parent_freeze_sha256_claim': CONDUCTOR_KERNEL_SHA256,
        'conductor_panel_stub_sha256_claim': CONDUCTOR_PANEL_STUB_SHA256,
        'conductor_bytes_in_checkout': True,
        'packet_matches_conductor_claim': True,
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
    scorecard['atl_gb'] = 'REFUSED'
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


def publish_residual_rms(value):
    """The RMS aggregate is an Examiner field. Any publish is refused."""
    if value is None or value is not None:
        raise ScorecardPromotionRefused()
    raise ScorecardPromotionRefused()


def _report(arm, source, extra):
    family = _family_name(arm)
    published = published_scorecard()
    report = {
        'experiment_id': EXPERIMENT_ID,
        'arm': arm,
        'family': family,
        'source': source,
        'published': published,
        'promoted': False,
        'strategy_pointer': None,
        'live_orders': False,
        'lee_ready': 'REFUSED',
        'atl_gb': 'REFUSED',
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
    """Schema for one family on the loaded panel. The stub has no strike mids."""
    if arm not in FAMILIES:
        raise UnknownFamily()
    if panel is None:
        panel = load_panel()
    events = panel.get('events') or []
    market_count = 0
    for event in events:
        market_count += len(event.get('market_tickers') or [])
    extra = {
        'event_count': len(events),
        'market_count': market_count,
        'admitted_markets': market_count > 0,
        'panel_note': 'market_tickers_empty_not_a_cohort',
    }
    return _report(arm, 'panel', extra)


def load_synthetic_ladder(path=None):
    path = SYNTHETIC_LADDER if path is None else Path(path)
    payload = json.loads(Path(path).read_text())
    if payload.get('source') != 'synthetic_schema_standin':
        raise OrchestratorError('source')
    strikes = payload.get('strikes')
    if not isinstance(strikes, list) or len(strikes) < 2:
        raise OrchestratorError('synthetic ladder')
    return strikes


def conduct_ladder(arm, path=None):
    """In-memory monotone fit on the synthetic ladder. Scorecard fields stay null."""
    rows = partition_ladder(load_synthetic_ladder(path), arm)
    return _report(arm, 'synthetic_schema_standin', {
        'strikes': rows,
        'strike_count': len(rows),
        'player_ids': tuple(sorted({row['player_id'] for row in rows})),
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
        'stamp': json.loads(CONDUCTOR_STAMP.read_text()),
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
