"""AF-8 entry gate.

Fees come from an astra.fee_source.v1 file loaded at runtime. One unpinned
series blocks the card. No fee, net, or signal is computed in that case.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from decimal import Decimal
from pathlib import Path

from card01_amc.fee_source import (
    CONDUCTOR_ACCEPT_SHA256,
    FEE_SOURCE_ID,
    FEE_SOURCE_SHA256,
    FeeBlocked,
    load_fee_source,
    pinned_entry,
    pinned_taker_fee,
)
from card01_amc.pinload import sha256_bytes

EXTRA_COST = Decimal("0.02")
RESERVE = Decimal("0.03")
SELECT_EPS = Decimal("1e-12")
OUTCOME_KEYS = ("y", "result", "settlement", "outcome", "settled")


class OutcomePresent(RuntimeError):
    pass


def module_sha256() -> str:
    return sha256_bytes(Path(__file__).read_bytes())


def _rows_of(doc):
    if isinstance(doc, dict) and isinstance(doc.get("rows"), list):
        return doc["rows"]
    if isinstance(doc, list):
        return doc
    raise ValueError("rows must be a list or an object with rows")


def _refuse_outcomes(rows):
    for row in rows:
        if not isinstance(row, dict):
            continue
        for key in OUTCOME_KEYS:
            if key in row and row[key] is not None:
                raise OutcomePresent(key)


def _series_of(row):
    series = row.get("series")
    if isinstance(series, str) and series:
        return series
    if row.get("mapping_status") == "KXHOUSERACE":
        return "KXHOUSERACE"
    return None


def _scorable(row) -> bool:
    return (
        row.get("mapping_status") in ("KXHOUSERACE", "LEGACY")
        and row.get("p_market") is not None
        and row.get("p_model") is not None
    )


def _blocked(reason, blocked_series=None):
    return {
        "status": "BLOCKED_FEE_UNVERIFIED",
        "signals": None,
        "reason": reason,
        "blocked_series": list(blocked_series or []),
    }


def _qty_ok(value) -> bool:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return False
    return math.isfinite(float(value)) and float(value) >= 1


def _select(row, entry):
    if row.get("yes_bid") is None or row.get("yes_ask") is None:
        return None
    model = Decimal(str(row["p_model"]))
    market = Decimal(str(row["p_market"]))
    q = Decimal("0.5") * model + Decimal("0.5") * market
    bid = Decimal(str(row["yes_bid"]))
    ask = Decimal(str(row["yes_ask"]))
    choices = []
    for side, prob, price, qty_key in (
        ("yes", q, ask, "yes_ask_qty"),
        ("no", Decimal(1) - q, Decimal(1) - bid, "yes_bid_qty"),
    ):
        quoted = pinned_taker_fee(entry, price)
        headline = quoted["headline"]
        expected_net = prob - (price + headline + EXTRA_COST)
        choices.append({
            "side": side,
            "price": price,
            "headline": headline,
            "direct": quoted["sensitivity_direct_member"],
            "expected_net": expected_net,
            "qty": row.get(qty_key),
        })
    best = max(choices, key=lambda item: (item["expected_net"], item["side"] == "yes"))
    if not (best["expected_net"] > RESERVE + SELECT_EPS):
        return None
    if not _qty_ok(best["qty"]):
        return None
    return best


def gate(
    rows,
    fee_source_bytes=None,
    *,
    expected_sha256=FEE_SOURCE_SHA256,
    expected_id=FEE_SOURCE_ID,
    expected_accept=CONDUCTOR_ACCEPT_SHA256,
):
    """Apply the frozen gate. Expectation overrides are for tests. The CLI does not pass them."""
    _refuse_outcomes(rows)
    if fee_source_bytes is None:
        return _blocked("FEE_SOURCE_ABSENT")
    try:
        loaded = load_fee_source(
            fee_source_bytes,
            expected_sha256=expected_sha256,
            expected_id=expected_id,
            expected_accept=expected_accept,
        )
    except FeeBlocked as exc:
        return _blocked(exc.reason, exc.blocked_series)

    used = []
    seen = set()
    for row in rows:
        if not isinstance(row, dict) or not _scorable(row):
            continue
        series = _series_of(row)
        if series not in seen:
            seen.add(series)
            used.append(series)
    entries = {}
    blocked = []
    first_reason = None
    for series in used:
        try:
            entries[series] = pinned_entry(loaded, series)
        except FeeBlocked as exc:
            blocked.append(series)
            if first_reason is None:
                first_reason = exc.reason
    if blocked:
        return _blocked(first_reason, blocked)

    signals = []
    for row in rows:
        if not isinstance(row, dict) or not _scorable(row):
            continue
        series = _series_of(row)
        best = _select(row, entries[series])
        if best is None:
            continue
        signals.append({
            "race_id": row["race_id"],
            "side": "D_YES" if best["side"] == "yes" else "D_NO",
            "price": float(best["price"]),
            "fee": float(best["headline"]),
            "fee_decimal": str(best["headline"]),
            "fee_sensitivity_direct_member": str(best["direct"]),
            "fee_rounding": "NON_DIRECT_CEIL_CENT",
            "contracts": 1,
            "series": series,
            "fee_type": entries[series].fee_type,
            "fee_multiplier": entries[series].fee_multiplier_str,
            "fee_source": loaded.manifest_id,
            "fee_source_sha256": loaded.sha256,
            "visible_qty": best["qty"],
            "expected_net_gate": float(best["expected_net"]),
        })
    return {
        "status": "OK",
        "n_selected": len(signals),
        "signals": signals,
        "fee_source": loaded.manifest_id,
        "fee_source_sha256": loaded.sha256,
        "fee_source_status": "ADOPTED",
        "conductor_accept_sha256": loaded.conductor_accept_sha256,
        "series_used": [{"series": series, "series_status": "PINNED"} for series in used],
        "gate_sha256": module_sha256(),
    }


def main(argv):
    parser = argparse.ArgumentParser(description="outcome-free entry gate")
    parser.add_argument("rows")
    parser.add_argument("--fee-source", default=None)
    args = parser.parse_args(argv)
    try:
        rows = _rows_of(json.loads(Path(args.rows).read_text()))
        fee_bytes = Path(args.fee_source).read_bytes() if args.fee_source else None
        obj = gate(rows, fee_bytes)
    except (OutcomePresent, ValueError, json.JSONDecodeError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    json.dump(obj, sys.stdout, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
