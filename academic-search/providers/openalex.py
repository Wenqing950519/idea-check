from __future__ import annotations

import json
import os
import urllib.parse
import urllib.request
from collections.abc import Callable
from typing import Any

from src.contracts import Source, stable_id

from .base import DiscoveryProvider, DiscoveryQuery, ProviderUnavailableError


Transport = Callable[[str, dict[str, str], float], dict[str, Any]]


class OpenAlexProvider(DiscoveryProvider):
    name = "openalex"
    capabilities = frozenset({"search", "metadata", "citation_graph", "open_access"})
    endpoint = "https://api.openalex.org/works"

    def __init__(
        self,
        api_key: str | None = None,
        transport: Transport | None = None,
        timeout: float = 20.0,
    ) -> None:
        self.api_key = api_key or os.getenv("OPENALEX_API_KEY")
        self._custom_transport = transport is not None
        self.transport = transport or self._http_get
        self.timeout = timeout

    def available(self) -> bool:
        return bool(self.api_key) or self._custom_transport

    def search(self, query: DiscoveryQuery) -> list[Source]:
        if not self.api_key and not self._custom_transport:
            raise ProviderUnavailableError("OPENALEX_API_KEY is not configured.")
        filters: list[str] = []
        if query.year_from and query.year_to:
            filters.append(f"publication_year:{query.year_from}-{query.year_to}")
        elif query.year_from:
            filters.append(f"publication_year:>{query.year_from - 1}")
        elif query.year_to:
            filters.append(f"publication_year:<{query.year_to + 1}")
        for key, value in sorted(query.filters.items()):
            filters.append(f"{key}:{value}")
        params = {
            "search": query.text,
            "per_page": str(min(max(query.limit, 1), 100)),
            "select": "id,doi,display_name,publication_year,publication_date,type,authorships,primary_location,open_access,cited_by_count,referenced_works,abstract_inverted_index,is_retracted",
        }
        if filters:
            params["filter"] = ",".join(filters)
        if self.api_key:
            params["api_key"] = self.api_key
        url = f"{self.endpoint}?{urllib.parse.urlencode(params)}"
        payload = self.transport(url, {"Accept": "application/json", "User-Agent": "academic-search/1.0"}, self.timeout)
        return [self.normalize(record) for record in payload.get("results", [])]

    @staticmethod
    def normalize(record: dict[str, Any]) -> Source:
        provider_id = str(record.get("id", "")).rsplit("/", 1)[-1]
        title = str(record.get("display_name") or "Untitled work")
        authors = [
            str(row.get("author", {}).get("display_name", "")).strip()
            for row in record.get("authorships") or []
            if row.get("author", {}).get("display_name")
        ]
        primary = record.get("primary_location") or {}
        source_meta = primary.get("source") or {}
        oa = record.get("open_access") or {}
        doi = record.get("doi")
        publication_status = "retracted" if record.get("is_retracted") else (
            "preprint" if str(record.get("type", "")).casefold() == "preprint" else "published"
        )
        return Source(
            source_id=stable_id("SRC", "openalex", provider_id or doi or title),
            provider="openalex", provider_id=provider_id, title=title, authors=authors,
            year=record.get("publication_year"), doi=doi,
            url=str(record.get("id") or "") or None,
            source_type=str(record.get("type") or "scholarly_work"),
            publication_status=publication_status,
            abstract=OpenAlexProvider._abstract(record.get("abstract_inverted_index")),
            oa_url=oa.get("oa_url") or primary.get("landing_page_url") or primary.get("pdf_url"),
            cited_by_count=int(record.get("cited_by_count") or 0),
            referenced_ids=[str(item).rsplit("/", 1)[-1] for item in record.get("referenced_works") or []],
            metadata={
                "publication_date": record.get("publication_date"),
                "venue": source_meta.get("display_name"),
                "is_oa": bool(oa.get("is_oa")),
                "oa_status": oa.get("oa_status"),
            },
        )

    @staticmethod
    def _abstract(index: dict[str, list[int]] | None) -> str:
        if not index:
            return ""
        positioned = sorted((position, token) for token, positions in index.items() for position in positions)
        return " ".join(token for _, token in positioned)

    @staticmethod
    def _http_get(url: str, headers: dict[str, str], timeout: float) -> dict[str, Any]:
        request = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(request, timeout=timeout) as response:  # noqa: S310
            return json.loads(response.read().decode("utf-8"))
