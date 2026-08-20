from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

from src.contracts import Source, normalize_title


class ProviderUnavailableError(RuntimeError):
    pass


@dataclass(slots=True)
class DiscoveryQuery:
    text: str
    year_from: int | None = None
    year_to: int | None = None
    limit: int = 25
    filters: dict[str, Any] = field(default_factory=dict)


class DiscoveryProvider(ABC):
    name = "base"
    capabilities: frozenset[str] = frozenset({"search"})

    def available(self) -> bool:
        return True

    @abstractmethod
    def search(self, query: DiscoveryQuery) -> list[Source]:
        raise NotImplementedError


class DiscoveryRouter:
    """Sequential fallback router. Providers are queried only until the target is met."""

    def __init__(self, providers: list[DiscoveryProvider]) -> None:
        self.providers = providers
        self.failures: list[dict[str, str]] = []

    def search(self, query: DiscoveryQuery) -> list[Source]:
        self.failures = []
        merged: dict[str, Source] = {}
        for provider in self.providers:
            if not provider.available():
                self.failures.append({"provider": provider.name, "error": "UNAVAILABLE"})
                continue
            try:
                records = provider.search(query)
            except Exception as exc:  # provider boundary must fail over
                self.failures.append({"provider": provider.name, "error": f"{type(exc).__name__}: {exc}"})
                continue
            for source in records:
                key = source.dedupe_key
                current = merged.get(key)
                if current is None or source.cited_by_count > current.cited_by_count:
                    merged[key] = source
            if len(merged) >= query.limit:
                break
        return sorted(
            merged.values(),
            key=lambda item: (-item.cited_by_count, -(item.year or 0), normalize_title(item.title)),
        )[: query.limit]
