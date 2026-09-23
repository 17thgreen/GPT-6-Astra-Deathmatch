# C5 KXBTC15M fee and queue honesty stress

September 23, 2026. This file is the hypothesis. It is committed before source
is frozen and before any unit-test outcome is recorded. No figure in this
document is a trading result. Q6 outcomes that already exist are not re-labeled
as evidence from this probe. This is measurement-only 15-minute crypto
fee and queue honesty stress. It is not live crypto trading.

## Placement

The canonical honesty freeze is
`C5_KXBTC15M_HONESTY_HARNESS_FREEZE_2026-09-23.md`, sha256
`23b908af6e9a7799c9bbdac04b27e683dfccd0c0c25d691df84ff715202d3cab`.
The parent measurement kernel is
`C5_KXBTC15M_MEASUREMENT_FREEZE_KERNEL_2026-09-22.md`, sha256
`4d1b72a38603de181e71f80b3cc6515b170a2bffe11f8770dac1296373e50263`.
`EXPERIMENT_SPEC.md` is the lab hypothesis. It is not a second freeze.

`lab/governance/astra/packets/` is not in this checkout. Packet copies sit
beside the engine and under `packets/`:

| Copy | Path |
|---|---|
| Honesty freeze | `kalshi_c5_kxbtc15m_honesty_lab_20260923/C5_KXBTC15M_HONESTY_HARNESS_FREEZE_2026-09-23.md` |
| Parent kernel | `kalshi_c5_kxbtc15m_honesty_lab_20260923/C5_KXBTC15M_MEASUREMENT_FREEZE_KERNEL_2026-09-22.md` |
| Lab bundle | `kalshi_c5_kxbtc15m_honesty_lab_20260923/C5_KXBTC15M_HONESTY_HARNESS/` |
| Governance freeze | `packets/C5_KXBTC15M_HONESTY_HARNESS_FREEZE_2026-09-23.md` |
| Governance kernel | `packets/C5_KXBTC15M_MEASUREMENT_FREEZE_KERNEL_2026-09-22.md` |
| Governance bundle | `packets/C5_KXBTC15M_HONESTY_HARNESS/` |

`FROZEN_EXPERIMENT.json` keeps `results` and `pnl` null.
`results/EMPTY_RESULTS.json` keeps `freshness_gap_sec`,
`queue_bin_mismatch_rate`, `fee_delta_vs_inherited_model`, and
`turnover_stress_flag` null.

Panel stub: `lab/astra-capture/c5-kxbtc15m/panel_stub.json`,
`panel_version` `2026-09-22.c5-kxbtc15m-v0`, sha256
`60f613e8d775b66b9044ad31d2faf77bba84176f214a7bce599aa7a65b6905f8`.
`admitted_at` is null. `panel_admitted.json` is not in this freeze. When
that file appears later, the harness prefers it and still refuses a non-null
scorecard.

Fee path, fixed: `kalshi_feebook_lab_20260922` at
`22371178cb2663250b4762f328069571c48cb551`.

Rails path, fixed: `kalshi_rails_lab_20260922` at
`6a28e0d6254327ea4e6451c781bec56215ac6cac`.

Shadow fee literals `0.0175` and `0.07` are forbidden in the harness source.
Rates come from the imported feebook table.

## One knob

Honesty stress cadence only.

| Arm | Cadence |
|---|---|
| C5H0 | `per_window` |
| C5H1 | `multi_window_stack` |

Both arms share the feebook pin and the rails pin. The stub exposes one
rolling window. C5H1 may stack a synthetic multi-window fixture in unit
tests. That fixture is not a panel fill and does not write the freeze
scorecard.

C3 bordering-strike stays queued. This pulse does not implement C3.
Cap-SR, capital structure, queue-fragility, the Q labs, the C1 lab, and
the Examiner `000` lab stay untouched.

## Question

Holding the R1-P1 feebook and the R1-P5 rails fixed, does one harness do
all of the following on a code check:

1. Load `panel_stub.json` at `panel_version` `2026-09-22.c5-kxbtc15m-v0`
   with `admitted_at` null. Prefer `panel_admitted.json` when that file
   is present. Refuse a different panel version, a live-order route, a
   live-crypto trading flag, and a bacchus or kxeth15m strategy port.
2. Bind fees through `kalshi_feebook_lab_20260922` and rails through
   `kalshi_rails_lab_20260922` at the commits above. Reuse the Examiner
   fee-channel field names and the hygiene helpers those joins already
   call (`fee_delta`, `freshness_gap_seconds`, `queue_bin_mismatch`) by
   import. Reuse the C1 queue-bin helper only as a sibling agreement
   check. Do not edit those modules.
3. Emit C5H0 and C5H1 schema with the same four instrument fields. C5H0
   scores one window at a time. C5H1 names a stack. The stub does not
   grow a second window inside the harness.
4. Leave `freshness_gap_sec`, `queue_bin_mismatch_rate`,
   `fee_delta_vs_inherited_model`, `turnover_stress_flag`, `results`, and
   `pnl` null in `FROZEN_EXPERIMENT.json` and `results/EMPTY_RESULTS.json`.
   `turnover_stress_flag` stays null while panel volume is null. The
   harness does not invent volume, open interest, or PnL.

This is a code-verification question. It is not a tape walk, not a
Q6-`000` retune, and not live trading. The strategy pointer is null.
`000` stays KEEP and untouched. No queue-fragility arm is reopened.
No Logan demo key is required. Capture, when a later collector runs, is
GET-only on the public elections host. This harness does not place orders
and does not open a network client.

## Scorecard

Until Examiner opens the packet after Clock admit, each of these keys is
present and null:

| Field | Meaning while null |
|---|---|
| `freshness_gap_sec` | Rails freshness gap under 15m rollover |
| `queue_bin_mismatch_rate` | Queue attribution bin versus rails defaults |
| `fee_delta_vs_inherited_model` | Feebook versus the inherited sports-maker fee |
| `turnover_stress_flag` | Window turnover versus a sports T-window label |
| `results` / `pnl` | Null in this freeze |

`write_scorecard` does not write these fields. A non-null value is refused.
A null payload is also refused, so the freeze files stay as committed.

## Do-not

1. No live orders, no signed trading host, and no live crypto trading.
2. No Logan demo or API keys.
3. No invented PnL, volume, or open interest.
4. No Q6-`000` retune, no queue-fragility reopen, and no Cap-SR or A1/A3 reopen.
5. No bacchus or kxeth15m strategy port. ETH15M is watch-only and is not this series.
6. No C3 implementation in this pulse.
7. No inherited fee literals in the harness source.
8. No silent backfill of expired windows.
9. Do not edit the feebook, rails, capital, Cap-SR, Q, Examiner `000`, or C1 trees.

## Empty results

`results/EMPTY_RESULTS.json`, the lab bundle `results.json`, and
`packets/C5_KXBTC15M_HONESTY_HARNESS/results.json` stay
`EMPTY_RESULTS_PRE_EXAMINER` with the four instrument fields, `results`,
and `pnl` null.
