# Strategy 1: neglected-market hybrid forecasting

**Promising historical House signal; insufficient evidence for deployment.
Senate replication fails.** Read [RESULTS.md](RESULTS.md).

The fixed 50/50 external-model/market hybrid improved Brier loss by 12.4% on 19
admitted 2024 House races. Its two hypothetical unit purchases earned $0.88556
after illustrative fees and a 2c buffer. The preselected second horizon improved
Brier by 9.6% on 23 races, with three signals and $1.519439 hypothetical net.
These horizons overlap: do not add their returns or race counts.

The primary sample misses the frozen 20-race breadth minimum. Two trades explain
all its profit. Historical fees, depth, fills and sustainable capacity remain
unverified. This is a quoted-price cost screen, not actual trading P&L.

## Reproduce offline

Python 3.12+, standard library. From this directory:

```bash
python3 -m unittest -v test_core test_normalize test_books
python3 verify.py
python3 run_study.py data/analysis_input.json /tmp/nh-replay
```

27 tests pass. Verification reproduces three result files byte-for-byte from the
included derived dataset, verifies eight frozen source hashes, and independently
checks 29 arm/horizon trade records with decimal arithmetic. Those records are
overlapping comparisons, not 29 independent opportunities.

## Contents

- `SPEC.md`, `AMENDMENT_A.md`, `IMPLEMENTATION_FREEZE*.json`: design, disclosed archive amendment, pre-score hashes.
- `core.py`, `normalize.py`, `run_study.py`: causal joins, comparisons and cost accounting.
- `data/analysis_input.json`: 42 mapped races, 66 relevant forecasts, 252 quote observations.
- `data/PROVENANCE.json`, `data/source_receipts.json`: attribution and raw-source hash indexes.
- `results/`: scores, trade records, exclusions, negative findings and diagnostics.
- `execution_audit.py`: later-minute quote diagnostic; six successful requests returned empty candles.
- `capture_books.py`: bounded current-depth recorder, exercised on three current contracts.
- `NEXT_EXPERIMENT.md`: remaining admissions and integration requirements.

## Raw reacquisition

```bash
# First GET the current Elections series catalog into raw/series.json:
# https://api.elections.kalshi.com/trade-api/v2/series?category=Elections
python3 acquire_v2.py raw raw/series.json
python3 forecast_archive.py raw/forecasts
python3 normalize.py raw raw/forecasts evidence/dataset.json
```

Current discovery may change. `data/panel.json` preserves the actual 155 series
searched. Raw upstream bytes are excluded from Git; their hashes are not copies.
The included compact derived input reproduces scores without network access.
No upstream redistribution license is inferred. No orders or recurring processes
were started.
