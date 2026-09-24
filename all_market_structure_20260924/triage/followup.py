import concurrent.futures as cf,json,time,urllib.request,urllib.error,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parent
K='https://api.elections.kalshi.com/trade-api/v2'
T='KXAAAGASDFL-26SEP24-4.4400'
def get(job):
    name,url=job;raw=b'';status=None;error=None;wall=time.time_ns();mono=time.monotonic_ns()
    if not (url.startswith(K+'/') or url.startswith('https://api.kraken.com/0/public/Depth?')):raise ValueError('route')
    try:
        with urllib.request.urlopen(url,timeout=12) as r:status=r.status;raw=r.read()
    except urllib.error.HTTPError as e:status=e.code;raw=e.read();error=type(e).__name__
    except Exception as e:error=type(e).__name__
    rec=dict(url=url,sent_ns=wall,sent_monotonic_ns=mono,received_ns=time.time_ns(),received_monotonic_ns=time.monotonic_ns(),status=status,error=error,sha256=hashlib.sha256(raw).hexdigest(),raw=raw.decode(errors='replace'))
    (ROOT/'followup_capture'/f'{name}.json').write_text(json.dumps(rec)+'\n');print(name,status,error,flush=True)
def main():
    (ROOT/'followup_capture').mkdir()
    for rnd in [1,2]:
        jobs=[(f'{rnd}_margin',K+'/margin/markets'),(f'{rnd}_gap_book',K+'/markets/'+T+'/orderbook?depth=0'),(f'{rnd}_gap_metadata',K+'/markets/'+T)]
        for asset,pair in [('BTC','XBTUSD'),('ETH','ETHUSD'),('SOL','SOLUSD')]:
            jobs.extend([(f'{rnd}_{asset}_kalshi',K+'/margin/markets/KX'+asset+'PERP/orderbook?depth=100'),(f'{rnd}_{asset}_kraken','https://api.kraken.com/0/public/Depth?pair='+pair+'&count=100')])
        with cf.ThreadPoolExecutor(max_workers=4) as ex:list(ex.map(get,jobs))
if __name__=='__main__':main()
