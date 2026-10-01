"""Q6S5 KXMLBSPREAD FL-band settled-tape measurement path.

One knob: price_band on the taker-purchased side p_taker.
Arms are Q6S5FL0 longshot [0.00, 0.20), Q6S5FL1 mid [0.20, 0.80),
and Q6S5FL2 favorite [0.80, 1.00], using R3-P3 registry bands b00–b09.

Observations are public prints labeled public_counterparty_realized.
This module does not place orders, does not run admit.py, does not open
ADMIT-1 capture.sqlite, does not rebin the registry, and does not write
results or pnl.
"""
import copy
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PARENT = ROOT.parent
FEEBOOK_ROOT = PARENT / 'kalshi_feebook_lab_20260922'
if str(FEEBOOK_ROOT) not in sys.path:
    sys.path.insert(0, str(FEEBOOK_ROOT))
import feebook  # noqa: E402


LAB_DIRECTORY = 'kalshi_q6s5_kxmlbspread_fl_band_settled_tape_lab_20260929'
EXPERIMENT_ID = 'Q6S5-KXMLBSPREAD-FL-BAND-SETTLED-TAPE'
PACKET_ID = 'Q6S5-KXMLBSPREAD-FEEQUEUE-HARNESS'
FEATURE_FAMILY = 'settled_tape_fl_band'
SERIES = 'KXMLBSPREAD'
KNOB = 'price_band'
ORTHOGONAL_KNOBS = ('analysis_slice', 'fill_model')
Q6S5FL0 = 'Q6S5FL0'
Q6S5FL1 = 'Q6S5FL1'
Q6S5FL2 = 'Q6S5FL2'
ARMS = (Q6S5FL0, Q6S5FL1, Q6S5FL2)
ARM_BANDS = {
    Q6S5FL0: ('b00', 'b01'),
    Q6S5FL1: ('b02', 'b03', 'b04', 'b05', 'b06', 'b07'),
    Q6S5FL2: ('b08', 'b09'),
}
BAND_IDS = tuple(band for bands in ARM_BANDS.values() for band in bands)
FEEBOOK_COMMIT = '22371178cb2663250b4762f328069571c48cb551'
RAILS_COMMIT = '6a28e0d6254327ea4e6451c781bec56215ac6cac'
ACCEPT_SHA256 = '8e4fbac7d0426bc67c1f53fb8057a382fe46da738bd701cb970a9812a6dc2a3b'
FREEZE_SHA256 = 'fb6540f52ed5f819ccf6e80bf0cf7eb6d951e065416b9d550fead0c6d06043fa'
BUNDLE_SHA256 = '63b5d981bc06f684eebb69a8ac29394534f8ae52c101f3018557544f14e29857'
BAND_REGISTRY_SHA256 = '0860cbe28d28ecc6142ddf6f1ebb67792084264ed82e0b4d868c3b3138ea5312'
FROZEN_EXPERIMENT_SHA256 = '66819a4144ab0ed16fa73295357aebe5c200dee7d7ca393296d80965313f86f4'
FREEZE_DIGEST_SHA256 = '5f964e12cf02cfd9e45d701e34d40769ef0ed92db2bbfd133a1fd59408703213'
SOURCE_PINS_SHA256 = 'ab8ab6a7570da5099dffe001b92c07cc68bbf9efba2729407763a84d5485da0b'
EMPTY_RESULTS_SHA256 = 'dab3414d2a26205cff5667f8e4952f4121aed98f87f5814bd8627c64e3bfbc12'
EXAMINER_STUB_SHA256 = 'fb01725b1212123fe3f9ffeeedd7c46a3e2404114ef1393381765953cd07f1f3'
FEE_PIN_SHA256 = '9c0f3554eedc582ed4bed940575bf7ee6c0540ce5134140c5ea19e7c458d2b6a'
ADMIT1_RULING_SHA256 = 'ac7cfe63623ca342ab5b4285ff58382a8138b58fb6cd8e95310a5d30d90304f2'
FEE_TYPE = 'quadratic'
FEE_MULTIPLIER = '0.5'
FEE_LABEL = 'CACHE_NOT_R1P1'
LABEL = 'public_counterparty_realized'
VERDICT_CEILING = 'ITERATE'
EXAMINER_STATUS = 'HOLD_PRE_PR'
EXAMINER_PATH_AFTER_PR = 'READY_NOT_SCORED'
PINNED_PRINTS_N = 11723
ONE = Decimal('1')
TICK = Decimal('0.01')
PRICE_TOLERANCE = Decimal('1e-9')
ADMIT1_WINDOW_START = datetime(2026, 9, 27, 0, 0, tzinfo=timezone.utc)
ADMIT1_WINDOW_END = datetime(2026, 9, 30, 4, 0, tzinfo=timezone.utc)
CAPTURE_STAMP = re.compile(r'(\d{4})(\d{2})(\d{2})T(\d{2})(\d{2})(\d{2})Z')

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
BUNDLE = PINS / 'Q6S5_KXMLBSPREAD_FL_BAND_SETTLED_TAPE_authentic_pins_2026-09-29'
BUNDLE_TGZ = PINS / 'Q6S5_KXMLBSPREAD_FL_BAND_SETTLED_TAPE_authentic_pins_2026-09-29.tgz'
ACCEPT_PATH = PINS / 'CONDUCTOR_ACCEPT_VARIANTS_Q6S5_FL_BAND_SETTLED_TAPE_FREEZE_2026-10-01.json'
PACKET_REL = Path('lab/governance/astra/packets/Q6S5_KXMLBSPREAD_FL_BAND_SETTLED_TAPE')
FREEZE_REL = Path('lab/governance/astra/packets/Q6S5_KXMLBSPREAD_FL_BAND_SETTLED_TAPE_FREEZE_2026-09-29.md')
BAND_REL = Path('lab/governance/astra/packets/r3_p3_fl_maker_taker/bands_registry_10c.json')
SOURCE_PINS_REL = PACKET_REL / 'SOURCE_PINS.json'
FROZEN_EXPERIMENT_REL = PACKET_REL / 'FROZEN_EXPERIMENT.json'
EMPTY_RESULTS_REL = PACKET_REL / 'EMPTY_RESULTS.json'
FREEZE_DIGEST_REL = PACKET_REL / 'Q6S5_KXMLBSPREAD_FL_BAND_SETTLED_TAPE_FREEZE_DIGEST_2026-09-29.json'
EXAMINER_STUB_REL = PACKET_REL / 'EXAMINER_SCORECARD_STUB_Q6S5_KXMLBSPREAD_FL_BAND_SETTLED_TAPE_2026-09-29.json'
FEE_PIN_REL = Path('lab/governance/astra/packets/EXAMINER_FEE_PIN_Q6S5_KXMLBSPREAD_LIVE_SERIES_2026-09-25.json')
ADMIT1_RULING_REL = Path(
    'lab/governance/astra/packets/CONDUCTOR_RULING_ADMIT1_OUTAGE_GAP_WEATHER_CARD03_RELAUNCH_2026-09-29.json'
)
EMPTY_RESULTS = ROOT / 'results' / 'EMPTY_RESULTS.json'
EXAMINER_HOLD = ROOT / 'EXAMINER_HOLD_Q6S5_KXMLBSPREAD_FL_BAND_SETTLED_TAPE_PRE_PR_2026-10-01.json'
AUTHORITY = ROOT / 'AUTHORITY_VERIFICATION.json'
GOVERNANCE_PACKET = (
    PARENT / 'lab' / 'governance' / 'astra' / 'packets' / 'Q6S5_KXMLBSPREAD_FL_BAND_SETTLED_TAPE'
)
TRADES_ROOT_REL = Path('lab/astra-capture/q6s5-kxmlbspread/trades_fills_2026-09-25')
ABSENT_PINS = (
    {
        'key': 'variants_accept_ping',
        'path': 'packets/VARIANTS_ACCEPT_PING_Q6S5_KXMLBSPREAD_FL_BAND_SETTLED_TAPE_2026-09-29.json',
        'sha256': '32b1d5f2637e8f7b864dc43b53fffce7fdfde799ec05d295f38549caeedb0060',
    },
    {
        'key': 'variants_archivist_ping',
        'path': 'packets/VARIANTS_ARCHIVIST_REGISTRY_PING_Q6S5_KXMLBSPREAD_FL_BAND_SETTLED_TAPE_2026-09-29.json',
        'sha256': 'eba1260f1ab901a223f3f0b5feb1ff6f023d9f8870c1e69e16007e93e12b3a40',
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
    """Fills, PnL, depth, settlement, and missing results are not invented."""


class RebinRefused(OrchestratorError):
    """The R3-P3 10 cent registry is not rebinned."""


class OrthogonalKnobRefused(OrchestratorError):
    """analysis_slice and fill_model stay on their own packets."""


class LiveOrderRefused(OrchestratorError):
    """Live orders are refused."""


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
    """Band assignment uses only the print's own price."""


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


def parse_ts(value):
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
    if checked != len(pins['inputs_core']) + pins['inputs_raw_n'] + pins['inputs_excluded_proof_n']:
        raise ManifestShaMismatch('closed manifest count')
    return pins


def load_band_registry(bundle=None):
    registry = load_pinned_json(bundle_path(BAND_REL, bundle), BAND_REGISTRY_SHA256)
    bands = registry.get('bands')
    if registry.get('registry_id') != 'astra.r3p3.fl_maker_taker.price_bands_10c.v0':
        raise RebinRefused('registry_id')
    if not isinstance(bands, list) or [item.get('band_id') for item in bands] != list(BAND_IDS):
        raise RebinRefused('band_id')
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


def arm_for_band(band_id):
    for arm, bands in ARM_BANDS.items():
        if band_id in bands:
            return arm
    raise RebinRefused(band_id)


def assign_arm(price, registry=None):
    band_id = assign_registry_band(price, registry)
    return arm_for_band(band_id), band_id


def set_knob(name):
    if name in ORTHOGONAL_KNOBS:
        raise OrthogonalKnobRefused(name)
    if name != KNOB:
        raise OrchestratorError('knob')
    return KNOB


def live_order(path='/orders'):
    del path
    raise LiveOrderRefused()


def run_admit_py():
    raise AdmitPyRefused()


def dual_cloud():
    raise DualCloudRefused()


def retune(name):
    closed = ('q6-000', 'q6_000', 'cap-sr', 'cap_sr', 'q6s1', 's1', 'kxmlbgame')
    if str(name).lower() not in closed:
        raise OrchestratorError('retune')
    raise RetuneRefused(str(name))


def claim_keep():
    raise KeepRefused()


def claim_live_r1p1(quote=None):
    del quote
    raise CacheNotLiveR1P1()


def read_admit1_capture(path):
    """Refuse the recorder DB. The file is not opened."""
    text = str(path)
    if Path(text).name != 'capture.sqlite' and not text.endswith('capture.sqlite'):
        raise Admit1CaptureRefused(text)
    raise Admit1CaptureRefused(text)


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
    """CACHE secondary quote. The feebook algebra id is not an R1-P1 claim."""
    if times not in (1, 2):
        raise OrchestratorError('fee times')
    quote = feebook.order_fee(
        role,
        contracts,
        price,
        round_up=True,
        series=SERIES,
        table=cache_fee_table(),
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
    bands = {band_id: _blank_bucket() for band_id in BAND_IDS}
    for row in rows:
        arm = row['arm']
        band_id = row['band_id']
        if arm not in arms or band_id not in ARM_BANDS[arm]:
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
        taker_return = quantity * (outcome - price)
        taker_capital = quantity * price
        maker_fee = Decimal('0')
        taker_fee = Decimal('0')
        if fee_times:
            maker_fee = cache_order_fee('maker', quantity, ONE - price, times=fee_times)['fee']
            taker_fee = cache_order_fee('taker', quantity, price, times=fee_times)['fee']
        for bucket in (arms[arm], bands[band_id]):
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
    return arms, bands


def _delta(reports, left, right, key):
    left_value = reports[left][key]
    right_value = reports[right][key]
    if left_value is None or right_value is None:
        return None
    return left_value - right_value


def _subset_deltas(rows, key_name, one_tick=False, fee_times=0):
    groups = []
    seen = []
    for row in rows:
        if row[key_name] not in seen:
            seen.append(row[key_name])
    for held_out in seen:
        kept = [row for row in rows if row[key_name] != held_out]
        reports, _bands = _accumulate(kept, one_tick=one_tick, fee_times=fee_times)
        finalized = {arm: _finalize(reports[arm], with_fee=bool(fee_times)) for arm in ARMS}
        groups.append({
            'held_out': held_out,
            'maker_gross_roi_delta_FL0_minus_FL1': _delta(
                finalized, Q6S5FL0, Q6S5FL1, 'maker_gross_roi',
            ),
            'maker_gross_roi_delta_FL2_minus_FL1': _delta(
                finalized, Q6S5FL2, Q6S5FL1, 'maker_gross_roi',
            ),
        })
    return groups


def measure_rows(rows):
    """Algebra for caller-supplied rows. Does not write results or pnl.

    The return is public_counterparty_realized. It is not an Examiner score.
    """
    gross_arms, gross_bands = _accumulate(rows, one_tick=False, fee_times=0)
    cache_arms, _cache_bands = _accumulate(rows, one_tick=False, fee_times=1)
    tick_arms, _tick_bands = _accumulate(rows, one_tick=True, fee_times=0)
    fee2_arms, _fee2_bands = _accumulate(rows, one_tick=False, fee_times=2)
    arms = {arm: _finalize(gross_arms[arm], with_fee=False) for arm in ARMS}
    cached = {arm: _finalize(cache_arms[arm], with_fee=True) for arm in ARMS}
    ticked = {arm: _finalize(tick_arms[arm], with_fee=False) for arm in ARMS}
    doubled = {arm: _finalize(fee2_arms[arm], with_fee=True) for arm in ARMS}
    for arm in ARMS:
        arms[arm]['maker_net_roi_cache'] = cached[arm]['maker_net_roi_cache']
        arms[arm]['taker_net_roi_cache'] = cached[arm]['taker_net_roi_cache']
    bands = {band_id: _finalize(gross_bands[band_id], with_fee=False) for band_id in BAND_IDS}
    return {
        'label': LABEL,
        'knob': KNOB,
        'results': None,
        'pnl': None,
        'promote': False,
        'counts_toward_keep': False,
        'verdict_ceiling': VERDICT_CEILING,
        'fee_label': FEE_LABEL,
        'fee_honest': False,
        'claim_as_live_R1P1': False,
        'arms': arms,
        'maker_gross_roi_by_registry_band': {
            band_id: bands[band_id]['maker_gross_roi'] for band_id in BAND_IDS
        },
        'maker_gross_roi_delta_FL0_minus_FL1': _delta(arms, Q6S5FL0, Q6S5FL1, 'maker_gross_roi'),
        'maker_gross_roi_delta_FL2_minus_FL1': _delta(arms, Q6S5FL2, Q6S5FL1, 'maker_gross_roi'),
        'loeo': _subset_deltas(rows, 'event'),
        'lomo': _subset_deltas(rows, 'ticker'),
        'stress_one_tick_worse': {
            'maker_gross_roi_delta_FL0_minus_FL1': _delta(ticked, Q6S5FL0, Q6S5FL1, 'maker_gross_roi'),
            'maker_gross_roi_delta_FL2_minus_FL1': _delta(ticked, Q6S5FL2, Q6S5FL1, 'maker_gross_roi'),
        },
        'stress_fees_2x_cache': {
            'maker_net_roi_cache_delta_FL0_minus_FL1': _delta(
                doubled, Q6S5FL0, Q6S5FL1, 'maker_net_roi_cache',
            ),
            'maker_net_roi_cache_delta_FL2_minus_FL1': _delta(
                doubled, Q6S5FL2, Q6S5FL1, 'maker_net_roi_cache',
            ),
            'label': FEE_LABEL,
            'fee_honest': False,
            'claim_as_live_R1P1': False,
        },
        'reading': None,
    }


def reading_rule(full_delta, loeo_deltas):
    """Variants-proposed reading. Examiner owns the verdict. Ceiling is ITERATE."""
    if full_delta is None or len(loeo_deltas) != 3:
        return 'inconclusive'
    if any(item is None for item in loeo_deltas):
        return 'inconclusive'
    positive = sum(1 for item in loeo_deltas if item > 0)
    nonpositive = sum(1 for item in loeo_deltas if item <= 0)
    if full_delta > 0 and positive >= 2:
        return 'supports_H1'
    if full_delta <= 0 and nonpositive >= 2:
        return 'contradicts_H1'
    return 'inconclusive'


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
    if trade.get('lookahead') or trade.get('use_future_print'):
        raise LookaheadRefused()
    for key in ('fill', 'fills', 'pnl', 'astra_pnl', 'simulated_fill', 'depth', 'invent_settlement'):
        if key in trade:
            raise NoInvent(key)


def classify_trade(trade, market, captured_utc=None):
    """Include a public print or count an exclusion. Never impute a dropped row."""
    _guard_trade(trade)
    body = _market_body(market)
    ticker = trade.get('ticker') or body.get('ticker')
    if ticker in SEP25_OUT_OF_SCOPE:
        return _exclude('out_of_scope_sep25', 'market')
    if ticker not in IN_SCOPE:
        return _exclude('out_of_scope', 'market')
    if captured_utc is None:
        captured_utc = body.get('captured_utc')
    for source, raw in (
        ('markets', captured_utc),
        ('close_time', body.get('close_time')),
        ('settlement', body.get('settlement_ts')),
    ):
        if raw is None:
            continue
        if in_admit1_window(raw):
            raise Admit1WindowRejected(source)
    result = body.get('result')
    if body.get('status') != 'finalized' or result not in ('yes', 'no'):
        return _exclude('market_result_not_yes_no', 'market')
    created = trade.get('created_time')
    if created is None:
        raise NoInvent('created_time')
    if in_admit1_window(created):
        raise Admit1WindowRejected('trades')
    close_time = body.get('close_time')
    if close_time is None:
        raise NoInvent('close_time')
    if parse_ts(created) >= parse_ts(close_time):
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
    arm, band_id = assign_arm(p_taker)
    if 'count_fp' not in trade:
        raise NoInvent('count_fp')
    quantity = _as_decimal(trade['count_fp'], 'count_fp')
    if quantity <= 0:
        raise OrchestratorError('count_fp')
    return {
        'included': True,
        'reason': None,
        'source': None,
        'row': {
            'arm': arm,
            'band_id': band_id,
            'p_taker': p_taker,
            'q': quantity,
            'y_s': 1 if result == side else 0,
            'ticker': ticker,
            'event': IN_SCOPE[ticker],
            'created_time': created,
            'label': LABEL,
        },
    }


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
        pages = sorted((bundle / TRADES_ROOT_REL / 'raw' / 'trades' / ticker).glob('page_*.json'))
        pages = [page for page in pages if not page.name.endswith('.meta.json')]
        count = 0
        for page in pages:
            payload = json.loads(page.read_text(encoding='utf-8'))
            count += len(payload['trades'])
        if count != expected:
            raise ManifestShaMismatch(ticker)
        per_ticker[ticker] = count
        raw_total += count
    if raw_total != PINNED_PRINTS_N:
        raise ManifestShaMismatch('print count')
    return {
        'n_prints': raw_total,
        'per_ticker_n': per_ticker,
        'matches_collector_pin': True,
        'results': None,
        'pnl': None,
        'maker_gross_roi_delta_FL0_minus_FL1': None,
        'reading': None,
    }


def published_scorecard():
    payload = load_pinned_json(EMPTY_RESULTS, EMPTY_RESULTS_SHA256)
    vendored = load_pinned_json(BUNDLE / EMPTY_RESULTS_REL, EMPTY_RESULTS_SHA256)
    if payload != vendored:
        raise ScorecardPromotionRefused('empty results drift')
    if payload.get('results') is not None or payload.get('pnl') is not None:
        raise ScorecardPromotionRefused('results')
    if payload['metrics']['reading'] is not None:
        raise ScorecardPromotionRefused('reading')
    if payload['metrics']['maker_gross_roi_delta_FL0_minus_FL1'] is not None:
        raise ScorecardPromotionRefused('primary')
    return payload


def write_scorecard(payload, path):
    """Refuse any write that fills results, pnl, or the primary delta."""
    if not isinstance(payload, dict):
        raise ScorecardPromotionRefused('payload')
    if payload.get('results') is not None or payload.get('pnl') is not None:
        raise ScorecardPromotionRefused('results')
    metrics = payload.get('metrics') or {}
    if metrics.get('maker_gross_roi_delta_FL0_minus_FL1') is not None:
        raise ScorecardPromotionRefused('primary')
    if metrics.get('reading') is not None:
        raise ScorecardPromotionRefused('reading')
    if Path(path).resolve() == EMPTY_RESULTS.resolve():
        raise ScorecardPromotionRefused('frozen empty results')
    raise ScorecardPromotionRefused('score write')


def examiner_status():
    hold = json.loads(EXAMINER_HOLD.read_text(encoding='utf-8'))
    if hold.get('status') != EXAMINER_STATUS or hold.get('scored') is not False:
        raise ScorecardPromotionRefused('examiner')
    if hold.get('results') is not None or hold.get('pnl') is not None:
        raise ScorecardPromotionRefused('examiner')
    return hold


def digest_status():
    rows = (
        ('accept', ACCEPT_PATH, ACCEPT_SHA256),
        ('freeze_md', BUNDLE / FREEZE_REL, FREEZE_SHA256),
        ('frozen_experiment', BUNDLE / FROZEN_EXPERIMENT_REL, FROZEN_EXPERIMENT_SHA256),
        ('freeze_digest', BUNDLE / FREEZE_DIGEST_REL, FREEZE_DIGEST_SHA256),
        ('source_pins', BUNDLE / SOURCE_PINS_REL, SOURCE_PINS_SHA256),
        ('empty_results', BUNDLE / EMPTY_RESULTS_REL, EMPTY_RESULTS_SHA256),
        ('empty_results_lab', EMPTY_RESULTS, EMPTY_RESULTS_SHA256),
        ('examiner_stub', BUNDLE / EXAMINER_STUB_REL, EXAMINER_STUB_SHA256),
        ('band_registry', BUNDLE / BAND_REL, BAND_REGISTRY_SHA256),
        ('fee_pin', BUNDLE / FEE_PIN_REL, FEE_PIN_SHA256),
        ('admit1_ruling', BUNDLE / ADMIT1_RULING_REL, ADMIT1_RULING_SHA256),
        ('authentic_bundle', BUNDLE_TGZ, BUNDLE_SHA256),
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
    capture = PARENT / 'lab' / 'astra-capture' / 'prospective' / 'capture.sqlite'
    absent = []
    for item in ABSENT_PINS:
        candidate = PARENT / item['path']
        absent.append({
            'key': item['key'],
            'present': candidate.is_file(),
            'invented': False,
        })
    claimed = not missing and not mismatch and all(not item['present'] for item in absent)
    claimed = claimed and not capture.exists() and not GOVERNANCE_PACKET.exists()
    return {
        'digest_all_match_claimed': claimed,
        'present': present,
        'missing': missing,
        'mismatch': mismatch,
        'absent_not_invented': absent,
        'results': None,
        'pnl': None,
    }


def conduct():
    """Pin check and null scorecard. Does not join the tape to settlement ROI."""
    inventory = inventory_pinned_prints()
    card = published_scorecard()
    hold = examiner_status()
    digest = digest_status()
    if inventory['results'] is not None or inventory['pnl'] is not None:
        raise ScorecardPromotionRefused('inventory')
    if digest['digest_all_match_claimed'] is not True:
        raise ManifestShaMismatch('digest')
    return {
        'experiment_id': EXPERIMENT_ID,
        'knob': KNOB,
        'arms': list(ARMS),
        'n_prints_pinned': inventory['n_prints'],
        'examiner_status': hold['status'],
        'examiner_path_after_pr': hold['examiner_path_after_pr'],
        'scored': False,
        'promote': False,
        'counts_toward_keep': False,
        'verdict_ceiling': VERDICT_CEILING,
        'fee_label': FEE_LABEL,
        'results': None,
        'pnl': None,
        'maker_gross_roi_delta_FL0_minus_FL1': None,
        'reading': None,
        'digest_all_match_claimed': True,
        'live_gets': 0,
        'orders': 0,
        'scorecard_results': card['results'],
        'scorecard_pnl': card['pnl'],
    }
