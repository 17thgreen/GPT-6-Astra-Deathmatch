# C5 KXBTC15M settled-resolution join

September 23, 2026. This file is the hypothesis. It is committed before a
unit-test outcome is recorded. No figure in this document is a trading
result. This is measurement-only settled-resolution join. Feature family
C5-RJ. It is not a reopen of the C5 honesty lab and it is not live crypto
trading.

## Placement

The harness freeze committed verbatim is
`C5_KXBTC15M_SETTLED_RESOLUTION_JOIN_HARNESS_FREEZE_2026-09-23.md`, sha256
`7f4b36eca39d43ee7403628c2e525d5980fa40bcfc906550c7f00bb06ffd4f21`.
Those bytes are the attached conductor freeze. The same bytes sit at the
lab root and in `C5_KXBTC15M_SETTLED_RESOLUTION_JOIN_HARNESS/`.

Scout reget sha256
`7be17c44aef31abf7a0ab94938d0289f8766670ddacefdec566735818e044796`
is `scout_settled_rejoin_C5_KXBTC15M.json`. The freeze cites
`lab/governance/astra/packets/scout_c5_settled_rejoin_2026-09-23/`.
That C5 cite is absent in this checkout. The attached bytes are in this
lab. An unrelated R3-P2 packet under `lab/governance/astra/packets/` is
not this harness and is not edited.

Seed summary sha256
`b39c919809f709bcb81ff10a3d983b266bc7a1303c0de502c7c20be726415198`
is `SEED_SETTLED_SUMMARY.json`.

Panel stub sha256
`60f613e8d775b66b9044ad31d2faf77bba84176f214a7bce599aa7a65b6905f8`,
`panel_version` `2026-09-22.c5-kxbtc15m-v0`, packet
`C5-KXBTC15M-MEAS`. `admitted_at` is null on the stub, on the event,
and on the market. The same bytes are already at
`lab/astra-capture/c5-kxbtc15m/panel_stub.json` and are not rewritten.
`panel_admitted.json` is absent. This harness does not run `admit.py`
and does not write `admitted_at`.

Settled reget capture sha256
`319d6d3e394089fd21fefbfaa52c58166e78c2d781077a3f876331d2c54de617`
is `settled_reget_2026-09-23.json`. The freeze cites
`lab/astra-capture/c5-kxbtc15m/settled_reget_2026-09-23.json`. The
attached bytes are committed in this lab. The capture directory's
existing `panel_stub.json` is left as it was.

Conductor ACCEPT sha256
`e116bbcb5f9518e6008ef412c8ff212a3170d0e3f26eb978f07a204b327aba7d`
is `decision` ACCEPT and `implement` true. It is committed verbatim.

Attached `FROZEN_EXPERIMENT.json` sha256
`31db09b93b09dccd449ad2ade56838eb6ccb531990209a5cbe85e91703dfeffc`
keeps `results` and `pnl` null. Attached `results/EMPTY_RESULTS.json`
sha256
`94f5e75928b530516143fcf6b23c6b532701c3afb5da84327adf550a4046d4e3`
keeps `results`, `pnl`, `settled_join_n`, `occurrence_match_n`, and
`admit_ready_flag` null.

`SOURCE_PINS.json` lists those digests. It does not contain the file
bytes.

Starting ref is main at `9eba15870e66dcde8ffc17a56c73016245a833c1`.
Feebook `22371178cb2663250b4762f328069571c48cb551` and rails
`6a28e0d6254327ea4e6451c781bec56215ac6cac` stay fixed and are not loaded.
This join has no fee arm.

## One knob

`join_gate`:

| Arm | Gate |
|---|---|
| J0 | `nonempty_result_required` — Clock-admit readiness is defined only for settled markets whose official `result` is already non-empty on the reget |
| J1 | `occurrence_datetime_match` — SoT `occurrence_datetime` on the reget matches the seed summary for that ticker, and the parent seed ticker also matches the panel stub |

Both arms share the same panel parent and the same GET-only reget pins.

The scout pin `settled_nonempty_result_N` is 20. That pin is the settled
list page. It is not `settled_join_n`. The parent seed ticker
`KXBTC15M-26SEP222045-45` is finalized with official `result` `no` on
the authentic reget and is not on that limit-20 page. The panel stub
still stores `result` null and `status_at_stub` `active`. This harness
does not copy the reget result onto the stub.

`status=finalized` and `status=closed` list filters are recorded as
`429 too_many_requests`. Those gaps have no market object. They are not
backfilled. Open ticker `KXBTC15M-26SEP231530-30` is cited on the scout
and has no market object in the settled reget. It is not invented.

## What this run does not claim

No invented settled `result`, depth, fills, or PnL. No Lee-Ready. No
`admit.py`. No live orders. No Logan keys. No live crypto trading. No
Cap-SR reopen. No FQ sibling reopen. No C5 honesty reopen. No C3-RJ
reopen. No Arm B. No ungate of S1, S2, or R2-P4. `settled_join_n`,
`occurrence_match_n`, and `admit_ready_flag` stay null until Examiner
after merge and sha verify and Clock admit. Examiner status stays
HOLD / `NOT_SCORED`. A later unit page is code verification only.
