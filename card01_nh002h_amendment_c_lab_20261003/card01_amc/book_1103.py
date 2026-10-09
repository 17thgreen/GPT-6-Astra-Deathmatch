"""11-03 adverse selection from a normalized book.

The raw order-book adapter is out of scope. Null labels are the four ruled
statuses. Nothing is carried forward from an earlier book.
"""
from __future__ import annotations

import math
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_EVEN

WINDOW_START = datetime(2026, 11, 3, 21, 45, 0, tzinfo=timezone.utc)
WINDOW_END = datetime(2026, 11, 3, 22, 15, 0, tzinfo=timezone.utc)
TARGET = datetime(2026, 11, 3, 22, 0, 0, tzinfo=timezone.utc)
OPEN_STATUS = frozenset({"active", "open"})
LABELS = (
    "MARKET_NOT_OPEN_AT_T",
    "NOT_CAPTURED",
    "NOT_CAPTURED_EGRESS_CLOSED",
    "NO_TWO_SIDED_BOOK_IN_WINDOW",
)
_MEAN = Decimal("0.0001")


def _parse_utc(text):
    if not isinstance(text, str) or not text:
        return None
    for fmt in ("%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ"):
        try:
            return datetime.strptime(text, fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    return None


def _abs_us(ts):
    delta = ts - TARGET
    us = delta.days * 86_400_000_000 + delta.seconds * 1_000_000 + delta.microseconds
    if us < 0:
        return -us
    return us


def _nearest(pairs):
    best = None
    best_key = None
    for ts, snap in pairs:
        key = (_abs_us(ts), ts)
        if best_key is None or key < best_key:
            best_key = key
            best = snap
    return best


def _number(value):
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value, (int, float, Decimal, str)):
        try:
            number = float(value)
        except (TypeError, ValueError):
            return None
        if not math.isfinite(number):
            return None
        return number
    return None


def _kind(snap):
    bid = _number(snap.get("yes_bid"))
    ask = _number(snap.get("yes_ask"))
    if bid is None and ask is None:
        return "both"
    if bid is None:
        return "bid"
    if ask is None:
        return "ask"
    if 0 < bid <= ask < 1:
        return "two_sided"
    return "crossed_or_out_of_range"


def _open(snap) -> bool:
    return str(snap.get("market_status") or "").lower() in OPEN_STATUS


def _missing_side(kinds):
    bad = [kind for kind in kinds if kind != "two_sided"]
    if not bad:
        return "crossed_or_out_of_range"
    first = bad[0]
    for kind in bad:
        if kind != first:
            return "both"
    return first


def book_status(book) -> str:
    """Capture label. A missing book is egress-closed. {} is an empty book."""
    if not isinstance(book, dict) or book.get("capture_status") == "NOT_CAPTURED_EGRESS_CLOSED":
        return "NOT_CAPTURED_EGRESS_CLOSED"
    if not book:
        return "ENTRY_BOOK_EMPTY"
    return "OK"


def _blank_counts():
    return {label: 0 for label in LABELS}


def quote_for_ticker(book, ticker):
    """One 11-03 quote, or a null label. Outside-window snapshots are ignored."""
    status = book_status(book)
    if status != "OK":
        return {"status": status, "yes_mid": None}
    snaps = book.get("snapshots") if isinstance(book, dict) else None
    in_window = []
    if isinstance(snaps, list):
        for snap in snaps:
            if not isinstance(snap, dict) or snap.get("ticker") != ticker:
                continue
            ts = _parse_utc(snap.get("received_at_utc"))
            if ts is None or ts < WINDOW_START or ts > WINDOW_END:
                continue
            in_window.append((ts, snap))
    if not in_window:
        return {"status": "NOT_CAPTURED", "yes_mid": None}
    nearest = _nearest(in_window)
    if not _open(nearest):
        return {
            "status": "MARKET_NOT_OPEN_AT_T",
            "market_status_verbatim": nearest.get("market_status"),
            "yes_mid": None,
        }
    two_sided = []
    kinds = []
    for ts, snap in in_window:
        kind = _kind(snap)
        kinds.append(kind)
        if kind == "two_sided" and _open(snap):
            two_sided.append((ts, snap))
    if not two_sided:
        return {
            "status": "NO_TWO_SIDED_BOOK_IN_WINDOW",
            "no_two_sided_detail": {
                "missing_side": _missing_side(kinds),
                "n_captures": len(in_window),
            },
            "yes_mid": None,
        }
    chosen = _nearest(two_sided)
    bid = Decimal(repr(_number(chosen.get("yes_bid"))))
    ask = Decimal(repr(_number(chosen.get("yes_ask"))))
    return {"status": "OK", "yes_mid": (bid + ask) / 2}


def _money(value):
    if isinstance(value, Decimal):
        return value
    if isinstance(value, float):
        return Decimal(repr(value))
    return Decimal(str(value))


def _side_value(yes_mid, side):
    if side == "D_NO":
        return Decimal(1) - yes_mid
    return yes_mid


def _cents(mid_side, fill):
    return (mid_side - fill) * Decimal(-1) * Decimal(100)


def _aggregate(values):
    defined = [item for item in values if item["status"] == "OK"]
    counts = _blank_counts()
    for item in values:
        status = item["status"]
        if status in counts:
            counts[status] += 1
    if not defined:
        return {
            "n_defined": 0,
            "n_missing": len(values),
            "n_missing_by_label": counts,
            "sum_cents": "0",
            "mean_cents": None,
            "per_signal": values,
        }
    total = Decimal(0)
    for item in defined:
        total += Decimal(item["value"])
    mean = (total / Decimal(len(defined))).quantize(_MEAN, rounding=ROUND_HALF_EVEN)
    return {
        "n_defined": len(defined),
        "n_missing": len(values) - len(defined),
        "n_missing_by_label": counts,
        "sum_cents": str(total),
        "mean_cents": str(mean),
        "per_signal": values,
    }


def _row_of(signal, rows_by_id):
    row = rows_by_id.get(signal.get("race_id"))
    return row if isinstance(row, dict) else {}


def adverse_selection(signals, rows_by_id, book):
    """Simulated-fill adverse selection. Buys only. +60s and +300s stay uncaptured."""
    plus = []
    settlement = []
    for signal in signals:
        row = _row_of(signal, rows_by_id)
        ticker = row.get("ticker") or signal.get("ticker")
        quote = quote_for_ticker(book, ticker)
        fill = _money(signal.get("price"))
        side = signal.get("side")
        record = {"race_id": signal.get("race_id"), "status": quote["status"], "value": None}
        if quote["status"] == "OK":
            record["value"] = str(_cents(_side_value(quote["yes_mid"], side), fill))
        if "market_status_verbatim" in quote:
            record["market_status_verbatim"] = quote["market_status_verbatim"]
        if "no_two_sided_detail" in quote:
            record["no_two_sided_detail"] = quote["no_two_sided_detail"]
        plus.append(record)
        y = row.get("y")
        settled = {"race_id": signal.get("race_id"), "status": "OK", "value": None}
        if y not in (0, 1):
            settled["status"] = "INPUT_MISSING:y"
        else:
            mid = Decimal(y) if side == "D_YES" else Decimal(1) - Decimal(y)
            settled["value"] = str(_cents(mid, fill))
        settlement.append(settled)
    return {
        "book_1103_status": book_status(book),
        "plus_24h": _aggregate(plus),
        "settlement": _aggregate(settlement),
        "plus_60s": None,
        "plus_60s_status": "NOT_CAPTURED",
        "plus_300s": None,
        "plus_300s_status": "NOT_CAPTURED",
        "freeze_named": True,
        "class": "DISPLAY-ONLY",
    }
