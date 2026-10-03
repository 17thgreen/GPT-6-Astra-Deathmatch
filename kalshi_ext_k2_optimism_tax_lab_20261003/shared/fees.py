"""Fee arithmetic. Headline is the non-direct cent round-up. Direct-member is sensitivity.

Part (a) uses the K1 per-order accumulator (ceil to 6 dp, then ceil to $0.01).
Part (b) uses the per-trade proxy. Gross is the headline wherever a net sits beside it.
"""

from decimal import Decimal, ROUND_CEILING


class FeeCacheRefused(Exception):
    """The cached KXNFLGAME multiplier was not the pinned M=1."""


MAKER_COEF = Decimal("0.0175")
TAKER_COEF = Decimal("0.07")
FEE_LABEL = "CACHE_NOT_R1P1"
# Conductor ACCEPT: Becker net is an illustrative 2026-schedule sensitivity, not history.
NET_ILLUSTRATIVE_LABEL = "NET_ILLUSTRATIVE_2026_SCHEDULE_NOT_HISTORICAL"
PER_TRADE_PROXY_LABEL = "PER_TRADE_PROXY"
FEE_2026_ON_2025_LABEL = "FEE_SCHEDULE_2026_CACHE_APPLIED_TO_2025_TRADES_U"
PROXY_OVERSTATEMENT = (
    "The one-maker-plus-one-taker-per-trade proxy overstates fees when one order "
    "matches several rows, because the sum of per-row cent ceilings is at least "
    "the ceiling of the sum. It is not a fill, queue, or quote model."
)


def _ceil(value, quantum):
    return Decimal(value).quantize(Decimal(quantum), rounding=ROUND_CEILING)


def ceil_6dp(value):
    return _ceil(value, "0.000001")


def ceil_cent(value):
    return _ceil(value, "0.01")


def ceil_subcent(value):
    """Direct-member sensitivity: ceiling to $0.0001. Never the headline."""
    return _ceil(value, "0.0001")


def read_kxnflgame_multiplier(schedule_text):
    """M for KXNFLGAME from the cached fee schedule. Both columns must be 1."""
    import re
    found = re.findall(
        r"KXNFLGAME\s+Professional Football Game\s+(\d+)\s+(\d+)",
        schedule_text,
    )
    if not found:
        raise FeeCacheRefused("KXNFLGAME row missing from the fee cache")
    for maker_m, taker_m in found:
        if maker_m != "1" or taker_m != "1":
            raise FeeCacheRefused("KXNFLGAME multiplier is not 1")
    return Decimal(1)


def model_quadratic(coef, contracts, price, multiplier):
    """coef * M * C * p * (1-p) as an exact Decimal. price is a probability."""
    c = Decimal(contracts)
    p = Decimal(price)
    m = Decimal(multiplier)
    return Decimal(coef) * m * c * p * (Decimal(1) - p)


def part_a_order_headline(fills, multiplier):
    """K1 R24. fills are (contracts, price) pairs of one maker order.

    Returns the order fee in dollars (cent ceiling) and the per-contract allocation.
    """
    total_c = Decimal(0)
    acc = Decimal(0)
    for contracts, price in fills:
        total_c += Decimal(contracts)
        acc += ceil_6dp(model_quadratic(MAKER_COEF, contracts, price, multiplier))
    headline = ceil_cent(acc)
    per_contract = (headline / total_c) if total_c != 0 else None
    return headline, per_contract


def part_b_row_fee(coef, contracts, yes_cents, multiplier=Decimal(1)):
    """Per-trade proxy. Returns (model, cent_headline, subcent_sensitivity)."""
    price = Decimal(int(yes_cents)) / Decimal(100)
    model = model_quadratic(coef, contracts, price, multiplier)
    return model, ceil_cent(model), ceil_subcent(model)


def part_b_group_cent(rows, coef, multiplier=Decimal(1)):
    """Sensitivity 2: one ceiling on the sum of model fees in a sweep group.

    rows are (contracts, yes_cents). Maker fees are not grouped here.
    """
    acc = Decimal(0)
    for contracts, yes_cents in rows:
        price = Decimal(int(yes_cents)) / Decimal(100)
        acc += model_quadratic(coef, contracts, price, multiplier)
    return ceil_cent(acc)
