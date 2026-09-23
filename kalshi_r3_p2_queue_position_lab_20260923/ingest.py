"""R3-P2 queue_position sample ingest.

Loads the sanitized Mechanic demo fixtures. When a queue_position_fp is
present, the label join cites the R1-P5 rails through the R2-P1 hygiene
bin helper. Q6-000 queue magnitudes stay at the pinned rails values.

Calibration is not run. results, abs_err_contracts, signed_bias, brier,
pnl, mz, and roi stay null. Status is SAMPLE_INGESTED_CALIBRATION_NOT_RUN.
This module does not place live orders and does not read keys.
"""
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

import rails

_hygiene_spec = importlib.util.spec_from_file_location('r2p1_hygiene', HYGIENE_PATH)
hygiene = importlib.util.module_from_spec(_hygiene_spec)
_hygiene_spec.loader.exec_module(hygiene)

LAB_DIRECTORY = 'kalshi_r3_p2_queue_position_lab_20260923'
EXPERIMENT_ID = 'R3-P2-QUEUE-POSITION'
FEATURE_FAMILY = 'R3-P2'
STATUS = 'SAMPLE_INGESTED_CALIBRATION_NOT_RUN'
HOST = 'demo-api.kalshi.co'
TICKER = 'KXNFLGAME-26OCT01PITCLE-PIT'
QUEUE_POSITION_FP = '4207.00'
VERDICT = 'POLL_OK'
L2_TOP_PRICE = '0.01'
L2_TOP_SIZE_NARRATIVE = '~4208'
N_SUCCESS_THIS_RUN = 4
ROWS_TOTAL = 26
EMBEDDED_SAMPLE_BODIES = 1
UNEMBEDDED_ROW_BODIES = 25
FEEBOOK_COMMIT = '22371178cb2663250b4762f328069571c48cb551'
RAILS_COMMIT = '6a28e0d6254327ea4e6451c781bec56215ac6cac'
RAILS_QUEUE_AHEAD = Decimal('3300')
RAILS_STRESS_AHEAD = Decimal('10000')
SCORECARD_FIELDS = (
    'results',
    'abs_err_contracts',
    'signed_bias',
    'brier',
    'pnl',
    'mz',
    'roi',
)
ESTIMATE_FIELDS = (
    'abs_err_contracts',
    'signed_bias',
    'brier',
    'mz',
)
PROFIT_FIELDS = (
    'pnl',
    'roi',
    'profit',
)
SECRET_KEYS = (
    'api_key',
    'api_secret',
    'private_key',
    'access_token',
    'refresh_token',
    'password',
    'secret',
    'authorization',
)
FIXTURES = ROOT / 'fixtures'
FIRST_POLL_PATH = FIXTURES / 'first_demo_queue_poll.json'
SERIES_PATH = FIXTURES / 'demo_queue_sample_series.json'
FROZEN_EXPERIMENT = ROOT / 'FROZEN_EXPERIMENT.json'
EMPTY_RESULTS = ROOT / 'results' / 'EMPTY_RESULTS.json'


class IngestError(Exception):
    """A fixture failed a pin or a forbidden write was requested."""


class CalibrationNotRun(IngestError):
    """Estimate-error and scorecard fields stay null."""


class ProfitLabelRefused(IngestError):
    """A cancel sample and a null scorecard are not profit."""


def null_scorecard():
    """The frozen calibration record. Every metric is null."""
    payload = {key: None for key in SCORECARD_FIELDS}
    payload['status'] = STATUS
    return payload


def assert_null_scorecard(payload):
    """Refuse a non-null calibration or profit field."""
    if not isinstance(payload, dict):
        raise TypeError('scorecard')
    for key in SCORECARD_FIELDS:
        if key not in payload:
            raise CalibrationNotRun('missing %s' % key)
        if payload[key] is not None:
            if key in PROFIT_FIELDS:
                raise ProfitLabelRefused(key)
            raise CalibrationNotRun(key)
    if payload.get('status') != STATUS:
        raise CalibrationNotRun('status')
    if payload.get('profit') is not None:
        raise ProfitLabelRefused('profit')


def refuse_estimate_metrics(proposed=None):
    """Estimate error is not computed from an ingested sample."""
    if proposed is None:
        raise CalibrationNotRun('estimate metrics are not computed')
    if not isinstance(proposed, dict):
        raise TypeError('proposed')
    for key in ESTIMATE_FIELDS:
        if proposed.get(key) is not None:
            raise CalibrationNotRun(key)
    raise CalibrationNotRun('estimate metrics are not computed')


def refuse_profit_label(proposed=None):
    """A queue poll and a null pnl are not a profit label."""
    if proposed is None:
        raise ProfitLabelRefused('profit label is refused')
    if not isinstance(proposed, dict):
        raise TypeError('proposed')
    for key in PROFIT_FIELDS:
        if proposed.get(key) is not None:
            raise ProfitLabelRefused(key)
    if proposed.get('is_profit') is True:
        raise ProfitLabelRefused('is_profit')
    raise ProfitLabelRefused('profit label is refused')


def refuse_live_order():
    """This lab does not place orders."""
    raise IngestError('live orders are refused')


def refuse_q6_retune():
    """Q6-000 queue magnitudes stay on the R1-P5 pins."""
    raise IngestError('Q6-000 retune is refused')


def _walk_secret_keys(value, found):
    if isinstance(value, dict):
        for key, item in value.items():
            if isinstance(key, str) and key.lower() in SECRET_KEYS and item not in (None, ''):
                found.append(key)
            _walk_secret_keys(item, found)
    elif isinstance(value, list):
        for item in value:
            _walk_secret_keys(item, found)


def assert_no_secrets(payload):
    found = []
    _walk_secret_keys(payload, found)
    if found:
        raise IngestError('secret key present')
    if payload.get('secrets') is not None or payload.get('live_keys') is not None:
        raise IngestError('secret payload present')


def load_json(path):
    payload = json.loads(Path(path).read_text())
    if not isinstance(payload, dict):
        raise TypeError('fixture')
    assert_no_secrets(payload)
    return payload


def load_first_poll(path=None):
    poll = load_json(FIRST_POLL_PATH if path is None else path)
    if poll.get('host') != HOST:
        raise IngestError('host')
    if poll.get('verdict') != VERDICT:
        raise IngestError('verdict')
    if poll.get('ticker') != TICKER:
        raise IngestError('ticker')
    if 'queue_position_fp' not in poll or poll['queue_position_fp'] in (None, ''):
        raise IngestError('queue_position_fp')
    if poll['queue_position_fp'] != QUEUE_POSITION_FP:
        raise IngestError('queue_position_fp')
    if poll.get('order_canceled_clean') is not True:
        raise IngestError('cancel')
    if poll.get('is_fill') is not False or poll.get('fill') is not None:
        raise IngestError('fill')
    top = poll.get('l2_top')
    if not isinstance(top, dict):
        raise IngestError('l2_top')
    if top.get('price') != L2_TOP_PRICE:
        raise IngestError('l2 price')
    if top.get('size_narrative') != L2_TOP_SIZE_NARRATIVE:
        raise IngestError('l2 size narrative')
    if top.get('size_exact') is not None:
        raise IngestError('exact l2 size was not stated')
    return poll


def load_series(path=None):
    series = load_json(SERIES_PATH if path is None else path)
    if series.get('host') != HOST or series.get('host_only') is not True:
        raise IngestError('host')
    if series.get('leftover_resting') != 'no':
        raise IngestError('leftover_resting')
    if series.get('n_success_this_run') != N_SUCCESS_THIS_RUN:
        raise IngestError('n_success_this_run')
    if series.get('prior_first_included') is not True:
        raise IngestError('prior_first')
    if series.get('rows_total') != ROWS_TOTAL:
        raise IngestError('rows_total')
    if series.get('embedded_sample_bodies') != EMBEDDED_SAMPLE_BODIES:
        raise IngestError('embedded_sample_bodies')
    if series.get('unembedded_row_bodies') != UNEMBEDDED_ROW_BODIES:
        raise IngestError('unembedded_row_bodies')
    if series.get('this_run_success_bodies_embedded') is not False:
        raise IngestError('this-run bodies')
    if series.get('checkout_contained_desk_bytes') is not False:
        raise IngestError('desk bytes')
    invented = series.get('rows')
    if isinstance(invented, list) and len(invented) > EMBEDDED_SAMPLE_BODIES:
        raise IngestError('invented row bodies')
    return series


def join_queue_label(queue_position_fp):
    """Cite R1-P5. The observed position is labeled; the rails are unchanged."""
    if rails.QUEUE_AHEAD_DEFAULT != RAILS_QUEUE_AHEAD:
        raise IngestError('rails queue ahead changed')
    if rails.STRESS_QUEUE_AHEAD != RAILS_STRESS_AHEAD:
        raise IngestError('rails stress queue changed')
    if hygiene.ASSUMED_SCENARIOS != ('q3300', 'q10000'):
        raise IngestError('assumed scenarios changed')
    attributed = hygiene.queue_attribution_bin(queue_position_fp)
    return {
        'queue_position_fp': str(queue_position_fp),
        'queue_attribution_bin': attributed,
        'rails_commit': RAILS_COMMIT,
        'rails_queue_ahead': str(rails.QUEUE_AHEAD_DEFAULT),
        'rails_stress_ahead': str(rails.STRESS_QUEUE_AHEAD),
        'q6_retune': False,
        'scorecard_write': False,
    }


def ingest():
    """Load the fixtures and return the null scorecard plus the label join."""
    poll = load_first_poll()
    series = load_series()
    label = join_queue_label(poll['queue_position_fp'])
    scorecard = null_scorecard()
    assert_null_scorecard(scorecard)
    frozen = load_json(FROZEN_EXPERIMENT)
    empty = load_json(EMPTY_RESULTS)
    assert_null_scorecard(frozen)
    assert_null_scorecard(empty)
    if frozen.get('live_orders') is not False or frozen.get('signal_retune_000') is not False:
        raise IngestError('freeze flags')
    return {
        'experiment_id': EXPERIMENT_ID,
        'feature_family': FEATURE_FAMILY,
        'status': STATUS,
        'host': HOST,
        'ticker': poll['ticker'],
        'verdict': poll['verdict'],
        'queue_position_fp': poll['queue_position_fp'],
        'order_canceled_clean': True,
        'is_fill': False,
        'n_success_this_run': series['n_success_this_run'],
        'prior_first_included': True,
        'rows_total': series['rows_total'],
        'embedded_sample_bodies': series['embedded_sample_bodies'],
        'unembedded_row_bodies': series['unembedded_row_bodies'],
        'leftover_resting': series['leftover_resting'],
        'queue_label': label,
        'scorecard': scorecard,
        'live_orders': False,
        'signal_retune_000': False,
    }
