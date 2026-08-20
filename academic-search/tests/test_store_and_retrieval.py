import tempfile
import unittest
from pathlib import Path

from src.hybrid_retrieval import HybridRetriever
from src.research_engine import ResearchEngine
from src.store import ResearchStore


class StoreAndRetrievalTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.store = ResearchStore(Path(self.temp.name) / "research.db")
        self.engine = ResearchEngine(self.store)

    def tearDown(self) -> None:
        self.store.close()
        self.temp.cleanup()

    def test_persistent_source_and_exact_locator_retrieval(self) -> None:
        source, document = self.engine.ingest_text(
            "Citation Study",
            "Unrelated introduction.\n\nStructured metadata improves citation selection in this benchmark.",
            "local://citation-study",
        )
        hits = HybridRetriever(self.store).search("citation selection", limit=3)
        self.assertEqual(hits[0].source_id, source.source_id)
        self.assertEqual(hits[0].document_id, document.document_id)
        self.assertEqual(hits[0].locator, "passage-2")
        self.assertIn("citation selection", hits[0].passage)

    def test_semantic_paraphrase_signal(self) -> None:
        self.engine.ingest_text("Orders", "Customers buy products through marketplace transactions.", "local://orders")
        hits = HybridRetriever(self.store).search("purchase", limit=1)
        self.assertGreater(hits[0].signals["semantic"], 0)

    def test_metadata_filter(self) -> None:
        source, _ = self.engine.ingest_text("Old", "citation ranking evidence", "local://old")
        self.store.connection.execute("UPDATE sources SET year=2020 WHERE source_id=?", (source.source_id,))
        self.store.connection.commit()
        self.assertEqual(HybridRetriever(self.store).search("citation", year_from=2025), [])


if __name__ == "__main__":
    unittest.main()
