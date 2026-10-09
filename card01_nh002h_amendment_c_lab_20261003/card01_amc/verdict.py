"""Examiner-aid verdict helper.

Precedence is validity, then INCONCLUSIVE_DEGENERATE_BLOCK, then REJECT (a)
or (b), then the fee branch. Notes do not change the verdict. Realized P&L
for (c) and (d) is supplied by the caller and is not computed here. A missing
boolean stays fail-closed. Zero signals make both (c) and (d) true.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from card01_amc.fee_source import CONDUCTOR_ACCEPT_SHA256, FEE_SOURCE_ID, FEE_SOURCE_SHA256

PASS_FORECAST = "FORECAST_ONLY_FEE_BLOCKED: PASS-FORECAST"
REJECT_FORECAST = "FORECAST_ONLY_FEE_BLOCKED: REJECT"
DEGENERATE = "INCONCLUSIVE_DEGENERATE_BLOCK"
FULL = "FULL_VERDICT_REQUIRES_EXAMINER"
PASS = "PASS-FORECAST"
REJECT = "REJECT"


def _hi(score, field):
    arms = (score.get("all_admitted") or {}).get("arms") or {}
    arm = arms.get("0.5") or {}
    ci = arm.get(field)
    if not isinstance(ci, (list, tuple)) or len(ci) != 2:
        return None
    return ci[1]


def _degenerate_from(score):
    status = score.get("headline_status")
    reason = score.get("degenerate_reason")
    block = score.get("all_admitted") or {}
    n = block.get("n")
    states = block.get("states")
    if status == DEGENERATE or n == 0 or (states is not None and states < 2):
        if reason in ("N_ZERO", "FEWER_THAN_2_STATES"):
            why = reason
        elif n == 0:
            why = "N_ZERO"
        elif states is not None and states < 2:
            why = "FEWER_THAN_2_STATES"
        else:
            why = reason
        return why
    return None


def _is_v2_gate(gate) -> bool:
    return isinstance(gate, dict) and (
        "fee_admission" in gate or "adoption_mode" in gate or "fee_formula_id" in gate
    )


def _attest_reason(gate):
    verdict = gate.get("fee_attest_verdict")
    recorded = gate.get("fee_attest_fee_source_sha256")
    if verdict is None and recorded is None:
        return "FEE_ATTEST_ABSENT"
    if recorded != gate.get("fee_source_sha256"):
        return "FEE_ATTEST_SHA_MISMATCH"
    if verdict != "ATTEST_PASS":
        return "FEE_ATTEST_NOT_PASS"
    return None


def _blocked(notes, reason):
    return "BLOCKED_FEE_UNVERIFIED", notes, reason


def _fee_state(gate, attestation, expected, expected_formula):
    """Return fee_state, notes, and fee_block_reason.

    A v2 gate (fee_admission, adoption_mode, or fee_formula_id) computes only
    when fee_admission is ADMITTED_INDEX_ONLY and the caller supplied the
    matching pair. A legacy gate stays on the v1 ATTEST_PASS path. The v1
    signature default is not an admitted v2 pair.
    """
    notes = []
    if not isinstance(gate, dict):
        return _blocked(notes, "GATE_MISSING")
    if gate.get("status") != "OK":
        return _blocked(notes, gate.get("fee_block_reason") or gate.get("reason") or "GATE_STATUS_NOT_OK")
    expected_id, expected_sha = expected
    if _is_v2_gate(gate):
        if "fee_admission" not in gate:
            return _blocked(notes, "FEE_ADMISSION_MISSING")
        if gate.get("fee_admission") != "ADMITTED_INDEX_ONLY":
            return _blocked(notes, gate.get("fee_block_reason") or "FEE_ADMISSION_NOT_ADMITTED")
        pair_ok = (
            expected_formula is not None
            and gate.get("fee_source") == expected_id
            and gate.get("fee_source_sha256") == expected_sha
            and gate.get("fee_formula_id") == expected_formula
        )
        if not pair_ok:
            return _blocked(notes, "FEE_SOURCE_PAIR_MISMATCH")
        return "ADMITTED", notes, None
    if gate.get("fee_source") != expected_id or gate.get("fee_source_sha256") != expected_sha:
        return _blocked(notes, "FEE_SOURCE_PAIR_MISMATCH")
    attest_reason = _attest_reason(gate)
    if attest_reason is not None:
        return _blocked(notes, attest_reason)
    if not isinstance(attestation, dict):
        return _blocked(notes, "FEE_ATTEST_ABSENT")
    series = attestation.get("series")
    accept = attestation.get("conductor_accept_sha256")
    admitted = (
        attestation.get("fee_source") == expected_id
        and attestation.get("fee_source_sha256") == expected_sha
        and attestation.get("rehash_ok") is True
        and attestation.get("packet_index_anchor_ok") is True
        and attestation.get("status") == "ADOPTED"
        and accept == CONDUCTOR_ACCEPT_SHA256
        and isinstance(attestation.get("examiner"), str)
        and attestation.get("examiner") != ""
        and isinstance(attestation.get("time"), str)
        and attestation.get("time") != ""
        and isinstance(series, list)
        and len(series) > 0
        and all(isinstance(item, dict) and item.get("series_status") == "PINNED" for item in series)
    )
    if not admitted:
        return _blocked(notes, "FEE_ATTEST_NOT_PASS")
    return "ADMITTED", notes, None


def _evaluations(raw_hi, rc_hi, admitted, cd):
    ev = {
        "pass_i": None if raw_hi is None else raw_hi < 0,
        "reject_a": None if raw_hi is None else raw_hi >= 0,
        "pass_ii": None if rc_hi is None else rc_hi < 0,
        "reject_b": None if rc_hi is None else rc_hi >= 0,
    }
    if not admitted:
        ev["reject_c"] = "BLOCKED_FEE_UNVERIFIED"
        ev["reject_d"] = "BLOCKED_FEE_UNVERIFIED"
    elif isinstance(cd, dict) and cd.get("n_signals") == 0:
        ev["reject_c"] = True
        ev["reject_d"] = True
    elif isinstance(cd, dict):
        ev["reject_c"] = cd.get("reject_c")
        ev["reject_d"] = cd.get("reject_d")
    else:
        ev["reject_c"] = None
        ev["reject_d"] = None
    return ev


def _cd_firing(cd):
    if not isinstance(cd, dict):
        return []
    if cd.get("n_signals") == 0:
        return ["(c)", "(d)"]
    firing = []
    if cd.get("reject_c") is True:
        firing.append("(c)")
    if cd.get("reject_d") is True:
        firing.append("(d)")
    return firing


def apply_verdict(
    score,
    *,
    gate=None,
    attestation=None,
    cd=None,
    validity=None,
    expected_fee_source=(FEE_SOURCE_ID, FEE_SOURCE_SHA256),
    expected_fee_formula=None,
):
    """Return the verdict label. cd booleans are precomputed and are not P&L."""
    score = score if isinstance(score, dict) else {}
    fee_state, notes, fee_block_reason = _fee_state(
        gate, attestation, expected_fee_source, expected_fee_formula
    )
    admitted = fee_state == "ADMITTED"
    if admitted and isinstance(cd, dict) and cd.get("n_signals") == 0:
        notes = list(notes) + ["NO_SIGNALS_SELECTED"]
    raw_hi = _hi(score, "CI95_D_raw")
    rc_hi = _hi(score, "CI95_D_rc")
    evaluations = _evaluations(raw_hi, rc_hi, admitted, cd)
    if isinstance(validity, dict) and validity.get("licence_gate") == "REFUSED":
        return {
            "verdict": "VOID",
            "reason": "LICENCE_GATE_REFUSED",
            "firing": [],
            "evaluations": evaluations,
            "fee_state": fee_state,
            "fee_block_reason": fee_block_reason,
            "notes": notes,
        }
    why = _degenerate_from(score)
    if why is not None:
        out = {
            "verdict": DEGENERATE,
            "degenerate_reason": why,
            "firing": [],
            "evaluations": evaluations,
            "fee_state": fee_state,
            "fee_block_reason": fee_block_reason,
            "notes": notes,
        }
        return out
    if raw_hi is None or rc_hi is None:
        raise ValueError("headline CI is missing")
    if evaluations["reject_a"] or evaluations["reject_b"]:
        firing = []
        if evaluations["reject_a"]:
            firing.append("(a)")
        if evaluations["reject_b"]:
            firing.append("(b)")
        if admitted:
            for label in _cd_firing(cd):
                if label not in firing:
                    firing.append(label)
            verdict = REJECT
        else:
            verdict = REJECT_FORECAST
        return {
            "verdict": verdict,
            "firing": firing,
            "evaluations": evaluations,
            "fee_state": fee_state,
            "fee_block_reason": fee_block_reason,
            "notes": notes,
        }
    if not admitted:
        return {
            "verdict": PASS_FORECAST,
            "firing": [],
            "evaluations": evaluations,
            "fee_state": fee_state,
            "fee_block_reason": fee_block_reason,
            "notes": notes,
        }
    if not isinstance(cd, dict) or cd.get("reject_c") is None or cd.get("reject_d") is None:
        if isinstance(cd, dict) and cd.get("n_signals") == 0:
            pass
        else:
            return {
                "verdict": FULL,
                "firing": [],
                "evaluations": evaluations,
                "fee_state": fee_state,
                "fee_block_reason": fee_block_reason,
                "notes": notes,
            }
    firing = _cd_firing(cd)
    if firing:
        verdict = REJECT
    else:
        verdict = PASS
    return {
        "verdict": verdict,
        "firing": firing,
        "evaluations": evaluations,
        "fee_state": fee_state,
        "fee_block_reason": fee_block_reason,
        "notes": notes,
    }


def main(argv):
    if len(argv) != 1:
        print("usage: python -m card01_amc.verdict score.json", file=sys.stderr)
        return 2
    score = json.loads(Path(argv[0]).read_text())
    json.dump(apply_verdict(score), sys.stdout, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
