"""Aggregates, bootstrap contrast, and the frozen verdict rule. No grid selection."""

import math
import random
import statistics
from collections import defaultdict

from constants import (
    BOOTSTRAP_B,
    BOOTSTRAP_SEED,
    EX_POST_SENTENCE,
    HORIZONS_S,
    PRIMARY_HORIZON_S,
    VERDICT_DOMAIN,
)

BUCKETS = ("ON", "AGAINST", "NEUTRAL", "UNCLASSIFIED")
HORIZON_KEYS = tuple(str(horizon) for horizon in HORIZONS_S) + ("CLOSE", "SETTLE")


def weighted_quantile(pairs, fraction):
    ordered = sorted(pairs, key=lambda item: item[0])
    total = sum(weight for _duration, weight in ordered)
    if total <= 0:
        return None
    accumulated = 0.0
    for duration, weight in ordered:
        accumulated += weight
        if accumulated >= total * fraction:
            return duration
    return None


def summarize(portions, horizon_key):
    gross_values = []
    net_values = []
    weights = []
    censored_n = 0
    censored_contracts = 0.0
    contracts = 0.0
    for portion in portions:
        contracts += portion["size"]
        cell = portion["markouts"][horizon_key]
        if cell["gross"] is None:
            censored_n += 1
            censored_contracts += portion["size"]
        else:
            gross_values.append(cell["gross"])
            net_values.append(cell["net"])
            weights.append(portion["size"])

    def mean(values):
        if not weights:
            return None
        return sum(value * weight for value, weight in zip(values, weights)) / sum(weights)

    return {
        "n_portions": len(portions),
        "contracts": contracts,
        "censored_n": censored_n,
        "censored_contracts": censored_contracts,
        "mean_gross": mean(gross_values),
        "mean_net": mean(net_values),
        "median_gross": statistics.median(gross_values) if gross_values else None,
        "median_net": statistics.median(net_values) if net_values else None,
    }


def horizon_table(portions):
    return {key: summarize(portions, key) for key in HORIZON_KEYS}


def split_table(portions, attr):
    grouped = {bucket: [] for bucket in BUCKETS}
    for portion in portions:
        grouped[portion[attr]].append(portion)
    return {bucket: {"horizons": horizon_table(rows)} for bucket, rows in grouped.items()}


def per_game_split_table(portions, attr):
    grouped = defaultdict(list)
    for portion in portions:
        grouped[portion["event"]].append(portion)
    return {event: split_table(grouped[event], attr) for event in sorted(grouped)}


def uch_by_split(portions, attr):
    out = {}
    for bucket in BUCKETS:
        rows = [portion for portion in portions if portion[attr] == bucket]
        out[bucket] = {
            "n_portions": len(rows),
            "contracts": sum(portion["size"] for portion in rows),
            "uch": sum(portion["uch"] for portion in rows),
            "premium_hours": sum(portion["premium_hours"] for portion in rows),
        }
    return out


def hold_time_pairs(portions):
    pairs = []
    for portion in portions:
        for size, t_close in portion["closes"]:
            pairs.append((t_close - portion["t_open"], size))
    return pairs


def _percentile(sorted_values, probability):
    count = len(sorted_values)
    if count == 0:
        return None
    if count == 1:
        return sorted_values[0]
    position = probability * (count - 1)
    lo = math.floor(position)
    hi = math.ceil(position)
    if lo == hi:
        return sorted_values[lo]
    weight = position - lo
    return sorted_values[lo] * (1.0 - weight) + sorted_values[hi] * weight


def _bucket_sums(portions, horizon_key):
    """Per event, valid-markout weight and weighted gross/net for ON and AGAINST."""
    stats = {}
    for portion in portions:
        bucket = portion["s_dev"]
        if bucket not in ("ON", "AGAINST"):
            continue
        cell = portion["markouts"][horizon_key]
        if cell["gross"] is None:
            continue
        event_stats = stats.setdefault(portion["event"], {
            "ON": [0.0, 0.0, 0.0],
            "AGAINST": [0.0, 0.0, 0.0],
        })
        slot = event_stats[bucket]
        slot[0] += portion["size"]
        slot[1] += portion["size"] * cell["gross"]
        slot[2] += portion["size"] * cell["net"]
    return stats


def contrast(portions, horizon_key=str(PRIMARY_HORIZON_S), events=None):
    """Δ* = contract-weighted MO(AGAINST) - MO(ON), gross. Net is reported beside it."""
    on = summarize(
        [portion for portion in portions if portion["s_dev"] == "ON"],
        horizon_key,
    )
    against = summarize(
        [portion for portion in portions if portion["s_dev"] == "AGAINST"],
        horizon_key,
    )
    gross = net = None
    if on["mean_gross"] is not None and against["mean_gross"] is not None:
        gross = against["mean_gross"] - on["mean_gross"]
        net = against["mean_net"] - on["mean_net"]
    by_event = _bucket_sums(portions, horizon_key)
    if events is None:
        events = sorted({portion["event"] for portion in portions})
    else:
        events = list(events)
    rng = random.Random(BOOTSTRAP_SEED)
    gross_draws = []
    net_draws = []
    dropped = 0
    for _ in range(BOOTSTRAP_B):
        draw = rng.choices(events, k=len(events))
        totals = {
            "ON": [0.0, 0.0, 0.0],
            "AGAINST": [0.0, 0.0, 0.0],
        }
        for event in draw:
            event_stats = by_event.get(event)
            if event_stats is None:
                continue
            for bucket in ("ON", "AGAINST"):
                for index in range(3):
                    totals[bucket][index] += event_stats[bucket][index]
        if totals["ON"][0] <= 0 or totals["AGAINST"][0] <= 0:
            dropped += 1
            continue
        gross_draws.append(totals["AGAINST"][1] / totals["AGAINST"][0] - totals["ON"][1] / totals["ON"][0])
        net_draws.append(totals["AGAINST"][2] / totals["AGAINST"][0] - totals["ON"][2] / totals["ON"][0])
    gross_draws.sort()
    net_draws.sort()
    ci_low = _percentile(gross_draws, 0.025)
    ci_high = _percentile(gross_draws, 0.975)
    excludes = ci_low is not None and ci_high is not None and (ci_low > 0 or ci_high < 0)
    return {
        "horizon_s": PRIMARY_HORIZON_S,
        "split": "S_DEV",
        "delta": 0.005,
        "on": on,
        "against": against,
        "delta_star_gross": gross,
        "delta_star_net": net,
        "ci95_low": ci_low,
        "ci95_high": ci_high,
        "ci95_net_low": _percentile(net_draws, 0.025),
        "ci95_net_high": _percentile(net_draws, 0.975),
        "ci_excludes_0": excludes,
        "bootstrap_replicates_kept": len(gross_draws),
        "bootstrap_replicates_dropped_empty_bucket": dropped,
        "bootstrap_B": BOOTSTRAP_B,
        "bootstrap_seed": BOOTSTRAP_SEED,
        "bootstrap_sampler": "random.Random(20261003).choices(events, k=31)",
        "percentile_method": "linear interpolation at p*(n-1)",
        "role": "PRIMARY_CONTRAST",
        "net_role": "REPORTED_BESIDE_GROSS_NOT_USED_FOR_VERDICT",
    }


def censored_share(summary):
    contracts = summary["contracts"]
    if contracts <= 0:
        return None
    return summary["censored_contracts"] / contracts


def decide_verdict(
    *,
    join_ok,
    structural_ok,
    unclassified_share,
    censored_on,
    censored_against,
    open_at_window_end_contracts,
    ci_excludes_0,
):
    """R32. Only Δ* can move a non-inconclusive verdict. Domain is closed."""
    reasons = []
    if not join_ok:
        reasons.append("join")
    if not structural_ok:
        reasons.append("R36")
    if open_at_window_end_contracts != 0:
        reasons.append("open_at_window_end")
    if unclassified_share is not None and unclassified_share > 0.05:
        reasons.append("unclassified_opening_contracts")
    if censored_on is not None and censored_on > 0.20:
        reasons.append("censored_ON_at_Hstar")
    if censored_against is not None and censored_against > 0.20:
        reasons.append("censored_AGAINST_at_Hstar")
    if reasons:
        verdict = "INCONCLUSIVE"
    elif ci_excludes_0:
        verdict = "ITERATE"
        reasons = ["delta_star_ci95_excludes_0"]
    else:
        verdict = "DESCRIPTIVE"
        reasons = ["delta_star_ci95_does_not_exclude_0"]
    if verdict not in VERDICT_DOMAIN:
        raise RuntimeError(verdict)
    return verdict, reasons


def ex_post_block():
    return {
        "EX_POST_ANCHOR_U": True,
        "ex_post_sentence": EX_POST_SENTENCE,
        "evidence_tag": "[U]",
    }


def stamp_ex_post(obj):
    """Every object in a consensus-using output carries the [U] tag and sentence."""
    if isinstance(obj, dict):
        for value in list(obj.values()):
            stamp_ex_post(value)
        obj.update(ex_post_block())
    elif isinstance(obj, list):
        for value in obj:
            stamp_ex_post(value)
    return obj


def _round_float(key, value):
    if key.endswith("_raw") or key in {"shin_z", "kickoff"}:
        return value
    if (
        "hour" in key
        or key in {"uch", "uch_integral", "uch_fifo", "uch_refused", "premium_hours"}
        or key.endswith("_uch")
    ):
        return float(f"{value:.4f}")
    return float(f"{value:.6f}")


def round_reported(obj, key=None):
    if isinstance(obj, dict):
        return {name: round_reported(value, name) for name, value in obj.items()}
    if isinstance(obj, list):
        return [round_reported(value, key) for value in obj]
    if isinstance(obj, float):
        return _round_float(key or "", obj)
    return obj
