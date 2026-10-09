"""Receipt and results assembly. Library callers pass rows that are already loaded."""

import platform
import sys

from .canonical import canonical_sha256
from .constants import (
    ACCEPT_SHA256,
    ADVERSARY_PASS_SHA256,
    AGGREGATION,
    BUILDER_RELATIVE_PATH,
    FEE_ADMISSION,
    FEE_BLOCK_REASON,
    FREEZE_JSON_SHA256,
    FREEZE_MD_SHA256,
    PERCENTILE_METHOD,
    POST_GROUP_EXPECTED_NO,
    POST_GROUP_EXPECTED_YES,
    RECEIPT_SCHEMA,
    REPORTING_DEFECT,
    SAMPLER_STRING,
    SWEEP_KEY,
    SWEEP_ORDER,
    SWEEPS_SCHEMA,
    TAGS,
    THRESHOLD_HEADLINE,
    THRESHOLD_S5K,
)
from .fees import admission
from .gates import builder_receipt, count_gate, structure_gate
from .metrics import cell_block, impact_profile, leave_one_out, primary_side
from .placebo import run_placebo
from .refusals import assert_no_result_fields, assert_not_holdout
from .sweeps import build as build_sweeps
from .sweeps import per_side_per_event_counts
from .verdict import evaluate

from . import quotes as quote_mod


def _events(week_membership):
    return sorted(week_membership)


def _screen_identity(rows):
    """Holdout and result-field screen. Quote as-of values stay inside the structure gate."""
    for row in rows:
        assert_no_result_fields(row, allow_b2_fields=False)
        assert_not_holdout(ticker=row.get("ticker"), event=row.get("event"))


def _public(mapping):
    return {key: value for key, value in mapping.items() if not str(key).startswith("_")}


def _unbuilt_sweeps_document():
    """KD-1 shell with no sweeps. Used only when the structure gate rejected a timestamp."""
    return {
        "schema": SWEEPS_SCHEMA,
        "threshold_headline": THRESHOLD_HEADLINE,
        "threshold_s5k": THRESHOLD_S5K,
        "key": list(SWEEP_KEY),
        "order": list(SWEEP_ORDER),
        "sweeps": [],
    }


def structure_timestamp_malformed(receipt_or_gate):
    gate = receipt_or_gate.get("structure_gate", receipt_or_gate)
    return gate.get("reason") == "STRUCTURE_TIMESTAMP_MALFORMED"


def build_receipt(
    rows,
    markets,
    week_membership,
    pins,
    *,
    builder_sha256,
    source_pins,
    sweeps_module_sha256,
    python_version=None,
    platform_name=None,
):
    """Label-free receipt. Caller has already hashed the builder, before quote prices are used."""
    _screen_identity(rows)
    counted = count_gate(rows, markets, week_membership, pins)
    builder = builder_receipt(builder_sha256, pins.builder_expected_sha256, BUILDER_RELATIVE_PATH)
    structure = structure_gate(rows)
    if structure_timestamp_malformed(structure):
        document = _unbuilt_sweeps_document()
    else:
        document = build_sweeps(rows, markets)
    events = _events(week_membership)
    sweeps = document["sweeps"]
    no_count = sum(1 for sweep in sweeps if sweep["d"] == -1)
    yes_count = sum(1 for sweep in sweeps if sweep["d"] == 1)
    receipt = {
        "schema": RECEIPT_SCHEMA,
        "source_pins": source_pins,
        "b1_quote_builder": builder,
        "count_gate": counted,
        "structure_gate": structure,
        "sweeps_sha256": canonical_sha256(document),
        "sweeps_builder_sha256": sweeps_module_sha256,
        "per_side_per_event_counts": per_side_per_event_counts(sweeps, events),
        "per_print_counts": counted["observed"]["per_print_counts"],
        "post_grouping_crosscheck": {
            "NO": no_count,
            "YES": yes_count,
            "expected": {"NO": POST_GROUP_EXPECTED_NO, "YES": POST_GROUP_EXPECTED_YES},
            "gate": False,
        },
        "freeze": {
            "md_sha256": FREEZE_MD_SHA256,
            "json_sha256": FREEZE_JSON_SHA256,
            "accept_sha256": ACCEPT_SHA256,
        },
        "python_version": sys.version if python_version is None else python_version,
        "platform": platform.platform() if platform_name is None else platform_name,
        "reporting_defects": [dict(REPORTING_DEFECT)],
    }
    receipt["reporting_defects"][0]["items"] = list(REPORTING_DEFECT["items"])
    return receipt, document


def _provenance(git_commit):
    if git_commit is None:
        from .pins_io import read_git_commit

        git_commit = read_git_commit()
    return {
        "python_version": sys.version,
        "platform": platform.platform(),
        "git_commit": git_commit,
        "freeze_md_sha256": FREEZE_MD_SHA256,
        "freeze_json_sha256": FREEZE_JSON_SHA256,
        "accept_sha256": ACCEPT_SHA256,
        "adversary_pass_sha256": ADVERSARY_PASS_SHA256,
        "tags": list(TAGS),
    }


def _flags():
    return {
        "counts_toward_keep": False,
        "promote": False,
        "live_promotion": False,
        "feeds_gate": False,
        "pnl": None,
        "roi": None,
        "keep": None,
        "results": None,
    }


def _base_results(receipt, git_commit):
    body = {
        "provenance": _provenance(git_commit),
        "receipt_sha256": canonical_sha256(receipt),
        "sweeps_sha256": receipt["sweeps_sha256"],
        "fee_admission": FEE_ADMISSION,
        "fee_block_reason": FEE_BLOCK_REASON,
        "fee": admission(),
        "reporting_defects": receipt["reporting_defects"],
    }
    body.update(_flags())
    return body


def _verdict_only(receipt):
    count_pass = bool(receipt["count_gate"]["pass"])
    structure_pass = bool(receipt["structure_gate"]["pass"] and receipt["b1_quote_builder"]["match"])
    table = evaluate(
        {},
        {},
        count_pass=count_pass,
        structure_pass=structure_pass,
    )
    if table["rule"] == "V1s":
        builder = receipt["b1_quote_builder"]
        structure = receipt["structure_gate"]
        if not builder.get("match"):
            table["reason"] = builder.get("reason") or "C2_BUILDER_SHA_MISMATCH"
        elif structure.get("reason"):
            table["reason"] = structure["reason"]
    return count_pass and structure_pass, table


def body_if_sweeps_sha_differs(receipt, filed_sweeps_sha256, git_commit=None):
    """None when the filed sha matches. Otherwise a V1 body and no statistics."""
    if receipt.get("sweeps_sha256") == filed_sweeps_sha256:
        return None
    return results_for_sweeps_mismatch(receipt, git_commit)


def results_for_sweeps_mismatch(receipt, git_commit=None):
    """Filed SWEEPS sha disagrees with the rebuild. V1, no statistics."""
    body = _base_results(receipt, git_commit)
    body["verdict_table_evaluation"] = {
        "verdict": "INCONCLUSIVE",
        "rule": "V1",
        "owner": "Examiner",
        "status": "RUNNER_EVALUATION_NOT_A_SCORE",
        "reason": "SWEEPS_SHA_MISMATCH",
    }
    body["output_sha256"] = canonical_sha256(
        {key: value for key, value in body.items() if key != "output_sha256"}
    )
    return body


def build_results(
    rows,
    markets,
    week_membership,
    pins,
    *,
    builder_sha256,
    source_pins,
    sweeps_module_sha256,
    b2_rows=None,
    git_commit=None,
):
    """Score loaded rows. A failed gate returns V1 or V1s and does not call the mid module."""
    receipt, document = build_receipt(
        rows,
        markets,
        week_membership,
        pins,
        builder_sha256=builder_sha256,
        source_pins=source_pins,
        sweeps_module_sha256=sweeps_module_sha256,
    )
    gates_ok, early = _verdict_only(receipt)
    if not gates_ok:
        body = _base_results(receipt, git_commit)
        body["verdict_table_evaluation"] = early
        body["output_sha256"] = canonical_sha256(
            {key: value for key, value in body.items() if key != "output_sha256"}
        )
        return receipt, document, body

    records = quote_mod.classify_sweeps(document["sweeps"], rows)
    from .bootstrap import make_idx
    from .canonical import canonical_sha256 as sha256

    events = _events(week_membership)
    idx = make_idx(len(events))
    yes = primary_side(events, records, 1, idx)
    no = primary_side(events, records, -1, idx)
    table = evaluate(
        yes,
        no,
        count_pass=True,
        structure_pass=True,
    )
    if b2_rows is None:
        b2_rows = []
    from .b2join import join as join_b2

    body = _base_results(receipt, git_commit)
    body["IDX_sha256"] = sha256(idx)
    body["bootstrap"] = {
        "sampler": SAMPLER_STRING,
        "percentile_method": PERCENTILE_METHOD,
        "aggregation": AGGREGATION,
    }
    body["primary"] = {"YES": _public(yes), "NO": _public(no)}
    body["cells"] = {
        "YES": cell_block(events, records, 1, idx),
        "NO": cell_block(events, records, -1, idx),
    }
    body["impact_profile"] = impact_profile(records)
    body["loo"] = leave_one_out(events, records, document["sweeps"])
    body["placebo"] = run_placebo(events, records)
    body["b2_join"] = join_b2(document["sweeps"], b2_rows)
    body["verdict_table_evaluation"] = table
    body["per_sweep"] = records
    # per_sweep is a test aid. The frozen results object in §4.3 does not list it.
    # Keep it out of the hashed score output by publishing a separate view below.
    published = {key: value for key, value in body.items() if key != "per_sweep"}
    published["output_sha256"] = canonical_sha256(published)
    body["output_sha256"] = published["output_sha256"]
    body["_published"] = published
    return receipt, document, body


def published_results(body):
    """Results object without private fields. This is what RESULTS.json stores."""
    if "_published" in body:
        return body["_published"]
    return {key: value for key, value in body.items() if key != "per_sweep" and not str(key).startswith("_")}
