# Q6S5 KXMLBSPREAD strategy-fill path

Hypothesis committed before any unit outcome. Measurement infrastructure only.
Feature family `Q6S5-MLBSPREAD-STRATEGY-FILL`. Series `KXMLBSPREAD` only.
Packet `Q6S5-KXMLBSPREAD-STRATEGY-FILL`.

This lab does not place live orders, does not run `admit.py`, and does not
write `results`, `pnl`, or arm ROI. Examiner status stays `HOLD_PRE_PR`
with `stub_ready` false until merge and a later Conductor/Examiner kick.

## Authority check before code

Checked on `origin/main` at `cb8957d7086c9ab82a1d25090bf90d6c17fbc217`
(fetched 2026-09-29). The cited conductor bytes are absent from this
checkout and were not recreated:

| Pin | Path | Claimed sha256 |
|---|---|---|
| Conductor ACCEPT | `lab/governance/astra/packets/CONDUCTOR_ACCEPT_VARIANTS_Q6S5_STRATEGY_FILL_FREEZE_2026-09-29.json` | `c6f95b32a9224a6beede1a8c0e3d7f0a5a4530cc8b3d0b9d997995f65d64f8f3` |
| Freeze markdown | `lab/governance/astra/packets/Q6S5_KXMLBSPREAD_STRATEGY_FILL_FREEZE_2026-09-25.md` | `9f50ba19694083c774bbe2a6cff491d1a2f81ed3a6f9cc21a3641a938c84955d` |
| Kick | `lab/governance/astra/packets/CONDUCTOR_KICK_VARIANTS_Q6S5_STRATEGY_FILL_FREEZE_2026-09-25.json` | prefix `dc19794b` (full digest not supplied; not invented) |
| ADMIT-1 gap ruling | cited as `ac7cfe63` | prefix only (full digest not supplied; not invented) |
| Packet bundle | `lab/governance/astra/packets/Q6S5_KXMLBSPREAD_STRATEGY_FILL/` (`FROZEN_EXPERIMENT`, `SOURCE_PINS`, `EMPTY_RESULTS`) | absent; hashes not supplied |

`digest_all_match_claimed` stays false until those bytes re-hash on disk.
Parent Q6S5 fee+queue pins that are already in this checkout stay import-only.

## Knob

One knob: `fill_model`.

| Model | Status |
|---|---|
| `public_trade_through_conservative` | Implemented path. A public print is a through observation only when its timestamp is strictly after the resting quote and its YES price is strictly through the resting price (bid: print below the bid; ask: print above the ask). A touch is not a through. |
| `mechanic_demo_observed` | Cells stay null. Status `UNAVAILABLE`. Demo observations are not invented. |

Parent arms stay the fee+queue values:

| Arm | Slice |
|---|---|
| Q6S5A0 | `maker_vs_taker_native` |
| Q6S5A1 | `content_fresh_vs_stale_bin` |

Those slices are not retuned. Arm ROI stays null.

## Fee

Label `CACHE_NOT_R1P1`. `fee_type` `quadratic`. Multiplier `0.5`.
`formula_id` null. `cache_labeled` true. `live_r1p1` false.
Feebook `22371178cb2663250b4762f328069571c48cb551` and rails
`6a28e0d6254327ea4e6451c781bec56215ac6cac` stay fixed imports.
The cache label is not an R1-P1 live `/series` pin.

## Simulated fills

`counts_toward_keep` is false. Contract counts, fill prices, `results`,
`pnl`, and arm ROI stay null. A through observation is not a fill.
Missing queue bytes prefixed `08aa54de` are not recreated.

## Refuses

- ADMIT-1 exclusion window `[2026-09-27T00:00:00Z, 2026-09-30T04:00:00Z)`. No backfill.
- Any read of ADMIT-1 `capture.sqlite`.
- Lookahead: trade time at or before the quote, or a later book or settlement used as an input.
- Lee-Ready on every input.
- Invented fills and invented PnL.
- Live orders, Logan keys, dual-cloud, `admit.py`.
- Q6-000, S1 KXMLBGAME ML, Cap-SR, and Q6S1 retune.

## Panel

Parent stub `lab/astra-capture/q6s5-kxmlbspread/panel_stub.json`,
`panel_version` `2026-09-25.q6s5-kxmlbspread-v0`, `admitted_at` null,
sha256 `c7f1f1f4ca263838c4600ed46db8f525b68efc5399a567bd60929d18d76803cc`.
The capture file is not rewritten. `panel_admitted.json` is absent.

## Scorecard

`results`, `pnl`, Q6S5A0 ROI, and Q6S5A1 ROI stay null.
Examiner v1.2 verdict, `gate_status`, and common-scorecard values stay null.
This spec does not mark Examiner `READY`.
