# Sibling deathmatch review — 2026-09-22 (ET)

**Reviewer:** Scout / Archivist seat (executor)  
**Window:** 2026-09-22 ~17:28–17:45 America/New_York  
**Method:** GitHub MCP `user-GitHub-xai` — `list_branches`, `list_releases`, `list_tags`, `get_repository_tree`, `get_file_contents`, `search_code`  
**Astra SoT:** `17thgreen/GPT-6-Astra-Deathmatch` + local `/workspace/lab/astra-science`  
**Hard rules:** NO LIVE ORDERS. No fabricated PnL. Sibling ROI claims are not Examiner evidence.

---

## Executive

| Question | Answer |
|---|---|
| **Factorial kit found?** | **NO — definitive miss** in both sibling repos + empty stub |
| **Any ARCHIVES.json kit ZIP?** | **NO** (zero `.zip` blobs; zero Releases/tags) |
| **Q7-usable `events.jsonl.gz`?** | **NO** (not in git; Claude `data/*` gitignored; Grok has no gz) |
| **What to pull?** | Measurement kernels only — fee/book + queue rails + print-role scoring |
| **What to leave?** | Sibling as kit store; claimed MM ROI; dead directional/Stern/weather lottery cards |

Primary blocker for **Q7-RUN** remains owner-supplied `NFL_Allocation_Factorial_Kit.zip` (sha256 `f330169d9b58826348b662863518ca82fdd64e34e8a30e1df4e54b45c5552c39`, ~62.3 MB). Siblings are **not** a substitute archive.

---

## A) `17thgreen/Grok-Deathmatch` — Linewright (Grok side)

| Field | Value |
|---|---|
| Default branch | `main` @ `2b343c2af2917ba1c98076eb6d9b5ff635a6532c` |
| Releases / tags | **none** |
| Tree size | **44** blobs/trees (`truncated: false`) |
| Role | Paper-only Kalshi research desk; competitor to Claude Flat-Line |

### Structure

```
README.md, docs/{CHECKLIST,EXECUTIVE,FORWARD,MODEL_CARD,RESEARCH}.md
scripts/run-micro.ts
src/components/linewright/
src/lib/engine/api.ts
src/lib/linewright/   # config, fees, micro, inplay, nowcast, cross, scan, tape, paper, tests
src/lib/linewright/data/micro-summary.json   # committed micro walk summary (~82KB)
src/lib/providers/    # kalshi-catalog, kalshi-hist, espn, polymarket (+ imports of kalshi/dutch/tape/ws)
src/routes/{desk,health,index}.tsx
```

TypeScript / React app. Explicitly paper-only: no actuator, no funds. Micro lab walks official Kalshi `/historical/trades` + `/historical/markets`. Docs state **no historical CLOB**.

### Kit / data findings — **DEFINITIVE MISS**

| Probe | Result |
|---|---|
| `search_code` Kit.zip / Factorial / ARCHIVES / `f330169d` / `events.jsonl` / `restore_kit` | **0 hits** |
| `extension:zip` / `extension:gz` | **0 hits** |
| Releases / tags | empty |
| Tree scan | no `.zip`, no `.jsonl.gz` |
| Optional local path mentioned in docs | `data/processed/micro-prints.jsonl.gz` **if present** — **not in repo tree** |

Committed replay-adjacent artifact: `src/lib/linewright/data/micro-summary.json` only (aggregated role ROI summary, not Astra `events.jsonl.gz`).

### Candidate kernels (Grok)

1. **`src/lib/linewright/fees.ts`** — Kalshi quadratic fees: taker `ceil_cent(rate·P·(1−P))`, maker unrounded; `EXCHANGE_V1` rates 0.07 / 0.0175 in `config.ts`.
2. **`MICRO_V1` + `micro.ts` / `run-micro.ts`** — print-role maker vs taker scoring on settled public trades; size-weighted gates; NFL in-play window heuristic.
3. **Fleet / Dutch / in-play / cross** — forward paper scan only; theoretical locks; **not** Q6 allocator.

**Dead cards (do not reopen):** HX spread picker holdout **−6.7%**; Kelly-on-negative-edge; reverse-FLB weather cheap YES (Claude board: DEAD); naive Stern (Claude: FAIL).

---

## B) `17thgreen/Claude-SportsBetting-Competition-to-the-Death` — Flat-Line (Claude side)

| Field | Value |
|---|---|
| Default branch | **`claude/kind-hamilton-gdfr9q`** (not `main`) @ `11e00f182e0fa1f97ed80eb69fec1269d43d8f5a` |
| Releases / tags | **none** |
| Role | Football EV → Kalshi paper MM lineage; `flatstake` Python package |

### Structure (root)

```
README.md, STRATEGY_BOARD.md, pyproject.toml, uv.lock, LICENSE, .env.example, .gitignore
artifacts/experiments/     # many per-run dirs + diagnostics/ + registry.jsonl
data/                      # GITIGNORED except data/fixtures/**
deploy/, docs/ (00–27+), scripts/, src/flatstake/, tests/, views/, web/
```

`.gitignore` excludes `data/*` (raw Kalshi parquet tapes, SQLite ledgers, snapshots). Docker build copies only `registry.jsonl` + `diagnostics/` + models/freeze/forward — **not** raw tapes.

### Kit / data findings — **DEFINITIVE MISS for Astra kits**

| Probe | Result |
|---|---|
| Factorial / `NFL_Allocation` / `Kit.zip` / sha256 `f330169d` | **0 hits** |
| `events.jsonl` / `restore_kit` / `ARCHIVES.json` | **0 hits** |
| `extension:zip` / `extension:gz` | **0 hits** |
| Releases | empty |

**Present but not Q7 drop-in:**

| Artifact | Usable by Astra Q7? |
|---|---|
| `artifacts/experiments/registry.jsonl` + per-run `summary.json` / `bets.csv` | No — sportsbook/EV registry + paper MM summaries; wrong schema |
| `artifacts/experiments/diagnostics/*.json` (e.g. kalshi microstructure) | Measurement reference only |
| `weather_forecast_ledger.csv` (committed under diagnostics per STRATEGY_BOARD) | Weather forward ledger — not NFL game-book events |
| Paper MM SQLite ledgers / `data/raw/kalshi/trades_*.parquet` | **Gitignored** — not fetchable via GitHub tree |
| Public-tape refresh code (`kalshi_public.refresh_tape`) | Can **regenerate** public trades going forward; cannot mint ARCHIVES-indexed kit SHA |

Astra Q7 / Factorial need indexed `nfl_factorial_lab_20260921/inputs/events.jsonl.gz` (sha256 `cd300e664c2c5f2ff344c4b1eb17dd3f8e5f3326168b9dd8e3ade94a3a7382b4`, ~22.9 MB) restored via owner kit + `scripts/restore_kit.py`. Sibling artifacts do **not** substitute.

### Candidate kernels (Claude) — highest value

| Kernel | Path | Why it matters for Astra |
|---|---|---|
| **FeeModel** | `src/flatstake/paper/fees.py` | Order-level `ceil_cent(0.07·C·P·(1−P))` taker / `0.0175` maker; per-contract cap $0.035; partial-fill rounding discipline — **R1-P1** |
| **YES/NO + event netting** | `src/flatstake/paper/account.py` | Collateral netting; YES+YES / NO+NO across mutex pair — overlaps Q6/Q7 pair economics |
| **Queue fill model** | `src/flatstake/paper/execution.py` | Default queue **3300**, fill participation **0.5**, taker_side→passive mapping, requote queue reset — matches Astra queue scenarios; **R1-P5** instrument |
| **Policy window** | `src/flatstake/paper/policy.py` v1.3.0 | 7d→kickoff, stop_at_start, size ≤ book depth — spirit of Q4–Q6; **do not import ROI** |
| **Public fee + tape** | `src/flatstake/providers/kalshi_public.py` | `taker_fee` ceil_cent; historical cutoff routing; parquet tape layout |

**STRATEGY_BOARD dead / leave alone:** naive Stern (FAIL 1/6); spread/total ladder makers; MLB pregame MM; cross-venue arb (0/694); directional NFL/CFB pickers; weather FLB favorites; Kelly-on-negative. **ON BOARD but not for silent Astra retune:** NFL moneyline maker (2025 +0.24¢/contract framing; early 2026 +34% called out as optimistic in-sample — **not Examiner [V]**).

---

## C) `17thgreen/Grok-Death-Match` (stub)

| Probe | Result |
|---|---|
| `list_branches` | `[]` |
| `get_file_contents` `/` | **409 Git Repository is empty** |

Empty stub. No kits, no code. Ignore.

---

## Kit download status

| Action | Result |
|---|---|
| Release asset download | N/A — **no releases** on A or B |
| Raw URL / tree blob for Factorial zip | **none** |
| `/workspace/lab/astra-kits/` | **empty** (prior `MISS_REPORT.md` only); **no sha256 verify** |

Expected Factorial index (from science `provenance/ARCHIVES.json`):

```
path:   nfl_factorial_lab_20260921/NFL_Allocation_Factorial_Kit.zip
bytes:  62342699
sha256: f330169d9b58826348b662863518ca82fdd64e34e8a30e1df4e54b45c5552c39
```

---

## Dead-card overlap vs Astra (Q6 / Q7 / R1)

| Sibling idea | Astra card | Overlap | Disposition |
|---|---|---|---|
| Fee ceil_cent + maker 0.0175 (Grok + Claude) | **R1-P1 FEEBOOK** | Doc/hardening; does not retune Q6 | **PULL** algebra into R1-P1 tests |
| Reciprocal YES/NO / event pair netting (Claude `account.py`) | **Q6 allocator + Q7 paircheck** | High conceptual overlap | **LEAVE strategy**; may cite as external pair-algebra reference **after** Q7 freeze |
| Queue 3300 / participation / requote (Claude `execution.py`) | Q1–Q6 queue arms + **R1-P5** | Instrument overlap | **PULL** as measurement rail only |
| Policy 7d→kickoff, stop_at_start, size≤depth | Q4–Q6 incumbent spirit | Already in Astra lineage | **LEAVE** — no silent retune; do not copy claimed ROI |
| Micro print-role lab (Grok) | Orthogonal to development cohort books | Low | **PULL** as Deep Research / adverse-selection scorecard |
| HX / directional pickers / naive Stern / weather lottery | Cemetery | Dead | **LEAVE** |
| Weather/crypto fleet locks (Grok) | Non-NFL Scout | Charter-adjacent | Market Scout TRY later; not Q7 |
| Factorial / REST replay kits | Q7-RUN gate | **Missing** | Owner supply only |

---

## Top 3 kernels to extract

1. **Claude `FeeModel` (`src/flatstake/paper/fees.py`) + Grok `fees.ts` cross-check** → pin R1-P1 Examiner fee channel (order-level ceil, maker 0.0175, cap, partial-fill rule).  
2. **Claude `SimulatedExecutionAdapter` queue/fill (`execution.py`)** → R1-P5 queue-attribution instrument aligned to Astra 3300/10k scenarios; taker_side polarity tests.  
3. **Grok `MICRO_V1` print-role scoring (`micro.ts` + fees)** → size-weighted maker/taker role ROI on public historical prints; adverse-selection / fee honesty for Adversary — **not** a Q6 challenger.

Honorable mention (do **not** promote as allocator): Claude `account.py` event-level YES/YES netting — pair economics reference for post-Q7 Adversary, not a silent `000` retune.

---

## Recommendation

### Pull into Astra

- R1-P1: port/compare fee formulas from Claude `fees.py` and Grok `fees.ts` against published Kalshi schedule; unit fixtures only.  
- R1-P5: adopt Claude queue semantics (measured ahead, participation, same-price keep place / new-price back of queue) as **instrument**, not strategy.  
- Optional: Grok micro-role gates as Examiner refuse-criteria for fee-blind PnL claims.

### Leave alone

- Entire sibling trees as **kit stores** — they do not hold ARCHIVES ZIPs.  
- Paper MM policy versions / dashboard ROI / “+34%” replay framings.  
- Dead STRATEGY_BOARD / RESEARCH cards (Stern naive, spread/total makers, directional EV, weather FLB).  
- Claude `data/` parquet regeneration as a fake kit — regenerated tape **cannot** match Factorial kit sha256.  
- Stub `Grok-Death-Match`.

### Unlock Q7-RUN

1. Logan supplies `NFL_Allocation_Factorial_Kit.zip` matching ARCHIVES sha256.  
2. `python scripts/restore_kit.py /path/to/NFL_Allocation_Factorial_Kit.zip` in science clone.  
3. Confirm `nfl_factorial_lab_20260921/inputs/events.jsonl.gz` bytes+sha256.  
4. Then Q7 16-scenario run (arms A–D); keep `pnl: null` until executed.

---

## Explicit non-actions this review

- Did **not** download any kit (none available).  
- Did **not** run Q7 grid or fabricate PnL.  
- Did **not** place or simulate live orders.  
- Did **not** promote sibling ROI into Examiner scorecards.

---

## Return summary

| Item | Value |
|---|---|
| Memo | `/workspace/lab/governance/astra/packets/SIBLING_DEATHMATCH_REVIEW_2026-09-22.md` |
| Factorial kit | **MISS** |
| Top 3 kernels | (1) Claude+Grok fee models → R1-P1 (2) Claude queue/fill adapter → R1-P5 (3) Grok MICRO print-role lab |
