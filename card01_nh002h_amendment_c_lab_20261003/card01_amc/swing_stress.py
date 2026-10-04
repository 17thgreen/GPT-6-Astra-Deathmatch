"""AF-7 outcome-free correlated-swing stress.

Does not call the pinned stress() helper, which looks up scored rows that
already have y. The formula is the same: q = sig(logit(arm_p(row, 0.5)) + s).
Fragility is read from the s = ±0.5 rows only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
import sys
from pathlib import Path

from card01_amc.pinload import PIN_SHA256, load_national_miss, sha256_bytes

# Refusal list. The EV formula does not subscript these names.
FORBIDDEN_OUTCOME_KEYS = ("y", "result", "settlement", "outcome", "settled")


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


def assert_outcome_free(rows):
    for row in rows:
        if not isinstance(row, dict):
            continue
        for key in FORBIDDEN_OUTCOME_KEYS:
            if key in row and row[key] is not None:
                raise OutcomePresent(key)


def _fee_net_allowed(gate, signals) -> bool:
    if gate.get("status") != "OK":
        return False
    if not gate.get("manifest_id") or gate.get("manifest_status") != "ADOPTED":
        return False
    adopted = gate.get("adopted_entry_ids")
    if not isinstance(adopted, list) or not adopted:
        return False
    adopted_set = set(adopted)
    if not signals:
        return False
    for signal in signals:
        fee = signal.get("fee")
        if isinstance(fee, bool) or not isinstance(fee, (int, float)):
            return False
        source = signal.get("fee_source")
        if not isinstance(source, str) or source not in adopted_set:
            return False
    return True


def _ev(pinned, row, signal, swing):
    q = pinned.sig(pinned.logit(pinned.arm_p(row, pinned.HEADLINE_W)) + swing)
    if signal["side"] == "D_YES":
        return q - signal["price"]
    return (1.0 - q) - signal["price"]


def _grid(pinned):
    grid = [(-1.0, True)]
    for swing in pinned.SWING_GRID:
        grid.append((float(swing), False))
    grid.append((1.0, True))
    return grid


def _fragility(stress_rows):
    fired = False
    for row in stress_rows:
        if row["informational"]:
            continue
        if row["swing_logit"] not in (-0.5, 0.5):
            continue
        if row["expected_gross"] <= 0 or row["share_sign_flips_vs_s0"] >= 0.5:
            fired = True
    return "FRAGILE_NATIONAL_SWING" if fired else "NOT_FRAGILE_AT_PM0.5"


def _envelope(status, fragility, rows, rows_sha, gate_sha, extra=None):
    obj = {
        "stress_status": status,
        "fragility": fragility,
        "gating": False,
        "rows": rows,
        "rows_sha256": rows_sha,
        "gate_sha256": gate_sha,
        "swing_stress_sha256": module_sha256(),
        "pinned_script_sha256": PIN_SHA256,
        "python_version": sys.version,
        "platform": platform.platform(),
    }
    if extra:
        for key, val in extra.items():
            obj[key] = val
    raw = json.dumps(obj, indent=1).encode()
    obj["output_sha256"] = hashlib.sha256(raw).hexdigest()
    return obj


def _defect(rows_sha, gate_sha, reason):
    return _envelope(
        "REPORTING_DEFECT",
        "FRAGILE_NOT_CLEARED_REPORTING_DEFECT",
        None,
        rows_sha,
        gate_sha,
        {"reason": reason},
    )


def evaluate(rows, gate, rows_sha256, gate_sha256, gate_sha_expected=None):
    """Outcome-free stress. Caller has already rejected non-null outcome fields."""
    assert_outcome_free(rows)
    if gate_sha_expected is not None and gate_sha256 != gate_sha_expected:
        return _defect(rows_sha256, gate_sha256, "GATE_SHA_MISMATCH")
    if not isinstance(gate, dict):
        return _defect(rows_sha256, gate_sha256, "GATE_MISSING")
    status = gate.get("status")
    if status == "BLOCKED_FEE_UNVERIFIED":
        extra = {}
        if gate.get("reason") is not None:
            extra["reason"] = gate["reason"]
        if gate.get("manifest_id") is not None:
            extra["manifest_id"] = gate["manifest_id"]
        return _envelope(
            "BLOCKED_FEE_UNVERIFIED",
            "NOT_EVALUATED_FEE_BLOCKED",
            None,
            rows_sha256,
            gate_sha256,
            extra or None,
        )
    if status != "OK":
        return _defect(rows_sha256, gate_sha256, "GATE_STATUS_UNKNOWN")

    n_selected = gate.get("n_selected")
    signals = gate.get("signals")
    if not signals:
        if n_selected in (0, None):
            return _envelope(
                "NO_SIGNALS_SELECTED",
                None,
                None,
                rows_sha256,
                gate_sha256,
                {"gate_n_selected": 0},
            )
        return _defect(rows_sha256, gate_sha256, "SIGNALS_MISSING")
    if isinstance(n_selected, int) and n_selected != len(signals):
        return _defect(rows_sha256, gate_sha256, "SIGNAL_COUNT_MISMATCH")

    byid = {}
    for row in rows:
        if isinstance(row, dict) and row.get("race_id") is not None:
            byid[row["race_id"]] = row
    for signal in signals:
        row = byid.get(signal.get("race_id"))
        if row is None or row.get("p_model") is None or row.get("p_market") is None:
            return _defect(rows_sha256, gate_sha256, "SIGNAL_ROW_UNUSABLE")

    pinned = load_national_miss()
    base = [_ev(pinned, byid[s["race_id"]], s, 0.0) for s in signals]
    fees = [s.get("fee") for s in signals]
    grid = _grid(pinned)
    fee_ok = _fee_net_allowed(gate, signals)
    # A gate file cannot self-certify a numeric net. The caller must pass the
    # gate file's sha, and it must match the bytes that were hashed.
    net_block_reason = None
    if gate_sha_expected is None:
        net_block_reason = "GATE_SHA_NOT_SUPPLIED"
    out_rows = []
    for swing, informational in grid:
        evs = [_ev(pinned, byid[s["race_id"]], s, swing) for s in signals]
        flips = sum(1 for a, b in zip(base, evs) if (a > 0) != (b > 0))
        gross = sum(evs)
        if net_block_reason is not None or not fee_ok:
            net = "BLOCKED_FEE_UNVERIFIED"
        else:
            net = gross - sum(fees)
        row = {
            "swing_logit": swing,
            "expected_gross": gross,
            "expected_net": net,
            "n_sign_flips_vs_s0": flips,
            "share_sign_flips_vs_s0": flips / len(signals),
            "informational": informational,
        }
        if net_block_reason is not None:
            row["net_block_reason"] = net_block_reason
        out_rows.append(row)
    extra = {"n_signals": len(signals)}
    if net_block_reason is not None:
        extra["net_block_reason"] = net_block_reason
    if gate.get("manifest_id") is not None:
        extra["manifest_id"] = gate["manifest_id"]
    return _envelope("OK", _fragility(out_rows), out_rows, rows_sha256, gate_sha256, extra)


def main(argv):
    parser = argparse.ArgumentParser(description="outcome-free swing stress")
    parser.add_argument("--rows", required=True)
    parser.add_argument("--gate", default=None)
    parser.add_argument("--gate-sha256", default=None, dest="gate_sha256")
    args = parser.parse_args(argv)
    try:
        row_bytes = Path(args.rows).read_bytes()
        rows = _rows_of(json.loads(row_bytes))
        assert_outcome_free(rows)
    except OutcomePresent:
        return 2
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 2

    gate = None
    gate_sha = None
    if args.gate:
        gate_path = Path(args.gate)
        if gate_path.is_file():
            gate_bytes = gate_path.read_bytes()
            gate_sha = hashlib.sha256(gate_bytes).hexdigest()
            try:
                gate = json.loads(gate_bytes)
            except json.JSONDecodeError:
                gate = {"status": "UNPARSEABLE"}
        else:
            gate = None
    obj = evaluate(rows, gate, hashlib.sha256(row_bytes).hexdigest(), gate_sha, args.gate_sha256)
    json.dump(obj, sys.stdout, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
