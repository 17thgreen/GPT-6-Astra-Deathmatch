# Q6S5 KXMLBSPREAD FL-band settled-tape

Hypothesis and row rules are the frozen packet
`Q6S5-KXMLBSPREAD-FL-BAND-SETTLED-TAPE`, vendored verbatim.

- Feature family: `settled_tape_fl_band`
- Parent packet: `Q6S5-KXMLBSPREAD-FEEQUEUE-HARNESS`
- One knob: `price_band` on taker-purchased price `p_taker`
- Arms: `Q6S5FL0` longshot `[0.00, 0.20)`, `Q6S5FL1` mid `[0.20, 0.80)`, `Q6S5FL2` favorite `[0.80, 1.00]`
- Registry: R3-P3 10¢ bands b00–b09, sha256 `0860cbe28d28ecc6142ddf6f1ebb67792084264ed82e0b4d868c3b3138ea5312`. No rebin.
- Universe: 6 finalized panel_admitted markets, 3 events (HOUATH, LAASEA, SDLAD), 11,723 pinned prints. Six Sep-25 markets stay out of scope.
- Primary metric: `maker_gross_roi_delta_FL0_minus_FL1` (gross, fee-free). Secondary: FL2−FL1, CACHE post-fee, LOEO/LOMO, `one_tick_worse`, `fees_2x`.
- Fee label: `CACHE_NOT_R1P1`. Not R1-P1.
- Orthogonal to `analysis_slice` (PR58) and `fill_model` (PR60).
- Verdict ceiling: ITERATE. `promote` false. `counts_toward_keep` false.
- `results` and `pnl` stay null until Examiner scores.

Conductor ACCEPT sha256 `8e4fbac7d0426bc67c1f53fb8057a382fe46da738bd701cb970a9812a6dc2a3b`.
Freeze sha256 `fb6540f52ed5f819ccf6e80bf0cf7eb6d951e065416b9d550fead0c6d06043fa`.
Authentic bundle sha256 `63b5d981bc06f684eebb69a8ac29394534f8ae52c101f3018557544f14e29857`.

Examiner status at implement: `HOLD_PRE_PR`. The post-PR examiner path is `READY_NOT_SCORED`. This lab does not mark SCORED.

## Conductor addendum 2026-10-01

Ruling `CONDUCTOR_RULING_Q6S5_FL_BAND_IN_SAMPLE_DEV_LABEL` sha256 `09763030c67df066f2b59346200813e181777670cd46fcee6b8877a6dd74d754` is an addendum to ACCEPT `8e4fbac7d0426bc67c1f53fb8057a382fe46da738bd701cb970a9812a6dc2a3b`. Historical tape is admissible with `evidence_class` `IN_SAMPLE_DEV`. `pre_admitted_at` is true iff trade `created_time` is strictly before `2026-09-25T04:37:47Z`. A trade at that instant is false. The label is on every output row, the summary, and the scorecard stub. Counts of pre- and post-admitted_at rows are reported per arm with no outcome values. `promote` stays false. `counts_toward_keep` stays false. Verdict ceiling stays ITERATE. `results` and `pnl` stay null. The price_band registry is not rebinned.
