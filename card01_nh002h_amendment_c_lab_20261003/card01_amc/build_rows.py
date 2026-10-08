"""AF-8 outcome-free input builder.

Emits exactly the frozen universe, in that order. state is the USPS two-letter
code equal to the universe code's first two characters. Rows are never dropped.
A selected forecast is priced only after the sha-checked dem_name step accepts it.
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from card01_amc.dem_name_step import ADD_DEM_NAME_SHA256, run_dem_name_step
from card01_amc.pinload import UNIVERSE_SHA256, sha256_bytes

DECISION_SNAPSHOT_UTC = "2026-11-02T22:00:00Z"
BOOK_WINDOW_START_UTC = "2026-11-02T21:45:00Z"
BOOK_WINDOW_END_UTC = "2026-11-02T22:15:00Z"
FORECAST_EARLIEST_UTC = "2026-10-25T22:00:00Z"
FORECAST_LATEST_UTC = "2026-11-01T22:00:00Z"
BOOK_MAX_DISTANCE_SECONDS = 15 * 60

CODE_RE = re.compile(r"^[A-Z]{2}-\d{2}$")
STATE_RE = re.compile(r"^[A-Z]{2}$")
NO_DEMOCRAT_RE = re.compile(r"^\(no democrat\b", re.IGNORECASE)
Q5_STATUS = "UNAVAILABLE_NEEDS_EGRESS"
DEGENERATE_BLOCK = "INCONCLUSIVE_DEGENERATE_BLOCK"
OUTCOME_KEYS = ("y", "result", "settlement", "outcome", "settled")
OPEN_MARKET = ("active", "open")


class BuilderError(RuntimeError):
    pass


class OutcomeKeyRefused(BuilderError):
    pass


def module_sha256() -> str:
    return sha256_bytes(Path(__file__).read_bytes())


def q5_orderbook_status() -> str:
    """Q5 is deferred. This does not fetch or parse an order book."""
    return Q5_STATUS


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
    if forecast is None:
        return {}, set(), False
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


def _blank_ticker(ticker) -> bool:
    return ticker is None or ticker == ""


def _model(code, by, conflict, file_ok):
    if not file_ok or code in conflict or code not in by:
        return None
    row = by[code]
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


def _public_step(step):
    step = step or {}
    return {
        "status": step.get("status"),
        "reason": step.get("reason"),
        "expected_script_sha256": step.get("expected_script_sha256", ADD_DEM_NAME_SHA256),
        "observed_script_sha256": step.get("observed_script_sha256"),
        "original_sha256": step.get("original_sha256"),
        "v1_sha256": step.get("v1_sha256"),
        "check": step.get("check"),
    }


def _step_not_run():
    return _public_step({
        "status": "DEM_NAME_STEP_REFUSED",
        "reason": "STEP_NOT_RUN",
        "expected_script_sha256": ADD_DEM_NAME_SHA256,
    })


def _name_flags(v1_row):
    flags = {"no_democrat": None, "same_party_s5": None, "dem_name_resolved": False}
    codes = []
    if not isinstance(v1_row, dict):
        codes.append("DEM_NAME_UNRESOLVED")
        return codes, flags
    name = v1_row.get("dem_name")
    status = v1_row.get("dem_name_status")
    s5 = v1_row.get("same_party_excluded_s5")
    if isinstance(name, str):
        flags["no_democrat"] = NO_DEMOCRAT_RE.match(name) is not None
    if isinstance(s5, bool):
        flags["same_party_s5"] = s5
    flags["dem_name_resolved"] = status == "RESOLVED" and name is not None and isinstance(s5, bool)
    if flags["no_democrat"] is True:
        codes.append("NO_DEMOCRAT")
    if s5 is True:
        codes.append("SAME_PARTY_S5")
    if name is None or status != "RESOLVED" or not isinstance(s5, bool):
        codes.append("DEM_NAME_UNRESOLVED")
    return codes, flags


def _v1_index(step):
    if not isinstance(step, dict) or step.get("status") != "DEM_NAME_ACCEPTED":
        return None
    v1 = step.get("v1")
    rows = v1.get("rows") if isinstance(v1, dict) else None
    if not isinstance(rows, list):
        return {}
    found = {}
    for row in rows:
        if isinstance(row, dict) and row.get("race_code") not in found:
            found[row.get("race_code")] = row
    return found


def build(universe, forecast, mapping, book, input_shas, *, selection, dem_name_step=None):
    """Return the builder object. input_shas maps universe/forecast/mapping/book/selection to hex."""
    if not isinstance(selection, dict):
        raise BuilderError("selection is required")
    if input_shas.get("universe") != UNIVERSE_SHA256:
        raise BuilderError("universe sha mismatch")
    status = selection.get("status")
    if status == "SELECTED":
        if forecast is None:
            raise BuilderError("FORECAST_REQUIRED")
        if input_shas.get("forecast") != selection.get("selected_derived_sha256"):
            raise BuilderError("FORECAST_SHA_MISMATCH")
    elif forecast is not None:
        raise BuilderError("FORECAST_NOT_SELECTED")
    for doc in (universe, forecast, mapping, book, selection):
        if doc is not None:
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

    if status != "SELECTED":
        forecast = None
        dem_name_step = _step_not_run()
    elif dem_name_step is None:
        dem_name_step = _step_not_run()
    step_ok = isinstance(dem_name_step, dict) and dem_name_step.get("status") == "DEM_NAME_ACCEPTED"
    v1_by = _v1_index(dem_name_step) if step_ok else None

    map_by = _mapping_table(mapping)
    fc_by, fc_conflict, file_ok = _forecast_table(forecast)
    snaps = _snapshots_by_ticker(book)

    rows = []
    exclusions = []
    for code in codes:
        state = code[:2]
        mapping_status, series, ticker, map_reason = _classify_mapping(map_by.get(code))
        p_model = _model(code, fc_by, fc_conflict, file_ok)
        file_level = not file_ok
        per_race = file_ok and p_model is None
        reasons = []
        flags = {"no_democrat": None, "same_party_s5": None, "dem_name_resolved": False}
        if map_reason:
            reasons.append(map_reason)
        if file_level:
            reasons.append("no_admissible_forecast")
        elif step_ok:
            name_codes, flags = _name_flags(None if v1_by is None else v1_by.get(code))
            reasons.extend(name_codes)
        elif p_model is not None:
            reasons.append("DEM_NAME_UNRESOLVED")
        if per_race and "no_admissible_forecast" not in reasons:
            reasons.append("no_admissible_forecast")
        snap = None if _blank_ticker(ticker) else _select_snapshot(snaps, ticker)
        if mapping_status in ("KXHOUSERACE", "LEGACY") and _blank_ticker(ticker):
            reasons.append("no_ticker_for_mapped_race")
        elif snap is None:
            reasons.append("snapshot_outside_window")
        else:
            market = str(snap.get("market_status") or "").lower()
            if market not in OPEN_MARKET:
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
            exclusions.append({"race_id": code, "reason": exclusion, "reasons": list(reasons)})
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
            "exclusion_reasons": reasons,
            "dem_name_flags": flags,
        })
    refused = (
        isinstance(dem_name_step, dict)
        and dem_name_step.get("status") == "DEM_NAME_STEP_REFUSED"
    )
    return {
        "rows": rows,
        "builder_sha256": module_sha256(),
        "q6_status": status,
        "dem_name_step": _public_step(dem_name_step),
        "closed_result": DEGENERATE_BLOCK if refused else None,
        "q5_status": q5_orderbook_status(),
        "inputs_sha256": {
            "universe": input_shas.get("universe"),
            "forecast": input_shas.get("forecast"),
            "mapping": input_shas.get("mapping"),
            "book": input_shas.get("book"),
            "selection": input_shas.get("selection"),
        },
        "exclusions": exclusions,
    }


def dumps(obj) -> str:
    return json.dumps(obj, indent=1)


def _load(path):
    raw = Path(path).read_bytes()
    return json.loads(raw), raw


def build_cli(universe_path, selection_path, forecast_path, mapping_path, book_path, add_dem_name, dem_name_out_dir):
    universe, universe_raw = _load(universe_path)
    selection, selection_raw = _load(selection_path)
    mapping, mapping_raw = _load(mapping_path)
    book, book_raw = _load(book_path)
    forecast = None
    forecast_raw = None
    if forecast_path:
        forecast, forecast_raw = _load(forecast_path)
    codes = universe.get("universe_2026_house") if isinstance(universe, dict) else []
    step = None
    if isinstance(selection, dict) and selection.get("status") == "SELECTED" and forecast_path:
        if add_dem_name:
            out_dir = dem_name_out_dir or tempfile.mkdtemp()
            step = run_dem_name_step(
                add_dem_name,
                forecast_path,
                out_dir,
                universe_codes=codes,
            )
    shas = {
        "universe": sha256_bytes(universe_raw),
        "forecast": sha256_bytes(forecast_raw) if forecast_raw is not None else None,
        "mapping": sha256_bytes(mapping_raw),
        "book": sha256_bytes(book_raw),
        "selection": sha256_bytes(selection_raw),
    }
    return build(universe, forecast, mapping, book, shas, selection=selection, dem_name_step=step)


def main(argv):
    parser = argparse.ArgumentParser(description="outcome-free row builder")
    parser.add_argument("--universe", required=True)
    parser.add_argument("--selection", required=True)
    parser.add_argument("--forecast", default=None)
    parser.add_argument("--mapping", required=True)
    parser.add_argument("--book", required=True)
    parser.add_argument("--add-dem-name", default=None)
    parser.add_argument("--dem-name-out-dir", default=None)
    args = parser.parse_args(argv)
    try:
        obj = build_cli(
            args.universe,
            args.selection,
            args.forecast,
            args.mapping,
            args.book,
            args.add_dem_name,
            args.dem_name_out_dir,
        )
    except (BuilderError, json.JSONDecodeError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    json.dump(obj, sys.stdout, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
