"""R3-P3 favorite-longshot maker/taker scaffold.

Taker side comes from native public taker_* fields. Fees come from the
imported R1-P1 feebook. Bands come from the pinned 10-cent registry.
Mincer-Zarnowitz and band ROI stay null: the clock refused admit and
settled N is 0. This module does not place live orders.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PARENT = ROOT.parent
FEEBOOK_DIR = PARENT / 'kalshi_feebook_lab_20260922'
if str(FEEBOOK_DIR) not in sys.path:
    sys.path.insert(0, str(FEEBOOK_DIR))

import feebook

PACKET_ID = 'R3-P3-FL-MAKER-TAKER'
EXPERIMENT_ID = 'r3_p3_fl_maker_taker_20260922'
PANEL_VERSION = '2026-09-22.r3-p3-fl-maker-taker-v0'
BANDS_REGISTRY_ID = 'astra.r3p3.fl_maker_taker.price_bands_10c.v0'
FEEBOOK_COMMIT = '22371178cb2663250b4762f328069571c48cb551'
FEEBOOK_DIRECTORY = 'kalshi_feebook_lab_20260922'
COLLECTOR_STATUS = 'READY'
CLOCK_ADMIT = 'REFUSED'
SETTLED_N = 0
EXAMINER_STATUS = 'NOT_NOW'
LEE_READY = False
LIVE_ORDERS = False
SIGNAL_RETUNE = False
Q6_000_RETUNE = False
OUTPUT_KEYS = ('results', 'pnl', 'MZ', 'band_roi')
PUBLIC_TAKER_FIELDS = ('taker_outcome_side', 'taker_book_side', 'taker_side')
BOOK_TO_OUTCOME = {'bid': 'yes', 'ask': 'no'}
SETTLED_KEYS = ('resolution', 'result', 'outcome', 'pnl', 'roi', 'MZ', 'band_roi')
QUOTE_FIELDS = ('mid', 'bid', 'ask', 'prev_price')
SCHEMA_LABEL = 'SCHEMA_ONLY'
BANDS_FILE = ROOT / 'price_bands_10c.v0.json'
SCHEMA_FIXTURE = ROOT / 'fixtures' / 'schema_only_public_trades.json'
FROZEN_EXPERIMENT = ROOT / 'FROZEN_EXPERIMENT.json'
EMPTY_RESULTS = ROOT / 'results' / 'EMPTY_RESULTS.json'
_UNSET = object()


class MakerTakerError(Exception):
    """A schema row or a scorecard claim was rejected."""


class LeeReadyRefused(MakerTakerError):
    """Lee-Ready has no successful path. Native public taker_* fields are required."""


class TakerFieldRefused(MakerTakerError):
    """The row has no agreeing native public taker_* field."""


class ScorecardRefused(MakerTakerError):
    """results, pnl, MZ, and band_roi stay null while settled N is 0."""


class AdmitRefused(MakerTakerError):
    """The clock refused admit. Settled N is 0."""


class RebinRefused(MakerTakerError):
    """Band edges are not refit after outcomes."""


class SchemaOnlyRefused(MakerTakerError):
    """The fixture is a schema sheet, not an admitted settled panel."""


class LiveOrdersForbidden(MakerTakerError):
    """This lab has no live order path."""

    def __init__(self):
        super().__init__('no live orders and no account endpoint')


def _null_metrics():
    return {key: None for key in OUTPUT_KEYS}


def instrument_binding():
    """Pins for the scaffold. Rates are read from the imported feebook stub."""
    table = feebook.load_series_table()
    rates = table['rates']
    return {
        'packet_id': PACKET_ID,
        'experiment_id': EXPERIMENT_ID,
        'panel_version': PANEL_VERSION,
        'collector': COLLECTOR_STATUS,
        'clock': CLOCK_ADMIT,
        'settled_n': SETTLED_N,
        'examiner': EXAMINER_STATUS,
        'feebook_directory': FEEBOOK_DIRECTORY,
        'feebook_commit': FEEBOOK_COMMIT,
        'feebook_imported': True,
        'feebook_copied': False,
        'examiner_formula_id': feebook.EXAMINER_FORMULA_ID,
        'symbols': ('order_fee', 'examiner_fee_channel', 'TAKER_FILLS_RESTING'),
        'price_bands_registry_id': BANDS_REGISTRY_ID,
        'lee_ready': LEE_READY,
        'live_orders': LIVE_ORDERS,
        'authenticated_account_calls': False,
        'signal_retune': SIGNAL_RETUNE,
        'q6_000_retune': Q6_000_RETUNE,
        'maker_rate': feebook.as_decimal(rates['maker'], 'maker'),
        'taker_rate': feebook.as_decimal(rates['taker'], 'taker'),
    }


def execution_adapter():
    """No live order client lives in this lab."""
    raise LiveOrdersForbidden()


def collector_stub():
    """Ready collector. It has not admitted a settled panel."""
    stub = {
        'panel_version': PANEL_VERSION,
        'status': COLLECTOR_STATUS,
        'admitted': False,
        'admitted_settled_panel': False,
        'clock': CLOCK_ADMIT,
        'settled_n': SETTLED_N,
        'examiner': EXAMINER_STATUS,
    }
    stub.update(_null_metrics())
    return stub


def clock_admit(*_args, **_kwargs):
    """The conductor clock refused admission."""
    raise AdmitRefused('Clock REFUSED admit; settled N=0')


def scorecard_refuse(*_args, **_kwargs):
    """Refuse every scorecard fill. Settled N is 0 and the Examiner is not running."""
    raise ScorecardRefused(
        'Clock REFUSED admit; settled N=0; results, pnl, MZ, and band_roi stay null'
    )


def mincer_zarnowitz(*args, **kwargs):
    """Mincer-Zarnowitz has no successful path in this scaffold."""
    scorecard_refuse(*args, **kwargs)


def band_roi(*args, **kwargs):
    """Per-band return has no successful path in this scaffold."""
    scorecard_refuse(*args, **kwargs)


def lee_ready(*_args, **_kwargs):
    """Quote test and tick test are refused for every input."""
    raise LeeReadyRefused(
        'Lee-Ready is refused; native public taker_* fields are required'
    )


def _expected_band_ids():
    return tuple('b%02d' % index for index in range(10))


def load_bands(path=None):
    """Load the pinned 10-cent registry. Edges are not sample quantiles."""
    if path is None:
        path = BANDS_FILE
    payload = json.loads(Path(path).read_text())
    if payload.get('registry_id') != BANDS_REGISTRY_ID:
        raise ValueError('registry_id')
    if payload.get('rebinned_after_outcomes') is not False:
        raise RebinRefused('bands were rebinned after outcomes')
    if payload.get('low_inclusive') is not True or payload.get('high_exclusive') is not True:
        raise ValueError('band edges')
    if payload.get('last_band_includes_one') is not True:
        raise ValueError('last band')
    width = feebook.as_decimal(payload['width_dollars'], 'width_dollars')
    raw_bands = payload.get('bands')
    expected = _expected_band_ids()
    if not isinstance(raw_bands, list) or len(raw_bands) != len(expected):
        raise ValueError('bands')
    parsed = []
    previous_hi = None
    for index, band in enumerate(raw_bands):
        if not isinstance(band, dict) or band.get('id') != expected[index]:
            raise ValueError('band id')
        lo = feebook.as_decimal(band['lo'], 'lo')
        hi = feebook.as_decimal(band['hi'], 'hi')
        if hi - lo != width:
            raise ValueError('width')
        if previous_hi is None:
            if lo != 0:
                raise ValueError('origin')
        elif lo != previous_hi:
            raise ValueError('gap')
        previous_hi = hi
        parsed.append({'id': band['id'], 'lo': lo, 'hi': hi})
    if previous_hi != feebook.ONE:
        raise ValueError('span')
    return {
        'registry_id': payload['registry_id'],
        'width_dollars': width,
        'low_inclusive': True,
        'high_exclusive': True,
        'last_band_includes_one': True,
        'rebinned_after_outcomes': False,
        'bands': parsed,
    }


def rebin_after_outcomes(*_args, **_kwargs):
    """Outcomes do not move the pinned edges."""
    raise RebinRefused('do not rebin after outcomes')


def assign_band(price, bands=None, *, outcome=_UNSET):
    """Assign one price to b00-b09. An outcome argument is a rebin attempt."""
    if outcome is not _UNSET:
        raise RebinRefused('do not rebin after outcomes')
    table = load_bands() if bands is None else bands
    if not isinstance(table, dict) or not isinstance(table.get('bands'), list):
        raise TypeError('bands')
    if table.get('rebinned_after_outcomes') is not False:
        raise RebinRefused('do not rebin after outcomes')
    registry = table.get('registry_id')
    if registry != BANDS_REGISTRY_ID:
        raise ValueError('registry_id')
    if table.get('last_band_includes_one') is not True:
        raise ValueError('last band')
    rows = table['bands']
    if not rows:
        raise ValueError('bands')
    price = feebook.as_decimal(price, 'price')
    if price < 0 or price > feebook.ONE:
        raise ValueError('price')
    last_id = rows[-1]['id']
    for band in rows:
        lo = band['lo'] if isinstance(band['lo'], feebook.Decimal) else feebook.as_decimal(band['lo'], 'lo')
        hi = band['hi'] if isinstance(band['hi'], feebook.Decimal) else feebook.as_decimal(band['hi'], 'hi')
        if price < lo:
            continue
        if price < hi or (band['id'] == last_id and price == hi):
            return {
                'band_id': band['id'],
                'lo': lo,
                'hi': hi,
                'registry_id': BANDS_REGISTRY_ID,
            }
    raise ValueError('price')


def _require_row(row):
    if not isinstance(row, dict):
        raise TypeError('row')
    return row


def _lee_ready_requested(row):
    if 'lee_ready' in row and row['lee_ready'] is not False and row['lee_ready'] is not None:
        return True
    classifier = row.get('classifier')
    if isinstance(classifier, str) and classifier.lower().replace('_', '-') in ('lee-ready', 'leeready'):
        return True
    return False


def _agree(current, value):
    if current is None:
        return value
    if current != value:
        raise TakerFieldRefused('taker_* fields disagree')
    return current


def classify_taker(row):
    """Classify from native public taker_* fields. Quote fields do not vote."""
    row = _require_row(row)
    if _lee_ready_requested(row):
        raise LeeReadyRefused(
            'Lee-Ready is refused; native public taker_* fields are required'
        )
    unknown = [
        key for key in row
        if key.startswith('taker_') and key not in PUBLIC_TAKER_FIELDS
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
    return {
        'taker_outcome_side': outcome,
        'taker_book_side': 'bid' if outcome == 'yes' else 'ask',
        'maker_outcome_side': feebook.TAKER_FILLS_RESTING[outcome],
        'native_fields': present,
        'classification': 'native_public_taker',
        'lee_ready': None,
    }


def _reject_settled(row):
    for key in SETTLED_KEYS:
        if key in row and row[key] is not None:
            raise ScorecardRefused('settled fields are not admitted')


def _contracts(row):
    has_fp = 'count_fp' in row and row['count_fp'] is not None
    has_count = 'count' in row and row['count'] is not None
    if not has_fp and not has_count:
        raise ValueError('contracts')
    fp = feebook.as_decimal(row['count_fp'], 'count_fp') if has_fp else None
    count = feebook.as_decimal(row['count'], 'count') if has_count else None
    if fp is not None and count is not None and fp != count:
        raise ValueError('count_fp and count disagree')
    contracts = fp if fp is not None else count
    if contracts <= 0:
        raise ValueError('contracts')
    return contracts


def _prices(row, taker_outcome):
    if row.get('yes_price_dollars') is None or row.get('no_price_dollars') is None:
        raise ValueError('both dollar prices are required')
    yes = feebook.as_decimal(row['yes_price_dollars'], 'yes_price_dollars')
    no = feebook.as_decimal(row['no_price_dollars'], 'no_price_dollars')
    if yes + no != feebook.ONE:
        raise ValueError('yes and no prices must sum to 1')
    if taker_outcome == 'yes':
        return yes, no
    return no, yes


def _series(row):
    if row.get('series') is None:
        return None
    series = row['series']
    if not isinstance(series, str) or series.strip() == '':
        raise TypeError('series')
    return series


def _block(row):
    if row.get('is_block_trade') is None:
        return None
    if not isinstance(row['is_block_trade'], bool):
        raise TypeError('is_block_trade')
    return row['is_block_trade']


def join_fees(row, table=None):
    """Join examiner taker and maker quotes. Scorecard metrics stay null."""
    row = _require_row(row)
    _reject_settled(row)
    classified = classify_taker(row)
    if table is None:
        table = feebook.load_series_table()
    contracts = _contracts(row)
    taker_price, maker_price = _prices(row, classified['taker_outcome_side'])
    taker_band = assign_band(taker_price)
    maker_band = assign_band(maker_price)
    series = _series(row)
    taker_quote = feebook.order_fee(
        'taker', contracts, taker_price, round_up=True, series=series, table=table,
    )
    maker_quote = feebook.order_fee(
        'maker', contracts, maker_price, round_up=True, series=series, table=table,
    )
    if taker_quote['formula_id'] != feebook.EXAMINER_FORMULA_ID:
        raise MakerTakerError('examiner formula')
    if maker_quote['formula_id'] != feebook.EXAMINER_FORMULA_ID:
        raise MakerTakerError('examiner formula')
    channel = feebook.examiner_fee_channel(taker_quote, maker_quote)
    ignored = [key for key in QUOTE_FIELDS if key in row]
    joined = {
        'schema_id': row.get('schema_id'),
        'label': SCHEMA_LABEL,
        'taker_outcome_side': classified['taker_outcome_side'],
        'maker_outcome_side': classified['maker_outcome_side'],
        'taker_book_side': classified['taker_book_side'],
        'native_fields': classified['native_fields'],
        'classification': classified['classification'],
        'ignored_quote_fields': ignored,
        'contracts': contracts,
        'taker_price': taker_price,
        'maker_price': maker_price,
        'taker_band': taker_band['band_id'],
        'maker_band': maker_band['band_id'],
        'band_registry_id': taker_band['registry_id'],
        'series': series,
        'taker_quote': taker_quote,
        'maker_quote': maker_quote,
        'formula_id': channel['formula_id'],
        'fee_channel': channel,
        'is_block_trade': _block(row),
        'lee_ready': None,
        'scorecard_label': None,
    }
    joined.update(_null_metrics())
    return joined


def load_schema_fixture(path=None):
    """Read the schema sheet. Resolution keys are rejected."""
    if path is None:
        path = SCHEMA_FIXTURE
    payload = json.loads(Path(path).read_text())
    if payload.get('label') != SCHEMA_LABEL:
        raise SchemaOnlyRefused('label')
    if payload.get('admitted_settled_panel') is not False:
        raise SchemaOnlyRefused('admitted settled panel')
    if payload.get('panel_version') != PANEL_VERSION:
        raise ValueError('panel_version')
    if payload.get('collector') != COLLECTOR_STATUS:
        raise ValueError('collector')
    if payload.get('clock') != CLOCK_ADMIT:
        raise ValueError('clock')
    if payload.get('settled_n') != SETTLED_N:
        raise AdmitRefused('settled N is 0')
    rows = payload.get('rows')
    if not isinstance(rows, list) or not rows:
        raise ValueError('rows')
    for row in rows:
        if not isinstance(row, dict) or row.get('schema_only') is not True:
            raise SchemaOnlyRefused('schema_only')
        for key in SETTLED_KEYS:
            if key in row:
                raise SchemaOnlyRefused(key)
    return payload


def walk_schema(path=None, table=None):
    """Join schema rows. Refusals carry no side and no scorecard fill."""
    payload = load_schema_fixture(path)
    joined = []
    refused = []
    for row in payload['rows']:
        try:
            joined.append(join_fees(row, table=table))
        except (TakerFieldRefused, LeeReadyRefused) as exc:
            refusal = {
                'schema_id': row.get('schema_id'),
                'reason': exc.__class__.__name__,
                'lee_ready': None,
            }
            refusal.update(_null_metrics())
            refused.append(refusal)
    walked = {
        'label': SCHEMA_LABEL,
        'admitted_settled_panel': False,
        'panel_version': payload['panel_version'],
        'collector': COLLECTOR_STATUS,
        'clock': CLOCK_ADMIT,
        'settled_n': SETTLED_N,
        'examiner': EXAMINER_STATUS,
        'joined': joined,
        'refusals': refused,
        'lee_ready': None,
        'status': SCHEMA_LABEL,
    }
    walked.update(_null_metrics())
    return walked


def empty_outputs():
    """The freeze contract. Schema walks do not fill it."""
    payload = {
        'settled_n': SETTLED_N,
        'clock': CLOCK_ADMIT,
        'collector': COLLECTOR_STATUS,
        'panel_version': PANEL_VERSION,
        'status': 'EMPTY',
    }
    payload.update(_null_metrics())
    return payload


def frozen_output_snapshot():
    """Read the freeze file. Does not modify it."""
    payload = json.loads(FROZEN_EXPERIMENT.read_text())
    return {key: payload[key] for key in OUTPUT_KEYS}
