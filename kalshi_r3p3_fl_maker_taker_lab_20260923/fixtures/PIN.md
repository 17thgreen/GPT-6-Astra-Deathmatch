# R3-P3 FL maker/taker harness pins

Measurement only. Lee-Ready refused. Scorecard fields stay null until
Examiner after Clock admit.

| Pin | Value |
|---|---|
| Harness freeze sha256 | `fbc58539b7a469d005b7f75b786efddecc1028a3bb0da601bc0082c9d4aab179` |
| Parent kernel sha256 | `0ed697149136acb3aa840aeeb79d11c8f6ef80f37ce4dd692a3cb690212206a7` |
| Panel stub sha256 | `6f640dd3a6091ba6b896ded38fdded4676583aa3c885223da21ddf03780250c0` |
| Bands registry sha256 | `0860cbe28d28ecc6142ddf6f1ebb67792084264ed82e0b4d868c3b3138ea5312` |
| Panel version | `2026-09-22.r3-p3-fl-maker-taker-v0` |
| Admitted at | null on the stub. `panel_admitted.json` is absent |
| Fee | `kalshi_feebook_lab_20260922` @ `22371178cb2663250b4762f328069571c48cb551` |
| Rails | `kalshi_rails_lab_20260922` @ `6a28e0d6254327ea4e6451c781bec56215ac6cac` |
| Untouched base | `637644966bae3737b52ab35826d3a63bf4b9b936` (C3 PR22). C3 and C5 are not edited |
| Knob | `analysis_slice` |
| R3P3A0 | `maker_vs_taker` |
| R3P3A1 | `fl_bands_10c` |
| Lee-Ready | refused. Native `taker_outcome_side` / `taker_book_side` only |
| Synthetic trades | `fixtures/synthetic_trades.json` |

`lab/governance/astra/packets/` is not in this checkout. Copies live beside
the lab and under `packets/R3_P3_FL_MAKER_TAKER_HARNESS/`.

No Logan keys. No live orders. No paper EV. No invented settlement. No
Q6-`000` retune. No queue-fragility reopen.
