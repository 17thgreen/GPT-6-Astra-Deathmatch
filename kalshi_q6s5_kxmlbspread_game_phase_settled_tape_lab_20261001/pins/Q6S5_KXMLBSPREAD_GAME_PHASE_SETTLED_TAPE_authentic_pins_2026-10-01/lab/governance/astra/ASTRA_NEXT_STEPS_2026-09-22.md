# Astra next steps — Q7 / collector / admission / kits
**Date:** 2026-09-22 (America/New_York)  
**Repo:** 17thgreen/GPT-6-Astra-Deathmatch  
**Audience:** The Conductor (assignable work packets)  
**Constraints:** NO LIVE ORDERS. No secrets. Do not invent P&L. Do not push from this memo alone.

Sources read (GitHub MCP `cursor-github`, main):  
`docs/NEXT_EXPERIMENT.md`, `docs/EXPERIMENT_REGISTRY.md`,  
`nfl_factorial_lab_20260921/{EXPERIMENT_SPEC,FORWARD_PROTOCOL,FORWARD_HANDOFF,SHADOW_CANDIDATE_FREEZE,RESERVED_HOLDOUT,README,factorial_policy,shared_margin_probe}`,  
`nfl_measurement_lab_20260921/{PROTOCOL,README,capture,evaluation_gate,HOLDOUT_MANIFEST}`,  
`nfl_timing_lab_20260921/{README,Dockerfile,compose.yaml,collector/*}`,  
`provenance/{ARCHIVES,EXTERNAL_ARTIFACTS}`, `scripts/restore_kit.py`, root `README.md` / `AGENTS.md` / `.gitignore`.

---

## 1. Q7 exact 2×2 arms (PROPOSED, NOT IMPLEMENTED, NOT RUN)

**Question** (`docs/NEXT_EXPERIMENT.md`): Does checking the **combined acquisition cost of the two routes actually chosen** explain the Q6 improvement, or do the allocator’s scheduling/sizing rules matter?

| Arm | Architecture | Chosen-pair price check |
|---|---|---|
| A | Original router (`AdaptiveReplay(..., 'baseline')`) | **off** — untouched reference |
| B | Original router | **on** — change **only** admission of new paired exposure |
| C | Q6 simplified allocator (`FactorialReplay` / selected **`000`**) | **off** — remove only the combined-cost filter; keep timing/sizing/offset; use Q6 neutral ranking |
| D | Q6 simplified allocator | **on** — untouched Q6 reference |

**Fixed across all arms (do not retune):**  
$5,000 account · 31-game development cohort · 250 event cap · 250 assumed exit depth · inherited fee model · quote timing/queue assumptions · queues **3300 / 10000** · delays **0.25 / 5 s** → **16 scenarios**.  
Do **not** co-optimize route choices, thresholds, patience, or size.

**Pre-code semantics to freeze (explicit in NEXT_EXPERIMENT):**  
treatment of offset-only orders and partially filled pairs; check must **not** block necessary inventory reduction, assume simultaneous fills, inspect future quotes, or cancel instantly; record rejected pairs + reasons (skipped hypothetical profits ≠ money); for check-off allocator arm, ensure filter is not retained via another score/eligibility path; match positive controls exactly.

**Decision gate after run:** report guard effects within each architecture + interaction; completed net after fees; adverse fills; residuals; per-week contributions; inventory duration; preserve losses; exclude unresolved from completed-profit claims; declare candidate-selection rule and freeze source **before** outcomes. If guard-only original retains improvement → freeze for prospective shadow; else allocator bundle remains combined. Neither substitutes for fresh data.

### Freeze-before-run checklist (Conductor gate)

1. **New experiment directory** (do not mutate frozen Q6 originals) with committed `EXPERIMENT_SPEC.md` + `FROZEN_EXPERIMENT.json` **before** any Q7 result files.  
2. Pin hashes of: engine copies / policy modules / tests / inputs manifest / Q6 `SHADOW_CANDIDATE_FREEZE.json` selection label **`000`** + its `source_sha256` / `baseline_sha256`.  
3. Predeclare arm labels A–D, 16 scenario grid, metrics list, and simplest-candidate / retain rule (or “report only, no new selection”).  
4. Unit tests for: check-on original admits/rejects correctly; check-off allocator has **no** residual margin gate; offset-only path unblocked; rejection ledger present.  
5. Positive-control plan: Arm D reproduces Q6 `000` summaries/ledger hashes where comparable; Arm A reproduces original-router references from Q6 `Q5_REFERENCES` / baseline.  
6. **No** live orders, paid data, multi-wallet, or holdout outcome peek.  
7. Parallel: collector/admission work is **separate** and does not wait on Q7 results—but Q7 does not unlock fresh validation.

**Suggested new dir name:** `nfl_paircheck_lab_20260922` (or `nfl_q7_paircheck_lab_20260922`).  
Update `docs/EXPERIMENT_REGISTRY.md` + `docs/NEXT_EXPERIMENT.md` status only after freeze commit (per `AGENTS.md`).

### Code that must change (implement later — not in this memo)

| Area | Why | Cite / note |
|---|---|---|
| New lab tree (copy or import engine) | Frozen Q6 dirs are evidence snapshots | `AGENTS.md` |
| Original-router pairing / admission | Arm B needs check **on** without allocator timing/sizing | Today margin check lives in allocator path: `nfl_factorial_lab_20260921/factorial_policy.py` `portfolio_rank` (`margin=1-sum(costs)-…`; `if margin<=0: return None`) |
| Allocator check toggle | Arm C must remove combined-cost filter only | Same `factorial_policy.py`; ensure no second eligibility path |
| `run_experiment.py` / analyze / verify / tests | 2×2 × 4 stresses = 16 cases; effects + interaction reporting | Mirror Q6 runner pattern |
| `shared_margin_probe.py` | Structural probe only; **not** Q7 attribution | Already documents the mechanism gap |

Do **not** implement Q7 in this governance pass unless trivial docs (registry pointer). Full implementation is a separate Conductor assignment.

---

## 2. Collector: what exists vs what must still be built/deployed

### Already in-repo (GET-only public)

| Path | Role | Status |
|---|---|---|
| `nfl_timing_lab_20260921/collector/record.py` | Restartable SQLite recorder; allowlisted public GETs only (`events/…`, `…/orderbook`, `markets/trades`); watermarks, dedupe, gaps on restart; polls **T−7d → T−3h+5m** | **Code present**; rejects `purpose != development` |
| `nfl_timing_lab_20260921/collector/OPERATIONS.md` | Local + Docker ops | Prepared |
| `nfl_timing_lab_20260921/collector/inspect_capture.py` | Capture integrity inspect | Present |
| `nfl_timing_lab_20260921/collector/development_panel.json` | Dev panel (2 events) | Present |
| `nfl_timing_lab_20260921/collector/RESERVED_HOLDOUT.json` | Schedule registry copy | Present; **not** proof of recording |
| `nfl_timing_lab_20260921/Dockerfile` + `compose.yaml` | `nfl-recorder` service, volume `./capture-data` | **Prepared, not deployed** (README + FORWARD_PROTOCOL) |
| `nfl_timing_lab_20260921/test_collector.py` | Unit tests (lock, restart gap, dedupe, no private routes) | Present |
| `nfl_measurement_lab_20260921/capture.py` | Bounded finite JSONL capture (Q3); GET allowlist; refuses overwrite | Present; **not** always-on durable host |

Docs repeatedly state: **no always-on recorder running**; committing Docker ≠ deployment.

### Must still be built / operated (not inventable from clone alone)

1. **Durable host** running compose (or equivalent supervisor) with persistent disk for SQLite — not ephemeral.  
2. **Holdout / prospective panel configuration** — `record.py` `validate_panel` **rejects** `purpose: holdout`; needs separately reviewed config + code/settings frozen **before** windows + verified Kalshi event tickers.  
3. **Venue identity resolution** for reserved games (31/32 holdout `event` fields are `null` except `KXNFLGAME-26SEP28PHICHI`).  
4. Coverage audit pipeline before strategy P&L (per `FORWARD_PROTOCOL.md`).  
5. Optional: promote Q3 `capture.py` patterns into holdout ops — but Q4 `collector/record.py` is the intended durable recorder cited by forward docs.

**Assignable packet “COLLECTOR-1”:** deploy GET-only recorder on a durable host using Q4 paths; start **development** panel first (smoke); then design holdout panel admission without backdating.

---

## 3. Cohort admission / T−7d status (as of 2026-09-22 ~16:44 ET)

**Reservation:** schedule-only 32 games in  
`nfl_factorial_lab_20260921/RESERVED_HOLDOUT.json` (= measurement `HOLDOUT_MANIFEST.json`).  
Status: `PENDING_FUTURE_WINDOWS_NO_HOLDOUT_RESULTS`.  
Freeze of reservation: `2026-09-21T15:29:51Z`.

| Fact | Value |
|---|---|
| First reserved kickoff | `2026_03_PHI_CHI` / `KXNFLGAME-26SEP28PHICHI` · kickoff **2026-09-29T00:15:00Z** (**2026-09-28 20:15 ET**) |
| First full T−7d window start | **2026-09-22T00:15:00Z** = **2026-09-21 20:15 ET** |
| Docs’ stated first window | Same (`FORWARD_PROTOCOL` / `FORWARD_HANDOFF` / measurement README) |
| Always-on capture at packaging | **None** |
| Venue IDs | Mostly unresolved (`event: null`) |

### Was the 2026-09-22 window missed?

**Yes for complete full-window capture of game 1 (PHI@CHI).**  
T−7d for that game began **2026-09-21 20:15 ET**. By afternoon 2026-09-22 ET the window had already been open ~20+ hours with **no** durable collector documented as running. Per protocol: label incomplete; **do not backdate** admission; do not call partial coverage complete.

Remaining games in the **same** reserved registry can still get full windows **if** capture starts before *their* T−7d and identities are verified — but the **32-game complete-cohort** gate (`evaluation_gate.py`: all 32 complete windows) is already broken for this registry unless every later game is complete **and** game 1 is explicitly incomplete/excluded under a revised rule (docs prefer: **new schedule-only admission** with new identity/version rather than silent replacement).

### Next actionable admit / capture deadlines (from frozen kickoffs)

| Game | Kickoff (UTC) | T−7d (UTC) | T−7d (ET) | Notes |
|---|---|---|---|---|
| PHI@CHI (first) | 2026-09-29T00:15Z | 2026-09-22T00:15Z | **2026-09-21 20:15 ET** | **Missed** for full window |
| PIT@CLE | 2026-10-02T00:15Z | 2026-09-25T00:15Z | **2026-09-24 20:15 ET** | Next clock if staying on this registry for *partial* capture research — still needs identity + collector **before** this instant |
| IND@WAS | 2026-10-04T13:30Z | 2026-09-27T13:30Z | **2026-09-27 09:30 ET** | Later |

**Recommended Conductor choice:** treat current 32-game registry as **ineligible for complete-cohort profit comparison**; assign **ADMIT-1**: new schedule-only freeze of future games whose entire T−7d starts **after** collector+identity readiness (do not peek outcomes). Use PIT@CLE deadline only as a stretch target if owner wants salvage partial tape — not as a substitute for a clean cohort.

---

## 4. Kit restore (`scripts/restore_kit.py`)

**What it does:** takes one owner-supplied ZIP; SHA-256 must uniquely match `provenance/ARCHIVES.json`; extracts only paths indexed under that kit prefix in `EXTERNAL_ARTIFACTS.json`; verifies bytes + hash; refuses overwrite of differing files.

**Can it run without owner kits?** **No.** Clone alone is insufficient (root README).

**Blockers:**

1. Eight kit ZIPs are **not in Git** (`.gitignore` includes `*.zip`; also `*.jsonl.gz`, `*.csv.gz`).  
2. `ARCHIVES.json` lists kits by path/size/sha only (indexes ≠ downloads), e.g. `nfl_factorial_lab_20260921/NFL_Allocation_Factorial_Kit.zip` (~62 MB), through Q1–Q6 + maker/strategy kits (~255 MB zip total).  
3. `EXTERNAL_ARTIFACTS.json`: **718** files · ~**330 MB** omitted bytes (normalized inputs, compressed ledgers, raw captures, stern results, etc.), keyed by path/sha — top dirs: queue/completion/timing/factorial/maker dominate.  
4. Full historical Q6/Q7 ledger replay and many offline runners need those restored inputs; **unit tests** are designed to run without full external data (README).

**Assignable packet “KITS-1”:** obtain matching ZIPs from project owner/deliverables → `python3 scripts/restore_kit.py /path/to/NFL_Allocation_Factorial_Kit.zip` (and others as needed) → confirm restored counts; never commit restored binaries.

---

## 5. Provenance gap summary (full replay)

| Layer | In Git | Missing for full replay |
|---|---|---|
| Specs, code, tests, JSON summaries, freeze hashes | Yes | — |
| Kit ZIP binaries | No (gitignored) | All 8 `ARCHIVES.json` kits from owner |
| Indexed external file bytes | No | 718 paths in `EXTERNAL_ARTIFACTS.json` |
| Always-on forward tape | No | Collector deploy + holdout panel + identities |
| Completed fresh games | Zero | Time + capture |

---

## 6. Concrete next actions Conductor can assign

**Priority recommendation (time vs science):**

1. **COLLECTOR-1 first (time-critical):** stand up Q4 GET-only recorder on durable host; resolve identities; either salvage PIT@CLE+ windows under explicit incomplete-cohort labeling **or** (preferred) cut **ADMIT-1** new schedule-only cohort before its T−7d. Missing Sep 22 start cannot be fixed by backdating.  
2. **KITS-1 (unblocks offline fidelity):** owner supplies ZIPs → `restore_kit.py` for factorial (+ prior labs if needed).  
3. **Q7-IMPLEMENT (offline science, parallelizable after kits for full run):** new `nfl_paircheck_lab_20260922`, freeze spec, implement 2×2, run 16 scenarios — **no orders**. Unit-test-first possible before kits; full ledger verification needs KITS-1.  
4. **SHADOW-1 (after collector + freeze):** replay identical received stream into isolated 5k accounts: original / Q6 `000` / optional Q7 winner — per `FORWARD_PROTOCOL.md`. Still no live promotion.

**Do not assign:** live order placement, credentialed trading, invented P&L, silent holdout game swaps, mutating frozen Q1–Q6 evidence trees in place.

---

## 7. One-line status for Conductor MO

Q7 is a clean offline 2×2 still to implement; durable public collector **code exists** under `nfl_timing_lab_20260921/collector/` but is **not running**; first T−7d (**2026-09-22T00:15Z**) for the reserved 32-game cohort is **missed** for PHI@CHI full window — next clean path is new admission (or explicit partial salvage before **2026-09-24 20:15 ET** PIT@CLE T−7d); full replay blocked until owner kits hit `restore_kit.py`.
