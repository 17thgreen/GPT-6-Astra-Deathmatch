# S4 KXNCAAFGAME settled-resolution join

September 23, 2026. This file is the hypothesis. It is committed before a
unit-test outcome is recorded. No figure in this document is a trading
result. This is measurement-only settled-resolution join. Feature family
S4-RJ. It is orthogonal to S4-FQ and NCAAF-FQ. It is not a reopen of
Cap-SR, C3-RJ, C5-RJ, R3P3-RJ, or NHL-RJ.

## Placement

The harness freeze committed verbatim is
`S4_KXNCAAFGAME_SETTLED_RESOLUTION_JOIN_HARNESS_FREEZE_2026-09-23.md`, sha256
`3a8e8ba52edd6acdc342c6a2faabb08665fe8a7a76e1b28af1c8e18850b03d99`.
Those bytes are the attached conductor freeze. The same bytes sit in this
lab, in `S4_KXNCAAFGAME_SETTLED_RESOLUTION_JOIN_HARNESS/`, in
`lab/astra-science/kalshi_kxncaafgame_settled_join_lab_20260923/`, in
`packets/S4_KXNCAAFGAME_SETTLED_JOIN_HARNESS/`, and at
`lab/governance/astra/packets/S4_KXNCAAFGAME_SETTLED_RESOLUTION_JOIN_HARNESS_FREEZE_2026-09-23.md`.

Scout reget sha256
`57fa0b28325ac13015f49521a87661b3cc064d22a13cf960f4fcdfd9badaa3dc`
is `scout_settled_rejoin_S4_KXNCAAFGAME.json`. The freeze cites
`lab/governance/astra/packets/scout_s4_settled_rejoin_2026-09-23/`.
That directory holds the same scout bytes and the seed summary.

Seed summary sha256
`9e67cd16f3ec6536d5dae3fe07de6e6b073c1c8d1adc9bb7e9297090ef567ce1`
is `SEED_SETTLED_SUMMARY.json`.

Panel stub sha256
`38167d11da5842bc4d39e6e7dcaab20a67294c735ba14d8bbeafde3154c6342a`,
`panel_version` `2026-09-22.s4-kxncaafgame-v0`, packet
`S4-KXNCAAFGAME-MEAS`. `admitted_at` is null. The same bytes are already
at `lab/astra-capture/s4-kxncaafgame/panel_stub.json` and are not
rewritten. A governance copy is
`lab/governance/astra/packets/S4_KXNCAAFGAME_PANEL_STUB_2026-09-22.json`.
The stub has 113 Saturday `26SEP26` events and 226 market tickers nested
on those events. It has no top-level `markets` array. `results`, `pnl`,
and `volume` are null. `panel_admitted.json` is absent. This harness
does not run `admit.py` and does not write `admitted_at`.

Settled reget capture sha256
`5bb0acfaa429e2ec1ad22e2e35e296540ac5b8e66eba4df6a0b2419d43257528`
is `settled_reget_2026-09-23.json`. The same bytes are in this lab and
at `lab/astra-capture/s4-kxncaafgame/settled_reget_2026-09-23.json`.

Conductor ACCEPT sha256
`87bb8d44e8ac50099cc66d0469dcd4a5cfafb78d92dd24e7a218100a6254da4a`
is `decision` ACCEPT and `implement` true. It is committed verbatim at
`packets/S4_KXNCAAFGAME_SETTLED_JOIN_HARNESS/CONDUCTOR_ACCEPT_S4_KXNCAAFGAME_SETTLED_JOIN_HARNESS_2026-09-23.json`
and in this lab.

Attached `FROZEN_EXPERIMENT.json` sha256
`273c59f2af1d18c840121923f07c3d557abb5b8b1a0fefa9bdb048ce89fc6abb`
keeps `results` and `pnl` null. Attached `results/EMPTY_RESULTS.json`
sha256
`4a67cd4f8d62bbffc7d2b3f7acdc1639dc01cbab058b86a8e8c74fe56da69e43`
keeps `results`, `pnl`, `settled_join_n`, `occurrence_match_n`, and
`admit_ready_flag` null.

`SOURCE_PINS.json`, when the harness source lands, lists those digests.
It does not contain the file bytes.

Starting ref is main at `b450e780fd9752887579ee8d217b6dee76d918f8`.
Feebook `22371178cb2663250b4762f328069571c48cb551` and rails
`6a28e0d6254327ea4e6451c781bec56215ac6cac` stay fixed and are not loaded.
This join has no fee arm.

## One knob

`join_gate`:

| Arm | Gate |
|---|---|
| J0 | `nonempty_result_required` — Clock-admit readiness is defined only for settled markets whose official `result` is already non-empty on the reget |
| J1 | `occurrence_datetime_match` — `occurrence_datetime` on each settled scout row matches the seed summary and the settled reget |

Both arms share the same panel parent and the same GET-only reget pins.

The scout pin `settled_nonempty_result_N` is 18. That pin is the
prior-weekend SEP05/SEP12/SEP19 cohort from event embeds and
single-market GETs. It is not `settled_join_n`. The series list
`status=settled|finalized|open` is `429_honest` and is not backfilled.
The events settled list is the same honest gap. Twelve named event and
market GETs in the scout `honest_gaps` stay `not_found` or
`too_many_requests`. Parent FQ SEP26 seeds
`KXNCAAFGAME-26SEP26BUCKPITT-PITT`,
`KXNCAAFGAME-26SEP26BUCKPITT-BUCK`, and
`KXNCAAFGAME-26SEP26TEXTENN-TEX` stay active with a null `result`.
Their finalized nonempty count is 0. The reget records those three
statuses and null results. It does not carry an `occurrence_datetime`
for them, and this harness does not invent one. The panel stub has no
settled `result`. This harness does not copy a reget `result` onto the
stub and does not copy 18 into `settled_join_n`.

## What this run does not claim

No invented settled `result`, depth, fills, or PnL. No Lee-Ready. No
`admit.py`. No live orders. No Logan keys. No Cap-SR reopen. No S4-FQ
or NCAAF-FQ reopen. No other FQ sibling reopen. No C3-RJ reopen. No
C5-RJ reopen. No R3P3-RJ reopen. No NHL-RJ reopen. No Arm B. No ungate
of S1, S2, or R2-P4. No Conductor pulse cloud. `settled_join_n`,
`occurrence_match_n`, and `admit_ready_flag` stay null until Examiner
after merge and sha verify and Clock admit. Examiner status stays HOLD
pre-PR. The attached hold has `stub_ready` false. A later unit page is
code verification only.
