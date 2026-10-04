"""AF-8 outcome-free input builder.

Emits exactly the frozen universe, in that order. state is the USPS two-letter
code equal to the universe code's first two characters. Rows are never dropped.
"""
from __future__ import annotations

import json
import math
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

from card01_amc.pinload import UNIVERSE_SHA256, sha256_bytes

DECISION_SNAPSHOT_UTC = "2026-11-02T22:00:00Z"
BOOK_WINDOW_START_UTC = "2026-11-02T21:45:00Z"
BOOK_WINDOW_END_UTC = "2026-11-02T22:15:00Z"
FORECAST_EARLIEST_UTC = "2026-10-25T22:00:00Z"
FORECAST_LATEST_UTC = "2026-11-01T22:00:00Z"
BOOK_MAX_DISTANCE_SECONDS = 15 * 60

CODE_RE = re.compile(r"^[A-Z]{2}-\d{2}$")
STATE_RE = re.compile(r"^[A-Z]{2}$")
OUTCOME_KEYS = ("y", "result", "settlement", "outcome", "settled")
OPEN_MARKET = ("active", "open")


class BuilderError(RuntimeError):
    pass


class OutcomeKeyRefused(BuilderError):
    pass


def module_sha256() -> str:
    return sha256_bytes(Path(__file__).read_bytes())


def parse_utc(value: str) -> datetime:
    if not isinstance(value, str):
        raise ValueError("timestamp must be a string")
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        raise ValueError("timezone required")
    return dt.astimezone(timezone.utc)


def _try_parse(value):
    try:
        return parse_utc(value)
    except (TypeError, ValueError):
        return None


def _walk_outcome_keys(obj):
    if isinstance(obj, dict):
        for key, val in obj.items():
            if key in OUTCOME_KEYS:
                raise OutcomeKeyRefused(key)
            _walk_outcome_keys(val)
    elif isinstance(obj, list):
        for val in obj:
            _walk_outcome_keys(val)


def _mapping_table(mapping):
    if isinstance(mapping, list):
        races = mapping
    elif isinstance(mapping, dict):
        races = mapping.get("races") or []
    else:
        raise BuilderError("mapping must be a list or an object with races")
    by = {}
    for row in races:
        if isinstance(row, dict) and row.get("race") is not None:
            by[row["race"]] = row
    return by


def _forecast_table(forecast):
    rows = forecast.get("rows") if isinstance(forecast, dict) else None
    if not isinstance(rows, list):
        raise BuilderError("forecast.rows must be a list")
    by = {}
    conflict = set()
    for row in rows:
        if not isinstance(row, dict):
            continue
        code = row.get("race_code")
        if code in by:
            conflict.add(code)
        by[code] = row
    fetched = _try_parse(forecast.get("source_fetched_at_utc") if isinstance(forecast, dict) else None)
    earliest = parse_utc(FORECAST_EARLIEST_UTC)
    latest = parse_utc(FORECAST_LATEST_UTC)
    file_ok = fetched is not None and earliest <= fetched <= latest
    return by, conflict, file_ok


def _model(code, by, conflict, file_ok):
    if not file_ok or code in conflict or code not in by:
        return None
    row = by[code]
    if row.get("dem_name") == "(No Democrat)":
        return None
    dem = row.get("dem_prob")
    if isinstance(dem, bool) or not isinstance(dem, (int, float)):
        return None
    if not math.isfinite(float(dem)) or not 0 <= float(dem) <= 100:
        return None
    return float(dem) / 100.0


def _snapshots_by_ticker(book):
    snaps = book.get("snapshots") if isinstance(book, dict) else None
    if not isinstance(snaps, list):
        raise BuilderError("book.snapshots must be a list")
    return snaps


def _select_snapshot(snaps, ticker):
    start = parse_utc(BOOK_WINDOW_START_UTC)
    end = parse_utc(BOOK_WINDOW_END_UTC)
    decision = parse_utc(DECISION_SNAPSHOT_UTC)
    chosen = None
    chosen_key = None
    for snap in snaps:
        if not isinstance(snap, dict) or snap.get("ticker") != ticker:
            continue
        at = _try_parse(snap.get("received_at_utc"))
        if at is None or not (start <= at <= end):
            continue
        distance = abs((at - decision).total_seconds())
        if distance > BOOK_MAX_DISTANCE_SECONDS:
            continue
        key = (distance, at)
        if chosen_key is None or key < chosen_key:
            chosen = snap
            chosen_key = key
    return chosen


def _book_problem(snap):
    bid = snap.get("yes_bid")
    ask = snap.get("yes_ask")
    if bid is None or ask is None:
        return "no_two_sided_book"
    if isinstance(bid, bool) or isinstance(ask, bool):
        return "no_two_sided_book"
    if not isinstance(bid, (int, float)) or not isinstance(ask, (int, float)):
        return "no_two_sided_book"
    if not math.isfinite(float(bid)) or not math.isfinite(float(ask)):
        return "no_two_sided_book"
    if float(bid) > float(ask) or float(bid) <= 0 or float(ask) >= 1:
        return "no_two_sided_book"
    return None


def _classify_mapping(entry):
    if not isinstance(entry, dict) or entry.get("status") != "mapped":
        return "UNRESOLVED", None, None, "mapping_unresolved"
    series = entry.get("series")
    ticker = entry.get("chosen_ticker")
    if series == "KXHOUSERACE":
        return "KXHOUSERACE", series, ticker, None
    if isinstance(series, str) and series:
        return "LEGACY", series, ticker, None
    return "UNRESOLVED", None, ticker, "mapping_unresolved"


def _quote_fields(snap):
    if snap is None:
        return None, None, None, None
    return snap.get("yes_bid"), snap.get("yes_ask"), snap.get("yes_bid_qty"), snap.get("yes_ask_qty")


def build(universe, forecast, mapping, book, input_shas):
    """Return the builder object. input_shas maps universe/forecast/mapping/book to hex."""
    if input_shas.get("universe") != UNIVERSE_SHA256:
        raise BuilderError("universe sha mismatch")
    for doc in (universe, forecast, mapping, book):
        _walk_outcome_keys(doc)
    codes = universe.get("universe_2026_house") if isinstance(universe, dict) else None
    if not isinstance(codes, list) or len(codes) != 92:
        raise BuilderError("universe must contain 92 codes")
    for code in codes:
        if not isinstance(code, str) or CODE_RE.fullmatch(code) is None:
            raise BuilderError("universe code is not XX-NN")
    states = {code[:2] for code in codes}
    if len(states) != 28 or any(STATE_RE.fullmatch(s) is None for s in states):
        raise BuilderError("universe states are not 28 USPS2 codes")

    map_by = _mapping_table(mapping)
    fc_by, fc_conflict, file_ok = _forecast_table(forecast)
    snaps = _snapshots_by_ticker(book)

    rows = []
    exclusions = []
    for code in codes:
        state = code[:2]
        mapping_status, series, ticker, map_reason = _classify_mapping(map_by.get(code))
        p_model = _model(code, fc_by, fc_conflict, file_ok)
        forecast_reason = None if p_model is not None else "no_admissible_forecast"
        snap = _select_snapshot(snaps, ticker) if ticker else None
        reasons = []
        if map_reason:
            reasons.append(map_reason)
        if forecast_reason:
            reasons.append(forecast_reason)
        if snap is None:
            reasons.append("snapshot_outside_window")
        else:
            status = str(snap.get("market_status") or "").lower()
            if status not in OPEN_MARKET:
                reasons.append("market_closed_or_settled")
            problem = _book_problem(snap)
            if problem:
                reasons.append(problem)
        exclusion = reasons[0] if reasons else None
        bid, ask, bid_qty, ask_qty = _quote_fields(snap)
        if exclusion is None:
            p_market = (float(bid) + float(ask)) / 2.0
            model_out = p_model
        else:
            p_market = None
            model_out = None
            exclusions.append({"race_id": code, "reason": exclusion})
        rows.append({
            "race_id": code,
            "state": state,
            "mapping_status": mapping_status,
            "series": series,
            "p_market": p_market,
            "p_model": model_out,
            "y": None,
            "ticker": ticker,
            "yes_bid": bid,
            "yes_ask": ask,
            "yes_bid_qty": bid_qty,
            "yes_ask_qty": ask_qty,
            "exclusion_reason": exclusion,
        })
    return {
        "rows": rows,
        "builder_sha256": module_sha256(),
        "inputs_sha256": {
            "universe": input_shas["universe"],
            "forecast": input_shas["forecast"],
            "mapping": input_shas["mapping"],
            "book": input_shas["book"],
        },
        "exclusions": exclusions,
    }


def dumps(obj) -> str:
    return json.dumps(obj, indent=1)


def build_paths(universe_path, forecast_path, mapping_path, book_path):
    blobs = {
        "universe": Path(universe_path).read_bytes(),
        "forecast": Path(forecast_path).read_bytes(),
        "mapping": Path(mapping_path).read_bytes(),
        "book": Path(book_path).read_bytes(),
    }
    docs = {key: json.loads(blobs[key]) for key in blobs}
    shas = {key: sha256_bytes(blobs[key]) for key in blobs}
    return build(docs["universe"], docs["forecast"], docs["mapping"], docs["book"], shas)


def main(argv):
    if len(argv) != 4:
        print("usage: python -m card01_amc.build_rows universe.json forecast.json mapping.json book.json", file=sys.stderr)
        return 2
    try:
        obj = build_paths(*argv)
    except (BuilderError, json.JSONDecodeError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    json.dump(obj, sys.stdout, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
