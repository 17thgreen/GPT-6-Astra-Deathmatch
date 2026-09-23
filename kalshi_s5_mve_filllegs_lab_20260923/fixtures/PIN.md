# S5 fill-vs-legs harness pins

Measurement only. Feature family MVE-FL. Scorecard fields stay null until
Examiner after Clock admit. RFQ is out of scope.

| Pin | Value |
|---|---|
| Harness freeze sha256 | `8a118e6f1fdc8c22c6e559f395667aedffa5d270d067e39b6ae3ee24b2046d16` |
| Parent kernel sha256 | `a28932ba13b4913b69c48b73dde8ba066cebd212670d0b1cbb5ea8e93734b8ba` |
| Panel stub sha256 | `4918b820d454c5f997ea100917859f7e9467d92933bed1bc8a55c81ab8ce5b8e` |
| Panel version | `2026-09-22.s5-kxmvecrosscategory-v0` |
| Admitted at | null on the stub. `panel_admitted.json` is absent |
| Seed | 5 markets, 21 events, `mve_selected_legs` on 5/5 |
| Fee | `kalshi_feebook_lab_20260922` @ `22371178cb2663250b4762f328069571c48cb551` |
| Series override | `quadratic_with_combo_maker_fees`, multiplier 1 |
| Rails | `kalshi_rails_lab_20260922` @ `6a28e0d6254327ea4e6451c781bec56215ac6cac` |
| Untouched base | `79347f0ed8562f7df8d539e79a1cb15985d8abfe` |
| Knob | `leg_mid_source` |
| S5L0 | `tob_1m` |
| S5L1 | `synthetic_leg_product` |
| Synthetic product | `fixtures/synthetic_leg_product.json` |

`lab/governance/astra/packets/` is not in this checkout. Copies live beside
the lab and under `packets/S5_KXMVECROSSCATEGORY_FILLLEGS_HARNESS/`.

S4 NCAAF and R2-P3 stay queued. No Logan keys. No live orders. No RFQ.
No R1-P4 strategy. No Q6-`000` retune. No queue-fragility reopen. No `admit.py`.
