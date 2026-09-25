# Q6S5 KXMLBSPREAD fee and queue honesty

September 25, 2026. This file is the hypothesis. It is committed with the
harness before a unit-test outcome is recorded in `results/UNIT_RESULTS.md`.
No figure in this document is a trading result. Q6 outcomes that already
exist are not re-labeled as evidence from this probe. This is measurement-only
MLB spread fee and queue honesty. Feature family Q6S5-MLBSPREAD-FEEQUEUE.
The series is `KXMLBSPREAD` only.

## Placement

The harness freeze is
`Q6S5_KXMLBSPREAD_FEEQUEUE_HARNESS_FREEZE_2026-09-25.md`, sha256
`4f65dcdf536755b9f7dc2449c2dcd90b2df74cdf99a441b676f1a71c4d709c6e`.
Those bytes are the attached Conductor freeze. The same bytes sit at the
lab root, the lab bundle, and
`lab/governance/astra/packets/`.

Conductor ACCEPT sha256
`5adc42f9c9533238a2187aafe7593bdf1b8cdec6d12b8d3e9b12cb5ab29000fc`.

Panel stub: `lab/astra-capture/q6s5-kxmlbspread/panel_stub.json`,
`panel_version` `2026-09-25.q6s5-kxmlbspread-v0`, sha256
`c7f1f1f4ca263838c4600ed46db8f525b68efc5399a567bd60929d18d76803cc`.
`admitted_at` is null. 6 events and 12 markets. The same bytes are in the
lab. `panel_admitted.json` is preferred when it appears. This harness does
not write it and does not run `admit.py`.

Scout raw markets sha256
`80b52f47c836248d5869806d7f59617535e6b78258367ebe6045af4275fff7e7`
(93 markets / 15 events) and summary sha256
`c9e871b3c4edbc648972f9313b3bbcd6784efc46ca847e1f0de4c2847ce85ebe`
are cited. Those files are not in this checkout. They are not recreated.
`digest_all_match_claimed` is true only when every claimed pin re-hashes,
including those scout files, the p16 PDF, and the archivist ping.

`SOURCE_PINS.json` sha256
`588fdbd0a293823cf96b66ace00145ad10f56efb40badc4b2007b5e4bc832fde`
is identical at the governance packet, the lab root, and the lab bundle.

## One knob

`analysis_slice`:

| Arm | Slice |
|---|---|
| Q6S5A0 | `maker_vs_taker_native` — native `taker_*` fields only. Lee-Ready refused |
| Q6S5A1 | `content_fresh_vs_stale_bin` — rails `content_fresh_flag` and queue-attribution bins. No invented fills |

Feebook commit `22371178cb2663250b4762f328069571c48cb551` (import only).
Rails commit `6a28e0d6254327ea4e6451c781bec56215ac6cac` (import only).

The series fee is cache-labeled: `fee_type=quadratic`, multiplier `0.5`.
Every fee output sets `cache_labeled` true and `live_r1p1` false. The cache
label is not an R1-P1 live `/series` pin. No dollar fee is published.

Public capture, when exercised, uses the stub transport against
`https://api.elections.kalshi.com/trade-api/v2/`. GET only. `/orders` and
`/portfolio` are refused. While `/markets` is hot the stub prefers `/events`.
The default transport records `live_gets` 0.

`results`, `pnl`, `maker_vs_taker_roi_delta`, `fresh_vs_stale_gap`,
`settled_join_n`, and `n_books` stay null. Examiner scorecard v1.2
`verdict`, `gate_status`, common-scorecard values, and `study_label` stay
null. Examiner status stays `HOLD_PRE_PR`.

Nearest dead cards: Card 06 open-window CLOSED, and S1 KXMLBGAME ML retune
FORBIDDEN. This packet does not retune either. The NFL `000` file is a
pointer only.
