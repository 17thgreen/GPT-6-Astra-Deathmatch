# WX-FL KXHIGH settled-tape lab

Measurement scaffolding for freeze `WX-FL-KXHIGH-SETTLED-TAPE` (arms WXFL0, WXFL1, WXFL2). The implement base is main `749bc1464764fda03dcddd1162177ef062b2ece3`.

This lab does not place orders and does not perform HTTP GETs. `results` and `pnl` stay null. ROI, deltas, and PnL are implemented for synthetic rows only. The pinned tape is used for counts.

Conductor ACCEPT `b5bd4f046b3a48cffc5617e5f8680a8b8d9d1688568a6fd723fd3b46a845045a` governs where it differs from the freeze, and addendum `68e1ff7a3f170a90b74a72448809558c3ce7364e32a8b5296a1d10c3b2590153` governs where it differs from that ACCEPT. Primary gap mapping is GM-COV union coverage: a window `[start, end)` is proven when the union of later complete polls' closed intervals `[min_ts, requested_at]` covers it with no hole. Later means first-page `requested_at` is strictly after the window start. Open windows stay unproven. The collector's cursor-minus-1-second design is not treated as proof. GM-COV-SINGLE (one poll spans the window) and GM-LIT are full sensitivities. GM-LIT-PAD is counts only.

LOCDO uses the freeze formula `n = n_eff = |D|`, `need = ceil(2n/3)`, inconclusive if `n_eff < 3`. H1 votes only over D01 and H2 only over D21. The addendum supersedes the ACCEPT's ">= 6 of 8". Under the primary, `date_level_n = 1`, so the verdict cap is ITERATE and `contradicts_H1` does not map to KILL. The without-Sep-25 subset is `n_eff = 0`, inconclusive.

`sqlite3` is imported only in `snapshot_loader.py`. The snapshot is opened with `file:...?mode=ro&immutable=1` after the tarball, MANIFEST, and snapshot sha256 checks. The 94.6 MB database is not committed; `pins/WX_FL_KXHIGH_SETTLED_TAPE_authentic_pins_2026-10-01.tgz` is.

```bash
python3 -m unittest discover -s tests -v
```

Run that from this directory. The log belongs in `results/UNIT_RESULTS.md` and is not an Examiner score.
