# AMS-009: the opportunity survives, but the entry clock matters

Continue researching short-window missing-depth rewards. The strongest candidates
still have meaningful conditional economics, but filling every empty side at any
point in the reward period would be a poor policy. Entry time, reference-price
competition and the depth behind the best opposite quote are decisive.

## Fresh observations

The 98.27-second acquisition ended after its original three scheduled cycles.
The first catalog request failed with URLError; DNS resolution also failed then.
The next scheduled cycles succeeded without retries: 10 HTTP 200 receipts, 58 then
57 selected programs, 70 distinct programs/tickers across ten series in total.
Neither successful catalog had a cursor or selection cap. There were 100
open/current book observations and 15 outside their open window. The failed
first cycle is unavailable data, not evidence that the venue had no opportunities.

At approximately 04:29:48 and 04:30:29 UTC on September 24, six Miami hourly
temperature markets still permitted a resting 1000-contract one-cent bid that
completed missing depth. Each had a $100 campaign ending at 05:00 UTC. They were
T71.99, T72.99, T73.99, T74.99, T75.99 and T80.99 in KXTEMPMIAH-26SEP2401.
All six passed the no-new-competition, 50%-future-uptime stress at both reads,
including a chosen fee reserve. All six belong to one event; they are not six
independent risk sources. No program terms changed during these two reads.

Other observed depth-completion cases in currencies and crypto either had too
little time remaining or had existing better-priced depth that almost eliminated
the one-cent bid's score. Three first-successful-cycle cases required completing
both sides; none passed the same economic stress. Empty depth alone is insufficient.

## One representative market at the final read

These figures apply to each of the six candidates, before payout rounding and
account eligibility checks. The final read was 04:30:29.302940 UTC. They describe
past, conditional book states, not current availability or earned money.

| Hypothetical condition | Remaining gross reward | At 50% future qualifying time |
|---|---:|---:|
| Sole bidder on missing side, 1000 at one cent | $25.57 | $12.78 |
| 100 additional one-cent rival contracts, rivals allocated first | $23.01 | $11.50 |
| 200 additional one-cent rival contracts, rivals allocated first | $20.45 | $10.23 |
| Best opposite level removed; 200 rival contracts at two cents | $17.04 | $8.52 |

The exact-completion quote has $10 principal. We additionally reserve $1 per
1000 proposed contracts as a deliberately selected fee stress, not a verified
fee rate. Thus the comparison threshold is $11. A 1100-contract buffered quote
has $11 principal plus $1.10 reserve, and can absorb 100 own fills before its
remaining depth falls below target, assuming no other book changes. It does not
increase the sole-side reward share. Automatic replenishment is not assumed.

## A fragile price barrier

At the actual snapshots, the best opposite bid was 98 cents. A two-cent bid on
our proposed side would therefore execute, rather than rest. However, each book
had only 12 contracts at that best opposite price. It is a thin barrier, not a
durable protection against competition.

The last table row is explicitly post-hoc: remove that best opposite price level,
without assigning it a trade or cancellation, then add the original model's
200-contract two-cent competitor. Opposite total depth still exceeds 1000 in all
six books. Under capped allocation, our snapshot share falls from 50% to one third
of the overall reward. The alternative whole-boundary-level convention is more
generous; actual account scoring for boundary orders and same-price ties remains
unverified because public books aggregate orders.

At 50% future qualifying time, this stronger stress requires at least **38.09
minutes remaining** for the $10 exact-completion quote plus $1 reserve, or **41.90
minutes** for the $11 buffered quote plus $1.10 reserve. At the last snapshot only
29.51 minutes remained, so those six quotes fail the stronger entry test. This
supports researching early-window entry, not chasing a displayed reward late.
Those thresholds are model-derived development choices, not optimized or validated
trading parameters. They change with pool, period, target, price and competition.

## Reused evidence and limits

After the connection failure, a retained-data fallback was preregistered. It was
completed even though later scheduled requests recovered. The frozen model was
applied to every eligible retained AMS-005 census book and all twelve AMS-007
frames, explicitly as development data. AMS-005's later-in-window observations
had zero candidates passing the half-uptime-plus-reserve test. AMS-007's earlier
observations had seven such candidates in each of its ten Miami-containing
frames. This comparison changes time and reward period together; it does not
isolate a causal timing effect or prove profitability.

The first fresh cycle failed, so the preregistered first-cycle shortlist/next-two
check could not be completed as specified. The two successful reads are brief
observations; the retained-data replay is not an independent holdout. Neither
establishes continuous qualification between snapshots. Rewards at 50% uptime
require that qualifying exposure actually exists for that time. A full immediate
losing fill could prevent that and lose the quote's principal before rewards
accrue. No fills, credited rewards, account entitlement or profit were verified.

Eight meaningful scoring/admission tests passed before acquisition. Original
source hashes, all used receipt hashes and selection-before-book times verified.
The reference-price test covers the sharp one-fifth-target threshold; other tests
cover price crossing, missing data, target eligibility, allocation ambiguity,
two-sided completion, discount zero and buffer exhaustion. No new tests claim to
verify undocumented exchange behavior.

Spec commit 53f2e35abac8fa678293823f0041d94e014a885e; source freeze
11b8a17ec47b0f9a9a8274099764d27a5abeaf97. The separate REPLAY_SPEC.md records the
fallback's provenance. TOP_LEVEL_STRESS.json is labelled post-hoc throughout.

Scoring source: https://help.kalshi.com/en/articles/13823851-liquidity-incentive-program

Restore AMS-009 raw evidence and the separately retained AMS-005/AMS-007 archives
to reproduce: run `python report.py`, `python top_level_stress.py`, then
`python -c 'import report; report.archive()'`. Original acquisition must not be
rerun into its existing capture directory. No account/order routes or credentials.
No monitoring process remains running.
