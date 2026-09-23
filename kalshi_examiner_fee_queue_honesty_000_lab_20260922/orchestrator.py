"""One Examiner channel for Q6-000 fee hygiene and queue fragility.

This module imports the pick A join and the pick B join. It does not edit
feebook, rails, hygiene.py, or queue_fragility.py. It does not place live
orders, does not retune Q6-000, and does not write scorecard metrics.
"""
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PARENT = ROOT.parent
LAB_DIRECTORY = 'kalshi_examiner_fee_queue_honesty_000_lab_20260922'
HYGIENE_LAB = 'kalshi_r2p1_hygiene_000_lab_20260922'
QF_LAB = 'kalshi_queue_fragility_000_lab_20260922'
HYGIENE_FIXTURE_JOIN = PARENT / HYGIENE_LAB / 'fixture_join.py'
QF_FIXTURE_JOIN = PARENT / QF_LAB / 'fixture_join.py'

EXPERIMENT_ID = 'examiner_fee_queue_honesty_000_20260922'
STRATEGY_POINTER = 'Q6-000'
FEEBOOK_COMMIT = '22371178cb2663250b4762f328069571c48cb551'
RAILS_COMMIT = '6a28e0d6254327ea4e6451c781bec56215ac6cac'
HYGIENE_JOIN_COMMIT = '79800a82b8ad2c1e10f614f69fd7105d11e0d041'
QF_JOIN_COMMIT = '7026be5104cd00cabcf9b34154506a76b2768b8a'
PACKET = PARENT / 'packets' / 'EXAMINER_FEE_QUEUE_HONESTY_000_FREEZE_2026-09-22.md'
PACKET_SHA256 = '4799642e54cf233a925697e00c5a9e29f5cb39070962a2e011f0fbe090c169f2'
PACKET_DIR = PARENT / 'packets' / 'EXAMINER_FEE_QUEUE_HONESTY_000'
PACKET_RESULTS = PACKET_DIR / 'results.json'
PACKET_FROZEN = PACKET_DIR / 'FROZEN_EXPERIMENT.json'
PACKET_KERNEL = PACKET_DIR / 'freeze.json'
FROZEN_EXPERIMENT = ROOT / 'FROZEN_EXPERIMENT.json'
EMPTY_RESULTS = ROOT / 'results' / 'EMPTY_RESULTS.json'
PRIMARY_FILLS_REL = 'nfl_factorial_lab_20260921/results/q3300_d0.25_000_fills.jsonl.gz'
PRIMARY_ORDERS_REL = 'nfl_factorial_lab_20260921/results/q3300_d0.25_000_orders.jsonl.gz'
PRIMARY_FILLS_SHA256 = '9d56f5d3c599e092606be9f4a1ad41ae8baabff4921d3d722adf0b57ac944a3f'
PRIMARY_ORDERS_SHA256 = 'c390801b9a7cf6d182d2d097123ed944792980524a7975e6e59a904a530f4b1c'
SHADOW_FREEZE = PARENT / 'nfl_factorial_lab_20260921' / 'SHADOW_CANDIDATE_FREEZE.json'
SHADOW_FREEZE_SHA256 = 'b55ff36cb161c824a3d1b490795c8ac6891f01489456f61da311ac863366af48'
STRESS_ROLE = 'queue_label_only_not_a_fee_knob'
CAPITAL_MODE = 'A1_shared_pool'
FEE_CHANNEL = 'fee'
QUEUE_CHANNEL = 'queue'
# Value types describe a later Examiner fill. This harness stores None.
# The two queue maps are arm to Decimal, the same shape the QF join would
# publish. participation_stress_gap is one Decimal, as are the fee fields.
# None of those aggregates are computed here.
DECIMAL_TYPE = 'Decimal'
ARM_DECIMAL_MAP_TYPE = 'mapping[arm, Decimal]'
SCORECARD_SCHEMA = (
    ('fee_delta_vs_inherited_model', FEE_CHANNEL, DECIMAL_TYPE),
    ('freshness_gap_sec', FEE_CHANNEL, DECIMAL_TYPE),
    ('queue_bin_mismatch_rate', FEE_CHANNEL, DECIMAL_TYPE),
    ('fill_rate_delta_vs_q3300', QUEUE_CHANNEL, ARM_DECIMAL_MAP_TYPE),
    ('adverse_queue_exposure', QUEUE_CHANNEL, ARM_DECIMAL_MAP_TYPE),
    ('participation_stress_gap', QUEUE_CHANNEL, DECIMAL_TYPE),
)
OUTPUT_KEYS = tuple(name for name, _channel, _value_type in SCORECARD_SCHEMA) + (
    'results',
    'pnl',
)


class OrchestratorError(Exception):
    """The two joins disagreed, or a scorecard write was requested."""


class ScorecardPromotionRefused(OrchestratorError):
    """Filled scorecard metrics stay out of the freeze packet."""

    def __init__(self):
        super().__init__('scorecard metrics stay null until Examiner-ready')


class LiveOrdersForbidden(OrchestratorError):
    """This lab has no live order path."""

    def __init__(self):
        super().__init__('no live orders and no KalshiExecutionAdapter')


def _load_join(module_name, path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise OrchestratorError('join import')
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


hygiene_join = _load_join('examiner_hygiene_fixture_join', HYGIENE_FIXTURE_JOIN)
qf_join = _load_join('examiner_qf_fixture_join', QF_FIXTURE_JOIN)
import queue_fragility as queue_fragility_core


def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def execution_adapter():
    """No live order client lives in this lab."""
    raise LiveOrdersForbidden()


def shared_capital(mode=CAPITAL_MODE):
    """One shared 5000 USD pool. A2 and A3 are refused by the QF core."""
    return queue_fragility_core.shared_capital(mode)


def instrument_binding():
    """Both joins, one fee commit, one rails commit, one strategy pointer."""
    hygiene_binding = hygiene_join.instrument_binding()
    qf_binding = qf_join.instrument_binding()
    if hygiene_binding['feebook_commit'] != FEEBOOK_COMMIT:
        raise OrchestratorError('feebook commit')
    if qf_binding['feebook_commit'] != FEEBOOK_COMMIT:
        raise OrchestratorError('feebook commit')
    if hygiene_binding['rails_commit'] != RAILS_COMMIT:
        raise OrchestratorError('rails commit')
    if qf_binding['rails_commit'] != RAILS_COMMIT:
        raise OrchestratorError('rails commit')
    if hygiene_binding['examiner_formula_id'] != qf_binding['examiner_formula_id']:
        raise OrchestratorError('examiner formula')
    if hygiene_binding['strategy_pointer'] != STRATEGY_POINTER:
        raise OrchestratorError('strategy pointer')
    if qf_binding['strategy_pointer'] != STRATEGY_POINTER:
        raise OrchestratorError('strategy pointer')
    if hygiene_join.HYGIENE_LAB_MERGE is None:
        raise OrchestratorError('hygiene join')
    capital = shared_capital()
    return {
        'experiment_id': EXPERIMENT_ID,
        'lab_directory': LAB_DIRECTORY,
        'single_examiner_packet': True,
        'strategy_pointer': STRATEGY_POINTER,
        'feebook_commit': FEEBOOK_COMMIT,
        'rails_commit': RAILS_COMMIT,
        'hygiene_join': str(HYGIENE_FIXTURE_JOIN.relative_to(PARENT)),
        'hygiene_join_commit': HYGIENE_JOIN_COMMIT,
        'qf_join': str(QF_FIXTURE_JOIN.relative_to(PARENT)),
        'qf_join_commit': QF_JOIN_COMMIT,
        'hygiene_binding': hygiene_binding,
        'qf_binding': qf_binding,
        'examiner_formula_id': hygiene_binding['examiner_formula_id'],
        'capital': capital,
        'live_orders': False,
        'signal_retune': False,
        'forbid_capital_A2_A3': True,
        'forbid_000_retune': True,
        'fee_is_knob': False,
        'stress_role': STRESS_ROLE,
        'fee_fields': channel_fields(FEE_CHANNEL),
        'queue_fields': channel_fields(QUEUE_CHANNEL),
    }


def channel_fields(channel):
    """Names and value types for one side of the single scorecard."""
    if channel not in (FEE_CHANNEL, QUEUE_CHANNEL):
        raise OrchestratorError('channel')
    fields = tuple(
        (name, value_type)
        for name, owner, value_type in SCORECARD_SCHEMA
        if owner == channel
    )
    if len(fields) != 3:
        raise OrchestratorError('channel width')
    return fields


def published_scorecard():
    """The freeze outputs. Fee and queue fields are present and null."""
    scorecard = {key: None for key in OUTPUT_KEYS}
    for name, _channel, _value_type in SCORECARD_SCHEMA:
        if name not in scorecard or scorecard[name] is not None:
            raise ScorecardPromotionRefused()
    scorecard['status'] = 'NOT_SCORED'
    scorecard['single_examiner_packet'] = True
    scorecard['fee_fields'] = channel_fields(FEE_CHANNEL)
    scorecard['queue_fields'] = channel_fields(QUEUE_CHANNEL)
    return scorecard


def assert_null_scorecard(payload):
    """Require every fee field and every queue field, and require null.

    A missing queue field is the same refusal as a missing fee field or a
    filled value. This harness does not treat queue keys as optional.
    """
    if not isinstance(payload, dict):
        raise ScorecardPromotionRefused()
    for key in OUTPUT_KEYS:
        if key not in payload or payload[key] is not None:
            raise ScorecardPromotionRefused()
    return payload


def write_scorecard(payload):
    """Refuse a missing or non-null scorecard field. Nothing is written."""
    assert_null_scorecard(payload)
    raise ScorecardPromotionRefused()


def stress_pin():
    """Harsh twin paths. The default channel does not open them."""
    left = hygiene_join.stress_pin()
    right = qf_join.stress_pin()
    if left['fills'] != right['fills'] or left['orders'] != right['orders']:
        raise OrchestratorError('stress pin')
    if left['loaded'] or right['loaded']:
        raise OrchestratorError('stress loaded')
    if left['role'] != STRESS_ROLE or right['role'] != STRESS_ROLE:
        raise OrchestratorError('stress role')
    return {
        'fills': left['fills'],
        'orders': left['orders'],
        'fills_sha256': left['fills_sha256'],
        'orders_sha256': right['orders_sha256'],
        'role': STRESS_ROLE,
        'loaded': False,
    }


def resolve_primary():
    """One fills stream for both joins.

    Production gzip when both pinned files exist and both joins accept the
    sha256. Otherwise one synthetic pair that both joins can read. The
    published scorecard stays null either way.
    """
    hygiene_choice = hygiene_join.resolve_primary()
    qf_choice = qf_join.resolve_primary()
    if bool(hygiene_choice['production_present']) != bool(qf_choice['production_present']):
        raise OrchestratorError('production presence')
    if hygiene_choice['production_present']:
        if hygiene_choice['source'] != 'production_pin' or qf_choice['source'] != 'production_pin':
            raise OrchestratorError('production source')
        if Path(hygiene_choice['fills_path']) != Path(qf_choice['fills_path']):
            raise OrchestratorError('fills path')
        if Path(hygiene_choice['orders_path']) != Path(qf_choice['orders_path']):
            raise OrchestratorError('orders path')
        if hygiene_join.PRIMARY_FILLS_SHA256 != PRIMARY_FILLS_SHA256:
            raise OrchestratorError('fills sha256')
        if qf_join.PRIMARY_ORDERS_SHA256 != PRIMARY_ORDERS_SHA256:
            raise OrchestratorError('orders sha256')
        return {
            'source': 'production_pin',
            'fills_path': Path(hygiene_choice['fills_path']),
            'orders_path': Path(hygiene_choice['orders_path']),
            'production_present': True,
        }
    return {
        'source': 'synthetic_schema_standin',
        'fills_path': qf_join.SYNTHETIC_FILLS,
        'orders_path': qf_join.SYNTHETIC_ORDERS,
        'production_present': False,
    }


def ledger_identity(path):
    """Both joins must agree. The strategy label is 000."""
    left = hygiene_join.ledger_identity(path)
    right = qf_join.ledger_identity(path)
    if left != right:
        raise OrchestratorError('ledger identity')
    if left['strategy_label'] != '000':
        raise OrchestratorError('strategy label')
    return left


def conduct(choice=None):
    """Run both joins on one fill path and one order path.

    Child reports keep their in-memory labels. This report's scorecard keys
    stay null. Nothing is written to the freeze files.
    """
    if choice is None:
        choice = resolve_primary()
    fills_path = Path(choice['fills_path'])
    orders_path = Path(choice['orders_path'])
    source = choice['source']
    if source not in ('production_pin', 'synthetic_schema_standin'):
        raise OrchestratorError('source')
    if choice.get('production_present') and source != 'production_pin':
        raise OrchestratorError('production source')
    hygiene_report = hygiene_join.join_ledgers(fills_path, orders_path, source=source)
    qf_report = qf_join.join_ledgers(fills_path, orders_path, source=source)
    if hygiene_report['row_count'] != qf_report['row_count']:
        raise OrchestratorError('row count')
    if hygiene_report['maker_rows'] != qf_report['maker_rows']:
        raise OrchestratorError('maker rows')
    if hygiene_report['taker_rows'] != qf_report['taker_rows']:
        raise OrchestratorError('taker rows')
    if hygiene_report['strategy_label'] != '000' or qf_report['strategy_label'] != '000':
        raise OrchestratorError('strategy label')
    if hygiene_report['assumed_scenario'] != qf_report['assumed_scenario']:
        raise OrchestratorError('assumed scenario')
    if Path(hygiene_report['fills_path']) != fills_path:
        raise OrchestratorError('fills path')
    if Path(qf_report['fills_path']) != fills_path:
        raise OrchestratorError('fills path')
    if Path(hygiene_report['orders_path']) != orders_path:
        raise OrchestratorError('orders path')
    if Path(qf_report['orders_path']) != orders_path:
        raise OrchestratorError('orders path')
    hygiene_join.assert_null_scorecard(hygiene_report['published'])
    qf_join.assert_null_scorecard(qf_report['published'])
    if not qf_report['arms_run'] or tuple(qf_report['arms_run']) != tuple(queue_fragility_core.ARMS):
        raise OrchestratorError('queue arms')
    published = assert_null_scorecard(published_scorecard())
    channels = {
        FEE_CHANNEL: {
            'wired': True,
            'fields': channel_fields(FEE_CHANNEL),
            'row_count': hygiene_report['row_count'],
        },
        QUEUE_CHANNEL: {
            'wired': True,
            'fields': channel_fields(QUEUE_CHANNEL),
            'row_count': qf_report['row_count'],
        },
    }
    if channels[FEE_CHANNEL]['row_count'] != channels[QUEUE_CHANNEL]['row_count']:
        raise OrchestratorError('row count')
    report = {
        'experiment_id': EXPERIMENT_ID,
        'source': source,
        'fills_path': str(fills_path),
        'orders_path': str(orders_path),
        'production_present': bool(choice.get('production_present')),
        'strategy_label': '000',
        'assumed_scenario': hygiene_report['assumed_scenario'],
        'row_count': hygiene_report['row_count'],
        'maker_rows': hygiene_report['maker_rows'],
        'taker_rows': hygiene_report['taker_rows'],
        'hygiene_join': hygiene_report,
        'qf_join': qf_report,
        'channels': channels,
        'published': published,
        'promoted': False,
        'single_examiner_packet': True,
        'stress': stress_pin(),
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
        'packet_frozen': json.loads(PACKET_FROZEN.read_text()),
    }
    snapshot = {}
    for name, payload in payloads.items():
        for key in OUTPUT_KEYS:
            if key not in payload or payload[key] is not None:
                raise ScorecardPromotionRefused()
            snapshot['%s.%s' % (name, key)] = None
    packet_results = json.loads(PACKET_RESULTS.read_text())
    for key in ('results', 'pnl', 'metrics'):
        if packet_results.get(key) is not None:
            raise ScorecardPromotionRefused()
        snapshot['packet_results.%s' % key] = None
    return snapshot
