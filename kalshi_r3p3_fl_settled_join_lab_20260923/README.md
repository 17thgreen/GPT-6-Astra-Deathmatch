# R3-P3 FL maker/taker settled-resolution join harness

Status: hypothesis committed, then source frozen. The unit page is
`results/UNIT_RESULTS.md`. `python3 -m unittest -v tests.test_orchestrator`
ran 10 tests in 0.129s. Recorded at 2026-09-23T19:53:37Z. Result: OK.
Failures: 0. Errors: 0. That page is not profit and not an Examiner pass.
`EXPERIMENT_SPEC.md` is the hypothesis. `FROZEN_EXPERIMENT.json` keeps
`results` and `pnl` null. `results/EMPTY_RESULTS.json` keeps `results`,
`pnl`, `settled_join_n`, `occurrence_match_n`, and `admit_ready_flag`
null.

This lab is measurement-only. Feature family R3P3-RJ. The only knob is
`join_gate`: J0 `nonempty_result_required` and J1
`occurrence_datetime_match`. The scout pin says settled nonempty
`result` N=20. That pin is not `settled_join_n`. The CHI settled list
and the NY open list stay the honest 429 gaps. Parent seeds
`KXHIGHNY-26SEP22-B67.5`, `KXHIGHNY-26SEP22-T70`, and
`KXHIGHCHI-26SEP22-B64.5` are finalized with nonempty `result` on the
authentic reget. `admitted_at` on the parent panel stub stays null.
This lab does not run `admit.py`. This is not a reopen of the R3-P3
fee arms and it is not a reopen of C3-RJ.

`lab/governance/astra/packets/scout_r3p3_settled_rejoin_2026-09-23/` is
not in this checkout. Attached bytes are in this directory.
`SOURCE_PINS.json` lists the digests. It does not contain the file
bytes.

- Freeze sha256 `7fcfc36ab4761e2dec56018b498372fb63c402f2582fe848e8775e28f9b720b9`
- Scout reget sha256 `f675d7c40ccad37173b2cb54837349cd3053b7b76606c43efba5759a1bde551f`
- Seed summary sha256 `b43d4ab065b712f5bf1b87eb164bccb00e8e9993f97db9d86a8d1619ce9ec13d`
- Panel stub sha256 `6f640dd3a6091ba6b896ded38fdded4676583aa3c885223da21ddf03780250c0` (`2026-09-22.r3-p3-fl-maker-taker-v0`, `admitted_at` null)
- Settled reget sha256 `c5f680e4ff66af67691672c4b8c43eb57906f25b4d79fdeb65f61e031c13efda`
- Accept sha256 `a6434fe4854b850df24a0a081168ba5d90d4646ba9a409418d7b874262a5fa9c`

Feebook and rails commits are fixed path pins and are not imported.
No fee arm. No live orders. No Logan keys.

From this directory, Python 3.12 standard library:

```bash
python3 -m unittest -v tests.test_orchestrator
```

No Logan keys. No live orders. A passing unit run is not an Examiner score.
