# Examiner scorecard — R3-P2 abs_err / signed_bias — SCORED

**Seat:** Examiner (Kalshi)  
**Packet:** R3-P2-QUEUE-POSITION-CALIB (feature family **R3-P2**)  
**Scope:** `abs_err_contracts` + `signed_bias` measurement honesty **only**  
**Route:** `packets/CONDUCTOR_ROUTE_R3_P2_ABS_ERR_SIGNED_BIAS_EXAMINER_2026-09-23.json`  
**Mechanic:** ABS_ERR_SIGNED_BIAS_COMPUTED · `calibration_run=true`  
**PR37 stub:** SUPERSEDED for this channel (sample-ingest stub → calibration metrics non-null)

**Series:** sha256 `74ef9a9bb54054691e26b7b752568c8e833f51d21292034b1f40b9f3ca4ba8b4`  
**Labels:** sha256 `f89c06dc1639b194c9d026e157fbfbc2a8b527853afe698dd1f77389eb34c964`  
**Frozen knobs:** sha256 `9a3534219b9be6cbfccb259b23e1245cec682dcee754b5f6a004c55d5354d2a6` (not retuned after peek)  
**abs_err artifact:** sha256 `f7e83a28abbf2f216fafe316a153aff27a94a27f231f5aa65bfd8310e6224141`  
**Desk digest verification:** **PASS** (series / labels / knobs / abs_err). Independent recompute of `|estimate_ahead − queue_position_fp|` and signed bias on all 51 OK rows: **0 mismatches**; all identity.

---

## REQUIRED CAVEAT

**STATIC_SERIES_IDENTITY_MATCH — cancel fractions recorded not applied; estimate_ahead = visible_qty_pre_own (= qp) on cancel-safe rest→poll→cancel samples. Zero abs_err is expected join-back integrity, NOT a trade-step cancel-model stress and NOT a promote. Brier waits fill-label GO.**

Evidence on labels: all 51 OK rows have `trade_size_observed=null` and `estimate_ahead == visible_qty_pre_own == queue_position_fp`. Series `fill_count=0` on all 38 samples. tfrmma notes: cancel fraction recorded not applied. acheron notes: cold-start `visible_pre_own * initial_ahead_fraction` with frozen fraction `1.0` (depletion unused).

---

## Verdict

| Subject | Stamp |
|---|---|
| `abs_err_contracts` / `signed_bias` measurement honesty | **KEEP** |
| Cancel-model / trade-step dynamics | **NOT_SCORED** (ITERATE pending trade-step series) |
| Fill prediction (Brier) | **NOT_SCORED** (null; waits fill-label GO) |
| PnL / promote / live | **DENIED** |
| Knob retune after peek / Q6-`000` | **DENIED** |

**Desk headline:** KEEP on abs_err/signed_bias plumbing honesty under STATIC_SERIES_IDENTITY_MATCH. Zero error is expected identity join-back — **not** a cancel-model promote.

**Evidence tags:** [V][H][A]

---

## Measured (artifact-backed)

| Metric | Value |
|---|---|
| `n_metric_ok` | **51** (17×3 models) |
| `n_skipped` | **63** (`SKIP_INSUFFICIENT_L2_OR_UNSUCCESSFUL`) |
| `mean_abs_err_contracts` | **0.0** |
| `median_abs_err_contracts` | **0.0** |
| `max_abs_err_contracts` | **0.0** |
| `mean_signed_bias` | **0.0** |
| `median_signed_bias` | **0.0** |
| `zero_err_n` | **51** |
| `brier` | **null** |
| `pnl` | **null** |

### By model (each n=17, all zero-err)

| Model | mean abs_err | mean signed_bias | zero_err_n |
|---|---|---|---|
| `acheron_estimate_queue` | 0.0 | 0.0 | 17 |
| `tfrmma_prob_queue` | 0.0 | 0.0 | 17 |
| `tfrmma_reduce_ratio` | 0.0 | 0.0 | 17 |

---

## ScorecardPromotionRefused if

1. Treated zero abs_err static identity as cancel-model proven or a scored promote.
2. Invented Brier / PnL / fill outcomes.
3. Retuned frozen knobs after peeking at abs_err.
4. Q6-`000` retune / soft-kill-bar abuse.
5. Live orders.
6. Scored Brier before fill-label GO.

### Next (not this card)

Trade-step series where cancel fractions apply · fill-label GO for Brier · then re-route Examiner for cancel-model / fill channels.

**ACK:** `lab/governance/astra/packets/EXAMINER_ACK_R3_P2_ABS_ERR_SIGNED_BIAS_SCORED_2026-09-23.json`  
**Cites:** Mechanic abs_err md · `results/abs_err_signed_bias.json` · Simulator estimate-ahead handoff · Conductor route  
**Stamped:** 2026-09-23T17:28:00-04:00
