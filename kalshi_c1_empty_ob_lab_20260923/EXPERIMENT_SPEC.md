# C1 KXUFCFIGHT empty-orderbook refuse harness

Status: hypothesis committed before a unit outcome. Feature family EMPTY-OB.
The only knob is `empty_book_gate`.

| Arm | Gate | Empty book |
|---|---|---|
| C1E0 | `refuse_scorecard` | `ScorecardPromotionRefused`. Lee-Ready refused. Bids stay empty |
| C1E1 | `wait_fresh_depth` | Wait bin only. Rails `content_fresh_flag` is a freshness label, not depth. `results` and `pnl` stay null. No fills |

The subject is the admitted C1 panel (`2026-09-22.c1-kxufcfight-v0`,
`admitted_at` `2026-09-23T00:49:43Z`, 2 events / 4 markets) and the four
identical empty `orderbook_fp` files. Fee and rails are import-only:

- `kalshi_feebook_lab_20260922` @ `22371178cb2663250b4762f328069571c48cb551`
- `kalshi_rails_lab_20260922` @ `6a28e0d6254327ea4e6451c781bec56215ac6cac`

`empty_book_n`, `scorecard_refuse_n`, `wait_fresh_depth_n`, `depth_present_n`,
`results`, and `pnl` stay null until Examiner. A content-fresh flag on the
first observation of an empty book is not a depth count and is not copied
into those fields.

This packet does not ungate S2 or R2-P4. It does not reopen Cap-SR, QF,
L2-CAT, PROP-LQ, or SOT-ID. It does not retune Q6-`000`. It does not run
`admit.py`, read Logan keys, or place orders. GET-only offline pins. No
invented depth, fills, or PnL.

`lab/governance/astra/` is absent. Authentic copies live at the lab root,
`C1_EMPTY_OB_HARNESS/`, `packets/`, and `packets/C1_EMPTY_OB_HARNESS/`.
Production bytes already at `lab/astra-capture/c1-kxufcfight/` are checked,
not rewritten.

The attached pre-ACCEPT `EMPTY_RESULTS.json` is stored as
`PRE_ACCEPT_EMPTY_RESULTS.json` and is refused as a scorecard.
