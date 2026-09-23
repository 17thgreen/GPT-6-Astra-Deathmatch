# R3-P4 L2-SF shape-object harness unit results

September 23, 2026. This file records a code check of the frozen L2-SF
harness. It is a unit verification. It is not a simulated trading run and
not live validation. `FROZEN_EXPERIMENT.json` still has `results: null` and
`pnl: null`. `results/EMPTY_RESULTS.json` still has
`sf1_median_half_spread_bps_by_mid_decile`, `sf2_l1_top10_depth_share`,
`sf2_kl_vs_uniform_1_10`, `n_books`, and `n_snapshots` null. Those fields
stay null on purpose. This page is not profit, and it is not folded back
into the freeze hashes. No tape walk was run. No P&L figure is reported.
This is not an Examiner score and not a live-order certification.

## Command

From `kalshi_r3p4_l2_sf_lab_20260923`, Python 3, standard library:

```bash
python3 -m unittest -v tests.test_orchestrator
```

Ran 7 tests in 0.069s at 2026-09-23T17:31:39Z. Result: OK. Failures: 0.
Errors: 0.

The checks that passed are the predeclared ones: fee pin
`22371178cb2663250b4762f328069571c48cb551` and rails pin
`6a28e0d6254327ea4e6451c781bec56215ac6cac` with those trees unchanged since
those commits; the packet, parent kernel, panel-stub, and six order-book
digests equal the attached conductor bytes; 4 events and 6 markets (sports
4, nonsports 2); preference for a temporary `panel_admitted.json` when that
file exists; a 5-market recreation refused; an empty seed refused; the
superseded digest prefix `e7c6b6d5` refused; R3P4S0 `sf1_half_spread` and
R3P4S1 `sf2_depth_kl` both see the full natural panel and do not promote a
scorecard; category slice is refused as an arm; one-sided recorded books
stay one-sided; synthetic SF1/SF2 identities stay out of the scorecard;
invented depth refused; Lee-Ready refused; ATL@GB refused; a supplied fee
literal refused; live orders, Logan keys, Q6 retune, QF reopen, Cap-SR
reopen, Cap-SR-FX reopen, L2-CAT reopen, EMPTY-OB reopen, PROP-LQ reopen,
SOT-ID reopen, PR13 dual-edit, S2/R2-P4 ungate, and `admit.py` refused.

`fee_source` is feebook. `rails_source` is rails. The PR13 base shape module
is imported read-only. On the synthetic ladder, both category labels stay
in each arm. `synthetic:flat10:sports` and `synthetic:flat10:nonsports`
quote half-spread 200 bps at mid 0.50 under R3P4S0, and L1 share 1/10 with
KL 0 under R3P4S1. Those in-memory labels are not copied into the freeze
files. Recorded TENN and MRST books are two-sided, so the selected algebra
runs in memory and is compared with the imported shape module. The named
scorecard fields stay null. PITT, BUCK, T76250, and T95749.99 each have one
empty side. That side is not filled, and the shape module raises
`BookIncomplete` on those books.

Feebook, rails, the PR13 base L2 shape lab, L2-CAT, EMPTY-OB, SOT-ID, Q,
Cap-SR, Cap-SR-FX, C3, C5, R3-P3, S4, S5, and R2-P3 match
`d7b935951c9ddd5e6c4d813fad69e401b6a7b6a3` for those trees.

## Conductor bytes

Verified sha256 on this branch:

- harness freeze `f00425261f085aef90e93b186810a0248165273f8bb923ef3597940a9e8345de`
- parent kernel `4a4e7cc61efcb436955c566edc7a2681603a014725bc79047f9d825392064528`
- panel stub `7477e023ab70c59a6739650155ddb9d77077766e3afd80443e540d60b5a86cbb` (4 events; 6 markets; sports 4; nonsports 2; `admitted_at` null)
- `SOURCE_PINS.json` `6ac2f00e75b60bc5b3b865d55f68b332cd87998e44c61d214445d66e348e84fa`
- conductor stamp `df5f52aa191ae31df81b95da3346b39e27f8870484f83826d3a9370f84835762`
- pre-ACCEPT empty `1362153d8ebb96d348184580a1d4fc4e5e6a0c030de3baf683f4664cef05fac0`, refused as a scorecard
- six `ob_*.json` files at the digests listed in `SOURCE_PINS.json`

`FREEZE_SHA256`, `PARENT_SHA256`, and `PANEL_STUB_SHA256` equal those
conductor digests. `conductor_pin_status` reports the matches and
`conductor_bytes_in_checkout` true. `results` and `pnl` stay null. The
2026-09-23T17:31:39Z unit run is code verification. It is not an Examiner
score.

## Limitations

- `lab/governance/astra/` is absent. The verified copies are the lab paths
  and `packets/R3_P4_L2_SF_HARNESS/`. Shared names already at `packets/`
  root (`PRE_ACCEPT_EMPTY_RESULTS.json`, `CONDUCTOR_FROZEN_EXPERIMENT.json`)
  belong to earlier packets and were not overwritten.
- `packets/r3_p4_l2_shape/live_get_2026-09-22/` stays absent because the
  closed L2-CAT harness pins that absence. The authentic order-book bytes
  are under this lab's `live_get_2026-09-22/` and the L2-SF packet copy.
- R3P4S0 and R3P4S1 on the conductor stub see 6 markets. They do not write
  a scorecard. Two-sided recorded books are probed in memory. One-sided
  books are not completed.
- The synthetic ladder is `fixtures/synthetic_two_sided_ladder.json` with
  source `synthetic_schema_standin`. It is not a Kalshi GET and not
  production depth.
- `panel_admitted.json` is absent. `admitted_at` on the seed is null.
  Clock admit is still closed, so Examiner scoring stays closed.
  `stub_ready` stays false.
- No Logan key was read. No order route exists in this lab. Loading the
  shape module does not edit the PR13 base lab. S2 and R2-P4 stay queued.
