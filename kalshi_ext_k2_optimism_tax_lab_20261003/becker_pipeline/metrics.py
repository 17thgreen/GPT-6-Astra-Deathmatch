"""Population descriptives. Gross is the headline. Net is an illustrative sensitivity.

Bootstrap resamples events. Each event is reduced to sufficient statistics once,
so a resample sums those statistics instead of walking rows again.
"""

import random
from decimal import Decimal

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
    ceil_cent,
    part_b_row_fee,
)
from shared.stats import q7, sample_sd, spearman
from shared.refusals import assert_not_holdout, assert_timestamp_allowed
from shared.weeks import is_complete_week, week_from_event_ticker

B_WEEK = 2000
B_POOLED = 10000
SEED_BASE = 20261003
COMPLETE_MIN_EVENTS = 8
BAND_MIN_EVENTS = 20
SYNTHETIC_SELECTION = "SYNTHETIC_NOT_BECKER"
SYNTHETIC_COVERAGE = "Synthetic coverage only."

TAGS = [
    "BECKER_EXTERNAL_PRIOR_A",
    "TRADE_ONLY_NO_QUOTES",
    "SELECTION_VOLUME_GE_100",
    "ARCHIVE_ENDS_2025-11-25",
    "LICENCE_U_NO_REDISTRIBUTION",
]
LABEL_TAG = "BECKER_LABEL_DEPENDENT_DESCRIPTIVE_ONLY"

_STAT_KEYS = (
    "n_rows",
    "contracts",
    "taker_yes_contracts",
    "taker_no_contracts",
    "no_excess_cents",
    "yes_excess_cents",
    "maker_fee_no",
    "maker_fee_yes",
    "maker_sub_no",
    "maker_sub_yes",
    "taker_fee_yes",
    "taker_fee_no",
    "taker_group_yes",
    "taker_group_no",
)


def blank_stats():
    return {
        "n_rows": 0,
        "contracts": 0,
        "taker_yes_contracts": 0,
        "taker_no_contracts": 0,
        "no_excess_cents": 0,
        "yes_excess_cents": 0,
        "maker_fee_no": Decimal(0),
        "maker_fee_yes": Decimal(0),
        "maker_sub_no": Decimal(0),
        "maker_sub_yes": Decimal(0),
        "taker_fee_yes": Decimal(0),
        "taker_fee_no": Decimal(0),
        "taker_group_yes": Decimal(0),
        "taker_group_no": Decimal(0),
    }


def add_stats(left, right):
    out = blank_stats()
    for key in _STAT_KEYS:
        out[key] = left[key] + right[key]
    return out


def fold_stats(items):
    acc = blank_stats()
    for item in items:
        acc = add_stats(acc, item)
    return acc


def _time_key(value):
    if value is None:
        return ""
    if hasattr(value, "isoformat"):
        text = value.isoformat()
        return text[:-6] + "Z" if text.endswith("+00:00") else text
    return str(value)


def _ratio(numer, denom):
    if not denom:
        return None
    return float(Decimal(numer) / Decimal(denom))


def _money(cents, denom):
    if not denom:
        return None
    return float((Decimal(cents) / Decimal(100)) / Decimal(denom))


def _net(cents, fee, denom):
    if not denom:
        return None
    return float(((Decimal(cents) / Decimal(100)) - fee) / Decimal(denom))


def metric(stats, field):
    """Contract-weighted cell metric. None when the denominator is empty."""
    if field == "S":
        return _ratio(stats["taker_yes_contracts"], stats["contracts"])
    if field == "MNO":
        return _money(stats["no_excess_cents"], stats["taker_yes_contracts"])
    if field == "MYES":
        return _money(stats["yes_excess_cents"], stats["taker_no_contracts"])
    if field == "MNO_minus_MYES":
        left = metric(stats, "MNO")
        right = metric(stats, "MYES")
        if left is None or right is None:
            return None
        return left - right
    if field == "MNO_net":
        return _net(stats["no_excess_cents"], stats["maker_fee_no"], stats["taker_yes_contracts"])
    if field == "MYES_net":
        return _net(stats["yes_excess_cents"], stats["maker_fee_yes"], stats["taker_no_contracts"])
    if field == "MNO_sub":
        return _net(stats["no_excess_cents"], stats["maker_sub_no"], stats["taker_yes_contracts"])
    if field == "MYES_sub":
        return _net(stats["yes_excess_cents"], stats["maker_sub_yes"], stats["taker_no_contracts"])
    if field == "TAKER_YES_GROUP":
        return _net(-stats["no_excess_cents"], stats["taker_group_yes"], stats["taker_yes_contracts"])
    if field == "TAKER_NO_GROUP":
        return _net(-stats["yes_excess_cents"], stats["taker_group_no"], stats["taker_no_contracts"])
    raise KeyError(field)


def prepare_trade(row, market, registry, multiplier):
    week, index = week_from_event_ticker(market["event_ticker"])
    contracts = int(row["count"])
    yes_price = int(row["yes_price"])
    no_price = int(row["no_price"])
    taker_side = row["taker_side"]
    taker_yes = taker_side == "yes"
    _maker_model, maker_fee, maker_sub = part_b_row_fee(MAKER_COEF, contracts, yes_price, multiplier)
    taker_model, taker_fee, _taker_sub = part_b_row_fee(TAKER_COEF, contracts, yes_price, multiplier)
    settled = market.get("result")
    return {
        "event": market["event_ticker"],
        "week": week,
        "week_index": 0 if index is None else index,
        "stratum": "PRE" if week == "PRE" else "REG",
        "band": band_id_for_yes_price(yes_price, registry),
        "contracts": contracts,
        "taker_yes": taker_yes,
        "taker_side": taker_side,
        "ticker": row["ticker"],
        "created_time": _time_key(row.get("created_time")),
        "no_excess_cents": contracts * ((100 if settled == "no" else 0) - no_price) if taker_yes else 0,
        "yes_excess_cents": contracts * ((100 if settled == "yes" else 0) - yes_price) if not taker_yes else 0,
        "maker_fee": maker_fee,
        "maker_sub": maker_sub,
        "taker_fee": taker_fee,
        "taker_model": taker_model,
    }


class Accumulator:
    """Per-event and per-event-band sufficient statistics. Rows are not kept."""

    def __init__(self):
        self.events = {}
        self._group_all = {}
        self._group_band = {}

    def add(self, prepared):
        event = prepared["event"]
        slot = self.events.get(event)
        if slot is None:
            slot = {
                "week": prepared["week"],
                "week_index": prepared["week_index"],
                "stratum": prepared["stratum"],
                "all": blank_stats(),
                "bands": {},
            }
            self.events[event] = slot
        band = prepared["band"]
        if band not in slot["bands"]:
            slot["bands"][band] = blank_stats()
        for target in (slot["all"], slot["bands"][band]):
            self._add_row(target, prepared)
        group_key = (prepared["ticker"], prepared["created_time"], prepared["taker_side"])
        self._group_all[(event, group_key)] = (
            self._group_all.get((event, group_key), Decimal(0)) + prepared["taker_model"]
        )
        self._group_band[(event, band, group_key)] = (
            self._group_band.get((event, band, group_key), Decimal(0)) + prepared["taker_model"]
        )

    def _add_row(self, stats, prepared):
        contracts = prepared["contracts"]
        stats["n_rows"] += 1
        stats["contracts"] += contracts
        if prepared["taker_yes"]:
            stats["taker_yes_contracts"] += contracts
            stats["no_excess_cents"] += prepared["no_excess_cents"]
            stats["maker_fee_no"] += prepared["maker_fee"]
            stats["maker_sub_no"] += prepared["maker_sub"]
            stats["taker_fee_yes"] += prepared["taker_fee"]
        else:
            stats["taker_no_contracts"] += contracts
            stats["yes_excess_cents"] += prepared["yes_excess_cents"]
            stats["maker_fee_yes"] += prepared["maker_fee"]
            stats["maker_sub_yes"] += prepared["maker_sub"]
            stats["taker_fee_no"] += prepared["taker_fee"]

    def finish(self):
        for (event, (_ticker, _created, side)), model in self._group_all.items():
            fee = ceil_cent(model)
            key = "taker_group_yes" if side == "yes" else "taker_group_no"
            self.events[event]["all"][key] += fee
        for (event, band, (_ticker, _created, side)), model in self._group_band.items():
            fee = ceil_cent(model)
            key = "taker_group_yes" if side == "yes" else "taker_group_no"
            self.events[event]["bands"][band][key] += fee
        self._group_all.clear()
        self._group_band.clear()
        return self.events


def stats_from_prepared(rows):
    """Row-level sufficient statistics for one event list. Group fees stay inside the list."""
    acc = Accumulator()
    for prepared in rows:
        acc.add(prepared)
    folded = acc.finish()
    if not folded:
        return blank_stats()
    return fold_stats(slot["all"] for slot in folded.values())


def cluster_bootstrap_units(stats_by_event, field, b, seed):
    """Event-cluster percentile interval from precomputed unit statistics."""
    return _bootstrap_many(stats_by_event, (field,), b, seed)[field]


def cluster_bootstrap_rows(rows_by_event, field, b, seed):
    """Naive bootstrap: each draw concatenates that event's rows, then reduces them."""
    events = sorted(rows_by_event)
    if len(events) < 5 or b <= 0:
        return None
    rng = random.Random(seed)
    samples = []
    n = len(events)
    for _ in range(b):
        drawn = []
        for _draw in range(n):
            drawn.extend(rows_by_event[events[rng.randrange(n)]])
        value = metric(stats_from_prepared(drawn), field)
        if value is not None:
            samples.append(value)
    return _interval(samples)


def _bootstrap_many(stats_by_event, fields, b, seed):
    events = sorted(stats_by_event)
    out = {field: None for field in fields}
    if len(events) < 5 or b <= 0:
        return out
    rng = random.Random(seed)
    buckets = {field: [] for field in fields}
    n = len(events)
    for _ in range(b):
        acc = None
        for _draw in range(n):
            stats = stats_by_event[events[rng.randrange(n)]]
            acc = stats if acc is None else add_stats(acc, stats)
        for field in fields:
            value = metric(acc, field)
            if value is not None:
                buckets[field].append(value)
    for field, samples in buckets.items():
        out[field] = _interval(samples)
    return out


def _interval(samples):
    if not samples:
        return None
    samples.sort()
    return [q7(samples, 0.025), q7(samples, 0.975)]


_FIELDS = (
    ("S", "S", "GROSS"),
    ("MNO", "MNO", "GROSS"),
    ("MYES", "MYES", "GROSS"),
    ("MNO_minus_MYES", "MNO_minus_MYES", "GROSS"),
    ("MNO_net", "MNO", "NET_ILLUSTRATIVE"),
    ("MYES_net", "MYES", "NET_ILLUSTRATIVE"),
    ("MNO_sub", "MNO", "SENSITIVITY_DIRECT_MEMBER"),
    ("MYES_sub", "MYES", "SENSITIVITY_DIRECT_MEMBER"),
    ("TAKER_YES_GROUP", "TAKER_YES", "SENSITIVITY_TAKER_SWEEP"),
    ("TAKER_NO_GROUP", "TAKER_NO", "SENSITIVITY_TAKER_SWEEP"),
)


def _cell(stratum, week, band, metric_name, value, n_rows, n_events, fee_variant, ci, net_enabled):
    suppressed = n_rows < 20 or n_events < 2
    net_variant = fee_variant != "GROSS"
    if net_variant and not net_enabled:
        value = None
        ci = None
    if suppressed:
        value = None
        ci = None
    return {
        "stratum": stratum,
        "week": week,
        "band": band,
        "metric": metric_name,
        "fee_variant": fee_variant,
        "value": value,
        "n_trade_rows": n_rows,
        "n_events": n_events,
        "flag": "SUPPRESSED_SMALL_CELL" if suppressed else None,
        "ci95": ci,
        "gross_is_headline": fee_variant == "GROSS",
        "fee_label": FEE_LABEL,
        "net_label": NET_ILLUSTRATIVE_LABEL if net_variant else None,
        "proxy_label": PER_TRADE_PROXY_LABEL if net_variant else None,
        "schedule_label": FEE_2026_ON_2025_LABEL if net_variant else None,
        "proxy_disclosure": PROXY_OVERSTATEMENT if net_variant else None,
        "label_dependent": metric_name != "S",
        "tags": list(TAGS) + ([LABEL_TAG] if metric_name != "S" else []),
    }


def _ci_excludes(interval, point):
    if not interval or point is None:
        return False
    lo, hi = interval
    return hi < point or lo > point


def document_from_events(by_event, net_enabled=True, bootstrap_scale=1,
                         selection_bias=None, coverage=None):
    cells = []
    week_record = []
    band_record = []

    def emit(stats_map, stratum, week, band, seed, b, with_ci):
        folded = fold_stats(stats_map.values()) if stats_map else blank_stats()
        n_events = len(stats_map)
        n_rows = folded["n_rows"]
        draws = max(0, int(b * bootstrap_scale)) if with_ci else 0
        fields = [field for field, _name, variant in _FIELDS if variant == "GROSS" or net_enabled]
        cis = _bootstrap_many(stats_map, fields, draws, seed) if fields else {}
        emitted = {}
        for field, metric_name, variant in _FIELDS:
            raw = metric(folded, field)
            ci = cis.get(field)
            cells.append(_cell(
                stratum, week, band, metric_name, raw, n_rows, n_events, variant, ci, net_enabled,
            ))
            emitted[field] = (raw, ci)
        return folded, n_events, emitted

    weeks = {}
    for event, slot in by_event.items():
        weeks.setdefault((slot["stratum"], slot["week"], slot["week_index"]), {})[event] = slot["all"]
    for (stratum, week, index), stats_map in sorted(weeks.items()):
        _folded, n_events, emitted = emit(
            stats_map, stratum, week, "ALL", SEED_BASE + (index or 0), B_WEEK, True,
        )
        if stratum == "REG":
            week_record.append((index, week, n_events, emitted))

    reg = {event: slot["all"] for event, slot in by_event.items() if slot["stratum"] == "REG"}
    _folded, _n_events, pooled = emit(reg, "REG", "POOLED", "ALL", SEED_BASE, B_POOLED, True)

    for band_index, band in enumerate(f"b{i:02d}" for i in range(10)):
        stats_map = {}
        for event, slot in by_event.items():
            if slot["stratum"] == "REG" and band in slot["bands"]:
                stats_map[event] = slot["bands"][band]
        _folded, n_events, emitted = emit(
            stats_map, "REG", "POOLED", band, SEED_BASE + 100 + band_index, B_POOLED, True,
        )
        band_record.append((band, n_events, emitted))

    cross = {}
    for event, slot in by_event.items():
        if slot["stratum"] != "REG":
            continue
        for band, stats in slot["bands"].items():
            cross.setdefault((slot["week"], band), {})[event] = stats
    for (week, band), stats_map in sorted(cross.items()):
        emit(stats_map, "REG", week, band, SEED_BASE, 0, False)

    dispersion = {}
    week_metrics = ("S", "MNO", "MNO_net", "MNO_minus_MYES")
    for field in week_metrics:
        series = []
        exclude_n = 0
        positive_n = 0
        lower_n = 0
        pooled_point = pooled[field][0]
        for index, _week, n_events, emitted in sorted(week_record):
            if not is_complete_week(n_events, COMPLETE_MIN_EVENTS):
                continue
            value, ci = emitted[field]
            if value is None:
                continue
            series.append((index, value, ci))
            if _ci_excludes(ci, pooled_point):
                exclude_n += 1
            if field == "MNO" and value > 0:
                positive_n += 1
            if field == "MNO" and ci and ci[0] > 0:
                lower_n += 1
        values = [value for _index, value, _ci in series]
        indexes = [index for index, value, _ci in series]
        band_values = []
        for _band, n_events, emitted in band_record:
            if n_events < BAND_MIN_EVENTS:
                continue
            value = emitted[field][0]
            if value is not None:
                band_values.append(value)
        dispersion[field] = {
            "sample_sd": sample_sd(values) if len(values) >= 2 else None,
            "d_week": sample_sd(values) if len(values) >= 2 else None,
            "d_band": sample_sd(band_values) if len(band_values) >= 2 else None,
            "range": (max(values) - min(values)) if len(values) >= 2 else None,
            "n_complete_weeks": len(values),
            "n_complete_weeks_ci_excludes_pooled": exclude_n,
            "spearman_week": spearman(indexes, values) if values else None,
        }
        if field == "MNO":
            dispersion[field]["n_complete_weeks_positive"] = positive_n
            dispersion[field]["n_complete_weeks_ci_lower_gt_0"] = lower_n
    dispersion["S_band"] = {"sample_sd": dispersion["S"]["d_band"]}
    return {
        "cells": cells,
        "dispersion": dispersion,
        "selection_bias": selection_bias if selection_bias is not None else SYNTHETIC_SELECTION,
        "coverage": coverage if coverage is not None else SYNTHETIC_COVERAGE,
        "tags": list(TAGS),
        "feeds_gate": False,
        "promote": False,
        "counts_toward_keep": False,
        "results": None,
        "pnl": None,
        "roi": None,
    }


def build_cells(rows, market_by, registry, multiplier, excluded, net_enabled=True, bootstrap_scale=1,
                holdout_events=None, holdout_game_ids=None, selection_bias=None, coverage=None):
    if holdout_events is None or holdout_game_ids is None:
        loaded_events, loaded_ids = load_holdout_sets()
        if holdout_events is None:
            holdout_events = loaded_events
        if holdout_game_ids is None:
            holdout_game_ids = loaded_ids
    assert_none_excluded((row["ticker"] for row in rows), excluded)
    acc = Accumulator()
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
        acc.add(prepare_trade(row, market, registry, multiplier))
    return document_from_events(
        acc.finish(), net_enabled=net_enabled, bootstrap_scale=bootstrap_scale,
        selection_bias=selection_bias, coverage=coverage,
    )
