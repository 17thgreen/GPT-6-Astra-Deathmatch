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

from card01_amc.fee_admission import FEE_FORMULA_ID, REFUSED_FEE_SOURCES

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


def _blocked(notes, reason):
    return "BLOCKED_FEE_UNVERIFIED", notes, reason


def _report_reason(regime_report, admission):
    secondary = regime_report.get("secondary") if isinstance(regime_report, dict) else None
    if isinstance(secondary, dict) and secondary.get("fee_block_reason"):
        return secondary.get("fee_block_reason")
    if isinstance(admission, dict) and admission.get("fee_block_reason"):
        return admission.get("fee_block_reason")
    return None


def _fee_state(regime_report):
    """Return fee_state, notes, and fee_block_reason from the regime report.

    The report is the fee state. A passed-in gate or pair is not read.
    """
    notes = []
    if not isinstance(regime_report, dict):
        return _blocked(notes, "FEE_REPORT_MISSING")
    admission = regime_report.get("fee_admission")
    if not isinstance(admission, dict):
        return _blocked(notes, "FEE_ADMISSION_MISSING")
    if (
        admission.get("fee_source") in REFUSED_FEE_SOURCES
        or admission.get("fee_source_sha256") in REFUSED_FEE_SOURCES
    ):
        return _blocked(notes, "FEE_SOURCE_NOT_ADMITTED_V1_ATTEST_FAIL")
    admitted = (
        regime_report.get("fee_state") == "ADMITTED"
        and admission.get("fee_admission") == "ADMITTED_INDEX_ONLY"
        and regime_report.get("verdict_fee_branch") is None
        and admission.get("fee_formula_id") == FEE_FORMULA_ID
        and isinstance(admission.get("fee_source_sha256"), str)
        and isinstance(admission.get("fee_source_accept_sha256"), str)
    )
    if admitted:
        return "ADMITTED", notes, None
    return _blocked(notes, _report_reason(regime_report, admission) or "FEE_ADMISSION_NOT_ADMITTED")


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
    expected_fee_sha256=None,
    expected_accept_sha256=None,
    regime_report=None,
):
    """Return the verdict label. cd booleans are precomputed and are not P&L.

    Fee state comes from regime_report, which build_report filled from the
    on-disk fee files. gate, attestation, and the expected pair are ignored.
    """
    del gate, attestation, expected_fee_sha256, expected_accept_sha256
    score = score if isinstance(score, dict) else {}
    fee_state, notes, fee_block_reason = _fee_state(regime_report)
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
