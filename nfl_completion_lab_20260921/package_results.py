import hashlib,json,platform,sys,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def main():
    (ROOT/'results/runtime.json').write_text(json.dumps(dict(python=sys.version,platform=platform.platform()),indent=2))
    exclude={'NFL_Completion_Experiment_Kit.zip','DELIVERY_MANIFEST.json'}
    files=sorted(p for p in ROOT.rglob('*') if p.is_file() and p.name not in exclude
                 and '__pycache__' not in p.parts and not p.name.endswith(('.pyc','.partial')))
    manifest=dict(files=[dict(path=str(p.relative_to(ROOT)),bytes=p.stat().st_size,
                  sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in files])
    (ROOT/'DELIVERY_MANIFEST.json').write_text(json.dumps(manifest,indent=2))
    archive=ROOT/'NFL_Completion_Experiment_Kit.zip'
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for p in files+[ROOT/'DELIVERY_MANIFEST.json']:z.write(p,p.relative_to(ROOT))
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        for item in manifest['files']:assert hashlib.sha256(z.read(item['path'])).hexdigest()==item['sha256']
    print(json.dumps(dict(archive=str(archive),bytes=archive.stat().st_size,files=len(files)+1,
                         sha256=hashlib.sha256(archive.read_bytes()).hexdigest())))

if __name__=='__main__':main()
