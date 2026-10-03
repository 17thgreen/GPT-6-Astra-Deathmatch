"""FIFO opening portions. K1 R04–R07, applied to the recorded 000 ledger."""

from collections import defaultdict, deque

from shared.exceptions import StructureDrift

PAIR_TOL = 1e-6
OPEN_TOL = 1e-8


def reconstruct(fills, markets):
    """Return portions, UCH by the integral, UCH by FIFO, and close slices.

    Fills are processed in ledger order. A taker remainder is structure drift.
    """
    coverage_end = max(row["kickoff"] - 10800 for row in markets.values()) + 300
    kickoff_by_event = {}
    for ticker, row in markets.items():
        event = row["event"]
        kickoff = row["kickoff"]
        if event in kickoff_by_event and abs(kickoff_by_event[event] - kickoff) > PAIR_TOL:
            raise StructureDrift("kickoff disagrees inside " + event)
        kickoff_by_event[event] = kickoff

    lots = defaultdict(deque)
    portions = []
    running = defaultdict(float)
    integral = defaultdict(float)
    last = {}
    for index, fill in enumerate(fills):
        event = fill["event"]
        if event in last:
            integral[event] += abs(last[event][1]) * (fill["at"] - last[event][0])
        signed = fill["direction"] * fill["size"]
        running[event] += signed
        if abs(running[event] - fill["inventory_after"]) > PAIR_TOL:
            raise StructureDrift("inventory_after mismatch at row " + str(index))
        expected_direction = markets[fill["ticker"]]["direction"] * (1 if fill["outcome"] == "yes" else -1)
        if expected_direction != fill["direction"]:
            raise StructureDrift("direction mismatch at row " + str(index))
        last[event] = (fill["at"], fill["inventory_after"])
        pending = fill["size"]
        book = lots[event]
        while pending > OPEN_TOL and book and book[0]["direction"] != fill["direction"]:
            lot = book[0]
            take = pending if pending < lot["size_remaining"] else lot["size_remaining"]
            lot["closes"].append({"at": fill["at"], "size": take, "kind": fill["kind"]})
            lot["size_remaining"] -= take
            pending -= take
            if lot["size_remaining"] < OPEN_TOL:
                book.popleft()
        if pending > OPEN_TOL:
            if fill["kind"] != "maker":
                raise StructureDrift("taker opening portion")
            portion = {
                "direction": fill["direction"],
                "size_open": pending,
                "size_remaining": pending,
                "t_open": fill["at"],
                "ticker": fill["ticker"],
                "outcome": fill["outcome"],
                "p_entry": fill["price"],
                "order_id": fill["order_id"],
                "row_index": index,
                "inventory_after": fill["inventory_after"],
                "m_open": fill.get("outcome_mid_at_fill"),
                "event": event,
                "kind": fill["kind"],
                "fee": fill.get("fee"),
                "ledger_size": fill["size"],
                "closes": [],
            }
            book.append(portion)
            portions.append(portion)

    residual = 0.0
    fifo_area = 0.0
    for portion in portions:
        for sliver in portion["closes"]:
            fifo_area += sliver["size"] * (sliver["at"] - portion["t_open"])
        residual += max(0.0, portion["size_remaining"])
    for event, (at, inventory) in last.items():
        end = min(coverage_end, kickoff_by_event[event] - 10800)
        integral[event] += abs(inventory) * max(0.0, end - at)
        # Unconsumed units close at T_end. Expected residual is 0.
    if residual > OPEN_TOL:
        for portion in portions:
            if portion["size_remaining"] > OPEN_TOL:
                end = min(coverage_end, kickoff_by_event[portion["event"]] - 10800)
                portion["closes"].append({
                    "at": end, "size": portion["size_remaining"], "kind": "window_end",
                })
                fifo_area += portion["size_remaining"] * max(0.0, end - portion["t_open"])
    uch_integral = sum(integral.values()) / 3600.0
    uch_fifo = fifo_area / 3600.0
    return {
        "portions": portions,
        "uch_integral": uch_integral,
        "uch_fifo": uch_fifo,
        "residual_contracts": residual,
        "coverage_end": coverage_end,
        "n_portions": len(portions),
    }
