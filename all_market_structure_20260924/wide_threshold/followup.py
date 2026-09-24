import concurrent.futures as cf,hashlib,json,time,urllib.request,urllib.error,urllib.parse
from pathlib import Path
ROOT=Path(__file__).resolve().parent;BASE='https://api.elections.kalshi.com/trade-api/v2'
TICKERS=['KXMSCOTTON-28JAN31-T800000','KXMSCOTTON-28JAN31-T900000','KXTEENCLOTHADS-26OCT06-T136','KXTEENCLOTHADS-26OCT06-T140']
def get(job):
    name,path,params=job;url=BASE+path+'?'+urllib.parse.urlencode(params);raw=b'';status=None;error=None;sent=time.time_ns()
    try:
        with urllib.request.urlopen(url,timeout=12) as r:status=r.status;raw=r.read()
    except urllib.error.HTTPError as e:status=e.code;raw=e.read();error=type(e).__name__
    except Exception as e:error=type(e).__name__
    rec={'url':url,'sent_ns':sent,'received_ns':time.time_ns(),'status':status,'error':error,'sha256':hashlib.sha256(raw).hexdigest(),'raw':raw.decode(errors='replace')}
    (ROOT/'capture'/f'{name}.json').write_text(json.dumps(rec)+'\n');print(name,status,error,flush=True)
    try:return json.loads(rec['raw']) if status==200 else {}
    except ValueError:return {}
def main():
    (ROOT/'capture').mkdir();jobs=[]
    for t in TICKERS:
        path='/markets/'+t;jobs.extend([(t+'_metadata',path,{}),(t+'_book',path+'/orderbook',{'depth':0})])
    jobs.extend([(s,'/series/'+s,{}) for s in ['KXMSCOTTON','KXTEENCLOTHADS']])
    with cf.ThreadPoolExecutor(max_workers=4) as ex:list(ex.map(get,jobs))
    cursor=None
    for i in range(2):
        params={'status':'active','type':'volume','limit':10000}
        if cursor:params['cursor']=cursor
        d=get((f'volume_{i}','/incentive_programs',params));cursor=d.get('next_cursor')
        if not cursor:break
if __name__=='__main__':main()
