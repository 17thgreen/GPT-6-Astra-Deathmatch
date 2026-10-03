#!/usr/bin/env python3
"""EXT-K2 part (a) structural verify + tercile fixture (DEV TAPE ONLY; label-free; no quotes used; no fills joined; no markout).
Reads only B1 trades (events.jsonl.gz cd300e66) and markets.json. Never reads Becker, nflverse, scores, settlement, quotes' bid/ask, or 000 ledgers.
Writes TERCILE_FIXTURE.json (cut points, event shares, counts) and TERCILE_BUCKETS.json (per ticker-hour bucket table) + STRUCTURAL_VERIFY_DEVTAPE.json."""
import gzip, json, math, hashlib, os, datetime as dt
LAB = "/workspace/lab/astra-science/nfl_factorial_lab_20260921"
TAPE = LAB + "/inputs/events.jsonl.gz"; MKTS = LAB + "/inputs/markets.json"
PIN = {"events.jsonl.gz": "cd300e664c2c5f2ff344c4b1eb17dd3f8e5f3326168b9dd8e3ade94a3a7382b4", "markets.json": "66cc07e9e9e1543b3fdcbcded30ff50af0abae87bb2aa3d5fcb3d0be7925632f"}
OUT = os.path.dirname(os.path.abspath(__file__))
MIN_TRADES = 5            # R-A04 bucket eligibility (pinned)
A1_LO = dt.datetime(2026, 9, 27, tzinfo=dt.timezone.utc).timestamp(); A1_HI = dt.datetime(2026, 9, 30, 4, tzinfo=dt.timezone.utc).timestamp()

def sha(p):
    h = hashlib.sha256(); h.update(open(p, "rb").read()); return h.hexdigest()
def q7(xs, p):  # type-7 (linear) quantile on sorted list
    h = (len(xs) - 1) * p; lo = math.floor(h); hi = min(lo + 1, len(xs) - 1); return xs[lo] + (h - lo) * (xs[hi] - xs[lo])
def tercile(s, c1, c2):
    return "T1_LOW" if s <= c1 else ("T2_MID" if s <= c2 else "T3_HIGH")
canon = lambda o: json.dumps(o, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()

assert sha(TAPE) == PIN["events.jsonl.gz"] and sha(MKTS) == PIN["markets.json"], "pin mismatch"
mk = json.load(open(MKTS)); tickers = set(mk) if isinstance(mk, dict) else None
bk = {}; ev = {}; n_tr = n_q = 0; yes_c = []; all_c = []; a1 = 0
for line in gzip.open(TAPE, "rt"):
    r = json.loads(line)
    if A1_LO <= r["at"] < A1_HI: a1 += 1
    if r.get("kind") == "quote": n_q += 1; continue
    n_tr += 1
    k = (r["ticker"], int(math.floor(r["at"] / 3600))); e = r["ticker"].rsplit("-", 1)[0]
    for key, d in ((k, bk), (e, ev)):
        x = d.setdefault(key, {"n": 0, "y": [], "a": []}); x["n"] += 1; x["a"].append(r["size"])
        if r["taker_side"] == "yes": x["y"].append(r["size"])
    all_c.append(r["size"]); 
    if r["taker_side"] == "yes": yes_c.append(r["size"])
rows = []
for (t, h), x in sorted(bk.items()):
    a = math.fsum(x["a"]); y = math.fsum(x["y"]); rows.append({"ticker": t, "hour_utc_epoch_div_3600": h, "n_trades": x["n"], "contracts": a, "yes_contracts": y, "share": (y / a) if a > 0 else None})
elig = sorted(r["share"] for r in rows if r["n_trades"] >= MIN_TRADES and r["contracts"] > 0)
c1, c2 = q7(elig, 1 / 3), q7(elig, 2 / 3)
for r in rows:
    r["tercile"] = tercile(r["share"], c1, c2) if (r["n_trades"] >= MIN_TRADES and r["contracts"] > 0) else "UNCLASSIFIED"
evs = {e: math.fsum(x["y"]) / math.fsum(x["a"]) for e, x in sorted(ev.items())}
es = sorted(evs.values()); e1, e2 = q7(es, 1 / 3), q7(es, 2 / 3)
ev_terc = {e: tercile(s, e1, e2) for e, s in evs.items()}
cnt = lambda it: {k: sum(1 for v in it if v == k) for k in ("T1_LOW", "T2_MID", "T3_HIGH", "UNCLASSIFIED")}
buckets = {"experiment_id": "EXT-K2-OPTIMISM-TAX-DEPENDENCE-STRESS", "source_tape_sha256": PIN["events.jsonl.gz"], "unit": "ticker x UTC clock hour floor(at/3600)",
           "share_formula": "fsum(size | taker_side=yes)/fsum(size), IEEE double", "rows": rows}
bb = canon(buckets); open(os.path.join(OUT, "TERCILE_BUCKETS.json"), "wb").write(bb)
fix = {"experiment_id": "EXT-K2-OPTIMISM-TAX-DEPENDENCE-STRESS", "label_free": True, "inputs": PIN,
       "primary_unit": {"unit": "ticker-hour (fill's own ticker; UTC hour = floor(at/3600))", "eligibility_min_trades": MIN_TRADES, "quantile_method": "type-7 linear on sorted eligible bucket shares (unweighted, one obs per bucket)",
                        "assignment": "T1_LOW if share<=c1; T2_MID if c1<share<=c2; T3_HIGH if share>c2; ineligible -> UNCLASSIFIED",
                        "n_buckets_total": len(rows), "n_buckets_eligible": len(elig), "c1": c1, "c2": c2, "repr_c1": repr(c1), "repr_c2": repr(c2),
                        "buckets_per_tercile": cnt([r["tercile"] for r in rows]), "frac_eligible_buckets_share_eq_1": sum(1 for s in elig if s == 1.0) / len(elig),
                        "tercile_buckets_file_sha256": hashlib.sha256(bb).hexdigest()},
       "secondary_unit_event": {"unit": "event (both tickers, whole B1 tape)", "n_events": len(evs), "c1": e1, "c2": e2, "event_share": evs, "event_tercile": ev_terc, "events_per_tercile": cnt(ev_terc.values())},
       "sensitivity_trailing_60min": {"unit": "fill's own ticker trades with at in [t_fill-3600, t_fill)", "eligibility_min_trades": MIN_TRADES, "cuts": "primary c1/c2 (not re-estimated)", "computed_at_run_time": True}}
open(os.path.join(OUT, "TERCILE_FIXTURE.json"), "wb").write(canon(fix))
sv = {"experiment_id": "EXT-K2-OPTIMISM-TAX-DEPENDENCE-STRESS", "reads": ["B1 trades only", "markets.json"], "not_read": ["quotes bid/ask", "000 ledgers", "nflverse", "Becker", "settlement", "scores"],
      "trade_rows": n_tr, "quote_rows": n_q, "tickers_with_trades": len({t for t, _ in bk}), "events": len(ev), "markets_json_tickers": len(mk),
      "taker_yes_contract_share": math.fsum(yes_c) / math.fsum(all_c), "taker_yes_contracts": math.fsum(yes_c), "all_contracts": math.fsum(all_c),
      "taker_yes_trade_rows": sum(1 for _ in yes_c), "admit1_window_rows": a1,
      "k1_repro": {"taker_yes_contract_share_k1": 0.916882, "trade_rows_k1": 681732, "quote_rows_k1": 364988}}
json.dump(sv, open(os.path.join(OUT, "STRUCTURAL_VERIFY_DEVTAPE.json"), "w"), indent=1, sort_keys=True)
print(json.dumps(sv, indent=1)); print(json.dumps({k: v for k, v in fix["primary_unit"].items()}, indent=1)); print(fix["secondary_unit_event"]["c1"], fix["secondary_unit_event"]["c2"], fix["secondary_unit_event"]["events_per_tercile"])
