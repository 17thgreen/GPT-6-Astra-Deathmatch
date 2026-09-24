# C1 KXUFCFIGHT settled-resolution join unit results

September 24, 2026. This file records a code check of the join-gate
harness. It is a unit verification. It is not a simulated trading run and
not live validation. `FROZEN_EXPERIMENT.json` still has `results` null
and `pnl` null. `results/EMPTY_RESULTS.json` still has `settled_join_n`,
`occurrence_match_n`, `admit_ready_flag`, `results`, and `pnl` null.
Those fields stay null on purpose. This page is not profit. No tape walk
was run. No P&L figure is reported. This is not an Examiner score.

## Command

From `kalshi_c1_kxufcfight_settled_join_lab_20260923`, Python 3, standard library:

```bash
python3 -m unittest -v tests.test_orchestrator
```

Ran 10 tests in 0.024s. Recorded at 2026-09-24T23:03:36Z. Result: OK.
Failures: 0. Errors: 0.

## What the checks cover

The panel parent copy matches `lab/astra-capture/c1-kxufcfight/panel_admitted.json`,
sha256 `24426d804c51bde23cf2557a11a8481a12026da10024094c4ae546d1f7d3956e`,
12396 bytes. Top-level `admitted_at` stays `2026-09-23T00:49:43Z`.
Per-market `admitted_at` stays null. The pre-admit stub stays sha256
`2cc661d86202d3daf9ffa45320e39d249852a97490f458f72ab7ea8ec5c81a00`.
The admit tool is refused.

J0 `nonempty_result_required` and J1 `occurrence_datetime_match` both
run on the four admitted parent seeds. Each market
`occurrence_datetime` equals its event clock. `occurrence_source` is
`live_get_market`. J1 does not invent `occurrence_datetime` and does not
substitute `expected_expiration_time`. A seed with `occurrence_datetime`
removed is refused. The scorecard fields stay null. Declared scout N=4
is not `settled_join_n`.

The cited freeze path, Conductor ACCEPT path, maximize pin
`MAXIMIZE_PIN_2026-09-23_1750ET.md`, and scout directory
`lab/governance/astra/packets/scout_c1_settled_rejoin_2026-09-23/` were
absent from `origin/main` at `a281adc944e4dacffcdb5677a140fabaed675a81`.
Regenerating the freeze is refused. Those bytes are present in this checkout.
`digest_all_match_claimed` is true. Cited freeze sha256
`3ea3362ad3c16951369d5f90497ec6079213dd54e5556340c4d3738744126cf1`
matches `lab/governance/astra/packets/C1_KXUFCFIGHT_SETTLED_RESOLUTION_JOIN_HARNESS_FREEZE_2026-09-23.md`.

Settled, finalized, and events list books are not written. Backfill is
refused. The four captured orderbooks stay sha256
`e07d09f130e604a9e1acfc736fb57cbdfc33d8a5a253466a0cbd5c98cf6c9f74`
with empty bid lists. Filling them is refused. Lee-Ready, live orders,
Logan keys, Cap-SR, FQ siblings, EMPTY-OB, C3-RJ, C5-RJ, R3P3-RJ,
NHL-RJ, S4-RJ, R2P3-RJ, S5-RJ, Arm B, and Q6-000 retune are refused.
S1, S2, and R2-P4 stay gated. Examiner status stays `HOLD_PRE_PR`.
`stub_ready` stays false.

## Limitation

This run does not load a scout reget. The join schema reads the admitted
panel's existing `result_observed_live_get` and `occurrence_datetime`.
It does not claim those reads are the absent scout file. If the cited
freeze, ACCEPT, maximize pin, and scout directory later appear together
and the ACCEPT says digests match, this revision still refuses to claim
ALL_MATCH until a follow-up wires those bytes. Absence is not a score.
