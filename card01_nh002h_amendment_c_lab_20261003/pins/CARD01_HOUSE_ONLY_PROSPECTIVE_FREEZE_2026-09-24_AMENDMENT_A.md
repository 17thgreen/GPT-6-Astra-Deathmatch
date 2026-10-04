# AMENDMENT A to CARD01-NH002-HOUSE-PROSPECTIVE: contract-mapping correction (pre-outcome, disclosed)

**Amends:** `packets/CARD01_HOUSE_ONLY_PROSPECTIVE_FREEZE_2026-09-24.md` (frozen 2026-09-24T23:52:48Z). That file is left byte-for-byte unchanged.
**Filed:** `2026-09-24T23:59:50Z` UTC. This is before the decision time (2026-11-02T22:00Z) and before any 2026 outcome exists.
**Why this amendment is needed:**
- The full `KXHOUSERACE` open-market pagination came back after the freeze. It covers 707 contracts across 351 races (pages received between 23:48:58Z and 23:57:08Z).
- Only **58 of the 92** frozen races have an open `KXHOUSERACE-…-26-D` contract.
- The other 34 are the most-watched competitive districts. They are listed under **per-district legacy series** that also use HOUSEPARTY terms (raw series list, `live_get_2026-09-24/series_list_*.json`):
  - AZ-01 HOUSEAZ1, AZ-02 HOUSEAZ2, AZ-06 HOUSEAZ6
  - CA-22 HOUSECA22
  - CO-03 HOUSECO3, CO-08 HOUSECO8
  - FL-13 HOUSEFL13
  - IA-03 HOUSEIA3
  - ME-02 HOUSEME2
  - MI-04 HOUSEMI4, MI-07 HOUSEMI7 / HOUSEPARTY-MI07, MI-10 HOUSEMI10
  - MT-01 HOUSEMT1
  - NC-01 HOUSENC1, NC-11 KXHOUSENC11
  - NE-02 HOUSENE2
  - NH-01 HOUSENH1
  - NJ-07 HOUSENJ7
  - NY-17 HOUSENY17
  - OH-09 HOUSEOH9
  - PA-01 HOUSEPA1, PA-07 HOUSEPA7, PA-08 HOUSEPA8, PA-10 HOUSEPA10
  - TX-09 KXHOUSETX9, TX-15 HOUSETX15, TX-32 KXHOUSETX32, TX-34 HOUSETX34, TX-35 KXHOUSETX35
  - VA-01 HOUSEVA1, VA-02 HOUSEVA2
  - WA-03 HOUSEWA3
  - WI-01 HOUSEWI1, WI-03 HOUSEWI3
- Under the frozen rule "no `-D` contract → exclude", the test would silently drop the competitive core. NH-001 itself used exactly these legacy series for 2024 (e.g. `HOUSEAZ1-24-D`).

**What changes (mapping only):**
- For each of the 92 frozen races, the contract is the Democratic-party contract for the 2026 election (term beginning 2027). Candidate series are searched in this fixed order:
  1. `KXHOUSERACE`
  2. `HOUSE<ST><N>`
  3. `HOUSEPARTY-<ST><NN>`
  4. `KXHOUSE<ST><N>`
- The first series that has an open market meeting both conditions below is used:
  - (a) its `rules_primary` names the same seat, the term beginning in 2027, and the Democratic Party;
  - (b) its contract terms are HOUSEPARTY.
- Series whose markets are candidate-named ("Who will win TX-09") qualify only if a Democratic-**party** market exists. Otherwise the race is excluded, with reason `no_party_contract`.
- The Collector resolves the mapping from raw GETs **before 2026-10-26** and writes `MAPPING_2026_HOUSE.json` (ticker, series, rules text sha256, receipt time). Mapping is decided on rules text only. **Prices, depth and volume may not influence it.**

**What does not change:**
- The universe (92 races), w = 0.5, knob levels, decision time, source, fee and rails pins, tests, and rejections.

**Disclosure:**
- Deep Research has viewed `KXHOUSERACE` prices (step5/step6 raw pages) but has **not** viewed any legacy-series 2026 prices.
- The amendment was written from series metadata only.
- It adds no variant. It restores the admission the frozen universe intended.
- Logged as ledger entry A1.
- The capacity numbers in freeze §8 came from `KXHOUSERACE` page 0 only. The all-pages figures are in `card01_hybrid_forecast/EXPLORE_DIAG_KXHOUSERACE_liquidity_ALLPAGES_2026-09-24.txt`. They cover 58 in-universe races / 117 contracts: median `volume_24h_fp` 3.04, sum 47,809.50, median OI 4,777.11, median spread 2.8c, median top YES ask size 200.00. They exclude the 34 legacy-series races, whose liquidity is unmeasured.
