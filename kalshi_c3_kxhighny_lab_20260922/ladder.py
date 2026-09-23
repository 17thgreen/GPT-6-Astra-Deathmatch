"""C3-KXHIGHNY bordering-strike scaffold.

Adjacent whole-degree strikes on schema ladders for KXHIGHNY and KXHIGHCHI.
Books and maker credit come from the imported feebook and rails. The GitHub
weather-spread text stays a hypothesis. Settled fills are refused. results,
pnl, MZ, and ROI stay null.
"""
import json
import re
import sys
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PARENT = ROOT.parent
FEEBOOK_DIR = PARENT / 'kalshi_feebook_lab_20260922'
RAILS_DIR = PARENT / 'kalshi_rails_lab_20260922'
if str(FEEBOOK_DIR) not in sys.path:
    sys.path.insert(0, str(FEEBOOK_DIR))
if str(RAILS_DIR) not in sys.path:
    sys.path.insert(0, str(RAILS_DIR))

import feebook
import rails

PACKET_ID = 'C3-KXHIGHNY-MEAS'
EXPERIMENT_ID = 'c3_kxhighny_meas_20260922'
PANEL_VERSION = '2026-09-23.c3-kxhighny-meas-v0'
BORDER_RULE_ID = 'astra.c3.kxhighny.bordering_strike.v0'
HYPOTHESIS_ID = 'github.weather_spread.mutually_exclusive_buckets.hypothesis_only'
FEEBOOK_COMMIT = '22371178cb2663250b4762f328069571c48cb551'
FEEBOOK_DIRECTORY = 'kalshi_feebook_lab_20260922'
RAILS_COMMIT = '6a28e0d6254327ea4e6451c781bec56215ac6cac'
RAILS_DIRECTORY = 'kalshi_rails_lab_20260922'
WEATHER_BLOB_SHA = '323463cd7538464dfe90ec8b6acea9c76e10ee29'
WEATHER_REF = 'ce34417c1a2f3353225ed6e585e48217d41de96d'
COLLECTOR_STATUS = 'READY'
CLOCK_ADMIT = 'REFUSED'
SETTLED_N = 0
EXAMINER_STATUS = 'NOT_NOW'
LIVE_ORDERS = False
SIGNAL_RETUNE = False
Q6_000_RETUNE = False
SCHEMA_LABEL = 'SCHEMA_ONLY'
OUTPUT_KEYS = ('results', 'pnl', 'MZ', 'ROI')
PROBE_CONTRACTS = Decimal('1')
DEGREE = Decimal('1')
SERIES = ('KXHIGHNY', 'KXHIGHCHI')
STATIONS = {
    'KXHIGHNY': {'city': 'New York City', 'nws_station': 'KNYC'},
    'KXHIGHCHI': {'city': 'Chicago', 'nws_station': 'KMDW', 'identity_note': 'Midway'},
}
MONTHS = ('JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC')
EVENT_TICKER = re.compile(
    r'^(KXHIGHNY|KXHIGHCHI)-(\d{2})(' + '|'.join(MONTHS) + r')(\d{2})$'
)
SETTLED_KEYS = (
    'resolution', 'result', 'outcome', 'settlement', 'settled',
    'fill', 'fills', 'pnl', 'roi', 'ROI', 'MZ', 'results',
)
SCHEMA_FIXTURE = ROOT / 'fixtures' / 'schema_only_ladder.json'
FROZEN_EXPERIMENT = ROOT / 'FROZEN_EXPERIMENT.json'
EMPTY_RESULTS = ROOT / 'results' / 'EMPTY_RESULTS.json'


class LadderError(Exception):
    """A schema ladder or a scorecard claim was rejected."""


class LadderDefect(LadderError):
    """Strikes overlap, repeat, or break the tail rules."""


class SeriesRefused(LadderError):
    """The packet ladder is KXHIGHNY and KXHIGHCHI."""


class SettledFillRefused(LadderError):
    """A settled fill is not part of this schema sheet."""


class InventedFillRefused(LadderError):
    """Queue volume is not awarded on this scaffold."""


class ScorecardRefused(LadderError):
    """results, pnl, MZ, and ROI stay null while settled N is 0."""


class AdmitRefused(LadderError):
    """The clock refused admit. Settled N is 0."""


class AlgoPortRefused(LadderError):
    """The GitHub weather-spread text is a hypothesis. It is not ported."""


class SchemaOnlyRefused(LadderError):
    """The fixture is a schema sheet, not an admitted settled panel."""


class LiveOrdersForbidden(LadderError):
    """This lab has no live order path."""

    def __init__(self):
        super().__init__('no live orders and no account endpoint')


def _null_metrics():
    return {key: None for key in OUTPUT_KEYS}


def weather_spread_hypothesis():
    """Citation of the GitHub ladder text. ROI stays null."""
    record = {
        'hypothesis_id': HYPOTHESIS_ID,
        'repo': '17thgreen/Claude-SportsBetting-Competition-to-the-Death',
        'path': 'src/flatstake/providers/kalshi_weather.py',
        'blob_sha': WEATHER_BLOB_SHA,
        'ref': WEATHER_REF,
        'vendored': False,
        'algo_ported': False,
        'published_returns_are_evidence': False,
        'sum_of_mids_computed_here': False,
        'statement': (
            'A daily high-temperature ladder is mutually exclusive buckets. '
            'Honest mids on an exhaustive ladder should sum to about 1. '
            'That overround is a hypothesis, not a scorecard entry.'
        ),
    }
    record.update(_null_metrics())
    return record


def instrument_binding():
    """Pins for the scaffold. Rates and queue labels come from the imports."""
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
        'border_rule_id': BORDER_RULE_ID,
        'series': list(SERIES),
        'stations': STATIONS,
        'feebook_directory': FEEBOOK_DIRECTORY,
        'feebook_commit': FEEBOOK_COMMIT,
        'feebook_imported': True,
        'feebook_copied': False,
        'examiner_formula_id': feebook.EXAMINER_FORMULA_ID,
        'rails_directory': RAILS_DIRECTORY,
        'rails_commit': RAILS_COMMIT,
        'rails_imported': True,
        'rails_copied': False,
        'fee_credit_rule_id': rails.FEE_CREDIT_RULE_ID,
        'queue_q3300': rails.scenario_queue('q3300'),
        'queue_q10000': rails.scenario_queue('q10000'),
        'queue_labels_are_a_knob': False,
        'hypothesis_id': HYPOTHESIS_ID,
        'algo_ported': False,
        'live_orders': LIVE_ORDERS,
        'authenticated_account_calls': False,
        'signal_retune': SIGNAL_RETUNE,
        'q6_000_retune': Q6_000_RETUNE,
        'maker_rate': feebook.as_decimal(rates['maker'], 'maker'),
        'taker_rate': feebook.as_decimal(rates['taker'], 'taker'),
        'later_r3_p3_panel': {'preferred': True, 'joined_now': False},
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
        'series': list(SERIES),
        'later_r3_p3_panel': {
            'preferred': True,
            'joined_now': False,
            'native_taker_fields_present': False,
        },
    }
    stub.update(_null_metrics())
    return stub


def clock_admit(*_args, **_kwargs):
    """The conductor clock refused admission."""
    raise AdmitRefused('Clock REFUSED admit; settled N=0')


def scorecard_refuse(*_args, **_kwargs):
    """Refuse every scorecard fill. Settled N is 0 and the Examiner is not running."""
    raise ScorecardRefused(
        'Clock REFUSED admit; settled N=0; results, pnl, MZ, and ROI stay null'
    )


def write_scorecard(_payload):
    """Schema walks do not write the freeze file."""
    scorecard_refuse()


def mincer_zarnowitz(*args, **kwargs):
    """Mincer-Zarnowitz has no successful path in this scaffold."""
    scorecard_refuse(*args, **kwargs)


def roi(*args, **kwargs):
    """Return has no successful path in this scaffold."""
    scorecard_refuse(*args, **kwargs)


def port_weather_algorithm(*_args, **_kwargs):
    """Forecast and implied-distribution code stay in the cited repository."""
    raise AlgoPortRefused(
        'GitHub weather-spread is hypothesis only; the forecast ladder is not ported'
    )


def award_queue_fill(*_args, **_kwargs):
    """Rails queue labels are not a fill engine here."""
    raise InventedFillRefused('queue volume is not awarded')


def _require_mapping(value, name):
    if not isinstance(value, dict):
        raise TypeError(name)
    return value


def _whole_degree(value, name):
    if value is None:
        return None
    strike = feebook.as_decimal(value, name)
    if strike != strike.to_integral_value():
        raise LadderDefect('strikes are whole degrees')
    return strike


def _reject_settled(payload):
    if not isinstance(payload, dict):
        return
    for key in SETTLED_KEYS:
        if key in payload and payload[key] is not None:
            raise SettledFillRefused('settled fills are not admitted')
    for key, value in payload.items():
        if isinstance(value, dict):
            _reject_settled(value)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    _reject_settled(item)


def _series(value):
    if value not in SERIES:
        raise SeriesRefused('series')
    return value


def _event_ticker(series, ticker):
    if not isinstance(ticker, str):
        raise TypeError('event_ticker')
    match = EVENT_TICKER.match(ticker)
    if match is None or match.group(1) != series:
        raise LadderDefect('event_ticker')
    return ticker


def _rung_ticker(event_ticker, ticker):
    if not isinstance(ticker, str) or not ticker.startswith(event_ticker + '-'):
        raise LadderDefect('ticker')
    return ticker


def _parse_rung(raw, series, event_ticker):
    raw = _require_mapping(raw, 'rung')
    _reject_settled(raw)
    floor_strike = _whole_degree(raw.get('floor_strike'), 'floor_strike')
    cap_strike = _whole_degree(raw.get('cap_strike'), 'cap_strike')
    if floor_strike is None and cap_strike is None:
        raise LadderDefect('empty strike')
    if floor_strike is not None and cap_strike is not None and cap_strike < floor_strike:
        raise LadderDefect('cap below floor')
    book = raw.get('orderbook_fp')
    if book is not None and not isinstance(book, dict):
        raise TypeError('orderbook_fp')
    return {
        'ticker': _rung_ticker(event_ticker, raw.get('ticker')),
        'series': series,
        'event_ticker': event_ticker,
        'floor_strike': floor_strike,
        'cap_strike': cap_strike,
        'orderbook_fp': book,
    }


def _ordered(rungs):
    if not rungs:
        raise LadderDefect('rungs')
    bottoms = [rung for rung in rungs if rung['floor_strike'] is None]
    tops = [rung for rung in rungs if rung['cap_strike'] is None]
    if len(bottoms) > 1:
        raise LadderDefect('more than one bottom tail')
    if len(tops) > 1:
        raise LadderDefect('more than one top tail')
    floors = [rung['floor_strike'] for rung in rungs if rung['floor_strike'] is not None]
    if len(floors) != len(set(floors)):
        raise LadderDefect('duplicate floor')
    return sorted(
        rungs,
        key=lambda rung: (
            rung['floor_strike'] is not None,
            rung['floor_strike'] if rung['floor_strike'] is not None else Decimal('0'),
        ),
    )


def _relation(colder, warmer):
    if colder['cap_strike'] is None:
        raise LadderDefect('top tail is not last')
    if warmer['floor_strike'] is None:
        raise LadderDefect('bottom tail is not first')
    degree_gap = warmer['floor_strike'] - colder['cap_strike']
    if degree_gap <= 0:
        raise LadderDefect('overlap')
    relation = 'border' if degree_gap == DEGREE else 'gap'
    pair = {
        'relation': relation,
        'rule_id': BORDER_RULE_ID,
        'colder_ticker': colder['ticker'],
        'warmer_ticker': warmer['ticker'],
        'degree_gap': degree_gap,
        'uncovered_degrees': degree_gap - DEGREE,
        'inserted_rung': False,
    }
    pair.update(_null_metrics())
    return pair


def bordering_pairs(rungs):
    """Adjacent whole-degree strikes. Gaps stay gaps. Overlaps raise."""
    ordered = _ordered(rungs)
    borders = []
    gaps = []
    for index in range(len(ordered) - 1):
        pair = _relation(ordered[index], ordered[index + 1])
        if pair['relation'] == 'border':
            borders.append(pair)
        else:
            gaps.append(pair)
    return {'ordered': ordered, 'borders': borders, 'gaps': gaps}


def _quote_rung(rung):
    quoted = {
        'ticker': rung['ticker'],
        'floor_strike': rung['floor_strike'],
        'cap_strike': rung['cap_strike'],
        'book': None,
        'maker_admission': None,
        'awarded_fill': None,
        'series_resolution': None,
    }
    book_raw = rung['orderbook_fp']
    if book_raw is not None:
        book = feebook.reciprocal_book({'orderbook_fp': book_raw})
        quoted['book'] = book
        if book['bid_yes'] is not None:
            evaluation = rails.maker_quote_credit(
                book['bid_yes'], PROBE_CONTRACTS, series=rung['series'],
            )
            quoted['maker_admission'] = {
                'rule_id': evaluation['rule_id'],
                'admitted': evaluation['admitted'],
                'credit': evaluation['credit'],
                'price': evaluation['price'],
                'contracts': evaluation['contracts'],
                'formula_id': evaluation['fee_quote']['formula_id'],
                'series_resolution': evaluation['fee_quote']['series_resolution'],
            }
            quoted['series_resolution'] = evaluation['fee_quote']['series_resolution']
    quoted.update(_null_metrics())
    return quoted


def admit_rung_quote(rung):
    """Raise when the one-contract YES bid fails the imported credit floor."""
    quoted = _quote_rung(rung)
    admission = quoted['maker_admission']
    if admission is None:
        raise feebook.BookIncomplete('missing yes bid')
    if not admission['admitted']:
        raise rails.MakerCreditRefused(admission)
    return admission


def ladder_observation(event):
    """Canonical content token for the rails freshness predicate."""
    payload = {
        'series': event['series'],
        'event_ticker': event['event_ticker'],
        'rungs': [
            {
                'ticker': rung['ticker'],
                'floor_strike': None if rung['floor_strike'] is None else format(rung['floor_strike'], 'f'),
                'cap_strike': None if rung['cap_strike'] is None else format(rung['cap_strike'], 'f'),
                'orderbook_fp': rung['orderbook_fp'],
            }
            for rung in event['rungs']
        ],
    }
    return rails.BookObservation(
        rails.canonical_book_content(payload),
        event.get('schema_transaction_time'),
    )


def judge_ladder_freshness(previous, current, *, keepalive=False):
    """Content or schema transaction label. A keepalive is never fresh."""
    return rails.judge_freshness(previous, current, keepalive=keepalive)


def _parse_event(raw):
    raw = _require_mapping(raw, 'event')
    if raw.get('schema_only') is not True:
        raise SchemaOnlyRefused('schema_only')
    _reject_settled(raw)
    series = raw.get('series')
    if series not in SERIES:
        raise SeriesRefused('series')
    event_ticker = _event_ticker(series, raw.get('event_ticker'))
    rungs_raw = raw.get('rungs')
    if not isinstance(rungs_raw, list) or not rungs_raw:
        raise LadderDefect('rungs')
    rungs = [_parse_rung(rung, series, event_ticker) for rung in rungs_raw]
    return {
        'schema_id': raw.get('schema_id'),
        'series': series,
        'event_ticker': event_ticker,
        'schema_transaction_time': raw.get('schema_transaction_time'),
        'rungs': rungs,
    }


def _event_report(event):
    paired = bordering_pairs(event['rungs'])
    observation = ladder_observation(event)
    freshness = judge_ladder_freshness(None, observation)
    report = {
        'schema_id': event['schema_id'],
        'series': event['series'],
        'event_ticker': event['event_ticker'],
        'station': dict(STATIONS[event['series']]),
        'rungs': [_quote_rung(rung) for rung in paired['ordered']],
        'borders': paired['borders'],
        'gaps': paired['gaps'],
        'freshness': {'fresh': freshness.fresh, 'reason': freshness.reason},
        'awarded_fill': None,
        'sum_of_mids': None,
        'native_taker_fields_present': False,
    }
    report.update(_null_metrics())
    return report


def load_schema_fixture(path=None):
    """Read the schema sheet. Resolution keys are rejected."""
    if path is None:
        path = SCHEMA_FIXTURE
    payload = json.loads(Path(path).read_text())
    if payload.get('label') != SCHEMA_LABEL:
        raise SchemaOnlyRefused('label')
    if payload.get('packet_id') != PACKET_ID:
        raise ValueError('packet_id')
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
    if payload.get('invented_fills') is not False:
        raise InventedFillRefused('fixture claims fills')
    events = payload.get('events')
    if not isinstance(events, list) or not events:
        raise ValueError('events')
    _reject_settled(payload)
    return payload


def simulate_ladder(path=None):
    """Walk the schema ladder. Scorecard metrics stay null."""
    payload = load_schema_fixture(path)
    events = []
    refusals = []
    for raw in payload['events']:
        schema_id = raw.get('schema_id') if isinstance(raw, dict) else None
        try:
            events.append(_event_report(_parse_event(raw)))
        except (SeriesRefused, LadderDefect, SettledFillRefused) as exc:
            refusal = {
                'schema_id': schema_id,
                'reason': exc.__class__.__name__,
                'awarded_fill': None,
            }
            refusal.update(_null_metrics())
            refusals.append(refusal)
    walked = {
        'label': SCHEMA_LABEL,
        'packet_id': PACKET_ID,
        'admitted_settled_panel': False,
        'panel_version': payload['panel_version'],
        'collector': COLLECTOR_STATUS,
        'clock': CLOCK_ADMIT,
        'settled_n': SETTLED_N,
        'examiner': EXAMINER_STATUS,
        'invented_fills': False,
        'later_r3_p3_panel': {
            'preferred': True,
            'joined_now': False,
            'native_taker_fields_present': False,
        },
        'events': events,
        'refusals': refusals,
        'status': SCHEMA_LABEL,
    }
    walked.update(_null_metrics())
    return walked


def empty_outputs():
    """The freeze contract. Schema walks do not fill it."""
    payload = {
        'packet_id': PACKET_ID,
        'panel_version': PANEL_VERSION,
        'collector': COLLECTOR_STATUS,
        'clock': CLOCK_ADMIT,
        'settled_n': SETTLED_N,
        'status': 'EMPTY',
        'invented_fills': False,
    }
    payload.update(_null_metrics())
    return payload


def frozen_output_snapshot():
    """Read the freeze file. Does not modify it."""
    payload = json.loads(FROZEN_EXPERIMENT.read_text())
    return {key: payload[key] for key in OUTPUT_KEYS}
