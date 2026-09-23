# S4 — KXNCAAFGAME football OOS measurement kernel — FREEZE 2026-09-22 (ET)

**Packet ID:** S4-KXNCAAFGAME-MEAS  
**Scout series:** `KXNCAAFGAME` (college football game moneyline binaries)  
**Optional later siblings (not this freeze):** `KXNCAAFSPREAD` / `KXNCAAFTOTAL` if Scout confirms listing  
**Owner (freeze):** Deep Research  
**Implementer (later):** Collector (panel) → Simulator (fee/queue-honest markout) → Examiner (Kalshi)  
**Reviewer:** Conductor triage; Adversary on fee-blind / weekend overlap vs `000`  
**Status:** **FROZEN** — results/pnl **null** (not run)  
**Cite:** Conductor maximize kick 2026-09-22 (S4 after S5 accept); Scout `SCOUT_MAXIMIZE_DELTA_2026-09-22.md` §S4 replace; triage `SCOUT_TRIAGE_MAXIMIZE_DELTA_2026-09-22.md` ADMIT TRY; R1-P1 feebook; R1-P5 rails  
**Repo (future lab dir):** `17thgreen/GPT-6-Astra-Deathmatch` → e.g. `kalshi_ncaaf_game_meas_lab_20260922/` (do not mutate Q6/Q7/capital / S1 MLB / R2-P3 / S5 labs)  
**Hard rules:** No live orders. No invented PnL. No Q6-`000` signal retune. No capital-structure arms. **Must** bind R1-P1 feebook + R1-P5 rails — **forbid** inherited Q7/Q6 `0.0175`/`0.07` fee literals. Orthogonal **football OOS** vs NFL `000` — not more `KXNFLGAME` capacity.

---

## Intent (one measurement kernel)

Measure whether NFL T−7d→T−3h **timing / microstructure lab objects** (fee-honest reciprocal book + rails freshness/queue labels) transfer to **college football** `KXNCAAFGAME` YES/NO books — a **football out-of-sample** series vs the NFL allocator `000`, without porting `000` or inventing maker EV.

Contrast to S1 (`KXMLBGAME`): S1 is daily non-football binary generalize; S4 is **weekend football OOS** with fee channel matching NFL game books (`maker_fees` / 1 per Scout).

**Not a strategy.** Pre-settlement measurement only until Examiner opens a scorecard after freeze+units. Not an R1-P2 challenger open unless Conductor separately kicks bakeoff.

---

## Bound inventory (Scout-confirmed — mandatory)

**Scout packet:** `lab/governance/astra/SCOUT_MAXIMIZE_DELTA_2026-09-22.md`

| Field | Scout observation (raw API; not invented) |
|---|---|
| Series | `KXNCAAFGAME` |
| Listing | **CLEARED** (was 429 on earlier brief) |
| First page | **20 markets / 10 events** |
| OI sum (page) | ≈ **2.55e5** (dominated by **MCNS/LSU**) |
| Fee metadata | `maker_fees` / **1** (matches NFL game-book fee channel shape) |
| Prior status | Brief DEFER → Maximize REPLACE placeholder → **TRY** |

**Kickoff SoT:** Kalshi public `occurrence_datetime` / market close fields.  
**Capture:** GET-only public elections host allowlist. Do not steal PIT@CLE / S1 / R2-P3 / S5 / R2-P1 poll budget.

**Panel note:** Collector owns first bounded weekend/next-Saturday slate map; this freeze does **not** invent event tickers beyond Scout’s MCNS/LSU dominance note. Suggested panel_version: `2026-09-22.s4-kxncaafgame-v0`.

---

## Dead-card / live-pin overlap (named) — **MEDIUM**

| Pin / card | Overlap | Handling |
|---|---|---|
| Q6-`000` KEEP | **Medium — weekend football calendar overlap with NFL Sun; different series** | Football **OOS** measurement vs `000`; **no** quote/size/route retune of `000`; not more NFL ML capacity |
| Q7 pair-check / Arm B KILL | **None** — no pair-check knob | Cemetery CEM-ASTRA-20260922-001 stands |
| Capital-structure A1/A2/A3 | **None** | Separate freeze |
| Crypto F1–F3 / Gauntlet | **N/A** | Idle science |
| More `KXNFLGAME` MM | **Explicitly out** | Incumbent territory |
| S1 `KXMLBGAME` | **Complementary** — non-football daily vs football weekend OOS | Separate panels; may share feebook/rails libs |
| R2-P3 PASSYDS | **Schedule kinship only** (football weekend) | Distinct prop-ladder contracts |
| S5 MVE cross-category | **None** — distinct structure | Already frozen separately |
| R1-P2 challenger QUEUE | **Related class, not this open** | Measurement freeze only; bakeoff needs separate Conductor kick |
| Weather/politics placeholder | **Superseded** | This packet **is** the S4 series pin (`KXNCAAFGAME`) |

---

## Mandatory instrument pins (not inherited Q7 fees)

| Dep | Pin | Rule |
|---|---|---|
| Fee | R1-P1 `kalshi_feebook_lab_20260922/` @ `22371178cb2663250b4762f328069571c48cb551` (or Archivist tip) | Reciprocal book + `order_fee` / `round_up` / series maker flag; Scout fee shape `maker_fees`/1 via feebook API only |
| Rails | R1-P5 `kalshi_rails_lab_20260922/` @ `6a28e0d6254327ea4e6451c781bec56215ac6cac` | `content_fresh_flag`, `maker_credit_floor_zero_refuse`, `queue_attribution_bin` — instrument only |
| Kickoff / close SoT | Kalshi `occurrence_datetime` / market close | CFB weekend cluster — do not mix NFL holdout +3h clocks |
| Capture | GET-only public events/markets/orderbook/trades | Collector discipline; throttle |

**Refuse gate:** completed-profit without feebook fee channel → refuse. Freshness from content/transaction time, not WS ping.

---

## Measurement objects (pre-settlement)

For each admitted `KXNCAAFGAME` YES-NO market at sample time `t` with `content_fresh_flag=true`:

1. **Reciprocal book:** `bid_YES`, `bid_NO`, asks via R1-P1 Pin A, `spread_YES`.  
2. **Fee channel** on fill or hypothetical size C at P via R1-P1 `order_fee` — never shadow Q7/Q6 literals.  
3. **Rails labels:** `maker_credit_floor_zero_refuse`, `queue_attribution_bin` (3300 / 10000 as **labels**).  
4. **Timing shape:** minutes-to-`occurrence_datetime`; raw `volume_fp` / `volume_24h_fp` / `open_interest_fp` only.  
5. **Adverse mid markout (optional first units):** mid Δ over 1m / 5m / 15m conditional on touch — **no** outcome P&L required.  
6. **OOS contrast vs `000`:** fee+queue honesty metrics only on CFB tape; **no** `000` parameter change.

**Explicitly null until Examiner run:** `results`, `pnl`, strategy EV, annualization, live promotion, “beats `000`” claims.

---

## Arms (optional contrast — still one kernel)

If Simulator needs a factorial later, **one knob only:** markout horizon ∈ {`1m`, `5m`, `15m`} with feebook+rails fixed.  
**Not arms:** capital slices; Q6 signal; pair-check; spread/total expand; weather/politics revert.

First PR may be **schema + unit fixtures only** (empty results unchanged).

---

## Do-not-modify

1. No live orders / no live launcher.  
2. No invented PnL / no invented event tickers or OI beyond Scout raw figures.  
3. No Q6-`000` retune; no Q7 reopen; no capital A2/A3.  
4. No scoring with inherited Q7/Q6 fee literals.  
5. No silent panel backfill; no steal of PIT@CLE / S1 / R2-P3 / S5 / R2-P1 budget.  
6. Do not mutate feebook/rails/Q/S1/R2-P3/S5 labs — new NCAAF meas lab dir when implementing.  
7. Do not expand this packet to `KXNFLGAME` MM capacity, `KXNCAAFSPREAD`/`TOTAL` until Scout listing confirm, or R1-P2 bakeoff without Conductor kick.

---

## Empty results (on disk)

- `packets/scout_s4_kxncaafgame/FROZEN_EXPERIMENT.json` — `results`/`pnl` null  
- `packets/scout_s4_kxncaafgame/results.json` + `results/EMPTY_RESULTS.json` — `NOT_RUN`

---

## Done =

Freeze packet on disk + Conductor ping with path. Implementation / admit / Examiner score = later seats.

## Frozen-at
`2026-09-22T23:44:37+00:00` UTC. Desk 2026-09-22 ET.
Deep Research freeze under Conductor maximize kick (S4 after S5 accept).
