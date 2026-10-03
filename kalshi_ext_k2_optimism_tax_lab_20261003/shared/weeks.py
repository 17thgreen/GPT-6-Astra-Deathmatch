"""Game week from the event-ticker date. close_time is not used."""

import datetime as dt
import math

ANCHOR = dt.date(2025, 9, 2)
_MONTHS = {
    "JAN": 1, "FEB": 2, "MAR": 3, "APR": 4, "MAY": 5, "JUN": 6,
    "JUL": 7, "AUG": 8, "SEP": 9, "OCT": 10, "NOV": 11, "DEC": 12,
}


def ticker_date_from_event(event_ticker):
    """The YYMMMDD token, e.g. KXNFLGAME-25SEP07AAAA -> 2025-09-07."""
    token = event_ticker.split("-", 1)[1][:7]
    year = 2000 + int(token[:2])
    month = _MONTHS[token[2:5]]
    day = int(token[5:7])
    return dt.date(year, month, day)


def week_from_date(day):
    """floor((day - 2025-09-02) / 7) + 1, or PRE when day is before the anchor."""
    if day < ANCHOR:
        return "PRE", None
    delta = (day - ANCHOR).days
    index = math.floor(delta / 7) + 1
    return f"W{index:02d}", index


def week_from_event_ticker(event_ticker):
    return week_from_date(ticker_date_from_event(event_ticker))


def is_complete_week(n_eligible_events, threshold=8):
    return n_eligible_events >= threshold
