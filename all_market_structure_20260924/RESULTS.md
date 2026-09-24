# All-market structural research: first measured checkpoint

The discovery and demo connection tests establish usable research access. They do
not establish a profitable strategy or a speed advantage. No orders were placed.
The recovery scan hit its declared 300-second deadline; its partial receipts are
saved. Both processes have ended. No background service is running.

## What was observed

| Measurement | Result |
|---|---:|
| Series catalog | 14,330 series; 18 category labels |
| Perpetual catalog | 25 contracts; 22 active, 3 inactive |
| Incentive sample | 5,000 records / 5,000 distinct markets; all liquidity programs |
| Incentive category coverage | 12 primary categories |
| Completed HTTP receipts retained | 204: 102 HTTP 200, 102 HTTP 403 |
| Successful production book observations | 20, across 8 event contracts |
| Latest observed book states | 5 two-sided, 1 one-sided, 2 empty |
| Demo WebSocket | Connected; 2 subscription acknowledgements; 3 snapshots |
| Demo delta/trade messages during 30-second observation | 0 / 0 |
| Focused unit tests | 7 core + 2 message-redaction tests passed |

Series may have multiple category memberships; counts are not counts of currently
tradeable markets. Incentives were deliberately capped at five pages and still had
a continuation cursor. All sampled program periods contained their page's recorded
receipt time; this does not establish current availability or account eligibility.
The category join uses each market ticker's series prefix and series primary category.

The incentive sample contained 1,478 Entertainment, 1,411 Economics, 923 Financials,
259 Politics, 223 Science and Technology, 168 Elections, 161 Climate and Weather,
159 Sports, 137 Mentions, 54 Companies, 16 Crypto and 11 Commodities programs.
These are observations of a bounded page sample, not market-wide proportions.
Absence from this sample is not evidence of no incentives. The sample cannot answer
whether margin maker/taker programs exist elsewhere in the listing.

The recommended production host returned 403 on the completed attempts; the
documented legacy production host returned 200. This is host-specific access evidence
from this environment, not a diagnosis of a Kalshi outage. RTT includes research-host
network overhead and is not exchange order-entry latency or a competitive speed rank.

## What changes our research choices

**The all-market scope is justified.** Incentivized liquidity is visibly spread
across market families. Incentives can be used to build a candidate universe and
test quote replenishment. They are not themselves a taker edge or guaranteed income.

**Displayed price without size is insufficient.** The latest retained AI-mention
book offered a 2-cent YES ask with only 0.99 contracts at that price. The same scan
found thousands of contracts at some political best prices. Any profitability model
that applies a best price to arbitrary order size would misstate opportunity size.
These asynchronous examples illustrate depth variation; they do not rank strategies.

**The lexical catalog sampler is inadequate for economic selection.** Many early
series are archival and return no open markets. Only eight event books were reached
before the deadline, and perps books were not reached. The next screen should begin
with open contracts and active program periods, then group by exact settlement
relationships. Preserve this initial failure rather than calling it an all-market
liquidity census. Market-list responses also had their own cursors; 1,027 unique
returned open-market records are a partial union, not an exhaustive active universe.

**Faster taking remains an open hypothesis.** Prioritize measurable mechanisms:
nested-payoff inconsistencies, delayed official-release interpretation, external
reference propagation and incentive-linked replenishment. No production stream,
independent information feed comparison, attainable order delay, or executable
net-profit result exists in this checkpoint. A broad search is warranted; there is
not yet evidence to purchase speed infrastructure or declare a winning bot.

## Demo test limits

The explicitly supplied demo credential authenticated successfully. This run
connected to the recommended demo WebSocket and subscribed to orderbook_delta and
trade for three mechanically selected demo contracts. No trading endpoints were
called. Credentials and authentication headers are absent from the artifacts.

The retained snapshot messages have no depth fields. The probe uses an allowlist
for public market fields, so these files cannot distinguish omitted empty-book
fields from an unrecognized schema. Do not claim the books were empty. Snapshot
receipt is proven; depth reconstruction, delta handling and trade receipt are not.
No messages in this short sample validates neither stability nor inactivity across
the demo environment. Demo results cannot substitute for production fill competition.

## Reproducibility and next step

The original frozen source remains unchanged. Recovery protocol and source were
published before its observations in commit `120288d6707fa87cff2d8eb91fb98ef452bcb646`.
The original process lost its unsaved capture; its console counts are not used as
raw evidence. Recovery checkpoints now retain every completed request batch.
In-flight requests at termination have no receipts and are not counted as successes.

`recovery/ANALYSIS.json` contains the descriptive measurements;
`recovery/public_book_receipts.json` contains compact public book evidence;
`recovery/demo_messages.jsonl` contains sanitized demo market-data messages.
The full compressed evidence package preserves catalogs, request receipts, source,
tests, source hashes and failure status. See `ARCHIVE.json` for its checksum.

Run `python recovery/analyze.py` from this directory to regenerate the descriptive
analysis after restoring the archive. `recovery/NEXT_STUDY.md` describes the next
research queue. Production-stream research needs separately provisioned production
credentials. That is a data-access requirement, not authorization to trade.
