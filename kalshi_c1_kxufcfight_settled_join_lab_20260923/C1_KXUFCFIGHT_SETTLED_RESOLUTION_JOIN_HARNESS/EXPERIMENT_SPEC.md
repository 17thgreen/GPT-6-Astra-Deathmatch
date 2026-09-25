# C1 KXUFCFIGHT settled-resolution join

September 24, 2026. This file is the hypothesis. It is committed before a
unit-test outcome is recorded. No figure in this document is a trading
result. This is measurement-only settled-resolution join. Feature family
C1-RJ. It is orthogonal to the C1 honesty lab and to the C1 EMPTY-OB
refuse harness. It is not a reopen of Cap-SR, FQ siblings, C3-RJ, C5-RJ,
R3P3-RJ, NHL-RJ, S4-RJ, R2P3-RJ, or S5-RJ.

## Pin gap

The implement order cites these bytes and says to commit them verbatim:

- Freeze `lab/governance/astra/packets/C1_KXUFCFIGHT_SETTLED_RESOLUTION_JOIN_HARNESS_FREEZE_2026-09-23.md`, sha256 `3ea3362ad3c16951369d5f90497ec6079213dd54e5556340c4d3738744126cf1`
- Conductor ACCEPT `lab/governance/astra/packets/CONDUCTOR_ACCEPT_C1_KXUFCFIGHT_SETTLED_JOIN_HARNESS_2026-09-24.json` (`implement` true, digests ALL_MATCH)
- Maximize pin `MAXIMIZE_PIN_2026-09-23_1750ET.md`
- Scout reget directory `lab/governance/astra/packets/scout_c1_settled_rejoin_2026-09-23/`

Those four were absent from `origin/main` at `a281adc944e4dacffcdb5677a140fabaed675a81`. They were not regenerated. They are present in this checkout under `lab/governance/astra/packets/`. `digest_all_match_claimed` is true. This markdown is not that freeze, and its own sha256 is not the cited freeze digest.

## What is on disk

The panel parent the order names
`lab/governance/astra/packets/C1_KXUFCFIGHT_PANEL_STUB_2026-09-22.json`
is a byte copy of `lab/astra-capture/c1-kxufcfight/panel_admitted.json`.
sha256 `24426d804c51bde23cf2557a11a8481a12026da10024094c4ae546d1f7d3956e`,
12396 bytes, `panel_version` `2026-09-22.c1-kxufcfight-v0`, top-level
`admitted_at` `2026-09-23T00:49:43Z`. The capture file was not rewritten.
The pre-admit stub `panel_stub.json` stays sha256
`2cc661d86202d3daf9ffa45320e39d249852a97490f458f72ab7ea8ec5c81a00`.
This lab does not run `admit.py` and does not write a new `admitted_at`.

The admitted panel has 2 events and 4 markets. Each market
`occurrence_datetime` equals its event `occurrence_datetime`.
`occurrence_source` is `live_get_market`. `kickoff_sot` is
`kalshi_occurrence_datetime`. J1 uses that `occurrence_datetime`. It does
not invent one, and it does not substitute `expected_expiration_time`.
`result_observed_live_get` is already on those four markets. This lab
reads that field for the J0 schema. It does not write a new settled
`result`, and it does not copy the declared scout N=4 into
`settled_join_n`.

Settled, finalized, and events list books are not in this checkout. They
are not invented. The four captured orderbooks stay the empty public GET
sha256 `e07d09f130e604a9e1acfc736fb57cbdfc33d8a5a253466a0cbd5c98cf6c9f74`.
Empty bid lists are not filled.

## Knob

One knob: `join_gate`.

| Arm | Name | Gate |
|---|---|---|
| J0 | Nonempty result required | `result_observed_live_get` is `yes` or `no` on the admitted parent seed |
| J1 | Occurrence datetime match | market `occurrence_datetime` equals the event clock when both are present |

`results`, `pnl`, `settled_join_n`, `occurrence_match_n`, and
`admit_ready_flag` stay null. Examiner status is `READY_NOT_SCORED`
(`stub_ready` true, `NOT_SCORED`). This supersedes the earlier
`HOLD_PRE_PR` wording. Examiner ACK
`lab/governance/astra/packets/C1_KXUFCFIGHT_SETTLED_JOIN_HARNESS/EXAMINER_ACK_C1_RJ_PR49_STUB_READY_NOT_SCORED_2026-09-24.json`
sha256 `3eb4900dcdf72d34247f25dfb259bf74193267c1e3a2983e8c4fd486e278bdec`.
Conductor ACCEPT
`lab/governance/astra/packets/CONDUCTOR_ACCEPT_EXAMINER_C1_RJ_PR49_STUB_READY_NOT_SCORED_2026-09-24.json`
sha256 `a964146f34a32527b75fb64011ead9a6e6013078474f8a54e208ba7c543f06d4`.
The scorecard remains null. Nothing was scored.

Feebook `22371178cb2663250b4762f328069571c48cb551` and rails
`6a28e0d6254327ea4e6451c781bec56215ac6cac` are fixed commits and are not
loaded. No fee arm. No live orders. No Logan keys. No Lee-Ready. No Arm B.
Does not ungate S1, S2, or R2-P4. Does not replace the Q6 candidate.
