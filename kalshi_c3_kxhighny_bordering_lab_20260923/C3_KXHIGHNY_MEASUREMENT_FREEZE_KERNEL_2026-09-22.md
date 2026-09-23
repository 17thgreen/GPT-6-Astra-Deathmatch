# C3 — KXHIGHNY (+CHI) measurement kernel — FREEZE 2026-09-22 (ET)

**Packet ID:** C3-KXHIGHNY-MEAS  
**Scout series:** `KXHIGHNY` weather high-temp ladder (+ multi-city proof `KXHIGHCHI`)  
**Owner (freeze):** Deep Research  
**Implementer (later):** Collector (weather ladder panel) → Simulator (bordering-strike / fee-honest Bernoulli objects) → Examiner (Kalshi)  
**Reviewer:** Conductor cash-cow triage GO; Adversary on GitHub weather-spread as Astra EV  
**Status:** **FROZEN** — results/pnl **null** (not run)  
**Cite:** Conductor `SCOUT_TRIAGE_CASHCOW_2026-09-22.md` ADMIT FREEZE NOW; Scout `SCOUT_CASHCOW_HUNT_2026-09-22.md` §C3; GitHub `Ciarnan-Moloney/Kalshi-Weather-Spread-Algo` **structure pointer only**; R1-P1; R1-P5; **prefer weather panel material for R3-P3**  
**Raw inventory (Scout, cite only):** NY **200** · 12 mkts / 2 events · Σ vol≈**1.6799e5** · Σ vol24≈**1.5363e5** · Σ oi≈**1.0118e5**. CHI **200** · 12 mkts · Σ vol24≈**5.1343e4** · Σ oi≈**3.5869e4**. Raw: `packets/scout_cashcow_hunt_2026-09-22/scout_hunt_KXHIGHNY.json`, `…_KXHIGHCHI.json`. Do **not** invent new OI/liquidity.  
**Hard rules:** Measurement-only. No live orders. No invented PnL. No Q6-`000` retune. No wholesale weather-spread strategy import. Weather-spread bordering-strike MM = **hypothesis only**. Must bind R1-P1 + R1-P5.

---

## Intent (one measurement kernel)

On daily max-temp threshold ladders (`KXHIGHNY`, with `KXHIGHCHI` as multi-city proof), measure fee-honest Bernoulli / **bordering-strike** microstructure objects under R1-P1 + R1-P5 — without claiming the GitHub weather-spread algo beats `000` after settlement-penalty + queue attribution.

**Not a strategy.** Bordering-strike weather ladder measurement. GitHub weather-spread structure is **hypothesis only**.

### Weather panel preference for R3-P3 (cited)

**Prefer this C3 weather panel material as first-panel inventory for R3-P3** (Maker/Taker + favorite–longshot bands) when Conductor/Collector stand up settled public tape: R3-P3 hard rule is prefer weather/politics/economics first; C3 supplies Scout-proven `KXHIGH*` inventory that is **non-frozen-sports** and orthogonal to S1/S4/S5/R2-P3. C3 freeze remains cash-cow measurement; R3-P3 may **reuse** C3-admitted weather markets as panel material — not a merge of kernels, not a strategy claim.

---

## Dead-card / live-pin overlap (named)

| Pin / card | Overlap | Handling |
|---|---|---|
| Q6-`000` KEEP | **None** — climate binaries; no NFL event join | Do **not** retune `000` |
| Q7 / capital A1–A3 / F1–F3 | **None** | Orthogonal |
| S1/S4/S5/R2-P3 | **Orthogonal series** | Avoid as R3-P3 first panel; C3 weather is preferred alternate |
| R3-P3 FL maker/taker bands | **Complementary panel material** | Prefer C3 weather for R3-P3 settled tape (cited above); kernels stay distinct |
| R3-P4 L2 shape | **May share L2 later** | Separate panel_version |
| GitHub weather-spread algo | **Hypothesis / structure only** | No wholesale import; no author PnL as Astra EV |
| More `KXNFLGAME` / `000` reopen | **Explicitly out** | Scout forbidden |

---

## Mandatory instrument pins

| Dep | Pin | Rule |
|---|---|---|
| Fee | R1-P1 `kalshi_feebook_lab_20260922/` @ `22371178cb2663250b4762f328069571c48cb551` | Scout fee pin cite: `quadratic` / **1** (NY + CHI). Ladder near 0/1 strikes = R1-P1 stress |
| Rails | R1-P5 `kalshi_rails_lab_20260922/` @ `6a28e0d6254327ea4e6451c781bec56215ac6cac` | Freshness + queue attribution labels — instrument only |
| Settlement SoT | Kalshi public `occurrence_datetime` / resolution | Scout sample occ→**2026-09-23 10:00 ET** |
| Capture | GET-only public elections host (events, markets, orderbook, trades, resolutions when settled) | No live orders |
| Structure hyp | Weather-spread bordering strikes (GitHub pointer) | **Hypothesis only** — measure adjacent-contract book objects; do not import EV |

**Refuse gate:** completed-profit without feebook → refuse. Citing GitHub weather-spread PnL as Astra evidence → refuse.

---

## Measurement objects (pre-settlement)

For each admitted `KXHIGHNY` (and optional `KXHIGHCHI`) threshold market at fresh `t`:

1. **Reciprocal book** + spread on threshold strikes (esp. near 0/1).  
2. **Bordering-strike ladder objects:** adjacent-strike mid/spread/depth raw API fields — structure hypothesis, not EV.  
3. **Fee channel** via R1-P1 on hypothetical C at P.  
4. **Rails labels** (freshness / zero-credit refuse / queue bin).  
5. **Multi-city proof join:** same calendar day NY vs CHI inventory presence (Scout-proven) — no invented cross-city arb PnL.

**Explicitly null until Examiner:** `results`, `pnl`, “beats 000”, settlement-penalty EV, annualization.

---

## Panel / cohort (freeze rule — admit is Collector)

- Primary series: `KXHIGHNY`. Multi-city proof: `KXHIGHCHI` (and later other `KXHIGH*` if Scout unblocks — **TBD**, not invented).  
- Suggested panel_version: `2026-09-22.c3-kxhighny-v0`.  
- Scout samples (cite only): `KXHIGHNY-26SEP22-T70`, `…-B67.5`.  
- **R3-P3 overlap:** Collector may mark weather markets from this panel as eligible first material for R3-P3 settled bands (cite this preference).

---

## Arms (optional — still one kernel)

One knob later if needed: strike band ∈ {near-0/1, mid-ladder} with feebook+rails fixed.  
**Not arms:** capital slices; Q6 signal; wholesale weather-spread MM port.

---

## Do-not-modify

1. No live orders.  
2. No invented PnL / no GitHub author EV as evidence.  
3. No Q6-`000` retune.  
4. No inherited Q7/Q6 fee literals.  
5. No silent backfill; no inventing OI beyond Scout cite / live GET.  
6. Do not mutate feebook/rails/Q labs.  
7. Do not merge C3 into R3-P3 as a strategy — panel material preference only.

---

## Empty results (on disk)

- `packets/scout_c3_kxhighny/FROZEN_EXPERIMENT.json` — `results`/`pnl` null  
- `packets/scout_c3_kxhighny/results.json` + `results/EMPTY_RESULTS.json` — `NOT_RUN`

---

## Done =

Freeze packet on disk + Conductor ACK. Collector admit / R3-P3 weather panel reuse / Examiner = later.

## Frozen-at

`2026-09-23T00:13:00+00:00` UTC. Desk 2026-09-22 ET.  
Deep Research freeze under Conductor cash-cow ADMIT FREEZE NOW (Scout C3). **Weather panel preferred for R3-P3.**
