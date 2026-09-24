# AMS-003: three mechanisms compared

The most useful new lead is a missing-side liquidity incentive, not static
arbitrage. The mathematical volume-fee screen rejects one broad subsidy-only
taker hypothesis. The cross-venue basis screen could not be measured because both
independent spot data sources returned unusable pages. No profitable strategy is
validated; no orders were placed. Research decisions are in DECISIONS.md.

## 1. Public event volume rewards versus ordinary taker fees

For multiplier 1, compare the unrounded fee 0.07*p*(1-p) with the public event
volume-program maximum of $0.005 per eligible contract. Solving the equality gives
p = 0.0774228726 and 0.9225771274. Between these prices, the fee alone exceeds the
maximum reward, even with zero spread, zero slippage and zero adverse movement.

At a 50-cent contract price, the unrounded fee is 1.75 cents per contract and the
maximum reward is 0.5 cents: a 1.25-cent deficit before trading losses. Reward share
can be below the cap. Prices outside the interval are not proven profitable, and
the cited program excludes event contracts below 3 cents or above 97 cents.
This bound does not apply the event fee formula to perpetuals, special fee terms,
zero-fee series, makers, or account-specific rebates.

Decision: do not build a zero-edge middle-price taker strategy whose only supposed
advantage is this public reward. Volume rewards can still improve an independently
profitable trade's economics.

## 2. Liquidity-program screen

From the retained AMS-001 sample, choose the highest pool dollars/hour program
whose listed time window contained selection time in each of 12 categories.
This is intentionally enriched, not representative, and the old sample was capped.
Current program terms and account entitlement were not independently refreshed.

All 12 market metadata and full-book requests succeeded. Eleven met the observed
open-market, listed-window and two-sided target-depth conditions at receipt; one
did not. A single snapshot does not estimate the proportion of qualifying seconds.
The 11 passing programs' total pool rates ranged from roughly $0.77 to $25/hour.
At an assumed 10% score share and full qualifying time, the gross budget would be
about $0.08–$2.50/hour before fees or inventory losses. Share is not observed.

The exception was KXAAAGASDFL-26SEP24-4.4400, with no YES bids and 7,132 NO-side
contracts in the initial full book. The retained schedule listed a $100 pool over
4.15 hours and a 1,000-contract target. Two separately frozen follow-up reads again
found the YES side empty and the other side above target. See DECISIONS.md for the
conditional $10-principal / $7.37-remaining-reward scenario and why it is not a
guarantee. All three observations span about 217 seconds, not continuous coverage.

Mechanism: a missing side may let a small absolute capital commitment supply a
large fraction of qualifying liquidity. The marginal reward depends on the book
after insertion, other participants, period duration and actual eligibility.
Reported large pools are not account income and not necessarily available for
the full advertised interval. Captured depth belongs to other participants.

## 3. Perpetual/spot entry-basis screen

BTC, ETH and SOL were selected before new observations. Three Coinbase rounds
produced nine HTTP 200 HTML Site Unavailable pages, not usable JSON books. One
Kalshi SOL book request failed in transport. The original nine comparisons are
unscored. A predeclared two-round Kraken alternative also produced six HTTP 200
HTML unavailable pages. These six comparisons are unscored too.

The Kalshi perps books were accessible in 14 of 15 attempts. This cannot establish
a cross-venue price difference without independent spot evidence. No third data
provider was attempted. We did not turn a source failure into an economic failure,
or substitute Kalshi's own reference feed as independent confirmation.

Fees for perps are not the binary-event quadratic formula; their notional fees,
closing costs and funding require separate modeling. A positive entry basis alone
would not guarantee convergence or access to the hedge. The fixed test model and
0/5/10/25/50 bps sensitivity are retained for later usable data, but no numerical
basis result is reported from this run.

## Evidence and verification

- 63 HTTP/transport attempts retained: 47 usable Kalshi JSON responses, 15 HTML
  unavailable-page responses from spot sources, one transport failure.
- Eight cost/depth tests passed before acquisition; a ninth test checks that HTTP
  200 HTML is rejected by the analysis reader.
- Original freeze commit: `694fc2b64c31270a95ff7072a1df81fb522222bd`.
- Follow-up freeze: `c8a4523e98aa4f83f80932d4b705746a46daf611`.
- `RESULTS.json` and `FOLLOWUP_RESULTS.json` preserve numerical scenarios and
  unscored cases. `AMS_003_Evidence.zip` includes source, tests, raw receipts,
  hashes, freezes and decisions. `ARCHIVE.json` gives its checksum.
- Reproduce with `python analyze.py`, `python analyze_followup.py`, and
  `python -m unittest discover -p 'test_*.py'` after extracting the archive.

The first analysis invocation stopped on HTTP 200 non-JSON content. The reader was
repaired to classify it as unavailable data; raw capture and frozen acquisition
code were not changed. No numerical basis was emitted from the failed invocation.
All bounded processes have ended. No credentials or private accounts were used.

## Primary sources read

- Public liquidity scoring: https://help.kalshi.com/en/articles/13823851-liquidity-incentive-program
- Volume reward cap and eligibility: https://help.kalshi.com/en/articles/13823850-what-is-the-kalshi-volume-incentive-program
- Event fee schedule: https://kalshi.com/docs/kalshi-fee-schedule.pdf
- Separate designated-provider program: https://help.kalshi.com/en/articles/15410219-liquidity-provider-program
- Perps fees: https://help.kalshi.com/en/articles/16071417-perps-fees-explained
- Funding: https://help.kalshi.com/en/articles/15357613-how-funding-works
- Coinbase book API: https://docs.cdp.coinbase.com/api-reference/exchange-api/rest-api/products/get-product-book
- Kraken book API: https://docs.kraken.com/api-reference/market-data/get-order-book
- Kalshi contracts and books: https://docs.kalshi.com/margin-rest/market/get-markets
- Kalshi event depth parameter: https://docs.kalshi.com/api-reference/market/get-market-orderbook
