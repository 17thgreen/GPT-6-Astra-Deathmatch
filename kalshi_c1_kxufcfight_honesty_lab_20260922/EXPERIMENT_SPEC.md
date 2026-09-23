# C1 KXUFCFIGHT fee and queue honesty bakeoff

September 22, 2026 (desk ET). This file is the hypothesis. It is committed
before source is frozen and before any unit-test outcome is recorded. No
figure in this document is a trading result. Q6 outcomes that already exist
are not re-labeled as evidence from this lab.

## Pin lock

The canonical kernel is
`packets/C1_KXUFCFIGHT_MEASUREMENT_FREEZE_KERNEL_2026-09-22.md`. Its sha256 is
`a191c9b3f71030445d1d32684feb6dc1bf09abb7e09403d5dbdf1927eafc63c9`.
The scout packet is `packets/scout_c1_kxufcfight/FROZEN_EXPERIMENT.json`.
`EXPERIMENT_SPEC.md` is the lab hypothesis. It is not a second freeze.

Panel schema seed: `lab/astra-capture/c1-kxufcfight/panel_stub.json`,
`panel_version` `2026-09-22.c1-kxufcfight-v0`, sha256
`2cc661d86202d3daf9ffa45320e39d249852a97490f458f72ab7ea8ec5c81a00`.
`admitted_at` is null. The recorder is not started.

Fee path, fixed: `kalshi_feebook_lab_20260922` at
`22371178cb2663250b4762f328069571c48cb551`.

Rails path, fixed: `kalshi_rails_lab_20260922` at
`6a28e0d6254327ea4e6451c781bec56215ac6cac`.

The same two commits are the instruments on the Q6-`000` honesty channel.
This lab points those instruments at the UFC fight ML panel. It does not
read the `000` fills gzip, does not edit the `000` allocator, and does not
open a second `000` lab.

## Placement

`kalshi_feebook_lab_20260922` and `kalshi_rails_lab_20260922` are frozen
cores. This lab imports those modules and does not edit them. The Q6, Q7,
capital-structure, hygiene, queue-fragility, and examiner-`000` trees stay
untouched. The new directory is
`kalshi_c1_kxufcfight_honesty_lab_20260922`.

## Question

On the pinned `KXUFCFIGHT` panel seed, under the shared 5000 USD measurement
label, does one harness do all of the following on a code check:

1. Load `panel_version` `2026-09-22.c1-kxufcfight-v0` and refuse a different
   version. Keep `admitted_at` null. Leave the dropped ORTDAS tickers out.
2. Build the reciprocal book with `feebook.reciprocal_book`: `bid_YES`,
   `bid_NO`, `ask_YES = 1 - bid_NO`, `ask_NO = 1 - bid_YES`, `spread_YES`.
   A missing bid leaves the implied ask unset. The extreme-favorite fixture
   is part of the check.
3. Price any hypothetical size C at P with `feebook.order_fee` for series
   `KXUFCFIGHT`, formula
   `astra.r1p1.feebook.claude_order_level_ceil.v1`, `round_up` true. The
   series is absent from the frozen override map, so resolution is
   `default_unknown_series` and the multiplier is the table default, which
   the panel live-GET multiplier also records as 1.
4. Emit rails labels only: `content_fresh_flag` from content or transaction
   time (`rails.judge_freshness`; a keepalive is stale),
   `maker_credit_floor_zero_refuse` from `rails.admit_maker_quote`, and
   `queue_attribution_bin` by exact match to `rails.QUEUE_SCENARIO_LABELS`
   (otherwise `outside_pinned_bins`). These labels match the Q6-`000`
   hygiene instrument on the same inputs. They are labels, not a strategy.
5. Refuse completed-profit classification when the feebook fee channel is
   missing, and refuse a shadow formula (Grok comparator or the inherited
   Q6 fixed-point model) in place of the examiner formula. Source in this
   lab does not carry the shadow rate literals.
6. Leave every measurement field, `results`, and `pnl` null in
   `FROZEN_EXPERIMENT.json`, `results/EMPTY_RESULTS.json`, and
   `packets/scout_c1_kxufcfight/`. In-memory fixture labels are not copied
   into those files. `volume_fp` and `open_interest_fp` stay null. The
   kernel's scout page-sample sums are a cite, not a panel fill.

This is a code-verification question. It is not a tape walk and not live
trading. The markout horizons `1m`, `5m`, and `15m` are not emitted.

## Predeclared fixture identities

Synthetic books live at `fixtures/synthetic_orderbooks.json`. They are not a
live GET and they carry no volume and no open interest. Production orderbook
bytes, when a later capture writes them, belong under
`lab/astra-capture/c1-kxufcfight/orderbooks/`. This freeze has no production
orderbook pin. A file in that directory without a pin is refused. The stub
panel remains the schema.

| Fixture | Book |
|---|---|
| `KXUFCFIGHT-26SEP22DEGMOR-DEG` | YES bid 0.98, NO bid 0.01, so ask YES 0.99, ask NO 0.02, spread YES 0.01 |
| `KXUFCFIGHT-26SEP22DEGMOR-MOR` | YES bid 0.01, NO bid 0.98, so ask YES 0.02, ask NO 0.99, spread YES 0.01 |
| `KXUFCFIGHT-26SEP22CONGUA-CON` | YES bid 0.40, NO bid 0.45, so ask YES 0.55, ask NO 0.60, spread YES 0.15 |
| `KXUFCFIGHT-26SEP22CONGUA-GUA` | YES bid only. Ask YES, ask NO, and spread YES stay unset |

Queue ahead equal to `rails.QUEUE_AHEAD_DEFAULT` labels `q3300`. Queue ahead
equal to `rails.STRESS_QUEUE_AHEAD` labels `q10000`. Any other non-negative
size labels `outside_pinned_bins`. A one-contract maker quote at 0.01 is
refused by the maker-credit floor. A one-contract maker quote at 0.50 is
admitted. Those two quotes are rails checks, not panel open interest.

`KXUFCFIGHT-26SEP22DEGMOR` occurrence `2026-09-23T04:40:00Z` minus sample
`2026-09-23T04:00:00Z` is 40 minutes, in memory only. The scorecard key
`timing_shape` stays null.

## Constants

| Pin | Frozen value |
|---|---|
| Series | `KXUFCFIGHT` |
| Panel version | `2026-09-22.c1-kxufcfight-v0` |
| Strategy pointer | null |
| Capital | Shared 5000 USD measurement label. Capital-structure modes A1, A2, and A3 are refused |
| Examiner formula | `feebook.EXAMINER_FORMULA_ID` |
| Empty outputs | `results/EMPTY_RESULTS.json` |
| Packet results | `packets/scout_c1_kxufcfight/results.json` and `packets/scout_c1_kxufcfight/results/EMPTY_RESULTS.json` |
| Capture slot | `lab/astra-capture/c1-kxufcfight/` |

## Scorecard

One packet. Until Examiner GO, each of these keys is present and null:

| Field | Meaning while null |
|---|---|
| `reciprocal_book` | Book algebra checked in memory only |
| `fee_channel` | `order_fee` binding checked in memory only |
| `content_fresh_flag` | Rails freshness label |
| `maker_credit_floor_zero_refuse` | Rails credit-floor label |
| `queue_attribution_bin` | Rails queue-bin label |
| `timing_shape` | Minutes to occurrence, in memory only |
| `volume_fp` / `volume_24h_fp` / `open_interest_fp` | Unset. Scout sums are not copied |
| `strategy_ev` / `beats_000` / `completed_profit` | No strategy claim |
| `fill_rate` / `annualization` / `live_promotion` | Not scored |
| `results` / `pnl` | Null in this freeze |

`write_scorecard` does not write these fields. A non-null value is refused.
A null payload is also refused, so the freeze files stay as committed.

## Do-not

1. No live orders and no signed trading host.
2. No invented PnL, volume, or open interest.
3. No Q6-`000` retune, no Q7 reopen, no capital-structure A2 or A3, and no A1 wallet partition.
4. No scoring with inherited Q6 or Q7 fee literals.
5. No silent panel backfill and no expansion of the four-market seed.
6. Do not edit the feebook core or the rails core.
7. No wholesale combat market-making strategy import.

## Empty results

`packets/scout_c1_kxufcfight/results.json`,
`packets/scout_c1_kxufcfight/results/EMPTY_RESULTS.json`, and
`results/EMPTY_RESULTS.json` stay `NOT_RUN` with measurement fields null.
