# Forward handoff: NH-002 is not admitted or running

The historical House result justifies collecting prospective evidence. The
current-book recorder is implemented and tested. A current forecast adapter and
a complete prospective experiment remain blocked by source admission. This is
not a deployment record or an instruction to trade.

## Scientific question

Does a current external congressional model improve House probabilities, and can
its fixed 50/50 hybrid identify purchases that retain an advantage after actual
fees, entry latency and observed depth? Keep market-only, model-only and 25%-model
comparisons. Do not select weights by the completed 2024 result. Treat election
outcomes as correlated and repeated snapshots as repeated observations.

## Required admissions

1. **Probability source:** obtain a lawfully accessible current feed. Preserve
   bytes, URL, retrieval/publication time and model version. Verify party victory
   for the exact district, not vote share or qualitative ratings. Disclose market
   inputs in the model. Refuse stale/missing probabilities; never reuse 2024 538
   values for 2026 contracts. The Economist page was not accessible for admission.
2. **Immutable panel:** enumerate the current series with full pagination, audit
   regular-election/2027 swearing-in rules, redistricting and independents, then
   deduplicate party and YES/NO representations. Freeze before scoring. Do not
   choose only the three winning 2024 districts. The observed 707 open contracts
   are discovery data, not 707 distinct races or a frozen admitted cohort.
3. **Observation times:** freeze decision/capture times before collecting scores.
   Retain 24-hour forecast lag and seven-day maximum age unless a new specification
   changes them in advance. Preserve missed windows as missing. Record request
   start/end and exchange timestamps where supplied; never backdate availability.
4. **Fees and execution:** admit series fee schedule, multiplier, rounding and
   exceptions. Use reciprocal depth, actual level prices and later snapshots.
   A disappearing quote is a failed opportunity, not an assumed fill. Begin with
   one unit; investigate size as a separate capacity diagnostic. Do not multiply
   unit returns by bankroll without evidence of available size.
5. **Portfolio and outcomes:** one position per underlying race. Freeze any repeat
   entry policy in advance. Track cash, cost, open inventory, party/regional
   concentration, both adverse national scenarios and official settlements.
   Unresolved inventory is not realized profit. Model holding time and any exit
   policy explicitly. Keep every abstention and missing-data reason.

## Implemented interface

```bash
python3 capture_books.py raw/a-new-unique-run KXHOUSERACE-AL01-26-D
```

This bounded one-shot GET-only recorder accepts 1–25 explicit tickers. It refuses
to reuse an output directory, records response bytes and hashes, validates decimal
prices/quantities, computes reciprocal asks, and emits no forecasts or trade
signals. The example is a schema smoke-test ticker, not a recommendation.

The three-book smoke test passed September 24, 2026. Requests took several seconds;
receipt time is not proof of continuously fresh exchange state. The recorder has
no scheduler, order placement, position sizing, credentials or production risk
integration. No background process was started.

## Promotion or stop

Resolve source and mapping admission, then commit a full prospective specification.
Require improved forecast loss on the untouched cohort, positive performance
under admitted fees/latency, adequate distinct opportunities to assess concentration,
and a credible size bound before discussing capital. A race-count minimum alone
is not a power analysis; hundreds of races in one election share common shocks.

Stop or open a newly frozen hypothesis if the improvement disappears, entries
cannot be acquired at the recorded cost, results rely on a few correlated races,
or capital holding periods defeat the intended economics. Preserve the negative
Senate finding and all failed data and entry gates.
