"""Label-permutation artifacts. Scores may change only the settlement markout."""

from canonical import canonical_bytes
from consensus import settlement_value
from gate import assignment_token, cell_key, iter_cells, portion_refused

ARTIFACT_ORDER = ("gate_assignments", "splits", "uch", "markouts_h")


def gate_assignments(portions):
    out = {}
    for portion in portions:
        cells = {}
        for x, exposure_floor, devig in iter_cells():
            refused = portion_refused(portion, x, exposure_floor, devig)
            cells[cell_key(x, exposure_floor, devig)] = assignment_token(refused)
        out[portion["portion_id"]] = cells
    return out


def splits_artifact(portions):
    return {
        portion["portion_id"]: {
            "S_DEV": portion["s_dev"],
            "S_FAV": portion["s_fav"],
        }
        for portion in portions
    }


def uch_artifact(portions):
    return {
        portion["portion_id"]: portion["uch"]
        for portion in portions
    }


def markouts_h_artifact(portions):
    """Horizons union CLOSE. Settlement is omitted on purpose."""
    out = {}
    for portion in portions:
        cells = {}
        for key, cell in portion["markouts"].items():
            if key == "SETTLE":
                continue
            cells[key] = cell["gross"]
        out[portion["portion_id"]] = cells
    return out


def settle_artifact(portions, games_by_event):
    out = {}
    for portion in portions:
        game = games_by_event[portion["event"]]
        value = settlement_value(game, portion["team_long"])
        if value is None:
            gross = None
        else:
            gross = value - portion["p_entry"]
        out[portion["portion_id"]] = gross
    return out


def artifact_bytes(portions, games_by_event):
    """Rebuild the four label-free artifacts. games_by_event is in scope for settlement only."""
    blobs = {
        "gate_assignments": canonical_bytes(gate_assignments(portions)),
        "splits": canonical_bytes(splits_artifact(portions)),
        "uch": canonical_bytes(uch_artifact(portions)),
        "markouts_h": canonical_bytes(markouts_h_artifact(portions)),
    }
    # Settlement is computed so a caller can see that scores move, and so this
    # function actually receives the score-bearing games. It is not one of the four.
    _settle = canonical_bytes(settle_artifact(portions, games_by_event))
    blobs["settle"] = _settle
    return blobs


def constancy_sha(blobs):
    """sha256 of the four artifact payloads in ARTIFACT_ORDER, name-prefixed."""
    import hashlib
    digest = hashlib.sha256()
    for name in ARTIFACT_ORDER:
        digest.update(name.encode("utf-8"))
        digest.update(b"\0")
        digest.update(blobs[name])
        digest.update(b"\0")
    return digest.hexdigest()


def sha_map(blobs):
    return {name: hashlib_sha(blobs[name]) for name in list(ARTIFACT_ORDER) + ["settle"]}


def hashlib_sha(blob):
    import hashlib
    return hashlib.sha256(blob).hexdigest()


def four_shas(blobs):
    return {name: hashlib_sha(blobs[name]) for name in ARTIFACT_ORDER}
