# Mechanic — R3-P2 abs_err / signed_bias — 2026-09-23 (ET)

**Status:** **ABS_ERR_SIGNED_BIAS_COMPUTED** · `calibration_run=true`  
**Packet:** R3-P2-QUEUE-POSITION-CALIB  
**From labels:** Simulator `estimate_ahead` sha256 `f89c06dc1639b194c9d026e157fbfbc2a8b527853afe698dd1f77389eb34c964`  
**Series:** sha256 `74ef9a9bb54054691e26b7b752568c8e833f51d21292034b1f40b9f3ca4ba8b4` (unchanged)  
**Knobs:** sha256 `9a3534219b9be6cbfccb259b23e1245cec682dcee754b5f6a004c55d5354d2a6` (frozen; not retuned)

---

## Definitions

| Metric | Definition |
|---|---|
| `abs_err_contracts` | `|estimate_ahead − queue_position_fp|` |
| `signed_bias` | `estimate_ahead − queue_position_fp` (positive = overestimate of contracts ahead) |
| `brier` | **null** — cancel-safe series `fill_count=0`; waits fill-label GO |
| `pnl` | **null** — not invented |

**Inclusion:** `estimate_status==OK` and non-null `queue_position_fp` and non-null `estimate_ahead`.

---

## Counts

- Label rows: **114** (38 samples × 3 models)
- Metric OK: **51**
- Skipped: **63** — {"estimate_status!='SKIP_INSUFFICIENT_L2_OR_UNSUCCESSFUL'": 63}

---

## Summary by model

### `acheron_estimate_queue`

- n=17
- mean abs_err=0.0
- median abs_err=0.0
- mean signed_bias=0.0
- median signed_bias=0.0
- max abs_err=0.0
- zero_err_n=17

### `tfrmma_prob_queue`

- n=17
- mean abs_err=0.0
- median abs_err=0.0
- mean signed_bias=0.0
- median signed_bias=0.0
- max abs_err=0.0
- zero_err_n=17

### `tfrmma_reduce_ratio`

- n=17
- mean abs_err=0.0
- median abs_err=0.0
- mean signed_bias=0.0
- median signed_bias=0.0
- max abs_err=0.0
- zero_err_n=17

## Overall (all models pooled)

- n=51
- mean abs_err=0.0
- median abs_err=0.0
- mean signed_bias=0.0
- median signed_bias=0.0
- max abs_err=0.0
- zero_err_n=51

---

## Notes

- Static cancel-safe series: tfrmma estimates are join-back `qty_in_front` only (cancel fractions recorded, not applied).
- Do **not** retune frozen knobs against this series after peeking at abs_err.
- Examiner scores after non-null estimate-error metrics (now present for abs_err/bias). Brier still null — not a scored fill-prediction promote.
- No live orders. No Q6-000 retune. No invented PnL.

## Files

- `packets/r3_p2_queue_position/results/abs_err_signed_bias.json`
- `packets/r3_p2_queue_position/results.json`
- `packets/r3_p2_queue_position/MECHANIC_ABS_ERR_SIGNED_BIAS_2026-09-23.md`

**Stamped:** 2026-09-23T17:23:52.770689-04:00  
**Evidence:** [V][H][A]
