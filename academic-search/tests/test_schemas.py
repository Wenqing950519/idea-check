import json
import unittest
from pathlib import Path

from tests.helpers import FIXTURES


ROOT = Path(__file__).resolve().parents[1]


class SchemaTests(unittest.TestCase):
    def test_all_schemas_are_valid_json_with_2020_12_marker(self) -> None:
        schemas = list((ROOT / "schemas").glob("*.schema.json"))
        self.assertTrue({
            "claim.schema.json", "evidence.schema.json", "verdict.schema.json", "audit.schema.json"
        }.issubset({path.name for path in schemas}))
        for path in schemas:
            data = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(data["$schema"], "https://json-schema.org/draft/2020-12/schema")

    def test_five_fixture_cases_have_passage_level_evidence(self) -> None:
        fixtures = [path for path in FIXTURES.glob("*.json") if "expected_verdict" in json.loads(path.read_text(encoding="utf-8"))]
        self.assertEqual(len(fixtures), 5)
        for path in fixtures:
            data = json.loads(path.read_text(encoding="utf-8"))
            self.assertIn(data["expected_verdict"], {
                "VERIFIED", "SUPPORTED", "QUALIFIED", "UNVERIFIED", "CONTRADICTED", "ORIGINAL_HYPOTHESIS"
            })
            for evidence in data["evidence"]:
                self.assertTrue(evidence["passage"].strip())
                self.assertTrue(evidence["document_locator"].strip())


if __name__ == "__main__":
    unittest.main()
