from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any


class StringEnum(str, Enum):
    def __str__(self) -> str:
        return self.value


class ClaimType(StringEnum):
    FACTUAL = "FACTUAL"
    CAUSAL = "CAUSAL"
    COMPARATIVE = "COMPARATIVE"
    DEFINITIONAL = "DEFINITIONAL"
    QUANTITATIVE = "QUANTITATIVE"
    PREDICTIVE = "PREDICTIVE"
    GENERALIZATION = "GENERALIZATION"
    METHODOLOGICAL = "METHODOLOGICAL"
    INTERPRETIVE = "INTERPRETIVE"
    NORMATIVE = "NORMATIVE"
    ORIGINAL_HYPOTHESIS = "ORIGINAL_HYPOTHESIS"


class EvidenceRelation(StringEnum):
    DIRECT_SUPPORT = "DIRECT_SUPPORT"
    PARTIAL_SUPPORT = "PARTIAL_SUPPORT"
    CONTEXT_ONLY = "CONTEXT_ONLY"
    QUALIFIES = "QUALIFIES"
    CONTRADICTS = "CONTRADICTS"
    IRRELEVANT = "IRRELEVANT"
    UNRESOLVED = "UNRESOLVED"


class SourceQuality(StringEnum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"


class VerdictLabel(StringEnum):
    VERIFIED = "VERIFIED"
    SUPPORTED = "SUPPORTED"
    QUALIFIED = "QUALIFIED"
    UNVERIFIED = "UNVERIFIED"
    CONTRADICTED = "CONTRADICTED"
    ORIGINAL_HYPOTHESIS = "ORIGINAL_HYPOTHESIS"


class SearchIntent(StringEnum):
    SUPPORT = "SUPPORT"
    DIRECT_SOURCE = "DIRECT_SOURCE"
    CONTRADICTION = "CONTRADICTION"
    BOUNDARY = "BOUNDARY"
    ALTERNATIVE_EXPLANATION = "ALTERNATIVE_EXPLANATION"


@dataclass
class Claim:
    claim_id: str
    parent_id: str | None
    source_location: str
    original_text: str
    atomic_claim: str
    claim_type: ClaimType
    verification_required: bool
    dependencies: list[str]
    author_assertion_level: str
    risk_flags: list[str] = field(default_factory=list)
    notes: str = ""

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Claim":
        values = dict(data)
        values["claim_type"] = ClaimType(values["claim_type"])
        return cls(**{key: values[key] for key in cls.__dataclass_fields__ if key in values})

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result["claim_type"] = self.claim_type.value
        return result


@dataclass
class Evidence:
    evidence_id: str
    claim_id: str
    source_title: str
    source_author: str
    source_type: str
    publisher_or_org: str
    year: int | None
    url_or_doi: str
    document_locator: str
    passage: str
    relation: EvidenceRelation
    source_quality: SourceQuality
    retrieval_query: str
    notes: str
    causal_design: bool = False
    scope_match: bool = False
    boundary_condition: bool = False
    citation_key: str | None = None
    retrieved_at: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Evidence":
        values = dict(data)
        values.setdefault("relation", "UNRESOLVED")
        values.setdefault("source_quality", "E")
        values["relation"] = EvidenceRelation(values["relation"])
        values["source_quality"] = SourceQuality(values["source_quality"])
        return cls(**{key: values[key] for key in cls.__dataclass_fields__ if key in values})

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result["relation"] = self.relation.value
        result["source_quality"] = self.source_quality.value
        return result


@dataclass
class SearchTask:
    claim_id: str
    intent: SearchIntent
    query: str
    priority: int


@dataclass
class VerificationPlan:
    claim_id: str
    tasks: list[SearchTask]
    max_search_budget: int = 5


@dataclass
class AtomizationResult:
    parent: Claim
    children: list[Claim]


@dataclass
class EntailmentJudgment:
    claim_id: str
    evidence_id: str
    relation: EvidenceRelation
    reason: str
    inference_gap: str = ""


@dataclass
class Verdict:
    claim_id: str
    verdict: VerdictLabel
    reason: str
    evidence_ids: list[str]
    inference_gaps: list[str]
    recommended_action: str
    human_review_required: bool
    risk_flags: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result["verdict"] = self.verdict.value
        return result
