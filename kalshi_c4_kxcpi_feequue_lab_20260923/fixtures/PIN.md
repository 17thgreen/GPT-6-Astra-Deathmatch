# Synthetic schema stand-ins

`synthetic_native_trades.json` and `synthetic_sparse_fresh.json` are in-memory
schema rows. They are not Kalshi prints, not the conductor panel, not the
scout hunt, and not fills. A `volume_24h_fp` of `0.00` on a synthetic row is
a refuse label. It is not a fill density. A null `occurrence_datetime` on a
synthetic row stays null. `results` and `pnl` stay null when these rows are
classified.

The conductor panel stub sha256
`b20b0cbee50c127d2e9bb2548b574b7d643cc708f54019d53bd91775f9762c13`
is not these files. The scout hunt sha256
`6033907bb739bc00c41c796a3c1ed24553e0b7a44116ec3ea4bbaf39066bdcc8`
is not these files.
