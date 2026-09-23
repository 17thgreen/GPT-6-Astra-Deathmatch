# S4 — KXNCAAFGAME fee+queue honesty measurement kernel — FREEZE 2026-09-22 (ET)

**Packet ID:** S4-KXNCAAFGAME-MEAS  
**Scout series:** `KXNCAAFGAME` (college football game moneyline)  
**Owner (freeze):** Deep Research  
**Implementer (later):** Collector (panel) → Simulator (fee+queue honesty harness) → Examiner (Kalshi)  
**Reviewer:** Conductor triage; Adversary on Lee-Ready, invented fills, and live orders  
**Status:** **FROZEN** — results/pnl **null** (not run)  
**Cite:** Conductor maximize kick 2026-09-22 (S5 preferred that cycle; S4 remains TRY for a later football-OOS freeze); R1-P1 feebook; R1-P5 rails  
**Conductor sha256 claim:** `9e6556c150c726b679ac8393f1f5338cf983489259b0f34cdedf221c030be795`  
**Checkout status:** `lab/governance/astra/packets/` is absent and the conductor-box bytes were not attached to the implement run. This file is the lab recreation of that kernel. It is not asserted to equal the conductor sha256 claim. The recreation sha256 is recorded in `FROZEN_EXPERIMENT.json`.  
**Repo (lab dir):** `17thgreen/GPT-6-Astra-Deathmatch` → `kalshi_s4_ncaaf_feequue_lab_20260923/` (do not mutate Q / Cap-SR / Cap-SR-FX / C3 / C5 / R3-P3 / S5 / feebook / rails labs)  
**Hard rules:** Measurement-only college-football fee+queue honesty. GET-only. No Logan keys. No live orders. No invented fills or PnL. No Q6-`000` retune. No queue-fragility reopen. No Cap-SR reopen. No `admit.py`. No R1-P2 challenger bakeoff. Lee-Ready is refused. Must bind R1-P1 + R1-P5.

---

## Intent (one measurement kernel)

Do public `KXNCAAFGAME` books stress the same fee and queue honesty instruments as `000`, under a college-football clock, when maker versus taker is read only from native `taker_*` fields and freshness is read only from rails content-fresh and queue-attribution bins?

**Not a strategy.** Not a retune of the Q6 candidate. Not an Examiner score. Feature family **NCAAF-FQ**. Orthogonal to Cap-SR, Cap-SR-FX, MVE-FL, and F1–F3.

---

## Dead-card / live-pin overlap (named)

| Pin / card | Overlap | Handling |
|---|---|---|
| Q6-`000` KEEP | **None** — college slate, not the NFL week allocator | Do not retune `000` |
| Q7 Arm B KILL | **Nearest dead card** | Do not reopen |
| C1 empty-book `NOT_SCORED` | **Closed sibling** | Do not ungate; do not fill empty books |
| Cap-SR / Cap-SR-FX | **Orthogonal** | Soft-policy and fixture stress stay closed |
| MVE-FL (S5) | **Orthogonal** | Combo fill-vs-legs is a different knob |
| F1–F3 / Gauntlet | **Out** | Not this kernel |
| R1-P2 challenger bakeoff | **Denied** | Do not open |
| Queue-fragility QF0/QF1/QF2 | **No reopen** | Import rails bins only |
| Lee-Ready | **Refused** | Native `taker_*` fields only |

---

## Mandatory instrument pins

| Dep | Pin | Rule |
|---|---|---|
| Fee | R1-P1 `kalshi_feebook_lab_20260922/` @ `22371178cb2663250b4762f328069571c48cb551` | Import only. No shadow `0.0175` / `0.07` literals |
| Rails | R1-P5 `kalshi_rails_lab_20260922/` @ `6a28e0d6254327ea4e6451c781bec56215ac6cac` | `content_fresh_flag`, `queue_attribution_bin`, maker-credit floor refuse |
| Capture | GET-only public elections host | No signed trading host. No Logan keys |
| Panel | `lab/astra-capture/s4-kxncaafgame/panel_stub.json` | `panel_version` `2026-09-22.s4-kxncaafgame-v0`. `admitted_at` null. Prefer `panel_admitted.json` when it appears |

**Conductor panel-stub sha256 claim:** `38167d11da5842bc4d39e6e7dcaab20a67294c735ba14d8bbeafde3154c6342a` (~113 events). Those bytes were not in this checkout. The committed stub is a schema seed with an empty event list. It does not invent the 113-event cohort.

**Refuse gate:** Lee-Ready on any input. Completed-profit label without the feebook channel. Invented fills, invented settlement, or a non-null scorecard before Examiner.

---

## Measurement objects (pre-settlement)

For each later-admitted `KXNCAAFGAME` event:

1. **Native taker partition:** `taker_outcome_side` / `taker_book_side` / `taker_side` only. Lee-Ready stays `REFUSED`.  
2. **Rails freshness bin:** `content_fresh_flag` and `queue_attribution_bin` only.  
3. **Fee channel:** R1-P1 `order_fee` as a pin check. The delta is not a scorecard field in this kernel.

**Explicitly null until Examiner:** `maker_vs_taker_roi_delta`, `fresh_vs_stale_gap`, `settled_join_n`, `results`, `pnl`.

---

## Panel / cohort (freeze rule — admit is Collector)

- Series filter: `KXNCAAFGAME`.  
- Suggested panel_version: `2026-09-22.s4-kxncaafgame-v0`.  
- `admit.py` is not run. Do not backfill.  
- Conductor described about 113 events. This recreation does not synthesize them.

---

## Arms (one knob — harness)

One knob: honesty partition ∈ {`maker_vs_taker_native`, `content_fresh_vs_stale_bin`} with feebook and rails commits fixed.

**Not arms:** Lee-Ready, Q6 signal, Cap-SR, queue-fragility, R1-P2 challenger, live maker sizes.

---

## Do-not-modify

1. No live orders. No Logan keys. No `admit.py`.  
2. No invented fills, settlement, or PnL.  
3. No Q6-`000` retune. No Q7 Arm B reopen. No QF reopen. No Cap-SR reopen.  
4. No R1-P2 challenger bakeoff.  
5. Do not mutate feebook, rails, Q, Cap-SR, Cap-SR-FX, C3, C5, R3-P3, or S5 labs.  
6. `results` / `pnl` null until Examiner opens after Clock admit.

---

## Empty results

Scorecard fields stay null in `FROZEN_EXPERIMENT.json` and `results/EMPTY_RESULTS.json`.

---

## Done =

Kernel text on disk for the implement seat. Conductor-box bytes were not in the checkout, so this recreation is labeled as such. Implementation / admit / Examiner score = later seats.

## Frozen-at

`2026-09-22T23:59:00+00:00` UTC is the conductor-cycle cite. The checkout recreation was written 2026-09-23 because the governance tree and the conductor file were absent.
Deep Research freeze. S4 stays orthogonal to the S5 pick.
