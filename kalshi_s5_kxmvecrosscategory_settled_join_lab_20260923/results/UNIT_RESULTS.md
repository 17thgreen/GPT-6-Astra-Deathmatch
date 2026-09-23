# S5 KXMVECROSSCATEGORY settled-resolution join unit results

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

From `kalshi_s5_kxmvecrosscategory_settled_join_lab_20260923`, Python 3, standard library:

```bash
python3 -m unittest -v tests.test_orchestrator
```

Ran 10 tests in 0.240s. Recorded at 2026-09-23T21:46:24Z. Result: OK.
Failures: 0. Errors: 0.

The checks that passed are the predeclared ones: freeze, scout reget,
seed summary, panel stub, settled reget, accept, frozen experiment, and
empty-results digests recorded in `orchestrator.py` and `SOURCE_PINS.json`;
`admitted_at` null on the stub; refusal of `panel_admitted.json` and of a
stub copy that sets `admitted_at`; J0 and J1 schema on the authentic reget
with the scorecard fields null; the settled list left as HTTP 200 with
limit 20 and the cursor not followed; earlier settled, finalized, and
events lists left as `429_honest` without a backfilled market object;
`KXMVECROSSCATEGORY-SHARD1` left as `429_honest`; twenty settled rows
finalized with nonempty official `result` (`yes` 4, `no` 16) from
`markets_settled_KXMVECROSSCATEGORY_lim20.json`; `occurrence_datetime`
null on those rows, with J1 using `expected_expiration_time` and not
inventing `occurrence_datetime`; five parent ticker GETs finalized with
`result` `no` left in the scout and not copied onto the panel stub; the
panel stub keeps two `status_observed` `active` rows and three
`finalized` rows and no `result`; Lee-Ready refused; refusal of live
orders, Logan keys, invented results, invented depth, invented fills, a
list-429 backfill, a SHARD1 backfill, a cursor follow, an invented
related-series market, an invented parent settlement, an invented
`occurrence_datetime`, `admit.py`, an Examiner-ready claim, an S1 / S2 /
R2-P4 ungate, copying scout N into `settled_join_n`, and Cap-SR / FQ /
S5 FILLLEGS / MVE-FL / C3-RJ / C5-RJ / R3P3-RJ / NHL-RJ / S4-RJ / R2P3-RJ
/ Arm B reopen.

Feebook and rails were not imported. Their pinned commits
`22371178cb2663250b4762f328069571c48cb551` and
`6a28e0d6254327ea4e6451c781bec56215ac6cac` are unchanged. The scout pin
`settled_nonempty_result_N` is 20 and was not copied into `settled_join_n`.
The twenty settled rows share `expected_expiration_time` across the scout,
the seed summary, and the reget because `occurrence_datetime` is null.
That list is not `occurrence_match_n`. Five parent seeds are finalized
nonempty on ticker GETs. The related fee-pin series count N=20 is not a
market list in this reget.

## Pins verified on this branch

- harness freeze `cd264a4d41ef055d1cbca80a5dbe6756746211537fb24799dca9dde8980cb799`
- scout reget `33db60a50f2e7746315f4603b9f78a9260145cb49d0250e141471de46f4df9e3`
- seed summary `3bc4aa5f44d7d31295dfd25f7bac3a3e39463c237315e8228c3fcf434d08419a`
- panel stub `4918b820d454c5f997ea100917859f7e9467d92933bed1bc8a55c81ab8ce5b8e` at `lab/astra-capture/s5-kxmvecrosscategory/panel_stub.json` and the lab copies (`2026-09-22.s5-kxmvecrosscategory-v0`, `admitted_at` null)
- settled reget `91111f20586a1b684e430baa0e8b62a3fffc7d510de99e43bab7d213dfeb26da`
- accept `495675175589c08122bc57375dd8e7d00aea9f4a154df3aff086b015a2513a8c`
- frozen experiment `4bb57f793e5eb6ed3fed664843e1ad00f2e204739e3014df96a56e342036b8b0`
- empty results `9257b65bcb892cd5139fd25433cbe4b9a1704045fea86890bfa3e0ed56c1c88c`
- examiner hold `3bce25f0dacb43f93bafe2229839bece190ff889b3fdf00a21dc1aac583b0ff7`
- maximize pin `1e071f2cebdc18e198901e33af49387a751ecc1fe85bd14a0cb09a1f3ff6416f`
- `SOURCE_PINS.json` sha256 `75f7ef854c653bdf699e72a628a172b4a8dc161d7a4e0441c97ddcaad0f3d8b6`

`conductor_pin_status` reports the six conductor matches and
`conductor_bytes_in_checkout` true. `results` and `pnl` stay null. The
2026-09-23T21:46:24Z unit run is code verification. It is not an Examiner
score. Examiner status stays `HOLD_PRE_PR`. `stub_ready` on the attached
hold is false and is not a score.

## Limitations

- Scout nonempty N=20 is a pin from `GET /markets?series_ticker=KXMVECROSSCATEGORY&status=settled&limit=20`.
  It is not `settled_join_n`. The settled list HTTP status is 200 and the
  cursor is present. Markets past that cursor were not fetched and were
  not invented. Earlier settled-list attempts, the finalized list, and
  the events closed/settled list stay `429_honest` and were not
  backfilled. `KXMVECROSSCATEGORY-SHARD1` stays `429_honest`.
- `occurrence_datetime` is null on all 20 settled rows. J1 uses
  `expected_expiration_time` for that honest null. No `occurrence_datetime`
  was invented. The related series `KXMVESPORTSMULTIGAMEEXTENDED` settled
  count is 20 and HTTP 200. Those markets are not in this reget file and
  were not invented.
- Parent panel seeds are finalized with `result` `no` on the scout ticker
  GETs. Finalized nonempty parent count is 5. Those five tickers are not
  on the settled lim20 list. The panel stub was not rewritten: two markets
  stay `status_observed` `active`, three stay `finalized`, and the stub
  has no `result`. `admitted_at` stays null. This harness does not run
  `admit.py`.
- J0 and J1 on the conductor bytes label 29 keys in memory. Twenty
  settled rows have a non-empty official `result` and sit on the settled
  list file, matched on `expected_expiration_time`. Five parent seeds are
  ticker-GET nonempty with null `occurrence_datetime`. Four keys are the
  honest gaps (earlier settled list 429, finalized list 429, events
  closed/settled list 429, and SHARD1 429). Those labels are not written
  into `settled_join_n`, `occurrence_match_n`, or `admit_ready_flag`.
- `SOURCE_PINS.json` lists digests. It does not contain the file bytes.
- Public quote size fields on the attached reget are not a depth ladder.
  `quote_depth` refuses. No Logan key was read. No order route exists in
  this lab.
- Feebook, rails, Cap-SR, S5 FILLLEGS, MVE-FL, FQ siblings, the C3-RJ
  lab, the C5-RJ lab, the R3P3-RJ lab, the NHL-RJ lab, the S4-RJ lab, the
  R2P3-RJ lab, and Arm B were not modified. This packet does not ungate
  S1, S2, or R2-P4. Clock admit is still closed, so Examiner scoring
  stays closed.
