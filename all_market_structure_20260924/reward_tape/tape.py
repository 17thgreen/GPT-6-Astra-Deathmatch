"""Read and classify historical public prints; never infer hypothetical fills."""
import concurrent.futures as cf,hashlib,json,time,urllib.request,urllib.error,urllib.parse
from decimal import Decimal as D
from datetime import datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parent
BASE='https://api.elections.kalshi.com/trade-api/v2/markets/trades'
def stamp(s):return datetime.fromisoformat(s.replace('Z','+00:00')).timestamp()

def compatible(trade,quote_side):
    if trade.get('is_block_trade'):return False
    side=trade.get('taker_outcome_side',trade.get('taker_side'))
    if side not in ('yes','no'):return None
    if trade.get('taker_side') and trade['taker_side']!=side:return None
    book=trade.get('taker_book_side')
    if book and book!=('bid' if side=='yes' else 'ask'):return None
    try:
        yes=D(trade['yes_price_dollars']);no=D(trade['no_price_dollars'])
        if yes+no!=1 or not 0<yes<1:return None
        price=yes if quote_side=='yes' else no
    except (KeyError,ValueError):return None
    return side!=quote_side and price<=D('.01')

def fetch(row):
    t=row['ticker'];cursor=None;trades={};complete=False
    for page in range(2):
        params={'ticker':t,'limit':1000}
        if cursor:params['cursor']=cursor
        url=BASE+'?'+urllib.parse.urlencode(params);raw=b'';status=None;error=None;sent=time.time_ns()
        try:
            with urllib.request.urlopen(url,timeout=12) as r:status=r.status;raw=r.read()
        except urllib.error.HTTPError as e:status=e.code;raw=e.read();error=type(e).__name__
        except Exception as e:error=type(e).__name__
        rec={'url':url,'sent_ns':sent,'received_ns':time.time_ns(),'status':status,'error':error,'sha256':hashlib.sha256(raw).hexdigest(),'raw':raw.decode(errors='replace')}
        (ROOT/'capture'/f'{t}_{page}.json').write_text(json.dumps(rec)+'\n')
        print(t,page,status,error,flush=True)
        try:data=json.loads(rec['raw']) if status==200 else {}
        except ValueError:data={}
        if not isinstance(data,dict) or not isinstance(data.get('trades'),list):break
        for x in data['trades']:
            if x.get('ticker')!=t:raise ValueError('wrong ticker')
            trades[x['trade_id']]=x
        cursor=data.get('cursor');complete=not bool(cursor)
        if complete:break
    p=row['program'];detail=[]
    for trade in sorted(trades.values(),key=lambda x:x['created_time']):
        ts=stamp(trade['created_time']);count=D(trade['count_fp'])
        assert count>=0
        detail.append({'trade':trade,'within_program':stamp(p['start_date'])<=ts<stamp(p['end_date']),
                       'direction_price_compatible_with_quote':compatible(trade,row['quote']['side'])})
    return {'ticker':t,'complete_returned_pagination':complete,'cursor_remaining':bool(cursor),'prints':len(detail),
            'contracts':str(sum((D(x['trade']['count_fp']) for x in detail),D(0))),
            'within_program_contracts':str(sum((D(x['trade']['count_fp']) for x in detail if x['within_program']),D(0))),
            'compatible_within_program_contracts':str(sum((D(x['trade']['count_fp']) for x in detail if x['within_program'] and x['direction_price_compatible_with_quote'] is True),D(0))),
            'detail':detail}

def main():
    (ROOT/'capture').mkdir();panel=json.loads((ROOT/'PANEL.json').read_text());start=time.monotonic();rows=[]
    with cf.ThreadPoolExecutor(max_workers=4) as ex:
        for i in range(0,len(panel['rows']),4):
            if time.monotonic()-start>=120:break
            rows.extend(ex.map(fetch,panel['rows'][i:i+4]))
    out={'rows':rows,'selected':len(panel['rows']),'elapsed_seconds':time.monotonic()-start,'hypothetical_fills':None,'pnl':None}
    (ROOT/'RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
    for row in rows:print(json.dumps({k:v for k,v in row.items() if k!='detail'}))

if __name__=='__main__':main()
