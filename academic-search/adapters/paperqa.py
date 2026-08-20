from __future__ import annotations

import importlib.util
from collections.abc import Callable, Iterable
from pathlib import Path
from typing import Any

from src.models import Evidence, SearchTask

from .base import AdapterUnavailableError, RetrievalAdapter


class PaperQAAdapter(RetrievalAdapter):
    """Optional boundary for a separately installed PaperQA integration."""

    name = "paperqa"

    def __init__(self, runner: Callable[[SearchTask], list[Evidence]] | None = None) -> None:
        self.runner = runner

    def available(self) -> bool:
        return self.runner is not None and importlib.util.find_spec("paperqa") is not None

    def search(self, task: SearchTask) -> list[Evidence]:
        if not self.available():
            raise AdapterUnavailableError("PaperQA is not installed or no integration runner was provided.")
        assert self.runner is not None
        return [item for item in self.runner(task) if item.passage.strip() and item.document_locator.strip()]

    def index_documents(self, paths: Iterable[str | Path]) -> Any:
        return self._method("index_documents", [str(Path(path)) for path in paths])

    def search_passages(self, task: SearchTask) -> list[Evidence]:
        result = self._method("search_passages", task)
        return [item for item in result if item.passage.strip() and item.document_locator.strip()]

    def gather_evidence(self, question: str) -> Any:
        return self._method("gather_evidence", question)

    def ask_with_evidence(self, question: str) -> Any:
        return self._method("ask_with_evidence", question)

    def find_contradictions(self, claim: str) -> Any:
        return self._method("find_contradictions", claim)

    def _method(self, name: str, argument: Any) -> Any:
        if not self.available():
            raise AdapterUnavailableError("PaperQA is not installed or no integration runner was provided.")
        method = getattr(self.runner, name, None)
        if method is None:
            raise AdapterUnavailableError(f"Configured PaperQA runner does not provide {name}().")
        return method(argument)
