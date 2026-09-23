"""R3-P2 queue_position sample ingest.

The series source is the operator desk JSON at DESK_SERIES_PATH:
`{meta, samples[]}`. It is not NDJSON. queue_position_fp on each sample
must match the batch `queue_positions` entry with the same order_id.

sample_id 0 is cross-checked against the first-poll fixture
(queue_position_fp 4207.00, ticker KXNFLGAME-26OCT01PITCLE-PIT, cancel,
fill absent).

abs_err_contracts, signed_bias, and brier stay null on every sample and
in the freeze. results, pnl, mz, and roi stay null. Status is
SAMPLE_INGESTED_CALIBRATION_NOT_RUN.

This module does not invent missing sample bodies, does not place live
orders, and does not retune Q6-000.
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
SAMPLE_NULL_FIELDS = (
    'abs_err_contracts',
    'signed_bias',
    'brier',
)
ESTIMATE_FIELDS = SAMPLE_NULL_FIELDS + ('mz',)
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
DESK_SERIES_PATH = (
    PARENT / 'lab' / 'governance' / 'astra' / 'packets'
    / 'r3_p2_queue_position' / 'results' / 'demo_queue_sample_series.json'
)
NARRATIVE_NAME = 'MECHANIC_DEMO_QUEUE_SAMPLE_SERIES_2026-09-23.md'
FROZEN_EXPERIMENT = ROOT / 'FROZEN_EXPERIMENT.json'
EMPTY_RESULTS = ROOT / 'results' / 'EMPTY_RESULTS.json'


class IngestError(Exception):
    """A fixture failed a pin or a forbidden write was requested."""


class SeriesSourceAbsent(IngestError):
    """The desk series JSON is not on this checkout. Bodies are not invented."""


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


def sha256_bytes(raw):
    return hashlib.sha256(raw).hexdigest()


def sha256_file(path):
    return sha256_bytes(Path(path).read_bytes())


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


def _strip_secrets(value):
    if isinstance(value, dict):
        clean = {}
        for key, item in value.items():
            if isinstance(key, str) and key.lower() in SECRET_KEYS:
                continue
            clean[key] = _strip_secrets(item)
        return clean
    if isinstance(value, list):
        return [_strip_secrets(item) for item in value]
    return value


def _norm_fp(value):
    """Decimal equality. 4207, 4207.0, and 4207.00 are the same position."""
    if isinstance(value, dict):
        value = value.get('queue_position_fp')
    if value is None or value == '':
        raise IngestError('queue_position_fp')
    try:
        return Decimal(str(value))
    except Exception as exc:
        raise IngestError('queue_position_fp') from exc


def _fp_text(value):
    number = _norm_fp(value)
    text = format(number, 'f')
    if '.' not in text:
        text += '.00'
    return text


def _leftover_ok(value):
    if value is False:
        return True
    if isinstance(value, str) and value.lower() in ('no', 'false'):
        return True
    return False


def _host_ok(value):
    if value is None:
        return True
    return value == HOST


def _cancel_not_fill(sample):
    if sample.get('is_fill') is True:
        raise IngestError('fill')
    if sample.get('fill') not in (None, False, 0, ''):
        if sample.get('fill') is not None:
            raise IngestError('fill')
    flags = (
        sample.get('order_canceled_clean'),
        sample.get('cancel_confirmed'),
        sample.get('canceled_clean'),
        sample.get('cancelled_clean'),
    )
    status = sample.get('status') or sample.get('order_status') or sample.get('action')
    status_cancel = isinstance(status, str) and status.lower() in (
        'canceled', 'cancelled', 'cancel', 'canceled_clean', 'cancel_confirmed',
    )
    if True in flags or status_cancel:
        return True
    if sample.get('is_fill') is False and sample.get('order_canceled_clean') is True:
        return True
    raise IngestError('cancel')


def _queue_position_index(payload):
    batch = None
    if 'queue_positions' in payload:
        batch = payload['queue_positions']
    elif isinstance(payload.get('batch'), dict) and 'queue_positions' in payload['batch']:
        batch = payload['batch']['queue_positions']
    elif isinstance(payload.get('meta'), dict) and 'queue_positions' in payload['meta']:
        batch = payload['meta']['queue_positions']
    if batch is None:
        raise IngestError('queue_positions')
    index = {}
    if isinstance(batch, dict):
        rows = batch.items()
        for order_id, value in rows:
            index[str(order_id)] = value
    elif isinstance(batch, list):
        for row in batch:
            if not isinstance(row, dict) or 'order_id' not in row:
                raise IngestError('queue_positions row')
            index[str(row['order_id'])] = row
    else:
        raise IngestError('queue_positions')
    return index


def _assert_sample_nulls(sample):
    for key in SAMPLE_NULL_FIELDS:
        if sample.get(key) is not None:
            raise CalibrationNotRun(key)


def assert_series_document(payload, first_poll=None):
    """Pin {meta, samples[]}. Match queue_position_fp by order_id. Keep errors null."""
    if not isinstance(payload, dict):
        raise IngestError('series schema')
    if 'samples' not in payload or 'meta' not in payload:
        raise IngestError('series schema')
    meta = payload['meta']
    samples = payload['samples']
    if not isinstance(meta, dict) or not isinstance(samples, list):
        raise IngestError('series schema')
    if not _leftover_ok(meta.get('leftover_resting')):
        raise IngestError('leftover_resting')
    if not _host_ok(meta.get('host')):
        raise IngestError('host')
    for key in SAMPLE_NULL_FIELDS:
        if meta.get(key) is not None:
            raise CalibrationNotRun(key)
    index = _queue_position_index(payload)
    seen = set()
    prior = None
    for sample in samples:
        if not isinstance(sample, dict):
            raise IngestError('sample')
        if 'sample_id' not in sample:
            raise IngestError('sample_id')
        sample_id = sample['sample_id']
        if sample_id in seen:
            raise IngestError('duplicate sample_id')
        seen.add(sample_id)
        if 'order_id' not in sample or sample['order_id'] in (None, ''):
            raise IngestError('order_id')
        order_id = str(sample['order_id'])
        if order_id not in index:
            raise IngestError('order_id unmatched')
        if _norm_fp(sample.get('queue_position_fp')) != _norm_fp(index[order_id]):
            raise IngestError('queue_position_fp mismatch')
        if not _host_ok(sample.get('host')):
            raise IngestError('host')
        _cancel_not_fill(sample)
        _assert_sample_nulls(sample)
        assert_no_secrets(sample)
        if sample_id == 0:
            prior = sample
    if prior is None:
        raise IngestError('sample_id 0')
    if prior.get('ticker') != TICKER:
        raise IngestError('sample_id 0 ticker')
    if _norm_fp(prior.get('queue_position_fp')) != _norm_fp(QUEUE_POSITION_FP):
        raise IngestError('sample_id 0 queue_position_fp')
    if first_poll is not None:
        if _norm_fp(first_poll.get('queue_position_fp')) != _norm_fp(prior.get('queue_position_fp')):
            raise IngestError('sample_id 0 cross-check')
        if first_poll.get('ticker') != prior.get('ticker'):
            raise IngestError('sample_id 0 cross-check')
        if first_poll.get('is_fill') is not False:
            raise IngestError('sample_id 0 cross-check')
    return {
        'samples_n': len(samples),
        'n_success_including_prior': meta.get('n_success_including_prior'),
        'n_success_new_total': meta.get('n_success_new_total'),
        'leftover_resting': meta.get('leftover_resting'),
        'sample_id_0_queue_position_fp': _fp_text(prior.get('queue_position_fp')),
        'sample_id_0_order_id': str(prior['order_id']),
    }


def load_json_text(text):
    stripped = text.lstrip()
    if not stripped.startswith('{'):
        raise IngestError('series schema')
    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        raise IngestError('series schema') from exc
    if not isinstance(payload, dict):
        raise IngestError('series schema')
    assert_no_secrets(payload)
    return payload


def load_json(path):
    return load_json_text(Path(path).read_text())


def load_first_poll(path=None):
    poll = load_json(FIRST_POLL_PATH if path is None else path)
    if poll.get('host') != HOST:
        raise IngestError('host')
    if poll.get('verdict') != VERDICT:
        raise IngestError('verdict')
    if poll.get('ticker') != TICKER:
        raise IngestError('ticker')
    if _norm_fp(poll.get('queue_position_fp')) != _norm_fp(QUEUE_POSITION_FP):
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


def resolve_series_path(path=None):
    """Desk JSON wins. The lab fixture is the sanitized copy, when present."""
    if path is not None:
        candidate = Path(path)
        if not candidate.is_file():
            raise SeriesSourceAbsent(str(candidate))
        return candidate
    if DESK_SERIES_PATH.is_file():
        return DESK_SERIES_PATH
    if SERIES_PATH.is_file():
        return SERIES_PATH
    raise SeriesSourceAbsent(str(DESK_SERIES_PATH))


def load_series(path=None, first_poll=None):
    source = resolve_series_path(path)
    payload = load_json(source)
    if 'samples' not in payload or 'meta' not in payload:
        raise IngestError('series schema')
    summary = assert_series_document(payload, first_poll=first_poll)
    summary['source_path'] = str(source)
    summary['sha256'] = sha256_file(source)
    summary['samples'] = payload['samples']
    summary['meta'] = payload['meta']
    return summary


def embed_desk_series(dest=None):
    """Copy a sanitized desk series into fixtures. Refuse a missing source."""
    if not DESK_SERIES_PATH.is_file():
        raise SeriesSourceAbsent(str(DESK_SERIES_PATH))
    payload = _strip_secrets(load_json(DESK_SERIES_PATH))
    poll = load_first_poll()
    assert_series_document(payload, first_poll=poll)
    raw = (json.dumps(payload, indent=2, sort_keys=True) + '\n').encode('utf-8')
    target = SERIES_PATH if dest is None else Path(dest)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(raw)
    return {
        'sha256': sha256_bytes(raw),
        'bytes': len(raw),
        'samples_n': len(payload['samples']),
        'path': str(target),
    }


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
        'queue_position_fp': _fp_text(queue_position_fp),
        'queue_attribution_bin': attributed,
        'rails_commit': RAILS_COMMIT,
        'rails_queue_ahead': str(rails.QUEUE_AHEAD_DEFAULT),
        'rails_stress_ahead': str(rails.STRESS_QUEUE_AHEAD),
        'q6_retune': False,
        'scorecard_write': False,
    }


def ingest():
    """Load the first poll and the series when the desk JSON is present."""
    poll = load_first_poll()
    label = join_queue_label(poll['queue_position_fp'])
    scorecard = null_scorecard()
    assert_null_scorecard(scorecard)
    frozen = load_json(FROZEN_EXPERIMENT)
    empty = load_json(EMPTY_RESULTS)
    assert_null_scorecard(frozen)
    assert_null_scorecard(empty)
    if frozen.get('live_orders') is not False or frozen.get('signal_retune_000') is not False:
        raise IngestError('freeze flags')
    series = None
    series_error = None
    try:
        series = load_series(first_poll=poll)
    except SeriesSourceAbsent as exc:
        series_error = str(exc)
    report = {
        'experiment_id': EXPERIMENT_ID,
        'feature_family': FEATURE_FAMILY,
        'status': STATUS,
        'host': HOST,
        'ticker': poll['ticker'],
        'verdict': poll['verdict'],
        'queue_position_fp': _fp_text(poll['queue_position_fp']),
        'order_canceled_clean': True,
        'is_fill': False,
        'sample_id_0_cross_check': True,
        'series_embedded': series is not None,
        'series_source_absent': series is None,
        'series_error': series_error,
        'samples_n': None if series is None else series['samples_n'],
        'n_success_including_prior': None if series is None else series['n_success_including_prior'],
        'n_success_new_total': None if series is None else series['n_success_new_total'],
        'series_sha256': None if series is None else series['sha256'],
        'leftover_resting': None if series is None else series['leftover_resting'],
        'queue_label': label,
        'scorecard': scorecard,
        'live_orders': False,
        'signal_retune_000': False,
    }
    return report
