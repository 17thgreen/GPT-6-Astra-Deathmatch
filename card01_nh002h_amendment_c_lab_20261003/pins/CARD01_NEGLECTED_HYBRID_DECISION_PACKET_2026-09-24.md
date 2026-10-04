# CARD 01: Neglected hybrid forecast: DECISION PACKET (2026-09-24 ET)

**Owner:** Deep Research (research, freeze and read-only diagnostics only). Variants implements after Conductor ACCEPT, Examiner scores (v1.2 + p16), Adversary checks overlap, and Archivist records.
**Charter (current): v1.1**, `charters/DEEP_RESEARCH_MASTER_BRIEF_v1_1_2026-09-24.md`, sha256 `02272754b01da5b65edd837545e485f4fd4dff2903a7ae1f52d9cb5e616fec5d` (required prefix 02272754 verified). It supersedes v1 `charters/DEEP_RESEARCH_MASTER_BRIEF_v1_2026-09-24.md` (sha256 `6a02cb468a4b6c600fc3a16078a216a6095321c6bc92c24b2a7aca58f149daa8`), under which this work was done. v1.1 adds, for every promising source, a smallest useful experiment vs a simpler baseline after costs plus the needed market adaptation (see the v1.1 source maps). The reference was bumped at 2026-09-24 ~20:05 ET as a documentation-only change; no frozen parameter, universe, weight, knob, pre-commit file or result was changed.
**Recovered run (preserved control):** `17thgreen/GPT-6-Astra-Deathmatch` → `neglected_hybrid_20260924/` @ **`2253c03cd86eb5515325f1d91b43bdcbea7a902c`**. This is not a fresh start. The files were fetched read-only (no clone) into `packets/card01_hybrid_forecast/recovered_2253c03c/` (RESULTS.md sha256 `8695ed1a…4aec`).
**Companion files:**
- Source map (v1.1 format): `packets/card01_hybrid_forecast/SOURCE_MAP_2026-09-24.md`
- Ledger: `packets/card01_hybrid_forecast/LEDGER_2026-09-24.md`
- Freeze (**filed**): `packets/CARD01_HOUSE_ONLY_PROSPECTIVE_FREEZE_2026-09-24.md`
**Amendment A (mapping correction, pre-outcome):** `packets/CARD01_HOUSE_ONLY_PROSPECTIVE_FREEZE_2026-09-24_AMENDMENT_A.md`
**Amendment B (pre-outcome; Adversary/Archivist/Conductor items a–e):** `packets/CARD01_HOUSE_ONLY_PROSPECTIVE_FREEZE_2026-09-24_AMENDMENT_B.md` (sha256 `ee6af37cef95f1e468d28e5b06750caaca8b1706ec11ed5cf5cdce460524c2c6`)
**Amendment C (pre-outcome, docs-only; pins Adversary AF-1/2/5/6/7/10/11; `AWAITING_CONDUCTOR_ACCEPT`):** `packets/CARD01_HOUSE_ONLY_PROSPECTIVE_FREEZE_2026-09-24_AMENDMENT_C.md` (sha256 `cc75f09614ad285756fd7cb7f7a5c2ce4e711b5adb98102c2dd043ccfc1af0f0`)
**SUPERSEDED_DRAFT:** no down-ballot freeze had been written before the course correction, so there was nothing to mark.

---

## 1. Assignment

- **Research question:** does an external specialist forecast add tradeable information to thin Kalshi legislative or down-ballot markets beyond the market price?
- **Intended decision:** continue, narrow, redesign or shelve the hybrid lane, and whether to freeze a House-only prospective confirmation.
- **Market and horizon:** Kalshi House, Senate and down-ballot contracts, held to settlement.

## 2. Economic thesis

- **What is mispriced:** district-level House race contracts (`KXHOUSERACE`). They are thin next to the chamber-control market:
  - In-universe race contracts: median `volume_24h_fp` **3.04** and median top-of-book YES ask size 85.00 (page 0, 23:48:58Z).
  - `CONTROLH-2026-R`: `volume_24h_fp` **841,209.14**, OI 15,087,531.98 (23:50:19Z).
  - The hypothesis is that race prices are set largely by the national environment plus partisan priors. They then under-weight district-specific information (candidate quality, fundraising, district polls, redistricting) that a specialist model aggregates.
- **Why it could persist:** attention is scarce. A trader cannot earn much by researching one district when capacity is tens of contracts. That is also exactly why the edge would be small.
- **Who trades with us:** partisan and retail participants expressing views, plus a few passive quotes. Informed district specialists are rarely present at these sizes.
- **What disproves it** (any one of these):
  - (a) Prospectively, the blend does not beat the mid in paired Brier.
  - (b) The gain is only a uniform national shift. That would be one correlated event, not race-level information.
  - (c) The gain exists only at midpoints and disappears at executable asks.
  - (d) The 2026 markets, open since January 2026 (2024 House contracts opened Oct 31, 2024), are mature enough that disagreement has closed.

## 3. Recovered state (quotes from RESULTS.md @ 2253c03c)

- Primary policy (RESULTS.md): "50% published specialist forecast + 50% market bid/ask midpoint".
  - At most one contract per race, held to settlement.
  - Entry requires probability minus cost to exceed a 3c reserve after "an illustrative unrounded `0.07*p*(1-p)` taker fee and 2c execution buffer".
  - Source: archived 538 `states_latest.json`, captured 2024-11-03 20:38:57Z, with a 24 h lag imposed.
  - RESULTS.md says: "a **prespecified retrospective analysis**, not a blind historical holdout."

| Family and decision (UTC) | Races | Market Brier | Hybrid Brier | Relative loss reduction | Signals | Hypothetical net | Modeled outlay |
|---|---:|---:|---:|---:|---:|---:|---:|
| House, Nov 4 2024 22:00 (amended primary) | 19 | 0.24176 | 0.21186 | 12.4% | 2 | +$0.885560 | $1.114440 |
| House, Nov 5 2024 16:00 (sensitivity) | 23 | 0.23091 | 0.20867 | 9.6% | 3 | +$1.519439 | $1.480561 |
| Senate, Nov 4 2024 22:00 (replication) | 12 | 0.08856 | 0.08904 | −0.5% | 0 | $0 | $0 |
| Senate, Nov 5 2024 16:00 (sensitivity) | 13 | 0.07524 | 0.07852 | −4.4% | 1 | −$0.385925 | $0.385925 |

**Why these cohorts cannot be combined:**
- RESULTS.md: "**The horizons overlap within one election. Do not add their profits or race counts or treat the House observations as independent replications.**"
- The 19-race primary spans 12 states and "fails the frozen minimum of 20 races". The 23-race sensitivity "does not repair that primary admission shortfall."

**House trades:**
- Primary trades: IA-1 D NO @ $0.46 (+$0.502612) and PA-10 D NO @ $0.58 (+$0.382948).
- Expected margins were about 3.9–4.0c. RESULTS.md: "These positions all backed Republicans and share national political risk."
- Removing the two best winners leaves primary net **$0**.
- The positions settled Jan 3, 2025, about 60 days after the decision.

**Model-only and 25% arms:**
- Model-only House: 0.18804 Brier, 6 signals, +$2.577394 (primary).
- RESULTS.md: "That is a research clue, not permission to choose its weight". This is **exploration only.**
- Senate model-only lost $0.454342 (primary).
- 25% arm: 0.22605 Brier, 0 signals.

**Statistical checks:**
- State bootstrap 95% CI for hybrid − market: primary [−0.05334, −0.00405], sensitivity [−0.04745, −0.00084].
- RESULTS.md says these are "conditional on one election, omit national common-factor risk".
- Leave-one-state-out keeps the sign in every case.

**Data gaps:**
- No historical depth.
- "All six requests succeeded but returned empty arrays" (minute bars).
- Fees unverified.
- Target mismatch (election winner vs party of the member sworn in).
- No current feed admitted.
- 707 open contracts ≠ 707 races.
- Code checks per RESULTS.md: "27 tests; exact reproduction of three result files; eight frozen source hashes; 29 independent decimal ledger checks." Deep Research did **not** re-run these.

## 4. Can the data answer the question?

| Question | 2024 (recovered) | 2026 (checked today) |
|---|---|---|
| Resolution definition | Party of member sworn in for the 2025 term (RESULTS.md) | **Verified by raw GET:** "If the House member sworn in for AL-02 for the term beginning in 2027 is a member of the Democratic Party, then the market resolves to Yes." HOUSEPARTY terms: first certificate-holder sworn in. Party switch resolves on election-day party. Vacancy resolves on the replacement's party. Accelerated determination on ≥4/8 media calls. `CONTROLH`/`CONTROLS` (CONTROL terms) resolve on the chamber leader's party on Feb 1, so they are **party control, not race win**. |
| Forecast at receipt time | Wayback archive time used as a bound | ElectIndex daily CSV (435 House rows). Our Collector receipt time governs. Source-admission gates are open (ToS, independence). |
| Quotes | Hourly closes, no depth | Live orderbook GET works (recovered smoke plus today's page 0) |
| Execution / fills | **Cannot answer** (minute bars empty) | Depth snapshots only. Fills stay hypothetical. |
| Fees | Unverified illustrative formula | R1-P1 pin. The Archivist manifest is pending, so net stays null. |
| Independence / sample size | One election; 19 races | One election; 92 races in the universe. Still one national draw. |

**Conclusion:** the data can answer forecast quality prospectively on about 50–92 races within one election. It cannot establish execution, repeatability, or scalable capacity this cycle.

## 5. Status-ladder rung (each rung judged separately; no rung implies the next)

| Rung | Status |
|---|---|
| Code verified | **Yes for the retrospective harness**, per RESULTS.md checks at 2253c03c (not re-run by Deep Research) |
| Retrospective predictive evidence | **House: yes**, conditional on one election (19 races, 12 states; the CI excludes 0 but breadth fails). **Senate: no.** |
| Hypothetical after-cost result | **Marginal:** 2 House trades, +$0.886, under an unverified fee and no depth. It is $0 without the two winners. |
| Prospective paper evidence | **No.** NH-002-H is frozen to produce it. |
| Observed live execution | No (forbidden) |
| Scalable repeatability | No |

## 6. Separate judgments

- **Forecast quality:** moderately encouraging for the House, negative for the Senate.
  - New read-only diagnostic (run after the freeze): recentering each forecaster by its own mean logit error, which removes a uniform national miss, **leaves the House gain in place**. Primary D goes from −0.0299 to −0.0276, state-bootstrap CI [−0.0483, −0.0040]. Sensitivity goes to −0.0202, CI [−0.0396, −0.0014].
  - The 2024 market was more Democratic-leaning than outcomes (logit shift +0.33 market vs +0.24 hybrid). Most, but not all, of the gain is cross-race rather than a pure level shift.
  - Senate stays null after recentering.
  - Caveat: recentering does not remove heterogeneous exposure to the national factor.
  - File: `card01_hybrid_forecast/EXPLORE_DIAG_national_factor_recentered_2253c03c.txt`.
  - My bootstrap CI for the raw primary D ([−0.0545, −0.0042]) differs slightly from RESULTS.md because of seed and method. **RESULTS.md numbers remain canonical.**
- **After-cost profit:** not established. There are 2 trades. Expected margin was about 4c/contract, which is inside plausible fee-plus-slippage error. There is no depth, and the fee is unverified.
- **Execution:** unknown. Historical execution cannot be recovered (empty minute bars). 2026 depth is visible but thin:
  - page 0 in-universe contracts: median top-of-book YES ask size 85, median spread 2.05c;
  - all pages (58 races, 117 contracts): median top-of-book YES ask size 200, median spread 2.8c;
  - the 34 legacy-series races are unmeasured.
- **Capacity:** small.
  - The freeze estimates about 9 signals × about 85 contracts × about $0.5, which is about **$380 of top-of-book capital for the whole cycle**, and about **$30 ex-ante EV** at a 4c margin.
  - With the all-pages median of 200 contracts, this becomes about $900 of capital and about $70 EV.
  - The order of magnitude is unchanged.
  - Capital-hours per $0.50 contract range from about 25–150 $-h (accelerated determination) to about 750 $-h (settlement after the Jan 2027 swearing-in).
  - This is an order-of-magnitude estimate from raw public quantities, not a result.
- **Repeatability:** unestablished and structurally slow. There is one House cycle every two years. The 2024 source (538) no longer exists (shut down March 2025), so every cycle is a new-source test.

## 7. Strongest critique

1. **One election is one draw.** Every 2024 House position backed Republicans. In a year where the market leaned too Democratic, any R-leaning external model "wins." Recentering helps but does not rule out heterogeneous national exposure. The Senate, where the same source was available and the markets were more liquid, **did not reproduce** at all. The sign pattern "helps where markets are thin" is also what one would see from noise in the thin cohort plus a national miss.
2. **The 2024 House markets were days old.** They opened Oct 31, 2024 for an early-November test. The "neglect" may have been initial price discovery, not persistent inattention. 2026 contracts have been open since January 2026 (earliest page-0 `open_time` 2026-01-07), so the 2024 effect size should be expected to shrink.
3. **The economics are tiny even if the forecast signal is real.** $0.886 on 2 trades, about $30 ex-ante EV per cycle at top-of-book, and 60-day capital lock. Even a clean PASS would promote a **forecast-quality** finding, not a cash lane.
4. **The source changes each cycle.** ElectIndex has no track record. Its market-independence is unverified, and it may ingest market signals. Its ToS is "all rights reserved". A pass or fail speaks about ElectIndex-2026, not "specialist forecasts."
5. **The nearest dead card already failed the same form.** F1 (FEAT-20260912-001/-002, TEST-20260912-002) was a λ = 0.35 model/market blend. It was REDUNDANT/FAIL-INSUFFICIENT against the Kalshi mid (e.g., BTC T−5m ΔBrier +0.003343, N = 569). A different domain, but a reminder that blends over a mid usually add nothing once the market is liquid.

## 8. Recommendation: **NARROW**

- **Keep:** a House-only, prospective, forecast-quality stream (NH-002-H, filed), treated as the "slower research stream" the research PDF prescribes.
- **Shelve:** the Senate hybrid (negative replication, preserved) and governor/down-ballot extensions for this cycle. No new families, sources or weights.
- **Do not claim:** a trading lane. After-cost, execution, capacity and repeatability stay unestablished. Per MAXIMIZE_PIN, this card is Examiner-scorable only after the 2026 settlements.

## 9. Next three experiments (ranked)

1. **NH-002-H House-only prospective confirmation.**
   - **Filed:** `packets/CARD01_HOUSE_ONLY_PROSPECTIVE_FREEZE_2026-09-24.md`.
   - Design: 92 untouched races, w = 0.5 fixed, decision 2026-11-02T22:00Z, state-cluster paired bootstrap plus national-factor recentering, R1-P1/R1-P5 pins.
   - Cost: GET-only capture.
   - Deadline: capture must start now, since it needs daily ElectIndex receipts from at least 2026-10-25.
   - **Gate:** Archivist ToS/licence decision on ElectIndex. If refused, the freeze is void (no substitution).
2. **Disagreement-and-depth census (read-only, unscored, needs no outcomes).**
   - Weekly from now to Nov 2: |p_ElectIndex − p_mid| and visible depth for the 92 races, by liquidity tier. Then hourly books from Nov 2 22:00Z to Nov 4, to see how fast any disagreement disappears.
   - Tests mechanism prediction (d): does disagreement exist in 2026, is it larger in thinner markets, and does it persist long enough to be executable? This is the only execution-rung evidence obtainable this cycle.
   - Would need its own short measurement freeze with a separate ID and one knob (liquidity-tier cut). Not filed today.
3. **Source-dependence shadow.**
   - Log a second free source (RacetotheWH, if a bulk file can be admitted) alongside ElectIndex at identical receipt times. Score it **after** NH-002-H as a separate, explicitly exploratory comparison.
   - Addresses critique 4 (is the result about the source or the idea?). Must never replace the NH-002-H headline.

**Done today (exploration, read-only):** the 2024 national-factor recentering diagnostic (§6). It was run after the freeze, so it could not influence the freeze.

## 10. Nearest dead card

**FEAT-20260912-001 / FEAT-20260912-002 (F1, INACTIVE), test TEST-20260912-002.**
- Files: `/workspace/lab/archive/tests/TEST-20260912-002-F1-INCREMENTAL.md`, `/workspace/lab/archive/features/FEAT-20260912-002.md`.
- It was a linear model/market blend p = (1−λ)m + λ·p_struct with λ = 0.35, scored against the Kalshi mid incumbent `MKT-KALSHI-15M-MID` (TEST-20260911-007).
- Verdict: REDUNDANT / FAIL-INSUFFICIENT on ΔBrier and ΔLogLoss.
- **No cemetery record exists for it.** The only CEM-ASTRA ID, CEM-ASTRA-20260922-001 (Q7 Arm B), is orthogonal. Archive CEM-20260910-001..003 and CEM-20260911-001..005 are Binance microstructure, also orthogonal.

## 11. Gaps and honesty notes

- Kalshi 429s on the shared egress IP (all logged in `card01_hybrid_forecast/live_get_2026-09-24/http_log.jsonl`; 18 total 429 responses):
  - `CONTROLH` (step3; probe aborted during backoff);
  - `KXHOUSERACE` ×2 and `CONTROLH` ×2, plus `CONTROLS` (step4; aborted);
  - `KXHOUSERACE` page 1 ×2 and `CONTROLS` ×2 (step5);
  - `KXHOUSERACE` pages 1 and 2 once each, both OK on retry (step6);
  - `CONTROLS` ×2 (step6);
  - `HOUSEPA10` ×2 and `HOUSEME2` ×2 (step7).
  - After backoff, `KXHOUSERACE` pages 0–3 were all captured (707 contracts / 351 races; receipt 23:48:58Z–23:57:08Z, so not one atomic snapshot).
  - **`CONTROLS` was never captured.** Legacy-series 2026 contracts were **not verified**. No gaps were filled.
- **Mapping finding (after the freeze):** only 58 of the 92 frozen races have a `KXHOUSERACE` `-D` contract. The other 34, including PA-07/08/10, AZ-01/06, CO-08, ME-02 and NE-02, sit in per-district legacy HOUSEPARTY series. This is fixed by Amendment A (mapping only, pre-outcome). The Collector must verify it by GET before 2026-10-26.
- **All-pages liquidity** (58 in-universe `KXHOUSERACE` races, 117 contracts): median `volume_24h_fp` 3.04, sum 47,809.50, median OI 4,777.11, median spread 2.8c, median top YES ask size 200.00. Out-of-universe (590 contracts): median `volume_24h_fp` 0.00, median spread 4.9c. Liquidity for the 34 legacy-series races is unmeasured.
- Market-independence of ElectIndex: **UNVERIFIED.** ToS/licence: **legal gap.**
- 2026 fee for `KXHOUSERACE`: from the R1-P1 pin only. The Archivist manifest is pending.
- The `KXHOUSE`/`KXSENATE` series metadata points at ROCKET.pdf / faa.gov. This is a metadata anomaly and was not relied on.
- Deep Research did not re-run the 2253c03c `verify.py`.

## Changelog

The file's hash lineage is **`58c44c4f…` → `d59c2642…` → (this version; full sha256 in LEDGER / FROZEN_EXPERIMENT)**. The earlier ACK text and the Conductor ruling had the direction reversed.

Versions before `58c44c4f` (drafting between 19:5x and ~20:03 ET) were not hash-recorded.

- **2026-09-24 ~20:03 ET: `58c44c4fb144968ba57e4c8b4a2018026a123d17a02e2e6c09fdfd38f465a353`.**
  - Last pre-v1.1 version: Amendment A pointer, full 429 list, all-pages liquidity.
  - It was cited in the ACK at the time.
  - No saved copy existed. It was **reconstructed byte-exact** at `packets/CARD01_NEGLECTED_HYBRID_DECISION_PACKET_2026-09-24.md.reconstructed-58c44c4f` by reversing the two v1.1 string edits. The sha256 matches.
- **2026-09-24 20:05:19 ET: `d59c26420713ef728a306efc0bb12761584125e96ba6a87e84fe0c3e57c69688`** (v1.1 bump). Two lines changed:
  - (1) line 4, the charter line: v1 `6a02cb46…` became v1.1 `02272754…`, plus a documentation-only note;
  - (2) line 7, `- Source map:` became `- Source map (v1.1 format):`.
  - **No number, rule, threshold, universe, weight, knob, recommendation or result changed.**
  - Saved copy: `…md.pre-20260925T001140Z` (sha256 `d59c2642…`).
- **2026-09-24 ~20:12–20:17 ET: this version** (full sha256 recorded in `packets/card01_hybrid_forecast/LEDGER_2026-09-24.md` hash register and in `FROZEN_EXPERIMENT.json`). Two changes:
  - (1) Added the Amendment B pointer line under the Amendment A line (with Amendment B sha256 `ee6af37cef95…`).
  - (2) Added this Changelog section (including the corrected lineage).
  - Intermediate bytes `cbc0cb8a…` existed briefly after the changelog was first written and before the Amendment B hash was added to the pointer line; they are superseded by this hash.
  - **No number, rule, threshold, universe, weight, knob, recommendation or result changed.**
- **2026-10-03 17:12 ET (21:12Z): next version** (pre-edit bytes `c0c1aa66f104e3f102228a7a8e16f205977afbee63928f30a6954ec46707a82c` saved byte-exact at `packets/_prev/c0c1aa66f104e3f102228a7a8e16f205977afbee63928f30a6954ec46707a82c.CARD01_NEGLECTED_HYBRID_DECISION_PACKET_2026-09-24.md` under RULE-FROZEN-EDIT-PREV-BYTES-001; new sha256 is recorded outside this file, since a file cannot contain its own hash). Two changes:
  - (1) Added the Amendment C pointer line under the Amendment B line (with Amendment C sha256 `cc75f096…f0f0`, status `AWAITING_CONDUCTOR_ACCEPT`).
  - (2) Added this changelog entry. (A transient intermediate `ebdaea01…`, with a wrong timestamp in this entry, existed for under a minute; its bytes are kept at `packets/_prev/ebdaea01…` and it is superseded.)
  - **No number, rule, threshold, universe, weight, knob, recommendation or result changed** in this file. The rule pins themselves live only in Amendment C.
