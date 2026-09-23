# S4 KXNCAAFGAME settled-resolution join harness

Status: hypothesis committed, then source frozen. The unit page is
`results/UNIT_RESULTS.md`. `python3 -m unittest -v tests.test_orchestrator`
ran 10 tests in 0.237s. Recorded at 2026-09-23T20:54:36Z. Result: OK.
Failures: 0. Errors: 0. That page is not profit and not an Examiner pass.
`EXPERIMENT_SPEC.md` is the hypothesis.
`FROZEN_EXPERIMENT.json` keeps `results` and `pnl` null.
`results/EMPTY_RESULTS.json` keeps `results`, `pnl`, `settled_join_n`,
`occurrence_match_n`, and `admit_ready_flag` null.

This lab is measurement-only. Feature family S4-RJ. The only knob is
`join_gate`: J0 `nonempty_result_required` and J1
`occurrence_datetime_match`. The scout pin says settled nonempty
`result` N=18. That pin is not `settled_join_n`. The series settled,
finalized, and open lists stay the honest 429 gaps. Named event and
market GET gaps stay gaps. Parent SEP26 FQ seeds stay active with a
null `result`. The reget does not carry `occurrence_datetime` for those
seeds. `admitted_at` on the parent panel stub stays null. This lab does
not run `admit.py`. This is orthogonal to S4-FQ and NCAAF-FQ. It is not
a reopen of Cap-SR, C3-RJ, C5-RJ, R3P3-RJ, or NHL-RJ.

Attached bytes are also at
`lab/governance/astra/packets/`,
`lab/astra-capture/s4-kxncaafgame/settled_reget_2026-09-23.json`,
`lab/astra-science/kalshi_kxncaafgame_settled_join_lab_20260923/`,
and `packets/S4_KXNCAAFGAME_SETTLED_JOIN_HARNESS/`.
`SOURCE_PINS.json` lists the digests. It does not contain the file
bytes.

- Freeze sha256 `3a8e8ba52edd6acdc342c6a2faabb08665fe8a7a76e1b28af1c8e18850b03d99`
- Scout reget sha256 `57fa0b28325ac13015f49521a87661b3cc064d22a13cf960f4fcdfd9badaa3dc`
- Seed summary sha256 `9e67cd16f3ec6536d5dae3fe07de6e6b073c1c8d1adc9bb7e9297090ef567ce1`
- Panel stub sha256 `38167d11da5842bc4d39e6e7dcaab20a67294c735ba14d8bbeafde3154c6342a` (`2026-09-22.s4-kxncaafgame-v0`, `admitted_at` null)
- Settled reget sha256 `5bb0acfaa429e2ec1ad22e2e35e296540ac5b8e66eba4df6a0b2419d43257528`
- Accept sha256 `87bb8d44e8ac50099cc66d0469dcd4a5cfafb78d92dd24e7a218100a6254da4a`

Feebook and rails commits are fixed path pins and are not imported.
No fee arm. No live orders. No Logan keys.

From this directory, Python 3 standard library:

```bash
python3 -m unittest -v tests.test_orchestrator
```

No Logan keys. No live orders. A passing unit run is not an Examiner score.
