"""AF-8 entry gate with the AF-4 fee block.

The production path never prices a contract. Commit 22371178's feebook
order_fee(role, contracts, price) is not a (fee_type, fee_multiplier, price)
function, so an otherwise ADOPTED manifest still returns FEE_FORMULA_NOT_PINNED.
Tests may pass fee_fn. The command line does not.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

from card01_amc.pinload import sha256_bytes

# R1-P1 kalshi_feebook_lab_20260922 @ 22371178 has no matching function.
FEE_FORMULA_PINNED = False
FEEBOOK_COMMIT = "22371178cb2663250b4762f328069571c48cb551"

EXTRA_COST = 0.02
RESERVE = 0.03
SELECT_EPS = 1e-12
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


def _term_ok(value) -> bool:
    if isinstance(value, bool):
        return False
    if isinstance(value, (int, float)):
        return math.isfinite(float(value))
    return isinstance(value, str) and value != ""


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


def _blocked(reason):
    return {"status": "BLOCKED_FEE_UNVERIFIED", "signals": None, "reason": reason}


def admissibility_reason(rows, manifest):
    """None when every scorable row's series has an ADOPTED series-endpoint entry."""
    if not isinstance(manifest, dict):
        return "MANIFEST_ABSENT"
    if manifest.get("status") != "ADOPTED":
        return "MANIFEST_NOT_ADOPTED"
    entries = manifest.get("entries")
    if not isinstance(entries, dict):
        return "MANIFEST_ENTRIES_MISSING"
    for row in rows:
        if not isinstance(row, dict) or not _scorable(row):
            continue
        series = _series_of(row)
        entry = entries.get(series) if series else None
        if not isinstance(entry, dict):
            return "SERIES_ENTRY_MISSING"
        if entry.get("status") != "ADOPTED":
            return "SERIES_ENTRY_NOT_ADOPTED"
        if entry.get("source") != "series_endpoint":
            return "SERIES_SOURCE_NOT_ENDPOINT"
        if not _term_ok(entry.get("fee_type")) or not _term_ok(entry.get("fee_multiplier")):
            return "FEE_TERMS_MISSING"
        if not isinstance(entry.get("entry_id"), str) or not entry["entry_id"]:
            return "ENTRY_ID_MISSING"
    return None


def _qty_ok(value) -> bool:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return False
    return math.isfinite(float(value)) and float(value) >= 1


def _select(row, fee_at):
    if row.get("yes_bid") is None or row.get("yes_ask") is None:
        return None
    q = 0.5 * float(row["p_model"]) + 0.5 * float(row["p_market"])
    bid = float(row["yes_bid"])
    ask = float(row["yes_ask"])
    choices = []
    for side, prob, price, qty_key in (
        ("yes", q, ask, "yes_ask_qty"),
        ("no", 1.0 - q, 1.0 - bid, "yes_bid_qty"),
    ):
        fee = float(fee_at(price))
        expected_net = prob - (price + fee + EXTRA_COST)
        choices.append({
            "side": side,
            "price": price,
            "fee": fee,
            "expected_net": expected_net,
            "qty": row.get(qty_key),
        })
    best = max(choices, key=lambda item: (item["expected_net"], item["side"] == "yes"))
    if not (best["expected_net"] > RESERVE + SELECT_EPS):
        return None
    if not _qty_ok(best["qty"]):
        return None
    return best


def gate(rows, manifest=None, fee_fn=None):
    """Apply the frozen gate. fee_fn is test-only and is ignored on the CLI."""
    _refuse_outcomes(rows)
    reason = admissibility_reason(rows, manifest)
    if reason:
        return _blocked(reason)
    # Production has no pinned (fee_type, fee_multiplier, price) function.
    # fee_fn is a test injection and is not available on the command line.
    if fee_fn is None:
        return _blocked("FEE_FORMULA_NOT_PINNED")

    entries = manifest["entries"]
    adopted = []
    signals = []
    for row in rows:
        if not isinstance(row, dict) or not _scorable(row):
            continue
        series = _series_of(row)
        entry = entries[series]
        entry_id = entry["entry_id"]
        if entry_id not in adopted:
            adopted.append(entry_id)

        def fee_at(price, entry=entry):
            return fee_fn(entry["fee_type"], entry["fee_multiplier"], price)

        best = _select(row, fee_at)
        if best is None:
            continue
        signals.append({
            "race_id": row["race_id"],
            "side": "D_YES" if best["side"] == "yes" else "D_NO",
            "price": best["price"],
            "fee": best["fee"],
            "fee_source": entry_id,
            "visible_qty": best["qty"],
            "expected_net_gate": best["expected_net"],
        })
    return {
        "status": "OK",
        "n_selected": len(signals),
        "signals": signals,
        "manifest_id": manifest.get("manifest_id"),
        "manifest_status": manifest.get("status"),
        "adopted_entry_ids": adopted,
        "gate_sha256": module_sha256(),
    }


def main(argv):
    if len(argv) not in (1, 2):
        print("usage: python -m card01_amc.entry_gate rows.json [manifest.json]", file=sys.stderr)
        return 2
    try:
        rows = _rows_of(json.loads(Path(argv[0]).read_text()))
        manifest = json.loads(Path(argv[1]).read_text()) if len(argv) == 2 else None
        obj = gate(rows, manifest)
    except (OutcomePresent, ValueError, json.JSONDecodeError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    json.dump(obj, sys.stdout, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
