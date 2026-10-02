# CARD 02 — Station weather nowcast (KXHIGH × 4 stations): measurement kernel FREEZE, 2026-09-24 (ET)

**Packet ID:** CARD02-STATION-WX-NOWCAST
**Series:** `KXHIGHLAX`, `KXHIGHMIA`, `KXHIGHNY`, `KXHIGHCHI` (daily max-temperature ladders). Daily lows (`KXLOWT*`) are excluded in v0 because they are thin; see raw values below.
**Owner (freeze):** Deep Research
**Implementer (later, only after Conductor ACCEPT):** Collector (GET-only 60-day archive), then Variants (nowcast and baselines), then Examiner (scorecard v1.2 + p16 checklist). Adversary checks overlap. Archivist records the fee/account manifest.
**Reviewer:** Conductor
**Status:** **FROZEN (design only)**. `results` = **null**, `pnl` = **null**. Not run. Study label (scorecard v1.2 §I): `prospective shadow` once collection starts. Today it is design-only.
**Governing charter (current): v1.1**, `charters/DEEP_RESEARCH_MASTER_BRIEF_v1_1_2026-09-24.md`, sha256 `02272754b01da5b65edd837545e485f4fd4dff2903a7ae1f52d9cb5e616fec5d` (required prefix 02272754 verified). It supersedes v1 `charters/DEEP_RESEARCH_MASTER_BRIEF_v1_2026-09-24.md` (sha256 `6a02cb468a4b6c600fc3a16078a216a6095321c6bc92c24b2a7aca58f149daa8`), under which this kernel was frozen at 23:47:00Z. v1.1 adds, for every promising source, a smallest useful experiment vs a simpler baseline after costs plus the needed market adaptation (see the v1.1 source maps). The reference was bumped at 2026-09-24 ~20:05 ET as a documentation-only change; no frozen parameter, universe, weight, knob, pre-commit file or result was changed. The kernel's sha256 at freeze was `9624ab2498e88896c46e8fd984211b4b8839e613567209841358d7cf5059e5d6`; `FROZEN_EXPERIMENT.json` keeps it and also records the post-bump hash.
**Cite:**
- `research/KALSHI_EDGE_RESEARCH_2026-09-24.pdf` Card 02 (rejection rule quoted verbatim below) and the p16 minimum preregistration.
- `packets/CONDUCTOR_ROUTING_KALSHI_EDGE_RESEARCH_2026-09-24.md`: Card 02 has Deep Research pick 3–4 stations and the settlement mapping; the Collector runs a GET-only 60-day archive.
- `packets/MAXIMIZE_PIN_2026-09-23_1455ET.md`: "Bias: Prefer work that can become Examiner-scorable (Clock admit + settled/authentic join, or strategy rehab with frozen PnL path) over new sibling fee+queue measurement stubs." This card is built toward a settled CLI join, not another fee/queue stub.
- `templates/EXAMINER_KALSHI_SCORECARD_TEMPLATE_v1.2.md` §J.
- R1-P1, R1-P5.
**Hard rules:**
- No live orders. No invented PnL. No Q6-`000` retune.
- Do not ungate S2/R2-P4 (`KXNFLSPREAD`/`KXNFLTOTAL`).
- Exactly one knob.
- GET-only public data. Never fill gaps. Missing or stale feeds count as missing evidence.

Sources are listed in `packets/card02_station_weather/SOURCE_MAP_2026-09-24.md` (v1.1 format). The explore/confirm ledger is `packets/card02_station_weather/LEDGER_2026-09-24.md`. The Collector handoff is `packets/card02_station_weather/COLLECTOR_HANDOFF_STATION_LIST_2026-09-24.md`.

---

## 0. Economic thesis (charter-required)

- **What might be mispriced:** late-day KXHIGH buckets. Once part of the climate day has passed, the final CLI maximum is bounded below by the running observed maximum. What remains depends on time of day, cloud, wind shifts, humidity and forecast revisions. The hypothesis is that some prices at 10:00–18:00 LST do not yet reflect (a) the observed running max mapped correctly into the official measurement and rounding process, or (b) the remaining-day distribution conditional on it.
- **Why it could persist:**
  - Settlement mapping is unusual. The CLI is whole °F from the rolling 5-minute ASOS average over midnight-to-midnight **LST**, so during DST the day runs 1:00 AM–12:59 AM local.
  - 5-minute METARs carry whole °C only, and converting back produces spurious °F values (NWS PSR example: 116 °F → 47 °C → 117 °F).
  - Market rules text names The Weather Company, while the contract terms and Help Center name the NWS CLI.
  - Participants who read app or METAR-converted values can be wrong by about 1 °F, which is exactly one bucket.
- **Who trades with us:** retail takers pricing from phone-app forecasts or converted METARs, and passive quotes that go stale. We would also compete against other weather bots (public GitHub weather algos exist, e.g. the C3 pointer), which is a reason to expect thin edges.
- **What disproves it:**
  1. At the headline issue time, executable ask prices on the purchased side already match or beat the nowcast's log-loss and Brier. The market is at least as good.
  2. The apparent edge is explained by rounding (edge concentrated on buckets adjacent to the °C↔°F conversion boundary, where our own mapping could equally be wrong).
  3. Net executable returns after the R1-P1 fee are ≤ 0, or depend on one station or one season.
  4. Visible depth at our limit is too small to matter (capital-hours and USD/day in scorecard v1.2 §H).
  - Live example of (1): at 23:42Z on 2026-09-24, `KXHIGHNY-26SEP25-T74` had a NO bid at 0.99 for 7,132.60 contracts. Many buckets may already be priced near certainty by T−6h.

## 1. Status ladder rung (charter)

| Rung | Reached? |
|---|---|
| code verified | **No.** There is no nowcast code and no collector for this card yet. The raw GET client used today is a research tool, not the card's code. |
| retrospective predictive evidence | No |
| hypothetical after-cost result | No |
| prospective paper evidence | No |
| observed live execution | No (forbidden) |
| scalable repeatability | No |

**Current state: pre-rung (design frozen, data plan specified).** Nothing here implies any rung.

## 2. Intent (one kernel)

For 4 stations, archive receipt-time Kalshi books and trades, receipt-time METAR/ASOS observations, and the first official non-preliminary NWS CLI. Then compare three forecasters of the CLI max bucket at a preregistered issue time:
- (i) the market: the executable ask on the purchased side, plus mid for reference only;
- (ii) a simple forecast-error distribution: the latest public NWS point forecast max plus an empirical error distribution learned in the pilot;
- (iii) a conditional nowcast: the remaining-day max conditional on the observed running max, time, cloud, wind shift, humidity and forecast change, mapped into the CLI rounding.

A no-trade control is always reported. This is **not a strategy.** Variants implements only after Conductor ACCEPT.

## 3. Station table and settlement mapping

| Series | CLI product / station (per Kalshi `rules_primary`) | ICAO | NWS WFO | Local tz | LST climate day | Close time (Sep 25 event, raw `close_time`) | Live liquidity rank (sum of open markets, events 26SEP24+26SEP25, received about 23:38–23:41Z) |
|---|---|---|---|---|---|---|---|
| KXHIGHLAX | CLILAX, Los Angeles Intl | KLAX | LOX | America/Los_Angeles (PST = UTC−8) | 00:00–23:59 PST = 01:00–00:59 PDT | 2026-09-26T08:00Z | #1: vol24 363,638.42 / OI 269,821.51 |
| KXHIGHMIA | CLIMIA, Miami Intl | KMIA | MFL | America/New_York (EST = UTC−5) | 01:00–00:59 EDT | 2026-09-26T05:00Z | #2: 187,957.74 / 117,860.25 |
| KXHIGHNY | CLINYC, Central Park | KNYC | OKX | America/New_York | 01:00–00:59 EDT | 2026-09-26T05:00Z | #3: 114,026.57 / 67,807.10 |
| KXHIGHCHI | CLIMDW, Chicago Midway | KMDW | LOT | America/Chicago (CST = UTC−6) | 01:00–00:59 CDT | 2026-09-26T06:00Z | #4: 82,253.08 / 49,861.80 |

- **Strike partition** (per event, from raw markets): T-low (`less`, <), four `between` buckets `Bxx.5` covering two integer °F each (floor and cap inclusive; e.g. B81.5 = 81–82 °F), and T-high (`greater`, >). Together these are a complete partition of integer °F, so a tie at an integer value is never ambiguous. Contract terms say "between" is inclusive and "Contract resolution is based on the full precision reported by the Source Agency" (whole °F on the CLI).
- **Rounding note:**
  - The CLI max is the highest rolling 5-minute ASOS average, stored in whole °F (NWS PSR HiRes ASOS).
  - Hourly METAR T-groups carry tenths °C, so converting them is roughly safe to ±0.1 °F before rounding.
  - 5-minute METARs carry whole °C only, so converting them back yields spurious °F values. The nowcast must use only the hourly T-group or the 6-/24-hr max groups (FMH-1 group semantics **UNVERIFIED**, not cited). It must never treat a converted 5-minute °C value as the running max.
- **Rank fragility:** CHI vs `KXHIGHTSFO` is close to a tie. CHI leads on vol24 (82,253.08 vs 80,961.94); TSFO leads on OI (51,740.79 vs 49,861.80). The tie-break is lifetime series `volume_fp` (`/series?include_volume=true`): CHI 110,703,361 vs TSFO 18,435,063. CHI also shares C3's panel. Everything rests on one snapshot. See the ledger.
- **Excluded (thin):** KXLOWTNYC 5,253.25 vol24 / 4,472.69 OI; the other KXLOWT* are about 3–4k vol24 each. KXLOWTAUS (24,295.79) is a low series outside the 4-station panel.

### Source conflict (recorded, not resolved)

| Source | What it says | Tag |
|---|---|---|
| Market `rules_primary` (raw GET) | "…according to The Weather Company" | verified (raw) |
| Series `settlement_sources` (raw GET) | weather.com / kalshi | verified (raw) |
| Contract terms GLOBALTEMPERATURE.pdf | Source agencies in hierarchical order, NWS first. "Only the first official non-preliminary report… will be used… Revisions after the Expiration Date are not included." If there is no data, the last fair price applies. | verified (PDF) |
| Kalshi Help Center (July 22, 2026) | Settles on the final NWS Daily Climate Report. Settlement may be delayed if the value is inconsistent with METAR 6h/24h highs or a final CLI is lower than a preliminary one. Explains the DST LST window. | verified (page) |
| `early_close_condition` text | "Last Trading Time will be 11:59 PM local time" vs raw `close_time` = 00:00 LST (01:00 local daylight) | **UNVERIFIED interpretation**. Collector must record both. |
| TWC value ≡ NWS CLI value | not established | **UNVERIFIED** |
| LAX CLI for Sep 23 was issued twice (08:26Z and 08:40Z), with identical values and no CCA header | illustrates how "first non-preliminary report" is ambiguous | observed (raw). Not used for scoring. |

**Settlement truth for scoring:** the Kalshi settled `result` field from a public GET after settlement, joined to the CLI value. Any day where the Kalshi result disagrees with the CLI-implied bucket is recorded as a `settlement_mismatch` event. It is excluded from the headline and reported separately. It is never "fixed."

## 4. Knob (exactly one)

**Knob:** nowcast **issue time** before the LST climate-day close, with levels {**14 h**, **10 h**, **6 h**} before close. These correspond to 10:00, 14:00 and 18:00 LST (11:00, 15:00 and 19:00 local daylight time during DST).
- **Headline (preregistered): T−10 h (14:00 LST).**
- All three levels are reported. There is no post hoc selection of the "best" level.
- Why this knob: it is the one design choice the thesis depends on. Early issue times test forecast skill. Late issue times test whether the market has absorbed the observed max. Everything else is fixed: fee instrument, fill model, sizing, universe and model family.

**Not knobs (fixed):** station set, fee pin, fill rule, sizing, model family, rounding map, exclusion rules.

## 5. Preregistration (p16 "Minimum preregistration"; scorecard v1.2 §J items 1–12)

This section declares each item. §J status fields stay **null** for the Examiner to fill.

| # | Item | Declaration |
|---|---|---|
| 1 | Market universe | All `KXHIGHLAX/MIA/NY/CHI` bucket markets for climate days inside the collection window. Lows excluded. No other series. |
| 2 | Exclusions | A station-day is excluded when any of these holds: (a) no book snapshot within ±5 min of the issue time; (b) no METAR received in the 90 min before issue time (stale feed counts as missing evidence and is logged, never imputed); (c) CLI value is MM or missing, or the Kalshi result is unavailable; (d) `settlement_mismatch` (reported separately); (e) market halted or `early_close`. Every exclusion is logged with a reason. |
| 3 | Receipt-time information set | Only bytes with a local `received_at` ≤ issue time: Kalshi book and trades, METARs from `api.weather.gov/stations/<ICAO>/observations`, the NWS point forecast (the product and its receipt time are archived), and the CLI for prior days. Server timestamps are recorded but never used to backdate. |
| 4 | Fee regime | R1-P1 feebook @ `22371178cb2663250b4762f328069571c48cb551`. The Scout cites the fee as `quadratic` / 1 for KXHIGHNY/CHI. The LAX and MIA fee fields must be read from raw series GETs by the Collector. The Archivist fee/account manifest is still pending, so net P&L stays null until it lands (scorecard v1.2). |
| 5 | Order timing | Hypothetical taker at the issue time. The price is the best ask on the purchased side in the snapshot at or before the issue time (±5 min). No resting orders. |
| 6 | Sizing | One contract per station-day, on the single bucket with the largest positive (nowcast probability − ask − fee − 2c buffer), only if that value is > 0. The `requested size` column is fixed at 1. Feasible size is min(1, visible depth at ask). |
| 7 | Fill model | Fill if visible ask quantity ≥ 1 at the snapshot. Otherwise no fill. Plus the v1.2 stress rows: one tick worse, and fees 2×. Freshness labels come from R1-P5 rails @ `6a28e0d6254327ea4e6451c781bec56215ac6cac`. |
| 8 | Stopping rules | Pilot: 60 consecutive climate days from the Collector start (a collection target, not proof of power). Evaluation: the next 60 climate days, untouched. There is no early stopping for success. Stop early only for data failure (> 30% of station-days excluded over 14 consecutive days), and report that as FAIL-DATA. |
| 9 | Evaluation metrics | Primary: paired per-station-day log-loss of the full bucket distribution, nowcast vs market-implied (normalized asks and mids, both reported) at T−10 h. Secondary: Brier, 10-bin calibration (v1.2), fill rate, adverse selection after fills, feasible vs requested size, capital-hours, drawdown, event concentration (top-1 and HHI), executable USD/day (median and p10). Net P&L with and without rewards is reported side by side and stays null until the manifest lands. Uncertainty is reported by **day** (cluster bootstrap over climate days, 10,000 resamples, stations kept together within a day because weather regimes co-move). |
| 10 | Limit candidate variants | Exactly 3 forecasters (market, simple error distribution, conditional nowcast) × 3 knob levels. No more. |
| 11 | Log every attempted variant | Any model-spec change during the pilot is logged in `LEDGER_2026-09-24.md` with a timestamp. The spec used for evaluation is frozen by hash before evaluation day 1. |
| 12 | Separate discovery / tuning / untouched evaluation | Discovery: today's snapshot (ranking only, no outcomes). Tuning: pilot days 1–60 (fit the error distribution and nowcast coefficients). Untouched evaluation: days 61–120. Evaluation days are never used for fitting. |

**Power / uncertainty plan:** there is no outcome data yet, so no honest SE can be given. At the end of the pilot, the Examiner computes the day-clustered SD of the paired log-loss difference. The evaluation window is fixed in advance at 60 days (up to 240 station-days) and **does not change** with the pilot result. A pilot estimate is used only to report the minimum detectable effect (≈ 2.8 × day-clustered SE for α = 0.05, 80% power). Per p16, "Sampling more prints from the same event does not solve small-sample uncertainty": multiple snapshots per station-day are not independent observations.

**Rejection rule (verbatim, research PDF Card 02):** "Archive original forecasts, receipt-time observations, exact station rules, books and eventual final reports for an initial 60-day pilot, then reserve future days for evaluation. Compare against the market and a simple forecast-error distribution. Sixty days is a collection target, not proof of power. Reject if extra skill fails to improve executable net returns, rounding explains the apparent edge, or profits depend on one season or station."

**Operationalized rejections (any one triggers REJECT):**
- (a) The upper bound of the day-bootstrap 95% CI of paired log-loss (nowcast − market ask-implied) at T−10 h is ≥ 0.
- (b) Executable net (R1-P1, once the manifest lands) is ≤ 0, or turns ≤ 0 under the one-tick-worse stress.
- (c) More than 50% of positive net comes from buckets within 1 °F of a °C↔°F conversion ambiguity.
- (d) Top-1 station share of positive net is > 50%.
- (e) Positive net only in one calendar month.

## 6. Dead-card / live-pin overlap

| Pin / card | Overlap | Handling |
|---|---|---|
| **FEAT-20260913-002 (W2-E strike-distance vs mid, INACTIVE)**, test TEST-20260913-003 | **Nearest dead card.** Observed-underlying-vs-strike nowcast scored against the mid on a non-oracle observation feed ("L3 ≠ oracle"). Both headlines had Δ > 0, verdict REDUNDANT/FAIL-INSUFFICIENT. There is no cemetery record. | Here, METAR/ASOS ≠ CLI is the same trap. Scoring is against the settled CLI join, never against a METAR proxy. Rejection (c) guards against rounding. |
| Sibling "weather FLB favorites / reverse-FLB weather cheap YES" (`packets/SIBLING_DEATHMATCH_REVIEW_2026-09-22.md`) | Domain-adjacent dead card with **no ID** | This is not a favorite–longshot bet. Price bands are not a feature. |
| CEM-ASTRA-20260922-001 (Q7 Arm B KILL) | None | Orthogonal |
| Archive CEM-20260910-001..003, CEM-20260911-001..005 | None (Binance microstructure) | Orthogonal |
| C3-KXHIGHNY-MEAS; C3-RJ settled-resolution join harness (knob join_gate); C3 bordering-strike harness (knob strike band) | **Shares NY/CHI inventory and the settled join** | Reuse the C3 capture at `/workspace/lab/astra-capture/c3-kxhighny/` for NY/CHI. Do not duplicate requests. Kernels stay distinct. Card 02 adds the METAR/CLI receipt-time archive and the forecast baselines. |
| R3-P3 FL maker/taker bands | Panel material only | The same KXHIGH markets may be reused. No merge. |
| `/workspace/lab/astra-capture/weather-nowcast/` (another box agent; `stations.json` = placeholder) | Possible duplicate collector | Collector must coordinate and adopt this station list, not start a second egress stream. The shared IP already produced 429s today. |
| Q6-`000` / S2 / R2-P4 | None | Q6-000 is not retuned. S2/R2-P4 stay gated. |

## 7. Mandatory instrument pins

| Dep | Pin | Rule |
|---|---|---|
| Fee | R1-P1 `kalshi_feebook_lab_20260922/` @ `22371178cb2663250b4762f328069571c48cb551` | Completed-profit claims without the feebook are refused |
| Rails | R1-P5 `kalshi_rails_lab_20260922/` @ `6a28e0d6254327ea4e6451c781bec56215ac6cac` | Freshness and queue labels, as an instrument only |
| Settlement truth | Kalshi settled `result` (public GET) joined to the first non-preliminary NWS CLI | Mismatches are reported separately |
| Capture | GET-only `https://api.elections.kalshi.com/trade-api/v2/` (2–3 s throttle; on 429, back off 60–90 s and log), `api.weather.gov` | No orders |

## 8. Do-not-modify

1. No live orders.
2. No invented PnL.
3. No Q6-`000` retune.
4. S2/R2-P4 stay gated.
5. No backfill or imputation of missing METAR, CLI or book data.
6. Do not mutate feebook, rails, C3 or Q labs.
7. Do not score against METAR proxies.
8. Do not change the knob levels or the headline after collection starts.

## 9. Empty results (on disk)

- `packets/card02_station_weather/FROZEN_EXPERIMENT.json`: results and pnl null
- `packets/card02_station_weather/results.json` and `results/EMPTY_RESULTS.json`: `NOT_RUN`

## 10. Done =

Freeze packet, stubs, source map, ledger and Collector handoff are on disk, then Conductor ACK. After that, in order: Collector 60-day archive, Variants implementation after ACCEPT, Examiner.

## Frozen-at

`2026-09-24T23:47:00Z` UTC (desk 2026-09-24 19:47 ET). Deep Research, under charter `6a02cb46…`.

## Changelog (post-freeze edits; none changes a frozen parameter)

- **2026-09-24T23:47:00Z: frozen at `9624ab2498e88896c46e8fd984211b4b8839e613567209841358d7cf5059e5d6`.**
  - An earlier draft, `31f2a06e…`, carried a mistaken Frozen-at timestamp. It was corrected to the actual write time before the stubs were written. That draft is superseded, and no copy survives.
  - No saved copy of `9624ab24` existed. It was **reconstructed byte-exact** at `packets/CARD02_STATION_WEATHER_NOWCAST_FREEZE_KERNEL_2026-09-24.md.reconstructed-9624ab24` by reversing the two v1.1 string edits. The sha256 matches the at-freeze hash recorded in `FROZEN_EXPERIMENT.json`.
- **2026-09-24 20:05:19 ET: `8412439f9a31211acbd66125275734afdf8e42e7a95ba7d9d5534003e587adfb`** (v1.1 bump). Two lines changed:
  - (1) line 9, the governing-charter line: v1 `6a02cb46…` became v1.1 `02272754…`, plus a note and the at-freeze hash;
  - (2) line 22: "Sources are listed in …SOURCE_MAP_2026-09-24.md" gained " (v1.1 format)".
  - **No station, knob level, headline, forecaster, exclusion, threshold, window, rejection rule or number changed.**
  - Saved copy: `…md.pre-20260925T001140Z` (sha256 `8412439f…`).
- **2026-09-24 ~20:12 ET: this version.** Added this Changelog section only.
