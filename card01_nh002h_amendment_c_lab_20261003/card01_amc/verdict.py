"""Examiner-aid verdict helper.

Precedence is validity, then INCONCLUSIVE_DEGENERATE_BLOCK, then REJECT (a)
or (b), then the fee branch. Notes do not change the verdict. Realized P&L
for (c) and (d) is supplied by the caller and is not computed here. A missing
boolean stays fail-closed. Zero signals make both (c) and (d) true.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from card01_amc.fee_admission import (
    FEE_FORMULA_ID,
    REFUSED_FEE_SOURCES,
    admit_fee_source_v2,
)
from card01_amc.pinload import sha256_bytes

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


# Production reader. Tests may monkeypatch this constant. No CLI or env override.
PINS_PATH = Path(__file__).resolve().parents[1] / "PINS.json"


def load_fee_source_v2(path=None):
    """Return the PINS.json fee_source_v2 pair, or None when it cannot be read."""
    target = PINS_PATH if path is None else Path(path)
    try:
        raw = target.read_bytes()
        doc = json.loads(raw.decode("utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError):
        return None
    block = doc.get("fee_source_v2") if isinstance(doc, dict) else None
    if not isinstance(block, dict):
        return None
    ident = block.get("id")
    digest = block.get("sha256")
    accept = block.get("accept_sha256")
    formula = block.get("fee_formula_id")
    if (
        not isinstance(ident, str)
        or ident == ""
        or not isinstance(digest, str)
        or len(digest) != 64
        or not isinstance(accept, str)
        or len(accept) != 64
        or not isinstance(formula, str)
        or formula == ""
    ):
        return None
    return {
        "id": ident,
        "sha256": digest,
        "accept_sha256": accept,
        "fee_formula_id": formula,
    }


def _fee_paths(fee_ctx):
    if not isinstance(fee_ctx, dict):
        return {"fee_source": None, "packet_index": None, "fee_accept": None}
    return {
        "fee_source": fee_ctx.get("fee_source_path"),
        "packet_index": fee_ctx.get("packet_index_path"),
        "fee_accept": fee_ctx.get("fee_accept_path"),
    }


def sha256_path(path):
    """Hash a file. path may be a string. Used by pnl_cd.module_sha256."""
    return sha256_bytes(Path(path).read_bytes())


def _sha_file(path):
    if path is None or path == "":
        return None
    try:
        return sha256_path(path)
    except OSError:
        return None


def _gate_fee_reason(gate, pin):
    """Consumer fee-state reasons. First failure wins. Pair is the PINS pair."""
    if not isinstance(gate, dict):
        return "GATE_MISSING"
    if (
        gate.get("fee_source") in REFUSED_FEE_SOURCES
        or gate.get("fee_source_sha256") in REFUSED_FEE_SOURCES
    ):
        return "FEE_SOURCE_NOT_ADMITTED_V1_ATTEST_FAIL"
    status = gate.get("status")
    if status == "BLOCKED_FEE_UNVERIFIED":
        return gate.get("fee_block_reason") or gate.get("reason") or "BLOCKED_FEE_UNVERIFIED"
    if status != "OK":
        return gate.get("fee_block_reason") or "GATE_STATUS_NOT_OK"
    if "fee_admission" not in gate:
        return "FEE_ADMISSION_MISSING"
    if gate.get("fee_admission") != "ADMITTED_INDEX_ONLY":
        return gate.get("fee_block_reason") or "FEE_ADMISSION_NOT_ADMITTED"
    if (
        gate.get("fee_source_sha256") != pin["sha256"]
        or gate.get("fee_source_accept_sha256") != pin["accept_sha256"]
    ):
        return "FEE_SOURCE_PAIR_MISMATCH"
    if gate.get("fee_formula_id") != pin["fee_formula_id"] or gate.get("fee_formula_id") != FEE_FORMULA_ID:
        return "FEE_FORMULA_ID_MISMATCH"
    return None


def disk_fee_state(gate, fee_ctx):
    """Rebuild v2 admission from the fee files. The expected pair is PINS only."""
    paths = _fee_paths(fee_ctx)
    fee_input_sha256 = {
        "fee_source": _sha_file(paths["fee_source"]),
        "packet_index": _sha_file(paths["packet_index"]),
        "fee_accept": _sha_file(paths["fee_accept"]),
    }
    pin = load_fee_source_v2()
    if pin is None:
        return {
            "admitted": False,
            "reason": "FEE_SOURCE_PAIR_MISSING",
            "admission": None,
            "pin": None,
            "fee_input_sha256": fee_input_sha256,
        }
    series = []
    if isinstance(gate, dict) and isinstance(gate.get("signals"), list):
        for signal in gate["signals"]:
            if isinstance(signal, dict):
                series.append(signal.get("series"))
    admission = admit_fee_source_v2(
        fee_source_path=paths["fee_source"],
        fee_source_id=pin["id"],
        fee_source_sha256=pin["sha256"],
        packet_index_path=paths["packet_index"],
        fee_accept_path=paths["fee_accept"],
        series_used=series,
    )
    if not admission.admitted:
        return {
            "admitted": False,
            "reason": admission.fee_block_reason or "FEE_RECOMPUTE_MISMATCH",
            "admission": admission,
            "pin": pin,
            "fee_input_sha256": fee_input_sha256,
        }
    if (
        admission.fee_source_sha256 != pin["sha256"]
        or admission.fee_source_accept_sha256 != pin["accept_sha256"]
        or admission.fee_formula_id != pin["fee_formula_id"]
        or admission.fee_formula_id != FEE_FORMULA_ID
    ):
        reason = "FEE_FORMULA_ID_MISMATCH"
        if (
            admission.fee_source_sha256 != pin["sha256"]
            or admission.fee_source_accept_sha256 != pin["accept_sha256"]
        ):
            reason = "FEE_SOURCE_PAIR_MISMATCH"
        return {
            "admitted": False,
            "reason": reason,
            "admission": admission,
            "pin": pin,
            "fee_input_sha256": fee_input_sha256,
        }
    reason = _gate_fee_reason(gate, pin)
    if reason is not None:
        return {
            "admitted": False,
            "reason": reason,
            "admission": admission,
            "pin": pin,
            "fee_input_sha256": fee_input_sha256,
        }
    return {
        "admitted": True,
        "reason": None,
        "admission": admission,
        "pin": pin,
        "fee_input_sha256": fee_input_sha256,
    }


def _pair_equal(left, pin):
    if not isinstance(left, dict) or pin is None:
        return False
    return (
        left.get("fee_source_sha256") == pin["sha256"]
        and left.get("fee_source_accept_sha256") == pin["accept_sha256"]
        and left.get("fee_formula_id") == pin["fee_formula_id"]
        and left.get("fee_formula_id") == FEE_FORMULA_ID
    )


def cd_from_prc(prc_output, gate, *, fee_ctx):
    """Hand-off check: schema, output hash, and the PINS fee pair.

    Returns the (c)/(d) booleans for apply_verdict, the blocked strings, or
    None when the hand-off fails. A caller-supplied pair is not accepted.
    """
    from card01_amc.pnl_cd import SCHEMA, score_body_sha256

    if not isinstance(prc_output, dict) or prc_output.get("schema") != SCHEMA:
        return None
    if score_body_sha256(prc_output) != prc_output.get("output_sha256"):
        return None
    state = disk_fee_state(gate, fee_ctx)
    status = prc_output.get("status")
    if status == "BLOCKED_FEE_UNVERIFIED":
        return {
            "n_signals": prc_output.get("n_signals"),
            "reject_c": "BLOCKED_FEE_UNVERIFIED",
            "reject_d": "BLOCKED_FEE_UNVERIFIED",
        }
    pin = state["pin"]
    if not _pair_equal(prc_output, pin) or not _pair_equal(gate, pin):
        return None
    if not state["admitted"]:
        return None
    defects = prc_output.get("reporting_defects") or []
    blocking = any(
        isinstance(item, dict) and item.get("blocking") is True for item in defects
    )
    if status in ("UNRESOLVED_INVENTORY_AT_SCORING", "REPORTING_DEFECT") or blocking:
        return {
            "n_signals": prc_output.get("n_signals"),
            "reject_c": None,
            "reject_d": None,
        }
    if prc_output.get("entry_book_anchor_status") != "VERIFIED":
        return None
    if status not in ("OK", "NO_SIGNALS_SELECTED"):
        return None
    return {
        "n_signals": prc_output.get("n_signals"),
        "reject_c": prc_output.get("reject_c"),
        "reject_d": prc_output.get("reject_d"),
    }


def main(argv):
    parser = argparse.ArgumentParser(prog="python -m card01_amc.verdict")
    parser.add_argument("score", nargs="?")
    parser.add_argument("--gate", default=None)
    parser.add_argument("--prc", default=None)
    parser.add_argument("--fee-source", default=None)
    parser.add_argument("--packet-index", default=None)
    parser.add_argument("--fee-accept", default=None)
    parser.add_argument("--regime-report", default=None)
    args = parser.parse_args(argv)
    if not args.score:
        print("usage: python -m card01_amc.verdict score.json", file=sys.stderr)
        return 2
    score = json.loads(Path(args.score).read_text(encoding="utf-8"))
    cd = None
    regime = None
    if args.prc is not None or args.gate is not None:
        if not args.prc or not args.gate:
            print("usage: --gate and --prc are supplied together", file=sys.stderr)
            return 2
        fee_ctx = {
            "fee_source_path": args.fee_source,
            "packet_index_path": args.packet_index,
            "fee_accept_path": args.fee_accept,
        }
        gate = json.loads(Path(args.gate).read_text(encoding="utf-8"))
        prc_output = json.loads(Path(args.prc).read_text(encoding="utf-8"))
        cd = cd_from_prc(prc_output, gate, fee_ctx=fee_ctx)
    if args.regime_report:
        regime = json.loads(Path(args.regime_report).read_text(encoding="utf-8"))
    json.dump(
        apply_verdict(score, cd=cd, regime_report=regime),
        sys.stdout,
        indent=1,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
