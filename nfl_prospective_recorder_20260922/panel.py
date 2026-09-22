"""Reviewed development and prospective panel checks.

A prospective panel may be stored with admitted_at null. Recording requires a
stamp that is strictly before every included T−7d start. Missed games stay in
ineligible_incomplete and are never polled.
"""
import re
from datetime import datetime, timedelta, timezone

from allowlist import allowed_recorder_path
from identity import expected_ticker, match_game, sanitize_listing_event

_VERSION = re.compile(r'[A-Za-z0-9._-]{1,64}')
_OUTCOME_KEYS = {
    'result', 'results', 'score', 'scores', 'winner', 'loser', 'settlement',
    'settlement_ts', 'settlement_value', 'settlement_value_dollars',
    'expiration_value', 'last_price', 'last_price_dollars',
    'previous_price_dollars', 'pnl', 'profit', 'payout', 'yes_bid_dollars',
    'no_bid_dollars', 'yes_ask_dollars', 'no_ask_dollars', 'volume',
    'volume_fp', 'open_interest', 'open_interest_fp',
}
RULES = [
    'Freeze this panel and stamp admitted_at before every included T-7d start. Do not backfill a start that has already passed.',
    'This is a new schedule-only version. It does not revive the prior 32-game complete-cohort gate.',
    'Venue tickers come only from a public KXNFLGAME listing match. Unmatched games keep a null event and are not polled.',
    'Do not store scores, results, settlement values, or prices in this panel.',
    'The recorder issues public GETs only. No credentials and no order routes.',
]
_WINDOW = timedelta(days=7)
_ADMIT_SKEW_SECONDS = 600


def window_start(kickoff):
    return _aware(kickoff, 'kickoff') - _WINDOW


def _aware(value, label):
    if not isinstance(value, str):
        raise ValueError(f'{label} must be a timestamp string')
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f'{label} is not an ISO timestamp') from exc
    if parsed.tzinfo is None:
        raise ValueError(f'{label} must include a timezone offset')
    return parsed.astimezone(timezone.utc)


def _reject_outcome_keys(obj, path='$'):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if str(key).lower() in _OUTCOME_KEYS:
                raise ValueError(f'Outcome field not allowed in panel: {path}.{key}')
            _reject_outcome_keys(value, f'{path}.{key}')
    elif isinstance(obj, list):
        for index, value in enumerate(obj):
            _reject_outcome_keys(value, f'{path}[{index}]')


def _same_instant(stamp, parsed):
    return _aware(stamp, 't_minus_7d_start') == parsed


def _development(panel):
    events = panel.get('events')
    if not isinstance(events, list) or not events:
        raise ValueError('Missing or duplicate events')
    seen = []
    for game in events:
        if not isinstance(game, dict):
            raise ValueError('Missing or duplicate events')
        event = game.get('event')
        if not isinstance(event, str) or not allowed_recorder_path('events/' + event):
            raise ValueError('Invalid event identifier')
        _aware(game.get('kickoff'), 'kickoff')
        seen.append(event)
    if len(set(seen)) != len(seen):
        raise ValueError('Missing or duplicate events')
    return events


def _row_ids(rows, require_event):
    ids = []
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError('Panel rows must be objects')
        game_id = row.get('game_id')
        if not isinstance(game_id, str) or not game_id:
            raise ValueError('game_id required')
        event = row.get('event')
        if require_event:
            if not isinstance(event, str) or not allowed_recorder_path('events/' + event):
                raise ValueError('Invalid event identifier')
            if event != expected_ticker(row):
                raise ValueError(f'event ticker does not match schedule date and teams for {game_id}')
            start = window_start(row['kickoff'])
            if 't_minus_7d_start' not in row or not _same_instant(row['t_minus_7d_start'], start):
                raise ValueError(f't_minus_7d_start must equal kickoff minus 7 days for {game_id}')
        else:
            if event is not None:
                raise ValueError(f'unresolved identity must keep a null event for {game_id}')
            _aware(row.get('kickoff'), 'kickoff')
            if not row.get('reason'):
                raise ValueError(f'unresolved identity needs a reason for {game_id}')
        ids.append((game_id, event))
    return ids


def validate_structure(panel):
    """Static checks. A prospective template may omit admitted_at."""
    if not isinstance(panel, dict):
        raise ValueError('Panel must be an object')
    _reject_outcome_keys(panel)
    purpose = panel.get('purpose')
    if purpose == 'development':
        return _development(panel)
    if purpose not in ('prospective', 'holdout'):
        raise ValueError('purpose must be development, prospective, or holdout')
    if panel.get('frozen_before_windows') is not True:
        raise ValueError('frozen_before_windows must be true before a prospective panel is used')
    if panel.get('complete_prior_32_game_cohort') is not False:
        raise ValueError('This panel cannot claim the prior 32-game complete cohort')
    if not isinstance(panel.get('panel_version'), str) or not _VERSION.fullmatch(panel['panel_version']):
        raise ValueError('panel_version required')
    if not isinstance(panel.get('cohort_id'), str) or not panel['cohort_id']:
        raise ValueError('cohort_id required')
    if panel.get('cohort_kind') not in ('schedule_only_new', 'partial_salvage_explicit'):
        raise ValueError('cohort_kind must be schedule_only_new or partial_salvage_explicit')
    if purpose == 'holdout' and panel.get('reviewed') is not True:
        raise ValueError('holdout purpose requires reviewed true; a bare holdout panel is rejected')
    if not isinstance(panel.get('rules'), list) or panel['rules'] != RULES:
        raise ValueError('panel rules must be the frozen admission rules')
    classified = _aware(panel.get('classified_as_of'), 'classified_as_of')
    retrieved = _aware(panel.get('identity_listing_retrieved_at'), 'identity_listing_retrieved_at')
    if classified + timedelta(minutes=5) < retrieved:
        raise ValueError('classification clock cannot predate the listing retrieval')
    if panel.get('admitted_at') is not None:
        _aware(panel.get('admitted_at'), 'admitted_at')
    events = panel.get('events')
    ineligible = panel.get('ineligible_incomplete')
    unresolved = panel.get('unresolved_identities')
    if not isinstance(events, list) or not events:
        raise ValueError('Missing or duplicate events')
    if not isinstance(ineligible, list) or not isinstance(unresolved, list):
        raise ValueError('ineligible_incomplete and unresolved_identities must be lists')
    event_ids = _row_ids(events, require_event=True)
    if len({item[0] for item in event_ids}) != len(event_ids) or len({item[1] for item in event_ids}) != len(event_ids):
        raise ValueError('Missing or duplicate events')
    ineligible_ids = []
    for row in ineligible:
        if not isinstance(row, dict) or not row.get('reason'):
            raise ValueError('ineligible rows need a reason')
        game_id = row.get('game_id')
        event = row.get('event')
        if not isinstance(game_id, str) or not game_id:
            raise ValueError('game_id required')
        if event is not None and (not isinstance(event, str) or not allowed_recorder_path('events/' + event)):
            raise ValueError('Invalid event identifier')
        if event is not None and event != expected_ticker(row):
            raise ValueError(f'ineligible event does not match schedule date and teams for {game_id}')
        start = window_start(row['kickoff'])
        if 't_minus_7d_start' not in row or not _same_instant(row['t_minus_7d_start'], start):
            raise ValueError('ineligible t_minus_7d_start must equal kickoff minus 7 days')
        if start > classified:
            raise ValueError('cannot mark a game incomplete before its T-7d start')
        ineligible_ids.append((game_id, event))
    unresolved_ids = _row_ids(unresolved, require_event=False)
    game_ids = [item[0] for item in event_ids + ineligible_ids + unresolved_ids]
    if len(set(game_ids)) != len(game_ids):
        raise ValueError('a game cannot appear in more than one panel list')
    tickers = [item[1] for item in event_ids + ineligible_ids if item[1]]
    if len(set(tickers)) != len(tickers):
        raise ValueError('duplicate venue event')
    polled = {item[1] for item in event_ids}
    blocked = {item[1] for item in ineligible_ids if item[1]}
    if polled & blocked:
        raise ValueError('an ineligible event cannot be polled')
    for game in events:
        if window_start(game['kickoff']) <= classified:
            raise ValueError(f'{game["game_id"]} was already inside its window at classification; do not backfill')
    return events


def validate_panel(panel, now=None, resuming=False):
    """Recording gate. Development panels skip the admission clock."""
    events = validate_structure(panel)
    if panel.get('purpose') == 'development':
        return events
    if panel.get('admitted_at') is None:
        raise ValueError('admitted_at is required before recording; do not backdate a missed window')
    admitted = _aware(panel['admitted_at'], 'admitted_at')
    if now is None:
        now = datetime.now(timezone.utc)
    if now.tzinfo is None:
        raise ValueError('now must be timezone-aware')
    now = now.astimezone(timezone.utc)
    for game in events:
        start = window_start(game['kickoff'])
        if admitted >= start:
            raise ValueError(f'admission is not before T-7d for {game["game_id"]}; do not backfill')
        if not resuming:
            if now >= start:
                raise ValueError(f'T-7d already passed for {game["game_id"]}; do not backfill')
            if abs((now - admitted).total_seconds()) > _ADMIT_SKEW_SECONDS:
                raise ValueError('admitted_at must match recorder start; do not backdate')
    return events


def _iso(dt):
    return dt.astimezone(timezone.utc).replace(microsecond=0).isoformat()


def build_panel(registry, listings, as_of, retrieved_at, panel_version, cohort_id):
    """Classify a reserved schedule without copying outcome fields."""
    if not isinstance(registry, dict) or not isinstance(registry.get('holdout_games'), list):
        raise ValueError('schedule registry must contain holdout_games')
    games = registry['holdout_games']
    blocked = set(registry.get('development_events') or []) | set(registry.get('measurement_development_events') or [])
    as_of = as_of.astimezone(timezone.utc)
    retrieved_at = retrieved_at.astimezone(timezone.utc)
    if as_of + timedelta(minutes=5) < retrieved_at:
        raise ValueError('classification clock cannot predate the listing retrieval')
    clean = [sanitize_listing_event(row) for row in listings]
    events, ineligible, unresolved = [], [], []
    for game in games:
        found = match_game(game, clean)
        if found['status'] == 'ambiguous' or found['status'] == 'subtitle_mismatch':
            raise ValueError(f'ambiguous public identity for {game.get("game_id")}')
        start = window_start(game['kickoff'])
        base = dict(game_id=game['game_id'], kickoff=game['kickoff'], away=game['away'], home=game['home'],
                    t_minus_7d_start=_iso(start))
        published = game.get('event')
        if found['status'] == 'matched':
            ticker = found['event_ticker']
            if published and published != ticker:
                raise ValueError(f'registry event disagrees with listing for {game["game_id"]}')
            if ticker in blocked:
                raise ValueError('development event cannot enter the prospective panel')
        else:
            ticker = None
        if start <= as_of:
            row = dict(base, event=ticker if ticker else published, reason=(
                'T-7d already started at classification; full window was not recorded. Do not backfill.'
            ))
            if row['event'] is not None and row['event'] != expected_ticker(game):
                raise ValueError(f'ineligible event does not match schedule for {game["game_id"]}')
            ineligible.append(row)
        elif ticker:
            events.append(dict(base, event=ticker, identity='public_events_listing_title_only'))
        else:
            unresolved.append(dict(base, event=None, reason=(
                'No open or unopened KXNFLGAME listing row matched the Eastern kickoff date and ticker team codes.'
            )))
    if not events:
        raise ValueError('classification produced no eligible games')
    panel = dict(
        purpose='prospective',
        panel_version=panel_version,
        cohort_id=cohort_id,
        cohort_kind='schedule_only_new',
        frozen_before_windows=True,
        complete_prior_32_game_cohort=False,
        admitted_at=None,
        classified_as_of=_iso(as_of),
        identity_listing_retrieved_at=_iso(retrieved_at),
        source_registry='nfl_factorial_lab_20260921/RESERVED_HOLDOUT.json',
        source_listing='GET /trade-api/v2/events?series_ticker=KXNFLGAME&status=open|unopened&with_nested_markets=false',
        rules=list(RULES),
        events=events,
        ineligible_incomplete=ineligible,
        unresolved_identities=unresolved,
    )
    validate_structure(panel)
    return panel
