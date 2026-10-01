# Examiner scorecard STUB — R3-P3-FL-MAKER-TAKER

**Seat:** Examiner (Kalshi)  
**Packet:** R3-P3-FL-MAKER-TAKER  
**Subject:** Maker/Taker + favorite–longshot bands (MZ / post-fee ROI by 10¢ band)  
**Freeze:** `lab/governance/astra/packets/R3-P3_FL_MAKER_TAKER_BANDS_FREEZE_KERNEL_2026-09-22.md`  
**Panel stub:** `lab/governance/astra/packets/R3_P3_FL_MAKER_TAKER_PANEL_STUB_2026-09-22.json` (READY; `admitted_at` **null**)  
**Panel status:** `lab/governance/astra/packets/R3_P3_FL_MAKER_TAKER_PANEL_STUB_STATUS_2026-09-22.md`  
**Stub dir:** `lab/governance/astra/packets/r3_p3_fl_maker_taker/`  
**Adversary refuse:** `lab/governance/astra/packets/R3-P3_ADVERSARY_REFUSE_BIND_2026-09-22.md`  
**Status:** **NOT_SCORED** — settled N=0 at stub; MZ / ROI / pnl **null** until Clock admit + units  
**Authority:** Working Plan v0.1 · `lab/governance/astra/seats/EXAMINER_KALSHI.md`

---

## Verdict (placeholder)

| Subject | Stamp |
|---|---|
| Measurement packet | **NOT_SCORED** |
| Paper +2.6% maker ≥50¢ | **HYPOTHESIS ONLY** (not Astra EV) |
| Incumbent Q6-`000` | **untouched** |
| Live promotion / orders | **DENIED** |

**Desk headline:** Panel stub READY owned — refuse any score while settled N=0 or any MZ/ROI/pnl non-null without Clock admit.

---

## Gates (pre-score checklist)

| Gate | Result | Notes |
|---|---|---|
| Freeze before outcomes | **PASS** | results/pnl null at freeze |
| Panel stub schema | **PASS** | READY; not admitted |
| Settled panel N > 0 | **FAIL / BLOCKED** | settled markets resolved = **0** (429 on settled lists) |
| Clock admit | **PENDING** | `admitted_at` null; do not run admit.py from Examiner |
| Units / Polars join | **PENDING** | Simulator |
| Fee channel = R1-P1 | **REQUIRED** | @ `22371178…` · `formula_id` `astra.r1p1.feebook.claude_order_level_ceil.v1` |
| Native taker fields only | **REQUIRED** | refuse Lee-Ready |
| Bands pre-registered | **PASS at stub** | 10¢ registry before outcome join |
| Completed PnL non-null | **null** | Not run |

---

## Metrics (null — mandatory)

| Metric | Value |
|---|---|
| `results` / `pnl` | **null** |
| `completed_strategy_pnl` | **null** |
| MZ regression (`Y-P=α+ψP`) | **null** |
| post-fee ROI by 10¢ band | **null** |
| maker vs taker slice | **null** |
| `settled_n` | **0** at panel stub |
| `fee_channel_id` | pin required: R1-P1 @ `22371178…` |
| `knob` | `fl_maker_taker_bands_mz_roi` |

---

## Examiner ownership ack (2026-09-22 ET) — panel stub READY OWN

**Owner:** Examiner (Kalshi). Panel stub READY accepted as **NOT_SCORED**.

### ScorecardPromotionRefused / score refuse if

1. **Settled N=0** — any score while settled panel N remains 0.  
2. **Any MZ / ROI / pnl non-null** without Clock admit (`admitted_at` set) + Examiner-ready.  
3. **Paper +2.6%** (or any author-wallet EV) treated as Astra evidence — stays **hypothesis only**.  
4. **Lee-Ready** / non-native aggressor inference.  
5. Invented fills, PnL, or band expectancy from Collector live-GET stubs or empty results.  
6. Fee-honest ROI without R1-P1 pin.  
7. Q6-`000` retune / promote / live orders.

**Standing binds:** R2-P5 · R1-P1 formula_id · R1-P5 rails · R3-P3 Adversary refuse · R3 suite refuse.

**Empty results:** `lab/governance/astra/packets/r3_p3_fl_maker_taker/results.json`  
**Stub READY filed-at:** `2026-09-22T20:21:11-04:00` ET


---

---

## PR23 harness landed — Examiner stub READY NOT_SCORED (2026-09-23 ET)

**Harness:** `kalshi_r3p3_fl_maker_taker_lab_20260923/` landed **main** via **PR23** @`cfd5f95a…` (**SUPERSEDES** closed #15).
**Harness freeze:** `lab/governance/astra/packets/R3_P3_FL_MAKER_TAKER_HARNESS_FREEZE_2026-09-23.md` sha256 `fbc58539b7a469d005b7f75b786efddecc1028a3bb0da601bc0082c9d4aab179`
**Arms:** **R3P3A0** (maker_vs_taker) · **R3P3A1** (fl_bands_10c)
**Lee-Ready:** **REFUSED** (native taker fields only)
**Panel:** stub READY; `admitted_at` **null**; settled N=**0** on stub

**Examiner status:** **READY** as scorecard stub · measurement status **NOT_SCORED**.
**results / pnl / MZ / band_roi / settled_join_n:** all **null**.

### ScorecardPromotionRefused if
1. Invent MZ / band ROI / maker-taker ROI from harness units alone.
2. **Lee-Ready** invent / non-native aggressor inference.
3. **Fee copy** onto freeze scorecard (R1-P1 pin only; no fee literals onto scorecard before Examiner-ready).
4. Non-null `settled_join_n` derived from stub `settled_n=0` (honest zero stays zero; do not invent join count).
5. KEEP/ITERATE/KILL / promotion / paper +2.6% as Astra EV before Clock admit + Examiner-ready.
6. Q6-`000` retune / live orders.

**Score gate:** Clock admit (`admitted_at` set) + real settled join N>0 + Examiner-ready declaration — then score.
**Empty results:** `lab/governance/astra/packets/r3_p3_fl_maker_taker/results.json` · harness `R3_P3_FL_MAKER_TAKER_HARNESS/EMPTY_RESULTS.json`
**Stub READY (PR23) stamped-at:** `2026-09-23T10:36:49-04:00` ET
