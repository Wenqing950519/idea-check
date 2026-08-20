from __future__ import annotations

import re

from .models import Claim, ClaimType, EntailmentJudgment, Evidence, EvidenceRelation


class EntailmentJudge:
    """Apply deterministic safety gates around a supplied or model-produced relation."""

    def judge(self, claim: Claim, evidence: Evidence) -> EntailmentJudgment:
        if evidence.claim_id != claim.claim_id:
            return EntailmentJudgment(claim.claim_id, evidence.evidence_id, EvidenceRelation.IRRELEVANT, "Evidence is linked to a different claim.")
        if not evidence.passage.strip():
            return EntailmentJudgment(claim.claim_id, evidence.evidence_id, EvidenceRelation.UNRESOLVED, "No exact evidence passage was supplied.", "A URL or title alone cannot establish entailment.")

        relation = evidence.relation
        gap = ""
        if claim.claim_type == ClaimType.CAUSAL and relation == EvidenceRelation.DIRECT_SUPPORT and not evidence.causal_design:
            relation = EvidenceRelation.PARTIAL_SUPPORT
            gap = "The passage does not identify a causal design, so causal wording is not established."
        if relation == EvidenceRelation.UNRESOLVED:
            if self._normalize(claim.atomic_claim) == self._normalize(evidence.passage) and evidence.source_quality.value in {"A", "B"}:
                relation = EvidenceRelation.DIRECT_SUPPORT
            else:
                relation = EvidenceRelation.CONTEXT_ONLY
                gap = "Deterministic mode cannot infer entailment from topical or lexical similarity."
        return EntailmentJudgment(
            claim.claim_id,
            evidence.evidence_id,
            relation,
            f"Judgment is based on the exact passage and its declared relation: {relation.value}.",
            gap,
        )

    @staticmethod
    def _normalize(text: str) -> str:
        return re.sub(r"\W+", "", text, flags=re.UNICODE).casefold()
