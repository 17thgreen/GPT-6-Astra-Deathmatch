# NHL KXNHLGAME settled-resolution join

September 23, 2026. This file is the hypothesis. It is committed before a
unit-test outcome is recorded. No figure in this document is a trading
result. This is measurement-only settled-resolution join. Feature family
NHL-RJ. It is orthogonal to NHL-FQ. It is not a reopen of Cap-SR, C3-RJ,
C5-RJ, or R3P3-RJ.

## Placement

The harness freeze committed verbatim is
`NHL_KXNHLGAME_SETTLED_RESOLUTION_JOIN_HARNESS_FREEZE_2026-09-23.md`, sha256
`d1f71cea6df8f6c5a9fac6f9d1aa418ce61aa650794f22b400a01c4f3fd45810`.
Those bytes are the attached conductor freeze. The same bytes sit in this
lab, in `NHL_KXNHLGAME_SETTLED_RESOLUTION_JOIN_HARNESS/`, in
`lab/astra-science/kalshi_kxnhlgame_settled_join_lab_20260923/`, in
`packets/NHL_KXNHLGAME_SETTLED_JOIN_HARNESS/`, and at
`lab/governance/astra/packets/NHL_KXNHLGAME_SETTLED_RESOLUTION_JOIN_HARNESS_FREEZE_2026-09-23.md`.

Scout reget sha256
`99a7f90564ee2150f5edef4efafb7ccb954b87036e0b43f29ff7dc6ed104706f`
is `scout_settled_rejoin_NHL_KXNHLGAME.json`. The freeze cites
`lab/governance/astra/packets/scout_nhl_settled_rejoin_2026-09-23/`.
That directory holds the same scout bytes and the seed summary.

Seed summary sha256
`794e148df5927c64d08b4578b47a7453589f02872af65880922bcb9273194a1a`
is `SEED_SETTLED_SUMMARY.json`.

Panel stub sha256
`60d183e7bdcf25adbc94eeeb3bb361b5232c19c0fe3e6a115f45ab3fcb100c79`,
`panel_version` `2026-09-23.c2-kxnhlgame-v0`, packet
`C2-KXNHLGAME-FEEQUEUE-HARNESS`. `admitted_at` is null. The same bytes
are already at `lab/astra-capture/c2-kxnhlgame/panel_stub.json` and at
`packets/C2_KXNHLGAME_PANEL_STUB_2026-09-23.json` and are not rewritten.
A governance copy is
`lab/governance/astra/packets/C2_KXNHLGAME_PANEL_STUB_2026-09-23.json`.
`panel_admitted.json` is absent. This harness does not run `admit.py`
and does not write `admitted_at`.

Settled reget capture sha256
`8d597578bc65ea14ab1cbf5aa3c6d121d61431078a755b8419c815aa1d354df0`
is `settled_reget_2026-09-23.json`. The same bytes are in this lab and
at `lab/astra-capture/c2-kxnhlgame/settled_reget_2026-09-23.json`.

Conductor ACCEPT sha256
`ce82d9347c8af6666d96fb5c63be7693f4672306639ce4ba2360ba231c01e698`
is `decision` ACCEPT and `implement` true. It is committed verbatim at
`packets/NHL_KXNHLGAME_SETTLED_JOIN_HARNESS/CONDUCTOR_ACCEPT_NHL_KXNHLGAME_SETTLED_JOIN_HARNESS_2026-09-23.json`
and in this lab.

Attached `FROZEN_EXPERIMENT.json` sha256
`a882ab8e410b6b5a77b60aa0225dcb932c0a1b0b3bcc692a02a5cfa23b81bd42`
keeps `results` and `pnl` null. Attached `results/EMPTY_RESULTS.json`
sha256
`cc28e226979959d417ea1b7c6a05c87e6776e96489d57f793249bc42f912934f`
keeps `results`, `pnl`, `settled_join_n`, `occurrence_match_n`, and
`admit_ready_flag` null.

`SOURCE_PINS.json` lists those digests. It does not contain the file
bytes.

Starting ref is main at `2fce8642d1b1961cbe0ef60fae1411cd8906f31a`.
Feebook `22371178cb2663250b4762f328069571c48cb551` and rails
`6a28e0d6254327ea4e6451c781bec56215ac6cac` stay fixed and are not loaded.
This join has no fee arm.

## One knob

`join_gate`:

| Arm | Gate |
|---|---|
| J0 | `nonempty_result_required` — Clock-admit readiness is defined only for settled markets whose official `result` is already non-empty on the reget |
| J1 | `occurrence_datetime_match` — `occurrence_datetime` on each settled single-market GET matches the scout reget and the seed summary |

Both arms share the same panel parent and the same GET-only reget pins.

The scout pin `settled_nonempty_result_N` is 17. That pin is the
overnight SEP22 single-market cohort. It is not `settled_join_n`. The
series list `status=settled|finalized|open` is `429_honest` and is not
backfilled. The events settled list is the same honest gap. Parent FQ
SEP26 seeds `KXNHLGAME-26SEP26TBFLA-TB`,
`KXNHLGAME-26SEP26TBFLA-FLA`, and `KXNHLGAME-26SEP26COLUTA-UTA` stay
active with an empty `result`. Their finalized nonempty count is 0.
The panel stub `result` stays empty. This harness does not copy a
reget `result` onto the stub and does not copy 17 into `settled_join_n`.

## What this run does not claim

No invented settled `result`, depth, fills, or PnL. No Lee-Ready. No
`admit.py`. No live orders. No Logan keys. No Cap-SR reopen. No NHL-FQ
reopen. No other FQ sibling reopen. No C3-RJ reopen. No C5-RJ reopen.
No R3P3-RJ reopen. No Arm B. No ungate of S1, S2, or R2-P4.
`settled_join_n`, `occurrence_match_n`, and `admit_ready_flag` stay null
until Examiner after merge and sha verify and Clock admit. Examiner
status stays HOLD pre-PR. A later unit page is code verification only.
