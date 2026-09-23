# C1 — KXUFCFIGHT measurement kernel — FREEZE 2026-09-22 (ET)

**Packet ID:** C1-KXUFCFIGHT-MEAS  
**Scout series:** `KXUFCFIGHT` (UFC fight ML binaries)  
**Owner (freeze):** Deep Research  
**Implementer (later):** Collector (panel) → Simulator (fee+queue honesty bakeoff harness) → Examiner (Kalshi)  
**Reviewer:** Conductor cash-cow triage GO; Adversary on strategy claim / fee-blind EV  
**Status:** **FROZEN** — results/pnl **null** (not run)  
**Cite:** Conductor `SCOUT_TRIAGE_CASHCOW_2026-09-22.md` ADMIT FREEZE NOW; Scout `SCOUT_CASHCOW_HUNT_2026-09-22.md` §C1; R1-P1 feebook; R1-P5 rails  
**Raw inventory (Scout, cite only):** `packets/scout_cashcow_hunt_2026-09-22/scout_hunt_KXUFCFIGHT.json` — Scout page-sample: **200** · 58 open markets / 29 events · Σ volume_fp≈**1.7088e6** · Σ volume_24h_fp≈**1.5108e6** · Σ open_interest_fp≈**1.2545e6** (full open set, no cursor). Do **not** invent new OI/liquidity.  
**Hard rules:** Measurement-only. No live orders. No invented PnL. No Q6-`000` retune. No wholesale strategy import. Shared **$5k** bakeoff capital **as measurement contrast only** — **no strategy claim**. Must bind R1-P1 + R1-P5 — forbid inherited Q7/Q6 fee literals.

---

## Intent (one measurement kernel)

Does a fight-night discrete settlement clock + deep YES/NO books show **fee-honest maker/taker + queue fragility** that can be scored under a **shared $5k** measurement bakeoff vs Q6-`000` instruments — without porting the `000` allocator or claiming maker EV?

**Not a strategy.** Fee+queue honesty bakeoff vs `000` under shared $5k. Pre-settlement / accounting objects only until Examiner opens a scorecard after freeze+units.

---

## Dead-card / live-pin overlap (named)

| Pin / card | Overlap | Handling |
|---|---|---|
| Q6-`000` KEEP | **None / low** — combat card calendar, not NFL week/T−7d allocator; no pair-router semantics | Subject is UFC fight ML microstructure + fee/queue honesty; do **not** retune `000` |
| Q7 pair-check / Arm B KILL | **None** | Cemetery stands; do not reopen |
| Capital-structure A1/A2/A3 | **None** — shared $5k is bakeoff sizing label only | Not a wallet/slice arm |
| S1/S4/S5/R2-P3 | **Orthogonal series** | Do not steal panel budget |
| R2-P1 / Variants fee+queue honesty on `000` | **Complementary bakeoff subject** | Variants owns `000` tape honesty; C1 stresses same instruments on **UFC** tape |
| R3-P1 venue `fee_cost` | **Optional later join** | Not required for first freeze |
| Crypto F1–F3 / Gauntlet | **N/A** | Idle science |
| More `KXNFLGAME` MM / `000` reopen | **Explicitly out** | Scout forbidden |

---

## Mandatory instrument pins

| Dep | Pin | Rule |
|---|---|---|
| Fee | R1-P1 `kalshi_feebook_lab_20260922/` @ `22371178cb2663250b4762f328069571c48cb551` | Reciprocal book + `order_fee` / `round_up` / series maker flag via feebook only. Scout fee pin cite: `quadratic` / **1** (cached `/series`) |
| Rails | R1-P5 `kalshi_rails_lab_20260922/` @ `6a28e0d6254327ea4e6451c781bec56215ac6cac` | `content_fresh_flag`, `maker_credit_floor_zero_refuse`, `queue_attribution_bin` — instrument only |
| Kickoff / close SoT | Kalshi public event `occurrence_datetime` / market close | Fight-night clock; Scout sample occ=`2026-09-23T04:20:00Z` → **2026-09-23 00:20 ET** |
| Capture | GET-only public elections host (events, markets, orderbook, trades) | No signed trading host for public GETs; **no live Astra orders** |
| Bakeoff capital | Shared **$5k** label | Measurement contrast sizing only — not a strategy bankroll claim |

**Refuse gate:** completed-profit / strategy-EV label without feebook fee channel → refuse. Freshness from content/transaction time, not WS ping. Zero-credit fight-night quotes → rails refuse label.

---

## Measurement objects (pre-settlement)

For each admitted `KXUFCFIGHT` event / YES-NO market pair, at each sample time `t` with `content_fresh_flag=true`:

1. **Reciprocal book:** `bid_YES`, `bid_NO`, `ask_YES=1-bid_NO`, `ask_NO=1-bid_YES`, `spread_YES` (R1-P1). Stress near extreme favorite prices.  
2. **Fee channel** on any fill or hypothetical fill size C at P: R1-P1 `order_fee` — never shadow literals.  
3. **Rails labels:** `maker_credit_floor_zero_refuse`, `queue_attribution_bin` vs reference rails defaults (labels, not strategy).  
4. **Timing shape:** minutes-to-scheduled-occurrence/close; raw API `volume_fp` / `open_interest_fp` **as Scout-cited or live GET only** (no invented depth).  
5. **Fee+queue honesty bakeoff objects vs `000`:** same instrument fields under shared $5k measurement budget — **null strategy EV**.

**Explicitly null until Examiner run:** `results`, `pnl`, fill rates as strategy EV, annualization, live promotion, “beats 000” claims.

---

## Panel / cohort (freeze rule — admit is Collector)

- Series: `KXUFCFIGHT` only.  
- First implementable panel: **bounded fight-card slate** after Conductor/Collector admit (do not backdate).  
- Suggested panel_version pattern: `2026-09-22.c1-kxufcfight-v0` (Collector owns final admit stamp).  
- Scout samples (cite only, not admit): `…-26SEP22CONGUA-GUA`, `…-CON`.

---

## Arms (optional contrast — still one kernel)

If Simulator needs a factorial later, **one knob only**: markout / honesty horizon ∈ {`1m`, `5m`, `15m`} with feebook+rails fixed.  
**Not arms:** capital slices beyond shared $5k label; Q6 signal; pair-check; queue as strategy; wholesale UFC strategy import.

First PR may be **schema + unit fixtures only** (empty results unchanged).

---

## Do-not-modify

1. No live orders / no live launcher.  
2. No invented PnL / no author-wallet anecdotes as evidence.  
3. No Q6-`000` retune; no Q7 reopen; no capital A2/A3.  
4. No scoring with inherited Q7/Q6 fee literals.  
5. No silent panel backfill; no inventing OI/liquidity beyond Scout cite / live GET.  
6. Do not mutate feebook/rails/Q labs — new UFC meas lab dir when implementing.  
7. No wholesale strategy import from external combat MM repos.

---

## Empty results (on disk)

- `packets/scout_c1_kxufcfight/FROZEN_EXPERIMENT.json` — `results`/`pnl` null  
- `packets/scout_c1_kxufcfight/results.json` + `results/EMPTY_RESULTS.json` — `NOT_RUN`

---

## Done =

Freeze packet on disk + Conductor ACK with path. Implementation / admit / Examiner score = later seats.

## Frozen-at

`2026-09-23T00:13:00+00:00` UTC. Desk 2026-09-22 ET.  
Deep Research freeze under Conductor cash-cow ADMIT FREEZE NOW (Scout C1).
