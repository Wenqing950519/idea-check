from __future__ import annotations

import re
import zlib
from dataclasses import dataclass

from src.models import Evidence, EvidenceRelation, SearchTask, SourceQuality

from .base import RetrievalAdapter


@dataclass
class LocalDocument:
    title: str
    text: str
    path: str
    author: str = ""
    year: int | None = None
    source_quality: SourceQuality = SourceQuality.C


class LocalDocumentAdapter(RetrievalAdapter):
    name = "local_document"

    def __init__(self, documents: list[LocalDocument], max_results: int = 5) -> None:
        self.documents = documents
        self.max_results = max_results

    def search(self, task: SearchTask) -> list[Evidence]:
        query_terms = self._terms(task.query)
        ranked: list[tuple[float, LocalDocument, int, str]] = []
        for document in self.documents:
            for index, passage in enumerate(self._passages(document.text), start=1):
                terms = self._terms(passage)
                score = len(query_terms & terms) / max(1, len(query_terms))
                if score > 0:
                    ranked.append((score, document, index, passage))
        ranked.sort(key=lambda item: (-item[0], item[1].path, item[2]))
        results: list[Evidence] = []
        for offset, (_, document, index, passage) in enumerate(ranked[: self.max_results], start=1):
            results.append(Evidence(
                evidence_id=self._evidence_id(task, document.path, index, offset),
                claim_id=task.claim_id,
                source_title=document.title,
                source_author=document.author,
                source_type="local_document",
                publisher_or_org="",
                year=document.year,
                url_or_doi=document.path,
                document_locator=f"passage-{index}",
                passage=passage,
                relation=EvidenceRelation.UNRESOLVED,
                source_quality=document.source_quality,
                retrieval_query=task.query,
                notes="Lexically retrieved local passage; entailment is not yet judged.",
            ))
        return results

    @staticmethod
    def _passages(text: str) -> list[str]:
        paragraphs = [part.strip() for part in re.split(r"\n\s*\n", text) if part.strip()]
        return paragraphs or [text.strip()]

    @staticmethod
    def _terms(text: str) -> set[str]:
        latin = re.findall(r"[A-Za-z0-9_-]{2,}", text.casefold())
        han = re.findall(r"[\u3400-\u9fff]{2,}", text)
        return set(latin + han)

    @staticmethod
    def _evidence_id(task: SearchTask, path: str, index: int, offset: int) -> str:
        value = f"{task.claim_id}|{task.priority}|{path}|{index}|{offset}".encode("utf-8")
        return f"E-{zlib.crc32(value):010d}"
