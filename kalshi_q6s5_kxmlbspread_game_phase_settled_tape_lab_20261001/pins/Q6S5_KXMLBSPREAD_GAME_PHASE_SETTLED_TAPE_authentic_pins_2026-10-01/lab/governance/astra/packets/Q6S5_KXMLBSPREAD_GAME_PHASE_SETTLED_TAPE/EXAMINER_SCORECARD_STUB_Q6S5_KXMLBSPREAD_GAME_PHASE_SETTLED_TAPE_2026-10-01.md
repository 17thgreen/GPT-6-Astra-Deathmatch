# EXAMINER SCORECARD STUB — Q6S5-KXMLBSPREAD-GAME-PHASE-SETTLED-TAPE (drafted by Variants; stamped 2026-10-01T19:20:29-04:00)

**Status:** FROZEN_AWAITING_ACCEPT · stub_ready=false · scored=false · verdict null · all metrics **null** (measured=false). Not an Examiner stamp.
**Template:** EXAMINER_KALSHI_SCORECARD_TEMPLATE v1.2 · sha256 `56bcf6269a42031d9d90496e9a65c2292321aed2165033f6fb44ff8cc4d6b1cc`
**Freeze:** sha256 `5beba803f3f6d33410409acc23ad3b782be62dc8829a0f54584e1da8ac18575a`
**Knob:** game_phase (print created_time vs scheduled first pitch from pinned rules_primary, cross-checked with event_ticker) ∈ {Q6S5GP0 pregame [open, start), Q6S5GP1 inplay [start, close_time)}
**Primary:** maker_gross_roi_delta_GP1_minus_GP0 (gross, fee-free) · **Secondary:** same delta within FL1 stratum (p_taker [0.20,0.80), registry `0860cbe2…` verbatim, no rebin; price_band held fixed, not re-measured); CACHE post-fee; LOEO/LOMO
**Stresses:** one_tick_worse · start_shift_plus_30m (stress only) · fees_2x (CACHE)
**Universe:** 6 finalized panel markets / 3 events (11,723 pinned prints; feasibility rows GP0 1,865 / GP1 9,852 / post-close 6 — counts, not results); 6 Sep-25 markets out of scope
**Evidence class:** IN_SAMPLE_DEV (per-row pre_admitted_at flag, strict < 2026-09-25T04:37:47Z; precedent ruling `09763030…`) · study label proposed "historical replay"
**Effective n:** 3 events / 6 markets · 4th knob on the same 3 events → multiplicity caveat; confirmatory test only on the untouched KXMLBSPREAD holdout
**Fee:** CACHE_NOT_R1P1 (FEE_PIN `9c0f3554…` formula_id absent) — not R1-P1; not "fee-honest"
**ADMIT-1 gap:** ruling `ac7cfe63…` pinned; window [2026-09-27T00:00Z, 2026-09-30T04:00Z) enforced; excluded_admit1_window_n null (expected 0)
**p16:** satisfied 8 / n/a 3 / missing 1 (item 12)
**simulated_fills:** n/a (no Astra fills) · counts_toward_keep=false · promote=false · verdict ceiling ITERATE
**Refuse:** invent fills/PnL/settlement_ts/first-pitch · public-counterparty return as Astra PnL · Lee-Ready · live orders · CACHE as R1-P1 · rebin · re-measure price_band/fill_model/analysis_slice · boundary move after outcomes · S1/Q6-000/Cap-SR/Q6S1 retune · Refiner · KEEP

Full null schema: `EMPTY_RESULTS.json` → `examiner_scorecard_v1_2`.
