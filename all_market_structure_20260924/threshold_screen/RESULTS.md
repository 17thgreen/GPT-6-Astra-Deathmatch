# AMS-002: static threshold consistency screen

**No positive paired-payoff discrepancy was observed.** The bounded screen
completed: 16 successful metadata requests, six admitted threshold ladders,
24 contracts, and 48 successful book requests across two rounds. Seven focused
cost-model tests passed. No orders, credentials, or private account data were used.

There were 216 pair/quantity/round cases, not 216 independent opportunities:
36 distinct pairs x three quantities (1, 10, 100 contracts) x two observations.
180 cases had sufficient displayed depth for both legs. Every one cost more than
the conditional $1 normal-resolution payoff floor before fees. The remaining
36 lacked sufficient depth; they are unscored, not zero-profit trades.

| Series | Mechanism | Complete cases | Best gross floor margin per paired unit | Best unrounded-fee margin per paired unit |
|---|---|---:|---:|---:|
| KXAAAGASDFL | Florida regular gas price | 0/36 | Unscored | Unscored |
| KXAPSMM | SMM APT tungsten daily average | 36/36 | -4.00 cents | -4.4018 cents |
| KXBA | Boeing quarterly deliveries | 36/36 | -12.00 cents | -15.4482 cents |
| KXBIGGESTQUAKE | Daily maximum reviewed USGS magnitude | 36/36 | -18.00 cents | -20.2890 cents |
| KXCCLA | Carnival annual available lower berth days | 36/36 | -2.00 cents | -2.2730 cents |
| KXCPIYOY | September year-over-year CPI | 36/36 | -1.00 cents | -1.3409 cents |

These margins are payoff-floor minus entry cost, not expected returns or realized
losses. A nested pair can pay $2 in some states. A negative floor margin therefore
rejects this static arbitrage screen; it does not prove the pair has negative
expected value under an independently validated forecast.

No eligible positive case survived even a zero-fee screen, so fee rounding cannot
change the conclusion. Unrounded quadratic fees are an optimistic sensitivity;
per-level cent rounding is also reported in SUMMARY.json and individual score files.
Series fee multipliers come from the prior public catalog; account-specific terms,
future fee changes and fill fragmentation remain unverified. There is no rebate.

## What the rule review teaches us about faster taking

**A source is useful only while the target contract is tradeable.** YOYCPI terms
close trading at 8:29 AM ET on the scheduled release date. An ordinary strategy
that reads the scheduled CPI release and then buys this contract has no post-release
trading window. It needs a different still-open instrument or a pre-release model.
The AAA gas contract likewise closes the prior evening in ET; today's posted gas
number must not be assumed available before that cutoff.

**The first visible datum may not be the settling datum.** BIGGESTQUAKE requires
reviewed USGS ComCat events and excludes automatic detections and withdrawn events;
pre-expiration revisions matter. A raw seismic alert is an input to an uncertain
forecast, not proof that a threshold has settled. COMMODITIES terms include formal
corrections and delayed-data provisions; speed does not remove this uncertainty.

**Company reporting gives an interpretation hypothesis worth testing.** The KPI
contracts use a hierarchy of official reporting materials. A system that parses
the correct metric, period and qualifying report could have an advantage over
traders reacting to a broad headline. This is a candidate mechanism, not an observed
edge. Boeing's quarterly contract and Carnival's annual contract also permit
exchange-determined fair-market settlement in specified missing/changed-metric
circumstances. The $1 paired floor is conditional on normal resolution.

## Selection and measurement limits

The series panel spans 12 categories, but the six-ladder book panel spans five
primary categories. Eight series had no same-event, same-time, same-comparator
ladder with distinct strikes. Sports playoff-host and movie-rating ladders were
eligible but excluded by the preregistered six-series lexical cap; they were not
rejected economically. Crypto hit-by-date markets were excluded by this particular
same-event/time test, not rejected as a strategy family. A deadline-nesting proof
would require its own source/start-time and early-resolution checks.

All admitted groups use their first four numerical strikes, not necessarily strikes
near a 50% probability. Two rounds are a tiny development sample. The pairwise
receipt skew among scored books reached roughly 136 ms; the median HTTP request
round trip was about 3.94 seconds. These are different measurements. Similar
receipt times do not establish simultaneous exchange snapshots or quote freshness.
There is no production streaming feed, order latency measurement, cancellation
race model, or independent source lead/lag test here.

The practical next experiment is **information propagation while trading is open**:
first verify the source, metric, revision policy and trading cutoff; then retain
source arrivals and venue book changes around releases. Corporate official-report
interpretation is a concrete candidate. Crypto deadline nesting and the excluded
movie/sports ladders remain separate candidates. Do not infer that any is profitable
from this static screen, and do not fund infrastructure based on it.

## Reproduce and inspect

- Initial specification and series panel: commit `9302bfa82d4c91841c5d68a6d1e418c307f21907`.
- Rules-reviewed instrument admission, source freeze and cost tests before books:
  commit `7ee26ba9ec0c3a8e37c564af0cae9f66dda8c618`.
- `SUMMARY.json`: aggregate descriptive results and best-case identifiers.
- `scores_*.json`: every pair/size/round outcome, including missing depth.
- `AMS_002_Evidence.zip`: full raw public metadata/book receipts, detailed leg cost
  calculations, source, tests, rule-source hashes, admission and summary.
- `ARCHIVE.json`: archive size and checksum. `EVIDENCE_HASHES.json`: member hashes.
- After extracting, run `python analyze.py` in this directory to reproduce results;
  `python -m unittest discover -p test_economics.py` runs the focused tests.

The PDF terms were read from the URLs recorded in RULE_SOURCES.json. Their bytes
were hashed; the PDFs themselves are not redistributed in this archive. API rule
fields are preserved with the metadata receipts. Original AMS-001 is unchanged.
Both bounded collection stages have ended. No background process is deployed.

Primary sources: https://kalshi.com/docs/kalshi-fee-schedule.pdf and the six contract
terms linked in ADMISSION.json. The normal-resolution review is not a determination
of every possible discretionary exchange settlement outcome.
