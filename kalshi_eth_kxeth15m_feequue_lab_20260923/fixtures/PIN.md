# Synthetic schema stand-ins

`synthetic_native_trades.json` and `synthetic_fresh_queue.json` are in-memory
schema rows. They are not Kalshi prints, not the conductor panel, not the
scout hunt, and not fills. `results` and `pnl` stay null when these rows are
classified. They do not carry `occurrence_datetime` or `fill_density`.

The conductor panel stub sha256
`b3379783c84eaa910f6a57f5318b8536f21220cfeaf0f73e9ff73ee0f20dd90d`
is not these files. The scout hunt sha256
`18f70001c8d68418d435e2016b756f90753e374a92d323f8e999f76215d9cf9c`
is not these files.
