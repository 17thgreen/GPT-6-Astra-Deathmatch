# CLOCK ADMIT — Q6S5 KXMLBSPREAD FEE+QUEUE PANEL 2026-09-25

**Issued by:** The Clock  
**Issued UTC:** 2026-09-25T04:37:47Z  
**Issued ET:** 2026-09-25 00:37:47 EDT  
**Packet:** `Q6S5-KXMLBSPREAD-FEEQUEUE-HARNESS`  
**panel_version:** `2026-09-25.q6s5-kxmlbspread-v0`  
**Series:** `KXMLBSPREAD` ONLY  
**Conductor kick:** `CONDUCTOR_KICK_CLOCK_Q6S5_KXMLBSPREAD_PANEL_ADMIT_2026-09-25.json` sha256 `1e2be3720a90283fffccd04b602d0350591ccc0242204e477086aeccc0d4d95f`  
**Conductor accept READY:** sha256 `96cb4632b2475a6819c5aa1d1bd2f7893de16309f6322a96271eaf0d7713ba8a`  
**Examiner READY NOT_SCORED:** sha256 `cb25d9a7aa65ea5bcbeaccab01fe27968542b78399e5049262f1e7ae296cead2`  
**Stub:** `/workspace/lab/astra-capture/q6s5-kxmlbspread/panel_stub.json` sha256 `c7f1f1f4ca263838c4600ed46db8f525b68efc5399a567bd60929d18d76803cc`  
**Admitted:** `/workspace/lab/astra-capture/q6s5-kxmlbspread/panel_admitted.json` sha256 `e36de2d1ce6286dff90d25f2fae680170c8a469c443c1beed974ffe80383fba1`  
**Packets copy:** `/workspace/lab/governance/astra/packets/Q6S5_KXMLBSPREAD_PANEL_ADMITTED_2026-09-25.json` (byte-identical)  
**live_get:** `/workspace/lab/astra-capture/q6s5-kxmlbspread/live_get_admit_2026-09-25/`

---

## DATA VERDICT: **ADMIT PASS**

Measurement-panel admit (C1 UFC class) — **NOT** NFL prospective `admit.py` T-7d/kickoff schema. Clock owns stamp under Conductor ADMIT GO; Variants forbidden. No orders. No score. No invented fills/PnL/depth/settled counts.

`admitted_at` = **`2026-09-25T04:37:47Z`** (live `date -u`; not backfilled)  
`stub_status` = **`PANEL_ADMITTED_Q6S5_KXMLBSPREAD_ONLY`**  
`clock_admit` = **`CLOCK_STAMPED_ADMIT_GO`**

### PASS [V]
| Check | Result |
|-------|--------|
| Kick sha256 | **PASS** `1e2be3720a90283fffccd04b602d0350591ccc0242204e477086aeccc0d4d95f` |
| Accept READY sha256 | **PASS** `96cb4632b2475a6819c5aa1d1bd2f7893de16309f6322a96271eaf0d7713ba8a` |
| Examiner READY sha256 | **PASS** `cb25d9a7aa65ea5bcbeaccab01fe27968542b78399e5049262f1e7ae296cead2` |
| Panel stub sha256 | **PASS** `c7f1f1f4ca263838c4600ed46db8f525b68efc5399a567bd60929d18d76803cc` == packets `Q6S5_KXMLBSPREAD_PANEL_STUB_2026-09-25.json` |
| Scout raw sha256 | **PASS** `80b52f47c836248d5869806d7f59617535e6b78258367ebe6045af4275fff7e7` |
| `admitted_at` pre-stamp | **null**; `stub_status` **NOT_ADMITTED** |
| `series_ticker` | **KXMLBSPREAD** only; 6 events / 12 markets |
| `pnl` / `results` | **null** (honest) |
| Rules | GET-only / no invent / `fee_cache_quadratic_x0.5_not_live_R1P1_until_Examiner` |
| Subset vs scout | **PASS** — first-6 lex events + lowest `floor_strike` per team-side; 12 markets **verbatim** |
| Markets verbatim scout | **PASS** all 12 tickers byte-equal to scout raw rows |
| Merge tip `f349ffa8…` | **[U]** git unavailable on box — claimed only; not invented |
| Occurrence near/past | **OK** for fee+queue measurement harness (not NFL T-7d refuse) |

### REFUSE [V]
| Gate | Stamp |
|------|-------|
| Variants / Conductor running admit | **REFUSED** — Clock owns |
| NFL `admit.py` T-7d validator on this schema | **REFUSED** — wrong tool |
| Live orders / Logan keys | **REFUSED** |
| Invent depth/fills/PnL/settled counts | **REFUSED** |
| Score / treat harness units as score | **REFUSED** — Examiner only after measured path |
| Claim fee CACHE×0.5 as live R1-P1 | **REFUSED** until Examiner `/series` pin (live GET observed quadratic×0.5 — still CACHE-LABELED) |
| Admit any series other than KXMLBSPREAD | **REFUSED** |
| Backfill / invent past timestamps | **REFUSED** |
| Lee-Ready | **N/A / REFUSED** — not applicable to this fee+queue measurement panel |

### Fee note
Fee remains **CACHE-LABELED quadratic×0.5** (≠ live R1-P1). Public `GET /series/KXMLBSPREAD` returned `fee_type=quadratic` `fee_multiplier=0.5` (HTTP 200) — recorded as observation only; **not** Examiner-pinned live R1-P1.

### GET freshness summary
| Route | HTTP | Note |
|-------|------|------|
| `GET /events?series_ticker=KXMLBSPREAD&status=open&limit=20` | **429** | honored; no invent expand |
| `GET /series/KXMLBSPREAD` | **200** | fee quadratic×0.5 observed; CACHE label retained |
| `GET /markets/…HOUATH-ATH2` | **200** | `finalized` / `result=no` — hygiene only; stub markets kept verbatim |
| `GET /markets/…PITDET-DET2` | **429** | honored |
| `GET /markets/…NYMWSH-NYM2` | **200** | `active` |

### Admit scope
- **Admitted:** `Q6S5_KXMLBSPREAD`
- **Explicitly not admitted:** S1_KXMLBGAME, C2_KXNHLGAME, C3_KXHIGHNY, C4_KXCPI, C5_KXBTC15M, R2_P3_PROP_SLATE, R3_P3_FL_MAKER_TAKER, R3_P4_L2_SHAPE, S4_KXNCAAFGAME, S5_KXMVECROSSCATEGORY, ADMIT_1_PROSPECTIVE, ATP_KXATPMATCH, ETH_KXETH15M, WEATHER_NOWCAST

### Next steps
1. **Collector** — durable public GET-only capture under `lab/astra-capture/q6s5-kxmlbspread/` (no orders; honor 429 shrink).
2. **Examiner** — scores **only after** measured path; READY NOT_SCORED remains until then; do not treat admit as score.
3. Keep fee CACHE-labeled until Examiner `/series` pin.
4. Isolation: do not reopen S1 ML / Cap-SR / Q6-000 / other panels via this stamp.

---

## Clock seal

**ADMIT PASS — Q6S5 KXMLBSPREAD ONLY.**  
`admitted_at=2026-09-25T04:37:47Z` · panel_admitted sha256 `e36de2d1ce6286dff90d25f2fae680170c8a469c443c1beed974ffe80383fba1` · stub sha256 `c7f1f1f4ca263838c4600ed46db8f525b68efc5399a567bd60929d18d76803cc` · production_claim=false · orders=false · scored=false.
