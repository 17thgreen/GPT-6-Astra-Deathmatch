"""Clock-conditioned Stern and symmetric state-residual models; research only."""
from __future__ import annotations
import numpy as np
from scipy.optimize import minimize
from scipy.special import expit, logit, log_ndtr, ndtr
from stern_state import design, state_probability
from run_experiment import weights

KNOTS = np.array([.05, .10, .25, .50, .75, .97])
TREE_FEATURES = ["r", "margin", "spread_line", "possession", "yardline_100", "down", "ydstogo",
                 "home_timeouts_remaining", "away_timeouts_remaining", "half_seconds_remaining",
                 "total_line", "score_z", "strength_z", "signed_progress", "signed_progress2",
                 "signed_second", "signed_third", "signed_fourth", "signed_distance",
                 "late_possession", "late_timeout_difference"]


def mirror(d):
    m = d.copy()
    for key in ["margin", "spread_line", "possession"]:
        m[key] = -d[key]
    m["home_timeouts_remaining"] = d.away_timeouts_remaining.to_numpy()
    m["away_timeouts_remaining"] = d.home_timeouts_remaining.to_numpy()
    return m


def clock_design(d):
    x = design(d)
    lr = np.log(d.r.to_numpy())
    lk = np.log(KNOTS)
    basis = np.column_stack([np.interp(lr, lk, np.eye(len(lk))[j]) for j in range(len(lk))])
    return np.column_stack([x[:, :1]*basis, x[:, 1:2]*basis, x[:, 2:]])


def fit_clock(d, penalty):
    x, y, w = clock_design(d), d.y.to_numpy(), weights(d)
    init = np.r_[np.ones(12), np.zeros(9)]
    def objective(b):
        z = x @ b
        lp, ln = log_ndtr(z), log_ndtr(-z)
        loss = -np.sum(w*(y*lp + (1-y)*ln)) + penalty*np.mean((b-init)**2)
        logphi = -.5*z*z - .5*np.log(2*np.pi)
        gz = -y*np.exp(logphi-lp) + (1-y)*np.exp(logphi-ln)
        grad = x.T @ (w*gz) + 2*penalty*(b-init)/len(b)
        return loss, grad
    opt = minimize(objective, init, jac=True, method="L-BFGS-B",
                   bounds=[(0., None)]*12+[(None, None)]*9,
                   options={"maxiter":1000, "ftol":1e-12, "gtol":1e-7})
    if not opt.success:
        raise RuntimeError(str(opt.message))
    return {"kind":"clock", "penalty":penalty, "knots":KNOTS.tolist(),
            "coefficient_vector":opt.x.tolist(), "iterations":int(opt.nit)}


def tree_features(d):
    x = design(d)
    raw = TREE_FEATURES[:11]
    a = d[raw].to_numpy(dtype=float)
    if not np.isfinite(a).all():
        raise ValueError("Missing/nonfinite state inputs")
    if ((a[:, 9] < 0) | (a[:, 9] > 1800)).any() or ((a[:, 10] <= 0) | (a[:, 10] > 150)).any():
        raise ValueError("Invalid half-clock or pregame total")
    # Original Stern coordinates and signed football interactions.
    return np.column_stack([a, x[:, :2], x[:, 3:]])


def encode_tree(tree):
    t = tree.tree_
    return {"left":t.children_left.tolist(), "right":t.children_right.tolist(),
            "feature":t.feature.tolist(), "threshold":t.threshold.tolist(),
            "value":np.clip(t.value[:, 0, 0], -2, 2).tolist()}


def tree_predict(x, tree):
    left, right = np.asarray(tree["left"]), np.asarray(tree["right"])
    feature, threshold = np.asarray(tree["feature"]), np.asarray(tree["threshold"])
    node = np.zeros(len(x), dtype=int)
    active = left[node] != -1
    while active.any():
        rows = np.flatnonzero(active); n = node[rows]
        node[rows] = np.where(x[rows, feature[n]] <= threshold[n], left[n], right[n])
        active = left[node] != -1
    return np.asarray(tree["value"])[node]


def fit_residual(d, base, depth, n_trees=200, checkpoints=()):
    from sklearn.tree import DecisionTreeRegressor
    x = np.vstack([tree_features(d), tree_features(mirror(d))]).astype(np.float32)
    y = np.r_[d.y.to_numpy(), 1-d.y.to_numpy()]
    w = np.tile(weights(d)/2, 2)
    p0 = ndtr(design(d) @ np.asarray(base["coefficient_vector"]))
    f0 = logit(np.clip(p0, 1e-9, 1-1e-9))
    f = np.r_[f0, -f0]
    trees = []; snapshots = {}
    for stage in range(n_trees):
        p = expit(f); h = np.maximum(p*(1-p), .001)
        t = DecisionTreeRegressor(max_depth=depth, min_samples_leaf=800,
                                 random_state=20260921+stage)
        t.fit(x, (y-p)/h, sample_weight=w*h)
        encoded = encode_tree(t)
        f += .05*tree_predict(x, encoded)
        trees.append(encoded)
        if stage+1 in checkpoints:
            snapshots[stage+1] = residual_model(base, depth, trees.copy())
    return residual_model(base, depth, trees), snapshots


def residual_model(base, depth, trees):
    return {"kind":"residual", "base":base, "depth":depth, "n_trees":len(trees),
            "learning_rate":.05, "min_samples_leaf":800, "hessian_floor":.001,
            "feature_names":TREE_FEATURES, "trees":trees, "symmetrized":True}


def predict(d, model):
    kind = model["kind"]
    if kind == "v1":
        return state_probability(d, model["coefficient_vector"])
    if kind == "clock":
        if model["knots"] != KNOTS.tolist():
            raise ValueError("Unsupported clock schema")
        beta = np.asarray(model["coefficient_vector"], dtype=float)
        if beta.shape != (21,) or not np.isfinite(beta).all() or (beta[:12] < 0).any():
            raise ValueError("Invalid clock coefficients")
        return ndtr(clock_design(d) @ beta)
    if kind != "residual" or model["feature_names"] != TREE_FEATURES:
        raise ValueError("Unsupported model/schema")
    dm = mirror(d)
    x = np.vstack([tree_features(d), tree_features(dm)]).astype(np.float32)
    p0 = predict(d, model["base"])
    f0 = logit(np.clip(p0, 1e-9, 1-1e-9)); f = np.r_[f0, -f0]
    for t in model["trees"]:
        f += model["learning_rate"]*tree_predict(x, t)
    n = len(d)
    return .5*(expit(f[:n]) + 1-expit(f[n:]))
