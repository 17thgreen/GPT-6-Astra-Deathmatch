# C1 EMPTY-OB unit results

September 23, 2026. This file records a code check of the frozen empty-orderbook
refuse harness. It is a unit verification. It is not a simulated trading run
and not live validation. `FROZEN_EXPERIMENT.json` still has `results: null`
and `pnl: null`. `results/EMPTY_RESULTS.json` still has `empty_book_n`,
`scorecard_refuse_n`, `wait_fresh_depth_n`, and `depth_present_n` null.
Those fields stay null on purpose. This page is not profit, and it is not
folded back into the freeze hashes. No tape walk was run. No P&L figure is
reported. This is not an Examiner pass and not a live-order certification.

## Command

From `kalshi_c1_empty_ob_lab_20260923`, Python 3, standard library:

```bash
python3 -m unittest -v tests.test_orchestrator
```

Ran 7 tests in 0.026s at 2026-09-23T17:10:22Z. Result: OK. Failures: 0.
Errors: 0.

The checks that passed are the predeclared ones: harness freeze sha256
`1b9f8fbec8bad866e055bcabd38c8c633835d505cbd25c367ff0675bff3a4b27`; parent
kernel sha256
`a191c9b3f71030445d1d32684feb6dc1bf09abb7e09403d5dbdf1927eafc63c9`; admitted
panel sha256
`24426d804c51bde23cf2557a11a8481a12026da10024094c4ae546d1f7d3956e`,
`panel_version` `2026-09-22.c1-kxufcfight-v0`, `admitted_at`
`2026-09-23T00:49:43Z`, 2 events and 4 markets; four identical empty
orderbooks sha256
`e07d09f130e604a9e1acfc736fb57cbdfc33d8a5a253466a0cbd5c98cf6c9f74`; pin meta
sha256
`241d745e6ddfb6cccdc8f123e4d57d627635065c3406df8f66d0d0d2e168f4ca`. Fee pin
`22371178cb2663250b4762f328069571c48cb551` and rails pin
`6a28e0d6254327ea4e6451c781bec56215ac6cac` with those trees unchanged since
those commits. C1E0 `refuse_scorecard` raises `ScorecardPromotionRefused`.
C1E1 `wait_fresh_depth` leaves the four instrument fields, `results`, and
`pnl` null.

`fee_source` is feebook. `rails_source` is rails. Both are import-only.
No fee quote was written onto a book.

## Limitations

- The four pinned books are byte-identical empty `orderbook_fp` lists.
  Feebook reciprocal bids, asks, spreads, and touch sizes stay unset.
  `polarity_fill` raises `BookIncomplete`. That is not a fill and not a
  depth invention. `empty_book_n` stays null.
- C1E0 on those books raises `ScorecardPromotionRefused` after the empty
  touch check. The refuse is not counted into `scorecard_refuse_n`.
- C1E1 calls rails `content_fresh_flag` through the hygiene import. The
  first observation of an empty book is `initial` and the flag is true.
  A keepalive is not fresh. The flag is not depth. The bin name is
  `wait_fresh_depth`. `wait_fresh_depth_n` stays null. No fill object is
  returned.
- An in-memory book with one bid level is `depth_present_unscored` on
  C1E1 and still raises `ScorecardPromotionRefused` on C1E0.
  `depth_present_n` stays null. `attempt_fill` raises `InventFillRefused`
  and does not rewrite the payload. That in-memory level is not a pin and
  is not written under `orderbooks/`.
- Lee-Ready raises `LeeReadyRefused` on every input, including a row that
  asks for it. The pre-admit stub is refused. A `labeled_recreation` book
  is refused.
- The attached pre-ACCEPT payload sha256
  `b5ea41454dbb56be5456a2d9602304fcc249a2e3db8cba3cbb7e8eb7c080a4e1` is
  stored as `PRE_ACCEPT_EMPTY_RESULTS.json` and refused as a scorecard.
  It is labeled `pre-ACCEPT empty` and omits `wait_fresh_depth_n` and
  `depth_present_n`.
- Panel-level `admitted_at` is `2026-09-23T00:49:43Z`. Event and market
  `admitted_at` fields on that same file are null. This harness does not
  fill them in.
- `lab/governance/astra/` is absent. Packet bytes are the copies under the
  lab and under `packets/C1_EMPTY_OB_HARNESS/`. Production panel and
  orderbooks under `lab/astra-capture/c1-kxufcfight/` already matched the
  attached digests and were not rewritten.
- No public GET was issued by this harness. No Logan key was read. No
  order route exists in this lab. `admit.py` was not run. S2 and R2-P4
  stay queued. Examiner hold stays `NOT_SCORED` and `stub_ready` false.
  This run does not stamp READY.
- Sibling labs in `DOES_NOT_MODIFY`, including the C1 honesty lab,
  feebook, rails, L2-CAT, SOT-ID, R2-P3, and
  `nfl_prospective_recorder_20260922`, match
  `6f1e22e15d8841605be5c34711f202277f4b685d`.
