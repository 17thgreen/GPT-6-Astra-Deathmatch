"""Canonical Q2 inputs for standalone offline reproduction; no outcome selection."""
import gzip,hashlib,importlib.util,json
from pathlib import Path

ROOT=Path(__file__).resolve().parent


def main():
    source=ROOT.parent/'nfl_completion_lab_20260921'
    spec=importlib.util.spec_from_file_location('q2_source_loader',source/'load_data.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    cohorts=module.load_all();events,markets,counts=cohorts['combined']
    with gzip.open(ROOT/'inputs/events.jsonl.gz','wt') as f:
        for r in events:f.write(json.dumps(r,separators=(',',':'))+'\n')
    (ROOT/'inputs/markets.json').write_text(json.dumps(markets,indent=2))
    membership={m['event']:week for week in ['week1','week2'] for m in cohorts[week][1].values()}
    (ROOT/'inputs/week_membership.json').write_text(json.dumps(membership,indent=2))
    source_hashes={str(p.relative_to(source)):hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted((source/'inputs').rglob('*')) if p.is_file()}
    names=['events.jsonl.gz','markets.json','week_membership.json']
    manifest=dict(source=str(source),source_raw_hashes=source_hashes,cohort=counts,
        notes='Q2 loader checked original capture hashes, pagination and payoff identities before normalizing. Full raw captures remain in the delivered Q2 kit.',
        sha256={n:hashlib.sha256((ROOT/'inputs'/n).read_bytes()).hexdigest() for n in names})
    (ROOT/'inputs/manifest.json').write_text(json.dumps(manifest,indent=2))
    print(json.dumps(dict(records=len(events),games=counts['games'],markets=len(markets))))


if __name__=='__main__':main()
