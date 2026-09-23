# R2-P3 prop-slate capture slot (stub only)

**panel_version:** `2026-09-22.r2-p3-prop-slate-v0`  
**status:** no recorder running — the conductor stub is on disk (`admitted_at` null)  
**events:** 6, Sun 2026-09-27 LAC@BUF + BAL@DAL (`KXNFLPASSYDS`, `KXNFLRECYDS`, `KXNFLRSHYDS`)  
**panel stub sha256:** `70e879e8738d033f392d821849dee3537af3e7b8a916670779d238f78ce098be`  
**isolation:** separate from ADMIT-1, S1, S4, and S5 — do not steal poll budget  
**admit gate:** both games' T−7d starts are already past at stub time. Live `admit.py` is not run here.

This README is lab-authored. It is not a conductor-box byte. The panel stub
beside it is the conductor file, copied verbatim. `market_tickers` are
empty. Volume fields are null. ATL@GB stays in `excluded`.

`panel_admitted.json` is absent. When Clock join writes one, the harness
prefers that file and still refuses ATL@GB, live orders, and a non-null
`results` or `pnl`.

No recorder is started. The planned db path, if a later seat starts one, is
`lab/astra-capture/r2-p3-prop-slate/capture.sqlite`. GET-only. No Logan keys.
