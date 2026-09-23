# R3-P4 L2-CAT category-slice harness unit results

September 23, 2026. This file records a code check of the frozen L2-CAT
harness. It is a unit verification. It is not a simulated trading run and
not live validation. `FROZEN_EXPERIMENT.json` still has `results: null` and
`pnl: null`. `results/EMPTY_RESULTS.json` still has
`sf1_median_half_spread_bps_by_mid_decile`, `sf2_l1_top10_depth_share`,
`sf2_kl_vs_uniform_1_10`, `sports_vs_nonsports_sf_gap`, `n_books`, and
`n_snapshots` null. Those fields stay null on purpose. This page is not
profit, and it is not folded back into the freeze hashes. No tape walk was
run. No P&L figure is reported. This is not an Examiner score and not a
live-order certification.

## Command

From `kalshi_r3p4_l2_cat_lab_20260923`, Python 3.12, standard library:

```bash
python3 -m unittest -v tests.test_orchestrator
```

Ran 7 tests in 0.043s at 2026-09-23T16:35:47Z. Result: OK. Failures: 0.
Errors: 0.

The checks that passed are the predeclared ones: fee pin
`22371178cb2663250b4762f328069571c48cb551` and rails pin
`6a28e0d6254327ea4e6451c781bec56215ac6cac` with those trees unchanged since
those commits; the packet, parent kernel, and panel-stub digests equal the
attached conductor claims; 4 events and 6 markets (sports 4, nonsports 2);
preference for a temporary `panel_admitted.json` when that file exists; a
5-market recreation refused; an empty seed refused; the superseded digest
prefix `e7c6b6d5` refused; R3P4C0 `sports_only` and R3P4C1 `nonsports_only`
partition the stub without scoring recorded books; synthetic SF1/SF2
identities stay out of the scorecard; invented depth refused; Lee-Ready
refused; ATL@GB refused; a supplied fee literal refused; live orders, Logan
keys, Q6 retune, QF reopen, Cap-SR reopen, Cap-SR-FX reopen, and `admit.py`
refused.

`fee_source` is feebook. `rails_source` is rails. The PR13 base shape module
is imported read-only. On the synthetic ladder, `synthetic:sports:flat10`
quotes half-spread 200 bps at mid 0.50 with L1 share 1/10 and KL 0. The
nonsports touch quotes mid 0.35, decile 3, L1 share 1, and KL equal to
ln(10). Those in-memory labels are not copied into the freeze files.
`sf1_median_half_spread_bps_by_mid_decile` stays null. A one-sided synthetic
book is refused rather than filled with invented depth. A keepalive row
stays stale under the rails predicate.

Feebook, rails, the PR13 base L2 shape lab, Q, Cap-SR, Cap-SR-FX, C3, C5,
R3-P3, S4, S5, and R2-P3 match `3b0d1429b9ea702f2cb242e79f21f5ab5d3f18a6`
for those trees.

## Conductor bytes

Verified sha256 on this branch:

- harness freeze `3fc370d93f0ea42864f7bf482d7f6515254999c76e2fc4477df1273bfcdc051f` at the lab root, the lab bundle, `packets/R3_P4_L2_CAT_HARNESS_FREEZE_2026-09-23_2259.md`, and `packets/R3_P4_L2_CAT_HARNESS/`
- parent kernel `4a4e7cc61efcb436955c566edc7a2681603a014725bc79047f9d825392064528` at the same four locations
- panel stub `7477e023ab70c59a6739650155ddb9d77077766e3afd80443e540d60b5a86cbb` at `lab/astra-capture/r3-p4-l2-shape/panel_stub.json` (4 events; 6 markets; sports 4; nonsports 2; `admitted_at` null; `half_spread_bps` and `l2_shape` null) and at the lab bundle and `packets/R3_P4_L2_CAT_HARNESS/`
- seed summary `e0d5281133d89d5f0215a8f02ae438b688bf53e4a48f2eb4c3727db4a29bb6f2`
- conductor stamp `6108488d33a4be6ece3235fa5b5a39cf563e97a543e3d8ec9828c4f5bea8ba9e`

`PACKET_SHA256`, `KERNEL_SHA256`, and `PANEL_STUB_SHA256` equal those
conductor digests. `conductor_pin_status` reports all three matches and
`conductor_bytes_in_checkout` true. The panel stub loads as 4 events and 6
markets. `results` and `pnl` stay null. The 2026-09-23T16:35:47Z unit run
is code verification. It is not an Examiner score.

## Limitations

- `lab/governance/astra/packets/` is absent. The verified copies are the
  lab paths and `packets/` paths listed above. The capture README is
  lab-authored and is not a conductor-box byte.
- R3P4C0 and R3P4C1 on the conductor stub report market counts 4 and 2.
  They do not write a scorecard. Recorded order books inside the stub are
  counted and are not reduced to SF1 or SF2.
- The synthetic ladder is `fixtures/synthetic_mid_depth_ladder.json` with
  source `synthetic_schema_standin` and book ids `synthetic:sports:flat10`
  and `synthetic:nonsports:touch`. It is not a Kalshi GET and not production
  depth.
- `panel_admitted.json` is absent. `admitted_at` on the seed is null.
  Clock admit is still closed, so Examiner scoring stays closed.
- `packets/r3_p4_l2_shape/live_get_2026-09-22/` is absent. It was not
  invented. The seed summary is the import-only supporting fixture.
- No Logan key was read. No order route exists in this lab. Loading the
  shape module does not edit the PR13 base lab.
