from __future__ import annotations

import importlib.util
from collections.abc import Callable

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
