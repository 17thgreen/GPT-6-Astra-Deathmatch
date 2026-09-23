# R3-P3 FL maker/taker settled-resolution join

September 23, 2026. This file is the hypothesis. It is committed before a
unit-test outcome is recorded. No figure in this document is a trading
result. This is measurement-only settled-resolution join. Feature family
R3P3-RJ. It is not a reopen of the R3-P3 maker/taker fee arms and it is
not a reopen of C3-RJ.

## Placement

The harness freeze committed verbatim is
`R3_P3_FL_SETTLED_RESOLUTION_JOIN_HARNESS_FREEZE_2026-09-23.md`, sha256
`7fcfc36ab4761e2dec56018b498372fb63c402f2582fe848e8775e28f9b720b9`.
Those bytes are the attached conductor freeze. The same bytes sit at the
lab root and in `R3_P3_FL_SETTLED_RESOLUTION_JOIN_HARNESS/`.

Scout reget sha256
`f675d7c40ccad37173b2cb54837349cd3053b7b76606c43efba5759a1bde551f`
is `scout_settled_rejoin_R3P3_FL_MAKER_TAKER.json`. The freeze cites
`lab/governance/astra/packets/scout_r3p3_settled_rejoin_2026-09-23/`.
That cite is absent in this checkout. The attached bytes are in this
lab. An unrelated R3-P2 packet under `lab/governance/astra/packets/` is
not this harness and is not edited.

Seed summary sha256
`b43d4ab065b712f5bf1b87eb164bccb00e8e9993f97db9d86a8d1619ce9ec13d`
is `SEED_SETTLED_SUMMARY.json`.

Panel stub sha256
`6f640dd3a6091ba6b896ded38fdded4676583aa3c885223da21ddf03780250c0`,
`panel_version` `2026-09-22.r3-p3-fl-maker-taker-v0`, packet
`R3-P3-FL-MAKER-TAKER`. `admitted_at` is null on the stub, on each
event, and on each market. The same bytes are already at
`lab/astra-capture/r3-p3-fl-maker-taker/panel_stub.json` and are not
rewritten. `panel_admitted.json` is absent. This harness does not run
`admit.py` and does not write `admitted_at`.

Settled reget capture sha256
`c5f680e4ff66af67691672c4b8c43eb57906f25b4d79fdeb65f61e031c13efda`
is `settled_reget_2026-09-23.json`. The freeze cites
`lab/astra-capture/r3-p3-fl-maker-taker/settled_reget_2026-09-23.json`.
The attached bytes are committed in this lab. That capture path is not
added.

Conductor ACCEPT sha256
`a6434fe4854b850df24a0a081168ba5d90d4646ba9a409418d7b874262a5fa9c`
is `decision` ACCEPT and `implement` true. It is committed verbatim.

Attached `FROZEN_EXPERIMENT.json` sha256
`dd2a4217de4476d9c54a4487e68fe7bd912914bb55a5a1be4bc00126199f19e0`
keeps `results` and `pnl` null. Attached `results/EMPTY_RESULTS.json`
sha256
`d0f5fbfa3e01fca5f047f42ecc7e1bb5b1d4097ee455d6ce62a4b8a861d4a613`
keeps `results`, `pnl`, `settled_join_n`, `occurrence_match_n`, and
`admit_ready_flag` null.

`SOURCE_PINS.json` lists those digests. It does not contain the file
bytes.

Starting ref is main at `8cfcd17a62d3793dee554a4da422e8075bde9cf6`.
Feebook `22371178cb2663250b4762f328069571c48cb551` and rails
`6a28e0d6254327ea4e6451c781bec56215ac6cac` stay fixed and are not loaded.
This join has no fee arm.

## One knob

`join_gate`:

| Arm | Gate |
|---|---|
| J0 | `nonempty_result_required` — Clock-admit readiness is defined only for settled markets whose official `result` is already non-empty on the reget |
| J1 | `occurrence_datetime_match` — SoT `occurrence_datetime` `2026-09-23T14:00:00Z` on the panel stub matches the authentic reget and the seed summary for each parent seed |

Both arms share the same panel parent and the same GET-only reget pins.

The scout pin `settled_nonempty_result_N` is 20. That pin is the
`KXHIGHNY` settled list page. It is not `settled_join_n`. The three
parent seeds `KXHIGHNY-26SEP22-B67.5`, `KXHIGHNY-26SEP22-T70`, and
`KXHIGHCHI-26SEP22-B64.5` are finalized with nonempty official `result`
on the authentic reget (`yes`, `no`, and `yes`). The CHI seed is present
by direct GET. The CHI settled list is not that page. The panel stub
still stores `result` null and `status_at_stub` `active` on each market.
This harness does not copy the reget result onto the stub.

`markets?series_ticker=KXHIGHCHI&status=settled` and
`markets?series_ticker=KXHIGHNY&status=open` stay the honest 429 gaps.
Those artifacts are `too_many_requests` and have no market object. They
are not backfilled. The CHI open list cites four active tickers with an
empty `result`. Those tickers are not invented as settled markets.

## What this run does not claim

No invented settled `result`, depth, fills, or PnL. No Lee-Ready. No
`admit.py`. No live orders. No Logan keys. No Cap-SR reopen. No FQ
sibling reopen. No C3-RJ reopen. No C5-RJ reopen. No R3-P3 fee-arm
reopen. No Arm B. No ungate of S1, S2, or R2-P4. `settled_join_n`,
`occurrence_match_n`, and `admit_ready_flag` stay null until Examiner
after merge and sha verify and Clock admit. Examiner status stays
HOLD / `NOT_SCORED`. A later unit page is code verification only.
