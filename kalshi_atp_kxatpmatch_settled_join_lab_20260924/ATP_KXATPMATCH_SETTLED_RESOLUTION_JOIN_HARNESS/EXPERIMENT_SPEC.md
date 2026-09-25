# ATP KXATPMATCH settled-resolution join

September 24, 2026. This file is the hypothesis. It is committed before a
unit-test outcome is recorded. No figure in this document is a trading
result. This is measurement-only settled-resolution join. Feature family
ATP-RJ. One knob: `join_gate`.

Nearest dead card: ATP-FQ, PR34 at `438f4abf28a3c0156daf6c96ece5efda9557f1dc`.
PR35 was a closed duplicate. ATP-FQ varied `analysis_slice` on the active
KXATPMATCH ladder and read fee and queue quantities. ATP-RJ varies only
`join_gate` on already-settled KXATPMATCH markets. It reads and produces no
fee, queue, book, fill, or tape metric. ATP-FQ stays closed.

## Pins

The implement bundle was committed byte-for-byte before this hypothesis.
Conductor ACCEPT sha256
`e42d75834086f34090581aee88563ab9849d60864c2d9e59c4ef495b3e8e5af5`
has decision `ACCEPT + IMPLEMENT GO`, issued_at_et `2026-09-24T19:52-04:00`
(`2026-09-24T23:52:00Z`). The ACCEPT names main at
`959c3f2beaec5f999b4852c428a3c4cdae1e9603`. This branch is cut from main
after that commit, at `37ad5b7b366c10dcdf278c2325611e6f426a62c6`.

| Pin | Path | sha256 |
|---|---|---|
| Freeze | `lab/governance/astra/packets/ATP_KXATPMATCH_SETTLED_RESOLUTION_JOIN_HARNESS_FREEZE_2026-09-24.md` | `dc9fcb326a97ce24267ed96438bf403687bc9aef6b79dccef3483d0e4cdeeb69` |
| Conductor ACCEPT | `lab/governance/astra/packets/CONDUCTOR_ACCEPT_ATP_KXATPMATCH_SETTLED_RESOLUTION_JOIN_HARNESS_2026-09-24.json` | `e42d75834086f34090581aee88563ab9849d60864c2d9e59c4ef495b3e8e5af5` |
| Maximize pin | `lab/governance/astra/packets/MAXIMIZE_PIN_2026-09-24_1948ET.md` | `70020baf5599f7afcd4c8335d5f084c34784c5b4b1b44ffabce1041e41cbc84a` |
| Examiner HOLD | `lab/governance/astra/packets/EXAMINER_HOLD_ATP_KXATPMATCH_SETTLED_JOIN_HARNESS_PRE_PR_2026-09-24.json` | `214fb8c1b54d1dfd14cdcff39c4a35e227eafe7e35ba96ff2e6e636b04f2ba76` |
| Suggested ping | `lab/governance/astra/packets/SUGGESTED_CONDUCTOR_ACCEPT_PING_ATP_RJ_2026-09-24.json` | `a666102da44910288756896aaa30b3d2bfde4fff867fca9fff0cd1b75420c28b` |
| Scout reget | `lab/governance/astra/packets/scout_atp_settled_rejoin_2026-09-24/scout_settled_rejoin_ATP_KXATPMATCH.json` | `2982a245ebd4ff8430ef4b2fe13692c15211c2077e2460d6c0246480f59736df` |
| Seed summary | `lab/governance/astra/packets/scout_atp_settled_rejoin_2026-09-24/SEED_SETTLED_SUMMARY.json` | `913fc5d646c51192e40869a68a64b4fe2b66f8231dd75b90f5467bd50559700e` |
| Panel stub | `lab/astra-capture/atp-kxatpmatch/panel_stub.json` | `ed041c502d1f775d33c44bf900ac91b1339d99045bddd2052edd09a139ae2d3f` |
| Settled reget | `lab/governance/astra/packets/scout_atp_settled_rejoin_2026-09-24/settled_reget_2026-09-24.json` | `068ff00fe420d3365cc798549ef2e89aac96fa7e841846f73e67d5103c49760a` |
| Scorecard template v1.2 | `lab/governance/astra/templates/EXAMINER_KALSHI_SCORECARD_TEMPLATE_v1.2.json` | `56bcf6269a42031d9d90496e9a65c2292321aed2165033f6fb44ff8cc4d6b1cc` |

`SOURCE_PINS.json` in `lab/astra-science/kalshi_atp_kxatpmatch_settled_join_lab_20260924/`
at sha256 `4de33473fd9bab9133ab30e55c7cfc409ee9c92b26d92a1b7ac237a587319a60`
is the pre-harness lab declaration from that first commit. A later commit
replaces every mirror with one canonical pin list. `digest_all_match_claimed`
is true only when a script shows every listed hash equals the in-repo bytes.

The capture panel stub is not rewritten. `panel_version` is
`2026-09-23.atp-kxatpmatch-v0`. Top-level `admitted_at` is null. Stub status
is `NOT_ADMITTED`. 6 events and 12 markets. 0 markets omit
`occurrence_datetime`. This lab does not run `admit.py` and does not write
`admitted_at`.

## Knob

| Arm | Name | Gate |
|---|---|---|
| J0 | Nonempty result required | `join_gate=nonempty_result_required` on already-settled markets whose official `result` is `yes` or `no` and whose `status` is `finalized` |
| J1 | Occurrence datetime match | `join_gate=occurrence_datetime_match`. When `occurrence_datetime` is present it is the clock and is kept verbatim. When `occurrence_datetime` is null, the row is labeled `join_source=expected_expiration_time_fallback` and the raw `expected_expiration_time` is the fallback clock. That fallback is never written into `occurrence_datetime`. |

Scout nonempty result N=30 is a pin. It is not copied into `settled_join_n`.
The 30 settled markets are 15 events (ATP Chengdu 7, ATP Hangzhou 8), yes 15
and no 15. On those 30, `occurrence_datetime` is present and equals
`expected_expiration_time`. Both raw values stay as returned. The fallback
path is not exercised by that cohort. `settlement_ts` is earlier than
`occurrence_datetime` on 8 of the 30. Both timestamps stay as returned.
`results`, `pnl`, `settled_join_n`, `occurrence_match_n`, `fallback_join_n`,
`admit_ready_flag`, and `admitted_at` stay null in the committed scorecard.

Parent seeds stay on the unadmitted stub: status `active`, `result` empty.
KXATPMATCH-26SEP22HARGAL and KXATPMATCH-26SEP22MOCKOT are finalized on the
single-event GET and are outside events-list page 1. They are not added to
N. The settled markets list is `429` four times. Events page 2 is not
fetched. Those gaps are not invented.

## Measurement mode

Conductor condition: a runnable measurement mode computes `settled_join_n`,
`occurrence_match_n`, and `fallback_join_n` on KXATPMATCH markets whose
`settlement_ts` is strictly after the ACCEPT timestamp
`2026-09-24T23:52:00Z`. The 30 scout markets and anything settled at or
before that timestamp are excluded. That cohort is the untouched evaluation
set. The command is:

```bash
python3 orchestrator.py measure --since 2026-09-24T23:52:00Z --out <path>
```

It uses public GET reads on `https://api.elections.kalshi.com/trade-api/v2`,
the host in the pinned scout `http_log.jsonl`. Every attempt is logged with
a real UTC timestamp. A 429 uses bounded backoff (10s, 20s, 40s) and the
gap stays empty. Raw response bodies are written beside the output. The
output JSON carries the counts, cohort tickers, the since timestamp,
`admitted_at` null, and admit_ready `pending Clock`. `results` and `pnl`
stay null. This hypothesis does not record a live measured count. The
committed scorecard stays null until a later run after Clock admit, which
Examiner scores. `admit.py` is refused.

Public Kalshi reads in the pinned scout are GET. Feebook
`22371178cb2663250b4762f328069571c48cb551` and rails
`6a28e0d6254327ea4e6451c781bec56215ac6cac` are fixed commits and are not
loaded.

## Scorecard

`EMPTY_RESULTS.json` carries the Examiner scorecard v1.2 field schema.
Score values stay null. Calibration stays null with
`emits_probabilities` false. Examiner status stays `HOLD_PRE_PR`.
`stub_ready` stays false. The authentic examiner hold file is not rewritten.

## Refuse

Lee-Ready. Live orders. Logan keys. Cap-SR. Any FQ feature, including
ATP-FQ. Sibling RJ reopen, including C4-RJ. Arm B. Ungating S1, S2, or
R2-P4. Inventing a settled result, depth, fills, books, PnL, or
`occurrence_datetime`. Writing `expected_expiration_time` into
`occurrence_datetime`. Running `admit.py`. Copying scout N=30 into
`settled_join_n`. Backfilling the markets-list 429 or events page 2.
