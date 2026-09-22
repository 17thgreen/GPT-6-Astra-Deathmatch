"""Hash the complete source/input checkpoint before outcomes."""
import os
from m4_common import ROOT, M3, read, save, sha


def main():
    target=ROOT/'FROZEN_REPLAY.json'
    if target.exists():raise ValueError('Existing freeze')
    files=set()
    for name,digest in read(M3/'FROZEN_REPLAY.json')['sha256'].items():
        path=(M3/name).resolve()
        if sha(path)!=digest:raise ValueError('Inherited frozen file changed')
        files.add(path)
    for sport in ('NCAAF','WNBA'):
        for queue in (3300,10000):
            for delay in ('0.25','5'):
                name=f'{sport}_t30_constant_q{queue}_d{delay}'
                for suffix in ('.json','_fills.jsonl.gz','_orders.jsonl.gz'):
                    files.add(M3/'results'/(name+suffix))
    for path in ROOT.rglob('*'):
        if not path.is_file() or '__pycache__' in path.parts or 'results' in path.parts:
            continue
        if path.name.endswith('.partial.json') or path.name in ('replay.log','FROZEN_REPLAY.json'):
            continue
        files.add(path)
    out=dict(spec_commit='ed5be41760b74c01116fef633b5c6869b25b40ad',
        declared_cases=80,executable_cases=48,blocked_new_cohort_cases=32,
        sha256={os.path.relpath(path,ROOT):sha(path) for path in sorted(files)})
    save(target,out)
    print('FROZEN',len(files),'source/input/control files')


if __name__=='__main__':main()
