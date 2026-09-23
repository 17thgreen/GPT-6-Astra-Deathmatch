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

Public GET orderbooks belong at `lab/astra-capture/c1-kxufcfight/orderbooks/`.
`collect_orderbooks.py` issues one GET per admitted ticker against
`https://api.elections.kalshi.com/trade-api/v2/markets/{ticker}/orderbook`.
Private routes, other methods, and other hosts are refused. The collector
does not start a recorder and does not edit this freeze by itself.

`production_orderbook_pins` in `FROZEN_EXPERIMENT.json` is the sha256 map.
`production_orderbook_status` refuses JSON in that directory unless the four
admitted filenames are present and each digest matches the map. A missing
capture is `FIXTURE_GAP`. A matching pin stays `NOT_SCORED` until an
Examiner-ready scorecard exists. This lab does not open that scorecard.

The 2026-09-23 public GET stored four files. Each is the empty venue object
`{"orderbook_fp":{"no_dollars":[],"yes_dollars":[]}}` with sha256
`e07d09f130e604a9e1acfc736fb57cbdfc33d8a5a253466a0cbd5c98cf6c9f74`. The lists
were not filled in. The pin is not an Examiner score.

Absence of pinned bytes leaves the synthetic stand-in for in-memory labels:

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
