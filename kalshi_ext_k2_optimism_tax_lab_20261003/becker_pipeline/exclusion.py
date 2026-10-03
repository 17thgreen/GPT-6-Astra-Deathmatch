"""R32 exclusion. The trading-end clock is not read anywhere else."""

from shared.exceptions import IntegrityRefused, OpenTickerRefused
from shared.refusals import parse_timestamp

EXPERIMENT_ID = "EXT-K2-OPTIMISM-TAX-DEPENDENCE-STRESS"
LIST_KEYS = (
    "excluded_events",
    "excluded_tickers_event_level",
    "excluded_tickers_ticker_level",
    "no_yes_no_result_closed_tickers",
    "no_yes_no_result_open_tickers",
    "open_at_trade_fetch_tickers",
    "orphan_trade_tickers",
)


def trade_columns():
    return [
        "trade_id", "ticker", "count", "yes_price", "no_price",
        "taker_side", "created_time", "_fetched_at",
    ]


def market_columns():
    return [
        "ticker", "event_ticker", "status", "result", "close_time",
        "_fetched_at", "volume",
    ]


def assert_integrity_row(row, seen):
    for key in ("trade_id", "ticker", "count", "yes_price", "no_price", "taker_side"):
        if row.get(key) is None:
            raise IntegrityRefused(key)
    if row["trade_id"] in seen:
        raise IntegrityRefused("duplicate trade_id")
    seen.add(row["trade_id"])
    if row["yes_price"] + row["no_price"] != 100:
        raise IntegrityRefused("yes_plus_no")
    if not isinstance(row["yes_price"], int) or not 1 <= row["yes_price"] <= 99:
        raise IntegrityRefused("yes_price")
    if row["count"] <= 0:
        raise IntegrityRefused("count")
    if row["taker_side"] not in ("yes", "no"):
        raise IntegrityRefused("taker_side")


def empty_scan():
    return {"seen": set(), "fetch": {}, "n_rows": {}}


def note_trade(scan, row):
    """Integrity plus per-ticker fetch max and row count. The row is not retained."""
    assert_integrity_row(row, scan["seen"])
    ticker = row["ticker"]
    scan["n_rows"][ticker] = scan["n_rows"].get(ticker, 0) + 1
    stamp = parse_timestamp(row["_fetched_at"])
    prev = scan["fetch"].get(ticker)
    if prev is None or stamp > prev:
        scan["fetch"][ticker] = stamp


def exclusion_from_scan(markets, scan, source_trades_sha256="", source_markets_sha256="", rule=""):
    """Build the pinned exclusion document from ticker aggregates.

    A market is open at trade fetch when close_time is after that ticker's
    maximum trade _fetched_at. That comparison is the only use of close_time.
    """
    fetch = scan["fetch"]
    n_rows = scan["n_rows"]
    market_by = {}
    for market in markets:
        market_by[market["ticker"]] = market
    open_ids = set()
    missing_open = set()
    closed_no = set()
    direct = set()
    for ticker, market in market_by.items():
        outcome = market.get("result")
        missing = outcome not in ("yes", "no")
        opened = False
        if ticker in fetch:
            # close_time is not a trading end and is not used to window rows.
            if parse_timestamp(market["close_time"]) > fetch[ticker]:
                opened = True
        if opened:
            open_ids.add(ticker)
        if opened and missing:
            missing_open.add(ticker)
        if missing and not opened:
            closed_no.add(ticker)
        if opened or missing:
            direct.add(ticker)
    orphans = set()
    for ticker in n_rows:
        if ticker not in market_by:
            orphans.add(ticker)
            direct.add(ticker)
    members = {}
    for market in markets:
        members.setdefault(market["event_ticker"], set()).add(market["ticker"])
    for ticker in n_rows:
        if ticker not in market_by:
            members.setdefault(ticker.rsplit("-", 1)[0], set()).add(ticker)
    excluded = set(direct)
    dirty = True
    while dirty:
        dirty = False
        for group in members.values():
            if group & excluded and not group <= excluded:
                excluded |= group
                dirty = True
    excluded_events = sorted(event for event, group in members.items() if group & excluded)
    return {
        "excluded_events": excluded_events,
        "excluded_tickers_event_level": sorted(excluded),
        "excluded_tickers_ticker_level": sorted(direct),
        "experiment_id": EXPERIMENT_ID,
        "no_yes_no_result_closed_tickers": sorted(closed_no),
        "no_yes_no_result_open_tickers": sorted(missing_open),
        "open_at_trade_fetch_tickers": sorted(open_ids),
        "orphan_trade_tickers": sorted(orphans),
        "rule": rule,
        "source_markets_sha256": source_markets_sha256,
        "source_trades_sha256": source_trades_sha256,
    }


def recompute_exclusion(markets, trades, source_trades_sha256="", source_markets_sha256="", rule=""):
    scan = empty_scan()
    for row in trades:
        note_trade(scan, row)
    return exclusion_from_scan(
        markets, scan,
        source_trades_sha256=source_trades_sha256,
        source_markets_sha256=source_markets_sha256,
        rule=rule,
    )


def summarize_counts(doc, n_rows):
    """Row and ticker counts derived from the exclusion lists. Not part of the pinned document."""

    def rows(ids):
        return sum(n_rows.get(ticker, 0) for ticker in ids)

    excluded = set(doc["excluded_tickers_event_level"])
    eligible = [ticker for ticker in n_rows if ticker not in excluded]
    return {
        "n_open_tickers": len(doc["open_at_trade_fetch_tickers"]),
        "n_open_rows": rows(doc["open_at_trade_fetch_tickers"]),
        "n_open_missing": len(doc["no_yes_no_result_open_tickers"]),
        "n_closed_tickers": len(doc["no_yes_no_result_closed_tickers"]),
        "n_closed_rows": rows(doc["no_yes_no_result_closed_tickers"]),
        "n_orphan_tickers": len(doc["orphan_trade_tickers"]),
        "n_excluded_tickers_event": len(doc["excluded_tickers_event_level"]),
        "n_excluded_tickers_direct": len(doc["excluded_tickers_ticker_level"]),
        "n_excluded_events": len(doc["excluded_events"]),
        "n_excluded_rows": rows(doc["excluded_tickers_event_level"]),
        "n_eligible_tickers": len(eligible),
        "n_eligible_rows": rows(eligible),
        "n_traded_tickers": len(n_rows),
        "n_traded_rows": sum(n_rows.values()),
    }


def assert_none_excluded(tickers, excluded):
    banned = set(excluded)
    for ticker in tickers:
        if ticker in banned:
            raise OpenTickerRefused(ticker)
