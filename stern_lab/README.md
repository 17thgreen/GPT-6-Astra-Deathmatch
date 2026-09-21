# Stern adaptation research kit

This package contains an implemented, historically evaluated NFL state-conditioned Stern model,
a market-anchored probability-update function, a research eligibility gate, and a repository audit.
It is not an execution bot or a validated profitable strategy. No orders are sent.

Read `Stern_Kalshi_Research_Memo.md` and `CLAUDE_HANDOFF.md` first. The second-round experiment
adds clock-conditioned and nonlinear state-residual challengers, with all selection results retained.

## Reproduce the second-round experiment

```bash
python -m pip install -r requirements.txt
python download_data.py --out data --years 2016 2017 2018 2019 2020 2021 2022 2023 2024 2025
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python run_round2.py --data data --out rerun_round2 --published-model results/model.json
python -m unittest -v test_research test_round2 test_settlement
```

The runner trains nine fixed candidates on 2016–2021, selects on 2022, refits the selected
specification on 2016–2022, and serializes it before evaluating 2023–2025. It compares the winner
with original Stern, the published first prototype, and that prototype refitted on the same larger
dataset. Selection artifacts, JSON models, forecasts, calibration bins, game/week bootstrap intervals,
source hashes and inference timing are in `results/round2/`. The experiment uses about 200 MB of public
source data; these raw files are downloaded separately. Upstream revisions can change results.

See `ROUND2_PROTOCOL.md` for selection rules and `ROUND2_MODEL_SPEC.md` for the mathematics and
input provenance. Historical test seasons have been seen by the project; this is not a fresh sealed
holdout. Development comparisons and all rejected candidates remain available.

To load the selected research predictor:

```python
import json
from stern_round2 import predict
model = json.load(open("results/round2/model.json"))
p = predict(state_dataframe, model)
```

`state_dataframe` needs the named fields documented in the model specification. Probability output is
for the non-tied historical forecasting target, not an admitted live Kalshi payout estimate.

## Reproduce the forecasting experiment

```bash
python -m pip install -r requirements.txt
python download_data.py --out data
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python run_experiment.py --data data --out rerun_results
python -m unittest -v test_research
```

The downloader retrieves six public nflverse seasons, approximately 120 MB. Source hashes from the
original run are in `results/data_manifest.json`; upstream data can be revised. Exact runtime versions
are in `results/forecast_results.json`. The protocol was written before fitting/evaluation.

Training: 2019–2022, 1,100 non-tied games and 60,999 admitted snapshots. Evaluation: 2023 and 2024,
285 games in each season. No test-driven refitting was performed. Sampling is the first eligible
pre-play scrimmage state in each elapsed minute; games receive equal total weight.

## Reproduce the repo arithmetic and the verified tie correction

```bash
python audit_repository.py --repo /absolute/path/to/Claude-SportsBetting-Competition-to-the-Death --out audit_results
```

The script requires the reviewed artifact's SHA-256; it fails if that artifact changed. The reference
commit is `b31fe30d0019263ff9af706a62430d31c9b961ef` on `claude/kind-hamilton-gdfr9q`.
The captured official Kalshi market response supporting the correction is included in
`results/tied_market_source.json`. This corrects one known game from aggregated counts and costs;
it is not a recreation of the original missing trade tape.

## What is implemented

* `stern_state.py`: frozen baseline, fitted state-conditioned probit, market-anchor update and cost/data gates.
* `run_experiment.py`: temporal train/test runner with game-weighted scores and paired bootstrap intervals.
* `stern_round2.py`: clock-conditioned probit and symmetric residual learner with JSON inference.
* `settlement.py`: outcome-to-payoff conversion and bounds with explicit contract tie settlement.
* `run_round2.py`: chronological candidate selection, refitting and comparison with the larger-data control.
* `test_research.py`, `test_round2.py`: mathematical, serialization, label-exclusion and domain checks.
* `results/`: fitted parameters, prediction rows, source hashes, audit outputs and model scores.

## What is not implemented or established

* A live feed, book recorder, order execution, realized fills, or Kalshi profitability.
* An empirically calibrated anchor reliability or signal uncertainty buffer.
* A drive-transition/endgame simulator, tie-aware probability distribution, or overtime model.
* A market forecast benchmark on time-aligned executable Kalshi quotes.

The predictor rejects states outside its admitted regulation band (3 to 58.2 minutes remaining),
unknown possession and invalid state fields. The trading gate defaults to blocked until model
admission and settlement verification are supplied. Never enable those flags merely because this
historical forecasting test improved on a basic model. Fees must be passed from a versioned schedule.

Public play-by-play source: [nflverse-data](https://github.com/nflverse/nflverse-data).
Raw source files are not redistributed in this package; generated forecasts retain game/play IDs.
