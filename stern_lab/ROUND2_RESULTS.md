# Stern lab — second-round results

**21 September 2026**

**Further complexity did not establish a reliable improvement over the first prototype. Keep V1 as the research reference.** The selected specification is **clock-conditioned Stern probit** (`clock_0.0001`).
I evaluated it on **854 non-tied NFL games across 2023–2025**, using equal game weights.
These are historical forecasting results; Kalshi trading profitability remains untested.

## Comparison on identical states

Lower log loss and Brier score are better.

| Season | Original Stern LL | Published V1 LL | V1, more training data LL | Selected LL | Change vs published V1 |
|---|---:|---:|---:|---:|---:|
| 2023 | 0.485206 | 0.471034 | 0.470950 | 0.470965 | -0.01% |
| 2024 | 0.450321 | 0.440578 | 0.438927 | 0.438808 | -0.40% |
| 2025 | 0.515333 | 0.489879 | 0.490856 | 0.490354 | +0.10% |

| Season | Published V1 Brier | Selected Brier | Published V1 late LL | Selected late LL | Games / states |
|---|---:|---:|---:|---:|---:|
| 2023 | 0.156502 | 0.156474 | 0.323428 | 0.325189 | 285 / 15,803 |
| 2024 | 0.145228 | 0.144861 | 0.278892 | 0.279084 | 285 / 15,798 |
| 2025 | 0.163875 | 0.163982 | 0.363924 | 0.362315 | 284 / 15,741 |

Late means 3–15 minutes remaining within the admitted sample. The last three minutes and overtime remain excluded.

## Does the gain survive clustered uncertainty?

Entries below are selected-minus-control log loss. Negative favors the challenger. Intervals use 5,000
paired bootstrap replicates; week resampling keeps games within each season-week together. These intervals
are descriptive, do not correct for the project's repeated research, and are not prospective proof.

| Season | Control | Mean change | Game-bootstrap 95% interval | Week-cluster 95% interval |
|---|---|---:|---:|---:|
| 2023 | published_v1 | -0.000069 | [-0.002993, +0.003107] | [-0.002385, +0.002331] |
| 2023 | expanded_v1 | +0.000015 | [-0.001696, +0.001681] | [-0.001451, +0.001548] |
| 2023 | original_stern | -0.014242 | [-0.027868, -0.001574] | [-0.028413, -0.001049] |
| 2024 | published_v1 | -0.001771 | [-0.004093, +0.000693] | [-0.003790, +0.000352] |
| 2024 | expanded_v1 | -0.000120 | [-0.001416, +0.001182] | [-0.001452, +0.001230] |
| 2024 | original_stern | -0.011513 | [-0.021062, -0.002092] | [-0.021047, -0.001809] |
| 2025 | published_v1 | +0.000475 | [-0.002461, +0.003710] | [-0.002807, +0.004786] |
| 2025 | expanded_v1 | -0.000502 | [-0.002229, +0.001237] | [-0.002407, +0.001754] |
| 2025 | original_stern | -0.024979 | [-0.040361, -0.010683] | [-0.040554, -0.009382] |

The larger-data V1 control separates a model change from the benefit of additional training seasons.
An interval crossing zero leaves the direction uncertain for that comparison, even if its point estimate improves.

## Selection, fixed before evaluation

Candidate training used 2016–2021: 1,615 games and 89,575 states.
Selection used only 2022: 282 games and 15,627 states.
The chosen specification was refitted on 2016–2022 (1,897 games; 105,202 states)
and saved before loading evaluation outcomes. No test-driven ensemble or subsequent parameter change was made.

| Candidate | 2022 log loss | 2022 Brier | Selected |
|---|---:|---:|---|
| clock_0.0001 | 0.536884 | 0.177998 | Yes |
| clock_0.001 | 0.536977 | 0.178105 |  |
| refit_v1 | 0.537402 | 0.178266 |  |
| residual_depth2_50 | 0.538639 | 0.178758 |  |
| residual_depth3_50 | 0.539157 | 0.179015 |  |
| residual_depth2_100 | 0.539776 | 0.179268 |  |
| residual_depth3_100 | 0.541498 | 0.179786 |  |
| residual_depth2_200 | 0.542090 | 0.180079 |  |
| residual_depth3_200 | 0.548120 | 0.181456 |  |

Selection minimized equal-game log loss; ties within 0.00001 favored lower complexity. All nine development models
and scores are preserved. The larger-data V1 was eligible to win. The 2023/2024 seasons were examined in round one;
2025 outcomes and original repository summaries had also been seen. These are chronological evaluation seasons,
not a fresh sealed holdout at the project level.

## What changed mathematically

The clock candidate replaces constant score/strength coefficients with six smooth-in-log-time basis weights.
The residual candidate starts from Stern's fitted log odds and learns state-dependent corrections with small trees.
Its final prediction averages the original view with the complement of the mirrored team view, enforcing symmetry.
The residual features add half-clock and pregame total to possession, field position, down, distance and timeouts.
The selected model and all rejected alternatives are distinguished in the table above.

These are engineering adaptations, not claims that state-aware forecasts or residual boosting are new inventions.
The clock model is a terminal probability model; it is not automatically a coherent diffusion process.
See `ROUND2_MODEL_SPEC.md` for equations, exact features, priors, clipping and timing qualifications.

## Engineering checks and artifacts

JSON reload prediction error: 0. Team-swap complement error: 0.
Single-state inference: median 4.52 ms; observed p95 6.88 ms over 25 calls
in this environment. This measures local Python inference only; it excludes feed and exchange latency.

Fifteen unit checks pass, covering baseline reduction, clock monotonicity, symmetry, serialized trees,
outcome-label exclusion, invalid inputs, diffusion integration, market transport and research gates.

- `results/round2/model.json`: selected fitted research model.
- `results/round2/expanded_v1.json`: same-training-data control.
- `results/round2/selection.json`: all development comparisons.
- `results/round2/forecast_results.json`: full scores, calibration bins, intervals, timing and source hashes.
- `results/round2/predictions_*.csv`: forecasts and loss rows with game/play identifiers.
- `stern_round2.py`, `run_round2.py`: inference and reproducible experimental runner.

## Additional improvement: explicit settlement uncertainty

`settlement.py` adds an explicit home-win/away-win/tie payoff converter and conservative payout bounds.
Given conditional non-tie home-win probability q, tie probability t and the contract's tie payout s,
the home contract's expected payout is `(1-t)*q + t*s`. The away contract uses `(1-q)` instead.
The function requires s explicitly. Bounds are calculated over supplied q and t intervals; it does not
invent a fitted tie estimate or confidence interval. For example, q in [0.61,0.72], t in [0,0.04],
and s=0.50 imply a home payout range [0.6056,0.7200]. These example inputs are hypothetical.
The lower endpoint can enter the existing cost gate as a conservative payout input, with model admission
still required. This fixes the target conversion; it does not supply the missing tie/endgame forecaster.

## What this establishes and what it leaves open

The experiment measures historical home-win forecasting on games that did not end tied. Retrospectively excluding
ties changes the target; these probabilities are not unconditional contract expected payouts. Pregame spread/total
are untimestamped historical proxies, and archived play states do not establish live receipt times. No fee,
slippage, queue priority or execution profit is inferred from the forecasting scores.

For Kalshi, the next informative experiment is an event-aligned replay: preserve the pre-event market anchor,
compute the model's odds update after the state actually arrives, and compare it with the executable book after
measured delay. Fit anchor reliability on earlier data and compare against a market-only control. The first-round
anchor function remains a hypothesis; this round does not validate it. A separate tie/endgame/OT model is needed
before broadening the domain. The verified tie-settlement correction and repository audit remain applicable below.

Public data: [nflverse play-by-play releases](https://github.com/nflverse/nflverse-data/releases/tag/pbp).
The original model reference is [Stern (1994)](https://www.stat.berkeley.edu/~aldous/157/Papers/stern.pdf).
