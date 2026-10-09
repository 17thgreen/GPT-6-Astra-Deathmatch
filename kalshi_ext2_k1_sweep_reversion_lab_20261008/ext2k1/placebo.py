"""R17 and KD-10. Own Random(20261008). RV stays fixed; side labels are shuffled."""

import math

from .bootstrap import percentile7
from .canonical import canonical_sha256
from .constants import K_STAR, N_PERM, SEED


def _contrast(pairs):
    no_values = [value for value, label in pairs if label == -1]
    yes_values = [value for value, label in pairs if label == 1]
    if not no_values or not yes_values:
        return None
    return math.fsum(no_values) / len(no_values) - math.fsum(yes_values) / len(yes_values)


def run_placebo(events, records):
    import random

    rng = random.Random(SEED)
    valid = [
        record
        for record in records
        if record["status"] == "OK" and record["RV"][str(K_STAR)] is not None
    ]
    by_event = {event: [record for record in valid if record["event"] == event] for event in events}
    observed = _contrast([(record["RV"][str(K_STAR)], record["d"]) for record in valid])
    draws = []
    for _ in range(N_PERM):
        pairs = []
        for event in events:
            labels = [record["d"] for record in by_event[event]]
            rng.shuffle(labels)
            pairs.extend(
                (record["RV"][str(K_STAR)], label)
                for record, label in zip(by_event[event], labels)
            )
        draws.append(_contrast(pairs))
    defined = sorted(value for value in draws if value is not None)
    if len(defined) >= 2:
        low = percentile7(defined, 0.025)
        high = percentile7(defined, 0.975)
    else:
        low = high = None
    if observed is None or not defined:
        share = None
    else:
        share = sum(1 for value in defined if abs(value) >= abs(observed)) / len(defined)
    return {
        "mode": "RV_FIXED_LABEL_PERMUTED",
        "D_obs": observed,
        "n_perm": N_PERM,
        "n_defined": len(defined),
        "perm_p025": low,
        "perm_p975": high,
        "share_abs_ge_obs": share,
        "D_list_sha256": canonical_sha256(draws),
    }
