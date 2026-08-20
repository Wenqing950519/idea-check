from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stable_id(prefix: str, *parts: object) -> str:
    material = "|".join(str(part).strip().casefold() for part in parts)
    return f"{prefix}-{hashlib.sha256(material.encode('utf-8')).hexdigest()[:16]}"


class ClaimStatus(str, Enum):
    SUPPORTED = "SUPPORTED"
    PARTIAL = "PARTIAL"
    CONTRADICTED = "CONTRADICTED"
    UNRESOLVED = "UNRESOLVED"


class EvidencePolarity(str, Enum):
    SUPPORT = "SUPPORT"
    PARTIAL = "PARTIAL"
    CONTRADICT = "CONTRADICT"
    CONTEXT = "CONTEXT"


class ArtifactStatus(str, Enum):
    PLANNED = "PLANNED"
    EXECUTED = "EXECUTED"
    FAILED = "FAILED"


class ActionType(str, Enum):
    SEARCH_EXECUTED = "SEARCH_EXECUTED"
    SOURCE_FETCHED = "SOURCE_FETCHED"
    FULLTEXT_PARSED = "FULLTEXT_PARSED"
    SOURCE_INDEXED = "SOURCE_INDEXED"
    EVIDENCE_RETRIEVED = "EVIDENCE_RETRIEVED"
    CITATION_VERIFIED = "CITATION_VERIFIED"
    ANALYSIS_EXECUTED = "ANALYSIS_EXECUTED"
    REVIEW_EXECUTED = "REVIEW_EXECUTED"


@dataclass(slots=True)
class Source:
    source_id: str
    provider: str
    provider_id: str
    title: str
    authors: list[str] = field(default_factory=list)
    year: int | None = None
    doi: str | None = None
    url: str | None = None
    source_type: str = "scholarly_work"
    publication_status: str = "unknown"
    abstract: str = ""
    oa_url: str | None = None
    cited_by_count: int = 0
    referenced_ids: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=utc_now)

    def __post_init__(self) -> None:
        if not self.title.strip():
            raise ValueError("Source title cannot be empty.")
        self.doi = normalize_doi(self.doi)

    @property
    def dedupe_key(self) -> str:
        if self.doi:
            return f"doi:{self.doi}"
        return f"title:{normalize_title(self.title)}:{self.year or ''}"


@dataclass(slots=True)
class Document:
    document_id: str
    source_id: str
    title: str
    content: str
    locator: str
    mime_type: str = "text/plain"
    content_hash: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=utc_now)

    def __post_init__(self) -> None:
        if not self.locator.strip():
            raise ValueError("Document locator cannot be empty.")
        if not self.content_hash:
            self.content_hash = hashlib.sha256(self.content.encode("utf-8")).hexdigest()


@dataclass(slots=True)
class ResearchEvidence:
    evidence_id: str
    source_id: str
    document_id: str
    claim_id: str | None
    passage: str
    locator: str
    polarity: EvidencePolarity
    retrieval_query: str
    score: float = 0.0
    source_quality: str = "UNRATED"
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=utc_now)

    def __post_init__(self) -> None:
        if not self.passage.strip():
            raise ValueError("Evidence requires an exact passage.")
        if not self.locator.strip():
            raise ValueError("Evidence requires a stable locator.")


@dataclass(slots=True)
class ResearchClaim:
    claim_id: str
    text: str
    status: ClaimStatus = ClaimStatus.UNRESOLVED
    evidence_ids: list[str] = field(default_factory=list)
    counterevidence_ids: list[str] = field(default_factory=list)
    hypothesis_id: str | None = None
    rationale: str = ""
    human_review_required: bool = True
    created_at: str = field(default_factory=utc_now)


@dataclass(slots=True)
class Hypothesis:
    hypothesis_id: str
    text: str
    rationale: str
    status: str = "OPEN"
    linked_claim_ids: list[str] = field(default_factory=list)
    created_at: str = field(default_factory=utc_now)


@dataclass(slots=True)
class AnalysisArtifact:
    analysis_id: str
    title: str
    status: ArtifactStatus
    command: str | None = None
    input_locator: str | None = None
    output_locator: str | None = None
    summary: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=utc_now)

    def __post_init__(self) -> None:
        if self.status == ArtifactStatus.EXECUTED and not self.output_locator:
            raise ValueError("Executed analysis requires an output locator.")


@dataclass(slots=True)
class ActionRecord:
    action_id: str
    action_type: ActionType
    status: str
    target_id: str | None = None
    provider: str | None = None
    query: str | None = None
    detail: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=utc_now)


def normalize_doi(value: str | None) -> str | None:
    if not value:
        return None
    normalized = value.strip().casefold()
    for prefix in ("https://doi.org/", "http://doi.org/", "doi:"):
        if normalized.startswith(prefix):
            normalized = normalized[len(prefix):]
    return normalized or None


def normalize_title(value: str) -> str:
    return " ".join("".join(char if char.isalnum() else " " for char in value.casefold()).split())


def to_dict(record: object) -> dict[str, Any]:
    data = asdict(record)
    for key, value in list(data.items()):
        if isinstance(value, Enum):
            data[key] = value.value
    return data


def to_json(record: object) -> str:
    return json.dumps(to_dict(record), ensure_ascii=False, sort_keys=True)
