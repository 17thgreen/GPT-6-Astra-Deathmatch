"""R27–R30 label-free refusal gate. The 16-cell grid is sensitivity only."""

from constants import GATE_DEVIG, GATE_E, GATE_X, PRIMARY_GATE
from errors import LookaheadRefused

GRID_ROLE = "SENSITIVITY_ONLY_NEVER_SELECTION"
_MISSING = object()


def cell_key(x, exposure_floor, devig):
    return f"x={x:.2f}|E={int(exposure_floor)}|devig={devig}"


def iter_cells():
    for devig in GATE_DEVIG:
        for x in GATE_X:
            for exposure_floor in GATE_E:
                yield x, exposure_floor, devig


def is_primary(x, exposure_floor, devig):
    return (
        abs(x - PRIMARY_GATE["x"]) < 1e-12
        and abs(exposure_floor - PRIMARY_GATE["E"]) < 1e-12
        and devig == PRIMARY_GATE["devig"]
    )


def gate_on_fill(
    fill,
    *,
    p_cons,
    x,
    exposure_floor,
    tape=_MISSING,
    score=_MISSING,
    markout=_MISSING,
):
    """REFUSE iff dev < -x and |inventory_after| >= E.

    A null consensus anchor or a null mid is never refused.
    tape, score, and markout are rejected so the signature cannot see ahead.
    """
    if tape is not _MISSING or score is not _MISSING or markout is not _MISSING:
        raise LookaheadRefused("gate accepts no tape, score, or markout")
    m_open = fill.get("outcome_mid_at_fill", fill.get("m_open"))
    inventory = fill.get("inventory_after")
    if p_cons is None or m_open is None or inventory is None:
        return False
    dev = p_cons - m_open
    return dev < -x and abs(inventory) >= exposure_floor


def _row_at(row):
    if isinstance(row, dict):
        return row["at"]
    return row


def _truncate(rows, at):
    """Drop rows strictly after at. Numeric sequences are time-sorted pins and use bisect."""
    if not rows:
        return []
    if isinstance(rows[0], dict):
        return [row for row in rows if row["at"] <= at]
    import bisect
    return list(rows[: bisect.bisect_right(rows, at)])


def gate_from_context(fill, tape_rows, ledger_rows, *, p_cons, x, exposure_floor):
    """Recompute G after deleting rows with at > fill.at. Those rows are not read."""
    at = fill["at"]
    kept_tape = _truncate(tape_rows, at)
    kept_ledger = _truncate(ledger_rows, at)
    if (kept_tape and _row_at(kept_tape[-1]) > at) or (kept_ledger and _row_at(kept_ledger[-1]) > at):
        raise LookaheadRefused("future row survived truncation")
    return gate_on_fill(fill, p_cons=p_cons, x=x, exposure_floor=exposure_floor)


def portion_refused(portion, x, exposure_floor, devig):
    key = "dev_proportional" if devig == "proportional" else "dev_shin"
    dev = portion.get(key)
    if dev is None:
        return False
    return dev < -x and abs(portion["inventory_after"]) >= exposure_floor


def assignment_token(refused):
    """Invariance artifact token named by T01. Committed outputs say KEPT, not this token."""
    return "REFUSE" if refused else "KEEP"
