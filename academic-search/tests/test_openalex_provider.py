import json
import unittest
from pathlib import Path

from providers.base import DiscoveryProvider, DiscoveryQuery, DiscoveryRouter
from providers.openalex import OpenAlexProvider
from src.contracts import Source, stable_id


FIXTURE = Path(__file__).parent / "fixtures" / "openalex_search.json"


class FailingProvider(DiscoveryProvider):
    name = "failing"

    def search(self, query: DiscoveryQuery) -> list[Source]:
        raise RuntimeError("offline")


class StaticProvider(DiscoveryProvider):
    name = "static"

    def search(self, query: DiscoveryQuery) -> list[Source]:
        return [Source(stable_id("SRC", "static", "1"), "static", "1", "Fallback Paper", year=2025, doi="10.1/x")]


class OpenAlexProviderTests(unittest.TestCase):
    def test_result_normalization_and_preprint_label(self) -> None:
        payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
        provider = OpenAlexProvider(transport=lambda *_: payload)
        records = provider.search(DiscoveryQuery("citation selection", year_from=2025, year_to=2026, limit=2))
        self.assertEqual(records[0].doi, "10.1000/geo.1")
        self.assertEqual(records[0].authors, ["Ada Researcher"])
        self.assertEqual(records[0].abstract, "Citation selection depends on retrieval")
        self.assertEqual(records[1].publication_status, "preprint")

    def test_provider_failure_falls_back(self) -> None:
        router = DiscoveryRouter([FailingProvider(), StaticProvider()])
        results = router.search(DiscoveryQuery("test", limit=1))
        self.assertEqual(results[0].title, "Fallback Paper")
        self.assertEqual(router.failures[0]["provider"], "failing")

    def test_duplicate_doi_merge_prefers_richer_record(self) -> None:
        first = StaticProvider()
        first.search = lambda _: [Source(stable_id("SRC", "a"), "a", "1", "Title A", doi="https://doi.org/10.1/X", cited_by_count=1)]
        second = StaticProvider()
        second.name = "second"
        second.search = lambda _: [Source(stable_id("SRC", "b"), "b", "2", "Title B", doi="10.1/x", cited_by_count=8)]
        results = DiscoveryRouter([first, second]).search(DiscoveryQuery("x", limit=5))
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].cited_by_count, 8)


if __name__ == "__main__":
    unittest.main()
