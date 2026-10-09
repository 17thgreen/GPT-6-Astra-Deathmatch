"""Assemble the regime-split and secondary-metrics report.

Fee-dependent sections are null unless admission is ADMITTED_INDEX_ONLY.
The CLI refuses an output path inside a git work tree.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
import sys
from pathlib import Path

from card01_amc.book_1103 import adverse_selection, book_status
from card01_amc.fee_admission import (
    FEE_ADMISSION_RULE_SHA256,
    REFUSED_FEE_SOURCES,
    SENSITIVITY_ROWS_STATUS,
    admit_fee_source_v2,
    pinned_entry_v2,
)
from card01_amc.fee_source import FeeBlocked
from card01_amc.pinload import load_national_miss, sha256_bytes
from card01_amc.regime_split import (
    build_regime_split,
    headline_rows,
    no_overlap_79,
    pre_change_snapshot,
)
from card01_amc.score import (
    BOOTSTRAP_SAMPLER,
    PERCENTILE_METHOD,
    ROWS_ORDER,
    STATE_ENCODING,
)
from card01_amc.secondary_metrics import (
    FEE_ASSUMPTIONS,
    capital_hours,
    drawdown,
    event_concentration,
    executable_usd_per_day,
    fee_views,
    log_loss_and_calibration,
    m3_mids_gaps,
    rewards,
    signals_and_size,
    unresolved_inventory,
)

SCHEMA = "astra.card01.regime_split_secondary.v1"
SPEC_SHA256 = "c5b08459dd6f1e1e6cae65dbb13c4aa5b0d6a1418d79d3bae54c9370d9beede5"
ACCEPT_SHA256 = "69b98b2f643a7510280cd6b959c30e285df081c8142b910808001db8cad5b81a"
DISPOSITION_SHA256 = "861b7d14e75979f798b872a2c16b6e440d4f5b6332d4ad9e1e81d713863f5757"
COLLECTOR_PLAN_SHA256 = "f9f727c118732119389ebbd1bc2eafb0c85d0123ce5970c802cfd78e8a93cb02"
FEE_SOURCE_NOTE_SHA256 = "1bd42d3a432dd79aea1a9a479c4a54d5143d2c1888702692c8f0efbedde8d3fb"


def module_sha256() -> str:
    return sha256_bytes(Path(__file__).read_bytes())


def output_inside_repo(path) -> bool:
    """True when any ancestor of path contains a git directory."""
    current = Path(path)
    if not current.is_absolute():
        current = Path.cwd() / current
    current = current.resolve()
    for parent in (current, *current.parents):
        if (parent / ".git").exists():
            return True
    return False


def _sha_obj(obj):
    if obj is None:
        return None
    raw = json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")
    return hashlib.sha256(raw).hexdigest()


def _rows_of(doc):
    if isinstance(doc, dict) and isinstance(doc.get("rows"), list):
        return doc["rows"]
    if isinstance(doc, list):
        return doc
    return []


def _settled_index(settled):
    found = {}
    results = settled.get("results") if isinstance(settled, dict) else None
    if not isinstance(results, list):
        return found
    for item in results:
        if isinstance(item, dict) and item.get("ticker") not in found:
            found[item.get("ticker")] = item
    return found


def _series_used(gate, explicit):
    if explicit:
        return list(explicit)
    found = []
    signals = gate.get("signals") if isinstance(gate, dict) else None
    if isinstance(signals, list):
        for signal in signals:
            series = signal.get("series") if isinstance(signal, dict) else None
            if series and series not in found:
                found.append(series)
    return found


def _gate_fee_reason(gate, admission):
    """None when this gate may compute against an admitted file."""
    if not admission.admitted:
        return admission.fee_block_reason
    if not isinstance(gate, dict):
        return "GATE_MISSING"
    if (
        gate.get("fee_source") in REFUSED_FEE_SOURCES
        or gate.get("fee_source_sha256") in REFUSED_FEE_SOURCES
    ):
        return "FEE_SOURCE_NOT_ADMITTED_V1_ATTEST_FAIL"
    if gate.get("status") != "OK":
        return gate.get("fee_block_reason") or "GATE_STATUS_NOT_OK"
    if "fee_admission" not in gate:
        return "FEE_ADMISSION_MISSING"
    if gate.get("fee_admission") != "ADMITTED_INDEX_ONLY":
        return gate.get("fee_block_reason") or "FEE_ADMISSION_NOT_ADMITTED"
    if (
        gate.get("fee_source_sha256") != admission.fee_source_sha256
        or gate.get("fee_source_accept_sha256") != admission.fee_source_accept_sha256
    ):
        return "FEE_SOURCE_PAIR_MISMATCH"
    return None


def _blocked_secondary(reason, forecast, capture):
    return {
        "log_loss": forecast["log_loss"],
        "log_loss_status": forecast["log_loss_status"],
        "delta_log_loss": forecast["delta_log_loss"],
        "delta_log_loss_status": forecast["delta_log_loss_status"],
        "calibration": forecast["calibration"],
        "calibration_status": forecast["calibration_status"],
        "m3_mids_gaps": forecast["m3_mids_gaps"],
        "no_overlap_79": forecast["no_overlap_79"],
        "adverse_selection_after_fills": None,
        "adverse_selection_after_fills_status": "NO_REAL_FILLS",
        "adverse_selection_simulated_fills": None,
        "adverse_selection_simulated_fills_status": "BLOCKED_FEE_UNVERIFIED",
        "signals_and_size": None,
        "signals_and_size_status": "BLOCKED_FEE_UNVERIFIED",
        "event_concentration": None,
        "event_concentration_status": "BLOCKED_FEE_UNVERIFIED",
        "capital_hours": None,
        "capital_hours_status": "BLOCKED_FEE_UNVERIFIED",
        "drawdown_usd": None,
        "drawdown_status": "BLOCKED_FEE_UNVERIFIED",
        "executable_usd_per_day": None,
        "executable_usd_per_day_status": "BLOCKED_FEE_UNVERIFIED",
        "unresolved_inventory": None,
        "unresolved_inventory_status": "BLOCKED_FEE_UNVERIFIED",
        **rewards(),
        "book_1103_status": capture,
        "fee_block_reason": reason,
    }


def build_report(
    rows,
    *,
    selection,
    score_json=None,
    gate=None,
    settled=None,
    book=None,
    pre_change_rows=None,
    pre_change_forecast_sha256=None,
    pr_c_output=None,
    fee_source_path=None,
    fee_source_id=None,
    fee_source_sha256=None,
    packet_index_path=None,
    fee_accept_path=None,
    series_used=None,
    pinned=None,
):
    pinned = pinned or load_national_miss()
    rows = _rows_of(rows)
    regime = build_regime_split(rows, selection, pinned)
    regime["selection_record_sha256"] = _sha_obj(selection)
    pre = pre_change_snapshot(
        selection,
        pre_change_rows,
        [row.get("race_id") for row in headline_rows(rows)],
        pre_change_forecast_sha256,
        pinned,
    )
    overlap = no_overlap_79(rows, pinned)
    forecast_metrics = log_loss_and_calibration(rows, pinned)
    forecast = {
        "log_loss": forecast_metrics["log_loss"],
        "log_loss_status": forecast_metrics["log_loss_status"],
        "delta_log_loss": forecast_metrics["delta_log_loss"],
        "delta_log_loss_status": forecast_metrics["delta_log_loss_status"],
        "calibration": forecast_metrics["calibration"],
        "calibration_status": forecast_metrics["calibration_status"],
        "m3_mids_gaps": m3_mids_gaps(rows),
        "no_overlap_79": overlap,
    }
    used = _series_used(gate, series_used)
    admission = admit_fee_source_v2(
        fee_source_path=fee_source_path,
        fee_source_id=fee_source_id,
        fee_source_sha256=fee_source_sha256,
        packet_index_path=packet_index_path,
        fee_accept_path=fee_accept_path,
        series_used=used,
    )
    capture = book_status(book)
    defects = []
    gate_reason = _gate_fee_reason(gate, admission)
    fee_state = "BLOCKED_FEE_UNVERIFIED"
    if gate_reason is None:
        signals = gate.get("signals") if isinstance(gate.get("signals"), list) else []
        rows_by_id = {}
        for row in rows:
            if isinstance(row, dict) and row.get("race_id") not in rows_by_id:
                rows_by_id[row.get("race_id")] = row
        if signals:
            try:
                entries = {}
                for signal in signals:
                    series = signal.get("series") if isinstance(signal, dict) else None
                    if series not in entries:
                        entries[series] = pinned_entry_v2(admission, series)
                views = fee_views(signals, rows_by_id, entries)
            except FeeBlocked as exc:
                secondary = _blocked_secondary(exc.reason, forecast, capture)
                views = None
                views_status = "BLOCKED_FEE_UNVERIFIED"
                branch = "FORECAST_ONLY_FEE_BLOCKED"
            else:
                defects.extend(views.pop("reporting_defects"))
                settled_by = _settled_index(settled)
                concentration, pnl_defects = event_concentration(views, pr_c_output)
                defects.extend(pnl_defects)
                selection_block = adverse_selection(signals, rows_by_id, book)
                secondary = {
                    **forecast,
                    "adverse_selection_after_fills": None,
                    "adverse_selection_after_fills_status": "NO_REAL_FILLS",
                    "adverse_selection_simulated_fills": selection_block,
                    "signals_and_size": signals_and_size(gate),
                    "event_concentration": concentration,
                    "capital_hours": capital_hours(signals, rows_by_id, views, settled_by),
                    "drawdown": drawdown(signals, views, settled_by, rows_by_id),
                    "executable_usd_per_day": executable_usd_per_day(signals, rows_by_id, views, pinned),
                    "unresolved_inventory": unresolved_inventory(signals, rows_by_id, views, settled_by),
                    **rewards(),
                    "book_1103_status": capture,
                }
                views_status = views["status"]
                branch = None
                fee_state = "ADMITTED"
        else:
            views = {
                "per_signal": [],
                "totals": {
                    "gross": "0",
                    "fee_headline": "0",
                    "fee_fees_2x": "0",
                    "net_headline": "0",
                    "net_fees_2x": "0",
                },
                "one_tick_worse_status": "PR_C_OUTPUT_ABSENT",
                "status": "NO_SIGNALS_SELECTED",
            }
            views_status = "NO_SIGNALS_SELECTED"
            branch = None
            fee_state = "ADMITTED"
            secondary = {
                **forecast,
                "adverse_selection_after_fills": None,
                "adverse_selection_after_fills_status": "NO_REAL_FILLS",
                "adverse_selection_simulated_fills": {
                    "book_1103_status": capture,
                    "plus_24h": None,
                    "plus_24h_status": "NO_SIGNALS_SELECTED",
                    "plus_60s": None,
                    "plus_60s_status": "NOT_CAPTURED",
                    "plus_300s": None,
                    "plus_300s_status": "NOT_CAPTURED",
                },
                "signals_and_size": signals_and_size(gate),
                "event_concentration": None,
                "event_concentration_status": "NO_SIGNALS_SELECTED",
                "capital_hours": None,
                "capital_hours_status": "NO_SIGNALS_SELECTED",
                "drawdown": None,
                "drawdown_status": "NO_SIGNALS_SELECTED",
                "executable_usd_per_day": None,
                "executable_usd_per_day_status": "NO_SIGNALS_SELECTED",
                "unresolved_inventory": {"n_contracts": 0, "race_ids": [], "cost_basis": "0", "status": "NO_SIGNALS_SELECTED"},
                **rewards(),
                "book_1103_status": capture,
            }
    else:
        views = None
        views_status = "BLOCKED_FEE_UNVERIFIED"
        branch = "FORECAST_ONLY_FEE_BLOCKED"
        secondary = _blocked_secondary(gate_reason, forecast, capture)
    report = {
        "schema": SCHEMA,
        "spec_sha256": SPEC_SHA256,
        "accept_sha256": ACCEPT_SHA256,
        "disposition_sha256": DISPOSITION_SHA256,
        "collector_plan_sha256": COLLECTOR_PLAN_SHA256,
        "fee_admission_rule_sha256": FEE_ADMISSION_RULE_SHA256,
        "fee_source_note_sha256": FEE_SOURCE_NOTE_SHA256,
        "module_sha256": module_sha256(),
        "r1p1_feebook": None,
        "inputs_sha256": {
            "joined_rows": _sha_obj(rows),
            "score_json": _sha_obj(score_json),
            "selection_record": _sha_obj(selection),
            "gate_output": _sha_obj(gate),
            "gate_sha256": None if not isinstance(gate, dict) else gate.get("gate_sha256"),
            "settled_results": _sha_obj(settled),
            "book_1103": _sha_obj(book),
            "pre_change_joined_rows": _sha_obj(pre_change_rows),
            "pr_c_output": _sha_obj(pr_c_output),
            "fee_source_accept": admission.fee_source_accept_sha256,
            "packet_index_at_admission": admission.packet_index_sha256_at_run,
        },
        "fee_admission": admission.public_dict(),
        "fee_assumptions": FEE_ASSUMPTIONS,
        "sensitivity_rows_status": SENSITIVITY_ROWS_STATUS,
        "verdict_fee_branch": branch,
        "fee_state": fee_state,
        "regime_split": regime,
        "pre_change_snapshot": pre,
        "secondary": secondary,
        "fee_views": views,
        "fee_views_status": views_status,
        "reporting_defects": defects,
        "bootstrap_sampler": BOOTSTRAP_SAMPLER,
        "percentile_method": PERCENTILE_METHOD,
        "state_encoding": STATE_ENCODING,
        "rows_order": ROWS_ORDER,
        "python_version": sys.version,
        "platform": platform.platform(),
    }
    return report


def render(report):
    body = {key: value for key, value in report.items() if key != "output_sha256"}
    payload = json.dumps(body, indent=1, sort_keys=True, ensure_ascii=True) + "\n"
    digest = hashlib.sha256(payload.encode("ascii")).hexdigest()
    body["output_sha256"] = digest
    final = json.dumps(body, indent=1, sort_keys=True, ensure_ascii=True) + "\n"
    return final, digest


def _load(path):
    if path is None:
        return None
    return json.loads(Path(path).read_text())


def main(argv):
    parser = argparse.ArgumentParser(prog="python -m card01_amc.regime_split_secondary")
    parser.add_argument("--joined-rows", required=True)
    parser.add_argument("--score", required=True)
    parser.add_argument("--selection", required=True)
    parser.add_argument("--gate", required=True)
    parser.add_argument("--settled", required=True)
    parser.add_argument("--book-1103", required=True)
    parser.add_argument("--fee-source", required=True)
    parser.add_argument("--fee-source-id", required=True)
    parser.add_argument("--fee-source-sha256", required=True)
    parser.add_argument("--packet-index", required=True)
    parser.add_argument("--fee-accept", required=True)
    parser.add_argument("--pre-change")
    parser.add_argument("--pre-change-sha")
    parser.add_argument("--pr-c")
    parser.add_argument("--out", required=True)
    args = parser.parse_args(argv)
    if output_inside_repo(args.out):
        print("OUTPUT_PATH_IN_REPO", file=sys.stderr)
        return 2
    try:
        rows = _load(args.joined_rows)
        sequence = _rows_of(rows)
        if len(sequence) != 92:
            print("JOINED_ROWS_NOT_92", file=sys.stderr)
            return 2
        report = build_report(
            sequence,
            selection=_load(args.selection),
            score_json=_load(args.score),
            gate=_load(args.gate),
            settled=_load(args.settled),
            book=_load(args.book_1103),
            pre_change_rows=_load(args.pre_change) if args.pre_change else None,
            pre_change_forecast_sha256=args.pre_change_sha,
            pr_c_output=_load(args.pr_c) if args.pr_c else None,
            fee_source_path=args.fee_source,
            fee_source_id=args.fee_source_id,
            fee_source_sha256=args.fee_source_sha256,
            packet_index_path=args.packet_index,
            fee_accept_path=args.fee_accept,
        )
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(type(exc).__name__, file=sys.stderr)
        return 2
    text, _digest = render(report)
    Path(args.out).write_text(text)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
