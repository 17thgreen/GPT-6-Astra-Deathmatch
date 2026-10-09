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

from card01_amc.fee_admission import admit_fee_source_v2, pinned_entry_v2
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


def fee_attest_reason(fee_sha, attest):
    """Return None when the attest admits this fee-source sha.

    Shape, marked as a kit reading: a JSON object with
    fee_source_sha256 equal to the fee-source bytes, and verdict
    exactly ATTEST_PASS. No other field is read.
    """
    if attest is None:
        return "FEE_ATTEST_ABSENT"
    if isinstance(attest, (bytes, bytearray)):
        try:
            attest = json.loads(bytes(attest))
        except json.JSONDecodeError:
            return "FEE_ATTEST_INVALID"
    if not isinstance(attest, dict):
        return "FEE_ATTEST_INVALID"
    quoted = attest.get("fee_source_sha256")
    if not isinstance(quoted, str) or quoted != fee_sha:
        return "FEE_ATTEST_SHA_MISMATCH"
    if attest.get("verdict") != "ATTEST_PASS":
        return "FEE_ATTEST_NOT_PASS"
    return None


def _blocked(reason, blocked_series=None, fee_source=None, fee_source_sha256=None, **extra):
    obj = {
        "status": "BLOCKED_FEE_UNVERIFIED",
        "signals": None,
        "reason": reason,
        "fee_block_reason": reason,
        "blocked_series": list(blocked_series or []),
        "fee_source": fee_source,
        "fee_source_sha256": fee_source_sha256,
    }
    for key, val in extra.items():
        obj[key] = val
    return obj


def _file_identity(fee_source_bytes):
    """Identity carried on a blocked gate once bytes were supplied."""
    if not isinstance(fee_source_bytes, (bytes, bytearray)):
        return None, None
    digest = sha256_bytes(bytes(fee_source_bytes))
    try:
        doc = json.loads(bytes(fee_source_bytes))
    except (json.JSONDecodeError, UnicodeDecodeError, TypeError):
        return None, digest
    if isinstance(doc, dict) and isinstance(doc.get("manifest_id"), str):
        return doc["manifest_id"], digest
    return None, digest


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
            "fee_only_ceil": quoted["FEE_ONLY_CEIL"],
            "direct": quoted["sensitivity_direct_member"],
            "expected_net": expected_net,
            "qty": row.get(qty_key),
        })
    best = max(choices, key=lambda item: (item["expected_net"], item["side"] == "yes"))
    if not (best["expected_net"] > RESERVE + SELECT_EPS):
        return None
    best["depth_ok"] = _qty_ok(best["qty"])
    return best


def _signal_from(row, series, entry, best, *, manifest_id, digest, formula_id=None):
    signal = {
        "race_id": row["race_id"],
        "side": "D_YES" if best["side"] == "yes" else "D_NO",
        "price": float(best["price"]),
        "fee": float(best["headline"]),
        "fee_decimal": str(best["headline"]),
        "fee_rounding": "NON_DIRECT_CEIL_CENT",
        "contracts": 1,
        "series": series,
        "fee_type": entry.fee_type,
        "fee_multiplier": entry.fee_multiplier_str,
        "fee_source": manifest_id,
        "fee_source_sha256": digest,
        "visible_qty": best["qty"],
        "expected_net_gate": float(best["expected_net"]),
    }
    if formula_id is not None:
        signal["fee_formula_id"] = formula_id
    else:
        signal["FEE_ONLY_CEIL"] = str(best["fee_only_ceil"])
        signal["fee_sensitivity_direct_member"] = str(best["direct"])
    return signal


def _depth_item(row, best):
    return {
        "race_id": row["race_id"],
        "side": "D_YES" if best["side"] == "yes" else "D_NO",
        "price": float(best["price"]),
        "visible_qty": best["qty"],
    }


def gate(
    rows,
    fee_source_bytes=None,
    *,
    fee_attest=None,
    expected_sha256=FEE_SOURCE_SHA256,
    expected_id=FEE_SOURCE_ID,
    expected_accept=CONDUCTOR_ACCEPT_SHA256,
):
    """Apply the frozen gate. Expectation overrides are for tests. The CLI does not pass them."""
    _refuse_outcomes(rows)
    if fee_source_bytes is None:
        return _blocked("FEE_SOURCE_ABSENT")
    file_id, file_sha = _file_identity(fee_source_bytes)
    try:
        loaded = load_fee_source(
            fee_source_bytes,
            expected_sha256=expected_sha256,
            expected_id=expected_id,
            expected_accept=expected_accept,
        )
    except FeeBlocked as exc:
        return _blocked(exc.reason, exc.blocked_series, file_id, file_sha)
    attest_reason = fee_attest_reason(loaded.sha256, fee_attest)
    if attest_reason is not None:
        return _blocked(attest_reason, fee_source=loaded.manifest_id, fee_source_sha256=loaded.sha256)

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
        return _blocked(first_reason, blocked, loaded.manifest_id, loaded.sha256)

    signals = []
    depth_rejected = []
    for row in rows:
        if not isinstance(row, dict) or not _scorable(row):
            continue
        series = _series_of(row)
        best = _select(row, entries[series])
        if best is None:
            continue
        if not best["depth_ok"]:
            depth_rejected.append(_depth_item(row, best))
            continue
        signals.append(_signal_from(
            row, series, entries[series], best,
            manifest_id=loaded.manifest_id, digest=loaded.sha256,
        ))
    return {
        "status": "OK",
        "n_selected": len(signals),
        "signals": signals,
        "fee_source": loaded.manifest_id,
        "fee_source_sha256": loaded.sha256,
        "fee_source_status": "ADOPTED",
        "fee_attest_verdict": "ATTEST_PASS",
        "fee_attest_fee_source_sha256": loaded.sha256,
        "conductor_accept_sha256": loaded.conductor_accept_sha256,
        "series_used": [{"series": series, "series_status": "PINNED"} for series in used],
        "depth_rejected": depth_rejected,
        "gate_sha256": module_sha256(),
    }


def _series_used(rows):
    used = []
    seen = set()
    for row in rows:
        if not isinstance(row, dict) or not _scorable(row):
            continue
        series = _series_of(row)
        if series not in seen:
            seen.add(series)
            used.append(series)
    return used


def gate_v2(
    rows,
    *,
    fee_source_path,
    fee_source_id,
    fee_source_sha256,
    packet_index_path,
    fee_accept_path,
    side="BUY",
    taker_maker_role="TAKER",
    member_class_assumption="NON_DIRECT",
    fill_model="SINGLE_FILL",
):
    """Headline gate. Admission is index-only. Sensitivity rows are not emitted."""
    _refuse_outcomes(rows)
    used = _series_used(rows)
    admission = admit_fee_source_v2(
        fee_source_path=fee_source_path,
        fee_source_id=fee_source_id,
        fee_source_sha256=fee_source_sha256,
        packet_index_path=packet_index_path,
        fee_accept_path=fee_accept_path,
        series_used=used,
        side=side,
        taker_maker_role=taker_maker_role,
        member_class_assumption=member_class_assumption,
        fill_model=fill_model,
    )
    base = admission.public_dict()
    if not admission.admitted:
        blocked = _blocked(
            admission.fee_block_reason,
            admission.blocked_series,
            admission.fee_source,
            admission.fee_source_sha256,
        )
        blocked.update(base)
        blocked["status"] = "BLOCKED_FEE_UNVERIFIED"
        blocked["signals"] = None
        blocked["depth_rejected"] = None
        return blocked

    entries = {}
    for series in used:
        entries[series] = pinned_entry_v2(admission, series)
    signals = []
    depth_rejected = []
    for row in rows:
        if not isinstance(row, dict) or not _scorable(row):
            continue
        series = _series_of(row)
        best = _select(row, entries[series])
        if best is None:
            continue
        if not best["depth_ok"]:
            depth_rejected.append(_depth_item(row, best))
            continue
        signals.append(_signal_from(
            row,
            series,
            entries[series],
            best,
            manifest_id=admission.fee_source,
            digest=admission.fee_source_sha256,
            formula_id=admission.fee_formula_id,
        ))
    out = {
        "status": "OK",
        "n_selected": len(signals),
        "signals": signals,
        "depth_rejected": depth_rejected,
        "gate_sha256": module_sha256(),
    }
    out.update(base)
    return out


def main(argv):
    parser = argparse.ArgumentParser(description="outcome-free entry gate")
    parser.add_argument("rows")
    parser.add_argument("--fee-source", default=None)
    parser.add_argument("--fee-source-id", default=None)
    parser.add_argument("--fee-source-sha256", default=None)
    parser.add_argument("--packet-index", default=None)
    parser.add_argument("--fee-accept", default=None)
    args = parser.parse_args(argv)
    try:
        rows = _rows_of(json.loads(Path(args.rows).read_text()))
        obj = gate_v2(
            rows,
            fee_source_path=args.fee_source,
            fee_source_id=args.fee_source_id,
            fee_source_sha256=args.fee_source_sha256,
            packet_index_path=args.packet_index,
            fee_accept_path=args.fee_accept,
        )
    except (OutcomePresent, ValueError, json.JSONDecodeError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    json.dump(obj, sys.stdout, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
