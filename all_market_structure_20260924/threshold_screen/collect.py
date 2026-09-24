"""Public discovery collector. Never sends credentials or order requests."""
import concurrent.futures as cf,json,time,urllib.request,urllib.parse,urllib.error,hashlib,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
BASE='https://api.elections.kalshi.com/trade-api/v2'
def get(path,query=None):
    if path!='/markets' and not (path.startswith('/markets/') and path.endswith('/orderbook')):raise ValueError('GET route refused')
    url=BASE+path+('?' + urllib.parse.urlencode(query) if query else '')
    t=time.time_ns();mono=time.monotonic_ns();raw=b'';status=None;error=None
    try:
        with urllib.request.urlopen(url,timeout=12) as r:status=r.status;raw=r.read()
    except urllib.error.HTTPError as e:status=e.code;raw=e.read();error=type(e).__name__
    except Exception as e:error=type(e).__name__
    return dict(url=url,sent_ns=t,received_ns=time.time_ns(),rtt_ms=(time.monotonic_ns()-mono)/1e6,status=status,error=error,sha256=hashlib.sha256(raw).hexdigest(),raw=raw.decode())
def fetch_metadata(s):
    r=get('/markets',{'series_ticker':s['ticker'],'status':'open','limit':1000})
    (ROOT/'metadata'/f"{s['ticker']}.json").write_text(json.dumps(r)+'\n')
    print(s['ticker'],r['status'],flush=True)
def fetch_book(job):
    round_id,ticker=job
    r=get('/markets/'+urllib.parse.quote(ticker,safe='')+'/orderbook',{'depth':100})
    (ROOT/'books'/f'{round_id}_{ticker}.json').write_text(json.dumps(r)+'\n')
    print(round_id,ticker,r['status'],flush=True)
def main(mode):
    if mode=='metadata':
        (ROOT/'metadata').mkdir()
        with cf.ThreadPoolExecutor(max_workers=4) as ex:list(ex.map(fetch_metadata,json.loads((ROOT/'SERIES_PANEL.json').read_text())))
    elif mode=='books':
        (ROOT/'books').mkdir()
        admitted=json.loads((ROOT/'ADMISSION.json').read_text())['groups']
        for round_id in [1,2]:
            jobs=[(round_id,m['ticker']) for g in admitted for m in g['markets']]
            with cf.ThreadPoolExecutor(max_workers=4) as ex:list(ex.map(fetch_book,jobs))
    else:raise ValueError('mode')
if __name__=='__main__':main(sys.argv[1])
