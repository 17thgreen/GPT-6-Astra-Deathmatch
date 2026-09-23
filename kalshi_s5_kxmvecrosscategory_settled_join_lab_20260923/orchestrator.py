"""S5 KXMVECROSSCATEGORY settled-resolution join harness.

Measurement only. One knob: join_gate. This module does not edit the
S5 FILLLEGS lab, the MVE-FL stub, the R2P3-RJ lab, the S4-RJ lab, the
NHL-RJ lab, the C3-RJ lab, the C5-RJ lab, the R3P3-RJ lab, feebook,
rails, Cap-SR, or any FQ sibling. It does not place orders, does not
read Logan keys, does not run admit.py, and does not write scorecard
metrics.

The checkout freeze, scout reget, seed summary, panel stub, settled
reget, and accept match the attached sha256 values. The panel stub keeps
admitted_at null. The settled list on the attached reget is HTTP 200
with limit 20 and a cursor present. Markets past that cursor are not
invented. Earlier settled, finalized, and events lists stay the honest
429 gaps. SHARD1 stays the honest 429 gap. occurrence_datetime is null
on the settled cohort. J1 uses expected_expiration_time for that honest
null and does not invent occurrence_datetime. Parent ticker GETs in the
scout are finalized with a nonempty result. Those results are not copied
onto the panel stub. Lee-Ready is refused. Settled results, depth,
fills, and PnL are not invented. Scout settled_nonempty_result_N is a
pin and is not copied into settled_join_n.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PARENT = ROOT.parent

LAB_DIRECTORY = 'kalshi_s5_kxmvecrosscategory_settled_join_lab_20260923'
EXPERIMENT_ID = 'S5-KXMVECROSSCATEGORY-SETTLED-RESOLUTION-JOIN-HARNESS'
FEATURE_FAMILY = 'S5-RJ'
SCOUT_PACKET = 'S5-KXMVECROSSCATEGORY-SETTLED-JOIN'
PARENT_PACKET_ID = 'S5-KXMVECROSSCATEGORY-MEAS'
PANEL_VERSION = '2026-09-22.s5-kxmvecrosscategory-v0'
SCHEMA_ID = 'astra.registry.s5_kxmvecrosscategory_panel.v0'
SERIES = 'KXMVECROSSCATEGORY'
SHARD1 = 'KXMVECROSSCATEGORY-SHARD1'
RELATED_SERIES = 'KXMVESPORTSMULTIGAMEEXTENDED'
SIBLING_SERIES = (SHARD1, RELATED_SERIES)
STUB_STATUS = 'PANEL_SCHEMA_STUB_SEED_NOT_ADMITTED'
PANEL_PURPOSE = 'measurement_gate'
COHORT_KIND = 'bounded_seed_sample_vs_open_inventory_gt_200'
KNOB = 'join_gate'
J0 = 'J0'
J1 = 'J1'
ARMS = (J0, J1)
JOIN_GATE = {
    J0: 'nonempty_result_required',
    J1: 'occurrence_datetime_match',
}
ACCEPT_ARMS = {
    J0: 'nonempty_result_required',
    J1: 'occurrence_datetime_match (expected_expiration_time when occurrence_datetime null honest)',
}
FINALIZED_RESULTS = ('yes', 'no')
SCOUT_NONEMPTY_N = 20
YES_N = 4
NO_N = 16
SETTLED_LIST_ROW_N = 20
PARENT_SEED_N = 5
PARENT_FINALIZED_N = 5
PANEL_EVENTS_N = 21
PANEL_MARKETS_N = 5
PANEL_BASE_EVENTS_N = 16
PANEL_SHARD1_EVENTS_N = 5
PANEL_STUB_ACTIVE_N = 2
PANEL_STUB_FINALIZED_N = 3
RELATED_SERIES_N = 20
HONEST_GAP_N = 4
ROW_LABEL_N = 29
SETTLED_LIST_LIMIT = 20
PARENT_KERNEL_SHA256 = 'a28932ba13b4913b69c48b73dde8ba066cebd212670d0b1cbb5ea8e93734b8ba'
SCOUT_CITE_PANEL = 'lab/governance/astra/packets/scout_s5_kxmvecrosscategory/'
FREEZE_CITE_PANEL = 'lab/governance/astra/packets/S5_KXMVECROSSCATEGORY_MEASUREMENT_FREEZE_KERNEL_2026-09-22.md'
STUBBED_AT = '2026-09-22T23:56:34Z'
ADMIT_GATE_STATUS = 'WAIT_CLOCK_JOIN'
SETTLED_SOURCE = 'markets_settled_KXMVECROSSCATEGORY_lim20.json'
PARENT_SOURCE = 'GET_/markets/{ticker}_parent_seed'
COLLECTION = 'KXMVECROSSCATEGORY-R'
FEE_OVERRIDE = 'quadratic_with_combo_maker_fees'
PARENT_SEED_TICKERS = (
    'KXMVECROSSCATEGORY-S20264CF5F0166A4-D93D828F247',
    'KXMVECROSSCATEGORY-S2026FFD15C7F85E-073CF08455C',
    'KXMVECROSSCATEGORY-S2026FAFE350FA8F-2DEC47CF182',
    'KXMVECROSSCATEGORY-S2026FAFE350FA8F-D22687ACA9C',
    'KXMVECROSSCATEGORY-S2026FAFE350FA8F-20154DED5EC',
)
PARENT_SEED_RESULTS = {
    'KXMVECROSSCATEGORY-S20264CF5F0166A4-D93D828F247': 'no',
    'KXMVECROSSCATEGORY-S2026FFD15C7F85E-073CF08455C': 'no',
    'KXMVECROSSCATEGORY-S2026FAFE350FA8F-2DEC47CF182': 'no',
    'KXMVECROSSCATEGORY-S2026FAFE350FA8F-D22687ACA9C': 'no',
    'KXMVECROSSCATEGORY-S2026FAFE350FA8F-20154DED5EC': 'no',
}
PARENT_SEED_STATUSES = {
    'KXMVECROSSCATEGORY-S20264CF5F0166A4-D93D828F247': 'finalized',
    'KXMVECROSSCATEGORY-S2026FFD15C7F85E-073CF08455C': 'finalized',
    'KXMVECROSSCATEGORY-S2026FAFE350FA8F-2DEC47CF182': 'finalized',
    'KXMVECROSSCATEGORY-S2026FAFE350FA8F-D22687ACA9C': 'finalized',
    'KXMVECROSSCATEGORY-S2026FAFE350FA8F-20154DED5EC': 'finalized',
}
PARENT_EXPECTED_EXPIRATION = {
    'KXMVECROSSCATEGORY-S20264CF5F0166A4-D93D828F247': '2026-09-23T04:40:00Z',
    'KXMVECROSSCATEGORY-S2026FFD15C7F85E-073CF08455C': '2026-10-11T00:00:00Z',
    'KXMVECROSSCATEGORY-S2026FAFE350FA8F-2DEC47CF182': '2026-10-11T00:00:00Z',
    'KXMVECROSSCATEGORY-S2026FAFE350FA8F-D22687ACA9C': '2026-10-11T00:00:00Z',
    'KXMVECROSSCATEGORY-S2026FAFE350FA8F-20154DED5EC': '2026-10-11T00:00:00Z',
}
PANEL_STATUS_OBSERVED = {
    'KXMVECROSSCATEGORY-S20264CF5F0166A4-D93D828F247': 'active',
    'KXMVECROSSCATEGORY-S2026FFD15C7F85E-073CF08455C': 'active',
    'KXMVECROSSCATEGORY-S2026FAFE350FA8F-2DEC47CF182': 'finalized',
    'KXMVECROSSCATEGORY-S2026FAFE350FA8F-D22687ACA9C': 'finalized',
    'KXMVECROSSCATEGORY-S2026FAFE350FA8F-20154DED5EC': 'finalized',
}
PARENT_EVENT_MARKETS = {
    'KXMVECROSSCATEGORY-S20264CF5F0166A4': (
        'KXMVECROSSCATEGORY-S20264CF5F0166A4-D93D828F247',
    ),
    'KXMVECROSSCATEGORY-S2026FFD15C7F85E': (
        'KXMVECROSSCATEGORY-S2026FFD15C7F85E-073CF08455C',
    ),
    'KXMVECROSSCATEGORY-S2026FAFE350FA8F': (
        'KXMVECROSSCATEGORY-S2026FAFE350FA8F-2DEC47CF182',
        'KXMVECROSSCATEGORY-S2026FAFE350FA8F-D22687ACA9C',
        'KXMVECROSSCATEGORY-S2026FAFE350FA8F-20154DED5EC',
    ),
}
PANEL_EVENTS = (
    'KXMVECROSSCATEGORY-S20264CF5F0166A4',
    'KXMVECROSSCATEGORY-S2026FFD15C7F85E',
    'KXMVECROSSCATEGORY-S2026FAFE350FA8F',
    'KXMVECROSSCATEGORY-S2026FFB9C9464EB',
    'KXMVECROSSCATEGORY-S2026FEAC93F2BEC',
    'KXMVECROSSCATEGORY-S2026FCFAAD0AA7C',
    'KXMVECROSSCATEGORY-S2026FB8C5C67DE5',
    'KXMVECROSSCATEGORY-S2026FB6F941E5CC',
    'KXMVECROSSCATEGORY-S2026FB60658D9D6',
    'KXMVECROSSCATEGORY-S2026FAEF90E8775',
    'KXMVECROSSCATEGORY-S2026F8A58CFE650',
    'KXMVECROSSCATEGORY-S2026F88D8962DB7',
    'KXMVECROSSCATEGORY-S2026F86E0B00B9E',
    'KXMVECROSSCATEGORY-S2026F7A3BA6681C',
    'KXMVECROSSCATEGORY-S2026F7396D7171B',
    'KXMVECROSSCATEGORY-S2026F70665FB10E',
    'KXMVECROSSCATEGORY-SHARD1-S2026FF7C4259D33',
    'KXMVECROSSCATEGORY-SHARD1-S2026FE64A14BA11',
    'KXMVECROSSCATEGORY-SHARD1-S2026FB5FB58764E',
    'KXMVECROSSCATEGORY-SHARD1-S2026FAFDE6BAB55',
    'KXMVECROSSCATEGORY-SHARD1-S2026F9D204D4217',
)
SETTLED_TICKERS = (
    'KXMVECROSSCATEGORY-S20264290BCB7D95-E84ABA76CF5',
    'KXMVECROSSCATEGORY-S20269A5366449A1-157C213FDFB',
    'KXMVECROSSCATEGORY-S202630B65D00180-29FCBDB1735',
    'KXMVECROSSCATEGORY-S2026952B279B225-B0FB5B7DABC',
    'KXMVECROSSCATEGORY-S2026E8EB758CD54-35F33E47E27',
    'KXMVECROSSCATEGORY-S2026CD75BDCFBFB-0926E544302',
    'KXMVECROSSCATEGORY-S2026D21C3FC056E-98426CAF209',
    'KXMVECROSSCATEGORY-S202636A38D2D6D0-A8E27A0E923',
    'KXMVECROSSCATEGORY-S202698E04A85492-E9B4AB04E83',
    'KXMVECROSSCATEGORY-S2026A317451EBAE-309674C4265',
    'KXMVECROSSCATEGORY-S20267D8D7FC5609-32A25CBE91D',
    'KXMVECROSSCATEGORY-S2026C147CAD5F9F-205271B6A27',
    'KXMVECROSSCATEGORY-S2026540B4738132-E7BD117C749',
    'KXMVECROSSCATEGORY-S2026BF280F2F996-AEA4F7EEE51',
    'KXMVECROSSCATEGORY-S2026CC194D2E1B6-C17F32F43F4',
    'KXMVECROSSCATEGORY-S202607A2B594FE2-923CD31CA59',
    'KXMVECROSSCATEGORY-S20269BD9A146EB2-DF6228FD086',
    'KXMVECROSSCATEGORY-S20261BD80F82A3B-247780EF168',
    'KXMVECROSSCATEGORY-S2026E1456692009-3D8F92E6B9B',
    'KXMVECROSSCATEGORY-S2026DC2703D8D91-98DB5FEBBF1',
)
HONEST_GAPS = (
    'GET /markets?series_ticker=KXMVECROSSCATEGORY&status=settled earlier list attempts 429',
    'GET /markets?series_ticker=KXMVECROSSCATEGORY&status=finalized list 429',
    'GET /events?series_ticker=KXMVECROSSCATEGORY&status=closed|settled list 429',
    'GET /series/KXMVECROSSCATEGORY-SHARD1 429',
)
LIST_429 = '429_honest'
LIST_200 = '200'
HTTP_HONESTY = {
    'settled_list_KXMVECROSSCATEGORY': '200',
    'settled_list_earlier_attempts_429_honest': True,
    'settled_list_KXMVESPORTSMULTIGAMEEXTENDED': '200',
    'finalized_list_KXMVECROSSCATEGORY_attempts': '429_honest_then_not_required',
    'events_closed_settled_attempts': '429_honest',
    'series_KXMVECROSSCATEGORY': '200',
    'series_KXMVESPORTSMULTIGAMEEXTENDED': '200',
    'series_SHARD1': '429_honest',
}
SCOUT_METHOD = (
    'GET-only /markets?series_ticker=KXMVECROSSCATEGORY&status=settled&limit=20 '
    '(earlier settled/finalized/events list attempts 429 honest; SHARD1 series 429 honest; '
    'parent seed ticker GETs finalized/nonempty)'
)
SEED_METHOD = (
    'GET-only /markets?status=settled on KXMVECROSSCATEGORY '
    '(earlier list 429s honest; parent seed ticker GETs finalized/nonempty)'
)
PARENT_NOTE = (
    'Parent panel stub seeds (2026-09-22.s5-kxmvecrosscategory-v0) reget via '
    'GET /markets/{ticker}: all 5 status=finalized with nonempty result (honest). '
    'Stub still admitted_at null — Variants does NOT run admit.py.'
)
OCCURRENCE_NOTE = (
    'occurrence_datetime null on settled lim20 cohort (honest API gap). '
    'J1 uses expected_expiration_time as available public clock pin when '
    'occurrence_datetime absent — do not invent occurrence_datetime.'
)
SCOUT_KEYS = {
    'packet',
    'feature_family',
    'series',
    'sibling_series_noted',
    'settled_nonempty_result_N',
    'settled_list_limit',
    'settled_list_http',
    'settled_list_cursor_present',
    'method',
    'host',
    'parent_seeds_finalized_nonempty_N',
    'parent_seed_tickers',
    'parent_seed_results',
    'parent_seed_statuses',
    'parent_panel_seeds_note',
    'occurrence_datetime_present_on_settled_N',
    'expected_expiration_time_present_on_settled_N',
    'occurrence_datetime_sot_note',
    'occurrence_datetime_sot_match_all_settled_seeds',
    'expected_expiration_time_present_all_settled',
    'related_series_settled_KXMVESPORTSMULTIGAMEEXTENDED_N',
    'related_series_settled_http',
    'open_list_n',
    'open_list_http',
    'markets',
    'parent_seed_markets',
    'http_honesty',
    'scouted_at_et',
}
SEED_KEYS = {
    'settled_nonempty_result_N',
    'settled_list_attempted_KXMVECROSSCATEGORY',
    'settled_list_earlier_attempts',
    'finalized_list_attempted_KXMVECROSSCATEGORY',
    'events_closed_settled_attempted',
    'method',
    'parent_seed_tickers',
    'parent_seeds_finalized_nonempty_N',
    'parent_seed_results',
    'parent_seed_statuses',
    'overnight_finalized_nonempty_N',
    'occurrence_datetime_present_on_settled_N',
    'expected_expiration_time_present_all_settled',
    'occurrence_datetime_match_all_settled_seeds',
    'markets',
    'related_fee_pin_series_settled_KXMVESPORTSMULTIGAMEEXTENDED_N',
}
MARKET_KEYS = {
    'ticker',
    'status',
    'result',
    'nonempty_result',
    'close_time',
    'occurrence_datetime',
    'expected_expiration_time',
    'expiration_time',
    'event_ticker',
    'mve_collection_ticker',
    'source',
}
SHARED_FIELDS = (
    'status',
    'result',
    'close_time',
    'expected_expiration_time',
    'expiration_time',
    'event_ticker',
    'mve_collection_ticker',
)
FEEBOOK_COMMIT = '22371178cb2663250b4762f328069571c48cb551'
RAILS_COMMIT = '6a28e0d6254327ea4e6451c781bec56215ac6cac'
BASE_COMMIT = 'b2c1639a77f62114572fd41182f8a3c5ef70cad1'
R2P3_ACCEPT_SHA256 = 'e5218cf2511607211ec1d825a9dad36abaee3d9cfda24488524c3d6bcbe3a565'
FREEZE_SHA256 = 'cd264a4d41ef055d1cbca80a5dbe6756746211537fb24799dca9dde8980cb799'
SCOUT_SHA256 = '33db60a50f2e7746315f4603b9f78a9260145cb49d0250e141471de46f4df9e3'
SEED_SHA256 = '3bc4aa5f44d7d31295dfd25f7bac3a3e39463c237315e8228c3fcf434d08419a'
PANEL_STUB_SHA256 = '4918b820d454c5f997ea100917859f7e9467d92933bed1bc8a55c81ab8ce5b8e'
REGET_SHA256 = '91111f20586a1b684e430baa0e8b62a3fffc7d510de99e43bab7d213dfeb26da'
ACCEPT_SHA256 = '495675175589c08122bc57375dd8e7d00aea9f4a154df3aff086b015a2513a8c'
FROZEN_SHA256 = '4bb57f793e5eb6ed3fed664843e1ad00f2e204739e3014df96a56e342036b8b0'
EMPTY_SHA256 = '9257b65bcb892cd5139fd25433cbe4b9a1704045fea86890bfa3e0ed56c1c88c'
HOLD_SHA256 = '3bce25f0dacb43f93bafe2229839bece190ff889b3fdf00a21dc1aac583b0ff7'
PIN_SHA256 = '1e071f2cebdc18e198901e33af49387a751ecc1fe85bd14a0cb09a1f3ff6416f'
DIGESTS_SHA256 = '63d8b10210fb7d20c6a9fead983c6d084292eff9eb87e20839bff62119e1405b'
SOURCE_PINS_SHA256 = '75f7ef854c653bdf699e72a628a172b4a8dc161d7a4e0441c97ddcaad0f3d8b6'
FREEZE_BYTES = 6285
SCOUT_BYTES = 16235
SEED_BYTES = 12306
PANEL_BYTES = 28570
REGET_BYTES = 71460
ACCEPT_BYTES = 2062
FROZEN_BYTES = 1070
EMPTY_BYTES = 180
HOLD_BYTES = 3026
PIN_BYTES = 2844
DIGESTS_BYTES = 1405
SOURCE_PINS_BYTES = 6576
ACCEPT_STAMPED_AT = '2026-09-23T17:36:00-04:00'
FROZEN_STAMPED_AT = '2026-09-23T17:33:00-04:00'
SCOUT_FETCHED_AT = '2026-09-23T17:33:00-04:00'
HOLD_STAMPED_AT = '2026-09-23T17:33:00-04:00'
EMPTY_NOTE = 'pre-ACCEPT empty; S5-RJ measurement join only'
PUBLIC_HOST = 'https://api.elections.kalshi.com/trade-api/v2'
PANEL_HOST = 'api.elections.kalshi.com'
OUT_OF_SCOPE_ROUTE = 'POST /portfolio/orders'
ORTHOGONAL_PIN = 'packets/MAXIMIZE_PIN_2026-09-23_1733ET.md'
PRIOR_DONE = 'R2P3-RJ PR46 main@' + BASE_COMMIT
SCORECARD_FIELDS = (
    'settled_join_n',
    'occurrence_match_n',
    'admit_ready_flag',
)
OUTPUT_KEYS = SCORECARD_FIELDS + ('results', 'pnl')
HOLD_METRICS = (
    'results',
    'pnl',
    'settled_join_n',
    'occurrence_match_n',
    'admit_ready_flag',
)
ACCEPT_HARD_REFUSE = (
    'invent_settled_result',
    'invent_fills',
    'invent_depth',
    'Lee-Ready',
    'FQ_reopen',
    'S5_FILLLEGS_reopen',
    'MVE_FL_reopen',
    'Cap-SR_reopen',
    'C3_RJ_reopen',
    'C5_RJ_reopen',
    'R3P3_RJ_reopen',
    'NHL_RJ_reopen',
    'S4_RJ_reopen',
    'R2P3_RJ_reopen',
    'ungate_S1_S2_R2P4',
    'Arm_B_touch',
    'admit_py_by_Variants',
    'live_orders',
    'copy_scout_N_into_settled_join_n',
    'Conductor_pulse_cloud_kick',
)
DOES_NOT_UNGATE = ('S1', 'S2', 'R2-P4')
ORTHOGONAL_TO = ('S5-FILLLEGS', 'MVE-FL')
VOLUME_FIELDS = ('volume_fp', 'volume_24h_fp', 'open_interest_fp')
ADVERSARY_LABELS = {
    'lee_ready': 'Lee-Ready is refused',
    'invent_settled_result': 'invented settled result is refused',
    'invented_result': 'invented settled result is refused',
    'invent_fills': 'invented fills are refused',
    'invented_fills': 'invented fills are refused',
    'invent_depth': 'invented depth is refused',
    'invented_depth': 'invented depth is refused',
    'invented_pnl': 'invented pnl is refused',
    'list_429_backfill': 'settled finalized and events list 429 backfill is refused',
    'shard1_backfill': 'SHARD1 429 backfill is refused',
    'cursor_follow': 'settled-list cursor follow is refused',
    'related_series_invent': 'related-series market invent is refused',
    'parent_seed_invent': 'invented parent settlement is refused',
    'invent_occurrence': 'invented occurrence_datetime is refused',
    'invented_occurrence': 'invented occurrence_datetime is refused',
    'filllegs_reopen': 'S5 FILLLEGS reopen is refused',
    'mve_fl_reopen': 'MVE-FL reopen is refused',
    'fq_reopen': 'FQ reopen is refused',
    's4_fq_reopen': 'S4-FQ reopen is refused',
    's4_rj_reopen': 'S4-RJ reopen is refused',
    'nhl_fq_reopen': 'NHL-FQ reopen is refused',
    'cpi_fq_reopen': 'CPI-FQ reopen is refused',
    'atp_fq_reopen': 'ATP-FQ reopen is refused',
    'eth_fq_reopen': 'ETH-FQ reopen is refused',
    'cap_sr_reopen': 'Cap-SR reopen is refused',
    'empty_ob_reopen': 'EMPTY-OB reopen is refused',
    'c3_rj_reopen': 'C3-RJ reopen is refused',
    'c5_rj_reopen': 'C5-RJ reopen is refused',
    'r3p3_rj_reopen': 'R3P3-RJ reopen is refused',
    'nhl_rj_reopen': 'NHL-RJ reopen is refused',
    'r2p3_rj_reopen': 'R2P3-RJ reopen is refused',
    'arm_b': 'Arm B is refused',
    'q7_arm_b': 'Arm B is refused',
    'admit_py': 'admit.py is refused',
    'live_orders': 'live orders are refused',
    'logan_keys': 'Logan keys are refused',
    'ungate': 'S1 S2 R2-P4 stay gated',
    'copy_scout_n': 'scout N is not settled_join_n',
    'conductor_pulse_cloud': 'Conductor pulse cloud is refused',
}
DOES_NOT_MODIFY = (
    'kalshi_feebook_lab_20260922',
    'kalshi_rails_lab_20260922',
    'kalshi_r2p1_hygiene_000_lab_20260922',
    'kalshi_queue_fragility_000_lab_20260922',
    'kalshi_soft_blended_reserves_000_lab_20260923',
    'kalshi_cap_sr_effects_000_lab_20260923',
    'kalshi_capital_structure_lab_20260922',
    'kalshi_examiner_fee_queue_honesty_000_lab_20260922',
    'kalshi_c1_kxufcfight_honesty_lab_20260922',
    'kalshi_c1_empty_ob_lab_20260923',
    'kalshi_c2_kxnhlgame_feequue_lab_20260923',
    'kalshi_c3_kxhighny_bordering_lab_20260923',
    'kalshi_c3_kxhighny_settled_join_lab_20260923',
    'kalshi_c4_kxcpi_feequue_lab_20260923',
    'kalshi_c5_kxbtc15m_honesty_lab_20260923',
    'kalshi_c5_kxbtc15m_settled_join_lab_20260923',
    'kalshi_atp_kxatpmatch_feequue_lab_20260923',
    'kalshi_eth_kxeth15m_feequue_lab_20260923',
    'kalshi_r3p3_fl_maker_taker_lab_20260923',
    'kalshi_r3p3_fl_settled_join_lab_20260923',
    'kalshi_r3p4_l2_cat_lab_20260923',
    'kalshi_r3p4_l2_sf_lab_20260923',
    'kalshi_r3_p4_l2_shape_lab_20260922',
    'kalshi_r3_p2_queue_position_lab_20260923',
    'kalshi_s4_ncaaf_feequue_lab_20260923',
    'kalshi_s5_mve_filllegs_lab_20260923',
    'kalshi_r2p3_prop_ladder_lab_20260923',
    'kalshi_r2p3_kxnflpassyds_settled_join_lab_20260923',
    'kalshi_r2p5_sot_id_lab_20260923',
    'kalshi_kxnhlgame_settled_join_lab_20260923',
    'kalshi_kxncaafgame_settled_join_lab_20260923',
    'nfl_factorial_lab_20260921',
    'nfl_paircheck_lab_20260922',
    'nfl_q7_rehab_p1_cadence_20260923',
    'packets/R2_P3_PROP_LADDER_HARNESS',
    'packets/R2P3_KXNFLPASSYDS_SETTLED_JOIN_HARNESS',
    'packets/S4_KXNCAAFGAME_SETTLED_JOIN_HARNESS',
    'packets/S4_KXNCAAFGAME_FEEQUEUE_HARNESS',
    'packets/S5_KXMVECROSSCATEGORY_FILLLEGS_HARNESS',
    'lab/astra-capture/s5-kxmvecrosscategory/panel_stub.json',
    'lab/astra-capture/s5-kxmvecrosscategory/README.md',
    'lab/governance/astra/packets/r3_p2_queue_position/results/demo_queue_sample_series.json',
)
FREEZE_NAME = 'S5_KXMVECROSSCATEGORY_SETTLED_RESOLUTION_JOIN_HARNESS_FREEZE_2026-09-23.md'
SCOUT_NAME = 'scout_settled_rejoin_S5_KXMVECROSSCATEGORY.json'
SEED_NAME = 'SEED_SETTLED_SUMMARY.json'
PANEL_ALIAS = 'S5_KXMVECROSSCATEGORY_PANEL_STUB_2026-09-22.json'
REGET_NAME = 'settled_reget_2026-09-23.json'
ACCEPT_NAME = 'CONDUCTOR_ACCEPT_S5_KXMVECROSSCATEGORY_SETTLED_JOIN_HARNESS_2026-09-23.json'
HOLD_NAME = 'EXAMINER_HOLD_S5_KXMVECROSSCATEGORY_SETTLED_JOIN_HARNESS_PRE_PR_2026-09-23.json'
PIN_NAME = 'MAXIMIZE_PIN_2026-09-23_1733ET.md'
DIGESTS_NAME = 'DIGESTS.txt'
SOURCE_PINS_NAME = 'SOURCE_PINS.json'
LAB_BUNDLE = ROOT / 'S5_KXMVECROSSCATEGORY_SETTLED_RESOLUTION_JOIN_HARNESS'
SCIENCE = PARENT / 'lab' / 'astra-science' / LAB_DIRECTORY
PACKET_DIR = PARENT / 'packets' / 'S5_KXMVECROSSCATEGORY_SETTLED_JOIN_HARNESS'
GOV = PARENT / 'lab' / 'governance' / 'astra' / 'packets'
SCOUT_CITE_DIR = GOV / 'scout_s5_settled_rejoin_2026-09-23'
FREEZE_GOV = GOV / FREEZE_NAME
PANEL_GOV = GOV / PANEL_ALIAS
PACKET = ROOT / FREEZE_NAME
SCOUT_PATH = ROOT / SCOUT_NAME
SEED_PATH = ROOT / SEED_NAME
REGET_PATH = ROOT / REGET_NAME
CONDUCTOR_ACCEPT = ROOT / ACCEPT_NAME
FROZEN_EXPERIMENT = ROOT / 'FROZEN_EXPERIMENT.json'
EMPTY_RESULTS = ROOT / 'results' / 'EMPTY_RESULTS.json'
EXAMINER_HOLD = ROOT / HOLD_NAME
MAXIMIZE_PIN = ROOT / PIN_NAME
DIGESTS_PATH = ROOT / DIGESTS_NAME
SOURCE_PINS = ROOT / SOURCE_PINS_NAME
PANEL_CAPTURE = PARENT / 'lab' / 'astra-capture' / 's5-kxmvecrosscategory' / 'panel_stub.json'
PANEL_ADMITTED = PARENT / 'lab' / 'astra-capture' / 's5-kxmvecrosscategory' / 'panel_admitted.json'
REGET_CITE = PARENT / 'lab' / 'astra-capture' / 's5-kxmvecrosscategory' / REGET_NAME
PIN_CITE = PARENT / 'packets' / PIN_NAME
ACCEPT_ROOT = PARENT / 'packets' / ACCEPT_NAME
ADMIT_PY = ROOT / 'admit.py'


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


class LeeReadyRefused(OrchestratorError):
    """Lee-Ready has no success path."""

    def __init__(self):
        super().__init__('Lee-Ready refused')


class InventedResultRefused(OrchestratorError):
    """A settled result was invented or a 429 list gap was backfilled."""

    def __init__(self):
        super().__init__('invented settled result')


class InventedFillRefused(OrchestratorError):
    """A fill was invented from volume or from a gap."""

    def __init__(self):
        super().__init__('invented fill')


class InventedDepthRefused(OrchestratorError):
    """Quote size is not a depth ladder."""

    def __init__(self):
        super().__init__('invented depth')


class InventedSoTRefused(OrchestratorError):
    """occurrence_datetime is not invented when the API left it null."""

    def __init__(self):
        super().__init__('invented occurrence_datetime')


class OccurrenceIntegrityRefused(OrchestratorError):
    """Scout, seed, and reget clocks disagree."""

    def __init__(self):
        super().__init__('occurrence clock')


class AdmitPyRefused(OrchestratorError):
    """Variants does not run admit.py and does not write admitted_at."""

    def __init__(self):
        super().__init__('admit.py refused')


class ExaminerNotReady(OrchestratorError):
    """Examiner stays HOLD pre-PR until after merge and Clock admit."""

    def __init__(self):
        super().__init__('Examiner HOLD pre-PR')


class UngateRefused(OrchestratorError):
    """S1, S2, and R2-P4 stay gated."""

    def __init__(self):
        super().__init__('does not ungate S1 S2 R2-P4')


class PanelVersionRefused(OrchestratorError):
    """The panel file is not the pinned S5 seed."""

    def __init__(self):
        super().__init__('panel_version')


class UnknownGate(OrchestratorError):
    """The only knob is the two named join gates."""

    def __init__(self):
        super().__init__('join_gate')


class InventedMarketRefused(OrchestratorError):
    """A ticker is outside the authentic reget and the panel stub."""

    def __init__(self):
        super().__init__('invented market')


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


def run_admit(path=None):
    """Variants does not admit the panel."""
    del path
    raise AdmitPyRefused()


def ungate(name):
    """S1, S2, and R2-P4 stay queued."""
    if name in DOES_NOT_UNGATE:
        raise UngateRefused()
    raise OrchestratorError('ungate')


def claim_admit_ready():
    """admit_ready_flag stays null. Clock admit is not this harness."""
    raise ExaminerNotReady()


def claim_examiner_ready():
    """Examiner HOLD pre-PR until after merge and sha verify."""
    raise ExaminerNotReady()


def quote_depth(market):
    """Public size fields are not a depth ladder."""
    del market
    raise InventedDepthRefused()


def invent_fill(market=None, value=None):
    """Volume on a market quote is not a fill."""
    del market, value
    raise InventedFillRefused()


def invent_result(ticker=None, result=None):
    """Official result is read from the reget only. Nothing is written."""
    del ticker, result
    raise InventedResultRefused()


def backfill_list_429(which=None, result=None, occurrence_datetime=None):
    """Settled, finalized, and events 429 list gaps stay gaps. Nothing is written."""
    del which, result, occurrence_datetime
    raise InventedResultRefused()


def backfill_shard1(which=None, result=None):
    """The SHARD1 429 gap stays a gap. Nothing is written."""
    del which, result
    raise InventedResultRefused()


def follow_settled_cursor(cursor=None):
    """The settled-list cursor is present. Markets past the pin are not fetched."""
    del cursor
    raise InventedMarketRefused()


def invent_related_series(ticker=None, result=None):
    """The related-series N=20 count is not a market list."""
    del ticker, result
    raise InventedMarketRefused()


def invent_parent_settlement(ticker=None, result=None):
    """Parent ticker-GET results stay in the scout. Nothing is written onto the panel."""
    del ticker, result
    raise InventedResultRefused()


def stamp_panel_result(ticker=None, result=None):
    """The panel stub has no result. Nothing is written."""
    del ticker, result
    raise InventedResultRefused()


def assign_occurrence(ticker=None, value=None):
    """A null occurrence_datetime stays null."""
    del ticker, value
    raise InventedSoTRefused()


def copy_scout_n_into_settled_join(value=None):
    """The scout pin is not the scorecard count."""
    del value
    raise ScorecardPromotionRefused()


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
    if label in (
        'invent_settled_result',
        'invented_result',
        'list_429_backfill',
        'shard1_backfill',
        'parent_seed_invent',
    ):
        raise InventedResultRefused()
    if label in ('cursor_follow', 'related_series_invent'):
        raise InventedMarketRefused()
    if label in ('invent_fills', 'invented_fills'):
        raise InventedFillRefused()
    if label in ('invent_depth', 'invented_depth'):
        raise InventedDepthRefused()
    if label in ('invent_occurrence', 'invented_occurrence'):
        raise InventedSoTRefused()
    if label == 'admit_py':
        raise AdmitPyRefused()
    if label == 'live_orders':
        raise LiveOrdersForbidden()
    if label == 'ungate':
        raise UngateRefused()
    if label == 'copy_scout_n':
        raise ScorecardPromotionRefused()
    raise AdversaryRefused(ADVERSARY_LABELS[label])


def owned_dirs():
    return (ROOT, LAB_BUNDLE, SCIENCE, PACKET_DIR)


def _assert_digest(path, digest, size=None):
    raw = Path(path).read_bytes()
    if hashlib.sha256(raw).hexdigest() != digest:
        raise OrchestratorError(Path(path).name)
    if size is not None and len(raw) != size:
        raise OrchestratorError(Path(path).name)
    return raw


def _assert_owned(name, digest, size=None):
    for directory in owned_dirs():
        _assert_digest(directory / name, digest, size)


def _read_pinned(path, digest, size):
    return json.loads(_assert_digest(path, digest, size))


def _nonempty_result(value):
    return value in FINALIZED_RESULTS


def _zulu(value):
    return isinstance(value, str) and value.endswith('Z')


def clock_pin(row):
    """J1 public clock. A null occurrence_datetime stays null.

    When occurrence_datetime is present it is the clock. When it is null,
    or when the raw reget omits the key, the clock is expected_expiration_time.
    This function does not write a datetime.
    """
    if not isinstance(row, dict):
        raise OccurrenceIntegrityRefused()
    if row.get('occurrence_datetime') is not None:
        occ = row.get('occurrence_datetime')
        if not _zulu(occ):
            raise OccurrenceIntegrityRefused()
        return ('occurrence_datetime', occ)
    expected = row.get('expected_expiration_time')
    if not _zulu(expected):
        raise OccurrenceIntegrityRefused()
    return ('expected_expiration_time', expected)


def _assert_source_pins(payload):
    if payload.get('packet_id') != EXPERIMENT_ID:
        raise OrchestratorError('source pins')
    if payload.get('feature_family') != FEATURE_FAMILY:
        raise OrchestratorError('source pins')
    if payload.get('freeze_sha256') != FREEZE_SHA256:
        raise OrchestratorError('source pins')
    if payload.get('scout_reget_sha256') != SCOUT_SHA256:
        raise OrchestratorError('source pins')
    if payload.get('seed_summary_sha256') != SEED_SHA256:
        raise OrchestratorError('source pins')
    if payload.get('panel_stub_sha256') != PANEL_STUB_SHA256:
        raise OrchestratorError('source pins')
    if payload.get('settled_reget_sha256') != REGET_SHA256:
        raise OrchestratorError('source pins')
    if payload.get('conductor_accept_sha256') != ACCEPT_SHA256:
        raise OrchestratorError('source pins')
    if payload.get('frozen_experiment_sha256') != FROZEN_SHA256:
        raise OrchestratorError('source pins')
    if payload.get('empty_results_sha256') != EMPTY_SHA256:
        raise OrchestratorError('source pins')
    if payload.get('examiner_hold_sha256') != HOLD_SHA256:
        raise OrchestratorError('source pins')
    if payload.get('maximize_pin_sha256') != PIN_SHA256:
        raise OrchestratorError('source pins')
    if payload.get('digests_txt_sha256') != DIGESTS_SHA256:
        raise OrchestratorError('source pins')
    if payload.get('knob') != KNOB or payload.get('arms') != JOIN_GATE:
        raise OrchestratorError('source pins')
    if payload.get('admitted_at') is not None:
        raise OrchestratorError('source pins')
    if payload.get('settled_nonempty_result_N_scout') != SCOUT_NONEMPTY_N:
        raise OrchestratorError('source pins')
    if payload.get('scout_n_copied_into_settled_join_n') is not False:
        raise ScorecardPromotionRefused()
    if payload.get('yes_n') != YES_N or payload.get('no_n') != NO_N:
        raise OrchestratorError('source pins')
    if payload.get('settled_list_row_n') != SETTLED_LIST_ROW_N:
        raise OrchestratorError('source pins')
    if payload.get('parent_seed_tickers') != list(PARENT_SEED_TICKERS):
        raise OrchestratorError('source pins')
    if payload.get('parent_seeds_finalized_nonempty_N') != PARENT_FINALIZED_N:
        raise OrchestratorError('source pins')
    if payload.get('parent_seed_results') != PARENT_SEED_RESULTS:
        raise InventedResultRefused()
    if payload.get('parent_seed_statuses') != PARENT_SEED_STATUSES:
        raise InventedResultRefused()
    if payload.get('seed_panel_result') is not None:
        raise InventedResultRefused()
    if payload.get('parent_results_copied_onto_panel') is not False:
        raise InventedResultRefused()
    if payload.get('panel_stub_active_n') != PANEL_STUB_ACTIVE_N:
        raise InventedResultRefused()
    if payload.get('panel_stub_finalized_status_n') != PANEL_STUB_FINALIZED_N:
        raise InventedResultRefused()
    if payload.get('parent_reget_occurrence_present') is not False:
        raise InventedSoTRefused()
    if payload.get('occurrence_datetime_present_on_settled_N') != 0:
        raise InventedSoTRefused()
    if payload.get('expected_expiration_time_present_on_settled_N') != SCOUT_NONEMPTY_N:
        raise OccurrenceIntegrityRefused()
    if payload.get('j1_null_occurrence_clock') != 'expected_expiration_time':
        raise InventedSoTRefused()
    if payload.get('related_series_settled_N') != RELATED_SERIES_N:
        raise OrchestratorError('source pins')
    if payload.get('related_series_markets_invented') is not False:
        raise InventedMarketRefused()
    if payload.get('settled_list_http') != LIST_200:
        raise OrchestratorError('source pins')
    if payload.get('settled_list_cursor_present') is not True or payload.get('cursor_followed') is not False:
        raise InventedMarketRefused()
    if payload.get('settled_list_earlier_429') != LIST_429:
        raise InventedResultRefused()
    if payload.get('finalized_list_429') != LIST_429:
        raise InventedResultRefused()
    if payload.get('events_closed_settled_429') != LIST_429:
        raise InventedResultRefused()
    if payload.get('shard1_series_429') != LIST_429:
        raise InventedResultRefused()
    if payload.get('list_429_backfilled') is not False:
        raise InventedResultRefused()
    if payload.get('honest_gap_n') != HONEST_GAP_N:
        raise InventedResultRefused()
    if payload.get('fee_import_used') is not False or payload.get('rails_import_used') is not False:
        raise OrchestratorError('source pins')
    if payload.get('fee_arms') is not False:
        raise OrchestratorError('source pins')
    if payload.get('feebook_commit_fixed_not_loaded') != FEEBOOK_COMMIT:
        raise OrchestratorError('source pins')
    if payload.get('rails_commit_fixed_not_loaded') != RAILS_COMMIT:
        raise OrchestratorError('source pins')
    if payload.get('does_not_run_admit_py') is not True:
        raise AdmitPyRefused()
    if payload.get('base_commit') != BASE_COMMIT:
        raise OrchestratorError('source pins')
    if payload.get('lee_ready') != 'REFUSED':
        raise LeeReadyRefused()
    if payload.get('filllegs_reopen') is not False or payload.get('mve_fl_reopen') is not False:
        raise OrchestratorError('source pins')
    if payload.get('r2p3_rj_reopen') is not False or payload.get('s4_rj_reopen') is not False:
        raise OrchestratorError('source pins')
    if payload.get('nhl_rj_reopen') is not False:
        raise OrchestratorError('source pins')
    if payload.get('fq_reopen') is not False or payload.get('cap_sr_reopen') is not False:
        raise OrchestratorError('source pins')
    if payload.get('c3_rj_reopen') is not False or payload.get('c5_rj_reopen') is not False:
        raise OrchestratorError('source pins')
    if payload.get('r3p3_rj_reopen') is not False:
        raise OrchestratorError('source pins')
    if payload.get('arm_b_touch') is not False or payload.get('live_orders') is not False:
        raise OrchestratorError('source pins')
    if payload.get('conductor_cloud_kick') is not False:
        raise OrchestratorError('source pins')
    if payload.get('does_not_ungate') != list(DOES_NOT_UNGATE):
        raise UngateRefused()
    if payload.get('panel_version') != PANEL_VERSION:
        raise PanelVersionRefused()
    if payload.get('panel_events_n') != PANEL_EVENTS_N:
        raise OrchestratorError('source pins')
    if payload.get('panel_markets_n') != PANEL_MARKETS_N:
        raise OrchestratorError('source pins')
    for key in OUTPUT_KEYS:
        if key not in payload or payload[key] is not None:
            raise ScorecardPromotionRefused()
    return payload


def _validate_market_row(row, panel_tickers, source):
    if not isinstance(row, dict) or set(row) != MARKET_KEYS:
        raise OrchestratorError('scout market')
    ticker = row.get('ticker')
    if not isinstance(ticker, str) or not ticker.startswith(SERIES + '-S'):
        raise InventedMarketRefused()
    if SHARD1 in ticker or ticker.startswith(RELATED_SERIES):
        raise InventedMarketRefused()
    if row.get('nonempty_result') is not True:
        raise InventedResultRefused()
    if row.get('status') != 'finalized' or not _nonempty_result(row.get('result')):
        raise InventedResultRefused()
    if row.get('occurrence_datetime') is not None:
        raise InventedSoTRefused()
    if not _zulu(row.get('expected_expiration_time')) or not _zulu(row.get('close_time')):
        raise OccurrenceIntegrityRefused()
    if not _zulu(row.get('expiration_time')):
        raise OccurrenceIntegrityRefused()
    if row.get('source') != source:
        raise InventedResultRefused()
    if row.get('mve_collection_ticker') != COLLECTION:
        raise InventedMarketRefused()
    event_ticker = row.get('event_ticker')
    if not isinstance(event_ticker, str) or not ticker.startswith(event_ticker + '-'):
        raise InventedMarketRefused()
    if 'orderbook_fp' in row:
        raise InventedDepthRefused()
    if source == SETTLED_SOURCE and ticker in panel_tickers:
        raise InventedMarketRefused()
    if source == SETTLED_SOURCE and ticker in PARENT_SEED_TICKERS:
        raise InventedMarketRefused()
    return row


def _parent_block(payload):
    if payload.get('parent_seed_tickers') != list(PARENT_SEED_TICKERS):
        raise OrchestratorError('parent seeds')
    if payload.get('parent_seed_results') != PARENT_SEED_RESULTS:
        raise InventedResultRefused()
    if payload.get('parent_seed_statuses') != PARENT_SEED_STATUSES:
        raise InventedResultRefused()
    if payload.get('parent_seeds_finalized_nonempty_N') != PARENT_FINALIZED_N:
        raise InventedResultRefused()
    return payload


def _validate_scout(payload, panel_tickers):
    if set(payload) != SCOUT_KEYS:
        raise OrchestratorError('scout')
    if payload.get('packet') != SCOUT_PACKET or payload.get('feature_family') != FEATURE_FAMILY:
        raise OrchestratorError('scout')
    if payload.get('series') != [SERIES]:
        raise OrchestratorError('scout')
    if payload.get('sibling_series_noted') != list(SIBLING_SERIES):
        raise OrchestratorError('scout')
    if payload.get('settled_nonempty_result_N') != SCOUT_NONEMPTY_N:
        raise OrchestratorError('scout N')
    if payload.get('settled_list_limit') != SETTLED_LIST_LIMIT:
        raise OrchestratorError('scout')
    if payload.get('settled_list_http') != LIST_200:
        raise InventedResultRefused()
    if payload.get('settled_list_cursor_present') is not True:
        raise InventedMarketRefused()
    if payload.get('open_list_n') is not None or payload.get('open_list_http') is not None:
        raise InventedMarketRefused()
    if payload.get('method') != SCOUT_METHOD:
        raise OrchestratorError('scout mode')
    if payload.get('host') != PUBLIC_HOST:
        raise OrchestratorError('scout host')
    _parent_block(payload)
    if payload.get('parent_panel_seeds_note') != PARENT_NOTE:
        raise OrchestratorError('scout')
    if payload.get('occurrence_datetime_present_on_settled_N') != 0:
        raise InventedSoTRefused()
    if payload.get('expected_expiration_time_present_on_settled_N') != SCOUT_NONEMPTY_N:
        raise OccurrenceIntegrityRefused()
    if payload.get('occurrence_datetime_sot_note') != OCCURRENCE_NOTE:
        raise InventedSoTRefused()
    if payload.get('occurrence_datetime_sot_match_all_settled_seeds') is not None:
        raise InventedSoTRefused()
    if payload.get('expected_expiration_time_present_all_settled') is not True:
        raise OccurrenceIntegrityRefused()
    if payload.get('related_series_settled_KXMVESPORTSMULTIGAMEEXTENDED_N') != RELATED_SERIES_N:
        raise OrchestratorError('scout')
    if payload.get('related_series_settled_http') != LIST_200:
        raise OrchestratorError('scout')
    if payload.get('http_honesty') != HTTP_HONESTY:
        raise InventedResultRefused()
    if payload.get('scouted_at_et') != SCOUT_FETCHED_AT:
        raise OrchestratorError('scout')
    markets = payload.get('markets')
    if not isinstance(markets, list) or len(markets) != SCOUT_NONEMPTY_N:
        raise OrchestratorError('scout markets')
    seen = []
    for row in markets:
        _validate_market_row(row, panel_tickers, SETTLED_SOURCE)
        if row['ticker'] in seen:
            raise InventedMarketRefused()
        seen.append(row['ticker'])
    if seen != list(SETTLED_TICKERS):
        raise OrchestratorError('scout census')
    parents = payload.get('parent_seed_markets')
    if not isinstance(parents, list) or len(parents) != PARENT_SEED_N:
        raise OrchestratorError('parent markets')
    parent_seen = []
    for row in parents:
        _validate_market_row(row, panel_tickers, PARENT_SOURCE)
        ticker = row['ticker']
        if ticker not in PARENT_SEED_TICKERS or row['result'] != PARENT_SEED_RESULTS[ticker]:
            raise InventedResultRefused()
        if row['expected_expiration_time'] != PARENT_EXPECTED_EXPIRATION[ticker]:
            raise OccurrenceIntegrityRefused()
        if ticker in seen:
            raise InventedMarketRefused()
        parent_seen.append(ticker)
    if parent_seen != list(PARENT_SEED_TICKERS):
        raise OrchestratorError('parent census')
    return payload


def _validate_seed(payload, scout):
    if set(payload) != SEED_KEYS:
        raise OrchestratorError('seed')
    if payload.get('settled_nonempty_result_N') != SCOUT_NONEMPTY_N:
        raise OrchestratorError('seed N')
    if payload.get('overnight_finalized_nonempty_N') != SCOUT_NONEMPTY_N:
        raise OrchestratorError('seed N')
    if payload.get('settled_list_attempted_KXMVECROSSCATEGORY') != LIST_200:
        raise InventedResultRefused()
    if payload.get('settled_list_earlier_attempts') != LIST_429:
        raise InventedResultRefused()
    if payload.get('finalized_list_attempted_KXMVECROSSCATEGORY') != LIST_429:
        raise InventedResultRefused()
    if payload.get('events_closed_settled_attempted') != LIST_429:
        raise InventedResultRefused()
    if payload.get('method') != SEED_METHOD:
        raise OrchestratorError('seed')
    _parent_block(payload)
    if payload.get('occurrence_datetime_present_on_settled_N') != 0:
        raise InventedSoTRefused()
    if payload.get('expected_expiration_time_present_all_settled') is not True:
        raise OccurrenceIntegrityRefused()
    if payload.get('occurrence_datetime_match_all_settled_seeds') is not None:
        raise InventedSoTRefused()
    if payload.get('related_fee_pin_series_settled_KXMVESPORTSMULTIGAMEEXTENDED_N') != RELATED_SERIES_N:
        raise OrchestratorError('seed')
    if 'results' in payload or 'pnl' in payload or 'honest_gaps' in payload:
        raise InventedResultRefused()
    if payload.get('markets') != scout.get('markets'):
        raise OrchestratorError('seed scout markets')
    return payload


def _validate_reget(payload, scout):
    if set(payload) != {'cursor', 'markets'}:
        raise OrchestratorError('reget')
    cursor = payload.get('cursor')
    if not isinstance(cursor, str) or not cursor:
        raise InventedMarketRefused()
    markets = payload.get('markets')
    if not isinstance(markets, list) or len(markets) != SCOUT_NONEMPTY_N:
        raise OrchestratorError('reget markets')
    if 'results' in payload or 'pnl' in payload:
        raise ScorecardPromotionRefused()
    yes_n = 0
    no_n = 0
    seen = []
    scout_rows = {row['ticker']: row for row in scout['markets']}
    for row in markets:
        if not isinstance(row, dict):
            raise OrchestratorError('reget market')
        if 'occurrence_datetime' in row:
            raise InventedSoTRefused()
        if 'orderbook_fp' in row:
            raise InventedDepthRefused()
        ticker = row.get('ticker')
        if ticker not in scout_rows:
            raise InventedMarketRefused()
        scout_row = scout_rows[ticker]
        for field in SHARED_FIELDS:
            if row.get(field) != scout_row.get(field):
                raise OrchestratorError('reget ' + field)
        if clock_pin(row) != clock_pin(scout_row):
            raise OccurrenceIntegrityRefused()
        if row.get('status') != 'finalized' or not _nonempty_result(row.get('result')):
            raise InventedResultRefused()
        if row.get('result') == 'yes':
            yes_n += 1
        elif row.get('result') == 'no':
            no_n += 1
        seen.append(ticker)
    if seen != list(SETTLED_TICKERS):
        raise OrchestratorError('reget census')
    if yes_n != YES_N or no_n != NO_N:
        raise OrchestratorError('reget census')
    return payload


def _validate_panel(payload):
    if not isinstance(payload, dict):
        raise OrchestratorError('panel')
    if payload.get('panel_version') != PANEL_VERSION:
        raise PanelVersionRefused()
    if payload.get('packet_id') != PARENT_PACKET_ID:
        raise OrchestratorError('packet')
    if payload.get('schema_id') != SCHEMA_ID:
        raise OrchestratorError('schema')
    if payload.get('stub_status') != STUB_STATUS:
        raise OrchestratorError('stub_status')
    if payload.get('series_ticker') != SERIES:
        raise OrchestratorError('panel')
    if payload.get('purpose') != PANEL_PURPOSE or payload.get('cohort_kind') != COHORT_KIND:
        raise OrchestratorError('panel')
    if payload.get('admitted_at') is not None:
        raise OrchestratorError('admitted_at')
    if payload.get('stubbed_at_utc') != STUBBED_AT:
        raise OrchestratorError('panel')
    if payload.get('freeze_packet_sha256') != PARENT_KERNEL_SHA256:
        raise OrchestratorError('panel')
    if payload.get('scout_cite') != SCOUT_CITE_PANEL:
        raise OrchestratorError('panel')
    if payload.get('freeze_cite') != FREEZE_CITE_PANEL:
        raise OrchestratorError('panel')
    for key in ('results', 'pnl', 'volume'):
        if key not in payload or payload[key] is not None:
            raise ScorecardPromotionRefused()
    admit = payload.get('admit_gate')
    if not isinstance(admit, dict):
        raise OrchestratorError('admit_gate')
    if admit.get('status') != ADMIT_GATE_STATUS or admit.get('admit_py_run') is not False:
        raise AdmitPyRefused()
    binds = payload.get('binds') or {}
    if binds.get('fee_lab_sha') != FEEBOOK_COMMIT or binds.get('rails_lab_sha') != RAILS_COMMIT:
        raise OrchestratorError('panel binds')
    if binds.get('fee_type_series_override') != FEE_OVERRIDE or binds.get('fee_multiplier') != 1:
        raise OrchestratorError('panel binds')
    capture = payload.get('capture') or {}
    if capture.get('mode') != 'GET_only_public':
        raise LiveOrdersForbidden()
    if capture.get('host_allowlist') != [PANEL_HOST]:
        raise LiveOrdersForbidden()
    routes = capture.get('routes_allowlist')
    if not isinstance(routes, list) or not routes:
        raise LiveOrdersForbidden()
    for route in routes:
        if not isinstance(route, str) or not route.startswith('GET '):
            raise LiveOrdersForbidden()
        if OUT_OF_SCOPE_ROUTE in route or 'portfolio/orders' in route:
            raise LiveOrdersForbidden()
    budget = capture.get('budget_isolation') or {}
    note = budget.get('note') or ''
    if 'No recorder started' not in note:
        raise AdmitPyRefused()
    schedule = capture.get('schedule') or {}
    if schedule.get('recorder_started') is True or schedule.get('admit_py_run') is True:
        raise AdmitPyRefused()
    if payload.get('ineligible') != []:
        raise OrchestratorError('ineligible')
    summary = payload.get('cohort_summary') or {}
    if summary.get('markets_seed_n') != PANEL_MARKETS_N or summary.get('events_seed_n') != PANEL_EVENTS_N:
        raise OrchestratorError('cohort')
    events = payload.get('events')
    if not isinstance(events, list) or len(events) != PANEL_EVENTS_N:
        raise OrchestratorError('events')
    markets = payload.get('markets')
    if not isinstance(markets, list) or len(markets) != PANEL_MARKETS_N:
        raise OrchestratorError('markets')
    seen_events = []
    base_n = 0
    shard_n = 0
    for event in events:
        if not isinstance(event, dict):
            raise OrchestratorError('events')
        if event.get('admitted_at') is not None:
            raise OrchestratorError('admitted_at')
        series = event.get('series_ticker')
        if series == SERIES:
            base_n += 1
        elif series == SHARD1:
            shard_n += 1
        else:
            raise OrchestratorError('events')
        if event.get('panel_version') != PANEL_VERSION:
            raise PanelVersionRefused()
        if 'result' in event:
            raise InventedResultRefused()
        if 'orderbook_fp' in event:
            raise InventedDepthRefused()
        for key in VOLUME_FIELDS:
            if key not in event or event[key] is not None:
                raise InventedFillRefused()
        if event.get('kalshi_occurrence_datetime') is not None or event.get('sot_pin') is not None:
            raise InventedSoTRefused()
        ticker = event.get('event_ticker')
        listed = event.get('market_tickers')
        if not isinstance(listed, list):
            raise OrchestratorError('events')
        if series == SHARD1 and listed != []:
            raise InventedMarketRefused()
        expected = list(PARENT_EVENT_MARKETS.get(ticker, ()))
        if listed != expected:
            raise InventedMarketRefused()
        seen_events.append(ticker)
    if tuple(seen_events) != PANEL_EVENTS:
        raise OrchestratorError('events')
    if base_n != PANEL_BASE_EVENTS_N or shard_n != PANEL_SHARD1_EVENTS_N:
        raise OrchestratorError('events')
    seen_markets = []
    for market in markets:
        if not isinstance(market, dict):
            raise OrchestratorError('markets')
        if market.get('admitted_at') is not None:
            raise OrchestratorError('admitted_at')
        if 'result' in market:
            raise InventedResultRefused()
        if 'orderbook_fp' in market:
            raise InventedDepthRefused()
        if market.get('panel_version') != PANEL_VERSION:
            raise PanelVersionRefused()
        if market.get('series_ticker') != SERIES:
            raise OrchestratorError('markets')
        ticker = market.get('market_ticker')
        if market.get('status_observed') != PANEL_STATUS_OBSERVED.get(ticker):
            raise OrchestratorError('panel status')
        seen_markets.append(ticker)
    if tuple(seen_markets) != PARENT_SEED_TICKERS:
        raise OrchestratorError('markets')
    return payload


def _panel_ticker_set(panel):
    tickers = []
    for event in panel.get('events') or []:
        for ticker in event.get('market_tickers') or []:
            tickers.append(ticker)
    if tickers != list(PARENT_SEED_TICKERS):
        raise InventedMarketRefused()
    return set(tickers)


def _assert_frozen(payload):
    if payload.get('packet_id') != EXPERIMENT_ID:
        raise OrchestratorError('frozen')
    if payload.get('feature_family') != FEATURE_FAMILY:
        raise OrchestratorError('frozen')
    if payload.get('status') != 'FROZEN_EXPERIMENT':
        raise OrchestratorError('frozen')
    if payload.get('lab_dir') != LAB_DIRECTORY + '/':
        raise OrchestratorError('frozen')
    if payload.get('knob') != KNOB:
        raise OrchestratorError('frozen')
    if payload.get('arms') != list(ARMS):
        raise OrchestratorError('frozen')
    if payload.get('arm_values') != JOIN_GATE:
        raise OrchestratorError('frozen')
    if payload.get('results') is not None or payload.get('pnl') is not None:
        raise ScorecardPromotionRefused()
    if 'settled_join_n' in payload or 'occurrence_match_n' in payload or 'admit_ready_flag' in payload:
        raise ScorecardPromotionRefused()
    if payload.get('settled_nonempty_result_N_scout') != SCOUT_NONEMPTY_N:
        raise OrchestratorError('frozen')
    if payload.get('admitted_at') is not None:
        raise OrchestratorError('admitted_at')
    if payload.get('panel_version') != PANEL_VERSION:
        raise PanelVersionRefused()
    if payload.get('does_not_run_admit_py') is not True:
        raise AdmitPyRefused()
    if payload.get('stamped_at_et') != FROZEN_STAMPED_AT:
        raise OrchestratorError('frozen')
    if payload.get('freeze_sha256') != FREEZE_SHA256:
        raise OrchestratorError('frozen')
    if payload.get('scout_reget_sha256') != SCOUT_SHA256:
        raise OrchestratorError('frozen')
    if payload.get('scout_summary_sha256') != SEED_SHA256:
        raise OrchestratorError('frozen')
    if payload.get('panel_stub_sha256') != PANEL_STUB_SHA256:
        raise OrchestratorError('frozen')
    if payload.get('settled_reget_capture_sha256') != REGET_SHA256:
        raise OrchestratorError('frozen')
    return payload


def _assert_accept(payload):
    if payload.get('packet_id') != EXPERIMENT_ID:
        raise OrchestratorError('conductor accept')
    if payload.get('feature_family') != FEATURE_FAMILY:
        raise OrchestratorError('conductor accept')
    if payload.get('decision') != 'ACCEPT' or payload.get('implement') is not True:
        raise OrchestratorError('conductor accept')
    if payload.get('seat') != 'Conductor':
        raise OrchestratorError('conductor accept')
    if payload.get('accepted_at_et') != ACCEPT_STAMPED_AT:
        raise OrchestratorError('conductor accept')
    if payload.get('lab') != LAB_DIRECTORY + '/':
        raise OrchestratorError('conductor accept')
    if payload.get('prior_done') != PRIOR_DONE:
        raise OrchestratorError('conductor accept')
    if payload.get('orthogonal_pin') != ORTHOGONAL_PIN:
        raise OrchestratorError('conductor accept')
    if payload.get('implement_owner') != 'R&D Variants':
        raise OrchestratorError('conductor accept')
    if payload.get('conductor_cloud_kick') is not False:
        raise OrchestratorError('conductor accept')
    if payload.get('knob') != KNOB or payload.get('arms') != ACCEPT_ARMS:
        raise OrchestratorError('conductor accept')
    digest = payload.get('digest_verify')
    if not isinstance(digest, dict):
        raise OrchestratorError('conductor accept')
    if digest.get('freeze') != FREEZE_SHA256:
        raise OrchestratorError('conductor accept')
    if digest.get('scout_reget') != SCOUT_SHA256:
        raise OrchestratorError('conductor accept')
    if digest.get('seed_summary') != SEED_SHA256:
        raise OrchestratorError('conductor accept')
    if digest.get('panel_stub') != PANEL_STUB_SHA256:
        raise OrchestratorError('conductor accept')
    if digest.get('settled_reget') != REGET_SHA256:
        raise OrchestratorError('conductor accept')
    if digest.get('settled_nonempty_result_N') != SCOUT_NONEMPTY_N or digest.get('match') is not True:
        raise OrchestratorError('conductor accept')
    if payload.get('hard_refuse') != list(ACCEPT_HARD_REFUSE):
        raise OrchestratorError('conductor accept')
    return payload


def _assert_hold(payload):
    if payload.get('id') != 'EXAMINER_HOLD_S5_KXMVECROSSCATEGORY_SETTLED_JOIN_HARNESS_PRE_PR':
        raise OrchestratorError('examiner hold')
    if payload.get('status') != 'HOLD_PRE_PR' or payload.get('stub_ready') is not False:
        raise ExaminerNotReady()
    if payload.get('packet') != EXPERIMENT_ID or payload.get('feature_family') != FEATURE_FAMILY:
        raise OrchestratorError('examiner hold')
    if payload.get('knob') != KNOB or payload.get('arm_values') != JOIN_GATE:
        raise OrchestratorError('examiner hold')
    if payload.get('arms') != list(ARMS):
        raise OrchestratorError('examiner hold')
    if payload.get('settled_nonempty_result_N_scout') != SCOUT_NONEMPTY_N:
        raise OrchestratorError('examiner hold')
    if payload.get('scout_markets_settled_nonempty') != SCOUT_NONEMPTY_N:
        raise OrchestratorError('examiner hold')
    if payload.get('admitted_at') is not None:
        raise OrchestratorError('admitted_at')
    if payload.get('panel_version') != PANEL_VERSION:
        raise PanelVersionRefused()
    if payload.get('metrics_null') != list(HOLD_METRICS):
        raise ScorecardPromotionRefused()
    if payload.get('does_not_ungate') != list(DOES_NOT_UNGATE):
        raise UngateRefused()
    if payload.get('orthogonal_to') != list(ORTHOGONAL_TO):
        raise OrchestratorError('examiner hold')
    if payload.get('stamped_at_et') != HOLD_STAMPED_AT:
        raise OrchestratorError('examiner hold')
    if payload.get('freeze_sha256') != FREEZE_SHA256:
        raise OrchestratorError('examiner hold')
    if payload.get('scout_reget_sha256') != SCOUT_SHA256:
        raise OrchestratorError('examiner hold')
    if payload.get('scout_summary_sha256') != SEED_SHA256:
        raise OrchestratorError('examiner hold')
    if payload.get('panel_stub_sha256') != PANEL_STUB_SHA256:
        raise OrchestratorError('examiner hold')
    if payload.get('settled_reget_capture_sha256') != REGET_SHA256:
        raise OrchestratorError('examiner hold')
    if payload.get('maximize_pin_sha256') != PIN_SHA256:
        raise OrchestratorError('examiner hold')
    if payload.get('box_digest_match') is not True:
        raise OrchestratorError('examiner hold')
    if payload.get('note_scout_N_not_copied_into_settled_join_n') is not True:
        raise ScorecardPromotionRefused()
    if payload.get('settled_list_http') != LIST_200:
        raise InventedResultRefused()
    if payload.get('settled_list_earlier_http') != LIST_429:
        raise InventedResultRefused()
    if payload.get('finalized_list_http') != LIST_429:
        raise InventedResultRefused()
    if payload.get('events_closed_settled_http') != LIST_429:
        raise InventedResultRefused()
    if payload.get('occurrence_datetime_present_on_settled_N') != 0:
        raise InventedSoTRefused()
    if payload.get('expected_expiration_time_present_on_settled_N') != SCOUT_NONEMPTY_N:
        raise OccurrenceIntegrityRefused()
    if payload.get('prior_r2p3_rj_pr46_main') != BASE_COMMIT:
        raise OrchestratorError('examiner hold')
    if payload.get('prior_r2p3_rj_accept_sha256') != R2P3_ACCEPT_SHA256:
        raise OrchestratorError('examiner hold')
    if payload.get('implement_owner') != 'R&D Variants':
        raise OrchestratorError('examiner hold')
    if payload.get('conductor_cloud_kick') is not False:
        raise OrchestratorError('examiner hold')
    return payload


def _assert_authentic_bytes():
    _assert_owned(FREEZE_NAME, FREEZE_SHA256, FREEZE_BYTES)
    _assert_owned(SCOUT_NAME, SCOUT_SHA256, SCOUT_BYTES)
    _assert_owned(SEED_NAME, SEED_SHA256, SEED_BYTES)
    _assert_owned(REGET_NAME, REGET_SHA256, REGET_BYTES)
    _assert_owned(ACCEPT_NAME, ACCEPT_SHA256, ACCEPT_BYTES)
    _assert_owned('FROZEN_EXPERIMENT.json', FROZEN_SHA256, FROZEN_BYTES)
    _assert_owned('panel_stub.json', PANEL_STUB_SHA256, PANEL_BYTES)
    _assert_owned(PANEL_ALIAS, PANEL_STUB_SHA256, PANEL_BYTES)
    _assert_owned(HOLD_NAME, HOLD_SHA256, HOLD_BYTES)
    _assert_owned(PIN_NAME, PIN_SHA256, PIN_BYTES)
    _assert_owned(DIGESTS_NAME, DIGESTS_SHA256, DIGESTS_BYTES)
    _assert_owned('EMPTY_RESULTS.json', EMPTY_SHA256, EMPTY_BYTES)
    _assert_owned(SOURCE_PINS_NAME, SOURCE_PINS_SHA256, SOURCE_PINS_BYTES)
    _assert_digest(FREEZE_GOV, FREEZE_SHA256, FREEZE_BYTES)
    _assert_digest(SCOUT_CITE_DIR / SCOUT_NAME, SCOUT_SHA256, SCOUT_BYTES)
    _assert_digest(SCOUT_CITE_DIR / SEED_NAME, SEED_SHA256, SEED_BYTES)
    _assert_digest(PANEL_GOV, PANEL_STUB_SHA256, PANEL_BYTES)
    _assert_digest(PANEL_CAPTURE, PANEL_STUB_SHA256, PANEL_BYTES)
    _assert_digest(REGET_CITE, REGET_SHA256, REGET_BYTES)
    _assert_digest(PIN_CITE, PIN_SHA256, PIN_BYTES)
    _assert_digest(ACCEPT_ROOT, ACCEPT_SHA256, ACCEPT_BYTES)
    _assert_digest(EMPTY_RESULTS, EMPTY_SHA256, EMPTY_BYTES)
    _assert_digest(LAB_BUNDLE / 'results.json', EMPTY_SHA256, EMPTY_BYTES)
    _assert_digest(LAB_BUNDLE / 'results' / 'EMPTY_RESULTS.json', EMPTY_SHA256, EMPTY_BYTES)
    _assert_digest(SCIENCE / 'results' / 'EMPTY_RESULTS.json', EMPTY_SHA256, EMPTY_BYTES)
    _assert_digest(PACKET_DIR / 'results.json', EMPTY_SHA256, EMPTY_BYTES)
    _assert_digest(PACKET_DIR / 'results' / 'EMPTY_RESULTS.json', EMPTY_SHA256, EMPTY_BYTES)
    panel = _validate_panel(_read_pinned(PANEL_CAPTURE, PANEL_STUB_SHA256, PANEL_BYTES))
    panel_tickers = _panel_ticker_set(panel)
    scout = _validate_scout(_read_pinned(SCOUT_PATH, SCOUT_SHA256, SCOUT_BYTES), panel_tickers)
    _validate_seed(_read_pinned(SEED_PATH, SEED_SHA256, SEED_BYTES), scout)
    _validate_reget(_read_pinned(REGET_PATH, REGET_SHA256, REGET_BYTES), scout)
    _assert_frozen(_read_pinned(FROZEN_EXPERIMENT, FROZEN_SHA256, FROZEN_BYTES))
    _assert_accept(_read_pinned(CONDUCTOR_ACCEPT, ACCEPT_SHA256, ACCEPT_BYTES))
    _assert_hold(_read_pinned(EXAMINER_HOLD, HOLD_SHA256, HOLD_BYTES))
    for directory in owned_dirs():
        _assert_source_pins(json.loads(_assert_digest(directory / SOURCE_PINS_NAME, SOURCE_PINS_SHA256, SOURCE_PINS_BYTES)))
    empty = json.loads(EMPTY_RESULTS.read_text())
    if empty.get('note') != EMPTY_NOTE:
        raise OrchestratorError('empty results')
    assert_null_scorecard(empty)
    if ADMIT_PY.exists():
        raise AdmitPyRefused()
    if PANEL_ADMITTED.exists():
        raise AdmitPyRefused()
    return True


def conductor_pin_status():
    """Report whether checkout bytes match the attached conductor sha256 values."""
    freeze_match = sha256_file(PACKET) == FREEZE_SHA256 and sha256_file(FREEZE_GOV) == FREEZE_SHA256
    scout_match = sha256_file(SCOUT_PATH) == SCOUT_SHA256 and sha256_file(SCOUT_CITE_DIR / SCOUT_NAME) == SCOUT_SHA256
    seed_match = sha256_file(SEED_PATH) == SEED_SHA256 and sha256_file(SCOUT_CITE_DIR / SEED_NAME) == SEED_SHA256
    panel_match = sha256_file(PANEL_CAPTURE) == PANEL_STUB_SHA256 and sha256_file(PANEL_GOV) == PANEL_STUB_SHA256
    reget_match = sha256_file(REGET_PATH) == REGET_SHA256 and sha256_file(REGET_CITE) == REGET_SHA256
    accept_match = (
        sha256_file(CONDUCTOR_ACCEPT) == ACCEPT_SHA256
        and sha256_file(PACKET_DIR / ACCEPT_NAME) == ACCEPT_SHA256
        and sha256_file(ACCEPT_ROOT) == ACCEPT_SHA256
    )
    return {
        'freeze_matches_conductor_claim': freeze_match,
        'scout_reget_matches_conductor_claim': scout_match,
        'seed_summary_matches_conductor_claim': seed_match,
        'panel_stub_matches_conductor_claim': panel_match,
        'settled_reget_matches_conductor_claim': reget_match,
        'accept_matches_conductor_claim': accept_match,
        'conductor_bytes_in_checkout': all((
            freeze_match,
            scout_match,
            seed_match,
            panel_match,
            reget_match,
            accept_match,
        )),
        'admitted_at': None,
        'governance_s5_cites_present': FREEZE_GOV.is_file() and (SCOUT_CITE_DIR / SCOUT_NAME).is_file(),
        'reget_cite_present': REGET_CITE.is_file(),
    }


def select_panel_path(stub_path=None, admitted_path=None):
    """The committed stub only. A panel_admitted.json file is not consumed."""
    if admitted_path is not None and Path(admitted_path).exists():
        raise AdmitPyRefused()
    if PANEL_ADMITTED.exists():
        raise AdmitPyRefused()
    stub_path = PANEL_CAPTURE if stub_path is None else Path(stub_path)
    if not Path(stub_path).is_file():
        raise OrchestratorError('panel stub')
    return Path(stub_path)


def load_panel(path=None):
    """Load a panel object. The committed stub must match the pin and stay unadmitted."""
    path = select_panel_path() if path is None else Path(path)
    canonical = {PANEL_CAPTURE.resolve(), PANEL_GOV.resolve()}
    for directory in owned_dirs():
        canonical.add((directory / 'panel_stub.json').resolve())
        canonical.add((directory / PANEL_ALIAS).resolve())
    if path.resolve() in canonical:
        _assert_authentic_bytes()
        _assert_digest(path, PANEL_STUB_SHA256, PANEL_BYTES)
    payload = json.loads(path.read_text())
    return _validate_panel(payload)


def load_scout():
    _assert_authentic_bytes()
    panel = _validate_panel(_read_pinned(PANEL_CAPTURE, PANEL_STUB_SHA256, PANEL_BYTES))
    return _validate_scout(_read_pinned(SCOUT_PATH, SCOUT_SHA256, SCOUT_BYTES), _panel_ticker_set(panel))


def load_seed():
    scout = load_scout()
    return _validate_seed(_read_pinned(SEED_PATH, SEED_SHA256, SEED_BYTES), scout)


def _settled_view(payload, scout):
    """In-memory settled index. This view is not written back to the reget file."""
    checked = _validate_reget(payload, scout)
    markets = {}
    for row in checked['markets']:
        markets[row['ticker']] = row
    return {
        'cursor': checked['cursor'],
        'markets': markets,
        'honest_gaps': list(HONEST_GAPS),
        'cursor_followed': False,
        'occurrence_datetime_key_present': False,
        'settled_nonempty_result_N': SCOUT_NONEMPTY_N,
    }


def load_reget():
    scout = load_scout()
    payload = _read_pinned(REGET_PATH, REGET_SHA256, REGET_BYTES)
    return _settled_view(payload, scout)


def list_429_gaps(reget=None):
    """Earlier settled, finalized, events, and SHARD1 gaps. The settled 200 list is not a gap."""
    if reget is None:
        reget = load_reget()
    if reget.get('honest_gaps') != list(HONEST_GAPS):
        raise InventedResultRefused()
    if reget.get('cursor_followed') is not False:
        raise InventedMarketRefused()
    if reget.get('occurrence_datetime_key_present') is not False:
        raise InventedSoTRefused()
    markets = reget.get('markets') or {}
    for key in HONEST_GAPS:
        if key in markets:
            raise InventedResultRefused()
    for row in markets.values():
        if row.get('status') != 'finalized':
            raise InventedResultRefused()
        if 'occurrence_datetime' in row:
            raise InventedSoTRefused()
    return HONEST_GAPS


def assert_occurrence_pair(left, right):
    """Require one shared J1 clock. Does not write a match count."""
    left_clock = clock_pin(left)
    right_clock = clock_pin(right)
    if left_clock != right_clock:
        raise OccurrenceIntegrityRefused()
    if left_clock[0] == 'occurrence_datetime':
        return left_clock[1]
    if left.get('occurrence_datetime') is not None or right.get('occurrence_datetime') is not None:
        raise InventedSoTRefused()
    return left_clock[1]


def occurrence_agreement_tickers(panel=None):
    """Settled rows whose scout, seed, and reget clocks agree.

    occurrence_datetime is null on this cohort. The shared clock is
    expected_expiration_time. This tuple is not occurrence_match_n and
    it is not settled_join_n.
    """
    if panel is None:
        panel = load_panel()
    else:
        _validate_panel(panel)
    reget = load_reget()['markets']
    seed_rows = {row['ticker']: row for row in load_seed()['markets']}
    scout_rows = {row['ticker']: row for row in load_scout()['markets']}
    if set(reget) != set(seed_rows) or set(reget) != set(scout_rows):
        raise InventedMarketRefused()
    if list(scout_rows) != list(SETTLED_TICKERS):
        raise OrchestratorError('occurrence rows')
    panel_tickers = _panel_ticker_set(panel)
    agreed = []
    for ticker in SETTLED_TICKERS:
        market = reget[ticker]
        assert_occurrence_pair(market, seed_rows[ticker])
        assert_occurrence_pair(market, scout_rows[ticker])
        if clock_pin(market)[0] != 'expected_expiration_time':
            raise InventedSoTRefused()
        for field in SHARED_FIELDS:
            if market.get(field) != seed_rows[ticker].get(field):
                raise OrchestratorError('seed reget ' + field)
            if market.get(field) != scout_rows[ticker].get(field):
                raise OrchestratorError('scout reget ' + field)
        if ticker in panel_tickers or ticker in PARENT_SEED_TICKERS:
            raise InventedMarketRefused()
        agreed.append(ticker)
    if len(agreed) != SCOUT_NONEMPTY_N:
        raise OrchestratorError('occurrence rows')
    return tuple(agreed)


def parent_finalized_tickers(panel=None):
    """Parent seeds finalized on ticker GETs, with null occurrence_datetime.

    expected_expiration_time is the ticker-GET clock. The panel stub keeps
    its own status_observed values and keeps result absent. This tuple is
    not occurrence_match_n and it is not settled_join_n.
    """
    if panel is None:
        panel = load_panel()
    else:
        _validate_panel(panel)
    scout = load_scout()
    seed = load_seed()
    _parent_block(scout)
    _parent_block(seed)
    by_ticker = {row['ticker']: row for row in scout['parent_seed_markets']}
    by_event = {event.get('event_ticker'): event for event in panel.get('events') or []}
    panel_markets = {row.get('market_ticker'): row for row in panel.get('markets') or []}
    agreed = []
    for ticker in PARENT_SEED_TICKERS:
        market = by_ticker[ticker]
        if market.get('result') != 'no' or market.get('status') != 'finalized':
            raise InventedResultRefused()
        if market.get('occurrence_datetime') is not None:
            raise InventedSoTRefused()
        if market.get('expected_expiration_time') != PARENT_EXPECTED_EXPIRATION[ticker]:
            raise OccurrenceIntegrityRefused()
        if clock_pin(market) != ('expected_expiration_time', PARENT_EXPECTED_EXPIRATION[ticker]):
            raise OccurrenceIntegrityRefused()
        event_ticker = None
        for candidate, markets in PARENT_EVENT_MARKETS.items():
            if ticker in markets:
                event_ticker = candidate
        event = by_event.get(event_ticker)
        if event is None:
            raise OrchestratorError('parent event')
        if event.get('kalshi_occurrence_datetime') is not None:
            raise InventedSoTRefused()
        if ticker not in event.get('market_tickers'):
            raise InventedMarketRefused()
        observed = panel_markets[ticker].get('status_observed')
        if observed != PANEL_STATUS_OBSERVED[ticker]:
            raise OrchestratorError('panel status')
        if 'result' in panel_markets[ticker]:
            raise InventedResultRefused()
        agreed.append(ticker)
    if len(agreed) != PARENT_SEED_N:
        raise OrchestratorError('parent rows')
    return tuple(agreed)


def structural_rows(panel=None):
    """Label authentic reget rows. Does not write scorecard counts."""
    if panel is None:
        panel = load_panel()
    else:
        _validate_panel(panel)
    list_429_gaps()
    agreed = occurrence_agreement_tickers(panel)
    parents = parent_finalized_tickers(panel)
    markets = load_reget()['markets']
    rows = []
    for ticker in agreed:
        market = markets[ticker]
        result = market.get('result')
        if market.get('status') != 'finalized' or result not in FINALIZED_RESULTS:
            raise InventedResultRefused()
        if 'occurrence_datetime' in market:
            raise InventedSoTRefused()
        rows.append({
            'key': ticker,
            'panel_ticker': None,
            'j0': 'nonempty_result_required_pass',
            'j1': 'expected_expiration_time_match',
            'result': result,
            'clock': 'expected_expiration_time',
            'on_settled_list': True,
            'settled_list_row': True,
            'parent_seed': False,
            'single_market_get': False,
            'event_embed': False,
        })
    for ticker in parents:
        rows.append({
            'key': ticker,
            'panel_ticker': ticker,
            'j0': 'parent_ticker_get_nonempty',
            'j1': 'occurrence_null_expected_expiration_on_ticker_get',
            'result': 'no',
            'clock': 'expected_expiration_time',
            'on_settled_list': False,
            'settled_list_row': False,
            'parent_seed': True,
            'single_market_get': True,
            'event_embed': False,
        })
    for key in HONEST_GAPS:
        rows.append({
            'key': key,
            'panel_ticker': None,
            'j0': 'honest_gap',
            'j1': 'honest_gap',
            'result': None,
            'clock': None,
            'on_settled_list': False,
            'settled_list_row': False,
            'parent_seed': False,
            'single_market_get': False,
            'event_embed': False,
        })
    if len(rows) != ROW_LABEL_N:
        raise OrchestratorError('row labels')
    passes = [row for row in rows if row['j0'] == 'nonempty_result_required_pass']
    active = [row for row in rows if row['j0'] == 'parent_ticker_get_nonempty']
    gaps = [row for row in rows if row['j0'] == 'honest_gap']
    if len(passes) != SCOUT_NONEMPTY_N or len(active) != PARENT_SEED_N or len(gaps) != HONEST_GAP_N:
        raise OrchestratorError('row labels')
    return rows


def arm_table():
    return tuple({'id': arm, 'join_gate': JOIN_GATE[arm]} for arm in ARMS)


def instrument_binding(panel=None):
    """One join-gate knob. Fee and rails commits stay unloaded. No scorecard fill."""
    if panel is None:
        panel = load_panel()
    pins = conductor_pin_status()
    if pins['conductor_bytes_in_checkout'] is not True:
        raise OrchestratorError('conductor bytes')
    if pins['governance_s5_cites_present'] is not True or pins['reget_cite_present'] is not True:
        raise OrchestratorError('governance cite')
    rows = structural_rows(panel)
    agreed = occurrence_agreement_tickers(panel)
    parent_agreed = parent_finalized_tickers(panel)
    if len(agreed) != SCOUT_NONEMPTY_N or len(parent_agreed) != PARENT_SEED_N:
        raise OrchestratorError('occurrence rows')
    return {
        'experiment_id': EXPERIMENT_ID,
        'lab_directory': LAB_DIRECTORY,
        'feature_family': FEATURE_FAMILY,
        'knob': KNOB,
        'arms': arm_table(),
        'panel_version': panel['panel_version'],
        'admitted_at': panel.get('admitted_at'),
        'parent_packet_id': PARENT_PACKET_ID,
        'events_n': len(panel.get('events') or []),
        'markets_n': PANEL_MARKETS_N,
        'settled_nonempty_result_N_scout': SCOUT_NONEMPTY_N,
        'scout_n_copied_into_settled_join_n': False,
        'yes_n': YES_N,
        'no_n': NO_N,
        'settled_list_row_n': SETTLED_LIST_ROW_N,
        'parent_seed_tickers': list(PARENT_SEED_TICKERS),
        'parent_seeds_finalized_nonempty_N': PARENT_FINALIZED_N,
        'parent_seed_results': dict(PARENT_SEED_RESULTS),
        'seed_panel_result': None,
        'parent_results_copied_onto_panel': False,
        'panel_stub_active_n': PANEL_STUB_ACTIVE_N,
        'panel_stub_finalized_status_n': PANEL_STUB_FINALIZED_N,
        'parent_reget_occurrence_present': False,
        'occurrence_datetime_present_on_settled_N': 0,
        'expected_expiration_time_present_on_settled_N': SCOUT_NONEMPTY_N,
        'j1_null_occurrence_clock': 'expected_expiration_time',
        'related_series_settled_N': RELATED_SERIES_N,
        'related_series_settled_http': LIST_200,
        'related_series_markets_invented': False,
        'settled_list_http': LIST_200,
        'settled_list_cursor_present': True,
        'cursor_followed': False,
        'open_list_http': None,
        'open_list_n': None,
        'settled_list_earlier_429': LIST_429,
        'finalized_list_429': LIST_429,
        'finalized_list_scout_attempts': '429_honest_then_not_required',
        'events_closed_settled_429': LIST_429,
        'shard1_series_429': LIST_429,
        'list_429_backfilled': False,
        'honest_gap_n': HONEST_GAP_N,
        'occurrence_sources_agree': True,
        'fee_import_used': False,
        'rails_import_used': False,
        'fee_arms': False,
        'feebook_commit_fixed_not_loaded': FEEBOOK_COMMIT,
        'rails_commit_fixed_not_loaded': RAILS_COMMIT,
        'lee_ready': 'REFUSED',
        'logan_keys_required': False,
        'live_orders': False,
        'cap_sr_reopen': False,
        'fq_reopen': False,
        'filllegs_reopen': False,
        'mve_fl_reopen': False,
        's4_rj_reopen': False,
        'nhl_rj_reopen': False,
        'c3_rj_reopen': False,
        'c5_rj_reopen': False,
        'r3p3_rj_reopen': False,
        'r2p3_rj_reopen': False,
        'arm_b_touch': False,
        'conductor_cloud_kick': False,
        'admit_py_run': False,
        'does_not_ungate': list(DOES_NOT_UNGATE),
        's1_s2_r2p4_ungated': False,
        'examiner_status': 'HOLD_PRE_PR',
        'stub_ready': False,
        'scorecard_fields': SCORECARD_FIELDS,
        'row_label_count': len(rows),
        'freeze_sha256': FREEZE_SHA256,
        'scout_reget_sha256': SCOUT_SHA256,
        'seed_summary_sha256': SEED_SHA256,
        'panel_stub_sha256': PANEL_STUB_SHA256,
        'settled_reget_sha256': REGET_SHA256,
        'conductor_accept_sha256': ACCEPT_SHA256,
        'frozen_experiment_sha256': FROZEN_SHA256,
        'empty_results_sha256': EMPTY_SHA256,
        'source_pins_sha256': SOURCE_PINS_SHA256,
        'conductor_bytes_in_checkout': True,
        'governance_s5_cites_present': True,
        'base_commit': BASE_COMMIT,
        'results': None,
        'pnl': None,
        'settled_join_n': None,
        'occurrence_match_n': None,
        'admit_ready_flag': None,
    }


def published_scorecard():
    """Freeze outputs. Every instrument field is present and null."""
    scorecard = {key: None for key in OUTPUT_KEYS}
    for key in OUTPUT_KEYS:
        if scorecard[key] is not None:
            raise ScorecardPromotionRefused()
    scorecard['status'] = 'EMPTY_RESULTS_PRE_EXAMINER'
    scorecard['lee_ready'] = 'REFUSED'
    scorecard['examiner_status'] = 'HOLD_PRE_PR'
    scorecard['stub_ready'] = False
    scorecard['list_429_backfilled'] = False
    scorecard['cursor_followed'] = False
    scorecard['scout_n_copied_into_settled_join_n'] = False
    return scorecard


def assert_null_scorecard(payload):
    """Require every instrument field, results, and pnl, and require null."""
    if not isinstance(payload, dict):
        raise ScorecardPromotionRefused()
    for key in OUTPUT_KEYS:
        if key not in payload or payload[key] is not None:
            raise ScorecardPromotionRefused()
    return payload


def load_scorecard(path):
    """Read a null scorecard. Non-null fields are refused."""
    path = Path(path)
    payload = json.loads(path.read_bytes())
    return assert_null_scorecard(payload)


def write_scorecard(payload):
    """Refuse a missing or non-null measurement field. Nothing is written."""
    assert_null_scorecard(payload)
    raise ScorecardPromotionRefused()


def _report(arm, extra):
    if arm not in JOIN_GATE:
        raise UnknownGate()
    published = published_scorecard()
    report = {
        'experiment_id': EXPERIMENT_ID,
        'arm': arm,
        'join_gate': JOIN_GATE[arm],
        'source': 'authentic_reget',
        'published': published,
        'promoted': False,
        'live_orders': False,
        'lee_ready': 'REFUSED',
        'fee_import_used': False,
        'rails_import_used': False,
        'admit_py_run': False,
        'list_429_backfilled': False,
        'cursor_followed': False,
        'scout_n_copied_into_settled_join_n': False,
        'filllegs_reopen': False,
        'mve_fl_reopen': False,
        's4_rj_reopen': False,
        'nhl_rj_reopen': False,
        'c3_rj_reopen': False,
        'c5_rj_reopen': False,
        'r3p3_rj_reopen': False,
        'r2p3_rj_reopen': False,
        'fq_reopen': False,
        'cap_sr_reopen': False,
        'arm_b_touch': False,
        'conductor_cloud_kick': False,
        's1_s2_r2p4_ungated': False,
        'examiner_status': 'HOLD_PRE_PR',
        'stub_ready': False,
    }
    report.update(extra)
    for key in OUTPUT_KEYS:
        report[key] = None
    assert_null_scorecard(report)
    assert_null_scorecard(published)
    return report


def conduct(arm, panel=None):
    """Schema for one join gate. Scorecard fields stay null."""
    if arm not in JOIN_GATE:
        raise UnknownGate()
    if panel is None:
        panel = load_panel()
    rows = structural_rows(panel)
    agreed = occurrence_agreement_tickers(panel)
    parent_agreed = parent_finalized_tickers(panel)
    extra = {
        'row_labels': rows,
        'occurrence_agreement_tickers': list(agreed),
        'parent_finalized_tickers': list(parent_agreed),
        'admitted_at': panel.get('admitted_at'),
        'event_count': len(panel.get('events') or []),
        'market_count': PANEL_MARKETS_N,
    }
    return _report(arm, extra)


def frozen_output_snapshot():
    """Read freeze files. Does not modify them."""
    frozen_payloads = {
        'frozen': json.loads(FROZEN_EXPERIMENT.read_text()),
        'bundle_frozen': json.loads((LAB_BUNDLE / 'FROZEN_EXPERIMENT.json').read_text()),
    }
    empty_payloads = {
        'empty': json.loads(EMPTY_RESULTS.read_text()),
        'bundle_results': json.loads((LAB_BUNDLE / 'results.json').read_text()),
        'bundle_empty': json.loads((LAB_BUNDLE / 'results' / 'EMPTY_RESULTS.json').read_text()),
    }
    snapshot = {}
    for name, payload in frozen_payloads.items():
        for key in ('results', 'pnl'):
            if key not in payload or payload[key] is not None:
                raise ScorecardPromotionRefused()
            snapshot['%s.%s' % (name, key)] = None
        if payload.get('admitted_at') is not None:
            raise OrchestratorError('admitted_at')
    for name, payload in empty_payloads.items():
        for key in OUTPUT_KEYS:
            if key not in payload or payload[key] is not None:
                raise ScorecardPromotionRefused()
            snapshot['%s.%s' % (name, key)] = None
    return snapshot
