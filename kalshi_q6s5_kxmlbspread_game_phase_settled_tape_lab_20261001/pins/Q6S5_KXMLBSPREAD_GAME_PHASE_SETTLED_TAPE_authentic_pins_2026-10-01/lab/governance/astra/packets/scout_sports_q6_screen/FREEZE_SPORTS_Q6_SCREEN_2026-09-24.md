# FREEZE — Sports / microstructure candidate screen vs Q6-000

- **Seat:** Market Scout (executor / Astra-Kalshi). **Freeze written:** 2026-09-24 23:46:51 EDT (ET). **Mode:** READ-ONLY. GET-only public Kalshi API. No orders, no invented volume/OI/PnL, no panel admits, no `SHADOW_CANDIDATE_FREEZE` / Q6-000 retune, no Cap-SR / FQ / RFQ objects.
- **Directory:** `lab/governance/astra/packets/scout_sports_q6_screen/`. Brief: `lab/governance/astra/SCOUT_SPORTS_Q6_SCREEN_2026-09-24.md`. Raw: `raw/` + `MANIFEST.sha256`.
- **Parent context:** Conductor ACCEPTED Card 06 company-KPI census (freeze `1413603c…`). Card 06 open-window differentiator is **CLOSED this wave**. Maximize-next = this sports/microstructure screen vs Q6-000 KEEP under fee/queue honesty.
- **Hosts:** `https://api.elections.kalshi.com/trade-api/v2` (primary); `https://external-api.kalshi.com/trade-api/v2` allowed. **Skip** `trading-api.kalshi.com`. Throttle **45–90s** between live GETs. On **429**: skip that series, record blocker, do not invent inventory.
- **Kickoff SoT:** Kalshi market `occurrence_datetime` (Z → America/New_York labeled ET).
- **This freeze file is never edited.** Later changes = dated `AMENDMENT_NN_*.md` + own sha256. RULE-FROZEN-EDIT-PREV-BYTES-001: before editing any already-filed file, save `_prev/<sha256>.<name>` and log old→new; prefer NEW files.

## 0. Pre-freeze local reads (DISCLOSED; not inventory proofs)

Local-only before this freeze (no live Kalshi inventory GETs yet):
- Prior Scout briefs: `SCOUT_Q6_STRESS_KERNELS`, `SCOUT_CASHCOW_HUNT`, `SCOUT_R2P3_PROP_SLATE`, `SCOUT_MAXIMIZE_DELTA`, Card 06 accepts/cemetery index.
- Fee-type **cache label** source: `packets/scout_house_fee_2026-09-24/raw/kalshi/nonstandard_fee_series.json` (house-fee packet; used only for `fee_type` / `fee_multiplier` preference when live `/series` 429s).
- Prior hunt JSON under `packets/scout_cashcow_hunt_2026-09-22/` used only to choose include candidates — **not** reused as this screen’s inventory proof. Every candidate’s open-markets page is re-pulled post-freeze.

## 1. Include series (post-freeze inventory pull set)

Pull `GET /markets?series_ticker=S&status=open&limit=200` (first page only; record cursor present/absent). Optional cheap `GET /series/S` for fee pin if `/series` list endpoint 429s — else use house-fee cache and **label cache**.

| Slot ID (template) | Primary series | Alternates (same slot; first with non-empty open inventory wins) |
|---|---|---|
| **Q6S1** | `KXATPMATCH` | `KXWTAMATCH` |
| **Q6S2** | `KXNHLGAME` | *(none — C2 reinforce/refine only)* |
| **Q6S3** | `KXNFLANYTD` | `KXNFLFIRSTTD`, `KXNFL2TD` |
| **Q6S4** | `KXUCLGAME` | `KXEPLGAME`, `KXBUNDESLIGAGAME`, `KXLALIGAGAME`, `KXSERIEAGAME` |
| **Q6S5** | `KXMLBSPREAD` | `KXMLBF5`, `KXMLBTOTAL`, `KXNBAGAME`, `KXWNBAGAME`, `KXNCAAFSPREAD` |

**N per series:** count of open markets on the **first successful HTTP 200 page** (`limit=200`). Sampling method = that first page only (no deep cursor chase this screen). If cursor present, note `partial_page=false` only when `len(markets)<200` or cursor empty; if `len==200` and cursor non-empty → flag `page_capped=true` (sums are lower bounds).

## 2. Exclude series (do not re-open / do not poll as new)

| Exclusion | Reason |
|---|---|
| CEM-ASTRA-20260924-006 macros: `KXJOBLESSCLAIMS`, `KXPCECORE`, `KXFEDDECISION`, `KXFED`, `KXEIACRUDEW` | Card 06 macro CEMETERY |
| CPI CEM-003 / `KXCPI*` / Card 06 reopen | Closed differentiator this wave |
| Cap-SR / FQ / merged RJs | Out of seat (Variants lane) |
| RFQ-blocked Card 07 / RFQ objects | No RFQ |
| `SHADOW_CANDIDATE_FREEZE` / Q6-000 retune | Forbidden |
| More `KXNFLGAME` ML capacity | Occupied incumbent |
| S5 `KXMVECROSSCATEGORY*` measurement | FREEZE locked — do not re-nominate as new |
| C1 `KXUFCFIGHT` / C3 `KXHIGHNY` / C5 `KXBTC15M` | Occupied cash-cow freezes — **unless** a *distinct* microstructure kernel is explicitly proposed (none in this ≤5 template set) |
| Hard capture `KXNFLSPREAD` / `KXNFLTOTAL` | S2/R2-P4 still gated on C1 PIT@CLE smoke — may appear only as **TRY-after-C1** narrative; **do not** steal ADMIT-1 poll budget with hard SPREAD/TOTAL GET this screen |
| Occupied freezes S1 `KXMLBGAME` game-ML / S4 `KXNCAAFGAME` game-ML / R2-P3 `KXNFLPASSYDS` (+ RECYDS/RSHYDS slate as *same* ladder kernel) | Do not re-nominate as “new”; S1 may appear only via **distinct** microstructure (Q6S5 spread/F5 path) |

## 3. Measurement-kernel templates (one sentence each slot; locked)

| Slot | One-sentence measurement kernel (what Examiner would score) |
|---|---|
| **Q6S1** | On ATP (or WTA) match ML books, do fee-honest maker/taker fills + R1-P5 freshness/queue instruments under a tennis match clock produce completed-net / unresolved-inventory statistics that **beat or stress** Q6-000’s NFL T−window shadow EV under shared $5k bakeoff rules? |
| **Q6S2** | Does NHL game ML (C2 reinforce/refine) generalize the daily-sports maker-fee channel vs Q6-000 without silently retuning the NFL ML allocator — score fee-honest adverse markout + queue fragility on puck-drop SoT windows? |
| **Q6S3** | On NFL anytime/first/multi-TD prop binaries **beyond** the occupied R2-P3 PASSYDS ladder slate, do sparse multi-player books show near-0/1 fee + queue honesty failures that stress whether `000`’s binary-ML fee assumptions transfer to TD props? |
| **Q6S4** | On soccer game ML (UCL/EPL/Bundesliga/La Liga/Serie A — first with inventory), does a non-US sports clock + maker-fee path displace or stress Q6-000 under the same R1-P1/P5 instruments? |
| **Q6S5** | On a **distinct** MLB microstructure (spread / first-5 / total) or NBA/WNBA game or NCAAF spread — **not** S1/S4 game-ML retune — does fee_type/multiplier divergence (esp. MLB `quadratic`×0.5 vs NFL `quadratic_with_maker_fees`×1) create honesty stress that threatens `000`’s inherited maker/taker assumptions? |

## 4. Dead-overlap rubric vs Q6-000 (locked before pulls)

| Label | Definition (apply to each slot after inventory) |
|---|---|
| **none** | Different calendar/clock and contract family; no NFL week/T−7d join; no pair-router semantics. |
| **low** | Different sport clock or structure; may share fee channel with sports books but not `000` event set. |
| **medium** | Same NFL (or same-weekend football) calendar as `000` events possible; **different contracts**; not a silent retune of timing/sizing/offset. |
| **high** | Same events + contract family close enough that a new freeze would risk silent `000` retune — **SKIP** or force explicit Conductor bakeoff (not used for SPREAD/TOTAL hard poll this screen). |

## 5. Fee_type preference (locked)

1. Prefer series with **readable** `fee_type` from live `/series/{S}` **or** house-fee cache (must **label cache** if live 429).
2. Preference order for honesty compare to NFL game books / `000`: `quadratic_with_maker_fees` (multiplier 1) → `quadratic_with_maker_fees` (other mult) → `quadratic` (esp. MLB 0.5 = stress) → other readable → unknown (**DEFER** if fee unreadable and cache miss).
3. Fee pin ≠ R1-P1 until Examiner tests land (Adversary note); still required as honesty hook metadata.

## 6. Inventory proof fields (locked; raw only)

From each HTTP **200** markets page, report only:
- HTTP status, `n_markets`, `n_events` (distinct `event_ticker`),
- Σ `volume_fp`, Σ `volume_24h_fp`, Σ `open_interest_fp` (raw API strings/numbers summed; **never invented**),
- up to 2 sample market tickers with their raw `volume_24h_fp` / `open_interest_fp` / `occurrence_datetime`→ET,
- `page_capped` flag, fee pin source (`live` | `cache`).

Non-200 / 429 → no inventory claimed for that series.

## 7. Recommendation labels (locked)

| Label | When |
|---|---|
| **TRY** | 200 + non-empty open inventory + fee readable + dead-overlap none/low/medium + kernel fits fee/queue honesty stress vs Q6-000 + not excluded. |
| **HOLD** | Inventory/fee OK but capacity/gate (Collector/ADMIT-1) or reinforce-only without new freeze ask. |
| **SKIP** | Empty open markets, occupied re-nominate, high dead-overlap retune risk, or excluded. |
| **DEFER** | 429 / fee unreadable / structural blocker; no invented fill. |
| **TRY-after-C1** | Reserved for S2/R2-P4 SPREAD/TOTAL family only — narrative OK; **no hard poll** this screen. |
| **CEMETERY** | Structure permanently unfit to stress fee/queue honesty vs Q6-000 (e.g. no event clock / no readable fee path / season-long futures with zero microstructure surface). Not expected for most sports game books. |

## 8. Analysis method (fixed before pulls)

1. After freeze hash filed: pull include series in slot order Q6S1→Q6S5; within a slot try primary then alternates until first **200 with n_markets>0**, else record all failures.
2. Throttle 45–90s between GETs; on 429 skip remainder of that series (no burst retry storm; optional single retry after ≥60s only if time allows — prefer DEFER).
3. Fill ≤5 table rows from templates; assign dead-overlap + rec using locked rubric.
4. Rank among TRY: (a) fee honesty hook strength, (b) lower dead-overlap preferred for displacement, (c) non-zero raw Σ vol24/oi, (d) sports-focus fit. Do not invent ranks from missing data.
5. Light GitHub/open-repo pointers **only if** inventory-backed for a TRY/HOLD slot (same rule as cash-cow hunt); else appendix omit.
6. Write brief + raw JSON + `MANIFEST.sha256`. No orders.

## 9. Cite prior (frozen references)

`SCOUT_Q6_STRESS_KERNELS_2026-09-22.md`, `SCOUT_CASHCOW_HUNT_2026-09-22.md`, `SCOUT_R2P3_PROP_SLATE_2026-09-22.md`, `SCOUT_MAXIMIZE_DELTA_2026-09-22.md`, Card 06 ACCEPT (`packets/CONDUCTOR_ACCEPT_CARD06_OPEN_WINDOW_CENSUS_2026-09-24.json` / company-KPI freeze `1413603c…`), CEM-ASTRA-20260924-006.
