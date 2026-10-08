"""Q6 strict forecast-file selector.

No step-back. Paths in the record are relative to the capture root. The
derived-file rebuild hook is injected; the command line has none, and a
derived sha mismatch then fails closed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

from card01_amc.pinload import sha256_bytes

WINDOW_START = "2026-10-25T22:00:00Z"
WINDOW_END = "2026-11-01T22:00:00Z"
DECISION = "2026-11-02T22:00:00Z"
CSV_URL = "https://raw.githubusercontent.com/ElectIndex/26_us_forecast_data/main/output/races_summary.csv"
CARD = "card01-NH002-H"
R0 = "caaff53e739413a8340f0addbec7136ec1995195291cab61889a94c1286ea87f"
UNIVERSE_SHA = "d8af74515e449b151016105f956c5e54a4fb4eac3ec570364da58f8fe47d8ca6"
RULE_DOC_SHA256 = "5535ff2a60223587bef9b9f3a0d981f01387ca57cf23e02a0bc2e6d991d6ac0c"
OUTCOME_KEYS = ("y", "result", "settlement", "outcome", "settled")
FLAG_ORDER = ("TIE_IDENTICAL_SHA", "DERIVED_REBUILT_MATCH", "DERIVED_REBUILD_UNAVAILABLE")
SAFE_GAP_KEYS = ("start_utc", "end_utc", "from_utc", "to_utc", "note", "gap")


class OutcomeKeyRefused(RuntimeError):
    pass


class SelectorError(RuntimeError):
    pass


def module_sha256() -> str:
    return sha256_bytes(Path(__file__).read_bytes())


def parse_utc(value):
    if not isinstance(value, str):
        raise ValueError("timestamp must be a string")
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        raise ValueError("timezone required")
    return dt.astimezone(timezone.utc)


def _walk_outcome_keys(obj):
    if isinstance(obj, dict):
        for key, val in obj.items():
            if key in OUTCOME_KEYS:
                raise OutcomeKeyRefused(key)
            _walk_outcome_keys(val)
    elif isinstance(obj, list):
        for val in obj:
            _walk_outcome_keys(val)


def _relpath(value):
    if not isinstance(value, str) or value == "":
        return None
    path = Path(value)
    if path.is_absolute() or ".." in path.parts:
        return None
    return path.as_posix()


def _classify(record):
    if record.get("status") != 200:
        return "NON_200"
    if record.get("attempt") != 1:
        return "ATTEMPT_NOT_1"
    try:
        fetched = parse_utc(record.get("fetched_at_utc"))
    except (TypeError, ValueError):
        return "TIMESTAMP_INVALID"
    if fetched > parse_utc(WINDOW_END):
        return "LATE"
    if fetched < parse_utc(WINDOW_START):
        return "STALE"
    if record.get("url") != CSV_URL:
        return "URL_MISMATCH"
    return "IN_WINDOW"


def _parse_jsonl(raw, corrupt_status):
    if raw is None:
        return None, []
    text = raw.decode("utf-8")
    lines = text.splitlines()
    records = []
    for line_no, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            raise SelectorError(corrupt_status) from None
        if not isinstance(obj, dict):
            raise SelectorError(corrupt_status)
        _walk_outcome_keys(obj)
        records.append((line_no, obj))
    return lines, records


def _read_file(root, rel, files):
    if rel is None:
        return None
    if files is not None:
        data = files.get(rel)
        return data if isinstance(data, (bytes, bytearray)) else None
    path = Path(root) / rel
    if not path.is_file():
        return None
    return path.read_bytes()


def _runner_index(records):
    found = {}
    for _line_no, row in records:
        run_id = row.get("run_id")
        if run_id is not None and run_id not in found and isinstance(row.get("runner_sha256"), str):
            found[run_id] = row["runner_sha256"]
    return found


def _regime_table(method_rows):
    ordered = []
    for line_no, row in method_rows:
        try:
            stamp = parse_utc(row.get("fetched_at_utc"))
        except (TypeError, ValueError):
            stamp = datetime.max.replace(tzinfo=timezone.utc)
        ordered.append((stamp, line_no, row))
    ordered.sort(key=lambda item: (item[0], item[1]))
    table = []
    labels = {}
    rank = 0
    for _stamp, line_no, row in ordered:
        digest = row.get("methodology_asset_sha256")
        if not isinstance(digest, str) or digest in labels:
            continue
        if digest == R0:
            label = "R0"
        else:
            rank += 1
            label = "R" + str(rank)
        labels[digest] = label
        table.append({
            "label": label,
            "methodology_asset_sha256": digest,
            "first_seen_fetched_at_utc": row.get("fetched_at_utc"),
            "line_no": line_no,
        })
    return table, labels


def _asset_for(record, method_rows):
    matches = []
    for line_no, row in method_rows:
        if record.get("run_id") is not None:
            if row.get("run_id") == record.get("run_id"):
                matches.append((line_no, row))
        elif row.get("capture_date_utc") == record.get("capture_date_utc"):
            matches.append((line_no, row))
    if not matches:
        return None
    return min(matches, key=lambda item: item[0])


def _regime_of(record, method_rows, labels):
    asset = _asset_for(record, method_rows)
    if asset is None:
        return {
            "label": "UNMONITORED",
            "methodology_asset_sha256": None,
            "methodology_asset_line_no": None,
            "methodology_text_sha256": None,
            "regime_changed_since_freeze": True,
        }
    line_no, row = asset
    digest = row.get("methodology_asset_sha256")
    label = labels.get(digest, "UNMONITORED")
    return {
        "label": label,
        "methodology_asset_sha256": digest if isinstance(digest, str) else None,
        "methodology_asset_line_no": line_no,
        "methodology_text_sha256": row.get("methodology_text_sha256"),
        "regime_changed_since_freeze": label != "R0",
    }


def _empty_regime():
    return {
        "label": None,
        "methodology_asset_sha256": None,
        "methodology_asset_line_no": None,
        "methodology_text_sha256": None,
        "regime_changed_since_freeze": None,
    }


def _pick(window):
    """Return (record, flags) or a status string when the tie is ambiguous."""
    if not window:
        return "FORECAST_FILE_MISSING", None, []
    stamps = []
    for line_no, row in window:
        stamps.append(parse_utc(row["fetched_at_utc"]))
    t_max = max(stamps)
    tied = [(line_no, row) for line_no, row in window if parse_utc(row["fetched_at_utc"]) == t_max]
    flags = []
    if len(tied) > 1:
        shas = {row.get("sha256") for _line, row in tied}
        if len(shas) == 1:
            flags.append("TIE_IDENTICAL_SHA")
            tied = [min(tied, key=lambda item: item[0])]
        else:
            return "FORECAST_FILE_AMBIGUOUS", None, []
    return None, tied[0], flags


def _integrity(record, root, files, runners, rebuild_derived):
    flags = []
    rel = _relpath(record.get("raw_path_private"))
    if rel is None:
        return "FORECAST_FILE_CORRUPT", "PATH_NOT_RELATIVE" if isinstance(record.get("raw_path_private"), str) else "RAW_MISSING", None, flags
    raw = _read_file(root, rel, files)
    if raw is None:
        return "FORECAST_FILE_CORRUPT", "RAW_MISSING", None, flags
    if sha256_bytes(raw) != record.get("sha256"):
        return "FORECAST_FILE_CORRUPT", "RAW_SHA_MISMATCH", None, flags
    if len(raw) != record.get("bytes"):
        return "FORECAST_FILE_CORRUPT", "RAW_SIZE_MISMATCH", None, flags
    if record.get("derived_path") is None:
        return "FORECAST_FILE_UNPARSABLE", "DERIVED_PATH_NULL", None, flags
    derived_rel = _relpath(record.get("derived_path"))
    if derived_rel is None:
        return "FORECAST_FILE_CORRUPT", "PATH_NOT_RELATIVE", None, flags
    derived = _read_file(root, derived_rel, files)
    rebuilt = False
    expected = record.get("derived_sha256")
    if derived is None or sha256_bytes(derived) != expected:
        if rebuild_derived is None:
            flags.append("DERIVED_REBUILD_UNAVAILABLE")
            return "FORECAST_FILE_CORRUPT", "DERIVED_SHA_MISMATCH", None, flags
        rebuilt_bytes = rebuild_derived(raw, record)
        if isinstance(rebuilt_bytes, (bytes, bytearray)) and sha256_bytes(bytes(rebuilt_bytes)) == expected:
            derived = bytes(rebuilt_bytes)
            rebuilt = True
            flags.append("DERIVED_REBUILT_MATCH")
        else:
            return "FORECAST_FILE_CORRUPT", "DERIVED_SHA_MISMATCH", None, flags
    try:
        doc = json.loads(derived)
    except json.JSONDecodeError:
        return "FORECAST_FILE_CORRUPT", "DERIVED_UNPARSABLE", None, flags
    if not isinstance(doc, dict):
        return "FORECAST_FILE_CORRUPT", "DERIVED_UNPARSABLE", None, flags
    _walk_outcome_keys(doc)
    universe = doc.get("universe_ref") if isinstance(doc.get("universe_ref"), dict) else {}
    rows = doc.get("rows")
    checks = (
        ("card", doc.get("card") == CARD),
        ("source_url", doc.get("source_url") == CSV_URL),
        ("source_sha256", doc.get("source_sha256") == record.get("sha256")),
        ("source_fetched_at_utc", doc.get("source_fetched_at_utc") == record.get("fetched_at_utc")),
        ("universe_ref.sha256", universe.get("sha256") == UNIVERSE_SHA),
        ("n_rows", isinstance(rows, list) and doc.get("n_rows") == len(rows)),
    )
    for field, ok in checks:
        if not ok:
            return "FORECAST_FILE_CORRUPT", "FIELD_MISMATCH:" + field, None, flags
    selected = {
        "line_no": None,
        "run_id": record.get("run_id"),
        "capture_date_utc": record.get("capture_date_utc"),
        "fetched_at_utc": record.get("fetched_at_utc"),
        "raw_sha256": record.get("sha256"),
        "raw_bytes": record.get("bytes"),
        "raw_relpath": rel,
        "derived_relpath": derived_rel,
        "derived_sha256": expected,
        "derived_rebuilt": rebuilt,
        "runner_sha256": runners.get(record.get("run_id")),
        "n_rows": doc.get("n_rows"),
        "universe_ref_sha256": universe.get("sha256"),
    }
    return "SELECTED", None, selected, flags


def _selected_view(line_no, selected):
    out = dict(selected)
    out["line_no"] = line_no
    return out


def _gaps(records):
    found = []
    for line_no, row in records:
        if row.get("record_type") != "gap_unmonitored" and row.get("source") != "gap_unmonitored":
            continue
        item = {"line_no": line_no}
        for key in SAFE_GAP_KEYS:
            if key in row:
                item[key] = row[key]
        found.append(item)
    return found


def _constants():
    return {
        "WINDOW_START": WINDOW_START,
        "WINDOW_END": WINDOW_END,
        "DECISION": DECISION,
        "CSV_URL": CSV_URL,
        "R0": R0,
        "CARD": CARD,
        "UNIVERSE_SHA": UNIVERSE_SHA,
    }


def _finalize(obj):
    body = {key: value for key, value in obj.items() if key != "output_sha256"}
    raw = json.dumps(body, indent=1, sort_keys=True).encode()
    obj["output_sha256"] = hashlib.sha256(raw).hexdigest()
    return obj


def _base(capture_raw, daily_raw, run_at, n_lines):
    return {
        "rule_doc_sha256": RULE_DOC_SHA256,
        "selector_module_sha256": module_sha256(),
        "run_at_utc": run_at,
        "constants": _constants(),
        "capture_log_sha256": sha256_bytes(capture_raw) if capture_raw is not None else None,
        "capture_log_n_lines": n_lines,
        "daily_runs_sha256": sha256_bytes(daily_raw),
        "status": None,
        "status_reason": None,
        "flags": [],
        "candidates": [],
        "n_in_window": 0,
        "n_late": 0,
        "n_stale": 0,
        "n_non_200": 0,
        "n_other_excluded": 0,
        "selected": None,
        "selected_derived_sha256": None,
        "regime": _empty_regime(),
        "regime_table": [],
        "unmonitored_intervals": [],
        "sensitivity_pre_change": "NOT_APPLICABLE",
        "possible_unlogged_method_change_notes": None,
        "python_version": sys.version,
        "platform": platform.platform(),
    }


def select_forecast(capture_log, daily_runs, root, run_at_utc, *, rebuild_derived=None, files=None):
    """Return the selection record. capture_log None means the log is absent."""
    try:
        run_at = parse_utc(run_at_utc)
    except (TypeError, ValueError):
        raise SelectorError("RUN_AT_OUT_OF_RANGE") from None
    if not (parse_utc(WINDOW_END) < run_at < parse_utc(DECISION)):
        raise SelectorError("RUN_AT_OUT_OF_RANGE")
    if not isinstance(daily_runs, (bytes, bytearray)):
        raise SelectorError("DAILY_RUNS_MISSING")
    daily_runs = bytes(daily_runs)
    if capture_log is None:
        return _finalize(_base(None, daily_runs, run_at_utc, 0) | {"status": "FORECAST_LOG_MISSING"})
    capture_log = bytes(capture_log)
    try:
        lines, records = _parse_jsonl(capture_log, "FORECAST_LOG_CORRUPT")
        _daily_lines, daily_records = _parse_jsonl(daily_runs, "FORECAST_LOG_CORRUPT")
    except SelectorError as exc:
        obj = _base(capture_log, daily_runs, run_at_utc, len(capture_log.decode("utf-8").splitlines()))
        obj["status"] = str(exc)
        return _finalize(obj)
    obj = _base(capture_log, daily_runs, run_at_utc, len(lines))
    method_rows = [
        (line_no, row)
        for line_no, row in records
        if row.get("record_type") == "capture" and row.get("source") == "methodology_asset" and row.get("status") == 200
    ]
    table, labels = _regime_table(method_rows)
    obj["regime_table"] = [
        {key: row[key] for key in ("label", "methodology_asset_sha256", "first_seen_fetched_at_utc")}
        for row in table
    ]
    obj["unmonitored_intervals"] = _gaps(records)
    captures = [
        (line_no, row)
        for line_no, row in records
        if row.get("record_type") == "capture" and row.get("source") == "races_summary"
    ]
    candidates = []
    window = []
    counts = {"IN_WINDOW": 0, "LATE": 0, "STALE": 0, "NON_200": 0}
    other = 0
    for line_no, row in captures:
        kind = _classify(row)
        candidates.append({
            "line_no": line_no,
            "capture_date_utc": row.get("capture_date_utc"),
            "fetched_at_utc": row.get("fetched_at_utc"),
            "status": row.get("status"),
            "attempt": row.get("attempt"),
            "sha256": row.get("sha256"),
            "classification": kind,
        })
        if kind == "IN_WINDOW":
            window.append((line_no, row))
            counts["IN_WINDOW"] += 1
        elif kind in counts:
            counts[kind] += 1
        else:
            other += 1
    obj["candidates"] = candidates
    obj["n_in_window"] = counts["IN_WINDOW"]
    obj["n_late"] = counts["LATE"]
    obj["n_stale"] = counts["STALE"]
    obj["n_non_200"] = counts["NON_200"]
    obj["n_other_excluded"] = other
    status, picked, tie_flags = _pick(window)
    if status is not None:
        obj["status"] = status
        return _finalize(obj)
    line_no, record = picked
    runners = _runner_index(daily_records)
    state, reason, selected, flags = _integrity(record, root, files, runners, rebuild_derived)
    flag_set = list(tie_flags)
    for flag in flags:
        if flag not in flag_set:
            flag_set.append(flag)
    obj["flags"] = [flag for flag in FLAG_ORDER if flag in flag_set]
    obj["regime"] = _regime_of(record, method_rows, labels)
    obj["possible_unlogged_method_change_notes"] = record.get("possible_unlogged_method_change_notes")
    if state != "SELECTED":
        obj["status"] = state
        obj["status_reason"] = reason
        return _finalize(obj)
    obj["status"] = "SELECTED"
    obj["status_reason"] = None
    obj["selected"] = _selected_view(line_no, selected)
    obj["selected_derived_sha256"] = selected["derived_sha256"]
    if obj["regime"]["label"] == "R0":
        obj["sensitivity_pre_change"] = "NOT_APPLICABLE"
        return _finalize(obj)
    r0_window = [(n, row) for n, row in window if _regime_of(row, method_rows, labels)["label"] == "R0"]
    pre_status, pre_picked, _pre_flags = _pick(r0_window)
    if pre_status is not None or pre_picked is None:
        obj["sensitivity_pre_change"] = "UNAVAILABLE_NO_PRECHANGE_FILE"
        return _finalize(obj)
    pre_line, pre_record = pre_picked
    pre_state, _pre_reason, pre_selected, _pre_more = _integrity(
        pre_record, root, files, runners, rebuild_derived
    )
    if pre_state != "SELECTED":
        obj["sensitivity_pre_change"] = "UNAVAILABLE_NO_PRECHANGE_FILE"
        return _finalize(obj)
    obj["sensitivity_pre_change"] = {
        "status": "SELECTED",
        "selected": _selected_view(pre_line, pre_selected),
    }
    return _finalize(obj)


def dumps(obj) -> str:
    return json.dumps(obj, indent=1, sort_keys=True) + "\n"


def main(argv):
    parser = argparse.ArgumentParser(description="Q6 forecast-file selector")
    parser.add_argument("--capture-log", required=True)
    parser.add_argument("--daily-runs", required=True)
    parser.add_argument("--root", required=True)
    parser.add_argument("--run-at-utc", required=True)
    args = parser.parse_args(argv)
    log_path = Path(args.capture_log)
    runs_path = Path(args.daily_runs)
    try:
        if not runs_path.is_file():
            raise SelectorError("DAILY_RUNS_MISSING")
        capture = log_path.read_bytes() if log_path.is_file() else None
        obj = select_forecast(capture, runs_path.read_bytes(), args.root, args.run_at_utc)
    except OutcomeKeyRefused:
        return 2
    except SelectorError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    sys.stdout.write(dumps(obj))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
