"""EXT-K1 structural (label-free, PnL-free) verification. Counts only.
Reads: 000 fills ledger, 000 summary json, dev tape events, markets.json, nflverse games.csv.
Never reads scores/results/moneylines for any computation other than join presence."""
import gzip, json, csv, hashlib, collections, datetime as dt, sys
LAB='/workspace/lab/astra-science/nfl_factorial_lab_20260921'
GAMES='/workspace/lab/governance/astra/packets/scout_external_hunt_2026-10-03/raw/nflverse_nfldata_games.csv'
ADMIT1=(dt.datetime(2026,9,27,0,0,tzinfo=dt.timezone.utc).timestamp(), dt.datetime(2026,9,30,4,0,tzinfo=dt.timezone.utc).timestamp())
def sha(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()
out={}
markets=json.load(open(f'{LAB}/inputs/markets.json'))
summary=json.load(open(f'{LAB}/results/q3300_d0.25_000.json'))
# fills
fills=[json.loads(l) for l in gzip.open(f'{LAB}/results/q3300_d0.25_000_fills.jsonl.gz','rt')]
keys=collections.Counter(k for f in fills for k in f)
by=collections.defaultdict(float); n_by=collections.Counter()
for f in fills: by[(f['kind'],f['outcome'])]+=f['size']; n_by[(f['kind'],f['outcome'])]+=1
maker=sum(v for (k,o),v in by.items() if k=='maker')
out['fills']=dict(rows=len(fills),keys=dict(keys),contracts_by_kind_outcome={f'{k}/{o}':round(v,2) for (k,o),v in sorted(by.items())},
  rows_by_kind_outcome={f'{k}/{o}':v for (k,o),v in sorted(n_by.items())},maker_contracts=round(maker,2),
  maker_no_share=by[('maker','no')]/maker, taker_contracts=round(sum(v for (k,o),v in by.items() if k=='taker'),2),
  sorted_by_at=all(fills[i]['at']<=fills[i+1]['at'] for i in range(len(fills)-1)),
  events=len({f['event'] for f in fills}), at_min=min(f['at'] for f in fills), at_max=max(f['at'] for f in fills),
  in_admit1=sum(ADMIT1[0]<=f['at']<ADMIT1[1] for f in fills),
  maker_fills_at_or_after_cutoff=sum(f['kind']=='maker' and f['at']>=markets[f['ticker']]['kickoff']-10800 for f in fills),
  distinct_order_ids=len({f['order_id'] for f in fills if f['kind']=='maker'}))
# unhedged contract-hours: integral of |event net inventory| dt, end=min(coverage_end, K-3h)
coverage_end=max(m['kickoff']-10800 for m in markets.values())+300
area=collections.defaultdict(float); last={}
for f in fills:
    e=f['event']
    if e in last: area[e]+=abs(last[e][1])*(f['at']-last[e][0])
    last[e]=(f['at'],f['inventory_after'])
for e,(at,inv) in last.items():
    k=markets[[t for t in markets if markets[t]['event']==e][0]]['kickoff']
    area[e]+=abs(inv)*max(0,min(coverage_end,k-10800)-at)
uch=sum(area.values())/3600
# FIFO lot reconstruction (per event, direction-signed) -> lot-hours must equal uch
lots=collections.defaultdict(collections.deque); lot_area=0.0; open_end=0.0; n_open_lots=0; closes_by_kind=collections.defaultdict(float)
for f in fills:
    e=f['event']; d=f['direction']; q=f['size']; L=lots[e]
    while q>1e-8 and L and L[0][0]!=d:
        lot=L[0]; p=min(q,lot[1]); lot_area+=p*(f['at']-lot[2]); closes_by_kind[f['kind']]+=p; q-=p; lot[1]-=p
        if lot[1]<1e-8: L.popleft()
    if q>1e-8: L.append([d,q,f['at']]); n_open_lots+=1
residual=sum(l[1] for L in lots.values() for l in L)
out['unhedged']=dict(recomputed_contract_hours=uch, ledger_contract_hours=summary['unhedged_contract_hours'],
  abs_diff=abs(uch-summary['unhedged_contract_hours']), fifo_lot_contract_hours=lot_area/3600, opening_lots=n_open_lots,
  contracts_closed_by_kind={k:round(v,2) for k,v in closes_by_kind.items()}, residual_open_contracts_at_end=residual,
  coverage_end=coverage_end, all_flat=summary['all_flat'], passive_pairing_fraction=summary['passive_pairing_fraction'])
# dev tape
tr=collections.Counter(); trc=collections.defaultdict(float); q=0; tick=set(); kinds=collections.Counter(); tkeys=collections.Counter(); qkeys=collections.Counter()
amin=1e20; amax=0; inadm=0; last_row=collections.defaultdict(float); block=0
for l in gzip.open(f'{LAB}/inputs/events.jsonl.gz','rt'):
    r=json.loads(l); tick.add(r['ticker']); a=r['at']; amin=min(amin,a); amax=max(amax,a); last_row[r['ticker']]=max(last_row[r['ticker']],a)
    if ADMIT1[0]<=a<ADMIT1[1]: inadm+=1
    if r.get('kind')=='quote': q+=1; qkeys.update(r.keys())
    else:
        tr[r['taker_side']]+=1; trc[r['taker_side']]+=r['size']; tkeys.update(r.keys()); block+=bool(r.get('is_block_trade',False))
tot=sum(trc.values())
lead=[ (markets[t]['kickoff']-last_row[t])/60 for t in tick]
out['tape']=dict(trades=sum(tr.values()),quotes=q,rows=sum(tr.values())+q,tickers=len(tick),events=len({markets[t]['event'] for t in tick}),
  trades_by_taker_side=dict(tr),contracts_by_taker_side={k:round(v,2) for k,v in trc.items()},taker_yes_contract_share=trc['yes']/tot,
  taker_yes_trade_share=tr['yes']/sum(tr.values()), trade_keys=dict(tkeys), quote_keys=dict(qkeys), block_trades=block,
  at_min_utc=dt.datetime.fromtimestamp(amin,dt.timezone.utc).isoformat(), at_max_utc=dt.datetime.fromtimestamp(amax,dt.timezone.utc).isoformat(),
  rows_in_admit1_window=inadm, last_row_minutes_before_kickoff_min=min(lead), last_row_minutes_before_kickoff_max=max(lead))
# join
ALIAS={'JAC':'JAX','LAR':'LA'}
games=list(csv.DictReader(open(GAMES)))
ET=dt.timezone(dt.timedelta(hours=-4))
evs=collections.defaultdict(list)
for t,m in markets.items(): evs[m['event']].append(t.split('-')[-1])
rows=[]; exact=0
for e,teams in sorted(evs.items()):
    k=[markets[t]['kickoff'] for t in markets if markets[t]['event']==e][0]
    kd=dt.datetime.fromtimestamp(k,ET)
    code=e.split('-')[1]; tdate=code[:7]
    mapped={ALIAS.get(x,x) for x in teams}
    cand=[g for g in games if g['season']=='2026' and g['game_type']=='REG' and g['gameday']==kd.strftime('%Y-%m-%d') and {g['home_team'],g['away_team']}==mapped]
    raw=[g for g in games if g['season']=='2026' and g['gameday']==kd.strftime('%Y-%m-%d') and {g['home_team'],g['away_team']}==set(teams)]
    exact+=len(raw)==1
    g=cand[0] if len(cand)==1 else None
    ok_time = g is not None and g['gametime']==kd.strftime('%H:%M')
    ok_tdate = kd.strftime('%y%b%d').upper()==tdate
    rows.append(dict(event=e,teams=sorted(teams),n_candidates=len(cand),game_id=g['game_id'] if g else None,kickoff_matches_gametime_et=ok_time,ticker_date_matches=ok_tdate,
      has_both_moneylines=bool(g and g['away_moneyline'] and g['home_moneyline']), aliases_used=sorted(x for x in teams if x in ALIAS)))
out['join']=dict(joined=sum(r['n_candidates']==1 for r in rows),events=len(rows),exact_without_alias=exact,
  alias_events={r['event']:r['aliases_used'] for r in rows if r['aliases_used']},all_kickoff_time_match=all(r['kickoff_matches_gametime_et'] for r in rows),
  all_ticker_date_match=all(r['ticker_date_matches'] for r in rows), all_have_both_ml=all(r['has_both_moneylines'] for r in rows),
  game_ids=[r['game_id'] for r in rows], rows=rows,
  nflverse_rows=len(games), nflverse_columns=list(games[0].keys()), nflverse_2026_rows=sum(g['season']=='2026' for g in games),
  nflverse_2026_w1w2=sum(g['season']=='2026' and g['week'] in('1','2') for g in games))
# substring-style join (to explain Scout's '29 exact')
sub=0
for e,teams in evs.items():
    code=e.split('-')[1][7:]
    k=[markets[t]['kickoff'] for t in markets if markets[t]['event']==e][0]; d=dt.datetime.fromtimestamp(k,ET).strftime('%Y-%m-%d')
    sub+=any(g['season']=='2026' and g['gameday']==d and code.startswith(g['away_team']) and code.endswith(g['home_team']) for g in games) or any(g['season']=='2026' and g['gameday']==d and code.startswith(g['away_team']) and g['home_team'] in code[len(g['away_team']):] for g in games)
out['join']['substring_style_matches_no_alias']=sub
json.dump(out,open('/workspace/ext_k1_scratch/structural_verify_out.json','w'),indent=1,default=str)
s={k:(v if k!='join' else {kk:vv for kk,vv in v.items() if kk not in('rows','nflverse_columns')}) for k,v in out.items()}
print(json.dumps(s,indent=1,default=str))
