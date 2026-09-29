# Q6S5 KXMLBSPREAD strategy-fill path

Measurement path for packet `Q6S5-KXMLBSPREAD-STRATEGY-FILL`.
One knob: `fill_model`. Implemented model: `public_trade_through_conservative`.
`mechanic_demo_observed` stays `UNAVAILABLE`.

Parent arms stay `Q6S5A0` `maker_vs_taker_native` and `Q6S5A1`
`content_fresh_vs_stale_bin`. Fee label `CACHE_NOT_R1P1` (quadratic,
multiplier 0.5, `formula_id` null). Simulated fills have
`counts_toward_keep` false. `results`, `pnl`, and arm ROI stay null.

Conductor ACCEPT, freeze markdown, kick, and the
`Q6S5_KXMLBSPREAD_STRATEGY_FILL` packet bundle were absent at
`origin/main` `cb8957d` and were not recreated. `digest_all_match_claimed`
is false.

Examiner status is `HOLD_PRE_PR`. This lab does not mark READY.

```bash
python3 -m unittest -v tests.test_orchestrator
```

Code verification `python3 -m unittest -v tests.test_orchestrator`: Ran 11 tests in 0.007s at 2026-09-29T21:04:24Z. Result: OK. Failures: 0. Errors: 0. That run is not an Examiner score. `results`, `pnl`, and arm ROI stay null.
