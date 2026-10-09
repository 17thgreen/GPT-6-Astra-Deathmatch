"""Examiner-aid verdict helper.

Precedence is validity, then INCONCLUSIVE_DEGENERATE_BLOCK, then REJECT (a)
or (b), then the fee branch. Notes do not change the verdict. Realized P&L
for (c) and (d) is supplied by the caller and is not computed here. A missing
boolean stays fail-closed. Zero signals make both (c) and (d) true.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

from card01_amc.fee_admission import (
    FEE_FORMULA_ID,
    REFUSED_FEE_SOURCES,
    admit_fee_source_v2,
    pinned_entry_v2,
)
from card01_amc.fee_source import FeeBlocked
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
    pinned = block.get("series_pinned")
    if (
        not isinstance(pinned, list)
        or not pinned
        or any(not isinstance(name, str) or name == "" for name in pinned)
        or len(set(pinned)) != len(pinned)
    ):
        return None
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
        "series_pinned": tuple(pinned),
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


def _checked_series(pin, gate):
    """Pinned series first, then any extra names the gate lists.

    Gate series can only add names. A blocked, empty, or missing gate adds
    nothing, and the pinned list is still checked.
    """
    names = list(pin["series_pinned"])
    extra = []
    if isinstance(gate, dict):
        signals = gate.get("signals")
        if isinstance(signals, list):
            for signal in signals:
                if isinstance(signal, dict):
                    extra.append(signal.get("series"))
        blocked = gate.get("blocked_series")
        if isinstance(blocked, list):
            extra.extend(blocked)
    for name in extra:
        if isinstance(name, str) and name != "" and name not in names:
            names.append(name)
    return names


def _disk_admission(fee_ctx, gate, pin):
    """Return (admission, reason). reason is None when the fee files admit."""
    paths = _fee_paths(fee_ctx)
    names = _checked_series(pin, gate)
    admission = admit_fee_source_v2(
        fee_source_path=paths["fee_source"],
        fee_source_id=pin["id"],
        fee_source_sha256=pin["sha256"],
        packet_index_path=paths["packet_index"],
        fee_accept_path=paths["fee_accept"],
        series_used=names,
    )
    if not admission.admitted:
        return admission, admission.fee_block_reason or "FEE_RECOMPUTE_MISMATCH"
    for name in names:
        try:
            pinned_entry_v2(admission, name)
        except FeeBlocked as exc:
            return admission, exc.reason
    if (
        admission.fee_source_sha256 != pin["sha256"]
        or admission.fee_source_accept_sha256 != pin["accept_sha256"]
    ):
        return admission, "FEE_SOURCE_PAIR_MISMATCH"
    if admission.fee_formula_id != pin["fee_formula_id"] or admission.fee_formula_id != FEE_FORMULA_ID:
        return admission, "FEE_FORMULA_ID_MISMATCH"
    return admission, None


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
    admission, reason = _disk_admission(fee_ctx, gate, pin)
    if reason is not None:
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


def _both_bool(reject_c, reject_d):
    return type(reject_c) is bool and type(reject_d) is bool


def _hex64(value):
    if not isinstance(value, str) or len(value) != 64:
        return False
    return all(char in "0123456789abcdef" for char in value)


def _handed_gate_sha(gate, gate_sha256):
    if isinstance(gate_sha256, str):
        return gate_sha256
    if not isinstance(gate, dict):
        return None
    raw = json.dumps(gate, sort_keys=True).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _gate_bound(prc_output, gate, gate_sha256):
    """True when the score's gate sha and n_signals match the handed gate."""
    inputs = prc_output.get("inputs_sha256")
    recorded = inputs.get("gate_output") if isinstance(inputs, dict) else None
    handed = _handed_gate_sha(gate, gate_sha256)
    if not _hex64(recorded) or recorded != handed:
        return False
    signals = gate.get("signals") if isinstance(gate, dict) else None
    if not isinstance(signals, list):
        return False
    return prc_output.get("n_signals") == len(signals)


def _gate_identities(gate, file_sha):
    """File bytes, compact canonical JSON, and spaced canonical JSON.

    build_report records the compact form in inputs_sha256.gate_output.
    The CLI records the file bytes. Both name the same parsed gate.
    """
    found = set()
    if isinstance(file_sha, str):
        found.add(file_sha)
    if isinstance(gate, dict):
        compact = json.dumps(gate, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")
        found.add(hashlib.sha256(compact).hexdigest())
        spaced = json.dumps(gate, sort_keys=True).encode("utf-8")
        found.add(hashlib.sha256(spaced).hexdigest())
    return found


def _regime_gate_ids(regime):
    """Identities build_report or a hand-built report actually records.

    inputs_sha256.gate_sha256 is entry_gate.module_sha256(), not the gate
    document, so it is not an identity of this gate.
    """
    found = []
    if not isinstance(regime, dict):
        return found
    if isinstance(regime.get("gate_sha256"), str):
        found.append(regime["gate_sha256"])
    inputs = regime.get("inputs_sha256")
    if isinstance(inputs, dict) and isinstance(inputs.get("gate_output"), str):
        found.append(inputs["gate_output"])
    return found


def _regime_n_signals(regime):
    """Signal count from the fields build_report fills, then a hand-built fallback."""
    if not isinstance(regime, dict):
        return None
    secondary = regime.get("secondary")
    sized = secondary.get("signals_and_size") if isinstance(secondary, dict) else None
    if isinstance(sized, dict) and type(sized.get("n_signals")) is int:
        return sized["n_signals"]
    if type(regime.get("n_signals")) is int:
        return regime["n_signals"]
    views = regime.get("fee_views")
    per = views.get("per_signal") if isinstance(views, dict) else None
    if isinstance(per, list):
        return len(per)
    return None


def _binding_reason(gate, file_sha, prc, regime):
    """None when the gate file, the PR-C output, and the regime report match.

    The regime side may hash the parsed gate as compact JSON. The PR-C side
    records the file bytes. n_signals is read from secondary.signals_and_size
    when build_report wrote it. A missing identity or a count disagreement
    is a named reason. The caller must not drop that reason and score the
    regime report on its own.
    """
    if not isinstance(prc, dict) or not isinstance(regime, dict) or not isinstance(gate, dict):
        return "BINDING_IDENTITY_MISSING"
    identities = _gate_identities(gate, file_sha)
    inputs = prc.get("inputs_sha256")
    prc_sha = inputs.get("gate_output") if isinstance(inputs, dict) else None
    if not isinstance(prc_sha, str):
        return "BINDING_IDENTITY_MISSING"
    if prc_sha not in identities:
        return "GATE_BINDING_MISMATCH"
    regime_ids = _regime_gate_ids(regime)
    if not regime_ids:
        return "BINDING_IDENTITY_MISSING"
    if any(item not in identities for item in regime_ids):
        return "GATE_BINDING_MISMATCH"
    signals = gate.get("signals")
    if not isinstance(signals, list):
        return "BINDING_IDENTITY_MISSING"
    n_signals = len(signals)
    regime_n = _regime_n_signals(regime)
    if type(prc.get("n_signals")) is not int or type(regime_n) is not int:
        return "N_SIGNALS_MISMATCH"
    if prc.get("n_signals") != n_signals or regime_n != n_signals:
        return "N_SIGNALS_MISMATCH"
    return None


def _triple_agrees(gate, file_sha, prc, regime):
    """True when _binding_reason finds no mismatch."""
    return _binding_reason(gate, file_sha, prc, regime) is None


def _binding_block(score, reason, regime, detail=None):
    """Examiner hand-off. cd is not taken from a report that failed to bind."""
    raw_hi = _hi(score if isinstance(score, dict) else {}, "CI95_D_raw")
    rc_hi = _hi(score if isinstance(score, dict) else {}, "CI95_D_rc")
    evaluations = _evaluations(raw_hi, rc_hi, True, None)
    fee_state = "BLOCKED_FEE_UNVERIFIED"
    if isinstance(regime, dict) and isinstance(regime.get("fee_state"), str):
        fee_state = regime["fee_state"]
    out = {
        "verdict": FULL,
        "binding_reason": reason,
        "firing": [],
        "evaluations": evaluations,
        "fee_state": fee_state,
        "fee_block_reason": reason,
        "notes": [reason],
    }
    if detail is not None:
        out["binding_detail"] = detail
    return out


def cd_from_prc(prc_output, gate, *, fee_ctx, gate_sha256=None):
    """Hand-off check: schema, output hash, the PINS fee pair, and the gate.

    Returns the (c)/(d) booleans for apply_verdict, or None when the hand-off
    fails. A blocked PR-C output is None. reject_c and reject_d are returned
    only when both are real booleans. The recorded gate sha must equal the
    sha of the gate handed here, and n_signals must equal that gate's signal
    count. A caller-supplied pair is not accepted.
    """
    from card01_amc.pnl_cd import SCHEMA, score_body_sha256

    if not isinstance(prc_output, dict) or prc_output.get("schema") != SCHEMA:
        return None
    if score_body_sha256(prc_output) != prc_output.get("output_sha256"):
        return None
    status = prc_output.get("status")
    if status == "BLOCKED_FEE_UNVERIFIED":
        return None
    state = disk_fee_state(gate, fee_ctx)
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
        return None
    if prc_output.get("entry_book_anchor_status") != "VERIFIED":
        return None
    if status not in ("OK", "NO_SIGNALS_SELECTED"):
        return None
    if not _gate_bound(prc_output, gate, gate_sha256):
        return None
    reject_c = prc_output.get("reject_c")
    reject_d = prc_output.get("reject_d")
    if not _both_bool(reject_c, reject_d):
        return None
    return {
        "n_signals": prc_output.get("n_signals"),
        "reject_c": reject_c,
        "reject_d": reject_d,
    }


def _fee_paths_ready(fee_ctx):
    """True when all three fee paths are present files."""
    paths = _fee_paths(fee_ctx)
    for key in ("fee_source", "packet_index", "fee_accept"):
        path = paths[key]
        if not isinstance(path, str) or path == "":
            return False
        if not Path(path).is_file():
            return False
    return True


def _disk_files_admit(fee_ctx, gate):
    """Fee-file admission. A blocked gate status is not itself a disk block.

    The pinned series list is always checked. Names on the gate can only add
    series. A missing gate adds none.
    """
    pin = load_fee_source_v2()
    if pin is None:
        return False
    _admission, reason = _disk_admission(fee_ctx, gate, pin)
    return reason is None


def _race_ids(items):
    if not isinstance(items, list):
        return None
    found = []
    for item in items:
        if not isinstance(item, dict) or "race_id" not in item:
            return None
        found.append(item["race_id"])
    return found


def _signal_identity_reason(gate, prc):
    """SIGNAL_IDENTITY_MISMATCH when race_id multisets differ.

    Order does not matter. The PR-C side is per_signal. The gate side is
    signals. A missing list is a mismatch.
    """
    gate_ids = _race_ids(gate.get("signals") if isinstance(gate, dict) else None)
    prc_ids = _race_ids(prc.get("per_signal") if isinstance(prc, dict) else None)
    if gate_ids is None or prc_ids is None:
        return "SIGNAL_IDENTITY_MISMATCH"
    try:
        if Counter(gate_ids) != Counter(prc_ids):
            return "SIGNAL_IDENTITY_MISMATCH"
    except TypeError:
        return "SIGNAL_IDENTITY_MISMATCH"
    return None


_ABSENT = object()

# Positive fee-block labels. A trailing underscore is a prefix for that family.
# FEE_SOURCE_ includes FEE_SOURCE_UNREADABLE and the v1 refusal
# FEE_SOURCE_NOT_ADMITTED_V1_ATTEST_FAIL. NOT_AN_ACCEPT is the accept-file
# label. SERIES_NOT_PINNED, HEADLINE_SCOPE_MISMATCH and TAKER_RATE_MISMATCH
# are fee-rule blocks. The bare status BLOCKED_FEE_UNVERIFIED is not a reason.
# GATE_NOT_REPRODUCED, ENTRY_BOOK_*, ENTRY_ROW_BOOK_MISSING, an OK gate, and a
# missing field are not here.
FEE_CLASS_REASONS = (
    "FEE_SOURCE_",
    "FEE_ACCEPT_",
    "ACCEPT_69B98B2F_",
    "FEE_CITATIONS_CHANGED",
    "NOT_AN_ACCEPT",
    "FEE_FORMULA_ID_MISMATCH",
    "SERIES_NOT_PINNED",
    "HEADLINE_SCOPE_MISMATCH",
    "TAKER_RATE_MISMATCH",
)


def _is_fee_class_reason(reason):
    """True when reason is a fee or citation block label in FEE_CLASS_REASONS."""
    if not isinstance(reason, str) or reason == "":
        return False
    for label in FEE_CLASS_REASONS:
        if reason == label:
            return True
        if label.endswith("_") and reason.startswith(label):
            return True
    return False


def _label(value, missing):
    if isinstance(value, str) and value != "":
        return value
    return missing


def _regime_fee_block_gap(regime):
    """None when the report's own fee_admission proves a fee-class block.

    fee_state is not read. A GATE_NOT_REPRODUCED report whose admission is
    still ADMITTED_INDEX_ONLY does not prove a fee block.
    """
    if not isinstance(regime, dict):
        return "not_a_report"
    admission = regime.get("fee_admission")
    if not isinstance(admission, dict):
        return "fee_admission_missing"
    if admission.get("fee_admission") != "BLOCKED_FEE_UNVERIFIED":
        return "fee_admission=" + _label(admission.get("fee_admission"), "missing")
    if _is_fee_class_reason(admission.get("fee_block_reason")):
        return None
    return "reason=" + _label(admission.get("fee_block_reason"), "missing")


def _prc_fee_block_gap(prc):
    """None when status or fee_state is blocked for a fee-class reason."""
    if not isinstance(prc, dict):
        return "not_a_prc"
    status = prc.get("status")
    state = prc.get("fee_state")
    blocked = (
        status == "BLOCKED_FEE_UNVERIFIED"
        or state == "BLOCKED_FEE_UNVERIFIED"
    )
    if not blocked:
        return "status=" + _label(status, "missing") + ",fee_state=" + _label(state, "missing")
    if _is_fee_class_reason(prc.get("fee_block_reason")):
        return None
    return "reason=" + _label(prc.get("fee_block_reason"), "missing")


def _gate_fee_block_gap(gate):
    """None only when the gate status is BLOCKED_FEE_UNVERIFIED.

    An OK gate with an empty signals list does not prove a fee block.
    """
    if not isinstance(gate, dict):
        return "not_a_gate"
    if gate.get("status") == "BLOCKED_FEE_UNVERIFIED":
        return None
    return "status=" + _label(gate.get("status"), "missing")


def _unproven_fee_blocks(regime, gate, prc):
    """Supplied inputs that do not positively prove a fee block.

    _ABSENT means that input was not supplied. Each item is name:why.
    """
    gaps = []
    if regime is not _ABSENT:
        why = _regime_fee_block_gap(regime)
        if why is not None:
            gaps.append("regime_report:" + why)
    if prc is not _ABSENT:
        why = _prc_fee_block_gap(prc)
        if why is not None:
            gaps.append("prc:" + why)
    if gate is not _ABSENT:
        why = _gate_fee_block_gap(gate)
        if why is not None:
            gaps.append("gate:" + why)
    return gaps


def _get(doc, *keys):
    for key in keys:
        if not isinstance(doc, dict):
            return None
        doc = doc.get(key)
    return doc


def _disk_identity(fee_ctx, gate):
    """Fee identity of this disk admission, or None when the pin cannot be read."""
    pin = load_fee_source_v2()
    if pin is None:
        return None
    admission, reason = _disk_admission(fee_ctx, gate, pin)
    paths = _fee_paths(fee_ctx)
    return {
        "reason": reason,
        "pin_sha256": pin["sha256"],
        "pin_accept_sha256": pin["accept_sha256"],
        "adm_fee_source_sha256": admission.fee_source_sha256,
        "adm_accept_sha256": admission.fee_source_accept_sha256,
        "adm_packet_index_sha256": admission.packet_index_sha256_at_run,
        "file_fee_source": _sha_file(paths["fee_source"]),
        "file_packet_index": _sha_file(paths["packet_index"]),
        "file_fee_accept": _sha_file(paths["fee_accept"]),
    }


def _fee_identity_gaps(disk, regime, gate, prc):
    """Each supplied input's recorded fee identity must equal the disk's own.

    An absent field is None. disk.reason must itself be fee-class. Any
    difference is name:field.
    """
    if disk is None:
        return ["disk:pin_missing"]
    checks = []
    if regime is not _ABSENT:
        checks += [
            ("regime_report", "fee_block_reason", _get(regime, "fee_admission", "fee_block_reason"), disk["reason"]),
            ("regime_report", "fee_source_sha256", _get(regime, "fee_admission", "fee_source_sha256"), disk["adm_fee_source_sha256"]),
            ("regime_report", "fee_source_accept_sha256", _get(regime, "fee_admission", "fee_source_accept_sha256"), disk["adm_accept_sha256"]),
            ("regime_report", "packet_index_sha256_at_run", _get(regime, "fee_admission", "packet_index_sha256_at_run"), disk["adm_packet_index_sha256"]),
            ("regime_report", "inputs.fee_source_accept", _get(regime, "inputs_sha256", "fee_source_accept"), disk["adm_accept_sha256"]),
            ("regime_report", "inputs.packet_index_at_admission", _get(regime, "inputs_sha256", "packet_index_at_admission"), disk["adm_packet_index_sha256"]),
        ]
    if gate is not _ABSENT:
        reason = _get(gate, "fee_block_reason") or _get(gate, "reason")
        checks += [
            ("gate", "fee_block_reason", reason, disk["reason"]),
            ("gate", "fee_source_sha256", _get(gate, "fee_source_sha256"), disk["adm_fee_source_sha256"]),
            ("gate", "fee_source_accept_sha256", _get(gate, "fee_source_accept_sha256"), disk["adm_accept_sha256"]),
            ("gate", "packet_index_sha256_at_run", _get(gate, "packet_index_sha256_at_run"), disk["adm_packet_index_sha256"]),
        ]
    if prc is not _ABSENT:
        checks += [
            ("prc", "fee_block_reason", _get(prc, "fee_block_reason"), disk["reason"]),
            ("prc", "inputs.fee_source", _get(prc, "inputs_sha256", "fee_source"), disk["file_fee_source"]),
            ("prc", "inputs.packet_index", _get(prc, "inputs_sha256", "packet_index"), disk["file_packet_index"]),
            ("prc", "inputs.fee_accept", _get(prc, "inputs_sha256", "fee_accept"), disk["file_fee_accept"]),
            ("prc", "fee_source_sha256", _get(prc, "fee_source_sha256"), disk["pin_sha256"]),
            ("prc", "fee_source_accept_sha256", _get(prc, "fee_source_accept_sha256"), disk["pin_accept_sha256"]),
        ]
    gaps = []
    for name, field, got, want in checks:
        if got != want:
            gaps.append(name + ":" + field)
    if disk["reason"] is None or not _is_fee_class_reason(disk["reason"]):
        gaps.append("disk:reason")
    return gaps


def _forecast_only(score, regime):
    """Disk-blocked hand-off when every supplied input proves a fee block.

    A supplied report is passed through. It is not replaced with a missing report.
    """
    return apply_verdict(score, cd=None, regime_report=regime)


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
    touched = args.regime_report is not None or args.gate is not None or args.prc is not None
    if not touched:
        json.dump(apply_verdict(score, cd=None, regime_report=None), sys.stdout, indent=1)
        return 0
    fee_ctx = {
        "fee_source_path": args.fee_source,
        "packet_index_path": args.packet_index,
        "fee_accept_path": args.fee_accept,
    }
    if not _fee_paths_ready(fee_ctx):
        json.dump(_binding_block(score, "FEE_PATHS_REQUIRED", None), sys.stdout, indent=1)
        return 0
    gate = None
    gate_sha = None
    if args.gate is not None:
        gate_bytes = Path(args.gate).read_bytes()
        gate = json.loads(gate_bytes.decode("utf-8"))
        gate_sha = hashlib.sha256(gate_bytes).hexdigest()
    if not _disk_files_admit(fee_ctx, gate):
        regime = _ABSENT
        if args.regime_report is not None:
            regime = json.loads(Path(args.regime_report).read_text(encoding="utf-8"))
        prc_output = _ABSENT
        if args.prc is not None:
            prc_output = json.loads(Path(args.prc).read_text(encoding="utf-8"))
        gaps = _unproven_fee_blocks(
            regime,
            gate if args.gate is not None else _ABSENT,
            prc_output,
        )
        if gaps:
            report = regime if isinstance(regime, dict) else None
            json.dump(
                _binding_block(
                    score,
                    "DISK_BLOCKED_INPUTS_ADMITTED",
                    report,
                    detail=";".join(gaps),
                ),
                sys.stdout,
                indent=1,
            )
            return 0
        identity = _fee_identity_gaps(
            _disk_identity(fee_ctx, gate),
            regime,
            gate if args.gate is not None else _ABSENT,
            prc_output,
        )
        if identity:
            report = regime if isinstance(regime, dict) else None
            json.dump(
                _binding_block(
                    score,
                    "DISK_INPUT_FEE_IDENTITY_MISMATCH",
                    report,
                    detail=";".join(identity),
                ),
                sys.stdout,
                indent=1,
            )
            return 0
        handed = None if regime is _ABSENT else regime
        json.dump(_forecast_only(score, handed), sys.stdout, indent=1)
        return 0
    if args.regime_report is None:
        json.dump(_binding_block(score, "REGIME_REPORT_REQUIRED", None), sys.stdout, indent=1)
        return 0
    regime = json.loads(Path(args.regime_report).read_text(encoding="utf-8"))
    if args.gate is None:
        json.dump(_binding_block(score, "GATE_REQUIRED", regime), sys.stdout, indent=1)
        return 0
    if args.prc is None:
        json.dump(_binding_block(score, "PRC_REQUIRED", regime), sys.stdout, indent=1)
        return 0
    fee_state, _notes, _why = _fee_state(regime)
    if fee_state != "ADMITTED":
        json.dump(
            _binding_block(score, "REGIME_BLOCKED_DISK_ADMITS", regime),
            sys.stdout,
            indent=1,
        )
        return 0
    prc_output = json.loads(Path(args.prc).read_text(encoding="utf-8"))
    reason = _binding_reason(gate, gate_sha, prc_output, regime)
    if reason is not None:
        json.dump(_binding_block(score, reason, regime), sys.stdout, indent=1)
        return 0
    identity = _signal_identity_reason(gate, prc_output)
    if identity is not None:
        json.dump(_binding_block(score, identity, regime), sys.stdout, indent=1)
        return 0
    cd = cd_from_prc(
        prc_output,
        gate,
        fee_ctx=fee_ctx,
        gate_sha256=gate_sha,
    )
    json.dump(
        apply_verdict(score, cd=cd, regime_report=regime),
        sys.stdout,
        indent=1,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
