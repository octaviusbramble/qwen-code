import json,pathlib,unittest
class T(unittest.TestCase):
 def test_no_key(self):
  d=json.loads((pathlib.Path(__file__).parents[1]/'config/settings.example.json').read_text());self.assertNotIn('sk-',str(d));self.assertIn('base_url',d['provider'])
if __name__=='__main__':unittest.main()
