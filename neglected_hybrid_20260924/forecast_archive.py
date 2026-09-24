"""Recover the exact pre-election 538 snapshots; never backdate later captures."""
from datetime import datetime, timezone
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse,gzip,hashlib,json,re,urllib.request

SOURCES=[
 ('house','20241103203857','house_latest_20241103'),
 ('senate','20241103203855','senate_latest_20241103'),
 ('house','20241010062315','house_latest_20241010'),
]
def capture(item,root):
    chamber,ts,name=item
    original=f'https://projects.fivethirtyeight.com/2024-election-forecast/{chamber}/states_latest.json'
    url=f'https://web.archive.org/web/{ts}id_/{original}'
    info={'url':url,'original_url':original,'chamber':chamber,'requested_capture':ts,
          'retrieved_at':datetime.now(timezone.utc).isoformat()}
    try:
        with urllib.request.urlopen(url,timeout=30) as r:
            body=r.read(2_000_001);info.update(status=r.status,final_url=r.url,headers=dict(r.headers))
        if len(body)>2_000_000:raise ValueError('Capture too large')
        root.mkdir(parents=True,exist_ok=True)
        (root/(name+'.body')).write_bytes(body)
        info['body_sha256']=hashlib.sha256(body).hexdigest()
        plain=gzip.decompress(body) if body[:2]==b'\x1f\x8b' else body
        data=json.loads(plain)
        actual=re.search(r'/web/(\d{14})(?:id_)?/',info['final_url'])
        if not actual or actual.group(1)!=ts:raise ValueError('Archive redirected to a different capture')
        (root/(name+'.json')).write_bytes(plain)
        info.update(decoded_sha256=hashlib.sha256(plain).hexdigest(),rows=len(data),
                    available_at=datetime.strptime(ts,'%Y%m%d%H%M%S').replace(tzinfo=timezone.utc).isoformat(),
                    source_file=name+'.json',admitted=True)
    except Exception as e:info.update(admitted=False,error=str(e))
    (root/(name+'.receipt.json')).write_text(json.dumps(info,indent=2)+'\n')
    return info

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('root',type=Path);a=p.parse_args();a.root.mkdir(parents=True,exist_ok=True)
    with ThreadPoolExecutor(max_workers=3) as pool:
        for f in as_completed([pool.submit(capture,x,a.root) for x in SOURCES]):
            r=f.result();print(json.dumps({k:r.get(k) for k in ['chamber','requested_capture','admitted','rows','error']}),flush=True)
