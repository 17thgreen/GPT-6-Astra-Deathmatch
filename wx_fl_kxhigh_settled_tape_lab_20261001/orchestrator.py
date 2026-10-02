"""WX-FL KXHIGH settled-tape measurement scaffolding.

One knob: price_band on the taker-purchased side, arms WXFL0 / WXFL1 / WXFL2.
This module does not place orders, does not perform HTTP GETs, does not open
capture.sqlite or the live weather database, and does not compute ROI, deltas,
or PnL on the pinned trades. results and pnl stay null.

PRIMARY gap mapping is GM-COV under Conductor ACCEPT
b5bd4f046b3a48cffc5617e5f8680a8b8d9d1688568a6fd723fd3b46a845045a.
That decision overrides the freeze's GM-LIT primary. GM-LIT and GM-LIT-PAD
are sensitivities. GM-LIT-PAD is counts only.
"""

import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

import gap_mapping
import snapshot_loader


ROOT = Path(__file__).resolve().parent
PINS = ROOT / 'pins'
RESULTS = ROOT / 'results'
BUNDLE_TGZ = snapshot_loader.BUNDLE_TGZ
ACCEPT_PATH = PINS / 'CONDUCTOR_ACCEPT_VARIANTS_WX_FL_KXHIGH_SETTLED_TAPE_FREEZE_2026-10-01.json'
RULING_PATH = PINS / 'CONDUCTOR_RULING_VARIANTS_WX_FL_PREFREEZE_2026-10-01.json'
PINS_MANIFEST = PINS / 'MANIFEST.sha256'
VENDORED_REGISTRY = (
    PINS / 'vendored/lab/governance/astra/packets/r3_p3_fl_maker_taker/bands_registry_10c.json'
)
EMPTY_RESULTS_PATH = RESULTS / 'EMPTY_RESULTS.json'
VENDORED_EMPTY = (
    PINS / 'vendored/lab/governance/astra/packets/WX_FL_KXHIGH_SETTLED_TAPE/EMPTY_RESULTS.json'
)

EXPERIMENT_ID = 'WX-FL-KXHIGH-SETTLED-TAPE'
LAB_DIRECTORY = 'wx_fl_kxhigh_settled_tape_lab_20261001'
KNOB = 'price_band'
WXFL0 = 'WXFL0'
WXFL1 = 'WXFL1'
WXFL2 = 'WXFL2'
ARMS = (WXFL0, WXFL1, WXFL2)
ARM_BANDS = {
    WXFL0: ('b00', 'b01'),
    WXFL1: ('b02', 'b03', 'b04', 'b05', 'b06', 'b07'),
    WXFL2: ('b08', 'b09'),
}
BAND_IDS = tuple(band for bands in ARM_BANDS.values() for band in bands)
ARM_LABELS = {
    WXFL0: 'longshot_taker',
    WXFL1: 'mid',
    WXFL2: 'favorite_taker',
}
ACCEPT_SHA256 = 'b5bd4f046b3a48cffc5617e5f8680a8b8d9d1688568a6fd723fd3b46a845045a'
RULING_SHA256 = '0e37f91b60289084f4e660b74bcb12a04f83f66fc93410add3a26baf0dd9f6af'
FREEZE_SHA256 = 'aec5b760f8539ea9f30aa1c3601534dccf78a62ee2026cb939842656e3c20e0f'
BUNDLE_SHA256 = snapshot_loader.BUNDLE_SHA256
SNAPSHOT_SHA256 = snapshot_loader.SNAPSHOT_SHA256
FL_BAND_FREEZE_SHA256 = 'fb6540f52ed5f819ccf6e80bf0cf7eb6d951e065416b9d550fead0c6d06043fa'
REGISTRY_SHA256 = snapshot_loader.REGISTRY_SHA256
DESIGN_LOCK_SHA256 = '4ff6bf2cb79ded3ecb77be57a7502392d1295d8a7cfacfc77b926809e671947c'
EXAMINER_SCORE_SHA256 = '2e74f17b1307b8b57f33a6475cd7ce8af48c470099478cadfb07877b0d70745f'
KILL_SHA256 = 'be2357773ca7a842e6896676e3ba0291f40ef8e0b8f997d46f7124d4b2705229'
EMPTY_RESULTS_SHA256 = '65b673120d9310b26e07c16d78864175b9dc6eac199a7041b156f81cd394f5e5'
IMPLEMENT_BASE = '749bc1464764fda03dcddd1162177ef062b2ece3'
EVIDENCE_CLASS = 'IN_SAMPLE_DEV / HISTORICAL_REPLAY'
STUDY_LABEL = 'HISTORICAL_REPLAY'
FEE_LABEL = 'CACHE_NOT_R1P1'
VERDICT_CEILING = 'ITERATE'
FAMILY_SIZE = 1
KILL_SCOPE = 'KXHIGHCHI/KXHIGHLAX/KXHIGHMIA/KXHIGHNY only'
H1 = 'maker_gross_roi_delta_FL0_minus_FL1 > 0'
H2 = 'maker_gross_roi_delta_FL2_minus_FL1 <= 0'
PRIMARY_MAPPING = 'GM-COV'
CAVEATS = (
    'Sep-24 covers only its last ~5-8 h',
    'Sep-25 lacks its first ~10 h',
    'Sep-25 carries 33,119 of 33,757 trades',
)
CITY_DAYS = (
    'KXHIGHCHI-26SEP24',
    'KXHIGHLAX-26SEP24',
    'KXHIGHMIA-26SEP24',
    'KXHIGHNY-26SEP24',
    'KXHIGHCHI-26SEP25',
    'KXHIGHLAX-26SEP25',
    'KXHIGHMIA-26SEP25',
    'KXHIGHNY-26SEP25',
)
TRADES_BY_CITY_DAY = {
    'KXHIGHCHI-26SEP24': 60,
    'KXHIGHLAX-26SEP24': 341,
    'KXHIGHMIA-26SEP24': 172,
    'KXHIGHNY-26SEP24': 65,
    'KXHIGHCHI-26SEP25': 4374,
    'KXHIGHLAX-26SEP25': 10604,
    'KXHIGHMIA-26SEP25': 10391,
    'KXHIGHNY-26SEP25': 7750,
}
TRADES_BY_DATE = {'26SEP24': 638, '26SEP25': 33119}
TRADES_IN_SCOPE = 33757
GM_LIT_DROPPED = 27199
GM_LIT_KEPT = 6558
GM_LIT_KEPT_BY_CITY_DAY = {
    'KXHIGHCHI-26SEP24': 12,
    'KXHIGHLAX-26SEP24': 97,
    'KXHIGHMIA-26SEP24': 34,
    'KXHIGHNY-26SEP24': 14,
    'KXHIGHCHI-26SEP25': 775,
    'KXHIGHLAX-26SEP25': 2209,
    'KXHIGHMIA-26SEP25': 1701,
    'KXHIGHNY-26SEP25': 1716,
}
GM_LIT_PAD_DROPPED = 33622
GM_LIT_PAD_KEPT = 135
GM_LIT_PAD_KEPT_BY_CITY_DAY = {
    'KXHIGHCHI-26SEP24': 0,
    'KXHIGHCHI-26SEP25': 23,
    'KXHIGHLAX-26SEP24': 7,
    'KXHIGHLAX-26SEP25': 35,
    'KXHIGHMIA-26SEP24': 6,
    'KXHIGHMIA-26SEP25': 46,
    'KXHIGHNY-26SEP24': 0,
    'KXHIGHNY-26SEP25': 18,
}
GM_LIT_COMPONENT_PCT = {
    'budget_only': '53.61',
    'per_ticker_429_only': '11.98',
    'storm_only': '58.51',
}
ONE = Decimal('1')
TICK = Decimal('0.01')
PRICE_TOLERANCE = Decimal('1e-9')
ADMIT1_START = datetime(2026, 9, 27, 0, 0, tzinfo=timezone.utc)
ADMIT1_END = datetime(2026, 9, 30, 4, 0, tzinfo=timezone.utc)
EXAMINER_STATUS = 'HOLD_PRE_PR'
EXAMINER_PATH_AFTER_PR = 'READY_NOT_SCORED'


class OrchestratorError(Exception):
    """The measurement path refused the input."""


class Admit1WindowRejected(OrchestratorError):
    """A trade or settlement falls inside the ADMIT-1 window."""


class LeeReadyRefused(OrchestratorError):
    """Lee-Ready is refused. Direction is not inferred."""


class RebinRefused(OrchestratorError):
    """The 10 cent registry is not rebinned."""


class LiveOrderRefused(OrchestratorError):
    """Live orders are refused."""


class LiveHttpGetRefused(OrchestratorError):
    """Live HTTP GET is refused. This lab makes zero network calls."""


class RealTapeRoiRefused(OrchestratorError):
    """ROI, deltas, and PnL are not computed on pinned trades."""


class NoInvent(OrchestratorError):
    """Fills, PnL, and missing settlement fields are not invented."""


class KeepRefused(OrchestratorError):
    """This measurement cannot KEEP."""


class CacheNotLiveR1P1(OrchestratorError):
    """CACHE_NOT_R1P1 is not a live R1-P1 fee claim. Net stays null."""


def stamp_labels(payload):
    """Labels required on every measurement output."""
    body = dict(payload)
    body['evidence_class'] = EVIDENCE_CLASS
    body['study_label'] = STUDY_LABEL
    body['pre_admitted_at'] = None
    body['pre_admitted_at_flag_possible'] = False
    body['pre_admitted_at_reason'] = 'admitted_at null; card02 never admitted'
    body['family_size'] = FAMILY_SIZE
    body['verdict_ceiling'] = VERDICT_CEILING
    body['counts_toward_keep'] = False
    body['promote'] = False
    body['fee_label'] = FEE_LABEL
    body['fee_honest'] = False
    body['claim_as_live_R1P1'] = False
    body['net'] = None
    body['maker_net_roi_cache'] = None
    body['taker_net_roi_cache'] = None
    body['results'] = None
    body['pnl'] = None
    body['out_of_domain_replication_of'] = FL_BAND_FREEZE_SHA256
    body['accept_sha256'] = ACCEPT_SHA256
    body['caveats'] = list(CAVEATS)
    body['not_an_examiner_score'] = True
    return body


def sha256_file(path):
    return snapshot_loader.sha256_file(path)


def verify_pins_manifest(path=None):
    manifest = Path(path or PINS_MANIFEST)
    root = manifest.parent
    seen = []
    for line in manifest.read_text(encoding='utf-8').splitlines():
        if not line.strip():
            continue
        digest, name = line.split('  ', 1)
        target = root / name
        if sha256_file(target) != digest:
            raise snapshot_loader.ManifestShaMismatch(name)
        seen.append(name)
    expected = {
        BUNDLE_TGZ.name,
        ACCEPT_PATH.name,
        RULING_PATH.name,
    }
    if set(seen) != expected:
        raise snapshot_loader.ManifestShaMismatch('pins manifest set')
    if sha256_file(ACCEPT_PATH) != ACCEPT_SHA256:
        raise snapshot_loader.SnapshotShaMismatch('accept')
    if sha256_file(RULING_PATH) != RULING_SHA256:
        raise snapshot_loader.SnapshotShaMismatch('ruling')
    if sha256_file(BUNDLE_TGZ) != BUNDLE_SHA256:
        raise snapshot_loader.SnapshotShaMismatch('bundle')
    return {'pins_manifest_ok': True, 'results': None, 'pnl': None}


def load_band_registry(path=None):
    registry_path = Path(path or VENDORED_REGISTRY)
    if sha256_file(registry_path) != REGISTRY_SHA256:
        raise RebinRefused('registry sha')
    registry = json.loads(registry_path.read_text(encoding='utf-8'))
    if registry.get('registry_id') != 'astra.r3p3.fl_maker_taker.price_bands_10c.v0':
        raise RebinRefused('registry_id')
    if [band.get('band_id') for band in registry.get('bands', [])] != list(BAND_IDS):
        raise RebinRefused('band_id')
    return registry


def rebin(bands=None):
    """Band rebin exists only as a refusal."""
    del bands
    raise RebinRefused('rebin')


def live_order(path='/orders'):
    """Live order exists only as a refusal."""
    del path
    raise LiveOrderRefused()


def live_http_get(url=None):
    """Live HTTP GET exists only as a refusal. No socket is opened."""
    del url
    raise LiveHttpGetRefused()


def infer_lee_ready(row=None):
    """Lee-Ready exists only as a refusal."""
    del row
    raise LeeReadyRefused()


def claim_keep():
    raise KeepRefused()


def claim_live_r1p1(quote=None):
    del quote
    raise CacheNotLiveR1P1()


def run_admit_py():
    raise OrchestratorError('admit.py')


def read_capture_sqlite(path):
    raise snapshot_loader.CaptureSqliteRefused(str(path))


def open_live_database(path):
    raise snapshot_loader.LiveDatabaseRefused(str(path))


def backfill_gap(payload=None):
    del payload
    raise OrchestratorError('backfill')


def _as_decimal(value, name):
    if isinstance(value, bool) or value is None:
        raise OrchestratorError(name)
    try:
        decimal = Decimal(str(value))
    except Exception as exc:
        raise OrchestratorError(name) from exc
    return decimal


def _as_price(value):
    return _as_decimal(value, 'price')


def _band_bounds(band):
    return (
        Decimal(str(band['price_lo'])),
        Decimal(str(band['price_hi'])),
        bool(band['lo_inclusive']),
        bool(band['hi_inclusive']),
    )


def assign_registry_band(price, registry=None):
    """Assign p_taker with registry lo/hi inclusivity. No other cut."""
    if registry is None:
        registry = load_band_registry()
    price = _as_price(price)
    matched = []
    for band in registry['bands']:
        lo, hi, lo_in, hi_in = _band_bounds(band)
        above = price >= lo if lo_in else price > lo
        below = price <= hi if hi_in else price < hi
        if above and below:
            matched.append(band['band_id'])
    if len(matched) != 1:
        raise RebinRefused('assignment')
    return matched[0]


def arm_for_band(band_id):
    for arm, bands in ARM_BANDS.items():
        if band_id in bands:
            return arm
    raise RebinRefused(band_id)


def assign_arm(price, registry=None):
    band_id = assign_registry_band(price, registry)
    return arm_for_band(band_id), band_id


def parse_ts(value):
    if isinstance(value, datetime):
        if value.tzinfo is None:
            raise OrchestratorError('timestamp')
        return value.astimezone(timezone.utc)
    return datetime.fromtimestamp(gap_mapping.parse_epoch(value), timezone.utc)


def in_admit1_window(value):
    if value is None:
        return False
    moment = parse_ts(value)
    return ADMIT1_START <= moment < ADMIT1_END


def assert_outside_admit1(value, source):
    if in_admit1_window(value):
        raise Admit1WindowRejected(source)


def locdo_vote_threshold(n_eff):
    """ceil(2n/3). n=8 returns 6. n_eff < 3 returns None (inconclusive)."""
    if n_eff < 3:
        return None
    return (2 * n_eff + 2) // 3


def _blank():
    return {'return': Decimal('0'), 'capital': Decimal('0'), 'contracts': Decimal('0'), 'n': 0}


def _accumulate(rows, one_tick=False):
    by_arm = {arm: _blank() for arm in ARMS}
    by_event = {}
    for row in rows:
        if row.get('synthetic') is not True:
            raise RealTapeRoiRefused()
        arm = row['arm']
        if arm not in by_arm:
            raise RebinRefused('row arm')
        if row.get('y_s') not in (0, 1):
            raise NoInvent('y_s')
        quantity = _as_decimal(row['q'], 'q')
        if quantity <= 0:
            raise OrchestratorError('q')
        price = _as_price(row['p_taker'])
        outcome = Decimal(row['y_s'])
        maker_return = quantity * (price - outcome)
        maker_capital = quantity * (ONE - price)
        if one_tick:
            maker_return -= TICK * quantity
            maker_capital += TICK * quantity
        bucket = by_arm[arm]
        bucket['return'] += maker_return
        bucket['capital'] += maker_capital
        bucket['contracts'] += quantity
        bucket['n'] += 1
        event = row['event']
        by_event.setdefault(event, {name: _blank() for name in ARMS})
        event_bucket = by_event[event][arm]
        event_bucket['return'] += maker_return
        event_bucket['capital'] += maker_capital
        event_bucket['contracts'] += quantity
        event_bucket['n'] += 1
    return by_arm, by_event


def maker_gross_roi(bucket):
    """Examiner maker_gross_roi: return / capital. None when capital is 0."""
    if bucket['capital'] == 0:
        return None
    return bucket['return'] / bucket['capital']


def _roi_table(by_event):
    table = {}
    for event, arms in by_event.items():
        table[event] = {arm: maker_gross_roi(arms[arm]) for arm in ARMS}
    return table


def equal_weighted_delta(roi_table, left, right):
    """City-day-equal-weighted mean of per-city-day ROI differences.

    D is the city-days where both arms have capital > 0 (ROI is defined).
    """
    deltas = []
    for event in sorted(roi_table):
        left_roi = roi_table[event][left]
        right_roi = roi_table[event][right]
        if left_roi is None or right_roi is None:
            continue
        deltas.append(left_roi - right_roi)
    if not deltas:
        return None, 0
    return sum(deltas) / Decimal(len(deltas)), len(deltas)


def trade_weighted_delta(by_arm, left, right):
    """Pooled maker_gross_roi[left] - maker_gross_roi[right]."""
    left_roi = maker_gross_roi(by_arm[left])
    right_roi = maker_gross_roi(by_arm[right])
    if left_roi is None or right_roi is None:
        return None
    return left_roi - right_roi


def _delta_pair(rows, one_tick=False):
    by_arm, by_event = _accumulate(rows, one_tick=one_tick)
    table = _roi_table(by_event)
    ew01, n01 = equal_weighted_delta(table, WXFL0, WXFL1)
    ew21, n21 = equal_weighted_delta(table, WXFL2, WXFL1)
    return {
        'EW_delta_FL0_minus_FL1': ew01,
        'EW_delta_FL2_minus_FL1': ew21,
        'n_eff_D01': n01,
        'n_eff_D21': n21,
        'TW_delta_FL0_minus_FL1': trade_weighted_delta(by_arm, WXFL0, WXFL1),
        'TW_delta_FL2_minus_FL1': trade_weighted_delta(by_arm, WXFL2, WXFL1),
    }


def _leave_one_out(rows, key, one_tick=False):
    values = []
    for row in rows:
        if row[key] not in values:
            values.append(row[key])
    if key == 'date' and len(values) < 2:
        return None
    reports = []
    for held in values:
        kept = [row for row in rows if row[key] != held]
        pair = _delta_pair(kept, one_tick=one_tick)
        reports.append({
            'held_out': held,
            'EW_delta_FL0_minus_FL1': pair['EW_delta_FL0_minus_FL1'],
            'EW_delta_FL2_minus_FL1': pair['EW_delta_FL2_minus_FL1'],
            'TW_delta_FL0_minus_FL1': pair['TW_delta_FL0_minus_FL1'],
            'TW_delta_FL2_minus_FL1': pair['TW_delta_FL2_minus_FL1'],
            'verdict_input': key == 'event',
        })
    return reports


def reading_h1(full_delta, locdo_deltas):
    """supports_H1 / contradicts_H1 / inconclusive from fb6540f5 with city-day substitution.

    The vote is >= ceil(2n/3) of the leave-one-city-day-out deltas. n=8 requires 6.
    Leave-one-date-out and leave-one-city-out are not inputs.
    """
    if full_delta is None or locdo_deltas is None:
        return 'inconclusive'
    n_eff = len(locdo_deltas)
    need = locdo_vote_threshold(n_eff)
    if need is None or any(item is None for item in locdo_deltas):
        return 'inconclusive'
    positive = sum(1 for item in locdo_deltas if item > 0)
    nonpositive = sum(1 for item in locdo_deltas if item <= 0)
    if full_delta > 0 and positive >= need:
        return 'supports_H1'
    if full_delta <= 0 and nonpositive >= need:
        return 'contradicts_H1'
    return 'inconclusive'


def reading_h2(full_delta, locdo_deltas):
    """H2 uses <= 0, the fb6540f5 text, not the ruling's loose paraphrase."""
    if full_delta is None or locdo_deltas is None:
        return 'inconclusive'
    n_eff = len(locdo_deltas)
    need = locdo_vote_threshold(n_eff)
    if need is None or any(item is None for item in locdo_deltas):
        return 'inconclusive'
    positive = sum(1 for item in locdo_deltas if item > 0)
    nonpositive = sum(1 for item in locdo_deltas if item <= 0)
    if full_delta <= 0 and nonpositive >= need:
        return 'consistent_with_H2'
    if full_delta > 0 and positive >= need:
        return 'inconsistent_with_H2'
    return 'inconclusive'


def verdict_for(reading):
    """Ceiling is ITERATE. A reading is not a KEEP."""
    del reading
    return VERDICT_CEILING


def measure_synthetic(rows, one_tick=False):
    """Algebra on caller-supplied synthetic rows only. Pinned trades are refused."""
    for row in rows:
        if row.get('synthetic') is not True:
            raise RealTapeRoiRefused()
    full = _delta_pair(rows, one_tick=one_tick)
    locdo = _leave_one_out(rows, 'event', one_tick=one_tick)
    h1_votes = [item['EW_delta_FL0_minus_FL1'] for item in locdo] if locdo else []
    h2_votes = [item['EW_delta_FL2_minus_FL1'] for item in locdo] if locdo else []
    without = [row for row in rows if row.get('date') == '26SEP24']
    without_report = _delta_pair(without, one_tick=one_tick) if without else None
    without_locdo = _leave_one_out(without, 'event', one_tick=one_tick) if without else None
    return {
        'synthetic': True,
        'one_tick_worse': one_tick,
        'full': full,
        'locdo': locdo,
        'lodo': _leave_one_out(rows, 'date', one_tick=one_tick),
        'loco': _leave_one_out(rows, 'city', one_tick=one_tick),
        'without_sep25': {
            'full': without_report,
            'locdo': without_locdo,
            'lodo': None,
            'loco': _leave_one_out(without, 'city', one_tick=one_tick) if without else None,
        },
        'variants_proposed_reading_H1': reading_h1(full['EW_delta_FL0_minus_FL1'], h1_votes),
        'variants_proposed_reading_H2': reading_h2(full['EW_delta_FL2_minus_FL1'], h2_votes),
        'reading': None,
        'verdict': VERDICT_CEILING,
        'kill_scope': KILL_SCOPE,
        'h1': H1,
        'h2': H2,
        'results': None,
        'pnl': None,
        'maker_net_roi_cache': None,
        'taker_net_roi_cache': None,
    }


def _lee_ready_requested(trade):
    if trade.get('lee_ready') or trade.get('infer_side'):
        return True
    method = trade.get('direction_method')
    if not isinstance(method, str):
        return False
    return 'lee-ready' in method.lower().replace('_', '-')


def classify_trade(trade, registry=None):
    """Include a public print or count an exclusion. Never impute a dropped row.

    Settlement outcome is used only as the yes/no gate here. y_s is not returned
    for pinned trades, so the count path cannot accumulate ROI.
    """
    if not isinstance(trade, dict):
        raise OrchestratorError('trade')
    if trade.get('backfill') or trade.get('gap_backfill') or trade.get('interpolate'):
        raise OrchestratorError('backfill')
    if _lee_ready_requested(trade):
        raise LeeReadyRefused()
    if trade.get('lookahead') or trade.get('use_future_print'):
        raise OrchestratorError('lookahead')
    for key in ('fill', 'fills', 'pnl', 'astra_pnl', 'simulated_fill', 'invent_settlement'):
        if key in trade:
            raise NoInvent(key)
    ticker = trade.get('ticker')
    event = trade.get('event')
    if event in ('KXHIGHCHI-26SEP26', 'KXHIGHMIA-26SEP26', 'KXHIGHNY-26SEP26'):
        return {'included': False, 'reason': 'out_of_scope_sep26'}
    if ticker not in _frozen_ticker_set():
        return {'included': False, 'reason': 'out_of_scope'}
    assert_outside_admit1(trade.get('created_time') or trade.get('created_epoch'), 'trades')
    assert_outside_admit1(trade.get('settlement_ts'), 'settlement')
    assert_outside_admit1(trade.get('received_at'), 'received_at')
    result = trade.get('result')
    if result not in ('yes', 'no'):
        return {'included': False, 'reason': 'market_result_not_yes_no'}
    close_time = trade.get('close_time')
    created = trade.get('created_time')
    if created is None or close_time is None:
        raise NoInvent('clock')
    if parse_ts(created) >= parse_ts(close_time):
        return {'included': False, 'reason': 'post_close'}
    if 'is_block_trade' not in trade or not isinstance(trade['is_block_trade'], bool):
        raise OrchestratorError('is_block_trade')
    if trade['is_block_trade'] is True:
        return {'included': False, 'reason': 'block'}
    side = trade.get('taker_outcome_side')
    if side not in ('yes', 'no'):
        return {'included': False, 'reason': 'taker_conflict'}
    book_ok = (
        (side == 'yes' and trade.get('taker_book_side') == 'bid')
        or (side == 'no' and trade.get('taker_book_side') == 'ask')
    )
    column_side = trade.get('taker_side')
    raw_side = trade.get('raw_taker_side', column_side)
    if column_side != side or raw_side != side or not book_ok:
        return {'included': False, 'reason': 'taker_conflict'}
    yes_price = _as_price(trade.get('yes_price_dollars'))
    no_price = _as_price(trade.get('no_price_dollars'))
    if abs(yes_price + no_price - ONE) > PRICE_TOLERANCE:
        return {'included': False, 'reason': 'price_inconsistent'}
    p_taker = yes_price if side == 'yes' else no_price
    try:
        arm, band_id = assign_arm(p_taker, registry)
    except RebinRefused:
        return {'included': False, 'reason': 'price_out_of_registry'}
    if 'count_fp' not in trade:
        raise NoInvent('count_fp')
    quantity = _as_decimal(trade['count_fp'], 'count_fp')
    if quantity <= 0:
        raise OrchestratorError('count_fp')
    return {
        'included': True,
        'reason': None,
        'row': {
            'arm': arm,
            'band_id': band_id,
            'ticker': ticker,
            'event': event,
            'city': trade.get('city') or event.split('-')[0],
            'date': trade.get('date') or event.split('-', 1)[1],
            'created_epoch': trade.get('created_epoch', gap_mapping.parse_epoch(created)),
            'synthetic': False,
            'evidence_class': EVIDENCE_CLASS,
            'pre_admitted_at': None,
            'pre_admitted_at_flag_possible': False,
        },
    }


_TICKER_CACHE = None


def _frozen_ticker_set():
    global _TICKER_CACHE
    if _TICKER_CACHE is None:
        frozen_path = (
            PINS / 'vendored/lab/governance/astra/packets/WX_FL_KXHIGH_SETTLED_TAPE/FROZEN_EXPERIMENT.json'
        )
        if sha256_file(frozen_path) != snapshot_loader.FROZEN_SHA256:
            raise snapshot_loader.SnapshotShaMismatch('frozen experiment')
        payload = json.loads(frozen_path.read_text(encoding='utf-8'))
        _TICKER_CACHE = set(payload['universe']['markets'])
    return _TICKER_CACHE


def assert_finalized_results_agree(rows):
    """Hard fail when later finalized results disagree with the first."""
    seen = {}
    for row in rows:
        if row.get('status') != 'finalized':
            continue
        result = row.get('result')
        if result in (None, ''):
            continue
        ticker = row['ticker']
        if ticker not in seen:
            seen[ticker] = result
        elif seen[ticker] != result:
            raise snapshot_loader.ResultDisagreement(ticker)
    return True


def _empty_arm_city():
    return {arm: {event: 0 for event in CITY_DAYS} for arm in ARMS}


def _add(table, arm, event):
    table[arm][event] += 1


def _arm_totals(table):
    return {arm: sum(table[arm].values()) for arm in ARMS}


def _mapping_arm_counts(included, windows, drop_fn):
    dropped = _empty_arm_city()
    kept = _empty_arm_city()
    for row in included:
        if drop_fn(row['created_epoch'], row['ticker'], windows):
            _add(dropped, row['arm'], row['event'])
        else:
            _add(kept, row['arm'], row['event'])
    return {
        'dropped_per_arm_city_day': dropped,
        'kept_per_arm_city_day': kept,
        'dropped_per_arm': _arm_totals(dropped),
        'kept_per_arm': _arm_totals(kept),
        'dropped_n': sum(_arm_totals(dropped).values()),
        'kept_n': sum(_arm_totals(kept).values()),
    }


def _timestamp_mapping(trades, windows, drop_fn):
    dropped = {event: 0 for event in CITY_DAYS}
    kept = {event: 0 for event in CITY_DAYS}
    for trade in trades:
        event = trade['event']
        if drop_fn(trade['created_epoch'], trade['ticker'], windows):
            dropped[event] += 1
        else:
            kept[event] += 1
    return {
        'dropped_n': sum(dropped.values()),
        'kept_n': sum(kept.values()),
        'dropped_by_city_day': dropped,
        'kept_by_city_day': kept,
        'scope': 'timestamp_only_before_row_rules',
    }


def _unassignable(trades, windows, drop_fn):
    return sum(1 for trade in trades if drop_fn(trade['created_epoch'], trade['ticker'], windows))


def assert_timestamp_universe(timestamp):
    if timestamp['trades_in_scope_pre_w0'] != TRADES_IN_SCOPE:
        raise OrchestratorError('trade count')
    if timestamp['by_city_day'] != TRADES_BY_CITY_DAY:
        raise OrchestratorError('city-day count')
    if timestamp['by_date'] != TRADES_BY_DATE:
        raise OrchestratorError('date count')
    if timestamp['trades_created_ge_w0'] != 0 or timestamp['trades_received_ge_w0'] != 0:
        raise Admit1WindowRejected('pinned tape')
    if timestamp['post_close_timestamp_only'] != 0:
        raise OrchestratorError('post close')
    if timestamp['n_markets'] != 48 or timestamp['n_city_days'] != 8:
        raise OrchestratorError('universe')
    return True


def build_counts(frame=None):
    """Counts only. Does not call measure_synthetic and does not emit prices."""
    frame = frame or snapshot_loader.load_frame()
    assert_timestamp_universe(frame['timestamp'])
    if frame['registry_sha256'] != REGISTRY_SHA256:
        raise RebinRefused('registry sha')
    registry = frame['registry']
    if [band.get('band_id') for band in registry['bands']] != list(BAND_IDS):
        raise RebinRefused('band_id')
    included = []
    exclusions = Counter()
    unassigned_trades = []
    for trade in frame['trades_pre_w0']:
        classified = classify_trade(trade, registry)
        if classified['included']:
            included.append(classified['row'])
        else:
            exclusions[classified['reason']] += 1
            unassigned_trades.append(trade)
    windows = gap_mapping.flagged_windows(frame['gap_rows'], _frozen_ticker_set())
    proven = gap_mapping.attach_proof(windows, frame['poll_rows'], sorted(_frozen_ticker_set()))
    summary = gap_mapping.window_summary(proven, sorted(_frozen_ticker_set()))
    near_miss = gap_mapping.near_miss_requested_before_end(proven, frame['poll_rows'])

    def cov(created, ticker, _windows=None):
        del _windows
        return gap_mapping.gm_cov_drops(created, ticker, proven)

    def lit(created, ticker, _windows=None):
        del _windows
        return gap_mapping.gm_lit_drops(created, ticker, windows, pad_budget=0.0)

    def pad(created, ticker, _windows=None):
        del _windows
        return gap_mapping.gm_lit_drops(
            created, ticker, windows, pad_budget=gap_mapping.BUDGET_PAD_SECONDS
        )

    def component(stream):
        subset = [window for window in windows if window['stream'] == stream]

        def drop(created, ticker, _windows=None):
            del _windows
            return gap_mapping.gm_lit_drops(created, ticker, subset, pad_budget=0.0)

        return _timestamp_mapping(frame['trades_pre_w0'], subset, drop)

    if len(included) + sum(exclusions.values()) != TRADES_IN_SCOPE:
        raise OrchestratorError('row-rule partition')
    row_counts = _empty_arm_city()
    for row in included:
        _add(row_counts, row['arm'], row['event'])
    timestamp_lit = _timestamp_mapping(frame['trades_pre_w0'], windows, lit)
    timestamp_pad = _timestamp_mapping(frame['trades_pre_w0'], windows, pad)
    timestamp_cov = _timestamp_mapping(frame['trades_pre_w0'], proven, cov)
    if timestamp_lit['dropped_n'] != GM_LIT_DROPPED or timestamp_lit['kept_n'] != GM_LIT_KEPT:
        raise OrchestratorError('GM-LIT %s' % (timestamp_lit['dropped_n'], timestamp_lit['kept_n']))
    if timestamp_lit['kept_by_city_day'] != GM_LIT_KEPT_BY_CITY_DAY:
        raise OrchestratorError('GM-LIT city-day %s' % timestamp_lit['kept_by_city_day'])
    if timestamp_pad['dropped_n'] != GM_LIT_PAD_DROPPED or timestamp_pad['kept_n'] != GM_LIT_PAD_KEPT:
        raise OrchestratorError('GM-LIT-PAD %s' % (timestamp_pad['dropped_n'], timestamp_pad['kept_n']))
    if timestamp_pad['kept_by_city_day'] != GM_LIT_PAD_KEPT_BY_CITY_DAY:
        raise OrchestratorError('GM-LIT-PAD city-day %s' % timestamp_pad['kept_by_city_day'])
    components = {
        'budget_only': component('kalshi_trades_budget'),
        'per_ticker_429_only': component('kalshi_trades'),
        'storm_only': component('kalshi_all'),
    }
    for name, expected_pct in GM_LIT_COMPONENT_PCT.items():
        dropped = components[name]['dropped_n']
        pct = (Decimal(dropped) * Decimal(100) / Decimal(TRADES_IN_SCOPE)).quantize(Decimal('0.01'))
        if str(pct) != expected_pct:
            raise OrchestratorError('%s %s != %s (%s)' % (name, pct, expected_pct, dropped))
    cov_arm = _mapping_arm_counts(included, proven, cov)
    lit_arm = _mapping_arm_counts(included, windows, lit)
    pad_arm = _mapping_arm_counts(included, windows, pad)
    for arm_counts in (cov_arm, lit_arm, pad_arm):
        if arm_counts['kept_n'] + arm_counts['dropped_n'] != len(included):
            raise OrchestratorError('arm partition')
    payload = {
        'experiment_id': EXPERIMENT_ID,
        'primary_mapping': PRIMARY_MAPPING,
        'primary_mapping_source': 'ACCEPT decision 1 overrides freeze GM-LIT primary',
        'cursor_minus_1s_assumed': False,
        'zero_gets': True,
        'zero_orders': True,
        'timestamp_universe': frame['timestamp'],
        'row_rule_trade_counts_per_arm_city_day': row_counts,
        'row_rule_trade_counts_per_arm': _arm_totals(row_counts),
        'row_rule_exclusions': dict(exclusions),
        'row_rule_included_n': len(included),
        'gm_cov': {
            'rule': (
                'A gap window is covered only if a later poll cursor range '
                '[min_ts, requested_at) spans the whole window and that poll '
                'completed with no 429, no truncation, and no pagination break. '
                'Trades whose created_time falls in an unproven window are dropped '
                'from all arms. Coverage is not assumed from cursor-minus-1s.'
            ),
            'windows': summary,
            'near_miss_complete_poll_requested_at_before_window_end': near_miss,
            'near_miss_note': (
                'Counted and left not proven. The span rule was not loosened.'
            ),
            'timestamp_only': timestamp_cov,
            'per_arm': cov_arm,
            'excluded_gap_n_unassignable': _unassignable(unassigned_trades, proven, cov),
        },
        'gm_lit': {
            'role': 'sensitivity',
            'decisive': False,
            'timestamp_only': timestamp_lit,
            'per_arm': lit_arm,
            'excluded_gap_n_unassignable': _unassignable(unassigned_trades, windows, lit),
            'components_timestamp_only': {
                name: {
                    'dropped_n': report['dropped_n'],
                    'kept_n': report['kept_n'],
                    'dropped_pct': str(
                        (Decimal(report['dropped_n']) * Decimal(100) / Decimal(TRADES_IN_SCOPE))
                        .quantize(Decimal('0.01'))
                    ),
                }
                for name, report in components.items()
            },
        },
        'gm_lit_pad': {
            'role': 'counts_only',
            'pad_seconds': gap_mapping.BUDGET_PAD_SECONDS,
            'decisive': False,
            'not_interpretable_for_ew': True,
            'timestamp_only': timestamp_pad,
            'per_arm': pad_arm,
            'excluded_gap_n_unassignable': _unassignable(unassigned_trades, windows, pad),
        },
    }
    return stamp_labels(payload)


def _json_ready(value):
    if isinstance(value, Decimal):
        raise RealTapeRoiRefused()
    if isinstance(value, dict):
        return {key: _json_ready(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_json_ready(item) for item in value]
    if isinstance(value, tuple):
        return [_json_ready(item) for item in value]
    return value


def _reject_price_keys(value, path=''):
    banned = {
        'yes_price_dollars', 'no_price_dollars', 'p_taker', 'count_fp', 'y_s',
        'maker_gross_roi', 'maker_gross_return_usd', 'maker_capital_usd',
        'taker_gross_roi',
    }
    if isinstance(value, dict):
        for key, item in value.items():
            if key in banned and item is not None:
                raise RealTapeRoiRefused(path + key)
            if key == 'result' and item not in (None,):
                raise RealTapeRoiRefused(path + key)
            _reject_price_keys(item, path + key + '.')
    elif isinstance(value, list):
        for item in value:
            _reject_price_keys(item, path)


def published_scorecard():
    """Pinned empty card. results and pnl stay null. This is not an Examiner score."""
    if sha256_file(VENDORED_EMPTY) != EMPTY_RESULTS_SHA256:
        raise snapshot_loader.SnapshotShaMismatch('empty results')
    if sha256_file(EMPTY_RESULTS_PATH) != EMPTY_RESULTS_SHA256:
        raise snapshot_loader.SnapshotShaMismatch('results empty')
    payload = json.loads(EMPTY_RESULTS_PATH.read_text(encoding='utf-8'))
    if payload.get('results') is not None or payload.get('pnl') is not None:
        raise OrchestratorError('results')
    return payload


def scorecard_shell():
    """Lab scorecard shell. Metrics that would be ROI stay null."""
    return stamp_labels({
        'id': 'WX_FL_KXHIGH_SETTLED_TAPE_SCORECARD_SHELL',
        'status': EXAMINER_STATUS,
        'examiner_path_after_pr': EXAMINER_PATH_AFTER_PR,
        'scored': False,
        'signed_by_examiner': False,
        'stub_ready': False,
        'verdict': None,
        'reading': None,
        'primary_mapping': PRIMARY_MAPPING,
        'h1': H1,
        'h2': H2,
        'kill_scope': KILL_SCOPE,
        'EW_delta_FL0_minus_FL1': None,
        'EW_delta_FL2_minus_FL1': None,
        'TW_delta_FL0_minus_FL1': None,
        'TW_delta_FL2_minus_FL1': None,
        'n_eff_D01': None,
        'n_eff_D21': None,
        'implement_base': IMPLEMENT_BASE,
        'freeze_sha256': FREEZE_SHA256,
        'bundle_sha256': BUNDLE_SHA256,
        'snapshot_sha256': SNAPSHOT_SHA256,
        'ruling_sha256': RULING_SHA256,
        'note': 'Implementer shell only. Counts live in sibling JSON files and are not ROI.',
    })


def write_count_files(counts, results_dir=None):
    results_dir = Path(results_dir or RESULTS)
    results_dir.mkdir(parents=True, exist_ok=True)
    ready = _json_ready(counts)
    _reject_price_keys(ready)
    files = {
        'TIMESTAMP_UNIVERSE_COUNTS.json': stamp_labels({
            'timestamp_universe': ready['timestamp_universe'],
        }),
        'ARM_CITY_DAY_COUNTS.json': stamp_labels({
            'row_rule_trade_counts_per_arm_city_day': ready['row_rule_trade_counts_per_arm_city_day'],
            'row_rule_trade_counts_per_arm': ready['row_rule_trade_counts_per_arm'],
            'row_rule_included_n': ready['row_rule_included_n'],
            'row_rule_exclusions': ready['row_rule_exclusions'],
            'note': 'Row-rule arm assignment before gap drops. Not ROI.',
        }),
        'GM_COV_COUNTS.json': stamp_labels({
            'primary': True,
            'gm_cov': ready['gm_cov'],
        }),
        'GM_LIT_COUNTS.json': stamp_labels({
            'primary': False,
            'gm_lit': ready['gm_lit'],
        }),
        'GM_LIT_PAD_COUNTS.json': stamp_labels({
            'primary': False,
            'counts_only': True,
            'gm_lit_pad': ready['gm_lit_pad'],
        }),
        'SCORECARD.json': scorecard_shell(),
    }
    for name, payload in files.items():
        _reject_price_keys(payload)
        text = json.dumps(payload, indent=2, sort_keys=True) + '\n'
        (results_dir / name).write_text(text, encoding='utf-8')
    return files


def conduct(results_dir=None):
    """Verify pins, count the pinned tape, and leave results and pnl null."""
    verify_pins_manifest()
    counts = build_counts()
    published_scorecard()
    write_count_files(counts, results_dir)
    return {
        'experiment_id': EXPERIMENT_ID,
        'examiner_status': EXAMINER_STATUS,
        'scored': False,
        'primary_mapping': PRIMARY_MAPPING,
        'row_rule_included_n': counts['row_rule_included_n'],
        'gm_cov_windows': counts['gm_cov']['windows'],
        'gm_cov_dropped_per_arm': counts['gm_cov']['per_arm']['dropped_per_arm'],
        'gm_cov_kept_per_arm': counts['gm_cov']['per_arm']['kept_per_arm'],
        'gm_lit_timestamp': counts['gm_lit']['timestamp_only'],
        'gm_lit_per_arm': counts['gm_lit']['per_arm'],
        'gm_lit_pad_timestamp': counts['gm_lit_pad']['timestamp_only'],
        'results': None,
        'pnl': None,
        'zero_gets': True,
        'zero_orders': True,
    }


def authority_report():
    return stamp_labels({
        'experiment_id': EXPERIMENT_ID,
        'implement_base': IMPLEMENT_BASE,
        'lab_directory': LAB_DIRECTORY,
        'accept_sha256': ACCEPT_SHA256,
        'ruling_sha256': RULING_SHA256,
        'freeze_sha256': FREEZE_SHA256,
        'bundle_sha256': BUNDLE_SHA256,
        'snapshot_sha256': SNAPSHOT_SHA256,
        'design_lock_sha256': DESIGN_LOCK_SHA256,
        'band_registry_sha256': REGISTRY_SHA256,
        'fl_band_freeze_sha256': FL_BAND_FREEZE_SHA256,
        'examiner_score_sha256': EXAMINER_SCORE_SHA256,
        'kill_sha256': KILL_SHA256,
        'gaps_sha256': snapshot_loader.GAPS_SHA256,
        'polls_sha256': snapshot_loader.POLLS_SHA256,
        'primary_mapping': PRIMARY_MAPPING,
        'h1': H1,
        'h2': H2,
        'kill_scope': KILL_SCOPE,
        'locdo_threshold_n8': locdo_vote_threshold(8),
        'zero_gets': True,
        'zero_orders': True,
        'sqlite3_module': 'snapshot_loader.py',
        'snapshot_open': 'file:...?mode=ro&immutable=1 after sha256',
        'cited_by_accept_absent_from_bundle_not_invented': {
            'packet_manifest_prefix': '21beb0b5',
            'ping_prefix': '2fbc2515',
        },
    })


if __name__ == '__main__':
    summary = conduct()
    print(json.dumps({
        'row_rule_included_n': summary['row_rule_included_n'],
        'gm_cov_windows': summary['gm_cov_windows'],
        'gm_cov_dropped_per_arm': summary['gm_cov_dropped_per_arm'],
        'gm_lit_dropped': summary['gm_lit_timestamp']['dropped_n'],
        'gm_lit_kept': summary['gm_lit_timestamp']['kept_n'],
        'results': summary['results'],
        'pnl': summary['pnl'],
    }, indent=2, sort_keys=True))
