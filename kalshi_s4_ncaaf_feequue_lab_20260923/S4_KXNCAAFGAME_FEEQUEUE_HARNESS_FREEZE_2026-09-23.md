# S4 KXNCAAFGAME FEE+QUEUE HONESTY HARNESS — FREEZE KERNEL 2026-09-23 (ET)

**Owner:** R&D Variants (harness freeze / implement) → Simulator → Examiner  
**Status:** FROZEN — Conductor slot after S5 PR#25 merge @`6626c6892298b015cf63688081545e27363226bc`  
**Cite:** Conductor 2026-09-23 leftover orthogonal; parent DR freeze `S4_KXNCAAFGAME_MEASUREMENT_FREEZE_KERNEL_2026-09-22.md`; panel stub `2026-09-22.s4-kxncaafgame-v0`  
**Repo:** `https://github.com/17thgreen/GPT-6-Astra-Deathmatch`  
**Packet ID:** S4-KXNCAAFGAME-FEEQUEUE-HARNESS  
**Feature family:** **NCAAF-FQ** (college football fee+queue honesty OOS) — ≠ Cap-SR / Cap-SR-FX / MVE-FL / F1–F3  
**Series:** `KXNCAAFGAME`  
**Conductor harness sha256 claim:** `3318204bf6e962f4f3372dad8c0f302e62d85c26b855de7369718654d0114728`  
**Conductor parent sha256 claim:** `9e6556c150c726b679ac8393f1f5338cf983489259b0f34cdedf221c030be795`  
**Checkout status:** The harness freeze was cited as already on the Conductor box. `lab/governance/astra/packets/` is absent in this checkout and those bytes were not attached. This file is the equivalent recreation. It is not asserted to equal the conductor sha256 claim. The recreation sha256 is recorded in `FROZEN_EXPERIMENT.json` and must not be edited after the hypothesis commit.  
**Hard rules:** Measurement-only. GET-only. No Logan keys. No live orders. No invent fills/PnL. No Q6-`000` retune. No QF reopen. No Cap-SR reopen. No `admit.py`. No R1-P2 challenger bakeoff. `maker_vs_taker_roi_delta`, `fresh_vs_stale_gap`, `settled_join_n`, `results`, and `pnl` stay null until Examiner after Clock admit.

---

## Why S4 (this slot)

S5 fill-vs-legs is merged. Cap-SR and Cap-SR-FX stay closed. Q7 Arm B stays killed. C1 empty-book stays `NOT_SCORED`. S4 is the college-football fee+queue honesty harness on public `KXNCAAFGAME` tape, without Logan keys.

---

## Intent (one knob)

Holding **R1-P1 feebook** and **R1-P5 rails** fixed, wire a fee+queue honesty harness that consumes the S4 panel stub (and later `panel_admitted.json`).

**One knob only:** honesty partition ∈ {`maker_vs_taker_native`, `content_fresh_vs_stale_bin`}.

**Not arms:** Lee-Ready; Q6 signal; Cap-SR; queue-fragility; R1-P2 challenger bakeoff; live order size.

---

## Pins

| Pin | Value |
|---|---|
| Parent freeze | `S4_KXNCAAFGAME_MEASUREMENT_FREEZE_KERNEL_2026-09-22.md`. Conductor claim sha256 `9e6556c150c726b679ac8393f1f5338cf983489259b0f34cdedf221c030be795`. Checkout recreation sha256 is in `FROZEN_EXPERIMENT.json` |
| Panel stub | `lab/astra-capture/s4-kxncaafgame/panel_stub.json` · panel_version `2026-09-22.s4-kxncaafgame-v0` · `admitted_at` **null**. Conductor claim sha256 `38167d11da5842bc4d39e6e7dcaab20a67294c735ba14d8bbeafde3154c6342a` (~113 events). Prefer `panel_admitted.json` when present. Checkout seed does not invent that cohort |
| Fee (FIXED) | `kalshi_feebook_lab_20260922/` @`22371178cb2663250b4762f328069571c48cb551` — import only |
| Rails (FIXED) | `kalshi_rails_lab_20260922/` @`6a28e0d6254327ea4e6451c781bec56215ac6cac` — import only |
| Capture | GET-only public — no Logan keys |
| Strategy | **None** |

---

## Arms (partition knob only)

| Arm | Name | Partition |
|---|---|---|
| **S4A0** | `maker_vs_taker_native` | Native `taker_*` fields only. Lee-Ready **REFUSED** on every input |
| **S4A1** | `content_fresh_vs_stale_bin` | Rails `content_fresh_flag` and queue-attribution bins only |

Both arms share the same fee and rails commits. Empty historical tape is allowed. Units may use synthetic rows for schema only. Synthetic rows are not panel fills and are not PnL.

---

## Scorecard fields (null now)

| Field | Meaning |
|---|---|
| `maker_vs_taker_roi_delta` | Native maker-versus-taker ROI gap |
| `fresh_vs_stale_gap` | Content-fresh versus stale gap |
| `settled_join_n` | Settled-join count |
| `results` | Examiner block |
| `pnl` | Examiner block |

All stay **null** in this freeze / EMPTY_RESULTS until Examiner after Clock admit.

---

## Lab deliverables (implement now)

New dir: `kalshi_s4_ncaaf_feequue_lab_20260923/` in the Astra repo:

- `EXPERIMENT_SPEC.md` + `FROZEN_EXPERIMENT.json` (`results` / `pnl` null)  
- Harness loads the panel stub and prefers `panel_admitted.json` when present  
- Bind feebook + rails imports; refuse fee literals and Lee-Ready  
- Unit tests: pin lock; stub load; S4A0 / S4A1 schema; null scorecard  
- First PR = **unit/instrument + stub join**; scorecard null  
- Do **not** mutate feebook / rails / Q / Cap-SR / Cap-SR-FX / C3 / C5 / R3-P3 / S5 labs

---

## Do-not-modify

1. No live orders / no Logan keys.  
2. No inventing fills or PnL.  
3. No Q6-`000` retune; no QF reopen; no Cap-SR reopen.  
4. No `admit.py`. No R1-P2 challenger bakeoff.  
5. Q7 Arm B stays killed. C1 empty-book stays closed.  
6. `results` / `pnl` null until Examiner opens.

---

## Dead-card / orthogonality (named)

| Card | Handling |
|---|---|
| Q7 Arm B KILL | **Do not reopen** |
| C1 empty-book `NOT_SCORED` | **Closed sibling** |
| Cap-SR / Cap-SR-FX | **Orthogonal** — do not edit |
| MVE-FL / S5 | **Orthogonal** — do not edit |
| F1–F3 | **Out** |
| QF reopen | **DENIED** |

---

## Frozen-at

Desk 2026-09-23 ET. Conductor slot after S5 PR#25. Variants owner: R&D Variants. Checkout recreation because the conductor-box file was not in the sandbox.
