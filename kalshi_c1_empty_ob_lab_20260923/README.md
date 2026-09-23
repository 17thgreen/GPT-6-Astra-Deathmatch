# C1 EMPTY-OB harness

Status: hypothesis committed, then source frozen. Scorecard fields stay null.
`EXPERIMENT_SPEC.md` is the hypothesis. `results/EMPTY_RESULTS.json` keeps
`empty_book_n`, `scorecard_refuse_n`, `wait_fresh_depth_n`,
`depth_present_n`, `results`, and `pnl` null. The unit page is
`results/UNIT_RESULTS.md` after the code-verification run. That page is not
an Examiner score.

This lab is measurement-only. Feature family EMPTY-OB. The only knob is
`empty_book_gate`: C1E0 `refuse_scorecard` and C1E1 `wait_fresh_depth`.

`lab/governance/astra/` is not in this checkout. Authentic copies:

| File | sha256 |
|---|---|
| `C1_EMPTY_OB_HARNESS_FREEZE_2026-09-23.md` | `1b9f8fbec8bad866e055bcabd38c8c633835d505cbd25c367ff0675bff3a4b27` |
| `C1_KXUFCFIGHT_MEASUREMENT_FREEZE_KERNEL_2026-09-22.md` | `a191c9b3f71030445d1d32684feb6dc1bf09abb7e09403d5dbdf1927eafc63c9` |
| `C1_KXUFCFIGHT_PANEL_ADMITTED_2026-09-22.json` | `24426d804c51bde23cf2557a11a8481a12026da10024094c4ae546d1f7d3956e` |
| four empty orderbooks | `e07d09f130e604a9e1acfc736fb57cbdfc33d8a5a253466a0cbd5c98cf6c9f74` |
| `PIN_SHA256.json` | `241d745e6ddfb6cccdc8f123e4d57d627635065c3406df8f66d0d0d2e168f4ca` |

The same files sit at the lab root, `C1_EMPTY_OB_HARNESS/`, `packets/`, and
`packets/C1_EMPTY_OB_HARNESS/`. Production panel and orderbooks under
`lab/astra-capture/c1-kxufcfight/` match those digests and are not rewritten.
Digests are also listed in `SOURCE_PINS.json`.

Conductor stamp `CONDUCTOR_FROZEN_EXPERIMENT.json` sha256
`9adb8a8d30884abac8f4a82aafc0c2b57418a6f1e02341ff54bc46f2595456f5`
is the attached `FROZEN_EXPERIMENT.json` bytes.
Pre-ACCEPT empty payload `PRE_ACCEPT_EMPTY_RESULTS.json` sha256
`b5ea41454dbb56be5456a2d9602304fcc249a2e3db8cba3cbb7e8eb7c080a4e1`
is the attached `EMPTY_RESULTS.json` bytes. It is refused as a scorecard.

Panel `2026-09-22.c1-kxufcfight-v0`, admitted_at `2026-09-23T00:49:43Z`,
2 events / 4 markets.

Fee pin `22371178cb2663250b4762f328069571c48cb551` (import only).
Rails pin `6a28e0d6254327ea4e6451c781bec56215ac6cac` (import only).
Those trees are not edited. The C1 honesty lab and the ADMIT-1 recorder
are not edited.

From this directory, Python 3 standard library:

```bash
python3 -m unittest -v tests.test_orchestrator
```

C1E0 on the pinned empty books raises `ScorecardPromotionRefused`.
C1E1 returns a wait bin and a rails `content_fresh_flag`. That flag is not
depth and is not written into the null scorecard. Lee-Ready is refused.
This packet does not ungate S2 or R2-P4. Examiner status stays `NOT_SCORED`.
