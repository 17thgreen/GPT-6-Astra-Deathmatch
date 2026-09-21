"""Download public nflverse source files. No account or trading access required."""
import argparse
import hashlib
import json
from pathlib import Path
import urllib.request

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,default=Path('data'))
    p.add_argument('--years',type=int,nargs='+',default=[2019,2020,2021,2022,2023,2024])
    args=p.parse_args();args.out.mkdir(parents=True,exist_ok=True);records=[]
    for year in args.years:
        name=f'play_by_play_{year}.parquet'
        url=f'https://github.com/nflverse/nflverse-data/releases/download/pbp/{name}'
        path=args.out/name
        if not path.exists():
            with urllib.request.urlopen(url,timeout=60) as response:
                data=response.read()
            if not data.startswith(b'PAR1'):raise ValueError(f'Not parquet: {url}')
            path.write_bytes(data)
        data=path.read_bytes()
        records.append(dict(file=name,url=url,bytes=len(data),sha256=hashlib.sha256(data).hexdigest()))
        print(name, len(data), flush=True)
    (args.out/'download_manifest.json').write_text(json.dumps(records,indent=2))

if __name__=='__main__':main()
