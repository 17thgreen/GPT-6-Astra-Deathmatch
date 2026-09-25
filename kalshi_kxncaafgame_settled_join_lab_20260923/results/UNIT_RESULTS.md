# S4 KXNCAAFGAME settled-resolution join unit results

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

From `kalshi_kxncaafgame_settled_join_lab_20260923`, Python 3.12, standard library:

```bash
python3 -m unittest -v tests.test_orchestrator
```

Ran 10 tests in 0.237s. Recorded at 2026-09-23T20:54:36Z. Result: OK.
Failures: 0. Errors: 0.

An earlier local run failed because the settled reget omits
`parent_seeds_finalized_nonempty_N` and the checker required that key.
The scout and the seed pin the count at 0. The reget pin is the omission.
The correction refuses a count written onto the reget.

The checks that passed are the predeclared ones: freeze, scout reget,
seed summary, panel stub, settled reget, accept, frozen experiment, and
empty-results digests recorded in `orchestrator.py` and `SOURCE_PINS.json`;
`admitted_at` null on the stub; refusal of `panel_admitted.json` and of a
stub copy that sets `admitted_at`; J0 and J1 schema on the authentic reget
with the scorecard fields null; the series settled/finalized/open list and
the events settled list left as `429_honest` without a backfilled market
object; twelve named event and market GET gaps left as `not_found` or
`too_many_requests`; eighteen prior-weekend SEP05/SEP12/SEP19 rows
finalized with nonempty official `result` (`yes` 9, `no` 9; 10 event
embeds and 8 single-market GETs) while the panel stub has no settled
`result`; parent SEP26 seeds stay active with a null `result` and
finalized nonempty count 0; Lee-Ready refused; refusal of live orders,
Logan keys, invented results, invented depth, invented fills, a list-429
backfill, an invented parent SEP26 settlement, an invented
`occurrence_datetime`, `admit.py`, an Examiner-ready claim, an S1 / S2 /
R2-P4 ungate, copying scout N into `settled_join_n`, and Cap-SR / FQ /
S4-FQ / NCAAF-FQ / C3-RJ / C5-RJ / R3P3-RJ / NHL-RJ / Arm B reopen.

Feebook and rails were not imported. Their pinned commits
`22371178cb2663250b4762f328069571c48cb551` and
`6a28e0d6254327ea4e6451c781bec56215ac6cac` are unchanged. The scout pin
`settled_nonempty_result_N` is 18 and was not copied into `settled_join_n`.
The eighteen settled rows share `occurrence_datetime` across the scout,
the seed summary, and the reget. That list is not `occurrence_match_n`.
Three parent seeds stay active with a null `result`. The reget has no
`occurrence_datetime` for them, and none was invented. They are not
settled-join markets.

## Pins verified on this branch

- harness freeze `3a8e8ba52edd6acdc342c6a2faabb08665fe8a7a76e1b28af1c8e18850b03d99`
- scout reget `57fa0b28325ac13015f49521a87661b3cc064d22a13cf960f4fcdfd9badaa3dc`
- seed summary `9e67cd16f3ec6536d5dae3fe07de6e6b073c1c8d1adc9bb7e9297090ef567ce1`
- panel stub `38167d11da5842bc4d39e6e7dcaab20a67294c735ba14d8bbeafde3154c6342a` at `lab/astra-capture/s4-kxncaafgame/panel_stub.json` and the lab copies (`2026-09-22.s4-kxncaafgame-v0`, `admitted_at` null)
- settled reget `5bb0acfaa429e2ec1ad22e2e35e296540ac5b8e66eba4df6a0b2419d43257528`
- accept `87bb8d44e8ac50099cc66d0469dcd4a5cfafb78d92dd24e7a218100a6254da4a`
- frozen experiment `273c59f2af1d18c840121923f07c3d557abb5b8b1a0fefa9bdb048ce89fc6abb`
- empty results `4a67cd4f8d62bbffc7d2b3f7acdc1639dc01cbab058b86a8e8c74fe56da69e43`
- examiner hold `082921d6a9f202542792b4b34ae827835b2652b7b1c127466e9988a58e6d2d55`
- maximize pin `bd72d0d807d3854a1dfd9c3162c177850d682ad46af1ed77e4e824d5a657fa01`
- `SOURCE_PINS.json` sha256 `8c845b52335819448db146e1abc23cdbee2f314552eb8aad859549ae37dc766a`

`conductor_pin_status` reports the six conductor matches and
`conductor_bytes_in_checkout` true. `results` and `pnl` stay null. The
2026-09-23T20:54:36Z unit run is code verification. It is not an Examiner
score. Examiner status stays `HOLD_PRE_PR`. `stub_ready` on the attached
hold is false and is not a score.

## Limitations

- Scout nonempty N=18 is a pin from event embeds and single-market GETs.
  It is not `settled_join_n`. The series list
  `status=settled|finalized|open` and the events settled list stay
  `429_honest` and were not backfilled. Twelve named event and market
  GETs stay `not_found` or `too_many_requests`.
- Parent FQ seeds `KXNCAAFGAME-26SEP26BUCKPITT-PITT`,
  `KXNCAAFGAME-26SEP26BUCKPITT-BUCK`, and
  `KXNCAAFGAME-26SEP26TEXTENN-TEX` stay active with a null `result`.
  Finalized nonempty parent count is 0. The reget does not carry
  `occurrence_datetime` for those seeds. `admitted_at` stays null. This
  harness does not run `admit.py`.
- J0 and J1 on the conductor bytes label 36 keys in memory. Eighteen
  settled rows have a non-empty official `result`. Three parent seeds
  are active and empty. Fifteen keys are the honest gaps (series list
  429, events list 429, the parent SEP26 note, and twelve named GET
  failures). Those labels are not written into `settled_join_n`,
  `occurrence_match_n`, or `admit_ready_flag`. The other 223 panel
  market tickers have no reget row and no market object was invented
  for them. `KXNCAAFGAME-26SEP26TEXTENN-TENN` is on the panel and is
  not one of the three parent seed tickers.
- `SOURCE_PINS.json` lists digests. It does not contain the file bytes.
- No public orderbook GET was stored. `quote_depth` refuses. No Logan key
  was read. No order route exists in this lab.
- Feebook, rails, Cap-SR, FQ siblings including S4-FQ, the C3-RJ lab,
  the C5-RJ lab, the R3P3-RJ lab, the NHL-RJ lab, and Arm B were not
  modified. This packet does not ungate S1, S2, or R2-P4. Clock admit
  is still closed, so Examiner scoring stays closed.

## Status update (2026-09-24)

The Examiner has since issued `READY_NOT_SCORED` (`stub_ready` true, `NOT_SCORED`). This supersedes the earlier `HOLD_PRE_PR` wording above. Examiner ACK `lab/governance/astra/packets/S4_KXNCAAFGAME_SETTLED_JOIN_HARNESS/EXAMINER_ACK_S4_RJ_PR45_STUB_READY_NOT_SCORED_2026-09-23.json` sha256 `1417203a036421783b07fe7e954b4c6b3ae183ff19f6c51624ae96e93142c43d`. `results`, `pnl`, and the scorecard remain null. Nothing was scored.
