"""Population descriptives. Gross is the headline. Net is an illustrative sensitivity."""

import math
import random

from becker_pipeline.exclusion import assert_none_excluded
from becker_pipeline.pins import load_holdout_sets
from shared.bands import band_id_for_yes_price
from shared.fees import (
    FEE_2026_ON_2025_LABEL,
    FEE_LABEL,
    MAKER_COEF,
    NET_ILLUSTRATIVE_LABEL,
    PER_TRADE_PROXY_LABEL,
    PROXY_OVERSTATEMENT,
    TAKER_COEF,
    part_b_row_fee,
)
from shared.stats import q7, sample_sd, spearman
from shared.refusals import assert_not_holdout, assert_timestamp_allowed
from shared.weeks import is_complete_week, week_from_event_ticker

B_WEEK = 2000
B_POOLED = 10000
SEED_BASE = 20261003
COMPLETE_MIN_EVENTS = 8

TAGS = [
    "BECKER_EXTERNAL_PRIOR_A",
    "TRADE_ONLY_NO_QUOTES",
    "SELECTION_VOLUME_GE_100",
    "ARCHIVE_ENDS_2025-11-25",
    "LICENCE_U_NO_REDISTRIBUTION",
]
LABEL_TAG = "BECKER_LABEL_DEPENDENT_DESCRIPTIVE_ONLY"

SELECTION_BIAS = (
    "Becker fetched trades only for markets with snapshot volume ≥ 100 "
    "(Clock (c), [V code / I data]). Thin markets are therefore missing by design "
    "across every tier. Any population statistic describes liquid markets and "
    "over-weights high-attention games relative to all listed markets [I]. For t0 "
    "the effect is small in count (2 of 486 markets have no trades, both under 100 "
    "volume [V]), but any cross-series generalization inherits the bias. "
    "Closed-market trade sums also fall slightly short of volume (Clock (d); t0: "
    "190/428 exact, median relative shortfall 7.13e-05 [V Clock])."
)
COVERAGE = (
    "KXNFLGAME 2025 preseason plus REG W01–W12 only (the archive ends 2025-11-25; "
    "no late season and no playoffs [V Clock])."
)


def _working_rows(rows, market_by, registry, multiplier, excluded, holdout_events, holdout_game_ids):
    assert_none_excluded((row["ticker"] for row in rows), excluded)
    out = []
    for row in rows:
        if row.get("created_time") is not None:
            assert_timestamp_allowed(row["created_time"])
        market = market_by[row["ticker"]]
        assert_not_holdout(
            event=market.get("event_ticker"),
            ticker=row["ticker"],
            game_id=row.get("game_id"),
            holdout_events=holdout_events,
            holdout_game_ids=holdout_game_ids,
        )
        week, index = week_from_event_ticker(market["event_ticker"])
        stratum = "PRE" if week == "PRE" else "REG"
        band = band_id_for_yes_price(row["yes_price"], registry)
        contracts = row["count"]
        taker_yes = row["taker_side"] == "yes"
        _model_m, maker_fee, _sub_m = part_b_row_fee(MAKER_COEF, contracts, row["yes_price"], multiplier)
        _model_t, taker_fee, _sub_t = part_b_row_fee(TAKER_COEF, contracts, row["yes_price"], multiplier)
        settled = market["result"]
        e_no = None
        e_yes = None
        if taker_yes:
            e_no = (1.0 if settled == "no" else 0.0) - (row["no_price"] / 100.0)
        else:
            e_yes = (1.0 if settled == "yes" else 0.0) - (row["yes_price"] / 100.0)
        out.append({
            "event": market["event_ticker"],
            "week": week,
            "week_index": 0 if index is None else index,
            "stratum": stratum,
            "band": band,
            "contracts": contracts,
            "taker_yes": taker_yes,
            "e_no": e_no,
            "e_yes": e_yes,
            "maker_fee": maker_fee,
            "taker_fee": taker_fee,
        })
    return out


def _combine(rows, net_enabled):
    contracts = math.fsum(row["contracts"] for row in rows)
    yes_contracts = math.fsum(row["contracts"] for row in rows if row["taker_yes"])
    n_rows = len(rows)
    events = {row["event"] for row in rows}
    s_value = (yes_contracts / contracts) if contracts else None
    no_rows = [row for row in rows if row["taker_yes"]]
    yes_rows = [row for row in rows if not row["taker_yes"]]
    no_den = math.fsum(row["contracts"] for row in no_rows)
    yes_den = math.fsum(row["contracts"] for row in yes_rows)
    mno = (math.fsum(row["contracts"] * row["e_no"] for row in no_rows) / no_den) if no_den else None
    myes = (math.fsum(row["contracts"] * row["e_yes"] for row in yes_rows) / yes_den) if yes_den else None
    contrast = None if mno is None or myes is None else mno - myes
    mno_net = None
    myes_net = None
    if net_enabled and no_den:
        mno_net = math.fsum(
            row["contracts"] * row["e_no"] - float(row["maker_fee"]) for row in no_rows
        ) / no_den
    if net_enabled and yes_den:
        myes_net = math.fsum(
            row["contracts"] * row["e_yes"] - float(row["maker_fee"]) for row in yes_rows
        ) / yes_den
    return {
        "n_trade_rows": n_rows,
        "n_events": len(events),
        "contracts": contracts,
        "S": s_value,
        "MNO": mno,
        "MYES": myes,
        "MNO_minus_MYES": contrast,
        "MNO_net": mno_net,
        "MYES_net": myes_net,
        "events": events,
        "by_event": _by_event(rows),
    }


def _by_event(rows):
    grouped = {}
    for row in rows:
        grouped.setdefault(row["event"], []).append(row)
    return grouped


def _boot_mean(by_event, field, b, seed, net_enabled):
    events = sorted(by_event)
    if len(events) < 5 or b <= 0:
        return None
    rng = random.Random(seed)
    samples = []
    n = len(events)
    for _ in range(b):
        draw = [by_event[events[rng.randrange(n)]] for _ in range(n)]
        flat = [row for group in draw for row in group]
        samples.append(_combine(flat, net_enabled)[field])
    samples = [value for value in samples if value is not None]
    if not samples:
        return None
    samples.sort()
    return [q7(samples, 0.025), q7(samples, 0.975)]


def _cell(stratum, week, band, metric, value, summary, fee_variant, ci, net_enabled):
    suppressed = summary["n_trade_rows"] < 20 or summary["n_events"] < 2
    net_variant = fee_variant != "GROSS"
    if net_variant and not net_enabled:
        value = None
    if suppressed:
        value = None
        ci = None
    return {
        "stratum": stratum,
        "week": week,
        "band": band,
        "metric": metric,
        "fee_variant": fee_variant,
        "value": value,
        "n_trade_rows": summary["n_trade_rows"],
        "n_events": summary["n_events"],
        "flag": "SUPPRESSED_SMALL_CELL" if suppressed else None,
        "ci95": ci,
        "gross_is_headline": fee_variant == "GROSS",
        "fee_label": FEE_LABEL,
        "net_label": NET_ILLUSTRATIVE_LABEL if net_variant else None,
        "proxy_label": PER_TRADE_PROXY_LABEL if net_variant else None,
        "schedule_label": FEE_2026_ON_2025_LABEL if net_variant else None,
        "proxy_disclosure": PROXY_OVERSTATEMENT if net_variant else None,
        "label_dependent": metric != "S",
        "tags": list(TAGS) + ([LABEL_TAG] if metric != "S" else []),
    }


def build_cells(rows, market_by, registry, multiplier, excluded, net_enabled=True, bootstrap_scale=1,
               holdout_events=None, holdout_game_ids=None):
    if holdout_events is None or holdout_game_ids is None:
        loaded_events, loaded_ids = load_holdout_sets()
        if holdout_events is None:
            holdout_events = loaded_events
        if holdout_game_ids is None:
            holdout_game_ids = loaded_ids
    working = _working_rows(
        rows, market_by, registry, multiplier, excluded, holdout_events, holdout_game_ids,
    )
    cells = []
    reg = [row for row in working if row["stratum"] == "REG"]
    weeks = {}
    for row in working:
        weeks.setdefault((row["stratum"], row["week"], row["week_index"]), []).append(row)

    def emit(group, stratum, week, band, week_index, b, seed, with_ci):
        if not group and week != "POOLED":
            return
        summary = _combine(group, net_enabled) if group else {
            "n_trade_rows": 0, "n_events": 0, "S": None, "MNO": None, "MYES": None,
            "MNO_minus_MYES": None, "MNO_net": None, "MYES_net": None, "by_event": {},
        }
        for metric, field in (
            ("S", "S"),
            ("MNO", "MNO"),
            ("MYES", "MYES"),
            ("MNO_minus_MYES", "MNO_minus_MYES"),
        ):
            draws = max(0, int(b * bootstrap_scale))
            ci = _boot_mean(summary["by_event"], field, draws, seed, net_enabled) if with_ci else None
            cells.append(_cell(stratum, week, band, metric, summary[field], summary, "GROSS", ci, net_enabled))
            if metric in ("MNO", "MYES"):
                net_field = metric + "_net"
                net_ci = _boot_mean(summary["by_event"], net_field, draws, seed, net_enabled) if with_ci else None
                cells.append(_cell(
                    stratum, week, band, metric, summary[net_field], summary,
                    "NET_ILLUSTRATIVE", net_ci, net_enabled,
                ))

    for (stratum, week, index), group in sorted(weeks.items()):
        seed = SEED_BASE + (index or 0)
        emit(group, stratum, week, "ALL", index, B_WEEK, seed, True)
    emit(reg, "REG", "POOLED", "ALL", None, B_POOLED, SEED_BASE, True)
    # PRE is already emitted by the week loop. It is never pooled into REG.
    bands = {}
    for row in reg:
        bands.setdefault(row["band"], []).append(row)
    for band_index, band in enumerate(f"b{i:02d}" for i in range(10)):
        emit(bands.get(band, []), "REG", "POOLED", band, None, B_POOLED, SEED_BASE + 100 + band_index, True)
    cross = {}
    for row in reg:
        cross.setdefault((row["week"], row["band"]), []).append(row)
    for (week, band), group in sorted(cross.items()):
        emit(group, "REG", week, band, None, 0, SEED_BASE, False)

    complete = []
    for (stratum, week, index), group in weeks.items():
        if stratum == "REG" and is_complete_week(_combine(group, net_enabled)["n_events"], COMPLETE_MIN_EVENTS):
            complete.append((index, week, group))
    dispersion = {}
    for metric in ("S", "MNO", "MNO_net", "MNO_minus_MYES"):
        series = []
        for index, _week, group in sorted(complete):
            summary = _combine(group, net_enabled)
            series.append((index, summary[metric]))
        values = [value for _index, value in series if value is not None]
        rho = spearman([index for index, value in series if value is not None], values) if values else None
        dispersion[metric] = {
            "sample_sd": sample_sd(values) if len(values) >= 2 else None,
            "range": (max(values) - min(values)) if len(values) >= 2 else None,
            "n_complete_weeks": len(values),
            "spearman_week": rho,
        }
    band_events = []
    for band, group in bands.items():
        n_events = _combine(group, net_enabled)["n_events"]
        if n_events >= 20:
            band_events.append(_combine(group, net_enabled)["S"])
    dispersion["S_band"] = {
        "sample_sd": sample_sd([v for v in band_events if v is not None]) if len(band_events) >= 2 else None,
    }
    return {
        "cells": cells,
        "dispersion": dispersion,
        "selection_bias": SELECTION_BIAS,
        "coverage": COVERAGE,
        "tags": list(TAGS),
        "feeds_gate": False,
        "promote": False,
        "counts_toward_keep": False,
        "results": None,
        "pnl": None,
        "roi": None,
    }
