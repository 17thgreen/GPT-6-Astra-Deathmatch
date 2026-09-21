import argparse,json,sqlite3
from pathlib import Path


def inspect(path):
    db=sqlite3.connect(f'file:{Path(path).resolve()}?mode=ro',uri=True)
    integrity=db.execute('PRAGMA integrity_check').fetchone()[0]
    runs=[dict(id=i,started=s,ended=e,status=t) for i,s,e,t in db.execute('SELECT id,started,ended,status FROM runs ORDER BY id')]
    counts={kind:n for kind,n in db.execute('SELECT kind,COUNT(*) FROM responses GROUP BY kind')}
    missing=[]
    for ticker,through in db.execute('SELECT ticker,through_ts FROM checkpoints'):
        covered=db.execute('SELECT MAX(end_ts) FROM coverage WHERE ticker=?',(ticker,)).fetchone()[0]
        if covered!=through:missing.append(ticker)
    assert integrity=='ok' and not missing
    result=dict(integrity=integrity,runs=runs,response_counts=counts,distinct_trades=db.execute('SELECT COUNT(*) FROM trades').fetchone()[0],
        failed_responses=db.execute('SELECT COUNT(*) FROM responses WHERE ok=0').fetchone()[0],
        restart_gaps=db.execute('SELECT COUNT(*) FROM gaps').fetchone()[0],
        watermarks_match_completed_pagination=not missing,
        last_received=db.execute('SELECT MAX(received) FROM responses').fetchone()[0],
        note='Finite development capture; no orders placed. No claim of complete seven-day or holdout coverage.')
    db.close();return result


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('database',type=Path);p.add_argument('--output',type=Path);a=p.parse_args();r=inspect(a.database)
    if a.output:a.output.write_text(json.dumps(r,indent=2))
    print(json.dumps(r,indent=2))
