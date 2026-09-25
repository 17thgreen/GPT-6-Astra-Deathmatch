# Q6S1 KXATPMATCH inventory re-proof

September 25, 2026. This file is the hypothesis. It is committed with the
harness before a unit-test outcome is recorded in `results/UNIT_RESULTS.md`.
No figure in this document is a trading result. Q6 outcomes that already
exist are not re-labeled as evidence from this probe. This is measurement-only
inventory re-proof on KXATPMATCH. Feature family Q6S1-ATP-INVENTORY. The
series is `KXATPMATCH` only.

## Placement

The harness freeze is
`Q6S1_KXATPMATCH_INVENTORY_REPROOF_FREEZE_2026-09-25.md`, sha256
`d86f7a402ea63fb132d80480f844a954fe9061a27b9b6bed125f9785ae64640e`.
Those bytes are the attached Conductor freeze. The same bytes sit at the
lab root, the lab bundle, and `lab/governance/astra/packets/`.

Conductor ACCEPT sha256
`162100624297588516390aab51ba0161cf15d0659c439ec6b60e940b99845635`.

v2 pin bundle sha256
`62de476ec3d27b64183d1eba0d223c2c5ad61a6bc8abffde9873f6e76a5e633e`.

Panel stub: `lab/astra-capture/atp-kxatpmatch/panel_stub.json`,
`panel_version` `2026-09-23.atp-kxatpmatch-v0`, sha256
`ed041c502d1f775d33c44bf900ac91b1339d99045bddd2052edd09a139ae2d3f`.
`admitted_at` is null. 6 events and 12 markets. The capture file is not
rewritten. `panel_admitted.json` is absent. This harness does not write it
and does not run `admit.py`.

Scout hunt sha256
`14c99ec8ea00bae507a21d0e6a1879fb94d32ef69ad4b5e3b40a9952821e5da7`
(48 markets / 24 events) and sports-screen raw sha256
`b603474b3ca336b0a3678ff0deb8a937dfdcc4205e8e24db4d657d40d2323c60`
(28 markets / 14 events) are pins. They are not copied into scorecard
counts and they are not a replacement panel.

`digest_all_match_claimed` is false. Absent pins stay absent.

`SOURCE_PINS.json` sha256
`cddb85e83e679a101108c45cd82b2e9b59e68f9afd0d89d141a5bee0460376e7`
is identical at the governance packet, the lab root, and the lab bundle.

## Knob

One knob: `inventory_slice`.

- Q6S1A0 `flat_control`
- Q6S1A1 `inventory_bin_exposure`

ATP-FQ and ATP-RJ are import-only. `analysis_slice` and `join_gate` are
not arms. Feebook `22371178cb2663250b4762f328069571c48cb551` and rails
`6a28e0d6254327ea4e6451c781bec56215ac6cac` are fixed commits. The fee
label is cache-labeled `quadratic_with_maker_fees` multiplier 1.
`cache_labeled` is true. `live_r1p1` is false.

## Outputs

`inventory_delta_flat_vs_binned`, `unresolved_inventory`,
`position_bucket_gap`, `settled_join_n`, `n_books`, `results`, and `pnl`
stay null. Examiner scorecard v1.2 measured fields stay null. Examiner
status stays `HOLD_PRE_PR`. Public reads use the in-memory GET stub.
`live_gets` stays 0. `/orders` and `/portfolio` are refused. A hot
`/markets` path prefers `/events`.
