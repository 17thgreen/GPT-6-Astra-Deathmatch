"""C1 / C5 / degenerate-block verdict helper.

Examiner aid only. Nothing here is written back onto the scorer output.
INCONCLUSIVE_DEGENERATE_BLOCK is checked first and outranks REJECT (a) and (b).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

PASS_FORECAST = "FORECAST_ONLY_FEE_BLOCKED: PASS-FORECAST"
REJECT_FORECAST = "FORECAST_ONLY_FEE_BLOCKED: REJECT"
DEGENERATE = "INCONCLUSIVE_DEGENERATE_BLOCK"
FULL = "FULL_VERDICT_REQUIRES_EXAMINER"


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


def _evaluations(raw_hi, rc_hi, fee_blocked):
    ev = {
        "pass_i": None if raw_hi is None else raw_hi < 0,
        "reject_a": None if raw_hi is None else raw_hi >= 0,
        "pass_ii": None if rc_hi is None else rc_hi < 0,
        "reject_b": None if rc_hi is None else rc_hi >= 0,
    }
    if fee_blocked:
        ev["reject_c"] = "BLOCKED_FEE_UNVERIFIED"
        ev["reject_d"] = "BLOCKED_FEE_UNVERIFIED"
    else:
        ev["reject_c"] = None
        ev["reject_d"] = None
    return ev


def apply_verdict(score, fee_blocked=True):
    """Return the frozen verdict label for a scorer object or a CI dict."""
    why = _degenerate_from(score if isinstance(score, dict) else {})
    raw_hi = _hi(score, "CI95_D_raw") if isinstance(score, dict) else None
    rc_hi = _hi(score, "CI95_D_rc") if isinstance(score, dict) else None
    evaluations = _evaluations(raw_hi, rc_hi, fee_blocked)
    if why is not None:
        return {
            "verdict": DEGENERATE,
            "degenerate_reason": why,
            "firing": [],
            "evaluations": evaluations,
        }
    if raw_hi is None or rc_hi is None:
        raise ValueError("headline CI is missing")
    if not fee_blocked:
        return {
            "verdict": FULL,
            "firing": [],
            "evaluations": evaluations,
        }
    firing = []
    if evaluations["reject_a"]:
        firing.append("(a)")
    if evaluations["reject_b"]:
        firing.append("(b)")
    if evaluations["pass_i"] and evaluations["pass_ii"]:
        label = PASS_FORECAST
        firing = []
    else:
        label = REJECT_FORECAST
    return {"verdict": label, "firing": firing, "evaluations": evaluations}


def main(argv):
    if len(argv) != 1:
        print("usage: python -m card01_amc.verdict score.json", file=sys.stderr)
        return 2
    score = json.loads(Path(argv[0]).read_text())
    json.dump(apply_verdict(score), sys.stdout, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
