# C1-EMPTY-OB-HARNESS packet bundle

`lab/governance/astra/` is not in this checkout. This directory is the
packets-side copy. The same authentic bytes sit in
`kalshi_c1_empty_ob_lab_20260923/C1_EMPTY_OB_HARNESS/` and at the lab root.
Top-level copies of the conductor files also sit in `packets/`.

| File | Role |
|---|---|
| `C1_EMPTY_OB_HARNESS_FREEZE_2026-09-23.md` | Harness freeze, sha256 `1b9f8fbec8bad866e055bcabd38c8c633835d505cbd25c367ff0675bff3a4b27` |
| `C1_KXUFCFIGHT_MEASUREMENT_FREEZE_KERNEL_2026-09-22.md` | Parent kernel, sha256 `a191c9b3f71030445d1d32684feb6dc1bf09abb7e09403d5dbdf1927eafc63c9` |
| `C1_KXUFCFIGHT_PANEL_ADMITTED_2026-09-22.json` | Admitted panel, sha256 `24426d804c51bde23cf2557a11a8481a12026da10024094c4ae546d1f7d3956e`, 2 events / 4 markets, admitted_at `2026-09-23T00:49:43Z` |
| `orderbooks/*.json` | Four identical empty books, sha256 `e07d09f130e604a9e1acfc736fb57cbdfc33d8a5a253466a0cbd5c98cf6c9f74` |
| `PIN_SHA256.json` | Pin meta, sha256 `241d745e6ddfb6cccdc8f123e4d57d627635065c3406df8f66d0d0d2e168f4ca` |
| `CONDUCTOR_FROZEN_EXPERIMENT.json` | Attached conductor stamp bytes, `results` and `pnl` null |
| `PRE_ACCEPT_EMPTY_RESULTS.json` | Attached pre-ACCEPT payload. Refused as a scorecard |
| `CONDUCTOR_ACCEPT_C1_EMPTY_OB_HARNESS_2026-09-23.json` | ACCEPT+IMPLEMENT GO |
| `EXAMINER_HOLD_C1_EMPTY_OB_HARNESS_PRE_PR_2026-09-23.json` | Pre-PR hold, `NOT_SCORED`, `stub_ready` false |
| `SOURCE_PINS.json` | Digest index. Not a substitute for the file bytes |
| `FROZEN_EXPERIMENT.json` | Lab freeze record, scorecard null |
| `results/EMPTY_RESULTS.json` | Same empty scorecard bytes as `results.json` |

Feature family EMPTY-OB. Scorecard fields stay null.
This packet does not ungate S2 or R2-P4.
