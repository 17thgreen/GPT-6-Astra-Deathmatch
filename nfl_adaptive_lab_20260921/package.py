import hashlib,json,platform,sys,zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parent


def main():
    (ROOT/'results/runtime.json').write_text(json.dumps(dict(python=sys.version,platform=platform.platform()),indent=2))
    paths=sorted(p for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts
        and p.name not in ['NFL_Adaptive_Kit.zip','DELIVERY_MANIFEST.json']
        and not p.name.endswith(('.pyc','.partial','.lock','-wal','-shm')))
    manifest=dict(files=[dict(path=str(p.relative_to(ROOT)),bytes=p.stat().st_size,
        sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in paths])
    (ROOT/'DELIVERY_MANIFEST.json').write_text(json.dumps(manifest,indent=2))
    archive=ROOT/'NFL_Adaptive_Kit.zip'
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for p in paths+[ROOT/'DELIVERY_MANIFEST.json']:z.write(p,p.relative_to(ROOT))
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        for f in manifest['files']:assert hashlib.sha256(z.read(f['path'])).hexdigest()==f['sha256']
    print(json.dumps(dict(file=str(archive),bytes=archive.stat().st_size,entries=len(paths)+1,
        sha256=hashlib.sha256(archive.read_bytes()).hexdigest())))


if __name__=='__main__':main()
