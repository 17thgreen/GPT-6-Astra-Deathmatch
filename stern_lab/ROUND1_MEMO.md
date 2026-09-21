# Adapting Stern for the Kalshi sports lab

**Prepared for Logan — 21 September 2026**

**Finding:** There is a better research direction than another volatility sweep. Keep Stern's interpretable
score-and-time structure, condition it on football state, then test whether its predicted *change* in odds
adds value to a market price observed before new information arrives. I implemented the first part and
tested it on 570 NFL games. It improved both forecasting scores in both evaluation seasons. The market
update layer is implemented as a research primitive, but its trading value remains untested.

This is an engineering adaptation and an empirical result, not a claim of a new mathematical discovery or
a profitable bot. Possession-aware sports prediction and market-implied volatility have substantial prior art.

## What I reviewed and reproduced

Repository: [Claude-SportsBetting-Competition-to-the-Death](https://github.com/17thgreen/Claude-SportsBetting-Competition-to-the-Death),
branch `claude/kind-hamilton-gdfr9q`, commit `b31fe30d0019263ff9af706a62430d31c9b961ef`.
The review focused on the strategy board, executive/research briefs, Stern scripts, matchup-filter and FLB
scripts, data provider, fee model, and committed experiment outputs. This was not a full application audit.
Terminal cloning lacked credentials; connected GitHub access supplied a commit-pinned source snapshot.
The repository's `.gitignore` excludes raw caches. Its multi-million-row exchange tape was not available
in the repository. No remote files were changed.

I independently reproduced the arithmetic of the committed 196-game Stern ledger:

| Measure | Reported ledger | After one verified tie correction |
|---|---:|---:|
| Games | 196 | 196 |
| Hypothetical one-contract entries | 1,340,105 | 1,340,105 |
| Dollar-weighted return on total entry cost | +9.332% | +9.736% |
| Equal-weighted mean game ROI | −8.135% | −7.948% |
| Median game ROI | −6.177% | −5.713% |
| Profitable games | 89 | 89 |
| Top three games / net profit | 60.72% | 58.20% |
| Game-bootstrap 95% interval for mean game ROI | [−15.849%, −0.168%] | [−15.668%, +0.060%] |

These are simulated ledger statistics, not attainable returns. Both weightings answer legitimate but
different questions. Neither is intrinsically the only honest estimator. The deployment policy must fix
how much capital and how many decisions each game receives, then evaluate that exact policy with clustered
uncertainty. Millions of prints do not supply millions of independent game outcomes.

### One confirmed settlement error

The game `2025_04_GB_DAL` ended tied. The public Kalshi historical market record for
`KXNFLGAME-25SEP28GBDAL-DAL` reports `result = scalar` and `settlement_value_dollars = 0.5000`; its rules
specify 50/50 for both teams in a tie. The response is preserved in `results/tied_market_source.json`.
The script's boolean expression `(final_margin > 0) == pays_home` treats a tie as an away-team victory.
That is incorrect for this contract.

The committed game row has 15,187 one-contract entries and total cost $7,823.27. Its correct gross payout
is therefore $7,593.50 and P&L is −$229.77, rather than −$3,096.27. The $2,866.50 adjustment can be made
from the aggregated ledger without inventing missing fills. It changes the interval's upper endpoint
from negative to slightly positive. **The old claim that this particular interval excludes zero on the
negative side does not survive the correction. The positive-edge admission criteria still fail.**

This is one verified correction, not a full tape replay. Actual settlement values must also handle other
scalar resolutions, cancellations and contract-specific rules. [Kalshi historical-market API](https://docs.kalshi.com/api-reference/historical/get-historical-market).

An earlier suspicion about final-score extraction was withdrawn: my first audit mishandled mixed
timestamp strings. Executing the repository's own `format="ISO8601"` parser matched the official final
margins in all 315 checked 2025–2026 games, and all 570 checked 2023–2024 games. That suspected bug is not
an admitted finding. The separate tie-to-payoff error above is independently verified.

## Why the current modernization is too narrow

The code in `run_inplay_stern_modern.py` changes sigma while retaining the same three game inputs: score
margin, pregame spread and time remaining. Possession, field position, down, yards to go and timeouts are
absent. Increasing uncertainty cannot recover information that was never supplied to the model.

Several interpretations also need tightening:

* Lower log loss is better probabilistic scoring; it is not, by itself, proof of better calibration in
  every state or better conditional returns on a selected trading subset.
* Fitting sigma to a single observed market probability and then repricing that same probability is
  circular. A discrepancy may be model error, stale data, execution cost, omitted information or market
  mispricing. Inversion alone cannot distinguish these explanations.
* One moneyline identifies a standardized location, not an independent mean and variance. If the numerator
  is zero, a 50% quote identifies no sigma at all. Near this point the inversion is unstable.
* The modern script scores millions of taker prints equally when fitting sigma. Busy games/states dominate
  the forecast objective, while its final criterion weights games equally. Those are different populations.
* The committed basic diagnostic covers 196 games; the modernized result covers 219 training plus 17 test
  games. They are not a frozen common cohort. Freeze game IDs, coverage and file hashes for model comparisons.
* The 2026 sample has already been examined repeatedly. Calling it a fresh untouched test for each new
  variant overstates independence. Preserve prior failures and require new forward evidence for promotion.
* The literature brief's universal claim that the old model always overvalues leaders is stronger than the
  evidence established here. A fitted model can be overconfident in one regime and underconfident in another.
  Its assertion that a different trade is the literature's proven cleaner edge should remain a hypothesis.

The original model is useful as a baseline. Stern's 1994 paper derives a probit relationship from a Brownian
score differential and explicitly discusses adding team strength and possession. Its empirical main case
was basketball, not a modern NFL order book. [Stern 1994](https://www.stat.berkeley.edu/~aldous/157/Papers/stern.pdf).
Polson and Stern later examined market-implied game volatility; simply doing that inversion is not a new
innovation. [Polson and Stern 2015](https://escholarship.org/uc/item/8fq0v7hb).

## The implemented adaptation

Let D be the current home lead, mu the expected pregame home margin and r the fraction of regulation left.
The baseline is:

\[
p_0=\Phi\left(\frac{D+\mu r}{13.7\sqrt r}\right).
\]

The prototype learns:

\[
p_{state}=\Phi\left(\frac{aD+b\mu r+\beta^\top h(S,r)}{13.7\sqrt r}\right).
\]

Here h contains possession, field progress and its square, down indicators, yards to go, late possession,
and late timeout difference. a and b are nonnegative. A small fixed penalty shrinks the model toward the
baseline. There is no test-driven feature sweep. This is a conditional probit adaptation; it is not yet
a fully specified stochastic process for entire game paths.

The fit gives approximately a = 0.735 and b = 1.270. These are learned predictive coefficients, not causal
estimates or universal football constants. Timeout contribution was tiny and had a negative fitted sign;
that is no basis for concluding that keeping timeouts hurts a team.

For a hypothetical tied game with six minutes remaining, evenly matched teams, two timeouts each and
home possession, the fitted prototype gives:

| State | Original Stern | State-conditioned prototype |
|---|---:|---:|
| First-and-goal from the opponent's 5 | 50.0% | 75.7% |
| First-and-10 from its own 5 | 50.0% | 53.9% |

These are illustrative model outputs, not validated probabilities for a particular live situation. They
show the missing distinction the original model cannot express. Modern NFL probability models also use
game-state information; this is a necessary baseline improvement rather than exclusive intellectual
property. [nflfastR model documentation](https://opensourcefootball.com/posts/2020-09-28-nflfastr-ep-wp-and-cp-models/).

### What the historical test actually found

The written protocol preceded model fitting. Training used 2019–2022: **1,100 non-tied games and 60,999
snapshots**. The frozen fit was then evaluated on **285 games in 2023 and 285 in 2024**. Each game received
equal weight; sampling used the first eligible pre-play scrimmage state per elapsed minute. Fields were
restricted to regulation with 3 to 58.2 minutes remaining. Final scores were labels only.

| Evaluation season | Original log loss | Scale-only log loss | State-model log loss | Original Brier | State-model Brier |
|---|---:|---:|---:|---:|---:|
| 2023 | 0.48521 | 0.48049 | **0.47103** | 0.15949 | **0.15650** |
| 2024 | 0.45032 | 0.45561 | **0.44058** | 0.15035 | **0.14523** |

Lower is better. Log loss improves **2.92% and 2.16%** relative to frozen Stern; Brier improves **1.87% and
3.41%**. The scale-only benchmark was fit on the same training games and implied sigma = 17.18. Its 2024
scores worsened, while the state-conditioned model improved. This is evidence for testing richer state,
not evidence that any particular sigma is permanently right or wrong.

The uncertainty is material. Paired game-bootstrap intervals for the log-loss change against Stern are
[−0.02883, −0.00088] in 2023 and [−0.01954, −0.00001] in 2024. Paired **week-cluster** intervals are
[−0.02962, +0.00039] and [−0.01962, +0.00005], respectively, and cross zero. Against the fitted scale-only
benchmark, the state model's 2024 improvement excludes zero by both resampling methods; the 2023
improvement does not. These intervals condition on the one trained fit and do not incorporate model-search
history, training uncertainty or regime change.

This is a promising historical forecasting result, not a decisive statistical victory. It also has these
limits: no market benchmark on synchronized quotes, no live availability timestamps, untimestamped closing
spread as a pregame strength proxy, no tied games, no overtime states, no final-three-minute model, and
public data that may have been revised after games. The wider project has previously examined these NFL
seasons for other purposes, so they are not a globally untouched project holdout.

## The prediction-market adaptation worth testing

Use the model to estimate **how a new play changes the odds**, anchored to what the market already knew.

Let q_prev be a synchronized market reference captured before a play. Let p_prev and p_now be the model's
probabilities immediately before and after that same play, using states available when the bot received
them. Define:

\[
\Delta\ell=\operatorname{logit}(p_{now})-\operatorname{logit}(p_{prev}),
\qquad
p_{candidate}=\operatorname{logistic}\left(\operatorname{logit}(q_{prev})+\lambda\Delta\ell\right).
\]

The previous market price carries information about injuries, lineup quality and the matchup. The model
supplies the event update. In odds terms this multiplies the anchor odds by the model's odds ratio raised
to lambda. If there is no state change, the estimate remains at the anchor; if lambda is zero, the model
contributes nothing. For an illustrative move from model 70% to 80%, starting from market 60%, lambda = 1
produces 72%. The unchanged model-versus-market level discrepancy is not repeatedly treated as new alpha.

This transport assumes the model's relative odds update is useful under the market's prior. That can fail.
It is not automatically a valid likelihood ratio for every state representation. Fit lambda on earlier
data, including a lambda=0 ablation, then freeze it. The implemented function uses lambda=1 only as a
transparent research default; no empirical reliability parameter has been learned.

At order arrival, compare the candidate expected payout to the *current executable ask*, not the previous
market reference, last trade or midpoint. Require:

\[
\text{expected payout}-\text{ask}-\text{fee per contract}
-\text{uncertainty buffer}-\text{latency buffer}>0.
\]

For a NO purchase, compute the correct complementary payoff under the contract's rules, and use its own
ask/depth. Build asks from the opposite bids when using Kalshi's bid-only order book. Quoting an attractive
price is not evidence of a reachable fill. [Kalshi order-book documentation](https://docs.kalshi.com/getting_started/orderbook_responses).

The candidate should be tested at measured source/feed/compute/order-arrival delays. Historical print
replay is a diagnostic of price differences; another trader having paid a price does not establish that
our order could have reached it. Record source event time, receive time, state version, reference quote
time, order-book sequence, decision time and assumed arrival time separately. Bound exposure per game;
winner, spread and total positions on that game belong in one joint loss calculation.

The fee input must be versioned by date, series and role, including rounding and exceptions. Do not apply
today's schedule retroactively to 2025 by assumption. The current official document has formula/table
rounding language that should be reconciled with actual charged fees before execution accounting is
promoted. The prototype therefore accepts total fees explicitly. [Official fee schedule](https://kalshi.com/docs/kalshi-fee-schedule.pdf).

## The longer-term stochastic model

For NFL endgames, discrete scoring and possession transitions should eventually replace the diffusion
approximation. A practical extension is a state-dependent drive-transition kernel over points, elapsed
clock, next possession and next field position. Recurse until regulation ends, then apply a rule-versioned
overtime kernel. This creates actual mass at football score differences and tied regulation outcomes.
Price each contract by integrating its exact payoff over the resulting terminal distribution.

The Brownian model is the inexpensive many-drive approximation and a regularization prior where data are
sparse. It should not force a continuous approximation into states with one meaningful possession left.
This transition engine is a proposed next stage, not implemented or tested in this package. The current
prototype explicitly rejects the final-three-minute and overtime domains.

There is also a mathematical correction to the current time-varying-sigma experiment. If instantaneous
volatility is sigma(u)=s0(1+k*u), remaining variance must be its squared integral:

\[
V(r)=s_0^2\left((1+k)^2r-(1+k)kr^2+\frac{k^2r^3}{3}\right).
\]

The repository instead uses s0²*r*[1+k*(1-r)]². That can be a phenomenological residual-scale formula, but
it is not the variance integral of the stated deterministic diffusion. For k=.6 or 1, its derivative in
r becomes negative within the tested range, which a nonnegative deterministic variance integral cannot
do. `remaining_diffusion_variance` implements the integral and is checked against numerical integration.
It was not fitted or included in the forecasting results above.

## Concrete next experiment for Claude

1. Preserve the old results and add the verified tie correction as a new version. Consume official market
   settlement values; verify scalar results, ties and voids before assigning binary labels.
2. Freeze one data manifest and common coverage cohort. Recreate the original baseline exactly, with
   game-weighted and policy-weighted reports. Keep point-in-time acquisition defects visible.
3. Import the supplied trained model as a challenger. Compare it, original Stern, scale-only Stern and the
   synchronized market reference on the same snapshots. Treat already-viewed 2025/2026 as development.
4. Start recording synchronized state and order books. Select one fixed event-update policy and one
   per-game exposure rule. Freeze the anchor, lambda fitting method, cost assumptions and latency test.
5. Evaluate new forward events with score-based and realized-execution metrics. Compare the anchored
   update against both direct state-model trading and the market-only baseline. Report rejected signals
   and missed fills. Abstain if the edge disappears at measured latency or no calibrated uncertainty
   estimate is available.

The immediate deliverable is a tested probability-model improvement plus an explicit exchange hypothesis.
The next admission gate is whether information still remains in that hypothesis **after the market has
updated and after the bot's actual costs and delay**.
