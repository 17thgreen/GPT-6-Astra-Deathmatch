# AMS-008: broad static price discrepancies fail current fees

Retained development snapshot: 5432 open usable markets, 3268 threshold contracts admitted, 312 pairable rule/expiry groups, 16436 pairs at three quantities. 32270 depth-complete cases and 17038 insufficient-depth cases.

Five cases across two pairs had positive gross floor margins. None survived the ordinary M=1 unrounded taker-fee benchmark. The fixed follow-up confirmed both series currently report quadratic fees with multiplier 1, and refreshed quotes still failed after fees. Matching rule templates remained intact. No profitable opportunity was established.

| Pair series | Quantity per leg | Fresh gross margin | Fresh margin after standard raw fees |
|---|---:|---:|---:|
| KXMSCOTTON | 1 | 0.0100 | -0.0247130000 |
| KXMSCOTTON | 10 | 0.1000 | -0.2471300000 |
| KXMSCOTTON | 100 | 0.000000 | -3.476900000000 |
| KXTEENCLOTHADS | 1 | 0.0100 | -0.0063450000 |
| KXTEENCLOTHADS | 10 | 0.1000 | -0.0634500000 |
| KXTEENCLOTHADS | 100 | 1.0000 | -0.6345000000 |

The active public event-volume catalog returned 0 programs with no remaining cursor. We could not establish an applicable volume subsidy to offset these costs. The theoretical two-leg cap of one cent per paired unit is not admitted revenue. Private fee terms and account-specific eligibility were not inspected.

Decision: keep the static taker threshold lane parked. This broader check justified one revisit; do not continue scanning the same retained data for a desired answer.

This is reused development data, not an independent holdout. Quotes are asynchronous; even same-response receipt times do not imply atomic multi-market execution. The payoff floor assumes ordinary, common-source binary resolution and excludes explicit fair-value language, but source metadata and normalized text do not substitute for a complete contractual settlement proof. These limitations would matter for a positive result. No inventory, reward or realized P&L was booked.

Four focused tests passed before analysis. All original and follow-up freeze hashes and eleven HTTP 200 follow-up receipts verified. CASES.jsonl preserves all 49,308 cases. The archive includes cases, code, freezes, follow-up receipts and results; reproducing the original screen additionally needs the AMS-005 raw-evidence artifact referenced in ../reward_census/ARCHIVE.json.

Original source freeze: 08a6cb8bd7cc3c005c4b2fbb97ec45d1b0efc66b. Follow-up freeze: 29bfce1fc2e1dfdb463d4b1cd7aa62b1055eb13b.

Sources: https://kalshi.com/docs/kalshi-fee-schedule.pdf ; https://help.kalshi.com/en/articles/13823850-what-is-the-kalshi-volume-incentive-program ; https://docs.kalshi.com/api-reference/market/get-market-orderbook .

No acquisition or analysis process remains running for AMS-008.
