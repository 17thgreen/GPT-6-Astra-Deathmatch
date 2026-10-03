"""End-to-end score-column invariance probe for the EXT-K1 games csv.

Permutes the away_score and home_score columns across the 31 cohort rows
inside the pinned csv bytes. Uses random.Random(7): 25 shuffles, then one
shift-1 derangement (each cohort row receives the next row's score pair).
Every permutation rebuilds the join, consensus attachment, refusal gate and
markouts from scratch and hashes the four invariance artifacts.

Those artifact shas stay on constancy sha a73a90e0…. Permuting the moneyline
columns is the positive control and must change the artifacts. The cached
1,000-shuffle in T01(b) covers settle_artifact only and is not this rebuild.
"""

import csv
import io
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from artifacts import artifact_bytes, constancy_sha, four_shas  # noqa: E402
from consensus import join_cohort  # noqa: E402
from constants import PINS_REL, PINNED_GAME_IDS  # noqa: E402
from orchestrator import _attach_consensus, _attach_markouts, measure  # noqa: E402
from pins_io import verified_bytes  # noqa: E402

PROBE_SEED = 7
PROBE_SHUFFLES = 25
SCORE_COLUMNS = ("away_score", "home_score")
MONEYLINE_COLUMNS = ("away_moneyline", "home_moneyline")
CONSTANCY_SHA256 = "a73a90e0156c1b64b0ae3d70fd1b58e7279d4fff0b1c0b00a93108f62061d2d7"
RECORDED_ARTIFACT_SHAS = {
    "gate_assignments": "1594860cb1d20ee38cb03877d9ec30eab11fc74dd0d9d51734d9b12b280aae70",
    "splits": "6fb24d902c0e1cc89869ac6dab815792b1bb894eb90cb9535a5ecfb870a60ee2",
    "uch": "947970df887c49d1f7656c4666f2ebaf4de76ec865c718a9513ecf0f4f5c3733",
    "markouts_h": "c0d4d2a28b9f4167a4dcefed4262ad7635637a59ac0b835e2b1dc45d1ef91461",
}


def games_csv_text():
    return verified_bytes(PINS_REL["games"]).decode("utf-8")


def _table(csv_text):
    return list(csv.reader(io.StringIO(csv_text)))


def cohort_row_indexes(rows):
    header = rows[0]
    game_id = header.index("game_id")
    wanted = set(PINNED_GAME_IDS)
    indexes = [index for index, row in enumerate(rows) if row[game_id] in wanted]
    if len(indexes) != len(PINNED_GAME_IDS) or len(indexes) != len(wanted):
        raise RuntimeError(f"cohort csv rows {len(indexes)}")
    return indexes


def score_permutation_orders(n=len(PINNED_GAME_IDS), seed=PROBE_SEED, shuffles=PROBE_SHUFFLES):
    """25 Random(seed) shuffles, then shift-1. order[i] is the source slot."""
    rng = random.Random(seed)
    orders = []
    for _ in range(shuffles):
        order = list(range(n))
        rng.shuffle(order)
        orders.append(tuple(order))
    orders.append(tuple(list(range(1, n)) + [0]))
    return tuple(orders)


def moneyline_control_order(n=len(PINNED_GAME_IDS), seed=PROBE_SEED):
    order = list(range(n))
    random.Random(seed).shuffle(order)
    if order == list(range(n)):
        raise RuntimeError("moneyline control permutation was the identity")
    return tuple(order)


def permute_csv_columns(csv_text, columns, order):
    """Rewrite paired column values on the 31 cohort rows. Other cells stay."""
    rows = _table(csv_text)
    header = rows[0]
    columns_at = [header.index(name) for name in columns]
    selected = cohort_row_indexes(rows)
    if len(order) != len(selected):
        raise RuntimeError("permutation length")
    if sorted(order) != list(range(len(selected))):
        raise RuntimeError("permutation is not a rearrangement of the cohort")
    original = [tuple(rows[index][column] for column in columns_at) for index in selected]
    for slot, source in enumerate(order):
        for column, value in zip(columns_at, original[source]):
            rows[selected[slot]][column] = value
    buffer = io.StringIO()
    csv.writer(buffer, lineterminator="\n").writerows(rows)
    return buffer.getvalue()


def rebuild_blobs(measurement, csv_text):
    """Join, consensus, gate and markouts from csv_text. Does not touch the cache."""
    import copy

    joined = join_cohort(measurement["markets"], measurement["weeks"], csv_text)
    portions = copy.deepcopy(measurement["lots"]["portions"])
    _attach_consensus(portions, joined["by_event"])
    _attach_markouts(portions, measurement["book"], joined["by_event"])
    games = {
        event: {
            "away_team": row["away_team"],
            "home_team": row["home_team"],
            "away_score": row["away_score"],
            "home_score": row["home_score"],
        }
        for event, row in joined["by_event"].items()
    }
    return artifact_bytes(portions, games)


def run_score_probe(measurement, csv_text=None):
    """Return the baseline blobs and one blob dict per score permutation."""
    text = games_csv_text() if csv_text is None else csv_text
    baseline = rebuild_blobs(measurement, text)
    rebuilt = []
    for order in score_permutation_orders():
        rebuilt.append(rebuild_blobs(measurement, permute_csv_columns(text, SCORE_COLUMNS, order)))
    return baseline, tuple(rebuilt)


def main():
    measurement = measure(write=False)
    baseline, rebuilt = run_score_probe(measurement)
    base_sha = constancy_sha(baseline)
    base_four = four_shas(baseline)
    print(base_sha)
    if base_sha != CONSTANCY_SHA256 or base_four != RECORDED_ARTIFACT_SHAS:
        raise SystemExit("baseline constancy drifted")
    for blobs in rebuilt:
        if four_shas(blobs) != base_four or constancy_sha(blobs) != CONSTANCY_SHA256:
            raise SystemExit("score permutation moved an invariance artifact")
    control = rebuild_blobs(
        measurement,
        permute_csv_columns(games_csv_text(), MONEYLINE_COLUMNS, moneyline_control_order()),
    )
    if constancy_sha(control) == CONSTANCY_SHA256:
        raise SystemExit("moneyline permutation left the artifacts unchanged")
    print("score permutations", len(rebuilt))
    print("moneyline constancy", constancy_sha(control))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
