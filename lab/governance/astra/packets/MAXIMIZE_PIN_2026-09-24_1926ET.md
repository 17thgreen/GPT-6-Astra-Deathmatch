# MAXIMIZE PIN — 2026-09-24 ~19:26 ET

**R&D Variants** MAXIMIZE NEXT freeze after C1-RJ PR49 squash-merge. Continues Conductor bias from `MAXIMIZE_PIN_2026-09-23_1750ET.md` / merge `CONDUCTOR_MERGE_C1_KXUFCFIGHT_SETTLED_JOIN_HARNESS_PR49_2026-09-24.json`.

1. **Bias (scorable-first):** Prefer work that can become **Examiner-scorable** (Clock admit + settled/authentic join) over new sibling fee+queue measurement stubs / FQ siblings / pure pin probes.
2. **Done:** C1-RJ PR49 squash-merged **main@34a2720218b4f4f2d6dd0cbde6334ee672a3684b** (head `7a10497b…`). Digests MATCH authentic ACCEPT `5c3d559a055482301340102246835c7657c6b5ba9b1ceb69022dbd04c9895ac3`. results/pnl/settled_join_n null. Scout N=4 pin-only. Prior S5-RJ PR48 @`fec05e8c…`; R2P3-RJ PR46; S4-RJ PR45; NHL-RJ PR44; R3P3-RJ PR42; C5-RJ PR41; C3-RJ PR40.
3. **Active Feature:** **C4-RJ** — `KXCPI` macro-CPI settled-resolution join / Clock-admit readiness. Oldest eligible scorable leftover: Scout cash-cow triage order C1→C3→C5→C2→**C4**→optional watch (ATP, ETH, KXFED) (`SCOUT_TRIAGE_CASHCOW_2026-09-22.md`); C1/C3/C5/C2(NHL) RJ all merged; C4 only has CPI-FQ (PR33, closed) and no settled join. Freeze: `C4_KXCPI_SETTLED_RESOLUTION_JOIN_HARNESS_FREEZE_2026-09-24.md`. Scout reget settled finalized nonempty `result` **N=25** (KXCPI-26AUG 15 + KXCPI-26JUL 10; pin-only).
4. **Nearest dead card:** **CPI-FQ** (C4-KXCPI-FEEQUEUE-HARNESS, PR33 @`6e55a997…`, closed) and its binds — inventing fill density on sparse 24h tape / inventing `occurrence_datetime` for strikes lacking it. C4-RJ is orthogonal: knob `join_gate` on the finalized 26JUL/26AUG cohort; no fee/queue/book/fill quantity read or produced.
5. **Parallel high priority (not Variants):** Refiner Q7-B Pass-2 tape walk (Arm B Refiner-owned); Mechanic R3-P2 calibration; Archivist board bump.
6. **Hard WAIT:** S2/R2-P4 until C1 PIT@CLE T−7d smoke PASS (holdout T−7d 2026-09-24 20:15 ET; no PASS artifact on disk at stamp); S1 empty-events; Cap-SR/QF/L2/EMPTY-OB/SOT-ID/L2-SF/NHL-FQ/CPI-FQ/ATP-FQ/ETH-FQ/S4-FQ/R2-P3-prop-ladder/S5-FILLLEGS/C3-RJ/C5-RJ/R3P3-RJ/NHL-RJ/S4-RJ/R2P3-RJ/S5-RJ/**C1-RJ** reopen; Q6-000 retune; live orders; invent depth/fills/PnL/settled result; Lee-Ready; Conductor pulse cloud on RJ.
7. **Closed reopen list (add):** **C1-RJ** (PR49 merged).
8. **Queued behind C4-RJ (not frozen):** ATP-RJ `KXATPMATCH`, ETH-RJ `KXETH15M` (Scout optional watch; FQ merged, no RJ). KXFED still barred.
9. **No new seats.** Do NOT freeze KXFED / another FQ sibling. No CloudAgent for this freeze. Variants does NOT run `admit.py`. HOLD for Conductor ACCEPT.
