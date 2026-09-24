import unittest
from demo_probe import public_message
class ProbeTests(unittest.TestCase):
    def test_private_metadata_removed(self):
        result=public_message({'type':'orderbook_delta','sid':1,'seq':2,'account_id':'secret',
            'msg':{'market_ticker':'EXAMPLE','client_order_id':'secret','account_id':'secret',
                   'price_dollars':'0.25','delta_fp':'-2.00','side':'yes'}})
        self.assertNotIn('secret',str(result))
        self.assertEqual(result['msg']['delta_fp'],'-2.00')
    def test_documented_fixed_point_snapshot_preserved(self):
        msg={'market_ticker':'EXAMPLE','yes_dollars_fp':[['0.25','2.00']],'no_dollars_fp':[]}
        self.assertEqual(public_message({'type':'orderbook_snapshot','msg':msg})['msg'],msg)
if __name__=='__main__':unittest.main()
