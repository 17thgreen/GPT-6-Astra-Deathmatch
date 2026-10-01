# Q6S5 KXMLBSPREAD game-phase settled-tape

Measurement lab for freeze `Q6S5-KXMLBSPREAD-GAME-PHASE-SETTLED-TAPE`.
One knob: `game_phase`. Arms `Q6S5GP0` (pregame) and `Q6S5GP1` (in-play)
use the print timestamp against the pinned scheduled first pitch.
`first_pitch_source` is `SCHEDULED_START_PROXY`.

The observations are public prints labeled `public_counterparty_realized`.
Fee label `CACHE_NOT_R1P1`. `family_size` is 4. `hypothesis_generating_only`
is true. `universe_cap_last_knob` is true. `counts_toward_keep` is false.
`results` and `pnl` stay null.

Vendored pins live under `pins/`. The authentic bundle sha256 is
`6576ee6cf9f023137e4357270f228dd9a5d29e3dc1d5e7ced85384681f2a7ecc`.
Conductor ACCEPT sha256 is
`08d23b363d72b8c8599772ee6fc6736cb90f13e8ed814b12c59b58fd5c7dc91e`.
Freeze sha256 is
`5beba803f3f6d33410409acc23ad3b782be62dc8829a0f54584e1da8ac18575a`.
The packet-dir MANIFEST sha256 is
`88af3bd79ad37c6fa09cfbe1bcd516c72b8a35d2928ce04eeaec994b5c1233a1`.
The band registry sha256 is
`0860cbe28d28ecc6142ddf6f1ebb67792084264ed82e0b4d868c3b3138ea5312`.
The inherited IN_SAMPLE_DEV ruling sha256 is
`09763030c67df066f2b59346200813e181777670cd46fcee6b8877a6dd74d754`.
`digest_all_match_claimed` is true for those vendored bytes.
`lab/governance/astra/packets/Q6S5_KXMLBSPREAD_GAME_PHASE_SETTLED_TAPE` was
not created. The variants ping prefix `7af58fa9` was not invented as a file.

Examiner status is `HOLD_PRE_PR`. The post-PR path is `READY_NOT_SCORED`.
This lab does not mark SCORED.

```bash
python3 -m unittest discover -s tests -v
```

From the bundle root:

```bash
sha256sum -c MANIFEST.sha256
```

From `pins/`:

```bash
sha256sum -c MANIFEST.sha256
```
