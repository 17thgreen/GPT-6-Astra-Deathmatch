# EXT-K2: OPTIMISM-TAX DEPENDENCE STRESS (Q6-000 = NO-maker vs YES-taker flow). MEASUREMENT / DESCRIPTIVE-ONLY FREEZE (spec only; no results run)

**File date:** `2026-10-03` (ET). **Frozen / declared at:** `2026-10-03T16:48:49-04:00` (ET, America/New_York, UTC−4). Every rule below, including each UNPINNED resolution, was stated **before** any implementation. For this packet Variants has computed **no markout, no tercile attribution of any 000 fill, no Becker taker-YES share, no maker-NO or maker-YES excess, no fee total, no PnL and no ROI**. The only numbers computed are the structural, label-free counts in §3 and the label-free tercile fixture in §4, both of which the commission asked for.
**Owner:** R&D Variants (freeze; implementation only after Conductor ACCEPT) → one Variants cloud (implements code; runs part (a)) → Simulator (runs part (b) **on the box only**) → Examiner (verdict, account-class pin). Clock co-signs the part (b) execution-split and fee-proxy items (§11).
**Status:** FROZEN, FREEZE_ONLY. Awaiting Conductor **ACCEPT + IMPLEMENT GO**. This packet involves no cloud, no PR, no commit, no push, no message, no network GET of any kind, no orders, no `admit.py`, no `capture.sqlite` and no weather `archive.sqlite`. It writes only new files, all on the box.
**Experiment id:** `EXT-K2-OPTIMISM-TAX-DEPENDENCE-STRESS` · **Kernel:** EXT-K2 (Scout external hunt 2026-10-03) · **Incumbent stressed:** Q6-000 (`q3300_d0.25_000`, NFL `KXNFLGAME` maker pairing allocator, SHADOW)
**Sister freeze / format template:** EXT-K1 `packets/VARIANTS_EXT_K1_Q6000_LEGGING_RISK_AUDIT_FREEZE_2026-10-03.md` (`5c40fb9d…`), Conductor-ACCEPTED 16:16:49 ET. K2 **cites** K1's pinned inputs and definitions rather than redefining them (e.g. "K1 R18").
**Feature family:** `optimism_tax_dependence_stress` (measurement). **Knobs on 000: zero. Parameters of 000 changed: zero.**
**Evidence tags:** [V] verified on box in a pinned file or re-derived this session · [I] inferred · [H] hypothesis · [A] assumption / external prior · [U] unknown. **Every Becker-derived claim is at most [A].** (The Clock uses "[A]" to mean "external prior". Here [A] covers both senses, and no Becker claim may ever be upgraded.)
**Proposed lab dir:** `kalshi_ext_k2_optimism_tax_lab_20261003/`. Not created. The **single** K2 cloud creates it at implementation time, after ACCEPT.

---

## 0. Governing ruling, Clock verdict and commission (verbatim)

### 0.1 Ruling
`packets/CONDUCTOR_RULING_SCOUT_EXTERNAL_HUNT_2026-10-03.json`, sha256 `870895a58e80fd1442d0ce97e42df02426bf7e38f64dcd091efc6fbf26b74ebf` [V]. The K1 freeze §0 quotes the full bytes. The keys that bind K2, verbatim:

> `"EXT-K2": "TRY box part second (flow-mix tercile stress on B1/B2). Season-scale via Becker archive after extract + Clock audit."`
>
> `"becker_archive": "ALLOWED under dd1d7039: public third-party research dataset, not a Kalshi endpoint and not throttle evasion. Collector owns a streamed filtered extract (Kalshi NFL/sports series only) - never store the full 36 GB tar; extract output cap 5 GB; abort if box free disk < 12 GB; record URL, HEAD size/Last-Modified, license from repo README, and sha256 of extract. Clock provenance audit required before any Examiner use. Trade-only, gross-of-fee, no quotes: an external prior [A], can never replay or promote 000."`
>
> `"fee_rounding": "Examiner pins. Until account member-type is resolved, score with the conservative non-direct-member rule (fees rounded up to $0.01 per order); may also report the $0.0001 direct-member figure as a sensitivity, never as the headline."`
>
> `"dev_grade": "All box-scorable results on the reused 31-game dev cohort are dev-grade, not OOS; no KEEP from them."`

### 0.2 Clock provenance audit: VERDICT CAVEAT (limits quoted verbatim)
`packets/CLOCK_PROVENANCE_BECKER_ARCHIVE_2026-10-03.md` sha256 `e7424a130e95b72d288d567ef75b00804672b29b15bd93889aafb0722fd84d80` and its json `dc54e3dae4bbeeffc0e1c792bd769a2d63daee02a974dbff03d04da8780eebc3` [V]. A byte-identical copy of each is at `lab/astra-capture/external/becker_2026-10-03/clock/` [V]. Issued 2026-10-03T16:35:27-04:00.

> ## VERDICT: **CAVEAT**
>
> The archive is usable **only as an [A] external prior**, with the limitations below. There is no holdout, dev-cohort or ADMIT-1 contamination. Timestamp semantics are established for every time column. There is no structural defect: no duplicate rows, no duplicate trade_ids, no nulls in key fields, and all counts match the ADMISSION json.
> **Tags stay [A]. This archive can never replay, score, or promote strategy 000 (or any Astra strategy), and it is never holdout, OOS, or confirmatory evidence.**
>
> Named limitations: (a) it cannot be cross-checked against our own tape, because there is zero time or ticker overlap [V]. (b) Markets still open at the 2025-11-25 hard end are truncated [V]. (c) Trades exist only for markets with snapshot volume ≥ 100 [V code / I data]. (d) Closed-market trade sums fall slightly short of `volume` on some tickers [V]. (e) On no-result/void markets, `close_time` does not mark the end of trading [V]. (f) The data licence is unknown [U]. (g) The commission's LICENSE pin prefix is mislabelled (see Pins).

> ## Safe uses
> - [A] external prior for season-scale descriptive stats on 2024-12..2025-11 Kalshi sports trades (e.g. EXT-K2 flow-mix tercile stress), labelled [A], gross of fees, trade-only
> - Base rates / priors that are computed only on closed markets with yes/no results (filter close_time <= _fetched_at and result in {yes,no})
> - Sanity ranges for print size, cadence, price-band mix, pre/in-game split
>
> ## Unsafe uses
> - Any replay, scoring, KEEP or promotion of strategy 000 or any Astra strategy
> - Any use as holdout, OOS, or confirmatory evidence; any mixing into dev-cohort, holdout, or ADMIT-1 rows
> - Quote, depth, queue, fill, or fee modelling (no quotes/book; markets yes_bid/ask are a single 2025-11-23 snapshot)
> - Per-game metrics on markets open at 2025-11-25 (truncated) or on no-result/void markets (close_time unreliable)
> - Treating close_time as the trading end without checking it per series (t0/t3 resolved: prints up to 60 s after close; t1/t2/t4 and void markets: hours); using (ticker,price,count,side,time) as a unique key
> - Any redistribution of the data until the data licence is resolved [U]

Clock §5 recommendation, verbatim: "Recommendation: internal research use only, with attribution, and no redistribution until resolved."
Clock §2 cross-check note, verbatim: "(ticker, price, count, side, time) is **not unique** in Becker (t0 has 57,027 rows that share that tuple but carry distinct trade_ids), so match on trade_id only."

Every limit above is bound as a rule in §5 (R04–R09, R30–R47) and, wherever code can enforce it, as a named refusal and test in §8. **One tension needs a co-sign:** the Clock lists "fee modelling" as unsafe, while the commission orders net-of-fee figures. See R39 (UNPINNED) for the resolution.

### 0.3 Commission: Conductor's 16:36 ET message (verbatim, as relayed in the task)
No on-box file carries this message. It was relayed in the delegation text, so its provenance is [U] and the Archivist should file it. Quoted verbatim:

> COMMISSION (quote Conductor's 16:36 ET message as the commission):
> (a) DEV-TAPE part (box): split 000's open-leg markout by taker-YES-share regime. Use terciles of taker-YES share, defined label-free on the dev tape; pre-declare the unit (per game? per ticker-hour?) and the tercile cut method. The Scout brief mentions B1/B2. Read it and define them exactly.
> (b) SEASON-SCALE part on Becker 2025: DESCRIPTIVE only. Measure the stability of the taker-YES skew and the maker-NO surplus across weeks and price bands. First gross of fees, then net with maker fee 0.0175·p(1−p) and taker fee 0.07·p(1−p), each with the $0.01-per-order round-up (state the per-trade proxy, because Becker has trades, not orders). Label fees CACHE_NOT_R1P1. Note: the 'maker-NO surplus' needs settlement results, so it is label-dependent. That's fine for descriptive Becker-only, but state it explicitly and keep it out of anything feeding a gate.
>
> CLOCK'S BINDING LIMITS (must appear as rules plus code-enforced refusals where possible):
> - No replay, score, KEEP or promotion from Becker. No mixing Becker with dev, holdout or ADMIT-1 rows: separate pipelines, plus a test that refuses the mix.
> - No quote, depth, fill or queue modelling on Becker.
> - Exclude the 56 still-open KXNFLGAME tickers, and any market without a yes/no result, from per-game metrics. Pin the exclusion list by sha.
> - close_time is NOT end of trading.
> - Any cross-check (e.g. Becker vs the dev tape on overlapping 2026 games, if any) joins on trade_id only.
> - Trades exist only for markets with volume ≥ 100: state the selection bias.
> - No redistribution while the license is [U]. CONSEQUENCE YOU MUST RESOLVE: raw Becker files must NOT be committed to GitHub or put in a cloud-attached bundle. Propose an execution split, e.g. part (a) by one cloud from a bundle of non-Becker pins as usual, while part (b) runs box-only from a frozen script whose committed outputs are aggregates only (no row-level data). Or another compliant design. State it as a rule.
> - The holdout (74507e1a, pre-reg 9a987a77 / 370dc31d) and the ADMIT-1 window [2026-09-27T00:00Z, 2026-09-30T04:00Z) are refused in code.
> - The verdict domain is DESCRIPTIVE, ITERATE or INCONCLUSIVE only. No KEEP, no KILL, no retune of 000, results/pnl null in the packet.

| # | Requirement | Where met |
|---|---|---|
| C1 | (a) open-leg markout split by taker-YES terciles, label-free, unit + cut method pre-declared | R10–R25, §4 fixture |
| C2 | B1/B2 defined exactly | R10, §2.1 |
| C3 | (b) stability of taker-YES skew and maker-NO surplus across weeks and price bands, gross then net | R30–R44 |
| C4 | Fee coefficients, $0.01 round-up, per-trade proxy stated, CACHE_NOT_R1P1 | R38–R39; T09 |
| C5 | maker-NO surplus is label-dependent; stated; kept out of any gate | R37, R44; T15 |
| C6 | Clock limits as rules + code refusals | R04–R09, R30–R47; T05–T08, T11–T14, T17 |
| C7 | Exclusion list pinned by sha | R32; `BECKER_EXCLUSION_LIST_KXNFLGAME.json` `61a4c993…` |
| C8 | Execution split (licence consequence) as a rule | **R04**, §9 |
| C9 | Holdout + ADMIT-1 refused in code | R07; T08 |
| C10 | Verdict domain {DESCRIPTIVE, ITERATE, INCONCLUSIVE}; results/pnl null | R08, R23, R44; `EMPTY_RESULTS.json` |
| C11 | Tests: permutation, mix refusal, open-ticker exclusion, holdout/ADMIT-1, fee units, manifest tamper, no row-level output | §8 T01–T17 |
| C12 | Cloud bundle from non-Becker pins only; Becker box-only manifest; packet dir with MANIFEST | §10 |

## 1. What is stressed (read from box; cited from K1 §1)

- Q6-000 = `q3300_d0.25_000`, a SHADOW-only hypothetical replay (K1 §1) [V]. Every quantity in part (a) describes the **replayed** 000, not real execution [V].
- Scout §0 [V]: of 000's maker contracts, 321,622.45 (98.97%) are NO-side. The replay fills a resting NO when a trade prints with `taker_side=yes` (`replay_v2.py:218`, `queue_policies.py:37`). K1 §3.1 re-derived this, and it reproduces.
- Dev-tape flow [V, re-derived this session, §3]: taker-YES contract share **0.9168821893496498** (43,386,453.85 of 47,319,551.36 contracts; 636,251 of 681,732 trades). K1 §3.2 matches.
- Thesis [H]: 000's dev-cohort result may be the YES-optimist surplus at one point in time (Becker; Bartlett–O'Hara, per Scout §3 [V saved pages / I]). K2 **measures** how 000's open-leg markouts vary with the flow mix on the dev tape (a), and how stable the 2025 season-scale taker-YES skew and maker-NO surplus are (b, an [A] prior). It does not test, tune, gate, keep or kill 000.

## 2. Pins (re-hashed on box 2026-10-03 16:36–16:45 ET; all MATCH the requested prefixes)

| Item | Path (relative to `/workspace/`) | sha256 | Notes |
|---|---|---|---|
| **Ruling** | `lab/governance/astra/packets/CONDUCTOR_RULING_SCOUT_EXTERNAL_HUNT_2026-10-03.json` | `870895a58e80fd1442d0ce97e42df02426bf7e38f64dcd091efc6fbf26b74ebf` | [V] |
| **Scout brief (post-edit)** | `lab/governance/astra/SCOUT_EXTERNAL_HUNT_2026-10-03.md` | `13e442892d27466f3ee3082509a47ac9706c7f3448aa079de798bec8cb1a1dfb` | K2 = §2 row + §3 "EXT-K2"; B1/B2 = §1 rows B1/B2 [V] |
| **Clock audit md / json** | `lab/governance/astra/packets/CLOCK_PROVENANCE_BECKER_ARCHIVE_2026-10-03.{md,json}` | `e7424a130e95b72d288d567ef75b00804672b29b15bd93889aafb0722fd84d80` / `dc54e3dae4bbeeffc0e1c792bd769a2d63daee02a974dbff03d04da8780eebc3` | CAVEAT; a byte-identical copy is in `…/becker_2026-10-03/clock/` [V] |
| **K1 freeze md / json** | `lab/governance/astra/packets/VARIANTS_EXT_K1_Q6000_LEGGING_RISK_AUDIT_FREEZE_2026-10-03.{md,json}` | `5c40fb9d03a924e40577a81f262231701e331c98922f60f6dc7ab65a2dbed6d3` / `be3e88336389bc62c40413785e6ffb4a572e1dbd006d7cf3dfbc962f8184efaa` | template + cited definitions [V] |
| K1 ACCEPT | `lab/governance/astra/packets/CONDUCTOR_ACCEPT_EXT_K1_FREEZE_2026-10-03.json` | `021290077cbbed277455145d2e56e1335f6ae331d56c2ad79d4d85b405559397` | ACCEPT 16:16:49 EDT; launch_ref main@761eaaed [V] |
| K1 packet dir MANIFEST | `lab/governance/astra/packets/EXT_K1_LEGGING_AUDIT/MANIFEST.sha256` | `5e8f79063f132fe2db97ad3ecff5fea463d429f167abed09c58398a87fcadf01` | all 9 lines OK (= ACCEPT `verified.manifest`) [V] |
| **K1 pin bundle (reused by sha)** | `EXT_K1_authentic_pins_2026-10-03.tgz` (+ `.part-00`, `.part-01`, `.PARTS.sha256`) | `0f8f529733bfd1ccb01b36f312cdc20865cc2811c04dcd3c812d50c67295db38` (25,008,407 B); parts `3fd70f7b…` / `1f8b2ac1…`; PARTS file `a92df01d…`; inner MANIFEST `a041561e130fb97eaa8d7bfab5dd6fa53963fa4fbdb13c00cd4f71089e0e3db5` | Verified: concat of parts = `0f8f5297`; inner MANIFEST 37/37 OK; on-box K1 SOURCE_PINS 38/38 unchanged [V] |
| **B1 dev tape** | `lab/astra-science/nfl_factorial_lab_20260921/inputs/events.jsonl.gz` | `cd300e664c2c5f2ff344c4b1eb17dd3f8e5f3326168b9dd8e3ade94a3a7382b4` | 681,732 trades + 364,988 quotes; 62 tickers / 31 events [V] |
| B1 markets map / manifest / cohort | `…/inputs/markets.json` / `…/inputs/manifest.json` / `…/inputs/week_membership.json` | `66cc07e9e9e1543b3fdcbcded30ff50af0abae87bb2aa3d5fcb3d0be7925632f` / `375ea6e2c9125a411d5444a88115213542d5b19c874d73a2bed0b9355fd6277d` / `a47d0e0dc5a64d79335bc5588f8aa5e1d937503d36ebcbaaf219965a68adf88c` | [V] |
| **B2 000 fills** | `…/results/q3300_d0.25_000_fills.jsonl.gz` | `9d56f5d3c599e092606be9f4a1ad41ae8baabff4921d3d722adf0b57ac944a3f` | 12,853 rows (K1 §2) [V] |
| B2 000 orders / summary | `…/results/q3300_d0.25_000_orders.jsonl.gz` / `…/results/q3300_d0.25_000.json` | `c390801b9a7cf6d182d2d097123ed944792980524a7975e6e59a904a530f4b1c` / `78b94ae5a846dfa81a1baec8fdc0b7992e479af1ddbc67908195f47500a7930a` | orders for audit only; summary used only for K1 R18's pair-hold median [V] |
| B2 decisions (pinned, not read) | `…/results/q3300_d0.25_000_decisions.jsonl.gz` | `e6db52374f834bba210d5c17836828ac3bf0dd54ca9feb5836ea71a611c61b71` | not an input |
| Replay code | `…/replay_v2.py` / `…/queue_policies.py` / `…/run_experiment.py` | `5aba1bf3…` / `641d0df3…` / `c1a0fd2d…` (full in K1 §2) | semantics only [V] |
| **NFL reserved holdout** | `…/RESERVED_HOLDOUT.json` | `74507e1a4371d69bc79ea2369f9bff030a74f51ee80c8072ba9c0f5345d377ca` | refusal list [V] |
| **KXMLBSPREAD holdout prereg** | `lab/governance/astra/packets/CONDUCTOR_ACCEPT_VARIANTS_HOLDOUT_PREREG_ADDENDUM_Q6S5_KXMLBSPREAD_UNTOUCHED_CAPTURE_2026-10-01.json` / `…/VARIANTS_HOLDOUT_PREREG_ADDENDUM_Q6S5_KXMLBSPREAD_UNTOUCHED_CAPTURE_2026-10-01.md` | `9a987a77e6cd6293ddaeb14fadbf33a25c1a6cc392af25f46eaaaaae33ebb273` / `370dc31df17191446013b6cebb52d44ee8346f47d2f5b543a1c73049ba52c063` | refusal; ADMIT-1 window defined in 370dc31d §3.4 [V] |
| ADMIT-1 ruling | `lab/governance/astra/packets/CONDUCTOR_RULING_ADMIT1_OUTAGE_GAP_WEATHER_CARD03_RELAUNCH_2026-09-29.json` | `ac7cfe63623ca342ab5b4285ff58382a8138b58fb6cd8e95310a5d30d90304f2` | [V] |
| Fee CACHE | `lab/governance/astra/packets/scout_house_fee_2026-09-24/raw/docs/{kalshi_fee_schedule.txt, docs_fee_rounding.txt, nonstandard_fee_series.json}` | `d9435b8b7e30fecbe1a07539990667b23b828a8175962c0882d6c7bce93980ec` / `7591cf0fb277eaf8fac8aedaf1645e58b61dacb22b5fed20ba7d8ea9f76ffa22` / `558a4fa75516cc68b31568ca83aeb15e1b5f301c2696b32647315668e464c5be` | maker 0.0175, taker 0.07; KXNFLGAME M=1/1 "effective July 7, 2026"; non-direct $0.01 / direct $0.0001; per-order accumulator [V cache] |
| **Price-band registry 0860cbe2** | `lab/governance/astra/packets/r3_p3_fl_maker_taker/bands_registry_10c.json` | `0860cbe28d28ecc6142ddf6f1ebb67792084264ed82e0b4d868c3b3138ea5312` | 10 bands of 0.10 on `yes_price_dollars_0_to_1`, `[lo,hi)`, last band `[0.90-1.00]`; registered 2026-09-22 20:12:45 EDT "before outcome join" [V]. Used **verbatim**; never rebinned |
| nflverse games.csv | `lab/governance/astra/packets/scout_external_hunt_2026-10-03/raw/nflverse_nfldata_games.csv` | `683673b5f33c46c1c0fbe6535964b245ceea6984e144bf4b52bd8afaeec91cd6` | used **only** to verify the week formula (schedule columns `season, game_type, week, gameday, away_team, home_team`); no runner reads it; no moneyline or score column read; no ex-post anchor used in K2 |
| **Becker t0 trades** | `lab/astra-capture/external/becker_2026-10-03/data/becker_kalshi_trades_t0_KXNFLGAME_part000.parquet` | `a1e1027e8fd1e5bda30c3a4124e990048d5a7700cf2b08df24c1fbc5a0054e99` | 262,380,071 B; **8,297,967 rows; 484 tickers**; schema `trade_id: string, ticker: string, count: int64, yes_price: int64, no_price: int64, taker_side: string, created_time: timestamp[ns, tz=UTC], _fetched_at: timestamp[ns]`; BOX-ONLY [V] |
| Becker t0 markets | `…/data/becker_kalshi_markets_t0_KXNFLGAME_part000.parquet` | `7238e85874f3e231a9719aaa66847bd166c51c746f92f2e2ccc737ed96e439dd` | 110,313 B; 486 rows / 486 tickers; 20 columns (`ticker, event_ticker, market_type, title, yes_sub_title, no_sub_title, status, yes_bid, yes_ask, no_bid, no_ask, last_price, volume, volume_24h, open_interest, result, created_time, open_time, close_time, _fetched_at`); BOX-ONLY [V] |
| Becker t1–t4 (pinned, **refused** by part (b)) | `…/data/becker_kalshi_{trades,markets}_t{1..4}_*.parquet` | trades `8aded261…` `0c91d375…` `80413fcf…` `736915ea…`; markets `13805498…` `f1f3a918…` `aebec3d1…` `b1e13d89…` (full shas, rows, schemas in the box-only manifest) | match ADMISSION + Clock [V]; never read by K2 |
| Becker provenance | `…/becker_2026-10-03/ADMISSION_NOTE_BECKER_2026-10-03.{md,json}`; `license/{LICENSE,README.md,SCHEMAS.md,main_commit.txt}` | `b0763e60…` / `6ec7dc54…`; LICENSE `a69ab694…`, README `b60f3f35…`, SCHEMAS `5e2746fe…`, main_commit.txt `cd37a571…` (content: Becker repo commit `5690e332…`) | [V]; data licence [U] |
| **Becker exclusion list (box-only)** | `lab/astra-capture/external/ext_k2_becker_boxonly_2026-10-03/BECKER_EXCLUSION_LIST_KXNFLGAME.json` | **`61a4c993fbea5940e5999177ffb5a0e3161219a8f84812af2d2f44d9f556641b`** | canonical JSON; 56 open + 8 no-result tickers → 33 events / 64 tickers [V] |
| **Becker box-only pin manifest** | `lab/astra-capture/external/ext_k2_becker_boxonly_2026-10-03/BECKER_BOXONLY_PIN_MANIFEST.json` | **`fd5e10531f488f30baf05e2dd6f17c8f8823603ecbae457170dbbde66126fb95`** | 38 items (paths, shas, bytes, schema, row counts, role, `read_by_part_b_runner`, `cloud_allowed`); **never bundled** |
| Becker structural script / outputs (box-only) | `…/ext_k2_becker_boxonly_2026-10-03/{k2_becker_structural.py, BECKER_STRUCTURAL_BOXONLY.json, BECKER_STRUCTURAL_AGG.json}` | `6f5af9071dd72dc398b0180b779a78da3cb2bfbb88a75217d9c6e65e3fb58819` / `79be0f4e42e913c341b9186a9b7ee2e02bbb9c4d95d97368176b682e2e5e15ab` / `ea354f2f4cf75a1a395fed7044c3a05ba0644a93852eb51adce16d8a5f226ef4` | AGG = counts only (copied to the packet dir); BOXONLY carries identifiers |
| RULE-FROZEN-EDIT-PREV-BYTES-001 | `lab/governance/astra/registry/RULE_FROZEN_EDIT_PREV_BYTES_2026-09-24.md` | `f0aab7d15ca78a097644008db02013eae3a56cb81b2a6aef2cfe6faf21e3e6d1` | [V] |

The machine-readable lists are `packets/EXT_K2_OPTIMISM_TAX/SOURCE_PINS.json` for the cloud/part (a) inputs (K1 bundle by sha, plus the K2 delta bundle) and the box-only manifest above for part (b).

### 2.1 B1 and B2, exactly (commission: "define them exactly")
- **B1** := the dev tape `events.jsonl.gz` `cd300e66…` together with `markets.json` `66cc07e9…` and `manifest.json` `375ea6e2…` (Scout §1 row B1, path `lab/astra-science/nfl_factorial_lab_20260921/inputs/`). K2 uses B1 **trade rows** `{at, ticker, taker_side, yes_price, size, trade_id}` for regime definition, and B1 **quote rows** `{at, asof, ticker, bid, ask}` only for markouts, per K1 R19.
- **B2** := the 000 ledgers of the **q3300_d0.25_000 arm only**: fills `9d56f5d3…` (input), orders `c390801b…` (audit), summary `78b94ae5…` (K1 R18 median only). The decisions ledger `e6db5237…` is pinned and not read. **UNPINNED** (Scout row B2 says "+ q10000 / d5 arms"). Resolution: those arms are excluded. They are not the incumbent and the commission names "000"; their files are pinned as `pinned_not_used` in SOURCE_PINS.

## 3. Structural facts (label-free; counts only; re-derived this session)

Scripts: `packets/EXT_K2_OPTIMISM_TAX/structural_verify_devtape.py` (`cf7112e4…`) → `STRUCTURAL_VERIFY_DEVTAPE.json` (`a687a883…`), and box-only `…/ext_k2_becker_boxonly_2026-10-03/k2_becker_structural.py` (`6f5af907…`) → `BECKER_STRUCTURAL_AGG.json` (`ea354f2f…`, counts only). The Becker script hashed all **62** files in the Becker download dir before and after its run: **unchanged** [V].

### 3.1 Dev tape (B1)
| Fact | Value | Tag |
|---|---|---|
| Trade rows / quote rows | 681,732 / 364,988 (= K1) | [V] |
| Tickers / events | 62 / 31 | [V] |
| Taker-YES contract share | 0.9168821893496498 (K1: 0.916882) | [V] |
| Rows in ADMIT-1 window | 0 | [V] |

### 3.2 Becker KXNFLGAME (t0)
| Fact | Value | Tag |
|---|---|---|
| Trade rows / traded tickers / traded events | **8,297,967 / 484 / 243** (241 events with 2 tickers, 2 with 1) | [V] |
| Market rows | 486; 2 markets have no trades, both with volume < 100 (0 markets with volume ≥ 100 lack trades) | [V] |
| `status` at the 2025-11-23 market snapshot | active 58 (56 of them traded) / finalized 428 | [V] |
| **Open at trade fetch** (`close_time` > ticker's max `_fetched_at` read as UTC; Clock definition) | **56 tickers** (expected 56 ✓), 530,529 rows; close_time 2025-12-07T18:00Z → 2025-12-16T01:15Z | [V] |
| No yes/no `result` (read only as boolean `result IN ('yes','no')`) | 56 open (all of them) + **8 closed** (175,020 rows) | [V] |
| **Excluded** (ticker-level union = event-level closure) | **64 tickers / 33 events / 705,549 rows** | [V] |
| **Eligible** | **420 tickers / 210 events / 7,592,418 rows** | [V] |
| Week formula vs nflverse 2025 REG schedule | 272/272 schedule rows agree; 192/192 Becker REG events have a unique (date, team-set) nflverse match with the same week (alias JAC→JAX, LAR→LA) | [V] |
| Weeks present | PRE (49 events, 46 eligible); W01–W13. W13 has 16 events, **0 eligible** (all open); W12 has 14 events, **1 eligible**; W04 has 16 events, 15 eligible (1 no-result); W01–W11 otherwise complete | [V] |
| **Eligible REG weeks** | W01–W12 (12 weeks); "complete" (≥ 8 eligible events, R34): **W01–W11 (11 weeks)** | [V] |
| 2 non-PRE unmatched events | both single-ticker W13 events (open → excluded anyway) | [V] |
| **trade_id overlap with dev tape** (681,732 dev trade_ids vs all 5 Becker trade files) | **0 / 0 / 0 / 0 / 0** | [V] |
| Ticker overlap with dev tape; t0 tickers or events in RESERVED_HOLDOUT `74507e1a` | 0; 0 | [V] |
| Becker trade rows in the ADMIT-1 window (all 5 tiers) | 0 | [V] |

Selection-bias statement (binding, R43): Becker fetched trades **only for markets with snapshot volume ≥ 100** (Clock (c), [V code / I data]). Thin markets are therefore missing by design across every tier. Any population statistic describes liquid markets and over-weights high-attention games relative to all listed markets [I]. For t0 the effect is small in count (2 of 486 markets have no trades, both under 100 volume [V]), but any cross-series generalization inherits the bias. Closed-market trade sums also fall slightly short of `volume` (Clock (d); t0: 190/428 exact, median relative shortfall 7.13e-05 [V Clock]).

## 4. Part (a) tercile fixture (label-free; flow only; no fills joined)

`packets/EXT_K2_OPTIMISM_TAX/TERCILE_FIXTURE.json` (`4acbb826…`) and `TERCILE_BUCKETS.json` (`9acb5288…`, the per ticker-hour table with 10,089 rows). Both are built from B1 trade rows only. No quote, fill, ledger, score or settlement byte is read.

| Unit | n | Cut method | c1 / c2 | Per tercile |
|---|---|---|---|---|
| **PRIMARY ticker-hour** (eligible n_trades ≥ 5) | 9,277 eligible of 10,089 buckets | type-7 linear quantiles at 1/3, 2/3 of the unweighted eligible bucket shares | **0.9271702456462422 / 0.989881659505818** | T1 3,093 · T2 3,092 · T3 3,092 · UNCLASSIFIED 812 buckets; 21.70% of eligible buckets have share = 1.0 (all in T3) |
| SECONDARY event (whole B1 tape) | 31 | same | 0.9126590461375717 / 0.9359888338062846 | 11 / 10 / 10 events |
| SENSITIVITY trailing 60 min (causal) | per opening portion at run time | primary c1/c2, not re-estimated | — | computed at run time |

Share = `math.fsum(size | taker_side=yes) / math.fsum(size)` in IEEE double. Naive summation changes c1 in the 16th digit [V]; hence the fsum pin.

## 5. Rules (every degree of freedom pinned; UNPINNED = ambiguity resolved conservatively before implementation)

Conservative criterion for every UNPINNED resolution, adopted from K1 §5 and extended for K2:
- (i) use only pinned bytes;
- (ii) never invent a value or impute a null;
- (iii) never choose by looking at outcomes, markouts, surplus or any Becker price or side statistic;
- (iv) give the less favorable or less dramatic reading for any claim about 000's dependence;
- (v) add no number without a stated label-free rationale;
- (vi) for K2: when in doubt, keep Becker bytes further from git, clouds and gates.

### 5.A Global rules
| # | Rule | Source / resolution | Tag |
|---|---|---|---|
| R01 | **Two parts, two pipelines.** Part (a) `dev_pipeline` covers B1/B2 (dev-grade). Part (b) `becker_pipeline` covers Becker t0 (an [A] prior). Neither package imports the other. Shared code is limited to `shared/` pure functions with no data access: fee arithmetic, the band-registry loader, the week formula, canonical JSON and the provenance container. | commission + Clock | [V] |
| R02 | **Closed manifests, fail-closed.** Part (a) reads only files in `SOURCE_PINS.json` → `cloud_part_a_inputs` (K1 bundle `0f8f5297` by sha, plus K2 delta bundle `963f7663`). Part (b) reads only items with `read_by_part_b_runner=true` in the box-only manifest `fd5e1053`. Every sha256 is checked before reading. A mismatch is a hard fail, and no gap is filled. | house (K1 R02) | [V] |
| R03 | **000 is read, never re-run or retuned** (K1 R03 applies in full). No 000 parameter, policy or code changes, and `nfl_factorial_lab_20260921/` stays byte-unchanged. | ruling | [V] |
| **R04** | **EXECUTION SPLIT (licence consequence; binding).** **(1) Part (a) runs in ONE cloud**, from the K1 bundle `0f8f5297…` (reused by sha) plus the K2 delta bundle `963f7663…`. Neither bundle contains any Becker byte or any Becker-derived data file [V: `becker_bytes_in_bundle: 0`]. **(2) Part (b) code** (`becker_pipeline/`) is written and unit-tested by that same cloud on **synthetic fixtures only**. The cloud never receives, fetches or sees a Becker row. **(3) Part (b) execution is BOX-ONLY.** After merge, the Simulator runs the **merged commit's** `becker_pipeline` runner on the box. It reads Becker read-only from `lab/astra-capture/external/becker_2026-10-03/data/` and writes to the box-only dir `lab/astra-capture/external/ext_k2_becker_boxonly_2026-10-03/run_<utc>/`. Before the runner reads any Becker price, side or result, a **pre-run receipt** must record: the commit sha, the runner file sha256, the box-only manifest sha `fd5e1053…`, the exclusion list sha `61a4c993…`, and an all-files hash of the Becker dir. **(4) These never go into git, a PR, a gist, a cloud prompt, a cloud-attached bundle, Drive, any upload or any message:** raw Becker files; any row-level Becker-derived file; the ticker identifiers in the exclusion list; `BECKER_STRUCTURAL_BOXONLY.json`. **(5) The only things that may leave the box** are part (b) aggregate JSON/MD outputs that pass T11 (no row-level output) and the R41 small-cell suppression, carry the R45 attribution line, and have a Clock co-sign plus a Conductor OK (R45). | commission (licence [U]) + Clock §5 | [V]/[A] |
| R05 | **Becker-mix refusal (code).** Every loaded table is wrapped in a `Provenanced` container with `provenance` ∈ {`DEV_B1B2`, `BECKER_A`}. Any concat, merge, join, zip or comparison across provenances raises `BeckerMixRefused`; the only exception is R06. `dev_pipeline` refuses any path matching `becker` or `*.parquet`, and any sha in the box-only manifest (`BeckerMixRefused`). `becker_pipeline` refuses any path under `astra-science/` or `astra-capture/prospective/`, the K1 or K2 bundles, and any sha in SOURCE_PINS `cloud_part_a_inputs` (`BeckerMixRefused`). No Becker row ever enters a dev, holdout or ADMIT-1 table, and no such row ever enters a Becker table. | Clock unsafe use 2 | [V] |
| R06 | **Cross-check on trade_id only.** The single allowed cross-provenance operation is `trade_id_overlap_count(dev_ids, becker_ids) -> int`. It accepts only `trade_id` sets and returns only an integer. Any other key (ticker, price, count, side, time, or that tuple) raises `CrossCheckKeyRefused`. The expected value is **0** [V §3.2]. With zero overlap, no price, count or time agreement is computed (Clock: "not computable [U]"). | Clock §2 | [V] |
| R07 | **Holdout / ADMIT-1 refusal (code, both pipelines).** (a) Any row with a timestamp in `[2026-09-27T00:00:00Z, 2026-09-30T04:00:00Z)` (half-open) raises `Admit1WindowRejected`. (b) `HoldoutRefused` is raised for: any `RESERVED_HOLDOUT` (`74507e1a`) `holdout_games` event or game_id; any `measurement_development_events` event (`KXNFLGAME-26SEP21NYGLAR`, `KXNFLGAME-26SEP24ATLGB`); any `KXMLBSPREAD` ticker (prereg `9a987a77` / `370dc31d`). (c) The `capture.sqlite` and weather `archive.sqlite` paths are refused. No `sqlite3`, `urllib`, `requests`, `http`, `socket` or `subprocess` import is allowed (AST test). Expected counts are 0 in both pipelines [V §3]. | commission; K1 R34 | [V] |
| R08 | **Verdict domain {DESCRIPTIVE, ITERATE, INCONCLUSIVE} only.** No KEEP, no KILL of 000, no retune, no promotion. `counts_toward_keep=false`, `promote=false`, `feeds_gate=false`. The packet verdict is the part (a) verdict (R23). Part (b) carries its own label ∈ {DESCRIPTIVE, INCONCLUSIVE} (R44) and **can never move** the part (a) verdict or any gate. `results`/`pnl`/`roi` = null in this packet. | commission | — |
| R09 | **Tags on every output.** Part (a): `DEV_GRADE_REUSED_31_GAME_COHORT`, `HYPOTHETICAL_REPLAY_FILLS`, `IN_SAMPLE_DEV`. Part (b): `BECKER_EXTERNAL_PRIOR_A`, `TRADE_ONLY_NO_QUOTES`, `SELECTION_VOLUME_GE_100`, `ARCHIVE_ENDS_2025-11-25`, `LICENCE_U_NO_REDISTRIBUTION`, plus `BECKER_LABEL_DEPENDENT_DESCRIPTIVE_ONLY` on every MNO, MYES and taker-return field. Fee fields carry `CACHE_NOT_R1P1`. Becker fee-net fields also carry `FEE_SCHEDULE_2026_CACHE_APPLIED_TO_2025_TRADES_U` and `PER_TRADE_PROXY`. | ruling + Clock | — |

### 5.B Part (a): dev tape (B1/B2)
| # | Rule | Source / resolution | Tag |
|---|---|---|---|
| R10 | **Inputs** are B1 and B2 exactly as defined in §2.1. | commission ("define them exactly") | [V] |
| R11 | **Universe** = K1 R01: the 31 events in `week_membership.json` and their 62 tickers in `markets.json`. Anything else raises `ClosedUniverseRefused`. | K1 R01 | [V] |
| R12 | **Open legs and exposure** = K1 R04–R07 verbatim: event net inventory, FIFO opening portions (expected **6,161 portions, all maker**), open-leg close, UCH. K1's R36 structural gate runs first. Any failure stops the run: INCONCLUSIVE, no markout. | K1 R04–R07, R36 | [V] |
| R13 | **PRIMARY regime unit = ticker-hour**, i.e. (the fill's own `ticker`, `floor(at/3600)` UTC). Share s = `fsum(size, taker_side=yes) / fsum(size)` over the B1 trade rows in that bucket. A bucket is **eligible iff n_trades ≥ 5**. **UNPINNED** (the commission asks "per game? per ticker-hour?"). Resolution: ticker-hour is primary because (i) 000 fills a resting NO on the ticker whose YES-takers print [V `replay_v2.py:218`], so the fill's own ticker carries the relevant flow; (ii) it captures within-game variation, whereas a per-game unit confounds regime with game identity and leaves only 10–11 games per tercile; (iii) the K1 bootstrap still clusters by game. Five trades is the smallest count at which a single print cannot set the share by itself. The threshold is label-free and was fixed before any fill was joined. Disclosure: the author saw the label-free share quantiles at thresholds 1, 5, 10 and 20 before pinning (§6). | UNPINNED → resolved | [A] |
| R14 | **Tercile cut method.** c1 and c2 are the type-7 (linear-interpolation) quantiles at 1/3 and 2/3 of the **unweighted** list of eligible bucket shares over the whole B1 tape, one observation per bucket. Assignment: **T1_LOW** if s ≤ c1; **T2_MID** if c1 < s ≤ c2; **T3_HIGH** if s > c2; ineligible buckets are **UNCLASSIFIED**. Pinned values: c1 = `0.9271702456462422`, c2 = `0.989881659505818`. The bucket table sha is `9acb5288…`. The implementer must reproduce both cuts within 1e-12 and reproduce the bucket→tercile table byte-identically (T03). **UNPINNED** (quantile type, weighting, ties). Resolution: unweighted, so each tercile is a share of market-hours, not of volume. Ties go to the **lower** tercile. A share of 1.0 sits above c2, so T3 is never empty [V]. The cuts are computed once on the full tape, not per game; this is in-sample, which fits the descriptive purpose. | UNPINNED → resolved | [V]/[A] |
| R15 | **Assigning an opening portion.** A portion takes the regime of the (ticker, floor(fill.at/3600)) bucket of its opening fill. That bucket includes trades that print after the fill within the same clock hour, and it includes the YES print that triggered the fill. The label is therefore **contemporaneous, not a causal signal** [I]. There is also a mechanical link [I]: more YES-taker prints produce more 000 NO fills, so T3 holds more fills by construction. Contract-hours and fill counts per tercile are descriptive only and are not evidence of anything. | — | [I] |
| R16 | **SECONDARY unit = event.** The event share is computed over both tickers' B1 trades for the whole tape. Cuts are e1 = `0.9126590461375717` and e2 = `0.9359888338062846` (type-7 over 31 events), giving 11/10/10 events. Every portion of an event takes the event's tercile. Reported, never selected. | commission alternative | [V] |
| R17 | **SENSITIVITY (causal) = trailing 60 min.** The share is computed over the fill's own ticker's B1 trades with `at ∈ [t_fill − 3600, t_fill)`, i.e. strictly before the fill. The window is eligible iff it holds ≥ 5 trades, and it is classified with the **primary** c1/c2 (not re-estimated). Reported, never selected. **UNPINNED** (whether to add a causal variant). Resolution: add it as a sensitivity, so a reader can see whether the contemporaneous label is what drives the split. | UNPINNED → resolved | [A] |
| R18 | **Markouts** follow K1 R18–R22 unchanged. Horizons H = {60, 300, 1800, 3600} s plus CLOSE. **Primary H\* = 1800 s** (K1 R18). The mid is the quote-row mid under the `replay_v2.book_valid` validity rule (K1 R19). MO_h = mid_out(t_open+h) − p_entry, in $/contract (K1 R20). Nulls and censoring follow K1 R21. The CLOSE mark follows K1 R22 and is never summed into a PnL. **Reference mid at open = K1 R14** (ledger `outcome_mid_at_fill`). From it, K2 adds the **secondary, descriptive** mid-anchored markout MO_h^mid = mid_out(t_open+h) − m_open, which strips out spread capture. **UNPINNED** (whether to add MO^mid). Resolution: secondary only, because the commission says "reference mid per R14". | K1 R14, R18–R22 | [V]/[I] |
| R19 | **No SETTLE markout in K2.** Part (a) reads no score, no settlement and no nflverse byte. **UNPINNED** (K1 had SETTLE as a secondary). Resolution: drop it, so that part (a) stays fully label-free and T01 is a strict invariance. | UNPINNED → resolved | [V] |
| R20 | **Fees on part (a).** Headline per K1 R24: per maker order, ceil to $0.01 of Σ ceil_6dp(0.0175·M·C·p(1−p)), M = 1, allocated pro rata. Sensitivity per K1 R25: the direct-member $0.0001 figure (= ledger fee/size), never the headline. Per K1 R26, taker flatten fees are not charged to open legs. Label `CACHE_NOT_R1P1`; `examiner_pin_account_class: null`. | ruling + K1 | [V cache]/[I] |
| R21 | **Per-tercile outputs** (for the primary, secondary and sensitivity units, plus UNCLASSIFIED): n opening portions; opening contracts and their share; the maker-NO share of opening contracts; distinct games contributing; UCH (K1 R07) and its share; and, for each h ∈ H ∪ {CLOSE}, the contract-weighted mean MO (gross and net), the unweighted median, n, censored n and censored contracts. The same set is produced for MO^mid, and all of it is also produced per game. Bucket-level counts per tercile (buckets, trades, contracts) come from the fixture. **No PnL, ROI, "edge", "would have earned" or Sharpe.** **UNPINNED** (the output set). Resolution as stated. | commission + K1 R20/R29 | — |
| R22 | **Primary contrast.** Δ\*_a = MO_1800(T3_HIGH) − MO_1800(T1_LOW) on the primary unit, contract-weighted, **gross**, with net reported beside it. Uncertainty comes from a **game-cluster bootstrap** over the 31 games: B = 10,000, `random.Random(20261003)`, percentile 95% CI (K1 R31). Resamples in which T1 or T3 is empty are dropped and counted. **UNPINNED** (contrast direction and inference). Resolution: T3 − T1, i.e. high-optimism minus low-optimism regime, matching the thesis; inference as in K1. | UNPINNED → resolved | [A] |
| R23 | **Part (a) verdict (Examiner-owned; proposal).** **INCONCLUSIVE** if any of these holds: the K1 R36 gate fails; the T03 fixture reproduction fails; UNCLASSIFIED exceeds 20% of opening contracts; censoring at H\* exceeds 20% of opening contracts in T1 or in T3; fewer than 5 games contribute opening portions to T1 or to T3; more than 5% of bootstrap resamples are dropped. Otherwise **ITERATE** if the 95% CI of Δ\*_a excludes 0, in either direction: flow-mix dependence of 000's open-leg markout is then visible on the dev cohort and warrants a separate freeze. Otherwise **DESCRIPTIVE**. **UNPINNED** (thresholds). Resolution: stated now, label-free, mirroring K1 R32. | UNPINNED → resolved | [A] |
| R24 | **Static attribution only.** The split shows how recorded fills and open legs sort by flow regime. It does not say how 000 would behave under a different flow mix, and it is not a gate. Any regime-conditional 000 variant needs a new Variants freeze and a Conductor ACCEPT. | K1 R30 analog | [I] |
| R25 | **Multiplicity.** Only Δ\*_a can move the verdict. Every other unit, horizon, MO^mid figure, net figure and per-game table, and all of part (b), is descriptive and is labelled as such. | — | — |

### 5.C Part (b): Becker 2025 KXNFLGAME (box-only; DESCRIPTIVE; [A])
| # | Rule | Source / resolution | Tag |
|---|---|---|---|
| R30 | **No replay, score, KEEP or promotion from Becker.** Part (b) never touches 000, never simulates any order and never outputs a strategy metric. Its outputs are population descriptives of 2025 prints. | Clock unsafe 1; ruling | [V] |
| R31 | **Inputs and tier refusal.** Only t0 trades `a1e1027e…` and t0 markets `7238e858…` are read. Any t1–t4 file raises `TierRefused`. This also keeps Becker's 2025 KXMLBSPREAD rows (in t3) out entirely, beyond what R07 requires. | conservative | [V] |
| R32 | **Exclusion (applies to every per-game, per-week and per-band metric).** A ticker is excluded if: its markets `close_time` > the ticker's max trade `_fetched_at` read as UTC (OPEN_AT_TRADE_FETCH; Clock definition; **56** tickers); or `result ∉ {yes, no}` (**8 closed tickers plus the 56 open ones**); or it has no markets row (0). Exclusion then **closes over events**: every ticker of an event that has any excluded ticker is excluded. The runner recomputes the list and requires canonical-JSON equality with the pinned `BECKER_EXCLUSION_LIST_KXNFLGAME.json` (sha **`61a4c993…`**): 64 tickers, 33 events and 705,549 rows excluded; **420 tickers / 210 events / 7,592,418 rows eligible** [V]. A mismatch means INCONCLUSIVE and no output. An excluded ticker reaching any metric raises `OpenTickerRefused`. **UNPINNED** (ticker level vs event level). Resolution: event level. Here it gives the same set as ticker level [V], so it costs nothing, but it stays binding. | commission + Clock unsafe 4 | [V] |
| R33 | **`close_time` is NOT end of trading.** `close_time` appears only inside the R32 exclusion recompute. It is never used to truncate, to window, to split pre/post, or to define a trading end. Every trade of an eligible ticker is included whatever its `created_time` vs `close_time`, including post-game prints, which land mostly in bands b00/b09 [I]. K2 has **no pre/in-game split**, because Becker carries no kickoff time and using the nflverse `gametime` would be a cross-dataset join. **UNPINNED** (whether to split pre/in-game). Resolution: no split; T13 enforces it. | Clock (e) / unsafe 5 | [V] |
| R34 | **Weeks (pinned a priori, not from data).** ticker_date = the `YYMMMDD` token of `event_ticker` (e.g. `25SEP28` → 2025-09-28). **week = floor((ticker_date − 2025-09-02)/7 d) + 1**: Tue–Mon ET weeks anchored on the Tuesday before the 2025 opener. ticker_date < 2025-09-02 goes to the **PRE** stratum. Verified [V]: the formula reproduces the nflverse week for 272/272 rows of the 2025 REG schedule, and 192/192 Becker REG events unique-match nflverse on (date, team set) with the same week. ticker_date is assumed to be the ET game date [A]: K1 §3.4 verified this for the 2026 tickers, and the 2025 nflverse gameday match is [V]. **REG** is the primary population, with eligible weeks W01–W12. A week enters a **dispersion** statistic only if it is **complete (≥ 8 eligible events)**, which gives **W01–W11** [V counts]. W12 (1 eligible event) is reported with a null CI. **PRE** is reported as its own stratum and never pooled with REG. **UNPINNED** (game week vs trade-time week; the completeness threshold). Resolution: game week (the week of the market's game), so that one game's flow is not split across weeks. The threshold of 8 is half a 16-game slate; it was set from structural counts only, with no outcome seen. | UNPINNED → resolved | [V]/[A] |
| R35 | **Price bands = registry `0860cbe2` verbatim.** Ten bands on `p = yes_price/100`: b00 `[0,0.10)` … b08 `[0.80,0.90)`, b09 `[0.90,1.00]`. Integer cents 1–99 map uniquely (b00 = 1–9¢, b09 = 90–99¢). A trade's band is the band of its yes_price, including for maker-NO rows (no NO-price re-banding). **No rebin, merge, split or alternative edges.** The registry bytes are read and sha-checked at run time (T14). | house rule ("never rebin 0860cbe2") | [V] |
| R36 | **Metric S, taker-YES skew (label-free).** S = Σ count[taker_side=yes] / Σ count over the eligible rows in a cell. Secondary: the trade-row share. | commission | [A] |
| R37 | **Metric MNO, maker-NO surplus (gross; LABEL-DEPENDENT).** Every Becker trade has a taker side, and the maker holds the opposite side [I from the schema text "Which side the taker bought"]. On rows with `taker_side=yes` the maker bought NO at `no_price`, and the per-contract excess is **e_NO = 1{result=no} − no_price/100**. MNO = Σ count·e_NO / Σ count. **MYES** covers rows with `taker_side=no`, where the maker bought YES: e_YES = 1{result=yes} − yes_price/100. The contrast is **MNO − MYES**. Taker mirrors: taker-YES excess = −e_NO on the same rows, and taker-NO excess = −e_YES. Units are $/contract (= probability points / 100). The Becker paper reports in pp; whether its exact definition matches this one is [I]/[U]. **Every MNO, MYES and taker-return value depends on the settlement `result`. Each is tagged `BECKER_LABEL_DEPENDENT_DESCRIPTIVE_ONLY` and never feeds a gate, threshold, parameter, regime cut, the part (a) verdict or any 000 decision (T15).** | commission | [A] |
| R38 | **Fees: per-trade proxy (Becker has trades, not orders).** For each eligible row with count C and p = yes_price/100 (exact Decimal): maker_fee_row = **ceil_to_$0.01(0.0175 · M · C · p(1−p))**, taker_fee_row = **ceil_to_$0.01(0.07 · M · C · p(1−p))**, with M = 1 for KXNFLGAME (cache). **Proxy statement:** each Becker trade row is treated as **one order for the maker and one order for the taker**. Under cent round-up, Σ ceil ≥ ceil Σ, so the proxy **overstates** fees whenever one order fills across several rows (multi-fill sweeps exist: t0 has 773,448 zero-gap pairs [V Clock]). It is therefore an **upper bound**, provided each row matches a single maker order. If one row aggregates several maker orders, maker fees are understated; row granularity is [U]. **Sensitivity 1 (direct member):** ceil to $0.0001 per row, never the headline. **Sensitivity 2 (taker sweep proxy):** rows sharing an identical (ticker, created_time ns, taker_side) are grouped as one taker order, with ceil-cent applied to the group sum; maker fees are unchanged. Labels: `CACHE_NOT_R1P1`, `PER_TRADE_PROXY`, **`FEE_SCHEDULE_2026_CACHE_APPLIED_TO_2025_TRADES_U`**. The fee schedule that actually applied in 2025 is [U]; the cached KXNFLGAME non-standard row is "effective July 7, 2026". Net figures therefore mean "as if the 2026 cached schedule applied". They are **not historical net**. **UNPINNED** (proxy granularity; sweep grouping key). Resolution as stated. | commission + ruling `fee_rounding` | [V cache]/[I]/[U] |
| R39 | **Net metrics.** MNO_net = Σ (C·e_NO − maker_fee_row) / Σ C over taker-YES rows. MYES_net is built the same way, and the taker-side nets use taker_fee_row. Gross is reported **first and is the headline**; net sits beside it. **UNPINNED; needs a co-sign.** The Clock lists "fee modelling" as an unsafe use, and the commission (16:36 ET, after the Clock's 16:35:27 verdict) orders net figures. Resolution: compute them, because they are a deterministic arithmetic deduction per print and involve no order, queue, fill or book reconstruction. Never present them as modelled execution costs. Record a Clock co-sign at ACCEPT. **If the ACCEPT excludes them, every net field is emitted null** (runner flag `NET_FEE_PROXY_ENABLED`, whose value comes from the ACCEPT). | UNPINNED → resolved | [A] |
| R40 | **Cells and stability statistics.** (1) **Per week** w (REG W01–W12; PRE separate): S_w, MNO_w (gross and net), MYES_w, (MNO−MYES)_w. 95% CI by **event-cluster bootstrap within the week** (resample that week's eligible events with replacement), B = 2,000, seed `20261003 + w`, percentile. (2) **Pooled REG**: the same metrics, with an event-cluster bootstrap over all eligible REG events, B = 10,000, seed 20261003. (3) **Per band** b00–b09 (pooled REG): event-cluster bootstrap over eligible REG events, B = 10,000, seed 20261003 + 100 + band index. (4) **Week × band**: point estimates and counts only, with no CI. (5) **Dispersion (pre-declared).** PRIMARY: D_week(X) = sample SD (ddof = 1) of X_w across the **11 complete weeks**, for X ∈ {S, MNO_gross, MNO_net, MNO−MYES gross}; D_band(X) = sample SD across bands with ≥ 20 contributing eligible REG events. SECONDARY: the range (max − min); the number of complete weeks whose 95% CI excludes the pooled REG point estimate; for MNO, the count of complete weeks with MNO_w > 0 and the count with a CI lower bound > 0; and Spearman ρ(week index, X_w) over complete weeks, as a drift descriptor. **No hypothesis test, no p-value gate and no threshold applies to any of these.** **UNPINNED** (B, seeds, dispersion choice, band-inclusion threshold). Resolution as stated. | commission | [A] |
| R41 | **Null handling.** An empty denominator gives null. The CI is null if a cell has fewer than 5 eligible events. **Small-cell suppression:** any committed cell with fewer than 20 trade rows or fewer than 2 events gets a null value and the flag `SUPPRESSED_SMALL_CELL`, with its counts kept. No imputation, no forward fill, no substitute data. The Clock's integrity invariants are re-asserted: yes_price ∈ 1..99, yes + no = 100, count > 0, taker_side ∈ {yes, no}, unique trade_id, no nulls in key fields. Any violation is a hard fail and the run is INCONCLUSIVE. | Clock §4 | [V] |
| R42 | **No row-level Becker output.** The part (b) writer emits only aggregate cells keyed by {stratum, week, band, metric, fee_variant}. Forbidden output keys: `trade_id, ticker, event_ticker, created_time, _fetched_at, count, yes_price, no_price, taker_side, result, close_time`. Every output string is scanned against the sets of Becker trade_ids and tickers; any hit raises `RowLevelOutputRefused` (T11). The exclusion-list identifiers stay in the box-only dir, and outputs carry only its sha and counts. | commission (licence) | [V] |
| R43 | **Selection-bias statement.** The §3.2 selection-bias text is printed verbatim in the header of every part (b) output, together with this coverage statement: KXNFLGAME 2025 preseason plus REG W01–W12 only (the archive ends 2025-11-25; no late season and no playoffs [V Clock]). | Clock (b)(c)(d) | [V] |
| R44 | **Part (b) label** ∈ {DESCRIPTIVE, INCONCLUSIVE}. INCONCLUSIVE if any of these holds: the exclusion list sha ≠ `61a4c993`; the §3.2 structural counts do not reproduce exactly; any input sha mismatches; the Becker dir hash changes; an R41 integrity check fails. Otherwise DESCRIPTIVE. The label can never be ITERATE, never moves Δ\*_a and never feeds a gate (`feeds_gate=false`). Part (b) is never holdout, OOS or confirmatory evidence. | commission + Clock | — |
| R45 | **Licence, attribution and what may be committed.** The data licence is [U]. Every part (b) output carries the line: "Derived aggregates from Jon Becker's prediction-market-analysis dataset (data licence unknown [U]); internal research use; not redistribution of the data." Aggregates may be committed only if T11 and R41 pass **and** the Clock co-signs **and** the Conductor approves. **UNPINNED** (whether aggregates count as redistribution under a [U] licence). Resolution: the default is **box-only**. Aggregates stay in `packets/EXT_K2_OPTIMISM_TAX/results_b/` on the box until the Conductor rules, and nothing is committed by default. | Clock §5 | [U]/[A] |
| R46 | **No quote, depth, fill or queue modelling on Becker (code).** Column allowlist. Trades: `trade_id` (dedupe assert and the R06 count only), `ticker`, `count`, `yes_price`, `no_price`, `taker_side`, `created_time` (integrity and the sweep key only), `_fetched_at` (R32 only). Markets: `ticker`, `event_ticker`, `status`, `result`, `close_time` (R32 only), `_fetched_at`, `volume` (the R43 statement only). Reading `yes_bid, yes_ask, no_bid, no_ask, last_price, open_interest` or `volume_24h` raises `BeckerQuoteFieldRefused`. AST test: `becker_pipeline` defines or calls nothing whose name contains fill, queue, depth, book, quote, replay or simulate. | Clock unsafe 3 | [V] |
| R47 | **Frozen script for part (b).** The runner is the merged commit's `becker_pipeline/run_part_b.py`. Its sha256 is written into the pre-run receipt (R04(3)) before any Becker price, side or result is read. Any edit after that point is a new freeze. The Simulator may not change code, parameters or seeds on the box. | commission | — |

### 5.D House rules
| # | Rule | Tag |
|---|---|---|
| R48 | Lee-Ready is refused. No tick rule and no print-derived mids: B1 `taker_side` and Becker `taker_side` are native fields. Registry `0860cbe2` is never rebinned. No network GET and no new data pull (no new nflverse, no Becker re-extract, no Kalshi). | [V] |
| R49 | Precision and canonical JSON follow K1 R37: $/contract to 6 dp, shares to 6 dp, contract-hours to 4 dp; `sort_keys`, `separators=(',',':')`, UTF-8. Times are stored in UTC with an ET rendering. | — |
| R50 | **Label hygiene during implementation.** The cloud never sees Becker data. Before the part (b) run, the Simulator may look only at the pre-run receipt and the T07/T11 outputs. Results are opened only after the receipt sha has been logged. | — |

**UNPINNED rules (17), each resolved above:** R04-sub (the cloud writes part (b) code on synthetic fixtures only), §2.1/R10 (the B2 arms q10000/d5 are excluded), R13 (primary unit + eligibility of 5), R14 (quantile type, weighting, ties), R17 (causal sensitivity), R18 (MO^mid as secondary), R19 (SETTLE dropped), R21 (per-tercile output set), R22 (contrast direction + inference), R23 (verdict thresholds), R32 (event-level exclusion), R33 (no pre/in-game split), R34 (game week + completeness threshold of 8), R38 (per-trade proxy + sweep key), **R39 (net fee vs the Clock's "fee modelling": co-sign needed)**, R40 (B, seeds, dispersion, band threshold), **R45 (aggregate commit; default box-only)**.
**Key ones:** R13/R14 (unit and cuts), R39 (net-fee co-sign), R45 (aggregate commit), R38 (fee proxy), R34 (week basis).
Non-rule UNPINNED items: cloud base main and the K1 merge dependency (§9.1); provenance of the 16:36 commission text (§0.3).
**BLOCKERS: none for freezing.** Two items need a co-sign at ACCEPT: R39 and R45.

## 6. Lookahead / label-exposure declaration

- **What the author saw before freezing:**
  - **Briefs and packets.** The Scout brief, including 000's reported net and the dev flow shares. The Clock packet, including its named no-result example `KXNFLGAME-25SEP28GBDAL-*` and all its counts. The K1 freeze and packet.
  - **Becker.** Schemas; row, ticker and event counts; the status histogram; open-at-fetch counts; the **boolean** count of markets with result ∈ {yes, no} (56 open + 8 closed without one); per-week event, ticker and row counts; and the trade_id and ticker overlap counts. **The yes/no split of `result` was never computed or printed.** No Becker price distribution, taker-side share, MNO/MYES or fee total was computed.
  - **Dev tape.** Taker-YES share quantiles per ticker-hour at thresholds 1/5/10/20, all shown together, and the event-level shares. Both are label-free flow only, and both were seen before R13/R14 were pinned.
  - **Not done.** No 000 fill was joined to any regime. No markout, UCH-by-tercile or fill-count-by-tercile was computed.
- **Exposure disclosure.** (1) Identifying the no-result markets told the author which Becker 2025 games did not resolve yes/no: 4 events, namely 3 PRE plus `25SEP28GBDAL`, which the Clock had already named. This was needed for the commissioned exclusion. (2) The dev-tape flow distribution was seen before the R13 threshold was pinned. It is label-free and outcome-free, but it was a design-time look, so it is disclosed.
- **Label-free part (a).** Tercile assignment is a function of B1 trade rows `(ticker, at, taker_side, size)` and nothing else. Permuting any label (a synthetic `result`, nflverse scores, settlement), any quote row, or any 000 fill or markout must leave the cuts and assignments byte-identical (T01).
- **Part (b) is label-dependent by design** (R37). It never crosses into part (a), any gate or any verdict.

## 7. Verdict mapping and scope

- **Verdicts.** The packet verdict is the part (a) verdict ∈ {DESCRIPTIVE, ITERATE, INCONCLUSIVE} (R23). The part (b) label ∈ {DESCRIPTIVE, INCONCLUSIVE} (R44) is attached as an [A] context block. **KEEP, KILL of 000, retune and promotion are all impossible.** `counts_toward_keep=false`, `promote=false`, `live_promotion=false`, `feeds_gate=false`.
- **Part (a) evidence.** Evidence class `IN_SAMPLE_DEV` / `HISTORICAL_REPLAY` on the reused 31-game cohort, so dev-grade (ruling `dev_grade`). family_size = 1 (Δ\*_a). Effective n = 31 games.
- **Part (b) evidence.** Evidence class `EXTERNAL_PRIOR_A` / `DESCRIPTIVE_POPULATION_2025`. n = 210 eligible events across the REG and PRE strata.
- **Untouched data.** The NFL `RESERVED_HOLDOUT` `74507e1a…`, the KXMLBSPREAD prereg `9a987a77…` / `370dc31d…` and the ADMIT-1 window stay untouched and are refused in code (R07).

## 8. Required tests (named; all green before the PR leaves draft; the box-mode part (b) tests run as part of the pre-run receipt)

- **T01 Label-permutation invariance (part (a) terciles).**
  - (a) Fixture of 2 synthetic games with their labels swapped: the canonical bytes and sha of `tercile_cuts.json`, `bucket_terciles.json` and `portion_terciles.json` (primary, secondary, sensitivity) must not change.
  - (b) Pinned data: apply 1,000 permutations (`random.Random(20261003)`) of a synthetic per-game `result` vector attached to markets, plus a shift-by-1 derangement, plus a permutation of every quote row's (bid, ask) across rows, plus a shuffle of fill `outcome_mid_at_fill`. All three shas stay constant and the cuts equal the §4 values.
  - The tercile function accepts only `(ticker, at, taker_side, size)` iterables. Passing a quote, fill, score or result argument raises `LabelInputRefused`. The test prints shas only.
- **T02 Causality of the R17 sensitivity.** For 200 seeded opening portions, deleting every B1 trade with `at ≥ t_fill` leaves the trailing-60 regime unchanged.
- **T03 Tercile fixture reproduction.** c1, c2, e1 and e2 within 1e-12 of §4. Bucket table sha `9acb5288…`, byte-identical. Tercile bucket counts 3,093 / 3,092 / 3,092 / 812. Event counts 11 / 10 / 10.
- **T04 Structural reproduction.**
  - The K1 R36 gate: maker NO share 0.989706; UCH 603,262.7291176913; 6,161 portions; counts.
  - K2 §3.1: taker-YES share 0.9168821893496498 within 1e-12; counts 681,732 / 364,988 / 62 / 31.
  - If the K1 lab has been merged, K2 imports it read-only and asserts equality.
- **T05 Becker-mix refusal.**
  - On synthetic `BECKER_A` and `DEV_B1B2` tables, concat, merge, join and compare each raise `BeckerMixRefused`.
  - `dev_pipeline` given a `*.parquet` path or a Becker sha from the manifest raises `BeckerMixRefused`.
  - `becker_pipeline` given `events.jsonl.gz` or a K1/K2 bundle path raises `BeckerMixRefused`.
  - Import-graph test: neither package imports the other.
- **T06 Cross-check key.** `trade_id_overlap_count` returns an int. A join on ticker, price, count, side, time or the full tuple raises `CrossCheckKeyRefused`. In the box run, the count equals 0.
- **T07 Open-ticker / no-result exclusion.**
  - Synthetic: a market with close_time > tfetch, one with result "" and one with result "void" are each excluded, and a sibling ticker of an excluded one is excluded at event level.
  - Box-only: the recomputed list equals the pinned file byte-for-byte (sha `61a4c993…`). Excluded counts: 56 open / 8 closed no-result / 64 tickers / 33 events / 705,549 rows. Eligible: 420 tickers / 210 events / 7,592,418 rows.
  - Injecting an excluded ticker into a week cell raises `OpenTickerRefused`.
- **T08 Holdout / ADMIT-1 refusal (both pipelines).**
  - `2026-09-27T00:00:00Z` is rejected; `2026-09-30T03:59:59.999Z` is rejected; `2026-09-30T04:00:00Z` is accepted.
  - `KXNFLGAME-26SEP28PHICHI`, `2026_03_PHI_CHI`, `KXNFLGAME-26SEP21NYGLAR`, `KXNFLGAME-26SEP24ATLGB` and any `KXMLBSPREAD-…` ticker each raise `HoldoutRefused`.
  - The `capture.sqlite` and weather `archive.sqlite` paths are refused.
  - AST check: no `sqlite3`, `urllib`, `requests`, `http`, `socket` or `subprocess` import.
- **T09 Fee units (Decimal).**
  - Part (a): the K1 T05 vectors, verbatim.
  - Part (b) per-trade proxy. Each vector reads (coef, C, yes¢) → model fee → $0.01 headline / $0.0001 sensitivity.
    - Maker: (0.0175, 1, 50) 0.004375 → **0.01** / 0.0044; (0.0175, 100, 50) 0.4375 → 0.44 / 0.4375; (0.0175, 10, 97) 0.0050925 → 0.01 / 0.0051; (0.0175, 250, 37) 1.0198125 → 1.02 / 1.0199; (0.0175, 1, 1) 0.00017325 → 0.01 / 0.0002.
    - Taker: (0.07, 1, 50) 0.0175 → **0.02** / 0.0175; (0.07, 100, 50) 1.75 → 1.75 / 1.7500; (0.07, 10, 97) 0.02037 → 0.03 / 0.0204; (0.07, 1, 97) 0.002037 → 0.01 / 0.0021; (0.07, 250, 37) 4.07925 → 4.08 / 4.0793; (0.07, 1000, 99) 0.693 → 0.70 / 0.6930.
  - Sweep sensitivity: two taker rows of 2 @ 37¢ cost 0.04 + 0.04 = **0.08** per row, vs **0.07** grouped as 4 @ 37¢ (ceil of 0.065268).
  - Symmetry: fee(p) = fee(1−p). M = 1 is read from the cache table.
  - Every fee field carries `CACHE_NOT_R1P1`. The headline is never the $0.0001 figure. `examiner_pin_account_class` is null. With `NET_FEE_PROXY_ENABLED=false`, every net field is null.
- **T10 Manifest tamper.** A one-byte tamper causes a hard fail before any read when applied to any of: a vendored pin; `SOURCE_PINS.json`; the K2 bundle MANIFEST; a K1 bundle part; `BECKER_BOXONLY_PIN_MANIFEST.json`; a file listed in the box-only manifest (tested on a temp copy). A wrong exclusion-list sha makes the run INCONCLUSIVE with no output.
- **T11 No row-level Becker output.**
  - Synthetic: run the part (b) writer on a Becker-shaped fixture. No forbidden key appears, no output string equals any fixture trade_id or ticker, and cells below 20 rows or 2 events come out null with `SUPPRESSED_SMALL_CELL`.
  - Box run: scan every output file against the full Becker t0 trade_id and ticker sets; 0 hits required.
  - Repo test: the git tree contains no `*.parquet`, no `becker_kalshi_*` path, and no file whose sha is in the box-only manifest.
- **T12 No quote / depth / fill / queue on Becker.** Reading any refused markets column raises `BeckerQuoteFieldRefused`. The AST name scan of `becker_pipeline` is clean.
- **T13 close_time usage.** AST/grep check: `close_time` is referenced only in the R32 recompute function, and no window or truncation uses it.
- **T14 Tiers / weeks / bands.**
  - A t1–t4 path raises `TierRefused`.
  - Week fixtures: 2025-09-01 → PRE; 2025-09-02, 09-04 and 09-08 → W01; 09-09 → W02; 11-24 → W12; 11-25 → W13.
  - Band fixtures: 1¢ → b00, 9¢ → b00, 10¢ → b01, 89¢ → b08, 90¢ → b09, 99¢ → b09. The edges are read from the registry bytes (sha `0860cbe2…`), which stay unchanged. Any rebin, merge or custom edge list raises `RebinRefused`.
- **T15 No ROI / KEEP / gate framing.**
  - The committed `EMPTY_RESULTS.json` has `results`, `pnl` and `roi` = null.
  - No output key matching `/(^|_)(pnl|roi|keep|profit|sharpe)(_|$)/i` has a non-null value.
  - Verdict ∈ {DESCRIPTIVE, ITERATE, INCONCLUSIVE, null}; part (b) label ∈ {DESCRIPTIVE, INCONCLUSIVE, null}.
  - Passing a part (b) value into `dev_pipeline`, a verdict function or a threshold raises `LabelDependentToGateRefused`.
- **T16 000 untouched + Lee-Ready.** The shas of `replay_v2.py`, `queue_policies.py` and the q3300_d0.25_000 files equal the pins. The git diff of `nfl_factorial_lab_20260921/` is empty. Any Lee-Ready key or call is refused.
- **T17 Execution-split guard.** `run_part_b.py` refuses to start unless: the Becker dir exists on the local filesystem, the box-only manifest sha equals `fd5e1053…`, and a pre-run receipt has been written. In CI or the cloud, part (b) tests run on synthetic fixtures only, and the guard test asserts that the real runner refuses to start there.

Test command: `python3 -m unittest discover -s tests -v`, run from the lab dir (K1 convention).

## 9. Cloud / implementer section (execution split per R04)

1. **Cloud, repo and base.** **One** K2 cloud (the sole Variants cloud for K2), repo `17thgreen/GPT-6-Astra-Deathmatch`, **draft PR**, base = main. The last recorded ref is K1's ACCEPT launch_ref `main@761eaaedc153dca9807d7630adcea1ae3387d9c1` [V file]; it has not been network-verified. **UNPINNED** (main may have moved; the K1 PR may or may not be merged). Resolution:
   - The cloud records the actual HEAD. It proceeds only if `nfl_factorial_lab_20260921/` is byte-identical to the pins (T16).
   - If the K1 lab is on main, the cloud imports K1's lot, markout and fee modules **read-only** and asserts T04 equality.
   - If it is not, the cloud implements the cited K1 rules inside the K2 lab and runs K1's R36 gate.
   - The cloud never edits K1's lab.
   - Whether the K2 cloud may run concurrently with K1's cloud is a Conductor call at ACCEPT. The default is sequential.
2. **Lab layout.** Lab dir `kalshi_ext_k2_optimism_tax_lab_20261003/` with: `shared/` (fees, bands, weeks, canonical JSON, provenance container); `dev_pipeline/` (pins, terciles, lots, markouts, orchestrator); `becker_pipeline/` (pins, exclusion, metrics, bootstrap, writer, `run_part_b.py`); `tests/`; `pins/`; `results_a/`; `EXPERIMENT_SPEC.md`; `README.md`; `FROZEN_EXPERIMENT.json`; an Examiner HOLD_PRE_PR file; and one registry row.
3. **Vendoring.** Vendor the K1 bundle `0f8f5297…` (its parts) and the K2 delta bundle `963f7663…` verbatim under `pins/`, and check each against its MANIFEST. `*.jsonl.gz` is git-ignored, so vendor the B1/B2 gz files from the bundle only (force-add under `pins/`, as in K1). **Never vendor, fetch or synthesize anything from real Becker bytes.** Part (b) tests use hand-written synthetic fixtures labelled `SYNTHETIC_NOT_BECKER`.
4. **Part (a) runs in the cloud.** The cloud runs `dev_pipeline` and commits `results_a/STRUCTURAL.json`, `results_a/TERCILES.json` (cuts, bucket counts), `results_a/MARKOUTS_BY_TERCILE.json` (aggregates per unit × tercile × horizon, and per game), `results_a/UCH_BY_TERCILE.json`, `results_a/EMPTY_RESULTS.json` and `results_a/UNIT_RESULTS.md`. **Not allowed:** PnL, ROI, Sharpe, "would have earned", KEEP/KILL language, or a per-fill dump of the real ledger.
5. **Part (b) runs on the box only.** The cloud commits **code and synthetic tests only**. After merge, the **Simulator on the box**:
   1. writes the pre-run receipt (R04(3));
   2. runs T07, T10, T11 and T17 in box mode;
   3. runs `run_part_b.py` from the merged commit, reading `lab/astra-capture/external/becker_2026-10-03/data/` read-only;
   4. writes outputs to `lab/astra-capture/external/ext_k2_becker_boxonly_2026-10-03/run_<utc>/`;
   5. copies only the T11-clean aggregate JSON/MD to `packets/EXT_K2_OPTIMISM_TAX/results_b/` on the box.

   Committing those aggregates follows R45 (default box-only). No cloud ever runs part (b).
6. **Prohibitions and seeds.** No `sqlite3`, no network imports, no `admit.py`, no orders. `capture.sqlite` and the weather `archive.sqlite` are never opened. All seeds are from the 20261003 family.
7. **Examiner and Adversary.** The Examiner pins the account class (R20 / K1 R25), scores part (a) within {DESCRIPTIVE, ITERATE, INCONCLUSIVE} and records the part (b) label within {DESCRIPTIVE, INCONCLUSIVE}. The Adversary reviews T01, T05 and T11 before the Examiner scores.

## 10. Integrity

- **Cloud bundles.**
  - Reused: `/workspace/EXT_K1_authentic_pins_2026-10-03.tgz`, sha256 `0f8f5297…` (25,008,407 B, 2 parts).
  - New K2 delta bundle: **`/workspace/EXT_K2_authentic_pins_2026-10-03.tgz`**, sha256 **`963f7663a74527db38479bbf4a253870bd5dc6f99c8f85b70750d3600c65907f`**, **288,078 B**, not split (< 25 MB). It holds 20 files: 18 inputs, an inner `MANIFEST.sha256` (`2e91d48f87e144031aa18fc4eb0f6d85953a7fa6c817bbfa4e5ba4af567931a3`) and `DEPENDS_ON.txt` (`371597f1…`, which names the K1 bundle).
  - The 18 inputs are: the K1 freeze md and json, the K1 ACCEPT, the K1 packet dir (9 files), K1's `.PARTS.sha256`, and K2's `structural_verify_devtape.py`, `STRUCTURAL_VERIFY_DEVTAPE.json`, `TERCILE_FIXTURE.json`, `TERCILE_BUCKETS.json`, `SOURCE_PINS.json` and `EMPTY_RESULTS.json`.
  - **Becker bytes in the bundle: 0.** Receipt: `packets/EXT_K2_OPTIMISM_TAX/BUNDLE_RECEIPT.json` (`fc708127…`).
- **Box-only Becker manifest.** `lab/astra-capture/external/ext_k2_becker_boxonly_2026-10-03/BECKER_BOXONLY_PIN_MANIFEST.json`, sha256 **`fd5e10531f488f30baf05e2dd6f17c8f8823603ecbae457170dbbde66126fb95`** (38 items). It is not bundled, and every Becker-derived item in it has `cloud_allowed=false`.
- **Packet folder `packets/EXT_K2_OPTIMISM_TAX/`.** Contents:
  - `FROZEN_EXPERIMENT.json`
  - `SOURCE_PINS.json` (`5133c826…`)
  - `STRUCTURAL_VERIFY_DEVTAPE.json` (`a687a883…`)
  - `structural_verify_devtape.py` (`cf7112e4…`)
  - `TERCILE_FIXTURE.json` (`4acbb826…`)
  - `TERCILE_BUCKETS.json` (`9acb5288…`)
  - `BECKER_STRUCTURAL_AGG.json` (`ea354f2f…`; counts only, no identifiers [V: 0 ticker strings])
  - `EMPTY_RESULTS.json` (`ab5ec779…`)
  - `BUNDLE_RECEIPT.json` (`fc708127…`)
  - `MANIFEST.sha256`

  JSON twin: `packets/VARIANTS_EXT_K2_OPTIMISM_TAX_DEPENDENCE_STRESS_FREEZE_2026-10-03.json`, which embeds this md's sha256.
- **New files only.** Under RULE-FROZEN-EDIT-PREV-BYTES-001, this freeze **creates only new files**. No frozen file was edited, so there was no `_prev` write. The Becker download dir was read only: 62 files were hashed before and after, and none changed [V].
- `results = null`, `pnl = null`, `roi = null`.

## 11. Data gaps / attention items (not blockers)

1. **Co-sign R39.** The Clock lists "fee modelling" as an unsafe use, but the commission orders net-of-fee figures. Net is an arithmetic per-print deduction, and it is emitted null if the ACCEPT excludes it.
2. **Co-sign R45.** Whether part (b) aggregates may be committed while the licence is [U]. The default is box-only.
3. **2025 fee schedule [U].** Net figures apply the 2026 cached schedule (KXNFLGAME M=1, "effective July 7, 2026") to 2025 prints. They are counterfactual-at-cache, not historical.
4. **Per-trade proxy granularity [U].** Unknown whether one Becker row can aggregate several maker orders (R38).
5. **Becker coverage.** W12 has 1 eligible event and W13 none, because both were open at the archive end. The late season and playoffs are absent. Complete weeks are W01–W11. Selection is volume ≥ 100 only.
6. **Contemporaneous regime label (R15).** The ticker-hour bucket includes post-fill prints and the triggering print, so T3 holds more 000 fills mechanically. The causal trailing-60 sensitivity is provided for this reason.
7. **Commission provenance.** The 16:36 ET message exists only in the relayed task text [U]. The Archivist should file it.
8. **Clock definition nuance.** The Clock md says "58 markets were `active` at the snapshot"; 2 of those have no trades. The commission's 56 are the traded tickers open at trade fetch. Both counts reproduce [V].
9. **Repo base / K1 merge state.** Not network-verified (§9.1).
10. **Clock limit (a) holds.** No cross-check is possible: 0 trade_id overlap and 0 ticker overlap [V].

## 12. Refuse binds

**Becker scope**
- replay, score, KEEP or promote from Becker
- mix Becker with dev, holdout or ADMIT-1 rows
- any cross-check key other than trade_id
- quote, depth, fill or queue modelling on Becker
- Becker quote/snapshot columns
- per-game metrics on open or no-result markets
- close_time as trading end
- t1–t4 tiers

**Data handling**
- Becker bytes in git, PR, gist, cloud, cloud bundle, Drive, upload or message
- row-level Becker output
- publishing exclusion identifiers

**Fees and labels**
- net fee as headline or as modelled cost
- direct-member fee as headline
- claiming CACHE as R1-P1
- MNO/MYES (label-dependent) into any gate, threshold or verdict

**000 and framing**
- re-run or retune 000
- KEEP or KILL 000
- ROI/PnL framing
- Lee-Ready, tick rule or print-derived mids
- rebinning registry `0860cbe2`

**Protected data and systems**
- holdout rows (NFL RESERVED_HOLDOUT `74507e1a`, KXMLBSPREAD prereg `9a987a77` / `370dc31d`)
- ADMIT-1 window data
- `capture.sqlite`
- weather `archive.sqlite`
- `admit.py`
- any Kalshi or network GET
- new data pulls

**Process**
- dual cloud for K2
- part (b) in any cloud
- moving any rule after a run
- editing any frozen byte
