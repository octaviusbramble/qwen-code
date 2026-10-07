import json
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).parents[1]
sys.path.insert(0, str(ROOT))
from config.validate import validate


class ConfigTests(unittest.TestCase):
    def test_current_settings_shape(self):
        data = validate(ROOT / "config/settings.example.json")
        provider = data["modelProviders"]["openai"][0]
        self.assertEqual(provider["baseUrl"], "https://argolink.io/v1")
        self.assertEqual(provider["wireApi"], "responses")
        self.assertEqual(data["model"]["name"], "gpt-6-sol")

    def test_no_real_key_or_retired_base(self):
        text = (ROOT / "config/settings.example.json").read_text(encoding="utf-8")
        self.assertNotIn("sk-", text.lower())
        self.assertNotIn("api." + "argolink.io", text)

    def test_workflow_names_current_config(self):
        plan = (ROOT / "workflow/plan.yaml").read_text(encoding="utf-8")
        self.assertIn("qwen-code", plan)
        self.assertIn("gpt-6-sol", plan)
        self.assertIn("wire_api: responses", plan)


if __name__ == "__main__":
    unittest.main()
