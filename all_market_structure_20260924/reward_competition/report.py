"""Reproduce fresh and explicitly reused scoring; never create virtual fills."""
import collections,datetime,hashlib,json,zipfile
from pathlib import Path
from model import analyze,admitted
ROOT=Path(__file__).resolve().parent
INPUTS={}

def read(p):
    INPUTS[str(p.relative_to(ROOT.parent))]=hashlib.sha256(p.read_bytes()).hexdigest()
    return json.loads(p.read_text())

def receipt(p):
    r=read(p);assert hashlib.sha256(r['raw'].encode()).hexdigest()==r['sha256'],p
    return json.loads(r['raw']) if r['status']==200 else {},r

def replay_census():
    base=ROOT.parent/'reward_census';panel=read(base/'PANEL.json');books={};meta={};times={}
    for p in sorted((base/'capture').glob('books_*.json')):
        data,r=receipt(p)
        for b in data.get('orderbooks',[]):books[b['ticker']]=b.get('orderbook_fp');times[b['ticker']]=r['received_ns']
    for p in sorted((base/'capture').glob('metadata_*.json')):
        data,r=receipt(p)
        for m in data.get('markets',[]):meta[m['ticker']]=m
    rows=[]
    for p in panel['programs']:
        t=p['market_ticker'];ns=times.get(t)
        if ns is not None and admitted(p,ns/1e9):rows.append(analyze(t,p,meta.get(t),books.get(t),ns))
    return {'source':'AMS-005 reused development census','rows':rows}

def replay_watch():
    base=ROOT.parent/'reward_replication';out=[]
    for f in sorted(base.glob('FRAME_*.json')):
        frame=read(f);cycle=frame['cycle'];bookfile=base/'capture'/f'{cycle:02d}_books.json'
        if not bookfile.exists():continue
        data,r=receipt(bookfile);ns=r['received_ns'];books={b['ticker']:b.get('orderbook_fp') for b in data.get('orderbooks',[])}
        data,_=receipt(base/'capture'/f'{cycle:02d}_metadata.json');meta={m['ticker']:m for m in data.get('markets',[])}
        rows=[analyze(x['ticker'],x['program'],meta.get(x['ticker']),books.get(x['ticker']),ns) for x in frame['rows'] if admitted(x['program'],ns/1e9)]
        out.append({'source':'AMS-007 reused development snapshot','cycle':cycle,'rows':rows})
    cat,r=receipt(base/'capture/11_catalog_0.json');eligible=[p for p in cat.get('incentive_programs',[]) if admitted(p,r['received_ns']/1e9)]
    inventory={'received_ns':r['received_ns'],'eligible_programs':len(eligible),'series':dict(collections.Counter(p['market_ticker'].split('-')[0] for p in eligible)),'cursor_remaining':bool(cat.get('next_cursor'))}
    return out,inventory

def compact(frame):
    rows=frame['rows'];candidates=[]
    for r in rows:
        if r['class']!='resting_completion':continue
        plans=[]
        for p in r['plans']:
            cases={s['kind']:{'available':s['available'],**({'competitor_principal':s['competitor_principal'],'shares':{m:x['overall_share'] for m,x in s['scores'].items()},'capped_remaining':s['scores']['capped']['remaining_gross'],'half_uptime_covers_principal_and_stress':s['scores']['capped']['half_uptime_covers_principal_and_stress']} if s['available'] else {})} for s in p['scenarios']}
            plans.append({k:p[k] for k in ('buffer_fraction','quantity','principal','fee_stress_reserve')}|{'cases':cases})
        candidates.append({k:r[k] for k in ('ticker','event_ticker','book_received_ns','depth','short_sides','remaining_hours')}|{'program_id':r['program']['id'],'pool_dollars':r['pool_dollars'],'plans':plans})
    return {'cycle':frame.get('cycle'),'source':frame.get('source','AMS-009 fresh acquisition'),'counts':dict(collections.Counter(r['class'] for r in rows)),'candidates':candidates}

def main():
    frozen=read(ROOT/'FREEZE.json')
    for f,h in frozen['sha256'].items():assert hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==h,f
    fresh=[];selections=[];statuses=[]
    for f in sorted((ROOT/'capture').glob('*.json')):
        _,r=receipt(f);statuses.append(str(r['status']))
    for f in sorted(ROOT.glob('FRAME_*.json')):
        d=read(f);s=read(ROOT/f"SELECTION_{d['cycle']}.json");selections.append({k:v for k,v in s.items() if k!='programs'})
        for r in d['rows']:
            if r['book_received_ns']:assert s['selected_before_books_ns']<r['book_received_ns']
        fresh.append(d)
    reused=[replay_census()];watch,inventory=replay_watch();reused+=watch
    replay={'designation':'reused development evidence; not fresh or independent holdout','frames':reused,'last_AMS007_catalog_inventory':inventory}
    (ROOT/'REPLAY.json').write_text(json.dumps(replay,indent=2)+'\n')
    short={'fresh':[compact(f) for f in fresh],'reused':[compact(f) for f in reused],'run':read(ROOT/'RUN.json'),'fresh_selections':selections,'fresh_http_statuses':dict(collections.Counter(statuses)),'last_AMS007_catalog_inventory':inventory,'realized_pnl':None}
    (ROOT/'SUMMARY.json').write_text(json.dumps(short,indent=2)+'\n')
    (ROOT/'INPUT_HASHES.json').write_text(json.dumps(INPUTS,indent=2)+'\n')
    print(json.dumps({'run':short['run'],'fresh_http_statuses':short['fresh_http_statuses'],'fresh':[{k:v for k,v in compact(f).items() if k!='candidates'} for f in fresh],'reused':[{k:v for k,v in compact(f).items() if k!='candidates'} for f in reused],'catalog_inventory':inventory},indent=2))

def archive():
    paths=sorted((ROOT/'capture').glob('*.json'))+sorted(ROOT.glob('FRAME_*.json'))+sorted(ROOT.glob('SELECTION_*.json'))+[ROOT/x for x in ('RUN.json','REPLAY.json','INPUT_HASHES.json','SUMMARY.json','TOP_LEVEL_STRESS.json')]
    hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    (ROOT/'EVIDENCE_HASHES.json').write_text(json.dumps(hashes,indent=2)+'\n')
    dest=ROOT.parents[2]/'artifacts'/'AMS_009_Raw_Evidence.zip'
    with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in paths+[ROOT/'EVIDENCE_HASHES.json']:z.write(p,str(p.relative_to(ROOT)))
    with zipfile.ZipFile(dest) as z:assert z.testzip() is None
    a={'filename':dest.name,'bytes':dest.stat().st_size,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'dependencies':'Replay requires the separately retained AMS-005 and AMS-007 raw artifacts restored into their original experiment directories.'}
    (ROOT/'ARCHIVE.json').write_text(json.dumps(a,indent=2)+'\n');print(json.dumps(a))

if __name__=='__main__':main();archive()
