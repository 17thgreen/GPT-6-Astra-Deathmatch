# C4 KXCPI capture slot (stub only)

**panel_version:** `2026-09-23.c4-kxcpi-v0`  
**status:** no recorder running. `admitted_at` is null. `stub_status` is `NOT_ADMITTED`.  
**panel stub sha256:** `b20b0cbee50c127d2e9bb2548b574b7d643cc708f54019d53bd91775f9762c13`  
**scout hunt:** `packets/scout_cashcow_hunt_2026-09-22/scout_hunt_KXCPI.json`  
**scout sha256:** `6033907bb739bc00c41c796a3c1ed24553e0b7a44116ec3ea4bbaf39066bdcc8`

The stub file is the attached conductor bytes: 4 events and 44 markets. Each
market object is the scout-hunt object with the same ticker. Twenty-one
markets keep a null `occurrence_datetime`. The `KXCPI-26NOV` event
`occurrence_datetime` stays null. No orderbook ladder is stored in this
directory. No fill density is stored. No recorder is started. `admit.py` is
not run. `lab/governance/astra/packets/` is not in this checkout.
