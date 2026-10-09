"""Forecast-only regime partition.

Bootstrap stays in score.block_with_boundary_count. This module does not
price a fee and is outside the fee-path max/min ban.
"""
from __future__ import annotations

import copy
import re
from decimal import Decimal, ROUND_HALF_EVEN

from card01_amc.pinload import load_national_miss
from card01_amc.score import block_with_boundary_count

LABEL_RE = re.compile(r"^(R0|R[1-9][0-9]*|UNMONITORED)$")
FROZEN_13 = frozenset({
    "AZ-01",
    "AZ-06",
    "CA-22",
    "CO-08",
    "IA-03",
    "ME-02",
    "MI-07",
    "NC-01",
    "NE-02",
    "PA-07",
    "PA-08",
    "PA-10",
    "WA-03",
})
_SHARE = Decimal("0.000001")


def is_headline(row) -> bool:
    return (
        isinstance(row, dict)
        and row.get("mapping_status") in ("KXHOUSERACE", "LEGACY")
        and row.get("y") is not None
        and row.get("p_market") is not None
        and row.get("p_model") is not None
    )


def headline_rows(rows):
    return [row for row in rows if is_headline(row)]


def m3_rows(rows):
    return [row for row in rows if not is_headline(row)]


def share_of(numerator, denominator):
    if not denominator:
        return None
    return (Decimal(numerator) / Decimal(denominator)).quantize(_SHARE, rounding=ROUND_HALF_EVEN)


def label_for(row, selection) -> str:
    """UNCLASSIFIED when the selection or the row forecast sha does not qualify."""
    if not isinstance(selection, dict) or selection.get("status") != "SELECTED":
        return "UNCLASSIFIED"
    regime = selection.get("regime") if isinstance(selection.get("regime"), dict) else {}
    override = row.get("regime_label") if isinstance(row.get("regime_label"), str) else None
    label = override if override is not None else regime.get("label")
    if not isinstance(label, str) or LABEL_RE.fullmatch(label) is None:
        return "UNCLASSIFIED"
    if "forecast_input_sha256" in row and row.get("forecast_input_sha256") != selection.get("selected_derived_sha256"):
        return "UNCLASSIFIED"
    return label


def _ci_rule(block):
    """Null CI fields only when the block has fewer than 2 states."""
    if not isinstance(block, dict) or block.get("n", 0) == 0:
        return block
    states = block.get("states")
    if not isinstance(states, int) or states >= 2:
        return block
    out = copy.deepcopy(block)
    arms = out.get("arms")
    if isinstance(arms, dict):
        for arm in arms.values():
            if isinstance(arm, dict):
                arm["CI95_D_raw"] = None
                arm["CI95_D_rc"] = None
    out["ci_status"] = "UNDEFINED_FEWER_THAN_2_STATES"
    return out


def safe_block(rows, pinned=None):
    """Return (block, status). n = 0 skips the resampler."""
    pinned = pinned or load_national_miss()
    if not rows:
        return {"n": 0}, "EMPTY"
    try:
        block = block_with_boundary_count(rows, pinned)
    except Exception:
        return {
            "n": len(rows),
            "states": len({row.get("state") for row in rows}),
            "arms": None,
            "ci_status": "ERROR",
        }, "ERROR"
    states = block.get("states")
    if isinstance(states, int) and states < 2:
        return _ci_rule(block), "UNDEFINED_FEWER_THAN_2_STATES"
    return block, "OK"


def _table_entries(selection):
    table = selection.get("regime_table") if isinstance(selection, dict) else None
    entries = []
    if isinstance(table, list):
        for item in table:
            if not isinstance(item, dict):
                continue
            label = item.get("label")
            if label in ("UNMONITORED", "UNCLASSIFIED"):
                continue
            entries.append(item)
    entries.append({
        "label": "UNMONITORED",
        "methodology_asset_sha256": None,
        "first_seen_fetched_at_utc": None,
    })
    entries.append({
        "label": "UNCLASSIFIED",
        "methodology_asset_sha256": None,
        "first_seen_fetched_at_utc": None,
    })
    return entries


def _row_shell(entry, members, n_scored, pinned):
    label = entry.get("label")
    special = label in ("UNMONITORED", "UNCLASSIFIED")
    block, status = safe_block(members, pinned)
    n = len(members)
    return {
        "regime_label": label,
        "methodology_asset_sha256": None if special else entry.get("methodology_asset_sha256"),
        "first_seen_fetched_at_utc": None if special else entry.get("first_seen_fetched_at_utc"),
        "snapshot_role": "HEADLINE_L" if n else None,
        "n": n,
        "states": len({row.get("state") for row in members}),
        "share_of_scored": share_of(n, n_scored),
        "race_ids": [row.get("race_id") for row in members],
        "block": block,
        "status": status,
        "class": "DISPLAY-ONLY",
        "freeze_named": True,
    }


def regime_labels(rows, selection):
    """Label of each headline row, in row order. No bootstrap."""
    return [label_for(row, selection) for row in headline_rows(rows)]


def build_regime_split(rows, selection, pinned=None):
    pinned = pinned or load_national_miss()
    scored = headline_rows(rows)
    n_scored = len(scored)
    grouped = {entry["label"]: [] for entry in _table_entries(selection)}
    for row in scored:
        label = label_for(row, selection)
        grouped.setdefault(label, []).append(row)
    built = []
    seen = []
    for entry in _table_entries(selection):
        label = entry["label"]
        if label in seen:
            continue
        seen.append(label)
        built.append(_row_shell(entry, grouped.get(label, []), n_scored, pinned))
    assigned = []
    for item in built:
        assigned.extend(item["race_ids"])
    nonempty = 0
    for item in built:
        if item["n"]:
            nonempty += 1
    n_unclassified = 0
    for item in built:
        if item["regime_label"] == "UNCLASSIFIED":
            n_unclassified = item["n"]
    regime = selection.get("regime") if isinstance(selection, dict) else None
    applicable = regime.get("regime_changed_since_freeze") if isinstance(regime, dict) else None
    return {
        "applicable": applicable,
        "selection_record_sha256": None,
        "n_universe": len(rows),
        "n_scored": n_scored,
        "n_not_scored": len(rows) - n_scored,
        "n_unclassified": n_unclassified,
        "unclassified_share_of_scored": None if share_of(n_unclassified, n_scored) is None else str(share_of(n_unclassified, n_scored)),
        "partition_ok": len(assigned) == n_scored and len(assigned) == len(set(assigned)),
        "rows_nonempty": nonempty,
        "structural_label": "ROWS_NONEMPTY=" + str(nonempty),
        "pooled_row_ref": "all_admitted",
        "rows": _stringify_shares(built),
        "class": "DISPLAY-ONLY",
    }


def _stringify_shares(rows):
    out = []
    for row in rows:
        item = dict(row)
        share = item.get("share_of_scored")
        item["share_of_scored"] = None if share is None else str(share)
        out.append(item)
    return out


def no_overlap_79(rows, pinned=None):
    kept = [row for row in headline_rows(rows) if row.get("race_id") not in FROZEN_13]
    block, status = safe_block(kept, pinned)
    return {
        "n": len(kept),
        "removed_labels": sorted(FROZEN_13),
        "status": status,
        "block": block,
        "freeze_named": True,
        "class": "DISPLAY-ONLY",
    }


def _pre_status(selection):
    sens = selection.get("sensitivity_pre_change") if isinstance(selection, dict) else None
    if isinstance(sens, str):
        return sens
    if isinstance(sens, dict):
        status = sens.get("status")
        if isinstance(status, str) and status:
            return status
        return "SELECTED"
    regime = selection.get("regime") if isinstance(selection, dict) else None
    label = regime.get("label") if isinstance(regime, dict) else None
    if label == "R0":
        return "NOT_APPLICABLE"
    return "UNAVAILABLE_NO_PRECHANGE_FILE"


def _derived_sha(selection):
    sens = selection.get("sensitivity_pre_change") if isinstance(selection, dict) else None
    if isinstance(sens, dict):
        if isinstance(sens.get("derived_sha256"), str):
            return sens["derived_sha256"]
        selected = sens.get("selected")
        if isinstance(selected, dict) and isinstance(selected.get("derived_sha256"), str):
            return selected["derived_sha256"]
    return None


def pre_change_snapshot(selection, pre_rows, headline_ids, forecast_sha256=None, pinned=None):
    """Counts plus all_admitted when the pre-change file is SELECTED. Nothing else."""
    status = _pre_status(selection)
    shell = {"status": status, "counts": None, "all_admitted": None, "class": "DISPLAY-ONLY"}
    if status != "SELECTED":
        return shell
    expected = _derived_sha(selection)
    if expected is None or forecast_sha256 != expected:
        shell["status"] = "INPUT_MISSING:pre_change_linkage"
        return shell
    if not isinstance(pre_rows, list):
        shell["status"] = "INPUT_MISSING:pre_change_joined_rows"
        return shell
    pre_ids = {row.get("race_id") for row in headline_rows(pre_rows)}
    current = set(headline_ids)
    differs = 0
    for race_id in current | pre_ids:
        in_current = race_id in current
        in_pre = race_id in pre_ids
        if in_current != in_pre:
            differs += 1
    block, _status = safe_block(headline_rows(pre_rows), pinned)
    shell["counts"] = {
        "n_universe": len(pre_rows),
        "n_scored": len(pre_ids),
        "n_not_scored": len(pre_rows) - len(pre_ids),
        "n_admission_differs": differs,
    }
    shell["all_admitted"] = block
    return shell
