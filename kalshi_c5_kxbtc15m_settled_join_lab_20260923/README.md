# C5 KXBTC15M settled-resolution join harness

Status: hypothesis committed. The unit page is not recorded yet.
`EXPERIMENT_SPEC.md` is the hypothesis. `FROZEN_EXPERIMENT.json` keeps
`results` and `pnl` null. `results/EMPTY_RESULTS.json` keeps `results`,
`pnl`, `settled_join_n`, `occurrence_match_n`, and `admit_ready_flag`
null.

This lab is measurement-only. Feature family C5-RJ. The only knob is
`join_gate`: J0 `nonempty_result_required` and J1
`occurrence_datetime_match`. The scout pin says settled nonempty
`result` N=20. That pin is not `settled_join_n`. Finalized and closed
list filters stay the honest 429 gaps. Parent seed
`KXBTC15M-26SEP222045-45` is finalized `result` `no` on the authentic
reget. `admitted_at` on the parent panel stub stays null. This lab does
not run `admit.py`. This is not live crypto trading.

`lab/governance/astra/packets/scout_c5_settled_rejoin_2026-09-23/` is
not in this checkout. Attached bytes are in this directory.
`SOURCE_PINS.json` lists the digests. It does not contain the file
bytes.

- Freeze sha256 `7f4b36eca39d43ee7403628c2e525d5980fa40bcfc906550c7f00bb06ffd4f21`
- Scout reget sha256 `7be17c44aef31abf7a0ab94938d0289f8766670ddacefdec566735818e044796`
- Seed summary sha256 `b39c919809f709bcb81ff10a3d983b266bc7a1303c0de502c7c20be726415198`
- Panel stub sha256 `60f613e8d775b66b9044ad31d2faf77bba84176f214a7bce599aa7a65b6905f8` (`2026-09-22.c5-kxbtc15m-v0`, `admitted_at` null)
- Settled reget sha256 `319d6d3e394089fd21fefbfaa52c58166e78c2d781077a3f876331d2c54de617`
- Accept sha256 `e116bbcb5f9518e6008ef412c8ff212a3170d0e3f26eb978f07a204b327aba7d`

Feebook and rails commits are fixed path pins and are not imported.
No fee arm. No live orders. No Logan keys.

From this directory, Python 3.12 standard library:

```bash
python3 -m unittest -v tests.test_orchestrator
```

No Logan keys. No live orders. A passing unit run is not an Examiner score.
