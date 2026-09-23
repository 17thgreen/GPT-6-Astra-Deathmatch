# S5 KXMVECROSSCATEGORY settled-resolution join

September 23, 2026. This file is the hypothesis. It is committed before a
unit-test outcome is recorded. No figure in this document is a trading
result. This is measurement-only settled-resolution join. Feature family
S5-RJ. It is orthogonal to S5 FILLLEGS and to MVE-FL. It is not a reopen
of Cap-SR, C3-RJ, C5-RJ, R3P3-RJ, NHL-RJ, S4-RJ, or R2P3-RJ.

## Placement

The harness freeze committed verbatim is
`S5_KXMVECROSSCATEGORY_SETTLED_RESOLUTION_JOIN_HARNESS_FREEZE_2026-09-23.md`,
sha256
`cd264a4d41ef055d1cbca80a5dbe6756746211537fb24799dca9dde8980cb799`.
Those bytes are the attached conductor freeze. The same bytes sit in this
lab, in `S5_KXMVECROSSCATEGORY_SETTLED_RESOLUTION_JOIN_HARNESS/`, in
`lab/astra-science/kalshi_s5_kxmvecrosscategory_settled_join_lab_20260923/`, in
`packets/S5_KXMVECROSSCATEGORY_SETTLED_JOIN_HARNESS/`, and at
`lab/governance/astra/packets/S5_KXMVECROSSCATEGORY_SETTLED_RESOLUTION_JOIN_HARNESS_FREEZE_2026-09-23.md`.

Scout reget sha256
`33db60a50f2e7746315f4603b9f78a9260145cb49d0250e141471de46f4df9e3`
is `scout_settled_rejoin_S5_KXMVECROSSCATEGORY.json`. The freeze cites
`lab/governance/astra/packets/scout_s5_settled_rejoin_2026-09-23/`.
That directory holds the same scout bytes and the seed summary.

Seed summary sha256
`3bc4aa5f44d7d31295dfd25f7bac3a3e39463c237315e8228c3fcf434d08419a`
is `SEED_SETTLED_SUMMARY.json`.

Panel stub sha256
`4918b820d454c5f997ea100917859f7e9467d92933bed1bc8a55c81ab8ce5b8e`,
`panel_version` `2026-09-22.s5-kxmvecrosscategory-v0`, packet
`S5-KXMVECROSSCATEGORY-MEAS`. `admitted_at` is null. The same bytes are
already at `lab/astra-capture/s5-kxmvecrosscategory/panel_stub.json` and
are not rewritten. A governance copy is
`lab/governance/astra/packets/S5_KXMVECROSSCATEGORY_PANEL_STUB_2026-09-22.json`.
The stub has 21 events and 5 markets. Two stub markets stay
`status_observed` `active`. Three stay `finalized`. The stub has no
`result`. `results`, `pnl`, and `volume` are null. `panel_admitted.json`
is absent. This harness does not run `admit.py` and does not write
`admitted_at`.

Settled reget capture sha256
`91111f20586a1b684e430baa0e8b62a3fffc7d510de99e43bab7d213dfeb26da`
is `settled_reget_2026-09-23.json`. The same bytes are in this lab and
at `lab/astra-capture/s5-kxmvecrosscategory/settled_reget_2026-09-23.json`.
The capture object is the public list body: `cursor` plus `markets`.

Conductor ACCEPT sha256
`495675175589c08122bc57375dd8e7d00aea9f4a154df3aff086b015a2513a8c`
is `decision` ACCEPT and `implement` true. It is committed verbatim at
`packets/CONDUCTOR_ACCEPT_S5_KXMVECROSSCATEGORY_SETTLED_JOIN_HARNESS_2026-09-23.json`,
in `packets/S5_KXMVECROSSCATEGORY_SETTLED_JOIN_HARNESS/`, and in this lab.

Attached `FROZEN_EXPERIMENT.json` sha256
`4bb57f793e5eb6ed3fed664843e1ad00f2e204739e3014df96a56e342036b8b0`
keeps `results` and `pnl` null. Attached `results/EMPTY_RESULTS.json`
sha256
`9257b65bcb892cd5139fd25433cbe4b9a1704045fea86890bfa3e0ed56c1c88c`
keeps `results`, `pnl`, `settled_join_n`, `occurrence_match_n`, and
`admit_ready_flag` null.

`SOURCE_PINS.json`, when the harness source lands, lists those digests.
It does not contain the file bytes.

Starting ref is main at `b2c1639a77f62114572fd41182f8a3c5ef70cad1`.
Feebook `22371178cb2663250b4762f328069571c48cb551` and rails
`6a28e0d6254327ea4e6451c781bec56215ac6cac` stay fixed and are not loaded.
This join has no fee arm. The panel records series override
`quadratic_with_combo_maker_fees` / multiplier 1 as a cite only.

## One knob

`join_gate`:

| Arm | Gate |
|---|---|
| J0 | `nonempty_result_required` — Clock-admit readiness is defined only for settled markets whose official `result` is already non-empty on the reget |
| J1 | `occurrence_datetime_match` — when `occurrence_datetime` is present it must agree across scout, seed, and reget; when it is null, which is the honest state of this MVE cohort, the public clock is `expected_expiration_time`. This harness does not invent `occurrence_datetime` |

Both arms share the same panel parent and the same GET-only reget pins.

The scout pin `settled_nonempty_result_N` is 20. That pin is the
`GET /markets?series_ticker=KXMVECROSSCATEGORY&status=settled&limit=20`
cohort (`yes` 4, `no` 16). It is not `settled_join_n`. The settled list
HTTP status on that capture is 200 and the cursor is present. Markets
past that cursor are not invented. Earlier settled-list attempts, the
finalized list, and the events closed/settled list are `429_honest` and
are not backfilled. `KXMVECROSSCATEGORY-SHARD1` series GET is
`429_honest` and is not backfilled. The related fee-pin series
`KXMVESPORTSMULTIGAMEEXTENDED` settled list is HTTP 200 with N=20 as a
count pin only. Those markets are not in this reget and are not invented.
`occurrence_datetime` is null on all 20 settled rows. Each row has
`expected_expiration_time`. Parent panel seeds, five tickers, are
finalized with nonempty `result` `no` on single-ticker GETs stored in
the scout. That count is 5. Those five tickers are not on the settled
lim20 list. The panel stub is not rewritten with those results. Two stub
rows stay `status_observed` `active`. Three stay `finalized`. The stub
still has no `result`. This harness does not copy 20 into
`settled_join_n`.

## What this run does not claim

No invented settled `result`, depth, fills, or PnL. No Lee-Ready. No
`admit.py`. No live orders. No Logan keys. No Cap-SR reopen. No S5
FILLLEGS reopen. No MVE-FL reopen. No other FQ sibling reopen. No C3-RJ
reopen. No C5-RJ reopen. No R3P3-RJ reopen. No NHL-RJ reopen. No S4-RJ
reopen. No R2P3-RJ reopen. No Arm B. No ungate of S1, S2, or R2-P4. No
Conductor pulse cloud. `settled_join_n`, `occurrence_match_n`, and
`admit_ready_flag` stay null until Examiner after merge and sha verify
and Clock admit. Examiner status stays HOLD pre-PR. The attached hold
has `stub_ready` false. A later unit page is code verification only.
