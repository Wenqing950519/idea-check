from __future__ import annotations

from abc import ABC, abstractmethod

from src.models import Evidence, SearchTask


class AdapterUnavailableError(RuntimeError):
    pass


class RetrievalAdapter(ABC):
    name = "base"

    @abstractmethod
    def search(self, task: SearchTask) -> list[Evidence]:
        """Return passage-level evidence; never return URL-only records."""

    def available(self) -> bool:
        return True
