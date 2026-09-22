"""Restartable public GET recorder for a development smoke test or a reviewed prospective panel.

The polling and SQLite watermark logic is adapted from the frozen Q4 collector
at nfl_timing_lab_20260921/collector/record.py. That file still rejects an
unreviewed holdout panel. This process has no credentials and no order routes.
"""
import argparse,fcntl,hashlib,json,math,signal,sqlite3,time
from concurrent.futures import ThreadPoolExecutor,as_completed
from datetime import datetime,timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request,urlopen

from allowlist import allowed_recorder_path as allowed
from panel import validate_panel

BASE='https://api.elections.kalshi.com/trade-api/v2/'


def get(path,params):
    if not allowed(path):raise ValueError('Public data route required')
    attempts=[]
    for _ in range(2):
        started=time.time()
        try:
            with urlopen(Request(BASE+path+'?'+urlencode(params),headers={'User-Agent':'NFLProspectiveRecorder/1.0'}),timeout=20) as r:body=json.load(r)
            return dict(path=path,params=params,request_at=started,received_at=time.time(),attempts=attempts,body=body)
        except Exception as exc:attempts.append(dict(at=started,error=repr(exc),ended_at=time.time()))
    return dict(path=path,params=params,received_at=time.time(),attempts=attempts,error='Bounded request attempts exhausted')


def pages(ticker,start,end):
    rows=[];cursor=None;seen=set()
    for page in range(100):
        params=dict(ticker=ticker,min_ts=start,max_ts=end,limit=1000,is_block_trade='false')
        if cursor:params['cursor']=cursor
        row=get('markets/trades',params);rows.append(dict(kind='trades',ticker=ticker,page=page,**row))
        if row.get('error'):return rows,False
        cursor=row['body'].get('cursor')
        if not cursor:return rows,True
        if cursor in seen:return rows,False
        seen.add(cursor)
    return rows,False


def trade_identity(t):
    yes=float(t['yes_price_dollars']);no=float(t['no_price_dollars']);size=float(t['count_fp'])
    if not math.isfinite(yes+no+size) or abs(yes+no-1)>1e-6 or size<=0 or t['taker_side'] not in ('yes','no'):
        raise ValueError('Invalid public trade')
    return json.dumps(dict(id=t['trade_id'],ticker=t['ticker'],at=t['created_time'],yes=yes,no=no,size=size,
                           taker_side=t['taker_side'],block=bool(t.get('is_block_trade'))),sort_keys=True,separators=(',',':'))


class Store:
    def __init__(self,path,panel_hash):
        path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
        self.lock=path.with_suffix(path.suffix+'.lock').open('a')
        try:fcntl.flock(self.lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError:self.lock.close();raise RuntimeError('Another recorder already owns this database')
        self.db=sqlite3.connect(path)
        self.db.execute('PRAGMA journal_mode=WAL');self.db.execute('PRAGMA synchronous=FULL')
        self.db.executescript('''
          CREATE TABLE IF NOT EXISTS metadata (key TEXT PRIMARY KEY,value TEXT NOT NULL);
          CREATE TABLE IF NOT EXISTS runs (id INTEGER PRIMARY KEY,started REAL NOT NULL,ended REAL,status TEXT NOT NULL);
          CREATE TABLE IF NOT EXISTS responses (id INTEGER PRIMARY KEY,run_id INTEGER,kind TEXT,ticker TEXT,received REAL,committed REAL,ok INTEGER,payload TEXT NOT NULL);
          CREATE TABLE IF NOT EXISTS trades (trade_id TEXT PRIMARY KEY,ticker TEXT,identity TEXT NOT NULL,first_received REAL,first_committed REAL,payload TEXT NOT NULL);
          CREATE TABLE IF NOT EXISTS checkpoints (ticker TEXT PRIMARY KEY,through_ts INTEGER NOT NULL);
          CREATE TABLE IF NOT EXISTS coverage (id INTEGER PRIMARY KEY,run_id INTEGER,ticker TEXT,start_ts INTEGER,end_ts INTEGER,known_at REAL);
          CREATE TABLE IF NOT EXISTS gaps (id INTEGER PRIMARY KEY,started REAL,ended REAL,reason TEXT);
        ''')
        old=self.db.execute("SELECT value FROM metadata WHERE key='panel_sha256'").fetchone()
        if old and old[0]!=panel_hash:self.close();raise ValueError('Panel changed; preserve this collection and start a new database')
        with self.db:self.db.execute("INSERT OR IGNORE INTO metadata VALUES ('panel_sha256',?)",(panel_hash,))
        previous=self.db.execute('SELECT MAX(committed) FROM responses').fetchone()[0]
        now=time.time()
        with self.db:
            self.db.execute("UPDATE runs SET status='interrupted' WHERE status='running'")
            if previous is not None:self.db.execute('INSERT INTO gaps(started,ended,reason) VALUES (?,?,?)',(previous,now,'process restart; books cannot be backfilled'))
            self.run=self.db.execute("INSERT INTO runs(started,status) VALUES (?,'running')",(now,)).lastrowid

    def checkpoint(self,ticker,default):
        row=self.db.execute('SELECT through_ts FROM checkpoints WHERE ticker=?',(ticker,)).fetchone()
        return row[0] if row else default

    def write(self,rows,ticker=None,start=None,end=None,complete=False):
        committed=time.time()
        with self.db:
            for row in rows:
                row=dict(row,recorded_at=committed)
                self.db.execute('INSERT INTO responses(run_id,kind,ticker,received,committed,ok,payload) VALUES (?,?,?,?,?,?,?)',
                    (self.run,row['kind'],row.get('ticker'),row['received_at'],committed,not bool(row.get('error')),json.dumps(row,separators=(',',':'))))
                if row['kind']=='trades' and not row.get('error'):
                    for t in row['body']['trades']:
                        identity=trade_identity(t)
                        old=self.db.execute('SELECT identity FROM trades WHERE trade_id=?',(t['trade_id'],)).fetchone()
                        if old and old[0]!=identity:raise ValueError('Conflicting duplicate trade; transaction rolled back')
                        self.db.execute('INSERT OR IGNORE INTO trades VALUES (?,?,?,?,?,?)',
                            (t['trade_id'],t['ticker'],identity,row['received_at'],committed,json.dumps(t,separators=(',',':'))))
            if complete:
                if not rows or any(r.get('error') for r in rows) or rows[-1]['body'].get('cursor'):
                    raise ValueError('Incomplete pagination cannot advance a watermark')
                indices=[r['page'] for r in rows]
                if indices!=list(range(len(rows))):raise ValueError('Missing trade page')
                self.db.execute('INSERT INTO coverage(run_id,ticker,start_ts,end_ts,known_at) VALUES (?,?,?,?,?)',(self.run,ticker,start,end,committed))
                self.db.execute('INSERT INTO checkpoints(ticker,through_ts) VALUES (?,?) ON CONFLICT(ticker) DO UPDATE SET through_ts=MAX(through_ts,excluded.through_ts)',(ticker,end))

    def finish(self,status='complete'):
        with self.db:self.db.execute('UPDATE runs SET ended=?,status=? WHERE id=?',(time.time(),status,self.run))

    def close(self):
        if hasattr(self,'db'):
            self.db.execute('PRAGMA wal_checkpoint(TRUNCATE)');self.db.close()
        if not self.lock.closed:fcntl.flock(self.lock,fcntl.LOCK_UN);self.lock.close()


def run(panel_path,database,seconds=86400,interval=5):
    if not 10<=seconds<=86400 or interval<1:raise ValueError('Finite session bounds required')
    panel_bytes=Path(panel_path).read_bytes();panel=json.loads(panel_bytes)
    now=datetime.now(timezone.utc)
    database=Path(database)
    games=None if database.exists() else validate_panel(panel,now=now,resuming=False)
    store=Store(database,hashlib.sha256(panel_bytes).hexdigest());stop=[False]
    def stopping(*args):stop[0]=True
    signal.signal(signal.SIGTERM,stopping);signal.signal(signal.SIGINT,stopping)
    tickers={};began=time.time();deadline=time.monotonic()+seconds
    status='complete';next_trade=0;poll=0
    try:
        if games is None:games=validate_panel(panel,now=now,resuming=True)
        for game in games:
            row=get('events/'+game['event'],{'with_nested_markets':'true'})
            store.write([dict(kind='metadata',**row)])
            if row.get('error'):raise RuntimeError('Metadata missing')
            body=row['body'];ms=body.get('markets') or body['event'].get('markets',[])
            if body['event'].get('event_ticker')!=game['event'] or len(ms)!=2 or not body['event'].get('mutually_exclusive') or body['event'].get('collateral_return_type')!='MECNET':
                raise ValueError('Unverified event identity/payoff')
            for m in ms:
                if m.get('price_level_structure')!='linear_cent' or '$0.50' not in m.get('rules_secondary',''):raise ValueError('Unsupported market rules')
                tickers[m['ticker']]=datetime.fromisoformat(game['kickoff']).timestamp()
        with ThreadPoolExecutor(max_workers=8) as pool:
            while time.monotonic()<deadline and not stop[0]:
                cycle=time.monotonic();now_ts=time.time()
                active=[t for t,ko in tickers.items() if ko-604800<=now_ts<ko-10800+300]
                jobs={pool.submit(get,'markets/'+t+'/orderbook',{'depth':10}):('book',t,None,None) for t in active}
                if cycle>=next_trade:
                    for t in active:
                        start=store.checkpoint(t,int(now_ts)-3600)-120;end=int(now_ts)-2
                        jobs[pool.submit(pages,t,start,end)]=('trades',t,start,end)
                    next_trade=cycle+30
                for future in as_completed(jobs):
                    kind,ticker,start,end=jobs[future]
                    if kind=='book':store.write([dict(kind='book',ticker=ticker,poll=poll,**future.result())])
                    else:
                        rows,complete=future.result();store.write([dict(poll=poll,**r) for r in rows],ticker,start,end,complete)
                if poll%6==0:print(json.dumps(dict(poll=poll,elapsed=round(time.time()-began,1),active_markets=len(active))),flush=True)
                poll+=1;time.sleep(max(0,min(interval-(time.monotonic()-cycle),deadline-time.monotonic())))
        if stop[0]:status='stopped_by_signal'
        last=store.db.execute("SELECT MAX(received) FROM responses WHERE run_id=? AND kind='book'",(store.run,)).fetchone()[0]
        if last:
            while time.time()<math.ceil(last)+1:time.sleep(.1)
            for ticker,ko in tickers.items():
                end=min(int(time.time())-1,int(ko-10800+300));start=store.checkpoint(ticker,int(began)-3600)-120
                if end<start:continue
                rows,complete=pages(ticker,start,end);store.write(rows,ticker,start,end,complete)
        store.finish(status)
        print(json.dumps(dict(run_id=store.run,status=status,elapsed=round(time.time()-began,1),database=str(database))),flush=True)
    except Exception:
        store.finish('failed');raise
    finally:store.close()


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--panel',type=Path,required=True);p.add_argument('--database',type=Path,required=True)
    p.add_argument('--seconds',type=int,default=86400);p.add_argument('--interval',type=float,default=5)
    a=p.parse_args();run(a.panel,a.database,a.seconds,a.interval)
