# Claude handoff — review and integrate the Stern research challenger

Work from reviewed commit `b31fe30d0019263ff9af706a62430d31c9b961ef` of
`17thgreen/Claude-SportsBetting-Competition-to-the-Death`. If HEAD differs, identify the changed relevant
files before applying this handoff. Keep the existing paper-only mandate. Preserve all failed experiments.

The user requested an innovative Brownian/Stern adaptation for Kalshi sports markets. This package supplies
tested code and a more specific hypothesis than a volatility sweep. Read the memo, protocol, fitted
parameters and raw results before proceeding. Do not call its forecasting result a profitable strategy.

## Round 2 decision: retain V1 as the reference

Nine fixed candidates were trained on 2016–2021 and selected on 2022. The clock-conditioned probit
won selection; all six nonlinear residual variants lost. After refitting on 2016–2022, the selected
model did not establish a reliable improvement over published V1 on 2023–2025. Its 2025 score was
slightly worse, and every week-cluster interval for the incremental improvement crossed zero.
Do not promote `results/round2/model.json` merely because it won development selection. Keep it as
an experimental challenger. `results/model.json` remains the original research reference.

Read `ROUND2_RESULTS.md`, `ROUND2_PROTOCOL.md` and `ROUND2_MODEL_SPEC.md`. All candidate parameters,
selection scores, evaluation forecasts and larger-training-set controls are retained. The test years
are chronologically later, but are not a fresh project-level holdout.

`settlement.py` is a separate useful integration: explicit home/away/tie payout conversion and
conservative payout ranges from supplied conditional-win and tie-probability intervals. It requires
the exact contract tie payoff and never turns a tied game into an away win. It does not estimate tie
probability. Do not pass the original non-tie forecast directly to an unconditional payoff gate.

## Findings to address first

1. **Verified scalar-settlement error:** `2025_04_GB_DAL` is a tie in the committed 196-game ledger.
   The archived Dallas market pays $0.50; the rule text says 50/50 for both teams. The current
   `(finals[gid] > 0) == pays_home` expression labels a tie as an away win. Use the captured exchange
   response in `results/tied_market_source.json`, then independently verify both market records. The
   supplied one-game arithmetic changes P&L from −3096.27 to −229.77 and the equal-game bootstrap interval
   from [−15.849%, −0.168%] to [−15.668%, +0.060%]. This is a partial correction, not a full replay.
   Repair this settlement logic anywhere reused, including the FLB and matchup scripts; rerun from your
   raw tape with a new artifact ID. Preserve the original artifacts.
2. **Do not revive the withdrawn final-score suspicion:** exact ISO8601 parsing matched final margins in
   315 2025/2026 games. Pandas mixed timestamp parsing caused the first audit's false alarm. The tie
   payoff defect is distinct.
3. **Fix evaluation coherence:** freeze shared game IDs and hashes; basic and modern diagnostics use
   different coverage. Score forecasts on fixed snapshots with game weights. Do not treat repeated
   prints as independent evidence. Preserve the original estimands and also evaluate an executable
   capital-allocation policy. The 2026 sample is already used for multiple hypotheses.
4. **Do not diagnose alpha by fitting sigma to the same quote being judged.** It is a circular fit and
   mean/variance identification is underdetermined from one moneyline. Better log loss plus worse selected
   ROI does not prove all prior model–market gaps were calibration errors.

## Implemented challenger

`stern_state.py` supplies a regularized state-conditioned probit that retains Stern's score/time terms
and adds possession, field position, down, distance and timeout information. The model was trained on
2019–2022 with fixed choices before evaluation. On 285 games each in 2023/2024 it improves log loss from
0.48521→0.47103 and 0.45032→0.44058, and Brier from 0.15949→0.15650 and 0.15035→0.14523.
Week-cluster intervals against frozen Stern cross zero. Keep that limitation attached to the result.

Suggested integration locations (new files, preserving baseline behavior):
- `src/flatstake/models/inplay_stern_state.py`: state construction and fitted forecast.
- `src/flatstake/eval/inplay_state_eval.py`: shared-cohort predictor evaluation.
- `src/flatstake/paper/inplay_anchor.py`: market-reference transport and blocked-by-default research gate.
- new immutable run directory + registry entry + strategy-board update under a new challenger name.

The prototype trains on non-tied outcomes, excludes overtime and the final three minutes, and uses closing
spread as an untimestamped pregame proxy. It is not an admitted live payout model. Build the proper tie and
overtime outcome distribution before removing those restrictions. Use explicit state availability times.
Never substitute final scores, post-play EPA, wp columns or future market quotes into predictor features.

## New Kalshi hypothesis

Before a new play, capture market reference q0 and model probability p0. After the play is received, compute
p1. Transport the old market odds by the model update:

`p_candidate = expit(logit(q0) + lambda * (logit(p1) - logit(p0)))`.

This is a relative-update hypothesis, not a proof that the model increment is a likelihood ratio. Learn
lambda on earlier data, include lambda=0 as a control, freeze it, then evaluate forward. Do not use the
current target quote as q0 or reset the anchor after observing the very event being traded.

Required logs: source event time, receive time, play/state revision, pre-event reference quote time,
book sequence/receipt time, decision time, expected arrival time, current executable ask/depth, fee
version, model version, proposed size, game-level exposure, rejection reason and settlement.

Compare against direct model-level trading and market-only forecasts; evaluate at measured latency.
Print-only data cannot prove fill reachability. Fixed fees and buffers in toy examples are not fitted
parameters. Do not allow missing asks to become last-price fills. Do not count each print as a new
independent position or duplicate correlated contracts without a shared exposure cap.

## Acceptance and stop conditions

- Reproduce the package's forecast and audit arithmetic within numerical tolerance; verify source hashes.
- Preserve baseline outputs and attach every correction, data revision and failed candidate.
- Produce game- and week-clustered results, forecast calibration curves, signal coverage and policy costs.
- Advance only if an untouched forward sample supports positive after-cost results under reachable fills,
  and any claimed forecasting improvement survives an appropriate market benchmark.
- Reject the trading hypothesis if measured latency/costs remove the advantage. A good forecasting model
  is still useful even if this venue prices its information first.

No live deployment, capital allocation or actual wager placement is requested by this handoff.
