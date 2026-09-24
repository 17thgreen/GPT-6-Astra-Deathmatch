"""Exploratory description of saved receipts; not an economic scorecard."""
import json,collections,datetime,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def main():
    receipts=[json.loads(line) for line in (ROOT/'receipts.jsonl').open()]
    series=json.loads((ROOT/'series.json').read_text())
    perps=json.loads((ROOT/'margin_markets.json').read_text())
    incentives=json.loads((ROOT/'incentive_programs.json').read_text())
    by_series={x['ticker']:x for x in series}
    categories=collections.Counter(c for x in series for c in (x.get('categories') or [x.get('category') or 'Uncategorized']))
    incentive_categories=collections.Counter(by_series.get(x['market_ticker'].split('-')[0],{}).get('category','Unknown') for x in incentives)
    windows=collections.Counter();events={};book_receipts=[]
    for r in receipts:
        if r['status']!=200:continue
        data=json.loads(r['raw'])
        for x in data.get('incentive_programs',[]):
            start=datetime.datetime.fromisoformat(x['start_date'].replace('Z','+00:00')).timestamp()
            end=datetime.datetime.fromisoformat(x['end_date'].replace('Z','+00:00')).timestamp()
            t=r['received_ns']/1e9
            windows['ended' if t>=end else 'not_started' if t<start else 'within_window']+=1
        if '/markets?' in r['url'] and '/margin/' not in r['url']:
            for m in data.get('markets',[]):events[m['ticker']]=m
        if '/orderbook' in r['url']:book_receipts.append(r)
    # Compact book evidence is public GET data only, never authentication headers.
    (ROOT/'public_book_receipts.json').write_text(json.dumps(book_receipts,indent=2)+'\n')
    report={'status':'DISCOVERY_ONLY','scan_completed':(ROOT/'capture/summary.json').exists(),
      'series_count':len(series),'series_category_memberships':dict(categories),
      'perpetual_count':len(perps),'perpetual_statuses':dict(collections.Counter(x.get('status') for x in perps)),
      'incentive_records':len(incentives),'incentive_sample_complete':False,
      'incentive_unique_markets':len({x['market_ticker'] for x in incentives}),
      'incentive_types':dict(collections.Counter(x.get('incentive_type') for x in incentives)),
      'incentive_primary_categories':dict(incentive_categories),'incentive_windows_at_receipt':dict(windows),
      'receipt_count':len(receipts),'http_statuses':dict(collections.Counter(str(x['status']) for x in receipts)),
      'nonempty_open_market_union':len(events),'successful_book_receipts':len(book_receipts),
      'realized_pnl':None,'taker_advantage':None,'order_latency':None,
      'limitations':['lexical access sample, not representative opportunity ranking','incentives capped at five pages','book observations are not fills','demo is not production performance']}
    (ROOT/'ANALYSIS.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
