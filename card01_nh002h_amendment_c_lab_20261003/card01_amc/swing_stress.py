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

from card01_amc.entry_gate import OutcomePresent as GateOutcomePresent
from card01_amc.entry_gate import gate_v2
from card01_amc.fee_admission import (
    REFUSED_FEE_SOURCES,
    SENSITIVITY_ROWS_STATUS,
    admit_fee_source_v2,
    pinned_entry_v2,
)
from card01_amc.fee_source import FeeBlocked, pinned_taker_fee
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


_UNSET = object()

# Consumer-side checks that still emit the swing grid, with the net column blocked.
_ROW_BLOCK_REASONS = frozenset({
    "GATE_SHA_NOT_SUPPLIED",
    "FEE_SOURCE_NOT_SUPPLIED",
    "FEE_SOURCE_PAIR_MISMATCH",
    "FEE_RECOMPUTE_MISMATCH",
})


def _refused(gate, expected_id, expected_sha) -> bool:
    values = []
    if isinstance(gate, dict):
        values.append(gate.get("fee_source"))
        values.append(gate.get("fee_source_sha256"))
    if expected_id is not _UNSET:
        values.append(expected_id)
    if expected_sha is not _UNSET:
        values.append(expected_sha)
    return any(item in REFUSED_FEE_SOURCES for item in values)


def _fee_identity(gate):
    extra = {}
    if not isinstance(gate, dict):
        return extra
    if "fee_source" in gate:
        extra["fee_source"] = gate.get("fee_source")
    if "fee_source_sha256" in gate:
        extra["fee_source_sha256"] = gate.get("fee_source_sha256")
    return extra


def _pair_reason(gate, expected_sha, expected_accept, expected_formula):
    if (
        expected_sha is _UNSET
        or expected_accept is _UNSET
        or expected_formula is _UNSET
    ):
        return "FEE_SOURCE_PAIR_MISSING"
    if (
        gate.get("fee_source_sha256") != expected_sha
        or gate.get("fee_source_accept_sha256") != expected_accept
        or gate.get("fee_formula_id") != expected_formula
    ):
        return "FEE_SOURCE_PAIR_MISMATCH"
    return None


def _bare_rows(rows):
    bare = []
    for row in rows:
        if isinstance(row, dict):
            bare.append({
                key: value
                for key, value in row.items()
                if key not in FORBIDDEN_OUTCOME_KEYS
            })
    return bare


def _again(rows, gate, paths, expected_sha):
    """Re-run gate_v2 on the outcome-stripped rows and the same fee files."""
    fee_source_path, packet_index_path, fee_accept_path = paths
    try:
        return gate_v2(
            _bare_rows(rows),
            fee_source_path=fee_source_path,
            fee_source_id=gate.get("fee_source"),
            fee_source_sha256=expected_sha,
            packet_index_path=packet_index_path,
            fee_accept_path=fee_accept_path,
        )
    except (FeeBlocked, GateOutcomePresent, ValueError, TypeError):
        return None


def _same_signals(gate, again):
    return (
        isinstance(again, dict)
        and again.get("status") == "OK"
        and again.get("signals") == gate.get("signals")
    )


def _v2_recompute(gate, signals, gate_sha_expected, paths, expected_sha, rows):
    """Return (block_reason, headlines). Headlines are recomputed Decimals."""
    fee_source_path, packet_index_path, fee_accept_path = paths
    if gate_sha_expected is None:
        return "GATE_SHA_NOT_SUPPLIED", None
    if fee_source_path is None or packet_index_path is None or fee_accept_path is None:
        return "FEE_SOURCE_NOT_SUPPLIED", None
    admission = admit_fee_source_v2(
        fee_source_path=fee_source_path,
        fee_source_id=gate.get("fee_source"),
        fee_source_sha256=expected_sha,
        packet_index_path=packet_index_path,
        fee_accept_path=fee_accept_path,
        series_used=[signal.get("series") for signal in signals],
    )
    if not admission.admitted:
        return admission.fee_block_reason or "FEE_RECOMPUTE_MISMATCH", None
    if (
        admission.fee_source_sha256 != gate.get("fee_source_sha256")
        or admission.fee_source_accept_sha256 != gate.get("fee_source_accept_sha256")
        or admission.fee_formula_id != gate.get("fee_formula_id")
    ):
        return "FEE_SOURCE_PAIR_MISMATCH", None
    again = _again(rows, gate, paths, expected_sha)
    if not _same_signals(gate, again):
        return "GATE_NOT_REPRODUCED", None
    headlines = []
    for signal in signals:
        if (
            signal.get("fee_source") != admission.fee_source
            or signal.get("fee_source_sha256") != admission.fee_source_sha256
            or signal.get("fee_formula_id") != admission.fee_formula_id
        ):
            return "FEE_SOURCE_PAIR_MISMATCH", None
        try:
            entry = pinned_entry_v2(admission, signal.get("series"))
            quoted = pinned_taker_fee(entry, signal.get("price"))
            declared = Decimal(signal.get("fee_decimal"))
        except (FeeBlocked, TypeError, InvalidOperation, ArithmeticError, ValueError):
            return "FEE_RECOMPUTE_MISMATCH", None
        if quoted["headline"] != declared:
            return "FEE_RECOMPUTE_MISMATCH", None
        headlines.append(quoted["headline"])
    return None, headlines


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
    if reason == "GATE_NOT_REPRODUCED":
        extra["reporting_defects"] = [{
            "kind": "GATE_NOT_REPRODUCED",
            "status": "REPORTING_DEFECT",
        }]
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
    """Outcome-free stress.

    The only fee input is a v2 admission state. Numbers are computed only when
    fee_admission is ADMITTED_INDEX_ONLY, the gate's fee-source sha, accept
    sha, and fee_formula_id equal the pair the caller passed, and gate_v2
    reproduces the gate's signals from these rows and fee files. A mismatch
    is GATE_NOT_REPRODUCED with no fee or net numbers. fee_source_bytes is
    ignored.
    """
    del fee_source_bytes
    assert_outcome_free(rows)
    if gate_sha_expected is not None and gate_sha256 != gate_sha_expected:
        return _defect(rows_sha256, gate_sha256, "GATE_SHA_MISMATCH")
    if not isinstance(gate, dict):
        return _fee_block(rows_sha256, gate_sha256, "GATE_MISSING")
    if _refused(gate, fee_source_expected_id, fee_source_expected_sha256):
        return _fee_block(
            rows_sha256,
            gate_sha256,
            "FEE_SOURCE_NOT_ADMITTED_V1_ATTEST_FAIL",
            gate,
        )
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
    pair_reason = _pair_reason(
        gate,
        fee_source_expected_sha256,
        fee_source_expected_accept,
        fee_source_expected_formula,
    )
    if pair_reason is not None:
        return _fee_block(rows_sha256, gate_sha256, pair_reason, gate)

    n_selected = gate.get("n_selected")
    signals = gate.get("signals")
    paths = (fee_source_path, packet_index_path, fee_accept_path)
    if not signals:
        if n_selected in (0, None):
            if all(path is not None for path in paths):
                reason, _headlines = _v2_recompute(
                    gate,
                    [],
                    gate_sha_expected,
                    paths,
                    fee_source_expected_sha256,
                    rows,
                )
                if reason is not None:
                    return _fee_block(rows_sha256, gate_sha256, reason, gate)
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
    # A gate file cannot self-certify a numeric net. The headline is recomputed.
    net_block_reason, headlines = _v2_recompute(
        gate,
        signals,
        gate_sha_expected,
        paths,
        fee_source_expected_sha256,
        rows,
    )
    if net_block_reason is not None and net_block_reason not in _ROW_BLOCK_REASONS:
        return _fee_block(rows_sha256, gate_sha256, net_block_reason, gate)
    out_rows = []
    for swing, informational in grid:
        evs = [_ev(pinned, byid[s["race_id"]], s, swing) for s in signals]
        flips = sum(1 for a, b in zip(base, evs) if (a > 0) != (b > 0))
        gross = sum(evs)
        if net_block_reason is not None:
            net = "BLOCKED_FEE_UNVERIFIED"
        else:
            net = gross - sum(float(headline) for headline in headlines)
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
    extra = {"n_signals": len(signals), "sensitivity_rows_status": SENSITIVITY_ROWS_STATUS}
    if net_block_reason is not None:
        extra["net_block_reason"] = net_block_reason
    extra.update(_fee_identity(gate))
    return _envelope("OK", _fragility(out_rows), out_rows, rows_sha256, gate_sha256, extra)


def main(argv):
    parser = argparse.ArgumentParser(description="outcome-free swing stress")
    parser.add_argument("--rows", required=True)
    parser.add_argument("--gate", default=None)
    parser.add_argument("--gate-sha256", default=None, dest="gate_sha256")
    parser.add_argument("--fee-source", default=None)
    parser.add_argument("--fee-source-id", default=None)
    parser.add_argument("--fee-source-sha256", default=None)
    parser.add_argument("--fee-formula-id", default=None)
    parser.add_argument("--packet-index", default=None)
    parser.add_argument("--fee-accept", default=None)
    parser.add_argument("--fee-accept-sha256", default=None)
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
    obj = evaluate(
        rows,
        gate,
        hashlib.sha256(row_bytes).hexdigest(),
        gate_sha,
        args.gate_sha256,
        fee_source_path=args.fee_source,
        packet_index_path=args.packet_index,
        fee_accept_path=args.fee_accept,
        fee_source_expected_id=args.fee_source_id if args.fee_source_id is not None else _UNSET,
        fee_source_expected_sha256=(
            args.fee_source_sha256 if args.fee_source_sha256 is not None else _UNSET
        ),
        fee_source_expected_accept=(
            args.fee_accept_sha256 if args.fee_accept_sha256 is not None else _UNSET
        ),
        fee_source_expected_formula=(
            args.fee_formula_id if args.fee_formula_id is not None else _UNSET
        ),
    )
    json.dump(obj, sys.stdout, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
