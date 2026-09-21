# NFL maker research audit

Read `NFL_Maker_Audit_and_Strategy_Ranking.md` first. This is an artifact audit and research prototype, not an execution bot or a corrected profitability backtest.

The review is pinned to `17thgreen/Claude-SportsBetting-Competition-to-the-Death` commit `f4ad8e8bfba2db2a5e8e1ecf80f935424f60f175`. The private repository's files are not bundled. Already computed results and newly written audit code are included.

## Reproduce

Use Python 3.12 and the dependencies in `requirements.txt`, preferably in a virtual environment. From this folder:

```bash
python -m pip install -r requirements.txt
python fetch_sources.py --repo-root /absolute/path/to/your/clone
python audit_maker.py
python reproduce_defects.py
python -m unittest discover -s . -p test_review.py -v
```

The clone must already contain the pinned commit; the script never switches branches or fetches into the clone. Alternatively, run `python fetch_sources.py` with an already authenticated GitHub CLI that can read the private repository. It downloads eight required inputs and verifies each hash. No credentials are embedded or requested by these scripts. `python fetch_sources.py --verify-only` performs offline verification after restoration.

`SOURCE_MANIFEST.json` also lists the other reviewed source files and their hashes for provenance. Only eight files are needed for these reproductions. Schedule keys for all 315 games are included; two UTC-date ticker aliases are explicitly documented in the keys file. Schedule provenance is in `inputs/schedule_source.json`.

## Scope of the results

- `results/artifact_audit.json`: recomputation of the saved simulated P&Ls, not a new replay. The complete-window filter changes the cohort, not the policy that generated the fills. The source policy still quotes to T−1 minute.
- `results/*_audited_games.csv`: derived rows with corrected league season/week and window-completion labels.
- `results/defect_reproductions.json`: synthetic evidence of four source defects. It does not estimate their historical monetary impact.
- `results/tests.txt`: eight tests passed. The replay reproducer loads unchanged function bodies through Python AST solely to avoid unrelated database imports.
- `quote_guards.py`: window/book admission, joint outstanding-order reservations, size reduction and illustrative pairing economics. Call admission on a timer and before simulated matching. A cancel instruction is not an acknowledgment; retain outstanding obligations until acknowledgment.

The guard functions do not implement an exchange adapter, fitting, queue inference, fee rounding, price/quantity grids, collateral netting or general multi-outcome risk. Verify payoff equivalence before assigning signed exposure, including tie/cancellation rules. Round allowed quantities down to permitted increments and calculate dated fees separately. Pending orders on unrelated games must already have their cash reserved before calling the single-game allocation primitive.

No test in this kit establishes profitability. Full corrected trade/book replay and a frozen prospective paper evaluation remain necessary. Do not sum independent per-game accounts or window simulations into a shared-bankroll return.
