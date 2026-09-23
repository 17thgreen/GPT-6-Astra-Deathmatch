# ETH KXETH15M fee+queue honesty harness

Status: hypothesis committed, then source frozen. The unit page is
`results/UNIT_RESULTS.md` after the code check. That page is not profit and
not an Examiner pass. `EXPERIMENT_SPEC.md` is the hypothesis.
`FROZEN_EXPERIMENT.json` keeps `results` and `pnl` null.
`results/EMPTY_RESULTS.json` keeps `maker_vs_taker_roi_delta`,
`fresh_vs_stale_gap`, `settled_join_n`, and `n_books` null.

This lab is measurement-only. Feature family ETH-FQ. The series is
`KXETH15M`. The only knob is `analysis_slice`: ETHA0
`maker_vs_taker_native` and ETHA1 `content_fresh_vs_stale_bin`. Lee-Ready
is refused on every input. Fill density and `occurrence_datetime` are not
invented. On the attached hunt the missing `occurrence_datetime` count is
0, and that zero is the census, not a filled timestamp. The panel is the
full tiny hunt: 1 event and 1 market. The NFL `000` file is a pointer only.
S1 is not claimed green. S1, S2, and R2-P4 stay gated. C5 and ATP-FQ stay
closed. This is not live crypto trading.

`lab/governance/astra/packets/` is not in this checkout. The attached
freeze, scout hunt, panel stub, and accept on this branch match the
conductor sha256 claims. `SOURCE_PINS.json` lists those digests. It does
not contain the file bytes.

- Freeze `ETH_KXETH15M_FEEQUEUE_HARNESS_FREEZE_2026-09-23.md` sha256 `9cae3bad089e6e18bee22694a36a1a2c18db33935a315766cd6bd8f8476aa83a`
- Scout hunt `packets/scout_eth_kxeth15m_2026-09-23/scout_hunt_KXETH15M.json` sha256 `18f70001c8d68418d435e2016b756f90753e374a92d323f8e999f76215d9cf9c` (1 market / 1 event)
- Panel stub `lab/astra-capture/eth-kxeth15m/panel_stub.json` sha256 `b3379783c84eaa910f6a57f5318b8536f21220cfeaf0f73e9ff73ee0f20dd90d` (`2026-09-23.eth-kxeth15m-v0`, `admitted_at` null, full tiny hunt)
- Accept stamp sha256 `3e553395a47d5ced1a4b48d81b8d0d760d984becdbcb6c1dd574dafc39621a5e`

Fee pin `22371178cb2663250b4762f328069571c48cb551`.
Rails pin `6a28e0d6254327ea4e6451c781bec56215ac6cac`.
Those trees are not edited. The attached panel records series fee type
`quadratic` and multiplier 1. No feebook series override is written.

From this directory, Python 3.12 standard library:

```bash
python3 -m unittest -v tests.test_orchestrator
```

No Logan keys. No live orders. A passing unit run is not an Examiner score.
