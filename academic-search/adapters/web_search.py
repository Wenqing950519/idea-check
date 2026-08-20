from __future__ import annotations

from collections.abc import Callable, Iterable
from typing import Any
import zlib

from src.models import Evidence, EvidenceRelation, SearchTask, SourceQuality

from .base import AdapterUnavailableError, RetrievalAdapter


SearchProvider = Callable[[str], Iterable[dict[str, Any]]]


class WebSearchAdapter(RetrievalAdapter):
    """Normalize results from a host-provided web search callable."""

    name = "web_search"

    def __init__(self, provider: SearchProvider | None = None) -> None:
        self.provider = provider

    def available(self) -> bool:
        return self.provider is not None

    def search(self, task: SearchTask) -> list[Evidence]:
        if self.provider is None:
            raise AdapterUnavailableError("No web search provider was injected.")
        evidence: list[Evidence] = []
        for index, item in enumerate(self.provider(task.query), start=1):
            passage = str(item.get("passage", "")).strip()
            locator = str(item.get("document_locator", "")).strip()
            if not passage or not locator:
                continue
            evidence.append(Evidence(
                evidence_id=str(item.get("evidence_id") or self._evidence_id(task, item, index)),
                claim_id=task.claim_id,
                source_title=str(item.get("source_title", "Untitled source")),
                source_author=str(item.get("source_author", "")),
                source_type=str(item.get("source_type", "other")),
                publisher_or_org=str(item.get("publisher_or_org", "")),
                year=item.get("year"),
                url_or_doi=str(item.get("url_or_doi", "")),
                document_locator=locator,
                passage=passage,
                relation=EvidenceRelation(item.get("relation", "UNRESOLVED")),
                source_quality=SourceQuality(item.get("source_quality", "E")),
                retrieval_query=task.query,
                notes=str(item.get("notes", "Host-provided web passage; relation requires judgment.")),
                causal_design=bool(item.get("causal_design", False)),
                scope_match=bool(item.get("scope_match", False)),
                boundary_condition=bool(item.get("boundary_condition", False)),
                citation_key=item.get("citation_key"),
                retrieved_at=item.get("retrieved_at"),
            ))
        return evidence

    @staticmethod
    def _evidence_id(task: SearchTask, item: dict[str, Any], index: int) -> str:
        value = f"{task.claim_id}|{task.priority}|{item.get('url_or_doi', '')}|{item.get('document_locator', '')}|{index}".encode("utf-8")
        return f"E-{zlib.crc32(value):010d}"
