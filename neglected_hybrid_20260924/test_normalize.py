import hashlib,json,tempfile,unittest
from pathlib import Path
from normalize import forecast_rows,race_key,reviewed_rule,REVIEWED_PARTY_RULES

class SourceMappingTests(unittest.TestCase):
    def test_rule_alias_is_exact_and_ticker_scoped(self):
        for ticker,rule in REVIEWED_PARTY_RULES.items():
            self.assertTrue(reviewed_rule(ticker,rule))
            self.assertFalse(reviewed_rule('OTHER-24-D',rule))
            self.assertFalse(reviewed_rule(ticker,rule.replace('2025','2027')))
    def write_source(self,root,data):
        blob=json.dumps(data).encode();(root/'source.json').write_bytes(blob)
        (root/'house_latest.receipt.json').write_text(json.dumps({'admitted':True,'chamber':'house',
          'source_file':'source.json','decoded_sha256':hashlib.sha256(blob).hexdigest(),
          'available_at':'2024-11-03T20:38:57+00:00','url':'https://example.test/archived'}))
    def test_party_probability_sums_same_party_candidates(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);self.write_source(p,[{'state':'CA','seat':'16','candidates':{'dem':'A','dem1':'B'},'winprob':{'dem':40,'dem1':60}}])
            rows=forecast_rows(p);self.assertEqual(rows[0]['p_dem'],1)
            self.assertEqual(rows[0]['available_at'],'2024-11-03T20:38:57+00:00')
    def test_integrity_mismatch_refused(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);self.write_source(p,[]);(p/'source.json').write_text('[{}]')
            with self.assertRaises(ValueError):forecast_rows(p)
    def test_invalid_probability_sum_refused(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);self.write_source(p,[{'state':'CA','seat':'1','candidates':{},'winprob':{'dem':40,'rep':40}}])
            with self.assertRaises(ValueError):forecast_rows(p)
    def test_at_large_and_leading_zero_mapping(self):
        self.assertEqual(race_key('HOUSEAKAL-24-D')[0],'2024-HOUSE-AK-1')
        self.assertEqual(race_key('HOUSEPARTY-MI07-24-D')[0],'2024-HOUSE-MI-7')
        self.assertEqual(race_key('SENATEPA-24-D')[0],'2024-SENATE-PA-1')
    def test_special_or_wrong_year_not_silently_joined(self):
        for ticker in ['SENATENE-26-D','SENATENES-24-D','HOUSECA13-24-R','HOUSECA13-25-D']:
            self.assertIsNone(race_key(ticker))

if __name__=='__main__':unittest.main()
