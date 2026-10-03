# Examiner (Kalshi) scorecard TEMPLATE — v1.2 (RATIFIED)

**Seat:** Examiner (Kalshi) · Astra desk  
**Status:** **RATIFIED** · ratified by **Conductor** · ratified_at_et **2026-09-24 ~19:37 ET** (ruling: "v1.2 defaults")  
**Filed:** 2026-09-24 19:37 ET (approximate) · Conductor message id `50948621-ce91-47df-b661-12e9df823fe2`  
**Machine-readable:** `lab/governance/astra/templates/EXAMINER_KALSHI_SCORECARD_TEMPLATE_v1.2.json`  
**Supersedes:** v1.1 — not edited in place  
- `lab/governance/astra/templates/EXAMINER_KALSHI_SCORECARD_TEMPLATE_v1.1.json` sha256 `4042e4f63bdba98faca8fe2f741556dc79260cffbc28d293dc834ba40fa29ffd`
- `lab/governance/astra/templates/EXAMINER_KALSHI_SCORECARD_TEMPLATE_v1.1.md` sha256 `7880d0d135b001250ebb637866d46289486c8cf7435e9f1c11fb055f11e8d52a`
- v1.1 revision note `lab/governance/astra/packets/EXAMINER_KALSHI_SCORECARD_TEMPLATE_REVISION_v1.1_2026-09-24.json` sha256 `f2ce985d8e2a85d63336bbbb36b6e9f924959e06fad68060ae17850c178c6cfd`

**Research source:** `lab/governance/astra/research/KALSHI_EDGE_RESEARCH_2026-09-24.pdf` (sha256 `7e55bc26…8b45e`), pp. 15–16; cards 01–04 on pp. 5–8. The PDF footer reads "research, not a profit claim".  
**Scope:** Template revision only. **No existing EXAMINER_* stamp was edited, re-scored, or re-opened.** No numbers are populated.

## Changelog
- **v0 (implicit):** the shape used by the EXAMINER_SCORECARD_STUB_* / ACK_* / SCORECARD_* stamps, 2026-09-22 to 09-24.
- **v1 (2026-09-24):** added common_scorecard, controls, fee_regime, proposed_optional, and rules. All values null.
- **v1.1 (2026-09-24):** Conductor ratified v1 plus defaults. This version adds:
  - the default override policy
  - ruling definitions and units for 8 metrics
  - a per-metric `override_rule`
  - the rewards rule
  - a `simulated_fills` section
  - four blocks adopted from proposed_optional: `study_label`, `stress_sensitivity`, `executable_dollars_per_day`, and `preregistration_checklist` (a REQUIRED gate for cards 01–04)
  
  The other 10 proposed_optional items stay unadopted. Both net P&L columns stay null until the Archivist manifest lands.

---

## v1.2 changelog
- **v1.2 (2026-09-24):** adopted the four Conductor defaults and canonical study-label source. Calibration bins, adverse-selection sign/formula, event-concentration HHI basis/scale, and executable $/day formula/reporting are resolved. The four items are removed from pending questions. All metric values remain null; existing stamps are untouched.

## Section A — v0/v1 shape (unchanged)
The scorecard header, pins, gates, verdict, and so on are carried over from v1.1 unchanged (`scorecard` block copied verbatim into the v1.2 JSON).

MD stamp section order, with v1.1 and v1.2 additions in **bold**:
1. Header
2. **Study label**
3. **Preregistration checklist** (cards 01–04)
4. Pins
5. Gates
6. Verdict + headline
7. Arms
8. Metrics
9. Frozen bar / fee-honest P&L
10. Common scorecard
11. **Simulated fills (separate)**
12. **Stress sensitivity**
13. **Executable $/day**
14. Controls
15. Refused-if
16. Score gate
17. Pointers + Stamped

## Section B — Default override policy (ruling)
A packet freeze may override any default **only by declaring the override before outcomes are seen**. Otherwise the defaults apply. Each metric carries `override_rule: "freeze may override only if declared pre-outcome"`. An override declared after outcomes is inadmissible.

## Section C — Fee regime (unchanged from v1)
- **Feebook pin:** `astra.r1p1.feebook.claude_order_level_ceil.v1`.
- **Archivist fee/account-version manifest:** path, sha256, and manifest_id are **null**; status is **pending**.
- **Check at v1.1 filing:** I searched lab/ for this manifest and **did not find it** (no Archivist manifest dated 2026-09-24). Even after it lands, values are not populated automatically; Conductor gets notified instead.

## Section D — Common scorecard (v1.2 defaults; every metric value remains `null`, `measured=false`)

| Field (v1 key) | Ruling label | Definition (Conductor default) | Unit | Notes |
|---|---|---|---|---|
| `net_pnl_without_rewards` | net P&L w/o rewards | As in v1 (p15 components). **KEEP basis.** | USD | Null until the Archivist manifest lands. The formula is still pending_definition. |
| `net_pnl_with_rewards` | net P&L with rewards | As in v1 | USD | Always reported side by side with w/o rewards. Null until the manifest lands. |
| `rewards_actually_earned` | rewards earned | Unchanged: cash received only, never an ideal estimate | USD | — |
| `calibration` | calibration | Brier score plus 10 equal-width bins on [0,1], with per-bin counts; bins 1–9 are half-open and the last bin is closed [0.9,1.0]. Flag a bin as **thin** when n<10. | Brier (dimensionless) + table | The value is **"N/A"** (not null) when the strategy is not probabilistic. All measured values and counts remain null until measured. |
| `fill_rate` | fill_rate | Filled contracts ÷ requested contracts, at order level. Only fills tagged **demo / shadow / live** count. | fraction | Replay/simulated fills go in `simulated_fills` and never count toward KEEP. |
| `adverse_selection_after_fills` | post_fill_adverse_selection | At +60s, +300s, and settlement, `(mid_t − fill_price) × side`, where side = −1 for a buy and +1 for a sell. Positive means the mid moved against our side (a cost to us). | cents/contract (signed) | Buy at 50, mid 40 gives +10; sell at 50, mid 60 gives +10. |
| `feasible_vs_requested_size` | feasible_vs_requested | Fraction of requested size that visible depth supported at decision time, taken from the book at receipt time | fraction | — |
| `unresolved_inventory` | unresolved_inventory | Open contracts and dollar risk at window end, marked at conservative (bid-side) value | contracts + USD | — |
| `capital_hours` | capital_hours | Σ(max collateral at risk × hours held) | USD-hours | — |
| `drawdown` | drawdown | Max peak-to-trough on cumulative net P&L **without** rewards | USD | Depends on net P&L, so null until the manifest lands. |
| `event_concentration` | event_concentration | Top-1 event share of positive net P&L plus HHI over events. HHI uses each event’s share of **absolute net P&L without rewards**, on a **0–1** scale (sum of squared shares). **Flag top-1 if >50%.** | fraction + HHI | Top-1 positive-net-P&L share remains a separate flag. P&L-based, so null until the manifest lands. |

## Section E — Rewards rule (ruling; p15 is law)
- P&L without rewards and P&L with rewards are **always reported side by side**.
- **KEEP is judged on P&L without rewards.** The only exception: the packet freeze explicitly declares the rewards thesis before outcomes are seen, and this applies to **card 03 only**.
- p15: "Do not hide a negative forecasting strategy inside a positive subsidy. Likewise, do not count an ideal reward estimate as cash received."
- `rewards_actually_earned` is unchanged from v1.

## Section F — Simulated fills (separate; never count toward KEEP)
| Field | Value |
|---|---|
| label | `simulated` |
| included tags | replay, simulated |
| `fill_rate_simulated` | null (fraction) |
| filled / requested (simulated) | null / null |
| counts_toward_keep | **false** |
| fill_model_ref | null. The fill model must be frozen per p16. |

## Section G — Stress sensitivity (adopted; p16 "sensitivity to worse queues, latency and costs")
| Scenario | Definition | Net P&L w/o rewards | Net P&L with rewards |
|---|---|---|---|
| `one_tick_worse` | every fill one tick worse against our side | null | null |
| `fees_2x` | fees doubled vs the fee regime | null | null |

Both scenarios are P&L-based, so both stay null until the Archivist manifest lands.

## Section H — Executable dollars per day (adopted; p15)
Value: null. Unit: USD/day. For each signal: `min(requested size, visible depth at our limit price or better in the book at receipt time) × per-contract edge net of fees`, where `edge = expected value − price paid`. Sum by calendar day in ET. Report the median day and p10 day; never report the mean alone. Value remains null until the Archivist fee/account-version manifest lands.

## Section I — Study label (adopted)
Value: null. Allowed values:
- `unit-only`
- `synthetic`
- `historical replay`
- `prospective shadow`
- `live`

**Source:** canonical per the Conductor ruling: PDF p16 ("Mark each study as unit-only, synthetic, historical replay, prospective shadow or live."), with the Conductor routing step 0 assigning this to the Archivist. **Archivist should adopt these five names exactly.**

## Section J — Preregistration checklist (adopted; **REQUIRED gate for new cards 01–04**)
Source: PDF p16, "Minimum preregistration". Everything must be frozen **before the test**. Every status is null.

| # | Item | Status |
|---|---|---|
| 1 | Freeze the market universe | null |
| 2 | Freeze the exclusions | null |
| 3 | Freeze the receipt-time information set | null |
| 4 | Freeze the fee regime | null |
| 5 | Freeze the order timing | null |
| 6 | Freeze the sizing | null |
| 7 | Freeze the fill model | null |
| 8 | Freeze the stopping rules | null |
| 9 | Freeze the evaluation metrics | null |
| 10 | Limit candidate variants | null |
| 11 | Log every attempted variant | null |
| 12 | Separate discovery, tuning and untouched evaluation periods | null |

p16 also says: "Sampling more prints from the same event does not solve small-sample uncertainty." That is context, not a checklist item.

Cards 01–04. Titles are from PDF pp. 5–8; assignments are from `packets/CONDUCTOR_ROUTING_KALSHI_EDGE_RESEARCH_2026-09-24.md`.

| Card | Title | On disk | Freeze |
|---|---|---|---|
| 01 | Neglected-market hybrid forecasts | `packets/card01_hybrid_forecast/`, which holds only GET series lists | none |
| 02 | Station-specific weather nowcasts | `packets/card02_station_weather/`, which holds only a GET series list and markets_open | none |
| 03 | Selective liquidity-reward allocation (the only card where a rewards thesis can be declared) | No card03 directory. Related AMS reward work, not labeled card 03: `lab/tmp/ams_branch_ro/all_market_structure_20260924/reward_*` | none |
| 04 | Stale quotes in subsidized perpetuals | No card04 directory. Likely related, not labeled card 04: `packets/scout_perps_screen_2026-09-24/` | none |

## Section K — Controls (unchanged from v1)
`market_only`, `simple_model`, and `no_trade` apply per packet. Each stays null until that packet's freeze declares it.

## Section L — Proposed optional: still unadopted (10)
These are listed only; they are null and not scored.
- uncertainty by event or day
- independent opportunities
- correlation with existing positions
- fees reported separately
- capital cost
- inventory liquidation/settlement P&L
- risk-adjusted net $/capital-hour
- attempted-variants log
- period separation
- single-event dependence

Note that attempted-variants log and period separation also appear as checklist items 10–12. Only the standalone scorecard fields stay optional.

## Section M — Rules (v1 rules as amended, plus v1.1 and v1.2 additions)
1. Values stay null with `measured=false` until measured on a frozen packet. The one exception: calibration is "N/A" when the strategy is not probabilistic.
2. Never back-fill from scout N, unit counts, fixtures, admit flags, or estimates.
3. The net P&L formula remains pending_definition and gets no Examiner-invented formula. The v1.2 defaults resolve calibration bin edges, the adverse-selection sign, HHI basis/scale, and executable $/day formula.
4. P&L with rewards and P&L without rewards are always reported side by side. KEEP is judged on P&L without rewards, except for a rewards thesis declared before outcomes in a card 03 freeze.
5. `rewards_actually_earned` counts cash received only.
6. Fee-honest P&L needs both the feebook pin and the pinned Archivist manifest. When the manifest lands, values are not populated automatically.
7. A freeze may override defaults only if the override is declared before outcomes are seen.
8. `fill_rate` counts demo, shadow, and live fills only. Simulated fills are kept separate and never count toward KEEP.
9. The preregistration checklist is required for cards 01–04 before any scoring.
10. Controls apply per packet.
11. This template revision does not alter any existing stamped verdict.
12. The v1.2 defaults are canonical unless a packet freeze declares a pre-outcome override; all metric values remain null.
