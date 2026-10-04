#!/usr/bin/env python3
"""NH-002-H Amendment B: national-miss recentering, correlated-swing stress, mapping-status split.

Implements exactly the definitions in packets/CARD01_HOUSE_ONLY_PROSPECTIVE_FREEZE_2026-09-24_AMENDMENT_B.md section (a)/(d).
Pure standard library, deterministic. Read-only: reads an input JSON, writes JSON to stdout. No network.

INPUT (JSON): {"rows":[{"race_id","state","mapping_status":"KXHOUSERACE"|"LEGACY"|"UNRESOLVED",
                        "p_market","p_model","y"}...],
               "signals":[{"race_id","side":"D_YES"|"D_NO","price","fee"(number or null)}...]   # optional}
  p_market = Kalshi -D YES bid/ask mid at the decision snapshot; p_model = ElectIndex dem_prob/100;
  y = 1 if Kalshi settled the -D contract YES, else 0. Rows with mapping_status UNRESOLVED (or y/prices null)
  are counted, never scored.

DEFINITIONS
  arms: p_w = w*p_model + (1-w)*p_market, w in {0 (market-only control), 0.25, 0.5 (HEADLINE), 1.0}
  clip: p -> min(max(p, 1e-4), 1-1e-4) before any logit
  national miss (descriptive):  M_f = mean_i (p_f,i - y_i)
  national shift (Bernoulli MLE): delta_f = argmax_d sum_i [ y_i*log s(l_i+d) + (1-y_i)*log(1-s(l_i+d)) ],
        l_i = logit(clip(p_f,i)), s = logistic. Solved by bisection on the score
        g(d) = sum_i (y_i - s(l_i+d)) (strictly decreasing) over [-10, 10], 60 iterations (interval width 20/2^60 < 1e-16).
        If all y equal (no interior root) delta is set to the bound and flagged boundary=true.
        Property: mean_i(s(l_i+delta_f) - y_i) = 0, i.e. the recentered national miss is zero.
  recentered prob: pr_f,i = s(l_i + delta_f)
  Brier: B(p) = (p - y)^2 (unclipped p for raw; pr for recentered)
  D_raw(w) = mean_i [B(p_w,i) - B(p_0,i)];  D_rc(w) = mean_i [B(pr_w,i) - B(pr_0,i)]
  CI: state-cluster bootstrap, 10000 resamples of states with replacement, random.Random(20261102);
      delta re-estimated inside every resample for every arm; 95% percentile interval
      lo = sorted[int(0.025*B)], hi = sorted[int(0.975*B) - 1].
  Split: the same statistics computed separately within mapping_status KXHOUSERACE and LEGACY
      (delta re-estimated within group); UNRESOLVED only counted.
  Correlated-swing stress (secondary, non-gating): swing grid S = [-0.50, -0.25, 0.0, +0.25, +0.50] (logit units,
      positive = toward Democrats). For each signal, q_i(s) = s(logit(clip(p_0.5,i)) + s);
      expected gross per contract: D_YES -> q - price; D_NO -> (1 - q) - price. Summed over signals.
      Net = gross - sum(fee) only if every fee is a number; otherwise net = "BLOCKED_FEE_UNVERIFIED".
      Sign flips: number and share of signals whose expected gross EV sign (>0 vs <=0) at swing s differs from s=0.
"""
import json, math, random, sys

EPS = 1e-4
WS = [0.0, 0.25, 0.5, 1.0]
HEADLINE_W = 0.5
SWING_GRID = [-0.50, -0.25, 0.0, 0.25, 0.50]
B_RESAMPLES = 10000
SEED = 20261102

def clip(p): return min(max(p, EPS), 1 - EPS)
def logit(p): p = clip(p); return math.log(p / (1 - p))
def sig(x): return 1 / (1 + math.exp(-x)) if x >= 0 else math.exp(x) / (1 + math.exp(x))

def delta_mle(ps, ys):
    ls = [logit(p) for p in ps]
    g = lambda d: sum(y - sig(l + d) for l, y in zip(ls, ys))
    lo, hi = -10.0, 10.0
    if g(lo) <= 0: return lo, True
    if g(hi) >= 0: return hi, True
    for _ in range(60):
        mid = (lo + hi) / 2
        if g(mid) > 0: lo = mid
        else: hi = mid
    return (lo + hi) / 2, False

def arm_p(r, w): return w * r["p_model"] + (1 - w) * r["p_market"]

def stats(rows):
    ys = [r["y"] for r in rows]
    out = {}
    raw = {w: [arm_p(r, w) for r in rows] for w in WS}
    rc, meta = {}, {}
    for w in WS:
        d, b = delta_mle(raw[w], ys)
        rc[w] = [sig(logit(p) + d) for p in raw[w]]
        meta[w] = {"delta": d, "boundary": b, "M_raw": sum(p - y for p, y in zip(raw[w], ys)) / len(ys),
                   "M_recentered": sum(p - y for p, y in zip(rc[w], ys)) / len(ys)}
    for w in WS:
        braw = sum((a - y) ** 2 - (m - y) ** 2 for a, m, y in zip(raw[w], raw[0.0], ys)) / len(ys)
        brc = sum((a - y) ** 2 - (m - y) ** 2 for a, m, y in zip(rc[w], rc[0.0], ys)) / len(ys)
        out[str(w)] = {"D_raw": braw, "D_rc": brc, **meta[w]}
    return out

def boot(rows):
    states = sorted({r["state"] for r in rows})
    by = {s: [r for r in rows if r["state"] == s] for s in states}
    rng = random.Random(SEED)
    acc = {str(w): {"D_raw": [], "D_rc": []} for w in WS}
    for _ in range(B_RESAMPLES):
        rs = [r for s in rng.choices(states, k=len(states)) for r in by[s]]
        st = stats(rs)
        for w in WS:
            acc[str(w)]["D_raw"].append(st[str(w)]["D_raw"]); acc[str(w)]["D_rc"].append(st[str(w)]["D_rc"])
    ci = {}
    for w, v in acc.items():
        ci[w] = {}
        for k, xs in v.items():
            xs.sort(); ci[w][k] = [xs[int(0.025 * B_RESAMPLES)], xs[int(0.975 * B_RESAMPLES) - 1]]
    return ci

def block(rows):
    if not rows: return {"n": 0}
    st, ci = stats(rows), boot(rows)
    for w in st: st[w]["CI95_D_raw"] = ci[w]["D_raw"]; st[w]["CI95_D_rc"] = ci[w]["D_rc"]
    return {"n": len(rows), "states": len({r["state"] for r in rows}), "arms": st}

def stress(rows, signals):
    if not signals: return {"status": "NO_SIGNALS_SUPPLIED", "rows": None}
    byid = {r["race_id"]: r for r in rows}
    fees = [s.get("fee") for s in signals]
    fee_ok = all(isinstance(f, (int, float)) for f in fees)
    def ev(s, sw):
        q = sig(logit(arm_p(byid[s["race_id"]], HEADLINE_W)) + sw)
        return (q - s["price"]) if s["side"] == "D_YES" else ((1 - q) - s["price"])
    base = [ev(s, 0.0) for s in signals]
    out = []
    for sw in SWING_GRID:
        evs = [ev(s, sw) for s in signals]
        flips = sum(1 for a, b in zip(base, evs) if (a > 0) != (b > 0))
        out.append({"swing_logit": sw, "expected_gross": sum(evs),
                    "expected_net": (sum(evs) - sum(fees)) if fee_ok else "BLOCKED_FEE_UNVERIFIED",
                    "n_sign_flips_vs_s0": flips, "share_sign_flips_vs_s0": flips / len(signals)})
    return {"status": "OK", "n_signals": len(signals), "rows": out}

def main(path):
    d = json.load(open(path))
    allrows = d["rows"]
    ok = lambda r: r.get("mapping_status") in ("KXHOUSERACE", "LEGACY") and None not in (r.get("y"), r.get("p_market"), r.get("p_model"))
    scored = [r for r in allrows if ok(r)]
    res = {"definition": "Amendment B (a)/(d); headline w=0.5", "seed": SEED, "resamples": B_RESAMPLES,
           "counts": {"input": len(allrows), "scored": len(scored),
                      "KXHOUSERACE": sum(1 for r in scored if r["mapping_status"] == "KXHOUSERACE"),
                      "LEGACY": sum(1 for r in scored if r["mapping_status"] == "LEGACY"),
                      "UNRESOLVED_or_unscorable": len(allrows) - len(scored)},
           "all_admitted": block(scored),
           "split_KXHOUSERACE": block([r for r in scored if r["mapping_status"] == "KXHOUSERACE"]),
           "split_LEGACY": block([r for r in scored if r["mapping_status"] == "LEGACY"]),
           "correlated_swing_stress": stress(scored, d.get("signals"))}
    json.dump(res, sys.stdout, indent=1)

if __name__ == "__main__":
    main(sys.argv[1])
