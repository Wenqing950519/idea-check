import unittest

from src.entailment_judge import EntailmentJudge
from src.models import Claim, Evidence, EvidenceRelation
from tests.helpers import load_fixture


class EntailmentTests(unittest.TestCase):
    def test_passage_level_direct_support_is_preserved(self) -> None:
        fixture = load_fixture("directly_verifiable.json")
        judgment = EntailmentJudge().judge(
            Claim.from_dict(fixture["claim"]),
            Evidence.from_dict(fixture["evidence"][0]),
        )
        self.assertEqual(judgment.relation, EvidenceRelation.DIRECT_SUPPORT)
        self.assertIn("passage", judgment.reason.lower())

    def test_missing_passage_can_never_support(self) -> None:
        fixture = load_fixture("directly_verifiable.json")
        evidence = dict(fixture["evidence"][0])
        evidence["passage"] = ""
        judgment = EntailmentJudge().judge(
            Claim.from_dict(fixture["claim"]), Evidence.from_dict(evidence)
        )
        self.assertEqual(judgment.relation, EvidenceRelation.UNRESOLVED)

    def test_direct_support_without_contradiction_search_is_not_verified(self) -> None:
        from src.models import VerdictLabel
        from src.verdict_engine import VerdictEngine

        fixture = load_fixture("directly_verifiable.json")
        verdict = VerdictEngine().decide(
            Claim.from_dict(fixture["claim"]),
            [Evidence.from_dict(fixture["evidence"][0])],
            contradiction_search_completed=False,
        )
        self.assertEqual(verdict.verdict, VerdictLabel.SUPPORTED)
        self.assertIn("CONTRADICTION_SEARCH_MISSING", verdict.risk_flags)


if __name__ == "__main__":
    unittest.main()
