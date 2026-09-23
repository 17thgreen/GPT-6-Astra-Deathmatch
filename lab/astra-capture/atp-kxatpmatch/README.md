# ATP KXATPMATCH capture slot (stub only)

**panel_version:** `2026-09-23.atp-kxatpmatch-v0`  
**status:** no recorder running. `admitted_at` is null. `stub_status` is `NOT_ADMITTED`.  
**panel stub sha256:** `ed041c502d1f775d33c44bf900ac91b1339d99045bddd2052edd09a139ae2d3f`  
**scout hunt:** `packets/scout_cashcow_hunt_2026-09-22/scout_hunt_KXATPMATCH.json`  
**scout sha256:** `14c99ec8ea00bae507a21d0e6a1879fb94d32ef69ad4b5e3b40a9952821e5da7`

The stub file is the attached conductor bytes: 6 events and 12 markets. Each
market object is the scout-hunt object with the same ticker. No orderbook
ladder is stored in this directory. No recorder is started. `admit.py` is not
run. `lab/governance/astra/packets/` is not in this checkout.
