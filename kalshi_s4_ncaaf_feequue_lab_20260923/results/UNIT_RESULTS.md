# S4 KXNCAAFGAME fee+queue honesty harness unit results

September 23, 2026. This file records a code check of the frozen partition
harness. It is a unit verification. It is not a simulated trading run and
not live validation. `FROZEN_EXPERIMENT.json` still has `results: null` and
`pnl: null`. `results/EMPTY_RESULTS.json` still has
`maker_vs_taker_roi_delta`, `fresh_vs_stale_gap`, and `settled_join_n`
null. Those fields stay null on purpose. This page is not profit, and it
is not folded back into the freeze hashes. No tape walk was run. No P&L
figure is reported. This is not an Examiner score and not a live-order
certification.

## Command

From `kalshi_s4_ncaaf_feequue_lab_20260923`, Python 3.12, standard library:

```bash
python3 -m unittest -v tests.test_orchestrator
```

Ran 9 tests in 0.029s at 2026-09-23T15:46:14Z. Result: OK. Failures: 0.
Errors: 0.

The checks that passed are the predeclared ones: fee pin
`22371178cb2663250b4762f328069571c48cb551` and rails pin
`6a28e0d6254327ea4e6451c781bec56215ac6cac` with those trees unchanged since
those commits; recreation packet sha256
`00117c348573076bc35af422e6618d750c1e6b89c3387f2b7c0b0f259d3fe2a2`; recreation
parent kernel sha256
`f0e502264ce79d8e958c54cace387aa0521f616dd59290356aaafc33e9096847`; panel
seed `2026-09-22.s4-kxncaafgame-v0` sha256
`eb0a9ea7e4cf24d6f805f63688dbb48c71dc91a81bcea4afb2c88f73588b8112` with
`admitted_at` null and zero events; preference for a temporary
`panel_admitted.json` when that file exists; S4A0 native taker partitions
and S4A1 content-fresh / queue bins with the scorecard fields null;
Lee-Ready refused on every sampled input, including a well-formed native
row; refusal of live orders, Logan keys, invented fills, Q6 retune, QF
reopen, Cap-SR reopen, `admit.py`, and an R1-P2 challenger label.

`fee_source` is feebook. `queue_source` is rails. The hygiene module
supplies `content_fresh_flag` and `queue_attribution_bin`. The synthetic
fresh fixture bins to `(true, q3300)`, `(false, q3300)`, and
`(false, q10000)`. None of those in-memory flags are copied into the freeze
files. `fresh_vs_stale_gap` stays null.

Feebook, rails, Q, Cap-SR, Cap-SR-FX, C3, C5, R3-P3, and S5 match
`6626c6892298b015cf63688081545e27363226bc` for those trees.

## Limitations

- The conductor harness freeze sha256 claim
  `3318204bf6e962f4f3372dad8c0f302e62d85c26b855de7369718654d0114728`,
  the parent claim
  `9e6556c150c726b679ac8393f1f5338cf983489259b0f34cdedf221c030be795`,
  and the panel stub claim
  `38167d11da5842bc4d39e6e7dcaab20a67294c735ba14d8bbeafde3154c6342a`
  (~113 events) were not in this checkout. `lab/governance/astra/packets/`
  is absent. The committed markdown and the empty panel seed are
  recreations. Their hashes are the recreation hashes above. This page
  does not relabel them as the conductor bytes.
- The seed has zero events. S4A0 and S4A1 on that seed keep `event_count`
  0 and record `conductor_stub_absent_seed_not_invented`. The two-trade
  native partition and the three-row freshness bins are
  `fixtures/synthetic_native_trades.json` and
  `fixtures/synthetic_fresh_queue.json` with source
  `synthetic_schema_standin`. They are not a Kalshi GET and not an admitted
  cohort.
- `panel_admitted.json` is absent. `admitted_at` on the seed is null.
  Clock admit is still closed, so Examiner scoring stays closed.
- A public GET of open `KXNCAAFGAME` events was not stored. The first page
  returned 200 events and a cursor. That list is not the conductor stub
  and was not written into the panel.
- No Logan key was read. No order route exists in this lab. Loading
  hygiene does not import queue-fragility.
