# S4 KXNCAAFGAME capture slot (stub only)

**panel_version:** `2026-09-22.s4-kxncaafgame-v0`  
**status:** no recorder running — SCHEMA_STUB_SEED only (`admitted_at` null)  
**isolation:** separate from ADMIT-1 (`prospective/`), S1 (`s1-kxmlbgame/`), R2-P3 (`r2-p3-prop-slate/`), S5 — **do not steal poll budget**  
**admit gate:** T−7d already past for all Sat 2026-09-26 (`26SEP26`) seeded events at stub time → live admit.py would REFUSE_PAST_TMINUS7D; wait Clock join. Do not backfill. Do not start recorder.

Artifacts:
- Panel stub: `lab/governance/astra/packets/S4_KXNCAAFGAME_PANEL_STUB_2026-09-22.json`
- Schema: `lab/governance/astra/registry/schemas/s4_kxncaafgame_panel.schema.json`
- Capture plan: `lab/governance/astra/packets/S4_KXNCAAFGAME_CAPTURE_PLAN_2026-09-22.md`
- Freeze: `lab/governance/astra/packets/S4_KXNCAAFGAME_MEASUREMENT_FREEZE_KERNEL_2026-09-22.md` (sha `9e6556c150c726b679ac8393f1f5338cf983489259b0f34cdedf221c030be795`)
- Scout: `lab/governance/astra/packets/scout_s4_kxncaafgame/` (results/pnl null)

When Clock join + Conductor greenlight admit (and T−7d rule allows): write admitted panel here, start recorder with **this** db path only (`lab/astra-capture/s4-kxncaafgame/capture.sqlite`).
