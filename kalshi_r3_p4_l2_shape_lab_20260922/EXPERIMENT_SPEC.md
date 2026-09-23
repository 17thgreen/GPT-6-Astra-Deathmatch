# R3-P4 L2 shape: Dubach SF1 and SF2 on Kalshi bids-only books

September 23, 2026. This file is the hypothesis. It is committed before source is
frozen and before any unit-test outcome is recorded. No figure in this document
is a Kalshi trading result. Q1–Q6 outcomes that already exist are not
re-labeled as evidence from this lab. The numbers below are predeclared
identities of the synthetic fixtures.

This lab is a quote-side microstructure panel. It is not a strategy, not a
queue study, and not a fee study.

## Placement

`kalshi_feebook_lab_20260922` and `kalshi_rails_lab_20260922` are frozen
evidence snapshots. This lab imports those modules and does not edit them.
Q6, Q7, the capital-structure lab, the R2-P1 hygiene lab, the queue-fragility
lab, and the earlier Q labs stay untouched. The new directory is
`kalshi_r3_p4_l2_shape_lab_20260922`.

Book path: `feebook.reciprocal_book`, commit
`22371178cb2663250b4762f328069571c48cb551`.

Freshness path: `rails.judge_freshness` and `rails.canonical_book_content`,
commit `6a28e0d6254327ea4e6451c781bec56215ac6cac`. A snapshot is included only
when that predicate returns fresh.

## Question

On synthetic GET-shaped bids-only books, do SF1 and SF2 below reproduce the
predeclared half-spread, decile, depth-share, and KL identities, and does the
rails content-fresh gate drop a stale duplicate and a keepalive?

This is a code-verification question. It is not a backtest and not live
trading. `FROZEN_EXPERIMENT.json` keeps `results` and `pnl` null.
`results/EMPTY_RESULTS.json` keeps the same fields null. Nothing in this lab
writes a fixture median into those files.

## Attribution

SF1 and SF2 are the quote-side shape statistics in Philipp D. Dubach, "The
Anatomy of a Decentralized Prediction Market: Microstructure Evidence from the
Polymarket Order Book" (arXiv:2604.24366, 24 August 2026). The paper's bytes
are not vendored. The Polymarket panel numbers in that paper are not Kalshi
results and are not recomputed here.

Two readings of the paper's spread column are not silently merged. Section 5.1
bins "quoted half-spread (in basis points of mid)". The introduction says the
central decile's median quoted half-spread is about 200 bps. Table 1 prints
400 bps on that same central range, and the prose calls 1,300–1,800 bps a full
quoted spread whose half is 650–900 bps. This lab pins the half-spread:

```
half_spread_bps = (spread / 2) / mid * 10000
```

Table 1's larger column is not the pinned statistic.

## Pin A — reciprocal mid and half-spread

Inputs are Kalshi `orderbook_fp` objects with `yes_dollars` and `no_dollars`.
Prices and sizes are `Decimal`, `int`, or `str`. Floats are rejected by the
feebook parser. Best bid is the highest positive-size price. Array order is
not trusted.

```
book        = feebook.reciprocal_book(orderbook_fp)
mid         = (bid_yes + ask_yes) / 2
spread      = spread_yes
half_spread = spread / 2
half_spread_bps = half_spread / mid * 10000
```

`ask_yes` and `spread_yes` come from the feebook. This lab does not re-derive
the reciprocal identities and does not clamp a negative spread. A missing YES
bid or a missing NO bid leaves the spread unset; the snapshot is incomplete
and is not given a zero spread. A mid that is not strictly positive has no
bps-of-mid figure and is refused. The quoted contract is YES. The NO book is
the other observed bid ladder. Its size is not copied onto a synthetic ask
price as a second observation.

## Pin B — SF1 deciles

Deciles are Dubach Table 1's absolute probability bins, not sample quantiles.
On a handful of fixtures, empirical quantiles are not the pinned partition.

| Bin | Mid lo | Mid hi |
|---|---|---|
| 0 | 0.0 | 0.1 |
| 1 | 0.1 | 0.2 |
| 2 | 0.2 | 0.3 |
| 3 | 0.3 | 0.4 |
| 4 | 0.4 | 0.5 |
| 5 | 0.5 | 0.6 |
| 6 | 0.6 | 0.7 |
| 7 | 0.7 | 0.8 |
| 8 | 0.8 | 0.9 |
| 9 | 0.9 | 1.0 |

The low edge is included. The high edge is excluded, except bin 9, which
includes mid `1`. A market with several fresh snapshots is binned by the
arithmetic mean of its YES mids. The market's SF1 value is the median of its
snapshot half-spread bps. The bin's reported value is the median of those
market values. An even count uses the mean of the two central values. An
empty bin has count 0 and a null median. The null is not a zero spread.

Sports and non-sports are an optional slice of the same rule. The category
tags on the fixtures are `sports` and `non_sports`. A ticker that changes
category is refused. This slice is not Dubach SF5 and it does not use trades.

## Pin C — SF2 depth share and KL

Top-10 depth is rank-aligned and summed across the two observed bid ladders.
Rank 1 is the best bid on that ladder. Rank `k` on the NO ladder is the k-th
best YES ask under the reciprocal price identity. The size at that rank is
the observed NO size. It is not an invented ask size.

```
depth_k = yes_bid_size_at_rank_k + no_bid_size_at_rank_k
share_k = depth_k / sum(depth_1 .. depth_10)
```

Same-price rows are one level. Size zero is not a level. A ladder with fewer
than 10 positive levels keeps the missing ranks at size 0. Those zeros are
absent levels, not fabricated contracts. A side with no positive size leaves
the book incomplete; the missing side is not replaced by a zero ladder.
Shares are exact rationals and sum to 1. L1 share is `share_1`.

The uniform null is `1/10` at each rank. KL divergence, in nats, natural log:

```
KL = sum_k share_k * ln(share_k / (1/10))
```

`0 * ln(0)` is 0. A flat book has KL 0. A book with all top-10 depth on L1
has KL `ln(10)`. A market with several fresh snapshots averages the depth
vector first, then forms shares and KL from that average. The panel reports
the median L1 share and the median KL across markets. `top_heavy` means L1
share strictly greater than `1/2`.

## Pin D — content-fresh gate

Inclusion uses `rails.judge_freshness` on `rails.BookObservation` whose
content token is `rails.canonical_book_content` of the `orderbook_fp` object
and whose transaction time is the fixture's `transaction_time`.

```
keepalive true                         -> refuse (keepalive_ignored)
previous absent and keepalive false    -> include (initial)
content differs                        -> include (content_changed)
transaction time differs               -> include (transaction_time_changed)
otherwise                              -> refuse (unchanged)
```

A refused snapshot does not enter SF1 or SF2. The direct gate raises
`StaleSnapshotRefused`. The fixture walker records the refusal and continues.
`received_at` is not an argument. There is no collector and no live poll.

## Fixtures

`fixtures/l2_shape_fixtures.json` is a synthetic GET body list. It is not a
live capture. Notes on each row are comments. The walker does not read them
as a freshness verdict.

| Ticker | Category | Pinned shape |
|---|---|---|
| `SYN-SPORTS-D0` | sports | One fresh print. Mid `0.05`, bin 0, half-spread bps `4000`, flat, L1 share `1/10`, KL 0. A second row with the same book and the same transaction time is refused as unchanged. |
| `SYN-SPORTS-D2` | sports | Mid `0.25`, bin 2, half-spread bps `400`, flat. YES levels are stored away from the touch. |
| `SYN-SPORTS-D5A` | sports | Mid `0.50`, bin 5, half-spread bps `200`, flat. |
| `SYN-SPORTS-D5B` | sports | Mid `0.50`, bin 5, half-spread bps `400`, flat. Bin 5 median is `300`. |
| `SYN-SPORTS-SHIFT` | sports | Two fresh prints, mids `0.50` and `0.30`, half-spread bps `200` and `400`. Mean mid `0.40`, bin 4, market median bps `300`, flat. |
| `SYN-SPORTS-SHORT` | sports | Mid `0.65`, bin 6, half-spread bps `2000/13`. Three positive levels per side. Ranks 4–10 have depth 0. Positive ranks share `1/3`. Depth sums to the observed size total. |
| `SYN-NON-D1` | non_sports | Mid `0.15`, bin 1, half-spread bps `2000/3`. Level sizes `64,4,4,4,4,4,4,4,4,4` on both ladders. L1 share `16/25`. Top-heavy. |
| `SYN-NON-D7` | non_sports | Mid `0.75`, bin 7, half-spread bps `400/3`. Same top-heavy sizes. |
| `SYN-NON-D9` | non_sports | Mid `0.95`, bin 9, half-spread bps `2000/19`, flat. |
| `SYN-KEEPALIVE` | non_sports | `keepalive` true. Refused. Not a book. |

Nine markets and ten fresh snapshots are included. Two snapshots are refused.
Sports median L1 share is `1/10`. Non-sports median L1 share is `16/25`.
Empty bins stay null.

## Out of scope

Lee-Ready and any other trade-sign inference. Effective spread, realized
spread, and Kyle's lambda. Fee algebra and `completed_profit`. P&L. Live
orders. A live orderbook poll. Retuning Q6 `000`. Queue arms. Capital arms.
Ask depth that is not the observed opposite bid. Padding a missing side with
a zero ladder. Sample-quantile deciles. Writing fixture medians into
`results` or `pnl`.

## What a later result file may say

After the source freeze, a result file may record whether the unit tests
passed and may repeat these limitations. It may not report profit, may not
relabel development games, and may not treat a synthetic median as a Kalshi
stylized fact. `results` and `pnl` stay null.
