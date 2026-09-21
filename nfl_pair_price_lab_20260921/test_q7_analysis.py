import copy
import unittest
from q7_analysis import fill_markout, selection, differences, ARMS


def sample():
    out={}
    for q in [3300,10000]:
        for d in [.25,5]:
            for a,p in zip(ARMS,[100,150,120,155]):
                out[f'q{q}_d{d:g}_{a}']=dict(completed_strategy_pnl=p,all_flat=True,
                    unhedged_contract_hours=100,week_contributions=dict(week1=p/2,week2=p/2),
                    pnl_excluding_top_two_games=p-10)
    return out


class AnalysisTests(unittest.TestCase):
    def test_selection_all_gates_and_retention(self):
        s=sample();self.assertEqual(selection(s)['selected'],'router_on')
        s['q10000_d5_router_on']['completed_strategy_pnl']=140
        self.assertIsNone(selection(s)['selected'])

    def test_unresolved_is_not_profit(self):
        s=sample();s['q10000_d5_router_on'].update(all_flat=False,completed_strategy_pnl=None)
        self.assertIsNone(selection(s)['selected'])
        self.assertEqual(differences(s)['q10000_d5']['status'],'UNRESOLVED_NO_COMPLETE_CONTRAST')

    def test_interaction_sign(self):
        e=differences(sample())['q3300_d0.25']
        self.assertEqual(e['guard_effect_router'],50);self.assertEqual(e['guard_effect_allocator'],35)
        self.assertEqual(e['interaction'],-15)

    def test_markout_uses_received_quote_not_future_quote(self):
        f=dict(at=1000,outcome='yes',price=.49,size=10,fee=.04,outcome_mid_at_fill=.50)
        qs=[dict(at=1290,asof=1230,bid=.51,ask=.53),dict(at=1301,asof=1241,bid=.80,ask=.82)]
        m=fill_markout(f,[1290,1301],qs)
        self.assertAlmostEqual(m['change'],.02);self.assertAlmostEqual(m['entry_fee_mark'],.026)

    def test_stale_pre_fill_and_missing_marks_excluded(self):
        f=dict(at=1000,outcome='yes',price=.49,size=10,fee=.04,outcome_mid_at_fill=.50)
        for at,asof in [(1290,1000),(1100,1040)]:
            self.assertIsNone(fill_markout(f,[at],[dict(at=at,asof=asof,bid=.51,ask=.53)]))
        self.assertIsNone(fill_markout(f,[],[]))

    def test_no_contract_complement(self):
        f=dict(at=1000,outcome='no',price=.49,size=10,fee=.04,outcome_mid_at_fill=.50)
        m=fill_markout(f,[1290],[dict(at=1290,asof=1230,bid=.51,ask=.53)])
        self.assertAlmostEqual(m['change'],-.02)


if __name__=='__main__':unittest.main()
