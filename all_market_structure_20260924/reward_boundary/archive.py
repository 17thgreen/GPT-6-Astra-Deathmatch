"""Package replay evidence separately from source and summarize alternatives."""
import collections,hashlib,json,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def main():
    summary=json.loads((ROOT/'SUMMARY.json').read_text());rows=summary['best_per_side_observation']
    groups={}
    for source in summary['observations_by_source']:
        xs=[r for r in rows if r['source']==source]
        groups[source]={'passing_side_observations':len(xs),'unique_markets':len(set(r['ticker'] for r in xs)),
            'supported_side_observations':sum(r['classification']=='supported_level' for r in xs),
            'supported_unique_markets':len(set(r['ticker'] for r in xs if r['classification']=='supported_level')),
            'supported_events':sorted(set(r['event_ticker'] for r in xs if r['classification']=='supported_level'))}
    supported=[r for r in rows if r['classification']=='supported_level']
    first={};last={}
    for r in sorted(supported,key=lambda x:x['book_received_ns']):
        key=(r['program_id'],r['side']);first.setdefault(key,r);last[key]=r
    metrics={k:v for k,v in summary.items() if k!='best_per_side_observation'}
    metrics.update(by_source=groups,supported_first=list(first.values()),supported_last=list(last.values()))
    (ROOT/'METRICS.json').write_text(json.dumps(metrics,indent=2)+'\n')
    paths=[ROOT/x for x in ('CASES.jsonl','SUMMARY.json','INPUT_HASHES.json')]
    hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths};(ROOT/'EVIDENCE_HASHES.json').write_text(json.dumps(hashes,indent=2)+'\n')
    out=ROOT.parents[2]/'artifacts'/'AMS_011_Replay_Evidence.zip'
    with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in paths+[ROOT/'EVIDENCE_HASHES.json']:z.write(p,p.name)
    with zipfile.ZipFile(out) as z:assert z.testzip() is None
    a={'filename':out.name,'bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'dependencies':'Requires separately retained AMS-005, AMS-007, AMS-009 and AMS-010 raw books for scoring replay. No duplicate raw public captures included here.'}
    (ROOT/'ARCHIVE.json').write_text(json.dumps(a,indent=2)+'\n');print(json.dumps({'by_source':groups,'supported_distinct_program_sides':len(first),'archive':a},indent=2))

if __name__=='__main__':main()
