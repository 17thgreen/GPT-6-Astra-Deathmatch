"""PR-C REJECT (c) and (d) realized P&L, including the one-tick-worse stress.

Pre-outcome. Synthetic fixtures only. No resampling. Headline fee only.
The fee pair is read from the PINS document. Fee files are runtime inputs.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
import sys
from decimal import Decimal, ROUND_HALF_EVEN
from pathlib import Path

from card01_amc.entry_gate import EXTRA_COST as BUFFER_2C
from card01_amc.entry_gate import OutcomePresent as GateOutcomePresent
from card01_amc.entry_gate import gate_v2
from card01_amc.fee_source import FeeBlocked, pinned_taker_fee
from card01_amc import join_outcomes
from card01_amc.verdict import disk_fee_state, load_fee_source_v2, sha256_path
from card01_amc.fee_admission import pinned_entry_v2

TICK = Decimal("0.01")
ENTRY_TABLE_SCHEMA = "astra.card01.prc_entry_table.v1"
ENTRY_BOOK_SCHEMA = "astra.card01.prc_entry_book.v1"
ANCHOR_SCHEMA = "astra.card01.prc_entry_book_anchor.v1"
SCHEMA = "astra.card01.prc_pnl_cd.v1"
SENSITIVITY_ROWS_STATUS = "SENSITIVITY_BASIS_INCOMPLETE"
NET_FIGURE_LABEL = "ILLUSTRATIVE/R39"
# Inclusive after the 21:45–22:15Z capture close. Exclusive before the
# earliest US poll close (6pm EST, eastern IN/KY, after DST ends 2026-11-01).
ANCHOR_EARLIEST_UTC = "2026-11-02T22:15:00Z"
ANCHOR_BEFORE_UTC = "2026-11-03T23:00:00Z"
OUTCOME_KEYS = ("y", "result", "settlement", "outcome", "settled")
RULING_SHA256 = "61c1e4ea948109508ef12497a96b45f728f8e183168b26bffb87f11fda6107ca"
CITATION_DETAIL = (
    "base freeze c3172446 s9 (d) cites 'the NH-001 check'; NH-001 net included "
    "the 2c buffer; per ruling 61c1e4ea (4) the citation refers to the "
    "concentration-test shape only and the buffer is excluded everywhere"
)
GOVERNING_SHAS = (
    "114c5f2b635e419696fe627f6f27b6ca1175755e60a3ffb1ce550a2d699915be",
    "b8cb27e0e94c2a27c22fd1d92395109168a90ca78bb5928a65fbf0f89c397517",
    "c05d70037b82d62a9cf01740b50a34773f87025cd6887f5dcfc68f8a443bb813",
    "715fbafd588845867d7fe0af59b32a21d2411afc14bfb6da718f5592e0608703",
    "2c870cd57fc4acb4290c1273e06876e8380159f2f6614a5519314b43817a8583",
    "69b98b2f643a7510280cd6b959c30e285df081c8142b910808001db8cad5b81a",
    "861b7d14e75979f798b872a2c16b6e440d4f5b6332d4ad9e1e81d713863f5757",
    "e5227270b6e767b0c25fdfe68b8a859351a1a84d42200816c0f7eac6aad56bde",
    "c5b08459dd6f1e1e6cae65dbb13c4aa5b0d6a1418d79d3bae54c9370d9beede5",
    "61c1e4ea948109508ef12497a96b45f728f8e183168b26bffb87f11fda6107ca",
    "c31724463d81747702910a2d5296c2fc21d2a1dbc594727b26ac3d894b55ec59",
    "ee6af37cef95f1e468d28e5b06750caaca8b1706ec11ed5cf5cdce460524c2c6",
    "cc75f09614ad285756fd7cb7f7a5c2ce4e711b5adb98102c2dd043ccfc1af0f0",
)
_ANCHOR_SHA_FIELDS = (
    "entry_book_file_sha256",
    "entry_book_output_sha256",
    "entry_table_sha256",
    "gate_sha256",
    "fee_source_sha256",
    "pnl_cd_sha256",
    "ruling_sha256",
)


class OutcomePresent(RuntimeError):
    pass


def module_sha256() -> str:
    return sha256_path(__file__)


def _sha_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def entry_table_sha256(table) -> str:
    raw = json.dumps(table, indent=1, sort_keys=True, ensure_ascii=True) + "\n"
    return _sha_text(raw)


def envelope_output_sha256(obj) -> str:
    body = {key: value for key, value in obj.items() if key != "output_sha256"}
    return hashlib.sha256(json.dumps(body, indent=1).encode()).hexdigest()


def score_body_sha256(obj) -> str:
    """Hash the score. The labelled sensitivity row is not a verdict input."""
    body = {
        key: value
        for key, value in obj.items()
        if key not in ("output_sha256", "sensitivity_buffered_2c")
    }
    raw = json.dumps(body, indent=1, sort_keys=True, ensure_ascii=True) + "\n"
    return _sha_text(raw)


def _citation_defect():
    return {
        "kind": "CITATION_WORDING_NH001_CHECK",
        "detail": CITATION_DETAIL,
        "verdict_effect": "NONE",
        "validity_effect": "NONE",
        "blocking": False,
    }


def _carries_outcome(obj) -> bool:
    if not isinstance(obj, dict):
        return False
    for key in OUTCOME_KEYS:
        if key in obj:
            return True
    return False


def _hex64(value) -> bool:
    if not isinstance(value, str) or len(value) != 64:
        return False
    for char in value:
        if char not in "0123456789abcdef":
            return False
    return True


ASCII_DIGITS = "0123456789"
ISO_Z_SHAPE = "dddd-dd-ddTdd:dd:ddZ"


def _iso_z(value) -> bool:
    """True only for dddd-dd-ddTdd:dd:ddZ with ASCII digits and in-range parts.

    The full string is exactly 20 characters. A trailing newline does not match.
    Unicode decimal digits are rejected before int(), so they cannot verify
    and they cannot raise.
    """
    if not isinstance(value, str) or len(value) != len(ISO_Z_SHAPE):
        return False
    for char, shape in zip(value, ISO_Z_SHAPE):
        if shape == "d":
            if char not in ASCII_DIGITS:
                return False
        elif char != shape:
            return False
    month = int(value[5:7])
    day = int(value[8:10])
    hour = int(value[11:13])
    minute = int(value[14:16])
    second = int(value[17:19])
    if month < 1 or month > 12 or day < 1 or day > 31:
        return False
    if hour > 23 or minute > 59 or second > 59:
        return False
    return True


def _duplicate_race_id(items) -> bool:
    """True when a race_id is not a str, or a str race_id repeats.

    Scoring keys rows by the raw value, so 1, 1.0 and True are one key.
    Any non-str race_id is a reporting defect before that collision is scored.
    Non-dicts and race_id None are ignored, matching the book lookups.
    """
    seen = set()
    if not isinstance(items, list):
        return False
    for item in items:
        if not isinstance(item, dict):
            continue
        rid = item.get("race_id")
        if rid is None:
            continue
        if not isinstance(rid, str):
            return True
        if rid in seen:
            return True
        seen.add(rid)
    return False


def _on_open_grid(price: Decimal) -> bool:
    if not (Decimal(0) < price < Decimal(1)):
        return False
    grid = price.quantize(Decimal("0.0001"))
    gap = grid - price
    if gap < 0:
        gap = -gap
    return gap <= Decimal("1e-9")


def _blocked_table():
    return {
        "schema": ENTRY_TABLE_SCHEMA,
        "status": "BLOCKED_FEE_UNVERIFIED",
        "tick": str(TICK),
        "signals": None,
    }


def _identity(state):
    pin = state.get("pin") or {}
    admission = state.get("admission")
    fee_admission = "ADMITTED_INDEX_ONLY" if state.get("admitted") else "BLOCKED_FEE_UNVERIFIED"
    if admission is not None and not state.get("admitted"):
        fee_admission = admission.fee_admission
    return {
        "fee_admission": fee_admission,
        "fee_source": pin.get("id"),
        "fee_source_sha256": pin.get("sha256"),
        "fee_source_accept_sha256": pin.get("accept_sha256"),
        "fee_formula_id": pin.get("fee_formula_id"),
        "fee_block_reason": state.get("reason"),
        "fee_input_sha256": state.get("fee_input_sha256") or {},
    }


def entry_book(gate, *, fee_ctx) -> dict:
    """Outcome-free entry table. Prices and headline fees, no settlement read."""
    if _carries_outcome(gate):
        raise OutcomePresent(OUTCOME_KEYS[0])
    signals = gate.get("signals") if isinstance(gate, dict) else None
    if isinstance(signals, list):
        for signal in signals:
            if _carries_outcome(signal):
                raise OutcomePresent(OUTCOME_KEYS[0])
    state = disk_fee_state(gate, fee_ctx)
    ident = _identity(state)
    if not state["admitted"]:
        table = _blocked_table()
        return {
            "status": "BLOCKED_FEE_UNVERIFIED",
            "reporting_defects": [],
            "entry_table": table,
            "entry_table_sha256": entry_table_sha256(table),
            **ident,
        }
    defects = []
    rows = []
    if isinstance(signals, list) and _duplicate_race_id(signals):
        defects.append({"kind": "DUPLICATE_RACE_ID", "blocking": True, "detail": "signals"})
    if not signals:
        table = {
            "schema": ENTRY_TABLE_SCHEMA,
            "status": "NO_SIGNALS_SELECTED",
            "tick": str(TICK),
            "signals": [],
        }
        return {
            "status": "NO_SIGNALS_SELECTED",
            "reporting_defects": defects,
            "entry_table": table,
            "entry_table_sha256": entry_table_sha256(table),
            **ident,
        }
    for signal in signals:
        if signal.get("contracts") != 1:
            defects.append({"kind": "CONTRACTS_NOT_1", "blocking": True})
        price = Decimal(str(signal["price"]))
        worse = price + TICK
        entry = pinned_entry_v2(state["admission"], signal.get("series"))
        quoted = pinned_taker_fee(entry, price)
        declared = Decimal(signal["fee_decimal"])
        if quoted["headline"] != declared:
            defects.append({"kind": "FEE_RECOMPUTE_MISMATCH", "blocking": True})
        fee2 = None
        if not _on_open_grid(worse):
            defects.append({"kind": "STRESS_PRICE_OFF_GRID", "blocking": True})
        else:
            try:
                fee2 = pinned_taker_fee(entry, worse)["headline"]
            except FeeBlocked:
                defects.append({"kind": "STRESS_PRICE_OFF_GRID", "blocking": True})
        rows.append({
            "race_id": signal["race_id"],
            "side": signal["side"],
            "contracts": 1,
            "price": str(price),
            "fee_headline": str(quoted["headline"]),
            "price_one_tick_worse": str(worse),
            "fee_headline_one_tick_worse": None if fee2 is None else str(fee2),
        })
    status = "REPORTING_DEFECT" if defects else "OK"
    table = {
        "schema": ENTRY_TABLE_SCHEMA,
        "status": "OK",
        "tick": str(TICK),
        "signals": rows,
    }
    return {
        "status": status,
        "reporting_defects": defects,
        "entry_table": table,
        "entry_table_sha256": entry_table_sha256(table),
        **ident,
    }


def settle(book, joined_rows) -> dict:
    """The only reader of settlement. Prices and fees come from the anchored table."""
    table = book["entry_table"]
    signals = table.get("signals") or []
    if table.get("status") == "BLOCKED_FEE_UNVERIFIED":
        return {
            "status": "BLOCKED_FEE_UNVERIFIED",
            "n_signals": None,
            "per_signal": None,
            "reject_c": "BLOCKED_FEE_UNVERIFIED",
            "reject_d": "BLOCKED_FEE_UNVERIFIED",
        }
    if not signals:
        return {"status": "NO_SIGNALS_SELECTED", "n_signals": 0, "per_signal": []}
    by_id = {}
    for row in joined_rows:
        if isinstance(row, dict) and row.get("race_id") is not None:
            by_id[row["race_id"]] = row
    unresolved = []
    per_signal = []
    for signal in signals:
        row = by_id.get(signal["race_id"])
        observed = row.get("y") if isinstance(row, dict) else None
        if observed not in (0, 1):
            unresolved.append(signal["race_id"])
            continue
        payoff = Decimal(observed) if signal["side"] == "D_YES" else Decimal(1) - Decimal(observed)
        price = Decimal(signal["price"])
        fee = Decimal(signal["fee_headline"])
        worse = Decimal(signal["price_one_tick_worse"])
        fee2 = Decimal(signal["fee_headline_one_tick_worse"])
        gross = payoff - price
        net = gross - fee
        net2 = payoff - worse - fee2
        per_signal.append({
            "race_id": signal["race_id"],
            "side": signal["side"],
            "y": observed,
            "payoff": str(payoff),
            "price": str(price),
            "fee_headline": str(fee),
            "gross": str(gross),
            "net_headline": str(net),
            "price_one_tick_worse": str(worse),
            "fee_headline_one_tick_worse": str(fee2),
            "net_one_tick_worse": str(net2),
        })
    if unresolved:
        return {
            "status": "UNRESOLVED_INVENTORY_AT_SCORING",
            "n_signals": len(signals),
            "unresolved_race_ids": unresolved,
            "per_signal": None,
            "reject_c": None,
            "reject_d": None,
        }
    return {"status": "OK", "n_signals": len(signals), "per_signal": per_signal}


def _sum(values):
    total = Decimal(0)
    for value in values:
        total += value
    return total


def evaluate_cd(settled) -> dict:
    """(c) and (d) from headline nets. No builtin max or min. Stress is (c) only."""
    status = settled.get("status")
    if status == "BLOCKED_FEE_UNVERIFIED":
        return {
            "status": status,
            "n_signals": None,
            "reject_c": "BLOCKED_FEE_UNVERIFIED",
            "reject_d": "BLOCKED_FEE_UNVERIFIED",
            "notes": [],
        }
    if status == "UNRESOLVED_INVENTORY_AT_SCORING":
        return {
            "status": status,
            "n_signals": settled.get("n_signals"),
            "unresolved_race_ids": list(settled.get("unresolved_race_ids") or []),
            "reject_c": None,
            "reject_d": None,
            "notes": [],
        }
    if status == "NO_SIGNALS_SELECTED" or not settled.get("per_signal"):
        return {
            "status": "NO_SIGNALS_SELECTED",
            "n_signals": 0,
            "net_headline_total": "0",
            "net_one_tick_worse_total": "0",
            "sum_positive_net": "0",
            "max_positive_net": None,
            "top1_positive_share": None,
            "top1_positive_share_status": "NO_SIGNALS_SELECTED",
            "top1_rule": "fires iff 2*max_positive_net > sum_positive_net",
            "best_two_winners": [],
            "net_excluding_best_two_winners": "0",
            "reject_c_at_ask": True,
            "reject_c_one_tick_worse": True,
            "reject_c": True,
            "reject_d_top1": False,
            "reject_d_drop_best_two": True,
            "reject_d": True,
            "notes": ["NO_SIGNALS_SELECTED"],
            "per_signal": [],
        }
    rows = settled["per_signal"]
    nets = [Decimal(row["net_headline"]) for row in rows]
    nets2 = [Decimal(row["net_one_tick_worse"]) for row in rows]
    total = _sum(nets)
    total2 = _sum(nets2)
    positives = []
    for net in nets:
        if net > 0:
            positives.append(net)
    sum_pos = _sum(positives)
    max_pos = None
    for net in positives:
        if max_pos is None or net > max_pos:
            max_pos = net
    best_two = sorted(positives, reverse=True)[:2]
    drop = total - _sum(best_two)
    if positives:
        share = (max_pos / sum_pos).quantize(Decimal("0.000001"), rounding=ROUND_HALF_EVEN)
        top1_fire = (max_pos * 2) > sum_pos
        share_text = str(share)
        share_status = "OK"
        max_text = str(max_pos)
    else:
        top1_fire = False
        share_text = None
        share_status = "NO_POSITIVE_PNL"
        max_text = None
    at_ask = total <= 0
    stressed = total2 <= 0
    drop_fire = drop <= 0
    return {
        "status": "OK",
        "n_signals": len(rows),
        "per_signal": rows,
        "net_headline_total": str(total),
        "net_one_tick_worse_total": str(total2),
        "sum_positive_net": str(sum_pos),
        "max_positive_net": max_text,
        "top1_positive_share": share_text,
        "top1_positive_share_status": share_status,
        "top1_rule": "fires iff 2*max_positive_net > sum_positive_net",
        "best_two_winners": [str(value) for value in best_two],
        "net_excluding_best_two_winners": str(drop),
        "reject_c_at_ask": at_ask,
        "reject_c_one_tick_worse": stressed,
        "reject_c": at_ask or stressed,
        "reject_d_top1": top1_fire,
        "reject_d_drop_best_two": drop_fire,
        "reject_d": top1_fire or drop_fire,
        "notes": [],
    }


def entry_book_envelope(gate, *, gate_sha256, fee_ctx) -> dict:
    book = entry_book(gate, fee_ctx=fee_ctx)
    obj = {
        "schema": ENTRY_BOOK_SCHEMA,
        "entry_table": book["entry_table"],
        "entry_table_sha256": book["entry_table_sha256"],
        "gate_sha256": gate_sha256,
        "fee_admission": book["fee_admission"],
        "fee_source": book["fee_source"],
        "fee_source_sha256": book["fee_source_sha256"],
        "fee_formula_id": book["fee_formula_id"],
        "pnl_cd_sha256": module_sha256(),
        "python_version": sys.version,
        "platform": platform.platform(),
    }
    obj["output_sha256"] = envelope_output_sha256(obj)
    return obj


def _anchor_invalid(anchor) -> bool:
    if not isinstance(anchor, dict) or anchor.get("schema") != ANCHOR_SCHEMA:
        return True
    for field in _ANCHOR_SHA_FIELDS:
        if not _hex64(anchor.get(field)):
            return True
    if type(anchor.get("n_signals")) is not int:
        return True
    if not _iso_z(anchor.get("anchored_at_utc")):
        return True
    return False


def _anchor_window_detail(stamp):
    """BEFORE_EARLIEST, AT_OR_AFTER_CUTOFF, or None when the stamp is inside.

    _iso_z has already required the 20-character Z form, so the bounds compare
    as text: ANCHOR_EARLIEST_UTC <= stamp < ANCHOR_BEFORE_UTC.
    """
    if stamp < ANCHOR_EARLIEST_UTC:
        return "BEFORE_EARLIEST"
    if not stamp < ANCHOR_BEFORE_UTC:
        return "AT_OR_AFTER_CUTOFF"
    return None


def verify_entry_book_anchor(entry_book_bytes, anchor_doc, *, gate, gate_sha256, fee_ctx):
    """Outcome-free. First failure wins. Does not join.

    Returns (ok, kind, detail). detail is set only for a window miss.
    """
    if anchor_doc is None or entry_book_bytes is None:
        return False, "ENTRY_BOOK_ANCHOR_MISSING", None
    if _anchor_invalid(anchor_doc):
        return False, "ENTRY_BOOK_ANCHOR_INVALID", None
    detail = _anchor_window_detail(anchor_doc.get("anchored_at_utc"))
    if detail is not None:
        return False, "ENTRY_BOOK_ANCHOR_OUTSIDE_WINDOW", detail
    file_sha = hashlib.sha256(entry_book_bytes).hexdigest()
    if file_sha != anchor_doc["entry_book_file_sha256"]:
        return False, "ENTRY_BOOK_ANCHOR_MISMATCH", None
    try:
        parsed = json.loads(entry_book_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError):
        return False, "ENTRY_BOOK_ANCHOR_MISMATCH", None
    if not isinstance(parsed, dict):
        return False, "ENTRY_BOOK_ANCHOR_MISMATCH", None
    recomputed = envelope_output_sha256(parsed)
    if (
        recomputed != parsed.get("output_sha256")
        or recomputed != anchor_doc["entry_book_output_sha256"]
        or parsed.get("entry_table_sha256") != anchor_doc["entry_table_sha256"]
        or anchor_doc["gate_sha256"] != gate_sha256
    ):
        return False, "ENTRY_BOOK_ANCHOR_MISMATCH", None
    pin = load_fee_source_v2()
    if (
        pin is None
        or anchor_doc["fee_source_sha256"] != pin["sha256"]
        or anchor_doc.get("fee_formula_id") != pin["fee_formula_id"]
    ):
        return False, "ENTRY_BOOK_ANCHOR_MISMATCH", None
    fresh = entry_book(gate, fee_ctx=fee_ctx)
    if fresh["entry_table_sha256"] != anchor_doc["entry_table_sha256"]:
        return False, "ENTRY_BOOK_RECOMPUTE_MISMATCH", None
    return True, None, None


def make_anchor(entry_book_bytes, *, gate_sha256, anchored_at_utc) -> dict:
    parsed = json.loads(entry_book_bytes.decode("utf-8"))
    table = parsed.get("entry_table") or {}
    signals = table.get("signals")
    count = len(signals) if isinstance(signals, list) else 0
    return {
        "schema": ANCHOR_SCHEMA,
        "entry_book_file_sha256": hashlib.sha256(entry_book_bytes).hexdigest(),
        "entry_book_output_sha256": parsed.get("output_sha256"),
        "entry_table_sha256": parsed.get("entry_table_sha256"),
        "gate_sha256": gate_sha256,
        "fee_source_sha256": parsed.get("fee_source_sha256"),
        "fee_formula_id": parsed.get("fee_formula_id"),
        "pnl_cd_sha256": parsed.get("pnl_cd_sha256"),
        "n_signals": count,
        "anchored_at_utc": anchored_at_utc,
        "ruling_sha256": RULING_SHA256,
    }


def _canonical(obj) -> str:
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    ).hexdigest()


def _base_output(book, *, anchor_status, inputs, evaluated):
    out = {
        "schema": SCHEMA,
        "status": evaluated.get("status", book.get("status")),
        "fee_state": "ADMITTED" if book.get("fee_admission") == "ADMITTED_INDEX_ONLY" and book.get("status") != "BLOCKED_FEE_UNVERIFIED" else "BLOCKED_FEE_UNVERIFIED",
        "fee_admission": book.get("fee_admission"),
        "fee_block_reason": book.get("fee_block_reason"),
        "fee_source": book.get("fee_source"),
        "fee_source_sha256": book.get("fee_source_sha256"),
        "fee_source_accept_sha256": book.get("fee_source_accept_sha256"),
        "fee_formula_id": book.get("fee_formula_id"),
        "tick": str(TICK),
        "tick_basis": "RULED_61c1e4ea_(1)",
        "sensitivity_rows_status": SENSITIVITY_ROWS_STATUS,
        "fills_label": "simulated",
        "counts_toward_keep": False,
        "net_figure_label": NET_FIGURE_LABEL,
        "inputs_sha256": inputs,
        "entry_table_sha256": book.get("entry_table_sha256"),
        "entry_book_output_sha256": book.get("entry_book_output_sha256"),
        "entry_book_anchor_status": anchor_status,
        "module_sha256": module_sha256(),
        "governing_shas": list(GOVERNING_SHAS),
        "python_version": sys.version,
        "platform": platform.platform(),
        "n_signals": evaluated.get("n_signals"),
        "reject_c": evaluated.get("reject_c"),
        "reject_d": evaluated.get("reject_d"),
        "notes": list(evaluated.get("notes") or []),
        "reporting_defects": [_citation_defect()],
    }
    if evaluated.get("status") == "ADMITTED":
        pass
    return out


def _with_hash(out):
    defects = [item for item in out.get("reporting_defects") or [] if item.get("kind") != "CITATION_WORDING_NH001_CHECK"]
    out["reporting_defects"] = [_citation_defect(), *defects]
    out["output_sha256"] = score_body_sha256(out)
    return out


def _blocked_score(book, *, anchor_status, inputs):
    evaluated = {
        "status": "BLOCKED_FEE_UNVERIFIED",
        "n_signals": None,
        "reject_c": "BLOCKED_FEE_UNVERIFIED",
        "reject_d": "BLOCKED_FEE_UNVERIFIED",
        "notes": [],
    }
    out = _base_output(book, anchor_status=anchor_status, inputs=inputs, evaluated=evaluated)
    out["fee_state"] = "BLOCKED_FEE_UNVERIFIED"
    return _with_hash(out)


def _defect_score(book, kind, *, anchor_status, inputs, detail=None):
    evaluated = {
        "status": "REPORTING_DEFECT",
        "n_signals": None,
        "reject_c": None,
        "reject_d": None,
        "notes": [],
    }
    out = _base_output(book, anchor_status=anchor_status, inputs=inputs, evaluated=evaluated)
    out["fee_state"] = "ADMITTED" if book.get("fee_admission") == "ADMITTED_INDEX_ONLY" else "BLOCKED_FEE_UNVERIFIED"
    defect = {"kind": kind, "blocking": True}
    if detail is not None:
        defect["detail"] = detail
    out["reporting_defects"] = [
        _citation_defect(),
        defect,
    ]
    return _with_hash(out)


def _rows_outcome_free(rows):
    for row in rows:
        if _carries_outcome(row):
            raise OutcomePresent(OUTCOME_KEYS[0])


def _entry_book_block_reason(entry_book_bytes):
    """ENTRY_BOOK_ABSENT, ENTRY_BOOK_EMPTY, or None when a book is present."""
    if entry_book_bytes is None:
        return "ENTRY_BOOK_ABSENT"
    raw = entry_book_bytes.encode("utf-8") if isinstance(entry_book_bytes, str) else entry_book_bytes
    if not isinstance(raw, (bytes, bytearray)) or raw.strip() == b"":
        return "ENTRY_BOOK_ABSENT"
    try:
        parsed = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError):
        return None
    if parsed == {}:
        return "ENTRY_BOOK_EMPTY"
    return None


def _bare_rows(rows):
    bare = []
    for row in rows:
        if isinstance(row, dict):
            bare.append({key: value for key, value in row.items() if key not in OUTCOME_KEYS})
    return bare


def _signal_row_book_reason(gate, rows):
    """ENTRY_ROW_BOOK_MISSING when a signal has no two-sided row, else None.

    An empty signal list is vacuous. A deleted quote, a None quote, or a
    one-sided quote is missing. Production does not score those rows.
    """
    signals = gate.get("signals") if isinstance(gate, dict) else None
    if not isinstance(signals, list) or not signals:
        return None
    by_id = {}
    for row in rows:
        if isinstance(row, dict) and row.get("race_id") not in by_id:
            by_id[row.get("race_id")] = row
    for signal in signals:
        if not isinstance(signal, dict):
            return "ENTRY_ROW_BOOK_MISSING"
        row = by_id.get(signal.get("race_id"))
        if not isinstance(row, dict):
            return "ENTRY_ROW_BOOK_MISSING"
        if row.get("yes_bid") is None or row.get("yes_ask") is None:
            return "ENTRY_ROW_BOOK_MISSING"
    return None


def _signals_reproduced(gate, rows, fee_ctx):
    """True when gate_v2 on the outcome-stripped rows returns the same signals.

    Every admitted score re-runs gate_v2. There is no bookless skip.
    """
    if not isinstance(gate, dict) or not isinstance(fee_ctx, dict):
        return False
    pin = load_fee_source_v2()
    if pin is None:
        return False
    try:
        again = gate_v2(
            _bare_rows(rows),
            fee_source_path=fee_ctx.get("fee_source_path"),
            fee_source_id=gate.get("fee_source"),
            fee_source_sha256=pin["sha256"],
            packet_index_path=fee_ctx.get("packet_index_path"),
            fee_accept_path=fee_ctx.get("fee_accept_path"),
        )
    except (FeeBlocked, GateOutcomePresent, OutcomePresent, ValueError, TypeError):
        return False
    return (
        isinstance(again, dict)
        and again.get("status") == "OK"
        and again.get("signals") == gate.get("signals")
    )


def _label_nets(out):
    rows = out.get("per_signal")
    if not isinstance(rows, list):
        return out
    labelled = []
    for row in rows:
        if isinstance(row, dict):
            item = dict(row)
            item["net_label"] = NET_FIGURE_LABEL
            labelled.append(item)
        else:
            labelled.append(row)
    out["per_signal"] = labelled
    return out


def run(
    gate,
    rows,
    settled_results_loader,
    *,
    gate_sha256,
    entry_book_bytes,
    anchor_doc,
    fee_ctx,
    emit_buffered=False,
) -> dict:
    """Fee state, then the anchor, then the join. The loader runs only after both pass."""
    _rows_outcome_free(rows)
    book_reason = _entry_book_block_reason(entry_book_bytes)
    if book_reason is not None:
        inputs = {
            "gate_output": gate_sha256,
            "rows": _canonical(rows),
            "entry_book": None,
            "entry_book_anchor": None if anchor_doc is None else _canonical(anchor_doc),
            "settled_results": None,
            "fee_source": None,
            "packet_index": None,
            "fee_accept": None,
        }
        stub = {
            "status": "BLOCKED_FEE_UNVERIFIED",
            "fee_admission": "BLOCKED_FEE_UNVERIFIED",
            "fee_block_reason": book_reason,
            "fee_source": None,
            "fee_source_sha256": None,
            "fee_source_accept_sha256": None,
            "fee_formula_id": None,
            "entry_table_sha256": None,
            "entry_book_output_sha256": None,
            "fee_input_sha256": {},
        }
        out = _blocked_score(stub, anchor_status=book_reason, inputs=inputs)
        out["reporting_defects"] = [
            _citation_defect(),
            {"kind": book_reason, "blocking": True},
        ]
        return _with_hash(out)
    book = entry_book(gate, fee_ctx=fee_ctx)
    inputs = {
        "gate_output": gate_sha256,
        "rows": _canonical(rows),
        "entry_book": None if entry_book_bytes is None else hashlib.sha256(entry_book_bytes).hexdigest(),
        "entry_book_anchor": None if anchor_doc is None else _canonical(anchor_doc),
        "settled_results": None,
        "fee_source": (book.get("fee_input_sha256") or {}).get("fee_source"),
        "packet_index": (book.get("fee_input_sha256") or {}).get("packet_index"),
        "fee_accept": (book.get("fee_input_sha256") or {}).get("fee_accept"),
    }
    if book["status"] == "BLOCKED_FEE_UNVERIFIED":
        anchor_status = None
        if anchor_doc is not None or entry_book_bytes is not None:
            ok, kind, _detail = verify_entry_book_anchor(
                entry_book_bytes,
                anchor_doc,
                gate=gate,
                gate_sha256=gate_sha256,
                fee_ctx=fee_ctx,
            )
            anchor_status = "VERIFIED" if ok else kind
        return _blocked_score(book, anchor_status=anchor_status, inputs=inputs)
    ok, kind, detail = verify_entry_book_anchor(
        entry_book_bytes,
        anchor_doc,
        gate=gate,
        gate_sha256=gate_sha256,
        fee_ctx=fee_ctx,
    )
    if not ok:
        return _defect_score(book, kind, anchor_status=kind, inputs=inputs, detail=detail)
    if book["reporting_defects"]:
        return _defect_score(
            book,
            book["reporting_defects"][0]["kind"],
            anchor_status="VERIFIED",
            inputs=inputs,
        )
    if _duplicate_race_id(rows):
        return _defect_score(
            book,
            "DUPLICATE_RACE_ID",
            anchor_status="VERIFIED",
            inputs=inputs,
            detail="rows",
        )
    book_gap = _signal_row_book_reason(gate, rows)
    if book_gap is not None:
        out = _defect_score(book, book_gap, anchor_status="VERIFIED", inputs=inputs)
        out["status"] = "BLOCKED_FEE_UNVERIFIED"
        out["fee_block_reason"] = book_gap
        out["fee_state"] = "BLOCKED_FEE_UNVERIFIED"
        out["reject_c"] = "BLOCKED_FEE_UNVERIFIED"
        out["reject_d"] = "BLOCKED_FEE_UNVERIFIED"
        return _with_hash(out)
    if not _signals_reproduced(gate, rows, fee_ctx):
        out = _defect_score(book, "GATE_NOT_REPRODUCED", anchor_status="GATE_NOT_REPRODUCED", inputs=inputs)
        out["status"] = "GATE_NOT_REPRODUCED"
        out["fee_block_reason"] = "GATE_NOT_REPRODUCED"
        out["fee_state"] = "BLOCKED_FEE_UNVERIFIED"
        out["reject_c"] = "BLOCKED_FEE_UNVERIFIED"
        out["reject_d"] = "BLOCKED_FEE_UNVERIFIED"
        return _with_hash(out)
    settled_doc = settled_results_loader()
    inputs["settled_results"] = _canonical(settled_doc)
    joined = join_outcomes.join(rows, settled_doc)
    settled = settle(book, joined["rows"])
    evaluated = evaluate_cd(settled)
    out = _base_output(book, anchor_status="VERIFIED", inputs=inputs, evaluated=evaluated)
    out["fee_state"] = "ADMITTED"
    for field in (
        "per_signal",
        "net_headline_total",
        "net_one_tick_worse_total",
        "sum_positive_net",
        "max_positive_net",
        "top1_positive_share",
        "top1_positive_share_status",
        "top1_rule",
        "best_two_winners",
        "net_excluding_best_two_winners",
        "reject_c_at_ask",
        "reject_c_one_tick_worse",
        "reject_d_top1",
        "reject_d_drop_best_two",
        "unresolved_race_ids",
    ):
        if field in evaluated:
            out[field] = evaluated[field]
    _label_nets(out)
    if emit_buffered and evaluated.get("status") == "OK":
        per = []
        total = Decimal(0)
        for row in evaluated["per_signal"]:
            buffered = Decimal(row["net_headline"]) - BUFFER_2C
            total += buffered
            per.append({"race_id": row["race_id"], "net_buffered_2c": str(buffered)})
        out["sensitivity_buffered_2c"] = {
            "label": "DESCRIPTIVE_SENSITIVITY_BUFFERED_2C_NOT_VERDICT_INPUT",
            "verdict_input": False,
            "buffer": str(BUFFER_2C),
            "per_signal": per,
            "net_buffered_2c_total": str(total),
        }
    return _with_hash(out)


def _fee_ctx_from(args):
    return {
        "fee_source_path": args.fee_source,
        "packet_index_path": args.packet_index,
        "fee_accept_path": args.fee_accept,
    }


def main(argv):
    parser = argparse.ArgumentParser(prog="python -m card01_amc.pnl_cd")
    sub = parser.add_subparsers(dest="cmd", required=True)

    entry = sub.add_parser("entry-book")
    entry.add_argument("--gate", required=True)
    entry.add_argument("--fee-source", required=True)
    entry.add_argument("--packet-index", required=True)
    entry.add_argument("--fee-accept", required=True)
    entry.add_argument("--out", required=True)

    score = sub.add_parser("score")
    score.add_argument("--gate", required=True)
    score.add_argument("--rows", required=True)
    score.add_argument("--entry-book", required=True)
    score.add_argument("--entry-book-anchor", default=None)
    score.add_argument("--settled-results", required=True)
    score.add_argument("--fee-source", required=True)
    score.add_argument("--packet-index", required=True)
    score.add_argument("--fee-accept", required=True)
    score.add_argument("--emit-buffered-sensitivity", action="store_true")
    score.add_argument("--out", required=True)

    args = parser.parse_args(argv)

    def _ancestor_has_git(out_path) -> bool:
        current = Path(out_path)
        if not current.is_absolute():
            current = Path.cwd() / current
        current = current.resolve()
        for parent in (current, *current.parents):
            if (parent / ".git").exists():
                return True
        return False

    if _ancestor_has_git(args.out):
        print("OUTPUT_PATH_IN_REPO", file=sys.stderr)
        return 2
    try:
        gate_bytes = Path(args.gate).read_bytes()
        gate = json.loads(gate_bytes.decode("utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    gate_sha = hashlib.sha256(gate_bytes).hexdigest()
    fee_ctx = _fee_ctx_from(args)
    try:
        if args.cmd == "entry-book":
            envelope = entry_book_envelope(gate, gate_sha256=gate_sha, fee_ctx=fee_ctx)
            text = json.dumps(envelope, indent=1) + "\n"
            Path(args.out).write_text(text, encoding="utf-8")
            print(envelope["output_sha256"])
            print(envelope["entry_table_sha256"])
            return 0
        row_bytes = Path(args.rows).read_bytes()
        rows_doc = json.loads(row_bytes.decode("utf-8"))
        rows = rows_doc["rows"] if isinstance(rows_doc, dict) and "rows" in rows_doc else rows_doc
        entry_book_bytes = Path(args.entry_book).read_bytes()
        anchor_doc = None
        if args.entry_book_anchor:
            anchor_bytes = Path(args.entry_book_anchor).read_bytes()
            anchor_doc = json.loads(anchor_bytes.decode("utf-8"))
        settled_path = args.settled_results

        def _load_settled():
            blob = Path(settled_path).read_bytes()
            return json.loads(blob.decode("utf-8"))

        out = run(
            gate,
            rows,
            _load_settled,
            gate_sha256=gate_sha,
            entry_book_bytes=entry_book_bytes,
            anchor_doc=anchor_doc,
            fee_ctx=fee_ctx,
            emit_buffered=args.emit_buffered_sensitivity,
        )
    except OutcomePresent as exc:
        print(str(exc), file=sys.stderr)
        return 2
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    Path(args.out).write_text(json.dumps(out, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print(out["output_sha256"])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
