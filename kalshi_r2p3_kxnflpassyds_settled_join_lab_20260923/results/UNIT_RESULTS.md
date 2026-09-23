# R2P3 KXNFLPASSYDS settled-resolution join unit results

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

From `kalshi_r2p3_kxnflpassyds_settled_join_lab_20260923`, Python 3.12, standard library:

```bash
python3 -m unittest -v tests.test_orchestrator
```

Ran 10 tests in 0.157s. Recorded at 2026-09-23T21:24:42Z. Result: OK.
Failures: 0. Errors: 0.

The checks that passed are the predeclared ones: freeze, scout reget,
seed summary, panel stub, settled reget, accept, frozen experiment, and
empty-results digests recorded in `orchestrator.py` and `SOURCE_PINS.json`;
`admitted_at` null on the stub; refusal of `panel_admitted.json` and of a
stub copy that sets `admitted_at`; J0 and J1 schema on the authentic reget
with the scorecard fields null; the settled list left as HTTP 200 with
limit 20 and the cursor not followed; the finalized list and the events
closed/settled lists left as `429_honest` without a backfilled market
object; the close-window query left as `400_honest`; twenty prior-weekend
SEP20/SEP21 rows finalized with nonempty official `result` (`yes` 6,
`no` 14) from `markets_settled_KXNFLPASSYDS_lim20.json` while the panel
stub has empty `market_tickers` and no settled `result`; parent SEP27
seeds stay active with a null `result` and finalized nonempty count 0;
ATL@GB stays excluded; Lee-Ready refused; refusal of live orders, Logan
keys, invented results, invented depth, invented fills, a list-429
backfill, a close-window backfill, a cursor follow, an invented parent
SEP27 settlement, an invented `occurrence_datetime`, `admit.py`, an
Examiner-ready claim, an S1 / S2 / R2-P4 ungate, copying scout N into
`settled_join_n`, and Cap-SR / FQ / R2-P3 prop-ladder / PASSYDS-PROP /
C3-RJ / C5-RJ / R3P3-RJ / NHL-RJ / S4-RJ / Arm B reopen.

Feebook and rails were not imported. Their pinned commits
`22371178cb2663250b4762f328069571c48cb551` and
`6a28e0d6254327ea4e6451c781bec56215ac6cac` are unchanged. The scout pin
`settled_nonempty_result_N` is 20 and was not copied into `settled_join_n`.
The twenty settled rows share `occurrence_datetime` across the scout,
the seed summary, and the reget. That list is not `occurrence_match_n`.
Four parent seeds stay active with a null `result`. The reget has no
`occurrence_datetime` for them, and none was invented. They are not
settled-join markets. The panel `market_tickers` stay empty.

## Pins verified on this branch

- harness freeze `9ad3b0112243c1020aec2bd6ef0df15011b065c30aa691a988da02eb08be1e0b`
- scout reget `2c3664ac240887026076a84e451ca798e0c2d10d42bdaf61a9a83844881681e5`
- seed summary `534a617bc3f18be501c07237d261e945b1bcf0301ac956cddae46e0431b75cd3`
- panel stub `70e879e8738d033f392d821849dee3537af3e7b8a916670779d238f78ce098be` at `lab/astra-capture/r2-p3-prop-slate/panel_stub.json` and the lab copies (`2026-09-22.r2-p3-prop-slate-v0`, `admitted_at` null)
- settled reget `2ce8426edb4ee5053f63bf2fe1439dbd046978eb76afa1e0537b17cca9b8b0e4`
- accept `e5218cf2511607211ec1d825a9dad36abaee3d9cfda24488524c3d6bcbe3a565`
- frozen experiment `44c801e306ffc22325b7e689a9dadbdb8774f89fd39a14892aa7de965f9edd21`
- empty results `5a41a8295708e824757fdd51a680a660fdbbf49f2dc68a17785f8d3a9095cd46`
- examiner hold `baf5f6c3bc9f027c8f90de3fe0048c1b74ddebb5af1b93ca72e72f63afa61b5b`
- maximize pin `481b603c18df7dfe63475a32bde479f34dd0b5cae41ab0348aa2041788545451`
- `SOURCE_PINS.json` sha256 `de8efec52ba222e0ea6344664881acd65c9ffa17430a11dda19abdb335a4121c`

`conductor_pin_status` reports the six conductor matches and
`conductor_bytes_in_checkout` true. `results` and `pnl` stay null. The
2026-09-23T21:24:42Z unit run is code verification. It is not an Examiner
score. Examiner status stays `HOLD_PRE_PR`. `stub_ready` on the attached
hold is false and is not a score.

## Limitations

- Scout nonempty N=20 is a pin from `GET /markets?status=settled&limit=20`.
  It is not `settled_join_n`. The settled list HTTP status is 200 and the
  cursor is present. Markets past that cursor were not fetched and were
  not invented. The finalized list and the events closed/settled lists
  stay `429_honest` and were not backfilled. The close-window
  `min_close_ts`/`max_close_ts` query stays `400_honest`.
- Parent prop-ladder seeds `KXNFLPASSYDS-26SEP27LACBUF-BUFJALLEN17-150`,
  `KXNFLPASSYDS-26SEP27LACBUF-BUFJALLEN17-175`,
  `KXNFLPASSYDS-26SEP27BALDAL-DALDPRESCOTT4-175`, and
  `KXNFLPASSYDS-26SEP27BALDAL-DALDPRESCOTT4-200` stay active with a null
  `result`. Finalized nonempty parent count is 0. The reget does not
  carry `occurrence_datetime` for those seeds. Panel `market_tickers`
  stay empty. `admitted_at` stays null. This harness does not run
  `admit.py`. ATL@GB SEP24 stays excluded.
- J0 and J1 on the conductor bytes label 29 keys in memory. Twenty
  settled rows have a non-empty official `result` and sit on the settled
  list file. Four parent seeds are active and empty. Five keys are the
  honest gaps (finalized list 429, events closed/settled list 429,
  close-window 400, the parent SEP27 note, and the ATL@GB exclusion
  note). Those labels are not written into `settled_join_n`,
  `occurrence_match_n`, or `admit_ready_flag`. Sibling series
  `KXNFLRECYDS` and `KXNFLRSHYDS` are noted on the scout and are not
  given invented settled rows.
- `SOURCE_PINS.json` lists digests. It does not contain the file bytes.
- No public orderbook GET was stored. `quote_depth` refuses. No Logan key
  was read. No order route exists in this lab.
- Feebook, rails, Cap-SR, the R2-P3 prop-ladder lab, PASSYDS-PROP, FQ
  siblings, the C3-RJ lab, the C5-RJ lab, the R3P3-RJ lab, the NHL-RJ
  lab, the S4-RJ lab, and Arm B were not modified. This packet does not
  ungate S1, S2, or R2-P4. Clock admit is still closed, so Examiner
  scoring stays closed.
