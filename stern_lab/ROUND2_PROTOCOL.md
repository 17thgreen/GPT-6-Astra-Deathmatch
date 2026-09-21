# Round 2: fixed before candidate scores are computed

Date: 2026-09-21. Objective: improve on the first state-conditioned Stern prototype.
This is another historical research experiment; the project has viewed these seasons before.
No result will be presented as a fresh project-level sealed holdout or as Kalshi profitability.

## Data and development split

Use the same non-tied, regulation, 0.05–0.97 remaining-fraction domain and first eligible pre-play
scrimmage state per elapsed minute as Round 1. Every game contributes equal total weight.
Add public 2016–2018 play-by-play; retain 2019–2025 already downloaded.
Train candidate families on 2016–2021; select using 2022 ONLY. Refit the chosen specification on
2016–2022. Freeze and serialize before evaluating 2023, 2024 and 2025.
2023/2024 were viewed in Round 1; 2025 outcome data and original-repo aggregate results were seen,
but this challenger has never been evaluated there. No parameter changes after evaluation.

## Fixed candidates, including the simpler survivor

1. Refit V1 as-is on the larger training set (its existing 11 features and fixed penalty).
2. Clock-dependent probit: six nonnegative margin coefficients with a linear hat basis in log(r),
   knots r=[.05,.10,.25,.50,.75,.97]; the same basis for pregame strength; original possession/state
   terms. Two fixed penalties on deviation from the original Stern coefficients: 0.0001 and 0.001.
3. Stern-initialized residual boosting: start with fitted V1 log odds, learn regularized Bernoulli
   Newton corrections using decision trees. Fixed learning rate .05, depth 2 or 3, minimum 800
   augmented rows per leaf; evaluate checkpoints 50,100,200 trees. Leaf corrections clipped to
   [-2,2] before learning-rate multiplication. Input state includes the original fields, half-clock,
   pregame total (untimestamped proxy), and deterministic state interactions. No precomputed wp,
   EPA, future score, final margin or future odds predictor. Train on original and mirrored team
   views with half weight each; symmetrize probabilities at inference. This does not double N.

Select lowest equal-game 2022 log loss among these nine candidates (V1, two clock models, six tree
checkpoints). Ties within 1e-5 prefer fewer parameters/trees. Persist every candidate's score and the
selection rule. Refitting uses the selected specification, not a new search. No new test-based blend.

## Reporting and controls

Evaluate original Stern, published V1, larger-data refit V1, and selected challenger on identical rows.
Report per-season equal-game log loss and Brier, calibration bins, and the <=.25 remaining-fraction slice.
For selected-minus-refit-V1 and selected-minus-published-V1, report paired game and week-cluster
bootstrap intervals (5,000 replicates, fixed seed 20260921). Report selected-minus-original as well.
Do not claim superiority based only on a pooled score if individual seasons fail.
Keep all rejected candidates and all reported test seasons. No actual P&L without executable quotes,
receipt times, state synchronization and fee/settlement verification.

## Separate capabilities

Improve engineering with JSON-serialized models, schema validation, exact team-swap consistency,
signal provenance and empirically measured inference time. The endgame/OT domain remains outside this
experiment; improved medium-game forecasts do not authorize extrapolating into it.

Any later exchange-price diagnostic is a separately labeled development analysis, not part of the
fixed forecasting selection above. Do not retroactively change this protocol to make results pass.
