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

Ran 10 tests in 0.110s. Recorded at 2026-09-23T20:23:25Z. Result: OK.
Failures: 0. Errors: 0.

The checks that passed are the predeclared ones: freeze, scout reget,
seed summary, panel stub, settled reget, accept, frozen experiment, and
empty-results digests recorded in `orchestrator.py` and `SOURCE_PINS.json`;
`admitted_at` null on the stub; refusal of `panel_admitted.json` and of a
stub copy that sets `admitted_at`; J0 and J1 schema on the authentic reget
with the scorecard fields null; the series settled/finalized/open list and
the events settled list left as `429_honest` without a ticker, a result, or
an `occurrence_datetime`; the 17 overnight SEP22 markets finalized with a
non-empty official `result` on the single-market reget (8 `yes`, 9 `no`)
while each panel stub `result` stays `""`; the three parent SEP26 seeds
stay active with an empty result and `parent_seeds_finalized_nonempty_N`
0; Lee-Ready refused; refusal of live orders, Logan keys, invented
results, invented depth, invented fills, a list-429 backfill, an invented
SEP26 settle, an invented missing side, an invented `occurrence_datetime`,
`admit.py`, an Examiner-ready claim, an S1 / S2 / R2-P4 ungate, and
Cap-SR / FQ / NHL-FQ / C3-RJ / C5-RJ / R3P3-RJ / Arm B reopen.

Feebook and rails were not imported. Their pinned commits
`22371178cb2663250b4762f328069571c48cb551` and
`6a28e0d6254327ea4e6451c781bec56215ac6cac` are unchanged. The scout pin
`settled_nonempty_result_N` is 17 and was not copied into `settled_join_n`.
The 17 overnight rows share `occurrence_datetime` across the scout, the
seed summary, and the reget. That list is not `occurrence_match_n`.

## Pins verified on this branch

- harness freeze `d1f71cea6df8f6c5a9fac6f9d1aa418ce61aa650794f22b400a01c4f3fd45810`
- scout reget `99a7f90564ee2150f5edef4efafb7ccb954b87036e0b43f29ff7dc6ed104706f`
- seed summary `794e148df5927c64d08b4578b47a7453589f02872af65880922bcb9273194a1a`
- panel stub `60d183e7bdcf25adbc94eeeb3bb361b5232c19c0fe3e6a115f45ab3fcb100c79` at `lab/astra-capture/c2-kxnhlgame/panel_stub.json` and the lab copies (`2026-09-23.c2-kxnhlgame-v0`, `admitted_at` null)
- settled reget `8d597578bc65ea14ab1cbf5aa3c6d121d61431078a755b8419c815aa1d354df0`
- accept `cee2705a620ef9aef8316fa8629d6c025e7ac8489022bc35559994736be63eaf`
- frozen experiment `a882ab8e410b6b5a77b60aa0225dcb932c0a1b0b3bcc692a02a5cfa23b81bd42`
- empty results `cc28e226979959d417ea1b7c6a05c87e6776e96489d57f793249bc42f912934f`
- `SOURCE_PINS.json` sha256 `fa314d759d39f1700639024132c800d38824a05c83cc210fa7a4f1f84ebbcc69`

`conductor_pin_status` reports the six conductor matches and
`conductor_bytes_in_checkout` true. `results` and `pnl` stay null. The
2026-09-23T20:23:25Z unit run is code verification. It is not an Examiner
score. Examiner status stays `NOT_SCORED` and `stub_ready` stays false.

## Limitations

- The NHL scout cite under `lab/governance/astra/packets/` is absent. The
  verified copies are the lab paths and the existing panel stub under
  `lab/astra-capture/c2-kxnhlgame/`. An unrelated R3-P2 packet in that
  governance tree was not edited. `SOURCE_PINS.json` lists digests. It
  does not contain the file bytes.
- The freeze cites `lab/astra-capture/c2-kxnhlgame/settled_reget_2026-09-23.json`.
  That path was not added. The attached bytes are in this lab. If that
  cite path appears later, the orchestrator requires the same digest.
- J0 and J1 on the conductor bytes label 23 keys in memory. Seventeen
  overnight SEP22 single-market rows have a non-empty official `result`.
  Four SEP26 rows on the reget stay `active` with `result` `""`, including
  the three parent seeds and `KXNHLGAME-26SEP26WSHPHI-WSH`. Two keys are
  the series settled/finalized/open list and the events settled list, both
  `429_honest`. Those labels are not written into `settled_join_n`,
  `occurrence_match_n`, or `admit_ready_flag`. The scout pin 17 is not
  that scorecard field. The 17 occurrence agreements are not
  `occurrence_match_n`.
- Three overnight events have one market row
  (`KXNHLGAME-26SEP22TBNSH`, `KXNHLGAME-26SEP22UTALA`,
  `KXNHLGAME-26SEP22VGKSJ`). The other side is not in the reget and was
  not added.
- Eight of the 12 panel markets are absent from this reget. Their stub
  `result` stays `""`. No GET was invented for them.
- `panel_admitted.json` is absent. `admitted_at` on the stub is null.
  Each panel market `result` stays `""` even where the overnight reget
  results are `yes` or `no`. This harness does not run `admit.py`. Clock
  admit is still closed, so Examiner scoring stays closed.
- No public orderbook GET was stored. Quote size fields on the panel stub
  are not a depth ladder. `quote_depth` refuses. No Logan key was read. No
  order route exists in this lab.
- Feebook, rails, Cap-SR, FQ siblings, the NHL-FQ lab, the C3-RJ lab, the
  C5-RJ lab, the R3P3-RJ lab, and Arm B were not modified. This packet does
  not ungate S1, S2, or R2-P4.
