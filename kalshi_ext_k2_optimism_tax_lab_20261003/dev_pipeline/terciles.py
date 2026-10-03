"""Label-free taker-YES terciles. Inputs are (ticker, at, taker_side, size) only."""

import math

from shared.canonical import canon_bytes, canon_sha256
from shared.exceptions import LabelInputRefused

EXPERIMENT_ID = "EXT-K2-OPTIMISM-TAX-DEPENDENCE-STRESS"
TAPE_SHA = "cd300e664c2c5f2ff344c4b1eb17dd3f8e5f3326168b9dd8e3ade94a3a7382b4"
MIN_TRADES = 5
PINNED_C1 = 0.9271702456462422
PINNED_C2 = 0.989881659505818
PINNED_E1 = 0.9126590461375717
PINNED_E2 = 0.9359888338062846
PINNED_BUCKET_SHA = "9acb52888a411be801bb701d12f3982e1e2f1c884accc162ca6f1f1d8fef6a14"

_FLOW_KEYS = frozenset({"ticker", "at", "taker_side", "size"})
_LABEL_KEYS = frozenset({
    "bid", "ask", "asof", "kind", "outcome", "outcome_mid_at_fill", "price",
    "result", "score", "home_score", "away_score", "fee", "direction",
    "yes_price", "no_price", "close_time",
})


def q7(sorted_values, probability):
    """Type-7 linear quantile. sorted_values is ascending."""
    n = len(sorted_values)
    if n == 0:
        raise LabelInputRefused("empty quantile input")
    if n == 1:
        return sorted_values[0]
    h = (n - 1) * probability
    lo = math.floor(h)
    hi = min(lo + 1, n - 1)
    return sorted_values[lo] + (h - lo) * (sorted_values[hi] - sorted_values[lo])


def assign_label(share, c1, c2):
    if share <= c1:
        return "T1_LOW"
    if share <= c2:
        return "T2_MID"
    return "T3_HIGH"


def _reject_label_kwargs(quote, fill, score, result):
    if quote is not None or fill is not None or score is not None or result is not None:
        raise LabelInputRefused("terciles accept flow rows only")


def _as_flow(row):
    if isinstance(row, (tuple, list)):
        if len(row) != 4:
            raise LabelInputRefused("flow tuple is (ticker, at, taker_side, size)")
        ticker, at, taker_side, size = row
        return ticker, float(at), taker_side, float(size)
    keys = set(row.keys())
    extra = keys - _FLOW_KEYS
    if extra & _LABEL_KEYS or extra:
        raise LabelInputRefused("flow row has non-flow keys: " + ",".join(sorted(extra)))
    if keys != _FLOW_KEYS:
        raise LabelInputRefused("flow row is missing a flow key")
    return row["ticker"], float(row["at"]), row["taker_side"], float(row["size"])


def flow_terciles(rows, quote=None, fill=None, score=None, result=None):
    """Bucket and event terciles from flow rows only. Labels are refused."""
    _reject_label_kwargs(quote, fill, score, result)
    buckets = {}
    events = {}
    for row in rows:
        ticker, at, side, size = _as_flow(row)
        hour = int(math.floor(at / 3600.0))
        event = ticker.rsplit("-", 1)[0]
        for key, store in (((ticker, hour), buckets), (event, events)):
            slot = store.get(key)
            if slot is None:
                slot = {"n": 0, "y": [], "a": []}
                store[key] = slot
            slot["n"] += 1
            slot["a"].append(size)
            if side == "yes":
                slot["y"].append(size)
    table = []
    for (ticker, hour), slot in sorted(buckets.items()):
        contracts = math.fsum(slot["a"])
        yes_contracts = math.fsum(slot["y"])
        share = (yes_contracts / contracts) if contracts > 0 else None
        table.append({
            "ticker": ticker,
            "hour_utc_epoch_div_3600": hour,
            "n_trades": slot["n"],
            "contracts": contracts,
            "yes_contracts": yes_contracts,
            "share": share,
        })
    eligible = sorted(
        row["share"] for row in table
        if row["n_trades"] >= MIN_TRADES and row["contracts"] > 0
    )
    c1 = q7(eligible, 1.0 / 3.0)
    c2 = q7(eligible, 2.0 / 3.0)
    for row in table:
        if row["n_trades"] >= MIN_TRADES and row["contracts"] > 0:
            row["tercile"] = assign_label(row["share"], c1, c2)
        else:
            row["tercile"] = "UNCLASSIFIED"
    event_share = {}
    for event, slot in sorted(events.items()):
        event_share[event] = math.fsum(slot["y"]) / math.fsum(slot["a"])
    ordered = sorted(event_share.values())
    e1 = q7(ordered, 1.0 / 3.0)
    e2 = q7(ordered, 2.0 / 3.0)
    event_tercile = {event: assign_label(share, e1, e2) for event, share in event_share.items()}
    return {
        "rows": table,
        "c1": c1,
        "c2": c2,
        "e1": e1,
        "e2": e2,
        "event_share": event_share,
        "event_tercile": event_tercile,
        "n_eligible": len(eligible),
    }


def bucket_document(built, tape_sha=TAPE_SHA):
    return {
        "experiment_id": EXPERIMENT_ID,
        "source_tape_sha256": tape_sha,
        "unit": "ticker x UTC clock hour floor(at/3600)",
        "share_formula": "fsum(size | taker_side=yes)/fsum(size), IEEE double",
        "rows": built["rows"],
    }


def bucket_lookup(built):
    return {
        (row["ticker"], row["hour_utc_epoch_div_3600"]): row["tercile"]
        for row in built["rows"]
    }


def trailing_share(trades_for_ticker, t_fill):
    """Share on [t_fill-3600, t_fill). trades_for_ticker is sorted by at.

    Returns (share or None, n_trades, tercile). Cuts are the primary c1/c2,
    supplied by the caller via the tuple's closure in portion_labels.
    """
    lo = t_fill - 3600.0
    # Binary search. trades are (at, side, size).
    n = len(trades_for_ticker)
    left = 0
    right = n
    # first index with at >= lo
    a, b = 0, n
    while a < b:
        mid = (a + b) // 2
        if trades_for_ticker[mid][0] < lo:
            a = mid + 1
        else:
            b = mid
    left = a
    a, b = left, n
    while a < b:
        mid = (a + b) // 2
        if trades_for_ticker[mid][0] < t_fill:
            a = mid + 1
        else:
            b = mid
    window = trades_for_ticker[left:a]
    if len(window) < MIN_TRADES:
        return None, len(window), "UNCLASSIFIED"
    yes = math.fsum(size for at, side, size in window if side == "yes")
    total = math.fsum(size for at, side, size in window)
    if total <= 0:
        return None, len(window), "UNCLASSIFIED"
    return yes / total, len(window), None


def index_trades(flow_rows):
    by_ticker = {}
    for row in flow_rows:
        ticker, at, side, size = _as_flow(row)
        by_ticker.setdefault(ticker, []).append((at, side, size))
    for ticker in by_ticker:
        by_ticker[ticker].sort()
    return by_ticker


def portion_labels(portions, built, trade_index):
    """Primary, secondary, and trailing-60 labels for opening portions.

    A portion needs ticker, at, and event. Markout fields are ignored.
    """
    lookup = bucket_lookup(built)
    out = []
    for portion in portions:
        ticker = portion["ticker"]
        at = float(portion["t_open"])
        hour = int(math.floor(at / 3600.0))
        primary = lookup.get((ticker, hour), "UNCLASSIFIED")
        secondary = built["event_tercile"].get(portion["event"], "UNCLASSIFIED")
        share, n_trades, early = trailing_share(trade_index.get(ticker, []), at)
        if early is None:
            sensitivity = assign_label(share, built["c1"], built["c2"])
        else:
            sensitivity = early
        out.append({
            "row_index": portion["row_index"],
            "primary": primary,
            "secondary": secondary,
            "sensitivity": sensitivity,
            "sensitivity_n_trades": n_trades,
        })
    return out
