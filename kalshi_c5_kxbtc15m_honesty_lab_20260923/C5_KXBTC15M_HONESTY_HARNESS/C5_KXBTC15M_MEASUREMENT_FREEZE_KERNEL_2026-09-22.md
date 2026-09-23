# C5 — KXBTC15M measurement kernel — FREEZE 2026-09-22 (ET)

**Packet ID:** C5-KXBTC15M-MEAS  
**Scout series:** `KXBTC15M` (BTC 15-minute up/down binary)  
**Owner (freeze):** Deep Research  
**Implementer (later):** Collector (rolling 15m panel) → Simulator (fee/queue honesty stress) → Examiner (Kalshi)  
**Reviewer:** Conductor cash-cow triage GO; Adversary on live crypto trading / bacchus strategy port  
**Status:** **FROZEN** — results/pnl **null** (not run)  
**Cite:** Conductor `SCOUT_TRIAGE_CASHCOW_2026-09-22.md` ADMIT FREEZE NOW; Scout `SCOUT_CASHCOW_HUNT_2026-09-22.md` §C5; GitHub `meloun7711/kxeth15m-research` **structure parallel only** (ETH sibling); R1-P1; R1-P5  
**Raw inventory (Scout, cite only):** **200** · **1** open market / 1 event (rolling) · volume_fp≈**133994.61** · volume_24h_fp≈**107298.17** · open_interest_fp≈**88032.36**. Sample: `KXBTC15M-26SEP222015-15` occ=`2026-09-23T00:20:00Z` → **2026-09-22 20:20 ET**. Raw: `packets/scout_cashcow_hunt_2026-09-22/scout_hunt_KXBTC15M.json`. Do **not** invent new OI/liquidity.  
**Hard rules:** **15m crypto fee/queue honesty stress — not live crypto trading.** No live orders. No invented PnL. No Q6-`000` retune. No wholesale bacchus / kxeth15m strategy port. Must bind R1-P1 + R1-P5.

---

## Intent (one measurement kernel)

Do ultra-short crypto binaries force **fee/queue honesty failures** (turnover ≫ sports T−window) that stress `000`’s inherited maker/taker / freshness assumptions under shared instrument rules — without trading crypto live or importing a 15m maker strategy?

**Not a strategy.** Measurement-only fee/queue honesty stress on rolling 15m tape.

---

## Dead-card / live-pin overlap (named)

| Pin / card | Overlap | Handling |
|---|---|---|
| Q6-`000` KEEP | **None** — crypto clock; rolling 15m windows | Honesty stress subject ≠ NFL allocator retune |
| Q7 / capital / F1–F3 / Gauntlet | **Explicitly out of strategy** | Gauntlet idle; C5 is instrument stress only |
| bacchus-mm 15m crypto strategy | **Explicitly out** | Extract instrumentation preference elsewhere (R3-P1); **no** strategy port |
| kxeth15m-research | **Structure sibling only** | ETH15M optional watch (Scout); not this freeze’s series |
| S1/S4/S5/R2-P3 | **Orthogonal** | Different clocks |
| R3-P1 / R3-P2 | **Complementary instruments** | May join fee_cost / queue_position later; not required at freeze |
| Live crypto trading | **DENIED** | GET-only public tape/L2 |

---

## Mandatory instrument pins

| Dep | Pin | Rule |
|---|---|---|
| Fee | R1-P1 `kalshi_feebook_lab_20260922/` @ `22371178cb2663250b4762f328069571c48cb551` | Scout fee pin cite: `quadratic` / **1** |
| Rails | R1-P5 `kalshi_rails_lab_20260922/` @ `6a28e0d6254327ea4e6451c781bec56215ac6cac` | Extreme turnover → freshness/queue instruments dominate |
| Window SoT | Kalshi market `occurrence_datetime` / window close | Rolling 15m; do not mix sports T−windows |
| Capture | GET-only public elections host (markets, orderbook, trades) | **No live crypto trading**; no signed order routes |

**Refuse gate:** completed-profit / live-trading claim without feebook → refuse. Bacchus/kxeth15m strategy PnL as Astra evidence → refuse.

---

## Measurement objects (pre-settlement)

For each rolling `KXBTC15M` window admitted at fresh `t`:

1. **Reciprocal book** + spread under high turnover.  
2. **Fee channel** via R1-P1 on hypothetical fills.  
3. **Rails stress:** `content_fresh_flag` gaps, `queue_attribution_bin`, zero-credit refuse under rapid window rollover.  
4. **Turnover honesty objects:** raw API volume/OI as Scout-cited or live GET only — stress whether sports-inherited maker/taker assumptions hold.  

**Explicitly null until Examiner:** `results`, `pnl`, crypto strategy EV, “refutes/beats 000” claims, live promotion.

---

## Panel / cohort (freeze rule — admit is Collector)

- Series: `KXBTC15M` only (ETH15M = Scout optional watch — **TBD**, not frozen here).  
- First panel: **bounded rolling windows** after admit; no backfill of expired windows without explicit Collector stamp.  
- Suggested panel_version: `2026-09-22.c5-kxbtc15m-v0`.  
- Scout sample (cite only): `KXBTC15M-26SEP222015-15`.

---

## Arms (optional — still one kernel)

One knob later: freshness/queue stress cadence ∈ {per-window, multi-window stack} with feebook+rails fixed.  
**Not arms:** live maker sizes; capital slices; Q6 signal; bacchus strategy port.

---

## Do-not-modify

1. No live orders / no live crypto trading.  
2. No invented PnL.  
3. No Q6-`000` retune; no Gauntlet reopen as strategy.  
4. No inherited Q7/Q6 fee literals.  
5. No silent backfill; no inventing OI beyond Scout cite / live GET.  
6. Do not mutate feebook/rails/Q labs; no wholesale bacchus / kxeth15m strategy import.

---

## Empty results (on disk)

- `packets/scout_c5_kxbtc15m/FROZEN_EXPERIMENT.json` — `results`/`pnl` null  
- `packets/scout_c5_kxbtc15m/results.json` + `results/EMPTY_RESULTS.json` — `NOT_RUN`

---

## Done =

Freeze packet on disk + Conductor ACK. Collector admit / Examiner = later.

## Frozen-at

`2026-09-23T00:13:00+00:00` UTC. Desk 2026-09-22 ET.  
Deep Research freeze under Conductor cash-cow ADMIT FREEZE NOW (Scout C5). **Not live crypto trading.**
