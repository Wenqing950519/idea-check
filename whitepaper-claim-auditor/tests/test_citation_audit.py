import unittest

from src.citation_auditor import CitationAuditor
from src.models import Claim, Evidence
from src.verdict_engine import VerdictEngine
from tests.helpers import load_fixture


class CitationAuditTests(unittest.TestCase):
    def test_context_only_citation_counts_as_false_support(self) -> None:
        fixture = load_fixture("citation_laundering.json")
        claim = Claim.from_dict(fixture["claim"])
        evidence = [Evidence.from_dict(item) for item in fixture["evidence"]]
        verdict = VerdictEngine().decide(claim, evidence)
        audit = CitationAuditor().audit(
            [claim], evidence, [verdict], {claim.claim_id: [evidence[0].evidence_id]}
        )
        self.assertEqual(audit["false_support_count"], 1)
        self.assertEqual(audit["accuracy_issues"][0]["issue"], "FALSE_SUPPORT_CONTEXT_ONLY")


if __name__ == "__main__":
    unittest.main()
