# R3-P3 FL maker/taker bands harness unit results

September 23, 2026. This file records a code check of the frozen analysis-slice
harness. It is a unit verification. It is not a simulated trading run and
not live validation. `FROZEN_EXPERIMENT.json` still has `results: null` and
`pnl: null`. `results/EMPTY_RESULTS.json` still has `mz_alpha`, `mz_psi`,
`post_fee_roi_by_band`, `maker_vs_taker_roi_delta`, and `settled_join_n`
null. Those fields stay null on purpose. This page is not profit, and it is
not folded back into the freeze hashes. No tape walk was run. No P&L figure
is reported. This is not an Examiner pass and not a live-order certification.
Lee-Ready stays refused. Paper EV stays a hypothesis.

## Command

From `kalshi_r3p3_fl_maker_taker_lab_20260923`, Python 3.12.3, standard
library:

```bash
python3 -m unittest -v tests.test_orchestrator
```

Ran 8 tests in 0.045s at 2026-09-23T14:27:43Z. Result: OK. Failures: 0.
Errors: 0.

The checks that passed are the predeclared ones: fee pin
`22371178cb2663250b4762f328069571c48cb551` and rails pin
`6a28e0d6254327ea4e6451c781bec56215ac6cac` with those trees unchanged since
those commits; packet sha256
`fbc58539b7a469d005b7f75b786efddecc1028a3bb0da601bc0082c9d4aab179`; parent
kernel sha256
`0ed697149136acb3aa840aeeb79d11c8f6ef80f37ce4dd692a3cb690212206a7`; panel
stub `2026-09-22.r3-p3-fl-maker-taker-v0` sha256
`6f640dd3a6091ba6b896ded38fdded4676583aa3c885223da21ddf03780250c0` with
`admitted_at` null and 15 trades; bands registry sha256
`0860cbe28d28ecc6142ddf6f1ebb67792084264ed82e0b4d868c3b3138ea5312`;
preference for a temporary `panel_admitted.json` when that file exists;
R3P3A0 native taker partitions and R3P3A1 band membership with the five
instrument fields null; a synthetic band stand-in that does not change
freeze bytes; refusal of paper EV, Lee-Ready, live-order, and invented
settlement labels; refusal of a non-GET verb and of `execution_adapter`.

An earlier local run, before commit `b66500d`, failed one test:
`test_native_partition_and_band_membership_keep_roi_null` raised
`KeyError: aggressor_inference` because band rows omitted that flag.
The fix records `aggressor_inference` null on every band row. This page
is the rerun after that commit. The failure was a schema omission. It was
not a scored ROI.

## What the run kept null

`fee_source` is feebook. The in-memory `order_fee` probe checks
`astra.r1p1.feebook.claude_order_level_ceil.v1`. `numeric_fee_stored` is
false. The probe fee is not copied into `post_fee_roi_by_band` or
`maker_vs_taker_roi_delta`. Rails supplies the fee-credit rule id only.
Freshness is not a scorecard field.

On the stub, R3P3A0 partitions are `no`/`ask` (13 trades) and `yes`/`bid`
(2 trades). R3P3A1 assigns 5 trades at yes price `0.0100` to b00 and 10
trades at `0.9800` or `0.9900` to b09. Bands b01 through b08 have
`trade_n` 0. That empty membership is not a ROI of zero.
`panel_settled_markets_resolved_n` on the report echoes the stub cohort
count 0. `settled_join` is an empty list. `settled_join_n` on the scorecard
stays null.

C3, C5, and the other paths in `DOES_NOT_MODIFY` match
`637644966bae3737b52ab35826d3a63bf4b9b936`. C3 and C5 `results` and `pnl`
remain null.

## Limitations

- The stub has no trades in bands b01 through b08. Membership there is
  exercised by `fixtures/synthetic_trades.json`, source
  `synthetic_schema_standin`. That file is not a Kalshi GET and not an
  admitted cohort.
- Band edges checked in memory: `0` and `0.0999` are b00, `0.10` is b01,
  `0.50` is b05, `0.8999` is b08, `0.90` and `1` are b09. Prices outside
  `[0, 1]` are refused. The cuts are the pre-registered registry. They were
  not fit to a PnL.
- The maker-versus-taker arm records native `taker_outcome_side` and
  `taker_book_side` only. It does not invent a maker aggressor label.
  `infer_aggressor` raises. Lee-Ready is refused.
- `panel_admitted.json` is absent. `admitted_at` on the stub is null.
  Clock admit is still closed, so Examiner scoring stays closed. This run
  does not execute `admit.py`.
- The stub cohort resolved-market count is 0 because the seed markets are
  pre-settlement. That fact is not a fill of `settled_join_n`.
- No public GET was issued. No Logan key was read. No order route exists
  in this lab.
- `lab/governance/astra/packets/` is absent. The packet bytes used here are
  the copies under the lab and under `packets/R3_P3_FL_MAKER_TAKER_HARNESS/`.
- C3 weather preference on the stub stays a cite. This run does not merge
  kernels and does not edit the C3 or C5 labs.
- No Q6-`000` retune. No queue-fragility reopen. `queue_fragility` is not
  imported.

## PR15 absorption rerun

Draft PR15 (https://github.com/17thgreen/GPT-6-Astra-Deathmatch/pull/15)
stays a separate draft scaffold. This lab does not create
`kalshi_r3_p3_fl_maker_taker_lab_20260922/`. The kernels are not
dual-maintained.

From the same directory, after that absorption was committed:

```bash
python3 -m unittest -v tests.test_orchestrator tests.test_pr15_absorption
```

Ran 14 tests in 0.049s at 2026-09-23T14:34:35Z. Result: OK. Failures: 0.
Errors: 0. Python 3.12.3.

The added checks are native `taker_*` agreement, `lee_ready` raising on
every sample, `RebinRefused` when an outcome is passed to `assign_band`,
an in-memory schema sheet that joins three rows and refuses two, and null
`MZ` and `band_roi`. Imported `order_fee` quotes on that sheet are not
copied into `FROZEN_EXPERIMENT.json` or `results/EMPTY_RESULTS.json`.
`results` and `pnl` stayed null. `mz_alpha` and `post_fee_roi_by_band`
stayed null.
