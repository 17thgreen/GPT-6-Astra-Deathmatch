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
from decimal import Decimal, InvalidOperation
from pathlib import Path

from card01_amc.fee_admission import (
    SENSITIVITY_ROWS_STATUS,
    admit_fee_source_v2,
    pinned_entry_v2,
)
from card01_amc.fee_source import (
    CONDUCTOR_ACCEPT_SHA256,
    FEE_SOURCE_ID,
    FEE_SOURCE_SHA256,
    FeeBlocked,
    load_fee_source,
    pinned_entry,
    pinned_taker_fee,
)
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


def _pair_matches(obj, loaded) -> bool:
    return obj.get("fee_source") == loaded.manifest_id and obj.get("fee_source_sha256") == loaded.sha256


_UNSET = object()

# Consumer-side checks that still emit the swing grid, with the net column blocked.
_ROW_BLOCK_REASONS = frozenset({
    "GATE_SHA_NOT_SUPPLIED",
    "FEE_SOURCE_NOT_SUPPLIED",
    "FEE_SOURCE_PAIR_MISMATCH",
    "FEE_RECOMPUTE_MISMATCH",
})


def _is_v2_gate(gate) -> bool:
    return isinstance(gate, dict) and (
        "fee_admission" in gate or "adoption_mode" in gate or "fee_formula_id" in gate
    )


def _attest_reason(gate):
    """Distinct recorded-attestation failures. Absent, not-pass, and sha mismatch."""
    verdict = gate.get("fee_attest_verdict")
    recorded = gate.get("fee_attest_fee_source_sha256")
    if verdict is None and recorded is None:
        return "FEE_ATTEST_ABSENT"
    if recorded != gate.get("fee_source_sha256"):
        return "FEE_ATTEST_SHA_MISMATCH"
    if verdict != "ATTEST_PASS":
        return "FEE_ATTEST_NOT_PASS"
    return None


def _fee_identity(gate):
    extra = {}
    if not isinstance(gate, dict):
        return extra
    if "fee_source" in gate:
        extra["fee_source"] = gate.get("fee_source")
    if "fee_source_sha256" in gate:
        extra["fee_source_sha256"] = gate.get("fee_source_sha256")
    return extra


def _net_decision(gate, signals, gate_sha_expected, fee_source_bytes, fee_kwargs):
    """None when headline nets may be numeric. Otherwise a net_block_reason."""
    if gate_sha_expected is None:
        return "GATE_SHA_NOT_SUPPLIED"
    if fee_source_bytes is None:
        return "FEE_SOURCE_NOT_SUPPLIED"
    try:
        loaded = load_fee_source(fee_source_bytes, **fee_kwargs)
    except FeeBlocked as exc:
        return "FEE_SOURCE_INVALID:" + exc.reason
    if not _pair_matches(gate, loaded):
        return "FEE_SOURCE_PAIR_MISMATCH"
    for signal in signals:
        if not _pair_matches(signal, loaded):
            return "FEE_SOURCE_PAIR_MISMATCH"
        try:
            entry = pinned_entry(loaded, signal.get("series"))
            quoted = pinned_taker_fee(entry, signal.get("price"))
            declared = Decimal(signal.get("fee_decimal"))
        except (FeeBlocked, TypeError, InvalidOperation, ArithmeticError, ValueError):
            return "FEE_RECOMPUTE_MISMATCH"
        if quoted["headline"] != declared:
            return "FEE_RECOMPUTE_MISMATCH"
    return None


def _v2_pair_ok(gate, fee_id, fee_sha, formula):
    if fee_id is _UNSET or fee_sha is _UNSET or formula is _UNSET:
        return False
    return (
        gate.get("fee_source") == fee_id
        and gate.get("fee_source_sha256") == fee_sha
        and gate.get("fee_formula_id") == formula
    )


def _v2_recompute(gate, signals, gate_sha_expected, paths, expected):
    """None when every headline fee recomputes. Otherwise a block reason."""
    fee_source_path, packet_index_path, fee_accept_path = paths
    if gate_sha_expected is None:
        return "GATE_SHA_NOT_SUPPLIED"
    if fee_source_path is None or packet_index_path is None or fee_accept_path is None:
        return "FEE_SOURCE_NOT_SUPPLIED"
    admission = admit_fee_source_v2(
        fee_source_path=fee_source_path,
        fee_source_id=expected[0],
        fee_source_sha256=expected[1],
        packet_index_path=packet_index_path,
        fee_accept_path=fee_accept_path,
        series_used=[signal.get("series") for signal in signals],
    )
    if not admission.admitted:
        return admission.fee_block_reason or "FEE_RECOMPUTE_MISMATCH"
    if (
        admission.fee_source != gate.get("fee_source")
        or admission.fee_source_sha256 != gate.get("fee_source_sha256")
        or admission.fee_formula_id != gate.get("fee_formula_id")
    ):
        return "FEE_SOURCE_PAIR_MISMATCH"
    for signal in signals:
        if (
            signal.get("fee_source") != admission.fee_source
            or signal.get("fee_source_sha256") != admission.fee_source_sha256
        ):
            return "FEE_SOURCE_PAIR_MISMATCH"
        try:
            entry = pinned_entry_v2(admission, signal.get("series"))
            quoted = pinned_taker_fee(entry, signal.get("price"))
            declared = Decimal(signal.get("fee_decimal"))
        except (FeeBlocked, TypeError, InvalidOperation, ArithmeticError, ValueError):
            return "FEE_RECOMPUTE_MISMATCH"
        if quoted["headline"] != declared:
            return "FEE_RECOMPUTE_MISMATCH"
    return None


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


def _fee_block(rows_sha, gate_sha, reason, gate=None):
    extra = {
        "reason": reason,
        "fee_block_reason": reason,
        "net_block_reason": reason,
    }
    extra.update(_fee_identity(gate))
    return _envelope(
        "BLOCKED_FEE_UNVERIFIED",
        "NOT_EVALUATED_FEE_BLOCKED",
        None,
        rows_sha,
        gate_sha,
        extra,
    )


def evaluate(
    rows,
    gate,
    rows_sha256,
    gate_sha256,
    gate_sha_expected=None,
    fee_source_bytes=None,
    *,
    fee_source_expected_sha256=_UNSET,
    fee_source_expected_id=_UNSET,
    fee_source_expected_accept=_UNSET,
    fee_source_expected_formula=_UNSET,
    fee_source_path=None,
    packet_index_path=None,
    fee_accept_path=None,
):
    """Outcome-free stress. Caller has already rejected non-null outcome fields.

    A gate is v2 when it carries fee_admission, adoption_mode, or fee_formula_id,
    or when the caller passed v2 paths. Only ADMITTED_INDEX_ONLY computes on that
    path, and only against the caller-supplied pair. A legacy gate stays on the
    v1 ATTEST_PASS recompute path.
    """
    assert_outcome_free(rows)
    if gate_sha_expected is not None and gate_sha256 != gate_sha_expected:
        return _defect(rows_sha256, gate_sha256, "GATE_SHA_MISMATCH")
    v2_paths = (
        fee_source_path is not None
        or packet_index_path is not None
        or fee_accept_path is not None
    )
    if not isinstance(gate, dict):
        if v2_paths:
            return _fee_block(rows_sha256, gate_sha256, "GATE_MISSING")
        return _defect(rows_sha256, gate_sha256, "GATE_MISSING")
    status = gate.get("status")
    if status == "BLOCKED_FEE_UNVERIFIED":
        extra = {}
        reason = gate.get("fee_block_reason")
        if reason is None:
            reason = gate.get("reason")
        if reason is not None:
            extra["reason"] = gate.get("reason") if gate.get("reason") is not None else reason
            extra["fee_block_reason"] = reason
            extra["net_block_reason"] = reason
        if gate.get("manifest_id") is not None:
            extra["manifest_id"] = gate["manifest_id"]
        extra.update(_fee_identity(gate))
        return _envelope(
            "BLOCKED_FEE_UNVERIFIED",
            "NOT_EVALUATED_FEE_BLOCKED",
            None,
            rows_sha256,
            gate_sha256,
            extra or None,
        )
    v2 = _is_v2_gate(gate) or v2_paths
    if not v2 and status != "OK":
        return _defect(rows_sha256, gate_sha256, "GATE_STATUS_UNKNOWN")
    if v2:
        if status != "OK":
            return _fee_block(
                rows_sha256,
                gate_sha256,
                gate.get("fee_block_reason") or "GATE_STATUS_NOT_OK",
                gate,
            )
        if "fee_admission" not in gate:
            return _fee_block(rows_sha256, gate_sha256, "FEE_ADMISSION_MISSING", gate)
        if gate.get("fee_admission") != "ADMITTED_INDEX_ONLY":
            return _fee_block(
                rows_sha256,
                gate_sha256,
                gate.get("fee_block_reason") or "FEE_ADMISSION_NOT_ADMITTED",
                gate,
            )
        if not _v2_pair_ok(
            gate,
            fee_source_expected_id,
            fee_source_expected_sha256,
            fee_source_expected_formula,
        ):
            return _fee_block(rows_sha256, gate_sha256, "FEE_SOURCE_PAIR_MISMATCH", gate)
    else:
        # Fee attestation blocks before a zero-signal note, so an unattested
        # empty gate emits no numbers.
        attest_reason = _attest_reason(gate)
        if attest_reason is not None:
            return _fee_block(rows_sha256, gate_sha256, attest_reason, gate)

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
    grid = _grid(pinned)
    # A gate file cannot self-certify a numeric net. The caller must pass the
    # gate file's sha, and the headline fee must recompute from the fee source.
    if v2:
        net_block_reason = _v2_recompute(
            gate,
            signals,
            gate_sha_expected,
            (fee_source_path, packet_index_path, fee_accept_path),
            (fee_source_expected_id, fee_source_expected_sha256),
        )
        if net_block_reason is not None and net_block_reason not in _ROW_BLOCK_REASONS:
            return _fee_block(rows_sha256, gate_sha256, net_block_reason, gate)
    else:
        v1_sha = FEE_SOURCE_SHA256 if fee_source_expected_sha256 is _UNSET else fee_source_expected_sha256
        v1_id = FEE_SOURCE_ID if fee_source_expected_id is _UNSET else fee_source_expected_id
        v1_accept = (
            CONDUCTOR_ACCEPT_SHA256
            if fee_source_expected_accept is _UNSET
            else fee_source_expected_accept
        )
        net_block_reason = _net_decision(
            gate,
            signals,
            gate_sha_expected,
            fee_source_bytes,
            {
                "expected_sha256": v1_sha,
                "expected_id": v1_id,
                "expected_accept": v1_accept,
            },
        )
    out_rows = []
    for swing, informational in grid:
        evs = [_ev(pinned, byid[s["race_id"]], s, swing) for s in signals]
        flips = sum(1 for a, b in zip(base, evs) if (a > 0) != (b > 0))
        gross = sum(evs)
        if net_block_reason is not None:
            net = "BLOCKED_FEE_UNVERIFIED"
        else:
            net = gross - sum(float(s["fee"]) for s in signals)
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
    if v2:
        extra["sensitivity_rows_status"] = SENSITIVITY_ROWS_STATUS
    extra.update(_fee_identity(gate))
    return _envelope("OK", _fragility(out_rows), out_rows, rows_sha256, gate_sha256, extra)


def main(argv):
    parser = argparse.ArgumentParser(description="outcome-free swing stress")
    parser.add_argument("--rows", required=True)
    parser.add_argument("--gate", default=None)
    parser.add_argument("--gate-sha256", default=None, dest="gate_sha256")
    parser.add_argument("--fee-source", default=None)
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

    fee_bytes = None
    if args.fee_source:
        fee_path = Path(args.fee_source)
        if fee_path.is_file():
            fee_bytes = fee_path.read_bytes()
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
    obj = evaluate(rows, gate, hashlib.sha256(row_bytes).hexdigest(), gate_sha, args.gate_sha256, fee_bytes)
    json.dump(obj, sys.stdout, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
