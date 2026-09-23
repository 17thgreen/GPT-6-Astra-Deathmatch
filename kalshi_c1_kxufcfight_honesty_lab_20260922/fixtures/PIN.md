# C1 KXUFCFIGHT capture pin

The schema seed is the panel stub. This file is the path and the sha256. It
does not contain production orderbook bytes.

| Role | Path | SHA-256 |
|---|---|---|
| Kernel | `packets/C1_KXUFCFIGHT_MEASUREMENT_FREEZE_KERNEL_2026-09-22.md` | `a191c9b3f71030445d1d32684feb6dc1bf09abb7e09403d5dbdf1927eafc63c9` |
| Panel stub (pre-admit, not the subject) | `lab/astra-capture/c1-kxufcfight/panel_stub.json` | `2cc661d86202d3daf9ffa45320e39d249852a97490f458f72ab7ea8ec5c81a00` |
| Admitted panel | `lab/astra-capture/c1-kxufcfight/panel_admitted.json` | prefix `24426d80` |

`panel_version` is `2026-09-22.c1-kxufcfight-v0`. `admitted_at` is
`2026-09-23T00:49:43Z`. The harness reads the admitted file and refuses the stub.

## Production capture path

Public GET orderbooks belong at `lab/astra-capture/c1-kxufcfight/orderbooks/`
when a later collector writes them. The allowlist is the stub: series,
market, a small open list, orderbook, and small trades, on the public
elections host. This harness does not GET and does not start a recorder.

This freeze has no production orderbook sha256. If that directory contains a
JSON file, `resolve_orderbooks` refuses it. Absence selects the synthetic
stand-in:

`kalshi_c1_kxufcfight_honesty_lab_20260922/fixtures/synthetic_orderbooks.json`

That stand-in is not live depth. It omits `volume_fp` and `open_interest_fp`.
The kernel's scout page-sample sums stay in the kernel prose. They are not
copied onto the panel. Restoring a future capture does not authorize writing
measurement fields into `FROZEN_EXPERIMENT.json`.

## Instruments

Fee: `kalshi_feebook_lab_20260922` at
`22371178cb2663250b4762f328069571c48cb551`.

Rails: `kalshi_rails_lab_20260922` at
`6a28e0d6254327ea4e6451c781bec56215ac6cac`.

Queue bins are `rails.QUEUE_SCENARIO_LABELS`. A size that misses both labels
is `outside_pinned_bins`. Those are the same labels the Q6-`000` rails
instrument emits. This lab does not open the `000` fills gzip.
