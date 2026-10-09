"""R13–R16 and P10. Cell labels follow KD-8 and do not apply the verdict floors."""

import math

from .bootstrap import resample
from .constants import (
    BAND_HI,
    BAND_LO,
    CENSOR_SHARE_LIMIT,
    DROPPED_LIMIT,
    FEE_ADMISSION,
    HORIZONS,
    K_STAR,
    MIN_GAMES,
)


def side_name(d):
    return "YES" if d == 1 else "NO"


def _selected(records, side, key, horizon, pred):
    chosen = []
    token = str(horizon)
    for record in records:
        if record["d"] != side or record["status"] != "OK":
            continue
        if record[key][token] is None:
            continue
        if pred is not None and not pred(record):
            continue
        chosen.append(record)
    return chosen


def _stats(events, rows, key, horizon, weight):
    token = str(horizon)
    stats = {}
    lists = {}
    for event in events:
        group = [row for row in rows if row["event"] == event]
        if weight:
            stats[event] = (
                math.fsum(row["S"] for row in group),
                math.fsum(row["S"] * row[key][token] for row in group),
            )
        else:
            values = [row[key][token] for row in group]
            stats[event] = (float(len(values)), math.fsum(values))
        lists[event] = [row[key][token] for row in group]
    return stats, lists


def _point(rows, key, horizon, weight):
    token = str(horizon)
    if weight:
        den = math.fsum(row["S"] for row in rows)
        if den <= 0.0:
            return None
        return math.fsum(row["S"] * row[key][token] for row in rows) / den
    if not rows:
        return None
    return math.fsum(row[key][token] for row in rows) / len(rows)


def cell_label(point, low, high, kept, dropped):
    """KD-8. Censor share and the game floor do not set this label."""
    if point is None or low is None or high is None or kept < 2 or dropped > DROPPED_LIMIT or low == high:
        return "CELL_UNDEFINED"
    if low > 0 or high < 0:
        return "CELL_CI_EXCLUDES_0"
    return "CELL_CI_INCLUDES_0"


def cell_estimate(events, records, side, idx, *, key="RV", horizon=K_STAR, pred=None, weight=False):
    rows = _selected(records, side, key, horizon, pred)
    stats, lists = _stats(events, rows, key, horizon, weight)
    point = _point(rows, key, horizon, weight)
    draw = resample(events, stats, idx)
    label = cell_label(point, draw["L"], draw["U"], draw["kept"], draw["dropped"])
    return {
        "L": draw["L"],
        "U": draw["U"],
        "dropped": draw["dropped"],
        "games_valid": len({row["event"] for row in rows}),
        "kept": draw["kept"],
        "label": label,
        "n_valid": len(rows),
        "point": point,
        "_lists": lists,
        "_stats": stats,
    }


def primary_side(events, records, side, idx):
    headline = [row for row in records if row["d"] == side]
    estimate = cell_estimate(events, records, side, idx)
    n_pre = sum(1 for row in headline if row["status"] == "NO_PRE_MID")
    n_entry = sum(1 for row in headline if row["status"] == "NO_ENTRY_MID")
    n_null = sum(
        1
        for row in headline
        if row["status"] == "OK" and row["RV"][str(K_STAR)] is None
    )
    null_by_k = {}
    for horizon in HORIZONS:
        null_by_k[str(horizon)] = sum(
            1
            for row in headline
            if row["status"] == "OK" and row["RV"][str(horizon)] is None
        )
    censored = n_pre + n_entry + n_null
    share = None if not headline else censored / len(headline)
    width = None if estimate["L"] is None else estimate["U"] - estimate["L"]
    return {
        "L": estimate["L"],
        "NO_ENTRY_MID": n_entry,
        "NO_PRE_MID": n_pre,
        "U": estimate["U"],
        "censored_numerator": censored,
        "censored_share": share,
        "ci_width": width,
        "dropped": estimate["dropped"],
        "games_valid": estimate["games_valid"],
        "headline": len(headline),
        "kept": estimate["kept"],
        "label": estimate["label"],
        "n_valid": estimate["n_valid"],
        "null_at_kstar": n_null,
        "null_by_k_among_OK": null_by_k,
        "point": estimate["point"],
        "_lists": estimate["_lists"],
        "_stats": estimate["_stats"],
    }


def public_cell(estimate):
    """Drop private resample fields used only for the P8 check."""
    return {key: value for key, value in estimate.items() if not key.startswith("_")}


def cell_block(events, records, side, idx):
    """KD-9. No pooled both-sides cell. Net cells stay blocked."""
    block = {
        "S5K": public_cell(
            cell_estimate(events, records, side, idx, pred=lambda row: "S5K" in row["flags"])
        ),
        "SIZE_WEIGHTED": public_cell(
            cell_estimate(events, records, side, idx, weight=True)
        ),
        "ISOLATED": public_cell(
            cell_estimate(
                events, records, side, idx, pred=lambda row: "ISOLATED" in row["flags"]
            )
        ),
        "ENTRY_MID_BAND": public_cell(
            cell_estimate(
                events,
                records,
                side,
                idx,
                pred=lambda row: BAND_LO <= row["m_E"] <= BAND_HI,
            )
        ),
    }
    for horizon in HORIZONS:
        if horizon == K_STAR:
            continue
        block["RV_k%d" % horizon] = public_cell(
            cell_estimate(events, records, side, idx, horizon=horizon)
        )
    for horizon in HORIZONS:
        block["TMO_GROSS_k%d" % horizon] = public_cell(
            cell_estimate(events, records, side, idx, key="TMO", horizon=horizon)
        )
    block["TMO_NET_C100"] = FEE_ADMISSION
    block["TMO_NET_C1"] = FEE_ADMISSION
    return block


def impact_profile(records):
    """KD-12. Point estimates on sweeps valid at both entry and the exit."""
    profile = {}
    for side in (1, -1):
        side_profile = {}
        for horizon in HORIZONS:
            subset = [
                row
                for row in records
                if row["d"] == side
                and row["status"] == "OK"
                and row["I_Ek"][str(horizon)] is not None
            ]
            label = "E+%d" % horizon
            if not subset:
                side_profile[label] = None
                continue
            mean_entry = math.fsum(row["I_E"] for row in subset) / len(subset)
            mean_exit = math.fsum(row["I_Ek"][str(horizon)] for row in subset) / len(subset)
            side_profile[label] = {
                "n": len(subset),
                "mean_I_E": mean_entry,
                "mean_I_Ek": mean_exit,
                "transitory": mean_entry - mean_exit,
            }
        profile[side_name(side)] = side_profile
    return profile


def leave_one_out(events, records, sweeps):
    """P10. Point estimates only. UNDEFINED where a side has no valid sweep."""
    rows = []
    for event in events:
        row = {"left_out": event}
        for side in (1, -1):
            values = [
                record["RV"][str(K_STAR)]
                for record in records
                if record["d"] == side
                and record["event"] != event
                and record["status"] == "OK"
                and record["RV"][str(K_STAR)] is not None
            ]
            if not values:
                row["RV_" + side_name(side)] = "UNDEFINED"
            else:
                row["RV_" + side_name(side)] = math.fsum(values) / len(values)
        rows.append(row)
    share = {}
    for side in (1, -1):
        headline = [sweep for sweep in sweeps if sweep["d"] == side]
        if not headline:
            share[side_name(side)] = None
            continue
        counts = {}
        for sweep in headline:
            counts[sweep["event"]] = counts.get(sweep["event"], 0) + 1
        share[side_name(side)] = max(counts.values()) / len(headline)
    return {
        "rows": rows,
        "max_single_game_share_of_headline": share,
        "label": "SENSITIVITY_NOT_SELECTION",
    }


# Re-exported so a reader can see the floors that are reported, not used as labels.
CELL_FLOORS_REPORTED_NOT_LABELS = (CENSOR_SHARE_LIMIT, MIN_GAMES)
