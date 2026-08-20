from __future__ import annotations

from collections.abc import Callable, Iterable
from typing import Any

from src.models import SearchTask

from .web_search import WebSearchAdapter


class ScholarlyAdapter(WebSearchAdapter):
    """Injected scholarly API/index adapter with the web result contract."""

    name = "scholarly"

    def __init__(self, provider: Callable[[str], Iterable[dict[str, Any]]] | None = None) -> None:
        super().__init__(provider)

    def search(self, task: SearchTask):
        results = super().search(task)
        for item in results:
            if item.source_type == "other":
                item.source_type = "peer_reviewed_paper"
        return results
