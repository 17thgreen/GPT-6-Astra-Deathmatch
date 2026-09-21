import json
import unittest
import numpy as np
from sklearn.tree import DecisionTreeRegressor
import test_research
from stern_round2 import KNOTS, clock_design, encode_tree, tree_predict, residual_model, predict, mirror


class TestRound2(unittest.TestCase):
    def frame(self):
        d = test_research.TestResearchContract().frame()
        d["half_seconds_remaining"] = [360,1440,1080]
        d["total_line"] = [45,48,42]
        return d

    def base(self):
        return {"kind":"v1", "coefficient_vector":[.8,1.2,1,2,3,-1,-2,-3,-1,2,.5]}

    def test_clock_reduces_to_v1_and_monotone_in_score(self):
        b = self.base()["coefficient_vector"]
        m = {"kind":"clock", "knots":KNOTS.tolist(), "coefficient_vector":[b[0]]*6+[b[1]]*6+b[2:]}
        d = self.frame()
        np.testing.assert_allclose(predict(d,m),predict(d,self.base()))
        higher = d.copy(); higher["margin"] += 1
        self.assertTrue((predict(higher,m) >= predict(d,m)).all())
        np.testing.assert_allclose(predict(d,m)+predict(mirror(d),m),1.)

    def test_json_tree_matches_sklearn_at_float32_boundaries(self):
        rng = np.random.default_rng(912)
        x = rng.normal(size=(200,4)).astype(np.float32)
        t = DecisionTreeRegressor(max_depth=3,random_state=17).fit(x,3*x[:,0]-x[:,1]**2)
        encoded = json.loads(json.dumps(encode_tree(t)))
        np.testing.assert_allclose(tree_predict(x,encoded),np.clip(t.predict(x),-2,2))

    def test_residual_symmetry_with_asymmetric_tree(self):
        tree = {"left":[1,-1,-1],"right":[2,-1,-1],"feature":[1,-2,-2],
                "threshold":[0.,-2.,-2.],"value":[0.,.8,-.2]}
        m = residual_model(self.base(),1,[tree])
        d = self.frame()
        np.testing.assert_allclose(predict(d,m)+predict(mirror(d),m),1.,atol=1e-14)
        d["y"] = [0,1,0]; d["home_score"] = [99,99,99]
        p = predict(d,m)
        d["y"] = 1-d.y; d["home_score"] = [0,0,0]
        np.testing.assert_array_equal(p,predict(d,m))

    def test_empty_residual_reduces_to_base(self):
        m = residual_model(self.base(),2,[])
        np.testing.assert_allclose(predict(self.frame(),m),predict(self.frame(),self.base()),atol=1e-9)

    def test_rejects_missing_extra_state_and_invalid_coefficients(self):
        d = self.frame(); d.loc[0,"total_line"] = np.nan
        with self.assertRaises(ValueError):predict(d,residual_model(self.base(),2,[]))
        m = {"kind":"clock","knots":KNOTS.tolist(),"coefficient_vector":[1.]*20}
        with self.assertRaises(ValueError):predict(self.frame(),m)


if __name__ == "__main__":unittest.main()
