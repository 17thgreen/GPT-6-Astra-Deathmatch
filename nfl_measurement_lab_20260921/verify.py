"""Artifact integrity, availability-time and censoring checks."""
import gzip
import hashlib
import json
from collections import defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parent


def load(path):return json.loads((ROOT/path).read_text())


def main():
    for name in ['FROZEN_PROTOCOL.json','FROZEN_ANALYSIS.json']:
        for path,digest in load(name)['sha256'].items():
            assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest,path
    for raw,summary in [('inputs/q1_forward_observations.jsonl','inputs/q1_forward_capture_summary.json'),
                        ('forward/observations.jsonl','forward/capture_summary.json')]:
        assert hashlib.sha256((ROOT/raw).read_bytes()).hexdigest()==load(summary)['sha256'],raw
    panels={}
    for panel in ['q1_development','q3_development']:
        features=load(f'results/{panel}_features.json');labels=load(f'results/{panel}_labels.json')
        summary=load(f'results/{panel}_summary.json');lookup={f['join_id']:f for f in features}
        assert len(features)==len(lookup)==len(labels)==summary['shadow_joins']
        grouped=defaultdict(list)
        for label in labels:
            f=lookup[label['join_id']]
            assert f['feature_latest_trade_known_at'] is None or f['feature_latest_trade_known_at']<f['decision_at']
            assert abs(f['arrival_at']-f['decision_at']-.25)<1e-6
            assert 0<=label['serviced_contracts']<=250
            assert abs(label['serviced_contracts']-min(250,max(0,label['exact_price_volume']-f['displayed_depth'])*.5))<1e-7
            for k in ['first_service_at','full_service_at']:
                if label[k] is not None:assert f['arrival_at']<label[k]<=label['end_at']
            if label['horizon_observed']:assert abs(label['end_at']-f['decision_at']-600)<1e-6
            if label['censored_before_full']:assert label['end_reason']!='horizon' and label['full_service_at'] is None
            for m in label['markouts']:
                assert 0<=m['target_lateness']<=30
                assert m['observed_at']>=label['first_service_at']+m['horizon_seconds']
            grouped[(f['ticker'],f['outcome'])].append((f['decision_at'],label['end_at']))
        for intervals in grouped.values():
            intervals.sort()
            for a,b in zip(intervals,intervals[1:]):assert a[1]<=b[0]
        good=[l for l in labels if l['tape_interval_complete']]
        assert summary['full_service_joins']==sum(l['serviced_contracts']>=250 for l in good)
        panels[panel]=dict(joins=len(labels),full_service=summary['full_service_joins'],passed=True)
    weighted=defaultdict(lambda:[0.,0.,0]);count=0
    with gzip.open(ROOT/'results/historical_markout_rows.jsonl.gz','rt') as f:
        for line in f:
            r=json.loads(line);count+=1
            assert r['quote_available_at']<=r['target']
            assert r['quote_asof']>r['fill_at'] and r['target']-r['quote_asof']<=120
            item=weighted[(r['policy'],str(r['horizon_seconds']))]
            item[0]+=r['size'];item[1]+=r['size']*r['midpoint_change_cents'];item[2]+=1
    h=load('results/historical_markout_summary.json')['summaries']
    for (policy,horizon),(volume,numerator,n) in weighted.items():
        assert abs(volume-h[policy][horizon]['covered_contracts'])<1e-7
        assert abs(numerator/volume-h[policy][horizon]['midpoint_change_cents'])<1e-9
        assert n==h[policy][horizon]['observed_markouts']
    registry=load('HOLDOUT_MANIFEST.json')
    excluded=set(registry['development_events']+registry['measurement_development_events'])
    assert len(registry['holdout_games'])==len({g['game_id'] for g in registry['holdout_games']})==32
    assert not excluded.intersection(g['event'] for g in registry['holdout_games'])
    assert load('results/holdout_status.json')['status']=='INSUFFICIENT'
    # Reading every compressed file to EOF also detects truncated members.
    for path in ROOT.rglob('*.gz'):
        with gzip.open(path,'rb') as f:
            while f.read(1024*1024):pass
    result=dict(all_checks_passed=True,panels=panels,historical_markout_rows=count,
                frozen_hashes_verified=True,holdout_completed_games=0,
                note='Internal measurement and artifact checks, not proof of executable fills.')
    (ROOT/'results/verification.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))


if __name__=='__main__':main()
