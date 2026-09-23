# S5 KXMVECROSSCATEGORY settled-resolution join harness

Status: hypothesis committed, then source frozen. The unit page is
`results/UNIT_RESULTS.md`. `python3 -m unittest -v tests.test_orchestrator`
ran 10 tests in 0.240s. Recorded at 2026-09-23T21:46:24Z. Result: OK.
Failures: 0. Errors: 0. That page is not profit and not an Examiner pass.
`EXPERIMENT_SPEC.md` is the hypothesis.
`FROZEN_EXPERIMENT.json` keeps `results` and `pnl` null.
`results/EMPTY_RESULTS.json` keeps `results`, `pnl`, `settled_join_n`,
`occurrence_match_n`, and `admit_ready_flag` null.

This lab is measurement-only. Feature family S5-RJ. The only knob is
`join_gate`: J0 `nonempty_result_required` and J1
`occurrence_datetime_match`. When `occurrence_datetime` is null, J1 uses
`expected_expiration_time` and does not invent `occurrence_datetime`.
The scout pin says settled nonempty `result` N=20. That pin is not
`settled_join_n`. The settled list on the attached reget is HTTP 200
with limit 20 and a cursor present. Markets past that cursor are not
invented. Earlier settled, finalized, and events list attempts stay the
honest 429 gaps. `KXMVECROSSCATEGORY-SHARD1` stays the honest 429 gap.
Parent panel seeds are finalized nonempty on ticker GETs in the scout.
The panel stub is not rewritten. `admitted_at` stays null. This lab does
not run `admit.py`. This is orthogonal to S5 FILLLEGS and MVE-FL. It is
not a reopen of Cap-SR, C3-RJ, C5-RJ, R3P3-RJ, NHL-RJ, S4-RJ, or R2P3-RJ.

Attached bytes are also at
`lab/governance/astra/packets/`,
`lab/astra-capture/s5-kxmvecrosscategory/settled_reget_2026-09-23.json`,
`lab/astra-science/kalshi_s5_kxmvecrosscategory_settled_join_lab_20260923/`,
and `packets/S5_KXMVECROSSCATEGORY_SETTLED_JOIN_HARNESS/`.
The capture `panel_stub.json` is the existing file and is not rewritten.

- Freeze sha256 `cd264a4d41ef055d1cbca80a5dbe6756746211537fb24799dca9dde8980cb799`
- Scout reget sha256 `33db60a50f2e7746315f4603b9f78a9260145cb49d0250e141471de46f4df9e3`
- Seed summary sha256 `3bc4aa5f44d7d31295dfd25f7bac3a3e39463c237315e8228c3fcf434d08419a`
- Panel stub sha256 `4918b820d454c5f997ea100917859f7e9467d92933bed1bc8a55c81ab8ce5b8e` (`2026-09-22.s5-kxmvecrosscategory-v0`, `admitted_at` null)
- Settled reget sha256 `91111f20586a1b684e430baa0e8b62a3fffc7d510de99e43bab7d213dfeb26da`
- Accept sha256 `495675175589c08122bc57375dd8e7d00aea9f4a154df3aff086b015a2513a8c`

Feebook and rails commits are fixed path pins and are not imported.
No fee arm. No live orders. No Logan keys.

From this directory, Python 3 standard library:

```bash
python3 -m unittest -v tests.test_orchestrator
```

No Logan keys. No live orders. A passing unit run is not an Examiner score.
