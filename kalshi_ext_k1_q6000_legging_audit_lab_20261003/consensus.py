"""R09–R17 consensus join, de-vig, and ON/AGAINST splits. Ex-post anchor [U]."""

import csv
import io
import math
from datetime import datetime
from zoneinfo import ZoneInfo

from constants import ALIAS_MAP, PINNED_GAME_IDS, PRIMARY_DELTA
from errors import ClosedUniverseRefused, HoldoutRefused, JoinRefused
from refusals import assert_not_holdout

ET = ZoneInfo("America/New_York")
MONTHS = {
    "JAN": 1, "FEB": 2, "MAR": 3, "APR": 4, "MAY": 5, "JUN": 6,
    "JUL": 7, "AUG": 8, "SEP": 9, "OCT": 10, "NOV": 11, "DEC": 12,
}


def ticker_date(event):
    token = event.split("-")[1]
    year = 2000 + int(token[0:2])
    month = MONTHS[token[2:5]]
    day = int(token[5:7])
    return f"{year:04d}-{month:02d}-{day:02d}"


def alias_team(code, alias_map=None):
    table = ALIAS_MAP if alias_map is None else alias_map
    return table.get(code, code)


def event_teams(markets, event):
    suffixes = []
    kickoff = None
    for ticker, meta in markets.items():
        if meta["event"] != event:
            continue
        suffixes.append(ticker.split("-")[-1])
        kickoff = meta["kickoff"]
    if len(suffixes) != 2 or kickoff is None:
        raise ClosedUniverseRefused(event)
    return suffixes, kickoff


def parse_moneyline(value):
    if value is None:
        return None
    text = str(value).strip()
    if text == "" or text.lower() in {"na", "nan", "none", "null"}:
        return None
    try:
        number = float(text)
    except ValueError:
        return None
    if not math.isfinite(number) or number == 0:
        return None
    return number


def american_implied(moneyline):
    """R11. Missing, zero, or non-numeric is None (game UNCLASSIFIED)."""
    if moneyline is None:
        return None
    if moneyline < 0:
        magnitude = abs(moneyline)
        return magnitude / (magnitude + 100.0)
    if moneyline > 0:
        return 100.0 / (moneyline + 100.0)
    return None


def proportional(q_away, q_home):
    total = q_away + q_home
    p_home = q_home / total
    return 1.0 - p_home, p_home


def shin_probabilities(q_away, q_home, iterations=200):
    """R12 sensitivity. Bisection of z on [0, 0.4] for 200 iterations."""
    total_q = q_away + q_home

    def probs(z):
        scale = 2.0 * (1.0 - z)
        out = []
        for qi in (q_away, q_home):
            inner = z * z + 4.0 * (1.0 - z) * (qi * qi) / total_q
            out.append((math.sqrt(inner) - z) / scale)
        return out

    lo, hi = 0.0, 0.4
    for _ in range(iterations):
        mid = (lo + hi) / 2.0
        if sum(probs(mid)) > 1.0:
            lo = mid
        else:
            hi = mid
    z = (lo + hi) / 2.0
    p_away, p_home = probs(z)
    return p_away, p_home, z


def _load_games(csv_text):
    return list(csv.DictReader(io.StringIO(csv_text)))


def join_cohort(markets, week_membership, csv_text, alias_map=None, require_time=True):
    """R10. Exactly one nflverse candidate per cohort event, else JoinRefused.

    alias_map defaults to {JAC: JAX, LAR: LA}. Pass {} to require raw codes.
    Non-cohort nflverse rows are not analysis inputs. A joined holdout game_id raises.
    """
    if alias_map is None:
        alias_map = ALIAS_MAP
    games = _load_games(csv_text)
    joined = []
    exact_without_alias = 0
    alias_events = {}
    for event in sorted(week_membership):
        assert_not_holdout(event=event)
        suffixes, kickoff = event_teams(markets, event)
        mapped = sorted(alias_team(code, alias_map) for code in suffixes)
        raw = sorted(suffixes)
        when = datetime.fromtimestamp(kickoff, ET)
        gameday = when.strftime("%Y-%m-%d")
        gametime = when.strftime("%H:%M")
        if ticker_date(event) != gameday:
            raise JoinRefused(f"ticker date {event} {ticker_date(event)} != {gameday}")
        candidates = []
        for row in games:
            if str(row.get("season")) != "2026" or row.get("game_type") != "REG":
                continue
            if row.get("gameday") != gameday:
                continue
            sides = sorted((row.get("away_team"), row.get("home_team")))
            if sides == mapped:
                candidates.append(row)
        if len(candidates) != 1:
            raise JoinRefused(f"{event} candidates={len(candidates)}")
        row = candidates[0]
        if require_time and row.get("gametime") != gametime:
            raise JoinRefused(f"{event} gametime {row.get('gametime')} != {gametime}")
        assert_not_holdout(game_id=row["game_id"], event=event)
        away_ml = parse_moneyline(row.get("away_moneyline"))
        home_ml = parse_moneyline(row.get("home_moneyline"))
        q_away = american_implied(away_ml)
        q_home = american_implied(home_ml)
        unclassified = q_away is None or q_home is None
        if unclassified:
            p_away_prop = p_home_prop = p_away_shin = p_home_shin = shin_z = None
            overround = None
        else:
            p_away_prop, p_home_prop = proportional(q_away, q_home)
            p_away_shin, p_home_shin, shin_z = shin_probabilities(q_away, q_home)
            overround = q_away + q_home
        raw_match = [
            other for other in games
            if str(other.get("season")) == "2026"
            and other.get("game_type") == "REG"
            and other.get("gameday") == gameday
            and sorted((other.get("away_team"), other.get("home_team"))) == raw
        ]
        if len(raw_match) == 1:
            exact_without_alias += 1
        else:
            alias_events[event] = sorted(code for code in suffixes if code in (alias_map or {}))
        joined.append({
            "event": event,
            "game_id": row["game_id"],
            "away_team": row["away_team"],
            "home_team": row["home_team"],
            "gameday": gameday,
            "gametime": gametime,
            "away_moneyline": away_ml,
            "home_moneyline": home_ml,
            "away_score": row.get("away_score"),
            "home_score": row.get("home_score"),
            "q_away": q_away,
            "q_home": q_home,
            "overround": overround,
            "p_away_prop": p_away_prop,
            "p_home_prop": p_home_prop,
            "p_away_shin": p_away_shin,
            "p_home_shin": p_home_shin,
            "shin_z": shin_z,
            "unclassified": unclassified,
            "kalshi_suffixes": suffixes,
        })
    if len(joined) != 31 or len({row["game_id"] for row in joined}) != 31:
        raise JoinRefused("join count")
    game_ids = tuple(row["game_id"] for row in joined)
    if game_ids != PINNED_GAME_IDS:
        raise JoinRefused("joined game_id list")
    return {
        "rows": joined,
        "by_event": {row["event"]: row for row in joined},
        "exact_without_alias": exact_without_alias,
        "alias_events": alias_events,
        "game_ids": game_ids,
    }


def p_cons_for_team(game, team_long, method, alias_map=None):
    if game["unclassified"]:
        return None
    team = alias_team(team_long, ALIAS_MAP if alias_map is None else alias_map)
    if method == "proportional":
        away_key, home_key = "p_away_prop", "p_home_prop"
    elif method == "shin":
        away_key, home_key = "p_away_shin", "p_home_shin"
    else:
        raise JoinRefused(method)
    if team == game["home_team"]:
        return game[home_key]
    if team == game["away_team"]:
        return game[away_key]
    raise HoldoutRefused(team_long)


def deviation(p_cons, m_open):
    if p_cons is None or m_open is None:
        return None
    return p_cons - m_open


def split_dev(dev, delta=PRIMARY_DELTA):
    """R16. ON if consensus is above the Kalshi mid by more than delta."""
    if dev is None:
        return "UNCLASSIFIED"
    if dev > delta:
        return "ON"
    if dev < -delta:
        return "AGAINST"
    return "NEUTRAL"


def split_fav(p_cons):
    """R17. ON if the open leg is the consensus favorite."""
    if p_cons is None:
        return "UNCLASSIFIED"
    if p_cons > 0.5:
        return "ON"
    if p_cons < 0.5:
        return "AGAINST"
    return "NEUTRAL"


def settlement_value(game, team_long, alias_map=None):
    """R23. 1 if team_long won, 0 if it lost, None if tied or missing. Scores only."""
    away = game.get("away_score")
    home = game.get("home_score")
    if away is None or home is None or str(away).strip() == "" or str(home).strip() == "":
        return None
    try:
        away_score = float(away)
        home_score = float(home)
    except ValueError:
        return None
    if not math.isfinite(away_score) or not math.isfinite(home_score) or away_score == home_score:
        return None
    winner = game["home_team"] if home_score > away_score else game["away_team"]
    team = alias_team(team_long, ALIAS_MAP if alias_map is None else alias_map)
    if team == winner:
        return 1.0
    if team in (game["home_team"], game["away_team"]):
        return 0.0
    return None
