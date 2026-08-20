import unittest

from src.models import Claim, Evidence, VerdictLabel
from src.verdict_engine import VerdictEngine
from tests.helpers import load_fixture


class ContradictionTests(unittest.TestCase):
    def test_boundary_condition_prevents_cherry_picked_verification(self) -> None:
        fixture = load_fixture("contradiction.json")
        verdict = VerdictEngine().decide(
            Claim.from_dict(fixture["claim"]),
            [Evidence.from_dict(item) for item in fixture["evidence"]],
        )
        self.assertEqual(verdict.verdict, VerdictLabel.QUALIFIED)
        self.assertIn("BOUNDARY_CONDITION", verdict.risk_flags)
        self.assertEqual(set(verdict.evidence_ids), {"E-004", "E-005"})


if __name__ == "__main__":
    unittest.main()
