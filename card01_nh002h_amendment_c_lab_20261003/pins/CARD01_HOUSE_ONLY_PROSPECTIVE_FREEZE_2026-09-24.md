# CARD 01: House-only prospective confirmation (NH-002-H): FREEZE, 2026-09-24 (ET)

**Packet ID:** CARD01-NH002-HOUSE-PROSPECTIVE
**Series:** `KXHOUSERACE` (2026 House race contracts; Democratic contract `-D` per race)
**Owner (freeze):** Deep Research
**Implementer (only after Conductor ACCEPT):** Variants (scoring code), Collector (GET-only capture). Examiner scores with scorecard v1.2 + the p16 checklist. Adversary checks overlap. Archivist records the fee/account manifest and source admission.
**Reviewer:** Conductor
**Status:** **FROZEN**, not run. `results` = **null**, `pnl` = **null**. Study label (v1.2 §I): `prospective shadow`.
**Governing charter:** `charters/DEEP_RESEARCH_MASTER_BRIEF_v1_2026-09-24.md`, sha256 `6a02cb468a4b6c600fc3a16078a216a6095321c6bc92c24b2a7aca58f149daa8`.
**Recovered predecessor (preserved control, not altered or re-scored):** `17thgreen/GPT-6-Astra-Deathmatch` `neglected_hybrid_20260924/` @ `2253c03cd86eb5515325f1d91b43bdcbea7a902c` (NH-001/NH-001A). This freeze implements its NEXT_EXPERIMENT (NH-002), restricted to the House.
**Decision packet:** `packets/CARD01_NEGLECTED_HYBRID_DECISION_PACKET_2026-09-24.md`. **Source map:** `packets/card01_hybrid_forecast/SOURCE_MAP_2026-09-24.md`. **Ledger:** `packets/card01_hybrid_forecast/LEDGER_2026-09-24.md`.
**Hard rules:**
- No live orders. No paid data. No expert contact.
- No Q6-`000` retune. S2/R2-P4 stay gated.
- Exactly one knob. Results and pnl stay null.
- Never fill gaps. GET-only.

---

## 1. Intent (one kernel)

On untouched 2026 House races, test whether a fixed 50/50 blend of an admitted external specialist forecast (ElectIndex) and the Kalshi mid has lower paired Brier loss than the market mid alone. Hypothetical one-contract hold-to-settlement trades are also scored, under frozen fees and fills.

**Primary purpose:** forecast-quality confirmation. The after-cost, execution and capacity outputs are reported but are **not** the headline, because capacity is small by construction (decision packet §6).

## 2. Admission gate for the forecast source (must pass before capture counts)

- **Source:** ElectIndex `output/races_summary.csv`, field `dem_prob` (percent, divided by 100), from https://github.com/ElectIndex/26_us_forecast_data. The freeze-time snapshot is sha256 `eb65e9aa71616843fb48832ca5bf4391f99ea76dcd8e087cae72a1f871fcdaf0`, received 2026-09-24.
- **Why this source:**
  - It is public and free.
  - It covers all 435 House rows as machine-readable district probabilities, with daily snapshots.
  - It is the only candidate found today with that coverage and without a paywall (Split Ticket is partly paywalled; Silver Bulletin FLIPR is likely paywalled).
  - The 2024 source (538) was shut down in March 2025.
- **Open gates (Conductor/Archivist):**
  - (a) ToS says "all rights reserved" and the repo has no license. Internal research use needs Archivist sign-off.
  - (b) Market-independence is **UNVERIFIED**. The README does not mention market inputs, but absence is not proof.
  - (c) There is no published track record.
- **If (a) is refused, this freeze is VOID.** No other source may be substituted under this packet ID, because substitution would be a second variant.
- **Consequence:** because the source differs from 2024, this is a **new-source test of the same hypothesis, not a replication of NH-001.**

## 3. Universe (frozen before any 2026 price was viewed)

- **Rule** (pre-committed at `2026-09-24T23:48:37Z` in `card01_hybrid_forecast/PRECOMMIT_UNIVERSE_WEIGHT_2026-09-24.json`, sha256 `2968f389…e77e`): 2026 House races with ElectIndex `dem_prob` in [10, 90] inclusive at the freeze snapshot. That gives 93 races.
- **Forecast-side mapping exclusion:** AK-01 is excluded because it has no Democratic candidate and its `dem_prob` equals an independent's probability, so it does not map to the Kalshi Democratic contract.
- **Frozen universe: 92 races, 28 states.** Recorded in `card01_hybrid_forecast/UNIVERSE_2026_HOUSE_FROZEN.json` (sha256 `d8af7451…8ca6`).
- The universe was selected using the forecast only. Market prices and outcomes were not used. The first 2026 `KXHOUSERACE` price page was received at 23:48:58Z, after the pre-commit.

### Overlap proof versus the 2024 19-race and 23-race sets

- **Event overlap: none.** The 2024 sets are `2024-HOUSE-*` races (term beginning 2025; contracts `HOUSE<ST><N>-24-D`). The 2026 races are a different election, resolving on the member sworn in for the term beginning 2027 (`KXHOUSERACE-<ST><NN>-26-D`). No 2026 outcome exists yet, so none has been seen.
- The union of the 2024 sets is 24 district labels (`RECOVERED_RACE_SETS_2253c03c.json`).
- **District-label coincidence:** 13 of the 92 share a label with a 2024 district: AZ-01, AZ-06, CA-22, CO-08, IA-03, ME-02, MI-07, NC-01, NE-02, PA-07, PA-08, PA-10, WA-03. These are different events, and some districts were redrawn.
- **Preregistered sensitivity:** the headline is re-reported on the **79 races with no label overlap.** It is reported, not selected.

### Frozen universe (92 races)

| # | 2026 race (ElectIndex code) | Kalshi event (expected) | State | ElectIndex dem_prob at freeze snapshot (%) | Same district label as a 2024 set? |
|---|---|---|---|---:|---|
| 1 | AL-02 | `KXHOUSERACE-AL02-26` | AL | 45.8 | no |
| 2 | AR-02 | `KXHOUSERACE-AR02-26` | AR | 30.2 | no |
| 3 | AZ-01 | `KXHOUSERACE-AZ01-26` | AZ | 77.4 | YES (label only; different election/term) |
| 4 | AZ-02 | `KXHOUSERACE-AZ02-26` | AZ | 60.0 | no |
| 5 | AZ-05 | `KXHOUSERACE-AZ05-26` | AZ | 12.3 | no |
| 6 | AZ-06 | `KXHOUSERACE-AZ06-26` | AZ | 76.6 | YES (label only; different election/term) |
| 7 | AZ-08 | `KXHOUSERACE-AZ08-26` | AZ | 19.9 | no |
| 8 | CA-22 | `KXHOUSERACE-CA22-26` | CA | 80.7 | YES (label only; different election/term) |
| 9 | CA-48 | `KXHOUSERACE-CA48-26` | CA | 88.5 | no |
| 10 | CO-03 | `KXHOUSERACE-CO03-26` | CO | 53.9 | no |
| 11 | CO-04 | `KXHOUSERACE-CO04-26` | CO | 37.3 | no |
| 12 | CO-05 | `KXHOUSERACE-CO05-26` | CO | 29.2 | no |
| 13 | CO-08 | `KXHOUSERACE-CO08-26` | CO | 79.4 | YES (label only; different election/term) |
| 14 | FL-02 | `KXHOUSERACE-FL02-26` | FL | 20.7 | no |
| 15 | FL-04 | `KXHOUSERACE-FL04-26` | FL | 23.6 | no |
| 16 | FL-07 | `KXHOUSERACE-FL07-26` | FL | 55.3 | no |
| 17 | FL-08 | `KXHOUSERACE-FL08-26` | FL | 20.4 | no |
| 18 | FL-09 | `KXHOUSERACE-FL09-26` | FL | 57.5 | no |
| 19 | FL-11 | `KXHOUSERACE-FL11-26` | FL | 27.6 | no |
| 20 | FL-12 | `KXHOUSERACE-FL12-26` | FL | 13.7 | no |
| 21 | FL-13 | `KXHOUSERACE-FL13-26` | FL | 35.1 | no |
| 22 | FL-14 | `KXHOUSERACE-FL14-26` | FL | 81.4 | no |
| 23 | FL-16 | `KXHOUSERACE-FL16-26` | FL | 39.2 | no |
| 24 | FL-18 | `KXHOUSERACE-FL18-26` | FL | 16.3 | no |
| 25 | FL-22 | `KXHOUSERACE-FL22-26` | FL | 62.3 | no |
| 26 | FL-25 | `KXHOUSERACE-FL25-26` | FL | 83.4 | no |
| 27 | FL-26 | `KXHOUSERACE-FL26-26` | FL | 18.0 | no |
| 28 | FL-27 | `KXHOUSERACE-FL27-26` | FL | 34.1 | no |
| 29 | GA-01 | `KXHOUSERACE-GA01-26` | GA | 21.0 | no |
| 30 | GA-11 | `KXHOUSERACE-GA11-26` | GA | 11.6 | no |
| 31 | GA-12 | `KXHOUSERACE-GA12-26` | GA | 12.9 | no |
| 32 | IA-02 | `KXHOUSERACE-IA02-26` | IA | 68.4 | no |
| 33 | IA-03 | `KXHOUSERACE-IA03-26` | IA | 78.0 | YES (label only; different election/term) |
| 34 | KY-06 | `KXHOUSERACE-KY06-26` | KY | 28.9 | no |
| 35 | ME-02 | `KXHOUSERACE-ME02-26` | ME | 34.9 | YES (label only; different election/term) |
| 36 | MI-01 | `KXHOUSERACE-MI01-26` | MI | 12.4 | no |
| 37 | MI-04 | `KXHOUSERACE-MI04-26` | MI | 47.5 | no |
| 38 | MI-07 | `KXHOUSERACE-MI07-26` | MI | 65.0 | YES (label only; different election/term) |
| 39 | MI-10 | `KXHOUSERACE-MI10-26` | MI | 66.1 | no |
| 40 | MN-01 | `KXHOUSERACE-MN01-26` | MN | 29.2 | no |
| 41 | MN-08 | `KXHOUSERACE-MN08-26` | MN | 17.2 | no |
| 42 | MO-02 | `KXHOUSERACE-MO02-26` | MO | 23.7 | no |
| 43 | MT-01 | `KXHOUSERACE-MT01-26` | MT | 34.9 | no |
| 44 | NC-01 | `KXHOUSERACE-NC01-26` | NC | 71.6 | YES (label only; different election/term) |
| 45 | NC-03 | `KXHOUSERACE-NC03-26` | NC | 28.1 | no |
| 46 | NC-05 | `KXHOUSERACE-NC05-26` | NC | 18.4 | no |
| 47 | NC-06 | `KXHOUSERACE-NC06-26` | NC | 12.0 | no |
| 48 | NC-07 | `KXHOUSERACE-NC07-26` | NC | 18.4 | no |
| 49 | NC-09 | `KXHOUSERACE-NC09-26` | NC | 18.2 | no |
| 50 | NC-11 | `KXHOUSERACE-NC11-26` | NC | 42.5 | no |
| 51 | NC-13 | `KXHOUSERACE-NC13-26` | NC | 12.5 | no |
| 52 | NC-14 | `KXHOUSERACE-NC14-26` | NC | 12.2 | no |
| 53 | NE-01 | `KXHOUSERACE-NE01-26` | NE | 19.6 | no |
| 54 | NE-02 | `KXHOUSERACE-NE02-26` | NE | 87.3 | YES (label only; different election/term) |
| 55 | NH-01 | `KXHOUSERACE-NH01-26` | NH | 77.1 | no |
| 56 | NJ-02 | `KXHOUSERACE-NJ02-26` | NJ | 22.4 | no |
| 57 | NJ-07 | `KXHOUSERACE-NJ07-26` | NJ | 76.4 | no |
| 58 | NV-02 | `KXHOUSERACE-NV02-26` | NV | 41.6 | no |
| 59 | NY-01 | `KXHOUSERACE-NY01-26` | NY | 39.9 | no |
| 60 | NY-02 | `KXHOUSERACE-NY02-26` | NY | 15.8 | no |
| 61 | NY-17 | `KXHOUSERACE-NY17-26` | NY | 71.0 | no |
| 62 | NY-21 | `KXHOUSERACE-NY21-26` | NY | 14.3 | no |
| 63 | OH-07 | `KXHOUSERACE-OH07-26` | OH | 48.1 | no |
| 64 | OH-08 | `KXHOUSERACE-OH08-26` | OH | 23.4 | no |
| 65 | OH-09 | `KXHOUSERACE-OH09-26` | OH | 88.5 | no |
| 66 | OH-10 | `KXHOUSERACE-OH10-26` | OH | 22.5 | no |
| 67 | OH-15 | `KXHOUSERACE-OH15-26` | OH | 38.7 | no |
| 68 | PA-01 | `KXHOUSERACE-PA01-26` | PA | 46.5 | no |
| 69 | PA-07 | `KXHOUSERACE-PA07-26` | PA | 71.4 | YES (label only; different election/term) |
| 70 | PA-08 | `KXHOUSERACE-PA08-26` | PA | 61.4 | YES (label only; different election/term) |
| 71 | PA-10 | `KXHOUSERACE-PA10-26` | PA | 86.1 | YES (label only; different election/term) |
| 72 | SC-01 | `KXHOUSERACE-SC01-26` | SC | 41.7 | no |
| 73 | SC-02 | `KXHOUSERACE-SC02-26` | SC | 15.6 | no |
| 74 | TN-05 | `KXHOUSERACE-TN05-26` | TN | 14.9 | no |
| 75 | TN-09 | `KXHOUSERACE-TN09-26` | TN | 20.5 | no |
| 76 | TX-02 | `KXHOUSERACE-TX02-26` | TX | 12.7 | no |
| 77 | TX-09 | `KXHOUSERACE-TX09-26` | TX | 29.2 | no |
| 78 | TX-10 | `KXHOUSERACE-TX10-26` | TX | 11.1 | no |
| 79 | TX-15 | `KXHOUSERACE-TX15-26` | TX | 57.4 | no |
| 80 | TX-21 | `KXHOUSERACE-TX21-26` | TX | 12.8 | no |
| 81 | TX-22 | `KXHOUSERACE-TX22-26` | TX | 11.2 | no |
| 82 | TX-23 | `KXHOUSERACE-TX23-26` | TX | 45.4 | no |
| 83 | TX-24 | `KXHOUSERACE-TX24-26` | TX | 11.9 | no |
| 84 | TX-32 | `KXHOUSERACE-TX32-26` | TX | 23.6 | no |
| 85 | TX-34 | `KXHOUSERACE-TX34-26` | TX | 88.4 | no |
| 86 | TX-35 | `KXHOUSERACE-TX35-26` | TX | 62.3 | no |
| 87 | VA-01 | `KXHOUSERACE-VA01-26` | VA | 37.9 | no |
| 88 | VA-02 | `KXHOUSERACE-VA02-26` | VA | 74.5 | no |
| 89 | VA-05 | `KXHOUSERACE-VA05-26` | VA | 33.1 | no |
| 90 | WA-03 | `KXHOUSERACE-WA03-26` | WA | 82.2 | YES (label only; different election/term) |
| 91 | WI-01 | `KXHOUSERACE-WI01-26` | WI | 37.4 | no |
| 92 | WI-03 | `KXHOUSERACE-WI03-26` | WI | 75.5 | no |
## 4. Knob (exactly one): blend weight `w` on the external forecast

p_hybrid = w · p_ElectIndex + (1 − w) · p_mid, where p_mid is the Kalshi `-D` contract YES bid/ask midpoint at the decision snapshot.

| Level | Role |
|---|---|
| **w = 0.5** | **Headline (primary). Chosen before seeing any 2026 race.** |
| w = 0.25 | Comparator (reported) |
| w = 1.0 | Comparator (model-only, reported) |
| w = 0 | Market-only **control** (the baseline, not a knob level) |

A no-trade control is always $0.

**Weight justification (exploration only, no 2026 data):**
- (1) 0.5 was the weight declared for NH-001 before 2024 scoring. It is a preserved control and must not be retuned.
- (2) In Sethi et al. 2021 (arXiv 2102.04936), "A simple average of the two forecasts performs better than either one of them overall."
- (3) In the 2024 exploration, model-only did better on the House (Brier 0.18804 vs hybrid 0.21186) but worse on the Senate (model-only lost $0.454342 at primary). Choosing w = 1 would therefore be post hoc selection on one election, which RESULTS.md explicitly forbids ("a research clue, not permission to choose its weight after seeing this election").
- (4) w = 0.25 generated 0 primary House signals in 2024.

No other weight will be considered.

## 5. Decision time, information set, fees, fills, sizing

- **Decision time:** `2026-11-02T22:00:00Z`, the eve of the Nov 3, 2026 election. This mirrors the NH-001A primary.
- **Receipt-time information set:**
  - Forecast: the latest ElectIndex `races_summary.csv` received by **our** Collector at or before `2026-11-01T22:00:00Z` (the NH-002 24-hour lag) and no older than 7 days (received ≥ `2026-10-25T22:00:00Z`).
  - ElectIndex `output/historical/` folders and git commit times are recorded but **never** used to backdate. Our receipt time governs.
  - Book: a `GET /markets/<ticker>/orderbook` snapshot for each universe race's `-D` contract, taken between 21:45Z and 22:15Z on Nov 2. The snapshot nearest 22:00Z is used. Snapshots older than 15 minutes are excluded, and the exclusion is logged.
- **Exclusions at decision time** (logged, never imputed):
  - no `-D` contract;
  - no two-sided book (crossed, one-sided, or bid 0 / ask 1);
  - no admissible forecast;
  - forecast `dem_name` "(No Democrat)" or a same-party race at decision time;
  - market closed or settled early.
- **Fee regime:** R1-P1 feebook @ `22371178cb2663250b4762f328069571c48cb551`. The fee is taken from the pinned feebook for `KXHOUSERACE`. The illustrative `0.07·p·(1−p)` from NH-001 is recorded as a sensitivity only. Net P&L stays null until the Archivist fee/account manifest lands (v1.2).
- **Rails:** R1-P5 @ `6a28e0d6254327ea4e6451c781bec56215ac6cac` (freshness labels).
- **Order timing and fill model:**
  - Hypothetical taker at the snapshot: buy D YES at the YES ask, or D NO at (1 − YES bid).
  - Fill only if visible quantity at that price is ≥ 1.
  - Stress rows (v1.2 §G): one tick worse; fees 2×.
- **Sizing:** at most one contract per race, on the side where (p_hybrid of that side − price − fee − 2c buffer) > 3c reserve. This is the NH-001 gate, unchanged. Feasible size = min(1, visible depth).
- **Holding:** hold to Kalshi settlement.
  - Resolution text (verified by raw GET 2026-09-24, `KXHOUSERACE-AL02-26-D`): "If the House member sworn in for AL-02 for the term beginning in 2027 is a member of the Democratic Party, then the market resolves to Yes."
  - Contract terms HOUSEPARTY allow accelerated determination once ≥4 of 8 Designated Media Sources call the race.
  - The forecast targets the election winner, so the basis mismatch (death, vacancy, party switch) is retained, as in NH-001.

## 6. Evaluation metrics and tests

**Primary:** mean paired Brier difference D = Brier(hybrid w=0.5) − Brier(market mid) over admitted races, using Kalshi settled results.

**Paired test:**
- State-cluster bootstrap, 10,000 resamples of states with replacement, seed 20261102. Report the 95% percentile CI.
- **PASS-FORECAST** requires both:
  - (i) the CI upper bound < 0; and
  - (ii) the national-factor diagnostic below does not remove the gain.
- Leave-one-state-out range is reported.

**National common-factor diagnostic** (parameter-free, preregistered):
1. Recenter each forecaster by subtracting its own across-race mean logit error. This removes a uniform national miss.
2. Recompute D and its CI.
3. If the recentered CI includes 0, the verdict is "common-factor only". That triggers the research-PDF clause "concentrated in one correlated event", and race-level information is not claimed.

**Secondary (v1.2 common scorecard):**
- log loss;
- 10-bin calibration;
- signals, fill rate, feasible vs requested size;
- adverse selection: mid move 24 h after the decision snapshot, from a second Collector snapshot at `2026-11-03T22:00:00Z`;
- capital-hours, drawdown, event concentration (top-1 and HHI; flag if > 50%);
- executable USD/day (median and p10);
- net P&L with and without rewards (null until manifest);
- stress rows;
- sensitivity on the 79 no-label-overlap races;
- the w = 0.25 and w = 1.0 comparators.

**Uncertainty is reported by state cluster, and the report must state that it is conditional on one election.**

## 7. Power / uncertainty plan (not a race-count minimum)

**Inputs** (exploration only, from the recorded 2024 per-race rows @ 2253c03c; read-only diagnostic `card01_hybrid_forecast/EXPLORE_DIAG_paired_brier_SE_2253c03c.txt`):
- per-race SD of the paired Brier difference (hybrid_50 − market): 0.04498 (19 races) and 0.04629 (23 races);
- state-cluster inflation of the SE: 0.01275 / 0.01032 = 1.235.

**Expected SE:** SE(D) ≈ 0.045 × 1.235 / √n.

| Admitted n | Expected SE | Minimum detectable \|D\| (two-sided α = 0.05, 80% power ≈ 2.8·SE) | Relative to a 0.24 market Brier |
|---:|---:|---:|---:|
| 92 | 0.0058 | 0.0162 | 6.8% |
| 70 | 0.0066 | 0.0186 | 7.7% |
| 50 | 0.0079 | 0.0220 | 9.2% |
| 30 | 0.0102 | 0.0284 | 11.8% |

- The 2024 point estimate was D = −0.0299. That estimate was likely inflated by selection and by market immaturity: the 2024 contracts opened Oct 31, 2024, while the 2026 contracts have been open since Jan 2026.
- At n = 92, power is about 0.74 for |D| = 0.015 and about 0.41 for |D| = 0.010.
- At n = 50, power is about 0.48 for |D| = 0.015.

**Caveats (binding):**
- (1) The state bootstrap does **not** capture the national common factor. One election is one draw of that factor ("one election cycle is not hundreds of independent experiments", research PDF Card 01). A PASS is therefore at most **prospective paper evidence for this cycle**, not repeatability.
- (2) The 2024 SD came from a different source (538) and a less mature market, so the realized SE may differ. The Examiner reports the realized SE.
- (3) Hypothetical P&L has almost no power: about 9 signals are expected (2024 rate 2/19), so it is reported descriptively.

## 8. Capital-hours and capacity (from raw public data only)

- **Raw snapshot** (`live_get_2026-09-24/markets_open/markets_open_KXHOUSERACE_p0.json`, received 2026-09-24T23:48:58Z; 200 of about 707 open contracts; later pages hit 429s and were not filled):
  - The 23 page-0 contracts in the frozen universe had median `volume_24h_fp` **3.04**, sum 7,440.58, median `open_interest_fp` 5,163.09, median spread 2.05c (n = 22 two-sided), and median top-of-book `yes_ask_size_fp` 85.00.
  - Out-of-universe page-0 contracts had median `volume_24h_fp` 0.00, median spread 5.15c, and median top YES ask size 100.00.
- **Recovered smoke** (2026-09-24 05:20Z, three contracts): visible ask quantity AL-01 YES 98 / NO 50; AL-02 YES 23,211.90 / NO 225.60; AL-03 YES 218 / NO 8.
- **Headline comparison:** `CONTROLH-2026-R` `volume_24h_fp` 841,209.14 and OI 15,087,531.98; `CONTROLH-2026-D` 297,082.75 and 8,764,699.69 (received 23:50:19Z). The race contracts are thin relative to the chamber market, which is consistent with the "neglected" premise and also means capacity is small.
- **Capacity estimate** (frozen for reporting): feasible size per signal ≈ min(requested, visible top-of-book quantity) ≈ tens to low hundreds of contracts.
  - With about 9 signals × about 85 contracts × about $0.5, top-of-book deployable capital is about **$380 for the whole cycle**.
  - The 2024 expected margin was about 4c per contract, so the ex-ante expected value is about **$30 for the cycle** before any adverse selection. This is an order-of-magnitude estimate, not a result.
- **Capital-hours per contract:** price × hours from 2026-11-02T22:00Z to settlement.
  - Upper bound, settling after the swearing-in (term begins Jan 3, 2027; expiration is the first 10:00 AM ET after swearing-in): about 1,500 h, so a $0.50 contract is about 750 $-h.
  - Lower bound, accelerated determination days after the election: about 50–300 h, i.e. 25–150 $-h per $0.50 contract.
  - The 2024 contracts settled Jan 3, 2025 (RESULTS.md). The Examiner reports realized hours.

## 9. Preregistration (p16 "Minimum preregistration"; v1.2 §J items 1–12, statuses null for the Examiner)

| # | Item | Declared in |
|---|---|---|
| 1 | Market universe | §3 (92 races, frozen list) |
| 2 | Exclusions | §3 (AK-01), §5 decision-time exclusions |
| 3 | Receipt-time information set | §5 (24 h lag, 7-day max age, our receipt governs, book window 21:45–22:15Z) |
| 4 | Fee regime | §5 (R1-P1 pin; manifest pending, so net stays null) |
| 5 | Order timing | §5 (taker at decision snapshot) |
| 6 | Sizing | §5 (≤ 1 contract per race; NH-001 gate) |
| 7 | Fill model | §5 (visible qty ≥ 1; stress rows) |
| 8 | Stopping rules | Single decision time; scoring after all universe contracts settle or on 2027-02-15, whichever is first. Unsettled contracts are reported as unresolved inventory, never marked. No early stop. |
| 9 | Evaluation metrics | §6 |
| 10 | Limit candidate variants | One source × one decision time × knob w ∈ {0.25, **0.5**, 1.0} + market-only + no-trade. Nothing else. |
| 11 | Log every attempted variant | `card01_hybrid_forecast/LEDGER_2026-09-24.md` |
| 12 | Separate discovery / tuning / untouched evaluation | Discovery: 2024 NH-001/NH-001A (done, preserved). Tuning: **none** (w fixed at 0.5 from exploration only). Untouched evaluation: 2026 outcomes (not yet occurred). |

**Rejection rule (verbatim, research PDF Card 01):** "Freeze one family and its forecast sources before observing future outcomes. Record revisions and orderbooks at actual receipt time. Compare the three baselines under identical feasible fills, then test the hybrid on untouched events. Reject if its gains disappear against market-only, are concentrated in one correlated event, or exist only at midpoints. Treat this as a slower research stream; one election cycle is not hundreds of independent experiments."

**Operationalized (any one means REJECT):**
- (a) The upper bound of the state-bootstrap CI of D is ≥ 0.
- (b) The recentered (common-factor) CI includes 0.
- (c) The gain exists only against the mid, not against executable prices: the hypothetical taker P&L at ask is ≤ 0, or ≤ 0 under the one-tick-worse stress.
- (d) Top-1 race share of positive P&L is > 50%, or dropping the best two winners leaves ≤ $0 (the NH-001 check).

## 10. Collector ask (GET-only; lands under `/workspace/lab/astra-capture/card01-nh002-house/`)

1. ElectIndex `output/races_summary.csv`, pulled daily from now until 2026-11-03, with receipt time and sha256. Raw bytes only.
2. `KXHOUSERACE` open-markets full pagination, weekly. Record `rules_primary` for all universe `-D` contracts.
3. Orderbooks for the 92 `-D` contracts between 21:45Z and 22:15Z on 2026-11-02, and again at 2026-11-03T22:00Z for adverse selection. About 92 requests at a 3 s throttle is about 4.6 min per pass.
4. A pipeline dry-run pass at 22:00Z on 2026-10-12, 10-19 and 10-26. These passes are **not scored**.
5. Settled `result` for each contract after settlement.

Throttle 2–3 s. On a 429, back off 60–90 s and log it. Never fill gaps. The shared egress IP produced 429s today.

## 11. Dead-card / live-pin overlap

| Card | Overlap | Handling |
|---|---|---|
| **FEAT-20260912-001 / -002 (F1, INACTIVE), TEST-20260912-002** | Nearest dead card: model/market linear blend p = (1−λ)m + λ·p_struct, λ = 0.35, scored vs the Kalshi mid incumbent `MKT-KALSHI-15M-MID`. Verdict REDUNDANT/FAIL-INSUFFICIENT. **No cemetery record exists.** | Different domain (BTC 15-min), but the same blend form. Rejection (a) is the same incremental-over-mid test. The weight is fixed (0.5), not borrowed from λ = 0.35. |
| NH-001 / NH-001A @ 2253c03c | Predecessor (preserved control) | Not altered or re-scored. No event overlap (§3). |
| RJ harnesses (C3-RJ etc.) | None altered | Settled-join pattern reused conceptually only |
| Q6-`000`, S2/R2-P4, CEM-ASTRA-20260922-001, archive CEM-2026091x | None | Orthogonal |

## 12. Mandatory instrument pins

| Dep | Pin |
|---|---|
| Fee | R1-P1 `kalshi_feebook_lab_20260922/` @ `22371178cb2663250b4762f328069571c48cb551` |
| Rails | R1-P5 `kalshi_rails_lab_20260922/` @ `6a28e0d6254327ea4e6451c781bec56215ac6cac` |
| Predecessor | `17thgreen/GPT-6-Astra-Deathmatch` @ `2253c03cd86eb5515325f1d91b43bdcbea7a902c` |
| Charter | `6a02cb468a4b6c600fc3a16078a216a6095321c6bc92c24b2a7aca58f149daa8` |

## 13. Do-not-modify

1. No live orders.
2. No invented PnL.
3. Do not alter or re-score 2253c03c, the 50/50 blend as originally declared, Q6-000, or the RJ harnesses.
4. No source substitution.
5. No change to w, the universe or the decision time after this freeze.
6. No backdating from ElectIndex history.
7. No imputation.

## 14. Empty results (on disk)

`packets/card01_hybrid_forecast/FROZEN_EXPERIMENT.json`, `results.json`, `results/EMPTY_RESULTS.json` (NOT_RUN).

## 15. Done =

Freeze, stubs and ledger on disk. Then: Conductor ACCEPT → Archivist source/ToS decision (§2a) → Collector capture → Variants implementation → Examiner scoring after settlement.

## Frozen-at

`2026-09-24T23:52:48Z` UTC. Deep Research, under charter `6a02cb46…`.
