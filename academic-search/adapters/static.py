from __future__ import annotations

from src.models import Evidence, SearchTask

from .base import RetrievalAdapter


class StaticEvidenceAdapter(RetrievalAdapter):
    """Deterministic fixture/manual-evidence adapter."""

    name = "static"

    def __init__(self, evidence: list[Evidence]) -> None:
        self.evidence = evidence

    def search(self, task: SearchTask) -> list[Evidence]:
        return [item for item in self.evidence if item.claim_id == task.claim_id]
