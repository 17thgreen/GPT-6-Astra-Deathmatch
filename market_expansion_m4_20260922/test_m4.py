import copy
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path
from m4_common import write_rows
from m4_metadata import coefficients, select_nba, validate_structure
from m4_capture import trade_intervals, quote_schema
from m4_policy import SizeRouter, ClockRouter, Config
import m4_audit as audit

KO=2_000_000
AT=KO-100000


def markets():
    return {t:dict(event='G',direction=d,kickoff=KO,listed_at=KO-700000,verified_mecnet=True)
            for t,d in [('A',1),('B',-1)]}


def engine(size=250,complete_first=False):
    return SizeRouter(markets(),replace(Config(),order_size=size,exposure_cap=size,
        queue_early=3300,quote_source='candles',liquidation_lead_seconds=300),complete_first)


def book(r,at=AT):
    for t in ('A','B'):
        r.books[t]=dict(bid=.49,ask=.51,bid_at=at,ask_at=at)


def exercise(r):
    for ticker in ('A','B'):
        r.on_quote(dict(ticker=ticker,at=AT,asof=AT-60,bid=.49,ask=.51))
    for i in range(8):
        r.on_trade(dict(ticker='A',at=AT+i+1,yes_price=.49 if i%2 else .51,
            taker_side='no' if i%2 else 'yes',size=10000,trade_id=str(i)))
    return r.finish(KO-1500)


class StorageMetadataTests(unittest.TestCase):
    def test_tier_split_never_drops_boundary_second(self):
        self.assertEqual(trade_intervals(10,30,20),[('historical/trades',10,20),('markets/trades',20,30)])
        self.assertEqual(trade_intervals(10,15,20),[('historical/trades',10,15)])
        self.assertEqual(trade_intervals(25,30,20),[('markets/trades',25,30)])

    def test_historical_quote_uses_documented_dollar_string(self):
        row=quote_schema(dict(yes_bid={'close':'.49'},yes_ask={'close':'.51'}),True)
        self.assertEqual(row['yes_bid']['close_dollars'],'.49')

    def test_ambiguous_cents_and_conflicting_quote_fields_rejected(self):
        for data in ({'close':49},{'close':'49'},{'close':'.49','close_dollars':'.50'}):
            with self.assertRaises(ValueError):quote_schema({'yes_bid':data},True)

    def test_fee_override_has_precedence_over_series_discount(self):
        s=dict(fee_type='quadratic_with_maker_fees',fee_multiplier=.5)
        self.assertEqual(coefficients(s,{})['maker'],.00875)
        self.assertEqual(coefficients(s,dict(fee_multiplier_override=1))['maker'],.0175)
        self.assertEqual(coefficients(s,dict(fee_multiplier_override=1))['taker'],.07)

    def test_explicit_zero_override_and_no_maker_fee(self):
        s=dict(fee_type='quadratic_with_maker_fees',fee_multiplier=1)
        self.assertEqual(coefficients(s,dict(fee_multiplier_override=0))['taker'],0)
        self.assertEqual(coefficients(s,dict(fee_type_override='quadratic'))['maker'],0)

    def test_invalid_fee_rules_rejected(self):
        for s in [dict(fee_type='other',fee_multiplier=1),dict(fee_type='quadratic',fee_multiplier=-1)]:
            with self.assertRaises(ValueError):coefficients(s,{})

    def test_nba_selection_is_date_balanced_and_ignores_other_dates(self):
        ids=['KXNBAGAME-26MAY01BB','KXNBAGAME-26MAY01AA','KXNBAGAME-26MAY02CC',
             'KXNBAGAME-26MAY21DD','KXNBAGAME-26JUN01EE']
        selected,_=select_nba(ids)
        self.assertEqual(selected,['KXNBAGAME-26MAY01AA','KXNBAGAME-26MAY02CC','KXNBAGAME-26MAY01BB'])

    def test_missing_rules_block_admission(self):
        e=dict(event_ticker='G',series_ticker='KXNBAGAME',collateral_return_type='MECNET',mutually_exclusive=True)
        ms=[dict(ticker=t,event_ticker='G',yes_sub_title=t,market_type='binary',
             notional_value_dollars='1',price_level_structure='linear_cent',rules_primary='wins',rules_secondary='') for t in ('A','B')]
        with self.assertRaisesRegex(ValueError,'Missing contract rules'):
            validate_structure('KXNBAGAME',e,ms,{})


class InventoryPolicyTests(unittest.TestCase):
    def test_original_mode_exact_fill_and_order_control(self):
        a=engine();b=ClockRouter(markets(),a.cfg,30,'constant')
        exercise(a);exercise(b)
        self.assertTrue(a.fills)
        self.assertEqual(a.fills,b.fills)
        self.assertEqual(a.order_records,b.order_records)

    def test_order_and_cap_are_coupled_and_exit_allowance_unchanged(self):
        r=engine(25);result=exercise(r)
        self.assertTrue(r.order_records)
        self.assertTrue(all(o['submitted_quantity']<=25 for o in r.order_records.values()))
        self.assertLessEqual(r.max_exposure,25)
        self.assertEqual(r.cfg.assumed_exit_depth,250)

    def test_complete_first_keeps_only_bounded_offsets(self):
        r=engine(100,True);book(r);r.holdings['G']=20
        cs=r.event_candidates('G',AT);chosen=r.choose(cs)
        legs=[c for c in cs if c['key'] in chosen]
        self.assertTrue(legs)
        self.assertTrue(all(c['direction']==-1 and c['wanted']==20 for c in legs))

    def test_pending_other_offset_is_reserved_until_cancellation(self):
        r=engine(100,True);book(r);r.holdings['G']=20
        r.quote('B','yes',.49,7,AT)
        pending=r.orders['B','yes'];r.cancel(pending,AT,'test')
        cs=r.event_candidates('G',AT);chosen=r.choose(cs)
        legs=[c for c in cs if c['key'] in chosen]
        self.assertEqual(len(legs),1)
        self.assertEqual(legs[0]['wanted'],13)
        self.assertEqual(pending.cancel_at,AT+.25)

    def test_existing_offset_never_grows_or_loses_priority_for_free(self):
        r=engine(100,True);book(r);r.holdings['G']=20
        r.quote('A','no',.49,10,AT);o=r.orders['A','no'];o.queue=77
        identity=o.identity;r.refresh('G',AT)
        self.assertEqual(r.orders['A','no'].identity,identity)
        self.assertEqual(r.orders['A','no'].queue,77)
        self.assertEqual(r.orders['A','no'].remaining,10)

    def test_flat_inventory_retains_ordinary_pair_admission(self):
        a,b=engine(100,True),engine(100,False)
        book(a);book(b)
        self.assertEqual(a.choose(a.event_candidates('G',AT)),b.choose(b.event_candidates('G',AT)))

    def test_fill_immediately_requests_exposure_cancel(self):
        r=engine(100,True)
        for t in ('A','B'):r.on_quote(dict(ticker=t,at=AT,asof=AT-60,bid=.49,ask=.51))
        r.on_trade(dict(ticker='A',at=AT+1,yes_price=.49,taker_side='no',size=3400,trade_id='one'))
        self.assertEqual(r.holdings['G'],50)
        adding=[o for o in r.orders.values() if o.direction==1]
        self.assertTrue(adding)
        self.assertTrue(all(o.cancel_at==AT+1.25 for o in adding))
        # An order remains exposed during the cancellation delay.
        r.on_trade(dict(ticker='A',at=AT+1.1,yes_price=.49,taker_side='no',size=20,trade_id='two'))
        self.assertGreater(r.holdings['G'],50)


class FinancialAuditTests(unittest.TestCase):
    def test_small_cap_ledger_reconciles_and_tampering_is_rejected(self):
        r=engine(25);result=exercise(r)
        result['sport_cashflows']={'test':sum(g['cashflow'] for g in result['per_game'])}
        with tempfile.TemporaryDirectory() as directory:
            previous=audit.ROOT;audit.ROOT=Path(directory)
            try:
                write_rows(audit.ROOT/'results/case_fills.jsonl.gz',r.fills)
                write_rows(audit.ROOT/'results/case_orders.jsonl.gz',r.order_records.values())
                self.assertTrue(audit.verify('case',result,r.markets)['passed'])
                fills=copy.deepcopy(r.fills);fills[0]['fee']+=.01
                write_rows(audit.ROOT/'results/case_fills.jsonl.gz',fills)
                with self.assertRaises(AssertionError):audit.verify('case',result,r.markets)
            finally:audit.ROOT=previous


if __name__=='__main__':unittest.main()
