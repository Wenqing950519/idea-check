import unittest

from src.contracts import AnalysisArtifact, ArtifactStatus, ClaimStatus, ResearchClaim, ResearchEvidence, EvidencePolarity


class ResearchContractTests(unittest.TestCase):
    def test_claim_status_is_exactly_four_states(self) -> None:
        self.assertEqual({item.value for item in ClaimStatus}, {"SUPPORTED", "PARTIAL", "CONTRADICTED", "UNRESOLVED"})

    def test_evidence_requires_passage_and_locator(self) -> None:
        with self.assertRaises(ValueError):
            ResearchEvidence("EV-0000000000000000", "SRC-0000000000000000", "DOC-0000000000000000", "C1", "", "p1", EvidencePolarity.SUPPORT, "q")

    def test_hypothesis_link_does_not_turn_into_support(self) -> None:
        claim = ResearchClaim("C1", "A local mechanism explains the result.", hypothesis_id="H1")
        self.assertEqual(claim.status, ClaimStatus.UNRESOLVED)

    def test_executed_analysis_requires_output_locator(self) -> None:
        with self.assertRaises(ValueError):
            AnalysisArtifact("A1", "Missing output", ArtifactStatus.EXECUTED, command="python analysis.py")


if __name__ == "__main__":
    unittest.main()
