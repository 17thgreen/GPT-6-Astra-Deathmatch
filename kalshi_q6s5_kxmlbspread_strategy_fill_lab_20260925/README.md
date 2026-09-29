# Q6S5 KXMLBSPREAD strategy-fill path

Measurement path for packet `Q6S5-KXMLBSPREAD-STRATEGY-FILL`.
One knob: `fill_model`. Implemented model: `public_trade_through_conservative`.
`mechanic_demo_observed` stays `UNAVAILABLE`.

Parent arms stay `Q6S5A0` `maker_vs_taker_native` and `Q6S5A1`
`content_fresh_vs_stale_bin`. Fee label `CACHE_NOT_R1P1` (quadratic,
multiplier 0.5, `formula_id` null). Simulated fills have
`counts_toward_keep` false. `results`, `pnl`, and arm ROI stay null.

Cited governance paths were absent at `origin/main` `cb8957d` and were
not recreated there. Vendored copies live in
`Q6S5_KXMLBSPREAD_STRATEGY_FILL/`. Fourteen pins re-hash.
`digest_all_match_claimed` is true. v2 bundle `739d81d6…` is the primary
authentic bundle. v1 `6602e07e…` is its subset. Measurement gaps stay
absent: Mechanic demo artifact, Examiner `formula_id`, 6 Sep-25
settlements, untouched evaluation period, and ADMIT-1 window data.

Examiner status is `HOLD_PRE_PR`. This lab does not mark READY.

```bash
python3 -m unittest discover -s tests -v
```

Code verification `python3 -m unittest discover -s tests -v`: Ran 14 tests in 0.023s at 2026-09-29T21:14:42Z. Result: OK. Failures: 0. Errors: 0. That run is not an Examiner score. `results`, `pnl`, and arm ROI stay null. The prior pre-pin run was 11 tests at 2026-09-29T21:04:24Z.
