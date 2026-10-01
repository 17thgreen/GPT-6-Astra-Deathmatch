"""Q6S5 KXMLBSPREAD game-phase settled-tape measurement path.

One knob: game_phase. Q6S5GP0 is pregame (created_time < scheduled first
pitch). Q6S5GP1 is in-play (scheduled first pitch <= created_time < close).
Prints at or after close are excluded.

Scheduled first pitch is parsed from pinned rules_primary and cross-checked
against the event ticker. The label is first_pitch_source=SCHEDULED_START_PROXY.
This module does not place orders, does not run admit.py, does not open
ADMIT-1 capture.sqlite, does not rebin the registry, and does not write
results or pnl.
"""
import copy
import hashlib
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PARENT = ROOT.parent
FEEBOOK_ROOT = PARENT / 'kalshi_feebook_lab_20260922'
if str(FEEBOOK_ROOT) not in sys.path:
    sys.path.insert(0, str(FEEBOOK_ROOT))
import feebook  # noqa: E402


LAB_DIRECTORY = 'kalshi_q6s5_kxmlbspread_game_phase_settled_tape_lab_20261001'
EXPERIMENT_ID = 'Q6S5-KXMLBSPREAD-GAME-PHASE-SETTLED-TAPE'
PACKET_ID = 'Q6S5-KXMLBSPREAD-FEEQUEUE-HARNESS'
FEATURE_FAMILY = 'settled_tape_game_phase'
SERIES = 'KXMLBSPREAD'
KNOB = 'game_phase'
FAMILY_SIZE = 4
FAMILY_KNOBS = ('analysis_slice', 'fill_model', 'price_band', 'game_phase')
ORTHOGONAL_KNOBS = ('analysis_slice', 'fill_model', 'price_band')
Q6S5GP0 = 'Q6S5GP0'
Q6S5GP1 = 'Q6S5GP1'
ARMS = (Q6S5GP0, Q6S5GP1)
ARM_LABELS = {Q6S5GP0: 'pregame', Q6S5GP1: 'inplay'}
FL1_BANDS = ('b02', 'b03', 'b04', 'b05', 'b06', 'b07')
BAND_IDS = (
    'b00', 'b01', 'b02', 'b03', 'b04', 'b05', 'b06', 'b07', 'b08', 'b09',
)
FEEBOOK_COMMIT = '22371178cb2663250b4762f328069571c48cb551'
RAILS_COMMIT = '6a28e0d6254327ea4e6451c781bec56215ac6cac'
ACCEPT_SHA256 = '08d23b363d72b8c8599772ee6fc6736cb90f13e8ed814b12c59b58fd5c7dc91e'
FREEZE_SHA256 = '5beba803f3f6d33410409acc23ad3b782be62dc8829a0f54584e1da8ac18575a'
BUNDLE_SHA256 = '6576ee6cf9f023137e4357270f228dd9a5d29e3dc1d5e7ced85384681f2a7ecc'
BAND_REGISTRY_SHA256 = '0860cbe28d28ecc6142ddf6f1ebb67792084264ed82e0b4d868c3b3138ea5312'
PACKET_MANIFEST_SHA256 = '88af3bd79ad37c6fa09cfbe1bcd516c72b8a35d2928ce04eeaec994b5c1233a1'
FROZEN_EXPERIMENT_SHA256 = 'b8ba41d570211a49adabe28f21c37e33b21e76341fb2fb50662429e83fc70ea3'
FREEZE_DIGEST_SHA256 = 'fa851a1b1426fdcb65a7c39d9d39b8bc8ee3e7b1c1b1939dc0c0529327273619'
SOURCE_PINS_SHA256 = 'd0bb5c5ea881204cc045a3319898ae697df83c7637fbf2516924547759cfb472'
EMPTY_RESULTS_SHA256 = 'ebe019063ad56384fe6030ead5f6a77fa0f1c78d0a2b8e9373d700cf92b57fb5'
EXAMINER_STUB_SHA256 = 'd9f4727d914949b53fcdb3a0e3173ec005f6e14feadabc8ebd1d58b141718b8f'
EXAMINER_STUB_MD_SHA256 = '2785f8122c6d42757035524f885f1f74b296fbaaa47c538def58ff00ed7dda04'
FEE_PIN_SHA256 = '9c0f3554eedc582ed4bed940575bf7ee6c0540ce5134140c5ea19e7c458d2b6a'
ADMIT1_RULING_SHA256 = 'ac7cfe63623ca342ab5b4285ff58382a8138b58fb6cd8e95310a5d30d90304f2'
PANEL_ADMITTED_SHA256 = 'e36de2d1ce6286dff90d25f2fae680170c8a469c443c1beed974ffe80383fba1'
ADDENDUM_SHA256 = '09763030c67df066f2b59346200813e181777670cd46fcee6b8877a6dd74d754'
EVIDENCE_CLASS = 'IN_SAMPLE_DEV'
FIRST_PITCH_SOURCE = 'SCHEDULED_START_PROXY'
PANEL_ADMITTED_AT = '2026-09-25T04:37:47Z'
FEE_TYPE = 'quadratic'
FEE_MULTIPLIER = '0.5'
FEE_LABEL = 'CACHE_NOT_R1P1'
LABEL = 'public_counterparty_realized'
VERDICT_CEILING = 'ITERATE'
EXAMINER_STATUS = 'HOLD_PRE_PR'
EXAMINER_PATH_AFTER_PR = 'READY_NOT_SCORED'
PINNED_PRINTS_N = 11723
EXPECTED_GP0_N = 1865
EXPECTED_GP1_N = 9852
EXPECTED_POST_CLOSE_N = 6
ONE = Decimal('1')
TICK = Decimal('0.01')
PRICE_TOLERANCE = Decimal('1e-9')
SHIFT_30M = timedelta(minutes=30)
EDT = timezone(timedelta(hours=-4))
ADMIT1_WINDOW_START = datetime(2026, 9, 27, 0, 0, tzinfo=timezone.utc)
ADMIT1_WINDOW_END = datetime(2026, 9, 30, 4, 0, tzinfo=timezone.utc)
PANEL_ADMITTED_AT_UTC = datetime(2026, 9, 25, 4, 37, 47, tzinfo=timezone.utc)
CAPTURE_STAMP = re.compile(r'(\d{4})(\d{2})(\d{2})T(\d{2})(\d{2})(\d{2})Z')
RULES_START = re.compile(
    r'originally scheduled for (\w{3}) (\d{1,2}), (\d{4}) at (\d{1,2}):(\d{2}) (AM|PM) EDT'
)
EVENT_TICKER_CODE = re.compile(
    r'^KXMLBSPREAD-(\d{2})([A-Z]{3})(\d{2})(\d{2})(\d{2})[A-Z0-9]+$'
)
MONTHS = {
    'JAN': 1, 'FEB': 2, 'MAR': 3, 'APR': 4, 'MAY': 5, 'JUN': 6,
    'JUL': 7, 'AUG': 8, 'SEP': 9, 'OCT': 10, 'NOV': 11, 'DEC': 12,
}
DECLARED_STARTS = {
    'KXMLBSPREAD-26SEP242140HOUATH': '2026-09-25T01:40:00Z',
    'KXMLBSPREAD-26SEP242140LAASEA': '2026-09-25T01:40:00Z',
    'KXMLBSPREAD-26SEP242210SDLAD': '2026-09-25T02:10:00Z',
}
EXPECTED_PHASE_COUNTS = {
    'KXMLBSPREAD-26SEP242140HOUATH-ATH2': (22, 475, 0),
    'KXMLBSPREAD-26SEP242140HOUATH-HOU2': (498, 2057, 2),
    'KXMLBSPREAD-26SEP242140LAASEA-LAA2': (50, 1054, 1),
    'KXMLBSPREAD-26SEP242140LAASEA-SEA2': (386, 785, 2),
    'KXMLBSPREAD-26SEP242210SDLAD-LAD2': (836, 3308, 0),
    'KXMLBSPREAD-26SEP242210SDLAD-SD2': (73, 2173, 1),
}
NULL_METRIC_KEYS = (
    'maker_gross_roi_delta_GP1_minus_GP0',
    'maker_gross_roi_delta_GP1_minus_GP0_within_FL1',
    'loeo_delta_GP1_minus_GP0',
    'lomo_delta_GP1_minus_GP0',
    'loeo_delta_GP1_minus_GP0_within_FL1',
    'lomo_delta_GP1_minus_GP0_within_FL1',
    'per_market_table',
    'per_event_table',
    'stress_one_tick_worse',
    'stress_start_shift_plus_30m',
    'stress_fees_2x_cache',
    'n_trades_in_scope',
    'excluded_admit1_window_n',
    'excluded_post_close_n',
    'excluded_block_n',
    'excluded_taker_conflict_n',
    'excluded_price_inconsistent_n',
    'excluded_market_result_not_yes_no_n',
    'reading',
)

IN_SCOPE = {
    'KXMLBSPREAD-26SEP242140HOUATH-ATH2': 'KXMLBSPREAD-26SEP242140HOUATH',
    'KXMLBSPREAD-26SEP242140HOUATH-HOU2': 'KXMLBSPREAD-26SEP242140HOUATH',
    'KXMLBSPREAD-26SEP242140LAASEA-LAA2': 'KXMLBSPREAD-26SEP242140LAASEA',
    'KXMLBSPREAD-26SEP242140LAASEA-SEA2': 'KXMLBSPREAD-26SEP242140LAASEA',
    'KXMLBSPREAD-26SEP242210SDLAD-LAD2': 'KXMLBSPREAD-26SEP242210SDLAD',
    'KXMLBSPREAD-26SEP242210SDLAD-SD2': 'KXMLBSPREAD-26SEP242210SDLAD',
}
SEP25_OUT_OF_SCOPE = {
    'KXMLBSPREAD-26SEP251840PITDET-DET2',
    'KXMLBSPREAD-26SEP251840PITDET-PIT2',
    'KXMLBSPREAD-26SEP251840TBPHI-PHI2',
    'KXMLBSPREAD-26SEP251840TBPHI-TB2',
    'KXMLBSPREAD-26SEP251845NYMWSH-NYM2',
    'KXMLBSPREAD-26SEP251845NYMWSH-WSH2',
}
COLLECTOR_PRINTS = {
    'KXMLBSPREAD-26SEP242140HOUATH-ATH2': 497,
    'KXMLBSPREAD-26SEP242140HOUATH-HOU2': 2557,
    'KXMLBSPREAD-26SEP242140LAASEA-LAA2': 1105,
    'KXMLBSPREAD-26SEP242140LAASEA-SEA2': 1173,
    'KXMLBSPREAD-26SEP242210SDLAD-LAD2': 4144,
    'KXMLBSPREAD-26SEP242210SDLAD-SD2': 2247,
}

PINS = ROOT / 'pins'
BUNDLE_NAME = 'Q6S5_KXMLBSPREAD_GAME_PHASE_SETTLED_TAPE_authentic_pins_2026-10-01'
BUNDLE = PINS / BUNDLE_NAME
BUNDLE_TGZ = PINS / (BUNDLE_NAME + '.tgz')
ACCEPT_PATH = PINS / 'CONDUCTOR_ACCEPT_VARIANTS_Q6S5_GAME_PHASE_SETTLED_TAPE_FREEZE_2026-10-01.json'
ADDENDUM_PATH = PINS / 'CONDUCTOR_RULING_Q6S5_FL_BAND_IN_SAMPLE_DEV_LABEL_2026-10-01.json'
PINS_MANIFEST = PINS / 'MANIFEST.sha256'
PIN_MANIFEST_SHA = {
    BUNDLE_TGZ.name: BUNDLE_SHA256,
    ACCEPT_PATH.name: ACCEPT_SHA256,
    ADDENDUM_PATH.name: ADDENDUM_SHA256,
}
PACKET_REL = Path('lab/governance/astra/packets/Q6S5_KXMLBSPREAD_GAME_PHASE_SETTLED_TAPE')
FREEZE_REL = Path(
    'lab/governance/astra/packets/Q6S5_KXMLBSPREAD_GAME_PHASE_SETTLED_TAPE_FREEZE_2026-10-01.md'
)
BAND_REL = Path('lab/governance/astra/packets/r3_p3_fl_maker_taker/bands_registry_10c.json')
SOURCE_PINS_REL = PACKET_REL / 'SOURCE_PINS.json'
FROZEN_EXPERIMENT_REL = PACKET_REL / 'FROZEN_EXPERIMENT.json'
EMPTY_RESULTS_REL = PACKET_REL / 'EMPTY_RESULTS.json'
FREEZE_DIGEST_REL = PACKET_REL / 'Q6S5_KXMLBSPREAD_GAME_PHASE_SETTLED_TAPE_FREEZE_DIGEST_2026-10-01.json'
EXAMINER_STUB_REL = PACKET_REL / (
    'EXAMINER_SCORECARD_STUB_Q6S5_KXMLBSPREAD_GAME_PHASE_SETTLED_TAPE_2026-10-01.json'
)
EXAMINER_STUB_MD_REL = PACKET_REL / (
    'EXAMINER_SCORECARD_STUB_Q6S5_KXMLBSPREAD_GAME_PHASE_SETTLED_TAPE_2026-10-01.md'
)
PACKET_MANIFEST_REL = PACKET_REL / 'MANIFEST.sha256'
FEE_PIN_REL = Path(
    'lab/governance/astra/packets/EXAMINER_FEE_PIN_Q6S5_KXMLBSPREAD_LIVE_SERIES_2026-09-25.json'
)
ADMIT1_RULING_REL = Path(
    'lab/governance/astra/packets/CONDUCTOR_RULING_ADMIT1_OUTAGE_GAP_WEATHER_CARD03_RELAUNCH_2026-09-29.json'
)
PANEL_REL = Path('lab/astra-capture/q6s5-kxmlbspread/panel_admitted.json')
EMPTY_RESULTS = ROOT / 'results' / 'EMPTY_RESULTS.json'
EXAMINER_HOLD = ROOT / 'EXAMINER_HOLD_Q6S5_KXMLBSPREAD_GAME_PHASE_SETTLED_TAPE_PRE_PR_2026-10-01.json'
AUTHORITY = ROOT / 'AUTHORITY_VERIFICATION.json'
GOVERNANCE_PACKET = (
    PARENT / 'lab' / 'governance' / 'astra' / 'packets' / 'Q6S5_KXMLBSPREAD_GAME_PHASE_SETTLED_TAPE'
)
TRADES_ROOT_REL = Path('lab/astra-capture/q6s5-kxmlbspread/trades_fills_2026-09-25')
MARKETS_REL = Path('lab/astra-capture/q6s5-kxmlbspread/measured/raw/markets')
CAPTURE_SQLITE = PARENT / 'lab' / 'astra-capture' / 'prospective' / 'capture.sqlite'
ABSENT_PINS = (
    {
        'key': 'variants_ping_prefix_7af58fa9',
        'path': 'packets/VARIANTS_ACCEPT_PING_Q6S5_KXMLBSPREAD_GAME_PHASE_SETTLED_TAPE_2026-10-01.json',
        'note': 'ACCEPT records prefix 7af58fa9 only. The ping file is not in the bundle and is not invented.',
    },
    {
        'key': 'observed_first_pitch',
        'path': 'packets/OBSERVED_FIRST_PITCH_Q6S5_KXMLBSPREAD_2026-10-01.json',
        'note': 'Actual first pitch is not on disk. SCHEDULED_START_PROXY is the label.',
    },
)


class OrchestratorError(Exception):
    """The settled-tape path refused the input."""


class ManifestShaMismatch(OrchestratorError):
    """A closed-manifest sha256 did not match. The file is not parsed."""


class Admit1WindowRejected(OrchestratorError):
    """A timestamp falls inside the ADMIT-1 exclusion window."""


class Admit1CaptureRefused(OrchestratorError):
    """ADMIT-1 capture.sqlite is not opened."""


class GapBackfillRefused(OrchestratorError):
    """Gap backfill and interpolation are refused."""


class LeeReadyRefused(OrchestratorError):
    """Lee-Ready is refused. Direction is not inferred."""


class NoInvent(OrchestratorError):
    """Fills, PnL, depth, settlement, markets, and missing results are not invented."""


class RebinRefused(OrchestratorError):
    """The R3-P3 10 cent registry is not rebinned."""


class OrthogonalKnobRefused(OrchestratorError):
    """analysis_slice, fill_model, and price_band stay on their own packets."""


class LiveOrderRefused(OrchestratorError):
    """Live orders are refused."""


class LiveHttpRefused(OrchestratorError):
    """Live Kalshi HTTP and any other network read are refused."""


class AdmitPyRefused(OrchestratorError):
    """admit.py is not run."""


class DualCloudRefused(OrchestratorError):
    """A second cloud implement is refused."""


class RetuneRefused(OrchestratorError):
    """Q6-000, Cap-SR, Q6S1, and S1 stay closed."""


class CacheNotLiveR1P1(OrchestratorError):
    """CACHE_NOT_R1P1 is not a live R1-P1 fee claim."""


class KeepRefused(OrchestratorError):
    """This measurement cannot KEEP."""


class ScorecardPromotionRefused(OrchestratorError):
    """results and pnl stay null until Examiner scores."""


class LookaheadRefused(OrchestratorError):
    """The arm uses only the print timestamp and the pinned schedule."""


class ScheduledStartRefused(OrchestratorError):
    """rules_primary is missing the schedule pattern or disagrees with the event ticker."""


class UniverseCapRefused(OrchestratorError):
    """game_phase is the last knob on this three-game universe."""


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, 'rb') as handle:
        for chunk in iter(lambda: handle.read(1 << 16), b''):
            digest.update(chunk)
    return digest.hexdigest()


def assert_pinned_sha(path, expected_sha256):
    """Hash first. A mismatch raises before the caller parses the file."""
    path = Path(path)
    if not path.is_file():
        raise ManifestShaMismatch('missing %s' % path)
    got = sha256_file(path)
    if got != expected_sha256:
        raise ManifestShaMismatch('%s got %s expected %s' % (path, got, expected_sha256))
    return path


def load_pinned_json(path, expected_sha256):
    """Hash first. A mismatch raises before the bytes are parsed."""
    pinned = assert_pinned_sha(path, expected_sha256)
    return json.loads(pinned.read_text(encoding='utf-8'))


def verify_pins_manifest(manifest_path=None):
    """Hash each pins MANIFEST entry before that file is parsed.

    The manifest is the authentic tarball, the Conductor ACCEPT, and the
    inherited IN_SAMPLE_DEV ruling. A tampered byte raises ManifestShaMismatch.
    """
    manifest_path = Path(manifest_path or PINS_MANIFEST)
    if not manifest_path.is_file():
        raise ManifestShaMismatch('missing %s' % manifest_path)
    root = manifest_path.parent
    seen = {}
    for line_no, line in enumerate(manifest_path.read_text(encoding='utf-8').splitlines(), 1):
        if not line.strip() or line.startswith('#'):
            continue
        parts = line.split()
        if len(parts) != 2:
            raise ManifestShaMismatch('pins manifest line %s' % line_no)
        digest, name = parts
        if len(digest) != 64 or any(ch not in '0123456789abcdef' for ch in digest):
            raise ManifestShaMismatch('pins manifest line %s' % line_no)
        assert_pinned_sha(root / name, digest)
        if name in seen:
            raise ManifestShaMismatch('duplicate %s' % name)
        seen[name] = digest
    if seen != PIN_MANIFEST_SHA:
        raise ManifestShaMismatch('pins manifest set')
    accept = load_pinned_json(root / ACCEPT_PATH.name, ACCEPT_SHA256)
    if accept.get('decision') != 'ACCEPT_FREEZE_IMPLEMENT_GO':
        raise ManifestShaMismatch('accept decision')
    if accept.get('freeze_id') != EXPERIMENT_ID:
        raise ManifestShaMismatch('accept freeze')
    ruling_payload = load_pinned_json(root / ADDENDUM_PATH.name, ADDENDUM_SHA256)
    ruling = ruling_payload.get('ruling') if isinstance(ruling_payload, dict) else None
    if not isinstance(ruling, dict) or ruling.get('evidence_class') != EVIDENCE_CLASS:
        raise ManifestShaMismatch('addendum evidence_class')
    if ruling.get('panel_admitted_at') != PANEL_ADMITTED_AT:
        raise ManifestShaMismatch('addendum panel_admitted_at')
    return {'accept': accept, 'ruling': ruling_payload}


def stamp_labels(payload):
    """Labels required on outputs. Does not fill a metric."""
    payload['evidence_class'] = EVIDENCE_CLASS
    payload['family_size'] = FAMILY_SIZE
    payload['family_knobs'] = list(FAMILY_KNOBS)
    payload['hypothesis_generating_only'] = True
    payload['universe_cap_last_knob'] = True
    payload['first_pitch_source'] = FIRST_PITCH_SOURCE
    payload['promote'] = False
    payload['counts_toward_keep'] = False
    payload['verdict_ceiling'] = VERDICT_CEILING
    payload['results'] = None
    payload['pnl'] = None
    return payload


def pre_admitted_at(created_time):
    """True iff created_time is strictly before the panel admitted_at instant."""
    ts = created_time if isinstance(created_time, datetime) else parse_ts(created_time)
    return ts < PANEL_ADMITTED_AT_UTC


def parse_ts(value):
    if isinstance(value, datetime):
        if value.tzinfo is None:
            raise OrchestratorError('timestamp')
        return value.astimezone(timezone.utc)
    if not isinstance(value, str) or not value.endswith('Z') or 'T' not in value:
        raise OrchestratorError('timestamp')
    try:
        parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
    except ValueError as exc:
        raise OrchestratorError('timestamp') from exc
    if parsed.tzinfo is None:
        raise OrchestratorError('timestamp')
    return parsed.astimezone(timezone.utc)


def format_utc(value):
    ts = parse_ts(value).astimezone(timezone.utc)
    if ts.microsecond:
        raise OrchestratorError('timestamp')
    return ts.strftime('%Y-%m-%dT%H:%M:%SZ')


def in_admit1_window(ts):
    """Half-open window [2026-09-27T00:00:00Z, 2026-09-30T04:00:00Z)."""
    if not isinstance(ts, datetime):
        ts = parse_ts(ts)
    return ADMIT1_WINDOW_START <= ts < ADMIT1_WINDOW_END


def captured_utc_from_name(name):
    match = CAPTURE_STAMP.search(str(name))
    if match is None:
        return None
    year, month, day, hour, minute, second = match.groups()
    return '%s-%s-%sT%s:%s:%sZ' % (year, month, day, hour, minute, second)


def _as_decimal(value, name):
    if isinstance(value, bool) or isinstance(value, float):
        raise OrchestratorError(name)
    if isinstance(value, Decimal):
        return value
    if isinstance(value, int) or isinstance(value, str):
        return Decimal(value)
    raise OrchestratorError(name)


def _as_price(value):
    price = _as_decimal(value, 'price')
    if price < 0 or price > 1:
        raise OrchestratorError('price')
    return price


def _hour24(hour, ampm):
    if hour < 1 or hour > 12:
        raise ScheduledStartRefused('hour')
    if ampm == 'AM':
        return 0 if hour == 12 else hour
    if ampm == 'PM':
        return 12 if hour == 12 else hour + 12
    raise ScheduledStartRefused('ampm')


def _et_to_utc(year, month, day, hour, minute):
    if month is None or hour > 23 or minute > 59:
        raise ScheduledStartRefused('clock')
    try:
        et = datetime(year, month, day, hour, minute, tzinfo=EDT)
    except ValueError as exc:
        raise ScheduledStartRefused('clock') from exc
    return et.astimezone(timezone.utc)


def scheduled_start_utc(rules_primary, event_ticker):
    """Parse rules_primary and require equality with the event-ticker ET code.

    A missing pattern or any mismatch is a hard fail. occurrence_datetime,
    expected_expiration_time, and close_time are not inputs.
    """
    if not isinstance(rules_primary, str) or not isinstance(event_ticker, str):
        raise ScheduledStartRefused('missing')
    matches = list(RULES_START.finditer(rules_primary))
    if len(matches) != 1:
        raise ScheduledStartRefused('missing' if len(matches) == 0 else 'mismatch')
    month_name, day_s, year_s, hour_s, minute_s, ampm = matches[0].groups()
    month = MONTHS.get(month_name.upper())
    if month is None:
        raise ScheduledStartRefused('missing')
    rules_et = (
        int(year_s),
        month,
        int(day_s),
        _hour24(int(hour_s), ampm),
        int(minute_s),
    )
    ticker = EVENT_TICKER_CODE.match(event_ticker)
    if ticker is None:
        raise ScheduledStartRefused('mismatch')
    yy, mon, dd, hh, mm = ticker.groups()
    ticker_month = MONTHS.get(mon)
    if ticker_month is None:
        raise ScheduledStartRefused('mismatch')
    ticker_et = (2000 + int(yy), ticker_month, int(dd), int(hh), int(mm))
    if rules_et != ticker_et:
        raise ScheduledStartRefused('mismatch')
    utc = _et_to_utc(*rules_et)
    rendered = format_utc(utc)
    if event_ticker in DECLARED_STARTS and rendered != DECLARED_STARTS[event_ticker]:
        raise ScheduledStartRefused('mismatch')
    return rendered


def use_occurrence_datetime(value=None):
    del value
    raise ScheduledStartRefused('occurrence_datetime')


def use_expected_expiration(value=None):
    del value
    raise ScheduledStartRefused('expected_expiration_time')


def assign_phase(created_time, scheduled_start, close_time):
    """GP0 before the scheduled start, GP1 at or after it and before close.

    The arguments are the print timestamp, the pinned schedule, and close.
    A print at or after close returns None (excluded). This is not a third arm.
    """
    created = parse_ts(created_time)
    start = parse_ts(scheduled_start)
    close = parse_ts(close_time)
    if created >= close:
        return None
    if created < start:
        return Q6S5GP0
    return Q6S5GP1


def bundle_path(rel, bundle=None):
    return Path(bundle or BUNDLE) / rel


def verify_closed_manifest(bundle=None):
    """Read SOURCE_PINS only after its sha matches, then check every input."""
    bundle = Path(bundle or BUNDLE)
    pins = load_pinned_json(bundle / SOURCE_PINS_REL, SOURCE_PINS_SHA256)
    checked = 0
    for group in ('inputs_core', 'inputs_raw', 'inputs_excluded_proof'):
        for rel, digest in pins[group].items():
            if rel.endswith('capture.sqlite') or Path(rel).name == 'capture.sqlite':
                raise Admit1CaptureRefused(rel)
            assert_pinned_sha(bundle / rel, digest)
            checked += 1
    expected = (
        len(pins['inputs_core']) + pins['inputs_raw_n'] + pins['inputs_excluded_proof_n']
    )
    if checked != expected:
        raise ManifestShaMismatch('closed manifest count')
    return pins


_REGISTRY_CACHE = {}


def load_band_registry(bundle=None):
    path = bundle_path(BAND_REL, bundle)
    cached = _REGISTRY_CACHE.get(str(path))
    if cached is not None:
        return cached
    registry = load_pinned_json(path, BAND_REGISTRY_SHA256)
    bands = registry.get('bands')
    if registry.get('registry_id') != 'astra.r3p3.fl_maker_taker.price_bands_10c.v0':
        raise RebinRefused('registry_id')
    if not isinstance(bands, list) or [item.get('band_id') for item in bands] != list(BAND_IDS):
        raise RebinRefused('band_id')
    by_id = {item['band_id']: item for item in bands}
    b02 = by_id['b02']
    b07 = by_id['b07']
    if Decimal(str(b02['price_lo'])) != Decimal('0.2') or b02['lo_inclusive'] is not True:
        raise RebinRefused('fl1 lo')
    if Decimal(str(b07['price_hi'])) != Decimal('0.8') or b07['hi_inclusive'] is not False:
        raise RebinRefused('fl1 hi')
    if tuple(band for band in BAND_IDS if band in FL1_BANDS) != FL1_BANDS:
        raise RebinRefused('fl1')
    _REGISTRY_CACHE[str(path)] = registry
    return registry


def rebin(bands=None):
    del bands
    raise RebinRefused('rebin')


def _band_bounds(band):
    return (
        Decimal(str(band['price_lo'])),
        Decimal(str(band['price_hi'])),
        bool(band['lo_inclusive']),
        bool(band['hi_inclusive']),
    )


def assign_registry_band(price, registry=None):
    """Assign p_taker with the registry lo/hi inclusivity. No other cut."""
    if registry is None:
        registry = load_band_registry()
    price = _as_price(price)
    matched = []
    for band in registry['bands']:
        lo, hi, lo_in, hi_in = _band_bounds(band)
        above_lo = price >= lo if lo_in else price > lo
        below_hi = price <= hi if hi_in else price < hi
        if above_lo and below_hi:
            matched.append(band['band_id'])
    if len(matched) != 1:
        raise RebinRefused('assignment')
    return matched[0]


def in_fl1(price, registry=None):
    """FL1 is registry b02–b07, the mid band [0.20, 0.80). Not a new cut."""
    return assign_registry_band(price, registry) in FL1_BANDS


def set_knob(name):
    if name in ORTHOGONAL_KNOBS:
        raise OrthogonalKnobRefused(name)
    if name != KNOB:
        raise OrchestratorError('knob')
    return KNOB


def live_order(path='/orders'):
    del path
    raise LiveOrderRefused()


def live_http_get(url=None):
    del url
    raise LiveHttpRefused()


def run_admit_py():
    raise AdmitPyRefused()


def dual_cloud():
    raise DualCloudRefused()


def open_fifth_freeze(name=None):
    del name
    raise UniverseCapRefused('last knob on this universe')


def retune(name):
    closed = (
        'q6-000', 'q6_000', 'cap-sr', 'cap_sr', 'q6s1', 's1', 'kxmlbgame',
        'price_band', 'fill_model', 'analysis_slice',
    )
    if str(name).lower() not in closed:
        raise OrchestratorError('retune')
    raise RetuneRefused(str(name))


def claim_keep():
    raise KeepRefused()


def claim_live_r1p1(quote=None):
    del quote
    raise CacheNotLiveR1P1()


def read_admit1_capture(path):
    """Refuse the recorder DB. Existence may be checked. The file is not opened."""
    text = str(path)
    target = Path(text)
    if target.name != 'capture.sqlite' and not text.endswith('capture.sqlite'):
        raise Admit1CaptureRefused(text)
    exists = target.exists()
    raise Admit1CaptureRefused('exists=%s' % exists)


def backfill_gap(payload=None):
    del payload
    raise GapBackfillRefused()


def infer_lee_ready(row=None):
    del row
    raise LeeReadyRefused()


def cache_fee_table():
    """FEE_PIN multiplier on the feebook table. formula_id is not claimed."""
    table = copy.deepcopy(feebook.load_series_table())
    table['default'] = dict(table['default'])
    table['default']['M'] = FEE_MULTIPLIER
    table['formula_id'] = None
    return table


def cache_order_fee(role, contracts, price, times=1):
    """CACHE secondary quote. Resolved maker terms are not asserted."""
    if times not in (1, 2):
        raise OrchestratorError('fee times')
    table = cache_fee_table()
    resolved = feebook.resolve_terms(table, SERIES, role)
    if 'multiplier' not in resolved:
        raise CacheNotLiveR1P1()
    quote = feebook.order_fee(
        role,
        contracts,
        price,
        round_up=True,
        series=SERIES,
        table=table,
    )
    fee = quote['fee'] * Decimal(times)
    labeled = {
        'role': role,
        'fee': fee,
        'fee_type': FEE_TYPE,
        'fee_multiplier': FEE_MULTIPLIER,
        'label': FEE_LABEL,
        'formula_id': None,
        'cache_labeled': True,
        'fee_honest': False,
        'claim_as_live_R1P1': False,
        'resolved_terms_asserted': False,
        'results': None,
        'pnl': None,
    }
    if labeled['formula_id'] is not None or labeled['claim_as_live_R1P1'] is not False:
        raise CacheNotLiveR1P1()
    if labeled['label'] != FEE_LABEL or labeled['fee_honest'] is not False:
        raise CacheNotLiveR1P1()
    return labeled


def _blank_bucket():
    return {
        'return': Decimal('0'),
        'capital': Decimal('0'),
        'taker_return': Decimal('0'),
        'taker_capital': Decimal('0'),
        'fee': Decimal('0'),
        'taker_fee': Decimal('0'),
        'contracts': Decimal('0'),
        'n': 0,
        'markets': set(),
        'events': set(),
    }


def _roi(amount, capital):
    if capital == 0:
        return None
    return amount / capital


def _finalize(bucket, with_fee):
    gross_roi = _roi(bucket['return'], bucket['capital'])
    taker_roi = _roi(bucket['taker_return'], bucket['taker_capital'])
    report = {
        'maker_gross_return_usd': bucket['return'],
        'maker_capital_usd': bucket['capital'],
        'maker_gross_roi': gross_roi,
        'taker_gross_roi': taker_roi,
        'n_trades': bucket['n'],
        'contracts': bucket['contracts'],
        'n_markets': len(bucket['markets']),
        'n_events': len(bucket['events']),
        'maker_net_roi_cache': None,
        'taker_net_roi_cache': None,
        'results': None,
        'pnl': None,
    }
    if with_fee:
        report['maker_net_roi_cache'] = _roi(bucket['return'] - bucket['fee'], bucket['capital'])
        report['taker_net_roi_cache'] = _roi(
            bucket['taker_return'] - bucket['taker_fee'],
            bucket['taker_capital'],
        )
    return report


def _accumulate(rows, one_tick=False, fee_times=0):
    arms = {arm: _blank_bucket() for arm in ARMS}
    for row in rows:
        arm = row['arm']
        if arm not in arms:
            raise OrchestratorError('arm')
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
        taker_return = quantity * (outcome - price)
        taker_capital = quantity * price
        maker_fee = Decimal('0')
        taker_fee = Decimal('0')
        if fee_times:
            maker_fee = cache_order_fee('maker', quantity, ONE - price, times=fee_times)['fee']
            taker_fee = cache_order_fee('taker', quantity, price, times=fee_times)['fee']
        bucket = arms[arm]
        bucket['return'] += maker_return
        bucket['capital'] += maker_capital
        bucket['taker_return'] += taker_return
        bucket['taker_capital'] += taker_capital
        bucket['fee'] += maker_fee
        bucket['taker_fee'] += taker_fee
        bucket['contracts'] += quantity
        bucket['n'] += 1
        bucket['markets'].add(row['ticker'])
        bucket['events'].add(row['event'])
    return arms


def _delta(reports, key):
    left = reports[Q6S5GP1][key]
    right = reports[Q6S5GP0][key]
    if left is None or right is None:
        return None
    return left - right


def _reports(rows, one_tick=False, fee_times=0):
    arms = _accumulate(rows, one_tick=one_tick, fee_times=fee_times)
    return {arm: _finalize(arms[arm], with_fee=bool(fee_times)) for arm in ARMS}


def _check_algebra_row(row, registry):
    if row.get('first_pitch_source') not in (None, FIRST_PITCH_SOURCE):
        raise ScheduledStartRefused('proxy')
    phase = assign_phase(row['created_time'], row['scheduled_start'], row['close_time'])
    if phase != row['arm']:
        raise LookaheadRefused('arm')
    band_id = assign_registry_band(row['p_taker'], registry)
    if row.get('band_id') != band_id:
        raise RebinRefused('row band')
    row['band_id'] = band_id
    row['first_pitch_source'] = FIRST_PITCH_SOURCE


def _fl1_rows(rows):
    return [row for row in rows if row['band_id'] in FL1_BANDS]


def _subset_deltas(rows, key_name):
    seen = []
    for row in rows:
        if row[key_name] not in seen:
            seen.append(row[key_name])
    groups = []
    for held_out in seen:
        kept = [row for row in rows if row[key_name] != held_out]
        groups.append({
            'held_out': held_out,
            'maker_gross_roi_delta_GP1_minus_GP0': _delta(_reports(kept), 'maker_gross_roi'),
            'maker_gross_roi_delta_GP1_minus_GP0_within_FL1': _delta(
                _reports(_fl1_rows(kept)),
                'maker_gross_roi',
            ),
        })
    return groups


def _shift_rows(rows):
    """Recompute membership at scheduled_start + 30 min. Stress only, not an arm."""
    shifted = []
    for row in rows:
        start = parse_ts(row['scheduled_start']) + SHIFT_30M
        phase = assign_phase(row['created_time'], start, row['close_time'])
        if phase is None:
            continue
        moved = dict(row)
        moved['arm'] = phase
        moved['scheduled_start'] = start
        shifted.append(moved)
    return shifted


def _descriptive(rows, key_name):
    seen = []
    for row in rows:
        if row[key_name] not in seen:
            seen.append(row[key_name])
    tables = []
    for key in seen:
        kept = [row for row in rows if row[key_name] == key]
        reports = _reports(kept)
        tables.append({
            'key': key,
            'maker_gross_roi_GP0': reports[Q6S5GP0]['maker_gross_roi'],
            'maker_gross_roi_GP1': reports[Q6S5GP1]['maker_gross_roi'],
            'results': None,
            'pnl': None,
        })
    return tables


def measure_rows(rows):
    """Algebra for caller-supplied rows. Does not write results or pnl.

    The return is public_counterparty_realized. It is not an Examiner score.
    logo is leave-one-game-out, the same cut as loeo (one event per game).
    """
    registry = load_band_registry()
    prepared = []
    for row in rows:
        item = dict(row)
        _check_algebra_row(item, registry)
        prepared.append(item)
    rows = prepared
    gross = _reports(rows, one_tick=False, fee_times=0)
    cached = _reports(rows, one_tick=False, fee_times=1)
    for arm in ARMS:
        gross[arm]['maker_net_roi_cache'] = cached[arm]['maker_net_roi_cache']
        gross[arm]['taker_net_roi_cache'] = cached[arm]['taker_net_roi_cache']
    fl1 = _reports(_fl1_rows(rows))
    ticked = _reports(rows, one_tick=True, fee_times=0)
    ticked_fl1 = _reports(_fl1_rows(rows), one_tick=True, fee_times=0)
    doubled = _reports(rows, one_tick=False, fee_times=2)
    doubled_fl1 = _reports(_fl1_rows(rows), one_tick=False, fee_times=2)
    shifted = _shift_rows(rows)
    logo = _subset_deltas(rows, 'event')
    report = {
        'label': LABEL,
        'knob': KNOB,
        'arms': gross,
        'maker_gross_roi_delta_GP1_minus_GP0': _delta(gross, 'maker_gross_roi'),
        'maker_gross_roi_delta_GP1_minus_GP0_within_FL1': _delta(fl1, 'maker_gross_roi'),
        'logo': logo,
        'loeo': logo,
        'lomo': _subset_deltas(rows, 'ticker'),
        'per_market_table': _descriptive(rows, 'ticker'),
        'per_event_table': _descriptive(rows, 'event'),
        'stress_one_tick_worse': {
            'maker_gross_roi_delta_GP1_minus_GP0': _delta(ticked, 'maker_gross_roi'),
            'maker_gross_roi_delta_GP1_minus_GP0_within_FL1': _delta(ticked_fl1, 'maker_gross_roi'),
            'is_arm': False,
        },
        'stress_start_shift_plus_30m': {
            'maker_gross_roi_delta_GP1_minus_GP0': _delta(_reports(shifted), 'maker_gross_roi'),
            'boundary': 'scheduled_start_utc + 30 min',
            'is_arm': False,
            'first_pitch_source': FIRST_PITCH_SOURCE,
        },
        'stress_fees_2x_cache': {
            'maker_net_roi_cache_delta_GP1_minus_GP0': _delta(doubled, 'maker_net_roi_cache'),
            'maker_net_roi_cache_delta_GP1_minus_GP0_within_FL1': _delta(
                doubled_fl1,
                'maker_net_roi_cache',
            ),
            'label': FEE_LABEL,
            'fee_honest': False,
            'claim_as_live_R1P1': False,
            'is_arm': False,
        },
        'fee_label': FEE_LABEL,
        'fee_honest': False,
        'claim_as_live_R1P1': False,
        'reading': None,
        'arm_names': list(ARMS),
    }
    return stamp_labels(report)


def reading_rule(full_delta, loeo_deltas, secondary_delta=None):
    """Variants-proposed reading. Examiner owns the verdict. Ceiling is ITERATE.

    supports_H1 when the full primary is negative and at least 2 of 3 LOEO
    values are negative. The opposite pair is contradicts_H1. Opposite signs
    between the primary and the within-FL1 secondary cap the reading at
    inconclusive_price_confounded.
    """
    if full_delta is None or len(loeo_deltas) != 3:
        base = 'inconclusive'
    elif any(item is None for item in loeo_deltas):
        base = 'inconclusive'
    else:
        negative = sum(1 for item in loeo_deltas if item < 0)
        nonnegative = sum(1 for item in loeo_deltas if item >= 0)
        if full_delta < 0 and negative >= 2:
            base = 'supports_H1'
        elif full_delta >= 0 and nonnegative >= 2:
            base = 'contradicts_H1'
        else:
            base = 'inconclusive'
    if secondary_delta is not None and full_delta is not None:
        opposed = (full_delta > 0 and secondary_delta < 0) or (
            full_delta < 0 and secondary_delta > 0
        )
        if opposed:
            return 'inconclusive_price_confounded'
    return base


def verdict_for(reading):
    del reading
    return VERDICT_CEILING


def _market_body(market):
    if isinstance(market, dict) and isinstance(market.get('market'), dict):
        return market['market']
    if isinstance(market, dict):
        return market
    raise OrchestratorError('market')


def _exclude(reason, source):
    return {'included': False, 'reason': reason, 'source': source, 'row': None}


def _lee_ready_requested(trade):
    if trade.get('lee_ready') or trade.get('infer_side'):
        return True
    method = trade.get('direction_method')
    if not isinstance(method, str):
        return False
    folded = method.lower().replace('_', '-')
    return 'lee-ready' in folded


def _guard_trade(trade):
    if not isinstance(trade, dict):
        raise OrchestratorError('trade')
    if trade.get('backfill') or trade.get('gap_backfill') or trade.get('interpolate'):
        raise GapBackfillRefused()
    if _lee_ready_requested(trade):
        raise LeeReadyRefused()
    if trade.get('lookahead') or trade.get('use_future_print') or trade.get('use_result_for_phase'):
        raise LookaheadRefused()
    for key in (
        'fill', 'fills', 'pnl', 'astra_pnl', 'simulated_fill', 'depth',
        'invent_settlement', 'invented_market',
    ):
        if key in trade:
            raise NoInvent(key)


def _guard_market_clocks(body, captured_utc):
    for source, raw in (
        ('markets', captured_utc),
        ('close_time', body.get('close_time')),
        ('settlement', body.get('settlement_ts')),
    ):
        if raw is None:
            continue
        if in_admit1_window(raw):
            raise Admit1WindowRejected(source)


def classify_trade(trade, market, captured_utc=None):
    """Include a public print or count an exclusion. Never impute a dropped row.

    Phase uses created_time and the pinned schedule only. A trade-supplied
    start is ignored.
    """
    _guard_trade(trade)
    body = _market_body(market)
    ticker = trade.get('ticker') or body.get('ticker')
    if ticker in SEP25_OUT_OF_SCOPE:
        return _exclude('out_of_scope_sep25', 'market')
    if ticker not in IN_SCOPE:
        return _exclude('out_of_scope', 'market')
    if captured_utc is None:
        captured_utc = body.get('captured_utc')
    _guard_market_clocks(body, captured_utc)
    result = body.get('result')
    if body.get('status') != 'finalized' or result not in ('yes', 'no'):
        return _exclude('market_result_not_yes_no', 'market')
    event = body.get('event_ticker') or IN_SCOPE[ticker]
    if event != IN_SCOPE[ticker]:
        raise ScheduledStartRefused('mismatch')
    start = scheduled_start_utc(body.get('rules_primary'), event)
    created = trade.get('created_time')
    if created is None:
        raise NoInvent('created_time')
    if in_admit1_window(created):
        raise Admit1WindowRejected('trades')
    close_time = body.get('close_time')
    if close_time is None:
        raise NoInvent('close_time')
    phase = assign_phase(created, start, close_time)
    if phase is None:
        return _exclude('post_close', 'trades')
    if 'is_block_trade' not in trade or not isinstance(trade['is_block_trade'], bool):
        raise OrchestratorError('is_block_trade')
    if trade['is_block_trade'] is True:
        return _exclude('block', 'trades')
    side = trade.get('taker_outcome_side')
    if side not in ('yes', 'no'):
        return _exclude('taker_conflict', 'trades')
    book_ok = (side == 'yes' and trade.get('taker_book_side') == 'bid') or (
        side == 'no' and trade.get('taker_book_side') == 'ask'
    )
    if trade.get('taker_side') != side or not book_ok:
        return _exclude('taker_conflict', 'trades')
    yes_price = _as_price(trade.get('yes_price_dollars'))
    no_price = _as_price(trade.get('no_price_dollars'))
    if abs(yes_price + no_price - ONE) > PRICE_TOLERANCE:
        return _exclude('price_inconsistent', 'trades')
    p_taker = yes_price if side == 'yes' else no_price
    if 'count_fp' not in trade:
        raise NoInvent('count_fp')
    quantity = _as_decimal(trade['count_fp'], 'count_fp')
    if quantity <= 0:
        raise OrchestratorError('count_fp')
    band_id = assign_registry_band(p_taker)
    return {
        'included': True,
        'reason': None,
        'source': None,
        'row': {
            'arm': phase,
            'arm_label': ARM_LABELS[phase],
            'band_id': band_id,
            'in_fl1': band_id in FL1_BANDS,
            'p_taker': p_taker,
            'q': quantity,
            'y_s': 1 if result == side else 0,
            'ticker': ticker,
            'event': event,
            'created_time': created,
            'scheduled_start': start,
            'scheduled_start_utc': start,
            'close_time': close_time,
            'pre_admitted_at': pre_admitted_at(created),
            'evidence_class': EVIDENCE_CLASS,
            'family_size': FAMILY_SIZE,
            'hypothesis_generating_only': True,
            'universe_cap_last_knob': True,
            'first_pitch_source': FIRST_PITCH_SOURCE,
            'label': LABEL,
        },
    }


def _trade_pages(bundle, ticker):
    trade_dir = bundle / TRADES_ROOT_REL / 'raw' / 'trades' / ticker
    pages = sorted(trade_dir.glob('page_*.json'))
    return [page for page in pages if not page.name.endswith('.meta.json')]


def _load_market_clocks(bundle):
    """Pinned c0003 market clocks. result, price, and side are not copied."""
    root = bundle / MARKETS_REL
    found = {}
    for path in sorted(root.glob('*.json')):
        if '__c0003__' not in path.name:
            continue
        ticker = path.name.split('__')[-1][:-len('.json')]
        if ticker not in IN_SCOPE:
            continue
        if ticker in found:
            raise NoInvent(ticker)
        payload = json.loads(path.read_text(encoding='utf-8'))
        body = payload.get('market') if isinstance(payload, dict) else None
        if not isinstance(body, dict):
            raise NoInvent('market')
        captured = captured_utc_from_name(path.name)
        clocks = {
            'ticker': body.get('ticker'),
            'event_ticker': body.get('event_ticker'),
            'rules_primary': body.get('rules_primary'),
            'close_time': body.get('close_time'),
            'settlement_ts': body.get('settlement_ts'),
            'captured_utc': captured,
            'path': path,
        }
        if clocks['ticker'] != ticker or clocks['event_ticker'] != IN_SCOPE[ticker]:
            raise ScheduledStartRefused('mismatch')
        _guard_market_clocks(clocks, captured)
        found[ticker] = clocks
    if set(found) != set(IN_SCOPE):
        raise NoInvent('markets')
    by_event = {}
    for ticker, clocks in found.items():
        start = scheduled_start_utc(clocks['rules_primary'], clocks['event_ticker'])
        clocks['scheduled_start_utc'] = start
        prior = by_event.get(clocks['event_ticker'])
        if prior is not None and prior != start:
            raise ScheduledStartRefused('mismatch')
        by_event[clocks['event_ticker']] = start
    if by_event != DECLARED_STARTS:
        raise ScheduledStartRefused('mismatch')
    return found


def inventory_pinned_prints(bundle=None):
    """Count sha-pinned prints. The collector counts are pins, not ROI."""
    bundle = Path(bundle or BUNDLE)
    verify_closed_manifest(bundle)
    per_ticker = {}
    raw_total = 0
    for ticker, expected in COLLECTOR_PRINTS.items():
        meta_rel = TRADES_ROOT_REL / 'per_ticker' / ('%s.json' % ticker)
        meta = json.loads((bundle / meta_rel).read_text(encoding='utf-8'))
        if meta.get('n_trades_total') != expected or meta.get('ticker') != ticker:
            raise ManifestShaMismatch(ticker)
        count = 0
        for page in _trade_pages(bundle, ticker):
            payload = json.loads(page.read_text(encoding='utf-8'))
            count += len(payload['trades'])
        if count != expected:
            raise ManifestShaMismatch(ticker)
        per_ticker[ticker] = count
        raw_total += count
    if raw_total != PINNED_PRINTS_N:
        raise ManifestShaMismatch('print count')
    report = {
        'n_prints': raw_total,
        'per_ticker_n': per_ticker,
        'matches_collector_pin': True,
        'maker_gross_roi_delta_GP1_minus_GP0': None,
        'reading': None,
    }
    return stamp_labels(report)


def timestamp_only_phase_counts(bundle=None):
    """Arm counts from created_time, the pinned schedule, and close_time.

    Counts only. The return has no price, side, result, or ROI.
    """
    bundle = Path(bundle or BUNDLE)
    verify_closed_manifest(bundle)
    markets = _load_market_clocks(bundle)
    totals = {Q6S5GP0: 0, Q6S5GP1: 0, 'post_close': 0}
    per_market = {}
    admission = {
        arm: {'pre_admitted_at': 0, 'post_admitted_at': 0}
        for arm in ARMS
    }
    for ticker in IN_SCOPE:
        clocks = markets[ticker]
        start = clocks['scheduled_start_utc']
        close_time = clocks['close_time']
        counts = [0, 0, 0]
        for page in _trade_pages(bundle, ticker):
            payload = json.loads(page.read_text(encoding='utf-8'))
            for trade in payload['trades']:
                if 'created_time' not in trade:
                    raise NoInvent('created_time')
                created = trade['created_time']
                if in_admit1_window(created):
                    raise Admit1WindowRejected('trades')
                phase = assign_phase(created, start, close_time)
                if phase is None:
                    counts[2] += 1
                    continue
                slot = 0 if phase == Q6S5GP0 else 1
                counts[slot] += 1
                flag = 'pre_admitted_at' if pre_admitted_at(created) else 'post_admitted_at'
                admission[phase][flag] += 1
        if tuple(counts) != EXPECTED_PHASE_COUNTS[ticker]:
            raise ManifestShaMismatch(ticker)
        per_market[ticker] = {
            Q6S5GP0: counts[0],
            Q6S5GP1: counts[1],
            'post_close': counts[2],
        }
        totals[Q6S5GP0] += counts[0]
        totals[Q6S5GP1] += counts[1]
        totals['post_close'] += counts[2]
    if totals[Q6S5GP0] != EXPECTED_GP0_N or totals[Q6S5GP1] != EXPECTED_GP1_N:
        raise ManifestShaMismatch('phase totals')
    if totals['post_close'] != EXPECTED_POST_CLOSE_N:
        raise ManifestShaMismatch('post close')
    if totals[Q6S5GP0] + totals[Q6S5GP1] + totals['post_close'] != PINNED_PRINTS_N:
        raise ManifestShaMismatch('phase sum')
    report = {
        'rule': 'timestamp-only: GP0 created < scheduled start; GP1 start <= created < close; else post-close',
        'panel_admitted_at': PANEL_ADMITTED_AT,
        'admission_rule': 'pre_admitted_at = created_time < 2026-09-25T04:37:47Z',
        'arms': {Q6S5GP0: totals[Q6S5GP0], Q6S5GP1: totals[Q6S5GP1]},
        'post_close': totals['post_close'],
        'per_market': per_market,
        'pre_admitted_at_by_arm': admission,
        'declared_starts_utc': dict(DECLARED_STARTS),
        'counts_only': True,
        'maker_gross_roi_delta_GP1_minus_GP0': None,
        'reading': None,
    }
    return stamp_labels(report)


def output_row_admission_counts(bundle=None):
    """Pre/post admitted_at counts on included output rows.

    Counts only. Outcome, return, price, and PnL are not copied out.
    """
    bundle = Path(bundle or BUNDLE)
    verify_closed_manifest(bundle)
    markets = _load_market_clocks(bundle)
    counts = {
        arm: {'pre_admitted_at': 0, 'post_admitted_at': 0}
        for arm in ARMS
    }
    excluded = {
        'post_close': 0,
        'block': 0,
        'taker_conflict': 0,
        'price_inconsistent': 0,
        'market_result_not_yes_no': 0,
    }
    included_n = {arm: 0 for arm in ARMS}
    for ticker, clocks in markets.items():
        body = json.loads(clocks['path'].read_text(encoding='utf-8'))['market']
        market = {
            'market': {
                'ticker': clocks['ticker'],
                'event_ticker': clocks['event_ticker'],
                'rules_primary': clocks['rules_primary'],
                'close_time': clocks['close_time'],
                'settlement_ts': clocks['settlement_ts'],
                'status': body.get('status'),
                'result': body.get('result'),
                'captured_utc': clocks['captured_utc'],
            }
        }
        for page in _trade_pages(bundle, ticker):
            payload = json.loads(page.read_text(encoding='utf-8'))
            for trade in payload['trades']:
                got = classify_trade(trade, market)
                if got['included'] is not True:
                    reason = got['reason']
                    if reason in excluded:
                        excluded[reason] += 1
                    continue
                row = got['row']
                if row.get('evidence_class') != EVIDENCE_CLASS:
                    raise OrchestratorError('evidence_class')
                if row.get('first_pitch_source') != FIRST_PITCH_SOURCE:
                    raise ScheduledStartRefused('proxy')
                if row.get('family_size') != FAMILY_SIZE:
                    raise OrchestratorError('family_size')
                flag = 'pre_admitted_at' if row['pre_admitted_at'] is True else 'post_admitted_at'
                counts[row['arm']][flag] += 1
                included_n[row['arm']] += 1
    report = {
        'panel_admitted_at': PANEL_ADMITTED_AT,
        'rule': 'pre_admitted_at = created_time < 2026-09-25T04:37:47Z; post_admitted_at is the complement',
        'population': 'included output rows after block, native-side, price, and post-close exclusions',
        'arms': counts,
        'included_n': included_n,
        'excluded_n': excluded,
        'counts_only': True,
        'maker_gross_roi_delta_GP1_minus_GP0': None,
        'reading': None,
    }
    stamped = stamp_labels(report)
    for forbidden in ('y_s', 'result', 'p_taker', 'maker_gross_roi', 'win_rate'):
        if forbidden in stamped:
            raise NoInvent(forbidden)
    return stamped


def _metrics_stay_null(metrics):
    if not isinstance(metrics, dict):
        raise ScorecardPromotionRefused('metrics')
    for key in NULL_METRIC_KEYS:
        if metrics.get(key) is not None:
            raise ScorecardPromotionRefused(key)
    if metrics.get('results') is not None or metrics.get('pnl') is not None:
        raise ScorecardPromotionRefused('results')


def published_scorecard():
    payload = load_pinned_json(EMPTY_RESULTS, EMPTY_RESULTS_SHA256)
    vendored = load_pinned_json(BUNDLE / EMPTY_RESULTS_REL, EMPTY_RESULTS_SHA256)
    if payload != vendored:
        raise ScorecardPromotionRefused('empty results drift')
    _metrics_stay_null(payload.get('metrics'))
    if payload.get('results') is not None or payload.get('pnl') is not None:
        raise ScorecardPromotionRefused('results')
    card = copy.deepcopy(payload)
    _metrics_stay_null(card.get('metrics'))
    stamp_labels(card)
    card['metrics']['evidence_class'] = EVIDENCE_CLASS
    stub = card.get('examiner_scorecard_v1_2', {}).get('scorecard')
    if not isinstance(stub, dict):
        raise ScorecardPromotionRefused('stub')
    _metrics_stay_null(stub.get('metrics'))
    if stub.get('results') is not None or stub.get('pnl') is not None:
        raise ScorecardPromotionRefused('results')
    stub['evidence_class'] = EVIDENCE_CLASS
    stub['family_size'] = FAMILY_SIZE
    stub['family_knobs'] = list(FAMILY_KNOBS)
    stub['hypothesis_generating_only'] = True
    stub['universe_cap_last_knob'] = True
    stub['first_pitch_source'] = FIRST_PITCH_SOURCE
    stub['promote'] = False
    stub['counts_toward_keep'] = False
    stub['verdict_ceiling'] = VERDICT_CEILING
    return card


def write_scorecard(payload, path):
    """Refuse any write that fills results, pnl, or a metric."""
    if not isinstance(payload, dict):
        raise ScorecardPromotionRefused('payload')
    if payload.get('results') is not None or payload.get('pnl') is not None:
        raise ScorecardPromotionRefused('results')
    if payload.get('promote') is True or payload.get('counts_toward_keep') is True:
        raise ScorecardPromotionRefused('promote')
    metrics = payload.get('metrics') or {}
    for key in NULL_METRIC_KEYS:
        if metrics.get(key) is not None:
            raise ScorecardPromotionRefused(key)
    if Path(path).resolve() == EMPTY_RESULTS.resolve():
        raise ScorecardPromotionRefused('frozen empty results')
    raise ScorecardPromotionRefused('score write')


def examiner_status():
    hold = json.loads(EXAMINER_HOLD.read_text(encoding='utf-8'))
    if hold.get('status') != EXAMINER_STATUS or hold.get('scored') is not False:
        raise ScorecardPromotionRefused('examiner')
    if hold.get('results') is not None or hold.get('pnl') is not None:
        raise ScorecardPromotionRefused('examiner')
    if hold.get('family_size') != FAMILY_SIZE:
        raise ScorecardPromotionRefused('family_size')
    if hold.get('first_pitch_source') != FIRST_PITCH_SOURCE:
        raise ScorecardPromotionRefused('proxy')
    if hold.get('evidence_class') != EVIDENCE_CLASS:
        raise ScorecardPromotionRefused('evidence_class')
    return hold


def digest_status():
    rows = (
        ('accept', ACCEPT_PATH, ACCEPT_SHA256),
        ('freeze_md', BUNDLE / FREEZE_REL, FREEZE_SHA256),
        ('freeze_md_copy', BUNDLE / PACKET_REL / FREEZE_REL.name, FREEZE_SHA256),
        ('frozen_experiment', BUNDLE / FROZEN_EXPERIMENT_REL, FROZEN_EXPERIMENT_SHA256),
        ('freeze_digest', BUNDLE / FREEZE_DIGEST_REL, FREEZE_DIGEST_SHA256),
        ('source_pins', BUNDLE / SOURCE_PINS_REL, SOURCE_PINS_SHA256),
        ('empty_results', BUNDLE / EMPTY_RESULTS_REL, EMPTY_RESULTS_SHA256),
        ('empty_results_lab', EMPTY_RESULTS, EMPTY_RESULTS_SHA256),
        ('examiner_stub', BUNDLE / EXAMINER_STUB_REL, EXAMINER_STUB_SHA256),
        ('examiner_stub_md', BUNDLE / EXAMINER_STUB_MD_REL, EXAMINER_STUB_MD_SHA256),
        ('packet_manifest', BUNDLE / PACKET_MANIFEST_REL, PACKET_MANIFEST_SHA256),
        ('band_registry', BUNDLE / BAND_REL, BAND_REGISTRY_SHA256),
        ('fee_pin', BUNDLE / FEE_PIN_REL, FEE_PIN_SHA256),
        ('admit1_ruling', BUNDLE / ADMIT1_RULING_REL, ADMIT1_RULING_SHA256),
        ('panel_admitted', BUNDLE / PANEL_REL, PANEL_ADMITTED_SHA256),
        ('authentic_bundle', BUNDLE_TGZ, BUNDLE_SHA256),
        ('in_sample_dev_addendum', ADDENDUM_PATH, ADDENDUM_SHA256),
    )
    present = []
    missing = []
    mismatch = []
    for key, path, expected in rows:
        if not Path(path).is_file():
            missing.append(key)
            continue
        got = sha256_file(path)
        if got != expected:
            mismatch.append(key)
        present.append({'key': key, 'sha256': got, 'match': got == expected})
    absent = []
    for item in ABSENT_PINS:
        candidate = PARENT / item['path']
        absent.append({
            'key': item['key'],
            'present': candidate.is_file(),
            'invented': False,
        })
    claimed = not missing and not mismatch and all(not item['present'] for item in absent)
    claimed = claimed and not CAPTURE_SQLITE.exists() and not GOVERNANCE_PACKET.exists()
    try:
        verify_pins_manifest()
    except ManifestShaMismatch:
        claimed = False
        mismatch.append('pins_manifest')
    report = {
        'digest_all_match_claimed': claimed,
        'present': present,
        'missing': missing,
        'mismatch': mismatch,
        'absent_not_invented': absent,
    }
    return stamp_labels(report)


def conduct():
    """Pin check, timestamp counts, and a null scorecard. Does not score ROI."""
    verify_pins_manifest()
    inventory = inventory_pinned_prints()
    phases = timestamp_only_phase_counts()
    card = published_scorecard()
    hold = examiner_status()
    digest = digest_status()
    if inventory['results'] is not None or inventory['pnl'] is not None:
        raise ScorecardPromotionRefused('inventory')
    if phases['maker_gross_roi_delta_GP1_minus_GP0'] is not None:
        raise ScorecardPromotionRefused('primary')
    if digest['digest_all_match_claimed'] is not True:
        raise ManifestShaMismatch('digest')
    report = {
        'experiment_id': EXPERIMENT_ID,
        'knob': KNOB,
        'arms': list(ARMS),
        'n_prints_pinned': inventory['n_prints'],
        'timestamp_only_arms': phases['arms'],
        'post_close': phases['post_close'],
        'pre_admitted_at_by_arm': phases['pre_admitted_at_by_arm'],
        'examiner_status': hold['status'],
        'examiner_path_after_pr': hold['examiner_path_after_pr'],
        'scored': False,
        'fee_label': FEE_LABEL,
        'maker_gross_roi_delta_GP1_minus_GP0': None,
        'maker_gross_roi_delta_GP1_minus_GP0_within_FL1': None,
        'reading': None,
        'digest_all_match_claimed': True,
        'scorecard_evidence_class': card['evidence_class'],
        'scorecard_family_size': card['family_size'],
        'scorecard_first_pitch_source': card['first_pitch_source'],
        'live_gets': 0,
        'orders': 0,
        'scorecard_results': card['results'],
        'scorecard_pnl': card['pnl'],
    }
    return stamp_labels(report)
