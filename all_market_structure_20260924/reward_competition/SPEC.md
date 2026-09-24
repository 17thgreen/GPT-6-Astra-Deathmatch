# AMS-009: short-window reward quote economics

Continue only the short-window liquidity-reward mechanism. Test whether completing
missing target depth still has meaningful conditional economics after competition,
qualification buffers, and the clock are included. Include both one-sided and
two-sided depth gaps; inserting on both sides is modelled only when both genuine
orders would rest. No orders or credentials.

Before new data: capture three active-program catalogs and selected books/metadata
at 45-second start intervals, with a 240-second acquisition budget. Admit current,
unpaid, positive programs lasting at most two hours, with ideal half-pool hourly
rate divided by target*0.01 at least 1. Select up to 300 unique markets by descending
rate/principal, then ticker and program ID, before book acquisition. Re-select
from the catalog each cycle; report caps, missing responses and term changes.
All categories are eligible. Four concurrent public GETs, 12-second timeout,
no retries; at most two catalog pages. Retain raw bytes and receipt timestamps.

For linear-cent books only, propose one-cent bids on each side below target,
for target minus existing depth. Require the proposals to rest against every
existing opposite bid and each other. Do not propose on a side already at target.
Evaluate exact completion and 10%-of-target additional inventory buffer per
proposed side. Principal means one unreplenished order set, not a replenishing bot.

Implement the published one-fifth-target reference and distance discount. Because
the help page does not fully specify treatment of a boundary order or same-price
queues, report two allocation conventions: cap eligible quantity at target with
all incumbent/competing orders ahead of ours; and include the entire boundary
order. Neither convention is represented as verified account scoring. Normalize
each qualifying side independently, and divide combined own share by two.

Apply fixed same-side competitor scenarios independently on every proposed side:
none; 1, 100, 200, 500, or 1000 contracts at one cent; 200 contracts at two cents;
and 200 contracts at the highest cent price still resting against the opposite
book and our proposed opposite order. Omit a scenario when its price would cross.
Keep quantities fixed, report quantity/target ratios and competitor principal.
This is sensitivity analysis, not a forecast of competitors' behavior.

Report conditional remaining rewards for 100%, 50%, and 25% future qualifying
uptime, and full-principal-loss break-even minutes. Gross rewards are not P&L.
Also report a fee stress reserve of $1 per 1000 proposed contracts, explicitly a
chosen stress rather than a verified venue fee. Do not infer fills from public
prints or depth disappearance. A full immediate losing fill remains possible.

Aggregate distinct reward pools only; label series and event concentration.
Use first-cycle candidate qualification as the development shortlist and the
next two cycles as brief repeated snapshots, not an independent profitability
holdout. Preserve every failed response and nonpassing candidate.

Primary scoring source (retrieved before freeze):
https://help.kalshi.com/en/articles/13823851-liquidity-incentive-program
Interpretation is not account-level validation. No guaranteed income, extrapolated
daily return, assumed replenishment, or background service claim.
