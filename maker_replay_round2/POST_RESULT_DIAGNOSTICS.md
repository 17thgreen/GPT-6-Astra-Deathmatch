# Post-result diagnostics — explicitly not preregistered

The frozen runs produced +$681.73 for the bid/ask-candle profile baseline and +$217.84 for the inventory-direction filter, under unobserved queue/depth assumptions. Print-proxy runs left residual positions at the cutoff. These outcomes motivate three operational sensitivity checks, not a search for the best backtest:

1. Raise only the early queue to 3,300, retaining the profile's 1,327,847.005 inside twelve hours. Unlike a flat-3,300 case, this never makes the assumed late queue easier.
2. Limit total assumed exit depth to 50 contracts per game. Report unresolved positions and bounds honestly.
3. Start cancellations/liquidation five minutes before T−3h and retry once per minute until the hard deadline, keeping one total 250-contract exit budget per game. This tests a practical buffer; it does not fit an optimal lead time.

Run these on the candle quote source. Rerun its unchanged baseline as a regression check after adding the optional lead-time control. No new model fitting. One NFL week cannot validate a profitable edge or establish that the best-looking variant is superior.

Taker sweeps remain hypothetical immediate executions against the latest available quote proxy with assumed depth. These experiments do not model a full taker submission/acknowledgment protocol, and a simulated flat-at-deadline result is not a guarantee of an actual flat-at-deadline execution. The early buffer is a practical direction for a future adapter, not a substitute for measuring its latency.
