# C5 KXBTC15M settled-resolution join unit results

September 23, 2026. This file records a code check of the frozen join-gate
harness. It is a unit verification. It is not a simulated trading run and
not live validation. `FROZEN_EXPERIMENT.json` still has `results: null` and
`pnl: null`. `results/EMPTY_RESULTS.json` still has `settled_join_n`,
`occurrence_match_n`, `admit_ready_flag`, `results`, and `pnl` null. Those
fields stay null on purpose. This page is not profit, and it is not folded
back into the freeze hashes. No tape walk was run. No P&L figure is
reported. This is not an Examiner score and not a live-order
certification. This is not live crypto trading.

## Command

From `kalshi_c5_kxbtc15m_settled_join_lab_20260923`, Python 3.12, standard library:

```bash
python3 -m unittest -v tests.test_orchestrator
```

Ran 10 tests in 0.103s. Recorded at 2026-09-23T19:30:21Z. Result: OK.
Failures: 0. Errors: 0.

The checks that passed are the predeclared ones: freeze, scout reget,
seed summary, panel stub, settled reget, accept, frozen experiment, and
empty-results digests recorded in `orchestrator.py` and `SOURCE_PINS.json`;
`admitted_at` null on the stub, on the event, and on the market; refusal
of `panel_admitted.json` and of a stub copy that sets `admitted_at`; J0
and J1 schema on the authentic reget with the scorecard fields null; the
finalized and closed list `too_many_requests` gaps left without a ticker,
a result, or an `occurrence_datetime`; the parent seed
`KXBTC15M-26SEP222045-45` finalized `result` `no` on the reget while the
panel stub `result` stays null; Lee-Ready refused; refusal of live
orders, Logan keys, live crypto trading, invented results, invented
depth, invented fills, a list-429 backfill, an invented open-ticker
market, an invented `occurrence_datetime`, `admit.py`, an Examiner-ready
claim, an S1 / S2 / R2-P4 ungate, and Cap-SR / FQ / C5 honesty / C3-RJ /
Arm B reopen.

Feebook and rails were not imported. Their pinned commits
`22371178cb2663250b4762f328069571c48cb551` and
`6a28e0d6254327ea4e6451c781bec56215ac6cac` are unchanged. The scout pin
`settled_nonempty_result_N` is 20 and was not copied into `settled_join_n`.
Twenty-one reget market objects already share `occurrence_datetime` with
the seed summary. The parent seed also shares that timestamp with the
panel stub. That list is not `occurrence_match_n`. The cited open ticker
`KXBTC15M-26SEP231530-30` is not on that list.

## Pins verified on this branch

- harness freeze `7f4b36eca39d43ee7403628c2e525d5980fa40bcfc906550c7f00bb06ffd4f21`
- scout reget `7be17c44aef31abf7a0ab94938d0289f8766670ddacefdec566735818e044796`
- seed summary `b39c919809f709bcb81ff10a3d983b266bc7a1303c0de502c7c20be726415198`
- panel stub `60f613e8d775b66b9044ad31d2faf77bba84176f214a7bce599aa7a65b6905f8` at `lab/astra-capture/c5-kxbtc15m/panel_stub.json` and the lab copies (`2026-09-22.c5-kxbtc15m-v0`, `admitted_at` null)
- settled reget `319d6d3e394089fd21fefbfaa52c58166e78c2d781077a3f876331d2c54de617`
- accept `e116bbcb5f9518e6008ef412c8ff212a3170d0e3f26eb978f07a204b327aba7d`
- frozen experiment `31db09b93b09dccd449ad2ade56838eb6ccb531990209a5cbe85e91703dfeffc`
- empty results `94f5e75928b530516143fcf6b23c6b532701c3afb5da84327adf550a4046d4e3`
- `SOURCE_PINS.json` sha256 `3b8ca87c3ee89b23aa6cda2b90176060ebb3ebfe4c6b68dbeba917adeb44cb55`

`conductor_pin_status` reports the six conductor matches and
`conductor_bytes_in_checkout` true. `results` and `pnl` stay null. The
2026-09-23T19:30:21Z unit run is code verification. It is not an Examiner
score. Examiner status stays `NOT_SCORED` and `stub_ready` stays false.

## Limitations

- The C5 cites under `lab/governance/astra/packets/` are absent. The
  verified copies are the lab paths and the existing panel stub under
  `lab/astra-capture/c5-kxbtc15m/`. An unrelated R3-P2 packet in that
  governance tree was not edited. `SOURCE_PINS.json` lists digests. It
  does not contain the file bytes.
- The freeze cites `lab/astra-capture/c5-kxbtc15m/settled_reget_2026-09-23.json`.
  That path was not added. The attached bytes are in this lab. If that
  cite path appears later, the orchestrator requires the same digest.
- J0 and J1 on the conductor bytes label 23 keys in memory. Twenty
  settled-list markets and the parent seed have a non-empty official
  `result`. Two keys are the finalized and closed list 429 gaps. Those
  labels are not written into `settled_join_n`, `occurrence_match_n`, or
  `admit_ready_flag`. The scout pin 20 is not that scorecard field.
- `panel_admitted.json` is absent. `admitted_at` on the seed is null.
  The panel market `result` stays null even though the reget result is
  `no`. This harness does not run `admit.py`. Clock admit is still
  closed, so Examiner scoring stays closed.
- No public orderbook GET was stored. Quote size fields on the reget are
  not a depth ladder. `quote_depth` refuses. No Logan key was read. No
  order route exists in this lab.
- Feebook, rails, Cap-SR, FQ siblings, the C5 honesty lab, the C3-RJ lab,
  and Arm B were not modified. This packet does not ungate S1, S2, or
  R2-P4. This is not live crypto trading.
