"""Restore pinned inputs; read-only GitHub/git access, with SHA-256 verification."""
from pathlib import Path
import argparse
import base64
import hashlib
import json
import subprocess
from urllib.parse import quote

ROOT=Path(__file__).resolve().parent


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo-root',type=Path,help='Existing git clone containing the pinned commit')
    parser.add_argument('--verify-only',action='store_true',help='Verify already restored inputs without network access')
    args=parser.parse_args()
    manifest=json.loads((ROOT/'SOURCE_MANIFEST.json').read_text())
    count=0
    for row in manifest['files']:
        if not row['required_for_reproduction']:continue
        path=row['path'];target=ROOT/'repo'/path
        if args.verify_only:
            data=target.read_bytes()
        elif args.repo_root:
            data=subprocess.run(['git','-C',str(args.repo_root.resolve()),'show',f"{manifest['commit']}:{path}"],
                                check=True,stdout=subprocess.PIPE).stdout
        else:
            endpoint=f"repos/{manifest['repository']}/contents/{quote(path,safe='/')}?ref={manifest['commit']}"
            response=subprocess.run(['gh','api','--method','GET',endpoint],check=True,stdout=subprocess.PIPE).stdout
            payload=json.loads(response)
            if payload.get('encoding')!='base64':raise ValueError(f'Unsupported content encoding: {path}')
            data=base64.b64decode(payload['content'])
        if hashlib.sha256(data).hexdigest()!=row['sha256']:
            raise ValueError(f'Source hash mismatch; refusing input: {path}')
        if not args.verify_only:
            target.parent.mkdir(parents=True,exist_ok=True)
            target.write_bytes(data)
        count+=1
    print(f'Verified {count} pinned source inputs.')


if __name__=='__main__':main()
