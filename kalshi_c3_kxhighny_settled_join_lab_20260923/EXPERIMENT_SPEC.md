# C3 KXHIGHNY settled-resolution join

September 23, 2026. This file is the hypothesis. It is committed before a
unit-test outcome is recorded. No figure in this document is a trading
result. This is measurement-only settled-resolution join. Feature family
C3-RJ. It is not a reopen of the C3 bordering-strike algebra lab.

## Placement

The harness freeze committed verbatim is
`C3_KXHIGHNY_SETTLED_RESOLUTION_JOIN_HARNESS_FREEZE_2026-09-23.md`, sha256
`56adcf592239b028aaa8bcffbf09815115b8454f78db39b43c578e64c160a4d5`.
Those bytes are the attached conductor freeze. The same bytes sit at the
lab root and in `C3_KXHIGHNY_SETTLED_RESOLUTION_JOIN_HARNESS/`.

Scout reget sha256
`e8950352745007d3cb565050161430807fa5de70d15321bb00bede6ca9ac18ee`
is `scout_settled_rejoin_C3_KXHIGHNY.json`. The freeze cites
`lab/governance/astra/packets/scout_c3_settled_rejoin_2026-09-23/`.
That governance tree is absent in this checkout. The attached bytes are
in this lab.

Seed summary sha256
`b32bbf3200649bcea4fb61a98a4869d5123060a57702a9327262cccbc8e1ca93`
is `SEED_SETTLED_SUMMARY.json`.

Panel stub sha256
`2a5da7fe85ca1adc6b7c4dcf9e09ed5c6bb62be6b5c9b42731e36e31d1e8dfea`,
`panel_version` `2026-09-22.c3-kxhighny-v0`, packet
`C3-KXHIGHNY-MEAS`. `admitted_at` is null on the stub, on each event,
and on each market. The same bytes are already at
`lab/astra-capture/c3-kxhighny/panel_stub.json` and are not rewritten.
`panel_admitted.json` is absent. This harness does not run `admit.py`
and does not write `admitted_at`.

Settled reget capture sha256
`0055faae508ba034eb49a12d52713566cbfe20bfbfbd2a16203ef350152ac24a`
is `settled_reget_2026-09-23.json`. The freeze cites
`lab/astra-capture/c3-kxhighny/settled_reget_2026-09-23.json`. The
attached bytes are committed in this lab. The capture directory's
existing `panel_stub.json` is left as it was.

Conductor ACCEPT sha256
`9adb77ed01fd9ccb894564efa9d5534d2edf189365ca0852fff49dafd3598d69`
is `decision` ACCEPT and `implement` true. It is committed verbatim.

Attached `FROZEN_EXPERIMENT.json` sha256
`10f75f008f6fb870e212b81f9913b09ab06337973e850d36796f336331d33c23`
keeps `results` and `pnl` null. Attached `results/EMPTY_RESULTS.json`
sha256
`48e5916fff57563d14a6a84b8c6c0ed2515c3172066d565e5a18933faf02f4e6`
keeps `results`, `pnl`, `settled_join_n`, `occurrence_match_n`, and
`admit_ready_flag` null.

`SOURCE_PINS.json` lists those digests. It does not contain the file
bytes.

Starting ref is main at `82bf7bb99bcc618b912255cc24022b23f9f15047`
(ETH-FQ). Feebook `22371178cb2663250b4762f328069571c48cb551` and rails
`6a28e0d6254327ea4e6451c781bec56215ac6cac` stay fixed and are not loaded.
This join has no fee arm.

## One knob

`join_gate`:

| Arm | Gate |
|---|---|
| J0 | `nonempty_result_required` — Clock-admit readiness is defined only for settled markets whose official `result` is already non-empty on the reget |
| J1 | `occurrence_datetime_match` — SoT `occurrence_datetime` on the reget matches the seed summary and the panel stub for that ticker |

Both arms share the same panel parent and the same GET-only reget pins.

The scout pin `settled_nonempty_result_N` is 4: three finalized NY SEP22
markets and one finalized CHI SEP22 market. `KXHIGHNY-26SEP23-B67.5`
stays `active` with an empty `result`. `KXHIGHCHI-26SEP22-B66.5` is the
honest gap: reget key `market_KXHIGHCHI_26SEP22_B66_5.json` has error
code `too_many_requests` and no market object. That gap is not backfilled.

## What this run does not claim

No invented settled `result`, depth, fills, or PnL. No Lee-Ready. No
`admit.py`. No live orders. No Logan keys. No Cap-SR reopen. No FQ
sibling reopen, including ETH-FQ. No C3 bordering reopen. No Arm B.
No ungate of S1, S2, or R2-P4. `settled_join_n`, `occurrence_match_n`,
and `admit_ready_flag` stay null until Examiner after merge and sha
verify and Clock admit. Examiner status stays HOLD / `NOT_SCORED`.
A later unit page is code verification only.
