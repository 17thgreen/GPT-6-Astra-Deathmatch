# EXT-K2 optimism-tax dependence stress

Frozen experiment `EXT-K2-OPTIMISM-TAX-DEPENDENCE-STRESS`.

The binding specification is the vendored freeze:

`pins/governance/VARIANTS_EXT_K2_OPTIMISM_TAX_DEPENDENCE_STRESS_FREEZE_2026-10-03.md`

sha256 `d69a4f627cb420b59bbc961b072d28242faeb9d21d5d29b9f90a77f6825acbce`

JSON twin sha256 `025a01a121e5b3a64a0b683a8030f9cbd1681f132365dadb419377d09d71ff6c`

Conductor ACCEPT sha256 `d76779e1a309388e6bc7f401a2c992a3be2015ae81ba910b8f5655fb10472fc0`

Commission sha256 `1f2c7f68396131d65ef31e492355c2937a9a0a91fb6cdf67c7d66e220f0b51f5`

Built from main `761eaaedc153dca9807d7630adcea1ae3387d9c1`.

## Execution split

Part (a) runs in this checkout on the dev tape. It splits the recorded 000 open-leg markout by taker-YES share regime. Outputs are aggregates. `results`, `pnl`, and `roi` stay null. The verdict is `DESCRIPTIVE`, `ITERATE`, or `INCONCLUSIVE`.

Part (b) is code plus synthetic tests. The runner `becker_pipeline/run_part_b.py` is for the Simulator on the box. It writes a pre-run receipt before any Becker price, side, or result, and it writes aggregates only outside this repo. This checkout does not contain Becker rows. No Becker aggregate is committed. `results_b/BOX_ONLY_OUTPUT_SHA256.json` leaves the output sha null.

## Inputs

K1 bundle sha256 `0f8f529733bfd1ccb01b36f312cdc20865cc2811c04dcd3c812d50c67295db38` (inner manifest `a041561e130fb97eaa8d7bfab5dd6fa53963fa4fbdb13c00cd4f71089e0e3db5`).

K2 bundle sha256 `963f7663a74527db38479bbf4a253870bd5dc6f99c8f85b70750d3600c65907f` (inner manifest `2e91d48f87e144031aa18fc4eb0f6d85953a7fa6c817bbfa4e5ba4af567931a3`).

There is no new knob. Primary horizon, tercile cuts, seeds, fee coefficients, and the band registry are the freeze pins.

## What this lab does not do

It does not retune 000. It does not place orders. It does not read `capture.sqlite` or `archive.sqlite`. It does not import a network client. It does not read nflverse. Becker evidence, when the Simulator later runs part (b), is at most tag `[A]`. An nflverse anchor is not used here.
