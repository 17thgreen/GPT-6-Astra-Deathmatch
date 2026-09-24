# Strategy 1 validation: promising House evidence, no deployment qualification

Research date: September 24, 2026. Studies NH-001 and NH-001A.

**Decision: continue a focused House-race research track. Live trading is not
validated.** An external forecast improved prediction quality on this historical
House sample. A selective fixed hybrid produced positive hypothetical returns.
The Senate replication did not confirm an edge. Executable size, repeatability
across elections and a current probability feed remain unvalidated.

## Strategy and implementation

Primary probability = 50% published specialist forecast + 50% market bid/ask
midpoint. The source is external; its information is not assumed statistically
independent of the market. For each race, compare Democratic YES at the YES ask
with NO at one minus the YES bid. Choose at most one purchase, one contract, and
hold to official settlement. Require probability minus cost to exceed a 3c error
reserve after an illustrative unrounded `0.07*p*(1-p)` taker fee and 2c execution
buffer. Model-only, market-only and a 25%-model hybrid were frozen comparators.

The implemented system recovers archive snapshots, verifies availability and
hashes, maps party/district contracts, rejects unusable quotes, scores forecasts,
accounts for both binary sides, retains exclusions and records current depth.
No weight, threshold or district was selected by this run's return.

This is a **prespecified retrospective analysis**, not a blind historical holdout.
2024 outcomes and the motivating literature were already public. Design and
implementation were committed before this run calculated scores.

## Fixed 50/50 hybrid results

Brier loss measures probability error; lower is better. Dollars below represent
the whole one-contract-per-signal portfolio, not per-contract gains or live P&L.

| Family and decision (UTC) | Races | Market Brier | Hybrid Brier | Relative loss reduction | Signals | Hypothetical net | Modeled outlay |
|---|---:|---:|---:|---:|---:|---:|---:|
| House, Nov 4 2024 22:00 — amended primary | 19 | 0.24176 | 0.21186 | 12.4% | 2 | +$0.885560 | $1.114440 |
| House, Nov 5 2024 16:00 — sensitivity | 23 | 0.23091 | 0.20867 | 9.6% | 3 | +$1.519439 | $1.480561 |
| Senate, Nov 4 2024 22:00 — replication | 12 | 0.08856 | 0.08904 | −0.5% | 0 | $0 | $0 |
| Senate, Nov 5 2024 16:00 — sensitivity | 13 | 0.07524 | 0.07852 | −4.4% | 1 | −$0.385925 | $0.385925 |

**The horizons overlap within one election. Do not add their profits or race
counts or treat the House observations as independent replications.** The primary
House sample spans 12 states and fails the frozen minimum of 20 races. The
23-race sensitivity does not repair that primary admission shortfall.

### Positions behind the House result

| Observation | Fixed purchase | Ask | Hybrid probability of purchased side | Expected net after modeled fee/buffer | Realized hypothetical net |
|---|---|---:|---:|---:|---:|
| Primary | IA-1 Democratic NO | $0.46 | 53.765% | $0.040262 | +$0.502612 |
| Primary | PA-10 Democratic NO | $0.58 | 65.565% | $0.038598 | +$0.382948 |
| Sensitivity | IA-1 Democratic NO | $0.35 | 49.765% | $0.111725 | +$0.614075 |
| Sensitivity | IA-3 Democratic NO | $0.46 | 54.845% | $0.051062 | +$0.502612 |
| Sensitivity | PA-10 Democratic NO | $0.56 | 65.565% | $0.058402 | +$0.402752 |

These positions all backed Republicans and share national political risk. Five
rows represent only three distinct races. The primary expected margins were
about 3.9–4.0c, despite much larger realized gains. Another 3c of expected execution
cost would make both primary signals fail the original 3c reserve gate. Positive
ex-post stress returns do not establish a robust expected advantage.

The selected House contracts settled January 3, 2025, about 60 days after the
primary decision. This test holds until settlement; no liquid election-night
exit or annualized return is assumed.

## Comparisons and robustness

| House comparator | Primary Brier | Primary signals / hypothetical net | Sensitivity Brier | Sensitivity signals / hypothetical net |
|---|---:|---:|---:|---:|
| Market only | 0.24176 | 0 / $0 | 0.23091 | 0 / $0 |
| External model only | 0.18804 | 6 / +$2.577394 | 0.19171 | 8 / +$2.704760 |
| 50% model — primary policy | 0.21186 | 2 / +$0.885560 | 0.20867 | 3 / +$1.519439 |
| 25% model — sensitivity | 0.22605 | 0 / $0 | 0.21913 | 1 / +$0.614075 |

Model-only performed better here. That is a research clue, not permission to
choose its weight after seeing this election and call it validated. Market-only
abstention is expected: a midpoint cannot cover the ask, costs and reserve on its
own. No-trade also earns zero.

The Senate model-only comparator lost $0.454342 at the primary horizon and
$0.091450 at the sensitivity. The latter hybrid bought Ohio Democratic YES and
lost its entire $0.385925 modeled outlay. Preserve this negative replication.

Prespecified checks:

- Another 3c per original House trade leaves primary hypothetical net +$0.825560
  and sensitivity +$1.429439. This reprices fixed trades without reselecting them;
  it does not claim they still satisfy the entry gate at higher expected costs.
- Removing the two best winners leaves primary net **$0** and sensitivity
  +$0.402752. Primary profit has no breadth beyond those two winners.
- The state-bootstrap 95% interval for hybrid-minus-market Brier is primary
  [−0.05334, −0.00405], sensitivity [−0.04745, −0.00084]. These intervals are
  conditional on one election, omit national common-factor risk and do not
  establish cross-election significance or eliminate retrospective selection.
- Leaving out any one state preserves lower House hybrid Brier: primary
  difference range [−0.03577, −0.02131], sensitivity [−0.02675, −0.01125].
- All admitted House midpoints lie in the frozen competitive [10%,90%] range.

## Does the neglected-market explanation fit?

At the primary observation, admitted House markets had median spread 6c and
20 contracts traded in the last available quote bar; Senate medians were 1.5c
and 825 contracts. Five House bars had zero trading volume, versus none for
Senate. These post-score descriptive proxies did not select the trading cohort.
They are not order-book depth or capacity estimates.

This pattern is **consistent with** external forecasts adding information in
less-attended markets. It does not establish a causal mechanism. Market maturity,
participant composition, national forecasting error and sample selection are
alternatives. All mapped House contracts opened October 31, only days before
this test; initial price discovery is a plausible contributor.

A post-score diagnostic removes hour-old observations and keeps only quote bars
ending exactly at decision time. House Brier improvement remains: −0.03970 on
15 primary races and −0.02128 on 21 sensitivity races. Thus the allowed hour-old
quotes do not explain the entire finding. Bar-end prices still do not prove
duration, depth or attainable execution.

## Data admission and failed original gates

We searched 155 currently catalogued individual House/Senate series and retained
every retrieval outcome. They returned 87 2024 market records. The predetermined
Democratic-suffix selector yielded 42 distinct mapped party races: 24 House and
18 Senate. Every primary rule was audited, with exact aliases for PA-7's
“Democrat” wording and Minnesota's Democratic (DFL) wording. Current-catalog
discovery may miss old series no longer catalogued; this is not a proven
exhaustive, survivorship-free exchange universe.

All 168 hourly quote requests succeeded at HTTP level. Missing or unusable
responses remained missing. Deduplication left 252 quote observations. Crossed,
missing-sided and boundary bid-0/ask-1 books were excluded. Volume never became
fabricated depth.

Original House and Senate probability files were captured November 3, 2024 at
20:38:57 and 20:38:55 UTC. We use those exact archive times as conservative public
availability bounds and impose 24 hours' lag. An October 10 House capture was
recovered but is too stale for October 29. Archived HTML display shells were not
probability snapshots, and later-captured time series were not backdated.

The original NH-001 horizons remain in the scorecard with **zero admitted races**:

- October 29 16:00: all 24 House contracts had not opened. Senate had eight
  unopened contracts and ten with no eligible forecast.
- November 4 16:00: all 24 House forecasts failed the 24-hour availability lag;
  Senate had 17 with that failure and one unopened contract.

NH-001A added the feasible Nov 4 22:00 primary and Nov 5 16:00 sensitivity before
scoring. These are disclosed amended horizons. Two party-name alias corrections
were also committed before scoring, without outcome-based selection.

## Execution and operational limits

Historical hourly quotes contain no visible depth. A separately labeled post-score
diagnostic requested the next five minutes of minute bars for all six hybrid
signal observations, including the losing Senate signal. All six requests
succeeded but returned empty arrays. **Delayed-entry and quote-persistence
validation therefore remain unavailable.** Empty arrays neither prove no trading
occurred nor justify assigning zero profit.

Actual historical fees remain unverified. The declared illustrative formula is
unrounded; the extra 1c stress exceeds ordinary per-unit cent-rounding differences
under that formula. Fee schedules, exceptions and waivers remain separate unknowns.
These are hypothetical monetary results throughout.

The forecast targets election victory, while contracts pay on the party of the
member sworn in for the 2025 term. Death, replacement or party change creates
residual basis risk. Actual Kalshi resolutions were used and this mismatch was
retained. It is not rule-identical arbitrage.

The current-depth recorder successfully fetched three alphabetically selected
2026 Democratic House contracts, preserving decimal prices, fractional quantities,
receipt timing, hashes and reciprocal asks. This was a connectivity/schema test,
not a representative liquidity sample. The current series listing returned
707 open contracts, not 707 independent races. Displayed size is not a fill.

No current external probability feed was admitted. The Economist describes a
2026 congressional model publicly, but its House model page could not be retrieved
and admitted here. A 2024 538 probability cannot supply a 2026 signal. Recorder
output says `forecast_admitted: false`, contains no signals and has
`live_trading: false`. No recurring process is running.

## Decision and handoff

| Question | Finding |
|---|---|
| Code checked? | 27 tests; exact reproduction of three result files; eight frozen source hashes; 29 independent decimal ledger checks. |
| Historical House forecast improvement? | Yes, under the stated sample, joins and horizons. |
| Positive primary hybrid cost screen? | Yes, on two races only. |
| Senate replication? | Fails. |
| Frozen primary breadth requirement? | Fails: 19 races against minimum 20. |
| Historical fills, actual net P&L, sustainable capacity? | Unvalidated. |
| Repeatable cash-generating strategy? | Unvalidated. |

Continue with a **prospective specialist House-value screen**, retaining 50/50 as
the primary policy and model-only as a comparator. Admit a current probability
source, freeze exact contract mappings and record depth plus delayed observations.
Measure opportunity disappearance, size, common political risk and capital held
until settlement. The experiment must permit no trades or no advantage. See
[NEXT_EXPERIMENT.md](NEXT_EXPERIMENT.md).

This is presently a small, slow-turnover signal. Scaling its unit profits to a
daily income target has no evidentiary basis.

## Sources and reproduction

- [Exact archived 538 House capture](https://web.archive.org/web/20241103203857id_/https://projects.fivethirtyeight.com/2024-election-forecast/house/states_latest.json).
- [Exact archived 538 Senate capture](https://web.archive.org/web/20241103203855id_/https://projects.fivethirtyeight.com/2024-election-forecast/senate/states_latest.json).
- [Kalshi historical data](https://docs.kalshi.com/getting_started/historical_data); exact retrieval URLs and hashes are in `data/source_receipts.json`.
- [Kalshi reciprocal order-book semantics](https://docs.kalshi.com/getting_started/orderbook_responses).
- [The Economist's 2026 model description](https://theeconomistoffthecharts.substack.com/p/our-prediction-model-for-americas), source discovery only; no probabilities admitted.
- Protocol remote commit `7daf8665bdf9a0a13d64a51e80a39442605aa00f`; amendment `b960d19726f21c20350393d5d90f0cea3811e1f8`; implementation freeze `faa0562f96cae08037715e2a6337fd2b647c1505`; final pre-score mapping freeze `939226c9a038eaf752ad5003f91e323338a50237`.

Run `python3 verify.py` from this directory for exact offline reproduction. The
included compact projection retains all scored observations, omits irrelevant
out-of-panel forecasts and replaces full contract rules with hashes. Projection
changed no score. Receipts index omitted raw bytes; they are not downloads of them.
