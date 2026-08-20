import tempfile
import unittest
from pathlib import Path

from adapters.base import AdapterUnavailableError
from src.contracts import ClaimStatus, ResearchClaim
from src.fulltext import FullTextReader
from src.review import ReviewEngine
from src.store import ResearchStore
from src.writing_integrity import FactLock, claim_diff


class ReviewFullTextWritingTests(unittest.TestCase):
    def test_pdf_fails_with_actionable_optional_parser_message(self) -> None:
        with self.assertRaisesRegex(AdapterUnavailableError, "PaperQA, GROBID"):
            FullTextReader().read("missing.pdf")

    def test_review_catches_unresolved_causal_overclaim(self) -> None:
        with tempfile.TemporaryDirectory() as directory, ResearchStore(Path(directory) / "db.sqlite") as store:
            claim = ResearchClaim("C1", "This intervention causes all customers to buy more.")
            findings = ReviewEngine(store).review([claim], "quick")
            self.assertEqual({item.code for item in findings}, {"UNSUPPORTED_CLAIM", "POTENTIAL_OVERCLAIM"})

    def test_fact_lock_and_claim_diff_detect_stronger_status(self) -> None:
        before = [ResearchClaim("C1", "A tentative relationship exists.")]
        lock = FactLock(before)
        after = [ResearchClaim("C1", "A tentative relationship exists.", status=ClaimStatus.SUPPORTED)]
        self.assertFalse(lock.verify(after))
        self.assertEqual(claim_diff(before, after)[0].field, "status")


if __name__ == "__main__":
    unittest.main()
