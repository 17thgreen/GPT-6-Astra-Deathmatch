# AMS-006: historical prints around candidate reward windows

Motivation: AMS-005 metadata showed zero or one lifetime traded contract for seven
short-lived Miami weather candidates, but 1000 contracts at a one-cent last price
for two Truflation tail candidates. An empty book can follow a fill, not just lack
of interest. Metadata alone cannot establish trade time, size or taker direction.

Use exactly the 10 frozen AMS-005 FOLLOWUP_PANEL tickers; no replacements. Fetch
public trades, limit 1000, at most two pages per ticker, ticker filter, no credential.
Four workers, 12-second timeout, no retries, 120-second soft total budget. Retain
all raw responses and remaining cursors. This is retrospective tape description,
not a counterfactual execution backtest or independent holdout.

Report total contracts, first/last observed trade times, printed prices, whether
trades fell inside each candidate's program window, and taker side. For a one-cent
YES quote, only a NO-aggressor print at YES <= one cent is directionally compatible
with selling into that bid. For a one-cent NO quote, require YES aggressor and
NO <= one cent. Unknown schema/direction is unclassified. Such prints still do
not prove our hypothetical order would have filled (queue and market response are
unobserved). A zero-print interval without our quote does not measure the fill risk
after we improve the book. Never use absence of public trades as proof of rewards.

Compare before-program and within-program evidence. Do not infer wash trading,
participant identity, quote lifetime, reward credits or profitability from volume.
No orders, no risk-limit changes and no profitable-strategy admission.

Source: https://docs.kalshi.com/api-reference/market/get-trades
