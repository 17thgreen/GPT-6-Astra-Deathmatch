"""P1–P6 and P8. Fresh Random instances. No module-level random generator."""

import math

from .constants import B, DROPPED_LIMIT, SEED


def percentile7(sorted_values, probability):
    """Type-7 percentile. Caller handles len < 2."""
    count = len(sorted_values)
    position = probability * (count - 1)
    lo = math.floor(position)
    hi = math.ceil(position)
    if lo == hi:
        return sorted_values[lo]
    weight = position - lo
    return sorted_values[lo] * (1.0 - weight) + sorted_values[hi] * weight


def make_idx(n_events, draws=None, seed=None):
    """P3. One index, built before any statistic, from a fresh generator."""
    import random

    rng = random.Random(SEED if seed is None else seed)
    n_draws = B if draws is None else draws
    return [rng.choices(range(n_events), k=n_events) for _ in range(n_draws)]


def resample(events, stats, idx):
    """P5–P6. den <= 0 drops the draw. Fewer than 2 kept values leave L and U as None."""
    kept = []
    dropped = 0
    for draw in idx:
        den = math.fsum(stats.get(events[i], (0.0, 0.0))[0] for i in draw)
        num = math.fsum(stats.get(events[i], (0.0, 0.0))[1] for i in draw)
        if den <= 0.0:
            dropped += 1
            continue
        kept.append(num / den)
    kept.sort()
    if len(kept) < 2:
        low = high = None
    else:
        low = percentile7(kept, 0.025)
        high = percentile7(kept, 0.975)
    return {
        "kept_values": kept,
        "kept": len(kept),
        "dropped": dropped,
        "L": low,
        "U": high,
    }


def row_mean(events, lists, draw):
    """Naive row-level mean for one draw. Empty draw returns None."""
    values = []
    for index in draw:
        values.extend(lists.get(events[index], ()))
    if not values:
        return None
    return math.fsum(values) / len(values)


def sufficient_mean(events, stats, draw):
    den = math.fsum(stats.get(events[i], (0.0, 0.0))[0] for i in draw)
    num = math.fsum(stats.get(events[i], (0.0, 0.0))[1] for i in draw)
    if den <= 0.0:
        return None
    return num / den


def degenerate(low, high, dropped):
    """KD-19. U == L by float equality, or dropped resamples above the limit."""
    if low is None or high is None:
        return True
    if dropped > DROPPED_LIMIT:
        return True
    return low == high
