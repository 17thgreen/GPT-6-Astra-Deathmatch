# R2-P3 — KXNFLPASSYDS prop-ladder measurement kernel — FREEZE 2026-09-22 (ET)

**Packet ID:** R2-P3-KXNFLPASSYDS-MEAS  
**Scout series (kernel):** `KXNFLPASSYDS` (NFL passing-yards multi-strike ladders)  
**Sibling series (same games):** `KXNFLRECYDS`, `KXNFLRSHYDS`  
**Owner (freeze):** Deep Research  
**Implementer (later):** Collector (panel) → Simulator (fee+queue / residual harness) → Examiner (Kalshi)  
**Reviewer:** Conductor triage; Adversary on fee-blind / multi-strike honesty  
**Status:** **FROZEN** — results/pnl **null** (not run)  
**Cite:** Conductor R2-P3 ADMIT 2026-09-22; Scout slate `SCOUT_R2P3_PROP_SLATE_2026-09-22.md`; R2 brief §R2-P3; R1-P1 feebook; R1-P5 rails  
**Repo (future lab dir):** `17thgreen/GPT-6-Astra-Deathmatch` → e.g. `kalshi_nfl_passyds_ladder_meas_lab_20260922/` (do not mutate Q6/Q7/capital / S1 MLB labs)  
**Hard rules:** No live orders. No invented PnL. No Q6-`000` signal retune. No capital-structure arms. **Must** bind R1-P1 feebook + R1-P5 rails — **forbid** inherited Q7/Q6 `0.0175`/`0.07` fee literals. **Not ATL@GB.**

---

## Intent (one measurement kernel)

Measure **prop-ladder / multi-strike fee + queue honesty** on public NFL yards ladders versus the binary ML allocator `000` subject — without retuning `000` or claiming maker EV.

At each decision minute on the bound slate: record the strike set, TOB mid per strike, fee-aware effective touch via R1-P1, and rails freshness/queue labels via R1-P5. Test whether strike mids share one latent (player-mean) via cross-strike residual after a monotone fit, versus fragmented independent books. Contrast is **measurement vs `000` fee/queue honesty**, not a challenger strategy.

**Not a strategy.** Pre-settlement measurement only until Examiner opens a scorecard after freeze+units.

---

## Bound slate (Scout ADMIT — mandatory)

**Name:** Sun **2026-09-27** dual-game prop slate — **LAC@BUF + BAL@DAL**  
**Scout packet:** `lab/governance/astra/SCOUT_R2P3_PROP_SLATE_2026-09-22.md`

| Game | Kickoff SoT (`occurrence_datetime` → ET) | Kernel event | Sibling events |
|---|---|---|---|
| LAC@BUF | **2026-09-27 16:00 ET** (`2026-09-27T20:00:00Z`) | `KXNFLPASSYDS-26SEP27LACBUF` | `KXNFLRECYDS-26SEP27LACBUF`, `KXNFLRSHYDS-26SEP27LACBUF` |
| BAL@DAL | **2026-09-27 19:25 ET** (`2026-09-27T23:25:00Z`) | `KXNFLPASSYDS-26SEP27BALDAL` | `KXNFLRECYDS-26SEP27BALDAL`, `KXNFLRSHYDS-26SEP27BALDAL` |

**Kernel players (PASSYDS):** `LACJHERBERT10`, `BUFJALLEN17`, `DALDPRESCOTT4`, `BALLJACKSON8`.

**Sample market tickers (illustrative, not a panel admit):**
- `KXNFLPASSYDS-26SEP27LACBUF-LACJHERBERT10-300`
- `KXNFLPASSYDS-26SEP27LACBUF-BUFJALLEN17-275`
- `KXNFLPASSYDS-26SEP27BALDAL-DALDPRESCOTT4-275`
- `KXNFLPASSYDS-26SEP27BALDAL-BALLJACKSON8-250`

**Explicit exclusion:** `KXNFLPASSYDS-26SEP24ATLGB` / RECYDS / RSHYDS ATL@GB — **too late** (Conductor + Scout). Do not admit despite richer raw OI/vol.

**Kickoff SoT:** Kalshi public `occurrence_datetime` only (align R2-P5 / Clock discipline).

---

## Dead-card / live-pin overlap (named) — **MEDIUM**

| Pin / card | Overlap | Handling |
|---|---|---|
| Q6-`000` KEEP | **Medium — same NFL calendar / game days; different contracts** | Measurement contrasts multi-strike fee+queue honesty **vs** `000` binary ML; **no** quote/size/route retune of `000` |
| Q7 pair-check / Arm B KILL | **None** — no pair-check knob | Cemetery CEM-ASTRA-20260922-001 stands; do not reopen |
| Capital-structure A1/A2/A3 | **None** — no wallet/slice arms | Separate freeze |
| Crypto F1–F3 / Gauntlet | **N/A** | Idle science |
| More `KXNFLGAME` MM / incumbent | **Schedule overlap only** | Ladder microstructure subject; not ML capacity claim |
| R2-P1 fee hygiene / fee-sensitivity on `000` | **Complementary, not duplicate** — R2-P1 owns `000` fee pin; this packet measures **ladder** tape | Share feebook/rails libs only; Variants owns R2-P1 freeze |
| S1 `KXMLBGAME` | **Orthogonal sport/series** | Do not mutate S1 panel |
| R2-P4 SPREAD/TOTAL | **Distinct** | Still deferred until C1 PIT@CLE |
| R1-P3 adverse / R2-P5 SoT | **Optional join later** | Not required for first freeze; bot port remains KILL |
| Scout S5 MVE fill-vs-legs (optional FYI) | **Distinct series** (`KXMVECROSSCATEGORY*`) | Do not block or expand this packet |

---

## Mandatory instrument pins (not inherited Q7 fees)

| Dep | Pin | Rule |
|---|---|---|
| Fee | R1-P1 `kalshi_feebook_lab_20260922/` @ `22371178cb2663250b4762f328069571c48cb551` (or Archivist-updated tip if re-pinned) | Reciprocal book + `order_fee` / `round_up` / series maker flag via feebook API only; multi-strike fees must use same channel per strike |
| Rails | R1-P5 `kalshi_rails_lab_20260922/` @ `6a28e0d6254327ea4e6451c781bec56215ac6cac` | `content_fresh_flag` **per strike book**; `maker_credit_floor_zero_refuse`; `queue_attribution_bin` — instrument only |
| Kickoff / close SoT | Kalshi `occurrence_datetime` / market close fields | Dual-game slate: do not collapse LACBUF and BALDAL clocks |
| Capture | GET-only public elections host allowlist (events, markets, orderbook, trades) | Collector discipline; no signed trading host required for public GETs; throttle ≥45–90s between series |

**Refuse gate:** any completed-profit label without feebook fee channel → refuse. Freshness from content/transaction time, not WS ping. Near-0/1 strikes that floor maker credit to zero → `maker_credit_floor_zero_refuse`.

---

## Measurement objects (pre-settlement)

For each admitted PASSYDS (and optional sibling) market at sample time `t` with `content_fresh_flag=true`:

1. **Strike set + TOB mid** per market ticker (raw bid/ask reconstruct via R1-P1 Pin A).  
2. **Fee-aware effective touch** at size C via R1-P1 `order_fee` — never shadow Q7/Q6 literals.  
3. **Rails labels:** `maker_credit_floor_zero_refuse`, `queue_attribution_bin` vs reference rails defaults (3300 / 10000 as **labels**, not strategy claims).  
4. **Cross-strike residual:** after monotone fit to a single player-mean latent, residual per strike (fragmented vs one-latent hypothesis).  
5. **Contrast vs `000`:** same calendar windows where available — fee+queue honesty metrics only; **no** `000` parameter change.  
6. **Timing / liquidity proxies:** minutes-to-`occurrence_datetime`; raw API `volume_fp` / `volume_24h_fp` / `open_interest_fp` only (no invented depth).  
7. **Adverse mid markout (optional first units):** mid change 1m / 5m / 15m conditional on touch — **no** outcome P&L required.

**Explicitly null until Examiner run:** `results`, `pnl`, fill rates as strategy EV, annualization, live promotion, latent EV claims.

---

## Panel / cohort (freeze rule — admit is Collector)

- Kernel series: `KXNFLPASSYDS` on the two events above; siblings RECYDS/RSHYDS same events when cheap.  
- Bound slate only — **no ATL@GB**, no Monday open props this pass, no ANYTD until Scout clears 429.  
- Do **not** steal NFL ADMIT-1 / PIT@CLE / S1 MLB / R2-P1 join poll budget; separate panel version string required.  
- Suggested panel_version pattern: `2026-09-22.r2p3-kxnflpassyds-v0` (Collector owns final admit stamp).  
- First implementable panel: T− window while kickoffs remain ~days out (Scout: ~5d at slate map); do not backdate.

---

## Arms (optional contrast — still one kernel)

If Simulator needs a factorial later, **one knob only:** markout horizon ∈ {`1m`, `5m`, `15m`} **or** residual monotone family ∈ {`isotonic`, `logit-monotone`} with feebook+rails fixed — pick **one** knob family per run.  
**Not arms:** capital slices; Q6 signal; pair-check; queue as strategy; external odds bot; ATL@GB enrichment; MVE combo (S5).

First PR may be **schema + unit fixtures only** (empty results unchanged).

---

## Do-not-modify

1. No live orders / no live launcher.  
2. No invented PnL / no author-wallet anecdotes as evidence.  
3. No Q6-`000` retune; no Q7 reopen; no capital A2/A3.  
4. No scoring with inherited Q7/Q6 fee literals.  
5. No silent panel backfill / no ATL@GB admit.  
6. Do not mutate feebook/rails/Q/S1 labs — new PASSYDS meas lab dir when implementing.  
7. Do not expand this packet to `KXNFLSPREAD`/`TOTAL` (R2-P4), `KXMVECROSSCATEGORY*` (S5), or RFQ/communications.

---

## Empty results (on disk)

- `packets/scout_r2p3_kxnflpassyds/FROZEN_EXPERIMENT.json` — `results`/`pnl` null  
- `packets/scout_r2p3_kxnflpassyds/results.json` + `results/EMPTY_RESULTS.json` — `NOT_RUN`

---

## Done =

Freeze packet on disk + Conductor ping with path. Implementation / admit / Examiner score = later seats.

## Frozen-at
`2026-09-22T23:42:46+00:00` UTC. Desk 2026-09-22 ET.
Deep Research freeze under Conductor R2-P3 ADMIT (Scout slate Sun 2026-09-27 LAC@BUF + BAL@DAL).
