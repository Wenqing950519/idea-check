from __future__ import annotations

import math
import re
from dataclasses import dataclass, field

from .store import ResearchStore


_SYNONYMS = {
    "purchase": {"buy", "order", "transaction"},
    "buy": {"purchase", "order", "transaction"},
    "citation": {"reference", "cited", "mention"},
    "selection": {"ranking", "choice", "choose"},
    "increase": {"improve", "raise", "growth"},
    "提升": {"增加", "改善", "提高"},
    "引用": {"引文", "參考", "提及"},
}


@dataclass(slots=True)
class RetrievalHit:
    document_id: str
    source_id: str
    title: str
    passage: str
    locator: str
    score: float
    signals: dict[str, float] = field(default_factory=dict)


class HybridRetriever:
    """Deterministic lexical + lightweight semantic + metadata + graph reranker."""

    def __init__(self, store: ResearchStore) -> None:
        self.store = store

    def search(
        self,
        query: str,
        limit: int = 10,
        year_from: int | None = None,
        year_to: int | None = None,
        source_types: set[str] | None = None,
        seed_ids: list[str] | None = None,
    ) -> list[RetrievalHit]:
        candidates = self.store.search_documents(query, max(limit * 5, 20))
        seen = {row["document_id"] for row in candidates}
        # Semantic candidates cannot be discovered from an FTS-only candidate set.
        candidates.extend(row for row in self.store.list_documents(max(limit * 10, 50)) if row["document_id"] not in seen)
        neighbors = self.store.graph_neighbors(seed_ids or [])
        hits: list[RetrievalHit] = []
        for row in candidates:
            source = self.store.get_source(str(row["source_id"])) or {}
            year = source.get("year")
            if year_from and (year is None or year < year_from):
                continue
            if year_to and (year is None or year > year_to):
                continue
            if source_types and source.get("source_type") not in source_types:
                continue
            passage, locator = self._best_passage(str(row["content"]), query)
            lexical = self._overlap(query, passage)
            semantic = self._semantic_similarity(query, passage)
            metadata = 1.0 if query.casefold() in str(row["title"]).casefold() else 0.0
            graph = 1.0 if row["document_id"] in neighbors or row["source_id"] in neighbors else 0.0
            score = 0.45 * lexical + 0.30 * semantic + 0.15 * metadata + 0.10 * graph
            hits.append(RetrievalHit(
                document_id=str(row["document_id"]), source_id=str(row["source_id"]),
                title=str(row["title"]), passage=passage, locator=locator, score=round(score, 6),
                signals={"lexical": lexical, "semantic": semantic, "metadata": metadata, "graph": graph},
            ))
        return sorted(hits, key=lambda hit: (-hit.score, hit.document_id))[:limit]

    @staticmethod
    def _tokens(text: str) -> set[str]:
        return set(re.findall(r"[a-z0-9]{2,}|[\u3400-\u9fff]{2,}", text.casefold()))

    @classmethod
    def _expanded_tokens(cls, text: str) -> set[str]:
        tokens = cls._tokens(text)
        expanded = set(tokens)
        for token in tokens:
            expanded.update(_SYNONYMS.get(token, set()))
        return expanded

    @classmethod
    def _overlap(cls, query: str, passage: str) -> float:
        query_tokens = cls._tokens(query)
        return len(query_tokens & cls._tokens(passage)) / max(1, len(query_tokens))

    @classmethod
    def _semantic_similarity(cls, query: str, passage: str) -> float:
        left, right = cls._expanded_tokens(query), cls._expanded_tokens(passage)
        return len(left & right) / math.sqrt(max(1, len(left) * len(right)))

    @classmethod
    def _best_passage(cls, content: str, query: str) -> tuple[str, str]:
        passages = [part.strip() for part in re.split(r"\n\s*\n", content) if part.strip()] or [content.strip()]
        ranked = sorted(
            enumerate(passages, start=1),
            key=lambda item: (-cls._semantic_similarity(query, item[1]), item[0]),
        )
        index, passage = ranked[0]
        return passage, f"passage-{index}"
