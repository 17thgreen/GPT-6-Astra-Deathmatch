"""R07, R08, R10, R12 quote mids. KD-6 latest-then-validate. KD-7 last-row censor.

No fallback to an older quote. Prints never supply a mid. Lee-Ready is refused.
"""

import bisect

from .constants import ENTRY_GAP_S, HORIZONS, STALE_SECONDS
from .errors import LeeReadyRefused


def lee_ready(*_args, **_kwargs):
    raise LeeReadyRefused("Lee-Ready is refused")


def quote_valid(asof, bid, ask, t):
    return (0 < bid < ask < 1) and (0 <= (t - asof) < STALE_SECONDS)


class QuoteBook:
    """Latest quote with at <= t, then validate. No older-quote fallback."""

    def __init__(self, rows):
        self._quotes = {}
        self._ats = {}
        self.last_at = {}
        for row in rows:
            ticker = row["ticker"]
            at = row["at"]
            previous = self.last_at.get(ticker)
            if previous is None or at > previous:
                self.last_at[ticker] = at
            if row.get("kind") == "quote":
                self._quotes.setdefault(ticker, []).append(
                    (at, row["asof"], row["bid"], row["ask"])
                )
        for ticker, quotes in self._quotes.items():
            quotes.sort(key=lambda item: (item[0], item[1]))
            self._ats[ticker] = [item[0] for item in quotes]

    def _index(self, ticker, t, *, strict):
        ats = self._ats.get(ticker)
        if not ats:
            return None
        if strict:
            index = bisect.bisect_left(ats, t) - 1
        else:
            index = bisect.bisect_right(ats, t) - 1
        if index < 0:
            return None
        return index

    def mid_at(self, ticker, t):
        """R07 mid at t, censored when t is past the ticker's last row (KD-7)."""
        last = self.last_at.get(ticker)
        if last is None or t > last:
            return None, None
        index = self._index(ticker, t, strict=False)
        if index is None:
            return None, None
        row = self._quotes[ticker][index]
        _at, asof, bid, ask = row
        if not quote_valid(asof, bid, ask, t):
            return None, None
        return (bid + ask) / 2.0, row

    def pre_mid(self, ticker, t_s):
        """R08. Latest row with at < t_s, validated at t_s. No fallback (KD-6)."""
        index = self._index(ticker, t_s, strict=True)
        if index is None:
            return None
        _at, asof, bid, ask = self._quotes[ticker][index]
        if not quote_valid(asof, bid, ask, t_s):
            return None
        return (bid + ask) / 2.0

    def entry_row(self, ticker, t_s):
        """R10. Latest valid row with at <= t_e and asof > t_s. No fallback."""
        t_e = t_s + ENTRY_GAP_S
        last = self.last_at.get(ticker)
        if last is None or t_e > last:
            return None
        index = self._index(ticker, t_e, strict=False)
        if index is None:
            return None
        row = self._quotes[ticker][index]
        _at, asof, bid, ask = row
        if not (asof > t_s) or not quote_valid(asof, bid, ask, t_e):
            return None
        return row


def rv_value(d, m_k, m_e):
    return -d * (m_k - m_e)


def tmo_value(d, m_k, bid_e, ask_e):
    if d == -1:
        return m_k - ask_e
    return bid_e - m_k


def classify_sweeps(sweeps, rows):
    """Per-sweep mids. KD-5: NO_PRE_MID outranks NO_ENTRY_MID outranks OK."""
    book = QuoteBook(rows)
    records = []
    for sweep in sweeps:
        ticker = sweep["ticker"]
        t_s = sweep["t_s"]
        d = sweep["d"]
        t_e = t_s + ENTRY_GAP_S
        record = {
            "sweep_id": sweep["sweep_id"],
            "event": sweep["event"],
            "d": d,
            "S": sweep["S"],
            "flags": list(sweep["flags"]),
        }
        m_pre = book.pre_mid(ticker, t_s)
        entry = book.entry_row(ticker, t_s)
        record["m_pre"] = m_pre
        if entry is None:
            record["status"] = "NO_PRE_MID" if m_pre is None else "NO_ENTRY_MID"
            record["m_E"] = None
            record["bid_E"] = None
            record["ask_E"] = None
            record["entry_asof"] = None
            record["m"] = {str(k): None for k in HORIZONS}
        else:
            _at, asof, bid, ask = entry
            m_e = (bid + ask) / 2.0
            mids = {}
            for horizon in HORIZONS:
                mid, row = book.mid_at(ticker, t_e + horizon)
                if mid is None or not (row[1] > asof):
                    mids[str(horizon)] = None
                else:
                    mids[str(horizon)] = mid
            record["m_E"] = m_e
            record["bid_E"] = bid
            record["ask_E"] = ask
            record["entry_asof"] = asof
            record["m"] = mids
            record["status"] = "NO_PRE_MID" if m_pre is None else "OK"
        reversion = {}
        markout = {}
        impact = {}
        for horizon in HORIZONS:
            key = str(horizon)
            if record["status"] != "OK" or record["m"][key] is None:
                reversion[key] = None
                markout[key] = None
                impact[key] = None
                continue
            mid = record["m"][key]
            reversion[key] = rv_value(d, mid, record["m_E"])
            markout[key] = tmo_value(d, mid, record["bid_E"], record["ask_E"])
            impact[key] = d * (mid - record["m_pre"])
        record["RV"] = reversion
        record["TMO"] = markout
        if record["status"] != "OK":
            record["I_E"] = None
        else:
            record["I_E"] = d * (record["m_E"] - record["m_pre"])
        record["I_Ek"] = impact
        records.append(record)
    return records
