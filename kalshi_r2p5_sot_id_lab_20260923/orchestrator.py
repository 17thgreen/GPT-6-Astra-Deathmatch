"""R2-P5 SOT-ID kickoff SoT and holdout identity audit.

Measurement only. Imports the R1-P1 feebook and the R1-P5 rails as pin
references. Adverse hedge fields stay null unless external odds are present.
This module does not edit those labs, does not place orders, does not read
Logan keys, does not run admit.py, does not open a second ADMIT-1 panel,
does not steal the ADMIT-1 poll, and does not write scorecard metrics.

The checkout freeze, parent accept, ADMIT-1 seed, JSON schema, and PIT@CLE
identity cite match the attached conductor sha256 values. The seed has 16
rows, all kalshi_occurrence, delta_kickoff_sec 10800. A labeled recreation
and an empty seed are refused. Invented odds and holdout rewrites are refused.
"""
import hashlib
import importlib.util
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PARENT = ROOT.parent
FEEBOOK_DIR = PARENT / 'kalshi_feebook_lab_20260922'
RAILS_DIR = PARENT / 'kalshi_rails_lab_20260922'
HYGIENE_PATH = PARENT / 'kalshi_r2p1_hygiene_000_lab_20260922' / 'hygiene.py'
for _path in (FEEBOOK_DIR, RAILS_DIR):
    if str(_path) not in sys.path:
        sys.path.insert(0, str(_path))

import feebook
import rails

LAB_DIRECTORY = 'kalshi_r2p5_sot_id_lab_20260923'
EXPERIMENT_ID = 'R2-P5-SOT-ID-HARNESS'
FEATURE_FAMILY = 'SOT-ID'
SCHEMA_ID = 'astra.registry.r2_p5_admit_fields.v1'
REGISTRY_ID = 'REG-R2-P5-SCHEMA-20260922'
PANEL_VERSION = '2026-09-22.1-kalshi-occurrence-sot'
ADMIT_STAMP_UTC = '2026-09-22T21:18:13Z'
KNOB = 'audit_slice'
R2P5A0 = 'R2P5A0'
R2P5A1 = 'R2P5A1'
ARMS = (R2P5A0, R2P5A1)
AUDIT_SLICE = {
    R2P5A0: 'sot_pin_match',
    R2P5A1: 'holdout_delta_bin',
}
SEED_ROWS = 16
SEED_DELTA_SEC = 10800
WINDOW_CLOCK = 'kalshi_occurrence'
SERIES = 'KXNFLGAME'
CLOCK_ENUM = ('kalshi_occurrence', 'holdout_mixed', 'unknown')
FEEBOOK_COMMIT = '22371178cb2663250b4762f328069571c48cb551'
RAILS_COMMIT = '6a28e0d6254327ea4e6451c781bec56215ac6cac'
UNTOUCHED_BASE = 'e54554ff79b663b30836cd34f8d20004a9022a0a'
FREEZE_SHA256 = '0424455f062b7c46c7c6161b84fb7b29702719acc45bf6a61b4e8f16c5e26457'
PARENT_ACCEPT_SHA256 = '712e4771bf2783dbee1e4c553194cd2896a468184f2849f24e58c3eb350ff499'
SEED_SHA256 = '1edfa91979ab5dac72e28cc5e2ad5ff08aab414b5574fe115f86fb7d85e2ac4b'
SCHEMA_SHA256 = 'da7f6badd37d52fbd977681924379c3552f0dbfec94729d86ea411fb473ce53c'
PITCLE_SHA256 = 'f5ca19f15940a80476d1590e506951df87df619160b477f1dff06cc3554cb520'
CONDUCTOR_STAMP_SHA256 = '1ff111c61bbc518b176525fb40f538a229fc53b5c8460fae6f82929e0bbd4505'
PRE_ACCEPT_EMPTY_SHA256 = 'b796bfbbb3e78142569befd6a69801caaa662ed92072807df4068d49624f2926'
PITCLE_EVENT = 'KXNFLGAME-26OCT01PITCLE'
PITCLE_HOLDOUT_UTC = '2026-10-02T00:15:00Z'
PITCLE_OCCURRENCE_UTC = '2026-10-02T03:15:00Z'
PITCLE_T_MINUS_7D_UTC = '2026-09-25T03:15:00Z'
CANONICAL_TICKERS = (
    'KXNFLGAME-26OCT01PITCLE',
    'KXNFLGAME-26OCT04INDWAS',
    'KXNFLGAME-26OCT04ARINYG',
    'KXNFLGAME-26OCT04DALHOU',
    'KXNFLGAME-26OCT04GBTB',
    'KXNFLGAME-26OCT04JACCIN',
    'KXNFLGAME-26OCT04LARPHI',
    'KXNFLGAME-26OCT04NEBUF',
    'KXNFLGAME-26OCT04NYJCHI',
    'KXNFLGAME-26OCT04TENBAL',
    'KXNFLGAME-26OCT04MIAMIN',
    'KXNFLGAME-26OCT04DENSF',
    'KXNFLGAME-26OCT04KCLV',
    'KXNFLGAME-26OCT04LACSEA',
    'KXNFLGAME-26OCT04DETCAR',
    'KXNFLGAME-26OCT05ATLNO',
)
ROW_REQUIRED = (
    'event_ticker',
    'series_ticker',
    'kalshi_occurrence_datetime',
    'window_clock_source',
    't_minus_7d_utc',
    'sot_pin',
    'panel_version',
    'external_odds_present',
)
ADVERSE_FIELDS = (
    'edge_at_quote',
    'edge_at_fill',
    'hedge_complete_flag',
    'odds_age_sec',
    'fee_model_ref',
    'de_vig_method',
    'edge_lost_cancel',
)
SCORECARD_FIELDS = (
    'sot_pin_mismatch_n',
    'holdout_mixed_refuse_n',
    'delta_kickoff_sec_mode',
    'identity_join_ok_n',
    'external_odds_invent_refuse_n',
)
OUTPUT_KEYS = SCORECARD_FIELDS + ('results', 'pnl')
ADVERSARY_LABELS = {
    'external_odds_invent': 'invented external odds are refused',
    'invented_odds': 'invented external odds are refused',
    'holdout_rewrite': 'holdout kickoff rewrite is refused',
    'silent_holdout_mixed': 'silent holdout_mixed is refused',
    'labeled_recreation': 'labeled recreation is refused',
    'empty_seed': 'empty seed is refused',
    'pre_accept_empty': 'pre-ACCEPT empty payload is refused',
    'second_admit': 'a second ADMIT-1 panel is refused',
    'poll_steal': 'ADMIT-1 poll steal is refused',
    'admit_py': 'admit.py is refused',
    's2_ungate': 'S2 ungate is refused',
    'r2p4_ungate': 'R2-P4 ungate is refused',
    'logan_keys': 'Logan keys are refused',
    'logan_key': 'Logan keys are refused',
    'live_orders': 'live orders are refused',
    'invented_pnl': 'invented pnl is refused',
    'q6_retune': 'Q6-000 retune is refused',
    '000': 'Q6-000 retune is refused',
    'cap_sr_reopen': 'Cap-SR reopen is refused',
    'l2_cat_reopen': 'L2-CAT reopen is refused',
    'atl_gb': 'ATL@GB enrichment is refused',
}
DEAD_CARDS = (
    'silent_holdout_mixed',
    'external_odds_invent',
    'Q6-000_retune_REFUSED',
    'Cap-SR_reopen_DENIED',
    'L2-CAT_reopen_DENIED',
    'ATL@GB_REFUSED',
    'S2_R2-P4_WAIT',
)
DOES_NOT_MODIFY = (
    'kalshi_feebook_lab_20260922',
    'kalshi_rails_lab_20260922',
    'kalshi_r3p4_l2_cat_lab_20260923',
    'kalshi_r3_p4_l2_shape_lab_20260922',
    'kalshi_r2p1_hygiene_000_lab_20260922',
    'kalshi_r2p3_prop_ladder_lab_20260923',
    'kalshi_s4_ncaaf_feequue_lab_20260923',
    'kalshi_s5_mve_filllegs_lab_20260923',
    'kalshi_r3p3_fl_maker_taker_lab_20260923',
    'kalshi_c3_kxhighny_bordering_lab_20260923',
    'kalshi_c5_kxbtc15m_honesty_lab_20260923',
    'kalshi_soft_blended_reserves_000_lab_20260923',
    'kalshi_cap_sr_effects_000_lab_20260923',
    'kalshi_queue_fragility_000_lab_20260922',
    'kalshi_capital_structure_lab_20260922',
    'kalshi_examiner_fee_queue_honesty_000_lab_20260922',
    'nfl_prospective_recorder_20260922',
    'nfl_factorial_lab_20260921',
    'nfl_paircheck_lab_20260922',
    'nfl_queue_lab_20260921',
    'nfl_completion_lab_20260921',
    'nfl_measurement_lab_20260921',
    'nfl_timing_lab_20260921',
    'nfl_adaptive_lab_20260921',
)
FREEZE_NAME = 'R2_P5_SOT_ID_HARNESS_FREEZE_2026-09-23.md'
PARENT_NAME = 'R2-P5_SCHEMA_ACCEPT_2026-09-22.md'
SEED_NAME = 'R2-P5_SEED_INSTANCE_ADMIT1_SOT_ONLY_2026-09-22.json'
SCHEMA_NAME = 'r2_p5_admit_fields.schema.json'
PITCLE_NAME = 'PITCLE_HOLDOUT_IDENTITY_JOIN_HASH_FREEZE_2026-09-23.md'
STAMP_NAME = 'CONDUCTOR_FROZEN_EXPERIMENT.json'
PRE_ACCEPT_NAME = 'PRE_ACCEPT_EMPTY_RESULTS.json'
LAB_BUNDLE = ROOT / 'R2_P5_SOT_ID_HARNESS'
GOVERNANCE_BUNDLE = PARENT / 'packets' / 'R2_P5_SOT_ID_HARNESS'
GOVERNANCE_TREE = PARENT / 'lab' / 'governance' / 'astra'
PACKET = ROOT / FREEZE_NAME
PARENT_ACCEPT = ROOT / PARENT_NAME
SEED = ROOT / SEED_NAME
SCHEMA = ROOT / SCHEMA_NAME
PITCLE_CITE = ROOT / PITCLE_NAME
CONDUCTOR_STAMP = ROOT / STAMP_NAME
PRE_ACCEPT_EMPTY = ROOT / PRE_ACCEPT_NAME
FROZEN_EXPERIMENT = ROOT / 'FROZEN_EXPERIMENT.json'
EMPTY_RESULTS = ROOT / 'results' / 'EMPTY_RESULTS.json'
SEVEN_DAYS = timedelta(days=7)


class OrchestratorError(Exception):
    """A pin failed or a measurement write was requested."""


class ScorecardPromotionRefused(OrchestratorError):
    """Filled measurement fields stay out of the freeze packet."""

    def __init__(self):
        super().__init__('scorecard metrics stay null until Examiner')


class LiveOrdersForbidden(OrchestratorError):
    """This lab has no live order path."""

    def __init__(self):
        super().__init__('no live orders and no KalshiExecutionAdapter')


class AdversaryRefused(OrchestratorError):
    """A named out-of-scope label was requested."""

    def __init__(self, label):
        self.label = label
        super().__init__(label)


class SotPinMismatchRefused(OrchestratorError):
    """sot_pin differs from kalshi_occurrence_datetime."""

    def __init__(self):
        super().__init__('sot_pin mismatch')


class HoldoutMixedRefused(OrchestratorError):
    """Holdout and occurrence clocks were mixed without holdout_mixed."""

    def __init__(self):
        super().__init__(ADVERSARY_LABELS['silent_holdout_mixed'])


class ExternalOddsInventRefused(OrchestratorError):
    """Adverse or odds fields were filled without an odds document."""

    def __init__(self):
        super().__init__(ADVERSARY_LABELS['external_odds_invent'])


class RewriteHoldoutRefused(OrchestratorError):
    """Holdout kickoff is not rewritten to the SoT."""

    def __init__(self):
        super().__init__(ADVERSARY_LABELS['holdout_rewrite'])


class EmptySeedRefused(OrchestratorError):
    """An empty row list is not the ADMIT-1 seed."""

    def __init__(self):
        super().__init__(ADVERSARY_LABELS['empty_seed'])


class RecreationRefused(OrchestratorError):
    """A labeled recreation of the conductor seed is refused."""

    def __init__(self):
        super().__init__(ADVERSARY_LABELS['labeled_recreation'])


class PreAcceptEmptyRefused(OrchestratorError):
    """The pre-ACCEPT empty payload is not the seed and not the scorecard."""

    def __init__(self):
        super().__init__(ADVERSARY_LABELS['pre_accept_empty'])


class SecondPanelRefused(OrchestratorError):
    """A competing admit stamp is a second ADMIT-1 panel."""

    def __init__(self):
        super().__init__(ADVERSARY_LABELS['second_admit'])


class PollStealRefused(OrchestratorError):
    """The ADMIT-1 recorder poll budget stays with ADMIT-1."""

    def __init__(self):
        super().__init__(ADVERSARY_LABELS['poll_steal'])


class AdmitPyRefused(OrchestratorError):
    """admit.py is not run from this harness."""

    def __init__(self):
        super().__init__(ADVERSARY_LABELS['admit_py'])


class UngateRefused(OrchestratorError):
    """S2 and R2-P4 stay queued on C1 smoke."""

    def __init__(self):
        super().__init__('S2 and R2-P4 stay queued')


class PanelVersionRefused(OrchestratorError):
    """The seed is not the pinned ADMIT-1 panel version."""

    def __init__(self):
        super().__init__('panel_version')


class UnknownSlice(OrchestratorError):
    """The only knob is sot_pin_match or holdout_delta_bin."""

    def __init__(self):
        super().__init__('audit_slice')


class AtlGbRefused(OrchestratorError):
    """ATL@GB is excluded."""

    def __init__(self):
        super().__init__(ADVERSARY_LABELS['atl_gb'])


class DeltaInconsistentRefused(OrchestratorError):
    """Stated delta_kickoff_sec differs from the two clocks. Neither side is rewritten."""

    def __init__(self):
        super().__init__('delta_kickoff_sec inconsistent')


def _load_module(module_name, path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise OrchestratorError('sibling import')
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


hygiene = _load_module('r2p5_hygiene_labels', HYGIENE_PATH)


def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def execution_adapter():
    """No live order client lives in this lab."""
    raise LiveOrdersForbidden()


def assert_public_get(method):
    """GET is the only public capture verb. This function does not open a socket."""
    if method != 'GET':
        raise LiveOrdersForbidden()
    return None


def assert_route(route):
    """Allowlisted public GETs. Portfolio and order routes raise."""
    if not isinstance(route, str) or route == '':
        raise LiveOrdersForbidden()
    if not route.startswith('GET '):
        raise LiveOrdersForbidden()
    lowered = route.lower()
    if '/portfolio' in lowered or '/orders' in lowered:
        raise LiveOrdersForbidden()
    return None


def refuse_adversary(label):
    """Named refuse labels. Nothing is traded and no odds are invented."""
    if label not in ADVERSARY_LABELS:
        raise OrchestratorError('adversary label')
    if label in ('external_odds_invent', 'invented_odds'):
        raise ExternalOddsInventRefused()
    if label == 'holdout_rewrite':
        raise RewriteHoldoutRefused()
    if label == 'silent_holdout_mixed':
        raise HoldoutMixedRefused()
    if label == 'labeled_recreation':
        raise RecreationRefused()
    if label == 'empty_seed':
        raise EmptySeedRefused()
    if label == 'pre_accept_empty':
        raise PreAcceptEmptyRefused()
    if label == 'second_admit':
        raise SecondPanelRefused()
    if label == 'poll_steal':
        raise PollStealRefused()
    if label == 'admit_py':
        raise AdmitPyRefused()
    if label in ('s2_ungate', 'r2p4_ungate'):
        raise UngateRefused()
    if label == 'live_orders':
        raise LiveOrdersForbidden()
    if label == 'atl_gb':
        raise AtlGbRefused()
    raise AdversaryRefused(ADVERSARY_LABELS[label])


def rewrite_holdout_kickoff(row, new_kickoff=None):
    """Holdout kickoffs stay as admitted. This function does not edit the row."""
    if row is None or isinstance(row, (dict, str)) or new_kickoff is None or new_kickoff is not None:
        raise RewriteHoldoutRefused()
    raise RewriteHoldoutRefused()


def invent_external_odds(row):
    """Odds and adverse fields are not invented in this harness."""
    if row is None or isinstance(row, (dict, str, bool)):
        raise ExternalOddsInventRefused()
    raise ExternalOddsInventRefused()


def ungate_s2_r2p4():
    """This packet does not ungate S2 or R2-P4."""
    raise UngateRefused()


def second_admit_panel():
    """ADMIT-1 already stamped the seed. This harness does not admit again."""
    raise SecondPanelRefused()


def steal_admit1_poll():
    """The recorder poll budget stays on the ADMIT-1 recorder."""
    raise PollStealRefused()


def run_admit_py():
    """admit.py is not an entry point of this harness."""
    raise AdmitPyRefused()


def fetch_seed_over_network(url=None):
    """The seed is the offline file. This harness does not poll."""
    if url is None or isinstance(url, str):
        raise PollStealRefused()
    raise PollStealRefused()


def parse_utc(value):
    """Parse an ISO-8601 UTC timestamp. Z and +00:00 are the same instant."""
    if not isinstance(value, str) or value == '':
        raise OrchestratorError('timestamp')
    text = value[:-1] + '+00:00' if value.endswith('Z') else value
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        raise OrchestratorError('timestamp')
    if parsed.tzinfo is None:
        raise OrchestratorError('timestamp')
    return parsed.astimezone(timezone.utc)


def _atl_gb(value):
    if not isinstance(value, str):
        return False
    token = value.upper().replace('@', '').replace('_', '').replace('-', '')
    return 'ATLGB' in token or 'GBATL' in token


def _copy_paths(name):
    return (
        ROOT / name,
        LAB_BUNDLE / name,
        PARENT / 'packets' / name,
        GOVERNANCE_BUNDLE / name,
    )


def _assert_copies(name, digest):
    for path in _copy_paths(name):
        if sha256_file(path) != digest:
            raise OrchestratorError(name)


def conductor_pin_status():
    """Report whether checkout bytes match the attached conductor sha256 values."""
    freeze_match = sha256_file(PACKET) == FREEZE_SHA256
    parent_match = sha256_file(PARENT_ACCEPT) == PARENT_ACCEPT_SHA256
    seed_match = sha256_file(SEED) == SEED_SHA256
    schema_match = sha256_file(SCHEMA) == SCHEMA_SHA256
    pitcle_match = sha256_file(PITCLE_CITE) == PITCLE_SHA256
    payload = json.loads(SEED.read_text())
    rows = payload.get('rows') or []
    return {
        'freeze_matches_conductor_claim': freeze_match,
        'parent_accept_matches_conductor_claim': parent_match,
        'seed_matches_conductor_claim': seed_match,
        'schema_matches_conductor_claim': schema_match,
        'pitcle_matches_conductor_claim': pitcle_match,
        'conductor_bytes_in_checkout': all((
            freeze_match, parent_match, seed_match, schema_match, pitcle_match,
        )),
        'seed_rows': len(rows),
        'seed_rows_claim': SEED_ROWS,
        'governance_tree_present': GOVERNANCE_TREE.is_dir(),
    }


def _assert_authentic_bytes():
    _assert_copies(FREEZE_NAME, FREEZE_SHA256)
    _assert_copies(PARENT_NAME, PARENT_ACCEPT_SHA256)
    _assert_copies(SEED_NAME, SEED_SHA256)
    _assert_copies(SCHEMA_NAME, SCHEMA_SHA256)
    _assert_copies(PITCLE_NAME, PITCLE_SHA256)
    for path in (CONDUCTOR_STAMP, LAB_BUNDLE / STAMP_NAME, GOVERNANCE_BUNDLE / STAMP_NAME):
        if sha256_file(path) != CONDUCTOR_STAMP_SHA256:
            raise OrchestratorError('conductor stamp sha256')
    stamp = json.loads(CONDUCTOR_STAMP.read_text())
    if stamp.get('freeze_sha256') != FREEZE_SHA256:
        raise OrchestratorError('conductor stamp')
    if stamp.get('parent_accept_sha256') != PARENT_ACCEPT_SHA256:
        raise OrchestratorError('conductor stamp')
    if stamp.get('seed_instance_sha256') != SEED_SHA256:
        raise OrchestratorError('conductor stamp')
    if stamp.get('schema_sha256') != SCHEMA_SHA256:
        raise OrchestratorError('conductor stamp')
    if stamp.get('pitcle_identity_sha256') != PITCLE_SHA256:
        raise OrchestratorError('conductor stamp')
    if stamp.get('seed_rows') != SEED_ROWS:
        raise OrchestratorError('conductor stamp')
    if stamp.get('arms') != list(ARMS):
        raise OrchestratorError('conductor stamp')
    if stamp.get('feature_family') != FEATURE_FAMILY:
        raise OrchestratorError('conductor stamp')
    if stamp.get('packet_id') != EXPERIMENT_ID:
        raise OrchestratorError('conductor stamp')
    if stamp.get('results') is not None or stamp.get('pnl') is not None:
        raise ScorecardPromotionRefused()
    for path in (PRE_ACCEPT_EMPTY, LAB_BUNDLE / PRE_ACCEPT_NAME, GOVERNANCE_BUNDLE / PRE_ACCEPT_NAME):
        if sha256_file(path) != PRE_ACCEPT_EMPTY_SHA256:
            raise OrchestratorError('pre-accept empty sha256')
    status = conductor_pin_status()
    if status['conductor_bytes_in_checkout'] is not True:
        raise OrchestratorError('conductor bytes')
    if status['seed_rows'] != SEED_ROWS:
        raise OrchestratorError('seed rows')


def _labeled_recreation(payload):
    if not isinstance(payload, dict):
        return False
    if payload.get('recreation') is True or payload.get('labeled_recreation') is True:
        return True
    source = payload.get('source')
    if source in ('labeled_recreation', 'recreation'):
        return True
    note = payload.get('note')
    if isinstance(note, str) and 'recreation' in note.lower():
        return True
    return False


def _assert_fee_import_pins(seed):
    """Import-only pin. Hedge fields on the seed are not filled."""
    if feebook.EXAMINER_FORMULA_ID != 'astra.r1p1.feebook.claude_order_level_ceil.v1':
        raise OrchestratorError('examiner formula')
    if seed.get('fee_pin_formula_id') != feebook.EXAMINER_FORMULA_ID:
        raise OrchestratorError('fee pin')
    if hygiene.FEEBOOK_COMMIT != FEEBOOK_COMMIT or hygiene.RAILS_COMMIT != RAILS_COMMIT:
        raise OrchestratorError('pin')
    if rails.FEE_CREDIT_RULE_ID != 'astra.r1p5.rails.maker_credit_floor_cent.v1':
        raise OrchestratorError('rails rule')
    observation = rails.BookObservation(
        rails.canonical_book_content({'schema': 'r2p5-sot-id-pin'}),
        't0',
    )
    verdict = rails.judge_freshness(None, observation)
    if not verdict.fresh:
        raise OrchestratorError('freshness')
    return {
        'fee_source': 'feebook',
        'rails_source': 'rails',
        'fee_applied_to_seed_rows': False,
        'probe_scorecard_write': False,
    }


def assert_no_invented_odds(row, external_odds_path):
    """Adverse fields stay null when odds are absent. Filled values are refused."""
    if not isinstance(row, dict):
        raise ExternalOddsInventRefused()
    if row.get('invent_odds') is True or row.get('invent_adverse') is True:
        raise ExternalOddsInventRefused()
    present = row.get('external_odds_present')
    if not isinstance(present, bool):
        raise OrchestratorError('external_odds_present')
    if present is False:
        for key in ADVERSE_FIELDS:
            if key in row and row[key] is not None:
                raise ExternalOddsInventRefused()
        return None
    if external_odds_path is None:
        for key in ('edge_at_quote', 'edge_at_fill', 'hedge_complete_flag', 'odds_age_sec'):
            if row.get(key) is not None:
                raise ExternalOddsInventRefused()
    if row.get('hedge_complete_flag') is not None:
        if row.get('fee_model_ref') != feebook.EXAMINER_FORMULA_ID:
            raise OrchestratorError('fee_model_ref')
    return None


def _assert_pitcle_identity(row):
    """The identity cite is a hash freeze. A changed PIT@CLE holdout is a rewrite."""
    if row.get('event_ticker') != PITCLE_EVENT:
        return False
    if parse_utc(row.get('holdout_kickoff_utc')) != parse_utc(PITCLE_HOLDOUT_UTC):
        raise RewriteHoldoutRefused()
    if parse_utc(row.get('kalshi_occurrence_datetime')) != parse_utc(PITCLE_OCCURRENCE_UTC):
        raise OrchestratorError('pitcle occurrence')
    if parse_utc(row.get('sot_pin')) != parse_utc(PITCLE_OCCURRENCE_UTC):
        raise SotPinMismatchRefused()
    if parse_utc(row.get('t_minus_7d_utc')) != parse_utc(PITCLE_T_MINUS_7D_UTC):
        raise HoldoutMixedRefused()
    if row.get('delta_kickoff_sec') != SEED_DELTA_SEC:
        raise DeltaInconsistentRefused()
    if row.get('window_clock_source') != WINDOW_CLOCK:
        raise HoldoutMixedRefused()
    return True


def audit_sot_pin(row):
    """R2P5A0. sot_pin matches occurrence. Silent holdout_mixed raises."""
    if not isinstance(row, dict):
        raise OrchestratorError('row')
    if _atl_gb(row.get('event_ticker')):
        raise AtlGbRefused()
    if row.get('holdout_rewritten_to_sot') is True:
        raise RewriteHoldoutRefused()
    for key in ROW_REQUIRED:
        if key not in row:
            raise OrchestratorError('schema required')
    source = row.get('window_clock_source')
    if source not in CLOCK_ENUM:
        raise OrchestratorError('window_clock_source')
    if row.get('sot_pin') != row.get('kalshi_occurrence_datetime'):
        raise SotPinMismatchRefused()
    occurrence = parse_utc(row['kalshi_occurrence_datetime'])
    if parse_utc(row['sot_pin']) != occurrence:
        raise SotPinMismatchRefused()
    window_anchor = parse_utc(row['t_minus_7d_utc']) + SEVEN_DAYS
    holdout_raw = row.get('holdout_kickoff_utc')
    if source == WINDOW_CLOCK:
        if window_anchor != occurrence:
            raise HoldoutMixedRefused()
    elif source == 'unknown':
        if holdout_raw is not None and parse_utc(holdout_raw) != occurrence:
            raise HoldoutMixedRefused()
        if window_anchor != occurrence:
            raise HoldoutMixedRefused()
    if row.get('event_ticker') == PITCLE_EVENT:
        _assert_pitcle_identity(row)
    return {
        'event_ticker': row['event_ticker'],
        'audit_slice': AUDIT_SLICE[R2P5A0],
        'sot_pin_matches_occurrence': True,
    }


def _stated_delta(row):
    stated = row.get('delta_kickoff_sec')
    if stated is None:
        return None
    if isinstance(stated, bool) or not isinstance(stated, int):
        raise OrchestratorError('delta')
    return stated


def audit_delta_bin(row, external_odds_path):
    """R2P5A1. Delta matches the clocks. Odds invent and holdout rewrite raise."""
    if not isinstance(row, dict):
        raise OrchestratorError('row')
    if _atl_gb(row.get('event_ticker')):
        raise AtlGbRefused()
    if row.get('holdout_rewritten_to_sot') is True:
        raise RewriteHoldoutRefused()
    assert_no_invented_odds(row, external_odds_path)
    holdout_raw = row.get('holdout_kickoff_utc')
    stated = _stated_delta(row)
    if holdout_raw is None:
        if stated is not None:
            raise DeltaInconsistentRefused()
        return {
            'event_ticker': row.get('event_ticker'),
            'audit_slice': AUDIT_SLICE[R2P5A1],
            'delta_consistent': True,
        }
    computed = int((
        parse_utc(row['kalshi_occurrence_datetime']) - parse_utc(holdout_raw)
    ).total_seconds())
    if stated != computed:
        raise DeltaInconsistentRefused()
    if row.get('event_ticker') == PITCLE_EVENT:
        _assert_pitcle_identity(row)
    return {
        'event_ticker': row['event_ticker'],
        'audit_slice': AUDIT_SLICE[R2P5A1],
        'delta_consistent': True,
    }


def audit_row(arm, row, external_odds_path=None):
    """One audit slice on one row. Scorecard counters stay unpublished."""
    if arm == R2P5A0:
        assert_no_invented_odds(row, external_odds_path)
        return audit_sot_pin(row)
    if arm == R2P5A1:
        return audit_delta_bin(row, external_odds_path)
    raise UnknownSlice()


def _validate_seed(payload, canonical):
    if not isinstance(payload, dict):
        raise OrchestratorError('seed')
    if payload.get('note') == 'pre-ACCEPT empty':
        raise PreAcceptEmptyRefused()
    if _labeled_recreation(payload):
        raise RecreationRefused()
    if payload.get('schema_id') != SCHEMA_ID:
        raise OrchestratorError('schema')
    if payload.get('registry_id') != REGISTRY_ID:
        raise OrchestratorError('registry')
    if payload.get('panel_version') != PANEL_VERSION:
        raise PanelVersionRefused()
    if payload.get('admit_stamp_utc') != ADMIT_STAMP_UTC:
        raise SecondPanelRefused()
    if payload.get('external_odds_path') is not None:
        raise ExternalOddsInventRefused()
    rows = payload.get('rows')
    if not isinstance(rows, list) or len(rows) == 0:
        raise EmptySeedRefused()
    if len(rows) != SEED_ROWS:
        raise RecreationRefused()
    tickers = tuple(row.get('event_ticker') for row in rows if isinstance(row, dict))
    if tickers != CANONICAL_TICKERS:
        raise RecreationRefused()
    if len(set(tickers)) != SEED_ROWS:
        raise OrchestratorError('duplicate')
    odds_path = payload.get('external_odds_path')
    pitcle_n = 0
    for row in rows:
        if row.get('series_ticker') != SERIES:
            raise OrchestratorError('series')
        if not str(row.get('event_ticker', '')).startswith('KXNFLGAME-'):
            raise OrchestratorError('series')
        if row.get('panel_version') != PANEL_VERSION:
            raise PanelVersionRefused()
        if canonical and row.get('window_clock_source') != WINDOW_CLOCK:
            raise RecreationRefused()
        if canonical and row.get('delta_kickoff_sec') != SEED_DELTA_SEC:
            raise RecreationRefused()
        audit_row(R2P5A0, row, odds_path)
        audit_row(R2P5A1, row, odds_path)
        if row.get('event_ticker') == PITCLE_EVENT:
            pitcle_n += 1
    if pitcle_n != 1:
        raise OrchestratorError('pitcle')
    _assert_fee_import_pins(payload)
    return payload


def load_seed(path=None):
    """Offline ADMIT-1 seed. The canonical path must match the attached digest."""
    path = SEED if path is None else Path(path)
    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if digest == PRE_ACCEPT_EMPTY_SHA256:
        raise PreAcceptEmptyRefused()
    canonical = path.resolve() == SEED.resolve()
    if canonical:
        _assert_authentic_bytes()
        if digest != SEED_SHA256:
            raise OrchestratorError('seed sha256')
    payload = json.loads(raw)
    if isinstance(payload, dict) and payload.get('note') == 'pre-ACCEPT empty':
        raise PreAcceptEmptyRefused()
    return _validate_seed(payload, canonical=canonical)


def arm_table():
    return tuple({'id': arm, 'audit_slice': AUDIT_SLICE[arm]} for arm in ARMS)


def instrument_binding(seed=None):
    """One audit-slice knob. Fee and rails commits stay import-only."""
    if seed is None:
        seed = load_seed()
    pins = _assert_fee_import_pins(seed)
    rows = seed['rows']
    hedge_null = all(
        row.get('hedge_complete_flag') is None and row.get('external_odds_present') is False
        for row in rows
    )
    return {
        'experiment_id': EXPERIMENT_ID,
        'lab_directory': LAB_DIRECTORY,
        'feature_family': FEATURE_FAMILY,
        'knob': KNOB,
        'arms': arm_table(),
        'panel_version': seed['panel_version'],
        'admit_stamp_utc': seed['admit_stamp_utc'],
        'harness_admitted_at': None,
        'seed_rows': len(rows),
        'strategy_pointer': None,
        'feebook_commit': FEEBOOK_COMMIT,
        'rails_commit': RAILS_COMMIT,
        'examiner_formula_id': feebook.EXAMINER_FORMULA_ID,
        'fee_credit_rule_id': rails.FEE_CREDIT_RULE_ID,
        'fee_source': pins['fee_source'],
        'rails_source': pins['rails_source'],
        'fee_import_only': True,
        'rails_import_only': True,
        'fee_applied_to_seed_rows': False,
        'probe_scorecard_write': False,
        'hedge_fields_null': hedge_null,
        'external_odds_invent': 'REFUSED',
        'holdout_rewrite': 'REFUSED',
        'silent_holdout_mixed': 'REFUSED',
        'labeled_recreation': 'REFUSED',
        'empty_seed': 'REFUSED',
        'second_admit_panel': False,
        'poll_steal': False,
        's2_r2p4_ungated': False,
        'admit_py_run': False,
        'logan_keys_required': False,
        'live_orders': False,
        'signal_retune_000': False,
        'cap_sr_reopen': False,
        'l2_cat_reopen': False,
        'fee_is_knob': False,
        'dead_cards': DEAD_CARDS,
        'scorecard_fields': SCORECARD_FIELDS,
        'freeze_sha256': FREEZE_SHA256,
        'parent_accept_sha256': PARENT_ACCEPT_SHA256,
        'seed_sha256': SEED_SHA256,
        'schema_sha256': SCHEMA_SHA256,
        'pitcle_identity_sha256': PITCLE_SHA256,
    }


def published_scorecard():
    """Freeze outputs. Every instrument field is present and null."""
    scorecard = {key: None for key in OUTPUT_KEYS}
    for key in OUTPUT_KEYS:
        if scorecard[key] is not None:
            raise ScorecardPromotionRefused()
    scorecard['status'] = 'EMPTY_RESULTS_PRE_EXAMINER'
    scorecard['s2_r2p4_ungated'] = False
    scorecard['admit_py_run'] = False
    scorecard['logan_keys_required'] = False
    return scorecard


def assert_null_scorecard(payload):
    """Require every instrument field, results, and pnl, and require null."""
    if not isinstance(payload, dict):
        raise ScorecardPromotionRefused()
    if payload.get('note') == 'pre-ACCEPT empty':
        raise PreAcceptEmptyRefused()
    for key in OUTPUT_KEYS:
        if key not in payload or payload[key] is not None:
            raise ScorecardPromotionRefused()
    return payload


def write_scorecard(payload):
    """Refuse a missing or non-null measurement field. Nothing is written."""
    assert_null_scorecard(payload)
    raise ScorecardPromotionRefused()


def _audit_report(arm, seed):
    if arm not in AUDIT_SLICE:
        raise UnknownSlice()
    rows = seed['rows']
    odds_path = seed.get('external_odds_path')
    slots = [audit_row(arm, row, odds_path) for row in rows]
    if len(slots) != SEED_ROWS:
        raise OrchestratorError('seed rows')
    clocks = {row.get('window_clock_source') for row in rows}
    deltas = {row.get('delta_kickoff_sec') for row in rows}
    published = published_scorecard()
    report = {
        'experiment_id': EXPERIMENT_ID,
        'arm': arm,
        'audit_slice': AUDIT_SLICE[arm],
        'source': 'admit1_sot_seed',
        'rows_n': len(rows),
        'series_ticker': SERIES,
        'window_clock_uniform': clocks == {WINDOW_CLOCK},
        'delta_values_uniform': len(deltas) == 1,
        'external_odds_path': odds_path,
        'external_odds_present_all_false': all(row.get('external_odds_present') is False for row in rows),
        'adverse_fields_null': all(row.get(key) is None for row in rows for key in ADVERSE_FIELDS),
        'pitcle_event_ticker': PITCLE_EVENT,
        'pitcle_identity_checked': True,
        'pitcle_holdout_unchanged': True,
        'identity_cite_sha256': PITCLE_SHA256,
        'seed_sha256': SEED_SHA256,
        'published': published,
        'promoted': False,
        'strategy_pointer': None,
        'fee_import_only': True,
        'rails_import_only': True,
        'fee_pin': FEEBOOK_COMMIT,
        'rails_pin': RAILS_COMMIT,
        's2_r2p4_ungated': False,
        'second_admit_panel': False,
        'poll_steal': False,
        'admit_py_run': False,
        'live_orders': False,
        'logan_keys_required': False,
    }
    for key in OUTPUT_KEYS:
        report[key] = None
    assert_null_scorecard(report)
    assert_null_scorecard(published)
    return report


def conduct(arm, seed=None):
    """Schema for one audit slice. Scorecard fields stay null."""
    if arm not in AUDIT_SLICE:
        raise UnknownSlice()
    if seed is None:
        seed = load_seed()
    return _audit_report(arm, seed)


def frozen_output_snapshot():
    """Read freeze files. Does not modify them."""
    payloads = {
        'frozen': json.loads(FROZEN_EXPERIMENT.read_text()),
        'empty': json.loads(EMPTY_RESULTS.read_text()),
        'bundle_frozen': json.loads((LAB_BUNDLE / 'FROZEN_EXPERIMENT.json').read_text()),
        'bundle_results': json.loads((LAB_BUNDLE / 'results.json').read_text()),
        'governance_frozen': json.loads((GOVERNANCE_BUNDLE / 'FROZEN_EXPERIMENT.json').read_text()),
        'governance_results': json.loads((GOVERNANCE_BUNDLE / 'results.json').read_text()),
    }
    snapshot = {}
    for name, payload in payloads.items():
        for key in ('results', 'pnl'):
            if key not in payload or payload[key] is not None:
                raise ScorecardPromotionRefused()
            snapshot['%s.%s' % (name, key)] = None
        if name not in ('frozen', 'bundle_frozen', 'governance_frozen'):
            for key in SCORECARD_FIELDS:
                if key not in payload or payload[key] is not None:
                    raise ScorecardPromotionRefused()
                snapshot['%s.%s' % (name, key)] = None
    return snapshot
