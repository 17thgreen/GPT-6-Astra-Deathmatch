# S5 — KXMVECROSSCATEGORY fill-vs-legs measurement kernel — FREEZE 2026-09-22 (ET)

**Packet ID:** S5-KXMVECROSSCATEGORY-MEAS  
**Scout series (kernel):** `KXMVECROSSCATEGORY*` (cross-category MVE / combo binaries)  
**Related series (fee pin):** `KXMVECROSSCATEGORY`, `KXMVECROSSCATEGORY-SHARD1`, `KXMVESPORTSMULTIGAMEEXTENDED`  
**Owner (freeze):** Deep Research  
**Implementer (later):** Collector (GET panel) → Simulator (fill-vs-legs harness) → Examiner (Kalshi)  
**Reviewer:** Conductor triage; Adversary on fee-blind / combo fee schedule  
**Status:** **FROZEN** — results/pnl **null** (not run)  
**Cite:** Conductor maximize kick 2026-09-22 (pick S5 over S4); Scout `SCOUT_MAXIMIZE_DELTA_2026-09-22.md` §S5; triage `SCOUT_TRIAGE_MAXIMIZE_DELTA_2026-09-22.md` ADMIT TRY measurement-access; R1-P4 family **measurement only**; R1-P1 feebook; R1-P5 rails  
**Repo (future lab dir):** `17thgreen/GPT-6-Astra-Deathmatch` → e.g. `kalshi_mve_crosscat_filllegs_meas_lab_20260922/` (do not mutate Q6/Q7/capital / S1 / R2-P3 labs)  
**Hard rules:** No live orders. No invented PnL. No Q6-`000` signal retune. **Explicitly NOT R1-P4 strategy open.** RFQ `/communications` still deferred (401; do not ask Logan for key). Prefer `KXMVECROSSCATEGORY*` over empty `KXMVENFL*`. **Must** bind R1-P1 feebook + R1-P5 rails — **forbid** inherited Q7/Q6 fee literals; combo fee channel = series `quadratic_with_combo_maker_fees`.

---

## Intent (one measurement kernel)

Measure **fee-honest fill vs independent-leg product** on public cross-category combo tape — whether combo fills (and, when present, historical prints) align with the product of per-leg 1-minute TOB mids at the fill minute (flip \(1-\mathrm{mid}\) for NO legs), after applying the **combo maker fee** schedule via R1-P1 series override.

**Not a strategy.** Not an RFQ maker seat. Not a bakeoff claim vs `000`. Pre-settlement / historical measurement only until Examiner opens a scorecard after freeze+units.

---

## Bound inventory (Scout access — mandatory)

**Scout packet:** `lab/governance/astra/SCOUT_MAXIMIZE_DELTA_2026-09-22.md`

| Surface | Status | Use in this kernel |
|---|---|---|
| `/series` fee metadata | `fee_type=quadratic_with_combo_maker_fees`, `fee_multiplier=1` on cross-category combo series | R1-P1 series override pin |
| `/markets` open `KXMVECROSSCATEGORY*` | Public; large open inventory (≫200); sampled page vol/OI often 0.00 | Market + `mve_selected_legs` / `mve_collection_ticker` cohort |
| `/events/multivariate` | Public | Combo event join |
| `/markets/trades`, `/historical/trades` | Public GET | Fill / print tape; empty on zero-vol samples is allowed (do not invent fills) |
| `/communications/rfqs` | **401** | **Out of scope** this freeze |
| `is_block_trade=true` filter | **429** this Scout pass | Do not claim RFQ-fill density until Collector clears |
| `KXMVENFLSINGLEGAME` / `MULTIGAME` / `EXTENDED` | Empty or unconfirmed | **Do not prefer** over cross-category for first panel |

**Sample tickers (access proof only — not a panel admit):**
- Market: `KXMVECROSSCATEGORY-S20264CF5F0166A4-D93D828F247`
- Multivariate event: `KXMVECROSSCATEGORY-SHARD1-S2026FF7C4259D33`

**Hosts:** public elections / external Kalshi trade-api v2 allowlist (GET-only). Skip signed trading host for this measurement.

---

## Dead-card / live-pin overlap (named) — **NONE** vs game-book allocator

| Pin / card | Overlap | Handling |
|---|---|---|
| Q6-`000` KEEP | **None** — distinct combo/MVE structure | Measurement only; no quote/size/route of `000` |
| Q7 pair-check / Arm B KILL | **None** | Cemetery stands; do not reopen |
| Capital-structure A1/A2/A3 | **None** | Separate freeze |
| Crypto F1–F3 / Gauntlet | **N/A** | Idle science |
| R1-P4 RFQ strategy | **Family kinship only** | This packet = **measurement-access**; strategy / RFQ object stream remain **DEFER** |
| R2-P1 fee hygiene on `000` | **Complementary** — share feebook/rails libs | Variants owns `000` fee-sensitivity |
| S1 `KXMLBGAME` / R2-P3 PASSYDS / S4 NCAAF | **Orthogonal series** | Do not steal panels; S4 deferred this pick |
| Empty `KXMVENFL*` | **Explicitly out** | Prefer cross-category combo fee series |

---

## Mandatory instrument pins (not inherited Q7 fees)

| Dep | Pin | Rule |
|---|---|---|
| Fee | R1-P1 `kalshi_feebook_lab_20260922/` @ `22371178cb2663250b4762f328069571c48cb551` (or Archivist tip) | Series override: `quadratic_with_combo_maker_fees` / multiplier 1 on bound series; reciprocal algebra on each leg book; never shadow Q7/Q6 literals |
| Rails | R1-P5 `kalshi_rails_lab_20260922/` @ `6a28e0d6254327ea4e6451c781bec56215ac6cac` | `content_fresh_flag` per leg book + combo market; `maker_credit_floor_zero_refuse`; queue labels if resting books exist — instrument only |
| Legs product | Independent-leg mid product at fill minute | Flip NO legs; document missing-leg / stale-leg refuse |
| Capture | GET-only public markets / multivariate / trades / historical | Throttle; no RFQ communications; no signed portfolio |

**Refuse gate:** completed-profit label without feebook combo fee channel → refuse. Freshness from content/transaction time, not WS ping. Invented fills / invented OI → refuse.

---

## Measurement objects (pre-settlement / historical)

For each admitted combo market (and any public trade/print joined):

1. **Combo market state:** ticker, `mve_selected_legs`, `mve_collection_ticker`, reciprocal TOB via R1-P1 when book non-empty.  
2. **Per-leg 1-minute TOB mids** at fill minute (or sample minute); independent-leg product \(P_{\mathrm{legs}}\) (NO → \(1-\mathrm{mid}\)).  
3. **Fill / print price** \(P_{\mathrm{fill}}\) when trades exist; else null (do not invent).  
4. **Fee-aware residual:** \(P_{\mathrm{fill}} - P_{\mathrm{legs}}\) after R1-P1 combo maker fee channel; slice by price band, leg count, same-game vs decorrelated when leg metadata allows.  
5. **Optional resolution join later:** fill − resolution — only after Collector admits settled cohort; still null this freeze.  
6. **Rails labels:** freshness per leg/combo; maker-credit floor refuse on near-0/1 legs.  
7. **Liquidity honesty:** raw API `volume_fp` / `volume_24h_fp` / `open_interest_fp` only — Scout sampled zeros are valid observations, not bugs to fill.

**Explicitly null until Examiner run:** `results`, `pnl`, RFQ quote EV, maker seat ROI, annualization, live promotion, “beats `000`” claims.

---

## Panel / cohort (freeze rule — admit is Collector)

- Series filter: `KXMVECROSSCATEGORY*` (and SHARD1 / sports multigame extended only if fee pin matches combo-maker schedule).  
- Prefer markets with non-empty public trades or historical prints when available; zero-vol open inventory may be schema-only until tape appears.  
- Do **not** open RFQ communications crawl; do **not** require Logan API key for this freeze.  
- Do **not** steal R2-P1 join / S1 / R2-P3 / PIT@CLE poll budget; separate panel version string.  
- Suggested panel_version: `2026-09-22.s5-kxmvecrosscategory-v0` (Collector owns admit stamp).  
- First PR may be **schema + unit fixtures only** (empty results unchanged).

---

## Arms (optional contrast — still one kernel)

If Simulator needs a factorial later, **one knob only:** mid aggregation ∈ {`1m_mid`, `touch_mid`} with feebook+rails+combo fee fixed.  
**Not arms:** RFQ quoting; capital slices; Q6 signal; pair-check; NCAAF (S4); empty NFL MVE preference flip without Scout re-confirm.

---

## Do-not-modify

1. No live orders / no live launcher / no RFQ quotes.  
2. No invented PnL / no invented fills or OI.  
3. No Q6-`000` retune; no Q7 reopen; no capital A2/A3.  
4. No scoring with inherited Q7/Q6 fee literals; combo fee must use series override.  
5. No silent panel backfill; no opening R1-P4 **strategy**.  
6. Do not mutate feebook/rails/Q/S1/R2-P3 labs — new MVE meas lab dir when implementing.  
7. Do not expand this packet to S4 `KXNCAAFGAME`, `KXMVENFL*` empty inventory, or credentialed `/communications/rfqs`.

---

## Empty results (on disk)

- `packets/scout_s5_kxmvecrosscategory/FROZEN_EXPERIMENT.json` — `results`/`pnl` null  
- `packets/scout_s5_kxmvecrosscategory/results.json` + `results/EMPTY_RESULTS.json` — `NOT_RUN`

---

## Why S5 over S4 this cycle

Conductor offered S5 **or** S4. Deep Research picked **S5**: Scout already ADMIT TRY measurement-access on public combo GET path; dead-overlap **none** vs game-book `000`; S4 NCAAF remains TRY for a later football-OOS freeze without blocking R2-P1/S1/R2-P3 panels.

---

## Done =

Freeze packet on disk + Conductor ping with path. Implementation / admit / Examiner score = later seats.

## Frozen-at
`2026-09-22T23:43:54+00:00` UTC. Desk 2026-09-22 ET.
Deep Research freeze under Conductor maximize kick (S5 preferred over S4).
