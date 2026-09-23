# Synthetic schema stand-in

`synthetic_mid_ladder.json` is an in-memory yes-bid / no-bid ladder. It is
not a Kalshi print, not the conductor panel, and not a fill. Player ids are
`SYNTHETIC_A` and `SYNTHETIC_B`. Strike ids are not production market tickers.

The conductor panel stub sha256
`70e879e8738d033f392d821849dee3537af3e7b8a916670779d238f78ce098be`
is not this file. That stub has 6 events, empty `market_tickers`, and null
volume. `results` and `pnl` stay null when these rows are fit.
