"""Panel validation, public-GET allowlists, and no-backfill admission."""
import importlib.util,json,tempfile,unittest
from datetime import datetime,timezone
from pathlib import Path
from urllib.parse import parse_qs,urlparse

import admit,allowlist,identity,panel,record,resolve_event_tickers

ROOT=Path(__file__).resolve().parent
REGISTRY=ROOT.parent/'nfl_factorial_lab_20260921'/'RESERVED_HOLDOUT.json'
Q4=ROOT.parent/'nfl_timing_lab_20260921'/'collector'/'record.py'
AS_OF=datetime(2026,9,22,21,0,tzinfo=timezone.utc)
PIT_START=datetime(2026,9,25,0,15,tzinfo=timezone.utc)


def load_q4():
    spec=importlib.util.spec_from_file_location('q4_recorder',Q4)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


def tiny_registry():
    return dict(
        development_events=['KXNFLGAME-26SEP21NYGLAR'],
        measurement_development_events=['KXNFLGAME-26SEP24ATLGB'],
        holdout_games=[
            dict(game_id='2026_03_PHI_CHI',kickoff='2026-09-29T00:15:00+00:00',away='PHI',home='CHI',event='KXNFLGAME-26SEP28PHICHI'),
            dict(game_id='2026_04_PIT_CLE',kickoff='2026-10-02T00:15:00+00:00',away='PIT',home='CLE',event=None),
            dict(game_id='2026_04_JAX_CIN',kickoff='2026-10-04T17:00:00+00:00',away='JAX',home='CIN',event=None),
            dict(game_id='2026_04_LA_PHI',kickoff='2026-10-04T17:00:00+00:00',away='LA',home='PHI',event=None),
            dict(game_id='2026_05_TB_DAL',kickoff='2026-10-09T00:15:00+00:00',away='TB',home='DAL',event=None),
        ],
    )


def tiny_listings():
    rows=[
        dict(event_ticker='KXNFLGAME-26SEP28PHICHI',sub_title='PHI vs CHI (Sep 28)',title='Philadelphia vs Chicago',result='yes',last_price_dollars='0.6100'),
        dict(event_ticker='KXNFLGAME-26OCT01PITCLE',sub_title='PIT vs CLE (Oct 1)',title='PIT Steelers vs CLE Browns',volume_fp='10'),
        dict(event_ticker='KXNFLGAME-26OCT04JACCIN',sub_title='JAC vs CIN (Oct 4)',title='JAC Jaguars vs CIN Bengals'),
        dict(event_ticker='KXNFLGAME-26OCT04LARPHI',sub_title='LAR vs PHI (Oct 4)',title='LA Rams vs PHI Eagles'),
    ]
    return [identity.sanitize_listing_event(row) for row in rows]


def built():
    return panel.build_panel(tiny_registry(),tiny_listings(),AS_OF,AS_OF,'2026-09-22.1','test-cohort')


class Response:
    def __init__(self,body):
        self._raw=json.dumps(body).encode()
    def read(self):
        return self._raw
    def __enter__(self):
        return self
    def __exit__(self,*args):
        return False


class AllowlistTests(unittest.TestCase):
    def test_recorder_allowlist_matches_frozen_q4_and_rejects_private_routes(self):
        q4=load_q4()
        paths=[
            'events/KXNFLGAME-26OCT01PITCLE',
            'markets/KXNFLGAME-26OCT01PITCLE-PIT/orderbook',
            'markets/trades',
            'events',
            'portfolio/orders',
            'portfolio/positions',
            'orders',
            'markets/KXNFLGAME-26OCT01PITCLE-PIT/order',
            'events/KXNFLGAME-26OCT01PITCLE/../orders',
            'markets/../orders',
        ]
        for path in paths:
            self.assertEqual(allowlist.allowed_recorder_path(path),q4.allowed(path),path)
        self.assertFalse(allowlist.allowed_recorder_path('portfolio/orders'))
        self.assertFalse(allowlist.allowed_recorder_path('events'))

    def test_listing_allowlist_is_public_events_collection_only(self):
        ok=dict(series_ticker='KXNFLGAME',status='open',limit='200',with_nested_markets='false')
        self.assertTrue(allowlist.allowed_listing('events',ok))
        self.assertTrue(allowlist.allowed_listing('events',dict(ok,status='unopened',cursor='abcDEF012')))
        self.assertTrue(allowlist.allowed_listing('events',dict(ok,cursor='ab+cd/ef=')))
        self.assertFalse(allowlist.allowed_listing('events',dict(ok,cursor='ab..cd')))
        self.assertFalse(allowlist.allowed_listing('events',dict(ok,cursor='a&b')))
        self.assertFalse(allowlist.allowed_listing('portfolio/orders',ok))
        self.assertFalse(allowlist.allowed_listing('orders',ok))
        self.assertFalse(allowlist.allowed_listing('markets/trades',ok))
        self.assertFalse(allowlist.allowed_listing('events/KXNFLGAME-26OCT01PITCLE',ok))
        self.assertFalse(allowlist.allowed_listing('events',dict(ok,with_nested_markets='true')))
        self.assertFalse(allowlist.allowed_listing('events',dict(ok,status='settled')))
        self.assertFalse(allowlist.allowed_listing('events',dict(ok,series_ticker='KXOTHER')))
        self.assertFalse(allowlist.allowed_listing('events',dict(ok,side='yes')))

    def test_get_rejects_private_route_before_any_request(self):
        def explode(*args,**kwargs):
            raise AssertionError('urlopen should not be called')
        original=record.urlopen
        record.urlopen=explode
        try:
            with self.assertRaises(ValueError):
                record.get('portfolio/orders',{})
        finally:
            record.urlopen=original

    def test_listing_get_rejects_private_route_before_any_request(self):
        def explode(*args,**kwargs):
            raise AssertionError('urlopen should not be called')
        with self.assertRaises(ValueError):
            resolve_event_tickers.listing_get('portfolio/orders',{},opener=explode)


class IdentityTests(unittest.TestCase):
    def test_match_uses_listing_title_and_drops_outcome_fields(self):
        raw=dict(event_ticker='KXNFLGAME-26OCT01PITCLE',sub_title='PIT vs CLE (Oct 1)',title='PIT Steelers vs CLE Browns',
                 result='yes',last_price_dollars='0.5000',volume_fp='3')
        clean=identity.sanitize_listing_event(raw)
        self.assertNotIn('result',clean);self.assertNotIn('last_price_dollars',clean)
        found=identity.match_game(dict(kickoff='2026-10-02T00:15:00+00:00',away='PIT',home='CLE'),[clean])
        self.assertEqual(found['status'],'matched')
        self.assertEqual(found['event_ticker'],'KXNFLGAME-26OCT01PITCLE')
        self.assertNotIn('result',found)

    def test_aliases_and_eastern_date_and_unresolved_guess_is_not_an_id(self):
        self.assertEqual(identity.expected_ticker(dict(kickoff='2026-10-04T17:00:00+00:00',away='JAX',home='CIN')),'KXNFLGAME-26OCT04JACCIN')
        self.assertEqual(identity.expected_ticker(dict(kickoff='2026-10-04T17:00:00+00:00',away='LA',home='PHI')),'KXNFLGAME-26OCT04LARPHI')
        self.assertEqual(identity.eastern_stamp('2026-10-05T00:20:00+00:00'),'26OCT04')
        missing=identity.match_game(dict(kickoff='2026-10-09T00:15:00+00:00',away='TB',home='DAL'),[])
        self.assertEqual(missing['status'],'unresolved')
        self.assertIsNone(missing['event_ticker'])
        self.assertEqual(missing['pattern_absent_from_listing'],'KXNFLGAME-26OCT08TBDAL')

    def test_subtitle_disagreement_is_not_a_match(self):
        row=dict(event_ticker='KXNFLGAME-26OCT01PITCLE',sub_title='CLE vs PIT (Oct 1)',title='swapped')
        found=identity.match_game(dict(kickoff='2026-10-02T00:15:00+00:00',away='PIT',home='CLE'),[row])
        self.assertEqual(found['status'],'subtitle_mismatch')
        self.assertIsNone(found['event_ticker'])


class PanelTests(unittest.TestCase):
    def test_development_panel_and_bare_holdout(self):
        dev=json.loads((ROOT/'development_panel.json').read_text())
        self.assertEqual(len(panel.validate_panel(dev)),2)
        with self.assertRaises(ValueError):
            panel.validate_panel(dict(purpose='holdout',events=[]))
        with self.assertRaises(ValueError):
            panel.validate_structure(dict(purpose='holdout',events=[]))

    def test_classification_excludes_missed_window_and_unmatched_games(self):
        document=built()
        self.assertIsNone(document['admitted_at'])
        self.assertFalse(document['complete_prior_32_game_cohort'])
        self.assertEqual([game['game_id'] for game in document['events']],['2026_04_PIT_CLE','2026_04_JAX_CIN','2026_04_LA_PHI'])
        self.assertEqual(document['events'][0]['event'],'KXNFLGAME-26OCT01PITCLE')
        self.assertEqual(document['events'][1]['event'],'KXNFLGAME-26OCT04JACCIN')
        self.assertEqual(document['events'][2]['event'],'KXNFLGAME-26OCT04LARPHI')
        self.assertEqual(document['ineligible_incomplete'][0]['game_id'],'2026_03_PHI_CHI')
        self.assertEqual(document['unresolved_identities'][0]['event'],None)
        blob=json.dumps(document)
        self.assertNotIn('pattern_absent_from_listing',blob)
        self.assertNotIn('26OCT08TBDAL',blob)
        self.assertNotIn('"result"',blob)
        panel.validate_structure(document)

    def test_outcome_field_and_backfill_are_rejected(self):
        document=built()
        dirty=json.loads(json.dumps(document))
        dirty['events'][0]['result']='yes'
        with self.assertRaises(ValueError):
            panel.validate_structure(dirty)
        late=json.loads(json.dumps(document))
        late['events'].insert(0,json.loads(json.dumps(late['ineligible_incomplete'][0])))
        late['events'][0]['identity']='public_events_listing_title_only'
        late['ineligible_incomplete']=[]
        with self.assertRaises(ValueError):
            panel.validate_structure(late)

    def test_admission_stamp_must_precede_window_and_cannot_be_backdated(self):
        document=built()
        with self.assertRaises(ValueError):
            panel.validate_panel(document,now=AS_OF,resuming=False)
        stamped=admit.stamp_panel(document,AS_OF)
        self.assertEqual(panel.validate_panel(stamped,now=AS_OF,resuming=False)[0]['event'],'KXNFLGAME-26OCT01PITCLE')
        self.assertEqual(len(panel.validate_panel(stamped,now=PIT_START,resuming=True)),3)
        too_late=datetime(2026,9,25,0,15,1,tzinfo=timezone.utc)
        with self.assertRaises(ValueError):
            panel.validate_panel(stamped,now=too_late,resuming=False)
        rewritten=json.loads(json.dumps(stamped))
        rewritten['admitted_at']='2026-09-22T00:00:00+00:00'
        with self.assertRaises(ValueError):
            panel.validate_panel(rewritten,now=AS_OF,resuming=False)
        with self.assertRaises(ValueError):
            admit.stamp_panel(stamped,AS_OF)

    def test_reviewed_holdout_label_still_cannot_claim_the_old_cohort(self):
        document=built()
        document['purpose']='holdout'
        with self.assertRaises(ValueError):
            panel.validate_structure(document)
        document['reviewed']=True
        panel.validate_structure(document)
        document['complete_prior_32_game_cohort']=True
        with self.assertRaises(ValueError):
            panel.validate_structure(document)

    def test_fetch_listing_strips_outcomes_and_paginates_public_gets_only(self):
        pages={
            ('open',None):dict(cursor='Page2',events=[dict(event_ticker='KXNFLGAME-26OCT01PITCLE',sub_title='PIT vs CLE (Oct 1)',title='PIT',result='no',last_price_dollars='0.4000')]),
            ('open','Page2'):dict(cursor=None,events=[dict(event_ticker='KXNFLGAME-26OCT04JACCIN',sub_title='JAC vs CIN (Oct 4)',title='JAC')]),
            ('unopened',None):dict(cursor=None,events=[]),
        }
        seen=[]
        def opener(request,timeout):
            parsed=urlparse(request.full_url)
            self.assertTrue(parsed.path.endswith('/events'))
            query={key:values[-1] for key,values in parse_qs(parsed.query).items()}
            self.assertNotIn('portfolio',request.full_url)
            self.assertNotIn('order',request.full_url)
            seen.append(query)
            body=pages[(query['status'],query.get('cursor'))]
            return Response(body)
        rows=resolve_event_tickers.fetch_listings(opener=opener)
        self.assertEqual([row['event_ticker'] for row in rows],['KXNFLGAME-26OCT01PITCLE','KXNFLGAME-26OCT04JACCIN'])
        self.assertTrue(all('result' not in row and 'last_price_dollars' not in row for row in rows))
        self.assertEqual(seen[0]['with_nested_markets'],'false')
        self.assertEqual(seen[0]['series_ticker'],'KXNFLGAME')


class AdmissionAndStoreTests(unittest.TestCase):
    def test_template_has_no_admit_time_and_live_stamp_refuses_a_missed_deadline(self):
        document=built()
        form=admit.template_from_panel(document)
        self.assertIsNone(form['admitted_at'])
        self.assertIsNone(form['panel_sha256'])
        self.assertFalse(form['collector_running'])
        self.assertFalse(form['production_claim'])
        self.assertEqual(form['not_backfilled'][0]['game_id'],'2026_03_PHI_CHI')
        self.assertIn('2026-09-22T00:15:00+00:00',form['not_backfilled'][0]['t_minus_7d_start'])
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/'admitted_panel.json';log=Path(tmp)/'admission_log.jsonl'
            record_line=admit.write_admission(document,out,log,now=AS_OF)
            self.assertEqual(record_line['events'][0]['t_minus_7d_start'],'2026-09-25T00:15:00+00:00')
            self.assertFalse(record_line['collector_running'])
            saved=json.loads(out.read_text())
            self.assertEqual(saved['admitted_at'],'2026-09-22T21:00:00+00:00')
            with self.assertRaises(ValueError):
                admit.write_admission(document,out,log,now=datetime(2026,9,25,1,0,tzinfo=timezone.utc))

    def test_restart_keeps_watermark_and_rejects_a_changed_panel_hash(self):
        def page():
            return dict(kind='trades',ticker='T',page=0,received_at=100,body=dict(cursor='',trades=[dict(
                trade_id='one',ticker='T',yes_price_dollars='.4',no_price_dollars='.6',count_fp='10',
                taker_side='no',created_time='2026-09-21T00:00:00Z',is_block_trade=False)]))
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'capture.sqlite'
            store=record.Store(path,'panel')
            try:
                store.write([page()],ticker='T',start=0,end=100,complete=True);store.finish()
            finally:
                store.close()
            store=record.Store(path,'panel')
            try:
                self.assertEqual(store.checkpoint('T',0),100)
                self.assertEqual(store.db.execute('SELECT COUNT(*) FROM gaps').fetchone()[0],1)
            finally:
                store.close()
            with self.assertRaises(ValueError):
                record.Store(path,'changed')


class CommittedCohortTests(unittest.TestCase):
    def test_checked_in_panel_matches_listing_snapshot_and_leaves_phi_out(self):
        snapshot=json.loads((ROOT/'listing_snapshot_20260922.json').read_text())
        registry=json.loads(REGISTRY.read_text())
        retrieved=datetime.fromisoformat(snapshot['retrieved_at'])
        fresh=panel.build_panel(registry,snapshot['events'],retrieved,retrieved,'2026-09-22.1','schedule-only-20260922-after-phi-chi-miss')
        committed=json.loads((ROOT/'prospective_panel.json').read_text())
        self.assertEqual(committed,fresh)
        self.assertIsNone(committed['admitted_at'])
        self.assertEqual(committed['events'][0]['game_id'],'2026_04_PIT_CLE')
        self.assertEqual(committed['events'][0]['event'],'KXNFLGAME-26OCT01PITCLE')
        self.assertEqual(committed['events'][0]['t_minus_7d_start'],'2026-09-25T00:15:00+00:00')
        polled={game['game_id'] for game in committed['events']}
        self.assertNotIn('2026_03_PHI_CHI',polled)
        self.assertEqual(committed['ineligible_incomplete'][0]['event'],'KXNFLGAME-26SEP28PHICHI')
        self.assertTrue(all(game['event'] is None for game in committed['unresolved_identities']))
        self.assertEqual(len(committed['events'])+len(committed['ineligible_incomplete'])+len(committed['unresolved_identities']),32)
        form=json.loads((ROOT/'admission_log.template.json').read_text())
        self.assertIsNone(form['admitted_at'])
        self.assertEqual([game['event'] for game in form['events']],[game['event'] for game in committed['events']])
        self.assertEqual(form['not_backfilled'][0]['game_id'],'2026_03_PHI_CHI')
        blob=json.dumps(committed)+json.dumps(snapshot)
        for banned in ('"result"','last_price','settlement_value','"pnl"'):
            self.assertNotIn(banned,blob)


if __name__=='__main__':
    unittest.main()
