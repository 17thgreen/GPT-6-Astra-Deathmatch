"""Sha-checked runtime wrapper for add_dem_name.

The script is not vendored. Tests may pass a runner and an expected script
sha. The command line uses the pinned sha and subprocess.run.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from card01_amc.pinload import sha256_bytes

ADD_DEM_NAME_SHA256 = "19250333e6f5f1acaa80fd82fc7f02c01ed2de2101fb557165a04453a247036e"


def _refused(reason, **extra):
    out = {
        "status": "DEM_NAME_STEP_REFUSED",
        "reason": reason,
        "expected_script_sha256": extra.pop("expected_script_sha256", ADD_DEM_NAME_SHA256),
        "observed_script_sha256": extra.pop("observed_script_sha256", None),
        "original_sha256": extra.pop("original_sha256", None),
        "v1_sha256": extra.pop("v1_sha256", None),
        "check": extra.pop("check", None),
    }
    out.update(extra)
    return out


def _probs_equal(left, right) -> bool:
    if isinstance(left, bool) or isinstance(right, bool):
        return False
    if isinstance(left, (int, float)) and isinstance(right, (int, float)):
        return float(left) == float(right)
    return False


def _public_check(check_line):
    if not isinstance(check_line, dict):
        return None
    return {key: value for key, value in check_line.items() if key != "out"}


def _last_json(stdout):
    lines = [line for line in (stdout or "").splitlines() if line.strip()]
    if not lines:
        return None
    try:
        obj = json.loads(lines[-1])
    except json.JSONDecodeError:
        return None
    return obj if isinstance(obj, dict) else None


def validate_dem_name_doc(original_bytes, v1_bytes, check_line, universe_codes):
    """Pure check of a dem_name_v1 document against the original derived bytes."""
    if not isinstance(check_line, dict):
        return _refused("CHECK_SHA_MISMATCH")
    v1_sha = sha256_bytes(v1_bytes)
    original_sha = sha256_bytes(original_bytes)
    if check_line.get("sha256") != v1_sha:
        return _refused("CHECK_SHA_MISMATCH", original_sha256=original_sha, v1_sha256=v1_sha, check=_public_check(check_line))
    try:
        v1 = json.loads(v1_bytes)
        original = json.loads(original_bytes)
    except json.JSONDecodeError:
        return _refused("VERSION_INVALID", original_sha256=original_sha, v1_sha256=v1_sha, check=_public_check(check_line))
    if not isinstance(v1, dict) or v1.get("version") != "dem_name_v1":
        return _refused("VERSION_INVALID", original_sha256=original_sha, v1_sha256=v1_sha, check=_public_check(check_line))
    base = v1.get("base_derived")
    if not isinstance(base, dict) or base.get("sha256") != original_sha:
        return _refused("BASE_SHA_MISMATCH", original_sha256=original_sha, v1_sha256=v1_sha, check=_public_check(check_line))
    step = v1.get("step")
    if not isinstance(step, dict) or step.get("script_sha256") != ADD_DEM_NAME_SHA256:
        return _refused("STEP_SCRIPT_SHA_MISMATCH", original_sha256=original_sha, v1_sha256=v1_sha, check=_public_check(check_line))
    if not isinstance(original, dict) or v1.get("source_sha256") != original.get("source_sha256"):
        return _refused("SOURCE_SHA_MISMATCH", original_sha256=original_sha, v1_sha256=v1_sha, check=_public_check(check_line))
    rows = v1.get("rows")
    codes = [row.get("race_code") for row in rows] if isinstance(rows, list) else None
    if codes != list(universe_codes):
        return _refused("ROWS_INVALID", original_sha256=original_sha, v1_sha256=v1_sha, check=_public_check(check_line))
    original_rows = original.get("rows") if isinstance(original.get("rows"), list) else []
    by_code = {}
    for row in original_rows:
        if isinstance(row, dict) and row.get("race_code") not in by_code:
            by_code[row.get("race_code")] = row
    for row in rows:
        prior = by_code.get(row.get("race_code"))
        if prior is None or not _probs_equal(row.get("dem_prob"), prior.get("dem_prob")):
            return _refused("DEM_PROB_MISMATCH", original_sha256=original_sha, v1_sha256=v1_sha, check=_public_check(check_line))
    return {
        "status": "DEM_NAME_ACCEPTED",
        "reason": None,
        "expected_script_sha256": ADD_DEM_NAME_SHA256,
        "observed_script_sha256": ADD_DEM_NAME_SHA256,
        "original_sha256": original_sha,
        "v1_sha256": v1_sha,
        "check": _public_check(check_line),
        "v1": v1,
    }


def run_dem_name_step(
    script_path,
    original_path,
    out_dir,
    *,
    runner=subprocess.run,
    python=sys.executable,
    expected_script_sha256=ADD_DEM_NAME_SHA256,
    universe_codes,
):
    """Run the script, then --check, then validate. A sha mismatch does not execute."""
    try:
        script_bytes = Path(script_path).read_bytes()
    except OSError:
        return _refused("SCRIPT_SHA_MISMATCH", expected_script_sha256=expected_script_sha256)
    observed = sha256_bytes(script_bytes)
    if observed != expected_script_sha256:
        return _refused(
            "SCRIPT_SHA_MISMATCH",
            expected_script_sha256=expected_script_sha256,
            observed_script_sha256=observed,
        )
    try:
        original_bytes = Path(original_path).read_bytes()
    except OSError:
        return _refused(
            "SCRIPT_REFUSED",
            expected_script_sha256=expected_script_sha256,
            observed_script_sha256=observed,
            exit_code=None,
        )
    original_sha = sha256_bytes(original_bytes)
    first = runner(
        [python, str(script_path), "--derived", str(original_path), "--out-dir", str(out_dir)],
        capture_output=True,
        text=True,
    )
    if first.returncode != 0:
        return _refused(
            "SCRIPT_REFUSED",
            expected_script_sha256=expected_script_sha256,
            observed_script_sha256=observed,
            original_sha256=original_sha,
            exit_code=first.returncode,
        )
    check = runner(
        [python, str(script_path), "--check", "--derived", str(original_path), "--out-dir", str(out_dir)],
        capture_output=True,
        text=True,
    )
    check_line = _last_json(getattr(check, "stdout", ""))
    if check.returncode != 0 or not isinstance(check_line, dict) or check_line.get("byte_identical") is not True:
        return _refused(
            "CHECK_FAILED",
            expected_script_sha256=expected_script_sha256,
            observed_script_sha256=observed,
            original_sha256=original_sha,
            check=_public_check(check_line),
            exit_code=check.returncode,
        )
    out_path = check_line.get("out")
    try:
        v1_bytes = Path(out_path).read_bytes()
    except (OSError, TypeError):
        return _refused(
            "CHECK_FAILED",
            expected_script_sha256=expected_script_sha256,
            observed_script_sha256=observed,
            original_sha256=original_sha,
            check=_public_check(check_line),
        )
    result = validate_dem_name_doc(original_bytes, v1_bytes, check_line, universe_codes)
    result["expected_script_sha256"] = expected_script_sha256
    result["observed_script_sha256"] = observed
    return result
