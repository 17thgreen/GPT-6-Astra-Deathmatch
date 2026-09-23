# R2-P5 SOT / IDENTITY AUDIT HARNESS — FREEZE KERNEL 2026-09-23 (ET)

**Owner:** R&D Variants (harness freeze / implement) → Simulator → Examiner  
**Status:** FROZEN — Conductor MAXIMIZE NEXT after L2-CAT PR28 merge @`e54554ff`  
**Cite:** Parent Archivist accept `R2-P5_SCHEMA_ACCEPT_2026-09-22.md` (sha256 `712e4771bf2783dbee1e4c553194cd2896a468184f2849f24e58c3eb350ff499`); ADMIT-1 SoT seed `R2-P5_SEED_INSTANCE_ADMIT1_SOT_ONLY_2026-09-22.json` (sha256 `1edfa91979ab5dac72e28cc5e2ad5ff08aab414b5574fe115f86fb7d85e2ac4b`; 16 rows; panel_version `2026-09-22.1-kalshi-occurrence-sot`; admit_stamp `2026-09-22T21:18:13Z`); schema `r2_p5_admit_fields.schema.json` (sha256 `da7f6badd37d52fbd977681924379c3552f0dbfec94729d86ea411fb473ce53c`); PIT@CLE identity hash freeze `f5ca19f15940a80476d1590e506951df87df619160b477f1dff06cc3554cb520`  
**Repo:** `https://github.com/17thgreen/GPT-6-Astra-Deathmatch`  
**Packet ID:** R2-P5-SOT-ID-HARNESS  
**Feature family:** **SOT-ID** (kickoff SoT + holdout identity audit) — ≠ Cap-SR / Cap-SR-FX / MVE-FL / NCAAF-FQ / PROP-LQ / L2-CAT / F1–F3  
**Nearest dead card:** Mixing holdout + occurrence clocks without `window_clock_source=holdout_mixed` (R2-P5 refuse). Also refuse: inventing adverse/odds when `external_odds_present=false`; Q6-`000` retune; Cap-SR/QF/L2-CAT reopen; ATL@GB; live orders.  
**Hard rules:** Measurement-only provenance gate. GET-only / offline seed. No Logan keys. No live orders. No invented PnL/odds. No `admit.py`. No second live panel competing with ADMIT-1. `results`/`pnl` null until Examiner.

## Why SOT-ID (oldest leftover this slot)

Excluded (Conductor hard WAIT / closed): S2+R2-P4 until C1 smoke PASS; R3-P2 until Logan demo/paper keys; S1 empty-events deferred; R3-P1 FIXTURE_GAP (auth `fee_cost` absent); QF/Cap-SR/Cap-SR-FX reopen denied; Q6-`000` retune denied; ATL@GB denied; L2-CAT just merged — no reopen.

R2-P5 is SCHEMA_ACCEPTED with an authentic ADMIT-1 SoT seed (16 events, all `kalshi_occurrence`, uniform `delta_kickoff_sec=10800`) and needs no new Logan credentials. Orthogonal to fee/queue/L2 shape Feature families already landed.

## Intent (one knob)

Holding **R1-P1 feebook** and **R1-P5 rails** as import-only references (adverse hedge fields stay null unless odds present), wire a SoT/identity audit harness on the R2-P5 ADMIT-1 seed: verify `sot_pin` vs `kalshi_occurrence_datetime`, `window_clock_source` discipline, and holdout `delta_kickoff_sec` consistency (incl. PIT@CLE identity-join cite).

**One knob only:** audit slice ∈ {`sot_pin_match`, `holdout_delta_bin`} with schema+seed fixed.

**Not arms:** inventing external odds; rewriting holdout kickoff to match SoT in place; opening S2/R2-P4; stealing ADMIT-1 poll budget; Cap-SR/L2-CAT reopen.

## Pins

| Pin | Value |
|---|---|
| Parent accept | sha256 `712e4771bf2783dbee1e4c553194cd2896a468184f2849f24e58c3eb350ff499` |
| Seed instance | sha256 `1edfa91979ab5dac72e28cc5e2ad5ff08aab414b5574fe115f86fb7d85e2ac4b` · 16 rows · `admitted` via ADMIT-1 stamp (not this harness admit) |
| JSON schema | sha256 `da7f6badd37d52fbd977681924379c3552f0dbfec94729d86ea411fb473ce53c` |
| PIT@CLE identity cite | sha256 `f5ca19f15940a80476d1590e506951df87df619160b477f1dff06cc3554cb520` (hash freeze; not a re-admit) |
| Fee (import-only when hedge non-null) | `kalshi_feebook_lab_20260922/` @`22371178cb2663250b4762f328069571c48cb551` |
| Rails (import-only labels) | `kalshi_rails_lab_20260922/` @`6a28e0d6254327ea4e6451c781bec56215ac6cac` |
| Strategy | **None** — provenance / Clock join gate only |

## Arms

| Arm | Name | Slice |
|---|---|---|
| **R2P5A0** | SoT pin match | Assert `sot_pin == kalshi_occurrence_datetime` and `window_clock_source=kalshi_occurrence`; refuse silent holdout_mixed |
| **R2P5A1** | Holdout delta bin | Partition/audit `delta_kickoff_sec` bins (seed=10800); refuse inventing odds/adverse when `external_odds_present=false` |

## Dead-card / live-pin overlap (named)

| Pin / card | Overlap | Handling |
|---|---|---|
| Q6-`000` / Q7 | Schedule calendar only | No retune; SoT gate ≠ allocator |
| Cap-SR / QF / L2-CAT | Closed / just merged | Do not reopen |
| S2 / R2-P4 | Hard WAIT on C1 smoke | Stay queued; this packet does not ungating |
| ADMIT-1 / PIT@CLE | Uses seed + identity cite | No second competing admit; no poll steal |
| R3-P1 / R3-P2 | Fixture gap / keys WAIT | Stay deferred |

## Scorecard fields (null now)

`sot_pin_mismatch_n`, `holdout_mixed_refuse_n`, `delta_kickoff_sec_mode`, `identity_join_ok_n`, `external_odds_invent_refuse_n`, `results`, `pnl` — null until Examiner.

## Lab dir

`kalshi_r2p5_sot_id_lab_20260923/` (do not mutate Q / Cap-SR / Cap-SR-FX / C3 / C5 / R3-P3 / R3-P4 / L2-CAT / S4 / S5 / R2-P3 / feebook / rails / ADMIT-1 recorder).

## Integrity (Clock gate)

Commit the **attached** Conductor-box freeze / parent accept / seed / schema bytes **verbatim**. Pin digests to `sha256sum` of those files. **Refuse labeled recreations / empty seeds.** Do not invent odds or rewrite holdout kickoffs.

## Merge gates

Units green; `results`/`pnl` null; Examiner stub_ready NOT_SCORED after merge.
