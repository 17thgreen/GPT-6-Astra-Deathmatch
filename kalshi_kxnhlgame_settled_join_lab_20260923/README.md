# NHL KXNHLGAME settled-resolution join harness

Status: hypothesis committed in `EXPERIMENT_SPEC.md` before a unit
outcome. The unit page is `results/UNIT_RESULTS.md` after the code check
is recorded. `FROZEN_EXPERIMENT.json` keeps `results` and `pnl` null.
`results/EMPTY_RESULTS.json` keeps `results`, `pnl`, `settled_join_n`,
`occurrence_match_n`, and `admit_ready_flag` null.

This lab is measurement-only. Feature family NHL-RJ. The only knob is
`join_gate`: J0 `nonempty_result_required` and J1
`occurrence_datetime_match`. The scout pin says settled nonempty
`result` N=17. That pin is not `settled_join_n`. The series settled,
finalized, and open lists stay the honest 429 gaps. Parent SEP26 FQ
seeds stay active with an empty `result`. `admitted_at` on the parent
panel stub stays null. This lab does not run `admit.py`. This is
orthogonal to NHL-FQ. It is not a reopen of Cap-SR, C3-RJ, C5-RJ, or
R3P3-RJ.

Attached bytes are also at
`lab/governance/astra/packets/`,
`lab/astra-capture/c2-kxnhlgame/settled_reget_2026-09-23.json`,
`lab/astra-science/kalshi_kxnhlgame_settled_join_lab_20260923/`,
and `packets/NHL_KXNHLGAME_SETTLED_JOIN_HARNESS/`.
`SOURCE_PINS.json` lists the digests. It does not contain the file
bytes.

- Freeze sha256 `d1f71cea6df8f6c5a9fac6f9d1aa418ce61aa650794f22b400a01c4f3fd45810`
- Scout reget sha256 `99a7f90564ee2150f5edef4efafb7ccb954b87036e0b43f29ff7dc6ed104706f`
- Seed summary sha256 `794e148df5927c64d08b4578b47a7453589f02872af65880922bcb9273194a1a`
- Panel stub sha256 `60d183e7bdcf25adbc94eeeb3bb361b5232c19c0fe3e6a115f45ab3fcb100c79` (`2026-09-23.c2-kxnhlgame-v0`, `admitted_at` null)
- Settled reget sha256 `8d597578bc65ea14ab1cbf5aa3c6d121d61431078a755b8419c815aa1d354df0`
- Accept sha256 `ce82d9347c8af6666d96fb5c63be7693f4672306639ce4ba2360ba231c01e698`

Feebook and rails commits are fixed path pins and are not imported.
No fee arm. No live orders. No Logan keys.

From this directory, Python 3 standard library:

```bash
python3 -m unittest -v tests.test_orchestrator
```

No Logan keys. No live orders. A passing unit run is not an Examiner score.
