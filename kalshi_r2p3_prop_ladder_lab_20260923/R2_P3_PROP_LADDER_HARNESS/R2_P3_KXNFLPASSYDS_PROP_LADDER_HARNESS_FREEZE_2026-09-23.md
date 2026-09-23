# R2-P3 KXNFLPASSYDS PROP-LADDER HARNESS — FREEZE KERNEL 2026-09-23 (ET)

**Owner:** R&D Variants (harness freeze / implement) → Simulator → Examiner  
**Status:** FROZEN — Conductor MAXIMIZE NEXT after S4 PR26 merge @`d7584dd4`  
**Cite:** Parent DR freeze `R2-P3_KXNFLPASSYDS_MEASUREMENT_FREEZE_KERNEL_2026-09-22.md` (sha256 `a30108f658359590e170c73ea00d1a1f0852d5751cb15c9f2a9c6389f4dd3eaa`); panel stub `2026-09-22.r2-p3-prop-slate-v0` (sha256 `70e879e8738d033f392d821849dee3537af3e7b8a916670779d238f78ce098be`; admitted_at null; 6 events; volume null)  
**Repo:** `https://github.com/17thgreen/GPT-6-Astra-Deathmatch`  
**Packet ID:** R2-P3-KXNFLPASSYDS-PROP-LADDER-HARNESS  
**Feature family:** **PROP-LQ** (NFL yards multi-strike fee+queue honesty) — ≠ Cap-SR / Cap-SR-FX / MVE-FL / NCAAF-FQ / F1–F3  
**Nearest dead card:** Q6-`000` KEEP (medium calendar overlap, different contracts); Q7 Arm B KILL (CEM-001) closed — no pair-check reopen.  
**Hard rules:** Measurement-only. GET-only. No Logan keys. No live orders. No invented PnL. No Q6-`000` retune. No QF reopen. No Cap-SR reopen. No ATL@GB. No `admit.py`. `results`/`pnl` null until Examiner after Clock admit.

## Why R2-P3 (oldest leftover this slot)

Excluded: S4 NCAAF-FQ just merged; Cap-SR/FX + S5 MVE-FL merged; S1 empty-events deferred; S2+R2-P4 WAIT until C1 T−7d; R3-P2 keys HOLD; QF no reopen.

R2-P3 is the oldest remaining FREEZE-ACCEPTED Scout TRY kernel with a non-empty panel seed (6 events on Sun 2026-09-27 LAC@BUF + BAL@DAL) that is GET-only NFL **prop-ladder** OOS vs binary ML `000`.

## Intent (one knob)

Holding **R1-P1 feebook** and **R1-P5 rails** fixed, wire a prop-ladder fee+queue honesty harness on the R2-P3 panel stub (prefer `panel_admitted.json` when present): per strike TOB mid + fee-aware touch + rails freshness/queue labels; test whether strike mids share one player-mean latent via cross-strike residual after a monotone fit.

**One knob only:** residual monotone family ∈ {`isotonic`, `logit_monotone`} with feebook+rails fixed.

**Not arms:** markout horizon (leave null until Examiner); `000` retune; Cap-SR; ATL@GB enrichment; inventing fills when tape empty; Lee-Ready.

## Pins

| Pin | Value |
|---|---|
| Parent freeze | sha256 `a30108f658359590e170c73ea00d1a1f0852d5751cb15c9f2a9c6389f4dd3eaa` |
| Panel stub | `lab/astra-capture/r2-p3-prop-slate/panel_stub.json` · `2026-09-22.r2-p3-prop-slate-v0` · sha256 `70e879e8738d033f392d821849dee3537af3e7b8a916670779d238f78ce098be` · `admitted_at` **null** · 6 events · volume fields null |
| Fee (FIXED) | `kalshi_feebook_lab_20260922/` @`22371178cb2663250b4762f328069571c48cb551` |
| Rails (FIXED) | `kalshi_rails_lab_20260922/` @`6a28e0d6254327ea4e6451c781bec56215ac6cac` |
| Capture | GET-only public — no trading host; no Logan keys |
| Slate | LAC@BUF + BAL@DAL 2026-09-27 only — **NOT ATL@GB** |
| Strategy | **None** — measurement contrast only |

## Arms

| Arm | Name | Slice |
|---|---|---|
| **R2P3A0** | Isotonic residual | Monotone isotonic fit → cross-strike residual; Lee-Ready **REFUSED** |
| **R2P3A1** | Logit-monotone residual | Logit-monotone family → same residual + rails labels; no fee invent |

## Dead-card / live-pin overlap (named)

| Pin / card | Overlap | Handling |
|---|---|---|
| Q6-`000` KEEP | Medium — same NFL calendar; different contracts | Contrast fee+queue honesty only; **no** `000` retune |
| Q7 Arm B KILL | None | Do not reopen CEM-001 |
| Cap-SR / Cap-SR-FX | None (merged, orthogonal) | Do not reopen |
| S4 NCAAF-FQ / S5 MVE-FL | Just merged; distinct series | Do not mutate those labs |
| S2 + R2-P4 | WAIT on C1 T−7d | Stay queued; do not expand this packet |
| S1 empty-events | Deferred | Do not mutate |
| QF / Cap-SR soft reopen | Denied | Stay closed |
| ATL@GB | Explicit exclude | REFUSE enrichment |

## Scorecard fields (null now)

`cross_strike_residual_rms`, `latent_fit_fragmentation`, `maker_credit_floor_zero_n`, `fresh_strike_n`, `settled_join_n`, `results`, `pnl` — null until Clock admit + Examiner. Markout horizons stay null (not the knob).

## Lab dir

`kalshi_r2p3_prop_ladder_lab_20260923/` (do not mutate Q / Cap-SR / Cap-SR-FX / C3 / C5 / R3-P3 / S4 / S5 / feebook / rails labs).

## Integrity (Clock gate)

Commit the **attached** Conductor-box freeze / parent / panel bytes **verbatim**. Pin digests to `sha256sum` of those attached files. **Refuse labeled recreations.** Empty-schema panel seeds are forbidden when the authentic stub (6 events) is attached. Prefer `panel_admitted.json` when present; do not invent cohort / volume / fills.

## Merge gates

Units green; `results`/`pnl` null; Examiner stub_ready NOT_SCORED after merge.
