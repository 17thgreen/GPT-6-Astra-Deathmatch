# R2P3 KXNFLPASSYDS settled-resolution join

September 23, 2026. This file is the hypothesis. It is committed before a
unit-test outcome is recorded. No figure in this document is a trading
result. This is measurement-only settled-resolution join. Feature family
R2P3-RJ. It is orthogonal to the R2-P3 prop-ladder harness and to
PASSYDS-PROP. It is not a reopen of Cap-SR, C3-RJ, C5-RJ, R3P3-RJ,
NHL-RJ, or S4-RJ.

## Placement

The harness freeze committed verbatim is
`R2P3_KXNFLPASSYDS_SETTLED_RESOLUTION_JOIN_HARNESS_FREEZE_2026-09-23.md`,
sha256
`9ad3b0112243c1020aec2bd6ef0df15011b065c30aa691a988da02eb08be1e0b`.
Those bytes are the attached conductor freeze. The same bytes sit in this
lab, in `R2P3_KXNFLPASSYDS_SETTLED_RESOLUTION_JOIN_HARNESS/`, in
`lab/astra-science/kalshi_r2p3_kxnflpassyds_settled_join_lab_20260923/`, in
`packets/R2P3_KXNFLPASSYDS_SETTLED_JOIN_HARNESS/`, and at
`lab/governance/astra/packets/R2P3_KXNFLPASSYDS_SETTLED_RESOLUTION_JOIN_HARNESS_FREEZE_2026-09-23.md`.

Scout reget sha256
`2c3664ac240887026076a84e451ca798e0c2d10d42bdaf61a9a83844881681e5`
is `scout_settled_rejoin_R2P3_KXNFLPASSYDS.json`. The freeze cites
`lab/governance/astra/packets/scout_r2p3_settled_rejoin_2026-09-23/`.
That directory holds the same scout bytes and the seed summary.

Seed summary sha256
`534a617bc3f18be501c07237d261e945b1bcf0301ac956cddae46e0431b75cd3`
is `SEED_SETTLED_SUMMARY.json`.

Panel stub sha256
`70e879e8738d033f392d821849dee3537af3e7b8a916670779d238f78ce098be`,
`panel_version` `2026-09-22.r2-p3-prop-slate-v0`, packet
`R2-P3-KXNFLPASSYDS-MEAS`. `admitted_at` is null. The same bytes are
already at `lab/astra-capture/r2-p3-prop-slate/panel_stub.json` and at
`packets/R2_P3_PROP_LADDER_HARNESS/panel_stub.json` and are not rewritten.
A governance copy is
`lab/governance/astra/packets/R2_P3_PROP_SLATE_PANEL_STUB_2026-09-22.json`.
The stub has 6 Sunday `26SEP27` events and empty `market_tickers`.
`results`, `pnl`, and `volume` are null. `panel_admitted.json` is absent.
This harness does not run `admit.py` and does not write `admitted_at`.

Settled reget capture sha256
`2ce8426edb4ee5053f63bf2fe1439dbd046978eb76afa1e0537b17cca9b8b0e4`
is `settled_reget_2026-09-23.json`. The same bytes are in this lab and
at `lab/astra-capture/r2-p3-prop-slate/settled_reget_2026-09-23.json`.

Conductor ACCEPT sha256
`e5218cf2511607211ec1d825a9dad36abaee3d9cfda24488524c3d6bcbe3a565`
is `decision` ACCEPT and `implement` true. It is committed verbatim at
`packets/CONDUCTOR_ACCEPT_R2P3_KXNFLPASSYDS_SETTLED_JOIN_HARNESS_2026-09-23.json`,
in `packets/R2P3_KXNFLPASSYDS_SETTLED_JOIN_HARNESS/`, and in this lab.

Attached `FROZEN_EXPERIMENT.json` sha256
`44c801e306ffc22325b7e689a9dadbdb8774f89fd39a14892aa7de965f9edd21`
keeps `results` and `pnl` null. Attached `results/EMPTY_RESULTS.json`
sha256
`5a41a8295708e824757fdd51a680a660fdbbf49f2dc68a17785f8d3a9095cd46`
keeps `results`, `pnl`, `settled_join_n`, `occurrence_match_n`, and
`admit_ready_flag` null.

`SOURCE_PINS.json`, when the harness source lands, lists those digests.
It does not contain the file bytes.

Starting ref is main at `aeff380b29dbe89b16da58f9e15e58415b42b147`.
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

The scout pin `settled_nonempty_result_N` is 20. That pin is the
prior-weekend SEP20/SEP21 cohort from
`GET /markets?series_ticker=KXNFLPASSYDS&status=settled&limit=20`
(`yes` 6, `no` 14). It is not `settled_join_n`. The settled list HTTP
status on that capture is 200 and the cursor is present. Markets past
that cursor are not invented. The finalized list and the events
closed/settled lists are `429_honest` and are not backfilled. The close
window `min_close_ts`/`max_close_ts` query is `400_honest` and is not
backfilled. Parent prop-ladder SEP27 seeds
`KXNFLPASSYDS-26SEP27LACBUF-BUFJALLEN17-150`,
`KXNFLPASSYDS-26SEP27LACBUF-BUFJALLEN17-175`,
`KXNFLPASSYDS-26SEP27BALDAL-DALDPRESCOTT4-175`, and
`KXNFLPASSYDS-26SEP27BALDAL-DALDPRESCOTT4-200` stay active with a null
`result`. Their finalized nonempty count is 0. The panel stub
`market_tickers` stay empty. The reget records those four statuses and
null results. It does not carry an `occurrence_datetime` for them, and
this harness does not invent one. ATL@GB SEP24 stays excluded. The panel
stub has no settled `result`. This harness does not copy a reget
`result` onto the stub and does not copy 20 into `settled_join_n`.

## What this run does not claim

No invented settled `result`, depth, fills, or PnL. No Lee-Ready. No
`admit.py`. No live orders. No Logan keys. No Cap-SR reopen. No R2-P3
prop-ladder reopen. No PASSYDS-PROP reopen. No other FQ sibling reopen.
No C3-RJ reopen. No C5-RJ reopen. No R3P3-RJ reopen. No NHL-RJ reopen.
No S4-RJ reopen. No Arm B. No ungate of S1, S2, or R2-P4. No Conductor
pulse cloud. `settled_join_n`, `occurrence_match_n`, and
`admit_ready_flag` stay null until Examiner after merge and sha verify
and Clock admit. Examiner status stays HOLD pre-PR. The attached hold
has `stub_ready` false. A later unit page is code verification only.
