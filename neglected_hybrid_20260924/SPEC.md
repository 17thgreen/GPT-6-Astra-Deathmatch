# NH-001: neglected-election hybrid forecasting

Status: preregistered data admission and analysis design, before this study's
outcome scoring. This is retrospective research: 2024 results and the direction
of published Sethi findings are already publicly known. It is not a blind holdout.

## Hypothesis and scope

A contemporaneous external election forecast adds information to the prices of
individual legislative-race contracts. A fixed hybrid improves forecast scores
and may support a selective trading policy after costs. These are two separate
hypotheses. No production trading or risk-limit changes are authorized here.

Primary candidate cohort: all accessible 2024 US House district party-winner
contracts, followed by Senate state party-winner contracts if House lacks a usable
contemporaneous forecast archive. Admission chooses by provenance/coverage only,
never by return. Senate is also a separately reported replication if both exist.
Presidency, chamber control, vote margins and election-night markets are excluded.
Avoid duplicate YES/NO and party representations of the same race. Independent
candidates require an explicit rule and forecast mapping, never a guessed party.

Published 538 forecasts are the first external source, Economist second. If neither
is accessible, preserve the admission failure before considering a separately
specified model or older-cycle reproduction. A new family or model requires an
append-only protocol amendment before scoring its outcomes. Public APIs and free
archives only; no keys, paid subscriptions or live orders.

## Admission

Require exact venue rules and ticker, forecast probability and publication
timestamp (or a conservative date bound), original data provenance, and resolved
outcome. Final/latest retrospectively revised forecasts cannot stand in for
earlier forecasts. Git archives must distinguish the timestamp inside data from
the time the file became public. Data fetched after the event is not automatically
contemporaneous evidence. Log every exclusion and failed retrieval.

For a market comparison require both bid and ask with a usable as-of timestamp.
A trade price alone may support a separately labeled price proxy; it cannot be
silently called a midpoint or executable ask. Historical quote bars without depth
permit a quoted-price cost screen, never a claim of attainable fills or capacity.
No price interpolation across missing periods. Today's volume or final volume
cannot define a historically neglected cohort.

Primary decision: 2024-10-29 16:00 UTC (seven calendar days before election day).
Secondary robustness: 2024-11-04 16:00 UTC. One observation per race per horizon;
do not pool horizons into independent trials. Forecasts must have been available
at least 24 hours before decision. If only dates exist, availability is bounded by
the end of that date in America/New_York, then the 24-hour lag is applied. Select
the latest eligible forecast within 7 days; no post-decision information.
Quote observations must be at/before decision and no older than one hour.

## Frozen comparisons

For Democratic-party probability p_model and midpoint p_market:
- Market-only: p_market.
- Model-only: p_model.
- Primary hybrid: 0.5*p_model + 0.5*p_market.
- Sensitivity only: 0.25*p_model + 0.75*p_market. Never select the better weight
  on this retrospective cohort and call it validation.

Report Brier and log loss (clip only for log loss at 0.001/0.999), per-race paired
differences, counts, spread and missingness. Use a seeded 10,000-resample bootstrap
by state for descriptive intervals conditional on this election. All races share
national election risk: these intervals do not establish cross-cycle significance.
Report leave-one-state-out influence and competitive-race subset defined by
predecision market midpoint [0.10, 0.90]. No final-outcome-based exclusions.

## Trading screen, not assumed execution

One terminal binary purchase per race per arm; hold to official settlement.
Choose the side with the greater forecast-minus-ask margin. Require expected
margin after an illustrative standard taker fee 0.07*p*(1-p), a 2c execution
buffer, and a 3c additional error reserve to exceed zero. Actual historical fees
must be verified before the output can be called historical net P&L. If not,
label all monetary output hypothetical cost-screen results.

One contract per admitted signal for an interpretable unit portfolio; show total
capital and terminal net dollars, not a compounding projection. Compare model,
both hybrids, market-only and no-trade. No maker-fill assumption, leverage,
unlimited duplication or trade-based rebalancing. Market-only can correctly abstain
when its midpoint does not beat the ask and costs. Show additional adverse cost
stresses of 1c and 3c per contract, without reselecting original trades. Also show
P&L excluding the two best winning races, and maximum individual loss share.

## Verdict

Pass code verification only after focused tests for timestamps, leakage,
reciprocity, joins, fees, abstention and cash/settlement accounting.
Historical support requires primary-horizon hybrid Brier improvement and positive
cost-screen results under stated limitations; a result can support one and reject
the other. Fewer than 20 distinct races means insufficient breadth for promotion.
No retrospective result is live validation. A missing data gate produces a named
blocker, not a null score interpreted as a successful strategy.

Do not modify any frozen NFL, fee, reward or other study. Preserve source licenses
and hashes; public availability is not an inferred redistribution license. Commit
specification, implementation freeze, then results at separate checkpoints.
