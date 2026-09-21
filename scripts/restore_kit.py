"""Restore indexed external files from an exact owner-supplied research ZIP."""
import argparse,hashlib,json,zipfile
from pathlib import Path,PurePosixPath
ROOT=Path(__file__).resolve().parents[1]

def main():
    ap=argparse.ArgumentParser();ap.add_argument('archive',type=Path);args=ap.parse_args()
    digest=hashlib.sha256(args.archive.read_bytes()).hexdigest()
    matches=[r for r in json.loads((ROOT/'provenance/ARCHIVES.json').read_text()) if r['sha256']==digest]
    if len(matches)!=1:raise SystemExit('Archive SHA-256 is not uniquely recognized')
    prefix=PurePosixPath(matches[0]['path']).parent
    expected={r['path']:r for r in json.loads((ROOT/'provenance/EXTERNAL_ARTIFACTS.json').read_text()) if PurePosixPath(r['path']).is_relative_to(prefix)}
    restored=0
    with zipfile.ZipFile(args.archive) as archive:
        for entry in archive.infolist():
            rel=PurePosixPath(entry.filename)
            if rel.is_absolute() or '..' in rel.parts:raise SystemExit('Unsafe archive path')
            key=str(prefix/rel)
            if entry.is_dir() or key not in expected:continue
            data=archive.read(entry);record=expected[key]
            if len(data)!=record['bytes'] or hashlib.sha256(data).hexdigest()!=record['sha256']:raise SystemExit('Artifact hash mismatch: '+key)
            target=ROOT/key
            if target.exists():
                if hashlib.sha256(target.read_bytes()).hexdigest()!=record['sha256']:raise SystemExit('Refusing to overwrite different existing file: '+key)
                continue
            target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data);restored+=1
    print(f'Restored {restored} verified external files into {prefix}')
if __name__=='__main__':main()
