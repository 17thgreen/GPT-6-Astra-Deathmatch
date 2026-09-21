# NFL queue measurement lab Q3

Read `NFL_Measurement_Results.md` for findings. Q1/Q2 strategies are unchanged.
This is a measurement package, with no order entry and no live-profit claim.
Python 3.12 standard library; no account key is needed for the included captures.

Offline reproduction:

```bash
python3 -m unittest -v test_measurement
python3 historical.py
python3 measure.py
python3 contextualize.py
python3 evaluation_gate.py
python3 verify.py
python3 build_report.py
```

`inputs/` includes Q1's earlier public forward sample, the precise historical
quotes and two hypothetical fill ledgers used for this round, and provenance.
The historical inputs come from the prior 31-game Q2 kit; its original raw
captures remain in that separately delivered kit. The present package does not
need that kit to reproduce its diagnostics. To re-extract from it, use
`python3 historical.py --extract-from /absolute/path/to/Q2`.

`forward/` contains this round's finite development capture, including failures,
request and receipt times, all fetched trade pages, and coverage intervals.
`capture.py` runs a bounded session and refuses to overwrite an existing capture.
To collect again, make a separate working copy, preserve the delivered capture,
use an empty `forward/` directory, and declare its new manifest and purpose.
Do not repeatedly relabel development observations as holdout data.

Future evaluation is **pending**. HOLDOUT_MANIFEST.json reserves 32 schedule
identities. Most Kalshi event identities still need verification. No persistent
collector, external host, scheduled job, model deployment or order placement
has been configured. This workspace's bounded run does not cover future windows.
An operating recorder needs a durable host and continuous storage across those
windows before any full-window evidence can exist.

Before opening holdout data, freeze the candidate, baseline, execution settings
and evaluator. The earliest reserved window starts September 22, 2026 at 00:15
UTC, based on the frozen schedule. If the candidate is not frozen before then,
this registry is ineligible; declare another future cohort before its data are
examined. Never shift the dates or silently drop a game to manufacture a pass.

`evaluation_gate.py` checks the structural prerequisites in optional
`results/holdout_evidence.json`. It returns INSUFFICIENT for the current empty
evidence. It is a fail-closed checklist, not a replacement for independent data
and financial-ledger verification, and cannot by itself promote a strategy.

Useful extensions require more data: quote persistence conditional on depth and
flow; actual own-order queue measurements when authenticated access exists;
and adverse movement at execution-relevant resolution. Public REST cannot
identify which canceled orders were ahead of a hypothetical join. Neither
displayed depth declines nor midprice markouts establish realized profit.
