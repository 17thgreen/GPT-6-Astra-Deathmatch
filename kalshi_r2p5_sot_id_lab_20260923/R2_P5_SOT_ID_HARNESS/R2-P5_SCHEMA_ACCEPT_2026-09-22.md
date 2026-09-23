# R2-P5 — Archivist schema acceptance (Collector stub)

**When (ET):** 2026-09-22 ~6:59pm America/New_York  
**Seat:** The Archivist (Registry)  
**Cite:** Conductor R2 triage ADMIT · `briefs/R2_DEEP_RESEARCH_2026-09-22.md` §R2-P5 · `packets/R2-P5_ADVERSE_FIELD_LIST_2026-09-22.md` · Collector proposed field names  
**Status:** SCHEMA_ACCEPTED · Collector may land GET-only JSON schema stub  
**Hard rules:** Provenance/scorecard gate only — not a strategy. No ADMIT-1 / PIT@CLE budget steal. No invented PnL. No orders.

## Registry / experiment ids

| Kind | Id |
|---|---|
| Packet | `R2-P5` |
| Schema registry | `REG-R2-P5-SCHEMA-20260922` |
| Experiment | **none** (measurement gate; do not mint a strategy experiment id) |

## Preferred paths

| Role | Path |
|---|---|
| JSON schema stub (Collector lands) | `lab/governance/astra/registry/schemas/r2_p5_admit_fields.schema.json` |
| This acceptance | `lab/governance/astra/packets/R2-P5_SCHEMA_ACCEPT_2026-09-22.md` |
| Prior field list (Deep Research attach) | `lab/governance/astra/packets/R2-P5_ADVERSE_FIELD_LIST_2026-09-22.md` |

## A. Kickoff SoT block (always required on panel events)

| Field | Type | Note |
|---|---|---|
| `event_ticker` | string | Kalshi event id (required; from attached field list) |
| `series_ticker` | string | e.g. `KXNFLGAME` |
| `holdout_kickoff_utc` | string\|null | ISO-8601; null if no holdout |
| `kalshi_occurrence_datetime` | string | **Source of truth** for windowing (ISO-8601) |
| `delta_kickoff_sec` | int\|null | **Rename** from Collector `delta_sec` · `occurrence − holdout` seconds, signed · null if no holdout |
| `window_clock_source` | enum | **Rename** from Collector `window_clock_used` · `kalshi_occurrence` \| `holdout_mixed` \| `unknown` · Collector must prefer `kalshi_occurrence` for T−7d / capture windows |
| `t_minus_7d_utc` | string | **Prefer** over Collector `t_minus_7d_start_utc` (alias OK in stub comments only) · window start under `window_clock_source` |
| `sot_pin` | string | **Accept** · must equal the `kalshi_occurrence_datetime` value that drove windows |
| `panel_version` | string | Admit stamp (Archivist) |

**Refuse:** mixing holdout + occurrence clocks in one panel without `window_clock_source=holdout_mixed`.

## B. R1-P3 adverse join (nullable until external odds present)

| Field | Type | Note |
|---|---|---|
| `external_odds_present` | bool | **Accept** Collector · gate for nullability of edge/hedge fields |
| `edge_at_quote` | float\|null | null unless `external_odds_present` |
| `edge_at_fill` | float\|null | null unless odds/fill path |
| `hedge_complete_flag` | bool\|null | fee-aware via R1-P1; null if no odds/fill path |
| `odds_age_sec` | float\|null | |
| `fee_model_ref` | string\|null | **Accept** · pin to R1-P1 feebook id/version; **required when** `hedge_complete_flag` is non-null |
| `de_vig_method` | enum\|null | `proportional` \| `shin` \| `other` · freeze before fills (from attached field list) |
| `edge_lost_cancel` | bool\|null | optional companion |

## Explicit non-owns

- Not a strategy score; no Examiner KEEP/KILL from this schema alone.  
- Does not reopen Q6-`000` or Q7.  
- Does not admit a second live panel competing with ADMIT-1 / PIT@CLE.

## Accepted-at

`2026-09-22T18:59:04-04:00` ET
