# SCOUT — Card 06 Company-KPI Open-Window Census

- **Seat:** Market Scout (Astra/Kalshi desk)
- **Written:** 2026-09-24 23:43:40 EDT (ET)
- **Mode:** READ-ONLY. GET-only public Kalshi API + company IR/press pages (box browser when curl SPA-empty). No orders, no build, no P&L, no fills, no VPN/proxy. House-fee work out of scope.
- **Freeze (must read first):** `packets/scout_card06_company_kpi/FREEZE_CARD06_COMPANY_KPI_2026-09-24.md` · sha256 `1413603c964fa8087ea396997e5ecb56c0b0a21e5b3d497629b6078d7fb4a1e8` · freeze_time_ET **2026-09-24 21:41:48 EDT**
- **Amendments:** A01 (KX primary series remapping) `69d1c4ec…`; A02 (legacy event_ticker prefixes) `3a19829d…`
- **Raw:** `packets/scout_card06_company_kpi/raw/` + `MANIFEST.sha256`. Pre-freeze existence probes discarded in `PRE_FREEZE_DISCARDED_2026-09-24/`.
- **Method:** `script/census.py` (post-A02) on post-freeze bodies only. Open-window = arrival < close_time (tolerance **0 min**; equal = NO). Arrivals from company IR calendars / dated releases only (UNSOURCED if date-only or absent).
- **Parent:** Conductor ACCEPT Card 06 macro census (db3b0a18…); CEM-ASTRA-20260924-006; KXTESLA PARK; MIXED=NO_BUILD; no OPEN-WINDOW → no build.

## Family verdicts (headline)

| Family | Series | Verdict | n / sourced / YES / NO / UNSOURCED | Notes |
|---|---|---|---|---|
| Meta DAP | KXMETADAP | **MIXED** (lt20) | 8 / 8 / 5 / 3 / 0 | Arrival = Meta IR Past Events earnings-call time (PT→ET). 3 rows close 16:00 same day as 17:00 call → NO; others close after call → YES. |
| Spotify subscribers | KXSPOTIFYSUBS | **UNSOURCED** (lt20) | 7 / 0 / 0 / 0 / 7 | IR events list dates without clock times → UNSOURCED per freeze. |
| Netflix subscribers | KXNETFLIXSUBS | **UNSOURCED** (lt20) | 4 / 0 / 0 / 0 / 4 | Shareholder letters date-only (no clock) → UNSOURCED. |
| NYT subscribers | KXNYTSUBS | **UNSOURCED** (lt20) | 7 / 0 / 0 / 0 / 7 | nytco.com/investors events date-only → UNSOURCED. |
| Coinbase volume | KXCBVOLUME | **MIXED** (lt20) | 9 / 9 / 7 / 2 / 0 | Arrival = Coinbase IR earnings-call 5:30 PM ET. Two NO (Q1-25 close before May 8 call; Q2-25 close 16:00 vs call 17:30). |

**OPEN-WINDOW families:** none.
**CEMETERY families:** none (no family with ≥1 sourced row and all sourced NO).
**MIXED (NO_BUILD):** KXMETADAP, KXCBVOLUME.
**UNSOURCED / PARK:** KXSPOTIFYSUBS, KXNETFLIXSUBS, KXNYTSUBS.
**Excluded / PARK (series):** KXTESLA (IR 403; Conductor).

## Main table

Machine table: `packets/scout_card06_company_kpi/out/census_rows.csv` (36 lines incl. header).

| family | contract (event) | settlement source (rule snippet) | source arrival ET (evidence) | close ET (API `close_time`) | open window | gap_min |
|---|---|---|---|---|---|---|
| KXMETADAP | KXMETADAP-26-Q4 | If Meta has more than 3.5 billion daily active people, on average, for the last… | 2026-01-28 16:30:00 EST · dated-schedule | 2026-01-30 18:39:21 EST | **YES** | 3009.35 |
| KXMETADAP | KXMETADAP-25-Q3 | If Meta has more than 3.3 billion daily active people, on average, for the last… | 2025-10-29 16:30:00 EDT · dated-schedule | 2025-10-31 16:00:00 EDT | **YES** | 2850.0 |
| KXMETADAP | KXMETADAP-25-Q2 | If Meta has more than 3.35 billion daily active people, on average, for the las… | 2025-07-30 17:00:00 EDT · dated-schedule | 2025-07-31 16:00:00 EDT | **YES** | 1380.0 |
| KXMETADAP | KXMETADAP-25-Q1 | If Meta has more than 3.3 billion daily active people, on average, for the last… | 2025-04-30 17:00:00 EDT · dated-schedule | 2025-04-30 16:00:00 EDT | **NO** | -60.0 |
| KXMETADAP | KXMETADAP-24-Q4 | If Meta has more than 3.2 billion daily active people, on average, for the last… | 2025-01-29 17:00:00 EST · dated-schedule | 2025-01-29 17:41:03 EST | **YES** | 41.07 |
| KXMETADAP | METADAP-24-Q3 | If Meta has more than 3.3 billion daily active people, on average, for the last… | 2024-10-30 17:00:00 EDT · dated-schedule | 2024-10-30 21:19:42 EDT | **YES** | 259.71 |
| KXMETADAP | METADAP-24-Q2 | If Meta has more than 3.21 billion daily active people, on average, for the las… | 2024-07-31 17:00:00 EDT · dated-schedule | 2024-07-31 16:00:00 EDT | **NO** | -60.0 |
| KXMETADAP | METADAP-24-Q1 | If Meta has more than 3.19 billion daily active people, on average, for the las… | 2024-04-24 17:00:00 EDT · dated-schedule | 2024-04-24 16:00:00 EDT | **NO** | -60.0 |
| KXSPOTIFYSUBS | KXSPOTIFYSUBS-25-Q3 | If Spotify has more than 300 million subscribers in 2025 Q3, then the market re… | UNSOURCED · date-only-ir-events | 2025-10-31 16:00:00 EDT | **UNSOURCED** |  |
| KXSPOTIFYSUBS | KXSPOTIFYSUBS-25-Q2 | If Spotify has more than 225 million subscribers in 2025 Q2, then the market re… | UNSOURCED · date-only-ir-events | 2025-07-31 16:00:00 EDT | **UNSOURCED** |  |
| KXSPOTIFYSUBS | KXSPOTIFYSUBS-25-Q1 | If Spotify has more than 265 million subscribers in 2025 Q1, then the market re… | UNSOURCED · date-only-ir-events | 2025-04-29 09:50:09 EDT | **UNSOURCED** |  |
| KXSPOTIFYSUBS | KXSPOTIFYSUBS-24-Q4 | If Spotify has more than 245 million subscribers in 2024 Q4, then the market re… | UNSOURCED · date-only-ir-events | 2025-01-31 16:00:00 EST | **UNSOURCED** |  |
| KXSPOTIFYSUBS | SPOTIFYSUBS-24-Q3 | If Spotify has more than 245 million subscribers in 2024 Q3, then the market re… | UNSOURCED · date-only-ir-events | 2024-10-31 16:00:00 EDT | **UNSOURCED** |  |
| KXSPOTIFYSUBS | SPOTIFYSUBS-24-Q2 | If Spotify has more than 236 million subscribers in 2024 Q2, then the market re… | UNSOURCED · date-only-ir-events | 2024-07-24 12:56:41 EDT | **UNSOURCED** |  |
| KXSPOTIFYSUBS | SPOTIFYSUBS-24-Q1 | If Spotify has more than 236 million subscribers in 2024 Q1, then the market re… | UNSOURCED · date-only-ir-events | 2024-04-23 11:34:34 EDT | **UNSOURCED** |  |
| KXNETFLIXSUBS | NETFLIXSUBS-24-Q4 | If Netflix adds 6 million subscribers or more in 2024 Q4, then the market resol… | UNSOURCED · date-only-letter | 2025-01-25 00:36:06 EST | **UNSOURCED** |  |
| KXNETFLIXSUBS | NETFLIXSUBS-24-Q3 | If Netflix adds 6 million subscribers or more in 2024 Q3, then the market resol… | UNSOURCED · date-only-letter | 2024-10-18 10:04:50 EDT | **UNSOURCED** |  |
| KXNETFLIXSUBS | NETFLIXSUBS-24-Q2 | If Netflix adds 2 million subscribers or more in 2024 Q2, then the market resol… | UNSOURCED · date-only-letter | 2024-07-19 10:03:14 EDT | **UNSOURCED** |  |
| KXNETFLIXSUBS | NETFLIXSUBS-24-Q1 | If Netflix adds 2 million subscribers or more in 2024 Q1, then the market resol… | UNSOURCED · date-only-letter | 2024-04-15 16:00:00 EDT | **UNSOURCED** |  |
| KXNYTSUBS | KXNYTSUBS-25-Q3 | If the New York Times has added more than 275000 net digital subscribers in 202… | UNSOURCED · date-only-ir-events | 2025-10-31 10:00:00 EDT | **UNSOURCED** |  |
| KXNYTSUBS | KXNYTSUBS-25-Q2 | If the New York Times has added more than 200000 net digital subscribers in 202… | UNSOURCED · date-only-ir-events | 2025-07-31 10:00:00 EDT | **UNSOURCED** |  |
| KXNYTSUBS | KXNYTSUBS-25-Q1 | If the New York Times has added more than 275000 net digital subscribers in 202… | UNSOURCED · date-only-ir-events | 2025-05-07 15:13:55 EDT | **UNSOURCED** |  |
| KXNYTSUBS | KXNYTSUBS-24-Q4 | If the New York Times has added more than 300000 net digital subscribers in 202… | UNSOURCED · date-only-ir-events | 2025-02-05 10:06:35 EST | **UNSOURCED** |  |
| KXNYTSUBS | NYTSUBS-24-Q3 | If the New York Times has added more than 100000 net digital subscribers in 202… | UNSOURCED · date-only-ir-events | 2024-11-06 15:04:20 EST | **UNSOURCED** |  |
| KXNYTSUBS | NYTSUBS-24-Q2 | If the New York Times has added more than 150000 net digital subscribers in 202… | UNSOURCED · date-only-ir-events | 2024-08-07 11:43:33 EDT | **UNSOURCED** |  |
| KXNYTSUBS | NYTSUBS-24-Q1 | If the New York Times has added more than 250000 net digital subscribers in 202… | UNSOURCED · date-only-ir-events | 2024-05-08 10:45:47 EDT | **UNSOURCED** |  |
| KXCBVOLUME | CBVOLUME-24-Q1 | If Coinbase has more than 468 billion total volume in 2024 Q1, then the market … | 2024-05-02 17:30:00 EDT · dated-schedule | 2024-06-30 16:00:00 EDT | **YES** | 84870.0 |
| KXCBVOLUME | KXCBVOLUME-26-Q4 | If Coinbase reports above 200 trading volume in Q4 2025, then the market resolv… | 2026-02-12 17:30:00 EST · dated-schedule | 2026-02-13 22:18:20 EST | **YES** | 1728.33 |
| KXCBVOLUME | KXCBVOLUME-Q3-25 | If Coinbase has more than 210 billion total volume in 2025 Q3, then the market … | 2025-10-30 17:30:00 EDT · dated-schedule | 2025-10-31 16:00:00 EDT | **YES** | 1350.0 |
| KXCBVOLUME | KXCBVOLUME-Q2-25 | If Coinbase has more than 220 billion total volume in 2025 Q2, then the market … | 2025-07-31 17:30:00 EDT · dated-schedule | 2025-07-31 16:00:00 EDT | **NO** | -90.0 |
| KXCBVOLUME | KXCBVOLUME-Q1-25 | If Coinbase has more than 360 billion total volume in 2025 Q1, then the market … | 2025-05-08 17:30:00 EDT · dated-schedule | 2025-04-30 16:00:00 EDT | **NO** | -11610.0 |
| KXCBVOLUME | KXCBVOLUME-Q4-24 | If Coinbase has more than 200 billion total volume in 2024 Q4, then the market … | 2025-02-13 17:30:00 EST · dated-schedule | 2025-02-14 02:12:17 EST | **YES** | 522.3 |
| KXCBVOLUME | CBVOLUME-Q3-24 | If Coinbase has more than 200 billion total volume in 2024 Q3, then the market … | 2024-10-30 17:30:00 EDT · dated-schedule | 2024-10-31 10:00:04 EDT | **YES** | 990.08 |
| KXCBVOLUME | CBVOLUME-Q2-24 | If Coinbase has more than 250 billion total volume in 2024 Q2, then the market … | 2024-08-01 17:30:00 EDT · dated-schedule | 2024-08-02 10:06:18 EDT | **YES** | 996.31 |
| KXCBVOLUME | CBVOLUME-Q1-24 | If Coinbase has more than 154 billion total volume in 2024 Q1, then the market … | 2024-05-02 17:30:00 EDT · dated-schedule | 2024-05-03 10:47:14 EDT | **YES** | 1037.24 |

## Family verdicts
- **KXMETADAP**: **MIXED** — n=8, sourced=8, YES=5, NO=3, UNSOURCED=0, lt20=True, partial=False
- **KXSPOTIFYSUBS**: **UNSOURCED** — n=7, sourced=0, YES=0, NO=0, UNSOURCED=7, lt20=True, partial=True
- **KXNETFLIXSUBS**: **UNSOURCED** — n=4, sourced=0, YES=0, NO=0, UNSOURCED=4, lt20=True, partial=True
- **KXNYTSUBS**: **UNSOURCED** — n=7, sourced=0, YES=0, NO=0, UNSOURCED=7, lt20=True, partial=True
- **KXCBVOLUME**: **MIXED** — n=9, sourced=9, YES=7, NO=2, UNSOURCED=0, lt20=True, partial=False

## Blockers / notes
- Legacy Companies-category tickers (METADAP, …) exist but markets live under **KX** series_ticker (A01). Historical also returns legacy event prefixes (A02).
- Heavy Kalshi 429s; ERRORBODY files retained; empty open/settled arrays are real zeros for these series today.
- Meta/Coinbase arrivals use **earnings-call** times from official IR event calendars (DAP/volume published in associated earnings materials that day). Press-release PDFs for Meta are date-only (no clock); Netflix letters date-only.
- Spotify / Netflix / NYT: no company-published clock time found on accessible IR pages → honest **UNSOURCED** (not cemetery).
- No OPEN-WINDOW family → **no build, no P&L, no fills, no orders** from this census.
- lt20 honest on all five families (max events retrieved after historical ≤9).

## Paths
- Freeze: `lab/governance/astra/packets/scout_card06_company_kpi/FREEZE_CARD06_COMPANY_KPI_2026-09-24.md`
- Brief: `lab/governance/astra/SCOUT_CARD06_COMPANY_KPI_OPEN_WINDOW_2026-09-24.md`
- Census JSON: `lab/governance/astra/packets/scout_card06_company_kpi/out/census.json`
