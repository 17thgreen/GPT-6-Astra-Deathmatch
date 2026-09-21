# NFL maker REST replay, round 2

This package extends the previous artifact audit into a runnable, independently implemented research replay. It includes a fixed cohort's public Kalshi trade and bid/ask candle captures. No account credentials or order-placement code are present.

Start with `NFL_Maker_REST_Replay_Results.md` for measured outcomes and limitations. Read `EXPERIMENT_SPEC.md` for assumptions frozen before the runs. The cohort is all sixteen NFL games in season 2026 week one, already seen in repository research; it is not an untouched holdout.

## Run with the captured public data

Python 3.12 is the tested environment. The new replay and collectors use the standard library. The optional unchanged comparator also needs NumPy and pandas; versions are recorded in `requirements.txt`.

```bash
python -m unittest discover -s . -p test_replay_v2.py -v
python run_suite.py
python run_candle_suite.py
python run_post_diagnostics.py
python quote_source_audit.py
```

The suites verify captured-file hashes and require the entire fixed cohort. They write all results under `results/`. The print suite launches three worker processes; the candle suite launches two. Both can be run sequentially as shown.

`run_post_diagnostics.py` runs the explicitly post-result checks described in `POST_RESULT_DIAGNOSTICS.md`. `quote_source_audit.py` compares print proxies with candle closes ex post and never supplies a trading signal.

To rerun the unchanged repository comparator, first restore its private sources from your authenticated clone or GitHub CLI:

```bash
python -m pip install -r requirements.txt
python fetch_sources.py --repo-root /absolute/path/to/your/clone
python run_suite.py --legacy
```

Alternatively use `python fetch_sources.py` with an already authenticated GitHub CLI. It reads and verifies eight source inputs pinned to `f4ad8e8bfba2db2a5e8e1ecf80f935424f60f175`. Those files are not duplicated in this archive. The latest reviewed head, `0217e505202813ce724ff5898d1343b4770ef8e3`, changed the strategy board and added a weather calibration study; it did not change the comparator's maker code.

## Recapture public REST data

The captures in this package are the inputs used for the reported results. Re-fetching can yield different records if the provider revises history. Preserve the included captures when comparing runs.

```bash
python collect_public.py
python collect_postlude.py
python collect_candles.py
```

Collectors reuse completed, hash-verified files. The first requests the exact seven-day-to-three-hour window with exhausted pagination and excludes block trades. The second adds five minutes after the cutoff so the unchanged legacy engine can encounter a trade that triggers its stop rule. The third captures historical one-minute closing bid/ask observations. Sparse candle minutes remain missing. REST collection requires network access but no Kalshi API key.

`record_public_books.py --events EVENT_TICKER --polls 1` records current public depth with request and receipt timestamps. It was exercised on the next two eligible NFL events; those snapshots are included separately and are not used to set historical queue values. No recording process is left running.

## What the new replay fixes

- Scheduled stop/cancel/close events run even if no trade arrives.
- Pending orders reserve shared cash and joint event exposure until cancellation is acknowledged.
- Same-price reductions take effect after the assumed acknowledgment delay. Increasing size does not receive free time priority.
- Maker fees accumulate across an order's fills with explicit balance precision and fixed-point inputs.
- Invalid or stale quote sources trigger cancellation; each inferred side has its own age.
- Exit depth is a total game budget, so sibling markets do not silently double available liquidity.
- Missing or incomplete exits remain unresolved. No final-profit number is emitted unless every game window is complete and all inventory is flat.

## Material limitations

This is a sensitivity model. Print-derived bid/ask values are proxies. Candle closes are historical quote observations, but their publication delay is assumed to be sixty seconds; intraminute high/low values are not used. Historical queue positions, book depth, cancellation acknowledgment times, fill receipt times and the bot's own market impact are unobserved.

The model uses the repository's queue snapshot profile or declared alternatives. It is not estimating historical queue depth from the candles. Hypothetical fills consume public trade volume and retain same-price queue progress, under a 50% participation assumption. Displayed prices alone do not prove this order could have executed.

Only two-team MECNET events with the captured tie rule are admitted. Payoff equivalence and immediate collateral recycling remain model assumptions consistent with the recovered metadata; this package does not implement the exchange's full collateral engine or cancellation/postponement settlement rules. The supported quantity increment is .01 contracts and prices are normalized to four decimal places; these captures identify a one-cent price grid.

The inventory-direction candidate stops posting into the current exposure direction and requests cancellation of such resting orders. Offset orders may overshoot zero, and orders pending cancellation can still fill. It is not a guaranteed reduce-only exchange order or a fitted pair-completion model.

Terminal payout bounds value unresolved contracts between $0 and $1 before any future exit fee. They are neither confidence intervals nor achieved returns. Each game contributes one outcome; hundreds of thousands of prints do not create hundreds of thousands of independent sporting outcomes.
