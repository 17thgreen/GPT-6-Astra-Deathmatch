# M2: unchanged NFL settings do not establish profitable expansion

September 22, 2026. The frozen eight-game NCAAF/WNBA transport pilot is complete.
All twelve scenarios finish flat and all twelve financial ledgers reconcile.
Neither sport earns a profitability claim or production promotion from this pilot.
Q7 remains the selected NFL development candidate.

## Completed simulated net, after standardized modeled fees

Each row is an alternative with one $5000 account. Standalone sport rows have
four games; combined has all eight games in one chronological account.

| Alternative | Queue 3300, .25s | Queue 3300, 5s | Queue 10000, .25s | Queue 10000, 5s |
|---|---:|---:|---:|---:|
| NCAAF | +$2.47 | +$2.47 | -$2.80 | -$2.80 |
| WNBA | -$45.18 | -$45.18 | -$35.29 | -$35.29 |
| Combined | -$42.72 | -$42.72 | -$38.09 | -$38.09 |

These are counterfactual fills against real public trade tapes and delayed
minute-close bid/ask observations. They are not actual account fills or earnings.
NFL queue, participation, fee, netting and exit assumptions were deliberately
retained as transport controls. The small, nonrandom cohort cannot rank sports
or estimate durable expected returns. No parameter tuning followed the outcomes.

## Why the expansion did not work under these settings

At queue 3300, NCAAF generated 5,416.26 maker contracts and no taker exits.
After $14.6137 in modeled fees, it retained only $2.4676. Three of four games
traded: Syracuse/Pittsburgh +$2.0296, Houston/Texas Tech -$2.7810,
Miami/Wake Forest +$3.2190; Portland State/Oregon had no fills. The net becomes
negative at the deeper queue, with 253.57 taker contracts across the four games.

WNBA generated 750 maker contracts and needed 750 taker contracts to close them.
Passive completion was zero in that scenario. The before-fee loss was $35.00;
$10.185 in fees brought it to -$45.185. Thus fees did not create the entire loss.
Connecticut/Atlanta contributed -$1.6100, LA/Dallas $0, Las Vegas/Seattle
-$8.2830, and Phoenix/Portland -$35.2920. The deeper queue traded only the
Phoenix/Portland exposure and finished at -$35.2921. These are simulator
diagnostics, not estimates of the causal effects of queue depth in the venue.

Static complementary prices did not guarantee that both legs would fill before
their prices moved. This is the same completion issue identified by the failed
Q8 routing variants. Adding market coverage can add losing inventory as well
as independent opportunities. Faster modeled submit/cancel delays did not
change any of the twelve completed P&L values in this pilot.

## What the fleet question gains from this test

The combined $5000 account reproduces both standalone economic fill histories
exactly in every queue/delay scenario, after removing account-balance and order-ID
fields. Cash minus outstanding reservations stayed above a conservative lower
bound of $2,519.53 across the combined cases. Funding competition did not displace
fills here. More available cash would not repair these particular completion
losses under unchanged order and exposure limits.

This is a post-result accounting diagnostic, recorded in capital_diagnostics.json.
It is not evidence that shared allocation always dominates fixed allocations.
The current matrix did not test $2500/$2500 separately funded bots. Adding the
two standalone $5000 profits is generally a $10000 alternative; their equality
to the combined account here is a measured property of these fill histories.

Use distinct strategy ledgers and enforce per-sport plus total risk limits.
Then compare fixed funding with a common reserve at equal total capital on a
new frozen cohort. Each market should earn admission through completed net,
completion costs and robust access assumptions. See docs/FLEET_CAPITAL_DESIGN.md.

## Data coverage and limits

- Eight events selected before tapes: four NCAAF, four WNBA; sixteen tickers.
  No failures were replaced and no losing or inactive games were dropped.
- All sixteen bounded captures completed: 27,837 trades and 42,496 non-null
  minute bid/ask records. Of the latter, 39,741 have strictly valid inside-0/1
  spreads; invalid books remain visible to the engine and cannot support entry.
  Missing minutes and null prices were not interpolated.
- NCAAF had 25,232 trades; WNBA 2,605. These counts are public trade observations,
  not independent opportunities or the simulator's executed contracts.
- Valid, received, nonstale quote coverage was 58.38% of the NCAAF opening windows
  and 63.37% of WNBA windows, weighted by window seconds. Inactive/unquoted periods
  do not receive manufactured prices. Sparse observations limit interpretation.
- NCAAF markets were listed throughout the 165-hour T-7d to T-3h interval. WNBA
  markets supply only 68 hours 50 minutes from listing to T-3h. The five-minute
  pre-cutoff winddown further shortens opening eligibility in both sports.
- Starts and rules were retrieved retrospectively. There is no historical
  lifecycle stream verifying all schedule changes, pauses or exceptional states.
  Ordinary pregame operation at reconstructed starts is an explicit assumption.
  No fair-price settlement or terminal winner cash was credited.
- The final-12h queue of 1,327,847.005, early queues, .5 participation, 250 total
  exit contracts per game, immediate netting and .0175/.07 fee coefficients are
  standardized assumptions, not measured non-NFL execution conditions.

## Verification and recovery

Cohort freeze d7079b6 follows specification bcd39b3. Source and complete raw-input
freeze: **3f12171a2b0e0ad6d5b6cdde0fa76f0dcfa91176**, published before replay.
Ten new normalization/listing tests and 152 inherited tests pass. The synthetic
listing regression reproduces Q7's orders and fills after listing. Independent
verification recomputes fees, pairing, cash, inventory, order quantities, listing
eligibility, cancellation timing and total exit usage for all twelve runs.
All frozen input/source hashes still match. There were no failed matrix runs.

Raw inputs are small and included in Git. The 36 compressed outcome ledgers are
preserved in M2_CFB_WNBA_Ledgers_2026-09-22.zip (about 17.3 MB); DATA_ARCHIVE.json
and EXTERNAL_ARTIFACTS.json contain its checksum and every file's checksum.
The archive was saved successfully and its extracted bytes were checked.
Extract it at repository root; run `python verify_replay.py` from this directory.
Do not rerun run_replay.py over existing results; it deliberately refuses that.

No live fleet, orders, transfers, risk-limit increase or always-on collector was
created. User-owned forward validation remains separate from this research.
