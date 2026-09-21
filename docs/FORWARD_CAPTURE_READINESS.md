# Forward capture readiness after continuity recovery

This is a deployment/admission plan, not a claim that a service is running.
The existing GET-only recorder and Docker configuration are in
`nfl_timing_lab_20260921`. Its SQLite state, cursor exhaustion, first receipt
timestamps, restart gaps and writer locking are implemented and previously
tested. It has no order-entry capability.

The current development panel is explicitly not a holdout panel. The recorder
rejects `purpose: holdout`; changing that label alone is not a valid admission
procedure. A future collection version must distinguish raw public capture
from subsequent eligibility for a frozen evaluation and preserve the original
development database. Do not silently amend a frozen panel or code version.

Pending concrete work:

1. Select a persistent host and durable disk. No such host or deployment access
   was established in the recovered chat/workspace. A transient chat process
   cannot establish uninterrupted seven-day coverage.
2. Resolve venue event/team IDs and scheduled kickoff for the reserved schedule
   using metadata only. Verify payoff equivalence, cancellation/tie rules,
   price grid and the applicable netting treatment. Keep unknown IDs unavailable.
3. Freeze the selected candidate, named controls, capture code, configuration,
   panel and admission record before each required full window. Preserve the
   distinction between schedule reservation and actual admission.
4. Deploy GET-only capture with persistent SQLite storage and a restart policy;
   verify real receipts, exhausted trade pagination, database integrity, clock
   behavior and restart-gap records. A committed Compose file is insufficient.
5. Monitor coverage and storage. Lock coverage adjudication before examining
   P&L. Use the same received stream and shared-capital assumptions for every
   alternative policy; queue position and cancellation allocation remain
   uncertain in public REST data.

The carried-forward first T−7d window starts 2026-09-22T00:15Z. If admission or
capture is incomplete, label it incomplete. Do not reconstruct missing books,
backdate a candidate freeze or replace an unfavorable game. A new complete
cohort requires a new schedule-only declaration before its windows/outcomes.

Live trading, funded wallets and financial risk changes are outside the
approved Q7 research experiment. The separate multi-wallet experiment remains
unimplemented and must use one shared queue/volume model when resumed.
