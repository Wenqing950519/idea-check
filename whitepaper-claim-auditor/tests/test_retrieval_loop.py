import unittest

from adapters.static import StaticEvidenceAdapter
from src.evidence_retriever import EvidenceRetriever, RetrievalState
from src.models import Evidence, SearchIntent, SearchTask
from tests.helpers import load_fixture


class RetrievalLoopTests(unittest.TestCase):
    def test_cross_round_duplicate_passages_are_not_readded(self) -> None:
        fixture = load_fixture("directly_verifiable.json")
        evidence = Evidence.from_dict(fixture["evidence"][0])
        retriever = EvidenceRetriever([StaticEvidenceAdapter([evidence])])
        state = RetrievalState.empty()
        first = retriever.retrieve_next(SearchTask("C-001", SearchIntent.SUPPORT, "query one", 1), state)
        second = retriever.retrieve_next(SearchTask("C-001", SearchIntent.CONTRADICTION, "query two", 2), state)
        self.assertEqual(len(first), 1)
        self.assertEqual(second, [])
        self.assertEqual(len(state.evidence), 1)
        self.assertEqual(state.duplicate_rounds, 1)


if __name__ == "__main__":
    unittest.main()
