"""R24–R26 headline fees. Decimal arithmetic. Account class stays an Examiner pin."""

import re
from decimal import Decimal, ROUND_CEILING

from constants import (
    EXAMINER_PIN_ACCOUNT_CLASS,
    FEE_HEADLINE_NAME,
    FEE_LABEL,
    MAKER_COEFFICIENT,
)
from errors import FeeScheduleError

SIX = Decimal("0.000001")
CENT = Decimal("0.01")


def D(value):
    if isinstance(value, Decimal):
        return value
    if isinstance(value, int) and not isinstance(value, bool):
        return Decimal(value)
    return Decimal(str(value))


def read_kxnflgame_maker_multiplier(schedule_text):
    """Maker M for series KXNFLGAME, read from the cached schedule table."""
    found = []
    for line_no, line in enumerate(schedule_text.splitlines(), 1):
        stripped = line.strip()
        if not re.match(r"KXNFLGAME\b", stripped):
            continue
        numbers = re.findall(r"(?<![\w.])(\d+)(?![\w.])", stripped)
        if len(numbers) < 2:
            raise FeeScheduleError(f"KXNFLGAME row {line_no} has no multiplier pair")
        found.append((line_no, numbers[-2], numbers[-1]))
    if not found:
        raise FeeScheduleError("KXNFLGAME absent from fee schedule")
    if any(maker != "1" or taker != "1" for _, maker, taker in found):
        raise FeeScheduleError(found)
    return Decimal(1), tuple(found)


def model_fee(contracts, price, multiplier=Decimal(1)):
    """Return (unrounded model fee, ceil to 6 decimal places)."""
    contracts = D(contracts)
    price = D(price)
    multiplier = D(multiplier)
    raw = multiplier * MAKER_COEFFICIENT * contracts * price * (Decimal(1) - price)
    six = raw.quantize(SIX, rounding=ROUND_CEILING)
    return raw, six


def ceil_cent(amount):
    return D(amount).quantize(CENT, rounding=ROUND_CEILING)


def headline_order_fee(fills, multiplier=Decimal(1)):
    """F_o = ceil to $0.01 of the sum of per-fill 6dp model fees. Pro rata by contracts.

    fills is a sequence of (contracts, price). Returns (F_o, fee_per_contract, six_dp_sum).
    """
    sixes = []
    total = Decimal(0)
    for contracts, price in fills:
        _raw, six = model_fee(contracts, price, multiplier)
        sixes.append(six)
        total += D(contracts)
    if total <= 0:
        raise FeeScheduleError("order has no contracts")
    six_sum = sum(sixes, Decimal(0))
    order_fee = ceil_cent(six_sum)
    return order_fee, order_fee / total, six_sum


def direct_member_per_contract(ledger_fee, size):
    """R25 sensitivity. Never the headline."""
    size = D(size)
    if size <= 0:
        raise FeeScheduleError("fill size")
    return D(ledger_fee) / size


def fee_labels():
    return {
        "fee_label": FEE_LABEL,
        "headline_name": FEE_HEADLINE_NAME,
        "examiner_pin_account_class": EXAMINER_PIN_ACCOUNT_CLASS,
        "maker_coefficient": float(MAKER_COEFFICIENT),
        "maker_multiplier_kxnflgame": 1,
    }
