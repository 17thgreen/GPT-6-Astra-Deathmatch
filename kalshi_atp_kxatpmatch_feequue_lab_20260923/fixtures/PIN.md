# Synthetic schema stand-ins

`synthetic_native_trades.json` and `synthetic_fresh_queue.json` are in-memory
schema rows. They are not Kalshi prints, not the conductor panel, not the
scout hunt, and not fills. `results` and `pnl` stay null when these rows are
classified. They do not carry `occurrence_datetime` or `fill_density`.

The conductor panel stub sha256
`ed041c502d1f775d33c44bf900ac91b1339d99045bddd2052edd09a139ae2d3f`
is not these files. The scout hunt sha256
`14c99ec8ea00bae507a21d0e6a1879fb94d32ef69ad4b5e3b40a9952821e5da7`
is not these files.
