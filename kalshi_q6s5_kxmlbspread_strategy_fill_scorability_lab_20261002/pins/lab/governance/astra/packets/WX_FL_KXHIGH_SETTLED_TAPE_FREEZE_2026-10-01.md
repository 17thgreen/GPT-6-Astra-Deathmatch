# WX-FL KXHIGH SETTLED-TAPE: FREEZE KERNEL (one knob `price_band`; out-of-domain replication of fb6540f5)

**File date:** `2026-10-01`. **Frozen / declared pre-outcome at:** `2026-10-01T19:46:31-04:00` (ET). **Design locked at:** `2026-10-01T19:41:14-04:00` (`DESIGN_LOCK_PRE_FEASIBILITY.txt` `4ff6bf2c…`). The lock was written before the snapshot was made and before any count was taken. No band ROI, maker return, settlement-joined number, or per-arm count has been computed by anyone for this packet. I read only schema, row counts, `status`, timestamps (`created_time`, `received_at`, `close_time`, `open_time`, `settlement_ts`), ticker strings, a 0/1 "result is non-empty" flag computed in SQL, and the collector `gaps`/`polls` tables. **I did not read or print any `result` value, `yes_price_dollars`, `no_price_dollars`, `count_fp`, side field, or ROI-relevant column.**
**Owner:** R&D Variants (freeze; implement only after Conductor ACCEPT) → Simulator → Examiner
**Status:** FROZEN, FREEZE_ONLY. Awaiting Conductor **ACCEPT + IMPLEMENT GO**. No cloud agent, no PR, no GET (Kalshi or NWS), no orders, no `admit.py` until then. Per ruling `0e37f91b…` the cloud also waits for `bc-468d4736`.
**Authority:** Conductor RULING `CONDUCTOR_RULING_VARIANTS_WX_FL_PREFREEZE` (`0e37f91b…`), decision **CLEARED_TO_FREEZE**. Rulings 1–4 and all five freeze_requirements are obeyed below. See "Ruling compliance" for the one item that needs a Conductor choice at ACCEPT.
**Freeze ID / experiment id / packet id:** `WX-FL-KXHIGH-SETTLED-TAPE`. This is its own packet ID (ruling 1). Data lineage is card02 `CARD02-STATION-WEATHER-NOWCAST`, read only through a pinned snapshot. The card02 packets and the live db are not modified, and card02 LEDGER logging belongs to the card02 owner.
**Feature family:** `settled_tape_price_band` (FL-band maker thesis), applied out of domain to **KXHIGHCHI / KXHIGHLAX / KXHIGHMIA / KXHIGHNY**.
**Repo / implement base:** `https://github.com/17thgreen/GPT-6-Astra-Deathmatch`, **main `749bc1464764fda03dcddd1162177ef062b2ece3`** (PR62 game-phase squash, per Conductor MERGE `fa361354…`). The implement branch must start from 749bc146.
**Proposed lab dir:** `kalshi_wx_fl_kxhigh_settled_tape_lab_20261001/`. It has **not** been created. It gets created at implement, after ACCEPT, by the **sole** Variants cloud.

## Authority and context pins (re-hashed on box 2026-10-01)

| Item | Path | sha256 | Verify |
|---|---|---|---|
| **Conductor RULING WX-FL pre-freeze** | `packets/CONDUCTOR_RULING_VARIANTS_WX_FL_PREFREEZE_2026-10-01.json` | `0e37f91b60289084f4e660b74bcb12a04f83f66fc93410add3a26baf0dd9f6af` | MATCH |
| **FL-band freeze (H1/H2/rule source)** | `packets/Q6S5_KXMLBSPREAD_FL_BAND_SETTLED_TAPE_FREEZE_2026-09-29.md` | `fb6540f52ed5f819ccf6e80bf0cf7eb6d951e065416b9d550fead0c6d06043fa` | MATCH |
| **R3-P3 10¢ band registry** (verbatim, never rebinned) | `packets/r3_p3_fl_maker_taker/bands_registry_10c.json` | `0860cbe28d28ecc6142ddf6f1ebb67792084264ed82e0b4d868c3b3138ea5312` | MATCH |
| **Examiner SCORE PR61** (maker_gross_roi formula; H2 reading form) | `packets/EXAMINER_SCORE_Q6S5_KXMLBSPREAD_FL_BAND_SETTLED_TAPE_PR61_2026-10-01.json` | `2e74f17b1307b8b57f33a6475cd7ce8af48c470099478cadfb07877b0d70745f` | MATCH |
| **Conductor ACCEPT Examiner KILL** (KXMLBSPREAD FL-band H1) | `packets/CONDUCTOR_ACCEPT_EXAMINER_KILL_Q6S5_KXMLBSPREAD_FL_BAND_PR61_2026-10-01.json` | `be235777…` (full in SOURCE_PINS) | MATCH |
| **Snapshot (checkpointed copy)** | `packets/WX_FL_KXHIGH_SETTLED_TAPE/snapshot/archive.sqlite` | `d20d5e7d0cedc79ed77c92e905b2824f0ca1d79f8e524635bfd3a8f0e3c6eae2` | made 19:41:25 ET |
| **Gap log: `gaps` table export (all 13,558 rows)** | `packets/WX_FL_KXHIGH_SETTLED_TAPE/GAP_LOG_gaps_table_export_2026-10-01.jsonl` | `0211f5ca2fc6e9ec3ed0c889c5ed50e3ba35360f048a28986116892f090447f6` | from snapshot |
| Gap log: trades `polls` export (3,261 rows, coverage sensitivity) | `packets/WX_FL_KXHIGH_SETTLED_TAPE/GAP_LOG_trades_polls_export_2026-10-01.jsonl` | `a287572c53a69da5baa99f4f6746c9e31c2f58648a10fe9128ef381261d81cf8` | from snapshot |
| Gap log: collector text log (GAP open/close lines; verbatim copy) | `lab/astra-capture/weather-nowcast/logs/collector_20260925T000729Z.log` | `b39d1fcc407254defe0c38591778da36dae070ea161ef2f8d5a1a8a46b2fcdb0` | MATCH |
| Gap log: 429 log (verbatim copy) | `lab/astra-capture/weather-nowcast/logs/kalshi_429.jsonl` | `9b9a2d5e98c202a0b7e5d6b3f3c158a2937c46b0661a618c7d7789d4741d019e` | MATCH |
| Collector code (gap semantics) | `lab/astra-capture/weather-nowcast/collector.py` | `7bd1bddb47079f215502c4600d070497b24da9018e5b06903476062d442db493` | MATCH |
| **card02 freeze kernel** | `packets/CARD02_STATION_WEATHER_NOWCAST_FREEZE_KERNEL_2026-09-24.md` | `6b36dacb84f92524b18c3799c50c5818ee44fee89ac1743ceafb1092cd4c7e48` | MATCH |
| card02 FROZEN_EXPERIMENT / LEDGER / SOURCE_MAP / MANIFEST.md | `packets/card02_station_weather/…` | `beea299c…` / `2eb5b468…` / `2fa868de…` / `62c8b254…` | MATCH |
| weather-nowcast MANIFEST.json / README.md | `lab/astra-capture/weather-nowcast/` | `5214f50a…` / `b8f2bf29…` | MATCH |
| Live db / wal / shm at copy (never opened) | `lab/astra-capture/weather-nowcast/archive.sqlite{,-wal,-shm}` | `974ce4b5…` / `df9765a5…` / `6af7afeb…` | unchanged pre/post copy and at ~19:45 ET |
| Conductor ADMIT-1 RULING | `packets/CONDUCTOR_RULING_ADMIT1_OUTAGE_GAP_WEATHER_CARD03_RELAUNCH_2026-09-29.json` | `ac7cfe63623ca342ab5b4285ff58382a8138b58fb6cd8e95310a5d30d90304f2` | MATCH |
| Conductor MERGE PR62 (implement base 749bc146) | `packets/CONDUCTOR_MERGE_Q6S5_KXMLBSPREAD_GAME_PHASE_SETTLED_TAPE_PR62_2026-10-01.json` | `fa361354aa284b36482b0c4a67715ff6cda63fcf70f2d0c535bd1f7bdc465d5b` | MATCH |
| Conductor ACCEPT game-phase (bc-468d4736) | `packets/CONDUCTOR_ACCEPT_VARIANTS_Q6S5_GAME_PHASE_SETTLED_TAPE_FREEZE_2026-10-01.json` | `08d23b363d72b8c8599772ee6fc6736cb90f13e8ed814b12c59b58fd5c7dc91e` | MATCH |
| Conductor ACCEPT holdout addendum (context; not edited) | `packets/CONDUCTOR_ACCEPT_VARIANTS_HOLDOUT_PREREG_ADDENDUM_Q6S5_KXMLBSPREAD_UNTOUCHED_CAPTURE_2026-10-01.json` | `9a987a77…` | MATCH |
| IN_SAMPLE_DEV ruling (label precedent) | `packets/CONDUCTOR_RULING_Q6S5_FL_BAND_IN_SAMPLE_DEV_LABEL_2026-10-01.json` | `09763030c67df066f2b59346200813e181777670cd46fcee6b8877a6dd74d754` | MATCH |
| R3-P3 kernel / Adversary refuse-bind | `packets/R3-P3_FL_MAKER_TAKER_BANDS_FREEZE_KERNEL_2026-09-22.md` / `packets/R3-P3_ADVERSARY_REFUSE_BIND_2026-09-22.md` | `0ed69714…` / `6b6690cd…` | binds carried |
| v1.2 scorecard template json / md | `templates/EXAMINER_KALSHI_SCORECARD_TEMPLATE_v1.2.json` / `.md` | `56bcf626…` / `ad1dd283…` | MATCH |
| RULE-FROZEN-EDIT-PREV-BYTES-001 | `registry/RULE_FROZEN_EDIT_PREV_BYTES_2026-09-24.md` | `f0aab7d15ca78a097644008db02013eae3a56cb81b2a6aef2cfe6faf21e3e6d1` | pinned |
| PR61 reference runner (formula code, read-only reference) | `orchestrator.py` @ d7558fc4 (`lab/kalshi_q6s5_kxmlbspread_fl_band_settled_tape_lab_20260929/`) | `01a0bf5a3343eb5e9f12eaae9ac64120899603513bffd552f7eb4e616885f80c` | in bundle |

Full 64-hex shas for every row are in `WX_FL_KXHIGH_SETTLED_TAPE/SOURCE_PINS.json`.

## Snapshot (ruling 1)

1. I recorded the live `archive.sqlite` / `-wal` / `-shm` shas (`974ce4b5…` 94,568,448 B; `df9765a5…` 4,165,352 B; `6af7afeb…` 32,768 B) at 19:41:18 ET. The collector was **not running**: last heartbeat 2026-09-27T13:31:22Z, and the pids are dead.
2. I byte-copied the 3 files with `cp --preserve=timestamps` into `WX_FL_KXHIGH_SETTLED_TAPE/snapshot/` and confirmed that the copy shas equal the live shas. The live shas were unchanged after the copy and again at ~19:45 ET.
3. **On the copy only** I ran `PRAGMA wal_checkpoint(TRUNCATE)` → (0,0,0), then `journal_mode=DELETE`, then `integrity_check` → ok, then `chmod 444`. That leaves a single file of **94,629,888 B, sha256 `d20d5e7d0cedc79ed77c92e905b2824f0ca1d79f8e524635bfd3a8f0e3c6eae2`**. The pre-checkpoint wal/shm copies are carried in the bundle.
4. **Cloud open rule:** verify the sha256, then `sqlite3.connect("file:<snapshot>?mode=ro&immutable=1", uri=True)`. Never write. The live `lab/astra-capture/weather-nowcast/archive.sqlite` is **REFUSED** as an input.
5. **Disclosure:** in the earlier leftover survey, before this ruling was stamped, my `mode=ro` (non-immutable) opens of the **live** db rewrote the live `-shm` WAL index (mtime 09-29 16:44 → 10-01 19:36:06 ET). The live db and wal bytes were not modified. The snapshot depends only on db + wal content (`SNAPSHOT_PROVENANCE.json`).
6. **Size:** 94.6 MB, which is under the ~200 MB limit, so the full snapshot goes into the bundle. No pre-ADMIT-1 subset export was needed.

## Evidence class (ruling 2)

`evidence_class = "IN_SAMPLE_DEV"`, `study_label` proposed `"HISTORICAL_REPLAY"` ("historical replay"). **card02 has `admitted_at = null` (never Clock-admitted), so no `pre_admitted_at` flag is possible.** Every row, summary and card carries `pre_admitted_at: null` with `pre_admitted_at_reason: "admitted_at null; card02 never admitted"`. No pre/post-admission split is computed. Verdict ceiling **ITERATE**, `counts_toward_keep=false`, `promote=false`.

## ADMIT-1 exclusion (ruling 3) and verified counts

**Enforced window** `[2026-09-27T00:00:00Z, 2026-09-30T04:00:00Z)` (same as fb6540f5). **No partial-window use.** A market is in scope only if all of the following hold:
- its **first** `kalshi_markets` row with `status=="finalized"` and non-empty `result` was received **< 2026-09-27T00:00Z**
- `settlement_ts` (raw key) **< 2026-09-27T00:00Z**
- `close_time` is not in the window

A trade is in scope only if `created_time < 2026-09-27T00:00Z`. `capture.sqlite` is **REFUSED** and never opened. No backfill and no interpolation, ever.

**Re-verified from snapshot `d20d5e7d…`** (row counts / status / timestamps only; `tools/wx_fl_timestamp_feasibility.py` → `FEASIBILITY_COUNTS_TIMESTAMP_ONLY.json` `2f019a94…`):

| City-day (event_ticker) | Markets | Latest status | close_time max (UTC) | settlement_ts (UTC) | Trades created < W0 |
|---|---|---|---|---|---|
| KXHIGHCHI-26SEP24 | 6 | finalized ×6 | 2026-09-25T06:00Z | 2026-09-25T12:09:48Z | 60 |
| KXHIGHLAX-26SEP24 | 6 | finalized ×6 | 2026-09-25T08:00Z | 2026-09-25T14:09:28Z | 341 |
| KXHIGHMIA-26SEP24 | 6 | finalized ×6 | 2026-09-25T05:00Z | 2026-09-25T11:10:38Z | 172 |
| KXHIGHNY-26SEP24 | 6 | finalized ×6 | 2026-09-25T05:00Z | 2026-09-25T11:10:08Z | 65 |
| KXHIGHCHI-26SEP25 | 6 | finalized ×6 | 2026-09-26T06:00Z | 2026-09-26T12:09:36Z | 4,374 |
| KXHIGHLAX-26SEP25 | 6 | finalized ×6 | 2026-09-26T08:00Z | 2026-09-26T14:21:36Z | 10,604 |
| KXHIGHMIA-26SEP25 | 6 | finalized ×6 | 2026-09-26T05:00Z | 2026-09-26T11:20:06Z | 10,391 |
| KXHIGHNY-26SEP25 | 6 | finalized ×6 | 2026-09-26T05:00Z | 2026-09-26T11:19:36Z | 7,750 |
| **Total** | **48** | **48 finalized** | | 0 in window, 0 null | **33,757** (26SEP24 638 / 26SEP25 33,119) |

- **8 city-days / 48 markets confirmed**, matching the ruling.
- Out of scope: 66 markets / 11 events were ever finalized with a result. The 18 `-26SEP26` markets (CHI/MIA/NY) are excluded because their first finalized receipt is ≥ W0.
- Trades created ≥ W0 on in-scope markets: 0. Trades received ≥ W0: 0. Post-close trades (timestamp-only): 0. So the expected `excluded_admit1_window_n = 0`, and any non-zero count must be reported.
- Each city-day is one mutually exclusive bracket set (6 strikes, one YES), so each city-day carries **one** weather outcome.

**Sampling-frame caveat (declared; not a gap window).** The archive started at `2026-09-25T00:07:29Z`. The first trades poll used `min_ts = archive start`, and the earliest in-scope trade is 00:07:48Z. All markets opened at `14:00Z` the day before their date (`open_time` 09-23T14:00Z for 26SEP24, 09-24T14:00Z for 26SEP25). So the **26SEP24 city-days hold only the final ~4.9–7.9 h before close**, and the first ~10.1 h of 26SEP25 trading is unobserved. Nothing was captured there in any arm, so there is nothing to exclude. This is why "without Sep-25" (= the 4 late-session SEP24 city-days only) is reported but is not decisive.

## Weather HOLD (ruling 4)

The HOLD covers GETs and the collector relaunch only. This packet and its cloud make **zero GETs** (Kalshi, NWS, any host). No network import is allowed in the runner. The `-26SEP26` settlements and any post-W0 data stay out.

## Intent (one knob)

Keep everything fixed: the snapshot, the row rules of fb6540f5, the band registry, and gross/fee-free accounting. Vary **only** `price_band` of the **taker-purchased side** of each public KXHIGH print. Measure the realized settlement return of the **passive (maker) counterparty**. This is an **out-of-domain replication** of the MLB FL-band result (fb6540f5 → Examiner `2e74f17b` contradicts_H1 → Conductor KILL `be235777`, KXMLBSPREAD only). It is not a new fishing knob: same knob, same bands, same H1/H2, same rule.

**Not a strategy.** No Astra orders, fills or PnL. Observations are labeled `public_counterparty_realized`, never `pnl`. `results` / `pnl` / v1.2 `net_pnl_*` stay null.

| Arm | Label | `p_taker` range | Registry bands (`0860cbe2…`, lo/hi inclusivity verbatim) | Maker counterparty holds |
|---|---|---|---|---|
| **WXFL0** | `longshot_taker` | `[0.00, 0.20)` | b00, b01 | the favorite side at `1 − p_taker` ∈ (0.80, 1.00] |
| **WXFL1** | `mid` | `[0.20, 0.80)` | b02–b07 | the opposite side at (0.20, 0.80] |
| **WXFL2** | `favorite_taker` | `[0.80, 1.00]` | b08, b09 | the longshot side at `1 − p_taker` ∈ [0.00, 0.20] |

These are identical to fb6540f5 arms Q6S5FL0/1/2, renamed only for the series. No rebinning.

## Row construction (fb6540f5 rules verbatim; source fields mapped to the snapshot)

- **Source:** `kalshi_trades.raw`, the verbatim Kalshi trade JSON text. It has keys `count_fp, created_time, is_block_trade, no_price_dollars, taker_book_side, taker_outcome_side, taker_side, ticker, trade_id, yes_price_dollars`. `trade_id` is the primary key, so there are no duplicate rows.
- **Market fields** come from the **first** finalized-with-result `kalshi_markets` row per ticker (by `received_at`): `result`, `close_time`, and `settlement_ts` from its zlib raw JSON. Every later finalized row must carry the same `result`; otherwise it is a **hard fail**.
- **Universe:** the 48 tickers listed in `FROZEN_EXPERIMENT.json → universe.markets`. No other markets.
- **Native side only** (fb6540f5 verbatim): `s = taker_outcome_side` ∈ {yes, no}. A row is used only if `taker_side == taker_outcome_side` and (`s=yes` ⇔ `taker_book_side=bid`; `s=no` ⇔ `taker_book_side=ask`). Any other combination is excluded and counted. **Lee-Ready REFUSED.**
- **Taker price:** `p_taker = yes_price_dollars` if `s=yes`, else `no_price_dollars`. A row is excluded if `|yes+no−1| > 1e-9`.
- **Exclusions (counted per arm where the arm is defined, never imputed):**
  - `is_block_trade == true`
  - `created_time ≥ close_time` (post-close)
  - ADMIT-1 window
  - **gap windows (below)**
  - a market whose `result ∉ {yes,no}` (whole market)
- **Weight:** `q = count_fp`. **Settlement:** `Y_s = 1` if `result == s`, else 0.
- **Information set:** the band uses only the print's own price at its own `created_time`. Settlement is used only as the ex-post label. Gap exclusion uses only collector timestamps. No row selection depends on outcome or on later prints.
- **City-day** = `event_ticker` (e.g. `KXHIGHNY-26SEP25`). "Date" = the event's measured-temperature date code (26SEP24 / 26SEP25), not the trade's UTC date. "City" = series.

## Gap log and gap-window exclusion (freeze_requirement 4)

**Where the collector logged budget-short gaps:** the `gaps` table inside the archive (`collector.py` `gap_open`/`gap_close`; schema `id, stream, key, started_at, ended_at, reason, detail, n_polls`). The same events are echoed as `GAP open/close` lines in `logs/collector_20260925T000729Z.log`. Budget-short gaps are `stream='kalshi_trades_budget'`, `reason='budget_shortfall_sweep_late'`: no successful trades poll for that ticker within the 1,800 s sweep target. The pinned gap log is the full `gaps` table exported from the snapshot (`GAP_LOG_gaps_table_export_2026-10-01.jsonl`, 13,558 rows, `0211f5ca…`). Serialization: one `json.dumps(row, sort_keys=True, separators=(",",":"))` per line, ordered by `id`. The runner must regenerate this export from the snapshot and assert byte equality before use.

**Flagged gap windows that apply to trades:**

| Stream / reason | Applies to | Rows (all) | On in-scope tickers | Open-ended (in scope) |
|---|---|---|---|---|
| `kalshi_trades_budget` / `budget_shortfall_sweep_late` | its `key` ticker | 2,728 | 1,050 | 36 |
| `kalshi_trades` / `http_429` | its `key` ticker | 374 | 131 | 9 |
| `kalshi_all` / `pause_429_storm` (all Kalshi GETs paused) | **all tickers** | 225 | n/a | — |
| `collector` / `collector_not_running` | all tickers | 0 | — | — |
| `kalshi_trades` / `trades_page_limit` | its ticker | 0 | — | — |

Not mapped to trades: `kalshi_orderbook*`, `kalshi_events`, `kalshi_discover`, `kalshi_event_meta`, `kalshi_series_meta`, `nws_*`. These streams do not carry trade prints, and every in-scope market is trades-polled from archive start (below).

**PRIMARY mapping GM-LIT (ruling-literal; matches the design lock).**
- A trade on ticker `t` is excluded **from all arms** iff its `created_time` ∈ `[started_at, ended_at)` of any flagged window whose key is `t` (streams `kalshi_trades`, `kalshi_trades_budget`) or of any all-ticker window (`kalshi_all`, `collector`).
- Boundaries: `started_at` inclusive, `ended_at` exclusive. `ended_at = null` → `+∞`.
- No padding and no recovery credit.
- Expected (timestamp-only): **27,199 of 33,757 excluded (80.57%); 6,558 kept.** Kept by city-day: CHI24 12, LAX24 97, MIA24 34, NY24 14, CHI25 775, LAX25 2,209, MIA25 1,701, NY25 1,716. All 8 city-days are non-empty before the row rules.

**Pre-declared sensitivities (reported, never decisive unless the Conductor swaps at ACCEPT):**
- **GM-COV (recovery-aware).** Exclude iff the trade is inside a flagged window as above **and** outside every *complete-poll coverage interval* of its ticker. A logical trades poll is a page sequence in `polls` (stream `kalshi_trades`) that starts at a URL without `&cursor=`. It is complete iff every page has `ok=1` and the last page has `n_items < 1000`. Its coverage is `[min_ts (URL), requested_at of first page)`.
  - Expected: **0 excluded.** 3,261 logical polls, 2,821 complete. 100% of the 33,757 trades lie inside complete coverage. There are 0 coverage holes between archive start and close for all 48 markets.
  - Why it exists: `collector.py do_trades` re-polls from `last cursor − 1 s` and pages up to 10×1000. The flagged windows are receipt-latency windows whose trades were re-fetched later. Edge caveat: a trade created ≤ 1 s before a poll and not yet visible could be missed.
- **GM-LIT-PAD.** GM-LIT, with budget windows widened to `[started_at − 1,920 s, ended_at)`, i.e. the full lateness interval (1,800 s target + 120 s loop slack). Expected **33,622 excluded (99.60%); 135 kept.** CHI24 and NY24 are 0, so this mapping is NOT_INTERPRETABLE for EW and is reported as counts only.
- Single-stream components of GM-LIT (budget only 53.6%, trades_429 only 12.0%, storm only 58.5%) are reported as counts.

**Per-arm excluded counts are OMITTED here.** Computing them needs the native-side filter and `p_taker`, i.e. side and price fields beyond plain band assignment. The implement cloud computes and reports `excluded_gap_n[arm][mapping]` for every arm and mapping, plus `excluded_gap_n_unassignable` (gap-excluded rows that also fail native-side/price rules), before any ROI is printed.

## Metrics (all null now)

Per city-day `d` and arm `A`, these are the Examiner `maker_gross_roi` formula of score `2e74f17b` / fb6540f5 lines 97–100:
- `maker_gross_return_usd[d,A] = Σ q·(p_taker − Y_s)`
- `maker_capital_usd[d,A] = Σ q·(1 − p_taker)`
- `maker_gross_roi[d,A] = return / capital`
- `taker_gross_roi[d,A] = Σ q·(Y_s − p_taker) / Σ q·p_taker`
- `n_trades`, `contracts`, `n_markets`

**PRIMARY (H1), city-day-equal-weighted:** `EW_delta_FL0_minus_FL1 = mean over d ∈ D₀₁ of (maker_gross_roi[d,WXFL0] − maker_gross_roi[d,WXFL1])`. `D₀₁` = the city-days where both arms have `maker_capital_usd > 0`. `n_eff = |D₀₁|` is reported.
**Primary for H2:** `EW_delta_FL2_minus_FL1`, defined the same way over `D₂₁`.
**SECONDARY (trade-weighted):** pooled `maker_gross_roi[A] = Σ_d return / Σ_d capital` (Examiner `arms.maker_gross_roi`). Gives `TW_delta_FL0_minus_FL1` and `TW_delta_FL2_minus_FL1`.
**Robustness (pre-registered, for both deltas, EW and TW):**
- leave-one-city-day-out (LOCDO, `n_eff` values)
- leave-one-date-out (LODO, 2 values: drop 26SEP24 / drop 26SEP25)
- leave-one-city-out (LOCO, 4 values)

**With and without Sep-25:** every number above is also reported on the 26SEP24-only subset (4 city-days; LODO is undefined there and set null).
**Stresses:** `one_tick_worse` (maker charged $0.01/contract: capital +0.01, return −0.01), applied to EW and TW deltas. `fees_2x` is **n/a** because no fee view is computed. The mapping sensitivities GM-COV / GM-LIT-PAD are run under the identical pipeline.
**Descriptive:** per-city-day × arm tables; per-market; `maker_gross_roi` per 10 registry bands.
**Not in scope:** Mincer–Zarnowitz; clustered inference (8 correlated clusters); `executable_dollars_per_day`; any NWS/temperature feature (out of knob).

## Hypothesis and reading rule (written before outcomes; copied from fb6540f5)

Verbatim from fb6540f5 (`fb6540f5…`, §"Hypothesis and reading rule", lines 116–118):

> - **H1 (favorite–longshot bias, maker side):** `maker_gross_roi_delta_FL0_minus_FL1 > 0`. Passive counterparties to longshot-buying takers earn more per dollar at risk than mid-band counterparties. The Bürgi–Deng–Whelan "+2.6% maker ≥50¢" figure is a **hypothesis only, not Astra evidence** (Adversary bind).
> - **H2:** `maker_gross_roi_delta_FL2_minus_FL1 ≤ 0`. Counterparties to favorite-buying takers (makers holding longshots) do no better than mid.
> - **Variants-proposed reading (Examiner owns the verdict):** `supports_H1` if the full-sample delta > 0 **and** ≥2 of 3 leave-one-event-out deltas > 0. `contradicts_H1` if the full-sample delta ≤ 0 **and** ≥2 of 3 LOEO deltas ≤ 0. Otherwise `inconclusive`. **Verdict ceiling ITERATE:** measurement only, no KEEP, `counts_toward_keep=false`. `contradicts_H1` supports a KILL of the FL-band maker thesis **for KXMLBSPREAD only**.

**Domain substitutions (the only changes; declared pre-outcome):**
1. "event" := **city-day**. "full-sample delta" := the **PRIMARY `EW_delta`** under the PRIMARY gap mapping, over all 8 city-days.
2. "≥2 of 3 LOEO" := **≥ ⌈2·n/3⌉ of the n LOCDO deltas**, where n = `n_eff`; with n = 8 this is **≥ 6 of 8**. If `n_eff < 3`, the reading is `inconclusive` (insufficient city-days).
3. KILL scope "for KXMLBSPREAD only" := **for KXHIGHCHI/LAX/MIA/NY only (this snapshot universe)**.
4. H2 reading uses the Examiner form from `2e74f17b` (`secondary.reading_H2`: "consistent with H2 (full ≤ 0; 2/3 LOEO ≤ 0)"):
   - `consistent_with_H2` if `EW_delta_FL2_minus_FL1 ≤ 0` and ≥ ⌈2n/3⌉ LOCDO ≤ 0
   - `inconsistent_with_H2` if `> 0` and ≥ ⌈2n/3⌉ LOCDO > 0
   - else `inconclusive`

Note: ruling `0e37f91b` paraphrases H2 as "FL2 < FL1". The ruling also requires "the SAME … as fb6540f5", so the fb6540f5 text (`≤ 0`) governs here.

The same rule is **also** applied, as reported and non-decisive readings, to: the TW secondary, the 26SEP24-only subset, LODO/LOCO (sign counts reported), GM-COV, and `one_tick_worse`.

**Replication framing:**
- `contradicts_H1` here = the MLB KILL (`be235777`) **replicates out of domain**. It supports a KILL of the FL-band maker thesis for the 4 KXHIGH series.
- `supports_H1` = the MLB result does **not** replicate, so the FL-band effect is domain-dependent. That is hypothesis-generating only, and any KXHIGH maker build would need untouched post-relaunch weather capture.
- Either way: ITERATE ceiling, no KEEP, no Q6-000 retune.

**Power / multiplicity (declared):**
- **Effective n = 8 city-days**, not 33,757 prints.
- Cities sharing a date are correlated (one national weather regime, one session), hence LODO/LOCO.
- 26SEP25 holds 98.1% of prints, hence EW primary and the without-Sep-25 report.
- `family_size = 1` on this new universe: WX-TTC is **not** frozen alongside it, and no other knob is pre-registered on this snapshot. The MLB family (4 knobs on 3 games) is a different universe.

## Fee

Gross, fee-free primary and secondary. Fee label **`CACHE_NOT_R1P1`** is kept, with `fee_honest=false` and `claim_as_live_R1P1=false`. No KXHIGH FEE_PIN exists on disk: `kalshi_series_meta` has 0 rows in the snapshot, and no GET is allowed. So `maker_net_roi_cache` / `taker_net_roi_cache` stay **null** and are not computed. **Not R1-P1.**

## Ruling compliance (item by item)

| Ruling / requirement | Handling | Status |
|---|---|---|
| 1 card02 snapshot, checkpoint copy, pin sha | `d20d5e7d…`; live never opened by sqlite after the ruling; card02 packets untouched | **met** (prior live-shm touch disclosed) |
| 2 IN_SAMPLE_DEV / HISTORICAL_REPLAY; no pre_admitted_at | declared; `pre_admitted_at: null` with reason | **met** |
| 3 ADMIT-1: pre-W0 only; 8 city-days / 48 markets | re-verified 48 / 8; 0 trades or settlements in window | **met** |
| 4 zero GETs | no network in freeze or cloud | **met** |
| FR1 same H1/H2/rule as fb6540f5 | verbatim quote + 4 declared substitutions | **met** |
| FR2 n = 8; LODO + LOCO + LOCDO | declared | **met** |
| FR3 EW primary, TW secondary, with/without Sep-25 | declared | **met** |
| FR4 pin gap log; exclude flagged gap windows from both arms; per-arm excluded counts | gap log pinned; GM-LIT primary excludes from all arms | **met, with a Conductor choice:** GM-LIT drops 80.6% of trades, all of which were fully captured (GM-COV shows 100% recovery). The Conductor may designate GM-COV as primary **at ACCEPT, before any outcome is read**. Without that, GM-LIT governs. Per-arm counts are computed by the cloud (omitted here, see above). |
| FR5 CACHE_NOT_R1P1; gross; no invented fills/pnl; design lock before prices | lock 19:41:14 ET before snapshot/counts; no price/result value read | **met** |

## Scorecard fields (null now)

These all stay **null** until an Examiner-scored run:
- `results`, `pnl`
- per-city-day and pooled `maker_gross_roi` / `taker_gross_roi` per arm
- EW/TW deltas, LOCDO/LODO/LOCO vectors, with/without Sep-25, GM-COV/GM-LIT-PAD sensitivities, `one_tick_worse`
- `n_trades`, `contracts`, `n_markets`, `n_eff`
- `excluded_*_n` incl. `excluded_gap_n[arm][mapping]`
- `reading`

The v1.2 stub (template `56bcf626…`) is in `EXAMINER_SCORECARD_STUB_*.json/.md`:
- `simulated_fills` n/a (`counts_toward_keep=false`)
- controls: `market_only` applies; `no_trade` / `simple_model` n/a
- `emits_probabilities=false`
- `study_label` null, Variants proposes "historical replay"

## p16 preregistration checklist

| # | Item | Status | Evidence |
|---|---|---|---|
| 1 | market_universe | **satisfied** | 48 markets / 8 city-days listed; KXHIGH 4 series only |
| 2 | exclusions | **satisfied** | ADMIT-1 window; 26SEP26 events; post-close; block; native-field conflicts; price-inconsistent; gap windows (GM-LIT); result ∉ {yes,no}; live db, capture.sqlite refused |
| 3 | receipt_time_information_set | **satisfied** | band from own price at own created_time; gap mapping from collector timestamps only; settlement ex-post label; sha-pinned snapshot |
| 4 | fee_regime | **satisfied** | gross only; CACHE_NOT_R1P1 label; net null (no KXHIGH FEE_PIN; no GET) |
| 5 | order_timing | **n/a** | no Astra orders |
| 6 | sizing | **n/a** | rows weighted by `count_fp` |
| 7 | fill_model | **n/a** | no Astra fills |
| 8 | stopping_rules | **satisfied** | freeze → ACCEPT → sole cloud; single pass; mapping fixed at ACCEPT; no rerun with altered windows/bands |
| 9 | evaluation_metrics | **satisfied** | EW primary, TW secondary, LOCDO/LODO/LOCO, with/without Sep-25, one_tick_worse |
| 10 | limit_candidate_variants | **satisfied** | one knob × 3 values; registry fixed; family_size 1 |
| 11 | log_every_attempted_variant | **satisfied** | 3 arms + declared sensitivities only; any other cut needs a new freeze |
| 12 | separate_discovery_tuning_evaluation_periods | **missing** | no untouched weather set until the collector relaunch (HOLD); no tuned parameter |

Counts: satisfied 8, n/a 3, missing 1.

## Merge gates (implement)

Units must be green at implement, including:
- snapshot sha fail-closed, opened with `mode=ro&immutable=1`
- **live-db path refused**
- `capture.sqlite` refused
- **no network import** (`urllib`/`requests`/`http`/`socket` are forbidden-import tested)
- `sqlite3` import **permitted only** in the snapshot loader. This deviates from the PR61/PR62 convention, and is needed because the pinned input is a sqlite file.
- ADMIT-1 rejection of a synthetic trade and of a synthetic settlement in the window
- gap-export regeneration == pinned `0211f5ca…`
- GM-LIT boundary tests: a trade at `started_at` is excluded, at `ended_at` is kept, and an open-ended window excludes to +∞; an all-ticker storm window hits every ticker
- GM-COV complete-poll construction test
- first-finalized-result consistency hard fail
- native-side / Lee-Ready refusal
- registry inclusivity verbatim (0.20 → WXFL1, 0.80 → WXFL2, 1.00 → WXFL2)
- EW vs TW computation
- ⌈2n/3⌉ threshold (n=8 → 6)
- `pre_admitted_at` null with reason
- `evidence_class=IN_SAMPLE_DEV` on rows/summary/card
- no-invent: a market without a result produces no rows

`results` and all metrics stay null until Examiner. **HOLD for Conductor ACCEPT: no CloudAgent, no PR, no `admit.py`, no GET, no orders.**

## Integrity

- Pinned bytes are carried **verbatim** and checked with `sha256sum`. Authentic-pins bundle: `/workspace/WX_FL_KXHIGH_SETTLED_TAPE_authentic_pins_2026-10-01.tgz` (sha and file count in the digest and ping).
- RULE-FROZEN-EDIT-PREV-BYTES-001: this freeze **creates only new files**. No frozen file was edited, so there was no `_prev` write. The holdout addendum is untouched.
- Absent (declared, not recreated):
  - KXHIGH FEE_PIN / formula_id
  - untouched weather evaluation set
  - pre-archive trades (before 2026-09-25T00:07:29Z)
  - 26SEP26 settlements (in window)
  - card02 Clock admission (admitted_at null)
  - prior live `-shm` bytes

## Refuse binds

- invent fills / PnL / settlement_ts / markets / depth
- label public-counterparty return as Astra PnL
- any GET (Kalshi/NWS/other)
- orders
- `admit.py`
- reading `capture.sqlite`
- opening or writing the live weather db (or its -wal/-shm)
- collector relaunch
- Lee-Ready
- rebin `0860cbe2`
- Q6-000 retune
- S1 / Cap-SR / Q6S1 / Refiner
- re-measure KXMLBSPREAD
- choosing or swapping the gap mapping after any outcome or price read
- backfill / interpolation
- claim CACHE as R1-P1 or "fee-honest"
- dual-cloud
- editing prior SCORE / ACCEPT / RULING / addendum bytes
- KEEP from this measurement
