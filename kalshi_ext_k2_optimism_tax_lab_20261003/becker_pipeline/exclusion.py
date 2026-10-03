"""R32 exclusion. The trading-end clock is not read anywhere else."""

from shared.exceptions import IntegrityRefused, OpenTickerRefused
from shared.refusals import parse_timestamp


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


def assert_integrity(trades):
    seen = set()
    for row in trades:
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


def recompute_exclusion(markets, trades):
    """Ticker exclusion, then event closure.

    A market is open at trade fetch when close_time is after that ticker's
    maximum trade _fetched_at. That comparison is the only use of close_time.
    """
    assert_integrity(trades)
    fetch = {}
    n_rows = {}
    for row in trades:
        ticker = row["ticker"]
        n_rows[ticker] = n_rows.get(ticker, 0) + 1
        stamp = parse_timestamp(row["_fetched_at"])
        prev = fetch.get(ticker)
        if prev is None or stamp > prev:
            fetch[ticker] = stamp
    market_by = {}
    for market in markets:
        market_by[market["ticker"]] = market
    open_ids = set()
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
        if missing and not opened:
            closed_no.add(ticker)
        if opened or missing:
            direct.add(ticker)
    for ticker in n_rows:
        if ticker not in market_by:
            direct.add(ticker)
    members = {}
    for market in markets:
        members.setdefault(market["event_ticker"], set()).add(market["ticker"])
    for ticker in n_rows:
        if ticker not in market_by:
            members.setdefault(ticker.rsplit("-", 1)[0], set()).add(ticker)

    def event_of(ticker):
        if ticker in market_by:
            return market_by[ticker]["event_ticker"]
        return ticker.rsplit("-", 1)[0]

    excluded = set(direct)
    dirty = True
    while dirty:
        dirty = False
        for event, group in members.items():
            if group & excluded and not group <= excluded:
                excluded |= group
                dirty = True
    excluded_events = sorted(event for event, group in members.items() if group & excluded)
    excluded_rows = sum(n_rows.get(ticker, 0) for ticker in excluded)
    eligible_tickers = sorted(ticker for ticker in n_rows if ticker not in excluded)
    eligible_events = sorted({event_of(ticker) for ticker in eligible_tickers})
    eligible_rows = sum(n_rows.get(ticker, 0) for ticker in eligible_tickers)
    return {
        "excluded_tickers": sorted(excluded),
        "excluded_events": excluded_events,
        "open_at_trade_fetch_tickers": sorted(open_ids),
        "closed_no_result_tickers": sorted(closed_no),
        "n_excluded_tickers": len(excluded),
        "n_excluded_events": len(excluded_events),
        "n_excluded_rows": excluded_rows,
        "n_open_at_trade_fetch": len(open_ids),
        "n_closed_no_result": len(closed_no),
        "eligible_tickers": eligible_tickers,
        "eligible_events": eligible_events,
        "n_eligible_tickers": len(eligible_tickers),
        "n_eligible_events": len(eligible_events),
        "n_eligible_rows": eligible_rows,
        "level": "event",
    }


def assert_none_excluded(tickers, excluded):
    banned = set(excluded)
    for ticker in tickers:
        if ticker in banned:
            raise OpenTickerRefused(ticker)
