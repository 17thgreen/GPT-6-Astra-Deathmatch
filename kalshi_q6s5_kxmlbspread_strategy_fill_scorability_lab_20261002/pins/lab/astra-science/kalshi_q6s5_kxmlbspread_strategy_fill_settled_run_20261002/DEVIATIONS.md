# Deviations / notes: PR60 strategy-fill settled run (Simulator, 2026-10-01/02 America/New_York)

1. HEAD check: /workspace/repo_f233079/.git has no refs/ directory. It is a detached checkout with no refs; the empty dir appears to have been dropped when the box filesystem was restored, since most box files carry mtimes around 2026-10-01T23:12-23:13-04:00. Because of this, git does not recognize the checkout. I made a read-only copy (`cp -a`) at /tmp/gitcheck_f233079.git and added empty refs/heads and refs/tags. Run with GIT_WORK_TREE=/workspace/repo_f233079, it gives HEAD = f233079d9e7d2a91e2100f2085bcf85d0006e28f and a clean worktree. The checkout itself was not modified, and no network was used.
2. provenance/runner_sha256_BEFORE_RUN.txt left the two merged-PR60 comparison fields blank because of a shell env quoting error (GIT_DIR was set to empty). I did not rewrite it. provenance/runner_sha256_BEFORE_RUN_ADDENDUM_merged_pr60.txt was written before the run. It shows merged PR60 at 12e760f5 has orchestrator blob 2f4ca4e3 and sha256 296cfe64, which equals the lab copy and the PR61 pr60_check copy. The lab tree id is 78fca23c at 12e760f5, d7558fc4 and f233079d.
3. PARENT = <lab>/runner_tree, the standard workaround. The live /workspace/lab/astra-capture/q6s5-kxmlbspread/ contains panel_admitted.json, and load_panel() refuses when that file exists. runner_tree contains a git-archived panel_stub.json (c7f1f1f4) and parent freeze (4f65dcdf) taken from f233079d.
4. Settlement consumption: SITUATION B (no sanctioned path).
   - The PR60 runner has no settlement argument, config, loader or join.
   - classify_fill raises LookaheadRefused on settlement_ts.
   - Rows carrying only settlement_value_dollars give INCOMPLETE_NOT_INVENTED; the field is ignored.
   - The sibling parent feequeue module's settled_join(panel) returns None by design.
   - The runner has no tape loader at all. Its designed entry points are instrument_binding, digest_status, conduct(arm) and published_scorecard; classify_fill only takes caller-built quote/trade rows.
   - I constructed no quote/trade rows, since doing so would invent strategy quotes.
   - Outcomes are in the SEPARATE outputs/SETTLEMENT_JOIN_MANIFEST_SEP25.json.
5. Panel-level runner outputs (events_n 6, markets_n 12, panel_tickers) necessarily reflect the 12-market panel stub, which includes 6 Sep-24 markets. The runner computes no per-market metric. Everything the Simulator added (the settlement manifest, the scope list) is Sep-25 only. digest_verification hashes the Sep-24 raw tape pins listed in SOURCE_PINS for integrity only, flagged out of scope. No Sep-24 lab or packet was touched.
6. The run driver read one settlement raw file (TBPHI-TB2) to feed two refusal probes. That is the only file open outside runner_tree during the run.
7. Vendored MANIFEST.sha256 and MANIFEST_V2.sha256 were checked with --ignore-missing. A strict sha256sum -c also passes; nothing is missing.
8. The box clock is UTC. All renders use TZ=America/New_York with explicit offsets.
9. Observation: the raw settlement close_time values (2026-09-26T01:15-02:00Z) are earlier than the scheduled close_time 2026-09-28T22:40Z seen in the Sep-25 pre-game captures. This is consistent with markets closing after the games ended. Every settlement_ts falls before the ADMIT-1 window.
