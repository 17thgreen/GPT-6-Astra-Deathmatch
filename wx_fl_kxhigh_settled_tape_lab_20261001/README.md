# WX-FL KXHIGH settled-tape lab

Measurement scaffolding for freeze `WX-FL-KXHIGH-SETTLED-TAPE` (arms WXFL0, WXFL1, WXFL2). The implement base is main `749bc1464764fda03dcddd1162177ef062b2ece3`.

This lab does not place orders and does not perform HTTP GETs. `results` and `pnl` stay null. ROI, deltas, and PnL are implemented for synthetic rows only. The pinned tape is used for counts.

Conductor ACCEPT `b5bd4f046b3a48cffc5617e5f8680a8b8d9d1688568a6fd723fd3b46a845045a` governs where it differs from the freeze. Primary gap mapping is GM-COV with proven coverage. A gap window is covered only when a later poll's cursor range spans the whole window and that poll completed with no 429, no truncation, and no pagination break. The collector's cursor-minus-1-second design is not treated as proof. Windows that fail that test stay unproven, and trades in them are dropped from all arms. GM-LIT is a sensitivity. GM-LIT-PAD is counts only.

`sqlite3` is imported only in `snapshot_loader.py`. The snapshot is opened with `file:...?mode=ro&immutable=1` after the tarball, MANIFEST, and snapshot sha256 checks. The 94.6 MB database is not committed; `pins/WX_FL_KXHIGH_SETTLED_TAPE_authentic_pins_2026-10-01.tgz` is.

```bash
python3 -m unittest discover -s tests -v
```

Run that from this directory. The log belongs in `results/UNIT_RESULTS.md` and is not an Examiner score.
