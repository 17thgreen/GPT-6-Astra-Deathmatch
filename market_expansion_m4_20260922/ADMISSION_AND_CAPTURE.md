# M4 admission and capture checkpoint, before outcomes

CFB and MLB each pass the eight-event structural and manual identity review.
CFB has no M2/M3 event overlap. It is a historical evaluation from earlier
September, not later chronological validation. MLB milestone times match the
contract's Eastern times; Detroit/Cleveland's Game 1 identity agrees in both.
Both complete cohorts use maker .0175/taker .07: MLB's current series multiplier
is .5, but **all eight reserved events override it to 1**. The series discount
cannot be applied to those events. Historical fee provenance remains unverified.

All seven NHL reservations are explicitly **NHL Preseason** in event product
metadata. They specify full-game wins and 50c settlement for ties. The generic
contract includes regulation/overtime by default; market-specific period/rules
must still be checked. A two-team 50c tie preserves the complementary pair sum,
but the existing strict binary payoff classifier rejects fractional states.
This is an adapter/admission limitation, not a claim that a 50c tie destroys the
pair identity. Fair-price exceptions and cross-market collateral treatment need
separate review. No regular-season NHL profitability claim follows.

NBA live/historical metadata pagination completed and reserved eight May playoff
events by the declared date/ticker rule. All sixteen archived market records have
primary rules but empty secondary rules, including subsequent individual-market
GETs. The current basketball terms have a September 2026 amendment; applying
them retrospectively would not establish May's exceptions. The full fixed NBA
reservation is retained with unresolved rule history; no NBA replay was declared
for this admission stage. No event is silently replaced.

The data collector captured **14/16 CFB markets and 6/16 MLB markets**. Twelve
markets failed after three bounded attempts, returning proxy tunnel HTTP 403
errors. Two CFB markets failed partway through pagination; partial responses and
exact failing requests are retained. A separate public web read of one failed
MLB endpoint was also inaccessible. Neither sport is complete, so all 32 new-
cohort replay slots are blocked. They must not be labeled zero profit or inferred
from the successful subset. Future recovery must retain this failed capture,
complete these exact reservations and freeze a separate continuation checkpoint.

The 48 CFB/WNBA development sizing/completion scenarios remain executable from
the complete frozen M3 data. Eight original-mode size-250 runs are exact control
checks. The original NFL, M2 and M3 implementations remain unchanged.

Primary sources reviewed:
- https://assets.kalshi.com/contract_terms/BASEBALLGAMEWIN.pdf
- https://assets.kalshi.com/contract_terms/HOCKEYWINNINGINPERIOD.pdf
- https://www.cftc.gov/filings/orgrules/rules09152626141.pdf
- https://docs.kalshi.com/getting_started/historical_data

Full-game baseball includes extra innings and official shortened games; game
numbers identify separate doubleheaders, while postponement/cancellation states
require their own handling. This pregame replay models neither lifecycle changes
nor terminal settlement rescues. Exact event records and receipts are in
COHORT_METADATA.json, COHORT.json and metadata/. No actual fills are claimed.
