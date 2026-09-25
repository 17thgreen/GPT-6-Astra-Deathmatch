"""Q6S1 KXATPMATCH inventory re-proof harness.

Measurement only. Series is KXATPMATCH. One knob: inventory_slice.
Q6S1A0 is flat_control. Q6S1A1 is inventory_bin_exposure. Feebook and
rails stay at the pinned commits and are imported, not edited. The series
fee is the cache-labeled quadratic_with_maker_fees multiplier 1 pin. It is
not a live R1-P1 /series pin and it is not multiplier 0.5.

ATP-FQ and ATP-RJ are closed import-only parents. analysis_slice and
join_gate are not reopened. This module does not place orders, does not
read Logan keys, does not open a network client, does not run admit.py,
and does not write scorecard metrics. results, pnl, and inventory deltas
stay null.
"""
import hashlib
import json
import sys
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

LAB_DIRECTORY = 'kalshi_q6s1_kxatpmatch_inventory_reproof_lab_20260925'
EXPERIMENT_ID = 'Q6S1-KXATPMATCH-INVENTORY-REPROOF'
FEATURE_FAMILY = 'Q6S1-ATP-INVENTORY'
SERIES = 'KXATPMATCH'
SCHEMA_ID = 'astra.panel_stub.v0'
PANEL_VERSION = '2026-09-23.atp-kxatpmatch-v0'
STUB_STATUS = 'NOT_ADMITTED'
KNOB = 'inventory_slice'
Q6S1A0 = 'Q6S1A0'
Q6S1A1 = 'Q6S1A1'
ARMS = (Q6S1A0, Q6S1A1)
INVENTORY_SLICE = {
    Q6S1A0: 'flat_control',
    Q6S1A1: 'inventory_bin_exposure',
}
CLOSED_PARENT_ARMS = {
    'ATPA0': 'ATP-FQ analysis_slice',
    'ATPA1': 'ATP-FQ analysis_slice',
    'J0': 'ATP-RJ join_gate',
    'J1': 'ATP-RJ join_gate',
    'Q6S5A0': 'Q6S5 analysis_slice',
    'Q6S5A1': 'Q6S5 analysis_slice',
}
CLOSED_KNOBS = ('analysis_slice', 'join_gate')
FEEBOOK_COMMIT = '22371178cb2663250b4762f328069571c48cb551'
RAILS_COMMIT = '6a28e0d6254327ea4e6451c781bec56215ac6cac'
BASE_COMMIT = 'f349ffa819960b8f641725fbf259f5430dffcff7'
FREEZE_SHA256 = 'd86f7a402ea63fb132d80480f844a954fe9061a27b9b6bed125f9785ae64640e'
ACCEPT_SHA256 = '162100624297588516390aab51ba0161cf15d0659c439ec6b60e940b99845635'
PANEL_STUB_SHA256 = 'ed041c502d1f775d33c44bf900ac91b1339d99045bddd2052edd09a139ae2d3f'
SOURCE_PINS_SHA256 = 'cddb85e83e679a101108c45cd82b2e9b59e68f9afd0d89d141a5bee0460376e7'
FROZEN_EXPERIMENT_SHA256 = '632d352c30728dc4339cc74c2ba219aae3e8e9c7dc306e8d992c0386311eef98'
EMPTY_RESULTS_SHA256 = 'b6fab2cf7e2f4cee9889658ea2acebd6bdeab887fddf370c8081e8eddf3cffa6'
HOLD_SHA256 = 'eca9aad2409c5636742fe15cbc7947098cac4ba19c7d610e5e69a7454fdae72d'
TEMPLATE_V12_SHA256 = '56bcf6269a42031d9d90496e9a65c2292321aed2165033f6fb44ff8cc4d6b1cc'
TEMPLATE_V12_MD_SHA256 = 'ad1dd2834652b8e9be331ddf2f3ec900ea587efb042251fde6452532b2e36394'
P16_PDF_SHA256 = '7e55bc260526aa5088ee31f74475851219ab2cd7f19fdd2f0dd5e9f998c8b45e'
SCOUT_HUNT_SHA256 = '14c99ec8ea00bae507a21d0e6a1879fb94d32ef69ad4b5e3b40a9952821e5da7'
SPORTS_MARKETS_SHA256 = 'b603474b3ca336b0a3678ff0deb8a937dfdcc4205e8e24db4d657d40d2323c60'
SPORTS_SUMMARY_SHA256 = 'd5aee9c9254a0c9178b3ecc4fbd84f6db7bc29f6bc11af4df8690e4242ebe647'
ATP_FQ_FREEZE_SHA256 = '4d4ce944946e72dd40567d14388fe11c6145fbbb32505a880bcf80a4c8b4dffe'
ATP_RJ_FREEZE_SHA256 = 'dc9fcb326a97ce24267ed96438bf403687bc9aef6b79dccef3483d0e4cdeeb69'
SETTLED_REGET_SHA256 = '068ff00fe420d3365cc798549ef2e89aac96fa7e841846f73e67d5103c49760a'
KICK_SHA256 = '63eab2f727c9636196e08092339d5efc10439396bc9a7d3f696b7344ac746cb6'
SCORECARD_STUB_JSON_SHA256 = '2f72464583253ca3e5d3d3c8fbfd593e3fc94acc1f31396420074c85a8934e24'
BUNDLE_SHA256 = '62de476ec3d27b64183d1eba0d223c2c5ad61a6bc8abffde9873f6e76a5e633e'
PANEL_EVENTS_N = 6
PANEL_MARKETS_N = 12
SCOUT_EVENTS_N = 24
SCOUT_MARKETS_N = 48
SCREEN_EVENTS_N = 14
SCREEN_MARKETS_N = 28
FEE_TYPE = 'quadratic_with_maker_fees'
FEE_MULTIPLIER = 1
FEE_LABEL = 'CACHE-LABELED'
FEE_SRC = 'cache:sports_screen_Q6S1_and_ATP_FQ_pin'
PUBLIC_HOST = 'https://api.elections.kalshi.com/trade-api/v2'
NFL_000_POINTER = 'nfl_factorial_lab_20260921/SHADOW_CANDIDATE_FREEZE.json'
FEEBOOK_PIN = 'kalshi_feebook_lab_20260922/@22371178cb2663250b4762f328069571c48cb551'
RAILS_PIN = 'kalshi_rails_lab_20260922/@6a28e0d6254327ea4e6451c781bec56215ac6cac'
OUTPUT_KEYS = (
    'inventory_delta_flat_vs_binned',
    'unresolved_inventory',
    'position_bucket_gap',
    'settled_join_n',
    'n_books',
    'results',
    'pnl',
)
COMMON_SCORECARD_KEYS = (
    'net_pnl_without_rewards',
    'net_pnl_with_rewards',
    'rewards_actually_earned',
    'calibration',
    'fill_rate',
    'adverse_selection_after_fills',
    'feasible_vs_requested_size',
    'unresolved_inventory',
    'capital_hours',
    'drawdown',
    'event_concentration',
)
FOREIGN_SERIES = (
    'KXMLBSPREAD',
    'KXMLBGAME',
    'KXNFLGAME',
    'KXNFLPASSYDS',
    'KXNHLGAME',
    'KXNCAAFGAME',
    'KXCPI',
    'KXBTC15M',
    'KXETH15M',
    'KXHIGHNY',
    'KXHIGHCHI',
    'KXUFCFIGHT',
    'KXMVECROSSCATEGORY',
)
ABSENT_PINS = (
    'panel_admitted.json (ATP panel remains NOT_ADMITTED; admitted_at null; Variants does not run admit.py)',
    'live /series fee pin (fee remains CACHE-LABELED quadratic_with_maker_fees×1 until Examiner live /series)',
    'fresh sports-screen ATP panel subset matching screen inventory 28mkts/14ev (reuse authentic 6/12 stub; do not invent markets)',
    'invented fills / PnL / depth / settlement_ts / inventory deltas (null until Clock+Examiner)',
    'Q6S1-specific scout PDF / archivist index prior entry (none on disk at freeze; Archivist ping only)',
)
DOES_NOT_UNGATE = (
    'S1_KXMLBGAME_ML',
    'S2',
    'R2-P4',
    'Card06_open_window',
    'Q6-000_retune',
    'Cap-SR',
    'ATP-FQ',
    'ATP-RJ',
    'Q6S5',
    'PR57_INFRA',
)
UNGATE_ALIASES = {
    'S1': 'S1_KXMLBGAME_ML',
    'KXMLBGAME': 'S1_KXMLBGAME_ML',
    'Card 06': 'Card06_open_window',
    'Q6-000': 'Q6-000_retune',
    'Cap-SR': 'Cap-SR',
    'ATP-FQ': 'ATP-FQ',
    'ATP-RJ': 'ATP-RJ',
    'Q6S5': 'Q6S5',
    'PR57': 'PR57_INFRA',
}
ADVERSARY_LABELS = {
    'lee_ready': 'Lee-Ready is refused on every input',
    'live_orders': 'live orders are refused',
    'logan_keys': 'Logan keys are refused',
    'invented_pnl': 'invented pnl is refused',
    'invented_fills': 'invented fills are refused',
    'invented_depth': 'invented depth is refused',
    'invented_markets': 'invented markets are refused',
    'invented_inventory': 'invented inventory deltas are refused',
    'invented_settlement_ts': 'invented settlement_ts is refused',
    'q6_retune': 'Q6-000 retune is refused',
    'cap_sr_reopen': 'Cap-SR reopen is refused',
    'atp_fq_reopen': 'ATP-FQ reopen is refused',
    'atp_rj_reopen': 'ATP-RJ reopen is refused',
    'q6s5_reopen': 'Q6S5 reopen is refused',
    'pr57_infra': 'PR57 INFRA duplicate is refused',
    'kxmlbgame_ml_retune': 'KXMLBGAME ML retune is refused',
    'card06_reopen': 'Card 06 open-window reopen is refused',
    'dual_cloud': 'dual-cloud is refused',
    'admit_py': 'admit.py is refused',
    'claim_live_r1p1': 'cache fee is not live R1-P1',
    'fee_half': 'fee multiplier 0.5 is refused',
    'pass3_b2': 'Pass-3 / Refiner / B2 promote is refused',
}
DOES_NOT_MODIFY = (
    'kalshi_feebook_lab_20260922',
    'kalshi_rails_lab_20260922',
    'kalshi_atp_kxatpmatch_feequue_lab_20260923',
    'kalshi_atp_kxatpmatch_settled_join_lab_20260924',
    'kalshi_q6s5_kxmlbspread_feequue_lab_20260925',
    'kalshi_cap_sr_effects_000_lab_20260923',
    'kalshi_soft_blended_reserves_000_lab_20260923',
    'nfl_factorial_lab_20260921',
    'nfl_q7_rehab_p1_cadence_20260923',
    'nfl_q7_rehab_p2_rank_sizing_20260923',
    'lab/astra-capture/atp-kxatpmatch/panel_stub.json',
    'lab/astra-capture/atp-kxatpmatch/settled_reget_2026-09-24.json',
)
FREEZE_NAME = 'Q6S1_KXATPMATCH_INVENTORY_REPROOF_FREEZE_2026-09-25.md'
ACCEPT_NAME = 'CONDUCTOR_ACCEPT_Q6S1_KXATPMATCH_INVENTORY_REPROOF_2026-09-25.json'
HOLD_NAME = 'EXAMINER_HOLD_Q6S1_KXATPMATCH_INVENTORY_REPROOF_PRE_PR_2026-09-25.json'
SOURCE_PINS_NAME = 'SOURCE_PINS.json'
SCORECARD_JSON_NAME = 'EXAMINER_SCORECARD_STUB_Q6S1_KXATPMATCH_INVENTORY_REPROOF_2026-09-25.json'
SCORECARD_MD_NAME = 'EXAMINER_SCORECARD_STUB_Q6S1_KXATPMATCH_INVENTORY_REPROOF_2026-09-25.md'
PACKET = ROOT / FREEZE_NAME
LAB_BUNDLE = ROOT / 'Q6S1_KXATPMATCH_INVENTORY_REPROOF'
GOVERNANCE = PARENT / 'lab' / 'governance' / 'astra' / 'packets'
GOVERNANCE_BUNDLE = GOVERNANCE / 'Q6S1_KXATPMATCH_INVENTORY_REPROOF'
FROZEN_EXPERIMENT = ROOT / 'FROZEN_EXPERIMENT.json'
EMPTY_RESULTS = ROOT / 'results' / 'EMPTY_RESULTS.json'
SOURCE_PINS = ROOT / SOURCE_PINS_NAME
PANEL_STUB = PARENT / 'lab' / 'astra-capture' / 'atp-kxatpmatch' / 'panel_stub.json'
PANEL_ADMITTED = PARENT / 'lab' / 'astra-capture' / 'atp-kxatpmatch' / 'panel_admitted.json'
LAB_PANEL_STUB = ROOT / 'panel_stub.json'
CONDUCTOR_ACCEPT = ROOT / ACCEPT_NAME
EXAMINER_HOLD = ROOT / HOLD_NAME
P16_CHECKLIST = ROOT / 'p16_preregistration_checklist.json'
TEMPLATE_V12 = (
    PARENT / 'lab' / 'governance' / 'astra' / 'templates'
    / 'EXAMINER_KALSHI_SCORECARD_TEMPLATE_v1.2.json'
)
P16_PDF = PARENT / 'lab' / 'governance' / 'astra' / 'research' / 'KALSHI_EDGE_RESEARCH_2026-09-24.pdf'
SCOUT_HUNT = PARENT / 'packets' / 'scout_cashcow_hunt_2026-09-22' / 'scout_hunt_KXATPMATCH.json'
SPORTS_MARKETS = (
    GOVERNANCE / 'scout_sports_q6_screen' / 'raw' / 'markets_open_KXATPMATCH.json'
)
SPORTS_SUMMARY = (
    GOVERNANCE / 'scout_sports_q6_screen' / 'raw' / 'markets_open_KXATPMATCH_SUMMARY.json'
)
ATP_FQ_FREEZE = GOVERNANCE / 'ATP_KXATPMATCH_FEEQUEUE_HARNESS_FREEZE_2026-09-23.md'
ATP_RJ_FREEZE = GOVERNANCE / 'ATP_KXATPMATCH_SETTLED_RESOLUTION_JOIN_HARNESS_FREEZE_2026-09-24.md'
SETTLED_REGET = PARENT / 'lab' / 'astra-capture' / 'atp-kxatpmatch' / 'settled_reget_2026-09-24.json'
KICK = GOVERNANCE / 'CONDUCTOR_KICK_VARIANTS_Q6S1_KXATPMATCH_INVENTORY_REPROOF_FREEZE_2026-09-25.json'


class OrchestratorError(Exception):
    """Caller passed a shape this harness does not own."""


class SeriesRefused(OrchestratorError):
    """The series is not KXATPMATCH."""


class LiveOrdersForbidden(OrchestratorError):
    """Orders, portfolio, and any non-GET verb are refused."""


class FeeHalfRefused(OrchestratorError):
    """Multiplier 0.5 is not the Q6S1 cache pin."""


class FeeMultiplierRefused(OrchestratorError):
    """Only multiplier 1 is the cache pin."""


class CacheNotLiveR1P1(OrchestratorError):
    """The cache label is not a live R1-P1 /series pin."""


class UnknownSlice(OrchestratorError):
    """The arm is not Q6S1A0 or Q6S1A1."""


class ClosedParentRefused(OrchestratorError):
    """ATP-FQ analysis_slice and ATP-RJ join_gate stay closed."""


class AdmitPyRefused(OrchestratorError):
    """admit.py is not run by this harness."""


class InventedFillRefused(OrchestratorError):
    """Fills are not invented."""


class InventedPnlRefused(OrchestratorError):
    """PnL is not invented."""


class InventedInventoryRefused(OrchestratorError):
    """Inventory deltas are not invented."""


class InventedDepthRefused(OrchestratorError):
    """Depth is not invented."""


class InventedSettlementRefused(OrchestratorError):
    """settlement_ts is not invented."""


class InventedMarketRefused(OrchestratorError):
    """Markets are not invented."""


class ScorecardPromotionRefused(OrchestratorError):
    """A null scorecard is not promoted."""


class UngateRefused(OrchestratorError):
    """Named closed cards stay closed."""


class AdversaryRefused(OrchestratorError):
    """Named refuse label."""


class PanelVersionRefused(OrchestratorError):
    """Panel version is not the pinned ATP stub."""


class LeeReadyRefused(OrchestratorError):
    """Lee-Ready is refused on every input."""


def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def execution_adapter():
    """No live order client lives in this lab."""
    raise LiveOrdersForbidden()


def assert_series(value):
    """KXATPMATCH only. Foreign series tokens are refused."""
    if not isinstance(value, str) or not value:
        raise SeriesRefused()
    upper = value.upper()
    for token in FOREIGN_SERIES:
        if token in upper:
            raise SeriesRefused(token)
    if SERIES not in upper and (
        upper.startswith(SERIES) is False and 'SERIES_TICKER=' in upper
    ):
        ticker = upper.split('SERIES_TICKER=', 1)[-1].split('&', 1)[0]
        if ticker and not ticker.startswith(SERIES):
            raise SeriesRefused(ticker)
    if 'SERIES_TICKER=' in upper:
        ticker = upper.split('SERIES_TICKER=', 1)[-1].split('&', 1)[0].split('/', 1)[0]
        if ticker and not ticker.startswith(SERIES):
            raise SeriesRefused(ticker)
    return value


def _normalize_public_path(path):
    if not isinstance(path, str) or not path:
        raise OrchestratorError('path')
    if path.startswith('http://') or path.startswith('https://'):
        if not path.startswith(PUBLIC_HOST + '/') and path != PUBLIC_HOST:
            raise OrchestratorError('host')
        path = path[len(PUBLIC_HOST):] or '/'
    if not path.startswith('/'):
        path = '/' + path
    lowered = path.lower()
    if '/orders' in lowered or '/portfolio' in lowered:
        raise LiveOrdersForbidden()
    assert_series(path)
    return path


class StubTransport:
    """In-memory GET stand-in. live_gets stays 0. No network client is opened."""

    def __init__(self, bodies=None, markets_hot=False):
        self.bodies = {} if bodies is None else dict(bodies)
        self.markets_hot = bool(markets_hot)
        self.calls = []
        self.live_gets = 0

    def request(self, method, path):
        if method != 'GET':
            raise LiveOrdersForbidden()
        normalized = _normalize_public_path(path)
        self.calls.append(('GET', normalized))
        chosen = normalized
        preferred = None
        if self.markets_hot and (
            normalized == '/markets' or normalized.startswith('/markets?')
            or normalized.startswith('/markets/')
        ):
            chosen = '/events' + normalized[len('/markets'):]
            preferred = 'markets_hot'
            self.calls.append(('GET', chosen))
        if self.live_gets != 0:
            raise LiveOrdersForbidden()
        return {
            'method': 'GET',
            'path': chosen,
            'requested': normalized,
            'preferred_because': preferred,
            'body': self.bodies.get(chosen),
            'live': False,
            'live_gets': self.live_gets,
            'host': PUBLIC_HOST,
            'series': SERIES,
        }


def public_get(path, transport=None):
    """GET through the stub transport. The default transport performs no live GET."""
    if transport is None:
        transport = StubTransport()
    return transport.request('GET', path)


def assert_public_get(method):
    """GET is the only public capture verb. This function does not open a network client."""
    if method != 'GET':
        raise LiveOrdersForbidden()
    return None


def run_admit(path=None):
    """Refuse admit.py. Nothing is written and admitted_at stays null."""
    del path
    raise AdmitPyRefused('admit.py is refused')


def claim_live_r1p1(quote=None):
    """Refuse every promotion of the cache label to a live /series pin."""
    del quote
    raise CacheNotLiveR1P1()


def promote_series_fee(quote):
    """An examiner formula quote is not the KXATPMATCH series pin."""
    del quote
    raise CacheNotLiveR1P1()


def _pinned_feebook_resolution():
    """Read the imported table. KXATPMATCH has no override, so this is not a series pin."""
    table = feebook.load_series_table()
    if table.get('overrides'):
        raise CacheNotLiveR1P1()
    terms = feebook.resolve_terms(table, SERIES, 'taker')
    if terms.get('resolution') != 'default_unknown_series':
        raise CacheNotLiveR1P1()
    return terms['resolution']


def _fee_label(series, multiplier):
    if series in FOREIGN_SERIES or (
        isinstance(series, str) and any(series.startswith(token) for token in FOREIGN_SERIES)
    ):
        raise SeriesRefused(series)
    if series != SERIES:
        raise SeriesRefused(series)
    if multiplier in (0.5, '0.5'):
        raise FeeHalfRefused()
    if multiplier not in (1, '1'):
        raise FeeMultiplierRefused()
    resolution = _pinned_feebook_resolution()
    label = {
        'series': SERIES,
        'fee_type': FEE_TYPE,
        'multiplier': FEE_MULTIPLIER,
        'label': FEE_LABEL,
        'cache_labeled': True,
        'live_r1p1': False,
        'not_quadratic_x0_5': True,
        'fee_source': 'cache',
        'fee_src': FEE_SRC,
        'feebook_resolution_not_series_pin': resolution,
        'fee_dollars': None,
        'results': None,
        'pnl': None,
    }
    if label['cache_labeled'] is not True or label['live_r1p1'] is not False:
        raise CacheNotLiveR1P1()
    if label['multiplier'] != 1 or label['fee_type'] != FEE_TYPE:
        raise FeeMultiplierRefused()
    if label['fee_dollars'] is not None or label['results'] is not None or label['pnl'] is not None:
        raise InventedPnlRefused()
    return label


def fee_output(series=SERIES):
    """Cache-labeled quadratic_with_maker_fees ×1. No dollar fee is returned."""
    return _fee_label(series, FEE_MULTIPLIER)


def fee_output_with_multiplier(series, multiplier):
    """Refuse multiplier 0.5. Multiplier 1 returns the same cache label."""
    return _fee_label(series, multiplier)


def reopen_analysis_slice(arm=None):
    """ATP-FQ analysis_slice stays closed."""
    del arm
    raise ClosedParentRefused('ATP-FQ analysis_slice')


def reopen_join_gate(arm=None):
    """ATP-RJ join_gate stays closed."""
    del arm
    raise ClosedParentRefused('ATP-RJ join_gate')


def set_knob(name):
    """The only knob is inventory_slice."""
    if name in CLOSED_KNOBS:
        raise ClosedParentRefused(name)
    if name != KNOB:
        raise OrchestratorError('knob')
    return dict(INVENTORY_SLICE)


def ungate(name):
    """Named closed cards stay closed."""
    target = UNGATE_ALIASES.get(name, name)
    if target in DOES_NOT_UNGATE or name in DOES_NOT_UNGATE:
        raise UngateRefused()
    raise OrchestratorError('ungate')


def quote_depth(market):
    """Public size fields are not a depth ladder and are not n_books."""
    del market
    raise InventedDepthRefused()


def invent_fill(market=None, value=None):
    del market, value
    raise InventedFillRefused()


def invent_pnl(value=None):
    del value
    raise InventedPnlRefused()


def invent_inventory_delta(value=None):
    del value
    raise InventedInventoryRefused()


def invent_settlement_ts(market=None, value=None):
    del market, value
    raise InventedSettlementRefused()


def invent_market(ticker=None):
    del ticker
    raise InventedMarketRefused()


def copy_screen_counts_into_scorecard(summary=None):
    """Screen 28/14 and scout 48/24 stay pins. They are not scorecard counts."""
    del summary
    raise InventedMarketRefused()


def settled_join(panel):
    """No settlement join is published. The metric stays null."""
    if not isinstance(panel, dict):
        raise OrchestratorError('panel')
    if panel.get('results') is not None or panel.get('pnl') is not None:
        raise InventedFillRefused()
    return None


def infer_lee_ready(row):
    """Lee-Ready has no success path. Every input is refused."""
    del row
    raise LeeReadyRefused()


def refuse_adversary(label):
    """Named refuse labels. Nothing is traded."""
    if label not in ADVERSARY_LABELS:
        raise OrchestratorError('adversary label')
    if label == 'lee_ready':
        raise LeeReadyRefused()
    if label == 'invented_depth':
        raise InventedDepthRefused()
    if label == 'invented_markets':
        raise InventedMarketRefused()
    if label == 'invented_fills':
        raise InventedFillRefused()
    if label == 'invented_pnl':
        raise InventedPnlRefused()
    if label == 'invented_inventory':
        raise InventedInventoryRefused()
    if label == 'invented_settlement_ts':
        raise InventedSettlementRefused()
    if label == 'claim_live_r1p1':
        raise CacheNotLiveR1P1()
    if label == 'fee_half':
        raise FeeHalfRefused()
    if label == 'atp_fq_reopen':
        raise ClosedParentRefused('ATP-FQ')
    if label == 'atp_rj_reopen':
        raise ClosedParentRefused('ATP-RJ')
    if label == 'admit_py':
        raise AdmitPyRefused('admit.py is refused')
    if label in ('live_orders', 'logan_keys'):
        raise LiveOrdersForbidden()
    raise AdversaryRefused(ADVERSARY_LABELS[label])


def source_pin_paths():
    return (
        SOURCE_PINS,
        LAB_BUNDLE / SOURCE_PINS_NAME,
        GOVERNANCE_BUNDLE / SOURCE_PINS_NAME,
    )


def select_panel_path(stub_path=None, admitted_path=None):
    """Prefer panel_admitted.json when Clock has written one. This lab does not."""
    stub = PANEL_STUB if stub_path is None else Path(stub_path)
    admitted = PANEL_ADMITTED if admitted_path is None else Path(admitted_path)
    if admitted.is_file():
        return admitted
    return stub


def _validate_panel(payload):
    if not isinstance(payload, dict):
        raise OrchestratorError('panel')
    if payload.get('schema_id') != SCHEMA_ID:
        raise OrchestratorError('schema')
    if payload.get('panel_version') != PANEL_VERSION:
        raise PanelVersionRefused()
    if payload.get('series_ticker') != SERIES:
        raise SeriesRefused(str(payload.get('series_ticker')))
    events = payload.get('events') or []
    markets = payload.get('markets') or []
    if len(events) != PANEL_EVENTS_N or len(markets) != PANEL_MARKETS_N:
        raise InventedMarketRefused()
    for market in markets:
        ticker = market.get('ticker')
        if not isinstance(ticker, str) or not ticker.startswith(SERIES + '-'):
            raise SeriesRefused(str(ticker))
        assert_series(ticker)
    if payload.get('results') is not None or payload.get('pnl') is not None:
        raise InventedPnlRefused()
    return payload


def load_panel(stub_path=None, admitted_path=None):
    path = select_panel_path(stub_path, admitted_path)
    payload = json.loads(Path(path).read_text())
    return _validate_panel(payload)


def parent_import_status():
    """Hash-check closed parents. Do not reopen their knobs."""
    fq = sha256_file(ATP_FQ_FREEZE)
    rj = sha256_file(ATP_RJ_FREEZE)
    if fq != ATP_FQ_FREEZE_SHA256 or rj != ATP_RJ_FREEZE_SHA256:
        raise OrchestratorError('parent pin')
    return {
        'atp_fq_freeze_sha256': fq,
        'atp_rj_freeze_sha256': rj,
        'atp_fq_closed': True,
        'atp_rj_closed': True,
        'analysis_slice_reopened': False,
        'join_gate_reopened': False,
        'import_only': True,
    }


def screen_pin():
    """Read the sports-screen summary pin. Do not copy counts into the scorecard."""
    payload = json.loads(SPORTS_SUMMARY.read_text())
    if payload.get('series') != SERIES:
        raise SeriesRefused(str(payload.get('series')))
    if payload.get('fee_type') != FEE_TYPE:
        raise FeeMultiplierRefused()
    if str(payload.get('fee_multiplier')) != '1':
        raise FeeMultiplierRefused()
    if not str(payload.get('fee_src', '')).startswith('cache'):
        raise CacheNotLiveR1P1()
    if payload.get('n_markets') != SCREEN_MARKETS_N or payload.get('n_events') != SCREEN_EVENTS_N:
        raise InventedMarketRefused()
    return {
        'series': SERIES,
        'n_markets': SCREEN_MARKETS_N,
        'n_events': SCREEN_EVENTS_N,
        'fee_type': FEE_TYPE,
        'fee_multiplier': 1,
        'cache_labeled': True,
        'live_r1p1': False,
        'copied_into_scorecard': False,
        'results': None,
        'pnl': None,
        'unresolved_inventory': None,
    }


CLAIMED_PINS = (
    ('conductor_accept', ACCEPT_SHA256, 'lab/governance/astra/packets/' + ACCEPT_NAME),
    ('freeze', FREEZE_SHA256, 'lab/governance/astra/packets/' + FREEZE_NAME),
    ('panel_stub', PANEL_STUB_SHA256, 'lab/astra-capture/atp-kxatpmatch/panel_stub.json'),
    (
        'source_pins',
        SOURCE_PINS_SHA256,
        'lab/governance/astra/packets/Q6S1_KXATPMATCH_INVENTORY_REPROOF/SOURCE_PINS.json',
    ),
    (
        'empty_results',
        EMPTY_RESULTS_SHA256,
        'lab/governance/astra/packets/Q6S1_KXATPMATCH_INVENTORY_REPROOF/EMPTY_RESULTS.json',
    ),
    (
        'frozen_experiment',
        FROZEN_EXPERIMENT_SHA256,
        'lab/governance/astra/packets/Q6S1_KXATPMATCH_INVENTORY_REPROOF/FROZEN_EXPERIMENT.json',
    ),
    ('examiner_hold', HOLD_SHA256, 'lab/governance/astra/packets/' + HOLD_NAME),
    (
        'template_v12',
        TEMPLATE_V12_SHA256,
        'lab/governance/astra/templates/EXAMINER_KALSHI_SCORECARD_TEMPLATE_v1.2.json',
    ),
    (
        'p16_pdf',
        P16_PDF_SHA256,
        'lab/governance/astra/research/KALSHI_EDGE_RESEARCH_2026-09-24.pdf',
    ),
    (
        'scout_hunt',
        SCOUT_HUNT_SHA256,
        'packets/scout_cashcow_hunt_2026-09-22/scout_hunt_KXATPMATCH.json',
    ),
    (
        'sports_markets',
        SPORTS_MARKETS_SHA256,
        'lab/governance/astra/packets/scout_sports_q6_screen/raw/markets_open_KXATPMATCH.json',
    ),
    (
        'sports_summary',
        SPORTS_SUMMARY_SHA256,
        'lab/governance/astra/packets/scout_sports_q6_screen/raw/markets_open_KXATPMATCH_SUMMARY.json',
    ),
    (
        'atp_fq_freeze',
        ATP_FQ_FREEZE_SHA256,
        'lab/governance/astra/packets/ATP_KXATPMATCH_FEEQUEUE_HARNESS_FREEZE_2026-09-23.md',
    ),
    (
        'atp_rj_freeze',
        ATP_RJ_FREEZE_SHA256,
        'lab/governance/astra/packets/ATP_KXATPMATCH_SETTLED_RESOLUTION_JOIN_HARNESS_FREEZE_2026-09-24.md',
    ),
    (
        'settled_reget',
        SETTLED_REGET_SHA256,
        'lab/astra-capture/atp-kxatpmatch/settled_reget_2026-09-24.json',
    ),
    (
        'kick',
        KICK_SHA256,
        'lab/governance/astra/packets/CONDUCTOR_KICK_VARIANTS_Q6S1_KXATPMATCH_INVENTORY_REPROOF_FREEZE_2026-09-25.json',
    ),
    ('panel_admitted', None, 'lab/astra-capture/atp-kxatpmatch/panel_admitted.json'),
    (
        'live_series_fee',
        None,
        'lab/governance/astra/packets/Q6S1_KXATPMATCH_INVENTORY_REPROOF/live_series_fee.json',
    ),
    (
        'fresh_28_14_panel',
        None,
        'lab/astra-capture/atp-kxatpmatch/panel_stub_28_14.json',
    ),
    (
        'q6s1_scout_pdf',
        None,
        'lab/governance/astra/research/Q6S1_SCOUT.pdf',
    ),
    (
        'invented_fills',
        None,
        'lab/governance/astra/packets/Q6S1_KXATPMATCH_INVENTORY_REPROOF/invented_fills.json',
    ),
)


def digest_status(pin_specs=None):
    """Re-hash claimed pins. True only when every supplied pin is present and matches.

    The default list includes absent pins, so digest_all_match_claimed stays false.
    """
    specs = CLAIMED_PINS if pin_specs is None else tuple(pin_specs)
    rows = []
    for key, digest, rel in specs:
        path = PARENT / rel
        if not path.is_file() or digest is None:
            rows.append({
                'key': key,
                'present': path.is_file(),
                'match': False,
                'path': rel,
            })
            continue
        actual = sha256_file(path)
        rows.append({
            'key': key,
            'present': True,
            'match': actual == digest,
            'path': rel,
        })
    claimed = bool(rows) and all(row['match'] for row in rows)
    return {
        'pins': rows,
        'digest_all_match_claimed': claimed is True,
        'missing': [row['key'] for row in rows if not row['present']],
        'mismatch': [row['key'] for row in rows if row['present'] and not row['match']],
        'absent_pins': list(ABSENT_PINS),
    }


def assert_null_scorecard(payload):
    """Require every instrument field, results, and pnl, and require null."""
    if not isinstance(payload, dict):
        raise ScorecardPromotionRefused()
    for key in OUTPUT_KEYS:
        if key not in payload or payload[key] is not None:
            raise ScorecardPromotionRefused()
    return payload


def assert_v12_null(block):
    """Examiner scorecard v1.2 measured fields stay null."""
    if not isinstance(block, dict):
        raise ScorecardPromotionRefused()
    template = block.get('template') or {}
    if template.get('json_sha256') != TEMPLATE_V12_SHA256:
        raise OrchestratorError('template')
    if template.get('version') != 'v1.2':
        raise OrchestratorError('template')
    card = block.get('scorecard') or {}
    if card.get('verdict') is not None or card.get('status') != 'HOLD_PRE_PR':
        raise ScorecardPromotionRefused()
    if card.get('stub_ready') is not False or card.get('scored') is not False:
        raise ScorecardPromotionRefused()
    metrics = card.get('metrics') or {}
    for key in OUTPUT_KEYS:
        if key not in metrics or metrics[key] is not None:
            raise ScorecardPromotionRefused()
    common = block.get('common_scorecard') or {}
    if tuple(common.keys()) != COMMON_SCORECARD_KEYS:
        raise ScorecardPromotionRefused()
    for name, metric in common.items():
        if metric.get('value') is not None or metric.get('measured') is not False:
            raise ScorecardPromotionRefused()
        if name == 'calibration' and metric.get('emits_probabilities') is not False:
            raise ScorecardPromotionRefused()
    if block.get('study_label', {}).get('value') is not None:
        raise ScorecardPromotionRefused()
    gate = (block.get('preregistration_checklist') or {}).get('gate_status')
    if gate is not None:
        raise ScorecardPromotionRefused()
    counts = (block.get('preregistration_checklist') or {}).get('variants_declared_counts') or {}
    if counts.get('satisfied') != 8 or counts.get('n/a') != 4 or counts.get('missing') != 0:
        raise OrchestratorError('p16')
    stress = block.get('stress_sensitivity') or {}
    for name in ('one_tick_worse', 'fees_2x'):
        row = stress.get(name) or {}
        if row.get('measured') is not False:
            raise ScorecardPromotionRefused()
        if row.get('net_pnl_without_rewards') is not None or row.get('net_pnl_with_rewards') is not None:
            raise ScorecardPromotionRefused()
    dollars = block.get('executable_dollars_per_day') or {}
    if dollars.get('measured') is not False or dollars.get('value') is not None:
        raise ScorecardPromotionRefused()
    if dollars.get('median_day') is not None or dollars.get('p10_day') is not None:
        raise ScorecardPromotionRefused()
    fills = block.get('simulated_fills') or {}
    if fills.get('counts_toward_keep') is not False:
        raise ScorecardPromotionRefused()
    if (fills.get('fill_rate_simulated') or {}).get('value') is not None:
        raise ScorecardPromotionRefused()
    if block.get('all_score_values_null') is not True:
        raise ScorecardPromotionRefused()
    fee = block.get('fee_regime') or {}
    if fee.get('feebook_pin') != FEEBOOK_COMMIT or fee.get('rails_pin') != RAILS_COMMIT:
        raise OrchestratorError('fee regime')
    label = fee.get('fee_cache_label') or ''
    if 'CACHE-LABELED' not in label or '×1' not in label or '0.5' in label:
        raise FeeMultiplierRefused()
    return block


def published_scorecard():
    """Freeze outputs. Every instrument field is present and null."""
    scorecard = {key: None for key in OUTPUT_KEYS}
    assert_null_scorecard(scorecard)
    label = fee_output()
    scorecard['status'] = 'EMPTY_RESULTS_PRE_EXAMINER'
    scorecard['lee_ready'] = 'REFUSED'
    scorecard['examiner_status'] = 'HOLD_PRE_PR'
    scorecard['stub_ready'] = False
    scorecard['series_ticker'] = SERIES
    scorecard['knob'] = KNOB
    scorecard['fee_cache'] = label
    scorecard['cache_labeled'] = True
    scorecard['live_r1p1'] = False
    return scorecard


def write_scorecard(payload):
    """Refuse promotion. Nothing is written."""
    assert_null_scorecard(payload)
    raise ScorecardPromotionRefused()


def _report(arm, extra):
    if arm in CLOSED_PARENT_ARMS:
        raise ClosedParentRefused(CLOSED_PARENT_ARMS[arm])
    if arm not in INVENTORY_SLICE:
        raise UnknownSlice()
    published = published_scorecard()
    label = fee_output()
    report = {
        'experiment_id': EXPERIMENT_ID,
        'feature_family': FEATURE_FAMILY,
        'arm': arm,
        'inventory_slice': INVENTORY_SLICE[arm],
        'knob': KNOB,
        'source': 'panel',
        'series_ticker': SERIES,
        'published': published,
        'promoted': False,
        'strategy': None,
        'live_orders': False,
        'live_gets': 0,
        'lee_ready': 'REFUSED',
        'fee_pin': FEEBOOK_COMMIT,
        'rails_pin': RAILS_COMMIT,
        'fee_cache': label,
        'cache_labeled': True,
        'live_r1p1': False,
        'fee_import_only': True,
        'rails_import_only': True,
        'admit_py_run': False,
        'dual_cloud': False,
        'examiner_status': 'HOLD_PRE_PR',
        'stub_ready': False,
        'position_bucket': None,
        'inventory_bins': None,
    }
    report.update(extra)
    for key in OUTPUT_KEYS:
        report[key] = None
    assert_null_scorecard(report)
    assert_null_scorecard(published)
    if report['live_gets'] != 0 or report['cache_labeled'] is not True:
        raise OrchestratorError('report')
    if report['series_ticker'] != SERIES:
        raise SeriesRefused()
    return report


def conduct(arm, panel=None):
    """Schema for one inventory slice. Scorecard fields stay null."""
    if arm in CLOSED_PARENT_ARMS:
        raise ClosedParentRefused(CLOSED_PARENT_ARMS[arm])
    if arm not in INVENTORY_SLICE:
        raise UnknownSlice()
    if panel is None:
        panel = load_panel()
    events = panel.get('events') or []
    markets = panel.get('markets') or []
    for market in markets:
        ticker = str(market.get('ticker', ''))
        if not ticker.startswith(SERIES + '-'):
            raise SeriesRefused(ticker)
    if len(events) != PANEL_EVENTS_N or len(markets) != PANEL_MARKETS_N:
        if panel.get('panel_version') == PANEL_VERSION and panel.get('stub_status') == STUB_STATUS:
            raise InventedMarketRefused()
    extra = {
        'event_count': len(events),
        'market_count': len(markets),
        'scout_markets_n': SCOUT_MARKETS_N,
        'scout_events_n': SCOUT_EVENTS_N,
        'screen_markets_n': SCREEN_MARKETS_N,
        'screen_events_n': SCREEN_EVENTS_N,
        'screen_counts_copied_into_scorecard': False,
        'admitted_at': panel.get('admitted_at'),
    }
    report = _report(arm, extra)
    if report['event_count'] == SCREEN_EVENTS_N or report['market_count'] == SCREEN_MARKETS_N:
        raise InventedMarketRefused()
    if report['unresolved_inventory'] is not None or report['pnl'] is not None:
        raise InventedInventoryRefused()
    return report


def instrument_binding(panel=None):
    """Pin lock for the harness. Measured fields stay null."""
    if panel is None:
        panel = load_panel()
    pins = digest_status()
    parents = parent_import_status()
    label = fee_output()
    screen = screen_pin()
    return {
        'experiment_id': EXPERIMENT_ID,
        'feature_family': FEATURE_FAMILY,
        'series_ticker': SERIES,
        'knob': KNOB,
        'arms': dict(INVENTORY_SLICE),
        'panel_version': panel.get('panel_version'),
        'admitted_at': panel.get('admitted_at'),
        'stub_status': panel.get('stub_status'),
        'events_n': len(panel.get('events') or []),
        'markets_n': len(panel.get('markets') or []),
        'scout_events_n': SCOUT_EVENTS_N,
        'scout_markets_n': SCOUT_MARKETS_N,
        'screen_events_n': screen['n_events'],
        'screen_markets_n': screen['n_markets'],
        'feebook_commit': FEEBOOK_COMMIT,
        'rails_commit': RAILS_COMMIT,
        'fee_credit_rule_id': rails.FEE_CREDIT_RULE_ID,
        'fee_cache': label,
        'cache_labeled': True,
        'live_r1p1': False,
        'fee_source': 'cache',
        'live_gets': 0,
        'lee_ready': 'REFUSED',
        'dual_cloud': False,
        'admit_py_run': False,
        'examiner_status': 'HOLD_PRE_PR',
        'stub_ready': False,
        'results': None,
        'pnl': None,
        'inventory_delta_flat_vs_binned': None,
        'unresolved_inventory': None,
        'position_bucket_gap': None,
        'settled_join_n': None,
        'n_books': None,
        'freeze_sha256': FREEZE_SHA256,
        'panel_stub_sha256': PANEL_STUB_SHA256,
        'conductor_accept_sha256': ACCEPT_SHA256,
        'bundle_sha256': BUNDLE_SHA256,
        'template_v12_sha256': TEMPLATE_V12_SHA256,
        'digest_all_match_claimed': False if pins['missing'] or pins['mismatch'] else pins['digest_all_match_claimed'],
        'digest_missing': pins['missing'],
        'absent_pins': list(ABSENT_PINS),
        'base_commit': BASE_COMMIT,
        'atp_fq_closed': parents['atp_fq_closed'],
        'atp_rj_closed': parents['atp_rj_closed'],
        'analysis_slice_reopened': False,
        'join_gate_reopened': False,
        'nfl_000_pointer': NFL_000_POINTER,
    }


def frozen_output_snapshot():
    """Read freeze files. Does not modify them."""
    payloads = {
        'frozen': json.loads(FROZEN_EXPERIMENT.read_text()),
        'empty': json.loads(EMPTY_RESULTS.read_text()),
        'bundle_frozen': json.loads((LAB_BUNDLE / 'FROZEN_EXPERIMENT.json').read_text()),
        'bundle_results': json.loads((LAB_BUNDLE / 'results.json').read_text()),
        'governance_frozen': json.loads((GOVERNANCE_BUNDLE / 'FROZEN_EXPERIMENT.json').read_text()),
        'governance_empty': json.loads((GOVERNANCE_BUNDLE / 'EMPTY_RESULTS.json').read_text()),
    }
    snapshot = {}
    for name, payload in payloads.items():
        assert_null_scorecard(payload)
        for key in OUTPUT_KEYS:
            snapshot['%s.%s' % (name, key)] = None
        if name.endswith('frozen') or name == 'frozen':
            if payload.get('series_ticker') != SERIES:
                raise SeriesRefused()
            if payload.get('digest_all_match_claimed') is not False:
                raise OrchestratorError('digest')
    assert_v12_null(payloads['empty']['examiner_scorecard_v1_2'])
    return snapshot
