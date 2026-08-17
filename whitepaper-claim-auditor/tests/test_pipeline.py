import unittest

from adapters.static import StaticEvidenceAdapter
from src.models import Evidence
from src.pipeline import AuditPipeline
from tests.helpers import load_fixture


class PipelineTests(unittest.TestCase):
    def test_full_stage_sequence_produces_verified_report(self) -> None:
        fixture = load_fixture("directly_verifiable.json")
        evidence = [Evidence.from_dict(item) for item in fixture["evidence"]]
        pipeline = AuditPipeline([StaticEvidenceAdapter(evidence)])
        audit = pipeline.run(
            fixture["claim"]["original_text"],
            citations={"C-001": ["E-001"]},
        )
        self.assertEqual(audit["summary"]["verdict_counts"]["VERIFIED"], 1)
        self.assertEqual(audit["citation_audit"]["false_support_count"], 0)
        self.assertIn("# Evidence Matrix", pipeline.report_builder.to_markdown(audit))


if __name__ == "__main__":
    unittest.main()
