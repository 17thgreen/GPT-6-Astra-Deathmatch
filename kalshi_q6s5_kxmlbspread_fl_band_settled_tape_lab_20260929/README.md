# Q6S5 KXMLBSPREAD FL-band settled-tape

Measurement lab for freeze `Q6S5-KXMLBSPREAD-FL-BAND-SETTLED-TAPE`.
One knob: `price_band`. Arms `Q6S5FL0`, `Q6S5FL1`, and `Q6S5FL2` use the
R3-P3 10¢ registry without rebinning.

The observations are public prints labeled `public_counterparty_realized`.
Fee label `CACHE_NOT_R1P1`. `counts_toward_keep` is false. `results` and
`pnl` stay null.

Vendored pins live under `pins/`. The authentic bundle sha256 is
`63b5d981bc06f684eebb69a8ac29394534f8ae52c101f3018557544f14e29857`.
Conductor ACCEPT sha256 is
`8e4fbac7d0426bc67c1f53fb8057a382fe46da738bd701cb970a9812a6dc2a3b`.
Freeze sha256 is
`fb6540f52ed5f819ccf6e80bf0cf7eb6d951e065416b9d550fead0c6d06043fa`.
`digest_all_match_claimed` is true for those vendored bytes. Variants
ping files cited by ACCEPT and not present in the bundle were not invented.
`lab/governance/astra/packets/Q6S5_KXMLBSPREAD_FL_BAND_SETTLED_TAPE` was
not created.

Examiner status is `HOLD_PRE_PR`. The post-PR path is `READY_NOT_SCORED`.
This lab does not mark SCORED.

```bash
python3 -m unittest discover -s tests -v
```

From the bundle root:

```bash
sha256sum -c MANIFEST.sha256
```
