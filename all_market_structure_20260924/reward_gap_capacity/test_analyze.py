import unittest
from analyze import ledger,batches


class GapCapacityTests(unittest.TestCase):
    def test_funded_capacity(self):
        row=ledger(413,0)
        self.assertEqual(row['funded'],4997.3)
        self.assertGreater(ledger(414,0)['funded'],5000)
        self.assertEqual(row['reward'],6756.68)
        self.assertEqual(row['net_cushion'],1759.38)

    def test_failure_severity(self):
        self.assertEqual(ledger(413,'.25')['net_cushion'],70.21)
        self.assertEqual(ledger(413,1)['net_cushion'],-4997.3)

    def test_snapshots_not_summed(self):
        row=dict(source='S',cycle=0,book_received_ns=1,ticker='T',program_id='P',
                 event_ticker='E',quantity={'yes':'1100'},principal=11,reserve=1.1,reward=16.36,cushion=4.26)
        out=batches([row,dict(row),dict(row,book_received_ns=2)])
        self.assertEqual([r['order_sets'] for r in out],[1,1])

    def test_distinct_pools_same_event_count_separately(self):
        row=dict(source='S',cycle=0,book_received_ns=1,ticker='T',program_id='P',
                 event_ticker='E',quantity={'yes':'1100'},principal=11,reserve=1.1,reward=16.36,cushion=4.26)
        out=batches([row,dict(row,ticker='T2',program_id='P2')])
        self.assertEqual(out[0]['order_sets'],2)
        self.assertEqual(out[0]['principal'],22)
        self.assertEqual(out[0]['cushion'],8.52)


if __name__=='__main__':unittest.main()
