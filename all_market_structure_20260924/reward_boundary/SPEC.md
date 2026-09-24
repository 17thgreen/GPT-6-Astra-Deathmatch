# AMS-011: qualifying price-level sizing within the same reward strategy

Source update: the July 15, 2026 Kalshi filing, effective July 30, has clean terms
on PDF pages 7–10. Page 8 includes the entire price level where cumulative size
reaches target. The existing AMS-009 whole_level function implements that rule;
its capped function is now an additional stress, not an equally supported reading.
Frozen AMS-009 and AMS-010 results remain unchanged.

https://www.cftc.gov/filings/orgrules/rules07152610358.pdf

Hypothesis: qualifying one-cent levels already supported by other traders may
allow smaller genuine resting orders to earn useful rewards. Public depth is not
a measured individual queue position. We will not assert actual fill protection.

Before calculation: apply whole-level scoring to every eligible short-window
program in the retained AMS-005 full census, AMS-007 snapshots, AMS-009 snapshots,
and the already scheduled AMS-010 capture after that capture finishes. No fresh
network selection, no unrelated strategy, and no changing AMS-010 admission.
The old samples are reused development data. The AMS-010 overlay was specified
after that capture began and is exploratory, not its preregistered primary result.

For each side independently, test target fractions .05, .10, .25, .50, 1.00 and
1.10 at one cent. Require a noncrossing cent-grid book and sufficient opposite
depth. Ignore optional max_reward_per_account programs pending interpretation.
Insert only one candidate order per case; scenarios are alternatives, not an
additive portfolio. Require both sides to meet target after insertion.

Compute whole-level own share, conditional remaining reward at 50% qualification,
cent rounding/$1 minimum, principal, and the same $1/1000-contract fee reserve.
Repeat after removing the best public opposite level and adding one-fifth-target
rival depth on our side at two cents if it rests, otherwise one cent. Preserve
zero-qualification cases. A positive worst-of-base-and-stress cushion is a model
screen, never profit. This specification does not assume fills or paid credits.

For supported-level cases, require own-side public depth already >= target and
positive baseline own score at one cent. Count them separately from gap-completion
cases. Record existing one-cent depth, better-priced depth, reference, and price
level boundary. Rank quantity alternatives by cushion/principal and report event
concentration. Do not fit the quantity fractions after seeing outcomes.

Test entire-level inclusion and order-ordering invariance, no credit below the
qualifying boundary, reference-price discount, supported/gap classification,
and stressed loss of opposite depth. Freeze code/tests before dataset scoring.
