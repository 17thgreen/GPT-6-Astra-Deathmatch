"""Shared fixtures for the freeze tests. The dev tape is loaded once per process."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[0]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

_STATE = {}


def lab_root():
    return ROOT


def repo_root():
    return REPO


def dev_state():
    if "state" in _STATE:
        return _STATE["state"]
    from dev_pipeline.load import load_dev
    from dev_pipeline.lots import reconstruct
    from dev_pipeline.terciles import bucket_document, flow_terciles, index_trades, portion_labels
    from shared.canonical import canon_bytes, canon_sha256

    dev = load_dev()
    built = flow_terciles(dev["flow"])
    document = bucket_document(built)
    lots = reconstruct(dev["fills"], dev["markets"])
    labels = portion_labels(lots["portions"], built, index_trades(dev["flow"]))
    cuts = {"c1": built["c1"], "c2": built["c2"], "e1": built["e1"], "e2": built["e2"]}
    shas = {
        "tercile_cuts": canon_sha256(cuts),
        "bucket_terciles": canon_sha256(document),
        "portion_terciles": canon_sha256(labels),
    }
    shas["constancy"] = canon_sha256({
        "bucket_terciles_sha256": shas["bucket_terciles"],
        "portion_terciles_sha256": shas["portion_terciles"],
        "tercile_cuts_sha256": shas["tercile_cuts"],
    })
    _STATE["state"] = {
        "dev": dev,
        "built": built,
        "document": document,
        "document_bytes": canon_bytes(document),
        "lots": lots,
        "labels": labels,
        "cuts_bytes": canon_bytes(cuts),
        "portion_bytes": canon_bytes(labels),
        "shas": shas,
    }
    return _STATE["state"]
