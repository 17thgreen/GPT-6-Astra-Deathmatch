# Stern state adaptation: protocol fixed before model results

Date: 2026-09-21. Reference repository commit: b31fe30d0019263ff9af706a62430d31c9b961ef.

This is an independent historical forecasting experiment, not a Kalshi profit backtest.
The repository's 2025/2026 exchange samples have already been inspected and are development data.

Train on NFL 2019–2022. Evaluate once on 2023 and 2024 separately, without selecting parameters on either.
Use regular-season and postseason games, regulation pre-play states, remaining fraction [0.05, 0.97].
Use the first eligible scrimmage state in each elapsed regulation minute, ordered by play_id. Exclude
missing state fields, unknown possession, and games ending tied. The resulting target is home victory
on non-tied games. This is not a tie-aware contract payout model. Overtime states are out of scope.
Fields total_home_score and total_away_score are PRE-play; home_score and away_score are FINAL labels.
Closing spread is an untimestamped pregame strength proxy, not a verified point-in-time feed.

Compare three models on identical states:
1. Frozen Stern: Phi((margin + spread * r) / (13.7 * sqrt(r))).
2. Scale-only Stern: fit one positive probit slope by training loss, preserving numerator.
3. State-conditioned Stern: regularized probit with score, spread, possession, field position,
   down, yards to go, and timeout differences. Score and spread coefficients constrained nonnegative.
   State effects enter as expected-margin adjustments divided by 13.7 * sqrt(r).
   No trees, parameter sweep, test-driven feature selection, or test-period calibration.

Fixed state terms: possession; possession * field progress; possession * field progress squared;
possession * down indicators (2, 3, 4); possession * log1p(yards-to-go)/log(21);
possession * (1-r); home-minus-away timeout count * (1-r)/3.
Field progress is (100 - yardline_100)/100. Score margin and pregame spread get separate coefficients.
Parameters start at the Stern baseline and use a 0.0001 mean-square penalty on their displacement.
No intercept: sign reversal of both teams' state must complement the non-tie forecast.

Training weights: each game contributes total weight one. Reporting: average per-game log loss and
Brier score. Primary contrast: state model minus frozen Stern log loss in each test season.
Use paired game bootstrap (5,000 replicates, seed 20260921); also report a week-cluster bootstrap.
Report scale-only contrast to separate extra state information from mere variance recalibration.
Fixed late-game slice: remaining fraction <= 0.25. Report all three results, including failures.

Do not report exchange ROI: the repo does not track its raw tape, order-book history is absent, and
this experiment has neither receipt timestamps nor historical executable quotes.
The market-anchored update layer is a separate unvalidated hypothesis to implement and unit-check.
