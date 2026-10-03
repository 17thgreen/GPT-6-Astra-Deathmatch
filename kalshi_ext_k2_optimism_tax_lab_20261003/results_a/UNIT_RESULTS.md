# EXT-K2 part (a) dev-tape measurement

Tags: DEV_GRADE_REUSED_31_GAME_COHORT, HYPOTHETICAL_REPLAY_FILLS, IN_SAMPLE_DEV.
Fee label: CACHE_NOT_R1P1. Gross is the headline. Account class is unpinned.
Verdict: DESCRIPTIVE.
Reasons: none.
Primary contrast is contract-weighted gross MO at 1800 seconds, T3 minus T1.
delta_star_a_gross: -0.000302
ci95_gross: [-0.001031, 0.00045]
delta_star_a_net: -0.000414 (CACHE_NOT_R1P1, not the headline)
Constancy sha256: 523f840babd3e57d8a305ecc458f979d9288e69082210edaf8648e3132101968
Bucket table sha256: 9acb52888a411be801bb701d12f3982e1e2f1c884accc162ca6f1f1d8fef6a14
results, pnl, and roi are null.
Part (b) was not run. No Becker number is in this file.

Code verification `python3 -m unittest discover -s tests -v` from this lab: 37 tests (count corrected post-merge) at 2026-10-03T22:20:00Z. Result: OK. Failures: 0. Errors: 0. That run is not an Examiner score. Constancy sha256 `523f840babd3e57d8a305ecc458f979d9288e69082210edaf8648e3132101968`. Bucket table sha256 `9acb52888a411be801bb701d12f3982e1e2f1c884accc162ca6f1f1d8fef6a14`. Primary gross contrast at 1800 seconds, T3 minus T1, is `-0.000302` with type-7 95% interval `[-0.001031, 0.00045]`. The interval contains 0, so the part (a) verdict is DESCRIPTIVE. The rounded net contrast `-0.000414` is `CACHE_NOT_R1P1` and is not the headline. The headline maker-order fee total matches the K1 lab at $1,286.22. Examiner status is `HOLD_PRE_PR`. `results`, `pnl`, and `roi` stay null.
