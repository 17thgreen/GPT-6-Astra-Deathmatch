# Astra / Kalshi Desk — Working Plan v0
**Date:** 2026-09-22  
**Owner:** The Conductor (oversee + delegate; hands-on only when no better seat)  
**Status:** APPROVED 2026-09-22 by Logan — staffing in progress. Charter of record until v1.  
**Governor amendment (binding):** The current NFL maker / Astra Deathmatch line is **incumbent primary**, not permanent primary. It remains primary **only while nothing more profitable and executable is verified**. Any Kalshi bot, strategy, or market-maker design is **fair game**. Discovery that beats the incumbent on verified EV + executability **displaces** it. ALMANAC stays parked until explicit reopen.

---

## 1. Mission

Maximize **verified** profitability and compounding on Kalshi under lab doctrine:

- **NO LIVE ORDERS** until explicit Governor GO for that strategy and stage.
- Never invent returns, fill rates, queues, or fees.
- Prefer correct **NO TRADE / kill / defer** over a pretty backtest.
- Extrapolations are labeled **projections**, not evidence.
- Assume nothing; verify against ledger, fees, inventory, and unresolved risk.

**Success ≠ number of bots.** Success = capital growth under controls, with a desk that keeps finding and promoting better edges.

---

## 2. Scope (what is in / out)

| In | Out (unless Governor reopens) |
|---|---|
| Kalshi: NFL maker line (Astra), other sports, event markets, MM, taker, hybrid — fair game | BTC/ETH short-horizon binary **science** as primary (passive captures may continue health-only) |
| Research, sim, shadow, gated live | Fabricated P&L; silent holdout reuse; backdating admissions |
| OSS / web / GitHub scouting → proposals | ALMANAC mail/DID ops (parked) |
| Dedicated fleet repo later (Logan) | Force-pushing science history; live risk without Treasurer-class gate |

---

## 3. Evidence & returns (how we refuse to lie)

### Stages (strict separation)
1. **Hypothesis / freeze** — spec committed before outcomes.
2. **Historical sim** — development cohort; fees + inventory rules explicit; unresolved ≠ profit.
3. **Shadow / paper** — live public data, no orders (or orders disabled).
4. **Live micro** — tiny size, hard kill switches, Treasurer GO.
5. **Scale** — only after live micro matches shadow within predeclared band.

### “Accurate returns”
- Mark completed P&L after fees; track open inventory separately.
- No double-counting shared liquidity across concurrent sims.
- Queue, latency, and collateral assumptions stated; stress cases required for MM.
- **Modeled** = sim under frozen assumptions. **Extrapolated** = projection from those models (sample size, regime, capacity limits called out). Never mix labels.

### Incumbent displacement rule
A challenger becomes new primary only if it wins a predeclared bakeoff: same capital constraints (or explicitly scaled), fee-aware, executable on Kalshi microstructure we can actually access, and superior on the frozen scorecard (net EV, drawdown, capacity, operational risk). Conductor schedules bakeoffs; Examiner-class seat scores; Logan confirms promotion.

---

## 4. Desk layout (delegation)

Conductor = air traffic control. Seats below can be new agents, renamed existing ones, or Conductor-held until staffed.

| Seat | Mandate | Does not |
|---|---|---|
| **Conductor** | Allocate attention; freeze gates; promote/kill; MD truth; only do work with no better owner | Solo-build every bot; waive gates |
| **Archivist / Registry** | Experiment registry, freezes, hashes, admissions log | Invent results |
| **Collector Ops** | GET-only durable public capture; panel admission; coverage audits | Trading; backdated windows |
| **Simulator / Replay** | Historical engines, factorial screens, kit restore fidelity | Live orders |
| **Examiner (Kalshi)** | Deterministic scorecards; bakeoffs; kill/green; distinct from ALMANAC Examiner | Dual-hat ALMANAC scoring |
| **Deep Research** | Continuous web/GitHub/OSS/venue-doc scan; weekly proposal brief (kernels, risks, build candidates) | Auto-merge into live; fabricate win rates |
| **R&D Variants** | Controlled variations on incumbent + challengers; one change per trial when possible | Silent multi-knob retunes |
| **Adversary / Drift Guard** | Lookahead, leakage, fee blindness, regime break, capacity fantasy, prompt/strategy drift | Block all creativity — only forces named risks onto the scorecard |
| **Mechanic (execution)** | When near live: APIs, cancels, rate limits, kill switch | Strategy authorship |
| **Treasurer** | Capital, exposure caps, stage gates, demote live | Science scoring |
| **Scout (markets)** | New Kalshi markets / sports / structures worth a measurement kernel | Shipping untested bots |

**ALMANAC seats** (Radar, Quill, Drop, Switchboard, Examiner ALMANAC): remain idle/parked until Logan reopens ALMANAC.

**Crypto Gauntlet science seats:** idle for research; pulse may watch capture health only.

---



---

## 4b. Cohesion — one unit, one workflow

The desk is a **single operating unit**, not a chatroom of independent bots. Every seat speaks the same language (freeze → measure → score → promote/kill), shares one priority board, and hands work through named packets — never drive-by retunes.

### Operating loop (daily spine)

```
Scout / Deep Research  →  proposals (kernels only)
        ↓
Conductor triage       →  accept / defer / kill (one owner)
        ↓
Registry freeze        →  EXPERIMENT_SPEC + hashes BEFORE outcomes
        ↓
Collector / Simulator  →  data + runs (no invented fills)
        ↓
Examiner score         →  KEEP / ITERATE / KILL (+ bakeoff if challenger)
        ↓
Adversary spot-check   →  leakage, fee blindness, capacity fantasy, drift
        ↓
Conductor promote      →  incumbent update OR cemetery; Logan only for live/capital
```

### Packet protocol (how work moves)

1. **Packet ID + one outcome** (e.g. C1 collector admission, Q7 freeze).  
2. **Owner seat** + **reviewer seat** (never self-certify TEST/live).  
3. **Inputs / freeze / banned moves** listed up front.  
4. **Done = artifact on disk** (MD/JSON/PR), not a vibe.  
5. Conductor closes or reassigns; no parallel conflicting freezes on same line.

### Cohesion rules

| Do | Don't |
|---|---|
| One priority board (Conductor) | Three seats “primary” on the same problem |
| Challenger bakeoffs vs incumbent | Silent replacement of strategy |
| Shared cemetery + registry | Private win narratives in chat only |
| Cross-read: Research cites Examiner gates; Examiner cites freezes | Research shipping code past Examiner |
| Escalate to Logan only for credentials, capital, live GO, venture pivot | Ping Logan for routine triage |

### Maximize growth / ops / process / efficiency / strategy

- **Growth:** displacement rule — capital and attention follow verified better EV.  
- **Ops:** Collector + admission calendar is first-class (missed T−7d = process failure).  
- **Process:** freeze-before-outcome; stage gates; no dual-hat score+build.  
- **Efficiency:** Conductor does a task only if no better seat; kill stalled packets at weekly review.  
- **Strategy:** incumbent Kalshi line held lightly; fair game across Kalshi; ALMANAC parked until reopen.


## 5. Standing cadences

| Cadence | Who | Output |
|---|---|---|
| Continuous / event | Collector Ops | Capture health; admission deadlines |
| Daily (when science live) | Conductor | Priority board: collector, Q7, kits, challenger intake |
| Weekly | Deep Research | Proposal brief ≤5 items: source, kernel, dead-overlap, cost to try, recommend try/skip |
| Weekly | Adversary | Drift / leakage / fee / capacity red-team on active lines |
| Per experiment | Registry + Examiner | Freeze → run → score → cemetery or promote |
| Bakeoff (as needed) | Conductor | Incumbent vs challenger under frozen rules |

---

## 6. Near-term work packets (already in flight + next)

| ID | Packet | Owner (proposed) | Status |
|---|---|---|---|
| C1 | Durable GET collector + prospective/holdout panel path; PIT@CLE T−7d awareness | Collector Ops / cloud agent | **In flight** (cloud agent) |
| Q7 | `nfl_paircheck_lab_20260922` freeze + 2×2 implement; no invented P&L | Simulator / cloud agent | **In flight** (cloud agent) |
| K1 | Owner kit ZIPs → `restore_kit.py` for full ledger fidelity | Logan provides; Simulator verifies | Blocked on kits |
| R1 | First Deep Research brief: Kalshi MM / sports / OSS landscape vs Astra | Deep Research | After plan GO + seat exists |
| B0 | Bakeoff template (incumbent displacement scorecard) | Conductor drafts MD | After plan GO |

---

## 7. After plan GO — MD + agent actions (not done until you say)

1. Rewrite desk-mode skill: Astra/Kalshi primary **displaceable**; ALMANAC parked; crypto science idle.  
2. Create or retitle seats: Deep Research, Adversary/Drift, Collector Ops, Examiner (Kalshi), R&D Variants (minimum viable set; Mechanic/Treasurer when approaching live).  
3. Charter MDs under `lab/governance/astra/seats/`.  
4. Wire experiment registry pointer into Astra repo docs once PRs land.  
5. Keep Conductor as sole router to Logan for capital/live/credential asks.

---

## 8. What else is needed (anticipated)

- **Kit custody** path (where ZIPs live; who may restore).  
- **Kalshi API credential** handling only at Mechanic/live stage (secret-request, never chat).  
- **Capacity model** (how P&L scales with size / shared book).  
- **Market calendar** ownership (NFL + other sports kickoffs → T−7d).  
- **Fleet repo** timing: after first shadow-capable loop, not before.  
- **Explicit kill criteria** for incumbent (e.g. shadow EV ≤ 0 for N events; fee regime break).

---

## 9. Decision asked of Logan

Approve Working Plan v0.1 **as-is** (including cohesion loop + packet protocol), or edit:
- Seat set (trim/add)
- Whether Deep Research may propose **non-NFL Kalshi** in week 1 or NFL-only until Q7/collector land
- Whether to **cancel** either in-flight cloud agent

On GO: Conductor assigns seats + updates MDs and reports back with names.

