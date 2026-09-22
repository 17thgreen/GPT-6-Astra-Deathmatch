"""Apply documented manual contract review and deterministic identity checks."""
import copy
import re
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from m4_common import ROOT, M2, read, save, sha


def identity_checks(game):
    event = game['metadata']['event']
    milestone = game['matched_milestone']
    if event.get('product_metadata', {}).get('competition_scope') != 'Game':
        raise ValueError('Not full-game scope')
    if milestone.get('details', {}).get('main_game_event_ticker') != game['event']:
        raise ValueError('Not the milestone main game')
    date = datetime.fromtimestamp(game['kickoff'], timezone.utc).astimezone(ZoneInfo('America/New_York'))
    encoded = date.strftime('%y%b%d').upper()
    if not game['event'].startswith(game['series']+'-'+encoded):
        raise ValueError('Encoded date differs from reconstructed Eastern game date')
    rule_date = date.strftime('%b ')+str(date.day)+date.strftime(', %Y')
    for market in game['markets']:
        primary = market['rules_primary']
        if not primary.startswith('If '+market['yes_sub_title']+' wins ') or rule_date not in primary:
            raise ValueError('Rule team/date mismatch')
        if market['yes_sub_title'] not in event['title']:
            raise ValueError('Team not in event title')
    number = re.search(r'G([12])$', game['event'])
    if number:
        n = number[1]
        if '(game '+n+')' not in milestone['title'].lower():
            raise ValueError('Doubleheader milestone game number mismatch')
        if any('game '+n+' of the double header' not in m['rules_primary'].lower() for m in game['markets']):
            raise ValueError('Doubleheader contract game number mismatch')
    if game['series'] == 'KXMLBGAME':
        rule_time = date.strftime('%I:%M %p').lstrip('0')+' '+date.tzname()
        if any(rule_time not in m['rules_primary'] for m in game['markets']):
            raise ValueError('Baseball rule time and milestone differ')
    return dict(rule_team_date=True, full_game=True, main_milestone=True,
                game_number=int(number[1]) if number else None,
                schedule=milestone['start_date'], season_phase=event['product_metadata'].get('competition'))


def main():
    if (ROOT/'COHORT.json').exists():
        raise ValueError('Cohort already frozen')
    original = read(ROOT/'COHORT_METADATA.json')
    out = copy.deepcopy(original)
    old_events = {g['event'] for g in read(M2/'COHORT.json')['games']}
    assert not old_events.intersection(out['reserved']['KXNCAAFGAME'])
    for game in out['games']:
        series = game['series']
        if game['structurally_admitted']:
            game['identity_review'] = identity_checks(game)
        if series in ('KXNCAAFGAME', 'KXMLBGAME'):
            game['replay_admitted'] = game['structurally_admitted']
            game['manual_review_required'] = False
            game['admission_scope'] = 'ORDINARY_SCHEDULED_PREGAME_COUNTERFACTUAL'
            game['manual_note'] = ('Team aliases, original game date and full-game scope reviewed. '
                'For MLB, EDT rule times and doubleheader game number also agree exactly with milestone. '
                'Cancellation/postponement histories and collateral timing are not reconstructed. '
                'No terminal payoff is used; positive net requires flat inventory before cutoff.')
        elif series == 'KXNHLGAME':
            game['admission_scope'] = 'PRESEASON_METADATA_ONLY_FRACTIONAL_RULES_REQUIRE_SEPARATE_ADAPTER_REVIEW'
            game['manual_note'] = ('Current event rules specify 50c for ties. This preserves a $1 pair '
                'for the two team-YES contracts in a two-team tie, but the existing strict binary '
                'payoff admission checker rejects fractional states. Fair-price exceptional states '
                'and immediate cross-market collateral equivalence are not established. '
                'Event product metadata says NHL Preseason; no regular-season inference.')
        else:
            game['admission_scope'] = 'MAY_PLAYOFF_METADATA_RESERVED_RULE_HISTORY_UNRESOLVED'
            game['manual_note'] = ('Primary rules identify the game, but archived secondary rules '
                'are empty. Current September-amended generic terms cannot establish May exception '
                'rules. Preserve reservation and missing-rule finding; no NBA profit replay in M4.')
    out['sports'] = {}
    for series in ('KXNCAAFGAME','KXMLBGAME'):
        games = [g for g in out['games'] if g['series']==series]
        fees = {(g['coefficients']['maker'],g['coefficients']['taker']) for g in games if g['structurally_admitted']}
        complete = len(games)==8 and all(g['replay_admitted'] for g in games) and len(fees)==1 and not out['failures']
        if not complete:
            for game in games:
                game['replay_admitted'] = False
        out['sports'][series] = dict(admitted=complete, games=len(games), coefficients=list(next(iter(fees))) if len(fees)==1 else None)
    out['metadata_sha256'] = sha(ROOT/'COHORT_METADATA.json')
    out['status'] = 'FIXED_COHORT_BEFORE_TAPES_AND_OUTCOMES'
    save(ROOT/'COHORT.json', out)
    print(out['sports'])


if __name__ == '__main__':
    main()
