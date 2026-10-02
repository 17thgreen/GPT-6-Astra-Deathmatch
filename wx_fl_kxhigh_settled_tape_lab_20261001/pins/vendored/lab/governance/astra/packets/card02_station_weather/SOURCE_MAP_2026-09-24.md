# SOURCE MAP: Card 02 station weather (v1.1 format; 2026-09-24 ET)

**Charter:** `charters/DEEP_RESEARCH_MASTER_BRIEF_v1_1_2026-09-24.md`, sha256 `02272754b01da5b65edd837545e485f4fd4dff2903a7ae1f52d9cb5e616fec5d`. It supersedes v1 (`6a02cb46…`).

**What v1.1 changes:**
- Every promising entry records five fields: (1) mechanism or capability; (2) evidence and limits; (3) code, data and access; (4) the adaptation our Kalshi market needs; (5) the smallest useful experiment that shows value beyond a simpler baseline after costs.
- Each promising entry is tied to a decision: continue, narrow, redesign or shelve.

**This is a documentation-only update.** The frozen kernel is unchanged in every parameter: stations, knob {14, **10**, 6} h, the three forecasters, exclusions, pilot/evaluation split and rejections. Any experiment below that is not the kernel headline is a **proposal**. It needs its own packet ID and Conductor ACCEPT. Pilot-period (tuning) analyses are allowed by the kernel. Evaluation days 61–120 stay untouched.

**Tags:**
- **verified** = fetched or read on 2026-09-24.
- **unverified** = not confirmed.

**Status:** inspected · promising lead · inaccessible · superseded · irrelevant.

**Standard cost basis:**
- purchased-side executable ask at the snapshot;
- R1-P1 feebook @ `22371178cb2663250b4762f328069571c48cb551`;
- 2c buffer;
- R1-P5 rails @ `6a28e0d6254327ea4e6451c781bec56215ac6cac`;
- stress rows: one tick worse, fees 2×.
Net P&L stays null until the Archivist manifest lands.

---

## 1. Register (all entries)

| ID | Source | URL / path | Supports | Tag | Status | Promising? | Decision it could change |
|---|---|---|---|---|---|---|---|
| S1 | Charter v1.1 | `charters/DEEP_RESEARCH_MASTER_BRIEF_v1_1_2026-09-24.md` (sha256 `02272754…ec5d`) | Governs; supersedes v1 | verified | inspected | n/a | — |
| S2 | Research PDF Card 02 + p16 | `research/KALSHI_EDGE_RESEARCH_2026-09-24.pdf` | Mechanism and adaptation text; rejection rule; p16 | verified | inspected | **YES** (mechanism origin) | Continue/shelve (via kernel) |
| S3 | Conductor routing | `packets/CONDUCTOR_ROUTING_KALSHI_EDGE_RESEARCH_2026-09-24.md` | 3–4 stations; 60-day GET-only archive | verified | inspected | n/a | — |
| S4 | MAXIMIZE_PIN | `packets/MAXIMIZE_PIN_2026-09-23_1455ET.md` | Scorable-first bias | verified | inspected | n/a | — |
| S5 | Scorecard v1.2 | `templates/EXAMINER_KALSHI_SCORECARD_TEMPLATE_v1.2.md` | §J, §H, labels | verified | inspected | n/a | — |
| K1 | Kalshi series list (Climate and Weather, incl. `include_volume`) | `live_get_2026-09-24/series_list_*.json` | Universe; lifetime-volume tie-break | verified (raw) | inspected | no (plumbing) | — |
| K2 | Kalshi open markets ×19 series | `live_get_2026-09-24/markets_open/` | Liquidity rank; `rules_primary`; `close_time`; strikes | verified (raw, one snapshot) | inspected | no (plumbing) | Station choice (fragile CHI vs TSFO) |
| K3 | Kalshi orderbooks and trades (4 samples) | `orderbook_sample/`, `trades_sample/` | About 1c spreads; NY T74 NO bid 0.99 × 7,132.60 | verified (raw) | inspected | **YES** (evidence for the "already priced" disproof) | Narrow (drop T−6h if always ~certain) |
| K4 | GLOBALTEMPERATURE contract terms | https://assets.kalshi.com/contract_terms/GLOBALTEMPERATURE.pdf | NWS first; first non-preliminary report; inclusive "between"; full precision | verified (PDF) | inspected | **YES** (settlement mapping) | Continue vs shelve on the rounding thesis |
| K5 | Kalshi Help Center, weather markets (July 22, 2026) | https://help.kalshi.com/markets/popular-markets/weather-markets | Final NWS CLI; METAR-inconsistency delay; LST window | verified (page) | inspected | **YES** (part of the K4/N1–N3 mapping cluster) | same |
| N1 | NWSI 10-1004 | https://www.weather.gov/media/directives/010_pdfs/pd01010004curr.pdf | CLI timing; ASOS DSM; corrections; preliminary status; MM not estimated | verified | inspected | **YES** (mapping cluster) | same |
| N2 | NWS PSR HiRes ASOS | https://www.weather.gov/psr/HiResASOS | Rolling 5-min average in whole °F; 5-min METAR whole-°C conversion error | verified | inspected | **YES** (core rounding mechanism) | same |
| N3 | NWS LOX ASOS temperature page | https://www.weather.gov/lox/asostemperature | Max/min reported around 1 AM; LST; 1-min data not public | verified | inspected | **YES** (information clock) | Redesign (knob timing) |
| N4 | NWS LOT observations FAQ | https://www.weather.gov/lot/weather_observations_faq | Background | verified (read) | inspected | no (background) | — |
| N5 | api.weather.gov CLI lists and products | `https://api.weather.gov/products/types/CLI/locations/{NYC,LAX,MDW,MIA}` → `nws/` | Endpoints work; LAX Sep 23 issued twice; NYC min at 11:59 PM LST | verified (raw) | inspected | **YES** (settlement-risk capability) | Redesign (exclusions) |
| N6 | api.weather.gov station observations (METAR/ASOS) | `https://api.weather.gov/stations/<ICAO>/observations` | Running-max input at receipt time | verified (endpoint in use by T1; not fetched by Deep Research today) | inspected (via T1 code) | **YES** (nowcast input) | Continue/shelve |
| N7 | NWS point forecast (`/points` → `forecast`) | `https://api.weather.gov/points/<lat>,<lon>` | Simple-baseline input | unverified (not fetched today) | promising lead | **YES** (as the *baseline*, not an edge) | Shelve if the nowcast doesn't beat it |
| N8 | FMH-1 METAR 6-/24-hr max/min groups | not retrieved | Would sharpen the running max | **unverified** | promising lead (not retrieved) | lead | Redesign (feature) |
| T1 | weather-nowcast collector (another box agent) | `/workspace/lab/astra-capture/weather-nowcast/collector.py`, `stations.json` | GET-only receipt-time archive of Kalshi events/books/trades, NWS obs, CLI and CF6, with gap rows | verified (read-only code/config inspection) | inspected | **YES** (capability) | Continue (enables the kernel without a second egress stream) |
| T2 | GitHub `Ciarnan-Moloney/Kalshi-Weather-Spread-Algo` (C3 structure pointer) | https://github.com/Ciarnan-Moloney/Kalshi-Weather-Spread-Algo | Bordering-strike MM structure | unverified (not inspected by Deep Research) | promising lead for **C3**, not Card 02 | no (for Card 02) | — (belongs to the C3 bordering-strike harness) |
| T3 | C3 capture and harnesses (C3-RJ settled join; bordering strike) | `/workspace/lab/astra-capture/c3-kxhighny/`; `packets/C3_*_2026-09-2{2,3}.md` | NY/CHI books; settled join | verified | inspected | **YES** (reuse capability) | Continue (the settled join makes Card 02 scorable) |
| D1 | Dead card FEAT-20260913-002 / TEST-20260913-003 | `/workspace/lab/archive/features/FEAT-20260913-002.md`, `/workspace/lab/archive/tests/TEST-20260913-003-W2E-INCREMENTAL.md` | Observation-vs-strike nowcast vs mid on a non-oracle feed failed. No cemetery record. | verified | inspected | no (warning) | Shelve trigger if Card 02 repeats W2-E |
| D2 | Sibling weather FLB (no ID) | `packets/SIBLING_DEATHMATCH_REVIEW_2026-09-22.md` | Domain-adjacent dead card | verified | inspected | no (warning) | — |
| X1 | IBKR weather-contract article | (tertiary) | Background | unverified | irrelevant (tertiary; not relied on) | no | — |
| X2 | TWC value ≡ NWS CLI value | none | Market rules name TWC | **unverified** | open question | no | Redesign if they diverge |

**Emerging-technology gap:** no probabilistic temperature-nowcasting model or repo (ML or statistical) was searched or inspected today. This is a **gap**, not a finding. Per the charter, any such tool would have to beat the N7 baseline plus the conditional-nowcast baseline after costs.

**Shared ancestry:** K4, K5 and N1–N3 are one settlement-mapping cluster. They describe the same NWS process from different angles, so they count as **one** evidence line.

---

## 2. Promising entries: v1.1 five fields plus the decision link

### M1: the settlement-mapping cluster (K4, K5, N1, N2, N3): rounding and information clock

1. **Mechanism:**
   - The CLI max is the highest rolling 5-minute ASOS average, in whole °F, over midnight–midnight **LST**.
   - 5-minute METARs carry whole °C only, so converting back yields spurious °F (NWS PSR: 116 → 47 → 117).
   - Hourly METAR T-groups carry tenths °C.
   - Participants who read converted 5-minute values or apps can be off by about 1 °F, which is exactly one bucket.
2. **Evidence and limits:** authoritative NWS and Kalshi documents. They describe the process, but **no evidence yet that the market misprices it.** TWC-vs-CLI equivalence is unverified. The "first non-preliminary report" is ambiguous (N5).
3. **Code / data / access:** public documents. Raw inputs come via T1 (obs, CLI) at no cost.
4. **Adaptation:** map every observation into the CLI process before use:
   - use hourly T-groups; never convert a 5-min °C value into a running max;
   - use the LST window during DST;
   - use the inclusive integer buckets.
5. **Smallest useful experiment (proposed, pilot-period only):**
   - The "rounding-map check": for each pilot station-day, compute three things: (a) the naive running max (5-min °C → °F); (b) the mapped running max (hourly T-group → °F, rounded); (c) the eventual CLI max.
   - Measure how often (a) and (b) fall in different buckets, and on those days whether the market's purchased-side ask at T−6h sits on the *naive* bucket.
   - After-cost value: hypothetical taker on the mapped bucket at the ask, with the standard cost basis, vs **baseline = the naive-mapping forecaster** and vs **market-only**.
   - **Decision it could change:**
     - If divergence days are about 0, or the market already sits on the mapped bucket, the rounding thesis is dead: **narrow** Card 02 to remaining-day forecast skill (rejection (c) territory).
     - If divergence is frequent and mispriced, **continue** with rounding as the lead mechanism.

### K3: live books show many buckets already near certainty

1. **Capability / observation:** at 23:42Z on Sep 24, `KXHIGHNY-26SEP25-T74` had a NO bid of 0.99 for 7,132.60. Sampled buckets have about 1c spreads.
2. **Evidence and limits:** 4 samples, one snapshot, taken before the climate day. It says nothing about late-day pricing.
3. **Access:** public GET. T1 archives books every ~60 s.
4. **Adaptation:** separate "live" buckets (ask between 0.05 and 0.95) from near-certain ones at each knob level.
5. **Smallest useful experiment (pilot, read-only):**
   - For each knob level, record the share of buckets with ask in [0.05, 0.95] and the visible depth at those asks.
   - Baseline: no-trade.
   - The after-cost opportunity ceiling is (live buckets × depth × (1 − ask − fee − 2c)).
   - **Decision it could change:** if T−6h has about 0 live buckets with depth, **narrow** interpretation away from the late-day thesis. This is reported, not a knob change; all levels stay in the frozen grid. If T−10h/T−14h also have too little depth, **shelve** on capacity.

### N5: api.weather.gov CLI issuances (settlement-risk capability)

1. **Capability:** a receipt-time record of every CLI issuance, including duplicates and corrections (LAX Sep 23 was issued at 08:26Z and 08:40Z, identical values, no CCA).
2. **Evidence and limits:** one observed duplicate. It is unknown how often values change between issuances, and which issuance Kalshi uses.
3. **Access:** public API. T1 polls CLI and CF6.
4. **Adaptation:** join each station-day's issuance sequence to the Kalshi settled `result`. Flag `settlement_mismatch`.
5. **Smallest useful experiment (pilot, read-only):**
   - Count station-days with more than one issuance, with a value change, and with a Kalshi-result ≠ first-CLI bucket.
   - This is not a profit test. It bounds a settlement-risk cost that must be subtracted from any after-cost edge.
   - **Decision it could change:** if mismatches are non-trivial (for example ≥ 2% of station-days), **redesign** exclusions or the settlement-truth rule before evaluation starts. The kernel already reports mismatches separately.

### N6: station observations (nowcast input)

1. **Capability:** receipt-time METAR/ASOS observations (hourly T-group; 5-min obs) for KLAX, KMIA, KNYC and KMDW.
2. **Evidence and limits:** the feed can be stale or missing. Receipt lag relative to observation time is unmeasured. The observation feed ≠ oracle, which is the D1 dead-card lesson.
3. **Access:** public API, polled by T1 every ~5 min.
4. **Adaptation:** only observations with `received_at` ≤ issue time are used. More than 90 min without an observation excludes the day. Always score against the CLI, never against METAR.
5. **Smallest useful experiment:** the kernel's own headline. Conditional nowcast vs market ask-implied vs the simple error distribution, at T−10h, on untouched days 61–120, after the standard cost basis. **Proposed pilot add-on:** measure receipt lag (`received_at` − obs time) per station, to confirm the information set is realistic.
   - **Decision it could change:** continue vs **shelve** (rejections (a)–(e)).

### N7: NWS point forecast (the simpler baseline)

1. **Capability:** a free official forecast max, which is the natural "simple forecaster".
2. **Evidence and limits:** not fetched today. Its forecast-error distribution must be learned in the pilot.
3. **Access:** public API (`/points` → `forecast`). T1 does not currently poll it, so the Collector must add it or coordinate.
4. **Adaptation:** convert the forecast max into a bucket distribution using the pilot-fitted error distribution, then apply the CLI rounding map.
5. **Smallest useful experiment:** already a frozen kernel baseline. The nowcast must beat it *and* the market after costs.
   - **Decision it could change:** if the simple baseline matches the nowcast, the extra modeling is not worth its complexity: **shelve** the nowcast and possibly **redesign** as a simple-forecast-vs-market test.

### T1: weather-nowcast collector (tool built by another box agent)

1. **Capability** (from read-only inspection of `collector.py`):
   - GET-only, unauthenticated;
   - allowed-prefix and forbidden-path guards (no `/portfolio` or `/orders`);
   - streams: Kalshi events, event meta, batch orderbooks (~60 s), trades, NWS obs (~5 min), CLI/CF6 (~30/60 min);
   - raw bodies stored verbatim with `received_at_utc`;
   - 429s and stale polls become **gap rows** (no backfill);
   - SQLite archive; config versioning.
   - Its `stations.json` (config_version `2026-09-24.provisional-v0`, "PROVISIONAL - pending Deep Research final station list") **already lists KXHIGHLAX/KLAX, KXHIGHMIA/KMIA, KXHIGHNY/KNYC and KXHIGHCHI/KMDW**, matching the Card 02 kernel.
2. **Evidence and limits:** code inspection only. Run health, uptime and 429 budget are unknown. It is owned by another agent; Deep Research must not edit it.
3. **Access:** local box files. Ownership sits with that agent and the Collector.
4. **Adaptation for Card 02:**
   - add NWS point-forecast capture (N7);
   - add snapshots within ±2 min of 10:00, 14:00 and 18:00 LST (knob levels);
   - confirm one egress stream, shared with C3.
5. **Smallest useful experiment:** a 14-day pipeline-feasibility window at the start of the pilot. It measures:
   - the share of station-days passing the kernel's exclusion rules;
   - the 429 gap rate;
   - book-snapshot availability within ±5 min of each knob time.
   - Baseline: the kernel's FAIL-DATA threshold (> 30% excluded over 14 days). This is not a profit test; it gates whether any after-cost result is possible.
   - **Decision it could change:** **continue** (pilot proceeds on T1, with no duplicate collector) vs **redesign** (cadence or stations) vs **shelve** (data failure).

### T3: C3 capture and settled-join harness (reuse)

1. **Capability:** existing NY/CHI weather books plus a settled-resolution join harness (C3-RJ, knob join_gate).
2. **Evidence and limits:** covers NY/CHI only. The C3 kernels are distinct and must not be merged.
3. **Access:** local box.
4. **Adaptation:** reuse its books and join for NY/CHI, and extend the same join pattern to LAX/MIA via T1.
5. **Smallest useful experiment:** none separate. It is infrastructure that makes the kernel Examiner-scorable (MAXIMIZE_PIN bias).
   - **Decision it could change:** continue (scorability).

### S2: research PDF Card 02 (mechanism origin)

1. **Mechanism:** model the remaining-day maximum conditional on the observed max, time, cloud, wind shifts, humidity and forecast changes, mapped into the official rounding.
2. **Evidence and limits:** a research proposal, not an empirical result. "Sixty days is a collection target, not proof of power."
3. **Access:** local PDF.
4. **Adaptation:** 4 stations, KXHIGH only, knob = issue time.
5. **Smallest useful experiment:** the frozen kernel headline (T−10h paired log-loss vs market ask-implied and the simple baseline; after-cost taker with stress rows).
   - **Decision it could change:** continue vs shelve.

---

## 3. Trace: source → mechanism → adaptation → test

**Chain 1**
1. S2 (remaining-day nowcast) plus the M1 mapping cluster (rounding, LST) lead to the kernel's conditional nowcast.
2. That uses inputs from N6 and N7, archived by T1 and T3.
3. The headline T−10h test runs on untouched days.

**Pilot-only proposals:** M1 rounding-map check; K3 live-bucket census; N5 issuance/mismatch count; T1 14-day feasibility.

**Disagreement to record:** market rules name The Weather Company (K2), while the contract terms and Help Center name the NWS CLI (K4, K5). This is unresolved and has to be measured through N5 plus the settled join.
