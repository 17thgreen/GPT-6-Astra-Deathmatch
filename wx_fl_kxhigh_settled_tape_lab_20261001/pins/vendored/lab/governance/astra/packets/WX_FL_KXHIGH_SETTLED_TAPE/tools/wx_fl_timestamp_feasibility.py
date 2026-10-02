#!/usr/bin/env python3
"""WX-FL-KXHIGH-SETTLED-TAPE: timestamp/status-only feasibility + gap-mapping counts (freeze-time tool).

READS ONLY (never price / side / result value / ROI columns):
  kalshi_markets: ticker, event_ticker, series_ticker, received_at, status, close_time,
                  (result IS NOT NULL AND result != '') as a 0/1 flag,
                  settlement_ts and open_time keys of the zlib raw JSON (all other keys discarded unread)
  kalshi_trades:  trade_id, ticker, created_time, received_at
  polls:          stream, key, url (ticker/min_ts/cursor only), requested_at, ok, n_items, http_status
  gaps:           all columns (stream, key, started_at, ended_at, reason, detail, n_polls)
  runs:           all columns
Opens the snapshot with mode=ro&immutable=1 and verifies its sha256 first. No network.
Usage: python3 wx_fl_timestamp_feasibility.py <snapshot archive.sqlite> <expected_sha256> [out.json]
"""
import hashlib, json, sqlite3, sys, re, bisect, zlib
from datetime import datetime, timezone
from collections import Counter, defaultdict

W0 = "2026-09-27T00:00:00Z"            # ADMIT-1 enforced window start (ruling ac7cfe63 / 0e37f91b ruling 3)
W1 = "2026-09-30T04:00:00Z"
SERIES = ("KXHIGHCHI", "KXHIGHLAX", "KXHIGHMIA", "KXHIGHNY")
TRADE_STREAMS_PER_TICKER = ("kalshi_trades", "kalshi_trades_budget")
ALL_TICKER_STREAMS = ("kalshi_all", "collector")
BUDGET_PAD_S = 1800 + 120              # GM-LIT-PAD only: budget gap opens once lateness > 1800 s target (+120 s loop slack)
PAGE_LIMIT = 1000

def ts(s):
    if s is None: return None
    s = s.strip().replace("Z", "+00:00")
    m = re.match(r"^(.*T\d\d:\d\d:\d\d)(\.\d+)?(\+00:00)$", s)
    if m:  # normalise fractional seconds to <= 6 digits
        frac = (m.group(2) or "")[:7]
        s = m.group(1) + frac + m.group(3)
    return datetime.fromisoformat(s).timestamp()

def ts_keys(blob):
    """raw is zlib-compressed verbatim JSON (collector.py). Return ONLY the two timestamp keys; every other key is discarded unread."""
    d = json.loads(zlib.decompress(blob))
    return (d.get("settlement_ts"), d.get("open_time"))

def main():
    path, want = sys.argv[1], sys.argv[2]
    out = sys.argv[3] if len(sys.argv) > 3 else None
    h = hashlib.sha256(open(path, "rb").read()).hexdigest()
    if h != want: sys.exit(f"SHA MISMATCH {h} != {want}")
    c = sqlite3.connect(f"file:{path}?mode=ro&immutable=1", uri=True)
    w0, w1 = ts(W0), ts(W1)
    R = {"snapshot_sha256": h, "W0": W0, "W1": W1}
    run = c.execute("SELECT run_id, started_at, last_heartbeat, ended_at, end_reason FROM runs").fetchall()
    R["runs"] = [dict(zip(["run_id", "started_at", "last_heartbeat", "ended_at", "end_reason"], r)) for r in run]
    archive_start = min(ts(r[1]) for r in run)

    # ---- universe: markets whose FIRST finalized-with-result receipt is < W0 and close_time not in window
    rows = c.execute("""SELECT ticker, event_ticker, series_ticker, received_at, status, close_time,
                               (result IS NOT NULL AND result != '') AS has_result,
                               raw
                        FROM kalshi_markets ORDER BY ticker, received_at""").fetchall()
    rows = [r[:7] + ts_keys(r[7]) for r in rows]
    first_fin, latest, info = {}, {}, {}
    for t, ev, se, rcv, st, ct, hr, sts, ot in rows:
        if se not in SERIES: continue
        latest[t] = st
        if st == "finalized" and hr and t not in first_fin:
            first_fin[t] = rcv; info[t] = dict(event=ev, close_time=ct, settlement_ts=sts, open_time=ot)
    R["markets_ever_finalized_with_result"] = len(first_fin)
    R["events_ever_finalized_with_result"] = len({v["event"] for v in info.values()})
    scope = sorted(t for t in first_fin if ts(first_fin[t]) < w0 and not (w0 <= ts(info[t]["close_time"]) < w1)
                   and info[t]["settlement_ts"] and ts(info[t]["settlement_ts"]) < w0)
    R["in_scope_markets_n"] = len(scope)
    cd = defaultdict(list)
    for t in scope: cd[info[t]["event"]].append(t)
    R["in_scope_city_days"] = {e: dict(markets=len(v), latest_status=dict(Counter(latest[t] for t in v)),
                                       open_time_min=min(info[t]["open_time"] for t in v),
                                       close_time_max=max(info[t]["close_time"] for t in v),
                                       settlement_ts_min=min(info[t]["settlement_ts"] for t in v),
                                       settlement_ts_max=max(info[t]["settlement_ts"] for t in v),
                                       first_finalized_receipt_max=max(first_fin[t] for t in v)) for e, v in sorted(cd.items())}
    R["in_scope_city_days_n"] = len(cd)
    R["settlement_ts_in_window_n"] = sum(1 for t in scope if w0 <= ts(info[t]["settlement_ts"]) < w1)
    R["settlement_ts_null_n"] = sum(1 for t in scope if not info[t]["settlement_ts"])

    # ---- trades (id / ticker / timestamps only)
    S = set(scope)
    tr = [(tid, t, ts(ct), ts(rc)) for tid, t, ct, rc in c.execute("SELECT trade_id, ticker, created_time, received_at FROM kalshi_trades") if t in S]
    pre = [x for x in tr if x[2] < w0]
    R["trades_on_scope_markets_total"] = len(tr)
    R["trades_created_ge_W0_dropped"] = len(tr) - len(pre)
    R["trades_in_scope_pre_W0"] = len(pre)
    R["trades_received_ge_W0_n"] = sum(1 for x in pre if x[3] >= w0)
    R["trades_post_close_n_timestamp_only"] = sum(1 for x in pre if x[2] >= ts(info[x[1]]["close_time"]))
    R["trades_before_archive_start_n"] = sum(1 for x in pre if x[2] < archive_start)
    R["trades_by_city_day"] = dict(sorted(Counter(info[x[1]]["event"] for x in pre).items()))
    R["trades_by_date"] = dict(sorted(Counter(info[x[1]]["event"].split("-")[1] for x in pre).items()))
    R["created_time_min"] = datetime.fromtimestamp(min(x[2] for x in pre), timezone.utc).isoformat()
    R["created_time_max"] = datetime.fromtimestamp(max(x[2] for x in pre), timezone.utc).isoformat()

    # ---- complete-poll coverage from polls (stream kalshi_trades)
    cov = defaultdict(list)    # ticker -> [(lo, hi)]
    lp_stats = Counter()
    cur = None
    def flush(p):
        if p is None: return
        lp_stats["logical_polls"] += 1
        complete = all(r["ok"] == 1 for r in p["pages"]) and (p["pages"][-1]["n_items"] or 0) < PAGE_LIMIT
        if complete:
            lp_stats["complete"] += 1
            cov[p["key"]].append((p["min_ts"], p["req"]))
    for pid, key, url, rq, ok, n, hs in c.execute("SELECT id, key, url, requested_at, ok, n_items, http_status FROM polls WHERE stream='kalshi_trades' ORDER BY key, id"):
        is_first = "&cursor=" not in url
        if is_first or cur is None or cur["key"] != key:
            flush(cur)
            m = re.search(r"min_ts=(\d+)", url)
            cur = dict(key=key, min_ts=int(m.group(1)), req=ts(rq), pages=[])
        cur["pages"].append(dict(ok=ok, n_items=n))
    flush(cur)
    R["trades_logical_polls"] = dict(lp_stats)
    merged = {}
    for k, iv in cov.items():
        iv.sort(); m = []
        for lo, hi in iv:
            if m and lo <= m[-1][1]: m[-1][1] = max(m[-1][1], hi)
            else: m.append([lo, hi])
        merged[k] = m
    def covered(t, x):
        iv = merged.get(t, [])
        i = bisect.bisect_right([a for a, _ in iv], x) - 1
        return i >= 0 and iv[i][0] <= x < iv[i][1]
    holes = []
    for t in scope:
        iv = merged.get(t, []); lo_need, hi_need = archive_start, min(ts(info[t]["close_time"]), w0)
        if not iv: holes.append((t, "no_complete_poll")); continue
        p = lo_need
        for a, b in iv:
            if b <= p: continue
            if a > p and p < hi_need: holes.append((t, p, min(a, hi_need)))
            p = max(p, b)
            if p >= hi_need: break
        if p < hi_need: holes.append((t, p, hi_need))
    R["coverage_holes_archive_start_to_close"] = len(holes)
    R["coverage_holes_detail"] = holes[:50]
    R["trades_inside_complete_poll_coverage"] = sum(1 for x in pre if covered(x[1], x[2]))

    # ---- flagged gap windows
    gw_t, gw_all = defaultdict(list), []
    for gid, st, key, sa, ea, rs, dt, npl in c.execute("SELECT id, stream, key, started_at, ended_at, reason, detail, n_polls FROM gaps"):
        lo, hi = ts(sa), (ts(ea) if ea else float("inf"))
        if st in TRADE_STREAMS_PER_TICKER and key in S: gw_t[key].append((lo, hi, st, rs))
        elif st in ALL_TICKER_STREAMS: gw_all.append((lo, hi, st, rs))
    R["flagged_windows_on_scope_tickers"] = {s: sum(1 for v in gw_t.values() for w in v if w[2] == s) for s in TRADE_STREAMS_PER_TICKER}
    R["flagged_windows_open_ended_on_scope_tickers"] = {s: sum(1 for v in gw_t.values() for w in v if w[2] == s and w[1] == float("inf")) for s in TRADE_STREAMS_PER_TICKER}
    R["flagged_windows_all_ticker"] = dict(Counter(f"{w[2]}/{w[3]}" for w in gw_all))
    def in_flag(t, x, pad_budget=0.0, streams=None):
        for lo, hi, st, rs in gw_t.get(t, []):
            if streams and st not in streams: continue
            if (lo - (pad_budget if st == "kalshi_trades_budget" else 0.0)) <= x < hi: return True
        for lo, hi, st, rs in gw_all:
            if streams and st not in streams: continue
            if lo <= x < hi: return True
        return False
    def summarise(name, excl_fn, rule):
        ex = [x for x in pre if excl_fn(x)]
        kept = Counter(info[x[1]]["event"] for x in pre if not excl_fn(x))
        R.setdefault("gap_mappings", {})[name] = dict(rule=rule, excluded_n=len(ex), kept_n=len(pre) - len(ex),
            excluded_pct=round(100.0 * len(ex) / len(pre), 2),
            kept_by_city_day={e: kept.get(e, 0) for e in sorted(cd)},
            excluded_by_city_day=dict(sorted(Counter(info[x[1]]["event"] for x in ex).items())))
    summarise("GM-COV (PRIMARY)", lambda x: in_flag(x[1], x[2]) and not covered(x[1], x[2]),
              "exclude trade iff created_time in a flagged window for its ticker (or all-ticker window) AND outside every complete-poll coverage interval of its ticker")
    summarise("GM-LIT (sensitivity)", lambda x: in_flag(x[1], x[2]),
              "exclude trade iff created_time in any flagged window [started_at, ended_at or +inf) for its ticker or all tickers, regardless of recovery")
    summarise("GM-LIT-PAD (sensitivity)", lambda x: in_flag(x[1], x[2], BUDGET_PAD_S),
              "as GM-LIT, budget windows widened to [started_at-1920s, ended_at)")
    for s in ("kalshi_trades_budget", "kalshi_trades", "kalshi_all"):
        summarise(f"GM-LIT component only: {s}", (lambda s: lambda x: in_flag(x[1], x[2], 0.0, (s,)))(s), f"GM-LIT restricted to stream {s}")
    js = json.dumps(R, indent=1, sort_keys=False, default=str)
    if out: open(out, "w").write(js + "\n")
    print(js)

if __name__ == "__main__":
    main()
