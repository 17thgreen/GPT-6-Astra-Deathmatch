"""Fill venue event tickers from the public KXNFLGAME events listing.

GET /trade-api/v2/events only, with nested markets off and status open or
unopened. Settled listings are not requested. Nothing in this script places
an order or reads an account.
"""
import argparse,json
from datetime import datetime,timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request,urlopen

from allowlist import allowed_listing
from identity import sanitize_listing_event
from panel import build_panel

BASE='https://api.elections.kalshi.com/trade-api/v2/'
PANEL_VERSION='2026-09-22.1'
COHORT_ID='schedule-only-20260922-after-phi-chi-miss'


def listing_get(path,params,opener=urlopen):
    if not allowed_listing(path,params):
        raise ValueError('Public NFL events listing required')
    request=Request(BASE+path+'?'+urlencode(params),headers={'User-Agent':'NFLProspectiveRecorder/1.0'})
    with opener(request,timeout=30) as response:
        return json.load(response)


def fetch_listings(opener=urlopen):
    rows=[];seen_tickers=set()
    for status in ('open','unopened'):
        cursor=None;seen_cursors=set()
        for _ in range(30):
            params=dict(series_ticker='KXNFLGAME',status=status,limit='200',with_nested_markets='false')
            if cursor:params['cursor']=cursor
            body=listing_get('events',params,opener=opener)
            events=body.get('events') or []
            if not isinstance(events,list):
                raise ValueError('Listing events payload was not a list')
            for raw in events:
                clean=sanitize_listing_event(raw)
                ticker=clean.get('event_ticker')
                if ticker in seen_tickers:continue
                seen_tickers.add(ticker);rows.append(clean)
            cursor=body.get('cursor') or None
            if not cursor or not events:break
            if cursor in seen_cursors:raise ValueError('Listing cursor repeated')
            seen_cursors.add(cursor)
        else:
            raise ValueError('Listing pagination did not finish')
    return rows


def snapshot_document(rows,retrieved_at):
    return dict(
        retrieved_at=retrieved_at.astimezone(timezone.utc).replace(microsecond=0).isoformat(),
        source='GET /trade-api/v2/events?series_ticker=KXNFLGAME&status=open|unopened&with_nested_markets=false',
        retained_fields=['event_ticker','title','sub_title','series_ticker','mutually_exclusive','collateral_return_type','category'],
        note='Identity fields only. Prices, results, and settlements were not retained. This file is not an admission.',
        events=rows,
    )


def write_json(path,document):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(document,indent=2)+'\n')


def main(argv=None):
    parser=argparse.ArgumentParser(description='Resolve KXNFLGAME event tickers from a public listing')
    parser.add_argument('--registry',type=Path,required=True)
    parser.add_argument('--as-of',help='Classification clock. Defaults to listing retrieved_at. Cannot predate that retrieval.')
    parser.add_argument('--snapshot',type=Path,required=True)
    parser.add_argument('--panel',type=Path,required=True)
    parser.add_argument('--live',action='store_true',help='GET the public events listing and write --snapshot')
    args=parser.parse_args(argv)
    registry=json.loads(args.registry.read_text())
    if args.live:
        retrieved=datetime.now(timezone.utc)
        rows=fetch_listings()
        write_json(args.snapshot,snapshot_document(rows,retrieved))
    else:
        document=json.loads(args.snapshot.read_text())
        rows=document['events']
        retrieved=datetime.fromisoformat(document['retrieved_at'])
    as_of=retrieved if args.as_of is None else datetime.fromisoformat(args.as_of)
    if as_of.tzinfo is None:raise SystemExit('as-of must include a timezone offset')
    panel=build_panel(registry,rows,as_of,retrieved,PANEL_VERSION,COHORT_ID)
    write_json(args.panel,panel)
    print(json.dumps(dict(
        panel=str(args.panel),events=len(panel['events']),
        ineligible=len(panel['ineligible_incomplete']),
        unresolved=len(panel['unresolved_identities']),
        admitted_at=panel['admitted_at'],
    ),sort_keys=True))


if __name__=='__main__':
    main()
