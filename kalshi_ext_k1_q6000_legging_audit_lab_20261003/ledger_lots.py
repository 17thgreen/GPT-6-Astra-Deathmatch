"""R04–R08 FIFO opening portions and unhedged contract-hours."""

from collections import defaultdict, deque

from errors import ClosedUniverseRefused, StructureDrift
from refusals import assert_not_holdout, screen_clock_row


def team_for_direction(markets, event, direction):
    hits = [
        ticker.split("-")[-1]
        for ticker, meta in markets.items()
        if meta["event"] == event and meta["direction"] == direction
    ]
    if len(hits) != 1:
        raise StructureDrift(f"team_long {event} {direction} {hits}")
    return hits[0]


def coverage_bounds(markets):
    kickoffs = {}
    for meta in markets.values():
        kickoffs[meta["event"]] = meta["kickoff"]
    if not kickoffs:
        raise ClosedUniverseRefused("no markets")
    coverage_end = max(kickoff - 10800.0 for kickoff in kickoffs.values()) + 300.0
    ends = {
        event: min(coverage_end, kickoff - 10800.0)
        for event, kickoff in kickoffs.items()
    }
    return coverage_end, ends


def build_lots(fills, markets, week_membership):
    """FIFO lots identical to queue_policies.account_fill. Fills stay in file order."""
    allowed_events = set(week_membership)
    for event in allowed_events:
        assert_not_holdout(event=event)
    coverage_end, ends = coverage_bounds(markets)
    inventory = defaultdict(float)
    clock = {}
    area = defaultdict(float)
    lots = defaultdict(deque)
    portions = []
    opening_contracts = 0.0
    closing_contracts = 0.0
    maker_closing = 0.0
    taker_closing = 0.0
    for index, row in enumerate(fills):
        screen_clock_row(row)
        event = row["event"]
        ticker = row["ticker"]
        if event not in allowed_events or ticker not in markets or markets[ticker]["event"] != event:
            raise ClosedUniverseRefused(ticker)
        now = row["at"]
        direction = row["direction"]
        quantity = row["size"]
        previous = inventory[event]
        if event in clock:
            area[event] += abs(previous) * (now - clock[event])
        clock[event] = now
        inventory[event] += direction * quantity
        if abs(inventory[event]) < 1e-8:
            inventory[event] = 0.0
        if abs(inventory[event] - row["inventory_after"]) > 1e-6:
            raise StructureDrift(f"inventory_after row {index}")
        pending = quantity
        book = lots[event]
        while pending > 1e-8 and book and book[0]["direction"] != direction:
            lot = book[0]
            paired = min(pending, lot["size"])
            lot["portion"]["closes"].append((paired, now))
            closing_contracts += paired
            if row["kind"] == "maker":
                maker_closing += paired
            else:
                taker_closing += paired
            pending -= paired
            lot["size"] -= paired
            if lot["size"] < 1e-8:
                book.popleft()
        if pending > 1e-8:
            if row["kind"] != "maker":
                raise StructureDrift("taker opening portion")
            portion = {
                "portion_id": str(index),
                "row_index": index,
                "event": event,
                "ticker": ticker,
                "outcome": row["outcome"],
                "direction": direction,
                "order_id": row["order_id"],
                "kind": row["kind"],
                "t_open": now,
                "size": pending,
                "fill_size": quantity,
                "p_entry": row["price"],
                "m_open": row["outcome_mid_at_fill"],
                "inventory_after": row["inventory_after"],
                "team_long": team_for_direction(markets, event, direction),
                "ledger_fee": row["fee"],
                "closes": [],
            }
            portions.append(portion)
            opening_contracts += pending
            book.append({"direction": direction, "size": pending, "portion": portion})
    residual = 0.0
    for event, book in lots.items():
        for lot in book:
            if lot["size"] > 1e-8:
                residual += lot["size"]
                lot["portion"]["closes"].append((lot["size"], ends[event]))
    for event, at in clock.items():
        area[event] += abs(inventory[event]) * max(0.0, ends[event] - at)
    uch_integral = sum(area.values()) / 3600.0
    uch_fifo = 0.0
    premium_hours = 0.0
    for portion in portions:
        portion_uch = 0.0
        portion_premium = 0.0
        for size, t_close in portion["closes"]:
            dt = t_close - portion["t_open"]
            portion_uch += size * dt / 3600.0
            portion_premium += size * portion["p_entry"] * dt / 3600.0
        portion["uch"] = portion_uch
        portion["premium_hours"] = portion_premium
        uch_fifo += portion_uch
        premium_hours += portion_premium
    return {
        "portions": portions,
        "coverage_end": coverage_end,
        "t_end": ends,
        "uch_integral": uch_integral,
        "uch_fifo": uch_fifo,
        "premium_hours": premium_hours,
        "opening_contracts": opening_contracts,
        "closing_contracts": closing_contracts,
        "maker_closing_contracts": maker_closing,
        "taker_closing_contracts": taker_closing,
        "open_at_window_end_contracts": residual,
        "inventory_terminal": dict(inventory),
    }
