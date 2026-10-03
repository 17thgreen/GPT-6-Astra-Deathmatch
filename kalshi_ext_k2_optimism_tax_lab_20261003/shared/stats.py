"""Type-7 quantiles, sample SD, and Spearman rho. No data access."""

import math


def q7(sorted_values, probability):
    n = len(sorted_values)
    if n == 0:
        return None
    if n == 1:
        return sorted_values[0]
    h = (n - 1) * probability
    lo = math.floor(h)
    hi = min(lo + 1, n - 1)
    return sorted_values[lo] + (h - lo) * (sorted_values[hi] - sorted_values[lo])


def sample_sd(values):
    n = len(values)
    if n < 2:
        return None
    mean = math.fsum(values) / n
    var = math.fsum((value - mean) ** 2 for value in values) / (n - 1)
    return math.sqrt(var)


def _ranks(values):
    order = sorted(range(len(values)), key=lambda i: values[i])
    ranks = [0.0] * len(values)
    i = 0
    while i < len(values):
        j = i
        while j + 1 < len(values) and values[order[j + 1]] == values[order[i]]:
            j += 1
        average = (i + 1 + j + 1) / 2.0
        for k in range(i, j + 1):
            ranks[order[k]] = average
        i = j + 1
    return ranks


def spearman(xs, ys):
    if len(xs) != len(ys) or len(xs) < 2:
        return None
    rx = _ranks(xs)
    ry = _ranks(ys)
    mx = math.fsum(rx) / len(rx)
    my = math.fsum(ry) / len(ry)
    num = math.fsum((a - mx) * (b - my) for a, b in zip(rx, ry))
    dx = math.sqrt(math.fsum((a - mx) ** 2 for a in rx))
    dy = math.sqrt(math.fsum((b - my) ** 2 for b in ry))
    if dx == 0 or dy == 0:
        return None
    return num / (dx * dy)
