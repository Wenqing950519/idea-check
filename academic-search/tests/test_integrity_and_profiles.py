import tempfile
import unittest
from pathlib import Path

from src.contracts import ActionRecord, ActionType, stable_id
from src.integrity import ActionLedgerGuard, IntegrityError
from src.profiles import get_profile
from src.store import ResearchStore


class IntegrityAndProfileTests(unittest.TestCase):
    def test_completion_claim_requires_matching_action(self) -> None:
        with tempfile.TemporaryDirectory() as directory, ResearchStore(Path(directory) / "db.sqlite") as store:
            guard = ActionLedgerGuard(store)
            with self.assertRaises(IntegrityError):
                guard.require("reproducible", "C1")
            store.log_action(ActionRecord(stable_id("ACT", "run"), ActionType.ANALYSIS_EXECUTED, "SUCCESS", target_id="C1"))
            guard.require("reproducible", "C1")

    def test_profiles_have_required_distinct_behaviors(self) -> None:
        geo = get_profile("geo-whitepaper")
        olist = get_profile("olist-business-analysis")
        self.assertIn("official_web", geo.required_steps)
        self.assertIn("analysis_execution", olist.required_steps)
        self.assertGreater(len(olist.coaching_questions), 2)


if __name__ == "__main__":
    unittest.main()
