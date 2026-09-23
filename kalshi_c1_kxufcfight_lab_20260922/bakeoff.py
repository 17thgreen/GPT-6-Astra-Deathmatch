"""C1 KXUFCFIGHT fee and queue honesty scaffold.

Maker and taker fees come from kalshi_feebook_lab_20260922. Freshness,
queue-bin labels, and maker-credit admission come from
kalshi_rails_lab_20260922. The shared 5000 USD figure is a measurement
contrast label on KXUFCFIGHT and on the 000 instrument pointer.

The conductor reports settled N of 4 and a kicked clock rejoin. Admit status
is NOT_ADMITTED, so results, pnl, MZ, and roi stay null. This module does not
place live orders and does not award fills.
"""
import hashlib
import json
import sys
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

PACKET_ID = 'C1-KXUFCFIGHT-MEAS'
EXPERIMENT_ID = 'c1_kxufcfight_meas_20260922'
PANEL_VERSION = '2026-09-22.c1-kxufcfight-meas-v0'
SERIES_KXUFCFIGHT = 'KXUFCFIGHT'
INSTRUMENT_000 = '000'
ARM_IDS = (SERIES_KXUFCFIGHT, INSTRUMENT_000)
FEEBOOK_COMMIT = '22371178cb2663250b4762f328069571c48cb551'
RAILS_COMMIT = '6a28e0d6254327ea4e6451c781bec56215ac6cac'
FEEBOOK_DIRECTORY = 'kalshi_feebook_lab_20260922'
RAILS_DIRECTORY = 'kalshi_rails_lab_20260922'
COLLECTOR_STATUS = 'READY'
CLOCK_ADMIT = 'NOT_ADMITTED'
CLOCK_REJOIN = 'KICKED'
AWAITING_CLOCK = 'CLOCK_ADMIT_PASS'
REPORTED_SETTLED_N = 4
ADMITTED_SETTLED_N = 0
EVENTS_FINALIZED = 2
SETTLED_N = ADMITTED_SETTLED_N
RESOLUTION_LABEL = 'NOT_ADMITTED'
EXAMINER_STATUS = 'NOT_NOW'
LEE_READY = False
LIVE_ORDERS = False
Q6_000_RETUNE = False
STRATEGY_PORT = False
STRATEGY_CLAIM = False
MEASUREMENT_BUDGET_USD = Decimal('5000')
BUDGET_ROLE = 'measurement_contrast_label'
SHADOW_FILE = PARENT / 'nfl_factorial_lab_20260921' / 'SHADOW_CANDIDATE_FREEZE.json'
SHADOW_SHA256 = 'b55ff36cb161c824a3d1b490795c8ac6891f01489456f61da311ac863366af48'
OUTPUT_KEYS = ('results', 'pnl', 'MZ', 'roi')
PUBLIC_TAKER_FIELDS = ('taker_outcome_side', 'taker_book_side', 'taker_side')
BOOK_TO_OUTCOME = {'bid': 'yes', 'ask': 'no'}
QUOTE_FIELDS = ('mid', 'bid', 'ask', 'prev_price')
SETTLED_KEYS = (
    'resolution', 'result', 'settled_result', 'pnl', 'roi', 'MZ', 'mz',
    'winner', 'band_roi',
)
FILL_KEYS = (
    'fill', 'filled', 'fills', 'fill_count', 'awarded_contracts', 'awarded_fill',
)
QUEUE_LABELS = ('q3300', 'q10000')
OUTSIDE_BIN = 'outside_pinned_bins'
SCHEMA_LABEL = 'SCHEMA_ONLY'
SCHEMA_VECTOR = 'schema_vector'
SCHEMA_FIXTURE = ROOT / 'fixtures' / 'schema_only_kxufcfight.json'
RESOLUTION_FIXTURE = ROOT / 'fixtures' / 'resolution_hook_not_admitted.json'
FROZEN_EXPERIMENT = ROOT / 'FROZEN_EXPERIMENT.json'
EMPTY_RESULTS = ROOT / 'results' / 'EMPTY_RESULTS.json'
SOURCE_PINS = ROOT / 'SOURCE_PINS.json'


class BakeoffError(Exception):
    """A schema row, a budget claim, or a scorecard claim was rejected."""


class LeeReadyRefused(BakeoffError):
    """Lee-Ready has no successful path. Native public taker_* fields are required."""


class TakerFieldRefused(BakeoffError):
    """The row has no agreeing native public taker_* field."""


class InventedFillRefused(BakeoffError):
    """A schema probe is not an awarded fill."""


class ScorecardRefused(BakeoffError):
    """results, pnl, MZ, and roi stay null until Clock ADMIT_PASS."""


class ClockRefused(BakeoffError):
    """Rejoin is kicked. Admit has not passed, so the scorecard stays null."""

    def __init__(self):
        super().__init__(
            'Clock NOT_ADMITTED; rejoin KICKED; reported settled N=4; '
            'awaiting CLOCK_ADMIT_PASS; results, pnl, MZ, and roi stay null'
        )


class SchemaOnlyRefused(BakeoffError):
    """The fixture is a schema sheet, not an admitted settled panel."""


class BudgetContrastRefused(BakeoffError):
    """The shared measurement label is 5000 USD on both arms."""


class MeasurementBudgetNotCapital(BakeoffError):
    """The 5000 USD label does not lock cash and does not fund an order."""

    def __init__(self):
        super().__init__('measurement budget is a contrast label, not spendable capital')


class StrategyPortRefused(BakeoffError):
    """000 is an instrument pointer. It is not ported onto KXUFCFIGHT."""

    def __init__(self):
        super().__init__('strategy port is refused')


class Q6RetuneRefused(BakeoffError):
    """This scaffold does not retune Q6 label 000."""

    def __init__(self):
        super().__init__('Q6 000 retune is refused')


class LiveOrdersForbidden(BakeoffError):
    """This lab has no live order path."""

    def __init__(self):
        super().__init__('no live orders and no account endpoint')


def _null_metrics():
    return {key: None for key in OUTPUT_KEYS}


def _sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def instrument_binding():
    """Pins for the scaffold. Rates stay inside the imported feebook stub."""
    table = feebook.load_series_table()
    terms = feebook.resolve_terms(table, SERIES_KXUFCFIGHT, 'taker')
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
        'rails_directory': RAILS_DIRECTORY,
        'rails_commit': RAILS_COMMIT,
        'rails_imported': True,
        'rails_copied': False,
        'examiner_formula_id': feebook.EXAMINER_FORMULA_ID,
        'fee_credit_rule_id': rails.FEE_CREDIT_RULE_ID,
        'series': SERIES_KXUFCFIGHT,
        'series_resolution': terms['resolution'],
        'series_override_added': SERIES_KXUFCFIGHT in (table.get('overrides') or {}),
        'arms': ARM_IDS,
        'measurement_budget_usd': MEASUREMENT_BUDGET_USD,
        'measurement_budget_role': BUDGET_ROLE,
        'strategy_claim': STRATEGY_CLAIM,
        'lee_ready': LEE_READY,
        'live_orders': LIVE_ORDERS,
        'q6_000_retune': Q6_000_RETUNE,
        'strategy_port': STRATEGY_PORT,
        'pinned_queue_labels': pinned_queue_labels(),
        'clock_rejoin': CLOCK_REJOIN,
        'awaiting': AWAITING_CLOCK,
        'reported_settled_n': REPORTED_SETTLED_N,
        'admitted_settled_n': ADMITTED_SETTLED_N,
        'events_finalized': EVENTS_FINALIZED,
        'scorecard_filled_from_reported_settles': False,
    }


def instrument_000_pointer():
    """Hash the Q6 shadow file. Do not parse it."""
    digest = _sha256(SHADOW_FILE)
    if digest != SHADOW_SHA256:
        raise BakeoffError('shadow hash')
    return {
        'instrument_id': INSTRUMENT_000,
        'shadow_file': 'nfl_factorial_lab_20260921/SHADOW_CANDIDATE_FREEZE.json',
        'shadow_sha256': digest,
        'parsed_shadow_json': False,
        'reads_common_config': False,
        'retune': False,
        'strategy_port': False,
        'measurement_budget_usd': MEASUREMENT_BUDGET_USD,
        'measurement_budget_role': BUDGET_ROLE,
        'strategy_claim': False,
    }


def dependency_hashes():
    """Byte hashes of the imported modules. This lab does not copy them."""
    return {
        'feebook_py_sha256': _sha256(FEEBOOK_DIR / 'feebook.py'),
        'rails_py_sha256': _sha256(RAILS_DIR / 'rails.py'),
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
        'clock_rejoin': CLOCK_REJOIN,
        'awaiting': AWAITING_CLOCK,
        'settled_n': SETTLED_N,
        'reported_settled_n': REPORTED_SETTLED_N,
        'admitted_settled_n': ADMITTED_SETTLED_N,
        'events_finalized': EVENTS_FINALIZED,
        'examiner': EXAMINER_STATUS,
        'winner': None,
    }
    stub.update(_null_metrics())
    return stub


def clock_admit(*_args, **_kwargs):
    """Admit stays closed. A passed token is not a Clock ADMIT_PASS."""
    raise ClockRefused()


def clock_rejoin():
    """The conductor kicked a rejoin. The kick does not open the scorecard."""
    record = {
        'clock_rejoin': CLOCK_REJOIN,
        'clock_admit': CLOCK_ADMIT,
        'awaiting': AWAITING_CLOCK,
        'reported_settled_n': REPORTED_SETTLED_N,
        'admitted_settled_n': ADMITTED_SETTLED_N,
        'events_finalized': EVENTS_FINALIZED,
        'admitted': False,
        'resolutions_applied': 0,
        'winner': None,
    }
    record.update(_null_metrics())
    return record


def apply_resolutions(*_args, **_kwargs):
    """Resolution values stay unwired until Clock ADMIT_PASS."""
    raise ClockRefused()


def mz(*args, **kwargs):
    """Mincer-Zarnowitz waits on Clock admit."""
    clock_admit(*args, **kwargs)


def roi(*args, **kwargs):
    """Return waits on Clock admit."""
    clock_admit(*args, **kwargs)


def write_scorecard(*_args, **_kwargs):
    """Refuse every scorecard fill. Admit has not passed."""
    raise ScorecardRefused(
        'Clock NOT_ADMITTED; awaiting CLOCK_ADMIT_PASS; '
        'results, pnl, MZ, and roi stay null'
    )


def spend_measurement_budget(*_args, **_kwargs):
    """The shared 5000 USD figure is not cash that can be spent."""
    raise MeasurementBudgetNotCapital()


def port_strategy(*_args, **_kwargs):
    """Do not port the 000 strategy onto a UFC fight."""
    raise StrategyPortRefused()


def retune_000(*_args, **_kwargs):
    """Do not retune Q6 label 000."""
    raise Q6RetuneRefused()


def lee_ready(*_args, **_kwargs):
    """Quote test and tick test are refused for every input."""
    raise LeeReadyRefused(
        'Lee-Ready is refused; native public taker_* fields are required'
    )


def _require_row(row):
    if not isinstance(row, dict):
        raise TypeError('row')
    return row


def _lee_ready_requested(row):
    if 'lee_ready' in row and row['lee_ready'] is not False and row['lee_ready'] is not None:
        return True
    classifier = row.get('classifier')
    if isinstance(classifier, str) and classifier.lower().replace('_', '-') in (
        'lee-ready', 'leeready',
    ):
        return True
    return False


def _agree(current, value):
    if current is None:
        return value
    if current != value:
        raise TakerFieldRefused('taker_* fields disagree')
    return current


def _has_native_taker(row):
    return any(row.get(key) is not None for key in PUBLIC_TAKER_FIELDS)


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
        book_side = row['taker_book_side']
        if book_side not in BOOK_TO_OUTCOME:
            raise TakerFieldRefused('taker_book_side')
        outcome = _agree(outcome, BOOK_TO_OUTCOME[book_side])
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


def _reject_invented_fill(row):
    for key in FILL_KEYS:
        if key in row and row[key] is not None:
            raise InventedFillRefused(key)


def _series(row, arm):
    if 'series' in row:
        series = row['series']
    else:
        series = arm.get('series')
    if series is not None and (not isinstance(series, str) or series.strip() == ''):
        raise TypeError('series')
    if series != arm.get('series'):
        raise ValueError('series')
    return series


def _contracts(row):
    present = []
    for key in ('schema_probe_contracts', 'count_fp', 'count'):
        if key in row and row[key] is not None:
            present.append(feebook.as_decimal(row[key], key))
    if not present:
        raise ValueError('schema_probe_contracts')
    if any(value != present[0] for value in present):
        raise ValueError('contract counts disagree')
    if present[0] <= 0:
        raise ValueError('contracts')
    return present[0]


def pinned_queue_labels():
    """Rails scenario magnitudes. This lab does not restate the sizes."""
    return {label: rails.scenario_queue(label) for label in QUEUE_LABELS}


def queue_label(queue_ahead, assumed_scenario=None, *, is_observation=False):
    """Exact match to a pinned rails scenario. Absent ahead stays null.

    A schema vector is not an observed queue. The observation flag does not
    award a fill.
    """
    if not isinstance(is_observation, bool):
        raise TypeError('queue_ahead_is_observation')
    pinned = pinned_queue_labels()
    if queue_ahead is None:
        return {
            'observed_queue_ahead': None,
            'queue_attribution_bin': None,
            'assumed_scenario': None,
            'queue_bin_mismatch': None,
            'pinned_scenarios': pinned,
            'queue_ahead_is_observation': False,
            'awarded_fill': None,
        }
    ahead = feebook.as_decimal(queue_ahead, 'queue_ahead')
    if ahead < 0:
        raise ValueError('queue_ahead')
    attributed = OUTSIDE_BIN
    for label, magnitude in pinned.items():
        if ahead == magnitude:
            attributed = label
            break
    mismatch = None
    if assumed_scenario is not None:
        if assumed_scenario not in pinned:
            raise ValueError('assumed_scenario')
        mismatch = attributed != assumed_scenario
    observed = ahead if is_observation else None
    return {
        'observed_queue_ahead': observed,
        'queue_attribution_bin': attributed,
        'assumed_scenario': assumed_scenario,
        'queue_bin_mismatch': mismatch,
        'pinned_scenarios': pinned,
        'queue_ahead_is_observation': is_observation,
        'awarded_fill': None,
    }


def maker_credit_label(price, contracts, series=None, table=None):
    """R1-P5 maker-credit admission. The label does not place an order."""
    try:
        evaluation = rails.admit_maker_quote(
            price, contracts, series=series, table=table,
        )
        refused = False
    except rails.MakerCreditRefused as exc:
        evaluation = exc.evaluation
        refused = True
    if evaluation['rule_id'] != rails.FEE_CREDIT_RULE_ID:
        raise BakeoffError('fee credit rule')
    if evaluation['fee_quote']['formula_id'] != feebook.EXAMINER_FORMULA_ID:
        raise BakeoffError('examiner formula')
    return {
        'maker_credit_floor_zero_refuse': refused,
        'admitted': evaluation['admitted'],
        'credit': evaluation['credit'],
        'fee': evaluation['fee'],
        'rule_id': evaluation['rule_id'],
        'formula_id': evaluation['fee_quote']['formula_id'],
        'placed_order': False,
    }


class FreshnessCursor:
    """Last fresh book. A keepalive does not move the anchor."""

    def __init__(self):
        self.previous = None

    def observe(self, orderbook_fp, transaction_time, keepalive):
        if not isinstance(keepalive, bool):
            raise TypeError('keepalive')
        content = rails.canonical_book_content(orderbook_fp)
        current = rails.BookObservation(content, transaction_time)
        verdict = rails.judge_freshness(self.previous, current, keepalive=keepalive)
        if verdict.fresh:
            self.previous = current
        return {
            'content_fresh_flag': verdict.fresh,
            'reason': verdict.reason,
        }


def _blank_label(schema_id, series):
    label = {
        'schema_id': schema_id,
        'label': SCHEMA_LABEL,
        'series': series,
        'taker_outcome_side': None,
        'maker_outcome_side': None,
        'taker_book_side': None,
        'native_fields': [],
        'classification': None,
        'ignored_quote_fields': [],
        'contracts': None,
        'taker_quote': None,
        'maker_quote': None,
        'formula_id': None,
        'fee_channel': None,
        'series_resolution': None,
        'maker_credit': None,
        'freshness': None,
        'queue': None,
        'size_exceeds_touch': None,
        'awarded_fill': None,
        'scorecard_label': None,
        'placed_order': False,
        'lee_ready': None,
        'winner': None,
    }
    label.update(_null_metrics())
    return label


def label_schema_row(row, arm, cursor, table=None):
    """One schema label. Fees are probes. Fills, MZ, and ROI stay unset."""
    row = _require_row(row)
    if row.get('schema_only') is not True:
        raise SchemaOnlyRefused('schema_only')
    if _lee_ready_requested(row):
        raise LeeReadyRefused(
            'Lee-Ready is refused; native public taker_* fields are required'
        )
    _reject_invented_fill(row)
    _reject_settled(row)
    if table is None:
        table = feebook.load_series_table()
    series = _series(row, arm)
    label = _blank_label(row.get('schema_id'), series)
    label['ignored_quote_fields'] = [key for key in QUOTE_FIELDS if key in row]
    keepalive = row.get('keepalive', False)
    if not isinstance(keepalive, bool):
        raise TypeError('keepalive')
    if 'orderbook_fp' in row:
        if 'transaction_time' not in row:
            raise ValueError('transaction_time')
        label['freshness'] = cursor.observe(
            row['orderbook_fp'], row['transaction_time'], keepalive,
        )
    if 'queue_ahead' in row and row['queue_ahead'] is not None:
        role = row.get('queue_ahead_role', SCHEMA_VECTOR)
        if role != SCHEMA_VECTOR:
            raise ValueError('queue_ahead_role')
        observation = row.get('queue_ahead_is_observation', False)
        if observation is True:
            raise SchemaOnlyRefused('queue observation is not in this fixture')
        label['queue'] = queue_label(
            row['queue_ahead'],
            row.get('assumed_scenario'),
            is_observation=False,
        )
    if keepalive:
        return label
    classified = None
    if _has_native_taker(row):
        classified = classify_taker(row)
        label['taker_outcome_side'] = classified['taker_outcome_side']
        label['maker_outcome_side'] = classified['maker_outcome_side']
        label['taker_book_side'] = classified['taker_book_side']
        label['native_fields'] = classified['native_fields']
        label['classification'] = classified['classification']
    if classified is None:
        return label
    if 'orderbook_fp' not in row:
        raise ValueError('orderbook_fp')
    contracts = _contracts(row)
    probe = feebook.polarity_fill(
        {'orderbook_fp': row['orderbook_fp']},
        classified['taker_outcome_side'],
        contracts,
        round_up=True,
        series=series,
        table=table,
    )
    if probe['taker_fee']['formula_id'] != feebook.EXAMINER_FORMULA_ID:
        raise BakeoffError('examiner formula')
    if probe['maker_fee']['formula_id'] != feebook.EXAMINER_FORMULA_ID:
        raise BakeoffError('examiner formula')
    channel = feebook.examiner_fee_channel(probe['taker_fee'], probe['maker_fee'])
    label['contracts'] = contracts
    label['taker_quote'] = probe['taker_fee']
    label['maker_quote'] = probe['maker_fee']
    label['formula_id'] = channel['formula_id']
    label['fee_channel'] = channel
    label['series_resolution'] = probe['taker_fee']['series_resolution']
    label['size_exceeds_touch'] = probe['size_exceeds_touch']
    label['maker_credit'] = maker_credit_label(
        probe['maker_price'], contracts, series=series, table=table,
    )
    label['awarded_fill'] = None
    label['scorecard_label'] = None
    return label


def _budget(value, name):
    amount = feebook.as_decimal(value, name)
    if amount != MEASUREMENT_BUDGET_USD:
        raise BudgetContrastRefused('measurement budget')
    return amount


def load_schema_fixture(path=None):
    """Read the schema sheet. An admitted panel is rejected."""
    if path is None:
        path = SCHEMA_FIXTURE
    payload = json.loads(Path(path).read_text())
    if payload.get('packet_id') != PACKET_ID:
        raise ValueError('packet_id')
    if payload.get('label') != SCHEMA_LABEL:
        raise SchemaOnlyRefused('label')
    if payload.get('admitted_settled_panel') is not False:
        raise SchemaOnlyRefused('admitted settled panel')
    if payload.get('invented_fills') is not False:
        raise InventedFillRefused('fixture')
    if payload.get('panel_version') != PANEL_VERSION:
        raise ValueError('panel_version')
    if payload.get('collector') != COLLECTOR_STATUS:
        raise ValueError('collector')
    if payload.get('clock') != CLOCK_ADMIT:
        raise ValueError('clock')
    if payload.get('clock_rejoin') != CLOCK_REJOIN:
        raise ValueError('clock_rejoin')
    if payload.get('awaiting') != AWAITING_CLOCK:
        raise ClockRefused()
    if payload.get('reported_settled_n') != REPORTED_SETTLED_N:
        raise ValueError('reported_settled_n')
    if payload.get('admitted_settled_n') != ADMITTED_SETTLED_N:
        raise ClockRefused()
    if payload.get('events_finalized') != EVENTS_FINALIZED:
        raise ValueError('events_finalized')
    if payload.get('settled_n') != SETTLED_N:
        raise ClockRefused()
    if payload.get('series') != SERIES_KXUFCFIGHT:
        raise ValueError('series')
    if payload.get('measurement_budget_role') != BUDGET_ROLE:
        raise BudgetContrastRefused('role')
    if payload.get('strategy_claim') is not False:
        raise StrategyPortRefused()
    if payload.get('winner') is not None:
        raise ScorecardRefused('winner')
    _budget(payload.get('measurement_budget_usd'), 'measurement_budget_usd')
    arms = payload.get('arms')
    if not isinstance(arms, list) or len(arms) != 2:
        raise ValueError('arms')
    seen = []
    for arm in arms:
        if not isinstance(arm, dict):
            raise TypeError('arm')
        arm_id = arm.get('arm_id')
        if arm_id not in ARM_IDS or arm_id in seen:
            raise ValueError('arm_id')
        seen.append(arm_id)
        if arm.get('measurement_budget_role') != BUDGET_ROLE:
            raise BudgetContrastRefused('arm role')
        _budget(arm.get('measurement_budget_usd'), 'arm measurement_budget_usd')
        if arm_id == SERIES_KXUFCFIGHT:
            if arm.get('series') != SERIES_KXUFCFIGHT:
                raise ValueError('series')
            if arm.get('kind') != 'ml_binary':
                raise ValueError('kind')
        if arm_id == INSTRUMENT_000:
            if arm.get('series') is not None:
                raise ValueError('000 series')
            if arm.get('instrument_id') != INSTRUMENT_000:
                raise ValueError('instrument_id')
            if arm.get('retune') is not False:
                raise Q6RetuneRefused()
        rows = arm.get('rows')
        if not isinstance(rows, list) or not rows:
            raise ValueError('rows')
        for row in rows:
            if not isinstance(row, dict) or row.get('schema_only') is not True:
                raise SchemaOnlyRefused('schema_only')
            if row.get('queue_ahead_is_observation') is True:
                raise SchemaOnlyRefused('queue observation is not in this fixture')
    if seen != list(ARM_IDS):
        raise ValueError('arm order')
    return payload


def walk_schema(path=None, table=None):
    """Label both arms. Refusals carry no fill and no scorecard."""
    payload = load_schema_fixture(path)
    if table is None:
        table = feebook.load_series_table()
    if table.get('overrides'):
        raise BakeoffError('series override')
    arms_out = []
    for arm in payload['arms']:
        cursor = FreshnessCursor()
        labeled = []
        refused = []
        for row in arm['rows']:
            try:
                labeled.append(label_schema_row(row, arm, cursor, table=table))
            except (
                LeeReadyRefused,
                TakerFieldRefused,
                InventedFillRefused,
                ScorecardRefused,
                feebook.BookIncomplete,
            ) as exc:
                refusal = {
                    'schema_id': row.get('schema_id'),
                    'reason': exc.__class__.__name__,
                    'awarded_fill': None,
                    'winner': None,
                    'lee_ready': None,
                }
                refusal.update(_null_metrics())
                refused.append(refusal)
        arm_out = {
            'arm_id': arm['arm_id'],
            'kind': arm['kind'],
            'series': arm['series'],
            'series_resolution': feebook.resolve_terms(
                table, arm['series'], 'taker',
            )['resolution'],
            'instrument_id': arm['instrument_id'],
            'measurement_budget_usd': MEASUREMENT_BUDGET_USD,
            'measurement_budget_role': BUDGET_ROLE,
            'strategy_claim': False,
            'retune': False,
            'labeled': labeled,
            'refusals': refused,
            'awarded_fill': None,
            'observed_queue_ahead': None,
            'queue_bin_mismatch_rate': None,
            'winner': None,
        }
        arm_out.update(_null_metrics())
        arms_out.append(arm_out)
    if arms_out[0]['measurement_budget_usd'] != arms_out[1]['measurement_budget_usd']:
        raise BudgetContrastRefused('arms differ')
    walked = {
        'label': SCHEMA_LABEL,
        'packet_id': PACKET_ID,
        'admitted_settled_panel': False,
        'panel_version': payload['panel_version'],
        'collector': COLLECTOR_STATUS,
        'clock': CLOCK_ADMIT,
        'clock_rejoin': CLOCK_REJOIN,
        'awaiting': AWAITING_CLOCK,
        'settled_n': SETTLED_N,
        'reported_settled_n': REPORTED_SETTLED_N,
        'admitted_settled_n': ADMITTED_SETTLED_N,
        'events_finalized': EVENTS_FINALIZED,
        'examiner': EXAMINER_STATUS,
        'measurement_budget_usd': MEASUREMENT_BUDGET_USD,
        'measurement_budget_role': BUDGET_ROLE,
        'strategy_claim': False,
        'same_measurement_budget': True,
        'arms': arms_out,
        'lee_ready': None,
        'winner': None,
        'status': SCHEMA_LABEL,
    }
    walked.update(_null_metrics())
    return walked


def load_resolution_hook(path=None):
    """Read the not-admitted placeholder. A stored resolution is refused."""
    if path is None:
        path = RESOLUTION_FIXTURE
    payload = json.loads(Path(path).read_text())
    if payload.get('packet_id') != PACKET_ID:
        raise ValueError('packet_id')
    if payload.get('label') != RESOLUTION_LABEL:
        raise ClockRefused()
    if payload.get('awaiting') != AWAITING_CLOCK:
        raise ClockRefused()
    if payload.get('clock_rejoin') != CLOCK_REJOIN:
        raise ValueError('clock_rejoin')
    if payload.get('clock_admit') != CLOCK_ADMIT:
        raise ClockRefused()
    if payload.get('collector') != COLLECTOR_STATUS:
        raise ValueError('collector')
    if payload.get('panel_version') != PANEL_VERSION:
        raise ValueError('panel_version')
    if payload.get('reported_settled_n') != REPORTED_SETTLED_N:
        raise ValueError('reported_settled_n')
    if payload.get('admitted_settled_n') != ADMITTED_SETTLED_N:
        raise ClockRefused()
    if payload.get('events_finalized') != EVENTS_FINALIZED:
        raise ValueError('events_finalized')
    if payload.get('admitted_settled_panel') is not False:
        raise ClockRefused()
    if payload.get('series') != SERIES_KXUFCFIGHT:
        raise ValueError('series')
    for key in OUTPUT_KEYS:
        if payload.get(key) is not None:
            raise ScorecardRefused(key)
    if payload.get('winner') is not None:
        raise ScorecardRefused('winner')
    slots = payload.get('slots')
    if not isinstance(slots, list) or len(slots) != REPORTED_SETTLED_N:
        raise ValueError('slots')
    seen = set()
    per_event = {}
    for slot in slots:
        if not isinstance(slot, dict):
            raise TypeError('slot')
        slot_id = slot.get('slot_id')
        if not isinstance(slot_id, str) or slot_id == '' or slot_id in seen:
            raise ValueError('slot_id')
        seen.add(slot_id)
        event_index = slot.get('event_index')
        contract_index = slot.get('contract_index')
        if event_index not in (1, 2) or contract_index not in (1, 2):
            raise ValueError('slot index')
        per_event.setdefault(event_index, set()).add(contract_index)
        if slot.get('series') != SERIES_KXUFCFIGHT:
            raise ValueError('series')
        if slot.get('resolution') is not None or slot.get('result') is not None:
            raise ClockRefused()
        for key in ('pnl', 'roi', 'MZ', 'mz', 'winner'):
            if key in slot and slot[key] is not None:
                raise ScorecardRefused(key)
    if set(per_event) != {1, 2}:
        raise ValueError('events')
    for indexes in per_event.values():
        if indexes != {1, 2}:
            raise ValueError('contracts')
    return payload


def wire_resolution_hook(path=None):
    """Name the empty slots. Apply none of them to the scorecard."""
    payload = load_resolution_hook(path)
    wired = {
        'label': RESOLUTION_LABEL,
        'awaiting': AWAITING_CLOCK,
        'clock_rejoin': CLOCK_REJOIN,
        'clock_admit': CLOCK_ADMIT,
        'reported_settled_n': REPORTED_SETTLED_N,
        'admitted_settled_n': ADMITTED_SETTLED_N,
        'events_finalized': EVENTS_FINALIZED,
        'slot_ids': [slot['slot_id'] for slot in payload['slots']],
        'resolutions_applied': 0,
        'admitted': False,
        'admitted_settled_panel': False,
        'winner': None,
    }
    wired.update(_null_metrics())
    return wired


def empty_outputs():
    """The empty-file contract. Schema walks do not fill it."""
    payload = {
        'settled_n': SETTLED_N,
        'reported_settled_n': REPORTED_SETTLED_N,
        'admitted_settled_n': ADMITTED_SETTLED_N,
        'events_finalized': EVENTS_FINALIZED,
        'clock': CLOCK_ADMIT,
        'clock_rejoin': CLOCK_REJOIN,
        'awaiting': AWAITING_CLOCK,
        'collector': COLLECTOR_STATUS,
        'panel_version': PANEL_VERSION,
        'measurement_budget_usd': format(MEASUREMENT_BUDGET_USD, 'f'),
        'measurement_budget_role': BUDGET_ROLE,
        'strategy_claim': False,
        'status': 'EMPTY',
        'winner': None,
    }
    payload.update(_null_metrics())
    return payload


def frozen_output_snapshot():
    """Read the freeze file. Does not modify it."""
    payload = json.loads(FROZEN_EXPERIMENT.read_text())
    snapshot = {key: payload[key] for key in OUTPUT_KEYS}
    snapshot['winner'] = payload['winner']
    return snapshot
