"""C2 builder receipt, R20 counts, and the STRUCTURE gate.

STRUCTURE is the only reader of quote as-of values. This module never reads
quote prices.
"""

import math

from .constants import THRESHOLD_HEADLINE, THRESHOLD_S5K
from .errors import ClosedUniverseRefused
from .refusals import assert_timestamp_allowed


def structural_counts(rows):
    """KD-3 and KD-4, without the event-count check (that needs the market map)."""
    trades = 0
    quotes = 0
    tickers = set()
    taker_yes = 0
    taker_no = 0
    no_ge_headline = 0
    no_ge_s5k = 0
    yes_ge_headline = 0
    yes_ge_s5k = 0
    for row in rows:
        kind = row.get("kind")
        ticker = row["ticker"]
        tickers.add(ticker)
        if kind == "quote":
            quotes += 1
            continue
        trades += 1
        side = row["taker_side"]
        size = row["size"]
        if side == "yes":
            taker_yes += 1
            if size >= THRESHOLD_HEADLINE:
                yes_ge_headline += 1
            if size >= THRESHOLD_S5K:
                yes_ge_s5k += 1
        elif side == "no":
            taker_no += 1
            if size >= THRESHOLD_HEADLINE:
                no_ge_headline += 1
            if size >= THRESHOLD_S5K:
                no_ge_s5k += 1
    return {
        "trades": trades,
        "quotes": quotes,
        "tickers": len(tickers),
        "taker_yes_trades": taker_yes,
        "taker_no_trades": taker_no,
        "per_print_counts": {
            "NO_ge_1000": no_ge_headline,
            "NO_ge_5000": no_ge_s5k,
            "YES_ge_1000": yes_ge_headline,
            "YES_ge_5000": yes_ge_s5k,
        },
    }


def count_gate(rows, markets, week_membership, pins):
    """KD-4. events must equal both the expected count and len(week_membership)."""
    observed = structural_counts(rows)
    events = set()
    for row in rows:
        ticker = row["ticker"]
        if ticker not in markets:
            raise ClosedUniverseRefused(ticker)
        event = markets[ticker]["event"]
        if event not in week_membership:
            raise ClosedUniverseRefused(event)
        events.add(event)
    observed["events"] = len(events)
    expected = pins.expected_counts
    matches = (
        observed["trades"] == expected["trades"]
        and observed["quotes"] == expected["quotes"]
        and observed["tickers"] == expected["tickers"]
        and observed["events"] == expected["events"]
        and observed["events"] == len(week_membership)
        and observed["taker_yes_trades"] == expected["taker_yes_trades"]
        and observed["taker_no_trades"] == expected["taker_no_trades"]
        and observed["per_print_counts"] == expected["per_print_counts"]
    )
    return {"observed": observed, "expected": expected, "pass": matches}


def _malformed_timestamp(value):
    """NaN, inf, text, and other non-finite values. They fail the gate; they do not raise."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return True
    try:
        number = float(value)
    except (TypeError, ValueError, OverflowError):
        return True
    return math.isnan(number) or math.isinf(number)


def structure_gate(rows):
    """RE-2. Quote publication lag, and trade-time resolution not coarser than 1s."""
    quote_ok = True
    trade_times = []
    malformed = False
    trade_malformed = False
    for row in rows:
        if row.get("kind") == "quote":
            at = row.get("at")
            asof = row.get("asof")
            if _malformed_timestamp(at) or _malformed_timestamp(asof):
                malformed = True
                quote_ok = False
                continue
            assert_timestamp_allowed(asof)
            if (at - asof) != 60 or asof % 60 != 0:
                quote_ok = False
        else:
            at = row.get("at")
            if _malformed_timestamp(at):
                malformed = True
                trade_malformed = True
                continue
            assert_timestamp_allowed(at)
            trade_times.append(at)
    if trade_malformed:
        resolution_ok = False
    elif any(float(at) != math.floor(float(at)) for at in trade_times):
        resolution_ok = True
    else:
        divisor = 0
        for at in trade_times:
            divisor = math.gcd(divisor, int(at))
        resolution_ok = divisor == 1
    result = {
        "quote_at_minus_asof_60_and_asof_mod_60_0": quote_ok,
        "trade_at_not_coarser_than_1s": resolution_ok,
        "pass": quote_ok and resolution_ok and not malformed,
    }
    if malformed:
        result["reason"] = "STRUCTURE_TIMESTAMP_MALFORMED"
        result["pass"] = False
    return result


def builder_receipt(observed_sha256, expected_sha256, path):
    """C2. Absence is a mismatch. Callers record this before any mid."""
    if observed_sha256 is None:
        reason = "C2_BUILDER_SHA_MISSING"
        match = False
    elif observed_sha256 != expected_sha256:
        reason = "C2_BUILDER_SHA_MISMATCH"
        match = False
    else:
        reason = None
        match = True
    receipt = {
        "path": path,
        "sha256": observed_sha256,
        "expected_sha256": expected_sha256,
        "match": match,
    }
    if reason is not None:
        receipt["reason"] = reason
    return receipt
