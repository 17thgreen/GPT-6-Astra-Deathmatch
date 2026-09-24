import json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import analyze
class ReaderTests(unittest.TestCase):
    def test_http_200_html_is_not_market_data(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);(root/'capture').mkdir()
            (root/'capture/x.json').write_text(json.dumps({'status':200,'error':None,'raw':'<html>Site Unavailable</html>'}))
            with patch.object(analyze,'ROOT',root):receipt,data=analyze.read('x')
            self.assertIsNone(data);self.assertEqual(receipt['analysis_error'],'non_json_response')
if __name__=='__main__':unittest.main()
