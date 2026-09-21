"""Reject incomplete or contaminated future evaluation evidence."""
import hashlib
import json
from datetime import datetime
from pathlib import Path

ROOT=Path(__file__).resolve().parent


def check(manifest,evidence):
    reasons=[];expected={g['game_id']:g for g in manifest['holdout_games']}
    if len(expected)!=32:reasons.append('Registry must contain 32 distinct games')
    first_window=min(datetime.fromisoformat(g['kickoff']).timestamp()-604800 for g in expected.values())
    frozen=evidence.get('candidate_frozen_at')
    if frozen is None or datetime.fromisoformat(frozen).timestamp()>=first_window:
        reasons.append('Candidate not demonstrably frozen before first reserved window')
    for key in ['candidate_sha256','baseline_sha256','execution_settings_sha256','data_manifest_sha256']:
        value=evidence.get(key,'')
        if len(value)!=64 or any(c not in '0123456789abcdef' for c in value):reasons.append('Missing immutable '+key)
    games=evidence.get('games',[]);ids=[g.get('game_id') for g in games]
    if len(ids)!=len(set(ids)):reasons.append('Duplicate game evidence')
    if set(ids)!=set(expected):reasons.append('Incomplete or altered 32-game cohort')
    development=set(manifest['development_events']+manifest['measurement_development_events'])
    events=[g.get('event') for g in games]
    if len(events)!=len(set(events)):reasons.append('Duplicated or missing venue identities')
    if any(event in development for event in events):reasons.append('Development/holdout overlap')
    for game in games:
        if not game.get('event') or not game.get('identity_verified'):reasons.append('Unverified venue identity')
        if not game.get('complete_window') or not game.get('data_hashes_verified'):reasons.append('Missing full-window data or verified hashes')
        if game.get('baseline_unresolved',1)!=0 or game.get('candidate_unresolved',1)!=0:reasons.append('Unresolved inventory')
    if evidence.get('shared_bankroll')!=5000 or evidence.get('bankroll_reset_between_games') is not False:
        reasons.append('One shared $5,000 account not established')
    if evidence.get('same_execution_assumptions') is not True:reasons.append('Execution assumptions not matched')
    return dict(status='INSUFFICIENT' if reasons else 'ELIGIBLE_FOR_COMPARISON_NOT_LIVE_VALIDATION',
                reasons=sorted(set(reasons)),completed_games=sum(bool(g.get('complete_window')) for g in games),
                required_games=32,note='Structural evidence gate only; values and hashes require independent provenance verification. No profit pass is inferred.')


if __name__=='__main__':
    manifest=json.loads((ROOT/'HOLDOUT_MANIFEST.json').read_text())
    evidence_path=ROOT/'results/holdout_evidence.json'
    result=check(manifest,json.loads(evidence_path.read_text()) if evidence_path.exists() else {})
    (ROOT/'results/holdout_status.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
