"""R03–R06 sweep builder.

Trade rows contribute ticker, at, taker_side, and size. Quote rows are skipped
by kind and no other key is read. KD-1 schema, KD-2 isolation, KD-3 thresholds.
"""

import math

from .constants import (
    ENTRY_GAP_S,
    ISO_LOOKBACK_S,
    K_STAR,
    SWEEP_KEY,
    SWEEP_ORDER,
    SWEEPS_SCHEMA,
    THRESHOLD_HEADLINE,
    THRESHOLD_S5K,
)
from .errors import ClosedUniverseRefused


def build(rows, markets):
    groups = {}
    for row in rows:
        if row.get("kind") == "quote":
            continue
        ticker = row["ticker"]
        if ticker not in markets:
            raise ClosedUniverseRefused(ticker)
        key = (ticker, row["at"], row["taker_side"])
        groups.setdefault(key, []).append(row["size"])
    heads = []
    for (ticker, at, side), sizes in groups.items():
        total = math.fsum(sizes)
        if total < THRESHOLD_HEADLINE:
            continue
        heads.append(
            {
                "ticker": ticker,
                "event": markets[ticker]["event"],
                "t_s": at,
                "taker_side": side,
                "d": 1 if side == "yes" else -1,
                "S": total,
                "n_prints": len(sizes),
            }
        )
    heads.sort(key=lambda sweep: (sweep["t_s"], sweep["ticker"], sweep["taker_side"]))
    for index, sweep in enumerate(heads, start=1):
        sweep["sweep_id"] = "SW-%06d" % index
    horizon_end = ENTRY_GAP_S + K_STAR
    for sweep in heads:
        lo = sweep["t_s"] - ISO_LOOKBACK_S
        hi = sweep["t_s"] + horizon_end
        isolated = True
        for other in heads:
            if other is sweep:
                continue
            if other["ticker"] != sweep["ticker"]:
                continue
            if lo <= other["t_s"] <= hi:
                isolated = False
                break
        flags = ["HEADLINE"]
        if isolated:
            flags.append("ISOLATED")
        if sweep["S"] >= THRESHOLD_S5K:
            flags.append("S5K")
        sweep["flags"] = sorted(flags)
    return {
        "schema": SWEEPS_SCHEMA,
        "threshold_headline": THRESHOLD_HEADLINE,
        "threshold_s5k": THRESHOLD_S5K,
        "key": list(SWEEP_KEY),
        "order": list(SWEEP_ORDER),
        "sweeps": heads,
    }


def per_side_per_event_counts(sweeps, events):
    counts = {}
    for event in events:
        counts[event] = {"YES": 0, "NO": 0, "YES_S5K": 0, "NO_S5K": 0}
    for sweep in sweeps:
        slot = counts.setdefault(
            sweep["event"], {"YES": 0, "NO": 0, "YES_S5K": 0, "NO_S5K": 0}
        )
        side = "YES" if sweep["d"] == 1 else "NO"
        slot[side] += 1
        if "S5K" in sweep["flags"]:
            slot[side + "_S5K"] += 1
    return counts
