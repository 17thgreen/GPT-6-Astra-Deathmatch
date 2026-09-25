# Synthetic schema stand-ins

`synthetic_native_trades.json` and `synthetic_fresh_queue.json` are in-memory
schema rows. They are not Kalshi prints, not the conductor panel, not the
scout raw file, and not fills. `results` and `pnl` stay null when these rows
are classified. They do not carry `occurrence_datetime` or `fill_density`.

The conductor panel stub sha256
`c7f1f1f4ca263838c4600ed46db8f525b68efc5399a567bd60929d18d76803cc`
is not these files. The scout raw markets sha256
`80b52f47c836248d5869806d7f59617535e6b78258367ebe6045af4275fff7e7`
is not these files. Those scout bytes are not in this checkout and are not
recreated here.
