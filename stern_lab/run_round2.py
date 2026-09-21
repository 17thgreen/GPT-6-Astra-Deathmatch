"""Fixed 2022 selection; freeze refit before 2023–2025 evaluation."""
from __future__ import annotations
import argparse
import hashlib
import json
import platform
import time
from pathlib import Path
import numpy as np
import pandas as pd
import scipy
import sklearn
from stern_state import stern_probability
from run_experiment import load_states, fit, weights, loss_arrays, bootstrap
from stern_round2 import fit_clock, fit_residual, predict, mirror, tree_features


def load(root, season):
    d, audit = load_states(root, season)
    extra = pd.read_parquet(root/f"play_by_play_{season}.parquet",
                           columns=["game_id", "play_id", "half_seconds_remaining", "total_line"])
    d = d.merge(extra, on=["game_id", "play_id"], how="left", validate="one_to_one")
    before = len(d)
    d = d.dropna(subset=["half_seconds_remaining", "total_line"]).reset_index(drop=True)
    tree_features(d)
    audit["round2_missing_extra_states"] = before-len(d)
    audit["round2_states"] = len(d)
    audit["round2_games"] = int(d.game_id.nunique())
    return d, audit


def metrics(d, p):
    ll, bs = loss_arrays(d.y.to_numpy(), p)
    rows = pd.DataFrame({"game":d.game_id, "r":d.r, "ll":ll, "bs":bs})
    per = rows.groupby("game")[["ll", "bs"]].mean().mean()
    late = rows[rows.r <= .25].groupby("game")[["ll", "bs"]].mean().mean()
    w = weights(d)
    bins = []
    for i in range(10):
        mask = np.minimum((p*10).astype(int), 9) == i
        if mask.any():
            bins.append({"bin":i, "states":int(mask.sum()), "weight":float(w[mask].sum()),
                         "predicted":float(np.average(p[mask], weights=w[mask])),
                         "observed":float(np.average(d.y.to_numpy()[mask], weights=w[mask]))})
    return {"logloss":float(per.ll), "brier":float(per.bs),
            "late_logloss":float(late.ll), "late_brier":float(late.bs), "calibration":bins}


def contrast(rows, baseline):
    per = rows.groupby(["game_id", "cluster"])[["challenger_logloss", baseline+"_logloss"]].mean().reset_index()
    delta = per.challenger_logloss-per[baseline+"_logloss"]
    out = bootstrap(delta)
    blocks = pd.DataFrame({"cluster":per.cluster, "delta":delta}).groupby("cluster").delta.agg(["sum", "size"])
    a = blocks.to_numpy(); rng = np.random.default_rng(20260921)
    ix = rng.integers(0, len(a), (5000, len(a)))
    draws = a[ix].sum(axis=1)
    out["week_cluster_ci95"] = np.quantile(draws[:, 0]/draws[:, 1], [.025, .975]).tolist()
    return out


def dump(path, obj):
    path.write_text(json.dumps(obj, indent=2, allow_nan=False))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", type=Path, required=True)
    ap.add_argument("--out", type=Path, default=Path("results/round2"))
    ap.add_argument("--published-model", type=Path, default=Path("results/model.json"))
    args = ap.parse_args(); args.out.mkdir(parents=True, exist_ok=True)
    started = time.perf_counter(); audit = []; frames = []
    for season in range(2016, 2022):
        d, a = load(args.data, season); frames.append(d); audit.append(a)
    train = pd.concat(frames, ignore_index=True)
    val, a = load(args.data, 2022); audit.append(a)
    print(f"Development: {train.game_id.nunique()} train games; {val.game_id.nunique()} selection games", flush=True)
    base = {"kind":"v1", **fit(train)}
    candidates = [("refit_v1", base, 11)]
    for penalty in [.0001, .001]:
        model = fit_clock(train, penalty)
        candidates.append((f"clock_{penalty}", model, 21))
    for depth in [2, 3]:
        _, snapshots = fit_residual(train, base, depth, checkpoints=[50,100,200])
        for n, m in snapshots.items():
            candidates.append((f"residual_depth{depth}_{n}", m, n*(2**depth)))
        print(f"Finished residual depth {depth}", flush=True)
    scores = []
    for name, model, complexity in candidates:
        score = metrics(val, predict(val, model))
        scores.append({"name":name, "complexity":complexity, **score})
        dump(args.out/f"development_{name}.json", model)
        print(f"2022 {name}: log loss {score['logloss']:.7f}", flush=True)
    best = min(s["logloss"] for s in scores)
    selected = min((s for s in scores if s["logloss"] <= best+1e-5), key=lambda s:s["complexity"])
    spec = next(m for name,m,_ in candidates if name == selected["name"])
    selection = {"selection_year":2022, "train_years":list(range(2016,2022)),
                 "train_games":int(train.game_id.nunique()), "train_states":len(train),
                 "selection_games":int(val.game_id.nunique()), "selection_states":len(val),
                 "candidates":scores, "selected":selected["name"]}
    dump(args.out/"selection.json", selection)
    print("Selected "+selected["name"]+"; refitting frozen specification", flush=True)
    expanded = pd.concat([train, val], ignore_index=True)
    expanded_base = {"kind":"v1", **fit(expanded)}
    if spec["kind"] == "v1":
        challenger = expanded_base
    elif spec["kind"] == "clock":
        challenger = fit_clock(expanded, spec["penalty"])
    else:
        challenger, _ = fit_residual(expanded, expanded_base, spec["depth"], n_trees=spec["n_trees"])
    challenger["research_metadata"] = {"train_years":list(range(2016,2023)), "selection_year":2022,
        "training_games":int(expanded.game_id.nunique()), "training_states":len(expanded),
        "domain":"Non-tied NFL regulation games, remaining fraction .05–.97, first eligible pre-play state/minute",
        "market_admitted":False, "pregame_lines":"Untimestamped historical proxies"}
    dump(args.out/"model.json", challenger)
    dump(args.out/"expanded_v1.json", expanded_base)
    # Save all fit artifacts before loading any evaluation outcomes.
    print("Final model serialized; beginning 2023–2025 evaluation", flush=True)
    published = {"kind":"v1", **json.loads(args.published_model.read_text())}
    output = {"status":"HISTORICAL_FORECAST_RESEARCH_ONLY", "selection":selection["selected"], "tests":{},
              "training_games":int(expanded.game_id.nunique()), "training_states":len(expanded),
              "protocol_sha256":hashlib.sha256(Path(__file__).with_name("ROUND2_PROTOCOL.md").read_bytes()).hexdigest(),
              "model_sha256":hashlib.sha256((args.out/"model.json").read_bytes()).hexdigest(),
              "environment":{"python":platform.python_version(), "numpy":np.__version__,
                "pandas":pd.__version__, "scipy":scipy.__version__, "sklearn":sklearn.__version__}}
    for season in [2023,2024,2025]:
        d, a = load(args.data, season); audit.append(a)
        predictions = {"original_stern":stern_probability(d), "published_v1":predict(d,published),
                       "expanded_v1":predict(d,expanded_base), "challenger":predict(d,challenger)}
        rows = d[["game_id","cluster","season","week","play_id","r","y"]].copy()
        result = {"games":int(d.game_id.nunique()), "states":len(d), "models":{}}
        for name,p in predictions.items():
            result["models"][name] = metrics(d,p)
            rows[name+"_p"] = p
            rows[name+"_logloss"], rows[name+"_brier"] = loss_arrays(d.y.to_numpy(),p)
        result["paired_contrasts"] = {"challenger_minus_"+b:contrast(rows,b)
                                      for b in ["original_stern","published_v1","expanded_v1"]}
        rows.to_csv(args.out/f"predictions_{season}.csv",index=False)
        output["tests"][str(season)] = result
        print(json.dumps({"season":season, "games":result["games"],
              "scores":{n:{k:v for k,v in m.items() if k!='calibration'} for n,m in result["models"].items()},
              "paired_contrasts":result["paired_contrasts"]},indent=2),flush=True)
    sample = d.iloc[:100].copy()
    restored = json.loads((args.out/"model.json").read_text())
    roundtrip_error = float(np.max(np.abs(predict(sample,challenger)-predict(sample,restored))))
    swap_error = float(np.max(np.abs(predict(sample,restored)+predict(mirror(sample),restored)-1)))
    durations = []
    for _ in range(25):
        t0 = time.perf_counter(); predict(sample.iloc[:1],restored); durations.append((time.perf_counter()-t0)*1000)
    output["engineering"] = {"json_roundtrip_max_error":roundtrip_error,
                            "team_swap_max_error":swap_error,
                            "single_state_median_ms":float(np.median(durations)),
                            "single_state_p95_ms":float(np.quantile(durations,.95)),
                            "timing_repeats":25, "timing_scope":"Python DataFrame to probability; no network"}
    if roundtrip_error > 1e-12 or swap_error > 1e-12:
        raise AssertionError("Serialization/symmetry invariant failed")
    output["runtime_seconds"] = time.perf_counter()-started
    output["source_audit"] = audit
    dump(args.out/"forecast_results.json",output)
    print(json.dumps(output["engineering"],indent=2),flush=True)


if __name__ == "__main__":
    main()
