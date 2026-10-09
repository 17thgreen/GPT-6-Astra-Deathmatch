"""Pins and kit defaults. Each KD is one named constant or lives in one function.

KD-5, KD-6, KD-7, and KD-19 are frozen at these kit values
(Conductor addendum 2026-10-09). The other KD defaults stand as written.
"""

EXPERIMENT_ID = "EXT2-K1-SWEEP-REVERSION"

# Governing identities. Freeze md/json are pinned by sha and are not vendored.
FREEZE_MD_SHA256 = "8f35fa77cab5872f7956df34c145fda2e8ae5587e1c1396ca2d39b5e347676a9"
FREEZE_JSON_SHA256 = "afbcd089888c84fb5db4e611b1e58ef59a558d4b379c843bae68c82a386ed8af"
ACCEPT_SHA256 = "d3ddc2ca50db07f36142acce38add4153beeba2c466cfdebba647671049abf21"
ADVERSARY_PASS_SHA256 = "9da36baaf76d60eb221d3ed71605e4951e7ffe9e1e4bb3d01261fe60230d7797"
RULING_CONDITIONAL_SHA256 = "7bd04408703b7a0d5e36967477e1e697d03a131e28fe4d30f7439b0a9ca7abe8"
KERNEL_RULING_SHA256 = "85376e40518e5a51066ce290505ab3896bb804b43ad1780e48df0485d4d310fa"
FREEZE_R1_MD_SHA256 = "c2dcce31725eae1c1c238d924701b8712d1879c3093c620fba634e662d089c90"
FREEZE_R1_JSON_SHA256 = "78ae5d7dcaeee8e11c3166dcf8fee13009a6f4e915e819bd43a3a2af6f862915"
ADVERSARY_PREREVIEW_SHA256 = "8a1a38049e79b77c95caf74f561b16599f2e4e9a687c4a10aa7d507d251b58a0"
STANDING_BOOTSTRAP_SHA256 = "6824793a44f5a10ee1d6e869e694d6681cfaba1681ff9b4bfb7cd0ed98242502"
PUBLIC_REPO_RULE_SHA256 = "b1c1851f3edfd04ad9d2d0c91fed17e86f6fd543ad0f489f4775d1540478017f"
N6_RULING_SHA256 = "0b68c4bf218e7f85fa8af760ebcf5424d4e77262e62a5d71c43e9a5d2b929291"
FEE_AMENDMENT_SHA256 = "2c870cd57fc4acb4290c1273e06876e8380159f2f6614a5519314b43817a8583"
FEE_SOURCE_CARD01_V2_SHA256 = "6edc3effcd3bed0ce3a3b586880de50835440a3b1925b5803093c826424aea7f"
COMPLETION_FROZEN_CODE_SHA256 = "fbbef411cefae9c692b7a636b1d144ec36eb24c148e27b27814a5734b4e1414c"
R1_SQUASH_SHA256 = "05f8147e2ab1d823ca3144f16e0a9a3e80da6d48"
PR_C_SQUASH_SHA256 = "df7f514c43e29b0bc8fe067e0ff8d3090cdc3d3e"

BUILDER_RELATIVE_PATH = "nfl_completion_lab_20260921/load_data.py"
BUILDER_SHA256 = "817c74deec49103ff8e1849c23677b207cb698e5cb05559b69978fe25eaa2ca3"

HOLDOUT_SHA256 = "74507e1a4371d69bc79ea2369f9bff030a74f51ee80c8072ba9c0f5345d377ca"
TAPE_SHA256 = "cd300e664c2c5f2ff344c4b1eb17dd3f8e5f3326168b9dd8e3ade94a3a7382b4"
MARKETS_SHA256 = "66cc07e9e9e1543b3fdcbcded30ff50af0abae87bb2aa3d5fcb3d0be7925632f"
COHORT_SHA256 = "a47d0e0dc5a64d79335bc5588f8aa5e1d937503d36ebcbaaf219965a68adf88c"
B2_SHA256 = "9d56f5d3c599e092606be9f4a1ad41ae8baabff4921d3d722adf0b57ac944a3f"

# KD-18. Depends only on seed 20261008 and a cohort of length 31.
IDX_SHA256_N31 = "3539beba07d6ded86ab20954df75fa7797d821f873c8a61006f6500df7902c36"

SEED = 20261008
B = 10000
N_PERM = 1000
HORIZONS = (60, 300, 900, 1800, 3600)
K_STAR = 900
ENTRY_GAP_S = 120
STALE_SECONDS = 300
ISO_LOOKBACK_S = 3600

# KD-1 thresholds. Integers, so the SWEEPS document matches the kit schema.
THRESHOLD_HEADLINE = 1000
THRESHOLD_S5K = 5000
SWEEPS_SCHEMA = "astra.ext2k1.sweeps.v1"
RECEIPT_SCHEMA = "astra.ext2k1.receipt.v1"
SWEEP_KEY = ("ticker", "at", "taker_side")
SWEEP_ORDER = ("t_s", "ticker", "taker_side")

# KD-8 / KD-19 floors. Strict inequalities. Frozen for KD-19.
DROPPED_LIMIT = 500
CENSOR_SHARE_LIMIT = 0.20
MIN_GAMES = 5
BAND_LO = 0.05
BAND_HI = 0.95

# KD-13.
FEE_ADMISSION = "BLOCKED_FEE_UNVERIFIED"
FEE_BLOCK_REASON = "KXNFLGAME_NOT_IN_ADMITTED_FEE_SOURCE"
FUTURE_NET_LABEL = "ILLUSTRATIVE (R39)"
EXAMINER_PIN_ACCOUNT_CLASS = None

# Real-run cross-check. Not a gate (KD-14).
POST_GROUP_EXPECTED_NO = 317
POST_GROUP_EXPECTED_YES = 4367

SAMPLER_STRING = (
    "random.Random(20261008).choices(range(31),k=31) over sorted cohort events; "
    "one IDX shared"
)
PERCENTILE_METHOD = "type-7, K1 report._percentile expression; <2 kept -> None"
AGGREGATION = "math.fsum per event and per draw"

TAGS = (
    "DEV_GRADE_REUSED_31_GAME_COHORT",
    "IN_SAMPLE_DEV",
    "CACHE_NOT_R1P1",
)

VERDICT_DOMAIN = (
    "KILL_EXT2K1",
    "CLOSE_NULL",
    "ITERATE_DESCRIPTIVE",
    "INCONCLUSIVE",
    "INCONCLUSIVE(STRUCTURE)",
)

# R20 count gate for the real B1 tape. Synthetic Pins replace this object.
PRODUCTION_EXPECTED_COUNTS = {
    "trades": 681732,
    "quotes": 364988,
    "tickers": 62,
    "events": 31,
    "taker_yes_trades": 636251,
    "taker_no_trades": 45481,
    "per_print_counts": {
        "NO_ge_1000": 343,
        "NO_ge_5000": 94,
        "YES_ge_1000": 4500,
        "YES_ge_5000": 608,
    },
}

# KD-21. One object, verdict_effect NONE.
REPORTING_DEFECT = {
    "kind": "FREEZE_R2_CHANGELOG_OMITS_FIVE_WORDING_CHANGES",
    "items": [
        "(i) R20 timing 'before any quote value is read' -> 'logged before any mid is read'",
        "(ii) R21 'T01-T07 green' -> 'T01-T09'",
        "(iii) T08 drops the '(K1 T04 vectors)' reference for ADMIT-1 edge cases",
        "(iv) T06 'drop counting on a zero-sweep draw' -> 'drop counting'",
        "(v) P1 drops the 20261003 convention rationale; seed unchanged",
    ],
    "verdict_effect": "NONE",
    "validity_effect": "NONE",
    "blocking": False,
}


class Pins:
    """Expected gate counts and the builder sha. Tests pass a synthetic instance."""

    def __init__(self, expected_counts, builder_expected_sha256):
        self.expected_counts = expected_counts
        self.builder_expected_sha256 = builder_expected_sha256


PRODUCTION_PINS = Pins(PRODUCTION_EXPECTED_COUNTS, BUILDER_SHA256)
