"""C1 KXUFCFIGHT fee and queue honesty bakeoff.

Measurement only. Imports the R1-P1 feebook and the R1-P5 rails. Does not
edit those cores, does not retune Q6-000, does not place live orders, and
does not write scorecard metrics.
"""
import hashlib
import json
import sys
from datetime import datetime
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

LAB_DIRECTORY = 'kalshi_c1_kxufcfight_honesty_lab_20260922'
EXPERIMENT_ID = 'c1_kxufcfight_honesty_20260922'
PACKET_ID = 'C1-KXUFCFIGHT-MEAS'
SERIES = 'KXUFCFIGHT'
PANEL_VERSION = '2026-09-22.c1-kxufcfight-v0'
FEEBOOK_COMMIT = '22371178cb2663250b4762f328069571c48cb551'
RAILS_COMMIT = '6a28e0d6254327ea4e6451c781bec56215ac6cac'
KERNEL = PARENT / 'packets' / 'C1_KXUFCFIGHT_MEASUREMENT_FREEZE_KERNEL_2026-09-22.md'
KERNEL_SHA256 = 'a191c9b3f71030445d1d32684feb6dc1bf09abb7e09403d5dbdf1927eafc63c9'
PANEL_STUB = PARENT / 'lab' / 'astra-capture' / 'c1-kxufcfight' / 'panel_stub.json'
PANEL_STUB_SHA256 = '2cc661d86202d3daf9ffa45320e39d249852a97490f458f72ab7ea8ec5c81a00'
PANEL_ADMITTED = PARENT / 'lab' / 'astra-capture' / 'c1-kxufcfight' / 'panel_admitted.json'
ADMITTED_AT = '2026-09-23T00:49:43Z'
PANEL_SHA256_PREFIX = '24426d80'
CAPTURE_SLOT = 'lab/astra-capture/c1-kxufcfight/'
PRODUCTION_ORDERBOOK_REL = 'lab/astra-capture/c1-kxufcfight/orderbooks'
PRODUCTION_ORDERBOOK_DIR = PARENT / 'lab' / 'astra-capture' / 'c1-kxufcfight' / 'orderbooks'
ADMITTED_ORDERBOOK_TICKERS = (
    'KXUFCFIGHT-26SEP22CONGUA-GUA',
    'KXUFCFIGHT-26SEP22CONGUA-CON',
    'KXUFCFIGHT-26SEP22DEGMOR-MOR',
    'KXUFCFIGHT-26SEP22DEGMOR-DEG',
)
EXAMINER_GATE_NOTE = (
    'C1 stays NOT_SCORED until pinned production orderbooks under '
    'lab/astra-capture/c1-kxufcfight/orderbooks/ and an Examiner-ready '
    'scorecard. Synthetic fixtures are refused for scorecard fill.'
)
SYNTHETIC_BOOKS = ROOT / 'fixtures' / 'synthetic_orderbooks.json'
FROZEN_EXPERIMENT = ROOT / 'FROZEN_EXPERIMENT.json'
EMPTY_RESULTS = ROOT / 'results' / 'EMPTY_RESULTS.json'
SCOUT_DIR = PARENT / 'packets' / 'scout_c1_kxufcfight'
SCOUT_FROZEN = SCOUT_DIR / 'FROZEN_EXPERIMENT.json'
SCOUT_RESULTS = SCOUT_DIR / 'results.json'
SCOUT_EMPTY = SCOUT_DIR / 'results' / 'EMPTY_RESULTS.json'
BAKEOFF_CAPITAL_USD_LABEL = Decimal('5000')
OUTSIDE_BIN = 'outside_pinned_bins'
CAPITAL_ARMS = (
    'A1_shared_pool',
    'A2_shared_soft_reserve',
    'A3_hard_equal_slices',
)
SHADOW_FORMULA_IDS = (
    feebook.GROK_COMPARATOR_FORMULA_ID,
    'q6.order_fees.fixed_point_balance.v1',
)
INVENTORY_KEYS = ('volume_fp', 'volume_24h_fp', 'open_interest_fp')
OUTPUT_KEYS = (
    'reciprocal_book',
    'fee_channel',
    'content_fresh_flag',
    'maker_credit_floor_zero_refuse',
    'queue_attribution_bin',
    'timing_shape',
    'volume_fp',
    'volume_24h_fp',
    'open_interest_fp',
    'strategy_ev',
    'beats_000',
    'completed_profit',
    'fill_rate',
    'annualization',
    'live_promotion',
    'results',
    'pnl',
)


class OrchestratorError(Exception):
    """A pin failed or a measurement write was requested."""


class ScorecardPromotionRefused(OrchestratorError):
    """Filled measurement fields stay out of the freeze packet."""

    def __init__(self):
        super().__init__('scorecard metrics stay null until Examiner GO')


class LiveOrdersForbidden(OrchestratorError):
    """This lab has no live order path."""

    def __init__(self):
        super().__init__('no live orders and no KalshiExecutionAdapter')


class CapitalArmForbidden(OrchestratorError):
    """The shared 5000 USD figure is a measurement label."""

    def __init__(self):
        super().__init__('shared 5000 USD label is not a capital-structure arm')


class PanelVersionRefused(OrchestratorError):
    """The panel file is not the pinned C1 seed."""

    def __init__(self):
        super().__init__('panel_version')


class ShadowFeeLiteralRefused(OrchestratorError):
    """A fee quote bypassed the examiner feebook formula."""

    def __init__(self):
        super().__init__('shadow fee literal')


class InventedInventoryRefused(OrchestratorError):
    """Volume or open interest was filled without a pinned live GET."""

    def __init__(self):
        super().__init__('invented open interest')


def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def execution_adapter():
    """No live order client lives in this lab."""
    raise LiveOrdersForbidden()


def bakeoff_capital(mode=None):
    """Shared 5000 USD measurement label. A1, A2, and A3 are refused."""
    if mode is not None:
        raise CapitalArmForbidden()
    return {
        'bakeoff_capital_usd_label': BAKEOFF_CAPITAL_USD_LABEL,
        'bakeoff_capital_is_strategy_claim': False,
        'capital_structure_arm': None,
    }


def _parse_utc(value):
    if not isinstance(value, str) or not value.endswith('Z'):
        raise OrchestratorError('timestamp')
    return datetime.fromisoformat(value.replace('Z', '+00:00'))


def minutes_to_occurrence(sample_time, occurrence_datetime):
    """Signed minutes from the sample to the Kalshi occurrence clock.

    The value stays on the in-memory label. `timing_shape` on the scorecard
    stays null.
    """
    sample = _parse_utc(sample_time)
    occurrence = _parse_utc(occurrence_datetime)
    delta = occurrence - sample
    seconds = (
        Decimal(delta.days) * Decimal(86400)
        + Decimal(delta.seconds)
        + (Decimal(delta.microseconds) / Decimal('1000000'))
    )
    return seconds / Decimal(60)


def _require_null(payload, key):
    if key not in payload or payload[key] is not None:
        raise InventedInventoryRefused()


def _require_inventory_null(row):
    for key in INVENTORY_KEYS:
        if key in row:
            _require_null(row, key)


def _require_admitted(row):
    """The Clock stamp is the admitted panel. A null stamp is the stub."""
    if row.get('admitted_at') != ADMITTED_AT:
        raise OrchestratorError('admitted_at')


def load_panel(path=None):
    """Pinned admitted panel. The pre-admit stub is refused."""
    path = PANEL_ADMITTED if path is None else Path(path)
    if path.resolve() == PANEL_STUB.resolve():
        raise OrchestratorError('stub is not the admitted panel')
    canonical = path.resolve() == PANEL_ADMITTED.resolve()
    if canonical and not path.is_file():
        raise OrchestratorError('admitted panel')
    if canonical:
        digest = sha256_file(path)
        if not digest.startswith(PANEL_SHA256_PREFIX):
            raise OrchestratorError('panel sha256')
        if sha256_file(KERNEL) != KERNEL_SHA256:
            raise OrchestratorError('kernel sha256')
        if sha256_file(PANEL_STUB) != PANEL_STUB_SHA256:
            raise OrchestratorError('stub sha256')
    payload = json.loads(path.read_text())
    if payload.get('panel_version') != PANEL_VERSION:
        raise PanelVersionRefused()
    if payload.get('packet_id') != PACKET_ID:
        raise OrchestratorError('packet')
    if payload.get('series_ticker') != SERIES:
        raise OrchestratorError('series')
    _require_admitted(payload)
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
    if binds.get('no_000_retune') is not True:
        raise OrchestratorError('000 retune')
    if binds.get('forbid_inherited_q7_fee_literals') is not True:
        raise ShadowFeeLiteralRefused()
    if binds.get('bakeoff_capital_usd_label') != 5000:
        raise OrchestratorError('bakeoff label')
    if binds.get('bakeoff_capital_is_strategy_claim') is not False:
        raise OrchestratorError('strategy claim')
    capture = payload.get('capture') or {}
    if 'POST /portfolio/orders' not in (capture.get('out_of_scope_routes') or []):
        raise LiveOrdersForbidden()
    schedule = capture.get('schedule') or {}
    if schedule.get('recorder_started') is True:
        raise OrchestratorError('recorder')
    objects = payload.get('measurement_objects') or {}
    if objects.get('reciprocal_book', {}).get('status') is not None:
        raise ScorecardPromotionRefused()
    if objects.get('fee_channel_r1p1', {}).get('status') is not None:
        raise ScorecardPromotionRefused()
    rails_labels = objects.get('rails_labels') or {}
    for key in (
        'status',
        'content_fresh_flag',
        'maker_credit_floor_zero_refuse',
        'queue_attribution_bin',
    ):
        if rails_labels.get(key) is not None:
            raise ScorecardPromotionRefused()
    if objects.get('timing_shape', {}).get('status') is not None:
        raise ScorecardPromotionRefused()
    bakeoff = objects.get('fee_queue_honesty_bakeoff_vs_000') or {}
    if bakeoff.get('status') is not None or bakeoff.get('strategy_ev') is not None:
        raise ScorecardPromotionRefused()
    if bakeoff.get('shared_5k_label') is not True:
        raise OrchestratorError('bakeoff label')
    events = payload.get('events') or []
    markets = payload.get('markets') or []
    counts = payload.get('cohort_counts') or {}
    if counts.get('markets_n') != 4 or len(markets) != 4:
        raise OrchestratorError('cohort')
    if counts.get('events_n') != 2 or len(events) != 2:
        raise OrchestratorError('cohort')
    if counts.get('dropped_n') != 2:
        raise OrchestratorError('cohort')
    dropped = payload.get('dropped_from_seed') or {}
    if len(dropped) != 2:
        raise OrchestratorError('cohort')
    for event in events:
        if event.get('series_ticker') != SERIES:
            raise OrchestratorError('series')
        if event.get('panel_version') != PANEL_VERSION:
            raise PanelVersionRefused()
        if event.get('admitted_at') not in (None, ADMITTED_AT):
            raise OrchestratorError('admitted_at')
        for key in ('volume_fp', 'open_interest_fp'):
            _require_null(event, key)
    for market in markets:
        if market.get('series_ticker') != SERIES:
            raise OrchestratorError('series')
        if market.get('panel_version') != PANEL_VERSION:
            raise PanelVersionRefused()
        if market.get('admitted_at') not in (None, ADMITTED_AT):
            raise OrchestratorError('admitted_at')
        if market.get('market_ticker') in dropped:
            raise OrchestratorError('dropped market')
        _require_inventory_null(market)
    return payload


def assert_examiner_quote(quote):
    """Accept only the R1-P1 examiner formula."""
    if not isinstance(quote, dict):
        raise ShadowFeeLiteralRefused()
    formula = quote.get('formula_id')
    if formula in SHADOW_FORMULA_IDS or formula != feebook.EXAMINER_FORMULA_ID:
        raise ShadowFeeLiteralRefused()
    return quote


def bind_order_fee(role, contracts, price, panel=None):
    """Hypothetical size C at P through feebook.order_fee. round_up stays true."""
    if role not in ('taker', 'maker'):
        raise ValueError('role')
    if panel is None:
        panel = load_panel()
    quote = feebook.order_fee(role, contracts, price, round_up=True, series=SERIES)
    assert_examiner_quote(quote)
    if quote['rounded_up'] is not True:
        raise OrchestratorError('round_up')
    if quote['series_resolution'] != 'default_unknown_series':
        raise OrchestratorError('series resolution')
    table = feebook.load_series_table()
    expected_m = feebook.as_decimal(table['default']['M'], 'M')
    panel_m = feebook.as_decimal(panel['binds']['fee_multiplier_live_get'], 'fee_multiplier')
    if quote['M'] != expected_m or quote['M'] != panel_m:
        raise OrchestratorError('multiplier')
    return quote


def classify_completed_profit(scorecard):
    """Feebook gate. A passing label is still not a scorecard write."""
    return feebook.classify_scorecard(scorecard)


def measure_reciprocal_book(orderbook):
    """Asks and spreads from feebook. A missing bid does not invent an ask."""
    book = feebook.reciprocal_book(orderbook)
    if book['bid_yes'] is not None and book['bid_no'] is not None:
        if book['ask_yes'] != feebook.ONE - book['bid_no']:
            raise OrchestratorError('reciprocal ask')
        if book['ask_no'] != feebook.ONE - book['bid_yes']:
            raise OrchestratorError('reciprocal ask')
        if book['spread_yes'] != book['ask_yes'] - book['bid_yes']:
            raise OrchestratorError('spread')
        if book['spread_no'] != book['ask_no'] - book['bid_no']:
            raise OrchestratorError('spread')
    else:
        if book['bid_no'] is None and book['ask_yes'] is not None:
            raise OrchestratorError('invented ask')
        if book['bid_yes'] is None and book['ask_no'] is not None:
            raise OrchestratorError('invented ask')
        if book['spread_yes'] is not None or book['spread_no'] is not None:
            raise OrchestratorError('invented spread')
    return book


def content_fresh_flag(previous, current, *, keepalive=False):
    """R1-P5 freshness. A keepalive is never a fresh book."""
    verdict = rails.judge_freshness(previous, current, keepalive=keepalive)
    return {
        'content_fresh_flag': verdict.fresh,
        'reason': verdict.reason,
    }


def maker_credit_floor_zero_refuse(price, contracts):
    """True when the R1-P5 floored maker credit is zero or negative."""
    try:
        evaluation = rails.admit_maker_quote(price, contracts, series=SERIES)
        refused = False
    except rails.MakerCreditRefused as exc:
        evaluation = exc.evaluation
        refused = True
    assert_examiner_quote(evaluation['fee_quote'])
    if evaluation['rule_id'] != rails.FEE_CREDIT_RULE_ID:
        raise OrchestratorError('fee credit rule')
    return {
        'maker_credit_floor_zero_refuse': refused,
        'admitted': evaluation['admitted'],
        'credit': evaluation['credit'],
        'rule_id': evaluation['rule_id'],
        'formula_id': evaluation['fee_quote']['formula_id'],
    }


def queue_attribution_bin(queue_ahead):
    """Exact match to a pinned rails scenario. Other sizes stay outside."""
    ahead = feebook.as_decimal(queue_ahead, 'queue_ahead')
    if ahead < 0:
        raise ValueError('queue_ahead')
    for label, pinned in rails.QUEUE_SCENARIO_LABELS.items():
        if ahead == pinned:
            return label
    return OUTSIDE_BIN


def instrument_binding():
    """One fee commit, one rails commit, one panel version, no strategy pointer."""
    panel = load_panel()
    probe = bind_order_fee('taker', '1', '0.50')
    capital = bakeoff_capital()
    return {
        'experiment_id': EXPERIMENT_ID,
        'packet_id': PACKET_ID,
        'lab_directory': LAB_DIRECTORY,
        'panel_version': panel['panel_version'],
        'series_ticker': SERIES,
        'feebook_commit': FEEBOOK_COMMIT,
        'rails_commit': RAILS_COMMIT,
        'examiner_formula_id': feebook.EXAMINER_FORMULA_ID,
        'fee_credit_rule_id': rails.FEE_CREDIT_RULE_ID,
        'fee_formula_id': probe['formula_id'],
        'series_resolution': probe['series_resolution'],
        'multiplier': probe['M'],
        'strategy_pointer': None,
        'strategy_claim': False,
        'instrument_contrast': 'Q6-000-instruments',
        'q6_000_retune': False,
        'allocator_ported': False,
        'live_orders': False,
        'forbid_capital_A2_A3': True,
        'capital': capital,
        'queue_bins': tuple(rails.QUEUE_SCENARIO_LABELS),
        'outside_bin': OUTSIDE_BIN,
        'production_capture_path': CAPTURE_SLOT,
        'production_orderbook_dir': PRODUCTION_ORDERBOOK_REL + '/',
        'kernel_sha256': KERNEL_SHA256,
        'panel_stub_sha256': PANEL_STUB_SHA256,
        'panel_admitted_sha256': sha256_file(PANEL_ADMITTED),
        'admitted_at': ADMITTED_AT,
    }


def published_scorecard():
    """Freeze outputs. Every measurement field is present and null."""
    scorecard = {key: None for key in OUTPUT_KEYS}
    for key in OUTPUT_KEYS:
        if scorecard[key] is not None:
            raise ScorecardPromotionRefused()
    scorecard['status'] = 'NOT_RUN'
    scorecard['panel_version'] = PANEL_VERSION
    scorecard['strategy_claim'] = False
    return scorecard


def assert_null_scorecard(payload):
    """Require every measurement field, results, and pnl, and require null."""
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


def _orderbook_pin_key(name):
    return PRODUCTION_ORDERBOOK_REL + '/' + name


def expected_orderbook_pin_keys():
    return tuple(_orderbook_pin_key(ticker + '.json') for ticker in ADMITTED_ORDERBOOK_TICKERS)


def production_orderbook_pins(frozen=None):
    """Sha256 map from the freeze. Missing means no production pin yet."""
    if frozen is None:
        frozen = json.loads(FROZEN_EXPERIMENT.read_text())
    pins = frozen.get('production_orderbook_pins', {})
    if not isinstance(pins, dict):
        raise OrchestratorError('production orderbook pin')
    for key, value in pins.items():
        if not isinstance(key, str) or not isinstance(value, str) or len(value) != 64:
            raise OrchestratorError('production orderbook pin')
    return dict(pins)


def _production_orderbook_files(directory):
    directory = Path(directory)
    if not directory.exists():
        return []
    if not directory.is_dir():
        raise OrchestratorError('production orderbook pin')
    resolved = directory.resolve()
    files = []
    for path in sorted(resolved.iterdir(), key=lambda item: item.name):
        if path.is_symlink() or not path.is_file():
            raise OrchestratorError('production orderbook pin')
        if path.suffix != '.json' or path.resolve().parent != resolved:
            raise OrchestratorError('production orderbook pin')
        files.append(path)
    return files


def production_orderbook_status(directory=None, pins=None):
    """Pin check for the capture slot.

    No JSON and no pins is ``FIXTURE_GAP``. JSON is accepted only when the
    four admitted names are present and each sha256 matches the pin map.
    Any other file is refused. Status ``PINNED`` is still ``NOT_SCORED``.
    """
    directory = PRODUCTION_ORDERBOOK_DIR if directory is None else Path(directory)
    pins = production_orderbook_pins() if pins is None else dict(pins)
    files = _production_orderbook_files(directory)
    if not files and not pins:
        return {
            'status': 'FIXTURE_GAP',
            'score_status': 'NOT_SCORED',
            'examiner_ready': False,
            'pins': {},
            'production_orderbooks_present': False,
            'reason': 'FIXTURE_GAP',
        }
    expected = expected_orderbook_pin_keys()
    if len(files) != len(expected) or set(pins) != set(expected):
        raise OrchestratorError('production orderbook pin')
    matched = {}
    for path in files:
        key = _orderbook_pin_key(path.name)
        digest = sha256_file(path)
        if key not in pins or pins[key] != digest:
            raise OrchestratorError('production orderbook pin')
        matched[key] = digest
    if set(matched) != set(expected):
        raise OrchestratorError('production orderbook pin')
    return {
        'status': 'PINNED',
        'score_status': 'NOT_SCORED',
        'examiner_ready': False,
        'pins': matched,
        'production_orderbooks_present': True,
        'reason': 'PINNED_AWAITING_EXAMINER',
    }


def examiner_gate(status=None):
    """Score stays closed. Pinned books still wait on Examiner-ready."""
    if status is None:
        status = production_orderbook_status()
    pinned = status.get('status') == 'PINNED'
    return {
        'score_status': 'NOT_SCORED',
        'examiner_ready': False,
        'production_orderbook_status': 'PINNED' if pinned else 'FIXTURE_GAP',
        'reason': 'PINNED_AWAITING_EXAMINER' if pinned else 'FIXTURE_GAP',
        'note': EXAMINER_GATE_NOTE,
        'results': None,
        'pnl': None,
    }


def assert_score_gate(choice):
    """Synthetic fixtures cannot fill the scorecard. This lab never writes it."""
    if not isinstance(choice, dict):
        raise ScorecardPromotionRefused()
    if choice.get('source') == 'synthetic_schema_standin':
        raise ScorecardPromotionRefused()
    if choice.get('production_orderbook_status') != 'PINNED':
        raise ScorecardPromotionRefused()
    if choice.get('examiner_ready') is not True:
        raise ScorecardPromotionRefused()
    raise ScorecardPromotionRefused()


def resolve_orderbooks():
    """Synthetic label stand-in. Unpinned production JSON is refused.

    A matching pin does not replace the synthetic books and does not fill
    the scorecard. Missing production bytes are ``FIXTURE_GAP``.
    """
    status = production_orderbook_status()
    if not SYNTHETIC_BOOKS.is_file():
        raise OrchestratorError('synthetic books')
    return {
        'source': 'synthetic_schema_standin',
        'books_path': SYNTHETIC_BOOKS,
        'production_orderbooks_present': status['production_orderbooks_present'],
        'production_capture_path': CAPTURE_SLOT,
        'production_orderbook_status': status['status'],
        'score_status': 'NOT_SCORED',
        'examiner_ready': False,
    }


def _queue_ahead(row):
    has_scenario = 'queue_scenario' in row
    has_ahead = 'queue_ahead' in row
    if has_scenario == has_ahead:
        raise OrchestratorError('queue ahead')
    if has_scenario:
        return rails.scenario_queue(row['queue_scenario'])
    return row['queue_ahead']


def _market(panel, ticker):
    for row in panel['markets']:
        if row.get('market_ticker') == ticker:
            return row
    raise OrchestratorError('market')


def _label_book(panel, row, source):
    for key in INVENTORY_KEYS + ('results', 'pnl', 'strategy_ev'):
        if row.get(key) is not None:
            raise InventedInventoryRefused()
    ticker = row['market_ticker']
    if ticker in (panel.get('dropped_from_seed') or {}):
        raise OrchestratorError('dropped market')
    market = _market(panel, ticker)
    wrapped = row['orderbook_fp']
    if 'yes_dollars' not in wrapped or 'no_dollars' not in wrapped:
        raise OrchestratorError('orderbook')
    book = measure_reciprocal_book({'orderbook_fp': wrapped})
    content = rails.canonical_book_content(wrapped)
    current = rails.BookObservation(content, row.get('transaction_time'))
    fresh = content_fresh_flag(None, current, keepalive=False)
    if fresh['content_fresh_flag'] is not True:
        raise OrchestratorError('content fresh')
    complete = book['bid_yes'] is not None and book['bid_no'] is not None
    taker_fee = None
    maker_fee = None
    channel = None
    credit = None
    if complete:
        taker_fee = bind_order_fee('taker', row['hypothetical_contracts'], book['ask_yes'], panel=panel)
        maker_fee = bind_order_fee('maker', row['hypothetical_contracts'], book['bid_yes'], panel=panel)
        channel = feebook.examiner_fee_channel(taker_fee, maker_fee)
        if channel['formula_id'] != feebook.EXAMINER_FORMULA_ID:
            raise ShadowFeeLiteralRefused()
        credit = maker_credit_floor_zero_refuse(book['bid_yes'], row['hypothetical_contracts'])
    timing = None
    if row.get('sample_time') and market.get('occurrence_datetime'):
        timing = minutes_to_occurrence(row['sample_time'], market['occurrence_datetime'])
    return {
        'market_ticker': ticker,
        'event_ticker': market['event_ticker'],
        'source': source,
        'incomplete_book': not complete,
        'reciprocal_book': book,
        'taker_fee': taker_fee,
        'maker_fee': maker_fee,
        'fee_channel': channel,
        'content_fresh_flag': fresh['content_fresh_flag'],
        'freshness_reason': fresh['reason'],
        'maker_credit_floor_zero_refuse': None if credit is None else credit['maker_credit_floor_zero_refuse'],
        'queue_attribution_bin': queue_attribution_bin(_queue_ahead(row)),
        'timing_minutes': timing,
        'volume_fp': None,
        'volume_24h_fp': None,
        'open_interest_fp': None,
        'strategy_ev': None,
        'beats_000': None,
        'completed_profit': None,
        'results': None,
        'pnl': None,
    }


def conduct(panel=None):
    """Label the synthetic books in memory. The published scorecard stays null."""
    if panel is None:
        panel = load_panel()
    choice = resolve_orderbooks()
    payload = json.loads(Path(choice['books_path']).read_text())
    if payload.get('source') != 'synthetic_schema_standin':
        raise OrchestratorError('source')
    books = payload.get('books')
    if not isinstance(books, list) or len(books) != 4:
        raise OrchestratorError('synthetic books')
    labels = [_label_book(panel, row, choice['source']) for row in books]
    published = assert_null_scorecard(published_scorecard())
    report = {
        'experiment_id': EXPERIMENT_ID,
        'packet_id': PACKET_ID,
        'source': choice['source'],
        'books_path': str(choice['books_path']),
        'production_orderbooks_present': choice['production_orderbooks_present'],
        'production_orderbook_status': choice['production_orderbook_status'],
        'score_status': 'NOT_SCORED',
        'examiner_ready': False,
        'production_capture_path': choice['production_capture_path'],
        'panel_version': panel['panel_version'],
        'strategy_pointer': None,
        'strategy_claim': False,
        'q6_000_retune': False,
        'allocator_ported': False,
        'row_count': len(labels),
        'labels': labels,
        'published': published,
        'promoted': False,
    }
    for key in OUTPUT_KEYS:
        report[key] = None
    assert_null_scorecard(report)
    return report


def frozen_output_snapshot():
    """Read freeze files. Does not modify them."""
    payloads = {
        'frozen': json.loads(FROZEN_EXPERIMENT.read_text()),
        'empty': json.loads(EMPTY_RESULTS.read_text()),
        'scout_results': json.loads(SCOUT_RESULTS.read_text()),
        'scout_empty': json.loads(SCOUT_EMPTY.read_text()),
    }
    snapshot = {}
    for name, payload in payloads.items():
        for key in OUTPUT_KEYS:
            if key not in payload or payload[key] is not None:
                raise ScorecardPromotionRefused()
            snapshot['%s.%s' % (name, key)] = None
    scout = json.loads(SCOUT_FROZEN.read_text())
    for key in ('results', 'pnl'):
        if key not in scout or scout[key] is not None:
            raise ScorecardPromotionRefused()
        snapshot['scout_frozen.%s' % key] = None
    for key in OUTPUT_KEYS:
        if key in scout and scout[key] is not None:
            raise ScorecardPromotionRefused()
    return snapshot
