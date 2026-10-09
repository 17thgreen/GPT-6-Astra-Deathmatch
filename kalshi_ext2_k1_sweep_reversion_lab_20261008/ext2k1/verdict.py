"""Section 5 verdict table. First match wins. Examiner-owned; this is not a score."""

from .constants import CENSOR_SHARE_LIMIT, DROPPED_LIMIT, MIN_GAMES


def _floor_fail(side):
    if side.get("n_valid", 0) == 0:
        return True
    if side.get("point") is None or side.get("L") is None or side.get("U") is None:
        return True
    if side.get("kept", 0) < 2:
        return True
    if side.get("dropped", 0) > DROPPED_LIMIT:
        return True
    if side["L"] == side["U"]:
        return True
    share = side.get("censored_share")
    if share is not None and share > CENSOR_SHARE_LIMIT:
        return True
    if side.get("games_valid", 0) < MIN_GAMES:
        return True
    return False


def evaluate(yes, no, *, count_pass, structure_pass):
    if not count_pass:
        verdict, rule = "INCONCLUSIVE", "V1"
    elif not structure_pass:
        verdict, rule = "INCONCLUSIVE(STRUCTURE)", "V1s"
    elif _floor_fail(yes) or _floor_fail(no):
        verdict, rule = "INCONCLUSIVE", "V2"
    elif yes["L"] > 0 and no["L"] <= 0:
        verdict, rule = "KILL_EXT2K1", "V3"
    elif no["L"] > 0:
        verdict, rule = "ITERATE_DESCRIPTIVE", "V4"
    else:
        verdict, rule = "CLOSE_NULL", "V5"
    return {
        "verdict": verdict,
        "rule": rule,
        "owner": "Examiner",
        "status": "RUNNER_EVALUATION_NOT_A_SCORE",
    }
