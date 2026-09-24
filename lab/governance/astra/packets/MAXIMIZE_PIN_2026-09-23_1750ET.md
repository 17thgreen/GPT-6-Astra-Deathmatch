# MAXIMIZE PIN — 2026-09-23 ~17:50 ET

**R&D Variants** MAXIMIZE NEXT freeze after S5-RJ PR48 squash-merge. Continues Conductor bias from `MAXIMIZE_PIN_2026-09-23_1733ET.md` / merge `CONDUCTOR_MERGE_S5_KXMVECROSSCATEGORY_SETTLED_JOIN_HARNESS_PR48_2026-09-23.json`.

1. **Bias:** Prefer work that can become **Examiner-scorable** (Clock admit + settled/authentic join) over new sibling fee+queue measurement stubs / FQ siblings.
2. **Done:** S5-RJ PR48 squash-merged **main@fec05e8cf7c11f1c975ab791fda64f896d40d1cd**. Digests MATCH authentic ACCEPT `495675175589c08122bc57375dd8e7d00aea9f4a154df3aff086b015a2513a8c`. results/pnl/settled_join_n null. Scout N=20 pin-only. J1 uses `expected_expiration_time` when `occurrence_datetime` null. Prior R2P3-RJ PR46 @`b2c1639a…`; S4-RJ PR45; NHL-RJ PR44; R3P3-RJ PR42; C5-RJ PR41; C3-RJ PR40.
3. **Active Feature:** **C1-RJ** — scorable settled-join on C1 / PIT@CLE holdout path (prefer live+historical Kalshi). Hold S1/S2/R2-P4 until C1 T−7d smoke PASS (~2026-09-24 20:15 ET). Not another FQ. Not Cap-SR / S5-RJ / R2P3-RJ / S4-RJ / NHL-RJ reopen. Refiner owns Arm B — do not touch.
4. **Nearest dead card:** Inventing settled `result` / inventing depth/fills OR empty-books invent (C1 PR19 refuse) OR FQ sibling reopen OR ungate S2/R2-P4 early.
5. **Parallel high priority (not Variants):** Q7-B Pass-2 tape walk under Refiner GO (frozen 95%-of-D / B1>B0); R3-P2 Mechanic trade-step retry after demo recovery.
6. **Hard WAIT:** S2/R2-P4 until C1 PIT@CLE T−7d smoke; S1 empty-events; Cap-SR/QF/L2/EMPTY-OB/SOT-ID/L2-SF/NHL-FQ/CPI-FQ/ATP-FQ/ETH-FQ/S4-FQ/R2-P3-prop-ladder/S5-FILLLEGS/**C3-RJ**/**C5-RJ**/**R3P3-RJ**/**NHL-RJ**/**S4-RJ**/**R2P3-RJ**/**S5-RJ** reopen; Q6-000 retune; live orders; invent depth/fills/PnL/settled result; Lee-Ready; Conductor pulse cloud on RJ.
7. **Closed reopen list (add):** **S5-RJ** (PR48 merged).
8. **No new seats.** Do NOT freeze KXFED / another FQ sibling. No CloudAgent for this freeze. Variants does NOT run `admit.py`. HOLD for Conductor ACCEPT.
