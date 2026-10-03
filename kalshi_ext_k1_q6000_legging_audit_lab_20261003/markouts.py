"""R18–R23 open-leg markouts. Quote mids only. Lee-Ready is refused."""

import bisect

from errors import LeeReadyRefused

PROXY_MAX_AGE_SECONDS = 300.0


def lee_ready(*_args, **_kwargs):
    raise LeeReadyRefused("Lee-Ready is refused")


def reject_lee_ready(key=None, call=None):
    blob = f"{key or ''} {call or ''}".lower().replace("-", "_").replace(" ", "_")
    if "lee_ready" in blob or "leeready" in blob:
        raise LeeReadyRefused(key or call)
    return False


class QuoteBook:
    """Latest quote with at <= t. No fallback to an older quote. No print mids."""

    def __init__(self):
        self._rows = {}
        self._ats = {}
        self.last_at = {}

    def note(self, ticker, at):
        previous = self.last_at.get(ticker)
        if previous is None or at > previous:
            self.last_at[ticker] = at

    def add_quote(self, row):
        reject_lee_ready(key=" ".join(row.keys()))
        ticker = row["ticker"]
        self.note(ticker, row["at"])
        self._rows.setdefault(ticker, []).append(
            (row["at"], row["asof"], row["bid"], row["ask"])
        )
        self._ats.setdefault(ticker, []).append(row["at"])

    def yes_mid(self, ticker, instant):
        """YES-side mid, or None when the latest quote is missing or invalid."""
        last = self.last_at.get(ticker)
        if last is None or instant > last:
            return None
        ats = self._ats.get(ticker)
        if not ats:
            return None
        index = bisect.bisect_right(ats, instant) - 1
        if index < 0:
            return None
        _at, asof, bid, ask = self._rows[ticker][index]
        if not (0 < bid < ask < 1):
            return None
        if not (0 <= instant - asof < PROXY_MAX_AGE_SECONDS):
            return None
        return (bid + ask) / 2.0


def outcome_mid(yes_mid, outcome):
    if yes_mid is None:
        return None
    if outcome == "yes":
        return yes_mid
    if outcome == "no":
        return 1.0 - yes_mid
    raise LeeReadyRefused(outcome)


def portion_markouts(portion, book, horizons, fee_per_contract, settlement):
    """Gross markout is mid_out - p_entry. Net subtracts the headline fee per contract.

    CLOSE is censored for the whole portion when any unit lacks a valid mid.
    """
    out = {}
    for horizon in horizons:
        yes = book.yes_mid(portion["ticker"], portion["t_open"] + horizon)
        mid = outcome_mid(yes, portion["outcome"])
        gross = None if mid is None else mid - portion["p_entry"]
        net = None if gross is None else gross - fee_per_contract
        out[str(horizon)] = {"gross": gross, "net": net}
    unit_ok = True
    weighted = 0.0
    weight = 0.0
    for size, t_close in portion["closes"]:
        yes = book.yes_mid(portion["ticker"], t_close)
        mid = outcome_mid(yes, portion["outcome"])
        if mid is None:
            unit_ok = False
            break
        weighted += size * (mid - portion["p_entry"])
        weight += size
    if unit_ok and weight > 0:
        gross = weighted / weight
        close = {"gross": gross, "net": gross - fee_per_contract}
    else:
        close = {"gross": None, "net": None}
    out["CLOSE"] = close
    if settlement is None:
        settle = {"gross": None, "net": None}
    else:
        gross = settlement - portion["p_entry"]
        settle = {"gross": gross, "net": gross - fee_per_contract}
    out["SETTLE"] = settle
    return out
