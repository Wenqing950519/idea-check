from __future__ import annotations

from pathlib import Path

from providers.base import DiscoveryQuery, DiscoveryRouter

from .contracts import (
    ActionRecord,
    ActionType,
    AnalysisArtifact,
    ArtifactStatus,
    ClaimStatus,
    Document,
    EvidencePolarity,
    ResearchClaim,
    ResearchEvidence,
    Source,
    stable_id,
    utc_now,
)
from .fulltext import FullTextReader
from .hybrid_retrieval import HybridRetriever, RetrievalHit
from .profiles import get_profile
from .store import ResearchStore


class ResearchEngine:
    """Local-first coordinator; evidence state is persisted before conclusions are emitted."""

    def __init__(
        self,
        store: ResearchStore,
        router: DiscoveryRouter | None = None,
        reader: FullTextReader | None = None,
    ) -> None:
        self.store = store
        self.router = router or DiscoveryRouter([])
        self.reader = reader or FullTextReader()
        self.retriever = HybridRetriever(store)

    def ingest_text(
        self,
        title: str,
        text: str,
        locator: str,
        source_type: str = "local_document",
    ) -> tuple[Source, Document]:
        source = Source(
            source_id=stable_id("SRC", "local", locator), provider="local", provider_id=locator,
            title=title, url=locator, source_type=source_type, publication_status="local",
        )
        self.store.upsert_source(source)
        document = Document(
            document_id=stable_id("DOC", source.source_id, text), source_id=source.source_id,
            title=title, content=text, locator=locator,
        )
        self.store.upsert_document(document)
        self._action(ActionType.FULLTEXT_PARSED, document.document_id, provider="local", detail={"locator": locator})
        self._action(ActionType.SOURCE_INDEXED, source.source_id, provider="local", detail={"document_id": document.document_id})
        return source, document

    def ingest_file(self, path: str | Path, title: str | None = None) -> tuple[Source, Document]:
        source_path = Path(path)
        content, mime_type = self.reader.read(source_path)
        source, document = self.ingest_text(title or source_path.stem, content, str(source_path.resolve()))
        document.mime_type = mime_type
        self.store.upsert_document(document)
        return source, document

    def discover(
        self,
        query: str,
        limit: int = 10,
        year_from: int | None = None,
        year_to: int | None = None,
        profile: str = "geo-whitepaper",
        external_if_fewer_than: int = 3,
    ) -> dict[str, object]:
        profile_config = get_profile(profile)
        local = self.retriever.search(query, limit=limit, year_from=year_from, year_to=year_to)
        self._action(ActionType.EVIDENCE_RETRIEVED, None, provider="local", query=query, detail={"hits": len(local)})
        external: list[Source] = []
        if len(local) < external_if_fewer_than:
            external = self.router.search(DiscoveryQuery(query, year_from, year_to, limit))
            status = "SUCCESS" if external else ("FAILED" if self.router.failures else "SUCCESS")
            self._action(ActionType.SEARCH_EXECUTED, None, provider="discovery_router", query=query, status=status,
                         detail={"records": len(external), "failures": self.router.failures})
            for source in external:
                canonical_id = self.store.upsert_source(source)
                self._action(ActionType.SOURCE_FETCHED, canonical_id, provider=source.provider, query=query,
                             detail={"metadata_only": True})
        return {
            "query": query,
            "profile": profile_config.name,
            "local_hits": local,
            "external_sources": external,
            "provider_failures": list(self.router.failures),
        }

    def accept_hit_as_evidence(
        self,
        hit: RetrievalHit,
        claim_id: str,
        query: str,
        polarity: EvidencePolarity = EvidencePolarity.CONTEXT,
    ) -> ResearchEvidence:
        evidence = ResearchEvidence(
            evidence_id=stable_id("EV", claim_id, hit.document_id, hit.locator, hit.passage),
            source_id=hit.source_id, document_id=hit.document_id, claim_id=claim_id,
            passage=hit.passage, locator=hit.locator, polarity=polarity,
            retrieval_query=query, score=hit.score,
        )
        self.store.upsert_evidence(evidence)
        self.store.add_edge(claim_id, polarity.value.casefold(), evidence.evidence_id)
        return evidence

    def evaluate_claim(self, claim_id: str, text: str) -> ResearchClaim:
        evidence = self.store.evidence_for_claim(claim_id)
        supporting = [item.evidence_id for item in evidence if item.polarity == EvidencePolarity.SUPPORT]
        partial = [item.evidence_id for item in evidence if item.polarity == EvidencePolarity.PARTIAL]
        contradicting = [item.evidence_id for item in evidence if item.polarity == EvidencePolarity.CONTRADICT]
        if contradicting and not supporting:
            status = ClaimStatus.CONTRADICTED
            rationale = "Recorded counterevidence contradicts the claim and no direct support is accepted."
        elif supporting and contradicting:
            status = ClaimStatus.PARTIAL
            rationale = "Both supporting evidence and counterevidence are recorded; scope requires qualification."
        elif supporting:
            status = ClaimStatus.SUPPORTED
            rationale = "At least one exact-locator passage is accepted as direct support."
        elif partial:
            status = ClaimStatus.PARTIAL
            rationale = "Evidence addresses only part of the claim or requires qualification."
        else:
            status = ClaimStatus.UNRESOLVED
            rationale = "No accepted passage entails or contradicts the claim."
        claim = ResearchClaim(
            claim_id=claim_id, text=text, status=status,
            evidence_ids=supporting + partial,
            counterevidence_ids=contradicting,
            rationale=rationale,
            human_review_required=status != ClaimStatus.SUPPORTED or bool(contradicting),
        )
        self.store.upsert_claim(claim)
        return claim

    def record_analysis(self, analysis: AnalysisArtifact) -> None:
        """Persist planned/failed work, but log execution only for an actual output-bearing run."""
        self.store.upsert_analysis(analysis)
        if analysis.status == ArtifactStatus.EXECUTED:
            self._action(
                ActionType.ANALYSIS_EXECUTED,
                analysis.analysis_id,
                provider="local_analysis",
                detail={
                    "command": analysis.command,
                    "input_locator": analysis.input_locator,
                    "output_locator": analysis.output_locator,
                },
            )

    def _action(
        self,
        action_type: ActionType,
        target_id: str | None,
        provider: str | None = None,
        query: str | None = None,
        status: str = "SUCCESS",
        detail: dict[str, object] | None = None,
    ) -> None:
        self.store.log_action(ActionRecord(
            action_id=stable_id("ACT", action_type.value, target_id or "", provider or "", query or "", detail or {}, utc_now()),
            action_type=action_type, status=status, target_id=target_id,
            provider=provider, query=query, detail=detail or {},
        ))
