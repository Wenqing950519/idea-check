import unittest

from src.models import Claim, VerdictLabel
from src.verdict_engine import VerdictEngine
from tests.helpers import load_fixture


class UnverifiedTests(unittest.TestCase):
    def test_local_generalization_stays_original_hypothesis(self) -> None:
        fixture = load_fixture("original_local_hypothesis.json")
        verdict = VerdictEngine().decide(Claim.from_dict(fixture["claim"]), [])
        self.assertEqual(verdict.verdict, VerdictLabel.ORIGINAL_HYPOTHESIS)
        self.assertTrue(verdict.human_review_required)


if __name__ == "__main__":
    unittest.main()
