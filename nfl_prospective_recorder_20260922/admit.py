"""Stamp a prospective panel at the actual current time and append an admission log.

There is no switch for an earlier timestamp. If any included T−7d start has
already passed, the stamp is refused and nothing is written.
"""
import argparse,hashlib,json
from datetime import datetime,timezone
from pathlib import Path

from panel import validate_panel,window_start


def _iso(dt):
    return dt.astimezone(timezone.utc).replace(microsecond=0).isoformat()


def stamp_panel(panel,now):
    if not isinstance(panel,dict):
        raise ValueError('Panel must be an object')
    if panel.get('admitted_at') is not None:
        raise ValueError('Panel already has admitted_at; write a new panel version instead of restamping')
    if now.tzinfo is None:
        raise ValueError('now must be timezone-aware')
    stamped=json.loads(json.dumps(panel))
    stamped['admitted_at']=_iso(now)
    validate_panel(stamped,now=now,resuming=False)
    return stamped


def admission_record(stamped,panel_bytes):
    events=[]
    for game in stamped['events']:
        events.append(dict(
            game_id=game['game_id'],event=game['event'],kickoff=game['kickoff'],
            t_minus_7d_start=_iso(window_start(game['kickoff'])),
        ))
    missed=[]
    for game in stamped['ineligible_incomplete']:
        missed.append(dict(
            game_id=game['game_id'],event=game.get('event'),kickoff=game['kickoff'],
            t_minus_7d_start=game['t_minus_7d_start'],reason=game['reason'],
        ))
    return dict(
        admitted_at=stamped['admitted_at'],
        panel_version=stamped['panel_version'],
        cohort_id=stamped['cohort_id'],
        cohort_kind=stamped['cohort_kind'],
        purpose=stamped['purpose'],
        panel_sha256=hashlib.sha256(panel_bytes).hexdigest(),
        events=events,
        not_backfilled=missed,
        unresolved_not_admitted=[game['game_id'] for game in stamped.get('unresolved_identities',[])],
        collector_running=False,
        production_claim=False,
    )


def template_from_panel(panel):
    """Unstamped log form. admitted_at stays null on purpose."""
    record=admission_record(dict(panel,admitted_at='1970-01-01T00:00:00+00:00'),b'')
    record['admitted_at']=None
    record['panel_sha256']=None
    record['instructions']=(
        'Do not fill admitted_at by hand. Run admit.py at the host; it stamps the actual UTC time, '
        'refuses any included game whose T-7d start has already passed, and appends this record. '
        'Never copy an earlier timestamp to cover a missed window.'
    )
    return record


def write_admission(panel,out_panel,log_path,now=None):
    now=now or datetime.now(timezone.utc)
    stamped=stamp_panel(panel,now)
    payload=(json.dumps(stamped,indent=2)+'\n').encode()
    out_panel=Path(out_panel);out_panel.parent.mkdir(parents=True,exist_ok=True)
    out_panel.write_bytes(payload)
    record=admission_record(stamped,payload)
    log_path=Path(log_path);log_path.parent.mkdir(parents=True,exist_ok=True)
    with log_path.open('a') as handle:
        handle.write(json.dumps(record,sort_keys=True)+'\n')
    return record


def main(argv=None):
    parser=argparse.ArgumentParser(description='Admit a prospective panel at the current UTC time')
    parser.add_argument('--panel',type=Path,required=True)
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--log',type=Path,required=True)
    args=parser.parse_args(argv)
    panel=json.loads(args.panel.read_text())
    record=write_admission(panel,args.out,args.log)
    print(json.dumps(dict(
        admitted_at=record['admitted_at'],panel_sha256=record['panel_sha256'],
        events=len(record['events']),not_backfilled=len(record['not_backfilled']),
        collector_running=False,production_claim=False,
    ),sort_keys=True))


if __name__=='__main__':
    main()
