# Post-score execution diagnostic

This diagnostic is specified after NH-001/A scores were viewed. It is not another
holdout, a change to entry rules, or evidence of historical fills. Keep the
original strategy results unchanged.

For every frozen hybrid_50 signal at both NH-001A horizons (House and Senate),
request the next five minutes of historical minute candlesticks. Inspect the
original purchase side's ask at each strictly later candle end. Report the
one-minute observation when available, missingness, and the range of subsequent
quoted costs. Reprice the original fixed unit trade with its original outcome,
illustrative fee and 2c buffer; never reselect or change its side after seeing
prices. Missing observations stay missing. Quote persistence does not prove an
order could fill, that a quote stayed visible continuously, or that size existed.

Separately add a bounded, public GET-only current-book capture utility. Persist
receipt time, request latency, raw response hash and all returned depth. It must
interpret YES asks from NO bids and vice versa, support decimal quantities and
refuse invalid/crossed/missing books. This records data, not trade recommendations.
No recurring process, forecast substitution, sizing, order API, or credentials.

Live signals remain blocked until a current independent probability source,
exact current contract mappings, applicable fees and a separate prospective
protocol have been admitted. A 2024 538 probability must never feed a 2026 signal.
