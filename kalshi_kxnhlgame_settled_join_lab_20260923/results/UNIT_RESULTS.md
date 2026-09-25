# NHL KXNHLGAME settled-resolution join unit results

September 23, 2026. This file records a code check of the frozen join-gate
harness. It is a unit verification. It is not a simulated trading run and
not live validation. `FROZEN_EXPERIMENT.json` still has `results: null` and
`pnl: null`. `results/EMPTY_RESULTS.json` still has `settled_join_n`,
`occurrence_match_n`, `admit_ready_flag`, `results`, and `pnl` null. Those
fields stay null on purpose. This page is not profit, and it is not folded
back into the freeze hashes. No tape walk was run. No P&L figure is
reported. This is not an Examiner score and not a live-order
certification.

## Command

From `kalshi_kxnhlgame_settled_join_lab_20260923`, Python 3.12, standard library:

```bash
python3 -m unittest -v tests.test_orchestrator
```

Ran 10 tests in 0.161s. Recorded at 2026-09-23T20:26:12Z. Result: OK.
Failures: 0. Errors: 0.

The checks that passed are the predeclared ones: freeze, scout reget,
seed summary, panel stub, settled reget, accept, frozen experiment, and
empty-results digests recorded in `orchestrator.py` and `SOURCE_PINS.json`;
`admitted_at` null on the stub; refusal of `panel_admitted.json` and of a
stub copy that sets `admitted_at`; J0 and J1 schema on the authentic reget
with the scorecard fields null; the series settled/finalized/open list and
the events settled list left as `429_honest` without a backfilled market
object; seventeen overnight SEP22 single-market GETs finalized with
nonempty official `result` (`yes` 8, `no` 9) while each panel stub
`result` stays empty; parent SEP26 seeds stay active with an empty
`result` and finalized nonempty count 0; Lee-Ready refused; refusal of
live orders, Logan keys, invented results, invented depth, invented fills,
a list-429 backfill, an invented parent SEP26 settlement, an invented
`occurrence_datetime`, `admit.py`, an Examiner-ready claim, an S1 / S2 /
R2-P4 ungate, copying scout N into `settled_join_n`, and Cap-SR / FQ /
NHL-FQ / C3-RJ / C5-RJ / R3P3-RJ / Arm B reopen.

Feebook and rails were not imported. Their pinned commits
`22371178cb2663250b4762f328069571c48cb551` and
`6a28e0d6254327ea4e6451c781bec56215ac6cac` are unchanged. The scout pin
`settled_nonempty_result_N` is 17 and was not copied into `settled_join_n`.
The seventeen settled rows share `occurrence_datetime` across the scout,
the seed summary, and the reget. That list is not `occurrence_match_n`.
Four reget parent rows stay active with an empty `result` and match the
panel occurrence. They are not settled-join markets.

## Pins verified on this branch

- harness freeze `d1f71cea6df8f6c5a9fac6f9d1aa418ce61aa650794f22b400a01c4f3fd45810`
- scout reget `99a7f90564ee2150f5edef4efafb7ccb954b87036e0b43f29ff7dc6ed104706f`
- seed summary `794e148df5927c64d08b4578b47a7453589f02872af65880922bcb9273194a1a`
- panel stub `60d183e7bdcf25adbc94eeeb3bb361b5232c19c0fe3e6a115f45ab3fcb100c79` at `lab/astra-capture/c2-kxnhlgame/panel_stub.json` and the lab copies (`2026-09-23.c2-kxnhlgame-v0`, `admitted_at` null)
- settled reget `8d597578bc65ea14ab1cbf5aa3c6d121d61431078a755b8419c815aa1d354df0`
- accept `ce82d9347c8af6666d96fb5c63be7693f4672306639ce4ba2360ba231c01e698`
- frozen experiment `a882ab8e410b6b5a77b60aa0225dcb932c0a1b0b3bcc692a02a5cfa23b81bd42`
- empty results `cc28e226979959d417ea1b7c6a05c87e6776e96489d57f793249bc42f912934f`
- examiner hold `06fed86652d552820fd8336363c89e79b336ec0d7c3a2c406a45140eff3dbd59`
- maximize pin `222c5d6bc1d1758b224f4ddee92016093cecd883b07cf0f10bcd16ea418161ca`
- `SOURCE_PINS.json` sha256 `e1eb1f6504836ddfa1a0a79b0743d51a372895fe19c05b935c7eedc8fa770c3d`

`conductor_pin_status` reports the six conductor matches and
`conductor_bytes_in_checkout` true. `results` and `pnl` stay null. The
2026-09-23T20:26:12Z unit run is code verification. It is not an Examiner
score. Examiner status stays `HOLD_PRE_PR`. `stub_ready` on the attached
hold is true and is not a score.

## Limitations

- Scout nonempty N=17 is a pin from single-market GETs. It is not
  `settled_join_n`. The series list `status=settled|finalized|open` and
  the events settled list stay `429_honest` and were not backfilled.
- Parent FQ seeds `KXNHLGAME-26SEP26TBFLA-TB`,
  `KXNHLGAME-26SEP26TBFLA-FLA`, and `KXNHLGAME-26SEP26COLUTA-UTA` stay
  active with an empty `result`. Finalized nonempty parent count is 0.
  The panel stub `result` stays empty. `admitted_at` stays null. This
  harness does not run `admit.py`.
- J0 and J1 on the conductor bytes label 24 keys in memory. Seventeen
  settled single-market rows have a non-empty official `result`. Four
  reget parent rows are active and empty. Three keys are the honest gaps
  (series list 429, events list 429, and the parent SEP26 note). Those
  labels are not written into `settled_join_n`, `occurrence_match_n`, or
  `admit_ready_flag`. Eight other panel markets have no reget parent row
  and no market object was invented for them. Missing SEP22 pair sides
  were not invented.
- `SOURCE_PINS.json` lists digests. It does not contain the file bytes.
- No public orderbook GET was stored. `quote_depth` refuses. No Logan key
  was read. No order route exists in this lab.
- Feebook, rails, Cap-SR, FQ siblings including NHL-FQ, the C3-RJ lab,
  the C5-RJ lab, the R3P3-RJ lab, and Arm B were not modified. This packet
  does not ungate S1, S2, or R2-P4. Clock admit is still closed, so
  Examiner scoring stays closed.

## Status update (2026-09-24)

The Examiner has since issued `READY_NOT_SCORED` (`stub_ready` true, `NOT_SCORED`). This supersedes the earlier `HOLD_PRE_PR` wording above. Examiner ACK `lab/governance/astra/packets/NHL_KXNHLGAME_SETTLED_JOIN_HARNESS/EXAMINER_ACK_NHL_RJ_PR44_STUB_READY_NOT_SCORED_2026-09-23.json` sha256 `c71334a8c978aa885616cdfd034bf0e169fd6484be00925caf09fcd2e783684b`. `results`, `pnl`, and the scorecard remain null. Nothing was scored.
