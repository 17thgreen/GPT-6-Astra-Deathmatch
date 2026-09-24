"""Bounded credential-free GET observations across two independent venues."""
import concurrent.futures as cf,json,time,urllib.request,urllib.error,urllib.parse,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parent
K='https://api.elections.kalshi.com/trade-api/v2'
C='https://api.exchange.coinbase.com/products/'
def get(job):
    name,url=job
    if not (url.startswith(K+'/markets/') or url.startswith(K+'/margin/markets') or url.startswith(C)):raise ValueError('route')
    wall=time.time_ns();mono=time.monotonic_ns();raw=b'';status=None;error=None
    try:
        with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'AMS-003-public-research'}),timeout=12) as r:status=r.status;raw=r.read()
    except urllib.error.HTTPError as e:status=e.code;raw=e.read();error=type(e).__name__
    except Exception as e:error=type(e).__name__
    rec={'url':url,'sent_ns':wall,'sent_monotonic_ns':mono,'received_ns':time.time_ns(),'received_monotonic_ns':time.monotonic_ns(),'status':status,'error':error,'sha256':hashlib.sha256(raw).hexdigest(),'raw':raw.decode(errors='replace')}
    (ROOT/'capture'/f'{name}.json').write_text(json.dumps(rec)+'\n')
    print(name,status,error,flush=True)
def batch(jobs):
    with cf.ThreadPoolExecutor(max_workers=4) as ex:list(ex.map(get,jobs))
def main():
    (ROOT/'capture').mkdir()
    panel=json.loads((ROOT/'PANEL.json').read_text())
    for rnd in [1,2,3]:
        jobs=[(f'{rnd}_margin',K+'/margin/markets')]
        for asset,ticker in panel['perps'].items():
            jobs.extend([(f'{rnd}_{asset}_kalshi',K+'/margin/markets/'+ticker+'/orderbook?depth=100'),(f'{rnd}_{asset}_coinbase',C+asset+'-USD/book?level=2')])
        batch(jobs)
    jobs=[]
    for x in panel['programs']:
        t=x['market_ticker'];u=K+'/markets/'+urllib.parse.quote(t,safe='')
        jobs.extend([(t+'_metadata',u),(t+'_book',u+'/orderbook?depth=0')])
    batch(jobs)
if __name__=='__main__':main()
