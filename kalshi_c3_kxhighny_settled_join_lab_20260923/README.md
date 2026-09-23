# C3 KXHIGHNY settled-resolution join harness

Status: hypothesis committed, then source frozen. The unit page is
`results/UNIT_RESULTS.md`. `python3 -m unittest -v tests.test_orchestrator`
ran 10 tests in 0.086s. Recorded at 2026-09-23T19:12:16Z. Result: OK.
Failures: 0. Errors: 0. That page is not profit and not an Examiner pass.
`EXPERIMENT_SPEC.md` is the hypothesis. `FROZEN_EXPERIMENT.json` keeps
`results` and `pnl` null. `results/EMPTY_RESULTS.json` keeps `results`,
`pnl`, `settled_join_n`, `occurrence_match_n`, and `admit_ready_flag`
null.

This lab is measurement-only. Feature family C3-RJ. The only knob is
`join_gate`: J0 `nonempty_result_required` and J1
`occurrence_datetime_match`. The scout pin says settled nonempty
`result` N=4. That pin is not `settled_join_n`. CHI
`KXHIGHCHI-26SEP22-B66.5` stays the honest 429 gap. `admitted_at` on the
parent panel stub stays null. This lab does not run `admit.py`.

`lab/governance/astra/` is not in this checkout. Attached bytes are in
this directory. `SOURCE_PINS.json` lists the digests. It does not
contain the file bytes.

- Freeze sha256 `56adcf592239b028aaa8bcffbf09815115b8454f78db39b43c578e64c160a4d5`
- Scout reget sha256 `e8950352745007d3cb565050161430807fa5de70d15321bb00bede6ca9ac18ee`
- Seed summary sha256 `b32bbf3200649bcea4fb61a98a4869d5123060a57702a9327262cccbc8e1ca93`
- Panel stub sha256 `2a5da7fe85ca1adc6b7c4dcf9e09ed5c6bb62be6b5c9b42731e36e31d1e8dfea` (`2026-09-22.c3-kxhighny-v0`, `admitted_at` null)
- Settled reget sha256 `0055faae508ba034eb49a12d52713566cbfe20bfbfbd2a16203ef350152ac24a`
- Accept sha256 `9adb77ed01fd9ccb894564efa9d5534d2edf189365ca0852fff49dafd3598d69`

Feebook and rails commits are fixed path pins and are not imported.
No fee arm. No live orders. No Logan keys.

From this directory, Python 3.12 standard library:

```bash
python3 -m unittest -v tests.test_orchestrator
```

No Logan keys. No live orders. A passing unit run is not an Examiner score.
