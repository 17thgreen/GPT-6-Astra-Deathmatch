# EXT-K1 Q6-000 legging-risk audit

Measurement-only lab for the frozen audit `EXT-K1-Q6000-LEGGING-RISK-AUDIT`.
The specification is `EXPERIMENT_SPEC.md`, byte-identical to the vendored freeze.
This lab reads the recorded Q6-000 replay ledger. It does not re-run 000, retune 000,
place orders, or call Kalshi.

The refusal gate is primary: an opening fill is refused when Kalshi is more than 2 cents
richer than the nflverse consensus on that side (`x = 0.02`, `E = 0`, proportional de-vig).
The 16-cell grid is sensitivity only and does not pick a winner.

Every consensus-using output is tagged `EX_POST_ANCHOR_U`. The anchor is ex-post only.
The verdict is `DESCRIPTIVE`, `ITERATE`, or `INCONCLUSIVE`.

## Run

From this directory:

```bash
python3 -m unittest discover -s tests -v
```

Inputs are the vendored pin bundle `pins/EXT_K1_authentic_pins_2026-10-03.tgz`
(sha256 `0f8f529733bfd1ccb01b36f312cdc20865cc2811c04dcd3c812d50c67295db38`).
The runner hashes each manifest path before parsing it. `*.jsonl.gz` is gitignored,
so `q3300_d0.25_000_fills.jsonl.gz` is force-added from the bundle and is not regenerated.
The account class is an Examiner pin and stays null. Headline fees are the
non-direct `$0.01` per-order round-up, labeled `CACHE_NOT_R1P1`.
