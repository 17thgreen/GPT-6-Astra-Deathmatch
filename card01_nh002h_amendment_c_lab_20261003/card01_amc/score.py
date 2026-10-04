"""Amendment C scorer.

Reuses the pinned script's stats and stress. The bootstrap loop matches that
script and counts boundary resamples on the same draws. Added keys sit after
the Amendment B keys so a projection reproduces SELFTEST_SYNTHETIC_output.json.
"""
from __future__ import annotations

import json
import platform
import random
import sys
from pathlib import Path

from card01_amc.pinload import PIN_SHA256, load_national_miss

BOOTSTRAP_SAMPLER = "random.Random(20261102).choices(sorted_states, k=len(sorted_states)), fresh per block"
PERCENTILE_METHOD = "order statistics xs[250], xs[9749] of 10000 ascending"
STATE_ENCODING = "USPS2 from universe code"
ROWS_ORDER = "UNIVERSE_2026_HOUSE_FROZEN order"

ADDED_TOP_KEYS = (
    "leave_one_state_out",
    "headline_status",
    "degenerate_reason",
    "split_status",
    "python_version",
    "platform",
    "bootstrap_sampler",
    "percentile_method",
    "state_encoding",
    "rows_order",
    "pinned_script_sha256",
)


def _scored(rows):
    ok = lambda r: (
        r.get("mapping_status") in ("KXHOUSERACE", "LEGACY")
        and None not in (r.get("y"), r.get("p_market"), r.get("p_model"))
    )
    return [r for r in rows if ok(r)]


def _degenerate(rows):
    if not rows:
        return "INCONCLUSIVE_DEGENERATE_BLOCK", "N_ZERO"
    if len({r["state"] for r in rows}) < 2:
        return "INCONCLUSIVE_DEGENERATE_BLOCK", "FEWER_THAN_2_STATES"
    return "DEFINED", None


def block_with_boundary_count(rows, pinned):
    """Pinned block(), plus n_boundary_resamples counted inside the same loop."""
    if not rows:
        return {"n": 0}
    st = pinned.stats(rows)
    states = sorted({r["state"] for r in rows})
    by = {s: [r for r in rows if r["state"] == s] for s in states}
    rng = random.Random(pinned.SEED)
    acc = {str(w): {"D_raw": [], "D_rc": []} for w in pinned.WS}
    n_boundary = {str(w): 0 for w in pinned.WS}
    for _ in range(pinned.B_RESAMPLES):
        rs = [r for s in rng.choices(states, k=len(states)) for r in by[s]]
        bst = pinned.stats(rs)
        for w in pinned.WS:
            acc[str(w)]["D_raw"].append(bst[str(w)]["D_raw"])
            acc[str(w)]["D_rc"].append(bst[str(w)]["D_rc"])
            if bst[str(w)]["boundary"] is True:
                n_boundary[str(w)] += 1
    ci = {}
    for w, v in acc.items():
        ci[w] = {}
        for k, xs in v.items():
            xs.sort()
            ci[w][k] = [xs[int(0.025 * pinned.B_RESAMPLES)], xs[int(0.975 * pinned.B_RESAMPLES) - 1]]
    for w in st:
        st[w]["CI95_D_raw"] = ci[w]["D_raw"]
        st[w]["CI95_D_rc"] = ci[w]["D_rc"]
    return {
        "n": len(rows),
        "states": len({r["state"] for r in rows}),
        "arms": st,
        "n_boundary_resamples": n_boundary,
    }


def leave_one_state_out(rows, pinned):
    """Point estimates only. No bootstrap and no RNG."""
    arms = [str(w) for w in pinned.WS]
    blank = {arm: {"D_raw": None, "D_rc": None} for arm in arms}
    if not rows:
        return {"by_state": {}, "per_arm_min": blank, "per_arm_max": {a: dict(v) for a, v in blank.items()}}
    states = sorted({r["state"] for r in rows})
    by_state = {}
    collected = {arm: {"D_raw": [], "D_rc": []} for arm in arms}
    for state in states:
        rest = [r for r in rows if r["state"] != state]
        if not rest:
            by_state[state] = "UNDEFINED"
            continue
        st = pinned.stats(rest)
        cell = {}
        for w in pinned.WS:
            key = str(w)
            cell[key] = {
                "D_raw": st[key]["D_raw"],
                "D_rc": st[key]["D_rc"],
                "boundary": st[key]["boundary"],
            }
            collected[key]["D_raw"].append(st[key]["D_raw"])
            collected[key]["D_rc"].append(st[key]["D_rc"])
        by_state[state] = cell
    per_min = {}
    per_max = {}
    for arm in arms:
        raws = collected[arm]["D_raw"]
        rcs = collected[arm]["D_rc"]
        per_min[arm] = {
            "D_raw": min(raws) if raws else None,
            "D_rc": min(rcs) if rcs else None,
        }
        per_max[arm] = {
            "D_raw": max(raws) if raws else None,
            "D_rc": max(rcs) if rcs else None,
        }
    return {"by_state": by_state, "per_arm_min": per_min, "per_arm_max": per_max}


def score_document(doc, pinned=None):
    pinned = pinned or load_national_miss()
    allrows = doc["rows"]
    scored = _scored(allrows)
    kx = [r for r in scored if r["mapping_status"] == "KXHOUSERACE"]
    legacy = [r for r in scored if r["mapping_status"] == "LEGACY"]
    headline, headline_reason = _degenerate(scored)
    kx_status, kx_reason = _degenerate(kx)
    legacy_status, legacy_reason = _degenerate(legacy)
    res = {
        "definition": "Amendment B (a)/(d); headline w=0.5",
        "seed": pinned.SEED,
        "resamples": pinned.B_RESAMPLES,
        "counts": {
            "input": len(allrows),
            "scored": len(scored),
            "KXHOUSERACE": sum(1 for r in scored if r["mapping_status"] == "KXHOUSERACE"),
            "LEGACY": sum(1 for r in scored if r["mapping_status"] == "LEGACY"),
            "UNRESOLVED_or_unscorable": len(allrows) - len(scored),
        },
        "all_admitted": block_with_boundary_count(scored, pinned),
        "split_KXHOUSERACE": block_with_boundary_count(kx, pinned),
        "split_LEGACY": block_with_boundary_count(legacy, pinned),
        "correlated_swing_stress": pinned.stress(scored, doc.get("signals")),
        "leave_one_state_out": leave_one_state_out(scored, pinned),
        "headline_status": headline,
        "degenerate_reason": headline_reason,
        "split_status": {
            "split_KXHOUSERACE": {"status": kx_status, "degenerate_reason": kx_reason},
            "split_LEGACY": {"status": legacy_status, "degenerate_reason": legacy_reason},
        },
        "python_version": sys.version,
        "platform": platform.platform(),
        "bootstrap_sampler": BOOTSTRAP_SAMPLER,
        "percentile_method": PERCENTILE_METHOD,
        "state_encoding": STATE_ENCODING,
        "rows_order": ROWS_ORDER,
        "pinned_script_sha256": PIN_SHA256,
    }
    return res


def project(obj):
    """Drop Amendment C keys. The remainder serializes as the pinned script."""
    out = {}
    for key, val in obj.items():
        if key in ADDED_TOP_KEYS:
            continue
        out[key] = val
    for name in ("all_admitted", "split_KXHOUSERACE", "split_LEGACY"):
        block = out[name]
        if isinstance(block, dict) and "n_boundary_resamples" in block:
            out[name] = {k: v for k, v in block.items() if k != "n_boundary_resamples"}
    return out


def main(argv):
    if len(argv) != 1:
        print("usage: python -m card01_amc.score rows.json", file=sys.stderr)
        return 2
    doc = json.loads(Path(argv[0]).read_text())
    json.dump(score_document(doc), sys.stdout, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
