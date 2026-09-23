# C3 KXHIGHNY settled-resolution join unit results

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

From `kalshi_c3_kxhighny_settled_join_lab_20260923`, Python 3.12, standard library:

```bash
python3 -m unittest -v tests.test_orchestrator
```

Ran 10 tests in 0.086s. Recorded at 2026-09-23T19:12:16Z. Result: OK.
Failures: 0. Errors: 0.

The checks that passed are the predeclared ones: freeze, scout reget,
seed summary, panel stub, settled reget, accept, frozen experiment, and
empty-results digests recorded in `orchestrator.py` and `SOURCE_PINS.json`;
`admitted_at` null on the stub, on each event, and on each market;
refusal of `panel_admitted.json` and of a stub copy that sets
`admitted_at`; J0 and J1 schema on the authentic reget with the scorecard
fields null; the CHI `too_many_requests` body left without a ticker, a
result, or an `occurrence_datetime`; Lee-Ready refused; refusal of live
orders, Logan keys, invented results, invented depth, invented fills, a
CHI 429 backfill, an invented `occurrence_datetime`, `admit.py`, an
Examiner-ready claim, an S1 / S2 / R2-P4 ungate, and Cap-SR / FQ /
ETH-FQ / EMPTY-OB / C3 bordering / Arm B reopen.

Feebook and rails were not imported. Their pinned commits
`22371178cb2663250b4762f328069571c48cb551` and
`6a28e0d6254327ea4e6451c781bec56215ac6cac` are unchanged. The scout pin
`settled_nonempty_result_N` is 4 and was not copied into `settled_join_n`.
Five reget market objects already share `occurrence_datetime` with the
seed summary and the panel stub. That list is not `occurrence_match_n`.
`KXHIGHCHI-26SEP22-B66.5` is not on that list.

## Pins verified on this branch

- harness freeze `56adcf592239b028aaa8bcffbf09815115b8454f78db39b43c578e64c160a4d5`
- scout reget `e8950352745007d3cb565050161430807fa5de70d15321bb00bede6ca9ac18ee`
- seed summary `b32bbf3200649bcea4fb61a98a4869d5123060a57702a9327262cccbc8e1ca93`
- panel stub `2a5da7fe85ca1adc6b7c4dcf9e09ed5c6bb62be6b5c9b42731e36e31d1e8dfea` at `lab/astra-capture/c3-kxhighny/panel_stub.json` and the lab copies (`2026-09-22.c3-kxhighny-v0`, `admitted_at` null)
- settled reget `0055faae508ba034eb49a12d52713566cbfe20bfbfbd2a16203ef350152ac24a`
- accept `9adb77ed01fd9ccb894564efa9d5534d2edf189365ca0852fff49dafd3598d69`
- frozen experiment `10f75f008f6fb870e212b81f9913b09ab06337973e850d36796f336331d33c23`
- empty results `48e5916fff57563d14a6a84b8c6c0ed2515c3172066d565e5a18933faf02f4e6`
- `SOURCE_PINS.json` sha256 `a11360f5e62a2142b2064b58279cc507a4068ac9c73f4e4b64af1b781be3c4ff`

`conductor_pin_status` reports the six conductor matches and
`conductor_bytes_in_checkout` true. `results` and `pnl` stay null. The
2026-09-23T19:12:16Z unit run is code verification. It is not an Examiner
score. Examiner status stays `NOT_SCORED` and `stub_ready` stays false.

## Limitations

- `lab/governance/astra/` is absent. The verified copies are the lab paths
  and the existing panel stub under `lab/astra-capture/c3-kxhighny/`.
  `SOURCE_PINS.json` lists digests. It does not contain the file bytes.
- The freeze cites `lab/astra-capture/c3-kxhighny/settled_reget_2026-09-23.json`.
  That path was not added. The attached bytes are in this lab. If that
  cite path appears later, the orchestrator requires the same digest.
- J0 and J1 on the conductor bytes label six reget keys in memory. Four
  finalized markets have a non-empty official `result`. One NY SEP23
  market stays `active` with an empty `result`. One CHI key is the 429
  gap. Those labels are not written into `settled_join_n`,
  `occurrence_match_n`, or `admit_ready_flag`.
- `panel_admitted.json` is absent. `admitted_at` on the seed is null.
  This harness does not run `admit.py`. Clock admit is still closed, so
  Examiner scoring stays closed.
- No public orderbook GET was stored. Quote size fields on the reget are
  not a depth ladder. `quote_depth` refuses. No Logan key was read. No
  order route exists in this lab.
- Feebook, rails, Cap-SR, FQ siblings including ETH-FQ, the C3 bordering
  lab, and Arm B were not modified. This packet does not ungate S1, S2,
  or R2-P4.
