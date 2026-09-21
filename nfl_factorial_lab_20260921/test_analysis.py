import unittest
from analyze import contrasts,LABELS
class ContrastTests(unittest.TestCase):
    def test_additive_effects(self):
        values={s:10+2*int(s[0])+3*int(s[1])+5*int(s[2]) for s in LABELS}
        r=contrasts(values)
        self.assertEqual(r['main_effects'],dict(flow=2,protection=3,ranking=5))
        self.assertEqual(r['pairwise_interactions'],{'flow × protection':0,'flow × ranking':0,'protection × ranking':0})
        self.assertAlmostEqual(r['three_way_interaction'],0)
        for f,v in dict(flow=2,protection=3,ranking=5).items():self.assertAlmostEqual(r['shapley'][f],v)
    def test_known_interactions_and_shapley(self):
        values={}
        for s in LABELS:
            f,p,r=map(int,s);values[s]=10+2*f+3*p+5*r+7*f*p+11*f*r+13*p*r+17*f*p*r
        out=contrasts(values)
        self.assertAlmostEqual(out['pairwise_interactions']['flow × protection'],15.5)
        self.assertAlmostEqual(out['three_way_interaction'],17)
        self.assertAlmostEqual(out['shapley']['flow'],2+7/2+11/2+17/3)
        self.assertAlmostEqual(sum(out['shapley'].values()),values['111']-values['000'])
if __name__=='__main__':unittest.main()
