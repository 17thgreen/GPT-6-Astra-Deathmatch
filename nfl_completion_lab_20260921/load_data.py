"""Validate and normalize both public-data cohorts without reading game outcomes."""
import gzip,hashlib,json,math
from datetime import datetime,timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parent
def epoch(s):return datetime.fromisoformat(s.replace('Z','+00:00')).timestamp()
def read(path):return json.loads(path.read_text())
def checked(path,digest):
    if hashlib.sha256(path.read_bytes()).hexdigest()!=digest:raise ValueError('Input hash: '+str(path))
def jsonlines(path):
    with gzip.open(path,'rt') as f:
        for line in f:yield json.loads(line)

def load_week(week):
    root=ROOT/'inputs'/week;cohort=read(root/'cohort.json');games={g['event']:g for g in cohort}
    markets={};records=[];candle_records=[]
    if week=='week1':
        cap=read(root/'capture_manifest.json');post=read(root/'postlude_manifest.json');candle=read(root/'candle_manifest.json')
        if cap['failures'] or len(cap['games'])!=16 or len(post['markets'])!=32 or len(candle['markets'])!=32:
            raise ValueError('Incomplete week1')
        for g in cap['games']:checked(root/g['event']/'event.json',g['metadata_sha256'])
        for r in [m for g in cap['games'] for m in g['markets']]+post['markets']:
            if not r['pagination_exhausted']:raise ValueError('Unfinished pagination')
            records.append((root/r['path'].removeprefix('data/'),r['sha256']))
        for r in candle['markets']:
            candle_records.append((r['ticker'],root/r['path'].removeprefix('data/'),r['sha256'],len(r['missing_minutes'])))
    else:
        cap=read(root/'capture_manifest.json')
        if cap['failures'] or len(cap['markets'])!=30:raise ValueError('Incomplete week2')
        for r in cap['markets']:
            checked(root/r['event']/'event.json',r['metadata_sha256'])
            if not r['trades']['pagination_exhausted']:raise ValueError('Unfinished pagination')
            records.append((root/r['trades']['path'],r['trades']['sha256']))
            c=r['candles'];candle_records.append((r['ticker'],root/c['path'],c['sha256'],len(c['missing_minutes'])))
    for event,g in games.items():
        raw=read(root/event/'event.json');meta=raw['event'];ms=raw.get('markets') or meta['markets']
        if len(ms)!=2 or meta.get('collateral_return_type')!='MECNET' or not meta.get('mutually_exclusive'):raise ValueError('Unverified payoff map')
        tickers=sorted(m['ticker'] for m in ms)
        for m in ms:
            if m.get('price_level_structure')!='linear_cent' or '$0.50' not in m.get('rules_secondary',''):raise ValueError('Unverified price/tie rules')
            markets[m['ticker']]=dict(event=event,direction=1 if m['ticker']==tickers[0] else -1,
                                     kickoff=epoch(g['kickoff']),verified_mecnet=True)
    trades=[];quotes=[];ids=set();duplicates=0;missing=0;nulls=0;precuts=0;postcuts=0
    for path,digest in records:
        checked(path,digest)
        for t in jsonlines(path):
            if t['trade_id'] in ids:duplicates+=1;continue
            ids.add(t['trade_id'])
            if t.get('is_block_trade') or t['ticker'] not in markets:raise ValueError('Invalid trade identity')
            yes=float(t['yes_price_dollars']);no=float(t['no_price_dollars']);size=float(t['count_fp'])
            if abs(yes+no-1)>1e-6 or abs(size*100-round(size*100))>1e-5:raise ValueError('Invalid trade precision')
            at=epoch(t['created_time']);ko=markets[t['ticker']]['kickoff']
            if not ko-604800<=at<=ko-10800+300:raise ValueError('Trade outside cohort window')
            if at<ko-10800:precuts+=1
            else:postcuts+=1
            trades.append(dict(at=at,ticker=t['ticker'],taker_side=t['taker_side'],yes_price=yes,size=size,trade_id=t['trade_id']))
    for ticker,path,digest,absent in candle_records:
        checked(path,digest);missing+=absent
        for c in jsonlines(path):
            bid=c.get('yes_bid',{}).get('close_dollars');ask=c.get('yes_ask',{}).get('close_dollars')
            if bid is None or ask is None:nulls+=1;continue
            quotes.append(dict(at=c['end_period_ts']+60,asof=c['end_period_ts'],ticker=ticker,
                               bid=float(bid),ask=float(ask),kind='quote'))
    events=trades+quotes;events.sort(key=lambda r:(r['at'],0 if r.get('kind')=='quote' else 1,r.get('trade_id',r['ticker'])))
    summary=dict(cohort=week,games=len(games),markets=len(markets),trades=len(trades),precutoff_trades=precuts,
                 postlude_trades=postcuts,duplicate_trades=duplicates,quotes=len(quotes),missing_candle_minutes=missing,
                 null_candle_prices=nulls,start=events[0]['at'],end=events[-1]['at'])
    return events,markets,summary

def load_all():
    a,ma,sa=load_week('week1');b,mb,sb=load_week('week2')
    if ma.keys() & mb.keys():raise ValueError('Cohorts overlap by market')
    combined=a+b;combined.sort(key=lambda r:(r['at'],0 if r.get('kind')=='quote' else 1,r.get('trade_id',r['ticker'])))
    return {'week1':(a,ma,sa),'week2':(b,mb,sb),
            'combined':(combined,{**ma,**mb},dict(cohort='combined',games=31,markets=62,
                trades=sa['trades']+sb['trades'],quotes=sa['quotes']+sb['quotes'],bankroll_note='ONE shared $5,000 account; overlapping windows run chronologically.'))}
