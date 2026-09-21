"""Reproducible historical prediction test; does not claim Kalshi execution/P&L."""
from __future__ import annotations
import argparse
import hashlib
import json
import platform
from pathlib import Path
import numpy as np
import pandas as pd
import scipy
from scipy.optimize import minimize, minimize_scalar
from scipy.special import log_ndtr, ndtr
from stern_state import FEATURES, design, SIGMA

COLS = ["game_id", "season", "season_type", "week", "play_id", "qtr", "game_seconds_remaining",
        "total_home_score", "total_away_score", "home_team", "away_team", "posteam", "yardline_100",
        "down", "ydstogo", "home_timeouts_remaining", "away_timeouts_remaining", "spread_line",
        "home_score", "away_score"]


def load_states(root, season):
    path = root / f"play_by_play_{season}.parquet"
    d = pd.read_parquet(path, columns=COLS)
    source_games = d.game_id.nunique()
    tied = d.loc[d.home_score == d.away_score, "game_id"].nunique()
    d = d[(d.qtr.between(1, 4)) & d.season_type.isin(["REG", "POST"]) &
          (d.home_score != d.away_score)].copy()
    d["r"] = d.game_seconds_remaining / 3600.
    d["margin"] = d.total_home_score - d.total_away_score
    d["possession"] = np.where(d.posteam == d.home_team, 1., np.where(d.posteam == d.away_team, -1., np.nan))
    d = d[d.r.between(.05, .97) & d.down.isin([1, 2, 3, 4])]
    fields = ["r", "margin", "spread_line", "possession", "yardline_100", "down", "ydstogo",
              "home_timeouts_remaining", "away_timeouts_remaining", "home_score", "away_score"]
    d = d.dropna(subset=fields)
    d["elapsed_minute"] = np.floor((3600 - d.game_seconds_remaining) / 60).astype(int)
    d = d.sort_values(["game_id", "play_id"]).drop_duplicates(["game_id", "elapsed_minute"], keep="first")
    d["y"] = (d.home_score > d.away_score).astype(float)
    d["cluster"] = d.season.astype(str) + "_" + d.week.astype(str)
    design(d)  # enforce domain/field validation
    audit = dict(season=season, source_rows=pq_rows(path), source_games=int(source_games),
                 excluded_tied_games=int(tied), admitted_games=int(d.game_id.nunique()),
                 admitted_states=len(d), sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                 source=f"https://github.com/nflverse/nflverse-data/releases/download/pbp/{path.name}")
    return d.reset_index(drop=True), audit


def pq_rows(path):
    import pyarrow.parquet as pq
    return pq.ParquetFile(path).metadata.num_rows


def weights(d):
    w = 1. / d.groupby("game_id").game_id.transform("size").to_numpy()
    return w / w.sum()


def fit(d):
    x, y, w = design(d), d.y.to_numpy(), weights(d)
    init = np.zeros(len(FEATURES)); init[:2] = 1.
    def objective(b):
        z = x @ b
        lp, ln = log_ndtr(z), log_ndtr(-z)
        penalty = .0001 * np.mean((b - init)**2)
        loss = -np.sum(w * (y * lp + (1-y) * ln)) + penalty
        logphi = -.5 * z*z - .5*np.log(2*np.pi)
        gz = -y*np.exp(logphi-lp) + (1-y)*np.exp(logphi-ln)
        grad = x.T @ (w*gz) + .0002*(b-init)/len(b)
        return loss, grad
    opt = minimize(objective, init, jac=True, method="L-BFGS-B",
                   bounds=[(0., None), (0., None)] + [(None, None)]*(len(init)-2),
                   options={"maxiter":1000,"ftol":1e-12,"gtol":1e-7})
    if not opt.success:
        raise RuntimeError(f"State fit did not converge: {opt.message}")
    z0 = x[:,0] + x[:,1]
    def scale_loss(s):
        return float(-np.sum(w*(y*log_ndtr(s*z0)+(1-y)*log_ndtr(-s*z0))))
    scalar = minimize_scalar(scale_loss, bounds=(.05,5.), method="bounded", options={"xatol":1e-8})
    if not scalar.success:
        raise RuntimeError("Scale fit did not converge")
    return {"coefficients":dict(zip(FEATURES,map(float,opt.x))),"coefficient_vector":opt.x.tolist(),
            "scale_only_slope":float(scalar.x),"scale_only_sigma":float(SIGMA/scalar.x),
            "iterations":int(opt.nit),"optimizer_success":bool(opt.success)}


def loss_arrays(y,p):
    p=np.clip(p,1e-9,1-1e-9)
    return -(y*np.log(p)+(1-y)*np.log1p(-p)),(p-y)**2


def bootstrap(values, seed=20260921):
    a=np.asarray(values);rng=np.random.default_rng(seed)
    b=np.array([rng.choice(a,len(a),replace=True).mean() for _ in range(5000)])
    return {"mean":float(a.mean()),"ci95":np.quantile(b,[.025,.975]).tolist()}


def evaluate(d,model):
    x=design(d);z=x[:,0]+x[:,1]
    predictions={"frozen_stern":ndtr(z),"scale_only":ndtr(z*model["scale_only_slope"]),
                 "state_stern":ndtr(x@np.asarray(model["coefficient_vector"]))}
    out={"games":int(d.game_id.nunique()),"states":len(d),"models":{}}
    rows=d[["game_id","season","week","cluster","play_id","r","y"]].copy()
    for name,p in predictions.items():
        ll,bs=loss_arrays(d.y.to_numpy(),p)
        rows[name+"_p"]=p;rows[name+"_logloss"]=ll;rows[name+"_brier"]=bs
        per=rows.groupby("game_id")[[name+"_logloss",name+"_brier"]].mean()
        late=rows[rows.r<=.25].groupby("game_id")[[name+"_logloss",name+"_brier"]].mean()
        out["models"][name]={"game_mean_logloss":float(per.iloc[:,0].mean()),
                             "game_mean_brier":float(per.iloc[:,1].mean()),
                             "late_game_logloss":float(late.iloc[:,0].mean()),
                             "late_game_brier":float(late.iloc[:,1].mean())}
    paired=rows.groupby(["game_id","cluster"])[[n+"_logloss" for n in predictions]].mean().reset_index()
    out["paired_contrasts"]={}
    for baseline in ["frozen_stern","scale_only"]:
        delta=paired.state_stern_logloss-paired[baseline+"_logloss"]
        contrast=bootstrap(delta)
        blocks=pd.DataFrame({"cluster":paired.cluster,"delta":delta}).groupby("cluster").delta.agg(["sum","size"])
        rng=np.random.default_rng(20260921);b=[]
        for _ in range(5000):
            draw=blocks.iloc[rng.integers(0,len(blocks),len(blocks))]
            b.append(draw["sum"].sum()/draw["size"].sum())
        contrast["week_cluster_ci95"]=np.quantile(b,[.025,.975]).tolist()
        out["paired_contrasts"]["state_minus_"+baseline]=contrast
    return out,rows


def main():
    ap=argparse.ArgumentParser();ap.add_argument("--data",type=Path,required=True)
    ap.add_argument("--out",type=Path,default=Path("results"));args=ap.parse_args()
    args.out.mkdir(parents=True,exist_ok=True)
    audit=[];train=[]
    for season in [2019,2020,2021,2022]:
        d,a=load_states(args.data,season);audit.append(a);train.append(d)
    train=pd.concat(train,ignore_index=True)
    print(f"Training: {train.game_id.nunique()} games, {len(train)} fixed-cadence states",flush=True)
    model=fit(train)
    # Persist trained model BEFORE loading evaluation outcomes.
    (args.out/"model.json").write_text(json.dumps(model,indent=2))
    print("Model frozen; beginning two chronological evaluations",flush=True)
    output={"status":"HISTORICAL_FORECAST_TEST_ONLY_NOT_KALSHI_PNL",
            "training_games":int(train.game_id.nunique()),"training_states":len(train),
            "train_years":[2019,2020,2021,2022],"test_years":[2023,2024],"tests":{},
            "environment":{"python":platform.python_version(),"numpy":np.__version__,"pandas":pd.__version__,"scipy":scipy.__version__}}
    for season in [2023,2024]:
        d,a=load_states(args.data,season);audit.append(a)
        result,rows=evaluate(d,model);output["tests"][str(season)]=result
        rows.to_csv(args.out/f"predictions_{season}.csv",index=False)
        print(json.dumps({"season":season,**result},indent=2),flush=True)
    output["source_audit"]=audit
    output["protocol_sha256"]=hashlib.sha256(Path(__file__).with_name("EXPERIMENT_PROTOCOL.md").read_bytes()).hexdigest()
    (args.out/"forecast_results.json").write_text(json.dumps(output,indent=2))
    (args.out/"data_manifest.json").write_text(json.dumps(audit,indent=2))

if __name__=="__main__":main()
