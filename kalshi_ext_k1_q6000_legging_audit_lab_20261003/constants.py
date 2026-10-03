"""Frozen EXT-K1 constants. No new knobs."""

from decimal import Decimal

EXPERIMENT_ID = "EXT-K1-Q6000-LEGGING-RISK-AUDIT"
LAB_NAME = "kalshi_ext_k1_q6000_legging_audit_lab_20261003"

BUNDLE_SHA256 = "0f8f529733bfd1ccb01b36f312cdc20865cc2811c04dcd3c812d50c67295db38"
MANIFEST_SHA256 = "a041561e130fb97eaa8d7bfab5dd6fa53963fa4fbdb13c00cd4f71089e0e3db5"
FREEZE_MD_SHA256 = "5c40fb9d03a924e40577a81f262231701e331c98922f60f6dc7ab65a2dbed6d3"
FREEZE_JSON_SHA256 = "be3e88336389bc62c40413785e6ffb4a572e1dbd006d7cf3dfbc962f8184efaa"
ACCEPT_SHA256 = "021290077cbbed277455145d2e56e1335f6ae331d56c2ad79d4d85b405559397"
# ACCEPT.verified.manifest is a different digest from the inner bundle MANIFEST.
ACCEPT_CLAIMED_MANIFEST_SHA256 = "5e8f79063f132fe2db97ad3ecff5fea463d429f167abed09c58398a87fcadf01"

HOLDOUT_SHA256 = "74507e1a4371d69bc79ea2369f9bff030a74f51ee80c8072ba9c0f5345d377ca"
PREREG_ACCEPT_SHA256 = "9a987a77e6cd6293ddaeb14fadbf33a25c1a6cc392af25f46eaaaaae33ebb273"
PREREG_ADDENDUM_SHA256 = "370dc31df17191446013b6cebb52d44ee8346f47d2f5b543a1c73049ba52c063"
REPLAY_SHA256 = "5aba1bf36385d9defeb032040dd6560d3eb1a192fc0203e984a47d9e7c3f37c3"
QUEUE_POLICIES_SHA256 = "641d0df3913f4a66fb926c84d170fe1fe61347a2fad16959b6824abb0c135fc2"
RUN_EXPERIMENT_SHA256 = "c1a0fd2d85637b4fe909a24ca96784d3a99fe0a07c03bcef024c9fa16bbf84bc"
SUMMARY_SHA256 = "78b94ae5a846dfa81a1baec8fdc0b7992e479af1ddbc67908195f47500a7930a"
FILLS_SHA256 = "9d56f5d3c599e092606be9f4a1ad41ae8baabff4921d3d722adf0b57ac944a3f"
ORDERS_SHA256 = "c390801b9a7cf6d182d2d097123ed944792980524a7975e6e59a904a530f4b1c"
DECISIONS_SHA256_NOT_BUNDLED = "e6db52374f834bba210d5c17836828ac3bf0dd54ca9feb5836ea71a611c61b71"
FEE_SCHEDULE_SHA256 = "d9435b8b7e30fecbe1a07539990667b23b828a8175962c0882d6c7bce93980ec"
REGISTRY_CITATION_SHA256 = "0860cbe28d28ecc6142ddf6f1ebb67792084264ed82e0b4d868c3b3138ea5312"

ALIAS_MAP = {"JAC": "JAX", "LAR": "LA"}

PINNED_GAME_IDS = (
    "2026_01_NE_SEA",
    "2026_01_SF_LA",
    "2026_01_ARI_LAC",
    "2026_01_ATL_PIT",
    "2026_01_BAL_IND",
    "2026_01_BUF_HOU",
    "2026_01_CHI_CAR",
    "2026_01_CLE_JAX",
    "2026_01_DAL_NYG",
    "2026_01_GB_MIN",
    "2026_01_MIA_LV",
    "2026_01_NO_DET",
    "2026_01_NYJ_TEN",
    "2026_01_TB_CIN",
    "2026_01_WAS_PHI",
    "2026_01_DEN_KC",
    "2026_02_DET_BUF",
    "2026_02_CAR_ATL",
    "2026_02_CIN_HOU",
    "2026_02_CLE_TB",
    "2026_02_GB_NYJ",
    "2026_02_IND_KC",
    "2026_02_JAX_DEN",
    "2026_02_LV_LAC",
    "2026_02_MIA_SF",
    "2026_02_MIN_CHI",
    "2026_02_NO_BAL",
    "2026_02_PHI_TEN",
    "2026_02_PIT_NE",
    "2026_02_SEA_ARI",
    "2026_02_WAS_DAL",
)

# R18. Primary horizon is the first grid point at or above the ledger weighted-median pair hold.
HORIZONS_S = (60, 300, 1800, 3600)
PRIMARY_HORIZON_S = 1800
PRIMARY_DELTA = 0.005
DELTA_SENSITIVITY = (0.0, 0.01)

# R27 / R28. The primary cell is fixed. The grid is sensitivity only.
PRIMARY_GATE = {"x": 0.02, "E": 0.0, "devig": "proportional"}
GATE_X = (0.01, 0.02, 0.03, 0.05)
GATE_E = (0.0, 125.0)
GATE_DEVIG = ("proportional", "shin")

MAKER_COEFFICIENT = Decimal("0.0175")
FEE_LABEL = "CACHE_NOT_R1P1"
FEE_HEADLINE_NAME = "NON_DIRECT_CENT_HEADLINE"
EXAMINER_PIN_ACCOUNT_CLASS = None

BOOTSTRAP_B = 10000
BOOTSTRAP_SEED = 20261003

UNPINNED_RULES = (
    "R06", "R08", "R10", "R12", "R14", "R16", "R18", "R21",
    "R23", "R24", "R25", "R27", "R28", "R30", "R31", "R32",
)

VERDICT_DOMAIN = ("DESCRIPTIVE", "ITERATE", "INCONCLUSIVE")

EX_POST_SENTENCE = (
    "nflverse line timing undocumented [U]; ex-post anchor only; "
    "cannot support a tradable pre-game signal claim."
)

REFUSED_PATHS = (
    "lab/astra-capture/prospective/capture.sqlite",
    "lab/astra-capture/weather-nowcast/archive.sqlite",
)

# R36 reproduction targets.
MAKER_NO_SHARE = 0.9897056563576855
MAKER_NO_SHARE_6DP = 0.989706
SCOUT_MAKER_NO_SHARE = 0.990
TAKER_YES_SHARE = 0.9168821893495998
TAKER_YES_SHARE_6DP = 0.916882
SCOUT_TAKER_YES_SHARE = 0.917
LEDGER_UCH = 603262.7291176913
FILL_ROWS = 12853
TRADE_ROWS = 681732
QUOTE_ROWS = 364988
TICKERS = 62
EVENTS = 31
MAKER_NO_CONTRACTS = 321622.45
MAKER_YES_CONTRACTS = 3345.33
MAKER_CONTRACTS = 324967.78
TAKER_CONTRACTS = 2068.66
PAIRED_UNITS = 163518.22
OPENING_PORTIONS = 6161

PINS_REL = {
    "holdout": "lab/astra-science/nfl_factorial_lab_20260921/RESERVED_HOLDOUT.json",
    "markets": "lab/astra-science/nfl_factorial_lab_20260921/inputs/markets.json",
    "weeks": "lab/astra-science/nfl_factorial_lab_20260921/inputs/week_membership.json",
    "events": "lab/astra-science/nfl_factorial_lab_20260921/inputs/events.jsonl.gz",
    "summary": "lab/astra-science/nfl_factorial_lab_20260921/results/q3300_d0.25_000.json",
    "fills": "lab/astra-science/nfl_factorial_lab_20260921/results/q3300_d0.25_000_fills.jsonl.gz",
    "orders": "lab/astra-science/nfl_factorial_lab_20260921/results/q3300_d0.25_000_orders.jsonl.gz",
    "replay": "lab/astra-science/nfl_factorial_lab_20260921/replay_v2.py",
    "queue": "lab/astra-science/nfl_factorial_lab_20260921/queue_policies.py",
    "run": "lab/astra-science/nfl_factorial_lab_20260921/run_experiment.py",
    "games": "lab/governance/astra/packets/scout_external_hunt_2026-10-03/raw/nflverse_nfldata_games.csv",
    "schedule": "lab/governance/astra/packets/scout_house_fee_2026-09-24/raw/docs/kalshi_fee_schedule.txt",
    "prereg_json": "lab/governance/astra/packets/CONDUCTOR_ACCEPT_VARIANTS_HOLDOUT_PREREG_ADDENDUM_Q6S5_KXMLBSPREAD_UNTOUCHED_CAPTURE_2026-10-01.json",
    "prereg_md": "lab/governance/astra/packets/VARIANTS_HOLDOUT_PREREG_ADDENDUM_Q6S5_KXMLBSPREAD_UNTOUCHED_CAPTURE_2026-10-01.md",
}
