# Q8 restoration and reproducibility

Code, frozen specification, tests, scenario summaries and audits are committed on
`research/q8-joint-routing`. Q8 imports Q7 and Q6 source without modifying them.

1. Check out this branch with the inherited directories intact.
2. Restore Q7's data archive as described in its DELIVERY_NOTES.md. Q8 references
   those same input bytes and does not duplicate them in its own archive.
3. Verify both Q8 archive parts against DATA_ARCHIVE.json. Extract both
   at the repository root. EXTERNAL_ARTIFACTS.json lists all 48 files and hashes.
4. From `nfl_joint_route_lab_20260921`, run `python verify_results.py` and
   `python q8_analysis.py`. The existing frozen result should reconcile and retain
   Q7. The verifier requires all indexed ledger bytes, not only summary JSON.
5. Unit tests need no data archive:
   `python -m unittest -q test_joint_policy test_q8_analysis test_pair_policy test_q7_analysis test_replay_v2 test_queue_policies test_completion test_timing test_adaptive test_factorial test_analysis`.
   From repo root, portability tests use
   `python -m unittest discover -s market_portability -p 'test_*.py'`.

Do not run the matrix over existing result files casually; preserve outputs in a
separate checkout before a declared reproduction. No new parameter search is
licensed by this failed hypothesis. `inspect_series.py` makes GET-only public
requests; rerunning it replaces the discovery snapshot with current metadata.
No recorder, background job or live trading service is installed.
