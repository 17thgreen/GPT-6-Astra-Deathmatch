# EXT-K2 lab

Part (a) measures the dev-tape open-leg markout of recorded 000 fills by taker-YES tercile. Part (b) is the box-only Becker runner and its synthetic tests.

From this directory:

```bash
python3 -m unittest discover -s tests -v
python3 -m dev_pipeline.orchestrator
```

The orchestrator writes `results_a/`. It does not write a per-fill dump.

`python3 -m becker_pipeline.run_part_b` refuses in this checkout: the Becker directory is not on disk. The Simulator runs that module on the box after the receipt shas match. Box outputs stay outside the git repo. This tree commits a receipt template and a null output-sha placeholder only.

Pins are under `pins/` and are checked against `MANIFEST.sha256` before parse. `*.jsonl.gz` inputs are force-added and must stay byte-identical to the bundles.
