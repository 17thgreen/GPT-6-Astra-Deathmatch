"""R18 and KD-11. The only module that reads fill outcome fields."""

import math

from .errors import OutcomeFieldRefused
from .metrics import side_name

_RESULT_KEYS = ("result", "settlement", "settled")
_ALLOWED = ("outcome", "outcome_mid_at_fill")


def guard_row(row, *, allow_fill_fields):
    for key in row:
        if key in _RESULT_KEYS:
            raise OutcomeFieldRefused(key)
        if key in _ALLOWED and not allow_fill_fields:
            raise OutcomeFieldRefused(key)
    return row


def join(sweeps, fills):
    """Maker fills on the same ticker inside the closed [t_s-300, t_s+300] window."""
    joined = []
    for sweep in sweeps:
        matched = []
        for fill in fills:
            guard_row(fill, allow_fill_fields=True)
            if fill.get("kind") != "maker":
                continue
            if fill["ticker"] != sweep["ticker"]:
                continue
            if sweep["t_s"] - 300 <= fill["at"] <= sweep["t_s"] + 300:
                matched.append(fill)
        if not matched:
            continue
        mids = [
            fill["outcome_mid_at_fill"]
            for fill in matched
            if fill["outcome_mid_at_fill"] is not None
        ]
        joined.append(
            {
                "sweep_id": sweep["sweep_id"],
                "side": side_name(sweep["d"]),
                "n_fills": len(matched),
                "contracts": math.fsum(fill["size"] for fill in matched),
                "n_fill_outcome_yes": sum(1 for fill in matched if fill["outcome"] == "yes"),
                "n_fill_outcome_no": sum(1 for fill in matched if fill["outcome"] == "no"),
                "mean_outcome_mid_at_fill": None if not mids else math.fsum(mids) / len(mids),
                "mean_resting_seconds": math.fsum(fill["resting_seconds"] for fill in matched)
                / len(matched),
                "n_paired": sum(1 for fill in matched if fill["paired"] is True),
            }
        )
    return joined
