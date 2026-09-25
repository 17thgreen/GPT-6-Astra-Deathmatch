# ATP KXATPMATCH MEASURE-MODE HARDENING: INFRA FREEZE, 2026-09-24 (ET)

**Owner:** R&D Variants "KALSHI". **Status:** FROZEN. HOLD for Conductor ACCEPT (no CloudAgent, no PR, no repo edit, no admit.py, no live orders).
**Stamp:** 2026-09-24T20:14:43-04:00. **Base:** main@`e8770f1e48c364f3006d6e1909ed6b63652f3785` (PR54 squash; clone verified; 13/13 existing units OK).
**Canonical spec:** `VARIANTS_FREEZE_ATP_KXATPMATCH_MEASURE_HARDENING_INFRA_2026-09-24.json` · sha256 `1b7f3ab4705e00b9d2835ec759d23ef9434999b8e070d02010008dd653347c58`. If this summary and the JSON disagree, the JSON wins.
**Class:** INFRA, one-knob-NEUTRAL. `join_gate` (J0/J1) stays the only knob. This freeze adds no arm, metric or cohort rule.

## Problems (from the UNADMITTED smoke, 20:04:41-20:08:15 ET)
- (a) The run sweeps the full settled history and always hits both endpoints: 12 GETs, 11 × 429, 1 × 200.
- (b) `/markets` failed and `/events` stopped at p1, yet the output shows `cohort_source=events_nested` with no PARTIAL marker.
- (c) `settled_join_n=0` was emitted as 0 even though 2 gaps were open.

## Changes (orchestrator.py measure transport + new tests only)
1. **Server-side time filter.** `/markets` gets `min_settled_ts=floor(epoch(since))` (1790293920). The docs list it as compatible with `status=settled`. `min_close_ts` with `status=settled` is documented as **incompatible** and is not used. The endpoint order is **single-endpoint-first**: `/events` is called only after a `/markets` gap, with `min_close_ts = since − 48 h`. A 400 never triggers an unfiltered history re-sweep. The run records whether the filter was OBSERVED_HONORED, OBSERVED_IGNORED, REJECTED_400 or UNOBSERVED. **The client-side `settlement_ts > since` check stays the authoritative gate.**
2. **Collector budget limiter** (budget sha256 `7cb43886…`, which includes Addendum 1). It fails closed: with no Collector grant, zero GETs are sent. The ceiling is list ≤4 rpm and total ≤10 rpm with a 6 s floor in Phase A, stepping down at **2026-09-27T16:30Z (12:30 ET)** to list ≤2 rpm and total ≤5 rpm with a 12 s floor. The Collector audit slice is ≤3 rpm with a 20 s floor and pauses in Phase B. After 2026-10-02T06:15Z the limiter refuses. **NFL yield:** a `FORCE_PHASE_B` flag or any new recorder 429 (read-only check) switches to Phase B caps; if the check can't be read, Phase B is assumed. No GETs run in the relaunch window 22:52-22:56Z. **Backoff:** Retry-After, else 30/60/120/240 s capped at 600. At most 1 retry. +2 s spacing for 30 min after a 429. PAUSE_429_STORM (10 min) after 3 or more 429s in 10 min. The 429 JSONL fields match the budget exactly.
3. **Labels.** New output fields: `cohort_completeness` ∈ {COMPLETE, PARTIAL, INCOMPLETE}, per-endpoint `pull_status`, `counts_label`, `counts_are_lower_bounds`, `zero_with_gaps` and `cohort_source_qualified`. **Any gap → counts INCOMPLETE. A 0 with gaps is not zero.**

## Invariants
- J0/J1, `j1_label` fallback, the 30-ticker scout exclusion and the `since` gate are unchanged. The source sha256 of 9 join functions is pinned to e8770f1e.
- `tests/test_orchestrator.py` stays byte-identical (sha256 `b1c6dbe0…`) and all 13 tests must pass.
- The legacy 10/20/40×4 schedule survives only as `rate_policy=legacy_stub_unit_only` for injected stubs, because test_429 asserts it. That policy is refused when `live_fetch` is true.
- 17 new stub tests (no network) cover the filter param, the limiter and step-down, the NFL tripwire, backoff, the 429 log, the PARTIAL/INCOMPLETE/zero-with-gaps labels, the join-output identity check and the function-source digests.
- GET-only on the v2 host. No auth, no admit. `results`, `pnl`, `settled_join_n` and `admitted_at` stay null.

## API evidence
- **Docs** (saved under `/workspace/tmp/atp_hardening_probe/docs/`): `/markets` `min_settled_ts`/`max_settled_ts` ↔ `settled`; `min_close_ts`/`max_close_ts` ↔ `closed`/empty only; `/events` `min_close_ts` = "at least one market close ts > X". A 429 carries no Retry-After.
- **Live probe:** NOT RUN, 0 GETs sent. Budget Addendum 1 bars Variants from direct GETs. The 4 probes are logged as gaps and drafted for Collector (`COLLECTOR_ROUTING_REQUEST_DRAFT.json`). The filter is documented but not live-verified [U].
- **Post-ACCEPT settlements:** none on the one page already received. That is smoke `/events` p0 at 00:07:04Z: 100 events, 200 markets, max settlement_ts `2026-09-24T14:40:28.099145Z`. Gaps remain (`/markets` p0 429×4, `/events` p1 429×4), so this is **INCOMPLETE, not zero**.

## p16 (7 satisfied / 5 n/a / 0 missing) and v1.2
Both are embedded in the JSON (`p16_preregistration_checklist`, `examiner_scorecard_v1_2`). Every value is null.

## Pins (sha256)
- ATP-RJ ACCEPT: `e42d75834086f34090581aee88563ab9849d60864c2d9e59c4ef495b3e8e5af5`
- PR54 merge packet: `d02674a0c91430fcf98ba50e921cf097ade4caa27e28ff080aff806dd80de8fb`
- GET budget: `7cb4388681b950cf535a0d30a4bec44191ef809c40ef6f36b887de399fa30d22` (supersedes the cited 11eeeaf2 revision, which is not on disk)
- v1.2 template: `56bcf6269a42031d9d90496e9a65c2292321aed2165033f6fb44ff8cc4d6b1cc`
- ATP-RJ freeze: `dc9fcb326a97ce24267ed96438bf403687bc9aef6b79dccef3483d0e4cdeeb69`
