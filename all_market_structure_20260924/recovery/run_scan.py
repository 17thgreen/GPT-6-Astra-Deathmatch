"""Recovery wrapper; original protocol and source remain immutable."""
import sys,json,threading
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent))
import scan
scan.ROOT=ROOT
lock=threading.Lock()
original_get=scan.get
original_catalog=scan.catalog
def get(*a,**kw):
    data,receipts=original_get(*a,**kw)
    with lock:
        with (ROOT/'receipts.jsonl').open('a') as f:
            for r in receipts:f.write(json.dumps(r)+'\n')
            f.flush()
    return data,receipts
def catalog(path,key,params=None):
    result=original_catalog(path,key,params)
    (ROOT/(path.strip('/').replace('/','_')+'.json')).write_text(json.dumps(result[0]))
    print('CHECKPOINT',path,result[2],flush=True)
    return result
if __name__=='__main__':
    if (ROOT/'receipts.jsonl').exists():raise SystemExit('existing run; refusing overwrite')
    scan.get=get;scan.catalog=catalog
    scan.main()
