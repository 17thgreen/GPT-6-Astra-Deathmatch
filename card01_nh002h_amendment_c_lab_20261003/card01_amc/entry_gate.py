"""AF-8 entry gate.

gate() cannot mint an admitting state. gate_v2 computes a headline only
after index-only admission. One unpinned series blocks the card.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from decimal import Decimal
from pathlib import Path

from card01_amc.fee_admission import REFUSED_FEE_SOURCES, admit_fee_source_v2, pinned_entry_v2
from card01_amc.fee_source import FeeBlocked, pinned_taker_fee
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
    expected_sha256=None,
    expected_id=None,
    expected_accept=None,
):
    """v1 entry point. It cannot mint an admitting state.

    Missing bytes are FEE_SOURCE_ABSENT. Any supplied file, including a
    deny-listed v1 pair, is BLOCKED_FEE_UNVERIFIED with no signals and no
    sensitivity fields. fee_attest and the expectation arguments are ignored.
    """
    del fee_attest, expected_accept
    _refuse_outcomes(rows)
    if fee_source_bytes is None:
        return _blocked("FEE_SOURCE_ABSENT")
    file_id, file_sha = _file_identity(fee_source_bytes)
    if (
        file_sha in REFUSED_FEE_SOURCES
        or file_id in REFUSED_FEE_SOURCES
        or expected_sha256 in REFUSED_FEE_SOURCES
        or expected_id in REFUSED_FEE_SOURCES
    ):
        return _blocked(
            "FEE_SOURCE_NOT_ADMITTED_V1_ATTEST_FAIL",
            fee_source=file_id,
            fee_source_sha256=file_sha,
        )
    return _blocked(
        "FEE_SOURCE_NOT_ADMITTED_V1_ATTEST_FAIL",
        fee_source=file_id,
        fee_source_sha256=file_sha,
    )


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
    if fee_source_sha256 in REFUSED_FEE_SOURCES or fee_source_id in REFUSED_FEE_SOURCES:
        return _blocked(
            "FEE_SOURCE_NOT_ADMITTED_V1_ATTEST_FAIL",
            fee_source=fee_source_id if isinstance(fee_source_id, str) else None,
            fee_source_sha256=fee_source_sha256 if isinstance(fee_source_sha256, str) else None,
        )
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
    try:
        for series in used:
            entries[series] = pinned_entry_v2(admission, series)
    except FeeBlocked as exc:
        blocked = _blocked(
            exc.reason,
            exc.blocked_series,
            admission.fee_source,
            admission.fee_source_sha256,
        )
        blocked.update(base)
        blocked["status"] = "BLOCKED_FEE_UNVERIFIED"
        blocked["reason"] = exc.reason
        blocked["fee_block_reason"] = exc.reason
        blocked["signals"] = None
        blocked["depth_rejected"] = None
        return blocked
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
