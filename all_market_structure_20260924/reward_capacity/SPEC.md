# AMS-012: fixed $2.50 quote capacity and $5,000 sensitivity

User question: how many $2.50 orders can coexist, how many fail, what rewards,
percentage return and time span could a hypothetical $5,000 deployment produce?

This is a descriptive reanalysis of previously examined development books, not
an independent test. The earlier illustrative $2.50 case (2am Miami T79.99 YES,
AMS-010 cycle 7, reward $3.71, principal $2.50, fee reserve $0.25) is already known.
Do not select a different illustration after this analysis. No new network capture,
account action, orders, observed losses or calibrated probabilities are involved.

1. Reuse AMS-011 input readers and scoring with a fixed 250-contract quote at
   one cent, regardless of target size. Keep every other admission and stress rule.
   Include both supported-level and gap-completion states; report separately.
2. Count observations versus distinct program/side cases. For concurrent capacity,
   use only cases in the exact same public-book response timestamp and source/cycle.
   Report scan-cycle totals separately if responses differ; do not imply an atomic
   venue-wide census. Never sum successive snapshots or historical hourly programs.
   One chosen side per market/program avoids presenting alternatives as a portfolio.
3. Inspect subsequent observed states of passing program/sides: positive cushion,
   nonpositive cushion, no baseline qualifying quote, missing capture or program
   end. A later screen failure is not an execution, loss or estimated failure rate.
4. Report conditional reward, principal, chosen fee reserve, net cushion and ROI
   on quote capital and capital plus fee reserve. Preserve $1 minimum and rounding.
   Derive illustrative constant-score qualifying time to cover principal+reserve.
5. Extrapolate the declared $3.71 illustration to 2,000 distinct equivalent pools:
   $5,000 quote capital plus $500 fee reserve. Also report a strict all-in $5,000
   budget using floor(5000/2.75)=1,818 quotes. These are capacity counterfactuals.
6. Failure sensitivity uses fixed failed fractions 0%,10%,20%,25%,30%,50%,100%.
   In a failed scenario the affected quote loses all principal, earns zero rewards,
   and consumes its fee reserve. Other quotes receive the conditional $3.71 and
   also lose all principal and consume their reserve. This deliberately severe
   accounting is a sensitivity, not an execution simulation or loss forecast.
   Show the algebraic zero-profit failure fraction, with no independence assumption.
7. State that filled capital may stay tied up until exit/settlement; reward period
   completion is not a measured cash-availability date. Do not compound or annualize.

Freeze source and focused financial/counting tests before running the aggregation.
Keep older experiments unchanged. Store new source/results in this sibling and
publish to the authorized research branch with dependency hashes and restoration
pointers to the existing capture archives.
