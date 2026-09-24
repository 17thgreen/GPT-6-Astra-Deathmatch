"""Summarize sampled opportunities; no reward accrual or virtual execution."""
import collections,datetime,hashlib,importlib.util,json,zipfile
from decimal import Decimal as D
from pathlib import Path
ROOT=Path(__file__).resolve().parent
_s=importlib.util.spec_from_file_location('ams006_tape',ROOT.parent/'reward_tape/tape.py')
tape=importlib.util.module_from_spec(_s);_s.loader.exec_module(tape)

def read(p):return json.loads(p.read_text())
def utc(ns):return datetime.datetime.fromtimestamp(ns/1e9,datetime.timezone.utc).isoformat()

def main():
    run=read(ROOT/'RUN.json');freeze=read(ROOT/'FREEZE.json')
    for f,h in freeze['sha256'].items():assert hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==h,f
    receipts=[]
    for f in sorted((ROOT/'capture').glob('*.json')):
        r=read(f);assert hashlib.sha256(r['raw'].encode()).hexdigest()==r['sha256'],f;receipts.append(r)
    frames=[read(p) for p in sorted(ROOT.glob('FRAME_*.json'))];panels=[read(p) for p in sorted(ROOT.glob('SELECTION_*.json'))]
    assert [f['cycle'] for f in frames]==run['cycles']
    for f,p in zip(frames,panels):
        assert f['cycle']==p['cycle']
        for r in f['rows']:
            if r['book_received_ns']:assert p['selected_before_books_ns']<r['book_received_ns']
    alerts=read(ROOT/'FIRST_ALERTS.json');trades={p['ticker']:p for p in read(ROOT/'TRADES.json')};candidates=[]
    for t,first in alerts.items():
        r=first['row'];observations=[x for f in frames if f['cycle']>=first['cycle'] for x in f['rows'] if x['ticker']==t]
        available=[x for x in observations if x['book_received_ns']]
        last=available[-1] if available else r
        plan=r['plans'][1];tp=trades.get(t);prints={};usable=tp is not None
        if tp:
            for page in tp['pages']:
                xs=page['data'].get('trades');usable=usable and isinstance(xs,list)
                for x in xs or []:
                    assert x['ticker']==t;prints[x['trade_id']]=x
        after=[x for x in prints.values() if r['book_received_ns']/1e9<=tape.stamp(x['created_time'])<tape.stamp(r['program']['end_date'])]
        compatible={s:sum((D(x['count_fp']) for x in after if tape.compatible(x,s) is True),D(0)) for s in r['short_sides']}
        unknown={s:sum(tape.compatible(x,s) is None for x in after) for s in r['short_sides']}
        candidates.append({'ticker':t,'event_ticker':r['event_ticker'],'program_id':r['program']['id'],'pool_dollars':r['program']['period_reward']/10000,
            'first_alert_cycle':first['cycle'],'first_alert_utc':utc(r['book_received_ns']),'first_age_minutes':r['age_minutes'],'first_remaining_minutes':r['remaining_minutes'],
            'initial_quantity':plan['quantity'],'initial_principal':plan['principal'],'initial_fee_stress_reserve':plan['fee_stress_reserve'],'initial_conditional_reward':plan['conservative_half_uptime_reward'],'initial_conditional_cushion':plan['conditional_cushion'],
            'observations_from_first_alert':len(observations),'usable_books_from_first_alert':len(available),'recomputed_candidate_passes':sum(x['buffered_alert'] for x in observations),
            'sampled_span_minutes':(last['book_received_ns']-r['book_received_ns'])/6e10,'last_observed_utc':utc(last['book_received_ns']),'last_class':last['class'],
            'last_recomputed_buffered_pass':last['buffered_alert'],'last_recomputed_cushion':last.get('plans',[{},{}])[1].get('conditional_cushion') if len(last.get('plans',[]))>1 else None,
            'quote_quantity_changes':sum(x['plans'][1]['quantity']!=plan['quantity'] for x in observations if len(x.get('plans',[]))>1),
            'public_trade_pages_usable':usable,'public_trade_cursor_remaining':tp['cursor_remaining'] if tp else None,'returned_public_trades':len(prints),'public_trades_after_alert':len(after),
            'price_direction_compatible_contracts_after_alert':{s:str(q) for s,q in compatible.items()},'unclassified_trades_after_alert':unknown})
    unique={p['market_ticker']:p for panel in panels for p in panel['programs']}
    cycles=[{'cycle':f['cycle'],'catalog_ok':p['catalog_ok'],'selected':len(p['programs']),'active':len(p['active_tickers']),'buffered_alerts':len(f['ranked_alerts']),'classes':dict(collections.Counter(r['class'] for r in f['rows']))} for f,p in zip(frames,panels)]
    summary={'run':run,'http_statuses':dict(collections.Counter(str(r['status']) for r in receipts)),'catalog_failed_cycles':sum(not p['catalog_ok'] for p in panels),'catalog_cursor_cycles':sum(p['catalog_cursor_remaining'] for p in panels),'selection_cap_cycles':sum(p['selection_cap_applied'] for p in panels),
        'selected_unique_programs':len(unique),'selected_series':dict(collections.Counter(t.split('-')[0] for t in unique)),'program_terms_changed_observations':sum(r['program_terms_changed'] for f in frames for r in f['rows']),
        'cycles':cycles,'alert_markets':len(candidates),'alert_events':len(set(r['event_ticker'] for r in candidates)),'event_groups':dict(collections.Counter(r['event_ticker'] for r in candidates)),
        'candidates':candidates,'no_fill_or_reward_income_inferred':True,'realized_pnl':None}
    (ROOT/'SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
    deps={'../reward_tape/tape.py':hashlib.sha256((ROOT.parent/'reward_tape/tape.py').read_bytes()).hexdigest()}
    (ROOT/'REPORT_DEPENDENCIES.json').write_text(json.dumps(deps,indent=2)+'\n')
    print(json.dumps(summary,indent=2))

def archive():
    paths=sorted((ROOT/'capture').glob('*.json'))+sorted(ROOT.glob('FRAME_*.json'))+sorted(ROOT.glob('SELECTION_*.json'))+[ROOT/p for p in ('FIRST_ALERTS.json','TRADES.json','RUN.json')]
    hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    (ROOT/'EVIDENCE_HASHES.json').write_text(json.dumps(hashes,indent=2)+'\n')
    dest=ROOT.parents[2]/'artifacts'/'AMS_010_Raw_Evidence.zip'
    with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in paths+[ROOT/'EVIDENCE_HASHES.json']:z.write(p,str(p.relative_to(ROOT)))
    with zipfile.ZipFile(dest) as z:assert z.testzip() is None
    a={'filename':dest.name,'bytes':dest.stat().st_size,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'restoration':'Extract into reward_scanner. Scoring imports reward_competition/model.py and trade classification imports reward_tape/tape.py from the same research branch.'}
    (ROOT/'ARCHIVE.json').write_text(json.dumps(a,indent=2)+'\n');print(json.dumps(a))

if __name__=='__main__':main();archive()
