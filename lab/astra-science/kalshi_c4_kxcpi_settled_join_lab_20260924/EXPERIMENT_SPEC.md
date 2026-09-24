# C4 KXCPI settled-resolution join

September 24, 2026. This file is the hypothesis. It is committed before a
unit-test outcome is recorded. No figure in this document is a trading
result. This is measurement-only settled-resolution join. Feature family
C4-RJ. One knob: `join_gate`.

Nearest dead card: CPI-FQ, PR33 at `6e55a99790f4cc09a437d2e16ccf4e8e826a154b`.
CPI-FQ varied `analysis_slice` on the active pre-release KXCPI ladder and
read fee and queue quantities. C4-RJ varies only `join_gate` on
already-settled KXCPI markets. It reads and produces no fee, queue, book,
fill, or tape metric. C4 fill, tape, queue, and fee stay HELD. Only this
settled-resolution join is lifted.

## Pins

The implement bundle was committed byte-for-byte before this hypothesis.
Conductor ACCEPT `8a86ae6b9dfb0e80d80de8404750501e44aeb873e7f31789ece5fddf8dd03fc5`
has `implement` true. Base is main at
`34a2720218b4f4f2d6dd0cbde6334ee672a3684b`.

| Pin | Path | sha256 |
|---|---|---|
| Freeze | `lab/governance/astra/packets/C4_KXCPI_SETTLED_RESOLUTION_JOIN_HARNESS_FREEZE_2026-09-24.md` | `5e37f81a8959e83c3d2c0c42739e1ca6c127c748442ac6fe28c0013edee12e2f` |
| Conductor ACCEPT | `lab/governance/astra/packets/CONDUCTOR_ACCEPT_C4_KXCPI_SETTLED_JOIN_HARNESS_2026-09-24.json` | `8a86ae6b9dfb0e80d80de8404750501e44aeb873e7f31789ece5fddf8dd03fc5` |
| Maximize pin | `lab/governance/astra/packets/MAXIMIZE_PIN_2026-09-24_1926ET.md` | `4ee450ffe2b99154c08fd8619892ca2dc8efec92fb036fad2ad70d5c6e003e2f` |
| Examiner HOLD | `lab/governance/astra/packets/EXAMINER_HOLD_C4_KXCPI_SETTLED_JOIN_HARNESS_PRE_PR_2026-09-24.json` | `8625cb4906b6dd1dd02bf2648178c8c3ae08c0d407cd9ca29bbe9f67bbb59dfd` |
| Scout reget | `lab/governance/astra/packets/scout_c4_settled_rejoin_2026-09-24/scout_settled_rejoin_C4_KXCPI.json` | `bb72a2ebfa942026913687e4c040a9def598b5080294a346d71f8f7283ab5f7f` |
| Seed summary | `lab/governance/astra/packets/scout_c4_settled_rejoin_2026-09-24/SEED_SETTLED_SUMMARY.json` | `8b749373c6949a1aa40b6852e313b0c626da0d0623fcafe167a8196ec228e0bf` |
| Panel stub | `lab/astra-capture/c4-kxcpi/panel_stub.json` | `b20b0cbee50c127d2e9bb2548b574b7d643cc708f54019d53bd91775f9762c13` |
| Settled reget | `lab/governance/astra/packets/scout_c4_settled_rejoin_2026-09-24/settled_reget_2026-09-24.json` | `235c9dad7d244db4c91152c8ae3f6d043f6732d31f99b05bc836abaf2f5d3f56` |

`SOURCE_PINS.json` in `lab/astra-science/kalshi_c4_kxcpi_settled_join_lab_20260924/`
at sha256 `21df2532fd0c016ca17bd4b12e8e0eab06c18e05a2f2955e3fbe6004333c80ca`
is the pre-harness lab declaration from that first commit. A later commit
replaces every mirror with one canonical pin list. `digest_all_match_claimed`
is true only when a script shows every listed hash equals the in-repo bytes.

The capture panel stub is not rewritten. `panel_version` is
`2026-09-23.c4-kxcpi-v0`. Top-level `admitted_at` is null. Stub status is
`NOT_ADMITTED`. 4 events and 44 markets. 21 markets omit
`occurrence_datetime`. This lab does not run `admit.py` and does not write
`admitted_at`.

## Knob

| Arm | Name | Gate |
|---|---|---|
| J0 | Nonempty result required | `join_gate=nonempty_result_required` on already-settled markets whose official `result` is `yes` or `no` and whose `status` is `finalized` |
| J1 | Occurrence datetime match | `join_gate=occurrence_datetime_match`. When `occurrence_datetime` is present it is the clock and is kept verbatim. When `occurrence_datetime` is null, the row is labeled `join_source=expected_expiration_time_fallback` and the raw `expected_expiration_time` is the fallback clock. That fallback is never written into `occurrence_datetime`. |

Scout nonempty result N=25 is a pin. It is not copied into `settled_join_n`.
The 25 settled markets are KXCPI-26AUG (15) and KXCPI-26JUL (10). On those
25, `occurrence_datetime` is present and differs from
`expected_expiration_time`. Both raw values stay as returned.
`results`, `pnl`, `settled_join_n`, `occurrence_match_n`, `admit_ready_flag`,
and `admitted_at` stay null.

Parent seeds KXCPI-26OCT, KXCPI-26DEC, KXCPI-26SEP, and KXCPI-26NOV are
active. Their `result` is empty. They are not settled and are not counted.
KXCPI-26JUN, KXCPI-26MAY, and KXCPI-26APR are listed without nested markets.
They stay missing. The settled markets list is `429` four times. Those
books are not invented.

Public Kalshi reads in the pinned scout are GET. This harness does not
open a socket and does not place orders. Feebook
`22371178cb2663250b4762f328069571c48cb551` and rails
`6a28e0d6254327ea4e6451c781bec56215ac6cac` are fixed commits and are not
loaded.

## Refuse

Lee-Ready. Live orders. Logan keys. Cap-SR. Any FQ feature, including
CPI-FQ. Sibling RJ reopen, including C1-RJ. Arm B. Ungating S1, S2, or
R2-P4. Inventing a settled result, depth, fills, books, PnL, or
`occurrence_datetime`. Running `admit.py`. Copying scout N=25 into
`settled_join_n`.

Examiner status stays `HOLD_PRE_PR`. `stub_ready` stays false. The
authentic examiner hold file is not rewritten.
