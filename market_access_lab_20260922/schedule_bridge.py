"""Normalize a venue milestone response into an explicit start-time input.

This does not establish event state (scheduled/postponed/in play), historical
knowledge, or market admission. Caller supplies the response receipt timestamp.
"""
from datetime import datetime
from adapter import Schedule


def from_milestones(event,response,received_at,expected_type):
    if expected_type not in ('football_game','basketball_game','baseball_game','hockey_match'):
        raise ValueError('Unsupported full-game milestone type')
    matches=[m for m in response.get('milestones',[]) if event in m.get('related_event_tickers',[]) and m.get('type')==expected_type and m.get('category')=='Sports']
    if len(matches)!=1:raise ValueError('Missing or ambiguous exact event milestone')
    m=matches[0]
    if not m.get('id') or not m.get('start_date'):raise ValueError('Missing milestone identity/start')
    start=datetime.fromisoformat(m['start_date'].replace('Z','+00:00'))
    if start.tzinfo is None:raise ValueError('Start time needs a timezone')
    return Schedule(event,start.timestamp(),received_at,'https://api.elections.kalshi.com/trade-api/v2/milestones/'+m['id'])
