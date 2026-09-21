# Queue access, profit and expansion — 2026-09-21

Active mandate: improve the strategy and build market portability. The user owns
forward validation. Research progress does not wait for a recorder or a fresh
cohort. This document makes engineering priorities, not non-NFL profit claims.

## Increase useful queue access

1. **Choose an actual profitable pair, not two individually attractive legs.**
   Q7 can reject independently selected legs while an alternate pair is viable.
   Q8 tests recovery-only and full joint selection with exactly the same queues.
   Score the pair's bottleneck service, preserve valuable same-price incumbents,
   and pay both fees in the margin check. Full results are in the Q8 report.
2. **Preserve accumulated priority.** Keep valid same-price orders. Refreshing
   an unchanged price is not an access improvement. The inherited queue score
   already uses remaining incumbent queue; Q8 requires a 25% score improvement
   to replace a valid incumbent pair. Pending cancellation remains reserved.
3. **Find more independent queues.** Equivalent outcome routes within an event,
   more games and new compatible sports create places to earn spreads without
   assuming the same queue gets shorter. All positions still share one cash
   account; simultaneous strategies must consume one tape jointly. Do not add
   their standalone P&Ls or allocate $5000 separately and call it diversification.
4. **Know depth versus queue position.** The public book reports aggregate depth.
   The authenticated queue endpoint reports contracts ahead under price-time
   priority. Queue position is useful production input, not something historical
   candle data can manufacture. This is an interface requirement, not a request
   to postpone research. REST and FIX amendment documentation inspected here
   did not explicitly establish which amendments retain priority; no new credit
   for amendments or unseen cancellations is assumed.
5. **Do not buy access blindly.** One-cent improved offsets already disappointed
   in Q1; aggressive completion and smaller early orders also have negative prior
   findings. Any future price-step test must pay its smaller spread and fees and
   consume only eligible tape. Subpenny support is a venue capability, not proof
   this series permits a subpenny quote: sampled sports books use one-cent ticks.

Source: [queue position](https://docs.kalshi.com/api-reference/orders/get-order-queue-position),
[book structure](https://docs.kalshi.com/getting_started/orderbook_responses),
and the timestamped series/event/market responses in SERIES_SNAPSHOT.json.

## Increase completed profit

The working objective is completed net dollars per unit of scarce cash and
inventory time. More fills alone can mean more losses or expensive taker exits.

- Preserve Q7's chosen-pair cost gate, including fees and rounding allowance.
- Test route selection before changing size or cash limits. Q8 isolates that.
- Reduce one-sided inventory cost through better *paired* service, then test a
  cost-aware offset rule separately if diagnostics support it. Do not reintroduce
  Q2's unconditional completion merely because it reduces inventory hours.
- Use actual series/event fee rules. At price .50 and multiplier one, the inherited
  nominal maker fee is .4375 cents per contract per leg; two legs consume .875
  cents before rounding. A one-cent gross pair spread leaves little room. These
  are arithmetic examples, not the average realized edge. No rebates included.
- Expand the opportunity set before assuming leverage or larger caps fix return.
  The prior cap-500 run left inventory unresolved. Keep the hard caps unchanged.
- Keep latency in proportion: Q7's .25s versus 5s completed net differs by only
  $0.44 at queue 3300 and $11.37 at queue 10000. Queue access and pair selection
  are higher-priority research levers in these data; this is not a universal
  statement about live speed or fast in-play markets.
- Study capital allocation only after market-specific opportunities exist.
  Q6 optional ranking and cash earmarking did not explain its improvement.
  A new cross-sport study must use nonoverlapping opportunities, consistent fees,
  correlation-aware event limits and one shared account.

Source: [current fee schedule](https://kalshi.com/docs/kalshi-fee-schedule.pdf),
Q1–Q7 frozen reports. API snapshots reported quadratic_with_maker_fees and
multiplier 1 for all twelve queried series, including series with no sample.
Event overrides must still be resolved; absence of an override is not a future
fee guarantee. This snapshot does not alter frozen NFL fees.

## Portability ranking

“As is” applies to the fee-aware complementary-pair pricing and queue-preserving
router. No entire NFL configuration is certified unchanged for another sport:
its T-7d/T-3h window, final-12h queue assumption, fixed exit depth and schedule
handling are NFL research assumptions, not universal market mechanics.

| Priority | Market | Reusable core | Necessary adaptation |
|---|---|---|---|
| 1 | College football moneyline | Two-winner pair/routing architecture | Series/event mapping, game schedule, liquidity/flow profile, special settlement, explicit fees and windows |
| 2 | NBA and WNBA moneyline | Same pair/routing architecture | Listing-relative windows and daily schedule; news-sensitive flow/staleness profile; event limits and special settlement |
| 3 | MLB and NHL game winners | Same pair/routing architecture for matching final-result contracts | Game identity and period semantics, postponements, start-time changes, baseball doubleheaders; NHL sample has a fractional tie provision |
| 4 | Tennis match winners | Two-winner pricing candidate | Short/unreliable start scheduling, walkover/first-ball and retirement rules, longer postponement handling; separate flow windows |
| 5 | NFL spreads and totals, then other sports | YES/NO making within one exact threshold | Isolate thresholds, replace cross-team payoff map and cross-market netting assumptions, aggregate correlated game exposure; never pair different strikes as complements |
| 6 | Soccer three-way | Same-market YES/NO maker logic only | Full cross-outcome routing requires a three-state inventory/payoff model; opponent NO includes draw and is not own-team YES |
| 7 | Player props, outrights, multi-outcome futures | Binary quote/fee components only | Participation/void rules, correlated positions, sparse queues and longer collateral lockup; not a drop-in full strategy |

This is an engineering-priority ranking inferred from observed contract structure,
not a ranking of measured non-NFL returns. NBA/WNBA, MLB/NHL, NCAAF and ATP/WTA
samples each contain two markets with MECNET. UCL sample contains three with
MECNET: **MECNET alone does not imply a two-direction event**. NFL spread/total
samples contain 25/19 markets with empty collateral-return metadata. The queried
college basketball series returned no sample markets, so it is not classified
as verified portable from this discovery. Discovery uses one event per series,
not an exhaustive inventory or liquidity study.

Representative primary sources (retrieved in SERIES_SNAPSHOT.json):
[NCAAF](https://api.elections.kalshi.com/trade-api/v2/events/KXNCAAFGAME-26OCT04SJSUHAW),
[NBA](https://api.elections.kalshi.com/trade-api/v2/events/KXNBAGAME-26OCT20OKCSAS),
[MLB](https://api.elections.kalshi.com/trade-api/v2/events/KXMLBGAME-26SEP241510AZCOL),
[NHL](https://api.elections.kalshi.com/trade-api/v2/events/KXNHLGAME-26SEP24UTAVGK),
[tennis](https://api.elections.kalshi.com/trade-api/v2/events/KXATPMATCH-26SEP22SVRSEK),
[soccer](https://api.elections.kalshi.com/trade-api/v2/events/KXUCLGAME-26SEP10SLARCL),
[spreads](https://api.elections.kalshi.com/trade-api/v2/events/KXNFLSPREAD-26SEP27HOUIND).

## What is built

`payoff_gate.py` checks exact Decimal payout vectors for equivalence and
complementarity across declared states. It rejects missing/unreviewed state
spaces; tests catch draws and mismatched thresholds. It separately flags
fractional settlements as incompatible with this conservative binary-kernel
admission check, even when a pair still sums to one. That conservative rule also
flags current NFL tie/fair-price exceptions: it is NOT a retroactive claim that
all NFL outcomes are strictly binary, or that prior simulated early flattening
verifies special-settlement behavior. The Q7 replay and its evidence remain as
frozen. A future adapter must model exceptions explicitly.

`ResearchProfile` requires explicit windows, flow horizon, fees, tick, quote age,
cap, exit depth and collateral model with no inherited NFL defaults. It is a
validated configuration schema, not an implemented non-NFL replay or live broker.
There is no automatic natural-language rules parser. A reviewed complete state
space and venue collateral semantics are still inputs, not results of algebra.

`inspect_series.py` is a GET-only discovery utility. The committed snapshot
records source URLs, timestamps, rules, fee type and sampled market structures.
Eight targeted portability tests pass. No non-NFL P&L has been simulated here.

## Next bounded builds

1. Follow the frozen Q8 screen; preserve a failure instead of tuning it away.
2. Build a listing-relative pregame adapter for NCAAF and basketball first,
   including actual schedule and exceptional-state handling. Use separately
   declared historical cohorts and one shared account for combined comparisons.
3. Add exact-threshold spread/total portfolios with game-level correlated exposure
   and no assumed cross-threshold netting. This is a separate experiment family.
4. Investigate authenticated queue-position ingestion and documented order
   amendment behavior as execution plumbing. User-owned forward validation does
   not block steps 1–3. No live order submission is included in these builds.
