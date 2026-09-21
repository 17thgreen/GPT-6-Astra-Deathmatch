import copy,unittest
from q8_analysis import select

def fixture():
    return {f'q{q}_d{d:g}_{arm}':dict(all_flat=True,completed_strategy_pnl=100 if arm=='router_on' else 110,unhedged_contract_hours=100,week_contributions=dict(week1=50 if arm=='router_on' else 55,week2=50 if arm=='router_on' else 55),pnl_excluding_top_two_games=20) for q in [3300,10000] for d in [.25,5] for arm in ['router_on','rescue','joint']}

class SelectionTests(unittest.TestCase):
    def test_both_pass_prefers_rescue(self):self.assertEqual(select(fixture())['selected'],'rescue')
    def test_profit_tie_fails(self):
        s=fixture();s['q10000_d5_rescue']['completed_strategy_pnl']=100
        self.assertEqual(select(s)['selected'],'joint')
    def test_inventory_failure_and_unresolved_retain_q7(self):
        s=fixture();s['q3300_d5_rescue']['unhedged_contract_hours']=126
        s['q10000_d5_joint']['all_flat']=False;s['q10000_d5_joint']['completed_strategy_pnl']=None
        self.assertEqual(select(s)['selected'],'router_on')
    def test_week_and_concentration_failure(self):
        s=fixture();s['q3300_d0.25_rescue']['week_contributions']['week2']=49
        s['q3300_d0.25_joint']['pnl_excluding_top_two_games']=-1
        self.assertEqual(select(s)['selected'],'router_on')
