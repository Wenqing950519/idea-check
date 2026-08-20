import unittest

from src.models import Claim, Evidence, VerdictLabel
from src.verdict_engine import VerdictEngine
from tests.helpers import load_fixture


class OverclaimTests(unittest.TestCase):
    def _verdict(self, fixture_name: str):
        fixture = load_fixture(fixture_name)
        return VerdictEngine().decide(
            Claim.from_dict(fixture["claim"]),
            [Evidence.from_dict(item) for item in fixture["evidence"]],
        )

    def test_context_only_source_does_not_become_support(self) -> None:
        verdict = self._verdict("citation_laundering.json")
        self.assertEqual(verdict.verdict, VerdictLabel.UNVERIFIED)
        self.assertIn("INFERENCE_GAP", verdict.risk_flags)

    def test_correlation_does_not_verify_causality(self) -> None:
        verdict = self._verdict("causal_overreach.json")
        self.assertEqual(verdict.verdict, VerdictLabel.UNVERIFIED)
        self.assertIn("CAUSAL_EVIDENCE_MISMATCH", verdict.risk_flags)

    def test_strong_causal_claim_requires_scope_match(self) -> None:
        fixture = load_fixture("causal_overreach.json")
        row = dict(fixture["evidence"][0])
        row.update({"relation": "DIRECT_SUPPORT", "source_quality": "A", "causal_design": True, "scope_match": False})
        verdict = VerdictEngine().decide(
            Claim.from_dict(fixture["claim"]),
            [Evidence.from_dict(row)],
            contradiction_search_completed=True,
        )
        self.assertEqual(verdict.verdict, VerdictLabel.UNVERIFIED)
        self.assertIn("SCOPE_EVIDENCE_MISMATCH", verdict.risk_flags)


if __name__ == "__main__":
    unittest.main()
