# Scout external hunt — fee-honest Kalshi / sports-microstructure kernels vs Q6-000 (box-IP Kalshi CLOSED)
**Seat:** Market Scout "KALSHI" (executor) · Astra/Kalshi desk (Logan M)
**Written:** 2026-10-03 16:05 ET (America/New_York, UTC−4)
**Commission:** `packets/CONDUCTOR_KICK_SCOUT_EXTERNAL_HUNT_WHILE_BOX_IP_CLOSED_2026-10-03.json` sha256 `9c583e82aec1c5d622f222875c19c1edc5f4c11de4908fe32f503494aa7f60c9`
**Governing ruling:** `packets/CONDUCTOR_RULING_WEATHER_BOX_IP_CLOSED_AFTER_R2E_429_2026-10-03.json` sha256 `dd1d70396472a72fce2bad5233ba0190f5df4c14568d9b7746bf282ef892b2dc` (BOX_IP_KALSHI_CLOSED; maximize-while-blocked = this hunt)
**Freeze:** `packets/scout_external_hunt_2026-10-03/FREEZE_EXTERNAL_HUNT_2026-10-03.md` · sha256 `15e2d2e409cdb187bdc36e618c6d5369510963841f83b17056eb46891e27dad5` · frozen **2026-10-03 15:59:53 EDT** (19:59:53Z), before any external pull (stamp: `FREEZE_STAMP.txt`)
**Prev-bytes:** header time corrected 16:15→16:05 ET; pre-edit bytes at `_prev/bfb1b7f3…SCOUT_EXTERNAL_HUNT_2026-10-03.md` (RULE-FROZEN-EDIT-PREV-BYTES-001)
**Raw:** `packets/scout_external_hunt_2026-10-03/raw/` + `MANIFEST.sha256` (url, http, fetch UTC + ET, bytes, sha256) + `WEBSEARCH_AND_FAILED_FETCH_NOTES_2026-10-03.md`
**Mode:** kernels + triage only. **Zero Kalshi calls from the box** (no api.elections / external-api / trading-api / demo; no kalshi.com domain fetched at all). No orders. No P&L, fills, backtests or inventory invented. Nothing frozen, nothing scored. Fee facts come from the on-box **CACHE**.
**Tags:** [V] verified on box / in a saved source · [I] inferred · [H] hypothesis · [A] assumption · [U] unknown

---

## 0. What Q6-000 is (read from box, [V])
- NFL `KXNFLGAME` moneyline **maker pairing allocator**, SHADOW only. Net **+$345.24 / 6.90%** on $5k over 31 W1+W2 dev games, with early queue 3,300 and delay 0.25 s; maker 0.0175, taker 0.07 modeled (`reports/RPT-Q6-000.md`; `astra-science/nfl_factorial_lab_20260921/SHADOW_CANDIDATE_FREEZE.json`). Zero fresh holdout games.
- Primary ledger `results/q3300_d0.25_000.json`: 12,853 fills. Maker 324,967.78 contracts, taker 2,068.66. `passive_pairing_fraction` 0.987, `unhedged_contract_hours` 603,262.7, `all_flat` true, max event exposure $250 [V].
- **New observation [V]:** of the 000 maker contracts, **321,622 (≈99.0%) are NO-side** and 3,345 are YES-side (`q3300_d0.25_000_fills.jsonl.gz`, summed `size` by `kind`,`outcome`). The replay fills a resting NO when a trade prints with `taker_side=yes` (`replay_v2.py:218`, `queue_policies.py:37`). So **000 in effect sells to YES-takers on both teams and locks the pair.** This fact drives K2 and K3.

## 1. Box-data inventory (what is scorable now; read-only, verified this session)
| # | Dataset (exact path) | Verified content | Range (UTC → ET) | Status for this hunt |
|---|---|---|---|---|
| B1 | `lab/astra-science/nfl_factorial_lab_20260921/inputs/events.jsonl.gz` (+`markets.json`, `manifest.json`) | 681,732 trades + 364,988 one-minute quotes · 62 tickers / 31 games · taker_side yes 636,251 trades (43.39M contracts) vs no 45,481 (3.93M) · quoted spread median 1¢, 94.2% of quote rows ≤1¢ | 2026-09-03T00:20Z → 2026-09-20T21:26Z (09-02 20:20 ET → 09-20 17:26 ET). **Every ticker's last row is K−174 min**, so the tape is pregame and ends before the inactives window | **Scorable** (Q6 dev cohort, already reused) |
| B2 | `.../nfl_factorial_lab_20260921/results/q3300_d0.25_000_*.jsonl.gz` (+ q10000 / d5 arms) | 000 fills / orders / decisions ledgers (see §0) | same 31 games | **Scorable** (stress joins) |
| B3 | `lab/astra-capture/prospective/capture.sqlite` (ADMIT-1) | 220,951 KXNFLGAME trades, 32 tickers; 218,554 depth-10 book responses; 218,807 trade responses; 19 runs, 18 gaps | trades 2026-09-24T21:51Z → 2026-10-02T03:28Z (09-24 17:51 ET → 10-01 23:28 ET) | **Holdout-class: metadata only, peek-banned.** I looked at counts and time bounds only, never prices or outcomes |
| B4 | `lab/astra-capture/weather-nowcast/archive.sqlite` | 80,460 trades (KXHIGHCHI 11,358 / LAX 26,338 / MIA 22,144 / NY 20,620); 51,468 book snapshots; 2,502 market rows; NWS obs 2,666 | 2026-09-25T00:07Z → 09-27T13:27Z (09-24 20:07 ET → 09-27 09:27 ET) | Occupied (cash-cow weather). Not re-proposed |
| B5 | `lab/astra-capture/q6s5-kxmlbspread/` (`trades_fills_2026-09-25/raw` 44 files 4.7M; `measured/raw` 145; `settlement_only_2026-10-02/raw` 6) | KXMLBSPREAD tapes | Sep-25 universe CONSUMED (STATUS_2026-10-02) | Variants-owned / parked |
| B6 | `lab/data/DATA-PROV-PM-001/003/004/006/008/009` | Kalshi 15m resolved: 1,328 (PM-001), 1,208 candle sets (PM-003), 369 (PM-004). Poly BTC/ETH books: PM-006 `raw/book` 20 day-files, still running (status kept_rows 236,821). Kalshi 15m mid: PM-008 14 day-files. PM-009: 718 Poly book files | PM-006 2026-09-13 → 10-03; PM-008 09-14 → 09-27 | Occupied (KXBTC15M cash-cow / W2-B axis) |
| B7 | `lab/astra-capture/{c2-kxnhlgame,atp-kxatpmatch,s4-kxncaafgame,c1-kxufcfight,r2-p3-prop-slate,s5-...}/settled_reget_*.json` | Settlement snapshots only (≤120 KB each, no tapes) | Sep 22–24 | Too thin to score any kernel |
| B8 | `packets/scout_house_fee_2026-09-24/raw/docs/kalshi_fee_schedule.txt` + `docs_fee_rounding.txt` (**CACHE**, fetched 2026-09-24 21:38 ET) | Taker `round up(M×0.07×C×P×(1−P))`, M default 1 · Maker `round up(M×0.0175×C×P×(1−P))`, M default 0 unless listed · Non-standard table "effective July 7, 2026": **KXNFLGAME maker 1 / taker 1**, KXMLBGAME 1/1, KXATPMATCH 1/1, KXNCAAFGAME 1/1 · rounding doc: direct members to $0.0001, non-direct to $0.01 | — | Fee source for every kernel |
| B9 | **NEW** `packets/scout_external_hunt_2026-10-03/raw/nflverse_nfldata_games.csv` (sha `683673b5…`) | 7,548 games · 2026: 272 rows, W1–W4 64 with moneyline, 49 scored · **2025 REG: 272 with moneyline** · 31/31 dev events join (29 exact; JAC↔JAX alias for CLEJAC and JACDEN) | season 1999 → 2026-W4 | **Scorable** external consensus (free, public) |

## 2. Kernel table (≤5)
| ID | Name | Thesis one-liner | Data on box? (path) | Fee / cost path | Key tags | Rec |
|---|---|---|---|---|---|---|
| **EXT-K1** | Consensus-anchored legging-risk audit of 000 | 000's unpaired first legs (603k contract-hours) may sit on the side the sportsbook consensus disfavors, so part of its edge could be hidden directional risk; a consensus-deviation refusal gate could beat it | **Y**: B1 + B2 + B9 (nflverse ML, fetched today) | Maker 0.0175×p(1−p), M=1 (cache) per leg ≈0.4375¢/contract at p=.5; pair ≈0.875¢; spread 1¢ median; queue 3,300 assumption inherited | Join [V]; line timestamp **[U]**; edge [H] | **TRY** (measurement; Adversary/Examiner lane) |
| **EXT-K2** | Optimism-tax dependence stress | 000 is ≈99% NO-maker against YES-taker flow (91.7% of dev contracts). Becker and Bartlett–O'Hara say this YES overbetting is the maker's surplus, so if the flow mix shifts, 000 fails. Stress across flow-mix regimes, and season-scale on the 2025 archive | **Partial**: dev regime split on B1+B2 now; season-scale needs **Becker archive** (free, 36.0 GB, not Kalshi) | Same as 000; YES/NO mix changes fill rate and markout, not fee | Flow split [V]; literature [V]/[I]; dependence [H] | **TRY** (box part) · archive pull **HOLD** (approval + disk) |
| **EXT-K3** | Scheduled injury-report window toxicity | NFL Practice and Game-Status reports drop at 4:00 pm ET Wed/Thu/Fri. Informed takers pick off resting NO quotes right after, so a ±15–30 min stand-down could beat 000 net | **Y**: B1+B2 (8 Wed–Fri 15:30–16:30 ET windows, 22,392 trades, 7,943 quote rows); inactives T−90 **not on tape** | Avoided adverse fills vs lost spread capture: maker fee unchanged; cost is foregone pairs | Windows [V]; rule [V] (saved NFL ops pages); toxicity [H] | **TRY** (measurement; Variants owns any gate) |
| **EXT-K4** | Decided-but-unsettled sweep (post-final, pre-settlement) | After the final whistle, winner contracts still print below $1 until settlement. Impatient sellers pay a capital-recycling premium to whoever absorbs at 0.97–0.99 | **N**: B1 is pregame-only [V]; B3 in-game is holdout-banned; needs fresh tape (Kalshi egress) or Becker archive + nflverse pbp (free) | Taker at p=0.97: 0.07×0.97×0.03=0.204¢/ct; **C=1 order rounds to $0.01 (≈5×)** at cent rounding; maker 0.051¢/ct | Close/expiry gap [V cache]; premium [H]; reversal risk [A] | **DEFER** |
| **EXT-K5** | Cross-venue Polymarket↔Kalshi sports divergence | Same-game price gaps across venues offer arb or lead-lag | Crypto analogs on box (B6) belong to W2-B; no sports Poly data on box | Kalshi taker 1.75¢ at p=.5 + Poly sports taker (0.03 vs 0.05: **[U]** conflict) | pm-efficiency negative [V]; overlap with W2-B / collapsed Bridge seat | **SKIP** |

Scorable on box data **today**: **EXT-K1, EXT-K3, and the dev-regime half of EXT-K2.** K4 and the season-scale half of K2 need external data. K5 is skipped.

---

## 3. Per-kernel triage

### EXT-K1 — Consensus-anchored legging-risk audit of 000
- **Economic thesis.** The NFL sportsbook moneyline consensus is the sharpest public fair value [I]. 000 earns pair spread, but 0.987 passive pairing still leaves 603,262.7 unhedged contract-hours [V]. If first legs fill mostly when Kalshi drifts away from consensus (informed takers pushing toward it), the unpaired inventory is adversely selected and the pair-completion cost is understated. **Who pays:** in the stress case, 000 pays informed takers. In the beat case, a variant that refuses first legs when Kalshi mid is on the wrong side of the de-vigged consensus by >x¢ avoids those payments [H].
- **Measurement (for Examiner/Variants, not run here):** per game, de-vig the nflverse home/away ML (proportional and Shin) to get `p_cons`. Join to the B1 minute mids and to B2 fills (`outcome_mid_at_fill`, `resting_seconds`, `inventory_after`). Slice unpaired-leg contract-hours by sign(`mid − p_cons`), and settlement outcome by side, using the nflverse scores [V] for 32/32 W1–W2 games.
- **Data:** ON BOX. B1, B2, B9 (31/31 joinable with the JAC↔JAX alias [V]).
- **Fee/cost:** no new fee channel. Maker 0.0175×C×p(1−p) with M=1 for KXNFLGAME (cache B8): ≈0.4375¢/contract at p=.5 and ≈0.875¢ per locked pair. The pair must be bought at ≤$0.99 to clear fee plus rounding [I arithmetic]. Spread is 1¢ median (94.2% of quotes) [V], so a gate costs foregone pairs, not fees.
- **Evidence:** fills and ledger fields [V]; consensus lines present [V]; **line snapshot time is undocumented in nflverse DATASETS.md [U]**, so it may be the close or an earlier snapshot. Treat it as an ex-post anchor only. Consensus being sharper than Kalshi NFL ML [A]. Sign of the effect [H].
- **Overlap:** R1-P3 (sportsbook de-vig, ACCEPT measurement/Adversary only, needed a paid real-time odds feed). K1 is the **free ex-post half** of that lane, scorable now. Not a 000 retune: no parameter of 000 changes, it is an audit plus a candidate refusal arm.
- **Rec: TRY** (Adversary/Examiner measurement first; Variants decides any gate arm).

### EXT-K2 — Optimism-tax dependence stress (000 = NO-maker vs YES-taker flow)
- **Economic thesis.** Becker (72.1M Kalshi trades, Jun-2021→2025-11-25) finds Sports taker −1.11% / maker +1.12% (gap 2.23 pp, 43.6M trades). Takers favor affirmative YES, and makers buying NO beat makers buying YES (+1.25 vs +0.77 pp) [V saved page]. Bartlett–O'Hara (41.6M trades) find traders overbet YES, and that behavioral surplus cross-subsidizes adverse selection. One-sided (VPIN-style) flow predicts maker losses in single-name markets [V saved abstract]. On the dev tape, **91.7% of contracts are taker-YES** [V], and 000 is ≈99% NO-maker [V]. **Who pays:** YES-optimist takers. **Stress:** 000's +6.90% may simply be this surplus at one point in time. Becker shows the gap only turned maker-positive after late-2024 growth (time-varying) [V]. If flow composition shifts (Yurchyna "composition shift", SSRN 7364100, abstract fetch 403 [U]), 000 decays. No retune proposed.
- **Measurement:** (a) box now: split the 31 games or by hour into taker-YES-share terciles from B1, and attribute 000 fills and contract-hours per tercile from B2. (b) season-scale: 2025 KXNFLGAME trades from the Becker archive (schema: `taker_side`, `yes_price`, `count`, `created_time`, plus market `result`) [V schema doc]. Compute maker-NO vs maker-YES excess return by price band and week. This is a trade-only prior because the archive has **no quotes** [V schema], so it cannot replay 000 directly.
- **Data:** box part ON BOX (B1, B2). Archive: `https://s3.jbecker.dev/data.tar.zst`, HEAD 200, **36,020,641,508 bytes**, Last-Modified 2026-02-05 [V HEAD saved]. Free, public, third-party (Cloudflare R2), **not a Kalshi endpoint**. Box free disk is **21 GB** [V df], so the archive does not fit. A streamed, filtered extract (`curl | zstd -d | tar` keeping only `data/kalshi/*` NFL rows) is possible [I] but untested.
- **Fee/cost:** same maker path as 000 (cache B8). Becker returns are **gross of fees** [V], so Examiner must apply 0.0175×p(1−p) to maker and 0.07×p(1−p) to taker before comparing.
- **Evidence:** flow split [V]; literature [V]; Sports Kalshi games being "broad-based" vs "single-name" in Bartlett–O'Hara's taxonomy [U]; dependence of 000 on the surplus [H]; Kalshi `taker_side` semantics stable across the API's newer `taker_outcome_side`/`taker_book_side` fields [U] (B3 sample shows both present).
- **Overlap:** R3-P3 / FL-band is about price-band calibration; K2 is about **side-framing and flow mix at equal cost basis**, applied as a stress on 000. FL-band H1 KILL (CEM-ASTRA-20261001-001) is not reopened.
- **Rec: TRY** box part · **HOLD** archive pull pending Conductor/Logan approval (size and disk; third-party mirror of Kalshi data, see §5).

### EXT-K3 — Scheduled injury-report window toxicity
- **Economic thesis.** NFL clubs file Practice Reports (Wed/Thu) and Game Status Reports (Fri) by **4:00 pm New York time**, and the inactive list 90 min before kickoff [V saved NFL ops pages]. Scheduled news means takers with the news hit resting quotes before makers can cancel. 000's resting NO bids on both teams are exposed when one team's probability jumps. **Who pays:** 000 pays news-takers. A stand-down or widen gate around these clocks could beat 000 net if avoided adverse fills exceed foregone pair spread [H].
- **Measurement:** compare B2 fill markouts (mid at +5/+30 min from B1) and pair-completion latency inside vs outside Wed–Fri 15:30–16:30 ET. B1 has **8 such windows (2026-09-03/04/09/10/11/16/17/18), 22,392 trades, 7,943 quote rows** [V]. **Inactives T−90 cannot be measured on B1** because the tape ends at K−174 min for all 62 tickers [V]. That half needs a new capture (Kalshi egress) and must not come from the B3 holdout.
- **Fee/cost:** the gate changes no fee. Cost = foregone maker pairs (≈1¢ spread, maker fee ≈0.875¢/pair) [I]. If a variant crosses to flatten during news, it pays taker 0.07×p(1−p) ≈1.75¢/ct at p=.5 [V arithmetic, cache formula].
- **Evidence:** windows and rows [V]; report deadlines [V]; actual release timestamps vary ("or as soon as possible after practice") [V source text], so the window is approximate [A]; toxicity [H].
- **Overlap:** Q4 timing lab tested entry window and exit deadline vs kickoff, not news clocks [V README]. 000's F factor (two-sided positive-flow admission gate) is a flow gate, not a clock gate, so partial overlap only. Not a 000 retune; any gate arm is Variants' freeze.
- **Rec: TRY** (measurement on box; T−90 half DEFER to egress).

### EXT-K4 — Decided-but-unsettled sweep
- **Economic thesis.** KXNFLGAME markets stay listed past the game. The cached listing shows `KXNFLGAME-26SEP24ATLGB-ATL` with `expected_expiration_ts` 2026-09-25T06:15Z (02:15 ET) and `close_ts` 2026-09-27T00:15Z (09-26 20:15 ET) [V cache: `scout_house_fee_2026-09-24/raw/docs/nonstandard_fee_series.json`]. Between the final whistle and settlement, holders of near-certain winners who want cash now may sell at 0.95–0.99. **Who pays:** impatient sellers / capital recyclers [H]. Risk: result reversal or rule disputes for game winners is tiny [A], but capital is locked until settlement [V mechanism].
- **Data:** **not scorable on box.** B1 is pregame only [V]; B3 has in-game data but is ADMIT-1 holdout (peek ban). Needs either (a) Kalshi egress for a fresh post-game tape, or (b) the Becker archive (trades with timestamps, plus `close_time`/`result`) plus nflverse play-by-play (`time_of_day`, free on GitHub releases) for game-end time. Both are free but blocked by the 36 GB / 21 GB disk constraint.
- **Fee/cost:** taker at p=0.97 is 0.07×0.97×0.03 = **$0.002037/ct**. For C=100 that is **$0.21** (cent round-up). For **C=1 it rounds to $0.01, ≈5× the formula** (cent rounding for non-direct members; direct members round to $0.0001 per cached rounding doc [V]). Maker at p=0.97: 0.0175×0.0291 = $0.000509/ct. Gross edge 1–3¢/ct [H] minus fee minus capital-days.
- **Overlap:** conceptually adjacent to CEM-ASTRA-20260924-001 (Card 09 crypto settlement window), but a different domain and mechanism. Flag for Adversary.
- **Rec: DEFER** (until egress or approved archive extract).

### EXT-K5 — Cross-venue Polymarket↔Kalshi sports divergence
- **Thesis:** cross-venue gaps or lead-lag on the same games.
- **Evidence against:** `alexanderallen7/pm-efficiency` (8,285 matched outcomes / 700 MLB-NHL-NBA games over 40 days in 2026). Median gap 0.5¢ (mean 1.13¢), lag-0 correlation 0.86 with no ≥1-min lead, Brier tie 0.2438 vs 0.2440, arbitrage mostly erased at ≥0.5¢/side cost [V saved README; their numbers, not ours]. `kv1514/arb-engine` says "moneylines are efficient to within fees" and the residual arbs are in far-tail totals/spreads vs Robinhood/Rothera, a different venue [V saved README].
- **Fee:** Kalshi taker 1.75¢/ct at p=.5 (cache) plus Polymarket sports taker. **0.03 (pm-efficiency) vs 0.05 (sportstrades) conflict [U]**; Polymarket makers are free per both.
- **Overlap:** W2-B cross-venue axis; the Bridge seat collapsed. Crypto Poly/Kalshi data on box (B6) is W2-B / KXBTC15M-occupied and not re-proposed.
- **Rec: SKIP.**

---

## 4. Considered, not slotted
| Idea | Why not |
|---|---|
| Favorite-longshot band maker (Bürgi–Deng–Whelan) | Occupied: R3-P3 / FL-band H1 KILL (CEM-…20261001-001) / WX-FL ITERATE |
| VPIN one-sided-flow refusal gate (Bartlett–O'Hara) | Close to 000's F factor (already factorial-tested, 000 = F off). Folded into K2/K3 as a stress dimension |
| Liquidity Incentive Program quoting (`ghipszer20/Kalshi-LIP-Collector`) | card03 occupied (CEM-…-004 subsidy-only; card03 parked). LIP repo is non-sports and pre-result |
| RFQ combo copula pricing (`pranay123-stack/kalshi-rfq-combo-pricing-engine`) | RFQ Card 07 occupied |
| Pinnacle-anchored ATP (tennis-data odds) | Q6S1 KXATPMATCH kept for bakeoff; no ATP tape on box (B7 settlement JSON only) |
| AI/LLM bots and dashboards (CloddsBot, kalshi-ai-trading-bot, OctagonAI, etc.) | No measurable kernel (same disposition as R3) |

## 5. Blockers
1. **Box-IP Kalshi CLOSED** (ruling dd1d7039). K4 and the inactives half of K3 need a fresh post-game / T−90 tape. This waits on Logan's (b) read-only production key or (c) alternate host, then a fresh Conductor ruling.
2. **Becker archive (K2 season-scale, K4 alt path):** 36.0 GB compressed vs **21 GB free** on the box [V]. Third-party mirror of Kalshi data, not a Kalshi endpoint. Not downloaded. Needs a Conductor/Logan decision on (i) whether a third-party Kalshi-data mirror is acceptable under the ruling (it is not an IP rotation, but it is Kalshi-derived data), and (ii) disk (streamed filtered extract vs more disk).
3. **Possible non-box-IP data paths (FYI only, not touched):** PMXT archive (free, CC BY 4.0). Search snippet says its Kalshi folder was last updated **2026-05-14** [I], so it does **not** cover Sep-2026 windows; direct fetch timed out. Predexon Kalshi tick book since Jan-2026 is **paid** ($50 trial credits) [I]. predictiondata.dev Kalshi book stream is a vendor with unknown price [U]. Any vendor use is Logan's call.
4. **nflverse line timing [U]:** K1 is an ex-post anchor only. A real-time gate still needs a live odds feed (R1-P3 paid-API issue).
5. **ADMIT-1 holdout (B3)** is off-limits for scouting. All K1–K3 work must stay on the 31-game dev cohort (B1/B2), which has been used repeatedly, so results there are development-grade, not OOS.
6. Fee-rounding ambiguity: the kick says "rounded up to the cent per order"; the cached rounding doc says direct members are aligned to $0.0001 and non-direct to $0.01 [V cache]. Examiner should pin the account class.

## 6. Sources (saved under `packets/scout_external_hunt_2026-10-03/raw/`; sha in `MANIFEST.sha256`)
- Jon-Becker/prediction-market-analysis README + docs/SCHEMAS.md (raw.githubusercontent, 200); dataset HEAD `s3.jbecker.dev/data.tar.zst` (200, 36,020,641,508 B, Last-Modified 2026-02-05)
- Becker (2026), *The Microstructure of Wealth Transfer in Prediction Markets*, jbecker.dev (200; SSRN 7217640)
- Bartlett & O'Hara (2026), *Adverse Selection in Prediction Markets: Evidence from Kalshi*, Stanford Law page (200) + ingame.com summary (200); SSRN 6615739 (timeout)
- alexanderallen7/pm-efficiency README (200); kv1514/arb-engine README (200); VV1Git/sportstrades README (200); ghipszer20/Kalshi-LIP-Collector README (200)
- nflverse/nfldata `data/games.csv` (200, 2,182,453 B) + `DATASETS.md` (200)
- NFL Football Operations: 90-minute officiating meeting page (200); NFL Ops Manual 2022-23 p.104 injury-report deadlines (fliphtml5, 200)
- Failed/snippet-only: archive.pmxt.dev (timeout/504), karlwhelan.com Kalshi.pdf (timeout), SSRN 7364100 (403), predexon / predictiondata (search snippets). See notes file.
- On-box cache cited: `packets/scout_house_fee_2026-09-24/raw/docs/{kalshi_fee_schedule.txt, docs_fee_rounding.txt, nonstandard_fee_series.json}`; prior briefs `briefs/R1_DEEP_RESEARCH_2026-09-22.md` (R1-P3), `briefs/R3_DEEP_RESEARCH_EXTERNAL_CANDIDATES_2026-09-22.md`, `research/KALSHI_EDGE_RESEARCH_2026-09-24.txt`.

*End Scout external hunt 2026-10-03 · freeze-first · no box Kalshi GET · no orders · no invented P&L*
