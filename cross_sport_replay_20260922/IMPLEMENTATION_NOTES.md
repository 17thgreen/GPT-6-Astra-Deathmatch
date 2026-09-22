# M2 implementation freeze — September 22, 2026

Resumes the eight-game cohort committed at d7079b6. No cohort substitutions,
parameter search, observed-profit selection or edits to Q7/Q6 source.

All 16 market captures completed. Normalize validates identities, listing bounds,
raw hashes, all eight reserved events, duplicate IDs, quantities, prices and
pagination before supplying one chronological tape. Quotes use minute-close bid
and ask, received hypothetically 60 seconds later, with Q7's 300-second age cap.
The listing subclass only adds `now >= listed_at` to inherited eligibility.
A synthetic regression with actual fills reproduces Q7 orders and fills exactly
once both markets are listed. Ten focused tests and 152 inherited replay/adapter/
payoff tests pass. This is code verification, not a profit result.

The exact Q7 winddown starts five minutes BEFORE T-3h. The captured tape continues
through T-3h plus five minutes. These are different boundaries; both are retained.
Entries stop before the winddown, with inherited submit/cancel delays reserved.

## Interpretation boundaries

The cohort contains retrospectively retrieved market/rule/milestone metadata.
Normal winner payoffs were reviewed for two opposing teams on the same full game.
All eight saved events have ordinary complementary 0/1 settlement metadata.
These outcomes are neither selection criteria nor policy inputs. No terminal
winner payout is credited: any remaining inventory yields null completed profit.
The venue's fair-price exceptions remain outside this normal-game pilot. There
is no historical lifecycle feed proving the absence of an intervening pause,
reschedule or exceptional state. The replay assumes ordinary pregame operation
at the reconstructed starts; it must not be represented as verified historical
exception handling or historical schedule knowledge. No exception-detection
capability is inferred from today's finalized metadata.

Fees .0175/.07, queue 3300/10000 (1,327,847.005 inside 12 hours), participation .5,
250-contract orders/caps/total exit budget, immediate complementary netting and
one $5000 balance are deliberately standardized NFL transport assumptions.
Actual venue fills, queue positions, charged fees, collateral releases and exit
depth are unobserved. Reconstructed candle quotes are not a full order book.

Each standalone sport gets $5000 as a separate counterfactual; the combined case
gets one $5000 account. Adding the standalone results would represent $10000,
not the combined alternative. This matrix does NOT yet compare a $2500/$2500
fixed split against shared $5000. That is a distinct fleet-allocation experiment.
Separate strategy ledgers and per-sport risk limits are compatible with a shared
allocator, but running multiple bots against one queue does not multiply tape.

## Reproducibility

The bounded raw data total about 1.4 MB, so they are included in Git despite the
repository's default compression-file exclusion. No separate raw-data archive
or restoration dependency is needed for M2. Larger outcome ledgers, if any,
will be sized before deciding whether to include them or index an external kit.

Before replay, commit source, INPUT_AUDIT.json, raw captures and FROZEN_REPLAY.json.
Run `python run_replay.py` once, then `python verify_replay.py`. The latter does
independent per-fill fee, cash, pairing, inventory, order and exit reconciliation.
It does not establish executable historical fills or validate future returns.
