# Q6S5 KXMLBSPREAD strategy-fill scorability

Measurement lab for the accepted Sep-25 scorability freeze. It places quotes from pinned books, models fills from later prints, and joins settlement dollars only after those fills are hashed.

The Examiner file in this directory is `HOLD_PRE_PR`. This lab does not place orders and does not open a network client.

Verify from this directory:

```bash
python3 -m unittest discover -s tests -v
```

Do not run pytest from this directory. The vendored pin tree is not a test suite.

`results/EMPTY_RESULTS.json` keeps results, pnl, roi, and the arm metrics null. Structural counts, when recorded, live in `results/UNIT_RESULTS.md`.
