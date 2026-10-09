# CONDUCTOR ACCEPT — EXT2-K1 sweep-reversion freeze rev2 — 2026-10-08 20:48 ET
Freeze r2: md 8f35fa77cab5872f7956df34c145fda2e8ae5587e1c1396ca2d39b5e347676a9 / json afbcd089888c84fb5db4e611b1e58ef59a558d4b379c843bae68c82a386ed8af — re-hash PASS.
Adversary pre-review: r1 REQUIRED_EDITS 8a1a38049e79b77c95caf74f561b16599f2e4e9a687c4a10aa7d507d251b58a0; r2 PASS 9da36baaf76d60eb221d3ed71605e4951e7ffe9e1e4bb3d01261fe60230d7797.
Supersedes: ACCEPT_CONDITIONAL 7bd04408 (its OQ rulings stand except OQ1, replaced by RE-2).
STATUS: ACCEPT.
C1 — 20:41 ET override, stated verbatim for sha anchoring:
"Shift horizons from the new entry; k* stays 900 s after entry."
Meaning: all horizons {60,300,900,1800,3600} s are measured from the RE-1 entry row (t_s+120, asof > t_s strictly), and the primary k* = 900 s after entry. Set before any output existed.
C2 — B1 quote builder pin (binding at implementation, no rev3):
Expected B1 load_data.py sha256 = 817c74deec49103ff8e1849c23677b207cb698e5cb05559b69978fe25eaa2ca3 (per nfl_completion_lab_20260921/FROZEN_CODE.json). The implementation must record a receipt of the builder sha before reading any mid; mismatch or absence => INCONCLUSIVE(STRUCTURE), no fallback.
Required at implementation also: descriptive 0.05/0.95 entry-mid sensitivity (not a verdict input); five md wording changes missing from the changelog are logged as REPORTING_DEFECT (no verdict effect).
Queue: implement after R1 merge, then PR-C. No GETs; no live orders; verdict cannot reach KEEP or touch Q6-000. Adversary re-reviews before Examiner scores.
