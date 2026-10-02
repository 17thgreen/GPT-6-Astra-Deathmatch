# EXAMINER SCORECARD STUB: WX-FL-KXHIGH-SETTLED-TAPE (drafted by Variants; stamped 2026-10-01T19:46:31-04:00)

**Status:** FROZEN_AWAITING_ACCEPT · stub_ready=false · scored=false · verdict null · all metrics **null** (measured=false). Not an Examiner stamp.
**Template:** EXAMINER_KALSHI_SCORECARD_TEMPLATE v1.2 · sha256 `56bcf6269a42031d9d90496e9a65c2292321aed2165033f6fb44ff8cc4d6b1cc`
**Freeze:** sha256 `aec5b760f8539ea9f30aa1c3601534dccf78a62ee2026cb939842656e3c20e0f` · ruling `0e37f91b…` CLEARED_TO_FREEZE · implement base main `749bc146`
**Knob:** price_band of native taker side ∈ {WXFL0 [0,0.20), WXFL1 [0.20,0.80), WXFL2 [0.80,1.00]}, registry `0860cbe2…` verbatim, no rebin (= fb6540f5)
**Primary:** EW_delta_FL0_minus_FL1 (city-day-equal-weighted; Examiner 2e74f17b maker_gross_roi formula) · H2 EW_delta_FL2_minus_FL1 · **Secondary:** trade-weighted deltas · LOCDO / LODO / LOCO · all with and without Sep-25
**Reading rule:** fb6540f5 line 118 verbatim; event := city-day; ≥2 of 3 := ≥⌈2n/3⌉ of n LOCDO (8 → 6); KILL scope := 4 KXHIGH series
**Gap exclusion:** PRIMARY GM-LIT (flagged windows, all arms; expected 27,199 / 33,757 excluded, timestamp-only); sensitivities GM-COV (expected 0 excluded) and GM-LIT-PAD (counts only); per-arm counts computed by cloud
**Stresses:** one_tick_worse · fees_2x n/a
**Universe:** 48 finalized markets / 8 city-days (KXHIGH CHI/LAX/MIA/NY 26SEP24+26SEP25), 33,757 in-scope prints pre-exclusion (counts, not results)
**Evidence class:** IN_SAMPLE_DEV · study label proposed "historical replay" · **no pre_admitted_at flag possible (card02 admitted_at null)**
**Effective n:** 8 city-days · family_size 1 (WX-TTC not frozen)
**Fee:** CACHE_NOT_R1P1 label; gross only; net null (no KXHIGH FEE_PIN; no GET)
**ADMIT-1 gap:** ruling `ac7cfe63…`; window [2026-09-27T00:00Z, 2026-09-30T04:00Z); excluded_admit1_window_n null (expected 0)
**p16:** satisfied 8 / n/a 3 / missing 1 (item 12)
**simulated_fills:** n/a · counts_toward_keep=false · promote=false · verdict ceiling ITERATE · results/pnl null
**Refuse:** GETs · orders · admit.py · capture.sqlite · live weather db · Lee-Ready · rebin · Q6-000 retune · invent fills/PnL · CACHE as R1-P1 · mapping swap after outcomes · KEEP

Full null schema: `EMPTY_RESULTS.json` → `examiner_scorecard_v1_2`.
