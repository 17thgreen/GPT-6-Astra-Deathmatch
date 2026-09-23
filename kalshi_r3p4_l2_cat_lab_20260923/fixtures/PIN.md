# Synthetic schema stand-in

`synthetic_mid_depth_ladder.json` is an in-memory yes-bid / no-bid ladder.
It is not a Kalshi print, not the conductor panel, and not production depth.
Book ids are `synthetic:sports:flat10` and `synthetic:nonsports:touch`.

The conductor panel stub sha256
`7477e023ab70c59a6739650155ddb9d77077766e3afd80443e540d60b5a86cbb`
is not this file. That stub has 4 events and 6 markets. `SEED_SUMMARY.json`
sha256 `e0d5281133d89d5f0215a8f02ae438b688bf53e4a48f2eb4c3727db4a29bb6f2`
is an import-only copy of the attached summary. `results` and `pnl` stay
null when these synthetic rows are quoted.
