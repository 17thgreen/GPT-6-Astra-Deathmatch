# C3 KXHIGHNY bordering-strike harness

September 23, 2026. This file is the hypothesis. It is committed before source
is frozen and before any unit-test outcome is recorded. No figure in this
document is a trading result. Q6 outcomes that already exist are not re-labeled
as evidence from this probe. This is a measurement-only bordering-strike
weather ladder. It is not a GitHub weather-spread strategy and it is not
cross-city arbitrage.

## Placement

The canonical harness freeze is
`C3_KXHIGHNY_BORDERING_STRIKE_HARNESS_FREEZE_2026-09-23.md`, sha256
`27530d6427794a5559e40c7f56d6cd938d8c57cc8f51406fc26a5b0e36a5fdff`.
The parent measurement kernel is
`C3_KXHIGHNY_MEASUREMENT_FREEZE_KERNEL_2026-09-22.md`, sha256
`0e79a0194e2371efae8d8cac0f4f2ec9ce4cf53f60dd870bae1a1ed7acff3604`.
`EXPERIMENT_SPEC.md` is the lab hypothesis. It is not a second freeze.

`lab/governance/astra/packets/` is not in this checkout. Packet copies sit
beside the engine and under `packets/`:

| Copy | Path |
|---|---|
| Harness freeze | `kalshi_c3_kxhighny_bordering_lab_20260923/C3_KXHIGHNY_BORDERING_STRIKE_HARNESS_FREEZE_2026-09-23.md` |
| Parent kernel | `kalshi_c3_kxhighny_bordering_lab_20260923/C3_KXHIGHNY_MEASUREMENT_FREEZE_KERNEL_2026-09-22.md` |
| Lab bundle | `kalshi_c3_kxhighny_bordering_lab_20260923/C3_KXHIGHNY_BORDERING_STRIKE_HARNESS/` |
| Governance freeze | `packets/C3_KXHIGHNY_BORDERING_STRIKE_HARNESS_FREEZE_2026-09-23.md` |
| Governance kernel | `packets/C3_KXHIGHNY_MEASUREMENT_FREEZE_KERNEL_2026-09-22.md` |
| Governance bundle | `packets/C3_KXHIGHNY_BORDERING_STRIKE_HARNESS/` |

`FROZEN_EXPERIMENT.json` keeps `results` and `pnl` null.
`results/EMPTY_RESULTS.json` keeps `adjacent_spread_gap`,
`bordering_depth_imbalance`, `fee_delta_vs_inherited_model`,
`freshness_gap_sec`, and `multi_city_inventory_join` null.

Panel stub: `lab/astra-capture/c3-kxhighny/panel_stub.json`,
`panel_version` `2026-09-22.c3-kxhighny-v0`, sha256
`2a5da7fe85ca1adc6b7c4dcf9e09ed5c6bb62be6b5c9b42731e36e31d1e8dfea`.
`admitted_at` is null. `panel_admitted.json` is not in this freeze. When
that file appears later, the harness prefers it and still refuses a non-null
scorecard.

Fee path, fixed: `kalshi_feebook_lab_20260922` at
`22371178cb2663250b4762f328069571c48cb551`.

Rails path, fixed: `kalshi_rails_lab_20260922` at
`6a28e0d6254327ea4e6451c781bec56215ac6cac`.

Shadow fee literals `0.0175` and `0.07` are forbidden in the harness source.
Rates come from the imported feebook table.

The C5 honesty harness stays as merged at `ee69245a`. This pulse does not
edit it. Hygiene helpers are imported the way that harness uses them
(`fee_delta`, `freshness_gap_seconds`). The Examiner orchestrator and the
queue-fragility module are not loaded.

## One knob

Strike band only.

| Arm | Strike band |
|---|---|
| C3B0 | `near_extreme` |
| C3B1 | `mid_ladder` |

Both arms share the feebook pin and the rails pin.

A loaded price at or below `0.10`, or at or above `0.90`, is
`near_extreme`. A price strictly between those cuts is `mid_ladder`.
Scout role strings such as `mid_ladder_anchor` do not select the arm.
The cuts are a schema rule for this harness. They are not a trading
threshold and they are not fit to a PnL.

A bordering pair is two markets in the same event and the same band that
are neighbors after sorting by `floor_strike`. Neighbor means next to each
other in that loaded list. A strike missing from the six-ticker seed is
not invented. The open-list 429 notes on the stub stay as written.

The stub may put most rows in one band. C3B1 may use
`fixtures/synthetic_ladder.json` when the stub has no mid-ladder pair.
That fixture is not a panel fill and does not write the freeze scorecard.

## Question

Holding the R1-P1 feebook and the R1-P5 rails fixed, does one harness do
all of the following on a code check:

1. Load `panel_stub.json` at `panel_version` `2026-09-22.c3-kxhighny-v0`
   with `admitted_at` null. Prefer `panel_admitted.json` when that file
   is present. Refuse a different panel version, a live-order route, a
   GitHub weather-spread EV flag, and an R3-P3 strategy merge.
2. Bind fees through `kalshi_feebook_lab_20260922` and rails through
   `kalshi_rails_lab_20260922` at the commits above. Reuse the hygiene
   helpers `fee_delta` and `freshness_gap_seconds` by import. Do not edit
   those modules. Do not load queue-fragility.
3. Emit C3B0 and C3B1 schema. Each pair is a structure object: tickers,
   series, floors, and the band. Spread, depth, fee delta, freshness, and
   the multi-city join stay null on the object. C3B0 and C3B1 share the
   same fee pin and rails pin.
4. Build a NY versus CHI presence table from `occurrence_datetime`
   calendar dates already on the panel. `KXHIGHNY` and `KXHIGHCHI` set
   presence flags. `multi_city_inventory_join` on the scorecard stays
   null. The presence table carries `arb_pnl` null. It is not a PnL.
5. Leave `adjacent_spread_gap`, `bordering_depth_imbalance`,
   `fee_delta_vs_inherited_model`, `freshness_gap_sec`,
   `multi_city_inventory_join`, `results`, and `pnl` null in
   `FROZEN_EXPERIMENT.json` and `results/EMPTY_RESULTS.json`. The harness
   does not invent volume, open interest, or PnL.

This is a code-verification question. It is not a tape walk, not a
Q6-`000` retune, and not live trading. The strategy pointer is null.
R3-P3 weather preference on the stub is a cite. Kernels stay distinct.
No Logan key is required. Capture, when a later collector runs, is
GET-only on the public elections host. This harness does not place orders
and does not open a network client.

## Scorecard

Until Examiner opens the packet after Clock admit, each of these keys is
present and null:

| Field | Meaning while null |
|---|---|
| `adjacent_spread_gap` | Spread gap between adjacent threshold strikes |
| `bordering_depth_imbalance` | Depth imbalance across bordering YES/NO books |
| `fee_delta_vs_inherited_model` | Feebook versus the inherited sports-maker fee |
| `freshness_gap_sec` | Rails freshness gap on weather ladder samples |
| `multi_city_inventory_join` | NY versus CHI same-calendar presence instrument |
| `results` / `pnl` | Null in this freeze |

`write_scorecard` does not write these fields. A non-null value is refused.
A null payload is also refused, so the freeze files stay as committed.
An in-memory `fee_delta` or `freshness_gap_seconds` call is a helper check.
It is not a copy into the freeze field of the same name.

## Do-not

1. No live orders, no signed trading host, and no Logan keys.
2. No GitHub weather-spread author PnL as Astra evidence. Ladder objects
   are a structure hypothesis.
3. No invented cross-city arb and no settlement-penalty EV.
4. No Q6-`000` retune, no queue-fragility reopen, and no Cap-SR reopen.
5. No merge of this kernel into R3-P3 as a strategy. The stub cite stays
   a preference for panel material.
6. No C5 dual-steal. The C5 lab is not edited.
7. No inherited fee literals in the harness source.
8. No silent backfill and no invented open interest beyond the stub bytes.
9. Do not edit the feebook, rails, capital, Cap-SR, C5, Q, or C1 trees.

## Empty results

`results/EMPTY_RESULTS.json`, the lab bundle `results.json`, and
`packets/C3_KXHIGHNY_BORDERING_STRIKE_HARNESS/results.json` stay
`EMPTY_RESULTS_PRE_EXAMINER` with the five instrument fields, `results`,
and `pnl` null.
