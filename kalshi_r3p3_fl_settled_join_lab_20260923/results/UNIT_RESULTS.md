# R3-P3 FL maker/taker settled-resolution join unit results

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

From `kalshi_r3p3_fl_settled_join_lab_20260923`, Python 3.12, standard library:

```bash
python3 -m unittest -v tests.test_orchestrator
```

Ran 10 tests in 0.129s. Recorded at 2026-09-23T19:53:37Z. Result: OK.
Failures: 0. Errors: 0.

The checks that passed are the predeclared ones: freeze, scout reget,
seed summary, panel stub, settled reget, accept, frozen experiment, and
empty-results digests recorded in `orchestrator.py` and `SOURCE_PINS.json`;
`admitted_at` null on the stub, on each event, and on each market; refusal
of `panel_admitted.json` and of a stub copy that sets `admitted_at`; J0
and J1 schema on the authentic reget with the scorecard fields null; the
CHI settled list and the NY open list `too_many_requests` gaps left
without a ticker, a result, or an `occurrence_datetime`; the three parent
seeds finalized with nonempty official `result` on the reget
(`KXHIGHNY-26SEP22-B67.5` `yes`, `KXHIGHNY-26SEP22-T70` `no`,
`KXHIGHCHI-26SEP22-B64.5` `yes`) while each panel stub `result` stays
null; Lee-Ready refused; refusal of live orders, Logan keys, invented
results, invented depth, invented fills, a list-429 backfill, an invented
open-ticker settlement, an invented `occurrence_datetime`, `admit.py`, an
Examiner-ready claim, an S1 / S2 / R2-P4 ungate, and Cap-SR / FQ / R3-P3
fee-arm / C3-RJ / C5-RJ / Arm B reopen.

Feebook and rails were not imported. Their pinned commits
`22371178cb2663250b4762f328069571c48cb551` and
`6a28e0d6254327ea4e6451c781bec56215ac6cac` are unchanged. The scout pin
`settled_nonempty_result_N` is 20 and was not copied into `settled_join_n`.
The three parent seeds share `occurrence_datetime` `2026-09-23T14:00:00Z`
with the panel stub and the reget. That list is not `occurrence_match_n`.
The four cited CHI open tickers are active with an empty `result` and are
not on that list.

## Pins verified on this branch

- harness freeze `7fcfc36ab4761e2dec56018b498372fb63c402f2582fe848e8775e28f9b720b9`
- scout reget `f675d7c40ccad37173b2cb54837349cd3053b7b76606c43efba5759a1bde551f`
- seed summary `b43d4ab065b712f5bf1b87eb164bccb00e8e9993f97db9d86a8d1619ce9ec13d`
- panel stub `6f640dd3a6091ba6b896ded38fdded4676583aa3c885223da21ddf03780250c0` at `lab/astra-capture/r3-p3-fl-maker-taker/panel_stub.json` and the lab copies (`2026-09-22.r3-p3-fl-maker-taker-v0`, `admitted_at` null)
- settled reget `c5f680e4ff66af67691672c4b8c43eb57906f25b4d79fdeb65f61e031c13efda`
- accept `a6434fe4854b850df24a0a081168ba5d90d4646ba9a409418d7b874262a5fa9c`
- frozen experiment `dd2a4217de4476d9c54a4487e68fe7bd912914bb55a5a1be4bc00126199f19e0`
- empty results `d0f5fbfa3e01fca5f047f42ecc7e1bb5b1d4097ee455d6ce62a4b8a861d4a613`
- `SOURCE_PINS.json` sha256 `4b94c1823017f7fe725e98ece11ac42dd16fabd415e81b2f3c4d08b0f1c5eb3a`

`conductor_pin_status` reports the six conductor matches and
`conductor_bytes_in_checkout` true. `results` and `pnl` stay null. The
2026-09-23T19:53:37Z unit run is code verification. It is not an Examiner
score. Examiner status stays `NOT_SCORED` and `stub_ready` stays false.

## Limitations

- The R3P3 scout cite under `lab/governance/astra/packets/` is absent. The
  verified copies are the lab paths and the existing panel stub under
  `lab/astra-capture/r3-p3-fl-maker-taker/`. An unrelated R3-P2 packet in
  that governance tree was not edited. `SOURCE_PINS.json` lists digests.
  It does not contain the file bytes.
- The freeze cites `lab/astra-capture/r3-p3-fl-maker-taker/settled_reget_2026-09-23.json`.
  That path was not added. The attached bytes are in this lab. If that
  cite path appears later, the orchestrator requires the same digest.
- J0 and J1 on the conductor bytes label 23 keys in memory. Twenty
  `KXHIGHNY` settled-list markets plus the CHI parent seed have a
  non-empty official `result`. Two keys are the CHI settled list and the
  NY open list 429 gaps. Those labels are not written into
  `settled_join_n`, `occurrence_match_n`, or `admit_ready_flag`. The scout
  pin 20 is not that scorecard field. The three parent-seed SoT matches
  are not `occurrence_match_n`.
- `panel_admitted.json` is absent. `admitted_at` on the stub is null.
  Each panel market `result` stays null even though the reget results are
  `yes`, `no`, and `yes`. The stub cohort `settled_markets_resolved_n`
  stays 0. This harness does not run `admit.py`. Clock admit is still
  closed, so Examiner scoring stays closed.
- No public orderbook GET was stored. Quote size fields on the reget are
  not a depth ladder. `quote_depth` refuses. No Logan key was read. No
  order route exists in this lab.
- Feebook, rails, Cap-SR, FQ siblings, the R3-P3 fee lab, the C3-RJ lab,
  the C5-RJ lab, and Arm B were not modified. This packet does not ungate
  S1, S2, or R2-P4.
