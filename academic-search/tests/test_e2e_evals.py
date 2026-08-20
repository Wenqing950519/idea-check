import json
import tempfile
import unittest
from pathlib import Path

from providers.base import DiscoveryRouter
from providers.openalex import OpenAlexProvider
from src.contracts import AnalysisArtifact, ArtifactStatus, ClaimStatus, EvidencePolarity
from src.integrity import ActionLedgerGuard, IntegrityError
from src.research_engine import ResearchEngine
from src.store import ResearchStore


FIXTURE = Path(__file__).parent / "fixtures" / "openalex_search.json"


class EndToEndEvals(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.store = ResearchStore(Path(self.temp.name) / "research.db")

    def tearDown(self) -> None:
        self.store.close()
        self.temp.cleanup()

    def test_eval_1_local_first_supported_claim(self) -> None:
        engine = ResearchEngine(self.store)
        engine.ingest_text("Local Evidence", "A controlled test found that metadata improved citation selection.", "local://e1")
        result = engine.discover("metadata citation selection", external_if_fewer_than=0)
        hit = result["local_hits"][0]
        engine.accept_hit_as_evidence(hit, "C1", "metadata citation selection", EvidencePolarity.SUPPORT)
        self.assertEqual(engine.evaluate_claim("C1", "Metadata improved citation selection.").status, ClaimStatus.SUPPORTED)

    def test_eval_2_external_openalex_shortlist(self) -> None:
        payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
        router = DiscoveryRouter([OpenAlexProvider(transport=lambda *_: payload)])
        result = ResearchEngine(self.store, router).discover("LLM citation selection", 2, 2025, 2026)
        self.assertEqual(len(result["external_sources"]), 2)
        self.assertEqual(result["external_sources"][1].publication_status, "preprint")

    def test_eval_3_counterevidence_changes_verdict(self) -> None:
        engine = ResearchEngine(self.store)
        engine.ingest_text("Boundary Study", "The intervention had no effect outside the pilot region.", "local://boundary")
        hit = engine.discover("no effect pilot region", external_if_fewer_than=0)["local_hits"][0]
        evidence = engine.accept_hit_as_evidence(hit, "C2", "no effect", EvidencePolarity.CONTRADICT)
        claim = engine.evaluate_claim("C2", "The intervention always improves outcomes.")
        self.assertEqual(claim.status, ClaimStatus.CONTRADICTED)
        self.assertEqual(claim.counterevidence_ids, [evidence.evidence_id])

    def test_eval_4_olist_reproducibility_requires_execution(self) -> None:
        guard = ActionLedgerGuard(self.store)
        with self.assertRaises(IntegrityError):
            guard.require("reproducible", "analysis-olist")
        engine = ResearchEngine(self.store)
        engine.record_analysis(AnalysisArtifact(
            "analysis-olist", "Olist delivery analysis", ArtifactStatus.EXECUTED,
            command="python analysis.py", input_locator="data/orders.csv",
            output_locator="analysis/results.csv",
        ))
        guard.require("reproducible", "analysis-olist")


if __name__ == "__main__":
    unittest.main()
