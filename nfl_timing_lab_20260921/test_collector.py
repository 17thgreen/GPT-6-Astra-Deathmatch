import importlib.util,json,tempfile,unittest
from pathlib import Path

spec=importlib.util.spec_from_file_location('recorder',Path(__file__).parent/'collector/record.py')
rec=importlib.util.module_from_spec(spec);spec.loader.exec_module(rec)


def page(size='10',cursor='',index=0):
    return dict(kind='trades',ticker='T',page=index,received_at=100,
        body=dict(cursor=cursor,trades=[dict(trade_id='one',ticker='T',yes_price_dollars='.4',no_price_dollars='.6',
            count_fp=size,taker_side='no',created_time='2026-09-21T00:00:00Z',is_block_trade=False)]))


class CollectorTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.path=Path(self.tmp.name)/'capture.sqlite';self.s=rec.Store(self.path,'panel')
    def tearDown(self):
        if self.s:self.s.close()
        self.tmp.cleanup()

    def test_only_one_writer(self):
        with self.assertRaises(RuntimeError):rec.Store(self.path,'panel')

    def test_restart_preserves_watermark_and_records_gap(self):
        self.s.write([page()],ticker='T',start=0,end=100,complete=True);self.s.finish();self.s.close()
        self.s=rec.Store(self.path,'panel')
        self.assertEqual(self.s.checkpoint('T',0),100)
        self.assertEqual(self.s.db.execute('SELECT COUNT(*) FROM gaps').fetchone()[0],1)

    def test_duplicate_trade_not_duplicated(self):
        self.s.write([page()]);self.s.write([page()])
        self.assertEqual(self.s.db.execute('SELECT COUNT(*) FROM trades').fetchone()[0],1)
        self.assertEqual(self.s.db.execute('SELECT COUNT(*) FROM responses').fetchone()[0],2)

    def test_conflict_rolls_back_response_and_checkpoint(self):
        self.s.write([page()],ticker='T',start=0,end=100,complete=True)
        with self.assertRaises(ValueError):self.s.write([page('11')],ticker='T',start=90,end=200,complete=True)
        self.assertEqual(self.s.checkpoint('T',0),100)
        self.assertEqual(self.s.db.execute('SELECT COUNT(*) FROM responses').fetchone()[0],1)

    def test_unfinished_pages_never_advance(self):
        self.s.write([page(cursor='more')],ticker='T',start=0,end=100,complete=False)
        self.assertEqual(self.s.checkpoint('T',-1),-1)
        with self.assertRaises(ValueError):self.s.write([page(cursor='more')],ticker='T',start=0,end=100,complete=True)
        self.assertEqual(self.s.checkpoint('T',-1),-1)

    def test_missing_first_page_rejected(self):
        with self.assertRaises(ValueError):self.s.write([page(index=1)],ticker='T',start=0,end=100,complete=True)
        self.assertEqual(self.s.db.execute('SELECT COUNT(*) FROM responses').fetchone()[0],0)

    def test_watermark_cannot_move_backward(self):
        self.s.write([page()],ticker='T',start=0,end=100,complete=True)
        self.s.write([page()],ticker='T',start=0,end=90,complete=True)
        self.assertEqual(self.s.checkpoint('T',0),100)

    def test_private_and_unregistered_panel_rejected(self):
        self.assertFalse(rec.allowed('portfolio/orders'));self.assertFalse(rec.allowed('markets/../orders'))
        with self.assertRaises(ValueError):rec.validate_panel(dict(purpose='holdout',events=[]))

    def test_changed_panel_cannot_resume_database(self):
        self.s.close();self.s=None
        with self.assertRaises(ValueError):rec.Store(self.path,'changed')


if __name__=='__main__':unittest.main()
