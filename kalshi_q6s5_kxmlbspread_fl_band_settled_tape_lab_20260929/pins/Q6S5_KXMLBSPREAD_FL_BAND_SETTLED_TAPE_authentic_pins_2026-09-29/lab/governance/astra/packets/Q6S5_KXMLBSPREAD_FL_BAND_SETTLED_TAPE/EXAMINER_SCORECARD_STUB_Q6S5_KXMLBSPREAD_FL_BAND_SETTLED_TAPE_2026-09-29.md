# EXAMINER SCORECARD STUB — Q6S5-KXMLBSPREAD-FL-BAND-SETTLED-TAPE (drafted by Variants; stamped 2026-09-29T17:26:35-04:00)

**Status:** FROZEN_AWAITING_ACCEPT · stub_ready=false · scored=false · verdict null · all metrics **null** (measured=false). Not an Examiner stamp.
**Template:** EXAMINER_KALSHI_SCORECARD_TEMPLATE v1.2 · sha256 `56bcf6269a42031d9d90496e9a65c2292321aed2165033f6fb44ff8cc4d6b1cc`
**Freeze:** sha256 `fb6540f52ed5f819ccf6e80bf0cf7eb6d951e065416b9d550fead0c6d06043fa`
**Knob:** price_band (taker-purchased-side price, R3-P3 registry `0860cbe2…`) ∈ {Q6S5FL0 longshot_taker [0,0.20), Q6S5FL1 mid [0.20,0.80), Q6S5FL2 favorite_taker [0.80,1.00]}
**Primary:** maker_gross_roi_delta_FL0_minus_FL1 (gross, fee-free) · **Secondary:** FL2−FL1; CACHE post-fee; per-band; LOEO/LOMO
**Universe:** 6 finalized panel markets / 3 events (11,723 pinned prints per Collector metadata); 6 Sep-25 markets out of scope (close_time in ADMIT-1 window)
**Fee:** CACHE_NOT_R1P1 (FEE_PIN `9c0f3554…` formula_id absent) — not R1-P1; not "fee-honest"
**ADMIT-1 gap:** ruling `ac7cfe63…` pinned; window [2026-09-27T00:00Z, 2026-09-30T04:00Z) enforced; excluded_admit1_window_n null
**p16:** satisfied 8 / n/a 3 / missing 1 (item 12)
**simulated_fills:** n/a (no Astra fills) · counts_toward_keep=false · verdict ceiling ITERATE
**Refuse:** invent fills/PnL/settlement_ts · public-counterparty return as Astra PnL · Lee-Ready · live orders · CACHE as R1-P1 · paper EV as evidence · rebin · S1/Q6-000/Cap-SR/Q6S1 retune · Refiner · KEEP

Full null schema: `EMPTY_RESULTS.json` → `examiner_scorecard_v1_2`.
