## [RPT-Q7] — Chosen-pair cost check (arms A–D)
Status: **SCORED** (Examiner packet · HISTORICAL_DEV · fee-honest · **not** a live desk return · **no** promotion)
Desk headline: **KEEP** shadow `000` · **KILL** Arm B as candidate · live_promotion **DENIED**
Account: $5,000 | Horizon: 31 development games (W1+W2 pooled) | Fees: modeled (maker 0.0175 · taker 0.07)
Primary: `q3300_d0.25` | Evidence: `Q7_CHOSEN_PAIR_CHECK_REUSED_31_GAME_DEVELOPMENT_HYPOTHETICAL_EXECUTION`

| Arm | Role | Net PnL | %gain |
|---|---|---:|---:|
| A | original router · check off | +$201.52 | 4.03% |
| B | original router · check on | +$290.99 | 5.82% |
| C | Q6 `000` · check off (ablation) | +$205.94 | 4.12% |
| D | Q6 `000` · check on (reference) | +$345.24 | 6.90% |

Contrasts (primary): original_guard B−A +$89.47 · allocator_guard D−C +$139.30 · interaction +$49.83 · architecture_check_off C−A +$4.42 · architecture_check_on D−B +$54.25

**B vs D retention bar (need B ≥ 95% of D every stress):** primary B/D = **0.843** · miss · also NO on q3300_d5 (0.843), q10000_d0.25 (0.600), q10000_d5 (0.548)

Selection: `NO_NEW_SELECTION` · `retains_95pct_of_D=false` (hard fail) · fallback shadow **`000`** · `live_promotion=false`
95%-of-D bar addendum: Examiner **STAND** for this packet (refuse post-outcome soften/drop; new tolerance only via new freeze) — cite scorecard addendum
Verdict stamps: Arm B candidacy **KILL** · Q6 shadow `000` (Arm D) **KEEP** · live promotion/orders **DENIED** · Q7 measurement **CLOSED**
Extrapolation: projection on fixed reused development window only — **not** annualized · **not** holdout · **not** live causal
Caveats: HISTORICAL_DEV · fee-honest completed_strategy_pnl · NO LIVE ORDERS · no promotion language · no ITERATE on this 2×2 without a new freeze
Source packet: `lab/governance/astra/packets/Q7_EXAMINER_SCORECARD_2026-09-22.md`
Artifacts: `lab/astra-science/nfl_paircheck_lab_20260922/results/{paircheck_effects,verification,experiment_summary}.json` · `FROZEN_EXPERIMENT.json`
Published: 2026-09-22 18:45 ET
