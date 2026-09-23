# C5 KXBTC15M FEE+QUEUE HONESTY HARNESS — FREEZE KERNEL 2026-09-23 (ET)

**Owner:** R&D Variants (harness freeze / implement) → Simulator → Examiner  
**Status:** FROZEN — Conductor MAXIMIZE NEXT after Cap-SR PR20 merge @`45863037`  
**Cite:** Conductor 2026-09-23 post Cap-SR merge; parent DR freeze `C5_KXBTC15M_MEASUREMENT_FREEZE_KERNEL_2026-09-22.md` (sha256 `4d1b72a38603de181e71f80b3cc6515b170a2bffe11f8770dac1296373e50263`); panel stub `2026-09-22.c5-kxbtc15m-v0`; C1 honesty harness pattern (PR18)  
**Repo:** `https://github.com/17thgreen/GPT-6-Astra-Deathmatch`  
**Packet ID:** C5-KXBTC15M-HONESTY-HARNESS  
**Series:** `KXBTC15M` (BTC 15-minute up/down binary)  
**Hard rules:** Measurement-only **15m crypto fee/queue honesty stress** — **NOT live crypto trading**. No Logan demo keys required (GET-only public). No live orders. No invented PnL. No Q6-`000` retune. No queue-fragility reopen. No Cap-SR / A1↔A3 reopen. No bacchus / kxeth15m strategy port. `results`/`pnl` null until Examiner opens after Clock admit.

---

## Why C5 (not C3 this slot)

Conductor preferred leftover cash-cow scorable **without Logan keys**. C5 is fee/queue honesty stress on public rolling 15m tape (mirrors C1 honesty harness). C3 bordering-strike stays queued (panel stub also READY; R3-P3 weather preference) — do **not** dual-implement this pulse.

---

## Intent (one knob)

Holding **R1-P1 feebook** + **R1-P5 rails** fixed, wire a fee+queue honesty harness that consumes the C5 panel stub (and later admitted panel) for rolling `KXBTC15M` windows — same instrument fields as the Examiner fee+queue honesty path on `000`, under extreme turnover — **without** trading crypto or importing a 15m maker strategy.

**One knob only:** honesty stress cadence ∈ {`per_window`, `multi_window_stack`} with feebook+rails fixed.

**Not arms:** live maker sizes; capital Cap-SR; Q6 signal; queue-fragility QF0/1/2 reopen; bacchus/kxeth15m port; ETH15m series (Scout watch only).

---

## Pins

| Pin | Value |
|---|---|
| Parent freeze | `C5_KXBTC15M_MEASUREMENT_FREEZE_KERNEL_2026-09-22.md` sha256 `4d1b72a38603de181e71f80b3cc6515b170a2bffe11f8770dac1296373e50263` |
| Panel stub | `lab/astra-capture/c5-kxbtc15m/panel_stub.json` · panel_version `2026-09-22.c5-kxbtc15m-v0` · `admitted_at` **null** until Clock |
| Fee (FIXED) | `kalshi_feebook_lab_20260922/` @`22371178cb2663250b4762f328069571c48cb551` — forbid shadow `0.0175`/`0.07` |
| Rails (FIXED) | `kalshi_rails_lab_20260922/` @`6a28e0d6254327ea4e6451c781bec56215ac6cac` — `content_fresh_flag`, `maker_credit_floor_zero_refuse`, `queue_attribution_bin` |
| Honesty pattern | Prefer reuse of Examiner fee+queue honesty join helpers / C1 harness shape where present; do **not** mutate those labs beyond sibling import |
| Capture | GET-only public elections host — **no signed trading**; no Logan keys |
| Strategy pointer | **None** — measurement stress subject ≠ `000` retune. `000` remains KEEP/untouched. |
| Adversary refuse | `C1_C3_C5_ADVERSARY_REFUSE_BIND_2026-09-22.md` — live crypto / bacchus port / invented PnL |

---

## Arms (cadence knob only)

| Arm | Name | Cadence |
|---|---|---|
| **C5H0** | Per-window | Score honesty instruments once per admitted/stubbed rolling window |
| **C5H1** | Multi-window stack | Same instruments stacked across a bounded multi-window cohort (stub N≥1; expand only after admit) |

Both arms share identical fee+rails pins. Stub may only expose N=1 window — C5H1 units may use synthetic multi-window fixtures **without** writing non-null freeze scorecard fields.

---

## Scorecard fields (null now)

| Field | Meaning |
|---|---|
| `freshness_gap_sec` | Rails freshness gap under 15m rollover |
| `queue_bin_mismatch_rate` | Queue attribution bin mismatch vs rails defaults |
| `fee_delta_vs_inherited_model` | Feebook vs any inherited sports-maker assumption delta |
| `turnover_stress_flag` | Whether window turnover exceeds sports T−window reference label |

All stay **null** in this freeze / EMPTY_RESULTS until Examiner after Clock admit. Units assert schema + pin locks only.

---

## Lab deliverables (implement now)

New dir: `kalshi_c5_kxbtc15m_honesty_lab_20260923/` in Astra repo:

- `EXPERIMENT_SPEC.md` + `FROZEN_EXPERIMENT.json` (results/pnl null)  
- Harness that loads panel stub path; prefers admitted panel when `panel_admitted.json` appears  
- Bind feebook + rails imports; refuse fee literals  
- Unit tests: pin lock; stub load; C5H0/C5H1 schema; no live-order paths; adversary refuse labels for live crypto / bacchus port  
- First PR = **unit/instrument + stub join** (preferred); scorecard fields null  
- Do **not** mutate feebook / rails / capital / Cap-SR / Q / C1 labs

---

## Do-not-modify

1. No live orders / no live crypto trading / no signed order routes.  
2. No Logan demo/API keys required or requested for this harness.  
3. No Q6-`000` retune; no QF reopen; no Cap-SR / A1↔A3.  
4. No bacchus / kxeth15m strategy port.  
5. No inventing OI/volume beyond Scout cite / live GET / stub bytes.  
6. No silent backfill of expired windows without Collector/Clock stamp.  
7. `results`/`pnl` null until Examiner opens.

---

## Dead-card / orthogonality

- Nearest blocked sibling: **C1 empty-book** (UFC honesty scoring blocked on empty depth).  
- C5 does **not** ungate C1 books.  
- ≠ Cap-SR / F1–F3 / Q7 Arm B revival.

---

## Frozen-at

Desk 2026-09-23 ET. Conductor MAXIMIZE NEXT after Cap-SR PR20 merge. Variants owner: R&D Variants.
