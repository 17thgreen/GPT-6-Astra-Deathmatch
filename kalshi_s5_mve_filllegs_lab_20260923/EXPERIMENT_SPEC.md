# S5 KXMVECROSSCATEGORY fill-vs-legs harness

September 23, 2026. This file is the hypothesis. It is committed before source
is frozen and before any unit-test outcome is recorded. No figure in this
document is a trading result. Q6 outcomes that already exist are not re-labeled
as evidence from this probe. This is measurement-only combo fill versus
independent-leg product. Feature family **MVE-FL**.

## Placement

The canonical harness freeze is
`S5_KXMVECROSSCATEGORY_FILLLEGS_HARNESS_FREEZE_2026-09-23.md`, sha256
`8a118e6f1fdc8c22c6e559f395667aedffa5d270d067e39b6ae3ee24b2046d16`.
The parent measurement kernel is
`S5_KXMVECROSSCATEGORY_MEASUREMENT_FREEZE_KERNEL_2026-09-22.md`, sha256
`a28932ba13b4913b69c48b73dde8ba066cebd212670d0b1cbb5ea8e93734b8ba`.
`EXPERIMENT_SPEC.md` is the lab hypothesis. It is not a second freeze.

`lab/governance/astra/packets/` is not in this checkout. Packet copies sit
beside the engine and under `packets/`:

| Copy | Path |
|---|---|
| Harness freeze | `kalshi_s5_mve_filllegs_lab_20260923/S5_KXMVECROSSCATEGORY_FILLLEGS_HARNESS_FREEZE_2026-09-23.md` |
| Parent kernel | `kalshi_s5_mve_filllegs_lab_20260923/S5_KXMVECROSSCATEGORY_MEASUREMENT_FREEZE_KERNEL_2026-09-22.md` |
| Lab bundle | `kalshi_s5_mve_filllegs_lab_20260923/S5_KXMVECROSSCATEGORY_FILLLEGS_HARNESS/` |
| Governance freeze | `packets/S5_KXMVECROSSCATEGORY_FILLLEGS_HARNESS_FREEZE_2026-09-23.md` |
| Governance kernel | `packets/S5_KXMVECROSSCATEGORY_MEASUREMENT_FREEZE_KERNEL_2026-09-22.md` |
| Governance bundle | `packets/S5_KXMVECROSSCATEGORY_FILLLEGS_HARNESS/` |

`FROZEN_EXPERIMENT.json` keeps `results` and `pnl` null.
`results/EMPTY_RESULTS.json` keeps `fill_vs_legs_mid_gap`,
`combo_fee_delta_vs_feebook`, `legs_join_rate`, and `freshness_gap_sec` null.

Panel stub: `lab/astra-capture/s5-kxmvecrosscategory/panel_stub.json`,
`panel_version` `2026-09-22.s5-kxmvecrosscategory-v0`, sha256
`4918b820d454c5f997ea100917859f7e9467d92933bed1bc8a55c81ab8ce5b8e`.
`admitted_at` is null. The seed is 5 markets and 21 events. Every seed
market has `mve_selected_legs` (legs join 5/5 on the stub document).
`panel_admitted.json` is not in this freeze. When that file appears later,
the harness prefers it and still refuses a non-null scorecard.

Fee path, fixed: `kalshi_feebook_lab_20260922` at
`22371178cb2663250b4762f328069571c48cb551`.
Series override, fixed: `quadratic_with_combo_maker_fees`, multiplier 1,
on `KXMVECROSSCATEGORY`, `KXMVECROSSCATEGORY-SHARD1`, and
`KXMVESPORTSMULTIGAMEEXTENDED`. The override is applied in memory by this
harness. The feebook tree is not edited.

Rails path, fixed: `kalshi_rails_lab_20260922` at
`6a28e0d6254327ea4e6451c781bec56215ac6cac`.

Shadow fee literals `0.0175` and `0.07` are forbidden in the harness source.
Rates come from the imported feebook table.

## One knob

Leg mid source only.

| Arm | Leg mid source |
|---|---|
| S5L0 | `tob_1m` |
| S5L1 | `synthetic_leg_product` |

S5L0 builds the independent-leg product from 1-minute TOB YES mids. A NO
leg uses `1 - mid`. A missing bid stays unset. A stale leg is refused.
The seed tape is empty, so S5L0 on the stub records no fill and no product.

S5L1 is a unit-only synthetic leg-mid vector with a known product. That
fixture may carry a synthetic print for schema. The print does not enter
`fill_vs_legs_mid_gap`. It is not a panel invent.

Both arms share the combo feebook pin and the rails pin.

## Question

Holding the R1-P1 feebook series override and the R1-P5 rails fixed, does
one harness do all of the following on a code check:

1. Load `panel_stub.json` at `panel_version`
   `2026-09-22.s5-kxmvecrosscategory-v0` with `admitted_at` null, 5 markets,
   21 events, and complete `mve_selected_legs` on every seed market. Prefer
   `panel_admitted.json` when that file is present. Refuse a different panel
   version, a live-order route, an RFQ `/communications` route, an R1-P4
   strategy flag, a Logan key request, and `admit.py`.
2. Bind fees through `kalshi_feebook_lab_20260922` with an in-memory series
   override `quadratic_with_combo_maker_fees` / multiplier 1, and rails
   through `kalshi_rails_lab_20260922`, at the commits above. Refuse a quote
   whose formula id is not the examiner formula. Refuse inherited fee
   literals in this harness source. Do not edit those modules.
3. Emit S5L0 and S5L1 schema. S5L0 names `tob_1m` and leaves the product
   unset on the empty seed. S5L1 names `synthetic_leg_product`. The known
   product is computed only from `fixtures/synthetic_leg_product.json`.
4. Leave an empty trade tape empty. Do not invent fills. A synthetic print
   stays inside the unit fixture.
5. Leave `fill_vs_legs_mid_gap`, `combo_fee_delta_vs_feebook`,
   `legs_join_rate`, `freshness_gap_sec`, `results`, and `pnl` null in
   `FROZEN_EXPERIMENT.json` and `results/EMPTY_RESULTS.json`. The stub
   document's own `legs_join_rate` string is seed metadata. It is not copied
   into the scorecard.

This is a code-verification question. It is not a tape walk, not a
Q6-`000` retune, and not live trading. The strategy pointer is null.
RFQ is out of scope. R1-P4 strategy stays closed. No Logan key is required.
Capture, when a later collector runs, is GET-only on the public elections
host. This harness does not place orders and does not open a network client.

## Scorecard

Until Examiner opens the packet after Clock admit, each of these keys is
present and null:

| Field | Meaning while null |
|---|---|
| `fill_vs_legs_mid_gap` | Combo mid or print versus the independent-leg product |
| `combo_fee_delta_vs_feebook` | Observed combo fee versus the R1-P1 series override |
| `legs_join_rate` | Fraction of markets with complete `mve_selected_legs` |
| `freshness_gap_sec` | Rails freshness gap on joined samples |
| `results` / `pnl` | Null in this freeze |

`write_scorecard` does not write these fields. A non-null value is refused.
A null payload is also refused, so the freeze files stay as committed.

## Dead cards

| Card | Handling |
|---|---|
| Cap-SR / Cap-SR-FX | Orthogonal. Capital soft policy is a different feature family |
| S1 empty-events | Deferred |
| S2 + R2-P4 | WAIT until C1 T−7d smoke |
| R3-P2 queue_position_fp | HOLD |
| QF reopen | Denied |
| RFQ 401 / KXMVENFL empty | Out of scope |
| C1 empty-book / Q7 Arm B | Nearest blocked siblings. They stay closed |
| S4 NCAAF / R2-P3 prop slate | Queued behind this implement |

## Do-not

1. No live orders, no signed trading host, and no RFQ `/communications` path.
2. No Logan keys.
3. No R1-P4 strategy open.
4. No invented fills, invented open interest, or invented PnL.
5. No Q6-`000` retune, no queue-fragility reopen, and no Cap-SR reopen.
6. No `admit.py`.
7. No inherited fee literals in the harness source.
8. Do not edit the feebook, rails, Cap-SR, Cap-SR-FX, C3, C5, R3-P3, or Q lab trees.

## Empty results

`results/EMPTY_RESULTS.json`, the lab bundle `results.json`, and
`packets/S5_KXMVECROSSCATEGORY_FILLLEGS_HARNESS/results.json` stay
`EMPTY_RESULTS_PRE_EXAMINER` with the four instrument fields, `results`,
and `pnl` null.
